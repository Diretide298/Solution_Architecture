# WS94 — Rental Management board 7

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
| `BO-554` | Active Rental Operations Command Center | commandCentre | 0 | 0 | — |
| `BO-555` | Active Rental Detail & Live Timeline | listDetail | 0 | 0 | — |
| `BO-556` | Rental Extension Request | listDetail | 0 | 0 | — |
| `BO-557` | Extension Pricing & Confirmation | listDetail | 0 | 0 | — |
| `BO-558` | Equipment Swap / Replacement | listDetail | 0 | 0 | — |
| `BO-559` | Rental Incident & Operational Exception | listDetail | 0 | 0 | — |
| `BO-560` | Due Soon & Customer Notification Management | listDetail | 0 | 0 | — |
| `BO-561` | Overdue Rental Management | listDetail | 0 | 0 | — |
| `BO-562` | Active Group Rental Management | listDetail | 0 | 0 | — |
| `BO-563` | Active Rental Intelligence & Operational Alerts | listDetail | 0 | 0 | — |

## Thin screens in this batch

**BO-555, BO-556, BO-557, BO-558, BO-559, BO-560, BO-561, BO-562, BO-563 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-554",
  "name": "Active Rental Operations Command Center",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "7",
   "number": "1",
   "page": 78
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/active-rental-operations-command-center-bo-554",
   "component": "apps/venue-management-web/src/routes/rentals/ActiveRentalOperationsCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-555",
    "BO-556",
    "BO-557",
    "BO-558",
    "BO-559",
    "BO-560",
    "BO-561",
    "BO-562",
    "BO-563"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 7 wiring, 11 September 2026",
     "back": true
    },
    {
     "to": "BO-555",
     "trigger": "Active Rental Detail & Live Timeline",
     "provenance": "structural — pack board 7 wiring, 11 September 2026"
    },
    {
     "to": "BO-556",
     "trigger": "Rental Extension Request",
     "provenance": "structural — pack board 7 wiring, 11 September 2026"
    },
    {
     "to": "BO-557",
     "trigger": "Extension Pricing & Confirmation",
     "provenance": "structural — pack board 7 wiring, 11 September 2026"
    },
    {
     "to": "BO-558",
     "trigger": "Equipment Swap / Replacement",
     "provenance": "structural — pack board 7 wiring, 11 September 2026"
    },
    {
     "to": "BO-559",
     "trigger": "Rental Incident & Operational Exception",
     "provenance": "structural — pack board 7 wiring, 11 September 2026"
    },
    {
     "to": "BO-560",
     "trigger": "Due Soon & Customer Notification Management",
     "provenance": "structural — pack board 7 wiring, 11 September 2026"
    },
    {
     "to": "BO-561",
     "trigger": "Overdue Rental Management",
     "provenance": "structural — pack board 7 wiring, 11 September 2026"
    },
    {
     "to": "BO-562",
     "trigger": "Active Group Rental Management",
     "provenance": "structural — pack board 7 wiring, 11 September 2026"
    },
    {
     "to": "BO-563",
     "trigger": "Active Rental Intelligence & Operational Alerts",
     "provenance": "structural — pack board 7 wiring, 11 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide operators and supervisors with a real-time view of every rental currently in progress.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search active rental operations",
       "provenance": "pack Rental_Management.pdf, page 78 §Filters"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
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
       "notes": "The pack filters this screen by venue, location, product, customer, rental status, expected return and 2 more — which are present is a decision the pack already made.",
       "provenance": "pack Rental_Management.pdf, page 78 §Filters"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
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
     ]
    }
   ]
  },
  "states": {
   "loading": "The active rental operations list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the active rental operations untouched.",
   "emptyFirstRun": "No active rental operations yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the active rental operations are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
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
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-554"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 78. 0 of 8 labels bound to a contract property; 16 of 23 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-555",
  "name": "Active Rental Detail & Live Timeline",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "7",
   "number": "2",
   "page": 79
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/active-rental-detail-live-timeline-bo-555",
   "component": "apps/venue-management-web/src/routes/rentals/ActiveRentalDetailLiveTimeline.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-554"
   ],
   "exitTo": [
    "BO-554"
   ],
   "transitions": [
    {
     "to": "BO-554",
     "trigger": "Back to Active Rental Operations Command Center",
     "provenance": "structural — pack board 7 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide the complete operational view of one active rental.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 79"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 79"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The active rental detail list.",
   "error": "Could not load. Names which read failed and leaves the active rental detail untouched.",
   "emptyFirstRun": "No active rental detail yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the active rental detail are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-555"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 79. 0 of 0 labels bound to a contract property; 0 of 13 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-556",
  "name": "Rental Extension Request",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "7",
   "number": "3",
   "page": 81
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/rental-extension-request-bo-556",
   "component": "apps/venue-management-web/src/routes/rentals/RentalExtensionRequest.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-554"
   ],
   "exitTo": [
    "BO-554"
   ],
   "transitions": [
    {
     "to": "BO-554",
     "trigger": "Back to Active Rental Operations Command Center",
     "provenance": "structural — pack board 7 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow the customer or operator to request additional rental time. This is one of the important capabilities I recommend formally adding to the rental scope.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 81"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 81"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The rental extension request list.",
   "error": "Could not load. Names which read failed and leaves the rental extension request untouched.",
   "emptyFirstRun": "No rental extension request yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the rental extension request are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-556"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 81. 0 of 0 labels bound to a contract property; 0 of 23 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-557",
  "name": "Extension Pricing & Confirmation",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "7",
   "number": "4",
   "page": 82
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/extension-pricing-confirmation-bo-557",
   "component": "apps/venue-management-web/src/routes/rentals/ExtensionPricingConfirmation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-554"
   ],
   "exitTo": [
    "BO-554"
   ],
   "transitions": [
    {
     "to": "BO-554",
     "trigger": "Back to Active Rental Operations Command Center",
     "provenance": "structural — pack board 7 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Calculate the commercial impact of an approved extension. Once Board 3 confirms availability, Board 4 calculates the extension charge.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 82"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 82"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The extension pricing confirmation list.",
   "error": "Could not load. Names which read failed and leaves the extension pricing confirmation untouched.",
   "emptyFirstRun": "No extension pricing confirmation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the extension pricing confirmation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-557"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 82. 0 of 0 labels bound to a contract property; 0 of 15 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-558",
  "name": "Equipment Swap / Replacement",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "7",
   "number": "5",
   "page": 83
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/equipment-swap-replacement-bo-558",
   "component": "apps/venue-management-web/src/routes/rentals/EquipmentSwapReplacement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-554"
   ],
   "exitTo": [
    "BO-554"
   ],
   "transitions": [
    {
     "to": "BO-554",
     "trigger": "Back to Active Rental Operations Command Center",
     "provenance": "structural — pack board 7 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Replace equipment during an active rental without terminating and recreating the rental. This is another capability I strongly recommend adding.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 83"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 83"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The equipment swap replacement list.",
   "error": "Could not load. Names which read failed and leaves the equipment swap replacement untouched.",
   "emptyFirstRun": "No equipment swap replacement yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the equipment swap replacement are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-558"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 83. 0 of 0 labels bound to a contract property; 0 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-559",
  "name": "Rental Incident & Operational Exception",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "7",
   "number": "6",
   "page": 84
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/rental-incident-operational-exception-bo-559",
   "component": "apps/venue-management-web/src/routes/rentals/RentalIncidentOperationalException.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-554"
   ],
   "exitTo": [
    "BO-554"
   ],
   "transitions": [
    {
     "to": "BO-554",
     "trigger": "Back to Active Rental Operations Command Center",
     "provenance": "structural — pack board 7 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Capture incidents occurring while equipment is in customer possession.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 84"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 84"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The rental incident operational list.",
   "error": "Could not load. Names which read failed and leaves the rental incident operational untouched.",
   "emptyFirstRun": "No rental incident operational yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the rental incident operational are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-559"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 84. 0 of 0 labels bound to a contract property; 0 of 17 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-560",
  "name": "Due Soon & Customer Notification Management",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "7",
   "number": "7",
   "page": 85
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/due-soon-customer-notification-management-bo-560",
   "component": "apps/venue-management-web/src/routes/rentals/DueSoonCustomerNotificationManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-554"
   ],
   "exitTo": [
    "BO-554"
   ],
   "transitions": [
    {
     "to": "BO-554",
     "trigger": "Back to Active Rental Operations Command Center",
     "provenance": "structural — pack board 7 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Proactively communicate with customers before their rental becomes overdue. The original matrix requires overdue rental notifications.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 85"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 85"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The due soon customer list.",
   "error": "Could not load. Names which read failed and leaves the due soon customer untouched.",
   "emptyFirstRun": "No due soon customer yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the due soon customer are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-560"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 85. 0 of 0 labels bound to a contract property; 0 of 14 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-561",
  "name": "Overdue Rental Management",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "7",
   "number": "8",
   "page": 85
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/overdue-rental-management-bo-561",
   "component": "apps/venue-management-web/src/routes/rentals/OverdueRentalManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-554"
   ],
   "exitTo": [
    "BO-554"
   ],
   "transitions": [
    {
     "to": "BO-554",
     "trigger": "Back to Active Rental Operations Command Center",
     "provenance": "structural — pack board 7 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide operators with a dedicated workflow for rentals that have exceeded their expected return time. The original requirement calls for automatic late-fee calculation, configurable grace periods and overdue notifications.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 85"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 85"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The overdue rental list.",
   "error": "Could not load. Names which read failed and leaves the overdue rental untouched.",
   "emptyFirstRun": "No overdue rental yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the overdue rental are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-561"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 85. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-562",
  "name": "Active Group Rental Management",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "7",
   "number": "9",
   "page": 86
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/active-group-rental-management-bo-562",
   "component": "apps/venue-management-web/src/routes/rentals/ActiveGroupRentalManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-554"
   ],
   "exitTo": [
    "BO-554"
   ],
   "transitions": [
    {
     "to": "BO-554",
     "trigger": "Back to Active Rental Operations Command Center",
     "provenance": "structural — pack board 7 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Manage group rentals where multiple pieces of equipment may have different operational states.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 86"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 86"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The active group rental list.",
   "error": "Could not load. Names which read failed and leaves the active group rental untouched.",
   "emptyFirstRun": "No active group rental yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the active group rental are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-562"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 86. 0 of 0 labels bound to a contract property; 0 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-563",
  "name": "Active Rental Intelligence & Operational Alerts",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "7",
   "number": "10",
   "page": 87
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/active-rental-intelligence-operational-alerts-bo-563",
   "component": "apps/venue-management-web/src/routes/rentals/ActiveRentalIntelligenceOperationalAlerts.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-554"
   ],
   "exitTo": [
    "BO-554"
   ],
   "transitions": [
    {
     "to": "BO-554",
     "trigger": "Back to Active Rental Operations Command Center",
     "provenance": "structural — pack board 7 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Use AI and real-time operational data to identify risks before they become operational problems.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Rental_Management.pdf, page 87 §Display"
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
       "label": "Every active rental intelligence",
       "columns": [
        "Rentals due next hour",
        "Predicted late returns",
        "Future reservation conflicts",
        "Extension demand",
        "Equipment incident trends",
        "Location return pressure",
        "Expected inventory shortage"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Rental_Management.pdf, page 87 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected active rental intelligence",
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
       "notes": "The pack groups this record's detail under its own headings: “RNT-10482”, “Confirmed”, “Ready for Checkout”, “Active”, “Incident”, “Overdue”.",
       "provenance": "pack Rental_Management.pdf, page 87 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The active rental intelligence list.",
   "error": "Could not load. Names which read failed and leaves the active rental intelligence untouched.",
   "emptyFirstRun": "No active rental intelligence yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the active rental intelligence are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
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
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-563"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 87. 0 of 7 labels bound to a contract property; 7 of 74 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
