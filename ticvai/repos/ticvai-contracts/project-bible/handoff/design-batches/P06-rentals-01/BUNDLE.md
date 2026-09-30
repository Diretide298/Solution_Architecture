# P06-rentals-01 — P06 · Rentals (1 of 3)

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
  `ASSET_VIEW, RENTAL_OPERATE, RENTAL_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **4 of these operations work offline**: assignRentalEquipment, checkOutRental, lookupAsset, recordRentalInspection
  — and the rest do not. A surface that looks the same online and off is lying.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `EMP-071` | Rental Checkout Command Center | commandCentre | 1 | 0 | — |
| `EMP-072` | Voucher Scan & Reservation Retrieval | listDetail | 1 | 0 | — |
| `EMP-073` | Checkout Readiness Validation | listDetail | 1 | 0 | — |
| `EMP-074` | Equipment Assignment Workspace | listDetail | 1 | 0 | — |
| `EMP-075` | Equipment Scan & Validation | listDetail | 2 | 0 | — |
| `EMP-076` | Pre-Rental Condition Inspection | listDetail | 1 | 0 | — |
| `EMP-077` | Safety & Handover Checklist | listDetail | 1 | 0 | — |
| `EMP-078` | Deposit & Financial Handover Validation | listDetail | 1 | 0 | — |
| `EMP-079` | Group & Multi-Item Checkout | listDetail | 1 | 0 | — |
| `EMP-080` | Checkout Confirmation & Rental Activation | configEditor | 1 | 0 | — |

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
  "apis": [
   {
    "contract": "rental",
    "operationId": "listRentalBookings",
    "provenance": "board reading, 19 September 2026",
    "purpose": "Awaiting arrival",
    "trigger": "onLoad"
   }
  ],
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
  "apis": [
   {
    "contract": "rental",
    "operationId": "getRentalBooking",
    "provenance": "board reading, 19 September 2026",
    "purpose": "Retrieve by voucher scan",
    "trigger": "onAction"
   }
  ],
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
  "apis": [
   {
    "contract": "rental",
    "operationId": "getRentalBooking",
    "provenance": "board reading, 19 September 2026",
    "purpose": "What is still outstanding",
    "trigger": "onAction"
   }
  ],
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
   "regions": [
    {
     "components": [
      {
       "derived": true,
       "impliedBy": "assignRentalEquipment",
       "kind": "primaryButton",
       "label": "Assign rental equipment",
       "notes": "The act the screen exists for."
      },
      {
       "derived": true,
       "impliedBy": "assignRentalEquipment",
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
  "apis": [
   {
    "contract": "rental",
    "invalidates": [
     "getRentalBooking"
    ],
    "operationId": "assignRentalEquipment",
    "provenance": "board reading, 19 September 2026",
    "purpose": "Bind the assets",
    "trigger": "onAction"
   }
  ],
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
   "regions": [
    {
     "components": [
      {
       "derived": true,
       "impliedBy": "assignRentalEquipment",
       "kind": "primaryButton",
       "label": "Assign rental equipment",
       "notes": "The act the screen exists for."
      },
      {
       "derived": true,
       "impliedBy": "lookupAsset",
       "kind": "searchField",
       "label": "Search",
       "notes": "A search that returns nothing must say so differently from a search not yet run."
      },
      {
       "derived": true,
       "impliedBy": "assignRentalEquipment",
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
  "apis": [
   {
    "contract": "rental",
    "invalidates": [
     "getRentalBooking"
    ],
    "operationId": "assignRentalEquipment",
    "provenance": "board reading, 19 September 2026",
    "purpose": "Scan to assign",
    "trigger": "onAction"
   },
   {
    "contract": "maintenance",
    "operationId": "lookupAsset",
    "provenance": "board reading, 19 September 2026",
    "purpose": "Resolve the scanned code",
    "trigger": "onAction"
   }
  ],
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
       "label": "Reservation",
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
    },
    {
     "components": [],
     "name": "contentBody"
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
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 69"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 69"
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
    "purpose": "Condition before it goes out",
    "trigger": "onAction"
   }
  ],
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 69. 0 of 0 labels bound to a contract property; 3 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Asset, Reservation, Checkout inspection are choices sent by `recordRentalInspection` (assetId, bookingId (path), phase preRental).",
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
   "regions": [
    {
     "components": [
      {
       "derived": true,
       "impliedBy": "checkOutRental",
       "kind": "primaryButton",
       "notes": "The act the screen exists for."
      },
      {
       "derived": true,
       "impliedBy": "checkOutRental",
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
  "apis": [
   {
    "contract": "rental",
    "invalidates": [
     "getRentalBooking",
     "listRentalBookings",
     "getRentalAvailability"
    ],
    "operationId": "checkOutRental",
    "provenance": "board reading, 19 September 2026",
    "purpose": "Safety briefing and handover",
    "trigger": "onAction"
   }
  ],
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
   "regions": [
    {
     "components": [
      {
       "derived": true,
       "impliedBy": "checkOutRental",
       "kind": "primaryButton",
       "notes": "The act the screen exists for."
      },
      {
       "derived": true,
       "impliedBy": "checkOutRental",
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
  "apis": [
   {
    "contract": "rental",
    "invalidates": [
     "getRentalBooking",
     "listRentalBookings",
     "getRentalAvailability"
    ],
    "operationId": "checkOutRental",
    "provenance": "board reading, 19 September 2026",
    "purpose": "Hold the deposit",
    "trigger": "onAction"
   }
  ],
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
   "regions": [
    {
     "components": [
      {
       "derived": true,
       "impliedBy": "assignRentalEquipment",
       "kind": "primaryButton",
       "label": "Assign rental equipment",
       "notes": "The act the screen exists for."
      },
      {
       "derived": true,
       "impliedBy": "assignRentalEquipment",
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
  "apis": [
   {
    "contract": "rental",
    "invalidates": [
     "getRentalBooking"
    ],
    "operationId": "assignRentalEquipment",
    "provenance": "board reading, 19 September 2026",
    "purpose": "Several items at once",
    "trigger": "onAction"
   }
  ],
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
  "apis": [
   {
    "contract": "rental",
    "invalidates": [
     "getRentalBooking",
     "listRentalBookings",
     "getRentalAvailability"
    ],
    "operationId": "checkOutRental",
    "provenance": "board reading, 19 September 2026",
    "purpose": "Activate the rental",
    "trigger": "onAction"
   }
  ],
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
 }
]
```

## `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
 "assignRentalEquipment": {
  "method": "POST",
  "path": "/rental-bookings/{bookingId}/equipment",
  "contract": "rental",
  "summary": "Bind specific assets to the booking, by scan where required",
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
  "requestBody": null,
  "responds": "RentalEquipmentAssignment"
 },
 "checkOutRental": {
  "method": "POST",
  "path": "/rental-bookings/{bookingId}/check-out",
  "contract": "rental",
  "summary": "Hand it over, with the deposit held and the condition recorded",
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
  "requestBody": "RentalCheckOut",
  "responds": "RentalBooking"
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
 "lookupAsset": {
  "method": "GET",
  "path": "/assets/lookup",
  "contract": "maintenance",
  "summary": "Find an asset by tag or QR",
  "permission": "ASSET_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "assetTag",
    "in": "query",
    "required": null
   },
   {
    "name": "serialNumber",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "AssetDetail"
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
 "AssetDetail": {
  "x-ticvai-persistence": "maintenance.asset",
  "allOf": [
   {
    "$ref": "#/components/schemas/Asset"
   },
   {
    "type": "object",
    "properties": {
     "openWorkOrders": {
      "type": "array",
      "items": {
       "$ref": "#/components/schemas/WorkOrder"
      }
     },
     "maintenancePlans": {
      "type": "array",
      "items": {
       "$ref": "#/components/schemas/MaintenancePlan"
      }
     },
     "documents": {
      "type": "array",
      "description": "Manuals, procedures, certificates. What a technician needs on site. Read from `maintenance.asset_document`.\n",
      "items": {
       "$ref": "#/components/schemas/AssetDocument"
      }
     }
    }
   }
  ]
 },
 "AssetDocument": {
  "x-ticvai-persistence": "maintenance.asset_document",
  "type": "object",
  "description": "A document attached to an asset — manual, procedure, certificate — with the name and kind a technician needs on site. **One row per document**, because `AssetDetail.documents` returns a name and a kind for each and a `text[]` of refs has nowhere to hold either.\n",
  "required": [
   "id",
   "assetId",
   "ref"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "assetId": {
    "type": "string",
    "format": "uuid"
   },
   "ref": {
    "type": "string",
    "description": "The document in the media store."
   },
   "name": {
    "type": "string",
    "maxLength": 200,
    "nullable": true
   },
   "kind": {
    "allOf": [
     {
      "$ref": "#/components/schemas/AssetDocumentKind"
     }
    ],
    "nullable": true,
    "description": "Null where the document arrived as a bare ref in `documentRefs`."
   }
  }
 },
 "MaintenancePlan": {
  "x-ticvai-persistence": "maintenance.preventive_plan",
  "type": "object",
  "required": [
   "id",
   "name",
   "assetId",
   "taskTemplate"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "assetId": {
    "type": "string",
    "format": "uuid"
   },
   "assetCategoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Applies to every asset in the category rather than one."
   },
   "intervalDays": {
    "type": "integer",
    "nullable": true,
    "description": "Elapsed-time trigger."
   },
   "usageInterval": {
    "type": "number",
    "nullable": true,
    "description": "Usage trigger — cycles, hours, kilometres. **Whichever comes first** when both are set. A ride serviced every three months or ten thousand cycles is one plan.\n"
   },
   "leadTimeDays": {
    "type": "integer",
    "default": 7,
    "description": "How far ahead the work order is generated, so parts can be ordered before the job is already late.\n"
   },
   "taskTemplate": {
    "type": "object",
    "required": [
     "title",
     "priority"
    ],
    "properties": {
     "title": {
      "type": "string"
     },
     "description": {
      "type": "string"
     },
     "priority": {
      "$ref": "#/components/schemas/WorkOrderPriority"
     },
     "estimatedMinutes": {
      "type": "integer"
     },
     "inspectionTemplateId": {
      "type": "string",
      "format": "uuid"
     },
     "requiredPartIds": {
      "type": "array",
      "items": {
       "type": "string",
       "format": "uuid"
      }
     }
    }
   },
   "lastCompletedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "nextDueAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "isActive": {
    "type": "boolean"
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
 "RentalCheckOut": {
  "type": "object",
  "description": "Board 6. **The readiness gate is enforced server-side.**",
  "properties": {
   "depositAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "depositInstrument": {
    "type": "string",
    "nullable": true
   },
   "conditionNote": {
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
   "safetyBriefingGiven": {
    "type": "boolean",
    "default": false
   },
   "dueBackAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "overrideId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**A supervisor override for a failed precondition**, which is recorded rather than allowed silently.\n"
   }
  }
 },
 "RentalEquipmentAssignment": {
  "type": "object",
  "x-ticvai-persistence": "rental.equipment_assignment",
  "description": "Board 6.4. **The moment a serialised rental stops being a quantity.**",
  "required": [
   "assetId"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "assetId": {
    "type": "string",
    "format": "uuid",
    "description": "A `maintenance.Asset`, which is also a `resources` resource where the product is schedule-controlled."
   },
   "serialNumber": {
    "type": "string",
    "nullable": true
   },
   "scannedCode": {
    "type": "string",
    "nullable": true
   },
   "assignedManually": {
    "type": "boolean",
    "default": false
   },
   "assignedAt": {
    "type": "string",
    "format": "date-time"
   },
   "returnedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
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
 "WorkOrder": {
  "x-ticvai-persistence": "maintenance.work_order",
  "x-ticvai-retired-columns": [
   "is_overdue"
  ],
  "type": "object",
  "required": [
   "id",
   "workOrderNumber",
   "title",
   "venueId",
   "status",
   "priority",
   "kind",
   "createdAt"
  ],
  "properties": {
   "downtimeMinutes": {
    "type": "integer",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "**Measured from out-of-service to back-in-service, not from work start to work end.** A ride down for six hours of which two were spent working is down six hours, and the gap between the two numbers is the thing worth managing.\n**Maintained on write**: set when the asset returns to service, as the minutes from the `maintenance.asset_status_change` row that took it out carrying this work order's id to the asset's next change back to `inService`. Null while the asset is still out, and for a work order that never took it out.\n"
   },
   "rootCause": {
    "type": "string",
    "nullable": true,
    "enum": [
     "wearAndTear",
     "operatorError",
     "guestDamage",
     "manufacturingDefect",
     "environmental",
     "softwareFault",
     "powerFailure",
     "deferredMaintenance",
     "unknown"
    ],
    "description": "**Structured, because free text cannot be counted.** *Deferred maintenance* is the value a venue least wants to see and most needs to — a fault caused by work that was postponed is an argument for a budget.\n"
   },
   "rootCauseNote": {
    "type": "string",
    "nullable": true
   },
   "escalatedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "escalationLevel": {
    "type": "integer",
    "default": 0,
    "description": "**Escalation is a clock, not a decision.** A work order on a ride nobody has accepted after twenty minutes escalates itself, because the alternative is somebody noticing.\n"
   },
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "workOrderNumber": {
    "type": "string",
    "readOnly": true,
    "description": "**Server-assigned: the venue prefix plus a sequence per venue** (decided 28 September, audit R152). Not gapless; only tax invoices are gapless, per legal entity.\n"
   },
   "title": {
    "type": "string"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "assetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "assetName": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "The asset's name, copied when the work order is raised or its asset changes, and not updated when the asset is later renamed — the record reads as it was raised.\n"
   },
   "status": {
    "$ref": "#/components/schemas/WorkOrderStatus"
   },
   "priority": {
    "$ref": "#/components/schemas/WorkOrderPriority"
   },
   "priorityScore": {
    "type": "integer",
    "minimum": 0,
    "maximum": 100,
    "nullable": true,
    "readOnly": true,
    "description": "The score the venue's policy gave the fault when raised; null when a person or the asset set the priority (M17-01)."
   },
   "prioritySource": {
    "type": "string",
    "enum": [
     "scored",
     "assetOverride",
     "manual"
    ],
    "readOnly": true,
    "description": "Where `priority` came from (M17-01). A change through `updateWorkOrder` makes it `manual`."
   },
   "faultAssessment": {
    "$ref": "#/components/schemas/WorkOrderFaultAssessment"
   },
   "requiredQualificationCodes": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Skills the job needs (M17-13)."
   },
   "kind": {
    "$ref": "#/components/schemas/WorkOrderKind"
   },
   "assignedToPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "raisedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "categoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "As raised in `CreateWorkOrderRequest.categoryId`, amendable by `updateWorkOrder`. The category is what `completeWorkOrder` reads to decide whether completion photographs are required.\n"
   },
   "locationDescription": {
    "type": "string",
    "maxLength": 500,
    "nullable": true,
    "description": "Where the fault is, as raised. Needed where there is no asset — a broken tile, a leak in a corridor.\n"
   },
   "elapsedMinutes": {
    "type": "integer",
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "Labour minutes accumulated up to the last pause or stop. **Maintained on write** by `recordWorkOrderTime`, `pauseWorkOrder` and `completeWorkOrder`; while `isTimerRunning` is true the interval since the last start is not yet included.\n"
   },
   "isTimerRunning": {
    "type": "boolean",
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "Maintained on write by `startWorkOrder`, `resumeWorkOrder`, `recordWorkOrderTime`, `pauseWorkOrder` and `completeWorkOrder`.\n"
   },
   "dueAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "isOverdue": {
    "type": "boolean",
    "readOnly": true,
    "x-ticvai-persisted": false,
    "x-ticvai-derived": "onRead",
    "description": "`dueAt` is in the past and the status is still `open`, `assigned`, `inProgress`, `paused` or `awaitingParts`. **Computed on read and not stored** — it depends on the clock. `listWorkOrders?overdueOnly` applies the same test to `due_at`.\n"
   },
   "requiresVerification": {
    "type": "boolean"
   },
   "sourcePlanId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "sourceInspectionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "sourceIncidentId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   },
   "completedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "syncedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 }
}
```
