# P06-rentals-03 — P06 · Rentals (3 of 3)

**10 screens · 6 operations · 10 schemas · 3 permissions**

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

- **Every control that can be refused must be gated.** 3 permissions apply here:
  `ASSET_MANAGE, RENTAL_OPERATE, RENTAL_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **3 of these operations work offline**: recordRentalInspection, returnRental, setAssetStatus
  — and the rest do not. A surface that looks the same online and off is lying.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `EMP-091` | Rental Return Command Center | commandCentre | 1 | 0 | — |
| `EMP-092` | Return Scan & Rental Retrieval | listDetail | 1 | 0 | — |
| `EMP-093` | Return Summary & Actual Return Time | listDetail | 1 | 0 | — |
| `EMP-094` | Post-Rental Condition Inspection | listDetail | 1 | 0 | — |
| `EMP-095` | Before vs After Condition Comparison | listDetail | 1 | 0 | — |
| `EMP-096` | Damage Assessment & Charge Workflow | listDetail | 1 | 0 | — |
| `EMP-097` | Partial Return & Missing Equipment | listDetail | 1 | 0 | — |
| `EMP-098` | Late Fees, Damage Fees & Final Settlement | listDetail | 1 | 0 | — |
| `EMP-099` | Deposit Release, Capture & Customer Confirmation | listDetail | 1 | 0 | — |
| `EMP-100` | Return Completion & Equipment Disposition | listDetail | 2 | 0 | — |

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
  "apis": [
   {
    "contract": "rental",
    "operationId": "listRentalBookings",
    "provenance": "board reading, 19 September 2026",
    "purpose": "Expected back",
    "trigger": "onLoad"
   }
  ],
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
   "regions": [
    {
     "components": [
      {
       "derived": true,
       "impliedBy": "getRentalBooking",
       "kind": "detailPanel",
       "notes": "One record, read-only."
      }
     ],
     "name": "contentBody"
    }
   ],
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
  "apis": [
   {
    "contract": "rental",
    "operationId": "getRentalBooking",
    "provenance": "board reading, 19 September 2026",
    "purpose": "Retrieve by scan",
    "trigger": "onAction"
   }
  ],
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
  "entryState": {
   "params": [
    {
     "from": "navigation",
     "name": "bookingId"
    }
   ]
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
   "regions": [
    {
     "components": [
      {
       "derived": true,
       "impliedBy": "returnRental",
       "kind": "primaryButton",
       "notes": "The act the screen exists for."
      },
      {
       "derived": true,
       "impliedBy": "returnRental",
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**"
      }
     ],
     "name": "contentBody"
    }
   ],
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
  "apis": [
   {
    "contract": "rental",
    "invalidates": [
     "getRentalBooking",
     "listRentalBookings",
     "getRentalAvailability",
     "listOverdueRentals"
    ],
    "operationId": "returnRental",
    "provenance": "board reading, 19 September 2026",
    "purpose": "Record the actual return time",
    "trigger": "onAction"
   }
  ],
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
  "entryState": {
   "params": [
    {
     "from": "navigation",
     "name": "bookingId"
    }
   ]
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
   "regions": [
    {
     "components": [
      {
       "derived": true,
       "impliedBy": "recordRentalInspection",
       "kind": "primaryButton",
       "notes": "The act the screen exists for."
      },
      {
       "derived": true,
       "impliedBy": "recordRentalInspection",
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**"
      }
     ],
     "name": "contentBody"
    }
   ],
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
  "apis": [
   {
    "contract": "rental",
    "invalidates": [
     "getRentalBooking"
    ],
    "operationId": "recordRentalInspection",
    "provenance": "board reading, 19 September 2026",
    "purpose": "Condition on the way back",
    "trigger": "onAction"
   }
  ],
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
  "entryState": {
   "params": [
    {
     "from": "navigation",
     "name": "bookingId"
    }
   ]
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
   "regions": [
    {
     "components": [
      {
       "derived": true,
       "impliedBy": "recordRentalInspection",
       "kind": "primaryButton",
       "notes": "The act the screen exists for."
      },
      {
       "derived": true,
       "impliedBy": "recordRentalInspection",
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**"
      }
     ],
     "name": "contentBody"
    }
   ],
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
  "apis": [
   {
    "contract": "rental",
    "invalidates": [
     "getRentalBooking"
    ],
    "operationId": "recordRentalInspection",
    "provenance": "board reading, 19 September 2026",
    "purpose": "Before against after",
    "trigger": "onAction"
   }
  ],
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
  "entryState": {
   "params": [
    {
     "from": "navigation",
     "name": "bookingId"
    }
   ]
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
   "regions": [
    {
     "components": [
      {
       "derived": true,
       "impliedBy": "assessRentalDamage",
       "kind": "primaryButton",
       "notes": "The act the screen exists for."
      },
      {
       "derived": true,
       "impliedBy": "assessRentalDamage",
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**"
      }
     ],
     "name": "contentBody"
    }
   ],
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
  "apis": [
   {
    "contract": "rental",
    "invalidates": [
     "getRentalBooking"
    ],
    "operationId": "assessRentalDamage",
    "provenance": "board reading, 19 September 2026",
    "purpose": "Price the damage",
    "trigger": "onAction"
   }
  ],
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
  "entryState": {
   "params": [
    {
     "from": "navigation",
     "name": "bookingId"
    }
   ]
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
   "regions": [
    {
     "components": [
      {
       "derived": true,
       "impliedBy": "returnRental",
       "kind": "primaryButton",
       "notes": "The act the screen exists for."
      },
      {
       "derived": true,
       "impliedBy": "returnRental",
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**"
      }
     ],
     "name": "contentBody"
    }
   ],
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
  "apis": [
   {
    "contract": "rental",
    "invalidates": [
     "getRentalBooking",
     "listRentalBookings",
     "getRentalAvailability",
     "listOverdueRentals"
    ],
    "operationId": "returnRental",
    "provenance": "board reading, 19 September 2026",
    "purpose": "Partial return, with what is missing",
    "trigger": "onAction"
   }
  ],
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
  "entryState": {
   "params": [
    {
     "from": "navigation",
     "name": "bookingId"
    }
   ]
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
   "regions": [
    {
     "components": [
      {
       "derived": true,
       "impliedBy": "returnRental",
       "kind": "primaryButton",
       "notes": "The act the screen exists for."
      },
      {
       "derived": true,
       "impliedBy": "returnRental",
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**"
      }
     ],
     "name": "contentBody"
    }
   ],
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
  "apis": [
   {
    "contract": "rental",
    "invalidates": [
     "getRentalBooking",
     "listRentalBookings",
     "getRentalAvailability",
     "listOverdueRentals"
    ],
    "operationId": "returnRental",
    "provenance": "board reading, 19 September 2026",
    "purpose": "Late fee, damage and settlement",
    "trigger": "onAction"
   }
  ],
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
  "entryState": {
   "params": [
    {
     "from": "navigation",
     "name": "bookingId"
    }
   ]
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
   "regions": [
    {
     "components": [
      {
       "derived": true,
       "impliedBy": "returnRental",
       "kind": "primaryButton",
       "notes": "The act the screen exists for."
      },
      {
       "derived": true,
       "impliedBy": "returnRental",
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**"
      }
     ],
     "name": "contentBody"
    }
   ],
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
  "apis": [
   {
    "contract": "rental",
    "invalidates": [
     "getRentalBooking",
     "listRentalBookings",
     "getRentalAvailability",
     "listOverdueRentals"
    ],
    "operationId": "returnRental",
    "provenance": "board reading, 19 September 2026",
    "purpose": "Capture or release the deposit",
    "trigger": "onAction"
   }
  ],
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
  "entryState": {
   "params": [
    {
     "from": "navigation",
     "name": "bookingId"
    }
   ]
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
   "regions": [
    {
     "components": [
      {
       "derived": true,
       "impliedBy": "returnRental",
       "kind": "primaryButton",
       "notes": "The act the screen exists for."
      },
      {
       "derived": true,
       "impliedBy": "returnRental",
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**"
      }
     ],
     "name": "contentBody"
    }
   ],
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
  "apis": [
   {
    "contract": "rental",
    "invalidates": [
     "getRentalBooking",
     "listRentalBookings",
     "getRentalAvailability",
     "listOverdueRentals"
    ],
    "operationId": "returnRental",
    "provenance": "board reading, 19 September 2026",
    "purpose": "Complete, and dispose of the equipment",
    "trigger": "onAction"
   },
   {
    "contract": "maintenance",
    "invalidates": [
     "getAsset",
     "listAssets"
    ],
    "operationId": "setAssetStatus",
    "provenance": "board reading, 19 September 2026",
    "purpose": "Back into the pool, or not",
    "trigger": "onAction"
   }
  ],
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
  "entryState": {
   "params": [
    {
     "from": "navigation",
     "name": "assetId"
    },
    {
     "from": "navigation",
     "name": "bookingId"
    }
   ]
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
{
 "assessRentalDamage": {
  "method": "POST",
  "path": "/rental-bookings/{bookingId}/damage",
  "contract": "rental",
  "summary": "Price the damage, and say who approved it",
  "permission": "RENTAL_OPERATE",
  "offlineCapable": null,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "RentalDamageAssessment",
  "responds": "RentalDamageAssessment"
 },
 "getRentalBooking": {
  "method": "GET",
  "path": "/rental-bookings/{bookingId}",
  "contract": "rental",
  "summary": "One booking, its timeline and its readiness",
  "permission": "RENTAL_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "RentalBooking"
 },
 "listRentalBookings": {
  "method": "GET",
  "path": "/rental-bookings",
  "contract": "rental",
  "summary": "Reservations across venues and locations",
  "permission": "RENTAL_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "locationId",
    "in": "query",
    "required": null
   },
   {
    "name": "from",
    "in": "query",
    "required": null
   },
   {
    "name": "to",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "RentalBooking"
 },
 "recordRentalInspection": {
  "method": "POST",
  "path": "/rental-bookings/{bookingId}/inspection",
  "contract": "rental",
  "summary": "Condition before or after, with evidence",
  "permission": "RENTAL_OPERATE",
  "offlineCapable": true,
  "conflictPolicy": "append",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "RentalInspection",
  "responds": "RentalInspection"
 },
 "returnRental": {
  "method": "POST",
  "path": "/rental-bookings/{bookingId}/return",
  "contract": "rental",
  "summary": "Take it back, inspect it, and settle everything at once",
  "permission": "RENTAL_OPERATE",
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
  "requestBody": "RentalReturn",
  "responds": "RentalSettlement"
 },
 "setAssetStatus": {
  "method": "PUT",
  "path": "/assets/{assetId}/status",
  "contract": "maintenance",
  "summary": "Take an asset out of service or return it",
  "permission": "ASSET_MANAGE",
  "offlineCapable": true,
  "conflictPolicy": "append",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "SetAssetStatusRequest",
  "responds": "AssetStatusResult"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "Asset": {
  "x-ticvai-persistence": "maintenance.asset",
  "allOf": [
   {
    "$ref": "#/components/schemas/CreateAssetRequest"
   },
   {
    "type": "object",
    "x-ticvai-retired-columns": [
     "is_maintenance_overdue",
     "document_refs"
    ],
    "required": [
     "id",
     "status"
    ],
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid"
     },
     "resourceId": {
      "type": "string",
      "format": "uuid",
      "nullable": true,
      "description": "1.2.x. **Where this asset is also bookable.** An AV rig is an asset to maintain and a resource to allocate, and they are the same object seen from two sides.\n**`resources` owns the calendar and this owns the condition.** An asset out of service makes its resource unbookable, which is one link rather than two models of availability.\n"
     },
     "deviceId": {
      "type": "string",
      "format": "uuid",
      "nullable": true,
      "description": "BL-160. **Where this asset is also a registered device.** A turnstile is an asset to maintain and a device to operate, and — exactly as with `resourceId` above — they are the same object seen from two sides.\n**Nothing joined them before this.** A turnstile controller reporting `needsAttention` could not raise a work order against itself, and an engineer closing one had no way back to the device whose firmware caused it.\n**Null for most assets and for most devices.** A chiller is not a device and a signature pad is not on the asset register; the link is sparse, and it lives here rather than on `platform.device` because `platform` is the foundation tier and a foreign key pointing from it into `maintenance` would invert the tiers — every cell running a spine would carry a column for a satellite it may not deploy.\n"
     },
     "acquisitionCost": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "acquiredOn": {
      "type": "string",
      "format": "date",
      "nullable": true
     },
     "depreciation": {
      "type": "object",
      "nullable": true,
      "description": "**Recorded here and posted by `finance`.** Depreciation is an accounting act and the asset register is where the useful life is actually known — an engineer knows a chiller lasts fifteen years and an accountant knows what to do about it.\n",
      "properties": {
       "method": {
        "type": "string",
        "enum": [
         "straightLine",
         "reducingBalance",
         "unitsOfProduction",
         "none"
        ]
       },
       "usefulLifeMonths": {
        "type": "integer"
       },
       "residualValue": {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       },
       "accumulatedDepreciation": {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      }
     },
     "retiredOn": {
      "type": "string",
      "format": "date",
      "nullable": true,
      "description": "**Retirement is not deletion.** A work order from three years ago still names this asset, and an inspection record with no asset is an inspection of nothing.\n"
     },
     "disposalProceeds": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "status": {
      "$ref": "#/components/schemas/AssetStatus"
     },
     "statusReason": {
      "type": "string",
      "nullable": true
     },
     "openWorkOrderCount": {
      "type": "integer",
      "readOnly": true,
      "x-ticvai-derived": "onWrite",
      "description": "Work orders on this asset whose status is `open`, `assigned`, `inProgress`, `paused` or `awaitingParts` — the same set `AssetDetail.openWorkOrders` returns. **Maintained on write**: `createWorkOrder` and every transition into or out of that set (complete, cancel, close, reject back to open) adjust it in the same transaction as the work-order row.\n"
     },
     "nextMaintenanceDueAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true,
      "readOnly": true,
      "x-ticvai-derived": "onWrite",
      "description": "The earliest `nextDueAt` among this asset's active maintenance plans; null when none has one. **Maintained on write**: recomputed whenever one of those plans is created, amended, suspended or has its `nextDueAt` moved by a completed work order. `listAssets?maintenanceDue` filters on this column against the clock.\n"
     },
     "isMaintenanceOverdue": {
      "type": "boolean",
      "readOnly": true,
      "x-ticvai-persisted": false,
      "x-ticvai-derived": "onRead",
      "description": "`nextMaintenanceDueAt` is in the past at the moment of the read. **Computed on read and not stored** — it depends on the clock, so a stored copy is stale the minute after it is written.\n"
     },
     "lastInspectionAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true,
      "readOnly": true,
      "x-ticvai-derived": "onWrite",
      "description": "`performedAt` of the latest inspection submitted against this asset. **Maintained on write** by `submitInspection`, in the same transaction as the inspection row; an inspection synced late with an earlier `performedAt` does not move it back.\n"
     },
     "usageCounter": {
      "type": "number",
      "nullable": true,
      "description": "Cycles, hours or kilometres. Drives usage-based maintenance."
     }
    }
   }
  ]
 },
 "AssetStatus": {
  "type": "string",
  "enum": [
   "inService",
   "outOfService",
   "underMaintenance",
   "awaitingParts",
   "retired",
   "disposed"
  ]
 },
 "AssetStatusResult": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "asset",
   "downstreamEffects"
  ],
  "properties": {
   "asset": {
    "$ref": "#/components/schemas/Asset"
   },
   "downstreamEffects": {
    "type": "object",
    "description": "What else changed. Surfaced so the person taking a ride out of service sees the commercial consequence at the moment they do it.\n",
    "properties": {
     "productsSuspended": {
      "type": "array",
      "items": {
       "type": "string",
       "format": "uuid"
      }
     },
     "accessPointBlocked": {
      "type": "boolean"
     },
     "performancesAffected": {
      "type": "integer"
     },
     "workOrderId": {
      "type": "string",
      "format": "uuid",
      "nullable": true
     }
    }
   }
  }
 },
 "RentalBooking": {
  "type": "object",
  "x-ticvai-persistence": "rental.booking",
  "description": "Board 5. **The booking outlives the order** — an order completes at payment and the rental is still out.\n",
  "required": [
   "id",
   "productId",
   "from",
   "to",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "reference": {
    "type": "string"
   },
   "productId": {
    "type": "string",
    "format": "uuid"
   },
   "locationId": {
    "type": "string",
    "format": "uuid"
   },
   "returnLocationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "customerId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "orderId": {
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
   "quantity": {
    "type": "integer"
   },
   "status": {
    "type": "string",
    "enum": [
     "draft",
     "confirmed",
     "awaitingArrival",
     "checkedOut",
     "overdue",
     "partiallyReturned",
     "completed",
     "completedWithDamage",
     "notReturned",
     "cancelled",
     "noShow"
    ]
   },
   "checkedOutAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "dueBackAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "returnedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "depositAuthorisationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "accruedLateFee": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "readiness": {
    "type": "array",
    "readOnly": true,
    "description": "**Computed, not stored** — agreement, requirements, deposit, equipment.",
    "items": {
     "type": "object",
     "properties": {
      "check": {
       "type": "string"
      },
      "satisfied": {
       "type": "boolean"
      },
      "detail": {
       "type": "string",
       "nullable": true
      }
     }
    }
   },
   "participants": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/RentalParticipant"
    }
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "RentalDamageAssessment": {
  "type": "object",
  "x-ticvai-persistence": "rental.damage_assessment",
  "description": "Board 8.6. **A dispute is a state, not a deletion.**",
  "required": [
   "amount",
   "description"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "assetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "description": {
    "type": "string"
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "inspectionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "assessedBy": {
    "type": "string",
    "format": "uuid"
   },
   "approvedBy": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "customerAcknowledgement": {
    "type": "string",
    "enum": [
     "accepted",
     "disputed",
     "notPresented"
    ],
    "default": "notPresented"
   },
   "workOrderId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Raised in `maintenance`, so the repair is tracked where every other repair is."
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "RentalInspection": {
  "type": "object",
  "x-ticvai-persistence": "rental.inspection",
  "description": "Boards 6.5 and 8.4. **Before and after are one record shape with a phase**, which is what makes the comparison view possible.\n",
  "required": [
   "phase",
   "condition"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "assetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "phase": {
    "type": "string",
    "enum": [
     "preRental",
     "postRental"
    ]
   },
   "condition": {
    "type": "string",
    "enum": [
     "good",
     "minorDamage",
     "majorDamage",
     "faulty",
     "notReturned"
    ],
    "description": "**26 August: simplified state attributes.** *\"rental/equipment items can be tracked with simplified state attributes (e.g., available, rented, faulty) rather than requiring granular custom attributes for this category — agreed by Allam.\"* So the condition is a short enum, and anything finer belongs in the note or the photographs.\n"
   },
   "checklist": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "item": {
       "type": "string"
      },
      "passed": {
       "type": "boolean"
      },
      "note": {
       "type": "string",
       "nullable": true
      }
     }
    }
   },
   "note": {
    "type": "string",
    "nullable": true
   },
   "photoAssetIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "inspectedBy": {
    "type": "string",
    "format": "uuid"
   },
   "inspectedAt": {
    "type": "string",
    "format": "date-time"
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "RentalParticipant": {
  "type": "object",
  "x-ticvai-persistence": "rental.participant",
  "description": "Board 5.5. **A group rental is one booking with participants**, because the agreement, the deposit and the return are handled together.\n",
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string"
   },
   "isPrimaryRenter": {
    "type": "boolean",
    "default": false
   },
   "dateOfBirth": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "idNumber": {
    "type": "string",
    "nullable": true
   },
   "guardianName": {
    "type": "string",
    "nullable": true
   },
   "emergencyContact": {
    "type": "string",
    "nullable": true
   },
   "hasSignedWaiver": {
    "type": "boolean",
    "readOnly": true
   },
   "customFields": {
    "type": "object",
    "additionalProperties": true
   }
  }
 },
 "RentalReturn": {
  "type": "object",
  "description": "Board 8. **Late fee, damage and partial return all land on one deposit.**",
  "required": [
   "returnedAt"
  ],
  "properties": {
   "returnedAt": {
    "type": "string",
    "format": "date-time"
   },
   "returnLocationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "returnedAssetIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "missingAssetIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "inspection": {
    "$ref": "#/components/schemas/RentalInspection"
   },
   "damage": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/RentalDamageAssessment"
    }
   },
   "waiveLateFee": {
    "type": "boolean",
    "default": false
   },
   "overrideId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   }
  }
 },
 "RentalSettlement": {
  "type": "object",
  "x-ticvai-persistence": "rental.settlement",
  "description": "Board 8.8. **One statement, because there is one deposit.** *Capture AED 120, release AED 380.*\n",
  "properties": {
   "bookingId": {
    "type": "string",
    "format": "uuid"
   },
   "expectedReturnAt": {
    "type": "string",
    "format": "date-time"
   },
   "actualReturnAt": {
    "type": "string",
    "format": "date-time"
   },
   "gracePeriodMinutes": {
    "type": "integer"
   },
   "chargeableLateMinutes": {
    "type": "integer"
   },
   "lateFee": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "damageFee": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "missingItemFee": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "totalCharged": {
    "x-ticvai-column": "gross_charged_amount",
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "depositCaptured": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "depositReleased": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "balanceDue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "**Where the charges exceed the deposit.** A bike written off against a AED 200 hold leaves a real debt, and netting it to zero hides it.\n"
   },
   "outcome": {
    "type": "string",
    "enum": [
     "completed",
     "completedWithDamage",
     "partiallyReturned",
     "notReturned"
    ]
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "SetAssetStatusRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "status",
   "reason",
   "recordedAt"
  ],
  "properties": {
   "status": {
    "$ref": "#/components/schemas/AssetStatus"
   },
   "reason": {
    "type": "string",
    "minLength": 3,
    "maxLength": 1000
   },
   "inspectionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Required for return to service where the asset demands it."
   },
   "raiseWorkOrder": {
    "type": "boolean",
    "default": false
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 }
}
```
