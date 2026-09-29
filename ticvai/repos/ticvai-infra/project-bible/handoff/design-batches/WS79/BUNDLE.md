# WS79 — Game and Ride board 2

**10 screens · 7 operations · 7 schemas · 4 permissions**

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
  `DEVICE_CONFIGURE, DEVICE_MANAGE, DEVICE_VIEW, PRODUCT_CONFIGURE`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-404` | Reader Management Dashboard | commandCentre | 1 | 0 | — |
| `BO-405` | Reader Directory | listDetail | 4 | 1 | — |
| `BO-406` | Reader Profile & Device Setup | configEditor | 1 | 0 | — |
| `BO-407` | Reader Credit & Payment Configuration | configEditor | 2 | 0 | — |
| `BO-408` | Reader / Attraction Assignment | listDetail | 1 | 0 | — |
| `BO-409` | Retap Delay & Transaction Protection | configEditor | 1 | 0 | — |
| `BO-410` | Free Game Glow & Reader Display Rules | configEditor | 1 | 0 | — |
| `BO-411` | Reader Theme & Experience Configuration | configEditor | 1 | 0 | — |
| `BO-412` | Real-Time Tap Validation & Reader Response | listDetail | 1 | 0 | — |
| `BO-413` | Balance Check Reader & Device Test Console | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-408, BO-409, BO-412, BO-413 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-404",
  "name": "Reader Management Dashboard",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "2",
   "number": "1",
   "page": 13
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/reader-management-dashboard-bo-404",
   "component": "apps/venue-management-web/src/routes/games-rides/ReaderManagementDashboard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-405",
    "BO-406",
    "BO-407",
    "BO-408",
    "BO-409",
    "BO-410",
    "BO-411",
    "BO-412",
    "BO-413"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 2 wiring, 11 September 2026",
     "back": true
    },
    {
     "to": "BO-405",
     "trigger": "Reader Directory",
     "provenance": "structural — pack board 2 wiring, 11 September 2026"
    },
    {
     "to": "BO-406",
     "trigger": "Reader Profile & Device Setup",
     "provenance": "structural — pack board 2 wiring, 11 September 2026"
    },
    {
     "to": "BO-407",
     "trigger": "Reader Credit & Payment Configuration",
     "provenance": "structural — pack board 2 wiring, 11 September 2026"
    },
    {
     "to": "BO-408",
     "trigger": "Reader / Attraction Assignment",
     "provenance": "structural — pack board 2 wiring, 11 September 2026"
    },
    {
     "to": "BO-409",
     "trigger": "Retap Delay & Transaction Protection",
     "provenance": "structural — pack board 2 wiring, 11 September 2026"
    },
    {
     "to": "BO-410",
     "trigger": "Free Game Glow & Reader Display Rules",
     "provenance": "structural — pack board 2 wiring, 11 September 2026"
    },
    {
     "to": "BO-411",
     "trigger": "Reader Theme & Experience Configuration",
     "provenance": "structural — pack board 2 wiring, 11 September 2026"
    },
    {
     "to": "BO-412",
     "trigger": "Real-Time Tap Validation & Reader Response",
     "provenance": "structural — pack board 2 wiring, 11 September 2026"
    },
    {
     "to": "BO-413",
     "trigger": "Balance Check Reader & Device Test Console",
     "provenance": "structural — pack board 2 wiring, 11 September 2026"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Authorized users can see the operational and configuration status of all readers from one central screen.",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide a centralized operational overview of all game and ride readers deployed across venues.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search reader",
       "provenance": "pack Game_and_Ride_Module.pdf, page 13 §Filters"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Venue",
        "Zone",
        "Reader Type",
        "Attraction Type",
        "Status",
        "Assigned / Unassigned"
       ],
       "notes": "The pack filters this screen by venue, zone, reader type, attraction type, status, assigned / unassigned — which are present is a decision the pack already made.",
       "provenance": "pack Game_and_Ride_Module.pdf, page 13 §Filters"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Total Readers",
       "provenance": "pack Game_and_Ride_Module.pdf, page 13 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Online Readers",
       "provenance": "pack Game_and_Ride_Module.pdf, page 13 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Offline Readers",
       "provenance": "pack Game_and_Ride_Module.pdf, page 13 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Readers with Errors",
       "provenance": "pack Game_and_Ride_Module.pdf, page 13 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Unassigned Readers",
       "provenance": "pack Game_and_Ride_Module.pdf, page 13 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Transactions Today",
       "provenance": "pack Game_and_Ride_Module.pdf, page 13 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Successful Taps",
       "provenance": "pack Game_and_Ride_Module.pdf, page 13 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Rejected Taps",
       "provenance": "pack Game_and_Ride_Module.pdf, page 13 §KPI Cards"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The reader list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the reader untouched.",
   "emptyFirstRun": "No reader yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the reader are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listReaders",
    "contract": "games",
    "purpose": "Readers and their health",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-404",
   "workshopBoard": "wireframes/WS59 Game and Ride Board 2.dc.html#bo-404"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 13. 0 of 6 labels bound to a contract property; 14 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-405",
  "name": "Reader Directory",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "2",
   "number": "2",
   "page": 14
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/reader-directory-bo-405",
   "component": "apps/venue-management-web/src/routes/games-rides/ReaderDirectory.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-404"
   ],
   "exitTo": [
    "BO-404"
   ],
   "transitions": [
    {
     "to": "BO-404",
     "trigger": "Back to Reader Management Dashboard",
     "provenance": "structural — pack board 2 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Administrators can maintain a centralized registry of all readers and their current assignments.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Directory Columns) and no metric row",
  "purpose": "Maintain the master inventory of physical readers connected to TICVAI. The source requires the ability to define a minimum of three reader types.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Game_and_Ride_Module.pdf, page 14 §Directory Columns"
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
       "label": "Every reader",
       "columns": [
        "Reader ID",
        "Reader Name",
        "Reader Type",
        "Serial Number",
        "Venue",
        "Zone",
        "Assigned Attraction",
        "Firmware Version",
        "Connection Status",
        "Configuration Status",
        "Last Communication"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Game_and_Ride_Module.pdf, page 14 §Directory Columns"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected reader",
       "bindsTo": null,
       "columns": [
        "Reader ID",
        "Reader Name",
        "Reader Type",
        "Serial Number",
        "Venue",
        "Zone",
        "Assigned Attraction",
        "Firmware Version",
        "Connection Status",
        "Configuration Status",
        "Last Communication"
       ],
       "notes": "The pack groups this record's detail under its own headings: “At minimum”, “Page 14 of 105”.",
       "provenance": "pack Game_and_Ride_Module.pdf, page 14 §Directory Columns"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Add Reader",
       "provenance": "pack Game_and_Ride_Module.pdf, page 14 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Edit",
       "provenance": "pack Game_and_Ride_Module.pdf, page 14 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Clone Configuration",
       "operation": "cloneReaderConfiguration",
       "provenance": "pack Game_and_Ride_Module.pdf, page 14 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Assign",
       "provenance": "pack Game_and_Ride_Module.pdf, page 14 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Unassign",
       "provenance": "pack Game_and_Ride_Module.pdf, page 14 §Actions"
      },
      {
       "kind": "destructiveButton",
       "label": "Disable",
       "provenance": "pack Game_and_Ride_Module.pdf, page 14 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Search",
       "provenance": "pack Game_and_Ride_Module.pdf, page 14 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Export",
       "provenance": "pack Game_and_Ride_Module.pdf, page 14 §Actions"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmDisable",
    "component": "confirmDialog",
    "trigger": "Disable",
    "body": "**Disable on a reader is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Game_and_Ride_Module.pdf, page 14 §Actions"
   }
  ],
  "states": {
   "loading": "The reader list.",
   "error": "Could not load. Names which read failed and leaves the reader untouched.",
   "emptyFirstRun": "No reader yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the reader are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listReaders",
    "contract": "games",
    "purpose": "The directory",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "registerDevice",
    "contract": "tenancy",
    "purpose": "Register a new reader device",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration): serves the pack action(s) Add Reader; Edit, Assign, Unassign, Disable"
   },
   {
    "operationId": "setReaderConfiguration",
    "contract": "games",
    "purpose": "Edit the reader, assign/unassign it to a game (gameId) or disable it (status)",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration): serves the pack action(s) Add Reader; Edit, Assign, Unassign, Disable",
    "invalidates": [
     "listReaders"
    ]
   },
   {
    "operationId": "cloneReaderConfiguration",
    "contract": "games",
    "purpose": "Clone configuration",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "preloaded": [
    "Reader ID",
    "Reader Name",
    "Reader Type",
    "Serial Number",
    "Venue",
    "Zone"
   ],
   "params": [
    {
     "name": "readerId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-405",
   "workshopBoard": "wireframes/WS59 Game and Ride Board 2.dc.html#bo-405"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 14. 0 of 11 labels bound to a contract property; 19 of 29 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Search are choices sent by `listReaders`; Add Reader: `registerDevice`; Edit, Assign, Unassign, Disable: `setReaderConfiguration`; Export dropped (export is served by reporting exportReportResult); still owed by a contract change: `cloneReaderConfiguration`.",
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
  "id": "BO-406",
  "name": "Reader Profile & Device Setup",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "2",
   "number": "3",
   "page": 15
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/reader-profile-device-setup-bo-406",
   "component": "apps/venue-management-web/src/routes/games-rides/ReaderProfileDeviceSetup.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-404"
   ],
   "exitTo": [
    "BO-404"
   ],
   "transitions": [
    {
     "to": "BO-404",
     "trigger": "Back to Reader Management Dashboard",
     "provenance": "structural — pack board 2 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Every reader has a uniquely identifiable technical profile and can be associated with its physical deployment location.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Operational Settings) and no display directory — it is settings, not a population",
  "purpose": "Configure the technical and operational identity of an individual reader.",
  "gaps": [
   {
    "operation": null,
    "why": "**Reader Profile & Device Setup declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
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
       "label": "Enabled",
       "provenance": "pack Game_and_Ride_Module.pdf, page 15 §Operational Settings"
      },
      {
       "kind": "selectField",
       "label": "Transaction Enabled",
       "provenance": "pack Game_and_Ride_Module.pdf, page 15 §Operational Settings"
      },
      {
       "kind": "selectField",
       "label": "Offline Mode Allowed",
       "provenance": "pack Game_and_Ride_Module.pdf, page 15 §Operational Settings"
      },
      {
       "kind": "selectField",
       "label": "Logging Enabled",
       "provenance": "pack Game_and_Ride_Module.pdf, page 15 §Operational Settings"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The reader profile device configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the reader profile device untouched.",
   "emptyFirstRun": "No reader profile device configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setReaderProfile",
    "contract": "games",
    "purpose": "How a reader behaves and what it shows",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-406",
   "workshopBoard": "wireframes/WS59 Game and Ride Board 2.dc.html#bo-406"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 15. 0 of 0 labels bound to a contract property; 4 of 26 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-407",
  "name": "Reader Credit & Payment Configuration",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "2",
   "number": "4",
   "page": 16
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/reader-credit-payment-configuration-bo-407",
   "component": "apps/venue-management-web/src/routes/games-rides/ReaderCreditPaymentConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-404"
   ],
   "exitTo": [
    "BO-404"
   ],
   "transitions": [
    {
     "to": "BO-404",
     "trigger": "Back to Reader Management Dashboard",
     "provenance": "structural — pack board 2 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Each reader can determine what customer value it accepts and the required amount for gameplay authorization.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configuration; Configuration Source) and no display directory — it is settings, not a population",
  "purpose": "Define exactly what type of wallet value a reader accepts and how much is required to start the game or ride. This directly implements requirement 10.2.6, which requires configurable: Credit type accepted Credit amount required Attraction type linked to the reader.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "textField",
       "label": "Reader: R-023 – Basketball Skill Game",
       "provenance": "pack Game_and_Ride_Module.pdf, page 16 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Reader-specific",
       "provenance": "pack Game_and_Ride_Module.pdf, page 16 §Configuration Source"
      },
      {
       "kind": "selectField",
       "label": "Attraction price",
       "provenance": "pack Game_and_Ride_Module.pdf, page 16 §Configuration Source"
      },
      {
       "kind": "selectField",
       "label": "Pricing profile",
       "provenance": "pack Game_and_Ride_Module.pdf, page 16 §Configuration Source"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The reader credit payment configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the reader credit payment untouched.",
   "emptyFirstRun": "No reader credit payment configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setReaderConfiguration",
    "contract": "games",
    "purpose": "Profile and device setup",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listReaders"
    ]
   },
   {
    "operationId": "enrolDevice",
    "contract": "tenancy",
    "purpose": "Enrol the device behind it",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-407",
   "workshopBoard": "wireframes/WS59 Game and Ride Board 2.dc.html#bo-407"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 16. 0 of 0 labels bound to a contract property; 4 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "deviceId",
     "from": "session"
    },
    {
     "name": "readerId",
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
  "id": "BO-408",
  "name": "Reader / Attraction Assignment",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "2",
   "number": "5",
   "page": 17
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/reader-attraction-assignment-bo-408",
   "component": "apps/venue-management-web/src/routes/games-rides/ReaderAttractionAssignment.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-404"
   ],
   "exitTo": [
    "BO-404"
   ],
   "transitions": [
    {
     "to": "BO-404",
     "trigger": "Back to Reader Management Dashboard",
     "provenance": "structural — pack board 2 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Readers can be mapped to attractions, and incompatible reader/attraction combinations can be identified before activation.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Assign a physical reader to the appropriate game, ride, or attraction.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 17"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 17"
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
       "impliedBy": "setReaderConfiguration",
       "label": "Save reader configuration",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setReaderConfiguration"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The reader attraction list.",
   "error": "Could not load. Names which read failed and leaves the reader attraction untouched.",
   "emptyFirstRun": "No reader attraction yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the reader attraction are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setReaderConfiguration",
    "contract": "games",
    "purpose": "Credit and payment acceptance",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listReaders"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-408",
   "workshopBoard": "wireframes/WS59 Game and Ride Board 2.dc.html#bo-408"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 17. 0 of 0 labels bound to a contract property; 0 of 19 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "readerId",
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
  "id": "BO-409",
  "name": "Retap Delay & Transaction Protection",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "2",
   "number": "6",
   "page": 17
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/retap-delay-transaction-protection-bo-409",
   "component": "apps/venue-management-web/src/routes/games-rides/RetapDelayTransactionProtection.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-404"
   ],
   "exitTo": [
    "BO-404"
   ],
   "transitions": [
    {
     "to": "BO-404",
     "trigger": "Back to Reader Management Dashboard",
     "provenance": "structural — pack board 2 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "A second tap received within the configured delay does not create an unintended second charge.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configuration) and no display directory — it is settings, not a population",
  "purpose": "Prevent accidental repeated deductions when a customer taps the card multiple times within a short period. The requirement explicitly states that a configurable delay—example 5 seconds—must exist between the first tap and subsequent taps.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Retap Protection: ON/OFF",
       "provenance": "pack Game_and_Ride_Module.pdf, page 17 §Configuration"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "setReaderConfiguration",
       "label": "Save reader configuration",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setReaderConfiguration"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The retap delay transaction configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the retap delay transaction untouched.",
   "emptyFirstRun": "No retap delay transaction configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setReaderConfiguration",
    "contract": "games",
    "purpose": "Which attraction it opens",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listReaders"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-409",
   "workshopBoard": "wireframes/WS59 Game and Ride Board 2.dc.html#bo-409"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 17. 0 of 0 labels bound to a contract property; 1 of 19 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "readerId",
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
  "id": "BO-410",
  "name": "Free Game Glow & Reader Display Rules",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "2",
   "number": "7",
   "page": 18
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/free-game-glow-reader-display-rules-bo-410",
   "component": "apps/venue-management-web/src/routes/games-rides/FreeGameGlowReaderDisplayRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-404"
   ],
   "exitTo": [
    "BO-404"
   ],
   "transitions": [
    {
     "to": "BO-404",
     "trigger": "Back to Reader Management Dashboard",
     "provenance": "structural — pack board 2 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "The reader can visibly differentiate a free-play game from a normally charged game. Exact physical LED capabilities will depend on the selected reader hardware/API.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configuration; Display Configuration) and no display directory — it is settings, not a population",
  "purpose": "Configure how the reader visually communicates that a game or ride is available free of charge. The source specifically requires free games to display a different color on the reader, allowing the customer to recognize that the game is free.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "textField",
       "label": "Free Game Indicator: Enabled",
       "provenance": "pack Game_and_Ride_Module.pdf, page 18 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Free Game Glow",
       "provenance": "pack Game_and_Ride_Module.pdf, page 18 §Display Configuration"
      },
      {
       "kind": "selectField",
       "label": "Display Text",
       "provenance": "pack Game_and_Ride_Module.pdf, page 18 §Display Configuration"
      },
      {
       "kind": "selectField",
       "label": "Icon",
       "provenance": "pack Game_and_Ride_Module.pdf, page 18 §Display Configuration"
      },
      {
       "kind": "selectField",
       "label": "Animation",
       "provenance": "pack Game_and_Ride_Module.pdf, page 18 §Display Configuration"
      },
      {
       "kind": "selectField",
       "label": "Sound",
       "provenance": "pack Game_and_Ride_Module.pdf, page 18 §Display Configuration"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The free game glow configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the free game glow untouched.",
   "emptyFirstRun": "No free game glow configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setReaderConfiguration",
    "contract": "games",
    "purpose": "Retap delay",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listReaders"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-410",
   "workshopBoard": "wireframes/WS59 Game and Ride Board 2.dc.html#bo-410"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 18. 0 of 0 labels bound to a contract property; 6 of 18 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "readerId",
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
  "id": "BO-411",
  "name": "Reader Theme & Experience Configuration",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "2",
   "number": "8",
   "page": 19
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/reader-theme-experience-configuration-bo-411",
   "component": "apps/venue-management-web/src/routes/games-rides/ReaderThemeExperienceConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-404"
   ],
   "exitTo": [
    "BO-404"
   ],
   "transitions": [
    {
     "to": "BO-404",
     "trigger": "Back to Reader Management Dashboard",
     "provenance": "structural — pack board 2 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "BOS administrators can centrally configure and deploy different reader themes by game/ride category.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Theme Configuration) and no display directory — it is settings, not a population",
  "purpose": "Configure different visual experiences for reader categories. The source requires custom themes controlled from BOS, with skill games and rides able to have different reader themes.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Theme Name",
       "provenance": "pack Game_and_Ride_Module.pdf, page 19 §Theme Configuration"
      },
      {
       "kind": "selectField",
       "label": "Background",
       "provenance": "pack Game_and_Ride_Module.pdf, page 19 §Theme Configuration"
      },
      {
       "kind": "selectField",
       "label": "Logo",
       "provenance": "pack Game_and_Ride_Module.pdf, page 19 §Theme Configuration"
      },
      {
       "kind": "selectField",
       "label": "Reader Screen Layout",
       "provenance": "pack Game_and_Ride_Module.pdf, page 19 §Theme Configuration"
      },
      {
       "kind": "selectField",
       "label": "Icons",
       "provenance": "pack Game_and_Ride_Module.pdf, page 19 §Theme Configuration"
      },
      {
       "kind": "selectField",
       "label": "Display Messages",
       "provenance": "pack Game_and_Ride_Module.pdf, page 19 §Theme Configuration"
      },
      {
       "kind": "selectField",
       "label": "Animation",
       "provenance": "pack Game_and_Ride_Module.pdf, page 19 §Theme Configuration"
      },
      {
       "kind": "selectField",
       "label": "Sound Profile",
       "provenance": "pack Game_and_Ride_Module.pdf, page 19 §Theme Configuration"
      },
      {
       "kind": "selectField",
       "label": "Success State",
       "provenance": "pack Game_and_Ride_Module.pdf, page 19 §Theme Configuration"
      },
      {
       "kind": "selectField",
       "label": "Failure State",
       "provenance": "pack Game_and_Ride_Module.pdf, page 19 §Theme Configuration"
      },
      {
       "kind": "selectField",
       "label": "Free Play State",
       "provenance": "pack Game_and_Ride_Module.pdf, page 19 §Theme Configuration"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The reader theme experience configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the reader theme experience untouched.",
   "emptyFirstRun": "No reader theme experience configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setReaderConfiguration",
    "contract": "games",
    "purpose": "Free-game glow and display",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listReaders"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-411",
   "workshopBoard": "wireframes/WS59 Game and Ride Board 2.dc.html#bo-411"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 19. 0 of 0 labels bound to a contract property; 11 of 19 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "readerId",
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
  "id": "BO-412",
  "name": "Real-Time Tap Validation & Reader Response",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "2",
   "number": "9",
   "page": 20
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/real-time-tap-validation-reader-response-bo-412",
   "component": "apps/venue-management-web/src/routes/games-rides/RealTimeTapValidationReaderResponse.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-404"
   ],
   "exitTo": [
    "BO-404"
   ],
   "transitions": [
    {
     "to": "BO-404",
     "trigger": "Back to Reader Management Dashboard",
     "provenance": "structural — pack board 2 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "The reader receives a clear authorization/rejection result before allowing gameplay, and successful transactions update the applicable balance/entitlement.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Identify Card / Wallet) and no metric row",
  "purpose": "Define and visualize what occurs when a customer taps their card/device before gameplay. This screen directly addresses requirement 10.2.13: the system must validate the customer's credit/card balance, bonus and entitlements in real time before the game starts.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Game_and_Ride_Module.pdf, page 20 §Identify Card / Wallet"
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
       "label": "Every real-time tap validation",
       "columns": [
        "↓"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Game_and_Ride_Module.pdf, page 20 §Identify Card / Wallet"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected real-time tap validation",
       "bindsTo": null,
       "columns": [
        "↓"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Customer Tap”, “Check Entitlement”, “Check Bonus”, “Check Paid Balance”, “Apply Pricing”, “Authorize / Reject”.",
       "provenance": "pack Game_and_Ride_Module.pdf, page 20 §Identify Card / Wallet"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The real-time tap validation list.",
   "error": "Could not load. Names which read failed and leaves the real-time tap validation untouched.",
   "emptyFirstRun": "No real-time tap validation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the real-time tap validation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setReaderConfiguration",
    "contract": "games",
    "purpose": "Theme and experience",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listReaders"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "↓"
   ],
   "params": [
    {
     "name": "readerId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-412",
   "workshopBoard": "wireframes/WS59 Game and Ride Board 2.dc.html#bo-412"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 20. 0 of 1 labels bound to a contract property; 1 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-413",
  "name": "Balance Check Reader & Device Test Console",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "2",
   "number": "10",
   "page": 21
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/balance-check-reader-device-test-console-bo-413",
   "component": "apps/venue-management-web/src/routes/games-rides/BalanceCheckReaderDeviceTestConsole.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-404"
   ],
   "exitTo": [
    "BO-404"
   ],
   "transitions": [
    {
     "to": "BO-404",
     "trigger": "Back to Reader Management Dashboard",
     "provenance": "structural — pack board 2 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "A dedicated reader can display customer balances without initiating gameplay, and authorized administrators can test reader configuration before deployment. Board 2 — Exact Design Mapping The visual Board 2 must contain these exact 10 screens in this exact order: # Screen 1 Reader Management Dashboard 2 Reader Directory 3 Reader Profile & Device Setup 4 Reader Credit & Payment Configuration 5 Reader / Attraction Assignment 6 Retap Delay & Transaction Protection 7 Free Game Glow & Reader Display Rules 8 Reader Theme & Experience Configuration 9 Real-Time Tap Validation & Reader Response 10 Bala",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Configure dedicated balance-check readers and provide administrators with a test environment for deployed reader configurations. Requirement 10.2.20 specifically requires a reader through which the customer can check their balance.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Game_and_Ride_Module.pdf, page 21 §Show"
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
       "label": "Every balance check reader",
       "columns": [
        "Validation result",
        "Deduction source"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Game_and_Ride_Module.pdf, page 21 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected balance check reader",
       "bindsTo": null,
       "columns": [
        "Validation result",
        "Deduction source"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Upon tap, display”, “YOUR BALANCE”, “Test Actions”, “Page 21 of 105”, “Requirement coverage”, “Page 22 of 105”.",
       "provenance": "pack Game_and_Ride_Module.pdf, page 21 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The balance check reader list.",
   "error": "Could not load. Names which read failed and leaves the balance check reader untouched.",
   "emptyFirstRun": "No balance check reader yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the balance check reader are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "testReader",
    "contract": "games",
    "purpose": "Balance check and device test",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Validation result",
    "Deduction source"
   ],
   "params": [
    {
     "name": "readerId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-413",
   "workshopBoard": "wireframes/WS59 Game and Ride Board 2.dc.html#bo-413"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 21. 0 of 2 labels bound to a contract property; 8 of 61 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "cloneReaderConfiguration": {
  "method": "POST",
  "path": "/readers/{readerId}/clone",
  "contract": "games",
  "summary": "Copy one reader's configuration onto other readers",
  "permission": "DEVICE_CONFIGURE",
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
  "responds": "Reader"
 },
 "enrolDevice": {
  "method": "POST",
  "path": "/devices/{deviceId}/enrolment",
  "contract": "tenancy",
  "summary": "Take a registered device through enrolment to activation",
  "permission": "DEVICE_MANAGE",
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
  "requestBody": "DeviceEnrolment",
  "responds": "RegisteredDevice"
 },
 "listReaders": {
  "method": "GET",
  "path": "/readers",
  "contract": "games",
  "summary": "Readers, their attractions and their health",
  "permission": "DEVICE_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
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
   }
  ],
  "requestBody": null,
  "responds": "Reader"
 },
 "registerDevice": {
  "method": "POST",
  "path": "/devices",
  "contract": "tenancy",
  "summary": "Register a device",
  "permission": "DEVICE_CONFIGURE",
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
  "requestBody": "RegisteredDevice",
  "responds": "RegisteredDevice"
 },
 "setReaderConfiguration": {
  "method": "PUT",
  "path": "/readers/{readerId}",
  "contract": "games",
  "summary": "What this reader charges, opens, shows and refuses",
  "permission": "DEVICE_CONFIGURE",
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
  "requestBody": "Reader",
  "responds": "Reader"
 },
 "setReaderProfile": {
  "method": "PUT",
  "path": "/reader-profiles",
  "contract": "games",
  "summary": "How a reader behaves and what it shows",
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
  "requestBody": "ReaderProfile",
  "responds": "ReaderProfile"
 },
 "testReader": {
  "method": "POST",
  "path": "/readers/{readerId}/test",
  "contract": "games",
  "summary": "Prove a reader works before a guest finds out it does not",
  "permission": "DEVICE_CONFIGURE",
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
  "responds": "ReaderTestResult"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "DeviceCapability": {
  "type": "string",
  "description": "BL-179. **Something a driver reports, not something the platform provides.** The list grows as vendors are added, which is ADR-0015's whole position: adding a vendor is a driver plus configuration rather than a core change.\n**`genderClassification` is here because `VenueSettings.segregatedAccess. genderVerification` already offers `deviceAssisted` and nothing answered it** — a switch with no driver behind it. Where a venue's access hardware performs the check and the venue chooses to use it, the result is **advisory to the steward and never decisive at the turnstile** (`ValidationResult.advisory`). 3.2.45 asks for rejection; the package deviates deliberately and CF-130 records why.\n",
  "enum": [
   "genderClassification"
  ]
 },
 "DeviceEnrolment": {
  "x-ticvai-persistence": "platform.device",
  "type": "object",
  "description": "BL-160. **The body `enrolDevice` accepts, named so that it writes.**\nIt was an anonymous inline object, and `derive-lineage` reads writes from the schema an operation accepts — so the one operation that moves a device through its whole lifecycle recorded no writes at all, and `platform.device` looked like a table only `registerDevice` touched.\n**Provisioning is inside enrolment rather than beside it**, which is why `configurationProfileId` is here: a device that is enrolled but unprovisioned is a device that will fail at the gate on its first morning.\n",
  "required": [
   "state"
  ],
  "properties": {
   "state": {
    "type": "string",
    "enum": [
     "enrolled",
     "provisioned",
     "active",
     "deactivated",
     "retired"
    ],
    "description": "**The target state, not the current one.** `registered` is absent because `registerDevice` is what produces it and nothing transitions back to it.\n"
   },
   "configurationProfileId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "reason": {
    "type": "string",
    "nullable": true,
    "description": "**Recorded on the `tenancy.device_audit` row, not on the device.** Required in practice for `deactivated` and `retired`, where an investigation six months later needs to know why a gate stopped working.\n"
   }
  }
 },
 "DeviceKind": {
  "type": "string",
  "enum": [
   "receiptPrinter",
   "ticketPrinter",
   "labelPrinter",
   "cashDrawer",
   "barcodeScanner",
   "rfidReader",
   "nfcReader",
   "cardReader",
   "idReader",
   "biometricReader",
   "accessReader",
   "paymentTerminal",
   "customerDisplay",
   "signageDisplay",
   "kitchenDisplay",
   "turnstileController",
   "wristbandEncoder",
   "signaturePad",
   "scale",
   "camera"
  ]
 },
 "Reader": {
  "type": "object",
  "x-ticvai-persistence": "games.reader",
  "description": "Board 2. **A `tenancy` device with a game configuration on it.**",
  "required": [
   "deviceId"
  ],
  "properties": {
   "deviceId": {
    "type": "string",
    "format": "uuid",
    "description": "`tenancy.RegisteredDevice`. **Enrolment, firmware and tamper state live there.**\n"
   },
   "gameId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "readerProfileId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "acceptedCreditTypeIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "acceptsDirectPay": {
    "type": "boolean",
    "default": false
   },
   "retapDelaySeconds": {
    "type": "integer",
    "default": 3,
    "description": "**The setting that stops a guest paying twice for one go.** A wristband held against a reader for a second and a half is two taps to the hardware and one intention to the guest.\n"
   },
   "displayRules": {
    "type": "object",
    "properties": {
     "freeGameGlow": {
      "type": "boolean",
      "default": true,
      "description": "**What tells a guest their entitlement was used rather than their money.** Without it the complaint arrives at the desk.\n"
     },
     "showBalance": {
      "type": "boolean",
      "default": true
     },
     "showPrice": {
      "type": "boolean",
      "default": true
     },
     "themeCode": {
      "type": "string",
      "nullable": true
     },
     "languages": {
      "type": "array",
      "items": {
       "type": "string"
      }
     }
    }
   },
   "ioMapping": {
    "type": "object",
    "additionalProperties": true,
    "description": "Board 9.6. Which output starts the game, which input reports it finished. **Deliberately open.** The keys are the reader model's own I/O lines, so the shape belongs to the vendor adaptor for that model (game readers are a driver, not a build — ADR-0012, ADR-0015), not to this contract.\n"
   },
   "status": {
    "type": "string",
    "enum": [
     "unconfigured",
     "active",
     "offline",
     "maintenance",
     "disabled"
    ]
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "ReaderProfile": {
  "type": "object",
  "x-ticvai-persistence": "games.reader_profile",
  "description": "BL-153. **`games` is well built on the money and what is missing sits at the reader.**\n10.2.14 and 10.2.17 want a different colour for a free game and a different one for insufficient credit — **because a guest at an arcade machine cannot read a message, they can only see a light.** The whole interaction is a second long and happens across a noisy room.\n",
  "required": [
   "id",
   "name"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string"
   },
   "displayBehaviour": {
    "type": "object",
    "description": "**What the reader shows, per outcome.** Colour and tone, because the guest is looking at a machine rather than a screen.\n",
    "properties": {
     "accepted": {
      "type": "string"
     },
     "freeGame": {
      "type": "string"
     },
     "insufficientCredit": {
      "type": "string"
     },
     "cardBlocked": {
      "type": "string"
     },
     "readError": {
      "type": "string"
     }
    }
   },
   "retryPricing": {
    "type": "object",
    "nullable": true,
    "description": "**A retry after a machine fault is not a second play.** Without this a guest whose game crashed pays twice, and the attendant refunds by hand — which is how an arcade loses money and goodwill at once.\n",
    "properties": {
     "isFree": {
      "type": "boolean",
      "default": true
     },
     "withinSeconds": {
      "type": "integer",
      "default": 60
     },
     "maxRetries": {
      "type": "integer",
      "default": 1
     }
    }
   },
   "rePlayWindowSeconds": {
    "type": "integer",
    "nullable": true,
    "description": "**A second tap within this window is the same play, not a new one.** A guest tapping twice because nothing appeared to happen should not be charged twice.\n"
   },
   "entitlementProductIds": {
    "type": "array",
    "description": "**Per-game entitlement.** A pass that includes ten specific rides needs the reader to know which, and a card that works everywhere is a different product.\n",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"
   }
  }
 },
 "ReaderTestResult": {
  "type": "object",
  "description": "Boards 2.10 and 9.9. **Each check separately**, because they send an engineer to different places.\n",
  "properties": {
   "readerId": {
    "type": "string",
    "format": "uuid"
   },
   "testedAt": {
    "type": "string",
    "format": "date-time"
   },
   "checks": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "check": {
       "type": "string",
       "enum": [
        "connectivity",
        "cardRead",
        "balanceCheck",
        "display",
        "sound",
        "gameTrigger",
        "gameCompleteSignal"
       ]
      },
      "passed": {
       "type": "boolean"
      },
      "detail": {
       "type": "string",
       "nullable": true
      }
     }
    }
   },
   "overall": {
    "type": "string",
    "enum": [
     "pass",
     "partial",
     "fail"
    ]
   }
  }
 },
 "RegisteredDevice": {
  "x-ticvai-persistence": "platform.device",
  "type": "object",
  "required": [
   "id",
   "kind",
   "driver",
   "workstationId"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "kind": {
    "$ref": "#/components/schemas/DeviceKind"
   },
   "driver": {
    "type": "string",
    "description": "Built to an open standard where one exists — ESC/POS, UnifiedPOS, OSDP. Adding a vendor is a driver plus configuration, not a core change (ADR-0015).\n"
   },
   "identifier": {
    "type": "string",
    "nullable": true
   },
   "workstationId": {
    "type": "string",
    "format": "uuid"
   },
   "model": {
    "type": "string",
    "nullable": true
   },
   "pushToken": {
    "type": "string",
    "format": "password",
    "nullable": true,
    "writeOnly": true,
    "description": "BL-163. **Guest devices register for push and staff devices did not** — `registerGuestDevice` exists with a token, platform and failure count, and a scanner that cannot be told anything is a scanner somebody has to walk to.\nWrite-only, and marked `writeOnly`: accepted by `registerDevice` and never returned by `listDevices` or `getDevice`. **A push token is a credential**, and the rule that no surface holds a provider key applies here too.\n"
   },
   "pushPlatform": {
    "type": "string",
    "nullable": true,
    "enum": [
     "ios",
     "android",
     "web",
     "windows"
    ]
   },
   "pushFailureCount": {
    "type": "integer",
    "default": 0,
    "readOnly": true,
    "description": "**Consecutive failures.** A token that has failed repeatedly is a device that was wiped or reassigned, and continuing to push to it is how a notification queue fills with nothing.\n"
   },
   "offlineScope": {
    "type": "string",
    "nullable": true,
    "enum": [
     "none",
     "readOnly",
     "sellAndScan",
     "fullVenue"
    ],
    "description": "BL-163. **What this device may do with no connection**, which was unstated for the staff app while `venue-pos` and `venue-scanner` had it settled.\n**`fullVenue` on a personal handset is a decision, not a default** — a device that can do everything offline is a device that carries the whole venue's data in somebody's pocket.\n"
   },
   "firmwareVersion": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "As the device last reported it on its heartbeat."
   },
   "isRequired": {
    "type": "boolean",
    "description": "True blocks shift open when the device is unreachable."
   },
   "status": {
    "type": "string",
    "readOnly": true,
    "enum": [
     "online",
     "offline",
     "error",
     "consumableLow",
     "needsAttention",
     "unknown"
    ],
    "description": "What the device last said on its heartbeat; `unknown` until it has."
   },
   "batteryPercent": {
    "type": "integer",
    "nullable": true,
    "readOnly": true,
    "minimum": 0,
    "maximum": 100,
    "description": "Board 1 of the client's POS design set, 20 August. **A wristband encoder at 8% is a gate that stops working in an hour**, and nothing in the package carried it.\n**Null where the device has no battery**, which is most of them — a receipt printer reporting 100% forever is worse than one reporting nothing.\n"
   },
   "lastCheckedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "description": "**Distinct from `lastHeartbeatAt`.** A heartbeat is the workstation saying the device is attached; a check is the device answering. **A printer with no paper heartbeats perfectly**, which is why the client's board shows both columns.\n"
   },
   "health": {
    "type": "string",
    "enum": [
     "healthy",
     "warning",
     "degraded",
     "offline",
     "unknown"
    ],
    "default": "unknown",
    "readOnly": true,
    "description": "**Derived, not reported.** Computed from heartbeat age, battery, firmware currency and error rate — a device does not know whether it is healthy, and asking it produces a fleet that is 100% healthy and 12% broken.\n"
   },
   "lastHeartbeatAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "capabilities": {
    "type": "array",
    "readOnly": true,
    "items": {
     "$ref": "#/components/schemas/DeviceCapability"
    },
    "description": "BL-179. **What this driver reports it can do, beyond reading media.** ADR-0015 is standards-first — the device does what the device does — and until now a venue could switch on a feature that depended on hardware without anything being able to say whether the hardware was there.\n**A capability absent is a capability unavailable**, not a capability assumed. A venue setting that requires one is refused where no device in scope reports it, rather than silently doing nothing at the gate.\n"
   },
   "enrolmentState": {
    "type": "string",
    "enum": [
     "registered",
     "enrolled",
     "provisioned",
     "active",
     "deactivated",
     "retired"
    ],
    "default": "registered",
    "readOnly": true,
    "description": "BL-160. **Where the device is in its life, which is not the same question as whether it is answering.** `enrolDevice` has taken the whole matrix — registered, enrolled, provisioned, active, deactivated, retired — since 16.1.2, and until now there was no column for it to land in, so the operation read this table and wrote nothing.\n**Distinct from `status` and from `health`.** `status` is what the device last said and `health` is what we computed from it; a decommissioned turnstile still sitting on the network is `online` and `retired` at once, and neither column contradicts the other. **A device that is `retired` is refused at the gate whatever its status says.**\nThe transition itself — who moved it, from what, and why — is a `tenancy.device_audit` record. It is not repeated here, because the latest transition stored in two places is one place to go stale.\n"
   },
   "retiredAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "description": "**Set when `enrolmentState` reaches `retired`, and null otherwise.** Derivable from `tenancy.device_audit`, and kept as a column for the same reason `maintenance.asset.retired_on` is one: a retirement date you reconstruct from an audit log is a date nobody filters a fleet by.\n"
   },
   "configurationProfileId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "**The profile this device was provisioned with.** `enrolDevice` has accepted one since 16.1.3 and there was nowhere to keep it, so the answer to *\"what is this reader configured as\"* lived only in the request that set it.\n"
   }
  }
 }
}
```
