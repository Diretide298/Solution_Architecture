# WS167 — Seat Management Venue Mapping Reference v1.0 board 3

**10 screens · 14 operations · 13 schemas · 3 permissions**

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
  `ACCESS_POINT_CONFIGURE, CAPACITY_CONFIGURE, PRODUCT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-973` | Layout Command Center | listDetail | 1 | 0 | — |
| `BO-974` | Template Library | listDetail | 2 | 0 | — |
| `BO-975` | Event-Specific Layout | listDetail | 2 | 0 | — |
| `BO-976` | Clone & Inheritance | listDetail | 2 | 0 | — |
| `BO-977` | Version Compare | listDetail | 1 | 0 | — |
| `BO-978` | Multi-Performance Assignment | listDetail | 2 | 0 | — |
| `BO-979` | Temporary Seat Blocking | listDetail | 2 | 0 | — |
| `BO-980` | Scheduled Seat Release | listDetail | 2 | 0 | — |
| `BO-981` | Conflict & Impact Simulation | listDetail | 1 | 0 | — |
| `BO-982` | Approval, Publish & Rollback | listDetail | 2 | 0 | — |

## Thin screens in this batch

**BO-973, BO-974, BO-976, BO-979, BO-981, BO-982 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-973",
  "name": "Layout Command Center",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "3",
   "number": "01",
   "page": 14
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/layout-command-center-bo-973",
   "component": "apps/venue-management-web/src/routes/access-venue/LayoutCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-974",
    "BO-975",
    "BO-976",
    "BO-977",
    "BO-978",
    "BO-979",
    "BO-980",
    "BO-981",
    "BO-982"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "BO-974",
     "trigger": "Template Library",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "BO-975",
     "trigger": "Event-Specific Layout",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "BO-976",
     "trigger": "Clone & Inheritance",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "BO-977",
     "trigger": "Version Compare",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "BO-978",
     "trigger": "Multi-Performance Assignment",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "BO-979",
     "trigger": "Temporary Seat Blocking",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "BO-980",
     "trigger": "Scheduled Seat Release",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "BO-981",
     "trigger": "Conflict & Impact Simulation",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "BO-982",
     "trigger": "Approval, Publish & Rollback",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Manage layouts, versions and performance assignments from one operational view. Show active layouts, draft versions, total capacity, utilization, upcoming changes, validation issues and approval status. List layouts by venue, template, event, performance, version, owner, status and effective period. Surface urgent sold-seat impact, missing assignment and publication conflicts with direct remediation links. Preserve version lineage and require impact analysis for every change affecting capacity, products, sold seats, holds, access routes or pricing. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 14"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 14"
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
       "impliedBy": "listSeatMaps",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The layout list.",
   "error": "Could not load. Names which read failed and leaves the layout untouched.",
   "emptyFirstRun": "No layout yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the layout are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listSeatMaps",
    "contract": "seating",
    "purpose": "Layouts in use",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-973",
   "workshopBoard": "wireframes/WS142 Seat Management Venue Mapping Reference v1.0 Board 3.dc.html#bo-973"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 14. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-974",
  "name": "Template Library",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "3",
   "number": "02",
   "page": 14
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/template-library-bo-974",
   "component": "apps/venue-management-web/src/routes/access-venue/TemplateLibrary.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-973"
   ],
   "exitTo": [
    "BO-973"
   ],
   "transitions": [
    {
     "to": "BO-973",
     "trigger": "Back to Layout Command Center",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Maintain reusable layouts for common venue configurations. Provide templates for end-stage, center-stage, sports, theatre, banquet, classroom and venue-defined patterns. Store capacity, focal point, production footprint, section availability, access routes and default blocked inventory. Support preview, clone, compare, archive, ownership and controlled sharing across authorized tenants or venues. Preserve version lineage and require impact analysis for every change affecting capacity, products, sold seats, holds, access routes or pricing. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 14"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 14"
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
       "impliedBy": "listSeatMapTemplates",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createSeatMapTemplate",
       "label": "Create seat map template",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createSeatMapTemplate"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The template list.",
   "error": "Could not load. Names which read failed and leaves the template untouched.",
   "emptyFirstRun": "No template yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the template are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listSeatMapTemplates",
    "contract": "seating",
    "purpose": "The library",
    "trigger": "onLoad"
   },
   {
    "operationId": "createSeatMapTemplate",
    "contract": "seating",
    "purpose": "Add to the library",
    "trigger": "onAction",
    "invalidates": [
     "listSeatMapTemplates"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-974",
   "workshopBoard": "wireframes/WS142 Seat Management Venue Mapping Reference v1.0 Board 3.dc.html#bo-974"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 14. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-975",
  "name": "Event-Specific Layout",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "3",
   "number": "03",
   "page": 14
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/event-specific-layout-bo-975",
   "component": "apps/venue-management-web/src/routes/access-venue/EventSpecificLayout.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-973"
   ],
   "exitTo": [
    "BO-973"
   ],
   "transitions": [
    {
     "to": "BO-973",
     "trigger": "Back to Layout Command Center",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Create a seating layout tailored to one event or production. Start from the current venue map or approved template and adjust stage, field, sections, rows, seats, aisles and facilities. Display live capacity by section/category and affected pricing, products, access gates and operational resources. Support drafts, notes, attachments, production requirements and validation before performance assignment. Preserve version lineage and require impact analysis for every change affecting capacity, products, sold seats, holds, access routes or pricing. Configuration Scope of Work | Version 1.0 14 Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 14"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 14"
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
       "impliedBy": "getSeatMap",
       "notes": "One record, read-only."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "publishSeatMap",
       "label": "Publish seat map",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "publishSeatMap"
      },
      {
       "kind": "publishGate",
       "label": "What publishing changes",
       "notes": "**Replaces the map every channel sells from.** Seats already sold keep their labels; seats that no longer exist in the new map are listed before this proceeds.",
       "provenance": "authored — required by check-screens, 19 September 2026"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The event-specific layout list.",
   "error": "Could not load. Names which read failed and leaves the event-specific layout untouched.",
   "emptyFirstRun": "No event-specific layout yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the event-specific layout are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getSeatMap",
    "contract": "seating",
    "purpose": "The layout for this event",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "publishSeatMap",
    "contract": "seating",
    "purpose": "Publish it",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-975",
   "workshopBoard": "wireframes/WS142 Seat Management Venue Mapping Reference v1.0 Board 3.dc.html#bo-975"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 14. 0 of 0 labels bound to a contract property; 0 of 10 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "seatMapId",
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
  "id": "BO-976",
  "name": "Clone & Inheritance",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "3",
   "number": "04",
   "page": 15
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/clone-inheritance-bo-976",
   "component": "apps/venue-management-web/src/routes/access-venue/CloneInheritance.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-973"
   ],
   "exitTo": [
    "BO-973"
   ],
   "transitions": [
    {
     "to": "BO-973",
     "trigger": "Back to Layout Command Center",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Reuse a layout without losing the relationship to its approved source. Clone a layout for another event, venue or performance and select which settings are inherited, copied or excluded. Show inherited versus overridden geometry, categories, holds, accessibility, pricing and production settings. Warn when later source changes could affect dependent clones and require explicit synchronization decisions. Preserve version lineage and require impact analysis for every change affecting capacity, products, sold seats, holds, access routes or pricing. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 15"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 15"
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
       "impliedBy": "cloneSeatMap",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "cloneSeatMap"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The clone inheritance list.",
   "error": "Could not load. Names which read failed and leaves the clone inheritance untouched.",
   "emptyFirstRun": "No clone inheritance yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the clone inheritance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "cloneSeatMap",
    "contract": "seating",
    "purpose": "Copy a whole map",
    "trigger": "onAction",
    "invalidates": [
     "listSeatMaps"
    ]
   },
   {
    "operationId": "copySeatMapSection",
    "contract": "seating",
    "purpose": "Copy one section into another map",
    "trigger": "onAction",
    "invalidates": [
     "getSeatMap"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-976",
   "workshopBoard": "wireframes/WS142 Seat Management Venue Mapping Reference v1.0 Board 3.dc.html#bo-976"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 15. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "seatMapId",
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
  "id": "BO-977",
  "name": "Version Compare",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "3",
   "number": "05",
   "page": 15
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/version-compare-bo-977",
   "component": "apps/venue-management-web/src/routes/access-venue/VersionCompare.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-973"
   ],
   "exitTo": [
    "BO-973"
   ],
   "transitions": [
    {
     "to": "BO-973",
     "trigger": "Back to Layout Command Center",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Review exact differences between layout versions before approval or rollback. Provide side-by-side and overlay comparisons of added, removed, moved and changed sections, rows, seats and routes. Summarize capacity, accessible inventory, pricing, hold, product and revenue impact by category. Link each change to actor, timestamp, request, reason, approval and impacted performance. Preserve version lineage and require impact analysis for every change affecting capacity, products, sold seats, holds, access routes or pricing. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 15"
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
       "label": "From version",
       "operation": "diffSeatMapVersions",
       "notes": "Sends `?fromVersion=` (required); `seatMapId` is the path.",
       "provenance": "contract seating.yaml GET /seat-maps/{seatMapId}/diff"
      },
      {
       "kind": "selectField",
       "label": "To version",
       "operation": "diffSeatMapVersions",
       "notes": "Sends `?toVersion=` (required).",
       "provenance": "contract seating.yaml GET /seat-maps/{seatMapId}/diff"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Seats",
       "bindsTo": "SeatMapDiff",
       "columns": [
        "SeatMapDiff.seatCountBefore",
        "SeatMapDiff.seatCountAfter"
       ],
       "operation": "diffSeatMapVersions",
       "provenance": "contract seating.yaml GET /seat-maps/{seatMapId}/diff"
      },
      {
       "kind": "metricTile",
       "label": "Accessible seats",
       "bindsTo": "SeatMapDiff",
       "columns": [
        "SeatMapDiff.accessibleSeatsBefore",
        "SeatMapDiff.accessibleSeatsAfter"
       ],
       "operation": "diffSeatMapVersions",
       "provenance": "contract seating.yaml GET /seat-maps/{seatMapId}/diff"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Changed sections",
       "bindsTo": "SeatMapDiff.sectionsChanged",
       "columns": [
        "SeatMapDiff.sectionsChanged[].section",
        "SeatMapDiff.sectionsChanged[].seatsBefore",
        "SeatMapDiff.sectionsChanged[].seatsAfter",
        "SeatMapDiff.sectionsChanged[].summary",
        "Actor",
        "Timestamp",
        "Reason",
        "Approval"
       ],
       "operation": "diffSeatMapVersions",
       "notes": "The pack links each change to actor, timestamp, request, reason and approval; the diff does not.",
       "provenance": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 15"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "Added and removed sections",
       "bindsTo": "SeatMapDiff",
       "columns": [
        "SeatMapDiff.fromVersion",
        "SeatMapDiff.toVersion",
        "SeatMapDiff.sectionsAdded",
        "SeatMapDiff.sectionsRemoved"
       ],
       "operation": "diffSeatMapVersions",
       "provenance": "contract seating.yaml GET /seat-maps/{seatMapId}/diff"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The version compare list.",
   "error": "Could not load. Names which read failed and leaves the version compare untouched.",
   "emptyFirstRun": "No version compare yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the version compare are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "diffSeatMapVersions",
    "contract": "seating",
    "purpose": "Compare two versions of a layout",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-977",
   "workshopBoard": "wireframes/WS142 Seat Management Venue Mapping Reference v1.0 Board 3.dc.html#bo-977"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 15. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Layout drafted 29 September (VM close-out)** from pack Seat_Management_Venue_Mapping_Reference v1.0.pdf p.15; contract seating.yaml GET /seat-maps/{seatMapId}/diff. Pack labels with no schema field yet (shown as plain labels): Moved / changed rows, seats and routes, Pricing / hold / product / revenue impact by category, Per-change actor, timestamp, request, reason, approval, Impacted performances, Overlay comparison geometry.",
  "entryState": {
   "params": [
    {
     "name": "seatMapId",
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
  "id": "BO-978",
  "name": "Multi-Performance Assignment",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "3",
   "number": "06",
   "page": 15
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/multi-performance-assignment-bo-978",
   "component": "apps/venue-management-web/src/routes/access-venue/MultiPerformanceAssignment.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-973"
   ],
   "exitTo": [
    "BO-973"
   ],
   "transitions": [
    {
     "to": "BO-973",
     "trigger": "Back to Layout Command Center",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Assign approved layouts to one or many event performances. Provide calendar and grid views of event, date, venue, performance, assigned layout/version and status. Support bulk assignment, date range, recurrence, exception dates and different layouts across performances. Prevent assignment when a performance has incompatible sales, capacity, access or already-issued inventory. Preserve version lineage and require impact analysis for every change affecting capacity, products, sold seats, holds, access routes or pricing. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 15"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 15"
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
       "impliedBy": "listSeatMaps",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "publishSeatMap",
       "label": "Publish seat map",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "publishSeatMap"
      },
      {
       "kind": "publishGate",
       "label": "What publishing changes",
       "notes": "**Replaces the map every channel sells from.** Seats already sold keep their labels; seats that no longer exist in the new map are listed before this proceeds.",
       "provenance": "authored — required by check-screens, 19 September 2026"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The multi-performance list.",
   "error": "Could not load. Names which read failed and leaves the multi-performance untouched.",
   "emptyFirstRun": "No multi-performance yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the multi-performance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listSeatMaps",
    "contract": "seating",
    "purpose": "Maps available",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "publishSeatMap",
    "contract": "seating",
    "purpose": "Assign to performances",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-978",
   "workshopBoard": "wireframes/WS142 Seat Management Venue Mapping Reference v1.0 Board 3.dc.html#bo-978"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 15. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "seatMapId",
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
  "id": "BO-979",
  "name": "Temporary Seat Blocking",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "3",
   "number": "07",
   "page": 15
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/temporary-seat-blocking-bo-979",
   "component": "apps/venue-management-web/src/routes/access-venue/TemporarySeatBlocking.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-973"
   ],
   "exitTo": [
    "BO-973"
   ],
   "transitions": [
    {
     "to": "BO-973",
     "trigger": "Back to Layout Command Center",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Temporarily remove seats from sale for production or operational reasons. Select section, row, seat or polygon on the map and define block type, reason, owner and effective period. Preview affected available, held, reserved and sold inventory with required remediation or approval. Support camera, equipment, safety, maintenance, sightline, house and event-production block categories. Preserve version lineage and require impact analysis for every change affecting capacity, products, sold seats, holds, access routes or pricing. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history. Configuration Scope of Work | Version 1.0 15",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 15"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 15"
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
       "impliedBy": "createSeatHoldPool"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The temporary seat blocking list.",
   "error": "Could not load. Names which read failed and leaves the temporary seat blocking untouched.",
   "emptyFirstRun": "No temporary seat blocking yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the temporary seat blocking are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createSeatHoldPool",
    "contract": "seating",
    "purpose": "Block seats temporarily",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listSeatHoldPools",
     "getSeatInventory",
     "getSeatAvailability"
    ]
   },
   {
    "operationId": "listSeatHoldPools",
    "contract": "seating",
    "purpose": "What is blocked",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-979",
   "workshopBoard": "wireframes/WS142 Seat Management Venue Mapping Reference v1.0 Board 3.dc.html#bo-979"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 15. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-980",
  "name": "Scheduled Seat Release",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "3",
   "number": "08",
   "page": 16
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/scheduled-seat-release-bo-980",
   "component": "apps/venue-management-web/src/routes/access-venue/ScheduledSeatRelease.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-973"
   ],
   "exitTo": [
    "BO-973"
   ],
   "transitions": [
    {
     "to": "BO-973",
     "trigger": "Back to Layout Command Center",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Return temporarily blocked inventory to sale at a controlled time. Create release schedules by event, performance, hold/block type, seat set, time before event and condition. Preview release quantity, new capacity, pricing/category mapping and affected sales channels. Support reschedule, cancel, manual run, partial failure recovery and stakeholder notifications. Preserve version lineage and require impact analysis for every change affecting capacity, products, sold seats, holds, access routes or pricing. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 16"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 16"
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
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listSeatHoldTypes",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
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
   "loading": "The scheduled seat release list.",
   "error": "Could not load. Names which read failed and leaves the scheduled seat release untouched.",
   "emptyFirstRun": "No scheduled seat release yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the scheduled seat release are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "releaseSeatHoldPool",
    "contract": "seating",
    "purpose": "Scheduled release",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listSeatHoldPools",
     "getSeatInventory",
     "getSeatAvailability"
    ]
   },
   {
    "operationId": "listSeatHoldTypes",
    "contract": "seating",
    "purpose": "The release rules",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-980",
   "workshopBoard": "wireframes/WS142 Seat Management Venue Mapping Reference v1.0 Board 3.dc.html#bo-980"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 16. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-981",
  "name": "Conflict & Impact Simulation",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "3",
   "number": "09",
   "page": 16
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/conflict-impact-simulation-bo-981",
   "component": "apps/venue-management-web/src/routes/access-venue/ConflictImpactSimulation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-973"
   ],
   "exitTo": [
    "BO-973"
   ],
   "transitions": [
    {
     "to": "BO-973",
     "trigger": "Back to Layout Command Center",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Identify operational and commercial risk before a layout change becomes effective. Simulate seat removal, addition, movement, category change, stage change, route change and block/release actions. Calculate affected sold seats, holds, reservations, carts, products, access gates, capacity and forecast revenue. Provide resolution options such as reseating, alternative inventory, delayed release, refund workflow or rejected change. Preserve version lineage and require impact analysis for every change affecting capacity, products, sold seats, holds, access routes or pricing. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 16"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 16"
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
       "impliedBy": "simulatePolicyConflictImpact",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "simulatePolicyConflictImpact"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The conflict impact simulation list.",
   "error": "Could not load. Names which read failed and leaves the conflict impact simulation untouched.",
   "emptyFirstRun": "No conflict impact simulation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the conflict impact simulation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "simulatePolicyConflictImpact",
    "contract": "access",
    "purpose": "Policy Simulation, Conflict & Impact Analysis",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-981",
   "workshopBoard": "wireframes/WS142 Seat Management Venue Mapping Reference v1.0 Board 3.dc.html#bo-981"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 16. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-982",
  "name": "Approval, Publish & Rollback",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "3",
   "number": "10",
   "page": 16
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/approval-publish-rollback-bo-982",
   "component": "apps/venue-management-web/src/routes/access-venue/ApprovalPublishRollback.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-973"
   ],
   "exitTo": [
    "BO-973"
   ],
   "transitions": [
    {
     "to": "BO-973",
     "trigger": "Back to Layout Command Center",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Govern the complete release lifecycle for layout changes. Configure draft, review, operations, ticketing, finance and final approval stages by impact and venue policy. Schedule publication, notify dependent systems and verify synchronized version across channels. Maintain version history, failed-publication recovery, emergency unpublish and safe rollback with impact confirmation. Preserve version lineage and require impact analysis for every change affecting capacity, products, sold seats, holds, access routes or pricing. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history. Configuration Scope of Work | Version 1.0 16 Board 4 - Seat Inventory, Status & Audit Figure 4. High-definition configuration board with all 10 screens. Visual reference: information architecture and configuration coverage; detailed production behavior is defined in the following scope. Configuration Scope of Work | Version 1.0 17",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 16"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 16"
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
       "impliedBy": "validateSeatMap",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "validateSeatMap"
      },
      {
       "kind": "publishGate",
       "label": "What publishing changes",
       "notes": "**Replaces the map every channel sells from.** Seats already sold keep their labels; seats that no longer exist in the new map are listed before this proceeds.",
       "provenance": "authored — required by check-screens, 19 September 2026"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The approval publish rollback list.",
   "error": "Could not load. Names which read failed and leaves the approval publish rollback untouched.",
   "emptyFirstRun": "No approval publish rollback yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the approval publish rollback are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "validateSeatMap",
    "contract": "seating",
    "purpose": "Check before publishing",
    "trigger": "onAction"
   },
   {
    "operationId": "publishSeatMap",
    "contract": "seating",
    "purpose": "Publish or roll back",
    "trigger": "onAction",
    "invalidates": [
     "listSeatMaps",
     "getSeatMap"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-982",
   "workshopBoard": "wireframes/WS142 Seat Management Venue Mapping Reference v1.0 Board 3.dc.html#bo-982"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 16. 0 of 0 labels bound to a contract property; 0 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "seatMapId",
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
 "cloneSeatMap": {
  "method": "POST",
  "path": "/seat-maps/{seatMapId}/clone",
  "contract": "seating",
  "summary": "Clone a map, optionally into another venue",
  "permission": "CAPACITY_CONFIGURE",
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
  "responds": "SeatMap"
 },
 "copySeatMapSection": {
  "method": "POST",
  "path": "/seat-maps/{seatMapId}/sections/copy",
  "contract": "seating",
  "summary": "Copy one section into another map",
  "permission": "CAPACITY_CONFIGURE",
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
  "responds": "SeatMap"
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
 "createSeatMapTemplate": {
  "method": "POST",
  "path": "/seat-map-templates",
  "contract": "seating",
  "summary": "Save a map as a reusable template",
  "permission": "CAPACITY_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "SeatMapTemplate"
 },
 "diffSeatMapVersions": {
  "method": "GET",
  "path": "/seat-maps/{seatMapId}/diff",
  "contract": "seating",
  "summary": "Compare two versions of a layout",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "fromVersion",
    "in": "query",
    "required": true
   },
   {
    "name": "toVersion",
    "in": "query",
    "required": true
   }
  ],
  "requestBody": null,
  "responds": "SeatMapDiff"
 },
 "getSeatMap": {
  "method": "GET",
  "path": "/seat-maps/{seatMapId}",
  "contract": "seating",
  "summary": "Read a seat map with its structure",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "SeatMap"
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
 "listSeatMapTemplates": {
  "method": "GET",
  "path": "/seat-map-templates",
  "contract": "seating",
  "summary": "List reusable layout templates",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [],
  "requestBody": null,
  "responds": "SeatMapTemplate"
 },
 "listSeatMaps": {
  "method": "GET",
  "path": "/seat-maps",
  "contract": "seating",
  "summary": "List seat maps",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "venueId",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": null,
    "in": null,
    "required": null
   },
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Page"
 },
 "publishSeatMap": {
  "method": "POST",
  "path": "/seat-maps/{seatMapId}/publish",
  "contract": "seating",
  "summary": "Validate and publish a seat map",
  "permission": "CAPACITY_CONFIGURE",
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
  "responds": "SeatMap"
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
 "simulatePolicyConflictImpact": {
  "method": "PUT",
  "path": "/policy-conflict-impact",
  "contract": "access",
  "summary": "Policy Simulation, Conflict & Impact Analysis",
  "permission": "ACCESS_POINT_CONFIGURE",
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
  "requestBody": "PolicySimulationConflictImpactAnalysisInput",
  "responds": "PolicySimulationConflictImpactAnalysisView"
 },
 "validateSeatMap": {
  "method": "POST",
  "path": "/seat-maps/{seatMapId}/validate",
  "contract": "seating",
  "summary": "Run validation without publishing",
  "permission": "PRODUCT_VIEW",
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
  "responds": "ValidationReport"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "Page": {
  "type": "object",
  "required": [
   "items",
   "hasMore"
  ],
  "properties": {
   "items": {
    "type": "array",
    "items": {}
   },
   "nextCursor": {
    "type": "string"
   },
   "hasMore": {
    "type": "boolean"
   }
  }
 },
 "Point": {
  "type": "object",
  "required": [
   "x",
   "y"
  ],
  "properties": {
   "x": {
    "type": "number"
   },
   "y": {
    "type": "number"
   }
  }
 },
 "PolicySimulationConflictImpactAnalysisInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Policy Simulation, Conflict & Impact Analysis submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "policyId": {
    "type": "string"
   },
   "policyVersion": {
    "type": "string"
   },
   "scenarioTime": {
    "type": "string",
    "format": "date-time",
    "description": "Simulated moment of the scan"
   },
   "credentialId": {
    "type": "string",
    "description": "Optional credential to simulate"
   },
   "runSavedScenarios": {
    "type": "boolean",
    "description": "Regression: run saved scenarios against this policy version"
   },
   "scenarioCount": {
    "type": "integer"
   },
   "passedCount": {
    "type": "integer"
   },
   "changedOutcomeCount": {
    "type": "integer"
   },
   "affectedCredentials": {
    "type": "integer"
   }
  },
  "required": [
   "policyId"
  ]
 },
 "PolicySimulationConflictImpactAnalysisView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Policy Simulation, Conflict & Impact Analysis displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "policyId": {
    "type": "string"
   },
   "occupancy": {
    "type": "integer",
    "description": "Occupancy (the pack shows 82%)"
   },
   "policiesInvolved": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "policies involved"
   },
   "hierarchy": {
    "type": "string",
    "description": "hierarchy"
   },
   "priority": {
    "type": "integer",
    "description": "priority"
   },
   "resultingDecision": {
    "type": "string",
    "enum": [
     "allow",
     "deny",
     "review",
     "requireId",
     "requireBiometric",
     "requireCompanion",
     "requireSupervisor"
    ],
    "description": "resulting decision"
   },
   "affectedProducts": {
    "type": "integer",
    "description": "affected products"
   },
   "affectedVenues": {
    "type": "integer",
    "description": "affected venues"
   },
   "estimatedGuestsImpacted": {
    "type": "integer",
    "description": "estimated guests impacted"
   },
   "policyVersion": {
    "type": "string"
   },
   "scenarioTime": {
    "type": "string",
    "format": "date-time",
    "description": "Simulated moment of the scan"
   },
   "credentialId": {
    "type": "string",
    "description": "Optional credential to simulate"
   },
   "runSavedScenarios": {
    "type": "boolean",
    "description": "Regression: run saved scenarios against this policy version"
   },
   "scenarioCount": {
    "type": "integer"
   },
   "passedCount": {
    "type": "integer"
   },
   "changedOutcomeCount": {
    "type": "integer"
   },
   "affectedCredentials": {
    "type": "integer"
   }
  },
  "required": [
   "policyId"
  ]
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
 },
 "SeatMap": {
  "x-ticvai-persistence": "seating.seat_map",
  "allOf": [
   {
    "$ref": "#/components/schemas/SeatMapSummary"
   },
   {
    "type": "object",
    "required": [
     "sections"
    ],
    "properties": {
     "description": {
      "type": "string",
      "nullable": true
     },
     "viewBox": {
      "type": "object",
      "description": "Coordinate space for rendering. Absent when there is no geometry.",
      "nullable": true,
      "properties": {
       "width": {
        "type": "number"
       },
       "height": {
        "type": "number"
       }
      }
     },
     "stagePosition": {
      "$ref": "#/components/schemas/Point"
     },
     "sections": {
      "type": "array",
      "items": {
       "$ref": "#/components/schemas/Section"
      }
     },
     "isActive": {
      "type": "boolean"
     }
    }
   }
  ]
 },
 "SeatMapDiff": {
  "type": "object",
  "description": "**A diff a person can read, not 396 changed cells.** `Seating_Manifest_1.xlsx` is 396 rows and a comparison that lists every one is noise — *row H moved back two* is what a venue manager needs, and it only exists if the diff understands sections and rows rather than treating a map as a grid of values.\n\n**Counts first, then the shape, then the detail.** A reconfiguration is judged on whether the house got bigger or smaller before anything else.",
  "required": [
   "fromVersion",
   "toVersion",
   "seatCountBefore",
   "seatCountAfter"
  ],
  "properties": {
   "fromVersion": {
    "type": "integer"
   },
   "toVersion": {
    "type": "integer"
   },
   "seatCountBefore": {
    "type": "integer"
   },
   "seatCountAfter": {
    "type": "integer"
   },
   "sectionsAdded": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "sectionsRemoved": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "sectionsChanged": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "section": {
       "type": "string"
      },
      "seatsBefore": {
       "type": "integer"
      },
      "seatsAfter": {
       "type": "integer"
      },
      "summary": {
       "type": "string",
       "description": "**One sentence a person reads** — *row H moved back two, two seats removed at the aisle.*"
      }
     }
    }
   },
   "accessibleSeatsBefore": {
    "type": "integer",
    "nullable": true
   },
   "accessibleSeatsAfter": {
    "type": "integer",
    "nullable": true,
    "description": "**Called out separately because it is a compliance number, not a capacity one.** A reconfiguration that quietly loses two wheelchair spaces is the change nobody notices in a seat count."
   }
  }
 },
 "SeatMapSummary": {
  "x-ticvai-persistence": "seating.seat_map",
  "type": "object",
  "required": [
   "id",
   "name",
   "venueId",
   "status",
   "seatCount"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "status": {
    "$ref": "#/components/schemas/SeatMapStatus"
   },
   "seatCount": {
    "type": "integer"
   },
   "sectionCount": {
    "type": "integer"
   },
   "hasGeometry": {
    "type": "boolean",
    "description": "False when only a manifest has been imported. Such a map can be sold from a list but not rendered.\n"
   },
   "publishedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "SeatMapTemplate": {
  "x-ticvai-persistence": "seating.seat_map_template",
  "type": "object",
  "required": [
   "id",
   "name",
   "seatCount",
   "sectionCount"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string"
   },
   "description": {
    "type": "string",
    "nullable": true
   },
   "seatCount": {
    "type": "integer"
   },
   "sectionCount": {
    "type": "integer"
   },
   "hasGeometry": {
    "type": "boolean"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "Section": {
  "x-ticvai-persistence": "seating.section",
  "type": "object",
  "required": [
   "code",
   "name",
   "rowCount",
   "seatCount"
  ],
  "properties": {
   "code": {
    "type": "string"
   },
   "name": {
    "type": "string"
   },
   "rowCount": {
    "type": "integer"
   },
   "seatCount": {
    "type": "integer"
   },
   "boundary": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/Point"
    },
    "description": "Polygon for rendering. Absent without geometry."
   },
   "viewAssetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "x-ticvai-references": "assets.MediaAsset",
    "description": "**The view of the stage from this section, as a photo**, uploaded through `assets` like any other media (decided 29 September, rev 3 23SEP-14). Optional: where it is null the client renders the view from the imported geometry (the section `boundary`, the map's `stagePosition` and the seat positions), so a closer section shows a larger stage and fewer rows ahead. Set with `updateSeatMap` `sectionViews`, which is allowed on a published map because a photo does not change the map's shape.\n"
   },
   "rows": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "label",
      "seatCount"
     ],
     "properties": {
      "label": {
       "type": "string"
      },
      "seatCount": {
       "type": "integer"
      },
      "numberingDirection": {
       "type": "string",
       "enum": [
        "leftToRight",
        "rightToLeft"
       ],
       "description": "Which end row numbering starts from. Not recoverable from a manifest and must be stated — it determines whether a guest finds their seat.\n"
      }
     }
    }
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"
   }
  }
 },
 "ValidationFinding": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "kind",
   "severity",
   "message"
  ],
  "properties": {
   "kind": {
    "$ref": "#/components/schemas/ValidationFindingKind"
   },
   "severity": {
    "$ref": "#/components/schemas/ValidationSeverity"
   },
   "message": {
    "type": "string"
   },
   "sectionCode": {
    "type": "string",
    "nullable": true
   },
   "rowLabel": {
    "type": "string",
    "nullable": true
   },
   "seatNumbers": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "affectedCount": {
    "type": "integer"
   }
  }
 },
 "ValidationReport": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "seatMapId",
   "passed",
   "errorCount",
   "warningCount",
   "findings"
  ],
  "properties": {
   "seatMapId": {
    "type": "string",
    "format": "uuid"
   },
   "passed": {
    "type": "boolean",
    "description": "False when any finding has severity `error`."
   },
   "errorCount": {
    "type": "integer"
   },
   "warningCount": {
    "type": "integer"
   },
   "findings": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/ValidationFinding"
    }
   }
  }
 }
}
```
