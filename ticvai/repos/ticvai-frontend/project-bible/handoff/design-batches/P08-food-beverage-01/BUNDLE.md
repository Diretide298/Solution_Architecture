# P08-food-beverage-01 — P08 · Food & Beverage

**8 screens · 29 operations · 17 schemas · 7 permissions**

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

- **Every control that can be refused must be gated.** 7 permissions apply here:
  `ORDER_CREATE, ORDER_MODIFY, ORDER_VIEW, PRODUCT_CONFIGURE, PRODUCT_VIEW, SCOPE_VIEW, TENANT_CONFIGURE`. A control nobody can use must say so,
  not sit enabled and fail.
- **10 of these operations work offline**: acceptFnbOrder, cancelFnbOrder, createFnbOrder, getFnbOrder, getVenueSettings, listKitchenStations, listKitchenTickets, listProductionRuns
  — and the rest do not. A surface that looks the same online and off is lying.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-020` | F&B Order Management | listDetail | 11 | 1 | — |
| `BO-021` | Order Search | statusTracker | 2 | 0 | — |
| `BO-045` | Menu Management | listDetail | 10 | 0 | — |
| `BO-046` | Kitchen Display | listDetail | 5 | 0 | — |
| `BO-104` | Food & Beverage | listDetail | 3 | 0 | — |
| `BO-134` | Kitchen & Preparation Stations | listDetail | 2 | 0 | — |
| `BO-135` | Order Routing & KDS/Printer Rules | listDetail | 2 | 0 | — |
| `BO-136` | F&B Global Settings & Controls | listDetail | 5 | 0 | — |

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
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-104 declares entryState.params venueId, so an edge into it must carry them"
    },
    {
     "to": "GST-025",
     "trigger": "Tracks the order",
     "provenance": "flow F11 step 5→6",
     "crossesDevice": true,
     "back": false
    }
   ]
  },
  "notes": "Restored 20 August when the P15 build was rolled back. **Named `Timed Entry Rules` and carrying eleven F&B order operations.** Timed entry is an admission profile; this is the order desk. The client board calls it *Active Order Management & Fulfilment Journey*. **Purpose corrected 24 August.** The screen was renamed *F&B Order Management* and its purpose still read *\"Control how early and how late a ticket admits\"* — **timed entry, on a screen whose every operation is `fnb`.** A rename that moves the label and leaves the sentence is worse than no rename: the name is what a reader scans and the purpose is what they trust.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listFnbOrders` reads the population and `getFnbOrder` reads one of them — list, select, act",
  "purpose": "Take, amend and route an F&B order from the back office — and see what the kitchen is working on.",
  "gaps": [
   {
    "operation": "listKitchenStations",
    "why": "**2 declared operations reach no component on this screen**: listKitchenStations, listKitchenTickets. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every order",
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
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected order",
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
       "label": "Accept",
       "operation": "acceptFnbOrder",
       "provenance": "contract fnb.yaml POST /fnb-orders/{orderId}/accept"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "setKitchenTicketStatus",
       "provenance": "contract fnb.yaml PUT /kitchen/tickets/{ticketId}/status"
      },
      {
       "kind": "secondaryButton",
       "label": "Amend",
       "operation": "amendFnbOrder",
       "provenance": "contract fnb.yaml PATCH /fnb-orders/{orderId}"
      },
      {
       "kind": "destructiveButton",
       "label": "Cancel",
       "operation": "cancelFnbOrder",
       "provenance": "contract fnb.yaml POST /fnb-orders/{orderId}/cancel"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createFnbOrder",
       "provenance": "contract fnb.yaml POST /fnb-orders"
      },
      {
       "kind": "secondaryButton",
       "label": "Prioritise",
       "operation": "prioritiseKitchenTicket",
       "provenance": "contract fnb.yaml POST /kitchen/tickets/{ticketId}/prioritise"
      },
      {
       "kind": "secondaryButton",
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
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "acceptFnbOrder",
       "label": "Accept fnb order",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "destructiveButton",
       "derived": true,
       "impliedBy": "cancelFnbOrder",
       "label": "Cancel fnb order",
       "notes": "**Always confirms, never the default focus.** The consequence goes in the body — *cancel 3 orders worth AED 480* is a confirmation, *are you sure* is not.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "detailPanel",
       "derived": true,
       "impliedBy": "getFnbOrder",
       "notes": "One record, read-only.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "acceptFnbOrder",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "confirmDialog",
       "derived": true,
       "label": "Confirm",
       "notes": "**The consequence goes in the body, not the title.** *Cancel 3 orders worth AED 480* is a confirmation; *are you sure* is not — and a dialog that cannot name what it destroys is a dialog somebody dismisses.\n\n**Added 31 August.** `confirmDialog` and `modal` were both in the component library and used **zero times across 492 screens**, while `destructiveButton` was used 39 times and its own entry reads *always requires confirmation*.",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmCancelFnbOrder",
    "component": "confirmDialog",
    "trigger": "Cancel",
    "body": "**Names what `cancelFnbOrder` changes and what it leaves alone**, in the consequence rather than the verb. A order this affects should be identified in the dialog, not just counted.",
    "provenance": "contract fnb.yaml POST /fnb-orders/{orderId}/cancel"
   }
  ],
  "states": {
   "loading": "The order list.",
   "error": "Could not load. Names which read failed and leaves the order untouched.",
   "emptyFirstRun": "No order yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the order are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
    "trigger": "onLoad"
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
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-104 declares entryState.params venueId, so an edge into it must carry them"
    },
    {
     "to": "POS-002",
     "trigger": "Sell — Ticket Catalogue",
     "provenance": "flow F81 step 1→2",
     "crossesDevice": true,
     "back": false
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
       "label": "The selected order search",
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
       "kind": "detailPanel",
       "derived": true,
       "impliedBy": "getGuestOrderStatus",
       "notes": "One record, read-only.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "recordOrderHandover",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The order search list.",
   "error": "Could not load. Names which read failed and leaves the order search untouched.",
   "emptyFirstRun": "No order search yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the order search are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
   "source": "Claude Design Retail pack, 24 August",
   "note": "**Drawn by Claude Design on `Retail Board 3.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
     "to": "BO-111",
     "trigger": "An item's recipe changed, so its allergens are re-verified",
     "provenance": "flow F31 step 2→3",
     "operation": "applyMenuActions"
    },
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "provenance": "flow F93 step 2→3"
    },
    {
     "to": "BO-104",
     "trigger": "Food & Beverage",
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-104 declares entryState.params venueId, so an edge into it must carry them"
    },
    {
     "to": "POS-002",
     "trigger": "The till picks it up in its next catalogue bundle",
     "provenance": "flow F31 step 5→6",
     "operation": "publishMenu",
     "crossesDevice": true,
     "back": false
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
       "label": "Create",
       "operation": "createMenu",
       "provenance": "contract fnb.yaml POST /menus"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "setMenuSections",
       "provenance": "contract fnb.yaml PUT /menus/{menuId}/sections"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateMenu",
       "provenance": "contract fnb.yaml PATCH /menus/{menuId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Publish",
       "operation": "publishMenu",
       "provenance": "contract fnb.yaml POST /menus/{menuId}/publish"
      },
      {
       "kind": "secondaryButton",
       "label": "Schedule",
       "operation": "scheduleMenuPublish",
       "provenance": "contract fnb.yaml POST /menus/{menuId}/schedule"
      },
      {
       "kind": "secondaryButton",
       "label": "Rollback",
       "operation": "rollbackMenu",
       "provenance": "contract fnb.yaml POST /menus/{menuId}/rollback"
      },
      {
       "kind": "secondaryButton",
       "label": "Apply",
       "operation": "applyMenuActions",
       "provenance": "contract fnb.yaml POST /menus/{menuId}/actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Verify",
       "operation": "verifyAllergens",
       "provenance": "contract fnb.yaml POST /menu-items/{menuItemId}/verify-allergens"
      },
      {
       "kind": "publishGate",
       "label": "What publishing changes",
       "notes": "**Names what goes live, where, and from when.** A publish with no stated consequence is one somebody presses meaning to save.",
       "provenance": "authored — required by check-screens"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "detailPanel",
       "derived": true,
       "impliedBy": "getMenu",
       "notes": "One record, read-only.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createMenu",
       "label": "Create menu",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createMenu",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "publishGate",
       "impliedBy": "publishMenu",
       "notes": "Declares `publishMenu`. **The gate names what the publish will affect before it happens** — a disabled Publish with no reason is the state operators escalate.\n",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The menu list.",
   "error": "Could not load. Names which read failed and leaves the menu untouched.",
   "emptyFirstRun": "No menu yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the menu are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
    "trigger": "onLoad"
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
    "purpose": "Does this dish still match its claim?",
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
   "source": "Claude Design F&B pack, 24 August",
   "note": "**Drawn by Claude Design on `FnB Board 2.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 10 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-104 declares entryState.params venueId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Restored 20 August when the P15 build was rolled back. **Retained in P08 on 20 August when the P15 build was rolled back**, and P15 now owns the kitchen display for the venue floor. **This is the back-office view of the same tickets** — a manager watching the pass from a desk, not a screen at the pass.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listKitchenTickets` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Show the kitchen what to make, in order.",
  "gaps": [
   {
    "operation": "listKitchenStations",
    "why": "**1 declared operation reach no component on this screen**: listKitchenStations. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every kitchen display",
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
       "label": "The selected kitchen display",
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
       "label": "Prioritise",
       "operation": "prioritiseKitchenTicket",
       "provenance": "contract fnb.yaml POST /kitchen/tickets/{ticketId}/prioritise"
      },
      {
       "kind": "secondaryButton",
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
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "setKitchenTicketStatus",
       "label": "Save kitchen ticket status",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setKitchenTicketStatus",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The kitchen display list.",
   "error": "Could not load. Names which read failed and leaves the kitchen display untouched.",
   "emptyFirstRun": "No kitchen display yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the kitchen display are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
     "carries": [
      "orderId",
      "ticketId",
      "venueId"
     ],
     "provenance": "derived — BO-020 declares entryState.params orderId, ticketId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-021",
     "trigger": "Order Search",
     "carries": [
      "orderId",
      "venueId"
     ],
     "provenance": "derived — BO-021 declares entryState.params orderId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-045",
     "trigger": "Menu Management",
     "carries": [
      "menuId",
      "menuItemId",
      "venueId"
     ],
     "provenance": "derived — BO-045 declares entryState.params menuId, menuItemId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-046",
     "trigger": "Kitchen Display",
     "carries": [
      "ticketId",
      "venueId"
     ],
     "provenance": "derived — BO-046 declares entryState.params ticketId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-134",
     "trigger": "Kitchen & Preparation Stations",
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-134 declares entryState.params venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-135",
     "trigger": "Order Routing & KDS/Printer Rules",
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-135 declares entryState.params venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-136",
     "trigger": "F&B Global Settings & Controls",
     "carries": [
      "planId",
      "venueId"
     ],
     "provenance": "derived — BO-136 declares entryState.params planId, venueId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Section landing. **4 screens reach the entry point through here** — before 20 August they reached it through nothing. **Navigation repointed to P15 on 20 August** — the F&B screens it linked to moved out of the back office when the client board was adopted.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listMenus` reads the population and `getVenueSettings` reads one of them — list, select, act",
  "purpose": "Everything in food & beverage, and what in it needs attention.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every food beverage",
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
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected food beverage",
       "bindsTo": "VenueSettings",
       "columns": [
        "VenueSettings.id",
        "VenueSettings.venueId",
        "VenueSettings.supportHours",
        "VenueSettings.quietHours",
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
       "label": "Create",
       "operation": "createMenu",
       "provenance": "contract fnb.yaml POST /menus"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "cardList",
       "bindsTo": "screens",
       "notes": "4 screens, each with what needs attention.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "searchField",
       "label": "Search food & beverage",
       "provenance": "carried from the previous definition"
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
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-104 declares entryState.params venueId, so an edge into it must carry them"
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
       "kind": "dataTable",
       "label": "Every kitchen preparation stations",
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
       "label": "The selected kitchen preparation stations",
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
       "kind": "searchField",
       "label": "Search kitchen",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The kitchen preparation stations list.",
   "error": "Could not load. Names which read failed and leaves the kitchen preparation stations untouched.",
   "emptyFirstRun": "No kitchen preparation stations yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the kitchen preparation stations are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
   "note": "**Drawn by Claude Design on `FnB Board 1.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-104 declares entryState.params venueId, so an edge into it must carry them"
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
       "kind": "dataTable",
       "label": "Every order routing kds",
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
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected order routing kds",
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
       "kind": "searchField",
       "label": "Search order routing",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The order routing kds list.",
   "error": "Could not load. Names which read failed and leaves the order routing kds untouched.",
   "emptyFirstRun": "No order routing kds yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the order routing kds are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
   "note": "**Drawn by Claude Design on `FnB Board 1.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-104 declares entryState.params venueId, so an edge into it must carry them"
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
       "kind": "dataTable",
       "label": "Every global settings controls",
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
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected global settings controls",
       "bindsTo": "VenueSettings",
       "columns": [
        "VenueSettings.id",
        "VenueSettings.venueId",
        "VenueSettings.supportHours",
        "VenueSettings.quietHours",
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
       "label": "Save changes",
       "operation": "setVenueSettings",
       "provenance": "contract tenancy.yaml PUT /venues/{venueId}/settings"
      },
      {
       "kind": "secondaryButton",
       "label": "Build",
       "operation": "buildProductionPlan",
       "provenance": "contract fnb.yaml POST /production-plans"
      },
      {
       "kind": "secondaryButton",
       "label": "Release",
       "operation": "releaseProductionPlan",
       "provenance": "contract fnb.yaml POST /production-plans/{planId}/release"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
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
    }
   ]
  },
  "states": {
   "loading": "The global settings controls list.",
   "error": "Could not load. Names which read failed and leaves the global settings controls untouched.",
   "emptyFirstRun": "No global settings controls yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the global settings controls are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
   "source": "Claude Design F&B pack, 24 August",
   "note": "**Drawn by Claude Design on `FnB Board 2.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 5 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "responds": null
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
  "permission": "TENANT_CONFIGURE",
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
  "responds": "ProductionRun"
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
  "responds": null
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
  "responds": null
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
  "responds": null
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
   }
  }
 },
 "MenuAvailability": {
  "x-ticvai-persistence": "none — embedded in menu",
  "type": "object",
  "description": "When this menu is in force. Absent means always.",
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
    "pattern": "^([01]\\d|2[0-3]):[0-5]\\d$"
   },
   "endTime": {
    "type": "string",
    "pattern": "^([01]\\d|2[0-3]):[0-5]\\d$"
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
    "items": {
     "$ref": "#/components/schemas/MenuItem"
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
 "ProductionPlan": {
  "type": "object",
  "x-ticvai-persistence": "fnb.production_plan",
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
    "format": "date"
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
 "ProductionRun": {
  "type": "object",
  "x-ticvai-persistence": "fnb.production_run",
  "description": "BL-129. **A central kitchen makes 400 portions at 6am for four outlets**, and nothing modelled that — orders consume stock and no operation produced any.\n**Production converts ingredients into a sellable item**, which is a stock movement in both directions at once, and treating it as two unrelated adjustments loses the yield.\n",
  "required": [
   "id",
   "recipeId",
   "plannedQuantity",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "recipeId": {
    "type": "string",
    "format": "uuid"
   },
   "producingOutletId": {
    "type": "string",
    "format": "uuid"
   },
   "forOutletIds": {
    "type": "array",
    "description": "**Where it goes.** A central kitchen produces for outlets that did not make it.\n",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "plannedQuantity": {
    "type": "number"
   },
   "actualQuantity": {
    "type": "number",
    "nullable": true,
    "description": "BL-126. **Theoretical against actual is the whole point of recording this.** A recipe says 400 portions from the ingredients issued; the run says how many were made, and the gap is waste, theft or a recipe that is wrong.\n"
   },
   "scheduledFor": {
    "type": "string",
    "format": "date-time"
   },
   "status": {
    "type": "string",
    "enum": [
     "planned",
     "inProgress",
     "completed",
     "cancelled"
    ]
   },
   "varianceReason": {
    "type": "string",
    "nullable": true
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
