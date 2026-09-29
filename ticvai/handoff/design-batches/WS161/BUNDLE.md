# WS161 — Resource Management Configuration board 7

**10 screens · 11 operations · 16 schemas · 6 permissions**

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

- **Every control that can be refused must be gated.** 6 permissions apply here:
  `APPROVAL_REQUEST, EVENT_CONFIGURE, RESOURCE_BOOK, RESOURCE_CONFIGURE, RESOURCE_VIEW, WORKFORCE_MANAGE`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-913` | Event Resource Planning Command Center | listDetail | 1 | 0 | — |
| `BO-914` | Event Resource Requirement Builder | listDetail | 1 | 0 | — |
| `BO-915` | Venue & Space Allocation | listDetail | 2 | 0 | — |
| `BO-916` | Equipment & Asset Allocation | listDetail | 1 | 0 | — |
| `BO-917` | Event Staff & Personnel Allocation | listDetail | 1 | 0 | — |
| `BO-918` | Event Resource Template Library | configEditor | 2 | 0 | — |
| `BO-919` | AI Event Resource Forecasting | listDetail | 0 | 0 | — |
| `BO-920` | Event Resource Cost Estimator | listDetail | 2 | 0 | — |
| `BO-921` | Multi-Event Allocation & Conflict Optimizer | listDetail | 1 | 0 | — |
| `BO-922` | Event Resource Approval & Readiness Gate | listDetail | 2 | 0 | — |

## Thin screens in this batch

**BO-914, BO-915, BO-916, BO-919, BO-922 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-913",
  "name": "Event Resource Planning Command Center",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "7",
   "number": "01",
   "page": 99
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/event-resource-planning-command-center-bo-913",
   "component": "apps/venue-management-web/src/routes/rentals/EventResourcePlanningCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-914",
    "BO-915",
    "BO-916",
    "BO-917",
    "BO-918",
    "BO-919",
    "BO-920",
    "BO-921",
    "BO-922"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "BO-914",
     "trigger": "Event Resource Requirement Builder",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "carries": [
      "eventId"
     ]
    },
    {
     "to": "BO-915",
     "trigger": "Venue & Space Allocation",
     "provenance": "structural — pack board 7 wiring, 19 September 2026"
    },
    {
     "to": "BO-916",
     "trigger": "Equipment & Asset Allocation",
     "provenance": "structural — pack board 7 wiring, 19 September 2026"
    },
    {
     "to": "BO-917",
     "trigger": "Event Staff & Personnel Allocation",
     "provenance": "structural — pack board 7 wiring, 19 September 2026"
    },
    {
     "to": "BO-918",
     "trigger": "Event Resource Template Library",
     "provenance": "structural — pack board 7 wiring, 19 September 2026"
    },
    {
     "to": "BO-919",
     "trigger": "AI Event Resource Forecasting",
     "provenance": "structural — pack board 7 wiring, 19 September 2026"
    },
    {
     "to": "BO-920",
     "trigger": "Event Resource Cost Estimator",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "carries": [
      "eventId"
     ]
    },
    {
     "to": "BO-921",
     "trigger": "Multi-Event Allocation & Conflict Optimizer",
     "provenance": "structural — pack board 7 wiring, 19 September 2026"
    },
    {
     "to": "BO-922",
     "trigger": "Event Resource Approval & Readiness Gate",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "carries": [
      "eventId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide event and operations managers with a single workspace for understanding the resource readiness of upcoming events.",
  "purposeNote": "Managers can immediately understand resource readiness across upcoming events and identify events requiring operational attention.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 99 §Display"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search event resource planning",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 99 §Users shall filter by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Event",
        "Date",
        "Venue",
        "Event type",
        "Resource status",
        "Readiness",
        "Event manager",
        "Approval status",
        "Risk level",
        "AI Event Summary"
       ],
       "notes": "The pack filters this screen by event, date, venue, event type, resource status, readiness and 4 more — which are present is a decision the pack already made.",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 99 §Users shall filter by"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every event resource planning",
       "columns": [
        "Upcoming events",
        "Events fully resourced",
        "Events partially resourced",
        "Events with critical gaps",
        "Pending resource requests",
        "Pending approvals",
        "Resource conflicts",
        "Staff shortages",
        "Equipment shortages",
        "Venue/space conflicts",
        "Forecast resource cost",
        "Event Readiness"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 99 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected event resource planning",
       "bindsTo": null,
       "columns": [
        "Upcoming events",
        "Events fully resourced",
        "Events partially resourced",
        "Events with critical gaps",
        "Pending resource requests",
        "Pending approvals",
        "Resource conflicts",
        "Staff shortages",
        "Equipment shortages",
        "Venue/space conflicts",
        "Forecast resource cost",
        "Event Readiness"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Corporate Gala”, “Concert A”.",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 99 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The event resource planning list.",
   "error": "Could not load. Names which read failed and leaves the event resource planning untouched.",
   "emptyFirstRun": "No event resource planning yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the event resource planning are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getEventResourcePlan",
    "contract": "catalogue",
    "purpose": "Event resource plans",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Upcoming events",
    "Events fully resourced",
    "Events partially resourced",
    "Events with critical gaps",
    "Pending resource requests",
    "Pending approvals"
   ],
   "params": [
    {
     "name": "eventId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-913",
   "workshopBoard": "wireframes/WS132 Resource Management Configuration Board 7.dc.html#bo-913"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 99. 0 of 22 labels bound to a contract property; 22 of 41 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-914",
  "name": "Event Resource Requirement Builder",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "7",
   "number": "02",
   "page": 100
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/event-resource-requirement-builder-bo-914",
   "component": "apps/venue-management-web/src/routes/rentals/EventResourceRequirementBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-913"
   ],
   "exitTo": [
    "BO-913"
   ],
   "transitions": [
    {
     "to": "BO-913",
     "trigger": "Back to Event Resource Planning Command Center",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "eventId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Define every resource required to deliver a specific event.",
  "purposeNote": "Event managers can define a complete structured resource requirement plan for each event.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 100 §Display"
   },
   {
    "operation": null,
    "why": "**Event Resource Requirement Builder declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
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
       "label": "Every event resource requirement",
       "columns": [
        "Event",
        "Event type",
        "Venue",
        "Event date",
        "Start/end",
        "Expected attendance",
        "Capacity",
        "Event manager",
        "Resource Requirement Sections",
        "Spaces"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 100 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected event resource requirement",
       "bindsTo": null,
       "columns": [
        "Event",
        "Event type",
        "Venue",
        "Event date",
        "Start/end",
        "Expected attendance",
        "Capacity",
        "Event manager",
        "Resource Requirement Sections",
        "Spaces"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Event Selection”, “For each requirement”, “Requirements may change according to”.",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 100 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The event resource requirement list.",
   "error": "Could not load. Names which read failed and leaves the event resource requirement untouched.",
   "emptyFirstRun": "No event resource requirement yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the event resource requirement are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setEventResourcePlan",
    "contract": "catalogue",
    "purpose": "What an event needs",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getEventResourcePlan"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "Event",
    "Event type",
    "Venue",
    "Event date",
    "Start/end",
    "Expected attendance"
   ],
   "params": [
    {
     "name": "eventId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-914",
   "workshopBoard": "wireframes/WS132 Resource Management Configuration Board 7.dc.html#bo-914"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 100. 0 of 10 labels bound to a contract property; 35 of 59 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-915",
  "name": "Venue & Space Allocation",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "7",
   "number": "03",
   "page": 102
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/venue-space-allocation-bo-915",
   "component": "apps/venue-management-web/src/routes/rentals/VenueSpaceAllocation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-913"
   ],
   "exitTo": [
    "BO-913"
   ],
   "transitions": [
    {
     "to": "BO-913",
     "trigger": "Back to Event Resource Planning Command Center",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Assign suitable physical spaces to an event and its operational components.",
  "purposeNote": "Users can assign suitable venues and spaces while TICVAI validates the entire operational occupancy period rather than only the event start/end time.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 102 §Display"
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
       "label": "Every venue space allocation",
       "columns": [
        "Capacity",
        "Layout",
        "Location",
        "Availability",
        "Existing bookings",
        "Setup time",
        "Teardown time",
        "Accessibility",
        "Associated resources",
        "Operational restrictions"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 102 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected venue space allocation",
       "bindsTo": null,
       "columns": [
        "Capacity",
        "Layout",
        "Location",
        "Availability",
        "Existing bookings",
        "Setup time",
        "Teardown time",
        "Accessibility",
        "Associated resources",
        "Operational restrictions"
       ],
       "notes": "The pack groups this record's detail under its own headings: “The interface shall display available”, “Users shall see”, “Event”, “Teardown”, “Conflict Detection”.",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 102 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The venue space allocation list.",
   "error": "Could not load. Names which read failed and leaves the venue space allocation untouched.",
   "emptyFirstRun": "No venue space allocation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the venue space allocation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listSpaces",
    "contract": "catalogue",
    "purpose": "Venue and space allocation",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "bookResource",
    "contract": "resources",
    "purpose": "Book the space",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Capacity",
    "Layout",
    "Location",
    "Availability",
    "Existing bookings",
    "Setup time"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-915",
   "workshopBoard": "wireframes/WS132 Resource Management Configuration Board 7.dc.html#bo-915"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 102. 0 of 10 labels bound to a contract property; 11 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-916",
  "name": "Equipment & Asset Allocation",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "7",
   "number": "04",
   "page": 103
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/equipment-asset-allocation-bo-916",
   "component": "apps/venue-management-web/src/routes/rentals/EquipmentAssetAllocation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-913"
   ],
   "exitTo": [
    "BO-913"
   ],
   "transitions": [
    {
     "to": "BO-913",
     "trigger": "Back to Event Resource Planning Command Center",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allocate physical equipment and operational assets required for events.",
  "purposeNote": "Event equipment requirements can be translated into actual physical-asset allocations without creating resource conflicts.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 103"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 103"
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
       "impliedBy": "allocateResources",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "allocateResources"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The equipment asset allocation list.",
   "error": "Could not load. Names which read failed and leaves the equipment asset allocation untouched.",
   "emptyFirstRun": "No equipment asset allocation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the equipment asset allocation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "allocateResources",
    "contract": "resources",
    "purpose": "Equipment allocation",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-916",
   "workshopBoard": "wireframes/WS132 Resource Management Configuration Board 7.dc.html#bo-916"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 103. 0 of 0 labels bound to a contract property; 0 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-917",
  "name": "Event Staff & Personnel Allocation",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "7",
   "number": "05",
   "page": 105
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/event-staff-personnel-allocation-bo-917",
   "component": "apps/venue-management-web/src/routes/rentals/EventStaffPersonnelAllocation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-913"
   ],
   "exitTo": [
    "BO-913"
   ],
   "transitions": [
    {
     "to": "BO-913",
     "trigger": "Back to Event Resource Planning Command Center",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Each candidate may display) and no metric row",
  "purpose": "Assign qualified staff resources to event roles.",
  "purposeNote": "Event managers can assign qualified staff while TICVAI automatically validates workforce eligibility and availability.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 105 §Each candidate may display"
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
       "label": "Every event staff personnel",
       "columns": [
        "Name",
        "Role",
        "Skill",
        "Certification",
        "Availability",
        "Existing workload",
        "Venue",
        "Overtime impact",
        "AI match"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 105 §Each candidate may display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected event staff personnel",
       "bindsTo": null,
       "columns": [
        "Name",
        "Role",
        "Skill",
        "Certification",
        "Availability",
        "Existing workload",
        "Venue",
        "Overtime impact",
        "AI match"
       ],
       "notes": "The pack groups this record's detail under its own headings: “For each role”, “AV Technician Required”.",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 105 §Each candidate may display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Event manager",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 105 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Supervisor",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 105 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Security",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 105 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Customer service",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 105 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The event staff personnel list.",
   "error": "Could not load. Names which read failed and leaves the event staff personnel untouched.",
   "emptyFirstRun": "No event staff personnel yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the event staff personnel are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createRotaAssignment",
    "contract": "workforce",
    "purpose": "Staff allocation",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listRotaAssignments",
     "getStaffingCoverage"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "Name",
    "Role",
    "Skill",
    "Certification",
    "Availability",
    "Existing workload"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-917",
   "workshopBoard": "wireframes/WS132 Resource Management Configuration Board 7.dc.html#bo-917"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 105. 0 of 9 labels bound to a contract property; 13 of 41 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Event manager, Supervisor, Security, Customer service are choices sent by `createRotaAssignment` (position / requiredRoleId).",
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
  "id": "BO-918",
  "name": "Event Resource Template Library",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "7",
   "number": "06",
   "page": 106
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/event-resource-template-library-bo-918",
   "component": "apps/venue-management-web/src/routes/rentals/EventResourceTemplateLibrary.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-913"
   ],
   "exitTo": [
    "BO-913"
   ],
   "transitions": [
    {
     "to": "BO-913",
     "trigger": "Back to Event Resource Planning Command Center",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Administrators shall configure) and no display directory — it is settings, not a population",
  "purpose": "Allow frequently used event-resource configurations to be saved as reusable templates.",
  "purposeNote": "Reusable event-resource templates significantly reduce manual event setup while maintaining controlled versioning.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Template code",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 106 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Template name",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 106 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Event type",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 106 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Attendance range",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 106 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Applicable venues",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 106 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Required resources",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 106 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Quantities",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 106 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Staff roles",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 106 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Setup duration",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 106 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Teardown duration",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 106 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Dependencies",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 106 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Effective dates",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 106 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Template Application",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 106 §Administrators shall configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The event resource template configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the event resource template untouched.",
   "emptyFirstRun": "No event resource template configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "listResourcePackages",
    "contract": "resources",
    "purpose": "Template library",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "createResourcePackage",
    "contract": "resources",
    "purpose": "Save a template",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-918",
   "workshopBoard": "wireframes/WS132 Resource Management Configuration Board 7.dc.html#bo-918"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 106. 0 of 0 labels bound to a contract property; 13 of 38 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-919",
  "name": "AI Event Resource Forecasting",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "7",
   "number": "07",
   "page": 107
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/ai-event-resource-forecasting-bo-919",
   "component": "apps/venue-management-web/src/routes/rentals/AiEventResourceForecasting.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-913"
   ],
   "exitTo": [
    "BO-913"
   ],
   "transitions": [
    {
     "to": "BO-913",
     "trigger": "Back to Event Resource Planning Command Center",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Predict the resources required for an event before final allocation.",
  "purposeNote": "and predicted requirements.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 107 §Display"
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
       "label": "Every event resource forecasting",
       "columns": [
        "Configured",
        "AI Recommended"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 107 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected event resource forecasting",
       "bindsTo": null,
       "columns": [
        "Configured",
        "AI Recommended"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Security”, “Reason”.",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 107 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The event resource forecasting list.",
   "error": "Could not load. Names which read failed and leaves the event resource forecasting untouched.",
   "emptyFirstRun": "No event resource forecasting yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the event resource forecasting are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "entryState": {
   "preloaded": [
    "Configured",
    "AI Recommended"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-919",
   "workshopBoard": "wireframes/WS132 Resource Management Configuration Board 7.dc.html#bo-919"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 107. 0 of 2 labels bound to a contract property; 2 of 35 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-920",
  "name": "Event Resource Cost Estimator",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "7",
   "number": "08",
   "page": 108
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/event-resource-cost-estimator-bo-920",
   "component": "apps/venue-management-web/src/routes/rentals/EventResourceCostEstimator.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-913"
   ],
   "exitTo": [
    "BO-913"
   ],
   "transitions": [
    {
     "to": "BO-913",
     "trigger": "Back to Event Resource Planning Command Center",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "eventId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Calculate the expected resource cost of delivering an event.",
  "purposeNote": "Event managers can understand expected resource cost before approving the operational event plan.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 108 §Display"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search event resource cost",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 108 §Users shall analyze by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Resource type",
        "Department",
        "Venue",
        "Event phase",
        "Internal/external",
        "Staff/equipment",
        "AI Optimization"
       ],
       "notes": "The pack filters this screen by resource type, department, venue, event phase, internal/external, staff/equipment and 1 more — which are present is a decision the pack already made.",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 108 §Users shall analyze by"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every event resource cost",
       "columns": [
        "Budget",
        "Estimated",
        "Committed",
        "Actual",
        "Variance"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 108 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected event resource cost",
       "bindsTo": null,
       "columns": [
        "Budget",
        "Estimated",
        "Committed",
        "Actual",
        "Variance"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Budget Variance”, “Estimated saving”.",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 108 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Venue cost",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 108 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Equipment cost",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 108 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "External resource cost",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 108 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The event resource cost list.",
   "error": "Could not load. Names which read failed and leaves the event resource cost untouched.",
   "emptyFirstRun": "No event resource cost yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the event resource cost are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getEventResourcePlan",
    "contract": "catalogue",
    "purpose": "Cost estimate",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "estimateEventResourceCost",
    "contract": "catalogue",
    "purpose": "What the event's resource plan costs, by kind",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "Budget",
    "Estimated",
    "Committed",
    "Actual",
    "Variance"
   ],
   "params": [
    {
     "name": "eventId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-920",
   "workshopBoard": "wireframes/WS132 Resource Management Configuration Board 7.dc.html#bo-920"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 108. 0 of 12 labels bound to a contract property; 15 of 35 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** still owed by a contract change: `estimateEventResourceCost`.",
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
  "id": "BO-921",
  "name": "Multi-Event Allocation & Conflict Optimizer",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "7",
   "number": "09",
   "page": 109
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/multi-event-allocation-conflict-optimizer-bo-921",
   "component": "apps/venue-management-web/src/routes/rentals/MultiEventAllocationConflictOptimizer.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-913"
   ],
   "exitTo": [
    "BO-913"
   ],
   "transitions": [
    {
     "to": "BO-913",
     "trigger": "Back to Event Resource Planning Command Center",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Manage scarce resources across simultaneous or overlapping events.",
  "purposeNote": "Managers can resolve shared-resource conflicts across multiple simultaneous events using visual planning and AI-supported optimization.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 109"
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
       "kind": "datePicker",
       "label": "From",
       "operation": "getResourceCalendar",
       "notes": "Sends `?from=` (required).",
       "provenance": "contract resources.yaml GET /resource-calendar"
      },
      {
       "kind": "datePicker",
       "label": "To",
       "operation": "getResourceCalendar",
       "notes": "Sends `?to=` (required).",
       "provenance": "contract resources.yaml GET /resource-calendar"
      },
      {
       "kind": "selectField",
       "label": "Resource type",
       "operation": "getResourceCalendar",
       "notes": "Sends `?resourceTypeId=` (e.g. Security Level 2+, LED screens).",
       "provenance": "contract resources.yaml GET /resource-calendar"
      },
      {
       "kind": "selectField",
       "label": "View",
       "operation": "getResourceCalendar",
       "notes": "Sends `?granularity=`.",
       "provenance": "contract resources.yaml GET /resource-calendar"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Total required",
       "columns": [
        "Total required"
       ],
       "notes": "The pack asks for total required; the contract has no field for it.",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 110"
      },
      {
       "kind": "metricTile",
       "label": "Available",
       "bindsTo": "ResourceCalendarRow",
       "columns": [
        "ResourceCalendarRow.resourceId"
       ],
       "operation": "getResourceCalendar",
       "notes": "Count of resources of the chosen type.",
       "provenance": "contract resources.yaml GET /resource-calendar"
      },
      {
       "kind": "metricTile",
       "label": "Gap",
       "columns": [
        "Gap"
       ],
       "notes": "The pack asks for gap; the contract has no field for it.",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 110"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Shared timeline",
       "bindsTo": "ResourceCalendarRow",
       "columns": [
        "ResourceCalendarRow.resourceName",
        "ResourceCalendarRow.resourceTypeId",
        "ResourceCalendarRow.utilisationPercent",
        "ResourceCalendarRow.segments"
       ],
       "operation": "getResourceCalendar",
       "notes": "Segments in conflict are highlighted; the pack draws events, not resources, across the timeline.",
       "provenance": "contract resources.yaml GET /resource-calendar"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected conflict",
       "bindsTo": "ResourceCalendarRow.segments",
       "columns": [
        "ResourceCalendarRow.segments[].from",
        "ResourceCalendarRow.segments[].to",
        "ResourceCalendarRow.segments[].state",
        "ResourceCalendarRow.segments[].bookingId",
        "ResourceCalendarRow.segments[].conflictsWith",
        "Event",
        "Event priority",
        "Proposed resolution"
       ],
       "operation": "getResourceCalendar",
       "notes": "Event, priority and the proposed resolution are pack labels.",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 110"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The multi-event allocation conflict list.",
   "error": "Could not load. Names which read failed and leaves the multi-event allocation conflict untouched.",
   "emptyFirstRun": "No multi-event allocation conflict yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the multi-event allocation conflict are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getResourceCalendar",
    "contract": "resources",
    "purpose": "Conflicts across events",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-921",
   "workshopBoard": "wireframes/WS132 Resource Management Configuration Board 7.dc.html#bo-921"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 109. 0 of 0 labels bound to a contract property; 0 of 36 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Layout drafted 29 September (VM close-out)** from pack Resource_Management_Configuration_Reference.pdf p.110; contract resources.yaml GET /resource-calendar. Pack labels with no schema field yet (shown as plain labels): Total required, Gap, Required per event, Event priority / SLA / customer tier, AI redistribution proposal.",
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
  "id": "BO-922",
  "name": "Event Resource Approval & Readiness Gate",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "7",
   "number": "10",
   "page": 111
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/event-resource-approval-readiness-gate-bo-922",
   "component": "apps/venue-management-web/src/routes/rentals/EventResourceApprovalReadinessGate.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-913"
   ],
   "exitTo": [
    "BO-913"
   ],
   "transitions": [
    {
     "to": "BO-913",
     "trigger": "Back to Event Resource Planning Command Center",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "eventId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide the final governance checkpoint before an event resource plan becomes operational. Provide TICVAI with a centralized AI Resource Intelligence Engine capable of forecasting demand, identifying resource shortages, recommending optimal staff and physical resources, resolving conflicts, optimizing schedules, simulating operational scenarios, and allowing managers to interact with Resource Management through natural language. Board 8 shall consume information from the previous Resource Management boards rather than recreate their configuration.",
  "purposeNote": "An event cannot be marked operationally ready until mandatory resource requirements, conflicts, qualifications, costs, and approvals have passed configured readiness controls. Board 7 Shared Event Readiness Engine",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 111"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 111"
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
       "impliedBy": "getEventResourcePlan",
       "notes": "One record, read-only."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createApprovalRequest",
       "label": "Create approval request",
       "notes": "The act the screen exists for."
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
   "loading": "The event resource approval list.",
   "error": "Could not load. Names which read failed and leaves the event resource approval untouched.",
   "emptyFirstRun": "No event resource approval yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the event resource approval are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getEventResourcePlan",
    "contract": "catalogue",
    "purpose": "Readiness gate",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "createApprovalRequest",
    "contract": "approvals",
    "purpose": "Send for approval",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-922",
   "workshopBoard": "wireframes/WS132 Resource Management Configuration Board 7.dc.html#bo-922"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 111. 0 of 0 labels bound to a contract property; 0 of 150 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "eventId",
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
 "allocateResources": {
  "method": "POST",
  "path": "/resource-allocations",
  "contract": "resources",
  "summary": "Fill a requirement from the pool, rotating rather than repeating",
  "permission": "RESOURCE_BOOK",
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
  "responds": "ResourceBooking"
 },
 "bookResource": {
  "method": "POST",
  "path": "/resource-bookings",
  "contract": "resources",
  "summary": "Reserve a specific resource for a window — staff only",
  "permission": "RESOURCE_BOOK",
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
  "responds": "ResourceBooking"
 },
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
 "createResourcePackage": {
  "method": "POST",
  "path": "/resource-packages",
  "contract": "resources",
  "summary": "Define a reusable combination",
  "permission": "RESOURCE_CONFIGURE",
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
  "requestBody": "ResourcePackage",
  "responds": "ResourcePackage"
 },
 "createRotaAssignment": {
  "method": "POST",
  "path": "/rota-assignments",
  "contract": "workforce",
  "summary": "Put someone on the rota",
  "permission": "WORKFORCE_MANAGE",
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
  "requestBody": "RotaAssignment",
  "responds": "RotaAssignment"
 },
 "estimateEventResourceCost": {
  "method": "GET",
  "path": "/events/{eventId}/resource-cost",
  "contract": "catalogue",
  "summary": "What an event's resource plan costs, by kind",
  "permission": "EVENT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "includeContractors",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "EventResourceCostEstimate"
 },
 "getEventResourcePlan": {
  "method": "GET",
  "path": "/events/{eventId}/resource-plan",
  "contract": "catalogue",
  "summary": "Everything an event needs, and whether it has been secured",
  "permission": "EVENT_CONFIGURE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "EventResourcePlan"
 },
 "getResourceCalendar": {
  "method": "GET",
  "path": "/resource-calendar",
  "contract": "resources",
  "summary": "Every resource against time, with conflicts already marked",
  "permission": "RESOURCE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
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
    "name": "resourceTypeId",
    "in": "query",
    "required": null
   },
   {
    "name": "categoryId",
    "in": "query",
    "required": null
   },
   {
    "name": "granularity",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "ResourceCalendarRow"
 },
 "listResourcePackages": {
  "method": "GET",
  "path": "/resource-packages",
  "contract": "resources",
  "summary": "Predefined combinations assigned as one",
  "permission": "RESOURCE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ResourcePackage"
 },
 "listSpaces": {
  "method": "GET",
  "path": "/spaces",
  "contract": "catalogue",
  "summary": "Halls, rooms and areas an event can occupy",
  "permission": "EVENT_CONFIGURE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "Space"
 },
 "setEventResourcePlan": {
  "method": "PUT",
  "path": "/events/{eventId}/resource-plan",
  "contract": "catalogue",
  "summary": "State what the event needs, by role and by kind",
  "permission": "EVENT_CONFIGURE",
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
  "requestBody": "EventResourcePlan",
  "responds": "EventResourcePlan"
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
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
 "EventResourceCostEstimate": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over the event resource plan and the rates in resources and workforce, computed at read time",
  "description": "What `estimateEventResourceCost` returns (decided 29 September, readiness close-out): the event's resource plan priced, one line per requirement or contractor, with the total by kind.",
  "required": [
   "eventId",
   "lines",
   "total"
  ],
  "properties": {
   "eventId": {
    "type": "string",
    "format": "uuid"
   },
   "lines": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "kind",
      "quantity",
      "total"
     ],
     "properties": {
      "kind": {
       "type": "string",
       "enum": [
        "venue",
        "equipment",
        "staff",
        "external",
        "transport"
       ],
       "description": "The cost heading on BO-920. Mapped from the requirement kind: space -> venue, equipment and service -> equipment, staff -> staff, contractor -> external, vehicle -> transport."
      },
      "requirementId": {
       "type": "string",
       "format": "uuid",
       "nullable": true,
       "description": "The `EventResourcePlan.requirements[].id` priced; null on a contractor line."
      },
      "organisationId": {
       "type": "string",
       "format": "uuid",
       "nullable": true,
       "description": "The contractor organisation, on an `external` line."
      },
      "label": {
       "type": "string"
      },
      "quantity": {
       "type": "integer",
       "minimum": 0
      },
      "hours": {
       "type": "number",
       "nullable": true,
       "description": "Booked hours the unit cost applies to, where the rate is per hour."
      },
      "unitCost": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "total": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "costSource": {
       "type": "string",
       "enum": [
        "resourceRate",
        "workforceRate",
        "contractorQuote",
        "manual"
       ]
      }
     }
    }
   },
   "totalsByKind": {
    "type": "object",
    "description": "The sum of `lines[].total` for each kind, keyed by `kind`.",
    "additionalProperties": {
     "$ref": "../shared/common.yaml#/components/schemas/Money"
    }
   },
   "total": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "unpricedRequirementIds": {
    "type": "array",
    "description": "Requirements with no rate to price them; left out of `total` rather than guessed.",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   }
  }
 },
 "EventResourcePlan": {
  "type": "object",
  "x-ticvai-persistence": "catalogue.event_resource_plan",
  "description": "Event board 6. **Secured against required is the only number an event manager wants.**\n",
  "properties": {
   "eventId": {
    "type": "string",
    "format": "uuid"
   },
   "requirements": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "id": {
       "type": "string",
       "format": "uuid"
      },
      "kind": {
       "type": "string",
       "enum": [
        "space",
        "equipment",
        "staff",
        "contractor",
        "vehicle",
        "service"
       ]
      },
      "resourceTypeId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "roleCode": {
       "type": "string",
       "nullable": true
      },
      "quantity": {
       "type": "integer"
      },
      "from": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      },
      "to": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      },
      "locationScopePath": {
       "type": "string",
       "nullable": true
      },
      "securedCount": {
       "type": "integer",
       "readOnly": true
      },
      "status": {
       "type": "string",
       "enum": [
        "required",
        "partiallySecured",
        "secured",
        "atRisk"
       ]
      },
      "bookingIds": {
       "type": "array",
       "items": {
        "type": "string",
        "format": "uuid"
       }
      }
     }
    }
   },
   "contractors": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "organisationId": {
       "type": "string",
       "format": "uuid"
      },
      "role": {
       "type": "string"
      },
      "headcount": {
       "type": "integer"
      },
      "accreditationProgrammeId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "insuranceVerified": {
       "type": "boolean",
       "default": false
      }
     }
    }
   },
   "readiness": {
    "type": "string",
    "readOnly": true,
    "enum": [
     "notPlanned",
     "planning",
     "atRisk",
     "ready"
    ]
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "ResourceBooking": {
  "type": "object",
  "x-ticvai-persistence": "resources.booking",
  "required": [
   "id",
   "resourceId",
   "from",
   "to",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "resourceId": {
    "type": "string",
    "format": "uuid"
   },
   "subjectId": {
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
   "status": {
    "$ref": "#/components/schemas/ResourceBookingStatus"
   },
   "holdId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "nullable": true,
    "description": "The `ResourceHold` this booking was converted from, where a guest picked the resource on a venue map (rev 3 REV3-15). Null for a staff booking or an allocation.\n"
   },
   "recurrenceGroupId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Ties the occurrences of a recurring booking. **Cancelling one week does not cancel the series**, and cancelling the series is a separate act with a separate confirmation.\n"
   },
   "depositAuthorisationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The hold, through `orders.authoriseStoredValue` (CF-126). **A deposit taken and refunded is two transactions and a fee; held and released is neither.**\n"
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
   "conditionOut": {
    "type": "string",
    "nullable": true
   },
   "conditionIn": {
    "type": "string",
    "nullable": true
   },
   "syncedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "description": "When the latest offline check-out or check-in write reached the server. **The device times are `checkedOutAt` and `returnedAt`**, taken from each write's `recordedAt`; this is the server's half of the pair naming-and-style 5.2 requires. Null while pending.\n"
   }
  }
 },
 "ResourceBookingStatus": {
  "type": "string",
  "enum": [
   "reserved",
   "checkedOut",
   "returned",
   "overdue",
   "cancelled",
   "noShow"
  ]
 },
 "ResourceCalendarRow": {
  "type": "object",
  "description": "Board 2.01. **One resource across the window, with its states already computed** — including conflict, which a client cannot derive from a booking list.\n",
  "properties": {
   "resourceId": {
    "type": "string",
    "format": "uuid"
   },
   "resourceName": {
    "type": "string"
   },
   "resourceTypeId": {
    "type": "string",
    "format": "uuid"
   },
   "utilisationPercent": {
    "type": "number"
   },
   "segments": {
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
      "state": {
       "type": "string",
       "enum": [
        "available",
        "reserved",
        "assigned",
        "partiallyUtilised",
        "fullyUtilised",
        "unavailable",
        "onBreak",
        "onLeave",
        "underMaintenance",
        "operationallyBlocked",
        "pendingApproval",
        "conflict"
       ]
      },
      "bookingId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "conflictsWith": {
       "type": "array",
       "items": {
        "type": "string",
        "format": "uuid"
       }
      }
     }
    }
   }
  }
 },
 "ResourcePackage": {
  "type": "object",
  "x-ticvai-persistence": "resources.resource_package",
  "description": "Board 1.08. **A package may hold placeholders.** \"One technician\" is a slot, and naming a person would make the package unbookable whenever they are off.\n",
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
   "description": {
    "type": "string",
    "nullable": true
   },
   "applicableVenueIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "components": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/ResourceRequirement"
    }
   },
   "allocationPriority": {
    "type": "integer",
    "default": 0
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "effectiveTo": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "minimumMinutes": {
    "type": "integer",
    "nullable": true
   },
   "maximumMinutes": {
    "type": "integer",
    "nullable": true
   },
   "requiresApproval": {
    "type": "boolean",
    "default": false
   },
   "internalCost": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "ResourceRequirement": {
  "type": "object",
  "x-ticvai-persistence": "resources.resource_requirement",
  "description": "**A type and a quantity, never a named resource.** This is what makes the 26 August rule enforceable — the product states what it needs and the platform decides which one.\nFor resources placed on a published venue map the rule is superseded (decided 29 September, rev 3 REV3-15): the guest names the resource through a `ResourceHold`, and no requirement is needed.\n",
  "required": [
   "quantity"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "resourceTypeId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "categoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "resourceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**A fixed component, and the exception rather than the rule.** Meeting Room A really is Meeting Room A; the technician is not.\n"
   },
   "quantity": {
    "type": "integer",
    "default": 1
   },
   "mandatory": {
    "type": "boolean",
    "default": true
   },
   "requiredQualifications": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "requiredAttributes": {
    "type": "object",
    "additionalProperties": true
   },
   "substituteResourceIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "RotaAssignment": {
  "type": "object",
  "x-ticvai-persistence": "workforce.rota_assignment",
  "required": [
   "principalId",
   "venueId",
   "startsAt",
   "endsAt",
   "position"
  ],
  "properties": {
   "overtimeMinutes": {
    "type": "integer",
    "nullable": true,
    "readOnly": true,
    "description": "BL-044, 1.2.83. **UAE labour law limits working hours and mandates rest periods**, and nothing in the package counted either. Derived from attendance against the shift.\n"
   },
   "restPeriodBefore": {
    "type": "integer",
    "nullable": true,
    "description": "Minutes since the previous shift ended. **The check that stops a closing shift followed by an opening one**, which is legal in most places and unsafe in all of them.\n"
   },
   "breachesWorkingHourLimit": {
    "type": "boolean",
    "default": false,
    "readOnly": true,
    "description": "**Flagged at assignment, not discovered at payroll.** A rota that breaches a statutory limit is a rota somebody has to redo, and finding out a month later means it was worked.\n"
   },
   "labourCost": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "**Cost at the point of scheduling.** A manager building a rota without seeing its cost is a manager who finds out from finance.\n"
   },
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "principalId": {
    "type": "string",
    "format": "uuid"
   },
   "displayName": {
    "type": "string",
    "readOnly": true
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "departmentId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "position": {
    "type": "string",
    "description": "What they are rostered to do — gate steward, cashier, lifeguard, technician. **Most positions never touch a till**, which is why a rota assignment is not a shift.\n**A position code, not a label.** It is the same value as `StaffingRules.minimumCover[].positionCode`, `OpenShift.positionCode` and `StaffingCoverage.positionCode`: coverage counts rostered people per position, so an assignment spelled differently from the rule it fills is counted against nothing and the gap stays open. Tenant-defined, which is why it is not an enum here.\n"
   },
   "requiredRoleId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Checked on assignment. A rota naming someone unqualified is a rota that gets overridden."
   },
   "workstationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Where the position needs a till. **The link between a rota and a cash session**, without merging the two.\n"
   },
   "startsAt": {
    "type": "string",
    "format": "date-time"
   },
   "endsAt": {
    "type": "string",
    "format": "date-time"
   },
   "status": {
    "$ref": "#/components/schemas/RotaStatus"
   },
   "breakMinutes": {
    "type": "integer",
    "nullable": true
   },
   "note": {
    "type": "string",
    "nullable": true
   }
  }
 },
 "RotaStatus": {
  "type": "string",
  "enum": [
   "planned",
   "published",
   "confirmed",
   "swapPending",
   "cancelled",
   "completed",
   "noShow"
  ]
 },
 "Space": {
  "type": "object",
  "x-ticvai-persistence": "catalogue.space",
  "description": "Event board 3.2. **Bookable, as distinct from navigable** — `venue-map` owns the geometry.\n",
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
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "venueMapZoneId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "resourceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**Where the space is also a bookable `resources` resource**, so its calendar and conflict detection come from there rather than a second scheduler.\n"
   },
   "parentSpaceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "maximumCapacity": {
    "type": "integer",
    "nullable": true
   },
   "safeCapacity": {
    "type": "integer",
    "nullable": true
   },
   "setupMinutes": {
    "type": "integer",
    "default": 0
   },
   "teardownMinutes": {
    "type": "integer",
    "default": 0
   },
   "accessRules": {
    "type": "object",
    "nullable": true,
    "additionalProperties": true
   },
   "bookable": {
    "type": "boolean",
    "default": true
   },
   "scopePath": {
    "type": "string"
   }
  }
 }
}
```
