# WS90 — Rental Management board 3

**10 screens · 0 operations · 0 schemas · 0 permissions**

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

- **Every control that can be refused must be gated.** 0 permissions apply here:
  ``. A control nobody can use must say so,
  not sit enabled and fail.
- **0 of these operations work offline**
  
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-514` | Availability Command Center | commandCentre | 0 | 0 | — |
| `BO-515` | Availability Rule Configuration | configEditor | 0 | 0 | — |
| `BO-516` | Operating Hours & Rental Windows | listDetail | 0 | 0 | — |
| `BO-517` | Timeslot & Duration Availability Setup | configEditor | 0 | 0 | — |
| `BO-518` | Real-Time Availability Calendar | listDetail | 0 | 0 | — |
| `BO-519` | Resource / Equipment Calendar | listDetail | 0 | 0 | — |
| `BO-520` | Blackout, Closure & Capacity Blocking | listDetail | 0 | 0 | — |
| `BO-521` | Overlap & Conflict Engine | listDetail | 0 | 0 | — |
| `BO-522` | Inventory Holds, Buffers & Release Rules | listDetail | 0 | 0 | — |
| `BO-523` | Availability Intelligence & AI Forecasting | listDetail | 0 | 0 | — |

## Thin screens in this batch

**BO-516, BO-518, BO-519, BO-520, BO-521, BO-522, BO-523 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

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
     "provenance": "structural — pack board 3 wiring, 11 September 2026"
    },
    {
     "to": "BO-516",
     "trigger": "Operating Hours & Rental Windows",
     "provenance": "structural — pack board 3 wiring, 11 September 2026"
    },
    {
     "to": "BO-517",
     "trigger": "Timeslot & Duration Availability Setup",
     "provenance": "structural — pack board 3 wiring, 11 September 2026"
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
     "provenance": "structural — pack board 3 wiring, 11 September 2026"
    },
    {
     "to": "BO-521",
     "trigger": "Overlap & Conflict Engine",
     "provenance": "structural — pack board 3 wiring, 11 September 2026"
    },
    {
     "to": "BO-522",
     "trigger": "Inventory Holds, Buffers & Release Rules",
     "provenance": "structural — pack board 3 wiring, 11 September 2026"
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
  "apis": [],
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-514"
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
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-515"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 28. 0 of 0 labels bound to a contract property; 10 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
   "regions": []
  },
  "states": {
   "loading": "The operating hours rental list.",
   "error": "Could not load. Names which read failed and leaves the operating hours rental untouched.",
   "emptyFirstRun": "No operating hours rental yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the operating hours rental are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-516"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 29. 0 of 0 labels bound to a contract property; 0 of 21 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-517"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 30. 0 of 0 labels bound to a contract property; 7 of 17 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
   "regions": []
  },
  "states": {
   "loading": "The real-time availability calendar list.",
   "error": "Could not load. Names which read failed and leaves the real-time availability calendar untouched.",
   "emptyFirstRun": "No real-time availability calendar yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the real-time availability calendar are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-518"
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
   "regions": []
  },
  "states": {
   "loading": "The resource equipment calendar list.",
   "error": "Could not load. Names which read failed and leaves the resource equipment calendar untouched.",
   "emptyFirstRun": "No resource equipment calendar yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the resource equipment calendar are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-519"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 31. 0 of 0 labels bound to a contract property; 0 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
   "regions": []
  },
  "states": {
   "loading": "The blackout closure capacity list.",
   "error": "Could not load. Names which read failed and leaves the blackout closure capacity untouched.",
   "emptyFirstRun": "No blackout closure capacity yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the blackout closure capacity are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-520"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 32. 0 of 0 labels bound to a contract property; 0 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 33"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 33"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The overlap conflict list.",
   "error": "Could not load. Names which read failed and leaves the overlap conflict untouched.",
   "emptyFirstRun": "No overlap conflict yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the overlap conflict are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-521"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 33. 0 of 0 labels bound to a contract property; 0 of 23 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
   "regions": []
  },
  "states": {
   "loading": "The inventory holds buffers list.",
   "error": "Could not load. Names which read failed and leaves the inventory holds buffers untouched.",
   "emptyFirstRun": "No inventory holds buffers yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the inventory holds buffers are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-522"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 34. 0 of 0 labels bound to a contract property; 0 of 21 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "apis": [],
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-523"
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
{}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{}
```
