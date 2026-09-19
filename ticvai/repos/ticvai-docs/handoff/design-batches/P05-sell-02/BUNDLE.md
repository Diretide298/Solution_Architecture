# P05-sell-02 — P05 · Sell (2 of 2)

**6 screens · 10 operations · 21 schemas · 3 permissions**

Platform P05 Guest Kiosk · ships as **guest** ·
guest audience · kiosk ·
online only

## Who this is for

**guest on kiosk.** Everything below is how you know what is
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

- **Every control that can be refused must be gated.** 3 permissions apply here:
  `ORDER_CREATE, ORDER_VIEW, PRODUCT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **2 of these operations work offline**: getOrder, listMerchandise
  — and the rest do not. A surface that looks the same online and off is lying.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `KSK-011` | Collect a booking | statusTracker | 2 | 0 | — |
| `KSK-012` | Booking found | configEditor | 1 | 0 | — |
| `KSK-013` | Call staff | configEditor | 1 | 0 | — |
| `KSK-014` | Out of service | listDetail | 0 | 0 | — |
| `KSK-016` | Order Food | statusTracker | 2 | 0 | — |
| `KSK-017` | Shop | listDetail | 4 | 0 | — |

## Thin screens in this batch

**KSK-012, KSK-013, KSK-014 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "KSK-011",
  "name": "Collect a booking",
  "module": "Sell",
  "requiresModule": "retail",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "guest-app",
   "route": "/sell/collect-a-booking",
   "component": "apps/guest-app/src/routes/sell/CollectABookingDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "KSK-001",
    "KSK-002",
    "KSK-003"
   ],
   "inferred": false,
   "entryFrom": [
    "KSK-003"
   ],
   "notes": "**Reached from KSK-003** — collecting is an alternative to buying, offered at the start. Stated on 4 September: this screen exited somewhere and nothing exited to it, so it was outside the navigation graph entirely."
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.",
  "density": "touchLarge",
  "boardFrames": [
   "Kiosk Board 2.dc.html#KSK-011"
  ],
  "pattern": "statusTracker",
  "patternReason": "`getOrder` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "Turn a reference into media.",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected collect booking",
       "bindsTo": "Order",
       "columns": [
        "Order.id",
        "Order.orderNumber",
        "Order.channel",
        "Order.venueId",
        "Order.scopePath",
        "Order.status",
        "Order.currency",
        "Order.currencyScale",
        "Order.grossAmount",
        "Order.taxAmount",
        "Order.netAmount",
        "Order.refundedAmount",
        "Order.totalPriceVariance",
        "Order.lines",
        "Order.payments",
        "Order.principalId"
       ],
       "operation": "getOrder",
       "provenance": "contract orders.yaml GET /orders/{orderId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Lookup",
       "operation": "lookupShopAndDrop",
       "provenance": "contract retail.yaml GET /shop-and-drop/lookup"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "detailPanel",
       "notes": "Structure from the wireframe board. Components not yet enumerated.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "searchField",
       "derived": true,
       "impliedBy": "lookupShopAndDrop",
       "label": "Search",
       "notes": "A search that returns nothing must say so differently from a search not yet run.",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The collect booking list.",
   "error": "Could not load. Names which read failed and leaves the collect booking untouched.",
   "emptyFirstRun": "No collect booking yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the collect booking are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "Not available"
  },
  "apis": [
   {
    "operationId": "lookupShopAndDrop",
    "contract": "retail",
    "purpose": "Find a guest's dropped goods",
    "trigger": "onLoad"
   },
   {
    "operationId": "getOrder",
    "contract": "orders",
    "purpose": "Read an order",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "orderId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A guest opening an order link weeks later.** Shows the order if it still resolves; if it was refunded or the performance passed, says which and offers the order list rather than an error."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P05 Guest Kiosk.dc.html#ksk-011",
   "note": "**Drawn by Claude Design on `Kiosk Board 2.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P05",
   "audience": "guest",
   "formFactor": "kiosk",
   "shortName": "Guest Kiosk",
   "name": "Guest Kiosk — Self-Service",
   "app": "guest-app",
   "offlineCapable": false,
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "kiosk",
    "siblings": [
     "P01",
     "P02"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "KSK-012",
  "name": "Booking found",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "guest-app",
   "route": "/sell/booking-found",
   "component": "apps/guest-app/src/routes/sell/BookingFoundDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "KSK-001",
    "KSK-002",
    "KSK-003"
   ],
   "inferred": false,
   "entryFrom": [
    "KSK-011"
   ],
   "notes": "**Reached from KSK-011** — a booking is found by the search that looked for it. Stated on 4 September: this screen exited somewhere and nothing exited to it, so it was outside the navigation graph entirely."
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.",
  "density": "touchLarge",
  "boardFrames": [
   "Kiosk Board 2.dc.html#KSK-012"
  ],
  "pattern": "configEditor",
  "patternReason": "the screen declares only writes (`transferOrderTickets`) and no read of a population — it is settings, not a list",
  "purpose": "Confirm it is the right booking, then print.",
  "gaps": [
   {
    "operation": "transferOrderTickets",
    "why": "**`transferOrderTickets` declares no request body shape**, so nothing says what this editor edits. The fields cannot be derived and the screen needs the contract before it needs a designer.",
    "source": "contract orders.yaml POST /orders/{orderId}/transfer"
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
       "label": "Transfer",
       "operation": "transferOrderTickets",
       "provenance": "contract orders.yaml POST /orders/{orderId}/transfer"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "detailPanel",
       "notes": "Structure from the wireframe board. Components not yet enumerated.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "transferOrderTickets",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Booking detail",
   "error": "Not found. Offers KSK-013",
   "emptyFirstRun": "No booking for that reference",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "Not available"
  },
  "apis": [
   {
    "operationId": "transferOrderTickets",
    "contract": "orders",
    "purpose": "Transfer tickets to another guest",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "orderId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A guest opening an order link weeks later.** Shows the order if it still resolves; if it was refunded or the performance passed, says which and offers the order list rather than an error."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P05 Guest Kiosk.dc.html#ksk-012",
   "note": "**Drawn by Claude Design on `Kiosk Board 2.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 1 operation this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P05",
   "audience": "guest",
   "formFactor": "kiosk",
   "shortName": "Guest Kiosk",
   "name": "Guest Kiosk — Self-Service",
   "app": "guest-app",
   "offlineCapable": false,
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "kiosk",
    "siblings": [
     "P01",
     "P02"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "KSK-013",
  "name": "Call staff",
  "module": "Sell",
  "requiresModule": "marketing",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "guest-app",
   "route": "/sell/call-staff",
   "component": "apps/guest-app/src/routes/sell/CallStaffDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "KSK-001",
    "KSK-002",
    "KSK-003"
   ],
   "inferred": true,
   "entryFrom": [
    "KSK-009"
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Device audience on a guest surface.** `endKioskAssist` is called by the kiosk, not by the guest — **the guest presses a button and the device raises the call**, which is why the operation authenticates as a device and authorises nothing. A guest cannot end an assist session they did not start.",
  "density": "touchLarge",
  "audience": "device",
  "boardFrames": [
   "Kiosk Board 2.dc.html#KSK-013"
  ],
  "pattern": "configEditor",
  "patternReason": "the screen declares only writes (`endKioskAssist`) and no read of a population — it is settings, not a list",
  "purpose": "Get a human, without leaving the kiosk.",
  "gaps": [
   {
    "operation": "endKioskAssist",
    "why": "**`endKioskAssist` declares no request body shape**, so nothing says what this editor edits. The fields cannot be derived and the screen needs the contract before it needs a designer.",
    "source": "contract marketing-crm.yaml POST /kiosk-assists/{sessionId}/end"
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
       "label": "End",
       "operation": "endKioskAssist",
       "provenance": "contract marketing-crm.yaml POST /kiosk-assists/{sessionId}/end"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "detailPanel",
       "notes": "Structure from the wireframe board. Components not yet enumerated.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "endKioskAssist",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Alerting staff",
   "error": "**Cannot reach staff.** Shows the counter location and opening hours instead of a spinner",
   "emptyFirstRun": "Not applicable",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "Shows the counter location"
  },
  "apis": [
   {
    "operationId": "endKioskAssist",
    "contract": "marketing-crm",
    "purpose": "Stop assisting",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "sessionId",
     "from": "session"
    }
   ],
   "coldEntry": "Resolves from the session; a cold arrival is the ordinary case."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P05 Guest Kiosk.dc.html#ksk-013",
   "note": "**Drawn by Claude Design on `Kiosk Board 2.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 1 operation this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P05",
   "audience": "guest",
   "formFactor": "kiosk",
   "shortName": "Guest Kiosk",
   "name": "Guest Kiosk — Self-Service",
   "app": "guest-app",
   "offlineCapable": false,
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "kiosk",
    "siblings": [
     "P01",
     "P02"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "KSK-014",
  "name": "Out of service",
  "module": "Sell",
  "requiresModule": "core",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "guest-app",
   "route": "/sell/out-of-service",
   "component": "apps/guest-app/src/routes/sell/OutOfServiceDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "KSK-001",
    "KSK-002",
    "KSK-003"
   ],
   "inferred": false,
   "entryFrom": [
    "KSK-001"
   ],
   "notes": "**Reached from KSK-001** — the attract loop is what an out-of-service kiosk replaces. Stated on 4 September: this screen exited somewhere and nothing exited to it, so it was outside the navigation graph entirely."
  },
  "notes": "Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.",
  "density": "touchLarge",
  "boardFrames": [
   "Kiosk Board 2.dc.html#KSK-014"
  ],
  "pattern": "listDetail",
  "patternReason": "**the screen's operations choose no pattern** — no list, no get, no write that groups. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Fail in a way that does not strand anybody.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen declares no operation the contracts recognise.** Nothing fills it, nothing it does is committed anywhere, and its shape below is a default rather than a reading.",
    "source": "the screen's own declarations"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "detailPanel",
       "notes": "Structure from the wireframe board. Components not yet enumerated.",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Not applicable",
   "error": "This is the error state",
   "emptyFirstRun": "Not applicable",
   "emptyNoResults": "The filter narrowed it and the out service are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "This is the offline state. It does not attempt a cached sale"
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P05 Guest Kiosk.dc.html#ksk-014",
   "note": "**Drawn by Claude Design on `Kiosk Board 2.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 0 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P05",
   "audience": "guest",
   "formFactor": "kiosk",
   "shortName": "Guest Kiosk",
   "name": "Guest Kiosk — Self-Service",
   "app": "guest-app",
   "offlineCapable": false,
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "kiosk",
    "siblings": [
     "P01",
     "P02"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "KSK-016",
  "name": "Order Food",
  "module": "Sell",
  "requiresModule": "fnb",
  "wave": 2,
  "implementation": {
   "app": "guest-app",
   "route": "/sell/order-food",
   "component": "apps/guest-app/src/routes/sell/OrderFoodList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "KSK-003"
   ],
   "exitTo": [
    "KSK-017"
   ],
   "transitions": [
    {
     "to": "KSK-017",
     "trigger": "Shop",
     "carries": [
      "cartId",
      "outletId"
     ],
     "provenance": "derived — KSK-017 declares entryState.params cartId, outletId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "BL-066. **Every operation existed and no screen called them** — `getGuestMenu` and `createGuestFnbOrder` are contracted and guest-callable, and P05 had fifteen screens selling neither food nor merchandise.",
  "density": "touchLarge",
  "boardFrames": [
   "Kiosk Board 2.dc.html#KSK-016"
  ],
  "pattern": "statusTracker",
  "patternReason": "`getGuestMenu` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "Order food from the kiosk and collect it.",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected order food",
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
       "bindsTo": "Menu",
       "notes": "Photographs, because **a guest at a kiosk with a queue behind them is not reading descriptions**",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "banner",
       "notes": "Allergens shown on the card, not behind a tap. **contains and mayContain are different claims** and a fryer shared with breaded fish makes chips a fish risk",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Add to order",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The menu, with the first category open",
   "error": "Could not load the menu. **The kiosk still sells tickets** — one outlet being unreachable does not close the kiosk.",
   "emptyFirstRun": "Nothing is being served right now. **The state names the next service time** — a guest at a kiosk at 4pm needs to know whether to wait twenty minutes or go elsewhere.",
   "emptyNoResults": "Nothing matches that filter. **Allergen filters narrow hard** — a guest filtering for nut-free at a nut-heavy outlet should be told that plainly rather than shown a blank menu.",
   "emptyNoAccess": "Not applicable — a kiosk menu is public."
  },
  "apis": [
   {
    "operationId": "getGuestMenu",
    "contract": "fnb",
    "purpose": "The menu for this outlet",
    "trigger": "onLoad"
   },
   {
    "operationId": "createGuestFnbOrder",
    "contract": "fnb",
    "purpose": "Place the order",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "outletId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A guest arriving cold on a link that no longer resolves is shown what happened and one way onward — never a 404.** A shared ticket, a forwarded confirmation and a push notification opened three weeks late all land here, and the person holding the link did nothing wrong. **The screen names the thing, says it is expired, cancelled or withdrawn, and offers the list it came from.** Arrives with `outletId`."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P05 Guest Kiosk.dc.html#ksk-016",
   "note": "**Drawn by Claude Design on `Kiosk Board 2.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P05",
   "audience": "guest",
   "formFactor": "kiosk",
   "shortName": "Guest Kiosk",
   "name": "Guest Kiosk — Self-Service",
   "app": "guest-app",
   "offlineCapable": false,
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "kiosk",
    "siblings": [
     "P01",
     "P02"
    ],
    "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "KSK-017",
  "name": "Shop",
  "module": "Sell",
  "requiresModule": "retail",
  "wave": 2,
  "implementation": {
   "app": "guest-app",
   "route": "/sell/shop",
   "component": "apps/guest-app/src/routes/sell/ShopList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "KSK-016"
   ],
   "exitTo": [
    "KSK-016"
   ],
   "inferred": false,
   "notes": "**Returns to KSK-016.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "KSK-016",
     "trigger": "Order Food",
     "carries": [
      "outletId"
     ],
     "provenance": "derived — KSK-016 declares entryState.params outletId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "BL-066, BL-019. **A guest can browse and reserve and not buy**, which is where retail stops for a guest surface — `createRetailSale` is a till operation. **Cross-surface parity, 31 August**: added addCartLine, lookupMerchandise. **A guest does not know which surface they are on** — the same named screen on web and app now calls the same guest-callable operations.",
  "density": "touchLarge",
  "boardFrames": [
   "Kiosk Board 2.dc.html#KSK-017"
  ],
  "pattern": "listDetail",
  "patternReason": "`listMerchandise` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Buy merchandise at the kiosk, or reserve it for collection.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every shop",
       "bindsTo": "MerchandiseItem",
       "columns": [
        "MerchandiseItem.id",
        "MerchandiseItem.sku",
        "MerchandiseItem.barcode",
        "MerchandiseItem.name",
        "MerchandiseItem.outletId",
        "MerchandiseItem.categoryId",
        "MerchandiseItem.variantId",
        "MerchandiseItem.inventoryItemId",
        "MerchandiseItem.price",
        "MerchandiseItem.onHand",
        "MerchandiseItem.isReturnable",
        "MerchandiseItem.returnWindowDays"
       ],
       "operation": "listMerchandise",
       "provenance": "contract retail.yaml GET /merchandise"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected shop",
       "bindsTo": "MerchandiseItem",
       "columns": [
        "MerchandiseItem.id",
        "MerchandiseItem.sku",
        "MerchandiseItem.barcode",
        "MerchandiseItem.name",
        "MerchandiseItem.outletId",
        "MerchandiseItem.categoryId",
        "MerchandiseItem.variantId",
        "MerchandiseItem.inventoryItemId",
        "MerchandiseItem.price",
        "MerchandiseItem.onHand",
        "MerchandiseItem.isReturnable",
        "MerchandiseItem.returnWindowDays",
        "MerchandiseItem.requiresSerialNumber",
        "MerchandiseItem.imageAssetRef",
        "MerchandiseItem.isActive"
       ],
       "operation": "listMerchandise",
       "provenance": "contract retail.yaml GET /merchandise"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Reserve",
       "operation": "reserveMerchandise",
       "provenance": "contract retail.yaml POST /outlets/{outletId}/reserve"
      },
      {
       "kind": "secondaryButton",
       "label": "Add",
       "operation": "addCartLine",
       "provenance": "contract orders.yaml POST /carts/{cartId}/lines"
      },
      {
       "kind": "secondaryButton",
       "label": "Lookup",
       "operation": "lookupMerchandise",
       "provenance": "contract retail.yaml GET /merchandise/lookup"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "multiSelect",
       "label": "Size",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "label": "Add",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Reserve for collection",
       "notes": "BL-019. **Reserve is not buy** — the guest pays at a till or on the app, and this screen is honest about which",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Products with stock, in-stock first",
   "error": "Could not load. Tickets and food are unaffected.",
   "emptyFirstRun": "This kiosk does not sell merchandise. **Stated rather than shown as an empty shop** — a guest looking at a blank grid assumes it is broken.",
   "emptyNoResults": "Nothing in stock in that size or category. **Reserve-for-collection is offered here**, because out of stock at this kiosk is not out of stock at the venue.",
   "emptyNoAccess": "Not applicable."
  },
  "apis": [
   {
    "operationId": "listMerchandise",
    "contract": "retail",
    "purpose": "What is available",
    "trigger": "onLoad"
   },
   {
    "operationId": "reserveMerchandise",
    "contract": "retail",
    "purpose": "Hold for collection",
    "trigger": "onAction",
    "invalidates": [
     "listMerchandise"
    ]
   },
   {
    "operationId": "addCartLine",
    "contract": "orders",
    "purpose": "Add something",
    "trigger": "onAction",
    "invalidates": [
     "listMerchandise"
    ]
   },
   {
    "operationId": "lookupMerchandise",
    "contract": "retail",
    "purpose": "Price and stock check by barcode",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "outletId",
     "from": "KSK-016"
    },
    {
     "name": "cartId",
     "from": "session"
    }
   ],
   "coldEntry": "Resolves from the session; a cold arrival is the ordinary case.",
   "preloaded": [
    "MerchandiseItem.id",
    "MerchandiseItem.sku",
    "MerchandiseItem.barcode",
    "MerchandiseItem.name",
    "MerchandiseItem.outletId"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P05 Guest Kiosk.dc.html#ksk-017",
   "note": "**Drawn by Claude Design on `Kiosk Board 2.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P05",
   "audience": "guest",
   "formFactor": "kiosk",
   "shortName": "Guest Kiosk",
   "name": "Guest Kiosk — Self-Service",
   "app": "guest-app",
   "offlineCapable": false,
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "kiosk",
    "siblings": [
     "P01",
     "P02"
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
 "endKioskAssist": {
  "method": "POST",
  "path": "/kiosk-assists/{sessionId}/end",
  "contract": "marketing-crm",
  "summary": "Stop assisting",
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
  "responds": "KioskAssistSession"
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
 "getOrder": {
  "method": "GET",
  "path": "/orders/{orderId}",
  "contract": "orders",
  "summary": "Read an order",
  "permission": "ORDER_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "Order"
 },
 "listMerchandise": {
  "method": "GET",
  "path": "/merchandise",
  "contract": "retail",
  "summary": "List merchandise",
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
    "name": "categoryId",
    "in": "query",
    "required": null
   },
   {
    "name": "inStockOnly",
    "in": "query",
    "required": null
   },
   {
    "name": "search",
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
 "lookupMerchandise": {
  "method": "GET",
  "path": "/merchandise/lookup",
  "contract": "retail",
  "summary": "Price and stock check by barcode",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "barcode",
    "in": "query",
    "required": null
   },
   {
    "name": "sku",
    "in": "query",
    "required": null
   },
   {
    "name": "includeSiblingOutlets",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "PriceCheck"
 },
 "lookupShopAndDrop": {
  "method": "GET",
  "path": "/shop-and-drop/lookup",
  "contract": "retail",
  "summary": "Find a guest's dropped goods",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "entitlementId",
    "in": "query",
    "required": null
   },
   {
    "name": "dropReference",
    "in": "query",
    "required": null
   },
   {
    "name": "receiptNumber",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "ShopAndDrop"
 },
 "reserveMerchandise": {
  "method": "POST",
  "path": "/outlets/{outletId}/reserve",
  "contract": "retail",
  "summary": "Reserve an item for collection",
  "permission": "ORDER_CREATE",
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
  "responds": "MerchandiseReservation"
 },
 "transferOrderTickets": {
  "method": "POST",
  "path": "/orders/{orderId}/transfer",
  "contract": "orders",
  "summary": "Transfer tickets to another guest",
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
   "seatIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "parentLineId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "For an add-on attaching to a ticket already in the cart. **Removing the parent removes the child** — a locker with no admission is not a sale.\n"
   },
   "attributes": {
    "type": "object",
    "additionalProperties": true
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
   "subtotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "discountTotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "taxTotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "total": {
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
     "requiresPrerequisite"
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
    "description": "Most are not. `requiresPrerequisite` is — an add-on with no ticket to attach to cannot be sold.\n"
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
   "seatIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
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
    "format": "uuid",
    "nullable": true,
    "description": "The capacity held for this line. **Null for a product with no capacity** — a t-shirt needs stock, not a lease.\n"
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
 "KioskAssistSession": {
  "type": "object",
  "x-ticvai-persistence": "marketing.kiosk_assist_session",
  "description": "2.1.25. A staff member acting on a kiosk session remotely. **The guest can always see it and always end it** — remote assistance a guest cannot see or stop is surveillance.\n",
  "required": [
   "id",
   "deviceId",
   "staffPrincipalId",
   "startedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "deviceId": {
    "type": "string",
    "format": "uuid"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "staffPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "staffDisplayName": {
    "type": "string",
    "description": "**Shown on the kiosk.** A guest being helped should know by whom.\n"
   },
   "cartId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "reason": {
    "type": "string",
    "enum": [
     "guestCalled",
     "healthAlert",
     "stuckSession",
     "paymentIssue",
     "proactive"
    ]
   },
   "endedBy": {
    "type": "string",
    "nullable": true,
    "enum": [
     "staff",
     "guest",
     "timeout"
    ]
   },
   "actionsTaken": {
    "type": "array",
    "description": "**Every action recorded as the staff member's**, not the kiosk's. A cashier completing a guest's checkout remotely is a staff action on a guest cart.\n",
    "items": {
     "type": "object",
     "properties": {
      "operationId": {
       "type": "string"
      },
      "at": {
       "type": "string",
       "format": "date-time"
      }
     }
    }
   },
   "startedAt": {
    "type": "string",
    "format": "date-time"
   },
   "endedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "MerchandiseReservation": {
  "x-ticvai-persistence": "retail.reservation + retail.reservation_line",
  "type": "object",
  "required": [
   "id",
   "outletId",
   "lines",
   "status",
   "expiresAt"
  ],
  "properties": {
   "id": {
    "type": "string"
   },
   "reservationNumber": {
    "type": "string"
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
   "lines": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "merchandiseId": {
       "type": "string",
       "format": "uuid"
      },
      "name": {
       "type": "string"
      },
      "quantity": {
       "type": "integer"
      }
     }
    }
   },
   "status": {
    "type": "string",
    "enum": [
     "reserved",
     "collected",
     "expired",
     "cancelled"
    ]
   },
   "collectionNote": {
    "type": "string",
    "nullable": true
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time"
   },
   "collectedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
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
    "type": "string"
   },
   "orderNumber": {
    "type": "string"
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
    "nullable": true
   },
   "subjectId": {
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
  "x-ticvai-persistence": "orders.order_line",
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
      "items": {
       "type": "string"
      }
     },
     "crossRegionRightIds": {
      "type": "array",
      "items": {
       "type": "string"
      },
      "description": "Redemption rights propagated to other cells for this line."
     }
    }
   }
  ]
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
 "PriceCheck": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "merchandiseId",
   "name",
   "listPrice",
   "effectivePrice",
   "onHand"
  ],
  "properties": {
   "merchandiseId": {
    "type": "string",
    "format": "uuid"
   },
   "sku": {
    "type": "string"
   },
   "name": {
    "type": "string"
   },
   "listPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "effectivePrice": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "After any live promotion."
   },
   "appliedPromotionCode": {
    "type": "string",
    "nullable": true
   },
   "onHand": {
    "type": "number"
   },
   "isAvailable": {
    "type": "boolean"
   },
   "siblingOutlets": {
    "type": "array",
    "description": "Stock elsewhere in the venue, so a colleague can be sent.",
    "items": {
     "type": "object",
     "properties": {
      "outletId": {
       "type": "string",
       "format": "uuid"
      },
      "outletName": {
       "type": "string"
      },
      "onHand": {
       "type": "number"
      }
     }
    }
   }
  }
 },
 "ShopAndDrop": {
  "type": "object",
  "x-ticvai-persistence": "retail.shop_and_drop + retail.shop_and_drop_line",
  "required": [
   "id",
   "dropReference",
   "saleId",
   "collectionPointId",
   "status",
   "collectBy"
  ],
  "properties": {
   "id": {
    "type": "string"
   },
   "dropReference": {
    "type": "string",
    "description": "Short and readable. Printed on the slip a guest may or may not keep."
   },
   "saleId": {
    "type": "string"
   },
   "entitlementId": {
    "type": "string",
    "nullable": true,
    "description": "The ticket that claims these goods. The point of 4.4.7 — a guest does not have to keep a receipt safe for eight hours in a water park.\n"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "collectionPointId": {
    "type": "string",
    "format": "uuid"
   },
   "collectionPointName": {
    "type": "string"
   },
   "status": {
    "type": "string",
    "enum": [
     "awaitingCollection",
     "partiallyCollected",
     "collected",
     "uncollected",
     "disposed"
    ]
   },
   "lines": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "lineId": {
       "type": "string"
      },
      "merchandiseId": {
       "type": "string",
       "format": "uuid"
      },
      "name": {
       "type": "string"
      },
      "quantity": {
       "type": "integer"
      },
      "collectedQuantity": {
       "type": "integer"
      }
     }
    }
   },
   "droppedAt": {
    "type": "string",
    "format": "date-time"
   },
   "collectBy": {
    "type": "string",
    "format": "date-time"
   },
   "collectedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "collectedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "verifiedBy": {
    "type": "string",
    "nullable": true
   }
  }
 }
}
```
