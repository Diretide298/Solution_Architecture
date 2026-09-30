# WS173 — Seat Management Venue Mapping Reference v1.0 board 9

**10 screens · 5 operations · 6 schemas · 3 permissions**

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

- **Every control that can be refused must be gated.** 3 permissions apply here:
  `CAPACITY_CONFIGURE, ORDER_MODIFY, PRODUCT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-1033` | Recommendation Command Center | listDetail | 1 | 0 | — |
| `BO-1034` | Best Seat Recommendations | listDetail | 1 | 0 | — |
| `BO-1035` | Best Value Recommendations | listDetail | 1 | 0 | — |
| `BO-1036` | Closest-to-Stage Recommendations | listDetail | 1 | 0 | — |
| `BO-1037` | Family Seating Recommendations | listDetail | 1 | 0 | — |
| `BO-1038` | Accessibility Recommendations | listDetail | 2 | 0 | — |
| `BO-1039` | Seat Upgrade Recommendations | listDetail | 1 | 0 | — |
| `BO-1040` | Alternatives & Reseating | listDetail | 1 | 0 | — |
| `BO-1041` | Scoring Rules & Model Governance | listDetail | 1 | 0 | — |
| `BO-1042` | Performance, Feedback & Audit | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-1034, BO-1035, BO-1036, BO-1037, BO-1038, BO-1039, BO-1040, BO-1041 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-1033",
  "name": "Recommendation Command Center",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "9",
   "number": "01",
   "page": 38
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/recommendation-command-center-bo-1033",
   "component": "apps/venue-management-web/src/routes/access-venue/RecommendationCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-1034",
    "BO-1035",
    "BO-1036",
    "BO-1037",
    "BO-1038",
    "BO-1039",
    "BO-1040",
    "BO-1041",
    "BO-1042"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 9 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "BO-1034",
     "trigger": "Best Seat Recommendations",
     "provenance": "structural — pack board 9 wiring, 19 September 2026"
    },
    {
     "to": "BO-1035",
     "trigger": "Best Value Recommendations",
     "provenance": "structural — pack board 9 wiring, 19 September 2026"
    },
    {
     "to": "BO-1036",
     "trigger": "Closest-to-Stage Recommendations",
     "provenance": "structural — pack board 9 wiring, 19 September 2026"
    },
    {
     "to": "BO-1037",
     "trigger": "Family Seating Recommendations",
     "provenance": "structural — pack board 9 wiring, 19 September 2026"
    },
    {
     "to": "BO-1038",
     "trigger": "Accessibility Recommendations",
     "provenance": "structural — pack board 9 wiring, 19 September 2026"
    },
    {
     "to": "BO-1039",
     "trigger": "Seat Upgrade Recommendations",
     "provenance": "structural — pack board 9 wiring, 19 September 2026",
     "carries": [
      "performanceId"
     ]
    },
    {
     "to": "BO-1040",
     "trigger": "Alternatives & Reseating",
     "provenance": "structural — pack board 9 wiring, 19 September 2026"
    },
    {
     "to": "BO-1041",
     "trigger": "Scoring Rules & Model Governance",
     "provenance": "structural — pack board 9 wiring, 19 September 2026"
    },
    {
     "to": "BO-1042",
     "trigger": "Performance, Feedback & Audit",
     "provenance": "structural — pack board 9 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Monitor recommendation demand, quality, conversion and risk. Show recommendations served, accepted, locked, purchased, revenue uplift, fallback and no-result rates. Compare use case, channel, venue, performance, model/version, guest type and time period. Surface data gaps, drift, declining acceptance, accessibility mismatch and model/service incidents. Recommendations must be explainable, confidence-scored and subordinate to availability, price, lock, accessibility, eligibility and consent rules; models cannot write inventory state directly. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 38"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Recommendations served",
       "columns": [
        "Recommendations served"
       ],
       "notes": "The pack asks for recommendations served; the contract has no field for it.",
       "provenance": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 38"
      },
      {
       "kind": "metricTile",
       "label": "Accepted",
       "columns": [
        "Accepted"
       ],
       "notes": "The pack asks for accepted; the contract has no field for it.",
       "provenance": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 38"
      },
      {
       "kind": "metricTile",
       "label": "Purchased",
       "columns": [
        "Purchased"
       ],
       "notes": "The pack asks for purchased; the contract has no field for it.",
       "provenance": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 38"
      },
      {
       "kind": "metricTile",
       "label": "Revenue uplift",
       "columns": [
        "Revenue uplift"
       ],
       "notes": "The pack asks for revenue uplift; the contract has no field for it.",
       "provenance": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 38"
      },
      {
       "kind": "metricTile",
       "label": "Fallback / no-result rate",
       "columns": [
        "Fallback / no-result rate"
       ],
       "notes": "The pack asks for fallback / no-result rate; the contract has no field for it.",
       "provenance": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 38"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Recommendation profiles",
       "bindsTo": "SeatRecommendationRules.profiles",
       "columns": [
        "SeatRecommendationRules.profiles[].kind",
        "SeatRecommendationRules.profiles[].weights",
        "SeatRecommendationRules.profiles[].preferredSectionIds",
        "SeatRecommendationRules.profiles[].avoidSectionIds",
        "SeatRecommendationRules.profiles[].contiguityWeight"
       ],
       "operation": "getSeatRecommendationRules",
       "notes": "The only thing the bound read returns is configuration; the pack's metrics are all unbound.",
       "provenance": "contract seating.yaml GET /seat-recommendation-rules"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "Configuration in force",
       "bindsTo": "SeatRecommendationRules",
       "columns": [
        "SeatRecommendationRules.seatMapId",
        "SeatRecommendationRules.performanceId",
        "SeatRecommendationRules.reverseRowOrder",
        "SeatRecommendationRules.explainToGuest",
        "SeatRecommendationRules.scopePath"
       ],
       "operation": "getSeatRecommendationRules",
       "provenance": "contract seating.yaml GET /seat-recommendation-rules"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The recommendation list.",
   "error": "Could not load. Names which read failed and leaves the recommendation untouched.",
   "emptyFirstRun": "No recommendation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the recommendation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getSeatRecommendationRules",
    "contract": "seating",
    "purpose": "Scoring in force",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1033",
   "workshopBoard": "wireframes/WS148 Seat Management Venue Mapping Reference v1.0 Board 9.dc.html#bo-1033"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 38. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Layout drafted 29 September (VM close-out)** from pack Seat_Management_Venue_Mapping_Reference v1.0.pdf p.38; contract seating.yaml GET /seat-recommendation-rules. Pack labels with no schema field yet (shown as plain labels): Recommendations served, Accepted, Purchased, Revenue uplift, Fallback / no-result rate, Locked, Data gaps / drift / declining acceptance alerts, Model / version, Breakdown by use case, channel, venue, guest type.",
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
  "id": "BO-1034",
  "name": "Best Seat Recommendations",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "9",
   "number": "02",
   "page": 38
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/best-seat-recommendations-bo-1034",
   "component": "apps/venue-management-web/src/routes/access-venue/BestSeatRecommendations.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1033"
   ],
   "exitTo": [
    "BO-1033"
   ],
   "transitions": [
    {
     "to": "BO-1033",
     "trigger": "Back to Recommendation Command Center",
     "provenance": "structural — pack board 9 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Rank the strongest overall options for the requested quantity. Score view, distance, orientation, row, aisle, obstruction, amenities, demand and customer preference. Return valid seat groups with match score, total price, view summary, rationale and trade-offs. Support rule-based fallback when AI is unavailable or confidence falls below the configured threshold. Recommendations must be explainable, confidence-scored and subordinate to availability, price, lock, accessibility, eligibility and consent rules; models cannot write inventory state directly. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 38"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 38"
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
       "impliedBy": "setSeatRecommendationRules",
       "label": "Save",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setSeatRecommendationRules"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The best seat recommendations list.",
   "error": "Could not load. Names which read failed and leaves the best seat recommendations untouched.",
   "emptyFirstRun": "No best seat recommendations yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the best seat recommendations are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setSeatRecommendationRules",
    "contract": "seating",
    "purpose": "What \"best seat\" means here",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getSeatRecommendationRules"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1034",
   "workshopBoard": "wireframes/WS148 Seat Management Venue Mapping Reference v1.0 Board 9.dc.html#bo-1034"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 38. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1035",
  "name": "Best Value Recommendations",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "9",
   "number": "03",
   "page": 38
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/best-value-recommendations-bo-1035",
   "component": "apps/venue-management-web/src/routes/access-venue/BestValueRecommendations.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1033"
   ],
   "exitTo": [
    "BO-1033"
   ],
   "transitions": [
    {
     "to": "BO-1033",
     "trigger": "Back to Recommendation Command Center",
     "provenance": "structural — pack board 9 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Balance quality and price to identify strong value options. Calculate value from price, view, distance, category, demand, historical preference and comparable inventory. Present a price-versus-quality matrix and explain why each option represents better value. Respect minimum/maximum budget, promotion eligibility, fee transparency and price-lock policy. Recommendations must be explainable, confidence-scored and subordinate to availability, price, lock, accessibility, eligibility and consent rules; models cannot write inventory state directly. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history. Configuration Scope of Work | Version 1.0 38",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 38"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 38"
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
       "impliedBy": "setSeatRecommendationRules",
       "label": "Save",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setSeatRecommendationRules"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The best value recommendations list.",
   "error": "Could not load. Names which read failed and leaves the best value recommendations untouched.",
   "emptyFirstRun": "No best value recommendations yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the best value recommendations are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setSeatRecommendationRules",
    "contract": "seating",
    "purpose": "Best value weighting",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getSeatRecommendationRules"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1035",
   "workshopBoard": "wireframes/WS148 Seat Management Venue Mapping Reference v1.0 Board 9.dc.html#bo-1035"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 38. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1036",
  "name": "Closest-to-Stage Recommendations",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "9",
   "number": "04",
   "page": 39
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/closest-to-stage-recommendations-bo-1036",
   "component": "apps/venue-management-web/src/routes/access-venue/ClosestToStageRecommendations.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1033"
   ],
   "exitTo": [
    "BO-1033"
   ],
   "transitions": [
    {
     "to": "BO-1033",
     "trigger": "Back to Recommendation Command Center",
     "provenance": "structural — pack board 9 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Rank seats by meaningful proximity to the event focal point. Use configured stage/field/focal point, seat coordinates, orientation, level and route rather than row number alone. Show distance, section, row, elevation, obstruction and route information for each option. Support multiple focal points and event-specific stage layouts with the correct layout version. Recommendations must be explainable, confidence-scored and subordinate to availability, price, lock, accessibility, eligibility and consent rules; models cannot write inventory state directly. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 39"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 39"
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
       "impliedBy": "setSeatRecommendationRules",
       "label": "Save",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setSeatRecommendationRules"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The closest-to-stage recommendations list.",
   "error": "Could not load. Names which read failed and leaves the closest-to-stage recommendations untouched.",
   "emptyFirstRun": "No closest-to-stage recommendations yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the closest-to-stage recommendations are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setSeatRecommendationRules",
    "contract": "seating",
    "purpose": "Closest to stage",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getSeatRecommendationRules"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1036",
   "workshopBoard": "wireframes/WS148 Seat Management Venue Mapping Reference v1.0 Board 9.dc.html#bo-1036"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 39. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1037",
  "name": "Family Seating Recommendations",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "9",
   "number": "05",
   "page": 39
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/family-seating-recommendations-bo-1037",
   "component": "apps/venue-management-web/src/routes/access-venue/FamilySeatingRecommendations.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1033"
   ],
   "exitTo": [
    "BO-1033"
   ],
   "transitions": [
    {
     "to": "BO-1033",
     "trigger": "Back to Recommendation Command Center",
     "provenance": "structural — pack board 9 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Find safe and practical seat groups for families. Prioritize contiguity, aisle preference, child-friendly areas, short routes and proximity to approved facilities. Consider adult/child ratio, age policy, stroller/service needs, family membership and budget. Explain splits or compromises and never separate minors contrary to configured policy. Recommendations must be explainable, confidence-scored and subordinate to availability, price, lock, accessibility, eligibility and consent rules; models cannot write inventory state directly. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 39"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 39"
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
       "impliedBy": "setSeatRecommendationRules",
       "label": "Save",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setSeatRecommendationRules"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The family seating recommendations list.",
   "error": "Could not load. Names which read failed and leaves the family seating recommendations untouched.",
   "emptyFirstRun": "No family seating recommendations yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the family seating recommendations are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setSeatRecommendationRules",
    "contract": "seating",
    "purpose": "Family together",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getSeatRecommendationRules"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1037",
   "workshopBoard": "wireframes/WS148 Seat Management Venue Mapping Reference v1.0 Board 9.dc.html#bo-1037"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 39. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1038",
  "name": "Accessibility Recommendations",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "9",
   "number": "06",
   "page": 39
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/accessibility-recommendations-bo-1038",
   "component": "apps/venue-management-web/src/routes/access-venue/AccessibilityRecommendations.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1033"
   ],
   "exitTo": [
    "BO-1033"
   ],
   "transitions": [
    {
     "to": "BO-1033",
     "trigger": "Back to Recommendation Command Center",
     "provenance": "structural — pack board 9 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Match stated access needs to verified accessible inventory and routes. Use wheelchair, companion, transfer, aisle, step-free, hearing, vision and service-animal attributes. Show companion pairing, accessible route, distance to entrance/facilities and any assistance requirement. Protect sensitive preference data, allow human-assisted review and prevent inappropriate release of protected inventory. Recommendations must be explainable, confidence-scored and subordinate to availability, price, lock, accessibility, eligibility and consent rules; models cannot write inventory state directly. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 39"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 39"
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
       "impliedBy": "setSeatRecommendationRules",
       "label": "Save",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setSeatRecommendationRules"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The accessibility recommendations list.",
   "error": "Could not load. Names which read failed and leaves the accessibility recommendations untouched.",
   "emptyFirstRun": "No accessibility recommendations yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the accessibility recommendations are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setSeatRecommendationRules",
    "contract": "seating",
    "purpose": "Accessible recommendations",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getSeatRecommendationRules"
    ]
   },
   {
    "operationId": "getAccessibleSeating",
    "contract": "seating",
    "purpose": "The accessible inventory",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1038",
   "workshopBoard": "wireframes/WS148 Seat Management Venue Mapping Reference v1.0 Board 9.dc.html#bo-1038"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 39. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1039",
  "name": "Seat Upgrade Recommendations",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "9",
   "number": "07",
   "page": 39
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/seat-upgrade-recommendations-bo-1039",
   "component": "apps/venue-management-web/src/routes/access-venue/SeatUpgradeRecommendations.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1033"
   ],
   "exitTo": [
    "BO-1033"
   ],
   "transitions": [
    {
     "to": "BO-1033",
     "trigger": "Back to Recommendation Command Center",
     "provenance": "structural — pack board 9 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Offer an eligible higher-value alternative before or after purchase. Compare current and candidate seat on view, distance, level, amenities, accessibility and price difference. Apply membership, loyalty, promotion, exchange, refund, fee and event cutoff rules. Show expected value and acquire new inventory before releasing the original seat through a safe exchange flow. Recommendations must be explainable, confidence-scored and subordinate to availability, price, lock, accessibility, eligibility and consent rules; models cannot write inventory state directly. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history. Configuration Scope of Work | Version 1.0 39",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 39"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 39"
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
       "impliedBy": "recommendSeats",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "recommendSeats"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The seat upgrade recommendations list.",
   "error": "Could not load. Names which read failed and leaves the seat upgrade recommendations untouched.",
   "emptyFirstRun": "No seat upgrade recommendations yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the seat upgrade recommendations are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "recommendSeats",
    "contract": "seating",
    "purpose": "Upgrade options",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1039",
   "workshopBoard": "wireframes/WS148 Seat Management Venue Mapping Reference v1.0 Board 9.dc.html#bo-1039"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 39. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1040",
  "name": "Alternatives & Reseating",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "9",
   "number": "08",
   "page": 40
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/alternatives-reseating-bo-1040",
   "component": "apps/venue-management-web/src/routes/access-venue/AlternativesReseating.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1033"
   ],
   "exitTo": [
    "BO-1033"
   ],
   "transitions": [
    {
     "to": "BO-1033",
     "trigger": "Back to Recommendation Command Center",
     "provenance": "structural — pack board 9 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide comparable options when selected or issued seats become unavailable. Rank same-price, better-price, better-view, same-section, accessible and adjacent alternatives. Support operational reseating for layout changes, maintenance, production blocks and customer requests. Explain impact, require approval/acceptance where applicable and preserve original-to-new seat lineage. Recommendations must be explainable, confidence-scored and subordinate to availability, price, lock, accessibility, eligibility and consent rules; models cannot write inventory state directly. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 40"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 40"
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
       "impliedBy": "reassignSeats",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "reassignSeats"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The alternatives reseating list.",
   "error": "Could not load. Names which read failed and leaves the alternatives reseating untouched.",
   "emptyFirstRun": "No alternatives reseating yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the alternatives reseating are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "reassignSeats",
    "contract": "seating",
    "purpose": "Move a party, and tell them",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getSeatInventory",
     "getSeatReconciliation"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1040",
   "workshopBoard": "wireframes/WS148 Seat Management Venue Mapping Reference v1.0 Board 9.dc.html#bo-1040"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 40. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1041",
  "name": "Scoring Rules & Model Governance",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "9",
   "number": "09",
   "page": 40
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/scoring-rules-model-governance-bo-1041",
   "component": "apps/venue-management-web/src/routes/access-venue/ScoringRulesModelGovernance.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1033"
   ],
   "exitTo": [
    "BO-1033"
   ],
   "transitions": [
    {
     "to": "BO-1033",
     "trigger": "Back to Recommendation Command Center",
     "provenance": "structural — pack board 9 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure recommendation objectives, constraints and AI controls. Set weighted factors, hard constraints, tie-breakers, minimum score, fallback, audience and use-case priority. Manage model/version, training/evaluation metadata, approval, effective dates and rollback. Run test personas, backtests, bias/accessibility checks and scenario comparison before publication. Recommendations must be explainable, confidence-scored and subordinate to availability, price, lock, accessibility, eligibility and consent rules; models cannot write inventory state directly. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 40"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 40"
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
       "impliedBy": "setSeatRecommendationRules",
       "label": "Save",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setSeatRecommendationRules"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The scoring rules model list.",
   "error": "Could not load. Names which read failed and leaves the scoring rules model untouched.",
   "emptyFirstRun": "No scoring rules model yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the scoring rules model are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setSeatRecommendationRules",
    "contract": "seating",
    "purpose": "Scoring and governance",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getSeatRecommendationRules"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1041",
   "workshopBoard": "wireframes/WS148 Seat Management Venue Mapping Reference v1.0 Board 9.dc.html#bo-1041"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 40. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1042",
  "name": "Performance, Feedback & Audit",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "9",
   "number": "10",
   "page": 40
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/performance-feedback-audit-bo-1042",
   "component": "apps/venue-management-web/src/routes/access-venue/PerformanceFeedbackAudit.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1033"
   ],
   "exitTo": [
    "BO-1033"
   ],
   "transitions": [
    {
     "to": "BO-1033",
     "trigger": "Back to Recommendation Command Center",
     "provenance": "structural — pack board 9 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Measure realized recommendation quality and accountability. Report acceptance, conversion, revenue, upgrade, abandonment, no-result and downstream satisfaction. Capture accept/reject, reason, user feedback, actual purchase and post-event outcome for learning. Monitor drift and disparity and retain inputs, candidates, scores, explanation, model/version and human decisions. Recommendations must be explainable, confidence-scored and subordinate to availability, price, lock, accessibility, eligibility and consent rules; models cannot write inventory state directly. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history. Configuration Scope of Work | Version 1.0 40 Board 10 - Seat Revenue Management & Forecasting Figure 10. High-definition configuration board with all 10 screens. Visual reference: information architecture and configuration coverage; detailed production behavior is defined in the following scope. Configuration Scope of Work | Version 1.0 41",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 40"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Acceptance rate",
       "columns": [
        "Acceptance rate"
       ],
       "notes": "The pack asks for acceptance rate; the contract has no field for it.",
       "provenance": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 40"
      },
      {
       "kind": "metricTile",
       "label": "Conversion",
       "columns": [
        "Conversion"
       ],
       "notes": "The pack asks for conversion; the contract has no field for it.",
       "provenance": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 40"
      },
      {
       "kind": "metricTile",
       "label": "Upgrade rate",
       "columns": [
        "Upgrade rate"
       ],
       "notes": "The pack asks for upgrade rate; the contract has no field for it.",
       "provenance": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 40"
      },
      {
       "kind": "metricTile",
       "label": "No-result rate",
       "columns": [
        "No-result rate"
       ],
       "notes": "The pack asks for no-result rate; the contract has no field for it.",
       "provenance": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 40"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Recommendation decisions",
       "columns": [
        "Recommendation",
        "Guest action (accept / reject)",
        "Reason",
        "User feedback",
        "Actual purchase",
        "Model / version",
        "Score"
       ],
       "notes": "The retained inputs, candidates, scores, explanation and human decision; no operation returns them.",
       "provenance": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 40"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "Scoring configuration at the time",
       "bindsTo": "SeatRecommendationRules",
       "columns": [
        "SeatRecommendationRules.profiles",
        "SeatRecommendationRules.reverseRowOrder",
        "SeatRecommendationRules.explainToGuest",
        "SeatRecommendationRules.scopePath"
       ],
       "operation": "getSeatRecommendationRules",
       "notes": "Current configuration only; the contract keeps no history of it.",
       "provenance": "contract seating.yaml GET /seat-recommendation-rules"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The performance feedback audit list.",
   "error": "Could not load. Names which read failed and leaves the performance feedback audit untouched.",
   "emptyFirstRun": "No performance feedback audit yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the performance feedback audit are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getSeatRecommendationRules",
    "contract": "seating",
    "purpose": "Performance and feedback",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1042",
   "workshopBoard": "wireframes/WS148 Seat Management Venue Mapping Reference v1.0 Board 9.dc.html#bo-1042"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 40. 0 of 0 labels bound to a contract property; 0 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Layout drafted 29 September (VM close-out)** from pack Seat_Management_Venue_Mapping_Reference v1.0.pdf p.40; contract seating.yaml GET /seat-recommendation-rules. Pack labels with no schema field yet (shown as plain labels): Acceptance rate, Conversion, Upgrade rate, No-result rate, Revenue, Abandonment, Downstream satisfaction, Drift / disparity, Accept / reject, Reason, User feedback, Actual purchase, Model / version, Candidates and scores, Explanation.",
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
 "getAccessibleSeating": {
  "method": "GET",
  "path": "/accessible-seating",
  "contract": "seating",
  "summary": "Accessible seats, their routes and who may buy them",
  "permission": "CAPACITY_CONFIGURE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "seatMapId",
    "in": "query",
    "required": true
   }
  ],
  "requestBody": null,
  "responds": "AccessibleSeating"
 },
 "getSeatRecommendationRules": {
  "method": "GET",
  "path": "/seat-recommendation-rules",
  "contract": "seating",
  "summary": "What \"best\" means at this venue",
  "permission": "CAPACITY_CONFIGURE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "SeatRecommendationRules"
 },
 "reassignSeats": {
  "method": "POST",
  "path": "/seat-reassignment",
  "contract": "seating",
  "summary": "Move a booked party, and tell them",
  "permission": "ORDER_MODIFY",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "SeatReassignment"
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
 "setSeatRecommendationRules": {
  "method": "PUT",
  "path": "/seat-recommendation-rules",
  "contract": "seating",
  "summary": "Scoring for best seat, best value, closest, family and accessible",
  "permission": "CAPACITY_CONFIGURE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "SeatRecommendationRules",
  "responds": "SeatRecommendationRules"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AccessibleSeating": {
  "type": "object",
  "x-ticvai-persistence": "seating.accessible",
  "description": "Boards 7.6 to 7.8. **An accessible seat with no accessible route is not an accessible seat.**\n",
  "properties": {
   "seatMapId": {
    "type": "string",
    "format": "uuid"
   },
   "spaces": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "seatId": {
       "type": "string",
       "format": "uuid"
      },
      "kind": {
       "type": "string",
       "enum": [
        "wheelchairSpace",
        "transferSeat",
        "ambulant",
        "easyAccess",
        "assistanceDog",
        "hearingLoop",
        "visuallyImpaired"
       ]
      },
      "routeDescription": {
       "type": "string",
       "nullable": true
      },
      "stepFree": {
       "type": "boolean",
       "default": true
      },
      "nearestAccessibleWc": {
       "type": "string",
       "nullable": true
      }
     }
    }
   },
   "eligibility": {
    "type": "string",
    "enum": [
     "open",
     "selfDeclared",
     "verifiedOnce",
     "verifiedEachTime"
    ],
    "default": "selfDeclared",
    "description": "**Contested in both directions.** Open sale leaves none for the guests who need them; hard gating turns people away at the door.\n"
   },
   "minimumProvisionPercent": {
    "type": "number",
    "nullable": true
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "SeatReassignment": {
  "type": "object",
  "x-ticvai-persistence": "seating.reassignment",
  "description": "Board 9.8. **Never silently downgrades.**",
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "orderId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "fromSeatIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "toSeatIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "reason": {
    "type": "string"
   },
   "priceDifference": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "refundIssued": {
    "type": "boolean",
    "default": false
   },
   "guestNotifiedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "performedBy": {
    "type": "string",
    "format": "uuid"
   },
   "at": {
    "type": "string",
    "format": "date-time"
   },
   "scopePath": {
    "type": "string"
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
 "SeatRecommendationRules": {
  "type": "object",
  "x-ticvai-persistence": "seating.recommendation_rules",
  "description": "Board 9, and the 21 August minute: *\"best-seat ranking… must be configurable per seat map/event.\"* **Five kinds, one scoring model** — five algorithms would eventually contradict each other.\n",
  "properties": {
   "seatMapId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "performanceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "profiles": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "kind": {
       "type": "string",
       "enum": [
        "bestSeat",
        "bestValue",
        "closestToStage",
        "familyTogether",
        "accessible",
        "upgrade"
       ]
      },
      "weights": {
       "type": "object",
       "additionalProperties": {
        "type": "number"
       },
       "description": "Sightline, distance, centrality, row, price, availability, aisle proximity, legroom.\n"
      },
      "preferredSectionIds": {
       "type": "array",
       "items": {
        "type": "string",
        "format": "uuid"
       }
      },
      "avoidSectionIds": {
       "type": "array",
       "items": {
        "type": "string",
        "format": "uuid"
       }
      },
      "contiguityWeight": {
       "type": "number",
       "nullable": true
      }
     }
    }
   },
   "reverseRowOrder": {
    "type": "boolean",
    "default": false,
    "description": "**Last-row-is-best against first-row-is-best**, which the minute names as the worked example and which differs by venue sightline.\n"
   },
   "explainToGuest": {
    "type": "boolean",
    "default": true
   },
   "scopePath": {
    "type": "string"
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
 }
}
```
