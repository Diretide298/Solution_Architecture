# WS93 — Rental Management board 6

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
| `BO-544` | Rental Checkout Command Center | commandCentre | 0 | 0 | — |
| `BO-545` | Voucher Scan & Reservation Retrieval | listDetail | 0 | 0 | — |
| `BO-546` | Checkout Readiness Validation | listDetail | 0 | 0 | — |
| `BO-547` | Equipment Assignment Workspace | listDetail | 0 | 0 | — |
| `BO-548` | Equipment Scan & Validation | listDetail | 0 | 0 | — |
| `BO-549` | Pre-Rental Condition Inspection | listDetail | 0 | 0 | — |
| `BO-550` | Safety & Handover Checklist | listDetail | 0 | 0 | — |
| `BO-551` | Deposit & Financial Handover Validation | listDetail | 0 | 0 | — |
| `BO-552` | Group & Multi-Item Checkout | listDetail | 0 | 0 | — |
| `BO-553` | Checkout Confirmation & Rental Activation | configEditor | 0 | 0 | — |

## Thin screens in this batch

**BO-545, BO-546, BO-547, BO-548, BO-549, BO-550, BO-551, BO-552, BO-553 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-544",
  "name": "Rental Checkout Command Center",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "6",
   "number": "1",
   "page": 64
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/rental-checkout-command-center-bo-544",
   "component": "apps/venue-management-web/src/routes/rentals/RentalCheckoutCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-545",
    "BO-546",
    "BO-547",
    "BO-548",
    "BO-549",
    "BO-550",
    "BO-551",
    "BO-552",
    "BO-553"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 6 wiring, 11 September 2026",
     "back": true
    },
    {
     "to": "BO-545",
     "trigger": "Voucher Scan & Reservation Retrieval",
     "provenance": "structural — pack board 6 wiring, 11 September 2026"
    },
    {
     "to": "BO-546",
     "trigger": "Checkout Readiness Validation",
     "provenance": "structural — pack board 6 wiring, 11 September 2026"
    },
    {
     "to": "BO-547",
     "trigger": "Equipment Assignment Workspace",
     "provenance": "structural — pack board 6 wiring, 11 September 2026"
    },
    {
     "to": "BO-548",
     "trigger": "Equipment Scan & Validation",
     "provenance": "structural — pack board 6 wiring, 11 September 2026"
    },
    {
     "to": "BO-549",
     "trigger": "Pre-Rental Condition Inspection",
     "provenance": "structural — pack board 6 wiring, 11 September 2026"
    },
    {
     "to": "BO-550",
     "trigger": "Safety & Handover Checklist",
     "provenance": "structural — pack board 6 wiring, 11 September 2026"
    },
    {
     "to": "BO-551",
     "trigger": "Deposit & Financial Handover Validation",
     "provenance": "structural — pack board 6 wiring, 11 September 2026"
    },
    {
     "to": "BO-552",
     "trigger": "Group & Multi-Item Checkout",
     "provenance": "structural — pack board 6 wiring, 11 September 2026"
    },
    {
     "to": "BO-553",
     "trigger": "Checkout Confirmation & Rental Activation",
     "provenance": "structural — pack board 6 wiring, 11 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide rental operators with a real-time operational queue of customers requiring equipment checkout.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search rental checkout",
       "provenance": "pack Rental_Management.pdf, page 64 §Filters"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Location",
        "Product",
        "Start Time",
        "Booking Type",
        "Group/Individual",
        "Readiness",
        "Status"
       ],
       "notes": "The pack filters this screen by location, product, start time, booking type, group/individual, readiness and 1 more — which are present is a decision the pack already made.",
       "provenance": "pack Rental_Management.pdf, page 64 §Filters"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
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
     ]
    }
   ]
  },
  "states": {
   "loading": "The rental checkout list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the rental checkout untouched.",
   "emptyFirstRun": "No rental checkout yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the rental checkout are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
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
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-544"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 64. 0 of 7 labels bound to a contract property; 15 of 23 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-545",
  "name": "Voucher Scan & Reservation Retrieval",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "6",
   "number": "2",
   "page": 65
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/voucher-scan-reservation-retrieval-bo-545",
   "component": "apps/venue-management-web/src/routes/rentals/VoucherScanReservationRetrieval.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-544"
   ],
   "exitTo": [
    "BO-544"
   ],
   "transitions": [
    {
     "to": "BO-544",
     "trigger": "Back to Rental Checkout Command Center",
     "provenance": "structural — pack board 6 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Quickly identify the customer reservation when they arrive. The original requirement specifically requires scanning and validating the customer's voucher/ticket.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 65"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 65"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The voucher scan reservation list.",
   "error": "Could not load. Names which read failed and leaves the voucher scan reservation untouched.",
   "emptyFirstRun": "No voucher scan reservation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the voucher scan reservation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-545"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 65. 0 of 0 labels bound to a contract property; 0 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-546",
  "name": "Checkout Readiness Validation",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "6",
   "number": "3",
   "page": 66
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/checkout-readiness-validation-bo-546",
   "component": "apps/venue-management-web/src/routes/rentals/CheckoutReadinessValidation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-544"
   ],
   "exitTo": [
    "BO-544"
   ],
   "transitions": [
    {
     "to": "BO-544",
     "trigger": "Back to Rental Checkout Command Center",
     "provenance": "structural — pack board 6 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Prevent equipment from being handed over until mandatory requirements are satisfied.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 66"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 66"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The checkout readiness validation list.",
   "error": "Could not load. Names which read failed and leaves the checkout readiness validation untouched.",
   "emptyFirstRun": "No checkout readiness validation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the checkout readiness validation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-546"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 66. 0 of 0 labels bound to a contract property; 0 of 19 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-547",
  "name": "Equipment Assignment Workspace",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "6",
   "number": "4",
   "page": 67
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/equipment-assignment-workspace-bo-547",
   "component": "apps/venue-management-web/src/routes/rentals/EquipmentAssignmentWorkspace.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-544"
   ],
   "exitTo": [
    "BO-544"
   ],
   "transitions": [
    {
     "to": "BO-544",
     "trigger": "Back to Rental Checkout Command Center",
     "provenance": "structural — pack board 6 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Assign the actual physical equipment to the reservation.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 67"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 67"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The equipment list.",
   "error": "Could not load. Names which read failed and leaves the equipment untouched.",
   "emptyFirstRun": "No equipment yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the equipment are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-547"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 67. 0 of 0 labels bound to a contract property; 0 of 18 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-548",
  "name": "Equipment Scan & Validation",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "6",
   "number": "5",
   "page": 68
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/equipment-scan-validation-bo-548",
   "component": "apps/venue-management-web/src/routes/rentals/EquipmentScanValidation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-544"
   ],
   "exitTo": [
    "BO-544"
   ],
   "transitions": [
    {
     "to": "BO-544",
     "trigger": "Back to Rental Checkout Command Center",
     "provenance": "structural — pack board 6 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Ensure the operator cannot accidentally assign the wrong, unavailable or unsafe equipment.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 68"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 68"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The equipment scan validation list.",
   "error": "Could not load. Names which read failed and leaves the equipment scan validation untouched.",
   "emptyFirstRun": "No equipment scan validation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the equipment scan validation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-548"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 68. 0 of 0 labels bound to a contract property; 0 of 17 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-549",
  "name": "Pre-Rental Condition Inspection",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "6",
   "number": "6",
   "page": 69
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/pre-rental-condition-inspection-bo-549",
   "component": "apps/venue-management-web/src/routes/rentals/PreRentalConditionInspection.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-544"
   ],
   "exitTo": [
    "BO-544"
   ],
   "transitions": [
    {
     "to": "BO-544",
     "trigger": "Back to Rental Checkout Command Center",
     "provenance": "structural — pack board 6 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Document the equipment condition before handover. Photo capture at checkout is specifically recommended in the source.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 2 actions on this screen and the screen declares 0 operations.** Unserved: Asset, Checkout inspection. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Rental_Management.pdf, page 69 §Support"
   },
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
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "actionBar",
     "slot": "rowActions",
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
     ]
    }
   ]
  },
  "states": {
   "loading": "The pre-rental condition inspection list.",
   "error": "Could not load. Names which read failed and leaves the pre-rental condition inspection untouched.",
   "emptyFirstRun": "No pre-rental condition inspection yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the pre-rental condition inspection are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-549"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 69. 0 of 0 labels bound to a contract property; 2 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-550",
  "name": "Safety & Handover Checklist",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "6",
   "number": "7",
   "page": 70
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/safety-handover-checklist-bo-550",
   "component": "apps/venue-management-web/src/routes/rentals/SafetyHandoverChecklist.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-544"
   ],
   "exitTo": [
    "BO-544"
   ],
   "transitions": [
    {
     "to": "BO-544",
     "trigger": "Back to Rental Checkout Command Center",
     "provenance": "structural — pack board 6 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Ensure mandatory operational and safety steps are completed before starting the rental. Example — Kayak ✓ Life jacket provided ✓ Paddle provided ✓ Safety briefing completed ✓ Emergency procedure explained ✓ Restricted areas explained ✓ Customer confirms swimming ability Example — Bicycle ✓ Helmet provided ✓ Brake check completed ✓ Seat adjusted ✓ Safety briefing completed The checklist should be configurable by rental product/category from Board 1.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 70"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 70"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The safety handover checklist list.",
   "error": "Could not load. Names which read failed and leaves the safety handover checklist untouched.",
   "emptyFirstRun": "No safety handover checklist yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the safety handover checklist are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-550"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 70. 0 of 0 labels bound to a contract property; 0 of 17 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-551",
  "name": "Deposit & Financial Handover Validation",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "6",
   "number": "8",
   "page": 70
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/deposit-financial-handover-validation-bo-551",
   "component": "apps/venue-management-web/src/routes/rentals/DepositFinancialHandoverValidation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-544"
   ],
   "exitTo": [
    "BO-544"
   ],
   "transitions": [
    {
     "to": "BO-544",
     "trigger": "Back to Rental Checkout Command Center",
     "provenance": "structural — pack board 6 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Give the rental operator a clear commercial status without requiring them to enter the Finance module.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 70"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 70"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The deposit financial handover list.",
   "error": "Could not load. Names which read failed and leaves the deposit financial handover untouched.",
   "emptyFirstRun": "No deposit financial handover yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the deposit financial handover are still there. The pack's own statuses are ✓ AUTHORIZED — the state names which is selected.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-551"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 70. 0 of 0 labels bound to a contract property; 1 of 13 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-552",
  "name": "Group & Multi-Item Checkout",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "6",
   "number": "9",
   "page": 71
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/group-multi-item-checkout-bo-552",
   "component": "apps/venue-management-web/src/routes/rentals/GroupMultiItemCheckout.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-544"
   ],
   "exitTo": [
    "BO-544"
   ],
   "transitions": [
    {
     "to": "BO-544",
     "trigger": "Back to Rental Checkout Command Center",
     "provenance": "structural — pack board 6 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide an efficient checkout workflow for group rentals and reservations containing multiple equipment units. This is particularly important because the original requirements support group reservations.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 71"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 71"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The group multi-item checkout list.",
   "error": "Could not load. Names which read failed and leaves the group multi-item checkout untouched.",
   "emptyFirstRun": "No group multi-item checkout yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the group multi-item checkout are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-552"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 71. 0 of 0 labels bound to a contract property; 0 of 18 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-553",
  "name": "Checkout Confirmation & Rental Activation",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "6",
   "number": "10",
   "page": 72
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/checkout-confirmation-rental-activation-bo-553",
   "component": "apps/venue-management-web/src/routes/rentals/CheckoutConfirmationRentalActivation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-544"
   ],
   "exitTo": [
    "BO-544"
   ],
   "transitions": [
    {
     "to": "BO-544",
     "trigger": "Back to Rental Checkout Command Center",
     "provenance": "structural — pack board 6 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Options; Select Equipment) and no display directory — it is settings, not a population",
  "purpose": "Officially start the rental and transition the reservation into an active rental.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
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
     ]
    }
   ]
  },
  "states": {
   "loading": "The checkout confirmation rental configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the checkout confirmation rental untouched.",
   "emptyFirstRun": "No checkout confirmation rental configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-553"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 72. 0 of 0 labels bound to a contract property; 2 of 96 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
