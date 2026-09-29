# WS171 — Seat Management Venue Mapping Reference v1.0 board 7

**10 screens · 5 operations · 3 schemas · 1 permissions**

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

- **Every control that can be refused must be gated.** 1 permissions apply here:
  `CAPACITY_CONFIGURE`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-1013` | Rules Command Center | listDetail | 1 | 0 | — |
| `BO-1014` | Seat Kill Rules | listDetail | 1 | 0 | — |
| `BO-1015` | Buffer Seat Rules | listDetail | 1 | 0 | — |
| `BO-1016` | Companion Seat Rules | listDetail | 1 | 0 | — |
| `BO-1017` | Wheelchair Companion Rules | listDetail | 2 | 0 | — |
| `BO-1018` | Accessible Seating Master | listDetail | 2 | 0 | — |
| `BO-1019` | Accessible Route Mapping | listDetail | 1 | 0 | — |
| `BO-1020` | Accessible Filters & Eligibility | listDetail | 1 | 0 | — |
| `BO-1021` | Flexible Spacing Rules | listDetail | 1 | 0 | — |
| `BO-1022` | Compliance Validation & Audit | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-1014, BO-1015, BO-1016, BO-1017, BO-1018, BO-1019, BO-1020, BO-1021 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-1013",
  "name": "Rules Command Center",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "7",
   "number": "01",
   "page": 30
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/rules-command-center-bo-1013",
   "component": "apps/venue-management-web/src/routes/access-venue/RulesCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-1014",
    "BO-1015",
    "BO-1016",
    "BO-1017",
    "BO-1018",
    "BO-1019",
    "BO-1020",
    "BO-1021",
    "BO-1022"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "BO-1014",
     "trigger": "Seat Kill Rules",
     "provenance": "structural — pack board 7 wiring, 19 September 2026"
    },
    {
     "to": "BO-1015",
     "trigger": "Buffer Seat Rules",
     "provenance": "structural — pack board 7 wiring, 19 September 2026"
    },
    {
     "to": "BO-1016",
     "trigger": "Companion Seat Rules",
     "provenance": "structural — pack board 7 wiring, 19 September 2026"
    },
    {
     "to": "BO-1017",
     "trigger": "Wheelchair Companion Rules",
     "provenance": "structural — pack board 7 wiring, 19 September 2026"
    },
    {
     "to": "BO-1018",
     "trigger": "Accessible Seating Master",
     "provenance": "structural — pack board 7 wiring, 19 September 2026"
    },
    {
     "to": "BO-1019",
     "trigger": "Accessible Route Mapping",
     "provenance": "structural — pack board 7 wiring, 19 September 2026"
    },
    {
     "to": "BO-1020",
     "trigger": "Accessible Filters & Eligibility",
     "provenance": "structural — pack board 7 wiring, 19 September 2026"
    },
    {
     "to": "BO-1021",
     "trigger": "Flexible Spacing Rules",
     "provenance": "structural — pack board 7 wiring, 19 September 2026"
    },
    {
     "to": "BO-1022",
     "trigger": "Compliance Validation & Audit",
     "provenance": "structural — pack board 7 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Monitor seating-rule coverage, violations and compliance across venues. Show total and active rules, affected seats, open violations, capacity impact and venue compliance score. Filter by rule category, tenant, venue, event, layout, effective date, owner and severity. Surface missing accessible mappings, conflicting buffers and production changes requiring revalidation. Accessibility inventory and companion rules shall be policy-driven and auditable; overrides require authority and reason and must not unlawfully reduce accessible availability. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 30"
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
       "label": "Seat map",
       "operation": "getSeatRules",
       "notes": "Sends `?seatMapId=`.",
       "provenance": "contract seating.yaml GET /seat-rules"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Killed seats",
       "bindsTo": "SeatRules",
       "columns": [
        "SeatRules.killedSeatIds"
       ],
       "operation": "getSeatRules",
       "notes": "Count of `killedSeatIds`.",
       "provenance": "contract seating.yaml GET /seat-rules"
      },
      {
       "kind": "metricTile",
       "label": "Buffer rule",
       "bindsTo": "SeatRules.bufferRule",
       "columns": [
        "SeatRules.bufferRule.enabled"
       ],
       "operation": "getSeatRules",
       "provenance": "contract seating.yaml GET /seat-rules"
      },
      {
       "kind": "metricTile",
       "label": "Companion rule",
       "bindsTo": "SeatRules.companionRule",
       "columns": [
        "SeatRules.companionRule.enabled"
       ],
       "operation": "getSeatRules",
       "provenance": "contract seating.yaml GET /seat-rules"
      },
      {
       "kind": "metricTile",
       "label": "Open violations",
       "columns": [
        "Open violations"
       ],
       "notes": "The pack asks for open violations; the contract has no field for it.",
       "provenance": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 30"
      },
      {
       "kind": "metricTile",
       "label": "Venue compliance score",
       "columns": [
        "Venue compliance score"
       ],
       "notes": "The pack asks for venue compliance score; the contract has no field for it.",
       "provenance": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 30"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Killed seats and reasons",
       "bindsTo": "SeatRules",
       "columns": [
        "SeatRules.killedSeatIds",
        "SeatRules.killReasons"
       ],
       "operation": "getSeatRules",
       "notes": "One row per killed seat with its reason from `killReasons`.",
       "provenance": "contract seating.yaml GET /seat-rules"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "Rules in force",
       "bindsTo": "SeatRules",
       "columns": [
        "SeatRules.seatMapId",
        "SeatRules.scopePath",
        "SeatRules.bufferRule.seatsEitherSide",
        "SeatRules.bufferRule.rowsEitherSide",
        "SeatRules.bufferRule.avoidSingleGaps",
        "SeatRules.companionRule.pairs",
        "SeatRules.companionRule.releaseCompanionHoursBefore",
        "SeatRules.flexibleSpacing.enabled",
        "SeatRules.flexibleSpacing.densityPercent",
        "SeatRules.flexibleSpacing.perPerformanceOverride"
       ],
       "operation": "getSeatRules",
       "provenance": "contract seating.yaml GET /seat-rules"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The rules list.",
   "error": "Could not load. Names which read failed and leaves the rules untouched.",
   "emptyFirstRun": "No rules yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the rules are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getSeatRules",
    "contract": "seating",
    "purpose": "Rules in force",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1013",
   "workshopBoard": "wireframes/WS146 Seat Management Venue Mapping Reference v1.0 Board 7.dc.html#bo-1013"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 30. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Layout drafted 29 September (VM close-out)** from pack Seat_Management_Venue_Mapping_Reference v1.0.pdf p.30; contract seating.yaml GET /seat-rules. Pack labels with no schema field yet (shown as plain labels): Open violations, Venue compliance score, Total / active rules, Capacity impact, Missing accessible mappings, Conflicting buffers, Filters: rule category, venue, event, effective date, owner, severity.",
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
  "id": "BO-1014",
  "name": "Seat Kill Rules",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "7",
   "number": "02",
   "page": 30
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/seat-kill-rules-bo-1014",
   "component": "apps/venue-management-web/src/routes/access-venue/SeatKillRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1013"
   ],
   "exitTo": [
    "BO-1013"
   ],
   "transitions": [
    {
     "to": "BO-1013",
     "trigger": "Back to Rules Command Center",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Remove seats from sale based on permanent or conditional unusability. Configure sightline, stage, production, obstruction, equipment, safety, maintenance and venue-defined kill reasons. Apply by seat list, section, row, polygon, obstruction distance, event type or layout condition. Preview affected capacity, sold/reserved inventory and alternative seating before activation. Accessibility inventory and companion rules shall be policy-driven and auditable; overrides require authority and reason and must not unlawfully reduce accessible availability. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 30"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 30"
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
       "impliedBy": "setSeatRules",
       "label": "Save seat rules",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setSeatRules"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The seat kill rules list.",
   "error": "Could not load. Names which read failed and leaves the seat kill rules untouched.",
   "emptyFirstRun": "No seat kill rules yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the seat kill rules are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setSeatRules",
    "contract": "seating",
    "purpose": "Kill a seat, with a reason",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getSeatRules",
     "getSeatInventory"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1014",
   "workshopBoard": "wireframes/WS146 Seat Management Venue Mapping Reference v1.0 Board 7.dc.html#bo-1014"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 30. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1015",
  "name": "Buffer Seat Rules",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "7",
   "number": "03",
   "page": 30
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/buffer-seat-rules-bo-1015",
   "component": "apps/venue-management-web/src/routes/access-venue/BufferSeatRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1013"
   ],
   "exitTo": [
    "BO-1013"
   ],
   "transitions": [
    {
     "to": "BO-1013",
     "trigger": "Back to Rules Command Center",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Create controlled unsold spacing around seats, zones or production objects. Define left/right, radial, row, perimeter, alternating or custom buffer patterns and minimum distance. Apply dynamically around selected seats, wheelchair spaces, camera positions, stages or restricted zones. Configure release behavior, priority, interaction with holds and treatment when a buffer conflicts with a sale. Accessibility inventory and companion rules shall be policy-driven and auditable; overrides require authority and reason and must not unlawfully reduce accessible availability. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history. Configuration Scope of Work | Version 1.0 30",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 30"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 30"
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
       "impliedBy": "setSeatRules",
       "label": "Save seat rules",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setSeatRules"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The buffer seat rules list.",
   "error": "Could not load. Names which read failed and leaves the buffer seat rules untouched.",
   "emptyFirstRun": "No buffer seat rules yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the buffer seat rules are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setSeatRules",
    "contract": "seating",
    "purpose": "Buffer seats around a sale",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getSeatRules",
     "getSeatInventory"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1015",
   "workshopBoard": "wireframes/WS146 Seat Management Venue Mapping Reference v1.0 Board 7.dc.html#bo-1015"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 30. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1016",
  "name": "Companion Seat Rules",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "7",
   "number": "04",
   "page": 31
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/companion-seat-rules-bo-1016",
   "component": "apps/venue-management-web/src/routes/access-venue/CompanionSeatRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1013"
   ],
   "exitTo": [
    "BO-1013"
   ],
   "transitions": [
    {
     "to": "BO-1013",
     "trigger": "Back to Rules Command Center",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Keep appropriate companion inventory linked to designated seats. Configure eligible seat types, adjacency, ratio, maximum companions and same-row or nearby rules. Control whether companions must be selected together and when unneeded companion seats may be released. Support family, premium, group and venue-defined companion policies without overriding wheelchair-specific rules. Accessibility inventory and companion rules shall be policy-driven and auditable; overrides require authority and reason and must not unlawfully reduce accessible availability. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 31"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 31"
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
       "impliedBy": "setSeatRules",
       "label": "Save seat rules",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setSeatRules"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The companion seat rules list.",
   "error": "Could not load. Names which read failed and leaves the companion seat rules untouched.",
   "emptyFirstRun": "No companion seat rules yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the companion seat rules are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setSeatRules",
    "contract": "seating",
    "purpose": "Companion pairing",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getSeatRules",
     "getSeatInventory"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1016",
   "workshopBoard": "wireframes/WS146 Seat Management Venue Mapping Reference v1.0 Board 7.dc.html#bo-1016"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 31. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1017",
  "name": "Wheelchair Companion Rules",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "7",
   "number": "05",
   "page": 31
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/wheelchair-companion-rules-bo-1017",
   "component": "apps/venue-management-web/src/routes/access-venue/WheelchairCompanionRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1013"
   ],
   "exitTo": [
    "BO-1013"
   ],
   "transitions": [
    {
     "to": "BO-1013",
     "trigger": "Back to Rules Command Center",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Manage wheelchair-space and companion-seat pairing. Define one-to-one or configurable ratios, adjacency, transfer-seat eligibility and alternative companion locations. Require wheelchair space selection before companion inventory where policy permits and explain the rule clearly. Control release to general sale only through approved timing, evidence and accessible-demand safeguards. Accessibility inventory and companion rules shall be policy-driven and auditable; overrides require authority and reason and must not unlawfully reduce accessible availability. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 31"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 31"
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
       "impliedBy": "setSeatRules",
       "label": "Save seat rules",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setSeatRules"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The wheelchair companion rules list.",
   "error": "Could not load. Names which read failed and leaves the wheelchair companion rules untouched.",
   "emptyFirstRun": "No wheelchair companion rules yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the wheelchair companion rules are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setSeatRules",
    "contract": "seating",
    "purpose": "Wheelchair companion rules",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getSeatRules",
     "getSeatInventory"
    ]
   },
   {
    "operationId": "getAccessibleSeating",
    "contract": "seating",
    "purpose": "The spaces being paired",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1017",
   "workshopBoard": "wireframes/WS146 Seat Management Venue Mapping Reference v1.0 Board 7.dc.html#bo-1017"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 31. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1018",
  "name": "Accessible Seating Master",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "7",
   "number": "06",
   "page": 31
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/accessible-seating-master-bo-1018",
   "component": "apps/venue-management-web/src/routes/access-venue/AccessibleSeatingMaster.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1013"
   ],
   "exitTo": [
    "BO-1013"
   ],
   "transitions": [
    {
     "to": "BO-1013",
     "trigger": "Back to Rules Command Center",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Maintain a standard catalog of accessible seat and space attributes. Configure wheelchair, companion, ambulatory, transfer, hearing, vision, service-animal and other supported types. Store dimensions, capacity treatment, route requirements, amenities, assisted access and display labels. Map each type to venue inventory, ticket products, customer-facing filters and compliance reporting. Accessibility inventory and companion rules shall be policy-driven and auditable; overrides require authority and reason and must not unlawfully reduce accessible availability. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 31"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 31"
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
       "impliedBy": "setAccessibleSeating",
       "label": "Save accessible seating",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setAccessibleSeating"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The accessible seating master list.",
   "error": "Could not load. Names which read failed and leaves the accessible seating master untouched.",
   "emptyFirstRun": "No accessible seating master yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the accessible seating master are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getAccessibleSeating",
    "contract": "seating",
    "purpose": "The accessible inventory",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "setAccessibleSeating",
    "contract": "seating",
    "purpose": "Define it",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getAccessibleSeating",
     "validateSeatCompliance"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1018",
   "workshopBoard": "wireframes/WS146 Seat Management Venue Mapping Reference v1.0 Board 7.dc.html#bo-1018"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 31. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1019",
  "name": "Accessible Route Mapping",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "7",
   "number": "07",
   "page": 31
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/accessible-route-mapping-bo-1019",
   "component": "apps/venue-management-web/src/routes/access-venue/AccessibleRouteMapping.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1013"
   ],
   "exitTo": [
    "BO-1013"
   ],
   "transitions": [
    {
     "to": "BO-1013",
     "trigger": "Back to Rules Command Center",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Identify accessible journeys from entry to seats and facilities. Create routes through accessible entrances, lifts, ramps, concourses, restrooms and designated seating. Store distance, slope, level changes, width, surface, assistance requirement and temporary closure status. Validate route continuity and show impact when a layout, facility or access point becomes unavailable. Accessibility inventory and companion rules shall be policy-driven and auditable; overrides require authority and reason and must not unlawfully reduce accessible availability. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history. Configuration Scope of Work | Version 1.0 31",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 31"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 31"
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
       "impliedBy": "setAccessibleSeating",
       "label": "Save accessible seating",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setAccessibleSeating"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The accessible route mapping list.",
   "error": "Could not load. Names which read failed and leaves the accessible route mapping untouched.",
   "emptyFirstRun": "No accessible route mapping yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the accessible route mapping are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setAccessibleSeating",
    "contract": "seating",
    "purpose": "Routes to each space",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getAccessibleSeating",
     "validateSeatCompliance"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1019",
   "workshopBoard": "wireframes/WS146 Seat Management Venue Mapping Reference v1.0 Board 7.dc.html#bo-1019"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 31. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1020",
  "name": "Accessible Filters & Eligibility",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "7",
   "number": "08",
   "page": 32
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/accessible-filters-eligibility-bo-1020",
   "component": "apps/venue-management-web/src/routes/access-venue/AccessibleFiltersEligibility.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1013"
   ],
   "exitTo": [
    "BO-1013"
   ],
   "transitions": [
    {
     "to": "BO-1013",
     "trigger": "Back to Rules Command Center",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure inclusive discovery without exposing sensitive guest information. Define filters and labels for wheelchair, companion, aisle, step-free, transfer, hearing, vision and service-animal needs. Configure eligibility attestation, documentation policy where lawful, assisted-sale path and privacy restrictions. Preview the B2C, mobile, POS and call-center experience and ensure equivalent inventory visibility. Accessibility inventory and companion rules shall be policy-driven and auditable; overrides require authority and reason and must not unlawfully reduce accessible availability. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 32"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 32"
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
       "impliedBy": "setAccessibleSeating",
       "label": "Save accessible seating",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setAccessibleSeating"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The accessible filters eligibility list.",
   "error": "Could not load. Names which read failed and leaves the accessible filters eligibility untouched.",
   "emptyFirstRun": "No accessible filters eligibility yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the accessible filters eligibility are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setAccessibleSeating",
    "contract": "seating",
    "purpose": "Who may buy them",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getAccessibleSeating",
     "validateSeatCompliance"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1020",
   "workshopBoard": "wireframes/WS146 Seat Management Venue Mapping Reference v1.0 Board 7.dc.html#bo-1020"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 32. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1021",
  "name": "Flexible Spacing Rules",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "7",
   "number": "09",
   "page": 32
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/flexible-spacing-rules-bo-1021",
   "component": "apps/venue-management-web/src/routes/access-venue/FlexibleSpacingRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1013"
   ],
   "exitTo": [
    "BO-1013"
   ],
   "transitions": [
    {
     "to": "BO-1013",
     "trigger": "Back to Rules Command Center",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Support temporary public-health or operational spacing requirements. Configure distance, seat count, checkerboard, blocked-row, household-group and custom patterns. Apply by event, venue, zone, seat type or time window and preview capacity and revenue impact. Coordinate with group seating, accessible inventory, holds and sold seats and prevent retroactive unsafe changes. Accessibility inventory and companion rules shall be policy-driven and auditable; overrides require authority and reason and must not unlawfully reduce accessible availability. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 32"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 32"
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
       "impliedBy": "setSeatRules",
       "label": "Save seat rules",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setSeatRules"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The flexible spacing rules list.",
   "error": "Could not load. Names which read failed and leaves the flexible spacing rules untouched.",
   "emptyFirstRun": "No flexible spacing rules yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the flexible spacing rules are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setSeatRules",
    "contract": "seating",
    "purpose": "Flexible spacing and density",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getSeatRules",
     "getSeatInventory"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1021",
   "workshopBoard": "wireframes/WS146 Seat Management Venue Mapping Reference v1.0 Board 7.dc.html#bo-1021"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 32. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1022",
  "name": "Compliance Validation & Audit",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "7",
   "number": "10",
   "page": 32
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/compliance-validation-audit-bo-1022",
   "component": "apps/venue-management-web/src/routes/access-venue/ComplianceValidationAudit.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1013"
   ],
   "exitTo": [
    "BO-1013"
   ],
   "transitions": [
    {
     "to": "BO-1013",
     "trigger": "Back to Rules Command Center",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Demonstrate that seating rules and accessibility configuration are complete and enforced. Run validations for accessible quantities, companion ratios, route continuity, conflicts, labels and customer-channel parity. Provide issue severity, affected inventory, rule reference, owner, deadline, remediation and evidence. Retain configuration, approval, enforcement, release and override history with controlled compliance export. Accessibility inventory and companion rules shall be policy-driven and auditable; overrides require authority and reason and must not unlawfully reduce accessible availability. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history. Configuration Scope of Work | Version 1.0 32 Board 8 - Group Reservations & Bulk Allocation Figure 8. High-definition configuration board with all 10 screens. Visual reference: information architecture and configuration coverage; detailed production behavior is defined in the following scope. Configuration Scope of Work | Version 1.0 33",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 32"
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
       "label": "Seat map",
       "operation": "validateSeatCompliance",
       "notes": "Sends `?seatMapId=` (required).",
       "provenance": "contract seating.yaml GET /seat-compliance"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Breaches",
       "bindsTo": "SeatComplianceFinding",
       "columns": [
        "SeatComplianceFinding.severity"
       ],
       "operation": "validateSeatCompliance",
       "notes": "Count where `severity` is breach.",
       "provenance": "contract seating.yaml GET /seat-compliance"
      },
      {
       "kind": "metricTile",
       "label": "Warnings",
       "bindsTo": "SeatComplianceFinding",
       "columns": [
        "SeatComplianceFinding.severity"
       ],
       "operation": "validateSeatCompliance",
       "notes": "Count where `severity` is warning.",
       "provenance": "contract seating.yaml GET /seat-compliance"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Findings",
       "bindsTo": "SeatComplianceFinding",
       "columns": [
        "SeatComplianceFinding.code",
        "SeatComplianceFinding.severity",
        "SeatComplianceFinding.message",
        "SeatComplianceFinding.required",
        "SeatComplianceFinding.actual",
        "SeatComplianceFinding.affectedSeatIds",
        "Owner",
        "Deadline"
       ],
       "operation": "validateSeatCompliance",
       "notes": "Accessible quantities, companion ratios, route continuity, conflicts, labels and channel parity.",
       "provenance": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 32"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected finding",
       "bindsTo": "SeatComplianceFinding",
       "columns": [
        "SeatComplianceFinding.code",
        "SeatComplianceFinding.severity",
        "SeatComplianceFinding.message",
        "SeatComplianceFinding.required",
        "SeatComplianceFinding.actual",
        "SeatComplianceFinding.affectedSeatIds",
        "Rule reference",
        "Remediation",
        "Evidence"
       ],
       "operation": "validateSeatCompliance",
       "notes": "Rule reference, remediation and evidence are pack labels.",
       "provenance": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 32"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "secondaryButton",
       "label": "Run validation",
       "operation": "validateSeatCompliance",
       "notes": "Re-runs the checks.",
       "provenance": "contract seating.yaml GET /seat-compliance"
      },
      {
       "kind": "secondaryButton",
       "label": "Export compliance evidence",
       "provenance": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 32"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The compliance validation audit list.",
   "error": "Could not load. Names which read failed and leaves the compliance validation audit untouched.",
   "emptyFirstRun": "No compliance validation audit yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the compliance validation audit are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "validateSeatCompliance",
    "contract": "seating",
    "purpose": "Whether the map still complies",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1022",
   "workshopBoard": "wireframes/WS146 Seat Management Venue Mapping Reference v1.0 Board 7.dc.html#bo-1022"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 32. 0 of 0 labels bound to a contract property; 0 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Layout drafted 29 September (VM close-out)** from pack Seat_Management_Venue_Mapping_Reference v1.0.pdf p.32; contract seating.yaml GET /seat-compliance. Pack labels with no schema field yet (shown as plain labels): Rule reference, Owner, Deadline, Remediation, Evidence.",
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
 "getAccessibleSeating": {
  "method": "GET",
  "path": "/accessible-seating",
  "contract": "seating",
  "summary": "Accessible seats, their routes and who may buy them",
  "permission": "CAPACITY_CONFIGURE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "seatMapId",
    "in": "query",
    "required": true
   }
  ],
  "requestBody": null,
  "responds": "AccessibleSeating"
 },
 "getSeatRules": {
  "method": "GET",
  "path": "/seat-rules",
  "contract": "seating",
  "summary": "Kill, buffer, companion and accessibility rules",
  "permission": "CAPACITY_CONFIGURE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "seatMapId",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "SeatRules"
 },
 "setAccessibleSeating": {
  "method": "PUT",
  "path": "/accessible-seating",
  "contract": "seating",
  "summary": "Define accessible seats, routes and eligibility",
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
  "requestBody": "AccessibleSeating",
  "responds": "AccessibleSeating"
 },
 "setSeatRules": {
  "method": "PUT",
  "path": "/seat-rules",
  "contract": "seating",
  "summary": "Which seats are killed, buffered, paired or reserved for access",
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
  "requestBody": "SeatRules",
  "responds": "SeatRules"
 },
 "validateSeatCompliance": {
  "method": "GET",
  "path": "/seat-compliance",
  "contract": "seating",
  "summary": "Whether the map still meets its obligations",
  "permission": "CAPACITY_CONFIGURE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "seatMapId",
    "in": "query",
    "required": true
   }
  ],
  "requestBody": null,
  "responds": "SeatComplianceFinding"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AccessibleSeating": {
  "type": "object",
  "x-ticvai-persistence": "seating.accessible",
  "description": "Boards 7.6 to 7.8. **An accessible seat with no accessible route is not an accessible seat.**\n",
  "properties": {
   "seatMapId": {
    "type": "string",
    "format": "uuid"
   },
   "spaces": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "seatId": {
       "type": "string",
       "format": "uuid"
      },
      "kind": {
       "type": "string",
       "enum": [
        "wheelchairSpace",
        "transferSeat",
        "ambulant",
        "easyAccess",
        "assistanceDog",
        "hearingLoop",
        "visuallyImpaired"
       ]
      },
      "routeDescription": {
       "type": "string",
       "nullable": true
      },
      "stepFree": {
       "type": "boolean",
       "default": true
      },
      "nearestAccessibleWc": {
       "type": "string",
       "nullable": true
      }
     }
    }
   },
   "eligibility": {
    "type": "string",
    "enum": [
     "open",
     "selfDeclared",
     "verifiedOnce",
     "verifiedEachTime"
    ],
    "default": "selfDeclared",
    "description": "**Contested in both directions.** Open sale leaves none for the guests who need them; hard gating turns people away at the door.\n"
   },
   "minimumProvisionPercent": {
    "type": "number",
    "nullable": true
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "SeatComplianceFinding": {
  "type": "object",
  "description": "Board 7.10. **A map drifts below its obligation one kill rule at a time.**",
  "properties": {
   "code": {
    "type": "string"
   },
   "severity": {
    "type": "string",
    "enum": [
     "breach",
     "warning",
     "advisory"
    ]
   },
   "message": {
    "type": "string"
   },
   "required": {
    "type": "number",
    "nullable": true
   },
   "actual": {
    "type": "number",
    "nullable": true
   },
   "affectedSeatIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   }
  }
 },
 "SeatRules": {
  "type": "object",
  "x-ticvai-persistence": "seating.seat_rules",
  "description": "Board 7. **Four rules that move the same seats and are decided by different people.**\n",
  "properties": {
   "seatMapId": {
    "type": "string",
    "format": "uuid"
   },
   "killedSeatIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "killReasons": {
    "type": "object",
    "additionalProperties": {
     "type": "string"
    }
   },
   "bufferRule": {
    "type": "object",
    "properties": {
     "enabled": {
      "type": "boolean",
      "default": false
     },
     "seatsEitherSide": {
      "type": "integer",
      "default": 1
     },
     "rowsEitherSide": {
      "type": "integer",
      "default": 0
     },
     "avoidSingleGaps": {
      "type": "boolean",
      "default": true,
      "description": "**The commercial case for buffers.** A map leaving one empty seat between every party has lost those seats without anybody deciding to.\n"
     }
    }
   },
   "companionRule": {
    "type": "object",
    "description": "**The one with legal weight.** Selling the companion seat separately strands a carer.\n",
    "properties": {
     "enabled": {
      "type": "boolean",
      "default": true
     },
     "pairs": {
      "type": "array",
      "items": {
       "type": "object",
       "properties": {
        "wheelchairSpaceId": {
         "type": "string",
         "format": "uuid"
        },
        "companionSeatIds": {
         "type": "array",
         "items": {
          "type": "string",
          "format": "uuid"
         }
        }
       }
      }
     },
     "releaseCompanionHoursBefore": {
      "type": "integer",
      "nullable": true
     }
    }
   },
   "flexibleSpacing": {
    "type": "object",
    "properties": {
     "enabled": {
      "type": "boolean",
      "default": false
     },
     "densityPercent": {
      "type": "integer",
      "nullable": true
     },
     "perPerformanceOverride": {
      "type": "boolean",
      "default": true
     }
    }
   },
   "scopePath": {
    "type": "string"
   }
  }
 }
}
```
