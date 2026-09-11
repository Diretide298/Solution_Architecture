# P06-rentals-03 — P06 · Rentals (3 of 3)

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
| `EMP-091` | Rental Return Command Center | commandCentre | 0 | 0 | — |
| `EMP-092` | Return Scan & Rental Retrieval | listDetail | 0 | 0 | — |
| `EMP-093` | Return Summary & Actual Return Time | listDetail | 0 | 0 | — |
| `EMP-094` | Post-Rental Condition Inspection | listDetail | 0 | 0 | — |
| `EMP-095` | Before vs After Condition Comparison | listDetail | 0 | 0 | — |
| `EMP-096` | Damage Assessment & Charge Workflow | listDetail | 0 | 0 | — |
| `EMP-097` | Partial Return & Missing Equipment | listDetail | 0 | 0 | — |
| `EMP-098` | Late Fees, Damage Fees & Final Settlement | listDetail | 0 | 0 | — |
| `EMP-099` | Deposit Release, Capture & Customer Confirmation | listDetail | 0 | 0 | — |
| `EMP-100` | Return Completion & Equipment Disposition | listDetail | 0 | 0 | — |

## Thin screens in this batch

**EMP-092, EMP-093, EMP-094, EMP-095, EMP-096, EMP-097, EMP-098, EMP-099, EMP-100 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "EMP-091",
  "name": "Rental Return Command Center",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "sameAs": "BO-564",
   "book": "Rental_Management.pdf",
   "board": "8",
   "number": "1",
   "page": 92
  },
  "implementation": {
   "app": "venue-staff-app",
   "route": "/rentals/rental-return-command-center-emp-091",
   "component": "apps/venue-staff-app/src/routes/rentals/RentalReturnCommandCenter.tsx",
   "status": "notStarted"
  },
  "density": "comfortable",
  "notes": "The staff-app form of `BO-564`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.",
  "purpose": "Provide operators with a live operational view of all expected, in-progress, partial, overdue and completed returns.",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "layout": {
   "regions": [
    {
     "components": [
      {
       "kind": "searchField",
       "label": "Search rental return",
       "provenance": "pack Rental_Management.pdf, page 92 §Filters"
      },
      {
       "columns": [
        "Venue",
        "Return Location",
        "Product",
        "Expected Return",
        "Rental Status",
        "Damage Status",
        "Deposit Status",
        "Group/Individual"
       ],
       "kind": "multiSelect",
       "label": "Filter by",
       "notes": "The pack filters this screen by venue, return location, product, expected return, rental status, damage status and 2 more — which are present is a decision the pack already made.",
       "provenance": "pack Rental_Management.pdf, page 92 §Filters"
      }
     ],
     "name": "contentBody",
     "slot": "filters"
    },
    {
     "components": [
      {
       "kind": "metricTile",
       "label": "Expected Returns Today",
       "provenance": "pack Rental_Management.pdf, page 92 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Due Next 30 Minutes",
       "provenance": "pack Rental_Management.pdf, page 92 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Return in Progress",
       "provenance": "pack Rental_Management.pdf, page 92 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Overdue",
       "provenance": "pack Rental_Management.pdf, page 92 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Partial Returns",
       "provenance": "pack Rental_Management.pdf, page 92 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Damage Cases",
       "provenance": "pack Rental_Management.pdf, page 92 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Maintenance Required",
       "provenance": "pack Rental_Management.pdf, page 92 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Returns Completed Today",
       "provenance": "pack Rental_Management.pdf, page 92 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Deposits Pending Settlement",
       "provenance": "pack Rental_Management.pdf, page 92 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Equipment Awaiting Inspection",
       "provenance": "pack Rental_Management.pdf, page 92 §KPI Cards"
      }
     ],
     "name": "contentBody",
     "slot": "headline"
    }
   ],
   "template": "dashboard"
  },
  "states": {
   "emptyFirstRun": "No rental return yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "The filter narrowed it and the rental return are still there. Names the active filter and offers to clear it.",
   "error": "Could not load. Names which read failed and leaves the rental return untouched.",
   "loading": "The rental return list; the counts above it resolve separately.",
   "offline": "TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it."
  },
  "apis": [],
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 92. 0 of 8 labels bound to a contract property; 18 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "preloaded": [
    "Expected Returns Today",
    "Due Next 30 Minutes",
    "Return in Progress",
    "Overdue",
    "Partial Returns",
    "Damage Cases"
   ]
  },
  "navigation": {
   "entryFrom": [
    "EMP-003",
    "EMP-092",
    "EMP-093",
    "EMP-094",
    "EMP-095",
    "EMP-096",
    "EMP-097",
    "EMP-098",
    "EMP-099",
    "EMP-100"
   ],
   "exitTo": [
    "EMP-003",
    "EMP-092",
    "EMP-093",
    "EMP-094",
    "EMP-095",
    "EMP-096",
    "EMP-097",
    "EMP-098",
    "EMP-099",
    "EMP-100"
   ],
   "transitions": [
    {
     "to": "EMP-003",
     "trigger": "Back to Home — on duty",
     "provenance": "structural — Rental board 8 on the staff app, 11 September 2026",
     "back": true
    },
    {
     "to": "EMP-092",
     "trigger": "Return Scan & Rental Retrieval",
     "provenance": "structural — Rental board 8 on the staff app, 11 September 2026"
    },
    {
     "to": "EMP-093",
     "trigger": "Return Summary & Actual Return Time",
     "provenance": "structural — Rental board 8 on the staff app, 11 September 2026"
    },
    {
     "to": "EMP-094",
     "trigger": "Post-Rental Condition Inspection",
     "provenance": "structural — Rental board 8 on the staff app, 11 September 2026"
    },
    {
     "to": "EMP-095",
     "trigger": "Before vs After Condition Comparison",
     "provenance": "structural — Rental board 8 on the staff app, 11 September 2026"
    },
    {
     "to": "EMP-096",
     "trigger": "Damage Assessment & Charge Workflow",
     "provenance": "structural — Rental board 8 on the staff app, 11 September 2026"
    },
    {
     "to": "EMP-097",
     "trigger": "Partial Return & Missing Equipment",
     "provenance": "structural — Rental board 8 on the staff app, 11 September 2026"
    },
    {
     "to": "EMP-098",
     "trigger": "Late Fees, Damage Fees & Final Settlement",
     "provenance": "structural — Rental board 8 on the staff app, 11 September 2026"
    },
    {
     "to": "EMP-099",
     "trigger": "Deposit Release, Capture & Customer Confirmation",
     "provenance": "structural — Rental board 8 on the staff app, 11 September 2026"
    },
    {
     "to": "EMP-100",
     "trigger": "Return Completion & Equipment Disposition",
     "provenance": "structural — Rental board 8 on the staff app, 11 September 2026"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-091"
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
  "id": "EMP-092",
  "name": "Return Scan & Rental Retrieval",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "sameAs": "BO-565",
   "book": "Rental_Management.pdf",
   "board": "8",
   "number": "2",
   "page": 93
  },
  "implementation": {
   "app": "venue-staff-app",
   "route": "/rentals/return-scan-rental-retrieval-emp-092",
   "component": "apps/venue-staff-app/src/routes/rentals/ReturnScanRentalRetrieval.tsx",
   "status": "notStarted"
  },
  "density": "comfortable",
  "notes": "The staff-app form of `BO-565`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.",
  "purpose": "Quickly identify which active rental the returned equipment belongs to. The original requirements specifically require scanning the rented item and retrieving its reservation.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "layout": {
   "regions": [],
   "template": "split"
  },
  "states": {
   "emptyFirstRun": "No return scan rental yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "The filter narrowed it and the return scan rental are still there. Names the active filter and offers to clear it.",
   "error": "Could not load. Names which read failed and leaves the return scan rental untouched.",
   "loading": "The return scan rental list.",
   "offline": "TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it."
  },
  "gaps": [
   {
    "operation": null,
    "source": "pack Rental_Management.pdf, page 93",
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built."
   },
   {
    "operation": null,
    "source": "pack Rental_Management.pdf, page 93",
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built."
   }
  ],
  "apis": [],
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 93. 0 of 0 labels bound to a contract property; 0 of 13 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "EMP-091"
   ],
   "exitTo": [
    "EMP-091"
   ],
   "transitions": [
    {
     "to": "EMP-091",
     "trigger": "Back to Rental Return Command Center",
     "provenance": "structural — Rental board 8 on the staff app, 11 September 2026",
     "back": true
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-092"
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
  "id": "EMP-093",
  "name": "Return Summary & Actual Return Time",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "sameAs": "BO-566",
   "book": "Rental_Management.pdf",
   "board": "8",
   "number": "3",
   "page": 94
  },
  "implementation": {
   "app": "venue-staff-app",
   "route": "/rentals/return-summary-actual-return-time-emp-093",
   "component": "apps/venue-staff-app/src/routes/rentals/ReturnSummaryActualReturnTime.tsx",
   "status": "notStarted"
  },
  "density": "comfortable",
  "notes": "The staff-app form of `BO-566`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.",
  "purpose": "Establish the operational return event before inspection and financial settlement.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "layout": {
   "regions": [],
   "template": "split"
  },
  "states": {
   "emptyFirstRun": "No return summary actual yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "The filter narrowed it and the return summary actual are still there. Names the active filter and offers to clear it.",
   "error": "Could not load. Names which read failed and leaves the return summary actual untouched.",
   "loading": "The return summary actual list.",
   "offline": "TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it."
  },
  "gaps": [
   {
    "operation": null,
    "source": "pack Rental_Management.pdf, page 94",
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built."
   },
   {
    "operation": null,
    "source": "pack Rental_Management.pdf, page 94",
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built."
   }
  ],
  "apis": [],
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 94. 0 of 0 labels bound to a contract property; 0 of 15 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "EMP-091"
   ],
   "exitTo": [
    "EMP-091"
   ],
   "transitions": [
    {
     "to": "EMP-091",
     "trigger": "Back to Rental Return Command Center",
     "provenance": "structural — Rental board 8 on the staff app, 11 September 2026",
     "back": true
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-093"
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
  "id": "EMP-094",
  "name": "Post-Rental Condition Inspection",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "sameAs": "BO-567",
   "book": "Rental_Management.pdf",
   "board": "8",
   "number": "4",
   "page": 95
  },
  "implementation": {
   "app": "venue-staff-app",
   "route": "/rentals/post-rental-condition-inspection-emp-094",
   "component": "apps/venue-staff-app/src/routes/rentals/PostRentalConditionInspection.tsx",
   "status": "notStarted"
  },
  "density": "comfortable",
  "notes": "The staff-app form of `BO-567`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.",
  "purpose": "Perform a structured inspection of returned equipment.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "layout": {
   "regions": [],
   "template": "split"
  },
  "states": {
   "emptyFirstRun": "No post-rental condition inspection yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "The filter narrowed it and the post-rental condition inspection are still there. Names the active filter and offers to clear it.",
   "error": "Could not load. Names which read failed and leaves the post-rental condition inspection untouched.",
   "loading": "The post-rental condition inspection list.",
   "offline": "TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it."
  },
  "gaps": [
   {
    "operation": null,
    "source": "pack Rental_Management.pdf, page 95",
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built."
   },
   {
    "operation": null,
    "source": "pack Rental_Management.pdf, page 95",
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built."
   }
  ],
  "apis": [],
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 95. 0 of 0 labels bound to a contract property; 0 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "EMP-091"
   ],
   "exitTo": [
    "EMP-091"
   ],
   "transitions": [
    {
     "to": "EMP-091",
     "trigger": "Back to Rental Return Command Center",
     "provenance": "structural — Rental board 8 on the staff app, 11 September 2026",
     "back": true
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-094"
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
  "id": "EMP-095",
  "name": "Before vs After Condition Comparison",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "sameAs": "BO-568",
   "book": "Rental_Management.pdf",
   "board": "8",
   "number": "5",
   "page": 96
  },
  "implementation": {
   "app": "venue-staff-app",
   "route": "/rentals/before-vs-after-condition-comparison-emp-095",
   "component": "apps/venue-staff-app/src/routes/rentals/BeforeVsAfterConditionComparison.tsx",
   "status": "notStarted"
  },
  "density": "comfortable",
  "notes": "The staff-app form of `BO-568`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.",
  "purpose": "Use the evidence captured during Board 6 checkout to establish whether damage existed before the rental or occurred during it. This is one of the important capabilities I recommended adding.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "layout": {
   "regions": [],
   "template": "split"
  },
  "states": {
   "emptyFirstRun": "No before after condition yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "The filter narrowed it and the before after condition are still there. Names the active filter and offers to clear it.",
   "error": "Could not load. Names which read failed and leaves the before after condition untouched.",
   "loading": "The before after condition list.",
   "offline": "TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it."
  },
  "gaps": [
   {
    "operation": null,
    "source": "pack Rental_Management.pdf, page 96",
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built."
   },
   {
    "operation": null,
    "source": "pack Rental_Management.pdf, page 96",
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built."
   }
  ],
  "apis": [],
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 96. 0 of 0 labels bound to a contract property; 0 of 13 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "EMP-091"
   ],
   "exitTo": [
    "EMP-091"
   ],
   "transitions": [
    {
     "to": "EMP-091",
     "trigger": "Back to Rental Return Command Center",
     "provenance": "structural — Rental board 8 on the staff app, 11 September 2026",
     "back": true
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-095"
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
  "id": "EMP-096",
  "name": "Damage Assessment & Charge Workflow",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "sameAs": "BO-569",
   "book": "Rental_Management.pdf",
   "board": "8",
   "number": "6",
   "page": 97
  },
  "implementation": {
   "app": "venue-staff-app",
   "route": "/rentals/damage-assessment-charge-workflow-emp-096",
   "component": "apps/venue-staff-app/src/routes/rentals/DamageAssessmentChargeWorkflow.tsx",
   "status": "notStarted"
  },
  "density": "comfortable",
  "notes": "The staff-app form of `BO-569`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.",
  "purpose": "Convert confirmed equipment damage into a controlled operational and commercial case. The source specifically recommends a formal damage assessment workflow.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "layout": {
   "regions": [],
   "template": "split"
  },
  "states": {
   "emptyFirstRun": "No damage assessment charge yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "The filter narrowed it and the damage assessment charge are still there. Names the active filter and offers to clear it.",
   "error": "Could not load. Names which read failed and leaves the damage assessment charge untouched.",
   "loading": "The damage assessment charge list.",
   "offline": "TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it."
  },
  "gaps": [
   {
    "operation": null,
    "source": "pack Rental_Management.pdf, page 97",
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built."
   },
   {
    "operation": null,
    "source": "pack Rental_Management.pdf, page 97",
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built."
   }
  ],
  "apis": [],
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 97. 0 of 0 labels bound to a contract property; 0 of 19 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "EMP-091"
   ],
   "exitTo": [
    "EMP-091"
   ],
   "transitions": [
    {
     "to": "EMP-091",
     "trigger": "Back to Rental Return Command Center",
     "provenance": "structural — Rental board 8 on the staff app, 11 September 2026",
     "back": true
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-096"
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
  "id": "EMP-097",
  "name": "Partial Return & Missing Equipment",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "sameAs": "BO-570",
   "book": "Rental_Management.pdf",
   "board": "8",
   "number": "7",
   "page": 98
  },
  "implementation": {
   "app": "venue-staff-app",
   "route": "/rentals/partial-return-missing-equipment-emp-097",
   "component": "apps/venue-staff-app/src/routes/rentals/PartialReturnMissingEquipment.tsx",
   "status": "notStarted"
  },
  "density": "comfortable",
  "notes": "The staff-app form of `BO-570`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.",
  "purpose": "Handle multi-item and group rentals where equipment is returned at different times. This implements the partial-return capability we added in Board 7.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "layout": {
   "regions": [],
   "template": "split"
  },
  "states": {
   "emptyFirstRun": "No partial return missing yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "The filter narrowed it and the partial return missing are still there. Names the active filter and offers to clear it.",
   "error": "Could not load. Names which read failed and leaves the partial return missing untouched.",
   "loading": "The partial return missing list.",
   "offline": "TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it."
  },
  "gaps": [
   {
    "operation": null,
    "source": "pack Rental_Management.pdf, page 98",
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built."
   },
   {
    "operation": null,
    "source": "pack Rental_Management.pdf, page 98",
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built."
   }
  ],
  "apis": [],
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 98. 0 of 0 labels bound to a contract property; 0 of 13 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "EMP-091"
   ],
   "exitTo": [
    "EMP-091"
   ],
   "transitions": [
    {
     "to": "EMP-091",
     "trigger": "Back to Rental Return Command Center",
     "provenance": "structural — Rental board 8 on the staff app, 11 September 2026",
     "back": true
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-097"
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
  "id": "EMP-098",
  "name": "Late Fees, Damage Fees & Final Settlement",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "sameAs": "BO-571",
   "book": "Rental_Management.pdf",
   "board": "8",
   "number": "8",
   "page": 99
  },
  "implementation": {
   "app": "venue-staff-app",
   "route": "/rentals/late-fees-damage-fees-final-settlement-emp-098",
   "component": "apps/venue-staff-app/src/routes/rentals/LateFeesDamageFeesFinalSettlement.tsx",
   "status": "notStarted"
  },
  "density": "comfortable",
  "notes": "The staff-app form of `BO-571`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.",
  "purpose": "Calculate the customer's final rental financial position. Board 8 should consume, not recreate, the commercial policies configured in Board 4.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "layout": {
   "regions": [],
   "template": "split"
  },
  "states": {
   "emptyFirstRun": "No late fees damage yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "The filter narrowed it and the late fees damage are still there. Names the active filter and offers to clear it.",
   "error": "Could not load. Names which read failed and leaves the late fees damage untouched.",
   "loading": "The late fees damage list.",
   "offline": "TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it."
  },
  "gaps": [
   {
    "operation": null,
    "source": "pack Rental_Management.pdf, page 99",
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built."
   },
   {
    "operation": null,
    "source": "pack Rental_Management.pdf, page 99",
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built."
   }
  ],
  "apis": [],
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 99. 0 of 0 labels bound to a contract property; 0 of 3 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "EMP-091"
   ],
   "exitTo": [
    "EMP-091"
   ],
   "transitions": [
    {
     "to": "EMP-091",
     "trigger": "Back to Rental Return Command Center",
     "provenance": "structural — Rental board 8 on the staff app, 11 September 2026",
     "back": true
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-098"
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
  "id": "EMP-099",
  "name": "Deposit Release, Capture & Customer Confirmation",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "sameAs": "BO-572",
   "book": "Rental_Management.pdf",
   "board": "8",
   "number": "9",
   "page": 100
  },
  "implementation": {
   "app": "venue-staff-app",
   "route": "/rentals/deposit-release-capture-customer-confirmation-emp-099",
   "component": "apps/venue-staff-app/src/routes/rentals/DepositReleaseCaptureCustomerConfirmation.tsx",
   "status": "notStarted"
  },
  "density": "comfortable",
  "notes": "The staff-app form of `BO-572`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.",
  "purpose": "Complete the deposit lifecycle and provide the customer with a transparent final statement. The source requires full refund/release, partial refund and deposit forfeiture, together with transaction history.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "layout": {
   "regions": [],
   "template": "split"
  },
  "states": {
   "emptyFirstRun": "No deposit release capture yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "The filter narrowed it and the deposit release capture are still there. Names the active filter and offers to clear it.",
   "error": "Could not load. Names which read failed and leaves the deposit release capture untouched.",
   "loading": "The deposit release capture list.",
   "offline": "TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it."
  },
  "gaps": [
   {
    "operation": null,
    "source": "pack Rental_Management.pdf, page 100",
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built."
   },
   {
    "operation": null,
    "source": "pack Rental_Management.pdf, page 100",
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built."
   }
  ],
  "apis": [],
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 100. 0 of 0 labels bound to a contract property; 0 of 4 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "EMP-091"
   ],
   "exitTo": [
    "EMP-091"
   ],
   "transitions": [
    {
     "to": "EMP-091",
     "trigger": "Back to Rental Return Command Center",
     "provenance": "structural — Rental board 8 on the staff app, 11 September 2026",
     "back": true
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-099"
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
  "id": "EMP-100",
  "name": "Return Completion & Equipment Disposition",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "sameAs": "BO-573",
   "book": "Rental_Management.pdf",
   "board": "8",
   "number": "10",
   "page": 101
  },
  "implementation": {
   "app": "venue-staff-app",
   "route": "/rentals/return-completion-equipment-disposition-emp-100",
   "component": "apps/venue-staff-app/src/routes/rentals/ReturnCompletionEquipmentDisposition.tsx",
   "status": "notStarted"
  },
  "density": "comfortable",
  "notes": "The staff-app form of `BO-573`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.",
  "purpose": "Complete the rental while determining exactly what happens to every returned physical asset. This is extremely important because returning an item does not necessarily mean it becomes immediately available again.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "layout": {
   "regions": [],
   "template": "split"
  },
  "states": {
   "emptyFirstRun": "No return completion equipment yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "The filter narrowed it and the return completion equipment are still there. Names the active filter and offers to clear it.",
   "error": "Could not load. Names which read failed and leaves the return completion equipment untouched.",
   "loading": "The return completion equipment list.",
   "offline": "TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it."
  },
  "gaps": [
   {
    "operation": null,
    "source": "pack Rental_Management.pdf, page 101",
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built."
   },
   {
    "operation": null,
    "source": "pack Rental_Management.pdf, page 101",
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built."
   }
  ],
  "apis": [],
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 101. 0 of 0 labels bound to a contract property; 0 of 118 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "EMP-091"
   ],
   "exitTo": [
    "EMP-091"
   ],
   "transitions": [
    {
     "to": "EMP-091",
     "trigger": "Back to Rental Return Command Center",
     "provenance": "structural — Rental board 8 on the staff app, 11 September 2026",
     "back": true
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-100"
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
