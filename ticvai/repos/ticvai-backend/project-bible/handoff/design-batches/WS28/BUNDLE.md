# WS28 — Group Sales   Corporate Booking Management board 2

**10 screens · 18 operations · 27 schemas · 4 permissions**

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

- **Every control that can be refused must be gated.** 4 permissions apply here:
  `ORDER_CREATE, ORDER_MODIFY, ORDER_RESCHEDULE, ORDER_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-274` | Group Booking Operations Command Center | listDetail | 2 | 0 | — |
| `BO-275` | Group Operational Planning & Task Workspace | configEditor | 1 | 0 | — |
| `BO-276` | Participants, Guest Lists & Group Structure | listDetail | 2 | 0 | — |
| `BO-277` | Group Payment, Deposit & Balance Management | listDetail | 2 | 0 | — |
| `BO-278` | Group Ticket, Seat & Entitlement Allocation | listDetail | 2 | 0 | — |
| `BO-279` | Group Ticket Fulfillment & Distribution | listDetail | 2 | 0 | — |
| `BO-280` | Group Arrival, Check-In & Admission Operations | listDetail | 1 | 0 | — |
| `BO-281` | Group Amendments, Cancellation & Refund Operations | listDetail | 4 | 0 | — |
| `BO-282` | Group Booking Reconciliation, Closure & Performance | listDetail | 1 | 0 | — |
| `BO-283` | Group Sales Analytics & AI Intelligence Center | listDetail | 2 | 0 | — |

## Thin screens in this batch

**BO-274, BO-280, BO-282 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

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
     "provenance": "derived — BO-100 declares entryState.params  and BO-274 holds none of them, so the edge carries nothing and BO-100 opens cold"
    },
    {
     "to": "BO-275",
     "trigger": "Works in Group Operational Planning & Task Workspace",
     "provenance": "flow F137 step 1→2",
     "operation": "listGroupBooking"
    },
    {
     "to": "BO-280",
     "trigger": "Works in Group Arrival, Check-In & Admission Operations",
     "provenance": "flow F137 step 11→12",
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
    },
    {
     "to": "BO-276",
     "trigger": "Works in Participants, Guest Lists & Group Structure",
     "provenance": "flow F137 step 3→4",
     "operation": "listGroupBooking",
     "carries": [
      "groupBookingId"
     ]
    },
    {
     "to": "BO-277",
     "trigger": "Works in Group Payment, Deposit & Balance Management",
     "provenance": "flow F137 step 5→6",
     "operation": "listGroupBooking",
     "carries": [
      "groupBookingId"
     ]
    },
    {
     "to": "BO-278",
     "trigger": "Works in Group Ticket, Seat & Entitlement Allocation",
     "provenance": "flow F137 step 7→8",
     "operation": "listGroupBooking",
     "carries": [
      "groupBookingId"
     ]
    },
    {
     "to": "BO-279",
     "trigger": "Works in Group Ticket Fulfillment & Distribution",
     "provenance": "flow F137 step 9→10",
     "operation": "listGroupBooking",
     "carries": [
      "groupBookingId"
     ]
    },
    {
     "to": "BO-281",
     "trigger": "Works in Group Amendments, Cancellation & Refund Operations",
     "provenance": "flow F137 step 13→14",
     "operation": "listGroupBooking",
     "carries": [
      "groupBookingId"
     ]
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Operations can identify every upcoming group, its readiness and outstanding actions from one centralized workspace.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide Operations with a real-time command center for all confirmed and upcoming group bookings.",
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
   },
   {
    "operationId": "listGroupBookingReconciliation",
    "contract": "orders",
    "purpose": "Group Booking Reconciliation, Closure & Performance",
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-274",
   "workshopBoard": "wireframes/WS69 Group Sales   Corporate Booking Management Board 2.dc.html#bo-274"
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
  "purposeNote": "Every confirmed group can be translated into a structured operational plan with owners, deadlines and dependencies.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure/reference) and no display directory — it is settings, not a population",
  "purpose": "Convert the commercial booking into a detailed operational execution plan.",
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
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-275",
   "workshopBoard": "wireframes/WS69 Group Sales   Corporate Booking Management Board 2.dc.html#bo-275"
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
  "purposeNote": "confirmed group quantity.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Detect) and no metric row",
  "purpose": "Manage the people participating in the group where individual information is required.",
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
        "ParticipantsGuestListsGroupStructureView.validationIssues",
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
        "ParticipantsGuestListsGroupStructureView.validationIssues",
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
       "label": "Manual Entry",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 23 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "CSV/Excel Import",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 23 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Customer Upload",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 23 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "API",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 23 §Support"
      },
      {
       "kind": "primaryButton",
       "label": "Save participant list",
       "operation": "setParticipantGuestList",
       "provenance": "contract orders.yaml PUT /group-bookings/{groupBookingId}/participants (decided 29 September, VM close-out)"
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
   },
   {
    "operationId": "setParticipantGuestList",
    "contract": "orders",
    "purpose": "Save participant list",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "groupBookingId",
     "from": "navigation"
    }
   ],
   "preloaded": [
    "Duplicate guest",
    "ParticipantsGuestListsGroupStructureView.validationIssues",
    "Duplicate ticket assignment"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-276",
   "workshopBoard": "wireframes/WS69 Group Sales   Corporate Booking Management Board 2.dc.html#bo-276"
  },
  "apisNote": "Regenerated 9 September 2026 from Group_Sales___Corporate_Booking_Management_Reference.pdf page 23. 4 of 6 labels bound to a contract property; 10 of 38 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** still owed by a contract change: `setParticipantGuestList`.",
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
  "purposeNote": "Sales, Finance and Operations can understand exactly what has been paid, what remains due and whether payment conditions permit fulfillment.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Track the complete payment lifecycle of a group booking.",
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
       "label": "Deposit",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 25 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Milestone Payment",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 25 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Final Balance",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 25 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Custom Schedule",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 25 §Support"
      },
      {
       "kind": "primaryButton",
       "label": "Save payment schedule",
       "operation": "setGroupPaymentSchedule",
       "provenance": "contract orders.yaml PUT /group-bookings/{groupBookingId}/payment-schedule (decided 29 September, VM close-out)"
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
   },
   {
    "operationId": "setGroupPaymentSchedule",
    "contract": "orders",
    "purpose": "Save payment schedule",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "groupBookingId",
     "from": "navigation"
    }
   ],
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-277",
   "workshopBoard": "wireframes/WS69 Group Sales   Corporate Booking Management Board 2.dc.html#bo-277"
  },
  "apisNote": "Regenerated 9 September 2026 from Group_Sales___Corporate_Booking_Management_Reference.pdf page 25. 8 of 8 labels bound to a contract property; 12 of 38 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** still owed by a contract change: `setGroupPaymentSchedule`.",
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
  "purposeNote": "Every confirmed group entitlement can be correctly allocated without creating duplicate capacity or conflicting seat assignments.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Allocate the confirmed group inventory to individual guests, subgroups or quantity blocks.",
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
       "label": "Keep group together",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 26 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "VIP allocation",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 26 §Support"
      },
      {
       "kind": "primaryButton",
       "label": "Save allocation",
       "operation": "setGroupTicketAllocation",
       "provenance": "contract orders.yaml PUT /group-bookings/{groupBookingId}/allocation (decided 29 September, VM close-out)"
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
   },
   {
    "operationId": "setGroupTicketAllocation",
    "contract": "orders",
    "purpose": "Save allocation",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "groupBookingId",
     "from": "navigation"
    }
   ],
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-278",
   "workshopBoard": "wireframes/WS69 Group Sales   Corporate Booking Management Board 2.dc.html#bo-278"
  },
  "apisNote": "Regenerated 9 September 2026 from Group_Sales___Corporate_Booking_Management_Reference.pdf page 26. 8 of 8 labels bound to a contract property; 15 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** still owed by a contract change: `setGroupTicketAllocation`.",
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
  "purposeNote": "maintaining complete ticket-to-guest traceability.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Control how tickets and other credentials are delivered to the group.",
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
       "kind": "primaryButton",
       "label": "POS Print",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 27 §Support",
       "permission": "Print"
      },
      {
       "kind": "secondaryButton",
       "label": "Physical Collection",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 27 §Support"
      },
      {
       "kind": "banner",
       "label": "Permissions this screen separates",
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** Generate Tickets, Send, Resend, Reissue, Change Delivery Method, Revoke where permitted. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Group_Sales___Corporate_Booking_Management_Reference.pdf, page 27 §Authorized users can"
      },
      {
       "kind": "primaryButton",
       "label": "Save fulfilment",
       "operation": "setGroupTicketFulfillment",
       "provenance": "contract orders.yaml PUT /group-bookings/{groupBookingId}/fulfillment (decided 29 September, VM close-out)"
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
   },
   {
    "operationId": "setGroupTicketFulfillment",
    "contract": "orders",
    "purpose": "Save fulfilment",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "groupBookingId",
     "from": "navigation"
    }
   ],
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-279",
   "workshopBoard": "wireframes/WS69 Group Sales   Corporate Booking Management Board 2.dc.html#bo-279"
  },
  "apisNote": "Regenerated 9 September 2026 from Group_Sales___Corporate_Booking_Management_Reference.pdf page 27. 8 of 8 labels bound to a contract property; 17 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** still owed by a contract change: `setGroupTicketFulfillment`.",
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
  "purposeNote": "Operations can process large group arrivals efficiently while preserving accurate admission and headcount records.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Manage the physical arrival and admission of large groups efficiently.",
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-280",
   "workshopBoard": "wireframes/WS69 Group Sales   Corporate Booking Management Board 2.dc.html#bo-280"
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
  "purposeNote": "Post-confirmation changes update all affected commercial, capacity, resource, ticketing and operational records through one governed amendment process.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Manage changes occurring after group confirmation.",
  "gaps": [
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
   },
   {
    "operationId": "updateGroupBooking",
    "contract": "orders",
    "purpose": "Change the group size or package",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration): serves the pack action(s) Increase Guest Count, Reduce Guest Count, Package Change; Date Change, Time Change; Product Change, Seat Change, Catering Change …",
    "invalidates": [
     "listGroupAmendmentCancellation"
    ]
   },
   {
    "operationId": "rescheduleOrder",
    "contract": "orders",
    "purpose": "Move the group order to another date or time",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration): serves the pack action(s) Increase Guest Count, Reduce Guest Count, Package Change; Date Change, Time Change; Product Change, Seat Change, Catering Change …",
    "invalidates": [
     "listGroupAmendmentCancellation"
    ]
   },
   {
    "operationId": "modifyOrder",
    "contract": "orders",
    "purpose": "Swap product, seat or catering lines on the group order",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration): serves the pack action(s) Increase Guest Count, Reduce Guest Count, Package Change; Date Change, Time Change; Product Change, Seat Change, Catering Change …",
    "invalidates": [
     "listGroupAmendmentCancellation"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "groupBookingId",
     "from": "navigation"
    },
    {
     "name": "orderId",
     "from": "navigation"
    }
   ],
   "preloaded": [
    "GroupAmendmentsCancellationRefundOperationsView.amendmentType"
   ],
   "coldEntry": "Opened from BO-274 with the group booking picked there. Opened cold (a bookmark or a refresh), it shows the list to pick from rather than an empty record, and says plainly if the group booking no longer exists."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-281",
   "workshopBoard": "wireframes/WS69 Group Sales   Corporate Booking Management Board 2.dc.html#bo-281"
  },
  "apisNote": "Regenerated 9 September 2026 from Group_Sales___Corporate_Booking_Management_Reference.pdf page 30. 0 of 0 labels bound to a contract property; 9 of 36 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Increase Guest Count, Reduce Guest Count, Package Change: `updateGroupBooking`; Date Change, Time Change: `rescheduleOrder`; Product Change, Seat Change, Catering Change …: `modifyOrder`.",
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
  "purposeNote": "A group booking cannot be considered fully closed until operational and financial activity has been reconciled.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Measure; Display) and no metric row",
  "purpose": "Close the group booking after the visit and reconcile what was sold against what actually occurred.",
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-282",
   "workshopBoard": "wireframes/WS69 Group Sales   Corporate Booking Management Board 2.dc.html#bo-282"
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
  "purposeNote": "Management can analyze group-sales performance and use explainable AI recommendations to improve conversion, utilization, revenue and operational planning. Board 2 — Final Screen Register",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Analyze) and no metric row",
  "purpose": "Provide management with intelligence across the complete group-sales lifecycle. This should combine data from Board 1 + Board 2.",
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
   },
   {
    "operationId": "listGroupSale",
    "contract": "orders",
    "purpose": "Group Sales Command Center",
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-283",
   "workshopBoard": "wireframes/WS69 Group Sales   Corporate Booking Management Board 2.dc.html#bo-283"
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
 "listGroupSale": {
  "method": "GET",
  "path": "/group-sale",
  "contract": "orders",
  "summary": "Group Sales Command Center",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "GroupSalesCommandCenterView"
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
   },
   {
    "name": "campaign",
    "in": "query",
    "required": false
   },
   {
    "name": "market",
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
 "modifyOrder": {
  "method": "POST",
  "path": "/orders/{orderId}/modify",
  "contract": "orders",
  "summary": "Add or remove lines on an existing order",
  "permission": "ORDER_MODIFY",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "ModifyOrderRequest",
  "responds": "OrderModificationResult"
 },
 "rescheduleOrder": {
  "method": "POST",
  "path": "/orders/{orderId}/reschedule",
  "contract": "orders",
  "summary": "Move an order to another performance",
  "permission": "ORDER_RESCHEDULE",
  "offlineCapable": false,
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
  "responds": "OrderExchangeResult"
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "GroupOperationalPlanningTaskWorkspaceInput",
  "responds": "GroupOperationalPlanningTaskWorkspaceView"
 },
 "setGroupPaymentSchedule": {
  "method": "PUT",
  "path": "/group-bookings/{groupBookingId}/payment-schedule",
  "contract": "orders",
  "summary": "Set a group's payment schedule",
  "permission": "ORDER_MODIFY",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "GroupPaymentScheduleInput",
  "responds": "GroupPaymentScheduleView"
 },
 "setGroupTicketAllocation": {
  "method": "PUT",
  "path": "/group-bookings/{groupBookingId}/allocation",
  "contract": "orders",
  "summary": "Set how a group's tickets are allocated",
  "permission": "ORDER_MODIFY",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "GroupTicketAllocationInput",
  "responds": "GroupTicketAllocationView"
 },
 "setGroupTicketFulfillment": {
  "method": "PUT",
  "path": "/group-bookings/{groupBookingId}/fulfillment",
  "contract": "orders",
  "summary": "Set how a group's tickets are delivered",
  "permission": "ORDER_MODIFY",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "GroupTicketFulfillmentInput",
  "responds": "GroupTicketFulfillmentView"
 },
 "setParticipantGuestList": {
  "method": "PUT",
  "path": "/group-bookings/{groupBookingId}/participants",
  "contract": "orders",
  "summary": "Set a group's participant list",
  "permission": "ORDER_MODIFY",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "ParticipantGuestListInput",
  "responds": "ParticipantGuestListView"
 },
 "updateGroupBooking": {
  "method": "PATCH",
  "path": "/group-bookings/{groupBookingId}",
  "contract": "orders",
  "summary": "Confirm numbers, change the leader or cancel a group",
  "permission": "ORDER_MODIFY",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "UpdateGroupBookingRequest",
  "responds": "GroupBooking"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "CreateOrderLine": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "id",
   "variantId",
   "quantity",
   "quotedUnitPrice"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "Client-generated ULID of the line. `lineIds` everywhere in this contract are these."
   },
   "variantId": {
    "type": "string",
    "format": "uuid"
   },
   "performanceId": {
    "type": "string",
    "format": "uuid"
   },
   "bookedWindow": {
    "$ref": "#/components/schemas/BookedWindow"
   },
   "inventoryHoldId": {
    "type": "string",
    "nullable": true,
    "description": "Lease the units were drawn from — a `catalogue.InventoryHold.id`. Absent for uncontended products."
   },
   "seatIds": {
    "type": "array",
    "maxItems": 50,
    "items": {
     "type": "string",
     "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
    },
    "description": "Seated products only, as `seating.Seat.id`. Not available offline. **At most `VenueSettings.seating.maxSeatsPerGuestOrder` seats per booking on a guest channel** (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); **at most 10 per sale on staff and POS** (audit R080 (c)), across all the lines of one order for one performance. `createOrder` refuses more with 422 `seatLimitExceeded` (problem type `seat-limit-exceeded`)."
   },
   "resourceHoldId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "nullable": true,
    "description": "A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant. `createOrder` converts the hold into a `ResourceBooking` without releasing it. Not available offline."
   },
   "attributes": {
    "$ref": "#/components/schemas/OrderLineAttributes"
   },
   "quantity": {
    "type": "integer",
    "minimum": 1
   },
   "eligibilityDeclaration": {
    "type": "array",
    "nullable": true,
    "x-ticvai-note": "One row per declared guest in `orders.order_line_eligibility` (named on `OrderLine`), because an array of objects is a child table's rows, not a column.\n",
    "items": {
     "type": "object",
     "properties": {
      "ageBand": {
       "type": "string",
       "enum": [
        "infant",
        "child",
        "junior",
        "adult",
        "senior"
       ],
       "description": "Infant under 3, child 3–12, junior 13–17, adult 18–59, senior 60+."
      },
      "ageYears": {
       "type": "integer",
       "nullable": true
      },
      "heightBandIndex": {
       "type": "integer",
       "nullable": true
      },
      "confidentSwimmer": {
       "type": "boolean",
       "nullable": true,
       "description": "**Derived, kept for the gate check** (decided 29 September, rev 3 REV3-26). The swim question is a consent: the answer is a `marketing.BookingConsentRecord` of kind `swim`, and this is filled from it (true for a `yes` covering this person, whether answered for them or once for the booking). A value sent that contradicts the record is ignored and the record wins. No longer the place a swim answer is captured.\n"
      },
      "guardianSigned": {
       "type": "boolean"
      }
     }
    },
    "description": "What was declared for each guest on this line, kept as the record staff check at the gate."
   },
   "quotedUnitPrice": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "What the client charged, from its local bundle."
   },
   "holderName": {
    "type": "string",
    "nullable": true
   },
   "dataMaskValues": {
    "type": "object",
    "additionalProperties": true,
    "description": "**Deliberately open.** Custom fields keyed by the venue's data mask: the field definitions travel in the catalogue bundle (`catalogue.CatalogueBundle.payload`), so the keys are the venue's to define, as on `catalogue`'s own `dataMaskValues`.\n"
   }
  }
 },
 "GroupAmendmentsCancellationRefundOperationsView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Group Amendments, Cancellation & Refund Operations displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
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
   "amendmentType": {
    "type": "string",
    "enum": [
     "increaseGuestCount",
     "reduceGuestCount",
     "dateChange",
     "timeChange",
     "productChange",
     "packageChange",
     "seatChange",
     "cateringChange",
     "resourceChange",
     "fullCancellation",
     "partialCancellation"
    ],
    "description": "Amendment requested."
   },
   "approvalReasons": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "lateCancellation",
      "waivedFee",
      "largeRefund",
      "capacityOverride",
      "contractException"
     ]
    },
    "description": "Exceptions that trigger approval."
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
   "issues": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "missingGuest",
      "extraGuest",
      "invalidTicket",
      "wrongDate",
      "lateArrival",
      "paymentHold",
      "missingCredential",
      "accessibilityRequirement"
     ]
    },
    "description": "Arrival issues raised."
   }
  }
 },
 "GroupBooking": {
  "type": "object",
  "x-ticvai-persistence": "orders.group_booking",
  "description": "BL-028. **`BO-026 Group Bookings` ran on generic order operations** — no group size, no quota, no leader, no per-attendee capture.\n**The leader is the point.** A school booking forty places has one person who pays, one who is called if the coach is late, and forty who need names collecting — and a generic order has one guest.\n",
  "required": [
   "id",
   "orderId",
   "leaderSubjectId",
   "expectedSize",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "type": "string",
    "enum": [
     "general",
     "school",
     "corporate",
     "party"
    ],
    "default": "general"
   },
   "packageProductId": {
    "type": "string",
    "nullable": true,
    "description": "The school-trip format or party package."
   },
   "yearGroup": {
    "type": "string",
    "maxLength": 40,
    "nullable": true
   },
   "accessAndDietaryNeeds": {
    "type": "string",
    "maxLength": 1000,
    "nullable": true
   },
   "celebrantName": {
    "type": "string",
    "maxLength": 120,
    "nullable": true,
    "description": "The birthday child."
   },
   "celebrantTurningAge": {
    "type": "integer",
    "minimum": 1,
    "maximum": 18,
    "nullable": true
   },
   "allergiesAndRequests": {
    "type": "string",
    "maxLength": 1000,
    "nullable": true
   },
   "finalHeadcountDueBy": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "quoteSentAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "riskAssessmentSentAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "preferredDate": {
    "type": "string",
    "format": "date",
    "nullable": true,
    "description": "The date the guest asked for on `requestGroupBooking` — what its `409 dateUnavailable` is checked against. Null for a group a member of staff built from an order."
   },
   "orderId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "leaderSubjectId": {
    "type": "string",
    "format": "uuid"
   },
   "organisationName": {
    "type": "string",
    "nullable": true
   },
   "expectedSize": {
    "type": "integer"
   },
   "confirmedSize": {
    "type": "integer",
    "nullable": true
   },
   "minimumSize": {
    "type": "integer",
    "nullable": true,
    "description": "**Below which the group rate does not apply.** A booking for forty that arrives as twelve is a pricing question somebody has to answer at the gate, and stating the threshold means answering it at booking instead.\n"
   },
   "attendeeCaptureRequired": {
    "type": "boolean",
    "default": false,
    "description": "**Whether names are needed before admission.** A school trip usually needs them and a corporate day out usually does not, and the difference is a safeguarding requirement rather than a preference.\n"
   },
   "attendeeCaptureDueBy": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "provisional",
     "confirmed",
     "namesPending",
     "complete",
     "cancelled"
    ]
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
   "customerFeedbackCaptured": {
    "type": "string",
    "description": "Customer feedback captured where applicable"
   },
   "customerSatisfaction": {
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
   "tasks": {
    "type": "array",
    "description": "Department tasks",
    "items": {
     "type": "object",
     "properties": {
      "department": {
       "type": "string",
       "description": "Department"
      },
      "task": {
       "type": "string",
       "description": "Task"
      },
      "owner": {
       "type": "string",
       "description": "Owner"
      },
      "dueDate": {
       "type": "string",
       "format": "date-time",
       "description": "Due date"
      },
      "dueTime": {
       "type": "string",
       "description": "Due time"
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
    }
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
   "tasks": {
    "type": "array",
    "description": "Department tasks, e.g. admissions prepare group entry, F&B confirm meal quantities, finance confirm payment",
    "items": {
     "type": "object",
     "properties": {
      "department": {
       "type": "string",
       "description": "Department"
      },
      "task": {
       "type": "string",
       "description": "Task"
      },
      "owner": {
       "type": "string",
       "description": "Owner"
      },
      "dueDate": {
       "type": "string",
       "format": "date-time",
       "description": "Due date"
      },
      "dueTime": {
       "type": "string",
       "description": "Due time"
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
    }
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
   "finalBalance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Final Balance"
   },
   "scheduleType": {
    "type": "string",
    "enum": [
     "milestonePayment",
     "installment",
     "customSchedule"
    ],
    "description": "Payment schedule."
   },
   "paymentMethods": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "paymentLink",
      "card",
      "bankTransfer",
      "accountCredit",
      "cash",
      "otherApprovedMethod"
     ]
    },
    "description": "Methods offered."
   }
  }
 },
 "GroupPaymentScheduleInput": {
  "type": "object",
  "x-ticvai-persistence": "none — request only",
  "description": "What `setGroupPaymentSchedule` takes. The milestones must sum to the group booking's total (decided 29 September, readiness close-out).",
  "required": [
   "scheduleType",
   "milestones"
  ],
  "properties": {
   "scheduleType": {
    "type": "string",
    "description": "The shape of the schedule (decided 29 September, readiness close-out).",
    "enum": [
     "depositThenBalance",
     "milestonePayment",
     "finalBalance",
     "customSchedule"
    ]
   },
   "milestones": {
    "type": "array",
    "minItems": 1,
    "items": {
     "type": "object",
     "required": [
      "dueDate",
      "amount"
     ],
     "properties": {
      "dueDate": {
       "type": "string",
       "format": "date"
      },
      "amount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "label": {
       "type": "string",
       "maxLength": 60,
       "nullable": true
      }
     }
    }
   }
  }
 },
 "GroupPaymentScheduleView": {
  "type": "object",
  "x-ticvai-persistence": "orders.group_payment_schedule + orders.group_payment_milestone",
  "description": "**One group's payment schedule.** Written by `setGroupPaymentSchedule` (decided 29 September, readiness close-out); `DepositPolicy` stays the venue-wide default.\n",
  "required": [
   "groupBookingId",
   "scheduleType",
   "milestones"
  ],
  "properties": {
   "groupBookingId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "scheduleType": {
    "type": "string",
    "enum": [
     "depositThenBalance",
     "milestonePayment",
     "finalBalance",
     "customSchedule"
    ]
   },
   "total": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "readOnly": true,
    "description": "The group booking's total, which the milestones sum to."
   },
   "milestones": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "id",
      "dueDate",
      "amount",
      "status"
     ],
     "properties": {
      "id": {
       "type": "string",
       "format": "uuid",
       "readOnly": true
      },
      "dueDate": {
       "type": "string",
       "format": "date"
      },
      "amount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "label": {
       "type": "string",
       "maxLength": 60,
       "nullable": true
      },
      "status": {
       "type": "string",
       "readOnly": true,
       "enum": [
        "due",
        "paid",
        "overdue"
       ]
      }
     }
    }
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
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
   }
  }
 },
 "GroupSalesCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Group Sales Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "newEnquiries": {
    "type": "integer",
    "description": "New Enquiries"
   },
   "quotationsOutstanding": {
    "type": "string",
    "description": "Quotations Outstanding"
   },
   "quotesAwaitingApproval": {
    "type": "string",
    "description": "Quotes Awaiting Approval"
   },
   "confirmedGroups": {
    "type": "integer",
    "description": "Confirmed Groups"
   },
   "expectedGuests": {
    "type": "integer",
    "description": "Expected Guests"
   },
   "pipelineValue": {
    "type": "string",
    "description": "Pipeline Value"
   },
   "confirmedRevenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Confirmed Revenue"
   },
   "conversionRate": {
    "type": "number",
    "description": "Conversion Rate"
   },
   "averageGroupValue": {
    "type": "number",
    "description": "Average Group Value"
   },
   "expiringQuotes": {
    "type": "integer",
    "description": "Expiring Quotes"
   },
   "salesTargetAchievement": {
    "type": "string",
    "description": "Sales Target Achievement"
   },
   "enquiryId": {
    "type": "string",
    "description": "Enquiry ID"
   },
   "organizationCustomer": {
    "type": "string",
    "description": "Organization/Customer"
   },
   "groupType": {
    "type": "string",
    "description": "Group Type"
   },
   "eventAttraction": {
    "type": "string",
    "description": "Event/Attraction"
   },
   "visitDate": {
    "type": "string",
    "format": "date-time",
    "description": "Visit Date"
   },
   "guestCount": {
    "type": "integer",
    "description": "Guest Count"
   },
   "salesOwner": {
    "type": "string",
    "description": "Sales Owner"
   },
   "estimatedValue": {
    "type": "string",
    "description": "Estimated Value"
   },
   "quoteStatus": {
    "type": "string",
    "description": "Quote Status"
   },
   "probability": {
    "type": "string",
    "description": "Probability"
   },
   "nextAction": {
    "type": "string",
    "format": "date-time",
    "description": "Next Action"
   },
   "expectedCloseDate": {
    "type": "string",
    "format": "date-time",
    "description": "Expected Close Date"
   },
   "followUpsDue": {
    "type": "string",
    "description": "Follow-ups due"
   },
   "quotesExpiring": {
    "type": "string",
    "description": "Quotes expiring"
   },
   "customerResponses": {
    "type": "integer",
    "description": "Customer responses"
   },
   "approvalRequests": {
    "type": "integer",
    "description": "Approval requests"
   },
   "depositsPending": {
    "type": "integer",
    "description": "Deposits pending"
   }
  }
 },
 "GroupTicketAllocationInput": {
  "type": "object",
  "x-ticvai-persistence": "none — request only",
  "description": "What `setGroupTicketAllocation` takes (decided 29 September, readiness close-out).",
  "required": [
   "allocationMode",
   "allocations"
  ],
  "properties": {
   "allocationMode": {
    "type": "string",
    "description": "How the group's tickets are allocated (decided 29 September, readiness close-out).",
    "enum": [
     "individualTicket",
     "bulkTicket",
     "namedTicket",
     "quantityBasedTicket",
     "zoneAllocation"
    ]
   },
   "keepGroupTogether": {
    "type": "boolean",
    "default": false
   },
   "vipAllocation": {
    "type": "boolean",
    "default": false,
    "description": "Set aside the group's VIP places."
   },
   "allocations": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "productId",
      "quantity"
     ],
     "properties": {
      "productId": {
       "type": "string",
       "format": "uuid"
      },
      "quantity": {
       "type": "integer",
       "minimum": 1
      },
      "zoneId": {
       "type": "string",
       "format": "uuid",
       "nullable": true,
       "description": "Required for `zoneAllocation`."
      },
      "participantId": {
       "type": "string",
       "format": "uuid",
       "nullable": true,
       "description": "The participant a `namedTicket` line is for. Required for `namedTicket`."
      }
     }
    }
   }
  }
 },
 "GroupTicketAllocationView": {
  "type": "object",
  "x-ticvai-persistence": "orders.group_ticket_allocation + orders.group_ticket_allocation_line",
  "description": "**How one group's tickets are allocated.** Written by `setGroupTicketAllocation` (decided 29 September, readiness close-out).\n",
  "required": [
   "groupBookingId",
   "allocationMode",
   "allocations"
  ],
  "properties": {
   "groupBookingId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "allocationMode": {
    "type": "string",
    "enum": [
     "individualTicket",
     "bulkTicket",
     "namedTicket",
     "quantityBasedTicket",
     "zoneAllocation"
    ]
   },
   "keepGroupTogether": {
    "type": "boolean"
   },
   "vipAllocation": {
    "type": "boolean"
   },
   "allocations": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "id",
      "productId",
      "quantity"
     ],
     "properties": {
      "id": {
       "type": "string",
       "format": "uuid",
       "readOnly": true
      },
      "productId": {
       "type": "string",
       "format": "uuid"
      },
      "quantity": {
       "type": "integer",
       "minimum": 1
      },
      "zoneId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "participantId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      }
     }
    }
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "GroupTicketFulfillmentDistributionView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Group Ticket Fulfillment & Distribution displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
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
   "deliveryMethod": {
    "type": "string",
    "enum": [
     "oneGroupQr",
     "individualQr",
     "groupLeaderWallet",
     "individualMobileTickets",
     "email",
     "posPrint",
     "rfid",
     "nfc",
     "wristband",
     "physicalCollection"
    ],
    "description": "How the group receives credentials: one QR for a headcount, a QR each, or others (MoM 31 Aug)."
   },
   "distributionMode": {
    "type": "string",
    "enum": [
     "coordinator",
     "eachParticipant",
     "teachersTeamLeaders"
    ],
    "description": "Who the credentials go to"
   }
  }
 },
 "GroupTicketFulfillmentInput": {
  "type": "object",
  "x-ticvai-persistence": "none — request only",
  "description": "What `setGroupTicketFulfillment` takes (decided 29 September, readiness close-out).",
  "required": [
   "method",
   "recipients"
  ],
  "properties": {
   "method": {
    "type": "string",
    "description": "How the tickets are delivered (decided 29 September, readiness close-out).",
    "enum": [
     "email",
     "sms",
     "wallet",
     "bulkPdf",
     "posPrint",
     "physicalCollection"
    ]
   },
   "recipients": {
    "type": "string",
    "description": "Who receives them (decided 29 September, readiness close-out).",
    "enum": [
     "organiser",
     "eachParticipant"
    ]
   },
   "releaseAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "Hold the tickets back until then; null releases them when the group is confirmed."
   }
  }
 },
 "GroupTicketFulfillmentView": {
  "type": "object",
  "x-ticvai-persistence": "orders.group_ticket_fulfillment",
  "description": "**How one group's tickets reach them.** Written by `setGroupTicketFulfillment` (decided 29 September, readiness close-out).\n",
  "required": [
   "groupBookingId",
   "method",
   "recipients"
  ],
  "properties": {
   "groupBookingId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "method": {
    "type": "string",
    "enum": [
     "email",
     "sms",
     "wallet",
     "bulkPdf",
     "posPrint",
     "physicalCollection"
    ]
   },
   "recipients": {
    "type": "string",
    "enum": [
     "organiser",
     "eachParticipant"
    ]
   },
   "releaseAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "releasedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "GroupTicketSeatEntitlementAllocationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Group Ticket, Seat & Entitlement Allocation displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
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
   "ticketModel": {
    "type": "string",
    "enum": [
     "individualTicket",
     "bulkTicket",
     "groupCredential",
     "namedTicket",
     "quantityBasedTicket",
     "reservedSeat",
     "generalAdmission",
     "zoneAllocation"
    ],
    "description": "How the group is ticketed."
   },
   "seatingPreferences": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "keepGroupTogether",
      "accessibleSeats",
      "teacherLeaderAdjacentSeating",
      "vipAllocation",
      "companionSeats"
     ]
    },
    "description": "Seating preferences applied."
   },
   "associatedAllocations": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "meal",
      "workshop",
      "parking",
      "fastTrack",
      "merchandise",
      "otherPackageComponents"
     ]
    },
    "description": "Package items allocated with the tickets."
   }
  }
 },
 "ModifyOrderRequest": {
  "type": "object",
  "required": [
   "id",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "Client-generated ULID **of this modification, not of the order** — the order is the path's `orderId`. It is the modification's idempotency key and must equal the `Idempotency-Key` header.\n"
   },
   "addLines": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/CreateOrderLine"
    }
   },
   "removeLineIds": {
    "type": "array",
    "items": {
     "type": "string",
     "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
    }
   },
   "reason": {
    "type": "string",
    "maxLength": 500
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "Order": {
  "x-ticvai-persistence": "orders.sales_order + orders.order_line",
  "type": "object",
  "required": [
   "id",
   "venueId",
   "scopePath",
   "channel",
   "status",
   "currency",
   "currencyScale",
   "grossAmount",
   "taxAmount",
   "netAmount",
   "lines",
   "createdAt",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "The client ULID from `CreateOrderRequest.id`."
   },
   "orderNumber": {
    "type": "string",
    "readOnly": true,
    "description": "The number a guest reads and a cashier types. **Server-assigned: the venue prefix and a sequence per venue**, for example `DXB1-000123` (decided 28 September, audit R152). A till holds a reserved range of the venue sequence, so an order taken offline gets its number on the till and keeps it through `syncOrders`. **Not gapless**: an unused reserved range leaves a gap, and that is allowed. Only tax invoices are gapless, per legal entity. The receipt carries this number.\n"
   },
   "channel": {
    "allOf": [
     {
      "$ref": "#/components/schemas/OrderChannel"
     }
    ],
    "description": "Where it came from. Drives revenue attribution, promotion eligibility and the self-service adoption figures the operator will ask for within a month of launch.\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string"
   },
   "status": {
    "$ref": "#/components/schemas/OrderStatus"
   },
   "currency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "x-ticvai-persisted": false,
    "description": "**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"
   },
   "currencyScale": {
    "type": "integer",
    "minimum": 0,
    "maximum": 4,
    "x-ticvai-persisted": false,
    "description": "**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"
   },
   "grossAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "taxAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "netAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "refundedAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "droppedPromotions": {
    "type": "array",
    "readOnly": true,
    "x-ticvai-persisted": false,
    "description": "**Promotions left off this order at checkout because their budget cap would have been exceeded** (decided 28 September, audit R101 (8)). Empty when none was dropped. Returned by `checkoutCart` and `createOrder`, not stored.\n",
    "items": {
     "type": "object",
     "required": [
      "promotionId"
     ],
     "properties": {
      "promotionId": {
       "type": "string",
       "format": "uuid"
      },
      "name": {
       "type": "string"
      },
      "reason": {
       "type": "string",
       "enum": [
        "budgetCapReached"
       ]
      }
     }
    }
   },
   "totalPriceVariance": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Sum across lines. Zero on a normal order."
   },
   "lines": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/OrderLine"
    }
   },
   "payments": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/Payment"
    }
   },
   "principalId": {
    "type": "string",
    "format": "uuid"
   },
   "workstationId": {
    "type": "string",
    "format": "uuid"
   },
   "shiftId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "nullable": true
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "holdLabel": {
    "type": "string",
    "maxLength": 60,
    "nullable": true,
    "readOnly": true,
    "description": "The `label` a cashier gave when parking it with `holdOrder` — how they find it again. Null on an order never held."
   },
   "heldUntil": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "description": "When a held order expires and is voided (states/order.yaml), from `holdOrder`'s `holdUntil`. Null on an order not currently held."
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   },
   "syncedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "OrderExchangeResult": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "orderId",
   "outgoingValue",
   "incomingValue",
   "difference"
  ],
  "properties": {
   "orderId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "outgoingValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "incomingValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "exchangeFee": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "difference": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Only the difference settles. The replacement is held before the original is released, never the other way round.\n"
   },
   "newLineIds": {
    "type": "array",
    "items": {
     "type": "string",
     "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
    }
   },
   "revokedEntitlementIds": {
    "type": "array",
    "items": {
     "type": "string",
     "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
    }
   },
   "issuedEntitlementIds": {
    "type": "array",
    "items": {
     "type": "string",
     "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
    }
   }
  }
 },
 "OrderModificationResult": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "order",
   "balanceDue"
  ],
  "properties": {
   "order": {
    "$ref": "#/components/schemas/Order"
   },
   "addedValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "removedValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "balanceDue": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Positive means the guest pays; negative means a refund is due."
   },
   "refundId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "nullable": true
   },
   "revokedEntitlementIds": {
    "type": "array",
    "items": {
     "type": "string",
     "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
    }
   },
   "issuedEntitlementIds": {
    "type": "array",
    "items": {
     "type": "string",
     "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
    }
   }
  }
 },
 "ParticipantGuestListInput": {
  "type": "object",
  "x-ticvai-persistence": "none — request only",
  "description": "What `setParticipantGuestList` takes. It replaces the whole list (decided 29 September, readiness close-out).",
  "required": [
   "source",
   "participants"
  ],
  "properties": {
   "source": {
    "type": "string",
    "description": "How the names arrived (decided 29 September, readiness close-out).",
    "enum": [
     "manualEntry",
     "csvExcelImport",
     "customerUpload",
     "api"
    ]
   },
   "participants": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "fullName"
     ],
     "properties": {
      "fullName": {
       "type": "string",
       "maxLength": 200
      },
      "role": {
       "type": "string",
       "enum": [
        "participant",
        "leader",
        "supervisor"
       ],
       "default": "participant"
      },
      "email": {
       "type": "string",
       "format": "email",
       "nullable": true
      },
      "phone": {
       "type": "string",
       "maxLength": 30,
       "nullable": true
      },
      "dateOfBirth": {
       "type": "string",
       "format": "date",
       "nullable": true
      }
     }
    }
   },
   "fileRef": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The uploaded file the names came from. Required for `csvExcelImport` and `customerUpload`."
   }
  }
 },
 "ParticipantGuestListView": {
  "type": "object",
  "x-ticvai-persistence": "orders.group_participant_list + orders.group_participant",
  "description": "**A group's participants, and how the list arrived.** Written by `setParticipantGuestList` (decided 29 September, readiness close-out).\n",
  "required": [
   "groupBookingId",
   "source",
   "participants"
  ],
  "properties": {
   "groupBookingId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "source": {
    "type": "string",
    "enum": [
     "manualEntry",
     "csvExcelImport",
     "customerUpload",
     "api"
    ]
   },
   "fileRef": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "participants": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "id",
      "fullName"
     ],
     "properties": {
      "id": {
       "type": "string",
       "format": "uuid",
       "readOnly": true
      },
      "fullName": {
       "type": "string",
       "maxLength": 200
      },
      "role": {
       "type": "string",
       "enum": [
        "participant",
        "leader",
        "supervisor"
       ]
      },
      "email": {
       "type": "string",
       "format": "email",
       "nullable": true
      },
      "phone": {
       "type": "string",
       "maxLength": 30,
       "nullable": true
      },
      "dateOfBirth": {
       "type": "string",
       "format": "date",
       "nullable": true
      }
     }
    }
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "ParticipantsGuestListsGroupStructureView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Participants, Guest Lists & Group Structure displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
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
   "dateOfBirth": {
    "type": "string",
    "format": "date-time",
    "description": "Age/Date of Birth where applicable"
   },
   "captureSource": {
    "type": "string",
    "enum": [
     "manualEntry",
     "csvExcelImport",
     "customerUpload",
     "api",
     "previousGroupTemplate"
    ],
    "description": "How the participant was captured."
   },
   "validationIssues": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "missingRequiredField",
      "invalidCategory",
      "guestCountMismatch",
      "ageTicketMismatch"
     ]
    },
    "description": "Problems detected on the list."
   }
  }
 },
 "UpdateGroupBookingRequest": {
  "type": "object",
  "description": "Request only. Every field optional; absent means unchanged.",
  "properties": {
   "packageProductId": {
    "type": "string",
    "nullable": true,
    "description": "The school-trip format or party package."
   },
   "yearGroup": {
    "type": "string",
    "maxLength": 40,
    "nullable": true
   },
   "accessAndDietaryNeeds": {
    "type": "string",
    "maxLength": 1000,
    "nullable": true
   },
   "celebrantName": {
    "type": "string",
    "maxLength": 120,
    "nullable": true,
    "description": "The birthday child."
   },
   "celebrantTurningAge": {
    "type": "integer",
    "minimum": 1,
    "maximum": 18,
    "nullable": true
   },
   "allergiesAndRequests": {
    "type": "string",
    "maxLength": 1000,
    "nullable": true
   },
   "finalHeadcountDueBy": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "leaderSubjectId": {
    "type": "string",
    "format": "uuid"
   },
   "organisationName": {
    "type": "string",
    "maxLength": 200,
    "nullable": true
   },
   "expectedSize": {
    "type": "integer",
    "minimum": 2
   },
   "confirmedSize": {
    "type": "integer",
    "minimum": 0
   },
   "minimumSize": {
    "type": "integer",
    "minimum": 1,
    "nullable": true
   },
   "attendeeCaptureRequired": {
    "type": "boolean"
   },
   "attendeeCaptureDueBy": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "confirmed",
     "namesPending",
     "complete",
     "cancelled"
    ]
   }
  }
 }
}
```
