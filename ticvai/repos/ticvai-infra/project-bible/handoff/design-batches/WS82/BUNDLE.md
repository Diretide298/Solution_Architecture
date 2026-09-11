# WS82 — Game and Ride board 5

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
| `BO-434` | Game & Ride Pricing Command Center | commandCentre | 0 | 0 | — |
| `BO-435` | Standard Game & Ride Price Configuration | configEditor | 0 | 0 | — |
| `BO-436` | Group Pricing Configuration | configEditor | 0 | 0 | — |
| `BO-437` | Peak / Non-Peak Dynamic Pricing | configEditor | 0 | 0 | — |
| `BO-438` | Pricing Calendar & Exception Dates | configEditor | 0 | 0 | — |
| `BO-439` | Normal & VIP Pricing Configuration | configEditor | 0 | 0 | — |
| `BO-440` | Retry Price Configuration | listDetail | 0 | 0 | — |
| `BO-441` | Price Priority & Conflict Rules | listDetail | 0 | 0 | — |
| `BO-442` | Effective Pricing & Reader Price Preview | listDetail | 0 | 0 | — |
| `BO-443` | Pricing Audit, Approval & Publication | listDetail | 0 | 1 | — |

## Thin screens in this batch

**BO-439, BO-440, BO-441, BO-442, BO-443 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-434",
  "name": "Game & Ride Pricing Command Center",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "5",
   "number": "1",
   "page": 43
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/game-ride-pricing-command-center-bo-434",
   "component": "apps/venue-management-web/src/routes/games-rides/GameRidePricingCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-435",
    "BO-436",
    "BO-437",
    "BO-438",
    "BO-439",
    "BO-440",
    "BO-441",
    "BO-442",
    "BO-443"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 5 wiring, 11 September 2026",
     "back": true
    },
    {
     "to": "BO-435",
     "trigger": "Standard Game & Ride Price Configuration",
     "provenance": "structural — pack board 5 wiring, 11 September 2026"
    },
    {
     "to": "BO-436",
     "trigger": "Group Pricing Configuration",
     "provenance": "structural — pack board 5 wiring, 11 September 2026"
    },
    {
     "to": "BO-437",
     "trigger": "Peak / Non-Peak Dynamic Pricing",
     "provenance": "structural — pack board 5 wiring, 11 September 2026"
    },
    {
     "to": "BO-438",
     "trigger": "Pricing Calendar & Exception Dates",
     "provenance": "structural — pack board 5 wiring, 11 September 2026"
    },
    {
     "to": "BO-439",
     "trigger": "Normal & VIP Pricing Configuration",
     "provenance": "structural — pack board 5 wiring, 11 September 2026"
    },
    {
     "to": "BO-440",
     "trigger": "Retry Price Configuration",
     "provenance": "structural — pack board 5 wiring, 11 September 2026"
    },
    {
     "to": "BO-441",
     "trigger": "Price Priority & Conflict Rules",
     "provenance": "structural — pack board 5 wiring, 11 September 2026"
    },
    {
     "to": "BO-442",
     "trigger": "Effective Pricing & Reader Price Preview",
     "provenance": "structural — pack board 5 wiring, 11 September 2026"
    },
    {
     "to": "BO-443",
     "trigger": "Pricing Audit, Approval & Publication",
     "provenance": "structural — pack board 5 wiring, 11 September 2026"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Administrators can immediately identify current game/ride prices, active special pricing, upcoming changes, and missing/conflicting configurations.",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide a central view of all game and ride pricing configurations, active pricing rules, upcoming changes, and pricing issues.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search game ride pricing",
       "provenance": "pack Game_and_Ride_Module.pdf, page 43 §Filters"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Venue",
        "Zone",
        "Attraction",
        "Attraction Type",
        "Pricing Type",
        "VIP Enabled",
        "Effective Date",
        "Status"
       ],
       "notes": "The pack filters this screen by venue, zone, attraction, attraction type, pricing type, vip enabled and 2 more — which are present is a decision the pack already made.",
       "provenance": "pack Game_and_Ride_Module.pdf, page 43 §Filters"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Total Priced Attractions",
       "provenance": "pack Game_and_Ride_Module.pdf, page 43 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Active Price Rules",
       "provenance": "pack Game_and_Ride_Module.pdf, page 43 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Peak Pricing Active",
       "provenance": "pack Game_and_Ride_Module.pdf, page 43 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "VIP Pricing Enabled",
       "provenance": "pack Game_and_Ride_Module.pdf, page 43 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Retry Pricing Enabled",
       "provenance": "pack Game_and_Ride_Module.pdf, page 43 §KPI Cards"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The game ride pricing list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the game ride pricing untouched.",
   "emptyFirstRun": "No game ride pricing yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the game ride pricing are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-434"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 43. 0 of 8 labels bound to a contract property; 13 of 26 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-435",
  "name": "Standard Game & Ride Price Configuration",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "5",
   "number": "2",
   "page": 44
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/standard-game-ride-price-configuration-bo-435",
   "component": "apps/venue-management-web/src/routes/games-rides/StandardGameRidePriceConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-434"
   ],
   "exitTo": [
    "BO-434"
   ],
   "transitions": [
    {
     "to": "BO-434",
     "trigger": "Back to Game & Ride Pricing Command Center",
     "provenance": "structural — pack board 5 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Every payable game/ride can have a standard base price with controlled effective dates.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configuration) and no display directory — it is settings, not a population",
  "purpose": "Define the normal base price charged to play a specific game or ride. The source requires that prices be defined for each game.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Price Rule Name",
       "provenance": "pack Game_and_Ride_Module.pdf, page 44 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Attraction",
       "provenance": "pack Game_and_Ride_Module.pdf, page 44 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Attraction Type",
       "provenance": "pack Game_and_Ride_Module.pdf, page 44 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Game_and_Ride_Module.pdf, page 44 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Zone",
       "provenance": "pack Game_and_Ride_Module.pdf, page 44 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Standard Price",
       "provenance": "pack Game_and_Ride_Module.pdf, page 44 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Currency",
       "provenance": "pack Game_and_Ride_Module.pdf, page 44 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Wallet/Credit Equivalent",
       "provenance": "pack Game_and_Ride_Module.pdf, page 44 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Effective From",
       "provenance": "pack Game_and_Ride_Module.pdf, page 44 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Effective To",
       "provenance": "pack Game_and_Ride_Module.pdf, page 44 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Status",
       "provenance": "pack Game_and_Ride_Module.pdf, page 44 §Configuration"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The standard game ride configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the standard game ride untouched.",
   "emptyFirstRun": "No standard game ride configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-435"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 44. 0 of 0 labels bound to a contract property; 11 of 18 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-436",
  "name": "Group Pricing Configuration",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "5",
   "number": "3",
   "page": 45
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/group-pricing-configuration-bo-436",
   "component": "apps/venue-management-web/src/routes/games-rides/GroupPricingConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-434"
   ],
   "exitTo": [
    "BO-434"
   ],
   "transitions": [
    {
     "to": "BO-434",
     "trigger": "Back to Game & Ride Pricing Command Center",
     "provenance": "structural — pack board 5 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "A price can be assigned centrally to a group of games/rides and inherited by all linked attractions.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Group Setup; Configuration Options) and no display directory — it is settings, not a population",
  "purpose": "Allow multiple games or rides to share a common pricing rule instead of configuring each attraction individually.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Pricing Group Name",
       "provenance": "pack Game_and_Ride_Module.pdf, page 45 §Group Setup"
      },
      {
       "kind": "selectField",
       "label": "Group Code",
       "provenance": "pack Game_and_Ride_Module.pdf, page 45 §Group Setup"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Game_and_Ride_Module.pdf, page 45 §Group Setup"
      },
      {
       "kind": "selectField",
       "label": "Attraction Type",
       "provenance": "pack Game_and_Ride_Module.pdf, page 45 §Group Setup"
      },
      {
       "kind": "selectField",
       "label": "Price",
       "provenance": "pack Game_and_Ride_Module.pdf, page 45 §Group Setup"
      },
      {
       "kind": "selectField",
       "label": "Currency",
       "provenance": "pack Game_and_Ride_Module.pdf, page 45 §Group Setup"
      },
      {
       "kind": "selectField",
       "label": "Effective Period",
       "provenance": "pack Game_and_Ride_Module.pdf, page 45 §Group Setup"
      },
      {
       "kind": "selectField",
       "label": "Status",
       "provenance": "pack Game_and_Ride_Module.pdf, page 45 §Group Setup"
      },
      {
       "kind": "selectField",
       "label": "Add Attraction",
       "provenance": "pack Game_and_Ride_Module.pdf, page 45 §Configuration Options"
      },
      {
       "kind": "selectField",
       "label": "Remove Attraction",
       "provenance": "pack Game_and_Ride_Module.pdf, page 45 §Configuration Options"
      },
      {
       "kind": "textField",
       "label": "Apply price to all",
       "provenance": "pack Game_and_Ride_Module.pdf, page 45 §Configuration Options"
      },
      {
       "kind": "textField",
       "label": "Individual override allowed: Yes/No",
       "provenance": "pack Game_and_Ride_Module.pdf, page 45 §Configuration Options"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The group pricing configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the group pricing untouched.",
   "emptyFirstRun": "No group pricing configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-436"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 45. 0 of 0 labels bound to a contract property; 12 of 23 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-437",
  "name": "Peak / Non-Peak Dynamic Pricing",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "5",
   "number": "4",
   "page": 46
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/peak-non-peak-dynamic-pricing-bo-437",
   "component": "apps/venue-management-web/src/routes/games-rides/PeakNonPeakDynamicPricing.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-434"
   ],
   "exitTo": [
    "BO-434"
   ],
   "transitions": [
    {
     "to": "BO-434",
     "trigger": "Back to Game & Ride Pricing Command Center",
     "provenance": "structural — pack board 5 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "The backend automatically determines the applicable price using configured date/time rules.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Rule Configuration) and no display directory — it is settings, not a population",
  "purpose": "Configure different game/ride prices based on date and time. The source explicitly requires peak/non-peak pricing for games/rides based on specific date/time.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Rule Name",
       "provenance": "pack Game_and_Ride_Module.pdf, page 46 §Rule Configuration"
      },
      {
       "kind": "selectField",
       "label": "Attraction / Group",
       "provenance": "pack Game_and_Ride_Module.pdf, page 46 §Rule Configuration"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Game_and_Ride_Module.pdf, page 46 §Rule Configuration"
      },
      {
       "kind": "selectField",
       "label": "Days of Week",
       "provenance": "pack Game_and_Ride_Module.pdf, page 46 §Rule Configuration"
      },
      {
       "kind": "selectField",
       "label": "Specific Date",
       "provenance": "pack Game_and_Ride_Module.pdf, page 46 §Rule Configuration"
      },
      {
       "kind": "selectField",
       "label": "Start Time",
       "provenance": "pack Game_and_Ride_Module.pdf, page 46 §Rule Configuration"
      },
      {
       "kind": "selectField",
       "label": "End Time",
       "provenance": "pack Game_and_Ride_Module.pdf, page 46 §Rule Configuration"
      },
      {
       "kind": "selectField",
       "label": "Peak Price",
       "provenance": "pack Game_and_Ride_Module.pdf, page 46 §Rule Configuration"
      },
      {
       "kind": "selectField",
       "label": "Non-Peak Price",
       "provenance": "pack Game_and_Ride_Module.pdf, page 46 §Rule Configuration"
      },
      {
       "kind": "textField",
       "label": "Effective From / To",
       "provenance": "pack Game_and_Ride_Module.pdf, page 46 §Rule Configuration"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The peak non-peak dynamic configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the peak non-peak dynamic untouched.",
   "emptyFirstRun": "No peak non-peak dynamic configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-437"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 46. 0 of 0 labels bound to a contract property; 10 of 23 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-438",
  "name": "Pricing Calendar & Exception Dates",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "5",
   "number": "5",
   "page": 47
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/pricing-calendar-exception-dates-bo-438",
   "component": "apps/venue-management-web/src/routes/games-rides/PricingCalendarExceptionDates.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-434"
   ],
   "exitTo": [
    "BO-434"
   ],
   "transitions": [
    {
     "to": "BO-434",
     "trigger": "Back to Game & Ride Pricing Command Center",
     "provenance": "structural — pack board 5 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Authorized users can see price schedules visually and configure date-specific exceptions without changing the underlying standard rule. explicitly prescribe the UI method.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Exception Configuration) and no display directory — it is settings, not a population",
  "purpose": "Provide a visual calendar for understanding and overriding time-based pricing.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Date",
       "provenance": "pack Game_and_Ride_Module.pdf, page 47 §Exception Configuration"
      },
      {
       "kind": "selectField",
       "label": "Attraction / Group",
       "provenance": "pack Game_and_Ride_Module.pdf, page 47 §Exception Configuration"
      },
      {
       "kind": "selectField",
       "label": "Pricing Type",
       "provenance": "pack Game_and_Ride_Module.pdf, page 47 §Exception Configuration"
      },
      {
       "kind": "selectField",
       "label": "Price",
       "provenance": "pack Game_and_Ride_Module.pdf, page 47 §Exception Configuration"
      },
      {
       "kind": "selectField",
       "label": "Start Time",
       "provenance": "pack Game_and_Ride_Module.pdf, page 47 §Exception Configuration"
      },
      {
       "kind": "selectField",
       "label": "End Time",
       "provenance": "pack Game_and_Ride_Module.pdf, page 47 §Exception Configuration"
      },
      {
       "kind": "selectField",
       "label": "Priority",
       "provenance": "pack Game_and_Ride_Module.pdf, page 47 §Exception Configuration"
      },
      {
       "kind": "selectField",
       "label": "Reason",
       "provenance": "pack Game_and_Ride_Module.pdf, page 47 §Exception Configuration"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The pricing calendar exception configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the pricing calendar exception untouched.",
   "emptyFirstRun": "No pricing calendar exception configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-438"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 47. 0 of 0 labels bound to a contract property; 8 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-439",
  "name": "Normal & VIP Pricing Configuration",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "5",
   "number": "6",
   "page": 47
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/normal-vip-pricing-configuration-bo-439",
   "component": "apps/venue-management-web/src/routes/games-rides/NormalVipPricingConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-434"
   ],
   "exitTo": [
    "BO-434"
   ],
   "transitions": [
    {
     "to": "BO-434",
     "trigger": "Back to Game & Ride Pricing Command Center",
     "provenance": "structural — pack board 5 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "The same game and reader can support Normal and VIP prices, and TICVAI automatically selects the appropriate price after identifying the guest's VIP entitlement.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configuration) and no display directory — it is settings, not a population",
  "purpose": "Configure different prices for Normal and VIP guests for the same game/ride and reader. The source explicitly requires one reader to show both Normal Price and VIP Price for a specific game, with VIP eligibility obtained through purchase of a VIP product.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Attraction: VR Racing",
       "provenance": "pack Game_and_Ride_Module.pdf, page 47 §Configuration"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The normal vip pricing configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the normal vip pricing untouched.",
   "emptyFirstRun": "No normal vip pricing configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-439"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 47. 0 of 0 labels bound to a contract property; 1 of 17 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-440",
  "name": "Retry Price Configuration",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "5",
   "number": "7",
   "page": 48
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/retry-price-configuration-bo-440",
   "component": "apps/venue-management-web/src/routes/games-rides/RetryPriceConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-434"
   ],
   "exitTo": [
    "BO-434"
   ],
   "transitions": [
    {
     "to": "BO-434",
     "trigger": "Back to Game & Ride Pricing Command Center",
     "provenance": "structural — pack board 5 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "An eligible retry transaction is recognized separately from a new gameplay transaction and charged at the configured reduced price.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Guest taps card) and no metric row",
  "purpose": "Configure a discounted repeat-play price for applicable skill games. Requirement 10.2.16 describes a skill game where, before the game ends, the guest is offered: “Do you want to continue?” A subsequent RFID tap should deduct a lower amount than the original price.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Game_and_Ride_Module.pdf, page 48 §Guest taps card"
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
       "label": "Every retry price",
       "columns": [
        "↓"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Game_and_Ride_Module.pdf, page 48 §Guest taps card"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected retry price",
       "bindsTo": null,
       "columns": [
        "↓"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Basketball Challenge”, “Runtime Flow”, “Game approaching completion”, “Reader displays”, “RETRY AED 10”, “AED 10 deducted”.",
       "provenance": "pack Game_and_Ride_Module.pdf, page 48 §Guest taps card"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The retry price list.",
   "error": "Could not load. Names which read failed and leaves the retry price untouched.",
   "emptyFirstRun": "No retry price yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the retry price are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "entryState": {
   "preloaded": [
    "↓"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-440"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 48. 0 of 1 labels bound to a contract property; 9 of 26 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-441",
  "name": "Price Priority & Conflict Rules",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "5",
   "number": "8",
   "page": 49
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/price-priority-conflict-rules-bo-441",
   "component": "apps/venue-management-web/src/routes/games-rides/PricePriorityConflictRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-434"
   ],
   "exitTo": [
    "BO-434"
   ],
   "transitions": [
    {
     "to": "BO-434",
     "trigger": "Back to Game & Ride Pricing Command Center",
     "provenance": "structural — pack board 5 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "When multiple pricing rules apply, TICVAI consistently calculates one deterministic final price. but does not state the resolution hierarchy.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Define which pricing rule wins when several valid prices apply simultaneously. This is required to make the source pricing models operational because Standard, Group, Peak, VIP and Retry prices can overlap.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 0 operations.** Unserved: Reorder | Validate | Test | Save. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Game_and_Ride_Module.pdf, page 49 §Actions"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 49"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 49"
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
       "label": "Reorder | Validate | Test | Save",
       "provenance": "pack Game_and_Ride_Module.pdf, page 49 §Actions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The price priority conflict list.",
   "error": "Could not load. Names which read failed and leaves the price priority conflict untouched.",
   "emptyFirstRun": "No price priority conflict yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the price priority conflict are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-441"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 49. 0 of 0 labels bound to a contract property; 1 of 23 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-442",
  "name": "Effective Pricing & Reader Price Preview",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "5",
   "number": "9",
   "page": 50
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/effective-pricing-reader-price-preview-bo-442",
   "component": "apps/venue-management-web/src/routes/games-rides/EffectivePricingReaderPricePreview.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-434"
   ],
   "exitTo": [
    "BO-434"
   ],
   "transitions": [
    {
     "to": "BO-434",
     "trigger": "Back to Game & Ride Pricing Command Center",
     "provenance": "structural — pack board 5 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Administrators can confirm the final calculated price and expected reader display before publishing configuration.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow an administrator to preview what price will actually be presented/applied for a selected game before publishing configuration.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 50"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 50"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The effective pricing reader list.",
   "error": "Could not load. Names which read failed and leaves the effective pricing reader untouched.",
   "emptyFirstRun": "No effective pricing reader yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the effective pricing reader are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-442"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 50. 0 of 0 labels bound to a contract property; 0 of 21 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-443",
  "name": "Pricing Audit, Approval & Publication",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "5",
   "number": "10",
   "page": 51
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/pricing-audit-approval-publication-bo-443",
   "component": "apps/venue-management-web/src/routes/games-rides/PricingAuditApprovalPublication.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-434"
   ],
   "exitTo": [
    "BO-434"
   ],
   "transitions": [
    {
     "to": "BO-434",
     "trigger": "Back to Game & Ride Pricing Command Center",
     "provenance": "structural — pack board 5 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Every pricing change is traceable and only approved/effective pricing is delivered to runtime services/readers. Board 5 — Exact Screen Mapping The visual Board 5 must contain these exact 10 screens in this order: # Screen 1 Game & Ride Pricing Command Center 2 Standard Game & Ride Price Configuration 3 Group Pricing Configuration 4 Peak / Non-Peak Dynamic Pricing 5 Pricing Calendar & Exception Dates 6 Normal & VIP Pricing Configuration 7 Retry Price Configuration 8 Price Priority & Conflict Rules 9 Effective Pricing & Reader Price Preview 10 Pricing Audit, Approval & Publication Critical desig",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Govern pricing changes and maintain a full historical record.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 3 actions on this screen and the screen declares 0 operations.** Unserved: Publish Now, Schedule Publication, Deactivate Rule. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Game_and_Ride_Module.pdf, page 51 §Allow"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 51"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 51"
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
       "label": "Publish Now",
       "provenance": "pack Game_and_Ride_Module.pdf, page 51 §Allow"
      },
      {
       "kind": "secondaryButton",
       "label": "Schedule Publication",
       "provenance": "pack Game_and_Ride_Module.pdf, page 51 §Allow"
      },
      {
       "kind": "destructiveButton",
       "label": "Deactivate Rule",
       "provenance": "pack Game_and_Ride_Module.pdf, page 51 §Allow"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmDeactivateRule",
    "component": "confirmDialog",
    "trigger": "Deactivate Rule",
    "body": "**Deactivate Rule on a pricing audit approval is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Game_and_Ride_Module.pdf, page 51 §Allow"
   }
  ],
  "states": {
   "loading": "The pricing audit approval list.",
   "error": "Could not load. Names which read failed and leaves the pricing audit approval untouched.",
   "emptyFirstRun": "No pricing audit approval yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the pricing audit approval are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-443"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 51. 0 of 0 labels bound to a contract property; 3 of 59 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
