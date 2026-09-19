# WS28 — Group Sales   Corporate Booking Management board 2

**10 screens · 10 operations · 11 schemas · 2 permissions**

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
  `ORDER_CREATE, ORDER_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **0 of these operations work offline**
  
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-274` | Group Booking Operations Command Center | listDetail | 1 | 0 | — |
| `BO-275` | Group Operational Planning & Task Workspace | configEditor | 1 | 0 | — |
| `BO-276` | Participants, Guest Lists & Group Structure | listDetail | 1 | 0 | — |
| `BO-277` | Group Payment, Deposit & Balance Management | listDetail | 1 | 0 | — |
| `BO-278` | Group Ticket, Seat & Entitlement Allocation | listDetail | 1 | 0 | — |
| `BO-279` | Group Ticket Fulfillment & Distribution | listDetail | 1 | 0 | — |
| `BO-280` | Group Arrival, Check-In & Admission Operations | listDetail | 1 | 0 | — |
| `BO-281` | Group Amendments, Cancellation & Refund Operations | listDetail | 1 | 0 | — |
| `BO-282` | Group Booking Reconciliation, Closure & Performance | listDetail | 1 | 0 | — |
| `BO-283` | Group Sales Analytics & AI Intelligence Center | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-274, BO-277, BO-279, BO-280, BO-282 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-274",
  "name": "Group Booking Operations Command Center",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Group_Sales___Corporate_Booking_Management_Reference.pdf",
   "board": "2",
   "number": "9.2.1",
   "page": 20
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/group-booking-operations-command-center-bo-274",
   "component": "apps/venue-management-web/src/routes/sell/GroupBookingOperationsCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-275",
    "BO-276",
    "BO-277",
    "BO-278",
    "BO-279",
    "BO-280",
    "BO-281",
    "BO-282",
    "BO-283"
   ],
   "inferred": false,
   "notes": "**The board's hub.** The workshop specified this module as boards of ten and opened each with a command centre; the other nine screens are that board's detail, so they are reached from here and return here.",
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Venue Home",
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-100 declares entryState.params venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-275",
     "trigger": "Works in Group Operational Planning & Task Workspace",
     "provenance": "flow F137 step 1→2",
     "operation": "listGroupBooking"
    },
    {
     "to": "BO-276",
     "trigger": "Works in Participants, Guest Lists & Group Structure",
     "provenance": "flow F137 step 3→4",
     "operation": "listGroupBooking"
    },
    {
     "to": "BO-277",
     "trigger": "Works in Group Payment, Deposit & Balance Management",
     "provenance": "flow F137 step 5→6",
     "operation": "listGroupBooking"
    },
    {
     "to": "BO-278",
     "trigger": "Works in Group Ticket, Seat & Entitlement Allocation",
     "provenance": "flow F137 step 7→8",
     "operation": "listGroupBooking"
    },
    {
     "to": "BO-279",
     "trigger": "Works in Group Ticket Fulfillment & Distribution",
     "provenance": "flow F137 step 9→10",
     "operation": "listGroupBooking"
    },
    {
     "to": "BO-280",
     "trigger": "Works in Group Arrival, Check-In & Admission Operations",
     "provenance": "flow F137 step 11→12",
     "operation": "listGroupBooking"
    },
    {
     "to": "BO-281",
     "trigger": "Works in Group Amendments, Cancellation & Refund Operations",
     "provenance": "flow F137 step 13→14",
     "operation": "listGroupBooking"
    },
    {
     "to": "BO-282",
     "trigger": "Works in Group Booking Reconciliation, Closure & Performance",
     "provenance": "flow F137 step 15→16",
     "operation": "listGroupBooking"
    },
    {
     "to": "BO-283",
     "trigger": "Works in Group Sales Analytics & AI Intelligence Center",
     "provenance": "flow F137 step 17→18",
     "operation": "listGroupBooking"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide Operations with a real-time command center for all confirmed and upcoming group bookings.",
  "purposeNote": "Operations can identify every upcoming group, its readiness and outstanding actions from one centralized workspace.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every group booking operations",
       "columns": [
        "GroupBookingOperationsCommandCenterView.upcomingGroups",
        "GroupBookingOperationsCommandCenterView.groupsToday",
        "GroupBookingOperationsCommandCenterView.expectedGuestsToday",
        "GroupBookingOperationsCommandCenterView.groupsAwaitingDeposit",
        "GroupBookingOperationsCommandCenterView.guestListsPending",
        "GroupBookingOperationsCommandCenterView.ticketsPending",
        "GroupBookingOperationsCommandCenterView.resourcesPending",
        "GroupBookingOperationsCommandCenterView.groupsReady",
        "GroupBookingOperationsCommandCenterView.groupsWithIssues",
        "GroupBookingOperationsCommandCenterView.outstandingPayments",
        "GroupBookingOperationsCommandCenterView.checkInsToday",
        "GroupBookingOperationsCommandCenterView.completedGroups",
        "GroupBookingOperationsCommandCenterView.groupBookingId",
        "GroupBookingOperationsCommandCenterView.organization",
        "GroupBookingOperationsCommandCenterView.groupType",
        "GroupBookingOperationsCommandCenterView.venueEvent",
        "GroupBookingOperationsCommandCenterView.visitDate",
        "GroupBookingOperationsCommandCenterView.arrivalTime",
        "GroupBookingOperationsCommandCenterView.guests",
        "GroupBookingOperationsCommandCenterView.bookingValue",
        "GroupBookingOperationsCommandCenterView.paymentStatus",
        "GroupBookingOperationsCommandCenterView.guestListStatus",
        "GroupBookingOperationsCommandCenterView.ticketStatus",
        "GroupBookingOperationsCommandCenterView.resourceStatus",
        "GroupBookingOperationsCommandCenterView.readiness",
        "GroupBookingOperationsCommandCenterView.operationalOwner"
       ],
       "bindsTo": "GroupBookingOperationsCommandCenterView",
       "operation": "listGroupBooking",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 20 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected group booking operations",
       "bindsTo": "GroupBookingOperationsCommandCenterView",
       "columns": [
        "GroupBookingOperationsCommandCenterView.upcomingGroups",
        "GroupBookingOperationsCommandCenterView.groupsToday",
        "GroupBookingOperationsCommandCenterView.expectedGuestsToday",
        "GroupBookingOperationsCommandCenterView.groupsAwaitingDeposit",
        "GroupBookingOperationsCommandCenterView.guestListsPending",
        "GroupBookingOperationsCommandCenterView.ticketsPending",
        "GroupBookingOperationsCommandCenterView.resourcesPending",
        "GroupBookingOperationsCommandCenterView.groupsReady",
        "GroupBookingOperationsCommandCenterView.groupsWithIssues",
        "GroupBookingOperationsCommandCenterView.outstandingPayments",
        "GroupBookingOperationsCommandCenterView.checkInsToday",
        "GroupBookingOperationsCommandCenterView.completedGroups",
        "GroupBookingOperationsCommandCenterView.groupBookingId",
        "GroupBookingOperationsCommandCenterView.organization",
        "GroupBookingOperationsCommandCenterView.groupType",
        "GroupBookingOperationsCommandCenterView.venueEvent",
        "GroupBookingOperationsCommandCenterView.visitDate",
        "GroupBookingOperationsCommandCenterView.arrivalTime",
        "GroupBookingOperationsCommandCenterView.guests",
        "GroupBookingOperationsCommandCenterView.bookingValue",
        "GroupBookingOperationsCommandCenterView.paymentStatus",
        "GroupBookingOperationsCommandCenterView.guestListStatus",
        "GroupBookingOperationsCommandCenterView.ticketStatus",
        "GroupBookingOperationsCommandCenterView.resourceStatus",
        "GroupBookingOperationsCommandCenterView.readiness",
        "GroupBookingOperationsCommandCenterView.operationalOwner"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Use”.",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 20 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The group booking operations list.",
   "error": "Could not load. Names which read failed and leaves the group booking operations untouched.",
   "emptyFirstRun": "No group booking operations yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the group booking operations are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listGroupBooking",
    "contract": "orders",
    "purpose": "Group Booking Operations Command Center",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "GroupBookingOperationsCommandCenterView.upcomingGroups",
    "GroupBookingOperationsCommandCenterView.groupsToday",
    "GroupBookingOperationsCommandCenterView.expectedGuestsToday",
    "GroupBookingOperationsCommandCenterView.groupsAwaitingDeposit",
    "GroupBookingOperationsCommandCenterView.guestListsPending",
    "GroupBookingOperationsCommandCenterView.ticketsPending"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-274"
  },
  "apisNote": "Regenerated 9 September 2026 from Group_Sales___Corporate_Booking_Management_Reference.pdf page 20. 26 of 26 labels bound to a contract property; 26 of 37 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-275",
  "name": "Group Operational Planning & Task Workspace",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Group_Sales___Corporate_Booking_Management_Reference.pdf",
   "board": "2",
   "number": "9.2.2",
   "page": 22
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/group-operational-planning-task-workspace-bo-275",
   "component": "apps/venue-management-web/src/routes/sell/GroupOperationalPlanningTaskWorkspace.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-274"
   ],
   "exitTo": [
    "BO-274"
   ],
   "inferred": false,
   "notes": "**Reached from BO-274, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-274",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F137 step 2→3",
     "operation": "setGroupOperationalPlanning"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure/reference) and no display directory — it is settings, not a population",
  "purpose": "Convert the commercial booking into a detailed operational execution plan.",
  "purposeNote": "Every confirmed group can be translated into a structured operational plan with owners, deadlines and dependencies.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Arrival Date",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 22 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Arrival Time",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 22 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Arrival Location",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 22 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Group Meeting Point",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 22 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Entry Gate",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 22 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Departure Time",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 22 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Group Size",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 22 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Group Leaders",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 22 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Contact Person",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 22 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Ticketing Method",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 22 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Seating",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 22 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Guides",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 22 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Catering",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 22 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Transportation",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 22 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Parking",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 22 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Accessibility",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 22 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Equipment",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 22 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Special Requirements",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 22 §Configure/reference"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save changes",
       "provenance": "contract operation setGroupOperationalPlanning"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The group operational planning configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the group operational planning untouched.",
   "emptyFirstRun": "No group operational planning configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setGroupOperationalPlanning",
    "contract": "orders",
    "purpose": "Group Operational Planning & Task Workspace",
    "trigger": "onAction",
    "invalidates": [
     "setGroupOperationalPlanning"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-275"
  },
  "apisNote": "Regenerated 9 September 2026 from Group_Sales___Corporate_Booking_Management_Reference.pdf page 22. 0 of 0 labels bound to a contract property; 18 of 41 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-276",
  "name": "Participants, Guest Lists & Group Structure",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Group_Sales___Corporate_Booking_Management_Reference.pdf",
   "board": "2",
   "number": "9.2.3",
   "page": 23
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/participants-guest-lists-group-structure-bo-276",
   "component": "apps/venue-management-web/src/routes/sell/ParticipantsGuestListsGroupStructure.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-274"
   ],
   "exitTo": [
    "BO-274"
   ],
   "inferred": false,
   "notes": "**Reached from BO-274, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-274",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F137 step 4→5",
     "operation": "listParticipantGuestList"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Detect) and no metric row",
  "purpose": "Manage the people participating in the group where individual information is required.",
  "purposeNote": "confirmed group quantity.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 2 actions on this screen and the screen declares 1 operation.** Unserved: CSV/Excel Import, Customer Upload. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 23 §Support"
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
       "label": "Every participants guest lists",
       "columns": [
        "Duplicate guest",
        "ParticipantsGuestListsGroupStructureView.missingRequiredField",
        "ParticipantsGuestListsGroupStructureView.invalidCategory",
        "ParticipantsGuestListsGroupStructureView.guestCountMismatch",
        "ParticipantsGuestListsGroupStructureView.ageTicketMismatch",
        "Duplicate ticket assignment"
       ],
       "bindsTo": "ParticipantsGuestListsGroupStructureView",
       "operation": "listParticipantGuestList",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 23 §Detect"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected participants guest lists",
       "bindsTo": "ParticipantsGuestListsGroupStructureView",
       "columns": [
        "Duplicate guest",
        "ParticipantsGuestListsGroupStructureView.missingRequiredField",
        "ParticipantsGuestListsGroupStructureView.invalidCategory",
        "ParticipantsGuestListsGroupStructureView.guestCountMismatch",
        "ParticipantsGuestListsGroupStructureView.ageTicketMismatch",
        "Duplicate ticket assignment"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Named Guests”, “Quantity-Based”, “Hybrid”, “Where required”, “Privacy”.",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 23 §Detect"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "CSV/Excel Import",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 23 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Customer Upload",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 23 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The participants guest lists list.",
   "error": "Could not load. Names which read failed and leaves the participants guest lists untouched.",
   "emptyFirstRun": "No participants guest lists yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the participants guest lists are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listParticipantGuestList",
    "contract": "orders",
    "purpose": "Participants, Guest Lists & Group Structure",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "Duplicate guest",
    "ParticipantsGuestListsGroupStructureView.missingRequiredField",
    "ParticipantsGuestListsGroupStructureView.invalidCategory",
    "ParticipantsGuestListsGroupStructureView.guestCountMismatch",
    "ParticipantsGuestListsGroupStructureView.ageTicketMismatch",
    "Duplicate ticket assignment"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-276"
  },
  "apisNote": "Regenerated 9 September 2026 from Group_Sales___Corporate_Booking_Management_Reference.pdf page 23. 4 of 6 labels bound to a contract property; 8 of 38 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-277",
  "name": "Group Payment, Deposit & Balance Management",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Group_Sales___Corporate_Booking_Management_Reference.pdf",
   "board": "2",
   "number": "9.2.4",
   "page": 25
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/group-payment-deposit-balance-management-bo-277",
   "component": "apps/venue-management-web/src/routes/sell/GroupPaymentDepositBalanceManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-274"
   ],
   "exitTo": [
    "BO-274"
   ],
   "inferred": false,
   "notes": "**Reached from BO-274, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-274",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F137 step 6→7",
     "operation": "listGroupPaymentDeposit"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Track the complete payment lifecycle of a group booking.",
  "purposeNote": "Sales, Finance and Operations can understand exactly what has been paid, what remains due and whether payment conditions permit fulfillment.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Custom Schedule. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 25 §Support"
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
       "label": "Every group payment deposit",
       "columns": [
        "GroupPaymentDepositBalanceManagementView.bookingValue",
        "GroupPaymentDepositBalanceManagementView.depositRequired",
        "GroupPaymentDepositBalanceManagementView.depositPaid",
        "GroupPaymentDepositBalanceManagementView.balance",
        "GroupPaymentDepositBalanceManagementView.amountPaid",
        "GroupPaymentDepositBalanceManagementView.amountOutstanding",
        "GroupPaymentDepositBalanceManagementView.nextDueDate",
        "GroupPaymentDepositBalanceManagementView.paymentStatus"
       ],
       "bindsTo": "GroupPaymentDepositBalanceManagementView",
       "operation": "listGroupPaymentDeposit",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 25 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected group payment deposit",
       "bindsTo": "GroupPaymentDepositBalanceManagementView",
       "columns": [
        "GroupPaymentDepositBalanceManagementView.bookingValue",
        "GroupPaymentDepositBalanceManagementView.depositRequired",
        "GroupPaymentDepositBalanceManagementView.depositPaid",
        "GroupPaymentDepositBalanceManagementView.balance",
        "GroupPaymentDepositBalanceManagementView.amountPaid",
        "GroupPaymentDepositBalanceManagementView.amountOutstanding",
        "GroupPaymentDepositBalanceManagementView.nextDueDate",
        "GroupPaymentDepositBalanceManagementView.paymentStatus"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Payment Methods”, “Architecture”.",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 25 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Custom Schedule",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 25 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The group payment deposit list.",
   "error": "Could not load. Names which read failed and leaves the group payment deposit untouched.",
   "emptyFirstRun": "No group payment deposit yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the group payment deposit are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listGroupPaymentDeposit",
    "contract": "orders",
    "purpose": "Group Payment, Deposit & Balance Management",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "GroupPaymentDepositBalanceManagementView.bookingValue",
    "GroupPaymentDepositBalanceManagementView.depositRequired",
    "GroupPaymentDepositBalanceManagementView.depositPaid",
    "GroupPaymentDepositBalanceManagementView.balance",
    "GroupPaymentDepositBalanceManagementView.amountPaid",
    "GroupPaymentDepositBalanceManagementView.amountOutstanding"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-277"
  },
  "apisNote": "Regenerated 9 September 2026 from Group_Sales___Corporate_Booking_Management_Reference.pdf page 25. 8 of 8 labels bound to a contract property; 9 of 38 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-278",
  "name": "Group Ticket, Seat & Entitlement Allocation",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Group_Sales___Corporate_Booking_Management_Reference.pdf",
   "board": "2",
   "number": "9.2.5",
   "page": 26
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/group-ticket-seat-entitlement-allocation-bo-278",
   "component": "apps/venue-management-web/src/routes/sell/GroupTicketSeatEntitlementAllocation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-274"
   ],
   "exitTo": [
    "BO-274"
   ],
   "inferred": false,
   "notes": "**Reached from BO-274, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-274",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F137 step 8→9",
     "operation": "listGroupTicketSeat"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Allocate the confirmed group inventory to individual guests, subgroups or quantity blocks.",
  "purposeNote": "Every confirmed group entitlement can be correctly allocated without creating duplicate capacity or conflicting seat assignments.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 6 actions on this screen and the screen declares 1 operation.** Unserved: Individual Ticket, Bulk Ticket, Named Ticket, Quantity-Based Ticket, Zone Allocation, VIP allocation. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 26 §Support"
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
       "label": "Every group ticket seat",
       "columns": [
        "GroupTicketSeatEntitlementAllocationView.product",
        "GroupTicketSeatEntitlementAllocationView.quantityBooked",
        "GroupTicketSeatEntitlementAllocationView.quantityAllocated",
        "GroupTicketSeatEntitlementAllocationView.remaining",
        "GroupTicketSeatEntitlementAllocationView.ticketType",
        "GroupTicketSeatEntitlementAllocationView.seatZone",
        "GroupTicketSeatEntitlementAllocationView.guestSubgroup",
        "GroupTicketSeatEntitlementAllocationView.credentialStatus"
       ],
       "bindsTo": "GroupTicketSeatEntitlementAllocationView",
       "operation": "listGroupTicketSeat",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 26 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected group ticket seat",
       "bindsTo": "GroupTicketSeatEntitlementAllocationView",
       "columns": [
        "GroupTicketSeatEntitlementAllocationView.product",
        "GroupTicketSeatEntitlementAllocationView.quantityBooked",
        "GroupTicketSeatEntitlementAllocationView.quantityAllocated",
        "GroupTicketSeatEntitlementAllocationView.remaining",
        "GroupTicketSeatEntitlementAllocationView.ticketType",
        "GroupTicketSeatEntitlementAllocationView.seatZone",
        "GroupTicketSeatEntitlementAllocationView.guestSubgroup",
        "GroupTicketSeatEntitlementAllocationView.credentialStatus"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Reserved Seating”, “Assigned”, “Allocate associated”.",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 26 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Individual Ticket",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 26 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Bulk Ticket",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 26 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Named Ticket",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 26 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Quantity-Based Ticket",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 26 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Zone Allocation",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 26 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "VIP allocation",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 26 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The group ticket seat list.",
   "error": "Could not load. Names which read failed and leaves the group ticket seat untouched.",
   "emptyFirstRun": "No group ticket seat yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the group ticket seat are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listGroupTicketSeat",
    "contract": "orders",
    "purpose": "Group Ticket, Seat & Entitlement Allocation",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "GroupTicketSeatEntitlementAllocationView.product",
    "GroupTicketSeatEntitlementAllocationView.quantityBooked",
    "GroupTicketSeatEntitlementAllocationView.quantityAllocated",
    "GroupTicketSeatEntitlementAllocationView.remaining",
    "GroupTicketSeatEntitlementAllocationView.ticketType",
    "GroupTicketSeatEntitlementAllocationView.seatZone"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-278"
  },
  "apisNote": "Regenerated 9 September 2026 from Group_Sales___Corporate_Booking_Management_Reference.pdf page 26. 8 of 8 labels bound to a contract property; 14 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-279",
  "name": "Group Ticket Fulfillment & Distribution",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Group_Sales___Corporate_Booking_Management_Reference.pdf",
   "board": "2",
   "number": "9.2.6",
   "page": 27
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/group-ticket-fulfillment-distribution-bo-279",
   "component": "apps/venue-management-web/src/routes/sell/GroupTicketFulfillmentDistribution.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-274"
   ],
   "exitTo": [
    "BO-274"
   ],
   "inferred": false,
   "notes": "**Reached from BO-274, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-274",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F137 step 10→11",
     "operation": "listGroupTicketFulfillment"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Control how tickets and other credentials are delivered to the group.",
  "purposeNote": "maintaining complete ticket-to-guest traceability.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every group ticket fulfillment",
       "columns": [
        "GroupTicketFulfillmentDistributionView.ticketsRequired",
        "GroupTicketFulfillmentDistributionView.generated",
        "GroupTicketFulfillmentDistributionView.sent",
        "GroupTicketFulfillmentDistributionView.delivered",
        "GroupTicketFulfillmentDistributionView.opened",
        "GroupTicketFulfillmentDistributionView.downloaded",
        "GroupTicketFulfillmentDistributionView.failed",
        "GroupTicketFulfillmentDistributionView.reissued"
       ],
       "bindsTo": "GroupTicketFulfillmentDistributionView",
       "operation": "listGroupTicketFulfillment",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 27 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected group ticket fulfillment",
       "bindsTo": "GroupTicketFulfillmentDistributionView",
       "columns": [
        "GroupTicketFulfillmentDistributionView.ticketsRequired",
        "GroupTicketFulfillmentDistributionView.generated",
        "GroupTicketFulfillmentDistributionView.sent",
        "GroupTicketFulfillmentDistributionView.delivered",
        "GroupTicketFulfillmentDistributionView.opened",
        "GroupTicketFulfillmentDistributionView.downloaded",
        "GroupTicketFulfillmentDistributionView.failed",
        "GroupTicketFulfillmentDistributionView.reissued"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Central Distribution”, “Individual Distribution”, “Subgroup Distribution”, “Generate an operational manifest showing”, “Important Architecture”.",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 27 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "banner",
       "label": "Permissions this screen separates",
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** Generate Tickets, Send, Resend, Print, Reissue, Change Delivery Method, Revoke where permitted. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 27 §Authorized users can"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The group ticket fulfillment list.",
   "error": "Could not load. Names which read failed and leaves the group ticket fulfillment untouched.",
   "emptyFirstRun": "No group ticket fulfillment yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the group ticket fulfillment are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listGroupTicketFulfillment",
    "contract": "orders",
    "purpose": "Group Ticket Fulfillment & Distribution",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "GroupTicketFulfillmentDistributionView.ticketsRequired",
    "GroupTicketFulfillmentDistributionView.generated",
    "GroupTicketFulfillmentDistributionView.sent",
    "GroupTicketFulfillmentDistributionView.delivered",
    "GroupTicketFulfillmentDistributionView.opened",
    "GroupTicketFulfillmentDistributionView.downloaded"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-279"
  },
  "apisNote": "Regenerated 9 September 2026 from Group_Sales___Corporate_Booking_Management_Reference.pdf page 27. 8 of 8 labels bound to a contract property; 15 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-280",
  "name": "Group Arrival, Check-In & Admission Operations",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Group_Sales___Corporate_Booking_Management_Reference.pdf",
   "board": "2",
   "number": "9.2.7",
   "page": 29
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/group-arrival-check-in-admission-operations-bo-280",
   "component": "apps/venue-management-web/src/routes/sell/GroupArrivalCheckInAdmissionOperations.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-274"
   ],
   "exitTo": [
    "BO-274"
   ],
   "inferred": false,
   "notes": "**Reached from BO-274, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-274",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F137 step 12→13",
     "operation": "listGroupArrivalCheck"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Manage the physical arrival and admission of large groups efficiently.",
  "purposeNote": "Operations can process large group arrivals efficiently while preserving accurate admission and headcount records.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every group arrival check-in",
       "columns": [
        "GroupArrivalCheckInAdmissionOperationsView.groupsExpectedToday",
        "GroupArrivalCheckInAdmissionOperationsView.arrivalTime",
        "GroupArrivalCheckInAdmissionOperationsView.actualArrival",
        "GroupArrivalCheckInAdmissionOperationsView.groupSize",
        "GroupArrivalCheckInAdmissionOperationsView.checkedIn",
        "GroupArrivalCheckInAdmissionOperationsView.remaining",
        "GroupArrivalCheckInAdmissionOperationsView.gate",
        "GroupArrivalCheckInAdmissionOperationsView.groupLeader",
        "GroupArrivalCheckInAdmissionOperationsView.readiness",
        "GroupArrivalCheckInAdmissionOperationsView.issues"
       ],
       "bindsTo": "GroupArrivalCheckInAdmissionOperationsView",
       "operation": "listGroupArrivalCheck",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 29 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected group arrival check-in",
       "bindsTo": "GroupArrivalCheckInAdmissionOperationsView",
       "columns": [
        "GroupArrivalCheckInAdmissionOperationsView.groupsExpectedToday",
        "GroupArrivalCheckInAdmissionOperationsView.arrivalTime",
        "GroupArrivalCheckInAdmissionOperationsView.actualArrival",
        "GroupArrivalCheckInAdmissionOperationsView.groupSize",
        "GroupArrivalCheckInAdmissionOperationsView.checkedIn",
        "GroupArrivalCheckInAdmissionOperationsView.remaining",
        "GroupArrivalCheckInAdmissionOperationsView.gate",
        "GroupArrivalCheckInAdmissionOperationsView.groupLeader",
        "GroupArrivalCheckInAdmissionOperationsView.readiness",
        "GroupArrivalCheckInAdmissionOperationsView.issues"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Single Group Check-In”, “Batch Check-In”, “Individual Check-In”, “Group Arrives”, “Handle”, “Integration”.",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 29 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The group arrival check-in list.",
   "error": "Could not load. Names which read failed and leaves the group arrival check-in untouched.",
   "emptyFirstRun": "No group arrival check-in yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the group arrival check-in are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listGroupArrivalCheck",
    "contract": "orders",
    "purpose": "Group Arrival, Check-In & Admission Operations",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "GroupArrivalCheckInAdmissionOperationsView.groupsExpectedToday",
    "GroupArrivalCheckInAdmissionOperationsView.arrivalTime",
    "GroupArrivalCheckInAdmissionOperationsView.actualArrival",
    "GroupArrivalCheckInAdmissionOperationsView.groupSize",
    "GroupArrivalCheckInAdmissionOperationsView.checkedIn",
    "GroupArrivalCheckInAdmissionOperationsView.remaining"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-280"
  },
  "apisNote": "Regenerated 9 September 2026 from Group_Sales___Corporate_Booking_Management_Reference.pdf page 29. 10 of 10 labels bound to a contract property; 16 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-281",
  "name": "Group Amendments, Cancellation & Refund Operations",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Group_Sales___Corporate_Booking_Management_Reference.pdf",
   "board": "2",
   "number": "9.2.8",
   "page": 30
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/group-amendments-cancellation-refund-operations-bo-281",
   "component": "apps/venue-management-web/src/routes/sell/GroupAmendmentsCancellationRefundOperations.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-274"
   ],
   "exitTo": [
    "BO-274"
   ],
   "inferred": false,
   "notes": "**Reached from BO-274, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-274",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F137 step 14→15",
     "operation": "listGroupAmendmentCancellation"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Manage changes occurring after group confirmation.",
  "purposeNote": "Post-confirmation changes update all affected commercial, capacity, resource, ticketing and operational records through one governed amendment process.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 9 actions on this screen and the screen declares 1 operation.** Unserved: Increase Guest Count, Reduce Guest Count, Date Change, Time Change, Product Change, Package Change, Seat Change, Catering Change …. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 30 §Support"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 30"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 30"
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
       "label": "Increase Guest Count",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 30 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Reduce Guest Count",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 30 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Date Change",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 30 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Time Change",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 30 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Product Change",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 30 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Package Change",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 30 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Seat Change",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 30 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Catering Change",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 30 §Support"
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
   "loading": "The group amendments cancellation list.",
   "error": "Could not load. Names which read failed and leaves the group amendments cancellation untouched.",
   "emptyFirstRun": "No group amendments cancellation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the group amendments cancellation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listGroupAmendmentCancellation",
    "contract": "orders",
    "purpose": "Group Amendments, Cancellation & Refund Operations",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "GroupAmendmentsCancellationRefundOperationsView.increaseGuestCount",
    "GroupAmendmentsCancellationRefundOperationsView.reduceGuestCount",
    "GroupAmendmentsCancellationRefundOperationsView.dateChange",
    "GroupAmendmentsCancellationRefundOperationsView.timeChange",
    "GroupAmendmentsCancellationRefundOperationsView.productChange"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-281"
  },
  "apisNote": "Regenerated 9 September 2026 from Group_Sales___Corporate_Booking_Management_Reference.pdf page 30. 0 of 0 labels bound to a contract property; 9 of 36 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-282",
  "name": "Group Booking Reconciliation, Closure & Performance",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Group_Sales___Corporate_Booking_Management_Reference.pdf",
   "board": "2",
   "number": "9.2.9",
   "page": 31
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/group-booking-reconciliation-closure-performance-bo-282",
   "component": "apps/venue-management-web/src/routes/sell/GroupBookingReconciliationClosurePerformance.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-274"
   ],
   "exitTo": [
    "BO-274"
   ],
   "inferred": false,
   "notes": "**Reached from BO-274, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-274",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F137 step 16→17",
     "operation": "listGroupBookingReconciliation"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Measure; Display) and no metric row",
  "purpose": "Close the group booking after the visit and reconcile what was sold against what actually occurred.",
  "purposeNote": "A group booking cannot be considered fully closed until operational and financial activity has been reconciled.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every group booking reconciliation",
       "columns": [
        "GroupBookingReconciliationClosurePerformanceView.ty",
        "GroupBookingReconciliationClosurePerformanceView.finalBookingValue",
        "GroupBookingReconciliationClosurePerformanceView.amountPaid",
        "GroupBookingReconciliationClosurePerformanceView.refunds",
        "GroupBookingReconciliationClosurePerformanceView.additionalCharges",
        "GroupBookingReconciliationClosurePerformanceView.outstandingBalance",
        "GroupBookingReconciliationClosurePerformanceView.finalRevenue"
       ],
       "bindsTo": "GroupBookingReconciliationClosurePerformanceView",
       "operation": "listGroupBookingReconciliation",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 31 §Measure"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected group booking reconciliation",
       "bindsTo": "GroupBookingReconciliationClosurePerformanceView",
       "columns": [
        "GroupBookingReconciliationClosurePerformanceView.ty",
        "GroupBookingReconciliationClosurePerformanceView.finalBookingValue",
        "GroupBookingReconciliationClosurePerformanceView.amountPaid",
        "GroupBookingReconciliationClosurePerformanceView.refunds",
        "GroupBookingReconciliationClosurePerformanceView.additionalCharges",
        "GroupBookingReconciliationClosurePerformanceView.outstandingBalance",
        "GroupBookingReconciliationClosurePerformanceView.finalRevenue"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Quoted”, “Booked”, “Paid”, “Allocated”, “Issued”, “Attended”.",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 31 §Measure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The group booking reconciliation list.",
   "error": "Could not load. Names which read failed and leaves the group booking reconciliation untouched.",
   "emptyFirstRun": "No group booking reconciliation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the group booking reconciliation are still there. The pack's own statuses are Operationally Complete → Financially Complete → Closed — the state names which is selected.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listGroupBookingReconciliation",
    "contract": "orders",
    "purpose": "Group Booking Reconciliation, Closure & Performance",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "GroupBookingReconciliationClosurePerformanceView.ty",
    "GroupBookingReconciliationClosurePerformanceView.finalBookingValue",
    "GroupBookingReconciliationClosurePerformanceView.amountPaid",
    "GroupBookingReconciliationClosurePerformanceView.refunds",
    "GroupBookingReconciliationClosurePerformanceView.additionalCharges",
    "GroupBookingReconciliationClosurePerformanceView.outstandingBalance"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-282"
  },
  "apisNote": "Regenerated 9 September 2026 from Group_Sales___Corporate_Booking_Management_Reference.pdf page 31. 7 of 7 labels bound to a contract property; 14 of 37 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-283",
  "name": "Group Sales Analytics & AI Intelligence Center",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Group_Sales___Corporate_Booking_Management_Reference.pdf",
   "board": "2",
   "number": "9.2.10",
   "page": 33
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/group-sales-analytics-ai-intelligence-center-bo-283",
   "component": "apps/venue-management-web/src/routes/sell/GroupSalesAnalyticsAiIntelligenceCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-274"
   ],
   "exitTo": [
    "BO-274"
   ],
   "inferred": false,
   "notes": "**Reached from BO-274, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation."
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Analyze) and no metric row",
  "purpose": "Provide management with intelligence across the complete group-sales lifecycle. This should combine data from Board 1 + Board 2.",
  "purposeNote": "Management can analyze group-sales performance and use explainable AI recommendations to improve conversion, utilization, revenue and operational planning. Board 2 — Final Screen Register",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search group sales analytics",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 33 §Filter by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Customer Type",
        "Organization",
        "Venue",
        "Event",
        "Sales Owner",
        "Group Type",
        "Product",
        "Date",
        "Campaign",
        "Market"
       ],
       "notes": "The pack filters this screen by customer type, organization, venue, event, sales owner, group type and 4 more — which are present is a decision the pack already made.",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 33 §Filter by"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every group sales analytics",
       "columns": [
        "GroupSalesAnalyticsAiIntelligenceCenterView.enquiries",
        "GroupSalesAnalyticsAiIntelligenceCenterView.quotes",
        "GroupSalesAnalyticsAiIntelligenceCenterView.conversionRate",
        "GroupSalesAnalyticsAiIntelligenceCenterView.groupBookings",
        "GroupSalesAnalyticsAiIntelligenceCenterView.guests",
        "GroupSalesAnalyticsAiIntelligenceCenterView.revenue",
        "GroupSalesAnalyticsAiIntelligenceCenterView.averageGroupSize",
        "GroupSalesAnalyticsAiIntelligenceCenterView.averageBookingValue",
        "GroupSalesAnalyticsAiIntelligenceCenterView.discount",
        "GroupSalesAnalyticsAiIntelligenceCenterView.revenuePerGuest",
        "GroupSalesAnalyticsAiIntelligenceCenterView.cancellationRate",
        "GroupSalesAnalyticsAiIntelligenceCenterView.noShowRate",
        "GroupSalesAnalyticsAiIntelligenceCenterView.outstandingReceivables",
        "GroupSalesAnalyticsAiIntelligenceCenterView.repeatCustomerRate"
       ],
       "bindsTo": "GroupSalesAnalyticsAiIntelligenceCenterView",
       "operation": "listGroupSale2",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 33 §Analyze"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected group sales analytics",
       "bindsTo": "GroupSalesAnalyticsAiIntelligenceCenterView",
       "columns": [
        "GroupSalesAnalyticsAiIntelligenceCenterView.enquiries",
        "GroupSalesAnalyticsAiIntelligenceCenterView.quotes",
        "GroupSalesAnalyticsAiIntelligenceCenterView.conversionRate",
        "GroupSalesAnalyticsAiIntelligenceCenterView.groupBookings",
        "GroupSalesAnalyticsAiIntelligenceCenterView.guests",
        "GroupSalesAnalyticsAiIntelligenceCenterView.revenue",
        "GroupSalesAnalyticsAiIntelligenceCenterView.averageGroupSize",
        "GroupSalesAnalyticsAiIntelligenceCenterView.averageBookingValue",
        "GroupSalesAnalyticsAiIntelligenceCenterView.discount",
        "GroupSalesAnalyticsAiIntelligenceCenterView.revenuePerGuest",
        "GroupSalesAnalyticsAiIntelligenceCenterView.cancellationRate",
        "GroupSalesAnalyticsAiIntelligenceCenterView.noShowRate",
        "GroupSalesAnalyticsAiIntelligenceCenterView.outstandingReceivables",
        "GroupSalesAnalyticsAiIntelligenceCenterView.repeatCustomerRate"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Visualize”, “Conversion Insight”, “Pricing Insight”, “Capacity Insight”, “Operational Insight”, “Natural-Language Copilot”.",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 33 §Analyze"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The group sales analytics list.",
   "error": "Could not load. Names which read failed and leaves the group sales analytics untouched.",
   "emptyFirstRun": "No group sales analytics yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the group sales analytics are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listGroupSale2",
    "contract": "orders",
    "purpose": "Group Sales Analytics & AI Intelligence Center",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "GroupSalesAnalyticsAiIntelligenceCenterView.enquiries",
    "GroupSalesAnalyticsAiIntelligenceCenterView.quotes",
    "GroupSalesAnalyticsAiIntelligenceCenterView.conversionRate",
    "GroupSalesAnalyticsAiIntelligenceCenterView.groupBookings",
    "GroupSalesAnalyticsAiIntelligenceCenterView.guests",
    "GroupSalesAnalyticsAiIntelligenceCenterView.revenue"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-283"
  },
  "apisNote": "Regenerated 9 September 2026 from Group_Sales___Corporate_Booking_Management_Reference.pdf page 33. 14 of 24 labels bound to a contract property; 24 of 99 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "listGroupAmendmentCancellation": {
  "method": "GET",
  "path": "/group-amendment-cancellation",
  "contract": "orders",
  "summary": "Group Amendments, Cancellation & Refund Operations",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "GroupAmendmentsCancellationRefundOperationsView"
 },
 "listGroupArrivalCheck": {
  "method": "GET",
  "path": "/group-arrival-check",
  "contract": "orders",
  "summary": "Group Arrival, Check-In & Admission Operations",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "GroupArrivalCheckInAdmissionOperationsView"
 },
 "listGroupBooking": {
  "method": "GET",
  "path": "/group-booking",
  "contract": "orders",
  "summary": "Group Booking Operations Command Center",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "GroupBookingOperationsCommandCenterView"
 },
 "listGroupBookingReconciliation": {
  "method": "GET",
  "path": "/group-booking-reconciliation",
  "contract": "orders",
  "summary": "Group Booking Reconciliation, Closure & Performance",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "GroupBookingReconciliationClosurePerformanceView"
 },
 "listGroupPaymentDeposit": {
  "method": "GET",
  "path": "/group-payment-deposit",
  "contract": "orders",
  "summary": "Group Payment, Deposit & Balance Management",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "GroupPaymentDepositBalanceManagementView"
 },
 "listGroupSale2": {
  "method": "GET",
  "path": "/group-sale-2",
  "contract": "orders",
  "summary": "Group Sales Analytics & AI Intelligence Center",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "customerType",
    "in": "query",
    "required": false
   },
   {
    "name": "organization",
    "in": "query",
    "required": false
   },
   {
    "name": "venue",
    "in": "query",
    "required": false
   },
   {
    "name": "event",
    "in": "query",
    "required": false
   },
   {
    "name": "salesOwner",
    "in": "query",
    "required": false
   },
   {
    "name": "groupType",
    "in": "query",
    "required": false
   },
   {
    "name": "product",
    "in": "query",
    "required": false
   },
   {
    "name": "date",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "GroupSalesAnalyticsAiIntelligenceCenterView"
 },
 "listGroupTicketFulfillment": {
  "method": "GET",
  "path": "/group-ticket-fulfillment",
  "contract": "orders",
  "summary": "Group Ticket Fulfillment & Distribution",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "GroupTicketFulfillmentDistributionView"
 },
 "listGroupTicketSeat": {
  "method": "GET",
  "path": "/group-ticket-seat",
  "contract": "orders",
  "summary": "Group Ticket, Seat & Entitlement Allocation",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "GroupTicketSeatEntitlementAllocationView"
 },
 "listParticipantGuestList": {
  "method": "GET",
  "path": "/participant-guest-list",
  "contract": "orders",
  "summary": "Participants, Guest Lists & Group Structure",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ParticipantsGuestListsGroupStructureView"
 },
 "setGroupOperationalPlanning": {
  "method": "PUT",
  "path": "/group-operational-planning",
  "contract": "orders",
  "summary": "Group Operational Planning & Task Workspace",
  "permission": "ORDER_CREATE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "GroupOperationalPlanningTaskWorkspaceInput",
  "responds": "GroupOperationalPlanningTaskWorkspaceView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "GroupAmendmentsCancellationRefundOperationsView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Group Amendments, Cancellation & Refund Operations displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "increaseGuestCount": {
    "type": "integer",
    "description": "Increase Guest Count"
   },
   "reduceGuestCount": {
    "type": "integer",
    "description": "Reduce Guest Count"
   },
   "dateChange": {
    "type": "string",
    "format": "date-time",
    "description": "Date Change"
   },
   "timeChange": {
    "type": "string",
    "format": "date-time",
    "description": "Time Change"
   },
   "productChange": {
    "type": "string",
    "description": "Product Change"
   },
   "packageChange": {
    "type": "string",
    "description": "Package Change"
   },
   "seatChange": {
    "type": "string",
    "description": "Seat Change"
   },
   "cateringChange": {
    "type": "string",
    "description": "Catering Change"
   },
   "resourceChange": {
    "type": "string",
    "description": "Resource Change"
   },
   "fullCancellation": {
    "type": "string",
    "description": "Full Cancellation"
   },
   "partialCancellation": {
    "type": "string",
    "description": "Partial Cancellation"
   },
   "originalValue": {
    "type": "string",
    "description": "Original Value"
   },
   "newValue": {
    "type": "integer",
    "description": "New Value"
   },
   "additionalCharge": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Additional Charge"
   },
   "refundCredit": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Refund/Credit"
   },
   "fees": {
    "type": "string",
    "description": "Fees"
   },
   "ticketsAdded": {
    "type": "string",
    "description": "Tickets added"
   },
   "ticketsReleased": {
    "type": "string",
    "description": "Tickets released"
   },
   "seatsAffected": {
    "type": "integer",
    "description": "Seats affected"
   },
   "guides": {
    "type": "string",
    "description": "Guides"
   },
   "catering": {
    "type": "string",
    "description": "Catering"
   },
   "rooms": {
    "type": "string",
    "description": "Rooms"
   },
   "equipment": {
    "type": "string",
    "description": "Equipment"
   },
   "tasks": {
    "type": "string",
    "description": "Tasks"
   },
   "tickets": {
    "type": "string",
    "description": "Tickets"
   },
   "guestLists": {
    "type": "string",
    "description": "Guest lists"
   },
   "lateCancellation": {
    "type": "string",
    "description": "Late cancellation"
   },
   "waivedFee": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Waived fee"
   },
   "largeRefund": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Large refund"
   },
   "capacityOverride": {
    "type": "integer",
    "description": "Capacity override"
   },
   "contractException": {
    "type": "string",
    "description": "Contract exception"
   }
  }
 },
 "GroupArrivalCheckInAdmissionOperationsView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Group Arrival, Check-In & Admission Operations displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "groupsExpectedToday": {
    "type": "string",
    "description": "Groups Expected Today"
   },
   "arrivalTime": {
    "type": "string",
    "format": "date-time",
    "description": "Arrival Time"
   },
   "actualArrival": {
    "type": "string",
    "description": "Actual Arrival"
   },
   "groupSize": {
    "type": "string",
    "description": "Group Size"
   },
   "checkedIn": {
    "type": "string",
    "description": "Checked In"
   },
   "remaining": {
    "type": "string",
    "description": "Remaining"
   },
   "gate": {
    "type": "string",
    "description": "Gate"
   },
   "groupLeader": {
    "type": "string",
    "description": "Group Leader"
   },
   "readiness": {
    "type": "string",
    "description": "Readiness"
   },
   "issues": {
    "type": "integer",
    "description": "Issues"
   },
   "eachCredentialScannedIndividually": {
    "type": "string",
    "description": "Each credential scanned individually"
   },
   "booked": {
    "type": "string",
    "description": "Booked"
   },
   "expected": {
    "type": "string",
    "description": "Expected"
   },
   "arrived": {
    "type": "string",
    "description": "Arrived"
   },
   "noShow": {
    "type": "string",
    "description": "No-Show"
   },
   "additionalGuests": {
    "type": "string",
    "description": "Additional Guests"
   },
   "staffLeaders": {
    "type": "string",
    "description": "Staff/Leaders"
   },
   "missingGuest": {
    "type": "string",
    "description": "Missing guest"
   },
   "extraGuest": {
    "type": "string",
    "description": "Extra guest"
   },
   "invalidTicket": {
    "type": "string",
    "description": "Invalid ticket"
   },
   "wrongDate": {
    "type": "string",
    "format": "date-time",
    "description": "Wrong date"
   },
   "lateArrival": {
    "type": "string",
    "description": "Late arrival"
   },
   "paymentHold": {
    "type": "string",
    "description": "Payment hold"
   },
   "missingCredential": {
    "type": "string",
    "description": "Missing credential"
   },
   "accessibilityRequirement": {
    "type": "string",
    "description": "Accessibility requirement"
   }
  }
 },
 "GroupBookingOperationsCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Group Booking Operations Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "upcomingGroups": {
    "type": "integer",
    "description": "Upcoming Groups"
   },
   "groupsToday": {
    "type": "string",
    "description": "Groups Today"
   },
   "expectedGuestsToday": {
    "type": "string",
    "description": "Expected Guests Today"
   },
   "groupsAwaitingDeposit": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Groups Awaiting Deposit"
   },
   "guestListsPending": {
    "type": "integer",
    "description": "Guest Lists Pending"
   },
   "ticketsPending": {
    "type": "integer",
    "description": "Tickets Pending"
   },
   "resourcesPending": {
    "type": "integer",
    "description": "Resources Pending"
   },
   "groupsReady": {
    "type": "string",
    "description": "Groups Ready"
   },
   "groupsWithIssues": {
    "type": "integer",
    "description": "Groups With Issues"
   },
   "outstandingPayments": {
    "type": "integer",
    "description": "Outstanding Payments"
   },
   "checkInsToday": {
    "type": "string",
    "description": "Check-Ins Today"
   },
   "completedGroups": {
    "type": "integer",
    "description": "Completed Groups"
   },
   "groupBookingId": {
    "type": "string",
    "description": "Group Booking ID"
   },
   "organization": {
    "type": "string",
    "description": "Organization"
   },
   "groupType": {
    "type": "string",
    "description": "Group Type"
   },
   "venueEvent": {
    "type": "string",
    "description": "Venue/Event"
   },
   "visitDate": {
    "type": "string",
    "format": "date-time",
    "description": "Visit Date"
   },
   "arrivalTime": {
    "type": "string",
    "format": "date-time",
    "description": "Arrival Time"
   },
   "guests": {
    "type": "integer",
    "description": "Guests"
   },
   "bookingValue": {
    "type": "string",
    "description": "Booking Value"
   },
   "paymentStatus": {
    "type": "integer",
    "description": "Payment Status"
   },
   "guestListStatus": {
    "type": "integer",
    "description": "Guest List Status"
   },
   "ticketStatus": {
    "type": "integer",
    "description": "Ticket Status"
   },
   "resourceStatus": {
    "type": "integer",
    "description": "Resource Status"
   },
   "readiness": {
    "type": "number",
    "description": "Readiness %"
   },
   "operationalOwner": {
    "type": "string",
    "description": "Operational Owner"
   }
  }
 },
 "GroupBookingReconciliationClosurePerformanceView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Group Booking Reconciliation, Closure & Performance displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "ty": {
    "type": "string",
    "description": "ty"
   },
   "finalGuest": {
    "type": "string",
    "description": "Final Guest (the pack shows 414)"
   },
   "tickets": {
    "type": "integer",
    "description": "Tickets (the pack shows 414)"
   },
   "finalBookingValue": {
    "type": "string",
    "description": "Final Booking Value"
   },
   "amountPaid": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Amount Paid"
   },
   "refunds": {
    "type": "integer",
    "description": "Refunds"
   },
   "additionalCharges": {
    "type": "integer",
    "description": "Additional Charges"
   },
   "outstandingBalance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Outstanding Balance"
   },
   "finalRevenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Final Revenue"
   },
   "mealsBookedVsRedeemed": {
    "type": "string",
    "description": "Meals booked vs redeemed"
   },
   "workshopsBookedVsAttended": {
    "type": "string",
    "description": "Workshops booked vs attended"
   },
   "parkingUsed": {
    "type": "string",
    "description": "Parking used"
   },
   "merchandiseFulfilled": {
    "type": "string",
    "description": "Merchandise fulfilled"
   },
   "resourcesConsumed": {
    "type": "string",
    "description": "Resources consumed"
   },
   "admissionReconciled": {
    "type": "string",
    "description": "Admission reconciled"
   },
   "financeReconciled": {
    "type": "string",
    "description": "Finance reconciled"
   },
   "refundsResolved": {
    "type": "string",
    "description": "Refunds resolved"
   },
   "resourcesClosed": {
    "type": "integer",
    "description": "Resources closed"
   },
   "customerFeedbackCapturedWhereApplicable": {
    "type": "string",
    "description": "Customer feedback captured where applicable"
   },
   "attendance": {
    "type": "integer",
    "description": "Attendance %"
   },
   "noShow": {
    "type": "number",
    "description": "No-Show %"
   },
   "revenuePerGuest": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue per Guest"
   },
   "packageAttachment": {
    "type": "string",
    "description": "Package Attachment"
   },
   "operationalIssues": {
    "type": "string",
    "description": "Operational Issues"
   },
   "customerSatisfactionWhereAvailable": {
    "type": "string",
    "description": "Customer Satisfaction where available"
   }
  }
 },
 "GroupOperationalPlanningTaskWorkspaceInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table covers these fields** — the closest is catalogue.price_list at 3%, so this is not an update to anything the package stores today and no new table has been decided",
  "description": "**What Group Operational Planning & Task Workspace submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.\n\n**The pack defines this as a record**, under *Each task should contain* - one of only 13 drafted writes that does. That is the client writing a row rather than a screen, and it is where the table conversation should start.",
  "properties": {
   "arrivalDate": {
    "type": "string",
    "format": "date-time",
    "description": "Arrival Date"
   },
   "arrivalTime": {
    "type": "string",
    "format": "date-time",
    "description": "Arrival Time"
   },
   "arrivalLocation": {
    "type": "string",
    "description": "Arrival Location"
   },
   "groupMeetingPoint": {
    "type": "string",
    "description": "Group Meeting Point"
   },
   "entryGate": {
    "type": "string",
    "description": "Entry Gate"
   },
   "departureTime": {
    "type": "string",
    "format": "date-time",
    "description": "Departure Time"
   },
   "groupSize": {
    "type": "string",
    "description": "Group Size"
   },
   "groupLeaders": {
    "type": "string",
    "description": "Group Leaders"
   },
   "contactPerson": {
    "type": "string",
    "description": "Contact Person"
   },
   "ticketingMethod": {
    "type": "string",
    "description": "Ticketing Method"
   },
   "seating": {
    "type": "string",
    "description": "Seating"
   },
   "guides": {
    "type": "string",
    "description": "Guides"
   },
   "catering": {
    "type": "string",
    "description": "Catering"
   },
   "transportation": {
    "type": "string",
    "description": "Transportation"
   },
   "parking": {
    "type": "string",
    "description": "Parking"
   },
   "accessibility": {
    "type": "string",
    "description": "Accessibility"
   },
   "equipment": {
    "type": "string",
    "description": "Equipment"
   },
   "specialRequirements": {
    "type": "string",
    "description": "Special Requirements"
   },
   "prepareGroupEntry": {
    "type": "string",
    "description": "Prepare group entry"
   },
   "prepareCredentials": {
    "type": "string",
    "description": "Prepare credentials"
   },
   "confirmMealQuantities": {
    "type": "string",
    "description": "Confirm meal quantities"
   },
   "groupArrivalAwareness": {
    "type": "string",
    "description": "Group arrival awareness"
   },
   "confirmPayment": {
    "type": "string",
    "description": "Confirm payment"
   },
   "task": {
    "type": "string",
    "description": "Task"
   },
   "department": {
    "type": "string",
    "description": "Department"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   },
   "dueDate": {
    "type": "string",
    "format": "date-time",
    "description": "Due Date"
   },
   "dueTime": {
    "type": "string",
    "format": "date-time",
    "description": "Due Time"
   },
   "priority": {
    "type": "string",
    "description": "Priority"
   },
   "dependency": {
    "type": "string",
    "description": "Dependency"
   },
   "status": {
    "type": "string",
    "description": "Status"
   },
   "notes": {
    "type": "string",
    "description": "Notes"
   }
  },
  "x-ticvai-record-definition": "Each task should contain"
 },
 "GroupOperationalPlanningTaskWorkspaceView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Group Operational Planning & Task Workspace displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "arrivalDate": {
    "type": "string",
    "format": "date-time",
    "description": "Arrival Date"
   },
   "arrivalTime": {
    "type": "string",
    "format": "date-time",
    "description": "Arrival Time"
   },
   "arrivalLocation": {
    "type": "string",
    "description": "Arrival Location"
   },
   "groupMeetingPoint": {
    "type": "string",
    "description": "Group Meeting Point"
   },
   "entryGate": {
    "type": "string",
    "description": "Entry Gate"
   },
   "departureTime": {
    "type": "string",
    "format": "date-time",
    "description": "Departure Time"
   },
   "groupSize": {
    "type": "string",
    "description": "Group Size"
   },
   "groupLeaders": {
    "type": "string",
    "description": "Group Leaders"
   },
   "contactPerson": {
    "type": "string",
    "description": "Contact Person"
   },
   "ticketingMethod": {
    "type": "string",
    "description": "Ticketing Method"
   },
   "seating": {
    "type": "string",
    "description": "Seating"
   },
   "guides": {
    "type": "string",
    "description": "Guides"
   },
   "catering": {
    "type": "string",
    "description": "Catering"
   },
   "transportation": {
    "type": "string",
    "description": "Transportation"
   },
   "parking": {
    "type": "string",
    "description": "Parking"
   },
   "accessibility": {
    "type": "string",
    "description": "Accessibility"
   },
   "equipment": {
    "type": "string",
    "description": "Equipment"
   },
   "specialRequirements": {
    "type": "string",
    "description": "Special Requirements"
   },
   "prepareGroupEntry": {
    "type": "string",
    "description": "Prepare group entry"
   },
   "prepareCredentials": {
    "type": "string",
    "description": "Prepare credentials"
   },
   "confirmMealQuantities": {
    "type": "string",
    "description": "Confirm meal quantities"
   },
   "groupArrivalAwareness": {
    "type": "string",
    "description": "Group arrival awareness"
   },
   "confirmPayment": {
    "type": "string",
    "description": "Confirm payment"
   },
   "task": {
    "type": "string",
    "description": "Task"
   },
   "department": {
    "type": "string",
    "description": "Department"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   },
   "dueDate": {
    "type": "string",
    "format": "date-time",
    "description": "Due Date"
   },
   "dueTime": {
    "type": "string",
    "format": "date-time",
    "description": "Due Time"
   },
   "priority": {
    "type": "string",
    "description": "Priority"
   },
   "dependency": {
    "type": "string",
    "description": "Dependency"
   },
   "status": {
    "type": "string",
    "description": "Status"
   },
   "notes": {
    "type": "string",
    "description": "Notes"
   }
  }
 },
 "GroupPaymentDepositBalanceManagementView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Group Payment, Deposit & Balance Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "bookingValue": {
    "type": "string",
    "description": "Booking Value"
   },
   "depositRequired": {
    "type": "boolean",
    "description": "Deposit Required"
   },
   "depositPaid": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Deposit Paid"
   },
   "balance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Balance"
   },
   "amountPaid": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Amount Paid"
   },
   "amountOutstanding": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Amount Outstanding"
   },
   "nextDueDate": {
    "type": "string",
    "format": "date-time",
    "description": "Next Due Date"
   },
   "paymentStatus": {
    "type": "integer",
    "description": "Payment Status"
   },
   "deposit": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Deposit"
   },
   "milestonePayment": {
    "type": "string",
    "description": "Milestone Payment"
   },
   "installment": {
    "type": "string",
    "description": "Installment"
   },
   "finalBalance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Final Balance"
   },
   "customSchedule": {
    "type": "string",
    "description": "Custom Schedule"
   },
   "consumeTicvaiPaymentFinanceCapabilities": {
    "type": "string",
    "description": "Consume TICVAI Payment/Finance capabilities"
   },
   "paymentLink": {
    "type": "string",
    "description": "Payment Link"
   },
   "card": {
    "type": "string",
    "description": "Card"
   },
   "bankTransfer": {
    "type": "string",
    "description": "Bank Transfer"
   },
   "accountCredit": {
    "type": "string",
    "description": "Account Credit"
   },
   "cashWherePermitted": {
    "type": "string",
    "description": "Cash where permitted"
   },
   "otherApprovedMethod": {
    "type": "string",
    "description": "Other approved method"
   },
   "placeBookingOnPaymentHold": {
    "type": "string",
    "description": "Place booking on payment hold"
   },
   "preventTicketRelease": {
    "type": "string",
    "description": "Prevent ticket release"
   }
  }
 },
 "GroupSalesAnalyticsAiIntelligenceCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Group Sales Analytics & AI Intelligence Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "enquiries": {
    "type": "string",
    "description": "Enquiries"
   },
   "quotes": {
    "type": "string",
    "description": "Quotes"
   },
   "conversionRate": {
    "type": "number",
    "description": "Conversion Rate"
   },
   "groupBookings": {
    "type": "string",
    "description": "Group Bookings"
   },
   "guests": {
    "type": "string",
    "description": "Guests"
   },
   "revenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue"
   },
   "averageGroupSize": {
    "type": "number",
    "description": "Average Group Size"
   },
   "averageBookingValue": {
    "type": "number",
    "description": "Average Booking Value"
   },
   "discount": {
    "type": "number",
    "description": "Discount %"
   },
   "revenuePerGuest": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue per Guest"
   },
   "cancellationRate": {
    "type": "number",
    "description": "Cancellation Rate"
   },
   "noShowRate": {
    "type": "number",
    "description": "No-Show Rate"
   },
   "outstandingReceivables": {
    "type": "string",
    "description": "Outstanding Receivables"
   },
   "repeatCustomerRate": {
    "type": "number",
    "description": "Repeat Customer Rate"
   },
   "reconciliation": {
    "type": "string",
    "description": "reconciliation"
   },
   "resourceManagementAndAccessControl": {
    "type": "string",
    "description": "Resource Management and Access Control"
   },
   "showConversionAtEachStage": {
    "type": "number",
    "description": "Show conversion at each stage"
   },
   "afterOneDay": {
    "type": "string",
    "description": "after one day"
   },
   "affectingB2cDemand": {
    "type": "string",
    "description": "affecting B2C demand"
   },
   "toMateriallyIncreaseConversion": {
    "type": "number",
    "description": "to materially increase conversion"
   },
   "additionalGroups": {
    "type": "string",
    "description": "Additional groups"
   },
   "capacityUtilization": {
    "type": "integer",
    "description": "Capacity utilization"
   },
   "discountCost": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Discount cost"
   },
   "expectedContribution": {
    "type": "string",
    "description": "Expected contribution"
   },
   "prices": {
    "type": "string",
    "description": "Prices"
   },
   "discounts": {
    "type": "string",
    "description": "Discounts"
   },
   "capacity": {
    "type": "integer",
    "description": "Capacity"
   },
   "customerTerms": {
    "type": "string",
    "description": "Customer terms"
   },
   "management": {
    "type": "string",
    "description": "management"
   },
   "area9CompleteArchitecture": {
    "type": "string",
    "description": "Area 9 — Complete Architecture"
   }
  }
 },
 "GroupTicketFulfillmentDistributionView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Group Ticket Fulfillment & Distribution displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "oneGroupQr": {
    "type": "string",
    "description": "One Group QR"
   },
   "individualQr": {
    "type": "string",
    "description": "Individual QR"
   },
   "groupLeaderWallet": {
    "type": "string",
    "description": "Group Leader Wallet"
   },
   "individualMobileTickets": {
    "type": "string",
    "description": "Individual Mobile Tickets"
   },
   "email": {
    "type": "string",
    "description": "Email"
   },
   "posPrint": {
    "type": "string",
    "description": "POS Print"
   },
   "rfid": {
    "type": "string",
    "description": "RFID"
   },
   "nfc": {
    "type": "string",
    "description": "NFC"
   },
   "wristband": {
    "type": "string",
    "description": "Wristband"
   },
   "physicalCollection": {
    "type": "string",
    "description": "Physical Collection"
   },
   "eachParticipantReceivesTheirCredential": {
    "type": "string",
    "description": "Each participant receives their credential"
   },
   "ticketsDistributedToTeachersTeamLeaders": {
    "type": "string",
    "description": "Tickets distributed to teachers/team leaders"
   },
   "ticketsRequired": {
    "type": "boolean",
    "description": "Tickets Required"
   },
   "generated": {
    "type": "string",
    "description": "Generated"
   },
   "sent": {
    "type": "string",
    "description": "Sent"
   },
   "delivered": {
    "type": "string",
    "description": "Delivered"
   },
   "opened": {
    "type": "string",
    "description": "Opened"
   },
   "downloaded": {
    "type": "string",
    "description": "Downloaded"
   },
   "failed": {
    "type": "integer",
    "description": "Failed"
   },
   "reissued": {
    "type": "string",
    "description": "Reissued"
   },
   "changeDeliveryMethod": {
    "type": "string",
    "description": "Change Delivery Method"
   },
   "guest": {
    "type": "string",
    "description": "Guest"
   },
   "ticket": {
    "type": "string",
    "description": "Ticket"
   },
   "seat": {
    "type": "string",
    "description": "Seat"
   },
   "credential": {
    "type": "string",
    "description": "Credential"
   },
   "entitlements": {
    "type": "string",
    "description": "Entitlements"
   },
   "checkInStatus": {
    "type": "string",
    "description": "Check-In Status"
   },
   "services": {
    "type": "string",
    "description": "services"
   }
  }
 },
 "GroupTicketSeatEntitlementAllocationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Group Ticket, Seat & Entitlement Allocation displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "individualTicket": {
    "type": "string",
    "description": "Individual Ticket"
   },
   "bulkTicket": {
    "type": "string",
    "description": "Bulk Ticket"
   },
   "groupCredential": {
    "type": "string",
    "description": "Group Credential"
   },
   "namedTicket": {
    "type": "string",
    "description": "Named Ticket"
   },
   "quantityBasedTicket": {
    "type": "integer",
    "description": "Quantity-Based Ticket"
   },
   "reservedSeat": {
    "type": "string",
    "description": "Reserved Seat"
   },
   "generalAdmission": {
    "type": "string",
    "description": "General Admission"
   },
   "zoneAllocation": {
    "type": "string",
    "description": "Zone Allocation"
   },
   "keepGroupTogether": {
    "type": "string",
    "description": "Keep group together"
   },
   "accessibleSeats": {
    "type": "integer",
    "description": "Accessible seats"
   },
   "teacherLeaderAdjacentSeating": {
    "type": "string",
    "description": "Teacher/leader adjacent seating"
   },
   "vipAllocation": {
    "type": "string",
    "description": "VIP allocation"
   },
   "companionSeats": {
    "type": "integer",
    "description": "Companion seats"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "quantityBooked": {
    "type": "integer",
    "description": "Quantity Booked"
   },
   "quantityAllocated": {
    "type": "integer",
    "description": "Quantity Allocated"
   },
   "remaining": {
    "type": "string",
    "description": "Remaining"
   },
   "ticketType": {
    "type": "string",
    "description": "Ticket Type"
   },
   "seatZone": {
    "type": "string",
    "description": "Seat/Zone"
   },
   "guestSubgroup": {
    "type": "string",
    "description": "Guest/Subgroup"
   },
   "credentialStatus": {
    "type": "integer",
    "description": "Credential Status"
   },
   "sectionA": {
    "type": "string",
    "description": "Section A"
   },
   "rows1218": {
    "type": "string",
    "description": "Rows 12–18"
   },
   "admission": {
    "type": "string",
    "description": "Admission"
   },
   "meal": {
    "type": "string",
    "description": "Meal"
   },
   "workshop": {
    "type": "string",
    "description": "Workshop"
   },
   "parking": {
    "type": "string",
    "description": "Parking"
   },
   "fastTrack": {
    "type": "string",
    "description": "Fast Track"
   },
   "merchandise": {
    "type": "string",
    "description": "Merchandise"
   },
   "otherPackageComponents": {
    "type": "string",
    "description": "Other package components"
   }
  }
 },
 "ParticipantsGuestListsGroupStructureView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Participants, Guest Lists & Group Structure displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "manualEntry": {
    "type": "string",
    "description": "Manual Entry"
   },
   "csvExcelImport": {
    "type": "string",
    "description": "CSV/Excel Import"
   },
   "customerUpload": {
    "type": "string",
    "description": "Customer Upload"
   },
   "api": {
    "type": "string",
    "description": "API"
   },
   "previousGroupTemplate": {
    "type": "string",
    "description": "Previous Group Template"
   },
   "individualGuestInformationRequired": {
    "type": "boolean",
    "description": "Individual guest information required"
   },
   "firstName": {
    "type": "string",
    "description": "First Name"
   },
   "lastName": {
    "type": "string",
    "format": "date-time",
    "description": "Last Name"
   },
   "guestType": {
    "type": "string",
    "description": "Guest Type"
   },
   "ageDateOfBirthWhereApplicable": {
    "type": "string",
    "format": "date-time",
    "description": "Age/Date of Birth where applicable"
   },
   "ticketCategory": {
    "type": "string",
    "description": "Ticket Category"
   },
   "email": {
    "type": "string",
    "description": "Email"
   },
   "mobile": {
    "type": "string",
    "description": "Mobile"
   },
   "membership": {
    "type": "string",
    "description": "Membership"
   },
   "accessibilityRequirement": {
    "type": "string",
    "description": "Accessibility Requirement"
   },
   "dietaryRequirement": {
    "type": "string",
    "description": "Dietary Requirement"
   },
   "groupSubgroup": {
    "type": "string",
    "description": "Group/Subgroup"
   },
   "seat": {
    "type": "string",
    "description": "Seat"
   },
   "credentialStatus": {
    "type": "string",
    "description": "Credential Status"
   },
   "missingRequiredField": {
    "type": "string",
    "description": "Missing required field"
   },
   "invalidCategory": {
    "type": "string",
    "description": "Invalid category"
   },
   "guestCountMismatch": {
    "type": "integer",
    "description": "Guest count mismatch"
   },
   "ageTicketMismatch": {
    "type": "string",
    "description": "Age/ticket mismatch"
   }
  }
 }
}
```
