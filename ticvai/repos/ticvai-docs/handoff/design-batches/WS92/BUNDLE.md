# WS92 — Rental Management board 5

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
| `BO-534` | Rental Booking Command Center | commandCentre | 0 | 0 | — |
| `BO-535` | New Rental Booking Wizard | configEditor | 0 | 0 | — |
| `BO-536` | Availability Selection & Alternative Options | listDetail | 0 | 0 | — |
| `BO-537` | Customer & Participant Information | listDetail | 0 | 0 | — |
| `BO-538` | Group Rental & Participant Management | listDetail | 0 | 0 | — |
| `BO-539` | Rental Agreement & Waiver Completion | listDetail | 0 | 0 | — |
| `BO-540` | Booking Commercial Summary & Payment | listDetail | 0 | 0 | — |
| `BO-541` | Reservation Confirmation & QR Voucher | listDetail | 0 | 0 | — |
| `BO-542` | Reservation Modification, Cancellation & No-Show | listDetail | 0 | 0 | — |
| `BO-543` | Reservation Detail, Timeline & Readiness | configEditor | 0 | 0 | — |

## Thin screens in this batch

**BO-536, BO-537, BO-539, BO-540, BO-541, BO-543 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-534",
  "name": "Rental Booking Command Center",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "5",
   "number": "1",
   "page": 51
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/rental-booking-command-center-bo-534",
   "component": "apps/venue-management-web/src/routes/rentals/RentalBookingCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-535",
    "BO-536",
    "BO-537",
    "BO-538",
    "BO-539",
    "BO-540",
    "BO-541",
    "BO-542",
    "BO-543"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 5 wiring, 11 September 2026",
     "back": true
    },
    {
     "to": "BO-535",
     "trigger": "New Rental Booking Wizard",
     "provenance": "structural — pack board 5 wiring, 11 September 2026"
    },
    {
     "to": "BO-536",
     "trigger": "Availability Selection & Alternative Options",
     "provenance": "structural — pack board 5 wiring, 11 September 2026"
    },
    {
     "to": "BO-537",
     "trigger": "Customer & Participant Information",
     "provenance": "structural — pack board 5 wiring, 11 September 2026"
    },
    {
     "to": "BO-538",
     "trigger": "Group Rental & Participant Management",
     "provenance": "structural — pack board 5 wiring, 11 September 2026"
    },
    {
     "to": "BO-539",
     "trigger": "Rental Agreement & Waiver Completion",
     "provenance": "structural — pack board 5 wiring, 11 September 2026"
    },
    {
     "to": "BO-540",
     "trigger": "Booking Commercial Summary & Payment",
     "provenance": "structural — pack board 5 wiring, 11 September 2026"
    },
    {
     "to": "BO-541",
     "trigger": "Reservation Confirmation & QR Voucher",
     "provenance": "structural — pack board 5 wiring, 11 September 2026"
    },
    {
     "to": "BO-542",
     "trigger": "Reservation Modification, Cancellation & No-Show",
     "provenance": "structural — pack board 5 wiring, 11 September 2026"
    },
    {
     "to": "BO-543",
     "trigger": "Reservation Detail, Timeline & Readiness",
     "provenance": "structural — pack board 5 wiring, 11 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide a single operational view of all rental reservations across venues and locations.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search rental booking",
       "provenance": "pack Rental_Management.pdf, page 51 §Filters"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Date",
        "Venue",
        "Location",
        "Product",
        "Booking Type",
        "Channel",
        "Customer",
        "Status"
       ],
       "notes": "The pack filters this screen by date, venue, location, product, booking type, channel and 2 more — which are present is a decision the pack already made.",
       "provenance": "pack Rental_Management.pdf, page 51 §Filters"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Today's Reservations",
       "provenance": "pack Rental_Management.pdf, page 51 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Upcoming Rentals",
       "provenance": "pack Rental_Management.pdf, page 51 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Awaiting Arrival",
       "provenance": "pack Rental_Management.pdf, page 51 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Checked Out",
       "provenance": "pack Rental_Management.pdf, page 51 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Completed",
       "provenance": "pack Rental_Management.pdf, page 51 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Cancelled",
       "provenance": "pack Rental_Management.pdf, page 51 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "No-Shows",
       "provenance": "pack Rental_Management.pdf, page 51 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Group Bookings",
       "provenance": "pack Rental_Management.pdf, page 51 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Revenue Today",
       "provenance": "pack Rental_Management.pdf, page 51 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Booking Alerts",
       "provenance": "pack Rental_Management.pdf, page 51 §KPI Cards"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The rental booking list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the rental booking untouched.",
   "emptyFirstRun": "No rental booking yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the rental booking are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "entryState": {
   "preloaded": [
    "Today's Reservations",
    "Upcoming Rentals",
    "Awaiting Arrival",
    "Checked Out",
    "Completed",
    "Cancelled"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-534"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 51. 0 of 8 labels bound to a contract property; 18 of 34 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-535",
  "name": "New Rental Booking Wizard",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "5",
   "number": "2",
   "page": 52
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/new-rental-booking-wizard-bo-535",
   "component": "apps/venue-management-web/src/routes/rentals/NewRentalBookingWizard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-534"
   ],
   "exitTo": [
    "BO-534"
   ],
   "transitions": [
    {
     "to": "BO-534",
     "trigger": "Back to Rental Booking Command Center",
     "provenance": "structural — pack board 5 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Select) and no display directory — it is settings, not a population",
  "purpose": "Allow POS/rental operators to create a reservation through a guided workflow.",
  "gaps": [
   {
    "operation": null,
    "why": "**New Rental Booking Wizard declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
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
       "label": "Venue",
       "provenance": "pack Rental_Management.pdf, page 52 §Select"
      },
      {
       "kind": "selectField",
       "label": "Rental Location",
       "provenance": "pack Rental_Management.pdf, page 52 §Select"
      },
      {
       "kind": "selectField",
       "label": "Rental Product",
       "provenance": "pack Rental_Management.pdf, page 52 §Select"
      },
      {
       "kind": "selectField",
       "label": "Quantity",
       "provenance": "pack Rental_Management.pdf, page 52 §Select"
      },
      {
       "kind": "selectField",
       "label": "Rental Date",
       "provenance": "pack Rental_Management.pdf, page 52 §Select"
      },
      {
       "kind": "selectField",
       "label": "Start Time",
       "provenance": "pack Rental_Management.pdf, page 52 §Select"
      },
      {
       "kind": "selectField",
       "label": "Duration",
       "provenance": "pack Rental_Management.pdf, page 52 §Select"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The new rental booking configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the new rental booking untouched.",
   "emptyFirstRun": "No new rental booking configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-535"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 52. 0 of 0 labels bound to a contract property; 7 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-536",
  "name": "Availability Selection & Alternative Options",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "5",
   "number": "3",
   "page": 53
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/availability-selection-alternative-options-bo-536",
   "component": "apps/venue-management-web/src/routes/rentals/AvailabilitySelectionAlternativeOptions.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-534"
   ],
   "exitTo": [
    "BO-534"
   ],
   "transitions": [
    {
     "to": "BO-534",
     "trigger": "Back to Rental Booking Command Center",
     "provenance": "structural — pack board 5 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Give the operator/customer a clear booking choice based on Board 3 availability.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 53"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 53"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The availability selection alternative list.",
   "error": "Could not load. Names which read failed and leaves the availability selection alternative untouched.",
   "emptyFirstRun": "No availability selection alternative yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the availability selection alternative are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-536"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 53. 0 of 0 labels bound to a contract property; 0 of 18 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-537",
  "name": "Customer & Participant Information",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "5",
   "number": "4",
   "page": 54
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/customer-participant-information-bo-537",
   "component": "apps/venue-management-web/src/routes/rentals/CustomerParticipantInformation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-534"
   ],
   "exitTo": [
    "BO-534"
   ],
   "transitions": [
    {
     "to": "BO-534",
     "trigger": "Back to Rental Booking Command Center",
     "provenance": "structural — pack board 5 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Capture the configurable customer information required by the rental product. The original requirements specifically support configurable mandatory fields such as name, mobile, email, nationality, ID number and date of birth.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 54"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 54"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The customer participant information list.",
   "error": "Could not load. Names which read failed and leaves the customer participant information untouched.",
   "emptyFirstRun": "No customer participant information yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the customer participant information are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-537"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 54. 0 of 0 labels bound to a contract property; 0 of 19 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-538",
  "name": "Group Rental & Participant Management",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "5",
   "number": "5",
   "page": 55
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/group-rental-participant-management-bo-538",
   "component": "apps/venue-management-web/src/routes/rentals/GroupRentalParticipantManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-534"
   ],
   "exitTo": [
    "BO-534"
   ],
   "transitions": [
    {
     "to": "BO-534",
     "trigger": "Back to Rental Booking Command Center",
     "provenance": "structural — pack board 5 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Handle reservations involving multiple participants. The source explicitly requires group reservations, participant demographics and configurable participant forms.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 5 actions on this screen and the screen declares 0 operations.** Unserved: Add participant, Bulk upload participants, Copy primary contact, Guardian information, Group waiver where allowed. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Rental_Management.pdf, page 55 §Support"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 55"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 55"
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
       "label": "Add participant",
       "provenance": "pack Rental_Management.pdf, page 55 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Bulk upload participants",
       "provenance": "pack Rental_Management.pdf, page 55 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Copy primary contact",
       "provenance": "pack Rental_Management.pdf, page 55 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Guardian information",
       "provenance": "pack Rental_Management.pdf, page 55 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Group waiver where allowed",
       "provenance": "pack Rental_Management.pdf, page 55 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The group rental participant list.",
   "error": "Could not load. Names which read failed and leaves the group rental participant untouched.",
   "emptyFirstRun": "No group rental participant yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the group rental participant are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-538"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 55. 0 of 0 labels bound to a contract property; 5 of 18 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-539",
  "name": "Rental Agreement & Waiver Completion",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "5",
   "number": "6",
   "page": 55
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/rental-agreement-waiver-completion-bo-539",
   "component": "apps/venue-management-web/src/routes/rentals/RentalAgreementWaiverCompletion.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-534"
   ],
   "exitTo": [
    "BO-534"
   ],
   "transitions": [
    {
     "to": "BO-534",
     "trigger": "Back to Rental Booking Command Center",
     "provenance": "structural — pack board 5 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Complete all mandatory customer acknowledgments before confirmation or checkout. This implements the digital rental agreement/waiver capability recommended in the source.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Rental_Management.pdf, page 55 §Display"
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
       "label": "Every rental agreement waiver",
       "columns": [
        "Rental Terms",
        "Liability Terms",
        "Safety Conditions",
        "Damage Responsibility",
        "Late Return Policy",
        "Deposit Policy",
        "Cancellation Policy"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Rental_Management.pdf, page 55 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected rental agreement waiver",
       "bindsTo": null,
       "columns": [
        "Rental Terms",
        "Liability Terms",
        "Safety Conditions",
        "Damage Responsibility",
        "Late Return Policy",
        "Deposit Policy",
        "Cancellation Policy"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Agreement”, “Completion Methods”, “Customer Signature”.",
       "provenance": "pack Rental_Management.pdf, page 55 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The rental agreement waiver list.",
   "error": "Could not load. Names which read failed and leaves the rental agreement waiver untouched.",
   "emptyFirstRun": "No rental agreement waiver yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the rental agreement waiver are still there. The pack's own statuses are ✓ Rental Agreement — the state names which is selected.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "entryState": {
   "preloaded": [
    "Rental Terms",
    "Liability Terms",
    "Safety Conditions",
    "Damage Responsibility",
    "Late Return Policy",
    "Deposit Policy"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-539"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 55. 0 of 7 labels bound to a contract property; 11 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-540",
  "name": "Booking Commercial Summary & Payment",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "5",
   "number": "7",
   "page": 56
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/booking-commercial-summary-payment-bo-540",
   "component": "apps/venue-management-web/src/routes/rentals/BookingCommercialSummaryPayment.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-534"
   ],
   "exitTo": [
    "BO-534"
   ],
   "transitions": [
    {
     "to": "BO-534",
     "trigger": "Back to Rental Booking Command Center",
     "provenance": "structural — pack board 5 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Show the complete financial commitment before confirming the reservation.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 56"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 56"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The booking commercial summary list.",
   "error": "Could not load. Names which read failed and leaves the booking commercial summary untouched.",
   "emptyFirstRun": "No booking commercial summary yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the booking commercial summary are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-540"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 56. 0 of 0 labels bound to a contract property; 0 of 13 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-541",
  "name": "Reservation Confirmation & QR Voucher",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "5",
   "number": "8",
   "page": 57
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/reservation-confirmation-qr-voucher-bo-541",
   "component": "apps/venue-management-web/src/routes/rentals/ReservationConfirmationQrVoucher.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-534"
   ],
   "exitTo": [
    "BO-534"
   ],
   "transitions": [
    {
     "to": "BO-534",
     "trigger": "Back to Rental Booking Command Center",
     "provenance": "structural — pack board 5 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Create the confirmed rental reservation and customer credential. The original voucher flow specifically requires the system to generate a voucher/ticket that is later redeemed at the rental counter.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 57"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 57"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The reservation confirmation voucher list.",
   "error": "Could not load. Names which read failed and leaves the reservation confirmation voucher untouched.",
   "emptyFirstRun": "No reservation confirmation voucher yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the reservation confirmation voucher are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-541"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 57. 0 of 0 labels bound to a contract property; 0 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-542",
  "name": "Reservation Modification, Cancellation & No-Show",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "5",
   "number": "9",
   "page": 58
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/reservation-modification-cancellation-no-show-bo-542",
   "component": "apps/venue-management-web/src/routes/rentals/ReservationModificationCancellationNoShow.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-534"
   ],
   "exitTo": [
    "BO-534"
   ],
   "transitions": [
    {
     "to": "BO-534",
     "trigger": "Back to Rental Booking Command Center",
     "provenance": "structural — pack board 5 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Manage the reservation after confirmation but before/during fulfillment.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 2 actions on this screen and the screen declares 0 operations.** Unserved: Quantity, Product. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Rental_Management.pdf, page 58 §Allow authorized changes to"
   },
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Rental_Management.pdf, page 58 §Display"
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
       "label": "Every reservation modification cancellation",
       "columns": [
        "Cancellation policy",
        "Refund amount",
        "Deposit release",
        "Cancellation fee",
        "Inventory released"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Rental_Management.pdf, page 58 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected reservation modification cancellation",
       "bindsTo": null,
       "columns": [
        "Cancellation policy",
        "Refund amount",
        "Deposit release",
        "Cancellation fee",
        "Inventory released"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Original”, “Requested”, “Availability”, “Difference”, “No-Show”, “Expected arrival”.",
       "provenance": "pack Rental_Management.pdf, page 58 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Quantity",
       "provenance": "pack Rental_Management.pdf, page 58 §Allow authorized changes to"
      },
      {
       "kind": "secondaryButton",
       "label": "Product",
       "provenance": "pack Rental_Management.pdf, page 58 §Allow authorized changes to"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The reservation modification cancellation list.",
   "error": "Could not load. Names which read failed and leaves the reservation modification cancellation untouched.",
   "emptyFirstRun": "No reservation modification cancellation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the reservation modification cancellation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "entryState": {
   "preloaded": [
    "Cancellation policy",
    "Refund amount",
    "Deposit release",
    "Cancellation fee",
    "Inventory released"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-542"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 58. 0 of 5 labels bound to a contract property; 7 of 29 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-543",
  "name": "Reservation Detail, Timeline & Readiness",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "5",
   "number": "10",
   "page": 59
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/reservation-detail-timeline-readiness-bo-543",
   "component": "apps/venue-management-web/src/routes/rentals/ReservationDetailTimelineReadiness.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-534"
   ],
   "exitTo": [
    "BO-534"
   ],
   "transitions": [
    {
     "to": "BO-534",
     "trigger": "Back to Rental Booking Command Center",
     "provenance": "structural — pack board 5 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Select/Scan BIKE-028; Select Product; Capture Customer) and no display directory — it is settings, not a population",
  "purpose": "Provide the complete operational record before handing the reservation to Board 6 for checkout.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "↓",
       "provenance": "pack Rental_Management.pdf, page 59 §Select/Scan BIKE-028"
      },
      {
       "kind": "textField",
       "label": "Check Availability — Board 3",
       "provenance": "pack Rental_Management.pdf, page 59 §Select Product"
      },
      {
       "kind": "textField",
       "label": "Calculate Price & Deposit — Board 4",
       "provenance": "pack Rental_Management.pdf, page 59 §Select Product"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The reservation detail timeline configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the reservation detail timeline untouched.",
   "emptyFirstRun": "No reservation detail timeline configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-543"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 59. 0 of 0 labels bound to a contract property; 3 of 83 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
