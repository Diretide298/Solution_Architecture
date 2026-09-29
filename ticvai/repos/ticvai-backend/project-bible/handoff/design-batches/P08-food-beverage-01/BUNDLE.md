# P08-food-beverage-01 — P08 · Food & Beverage

**8 screens · 34 operations · 31 schemas · 9 permissions**

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

- **Every control that can be refused must be gated.** 9 permissions apply here:
  `ORDER_CREATE, ORDER_MODIFY, ORDER_VIEW, PRODUCT_CONFIGURE, PRODUCT_VIEW, REPORT_VIEW_VENUE, SCOPE_VIEW, TENANT_CONFIGURE, TENANT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-020` | F&B Order Management | listDetail | 11 | 7 | — |
| `BO-021` | Order Search | statusTracker | 2 | 1 | — |
| `BO-045` | Menu Management | listDetail | 12 | 7 | — |
| `BO-046` | Kitchen Display | listDetail | 5 | 3 | — |
| `BO-104` | Food & Beverage | listDetail | 4 | 1 | — |
| `BO-134` | Kitchen & Preparation Stations | listDetail | 4 | 1 | — |
| `BO-135` | Order Routing & KDS/Printer Rules | listDetail | 2 | 1 | — |
| `BO-136` | F&B Global Settings & Controls | listDetail | 5 | 2 | — |

## Thin screens in this batch

**BO-021 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-020",
  "name": "F&B Order Management",
  "module": "Food & Beverage",
  "requiresModule": "fnb",
  "wave": 1,
  "implementation": {
   "app": "venue-management-web",
   "route": "/fnb/bo-020",
   "component": "apps/venue-management-web/src/routes/fnb/BO020List.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-104"
   ],
   "exitTo": [
    "BO-104"
   ],
   "inferred": false,
   "notes": "**Returns to BO-104.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "BO-104",
     "trigger": "Food & Beverage",
     "provenance": "derived — BO-104 declares entryState.params  and BO-020 holds none of them, so the edge carries nothing and BO-104 opens cold"
    },
    {
     "to": "GST-025",
     "trigger": "Tracks the order",
     "provenance": "flow F11 step 5→6",
     "crossesDevice": true,
     "back": false,
     "carries": [
      "orderId"
     ]
    }
   ]
  },
  "notes": "Restored 20 August when the P15 build was rolled back. **Named `Timed Entry Rules` and carrying eleven F&B order operations.** Timed entry is an admission profile; this is the order desk. The client board calls it *Active Order Management & Fulfilment Journey*. **Purpose corrected 24 August.** The screen was renamed *F&B Order Management* and its purpose still read *\"Control how early and how late a ticket admits\"* — **timed entry, on a screen whose every operation is `fnb`.** A rename that moves the label and leaves the sentence is worse than no rename: the name is what a reader scans and the purpose is what they trust.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listFnbOrders` reads the population and `getFnbOrder` reads one of them — list, select, act",
  "purpose": "Take, amend and route an F&B order from the back office — and see what the kitchen is working on.",
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
       "operation": "listFnbOrders",
       "notes": "Sends `?outletId=` to `listFnbOrders`.",
       "provenance": "contract fnb.yaml GET /fnb-orders"
      },
      {
       "kind": "textField",
       "label": "Table visit id",
       "operation": "listFnbOrders",
       "notes": "Sends `?tableVisitId=` to `listFnbOrders`.",
       "provenance": "contract fnb.yaml GET /fnb-orders"
      },
      {
       "kind": "textField",
       "label": "Status",
       "operation": "listFnbOrders",
       "notes": "Sends `?status=` to `listFnbOrders`.",
       "provenance": "contract fnb.yaml GET /fnb-orders"
      },
      {
       "kind": "dataTable",
       "label": "Every F&B order",
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
        "FnbOrder.recordedAt"
       ],
       "operation": "listFnbOrders",
       "provenance": "contract fnb.yaml GET /fnb-orders"
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
        "KitchenStation.isActive"
       ],
       "operation": "listKitchenStations",
       "provenance": "contract fnb.yaml GET /kitchen/stations"
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
       "provenance": "contract fnb.yaml GET /kitchen/tickets"
      },
      {
       "kind": "confirmDialog",
       "derived": true,
       "label": "Confirm",
       "notes": "**The consequence goes in the body, not the title.** *Cancel 3 orders worth AED 480* is a confirmation; *are you sure* is not — and a dialog that cannot name what it destroys is a dialog somebody dismisses.\n\n**Added 31 August.** `confirmDialog` and `modal` were both in the component library and used **zero times across 492 screens**, while `destructiveButton` was used 39 times and its own entry reads *always requires confirmation*.",
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
       "label": "The selected F&B order",
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
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Accept F&B order",
       "operation": "acceptFnbOrder",
       "provenance": "contract fnb.yaml POST /fnb-orders/{orderId}/accept"
      },
      {
       "kind": "secondaryButton",
       "label": "Save kitchen ticket status",
       "operation": "setKitchenTicketStatus",
       "provenance": "contract fnb.yaml PUT /kitchen/tickets/{ticketId}/status"
      },
      {
       "kind": "secondaryButton",
       "label": "Amend F&B order",
       "operation": "amendFnbOrder",
       "provenance": "contract fnb.yaml PATCH /fnb-orders/{orderId}"
      },
      {
       "kind": "destructiveButton",
       "label": "Cancel F&B order",
       "operation": "cancelFnbOrder",
       "notes": "**Cancelling an accepted order is a void and needs `ORDER_VOID`** (decided 28 September, audit R091 (5)); before acceptance `ORDER_MODIFY` is enough. Without it the server answers 403 void-permission-required and the dialog says so.",
       "provenance": "contract fnb.yaml POST /fnb-orders/{orderId}/cancel"
      },
      {
       "kind": "secondaryButton",
       "label": "Create F&B order",
       "operation": "createFnbOrder",
       "provenance": "contract fnb.yaml POST /fnb-orders"
      },
      {
       "kind": "secondaryButton",
       "label": "Prioritise kitchen ticket",
       "operation": "prioritiseKitchenTicket",
       "provenance": "contract fnb.yaml POST /kitchen/tickets/{ticketId}/prioritise"
      },
      {
       "kind": "secondaryButton",
       "label": "Save kitchen stations",
       "operation": "setKitchenStations",
       "provenance": "contract fnb.yaml PUT /kitchen/stations"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmCancelFnbOrder",
    "component": "confirmDialog",
    "trigger": "Cancel F&B order",
    "body": "**Names what `cancelFnbOrder` changes and what it leaves alone**, in the consequence rather than the verb. A order this affects should be identified in the dialog, not just counted. **Collects what `cancelFnbOrder` sends before it is called.** Required: `recordedAt`, `reason`. Optional: `note`, `recordWaste`. Once the order is accepted the reason comes from the void reason list (guestChangedMind, enteredInError, itemUnavailable, qualityIssue, duplicate, other), **Other makes the note required**, and the act needs `ORDER_VOID` (decided 28 September, audit R125 (4), R091 (5), R222).",
    "provenance": "contract fnb.yaml POST /fnb-orders/{orderId}/cancel"
   },
   {
    "id": "formAcceptFnbOrder",
    "component": "modal",
    "trigger": "Accept F&B order",
    "body": "**Collects what `acceptFnbOrder` sends before it is called.** Required: `recordedAt`. Optional: `estimatedReadyAt`, `stationId`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Accept F&B order",
     "operation": "acceptFnbOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "recordedAt",
      "estimatedReadyAt",
      "stationId"
     ]
    },
    "provenance": "contract fnb.yaml POST /fnb-orders/{orderId}/accept"
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
    "id": "formAmendFnbOrder",
    "component": "modal",
    "trigger": "Amend F&B order",
    "body": "**Collects what `amendFnbOrder` sends before it is called.** Nothing in the body is required. Optional: `addLines`, `removeLineIds`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Amend F&B order",
     "operation": "amendFnbOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "addLines",
      "removeLineIds"
     ]
    },
    "provenance": "contract fnb.yaml PATCH /fnb-orders/{orderId}"
   },
   {
    "id": "formCreateFnbOrder",
    "component": "modal",
    "trigger": "Create F&B order",
    "body": "**Collects what `createFnbOrder` sends before it is called.** Required: `id`, `outletId`, `serviceMode`, `lines`, `recordedAt`. Optional: `tableVisitId`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateFnbOrderRequest",
    "confirm": {
     "label": "Create F&B order",
     "operation": "createFnbOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "outletId",
      "serviceMode",
      "lines",
      "recordedAt",
      "tableVisitId"
     ]
    },
    "provenance": "contract fnb.yaml POST /fnb-orders"
   },
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
  "states": {
   "loading": "The order list.",
   "error": "Could not load. Names which read failed and leaves the order untouched.",
   "emptyFirstRun": "No order yet. Offers Create F&B order (`createFnbOrder`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on outletId, tableVisitId, status and the order are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `ORDER_VIEW`, which `getFnbOrder` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "acceptFnbOrder",
    "contract": "fnb",
    "purpose": "The outlet takes the order",
    "trigger": "onAction",
    "invalidates": [
     "listFnbOrders"
    ]
   },
   {
    "operationId": "setKitchenTicketStatus",
    "contract": "fnb",
    "purpose": "Advance a kitchen ticket",
    "trigger": "onAction",
    "invalidates": [
     "listFnbOrders"
    ]
   },
   {
    "operationId": "amendFnbOrder",
    "contract": "fnb",
    "purpose": "Amend an order before it is prepared",
    "trigger": "onAction",
    "invalidates": [
     "listFnbOrders"
    ]
   },
   {
    "operationId": "cancelFnbOrder",
    "contract": "fnb",
    "purpose": "Cancel an order",
    "trigger": "onAction",
    "invalidates": [
     "listFnbOrders"
    ]
   },
   {
    "operationId": "createFnbOrder",
    "contract": "fnb",
    "purpose": "Place an F&B order",
    "trigger": "onAction",
    "invalidates": [
     "listFnbOrders"
    ]
   },
   {
    "operationId": "getFnbOrder",
    "contract": "fnb",
    "purpose": "Read an F&B order",
    "trigger": "onAction"
   },
   {
    "operationId": "listFnbOrders",
    "contract": "fnb",
    "purpose": "List F&B orders",
    "trigger": "onLoad"
   },
   {
    "operationId": "listKitchenStations",
    "contract": "fnb",
    "purpose": "List preparation stations and their routing",
    "trigger": "onLoad"
   },
   {
    "operationId": "listKitchenTickets",
    "contract": "fnb",
    "purpose": "Kitchen ticket queue",
    "trigger": "onLoad"
   },
   {
    "operationId": "prioritiseKitchenTicket",
    "contract": "fnb",
    "purpose": "Move a ticket up the queue",
    "trigger": "onAction",
    "invalidates": [
     "listFnbOrders"
    ]
   },
   {
    "operationId": "setKitchenStations",
    "contract": "fnb",
    "purpose": "Configure stations and item routing",
    "trigger": "onAction",
    "invalidates": [
     "listFnbOrders"
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
     "name": "orderId",
     "from": "deepLink"
    },
    {
     "name": "ticketId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "An order opened from a list or a link. A kitchen ticket opened from the rail.",
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-020"
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
  "id": "BO-021",
  "name": "Order Search",
  "module": "Food & Beverage",
  "requiresModule": "fnb",
  "wave": 1,
  "implementation": {
   "app": "venue-management-web",
   "route": "/fnb/bo-021",
   "component": "apps/venue-management-web/src/routes/fnb/BO021List.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-104"
   ],
   "exitTo": [
    "BO-104"
   ],
   "inferred": false,
   "notes": "**Returns to BO-104.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "BO-104",
     "trigger": "Food & Beverage",
     "provenance": "derived — BO-104 declares entryState.params  and BO-021 holds none of them, so the edge carries nothing and BO-104 opens cold"
    },
    {
     "to": "POS-002",
     "trigger": "Sell — Ticket Catalogue",
     "provenance": "flow F81 step 1→2",
     "crossesDevice": true,
     "back": false,
     "carries": [
      "orderId"
     ]
    }
   ]
  },
  "notes": "Restored 20 August when the P15 build was rolled back.",
  "density": "compact",
  "boardFrames": [
   "Retail Board 3.dc.html#ret-3a"
  ],
  "pattern": "statusTracker",
  "patternReason": "`getGuestOrderStatus` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "Find any order taken at this venue.",
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
       "provenance": "contract fnb.yaml POST /guest-orders/{orderId}/delivery"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The order search, read by `getGuestOrderStatus`.",
   "error": "Could not load. Names which read failed and leaves the order search untouched.",
   "emptyFirstRun": "No order search yet. Offers Record order handover (`recordOrderHandover`).",
   "emptyNoAccess": "Shown when the caller lacks `ORDER_MODIFY`, which `recordOrderHandover` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "recordOrderHandover",
    "contract": "fnb",
    "purpose": "Record that an order reached the guest",
    "trigger": "onAction"
   },
   {
    "operationId": "getGuestOrderStatus",
    "contract": "fnb",
    "purpose": "Track an order",
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
     "name": "orderId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "An order opened from a list or a link."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-021",
   "derivedFrom": "wireframes/reference/Retail Board 3.dc.html",
   "source": "Claude Design Retail pack, 24 August",
   "note": "**Drawn by Claude Design on `Retail Board 3.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formRecordOrderHandover",
    "component": "modal",
    "trigger": "Record order handover",
    "body": "**Collects what `recordOrderHandover` sends before it is called.** Required: `outcome`, `recordedAt`. Optional: `deliveredToLocationId`, `runnerPrincipalId`, `note`. Dismissing sends nothing; the screen behind is unchanged.",
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
  "id": "BO-045",
  "name": "Menu Management",
  "module": "Food & Beverage",
  "requiresModule": "fnb",
  "wave": 1,
  "implementation": {
   "app": "venue-management-web",
   "route": "/fnb/bo-045",
   "component": "apps/venue-management-web/src/routes/fnb/BO045List.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-007",
    "BO-104"
   ],
   "exitTo": [
    "BO-008",
    "BO-104",
    "BO-111"
   ],
   "inferred": false,
   "notes": "**Returns to BO-104.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product. **flow F31 — the manager re-verifies allergens from the menu being drafted.** The flow is the authority on the journey and the navigation has to agree with it; marking this block non-inferred is what turned the disagreement from a warning into a failure.",
   "transitions": [
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "provenance": "flow F93 step 2→3"
    },
    {
     "to": "BO-104",
     "trigger": "Food & Beverage",
     "provenance": "derived — BO-104 declares entryState.params  and BO-045 holds none of them, so the edge carries nothing and BO-104 opens cold"
    },
    {
     "to": "POS-002",
     "trigger": "The till picks it up in its next catalogue bundle",
     "provenance": "flow F31 step 5→6",
     "operation": "publishMenu",
     "crossesDevice": true,
     "back": false
    },
    {
     "to": "BO-111",
     "trigger": "An item's recipe changed, so its allergens are re-verified",
     "provenance": "flow F31 step 2→3",
     "operation": "applyMenuActions",
     "carries": [
      "menuId",
      "menuItemId"
     ]
    }
   ]
  },
  "notes": "Restored 20 August when the P15 build was rolled back. **Operations from the 24 August F&B build wired here** — the contract grew and the screens had not caught up, which is how 92 operations reached 49% of screens.",
  "density": "compact",
  "boardFrames": [
   "FnB Board 2.dc.html#fnb-2a",
   "FnB Board 2.dc.html#fnb-2b",
   "FnB Board 2.dc.html#fnb-2e",
   "FnB Board 2.dc.html#fnb-2j",
   "FnB Board 2.dc.html#fnb-2k"
  ],
  "pattern": "listDetail",
  "patternReason": "`listMenus` reads the population and `getMenu` reads one of them — list, select, act",
  "purpose": "Change what is on sale and what is in it.",
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
       "operation": "listMenus",
       "notes": "Sends `?outletId=` to `listMenus`.",
       "provenance": "contract fnb.yaml GET /menus"
      },
      {
       "kind": "datePicker",
       "label": "Active at",
       "operation": "listMenus",
       "notes": "Sends `?activeAt=` to `listMenus`.",
       "provenance": "contract fnb.yaml GET /menus"
      },
      {
       "kind": "dataTable",
       "label": "Every menu",
       "bindsTo": "Menu",
       "columns": [
        "Menu.id",
        "Menu.code",
        "Menu.name",
        "Menu.outletId",
        "Menu.availability",
        "Menu.sections",
        "Menu.isActive"
       ],
       "operation": "listMenus",
       "provenance": "contract fnb.yaml GET /menus"
      },
      {
       "kind": "publishGate",
       "impliedBy": "publishMenu",
       "notes": "Declares `publishMenu`. **The gate names what the publish will affect before it happens** — a disabled Publish with no reason is the state operators escalate.\n",
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
       "label": "The selected menu",
       "bindsTo": "Menu",
       "columns": [
        "Menu.id",
        "Menu.code",
        "Menu.name",
        "Menu.outletId",
        "Menu.availability",
        "Menu.sections",
        "Menu.isActive"
       ],
       "operation": "getMenu",
       "provenance": "contract fnb.yaml GET /menus/{menuId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create menu",
       "operation": "createMenu",
       "provenance": "contract fnb.yaml POST /menus"
      },
      {
       "kind": "secondaryButton",
       "label": "Save menu sections",
       "operation": "setMenuSections",
       "provenance": "contract fnb.yaml PUT /menus/{menuId}/sections"
      },
      {
       "kind": "secondaryButton",
       "label": "Save menu",
       "operation": "updateMenu",
       "provenance": "contract fnb.yaml PATCH /menus/{menuId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Publish menu",
       "operation": "publishMenu",
       "provenance": "contract fnb.yaml POST /menus/{menuId}/publish"
      },
      {
       "kind": "secondaryButton",
       "label": "Schedule menu publish",
       "operation": "scheduleMenuPublish",
       "provenance": "contract fnb.yaml POST /menus/{menuId}/schedule"
      },
      {
       "kind": "secondaryButton",
       "label": "Rollback menu",
       "operation": "rollbackMenu",
       "provenance": "contract fnb.yaml POST /menus/{menuId}/rollback"
      },
      {
       "kind": "secondaryButton",
       "label": "Apply menu actions",
       "operation": "applyMenuActions",
       "provenance": "contract fnb.yaml POST /menus/{menuId}/actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Re-check allergens (manual)",
       "operation": "verifyAllergens",
       "notes": "**A manual re-check** (decided 28 September, audit R241). The server already runs `verifyAllergens` after every recipe, substitution or modifier change; this button runs it again on demand.",
       "provenance": "contract fnb.yaml POST /menu-items/{menuItemId}/verify-allergens"
      },
      {
       "kind": "detailPanel",
       "label": "Last allergen verdict",
       "operation": "verifyAllergens",
       "notes": "**Shows the last automatic verdict** — `matches`, `undeclared` (with `via` and `sourceRef`, shown first), `overDeclared` — from the check the server runs after every recipe, substitution or modifier change, with when it ran (decided 28 September, audit R241). **The contract records the verdict but exposes no read of it yet**, so until one exists this panel shows the result of the latest manual re-check; the response is inline and binds to no named schema.",
       "provenance": "contract fnb.yaml POST /menu-items/{menuItemId}/verify-allergens"
      },
      {
       "kind": "publishGate",
       "label": "What publishing changes",
       "notes": "**Names what goes live, where, and from when.** A publish with no stated consequence is one somebody presses meaning to save.",
       "provenance": "authored — required by check-screens"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The menu list.",
   "error": "Could not load. Names which read failed and leaves the menu untouched.",
   "emptyFirstRun": "No menu yet. Offers Create menu (`createMenu`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on outletId, activeAt and the menu are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `PRODUCT_VIEW`, which `listMenus` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listMenus",
    "contract": "fnb",
    "purpose": "List menus",
    "trigger": "onLoad"
   },
   {
    "operationId": "getMenu",
    "contract": "fnb",
    "purpose": "Read a menu with sections and items",
    "trigger": "onAction"
   },
   {
    "operationId": "createMenu",
    "contract": "fnb",
    "purpose": "Create a menu",
    "trigger": "onAction",
    "invalidates": [
     "listMenus"
    ]
   },
   {
    "operationId": "setMenuSections",
    "contract": "fnb",
    "purpose": "Set menu sections and their item ordering",
    "trigger": "onAction",
    "invalidates": [
     "listMenus"
    ]
   },
   {
    "operationId": "updateMenu",
    "contract": "fnb",
    "purpose": "Amend a menu",
    "trigger": "onAction",
    "invalidates": [
     "listMenus"
    ]
   },
   {
    "operationId": "publishMenu",
    "contract": "fnb",
    "purpose": "Make the draft live, now or on a date",
    "trigger": "onAction",
    "invalidates": [
     "listMenus"
    ]
   },
   {
    "operationId": "scheduleMenuPublish",
    "contract": "fnb",
    "purpose": "Publish it on a date, not now",
    "trigger": "onAction",
    "invalidates": [
     "listMenus"
    ]
   },
   {
    "operationId": "rollbackMenu",
    "contract": "fnb",
    "purpose": "Put the previous version back",
    "trigger": "onAction",
    "invalidates": [
     "listMenus"
    ]
   },
   {
    "operationId": "applyMenuActions",
    "contract": "fnb",
    "purpose": "Do the same thing to many items at once",
    "trigger": "onAction",
    "invalidates": [
     "listMenus"
    ]
   },
   {
    "operationId": "verifyAllergens",
    "contract": "fnb",
    "purpose": "Does this dish still match its claim? Runs automatically after every change; here a manual re-check (audit R241)",
    "trigger": "onAction",
    "invalidates": [
     "listMenus"
    ]
   },
   {
    "operationId": "createModifierGroup",
    "contract": "fnb",
    "purpose": "Create a modifier group",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listMenus",
     "getMenu"
    ]
   },
   {
    "operationId": "attachModifierGroup",
    "contract": "fnb",
    "purpose": "Give a menu item its choices",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listMenus",
     "getMenu"
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
     "name": "menuId",
     "from": "deepLink"
    },
    {
     "name": "menuItemId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "A menu opened from the list. An item opened from the menu. **Allergen verification is per item** — a menu-wide check is a job, not a screen.",
   "preloaded": [
    "Menu.id",
    "Menu.code",
    "Menu.name",
    "Menu.outletId",
    "Menu.availability"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-045",
   "derivedFrom": "wireframes/reference/FnB Board 2.dc.html",
   "source": "Claude Design F&B pack, 24 August",
   "note": "**Drawn by Claude Design on `FnB Board 2.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 10 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formCreateMenu",
    "component": "modal",
    "trigger": "Create menu",
    "body": "**Collects what `createMenu` sends before it is called.** Required: `code`, `name`, `outletId`. Optional: `availability`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateMenuRequest",
    "confirm": {
     "label": "Create menu",
     "operation": "createMenu"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "code",
      "name",
      "outletId",
      "availability"
     ]
    },
    "provenance": "contract fnb.yaml POST /menus"
   },
   {
    "id": "formSetMenuSections",
    "component": "modal",
    "trigger": "Save menu sections",
    "body": "**Collects what `setMenuSections` sends before it is called.** Required: `sections`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save menu sections",
     "operation": "setMenuSections"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "sections"
     ]
    },
    "provenance": "contract fnb.yaml PUT /menus/{menuId}/sections"
   },
   {
    "id": "formUpdateMenu",
    "component": "modal",
    "trigger": "Save menu",
    "body": "**Collects what `updateMenu` sends before it is called.** Nothing in the body is required. Optional: `name`, `availability`, `isActive`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save menu",
     "operation": "updateMenu"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "name",
      "availability",
      "isActive"
     ]
    },
    "provenance": "contract fnb.yaml PATCH /menus/{menuId}"
   },
   {
    "id": "formPublishMenu",
    "component": "modal",
    "trigger": "Publish menu",
    "body": "**Collects what `publishMenu` sends before it is called.** Nothing in the body is required. Optional: `effectiveAt`, `channels`, `note`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Publish menu",
     "operation": "publishMenu"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "effectiveAt",
      "channels",
      "note"
     ]
    },
    "provenance": "contract fnb.yaml POST /menus/{menuId}/publish"
   },
   {
    "id": "formScheduleMenuPublish",
    "component": "modal",
    "trigger": "Schedule menu publish",
    "body": "**Collects what `scheduleMenuPublish` sends before it is called.** Nothing in the body is required. Optional: `effectiveAt`, `cancelScheduleId`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Schedule menu publish",
     "operation": "scheduleMenuPublish"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "effectiveAt",
      "cancelScheduleId"
     ]
    },
    "provenance": "contract fnb.yaml POST /menus/{menuId}/schedule"
   },
   {
    "id": "formRollbackMenu",
    "component": "modal",
    "trigger": "Rollback menu",
    "body": "**Collects what `rollbackMenu` sends before it is called.** Nothing in the body is required. Optional: `toVersion`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Rollback menu",
     "operation": "rollbackMenu"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "toVersion"
     ]
    },
    "provenance": "contract fnb.yaml POST /menus/{menuId}/rollback"
   },
   {
    "id": "formApplyMenuActions",
    "component": "modal",
    "trigger": "Apply menu actions",
    "body": "**Collects what `applyMenuActions` sends before it is called.** Required: `actions`. Optional: `previewOnly`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Apply menu actions",
     "operation": "applyMenuActions"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "actions",
      "previewOnly"
     ]
    },
    "provenance": "contract fnb.yaml POST /menus/{menuId}/actions"
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
  "id": "BO-046",
  "name": "Kitchen Display",
  "module": "Food & Beverage",
  "requiresModule": "fnb",
  "wave": 1,
  "implementation": {
   "app": "venue-management-web",
   "route": "/fnb/bo-046",
   "component": "apps/venue-management-web/src/routes/fnb/BO046List.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-104"
   ],
   "exitTo": [
    "BO-104"
   ],
   "inferred": false,
   "notes": "**Returns to BO-104.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "BO-104",
     "trigger": "Food & Beverage",
     "provenance": "derived — BO-104 declares entryState.params  and BO-046 holds none of them, so the edge carries nothing and BO-104 opens cold"
    }
   ]
  },
  "notes": "Restored 20 August when the P15 build was rolled back. **Retained in P08 on 20 August when the P15 build was rolled back**, and P15 now owns the kitchen display for the venue floor. **This is the back-office view of the same tickets** — a manager watching the pass from a desk, not a screen at the pass.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listKitchenTickets` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Show the kitchen what to make, in order.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Station id",
       "operation": "listKitchenTickets",
       "notes": "Sends `?stationId=` to `listKitchenTickets`.",
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
       "provenance": "contract fnb.yaml GET /kitchen/tickets"
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
       "provenance": "contract fnb.yaml PUT /kitchen/tickets/{ticketId}/status"
      },
      {
       "kind": "secondaryButton",
       "label": "Prioritise kitchen ticket",
       "operation": "prioritiseKitchenTicket",
       "provenance": "contract fnb.yaml POST /kitchen/tickets/{ticketId}/prioritise"
      },
      {
       "kind": "secondaryButton",
       "label": "Save kitchen stations",
       "operation": "setKitchenStations",
       "provenance": "contract fnb.yaml PUT /kitchen/stations"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The kitchen display list.",
   "error": "Could not load. Names which read failed and leaves the kitchen display untouched.",
   "emptyFirstRun": "No kitchen display yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on stationId, status and the kitchen display are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `ORDER_VIEW`, which `listKitchenTickets` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
    "operationId": "listKitchenStations",
    "contract": "fnb",
    "purpose": "List preparation stations and their routing",
    "trigger": "onLoad"
   },
   {
    "operationId": "prioritiseKitchenTicket",
    "contract": "fnb",
    "purpose": "Move a ticket up the queue",
    "trigger": "onAction",
    "invalidates": [
     "listKitchenTickets"
    ]
   },
   {
    "operationId": "setKitchenStations",
    "contract": "fnb",
    "purpose": "Configure stations and item routing",
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
     "name": "ticketId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "A kitchen ticket opened from the rail.",
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-046"
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
    "id": "formSetKitchenStations",
    "component": "modal",
    "trigger": "Save kitchen stations",
    "body": "**Collects what `setKitchenStations` sends before it is called.** Required: `stations`. **Each station carries its display assignment**, `displayWorkstationIds` — the kitchen displays that show this station's rail. A display belongs to one station; assigning it to a second is refused 400. The kitchen display takes its station from this assignment rather than from a picker on the display (decided 28 September, audit R277). Dismissing sends nothing; the screen behind is unchanged.",
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
  "id": "BO-104",
  "name": "Food & Beverage",
  "module": "Food & Beverage",
  "requiresModule": "core",
  "wave": 1,
  "implementation": {
   "app": "venue-management-web",
   "route": "/food-beverage",
   "component": "apps/venue-management-web/src/routes/home/FoodBeverageList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-020",
    "BO-021",
    "BO-045",
    "BO-046",
    "BO-134",
    "BO-135",
    "BO-136"
   ],
   "transitions": [
    {
     "to": "BO-020",
     "trigger": "F&B Order Management",
     "provenance": "derived — BO-020 declares entryState.params orderId, ticketId and BO-104 holds none of them, so the edge carries nothing and BO-020 opens cold"
    },
    {
     "to": "BO-021",
     "trigger": "Order Search",
     "provenance": "derived — BO-021 declares entryState.params orderId and BO-104 holds none of them, so the edge carries nothing and BO-021 opens cold"
    },
    {
     "to": "BO-045",
     "trigger": "Menu Management",
     "carries": [
      "menuId",
      "menuItemId"
     ],
     "provenance": "derived — BO-045 declares entryState.params menuId, menuItemId and BO-104 holds menuId, menuItemId, so an edge into it carries them"
    },
    {
     "to": "BO-046",
     "trigger": "Kitchen Display",
     "provenance": "derived — BO-046 declares entryState.params ticketId and BO-104 holds none of them, so the edge carries nothing and BO-046 opens cold"
    },
    {
     "to": "BO-134",
     "trigger": "Kitchen & Preparation Stations",
     "provenance": "derived — BO-134 declares entryState.params  and BO-104 holds none of them, so the edge carries nothing and BO-134 opens cold"
    },
    {
     "to": "BO-135",
     "trigger": "Order Routing & KDS/Printer Rules",
     "provenance": "derived — BO-135 declares entryState.params  and BO-104 holds none of them, so the edge carries nothing and BO-135 opens cold"
    },
    {
     "to": "BO-136",
     "trigger": "F&B Global Settings & Controls",
     "provenance": "derived — BO-136 declares entryState.params planId and BO-104 holds none of them, so the edge carries nothing and BO-136 opens cold"
    }
   ]
  },
  "notes": "Section landing. **4 screens reach the entry point through here** — before 20 August they reached it through nothing. **Navigation repointed to P15 on 20 August** — the F&B screens it linked to moved out of the back office when the client board was adopted.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listMenus` reads the population and `getVenueSettings` reads one of them — list, select, act",
  "purpose": "Everything in food & beverage.",
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
       "operation": "listMenus",
       "notes": "Sends `?outletId=` to `listMenus`.",
       "provenance": "contract fnb.yaml GET /menus"
      },
      {
       "kind": "datePicker",
       "label": "Active at",
       "operation": "listMenus",
       "notes": "Sends `?activeAt=` to `listMenus`.",
       "provenance": "contract fnb.yaml GET /menus"
      },
      {
       "kind": "dataTable",
       "label": "Every menu",
       "bindsTo": "Menu",
       "columns": [
        "Menu.id",
        "Menu.code",
        "Menu.name",
        "Menu.outletId",
        "Menu.availability",
        "Menu.sections",
        "Menu.isActive"
       ],
       "operation": "listMenus",
       "provenance": "contract fnb.yaml GET /menus"
      },
      {
       "kind": "metricTile",
       "label": "Takings and admissions today",
       "bindsTo": "KpiValue",
       "columns": [
        "KpiValue.code",
        "KpiValue.name",
        "KpiValue.value",
        "KpiValue.period",
        "KpiValue.comparison",
        "KpiValue.direction"
       ],
       "operation": "getKpiValues",
       "notes": "**Takings and admissions**, from `getKpiValues?kpiCodes=takings,admissions`; with no `period` the period is today in the venue's time zone (decided 28 September, audit R283).",
       "provenance": "contract reporting.yaml GET /kpi-values"
      },
      {
       "kind": "cardList",
       "bindsTo": "screens",
       "notes": "4 screens. **No attention counts** until a summary operation exists to supply them (decided 28 September, audit R283).",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "searchField",
       "label": "Search food & beverage",
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
       "label": "The selected menu",
       "bindsTo": "Menu",
       "columns": [
        "Menu.id",
        "Menu.code",
        "Menu.name",
        "Menu.outletId",
        "Menu.availability",
        "Menu.sections",
        "Menu.isActive",
        "Menu.publishedVersion",
        "Menu.publishedAt"
       ],
       "operation": "listMenus",
       "provenance": "contract fnb.yaml GET /menus"
      },
      {
       "kind": "detailPanel",
       "label": "The venue settings",
       "bindsTo": "VenueSettings",
       "columns": [
        "VenueSettings.id",
        "VenueSettings.venueId",
        "VenueSettings.currencyCode",
        "VenueSettings.currencyScale",
        "VenueSettings.supportHours",
        "VenueSettings.quietHours",
        "VenueSettings.biometrics",
        "VenueSettings.segregatedAccess",
        "VenueSettings.alerting"
       ],
       "operation": "getVenueSettings",
       "provenance": "contract tenancy.yaml GET /venues/{venueId}/settings"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create menu",
       "operation": "createMenu",
       "provenance": "contract fnb.yaml POST /menus"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The list, with counts.",
   "error": "Could not load. Venue Home is still reachable.",
   "emptyFirstRun": "**Nothing configured in food & beverage yet.** The action is the first thing to set up, not a blank list.",
   "emptyNoResults": "Nothing matches the filter.",
   "emptyNoAccess": "You do not have permission for food & beverage. **Said plainly** — an empty section reads as broken."
  },
  "apis": [
   {
    "operationId": "getKpiValues",
    "contract": "reporting",
    "purpose": "Today's takings and admissions tiles — `kpiCodes=takings,admissions`, period defaulting to today (decided 28 September, audit R283)",
    "trigger": "onLoad"
   },
   {
    "operationId": "getVenueSettings",
    "contract": "tenancy",
    "purpose": "What is enabled here",
    "trigger": "onLoad"
   },
   {
    "operationId": "listMenus",
    "contract": "fnb",
    "purpose": "Menus and their state",
    "trigger": "onLoad"
   },
   {
    "operationId": "createMenu",
    "contract": "fnb",
    "purpose": "Start a menu",
    "trigger": "onAction",
    "invalidates": [
     "listMenus"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    }
   ],
   "coldEntry": "**Resolves from the session, so a cold arrival is the ordinary case** — a manager bookmarks the back office and opens it every morning. A principal with more than one venue is asked which before the page renders, rather than shown the first one.",
   "preloaded": [
    "VenueSettings.id",
    "VenueSettings.venueId",
    "VenueSettings.supportHours",
    "VenueSettings.quietHours",
    "VenueSettings.segregatedAccess"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-104"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formCreateMenu",
    "component": "modal",
    "trigger": "Create menu",
    "body": "**Collects what `createMenu` sends before it is called.** Required: `code`, `name`, `outletId`. Optional: `availability`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateMenuRequest",
    "confirm": {
     "label": "Create menu",
     "operation": "createMenu"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "code",
      "name",
      "outletId",
      "availability"
     ]
    },
    "provenance": "contract fnb.yaml POST /menus"
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
  "id": "BO-134",
  "name": "Kitchen & Preparation Stations",
  "module": "Food & Beverage",
  "requiresModule": "fnb",
  "wave": 2,
  "implementation": {
   "app": "venue-management-web",
   "route": "/food-beverage/kitchen-preparation-stations",
   "component": "apps/venue-management-web/src/routes/ops/KitchenPreparationStationsList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-104"
   ],
   "exitTo": [
    "BO-104"
   ],
   "inferred": false,
   "notes": "**Returns to BO-104.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "BO-104",
     "trigger": "Food & Beverage",
     "provenance": "derived — BO-104 declares entryState.params  and BO-134 holds none of them, so the edge carries nothing and BO-104 opens cold"
    }
   ]
  },
  "notes": "**Added 20 August from the client design board.** The operations existed and no screen called them. **Named in the board contents and not written up in it** — the operations are real, the layout is not. **Drawn 31 August** — `FnB Board 1.dc.html` frame `fnb-1h`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Kitchen &amp; Preparation Stations* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.",
  "density": "compact",
  "boardFrames": [
   "FnB Board 1.dc.html#fnb-1h"
  ],
  "pattern": "listDetail",
  "patternReason": "`listKitchenStations` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Kitchen & Preparation Stations — from the client design board, 20 August.",
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
       "provenance": "contract fnb.yaml GET /kitchen/stations"
      },
      {
       "kind": "searchField",
       "label": "Search kitchen",
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
       "provenance": "contract fnb.yaml PUT /kitchen/stations"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The kitchen preparation stations list.",
   "error": "Could not load. Names which read failed and leaves the kitchen preparation stations untouched.",
   "emptyFirstRun": "No kitchen preparation stations yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on outletId and the kitchen preparation stations are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `PRODUCT_VIEW`, which `listKitchenStations` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
   },
   {
    "operationId": "setKitchenSla",
    "contract": "fnb",
    "purpose": "Set how long a ticket may sit before it is late",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listKitchenStations"
    ]
   },
   {
    "operationId": "listOutlets",
    "contract": "tenancy",
    "purpose": "The outlets whose kitchen SLA is set (setKitchenSla is per outlet)",
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
     "from": "session"
    }
   ],
   "coldEntry": "Resolves from the session. A principal with more than one venue is asked which first.",
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-134",
   "derivedFrom": "wireframes/reference/FnB Board 1.dc.html",
   "note": "**Drawn by Claude Design on `FnB Board 1.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formSetKitchenStations",
    "component": "modal",
    "trigger": "Save kitchen stations",
    "body": "**Collects what `setKitchenStations` sends before it is called.** Required: `stations`. **Each station carries its display assignment**, `displayWorkstationIds` — the kitchen displays that show this station's rail. A display belongs to one station; assigning it to a second is refused 400. The kitchen display takes its station from this assignment rather than from a picker on the display (decided 28 September, audit R277). Dismissing sends nothing; the screen behind is unchanged.",
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
  "id": "BO-135",
  "name": "Order Routing & KDS/Printer Rules",
  "module": "Food & Beverage",
  "requiresModule": "fnb",
  "wave": 2,
  "implementation": {
   "app": "venue-management-web",
   "route": "/food-beverage/order-routing-kds-printer-rules",
   "component": "apps/venue-management-web/src/routes/ops/OrderRoutingKdsPrinterRulesList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-104"
   ],
   "exitTo": [
    "BO-104"
   ],
   "inferred": false,
   "notes": "**Returns to BO-104.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "BO-104",
     "trigger": "Food & Beverage",
     "provenance": "derived — BO-104 declares entryState.params  and BO-135 holds none of them, so the edge carries nothing and BO-104 opens cold"
    }
   ]
  },
  "notes": "**Added 20 August from the client design board.** The operations existed and no screen called them. **Named in the board contents and not written up in it** — the operations are real, the layout is not. **Drawn 31 August** — `FnB Board 1.dc.html` frame `fnb-1j`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Order Routing &amp; KDS / Printer Rules* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.",
  "density": "compact",
  "boardFrames": [
   "FnB Board 1.dc.html#fnb-1j"
  ],
  "pattern": "listDetail",
  "patternReason": "`listWorkstations` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Order Routing & KDS/Printer Rules — from the client design board, 20 August.",
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
       "operation": "listWorkstations",
       "notes": "Sends `?venueId=` to `listWorkstations`.",
       "provenance": "contract tenancy.yaml GET /workstations"
      },
      {
       "kind": "textField",
       "label": "Sale board kind",
       "operation": "listWorkstations",
       "notes": "Sends `?saleBoardKind=` to `listWorkstations`.",
       "provenance": "contract tenancy.yaml GET /workstations"
      },
      {
       "kind": "dataTable",
       "label": "Every workstation",
       "bindsTo": "Workstation",
       "columns": [
        "Workstation.id",
        "Workstation.code",
        "Workstation.name",
        "Workstation.venueId",
        "Workstation.regionId",
        "Workstation.departmentId",
        "Workstation.scopePath",
        "Workstation.saleBoard",
        "Workstation.accessPointId",
        "Workstation.devices",
        "Workstation.currency",
        "Workstation.currencyScale"
       ],
       "operation": "listWorkstations",
       "provenance": "contract tenancy.yaml GET /workstations"
      },
      {
       "kind": "searchField",
       "label": "Search order routing",
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
       "label": "The selected workstation",
       "bindsTo": "Workstation",
       "columns": [
        "Workstation.id",
        "Workstation.code",
        "Workstation.name",
        "Workstation.venueId",
        "Workstation.regionId",
        "Workstation.departmentId",
        "Workstation.scopePath",
        "Workstation.saleBoard",
        "Workstation.accessPointId",
        "Workstation.devices",
        "Workstation.currency",
        "Workstation.currencyScale",
        "Workstation.timeZone",
        "Workstation.deploymentProfile",
        "Workstation.edgeNodeId",
        "Workstation.healthScore"
       ],
       "operation": "listWorkstations",
       "provenance": "contract tenancy.yaml GET /workstations"
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
       "provenance": "contract fnb.yaml PUT /kitchen/stations"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The order routing kds list.",
   "error": "Could not load. Names which read failed and leaves the order routing kds untouched.",
   "emptyFirstRun": "No order routing kds yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on venueId, saleBoardKind and the order routing kds are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `SCOPE_VIEW`, which `listWorkstations` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setKitchenStations",
    "contract": "fnb",
    "purpose": "Configure stations and item routing",
    "trigger": "onAction",
    "invalidates": [
     "listWorkstations"
    ]
   },
   {
    "operationId": "listWorkstations",
    "contract": "tenancy",
    "purpose": "List workstations",
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
   "coldEntry": "Resolves from the session. A principal with more than one venue is asked which first.",
   "preloaded": [
    "Workstation.id",
    "Workstation.code",
    "Workstation.name",
    "Workstation.venueId",
    "Workstation.regionId"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-135",
   "derivedFrom": "wireframes/reference/FnB Board 1.dc.html",
   "note": "**Drawn by Claude Design on `FnB Board 1.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
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
  "id": "BO-136",
  "name": "F&B Global Settings & Controls",
  "module": "Food & Beverage",
  "requiresModule": "core",
  "wave": 2,
  "implementation": {
   "app": "venue-management-web",
   "route": "/food-beverage/f-b-global-settings-controls",
   "component": "apps/venue-management-web/src/routes/ops/FBGlobalSettingsControlsList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-104"
   ],
   "exitTo": [
    "BO-104",
    "BO-137"
   ],
   "inferred": false,
   "notes": "**Returns to BO-104.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "BO-137",
     "trigger": "Recipe Consumption & Theoretical Inventory",
     "provenance": "flow F85 step 1→2"
    },
    {
     "to": "BO-104",
     "trigger": "Food & Beverage",
     "provenance": "derived — BO-104 declares entryState.params  and BO-136 holds none of them, so the edge carries nothing and BO-104 opens cold"
    }
   ]
  },
  "notes": "**Added 20 August from the client design board.** The operations existed and no screen called them. **Named in the board contents and not written up in it** — the operations are real, the layout is not.",
  "density": "compact",
  "boardFrames": [
   "FnB Board 2.dc.html#fnb-2m",
   "FnB Board 2.dc.html#fnb-2n",
   "FnB Board 5.dc.html#fnb-5d"
  ],
  "pattern": "listDetail",
  "patternReason": "`listProductionRuns` reads the population and `getVenueSettings` reads one of them — list, select, act",
  "purpose": "F&B Global Settings & Controls — from the client design board, 20 August.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "selectField",
       "label": "Status",
       "operation": "listProductionRuns",
       "notes": "Sends `?status=` to `listProductionRuns`.",
       "provenance": "contract fnb.yaml GET /production-runs"
      },
      {
       "kind": "selectField",
       "label": "Location kind",
       "operation": "listProductionRuns",
       "notes": "Sends `?locationKind=` to `listProductionRuns`.",
       "provenance": "contract fnb.yaml GET /production-runs"
      },
      {
       "kind": "datePicker",
       "label": "From",
       "operation": "listProductionRuns",
       "notes": "Sends `?from=` to `listProductionRuns`.",
       "provenance": "contract fnb.yaml GET /production-runs"
      },
      {
       "kind": "dataTable",
       "label": "Every production run",
       "bindsTo": "ProductionRun",
       "columns": [
        "ProductionRun.id",
        "ProductionRun.recipeId",
        "ProductionRun.producingOutletId",
        "ProductionRun.forOutletIds",
        "ProductionRun.plannedQuantity",
        "ProductionRun.actualQuantity",
        "ProductionRun.scheduledFor",
        "ProductionRun.status",
        "ProductionRun.varianceReason"
       ],
       "operation": "listProductionRuns",
       "provenance": "contract fnb.yaml GET /production-runs"
      },
      {
       "kind": "searchField",
       "label": "Search f",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "publishGate",
       "impliedBy": "releaseProductionPlan",
       "notes": "Declares `releaseProductionPlan`. **The gate names what the publish will affect before it happens** — a disabled Publish with no reason is the state operators escalate.\n",
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
       "label": "The selected production run",
       "bindsTo": "ProductionRun",
       "columns": [
        "ProductionRun.id",
        "ProductionRun.recipeId",
        "ProductionRun.productionPlanId",
        "ProductionRun.producingOutletId",
        "ProductionRun.forOutletIds",
        "ProductionRun.plannedQuantity",
        "ProductionRun.actualQuantity",
        "ProductionRun.scheduledFor",
        "ProductionRun.status",
        "ProductionRun.varianceReason"
       ],
       "operation": "listProductionRuns",
       "provenance": "contract fnb.yaml GET /production-runs"
      },
      {
       "kind": "detailPanel",
       "label": "The venue settings",
       "bindsTo": "VenueSettings",
       "columns": [
        "VenueSettings.id",
        "VenueSettings.venueId",
        "VenueSettings.currencyCode",
        "VenueSettings.currencyScale",
        "VenueSettings.supportHours",
        "VenueSettings.quietHours",
        "VenueSettings.biometrics",
        "VenueSettings.segregatedAccess",
        "VenueSettings.alerting",
        "VenueSettings.fnb"
       ],
       "operation": "getVenueSettings",
       "provenance": "contract tenancy.yaml GET /venues/{venueId}/settings"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save venue settings",
       "operation": "setVenueSettings",
       "provenance": "contract tenancy.yaml PUT /venues/{venueId}/settings"
      },
      {
       "kind": "secondaryButton",
       "label": "Build production plan",
       "operation": "buildProductionPlan",
       "provenance": "contract fnb.yaml POST /production-plans"
      },
      {
       "kind": "secondaryButton",
       "label": "Release production plan",
       "operation": "releaseProductionPlan",
       "provenance": "contract fnb.yaml POST /production-plans/{planId}/release"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The global settings controls list.",
   "error": "Could not load. Names which read failed and leaves the global settings controls untouched.",
   "emptyFirstRun": "No global settings controls yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on status, locationKind, from and the global settings controls are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `TENANT_CONFIGURE`, which `getVenueSettings` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getVenueSettings",
    "contract": "tenancy",
    "purpose": "Operational settings for this venue",
    "trigger": "onLoad"
   },
   {
    "operationId": "setVenueSettings",
    "contract": "tenancy",
    "purpose": "Set support hours, quiet hours, segregated access and alerti",
    "trigger": "onAction",
    "invalidates": [
     "listProductionRuns"
    ]
   },
   {
    "operationId": "buildProductionPlan",
    "contract": "fnb",
    "purpose": "Turn a forecast into a prep list",
    "trigger": "onAction",
    "invalidates": [
     "listProductionRuns"
    ]
   },
   {
    "operationId": "releaseProductionPlan",
    "contract": "fnb",
    "purpose": "Make the plan real",
    "trigger": "onAction",
    "invalidates": [
     "listProductionRuns"
    ]
   },
   {
    "operationId": "listProductionRuns",
    "contract": "fnb",
    "purpose": "What is being made, and what was",
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
     "name": "planId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "Resolves from the session. A principal with more than one venue is asked which first. A plan opened from the list.",
   "preloaded": [
    "VenueSettings.id",
    "VenueSettings.venueId",
    "VenueSettings.supportHours",
    "VenueSettings.quietHours",
    "VenueSettings.segregatedAccess"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-136",
   "derivedFrom": "wireframes/reference/FnB Board 2.dc.html",
   "source": "Claude Design F&B pack, 24 August",
   "note": "**Drawn by Claude Design on `FnB Board 2.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 5 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formSetVenueSettings",
    "component": "modal",
    "trigger": "Save venue settings",
    "body": "**Collects what `setVenueSettings` sends before it is called.** Nothing in the body is required. Optional: `id`, `venueId`, `currencyCode`, `currencyScale`, `supportHours`, `quietHours`, `biometrics`, `segregatedAccess`, `alerting`, and **the configured limits** — `displayCurrencies`, the cart, resale, exchange, reschedule and reservation limits, `shiftVarianceThreshold`, and the `catalogue`, `inventory`, `seating`, `promotions`, `fnb`, `queue` and `reporting` groups (decided 28 September, audit R094). **A limit left empty inherits the tenant default** (null = inherit); each field shows the default it would inherit. **`fnb.foodSafetyLeadPrincipalId` is settable here** — until a food-safety lead is named, escalating a corrective action is refused 409 no-food-safety-lead, and the screen says so (decided 28 September, audit R096 (9)). Dismissing sends nothing; the screen behind is unchanged.",
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
      "alerting",
      "displayCurrencies",
      "catalogue",
      "inventory",
      "seating",
      "promotions",
      "fnb",
      "queue",
      "reporting"
     ]
    },
    "provenance": "contract tenancy.yaml PUT /venues/{venueId}/settings"
   },
   {
    "id": "formBuildProductionPlan",
    "component": "modal",
    "trigger": "Build production plan",
    "body": "**Collects what `buildProductionPlan` sends before it is called.** Required: `id`, `forDate`, `status`, `lines`. Optional: `outletId`, `basedOnSuggestionId`, `releasedRunIds`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "ProductionPlan",
    "confirm": {
     "label": "Build production plan",
     "operation": "buildProductionPlan"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "forDate",
      "status",
      "lines",
      "outletId",
      "basedOnSuggestionId",
      "releasedRunIds"
     ]
    },
    "provenance": "contract fnb.yaml POST /production-plans"
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
 "acceptFnbOrder": {
  "method": "POST",
  "path": "/fnb-orders/{orderId}/accept",
  "contract": "fnb",
  "summary": "The outlet takes the order",
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
 "amendFnbOrder": {
  "method": "PATCH",
  "path": "/fnb-orders/{orderId}",
  "contract": "fnb",
  "summary": "Amend an order before it is prepared",
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
  "responds": "FnbOrder"
 },
 "applyMenuActions": {
  "method": "POST",
  "path": "/menus/{menuId}/actions",
  "contract": "fnb",
  "summary": "Do the same thing to many items at once",
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
  "responds": "MenuActionResult"
 },
 "attachModifierGroup": {
  "method": "PUT",
  "path": "/menu-items/{menuItemId}/modifier-groups",
  "contract": "fnb",
  "summary": "Give an item its choices",
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
  "responds": "MenuItem"
 },
 "buildProductionPlan": {
  "method": "POST",
  "path": "/production-plans",
  "contract": "fnb",
  "summary": "Turn a forecast into a prep list",
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
  "requestBody": "ProductionPlan",
  "responds": "ProductionPlan"
 },
 "cancelFnbOrder": {
  "method": "POST",
  "path": "/fnb-orders/{orderId}/cancel",
  "contract": "fnb",
  "summary": "Cancel an order",
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
 "createMenu": {
  "method": "POST",
  "path": "/menus",
  "contract": "fnb",
  "summary": "Create a menu",
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
  "requestBody": "CreateMenuRequest",
  "responds": "Menu"
 },
 "createModifierGroup": {
  "method": "POST",
  "path": "/modifier-groups",
  "contract": "fnb",
  "summary": "Create a modifier group",
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
  "requestBody": "ModifierGroup",
  "responds": "ModifierGroup"
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
 "getKpiValues": {
  "method": "GET",
  "path": "/kpi-values",
  "contract": "reporting",
  "summary": "Current values, against target, with movement",
  "permission": "REPORT_VIEW_VENUE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "kpiIds",
    "in": "query",
    "required": null
   },
   {
    "name": "kpiCodes",
    "in": "query",
    "required": null
   },
   {
    "name": "scopePath",
    "in": "query",
    "required": null
   },
   {
    "name": "period",
    "in": "query",
    "required": null
   },
   {
    "name": "compareTo",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "KpiValue"
 },
 "getMenu": {
  "method": "GET",
  "path": "/menus/{menuId}",
  "contract": "fnb",
  "summary": "Read a menu with sections and items",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "Menu"
 },
 "getVenueSettings": {
  "method": "GET",
  "path": "/venues/{venueId}/settings",
  "contract": "tenancy",
  "summary": "Operational settings for this venue",
  "permission": "TENANT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "VenueSettings"
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
 "listMenus": {
  "method": "GET",
  "path": "/menus",
  "contract": "fnb",
  "summary": "List menus",
  "permission": "PRODUCT_VIEW",
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
    "name": "activeAt",
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
 "listOutlets": {
  "method": "GET",
  "path": "/outlets",
  "contract": "tenancy",
  "summary": "List outlets",
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
    "name": "kind",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Outlet"
 },
 "listProductionRuns": {
  "method": "GET",
  "path": "/production-runs",
  "contract": "fnb",
  "summary": "What is being made, and what was",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "locationKind",
    "in": "query",
    "required": null
   },
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
 "listWorkstations": {
  "method": "GET",
  "path": "/workstations",
  "contract": "tenancy",
  "summary": "List workstations",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "venueId",
    "in": "query",
    "required": null
   },
   {
    "name": "saleBoardKind",
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
 "publishMenu": {
  "method": "POST",
  "path": "/menus/{menuId}/publish",
  "contract": "fnb",
  "summary": "Make the draft live, now or on a date",
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
  "responds": "MenuVersion"
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
 "releaseProductionPlan": {
  "method": "POST",
  "path": "/production-plans/{planId}/release",
  "contract": "fnb",
  "summary": "Make the plan real",
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
  "responds": "ProductionPlan"
 },
 "rollbackMenu": {
  "method": "POST",
  "path": "/menus/{menuId}/rollback",
  "contract": "fnb",
  "summary": "Put the previous version back",
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
  "responds": "MenuVersion"
 },
 "scheduleMenuPublish": {
  "method": "POST",
  "path": "/menus/{menuId}/schedule",
  "contract": "fnb",
  "summary": "Publish it on a date, not now",
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
  "responds": "MenuSchedule"
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
 "setMenuSections": {
  "method": "PUT",
  "path": "/menus/{menuId}/sections",
  "contract": "fnb",
  "summary": "Set menu sections and their item ordering",
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
  "responds": "Menu"
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
 },
 "updateMenu": {
  "method": "PATCH",
  "path": "/menus/{menuId}",
  "contract": "fnb",
  "summary": "Amend a menu",
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
  "responds": "Menu"
 },
 "verifyAllergens": {
  "method": "POST",
  "path": "/menu-items/{menuItemId}/verify-allergens",
  "contract": "fnb",
  "summary": "Does this dish still match its claim?",
  "permission": "PRODUCT_VIEW",
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
  "responds": "AllergenVerdict"
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
 "AllergenVerdict": {
  "x-ticvai-persistence": "fnb.allergen_verdict",
  "type": "object",
  "description": "One allergen check of one dish (decided 28 September, audit R241). Written by the server on every automatic run and by `verifyAllergens` on a manual re-check; `getAllergenVerification` reads the latest.\n",
  "required": [
   "menuItemId",
   "matches",
   "checkedAt",
   "trigger"
  ],
  "properties": {
   "menuItemId": {
    "type": "string",
    "format": "uuid"
   },
   "matches": {
    "type": "boolean"
   },
   "declared": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "actual": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "undeclared": {
    "type": "array",
    "description": "**Present in the dish and absent from the label.** The dangerous direction, and the response leads with it.\n",
    "items": {
     "type": "object",
     "properties": {
      "allergen": {
       "type": "string"
      },
      "via": {
       "type": "string",
       "enum": [
        "ingredient",
        "substitution",
        "modifier",
        "sharedEquipment"
       ]
      },
      "sourceRef": {
       "type": "string"
      }
     }
    }
   },
   "overDeclared": {
    "type": "array",
    "description": "Labelled and no longer present. **Safe, and still worth fixing** — a menu that over-declares teaches guests the labels are guesses.\n",
    "items": {
     "type": "string"
    }
   },
   "checkedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "trigger": {
    "type": "string",
    "readOnly": true,
    "description": "What ran the check. `manual` is the Verify button; the others are the automatic run after that change (audit R241).",
    "enum": [
     "manual",
     "recipeChanged",
     "substitutionChanged",
     "modifierChanged"
    ]
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
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
 "CreateMenuRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "code",
   "name",
   "outletId"
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
   "outletId": {
    "type": "string",
    "format": "uuid"
   },
   "availability": {
    "$ref": "#/components/schemas/MenuAvailability"
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
    "format": "uuid",
    "nullable": true,
    "description": "**Taken from their `fnb.order`, 20 September.** We carried outlet, table visit and kitchen ticket on an F&B order and nothing joining it to what was actually sold, so an F&B line could not be reconciled to the order that paid for it.\n"
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
 "KpiValue": {
  "type": "object",
  "description": "BI board 10.3. **Value, target, variance, direction and freshness in one read.**",
  "properties": {
   "kpiId": {
    "type": "string",
    "format": "uuid"
   },
   "code": {
    "type": "string"
   },
   "name": {
    "type": "string"
   },
   "scopePath": {
    "type": "string"
   },
   "period": {
    "type": "string"
   },
   "value": {
    "$ref": "#/components/schemas/MetricValue"
   },
   "target": {
    "allOf": [
     {
      "$ref": "#/components/schemas/MetricValue"
     }
    ],
    "nullable": true
   },
   "comparison": {
    "allOf": [
     {
      "$ref": "#/components/schemas/MetricValue"
     }
    ],
    "nullable": true
   },
   "variancePercent": {
    "type": "number",
    "nullable": true
   },
   "direction": {
    "type": "string",
    "enum": [
     "up",
     "down",
     "flat"
    ]
   },
   "status": {
    "type": "string",
    "enum": [
     "green",
     "amber",
     "red",
     "noTarget"
    ]
   },
   "asOf": {
    "type": "string",
    "format": "date-time"
   },
   "stale": {
    "type": "boolean",
    "description": "**True when the pipeline behind it has not refreshed.** A number nobody flagged as stale is a number somebody will act on.\n"
   }
  }
 },
 "Menu": {
  "x-ticvai-persistence": "fnb.menu",
  "type": "object",
  "required": [
   "id",
   "code",
   "name",
   "outletId",
   "isActive"
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
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "outletId": {
    "type": "string",
    "format": "uuid"
   },
   "availability": {
    "$ref": "#/components/schemas/MenuAvailability"
   },
   "sections": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/MenuSection"
    }
   },
   "isActive": {
    "type": "boolean"
   },
   "publishedVersion": {
    "type": "integer",
    "nullable": true,
    "readOnly": true,
    "description": "The `MenuVersion.version` live now. Null for a menu never published."
   },
   "publishedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   }
  }
 },
 "MenuActionResult": {
  "type": "object",
  "x-ticvai-persistence": "none — response shape",
  "description": "**The preview, or what was applied** (`applyMenuActions`). The same shape either way, so the screen that showed the preview shows the result.\n",
  "required": [
   "applied",
   "actions"
  ],
  "properties": {
   "applied": {
    "type": "boolean",
    "description": "False for a preview (`previewOnly`), true once applied."
   },
   "actions": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "index",
      "kind",
      "affectedItemCount"
     ],
     "properties": {
      "index": {
       "type": "integer",
       "description": "The action's position in the request."
      },
      "kind": {
       "type": "string",
       "enum": [
        "reprice",
        "retire",
        "activate",
        "moveSection",
        "setAvailability",
        "setTax"
       ]
      },
      "affectedItemCount": {
       "type": "integer",
       "description": "**How many items it touches** — the number the preview exists to show."
      },
      "affectedMenuItemIds": {
       "type": "array",
       "items": {
        "type": "string",
        "format": "uuid"
       }
      }
     }
    }
   },
   "appliedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "MenuAvailability": {
  "x-ticvai-persistence": "none — embedded in menu",
  "type": "object",
  "description": "When this menu is in force. Absent means always. Days, times and dates are all read in the Region's time zone, not UTC.",
  "properties": {
   "daysOfWeek": {
    "type": "array",
    "items": {
     "type": "integer",
     "minimum": 0,
     "maximum": 6
    }
   },
   "startTime": {
    "type": "string",
    "pattern": "^([01]\\d|2[0-3]):[0-5]\\d$",
    "description": "Wall-clock time, in the Region's time zone."
   },
   "endTime": {
    "type": "string",
    "pattern": "^([01]\\d|2[0-3]):[0-5]\\d$",
    "description": "Wall-clock time, in the Region's time zone."
   },
   "validFrom": {
    "type": "string",
    "format": "date",
    "nullable": true,
    "description": "Calendar day, in the Region's time zone, not UTC."
   },
   "validTo": {
    "type": "string",
    "format": "date",
    "nullable": true,
    "description": "Calendar day, in the Region's time zone, not UTC."
   }
  }
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
 "MenuSchedule": {
  "type": "object",
  "x-ticvai-persistence": "fnb.menu_schedule",
  "description": "**A publish dated for later** (`scheduleMenuPublish`, or `publishMenu` with an `effectiveAt`). Listed by `listMenuSchedules` while `pending`, so a venue with three scheduled price changes can see them; one per menu per date.\n",
  "required": [
   "id",
   "menuId",
   "effectiveAt",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "menuId": {
    "type": "string",
    "format": "uuid"
   },
   "effectiveAt": {
    "type": "string",
    "format": "date-time"
   },
   "status": {
    "type": "string",
    "enum": [
     "pending",
     "applied",
     "cancelled"
    ]
   },
   "publishedVersion": {
    "type": "integer",
    "nullable": true,
    "readOnly": true,
    "description": "The `MenuVersion.version` that went live when the schedule fired. Null until then."
   },
   "createdAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "createdByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "cancelledAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Operations write it at `venue` scope."
   }
  }
 },
 "MenuSection": {
  "x-ticvai-persistence": "fnb.menu_section",
  "type": "object",
  "required": [
   "code",
   "name",
   "sortOrder"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "code": {
    "type": "string"
   },
   "name": {
    "type": "string"
   },
   "sortOrder": {
    "type": "integer"
   },
   "items": {
    "type": "array",
    "description": "The section's items, in sale-board order. An item's membership is `MenuItem.menuSectionId`.",
    "items": {
     "$ref": "#/components/schemas/MenuItem"
    }
   }
  }
 },
 "MenuVersion": {
  "type": "object",
  "x-ticvai-persistence": "fnb.menu_version",
  "description": "**One published state of a menu, kept.** `publishMenu` writes one, `rollbackMenu` writes a new one from an older one, and `listMenuVersions` reads them — the previous version stays readable, which is what makes rollback and *what were we charging at noon* possible. **A version is never edited**; a menu history that can be edited cannot answer a refund dispute.\nStatuses follow flow F31: a new version is `draft` while the live one keeps selling, `scheduled` once dated, `live`, and `superseded` when a later version goes live.\n",
  "required": [
   "id",
   "menuId",
   "version",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "menuId": {
    "type": "string",
    "format": "uuid"
   },
   "version": {
    "type": "integer",
    "minimum": 1
   },
   "status": {
    "type": "string",
    "enum": [
     "draft",
     "scheduled",
     "live",
     "superseded"
    ]
   },
   "effectiveAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "publishedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "publishedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "restoredFromVersion": {
    "type": "integer",
    "nullable": true,
    "description": "Set on a version written by `rollbackMenu` — the version it restored."
   },
   "channels": {
    "type": "array",
    "items": {
     "$ref": "../shared/common.yaml#/components/schemas/SalesChannel"
    }
   },
   "note": {
    "type": "string",
    "nullable": true
   },
   "availability": {
    "$ref": "#/components/schemas/MenuAvailability"
   },
   "sections": {
    "type": "array",
    "description": "The sections and items as published. The snapshot, not a reference to the live rows.",
    "items": {
     "$ref": "#/components/schemas/MenuSection"
    }
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Operations write it at `venue` scope."
   }
  }
 },
 "MetricValue": {
  "x-ticvai-persistence-column": "numeric(18,4)",
  "description": "**A reading of a metric or KPI, or a threshold on one.** A `Money` where the metric is money-valued — `MetricSource` lists those in `x-ticvai-money-valued`, and a KPI is when its `unit` is `currency` — and a plain number otherwise. naming-and-style 5.1: money is never a float, at any layer.\nStored as `numeric(18,4)` either way: a money value stores its amount, and currency and scale resolve from the scope as they do for every `Money`.\n",
  "oneOf": [
   {
    "type": "number"
   },
   {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   }
  ]
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
 "OpeningHoursWindow": {
  "type": "object",
  "description": "26 September, pull audit R088. **One weekly window an outlet is open.** `Outlet.openingHours` was an array of untyped objects. The shape is the one `supportHours.windows` already uses — a day and a from/to — with the times as local `HH:MM` in the region's time zone. Several windows on one day are a split shift, such as lunch and dinner.\n",
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
    "description": "Local time, 24-hour `HH:MM`, when the outlet opens."
   },
   "to": {
    "type": "string",
    "pattern": "^([01][0-9]|2[0-3]):[0-5][0-9]$",
    "description": "Local time, 24-hour `HH:MM`, when the outlet closes."
   }
  }
 },
 "Outlet": {
  "type": "object",
  "x-ticvai-persistence": "platform.outlet",
  "required": [
   "id",
   "code",
   "name",
   "venueId",
   "kind"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
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
   "kind": {
    "$ref": "#/components/schemas/OutletKind"
   },
   "zone": {
    "type": "string",
    "nullable": true
   },
   "stockLocationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Where this outlet draws stock from. A shop and its stockroom are one location; a bar drawing from a central cellar is not.\n"
   },
   "costCenterId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Revenue and cost attribution. Outlet is the natural grain for both."
   },
   "openingHours": {
    "type": "array",
    "description": "The weekly pattern, one entry per window. Several windows on a day are allowed.",
    "items": {
     "$ref": "#/components/schemas/OpeningHoursWindow"
    }
   },
   "isActive": {
    "type": "boolean"
   }
  }
 },
 "OutletKind": {
  "type": "string",
  "enum": [
   "shop",
   "restaurant",
   "bar",
   "cafe",
   "kiosk",
   "gameFloor",
   "ticketOffice",
   "mobile"
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
 "ProductionPlan": {
  "type": "object",
  "x-ticvai-persistence": "fnb.production_plan + fnb.production_plan_line",
  "description": "Board 2M. **Forecast demand against recipes, producing a prep list.** Built from `requestSuggestion(kind=prepPlan)` and then edited — **a forecast a chef cannot overrule is a forecast a chef ignores.**\n**A plan is not a production run and the separation is deliberate.** A plan is drafted, argued over and edited; releasing it creates the runs. **A plan that creates runs as it is drafted creates runs nobody asked for.**\n",
  "required": [
   "id",
   "forDate",
   "status",
   "lines"
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
   "forDate": {
    "type": "string",
    "format": "date",
    "description": "The trading day this prep list is for, in the Region's time zone."
   },
   "status": {
    "type": "string",
    "enum": [
     "draft",
     "released",
     "superseded",
     "cancelled"
    ]
   },
   "basedOnSuggestionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**The forecast it started from.** Kept so plan-against-forecast can be compared later — which is the label `recordSuggestionOutcome` needs.\n"
   },
   "lines": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "itemId",
      "plannedQuantity"
     ],
     "properties": {
      "itemId": {
       "type": "string",
       "format": "uuid"
      },
      "suggestedQuantity": {
       "type": "number",
       "nullable": true
      },
      "plannedQuantity": {
       "type": "number"
      },
      "uom": {
       "type": "string"
      },
      "stationId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      }
     }
    }
   },
   "releasedRunIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "readOnly": true
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
