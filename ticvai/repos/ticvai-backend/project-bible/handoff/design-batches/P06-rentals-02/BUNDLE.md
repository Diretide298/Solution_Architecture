# P06-rentals-02 — P06 · Rentals (2 of 3)

**10 screens · 0 operations · 0 schemas · 0 permissions**

Platform P06 Venue Staff App · ships as **venue-staff-mobile** ·
staff audience · mobileApp ·
offline-capable

## Who this is for

**staff on mobileApp.** Everything below is how you know what is
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
| `EMP-081` | Active Rental Operations Command Center | commandCentre | 0 | 0 | — |
| `EMP-082` | Active Rental Detail & Live Timeline | listDetail | 0 | 0 | — |
| `EMP-083` | Rental Extension Request | listDetail | 0 | 0 | — |
| `EMP-084` | Extension Pricing & Confirmation | listDetail | 0 | 0 | — |
| `EMP-085` | Equipment Swap / Replacement | listDetail | 0 | 0 | — |
| `EMP-086` | Rental Incident & Operational Exception | listDetail | 0 | 0 | — |
| `EMP-087` | Due Soon & Customer Notification Management | listDetail | 0 | 0 | — |
| `EMP-088` | Overdue Rental Management | listDetail | 0 | 0 | — |
| `EMP-089` | Active Group Rental Management | listDetail | 0 | 0 | — |
| `EMP-090` | Active Rental Intelligence & Operational Alerts | listDetail | 0 | 0 | — |

## Thin screens in this batch

**EMP-082, EMP-083, EMP-084, EMP-085, EMP-086, EMP-087, EMP-088, EMP-089, EMP-090 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "EMP-081",
  "name": "Active Rental Operations Command Center",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "sameAs": "BO-554",
   "book": "Rental_Management.pdf",
   "board": "7",
   "number": "1",
   "page": 78
  },
  "implementation": {
   "app": "venue-staff-app",
   "route": "/rentals/active-rental-operations-command-center-emp-081",
   "component": "apps/venue-staff-app/src/routes/rentals/ActiveRentalOperationsCommandCenter.tsx",
   "status": "notStarted"
  },
  "density": "comfortable",
  "notes": "The staff-app form of `BO-554`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.",
  "purpose": "Provide operators and supervisors with a real-time view of every rental currently in progress.",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "layout": {
   "regions": [
    {
     "components": [
      {
       "kind": "searchField",
       "label": "Search active rental operations",
       "provenance": "pack Rental_Management.pdf, page 78 §Filters"
      },
      {
       "columns": [
        "Venue",
        "Location",
        "Product",
        "Customer",
        "Rental status",
        "Expected return",
        "Overdue duration",
        "Group/Individual"
       ],
       "kind": "multiSelect",
       "label": "Filter by",
       "notes": "The pack filters this screen by venue, location, product, customer, rental status, expected return and 2 more — which are present is a decision the pack already made.",
       "provenance": "pack Rental_Management.pdf, page 78 §Filters"
      }
     ],
     "name": "contentBody",
     "slot": "filters"
    },
    {
     "components": [
      {
       "kind": "metricTile",
       "label": "Active Rentals",
       "provenance": "pack Rental_Management.pdf, page 78 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Due Within 30 Minutes",
       "provenance": "pack Rental_Management.pdf, page 78 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Overdue",
       "provenance": "pack Rental_Management.pdf, page 78 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Extensions Requested",
       "provenance": "pack Rental_Management.pdf, page 78 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Equipment Swap Required",
       "provenance": "pack Rental_Management.pdf, page 78 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Active Incidents",
       "provenance": "pack Rental_Management.pdf, page 78 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Group Rentals Active",
       "provenance": "pack Rental_Management.pdf, page 78 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Expected Returns Next Hour",
       "provenance": "pack Rental_Management.pdf, page 78 §KPI Cards"
      }
     ],
     "name": "contentBody",
     "slot": "headline"
    }
   ],
   "template": "dashboard"
  },
  "states": {
   "emptyFirstRun": "No active rental operations yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "The filter narrowed it and the active rental operations are still there. Names the active filter and offers to clear it.",
   "error": "Could not load. Names which read failed and leaves the active rental operations untouched.",
   "loading": "The active rental operations list; the counts above it resolve separately.",
   "offline": "TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it."
  },
  "apis": [],
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 78. 0 of 8 labels bound to a contract property; 16 of 23 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "preloaded": [
    "Active Rentals",
    "Due Within 30 Minutes",
    "Overdue",
    "Extensions Requested",
    "Equipment Swap Required",
    "Active Incidents"
   ]
  },
  "navigation": {
   "entryFrom": [
    "EMP-003",
    "EMP-082",
    "EMP-083",
    "EMP-084",
    "EMP-085",
    "EMP-086",
    "EMP-087",
    "EMP-088",
    "EMP-089",
    "EMP-090"
   ],
   "exitTo": [
    "EMP-003",
    "EMP-082",
    "EMP-083",
    "EMP-084",
    "EMP-085",
    "EMP-086",
    "EMP-087",
    "EMP-088",
    "EMP-089",
    "EMP-090"
   ],
   "transitions": [
    {
     "to": "EMP-003",
     "trigger": "Back to Home — on duty",
     "provenance": "structural — Rental board 7 on the staff app, 11 September 2026",
     "back": true
    },
    {
     "to": "EMP-082",
     "trigger": "Active Rental Detail & Live Timeline",
     "provenance": "structural — Rental board 7 on the staff app, 11 September 2026"
    },
    {
     "to": "EMP-083",
     "trigger": "Rental Extension Request",
     "provenance": "structural — Rental board 7 on the staff app, 11 September 2026"
    },
    {
     "to": "EMP-084",
     "trigger": "Extension Pricing & Confirmation",
     "provenance": "structural — Rental board 7 on the staff app, 11 September 2026"
    },
    {
     "to": "EMP-085",
     "trigger": "Equipment Swap / Replacement",
     "provenance": "structural — Rental board 7 on the staff app, 11 September 2026"
    },
    {
     "to": "EMP-086",
     "trigger": "Rental Incident & Operational Exception",
     "provenance": "structural — Rental board 7 on the staff app, 11 September 2026"
    },
    {
     "to": "EMP-087",
     "trigger": "Due Soon & Customer Notification Management",
     "provenance": "structural — Rental board 7 on the staff app, 11 September 2026"
    },
    {
     "to": "EMP-088",
     "trigger": "Overdue Rental Management",
     "provenance": "structural — Rental board 7 on the staff app, 11 September 2026"
    },
    {
     "to": "EMP-089",
     "trigger": "Active Group Rental Management",
     "provenance": "structural — Rental board 7 on the staff app, 11 September 2026"
    },
    {
     "to": "EMP-090",
     "trigger": "Active Rental Intelligence & Operational Alerts",
     "provenance": "structural — Rental board 7 on the staff app, 11 September 2026"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-081"
  },
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "EMP-082",
  "name": "Active Rental Detail & Live Timeline",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "sameAs": "BO-555",
   "book": "Rental_Management.pdf",
   "board": "7",
   "number": "2",
   "page": 79
  },
  "implementation": {
   "app": "venue-staff-app",
   "route": "/rentals/active-rental-detail-live-timeline-emp-082",
   "component": "apps/venue-staff-app/src/routes/rentals/ActiveRentalDetailLiveTimeline.tsx",
   "status": "notStarted"
  },
  "density": "comfortable",
  "notes": "The staff-app form of `BO-555`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.",
  "purpose": "Provide the complete operational view of one active rental.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "layout": {
   "regions": [],
   "template": "split"
  },
  "states": {
   "emptyFirstRun": "No active rental detail yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "The filter narrowed it and the active rental detail are still there. Names the active filter and offers to clear it.",
   "error": "Could not load. Names which read failed and leaves the active rental detail untouched.",
   "loading": "The active rental detail list.",
   "offline": "TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it."
  },
  "gaps": [
   {
    "operation": null,
    "source": "pack Rental_Management.pdf, page 79",
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built."
   },
   {
    "operation": null,
    "source": "pack Rental_Management.pdf, page 79",
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built."
   }
  ],
  "apis": [],
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 79. 0 of 0 labels bound to a contract property; 0 of 13 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "EMP-081"
   ],
   "exitTo": [
    "EMP-081"
   ],
   "transitions": [
    {
     "to": "EMP-081",
     "trigger": "Back to Active Rental Operations Command Center",
     "provenance": "structural — Rental board 7 on the staff app, 11 September 2026",
     "back": true
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-082"
  },
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "EMP-083",
  "name": "Rental Extension Request",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "sameAs": "BO-556",
   "book": "Rental_Management.pdf",
   "board": "7",
   "number": "3",
   "page": 81
  },
  "implementation": {
   "app": "venue-staff-app",
   "route": "/rentals/rental-extension-request-emp-083",
   "component": "apps/venue-staff-app/src/routes/rentals/RentalExtensionRequest.tsx",
   "status": "notStarted"
  },
  "density": "comfortable",
  "notes": "The staff-app form of `BO-556`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.",
  "purpose": "Allow the customer or operator to request additional rental time. This is one of the important capabilities I recommend formally adding to the rental scope.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "layout": {
   "regions": [],
   "template": "split"
  },
  "states": {
   "emptyFirstRun": "No rental extension request yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "The filter narrowed it and the rental extension request are still there. Names the active filter and offers to clear it.",
   "error": "Could not load. Names which read failed and leaves the rental extension request untouched.",
   "loading": "The rental extension request list.",
   "offline": "TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it."
  },
  "gaps": [
   {
    "operation": null,
    "source": "pack Rental_Management.pdf, page 81",
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built."
   },
   {
    "operation": null,
    "source": "pack Rental_Management.pdf, page 81",
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built."
   }
  ],
  "apis": [],
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 81. 0 of 0 labels bound to a contract property; 0 of 23 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "EMP-081"
   ],
   "exitTo": [
    "EMP-081"
   ],
   "transitions": [
    {
     "to": "EMP-081",
     "trigger": "Back to Active Rental Operations Command Center",
     "provenance": "structural — Rental board 7 on the staff app, 11 September 2026",
     "back": true
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-083"
  },
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "EMP-084",
  "name": "Extension Pricing & Confirmation",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "sameAs": "BO-557",
   "book": "Rental_Management.pdf",
   "board": "7",
   "number": "4",
   "page": 82
  },
  "implementation": {
   "app": "venue-staff-app",
   "route": "/rentals/extension-pricing-confirmation-emp-084",
   "component": "apps/venue-staff-app/src/routes/rentals/ExtensionPricingConfirmation.tsx",
   "status": "notStarted"
  },
  "density": "comfortable",
  "notes": "The staff-app form of `BO-557`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.",
  "purpose": "Calculate the commercial impact of an approved extension. Once Board 3 confirms availability, Board 4 calculates the extension charge.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "layout": {
   "regions": [],
   "template": "split"
  },
  "states": {
   "emptyFirstRun": "No extension pricing confirmation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "The filter narrowed it and the extension pricing confirmation are still there. Names the active filter and offers to clear it.",
   "error": "Could not load. Names which read failed and leaves the extension pricing confirmation untouched.",
   "loading": "The extension pricing confirmation list.",
   "offline": "TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it."
  },
  "gaps": [
   {
    "operation": null,
    "source": "pack Rental_Management.pdf, page 82",
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built."
   },
   {
    "operation": null,
    "source": "pack Rental_Management.pdf, page 82",
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built."
   }
  ],
  "apis": [],
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 82. 0 of 0 labels bound to a contract property; 0 of 15 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "EMP-081"
   ],
   "exitTo": [
    "EMP-081"
   ],
   "transitions": [
    {
     "to": "EMP-081",
     "trigger": "Back to Active Rental Operations Command Center",
     "provenance": "structural — Rental board 7 on the staff app, 11 September 2026",
     "back": true
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-084"
  },
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "EMP-085",
  "name": "Equipment Swap / Replacement",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "sameAs": "BO-558",
   "book": "Rental_Management.pdf",
   "board": "7",
   "number": "5",
   "page": 83
  },
  "implementation": {
   "app": "venue-staff-app",
   "route": "/rentals/equipment-swap-replacement-emp-085",
   "component": "apps/venue-staff-app/src/routes/rentals/EquipmentSwapReplacement.tsx",
   "status": "notStarted"
  },
  "density": "comfortable",
  "notes": "The staff-app form of `BO-558`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.",
  "purpose": "Replace equipment during an active rental without terminating and recreating the rental. This is another capability I strongly recommend adding.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "layout": {
   "regions": [],
   "template": "split"
  },
  "states": {
   "emptyFirstRun": "No equipment swap replacement yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "The filter narrowed it and the equipment swap replacement are still there. Names the active filter and offers to clear it.",
   "error": "Could not load. Names which read failed and leaves the equipment swap replacement untouched.",
   "loading": "The equipment swap replacement list.",
   "offline": "TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it."
  },
  "gaps": [
   {
    "operation": null,
    "source": "pack Rental_Management.pdf, page 83",
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built."
   },
   {
    "operation": null,
    "source": "pack Rental_Management.pdf, page 83",
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built."
   }
  ],
  "apis": [],
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 83. 0 of 0 labels bound to a contract property; 0 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "EMP-081"
   ],
   "exitTo": [
    "EMP-081"
   ],
   "transitions": [
    {
     "to": "EMP-081",
     "trigger": "Back to Active Rental Operations Command Center",
     "provenance": "structural — Rental board 7 on the staff app, 11 September 2026",
     "back": true
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-085"
  },
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "EMP-086",
  "name": "Rental Incident & Operational Exception",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "sameAs": "BO-559",
   "book": "Rental_Management.pdf",
   "board": "7",
   "number": "6",
   "page": 84
  },
  "implementation": {
   "app": "venue-staff-app",
   "route": "/rentals/rental-incident-operational-exception-emp-086",
   "component": "apps/venue-staff-app/src/routes/rentals/RentalIncidentOperationalException.tsx",
   "status": "notStarted"
  },
  "density": "comfortable",
  "notes": "The staff-app form of `BO-559`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.",
  "purpose": "Capture incidents occurring while equipment is in customer possession.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "layout": {
   "regions": [],
   "template": "split"
  },
  "states": {
   "emptyFirstRun": "No rental incident operational yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "The filter narrowed it and the rental incident operational are still there. Names the active filter and offers to clear it.",
   "error": "Could not load. Names which read failed and leaves the rental incident operational untouched.",
   "loading": "The rental incident operational list.",
   "offline": "TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it."
  },
  "gaps": [
   {
    "operation": null,
    "source": "pack Rental_Management.pdf, page 84",
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built."
   },
   {
    "operation": null,
    "source": "pack Rental_Management.pdf, page 84",
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built."
   }
  ],
  "apis": [],
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 84. 0 of 0 labels bound to a contract property; 0 of 17 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "EMP-081"
   ],
   "exitTo": [
    "EMP-081"
   ],
   "transitions": [
    {
     "to": "EMP-081",
     "trigger": "Back to Active Rental Operations Command Center",
     "provenance": "structural — Rental board 7 on the staff app, 11 September 2026",
     "back": true
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-086"
  },
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "EMP-087",
  "name": "Due Soon & Customer Notification Management",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "sameAs": "BO-560",
   "book": "Rental_Management.pdf",
   "board": "7",
   "number": "7",
   "page": 85
  },
  "implementation": {
   "app": "venue-staff-app",
   "route": "/rentals/due-soon-customer-notification-management-emp-087",
   "component": "apps/venue-staff-app/src/routes/rentals/DueSoonCustomerNotificationManagement.tsx",
   "status": "notStarted"
  },
  "density": "comfortable",
  "notes": "The staff-app form of `BO-560`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.",
  "purpose": "Proactively communicate with customers before their rental becomes overdue. The original matrix requires overdue rental notifications.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "layout": {
   "regions": [],
   "template": "split"
  },
  "states": {
   "emptyFirstRun": "No due soon customer yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "The filter narrowed it and the due soon customer are still there. Names the active filter and offers to clear it.",
   "error": "Could not load. Names which read failed and leaves the due soon customer untouched.",
   "loading": "The due soon customer list.",
   "offline": "TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it."
  },
  "gaps": [
   {
    "operation": null,
    "source": "pack Rental_Management.pdf, page 85",
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built."
   },
   {
    "operation": null,
    "source": "pack Rental_Management.pdf, page 85",
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built."
   }
  ],
  "apis": [],
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 85. 0 of 0 labels bound to a contract property; 0 of 14 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "EMP-081"
   ],
   "exitTo": [
    "EMP-081"
   ],
   "transitions": [
    {
     "to": "EMP-081",
     "trigger": "Back to Active Rental Operations Command Center",
     "provenance": "structural — Rental board 7 on the staff app, 11 September 2026",
     "back": true
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-087"
  },
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "EMP-088",
  "name": "Overdue Rental Management",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "sameAs": "BO-561",
   "book": "Rental_Management.pdf",
   "board": "7",
   "number": "8",
   "page": 85
  },
  "implementation": {
   "app": "venue-staff-app",
   "route": "/rentals/overdue-rental-management-emp-088",
   "component": "apps/venue-staff-app/src/routes/rentals/OverdueRentalManagement.tsx",
   "status": "notStarted"
  },
  "density": "comfortable",
  "notes": "The staff-app form of `BO-561`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.",
  "purpose": "Provide operators with a dedicated workflow for rentals that have exceeded their expected return time. The original requirement calls for automatic late-fee calculation, configurable grace periods and overdue notifications.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "layout": {
   "regions": [],
   "template": "split"
  },
  "states": {
   "emptyFirstRun": "No overdue rental yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "The filter narrowed it and the overdue rental are still there. Names the active filter and offers to clear it.",
   "error": "Could not load. Names which read failed and leaves the overdue rental untouched.",
   "loading": "The overdue rental list.",
   "offline": "TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it."
  },
  "gaps": [
   {
    "operation": null,
    "source": "pack Rental_Management.pdf, page 85",
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built."
   },
   {
    "operation": null,
    "source": "pack Rental_Management.pdf, page 85",
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built."
   }
  ],
  "apis": [],
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 85. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "EMP-081"
   ],
   "exitTo": [
    "EMP-081"
   ],
   "transitions": [
    {
     "to": "EMP-081",
     "trigger": "Back to Active Rental Operations Command Center",
     "provenance": "structural — Rental board 7 on the staff app, 11 September 2026",
     "back": true
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-088"
  },
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "EMP-089",
  "name": "Active Group Rental Management",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "sameAs": "BO-562",
   "book": "Rental_Management.pdf",
   "board": "7",
   "number": "9",
   "page": 86
  },
  "implementation": {
   "app": "venue-staff-app",
   "route": "/rentals/active-group-rental-management-emp-089",
   "component": "apps/venue-staff-app/src/routes/rentals/ActiveGroupRentalManagement.tsx",
   "status": "notStarted"
  },
  "density": "comfortable",
  "notes": "The staff-app form of `BO-562`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.",
  "purpose": "Manage group rentals where multiple pieces of equipment may have different operational states.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "layout": {
   "regions": [],
   "template": "split"
  },
  "states": {
   "emptyFirstRun": "No active group rental yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "The filter narrowed it and the active group rental are still there. Names the active filter and offers to clear it.",
   "error": "Could not load. Names which read failed and leaves the active group rental untouched.",
   "loading": "The active group rental list.",
   "offline": "TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it."
  },
  "gaps": [
   {
    "operation": null,
    "source": "pack Rental_Management.pdf, page 86",
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built."
   },
   {
    "operation": null,
    "source": "pack Rental_Management.pdf, page 86",
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built."
   }
  ],
  "apis": [],
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 86. 0 of 0 labels bound to a contract property; 0 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "EMP-081"
   ],
   "exitTo": [
    "EMP-081"
   ],
   "transitions": [
    {
     "to": "EMP-081",
     "trigger": "Back to Active Rental Operations Command Center",
     "provenance": "structural — Rental board 7 on the staff app, 11 September 2026",
     "back": true
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-089"
  },
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "EMP-090",
  "name": "Active Rental Intelligence & Operational Alerts",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "sameAs": "BO-563",
   "book": "Rental_Management.pdf",
   "board": "7",
   "number": "10",
   "page": 87
  },
  "implementation": {
   "app": "venue-staff-app",
   "route": "/rentals/active-rental-intelligence-operational-alerts-emp-090",
   "component": "apps/venue-staff-app/src/routes/rentals/ActiveRentalIntelligenceOperationalAlerts.tsx",
   "status": "notStarted"
  },
  "density": "comfortable",
  "notes": "The staff-app form of `BO-563`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.",
  "purpose": "Use AI and real-time operational data to identify risks before they become operational problems.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "layout": {
   "regions": [
    {
     "components": [
      {
       "bindsTo": null,
       "columns": [
        "Rentals due next hour",
        "Predicted late returns",
        "Future reservation conflicts",
        "Extension demand",
        "Equipment incident trends",
        "Location return pressure",
        "Expected inventory shortage"
       ],
       "kind": "dataTable",
       "label": "Every active rental intelligence",
       "operation": null,
       "provenance": "pack Rental_Management.pdf, page 87 §Display"
      }
     ],
     "name": "contentBody",
     "slot": "collection"
    },
    {
     "components": [
      {
       "bindsTo": null,
       "columns": [
        "Rentals due next hour",
        "Predicted late returns",
        "Future reservation conflicts",
        "Extension demand",
        "Equipment incident trends",
        "Location return pressure",
        "Expected inventory shortage"
       ],
       "kind": "detailPanel",
       "label": "The selected active rental intelligence",
       "notes": "The pack groups this record's detail under its own headings: “RNT-10482”, “Confirmed”, “Ready for Checkout”, “Active”, “Incident”, “Overdue”.",
       "provenance": "pack Rental_Management.pdf, page 87 §Display"
      }
     ],
     "name": "contextPanel",
     "slot": "selection"
    }
   ],
   "template": "split"
  },
  "states": {
   "emptyFirstRun": "No active rental intelligence yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "The filter narrowed it and the active rental intelligence are still there. Names the active filter and offers to clear it.",
   "error": "Could not load. Names which read failed and leaves the active rental intelligence untouched.",
   "loading": "The active rental intelligence list.",
   "offline": "TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it."
  },
  "gaps": [
   {
    "operation": null,
    "source": "pack Rental_Management.pdf, page 87 §Display",
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists."
   }
  ],
  "apis": [],
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 87. 0 of 7 labels bound to a contract property; 7 of 74 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "preloaded": [
    "Rentals due next hour",
    "Predicted late returns",
    "Future reservation conflicts",
    "Extension demand",
    "Equipment incident trends",
    "Location return pressure"
   ]
  },
  "navigation": {
   "entryFrom": [
    "EMP-081"
   ],
   "exitTo": [
    "EMP-081"
   ],
   "transitions": [
    {
     "to": "EMP-081",
     "trigger": "Back to Active Rental Operations Command Center",
     "provenance": "structural — Rental board 7 on the staff app, 11 September 2026",
     "back": true
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-090"
  },
  "_platform": {
   "code": "P06",
   "audience": "staff",
   "formFactor": "mobileApp",
   "shortName": "Venue Staff App",
   "name": "Venue Staff App — Operations",
   "app": "venue-staff-app",
   "offlineCapable": true,
   "operator": "venue",
   "targetApp": {
    "app": "venue-staff-mobile",
    "name": "TICVAI Venue Staff",
    "shell": "mobile",
    "siblings": [
     "P07"
    ],
    "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.",
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
