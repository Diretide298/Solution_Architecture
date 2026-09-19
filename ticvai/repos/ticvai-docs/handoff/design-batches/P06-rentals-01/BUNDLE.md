# P06-rentals-01 — P06 · Rentals (1 of 3)

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
| `EMP-071` | Rental Checkout Command Center | commandCentre | 0 | 0 | — |
| `EMP-072` | Voucher Scan & Reservation Retrieval | listDetail | 0 | 0 | — |
| `EMP-073` | Checkout Readiness Validation | listDetail | 0 | 0 | — |
| `EMP-074` | Equipment Assignment Workspace | listDetail | 0 | 0 | — |
| `EMP-075` | Equipment Scan & Validation | listDetail | 0 | 0 | — |
| `EMP-076` | Pre-Rental Condition Inspection | listDetail | 0 | 0 | — |
| `EMP-077` | Safety & Handover Checklist | listDetail | 0 | 0 | — |
| `EMP-078` | Deposit & Financial Handover Validation | listDetail | 0 | 0 | — |
| `EMP-079` | Group & Multi-Item Checkout | listDetail | 0 | 0 | — |
| `EMP-080` | Checkout Confirmation & Rental Activation | configEditor | 0 | 0 | — |

## Thin screens in this batch

**EMP-072, EMP-073, EMP-074, EMP-075, EMP-076, EMP-077, EMP-078, EMP-079, EMP-080 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "EMP-071",
  "name": "Rental Checkout Command Center",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "sameAs": "BO-544",
   "book": "Rental_Management.pdf",
   "board": "6",
   "number": "1",
   "page": 64
  },
  "implementation": {
   "app": "venue-staff-app",
   "route": "/rentals/rental-checkout-command-center-emp-071",
   "component": "apps/venue-staff-app/src/routes/rentals/RentalCheckoutCommandCenter.tsx",
   "status": "notStarted"
  },
  "density": "comfortable",
  "notes": "The staff-app form of `BO-544`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.",
  "purpose": "Provide rental operators with a real-time operational queue of customers requiring equipment checkout.",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "layout": {
   "regions": [
    {
     "components": [
      {
       "kind": "searchField",
       "label": "Search rental checkout",
       "provenance": "pack Rental_Management.pdf, page 64 §Filters"
      },
      {
       "columns": [
        "Location",
        "Product",
        "Start Time",
        "Booking Type",
        "Group/Individual",
        "Readiness",
        "Status"
       ],
       "kind": "multiSelect",
       "label": "Filter by",
       "notes": "The pack filters this screen by location, product, start time, booking type, group/individual, readiness and 1 more — which are present is a decision the pack already made.",
       "provenance": "pack Rental_Management.pdf, page 64 §Filters"
      }
     ],
     "name": "contentBody",
     "slot": "filters"
    },
    {
     "components": [
      {
       "kind": "metricTile",
       "label": "Arriving Next 30 Min",
       "provenance": "pack Rental_Management.pdf, page 64 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Awaiting Checkout",
       "provenance": "pack Rental_Management.pdf, page 64 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Ready for Checkout",
       "provenance": "pack Rental_Management.pdf, page 64 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Checkout in Progress",
       "provenance": "pack Rental_Management.pdf, page 64 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Checked Out Today",
       "provenance": "pack Rental_Management.pdf, page 64 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Missing Requirements",
       "provenance": "pack Rental_Management.pdf, page 64 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Equipment Issues",
       "provenance": "pack Rental_Management.pdf, page 64 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Late Arrivals",
       "provenance": "pack Rental_Management.pdf, page 64 §KPI Cards"
      }
     ],
     "name": "contentBody",
     "slot": "headline"
    }
   ],
   "template": "dashboard"
  },
  "states": {
   "emptyFirstRun": "No rental checkout yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "The filter narrowed it and the rental checkout are still there. Names the active filter and offers to clear it.",
   "error": "Could not load. Names which read failed and leaves the rental checkout untouched.",
   "loading": "The rental checkout list; the counts above it resolve separately.",
   "offline": "TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it."
  },
  "apis": [],
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 64. 0 of 7 labels bound to a contract property; 15 of 23 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "preloaded": [
    "Arriving Next 30 Min",
    "Awaiting Checkout",
    "Ready for Checkout",
    "Checkout in Progress",
    "Checked Out Today",
    "Missing Requirements"
   ]
  },
  "navigation": {
   "entryFrom": [
    "EMP-003",
    "EMP-072",
    "EMP-073",
    "EMP-074",
    "EMP-075",
    "EMP-076",
    "EMP-077",
    "EMP-078",
    "EMP-079",
    "EMP-080"
   ],
   "exitTo": [
    "EMP-003",
    "EMP-072",
    "EMP-073",
    "EMP-074",
    "EMP-075",
    "EMP-076",
    "EMP-077",
    "EMP-078",
    "EMP-079",
    "EMP-080"
   ],
   "transitions": [
    {
     "to": "EMP-003",
     "trigger": "Back to Home — on duty",
     "provenance": "structural — Rental board 6 on the staff app, 11 September 2026",
     "back": true
    },
    {
     "to": "EMP-072",
     "trigger": "Voucher Scan & Reservation Retrieval",
     "provenance": "structural — Rental board 6 on the staff app, 11 September 2026"
    },
    {
     "to": "EMP-073",
     "trigger": "Checkout Readiness Validation",
     "provenance": "structural — Rental board 6 on the staff app, 11 September 2026"
    },
    {
     "to": "EMP-074",
     "trigger": "Equipment Assignment Workspace",
     "provenance": "structural — Rental board 6 on the staff app, 11 September 2026"
    },
    {
     "to": "EMP-075",
     "trigger": "Equipment Scan & Validation",
     "provenance": "structural — Rental board 6 on the staff app, 11 September 2026"
    },
    {
     "to": "EMP-076",
     "trigger": "Pre-Rental Condition Inspection",
     "provenance": "structural — Rental board 6 on the staff app, 11 September 2026"
    },
    {
     "to": "EMP-077",
     "trigger": "Safety & Handover Checklist",
     "provenance": "structural — Rental board 6 on the staff app, 11 September 2026"
    },
    {
     "to": "EMP-078",
     "trigger": "Deposit & Financial Handover Validation",
     "provenance": "structural — Rental board 6 on the staff app, 11 September 2026"
    },
    {
     "to": "EMP-079",
     "trigger": "Group & Multi-Item Checkout",
     "provenance": "structural — Rental board 6 on the staff app, 11 September 2026"
    },
    {
     "to": "EMP-080",
     "trigger": "Checkout Confirmation & Rental Activation",
     "provenance": "structural — Rental board 6 on the staff app, 11 September 2026"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-071"
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
  "id": "EMP-072",
  "name": "Voucher Scan & Reservation Retrieval",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "sameAs": "BO-545",
   "book": "Rental_Management.pdf",
   "board": "6",
   "number": "2",
   "page": 65
  },
  "implementation": {
   "app": "venue-staff-app",
   "route": "/rentals/voucher-scan-reservation-retrieval-emp-072",
   "component": "apps/venue-staff-app/src/routes/rentals/VoucherScanReservationRetrieval.tsx",
   "status": "notStarted"
  },
  "density": "comfortable",
  "notes": "The staff-app form of `BO-545`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.",
  "purpose": "Quickly identify the customer reservation when they arrive. The original requirement specifically requires scanning and validating the customer's voucher/ticket.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "layout": {
   "regions": [],
   "template": "split"
  },
  "states": {
   "emptyFirstRun": "No voucher scan reservation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "The filter narrowed it and the voucher scan reservation are still there. Names the active filter and offers to clear it.",
   "error": "Could not load. Names which read failed and leaves the voucher scan reservation untouched.",
   "loading": "The voucher scan reservation list.",
   "offline": "TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it."
  },
  "gaps": [
   {
    "operation": null,
    "source": "pack Rental_Management.pdf, page 65",
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built."
   },
   {
    "operation": null,
    "source": "pack Rental_Management.pdf, page 65",
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built."
   }
  ],
  "apis": [],
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 65. 0 of 0 labels bound to a contract property; 0 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "EMP-071"
   ],
   "exitTo": [
    "EMP-071"
   ],
   "transitions": [
    {
     "to": "EMP-071",
     "trigger": "Back to Rental Checkout Command Center",
     "provenance": "structural — Rental board 6 on the staff app, 11 September 2026",
     "back": true
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-072"
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
  "id": "EMP-073",
  "name": "Checkout Readiness Validation",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "sameAs": "BO-546",
   "book": "Rental_Management.pdf",
   "board": "6",
   "number": "3",
   "page": 66
  },
  "implementation": {
   "app": "venue-staff-app",
   "route": "/rentals/checkout-readiness-validation-emp-073",
   "component": "apps/venue-staff-app/src/routes/rentals/CheckoutReadinessValidation.tsx",
   "status": "notStarted"
  },
  "density": "comfortable",
  "notes": "The staff-app form of `BO-546`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.",
  "purpose": "Prevent equipment from being handed over until mandatory requirements are satisfied.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "layout": {
   "regions": [],
   "template": "split"
  },
  "states": {
   "emptyFirstRun": "No checkout readiness validation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "The filter narrowed it and the checkout readiness validation are still there. Names the active filter and offers to clear it.",
   "error": "Could not load. Names which read failed and leaves the checkout readiness validation untouched.",
   "loading": "The checkout readiness validation list.",
   "offline": "TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it."
  },
  "gaps": [
   {
    "operation": null,
    "source": "pack Rental_Management.pdf, page 66",
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built."
   },
   {
    "operation": null,
    "source": "pack Rental_Management.pdf, page 66",
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built."
   }
  ],
  "apis": [],
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 66. 0 of 0 labels bound to a contract property; 0 of 19 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "EMP-071"
   ],
   "exitTo": [
    "EMP-071"
   ],
   "transitions": [
    {
     "to": "EMP-071",
     "trigger": "Back to Rental Checkout Command Center",
     "provenance": "structural — Rental board 6 on the staff app, 11 September 2026",
     "back": true
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-073"
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
  "id": "EMP-074",
  "name": "Equipment Assignment Workspace",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "sameAs": "BO-547",
   "book": "Rental_Management.pdf",
   "board": "6",
   "number": "4",
   "page": 67
  },
  "implementation": {
   "app": "venue-staff-app",
   "route": "/rentals/equipment-assignment-workspace-emp-074",
   "component": "apps/venue-staff-app/src/routes/rentals/EquipmentAssignmentWorkspace.tsx",
   "status": "notStarted"
  },
  "density": "comfortable",
  "notes": "The staff-app form of `BO-547`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.",
  "purpose": "Assign the actual physical equipment to the reservation.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "layout": {
   "regions": [],
   "template": "split"
  },
  "states": {
   "emptyFirstRun": "No equipment yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "The filter narrowed it and the equipment are still there. Names the active filter and offers to clear it.",
   "error": "Could not load. Names which read failed and leaves the equipment untouched.",
   "loading": "The equipment list.",
   "offline": "TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it."
  },
  "gaps": [
   {
    "operation": null,
    "source": "pack Rental_Management.pdf, page 67",
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built."
   },
   {
    "operation": null,
    "source": "pack Rental_Management.pdf, page 67",
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built."
   }
  ],
  "apis": [],
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 67. 0 of 0 labels bound to a contract property; 0 of 18 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "EMP-071"
   ],
   "exitTo": [
    "EMP-071"
   ],
   "transitions": [
    {
     "to": "EMP-071",
     "trigger": "Back to Rental Checkout Command Center",
     "provenance": "structural — Rental board 6 on the staff app, 11 September 2026",
     "back": true
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-074"
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
  "id": "EMP-075",
  "name": "Equipment Scan & Validation",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "sameAs": "BO-548",
   "book": "Rental_Management.pdf",
   "board": "6",
   "number": "5",
   "page": 68
  },
  "implementation": {
   "app": "venue-staff-app",
   "route": "/rentals/equipment-scan-validation-emp-075",
   "component": "apps/venue-staff-app/src/routes/rentals/EquipmentScanValidation.tsx",
   "status": "notStarted"
  },
  "density": "comfortable",
  "notes": "The staff-app form of `BO-548`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.",
  "purpose": "Ensure the operator cannot accidentally assign the wrong, unavailable or unsafe equipment.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "layout": {
   "regions": [],
   "template": "split"
  },
  "states": {
   "emptyFirstRun": "No equipment scan validation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "The filter narrowed it and the equipment scan validation are still there. Names the active filter and offers to clear it.",
   "error": "Could not load. Names which read failed and leaves the equipment scan validation untouched.",
   "loading": "The equipment scan validation list.",
   "offline": "TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it."
  },
  "gaps": [
   {
    "operation": null,
    "source": "pack Rental_Management.pdf, page 68",
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built."
   },
   {
    "operation": null,
    "source": "pack Rental_Management.pdf, page 68",
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built."
   }
  ],
  "apis": [],
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 68. 0 of 0 labels bound to a contract property; 0 of 17 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "EMP-071"
   ],
   "exitTo": [
    "EMP-071"
   ],
   "transitions": [
    {
     "to": "EMP-071",
     "trigger": "Back to Rental Checkout Command Center",
     "provenance": "structural — Rental board 6 on the staff app, 11 September 2026",
     "back": true
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-075"
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
  "id": "EMP-076",
  "name": "Pre-Rental Condition Inspection",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "sameAs": "BO-549",
   "book": "Rental_Management.pdf",
   "board": "6",
   "number": "6",
   "page": 69
  },
  "implementation": {
   "app": "venue-staff-app",
   "route": "/rentals/pre-rental-condition-inspection-emp-076",
   "component": "apps/venue-staff-app/src/routes/rentals/PreRentalConditionInspection.tsx",
   "status": "notStarted"
  },
  "density": "comfortable",
  "notes": "The staff-app form of `BO-549`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.",
  "purpose": "Document the equipment condition before handover. Photo capture at checkout is specifically recommended in the source.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "layout": {
   "regions": [
    {
     "components": [
      {
       "kind": "primaryButton",
       "label": "Asset",
       "provenance": "pack Rental_Management.pdf, page 69 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Checkout inspection",
       "provenance": "pack Rental_Management.pdf, page 69 §Support"
      }
     ],
     "name": "actionBar",
     "slot": "rowActions"
    }
   ],
   "template": "split"
  },
  "states": {
   "emptyFirstRun": "No pre-rental condition inspection yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "The filter narrowed it and the pre-rental condition inspection are still there. Names the active filter and offers to clear it.",
   "error": "Could not load. Names which read failed and leaves the pre-rental condition inspection untouched.",
   "loading": "The pre-rental condition inspection list.",
   "offline": "TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it."
  },
  "gaps": [
   {
    "operation": null,
    "source": "pack Rental_Management.pdf, page 69 §Support",
    "why": "**The pack names 2 actions on this screen and the screen declares 0 operations.** Unserved: Asset, Checkout inspection. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side."
   },
   {
    "operation": null,
    "source": "pack Rental_Management.pdf, page 69",
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built."
   },
   {
    "operation": null,
    "source": "pack Rental_Management.pdf, page 69",
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built."
   }
  ],
  "apis": [],
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 69. 0 of 0 labels bound to a contract property; 2 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "EMP-071"
   ],
   "exitTo": [
    "EMP-071"
   ],
   "transitions": [
    {
     "to": "EMP-071",
     "trigger": "Back to Rental Checkout Command Center",
     "provenance": "structural — Rental board 6 on the staff app, 11 September 2026",
     "back": true
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-076"
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
  "id": "EMP-077",
  "name": "Safety & Handover Checklist",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "sameAs": "BO-550",
   "book": "Rental_Management.pdf",
   "board": "6",
   "number": "7",
   "page": 70
  },
  "implementation": {
   "app": "venue-staff-app",
   "route": "/rentals/safety-handover-checklist-emp-077",
   "component": "apps/venue-staff-app/src/routes/rentals/SafetyHandoverChecklist.tsx",
   "status": "notStarted"
  },
  "density": "comfortable",
  "notes": "The staff-app form of `BO-550`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.",
  "purpose": "Ensure mandatory operational and safety steps are completed before starting the rental. Example — Kayak ✓ Life jacket provided ✓ Paddle provided ✓ Safety briefing completed ✓ Emergency procedure explained ✓ Restricted areas explained ✓ Customer confirms swimming ability Example — Bicycle ✓ Helmet provided ✓ Brake check completed ✓ Seat adjusted ✓ Safety briefing completed The checklist should be configurable by rental product/category from Board 1.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "layout": {
   "regions": [],
   "template": "split"
  },
  "states": {
   "emptyFirstRun": "No safety handover checklist yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "The filter narrowed it and the safety handover checklist are still there. Names the active filter and offers to clear it.",
   "error": "Could not load. Names which read failed and leaves the safety handover checklist untouched.",
   "loading": "The safety handover checklist list.",
   "offline": "TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it."
  },
  "gaps": [
   {
    "operation": null,
    "source": "pack Rental_Management.pdf, page 70",
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built."
   },
   {
    "operation": null,
    "source": "pack Rental_Management.pdf, page 70",
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built."
   }
  ],
  "apis": [],
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 70. 0 of 0 labels bound to a contract property; 0 of 17 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "EMP-071"
   ],
   "exitTo": [
    "EMP-071"
   ],
   "transitions": [
    {
     "to": "EMP-071",
     "trigger": "Back to Rental Checkout Command Center",
     "provenance": "structural — Rental board 6 on the staff app, 11 September 2026",
     "back": true
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-077"
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
  "id": "EMP-078",
  "name": "Deposit & Financial Handover Validation",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "sameAs": "BO-551",
   "book": "Rental_Management.pdf",
   "board": "6",
   "number": "8",
   "page": 70
  },
  "implementation": {
   "app": "venue-staff-app",
   "route": "/rentals/deposit-financial-handover-validation-emp-078",
   "component": "apps/venue-staff-app/src/routes/rentals/DepositFinancialHandoverValidation.tsx",
   "status": "notStarted"
  },
  "density": "comfortable",
  "notes": "The staff-app form of `BO-551`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.",
  "purpose": "Give the rental operator a clear commercial status without requiring them to enter the Finance module.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "layout": {
   "regions": [],
   "template": "split"
  },
  "states": {
   "emptyFirstRun": "No deposit financial handover yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "The filter narrowed it and the deposit financial handover are still there. The pack's own statuses are ✓ AUTHORIZED — the state names which is selected.",
   "error": "Could not load. Names which read failed and leaves the deposit financial handover untouched.",
   "loading": "The deposit financial handover list.",
   "offline": "TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it."
  },
  "gaps": [
   {
    "operation": null,
    "source": "pack Rental_Management.pdf, page 70",
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built."
   },
   {
    "operation": null,
    "source": "pack Rental_Management.pdf, page 70",
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built."
   }
  ],
  "apis": [],
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 70. 0 of 0 labels bound to a contract property; 1 of 13 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "EMP-071"
   ],
   "exitTo": [
    "EMP-071"
   ],
   "transitions": [
    {
     "to": "EMP-071",
     "trigger": "Back to Rental Checkout Command Center",
     "provenance": "structural — Rental board 6 on the staff app, 11 September 2026",
     "back": true
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-078"
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
  "id": "EMP-079",
  "name": "Group & Multi-Item Checkout",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "sameAs": "BO-552",
   "book": "Rental_Management.pdf",
   "board": "6",
   "number": "9",
   "page": 71
  },
  "implementation": {
   "app": "venue-staff-app",
   "route": "/rentals/group-multi-item-checkout-emp-079",
   "component": "apps/venue-staff-app/src/routes/rentals/GroupMultiItemCheckout.tsx",
   "status": "notStarted"
  },
  "density": "comfortable",
  "notes": "The staff-app form of `BO-552`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.",
  "purpose": "Provide an efficient checkout workflow for group rentals and reservations containing multiple equipment units. This is particularly important because the original requirements support group reservations.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "layout": {
   "regions": [],
   "template": "split"
  },
  "states": {
   "emptyFirstRun": "No group multi-item checkout yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "The filter narrowed it and the group multi-item checkout are still there. Names the active filter and offers to clear it.",
   "error": "Could not load. Names which read failed and leaves the group multi-item checkout untouched.",
   "loading": "The group multi-item checkout list.",
   "offline": "TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it."
  },
  "gaps": [
   {
    "operation": null,
    "source": "pack Rental_Management.pdf, page 71",
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built."
   },
   {
    "operation": null,
    "source": "pack Rental_Management.pdf, page 71",
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built."
   }
  ],
  "apis": [],
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 71. 0 of 0 labels bound to a contract property; 0 of 18 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "EMP-071"
   ],
   "exitTo": [
    "EMP-071"
   ],
   "transitions": [
    {
     "to": "EMP-071",
     "trigger": "Back to Rental Checkout Command Center",
     "provenance": "structural — Rental board 6 on the staff app, 11 September 2026",
     "back": true
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-079"
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
  "id": "EMP-080",
  "name": "Checkout Confirmation & Rental Activation",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "sameAs": "BO-553",
   "book": "Rental_Management.pdf",
   "board": "6",
   "number": "10",
   "page": 72
  },
  "implementation": {
   "app": "venue-staff-app",
   "route": "/rentals/checkout-confirmation-rental-activation-emp-080",
   "component": "apps/venue-staff-app/src/routes/rentals/CheckoutConfirmationRentalActivation.tsx",
   "status": "notStarted"
  },
  "density": "comfortable",
  "notes": "The staff-app form of `BO-553`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.",
  "purpose": "Officially start the rental and transition the reservation into an active rental.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Options; Select Equipment) and no display directory — it is settings, not a population",
  "layout": {
   "regions": [
    {
     "components": [
      {
       "kind": "textField",
       "label": "Email | SMS | App Notification",
       "provenance": "pack Rental_Management.pdf, page 72 §Options"
      },
      {
       "kind": "selectField",
       "label": "↓",
       "provenance": "pack Rental_Management.pdf, page 72 §Select Equipment"
      }
     ],
     "name": "contentBody",
     "slot": "fields"
    }
   ],
   "template": "form"
  },
  "states": {
   "emptyFirstRun": "No checkout confirmation rental configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist",
   "error": "Could not load. Names which read failed and leaves the checkout confirmation rental untouched.",
   "loading": "The checkout confirmation rental configuration as saved.",
   "offline": "TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it."
  },
  "apis": [],
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 72. 0 of 0 labels bound to a contract property; 2 of 96 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "navigation": {
   "entryFrom": [
    "EMP-071"
   ],
   "exitTo": [
    "EMP-071"
   ],
   "transitions": [
    {
     "to": "EMP-071",
     "trigger": "Back to Rental Checkout Command Center",
     "provenance": "structural — Rental board 6 on the staff app, 11 September 2026",
     "back": true
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P06 Venue Staff App.dc.html#emp-080"
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
