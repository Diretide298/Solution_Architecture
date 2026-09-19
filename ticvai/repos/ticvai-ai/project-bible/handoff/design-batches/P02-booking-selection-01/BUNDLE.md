# P02-booking-selection-01 — P02 · Booking & Selection

**8 screens · 16 operations · 20 schemas · 7 permissions**

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

- **Every control that can be refused must be gated.** 7 permissions apply here:
  `GUEST_VIEW, MARKETING_MANAGE, MARKETING_VIEW, ORDER_CREATE, ORDER_MODIFY, ORDER_VIEW, PRODUCT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **5 of these operations work offline**: getBundle, getUpsellSuggestions, listCatalogueBundles, listPerformances, listProducts
  — and the rest do not. A surface that looks the same online and off is lying.
- **Offline, every screen shows one banner, the same on web and app:** *"You're offline. Connect to the internet to book, pay, order or join a queue."* The moment the connection drops, on every screen, above the screen's own content. By itself as soon as the connection is back, with a short "Back online" confirmation. **It never** Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing. Each screen's `states.offline` says what stays on screen and what waits.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `GST-007` | Select Date & Time | listDetail | 2 | 0 | — |
| `GST-008` | Tickets & Add-ons | configEditor | 1 | 0 | — |
| `GST-048` | Upsell / Cross-Sell | statusTracker | 2 | 0 | — |
| `GST-049` | Interactive Seat Selection | statusTracker | 3 | 0 | — |
| `GST-050` | Resource Booking – Cabana | listDetail | 3 | 0 | — |
| `GST-056` | Bundle Package | listDetail | 3 | 0 | — |
| `GST-058` | Resource Availability (Cabana) | listDetail | 2 | 0 | — |
| `GST-072` | Share & Group Booking | statusTracker | 5 | 0 | — |

## Thin screens in this batch

**GST-007, GST-008, GST-048, GST-050, GST-056, GST-058 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "GST-007",
  "name": "Select Date & Time",
  "module": "Booking & Selection",
  "requiresModule": "ticketing",
  "wave": 1,
  "capability": "C02",
  "implementation": {
   "app": "guest-app",
   "route": "/general/select-date-and-time",
   "component": "apps/guest-app/src/routes/general/SelectDateAndTimeDetail.tsx",
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
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement.",
  "openQuestions": [
   "Inventory cites `GET /performances, POST /inventory-holds` — no matching operation. Written before the contracts existed."
  ],
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listPerformances` reads the population and `getAvailability` reads one of them — list, select, act",
  "purpose": "See select date & time for this venue.",
  "gaps": [
   {
    "operation": "getAvailability",
    "why": "**1 declared operation reach no component on this screen**: getAvailability. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every select date time",
       "bindsTo": "Performance",
       "columns": [
        "Performance.id",
        "Performance.eventId",
        "Performance.startsAt",
        "Performance.endsAt",
        "Performance.approvalRequestId",
        "Performance.requiresApprovalToCancel",
        "Performance.status",
        "Performance.admissionRulesId",
        "Performance.seatMapId"
       ],
       "operation": "listPerformances",
       "provenance": "contract catalogue.yaml GET /events/{eventId}/performances"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The select date time list.",
   "error": "Could not load. Names which read failed and leaves the select date time untouched.",
   "emptyFirstRun": "No select date time yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the select date time are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing."
  },
  "apis": [
   {
    "operationId": "listPerformances",
    "contract": "catalogue",
    "purpose": "List performances of an event",
    "trigger": "onLoad"
   },
   {
    "operationId": "getAvailability",
    "contract": "catalogue",
    "purpose": "Live remaining capacity",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "eventId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A guest arriving cold on a link that no longer resolves is shown what happened and one way onward — never a 404.** A shared ticket, a forwarded confirmation and a push notification opened three weeks late all land here, and the person holding the link did nothing wrong. **The screen names the thing, says it is expired, cancelled or withdrawn, and offers the list it came from.** Arrives with `eventId`.",
   "preloaded": []
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P02 Guest App.dc.html#gst-007"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P02",
   "audience": "guest",
   "formFactor": "mobileApp",
   "shortName": "Guest App",
   "name": "Guest App — Mobile",
   "offlineCapable": true,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
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
 },
 {
  "id": "GST-008",
  "name": "Tickets & Add-ons",
  "module": "Booking & Selection",
  "requiresModule": "ticketing",
  "wave": 1,
  "capability": "C02",
  "implementation": {
   "app": "guest-app",
   "route": "/general/tickets-and-add-ons",
   "component": "apps/guest-app/src/routes/general/TicketsAndAddOnsList.tsx",
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
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement.",
  "openQuestions": [
   "Inventory cites `local` — no matching operation. Written before the contracts existed."
  ],
  "density": "comfortable",
  "pattern": "configEditor",
  "patternReason": "the screen declares only writes (`transferOrderTickets`) and no read of a population — it is settings, not a list",
  "purpose": "Find tickets & add-ons for this venue.",
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
     "components": [
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "transferOrderTickets"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The saved tickets add-ons.",
   "error": "Could not load. Names which read failed and leaves the tickets add-ons untouched.",
   "emptyFirstRun": "No tickets add-ons configured. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing."
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
   "board": "wireframes/P02 Guest App.dc.html#gst-008"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 1 operation this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P02",
   "audience": "guest",
   "formFactor": "mobileApp",
   "shortName": "Guest App",
   "name": "Guest App — Mobile",
   "offlineCapable": true,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
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
 },
 {
  "id": "GST-048",
  "name": "Upsell / Cross-Sell",
  "module": "Booking & Selection",
  "requiresModule": "ticketing",
  "wave": 2,
  "capability": "C88",
  "implementation": {
   "app": "guest-app",
   "route": "/general/upsell-cross-sell",
   "component": "apps/guest-app/src/routes/general/UpsellCrossSellDetail.tsx",
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
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement.",
  "openQuestions": [
   "Inventory cites `GET /recommendations` — no matching operation. Written before the contracts existed."
  ],
  "density": "comfortable",
  "pattern": "statusTracker",
  "patternReason": "`getUpsellSuggestions` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "See upsell / cross-sell for this venue.",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected upsell cross-sell",
       "bindsTo": "UpsellSuggestion",
       "columns": [
        "UpsellSuggestion.variantId",
        "UpsellSuggestion.bundleId",
        "UpsellSuggestion.name",
        "UpsellSuggestion.price",
        "UpsellSuggestion.discountedPrice",
        "UpsellSuggestion.source",
        "UpsellSuggestion.ruleId",
        "UpsellSuggestion.rank",
        "UpsellSuggestion.rationale"
       ],
       "operation": "getUpsellSuggestions",
       "provenance": "contract promotions.yaml POST /upsell-suggestions"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Add",
       "operation": "addCartLine",
       "provenance": "contract orders.yaml POST /carts/{cartId}/lines"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The upsell cross-sell list.",
   "error": "Could not load. Names which read failed and leaves the upsell cross-sell untouched.",
   "emptyFirstRun": "No upsell cross-sell yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the upsell cross-sell are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing."
  },
  "apis": [
   {
    "operationId": "addCartLine",
    "contract": "orders",
    "purpose": "Add something",
    "trigger": "onAction"
   },
   {
    "operationId": "getUpsellSuggestions",
    "contract": "promotions",
    "purpose": "Suggestions for a cart",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "cartId",
     "from": "session"
    }
   ],
   "coldEntry": "Resolves from the session; a cold arrival is the ordinary case."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P02 Guest App.dc.html#gst-048"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P02",
   "audience": "guest",
   "formFactor": "mobileApp",
   "shortName": "Guest App",
   "name": "Guest App — Mobile",
   "offlineCapable": true,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
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
 },
 {
  "id": "GST-049",
  "name": "Interactive Seat Selection",
  "module": "Booking & Selection",
  "requiresModule": "seating",
  "wave": 2,
  "capability": "C53",
  "implementation": {
   "app": "guest-app",
   "route": "/general/interactive-seat-selection",
   "component": "apps/guest-app/src/routes/general/InteractiveSeatSelectionCanvas.tsx",
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
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Drawn 26 August** — `Seat Board 4.dc.html` frame `seat-4a`. **The frame names this screen on its own face**, which is the first pack to do that: the earlier F&B, POS and Retail boards had to be hand-assigned by purpose after three derivation attempts produced nonsense. **A board that says what it draws removes the guess entirely.**",
  "density": "comfortable",
  "boardFrames": [
   "Seat Board 4.dc.html#seat-4a"
  ],
  "pattern": "statusTracker",
  "patternReason": "`getSeatAvailability` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "See interactive seat selection for this venue.",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected interactive seat selection",
       "bindsTo": "SeatAvailability",
       "columns": [
        "SeatAvailability.performanceId",
        "SeatAvailability.seatMapId",
        "SeatAvailability.totals",
        "SeatAvailability.byCategory",
        "SeatAvailability.seats"
       ],
       "operation": "getSeatAvailability",
       "provenance": "contract seating.yaml GET /performances/{performanceId}/seat-availability"
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
       "operation": "createSeatHold",
       "provenance": "contract seating.yaml POST /seat-holds"
      },
      {
       "kind": "secondaryButton",
       "label": "Recommend",
       "operation": "recommendSeats",
       "provenance": "contract seating.yaml POST /performances/{performanceId}/seat-recommendations"
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
       "impliedBy": "getSeatAvailability",
       "notes": "One record, read-only.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createSeatHold",
       "label": "Create seat hold",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createSeatHold",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "seatMap",
       "label": "Choose seats",
       "notes": "**A seat selection screen with no seat map.** `noGeometry` is the state that matters: a map imported from a manifest alone can be sold from a list and not rendered, and the screen has to say which it is rather than showing an empty frame.",
       "provenance": "minute 2026-08-03 §Ticket Flow Variations by Product Type"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The interactive seat selection list.",
   "error": "Could not load. Names which read failed and leaves the interactive seat selection untouched.",
   "emptyFirstRun": "No interactive seat selection yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the interactive seat selection are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing."
  },
  "apis": [
   {
    "operationId": "getSeatAvailability",
    "contract": "seating",
    "purpose": "Seat status for a performance",
    "trigger": "onLoad"
   },
   {
    "operationId": "createSeatHold",
    "contract": "seating",
    "purpose": "Hold specific seats",
    "trigger": "onAction"
   },
   {
    "operationId": "recommendSeats",
    "contract": "seating",
    "purpose": "Recommend seats for a party",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "performanceId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A link to a performance that has happened.** Offers the next performance of the same event."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P02 Guest App.dc.html#gst-049",
   "note": "**Drawn by Claude Design on `Seat Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P02",
   "audience": "guest",
   "formFactor": "mobileApp",
   "shortName": "Guest App",
   "name": "Guest App — Mobile",
   "offlineCapable": true,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
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
 },
 {
  "id": "GST-050",
  "name": "Resource Booking – Cabana",
  "module": "Booking & Selection",
  "requiresModule": "ticketing",
  "wave": 3,
  "capability": "C78",
  "implementation": {
   "app": "guest-app",
   "route": "/general/resource-booking-cabana",
   "component": "apps/guest-app/src/routes/general/ResourceBookingCabanaDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "GST-001",
    "GST-058"
   ],
   "inferred": true,
   "exitTo": [
    "GST-001",
    "GST-002",
    "GST-003",
    "GST-016"
   ],
   "transitions": [
    {
     "to": "GST-016",
     "trigger": "They see it in their reservations",
     "provenance": "flow F52 step 2→3"
    },
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
    }
   ]
  },
  "notes": "Minuted 10 Aug §4.8: *\"resource bookings (e.g., cabana rental) decrement a capacity-based inventory on booking\"*. **Distinct from GST-058**: this is one resource with a price and a booking action; GST-058 is availability across areas. Confirmed against storyboard boards 7.10 and 8.8 on 18 August.",
  "openQuestions": [
   "Inventory cites `POST /resource-bookings` — no matching operation. Written before the contracts existed."
  ],
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listProducts` reads the population and `getAvailability` reads one of them — list, select, act",
  "purpose": "Book a cabana or other capacity-based resource.",
  "gaps": [
   {
    "operation": "getAvailability",
    "why": "**1 declared operation reach no component on this screen**: getAvailability. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every resource booking cabana",
       "bindsTo": "Product",
       "columns": [
        "Product.id",
        "Product.code",
        "Product.name",
        "Product.description",
        "Product.kind",
        "Product.venueId",
        "Product.scopePath",
        "Product.createdByPrincipalId",
        "Product.approvedByPrincipalId",
        "Product.responsibleDepartmentId",
        "Product.onSaleFrom",
        "Product.onSaleTo"
       ],
       "operation": "listProducts",
       "provenance": "contract catalogue.yaml GET /products"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Add",
       "operation": "addCartLine",
       "provenance": "contract orders.yaml POST /carts/{cartId}/lines"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The resource booking cabana list.",
   "error": "Could not load. Names which read failed and leaves the resource booking cabana untouched.",
   "emptyFirstRun": "No resource booking cabana yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the resource booking cabana are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing."
  },
  "apis": [
   {
    "operationId": "addCartLine",
    "contract": "orders",
    "purpose": "Add something",
    "trigger": "onAction",
    "invalidates": [
     "listProducts"
    ]
   },
   {
    "operationId": "listProducts",
    "contract": "catalogue",
    "purpose": "List products",
    "trigger": "onLoad"
   },
   {
    "operationId": "getAvailability",
    "contract": "catalogue",
    "purpose": "Live remaining capacity",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "cartId",
     "from": "session"
    }
   ],
   "coldEntry": "Resolves from the session; a cold arrival is the ordinary case.",
   "preloaded": []
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P02 Guest App.dc.html#gst-050"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P02",
   "audience": "guest",
   "formFactor": "mobileApp",
   "shortName": "Guest App",
   "name": "Guest App — Mobile",
   "offlineCapable": true,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
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
 },
 {
  "id": "GST-056",
  "name": "Bundle Package",
  "module": "Booking & Selection",
  "requiresModule": "ticketing",
  "wave": 2,
  "capability": "C87",
  "implementation": {
   "app": "guest-app",
   "route": "/general/bundle-package",
   "component": "apps/guest-app/src/routes/general/BundlePackageDetail.tsx",
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
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered. Purpose derived from the screen name and its operations on 17 August, not from a requirement.",
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listCatalogueBundles` reads the population and `getBundle` reads one of them — list, select, act",
  "purpose": "See bundle package for this venue.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every bundle package",
       "bindsTo": "BundleSummary",
       "columns": [
        "BundleSummary.venueId",
        "BundleSummary.publishedAt",
        "BundleSummary.publishedBy",
        "BundleSummary.contentHash",
        "BundleSummary.signatureKeyId",
        "BundleSummary.staleAfter",
        "BundleSummary.sizeBytes",
        "BundleSummary.note",
        "BundleSummary.appliedByWorkstations"
       ],
       "operation": "listCatalogueBundles",
       "provenance": "contract catalogue.yaml GET /catalogue/bundles"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected bundle package",
       "bindsTo": "Bundle",
       "columns": [
        "Bundle.code",
        "Bundle.name",
        "Bundle.description",
        "Bundle.venueId",
        "Bundle.kind",
        "Bundle.price",
        "Bundle.components",
        "Bundle.choiceGroups",
        "Bundle.allocation",
        "Bundle.validFrom",
        "Bundle.validTo",
        "Bundle.id",
        "Bundle.savingsAmount",
        "Bundle.savingsPercentage",
        "Bundle.hasBeenSold",
        "Bundle.isActive"
       ],
       "operation": "getBundle",
       "provenance": "contract promotions.yaml GET /bundles/{bundleId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Add",
       "operation": "addCartLine",
       "provenance": "contract orders.yaml POST /carts/{cartId}/lines"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The bundle package list.",
   "error": "Could not load. Names which read failed and leaves the bundle package untouched.",
   "emptyFirstRun": "No bundle package yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the bundle package are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing."
  },
  "apis": [
   {
    "operationId": "listCatalogueBundles",
    "contract": "catalogue",
    "purpose": "List published bundles",
    "trigger": "onLoad"
   },
   {
    "operationId": "getBundle",
    "contract": "promotions",
    "purpose": "Read a bundle with components and allocation",
    "trigger": "onLoad"
   },
   {
    "operationId": "addCartLine",
    "contract": "orders",
    "purpose": "Add something",
    "trigger": "onAction",
    "invalidates": [
     "listCatalogueBundles"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "bundleId",
     "from": "deepLink"
    },
    {
     "name": "cartId",
     "from": "session"
    }
   ],
   "coldEntry": "**A guest arriving cold on a link that no longer resolves is shown what happened and one way onward — never a 404.** A shared ticket, a forwarded confirmation and a push notification opened three weeks late all land here, and the person holding the link did nothing wrong. **The screen names the thing, says it is expired, cancelled or withdrawn, and offers the list it came from.** Arrives with `bundleId`.",
   "preloaded": [
    "Bundle.code",
    "Bundle.name",
    "Bundle.description",
    "Bundle.venueId",
    "Bundle.kind"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P02 Guest App.dc.html#gst-056"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P02",
   "audience": "guest",
   "formFactor": "mobileApp",
   "shortName": "Guest App",
   "name": "Guest App — Mobile",
   "offlineCapable": true,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
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
 },
 {
  "id": "GST-058",
  "name": "Resource Availability (Cabana)",
  "module": "Booking & Selection",
  "requiresModule": "ticketing",
  "wave": 3,
  "capability": "C78",
  "implementation": {
   "app": "guest-app",
   "route": "/general/resource-availability-cabana",
   "component": "apps/guest-app/src/routes/general/ResourceAvailabilityCabanaDetail.tsx",
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
    "GST-003",
    "GST-050"
   ],
   "transitions": [
    {
     "to": "GST-050",
     "trigger": "They book and pay",
     "provenance": "flow F52 step 1→2"
    },
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
    }
   ]
  },
  "notes": "**Deliberately separate from GST-050**, and checked on 18 August. Board 8 panel 8 is availability across areas with counts remaining; board 7 panel 10 is one cabana with a price and a Book Now. **A list and a detail, not a duplicate** — merging them would put a booking action on a browsing screen.",
  "openQuestions": [
   "Inventory cites `GET /resources/availability` — no matching operation. Written before the contracts existed."
  ],
  "density": "comfortable",
  "pattern": "listDetail",
  "patternReason": "`listProducts` reads the population and `getAvailability` reads one of them — list, select, act",
  "purpose": "See which cabanas are free, by area and date, before choosing one.",
  "gaps": [
   {
    "operation": "getAvailability",
    "why": "**1 declared operation reach no component on this screen**: getAvailability. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every resource availability (cabana)",
       "bindsTo": "Product",
       "columns": [
        "Product.id",
        "Product.code",
        "Product.name",
        "Product.description",
        "Product.kind",
        "Product.venueId",
        "Product.scopePath",
        "Product.createdByPrincipalId",
        "Product.approvedByPrincipalId",
        "Product.responsibleDepartmentId",
        "Product.onSaleFrom",
        "Product.onSaleTo"
       ],
       "operation": "listProducts",
       "provenance": "contract catalogue.yaml GET /products"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The resource availability (cabana) list.",
   "error": "Could not load. Names which read failed and leaves the resource availability (cabana) untouched.",
   "emptyFirstRun": "No resource availability (cabana) yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the resource availability (cabana) are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing."
  },
  "apis": [
   {
    "operationId": "getAvailability",
    "contract": "catalogue",
    "purpose": "Live remaining capacity",
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
   "preloaded": []
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P02 Guest App.dc.html#gst-058"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P02",
   "audience": "guest",
   "formFactor": "mobileApp",
   "shortName": "Guest App",
   "name": "Guest App — Mobile",
   "offlineCapable": true,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
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
 },
 {
  "id": "GST-072",
  "name": "Share & Group Booking",
  "module": "Booking & Selection",
  "requiresModule": "core",
  "wave": 2,
  "capability": "read-write",
  "implementation": {
   "app": "guest-app",
   "route": "/account/share-group-booking",
   "component": "apps/guest-app/src/routes/account/ShareGroupBooking.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "GST-039"
   ],
   "entryFrom": [
    "GST-008"
   ],
   "inferred": false,
   "notes": "**Reached from GST-008** — sharing starts from the ticket being shared. Stated on 4 September: this screen exited somewhere and nothing exited to it, so it was outside the navigation graph entirely.",
   "transitions": [
    {
     "to": "GST-039",
     "trigger": "Profile",
     "carries": [
      "subjectId"
     ],
     "provenance": "derived — GST-039 declares entryState.params subjectId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "**A guest buying eight tickets could not give seven of them away.** `shareEntitlement`, `getGroupBooking` and `respondToInvitation` had no surface, so a group booking was one person holding eight barcodes.\n\n**`createReferral` writes `marketing.referral`, which nothing reads** — one of the sixteen orphan writes. This screen is where the reward would be visible, and it stays an open question until the wallet session settles what a referral credit is.",
  "density": "comfortable",
  "offline": false,
  "pattern": "statusTracker",
  "patternReason": "`getGroupBooking` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "**A guest buying eight tickets could not give seven of them away.** `shareEntitlement`, `getGroupBooking` and `respondToInvitation` had no surface, so a group booking was one person holding eight barc",
  "gaps": [
   {
    "operation": "getMyChallenges",
    "why": "**1 declared operation reach no component on this screen**: getMyChallenges. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "The selected share group booking",
       "bindsTo": "GroupBooking",
       "columns": [
        "GroupBooking.id",
        "GroupBooking.orderId",
        "GroupBooking.leaderSubjectId",
        "GroupBooking.organisationName",
        "GroupBooking.expectedSize",
        "GroupBooking.confirmedSize",
        "GroupBooking.minimumSize",
        "GroupBooking.attendeeCaptureRequired",
        "GroupBooking.attendeeCaptureDueBy",
        "GroupBooking.status"
       ],
       "operation": "getGroupBooking",
       "provenance": "contract orders.yaml GET /group-bookings/{groupBookingId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Share",
       "operation": "shareEntitlement",
       "provenance": "contract orders.yaml POST /entitlements/{entitlementId}/share"
      },
      {
       "kind": "secondaryButton",
       "label": "Respond",
       "operation": "respondToInvitation",
       "provenance": "contract marketing-crm.yaml POST /invitations/{token}/respond"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createReferral",
       "provenance": "contract marketing-crm.yaml POST /referrals"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Content loads.",
   "error": "Could not load. **Says what failed and offers one way onward**, never a bare failure.",
   "emptyFirstRun": "**Nothing shared.** A guest holding eight tickets sees the option here rather than discovering it at the gate.",
   "emptyNoResults": "**Nothing here yet.** The scope is what narrowed it — naming the scope is what stops somebody concluding the record does not exist.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "offline": "**The offline banner shows.** Tickets already shared stay visible. Sharing, invitations and referrals need the connection — a transfer nobody received is a ticket nobody holds."
  },
  "apis": [
   {
    "operationId": "shareEntitlement",
    "contract": "orders",
    "purpose": "Let somebody else use this, without giving it away",
    "trigger": "onAction"
   },
   {
    "operationId": "getGroupBooking",
    "contract": "orders",
    "purpose": "getGroupBooking",
    "trigger": "onLoad"
   },
   {
    "operationId": "respondToInvitation",
    "contract": "marketing-crm",
    "purpose": "Accept or decline",
    "trigger": "onAction"
   },
   {
    "operationId": "createReferral",
    "contract": "marketing-crm",
    "purpose": "Issue a referral code",
    "trigger": "onAction"
   },
   {
    "operationId": "getMyChallenges",
    "contract": "marketing-crm",
    "purpose": "Active challenges and how far along I am",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "entitlementId",
     "from": "deepLink"
    },
    {
     "name": "groupBookingId",
     "from": "deepLink"
    },
    {
     "name": "subjectId",
     "from": "session"
    },
    {
     "name": "token",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**Resolves from the session.** A guest arriving cold is asked to sign in and returned here afterwards — never a 404, and never a screen that silently shows somebody else's data (ADR-0030)."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P02 Guest App.dc.html#gst-072"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 5 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P02",
   "audience": "guest",
   "formFactor": "mobileApp",
   "shortName": "Guest App",
   "name": "Guest App — Mobile",
   "offlineCapable": true,
   "offlineBanner": {
    "kind": "banner",
    "state": "warning",
    "message": "You're offline. Connect to the internet to book, pay, order or join a queue.",
    "shows": "The moment the connection drops, on every screen, above the screen's own content.",
    "clears": "By itself as soon as the connection is back, with a short \"Back online\" confirmation.",
    "never": "Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing.",
    "provenance": "Decided 12 September 2026 — guest web and guest app behave identically offline and say so with the same banner."
   },
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
 "createReferral": {
  "method": "POST",
  "path": "/referrals",
  "contract": "marketing-crm",
  "summary": "Issue a referral code",
  "permission": "MARKETING_MANAGE",
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
  "requestBody": "Referral",
  "responds": "Referral"
 },
 "createSeatHold": {
  "method": "POST",
  "path": "/seat-holds",
  "contract": "seating",
  "summary": "Hold specific seats",
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
  "requestBody": "CreateSeatHoldRequest",
  "responds": "SeatHold"
 },
 "getAvailability": {
  "method": "GET",
  "path": "/availability",
  "contract": "catalogue",
  "summary": "Live remaining capacity",
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
    "name": "channelCapacityId",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": null
 },
 "getBundle": {
  "method": "GET",
  "path": "/bundles/{bundleId}",
  "contract": "promotions",
  "summary": "Read a bundle with components and allocation",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "Bundle"
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
 "getMyChallenges": {
  "method": "GET",
  "path": "/guests/me/challenges",
  "contract": "marketing-crm",
  "summary": "Active challenges and how far along I am",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ChallengeProgress"
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
 "getUpsellSuggestions": {
  "method": "POST",
  "path": "/upsell-suggestions",
  "contract": "promotions",
  "summary": "Suggestions for a cart",
  "permission": "PRODUCT_VIEW",
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
 "listCatalogueBundles": {
  "method": "GET",
  "path": "/catalogue/bundles",
  "contract": "catalogue",
  "summary": "List published bundles",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "BundleSummary"
 },
 "listPerformances": {
  "method": "GET",
  "path": "/events/{eventId}/performances",
  "contract": "catalogue",
  "summary": "List performances of an event",
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
    "name": "to",
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
 "recommendSeats": {
  "method": "POST",
  "path": "/performances/{performanceId}/seat-recommendations",
  "contract": "seating",
  "summary": "Recommend seats for a party",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "SeatRecommendationRequest",
  "responds": null
 },
 "respondToInvitation": {
  "method": "POST",
  "path": "/invitations/{token}/respond",
  "contract": "marketing-crm",
  "summary": "Accept or decline",
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
  "responds": "Invitation"
 },
 "shareEntitlement": {
  "method": "POST",
  "path": "/entitlements/{entitlementId}/share",
  "contract": "orders",
  "summary": "Let somebody else use this, without giving it away",
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
  "responds": "Problem"
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
 "Bundle": {
  "x-ticvai-persistence": "promotions.bundle + promotions.bundle_component",
  "allOf": [
   {
    "$ref": "#/components/schemas/CreateBundleRequest"
   },
   {
    "type": "object",
    "required": [
     "id",
     "savingsAmount",
     "isActive",
     "hasBeenSold"
    ],
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid"
     },
     "savingsAmount": {
      "allOf": [
       {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      ],
      "description": "Sum of component list prices less the bundle price."
     },
     "savingsPercentage": {
      "type": "number"
     },
     "hasBeenSold": {
      "type": "boolean",
      "description": "True locks components and allocation against amendment."
     },
     "isActive": {
      "type": "boolean"
     }
    }
   }
  ]
 },
 "BundleSummary": {
  "x-ticvai-persistence": "none — projection over bundle",
  "type": "object",
  "required": [
   "version",
   "venueId",
   "publishedAt",
   "publishedBy",
   "contentHash",
   "staleAfter",
   "sizeBytes"
  ],
  "properties": {
   "version": {
    "type": "string"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "publishedAt": {
    "type": "string",
    "format": "date-time"
   },
   "publishedBy": {
    "type": "string",
    "format": "uuid"
   },
   "contentHash": {
    "type": "string"
   },
   "signatureKeyId": {
    "type": "string",
    "description": "Key that signed this bundle. A terminal offline across a key rotation needs a grace window, or it cannot verify the next bundle.\n"
   },
   "staleAfter": {
    "type": "string",
    "format": "date-time"
   },
   "sizeBytes": {
    "type": "integer"
   },
   "note": {
    "type": "string"
   },
   "appliedByWorkstations": {
    "type": "integer"
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
 "ChallengeProgress": {
  "type": "object",
  "x-ticvai-persistence": "marketing.challenge_progress",
  "description": "22.6.15. **Progress is shown, not just the outcome.** A guest two visits from a reward behaves differently from one who does not know how close they are, which is the entire mechanism.\n",
  "required": [
   "id",
   "challengeId",
   "subjectId",
   "current",
   "target"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "challengeId": {
    "type": "string",
    "format": "uuid"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "portfolioId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "For a family or group challenge — where the shared progress accrues."
   },
   "current": {
    "type": "number"
   },
   "target": {
    "type": "number"
   },
   "streakCount": {
    "type": "integer",
    "nullable": true
   },
   "completedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "rewardIssuedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "CreateBundleRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "code",
   "name",
   "venueId",
   "kind",
   "price",
   "components",
   "allocation"
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
   "description": {
    "type": "string",
    "maxLength": 1000
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "$ref": "#/components/schemas/BundleKind"
   },
   "price": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "components": {
    "type": "array",
    "minItems": 0,
    "items": {
     "$ref": "#/components/schemas/BundleComponent"
    }
   },
   "choiceGroups": {
    "type": "array",
    "description": "Dynamic bundles (3.5.10). A bundle may carry fixed components and choice groups at once — a family pass with fixed parking and two groups the guest chooses from. **The bundle price does not move with the choice** (ADR-0019).\n",
    "items": {
     "$ref": "#/components/schemas/BundleChoiceGroup"
    }
   },
   "allocation": {
    "type": "object",
    "required": [
     "method",
     "components"
    ],
    "properties": {
     "method": {
      "$ref": "#/components/schemas/AllocationMethod"
     },
     "components": {
      "type": "array",
      "items": {
       "$ref": "#/components/schemas/AllocationComponent"
      }
     }
    }
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
 "CreateSeatHoldRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "id",
   "performanceId",
   "seatIds",
   "ttlSeconds"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "performanceId": {
    "type": "string",
    "format": "uuid"
   },
   "seatIds": {
    "type": "array",
    "minItems": 1,
    "maxItems": 50,
    "items": {
     "type": "string"
    }
   },
   "ttlSeconds": {
    "type": "integer",
    "minimum": 60,
    "maximum": 1800
   },
   "subjectId": {
    "type": "string",
    "format": "uuid"
   }
  }
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
 "Invitation": {
  "type": "object",
  "x-ticvai-persistence": "marketing.invitation",
  "description": "**Addressed and tokenised.** A guest accepting an invitation is claiming a specific place, not buying one.\n",
  "required": [
   "id",
   "campaignId",
   "token",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "campaignId": {
    "type": "string",
    "format": "uuid"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "recipientEmail": {
    "type": "string",
    "format": "email",
    "nullable": true
   },
   "token": {
    "type": "string",
    "description": "**Single-use and unguessable.** An invitation link forwarded to a group chat is the failure mode, and a token that survives its first use is one that ends up there.\n"
   },
   "plusOnes": {
    "type": "integer",
    "default": 0
   },
   "status": {
    "type": "string",
    "enum": [
     "issued",
     "viewed",
     "accepted",
     "declined",
     "expired",
     "revoked"
    ]
   },
   "entitlementIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "respondedAt": {
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
 "Problem": {
  "type": "object",
  "description": "RFC 9457 problem details. Every error response uses this shape.",
  "required": [
   "type",
   "title",
   "status"
  ],
  "properties": {
   "type": {
    "type": "string",
    "format": "uri"
   },
   "title": {
    "type": "string"
   },
   "status": {
    "type": "integer"
   },
   "detail": {
    "type": "string"
   },
   "instance": {
    "type": "string"
   },
   "traceId": {
    "type": "string"
   },
   "errors": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "field",
      "code"
     ],
     "properties": {
      "field": {
       "type": "string"
      },
      "code": {
       "type": "string"
      },
      "message": {
       "type": "string"
      }
     }
    }
   }
  }
 },
 "Referral": {
  "type": "object",
  "x-ticvai-persistence": "marketing.referral",
  "description": "BL-034. **No referrer, no reward, nothing anywhere.**\n**The reward fires on the referee's qualifying act, not on the sign-up**, because a referral that pays on registration pays for accounts rather than for guests.\n",
  "required": [
   "id",
   "referrerSubjectId",
   "code",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "referrerSubjectId": {
    "type": "string",
    "format": "uuid"
   },
   "refereeSubjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "code": {
    "type": "string"
   },
   "status": {
    "type": "string",
    "enum": [
     "issued",
     "registered",
     "qualified",
     "rewarded",
     "expired",
     "void"
    ]
   },
   "qualifyingAction": {
    "type": "string",
    "enum": [
     "firstPurchase",
     "firstVisit",
     "membershipPurchase"
    ]
   },
   "referrerRewardId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "refereeRewardId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "expiresAt": {
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
 "SeatAvailability": {
  "x-ticvai-persistence": "none — computed from seat, hold and block",
  "type": "object",
  "required": [
   "performanceId",
   "seatMapId",
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
      }
     }
    }
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
 "SeatRecommendationRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "partySize",
   "strategy"
  ],
  "properties": {
   "partySize": {
    "type": "integer",
    "minimum": 1,
    "maximum": 50
   },
   "strategy": {
    "$ref": "#/components/schemas/SeatRecommendationStrategy"
   },
   "categoryIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "maxPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "accessibleCount": {
    "type": "integer",
    "default": 0,
    "description": "Wheelchair spaces in the party. Companions are added automatically."
   },
   "maxOptions": {
    "type": "integer",
    "default": 3,
    "maximum": 10
   }
  }
 },
 "SeatRecommendationStrategy": {
  "type": "string",
  "enum": [
   "bestAvailable",
   "bestValue",
   "closestToStage",
   "accessible",
   "contiguous"
  ]
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
 }
}
```
