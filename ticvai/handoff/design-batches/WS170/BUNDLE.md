# WS170 — Seat Management Venue Mapping Reference v1.0 board 6

**10 screens · 6 operations · 8 schemas · 2 permissions**

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
  `APPROVAL_REQUEST, CAPACITY_CONFIGURE`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-1003` | Hold Command Center | listDetail | 1 | 0 | — |
| `BO-1004` | Hold Type Master | listDetail | 2 | 0 | — |
| `BO-1005` | Hold Pool Creation | listDetail | 1 | 0 | — |
| `BO-1006` | Hold Rule Assignment | listDetail | 1 | 0 | — |
| `BO-1007` | Expiration Rules | listDetail | 1 | 0 | — |
| `BO-1008` | Automatic Hold Release | listDetail | 1 | 0 | — |
| `BO-1009` | Release, Convert & Reassign | listDetail | 1 | 0 | — |
| `BO-1010` | Hold Approval Workflow | listDetail | 2 | 0 | — |
| `BO-1011` | Priority & Conflict Resolution | listDetail | 2 | 0 | — |
| `BO-1012` | Hold Utilization & Audit | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-1003, BO-1004, BO-1005, BO-1006, BO-1007, BO-1008, BO-1009, BO-1010, BO-1011, BO-1012 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-1003",
  "name": "Hold Command Center",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "6",
   "number": "01",
   "page": 26
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/hold-command-center-bo-1003",
   "component": "apps/venue-management-web/src/routes/access-venue/HoldCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-1004",
    "BO-1005",
    "BO-1006",
    "BO-1007",
    "BO-1008",
    "BO-1009",
    "BO-1010",
    "BO-1011",
    "BO-1012"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "BO-1004",
     "trigger": "Hold Type Master",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    },
    {
     "to": "BO-1005",
     "trigger": "Hold Pool Creation",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    },
    {
     "to": "BO-1006",
     "trigger": "Hold Rule Assignment",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    },
    {
     "to": "BO-1007",
     "trigger": "Expiration Rules",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    },
    {
     "to": "BO-1008",
     "trigger": "Automatic Hold Release",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    },
    {
     "to": "BO-1009",
     "trigger": "Release, Convert & Reassign",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    },
    {
     "to": "BO-1010",
     "trigger": "Hold Approval Workflow",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    },
    {
     "to": "BO-1011",
     "trigger": "Priority & Conflict Resolution",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    },
    {
     "to": "BO-1012",
     "trigger": "Hold Utilization & Audit",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide a complete operational view of held inventory and its risk. Show held seats, hold value, utilization, conversion, upcoming expiry, overdue decisions and inventory at risk. Analyze by tenant, venue, event, performance, hold type, owner, stakeholder, priority and age. Surface high-value unused holds, late release, conflicts and low conversion with direct action links. Hold creation and release shall be atomic, reason-coded and approval-controlled by value, quantity, type and timing; overlapping holds require explicit priority resolution. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 26"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 26"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listSeatHoldPools",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The hold list.",
   "error": "Could not load. Names which read failed and leaves the hold untouched.",
   "emptyFirstRun": "No hold yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the hold are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listSeatHoldPools",
    "contract": "seating",
    "purpose": "Pools and their utilisation",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1003",
   "workshopBoard": "wireframes/WS145 Seat Management Venue Mapping Reference v1.0 Board 6.dc.html#bo-1003"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 26. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1004",
  "name": "Hold Type Master",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "6",
   "number": "02",
   "page": 26
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/hold-type-master-bo-1004",
   "component": "apps/venue-management-web/src/routes/access-venue/HoldTypeMaster.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1003"
   ],
   "exitTo": [
    "BO-1003"
   ],
   "transitions": [
    {
     "to": "BO-1003",
     "trigger": "Back to Hold Command Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure reusable hold categories and their default behavior. Maintain VIP, Sponsor, Artist, Media, Corporate, Internal and custom types with code, color and description. Set default duration, priority, approval, reminder, maximum quantity, permitted channels and auto-release policy. Map type to stakeholder classes, contract requirements, reporting dimensions and permitted roles. Hold creation and release shall be atomic, reason-coded and approval-controlled by value, quantity, type and timing; overlapping holds require explicit priority resolution. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 26"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 26"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listSeatHoldTypes",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "setSeatHoldType",
       "label": "Save seat hold type",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setSeatHoldType"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The hold type master list.",
   "error": "Could not load. Names which read failed and leaves the hold type master untouched.",
   "emptyFirstRun": "No hold type master yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the hold type master are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listSeatHoldTypes",
    "contract": "seating",
    "purpose": "Hold kinds",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "setSeatHoldType",
    "contract": "seating",
    "purpose": "Define one",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listSeatHoldTypes"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1004",
   "workshopBoard": "wireframes/WS145 Seat Management Venue Mapping Reference v1.0 Board 6.dc.html#bo-1004"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 26. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1005",
  "name": "Hold Pool Creation",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "6",
   "number": "03",
   "page": 26
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/hold-pool-creation-bo-1005",
   "component": "apps/venue-management-web/src/routes/access-venue/HoldPoolCreation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1003"
   ],
   "exitTo": [
    "BO-1003"
   ],
   "transitions": [
    {
     "to": "BO-1003",
     "trigger": "Back to Hold Command Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Select and create an explicit pool of held seats or capacity. Choose inventory by map, section, row, seat list, zone quantity or uploaded allocation with current-state validation. Capture event/performance, type, owner, stakeholder, value, purpose, effective time, expiry and notes. Preview available, already held, reserved, sold, blocked and inaccessible inventory before submission. Hold creation and release shall be atomic, reason-coded and approval-controlled by value, quantity, type and timing; overlapping holds require explicit priority resolution. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history. Configuration Scope of Work | Version 1.0 26",
  "gaps": [
   {
    "operation": null,
    "why": "**Hold Pool Creation declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 26"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 26"
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
       "impliedBy": "createSeatHoldPool",
       "label": "Create seat hold pool",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createSeatHoldPool"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The hold pool creation list.",
   "error": "Could not load. Names which read failed and leaves the hold pool creation untouched.",
   "emptyFirstRun": "No hold pool creation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the hold pool creation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createSeatHoldPool",
    "contract": "seating",
    "purpose": "Create a pool",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listSeatHoldPools",
     "getSeatInventory",
     "getSeatAvailability"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1005",
   "workshopBoard": "wireframes/WS145 Seat Management Venue Mapping Reference v1.0 Board 6.dc.html#bo-1005"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 26. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1006",
  "name": "Hold Rule Assignment",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "6",
   "number": "04",
   "page": 27
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/hold-rule-assignment-bo-1006",
   "component": "apps/venue-management-web/src/routes/access-venue/HoldRuleAssignment.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1003"
   ],
   "exitTo": [
    "BO-1003"
   ],
   "transitions": [
    {
     "to": "BO-1003",
     "trigger": "Back to Hold Command Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Automatically apply approved hold policies to eligible performances. Build conditions by tenant, venue, event, product, date, performance, section, category, stakeholder and channel. Define seat set or quantity, type, owner, priority, duration, release rule and exception behavior. Simulate upcoming performances, detect rule collisions and version every activated rule. Hold creation and release shall be atomic, reason-coded and approval-controlled by value, quantity, type and timing; overlapping holds require explicit priority resolution. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 27"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 27"
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
       "impliedBy": "setSeatHoldType",
       "label": "Save seat hold type",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setSeatHoldType"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The hold rule list.",
   "error": "Could not load. Names which read failed and leaves the hold rule untouched.",
   "emptyFirstRun": "No hold rule yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the hold rule are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setSeatHoldType",
    "contract": "seating",
    "purpose": "Which rule applies where",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listSeatHoldTypes"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1006",
   "workshopBoard": "wireframes/WS145 Seat Management Venue Mapping Reference v1.0 Board 6.dc.html#bo-1006"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 27. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1007",
  "name": "Expiration Rules",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "6",
   "number": "05",
   "page": 27
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/expiration-rules-bo-1007",
   "component": "apps/venue-management-web/src/routes/access-venue/ExpirationRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1003"
   ],
   "exitTo": [
    "BO-1003"
   ],
   "transitions": [
    {
     "to": "BO-1003",
     "trigger": "Back to Hold Command Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Control when held inventory must be reviewed or released. Set fixed timestamp, time-before-performance, contract milestone, payment condition or manual approval expiry. Configure reminder sequence, grace period, escalation, extension eligibility and maximum extension. Respect venue timezone and daylight-saving behavior and preserve the rule/version applied to each hold. Hold creation and release shall be atomic, reason-coded and approval-controlled by value, quantity, type and timing; overlapping holds require explicit priority resolution. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 27"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 27"
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
       "impliedBy": "setSeatHoldType",
       "label": "Save seat hold type",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setSeatHoldType"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The expiration rules list.",
   "error": "Could not load. Names which read failed and leaves the expiration rules untouched.",
   "emptyFirstRun": "No expiration rules yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the expiration rules are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setSeatHoldType",
    "contract": "seating",
    "purpose": "Expiration rules",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listSeatHoldTypes"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1007",
   "workshopBoard": "wireframes/WS145 Seat Management Venue Mapping Reference v1.0 Board 6.dc.html#bo-1007"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 27. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1008",
  "name": "Automatic Hold Release",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "6",
   "number": "06",
   "page": 27
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/automatic-hold-release-bo-1008",
   "component": "apps/venue-management-web/src/routes/access-venue/AutomaticHoldRelease.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1003"
   ],
   "exitTo": [
    "BO-1003"
   ],
   "transitions": [
    {
     "to": "BO-1003",
     "trigger": "Back to Hold Command Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Release eligible held inventory reliably and in controlled batches. Schedule releases by type, rule, event, performance, stakeholder, age and remaining time. Preview seats, price bands, channel availability, sold-out status and exceptions before execution. Use idempotent processing, partial-failure handling, retry, reconciliation and stakeholder notification. Hold creation and release shall be atomic, reason-coded and approval-controlled by value, quantity, type and timing; overlapping holds require explicit priority resolution. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 27"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 27"
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
       "impliedBy": "releaseSeatHoldPool",
       "label": "Release seat hold pool",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "releaseSeatHoldPool"
      },
      {
       "kind": "publishGate",
       "label": "What publishing changes",
       "notes": "**Names what goes live, where, and from when.** A publish with no stated consequence is one somebody presses meaning to save.",
       "provenance": "authored — required by check-screens, 19 September 2026"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The automatic hold release list.",
   "error": "Could not load. Names which read failed and leaves the automatic hold release untouched.",
   "emptyFirstRun": "No automatic hold release yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the automatic hold release are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "releaseSeatHoldPool",
    "contract": "seating",
    "purpose": "Automatic release",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listSeatHoldPools",
     "getSeatInventory",
     "getSeatAvailability"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1008",
   "workshopBoard": "wireframes/WS145 Seat Management Venue Mapping Reference v1.0 Board 6.dc.html#bo-1008"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 27. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "poolId",
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
  "id": "BO-1009",
  "name": "Release, Convert & Reassign",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "6",
   "number": "07",
   "page": 27
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/release-convert-reassign-bo-1009",
   "component": "apps/venue-management-web/src/routes/access-venue/ReleaseConvertReassign.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1003"
   ],
   "exitTo": [
    "BO-1003"
   ],
   "transitions": [
    {
     "to": "BO-1003",
     "trigger": "Back to Hold Command Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow authorized users to change the outcome of an active hold. Release all or selected inventory, convert it to reservation/order, reassign owner/stakeholder or extend expiry. Revalidate state, price, eligibility, payment or contract condition before committing the action. Require reason, supporting notes and approval when value, timing or policy threshold is exceeded. Hold creation and release shall be atomic, reason-coded and approval-controlled by value, quantity, type and timing; overlapping holds require explicit priority resolution. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 27"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 27"
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
       "impliedBy": "releaseSeatHoldPool",
       "label": "Release seat hold pool",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "releaseSeatHoldPool"
      },
      {
       "kind": "publishGate",
       "label": "What publishing changes",
       "notes": "**Names what goes live, where, and from when.** A publish with no stated consequence is one somebody presses meaning to save.",
       "provenance": "authored — required by check-screens, 19 September 2026"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The release convert reassign list.",
   "error": "Could not load. Names which read failed and leaves the release convert reassign untouched.",
   "emptyFirstRun": "No release convert reassign yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the release convert reassign are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "releaseSeatHoldPool",
    "contract": "seating",
    "purpose": "Release, convert or reassign",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listSeatHoldPools",
     "getSeatInventory",
     "getSeatAvailability"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1009",
   "workshopBoard": "wireframes/WS145 Seat Management Venue Mapping Reference v1.0 Board 6.dc.html#bo-1009"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 27. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "poolId",
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
  "id": "BO-1010",
  "name": "Hold Approval Workflow",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "6",
   "number": "08",
   "page": 27
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/hold-approval-workflow-bo-1010",
   "component": "apps/venue-management-web/src/routes/access-venue/HoldApprovalWorkflow.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1003"
   ],
   "exitTo": [
    "BO-1003"
   ],
   "transitions": [
    {
     "to": "BO-1003",
     "trigger": "Back to Hold Command Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Route hold requests and sensitive changes to the correct approvers. Configure requester, venue operations, ticketing, commercial, finance and executive stages by policy. Configuration Scope of Work | Version 1.0 27 Display request details, seats, value, expiry, conflicts, supporting contract and previous decisions. Support approve, reject, request information, delegate and escalate with comments and SLA. Hold creation and release shall be atomic, reason-coded and approval-controlled by value, quantity, type and timing; overlapping holds require explicit priority resolution. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 27"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 27"
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
       "impliedBy": "createApprovalRequest",
       "label": "Create approval request",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listSeatHoldPools",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createApprovalRequest"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The hold approval workflow list.",
   "error": "Could not load. Names which read failed and leaves the hold approval workflow untouched.",
   "emptyFirstRun": "No hold approval workflow yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the hold approval workflow are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createApprovalRequest",
    "contract": "approvals",
    "purpose": "Send a hold for approval",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listSeatHoldPools",
    "contract": "seating",
    "purpose": "What is being requested",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1010",
   "workshopBoard": "wireframes/WS145 Seat Management Venue Mapping Reference v1.0 Board 6.dc.html#bo-1010"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 27. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1011",
  "name": "Priority & Conflict Resolution",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "6",
   "number": "09",
   "page": 28
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/priority-conflict-resolution-bo-1011",
   "component": "apps/venue-management-web/src/routes/access-venue/PriorityConflictResolution.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1003"
   ],
   "exitTo": [
    "BO-1003"
   ],
   "transitions": [
    {
     "to": "BO-1003",
     "trigger": "Back to Hold Command Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Resolve overlapping or competing hold requests predictably. Maintain priority matrix by hold type, event, stakeholder, contract, quantity, value and time before performance. List exact conflicting seats and compare current and proposed owner, purpose, priority and expiry. Allow automatic winner, supervisor decision, alternative seat suggestion or split allocation with recorded reason. Hold creation and release shall be atomic, reason-coded and approval-controlled by value, quantity, type and timing; overlapping holds require explicit priority resolution. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 28"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 28"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listSeatHoldPools",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "setSeatHoldType",
       "label": "Save seat hold type",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setSeatHoldType"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The priority conflict resolution list.",
   "error": "Could not load. Names which read failed and leaves the priority conflict resolution untouched.",
   "emptyFirstRun": "No priority conflict resolution yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the priority conflict resolution are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listSeatHoldPools",
    "contract": "seating",
    "purpose": "Competing holds",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "setSeatHoldType",
    "contract": "seating",
    "purpose": "Priority between kinds",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listSeatHoldTypes"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1011",
   "workshopBoard": "wireframes/WS145 Seat Management Venue Mapping Reference v1.0 Board 6.dc.html#bo-1011"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 28. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1012",
  "name": "Hold Utilization & Audit",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "6",
   "number": "10",
   "page": 28
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/hold-utilization-audit-bo-1012",
   "component": "apps/venue-management-web/src/routes/access-venue/HoldUtilizationAudit.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1003"
   ],
   "exitTo": [
    "BO-1003"
   ],
   "transitions": [
    {
     "to": "BO-1003",
     "trigger": "Back to Hold Command Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Measure whether held inventory creates value or suppresses sale unnecessarily. Report held-to-sold conversion, released and sold, expired unused, average age, value and revenue opportunity. Compare hold type, owner, stakeholder, event, section and release timing over time. Provide immutable creation, approval, extension, conversion, release, conflict and override history with secured export. Hold creation and release shall be atomic, reason-coded and approval-controlled by value, quantity, type and timing; overlapping holds require explicit priority resolution. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history. Configuration Scope of Work | Version 1.0 28 Board 7 - Seating Rules, Buffers & Accessibility Figure 7. High-definition configuration board with all 10 screens. Visual reference: information architecture and configuration coverage; detailed production behavior is defined in the following scope. Configuration Scope of Work | Version 1.0 29",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 28"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 28"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listSeatHoldPools",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The hold utilization audit list.",
   "error": "Could not load. Names which read failed and leaves the hold utilization audit untouched.",
   "emptyFirstRun": "No hold utilization audit yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the hold utilization audit are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listSeatHoldPools",
    "contract": "seating",
    "purpose": "Utilisation and audit",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1012",
   "workshopBoard": "wireframes/WS145 Seat Management Venue Mapping Reference v1.0 Board 6.dc.html#bo-1012"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 28. 0 of 0 labels bound to a contract property; 0 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "createApprovalRequest": {
  "method": "POST",
  "path": "/approval-requests",
  "contract": "approvals",
  "summary": "Raise a request",
  "permission": "APPROVAL_REQUEST",
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
  "requestBody": "CreateApprovalRequest",
  "responds": "ApprovalRequest"
 },
 "createSeatHoldPool": {
  "method": "POST",
  "path": "/seat-hold-pools",
  "contract": "seating",
  "summary": "Take a set of seats out of sale, for a reason, until a date",
  "permission": "CAPACITY_CONFIGURE",
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
  "requestBody": "SeatHoldPool",
  "responds": "SeatHoldPool"
 },
 "listSeatHoldPools": {
  "method": "GET",
  "path": "/seat-hold-pools",
  "contract": "seating",
  "summary": "Held seats, by pool, with what is left and when it releases",
  "permission": "CAPACITY_CONFIGURE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "performanceId",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "SeatHoldPool"
 },
 "listSeatHoldTypes": {
  "method": "GET",
  "path": "/seat-hold-types",
  "contract": "seating",
  "summary": "The kinds of hold a venue places, and who may release them",
  "permission": "CAPACITY_CONFIGURE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "SeatHoldType"
 },
 "releaseSeatHoldPool": {
  "method": "POST",
  "path": "/seat-hold-pools/{poolId}/release",
  "contract": "seating",
  "summary": "Put held seats back on sale, convert them, or reassign them",
  "permission": "CAPACITY_CONFIGURE",
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
  "responds": "SeatHoldPool"
 },
 "setSeatHoldType": {
  "method": "PUT",
  "path": "/seat-hold-types",
  "contract": "seating",
  "summary": "Define a hold kind, its owner and its release rule",
  "permission": "CAPACITY_CONFIGURE",
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
  "requestBody": "SeatHoldType",
  "responds": "SeatHoldType"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "ApprovalDecision": {
  "type": "object",
  "x-ticvai-persistence": "approvals.decision",
  "required": [
   "level",
   "principalId",
   "decision",
   "decidedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "level": {
    "type": "integer"
   },
   "principalId": {
    "type": "string",
    "format": "uuid"
   },
   "displayName": {
    "type": "string"
   },
   "isDelegate": {
    "type": "boolean"
   },
   "delegatedFrom": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "decision": {
    "type": "string",
    "enum": [
     "approve",
     "reject"
    ]
   },
   "comment": {
    "type": "string",
    "nullable": true
   },
   "reason": {
    "type": "string",
    "nullable": true
   },
   "usedMfa": {
    "type": "boolean"
   },
   "signatureRef": {
    "type": "string",
    "nullable": true
   },
   "decidedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "ApprovalKind": {
  "type": "string",
  "description": "11.1.7 and 11.1.30–11.1.37. **The first four already exist as bespoke implementations** and this contract is what they collapse into.\n**Which actions route here — decided 28 September, audit R144.** Finance and procurement acts go through this engine to a **finance approver**: closing a fiscal period (`periodClose`), reopening one (`periodReopen`), cancelling a purchase order (`purchaseOrderCancel`) and closing one short (`purchaseOrderShortClose`). The tenant default matrix for each of these names the finance approver role; a venue may tighten it and never loosen it. Starting a release rollout routes through `releasePromotion` to the platform release manager (a holder of `PLATFORM_RELEASE_PROMOTE`). **Not every `requiresApproval` goes here:** reopening a shift, recounting a stock count and a retail return above the venue threshold take a supervisor's step-up on the same device instead, and never raise a request.\n**Catalogue change requests route through `productChange` and `pricingChange`** (decided 29 September, writers pass): a product change and a price or pricing change raised in `catalogue` ask for approval under these two kinds, so a venue can route product edits and price edits to different approvers.\n",
  "enum": [
   "refund",
   "priceOverride",
   "discountOverride",
   "complimentaryTicket",
   "membershipCancellation",
   "accessPermissionChange",
   "configurationChange",
   "aiRecommendation",
   "releasePromotion",
   "requisition",
   "stockWriteOff",
   "journalEntry",
   "periodClose",
   "periodReopen",
   "purchaseOrderCancel",
   "purchaseOrderShortClose",
   "tenantMigration",
   "productChange",
   "pricingChange"
  ]
 },
 "ApprovalMode": {
  "type": "string",
  "description": "11.1.43–11.1.46. **Sequential** asks one at a time, **parallel** asks everyone at once, **consensus** needs all of them, **majority** needs more than half.\nParallel and consensus differ in when it completes: parallel completes on the first approval, consensus waits for all. Conflating them is how a four-eyes rule turns into a one-eye rule.\n",
  "enum": [
   "sequential",
   "parallel",
   "consensus",
   "majority"
  ]
 },
 "ApprovalRequest": {
  "type": "object",
  "x-ticvai-persistence": "approvals.request",
  "required": [
   "id",
   "kind",
   "status",
   "requestedByPrincipalId",
   "requestedAt"
  ],
  "properties": {
   "id": {
    "type": "string"
   },
   "kind": {
    "$ref": "#/components/schemas/ApprovalKind"
   },
   "rerouteOnNoApprover": {
    "type": "boolean",
    "default": true,
    "description": "BL-154. **An approver on leave is an approval that waits for them to come back.** Reroutes to the next in the chain rather than stalling — `workforce` already knows who is on leave, and an approval queue nobody is watching is the thing that stops a venue.\n"
   },
   "outOfOfficeDelegateId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "allowEmailApproval": {
    "type": "boolean",
    "default": false,
    "description": "**Approving from an email link with no second factor is the weakest path in the system**, so it is off by default and available only below a configured value.\n"
   },
   "reopenedFrom": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**Reopening a decided approval creates a new one that points back.** Editing a decision in place destroys the record of what was originally approved, which is the only thing an audit wants.\n"
   },
   "status": {
    "$ref": "#/components/schemas/ApprovalStatus"
   },
   "subjectContract": {
    "type": "string"
   },
   "subjectType": {
    "type": "string"
   },
   "subjectId": {
    "type": "string"
   },
   "scopePath": {
    "type": "string"
   },
   "summary": {
    "type": "string"
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "justification": {
    "type": "string",
    "nullable": true
   },
   "requestedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "matrixVersion": {
    "type": "integer"
   },
   "mode": {
    "$ref": "#/components/schemas/ApprovalMode"
   },
   "currentLevel": {
    "type": "integer"
   },
   "totalLevels": {
    "type": "integer"
   },
   "pendingApprovers": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "principalId": {
       "type": "string",
       "format": "uuid"
      },
      "displayName": {
       "type": "string"
      },
      "isDelegate": {
       "type": "boolean"
      }
     }
    }
   },
   "decisions": {
    "type": "array",
    "description": "Every decision at every level, in order. **Immutable once the request completes** (11.1.56) — an approval is evidence, and amending one is a different fact.\n",
    "items": {
     "$ref": "#/components/schemas/ApprovalDecision"
    }
   },
   "escalations": {
    "type": "array",
    "description": "11.1.48. Who was asked, when, and why it moved up. **Escalation adds an approver rather than replacing one**, so the original stays in the record.\n",
    "items": {
     "type": "object",
     "properties": {
      "at": {
       "type": "string",
       "format": "date-time"
      },
      "reason": {
       "type": "string"
      },
      "fromLevel": {
       "type": "integer"
      },
      "toLevel": {
       "type": "integer"
      },
      "wasAutomatic": {
       "type": "boolean"
      }
     }
    }
   },
   "resubmittedFromId": {
    "type": "string",
    "nullable": true
   },
   "reopenedFromId": {
    "type": "string",
    "nullable": true
   },
   "slaDueAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "slaBreached": {
    "type": "boolean"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "requestedAt": {
    "type": "string",
    "format": "date-time"
   },
   "completedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "aiAssessment": {
    "type": "object",
    "nullable": true,
    "readOnly": true,
    "description": "**AI context for the reviewer, never an input to the decision** (11.1.73 to 11.1.75; MoM 8 September; 29 September, build pass, group G2). Written by approvals from `ai.scoreApprovalRequest` on submit and on each SLA tick; null where AI is off or has not answered. Shown on the request labelled as AI; orders the inbox only when `sort=aiPriority` is asked for.",
    "properties": {
     "riskScore": {
      "type": "integer",
      "minimum": 0,
      "maximum": 100
     },
     "riskBand": {
      "type": "string",
      "enum": [
       "low",
       "medium",
       "high",
       "critical"
      ]
     },
     "priorityScore": {
      "type": "integer",
      "minimum": 0,
      "maximum": 100
     },
     "escalationSuggestion": {
      "type": "object",
      "description": "A suggestion a person may act on through `escalateApprovalRequest`, or the tenant's own SLA policy may; nothing escalates because of it.",
      "properties": {
       "action": {
        "type": "string",
        "enum": [
         "escalate",
         "addBackupApprover",
         "none"
        ]
       },
       "reason": {
        "type": "string",
        "nullable": true
       }
      }
     },
     "signals": {
      "type": "array",
      "maxItems": 10,
      "description": "The signals behind the scores, largest first, as `ai.AiApprovalRequestScore.signals`.",
      "items": {
       "type": "object",
       "properties": {
        "code": {
         "type": "string"
        },
        "contribution": {
         "type": "number"
        },
        "detail": {
         "type": "string",
         "nullable": true
        }
       }
      }
     },
     "scoreId": {
      "type": "string",
      "format": "uuid",
      "description": "The `ai.approval_request_score` row it was copied from; `ai.getApprovalRequestScore` gives the full context. Not a foreign key (the score lives in the AI service)."
     },
     "decisionRecordId": {
      "type": "string",
      "description": "The ai decision record, for the audit of what the AI said and why."
     },
     "assessedAt": {
      "type": "string",
      "format": "date-time"
     }
    }
   }
  }
 },
 "ApprovalStatus": {
  "type": "string",
  "enum": [
   "draft",
   "pending",
   "escalated",
   "returned",
   "informationRequested",
   "approved",
   "rejected",
   "withdrawn",
   "expired",
   "cancelled"
  ]
 },
 "CreateApprovalRequest": {
  "type": "object",
  "x-ticvai-persistence": "none — request only",
  "required": [
   "id",
   "kind",
   "subjectContract",
   "subjectType",
   "subjectId",
   "scopePath",
   "summary"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "$ref": "#/components/schemas/ApprovalKind"
   },
   "subjectContract": {
    "type": "string",
    "description": "Which contract owns the thing being approved."
   },
   "subjectType": {
    "type": "string"
   },
   "subjectId": {
    "type": "string",
    "description": "**A reference, never a copy.** A copy goes stale between raising and deciding, and an approver reading a stale copy approves something that no longer exists.\n"
   },
   "scopePath": {
    "type": "string"
   },
   "summary": {
    "type": "string",
    "maxLength": 300,
    "description": "What the approver sees in their queue before opening it."
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "attributes": {
    "type": "object",
    "additionalProperties": true
   },
   "justification": {
    "type": "string",
    "maxLength": 1000
   },
   "isDraft": {
    "type": "boolean",
    "default": false,
    "description": "True saves the request at `draft` without routing it; `submitApprovalRequest` sends it later (decided 28 September, audit R129).\n"
   }
  }
 },
 "SeatHoldPool": {
  "type": "object",
  "x-ticvai-persistence": "seating.hold_pool",
  "description": "Board 6.3. **Utilisation decides next season's allocation.**",
  "required": [
   "holdTypeId",
   "performanceId"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "holdTypeId": {
    "type": "string",
    "format": "uuid"
   },
   "performanceId": {
    "type": "string",
    "format": "uuid"
   },
   "seatIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "seatCount": {
    "type": "integer",
    "readOnly": true
   },
   "usedCount": {
    "type": "integer",
    "readOnly": true
   },
   "releasedCount": {
    "type": "integer",
    "readOnly": true
   },
   "holderName": {
    "type": "string",
    "nullable": true
   },
   "reason": {
    "type": "string",
    "nullable": true
   },
   "releaseAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "active",
     "partiallyReleased",
     "released",
     "expired"
    ]
   },
   "createdBy": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "SeatHoldType": {
  "type": "object",
  "x-ticvai-persistence": "seating.hold_type",
  "description": "Board 6.2. **A hold with no release rule becomes a permanent hole in the map.**",
  "required": [
   "code",
   "name"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "code": {
    "type": "string"
   },
   "name": {
    "type": "string"
   },
   "purpose": {
    "type": "string",
    "enum": [
     "production",
     "house",
     "accessibility",
     "press",
     "sponsor",
     "contractual",
     "maintenance",
     "distancing"
    ]
   },
   "ownerRole": {
    "type": "string",
    "nullable": true
   },
   "releaseRule": {
    "type": "string",
    "enum": [
     "manual",
     "hoursBeforePerformance",
     "onDate",
     "onSelloutThreshold"
    ],
    "default": "hoursBeforePerformance"
   },
   "releaseHoursBefore": {
    "type": "integer",
    "nullable": true
   },
   "releaseTo": {
    "type": "string",
    "enum": [
     "generalSale",
     "anotherPool",
     "remainsHeld"
    ],
    "default": "generalSale"
   },
   "countsAgainstCapacity": {
    "type": "boolean",
    "default": true,
    "description": "**Whether held seats are still \"sold out\".** A production hold that reads as availability puts a show on sale it cannot honour.\n"
   },
   "visibleToGuest": {
    "type": "boolean",
    "default": false
   },
   "scopePath": {
    "type": "string"
   }
  }
 }
}
```
