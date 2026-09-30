# WS174 — Seat Management Venue Mapping Reference v1.0 board 10

**8 screens · 8 operations · 13 schemas · 4 permissions**

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
  `AI_USE, CAPACITY_CONFIGURE, PRODUCT_CONFIGURE, PRODUCT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-1043` | Revenue Command Center | listDetail | 1 | 0 | — |
| `BO-1044` | Dynamic Seat Pricing | listDetail | 1 | 0 | — |
| `BO-1045` | Price Bands & Categories | listDetail | 3 | 0 | — |
| `BO-1046` | Inventory Forecasting | listDetail | 1 | 0 | — |
| `BO-1047` | Section Revenue Forecast | listDetail | 1 | 0 | — |
| `BO-1048` | Seat Upsell Recommendations | listDetail | 1 | 0 | — |
| `BO-1049` | Scenario & What-If Planning | listDetail | 1 | 0 | — |
| `BO-1050` | Revenue Analytics & Audit | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-1043, BO-1044, BO-1045, BO-1046, BO-1047, BO-1048, BO-1049, BO-1050 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-1043",
  "name": "Revenue Command Center",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "10",
   "number": "01",
   "page": 42
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/revenue-command-center-bo-1043",
   "component": "apps/venue-management-web/src/routes/access-venue/RevenueCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-1044",
    "BO-1045",
    "BO-1046",
    "BO-1047",
    "BO-1048",
    "BO-1049",
    "BO-1050"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 10 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "BO-1044",
     "trigger": "Dynamic Seat Pricing",
     "provenance": "structural — pack board 10 wiring, 19 September 2026"
    },
    {
     "to": "BO-1045",
     "trigger": "Price Bands & Categories",
     "provenance": "structural — pack board 10 wiring, 19 September 2026"
    },
    {
     "to": "BO-1046",
     "trigger": "Inventory Forecasting",
     "provenance": "structural — pack board 10 wiring, 19 September 2026"
    },
    {
     "to": "BO-1047",
     "trigger": "Section Revenue Forecast",
     "provenance": "structural — pack board 10 wiring, 19 September 2026"
    },
    {
     "to": "BO-1048",
     "trigger": "Seat Upsell Recommendations",
     "provenance": "structural — pack board 10 wiring, 19 September 2026"
    },
    {
     "to": "BO-1049",
     "trigger": "Scenario & What-If Planning",
     "provenance": "structural — pack board 10 wiring, 19 September 2026"
    },
    {
     "to": "BO-1050",
     "trigger": "Revenue Analytics & Audit",
     "provenance": "structural — pack board 10 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide a live executive and revenue-management view of seat performance. Show revenue, yield, occupancy, sales pace, average ticket price, remaining inventory and forecast variance. Analyze by tenant, venue, event, performance, section, category, price band, channel and time to event. Surface underperforming sections, demand spikes, inventory imbalance and pricing opportunities with drill-down. Pricing changes require explainable inputs, min/max guardrails, effective dates, approval, versioning and rollback; AI may recommend but cannot publish outside delegated authority. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 42"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 42"
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
       "impliedBy": "listRevenue",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The revenue list.",
   "error": "Could not load. Names which read failed and leaves the revenue untouched.",
   "emptyFirstRun": "No revenue yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the revenue are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listRevenue",
    "contract": "catalogue",
    "purpose": "Revenue Optimization Command Center",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1043",
   "workshopBoard": "wireframes/WS149 Seat Management Venue Mapping Reference v1.0 Board 10.dc.html#bo-1043"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 42. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1044",
  "name": "Dynamic Seat Pricing",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "10",
   "number": "02",
   "page": 42
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/dynamic-seat-pricing-bo-1044",
   "component": "apps/venue-management-web/src/routes/access-venue/DynamicSeatPricing.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1043"
   ],
   "exitTo": [
    "BO-1043"
   ],
   "transitions": [
    {
     "to": "BO-1043",
     "trigger": "Back to Revenue Command Center",
     "provenance": "structural — pack board 10 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure rules that adjust assigned-seat prices within controlled boundaries. Apply rules by section, row, seat, category, event, performance, sales pace, demand, remaining inventory and time to event. Set base price, adjustment type, floor, ceiling, step, maximum frequency, freeze window and competitor/manual inputs where approved. Preview affected inventory, customer display, active carts, taxes/fees, promotions and forecast impact before activation. Pricing changes require explainable inputs, min/max guardrails, effective dates, approval, versioning and rollback; AI may recommend but cannot publish outside delegated authority. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 42"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 42"
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
       "impliedBy": "listDynamicPricingStrategy",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The dynamic seat pricing list.",
   "error": "Could not load. Names which read failed and leaves the dynamic seat pricing untouched.",
   "emptyFirstRun": "No dynamic seat pricing yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the dynamic seat pricing are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listDynamicPricingStrategy",
    "contract": "catalogue",
    "purpose": "Dynamic pricing in force",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1044",
   "workshopBoard": "wireframes/WS149 Seat Management Venue Mapping Reference v1.0 Board 10.dc.html#bo-1044"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 42. 0 of 0 labels bound to a contract property; 0 of 11 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1045",
  "name": "Price Bands & Categories",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "10",
   "number": "03",
   "page": 42
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/price-bands-categories-bo-1045",
   "component": "apps/venue-management-web/src/routes/access-venue/PriceBandsCategories.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1043"
   ],
   "exitTo": [
    "BO-1043"
   ],
   "transitions": [
    {
     "to": "BO-1043",
     "trigger": "Back to Revenue Command Center",
     "provenance": "structural — pack board 10 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Maintain the commercial hierarchy applied to seat inventory. Configure price band, seat category, display label, color, currency, channel, customer segment and effective period. Map bands to venue sections, rows or seats and support event/performance overrides with inheritance. Detect overlapping dates, unmapped inventory, invalid currency, missing products and conflicting priority. Configuration Scope of Work | Version 1.0 42 Pricing changes require explainable inputs, min/max guardrails, effective dates, approval, versioning and rollback; AI may recommend but cannot publish outside delegated authority. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": "createSeatCategory",
    "why": "**Price bands on seat categories are kept** (decided 28 September, audit R275 (d)) and the contract has none: `SeatCategory` needs a price-band list (code, display label, colour, currency, channel, customer segment, effective from/to). Handed to the contracts group.",
    "source": "audit R275 (d)"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 42"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 42"
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
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows. **Each seat category shows its price bands** (label, currency, channel, customer segment, effective period) — kept by the client (decided 28 September, audit R275 (d)) and handed to the contracts group, since `SeatCategory` has no price band yet."
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
   "loading": "The price bands categories list.",
   "error": "Could not load. Names which read failed and leaves the price bands categories untouched.",
   "emptyFirstRun": "No price bands categories yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the price bands categories are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listSeatCategories",
    "contract": "seating",
    "purpose": "Price bands against categories",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "createSeatCategory",
    "contract": "seating",
    "purpose": "Add a band",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "updateSeatCategory",
    "contract": "seating",
    "purpose": "Rename, re-rank or re-price a seat category",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listSeatCategories"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1045",
   "workshopBoard": "wireframes/WS149 Seat Management Venue Mapping Reference v1.0 Board 10.dc.html#bo-1045"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 42. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "seatCategoryId",
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
  "id": "BO-1046",
  "name": "Inventory Forecasting",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "10",
   "number": "05",
   "page": 43
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/inventory-forecasting-bo-1046",
   "component": "apps/venue-management-web/src/routes/access-venue/InventoryForecasting.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1043"
   ],
   "exitTo": [
    "BO-1043"
   ],
   "transitions": [
    {
     "to": "BO-1043",
     "trigger": "Back to Revenue Command Center",
     "provenance": "structural — pack board 10 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Predict remaining inventory and sell-through by event day. Forecast seats remaining, sell-through, sold-out probability and over/under supply by section and category. Account for active locks, holds, scheduled releases, blocks, expected cancellations and group allocations. Highlight categories likely to sell out early or remain unsold and link to recommended actions. Pricing changes require explainable inputs, min/max guardrails, effective dates, approval, versioning and rollback; AI may recommend but cannot publish outside delegated authority. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 43"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 43"
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
       "impliedBy": "listDemandBookingCurve",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The inventory forecasting list.",
   "error": "Could not load. Names which read failed and leaves the inventory forecasting untouched.",
   "emptyFirstRun": "No inventory forecasting yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the inventory forecasting are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listDemandBookingCurve",
    "contract": "catalogue",
    "purpose": "Forecast against the curve",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1046",
   "workshopBoard": "wireframes/WS149 Seat Management Venue Mapping Reference v1.0 Board 10.dc.html#bo-1046"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 43. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1047",
  "name": "Section Revenue Forecast",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "10",
   "number": "06",
   "page": 43
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/section-revenue-forecast-bo-1047",
   "component": "apps/venue-management-web/src/routes/access-venue/SectionRevenueForecast.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1043"
   ],
   "exitTo": [
    "BO-1043"
   ],
   "transitions": [
    {
     "to": "BO-1043",
     "trigger": "Back to Revenue Command Center",
     "provenance": "structural — pack board 10 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Plan expected revenue at the venue-section level. Show capacity, sold, held, available, average price, forecast occupancy, forecast revenue and variance. Provide map heat view and ranking by revenue opportunity, yield gap and risk. Reconcile forecast totals with performance and finance dimensions and preserve scenario assumptions. Pricing changes require explainable inputs, min/max guardrails, effective dates, approval, versioning and rollback; AI may recommend but cannot publish outside delegated authority. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 43"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 43"
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
       "impliedBy": "listDemandBookingCurve",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The section revenue forecast list.",
   "error": "Could not load. Names which read failed and leaves the section revenue forecast untouched.",
   "emptyFirstRun": "No section revenue forecast yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the section revenue forecast are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listDemandBookingCurve",
    "contract": "catalogue",
    "purpose": "By section",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1047",
   "workshopBoard": "wireframes/WS149 Seat Management Venue Mapping Reference v1.0 Board 10.dc.html#bo-1047"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 43. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1048",
  "name": "Seat Upsell Recommendations",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "10",
   "number": "07",
   "page": 43
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/seat-upsell-recommendations-bo-1048",
   "component": "apps/venue-management-web/src/routes/access-venue/SeatUpsellRecommendations.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1043"
   ],
   "exitTo": [
    "BO-1043"
   ],
   "transitions": [
    {
     "to": "BO-1043",
     "trigger": "Back to Revenue Command Center",
     "provenance": "structural — pack board 10 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure revenue-positive seat offers that remain fair and eligible. Rank upgrade pairs by view improvement, distance, amenities, price delta, availability and customer eligibility. Set channels, offer window, frequency, minimum improvement, margin, membership/loyalty benefit and exclusion rules. Track offer, acceptance, incremental revenue, original-seat resale and guest outcome. Configuration Scope of Work | Version 1.0 43 Pricing changes require explainable inputs, min/max guardrails, effective dates, approval, versioning and rollback; AI may recommend but cannot publish outside delegated authority. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 43"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 43"
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
       "impliedBy": "getRecommendations",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "getRecommendations"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The seat upsell recommendations list.",
   "error": "Could not load. Names which read failed and leaves the seat upsell recommendations untouched.",
   "emptyFirstRun": "No seat upsell recommendations yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the seat upsell recommendations are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "decideRecommendations",
    "contract": "ai",
    "purpose": "Fill a recommendation slot",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1048",
   "workshopBoard": "wireframes/WS149 Seat Management Venue Mapping Reference v1.0 Board 10.dc.html#bo-1048"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 43. 0 of 0 labels bound to a contract property; 0 of 10 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1049",
  "name": "Scenario & What-If Planning",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "10",
   "number": "08",
   "page": 44
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/scenario-what-if-planning-bo-1049",
   "component": "apps/venue-management-web/src/routes/access-venue/ScenarioWhatIfPlanning.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1043"
   ],
   "exitTo": [
    "BO-1043"
   ],
   "transitions": [
    {
     "to": "BO-1043",
     "trigger": "Back to Revenue Command Center",
     "provenance": "structural — pack board 10 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Compare alternative price, demand and inventory decisions before publication. Adjust capacity, price, discount, holdback, release timing, demand uplift and sales pace assumptions. Calculate seats sold, occupancy, revenue, yield, gross margin, sell-out timing and downside risk. Save, compare, comment, share and approve scenarios without changing live prices or inventory. Pricing changes require explainable inputs, min/max guardrails, effective dates, approval, versioning and rollback; AI may recommend but cannot publish outside delegated authority. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 44"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 44"
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
       "impliedBy": "simulatePriceBreakdownCalculation",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "simulatePriceBreakdownCalculation"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The scenario what-if planning list.",
   "error": "Could not load. Names which read failed and leaves the scenario what-if planning untouched.",
   "emptyFirstRun": "No scenario what-if planning yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the scenario what-if planning are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "simulatePriceBreakdownCalculation",
    "contract": "catalogue",
    "purpose": "What-if on price",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1049",
   "workshopBoard": "wireframes/WS149 Seat Management Venue Mapping Reference v1.0 Board 10.dc.html#bo-1049"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 44. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1050",
  "name": "Revenue Analytics & Audit",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "10",
   "number": "10",
   "page": 44
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/revenue-analytics-audit-bo-1050",
   "component": "apps/venue-management-web/src/routes/access-venue/RevenueAnalyticsAudit.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1043"
   ],
   "exitTo": [
    "BO-1043"
   ],
   "transitions": [
    {
     "to": "BO-1043",
     "trigger": "Back to Revenue Command Center",
     "provenance": "structural — pack board 10 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Measure actual financial outcomes and preserve decision evidence. Compare realized versus forecast revenue, occupancy, yield, average price and sell-through by section/category. Attribute change to price actions, holds/releases, promotions, demand shifts, channels and model recommendations. Retain rule, input data version, model/version, recommendation, approval, publication, override and rollback history. Pricing changes require explainable inputs, min/max guardrails, effective dates, approval, versioning and rollback; AI may recommend but cannot publish outside delegated authority. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history. Configuration Scope of Work | Version 1.0 44 Board 11 - Seat Reporting & Analytics Figure 11. High-definition configuration board with all 10 screens. Visual reference: information architecture and configuration coverage; detailed production behavior is defined in the following scope. Configuration Scope of Work | Version 1.0 45",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 44"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 44"
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
       "impliedBy": "listRevenue",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The revenue analytics audit list.",
   "error": "Could not load. Names which read failed and leaves the revenue analytics audit untouched.",
   "emptyFirstRun": "No revenue analytics audit yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the revenue analytics audit are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listRevenue",
    "contract": "catalogue",
    "purpose": "Revenue Optimization Command Center",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1050",
   "workshopBoard": "wireframes/WS149 Seat Management Venue Mapping Reference v1.0 Board 10.dc.html#bo-1050"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 44. 0 of 0 labels bound to a contract property; 0 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "listDemandBookingCurve": {
  "method": "GET",
  "path": "/demand-booking-curve",
  "contract": "catalogue",
  "summary": "AI Demand Forecasting & Booking Curve Studio",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "venue",
    "in": "query",
    "required": false
   },
   {
    "name": "product",
    "in": "query",
    "required": false
   },
   {
    "name": "event",
    "in": "query",
    "required": false
   },
   {
    "name": "performance",
    "in": "query",
    "required": false
   },
   {
    "name": "channel",
    "in": "query",
    "required": false
   },
   {
    "name": "horizon",
    "in": "query",
    "required": false
   },
   {
    "name": "dateFrom",
    "in": "query",
    "required": false
   },
   {
    "name": "dateTo",
    "in": "query",
    "required": false
   },
   {
    "name": "priceCategory",
    "in": "query",
    "required": false
   },
   {
    "name": "sectionCode",
    "in": "query",
    "required": false
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
 "listDynamicPricingStrategy": {
  "method": "GET",
  "path": "/dynamic-pricing-strategy",
  "contract": "catalogue",
  "summary": "Dynamic Pricing Strategy Command Center",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "strategyType",
    "in": "query",
    "required": false
   },
   {
    "name": "status",
    "in": "query",
    "required": false
   },
   {
    "name": "automationMode",
    "in": "query",
    "required": false
   },
   {
    "name": "venue",
    "in": "query",
    "required": false
   },
   {
    "name": "search",
    "in": "query",
    "required": false
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
 "listRevenue": {
  "method": "GET",
  "path": "/revenue",
  "contract": "catalogue",
  "summary": "Revenue Optimization Command Center",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "venue",
    "in": "query",
    "required": false
   },
   {
    "name": "automationMode",
    "in": "query",
    "required": false
   },
   {
    "name": "urgency",
    "in": "query",
    "required": false
   },
   {
    "name": "rankBy",
    "in": "query",
    "required": false
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
 "simulatePriceBreakdownCalculation": {
  "method": "PUT",
  "path": "/price-breakdown-calculation",
  "contract": "catalogue",
  "summary": "Price Breakdown, Calculation Simulation & Explainability",
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
  "requestBody": "PriceBreakdownCalculationSimulationExplainabilityInput",
  "responds": "PriceBreakdownCalculationSimulationExplainabilityView"
 },
 "updateSeatCategory": {
  "method": "PATCH",
  "path": "/seat-categories/{seatCategoryId}",
  "contract": "seating",
  "summary": "Rename, re-rank or re-price a seat category",
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
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AiDemandForecastingBookingCurveStudioView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What AI Demand Forecasting & Booking Curve Studio displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "venue": {
    "type": "string",
    "description": "Venue id"
   },
   "product": {
    "type": "string",
    "description": "Product id",
    "nullable": true
   },
   "event": {
    "type": "string",
    "description": "Event id",
    "nullable": true
   },
   "performance": {
    "type": "string",
    "description": "Performance id",
    "nullable": true
   },
   "date": {
    "type": "string",
    "description": "Date",
    "format": "date"
   },
   "timeslot": {
    "type": "string",
    "description": "Timeslot",
    "nullable": true
   },
   "priceCategory": {
    "type": "string",
    "description": "Price category",
    "nullable": true
   },
   "sectionCode": {
    "type": "string",
    "nullable": true,
    "description": "Seat-map section (`seating.Section.code`) the row forecasts; null for a row at price-category or performance level (29 September, build pass, group G2; 21.11.4)"
   },
   "channel": {
    "$ref": "#/components/schemas/Channel",
    "description": "Channel"
   },
   "confidence": {
    "type": "number",
    "description": "Forecast Confidence, percent"
   },
   "forecastFinalOccupancy": {
    "type": "number",
    "description": "Forecast Final Occupancy, percent"
   },
   "demand": {
    "type": "integer",
    "description": "Forecast demand"
   },
   "attendance": {
    "type": "integer",
    "description": "Forecast attendance"
   },
   "occupancy": {
    "type": "number",
    "description": "Forecast occupancy, percent"
   },
   "sellThrough": {
    "type": "number",
    "description": "Forecast sell-through, percent"
   },
   "expectedSellOutTime": {
    "type": "string",
    "description": "Expected Sell-Out Time; empty if no sell-out forecast",
    "format": "date-time",
    "nullable": true
   },
   "revenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Forecast revenue"
   },
   "conversion": {
    "type": "number",
    "description": "Forecast conversion, percent"
   },
   "remainingInventory": {
    "type": "integer",
    "description": "Forecast remaining inventory at event"
   },
   "mape": {
    "type": "number",
    "description": "MAPE over closed forecasts at this level, percent"
   },
   "forecastBias": {
    "type": "number",
    "description": "Forecast Bias (positive = over-forecast), percent"
   },
   "overForecast": {
    "type": "number",
    "description": "Share of closed forecasts that over-forecast, percent"
   },
   "underForecast": {
    "type": "number",
    "description": "Share of closed forecasts that under-forecast, percent"
   },
   "forecastId": {
    "type": "string",
    "description": "Forecast id"
   },
   "horizon": {
    "type": "string",
    "description": "Forecast Horizon",
    "enum": [
     "intraday",
     "tomorrow",
     "days7",
     "days30",
     "eventHorizon",
     "seasonalHorizon"
    ]
   },
   "bookingCurve": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "daysBeforeEvent": {
       "type": "integer",
       "description": "T minus days"
      },
      "historicalExpectedPercentSold": {
       "type": "number",
       "description": "Historical expected curve, percent sold"
      },
      "actualPercentSold": {
       "type": "number",
       "nullable": true,
       "description": "Current actual curve, percent sold (empty for future points)"
      },
      "forecastPercentSold": {
       "type": "number",
       "description": "AI forecast curve, percent sold"
      }
     }
    },
    "description": "Booking Curve"
   },
   "signalContributions": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "signal": {
       "type": "string",
       "enum": [
        "internalSales",
        "bookingVelocity",
        "occupancy",
        "historicalEvents",
        "nearbyEvent",
        "weather",
        "marketTourism",
        "competitor",
        "priceElasticity",
        "other"
       ],
       "description": "Signal category"
      },
      "contributionPercent": {
       "type": "number",
       "description": "Explanatory share of the forecast"
      }
     }
    },
    "description": "Model Inputs: which signals contributed"
   },
   "confidenceReasons": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "strongHistoricalData",
      "stableBookingPattern",
      "reliableExternalSignals",
      "limitedHistoricalData",
      "volatileBookingPattern",
      "degradedExternalSignals"
     ]
    },
    "description": "Reasons behind the forecast confidence"
   },
   "modelVersion": {
    "type": "string",
    "description": "Model version that produced the forecast"
   },
   "generatedAt": {
    "type": "string",
    "description": "When the forecast was produced",
    "format": "date-time"
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
 "DynamicPricingStrategyCommandCenterSummary": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection; the headline tiles over the list, computed at read time for the filters in force",
  "description": "**The headline figures on Dynamic Pricing Strategy Command Center.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.",
  "properties": {
   "activeStrategies": {
    "type": "integer",
    "description": "Active Strategies"
   },
   "draftStrategies": {
    "type": "integer",
    "description": "Draft Strategies"
   },
   "productsUnderDynamicPricing": {
    "type": "integer",
    "description": "Products Under Dynamic Pricing"
   },
   "eventsUnderDynamicPricing": {
    "type": "integer",
    "description": "Events Under Dynamic Pricing"
   },
   "performancesUnderDynamicPricing": {
    "type": "integer",
    "description": "Performances Under Dynamic Pricing"
   },
   "rulesActive": {
    "type": "integer",
    "description": "Rules Active"
   },
   "currentPriceAdjustments": {
    "type": "integer",
    "description": "Current Price Adjustments"
   },
   "pricesAtMaximumGuardrail": {
    "type": "integer",
    "description": "Prices at Maximum Guardrail"
   },
   "pricesAtMinimumGuardrail": {
    "type": "integer",
    "description": "Prices at Minimum Guardrail"
   },
   "ruleConflicts": {
    "type": "integer",
    "description": "Rule Conflicts"
   },
   "frozenStrategies": {
    "type": "integer",
    "description": "Frozen Strategies"
   },
   "upcomingActivations": {
    "type": "integer",
    "description": "Upcoming Activations: strategies scheduled to activate within 7 days (decided 29 September, readiness close-out)"
   },
   "operationalAlerts": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Operational Alerts (pack p.76), e.g. performances at their upper band, strategies with unresolved conflicts, strategies activating within 48 hours"
   }
  }
 },
 "DynamicPricingStrategyCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Dynamic Pricing Strategy Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "strategyId": {
    "type": "string",
    "description": "Strategy ID"
   },
   "strategyName": {
    "type": "string",
    "description": "Strategy Name"
   },
   "strategyType": {
    "type": "string",
    "enum": [
     "demandBased",
     "occupancyBased",
     "availabilityBased",
     "inventoryBased",
     "bookingVelocity",
     "timeToEvent",
     "seasonal",
     "dayOfWeek",
     "timeslot",
     "channel",
     "segment",
     "location",
     "hybrid"
    ],
    "description": "Strategy Type (pack pp.75-76)"
   },
   "productEvent": {
    "type": "string",
    "description": "Product or event the strategy controls"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "basePriceSource": {
    "type": "string",
    "description": "Base price source: the Board 1 price list and rate the strategy moves from, e.g. UAE Standard Admission -> Adult"
   },
   "currentPrice": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Current resolved dynamic price (for a single-price scope)",
    "nullable": true
   },
   "adjustmentRange": {
    "type": "object",
    "properties": {
     "minPercent": {
      "type": "number",
      "description": "Lowest adjustment from base, percent"
     },
     "maxPercent": {
      "type": "number",
      "description": "Highest adjustment from base, percent"
     }
    },
    "description": "Adjustment range allowed by the strategy"
   },
   "ruleCount": {
    "type": "integer",
    "description": "Rule Count"
   },
   "effectivePeriod": {
    "type": "object",
    "properties": {
     "from": {
      "type": "string",
      "format": "date-time",
      "description": "Effective from"
     },
     "to": {
      "type": "string",
      "format": "date-time",
      "description": "Effective to; empty for open-ended",
      "nullable": true
     }
    },
    "description": "Effective period"
   },
   "automationMode": {
    "type": "string",
    "enum": [
     "monitor",
     "recommend",
     "prepareChange",
     "autoExecuteWithinGuardrails"
    ],
    "description": "Automation mode from the automation policy (listDynamicPricingAutomation); recommend by default"
   },
   "status": {
    "type": "string",
    "description": "Status: draft, testing, ready, scheduled, active, paused, frozen, expired or retired"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
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
 "PriceBreakdownCalculationSimulationExplainabilityInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Price Breakdown, Calculation Simulation & Explainability submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "customerId": {
    "type": "string",
    "nullable": true,
    "description": "Customer"
   },
   "productId": {
    "type": "string",
    "description": "Product"
   },
   "quantity": {
    "type": "integer",
    "description": "Quantity",
    "minimum": 1
   },
   "venueId": {
    "type": "string",
    "nullable": true,
    "description": "Venue"
   },
   "eventId": {
    "type": "string",
    "nullable": true,
    "description": "Event"
   },
   "channel": {
    "$ref": "../shared/common.yaml#/components/schemas/SalesChannel",
    "description": "Channel"
   },
   "date": {
    "type": "string",
    "format": "date",
    "description": "Date of visit"
   },
   "timeslotId": {
    "type": "string",
    "nullable": true,
    "description": "Timeslot"
   },
   "membershipId": {
    "type": "string",
    "nullable": true,
    "description": "Membership"
   },
   "promotionCode": {
    "type": "string",
    "nullable": true,
    "description": "Promotion"
   },
   "paymentMethod": {
    "type": "string",
    "nullable": true,
    "description": "Payment Method"
   },
   "deliveryMethod": {
    "type": "string",
    "nullable": true,
    "description": "Delivery Method"
   },
   "currency": {
    "type": "string",
    "description": "Currency: ISO 4217 code",
    "pattern": "^[A-Z]{3}$"
   },
   "compareChannels": {
    "type": "array",
    "items": {
     "$ref": "../shared/common.yaml#/components/schemas/SalesChannel"
    },
    "description": "Channel Comparison (p.51): run the same transaction through these channels too; empty for none"
   }
  }
 },
 "PriceBreakdownCalculationSimulationExplainabilityView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Price Breakdown, Calculation Simulation & Explainability displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "finalPayable": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Final Payable"
   },
   "components": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "sequence": {
       "type": "integer"
      },
      "componentType": {
       "type": "string",
       "enum": [
        "selectedRate",
        "memberAdjustment",
        "dynamicAdjustment",
        "promotion",
        "packageAdjustment",
        "fee",
        "surcharge",
        "waiver",
        "tax",
        "rounding"
       ]
      },
      "label": {
       "type": "string",
       "description": "e.g. Booking Fee, VAT"
      },
      "source": {
       "type": "string",
       "description": "Source: the price list, rule, fee or tax profile"
      },
      "rule": {
       "type": "string",
       "description": "Rule: id of the rule applied, e.g. FE-021, TAX-UAE-01"
      },
      "formula": {
       "type": "string"
      },
      "input": {
       "allOf": [
        {
         "$ref": "../shared/common.yaml#/components/schemas/Money"
        }
       ],
       "description": "Input amount"
      },
      "output": {
       "allOf": [
        {
         "$ref": "../shared/common.yaml#/components/schemas/Money"
        }
       ],
       "description": "Output amount (negative for a reduction)"
      },
      "reason": {
       "type": "string"
      },
      "taxTreatment": {
       "type": "string",
       "nullable": true
      }
     }
    },
    "description": "Explainability Panel and Rule Trace (p.51), in sequence"
   },
   "selectedRate": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Selected Rate x quantity"
   },
   "discountTotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Discounts and adjustments total"
   },
   "feeTotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Fees total"
   },
   "subtotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Subtotal before tax"
   },
   "taxTotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Tax total"
   },
   "calculationVersion": {
    "type": "string",
    "description": "Calculation version used"
   },
   "channelComparison": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "channel": {
       "$ref": "../shared/common.yaml#/components/schemas/SalesChannel"
      },
      "finalPayable": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "difference": {
       "type": "string",
       "description": "Why it differs, e.g. Call Center Booking Fee"
      }
     }
    },
    "description": "Channel Comparison results"
   },
   "aiInsights": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "AI observations for this screen; advisory only, never applied automatically"
   }
  }
 },
 "RevenueOptimizationCommandCenterSummary": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection; the headline tiles over the list, computed at read time for the filters in force",
  "description": "**The headline figures on Revenue Optimization Command Center.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.",
  "properties": {
   "revenueOpportunity": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue Opportunity"
   },
   "incrementalRevenueGenerated": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Incremental Revenue Generated"
   },
   "activeOptimizations": {
    "type": "integer",
    "description": "Active Optimizations"
   },
   "recommendationsAwaitingAction": {
    "type": "integer",
    "description": "Recommendations Awaiting Action"
   },
   "pendingSimulations": {
    "type": "integer",
    "description": "Pending Simulations"
   },
   "autoExecutedChanges": {
    "type": "integer",
    "description": "Auto-Executed Changes"
   },
   "approvalRequired": {
    "type": "integer",
    "description": "Approval Required: changes waiting for an approver"
   },
   "activeABTests": {
    "type": "integer",
    "description": "Active A/B Tests"
   },
   "pricingExceptions": {
    "type": "integer",
    "description": "Pricing Exceptions"
   },
   "revenueAtRisk": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue at Risk"
   },
   "forecastAccuracy": {
    "type": "number",
    "description": "Forecast Accuracy over the last 30 days (decided 29 September, readiness close-out), percent"
   },
   "optimizationSuccessRate": {
    "type": "number",
    "description": "Optimization Success Rate: executed changes with a positive measured outcome, percent"
   },
   "aiRevenueBrief": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "AI Revenue Brief, e.g. AED 284,000 of opportunity in the next seven days. Advisory only: generated narrative never changes a price (decided 29 September, readiness close-out)"
   }
  }
 },
 "RevenueOptimizationCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Revenue Optimization Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "eventProduct": {
    "type": "string",
    "description": "Event/Product"
   },
   "performance": {
    "type": "string",
    "description": "Performance",
    "nullable": true
   },
   "currentPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Current Price"
   },
   "recommendedPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Recommended Price"
   },
   "forecastRevenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Forecast Revenue"
   },
   "expectedUplift": {
    "type": "number",
    "description": "Expected Uplift, percent"
   },
   "confidence": {
    "type": "number",
    "description": "Confidence, percent"
   },
   "automationMode": {
    "type": "string",
    "description": "Automation Mode in force for this scope",
    "enum": [
     "advisory",
     "humanInTheLoop",
     "conditionalAutonomous",
     "autonomous"
    ]
   },
   "approvalStatus": {
    "type": "string",
    "description": "Approval Status: notRequired, pending, approved or rejected"
   },
   "executionStatus": {
    "type": "string",
    "description": "Execution Status: notStarted, queued, processing, live, partial, failed or rolledBack"
   },
   "revenueRisk": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue Risk if no action is taken"
   },
   "eventProximity": {
    "type": "integer",
    "description": "Event Proximity: days until the event"
   },
   "inventoryPosition": {
    "type": "number",
    "description": "Inventory Position: remaining inventory, percent"
   },
   "demandVariance": {
    "type": "number",
    "description": "Demand Variance against forecast, percent"
   },
   "urgency": {
    "type": "string",
    "description": "Urgency",
    "enum": [
     "low",
     "medium",
     "high",
     "critical"
    ]
   },
   "optimizationId": {
    "type": "string",
    "description": "Optimisation id"
   },
   "recommendationId": {
    "type": "string",
    "description": "Recommendation id",
    "nullable": true
   },
   "revenueOpportunity": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue Opportunity"
   },
   "priorityRank": {
    "type": "integer",
    "description": "Priority rank (1 = act first)"
   },
   "nextAction": {
    "type": "string",
    "description": "Suggested next action (the pack's Action column)",
    "enum": [
     "review",
     "simulate",
     "approve"
    ]
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
 }
}
```
