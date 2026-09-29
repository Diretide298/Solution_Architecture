# WS134 — F&B Backend Structure Module Sample Reference v1.0 board 1

**7 screens · 11 operations · 15 schemas · 5 permissions**

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

- **Every control that can be refused must be gated.** 5 permissions apply here:
  `ORDER_VIEW, PRODUCT_CONFIGURE, PRODUCT_VIEW, REPORT_VIEW_VENUE, SCOPE_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-727` | F&B Command Center | commandCentre | 1 | 0 | — |
| `BO-728` | Outlet Management | listDetail | 1 | 0 | — |
| `BO-729` | Create / Edit Outlet | listDetail | 4 | 0 | — |
| `BO-730` | Outlet Types & Templates | listDetail | 3 | 0 | — |
| `BO-731` | Operating Hours & Service Periods | listDetail | 1 | 0 | — |
| `BO-732` | POS & Device Assignment | listDetail | 1 | 0 | — |
| `BO-733` | Service Channel Configuration | listDetail | 3 | 0 | — |

## Thin screens in this batch

**BO-728, BO-729, BO-730, BO-731, BO-732, BO-733 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-727",
  "name": "F&B Command Center",
  "module": "Operations",
  "requiresModule": "fnb",
  "wave": 3,
  "source": {
   "pack": "F&B_Backend_Structure_Module Sample Reference v1.0.pdf",
   "board": "1",
   "number": "1",
   "page": 4
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/operations/f-b-command-center-bo-727",
   "component": "apps/venue-management-web/src/routes/operations/FBCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-728",
    "BO-729",
    "BO-730",
    "BO-731",
    "BO-732",
    "BO-733"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "BO-728",
     "trigger": "Outlet Management",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "BO-729",
     "trigger": "Create / Edit Outlet",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "BO-730",
     "trigger": "Outlet Types & Templates",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "BO-731",
     "trigger": "Operating Hours & Service Periods",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "BO-732",
     "trigger": "POS & Device Assignment",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "BO-733",
     "trigger": "Service Channel Configuration",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Top KPI cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "F&B Command Center",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Today's Sales",
       "provenance": "pack F&B_Backend_Structure_Module Sample Reference v1.0.pdf, page 4 §Top KPI cards"
      },
      {
       "kind": "metricTile",
       "label": "Orders Today",
       "provenance": "pack F&B_Backend_Structure_Module Sample Reference v1.0.pdf, page 4 §Top KPI cards"
      },
      {
       "kind": "metricTile",
       "label": "Average Order Value",
       "provenance": "pack F&B_Backend_Structure_Module Sample Reference v1.0.pdf, page 4 §Top KPI cards"
      },
      {
       "kind": "metricTile",
       "label": "Open Outlets",
       "provenance": "pack F&B_Backend_Structure_Module Sample Reference v1.0.pdf, page 4 §Top KPI cards"
      },
      {
       "kind": "metricTile",
       "label": "Active POS",
       "provenance": "pack F&B_Backend_Structure_Module Sample Reference v1.0.pdf, page 4 §Top KPI cards"
      },
      {
       "kind": "metricTile",
       "label": "Orders in Preparation",
       "provenance": "pack F&B_Backend_Structure_Module Sample Reference v1.0.pdf, page 4 §Top KPI cards"
      },
      {
       "kind": "metricTile",
       "label": "Average Preparation Time",
       "provenance": "pack F&B_Backend_Structure_Module Sample Reference v1.0.pdf, page 4 §Top KPI cards"
      },
      {
       "kind": "metricTile",
       "label": "Unavailable Items",
       "provenance": "pack F&B_Backend_Structure_Module Sample Reference v1.0.pdf, page 4 §Top KPI cards"
      },
      {
       "kind": "metricTile",
       "label": "Critical Stock Alerts",
       "provenance": "pack F&B_Backend_Structure_Module Sample Reference v1.0.pdf, page 4 §Top KPI cards"
      },
      {
       "kind": "metricTile",
       "label": "Operational Alerts",
       "provenance": "pack F&B_Backend_Structure_Module Sample Reference v1.0.pdf, page 4 §Top KPI cards"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The record list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the record untouched.",
   "emptyFirstRun": "No record yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the record are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listOutlets",
    "contract": "tenancy",
    "purpose": "F&B outlets",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-727",
   "workshopBoard": "wireframes/WS57 F&B Backend Structure Module Sample Reference v1.0 Board 1.dc.html#bo-727"
  },
  "apisNote": "Regenerated 9 September 2026 from F&B_Backend_Structure_Module Sample Reference v1.0.pdf page 4. 0 of 0 labels bound to a contract property; 10 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-728",
  "name": "Outlet Management",
  "module": "Operations",
  "requiresModule": "fnb",
  "wave": 3,
  "source": {
   "pack": "F&B_Backend_Structure_Module Sample Reference v1.0.pdf",
   "board": "1",
   "number": "2",
   "page": 5
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/operations/outlet-management-bo-728",
   "component": "apps/venue-management-web/src/routes/operations/OutletManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-727"
   ],
   "exitTo": [
    "BO-727"
   ],
   "transitions": [
    {
     "to": "BO-727",
     "trigger": "Back to F&B Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Outlet Management",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack F&B_Backend_Structure_Module Sample Reference v1.0.pdf, page 5"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack F&B_Backend_Structure_Module Sample Reference v1.0.pdf, page 5"
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
       "impliedBy": "listOutlets",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The outlet list.",
   "error": "Could not load. Names which read failed and leaves the outlet untouched.",
   "emptyFirstRun": "No outlet yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the outlet are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listOutlets",
    "contract": "tenancy",
    "purpose": "List outlets",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-728",
   "workshopBoard": "wireframes/WS57 F&B Backend Structure Module Sample Reference v1.0 Board 1.dc.html#bo-728"
  },
  "apisNote": "Regenerated 9 September 2026 from F&B_Backend_Structure_Module Sample Reference v1.0.pdf page 5. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-729",
  "name": "Create / Edit Outlet",
  "module": "Operations",
  "requiresModule": "fnb",
  "wave": 3,
  "source": {
   "pack": "F&B_Backend_Structure_Module Sample Reference v1.0.pdf",
   "board": "1",
   "number": "3",
   "page": 5
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/operations/create-edit-outlet-bo-729",
   "component": "apps/venue-management-web/src/routes/operations/CreateEditOutlet.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-727"
   ],
   "exitTo": [
    "BO-727"
   ],
   "transitions": [
    {
     "to": "BO-727",
     "trigger": "Back to F&B Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Create / Edit Outlet",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack F&B_Backend_Structure_Module Sample Reference v1.0.pdf, page 5"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack F&B_Backend_Structure_Module Sample Reference v1.0.pdf, page 5"
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
       "impliedBy": "listMenus",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createTable",
       "label": "Create table",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createTable"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The create edit outlet list.",
   "error": "Could not load. Names which read failed and leaves the create edit outlet untouched.",
   "emptyFirstRun": "No create edit outlet yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the create edit outlet are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listMenus",
    "contract": "fnb",
    "purpose": "Menus",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "createTable",
    "contract": "fnb",
    "purpose": "Add a table to the outlet floor",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listMenus"
    ]
   },
   {
    "operationId": "updateTable",
    "contract": "fnb",
    "purpose": "Change a table (covers, shape, joinable)",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listMenus"
    ]
   },
   {
    "operationId": "setSectionLayout",
    "contract": "fnb",
    "purpose": "Divide the floor into sections and give each a server",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listMenus"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "outletId",
     "from": "BO-727"
    },
    {
     "name": "tableId",
     "from": "navigation"
    }
   ],
   "coldEntry": "Opened from BO-727 with the outlet picked there. Opened cold (a bookmark or a refresh), it shows the list to pick from rather than an empty record, and says plainly if the outlet no longer exists."
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-729",
   "workshopBoard": "wireframes/WS57 F&B Backend Structure Module Sample Reference v1.0 Board 1.dc.html#bo-729"
  },
  "apisNote": "Regenerated 9 September 2026 from F&B_Backend_Structure_Module Sample Reference v1.0.pdf page 5. 0 of 0 labels bound to a contract property; 0 of 3 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-730",
  "name": "Outlet Types & Templates",
  "module": "Operations",
  "requiresModule": "fnb",
  "wave": 3,
  "source": {
   "pack": "F&B_Backend_Structure_Module Sample Reference v1.0.pdf",
   "board": "1",
   "number": "4",
   "page": 7
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/operations/outlet-types-templates-bo-730",
   "component": "apps/venue-management-web/src/routes/operations/OutletTypesTemplates.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-727"
   ],
   "exitTo": [
    "BO-727"
   ],
   "transitions": [
    {
     "to": "BO-727",
     "trigger": "Back to F&B Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Outlet Types & Templates",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack F&B_Backend_Structure_Module Sample Reference v1.0.pdf, page 7"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack F&B_Backend_Structure_Module Sample Reference v1.0.pdf, page 7"
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
       "label": "+ Create Template",
       "operation": "setOutletTemplate",
       "provenance": "pack F&B_Backend_Structure_Module Sample Reference v1.0.pdf, page 7 §Buttons"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listMenus",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The outlet types templates list.",
   "error": "Could not load. Names which read failed and leaves the outlet types templates untouched.",
   "emptyFirstRun": "No outlet types templates yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the outlet types templates are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listMenus",
    "contract": "fnb",
    "purpose": "Menu items",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listOutletTemplates",
    "contract": "fnb",
    "purpose": "The outlet templates",
    "trigger": "onLoad"
   },
   {
    "operationId": "setOutletTemplate",
    "contract": "fnb",
    "purpose": "Create template",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-730",
   "workshopBoard": "wireframes/WS57 F&B Backend Structure Module Sample Reference v1.0 Board 1.dc.html#bo-730"
  },
  "apisNote": "Regenerated 9 September 2026 from F&B_Backend_Structure_Module Sample Reference v1.0.pdf page 7. 0 of 0 labels bound to a contract property; 1 of 29 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** still owed by a contract change: `setOutletTemplate`, `listOutletTemplates`.",
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
  "id": "BO-731",
  "name": "Operating Hours & Service Periods",
  "module": "Operations",
  "requiresModule": "fnb",
  "wave": 3,
  "source": {
   "pack": "F&B_Backend_Structure_Module Sample Reference v1.0.pdf",
   "board": "1",
   "number": "5",
   "page": 7
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/operations/operating-hours-service-periods-bo-731",
   "component": "apps/venue-management-web/src/routes/operations/OperatingHoursServicePeriods.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-727"
   ],
   "exitTo": [
    "BO-727"
   ],
   "transitions": [
    {
     "to": "BO-727",
     "trigger": "Back to F&B Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Operating Hours & Service Periods",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack F&B_Backend_Structure_Module Sample Reference v1.0.pdf, page 7"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack F&B_Backend_Structure_Module Sample Reference v1.0.pdf, page 7"
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
       "impliedBy": "listKitchenTickets",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The operating hours service list.",
   "error": "Could not load. Names which read failed and leaves the operating hours service untouched.",
   "emptyFirstRun": "No operating hours service yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the operating hours service are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listKitchenTickets",
    "contract": "fnb",
    "purpose": "Kitchen operations",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-731",
   "workshopBoard": "wireframes/WS57 F&B Backend Structure Module Sample Reference v1.0 Board 1.dc.html#bo-731"
  },
  "apisNote": "Regenerated 9 September 2026 from F&B_Backend_Structure_Module Sample Reference v1.0.pdf page 7. 0 of 0 labels bound to a contract property; 0 of 13 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-732",
  "name": "POS & Device Assignment",
  "module": "Operations",
  "requiresModule": "fnb",
  "wave": 3,
  "source": {
   "pack": "F&B_Backend_Structure_Module Sample Reference v1.0.pdf",
   "board": "1",
   "number": "6",
   "page": 8
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/operations/pos-device-assignment-bo-732",
   "component": "apps/venue-management-web/src/routes/operations/PosDeviceAssignment.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-727"
   ],
   "exitTo": [
    "BO-727"
   ],
   "transitions": [
    {
     "to": "BO-727",
     "trigger": "Back to F&B Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Device cards/table) and no metric row",
  "purpose": "POS & Device Assignment",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack F&B_Backend_Structure_Module Sample Reference v1.0.pdf, page 8 §Device cards/table"
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
       "label": "Every pos device",
       "columns": [
        "Terminal Outlet Type Cashier Payment Printer Status"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack F&B_Backend_Structure_Module Sample Reference v1.0.pdf, page 8 §Device cards/table"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected pos device",
       "bindsTo": null,
       "columns": [
        "Terminal Outlet Type Cashier Payment Printer Status"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Main”, “Restaurant”, “I would also display”.",
       "provenance": "pack F&B_Backend_Structure_Module Sample Reference v1.0.pdf, page 8 §Device cards/table"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The pos device list.",
   "error": "Could not load. Names which read failed and leaves the pos device untouched.",
   "emptyFirstRun": "No pos device yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the pos device are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listOutlets",
    "contract": "tenancy",
    "purpose": "Outlet configuration",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Terminal Outlet Type Cashier Payment Printer Status"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-732",
   "workshopBoard": "wireframes/WS57 F&B Backend Structure Module Sample Reference v1.0 Board 1.dc.html#bo-732"
  },
  "apisNote": "Regenerated 9 September 2026 from F&B_Backend_Structure_Module Sample Reference v1.0.pdf page 8. 0 of 1 labels bound to a contract property; 16 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-733",
  "name": "Service Channel Configuration",
  "module": "Operations",
  "requiresModule": "fnb",
  "wave": 3,
  "source": {
   "pack": "F&B_Backend_Structure_Module Sample Reference v1.0.pdf",
   "board": "1",
   "number": "7",
   "page": 9
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/operations/service-channel-configuration-bo-733",
   "component": "apps/venue-management-web/src/routes/operations/ServiceChannelConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-727"
   ],
   "exitTo": [
    "BO-727"
   ],
   "transitions": [
    {
     "to": "BO-727",
     "trigger": "Back to F&B Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Service Channel Configuration",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack F&B_Backend_Structure_Module Sample Reference v1.0.pdf, page 9"
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
       "label": "Service channels",
       "columns": [
        "Channel",
        "Status",
        "Available outlets",
        "Menu",
        "Price book",
        "Payment",
        "Guest login",
        "Operating hours",
        "Maximum items per order",
        "Minimum order"
       ],
       "notes": "POS Counter, Dine-In, QR Table Order, Mobile App, B2C Web, Kiosk, Takeaway, Delivery, VIP / Hospitality, Event Catering. The bound read is `getKpiValues`, which carries no channel configuration.",
       "provenance": "pack F&B_Backend_Structure_Module Sample Reference v1.0.pdf, page 9"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected channel rules",
       "columns": [
        "Status",
        "Available outlets",
        "Menu",
        "Price book",
        "Payment",
        "Guest login",
        "Operating hours",
        "Maximum items per order",
        "Minimum order"
       ],
       "notes": "The pack's QR Table Ordering example (page 10).",
       "provenance": "pack F&B_Backend_Structure_Module Sample Reference v1.0.pdf, page 10"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Orders by channel",
       "bindsTo": "KpiValue",
       "columns": [
        "KpiValue.name",
        "KpiValue.value",
        "KpiValue.comparison"
       ],
       "operation": "getKpiValues",
       "notes": "The only use `getKpiValues` has here; needs a per-channel KPI code, which is not seeded.",
       "provenance": "contract reporting.yaml GET /kpi-values"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The service channel list.",
   "error": "Could not load. Names which read failed and leaves the service channel untouched.",
   "emptyFirstRun": "No service channel yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the service channel are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getKpiValues",
    "contract": "reporting",
    "purpose": "F&B performance",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "setFnbReservationPolicy",
    "contract": "fnb",
    "purpose": "Set turn times and seating buffers for table reservations",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   },
   {
    "operationId": "setFnbServiceChargePolicy",
    "contract": "fnb",
    "purpose": "Set the service charge per channel",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-733",
   "workshopBoard": "wireframes/WS57 F&B Backend Structure Module Sample Reference v1.0 Board 1.dc.html#bo-733"
  },
  "apisNote": "Regenerated 9 September 2026 from F&B_Backend_Structure_Module Sample Reference v1.0.pdf page 9. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Layout drafted 29 September (VM close-out)** from pack F&B_Backend_Structure_Module Sample Reference v1.0.pdf p.9; pack F&B_Backend_Structure_Module Sample Reference v1.0.pdf p.10; contract reporting.yaml GET /kpi-values. Pack labels with no schema field yet (shown as plain labels): Channel, Channel status, Available outlets, Menu, Price book, Payment options, Guest login, Operating hours, Maximum items per order, Minimum order, A channel-configuration read (bound op is getKpiValues).",
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
 "createTable": {
  "method": "POST",
  "path": "/tables",
  "contract": "fnb",
  "summary": "A table as a thing, not an inference",
  "permission": "PRODUCT_CONFIGURE",
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
  "requestBody": "TableDefinition",
  "responds": "TableDefinition"
 },
 "getKpiValues": {
  "method": "GET",
  "path": "/kpi-values",
  "contract": "reporting",
  "summary": "Current values, against target, with movement",
  "permission": "REPORT_VIEW_VENUE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "kpiIds",
    "in": "query",
    "required": null
   },
   {
    "name": "kpiCodes",
    "in": "query",
    "required": null
   },
   {
    "name": "scopePath",
    "in": "query",
    "required": null
   },
   {
    "name": "period",
    "in": "query",
    "required": null
   },
   {
    "name": "compareTo",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "KpiValue"
 },
 "listKitchenTickets": {
  "method": "GET",
  "path": "/kitchen/tickets",
  "contract": "fnb",
  "summary": "Kitchen ticket queue",
  "permission": "ORDER_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "stationId",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "course",
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
 "listMenus": {
  "method": "GET",
  "path": "/menus",
  "contract": "fnb",
  "summary": "List menus",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "outletId",
    "in": "query",
    "required": null
   },
   {
    "name": "activeAt",
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
 "listOutletTemplates": {
  "method": "GET",
  "path": "/outlet-templates",
  "contract": "fnb",
  "summary": "List outlet templates",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "outletType",
    "in": "query",
    "required": false
   },
   {
    "name": "includeInactive",
    "in": "query",
    "required": false
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
 "listOutlets": {
  "method": "GET",
  "path": "/outlets",
  "contract": "tenancy",
  "summary": "List outlets",
  "permission": "SCOPE_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "venueId",
    "in": "query",
    "required": null
   },
   {
    "name": "kind",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Outlet"
 },
 "setFnbReservationPolicy": {
  "method": "PUT",
  "path": "/reservation-policy",
  "contract": "fnb",
  "summary": "Set turn times and seating buffers",
  "permission": "PRODUCT_CONFIGURE",
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
  "requestBody": "FnbReservationPolicy",
  "responds": "FnbReservationPolicy"
 },
 "setFnbServiceChargePolicy": {
  "method": "PUT",
  "path": "/service-charge-policy",
  "contract": "fnb",
  "summary": "Set the service charge",
  "permission": "PRODUCT_CONFIGURE",
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
  "requestBody": "FnbServiceChargePolicy",
  "responds": "FnbServiceChargePolicy"
 },
 "setOutletTemplate": {
  "method": "PUT",
  "path": "/outlet-templates",
  "contract": "fnb",
  "summary": "Create or replace an outlet template",
  "permission": "PRODUCT_CONFIGURE",
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
  "requestBody": "OutletTemplateInput",
  "responds": "OutletTemplate"
 },
 "setSectionLayout": {
  "method": "PUT",
  "path": "/outlets/{outletId}/sections",
  "contract": "fnb",
  "summary": "Divide the floor into sections and give each a server",
  "permission": "PRODUCT_CONFIGURE",
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
  "requestBody": "SectionLayout",
  "responds": "SectionLayout"
 },
 "updateTable": {
  "method": "PUT",
  "path": "/tables/{tableId}",
  "contract": "fnb",
  "summary": "Change what a table is",
  "permission": "PRODUCT_CONFIGURE",
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
  "requestBody": "TableDefinition",
  "responds": "TableDefinition"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "CoursingPolicy": {
  "type": "string",
  "description": "How a ticket's courses are fired. `fireAndForget` sends every course at once, which is no coursing; `holdAndFire` waits for a server to call each course; `timed` fires on a clock; `phased` staggers by course. **One vocabulary for the ticket (`KitchenTicket.coursing`) and the outlet default (`CourseRules.defaultCoursing`)** — the default said `none` for `fireAndForget` and had no `delayed` until 26 September, so a default could not be copied onto the field it defaults.\n",
  "enum": [
   "fireAndForget",
   "holdAndFire",
   "phased",
   "timed",
   "delayed"
  ]
 },
 "FnbReservationPolicy": {
  "type": "object",
  "x-ticvai-persistence": "fnb.reservation_policy",
  "description": "**How long a table is held, and what sits between one seating and the next.** The source of `TableReservation.durationMinutes`, which keeps its own value as the snapshot.",
  "required": [
   "defaultTurnMinutes",
   "isActive"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "outletId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Null is the venue default; an outlet's own policy overrides it."
   },
   "defaultTurnMinutes": {
    "type": "integer",
    "minimum": 15,
    "description": "The turn time when no party-size band matches."
   },
   "turnTimeBands": {
    "type": "array",
    "description": "**Turn time by party size** — a two-top and a table of eight do not turn at the same speed, and a single default is how a restaurant ends up double-booking its large tables. The first band whose range contains the party size wins.",
    "items": {
     "type": "object",
     "required": [
      "fromPartySize",
      "turnMinutes"
     ],
     "properties": {
      "fromPartySize": {
       "type": "integer",
       "minimum": 1
      },
      "toPartySize": {
       "type": "integer",
       "nullable": true,
       "description": "Null means no upper bound."
      },
      "turnMinutes": {
       "type": "integer",
       "minimum": 15
      }
     }
    }
   },
   "seatingBufferMinutes": {
    "type": "integer",
    "minimum": 0,
    "default": 0,
    "description": "**The reset between seatings** — clearing, laying and a moment for the floor. Zero is a legitimate answer and a stated one."
   },
   "maximumDurationMinutes": {
    "type": "integer",
    "nullable": true,
    "description": "**The ceiling on a single booking.** A reservation extended by hand past this needs the manager, because the table after it is somebody else's booking."
   },
   "isActive": {
    "type": "boolean"
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "FnbServiceChargePolicy": {
  "type": "object",
  "x-ticvai-persistence": "fnb.service_charge_policy",
  "description": "**What the service charge on a bill is, and where it came from.** Every field here answers a question `fnb.sub_bill.service_charge` was being asked and could not answer.\n**Tax and service charge recompute per bill on a split** (`F29`), so the policy is resolved per bill rather than apportioned from the visit — which only works if there is a policy to resolve.",
  "required": [
   "basis",
   "isTaxable",
   "isDiscretionary",
   "distribution"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "basis": {
    "type": "string",
    "enum": [
     "none",
     "percentOfSubtotal",
     "fixedPerCover",
     "fixedPerBill"
    ],
    "description": "`none` is a real answer and the default. **A venue that does not levy one should say so**, rather than leaving a null that reads as unconfigured."
   },
   "ratePercent": {
    "type": "number",
    "nullable": true,
    "description": "Set when `basis` is `percentOfSubtotal`."
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "minimumPartySize": {
    "type": "integer",
    "nullable": true,
    "description": "**The common case for an automatic charge** — parties of six and above. Null applies it to every cover."
   },
   "serviceTypes": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "dineIn",
      "takeaway",
      "delivery",
      "roomService"
     ]
    },
    "description": "**A delivery order charged a dine-in service charge is a complaint.** Empty means every service type."
   },
   "isTaxable": {
    "type": "boolean",
    "description": "**Whether VAT applies to the charge itself.** It does in the UAE, and a bill that taxes the subtotal but not the charge is understated."
   },
   "includedInDisplayPrice": {
    "type": "boolean",
    "description": "**Menu-price inclusive or added at the bill.** The pair of this and `shownSeparately` is what a guest is entitled to see before ordering."
   },
   "shownSeparately": {
    "type": "boolean"
   },
   "isDiscretionary": {
    "type": "boolean",
    "description": "**Whether a guest may have it removed.** A charge that cannot be declined is a price; a charge that can is a request, and the bill has to say which."
   },
   "distribution": {
    "type": "string",
    "enum": [
     "venueRevenue",
     "staffPool",
     "split"
    ],
    "description": "**Not a tip.** `orders` separates `serviceCharge` from a gratuity because it is revenue in most jurisdictions and pooling the two is how a payroll dispute starts. This is the field that carries the distinction into payroll."
   },
   "staffPoolPercent": {
    "type": "number",
    "nullable": true,
    "description": "Set when `distribution` is `split`."
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "effectiveTo": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "KpiValue": {
  "type": "object",
  "description": "BI board 10.3. **Value, target, variance, direction and freshness in one read.**",
  "properties": {
   "kpiId": {
    "type": "string",
    "format": "uuid"
   },
   "code": {
    "type": "string"
   },
   "name": {
    "type": "string"
   },
   "scopePath": {
    "type": "string"
   },
   "period": {
    "type": "string"
   },
   "value": {
    "$ref": "#/components/schemas/MetricValue"
   },
   "target": {
    "allOf": [
     {
      "$ref": "#/components/schemas/MetricValue"
     }
    ],
    "nullable": true
   },
   "comparison": {
    "allOf": [
     {
      "$ref": "#/components/schemas/MetricValue"
     }
    ],
    "nullable": true
   },
   "variancePercent": {
    "type": "number",
    "nullable": true
   },
   "direction": {
    "type": "string",
    "enum": [
     "up",
     "down",
     "flat"
    ]
   },
   "status": {
    "type": "string",
    "enum": [
     "green",
     "amber",
     "red",
     "noTarget"
    ]
   },
   "asOf": {
    "type": "string",
    "format": "date-time"
   },
   "stale": {
    "type": "boolean",
    "description": "**True when the pipeline behind it has not refreshed.** A number nobody flagged as stale is a number somebody will act on.\n"
   }
  }
 },
 "MetricValue": {
  "x-ticvai-persistence-column": "numeric(18,4)",
  "description": "**A reading of a metric or KPI, or a threshold on one.** A `Money` where the metric is money-valued — `MetricSource` lists those in `x-ticvai-money-valued`, and a KPI is when its `unit` is `currency` — and a plain number otherwise. naming-and-style 5.1: money is never a float, at any layer.\nStored as `numeric(18,4)` either way: a money value stores its amount, and currency and scale resolve from the scope as they do for every `Money`.\n",
  "oneOf": [
   {
    "type": "number"
   },
   {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   }
  ]
 },
 "OpeningHoursWindow": {
  "type": "object",
  "description": "26 September, pull audit R088. **One weekly window an outlet is open.** `Outlet.openingHours` was an array of untyped objects. The shape is the one `supportHours.windows` already uses — a day and a from/to — with the times as local `HH:MM` in the region's time zone. Several windows on one day are a split shift, such as lunch and dinner.\n",
  "required": [
   "day",
   "from",
   "to"
  ],
  "properties": {
   "day": {
    "type": "string",
    "enum": [
     "mon",
     "tue",
     "wed",
     "thu",
     "fri",
     "sat",
     "sun"
    ]
   },
   "from": {
    "type": "string",
    "pattern": "^([01][0-9]|2[0-3]):[0-5][0-9]$",
    "description": "Local time, 24-hour `HH:MM`, when the outlet opens."
   },
   "to": {
    "type": "string",
    "pattern": "^([01][0-9]|2[0-3]):[0-5][0-9]$",
    "description": "Local time, 24-hour `HH:MM`, when the outlet closes."
   }
  }
 },
 "Outlet": {
  "type": "object",
  "x-ticvai-persistence": "platform.outlet",
  "required": [
   "id",
   "code",
   "name",
   "venueId",
   "kind"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "code": {
    "type": "string",
    "maxLength": 64
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "$ref": "#/components/schemas/OutletKind"
   },
   "zone": {
    "type": "string",
    "nullable": true
   },
   "stockLocationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Where this outlet draws stock from. A shop and its stockroom are one location; a bar drawing from a central cellar is not.\n"
   },
   "costCenterId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Revenue and cost attribution. Outlet is the natural grain for both."
   },
   "openingHours": {
    "type": "array",
    "description": "The weekly pattern, one entry per window. Several windows on a day are allowed.",
    "items": {
     "$ref": "#/components/schemas/OpeningHoursWindow"
    }
   },
   "isActive": {
    "type": "boolean"
   }
  }
 },
 "OutletKind": {
  "type": "string",
  "enum": [
   "shop",
   "restaurant",
   "bar",
   "cafe",
   "kiosk",
   "gameFloor",
   "ticketOffice",
   "mobile"
  ]
 },
 "OutletTemplate": {
  "type": "object",
  "x-ticvai-persistence": "fnb.outlet_template",
  "description": "**The configuration a new outlet is created from** (decided 29 September, readiness close-out; BO-730). New table. Copied into the outlet at creation and never linked after, so changing a template does not change existing outlets.\n",
  "required": [
   "id",
   "code",
   "name",
   "outletType",
   "serviceModel",
   "scopePath"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "code": {
    "type": "string",
    "maxLength": 64,
    "x-ticvai-unique": "venue"
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "outletType": {
    "$ref": "#/components/schemas/OutletTemplateType"
   },
   "serviceModel": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/ServiceMode"
    }
   },
   "defaultMenuIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "courseRules": {
    "type": "object",
    "nullable": true,
    "properties": {
     "defaultCoursing": {
      "$ref": "#/components/schemas/CoursingPolicy"
     }
    }
   },
   "kitchenSlaMinutes": {
    "type": "integer",
    "nullable": true
   },
   "deliveryPolicyId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "isActive": {
    "type": "boolean"
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "The venue it belongs to; server-set."
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "OutletTemplateInput": {
  "type": "object",
  "x-ticvai-persistence": "none — request only",
  "description": "What `setOutletTemplate` takes (decided 29 September, readiness close-out).",
  "required": [
   "code",
   "name",
   "outletType",
   "serviceModel"
  ],
  "properties": {
   "code": {
    "type": "string",
    "maxLength": 64,
    "pattern": "^[A-Za-z0-9_-]+$",
    "x-ticvai-unique": "venue"
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "outletType": {
    "$ref": "#/components/schemas/OutletTemplateType"
   },
   "serviceModel": {
    "type": "array",
    "minItems": 1,
    "description": "The service modes the outlet offers, e.g. `[tableService, collection]`.",
    "items": {
     "$ref": "#/components/schemas/ServiceMode"
    }
   },
   "defaultMenuIds": {
    "type": "array",
    "maxItems": 20,
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "courseRules": {
    "type": "object",
    "nullable": true,
    "description": "The coursing default a new outlet starts with; the same shape `setCourseRules` stores per outlet.",
    "properties": {
     "defaultCoursing": {
      "$ref": "#/components/schemas/CoursingPolicy"
     }
    }
   },
   "kitchenSlaMinutes": {
    "type": "integer",
    "minimum": 1,
    "maximum": 240,
    "nullable": true,
    "description": "The default ticket target, in minutes, before `setKitchenSla` sets per-mode targets."
   },
   "deliveryPolicyId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "isActive": {
    "type": "boolean",
    "default": true
   }
  }
 },
 "OutletTemplateType": {
  "type": "string",
  "enum": [
   "restaurant",
   "bar",
   "cafe",
   "kiosk",
   "mobile"
  ],
  "description": "The F&B kinds of `tenancy.OutletKind`, repeated here because a satellite does not reference another contract's schema."
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
 "SectionLayout": {
  "type": "object",
  "description": "An outlet's floor divided into sections, each with its server (`setSectionLayout`).",
  "required": [
   "sections"
  ],
  "properties": {
   "sections": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "name",
      "tableIds"
     ],
     "properties": {
      "name": {
       "type": "string"
      },
      "tableIds": {
       "type": "array",
       "items": {
        "type": "string",
        "format": "uuid"
       }
      },
      "serverPrincipalId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "servicePeriod": {
       "type": "string",
       "nullable": true
      }
     }
    }
   }
  }
 },
 "ServiceMode": {
  "type": "string",
  "enum": [
   "quickService",
   "tableService",
   "roomService",
   "collection",
   "delivery"
  ]
 },
 "TableDefinition": {
  "x-ticvai-persistence": "fnb.dining_table",
  "type": "object",
  "description": "A restaurant (dining) table, reserved with `createTableReservation`. Not a map-bookable `resources` table, which is a non-dining spot sold like a cabana (decided 29 September, rev 3 GAP-C2).",
  "required": [
   "id",
   "label",
   "capacity"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "label": {
    "type": "string",
    "maxLength": 32,
    "x-ticvai-unique": "venue",
    "description": "**The table code, unique per venue** (decided 28 September, audit R108). Two tables in one venue never share a label, across all its outlets, so *T12* names one table wherever it is read. `createTable` and `updateTable` refuse a duplicate with `409` `duplicate-code`.\n"
   },
   "capacity": {
    "type": "integer",
    "minimum": 1
   },
   "zone": {
    "type": "string",
    "nullable": true
   },
   "position": {
    "type": "object",
    "properties": {
     "x": {
      "type": "number"
     },
     "y": {
      "type": "number"
     }
    }
   },
   "shape": {
    "type": "string",
    "enum": [
     "round",
     "square",
     "rectangle",
     "booth",
     "bar"
    ]
   },
   "isOutOfService": {
    "type": "boolean",
    "default": false,
    "description": "**Damaged, or its section closed.** `getTableMap` shows it as `outOfService` and a claim on it is refused with `tableOutOfService`."
   }
  }
 }
}
```
