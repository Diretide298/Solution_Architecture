# WS169 — Seat Management Venue Mapping Reference v1.0 board 5

**10 screens · 11 operations · 13 schemas · 5 permissions**

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

- **Every control that can be refused must be gated.** 5 permissions apply here:
  `CAPACITY_CONFIGURE, ORDER_CREATE, ORDER_VIEW, PRICE_VIEW, PRODUCT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-993` | Experience Command Center | listDetail | 2 | 0 | — |
| `BO-994` | Choose My Seats | listDetail | 2 | 0 | — |
| `BO-995` | Find Seats For Me | listDetail | 1 | 0 | — |
| `BO-996` | Filters & Interactive Legend | listDetail | 1 | 0 | — |
| `BO-997` | Real-Time Availability & Locking | listDetail | 1 | 0 | — |
| `BO-998` | Lock Timeout & Concurrency | listDetail | 2 | 0 | — |
| `BO-999` | Cart & Multi-Seat Management | listDetail | 2 | 0 | — |
| `BO-1000` | Mobile & Accessible Selection | listDetail | 2 | 0 | — |
| `BO-1001` | View Preview, Compare & Heat Map | listDetail | 1 | 0 | — |
| `BO-1002` | AI Conversational Seat Assistant | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-993, BO-994, BO-995, BO-996, BO-997, BO-998, BO-999, BO-1000, BO-1001, BO-1002 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-993",
  "name": "Experience Command Center",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "5",
   "number": "01",
   "page": 22
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/experience-command-center-bo-993",
   "component": "apps/venue-management-web/src/routes/access-venue/ExperienceCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-1000",
    "BO-1001",
    "BO-1002",
    "BO-994",
    "BO-995",
    "BO-996",
    "BO-997",
    "BO-998",
    "BO-999"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "BO-994",
     "trigger": "Choose My Seats",
     "provenance": "structural — pack board 5 wiring, 19 September 2026"
    },
    {
     "to": "BO-995",
     "trigger": "Find Seats For Me",
     "provenance": "structural — pack board 5 wiring, 19 September 2026"
    },
    {
     "to": "BO-996",
     "trigger": "Filters & Interactive Legend",
     "provenance": "structural — pack board 5 wiring, 19 September 2026"
    },
    {
     "to": "BO-997",
     "trigger": "Real-Time Availability & Locking",
     "provenance": "structural — pack board 5 wiring, 19 September 2026"
    },
    {
     "to": "BO-998",
     "trigger": "Lock Timeout & Concurrency",
     "provenance": "structural — pack board 5 wiring, 19 September 2026"
    },
    {
     "to": "BO-999",
     "trigger": "Cart & Multi-Seat Management",
     "provenance": "structural — pack board 5 wiring, 19 September 2026"
    },
    {
     "to": "BO-1000",
     "trigger": "Mobile & Accessible Selection",
     "provenance": "structural — pack board 5 wiring, 19 September 2026"
    },
    {
     "to": "BO-1001",
     "trigger": "View Preview, Compare & Heat Map",
     "provenance": "structural — pack board 5 wiring, 19 September 2026"
    },
    {
     "to": "BO-1002",
     "trigger": "AI Conversational Seat Assistant",
     "provenance": "structural — pack board 5 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Monitor seat-selection performance, availability quality and conversion across channels. Show map loads, searches, selections, locks, expiries, carts, checkout conversion, abandonment and revenue. Compare web, mobile, POS, call center, box office, B2B and API channels by venue and performance. Surface slow maps, stale availability, lock conflicts, high timeout and selection drop-off with drill-down. All channels shall use the same authoritative availability, lock and pricing services; no channel may maintain an independent seat-state cache beyond approved freshness rules. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 22"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 22"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "detailPanel",
       "derived": true,
       "impliedBy": "getSeatingRules",
       "notes": "One record, read-only."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "setSeatingRules",
       "label": "Save seating rules",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setSeatingRules"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The experience list.",
   "error": "Could not load. Names which read failed and leaves the experience untouched.",
   "emptyFirstRun": "No experience yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the experience are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getSeatingRules",
    "contract": "seating",
    "purpose": "Rules in force",
    "trigger": "onAction"
   },
   {
    "operationId": "setSeatingRules",
    "contract": "seating",
    "purpose": "Best-seat ranking, per map",
    "trigger": "onAction",
    "invalidates": [
     "getSeatingRules"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-993",
   "workshopBoard": "wireframes/WS144 Seat Management Venue Mapping Reference v1.0 Board 5.dc.html#bo-993"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 22. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "seatMapId",
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
  "id": "BO-994",
  "name": "Choose My Seats",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "5",
   "number": "02",
   "page": 22
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/choose-my-seats-bo-994",
   "component": "apps/venue-management-web/src/routes/access-venue/ChooseMySeats.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-993"
   ],
   "exitTo": [
    "BO-993"
   ],
   "transitions": [
    {
     "to": "BO-993",
     "trigger": "Back to Experience Command Center",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "seatMapId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow a guest or authorized agent to select exact seats from an interactive map. Display section, row, seat, price, fees, type, view quality, accessibility, amenity and live availability. Support zoom, pan, section drill-down, keyboard navigation, clear selection and a live basket summary. Acquire locks only after server confirmation and clearly distinguish selected, unavailable, locked and accessible inventory. All channels shall use the same authoritative availability, lock and pricing services; no channel may maintain an independent seat-state cache beyond approved freshness rules. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 22"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 22"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "detailPanel",
       "derived": true,
       "impliedBy": "getSeatAvailability",
       "notes": "One record, read-only."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createSeatHold",
       "label": "Create seat hold",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createSeatHold"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The choose seats list.",
   "error": "Could not load. Names which read failed and leaves the choose seats untouched.",
   "emptyFirstRun": "No choose seats yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the choose seats are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getSeatAvailability",
    "contract": "seating",
    "purpose": "What the guest can choose",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "createSeatHold",
    "contract": "seating",
    "purpose": "Hold the selection",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-994",
   "workshopBoard": "wireframes/WS144 Seat Management Venue Mapping Reference v1.0 Board 5.dc.html#bo-994"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 22. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-995",
  "name": "Find Seats For Me",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "5",
   "number": "03",
   "page": 22
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/find-seats-for-me-bo-995",
   "component": "apps/venue-management-web/src/routes/access-venue/FindSeatsForMe.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-993"
   ],
   "exitTo": [
    "BO-993"
   ],
   "transitions": [
    {
     "to": "BO-993",
     "trigger": "Back to Experience Command Center",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Return best-available seat groups from stated customer preferences. Capture quantity, zone, level, price range, accessibility, aisle, view, amenity and proximity preferences. Rank valid contiguous or near-contiguous groups with total price, view summary, match score and trade-offs. Allow selection, alternative search and return to exact map without losing the current cart context. All channels shall use the same authoritative availability, lock and pricing services; no channel may maintain an independent seat-state cache beyond approved freshness rules. Configuration Scope of Work | Version 1.0 22 Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 22"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 22"
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
       "impliedBy": "assignSeats",
       "label": "Assign seats",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "assignSeats"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The find seats for list.",
   "error": "Could not load. Names which read failed and leaves the find seats for untouched.",
   "emptyFirstRun": "No find seats for yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the find seats for are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "assignSeats",
    "contract": "seating",
    "purpose": "Pick and hold the best available seats",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-995",
   "workshopBoard": "wireframes/WS144 Seat Management Venue Mapping Reference v1.0 Board 5.dc.html#bo-995"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 22. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-996",
  "name": "Filters & Interactive Legend",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "5",
   "number": "04",
   "page": 23
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/filters-interactive-legend-bo-996",
   "component": "apps/venue-management-web/src/routes/access-venue/FiltersInteractiveLegend.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-993"
   ],
   "exitTo": [
    "BO-993"
   ],
   "transitions": [
    {
     "to": "BO-993",
     "trigger": "Back to Experience Command Center",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "seatMapId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Make large and complex seat maps understandable and searchable. Provide zone, price, group size, amenities, seat type, accessibility, view quality, level and availability filters. Update results, counts, map emphasis and legend in real time without hiding selected seats unexpectedly. Configure tenant/venue labels and colors while maintaining accessible contrast and non-color status cues. All channels shall use the same authoritative availability, lock and pricing services; no channel may maintain an independent seat-state cache beyond approved freshness rules. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 23"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 23"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "detailPanel",
       "derived": true,
       "impliedBy": "getSeatAvailability",
       "notes": "One record, read-only."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The filters interactive legend list.",
   "error": "Could not load. Names which read failed and leaves the filters interactive legend untouched.",
   "emptyFirstRun": "No filters interactive legend yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the filters interactive legend are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getSeatAvailability",
    "contract": "seating",
    "purpose": "Filtered availability",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-996",
   "workshopBoard": "wireframes/WS144 Seat Management Venue Mapping Reference v1.0 Board 5.dc.html#bo-996"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 23. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-997",
  "name": "Real-Time Availability & Locking",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "5",
   "number": "05",
   "page": 23
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/real-time-availability-locking-bo-997",
   "component": "apps/venue-management-web/src/routes/access-venue/RealTimeAvailabilityLocking.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-993"
   ],
   "exitTo": [
    "BO-993"
   ],
   "transitions": [
    {
     "to": "BO-993",
     "trigger": "Back to Experience Command Center",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Show and control atomic seat locks during selection. Display lock owner class, channel, transaction, acquisition time, expiry and current authoritative state to permitted roles. Broadcast lock, unlock, sale, hold, block and availability events to active selection sessions. Handle lock rejection, partial group success, lost connectivity and stale version with clear recovery options. All channels shall use the same authoritative availability, lock and pricing services; no channel may maintain an independent seat-state cache beyond approved freshness rules. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 23"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 23"
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
       "impliedBy": "listRealTimeAvailability",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The real-time availability locking list.",
   "error": "Could not load. Names which read failed and leaves the real-time availability locking untouched.",
   "emptyFirstRun": "No real-time availability locking yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the real-time availability locking are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listRealTimeAvailability",
    "contract": "promotions",
    "purpose": "Real-Time Availability & Checkout Validation",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-997",
   "workshopBoard": "wireframes/WS144 Seat Management Venue Mapping Reference v1.0 Board 5.dc.html#bo-997"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 23. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-998",
  "name": "Lock Timeout & Concurrency",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "5",
   "number": "06",
   "page": 23
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/lock-timeout-concurrency-bo-998",
   "component": "apps/venue-management-web/src/routes/access-venue/LockTimeoutConcurrency.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-993"
   ],
   "exitTo": [
    "BO-993"
   ],
   "transitions": [
    {
     "to": "BO-993",
     "trigger": "Back to Experience Command Center",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure fair timeout and collision behavior under concurrent demand. Set default lock duration, warning, grace period, extension policy, maximum extension and auto-release by channel or event. Configure optimistic concurrency, version checks, idempotency, conflict messages and retry boundaries. Simulate multiple customers selecting the same inventory and verify that no double lock or oversell can occur. All channels shall use the same authoritative availability, lock and pricing services; no channel may maintain an independent seat-state cache beyond approved freshness rules. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 23"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 23"
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
       "impliedBy": "extendSeatHold",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "destructiveButton",
       "derived": true,
       "impliedBy": "relinquishSeatHold",
       "notes": "**Always confirms, never the default focus.** The consequence goes in the body — which seat hold is affected and what goes with it, in the screen's own words; *are you sure* is not a confirmation."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "extendSeatHold"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The lock timeout concurrency list.",
   "error": "Could not load. Names which read failed and leaves the lock timeout concurrency untouched.",
   "emptyFirstRun": "No lock timeout concurrency yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the lock timeout concurrency are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "extendSeatHold",
    "contract": "seating",
    "purpose": "Extend before it lapses",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "relinquishSeatHold",
    "contract": "seating",
    "purpose": "Release on abandonment",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-998",
   "workshopBoard": "wireframes/WS144 Seat Management Venue Mapping Reference v1.0 Board 5.dc.html#bo-998"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 23. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "holdId",
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
  "id": "BO-999",
  "name": "Cart & Multi-Seat Management",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "5",
   "number": "07",
   "page": 23
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/cart-multi-seat-management-bo-999",
   "component": "apps/venue-management-web/src/routes/access-venue/CartMultiSeatManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-993"
   ],
   "exitTo": [
    "BO-993"
   ],
   "transitions": [
    {
     "to": "BO-993",
     "trigger": "Back to Experience Command Center",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Manage several seats as one controlled cart allocation. List each seat, assigned guest, ticket type, price, fee, promotion, lock expiry and eligibility status. Support add, remove, replace, reassign, save-for-later where permitted and clear-cart actions. Revalidate availability, price, eligibility and adjacency before checkout and release all abandoned locks reliably. All channels shall use the same authoritative availability, lock and pricing services; no channel may maintain an independent seat-state cache beyond approved freshness rules. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history. Configuration Scope of Work | Version 1.0 23",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 23"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 23"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "detailPanel",
       "derived": true,
       "impliedBy": "getSeatHold",
       "notes": "One record, read-only."
      },
      {
       "kind": "destructiveButton",
       "derived": true,
       "impliedBy": "relinquishSeatHold",
       "notes": "**Always confirms, never the default focus.** The consequence goes in the body — which seat hold is affected and what goes with it, in the screen's own words; *are you sure* is not a confirmation."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "relinquishSeatHold"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The cart multi-seat list.",
   "error": "Could not load. Names which read failed and leaves the cart multi-seat untouched.",
   "emptyFirstRun": "No cart multi-seat yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the cart multi-seat are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getSeatHold",
    "contract": "seating",
    "purpose": "What is in the cart",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "relinquishSeatHold",
    "contract": "seating",
    "purpose": "Remove one",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-999",
   "workshopBoard": "wireframes/WS144 Seat Management Venue Mapping Reference v1.0 Board 5.dc.html#bo-999"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 23. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "holdId",
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
  "id": "BO-1000",
  "name": "Mobile & Accessible Selection",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "5",
   "number": "08",
   "page": 24
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/mobile-accessible-selection-bo-1000",
   "component": "apps/venue-management-web/src/routes/access-venue/MobileAccessibleSelection.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-993"
   ],
   "exitTo": [
    "BO-993"
   ],
   "transitions": [
    {
     "to": "BO-993",
     "trigger": "Back to Experience Command Center",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "seatMapId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Deliver an equivalent and WCAG-aligned selection flow on supported devices. Provide responsive map/list modes, large targets, screen-reader labels, logical focus order, keyboard and switch access. Support high contrast, text scaling, reduced motion and clear wheelchair, companion, aisle and route information. Maintain selection and lock state through rotation, app backgrounding, network interruption and session recovery. All channels shall use the same authoritative availability, lock and pricing services; no channel may maintain an independent seat-state cache beyond approved freshness rules. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 24"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 24"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "detailPanel",
       "derived": true,
       "impliedBy": "getSeatAvailability",
       "notes": "One record, read-only."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The mobile accessible selection list.",
   "error": "Could not load. Names which read failed and leaves the mobile accessible selection untouched.",
   "emptyFirstRun": "No mobile accessible selection yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the mobile accessible selection are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getSeatAvailability",
    "contract": "seating",
    "purpose": "Accessible and mobile selection",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "getAccessibleSeating",
    "contract": "seating",
    "purpose": "Which seats and routes",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1000",
   "workshopBoard": "wireframes/WS144 Seat Management Venue Mapping Reference v1.0 Board 5.dc.html#bo-1000"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 24. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1001",
  "name": "View Preview, Compare & Heat Map",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "5",
   "number": "09",
   "page": 24
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/view-preview-compare-heat-map-bo-1001",
   "component": "apps/venue-management-web/src/routes/access-venue/ViewPreviewCompareHeatMap.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-993"
   ],
   "exitTo": [
    "BO-993"
   ],
   "transitions": [
    {
     "to": "BO-993",
     "trigger": "Back to Experience Command Center",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Help customers understand qualitative and demand differences before choosing. Show approved seat-view previews or representative section views with source, freshness and obstruction disclosure. Compare seats by price, distance, view, level, amenities, accessibility and overall match. Display configurable demand, price or availability heat maps without revealing sensitive sales strategy. All channels shall use the same authoritative availability, lock and pricing services; no channel may maintain an independent seat-state cache beyond approved freshness rules. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 24"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 24"
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
   "loading": "The view preview compare list.",
   "error": "Could not load. Names which read failed and leaves the view preview compare untouched.",
   "emptyFirstRun": "No view preview compare yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the view preview compare are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "recommendSeats",
    "contract": "seating",
    "purpose": "Compare and preview",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1001",
   "workshopBoard": "wireframes/WS144 Seat Management Venue Mapping Reference v1.0 Board 5.dc.html#bo-1001"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 24. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1002",
  "name": "AI Conversational Seat Assistant",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "5",
   "number": "10",
   "page": 24
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/ai-conversational-seat-assistant-bo-1002",
   "component": "apps/venue-management-web/src/routes/access-venue/AiConversationalSeatAssistant.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-993"
   ],
   "exitTo": [
    "BO-993"
   ],
   "transitions": [
    {
     "to": "BO-993",
     "trigger": "Back to Experience Command Center",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow natural-language seat discovery through governed AI. Understand requests such as family size, budget, view, aisle, stage proximity, accessibility and preferred level. Return only currently valid seat groups with match score, rationale, trade-offs, total price and add-to-cart action. Record model/version and feedback, disclose uncertainty and prevent AI from bypassing locks, pricing, eligibility or accessible-seat rules. All channels shall use the same authoritative availability, lock and pricing services; no channel may maintain an independent seat-state cache beyond approved freshness rules. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history. Configuration Scope of Work | Version 1.0 24 Board 6 - Holds, Blocks & Inventory Controls Figure 6. High-definition configuration board with all 10 screens. Visual reference: information architecture and configuration coverage; detailed production behavior is defined in the following scope. Configuration Scope of Work | Version 1.0 25",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 24"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 24"
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
   "loading": "The conversational seat assistant list.",
   "error": "Could not load. Names which read failed and leaves the conversational seat assistant untouched.",
   "emptyFirstRun": "No conversational seat assistant yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the conversational seat assistant are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "recommendSeats",
    "contract": "seating",
    "purpose": "What the assistant proposes",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1002",
   "workshopBoard": "wireframes/WS144 Seat Management Venue Mapping Reference v1.0 Board 5.dc.html#bo-1002"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 24. 0 of 0 labels bound to a contract property; 0 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 }
]
```

## `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
 "assignSeats": {
  "method": "POST",
  "path": "/performances/{performanceId}/assign-seats",
  "contract": "seating",
  "summary": "Pick and hold the best available seats",
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
  "responds": null
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
 "extendSeatHold": {
  "method": "POST",
  "path": "/seat-holds/{holdId}/extend",
  "contract": "seating",
  "summary": "Extend a hold",
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
  "responds": "SeatHold"
 },
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
 "getSeatHold": {
  "method": "GET",
  "path": "/seat-holds/{holdId}",
  "contract": "seating",
  "summary": "Read a hold",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "SeatHold"
 },
 "getSeatingRules": {
  "method": "GET",
  "path": "/seat-maps/{seatMapId}/rules",
  "contract": "seating",
  "summary": "Read seating rules",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "SeatingRules"
 },
 "listRealTimeAvailability": {
  "method": "GET",
  "path": "/real-time-availability",
  "contract": "promotions",
  "summary": "Real-Time Availability & Checkout Validation",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "RealTimeAvailabilityCheckoutValidationView"
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
 "relinquishSeatHold": {
  "method": "DELETE",
  "path": "/seat-holds/{holdId}",
  "contract": "seating",
  "summary": "Release a hold",
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
  "responds": null
 },
 "setSeatingRules": {
  "method": "PUT",
  "path": "/seat-maps/{seatMapId}/rules",
  "contract": "seating",
  "summary": "Set seating rules",
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
  "requestBody": "SeatingRules",
  "responds": "SeatingRules"
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
 "CreateSeatHoldRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "id",
   "performanceId",
   "seatIds"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "performanceId": {
    "type": "string",
    "format": "uuid"
   },
   "seatIds": {
    "type": "array",
    "minItems": 1,
    "maxItems": 50,
    "description": "50 is the ceiling of the venue setting, not the limit a caller gets. On a guest channel the limit is `VenueSettings.seating.maxSeatsPerGuestOrder` (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); on a staff channel it stays 10 per sale (audit R080 (c)), as POS-002 shows. Either is refused with `422` `seat-limit-exceeded`.\n",
    "items": {
     "type": "string"
    }
   },
   "ttlSeconds": {
    "type": "integer",
    "minimum": 60,
    "maximum": 1800,
    "default": 480,
    "description": "**8 minutes by default, extendable to 30 in all** (decided 28 September, audit R169). Left out, the hold lasts 480 seconds. No hold, first grant or extended, outlives 1800 seconds from its creation.\n"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid"
   }
  }
 },
 "Money": {
  "type": "object",
  "x-ticvai-persistence-kind": "valueObject",
  "x-ticvai-persistence-column": "numeric(18,4)",
  "description": "**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n",
  "required": [
   "amount",
   "currency",
   "scale"
  ],
  "properties": {
   "amount": {
    "type": "string",
    "description": "Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n",
    "pattern": "^-?\\d+(\\.\\d{1,4})?$"
   },
   "currency": {
    "type": "string",
    "description": "**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n",
    "pattern": "^[A-Z]{3}$"
   },
   "scale": {
    "type": "integer",
    "description": "Resolved from the region alongside `currency`.",
    "minimum": 0,
    "maximum": 4
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
 "RealTimeAvailabilityCheckoutValidationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Real-Time Availability & Checkout Validation displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "failedChecks": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "productInactive",
      "inventoryUnavailable",
      "capacityUnavailable",
      "timeslotUnavailable",
      "resourceUnavailable",
      "priceInvalid",
      "promotionInvalid",
      "partnerComponentInvalid",
      "componentMappingInvalid"
     ]
    },
    "description": "Checkout validations that failed; empty means the bundle is sellable."
   },
   "bundleId": {
    "type": "string",
    "description": "Bundle ID"
   },
   "sellable": {
    "type": "boolean",
    "description": "Whether the bundle can be sold now"
   }
  }
 },
 "SeatAttribute": {
  "type": "string",
  "description": "BL-168. **Extended from eight values on 18 August.** Amenity and view filters needed attributes the original set did not carry, and a guest filtering for *aisle seat with power* was filtering on something the model could not express.\n",
  "enum": [
   "standard",
   "accessible",
   "companion",
   "obstructedView",
   "restrictedLegroom",
   "premium",
   "houseSeat",
   "buffer",
   "aisle",
   "endOfRow",
   "extraLegroom",
   "powerOutlet",
   "tableService",
   "shaded",
   "covered",
   "nearExit",
   "nearAccessibleWc",
   "wheelchairTransfer",
   "limitedRecline",
   "sofa",
   "beanbag"
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
    "x-ticvai-column": "gross_amount",
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
 "SeatingRules": {
  "x-ticvai-persistence": "seating.seating_rules",
  "type": "object",
  "required": [
   "seatMapId"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "seatMapId": {
    "type": "string",
    "format": "uuid"
   },
   "bufferSeats": {
    "type": "integer",
    "minimum": 0,
    "default": 0,
    "description": "Seats kept empty either side of a sold party."
   },
   "bufferRows": {
    "type": "integer",
    "minimum": 0,
    "default": 0
   },
   "preventOrphanSeats": {
    "type": "boolean",
    "default": false,
    "description": "Refuse a selection that would leave a single unsellable seat between parties. Operators want this and rarely ask for it by name.\n"
   },
   "maxPartySize": {
    "type": "integer",
    "nullable": true
   },
   "requireContiguous": {
    "type": "boolean",
    "default": false,
    "description": "A party must sit together or the selection is refused."
   },
   "accessibleCompanionCount": {
    "type": "integer",
    "default": 1,
    "description": "Companion seats sold alongside each accessible space."
   },
   "allowSplitAcrossRows": {
    "type": "boolean",
    "default": true
   }
  }
 }
}
```
