# WS92 — Rental Management board 5

**10 screens · 7 operations · 7 schemas · 2 permissions**

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

- **Every control that can be refused must be gated.** 2 permissions apply here:
  `RENTAL_BOOK, RENTAL_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-534` | Rental Booking Command Center | commandCentre | 1 | 0 | — |
| `BO-535` | New Rental Booking Wizard | configEditor | 2 | 0 | — |
| `BO-536` | Availability Selection & Alternative Options | listDetail | 1 | 0 | — |
| `BO-537` | Customer & Participant Information | listDetail | 1 | 0 | — |
| `BO-538` | Group Rental & Participant Management | listDetail | 2 | 0 | — |
| `BO-539` | Rental Agreement & Waiver Completion | listDetail | 1 | 0 | — |
| `BO-540` | Booking Commercial Summary & Payment | listDetail | 1 | 0 | — |
| `BO-541` | Reservation Confirmation & QR Voucher | listDetail | 1 | 0 | — |
| `BO-542` | Reservation Modification, Cancellation & No-Show | listDetail | 2 | 0 | — |
| `BO-543` | Reservation Detail, Timeline & Readiness | configEditor | 1 | 0 | — |

## Thin screens in this batch

**BO-537, BO-539, BO-540, BO-541, BO-543 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

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
  "apis": [
   {
    "operationId": "listRentalBookings",
    "contract": "rental",
    "purpose": "Reservations across locations",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-534",
   "workshopBoard": "wireframes/WS120 Rental Management Board 5.dc.html#bo-534"
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
  "apis": [
   {
    "operationId": "createRentalBooking",
    "contract": "rental",
    "purpose": "Reserve it",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listRentalBookings",
     "getRentalAvailability"
    ]
   },
   {
    "operationId": "quoteRentalPrice",
    "contract": "rental",
    "purpose": "What it will cost",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-535",
   "workshopBoard": "wireframes/WS120 Rental Management Board 5.dc.html#bo-535"
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
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 53"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "filters",
     "slot": "filters",
     "components": [
      {
       "kind": "selectField",
       "label": "Rental product",
       "operation": "getRentalAvailability",
       "notes": "Sends `?productId=` (required).",
       "provenance": "contract rental.yaml GET /rental-availability"
      },
      {
       "kind": "selectField",
       "label": "Rental location",
       "operation": "getRentalAvailability",
       "notes": "Sends `?locationId=`.",
       "provenance": "contract rental.yaml GET /rental-availability"
      },
      {
       "kind": "datePicker",
       "label": "Rental date and start",
       "operation": "getRentalAvailability",
       "notes": "Sends `?from=` and `?to=`.",
       "provenance": "contract rental.yaml GET /rental-availability"
      },
      {
       "kind": "numberField",
       "label": "Quantity",
       "operation": "getRentalAvailability",
       "notes": "Sends `?quantity=`.",
       "provenance": "contract rental.yaml GET /rental-availability"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Start times by duration",
       "bindsTo": "RentalAvailability.windows",
       "columns": [
        "RentalAvailability.windows[].from",
        "RentalAvailability.windows[].to",
        "RentalAvailability.windows[].availableQuantity"
       ],
       "operation": "getRentalAvailability",
       "notes": "The pack draws a start-time by duration grid (60 / 90 / 120 min); each duration column is one read with a different `to`. Zero shows Sold Out.",
       "provenance": "contract rental.yaml GET /rental-availability"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "Alternatives when the request cannot be met",
       "bindsTo": "RentalAvailability.windows",
       "columns": [
        "RentalAvailability.windows[].from",
        "RentalAvailability.windows[].availableQuantity",
        "Alternative location",
        "Distance from requested location",
        "AI recommendation"
       ],
       "operation": "getRentalAvailability",
       "notes": "Later start times are bound; other locations and the AI note (\"Marina B is about 5 minutes away\") are not.",
       "provenance": "pack Rental_Management.pdf, page 54"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Select this slot",
       "notes": "Carries the chosen window into the booking; no write operation is bound here.",
       "provenance": "pack Rental_Management.pdf, page 53"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The availability selection alternative list.",
   "error": "Could not load. Names which read failed and leaves the availability selection alternative untouched.",
   "emptyFirstRun": "No availability selection alternative yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the availability selection alternative are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getRentalAvailability",
    "contract": "rental",
    "purpose": "Alternatives when the first choice is gone",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-536",
   "workshopBoard": "wireframes/WS120 Rental Management Board 5.dc.html#bo-536"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 53. 0 of 0 labels bound to a contract property; 0 of 18 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Layout drafted 29 September (VM close-out)** from pack Rental_Management.pdf p.53; pack Rental_Management.pdf p.54; contract rental.yaml GET /rental-availability. Pack labels with no schema field yet (shown as plain labels): Duration columns in one read (60 / 90 / 120 min), Alternative location, Distance from requested location, AI recommendation.",
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
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "updateRentalBooking",
       "label": "Save rental booking",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "updateRentalBooking"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The customer participant information list.",
   "error": "Could not load. Names which read failed and leaves the customer participant information untouched.",
   "emptyFirstRun": "No customer participant information yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the customer participant information are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "updateRentalBooking",
    "contract": "rental",
    "purpose": "Capture customer details",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getRentalBooking",
     "listRentalBookings"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-537",
   "workshopBoard": "wireframes/WS120 Rental Management Board 5.dc.html#bo-537"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 54. 0 of 0 labels bound to a contract property; 0 of 19 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
    },
    {
     "name": "contentBody",
     "components": []
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
  "apis": [
   {
    "operationId": "createRentalBooking",
    "contract": "rental",
    "purpose": "One booking, many participants",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listRentalBookings",
     "getRentalAvailability"
    ]
   },
   {
    "operationId": "signRentalAgreement",
    "contract": "rental",
    "purpose": "Capture one group waiver signature for the booking",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration): serves the pack action(s) Group waiver where allowed"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-538",
   "workshopBoard": "wireframes/WS120 Rental Management Board 5.dc.html#bo-538"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 55. 0 of 0 labels bound to a contract property; 5 of 18 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Add participant, Bulk upload participants, Copy primary contact, Guardian information are choices sent by `createRentalBooking` (participants[] (name, isPrimaryRenter, guardianName, ...); bulk upload parsed client-side into participants[]); Group waiver where allowed: `signRentalAgreement`.",
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
  "apis": [
   {
    "operationId": "signRentalAgreement",
    "contract": "rental",
    "purpose": "Capture the signature against a version",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getRentalBooking"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "Rental Terms",
    "Liability Terms",
    "Safety Conditions",
    "Damage Responsibility",
    "Late Return Policy",
    "Deposit Policy"
   ],
   "params": [
    {
     "name": "bookingId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-539",
   "workshopBoard": "wireframes/WS120 Rental Management Board 5.dc.html#bo-539"
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
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "quoteRentalPrice",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "quoteRentalPrice"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The booking commercial summary list.",
   "error": "Could not load. Names which read failed and leaves the booking commercial summary untouched.",
   "emptyFirstRun": "No booking commercial summary yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the booking commercial summary are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "quoteRentalPrice",
    "contract": "rental",
    "purpose": "Rental amount and deposit, apart",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-540",
   "workshopBoard": "wireframes/WS120 Rental Management Board 5.dc.html#bo-540"
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
   "loading": "The reservation confirmation voucher list.",
   "error": "Could not load. Names which read failed and leaves the reservation confirmation voucher untouched.",
   "emptyFirstRun": "No reservation confirmation voucher yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the reservation confirmation voucher are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getRentalBooking",
    "contract": "rental",
    "purpose": "The confirmed reservation",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-541",
   "workshopBoard": "wireframes/WS120 Rental Management Board 5.dc.html#bo-541"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 57. 0 of 0 labels bound to a contract property; 0 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "apis": [
   {
    "operationId": "updateRentalBooking",
    "contract": "rental",
    "purpose": "Modify, cancel or mark a no-show",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getRentalBooking",
     "listRentalBookings"
    ]
   },
   {
    "operationId": "createRentalBooking",
    "contract": "rental",
    "purpose": "Rebook on a different product (cancel the old booking via updateRentalBooking)",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration): serves the pack action(s) Product"
   }
  ],
  "entryState": {
   "preloaded": [
    "Cancellation policy",
    "Refund amount",
    "Deposit release",
    "Cancellation fee",
    "Inventory released"
   ],
   "params": [
    {
     "name": "bookingId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-542",
   "workshopBoard": "wireframes/WS120 Rental Management Board 5.dc.html#bo-542"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 58. 0 of 5 labels bound to a contract property; 7 of 29 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Quantity are choices sent by `updateRentalBooking` (quantity); Product: `createRentalBooking`.",
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
  "apis": [
   {
    "operationId": "getRentalBooking",
    "contract": "rental",
    "purpose": "Timeline and readiness",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-543",
   "workshopBoard": "wireframes/WS120 Rental Management Board 5.dc.html#bo-543"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 59. 0 of 0 labels bound to a contract property; 3 of 83 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 }
]
```

## `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
 "createRentalBooking": {
  "method": "POST",
  "path": "/rental-bookings",
  "contract": "rental",
  "summary": "Reserve a rental",
  "permission": "RENTAL_BOOK",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "RentalBookingRequest",
  "responds": "RentalBooking"
 },
 "getRentalAvailability": {
  "method": "GET",
  "path": "/rental-availability",
  "contract": "rental",
  "summary": "What can be rented, when, with turnaround already subtracted",
  "permission": "RENTAL_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "productId",
    "in": "query",
    "required": true
   },
   {
    "name": "locationId",
    "in": "query",
    "required": null
   },
   {
    "name": "from",
    "in": "query",
    "required": true
   },
   {
    "name": "to",
    "in": "query",
    "required": true
   },
   {
    "name": "quantity",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "RentalAvailability"
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
 "quoteRentalPrice": {
  "method": "POST",
  "path": "/rental-price",
  "contract": "rental",
  "summary": "What this rental would cost, and the deposit it would hold",
  "permission": "RENTAL_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "RentalQuoteRequest",
  "responds": "RentalQuote"
 },
 "signRentalAgreement": {
  "method": "POST",
  "path": "/rental-bookings/{bookingId}/agreement",
  "contract": "rental",
  "summary": "Capture the signature, against a version",
  "permission": "RENTAL_BOOK",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "RentalAgreementSignature",
  "responds": "RentalAgreementSignature"
 },
 "updateRentalBooking": {
  "method": "PATCH",
  "path": "/rental-bookings/{bookingId}",
  "contract": "rental",
  "summary": "Modify, cancel or mark a no-show",
  "permission": "RENTAL_BOOK",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "RentalBooking"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "RentalAgreementSignature": {
  "type": "object",
  "x-ticvai-persistence": "rental.agreement_signature",
  "description": "Boards 1.9 and 5.6. **The version signed travels with the signature.**",
  "required": [
   "agreementVersion"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "participantId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "agreementVersion": {
    "type": "string"
   },
   "signatoryName": {
    "type": "string"
   },
   "signatoryRole": {
    "type": "string",
    "enum": [
     "renter",
     "participant",
     "guardian"
    ]
   },
   "signatureAssetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "documentAssetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "signedAt": {
    "type": "string",
    "format": "date-time"
   },
   "ipAddress": {
    "type": "string",
    "nullable": true
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "RentalAvailability": {
  "type": "object",
  "description": "Board 3. **A pooled product answers with a count, a serialised one with assets.**",
  "properties": {
   "productId": {
    "type": "string",
    "format": "uuid"
   },
   "locationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "windows": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "from": {
       "type": "string",
       "format": "date-time"
      },
      "to": {
       "type": "string",
       "format": "date-time"
      },
      "availableQuantity": {
       "type": "integer"
      },
      "availableAssetIds": {
       "type": "array",
       "items": {
        "type": "string",
        "format": "uuid"
       }
      }
     }
    }
   },
   "blockedWindows": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "from": {
       "type": "string",
       "format": "date-time"
      },
      "to": {
       "type": "string",
       "format": "date-time"
      },
      "reason": {
       "type": "string",
       "enum": [
        "booked",
        "turnaround",
        "maintenance",
        "blackout",
        "closed",
        "buffer",
        "held"
       ]
      }
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
 "RentalBookingRequest": {
  "type": "object",
  "required": [
   "productId",
   "from",
   "to"
  ],
  "properties": {
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
   "from": {
    "type": "string",
    "format": "date-time"
   },
   "to": {
    "type": "string",
    "format": "date-time"
   },
   "quantity": {
    "type": "integer",
    "default": 1
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
   "participants": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/RentalParticipant"
    }
   },
   "acceptedQuoteId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "A `rental.quote` id from `quoteRentalPrice`. **The booking is priced at the quote's `rentalAmount` and `depositAmount`** while the quote is unexpired and its product, location, window and quantity match the request; an expired or mismatched quote is `422` (`quoteExpired`, `quoteMismatch`) rather than silently repriced. Without it the booking is priced now (decided 29 September, writers pass; DM4)."
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
 "RentalQuote": {
  "type": "object",
  "x-ticvai-persistence": "rental.quote",
  "description": "Board 4.10. **Rental amount and deposit are returned apart, because the deposit is not revenue.**\n**A quote `quoteRentalPrice` issues is stored until `expiresAt`**, with what was asked, so the figures it gave can be held to and checked later. `explainRentalPrice` and `simulateRentalPricing` return the same shape and store nothing (decided 29 September, data model DM4).\n**Consumed by `acceptedQuoteId`** on `createRentalBooking` and the extension. A quote is not deleted when it is used or expires: a nightly job removes quotes 30 days past `expiresAt` that no booking references, so a booking can always show the quote it was priced at (decided 29 September, writers pass; DM4).\n",
  "required": [
   "quoteId",
   "productId",
   "from",
   "to",
   "rentalAmount",
   "depositAmount"
  ],
  "properties": {
   "quoteId": {
    "type": "string",
    "format": "uuid"
   },
   "productId": {
    "type": "string",
    "format": "uuid",
    "description": "The request's product; with `locationId`, `from`, `to` and `quantity`, what was quoted."
   },
   "locationId": {
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
    "type": "integer",
    "default": 1
   },
   "customerId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "rentalAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "taxAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "addOnAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "discountAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "totalPayable": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "depositAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "depositInstrument": {
    "type": "string",
    "nullable": true
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "createdAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "The partition key (ADR-0005), written at `venue` scope."
   }
  }
 },
 "RentalQuoteRequest": {
  "type": "object",
  "required": [
   "productId",
   "from",
   "to"
  ],
  "properties": {
   "productId": {
    "type": "string",
    "format": "uuid"
   },
   "locationId": {
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
    "type": "integer",
    "default": 1
   },
   "salesChannel": {
    "type": "string",
    "nullable": true
   },
   "customerId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "promotionCode": {
    "type": "string",
    "nullable": true
   }
  }
 }
}
```
