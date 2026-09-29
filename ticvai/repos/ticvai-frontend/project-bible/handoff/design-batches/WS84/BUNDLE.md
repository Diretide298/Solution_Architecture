# WS84 — Game and Ride board 7

**10 screens · 6 operations · 6 schemas · 4 permissions**

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
  `ACCESS_VALIDATE, PRODUCT_CONFIGURE, PRODUCT_VIEW, WALLET_OPERATE`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-454` | Card Lifecycle Command Center | commandCentre | 1 | 0 | — |
| `BO-455` | Card / Credential Profile | listDetail | 1 | 0 | — |
| `BO-456` | Card Expiry Rule Configuration | configEditor | 1 | 0 | — |
| `BO-457` | Last Recharge & Last Activity Tracking | listDetail | 1 | 0 | — |
| `BO-458` | Expiry Monitoring & Upcoming Expiration | listDetail | 1 | 0 | — |
| `BO-459` | Card Expiry Runtime Validation | listDetail | 1 | 0 | — |
| `BO-460` | Card Block, Suspend & Reactivation Control | listDetail | 1 | 1 | — |
| `BO-461` | Card Replacement & Wallet Relinking | listDetail | 2 | 0 | — |
| `BO-462` | Customer Balance & Credential Status View | listDetail | 1 | 0 | — |
| `BO-463` | Card Lifecycle Audit & History | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-455, BO-457, BO-458, BO-459, BO-461, BO-462, BO-463 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-454",
  "name": "Card Lifecycle Command Center",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "7",
   "number": "1",
   "page": 64
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/card-lifecycle-command-center-bo-454",
   "component": "apps/venue-management-web/src/routes/games-rides/CardLifecycleCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-455",
    "BO-456",
    "BO-457",
    "BO-458",
    "BO-459",
    "BO-460",
    "BO-461",
    "BO-462",
    "BO-463"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 7 wiring, 11 September 2026",
     "back": true
    },
    {
     "to": "BO-455",
     "trigger": "Card / Credential Profile",
     "provenance": "structural — pack board 7 wiring, 11 September 2026",
     "carries": [
      "cardCode"
     ]
    },
    {
     "to": "BO-456",
     "trigger": "Card Expiry Rule Configuration",
     "provenance": "structural — pack board 7 wiring, 11 September 2026"
    },
    {
     "to": "BO-457",
     "trigger": "Last Recharge & Last Activity Tracking",
     "provenance": "structural — pack board 7 wiring, 11 September 2026",
     "carries": [
      "cardCode"
     ]
    },
    {
     "to": "BO-458",
     "trigger": "Expiry Monitoring & Upcoming Expiration",
     "provenance": "structural — pack board 7 wiring, 11 September 2026"
    },
    {
     "to": "BO-459",
     "trigger": "Card Expiry Runtime Validation",
     "provenance": "structural — pack board 7 wiring, 11 September 2026"
    },
    {
     "to": "BO-460",
     "trigger": "Card Block, Suspend & Reactivation Control",
     "provenance": "structural — pack board 7 wiring, 11 September 2026"
    },
    {
     "to": "BO-461",
     "trigger": "Card Replacement & Wallet Relinking",
     "provenance": "structural — pack board 7 wiring, 11 September 2026"
    },
    {
     "to": "BO-462",
     "trigger": "Customer Balance & Credential Status View",
     "provenance": "structural — pack board 7 wiring, 11 September 2026",
     "carries": [
      "cardCode"
     ]
    },
    {
     "to": "BO-463",
     "trigger": "Card Lifecycle Audit & History",
     "provenance": "structural — pack board 7 wiring, 11 September 2026"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Authorized users can identify cards approaching expiry, expired cards, blocked cards and currently active cards from a single screen.",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Give operations and management a central view of all active game cards / RFID credentials and their lifecycle status.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search card lifecycle",
       "provenance": "pack Game_and_Ride_Module.pdf, page 64 §Filters"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Venue",
        "Status",
        "Expiry Period",
        "Last Activity",
        "Last Recharge",
        "Customer/Card"
       ],
       "notes": "The pack filters this screen by venue, status, expiry period, last activity, last recharge, customer/card — which are present is a decision the pack already made.",
       "provenance": "pack Game_and_Ride_Module.pdf, page 64 §Filters"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Total Active Cards",
       "provenance": "pack Game_and_Ride_Module.pdf, page 64 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Cards Used Today",
       "provenance": "pack Game_and_Ride_Module.pdf, page 64 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Cards Recharged Today",
       "provenance": "pack Game_and_Ride_Module.pdf, page 64 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Expiring in 30 Days",
       "provenance": "pack Game_and_Ride_Module.pdf, page 64 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Expired Cards",
       "provenance": "pack Game_and_Ride_Module.pdf, page 64 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Blocked Cards",
       "provenance": "pack Game_and_Ride_Module.pdf, page 64 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Dormant Cards",
       "provenance": "pack Game_and_Ride_Module.pdf, page 64 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Cards with Wallet Balance",
       "provenance": "pack Game_and_Ride_Module.pdf, page 64 §KPI Cards"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The card lifecycle list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the card lifecycle untouched.",
   "emptyFirstRun": "No card lifecycle yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the card lifecycle are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getGameCard",
    "contract": "games",
    "purpose": "Cards in circulation",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Total Active Cards",
    "Cards Used Today",
    "Cards Recharged Today",
    "Expiring in 30 Days",
    "Expired Cards",
    "Blocked Cards"
   ],
   "params": [
    {
     "name": "cardCode",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-454",
   "workshopBoard": "wireframes/WS64 Game and Ride Board 7.dc.html#bo-454"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 64. 0 of 6 labels bound to a contract property; 14 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-455",
  "name": "Card / Credential Profile",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "7",
   "number": "2",
   "page": 65
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/card-credential-profile-bo-455",
   "component": "apps/venue-management-web/src/routes/games-rides/CardCredentialProfile.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-454"
   ],
   "exitTo": [
    "BO-454"
   ],
   "transitions": [
    {
     "to": "BO-454",
     "trigger": "Back to Card Lifecycle Command Center",
     "provenance": "structural — pack board 7 wiring, 11 September 2026",
     "back": true,
     "carries": [
      "cardCode"
     ]
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Operators can view the complete lifecycle and wallet association of a credential without storing business logic inside the physical card.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Card Information) and no metric row",
  "purpose": "Provide the master backend profile for an individual physical or digital game credential.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Game_and_Ride_Module.pdf, page 65 §Card Information"
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
       "label": "Every card credential profile",
       "columns": [
        "Card ID",
        "RFID UID / Credential ID",
        "Card Number",
        "Customer",
        "Wallet ID",
        "Issue Date",
        "Issue Location",
        "Card Type",
        "Status"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Game_and_Ride_Module.pdf, page 65 §Card Information"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected card credential profile",
       "bindsTo": null,
       "columns": [
        "Card ID",
        "RFID UID / Credential ID",
        "Card Number",
        "Customer",
        "Wallet ID",
        "Issue Date",
        "Issue Location",
        "Card Type",
        "Status"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Linked Values”, “Page 65 of 105”.",
       "provenance": "pack Game_and_Ride_Module.pdf, page 65 §Card Information"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The card credential profile list.",
   "error": "Could not load. Names which read failed and leaves the card credential profile untouched.",
   "emptyFirstRun": "No card credential profile yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the card credential profile are still there. The pack's own statuses are Last Recharge — the state names which is selected.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getGameCard",
    "contract": "games",
    "purpose": "The card profile",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Card ID",
    "RFID UID / Credential ID",
    "Card Number",
    "Customer",
    "Wallet ID",
    "Issue Date"
   ],
   "params": [
    {
     "name": "cardCode",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-455",
   "workshopBoard": "wireframes/WS64 Game and Ride Board 7.dc.html#bo-455"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 65. 0 of 9 labels bound to a contract property; 18 of 27 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-456",
  "name": "Card Expiry Rule Configuration",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "7",
   "number": "3",
   "page": 66
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/card-expiry-rule-configuration-bo-456",
   "component": "apps/venue-management-web/src/routes/games-rides/CardExpiryRuleConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-454"
   ],
   "exitTo": [
    "BO-454"
   ],
   "transitions": [
    {
     "to": "BO-454",
     "trigger": "Back to Card Lifecycle Command Center",
     "provenance": "structural — pack board 7 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Rule Configuration; Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure the backend rule that determines when a card expires.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "textField",
       "label": "Rule Name: Standard Game Card Expiry",
       "provenance": "pack Game_and_Ride_Module.pdf, page 66 §Rule Configuration"
      },
      {
       "kind": "selectField",
       "label": "Last Recharge Date",
       "provenance": "pack Game_and_Ride_Module.pdf, page 66 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Last Activity Date",
       "provenance": "pack Game_and_Ride_Module.pdf, page 66 §Configure"
      },
      {
       "kind": "textField",
       "label": "Latest of Last Recharge or Last Activity",
       "provenance": "pack Game_and_Ride_Module.pdf, page 66 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The card expiry rule configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the card expiry rule untouched.",
   "emptyFirstRun": "No card expiry rule configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setGameCardExpiryRules",
    "contract": "games",
    "purpose": "When a card lapses",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getGameCard"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-456",
   "workshopBoard": "wireframes/WS64 Game and Ride Board 7.dc.html#bo-456"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 66. 0 of 0 labels bound to a contract property; 4 of 17 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-457",
  "name": "Last Recharge & Last Activity Tracking",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "7",
   "number": "4",
   "page": 67
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/last-recharge-last-activity-tracking-bo-457",
   "component": "apps/venue-management-web/src/routes/games-rides/LastRechargeLastActivityTracking.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-454"
   ],
   "exitTo": [
    "BO-454"
   ],
   "transitions": [
    {
     "to": "BO-454",
     "trigger": "Back to Card Lifecycle Command Center",
     "provenance": "structural — pack board 7 wiring, 11 September 2026",
     "back": true,
     "carries": [
      "cardCode"
     ]
    }
   ]
  },
  "density": "compact",
  "purposeNote": "The system records qualifying recharge/activity events and recalculates expiry automatically. but does not specify which activity types reset the period.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Maintain the two dates required for lifecycle calculation and show which events update them.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 67"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 67"
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
       "impliedBy": "getGameCard",
       "notes": "One record, read-only."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The last recharge last list.",
   "error": "Could not load. Names which read failed and leaves the last recharge last untouched.",
   "emptyFirstRun": "No last recharge last yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the last recharge last are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getGameCard",
    "contract": "games",
    "purpose": "Last recharge and activity",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-457",
   "workshopBoard": "wireframes/WS64 Game and Ride Board 7.dc.html#bo-457"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 67. 0 of 0 labels bound to a contract property; 0 of 23 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "cardCode",
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
  "id": "BO-458",
  "name": "Expiry Monitoring & Upcoming Expiration",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "7",
   "number": "5",
   "page": 68
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/expiry-monitoring-upcoming-expiration-bo-458",
   "component": "apps/venue-management-web/src/routes/games-rides/ExpiryMonitoringUpcomingExpiration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-454"
   ],
   "exitTo": [
    "BO-454"
   ],
   "transitions": [
    {
     "to": "BO-454",
     "trigger": "Back to Card Lifecycle Command Center",
     "provenance": "structural — pack board 7 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "The operation can identify cards approaching expiration and see the value associated with those credentials. without duplicating CRM configuration here.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Identify cards approaching expiry so operators can monitor liability and customer impact.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 68"
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
       "label": "Search expiry monitoring upcoming",
       "provenance": "pack Game_and_Ride_Module.pdf, page 68 §Filters"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Balance > 0",
        "Bonus > 0",
        "Redemption Credits > 0",
        "Venue",
        "Card Type",
        "Expiry Window"
       ],
       "notes": "The pack filters this screen by balance > 0, bonus > 0, redemption credits > 0, venue, card type, expiry window — which are present is a decision the pack already made.",
       "provenance": "pack Game_and_Ride_Module.pdf, page 68 §Filters"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "View Card | View Wallet | Export",
       "provenance": "pack Game_and_Ride_Module.pdf, page 68 §Actions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The expiry monitoring upcoming list.",
   "error": "Could not load. Names which read failed and leaves the expiry monitoring upcoming untouched.",
   "emptyFirstRun": "No expiry monitoring upcoming yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the expiry monitoring upcoming are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setGameCardExpiryRules",
    "contract": "games",
    "purpose": "Warnings before expiry",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getGameCard"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-458",
   "workshopBoard": "wireframes/WS64 Game and Ride Board 7.dc.html#bo-458"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 68. 0 of 6 labels bound to a contract property; 7 of 18 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** View Card | View Wallet | Export dropped (navigation (View Card / View Wallet) and a generic export already on the reporting screens).",
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
  "id": "BO-459",
  "name": "Card Expiry Runtime Validation",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "7",
   "number": "6",
   "page": 68
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/card-expiry-runtime-validation-bo-459",
   "component": "apps/venue-management-web/src/routes/games-rides/CardExpiryRuntimeValidation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-454"
   ],
   "exitTo": [
    "BO-454"
   ],
   "transitions": [
    {
     "to": "BO-454",
     "trigger": "Back to Card Lifecycle Command Center",
     "provenance": "structural — pack board 7 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Expired cards cannot initiate gameplay, while valid cards proceed automatically to the remaining transaction rules.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§CARD VALID; CARD EXPIRED) and no metric row",
  "purpose": "Show how TICVAI automatically handles a card tap when the credential is active or expired.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Game_and_Ride_Module.pdf, page 68 §CARD VALID"
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
       "label": "Every card expiry runtime",
       "columns": [
        "Expires: 08 Mar 2027"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Game_and_Ride_Module.pdf, page 68 §CARD VALID"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected card expiry runtime",
       "bindsTo": null,
       "columns": [
        "Expires: 08 Mar 2027"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Reader Tap”, “Reader sends Credential ID”, “Check Status”, “Check Calculated Expiry”, “Continue to”, “Reason Code”.",
       "provenance": "pack Game_and_Ride_Module.pdf, page 68 §CARD VALID"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The card expiry runtime list.",
   "error": "Could not load. Names which read failed and leaves the card expiry runtime untouched.",
   "emptyFirstRun": "No card expiry runtime yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the card expiry runtime are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "authoriseGameplay",
    "contract": "games",
    "purpose": "Expiry checked at the reader",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listGameplayTransactions",
     "getGameCard"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "Expires: 08 Mar 2027"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-459",
   "workshopBoard": "wireframes/WS64 Game and Ride Board 7.dc.html#bo-459"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 68. 0 of 1 labels bound to a contract property; 1 of 14 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-460",
  "name": "Card Block, Suspend & Reactivation Control",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "7",
   "number": "7",
   "page": 69
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/card-block-suspend-reactivation-control-bo-460",
   "component": "apps/venue-management-web/src/routes/games-rides/CardBlockSuspendReactivationControl.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-454"
   ],
   "exitTo": [
    "BO-454"
   ],
   "transitions": [
    {
     "to": "BO-454",
     "trigger": "Back to Card Lifecycle Command Center",
     "provenance": "structural — pack board 7 wiring, 11 September 2026",
     "back": true,
     "carries": [
      "cardCode"
     ]
    }
   ]
  },
  "density": "compact",
  "purposeNote": "A card can be blocked or reactivated independently from its underlying wallet balance. detailed in 10.2.21.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Blocked Card Tap) and no metric row",
  "purpose": "Allow authorized operators to disable a lost, suspicious or invalid card without affecting the underlying wallet record.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Game_and_Ride_Module.pdf, page 69 §Blocked Card Tap"
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
       "label": "Every card block suspend",
       "columns": [
        "→ Reader sends credential",
        "→ TICVAI recognizes blocked status",
        "→ Transaction rejected",
        "→ Wallet remains protected"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Game_and_Ride_Module.pdf, page 69 §Blocked Card Tap"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected card block suspend",
       "bindsTo": null,
       "columns": [
        "→ Reader sends credential",
        "→ TICVAI recognizes blocked status",
        "→ Transaction rejected",
        "→ Wallet remains protected"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Block Form”, “Require”.",
       "provenance": "pack Game_and_Ride_Module.pdf, page 69 §Blocked Card Tap"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Block",
       "provenance": "pack Game_and_Ride_Module.pdf, page 69 §Actions"
      },
      {
       "kind": "destructiveButton",
       "label": "Suspend",
       "provenance": "pack Game_and_Ride_Module.pdf, page 69 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Reactivate",
       "provenance": "pack Game_and_Ride_Module.pdf, page 69 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Replace Card",
       "provenance": "pack Game_and_Ride_Module.pdf, page 69 §Actions"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmSuspend",
    "component": "confirmDialog",
    "trigger": "Suspend",
    "body": "**Suspend on a card block suspend is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Game_and_Ride_Module.pdf, page 69 §Actions"
   }
  ],
  "states": {
   "loading": "The card block suspend list.",
   "error": "Could not load. Names which read failed and leaves the card block suspend untouched.",
   "emptyFirstRun": "No card block suspend yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the card block suspend are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setGameCardLifecycle",
    "contract": "games",
    "purpose": "Block, suspend or reactivate",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getGameCard"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "→ Reader sends credential",
    "→ TICVAI recognizes blocked status",
    "→ Transaction rejected",
    "→ Wallet remains protected"
   ],
   "params": [
    {
     "name": "cardId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-460",
   "workshopBoard": "wireframes/WS64 Game and Ride Board 7.dc.html#bo-460"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 69. 0 of 4 labels bound to a contract property; 8 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Block, Suspend, Reactivate, Replace Card are choices sent by `setGameCardLifecycle` (action enum block|suspend|reactivate|replace).",
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
  "id": "BO-461",
  "name": "Card Replacement & Wallet Relinking",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "7",
   "number": "8",
   "page": 70
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/card-replacement-wallet-relinking-bo-461",
   "component": "apps/venue-management-web/src/routes/games-rides/CardReplacementWalletRelinking.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-454"
   ],
   "exitTo": [
    "BO-454"
   ],
   "transitions": [
    {
     "to": "BO-454",
     "trigger": "Back to Card Lifecycle Command Center",
     "provenance": "structural — pack board 7 wiring, 11 September 2026",
     "back": true,
     "carries": [
      "cardCode"
     ]
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Replacing the physical card does not require creating a new wallet or losing customer balances and entitlements. explicitly stated in the source matrix.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Old Card) and no metric row",
  "purpose": "Allow a damaged, lost or replaced physical card to be substituted while retaining the customer's wallet and entitlements.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Game_and_Ride_Module.pdf, page 70 §Old Card"
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
       "label": "Every card replacement wallet",
       "columns": [
        "4321",
        "↓"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Game_and_Ride_Module.pdf, page 70 §Old Card"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected card replacement wallet",
       "bindsTo": null,
       "columns": [
        "4321",
        "↓"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Block Old Credential”, “Issue / Scan New Credential”, “Link Existing Wallet”, “Preserve”, “Page 70 of 105”.",
       "provenance": "pack Game_and_Ride_Module.pdf, page 70 §Old Card"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The card replacement wallet list.",
   "error": "Could not load. Names which read failed and leaves the card replacement wallet untouched.",
   "emptyFirstRun": "No card replacement wallet yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the card replacement wallet are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setGameCardLifecycle",
    "contract": "games",
    "purpose": "Replace and relink",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getGameCard"
    ]
   },
   {
    "operationId": "linkWalletCredential",
    "contract": "wallet",
    "purpose": "Bind the new credential",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "4321",
    "↓"
   ],
   "params": [
    {
     "name": "cardId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-461",
   "workshopBoard": "wireframes/WS64 Game and Ride Board 7.dc.html#bo-461"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 70. 0 of 2 labels bound to a contract property; 8 of 21 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-462",
  "name": "Customer Balance & Credential Status View",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "7",
   "number": "9",
   "page": 71
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/customer-balance-credential-status-view-bo-462",
   "component": "apps/venue-management-web/src/routes/games-rides/CustomerBalanceCredentialStatusView.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-454"
   ],
   "exitTo": [
    "BO-454"
   ],
   "transitions": [
    {
     "to": "BO-454",
     "trigger": "Back to Card Lifecycle Command Center",
     "provenance": "structural — pack board 7 wiring, 11 September 2026",
     "back": true,
     "carries": [
      "cardCode"
     ]
    }
   ]
  },
  "density": "compact",
  "purposeNote": "The same TICVAI backend balance data can be securely presented through different customer-facing devices. This does not duplicate Board 2 Screen 10. Board 2 configures the physical balance reader/device; this screen defines the card/wallet information service and backend data presented through that reader.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Card Information) and no metric row",
  "purpose": "Provide the backend configuration/view that supports balance-check readers, operator kiosks and self-service kiosks. The source requires a dedicated reader for checking customer balance and also requires wallet credits to be viewable at operator and self-service kiosks.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Game_and_Ride_Module.pdf, page 71 §Card Information"
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
       "label": "Every customer balance credential",
       "columns": [
        "Status: Active",
        "Card Expiry: 08 Mar 2027",
        "Bonus Expiry: 30 Sep 2026"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Game_and_Ride_Module.pdf, page 71 §Card Information"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected customer balance credential",
       "bindsTo": null,
       "columns": [
        "Status: Active",
        "Card Expiry: 08 Mar 2027",
        "Bonus Expiry: 30 Sep 2026"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Customer View”, “Redemption Credits”, “Free Games”, “Entitlements”.",
       "provenance": "pack Game_and_Ride_Module.pdf, page 71 §Card Information"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The customer balance credential list.",
   "error": "Could not load. Names which read failed and leaves the customer balance credential untouched.",
   "emptyFirstRun": "No customer balance credential yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the customer balance credential are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getGameCard",
    "contract": "games",
    "purpose": "Balance and credential status",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Status: Active",
    "Card Expiry: 08 Mar 2027",
    "Bonus Expiry: 30 Sep 2026"
   ],
   "params": [
    {
     "name": "cardCode",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-462",
   "workshopBoard": "wireframes/WS64 Game and Ride Board 7.dc.html#bo-462"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 71. 0 of 3 labels bound to a contract property; 6 of 17 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-463",
  "name": "Card Lifecycle Audit & History",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "7",
   "number": "10",
   "page": 72
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/card-lifecycle-audit-history-bo-463",
   "component": "apps/venue-management-web/src/routes/games-rides/CardLifecycleAuditHistory.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-454"
   ],
   "exitTo": [
    "BO-454"
   ],
   "transitions": [
    {
     "to": "BO-454",
     "trigger": "Back to Card Lifecycle Command Center",
     "provenance": "structural — pack board 7 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Every card lifecycle change can be traced to its originating event, device or authorized operator. Board 7 — Exact Screen Mapping The visual design for Board 7 must contain exactly these ten screens and in this order: # Screen 1 Card Lifecycle Command Center 2 Card / Credential Profile 3 Card Expiry Rule Configuration 4 Last Recharge & Last Activity Tracking 5 Expiry Monitoring & Upcoming Expiration 6 Card Expiry Runtime Validation 7 Card Block, Suspend & Reactivation Control 8 Card Replacement & Wallet Relinking 9 Customer Balance & Credential Status View 10 Card Lifecycle Audit & History",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Card Issued; Card Blocked) and no metric row",
  "purpose": "Maintain full traceability of card lifecycle changes.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Game_and_Ride_Module.pdf, page 72 §Card Issued"
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
       "label": "Every card lifecycle audit",
       "columns": [
        "05 Mar 2026",
        "18 Apr 2026"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Game_and_Ride_Module.pdf, page 72 §Card Issued"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected card lifecycle audit",
       "bindsTo": null,
       "columns": [
        "05 Mar 2026",
        "18 Apr 2026"
       ],
       "notes": "The pack groups this record's detail under its own headings: “AED 100 Recharge”, “Game Played”, “Expiry Recalculated”, “Events”, “Page 72 of 105”, “Important architecture for the design”.",
       "provenance": "pack Game_and_Ride_Module.pdf, page 72 §Card Issued"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The card lifecycle audit list.",
   "error": "Could not load. Names which read failed and leaves the card lifecycle audit untouched.",
   "emptyFirstRun": "No card lifecycle audit yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the card lifecycle audit are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listGameplayTransactions",
    "contract": "games",
    "purpose": "Card lifecycle history",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "05 Mar 2026",
    "18 Apr 2026"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-463",
   "workshopBoard": "wireframes/WS64 Game and Ride Board 7.dc.html#bo-463"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 72. 0 of 2 labels bound to a contract property; 12 of 65 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "authoriseGameplay": {
  "method": "POST",
  "path": "/gameplay-authorisations",
  "contract": "games",
  "summary": "Decide a tap, now",
  "permission": "ACCESS_VALIDATE",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "GameplayAuthorisationRequest",
  "responds": "GameplayAuthorisation"
 },
 "getGameCard": {
  "method": "GET",
  "path": "/game-cards/{cardCode}",
  "contract": "games",
  "summary": "Read a card's balances",
  "permission": null,
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "GameCard"
 },
 "linkWalletCredential": {
  "method": "POST",
  "path": "/wallet-credentials",
  "contract": "wallet",
  "summary": "Bind a wristband, card or device to a wallet",
  "permission": "WALLET_OPERATE",
  "offlineCapable": true,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "WalletCredential",
  "responds": "WalletCredential"
 },
 "listGameplayTransactions": {
  "method": "GET",
  "path": "/gameplay-transactions",
  "contract": "games",
  "summary": "Taps, decisions and what they cost",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "from",
    "in": "query",
    "required": null
   },
   {
    "name": "readerId",
    "in": "query",
    "required": null
   },
   {
    "name": "outcome",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "GameplayTransaction"
 },
 "setGameCardExpiryRules": {
  "method": "PUT",
  "path": "/game-card-expiry-rules",
  "contract": "games",
  "summary": "When a card lapses, and what warns the guest first",
  "permission": "PRODUCT_CONFIGURE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "GameCardExpiryRules",
  "responds": "GameCardExpiryRules"
 },
 "setGameCardLifecycle": {
  "method": "POST",
  "path": "/game-cards/{cardId}/lifecycle",
  "contract": "games",
  "summary": "Block, suspend, reactivate, replace or expire a card",
  "permission": "PRODUCT_CONFIGURE",
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
  "responds": "GameCard"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "GameCard": {
  "x-ticvai-persistence": "games.card",
  "type": "object",
  "required": [
   "cardCode",
   "venueId",
   "credits",
   "bonusCredits",
   "points",
   "status",
   "issuedAt"
  ],
  "properties": {
   "cardCode": {
    "type": "string",
    "description": "**A pre-printed card keeps the code printed on it. A generated code** (a digital card, or a card issued with no printed code) **is the venue prefix plus a sequence per venue** (decided 28 September, audit R152). Each till holds a reserved range of that sequence, so a card issued offline takes its code at once. Not gapless; only tax invoices are gapless, per legal entity.\n"
   },
   "kind": {
    "type": "string"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "credits": {
    "type": "integer",
    "description": "Bought with money. Buys plays."
   },
   "bonusCredits": {
    "type": "integer",
    "description": "From a promotion. Typically non-refundable and spent before paid credits.\n"
   },
   "points": {
    "type": "integer",
    "description": "Won by playing. Buys prizes. **Not interchangeable with credits** — a guest who wins should not simply be able to play more.\n"
   },
   "status": {
    "type": "string",
    "enum": [
     "active",
     "blocked",
     "expired",
     "transferred"
    ]
   },
   "blockedReason": {
    "type": "string",
    "nullable": true
   },
   "transferredToCardCode": {
    "type": "string",
    "nullable": true
   },
   "lastPlayedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "issuedAt": {
    "type": "string",
    "format": "date-time"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "GameCardExpiryRules": {
  "type": "object",
  "x-ticvai-persistence": "games.card_expiry_rules",
  "description": "Boards 7.3 to 7.6. **Measured from last activity, and the warning is part of the rule.**\n",
  "properties": {
   "basis": {
    "type": "string",
    "enum": [
     "fromIssue",
     "fromLastActivity",
     "fromLastRecharge"
    ],
    "default": "fromLastActivity"
   },
   "validityMonths": {
    "type": "integer"
   },
   "warnBeforeDays": {
    "type": "array",
    "items": {
     "type": "integer"
    },
    "description": "**Expiring a balance with no notice is what ends up on social media.**"
   },
   "warningChannels": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "extendOnRecharge": {
    "type": "boolean",
    "default": true
   },
   "onExpiry": {
    "type": "string",
    "enum": [
     "forfeit",
     "holdForClaim",
     "transferToBreakage"
    ],
    "default": "holdForClaim"
   },
   "holdForClaimDays": {
    "type": "integer",
    "nullable": true
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "GameplayAuthorisation": {
  "type": "object",
  "x-ticvai-persistence": "games.authorisation",
  "description": "Board 4.9. **The refusal reason is the product.**",
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "decision": {
    "type": "string",
    "enum": [
     "allow",
     "refuse"
    ]
   },
   "reason": {
    "type": "string",
    "nullable": true,
    "enum": [
     "ok",
     "cardNotFound",
     "cardExpired",
     "cardBlocked",
     "retapTooSoon",
     "heightRestriction",
     "ageRestriction",
     "insufficientFunds",
     "entitlementExhausted",
     "entitlementNotValidHere",
     "cooldownActive",
     "dailyCapReached",
     "readerNotConfigured",
     "gameUnavailable"
    ]
   },
   "guestMessage": {
    "type": "string",
    "nullable": true,
    "description": "***\"No plays left on your pass\"* rather than *\"Declined\"*.** One is a guest who understands; the other is a member of staff walking over.\n"
   },
   "chargedFrom": {
    "type": "string",
    "nullable": true
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "entitlementId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "remainingBalance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "remainingPlays": {
    "type": "integer",
    "nullable": true
   },
   "trace": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "check": {
       "type": "string"
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
   "decidedOffline": {
    "type": "boolean",
    "default": false
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "GameplayAuthorisationRequest": {
  "type": "object",
  "required": [
   "readerId"
  ],
  "properties": {
   "readerId": {
    "type": "string",
    "format": "uuid"
   },
   "cardId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "credentialIdentifier": {
    "type": "string",
    "nullable": true
   },
   "gameId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "at": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "guestHeightCm": {
    "type": "integer",
    "nullable": true
   },
   "offline": {
    "type": "boolean",
    "default": false
   }
  }
 },
 "GameplayTransaction": {
  "type": "object",
  "x-ticvai-persistence": "games.gameplay_transaction",
  "description": "Boards 8.2 and 8.5. **The refused ones are the valuable half.**",
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "readerId": {
    "type": "string",
    "format": "uuid"
   },
   "gameId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "cardId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "at": {
    "type": "string",
    "format": "date-time"
   },
   "outcome": {
    "type": "string",
    "enum": [
     "allowed",
     "refused",
     "reversed"
    ]
   },
   "reason": {
    "type": "string",
    "nullable": true
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "chargedFrom": {
    "type": "string",
    "nullable": true
   },
   "entitlementId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "ticketsEarned": {
    "type": "integer",
    "nullable": true
   },
   "decidedOffline": {
    "type": "boolean",
    "default": false
   },
   "syncedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "WalletCredential": {
  "type": "object",
  "x-ticvai-persistence": "wallet.credential",
  "description": "Boards 6.4 and 6.5. **A credential is not the wallet** — a lost wristband is relinked, not refunded.\n",
  "required": [
   "walletId",
   "kind",
   "identifier"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "walletId": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "type": "string",
    "enum": [
     "card",
     "wristband",
     "nfc",
     "rfid",
     "qr",
     "mobileApp",
     "digitalKey"
    ]
   },
   "identifier": {
    "type": "string"
   },
   "linkedAt": {
    "type": "string",
    "format": "date-time"
   },
   "unlinkedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "active",
     "lost",
     "replaced",
     "blocked",
     "expired"
    ]
   },
   "replacedByCredentialId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "scopePath": {
    "type": "string"
   }
  }
 }
}
```
