# WS78 — Game and Ride board 1

**10 screens · 0 operations · 0 schemas · 0 permissions**

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

- **Every control that can be refused must be gated.** 0 permissions apply here:
  ``. A control nobody can use must say so,
  not sit enabled and fail.
- **0 of these operations work offline**
  
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-394` | Game & Ride Operations Dashboard | commandCentre | 0 | 1 | — |
| `BO-395` | Game & Ride Directory | configEditor | 0 | 0 | — |
| `BO-396` | Attraction Profile | configEditor | 0 | 0 | — |
| `BO-397` | Attraction Type Configuration | configEditor | 0 | 0 | — |
| `BO-398` | Game & Ride Operational Configuration | listDetail | 0 | 0 | — |
| `BO-399` | Wallet & Credit Acceptance Mapping | listDetail | 0 | 0 | — |
| `BO-400` | Attraction / Reader Mapping | listDetail | 0 | 1 | — |
| `BO-401` | Game Package & Entitlement Association | listDetail | 0 | 0 | — |
| `BO-402` | Configuration Health & Validation | listDetail | 0 | 0 | — |
| `BO-403` | Attraction Audit, Dependencies & Governed Actions | configEditor | 0 | 0 | — |

## Thin screens in this batch

**BO-396, BO-398, BO-399, BO-401 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-394",
  "name": "Game & Ride Operations Dashboard",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "1",
   "number": "1",
   "page": 3
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/game-ride-operations-dashboard-bo-394",
   "component": "apps/venue-management-web/src/routes/games-rides/GameRideOperationsDashboard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-395",
    "BO-396",
    "BO-397",
    "BO-398",
    "BO-399",
    "BO-400",
    "BO-401",
    "BO-402",
    "BO-403"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 1 wiring, 11 September 2026",
     "back": true
    },
    {
     "to": "BO-395",
     "trigger": "Game & Ride Directory",
     "provenance": "structural — pack board 1 wiring, 11 September 2026"
    },
    {
     "to": "BO-396",
     "trigger": "Attraction Profile",
     "provenance": "structural — pack board 1 wiring, 11 September 2026"
    },
    {
     "to": "BO-397",
     "trigger": "Attraction Type Configuration",
     "provenance": "structural — pack board 1 wiring, 11 September 2026"
    },
    {
     "to": "BO-398",
     "trigger": "Game & Ride Operational Configuration",
     "provenance": "structural — pack board 1 wiring, 11 September 2026"
    },
    {
     "to": "BO-399",
     "trigger": "Wallet & Credit Acceptance Mapping",
     "provenance": "structural — pack board 1 wiring, 11 September 2026"
    },
    {
     "to": "BO-400",
     "trigger": "Attraction / Reader Mapping",
     "provenance": "structural — pack board 1 wiring, 11 September 2026"
    },
    {
     "to": "BO-401",
     "trigger": "Game Package & Entitlement Association",
     "provenance": "structural — pack board 1 wiring, 11 September 2026"
    },
    {
     "to": "BO-402",
     "trigger": "Configuration Health & Validation",
     "provenance": "structural — pack board 1 wiring, 11 September 2026"
    },
    {
     "to": "BO-403",
     "trigger": "Attraction Audit, Dependencies & Governed Actions",
     "provenance": "structural — pack board 1 wiring, 11 September 2026"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Management can identify the current operational and configuration status of games and rides from a single screen.",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Header KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide management with one central view of the operational and configuration status of all games, rides, skill games, video games and redemption games.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 7 actions on this screen and the screen declares 0 operations.** Unserved: Add Attraction, Open Attraction, Disable Attraction, View Configuration, View Reader, View Transactions, Filter by venue/zone/type/status. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Game_and_Ride_Module.pdf, page 3 §Actions"
   }
  ],
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Total Attractions",
       "provenance": "pack Game_and_Ride_Module.pdf, page 3 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Active Attractions",
       "provenance": "pack Game_and_Ride_Module.pdf, page 3 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Offline / Unavailable",
       "provenance": "pack Game_and_Ride_Module.pdf, page 3 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Active Readers",
       "provenance": "pack Game_and_Ride_Module.pdf, page 3 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Reader Faults",
       "provenance": "pack Game_and_Ride_Module.pdf, page 3 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Transactions Today",
       "provenance": "pack Game_and_Ride_Module.pdf, page 3 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Wallet Credits Consumed",
       "provenance": "pack Game_and_Ride_Module.pdf, page 3 §Header KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Redemption Credits Earned",
       "provenance": "pack Game_and_Ride_Module.pdf, page 3 §Header KPIs"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Add Attraction",
       "provenance": "pack Game_and_Ride_Module.pdf, page 3 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Open Attraction",
       "provenance": "pack Game_and_Ride_Module.pdf, page 3 §Actions"
      },
      {
       "kind": "destructiveButton",
       "label": "Disable Attraction",
       "provenance": "pack Game_and_Ride_Module.pdf, page 3 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "View Configuration",
       "provenance": "pack Game_and_Ride_Module.pdf, page 3 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "View Reader",
       "provenance": "pack Game_and_Ride_Module.pdf, page 3 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "View Transactions",
       "provenance": "pack Game_and_Ride_Module.pdf, page 3 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Filter by venue/zone/type/status",
       "provenance": "pack Game_and_Ride_Module.pdf, page 3 §Actions"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmDisableAttraction",
    "component": "confirmDialog",
    "trigger": "Disable Attraction",
    "body": "**Disable Attraction on a game ride operations is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Game_and_Ride_Module.pdf, page 3 §Actions"
   }
  ],
  "states": {
   "loading": "The game ride operations list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the game ride operations untouched.",
   "emptyFirstRun": "No game ride operations yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the game ride operations are still there. The pack's own statuses are Active — the state names which is selected.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-394"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 3. 0 of 0 labels bound to a contract property; 20 of 32 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-395",
  "name": "Game & Ride Directory",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "1",
   "number": "2",
   "page": 4
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/game-ride-directory-bo-395",
   "component": "apps/venue-management-web/src/routes/games-rides/GameRideDirectory.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-394"
   ],
   "exitTo": [
    "BO-394"
   ],
   "transitions": [
    {
     "to": "BO-394",
     "trigger": "Back to Game & Ride Operations Dashboard",
     "provenance": "structural — pack board 1 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Authorized users can search, filter and manage the complete game and ride catalogue.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Field Description) and no display directory — it is settings, not a population",
  "purpose": "Maintain the master catalogue of all attractions participating in the payment/redemption ecosystem.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 5 actions on this screen and the screen declares 0 operations.** Unserved: Create, Edit, Clone, View, Export. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Game_and_Ride_Module.pdf, page 4 §Actions"
   }
  ],
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search game ride",
       "provenance": "pack Game_and_Ride_Module.pdf, page 4 §Filters"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Venue",
        "Zone",
        "Attraction Type",
        "Reader Type",
        "Wallet Enabled",
        "Redemption Enabled",
        "Status"
       ],
       "notes": "The pack filters this screen by venue, zone, attraction type, reader type, wallet enabled, redemption enabled and 1 more — which are present is a decision the pack already made.",
       "provenance": "pack Game_and_Ride_Module.pdf, page 4 §Filters"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "textField",
       "label": "Redemption Earn / Spend / N/A",
       "provenance": "pack Game_and_Ride_Module.pdf, page 4 §Field Description"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create",
       "provenance": "pack Game_and_Ride_Module.pdf, page 4 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Edit",
       "provenance": "pack Game_and_Ride_Module.pdf, page 4 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Clone",
       "provenance": "pack Game_and_Ride_Module.pdf, page 4 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "View",
       "provenance": "pack Game_and_Ride_Module.pdf, page 4 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Export",
       "provenance": "pack Game_and_Ride_Module.pdf, page 4 §Actions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The game ride configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the game ride untouched.",
   "emptyFirstRun": "No game ride configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoResults": "The filter narrowed it and the game ride are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-395"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 4. 0 of 7 labels bound to a contract property; 13 of 17 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-396",
  "name": "Attraction Profile",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "1",
   "number": "3",
   "page": 5
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/attraction-profile-bo-396",
   "component": "apps/venue-management-web/src/routes/games-rides/AttractionProfile.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-394"
   ],
   "exitTo": [
    "BO-394"
   ],
   "transitions": [
    {
     "to": "BO-394",
     "trigger": "Back to Game & Ride Operations Dashboard",
     "provenance": "structural — pack board 1 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Each game/ride has a unique master configuration that determines how it participates in TICVAI's payment and entitlement ecosystem.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Transaction Configuration) and no display directory — it is settings, not a population",
  "purpose": "Create or maintain the master record for an individual game or ride.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Wallet Payment Enabled",
       "provenance": "pack Game_and_Ride_Module.pdf, page 5 §Transaction Configuration"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The attraction profile configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the attraction profile untouched.",
   "emptyFirstRun": "No attraction profile configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-396"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 5. 0 of 0 labels bound to a contract property; 1 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-397",
  "name": "Attraction Type Configuration",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "1",
   "number": "4",
   "page": 6
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/attraction-type-configuration-bo-397",
   "component": "apps/venue-management-web/src/routes/games-rides/AttractionTypeConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-394"
   ],
   "exitTo": [
    "BO-394"
   ],
   "transitions": [
    {
     "to": "BO-394",
     "trigger": "Back to Game & Ride Operations Dashboard",
     "provenance": "structural — pack board 1 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Administrators can define reusable attraction categories and establish common transaction behavior.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configuration Fields) and no display directory — it is settings, not a population",
  "purpose": "Configure reusable categories for games and rides so common rules do not have to be configured separately for every attraction.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Type Name",
       "provenance": "pack Game_and_Ride_Module.pdf, page 6 §Configuration Fields"
      },
      {
       "kind": "selectField",
       "label": "Type Code",
       "provenance": "pack Game_and_Ride_Module.pdf, page 6 §Configuration Fields"
      },
      {
       "kind": "selectField",
       "label": "Description",
       "provenance": "pack Game_and_Ride_Module.pdf, page 6 §Configuration Fields"
      },
      {
       "kind": "selectField",
       "label": "Default Reader Type",
       "provenance": "pack Game_and_Ride_Module.pdf, page 6 §Configuration Fields"
      },
      {
       "kind": "selectField",
       "label": "Wallet Allowed",
       "provenance": "pack Game_and_Ride_Module.pdf, page 6 §Configuration Fields"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The attraction type configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the attraction type untouched.",
   "emptyFirstRun": "No attraction type configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-397"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 6. 0 of 0 labels bound to a contract property; 5 of 27 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-398",
  "name": "Game & Ride Operational Configuration",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "1",
   "number": "5",
   "page": 7
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/game-ride-operational-configuration-bo-398",
   "component": "apps/venue-management-web/src/routes/games-rides/GameRideOperationalConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-394"
   ],
   "exitTo": [
    "BO-394"
   ],
   "transitions": [
    {
     "to": "BO-394",
     "trigger": "Back to Game & Ride Operations Dashboard",
     "provenance": "structural — pack board 1 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "An authorized operator can control whether an attraction can accept customer transactions without deleting or rebuilding its configuration.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure whether an attraction is currently available for customer transactions.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 7"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 7"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The game ride operational list.",
   "error": "Could not load. Names which read failed and leaves the game ride operational untouched.",
   "emptyFirstRun": "No game ride operational yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the game ride operational are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-398"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 7. 0 of 0 labels bound to a contract property; 0 of 18 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-399",
  "name": "Wallet & Credit Acceptance Mapping",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "1",
   "number": "6",
   "page": 8
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/wallet-credit-acceptance-mapping-bo-399",
   "component": "apps/venue-management-web/src/routes/games-rides/WalletCreditAcceptanceMapping.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-394"
   ],
   "exitTo": [
    "BO-394"
   ],
   "transitions": [
    {
     "to": "BO-394",
     "trigger": "Back to Game & Ride Operations Dashboard",
     "provenance": "structural — pack board 1 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "The attraction can identify which wallet/credit mechanisms it accepts before a gameplay transaction is authorized.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Define at attraction level which payment/value mechanisms are accepted. The source specifically requires digital-wallet credits to support pay-as-you-go for redemption games, skill games, rides and video games.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 8"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 8"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The wallet credit acceptance list.",
   "error": "Could not load. Names which read failed and leaves the wallet credit acceptance untouched.",
   "emptyFirstRun": "No wallet credit acceptance yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the wallet credit acceptance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-399"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 8. 0 of 0 labels bound to a contract property; 0 of 13 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-400",
  "name": "Attraction / Reader Mapping",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "1",
   "number": "7",
   "page": 8
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/attraction-reader-mapping-bo-400",
   "component": "apps/venue-management-web/src/routes/games-rides/AttractionReaderMapping.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-394"
   ],
   "exitTo": [
    "BO-394"
   ],
   "transitions": [
    {
     "to": "BO-394",
     "trigger": "Back to Game & Ride Operations Dashboard",
     "provenance": "structural — pack board 1 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Every applicable game/ride can be associated with the appropriate reader configuration.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide a high-level association between games/rides and their reader configurations. Important: This screen only performs the mapping. Detailed reader properties belong to Board 2 – Game Reader & Device Configuration.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 8 actions on this screen and the screen declares 0 operations.** Unserved: Video Game Reader, Skill Game Reader, Ride Reader, Assign Reader, Replace Reader, Remove Assignment, View Reader Configuration, Test Mapping. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Game_and_Ride_Module.pdf, page 8 §Support at least"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 8"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 8"
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
       "label": "Video Game Reader",
       "provenance": "pack Game_and_Ride_Module.pdf, page 8 §Support at least"
      },
      {
       "kind": "secondaryButton",
       "label": "Skill Game Reader",
       "provenance": "pack Game_and_Ride_Module.pdf, page 8 §Support at least"
      },
      {
       "kind": "secondaryButton",
       "label": "Ride Reader",
       "provenance": "pack Game_and_Ride_Module.pdf, page 8 §Support at least"
      },
      {
       "kind": "secondaryButton",
       "label": "Assign Reader",
       "provenance": "pack Game_and_Ride_Module.pdf, page 8 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Replace Reader",
       "provenance": "pack Game_and_Ride_Module.pdf, page 8 §Actions"
      },
      {
       "kind": "destructiveButton",
       "label": "Remove Assignment",
       "provenance": "pack Game_and_Ride_Module.pdf, page 8 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "View Reader Configuration",
       "provenance": "pack Game_and_Ride_Module.pdf, page 8 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Test Mapping",
       "provenance": "pack Game_and_Ride_Module.pdf, page 8 §Actions"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmRemoveAssignment",
    "component": "confirmDialog",
    "trigger": "Remove Assignment",
    "body": "**Remove Assignment on a attraction reader mapping is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Game_and_Ride_Module.pdf, page 8 §Actions"
   }
  ],
  "states": {
   "loading": "The attraction reader mapping list.",
   "error": "Could not load. Names which read failed and leaves the attraction reader mapping untouched.",
   "emptyFirstRun": "No attraction reader mapping yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the attraction reader mapping are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-400"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 8. 0 of 0 labels bound to a contract property; 8 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-401",
  "name": "Game Package & Entitlement Association",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "1",
   "number": "8",
   "page": 9
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/game-package-entitlement-association-bo-401",
   "component": "apps/venue-management-web/src/routes/games-rides/GamePackageEntitlementAssociation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-394"
   ],
   "exitTo": [
    "BO-394"
   ],
   "transitions": [
    {
     "to": "BO-394",
     "trigger": "Back to Game & Ride Operations Dashboard",
     "provenance": "structural — pack board 1 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Operators can determine which products/packages grant access to each attraction and under what usage model. Detailed package creation and entitlement logic will remain in Board 4, avoiding duplicate configuration.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Show which packages, tickets and entitlements provide access to each game or ride. The source requires packages containing specific games with configurable entitlement validity, plus products that can allow all games/rides, specific games/rides unlimited times, or specific games/rides a limited number of times.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 0 operations.** Unserved: View Package. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Game_and_Ride_Module.pdf, page 9 §Actions"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 9"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 9"
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
       "label": "View Package",
       "provenance": "pack Game_and_Ride_Module.pdf, page 9 §Actions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The game package entitlement list.",
   "error": "Could not load. Names which read failed and leaves the game package entitlement untouched.",
   "emptyFirstRun": "No game package entitlement yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the game package entitlement are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-401"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 9. 0 of 0 labels bound to a contract property; 1 of 26 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-402",
  "name": "Configuration Health & Validation",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "1",
   "number": "9",
   "page": 10
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/configuration-health-validation-bo-402",
   "component": "apps/venue-management-web/src/routes/games-rides/ConfigurationHealthValidation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-394"
   ],
   "exitTo": [
    "BO-394"
   ],
   "transitions": [
    {
     "to": "BO-394",
     "trigger": "Back to Game & Ride Operations Dashboard",
     "provenance": "structural — pack board 1 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "The system identifies missing or conflicting configuration before an attraction is activated.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Prevent incomplete or conflicting game/ride configurations from becoming operational.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 4 actions on this screen and the screen declares 0 operations.** Unserved: Fix Issue, Open Configuration, Validate Again, View Dependencies. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Game_and_Ride_Module.pdf, page 10 §Actions"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 10"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 10"
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
       "label": "Fix Issue",
       "provenance": "pack Game_and_Ride_Module.pdf, page 10 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Open Configuration",
       "provenance": "pack Game_and_Ride_Module.pdf, page 10 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Validate Again",
       "provenance": "pack Game_and_Ride_Module.pdf, page 10 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "View Dependencies",
       "provenance": "pack Game_and_Ride_Module.pdf, page 10 §Actions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The health validation list.",
   "error": "Could not load. Names which read failed and leaves the health validation untouched.",
   "emptyFirstRun": "No health validation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the health validation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-402"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 10. 0 of 0 labels bound to a contract property; 4 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-403",
  "name": "Attraction Audit, Dependencies & Governed Actions",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "1",
   "number": "10",
   "page": 11
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/attraction-audit-dependencies-governed-actions-bo-403",
   "component": "apps/venue-management-web/src/routes/games-rides/AttractionAuditDependenciesGovernedActions.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-394"
   ],
   "exitTo": [
    "BO-394"
   ],
   "transitions": [
    {
     "to": "BO-394",
     "trigger": "Back to Game & Ride Operations Dashboard",
     "provenance": "structural — pack board 1 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "All significant attraction configuration changes are auditable, and the system warns authorized users about affected dependencies before critical changes. Board 1 — Final Screen Mapping # Screen Primary Role 1 Game & Ride Operations Dashboard Central overview 2 Game & Ride Directory Master catalogue 3 Attraction Profile Individual game/ride setup 4 Attraction Type Configuration Reusable game/ride categories 5 Game & Ride Operational Configuration Availability/status 6 Wallet & Credit Acceptance Mapping Accepted value mechanisms 7 Attraction / Reader Mapping Device association 8 Game Package &",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population",
  "purpose": "Provide traceability and controlled management of attraction configuration changes.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Attraction created",
       "provenance": "pack Game_and_Ride_Module.pdf, page 11 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Type changed",
       "provenance": "pack Game_and_Ride_Module.pdf, page 11 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Reader assigned/replaced",
       "provenance": "pack Game_and_Ride_Module.pdf, page 11 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Wallet acceptance changed",
       "provenance": "pack Game_and_Ride_Module.pdf, page 11 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Package association changed",
       "provenance": "pack Game_and_Ride_Module.pdf, page 11 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Operational status changed",
       "provenance": "pack Game_and_Ride_Module.pdf, page 11 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Activation/deactivation",
       "provenance": "pack Game_and_Ride_Module.pdf, page 11 §Capture"
      },
      {
       "kind": "selectField",
       "label": "User",
       "provenance": "pack Game_and_Ride_Module.pdf, page 11 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Date/time",
       "provenance": "pack Game_and_Ride_Module.pdf, page 11 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Previous value",
       "provenance": "pack Game_and_Ride_Module.pdf, page 11 §Capture"
      },
      {
       "kind": "selectField",
       "label": "New value",
       "provenance": "pack Game_and_Ride_Module.pdf, page 11 §Capture"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The attraction audit dependencies configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the attraction audit dependencies untouched.",
   "emptyFirstRun": "No attraction audit dependencies configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-403"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 11. 0 of 0 labels bound to a contract property; 11 of 56 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
{}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{}
```
