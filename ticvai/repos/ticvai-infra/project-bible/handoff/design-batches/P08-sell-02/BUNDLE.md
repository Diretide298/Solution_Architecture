# P08-sell-02 — P08 · Sell (2 of 4)

**10 screens · 42 operations · 56 schemas · 15 permissions**

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

- **Every control that can be refused must be gated.** 15 permissions apply here:
  `ACCESS_VALIDATE, AI_USE, CAPACITY_CONFIGURE, EVENT_CONFIGURE, ORDER_CREATE, ORDER_VIEW, PERFORMANCE_CONFIGURE, PRODUCT_CONFIGURE, PRODUCT_VIEW, REGION_CONFIGURE, SCOPE_VIEW, TENANT_CONFIGURE`…. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-018` | Allocation & Holds | listDetail | 5 | 4 | — |
| `BO-019` | Closures & Blackouts | listDetail | 12 | 7 | — |
| `BO-037` | Offline Package Status | listDetail | 9 | 4 | — |
| `BO-063` | Opening Hours & Calendar | listDetail | 13 | 7 | — |
| `BO-102` | Sell | listDetail | 4 | 0 | — |
| `BO-109` | Menu Builder & POS Layout Designer | listDetail | 3 | 2 | — |
| `BO-110` | Recipe & BOM Management | listDetail | 2 | 1 | — |
| `BO-111` | Ingredient Substitution, Allergen & Nutrition | configEditor | 5 | 2 | — |
| `BO-112` | Production Planning & Production Sheets | configEditor | 1 | 0 | — |
| `BO-113` | Central Kitchen & Commissary Management | configEditor | 2 | 1 | — |

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-018",
  "name": "Allocation & Holds",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/allocation-holds",
   "component": "apps/venue-management-web/src/routes/venue-operations/AllocationHoldsDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-007",
    "BO-009"
   ],
   "inferred": true,
   "entryFrom": [
    "BO-102"
   ],
   "transitions": [
    {
     "to": "BO-007",
     "trigger": "Product Directory",
     "provenance": "derived — BO-007 declares entryState.params productId and BO-018 holds none of them. The edge carries nothing: productId only pre-selects (deep link or optional), and BO-007 opens on its own"
    },
    {
     "to": "BO-009",
     "trigger": "Pricing Rules",
     "provenance": "derived — BO-009 declares entryState.params priceListId, ruleId and BO-018 holds none of them. The edge carries nothing: priceListId only pre-selects (deep link or optional); BO-009 finds ruleId (listDynamicPriceRules) itself, and BO-009 opens on its own"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listInventoryHolds` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "See who is holding capacity, and release it.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Channel capacity id",
       "operation": "listInventoryHolds",
       "notes": "Sends `?channelCapacityId=` to `listInventoryHolds`.",
       "provenance": "contract catalogue.yaml GET /inventory-holds"
      },
      {
       "kind": "textField",
       "label": "Holder workstation id",
       "operation": "listInventoryHolds",
       "notes": "Sends `?holderWorkstationId=` to `listInventoryHolds`.",
       "provenance": "contract catalogue.yaml GET /inventory-holds"
      },
      {
       "kind": "textField",
       "label": "Status",
       "operation": "listInventoryHolds",
       "notes": "Sends `?status=` to `listInventoryHolds`.",
       "provenance": "contract catalogue.yaml GET /inventory-holds"
      },
      {
       "kind": "dataTable",
       "label": "Every inventory hold",
       "bindsTo": "InventoryHold",
       "columns": [
        "InventoryHold.id",
        "InventoryHold.channelCapacityId",
        "InventoryHold.holderWorkstationId",
        "InventoryHold.parentLeaseId",
        "InventoryHold.requestedUnits",
        "InventoryHold.channel",
        "InventoryHold.grantedUnits",
        "InventoryHold.consumedUnits",
        "InventoryHold.status",
        "InventoryHold.acquiredAt",
        "InventoryHold.expiresAt",
        "InventoryHold.releasedAt"
       ],
       "operation": "listInventoryHolds",
       "provenance": "contract catalogue.yaml GET /inventory-holds"
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
       "label": "The selected inventory hold",
       "bindsTo": "InventoryHold",
       "columns": [
        "InventoryHold.id",
        "InventoryHold.channelCapacityId",
        "InventoryHold.holderWorkstationId",
        "InventoryHold.parentLeaseId",
        "InventoryHold.requestedUnits",
        "InventoryHold.channel",
        "InventoryHold.grantedUnits",
        "InventoryHold.consumedUnits",
        "InventoryHold.status",
        "InventoryHold.acquiredAt",
        "InventoryHold.expiresAt",
        "InventoryHold.releasedAt",
        "InventoryHold.forceReleasedByPrincipalId",
        "InventoryHold.forceReleaseReason"
       ],
       "operation": "listInventoryHolds",
       "provenance": "contract catalogue.yaml GET /inventory-holds"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Acquire inventory hold",
       "operation": "acquireInventoryHold",
       "provenance": "contract catalogue.yaml POST /inventory-holds"
      },
      {
       "kind": "destructiveButton",
       "label": "Force release inventory hold",
       "operation": "forceReleaseInventoryHold",
       "provenance": "contract catalogue.yaml POST /inventory-holds/{inventoryHoldId}/force-release"
      },
      {
       "kind": "secondaryButton",
       "label": "Release inventory hold",
       "operation": "relinquishInventoryHold",
       "provenance": "contract catalogue.yaml DELETE /inventory-holds/{inventoryHoldId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Renew inventory hold",
       "operation": "renewInventoryHold",
       "provenance": "contract catalogue.yaml POST /inventory-holds/{inventoryHoldId}/renew"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmForceReleaseInventoryHold",
    "component": "confirmDialog",
    "trigger": "Force release inventory hold",
    "body": "**Names what `forceReleaseInventoryHold` changes and what it leaves alone**, in the consequence rather than the verb. A allocation holds this affects should be identified in the dialog, not just counted. **Collects what `forceReleaseInventoryHold` sends before it is called.** Required: `reason`.",
    "provenance": "contract catalogue.yaml POST /inventory-holds/{inventoryHoldId}/force-release"
   },
   {
    "id": "formAcquireInventoryHold",
    "component": "modal",
    "trigger": "Acquire inventory hold",
    "body": "**Collects what `acquireInventoryHold` sends before it is called.** Required: `id`, `channelCapacityId`, `requestedUnits`, `ttlSeconds`. Optional: `channel`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "AcquireLeaseRequest",
    "confirm": {
     "label": "Acquire inventory hold",
     "operation": "acquireInventoryHold"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "channelCapacityId",
      "requestedUnits",
      "ttlSeconds",
      "channel"
     ]
    },
    "provenance": "contract catalogue.yaml POST /inventory-holds"
   },
   {
    "id": "formRelinquishInventoryHold",
    "component": "modal",
    "trigger": "Release inventory hold",
    "body": "**Collects what `relinquishInventoryHold` sends before it is called.** Required: `consumedUnits`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Release inventory hold",
     "operation": "relinquishInventoryHold"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "consumedUnits"
     ]
    },
    "provenance": "contract catalogue.yaml DELETE /inventory-holds/{inventoryHoldId}"
   },
   {
    "id": "formRenewInventoryHold",
    "component": "modal",
    "trigger": "Renew inventory hold",
    "body": "**Collects what `renewInventoryHold` sends before it is called.** Required: `consumedUnits`. Optional: `additionalUnits`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Renew inventory hold",
     "operation": "renewInventoryHold"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "consumedUnits",
      "additionalUnits"
     ]
    },
    "provenance": "contract catalogue.yaml POST /inventory-holds/{inventoryHoldId}/renew"
   }
  ],
  "states": {
   "loading": "The allocation holds list.",
   "error": "Could not load. Names which read failed and leaves the allocation holds untouched.",
   "emptyFirstRun": "No allocation holds yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on channelCapacityId, holderWorkstationId, status and the allocation holds are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `PRODUCT_VIEW`, which `listInventoryHolds` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listInventoryHolds",
    "contract": "catalogue",
    "purpose": "List leases",
    "trigger": "onLoad"
   },
   {
    "operationId": "acquireInventoryHold",
    "contract": "catalogue",
    "purpose": "Acquire an inventory lease",
    "trigger": "onAction",
    "invalidates": [
     "listInventoryHolds"
    ]
   },
   {
    "operationId": "forceReleaseInventoryHold",
    "contract": "catalogue",
    "purpose": "Reclaim a stranded lease",
    "trigger": "onAction",
    "invalidates": [
     "listInventoryHolds"
    ]
   },
   {
    "operationId": "relinquishInventoryHold",
    "contract": "catalogue",
    "purpose": "Return unsold units",
    "trigger": "onAction",
    "invalidates": [
     "listInventoryHolds"
    ]
   },
   {
    "operationId": "renewInventoryHold",
    "contract": "catalogue",
    "purpose": "Extend a lease TTL",
    "trigger": "onAction",
    "invalidates": [
     "listInventoryHolds"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "inventoryHoldId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `inventoryHoldId`.",
   "preloaded": [
    "InventoryHold.id",
    "InventoryHold.channelCapacityId",
    "InventoryHold.holderWorkstationId",
    "InventoryHold.parentLeaseId",
    "InventoryHold.requestedUnits"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-018"
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
  "id": "BO-019",
  "name": "Closures & Blackouts",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/closures-blackouts",
   "component": "apps/venue-management-web/src/routes/venue-operations/ClosuresBlackoutsDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-001",
    "BO-007",
    "BO-009"
   ],
   "inferred": true,
   "entryFrom": [
    "BO-102"
   ],
   "transitions": [
    {
     "to": "BO-001",
     "trigger": "Queue Directory",
     "carries": [
      "eventId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId and BO-019 holds eventId, so an edge into it carries them"
    },
    {
     "to": "BO-007",
     "trigger": "Product Directory",
     "provenance": "derived — BO-007 declares entryState.params productId and BO-019 holds none of them. The edge carries nothing: productId only pre-selects (deep link or optional), and BO-007 opens on its own"
    },
    {
     "to": "BO-009",
     "trigger": "Pricing Rules",
     "provenance": "derived — BO-009 declares entryState.params priceListId, ruleId and BO-019 holds none of them. The edge carries nothing: priceListId only pre-selects (deep link or optional); BO-009 finds ruleId (listDynamicPriceRules) itself, and BO-009 opens on its own"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Drawn 26 August** — `Seat Board 2.dc.html` frame `seat-2d`. **The frame names this screen on its own face**, which is the first pack to do that: the earlier F&B, POS and Retail boards had to be hand-assigned by purpose after three derivation attempts produced nonsense. **A board that says what it draws removes the guess entirely.**",
  "density": "compact",
  "boardFrames": [
   "Seat Board 2.dc.html#seat-2d"
  ],
  "pattern": "listDetail",
  "patternReason": "`listPerformances` reads the population and `getEvent` reads one of them — list, select, act",
  "purpose": "Stop selling something, for a reason.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "datePicker",
       "label": "From",
       "operation": "listPerformances",
       "notes": "Sends `?from=` to `listPerformances`.",
       "provenance": "contract catalogue.yaml GET /events/{eventId}/performances"
      },
      {
       "kind": "datePicker",
       "label": "To",
       "operation": "listPerformances",
       "notes": "Sends `?to=` to `listPerformances`.",
       "provenance": "contract catalogue.yaml GET /events/{eventId}/performances"
      },
      {
       "kind": "dataTable",
       "label": "Every performance",
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
      },
      {
       "kind": "dataTable",
       "label": "Every event",
       "bindsTo": "Event",
       "columns": [
        "Event.id",
        "Event.code",
        "Event.name",
        "Event.venueId",
        "Event.scopePath",
        "Event.parentEventId",
        "Event.performanceCount",
        "Event.isActive"
       ],
       "operation": "listEvents",
       "provenance": "contract catalogue.yaml GET /events"
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
       "label": "The selected performance",
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
       "operation": "getPerformance",
       "provenance": "contract catalogue.yaml GET /performances/{performanceId}"
      },
      {
       "kind": "detailPanel",
       "label": "The seat availability",
       "bindsTo": "SeatAvailability",
       "columns": [
        "SeatAvailability.performanceId",
        "SeatAvailability.seatMapId",
        "SeatAvailability.renderMode",
        "SeatAvailability.totals",
        "SeatAvailability.byCategory",
        "SeatAvailability.seats"
       ],
       "operation": "getSeatAvailability",
       "provenance": "contract seating.yaml GET /performances/{performanceId}/seat-availability"
      },
      {
       "kind": "detailPanel",
       "label": "The event",
       "bindsTo": "Event",
       "columns": [
        "Event.id",
        "Event.code",
        "Event.name",
        "Event.venueId",
        "Event.scopePath",
        "Event.parentEventId",
        "Event.performanceCount",
        "Event.isActive"
       ],
       "operation": "getEvent",
       "provenance": "contract catalogue.yaml GET /events/{eventId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "destructiveButton",
       "label": "Cancel performance",
       "operation": "cancelPerformance",
       "provenance": "contract catalogue.yaml POST /performances/{performanceId}/cancel"
      },
      {
       "kind": "secondaryButton",
       "label": "Create event",
       "operation": "createEvent",
       "provenance": "contract catalogue.yaml POST /events"
      },
      {
       "kind": "secondaryButton",
       "label": "Create performances",
       "operation": "createPerformances",
       "provenance": "contract catalogue.yaml POST /events/{eventId}/performances"
      },
      {
       "kind": "secondaryButton",
       "label": "Recommend seats",
       "operation": "recommendSeats",
       "provenance": "contract seating.yaml POST /performances/{performanceId}/seat-recommendations"
      },
      {
       "kind": "secondaryButton",
       "label": "Save event",
       "operation": "updateEvent",
       "provenance": "contract catalogue.yaml PATCH /events/{eventId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Save performance",
       "operation": "updatePerformance",
       "provenance": "contract catalogue.yaml PATCH /performances/{performanceId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Save path closure",
       "operation": "setPathClosure",
       "provenance": "contract venue-map.yaml POST /venue-maps/{mapId}/paths/{pathId}/closure"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmCancelPerformance",
    "component": "confirmDialog",
    "trigger": "Cancel performance",
    "body": "**Names what `cancelPerformance` changes and what it leaves alone**, in the consequence rather than the verb. A closures blackouts this affects should be identified in the dialog, not just counted. **Collects what `cancelPerformance` sends before it is called.** Required: `reason`. Optional: `guestMessage`, `refundPercentage`, `offerAlternativePerformanceId`, `dryRun`. **A real run needs a supervisor PIN on this device** (`supervisorStepUp` {principalId, credential}); a dry run does not (decided 28 September, audit R144).",
    "provenance": "contract catalogue.yaml POST /performances/{performanceId}/cancel"
   },
   {
    "id": "formCreateEvent",
    "component": "modal",
    "trigger": "Create event",
    "body": "**Collects what `createEvent` sends before it is called.** Required: `code`, `name`, `venueId`. Optional: `parentEventId`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateEventRequest",
    "confirm": {
     "label": "Create event",
     "operation": "createEvent"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "code",
      "name",
      "venueId",
      "parentEventId"
     ]
    },
    "provenance": "contract catalogue.yaml POST /events"
   },
   {
    "id": "formCreatePerformances",
    "component": "modal",
    "trigger": "Create performances",
    "body": "**Collects what `createPerformances` sends before it is called.** Required: `startsAt`, `endsAt`. Optional: `admissionRulesId`, `seatMapId`, `recurrence`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreatePerformancesRequest",
    "confirm": {
     "label": "Create performances",
     "operation": "createPerformances"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "startsAt",
      "endsAt",
      "admissionRulesId",
      "seatMapId",
      "recurrence"
     ]
    },
    "provenance": "contract catalogue.yaml POST /events/{eventId}/performances"
   },
   {
    "id": "formRecommendSeats",
    "component": "modal",
    "trigger": "Recommend seats",
    "body": "**Collects what `recommendSeats` sends before it is called.** Required: `partySize`, `strategy`. Optional: `categoryIds`, `maxPrice`, `accessibleCount`, `maxOptions`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "SeatRecommendationRequest",
    "confirm": {
     "label": "Recommend seats",
     "operation": "recommendSeats"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "partySize",
      "strategy",
      "categoryIds",
      "maxPrice",
      "accessibleCount",
      "maxOptions"
     ]
    },
    "provenance": "contract seating.yaml POST /performances/{performanceId}/seat-recommendations"
   },
   {
    "id": "formUpdateEvent",
    "component": "modal",
    "trigger": "Save event",
    "body": "**Collects what `updateEvent` sends before it is called.** Nothing in the body is required. Optional: `name`, `parentEventId`, `isActive`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save event",
     "operation": "updateEvent"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "name",
      "parentEventId",
      "isActive"
     ]
    },
    "provenance": "contract catalogue.yaml PATCH /events/{eventId}"
   },
   {
    "id": "formUpdatePerformance",
    "component": "modal",
    "trigger": "Save performance",
    "body": "**Collects what `updatePerformance` sends before it is called.** Nothing in the body is required. Optional: `startsAt`, `endsAt`, `status`, `admissionRulesId`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save performance",
     "operation": "updatePerformance"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "startsAt",
      "endsAt",
      "status",
      "admissionRulesId"
     ]
    },
    "provenance": "contract catalogue.yaml PATCH /performances/{performanceId}"
   },
   {
    "id": "formSetPathClosure",
    "component": "modal",
    "trigger": "Save path closure",
    "body": "**Collects what `setPathClosure` sends before it is called.** Required: `isClosed`. Optional: `reason` (maintenance, incident, event, weather, crowding, other), `note`, `force`, `expectedReopenAt`. **Choosing Other makes the note required** — the form will not confirm without it and the server refuses 400 (decided 28 September, audit R222). Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save path closure",
     "operation": "setPathClosure"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "isClosed",
      "reason",
      "note",
      "force",
      "expectedReopenAt"
     ]
    },
    "provenance": "contract venue-map.yaml POST /venue-maps/{mapId}/paths/{pathId}/closure"
   }
  ],
  "states": {
   "loading": "The closures blackouts list.",
   "error": "Could not load. Names which read failed and leaves the closures blackouts untouched.",
   "emptyFirstRun": "No closures blackouts yet. Offers Create event (`createEvent`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on from, to and the closures blackouts are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `PRODUCT_VIEW`, which `listPerformances` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPerformances",
    "contract": "catalogue",
    "purpose": "List performances of an event",
    "trigger": "onAction"
   },
   {
    "operationId": "cancelPerformance",
    "contract": "catalogue",
    "purpose": "Cancel a performance",
    "trigger": "onAction",
    "invalidates": [
     "listPerformances"
    ]
   },
   {
    "operationId": "createEvent",
    "contract": "catalogue",
    "purpose": "Create an event",
    "trigger": "onAction",
    "invalidates": [
     "listPerformances"
    ]
   },
   {
    "operationId": "createPerformances",
    "contract": "catalogue",
    "purpose": "Create performances, singly or by schedule",
    "trigger": "onAction",
    "invalidates": [
     "listPerformances"
    ]
   },
   {
    "operationId": "getEvent",
    "contract": "catalogue",
    "purpose": "Read an event",
    "trigger": "onAction"
   },
   {
    "operationId": "getPerformance",
    "contract": "catalogue",
    "purpose": "Read a performance",
    "trigger": "onLoad"
   },
   {
    "operationId": "getSeatAvailability",
    "contract": "seating",
    "purpose": "Seat status for a performance",
    "trigger": "onLoad"
   },
   {
    "operationId": "listEvents",
    "contract": "catalogue",
    "purpose": "List events",
    "trigger": "onLoad"
   },
   {
    "operationId": "recommendSeats",
    "contract": "seating",
    "purpose": "Recommend seats for a party",
    "trigger": "onAction",
    "invalidates": [
     "listPerformances"
    ]
   },
   {
    "operationId": "updateEvent",
    "contract": "catalogue",
    "purpose": "Amend an event",
    "trigger": "onAction",
    "invalidates": [
     "listPerformances"
    ]
   },
   {
    "operationId": "updatePerformance",
    "contract": "catalogue",
    "purpose": "Amend a performance",
    "trigger": "onAction",
    "invalidates": [
     "listPerformances"
    ]
   },
   {
    "operationId": "setPathClosure",
    "contract": "venue-map",
    "purpose": "Close a path or an area",
    "trigger": "onAction",
    "invalidates": [
     "listPerformances"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "eventId",
     "from": "deepLink"
    },
    {
     "name": "performanceId",
     "from": "deepLink"
    },
    {
     "name": "mapId",
     "from": "navigation"
    },
    {
     "name": "pathId",
     "from": "navigation"
    }
   ],
   "coldEntry": "**A link to a performance that has happened.** Offers the next performance of the same event.",
   "preloaded": [
    "Performance.id",
    "Performance.eventId",
    "Performance.startsAt",
    "Performance.endsAt",
    "Performance.approvalRequestId"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-019",
   "derivedFrom": "wireframes/reference/Seat Board 2.dc.html",
   "note": "**Drawn by Claude Design on `Seat Board 2.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 12 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "BO-037",
  "name": "Offline Package Status",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/offline-package-status",
   "component": "apps/venue-management-web/src/routes/venue-operations/OfflinePackageStatusDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-007",
    "BO-009",
    "BO-128"
   ],
   "inferred": true,
   "entryFrom": [
    "BO-102",
    "BO-128",
    "BO-129"
   ],
   "transitions": [
    {
     "to": "BO-007",
     "trigger": "Product Directory",
     "provenance": "derived — BO-007 declares entryState.params productId and BO-037 holds none of them. The edge carries nothing: productId only pre-selects (deep link or optional), and BO-007 opens on its own"
    },
    {
     "to": "BO-009",
     "trigger": "Pricing Rules",
     "provenance": "derived — BO-009 declares entryState.params priceListId, ruleId and BO-037 holds none of them. The edge carries nothing: priceListId only pre-selects (deep link or optional); BO-009 finds ruleId (listDynamicPriceRules) itself, and BO-009 opens on its own"
    },
    {
     "to": "BO-128",
     "trigger": "The fleet is monitored",
     "provenance": "flow F89 step 3→4",
     "carries": [
      "workstationId"
     ]
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Improved 20 August against the client design board**, answering 2 board screen(s): Offline Operations Dashboard; Offline Product & Data Cache Management. **The id, flows and navigation are unchanged** — a board specifies a screen further; it does not replace it. **Owns POS board frame(s) POS-5A, POS-5C** (client pack, 24 August). **Assigned by board purpose rather than by operation overlap** — three attempts at deriving that mapping produced plausible nonsense, and a reader who trusts a bad table is worse off than one who has none.",
  "density": "compact",
  "boardFrames": [
   "POS Board 5.dc.html#pos-5a",
   "POS Board 5.dc.html#pos-5c",
   "Retail Board 3.dc.html#ret-3j"
  ],
  "pattern": "listDetail",
  "patternReason": "`listCatalogueBundles` reads the population and `getLatestBundle` reads one of them — list, select, act",
  "purpose": "Know what each device is enforcing right now.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every bundle",
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
      },
      {
       "kind": "dataTable",
       "label": "Every sync rejection",
       "bindsTo": "SyncRejection",
       "columns": [
        "SyncRejection.id",
        "SyncRejection.workstationId",
        "SyncRejection.kind",
        "SyncRejection.recordedAt",
        "SyncRejection.rejectedAt",
        "SyncRejection.problem",
        "SyncRejection.payload",
        "SyncRejection.resolvedAt",
        "SyncRejection.resolvedByPrincipalId",
        "SyncRejection.resolution",
        "SyncRejection.resolvedRecordId"
       ],
       "operation": "listSyncRejections",
       "provenance": "contract orders.yaml GET /sync/rejections"
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
       "kind": "publishGate",
       "impliedBy": "publishBundle",
       "notes": "Declares `publishBundle`. **The gate names what the publish will affect before it happens** — a disabled Publish with no reason is the state operators escalate.\n",
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
       "label": "The selected bundle",
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
      },
      {
       "kind": "detailPanel",
       "label": "The offline package",
       "bindsTo": "OfflinePackage",
       "columns": [
        "OfflinePackage.generatedAt",
        "OfflinePackage.validFrom",
        "OfflinePackage.validTo",
        "OfflinePackage.accessPointId",
        "OfflinePackage.entitlements",
        "OfflinePackage.delegatedRights",
        "OfflinePackage.blacklist",
        "OfflinePackage.admissionRules"
       ],
       "operation": "getOfflinePackage",
       "provenance": "contract access.yaml GET /access/offline-package"
      },
      {
       "kind": "detailPanel",
       "label": "The catalogue bundle",
       "bindsTo": "CatalogueBundle",
       "columns": [
        "CatalogueBundle.venueId",
        "CatalogueBundle.isDelta",
        "CatalogueBundle.baseVersion",
        "CatalogueBundle.signature",
        "CatalogueBundle.signatureKeyId",
        "CatalogueBundle.contentHash",
        "CatalogueBundle.staleAfter",
        "CatalogueBundle.payload"
       ],
       "operation": "getLatestBundle",
       "provenance": "contract catalogue.yaml GET /catalogue/bundles/latest"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Publish bundle",
       "operation": "publishBundle",
       "provenance": "contract catalogue.yaml POST /catalogue/bundles"
      },
      {
       "kind": "secondaryButton",
       "label": "Report bundle applied",
       "operation": "reportBundleApplied",
       "provenance": "contract catalogue.yaml POST /catalogue/bundles/{version}/applied"
      },
      {
       "kind": "secondaryButton",
       "label": "Save offline policy",
       "operation": "setOfflinePolicy",
       "provenance": "contract tenancy.yaml PUT /offline-policy"
      },
      {
       "kind": "secondaryButton",
       "label": "Sync orders",
       "operation": "syncOrders",
       "provenance": "contract orders.yaml POST /sync/orders"
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
   "loading": "The offline package status list.",
   "error": "Could not load. Names which read failed and leaves the offline package status untouched.",
   "emptyFirstRun": "No offline package status yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Never shown: `listCatalogueBundles` takes no filter, so an empty list is always the first-run state above.",
   "emptyNoAccess": "Shown when the caller lacks `PRODUCT_VIEW`, which `listCatalogueBundles` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCatalogueBundles",
    "contract": "catalogue",
    "purpose": "List published bundles",
    "trigger": "onLoad"
   },
   {
    "operationId": "getLatestBundle",
    "contract": "catalogue",
    "purpose": "Pull the current bundle for this workstation's venue",
    "trigger": "onLoad"
   },
   {
    "operationId": "publishBundle",
    "contract": "catalogue",
    "purpose": "Compute, sign and publish a catalogue bundle",
    "trigger": "onAction",
    "invalidates": [
     "listCatalogueBundles"
    ]
   },
   {
    "operationId": "reportBundleApplied",
    "contract": "catalogue",
    "purpose": "Report that a workstation applied a bundle",
    "trigger": "onAction",
    "invalidates": [
     "listCatalogueBundles"
    ]
   },
   {
    "operationId": "getOfflinePackage",
    "contract": "access",
    "purpose": "Entitlement and rule set for offline validation",
    "trigger": "onLoad"
   },
   {
    "operationId": "listSyncRejections",
    "contract": "orders",
    "purpose": "Entries the server refused",
    "trigger": "onLoad"
   },
   {
    "operationId": "listWorkstations",
    "contract": "tenancy",
    "purpose": "List workstations",
    "trigger": "onLoad"
   },
   {
    "operationId": "setOfflinePolicy",
    "contract": "tenancy",
    "purpose": "setOfflinePolicy",
    "trigger": "onAction",
    "invalidates": [
     "listCatalogueBundles"
    ]
   },
   {
    "operationId": "syncOrders",
    "contract": "orders",
    "purpose": "Replay orders recorded offline",
    "trigger": "onAction",
    "invalidates": [
     "listCatalogueBundles"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "version",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A version link is expected to point at something superseded — that is what versions are for.** The screen opens the requested version read-only, says it is not current, and links to the one that is. **An old version is history, not an error.** Arrives with `version`.",
   "preloaded": [
    "BundleSummary.venueId",
    "BundleSummary.publishedAt",
    "BundleSummary.publishedBy",
    "BundleSummary.contentHash",
    "BundleSummary.signatureKeyId"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-037",
   "derivedFrom": "wireframes/reference/POS Board 5.dc.html",
   "source": "Claude Design POS pack, 24 August",
   "note": "**Drawn by Claude Design on `POS Board 5.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 9 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formPublishBundle",
    "component": "modal",
    "trigger": "Publish bundle",
    "body": "**Collects what `publishBundle` sends before it is called.** Required: `venueId`. Optional: `note`, `staleAfterHours`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Publish bundle",
     "operation": "publishBundle"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "venueId",
      "note",
      "staleAfterHours"
     ]
    },
    "provenance": "contract catalogue.yaml POST /catalogue/bundles"
   },
   {
    "id": "formReportBundleApplied",
    "component": "modal",
    "trigger": "Report bundle applied",
    "body": "**Collects what `reportBundleApplied` sends before it is called.** Required: `appliedAt`, `outcome`. Optional: `error`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Report bundle applied",
     "operation": "reportBundleApplied"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "appliedAt",
      "outcome",
      "error"
     ]
    },
    "provenance": "contract catalogue.yaml POST /catalogue/bundles/{version}/applied"
   },
   {
    "id": "formSetOfflinePolicy",
    "component": "modal",
    "trigger": "Save offline policy",
    "body": "**Collects what `setOfflinePolicy` sends before it is called.** Required: `scopePath`. Optional: `id`, `maxOfflineHours`, `allowedOffline`, `offlineValueCeiling`, `offlineTransactionCeiling`, `onCeilingBreach`, `requiresManagerToExtend`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "OfflinePolicy",
    "confirm": {
     "label": "Save offline policy",
     "operation": "setOfflinePolicy"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "scopePath",
      "id",
      "maxOfflineHours",
      "allowedOffline",
      "offlineValueCeiling",
      "offlineTransactionCeiling",
      "onCeilingBreach",
      "requiresManagerToExtend"
     ]
    },
    "provenance": "contract tenancy.yaml PUT /offline-policy"
   },
   {
    "id": "formSyncOrders",
    "component": "modal",
    "trigger": "Sync orders",
    "body": "**Collects what `syncOrders` sends before it is called.** Required: `deviceId`, `orders`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Sync orders",
     "operation": "syncOrders"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "deviceId",
      "orders"
     ]
    },
    "provenance": "contract orders.yaml POST /sync/orders"
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
  "id": "BO-063",
  "name": "Opening Hours & Calendar",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/opening-hours-calendar",
   "component": "apps/venue-management-web/src/routes/venue-operations/OpeningHoursCalendarDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-001",
    "BO-007",
    "BO-009"
   ],
   "inferred": true,
   "entryFrom": [
    "BO-102"
   ],
   "transitions": [
    {
     "to": "BO-001",
     "trigger": "Queue Directory",
     "carries": [
      "eventId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId and BO-063 holds eventId, so an edge into it carries them"
    },
    {
     "to": "BO-007",
     "trigger": "Product Directory",
     "provenance": "derived — BO-007 declares entryState.params productId and BO-063 holds none of them. The edge carries nothing: productId only pre-selects (deep link or optional), and BO-007 opens on its own"
    },
    {
     "to": "BO-009",
     "trigger": "Pricing Rules",
     "provenance": "derived — BO-009 declares entryState.params priceListId, ruleId and BO-063 holds none of them. The edge carries nothing: priceListId only pre-selects (deep link or optional); BO-009 finds ruleId (listDynamicPriceRules) itself, and BO-009 opens on its own"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Improved 20 August against the client design board**, answering 2 board screen(s): Operating Hours & Service Periods; Operating Hours & Sales Periods. **The id, flows and navigation are unchanged** — a board specifies a screen further; it does not replace it. **Drawn 26 August** — `Seat Board 1.dc.html` frame `seat-1c`. **The frame names this screen on its own face**, which is the first pack to do that: the earlier F&B, POS and Retail boards had to be hand-assigned by purpose after three derivation attempts produced nonsense. **A board that says what it draws removes the guess entirely.**",
  "density": "compact",
  "boardFrames": [
   "Seat Board 1.dc.html#seat-1c"
  ],
  "pattern": "listDetail",
  "patternReason": "`listPerformances` reads the population and `getPerformance` reads one of them — list, select, act",
  "purpose": "Say when the venue is open, including the exceptions.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "calendarView",
       "label": "Calendar",
       "operation": "listPerformances",
       "notes": "Opening days and performances placed in the venue calendar. Day, week, month and agenda views; the day starts at the venue's `calendarDayStartHour`. Sends the visible window as `from`/`to` and the category filter as `categoryId`.",
       "provenance": "decided 29 September 2026, 17 September minutes M17-03 (applied 30 September)"
      },
      {
       "kind": "datePicker",
       "label": "From",
       "operation": "listPerformances",
       "notes": "Sends `?from=` to `listPerformances`.",
       "provenance": "contract catalogue.yaml GET /events/{eventId}/performances"
      },
      {
       "kind": "datePicker",
       "label": "To",
       "operation": "listPerformances",
       "notes": "Sends `?to=` to `listPerformances`.",
       "provenance": "contract catalogue.yaml GET /events/{eventId}/performances"
      },
      {
       "kind": "dataTable",
       "label": "Every performance",
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
      },
      {
       "kind": "dataTable",
       "label": "Every event",
       "bindsTo": "Event",
       "columns": [
        "Event.id",
        "Event.code",
        "Event.name",
        "Event.venueId",
        "Event.scopePath",
        "Event.parentEventId",
        "Event.performanceCount",
        "Event.isActive"
       ],
       "operation": "listEvents",
       "provenance": "contract catalogue.yaml GET /events"
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
       "label": "The selected performance",
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
       "operation": "getPerformance",
       "provenance": "contract catalogue.yaml GET /performances/{performanceId}"
      },
      {
       "kind": "detailPanel",
       "label": "The event",
       "bindsTo": "Event",
       "columns": [
        "Event.id",
        "Event.code",
        "Event.name",
        "Event.venueId",
        "Event.scopePath",
        "Event.parentEventId",
        "Event.performanceCount",
        "Event.isActive"
       ],
       "operation": "getEvent",
       "provenance": "contract catalogue.yaml GET /events/{eventId}"
      },
      {
       "kind": "detailPanel",
       "label": "The seat availability",
       "bindsTo": "SeatAvailability",
       "columns": [
        "SeatAvailability.performanceId",
        "SeatAvailability.seatMapId",
        "SeatAvailability.renderMode",
        "SeatAvailability.totals",
        "SeatAvailability.byCategory",
        "SeatAvailability.seats"
       ],
       "operation": "getSeatAvailability",
       "provenance": "contract seating.yaml GET /performances/{performanceId}/seat-availability"
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
       "label": "Create performances",
       "operation": "createPerformances",
       "provenance": "contract catalogue.yaml POST /events/{eventId}/performances"
      },
      {
       "kind": "destructiveButton",
       "label": "Cancel performance",
       "operation": "cancelPerformance",
       "provenance": "contract catalogue.yaml POST /performances/{performanceId}/cancel"
      },
      {
       "kind": "secondaryButton",
       "label": "Create event",
       "operation": "createEvent",
       "provenance": "contract catalogue.yaml POST /events"
      },
      {
       "kind": "secondaryButton",
       "label": "Recommend seats",
       "operation": "recommendSeats",
       "provenance": "contract seating.yaml POST /performances/{performanceId}/seat-recommendations"
      },
      {
       "kind": "secondaryButton",
       "label": "Save event",
       "operation": "updateEvent",
       "provenance": "contract catalogue.yaml PATCH /events/{eventId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Save performance",
       "operation": "updatePerformance",
       "provenance": "contract catalogue.yaml PATCH /performances/{performanceId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Save outlet",
       "operation": "updateOutlet",
       "provenance": "contract tenancy.yaml PATCH /outlets/{outletId}"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmCancelPerformance",
    "component": "confirmDialog",
    "trigger": "Cancel performance",
    "body": "**Names what `cancelPerformance` changes and what it leaves alone**, in the consequence rather than the verb. A opening hours calendar this affects should be identified in the dialog, not just counted. **Collects what `cancelPerformance` sends before it is called.** Required: `reason`. Optional: `guestMessage`, `refundPercentage`, `offerAlternativePerformanceId`, `dryRun`. **A real run needs a supervisor PIN on this device** (`supervisorStepUp` {principalId, credential}); a dry run does not (decided 28 September, audit R144).",
    "provenance": "contract catalogue.yaml POST /performances/{performanceId}/cancel"
   },
   {
    "id": "formCreatePerformances",
    "component": "modal",
    "trigger": "Create performances",
    "body": "**Collects what `createPerformances` sends before it is called.** Required: `startsAt`, `endsAt`. Optional: `admissionRulesId`, `seatMapId`, `recurrence`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreatePerformancesRequest",
    "confirm": {
     "label": "Create performances",
     "operation": "createPerformances"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "startsAt",
      "endsAt",
      "admissionRulesId",
      "seatMapId",
      "recurrence"
     ]
    },
    "provenance": "contract catalogue.yaml POST /events/{eventId}/performances"
   },
   {
    "id": "formCreateEvent",
    "component": "modal",
    "trigger": "Create event",
    "body": "**Collects what `createEvent` sends before it is called.** Required: `code`, `name`, `venueId`. Optional: `parentEventId`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateEventRequest",
    "confirm": {
     "label": "Create event",
     "operation": "createEvent"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "code",
      "name",
      "venueId",
      "parentEventId"
     ]
    },
    "provenance": "contract catalogue.yaml POST /events"
   },
   {
    "id": "formRecommendSeats",
    "component": "modal",
    "trigger": "Recommend seats",
    "body": "**Collects what `recommendSeats` sends before it is called.** Required: `partySize`, `strategy`. Optional: `categoryIds`, `maxPrice`, `accessibleCount`, `maxOptions`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "SeatRecommendationRequest",
    "confirm": {
     "label": "Recommend seats",
     "operation": "recommendSeats"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "partySize",
      "strategy",
      "categoryIds",
      "maxPrice",
      "accessibleCount",
      "maxOptions"
     ]
    },
    "provenance": "contract seating.yaml POST /performances/{performanceId}/seat-recommendations"
   },
   {
    "id": "formUpdateEvent",
    "component": "modal",
    "trigger": "Save event",
    "body": "**Collects what `updateEvent` sends before it is called.** Nothing in the body is required. Optional: `name`, `parentEventId`, `isActive`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save event",
     "operation": "updateEvent"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "name",
      "parentEventId",
      "isActive"
     ]
    },
    "provenance": "contract catalogue.yaml PATCH /events/{eventId}"
   },
   {
    "id": "formUpdatePerformance",
    "component": "modal",
    "trigger": "Save performance",
    "body": "**Collects what `updatePerformance` sends before it is called.** Nothing in the body is required. Optional: `startsAt`, `endsAt`, `status`, `admissionRulesId`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save performance",
     "operation": "updatePerformance"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "startsAt",
      "endsAt",
      "status",
      "admissionRulesId"
     ]
    },
    "provenance": "contract catalogue.yaml PATCH /performances/{performanceId}"
   },
   {
    "id": "formUpdateOutlet",
    "component": "modal",
    "trigger": "Save outlet",
    "body": "**Collects what `updateOutlet` sends before it is called.** Nothing in the body is required. Optional: `name`, `stockLocationId`, `costCenterId`, `openingHours`, `isActive`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save outlet",
     "operation": "updateOutlet"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "name",
      "stockLocationId",
      "costCenterId",
      "openingHours",
      "isActive"
     ]
    },
    "provenance": "contract tenancy.yaml PATCH /outlets/{outletId}"
   }
  ],
  "states": {
   "loading": "The opening hours calendar list.",
   "error": "Could not load. Names which read failed and leaves the opening hours calendar untouched.",
   "emptyFirstRun": "No opening hours calendar yet. Offers Create performances (`createPerformances`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on from, to and the opening hours calendar are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `PRODUCT_VIEW`, which `listPerformances` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPerformances",
    "contract": "catalogue",
    "purpose": "List performances of an event",
    "trigger": "onAction"
   },
   {
    "operationId": "getPerformance",
    "contract": "catalogue",
    "purpose": "Read a performance",
    "trigger": "onLoad"
   },
   {
    "operationId": "createPerformances",
    "contract": "catalogue",
    "purpose": "Create performances, singly or by schedule",
    "trigger": "onAction",
    "invalidates": [
     "listPerformances"
    ]
   },
   {
    "operationId": "cancelPerformance",
    "contract": "catalogue",
    "purpose": "Cancel a performance",
    "trigger": "onAction",
    "invalidates": [
     "listPerformances"
    ]
   },
   {
    "operationId": "createEvent",
    "contract": "catalogue",
    "purpose": "Create an event",
    "trigger": "onAction",
    "invalidates": [
     "listPerformances"
    ]
   },
   {
    "operationId": "getEvent",
    "contract": "catalogue",
    "purpose": "Read an event",
    "trigger": "onAction"
   },
   {
    "operationId": "getSeatAvailability",
    "contract": "seating",
    "purpose": "Seat status for a performance",
    "trigger": "onLoad"
   },
   {
    "operationId": "listEvents",
    "contract": "catalogue",
    "purpose": "List events",
    "trigger": "onLoad"
   },
   {
    "operationId": "recommendSeats",
    "contract": "seating",
    "purpose": "Recommend seats for a party",
    "trigger": "onAction",
    "invalidates": [
     "listPerformances"
    ]
   },
   {
    "operationId": "updateEvent",
    "contract": "catalogue",
    "purpose": "Amend an event",
    "trigger": "onAction",
    "invalidates": [
     "listPerformances"
    ]
   },
   {
    "operationId": "updatePerformance",
    "contract": "catalogue",
    "purpose": "Amend a performance",
    "trigger": "onAction",
    "invalidates": [
     "listPerformances"
    ]
   },
   {
    "operationId": "getVenueSettings",
    "contract": "tenancy",
    "purpose": "Operational settings for this venue",
    "trigger": "onLoad"
   },
   {
    "operationId": "updateOutlet",
    "contract": "tenancy",
    "purpose": "Amend an outlet",
    "trigger": "onAction",
    "invalidates": [
     "listPerformances"
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
     "name": "eventId",
     "from": "deepLink"
    },
    {
     "name": "outletId",
     "from": "deepLink"
    },
    {
     "name": "performanceId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "An outlet opened from the directory.",
   "preloaded": [
    "Performance.id",
    "Performance.eventId",
    "Performance.startsAt",
    "Performance.endsAt",
    "Performance.approvalRequestId"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-063",
   "derivedFrom": "wireframes/reference/Seat Board 1.dc.html",
   "note": "**Drawn by Claude Design on `Seat Board 1.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 13 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "BO-102",
  "name": "Sell",
  "module": "Sell",
  "requiresModule": "core",
  "wave": 1,
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell",
   "component": "apps/venue-management-web/src/routes/home/SellList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-007",
    "BO-009",
    "BO-010",
    "BO-011",
    "BO-012",
    "BO-013",
    "BO-014",
    "BO-015",
    "BO-016",
    "BO-017",
    "BO-018",
    "BO-019",
    "BO-037",
    "BO-063",
    "BO-109",
    "BO-110",
    "BO-111",
    "BO-112",
    "BO-113",
    "BO-114",
    "BO-115",
    "BO-116",
    "BO-117",
    "BO-118",
    "BO-119",
    "BO-120",
    "BO-121",
    "BO-122",
    "BO-123",
    "BO-124",
    "BO-125",
    "BO-126",
    "BO-142",
    "BO-143",
    "BO-1190"
   ],
   "transitions": [
    {
     "to": "BO-007",
     "trigger": "Product Directory",
     "provenance": "derived — BO-007 declares entryState.params productId and BO-102 holds none of them. The edge carries nothing: productId only pre-selects (deep link or optional), and BO-007 opens on its own"
    },
    {
     "to": "BO-009",
     "trigger": "Pricing Rules",
     "provenance": "derived — BO-009 declares entryState.params priceListId, ruleId and BO-102 holds none of them. The edge carries nothing: priceListId only pre-selects (deep link or optional); BO-009 finds ruleId (listDynamicPriceRules) itself, and BO-009 opens on its own"
    },
    {
     "to": "BO-010",
     "trigger": "Promotions & Coupons",
     "provenance": "derived — BO-010 declares entryState.params campaignId, code, dashboardId, promotionId, reportId, voucherId and BO-102 holds none of them. The edge carries nothing: campaignId, dashboardId, promotionId, reportId, code only pre-select (deep link or optional); BO-010 opens on listPromotions, and voucherId has no source on BO-010 yet (a gap in BO-010, not in this edge)"
    },
    {
     "to": "BO-011",
     "trigger": "Packages & Bundles",
     "provenance": "derived — BO-011 declares entryState.params bundleId, comboId, productId, version and BO-102 holds none of them. The edge carries nothing: version only pre-selects (deep link or optional); BO-011 finds productId (setPackagePricingDefinition), bundleId (createBundle), comboId (createCombo) itself, and BO-011 opens on its own"
    },
    {
     "to": "BO-012",
     "trigger": "Membership Products",
     "provenance": "derived — BO-012 declares entryState.params productId and BO-102 holds none of them. The edge carries nothing: productId only pre-selects (deep link or optional), and BO-012 opens on its own"
    },
    {
     "to": "BO-013",
     "trigger": "Channel & Distribution",
     "provenance": "derived — BO-013 declares entryState.params channelCapacityId and BO-102 holds none of them. The edge carries nothing: channelCapacityId only pre-selects (deep link or optional), and BO-013 opens on its own"
    },
    {
     "to": "BO-014",
     "trigger": "Catalogue Publishing",
     "provenance": "derived — BO-014 declares entryState.params itemId, priceListId, productId and BO-102 holds none of them. The edge carries nothing: itemId, priceListId, productId only pre-select (deep link or optional), and BO-014 opens on its own"
    },
    {
     "to": "BO-015",
     "trigger": "Performance Calendar",
     "provenance": "derived — BO-015 declares entryState.params eventId, performanceId and BO-102 holds none of them. The edge carries nothing: eventId, performanceId only pre-select (deep link or optional), and BO-015 opens on its own"
    },
    {
     "to": "BO-016",
     "trigger": "Performance Template",
     "provenance": "derived — BO-016 declares entryState.params  and BO-102 holds none of them. The edge carries nothing: BO-016 needs nothing to open"
    },
    {
     "to": "BO-017",
     "trigger": "Capacity Management",
     "provenance": "derived — BO-017 declares entryState.params channelCapacityId, entryId and BO-102 holds none of them. The edge carries nothing: channelCapacityId only pre-selects (deep link or optional); BO-017 finds entryId (listWaitlistEntries) itself, and BO-017 opens on its own"
    },
    {
     "to": "BO-018",
     "trigger": "Allocation & Holds",
     "provenance": "derived — BO-018 declares entryState.params inventoryHoldId and BO-102 holds none of them. The edge carries nothing: inventoryHoldId only pre-selects (deep link or optional), and BO-018 opens on its own"
    },
    {
     "to": "BO-019",
     "trigger": "Closures & Blackouts",
     "provenance": "derived — BO-019 declares entryState.params eventId, mapId, pathId, performanceId and BO-102 holds none of them. The edge carries nothing: eventId, performanceId only pre-select (deep link or optional); BO-019 opens on listEvents, and mapId, pathId have no source on BO-019 yet (a gap in BO-019, not in this edge)"
    },
    {
     "to": "BO-037",
     "trigger": "Offline Package Status",
     "provenance": "derived — BO-037 declares entryState.params version and BO-102 holds none of them. The edge carries nothing: version only pre-selects (deep link or optional), and BO-037 opens on its own"
    },
    {
     "to": "BO-063",
     "trigger": "Opening Hours & Calendar",
     "provenance": "derived — BO-063 declares entryState.params eventId, outletId, performanceId and BO-102 holds none of them. The edge carries nothing: eventId, outletId, performanceId only pre-select (deep link or optional), and BO-063 opens on its own"
    },
    {
     "to": "BO-109",
     "trigger": "Menu Builder & POS Layout Designer",
     "provenance": "derived — BO-109 declares entryState.params menuId, saleBoardId and BO-102 holds none of them. The edge carries nothing: menuId, saleBoardId only pre-select (deep link or optional), and BO-109 opens on its own"
    },
    {
     "to": "BO-110",
     "trigger": "Recipe & BOM Management",
     "provenance": "derived — BO-110 declares entryState.params  and BO-102 holds none of them. The edge carries nothing: BO-110 needs nothing to open"
    },
    {
     "to": "BO-111",
     "trigger": "Ingredient Substitution, Allergen & Nutrition",
     "provenance": "derived — BO-111 declares entryState.params menuId, menuItemId, recipeId and BO-102 holds none of them. The edge carries nothing: menuId, menuItemId only pre-select (deep link or optional); BO-111 finds recipeId (setSubstitutionRules) itself, and BO-111 opens on its own"
    },
    {
     "to": "BO-112",
     "trigger": "Production Planning & Production Sheets",
     "provenance": "derived — BO-112 declares entryState.params  and BO-102 holds none of them. The edge carries nothing: BO-112 needs nothing to open"
    },
    {
     "to": "BO-113",
     "trigger": "Central Kitchen & Commissary Management",
     "provenance": "derived — BO-113 declares entryState.params runId and BO-102 holds none of them. The edge carries nothing: runId only pre-selects (deep link or optional), and BO-113 opens on its own"
    },
    {
     "to": "BO-114",
     "trigger": "Variants, Attributes, Barcode & RFID Management",
     "provenance": "derived — BO-114 declares entryState.params  and BO-102 holds none of them. The edge carries nothing: BO-114 needs nothing to open"
    },
    {
     "to": "BO-115",
     "trigger": "Category, Brand & Merchandise Hierarchy",
     "provenance": "derived — BO-115 declares entryState.params reportId and BO-102 holds none of them. The edge carries nothing: reportId only pre-selects (deep link or optional), and BO-115 opens on its own"
    },
    {
     "to": "BO-116",
     "trigger": "Merchandising & Product Presentation",
     "provenance": "derived — BO-116 declares entryState.params merchandiseId, roleId, saleBoardId and BO-102 holds none of them. The edge carries nothing: merchandiseId, roleId, saleBoardId only pre-select (deep link or optional), and BO-116 opens on its own"
    },
    {
     "to": "BO-117",
     "trigger": "Product Import, Governance & AI Configuration Assistant",
     "provenance": "derived — BO-117 declares entryState.params jobId, saleBoardId and BO-102 holds none of them. The edge carries nothing: saleBoardId only pre-selects (deep link or optional); BO-117 finds jobId (importProductCatalogue) itself, and BO-117 opens on its own"
    },
    {
     "to": "BO-118",
     "trigger": "Campaign & Audience Management",
     "provenance": "derived — BO-118 declares entryState.params reportId, saleBoardId and BO-102 holds none of them. The edge carries nothing: reportId, saleBoardId only pre-select (deep link or optional), and BO-118 opens on its own"
    },
    {
     "to": "BO-119",
     "trigger": "Cross-Sell, Upsell & Recommendation Rules",
     "provenance": "derived — BO-119 declares entryState.params ruleId and BO-102 holds none of them. The edge carries nothing: BO-119 finds ruleId (createUpsellRule) itself, and BO-119 opens on its own"
    },
    {
     "to": "BO-120",
     "trigger": "Omnichannel Commerce & Journey Configuration",
     "provenance": "derived — BO-120 declares entryState.params  and BO-102 holds none of them. The edge carries nothing: BO-120 needs nothing to open"
    },
    {
     "to": "BO-121",
     "trigger": "Personalized Offers & Guest Engagement",
     "provenance": "derived — BO-121 declares entryState.params  and BO-102 holds none of them. The edge carries nothing: BO-121 needs nothing to open"
    },
    {
     "to": "BO-122",
     "trigger": "POS Experience Dashboard",
     "provenance": "derived — BO-122 declares entryState.params  and BO-102 holds none of them. The edge carries nothing: BO-122 needs nothing to open"
    },
    {
     "to": "BO-123",
     "trigger": "POS Profile Management",
     "provenance": "derived — BO-123 declares entryState.params  and BO-102 holds none of them. The edge carries nothing: BO-123 needs nothing to open"
    },
    {
     "to": "BO-124",
     "trigger": "Layout & Journey Builder",
     "provenance": "derived — BO-124 declares entryState.params deviceId, profileId, saleBoardId and BO-102 holds none of them. The edge carries nothing: saleBoardId, deviceId, profileId only pre-select (deep link or optional), and BO-124 opens on its own"
    },
    {
     "to": "BO-125",
     "trigger": "Product & Category Button Configuration",
     "provenance": "derived — BO-125 declares entryState.params deviceId, saleBoardId, workstationId and BO-102 holds none of them. The edge carries nothing: saleBoardId, deviceId, workstationId only pre-select (deep link or optional), and BO-125 opens on its own"
    },
    {
     "to": "BO-126",
     "trigger": "Deployment, Preview & Audit",
     "provenance": "derived — BO-126 declares entryState.params profileId, reportId, rolloutId, saleBoardId and BO-102 holds none of them. The edge carries nothing: profileId, saleBoardId, reportId, rolloutId only pre-select (deep link or optional), and BO-126 opens on its own"
    },
    {
     "to": "BO-142",
     "trigger": "Store Rules, Controls & Permissions",
     "provenance": "derived — BO-142 declares entryState.params  and BO-102 holds none of them. The edge carries nothing: BO-142 needs nothing to open"
    },
    {
     "to": "BO-143",
     "trigger": "Retail Global Settings & Controls",
     "provenance": "derived — BO-143 declares entryState.params dropId and BO-102 holds none of them. The edge carries nothing: BO-143 opens on lookupShopAndDrop, and dropId has no source on BO-143 yet (a gap in BO-143, not in this edge)"
    },
    {
     "to": "BO-1190",
     "trigger": "Donation Campaigns",
     "provenance": "decided 29 September, VM close-out (venue management and configuration)"
    }
   ]
  },
  "notes": "Section landing. **14 screens reach the entry point through here** — before 20 August they reached it through nothing.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listUpsellRules` reads the population and `getVenueSettings` reads one of them — list, select, act",
  "purpose": "Everything in sell, and what in it needs attention.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Placement",
       "operation": "listUpsellRules",
       "notes": "Sends `?placement=` to `listUpsellRules`.",
       "provenance": "contract promotions.yaml GET /upsell-rules"
      },
      {
       "kind": "dataTable",
       "label": "Every upsell rule",
       "bindsTo": "UpsellRule",
       "columns": [
        "UpsellRule.id",
        "UpsellRule.name",
        "UpsellRule.placement",
        "UpsellRule.triggerVariantIds",
        "UpsellRule.triggerCategoryIds",
        "UpsellRule.suggestedVariantIds",
        "UpsellRule.suggestedBundleId",
        "UpsellRule.channels",
        "UpsellRule.priority",
        "UpsellRule.maxSuggestions",
        "UpsellRule.isActive",
        "UpsellRule.regionId"
       ],
       "operation": "listUpsellRules",
       "notes": "**Read-only at the venue** (decided 28 September, audit R183) — upsell rules are created and deleted at region level; the venue sees the rules of its region in force, with no create, edit or delete here.",
       "provenance": "contract promotions.yaml GET /upsell-rules"
      },
      {
       "kind": "cardList",
       "bindsTo": "screens",
       "notes": "14 screens, each with what needs attention.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "searchField",
       "label": "Search sell",
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
       "label": "The selected upsell rule",
       "bindsTo": "UpsellRule",
       "columns": [
        "UpsellRule.id",
        "UpsellRule.name",
        "UpsellRule.placement",
        "UpsellRule.triggerVariantIds",
        "UpsellRule.triggerCategoryIds",
        "UpsellRule.suggestedVariantIds",
        "UpsellRule.suggestedBundleId",
        "UpsellRule.channels",
        "UpsellRule.priority",
        "UpsellRule.maxSuggestions",
        "UpsellRule.isActive",
        "UpsellRule.regionId"
       ],
       "operation": "listUpsellRules",
       "notes": "**Read-only at the venue** (decided 28 September, audit R183) — upsell rules are created and deleted at region level; the venue sees the rules of its region in force, with no create, edit or delete here.",
       "provenance": "contract promotions.yaml GET /upsell-rules"
      },
      {
       "kind": "detailPanel",
       "label": "The upsell suggestion",
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
    }
   ]
  },
  "states": {
   "loading": "The list, with counts.",
   "error": "Could not load. Venue Home is still reachable.",
   "emptyFirstRun": "**Nothing configured in sell yet.** The action is the first thing to set up, not a blank list.",
   "emptyNoResults": "Nothing matches the filter.",
   "emptyNoAccess": "You do not have permission for sell. **Said plainly** — an empty section reads as broken."
  },
  "apis": [
   {
    "operationId": "getVenueSettings",
    "contract": "tenancy",
    "purpose": "What is enabled here",
    "trigger": "onLoad"
   },
   {
    "operationId": "listUpsellRules",
    "contract": "promotions",
    "purpose": "Upsell rules in force, read-only — owned at region (decided 28 September, audit R183)",
    "trigger": "onLoad"
   },
   {
    "operationId": "decideRecommendations",
    "contract": "ai",
    "purpose": "Fill a recommendation slot",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "recordRecommendationEvents",
    "contract": "ai",
    "purpose": "Report what happened to recommended items",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-102"
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
  "id": "BO-109",
  "name": "Menu Builder & POS Layout Designer",
  "module": "Sell",
  "requiresModule": "fnb",
  "wave": 2,
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/menu-builder-pos-layout-designer",
   "component": "apps/venue-management-web/src/routes/sell/MenuBuilderPosLayoutDesignerList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-102"
   ],
   "exitTo": [
    "BO-102"
   ],
   "inferred": false,
   "notes": "**Returns to BO-102.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "BO-102",
     "trigger": "Sell",
     "provenance": "derived — BO-102 declares entryState.params  and BO-109 holds none of them. The edge carries nothing: BO-109 is opened from BO-102, so this edge is the way back and BO-102 keeps its own state"
    }
   ]
  },
  "notes": "**Added 20 August from the client design board.** The operations existed and no screen called them. **Drawn 31 August** — `FnB Board 2.dc.html` frame `fnb-2b`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Menu Builder &amp; POS Layout Designer* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.",
  "density": "compact",
  "boardFrames": [
   "FnB Board 2.dc.html#fnb-2b"
  ],
  "pattern": "listDetail",
  "patternReason": "`listMenus` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Menu Builder & POS Layout Designer — from the client design board, 20 August.",
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
       "kind": "searchField",
       "label": "Search menu builder",
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
       "operation": "listMenus",
       "provenance": "contract fnb.yaml GET /menus"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save menu sections",
       "operation": "setMenuSections",
       "provenance": "contract fnb.yaml PUT /menus/{menuId}/sections"
      },
      {
       "kind": "secondaryButton",
       "label": "Save sale board",
       "operation": "updateSaleBoard",
       "provenance": "contract tenancy.yaml PUT /sale-boards/{saleBoardId}"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The menu pos layout list.",
   "error": "Could not load. Names which read failed and leaves the menu pos layout untouched.",
   "emptyFirstRun": "No menu pos layout yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on outletId, activeAt and the menu pos layout are still there. Names the active filter and offers to clear it.",
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
    "operationId": "setMenuSections",
    "contract": "fnb",
    "purpose": "Set menu sections and their item ordering",
    "trigger": "onAction",
    "invalidates": [
     "listMenus"
    ]
   },
   {
    "operationId": "updateSaleBoard",
    "contract": "tenancy",
    "purpose": "Update a sale board",
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
     "name": "saleBoardId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "Resolves from the session. A principal with more than one venue is asked which before the page renders.",
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-109",
   "derivedFrom": "wireframes/reference/FnB Board 2.dc.html",
   "note": "**Drawn by Claude Design on `FnB Board 2.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
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
    "id": "formUpdateSaleBoard",
    "component": "modal",
    "trigger": "Save sale board",
    "body": "**Collects what `updateSaleBoard` sends before it is called.** Required: `id`, `code`, `name`, `venueId`, `kind`, `pages`. Optional: `isActive`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "SaleBoard",
    "confirm": {
     "label": "Save sale board",
     "operation": "updateSaleBoard"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "code",
      "name",
      "venueId",
      "kind",
      "pages",
      "isActive"
     ]
    },
    "provenance": "contract tenancy.yaml PUT /sale-boards/{saleBoardId}"
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
  "id": "BO-110",
  "name": "Recipe & BOM Management",
  "module": "Sell",
  "requiresModule": "fnb",
  "wave": 2,
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/recipe-bom-management",
   "component": "apps/venue-management-web/src/routes/sell/RecipeBomManagementList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-102"
   ],
   "exitTo": [
    "BO-102"
   ],
   "inferred": false,
   "notes": "**Returns to BO-102.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "BO-102",
     "trigger": "Sell",
     "provenance": "derived — BO-102 declares entryState.params  and BO-110 holds none of them. The edge carries nothing: BO-110 is opened from BO-102, so this edge is the way back and BO-102 keeps its own state"
    }
   ]
  },
  "notes": "**Added 20 August from the client design board.** The operations existed and no screen called them.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listRecipes` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Recipe & BOM Management — from the client design board, 20 August.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "searchField",
       "label": "Search",
       "operation": "listRecipes",
       "notes": "Sends `?search=` to `listRecipes`.",
       "provenance": "contract fnb.yaml GET /recipes"
      },
      {
       "kind": "textField",
       "label": "Menu item id",
       "operation": "listRecipes",
       "notes": "Sends `?menuItemId=` to `listRecipes`.",
       "provenance": "contract fnb.yaml GET /recipes"
      },
      {
       "kind": "dataTable",
       "label": "Every recipe",
       "bindsTo": "Recipe",
       "columns": [
        "Recipe.menuItemId",
        "Recipe.yield",
        "Recipe.ingredients",
        "Recipe.costPerPortion"
       ],
       "operation": "listRecipes",
       "provenance": "contract fnb.yaml GET /recipes"
      },
      {
       "kind": "searchField",
       "label": "Search recipe",
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
       "label": "The selected recipe",
       "bindsTo": "Recipe",
       "columns": [
        "Recipe.menuItemId",
        "Recipe.yield",
        "Recipe.ingredients",
        "Recipe.costPerPortion"
       ],
       "operation": "listRecipes",
       "provenance": "contract fnb.yaml GET /recipes"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save recipe",
       "operation": "setRecipe",
       "provenance": "contract fnb.yaml PUT /recipes"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The recipe bom list.",
   "error": "Could not load. Names which read failed and leaves the recipe bom untouched.",
   "emptyFirstRun": "No recipe bom yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on search, menuItemId and the recipe bom are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `PRODUCT_VIEW`, which `listRecipes` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listRecipes",
    "contract": "fnb",
    "purpose": "List recipes",
    "trigger": "onLoad"
   },
   {
    "operationId": "setRecipe",
    "contract": "fnb",
    "purpose": "Define a recipe for a menu item",
    "trigger": "onAction",
    "invalidates": [
     "listRecipes"
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
   "coldEntry": "Resolves from the session. A principal with more than one venue is asked which before the page renders.",
   "preloaded": [
    "Recipe.menuItemId",
    "Recipe.yield",
    "Recipe.ingredients",
    "Recipe.costPerPortion"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-110"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formSetRecipe",
    "component": "modal",
    "trigger": "Save recipe",
    "body": "**Collects what `setRecipe` sends before it is called.** Required: `menuItemId`, `ingredients`. Optional: `yield`, `costPerPortion`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "Recipe",
    "confirm": {
     "label": "Save recipe",
     "operation": "setRecipe"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "menuItemId",
      "ingredients",
      "yield",
      "costPerPortion"
     ]
    },
    "provenance": "contract fnb.yaml PUT /recipes"
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
  "id": "BO-111",
  "name": "Ingredient Substitution, Allergen & Nutrition",
  "module": "Sell",
  "requiresModule": "fnb",
  "wave": 2,
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/ingredient-substitution-allergen-nutrition",
   "component": "apps/venue-management-web/src/routes/sell/IngredientSubstitutionAllergenNutritioList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-102"
   ],
   "exitTo": [
    "BO-102",
    "BO-045"
   ],
   "inferred": false,
   "notes": "**Returns to BO-102.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product. **flow F31 — allergen verification returns to the menu it was opened from.** The flow is the authority on the journey and the navigation has to agree with it; marking this block non-inferred is what turned the disagreement from a warning into a failure.",
   "transitions": [
    {
     "to": "BO-102",
     "trigger": "Sell",
     "provenance": "derived — BO-102 declares entryState.params  and BO-111 holds none of them. The edge carries nothing: BO-111 is opened from BO-102, so this edge is the way back and BO-102 keeps its own state"
    },
    {
     "to": "BO-045",
     "trigger": "The draft is scheduled for Monday rather than published now",
     "provenance": "flow F31 step 3→4, F93 step 1→2",
     "carries": [
      "menuId",
      "menuItemId"
     ]
    }
   ]
  },
  "notes": "**Added 20 August from the client design board.** The operations existed and no screen called them.",
  "density": "compact",
  "boardFrames": [
   "FnB Board 2.dc.html#fnb-2l"
  ],
  "pattern": "configEditor",
  "patternReason": "the screen declares only writes (`setRecipe`, `updateMenu`, `setSubstitutionRules`) and no read of a population — it is settings, not a list",
  "purpose": "Ingredient Substitution, Allergen & Nutrition — from the client design board, 20 August.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "textField",
       "label": "menuItemId",
       "bindsTo": "Recipe.menuItemId",
       "provenance": "contract fnb.yaml PUT /recipes"
      },
      {
       "kind": "textField",
       "label": "yield",
       "bindsTo": "Recipe.yield",
       "provenance": "contract fnb.yaml PUT /recipes"
      },
      {
       "kind": "textField",
       "label": "ingredients",
       "bindsTo": "Recipe.ingredients",
       "provenance": "contract fnb.yaml PUT /recipes"
      },
      {
       "kind": "textField",
       "label": "costPerPortion",
       "bindsTo": "Recipe.costPerPortion",
       "provenance": "contract fnb.yaml PUT /recipes"
      },
      {
       "kind": "searchField",
       "label": "Search ingredient substitution, allergen",
       "provenance": "carried from the previous definition"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save recipe",
       "operation": "setRecipe",
       "provenance": "contract fnb.yaml PUT /recipes"
      },
      {
       "kind": "secondaryButton",
       "label": "Save menu",
       "operation": "updateMenu",
       "provenance": "contract fnb.yaml PATCH /menus/{menuId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Save substitution rules",
       "operation": "setSubstitutionRules",
       "provenance": "contract fnb.yaml PUT /substitution-rules"
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
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The saved ingredient substitution allergen.",
   "error": "Could not load. Names which read failed and leaves the ingredient substitution allergen untouched.",
   "emptyFirstRun": "No ingredient substitution allergen configured. The form opens empty and `setRecipe` saves the first one; it says what the platform does in the meantime.",
   "emptyNoAccess": "Shown when the caller lacks `PRODUCT_CONFIGURE`, which `setRecipe` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setRecipe",
    "contract": "fnb",
    "purpose": "Define a recipe for a menu item",
    "trigger": "onAction"
   },
   {
    "operationId": "updateMenu",
    "contract": "fnb",
    "purpose": "Amend a menu",
    "trigger": "onAction"
   },
   {
    "operationId": "setSubstitutionRules",
    "contract": "fnb",
    "purpose": "What may replace what",
    "trigger": "onAction"
   },
   {
    "operationId": "verifyAllergens",
    "contract": "fnb",
    "purpose": "Does this dish still match its claim? Runs automatically after every change; here a manual re-check (audit R241)",
    "trigger": "onAction"
   },
   {
    "operationId": "setIngredientSubstitutes",
    "contract": "fnb",
    "purpose": "Define approved ingredient substitutions",
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
     "name": "menuId",
     "from": "deepLink"
    },
    {
     "name": "menuItemId",
     "from": "deepLink"
    },
    {
     "name": "recipeId",
     "from": "navigation"
    }
   ],
   "coldEntry": "Resolves from the session. A principal with more than one venue is asked which before the page renders. An item opened from the menu. **Allergen verification is per item** — a menu-wide check is a job, not a screen."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-111",
   "derivedFrom": "wireframes/reference/FnB Board 2.dc.html",
   "source": "Claude Design F&B pack, 24 August",
   "note": "**Drawn by Claude Design on `FnB Board 2.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
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
    "id": "formSetSubstitutionRules",
    "component": "modal",
    "trigger": "Save substitution rules",
    "body": "**Collects what `setSubstitutionRules` sends before it is called.** Required: `rules`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save substitution rules",
     "operation": "setSubstitutionRules"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "rules"
     ]
    },
    "provenance": "contract fnb.yaml PUT /substitution-rules"
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
  "id": "BO-112",
  "name": "Production Planning & Production Sheets",
  "module": "Sell",
  "requiresModule": "fnb",
  "wave": 2,
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/production-planning-production-sheets",
   "component": "apps/venue-management-web/src/routes/sell/ProductionPlanningProductionSheetsList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-007",
    "BO-102"
   ],
   "exitTo": [
    "BO-009",
    "BO-102"
   ],
   "inferred": false,
   "notes": "**Returns to BO-102.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "BO-009",
     "trigger": "Pricing Rules",
     "provenance": "flow F78 step 3→4",
     "operation": "planProductionRun"
    },
    {
     "to": "BO-102",
     "trigger": "Sell",
     "provenance": "derived — BO-102 declares entryState.params  and BO-112 holds none of them. The edge carries nothing: BO-112 is opened from BO-102, so this edge is the way back and BO-102 keeps its own state"
    }
   ]
  },
  "notes": "**Added 20 August from the client design board.** The operations existed and no screen called them.",
  "density": "compact",
  "boardFrames": [
   "Retail Board 2.dc.html#ret-2e"
  ],
  "pattern": "configEditor",
  "patternReason": "the screen declares only writes (`planProductionRun`) and no read of a population — it is settings, not a list",
  "purpose": "Production Planning & Production Sheets — from the client design board, 20 August.",
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
       "bindsTo": "ProductionRun.id",
       "provenance": "contract fnb.yaml POST /production-runs"
      },
      {
       "kind": "textField",
       "label": "recipeId",
       "bindsTo": "ProductionRun.recipeId",
       "provenance": "contract fnb.yaml POST /production-runs"
      },
      {
       "kind": "textField",
       "label": "producingOutletId",
       "bindsTo": "ProductionRun.producingOutletId",
       "provenance": "contract fnb.yaml POST /production-runs"
      },
      {
       "kind": "textField",
       "label": "forOutletIds",
       "bindsTo": "ProductionRun.forOutletIds",
       "provenance": "contract fnb.yaml POST /production-runs"
      },
      {
       "kind": "textField",
       "label": "plannedQuantity",
       "bindsTo": "ProductionRun.plannedQuantity",
       "provenance": "contract fnb.yaml POST /production-runs"
      },
      {
       "kind": "textField",
       "label": "actualQuantity",
       "bindsTo": "ProductionRun.actualQuantity",
       "provenance": "contract fnb.yaml POST /production-runs"
      },
      {
       "kind": "textField",
       "label": "scheduledFor",
       "bindsTo": "ProductionRun.scheduledFor",
       "provenance": "contract fnb.yaml POST /production-runs"
      },
      {
       "kind": "textField",
       "label": "status",
       "bindsTo": "ProductionRun.status",
       "provenance": "contract fnb.yaml POST /production-runs"
      },
      {
       "kind": "textField",
       "label": "varianceReason",
       "bindsTo": "ProductionRun.varianceReason",
       "provenance": "contract fnb.yaml POST /production-runs"
      },
      {
       "kind": "searchField",
       "label": "Search production planning",
       "provenance": "carried from the previous definition"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Plan production run",
       "operation": "planProductionRun",
       "provenance": "contract fnb.yaml POST /production-runs"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The saved production planning production.",
   "error": "Could not load. Names which read failed and leaves the production planning production untouched.",
   "emptyFirstRun": "No production planning production configured. The form opens empty and `planProductionRun` saves the first one; it says what the platform does in the meantime.",
   "emptyNoAccess": "Shown when the caller lacks `PRODUCT_CONFIGURE`, which `planProductionRun` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "planProductionRun",
    "contract": "fnb",
    "purpose": "Plan a batch, for one outlet or several",
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
   "coldEntry": "Resolves from the session. A principal with more than one venue is asked which before the page renders."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-112",
   "derivedFrom": "wireframes/reference/Retail Board 2.dc.html",
   "source": "Claude Design Retail pack, 24 August",
   "note": "**Drawn by Claude Design on `Retail Board 2.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 1 operation this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "BO-113",
  "name": "Central Kitchen & Commissary Management",
  "module": "Sell",
  "requiresModule": "fnb",
  "wave": 2,
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/central-kitchen-commissary-management",
   "component": "apps/venue-management-web/src/routes/sell/CentralKitchenCommissaryManagementList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-102"
   ],
   "exitTo": [
    "BO-102"
   ],
   "inferred": false,
   "notes": "**Returns to BO-102.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "BO-102",
     "trigger": "Sell",
     "provenance": "derived — BO-102 declares entryState.params  and BO-113 holds none of them. The edge carries nothing: BO-113 is opened from BO-102, so this edge is the way back and BO-102 keeps its own state"
    }
   ]
  },
  "notes": "**Added 20 August from the client design board.** The operations existed and no screen called them.",
  "density": "compact",
  "boardFrames": [
   "Retail Board 2.dc.html#ret-2d"
  ],
  "pattern": "configEditor",
  "patternReason": "the screen declares only writes (`planProductionRun`, `completeProductionRun`) and no read of a population — it is settings, not a list",
  "purpose": "Central Kitchen & Commissary Management — from the client design board, 20 August.",
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
       "bindsTo": "ProductionRun.id",
       "provenance": "contract fnb.yaml POST /production-runs"
      },
      {
       "kind": "textField",
       "label": "recipeId",
       "bindsTo": "ProductionRun.recipeId",
       "provenance": "contract fnb.yaml POST /production-runs"
      },
      {
       "kind": "textField",
       "label": "producingOutletId",
       "bindsTo": "ProductionRun.producingOutletId",
       "provenance": "contract fnb.yaml POST /production-runs"
      },
      {
       "kind": "textField",
       "label": "forOutletIds",
       "bindsTo": "ProductionRun.forOutletIds",
       "provenance": "contract fnb.yaml POST /production-runs"
      },
      {
       "kind": "textField",
       "label": "plannedQuantity",
       "bindsTo": "ProductionRun.plannedQuantity",
       "provenance": "contract fnb.yaml POST /production-runs"
      },
      {
       "kind": "textField",
       "label": "actualQuantity",
       "bindsTo": "ProductionRun.actualQuantity",
       "provenance": "contract fnb.yaml POST /production-runs"
      },
      {
       "kind": "textField",
       "label": "scheduledFor",
       "bindsTo": "ProductionRun.scheduledFor",
       "provenance": "contract fnb.yaml POST /production-runs"
      },
      {
       "kind": "textField",
       "label": "status",
       "bindsTo": "ProductionRun.status",
       "provenance": "contract fnb.yaml POST /production-runs"
      },
      {
       "kind": "textField",
       "label": "varianceReason",
       "bindsTo": "ProductionRun.varianceReason",
       "provenance": "contract fnb.yaml POST /production-runs"
      },
      {
       "kind": "searchField",
       "label": "Search central kitchen",
       "provenance": "carried from the previous definition"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Plan production run",
       "operation": "planProductionRun",
       "provenance": "contract fnb.yaml POST /production-runs"
      },
      {
       "kind": "secondaryButton",
       "label": "Complete production run",
       "operation": "completeProductionRun",
       "provenance": "contract fnb.yaml POST /production-runs/{runId}/complete"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The saved central kitchen commissary.",
   "error": "Could not load. Names which read failed and leaves the central kitchen commissary untouched.",
   "emptyFirstRun": "No central kitchen commissary configured. The form opens empty and `planProductionRun` saves the first one; it says what the platform does in the meantime.",
   "emptyNoAccess": "Shown when the caller lacks `PRODUCT_CONFIGURE`, which `planProductionRun` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "planProductionRun",
    "contract": "fnb",
    "purpose": "Plan a batch, for one outlet or several",
    "trigger": "onAction"
   },
   {
    "operationId": "completeProductionRun",
    "contract": "fnb",
    "purpose": "Record what was actually made",
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
     "name": "runId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "Resolves from the session. A principal with more than one venue is asked which before the page renders."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-113",
   "derivedFrom": "wireframes/reference/Retail Board 2.dc.html",
   "source": "Claude Design Retail pack, 24 August",
   "note": "**Drawn by Claude Design on `Retail Board 2.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formCompleteProductionRun",
    "component": "modal",
    "trigger": "Complete production run",
    "body": "**Collects what `completeProductionRun` sends before it is called.** Required: `actualQuantity`, `recordedAt`. Optional: `varianceReason`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Complete production run",
     "operation": "completeProductionRun"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "actualQuantity",
      "recordedAt",
      "varianceReason"
     ]
    },
    "provenance": "contract fnb.yaml POST /production-runs/{runId}/complete"
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
 "acquireInventoryHold": {
  "method": "POST",
  "path": "/inventory-holds",
  "contract": "catalogue",
  "summary": "Acquire an inventory hold",
  "permission": "ORDER_CREATE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "workstation",
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
  "requestBody": "AcquireLeaseRequest",
  "responds": "InventoryHold"
 },
 "cancelPerformance": {
  "method": "POST",
  "path": "/performances/{performanceId}/cancel",
  "contract": "catalogue",
  "summary": "Cancel a performance",
  "permission": "PERFORMANCE_CONFIGURE",
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
  "responds": "PerformanceCancellationResult"
 },
 "completeProductionRun": {
  "method": "POST",
  "path": "/production-runs/{runId}/complete",
  "contract": "fnb",
  "summary": "Record what was actually made",
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
  "responds": "ProductionRun"
 },
 "createEvent": {
  "method": "POST",
  "path": "/events",
  "contract": "catalogue",
  "summary": "Create an event",
  "permission": "EVENT_CONFIGURE",
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
  "requestBody": "CreateEventRequest",
  "responds": "Event"
 },
 "createPerformances": {
  "method": "POST",
  "path": "/events/{eventId}/performances",
  "contract": "catalogue",
  "summary": "Create performances, singly or by schedule",
  "permission": "PERFORMANCE_CONFIGURE",
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
  "requestBody": "CreatePerformancesRequest",
  "responds": null
 },
 "decideRecommendations": {
  "method": "POST",
  "path": "/recommendations/decide",
  "contract": "ai",
  "summary": "Fill a recommendation slot",
  "permission": "AI_USE",
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
  "responds": "AiRecommendationResult"
 },
 "forceReleaseInventoryHold": {
  "method": "POST",
  "path": "/inventory-holds/{inventoryHoldId}/force-release",
  "contract": "catalogue",
  "summary": "Reclaim a stranded inventory hold",
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
  "requestBody": null,
  "responds": "InventoryHold"
 },
 "getEvent": {
  "method": "GET",
  "path": "/events/{eventId}",
  "contract": "catalogue",
  "summary": "Read an event",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "Event"
 },
 "getLatestBundle": {
  "method": "GET",
  "path": "/catalogue/bundles/latest",
  "contract": "catalogue",
  "summary": "Pull the current bundle for this workstation's venue",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "workstation",
  "parameters": [
   {
    "name": "since",
    "in": "query",
    "required": null
   },
   {
    "name": "If-None-Match",
    "in": "header",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "CatalogueBundle"
 },
 "getOfflinePackage": {
  "method": "GET",
  "path": "/access/offline-package",
  "contract": "access",
  "summary": "Entitlement and rule set for offline validation",
  "permission": "ACCESS_VALIDATE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "workstation",
  "parameters": [
   {
    "name": "sinceVersion",
    "in": "query",
    "required": null
   },
   {
    "name": null,
    "in": null,
    "required": null
   },
   {
    "name": "validFrom",
    "in": "query",
    "required": true
   },
   {
    "name": "validTo",
    "in": "query",
    "required": true
   },
   {
    "name": "If-None-Match",
    "in": "header",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "OfflinePackage"
 },
 "getPerformance": {
  "method": "GET",
  "path": "/performances/{performanceId}",
  "contract": "catalogue",
  "summary": "Read a performance",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "Performance"
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
 "listCatalogueBundles": {
  "method": "GET",
  "path": "/catalogue/bundles",
  "contract": "catalogue",
  "summary": "List published catalogue bundles",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "BundleSummary"
 },
 "listEvents": {
  "method": "GET",
  "path": "/events",
  "contract": "catalogue",
  "summary": "List events",
  "permission": "PRODUCT_VIEW",
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
  "responds": "Page"
 },
 "listInventoryHolds": {
  "method": "GET",
  "path": "/inventory-holds",
  "contract": "catalogue",
  "summary": "List inventory holds",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "channelCapacityId",
    "in": "query",
    "required": null
   },
   {
    "name": "holderWorkstationId",
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
    "name": "categoryId",
    "in": "query",
    "required": null
   },
   {
    "name": "language",
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
 "listRecipes": {
  "method": "GET",
  "path": "/recipes",
  "contract": "fnb",
  "summary": "List recipes",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "search",
    "in": "query",
    "required": null
   },
   {
    "name": "menuItemId",
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
 "listSyncRejections": {
  "method": "GET",
  "path": "/sync/rejections",
  "contract": "orders",
  "summary": "Entries the server refused",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "workstationId",
    "in": "query",
    "required": null
   },
   {
    "name": "kind",
    "in": "query",
    "required": null
   },
   {
    "name": "resolved",
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
 "listUpsellRules": {
  "method": "GET",
  "path": "/upsell-rules",
  "contract": "promotions",
  "summary": "List upsell and cross-sell rules",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "placement",
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
 "planProductionRun": {
  "method": "POST",
  "path": "/production-runs",
  "contract": "fnb",
  "summary": "Plan a batch, for one outlet or several",
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
  "requestBody": "ProductionRun",
  "responds": "ProductionRun"
 },
 "publishBundle": {
  "method": "POST",
  "path": "/catalogue/bundles",
  "contract": "catalogue",
  "summary": "Compute, sign and publish a catalogue bundle",
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
  "responds": "BundleSummary"
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "SeatRecommendationRequest",
  "responds": null
 },
 "recordRecommendationEvents": {
  "method": "POST",
  "path": "/recommendations/events",
  "contract": "ai",
  "summary": "Report what happened to recommended items",
  "permission": "AI_USE",
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
 "relinquishInventoryHold": {
  "method": "DELETE",
  "path": "/inventory-holds/{inventoryHoldId}",
  "contract": "catalogue",
  "summary": "Return unsold units",
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
  "responds": "InventoryHold"
 },
 "renewInventoryHold": {
  "method": "POST",
  "path": "/inventory-holds/{inventoryHoldId}/renew",
  "contract": "catalogue",
  "summary": "Extend an inventory hold's TTL",
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
  "responds": "InventoryHold"
 },
 "reportBundleApplied": {
  "method": "POST",
  "path": "/catalogue/bundles/{version}/applied",
  "contract": "catalogue",
  "summary": "Report that a workstation applied a bundle",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "append",
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
 "setIngredientSubstitutes": {
  "method": "PUT",
  "path": "/recipes/{recipeId}/substitutes",
  "contract": "fnb",
  "summary": "Define approved substitutions",
  "permission": "PRODUCT_CONFIGURE",
  "offlineCapable": null,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   },
   {
    "name": "recipeId",
    "in": "path",
    "required": true
   },
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "FnbIngredientSubstitute",
  "responds": "FnbIngredientSubstitute"
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
   },
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Menu"
 },
 "setOfflinePolicy": {
  "method": "PUT",
  "path": "/offline-policy",
  "contract": "tenancy",
  "summary": "What a workstation may do with no network, and for how long",
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
  "requestBody": "OfflinePolicy",
  "responds": "OfflinePolicy"
 },
 "setPathClosure": {
  "method": "POST",
  "path": "/venue-maps/{mapId}/paths/{pathId}/closure",
  "contract": "venue-map",
  "summary": "Close a route during works or an incident",
  "permission": "VENUE_MAP_MANAGE",
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
  "responds": "PathClosureResult"
 },
 "setRecipe": {
  "method": "PUT",
  "path": "/recipes",
  "contract": "fnb",
  "summary": "Define a recipe for a menu item",
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
  "requestBody": "Recipe",
  "responds": "Recipe"
 },
 "setSubstitutionRules": {
  "method": "PUT",
  "path": "/substitution-rules",
  "contract": "fnb",
  "summary": "What may replace what",
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
  "requestBody": null,
  "responds": "SubstitutionRule"
 },
 "syncOrders": {
  "method": "POST",
  "path": "/sync/orders",
  "contract": "orders",
  "summary": "Replay orders recorded offline",
  "permission": "ORDER_CREATE",
  "offlineCapable": false,
  "conflictPolicy": "append",
  "scopeLevel": "workstation",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "OrderSyncResult"
 },
 "updateEvent": {
  "method": "PATCH",
  "path": "/events/{eventId}",
  "contract": "catalogue",
  "summary": "Amend an event",
  "permission": "EVENT_CONFIGURE",
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
  "responds": "Event"
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
   },
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Menu"
 },
 "updateOutlet": {
  "method": "PATCH",
  "path": "/outlets/{outletId}",
  "contract": "tenancy",
  "summary": "Amend an outlet",
  "permission": "REGION_CONFIGURE",
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
  "responds": "Outlet"
 },
 "updatePerformance": {
  "method": "PATCH",
  "path": "/performances/{performanceId}",
  "contract": "catalogue",
  "summary": "Amend a performance",
  "permission": "PERFORMANCE_CONFIGURE",
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
  "responds": "Performance"
 },
 "updateSaleBoard": {
  "method": "PUT",
  "path": "/sale-boards/{saleBoardId}",
  "contract": "tenancy",
  "summary": "Update a sale board",
  "permission": "WORKSTATION_CONFIGURE",
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
  "requestBody": "SaleBoard",
  "responds": "SaleBoard"
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
 "AccessAccreditationCredential": {
  "type": "object",
  "x-ticvai-persistence": "access.accreditation_credential",
  "x-ticvai-agreed": "29 September: build pass (group OWN, from group RA's handoff; BL-181); the events accreditation.credentialIssued and accreditation.holderStatusChanged name access as their critical consumer",
  "description": "**What a gate needs to admit an accredited person, kept by `access`** (29 September, build). Written only by the consumers of `accreditation.credentialIssued` (a row per credential; a replacement sets the replaced row's `admits` false) and `accreditation.holderStatusChanged` (every credential of the holder: `admits` false unless the holder is `active`, validity taken from the event). Read by `validateAccess` and shipped in the offline package. The record of truth stays in `accreditation`; this is a copy shaped for the gate, never edited by a person.",
  "required": [
   "id",
   "holderId",
   "encodedIdentifier",
   "admits",
   "scopePath"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "The accreditation credential's id (`credentialId` on the events)."
   },
   "holderId": {
    "type": "string",
    "format": "uuid"
   },
   "programmeId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "kind": {
    "type": "string",
    "description": "printedBadge, mobileCredential, qr, nfcCard, rfidCard or wristband, as issued."
   },
   "encodedIdentifier": {
    "type": "string",
    "x-ticvai-unique": "tenant",
    "description": "What the gate reads from the credential. Never sent to webhook subscribers."
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
   },
   "zoneIds": {
    "type": "array",
    "description": "The holder's effective zones, from the event (`effectiveZones`).",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "holderStatus": {
    "type": "string",
    "enum": [
     "active",
     "suspended",
     "revoked",
     "expired",
     "archived"
    ],
    "description": "The holder's status as last published; only `active` admits."
   },
   "admits": {
    "type": "boolean",
    "description": "False once the credential is replaced or the holder is not active."
   },
   "sourceChangedAt": {
    "type": "string",
    "format": "date-time",
    "description": "The `issuedAt` or `changedAt` of the event last applied; an older event arriving late is ignored."
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005), the accreditation programme's scope."
   }
  }
 },
 "AccessDynamicPolicy": {
  "type": "object",
  "x-ticvai-persistence": "access.dynamic_policy",
  "description": "One guest-admission dynamic (attribute-based) policy with its current content - type, context or identity it tests, condition expression, result, priority, zones, validity, status and current version. Not identity.authorisation_policy, which is staff permission (declared 29 September, data-model close-out DM1).\n\n**Guest admission lives here and nowhere else** (ADR-0068, accepted 1 October). `validateAccess` online and the gate offline evaluate the same active version: `getOfflinePackage` carries it, and every `scan_event` records the policy and version that decided it (`dynamicPolicyId`, `dynamicPolicyVersion`) and the set it was decided under (`policySetVersion`). The condition is `conditionRule`, a closed JSON format (`AdmissionRule`), not free text. Identity's staff-permission engine was renamed `AuthorisationPolicy` on the same day, so \"access policy\" means this.\n\n**Which of the two policy engines this is** (stated 29 September, build pass). **This one governs who may pass which gate**: admission of a guest, pass holder, accreditation holder or employee at an access point, decided in validation with results a gate acts on (allow, deny, review, requireId, requireBiometric, requireCompanion, requireSupervisor). **identity `AuthorisationPolicy` governs who may do what in the software**: a principal's permissions on operations and screens, decided by identity `evaluateAccess`. An employee's badge opening a staff door is decided here; the same employee approving a refund is decided in identity. Effectiveness is reported per engine: `listDynamicPolicyEffectiveness` here, `listAuthorisationPolicyEffectiveness` in identity.",
  "required": [
   "id",
   "scopePath",
   "name",
   "policyType",
   "conditionRule",
   "result",
   "status",
   "currentVersion"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "The policyId"
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "scopePath": {
    "type": "string",
    "description": "ltree of the owning scope node; where it applies further is access.policy_scope_assignment"
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "policyType": {
    "type": "string",
    "enum": [
     "guestAttribute",
     "accreditation",
     "occupancy",
     "employee",
     "risk",
     "membership",
     "timeEvent"
    ]
   },
   "contextType": {
    "type": "string",
    "enum": [
     "date",
     "day",
     "time",
     "season",
     "event",
     "performance",
     "specialEvent",
     "holiday",
     "operatingCalendar",
     "occupancy",
     "attractionStatus"
    ],
    "nullable": true,
    "description": "Context/time/event policies (setContextTimeEvent)"
   },
   "identityType": {
    "type": "string",
    "enum": [
     "guest",
     "member",
     "annualPassHolder",
     "employee",
     "contractor",
     "vendor",
     "performer",
     "media",
     "vip",
     "security",
     "emergencyServices",
     "eventStaff"
    ],
    "nullable": true,
    "description": "Identity-based policies (listIdentityMembershipAccreditation)"
   },
   "conditionRule": {
    "$ref": "#/components/schemas/AdmissionRule",
    "description": "The condition, in the closed JSON rule format evaluated the same way online and at the gate (ADR-0068; replaces the free-text `conditionExpression`)."
   },
   "result": {
    "type": "string",
    "enum": [
     "allow",
     "deny",
     "review",
     "requireId",
     "requireBiometric",
     "requireCompanion",
     "requireSupervisor"
    ]
   },
   "priority": {
    "type": "integer",
    "nullable": true
   },
   "allowedZoneIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "deniedZoneIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "monitorThresholdPercent": {
    "type": "integer",
    "minimum": 0,
    "maximum": 100,
    "nullable": true,
    "description": "Occupancy policies. Percent at which the band becomes Monitor"
   },
   "restrictThresholdPercent": {
    "type": "integer",
    "minimum": 0,
    "maximum": 100,
    "nullable": true,
    "description": "Occupancy policies. Percent at which the band becomes Restrict"
   },
   "validFrom": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "validTo": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "The grant expires automatically at validTo"
   },
   "status": {
    "type": "string",
    "enum": [
     "draft",
     "pendingApproval",
     "active",
     "inactive",
     "expired"
    ],
    "default": "draft"
   },
   "currentVersion": {
    "type": "integer",
    "minimum": 1,
    "description": "The version in force (access.dynamic_policy_version)"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "AcquireLeaseRequest": {
  "type": "object",
  "description": "The body of `acquireInventoryHold`. **Named before the 26 August rename** (lease to `InventoryHold`); the name stays because generated code is keyed on it.",
  "required": [
   "id",
   "channelCapacityId",
   "requestedUnits",
   "ttlSeconds"
  ],
  "properties": {
   "holderKind": {
    "$ref": "#/components/schemas/InventoryHoldHolderKind"
   },
   "cartId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Required when `holderKind` is `cart`, else `400`. Sent by the order service from `orders.addCartLine` (SD-023, 29 September)."
   },
   "channel": {
    "allOf": [
     {
      "$ref": "#/components/schemas/Channel"
     }
    ],
    "description": "Which channel's allocation to draw from. Defaults to the session's channel. A lease is granted against a channel allocation, not against raw capacity.\n"
   },
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "Client-generated UUIDv7. Also the idempotency key."
   },
   "channelCapacityId": {
    "type": "string",
    "format": "uuid"
   },
   "requestedUnits": {
    "type": "integer",
    "minimum": 1
   },
   "ttlSeconds": {
    "type": "integer",
    "minimum": 30,
    "maximum": 3600,
    "default": 900,
    "description": "Short TTLs limit stranding when a terminal dies; long TTLs survive longer outages. The venue's default balances the two: **15 minutes (900 seconds), from the venue setting `cartLeaseSeconds`** with a tenant default (decided 28 September, audit R169; proposed, client to correct under audit R094).\n"
   }
  }
 },
 "AiRecommendationItem": {
  "type": "object",
  "x-ticvai-persistence": "none — held in jsonb on ai.rec_decision.items, through AiRecommendationItemList",
  "description": "One recommended item. **Carries a Pricing price reference, never a computed price** (AIR-029).",
  "required": [
   "trackingId",
   "rank"
  ],
  "properties": {
   "trackingId": {
    "type": "string",
    "format": "uuid",
    "description": "Echoed on every `recordRecommendationEvents` event and as `orders.addCartLine.recommendationId`, so attribution never guesses."
   },
   "productId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The product recommended. **Exactly one of `productId`, `promotionId` or `couponRef`, `rewardId` or `challengeId` is set, by `kind`** (29 September, build): `offer` carries a promotion or coupon, `reward` a loyalty reward, `challenge` a challenge, every other kind a product."
   },
   "promotionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "For `offer`, a published promotion the guest is eligible for. Promotions computes the discount at the basket, never the engine."
   },
   "couponRef": {
    "type": "string",
    "nullable": true,
    "description": "For `offer`, a coupon campaign; a code is assigned only when the guest takes it (`promotions.assignCoupon`)."
   },
   "rewardId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "For `reward`, a marketing-crm loyalty reward the guest can redeem."
   },
   "challengeId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "For `challenge`, a marketing-crm challenge the guest can join."
   },
   "kind": {
    "type": "string",
    "enum": [
     "upsell",
     "crossSell",
     "upgrade",
     "bundle",
     "addOn",
     "membership",
     "nextBestOffer",
     "offer",
     "reward",
     "challenge"
    ]
   },
   "rank": {
    "type": "integer",
    "minimum": 1
   },
   "priceRef": {
    "type": "string",
    "nullable": true,
    "description": "The Pricing reference the channel resolves to a price. AI never computes a price."
   },
   "reasonTemplateKey": {
    "type": "string",
    "nullable": true,
    "description": "The template reason (decided 29 September, decision 9): no model writes guest-visible reasons."
   },
   "reasonText": {
    "type": "string",
    "nullable": true,
    "description": "The rendered template in the session locale, where the channel shows reasons."
   },
   "confidenceBand": {
    "type": "string",
    "enum": [
     "high",
     "medium",
     "low"
    ],
    "description": "Design 5.6: a band, never a bare percentage."
   },
   "score": {
    "type": "number",
    "nullable": true,
    "description": "Normalised score. **Returned to staff callers only**; a guest response omits it."
   }
  }
 },
 "AiRecommendationResult": {
  "type": "object",
  "x-ticvai-persistence": "none — written as ai.rec_decision after the response",
  "description": "The recommendation slot's content (design 2.2 A). Empty `items` is a valid answer: the slot stays empty.",
  "required": [
   "decisionId",
   "mode",
   "items",
   "expiresAt"
  ],
  "properties": {
   "decisionId": {
    "type": "string",
    "format": "uuid"
   },
   "placement": {
    "type": "string",
    "enum": [
     "productPage",
     "cart",
     "checkout",
     "postPurchase",
     "preVisit",
     "inVenue",
     "posBasket",
     "kioskBasket",
     "fnbMenu",
     "retailBasket",
     "seatUpgrade",
     "membership",
     "email",
     "homepage",
     "loyalty"
    ]
   },
   "mode": {
    "type": "string",
    "enum": [
     "personalised",
     "contextual",
     "rulesOnly",
     "fallback"
    ]
   },
   "items": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/AiRecommendationItem"
    }
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
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
 "BundleSummary": {
  "x-ticvai-persistence": "none — projection over bundle",
  "type": "object",
  "description": "One published catalogue bundle — the signed snapshot terminals pull (ADR-0013). Not `promotions.Bundle`, which is a sellable product made of other products.",
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
 "CatalogueBundle": {
  "x-ticvai-persistence": "catalogue.published_bundle",
  "type": "object",
  "required": [
   "version",
   "venueId",
   "isDelta",
   "signature",
   "signatureKeyId",
   "contentHash",
   "staleAfter",
   "payload"
  ],
  "properties": {
   "version": {
    "type": "string"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "isDelta": {
    "type": "boolean"
   },
   "baseVersion": {
    "type": "string",
    "nullable": true,
    "description": "Present when `isDelta`. The version this delta applies to."
   },
   "signature": {
    "type": "string",
    "description": "Detached signature over `contentHash`. The terminal verifies before applying and rolls back on failure — a half-applied catalogue is never traded against.\n"
   },
   "signatureKeyId": {
    "type": "string"
   },
   "contentHash": {
    "type": "string"
   },
   "staleAfter": {
    "type": "string",
    "format": "date-time"
   },
   "payload": {
    "type": "object",
    "description": "Products, variants, price lists, prices, tax codes, events, performances, envelope definitions, data mask field definitions and the venue's sale boards. Shape is versioned with the bundle format, not with this API.\n",
    "additionalProperties": true,
    "properties": {
     "saleBoards": {
      "type": "array",
      "description": "**The venue's sale boards as `tenancy.listSaleBoards` returns them**, read from `platform.sale_board` when the bundle is snapshotted (decided 28 September, audit R129 (4)). A board changed by `updateSaleBoard` reaches terminals here, with the next bundle, and never mid-transaction.\n",
      "items": {
       "type": "object",
       "additionalProperties": true
      }
     }
    }
   }
  }
 },
 "CatalogueState": {
  "x-ticvai-persistence": "none — computed from workstation bundle_version",
  "type": "object",
  "description": "The workstation's local catalogue position. A terminal beyond `staleAfter` must refuse to trade rather than transact against stale prices.\n",
  "required": [
   "appliedBundleVersion",
   "appliedAt",
   "staleAfter",
   "isStale"
  ],
  "properties": {
   "appliedBundleVersion": {
    "type": "string"
   },
   "appliedAt": {
    "type": "string",
    "format": "date-time"
   },
   "staleAfter": {
    "type": "string",
    "format": "date-time",
    "description": "Beyond this the terminal refuses to trade."
   },
   "isStale": {
    "type": "boolean"
   },
   "pendingBundleVersion": {
    "type": "string",
    "nullable": true,
    "description": "Published but not yet applied."
   }
  }
 },
 "Channel": {
  "type": "string",
  "enum": [
   "pos",
   "kiosk",
   "web",
   "mobile",
   "b2b",
   "ota",
   "callCentre"
  ]
 },
 "CreateEventRequest": {
  "type": "object",
  "required": [
   "code",
   "name",
   "venueId"
  ],
  "properties": {
   "code": {
    "type": "string",
    "maxLength": 64,
    "x-ticvai-unique": "tenant",
    "description": "**Unique per tenant** (decided 28 September, audit R108). A code already used by any event in the tenant is refused with `409 duplicate-code`.\n"
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "parentEventId": {
    "type": "string",
    "format": "uuid"
   }
  }
 },
 "CreateOrderRequest": {
  "type": "object",
  "required": [
   "id",
   "venueId",
   "channel",
   "lines",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "Client-generated UUIDv7. Also the idempotency key: it must equal the `Idempotency-Key` header, and a replay or a mismatch follows `IdempotencyKey` in `shared/common.yaml`. Offline replay through `syncOrders` carries no header, and this id alone deduplicates there.\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "channel": {
    "$ref": "#/components/schemas/Channel"
   },
   "shiftId": {
    "type": "string",
    "format": "uuid"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Null for an anonymous sale. Identity and entitlement are separate."
   },
   "guestLinkId": {
    "type": "string",
    "nullable": true,
    "description": "Present where the guest is linked across cells."
   },
   "catalogueBundleVersion": {
    "type": "string",
    "description": "The bundle the client priced from. Lets the server explain a variance rather than merely report one.\n"
   },
   "lines": {
    "type": "array",
    "minItems": 1,
    "items": {
     "$ref": "#/components/schemas/CreateOrderLine"
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
    "format": "uuid",
    "description": "Client-generated UUIDv7 of the payment, and its idempotency key — it must equal the `Idempotency-Key` header."
   },
   "orderId": {
    "type": "string",
    "format": "uuid"
   },
   "tender": {
    "$ref": "#/components/schemas/TenderKind"
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "tenderCurrency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "nullable": true,
    "description": "The currency the guest handed over, where it is not the venue's — becomes `Payment.tenderCurrency`. Omit for a payment in the venue's own currency."
   },
   "tenderAmount": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "**What the guest handed over**, in `tenderCurrency` — becomes `Payment.tenderAmount`, one name for one concept (renamed from `tenderedAmount` on 26 September). For cash, change is the difference.\n"
   },
   "walletAuthorisationId": {
    "type": "string",
    "nullable": true,
    "description": "Cross-cell wallet hold, where the guest's home cell is elsewhere."
   },
   "walletHoldId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "For a `wallet` tender, the hold `wallet.holdWalletFunds` placed (SD-027). Capture debits it; the order service writes no wallet table."
   },
   "returnUrl": {
    "type": "string",
    "format": "uri",
    "nullable": true,
    "description": "Where the provider returns the guest after a 3-D Secure challenge or hosted page (SD-034). Required for a card payment from the guest web or app."
   },
   "terminalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The card terminal to instruct, for a card payment at a till (ECR flow, SD-034)."
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
 "CreatePerformancesRequest": {
  "type": "object",
  "required": [
   "startsAt",
   "endsAt"
  ],
  "properties": {
   "startsAt": {
    "type": "string",
    "format": "date-time"
   },
   "endsAt": {
    "type": "string",
    "format": "date-time"
   },
   "admissionRulesId": {
    "type": "string",
    "format": "uuid"
   },
   "seatMapId": {
    "type": "string",
    "format": "uuid"
   },
   "language": {
    "type": "string",
    "nullable": true,
    "maxLength": 35,
    "pattern": "^[A-Za-z]{2,3}(-[A-Za-z0-9]{1,8})*$",
    "description": "As `Performance.language`; every performance of a generated series takes it (decided 29 September, rev 3 REV3-17)."
   },
   "format": {
    "type": "string",
    "nullable": true,
    "maxLength": 40,
    "description": "As `Performance.format` (decided 29 September, rev 3 REV3-17)."
   },
   "recurrence": {
    "type": "object",
    "description": "Generate a series rather than a single performance. **Read in the region's time zone**: the Region owns the zone and every venue inherits it without override (tenancy), so `daysOfWeek` are the region's calendar days and `until` is compared on the region's clock.\n",
    "properties": {
     "intervalMinutes": {
      "type": "integer",
      "minimum": 1
     },
     "until": {
      "type": "string",
      "format": "date-time"
     },
     "daysOfWeek": {
      "type": "array",
      "items": {
       "type": "integer",
       "minimum": 0,
       "maximum": 6
      }
     }
    }
   }
  }
 },
 "DeploymentProfile": {
  "type": "string",
  "description": "How this workstation obtains catalogue and inventory (ADR-0013).\n- `terminalLocal` — own SQLite, leases direct from the cell. Small venues, 4G sites - `venueEdge` — own SQLite, distributed via the venue edge node which holds the\n  venue lease and sub-leases to terminals. Mid and large venues, stadium gates\n- `thin` — no local catalogue, server reads. Non-transactional surfaces only\n",
  "enum": [
   "terminalLocal",
   "venueEdge",
   "thin"
  ]
 },
 "DeviceBinding": {
  "x-ticvai-persistence": "platform.device",
  "type": "object",
  "required": [
   "kind",
   "driver"
  ],
  "properties": {
   "kind": {
    "$ref": "#/components/schemas/DeviceKind"
   },
   "driver": {
    "type": "string",
    "description": "Driver identifier. Adding a vendor is a driver plus configuration, never a core change — every venue arrives with hardware not previously seen.\n"
   },
   "identifier": {
    "type": "string",
    "description": "Serial",
    "port or network address.": null
   },
   "isRequired": {
    "type": "boolean",
    "default": false,
    "description": "When true, the workstation refuses to open a shift if the device is absent.\n"
   }
  }
 },
 "Event": {
  "x-ticvai-persistence": "catalogue.event",
  "type": "object",
  "required": [
   "id",
   "code",
   "name",
   "venueId",
   "scopePath"
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
   "scopePath": {
    "type": "string"
   },
   "parentEventId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "For grouped events."
   },
   "performanceCount": {
    "type": "integer",
    "readOnly": true,
    "description": "How many performances the event has. Counted by the server; never sent by a client."
   },
   "isActive": {
    "type": "boolean"
   }
  }
 },
 "FnbIngredientSubstitute": {
  "type": "object",
  "x-ticvai-persistence": "fnb.ingredient_substitute",
  "description": "**Taken from the backend workbook, 20 September.** Defines approved ingredient substitutions for F&B preparation.",
  "required": [
   "fromInventoryItemId",
   "toInventoryItemId",
   "substitutionRatio",
   "requiresApproval",
   "isActive",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "fromInventoryItemId": {
    "type": "string",
    "format": "uuid"
   },
   "toInventoryItemId": {
    "type": "string",
    "format": "uuid"
   },
   "substitutionRatio": {
    "type": "number"
   },
   "conditionsJson": {
    "type": "string",
    "nullable": true
   },
   "allergensAddedJson": {
    "type": "string",
    "nullable": true
   },
   "allergensRemovedJson": {
    "type": "string",
    "nullable": true
   },
   "requiresApproval": {
    "type": "boolean"
   },
   "isActive": {
    "type": "boolean"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "InventoryHold": {
  "x-ticvai-persistence": "catalogue.inventory_hold",
  "type": "object",
  "required": [
   "id",
   "channelCapacityId",
   "holderKind",
   "grantedUnits",
   "consumedUnits",
   "status",
   "acquiredAt",
   "expiresAt"
  ],
  "properties": {
   "id": {
    "type": "string"
   },
   "channelCapacityId": {
    "type": "string",
    "format": "uuid"
   },
   "holderKind": {
    "$ref": "#/components/schemas/InventoryHoldHolderKind"
   },
   "holderWorkstationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The holding workstation when `holderKind` is `workstation`; null on a cart hold, because a browser has none (SD-023, 29 September)."
   },
   "holderCartId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The holding cart (`orders.cart`) when `holderKind` is `cart` (SD-023, 29 September)."
   },
   "convertedOrderId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "The paid order the hold was converted for, set by `convertInventoryHold`."
   },
   "convertedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "parentLeaseId": {
    "type": "string",
    "nullable": true,
    "description": "Present when sub-leased from a venue edge node."
   },
   "requestedUnits": {
    "type": "integer"
   },
   "channel": {
    "allOf": [
     {
      "$ref": "#/components/schemas/Channel"
     }
    ],
    "description": "Allocation this lease draws from."
   },
   "grantedUnits": {
    "type": "integer",
    "description": "May be less than requested — a partial grant is not an error. Constrained by the channel's remaining allocation plus the general pool, never by raw capacity.\n"
   },
   "consumedUnits": {
    "type": "integer"
   },
   "status": {
    "$ref": "#/components/schemas/LeaseStatus"
   },
   "acquiredAt": {
    "type": "string",
    "format": "date-time"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time"
   },
   "releasedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "forceReleasedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "forceReleaseReason": {
    "type": "string",
    "nullable": true
   }
  }
 },
 "InventoryHoldHolderKind": {
  "type": "string",
  "enum": [
   "workstation",
   "cart"
  ],
  "default": "workstation",
  "description": "**Who holds the units** (decided 29 September, SD-023). A till, kiosk or edge node holds as a `workstation`; a guest's web or app cart holds as a `cart`, acquired by the order service. A browser has no workstation, so a cart hold carries `cartId` and no `holderWorkstationId`.\n"
 },
 "LeaseStatus": {
  "type": "string",
  "description": "`states/lease.yaml`. **`expired` is set by that model's timer transition when `expiresAt` passes without a renewal**, not by any operation in this contract. The job that runs the timer is the sweeper ADR-0037 deferred: it returns an expired hold's unconsumed units to `remaining` in the same guarded statement as a release (SD-023, 29 September), and **writes `inventoryHold.expired` to the outbox in the same transaction** (SD-023/SD-033, applied 30 September; `events/inventoryHold-expired.yaml`), so the cart that held the units hears of it before checkout. A `converted` hold is never swept.\n**`converted` is set by `convertInventoryHold`** when the order that holds the units is paid (decided 29 September, SD-023); its units are `sold` and the sweeper never touches it.\n",
  "enum": [
   "active",
   "expired",
   "released",
   "forceReleased",
   "converted"
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
 "OfflineOrder": {
  "x-ticvai-persistence": "none — client-side journal, not server storage",
  "allOf": [
   {
    "$ref": "#/components/schemas/CreateOrderRequest"
   },
   {
    "type": "object",
    "required": [
     "sequence",
     "payments"
    ],
    "properties": {
     "sequence": {
      "type": "integer",
      "minimum": 1,
      "description": "Monotonic per device. Processed in this order."
     },
     "payments": {
      "type": "array",
      "items": {
       "$ref": "#/components/schemas/CreatePaymentRequest"
      }
     }
    }
   }
  ]
 },
 "OfflinePackage": {
  "x-ticvai-persistence": "none — generated artefact in object storage",
  "type": "object",
  "required": [
   "etag",
   "generatedAt",
   "validFrom",
   "validTo",
   "accessPointId",
   "entitlements"
  ],
  "properties": {
   "etag": {
    "type": "string"
   },
   "generatedAt": {
    "type": "string",
    "format": "date-time"
   },
   "validFrom": {
    "type": "string",
    "format": "date-time"
   },
   "validTo": {
    "type": "string",
    "format": "date-time"
   },
   "accessPointId": {
    "type": "string",
    "format": "uuid"
   },
   "entitlementsVersion": {
    "type": "integer",
    "description": "The highest `access.entitlement` change included (SD-052, 29 September). A refresh sends it as `sinceVersion` and receives only what changed after it, so a 60,000-guest venue is not re-sent whole."
   },
   "policySetVersion": {
    "type": "string",
    "description": "**The active admission policy version the package carries** (ADR-0068, 1 October): a fingerprint of the `(id, currentVersion)` of every policy in `dynamicPolicies`, computed the same way by `validateAccess` online. Every scan the gate records carries it (`ScanEvent.policySetVersion`), so a scan decided offline under a set that has since changed is visible at sync rather than assumed equal."
   },
   "dynamicPolicies": {
    "type": "array",
    "description": "The active guest-admission dynamic policies for this access point's zones (SD-052), each at its active version with its `conditionRule` (ADR-0068), so an offline gate applies the same rules as an online one.",
    "items": {
     "$ref": "#/components/schemas/AccessDynamicPolicy"
    }
   },
   "entitlements": {
    "type": "array",
    "description": "Read from `access.entitlement` (SD-052). With `sinceVersion`, only the rows changed after it, including ones now void or used, so a device removes them.",
    "items": {
     "type": "object",
     "required": [
      "ticketId",
      "mediaCodes",
      "validFrom",
      "validTo",
      "entriesAllowed",
      "reentryAllowed"
     ],
     "properties": {
      "ticketId": {
       "type": "string",
       "format": "uuid",
       "description": "The `Entitlement.id`."
      },
      "mediaCodes": {
       "type": "array",
       "items": {
        "type": "string"
       },
       "description": "A ticket may carry several media over its life."
      },
      "validFrom": {
       "type": "string",
       "format": "date-time"
      },
      "validTo": {
       "type": "string",
       "format": "date-time"
      },
      "performanceId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "entriesAllowed": {
       "type": "integer",
       "nullable": true
      },
      "entriesUsed": {
       "type": "integer"
      },
      "reentryAllowed": {
       "type": "boolean"
      },
      "admissionRulesId": {
       "type": "string",
       "format": "uuid"
      }
     }
    }
   },
   "delegatedRights": {
    "type": "array",
    "description": "Redemption rights issued by other cells and valid at this access point. Included in the package so a cross-region entitlement still admits when the inter-cell link is down — the same reason locally issued entitlements are included.\n",
    "items": {
     "type": "object",
     "required": [
      "rightId",
      "ticketId",
      "issuingCellId",
      "validFrom",
      "validTo",
      "entriesAllowed",
      "entriesConsumed"
     ],
     "properties": {
      "rightId": {
       "type": "string"
      },
      "ticketId": {
       "type": "string",
       "format": "uuid",
       "description": "The `Entitlement.id` in the issuing cell."
      },
      "issuingCellId": {
       "type": "string"
      },
      "guestLinkId": {
       "type": "string",
       "nullable": true
      },
      "mediaCodes": {
       "type": "array",
       "items": {
        "type": "string"
       }
      },
      "validFrom": {
       "type": "string",
       "format": "date-time"
      },
      "validTo": {
       "type": "string",
       "format": "date-time"
      },
      "entriesAllowed": {
       "type": "integer",
       "nullable": true
      },
      "entriesConsumed": {
       "type": "integer"
      },
      "admissionRulesId": {
       "type": "string",
       "format": "uuid"
      }
     }
    }
   },
   "blacklist": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Media codes to deny outright regardless of entitlement state."
   },
   "admissionRules": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "id",
      "openMinutesBefore",
      "closeMinutesAfter"
     ],
     "properties": {
      "id": {
       "type": "string",
       "format": "uuid"
      },
      "openMinutesBefore": {
       "type": "integer"
      },
      "closeMinutesAfter": {
       "type": "integer"
      },
      "maxDurationMinutes": {
       "type": "integer",
       "nullable": true
      },
      "requiresExitBeforeReentry": {
       "type": "boolean"
      }
     }
    }
   },
   "accreditationCredentials": {
    "type": "array",
    "description": "Accreditation credentials that admit at this access point, from access.accreditation_credential (29 September, build; BL-181). Only rows that admit are included; a credential dropped from one package to the next no longer admits.",
    "items": {
     "$ref": "#/components/schemas/AccessAccreditationCredential"
    }
   }
  }
 },
 "OfflinePolicy": {
  "type": "object",
  "x-ticvai-persistence": "platform.offline_policy",
  "description": "Board 5 of the client's POS set. **ADR-0013 makes the POS local-first and nothing configured the policy** — one of only two things in 36 board screens the package genuinely could not do.\nCF-115 reframed offline into three data classes: catalogue and policy always local, contended inventory leased, transactional facts journalled. **This is where a venue says how far that goes for them.**\n**One per scope node, keyed on `scopePath`** (pull audit R162). `id` is server-owned and absent where `getOfflinePolicy` returns the defaults for a node with nothing saved.\n**The `minimum` and `maximum` on each field are proposed, client to correct (decided 28 September, audit R129).** A value outside them is refused `400`, `errors[]` naming the field.\n",
  "required": [
   "scopePath"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "pattern": "^[a-z0-9_]+(\\.[a-z0-9_]+)*$",
    "description": "**The node this policy is for, and the key `setOfflinePolicy` upserts on.** The body names its target here, because the path does not.\n"
   },
   "maxOfflineHours": {
    "type": "integer",
    "default": 24,
    "minimum": 1,
    "maximum": 72,
    "description": "**After which the workstation refuses to sell rather than keep journalling.** A till three days offline holding 900 unsynced sales is a reconciliation nobody can do and a fraud nobody can detect. Bounds 1 to 72 hours: proposed, client to correct (audit R129).\n"
   },
   "allowedOffline": {
    "type": "array",
    "description": "**What may happen with no network**, by data class. Selling from a cached catalogue is safe; issuing a refund is not, because the original sale cannot be verified.\n",
    "items": {
     "type": "string",
     "enum": [
      "sale",
      "refund",
      "exchange",
      "entitlementIssue",
      "entitlementValidate",
      "loyaltyAccrual",
      "loyaltyRedemption",
      "walletSpend",
      "priceOverride",
      "discount",
      "voidLine",
      "noSale"
     ]
    }
   },
   "offlineValueCeiling": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Above zero, and in the currency of the venue the policy resolves to; a ceiling in another currency is refused `400` (decided 28 September, audit R129).\n"
   },
   "offlineTransactionCeiling": {
    "type": "integer",
    "nullable": true,
    "minimum": 1,
    "maximum": 5000,
    "description": "**A ceiling on count as well as value.** Nine hundred small sales and one large one are different risks, and a value ceiling alone catches only the second. Bounds 1 to 5,000: proposed, client to correct (audit R129).\n"
   },
   "onCeilingBreach": {
    "type": "string",
    "enum": [
     "warn",
     "blockNewSales",
     "blockAll"
    ],
    "default": "blockNewSales"
   },
   "requiresManagerToExtend": {
    "type": "boolean",
    "default": true
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
 "OrderSyncResult": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "accepted",
   "results"
  ],
  "properties": {
   "accepted": {
    "type": "integer"
   },
   "stoppedAtSequence": {
    "type": "integer",
    "nullable": true,
    "description": "First entry that hit a **transient** failure (SD-028, 29 September): a refusal on the merits no longer stops the batch. Null when every entry was accepted, duplicate or quarantined. The client retries from here and never past it.\n"
   },
   "results": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "id",
      "sequence",
      "status"
     ],
     "properties": {
      "id": {
       "type": "string",
       "format": "uuid",
       "description": "The `OfflineOrder.id` this result is about."
      },
      "sequence": {
       "type": "integer"
      },
      "status": {
       "type": "string",
       "enum": [
        "accepted",
        "duplicate",
        "rejected",
        "blockedByRejection"
       ],
       "description": "`rejected`: refused on its merits and quarantined in `sync.rejection`; the batch continues. `blockedByRejection`: depends on a rejected entry for the same order (a void, a refund, a later payment) and is quarantined with it (SD-028, 29 September)."
      },
      "orderNumber": {
       "type": "string",
       "nullable": true
      },
      "priceVariance": {
       "allOf": [
        {
         "$ref": "../shared/common.yaml#/components/schemas/Money"
        }
       ],
       "description": "Posted to the variance account. Not surfaced to the cashier."
      },
      "varianceExceedsThreshold": {
       "type": "boolean",
       "description": "True when review is required per the venue's variance threshold."
      },
      "rejectionId": {
       "type": "string",
       "nullable": true,
       "description": "For a `rejected` or `blockedByRejection` entry, the `sync.rejection` row it was quarantined into (SD-028). The batch carried on past it."
      },
      "error": {
       "$ref": "../shared/common.yaml#/components/schemas/Problem"
      }
     }
    }
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
 "PathClosureResult": {
  "description": "What `setPathClosure` returns: the path, and **what a forced closure cut off**, named.\n",
  "allOf": [
   {
    "$ref": "#/components/schemas/VenuePath"
   },
   {
    "type": "object",
    "properties": {
     "strandedPoints": {
      "type": "array",
      "readOnly": true,
      "description": "Points no longer reachable because of this closure. Empty unless `force` was used.\n",
      "items": {
       "$ref": "#/components/schemas/StrandedPoint"
      }
     }
    }
   }
  ]
 },
 "Performance": {
  "x-ticvai-persistence": "catalogue.performance",
  "type": "object",
  "required": [
   "id",
   "eventId",
   "startsAt",
   "endsAt",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "eventId": {
    "type": "string",
    "format": "uuid"
   },
   "startsAt": {
    "type": "string",
    "format": "date-time"
   },
   "endsAt": {
    "type": "string",
    "format": "date-time"
   },
   "approvalRequestId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "BL-048. **The approval chain and the occurrence lifecycle sat on different entities**, so neither was complete: `states/performance.yaml` models scheduled, onSale, soldOut, suspended, cancelled and completed properly, and nothing said which of those transitions somebody had to sign.\n**Set on the transition that needs it, not on the performance.** Publishing a performance is routine; cancelling one that has sold is the act somebody signs — and binding approval to the whole entity would have required a signature to reschedule a wet Tuesday.\n"
   },
   "requiresApprovalToCancel": {
    "type": "boolean",
    "default": true,
    "description": "**Cancelling a sold performance is the one transition that needs a name against it.** `assessProductChange` already answers how many tickets are affected; this decides who has to look at that number before the button works.\n"
   },
   "status": {
    "type": "string",
    "enum": [
     "scheduled",
     "onSale",
     "soldOut",
     "suspended",
     "cancelled",
     "completed"
    ]
   },
   "admissionRulesId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "seatMapId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "language": {
    "type": "string",
    "nullable": true,
    "maxLength": 35,
    "pattern": "^[A-Za-z]{2,3}(-[A-Za-z0-9]{1,8})*$",
    "description": "The language the performance is given in, as a BCP 47 tag (`en`, `ar`, `fr`, `de`, `zh`, `ru`, `ar-AE`). **A guided tour at 10:00 in French and one at 10:00 in Arabic are two performances**, so a guest who picks a language sees only the tours in it (`listPerformances` `language`). Null when the performance is not language-specific (decided 29 September, rev 3 REV3-17).\n"
   },
   "format": {
    "type": "string",
    "nullable": true,
    "maxLength": 40,
    "description": "How it is presented, free text the venue chooses, e.g. `2D`, `3D`, `IMAX`, `subtitled`. A cinema screening shows language and format together. Null when it does not apply (decided 29 September, rev 3 REV3-17).\n"
   }
  }
 },
 "PerformanceCancellationResult": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "performanceId",
   "dryRun",
   "affectedOrders",
   "refundExposure"
  ],
  "properties": {
   "performanceId": {
    "type": "string",
    "format": "uuid"
   },
   "dryRun": {
    "type": "boolean"
   },
   "affectedOrders": {
    "type": "integer"
   },
   "affectedGuests": {
    "type": "integer"
   },
   "refundExposure": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "What the cancellation costs. Returned before committing, so the person cancelling sees the number at the moment they decide.\n"
   },
   "bulkRefundBatchId": {
    "type": "string",
    "nullable": true,
    "description": "**Null on this response.** The refund batch is created by `orders` when it consumes `performance.cancelled` (F09), after this call has returned, and is queued there for approval — refunds are not issued automatically. Read it from orders, not from here.\n"
   },
   "notificationsQueued": {
    "type": "integer"
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
   "productionPlanId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "The plan whose release created this run. Null for a run planned directly."
   },
   "stationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**The station whose prep list this run is on.** Copied from the plan line on release, where runs are grouped by station (audit R125 (7)).\n"
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
 "Recipe": {
  "x-ticvai-persistence": "fnb.recipe + fnb.recipe_ingredient",
  "type": "object",
  "required": [
   "menuItemId",
   "ingredients"
  ],
  "properties": {
   "menuItemId": {
    "type": "string",
    "format": "uuid"
   },
   "yield": {
    "type": "number",
    "minimum": 0,
    "description": "Portions produced by one execution."
   },
   "ingredients": {
    "type": "array",
    "minItems": 1,
    "items": {
     "type": "object",
     "required": [
      "inventoryItemId",
      "quantity",
      "unit"
     ],
     "properties": {
      "inventoryItemId": {
       "type": "string",
       "format": "uuid"
      },
      "quantity": {
       "type": "number",
       "minimum": 0
      },
      "unit": {
       "type": "string"
      },
      "isOptional": {
       "type": "boolean",
       "default": false
      }
     }
    }
   },
   "costPerPortion": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "readOnly": true,
    "description": "**Computed, never entered** (decided 28 September, audit R125 (9)): the sum of each ingredient quantity at its current inventory cost, divided by `yield`. Recomputed when the recipe or an ingredient cost changes.\n"
   }
  }
 },
 "SaleBoard": {
  "x-ticvai-persistence": "platform.sale_board",
  "type": "object",
  "required": [
   "id",
   "code",
   "name",
   "venueId",
   "kind",
   "pages"
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
    "$ref": "#/components/schemas/SaleBoardKind"
   },
   "pages": {
    "type": "array",
    "minItems": 1,
    "items": {
     "type": "object",
     "required": [
      "name",
      "sortOrder",
      "tiles"
     ],
     "properties": {
      "name": {
       "type": "string"
      },
      "sortOrder": {
       "type": "integer"
      },
      "tiles": {
       "type": "array",
       "items": {
        "type": "object",
        "required": [
         "position",
         "kind"
        ],
        "properties": {
         "position": {
          "type": "integer"
         },
         "kind": {
          "type": "string",
          "enum": [
           "product",
           "category",
           "action",
           "spacer"
          ]
         },
         "variantId": {
          "type": "string",
          "format": "uuid",
          "nullable": true
         },
         "label": {
          "type": "string"
         },
         "colour": {
          "type": "string",
          "nullable": true
         },
         "imageAssetRef": {
          "type": "string",
          "nullable": true
         }
        }
       }
      }
     }
    }
   },
   "isActive": {
    "type": "boolean"
   }
  }
 },
 "SaleBoardKind": {
  "type": "string",
  "enum": [
   "ticketing",
   "fnb",
   "retail",
   "mixed"
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
 "SeatRecommendation": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "seatIds",
   "totalPrice",
   "isContiguous",
   "rank"
  ],
  "properties": {
   "seatIds": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "displayLabels": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "totalPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "categoryId": {
    "type": "string",
    "format": "uuid"
   },
   "isContiguous": {
    "type": "boolean"
   },
   "rank": {
    "type": "integer",
    "description": "Best first."
   },
   "rationale": {
    "type": "string",
    "description": "Why this option was chosen — closest to stage, best value in category, only contiguous block remaining. Shown to a call-centre agent, not the guest.\n"
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
 },
 "StrandedPoint": {
  "type": "object",
  "x-ticvai-persistence": "none — computed from the graph",
  "required": [
   "pointId",
   "name",
   "kind",
   "isCritical"
  ],
  "properties": {
   "pointId": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string"
   },
   "kind": {
    "type": "string"
   },
   "isCritical": {
    "type": "boolean",
    "description": "First aid, an emergency exit or an assembly point, the same set as `GraphValidation.criticalUnreachable`. **The one the operator must read first.**\n"
   }
  }
 },
 "SubstitutionRule": {
  "type": "object",
  "x-ticvai-persistence": "fnb.substitution_rule",
  "description": "Board 2L, 24 August. **What may replace what, and under what conditions.** A kitchen substitutes constantly — a supplier is short, an item is 86'd, a guest asks — and the package had no way to say which swaps are allowed.\n**The rule exists so `verifyAllergens` has something to check against.** A substitution with no rule behind it is a decision made at the pass by whoever is standing there.\n**`allergensAdded` and `allergensRemoved` are the fields this table is for.** Swapping butter for margarine removes dairy and may add soy — **and a dish still labelled dairy-free after a swap nobody checked is the failure this prevents.**\n",
  "required": [
   "id",
   "recipeId",
   "fromIngredientId",
   "toIngredientId"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "recipeId": {
    "type": "string",
    "format": "uuid",
    "description": "**The recipe the rule applies to** (decided 28 September, audit R125 (10)). Not a menu item and not the whole venue: a swap that is safe in one dish is not safe in another.\n"
   },
   "fromIngredientId": {
    "type": "string",
    "format": "uuid"
   },
   "toIngredientId": {
    "type": "string",
    "format": "uuid"
   },
   "ratio": {
    "type": "number",
    "default": 1,
    "description": "**Not always one to one.** Fresh herbs to dried is roughly three to one, and a rule that assumes parity produces a dish nobody would serve.\n"
   },
   "allergensAdded": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/AllergenCode"
    }
   },
   "allergensRemoved": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/AllergenCode"
    }
   },
   "conditions": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "outOfStock",
      "seasonal",
      "guestRequest",
      "costSaving",
      "always"
     ]
    }
   },
   "requiresApproval": {
    "type": "boolean",
    "default": false,
    "description": "**True where the swap changes an allergen.** A chef may substitute freely within a claim; changing the claim is somebody else's decision.\n"
   },
   "isActive": {
    "type": "boolean",
    "default": true
   }
  }
 },
 "SupervisorStepUp": {
  "type": "object",
  "description": "**A supervisor signs the act in place, on the device making the call** (decided 28 September, audit R144). Used where the decision is a same-device step-up rather than an approval request: reopening a shift, recounting a stock count, a retail return above the venue threshold, and (proposed by the coordinator, client to confirm) closing a stock transfer short and cancelling a performance.\n\n**The verification rule, the same on every operation that takes it:** the server checks `credential` against `principalId`; that principal must hold the operation's `x-ticvai-permission` at the operation's scope, must be active at that venue, and must not be the person whose act is being reversed where the operation says so. Any failure is a `403` (`supervisor-step-up-refused`) and nothing is written. **No approval request is raised**, and the operation declares `x-ticvai-step-up: pin`.\n",
  "required": [
   "principalId",
   "credential"
  ],
  "properties": {
   "principalId": {
    "type": "string",
    "format": "uuid",
    "description": "The supervisor signing. Recorded against the act."
   },
   "credential": {
    "type": "string",
    "maxLength": 512,
    "writeOnly": true,
    "description": "The supervisor's staff PIN, as they sign in at a till with it. **A PIN, never a password** (audit R123 (7)). Never stored or returned."
   }
  }
 },
 "SyncRejection": {
  "x-ticvai-persistence": "sync.rejection",
  "type": "object",
  "required": [
   "id",
   "workstationId",
   "kind",
   "rejectedAt",
   "problem"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "workstationId": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "type": "string",
    "enum": [
     "order",
     "payment",
     "refund",
     "void",
     "scan"
    ]
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   },
   "rejectedAt": {
    "type": "string",
    "format": "date-time"
   },
   "problem": {
    "$ref": "../shared/common.yaml#/components/schemas/Problem"
   },
   "payload": {
    "type": "object",
    "additionalProperties": true,
    "description": "**Deliberately open: the journal entry exactly as the till sent it.** Its shape is the request schema for `kind` — an `OfflineOrder` for `order`, a `CreatePaymentRequest` for `payment` — kept verbatim so the supervisor resolves what was actually recorded, not a re-typed copy.\n"
   },
   "resolvedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "resolvedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true
   },
   "resolution": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "enum": [
     "posted",
     "voided",
     "refunded"
    ],
    "description": "What `resolveSyncRejection` recorded. Null while the rejection waits."
   },
   "resolvedRecordId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "The order, void or refund the resolution produced — what stops the entry being posted twice."
   }
  }
 },
 "UpsellPlacement": {
  "type": "string",
  "enum": [
   "productDetail",
   "cart",
   "checkout",
   "postPurchase",
   "atGate",
   "inVenue"
  ]
 },
 "UpsellRule": {
  "x-ticvai-persistence": "promotions.upsell_rule",
  "type": "object",
  "required": [
   "id",
   "name",
   "placement",
   "triggerVariantIds",
   "suggestedVariantIds"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "regionId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "The region that owns the rule. Upsell rules are owned at region and read at venue (decided 28 September, audit R183); set from the caller's region scope on create.\n"
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "placement": {
    "$ref": "#/components/schemas/UpsellPlacement"
   },
   "triggerVariantIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "triggerCategoryIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "suggestedVariantIds": {
    "type": "array",
    "minItems": 1,
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "suggestedBundleId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "channels": {
    "type": "array",
    "description": "Empty applies to every channel. Restriction is opt-in — a rule that fires on the website but not at a counter is a guest experience inconsistency.\n",
    "items": {
     "type": "string"
    }
   },
   "priority": {
    "type": "integer",
    "default": 0
   },
   "maxSuggestions": {
    "type": "integer",
    "default": 3
   },
   "isActive": {
    "type": "boolean"
   }
  }
 },
 "VenuePath": {
  "type": "object",
  "x-ticvai-persistence": "venuemap.path",
  "description": "19.2.56. **The navigation graph.** The map supplies it; routing over it is a client concern, because a phone with the map cached routes offline and a server round-trip per step does not.\n",
  "required": [
   "id",
   "mapId",
   "fromPointId",
   "toPointId"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "mapId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "From the path of the operation that writes the path."
   },
   "fromPointId": {
    "type": "string",
    "format": "uuid"
   },
   "toPointId": {
    "type": "string",
    "format": "uuid"
   },
   "geometry": {
    "type": "string",
    "nullable": true,
    "description": "The centreline this edge follows, as an encoded polyline. **A walkway in a drawing is a polygon and a route is a line down the middle of it**, so extraction thins the polygon to a centreline and splits it at every fork.\nNull where the path was drawn on screen as a straight connection, which is normal for a venue with no walkway layer.\n"
   },
   "distanceMetres": {
    "type": "number",
    "nullable": true,
    "readOnly": true,
    "description": "Computed by the server from `geometry` and the georeference. **Along the centreline, not point to point.** A path that curves round a lake is longer than the distance between its ends, and a guest told 80 metres who walks 200 stops trusting the map.\nRequires a georeference for real units; without one, distances are in drawing units and routing still works because **only the ratios matter to a shortest path.**\n"
   },
   "isStepFree": {
    "type": "boolean",
    "default": true,
    "description": "**The single most important attribute on this object.** A wheelchair user routed up a staircase has been failed by the map, not by the venue.\n"
   },
   "isIndoor": {
    "type": "boolean",
    "default": false
   },
   "restrictedByPointId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**Where a path is one-way, it is because of a thing on it — not because of the path.** Removed `isOneWay` on 18 August: a pedestrian walkway has no direction, and the three cases that look one-way are all a gate or a queue.\nA turnstile is one-way and `access.AccessPoint.direction` already says so. A queue line is one-way and `queue` owns it. **Putting the restriction on the path duplicated both and would have drifted from them** — a gate reconfigured to bidirectional would leave a path still marked one-way, and nothing would have noticed.\nSet where a path passes through an access point. The router reads the direction from the point.\n"
   },
   "closedReason": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "Set by `setPathClosure` during works or an incident, never by sending it here. **A closed path removes routes rather than hiding the path**, so a guest sees why rather than wondering where it went.\n"
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
 },
 "Workstation": {
  "x-ticvai-persistence": "platform.workstation",
  "type": "object",
  "required": [
   "id",
   "code",
   "name",
   "venueId",
   "regionId",
   "scopePath",
   "saleBoard",
   "currency",
   "currencyScale",
   "timeZone"
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
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "regionId": {
    "type": "string",
    "format": "uuid"
   },
   "departmentId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "scopePath": {
    "type": "string"
   },
   "saleBoard": {
    "type": "object",
    "description": "Determines which front end loads. Bound to the workstation, not the role — the F&B terminal opens the F&B board. What the operator may then DO within it is governed by their permissions.\n",
    "required": [
     "id",
     "kind"
    ],
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid"
     },
     "kind": {
      "$ref": "#/components/schemas/SaleBoardKind"
     },
     "name": {
      "type": "string"
     }
    }
   },
   "accessPointId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Inherited from the workstation, never selected by the operator. Null where the workstation is not at an access point.\n"
   },
   "devices": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/DeviceBinding"
    }
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
   "timeZone": {
    "type": "string"
   },
   "deploymentProfile": {
    "$ref": "#/components/schemas/DeploymentProfile"
   },
   "edgeNodeId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Present when `deploymentProfile` is `venueEdge`."
   },
   "healthScore": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "maximum": 100,
    "readOnly": true,
    "description": "Board 1 of the client's POS set. **A number a manager can sort by** — the package held `lastHeartbeatAt` and a heartbeat timestamp is not a score.\nThe client's board shows 1,248 workstations at 96% healthy, and **the value of that figure is that it ranks**: a fleet dashboard exists so somebody can open the worst one first.\n**Derived from its devices, its heartbeat age, its firmware currency and its error rate.** Read-only, because a workstation that could set its own score would.\n**The formula, proposed, client to correct (audit R096 (2)):** score = 40% device online share (the share of its devices reporting online) + 25% heartbeat freshness (100 at one minute old or less, 0 at 15 minutes or more, linear between) + 20% firmware and profile currency (100 on the latest, 50 one version behind, 0 older) + 15% error rate (100 at 0 errors an hour, 0 at 10 or more, linear between), rounded to a whole number. **Below 80 is a warning and below 60 a failure.**\n"
   },
   "configurationProfileId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Which profile this workstation runs, and at which version. **The client's board shows a fleet split four ways — 72% latest, 18.8% one behind, 6.1% outdated** — and the package had a firmware version field and no profile.\n**A profile is what a venue changes; a version is what it deploys.** Conflating them means a venue cannot say *roll the ticketing counters back and leave the kiosks*.\n"
   },
   "catalogueState": {
    "$ref": "#/components/schemas/CatalogueState"
   },
   "offlineCapable": {
    "type": "boolean",
    "description": "Derived from `deploymentProfile`. False only for `thin`. Under local-first, catalogue READS are always local on transactional surfaces; this flag governs whether WRITES can be queued.\n"
   },
   "isActive": {
    "type": "boolean"
   }
  }
 }
}
```
