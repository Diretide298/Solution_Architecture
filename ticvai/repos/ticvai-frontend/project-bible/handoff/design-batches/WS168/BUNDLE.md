# WS168 — Seat Management Venue Mapping Reference v1.0 board 4

**10 screens · 11 operations · 21 schemas · 4 permissions**

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

- **Every control that can be refused must be gated.** 4 permissions apply here:
  `CAPACITY_CONFIGURE, ORDER_VIEW, PRODUCT_VIEW, WORK_ORDER_MANAGE`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-983` | Inventory Command Center | listDetail | 1 | 0 | — |
| `BO-984` | Real-Time Seat Map | listDetail | 1 | 0 | — |
| `BO-985` | Status Model Configuration | listDetail | 2 | 0 | — |
| `BO-986` | Availability Tracker | listDetail | 1 | 0 | — |
| `BO-987` | Hold Tracker | listDetail | 2 | 0 | — |
| `BO-988` | Reservation Tracker | listDetail | 1 | 0 | — |
| `BO-989` | Sales & Allocation Tracker | listDetail | 2 | 0 | — |
| `BO-990` | Maintenance & Out of Service | listDetail | 2 | 0 | — |
| `BO-991` | Seat History | listDetail | 1 | 0 | — |
| `BO-992` | Audit & Reconciliation | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-985, BO-986, BO-987, BO-989, BO-990, BO-991 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-983",
  "name": "Inventory Command Center",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "4",
   "number": "01",
   "page": 18
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/inventory-command-center-bo-983",
   "component": "apps/venue-management-web/src/routes/access-venue/InventoryCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-984",
    "BO-985",
    "BO-986",
    "BO-987",
    "BO-988",
    "BO-989",
    "BO-990",
    "BO-991",
    "BO-992"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "BO-984",
     "trigger": "Real-Time Seat Map",
     "provenance": "structural — pack board 4 wiring, 19 September 2026"
    },
    {
     "to": "BO-985",
     "trigger": "Status Model Configuration",
     "provenance": "structural — pack board 4 wiring, 19 September 2026"
    },
    {
     "to": "BO-986",
     "trigger": "Availability Tracker",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "carries": [
      "performanceId"
     ]
    },
    {
     "to": "BO-987",
     "trigger": "Hold Tracker",
     "provenance": "structural — pack board 4 wiring, 19 September 2026"
    },
    {
     "to": "BO-988",
     "trigger": "Reservation Tracker",
     "provenance": "structural — pack board 4 wiring, 19 September 2026"
    },
    {
     "to": "BO-989",
     "trigger": "Sales & Allocation Tracker",
     "provenance": "structural — pack board 4 wiring, 19 September 2026"
    },
    {
     "to": "BO-990",
     "trigger": "Maintenance & Out of Service",
     "provenance": "structural — pack board 4 wiring, 19 September 2026"
    },
    {
     "to": "BO-991",
     "trigger": "Seat History",
     "provenance": "structural — pack board 4 wiring, 19 September 2026"
    },
    {
     "to": "BO-992",
     "trigger": "Audit & Reconciliation",
     "provenance": "structural — pack board 4 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Monitor live seat inventory health across all venues and performances. Show total, available, held, reserved, sold, blocked, out-of-service, accessible and discrepancy counts. Filter by tenant, venue, event, performance, layout, section, category, channel and time window. Surface expiring locks, hold spikes, maintenance impact, synchronization lag and oversell risk. Use atomic transitions, optimistic concurrency, idempotent events and immutable history; historical seat facts cannot be silently overwritten. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 18"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "filters",
     "slot": "filters",
     "components": [
      {
       "kind": "selectField",
       "label": "Performance",
       "operation": "getSeatInventory",
       "notes": "Sends `?performanceId=` (required).",
       "provenance": "contract seating.yaml GET /seat-inventory"
      },
      {
       "kind": "selectField",
       "label": "Section",
       "operation": "getSeatInventory",
       "notes": "Sends `?sectionId=`.",
       "provenance": "contract seating.yaml GET /seat-inventory"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Capacity",
       "bindsTo": "SeatInventory.totals",
       "columns": [
        "SeatInventory.totals.capacity"
       ],
       "operation": "getSeatInventory",
       "provenance": "contract seating.yaml GET /seat-inventory"
      },
      {
       "kind": "metricTile",
       "label": "Available",
       "bindsTo": "SeatInventory.totals",
       "columns": [
        "SeatInventory.totals.available"
       ],
       "operation": "getSeatInventory",
       "provenance": "contract seating.yaml GET /seat-inventory"
      },
      {
       "kind": "metricTile",
       "label": "Held / reserved",
       "bindsTo": "SeatInventory.totals",
       "columns": [
        "SeatInventory.totals.held",
        "SeatInventory.totals.reserved"
       ],
       "operation": "getSeatInventory",
       "provenance": "contract seating.yaml GET /seat-inventory"
      },
      {
       "kind": "metricTile",
       "label": "Sold",
       "bindsTo": "SeatInventory.totals",
       "columns": [
        "SeatInventory.totals.sold"
       ],
       "operation": "getSeatInventory",
       "provenance": "contract seating.yaml GET /seat-inventory"
      },
      {
       "kind": "metricTile",
       "label": "Blocked / out of service",
       "bindsTo": "SeatInventory.totals",
       "columns": [
        "SeatInventory.totals.blocked",
        "SeatInventory.totals.outOfService"
       ],
       "operation": "getSeatInventory",
       "provenance": "contract seating.yaml GET /seat-inventory"
      },
      {
       "kind": "metricTile",
       "label": "Discrepancies",
       "columns": [
        "Discrepancies"
       ],
       "notes": "The pack asks for discrepancies; the contract has no field for it.",
       "provenance": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 18"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Seats by state",
       "bindsTo": "SeatInventory.seats",
       "columns": [
        "SeatInventory.seats[].label",
        "SeatInventory.seats[].state",
        "SeatInventory.seats[].holdPoolId",
        "SeatInventory.seats[].orderId",
        "SeatInventory.seats[].expiresAt"
       ],
       "operation": "getSeatInventory",
       "notes": "Sorted by `expiresAt` to surface expiring locks. As of `asOf`.",
       "provenance": "contract seating.yaml GET /seat-inventory"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected seat",
       "bindsTo": "SeatInventory.seats",
       "columns": [
        "SeatInventory.seats[].seatId",
        "SeatInventory.seats[].label",
        "SeatInventory.seats[].state",
        "SeatInventory.seats[].holdPoolId",
        "SeatInventory.seats[].orderId",
        "SeatInventory.seats[].expiresAt",
        "SeatInventory.asOf"
       ],
       "operation": "getSeatInventory",
       "provenance": "contract seating.yaml GET /seat-inventory"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The inventory list.",
   "error": "Could not load. Names which read failed and leaves the inventory untouched.",
   "emptyFirstRun": "No inventory yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the inventory are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getSeatInventory",
    "contract": "seating",
    "purpose": "Every seat state",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-983",
   "workshopBoard": "wireframes/WS143 Seat Management Venue Mapping Reference v1.0 Board 4.dc.html#bo-983"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 18. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Layout drafted 29 September (VM close-out)** from pack Seat_Management_Venue_Mapping_Reference v1.0.pdf p.18; contract seating.yaml GET /seat-inventory. Pack labels with no schema field yet (shown as plain labels): Filters: tenant, venue, event, layout, category, channel, time window, Discrepancies, Accessible count, Hold spikes, Synchronisation lag, Oversell risk.",
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
  "id": "BO-984",
  "name": "Real-Time Seat Map",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "4",
   "number": "02",
   "page": 18
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/real-time-seat-map-bo-984",
   "component": "apps/venue-management-web/src/routes/access-venue/RealTimeSeatMap.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-983"
   ],
   "exitTo": [
    "BO-983"
   ],
   "transitions": [
    {
     "to": "BO-983",
     "trigger": "Back to Inventory Command Center",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Display the current authoritative status of each seat and zone. Render available, locked, held, reserved, sold, blocked, out-of-service and accessible states with an interactive legend. Stream near-real-time state changes with source, transaction reference and event timestamp. Allow authorized drill-down to seat details without permitting unsafe manual state changes. Use atomic transitions, optimistic concurrency, idempotent events and immutable history; historical seat facts cannot be silently overwritten. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 18"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "filters",
     "slot": "filters",
     "components": [
      {
       "kind": "selectField",
       "label": "Performance",
       "operation": "getSeatInventory",
       "notes": "Sends `?performanceId=` (required).",
       "provenance": "contract seating.yaml GET /seat-inventory"
      },
      {
       "kind": "selectField",
       "label": "Section",
       "operation": "getSeatInventory",
       "notes": "Sends `?sectionId=`.",
       "provenance": "contract seating.yaml GET /seat-inventory"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "State legend",
       "bindsTo": "SeatInventory.totals",
       "columns": [
        "SeatInventory.totals.available",
        "SeatInventory.totals.held",
        "SeatInventory.totals.reserved",
        "SeatInventory.totals.sold",
        "SeatInventory.totals.blocked",
        "SeatInventory.totals.outOfService"
       ],
       "operation": "getSeatInventory",
       "notes": "Interactive legend: one count per state.",
       "provenance": "contract seating.yaml GET /seat-inventory"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Seat states",
       "bindsTo": "SeatInventory.seats",
       "columns": [
        "SeatInventory.seats[].seatId",
        "SeatInventory.seats[].label",
        "SeatInventory.seats[].state"
       ],
       "operation": "getSeatInventory",
       "notes": "Drawn as the seat map coloured by `state`; the list is the accessible fallback. Seat geometry comes from the map, not this read.",
       "provenance": "contract seating.yaml GET /seat-inventory"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "Seat detail",
       "bindsTo": "SeatInventory.seats",
       "columns": [
        "SeatInventory.seats[].label",
        "SeatInventory.seats[].state",
        "SeatInventory.seats[].holdPoolId",
        "SeatInventory.seats[].orderId",
        "SeatInventory.seats[].expiresAt",
        "Source",
        "Transaction reference",
        "Event timestamp"
       ],
       "operation": "getSeatInventory",
       "notes": "Read-only; the pack forbids unsafe manual state changes here.",
       "provenance": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 18"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The real-time seat map list.",
   "error": "Could not load. Names which read failed and leaves the real-time seat map untouched.",
   "emptyFirstRun": "No real-time seat map yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the real-time seat map are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getSeatInventory",
    "contract": "seating",
    "purpose": "The live map",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-984",
   "workshopBoard": "wireframes/WS143 Seat Management Venue Mapping Reference v1.0 Board 4.dc.html#bo-984"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 18. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Layout drafted 29 September (VM close-out)** from pack Seat_Management_Venue_Mapping_Reference v1.0.pdf p.18; contract seating.yaml GET /seat-inventory. Pack labels with no schema field yet (shown as plain labels): Locked state, Accessible flag, Source, Transaction reference, Event timestamp, Seat geometry for map rendering.",
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
  "id": "BO-985",
  "name": "Status Model Configuration",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "4",
   "number": "03",
   "page": 18
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/status-model-configuration-bo-985",
   "component": "apps/venue-management-web/src/routes/access-venue/StatusModelConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-983"
   ],
   "exitTo": [
    "BO-983"
   ],
   "transitions": [
    {
     "to": "BO-983",
     "trigger": "Back to Inventory Command Center",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Define the permitted seat lifecycle and transition rules. Maintain status code, label, color, terminal flag, availability effect, channel visibility and inventory treatment. Configure allowed transitions, required reason, approval, timeout, event source and compensating action. Simulate changes and prohibit circular, orphaned or ambiguous transitions before activation. Use atomic transitions, optimistic concurrency, idempotent events and immutable history; historical seat facts cannot be silently overwritten. Configuration Scope of Work | Version 1.0 18 Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 18"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 18"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listSeatCategories",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createSeatCategory",
       "label": "Create seat category",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createSeatCategory"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The status model list.",
   "error": "Could not load. Names which read failed and leaves the status model untouched.",
   "emptyFirstRun": "No status model yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the status model are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listSeatCategories",
    "contract": "seating",
    "purpose": "The status and category model",
    "trigger": "onLoad"
   },
   {
    "operationId": "createSeatCategory",
    "contract": "seating",
    "purpose": "Add a category",
    "trigger": "onAction",
    "invalidates": [
     "listSeatCategories"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-985",
   "workshopBoard": "wireframes/WS143 Seat Management Venue Mapping Reference v1.0 Board 4.dc.html#bo-985"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 18. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-986",
  "name": "Availability Tracker",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "4",
   "number": "04",
   "page": 19
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/availability-tracker-bo-986",
   "component": "apps/venue-management-web/src/routes/access-venue/AvailabilityTracker.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-983"
   ],
   "exitTo": [
    "BO-983"
   ],
   "transitions": [
    {
     "to": "BO-983",
     "trigger": "Back to Inventory Command Center",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Analyze current and historical seat availability. Show available quantity by venue, performance, section, row, category, price band and sales channel. Graph availability over time and identify material changes caused by locks, holds, reservations, sales or blocks. Provide secured export and links to the exact transactions or events underlying each change. Use atomic transitions, optimistic concurrency, idempotent events and immutable history; historical seat facts cannot be silently overwritten. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 19"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 19"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "detailPanel",
       "derived": true,
       "impliedBy": "getSeatAvailability",
       "notes": "One record, read-only."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The availability tracker list.",
   "error": "Could not load. Names which read failed and leaves the availability tracker untouched.",
   "emptyFirstRun": "No availability tracker yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the availability tracker are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getSeatAvailability",
    "contract": "seating",
    "purpose": "What is free",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-986",
   "workshopBoard": "wireframes/WS143 Seat Management Venue Mapping Reference v1.0 Board 4.dc.html#bo-986"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 19. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "performanceId",
     "from": "navigation"
    }
   ]
  },
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
  "id": "BO-987",
  "name": "Hold Tracker",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "4",
   "number": "05",
   "page": 19
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/hold-tracker-bo-987",
   "component": "apps/venue-management-web/src/routes/access-venue/HoldTracker.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-983"
   ],
   "exitTo": [
    "BO-983"
   ],
   "transitions": [
    {
     "to": "BO-983",
     "trigger": "Back to Inventory Command Center",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Track active and historical held inventory regardless of hold type. List hold ID, type, owner, event, section/seat set, quantity, created time, expiry, priority and status. Filter upcoming expiry, extended, converted, released and conflicting holds and open the governing rule. Allow approved release, extend or reassign actions while preserving the original hold record. Use atomic transitions, optimistic concurrency, idempotent events and immutable history; historical seat facts cannot be silently overwritten. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 19"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 19"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listSeatBlocks",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "detailPanel",
       "derived": true,
       "impliedBy": "getSeatHold",
       "notes": "One record, read-only."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The hold tracker list.",
   "error": "Could not load. Names which read failed and leaves the hold tracker untouched.",
   "emptyFirstRun": "No hold tracker yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the hold tracker are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listSeatBlocks",
    "contract": "seating",
    "purpose": "Holds in force",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "getSeatHold",
    "contract": "seating",
    "purpose": "One hold",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-987",
   "workshopBoard": "wireframes/WS143 Seat Management Venue Mapping Reference v1.0 Board 4.dc.html#bo-987"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 19. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "holdId",
     "from": "navigation"
    }
   ]
  },
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
  "id": "BO-988",
  "name": "Reservation Tracker",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "4",
   "number": "06",
   "page": 19
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/reservation-tracker-bo-988",
   "component": "apps/venue-management-web/src/routes/access-venue/ReservationTracker.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-983"
   ],
   "exitTo": [
    "BO-983"
   ],
   "transitions": [
    {
     "to": "BO-983",
     "trigger": "Back to Inventory Command Center",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Monitor seat reservations and temporary allocations before final sale. List reservation, guest/group, source, seat set, lock/hold reference, expiry, payment state and confirmation status. Identify abandoned, timed-out, payment-pending, orphaned and channel-mismatched reservations. Support controlled retry, release, re-link or escalation without bypassing payment or inventory authority. Use atomic transitions, optimistic concurrency, idempotent events and immutable history; historical seat facts cannot be silently overwritten. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 19"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "filters",
     "slot": "filters",
     "components": [
      {
       "kind": "selectField",
       "label": "Performance",
       "operation": "getSeatInventory",
       "notes": "Sends `?performanceId=` (required).",
       "provenance": "contract seating.yaml GET /seat-inventory"
      },
      {
       "kind": "selectField",
       "label": "Issue",
       "notes": "Abandoned, timed-out, payment-pending, orphaned, channel-mismatched.",
       "provenance": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 19"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Reserved",
       "bindsTo": "SeatInventory.totals",
       "columns": [
        "SeatInventory.totals.reserved"
       ],
       "operation": "getSeatInventory",
       "provenance": "contract seating.yaml GET /seat-inventory"
      },
      {
       "kind": "metricTile",
       "label": "Held",
       "bindsTo": "SeatInventory.totals",
       "columns": [
        "SeatInventory.totals.held"
       ],
       "operation": "getSeatInventory",
       "provenance": "contract seating.yaml GET /seat-inventory"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Reservations",
       "bindsTo": "SeatInventory.seats",
       "columns": [
        "Reservation",
        "Guest / group",
        "Source",
        "SeatInventory.seats[].label",
        "SeatInventory.seats[].holdPoolId",
        "SeatInventory.seats[].orderId",
        "SeatInventory.seats[].expiresAt",
        "Payment state",
        "Confirmation status"
       ],
       "operation": "getSeatInventory",
       "notes": "Seats whose `state` is reserved or held. Reservation, guest, source, payment and confirmation are pack labels.",
       "provenance": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 19"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected reservation",
       "bindsTo": "SeatInventory.seats",
       "columns": [
        "SeatInventory.seats[].seatId",
        "SeatInventory.seats[].label",
        "SeatInventory.seats[].state",
        "SeatInventory.seats[].holdPoolId",
        "SeatInventory.seats[].orderId",
        "SeatInventory.seats[].expiresAt",
        "Reservation",
        "Guest / group",
        "Payment state",
        "Issue type"
       ],
       "operation": "getSeatInventory",
       "notes": "Only the seat side of the reservation is bound.",
       "provenance": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 19"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "secondaryButton",
       "label": "Retry",
       "provenance": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 19"
      },
      {
       "kind": "secondaryButton",
       "label": "Re-link",
       "provenance": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 19"
      },
      {
       "kind": "destructiveButton",
       "label": "Release",
       "provenance": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 19"
      },
      {
       "kind": "secondaryButton",
       "label": "Escalate",
       "provenance": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 19"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The reservation tracker list.",
   "error": "Could not load. Names which read failed and leaves the reservation tracker untouched.",
   "emptyFirstRun": "No reservation tracker yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the reservation tracker are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getSeatInventory",
    "contract": "seating",
    "purpose": "Reserved against sold",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-988",
   "workshopBoard": "wireframes/WS143 Seat Management Venue Mapping Reference v1.0 Board 4.dc.html#bo-988"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 19. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Layout drafted 29 September (VM close-out)** from pack Seat_Management_Venue_Mapping_Reference v1.0.pdf p.19; contract seating.yaml GET /seat-inventory. Pack labels with no schema field yet (shown as plain labels): Reservation ID, Guest / group, Source channel, Payment state, Confirmation status, Issue type (abandoned, timed-out, payment-pending, orphaned, channel-mismatched).",
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
  "id": "BO-989",
  "name": "Sales & Allocation Tracker",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "4",
   "number": "07",
   "page": 19
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/sales-allocation-tracker-bo-989",
   "component": "apps/venue-management-web/src/routes/access-venue/SalesAllocationTracker.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-983"
   ],
   "exitTo": [
    "BO-983"
   ],
   "transitions": [
    {
     "to": "BO-983",
     "trigger": "Back to Inventory Command Center",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Trace sold seats and inventory allocation across channels and partners. Report seats and revenue by web, mobile, POS, call center, box office, B2B reseller and partner API. Show allocation-versus-sold performance, remaining quota, order, ticket, price, fee and fulfillment status. Detect duplicate issue, invalid allocation, reversed payment and seat/order inconsistency. Use atomic transitions, optimistic concurrency, idempotent events and immutable history; historical seat facts cannot be silently overwritten. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history. Configuration Scope of Work | Version 1.0 19",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 19"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 19"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listSeatHoldPools",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The sales allocation tracker list.",
   "error": "Could not load. Names which read failed and leaves the sales allocation tracker untouched.",
   "emptyFirstRun": "No sales allocation tracker yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the sales allocation tracker are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getSeatInventory",
    "contract": "seating",
    "purpose": "Sales and allocation",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listSeatHoldPools",
    "contract": "seating",
    "purpose": "Allocation pools",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-989",
   "workshopBoard": "wireframes/WS143 Seat Management Venue Mapping Reference v1.0 Board 4.dc.html#bo-989"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 19. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-990",
  "name": "Maintenance & Out of Service",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "4",
   "number": "08",
   "page": 20
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/maintenance-out-of-service-bo-990",
   "component": "apps/venue-management-web/src/routes/access-venue/MaintenanceOutOfService.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-983"
   ],
   "exitTo": [
    "BO-983"
   ],
   "transitions": [
    {
     "to": "BO-983",
     "trigger": "Back to Inventory Command Center",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Control seats unavailable because of defects, inspection or venue work. Create or link work orders with seat/area, issue, severity, status, owner, due date and supporting evidence. Block affected inventory, identify sold/reserved seats and trigger reseating or guest-service workflows. Return seats to available only after required repair, inspection, approval and layout validation. Use atomic transitions, optimistic concurrency, idempotent events and immutable history; historical seat facts cannot be silently overwritten. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 20"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 20"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createSeatBlock",
       "label": "Create seat block",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createSeatBlock"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The maintenance out service list.",
   "error": "Could not load. Names which read failed and leaves the maintenance out service untouched.",
   "emptyFirstRun": "No maintenance out service yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the maintenance out service are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createSeatBlock",
    "contract": "seating",
    "purpose": "Take a seat out of service",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getSeatInventory",
     "listSeatBlocks"
    ]
   },
   {
    "operationId": "createWorkOrder",
    "contract": "maintenance",
    "purpose": "Raise the repair",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-990",
   "workshopBoard": "wireframes/WS143 Seat Management Venue Mapping Reference v1.0 Board 4.dc.html#bo-990"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 20. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-991",
  "name": "Seat History",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "4",
   "number": "09",
   "page": 20
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/seat-history-bo-991",
   "component": "apps/venue-management-web/src/routes/access-venue/SeatHistory.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-983"
   ],
   "exitTo": [
    "BO-983"
   ],
   "transitions": [
    {
     "to": "BO-983",
     "trigger": "Back to Inventory Command Center",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Present the complete chronological history of one seat for one performance or physical venue position. Show locks, holds, reservations, sales, releases, refunds, exchanges, scans, blocks and maintenance events. Preserve business timestamp, processing timestamp, source, actor, correlation ID, rule/version and related object. Provide authorized links to order, ticket, guest, hold, approval and device records with field masking. Use atomic transitions, optimistic concurrency, idempotent events and immutable history; historical seat facts cannot be silently overwritten. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 20"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 20"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listSeats",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The seat history list.",
   "error": "Could not load. Names which read failed and leaves the seat history untouched.",
   "emptyFirstRun": "No seat history yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the seat history are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listSeats",
    "contract": "seating",
    "purpose": "List seats in a map",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-991",
   "workshopBoard": "wireframes/WS143 Seat Management Venue Mapping Reference v1.0 Board 4.dc.html#bo-991"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 20. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "seatMapId",
     "from": "navigation"
    }
   ],
   "coldEntry": "**Reached from the list that owns it**, so the identifier arrives with the navigation. Opened cold without one, the screen says what is missing and offers that list — never an empty form that looks configurable."
  },
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
  "id": "BO-992",
  "name": "Audit & Reconciliation",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "4",
   "number": "10",
   "page": 20
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/audit-reconciliation-bo-992",
   "component": "apps/venue-management-web/src/routes/access-venue/AuditReconciliation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-983"
   ],
   "exitTo": [
    "BO-983"
   ],
   "transitions": [
    {
     "to": "BO-983",
     "trigger": "Back to Inventory Command Center",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Detect and resolve differences between authoritative inventory and connected systems. Compare state and quantity across Seat Inventory, Cart, Order, Payment, Ticket, Channel and Access systems. Queue discrepancies by severity, age, venue, performance, type and suspected source with recommended action. Require reason and approval for corrections, use compensating events and retain complete before/after evidence. Use atomic transitions, optimistic concurrency, idempotent events and immutable history; historical seat facts cannot be silently overwritten. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history. Configuration Scope of Work | Version 1.0 20 Board 5 - Seat Selection & Cart Experience Figure 5. High-definition configuration board with all 10 screens. Visual reference: information architecture and configuration coverage; detailed production behavior is defined in the following scope. Configuration Scope of Work | Version 1.0 21",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 20"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "filters",
     "slot": "filters",
     "components": [
      {
       "kind": "selectField",
       "label": "Performance",
       "operation": "getSeatReconciliation",
       "notes": "Sends `?performanceId=` (required).",
       "provenance": "contract seating.yaml GET /seat-reconciliation"
      },
      {
       "kind": "selectField",
       "label": "Discrepancy type",
       "operation": "getSeatReconciliation",
       "notes": "Client-side on `kind`.",
       "provenance": "contract seating.yaml GET /seat-reconciliation"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Open discrepancies",
       "bindsTo": "SeatDiscrepancy",
       "columns": [
        "SeatDiscrepancy.kind"
       ],
       "operation": "getSeatReconciliation",
       "notes": "Counted by `kind`.",
       "provenance": "contract seating.yaml GET /seat-reconciliation"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Discrepancy queue",
       "bindsTo": "SeatDiscrepancy",
       "columns": [
        "SeatDiscrepancy.label",
        "SeatDiscrepancy.kind",
        "SeatDiscrepancy.mapState",
        "SeatDiscrepancy.orderState",
        "SeatDiscrepancy.orderIds",
        "SeatDiscrepancy.detectedAt",
        "Severity",
        "Suspected source",
        "Recommended action"
       ],
       "operation": "getSeatReconciliation",
       "notes": "Age is computed from `detectedAt`. Severity, suspected source and recommended action are pack labels.",
       "provenance": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 20"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected discrepancy",
       "bindsTo": "SeatDiscrepancy",
       "columns": [
        "SeatDiscrepancy.seatId",
        "SeatDiscrepancy.label",
        "SeatDiscrepancy.kind",
        "SeatDiscrepancy.mapState",
        "SeatDiscrepancy.orderState",
        "SeatDiscrepancy.orderIds",
        "SeatDiscrepancy.detectedAt",
        "Cart state",
        "Payment state",
        "Ticket state",
        "Access state"
       ],
       "operation": "getSeatReconciliation",
       "notes": "The pack compares seven systems; the contract compares map and order only.",
       "provenance": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 20"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Correct with reason",
       "notes": "Correction needs reason and approval through a compensating event; no write operation is bound.",
       "provenance": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 20"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The audit reconciliation list.",
   "error": "Could not load. Names which read failed and leaves the audit reconciliation untouched.",
   "emptyFirstRun": "No audit reconciliation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the audit reconciliation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getSeatReconciliation",
    "contract": "seating",
    "purpose": "The map against the orders",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-992",
   "workshopBoard": "wireframes/WS143 Seat Management Venue Mapping Reference v1.0 Board 4.dc.html#bo-992"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 20. 0 of 0 labels bound to a contract property; 0 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Layout drafted 29 September (VM close-out)** from pack Seat_Management_Venue_Mapping_Reference v1.0.pdf p.20; contract seating.yaml GET /seat-reconciliation. Pack labels with no schema field yet (shown as plain labels): Severity, Suspected source, Recommended action, Cart / payment / ticket / channel / access state, Venue.",
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
 "createSeatBlock": {
  "method": "POST",
  "path": "/seat-blocks",
  "contract": "seating",
  "summary": "Block seats from sale",
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
  "requestBody": "CreateSeatBlockRequest",
  "responds": "SeatBlock"
 },
 "createSeatCategory": {
  "method": "POST",
  "path": "/seat-categories",
  "contract": "seating",
  "summary": "Create a seat category",
  "permission": "CAPACITY_CONFIGURE",
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
  "responds": "SeatCategory"
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
 "getSeatHold": {
  "method": "GET",
  "path": "/seat-holds/{holdId}",
  "contract": "seating",
  "summary": "Read a hold",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "SeatHold"
 },
 "getSeatInventory": {
  "method": "GET",
  "path": "/seat-inventory",
  "contract": "seating",
  "summary": "Every seat's state for a performance, in one read",
  "permission": "CAPACITY_CONFIGURE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "performanceId",
    "in": "query",
    "required": true
   },
   {
    "name": "sectionId",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "SeatInventory"
 },
 "getSeatReconciliation": {
  "method": "GET",
  "path": "/seat-reconciliation",
  "contract": "seating",
  "summary": "The map against the orders, seat by seat",
  "permission": "CAPACITY_CONFIGURE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "performanceId",
    "in": "query",
    "required": true
   }
  ],
  "requestBody": null,
  "responds": "SeatDiscrepancy"
 },
 "listSeatBlocks": {
  "method": "GET",
  "path": "/seat-blocks",
  "contract": "seating",
  "summary": "List seat blocks",
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
    "name": "reason",
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
 "listSeatCategories": {
  "method": "GET",
  "path": "/seat-categories",
  "contract": "seating",
  "summary": "List seat categories",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "venueId",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "SeatCategory"
 },
 "listSeatHoldPools": {
  "method": "GET",
  "path": "/seat-hold-pools",
  "contract": "seating",
  "summary": "Held seats, by pool, with what is left and when it releases",
  "permission": "CAPACITY_CONFIGURE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "performanceId",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "SeatHoldPool"
 },
 "listSeats": {
  "method": "GET",
  "path": "/seat-maps/{seatMapId}/seats",
  "contract": "seating",
  "summary": "List seats in a map",
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
    "name": "rowLabel",
    "in": "query",
    "required": null
   },
   {
    "name": "categoryId",
    "in": "query",
    "required": null
   },
   {
    "name": "attribute",
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
 "BlockReason": {
  "type": "string",
  "description": "`other` is allowed only with a note (decided 28 September, audit R222). Every block already requires `note`, so an `other` block always says why; the notes are reviewed quarterly to add the real reasons they reveal.\n",
  "enum": [
   "productionHold",
   "houseSeats",
   "groupAllocation",
   "maintenance",
   "accessibilityReserve",
   "distancing",
   "other"
  ]
 },
 "CreateSeatBlockRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "performanceId",
   "seatIds",
   "reason",
   "note"
  ],
  "properties": {
   "performanceId": {
    "type": "string",
    "format": "uuid"
   },
   "seatIds": {
    "type": "array",
    "minItems": 1,
    "items": {
     "type": "string"
    }
   },
   "reason": {
    "$ref": "#/components/schemas/BlockReason"
   },
   "note": {
    "type": "string",
    "minLength": 3,
    "maxLength": 500
   },
   "releaseAt": {
    "type": "string",
    "format": "date-time",
    "description": "Automatic release, for production holds freed close to performance."
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
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
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
    "allOf": [
     {
      "$ref": "#/components/schemas/WorkOrderPriority"
     }
    ],
    "description": "**Optional since 29 September** (M17-01). Sent, it is `manual` and wins. Absent, the asset's `priorityOverride` applies, and failing that the venue's `WorkOrderPriorityPolicy` scores the fault.\n"
   },
   "faultAssessment": {
    "$ref": "#/components/schemas/WorkOrderFaultAssessment"
   },
   "requiredQualificationCodes": {
    "type": "array",
    "maxItems": 10,
    "items": {
     "type": "string"
    },
    "description": "Skills the job needs, as qualification codes; `suggestWorkOrderAssignee` ranks by them (M17-13)."
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
 "Point": {
  "type": "object",
  "required": [
   "x",
   "y"
  ],
  "properties": {
   "x": {
    "type": "number"
   },
   "y": {
    "type": "number"
   }
  }
 },
 "Seat": {
  "x-ticvai-persistence": "seating.seat",
  "type": "object",
  "required": [
   "id",
   "sectionCode",
   "rowLabel",
   "seatNumber",
   "attribute"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "**Stable for the life of the seat.** Section, row and number are display labels that change on a refit; this does not. A ticket sold today must still resolve after a renumbering.\n"
   },
   "sectionCode": {
    "type": "string"
   },
   "rowLabel": {
    "type": "string"
   },
   "seatNumber": {
    "type": "string"
   },
   "displayLabel": {
    "type": "string",
    "description": "What the guest sees, e.g. `A2-7-11`."
   },
   "position": {
    "allOf": [
     {
      "$ref": "#/components/schemas/Point"
     }
    ],
    "nullable": true
   },
   "categoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "attribute": {
    "$ref": "#/components/schemas/SeatAttribute"
   },
   "companionSeatIds": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Present on accessible seats. Sold together, released together."
   },
   "isActive": {
    "type": "boolean"
   }
  }
 },
 "SeatAttribute": {
  "type": "string",
  "description": "BL-168. **Extended from eight values on 18 August.** Amenity and view filters needed attributes the original set did not carry, and a guest filtering for *aisle seat with power* was filtering on something the model could not express.\n",
  "enum": [
   "standard",
   "accessible",
   "companion",
   "obstructedView",
   "restrictedLegroom",
   "premium",
   "houseSeat",
   "buffer",
   "aisle",
   "endOfRow",
   "extraLegroom",
   "powerOutlet",
   "tableService",
   "shaded",
   "covered",
   "nearExit",
   "nearAccessibleWc",
   "wheelchairTransfer",
   "limitedRecline",
   "sofa",
   "beanbag"
  ]
 },
 "SeatAvailability": {
  "x-ticvai-persistence": "none — computed from seat, hold and block",
  "type": "object",
  "required": [
   "performanceId",
   "seatMapId",
   "renderMode",
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
   "renderMode": {
    "type": "string",
    "enum": [
     "graphical",
     "list"
    ],
    "description": "The mode the server actually used. With `mode=auto` this is how a client knows what it got: `list` means the map has no geometry (the seat map's `noGeometry` state), so the client sells from categories and best-available groups and does not draw a plan. `graphical` means every seat carries `position`.\n"
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
   "sections": {
    "type": "array",
    "description": "The map's sections with what a guest screen needs to show the view from each (decided 29 September, rev 3 23SEP-14): the photo where the venue supplied one, otherwise null and the client renders the view from `boundary` and the seat positions. In this response so WEB-007 and GST-049 need no second call.\n",
    "items": {
     "type": "object",
     "required": [
      "code",
      "name"
     ],
     "properties": {
      "code": {
       "type": "string"
      },
      "name": {
       "type": "string"
      },
      "viewAssetId": {
       "type": "string",
       "format": "uuid",
       "nullable": true,
       "description": "As `Section.viewAssetId`. Null means render the view from geometry."
      },
      "boundary": {
       "type": "array",
       "nullable": true,
       "items": {
        "$ref": "#/components/schemas/Point"
       },
       "description": "As `Section.boundary`. Null when `renderMode` is `list`."
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
      },
      "displayLabel": {
       "type": "string",
       "description": "What the guest sees, e.g. `A2-7-11`, as on `Seat`."
      },
      "position": {
       "allOf": [
        {
         "$ref": "#/components/schemas/Point"
        }
       ],
       "nullable": true,
       "description": "The seat's coordinates on the map, as on `Seat`. Present when `renderMode` is `graphical`; null when it is `list`."
      }
     }
    }
   }
  }
 },
 "SeatBlock": {
  "x-ticvai-persistence": "seating.seat_block",
  "type": "object",
  "required": [
   "id",
   "performanceId",
   "seatIds",
   "reason",
   "createdAt"
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
   "seatIds": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "reason": {
    "$ref": "#/components/schemas/BlockReason"
   },
   "note": {
    "type": "string"
   },
   "createdByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "releaseAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "releasedAt": {
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
 "SeatCategory": {
  "x-ticvai-persistence": "seating.seat_category",
  "type": "object",
  "required": [
   "id",
   "code",
   "name",
   "venueId",
   "rank"
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
   "displayColour": {
    "type": "string",
    "nullable": true
   },
   "rank": {
    "type": "integer",
    "description": "Ordering for best-seat assignment. Lower is better."
   },
   "seatCount": {
    "type": "integer"
   },
   "priceBands": {
    "type": "array",
    "description": "What a seat in this category costs, by band (decided 28 September, audit R275 (d), from the BO-1045 pack). Written by `createSeatCategory` and `updateSeatCategory`. A band may be narrowed to a sales channel or a customer segment and to a window; where several match a sale, the narrowest wins.\n",
    "items": {
     "$ref": "#/components/schemas/SeatPriceBand"
    }
   }
  }
 },
 "SeatDiscrepancy": {
  "type": "object",
  "description": "Board 4.8. **A seat sold twice and a seat sold to nobody are both invisible until somebody counts.**\n",
  "properties": {
   "seatId": {
    "type": "string",
    "format": "uuid"
   },
   "label": {
    "type": "string"
   },
   "mapState": {
    "type": "string"
   },
   "orderState": {
    "type": "string"
   },
   "orderIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "kind": {
    "type": "string",
    "enum": [
     "soldTwice",
     "soldNotMarked",
     "markedNotSold",
     "heldAndSold",
     "orphanedHold"
    ]
   },
   "detectedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "SeatHold": {
  "x-ticvai-persistence": "seating.seat_hold",
  "type": "object",
  "required": [
   "id",
   "performanceId",
   "seatIds",
   "status",
   "createdAt",
   "expiresAt"
  ],
  "properties": {
   "id": {
    "type": "string"
   },
   "performanceId": {
    "type": "string",
    "format": "uuid"
   },
   "seatIds": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "bufferedSeatIds": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Neighbours implicitly held by a seating rule."
   },
   "status": {
    "type": "string",
    "enum": [
     "held",
     "converted",
     "released",
     "expired"
    ]
   },
   "totalPrice": {
    "x-ticvai-column": "gross_amount",
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "heldByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "extensionCount": {
    "type": "integer"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "SeatHoldPool": {
  "type": "object",
  "x-ticvai-persistence": "seating.hold_pool",
  "description": "Board 6.3. **Utilisation decides next season's allocation.**",
  "required": [
   "holdTypeId",
   "performanceId"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "holdTypeId": {
    "type": "string",
    "format": "uuid"
   },
   "performanceId": {
    "type": "string",
    "format": "uuid"
   },
   "seatIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "seatCount": {
    "type": "integer",
    "readOnly": true
   },
   "usedCount": {
    "type": "integer",
    "readOnly": true
   },
   "releasedCount": {
    "type": "integer",
    "readOnly": true
   },
   "holderName": {
    "type": "string",
    "nullable": true
   },
   "reason": {
    "type": "string",
    "nullable": true
   },
   "releaseAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "active",
     "partiallyReleased",
     "released",
     "expired"
    ]
   },
   "createdBy": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "SeatInventory": {
  "type": "object",
  "description": "Board 4. **One read, because a real-time map assembling four endpoints renders one state late.**\n",
  "properties": {
   "performanceId": {
    "type": "string",
    "format": "uuid"
   },
   "asOf": {
    "type": "string",
    "format": "date-time"
   },
   "totals": {
    "type": "object",
    "properties": {
     "capacity": {
      "type": "integer"
     },
     "available": {
      "type": "integer"
     },
     "held": {
      "type": "integer"
     },
     "reserved": {
      "type": "integer"
     },
     "sold": {
      "type": "integer"
     },
     "blocked": {
      "type": "integer"
     },
     "outOfService": {
      "type": "integer"
     }
    }
   },
   "seats": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "seatId": {
       "type": "string",
       "format": "uuid"
      },
      "label": {
       "type": "string"
      },
      "state": {
       "type": "string",
       "enum": [
        "available",
        "held",
        "reserved",
        "sold",
        "blocked",
        "outOfService",
        "killed"
       ]
      },
      "holdPoolId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "orderId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "expiresAt": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      }
     }
    }
   }
  }
 },
 "SeatPriceBand": {
  "x-ticvai-persistence": "seating.seat_price_band",
  "type": "object",
  "description": "One price band on a seat category (decided 28 September, audit R275 (d)). The currency is `amount.currency`, resolved from the region like every `Money` (ADR-0018), so the band carries no currency of its own.\n",
  "required": [
   "code",
   "displayLabel",
   "amount",
   "effectiveFrom"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "seatCategoryId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "code": {
    "type": "string",
    "maxLength": 64,
    "description": "Unique within the category."
   },
   "displayLabel": {
    "type": "string",
    "maxLength": 200
   },
   "displayColour": {
    "type": "string",
    "nullable": true,
    "pattern": "^#[0-9A-Fa-f]{6}$"
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "channel": {
    "nullable": true,
    "description": "Null means every channel.",
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/SalesChannel"
     }
    ]
   },
   "customerSegmentId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "A `marketing-crm` customer segment; null means everyone."
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date-time"
   },
   "effectiveTo": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "Null means open-ended."
   }
  }
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
 "WorkOrder": {
  "x-ticvai-persistence": "maintenance.work_order",
  "x-ticvai-retired-columns": [
   "is_overdue"
  ],
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
    "x-ticvai-derived": "onWrite",
    "description": "**Measured from out-of-service to back-in-service, not from work start to work end.** A ride down for six hours of which two were spent working is down six hours, and the gap between the two numbers is the thing worth managing.\n**Maintained on write**: set when the asset returns to service, as the minutes from the `maintenance.asset_status_change` row that took it out carrying this work order's id to the asset's next change back to `inService`. Null while the asset is still out, and for a work order that never took it out.\n"
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
    "type": "string",
    "format": "uuid"
   },
   "workOrderNumber": {
    "type": "string",
    "readOnly": true,
    "description": "**Server-assigned: the venue prefix plus a sequence per venue** (decided 28 September, audit R152). Not gapless; only tax invoices are gapless, per legal entity.\n"
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
    "nullable": true,
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "The asset's name, copied when the work order is raised or its asset changes, and not updated when the asset is later renamed — the record reads as it was raised.\n"
   },
   "status": {
    "$ref": "#/components/schemas/WorkOrderStatus"
   },
   "priority": {
    "$ref": "#/components/schemas/WorkOrderPriority"
   },
   "priorityScore": {
    "type": "integer",
    "minimum": 0,
    "maximum": 100,
    "nullable": true,
    "readOnly": true,
    "description": "The score the venue's policy gave the fault when raised; null when a person or the asset set the priority (M17-01)."
   },
   "prioritySource": {
    "type": "string",
    "enum": [
     "scored",
     "assetOverride",
     "manual"
    ],
    "readOnly": true,
    "description": "Where `priority` came from (M17-01). A change through `updateWorkOrder` makes it `manual`."
   },
   "faultAssessment": {
    "$ref": "#/components/schemas/WorkOrderFaultAssessment"
   },
   "requiredQualificationCodes": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Skills the job needs (M17-13)."
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
   "categoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "As raised in `CreateWorkOrderRequest.categoryId`, amendable by `updateWorkOrder`. The category is what `completeWorkOrder` reads to decide whether completion photographs are required.\n"
   },
   "locationDescription": {
    "type": "string",
    "maxLength": 500,
    "nullable": true,
    "description": "Where the fault is, as raised. Needed where there is no asset — a broken tile, a leak in a corridor.\n"
   },
   "elapsedMinutes": {
    "type": "integer",
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "Labour minutes accumulated up to the last pause or stop. **Maintained on write** by `recordWorkOrderTime`, `pauseWorkOrder` and `completeWorkOrder`; while `isTimerRunning` is true the interval since the last start is not yet included.\n"
   },
   "isTimerRunning": {
    "type": "boolean",
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "Maintained on write by `startWorkOrder`, `resumeWorkOrder`, `recordWorkOrderTime`, `pauseWorkOrder` and `completeWorkOrder`.\n"
   },
   "dueAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "isOverdue": {
    "type": "boolean",
    "readOnly": true,
    "x-ticvai-persisted": false,
    "x-ticvai-derived": "onRead",
    "description": "`dueAt` is in the past and the status is still `open`, `assigned`, `inProgress`, `paused` or `awaitingParts`. **Computed on read and not stored** — it depends on the clock. `listWorkOrders?overdueOnly` applies the same test to `due_at`.\n"
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
    "format": "uuid",
    "nullable": true
   },
   "sourceIncidentId": {
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
 "WorkOrderFaultAssessment": {
  "x-ticvai-persistence": "none — columns on maintenance.work_order",
  "type": "object",
  "description": "What the person raising a fault says about it, which the priority score reads (M17-01).",
  "properties": {
   "safetyRisk": {
    "type": "boolean",
    "default": false
   },
   "guestImpact": {
    "type": "string",
    "enum": [
     "none",
     "degraded",
     "closed"
    ],
    "default": "none"
   }
  }
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
