# P08-sell-02 — P08 · Sell (2 of 4)

**10 screens · 40 operations · 31 schemas · 13 permissions**

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

- **Every control that can be refused must be gated.** 13 permissions apply here:
  `ACCESS_VALIDATE, CAPACITY_CONFIGURE, EVENT_CONFIGURE, ORDER_CREATE, ORDER_VIEW, PERFORMANCE_CONFIGURE, PRODUCT_CONFIGURE, PRODUCT_VIEW, REGION_CONFIGURE, SCOPE_VIEW, TENANT_CONFIGURE, VENUE_MAP_MANAGE`…. A control nobody can use must say so,
  not sit enabled and fail.
- **6 of these operations work offline**: completeProductionRun, getPerformance, getUpsellSuggestions, getVenueSettings, listCatalogueBundles, listPerformances
  — and the rest do not. A surface that looks the same online and off is lying.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-018` | Allocation & Holds | listDetail | 5 | 1 | — |
| `BO-019` | Closures & Blackouts | listDetail | 12 | 1 | — |
| `BO-037` | Offline Package Status | listDetail | 9 | 0 | — |
| `BO-063` | Opening Hours & Calendar | listDetail | 13 | 1 | — |
| `BO-102` | Sell | listDetail | 3 | 0 | — |
| `BO-109` | Menu Builder & POS Layout Designer | listDetail | 3 | 0 | — |
| `BO-110` | Recipe & BOM Management | listDetail | 2 | 0 | — |
| `BO-111` | Ingredient Substitution, Allergen & Nutrition | configEditor | 4 | 0 | — |
| `BO-112` | Production Planning & Production Sheets | configEditor | 1 | 0 | — |
| `BO-113` | Central Kitchen & Commissary Management | configEditor | 2 | 0 | — |

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
    "BO-001",
    "BO-007",
    "BO-008",
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
      "eventId",
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-007",
     "trigger": "Product Directory",
     "carries": [
      "productId"
     ],
     "provenance": "derived — BO-007 declares entryState.params productId, so an edge into it must carry them"
    },
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "carries": [
      "productId",
      "venueId"
     ],
     "provenance": "derived — BO-008 declares entryState.params productId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-009",
     "trigger": "Pricing Rules",
     "carries": [
      "priceListId"
     ],
     "provenance": "derived — BO-009 declares entryState.params priceListId, so an edge into it must carry them"
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
       "kind": "dataTable",
       "label": "Every allocation holds",
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
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected allocation holds",
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
       "label": "Acquire",
       "operation": "acquireInventoryHold",
       "provenance": "contract catalogue.yaml POST /inventory-holds"
      },
      {
       "kind": "destructiveButton",
       "label": "Force",
       "operation": "forceReleaseInventoryHold",
       "provenance": "contract catalogue.yaml POST /inventory-holds/{inventoryHoldId}/force-release"
      },
      {
       "kind": "secondaryButton",
       "label": "Release hold",
       "operation": "relinquishInventoryHold",
       "provenance": "contract catalogue.yaml DELETE /inventory-holds/{inventoryHoldId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Renew",
       "operation": "renewInventoryHold",
       "provenance": "contract catalogue.yaml POST /inventory-holds/{inventoryHoldId}/renew"
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
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listInventoryHolds",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "destructiveButton",
       "derived": true,
       "impliedBy": "relinquishInventoryHold",
       "label": "Release lease",
       "notes": "**Always confirms, never the default focus.** The consequence goes in the body — *cancel 3 orders worth AED 480* is a confirmation, *are you sure* is not.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "acquireInventoryHold",
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
    "id": "confirmForceReleaseInventoryHold",
    "component": "confirmDialog",
    "trigger": "Force",
    "body": "**Names what `forceReleaseInventoryHold` changes and what it leaves alone**, in the consequence rather than the verb. A allocation holds this affects should be identified in the dialog, not just counted.",
    "provenance": "contract catalogue.yaml POST /inventory-holds/{inventoryHoldId}/force-release"
   }
  ],
  "states": {
   "loading": "The allocation holds list.",
   "error": "Could not load. Names which read failed and leaves the allocation holds untouched.",
   "emptyFirstRun": "No allocation holds yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the allocation holds are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
    "BO-008",
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
      "eventId",
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-007",
     "trigger": "Product Directory",
     "carries": [
      "productId"
     ],
     "provenance": "derived — BO-007 declares entryState.params productId, so an edge into it must carry them"
    },
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "carries": [
      "productId",
      "venueId"
     ],
     "provenance": "derived — BO-008 declares entryState.params productId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-009",
     "trigger": "Pricing Rules",
     "carries": [
      "priceListId"
     ],
     "provenance": "derived — BO-009 declares entryState.params priceListId, so an edge into it must carry them"
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
  "gaps": [
   {
    "operation": "getPerformance",
    "why": "**3 declared operations reach no component on this screen**: getPerformance, getSeatAvailability, listEvents. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every closures blackouts",
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
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected closures blackouts",
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
       "label": "Cancel",
       "operation": "cancelPerformance",
       "provenance": "contract catalogue.yaml POST /performances/{performanceId}/cancel"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createEvent",
       "provenance": "contract catalogue.yaml POST /events"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createPerformances",
       "provenance": "contract catalogue.yaml POST /events/{eventId}/performances"
      },
      {
       "kind": "secondaryButton",
       "label": "Recommend",
       "operation": "recommendSeats",
       "provenance": "contract seating.yaml POST /performances/{performanceId}/seat-recommendations"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateEvent",
       "provenance": "contract catalogue.yaml PATCH /events/{eventId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updatePerformance",
       "provenance": "contract catalogue.yaml PATCH /performances/{performanceId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "setPathClosure",
       "provenance": "contract venue-map.yaml POST /venue-maps/{mapId}/paths/{pathId}/closure"
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
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listPerformances",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "destructiveButton",
       "derived": true,
       "impliedBy": "cancelPerformance",
       "label": "Cancel performance",
       "notes": "**Always confirms, never the default focus.** The consequence goes in the body — *cancel 3 orders worth AED 480* is a confirmation, *are you sure* is not.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createEvent",
       "label": "Create event",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "cancelPerformance",
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
    "id": "confirmCancelPerformance",
    "component": "confirmDialog",
    "trigger": "Cancel",
    "body": "**Names what `cancelPerformance` changes and what it leaves alone**, in the consequence rather than the verb. A closures blackouts this affects should be identified in the dialog, not just counted.",
    "provenance": "contract catalogue.yaml POST /performances/{performanceId}/cancel"
   }
  ],
  "states": {
   "loading": "The closures blackouts list.",
   "error": "Could not load. Names which read failed and leaves the closures blackouts untouched.",
   "emptyFirstRun": "No closures blackouts yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the closures blackouts are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPerformances",
    "contract": "catalogue",
    "purpose": "List performances of an event",
    "trigger": "onLoad"
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
    "trigger": "onLoad"
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
    "Event.id",
    "Event.code",
    "Event.name",
    "Event.venueId",
    "Event.scopePath"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-019",
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
    "BO-001",
    "BO-007",
    "BO-008",
    "BO-009",
    "BO-128"
   ],
   "inferred": true,
   "entryFrom": [
    "BO-102"
   ],
   "transitions": [
    {
     "to": "BO-128",
     "trigger": "Live Workstation Health Monitor",
     "provenance": "flow F89 step 1→2",
     "operation": "setOfflinePolicy"
    },
    {
     "to": "BO-001",
     "trigger": "Queue Directory",
     "carries": [
      "eventId",
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-007",
     "trigger": "Product Directory",
     "carries": [
      "productId"
     ],
     "provenance": "derived — BO-007 declares entryState.params productId, so an edge into it must carry them"
    },
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "carries": [
      "productId",
      "venueId"
     ],
     "provenance": "derived — BO-008 declares entryState.params productId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-009",
     "trigger": "Pricing Rules",
     "carries": [
      "priceListId"
     ],
     "provenance": "derived — BO-009 declares entryState.params priceListId, so an edge into it must carry them"
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
  "gaps": [
   {
    "operation": "getOfflinePackage",
    "why": "**3 declared operations reach no component on this screen**: getOfflinePackage, listSyncRejections, listWorkstations. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every offline package status",
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
       "label": "The selected offline package status",
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
       "label": "Publish",
       "operation": "publishBundle",
       "provenance": "contract catalogue.yaml POST /catalogue/bundles"
      },
      {
       "kind": "secondaryButton",
       "label": "Report",
       "operation": "reportBundleApplied",
       "provenance": "contract catalogue.yaml POST /catalogue/bundles/{version}/applied"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "setOfflinePolicy",
       "provenance": "contract tenancy.yaml PUT /offline-policy"
      },
      {
       "kind": "secondaryButton",
       "label": "Sync",
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
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listCatalogueBundles",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "publishBundle",
       "label": "Publish bundle",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "publishBundle",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "publishGate",
       "impliedBy": "publishBundle",
       "notes": "Declares `publishBundle`. **The gate names what the publish will affect before it happens** — a disabled Publish with no reason is the state operators escalate.\n",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The offline package status list.",
   "error": "Could not load. Names which read failed and leaves the offline package status untouched.",
   "emptyFirstRun": "No offline package status yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the offline package status are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
    "CatalogueBundle.venueId",
    "CatalogueBundle.isDelta",
    "CatalogueBundle.baseVersion",
    "CatalogueBundle.signature",
    "CatalogueBundle.signatureKeyId"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-037",
   "source": "Claude Design POS pack, 24 August",
   "note": "**Drawn by Claude Design on `POS Board 5.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 9 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
    "BO-008",
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
      "eventId",
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-007",
     "trigger": "Product Directory",
     "carries": [
      "productId"
     ],
     "provenance": "derived — BO-007 declares entryState.params productId, so an edge into it must carry them"
    },
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "carries": [
      "productId",
      "venueId"
     ],
     "provenance": "derived — BO-008 declares entryState.params productId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-009",
     "trigger": "Pricing Rules",
     "carries": [
      "priceListId"
     ],
     "provenance": "derived — BO-009 declares entryState.params priceListId, so an edge into it must carry them"
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
  "gaps": [
   {
    "operation": "getEvent",
    "why": "**4 declared operations reach no component on this screen**: getEvent, getSeatAvailability, listEvents, getVenueSettings. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every opening hours calendar",
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
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected opening hours calendar",
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
       "operation": "createPerformances",
       "provenance": "contract catalogue.yaml POST /events/{eventId}/performances"
      },
      {
       "kind": "destructiveButton",
       "label": "Cancel",
       "operation": "cancelPerformance",
       "provenance": "contract catalogue.yaml POST /performances/{performanceId}/cancel"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createEvent",
       "provenance": "contract catalogue.yaml POST /events"
      },
      {
       "kind": "secondaryButton",
       "label": "Recommend",
       "operation": "recommendSeats",
       "provenance": "contract seating.yaml POST /performances/{performanceId}/seat-recommendations"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateEvent",
       "provenance": "contract catalogue.yaml PATCH /events/{eventId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updatePerformance",
       "provenance": "contract catalogue.yaml PATCH /performances/{performanceId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateOutlet",
       "provenance": "contract tenancy.yaml PATCH /outlets/{outletId}"
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
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listPerformances",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createPerformances",
       "label": "Create performances",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "destructiveButton",
       "derived": true,
       "impliedBy": "cancelPerformance",
       "label": "Cancel performance",
       "notes": "**Always confirms, never the default focus.** The consequence goes in the body — *cancel 3 orders worth AED 480* is a confirmation, *are you sure* is not.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createPerformances",
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
    "id": "confirmCancelPerformance",
    "component": "confirmDialog",
    "trigger": "Cancel",
    "body": "**Names what `cancelPerformance` changes and what it leaves alone**, in the consequence rather than the verb. A opening hours calendar this affects should be identified in the dialog, not just counted.",
    "provenance": "contract catalogue.yaml POST /performances/{performanceId}/cancel"
   }
  ],
  "states": {
   "loading": "The opening hours calendar list.",
   "error": "Could not load. Names which read failed and leaves the opening hours calendar untouched.",
   "emptyFirstRun": "No opening hours calendar yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the opening hours calendar are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPerformances",
    "contract": "catalogue",
    "purpose": "List performances of an event",
    "trigger": "onLoad"
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
    "BO-143"
   ],
   "transitions": [
    {
     "to": "BO-007",
     "trigger": "Product Directory",
     "carries": [
      "productId"
     ],
     "provenance": "derived — BO-007 declares entryState.params productId, so an edge into it must carry them"
    },
    {
     "to": "BO-009",
     "trigger": "Pricing Rules",
     "carries": [
      "priceListId"
     ],
     "provenance": "derived — BO-009 declares entryState.params priceListId, so an edge into it must carry them"
    },
    {
     "to": "BO-010",
     "trigger": "Promotions & Coupons",
     "carries": [
      "campaignId",
      "code",
      "dashboardId",
      "promotionId",
      "reportId",
      "venueId"
     ],
     "provenance": "derived — BO-010 declares entryState.params campaignId, code, dashboardId, promotionId, reportId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-011",
     "trigger": "Packages & Bundles",
     "carries": [
      "version"
     ],
     "provenance": "derived — BO-011 declares entryState.params version, so an edge into it must carry them"
    },
    {
     "to": "BO-012",
     "trigger": "Membership Products",
     "carries": [
      "productId"
     ],
     "provenance": "derived — BO-012 declares entryState.params productId, so an edge into it must carry them"
    },
    {
     "to": "BO-013",
     "trigger": "Channel & Distribution",
     "carries": [
      "channelCapacityId"
     ],
     "provenance": "derived — BO-013 declares entryState.params channelCapacityId, so an edge into it must carry them"
    },
    {
     "to": "BO-014",
     "trigger": "Catalogue Publishing",
     "carries": [
      "itemId",
      "priceListId",
      "productId",
      "venueId"
     ],
     "provenance": "derived — BO-014 declares entryState.params itemId, priceListId, productId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-015",
     "trigger": "Session Calendar",
     "carries": [
      "eventId",
      "performanceId"
     ],
     "provenance": "derived — BO-015 declares entryState.params eventId, performanceId, so an edge into it must carry them"
    },
    {
     "to": "BO-016",
     "trigger": "Session Template",
     "carries": [
      "eventId",
      "performanceId"
     ],
     "provenance": "derived — BO-016 declares entryState.params eventId, performanceId, so an edge into it must carry them"
    },
    {
     "to": "BO-017",
     "trigger": "Capacity Management",
     "carries": [
      "channelCapacityId"
     ],
     "provenance": "derived — BO-017 declares entryState.params channelCapacityId, so an edge into it must carry them"
    },
    {
     "to": "BO-018",
     "trigger": "Allocation & Holds",
     "carries": [
      "inventoryHoldId"
     ],
     "provenance": "derived — BO-018 declares entryState.params inventoryHoldId, so an edge into it must carry them"
    },
    {
     "to": "BO-019",
     "trigger": "Closures & Blackouts",
     "carries": [
      "eventId",
      "mapId",
      "pathId",
      "performanceId"
     ],
     "provenance": "derived — BO-019 declares entryState.params eventId, mapId, pathId, performanceId, so an edge into it must carry them"
    },
    {
     "to": "BO-037",
     "trigger": "Offline Package Status",
     "carries": [
      "version"
     ],
     "provenance": "derived — BO-037 declares entryState.params version, so an edge into it must carry them"
    },
    {
     "to": "BO-063",
     "trigger": "Opening Hours & Calendar",
     "carries": [
      "eventId",
      "outletId",
      "performanceId",
      "venueId"
     ],
     "provenance": "derived — BO-063 declares entryState.params eventId, outletId, performanceId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-109",
     "trigger": "Menu Builder & POS Layout Designer",
     "carries": [
      "menuId",
      "saleBoardId",
      "venueId"
     ],
     "provenance": "derived — BO-109 declares entryState.params menuId, saleBoardId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-110",
     "trigger": "Recipe & BOM Management",
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-110 declares entryState.params venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-111",
     "trigger": "Ingredient Substitution, Allergen & Nutrition",
     "carries": [
      "menuId",
      "menuItemId",
      "venueId"
     ],
     "provenance": "derived — BO-111 declares entryState.params menuId, menuItemId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-112",
     "trigger": "Production Planning & Production Sheets",
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-112 declares entryState.params venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-113",
     "trigger": "Central Kitchen & Commissary Management",
     "carries": [
      "runId",
      "venueId"
     ],
     "provenance": "derived — BO-113 declares entryState.params runId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-114",
     "trigger": "Variants, Attributes, Barcode & RFID Management",
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-114 declares entryState.params venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-115",
     "trigger": "Category, Brand & Merchandise Hierarchy",
     "carries": [
      "reportId",
      "venueId"
     ],
     "provenance": "derived — BO-115 declares entryState.params reportId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-116",
     "trigger": "Merchandising & Product Presentation",
     "carries": [
      "merchandiseId",
      "roleId",
      "saleBoardId",
      "venueId"
     ],
     "provenance": "derived — BO-116 declares entryState.params merchandiseId, roleId, saleBoardId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-117",
     "trigger": "Product Import, Governance & AI Configuration Assistant",
     "carries": [
      "saleBoardId",
      "venueId"
     ],
     "provenance": "derived — BO-117 declares entryState.params saleBoardId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-118",
     "trigger": "Campaign & Audience Management",
     "carries": [
      "reportId",
      "saleBoardId",
      "venueId"
     ],
     "provenance": "derived — BO-118 declares entryState.params reportId, saleBoardId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-119",
     "trigger": "Cross-Sell, Upsell & Recommendation Rules",
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-119 declares entryState.params venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-120",
     "trigger": "Omnichannel Commerce & Journey Configuration",
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-120 declares entryState.params venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-121",
     "trigger": "Personalized Offers & Guest Engagement",
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-121 declares entryState.params venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-122",
     "trigger": "POS Experience Dashboard",
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-122 declares entryState.params venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-123",
     "trigger": "POS Profile Management",
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-123 declares entryState.params venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-124",
     "trigger": "Layout & Journey Builder",
     "carries": [
      "deviceId",
      "profileId",
      "saleBoardId",
      "venueId"
     ],
     "provenance": "derived — BO-124 declares entryState.params deviceId, profileId, saleBoardId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-125",
     "trigger": "Product & Category Button Configuration",
     "carries": [
      "deviceId",
      "saleBoardId",
      "venueId",
      "workstationId"
     ],
     "provenance": "derived — BO-125 declares entryState.params deviceId, saleBoardId, venueId, workstationId, so an edge into it must carry them"
    },
    {
     "to": "BO-126",
     "trigger": "Deployment, Preview & Audit",
     "carries": [
      "profileId",
      "reportId",
      "rolloutId",
      "saleBoardId",
      "venueId"
     ],
     "provenance": "derived — BO-126 declares entryState.params profileId, reportId, rolloutId, saleBoardId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-142",
     "trigger": "Store Rules, Controls & Permissions",
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-142 declares entryState.params venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-143",
     "trigger": "Retail Global Settings & Controls",
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-143 declares entryState.params venueId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Section landing. **14 screens reach the entry point through here** — before 20 August they reached it through nothing.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listUpsellRules` reads the population and `getVenueSettings` reads one of them — list, select, act",
  "purpose": "Everything in sell, and what in it needs attention.",
  "gaps": [
   {
    "operation": "getUpsellSuggestions",
    "why": "**1 declared operation reach no component on this screen**: getUpsellSuggestions. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every sell",
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
        "UpsellRule.isActive"
       ],
       "operation": "listUpsellRules",
       "provenance": "contract promotions.yaml GET /upsell-rules"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected sell",
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
     "name": "contentBody",
     "slot": "carried",
     "components": [
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
    "purpose": "Upsell rules in force",
    "trigger": "onLoad"
   },
   {
    "operationId": "getUpsellSuggestions",
    "contract": "promotions",
    "purpose": "What to offer this basket",
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
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-102 declares entryState.params venueId, so an edge into it must carry them"
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
       "kind": "dataTable",
       "label": "Every menu pos layout",
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
       "label": "The selected menu pos layout",
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
       "label": "Save changes",
       "operation": "setMenuSections",
       "provenance": "contract fnb.yaml PUT /menus/{menuId}/sections"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateSaleBoard",
       "provenance": "contract tenancy.yaml PUT /sale-boards/{saleBoardId}"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "searchField",
       "label": "Search menu builder",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The menu pos layout list.",
   "error": "Could not load. Names which read failed and leaves the menu pos layout untouched.",
   "emptyFirstRun": "No menu pos layout yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the menu pos layout are still there. Names the active filter and offers to clear it.",
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
   "note": "**Drawn by Claude Design on `FnB Board 2.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
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
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-102 declares entryState.params venueId, so an edge into it must carry them"
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
       "kind": "dataTable",
       "label": "Every recipe bom",
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
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected recipe bom",
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
       "label": "Save changes",
       "operation": "setRecipe",
       "provenance": "contract fnb.yaml PUT /recipes"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "searchField",
       "label": "Search recipe",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The recipe bom list.",
   "error": "Could not load. Names which read failed and leaves the recipe bom untouched.",
   "emptyFirstRun": "No recipe bom yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the recipe bom are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
     "to": "BO-045",
     "trigger": "The draft is scheduled for Monday rather than published now",
     "provenance": "flow F31 step 3→4, F93 step 1→2"
    },
    {
     "to": "BO-102",
     "trigger": "Sell",
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-102 declares entryState.params venueId, so an edge into it must carry them"
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
       "operation": "setRecipe",
       "provenance": "contract fnb.yaml PUT /recipes"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateMenu",
       "provenance": "contract fnb.yaml PATCH /menus/{menuId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "setSubstitutionRules",
       "provenance": "contract fnb.yaml PUT /substitution-rules"
      },
      {
       "kind": "secondaryButton",
       "label": "Verify",
       "operation": "verifyAllergens",
       "provenance": "contract fnb.yaml POST /menu-items/{menuItemId}/verify-allergens"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "searchField",
       "label": "Search ingredient substitution, allergen",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The saved ingredient substitution allergen.",
   "error": "Could not load. Names which read failed and leaves the ingredient substitution allergen untouched.",
   "emptyFirstRun": "No ingredient substitution allergen configured. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
    "purpose": "Does this dish still match its claim?",
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
     "name": "menuId",
     "from": "deepLink"
    },
    {
     "name": "menuItemId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "Resolves from the session. A principal with more than one venue is asked which before the page renders. An item opened from the menu. **Allergen verification is per item** — a menu-wide check is a job, not a screen."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-111",
   "source": "Claude Design F&B pack, 24 August",
   "note": "**Drawn by Claude Design on `FnB Board 2.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-102 declares entryState.params venueId, so an edge into it must carry them"
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
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Plan",
       "operation": "planProductionRun",
       "provenance": "contract fnb.yaml POST /production-runs"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "searchField",
       "label": "Search production planning",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The saved production planning production.",
   "error": "Could not load. Names which read failed and leaves the production planning production untouched.",
   "emptyFirstRun": "No production planning production configured. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-102 declares entryState.params venueId, so an edge into it must carry them"
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
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Plan",
       "operation": "planProductionRun",
       "provenance": "contract fnb.yaml POST /production-runs"
      },
      {
       "kind": "secondaryButton",
       "label": "Complete",
       "operation": "completeProductionRun",
       "provenance": "contract fnb.yaml POST /production-runs/{runId}/complete"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "searchField",
       "label": "Search central kitchen",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The saved central kitchen commissary.",
   "error": "Could not load. Names which read failed and leaves the central kitchen commissary untouched.",
   "emptyFirstRun": "No central kitchen commissary configured. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
   "source": "Claude Design Retail pack, 24 August",
   "note": "**Drawn by Claude Design on `Retail Board 2.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
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
  "summary": "Acquire an inventory lease",
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
   }
  ],
  "requestBody": "CreatePerformancesRequest",
  "responds": null
 },
 "forceReleaseInventoryHold": {
  "method": "POST",
  "path": "/inventory-holds/{inventoryHoldId}/force-release",
  "contract": "catalogue",
  "summary": "Reclaim a stranded lease",
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
  "summary": "List leases",
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
  "parameters": [],
  "requestBody": "SeatRecommendationRequest",
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
  "summary": "Extend a lease TTL",
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
  "responds": "VenuePath"
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
  "parameters": [],
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
  "responds": null
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AcquireLeaseRequest": {
  "type": "object",
  "required": [
   "id",
   "channelCapacityId",
   "requestedUnits",
   "ttlSeconds"
  ],
  "properties": {
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "Client-generated ULID. Also the idempotency key."
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
    "description": "Short TTLs limit stranding when a terminal dies; long TTLs survive longer outages. The venue's default balances the two.\n"
   }
  }
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
    "description": "Products, variants, price lists, prices, tax codes, events, performances, envelope definitions and data mask field definitions. Shape is versioned with the bundle format, not with this API.\n",
    "additionalProperties": true
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
   "parentEventId": {
    "type": "string",
    "format": "uuid"
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
   "recurrence": {
    "type": "object",
    "description": "Generate a series rather than a single performance.",
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
    "type": "integer"
   },
   "isActive": {
    "type": "boolean"
   }
  }
 },
 "InventoryHold": {
  "x-ticvai-persistence": "catalogue.inventory_hold",
  "type": "object",
  "required": [
   "id",
   "channelCapacityId",
   "holderWorkstationId",
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
   "holderWorkstationId": {
    "type": "string",
    "format": "uuid"
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
 "LeaseStatus": {
  "type": "string",
  "enum": [
   "active",
   "expired",
   "released",
   "forceReleased"
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
   "entitlements": {
    "type": "array",
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
       "type": "string"
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
       "type": "string"
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
   }
  }
 },
 "OfflinePolicy": {
  "type": "object",
  "x-ticvai-persistence": "platform.offline_policy",
  "description": "Board 5 of the client's POS set. **ADR-0013 makes the POS local-first and nothing configured the policy** — one of only two things in 36 board screens the package genuinely could not do.\nCF-115 reframed offline into three data classes: catalogue and policy always local, contended inventory leased, transactional facts journalled. **This is where a venue says how far that goes for them.**\n",
  "required": [
   "id",
   "scopePath"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string"
   },
   "maxOfflineHours": {
    "type": "integer",
    "default": 24,
    "description": "**After which the workstation refuses to sell rather than keep journalling.** A till three days offline holding 900 unsynced sales is a reconciliation nobody can do and a fraud nobody can detect.\n"
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
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "offlineTransactionCeiling": {
    "type": "integer",
    "nullable": true,
    "description": "**A ceiling on count as well as value.** Nine hundred small sales and one large one are different risks, and a value ceiling alone catches only the second.\n"
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
    "description": "First entry that could not be processed. Null when the batch succeeded. The client retries from here and never past it.\n"
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
       "type": "string"
      },
      "sequence": {
       "type": "integer"
      },
      "status": {
       "type": "string",
       "enum": [
        "accepted",
        "duplicate",
        "rejected"
       ]
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
    "items": {
     "type": "object"
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
    "description": "Queued for approval. Refunds are not issued automatically."
   },
   "notificationsQueued": {
    "type": "integer"
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
    "$ref": "../shared/common.yaml#/components/schemas/Money"
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
 "SubstitutionRule": {
  "type": "object",
  "x-ticvai-persistence": "fnb.substitution_rule",
  "description": "Board 2L, 24 August. **What may replace what, and under what conditions.** A kitchen substitutes constantly — a supplier is short, an item is 86'd, a guest asks — and the package had no way to say which swaps are allowed.\n**The rule exists so `verifyAllergens` has something to check against.** A substitution with no rule behind it is a decision made at the pass by whoever is standing there.\n**`allergenDelta` is the field this table is for.** Swapping butter for margarine removes dairy and may add soy — **and a dish still labelled dairy-free after a swap nobody checked is the failure this prevents.**\n",
  "required": [
   "id",
   "fromIngredientId",
   "toIngredientId"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
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
     "type": "string"
    }
   },
   "allergensRemoved": {
    "type": "array",
    "items": {
     "type": "string"
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
    "format": "uuid"
   },
   "mapId": {
    "type": "string",
    "format": "uuid"
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
    "description": "**Along the centreline, not point to point.** A path that curves round a lake is longer than the distance between its ends, and a guest told 80 metres who walks 200 stops trusting the map.\nRequires a georeference for real units; without one, distances are in drawing units and routing still works because **only the ratios matter to a shortest path.**\n"
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
    "description": "Set during works or an incident. **A closed path removes routes rather than hiding the path**, so a guest sees why rather than wondering where it went.\n"
   }
  }
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
