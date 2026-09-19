# P01-ticketing-01 — P01 · Ticketing

**3 screens · 13 operations · 13 schemas · 7 permissions**

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

- **Every control that can be refused must be gated.** 7 permissions apply here:
  `LEDGER_VIEW, ORDER_CANCEL, ORDER_CREATE, ORDER_VIEW, PRODUCT_VIEW, RESOURCE_BOOK, RESOURCE_VIEW`. A control nobody can use must say so,
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
| `WEB-030` | Ticket Transfer | listDetail | 4 | 0 | — |
| `WEB-031` | My Reservations | listDetail | 7 | 1 | — |
| `WEB-035` | Multi-Currency & Pricing | listDetail | 2 | 0 | — |

## Thin screens in this batch

**WEB-035 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "WEB-030",
  "name": "Ticket Transfer",
  "module": "Ticketing",
  "requiresModule": "ticketing",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "guest-web",
   "route": "/ticket-transfer",
   "component": "apps/guest-web/src/routes/TicketTransfer.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "WEB-001",
    "WEB-031",
    "WEB-035"
   ],
   "inferred": true,
   "entryFrom": [
    "WEB-010"
   ],
   "transitions": [
    {
     "to": "WEB-031",
     "trigger": "My Reservations",
     "carries": [
      "reservationId"
     ],
     "provenance": "derived — WEB-031 declares entryState.params reservationId, so an edge into it must carry them"
    },
    {
     "to": "GST-014",
     "trigger": "The friend claims it in the app",
     "provenance": "flow F55 step 4→5",
     "crossesDevice": true,
     "back": false
    }
   ]
  },
  "notes": "Added 17 August for parity with GST-014. **Not on the wireframe board** — needs drawing. CF-93.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listOrders` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Send a ticket to someone else, and see what you have sent.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every ticket transfer",
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
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected ticket transfer",
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
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Transfer",
       "operation": "transferOrderTickets",
       "provenance": "contract orders.yaml POST /orders/{orderId}/transfer"
      },
      {
       "kind": "secondaryButton",
       "label": "Claim",
       "operation": "claimTicketTransfer",
       "provenance": "contract orders.yaml POST /ticket-transfers/{transferId}/claim"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
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
   "loading": "The ticket transfer list.",
   "error": "Could not load. Names which read failed and leaves the ticket transfer untouched.",
   "emptyFirstRun": "No ticket transfer yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the ticket transfer are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** Sending, claiming and listing for resale need the connection — a transfer nobody received is a ticket nobody holds. Tickets already loaded stay visible."
  },
  "apis": [
   {
    "operationId": "transferOrderTickets",
    "contract": "orders",
    "purpose": "Transfer tickets to another guest",
    "trigger": "onAction",
    "invalidates": [
     "listOrders"
    ]
   },
   {
    "operationId": "claimTicketTransfer",
    "contract": "orders",
    "purpose": "Claim transferred tickets",
    "trigger": "onAction",
    "invalidates": [
     "listOrders"
    ]
   },
   {
    "operationId": "listOrders",
    "contract": "orders",
    "purpose": "List orders",
    "trigger": "onLoad"
   },
   {
    "operationId": "createResaleListing",
    "contract": "orders",
    "purpose": "List a ticket for resale",
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
     "name": "transferId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A guest opening an order link weeks later.** Shows the order if it still resolves; if it was refunded or the performance passed, says which and offers the order list rather than an error.",
   "preloaded": [
    "OrderSummary.id",
    "OrderSummary.orderNumber",
    "OrderSummary.status",
    "OrderSummary.grossAmount",
    "OrderSummary.refundedAmount"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P01 Guest Web.dc.html#web-030"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
 },
 {
  "id": "WEB-031",
  "name": "My Reservations",
  "module": "Ticketing",
  "requiresModule": "ticketing",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "guest-web",
   "route": "/my-reservations",
   "component": "apps/guest-web/src/routes/MyReservations.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "WEB-001",
    "WEB-030",
    "WEB-035"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "WEB-030",
     "trigger": "Ticket Transfer",
     "carries": [
      "orderId",
      "transferId"
     ],
     "provenance": "derived — WEB-030 declares entryState.params orderId, transferId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Added 17 August for parity with GST-016. **Not on the wireframe board** — needs drawing. CF-93.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listReservations` reads the population and `getReservation` reads one of them — list, select, act",
  "purpose": "What you have booked and not yet paid for.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every reservations",
       "bindsTo": "Reservation",
       "columns": [
        "Reservation.id",
        "Reservation.venueId",
        "Reservation.status",
        "Reservation.lines",
        "Reservation.expiresAt",
        "Reservation.convertedOrderId"
       ],
       "operation": "listReservations",
       "provenance": "contract orders.yaml GET /reservations"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected reservations",
       "bindsTo": "Reservation",
       "columns": [
        "Reservation.id",
        "Reservation.venueId",
        "Reservation.status",
        "Reservation.lines",
        "Reservation.expiresAt",
        "Reservation.convertedOrderId"
       ],
       "operation": "getReservation",
       "provenance": "contract orders.yaml GET /reservations/{reservationId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "destructiveButton",
       "label": "Cancel",
       "operation": "cancelReservation",
       "provenance": "contract orders.yaml DELETE /reservations/{reservationId}"
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
       "impliedBy": "getReservation",
       "notes": "One record, read-only.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "destructiveButton",
       "derived": true,
       "impliedBy": "cancelReservation",
       "label": "Cancel reservation",
       "notes": "**Always confirms, never the default focus.** The consequence goes in the body — *cancel 3 orders worth AED 480* is a confirmation, *are you sure* is not.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "cancelReservation",
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
    "id": "confirmCancelReservation",
    "component": "confirmDialog",
    "trigger": "Cancel",
    "body": "**Names what `cancelReservation` changes and what it leaves alone**, in the consequence rather than the verb. A reservations this affects should be identified in the dialog, not just counted.",
    "provenance": "contract orders.yaml DELETE /reservations/{reservationId}"
   }
  ],
  "states": {
   "loading": "The reservations list.",
   "error": "Could not load. Names which read failed and leaves the reservations untouched.",
   "emptyFirstRun": "No reservations yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the reservations are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** Reservations already loaded stay visible with their age. Booking, changing and cancelling need the connection — a table held offline is a table two people think they have."
  },
  "apis": [
   {
    "operationId": "listReservations",
    "contract": "orders",
    "purpose": "List reservations",
    "trigger": "onLoad"
   },
   {
    "operationId": "getReservation",
    "contract": "orders",
    "purpose": "Read a reservation",
    "trigger": "onLoad"
   },
   {
    "operationId": "cancelReservation",
    "contract": "orders",
    "purpose": "Cancel a reservation",
    "trigger": "onAction",
    "invalidates": [
     "listReservations"
    ]
   },
   {
    "operationId": "bookResource",
    "contract": "resources",
    "purpose": "Book a cabana or similar",
    "trigger": "onAction"
   },
   {
    "operationId": "getGroupBooking",
    "contract": "orders",
    "purpose": "A group booking this guest belongs to",
    "trigger": "onLoad"
   },
   {
    "operationId": "getResourceAvailability",
    "contract": "resources",
    "purpose": "What is free and when",
    "trigger": "onLoad"
   },
   {
    "operationId": "updateTableReservation",
    "contract": "fnb",
    "purpose": "Change or cancel it",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "reservationId",
     "from": "deepLink"
    },
    {
     "name": "groupBookingId",
     "from": "navigation"
    },
    {
     "name": "resourceId",
     "from": "navigation"
    }
   ],
   "coldEntry": "**A guest arriving cold on a link that no longer resolves is shown what happened and one way onward — never a 404.** A shared ticket, a forwarded confirmation and a push notification opened three weeks late all land here, and the person holding the link did nothing wrong. **The screen names the thing, says it is expired, cancelled or withdrawn, and offers the list it came from.** Arrives with `reservationId`.",
   "preloaded": [
    "Reservation.id",
    "Reservation.venueId",
    "Reservation.status",
    "Reservation.lines",
    "Reservation.expiresAt"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P01 Guest Web.dc.html#web-031"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
 },
 {
  "id": "WEB-035",
  "name": "Multi-Currency & Pricing",
  "module": "Ticketing",
  "requiresModule": "ticketing",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "guest-web",
   "route": "/multi-currency-pricing",
   "component": "apps/guest-web/src/routes/MulticurrencyPricing.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "WEB-001",
    "WEB-030",
    "WEB-031"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "WEB-030",
     "trigger": "Ticket Transfer",
     "carries": [
      "orderId",
      "transferId"
     ],
     "provenance": "derived — WEB-030 declares entryState.params orderId, transferId, so an edge into it must carry them"
    },
    {
     "to": "WEB-031",
     "trigger": "My Reservations",
     "carries": [
      "reservationId"
     ],
     "provenance": "derived — WEB-031 declares entryState.params reservationId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Added 17 August. **The surface the matrix names** — 2.6.33 *\"website should be able to display multi currency\"* and 2.9.1 *\"in the B2C portal for guests comparison\"*. Wave 1 against the app's Wave 2, because **the website is where an overseas guest compares before booking** and the app is where they check after. **Display only — the sale settles in base currency** (CF-37). Not on the wireframe board; needs drawing. **`getRegionSettings` deliberately not called** — a guest does not need the venue's scope configuration to pick a currency. `listFxRates` is the currency list: a rate exists only for a currency the venue enabled, so the two questions have one answer.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listFxRates` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Compare prices in your own currency before you travel.",
  "gaps": [
   {
    "operation": "listProducts",
    "why": "**1 declared operation reach no component on this screen**: listProducts. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every multi-currency pricing",
       "bindsTo": "FxRate",
       "columns": [
        "FxRate.id",
        "FxRate.fromCurrency",
        "FxRate.toCurrency",
        "FxRate.rate",
        "FxRate.purpose",
        "FxRate.source",
        "FxRate.effectiveFrom",
        "FxRate.effectiveTo",
        "FxRate.setByPrincipalId",
        "FxRate.providerReference",
        "FxRate.fetchedAt"
       ],
       "operation": "listFxRates",
       "provenance": "contract finance.yaml GET /fx-rates"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected multi-currency pricing",
       "bindsTo": "FxRate",
       "columns": [
        "FxRate.id",
        "FxRate.fromCurrency",
        "FxRate.toCurrency",
        "FxRate.rate",
        "FxRate.purpose",
        "FxRate.source",
        "FxRate.effectiveFrom",
        "FxRate.effectiveTo",
        "FxRate.setByPrincipalId",
        "FxRate.providerReference",
        "FxRate.fetchedAt"
       ],
       "operation": "listFxRates",
       "provenance": "contract finance.yaml GET /fx-rates"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The multi-currency pricing list.",
   "error": "Could not load. Names which read failed and leaves the multi-currency pricing untouched.",
   "emptyFirstRun": "No multi-currency pricing yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the multi-currency pricing are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows. Last known rates stay, with their age.** A rate is a number a guest may act on, and an undated one they cannot judge."
  },
  "apis": [
   {
    "operationId": "listFxRates",
    "contract": "finance",
    "purpose": "The rates in force",
    "trigger": "onLoad"
   },
   {
    "operationId": "listProducts",
    "contract": "catalogue",
    "purpose": "List products",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "FxRate.id",
    "FxRate.fromCurrency",
    "FxRate.toCurrency",
    "FxRate.rate",
    "FxRate.purpose"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P01 Guest Web.dc.html#web-035"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
 "bookResource": {
  "method": "POST",
  "path": "/resource-bookings",
  "contract": "resources",
  "summary": "Reserve a specific resource for a window",
  "permission": "RESOURCE_BOOK",
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
  "responds": "ResourceBooking"
 },
 "cancelReservation": {
  "method": "DELETE",
  "path": "/reservations/{reservationId}",
  "contract": "orders",
  "summary": "Cancel a reservation",
  "permission": "ORDER_CANCEL",
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
 "claimTicketTransfer": {
  "method": "POST",
  "path": "/ticket-transfers/{transferId}/claim",
  "contract": "orders",
  "summary": "Claim transferred tickets",
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
  "responds": "TicketTransfer"
 },
 "createResaleListing": {
  "method": "POST",
  "path": "/resale-listings",
  "contract": "orders",
  "summary": "List an entitlement for resale",
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
  "requestBody": "ResaleListing",
  "responds": "ResaleListing"
 },
 "getGroupBooking": {
  "method": "GET",
  "path": "/group-bookings/{groupBookingId}",
  "contract": "orders",
  "summary": "A group, its leader and its manifest",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "GroupBooking"
 },
 "getReservation": {
  "method": "GET",
  "path": "/reservations/{reservationId}",
  "contract": "orders",
  "summary": "Read a reservation",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "Reservation"
 },
 "getResourceAvailability": {
  "method": "GET",
  "path": "/resources/{resourceId}/availability",
  "contract": "resources",
  "summary": "When it is free, with conflicts already resolved",
  "permission": "RESOURCE_VIEW",
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
   }
  ],
  "requestBody": null,
  "responds": "ResourceAvailability"
 },
 "listFxRates": {
  "method": "GET",
  "path": "/fx-rates",
  "contract": "finance",
  "summary": "The rates in force",
  "permission": "LEDGER_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [
   {
    "name": "asAt",
    "in": "query",
    "required": null
   },
   {
    "name": "purpose",
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
  "responds": "FxRate"
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
 "listProducts": {
  "method": "GET",
  "path": "/products",
  "contract": "catalogue",
  "summary": "List products",
  "permission": "PRODUCT_VIEW",
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
   },
   {
    "name": "isSellable",
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
 "listReservations": {
  "method": "GET",
  "path": "/reservations",
  "contract": "orders",
  "summary": "List reservations",
  "permission": "ORDER_VIEW",
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
    "name": "expiringWithinMinutes",
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
 },
 "updateTableReservation": {
  "method": "PATCH",
  "path": "/table-reservations/{reservationId}",
  "contract": "fnb",
  "summary": "Change or cancel a booking",
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
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "CreateOrderLine": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "id",
   "variantId",
   "quantity",
   "quotedUnitPrice"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "variantId": {
    "type": "string",
    "format": "uuid"
   },
   "performanceId": {
    "type": "string",
    "format": "uuid"
   },
   "inventoryHoldId": {
    "type": "string",
    "nullable": true,
    "description": "Lease the units were drawn from. Absent for uncontended products."
   },
   "seatIds": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Seated products only. Not available offline."
   },
   "quantity": {
    "type": "integer",
    "minimum": 1
   },
   "quotedUnitPrice": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "What the client charged, from its local bundle."
   },
   "holderName": {
    "type": "string",
    "nullable": true
   },
   "dataMaskValues": {
    "type": "object",
    "additionalProperties": true
   }
  }
 },
 "FxRate": {
  "type": "object",
  "x-ticvai-persistence": "ledger.fx_rate",
  "required": [
   "fromCurrency",
   "toCurrency",
   "rate",
   "purpose",
   "effectiveFrom"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "fromCurrency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$"
   },
   "toCurrency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$"
   },
   "rate": {
    "type": "number",
    "description": "Units of `toCurrency` per one `fromCurrency`. Six decimal places — a two-place rate on a three-place currency loses money on every transaction, quietly.\n"
   },
   "purpose": {
    "$ref": "#/components/schemas/FxRatePurpose"
   },
   "source": {
    "$ref": "#/components/schemas/FxRateSource"
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date-time"
   },
   "effectiveTo": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "A rate change is a new row. The old one is never edited — a transaction posted last Tuesday must still reconcile at last Tuesday's rate.\n"
   },
   "setByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "providerReference": {
    "type": "string",
    "nullable": true,
    "description": "The provider's own identifier for this quote. **What makes a rate reproducible** — an auditor asking why a payment converted at 3.6725 gets an answer that is checkable against the source rather than a number somebody typed."
   },
   "fetchedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "When the rate was pulled. **Distinct from `effectiveFrom`**, which is when it applies — a rate fetched at 06:00 for a business day starting at 00:00 has two different times and conflating them makes a late feed look like a backdated rate."
   }
  }
 },
 "FxRatePurpose": {
  "type": "string",
  "description": "A venue does not accept dollars at the rate it books an intercompany balance at. Separating them is what stops a spread on the counter appearing as a loss in the accounts.\n",
  "enum": [
   "tender",
   "interEntity",
   "reporting",
   "revaluation"
  ]
 },
 "FxRateSource": {
  "type": "string",
  "description": "**Where the rate came from, and which provider specifically.** `source: provider` said a feed set it and not which one — two tenants on different feeds were indistinguishable in the ledger, and a rate cannot be defended in an audit without naming its origin.\n\n**`uaeCentralBank` is the default for AED pairs.** The UAE Central Bank publishes an official daily rate and it is what a UAE auditor expects to see — a commercial feed is defensible for tender and awkward for statutory reporting.\n\n**`openExchangeRates` and `ecb` are the commercial and reference options.** ECB publishes daily reference rates free and is the usual fallback for non-AED pairs; Open Exchange Rates is the common commercial feed with intraday granularity. **The choice is per purpose, not per platform** — a tender rate wants intraday, a reporting rate wants the official daily close.",
  "enum": [
   "manual",
   "uaeCentralBank",
   "ecb",
   "openExchangeRates",
   "cardScheme",
   "provider"
  ]
 },
 "GroupBooking": {
  "type": "object",
  "x-ticvai-persistence": "orders.group_booking",
  "description": "BL-028. **`BO-026 Group Bookings` ran on generic order operations** — no group size, no quota, no leader, no per-attendee capture.\n**The leader is the point.** A school booking forty places has one person who pays, one who is called if the coach is late, and forty who need names collecting — and a generic order has one guest.\n",
  "required": [
   "id",
   "orderId",
   "leaderSubjectId",
   "expectedSize",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "orderId": {
    "type": "string",
    "format": "uuid"
   },
   "leaderSubjectId": {
    "type": "string",
    "format": "uuid"
   },
   "organisationName": {
    "type": "string",
    "nullable": true
   },
   "expectedSize": {
    "type": "integer"
   },
   "confirmedSize": {
    "type": "integer",
    "nullable": true
   },
   "minimumSize": {
    "type": "integer",
    "nullable": true,
    "description": "**Below which the group rate does not apply.** A booking for forty that arrives as twelve is a pricing question somebody has to answer at the gate, and stating the threshold means answering it at booking instead.\n"
   },
   "attendeeCaptureRequired": {
    "type": "boolean",
    "default": false,
    "description": "**Whether names are needed before admission.** A school trip usually needs them and a corporate day out usually does not, and the difference is a safeguarding requirement rather than a preference.\n"
   },
   "attendeeCaptureDueBy": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "provisional",
     "confirmed",
     "namesPending",
     "complete",
     "cancelled"
    ]
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
 "ResaleListing": {
  "type": "object",
  "x-ticvai-persistence": "orders.resale_listing",
  "description": "BL-060. **Smaller than it first looked** — most of the machinery exists. An entitlement can already be transferred, an order can already be created, and payment already routes. What was missing is the listing itself and a cart line that can point at one.\n**A resale is a transfer with money attached**, and the venue is in the middle: the seller's entitlement is voided and a new one issued to the buyer, so **the ticket that admits is always one the venue issued.** That is what stops a screenshot at the gate.\n",
  "required": [
   "id",
   "entitlementId",
   "sellerSubjectId",
   "askPrice",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "entitlementId": {
    "type": "string",
    "format": "uuid"
   },
   "sellerSubjectId": {
    "type": "string",
    "format": "uuid"
   },
   "askPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "priceCapPercent": {
    "type": "number",
    "nullable": true,
    "description": "**A ceiling as a percentage of face value**, because uncapped resale is a venue watching its own tickets sold at four times the price with its name on them. Null means uncapped, which is a venue decision rather than a default.\n"
   },
   "sellerFeePercent": {
    "type": "number"
   },
   "buyerFeePercent": {
    "type": "number"
   },
   "status": {
    "type": "string",
    "enum": [
     "listed",
     "reserved",
     "sold",
     "withdrawn",
     "expired"
    ]
   },
   "listedAt": {
    "type": "string",
    "format": "date-time"
   },
   "soldToSubjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "payoutStatus": {
    "type": "string",
    "enum": [
     "pending",
     "held",
     "paid",
     "failed"
    ],
    "description": "**The seller is paid after the buyer is admitted, not after they pay.** A resale refunded at the gate for a void ticket cannot be clawed back from a seller who has already been paid.\n"
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"
   }
  }
 },
 "Reservation": {
  "x-ticvai-persistence": "orders.reservation",
  "type": "object",
  "required": [
   "id",
   "venueId",
   "status",
   "expiresAt",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "status": {
    "type": "string",
    "enum": [
     "held",
     "converted",
     "expired",
     "cancelled"
    ]
   },
   "lines": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/CreateOrderLine"
    }
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "convertedOrderId": {
    "type": "string",
    "nullable": true
   }
  }
 },
 "ResourceAvailability": {
  "type": "object",
  "description": "**Free windows, with setup and teardown already subtracted.** A client computing this from bookings will forget the turnaround.\n",
  "properties": {
   "resourceId": {
    "type": "string",
    "format": "uuid"
   },
   "freeWindows": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "from": {
       "type": "string",
       "format": "date-time"
      },
      "to": {
       "type": "string",
       "format": "date-time"
      }
     }
    }
   },
   "blockedWindows": {
    "type": "array",
    "description": "**With a reason, because they are not the same.** Booked and under repair need different responses from an operator looking for something free — wait, or look elsewhere.\n",
    "items": {
     "type": "object",
     "properties": {
      "from": {
       "type": "string",
       "format": "date-time"
      },
      "to": {
       "type": "string",
       "format": "date-time"
      },
      "reason": {
       "type": "string",
       "enum": [
        "booked",
        "setup",
        "teardown",
        "maintenance",
        "blackout",
        "closed"
       ]
      }
     }
    }
   }
  }
 },
 "ResourceBooking": {
  "type": "object",
  "x-ticvai-persistence": "resources.booking",
  "required": [
   "id",
   "resourceId",
   "from",
   "to",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "resourceId": {
    "type": "string",
    "format": "uuid"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "orderId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "from": {
    "type": "string",
    "format": "date-time"
   },
   "to": {
    "type": "string",
    "format": "date-time"
   },
   "status": {
    "type": "string",
    "enum": [
     "reserved",
     "checkedOut",
     "returned",
     "overdue",
     "cancelled",
     "noShow"
    ]
   },
   "recurrenceGroupId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Ties the occurrences of a recurring booking. **Cancelling one week does not cancel the series**, and cancelling the series is a separate act with a separate confirmation.\n"
   },
   "depositAuthorisationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The hold, through `orders.authoriseStoredValue` (CF-126). **A deposit taken and refunded is two transactions and a fee; held and released is neither.**\n"
   },
   "checkedOutAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "dueBackAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "returnedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "conditionOut": {
    "type": "string",
    "nullable": true
   },
   "conditionIn": {
    "type": "string",
    "nullable": true
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
 "TicketTransfer": {
  "x-ticvai-persistence": "orders.ticket_transfer",
  "type": "object",
  "required": [
   "id",
   "orderId",
   "ticketIds",
   "status",
   "offeredAt",
   "expiresAt"
  ],
  "properties": {
   "id": {
    "type": "string"
   },
   "orderId": {
    "type": "string"
   },
   "ticketIds": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "fromSubjectId": {
    "type": "string",
    "format": "uuid"
   },
   "toSubjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Set only on claim. Ownership moves then, not at offer."
   },
   "recipientAddressMasked": {
    "type": "string"
   },
   "status": {
    "type": "string",
    "enum": [
     "offered",
     "claimed",
     "expired",
     "cancelled"
    ]
   },
   "claimUrl": {
    "type": "string",
    "nullable": true
   },
   "offeredAt": {
    "type": "string",
    "format": "date-time"
   },
   "claimedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "description": "An unclaimed transfer expires and the tickets return. A transfer to a mistyped address must not strand a ticket somewhere nobody can reach.\n"
   }
  }
 }
}
```
