# WS95 — Rental Management board 8

**10 screens · 6 operations · 10 schemas · 3 permissions**

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
  `ASSET_MANAGE, RENTAL_OPERATE, RENTAL_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-564` | Rental Return Command Center | commandCentre | 1 | 0 | — |
| `BO-565` | Return Scan & Rental Retrieval | listDetail | 1 | 0 | — |
| `BO-566` | Return Summary & Actual Return Time | listDetail | 1 | 0 | — |
| `BO-567` | Post-Rental Condition Inspection | listDetail | 1 | 0 | — |
| `BO-568` | Before vs After Condition Comparison | listDetail | 1 | 0 | — |
| `BO-569` | Damage Assessment & Charge Workflow | listDetail | 1 | 0 | — |
| `BO-570` | Partial Return & Missing Equipment | listDetail | 1 | 0 | — |
| `BO-571` | Late Fees, Damage Fees & Final Settlement | listDetail | 1 | 0 | — |
| `BO-572` | Deposit Release, Capture & Customer Confirmation | listDetail | 1 | 0 | — |
| `BO-573` | Return Completion & Equipment Disposition | listDetail | 2 | 0 | — |

## Thin screens in this batch

**BO-565, BO-566, BO-567, BO-568, BO-569, BO-570, BO-571, BO-572, BO-573 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-564",
  "name": "Rental Return Command Center",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "8",
   "number": "1",
   "page": 92
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/rental-return-command-center-bo-564",
   "component": "apps/venue-management-web/src/routes/rentals/RentalReturnCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-565",
    "BO-566",
    "BO-567",
    "BO-568",
    "BO-569",
    "BO-570",
    "BO-571",
    "BO-572",
    "BO-573"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 8 wiring, 11 September 2026",
     "back": true
    },
    {
     "to": "BO-565",
     "trigger": "Return Scan & Rental Retrieval",
     "provenance": "structural — pack board 8 wiring, 11 September 2026"
    },
    {
     "to": "BO-566",
     "trigger": "Return Summary & Actual Return Time",
     "provenance": "structural — pack board 8 wiring, 11 September 2026"
    },
    {
     "to": "BO-567",
     "trigger": "Post-Rental Condition Inspection",
     "provenance": "structural — pack board 8 wiring, 11 September 2026"
    },
    {
     "to": "BO-568",
     "trigger": "Before vs After Condition Comparison",
     "provenance": "structural — pack board 8 wiring, 11 September 2026"
    },
    {
     "to": "BO-569",
     "trigger": "Damage Assessment & Charge Workflow",
     "provenance": "structural — pack board 8 wiring, 11 September 2026"
    },
    {
     "to": "BO-570",
     "trigger": "Partial Return & Missing Equipment",
     "provenance": "structural — pack board 8 wiring, 11 September 2026"
    },
    {
     "to": "BO-571",
     "trigger": "Late Fees, Damage Fees & Final Settlement",
     "provenance": "structural — pack board 8 wiring, 11 September 2026"
    },
    {
     "to": "BO-572",
     "trigger": "Deposit Release, Capture & Customer Confirmation",
     "provenance": "structural — pack board 8 wiring, 11 September 2026"
    },
    {
     "to": "BO-573",
     "trigger": "Return Completion & Equipment Disposition",
     "provenance": "structural — pack board 8 wiring, 11 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide operators with a live operational view of all expected, in-progress, partial, overdue and completed returns.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search rental return",
       "provenance": "pack Rental_Management.pdf, page 92 §Filters"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
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
       "notes": "The pack filters this screen by venue, return location, product, expected return, rental status, damage status and 2 more — which are present is a decision the pack already made.",
       "provenance": "pack Rental_Management.pdf, page 92 §Filters"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
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
     ]
    }
   ]
  },
  "states": {
   "loading": "The rental return list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the rental return untouched.",
   "emptyFirstRun": "No rental return yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the rental return are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listRentalBookings",
    "contract": "rental",
    "purpose": "Expected back",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
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
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-564",
   "workshopBoard": "wireframes/WS123 Rental Management Board 8.dc.html#bo-564"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 92. 0 of 8 labels bound to a contract property; 18 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-565",
  "name": "Return Scan & Rental Retrieval",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "8",
   "number": "2",
   "page": 93
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/return-scan-rental-retrieval-bo-565",
   "component": "apps/venue-management-web/src/routes/rentals/ReturnScanRentalRetrieval.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-564"
   ],
   "exitTo": [
    "BO-564"
   ],
   "transitions": [
    {
     "to": "BO-564",
     "trigger": "Back to Rental Return Command Center",
     "provenance": "structural — pack board 8 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Quickly identify which active rental the returned equipment belongs to. The original requirements specifically require scanning the rented item and retrieving its reservation.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 93"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 93"
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
       "impliedBy": "getRentalBooking",
       "notes": "One record, read-only."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The return scan rental list.",
   "error": "Could not load. Names which read failed and leaves the return scan rental untouched.",
   "emptyFirstRun": "No return scan rental yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the return scan rental are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getRentalBooking",
    "contract": "rental",
    "purpose": "Retrieve by scan",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-565",
   "workshopBoard": "wireframes/WS123 Rental Management Board 8.dc.html#bo-565"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 93. 0 of 0 labels bound to a contract property; 0 of 13 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "bookingId",
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
  "id": "BO-566",
  "name": "Return Summary & Actual Return Time",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "8",
   "number": "3",
   "page": 94
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/return-summary-actual-return-time-bo-566",
   "component": "apps/venue-management-web/src/routes/rentals/ReturnSummaryActualReturnTime.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-564"
   ],
   "exitTo": [
    "BO-564"
   ],
   "transitions": [
    {
     "to": "BO-564",
     "trigger": "Back to Rental Return Command Center",
     "provenance": "structural — pack board 8 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Establish the operational return event before inspection and financial settlement.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 94"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 94"
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
       "impliedBy": "returnRental",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "returnRental"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The return summary actual list.",
   "error": "Could not load. Names which read failed and leaves the return summary actual untouched.",
   "emptyFirstRun": "No return summary actual yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the return summary actual are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "returnRental",
    "contract": "rental",
    "purpose": "Record the actual return time",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getRentalBooking",
     "listRentalBookings",
     "getRentalAvailability",
     "listOverdueRentals"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-566",
   "workshopBoard": "wireframes/WS123 Rental Management Board 8.dc.html#bo-566"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 94. 0 of 0 labels bound to a contract property; 0 of 15 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "bookingId",
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
  "id": "BO-567",
  "name": "Post-Rental Condition Inspection",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "8",
   "number": "4",
   "page": 95
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/post-rental-condition-inspection-bo-567",
   "component": "apps/venue-management-web/src/routes/rentals/PostRentalConditionInspection.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-564"
   ],
   "exitTo": [
    "BO-564"
   ],
   "transitions": [
    {
     "to": "BO-564",
     "trigger": "Back to Rental Return Command Center",
     "provenance": "structural — pack board 8 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Perform a structured inspection of returned equipment.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 95"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 95"
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
       "impliedBy": "recordRentalInspection",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "recordRentalInspection"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The post-rental condition inspection list.",
   "error": "Could not load. Names which read failed and leaves the post-rental condition inspection untouched.",
   "emptyFirstRun": "No post-rental condition inspection yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the post-rental condition inspection are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "recordRentalInspection",
    "contract": "rental",
    "purpose": "Condition on the way back",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getRentalBooking"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-567",
   "workshopBoard": "wireframes/WS123 Rental Management Board 8.dc.html#bo-567"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 95. 0 of 0 labels bound to a contract property; 0 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "bookingId",
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
  "id": "BO-568",
  "name": "Before vs After Condition Comparison",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "8",
   "number": "5",
   "page": 96
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/before-vs-after-condition-comparison-bo-568",
   "component": "apps/venue-management-web/src/routes/rentals/BeforeVsAfterConditionComparison.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-564"
   ],
   "exitTo": [
    "BO-564"
   ],
   "transitions": [
    {
     "to": "BO-564",
     "trigger": "Back to Rental Return Command Center",
     "provenance": "structural — pack board 8 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Use the evidence captured during Board 6 checkout to establish whether damage existed before the rental or occurred during it. This is one of the important capabilities I recommended adding.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 96"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 96"
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
       "impliedBy": "recordRentalInspection",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "recordRentalInspection"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The before after condition list.",
   "error": "Could not load. Names which read failed and leaves the before after condition untouched.",
   "emptyFirstRun": "No before after condition yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the before after condition are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "recordRentalInspection",
    "contract": "rental",
    "purpose": "Before against after",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getRentalBooking"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-568",
   "workshopBoard": "wireframes/WS123 Rental Management Board 8.dc.html#bo-568"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 96. 0 of 0 labels bound to a contract property; 0 of 13 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "bookingId",
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
  "id": "BO-569",
  "name": "Damage Assessment & Charge Workflow",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "8",
   "number": "6",
   "page": 97
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/damage-assessment-charge-workflow-bo-569",
   "component": "apps/venue-management-web/src/routes/rentals/DamageAssessmentChargeWorkflow.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-564"
   ],
   "exitTo": [
    "BO-564"
   ],
   "transitions": [
    {
     "to": "BO-564",
     "trigger": "Back to Rental Return Command Center",
     "provenance": "structural — pack board 8 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Convert confirmed equipment damage into a controlled operational and commercial case. The source specifically recommends a formal damage assessment workflow.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 97"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 97"
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
       "impliedBy": "assessRentalDamage",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "assessRentalDamage"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The damage assessment charge list.",
   "error": "Could not load. Names which read failed and leaves the damage assessment charge untouched.",
   "emptyFirstRun": "No damage assessment charge yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the damage assessment charge are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "assessRentalDamage",
    "contract": "rental",
    "purpose": "Price the damage",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getRentalBooking"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-569",
   "workshopBoard": "wireframes/WS123 Rental Management Board 8.dc.html#bo-569"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 97. 0 of 0 labels bound to a contract property; 0 of 19 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "bookingId",
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
  "id": "BO-570",
  "name": "Partial Return & Missing Equipment",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "8",
   "number": "7",
   "page": 98
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/partial-return-missing-equipment-bo-570",
   "component": "apps/venue-management-web/src/routes/rentals/PartialReturnMissingEquipment.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-564"
   ],
   "exitTo": [
    "BO-564"
   ],
   "transitions": [
    {
     "to": "BO-564",
     "trigger": "Back to Rental Return Command Center",
     "provenance": "structural — pack board 8 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Handle multi-item and group rentals where equipment is returned at different times. This implements the partial-return capability we added in Board 7.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 98"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 98"
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
       "impliedBy": "returnRental",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "returnRental"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The partial return missing list.",
   "error": "Could not load. Names which read failed and leaves the partial return missing untouched.",
   "emptyFirstRun": "No partial return missing yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the partial return missing are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "returnRental",
    "contract": "rental",
    "purpose": "Partial return, with what is missing",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getRentalBooking",
     "listRentalBookings",
     "getRentalAvailability",
     "listOverdueRentals"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-570",
   "workshopBoard": "wireframes/WS123 Rental Management Board 8.dc.html#bo-570"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 98. 0 of 0 labels bound to a contract property; 0 of 13 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "bookingId",
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
  "id": "BO-571",
  "name": "Late Fees, Damage Fees & Final Settlement",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "8",
   "number": "8",
   "page": 99
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/late-fees-damage-fees-final-settlement-bo-571",
   "component": "apps/venue-management-web/src/routes/rentals/LateFeesDamageFeesFinalSettlement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-564"
   ],
   "exitTo": [
    "BO-564"
   ],
   "transitions": [
    {
     "to": "BO-564",
     "trigger": "Back to Rental Return Command Center",
     "provenance": "structural — pack board 8 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Calculate the customer's final rental financial position. Board 8 should consume, not recreate, the commercial policies configured in Board 4.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 99"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 99"
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
       "impliedBy": "returnRental",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "returnRental"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The late fees damage list.",
   "error": "Could not load. Names which read failed and leaves the late fees damage untouched.",
   "emptyFirstRun": "No late fees damage yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the late fees damage are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "returnRental",
    "contract": "rental",
    "purpose": "Late fee, damage and settlement",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getRentalBooking",
     "listRentalBookings",
     "getRentalAvailability",
     "listOverdueRentals"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-571",
   "workshopBoard": "wireframes/WS123 Rental Management Board 8.dc.html#bo-571"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 99. 0 of 0 labels bound to a contract property; 0 of 3 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "bookingId",
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
  "id": "BO-572",
  "name": "Deposit Release, Capture & Customer Confirmation",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "8",
   "number": "9",
   "page": 100
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/deposit-release-capture-customer-confirmation-bo-572",
   "component": "apps/venue-management-web/src/routes/rentals/DepositReleaseCaptureCustomerConfirmation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-564"
   ],
   "exitTo": [
    "BO-564"
   ],
   "transitions": [
    {
     "to": "BO-564",
     "trigger": "Back to Rental Return Command Center",
     "provenance": "structural — pack board 8 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Complete the deposit lifecycle and provide the customer with a transparent final statement. The source requires full refund/release, partial refund and deposit forfeiture, together with transaction history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 100"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 100"
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
       "impliedBy": "returnRental",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "returnRental"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The deposit release capture list.",
   "error": "Could not load. Names which read failed and leaves the deposit release capture untouched.",
   "emptyFirstRun": "No deposit release capture yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the deposit release capture are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "returnRental",
    "contract": "rental",
    "purpose": "Capture or release the deposit",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getRentalBooking",
     "listRentalBookings",
     "getRentalAvailability",
     "listOverdueRentals"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-572",
   "workshopBoard": "wireframes/WS123 Rental Management Board 8.dc.html#bo-572"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 100. 0 of 0 labels bound to a contract property; 0 of 4 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "bookingId",
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
  "id": "BO-573",
  "name": "Return Completion & Equipment Disposition",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "8",
   "number": "10",
   "page": 101
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/return-completion-equipment-disposition-bo-573",
   "component": "apps/venue-management-web/src/routes/rentals/ReturnCompletionEquipmentDisposition.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-564"
   ],
   "exitTo": [
    "BO-564"
   ],
   "transitions": [
    {
     "to": "BO-564",
     "trigger": "Back to Rental Return Command Center",
     "provenance": "structural — pack board 8 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Complete the rental while determining exactly what happens to every returned physical asset. This is extremely important because returning an item does not necessarily mean it becomes immediately available again.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 101"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 101"
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
       "impliedBy": "returnRental",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "returnRental"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The return completion equipment list.",
   "error": "Could not load. Names which read failed and leaves the return completion equipment untouched.",
   "emptyFirstRun": "No return completion equipment yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the return completion equipment are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "returnRental",
    "contract": "rental",
    "purpose": "Complete, and dispose of the equipment",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getRentalBooking",
     "listRentalBookings",
     "getRentalAvailability",
     "listOverdueRentals"
    ]
   },
   {
    "operationId": "setAssetStatus",
    "contract": "maintenance",
    "purpose": "Back into the pool, or not",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getAsset",
     "listAssets"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-573",
   "workshopBoard": "wireframes/WS123 Rental Management Board 8.dc.html#bo-573"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 101. 0 of 0 labels bound to a contract property; 0 of 118 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "assetId",
     "from": "navigation"
    },
    {
     "name": "bookingId",
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
