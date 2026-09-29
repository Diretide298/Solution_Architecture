# WS90 — Rental Management board 3

**10 screens · 7 operations · 7 schemas · 5 permissions**

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
  `PRICE_VIEW, RENTAL_CONFIGURE, RENTAL_MANAGE, RENTAL_VIEW, RESOURCE_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-514` | Availability Command Center | commandCentre | 1 | 0 | — |
| `BO-515` | Availability Rule Configuration | configEditor | 1 | 0 | — |
| `BO-516` | Operating Hours & Rental Windows | listDetail | 1 | 0 | — |
| `BO-517` | Timeslot & Duration Availability Setup | configEditor | 1 | 0 | — |
| `BO-518` | Real-Time Availability Calendar | listDetail | 2 | 0 | — |
| `BO-519` | Resource / Equipment Calendar | listDetail | 1 | 0 | — |
| `BO-520` | Blackout, Closure & Capacity Blocking | listDetail | 3 | 0 | — |
| `BO-521` | Overlap & Conflict Engine | listDetail | 1 | 0 | — |
| `BO-522` | Inventory Holds, Buffers & Release Rules | listDetail | 1 | 0 | — |
| `BO-523` | Availability Intelligence & AI Forecasting | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-516, BO-518, BO-520, BO-522, BO-523 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-514",
  "name": "Availability Command Center",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "3",
   "number": "1",
   "page": 27
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/availability-command-center-bo-514",
   "component": "apps/venue-management-web/src/routes/rentals/AvailabilityCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-515",
    "BO-516",
    "BO-517",
    "BO-518",
    "BO-519",
    "BO-520",
    "BO-521",
    "BO-522",
    "BO-523"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 3 wiring, 11 September 2026",
     "back": true
    },
    {
     "to": "BO-515",
     "trigger": "Availability Rule Configuration",
     "provenance": "structural — pack board 3 wiring, 11 September 2026",
     "carries": [
      "productId"
     ]
    },
    {
     "to": "BO-516",
     "trigger": "Operating Hours & Rental Windows",
     "provenance": "structural — pack board 3 wiring, 11 September 2026",
     "carries": [
      "productId"
     ]
    },
    {
     "to": "BO-517",
     "trigger": "Timeslot & Duration Availability Setup",
     "provenance": "structural — pack board 3 wiring, 11 September 2026",
     "carries": [
      "productId"
     ]
    },
    {
     "to": "BO-518",
     "trigger": "Real-Time Availability Calendar",
     "provenance": "structural — pack board 3 wiring, 11 September 2026"
    },
    {
     "to": "BO-519",
     "trigger": "Resource / Equipment Calendar",
     "provenance": "structural — pack board 3 wiring, 11 September 2026"
    },
    {
     "to": "BO-520",
     "trigger": "Blackout, Closure & Capacity Blocking",
     "provenance": "structural — pack board 3 wiring, 11 September 2026",
     "carries": [
      "productId"
     ]
    },
    {
     "to": "BO-521",
     "trigger": "Overlap & Conflict Engine",
     "provenance": "structural — pack board 3 wiring, 11 September 2026"
    },
    {
     "to": "BO-522",
     "trigger": "Inventory Holds, Buffers & Release Rules",
     "provenance": "structural — pack board 3 wiring, 11 September 2026",
     "carries": [
      "productId"
     ]
    },
    {
     "to": "BO-523",
     "trigger": "Availability Intelligence & AI Forecasting",
     "provenance": "structural — pack board 3 wiring, 11 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide management and operators with a real-time overview of rental availability across all locations.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search availability",
       "provenance": "pack Rental_Management.pdf, page 27 §Filters"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Tenant",
        "Venue",
        "Rental Location",
        "Product",
        "Category",
        "Date",
        "Time",
        "Availability Status"
       ],
       "notes": "The pack filters this screen by tenant, venue, rental location, product, category, date and 2 more — which are present is a decision the pack already made.",
       "provenance": "pack Rental_Management.pdf, page 27 §Filters"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Total Rentable Inventory",
       "provenance": "pack Rental_Management.pdf, page 27 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Available Now",
       "provenance": "pack Rental_Management.pdf, page 27 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Reserved",
       "provenance": "pack Rental_Management.pdf, page 27 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Currently Rented",
       "provenance": "pack Rental_Management.pdf, page 27 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Maintenance Blocked",
       "provenance": "pack Rental_Management.pdf, page 27 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Operationally Blocked",
       "provenance": "pack Rental_Management.pdf, page 27 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Next 2 Hours Demand",
       "provenance": "pack Rental_Management.pdf, page 27 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Availability Risk",
       "provenance": "pack Rental_Management.pdf, page 27 §KPI Cards"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The availability list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the availability untouched.",
   "emptyFirstRun": "No availability yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the availability are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getRentalAvailability",
    "contract": "rental",
    "purpose": "What is free, across products",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Total Rentable Inventory",
    "Available Now",
    "Reserved",
    "Currently Rented",
    "Maintenance Blocked",
    "Operationally Blocked"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-514",
   "workshopBoard": "wireframes/WS118 Rental Management Board 3.dc.html#bo-514"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 27. 0 of 8 labels bound to a contract property; 16 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-515",
  "name": "Availability Rule Configuration",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "3",
   "number": "2",
   "page": 28
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/availability-rule-configuration-bo-515",
   "component": "apps/venue-management-web/src/routes/rentals/AvailabilityRuleConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-514"
   ],
   "exitTo": [
    "BO-514"
   ],
   "transitions": [
    {
     "to": "BO-514",
     "trigger": "Back to Availability Command Center",
     "provenance": "structural — pack board 3 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure availability according to; Configuration) and no display directory — it is settings, not a population",
  "purpose": "Define the fundamental rules used by the availability engine for each rental product.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Physical inventory",
       "provenance": "pack Rental_Management.pdf, page 28 §Configure availability according to"
      },
      {
       "kind": "selectField",
       "label": "Location allocation",
       "provenance": "pack Rental_Management.pdf, page 28 §Configure availability according to"
      },
      {
       "kind": "selectField",
       "label": "Existing reservations",
       "provenance": "pack Rental_Management.pdf, page 28 §Configure availability according to"
      },
      {
       "kind": "selectField",
       "label": "Active rentals",
       "provenance": "pack Rental_Management.pdf, page 28 §Configure availability according to"
      },
      {
       "kind": "selectField",
       "label": "Maintenance blocks",
       "provenance": "pack Rental_Management.pdf, page 28 §Configure availability according to"
      },
      {
       "kind": "selectField",
       "label": "Out-of-service assets",
       "provenance": "pack Rental_Management.pdf, page 28 §Configure availability according to"
      },
      {
       "kind": "selectField",
       "label": "Inventory buffer",
       "provenance": "pack Rental_Management.pdf, page 28 §Configure availability according to"
      },
      {
       "kind": "selectField",
       "label": "Turnaround time",
       "provenance": "pack Rental_Management.pdf, page 28 §Configure availability according to"
      },
      {
       "kind": "selectField",
       "label": "Operating hours",
       "provenance": "pack Rental_Management.pdf, page 28 §Configure availability according to"
      },
      {
       "kind": "selectField",
       "label": "Booking Availability: ON",
       "provenance": "pack Rental_Management.pdf, page 28 §Configuration"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The availability rule configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the availability rule untouched.",
   "emptyFirstRun": "No availability rule configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setRentalAvailabilityRules",
    "contract": "rental",
    "purpose": "Windows, slots and holds",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getRentalAvailability"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-515",
   "workshopBoard": "wireframes/WS118 Rental Management Board 3.dc.html#bo-515"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 28. 0 of 0 labels bound to a contract property; 10 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "productId",
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
  "id": "BO-516",
  "name": "Operating Hours & Rental Windows",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "3",
   "number": "3",
   "page": 29
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/operating-hours-rental-windows-bo-516",
   "component": "apps/venue-management-web/src/routes/rentals/OperatingHoursRentalWindows.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-514"
   ],
   "exitTo": [
    "BO-514"
   ],
   "transitions": [
    {
     "to": "BO-514",
     "trigger": "Back to Availability Command Center",
     "provenance": "structural — pack board 3 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Control when rental products can actually be booked and used. The source specifically requires inventory allocation according to operating hours.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 29"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 29"
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
       "impliedBy": "setRentalAvailabilityRules",
       "label": "Save",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setRentalAvailabilityRules"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The operating hours rental list.",
   "error": "Could not load. Names which read failed and leaves the operating hours rental untouched.",
   "emptyFirstRun": "No operating hours rental yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the operating hours rental are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setRentalAvailabilityRules",
    "contract": "rental",
    "purpose": "Operating hours and rental windows",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getRentalAvailability"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-516",
   "workshopBoard": "wireframes/WS118 Rental Management Board 3.dc.html#bo-516"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 29. 0 of 0 labels bound to a contract property; 0 of 21 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "productId",
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
  "id": "BO-517",
  "name": "Timeslot & Duration Availability Setup",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "3",
   "number": "4",
   "page": 30
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/timeslot-duration-availability-setup-bo-517",
   "component": "apps/venue-management-web/src/routes/rentals/TimeslotDurationAvailabilitySetup.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-514"
   ],
   "exitTo": [
    "BO-514"
   ],
   "transitions": [
    {
     "to": "BO-514",
     "trigger": "Back to Availability Command Center",
     "provenance": "structural — pack board 3 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Duration options; Configuration) and no display directory — it is settings, not a population",
  "purpose": "Configure how rental availability is presented to customers. The source supports both fixed and customer-defined rental periods.",
  "gaps": [
   {
    "operation": null,
    "why": "**Timeslot & Duration Availability Setup declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   }
  ],
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Slot Interval",
       "provenance": "pack Rental_Management.pdf, page 30 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Fixed/Flexible Start",
       "provenance": "pack Rental_Management.pdf, page 30 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Allowed Durations",
       "provenance": "pack Rental_Management.pdf, page 30 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Minimum Duration",
       "provenance": "pack Rental_Management.pdf, page 30 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Maximum Duration",
       "provenance": "pack Rental_Management.pdf, page 30 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Turnaround Time",
       "provenance": "pack Rental_Management.pdf, page 30 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Booking Cutoff",
       "provenance": "pack Rental_Management.pdf, page 30 §Configuration"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The timeslot duration availability configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the timeslot duration availability untouched.",
   "emptyFirstRun": "No timeslot duration availability configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setRentalDurationRules",
    "contract": "rental",
    "purpose": "Slot and duration setup",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getRentalProduct",
     "getRentalAvailability"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-517",
   "workshopBoard": "wireframes/WS118 Rental Management Board 3.dc.html#bo-517"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 30. 0 of 0 labels bound to a contract property; 7 of 17 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "productId",
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
  "id": "BO-518",
  "name": "Real-Time Availability Calendar",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "3",
   "number": "5",
   "page": 31
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/real-time-availability-calendar-bo-518",
   "component": "apps/venue-management-web/src/routes/rentals/RealTimeAvailabilityCalendar.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-514"
   ],
   "exitTo": [
    "BO-514"
   ],
   "transitions": [
    {
     "to": "BO-514",
     "trigger": "Back to Availability Command Center",
     "provenance": "structural — pack board 3 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide the operational calendar explicitly required by the source.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 31"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 31"
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
   "loading": "The real-time availability calendar list.",
   "error": "Could not load. Names which read failed and leaves the real-time availability calendar untouched.",
   "emptyFirstRun": "No real-time availability calendar yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the real-time availability calendar are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listRealTimeAvailability",
    "contract": "promotions",
    "purpose": "Real-Time Availability & Checkout Validation",
    "trigger": "onLoad"
   },
   {
    "operationId": "getRentalAvailability",
    "contract": "rental",
    "purpose": "Live availability",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-518",
   "workshopBoard": "wireframes/WS118 Rental Management Board 3.dc.html#bo-518"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 31. 0 of 0 labels bound to a contract property; 0 of 16 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-519",
  "name": "Resource / Equipment Calendar",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "3",
   "number": "6",
   "page": 31
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/resource-equipment-calendar-bo-519",
   "component": "apps/venue-management-web/src/routes/rentals/ResourceEquipmentCalendar.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-514"
   ],
   "exitTo": [
    "BO-514"
   ],
   "transitions": [
    {
     "to": "BO-514",
     "trigger": "Back to Availability Command Center",
     "provenance": "structural — pack board 3 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide asset-level availability for serialized inventory.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 31"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "filters",
     "slot": "filters",
     "components": [
      {
       "kind": "datePicker",
       "label": "From",
       "operation": "getResourceCalendar",
       "notes": "Sends `?from=` (required).",
       "provenance": "contract resources.yaml GET /resource-calendar"
      },
      {
       "kind": "datePicker",
       "label": "To",
       "operation": "getResourceCalendar",
       "notes": "Sends `?to=` (required).",
       "provenance": "contract resources.yaml GET /resource-calendar"
      },
      {
       "kind": "selectField",
       "label": "Resource type",
       "operation": "getResourceCalendar",
       "notes": "Sends `?resourceTypeId=` (bikes, kayaks, watercraft, wheelchairs, cabanas).",
       "provenance": "contract resources.yaml GET /resource-calendar"
      },
      {
       "kind": "selectField",
       "label": "Category",
       "operation": "getResourceCalendar",
       "notes": "Sends `?categoryId=`.",
       "provenance": "contract resources.yaml GET /resource-calendar"
      },
      {
       "kind": "selectField",
       "label": "View",
       "operation": "getResourceCalendar",
       "notes": "Sends `?granularity=` (day, week, month, agenda).",
       "provenance": "contract resources.yaml GET /resource-calendar"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Equipment timeline",
       "bindsTo": "ResourceCalendarRow",
       "columns": [
        "ResourceCalendarRow.resourceName",
        "ResourceCalendarRow.resourceTypeId",
        "ResourceCalendarRow.utilisationPercent",
        "ResourceCalendarRow.segments"
       ],
       "operation": "getResourceCalendar",
       "notes": "One row per serialised resource; `segments` drawn as coloured blocks across the hours, as in the pack's BIKE-001 to BIKE-004 grid.",
       "provenance": "contract resources.yaml GET /resource-calendar"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected block",
       "bindsTo": "ResourceCalendarRow.segments",
       "columns": [
        "ResourceCalendarRow.segments[].from",
        "ResourceCalendarRow.segments[].to",
        "ResourceCalendarRow.segments[].state",
        "ResourceCalendarRow.segments[].bookingId",
        "ResourceCalendarRow.segments[].conflictsWith",
        "Customer",
        "Expected checkout",
        "Expected return",
        "Turnaround",
        "Equipment status",
        "Related maintenance"
       ],
       "operation": "getResourceCalendar",
       "notes": "The pack's block drill-down; only the reservation reference (`bookingId`) and state are bound.",
       "provenance": "pack Rental_Management.pdf, page 31"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The resource equipment calendar list.",
   "error": "Could not load. Names which read failed and leaves the resource equipment calendar untouched.",
   "emptyFirstRun": "No resource equipment calendar yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the resource equipment calendar are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getResourceCalendar",
    "contract": "resources",
    "purpose": "Equipment against time",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-519",
   "workshopBoard": "wireframes/WS118 Rental Management Board 3.dc.html#bo-519"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 31. 0 of 0 labels bound to a contract property; 0 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Layout drafted 29 September (VM close-out)** from pack Rental_Management.pdf p.31; contract resources.yaml GET /resource-calendar. Pack labels with no schema field yet (shown as plain labels): Customer, Expected checkout, Expected return, Turnaround (segment state), Return (segment state), Related maintenance.",
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
  "id": "BO-520",
  "name": "Blackout, Closure & Capacity Blocking",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "3",
   "number": "7",
   "page": 32
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/blackout-closure-capacity-blocking-bo-520",
   "component": "apps/venue-management-web/src/routes/rentals/BlackoutClosureCapacityBlocking.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-514"
   ],
   "exitTo": [
    "BO-514"
   ],
   "transitions": [
    {
     "to": "BO-514",
     "trigger": "Back to Availability Command Center",
     "provenance": "structural — pack board 3 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow authorized users to deliberately remove inventory from sale. The original scope requires seasonal availability, blackout dates and maintenance periods.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 32"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 32"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Selected weekdays",
       "provenance": "pack Rental_Management.pdf, page 32 §Support"
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
       "impliedBy": "createRentalBlackout"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The blackout closure capacity list.",
   "error": "Could not load. Names which read failed and leaves the blackout closure capacity untouched.",
   "emptyFirstRun": "No blackout closure capacity yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the blackout closure capacity are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createRentalBlackout",
    "contract": "rental",
    "purpose": "Close or reduce capacity",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getRentalAvailability"
    ]
   },
   {
    "operationId": "setRentalAvailabilityRules",
    "contract": "rental",
    "purpose": "Close the product on selected weekdays by removing them from its operating windows",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration): serves the pack action(s) Selected weekdays"
   },
   {
    "operationId": "listRentalProducts",
    "contract": "rental",
    "purpose": "The rental products whose availability is blocked",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-520",
   "workshopBoard": "wireframes/WS118 Rental Management Board 3.dc.html#bo-520"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 32. 0 of 0 labels bound to a contract property; 1 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Selected weekdays: `setRentalAvailabilityRules`.",
  "entryState": {
   "params": [
    {
     "name": "productId",
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
  "id": "BO-521",
  "name": "Overlap & Conflict Engine",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "3",
   "number": "8",
   "page": 33
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/overlap-conflict-engine-bo-521",
   "component": "apps/venue-management-web/src/routes/rentals/OverlapConflictEngine.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-514"
   ],
   "exitTo": [
    "BO-514"
   ],
   "transitions": [
    {
     "to": "BO-514",
     "trigger": "Back to Availability Command Center",
     "provenance": "structural — pack board 3 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide transparency into one of the most important calculations in the rental system. The original requirement explicitly states: Calculate overlapping rentals and prevent inventory conflicts.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 33"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "filters",
     "slot": "filters",
     "components": [
      {
       "kind": "selectField",
       "label": "Rental product",
       "operation": "getRentalAvailability",
       "notes": "Sends `?productId=` (required).",
       "provenance": "contract rental.yaml GET /rental-availability"
      },
      {
       "kind": "selectField",
       "label": "Location",
       "operation": "getRentalAvailability",
       "notes": "Sends `?locationId=`.",
       "provenance": "contract rental.yaml GET /rental-availability"
      },
      {
       "kind": "datePicker",
       "label": "From",
       "operation": "getRentalAvailability",
       "notes": "Sends `?from=` (required).",
       "provenance": "contract rental.yaml GET /rental-availability"
      },
      {
       "kind": "datePicker",
       "label": "To",
       "operation": "getRentalAvailability",
       "notes": "Sends `?to=` (required).",
       "provenance": "contract rental.yaml GET /rental-availability"
      },
      {
       "kind": "numberField",
       "label": "Quantity requested",
       "operation": "getRentalAvailability",
       "notes": "Sends `?quantity=`.",
       "provenance": "contract rental.yaml GET /rental-availability"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Sellable inventory",
       "bindsTo": "RentalAvailability.windows",
       "columns": [
        "RentalAvailability.windows[].availableQuantity"
       ],
       "operation": "getRentalAvailability",
       "notes": "The lowest `availableQuantity` across the requested period.",
       "provenance": "contract rental.yaml GET /rental-availability"
      },
      {
       "kind": "metricTile",
       "label": "Physical allocation",
       "columns": [
        "Physical allocation"
       ],
       "notes": "The pack asks for physical allocation; the contract has no field for it.",
       "provenance": "pack Rental_Management.pdf, page 33"
      },
      {
       "kind": "metricTile",
       "label": "Overlapping active rentals",
       "columns": [
        "Overlapping active rentals"
       ],
       "notes": "The pack asks for overlapping active rentals; the contract has no field for it.",
       "provenance": "pack Rental_Management.pdf, page 33"
      },
      {
       "kind": "metricTile",
       "label": "Safety buffer",
       "columns": [
        "Safety buffer"
       ],
       "notes": "The pack asks for safety buffer; the contract has no field for it.",
       "provenance": "pack Rental_Management.pdf, page 33"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Blocking windows (conflict types)",
       "bindsTo": "RentalAvailability.blockedWindows",
       "columns": [
        "RentalAvailability.blockedWindows[].from",
        "RentalAvailability.blockedWindows[].to",
        "RentalAvailability.blockedWindows[].reason"
       ],
       "operation": "getRentalAvailability",
       "notes": "`reason` covers booked, turnaround, maintenance, blackout, closed, buffer and held; the pack's rental-extension and location conflicts have no value.",
       "provenance": "contract rental.yaml GET /rental-availability"
      },
      {
       "kind": "dataTable",
       "label": "Available windows",
       "bindsTo": "RentalAvailability.windows",
       "columns": [
        "RentalAvailability.windows[].from",
        "RentalAvailability.windows[].to",
        "RentalAvailability.windows[].availableQuantity",
        "RentalAvailability.windows[].availableAssetIds"
       ],
       "operation": "getRentalAvailability",
       "notes": "The alternative times (\"14:30 - 10 available\") come from here.",
       "provenance": "contract rental.yaml GET /rental-availability"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "Alternative recommendation",
       "columns": [
        "Alternative location",
        "Available quantity there",
        "Alternative start time"
       ],
       "notes": "Alternative locations need a second read per location; the pack's Marina Station example is not returned by one call.",
       "provenance": "pack Rental_Management.pdf, page 33"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The overlap conflict list.",
   "error": "Could not load. Names which read failed and leaves the overlap conflict untouched.",
   "emptyFirstRun": "No overlap conflict yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the overlap conflict are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getRentalAvailability",
    "contract": "rental",
    "purpose": "Where bookings overlap",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-521",
   "workshopBoard": "wireframes/WS118 Rental Management Board 3.dc.html#bo-521"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 33. 0 of 0 labels bound to a contract property; 0 of 23 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Layout drafted 29 September (VM close-out)** from pack Rental_Management.pdf p.33; contract rental.yaml GET /rental-availability. Pack labels with no schema field yet (shown as plain labels): Physical allocation, Overlapping active rentals, Safety buffer, Existing reservations count, Maintenance count, Result (AVAILABLE / NOT AVAILABLE), Alternative location availability, Conflict types: rental extension overlap, location conflict.",
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
  "id": "BO-522",
  "name": "Inventory Holds, Buffers & Release Rules",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "3",
   "number": "9",
   "page": 34
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/inventory-holds-buffers-release-rules-bo-522",
   "component": "apps/venue-management-web/src/routes/rentals/InventoryHoldsBuffersReleaseRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-514"
   ],
   "exitTo": [
    "BO-514"
   ],
   "transitions": [
    {
     "to": "BO-514",
     "trigger": "Back to Availability Command Center",
     "provenance": "structural — pack board 3 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Control inventory that should temporarily or permanently be withheld from normal sales. The source explicitly requires configurable inventory buffers.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 34"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 34"
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
       "impliedBy": "setRentalAvailabilityRules",
       "label": "Save",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setRentalAvailabilityRules"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The inventory holds buffers list.",
   "error": "Could not load. Names which read failed and leaves the inventory holds buffers untouched.",
   "emptyFirstRun": "No inventory holds buffers yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the inventory holds buffers are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setRentalAvailabilityRules",
    "contract": "rental",
    "purpose": "Buffers and hold release",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getRentalAvailability"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-522",
   "workshopBoard": "wireframes/WS118 Rental Management Board 3.dc.html#bo-522"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 34. 0 of 0 labels bound to a contract property; 0 of 21 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "productId",
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
  "id": "BO-523",
  "name": "Availability Intelligence & AI Forecasting",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "3",
   "number": "10",
   "page": 34
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/availability-intelligence-ai-forecasting-bo-523",
   "component": "apps/venue-management-web/src/routes/rentals/AvailabilityIntelligenceAiForecasting.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-514"
   ],
   "exitTo": [
    "BO-514"
   ],
   "transitions": [
    {
     "to": "BO-514",
     "trigger": "Back to Availability Command Center",
     "provenance": "structural — pack board 3 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Use AI to forecast demand and proactively optimize rental availability. The source recommends AI-based utilization and demand forecasting.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Rental_Management.pdf, page 34 §Display"
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
       "label": "Every availability intelligence forecasting",
       "columns": [
        "Forecast Demand",
        "Forecast Utilization",
        "Sell-Out Probability",
        "Inventory Shortage Risk",
        "Excess Inventory",
        "Location Imbalance",
        "Expected Cancellations",
        "Expected Late Returns"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Rental_Management.pdf, page 34 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected availability intelligence forecasting",
       "bindsTo": null,
       "columns": [
        "Forecast Demand",
        "Forecast Utilization",
        "Sell-Out Probability",
        "Inventory Shortage Risk",
        "Excess Inventory",
        "Location Imbalance",
        "Expected Cancellations",
        "Expected Late Returns"
       ],
       "notes": "The pack groups this record's detail under its own headings: “North Station”, “Important Availability Formula”, “Allocated Physical Inventory”.",
       "provenance": "pack Rental_Management.pdf, page 34 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The availability intelligence forecasting list.",
   "error": "Could not load. Names which read failed and leaves the availability intelligence forecasting untouched.",
   "emptyFirstRun": "No availability intelligence forecasting yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the availability intelligence forecasting are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getRentalAvailability",
    "contract": "rental",
    "purpose": "Availability forecast",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Forecast Demand",
    "Forecast Utilization",
    "Sell-Out Probability",
    "Inventory Shortage Risk",
    "Excess Inventory",
    "Location Imbalance"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-523",
   "workshopBoard": "wireframes/WS118 Rental Management Board 3.dc.html#bo-523"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 34. 0 of 8 labels bound to a contract property; 8 of 36 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "createRentalBlackout": {
  "method": "POST",
  "path": "/rental-blackouts",
  "contract": "rental",
  "summary": "Close a product, location or window",
  "permission": "RENTAL_MANAGE",
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
  "requestBody": "RentalBlackout",
  "responds": "RentalBlackout"
 },
 "getRentalAvailability": {
  "method": "GET",
  "path": "/rental-availability",
  "contract": "rental",
  "summary": "What can be rented, when, with turnaround already subtracted",
  "permission": "RENTAL_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "productId",
    "in": "query",
    "required": true
   },
   {
    "name": "locationId",
    "in": "query",
    "required": null
   },
   {
    "name": "from",
    "in": "query",
    "required": true
   },
   {
    "name": "to",
    "in": "query",
    "required": true
   },
   {
    "name": "quantity",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "RentalAvailability"
 },
 "getResourceCalendar": {
  "method": "GET",
  "path": "/resource-calendar",
  "contract": "resources",
  "summary": "Every resource against time, with conflicts already marked",
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
   },
   {
    "name": "resourceTypeId",
    "in": "query",
    "required": null
   },
   {
    "name": "categoryId",
    "in": "query",
    "required": null
   },
   {
    "name": "granularity",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "ResourceCalendarRow"
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
 "listRentalProducts": {
  "method": "GET",
  "path": "/rental-products",
  "contract": "rental",
  "summary": "Rental products across venues and locations",
  "permission": "RENTAL_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "venueId",
    "in": "query",
    "required": null
   },
   {
    "name": "locationId",
    "in": "query",
    "required": null
   },
   {
    "name": "categoryId",
    "in": "query",
    "required": null
   },
   {
    "name": "trackingModel",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "RentalProduct"
 },
 "setRentalAvailabilityRules": {
  "method": "PUT",
  "path": "/rental-products/{productId}/availability-rules",
  "contract": "rental",
  "summary": "Operating hours, rental windows, buffers and release rules",
  "permission": "RENTAL_CONFIGURE",
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
  "requestBody": "RentalAvailabilityRules",
  "responds": "RentalAvailabilityRules"
 },
 "setRentalDurationRules": {
  "method": "PUT",
  "path": "/rental-products/{productId}/duration",
  "contract": "rental",
  "summary": "Minimum, maximum, increment, extension and turnaround",
  "permission": "RENTAL_CONFIGURE",
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
  "requestBody": "RentalDurationRules",
  "responds": "RentalDurationRules"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
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
 "RentalAvailability": {
  "type": "object",
  "description": "Board 3. **A pooled product answers with a count, a serialised one with assets.**",
  "properties": {
   "productId": {
    "type": "string",
    "format": "uuid"
   },
   "locationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "windows": {
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
      },
      "availableQuantity": {
       "type": "integer"
      },
      "availableAssetIds": {
       "type": "array",
       "items": {
        "type": "string",
        "format": "uuid"
       }
      }
     }
    }
   },
   "blockedWindows": {
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
      },
      "reason": {
       "type": "string",
       "enum": [
        "booked",
        "turnaround",
        "maintenance",
        "blackout",
        "closed",
        "buffer",
        "held"
       ]
      }
     }
    }
   }
  }
 },
 "RentalAvailabilityRules": {
  "type": "object",
  "x-ticvai-persistence": "rental.availability_rules",
  "description": "Boards 3.2, 3.3 and 3.9. **The hold-release rule is the one that quietly loses stock.**\n",
  "properties": {
   "operatingWindows": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "daysOfWeek": {
       "type": "array",
       "items": {
        "type": "string"
       }
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
   "slotMinutes": {
    "type": "integer",
    "nullable": true
   },
   "holdMinutes": {
    "type": "integer",
    "default": 15,
    "description": "**How long an unconfirmed basket keeps stock.** A hold that never expires removes inventory from sale after every abandoned checkout.\n"
   },
   "releaseOnPaymentFailure": {
    "type": "boolean",
    "default": true
   },
   "overbookPercent": {
    "type": "number",
    "default": 0
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "RentalBlackout": {
  "type": "object",
  "x-ticvai-persistence": "rental.blackout",
  "description": "Board 3.7. **Closure and capacity reduction are one act at different strengths.**",
  "required": [
   "from",
   "to",
   "reason"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "productId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "locationId": {
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
   "reason": {
    "type": "string"
   },
   "capacityPercent": {
    "type": "integer",
    "default": 0,
    "description": "Zero closes it; fifty halves it."
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "RentalDurationRules": {
  "type": "object",
  "x-ticvai-persistence": "rental.duration_rules",
  "description": "Board 1.7. **Turnaround feeds availability automatically.** *10:00–11:00 rental, 11:00–11:15 turnaround, next available 11:15.*\n",
  "properties": {
   "minimumMinutes": {
    "type": "integer"
   },
   "maximumMinutes": {
    "type": "integer"
   },
   "incrementMinutes": {
    "type": "integer",
    "default": 15
   },
   "defaultMinutes": {
    "type": "integer"
   },
   "turnaroundMinutes": {
    "type": "integer",
    "default": 0
   },
   "extensionAllowed": {
    "type": "boolean",
    "default": true
   },
   "maximumExtensionMinutes": {
    "type": "integer",
    "nullable": true
   },
   "sameDayReturnRequired": {
    "type": "boolean",
    "default": false
   },
   "overnightAllowed": {
    "type": "boolean",
    "default": false
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "RentalProduct": {
  "type": "object",
  "x-ticvai-persistence": "rental.product",
  "description": "Board 1.3. **The master reference every later board resolves against.**",
  "required": [
   "code",
   "name",
   "venueId"
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
   "internalName": {
    "type": "string",
    "nullable": true
   },
   "description": {
    "type": "string",
    "nullable": true
   },
   "categoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "imageAssetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "tags": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "tenantId": {
    "type": "string",
    "format": "uuid"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string"
   },
   "trackingModel": {
    "type": "string",
    "enum": [
     "pooled",
     "serialised",
     "hybrid"
    ]
   },
   "catalogueProductId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**The thing the guest actually buys.** `catalogue` sells it and this configures how it behaves once sold; the link is here so a rental is never sold twice through two different product records.\n"
   },
   "resourceTypeId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**For serialised products, the `resources` type its assets belong to.** The individual bikes are resources and maintenance assets — this contract does not keep a third register of them.\n"
   },
   "status": {
    "type": "string",
    "enum": [
     "draft",
     "configurationReview",
     "approved",
     "active",
     "suspended",
     "archived"
    ]
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "version": {
    "type": "integer",
    "default": 1
   },
   "isActive": {
    "type": "boolean",
    "default": true
   }
  }
 },
 "ResourceCalendarRow": {
  "type": "object",
  "description": "Board 2.01. **One resource across the window, with its states already computed** — including conflict, which a client cannot derive from a booking list.\n",
  "properties": {
   "resourceId": {
    "type": "string",
    "format": "uuid"
   },
   "resourceName": {
    "type": "string"
   },
   "resourceTypeId": {
    "type": "string",
    "format": "uuid"
   },
   "utilisationPercent": {
    "type": "number"
   },
   "segments": {
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
      },
      "state": {
       "type": "string",
       "enum": [
        "available",
        "reserved",
        "assigned",
        "partiallyUtilised",
        "fullyUtilised",
        "unavailable",
        "onBreak",
        "onLeave",
        "underMaintenance",
        "operationallyBlocked",
        "pendingApproval",
        "conflict"
       ]
      },
      "bookingId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "conflictsWith": {
       "type": "array",
       "items": {
        "type": "string",
        "format": "uuid"
       }
      }
     }
    }
   }
  }
 }
}
```
