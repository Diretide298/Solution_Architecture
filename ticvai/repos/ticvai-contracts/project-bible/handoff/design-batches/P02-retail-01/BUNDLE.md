# P02-retail-01 — P02 · Retail

**1 screens · 4 operations · 4 schemas · 2 permissions**

Platform P02 Guest App · ships as **guest** ·
guest audience · mobileApp ·
offline-capable

## Who this is for

**guest on mobileApp.** Everything below is how you know what is
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

- **Every control that can be refused must be gated.** 2 permissions apply here:
  `ORDER_CREATE, PRODUCT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **2 of these operations work offline**: getGameCard, listMerchandise
  — and the rest do not. A surface that looks the same online and off is lying.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `GST-026` | Retail / Merchandise | listDetail | 4 | 0 | — |

## Thin screens in this batch

**GST-026 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "GST-026",
  "name": "Retail / Merchandise",
  "module": "Retail",
  "requiresModule": "games",
  "wave": 2,
  "capability": "C08",
  "implementation": {
   "app": "guest-app",
   "route": "/general/retail-merchandise",
   "component": "apps/guest-app/src/routes/general/RetailMerchandiseDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "GST-001"
   ],
   "inferred": true,
   "exitTo": [
    "GST-001",
    "GST-002",
    "GST-003"
   ],
   "fromFlows": true,
   "transitions": [
    {
     "to": "GST-001",
     "trigger": "Home – Default",
     "carries": [
      "subjectId"
     ],
     "provenance": "derived — GST-001 declares entryState.params subjectId, so an edge into it must carry them"
    },
    {
     "to": "GST-003",
     "trigger": "Event & Attraction Listing",
     "carries": [
      "eventId"
     ],
     "provenance": "derived — GST-003 declares entryState.params eventId, so an edge into it must carry them"
    },
    {
     "to": "BO-048",
     "trigger": "Collected on the way out",
     "provenance": "flow F17 step 4→5",
     "operation": "listMerchandise",
     "crossesDevice": true,
     "back": false
    },
    {
     "to": "BO-069",
     "trigger": "Machine records the play",
     "provenance": "flow F18 step 2→3",
     "operation": "getGameCard",
     "crossesDevice": true,
     "back": false
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Cross-platform navigation removed 24 August**: BO-048, BO-069. **A till does not navigate to a back office and a guest app does not navigate to either** — those are device handovers, and a flow declares them with `crossesDevice` rather than a screen pretending there is a link.",
  "openQuestions": [
   "Inventory cites `GET /products?kind=retail` — no matching operation. Written before the contracts existed."
  ],
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listMerchandise` reads the population and `getGameCard` reads one of them — list, select, act",
  "purpose": "Find retail / merchandise for this venue.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every retail merchandise",
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
       "label": "The selected retail merchandise",
       "bindsTo": "GameCard",
       "columns": [
        "GameCard.cardCode",
        "GameCard.kind",
        "GameCard.venueId",
        "GameCard.subjectId",
        "GameCard.credits",
        "GameCard.bonusCredits",
        "GameCard.points",
        "GameCard.status",
        "GameCard.blockedReason",
        "GameCard.transferredToCardCode",
        "GameCard.lastPlayedAt",
        "GameCard.issuedAt",
        "GameCard.expiresAt"
       ],
       "operation": "getGameCard",
       "provenance": "contract games.yaml GET /game-cards/{cardCode}"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The retail merchandise list.",
   "error": "Could not load. Names which read failed and leaves the retail merchandise untouched.",
   "emptyFirstRun": "No retail merchandise yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the retail merchandise are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "Cached content with its age. **Nothing that spends money or holds capacity works offline**"
  },
  "apis": [
   {
    "operationId": "getGameCard",
    "contract": "games",
    "purpose": "Read a card's balances",
    "trigger": "onLoad"
   },
   {
    "operationId": "listMerchandise",
    "contract": "retail",
    "purpose": "List merchandise",
    "trigger": "onLoad"
   },
   {
    "operationId": "lookupMerchandise",
    "contract": "retail",
    "purpose": "Find an item by code or scan",
    "trigger": "onLoad"
   },
   {
    "operationId": "reserveMerchandise",
    "contract": "retail",
    "purpose": "Hold it for collection",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "cardCode",
     "from": "deepLink"
    },
    {
     "name": "outletId",
     "from": "session"
    }
   ],
   "coldEntry": "**A guest arriving cold on a link that no longer resolves is shown what happened and one way onward — never a 404.** A shared ticket, a forwarded confirmation and a push notification opened three weeks late all land here, and the person holding the link did nothing wrong. **The screen names the thing, says it is expired, cancelled or withdrawn, and offers the list it came from.** Arrives with `cardCode`.",
   "preloaded": [
    "GameCard.cardCode",
    "GameCard.kind",
    "GameCard.venueId",
    "GameCard.subjectId",
    "GameCard.credits"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P02 Guest App.dc.html#gst-026"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P02",
   "audience": "guest",
   "formFactor": "mobileApp",
   "shortName": "Guest App",
   "name": "Guest App — Mobile",
   "offlineCapable": true,
   "app": "guest-app",
   "operator": "guest",
   "targetApp": {
    "app": "guest",
    "name": "TICVAI Guest",
    "shell": "mobile",
    "siblings": [
     "P01",
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
 "getGameCard": {
  "method": "GET",
  "path": "/game-cards/{cardCode}",
  "contract": "games",
  "summary": "Read a card's balances",
  "permission": null,
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "GameCard"
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
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "GameCard": {
  "x-ticvai-persistence": "games.card",
  "type": "object",
  "required": [
   "cardCode",
   "venueId",
   "credits",
   "bonusCredits",
   "points",
   "status",
   "issuedAt"
  ],
  "properties": {
   "cardCode": {
    "type": "string"
   },
   "kind": {
    "type": "string"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "credits": {
    "type": "integer",
    "description": "Bought with money. Buys plays."
   },
   "bonusCredits": {
    "type": "integer",
    "description": "From a promotion. Typically non-refundable and spent before paid credits.\n"
   },
   "points": {
    "type": "integer",
    "description": "Won by playing. Buys prizes. **Not interchangeable with credits** — a guest who wins should not simply be able to play more.\n"
   },
   "status": {
    "type": "string",
    "enum": [
     "active",
     "blocked",
     "expired",
     "transferred"
    ]
   },
   "blockedReason": {
    "type": "string",
    "nullable": true
   },
   "transferredToCardCode": {
    "type": "string",
    "nullable": true
   },
   "lastPlayedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "issuedAt": {
    "type": "string",
    "format": "date-time"
   },
   "expiresAt": {
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
 }
}
```
