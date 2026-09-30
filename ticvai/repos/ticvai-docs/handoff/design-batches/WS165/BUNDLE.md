# WS165 — Seat Management Venue Mapping Reference v1.0 board 1

**10 screens · 14 operations · 22 schemas · 3 permissions**

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
  `ASSET_LIBRARY_MANAGE, CAPACITY_CONFIGURE, PRODUCT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-953` | Seat Map Command Center | listDetail | 2 | 0 | — |
| `BO-954` | Venue Canvas | listDetail | 3 | 0 | — |
| `BO-955` | Sections & Zones | listDetail | 5 | 0 | — |
| `BO-956` | Rows & Seats | listDetail | 2 | 0 | — |
| `BO-957` | Standing Zones | listDetail | 1 | 0 | — |
| `BO-958` | Suites & Boxes | listDetail | 1 | 0 | — |
| `BO-959` | Stage & Focal Point | listDetail | 2 | 0 | — |
| `BO-960` | Entrances, Exits & Aisles | listDetail | 1 | 0 | — |
| `BO-961` | Amenities & Obstructions | listDetail | 1 | 0 | — |
| `BO-962` | Templates, Validation & Publish | listDetail | 4 | 0 | — |

## Thin screens in this batch

**BO-953, BO-954, BO-956, BO-957, BO-958, BO-959, BO-960, BO-961 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-953",
  "name": "Seat Map Command Center",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "1",
   "number": "01",
   "page": 5
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/seat-map-command-center-bo-953",
   "component": "apps/venue-management-web/src/routes/access-venue/SeatMapCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-954",
    "BO-955",
    "BO-956",
    "BO-957",
    "BO-958",
    "BO-959",
    "BO-960",
    "BO-961",
    "BO-962"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "BO-954",
     "trigger": "Venue Canvas",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "BO-955",
     "trigger": "Sections & Zones",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "BO-956",
     "trigger": "Rows & Seats",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "BO-957",
     "trigger": "Standing Zones",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "BO-958",
     "trigger": "Suites & Boxes",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "BO-959",
     "trigger": "Stage & Focal Point",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "BO-960",
     "trigger": "Entrances, Exits & Aisles",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "BO-961",
     "trigger": "Amenities & Obstructions",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "BO-962",
     "trigger": "Templates, Validation & Publish",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide a role-specific overview of every venue map and its operational readiness. Show total venues, active maps, seats, sections, capacity, drafts, approvals, validation errors and upcoming layout changes. Filter and compare by tenant, brand, region, venue, map type, status, owner and last-published date. Open recent maps, validation alerts, approval tasks and impacted performances directly from the dashboard. Version geometry and property changes, enforce venue-scoped permissions, validate affected capacity and preserve before/after audit evidence. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 5"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 5"
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
   "loading": "The seat map list.",
   "error": "Could not load. Names which read failed and leaves the seat map untouched.",
   "emptyFirstRun": "No seat map yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the seat map are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listSeatMaps",
    "contract": "seating",
    "purpose": "List seat maps",
    "trigger": "onLoad"
   },
   {
    "operationId": "listSeatMapTemplates",
    "contract": "seating",
    "purpose": "List reusable layout templates",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-953",
   "workshopBoard": "wireframes/WS140 Seat Management Venue Mapping Reference v1.0 Board 1.dc.html#bo-953"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 5. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-954",
  "name": "Venue Canvas",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "1",
   "number": "02",
   "page": 5
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/venue-canvas-bo-954",
   "component": "apps/venue-management-web/src/routes/access-venue/VenueCanvas.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-953"
   ],
   "exitTo": [
    "BO-953"
   ],
   "transitions": [
    {
     "to": "BO-953",
     "trigger": "Back to Seat Map Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide the primary drag-and-drop workspace for constructing a venue map. Offer components for section, row, seat, standing zone, suite, stage, entrance, exit, aisle, facility, obstruction and label. Support zoom, pan, snap-to-grid, rulers, coordinates, layers, alignment, grouping, undo/redo and background- reference controls. Configure venue name, dimensions, unit, scale, orientation, origin, focal point and canvas boundaries in a properties inspector. Version geometry and property changes, enforce venue-scoped permissions, validate affected capacity and preserve before/after audit evidence. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 5"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 5"
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
       "impliedBy": "createSeatMap",
       "label": "Create seat map",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createSeatMap"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The venue canvas list.",
   "error": "Could not load. Names which read failed and leaves the venue canvas untouched.",
   "emptyFirstRun": "No venue canvas yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the venue canvas are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getSeatMap",
    "contract": "seating",
    "purpose": "The map being drawn",
    "trigger": "onAction"
   },
   {
    "operationId": "createSeatMap",
    "contract": "seating",
    "purpose": "Start a new map",
    "trigger": "onAction",
    "invalidates": [
     "listSeatMaps"
    ]
   },
   {
    "operationId": "updateSeatMap",
    "contract": "seating",
    "purpose": "Save the canvas",
    "trigger": "onAction",
    "invalidates": [
     "getSeatMap",
     "listSeatMaps"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-954",
   "workshopBoard": "wireframes/WS140 Seat Management Venue Mapping Reference v1.0 Board 1.dc.html#bo-954"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 5. 0 of 0 labels bound to a contract property; 0 of 11 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-955",
  "name": "Sections & Zones",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "1",
   "number": "03",
   "page": 5
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/sections-zones-bo-955",
   "component": "apps/venue-management-web/src/routes/access-venue/SectionsZones.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-953"
   ],
   "exitTo": [
    "BO-953"
   ],
   "transitions": [
    {
     "to": "BO-953",
     "trigger": "Back to Seat Map Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Define the commercial and operational hierarchy of the venue. Create, draw and edit section or zone polygons with name, code, level, capacity, color, category and parent hierarchy. Support curved, rectangular, freeform and imported boundaries with duplication, alignment and bulk-property updates. Configuration Scope of Work | Version 1.0 5 Map sections to pricing, access gates, sales channels, accessibility attributes and reporting dimensions. Version geometry and property changes, enforce venue-scoped permissions, validate affected capacity and preserve before/after audit evidence. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 5"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 5"
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
       "impliedBy": "setMapZones",
       "label": "Save map zones",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setMapZones"
      },
      {
       "kind": "fileUpload",
       "label": "View from this section",
       "operation": "createUpload",
       "notes": "**An optional photo per section** (decided 29 September, rev 3 23SEP-14): the view a guest sees on the seat map when they pick the section. Uploaded to the asset library (`createUpload`, then `completeUpload`) and saved with `updateSeatMap` `sectionViews`, which is allowed on a published map. With no photo, the guest app renders the view from the imported geometry (a closer section shows a larger stage and fewer rows ahead). Removing the photo sends a null `viewAssetId`.",
       "provenance": "contract assets.yaml POST /media/uploads"
      },
      {
       "kind": "secondaryButton",
       "label": "Save section views",
       "operation": "updateSeatMap",
       "provenance": "contract seating.yaml PATCH /seat-maps/{seatMapId}"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The sections zones list.",
   "error": "Could not load. Names which read failed and leaves the sections zones untouched.",
   "emptyFirstRun": "No sections zones yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the sections zones are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getSeatMap",
    "contract": "seating",
    "purpose": "The map being sectioned",
    "trigger": "onAction"
   },
   {
    "operationId": "setMapZones",
    "contract": "seating",
    "purpose": "Section type, set at the section level",
    "trigger": "onAction",
    "invalidates": [
     "getSeatMap"
    ]
   },
   {
    "operationId": "updateSeatMap",
    "contract": "seating",
    "purpose": "Set or clear the view photo of each section (rev 3 23SEP-14)",
    "trigger": "onAction",
    "invalidates": [
     "getSeatMap"
    ]
   },
   {
    "operationId": "createUpload",
    "contract": "assets",
    "purpose": "Upload a section's view photo",
    "trigger": "onAction"
   },
   {
    "operationId": "completeUpload",
    "contract": "assets",
    "purpose": "Finish the upload so the photo can be linked",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-955",
   "workshopBoard": "wireframes/WS140 Seat Management Venue Mapping Reference v1.0 Board 1.dc.html#bo-955"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 5. 0 of 0 labels bound to a contract property; 0 of 11 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "seatMapId",
     "from": "navigation"
    },
    {
     "name": "uploadId",
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
  "id": "BO-956",
  "name": "Rows & Seats",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "1",
   "number": "04",
   "page": 6
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/rows-seats-bo-956",
   "component": "apps/venue-management-web/src/routes/access-venue/RowsSeats.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-953"
   ],
   "exitTo": [
    "BO-953"
   ],
   "transitions": [
    {
     "to": "BO-953",
     "trigger": "Back to Seat Map Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Build and maintain numbered rows and individual seat positions at scale. Generate straight, curved, radial or custom rows using seat count, spacing, radius, angle, direction and offset parameters. Configure seat number, label, type, category, coordinate, status default, accessibility, view quality and amenity attributes. Support bulk add, renumber, reverse, insert, remove, copy, align and spacing changes with collision and duplicate detection. Version geometry and property changes, enforce venue-scoped permissions, validate affected capacity and preserve before/after audit evidence. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 6"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 6"
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
       "impliedBy": "listSeats",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "updateSeats",
       "label": "Save seats",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "updateSeats"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The rows seats list.",
   "error": "Could not load. Names which read failed and leaves the rows seats untouched.",
   "emptyFirstRun": "No rows seats yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the rows seats are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listSeats",
    "contract": "seating",
    "purpose": "The rows and seats as drawn",
    "trigger": "onAction"
   },
   {
    "operationId": "updateSeats",
    "contract": "seating",
    "purpose": "Renumber, move or relabel",
    "trigger": "onAction",
    "invalidates": [
     "listSeats"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-956",
   "workshopBoard": "wireframes/WS140 Seat Management Venue Mapping Reference v1.0 Board 1.dc.html#bo-956"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 6. 0 of 0 labels bound to a contract property; 0 of 11 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-957",
  "name": "Standing Zones",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "1",
   "number": "05",
   "page": 6
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/standing-zones-bo-957",
   "component": "apps/venue-management-web/src/routes/access-venue/StandingZones.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-953"
   ],
   "exitTo": [
    "BO-953"
   ],
   "transitions": [
    {
     "to": "BO-953",
     "trigger": "Back to Seat Map Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure non-assigned areas with controlled capacity and density. Draw standing, general-admission, pit, dance-floor or hospitality zones and assign type, capacity, density and color. Calculate capacity from area and approved density while allowing an authorized lower operating limit. Associate entrances, exits, age rules, access products, pricing bands and event-specific restrictions. Version geometry and property changes, enforce venue-scoped permissions, validate affected capacity and preserve before/after audit evidence. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 6"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 6"
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
       "impliedBy": "setMapZones",
       "label": "Save map zones",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setMapZones"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The standing zones list.",
   "error": "Could not load. Names which read failed and leaves the standing zones untouched.",
   "emptyFirstRun": "No standing zones yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the standing zones are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setMapZones",
    "contract": "seating",
    "purpose": "Standing areas",
    "trigger": "onAction",
    "invalidates": [
     "getSeatMap"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-957",
   "workshopBoard": "wireframes/WS140 Seat Management Venue Mapping Reference v1.0 Board 1.dc.html#bo-957"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 6. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-958",
  "name": "Suites & Boxes",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "1",
   "number": "06",
   "page": 6
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/suites-boxes-bo-958",
   "component": "apps/venue-management-web/src/routes/access-venue/SuitesBoxes.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-953"
   ],
   "exitTo": [
    "BO-953"
   ],
   "transitions": [
    {
     "to": "BO-953",
     "trigger": "Back to Seat Map Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Model suites, boxes and hospitality spaces as sellable seating inventory. Create suites and boxes with code, capacity, internal seat layout, standing allowance, amenities and accessibility attributes. Support whole-suite, per-seat, shared and configurable sales models with linked products and price categories. Maintain owner, contract, allocation, entrance, service area and operational-status references without duplicating CRM or contract data. Version geometry and property changes, enforce venue-scoped permissions, validate affected capacity and preserve before/after audit evidence. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history. Configuration Scope of Work | Version 1.0 6",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 6"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 6"
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
       "impliedBy": "setMapZones",
       "label": "Save map zones",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setMapZones"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The suites boxes list.",
   "error": "Could not load. Names which read failed and leaves the suites boxes untouched.",
   "emptyFirstRun": "No suites boxes yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the suites boxes are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setMapZones",
    "contract": "seating",
    "purpose": "Suites and boxes",
    "trigger": "onAction",
    "invalidates": [
     "getSeatMap"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-958",
   "workshopBoard": "wireframes/WS140 Seat Management Venue Mapping Reference v1.0 Board 1.dc.html#bo-958"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 6. 0 of 0 labels bound to a contract property; 0 of 11 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-959",
  "name": "Stage & Focal Point",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "1",
   "number": "07",
   "page": 7
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/stage-focal-point-bo-959",
   "component": "apps/venue-management-web/src/routes/access-venue/StageFocalPoint.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-953"
   ],
   "exitTo": [
    "BO-953"
   ],
   "transitions": [
    {
     "to": "BO-953",
     "trigger": "Back to Seat Map Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Define the viewing focal point and production footprint used by seating logic. Add stage, field, screen, court, track or custom focal areas with position, dimensions, rotation, height and event- specific variant. Configure one or multiple focal points for distance, orientation, best-seat and closest-to-stage calculations. Preview sightline coverage, obstructed areas and seats affected by production structures before publication. Version geometry and property changes, enforce venue-scoped permissions, validate affected capacity and preserve before/after audit evidence. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 7"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 7"
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
       "impliedBy": "setMapZones",
       "label": "Save map zones",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setMapZones"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The stage focal point list.",
   "error": "Could not load. Names which read failed and leaves the stage focal point untouched.",
   "emptyFirstRun": "No stage focal point yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the stage focal point are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setMapZones",
    "contract": "seating",
    "purpose": "Stage and focal point",
    "trigger": "onAction",
    "invalidates": [
     "getSeatMap"
    ]
   },
   {
    "operationId": "proposeSeatMapChanges",
    "contract": "ai",
    "purpose": "Propose categories, numbering, a stage variant or consistency findings for this map",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-959",
   "workshopBoard": "wireframes/WS140 Seat Management Venue Mapping Reference v1.0 Board 1.dc.html#bo-959"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 7. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-960",
  "name": "Entrances, Exits & Aisles",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "1",
   "number": "08",
   "page": 7
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/entrances-exits-aisles-bo-960",
   "component": "apps/venue-management-web/src/routes/access-venue/EntrancesExitsAisles.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-953"
   ],
   "exitTo": [
    "BO-953"
   ],
   "transitions": [
    {
     "to": "BO-953",
     "trigger": "Back to Seat Map Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Map circulation elements used by access, accessibility and safety operations. Create entrances, exits, gates, portals, vomitories, concourses, stairways and aisles with unique identifiers and attributes. Define width, direction, level, connected zones, access-control device, accessible status and emergency designation. Validate disconnected zones, blocked paths, minimum aisle width and route continuity against configured venue rules. Version geometry and property changes, enforce venue-scoped permissions, validate affected capacity and preserve before/after audit evidence. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 7"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 7"
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
       "impliedBy": "setMapZones",
       "label": "Save map zones",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setMapZones"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The entrances exits aisles list.",
   "error": "Could not load. Names which read failed and leaves the entrances exits aisles untouched.",
   "emptyFirstRun": "No entrances exits aisles yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the entrances exits aisles are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setMapZones",
    "contract": "seating",
    "purpose": "Entrances, exits and aisles",
    "trigger": "onAction",
    "invalidates": [
     "getSeatMap"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-960",
   "workshopBoard": "wireframes/WS140 Seat Management Venue Mapping Reference v1.0 Board 1.dc.html#bo-960"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 7. 0 of 0 labels bound to a contract property; 0 of 10 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-961",
  "name": "Amenities & Obstructions",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "1",
   "number": "09",
   "page": 7
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/amenities-obstructions-bo-961",
   "component": "apps/venue-management-web/src/routes/access-venue/AmenitiesObstructions.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-953"
   ],
   "exitTo": [
    "BO-953"
   ],
   "transitions": [
    {
     "to": "BO-953",
     "trigger": "Back to Seat Map Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Add guest facilities, service points and view-affecting objects to the venue map. Place restrooms, concessions, bars, first aid, merchandise, lifts, escalators, information, prayer and accessibility facilities. Map pillars, cameras, speaker arrays, lighting trusses, barriers and production structures with obstruction type and dimensions. Expose approved amenity and view attributes to filters, seat previews, operations and accessibility routing. Version geometry and property changes, enforce venue-scoped permissions, validate affected capacity and preserve before/after audit evidence. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 7"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 7"
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
       "impliedBy": "setMapZones",
       "label": "Save map zones",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setMapZones"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The amenities obstructions list.",
   "error": "Could not load. Names which read failed and leaves the amenities obstructions untouched.",
   "emptyFirstRun": "No amenities obstructions yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the amenities obstructions are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setMapZones",
    "contract": "seating",
    "purpose": "Amenities and obstructions",
    "trigger": "onAction",
    "invalidates": [
     "getSeatMap"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-961",
   "workshopBoard": "wireframes/WS140 Seat Management Venue Mapping Reference v1.0 Board 1.dc.html#bo-961"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 7. 0 of 0 labels bound to a contract property; 0 of 10 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-962",
  "name": "Templates, Validation & Publish",
  "module": "Access & Venue",
  "requiresModule": "seating",
  "wave": 3,
  "source": {
   "pack": "Seat_Management_Venue_Mapping_Reference v1.0.pdf",
   "board": "1",
   "number": "10",
   "page": 7
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/access-venue/templates-validation-publish-bo-962",
   "component": "apps/venue-management-web/src/routes/access-venue/TemplatesValidationPublish.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-953"
   ],
   "exitTo": [
    "BO-953"
   ],
   "transitions": [
    {
     "to": "BO-953",
     "trigger": "Back to Seat Map Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Govern reusable venue templates and release a map only when it is operationally complete. Create, classify, clone, archive and reuse venue templates while preserving lineage and ownership. Run checks for geometry, capacity, duplicate numbering, overlaps, missing routes, accessibility, sightlines and dependent products. Provide draft, review, approval, scheduled publication, preview, version comparison and rollback with impact confirmation. Configuration Scope of Work | Version 1.0 7 Version geometry and property changes, enforce venue-scoped permissions, validate affected capacity and preserve before/after audit evidence. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history. Configuration Scope of Work | Version 1.0 8 Board 2 - AI Seat Map Import & Designer Figure 2. High-definition configuration board with all 10 screens. Visual reference: information architecture and configuration coverage; detailed production behavior is defined in the following scope. Configuration Scope of Work | Version 1.0 9",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 7"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Seat_Management_Venue_Mapping_Reference v1.0.pdf, page 7"
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
   "loading": "The templates validation publish list.",
   "error": "Could not load. Names which read failed and leaves the templates validation publish untouched.",
   "emptyFirstRun": "No templates validation publish yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the templates validation publish are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listSeatMapTemplates",
    "contract": "seating",
    "purpose": "Templates to start from",
    "trigger": "onLoad"
   },
   {
    "operationId": "createSeatMapTemplate",
    "contract": "seating",
    "purpose": "Save this map as a template",
    "trigger": "onAction",
    "invalidates": [
     "listSeatMapTemplates"
    ]
   },
   {
    "operationId": "validateSeatMap",
    "contract": "seating",
    "purpose": "Check before publishing",
    "trigger": "onAction"
   },
   {
    "operationId": "publishSeatMap",
    "contract": "seating",
    "purpose": "Publish",
    "trigger": "onAction",
    "invalidates": [
     "listSeatMaps",
     "getSeatMap"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-962",
   "workshopBoard": "wireframes/WS140 Seat Management Venue Mapping Reference v1.0 Board 1.dc.html#bo-962"
  },
  "apisNote": "Regenerated 9 September 2026 from Seat_Management_Venue_Mapping_Reference v1.0.pdf page 7. 0 of 0 labels bound to a contract property; 0 of 27 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "completeUpload": {
  "method": "POST",
  "path": "/media/uploads/{uploadId}/complete",
  "contract": "assets",
  "summary": "Confirm an upload and create the asset",
  "permission": "ASSET_LIBRARY_MANAGE",
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
  "responds": "MediaAsset"
 },
 "createSeatMap": {
  "method": "POST",
  "path": "/seat-maps",
  "contract": "seating",
  "summary": "Create a seat map",
  "permission": "CAPACITY_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
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
  "requestBody": "CreateSeatMapRequest",
  "responds": "SeatMap"
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
 "createUpload": {
  "method": "POST",
  "path": "/media/uploads",
  "contract": "assets",
  "summary": "Request a signed upload URL",
  "permission": "ASSET_LIBRARY_MANAGE",
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
  "responds": "UploadTicket"
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
 "listSeats": {
  "method": "GET",
  "path": "/seat-maps/{seatMapId}/seats",
  "contract": "seating",
  "summary": "List seats in a map",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "sectionCode",
    "in": "query",
    "required": null
   },
   {
    "name": "rowLabel",
    "in": "query",
    "required": null
   },
   {
    "name": "categoryId",
    "in": "query",
    "required": null
   },
   {
    "name": "attribute",
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
 "proposeSeatMapChanges": {
  "method": "POST",
  "path": "/ai/seat-maps/{seatMapId}/proposals",
  "contract": "ai",
  "summary": "Propose changes to an existing seat map, as a plan a person approves",
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
  "responds": "AiSeatMapProposal"
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
 "setMapZones": {
  "method": "PUT",
  "path": "/seat-maps/{seatMapId}/zones",
  "contract": "seating",
  "summary": "Standing areas, suites, stages and obstructions",
  "permission": "CAPACITY_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
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
  "responds": "MapZone"
 },
 "updateSeatMap": {
  "method": "PATCH",
  "path": "/seat-maps/{seatMapId}",
  "contract": "seating",
  "summary": "Rename or amend a seat map",
  "permission": "CAPACITY_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
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
  "responds": "SeatMap"
 },
 "updateSeats": {
  "method": "PATCH",
  "path": "/seat-maps/{seatMapId}/seats",
  "contract": "seating",
  "summary": "Bulk-amend seats",
  "permission": "CAPACITY_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
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
  "requestBody": "BulkUpdateSeatsRequest",
  "responds": null
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
 "AiSeatMapProposal": {
  "type": "object",
  "x-ticvai-persistence": "none — the plan is ai.action_plan and ai.action_step, presented as one ai.proposed_action; the findings are the evidence of its decision record",
  "description": "What `proposeSeatMapChanges` proposed: findings with the seats they concern, and except for `consistency` the plan a person approves (1.4.23, 1.4.25, 1.4.26, 1.4.29).",
  "required": [
   "kind",
   "findings"
  ],
  "properties": {
   "kind": {
    "type": "string",
    "enum": [
     "categories",
     "numbering",
     "stageVariant",
     "consistency"
    ]
   },
   "seatMapId": {
    "type": "string",
    "format": "uuid"
   },
   "planId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The `ai.action_plan`, readable with `getActionPlan`. Null for `consistency`."
   },
   "proposedActionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The `ai.proposed_action` a person decides. Null for `consistency`."
   },
   "summary": {
    "type": "object",
    "additionalProperties": true,
    "description": "Counts: seats re-categorised or relabelled, seats blocked, capacity by category before and after."
   },
   "findings": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "code",
      "severity"
     ],
     "properties": {
      "code": {
       "type": "string",
       "description": "e.g. `accessibleSeatWithoutAccessiblePrice`, `restrictedViewInPremium`, `companionWithoutWheelchairSpace`, `sightLineLost`, `behindStage`, `numberingGap`, `duplicateLabel`, `categoryChange`, `labelChange`."
      },
      "severity": {
       "type": "string",
       "enum": [
        "blocking",
        "warning",
        "info"
       ]
      },
      "seatIds": {
       "type": "array",
       "items": {
        "type": "string",
        "format": "uuid"
       }
      },
      "sectionId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "current": {
       "type": "string",
       "nullable": true
      },
      "proposed": {
       "type": "string",
       "nullable": true
      },
      "reason": {
       "type": "string",
       "nullable": true
      }
     }
    }
   },
   "basis": {
    "$ref": "#/components/schemas/SuggestionBasis"
   },
   "decisionRecordId": {
    "type": "string",
    "format": "uuid"
   }
  }
 },
 "BulkUpdateSeatsRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "selection"
  ],
  "properties": {
   "selection": {
    "type": "object",
    "description": "Seats to amend. Combine filters; an empty selection is rejected.",
    "properties": {
     "seatIds": {
      "type": "array",
      "items": {
       "type": "string"
      }
     },
     "sectionCodes": {
      "type": "array",
      "items": {
       "type": "string"
      }
     },
     "rowLabels": {
      "type": "array",
      "items": {
       "type": "string"
      }
     }
    }
   },
   "categoryId": {
    "type": "string",
    "format": "uuid"
   },
   "attribute": {
    "$ref": "#/components/schemas/SeatAttribute"
   },
   "isActive": {
    "type": "boolean"
   }
  }
 },
 "CreateSeatMapRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "name",
   "venueId"
  ],
  "properties": {
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "description": {
    "type": "string",
    "maxLength": 1000
   },
   "templateId": {
    "type": "string",
    "format": "uuid",
    "description": "Create from a template rather than empty."
   }
  }
 },
 "LocalisedText": {
  "x-ticvai-persistence": "none — jsonb column",
  "type": "object",
  "additionalProperties": {
   "type": "string"
  }
 },
 "MapZone": {
  "type": "object",
  "x-ticvai-persistence": "seating.zone",
  "description": "BL-166. **`seating` is strong on everything that is a seat and the map itself was only seats.**\n**A standing area is a capacity without individual seats**, and modelling it as seats means inventing seat numbers nobody prints and a guest cannot find. A suite is the opposite — one sellable unit containing many seats, sold whole.\nNon-sellable zones matter too: **a stage, an entry and a sightline obstruction are not inventory and they change what the seats beside them are worth.**\n",
  "required": [
   "id",
   "seatMapId",
   "kind",
   "name"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "seatMapId": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "type": "string",
    "enum": [
     "standing",
     "suite",
     "box",
     "lounge",
     "accessiblePlatform",
     "stage",
     "entry",
     "exit",
     "concourse",
     "obstruction",
     "camera",
     "aisle"
    ]
   },
   "name": {
    "type": "string"
   },
   "capacity": {
    "type": "integer",
    "nullable": true,
    "description": "**For a standing zone this is the inventory** — sold as a count rather than as seats. Null for a stage or an obstruction, which sell nothing.\n"
   },
   "seatCategoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "containsSeatIds": {
    "type": "array",
    "description": "For a suite or box. **Sold whole, so the seats inside are held together** — selling one seat of a suite is not a thing a venue does.\n",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "obstructsZoneIds": {
    "type": "array",
    "description": "What this blocks the view of. **A pillar is not inventory and it decides what the seats behind it are worth**, which is the only reason to draw it.\n",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "geometry": {
    "type": "string",
    "nullable": true
   }
  }
 },
 "MediaAsset": {
  "x-ticvai-persistence": "assets.media_asset",
  "type": "object",
  "required": [
   "id",
   "kind",
   "status",
   "filename",
   "contentType",
   "sizeBytes",
   "referenceCount",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "$ref": "#/components/schemas/MediaKind"
   },
   "status": {
    "$ref": "#/components/schemas/MediaStatus"
   },
   "filename": {
    "type": "string"
   },
   "contentType": {
    "type": "string"
   },
   "sizeBytes": {
    "type": "integer"
   },
   "title": {
    "$ref": "#/components/schemas/LocalisedText"
   },
   "description": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "description": "Set by `updateMediaAsset` and matched by `searchMedia`'s `search`. It was accepted and searched on before it had anywhere to be stored.\n"
   },
   "altText": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "description": "Required before use in a guest-facing surface. WCAG 2.2 AA."
   },
   "width": {
    "type": "integer",
    "nullable": true
   },
   "height": {
    "type": "integer",
    "nullable": true
   },
   "durationSeconds": {
    "type": "number",
    "nullable": true
   },
   "customMetadata": {
    "type": "object",
    "nullable": true,
    "additionalProperties": true,
    "description": "BL-178. **`assets` is a strong contract and its metadata was fixed** — kind, title, alt text, dimensions, rights. A venue photographing four thousand products wants its own fields: shoot date, photographer, model release, season.\n**Free-form and searchable, not a schema.** Every venue would want a different one, and a fixed set would be wrong for all of them.\n"
   },
   "sharedWithTenantIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "BL-178. **Cross-tenant sharing, and it is refused by default for a reason.** A brand operating three venues wants one logo library; two unrelated tenants sharing an asset store is the isolation breach ADR-0011 exists to prevent.\n**Only within one tenant's own scope tree.** A share naming a tenant outside it is refused rather than warned about — this is the one place where a permissive default would be a cross-tenant data leak.\n"
   },
   "tags": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "categoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The asset's category, one of `MediaTaxonomy.categories[].id`; null while unclassified. Set by `bulkUpdateMediaAssets` (`setCategoryId`) (decided 29 September, data model DM4).\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "url": {
    "type": "string",
    "description": "Signed and expiring for private assets; stable CDN URL for public ones."
   },
   "thumbnailUrl": {
    "type": "string",
    "nullable": true
   },
   "referenceCount": {
    "type": "integer",
    "description": "How many surfaces reference this asset. Non-zero refuses deletion.\n"
   },
   "rights": {
    "$ref": "#/components/schemas/MediaRights"
   },
   "isRightsExpired": {
    "type": "boolean"
   },
   "version": {
    "type": "integer"
   },
   "uploadedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "MediaKind": {
  "type": "string",
  "enum": [
   "image",
   "video",
   "audio",
   "document",
   "vector",
   "font",
   "archive"
  ]
 },
 "MediaRights": {
  "x-ticvai-persistence": "none — embedded in asset",
  "type": "object",
  "description": "Licensing terms. Tracked because an expired licence on a live surface is a legal exposure, not a housekeeping item.\n",
  "properties": {
   "licenceKind": {
    "type": "string",
    "enum": [
     "owned",
     "royaltyFree",
     "rightsManaged",
     "creativeCommons",
     "editorialOnly",
     "unknown"
    ]
   },
   "licensor": {
    "type": "string",
    "nullable": true
   },
   "licenceReference": {
    "type": "string",
    "nullable": true
   },
   "validFrom": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "validTo": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "permittedUses": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "web",
      "print",
      "socialMedia",
      "inVenue",
      "advertising",
      "internal"
     ]
    }
   },
   "attributionRequired": {
    "type": "boolean",
    "default": false
   },
   "attributionText": {
    "type": "string",
    "nullable": true
   },
   "permittedTerritories": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "ISO country or region codes. **Empty means unrestricted, which is a claim rather than an absence** — an unknown territory and a worldwide licence are not the same thing, and `licenceKind: unknown` is how the second is said.\n"
   },
   "permittedChannels": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Distribution channel codes, checked by `setMediaDistributionChannels`. Narrower than `permittedUses`, which describes the medium rather than the route.\n"
   },
   "modelReleaseHeld": {
    "type": "boolean",
    "default": false
   },
   "renewalOwner": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   }
  }
 },
 "MediaStatus": {
  "type": "string",
  "enum": [
   "processing",
   "ready",
   "quarantined",
   "failed",
   "archived"
  ]
 },
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
 "Seat": {
  "x-ticvai-persistence": "seating.seat",
  "type": "object",
  "required": [
   "id",
   "sectionCode",
   "rowLabel",
   "seatNumber",
   "attribute"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "**Stable for the life of the seat.** Section, row and number are display labels that change on a refit; this does not. A ticket sold today must still resolve after a renumbering.\n"
   },
   "sectionCode": {
    "type": "string"
   },
   "rowLabel": {
    "type": "string"
   },
   "seatNumber": {
    "type": "string"
   },
   "displayLabel": {
    "type": "string",
    "description": "What the guest sees, e.g. `A2-7-11`."
   },
   "position": {
    "allOf": [
     {
      "$ref": "#/components/schemas/Point"
     }
    ],
    "nullable": true
   },
   "categoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "attribute": {
    "$ref": "#/components/schemas/SeatAttribute"
   },
   "companionSeatIds": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Present on accessible seats. Sold together, released together."
   },
   "isActive": {
    "type": "boolean"
   }
  }
 },
 "SeatAttribute": {
  "type": "string",
  "description": "BL-168. **Extended from eight values on 18 August.** Amenity and view filters needed attributes the original set did not carry, and a guest filtering for *aisle seat with power* was filtering on something the model could not express.\n",
  "enum": [
   "standard",
   "accessible",
   "companion",
   "obstructedView",
   "restrictedLegroom",
   "premium",
   "houseSeat",
   "buffer",
   "aisle",
   "endOfRow",
   "extraLegroom",
   "powerOutlet",
   "tableService",
   "shaded",
   "covered",
   "nearExit",
   "nearAccessibleWc",
   "wheelchairTransfer",
   "limitedRecline",
   "sofa",
   "beanbag"
  ]
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
 "SeatMapStatus": {
  "type": "string",
  "enum": [
   "draft",
   "validated",
   "published",
   "archived"
  ]
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
 "SuggestionBasis": {
  "type": "string",
  "description": "**How the answer was reached, and this is the field the whole design exists for.**\nA venue must be able to see that today's price suggestion is a margin rule and next quarter's is a trained model — **the same operation, the same screen, a different basis** — and a screen that cannot say which is a screen that asks a manager to trust arithmetic it will not show.\n**Swapping a heuristic for a model is a provider change, not a contract change.** That is the point of the abstraction: the frontend, the audit record and the outcome capture all stay exactly as they are.\n",
  "enum": [
   "heuristic",
   "statistical",
   "model",
   "hybrid",
   "manual"
  ]
 },
 "UploadTicket": {
  "x-ticvai-persistence": "assets.media_upload",
  "type": "object",
  "required": [
   "uploadId",
   "uploadUrl",
   "method",
   "expiresAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "uploadId": {
    "type": "string",
    "format": "uuid"
   },
   "uploadUrl": {
    "type": "string",
    "description": "Signed. PUT the file here, then confirm with `/complete`."
   },
   "method": {
    "type": "string",
    "enum": [
     "PUT",
     "POST"
    ]
   },
   "headers": {
    "type": "object",
    "additionalProperties": {
     "type": "string"
    }
   },
   "maxSizeBytes": {
    "type": "integer"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time"
   },
   "filename": {
    "type": "string"
   },
   "contentType": {
    "type": "string"
   },
   "sizeBytes": {
    "type": "integer"
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "assetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "The asset this upload became — created by `completeUpload`, or the asset whose file `replaceMediaAsset` swapped. Null while the transfer is outstanding.\n"
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
