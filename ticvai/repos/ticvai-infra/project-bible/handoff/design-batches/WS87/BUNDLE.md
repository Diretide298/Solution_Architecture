# WS87 — Game and Ride board 10

**10 screens · 9 operations · 10 schemas · 4 permissions**

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
  `PRODUCT_VIEW, TENANT_CONFIGURE, WALLET_OPERATE, WALLET_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-484` | Self-Service Experience Command Center | commandCentre | 1 | 0 | — |
| `BO-485` | Self-Service Kiosk Profile & Channel Configuration | listDetail | 1 | 0 | — |
| `BO-486` | Customer Card / Wallet Identification | listDetail | 1 | 0 | — |
| `BO-487` | Customer Wallet & Balance Summary | listDetail | 3 | 0 | — |
| `BO-488` | Self-Service Wallet Top-Up | listDetail | 1 | 0 | — |
| `BO-489` | Bonus, Free Game & Benefit View | listDetail | 1 | 0 | — |
| `BO-490` | Game & Ride Eligibility / “What Can I Play?” | listDetail | 1 | 0 | — |
| `BO-491` | Redemption Balance & Prize Discovery | listDetail | 1 | 0 | — |
| `BO-492` | Customer Game & Wallet Transaction History | listDetail | 1 | 0 | — |
| `BO-493` | Self-Service UI Theme, Language & Journey Configuration | configEditor | 1 | 0 | — |

## Thin screens in this batch

**BO-485, BO-486, BO-487, BO-488, BO-490, BO-491, BO-492 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-484",
  "name": "Self-Service Experience Command Center",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "10",
   "number": "1",
   "page": 96
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/self-service-experience-command-center-bo-484",
   "component": "apps/venue-management-web/src/routes/games-rides/SelfServiceExperienceCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-485",
    "BO-486",
    "BO-487",
    "BO-488",
    "BO-489",
    "BO-490",
    "BO-491",
    "BO-492",
    "BO-493"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 10 wiring, 11 September 2026",
     "back": true
    },
    {
     "to": "BO-485",
     "trigger": "Self-Service Kiosk Profile & Channel Configuration",
     "provenance": "structural — pack board 10 wiring, 11 September 2026"
    },
    {
     "to": "BO-486",
     "trigger": "Customer Card / Wallet Identification",
     "provenance": "structural — pack board 10 wiring, 11 September 2026"
    },
    {
     "to": "BO-487",
     "trigger": "Customer Wallet & Balance Summary",
     "provenance": "structural — pack board 10 wiring, 11 September 2026"
    },
    {
     "to": "BO-488",
     "trigger": "Self-Service Wallet Top-Up",
     "provenance": "structural — pack board 10 wiring, 11 September 2026"
    },
    {
     "to": "BO-489",
     "trigger": "Bonus, Free Game & Benefit View",
     "provenance": "structural — pack board 10 wiring, 11 September 2026"
    },
    {
     "to": "BO-490",
     "trigger": "Game & Ride Eligibility / “What Can I Play?”",
     "provenance": "structural — pack board 10 wiring, 11 September 2026"
    },
    {
     "to": "BO-491",
     "trigger": "Redemption Balance & Prize Discovery",
     "provenance": "structural — pack board 10 wiring, 11 September 2026"
    },
    {
     "to": "BO-492",
     "trigger": "Customer Game & Wallet Transaction History",
     "provenance": "structural — pack board 10 wiring, 11 September 2026"
    },
    {
     "to": "BO-493",
     "trigger": "Self-Service UI Theme, Language & Journey Configuration",
     "provenance": "structural — pack board 10 wiring, 11 September 2026"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Administrators can monitor the status and usage of all self-service game-wallet channels centrally.",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide administrators with a centralized view of all customer-facing game wallet kiosks, balance stations, and enabled self-service channels.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search self-service experience",
       "provenance": "pack Game_and_Ride_Module.pdf, page 96 §Filters"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Client",
        "Venue",
        "Zone",
        "Device Type",
        "Status"
       ],
       "notes": "The pack filters this screen by client, venue, zone, device type, status — which are present is a decision the pack already made.",
       "provenance": "pack Game_and_Ride_Module.pdf, page 96 §Filters"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Total Self-Service Devices",
       "provenance": "pack Game_and_Ride_Module.pdf, page 96 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Online Devices",
       "provenance": "pack Game_and_Ride_Module.pdf, page 96 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Offline Devices",
       "provenance": "pack Game_and_Ride_Module.pdf, page 96 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Customer Sessions Today",
       "provenance": "pack Game_and_Ride_Module.pdf, page 96 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Balance Checks",
       "provenance": "pack Game_and_Ride_Module.pdf, page 96 §KPI Cards"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The self-service experience list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the self-service experience untouched.",
   "emptyFirstRun": "No self-service experience yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the self-service experience are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getGameEligibility",
    "contract": "games",
    "purpose": "Self-service overview",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Total Self-Service Devices",
    "Online Devices",
    "Offline Devices",
    "Customer Sessions Today",
    "Balance Checks"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-484",
   "workshopBoard": "wireframes/WS67 Game and Ride Board 10.dc.html#bo-484"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 96. 0 of 5 labels bound to a contract property; 10 of 21 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-485",
  "name": "Self-Service Kiosk Profile & Channel Configuration",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "10",
   "number": "2",
   "page": 97
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/self-service-kiosk-profile-channel-configuration-bo-485",
   "component": "apps/venue-management-web/src/routes/games-rides/SelfServiceKioskProfileChannelConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-484"
   ],
   "exitTo": [
    "BO-484"
   ],
   "transitions": [
    {
     "to": "BO-484",
     "trigger": "Back to Self-Service Experience Command Center",
     "provenance": "structural — pack board 10 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Administrators can determine which self-service functions are available on each kiosk/device.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Define the business role of each kiosk or customer-facing station.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 97"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 97"
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
       "impliedBy": "setGameKioskConfiguration",
       "label": "Save",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setGameKioskConfiguration"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The self-service kiosk profile list.",
   "error": "Could not load. Names which read failed and leaves the self-service kiosk profile untouched.",
   "emptyFirstRun": "No self-service kiosk profile yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the self-service kiosk profile are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setGameKioskConfiguration",
    "contract": "games",
    "purpose": "Kiosk profile and channel",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-485",
   "workshopBoard": "wireframes/WS67 Game and Ride Board 10.dc.html#bo-485"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 97. 0 of 0 labels bound to a contract property; 0 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-486",
  "name": "Customer Card / Wallet Identification",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "10",
   "number": "3",
   "page": 98
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/customer-card-wallet-identification-bo-486",
   "component": "apps/venue-management-web/src/routes/games-rides/CustomerCardWalletIdentification.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-484"
   ],
   "exitTo": [
    "BO-484"
   ],
   "transitions": [
    {
     "to": "BO-484",
     "trigger": "Back to Self-Service Experience Command Center",
     "provenance": "structural — pack board 10 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "A self-service session opens only after TICVAI successfully identifies and validates the customer's credential.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Validate Card Status; Card recognized) and no metric row",
  "purpose": "Configure the first customer step: identifying the customer's game card or digital wallet securely.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Game_and_Ride_Module.pdf, page 98 §Validate Card Status"
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
       "label": "Every customer card wallet",
       "columns": [
        "↓",
        "4321"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Game_and_Ride_Module.pdf, page 98 §Validate Card Status"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected customer card wallet",
       "bindsTo": null,
       "columns": [
        "↓",
        "4321"
       ],
       "notes": "The pack groups this record's detail under its own headings: “WELCOME”, “Identification Methods”, “Customer Tap”, “Invalid Results”.",
       "provenance": "pack Game_and_Ride_Module.pdf, page 98 §Validate Card Status"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The customer card wallet list.",
   "error": "Could not load. Names which read failed and leaves the customer card wallet untouched.",
   "emptyFirstRun": "No customer card wallet yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the customer card wallet are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getGameCard",
    "contract": "games",
    "purpose": "Identify the customer",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "↓",
    "4321"
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-486",
   "workshopBoard": "wireframes/WS67 Game and Ride Board 10.dc.html#bo-486"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 98. 0 of 2 labels bound to a contract property; 3 of 17 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-487",
  "name": "Customer Wallet & Balance Summary",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "10",
   "number": "4",
   "page": 99
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/customer-wallet-balance-summary-bo-487",
   "component": "apps/venue-management-web/src/routes/games-rides/CustomerWalletBalanceSummary.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-484"
   ],
   "exitTo": [
    "BO-484"
   ],
   "transitions": [
    {
     "to": "BO-484",
     "trigger": "Back to Self-Service Experience Command Center",
     "provenance": "structural — pack board 10 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Customers can distinguish paid credit, bonus, redemption credits, free games, and entitlements in a single view.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Card Information) and no metric row",
  "purpose": "Present all relevant wallet balances clearly to the customer. The source specifically requires customers' stored credits to be viewable through self-service kiosks.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Game_and_Ride_Module.pdf, page 99 §Card Information"
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
       "label": "Every customer wallet balance",
       "columns": [
        "Card Status",
        "Card Expiry",
        "Last Recharge"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Game_and_Ride_Module.pdf, page 99 §Card Information"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected customer wallet balance",
       "bindsTo": null,
       "columns": [
        "Card Status",
        "Card Expiry",
        "Last Recharge"
       ],
       "notes": "The pack groups this record's detail under its own headings: “AED 25”, “Redemption Credits”, “Free Games”, “Active Entitlements”.",
       "provenance": "pack Game_and_Ride_Module.pdf, page 99 §Card Information"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The customer wallet balance list.",
   "error": "Could not load. Names which read failed and leaves the customer wallet balance untouched.",
   "emptyFirstRun": "No customer wallet balance yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the customer wallet balance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getWallet",
    "contract": "wallet",
    "purpose": "Balance summary",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "getWalletExitBalance",
    "contract": "wallet",
    "purpose": "Balance due / refundable at exit",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "settleWalletAtExit",
    "contract": "wallet",
    "purpose": "Settle the wallet at exit",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Card Status",
    "Card Expiry",
    "Last Recharge"
   ],
   "params": [
    {
     "name": "subjectId",
     "from": "navigation"
    },
    {
     "name": "walletId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-487",
   "workshopBoard": "wireframes/WS67 Game and Ride Board 10.dc.html#bo-487"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 99. 0 of 3 labels bound to a contract property; 3 of 13 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-488",
  "name": "Self-Service Wallet Top-Up",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "10",
   "number": "5",
   "page": 99
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/self-service-wallet-top-up-bo-488",
   "component": "apps/venue-management-web/src/routes/games-rides/SelfServiceWalletTopUp.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-484"
   ],
   "exitTo": [
    "BO-484"
   ],
   "transitions": [
    {
     "to": "BO-484",
     "trigger": "Back to Self-Service Experience Command Center",
     "provenance": "structural — pack board 10 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "The self-service channel retrieves the active TICVAI top-up rules and applies the resulting wallet and bonus values correctly.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow customers to add value to their game wallet through an enabled kiosk/channel.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 99"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 99"
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
       "impliedBy": "topUpWallet",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "topUpWallet"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The self-service wallet top-up list.",
   "error": "Could not load. Names which read failed and leaves the self-service wallet top-up untouched.",
   "emptyFirstRun": "No self-service wallet top-up yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the self-service wallet top-up are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "topUpWallet",
    "contract": "wallet",
    "purpose": "Self-service top-up",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-488",
   "workshopBoard": "wireframes/WS67 Game and Ride Board 10.dc.html#bo-488"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 99. 0 of 0 labels bound to a contract property; 0 of 14 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "subjectId",
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
  "id": "BO-489",
  "name": "Bonus, Free Game & Benefit View",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "10",
   "number": "6",
   "page": 100
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/bonus-free-game-benefit-view-bo-489",
   "component": "apps/venue-management-web/src/routes/games-rides/BonusFreeGameBenefitView.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-484"
   ],
   "exitTo": [
    "BO-484"
   ],
   "transitions": [
    {
     "to": "BO-484",
     "trigger": "Back to Self-Service Experience Command Center",
     "provenance": "structural — pack board 10 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Customers can understand what promotional/free value they hold, where it can be used, and its remaining validity.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Help customers understand promotional value and benefits available in their wallet.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 100"
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
       "kind": "textField",
       "label": "Card number",
       "operation": "getGameEligibility",
       "notes": "Sends `?cardId=`.",
       "provenance": "contract games.yaml GET /game-eligibility"
      },
      {
       "kind": "searchField",
       "label": "Guest",
       "operation": "getGameEligibility",
       "notes": "Sends `?subjectId=`.",
       "provenance": "contract games.yaml GET /game-eligibility"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "operation": "getGameEligibility",
       "notes": "Sends `?venueId=`.",
       "provenance": "contract games.yaml GET /game-eligibility"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Bonus credit",
       "columns": [
        "Bonus credit"
       ],
       "notes": "The pack's Bonus Section (AED 25, valid until 30 Sep 2026); the eligibility read carries no wallet balance.",
       "provenance": "pack Game_and_Ride_Module.pdf, page 100"
      },
      {
       "kind": "metricTile",
       "label": "Free plays remaining",
       "bindsTo": "GameEligibility",
       "columns": [
        "GameEligibility.remainingPlays"
       ],
       "operation": "getGameEligibility",
       "notes": "Summed where `costKind` is freeWithEntitlement.",
       "provenance": "contract games.yaml GET /game-eligibility"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "What this card can play",
       "bindsTo": "GameEligibility",
       "columns": [
        "GameEligibility.name",
        "GameEligibility.costKind",
        "GameEligibility.price",
        "GameEligibility.playable",
        "GameEligibility.remainingPlays",
        "GameEligibility.entitlementId",
        "GameEligibility.blockedReason"
       ],
       "operation": "getGameEligibility",
       "notes": "`costKind` maps to the pack's Included / Free / Pay to Play / Not Eligible.",
       "provenance": "contract games.yaml GET /game-eligibility"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected game or benefit",
       "bindsTo": "GameEligibility",
       "columns": [
        "GameEligibility.gameId",
        "GameEligibility.name",
        "GameEligibility.playable",
        "GameEligibility.costKind",
        "GameEligibility.price",
        "GameEligibility.entitlementId",
        "GameEligibility.remainingPlays",
        "GameEligibility.blockedReason",
        "GameEligibility.ticketsTypicallyEarned",
        "Benefit name",
        "Valid until",
        "Can be used at",
        "Cannot be used at"
       ],
       "operation": "getGameEligibility",
       "notes": "The benefit name (e.g. Birthday Free Play), its validity and where bonus value is accepted are pack labels.",
       "provenance": "pack Game_and_Ride_Module.pdf, page 101"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The bonus free game list.",
   "error": "Could not load. Names which read failed and leaves the bonus free game untouched.",
   "emptyFirstRun": "No bonus free game yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the bonus free game are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getGameEligibility",
    "contract": "games",
    "purpose": "Bonus, free game and benefits",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-489",
   "workshopBoard": "wireframes/WS67 Game and Ride Board 10.dc.html#bo-489"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 100. 0 of 0 labels bound to a contract property; 0 of 13 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Layout drafted 29 September (VM close-out)** from pack Game_and_Ride_Module.pdf p.100; pack Game_and_Ride_Module.pdf p.101; contract games.yaml GET /game-eligibility. Pack labels with no schema field yet (shown as plain labels): Bonus credit, Bonus valid until, Where bonus can / cannot be used (games, rides, F&B, retail), Benefit name (e.g. Birthday Free Play), Entitlement validity (e.g. Valid Today).",
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
  "id": "BO-490",
  "name": "Game & Ride Eligibility / “What Can I Play?”",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "10",
   "number": "7",
   "page": 101
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/game-ride-eligibility-what-can-i-play-bo-490",
   "component": "apps/venue-management-web/src/routes/games-rides/GameRideEligibilityWhatCanIPlay.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-484"
   ],
   "exitTo": [
    "BO-484"
   ],
   "transitions": [
    {
     "to": "BO-484",
     "trigger": "Back to Self-Service Experience Command Center",
     "provenance": "structural — pack board 10 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Customers can identify available gameplay options using the real-time rules configured in TICVAI.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow guests to see which games and rides they can currently access based on their wallet, packages, free plays and entitlements.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 101"
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
       "label": "Search game ride eligibility",
       "provenance": "pack Game_and_Ride_Module.pdf, page 101 §Filters"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Rides",
        "Video Games",
        "Skill Games",
        "Free for Me",
        "Included in My Package"
       ],
       "notes": "The pack filters this screen by rides, video games, skill games, free for me, included in my package — which are present is a decision the pack already made.",
       "provenance": "pack Game_and_Ride_Module.pdf, page 101 §Filters"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The game ride eligibility list.",
   "error": "Could not load. Names which read failed and leaves the game ride eligibility untouched.",
   "emptyFirstRun": "No game ride eligibility yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the game ride eligibility are still there. The pack's own statuses are Included — the state names which is selected.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getGameEligibility",
    "contract": "games",
    "purpose": "What can I play",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-490",
   "workshopBoard": "wireframes/WS67 Game and Ride Board 10.dc.html#bo-490"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 101. 0 of 5 labels bound to a contract property; 9 of 21 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-491",
  "name": "Redemption Balance & Prize Discovery",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "10",
   "number": "8",
   "page": 102
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/redemption-balance-prize-discovery-bo-491",
   "component": "apps/venue-management-web/src/routes/games-rides/RedemptionBalancePrizeDiscovery.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-484"
   ],
   "exitTo": [
    "BO-484"
   ],
   "transitions": [
    {
     "to": "BO-484",
     "trigger": "Back to Self-Service Experience Command Center",
     "provenance": "structural — pack board 10 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Customers can see their redemption balance and identify prizes that are currently available within that balance.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow customers to check redemption credits and browse prizes they can afford before visiting the redemption counter.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 102"
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
       "label": "Search redemption balance prize",
       "provenance": "pack Game_and_Ride_Module.pdf, page 102 §Filters"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Available Now",
        "Prize Category",
        "Credit Range",
        "Venue"
       ],
       "notes": "The pack filters this screen by available now, prize category, credit range, venue — which are present is a decision the pack already made.",
       "provenance": "pack Game_and_Ride_Module.pdf, page 102 §Filters"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The redemption balance prize list.",
   "error": "Could not load. Names which read failed and leaves the redemption balance prize untouched.",
   "emptyFirstRun": "No redemption balance prize yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the redemption balance prize are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPrizes",
    "contract": "games",
    "purpose": "Prize discovery",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-491",
   "workshopBoard": "wireframes/WS67 Game and Ride Board 10.dc.html#bo-491"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 102. 0 of 4 labels bound to a contract property; 4 of 17 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-492",
  "name": "Customer Game & Wallet Transaction History",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "10",
   "number": "9",
   "page": 102
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/customer-game-wallet-transaction-history-bo-492",
   "component": "apps/venue-management-web/src/routes/games-rides/CustomerGameWalletTransactionHistory.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-484"
   ],
   "exitTo": [
    "BO-484"
   ],
   "transitions": [
    {
     "to": "BO-484",
     "trigger": "Back to Self-Service Experience Command Center",
     "provenance": "structural — pack board 10 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Customers can review recent wallet/game activity without requiring back-office access.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow the customer to review recent activity associated with the card/wallet.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 102"
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
       "label": "Search customer game wallet",
       "provenance": "pack Game_and_Ride_Module.pdf, page 102 §Filters"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Games/Rides",
        "Top-Ups",
        "Bonus",
        "Redemption",
        "Free Play"
       ],
       "notes": "The pack filters this screen by games/rides, top-ups, bonus, redemption, free play — which are present is a decision the pack already made.",
       "provenance": "pack Game_and_Ride_Module.pdf, page 102 §Filters"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The customer game wallet list.",
   "error": "Could not load. Names which read failed and leaves the customer game wallet untouched.",
   "emptyFirstRun": "No customer game wallet yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the customer game wallet are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listGameplayTransactions",
    "contract": "games",
    "purpose": "Transaction history",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-492",
   "workshopBoard": "wireframes/WS67 Game and Ride Board 10.dc.html#bo-492"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 102. 0 of 5 labels bound to a contract property; 5 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-493",
  "name": "Self-Service UI Theme, Language & Journey Configuration",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "10",
   "number": "10",
   "page": 103
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/self-service-ui-theme-language-journey-configuration-bo-493",
   "component": "apps/venue-management-web/src/routes/games-rides/SelfServiceUiThemeLanguageJourneyConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-484"
   ],
   "exitTo": [
    "BO-484"
   ],
   "transitions": [
    {
     "to": "BO-484",
     "trigger": "Back to Self-Service Experience Command Center",
     "provenance": "structural — pack board 10 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "The customer-facing experience can be branded and configured centrally while continuing to consume the same TICVAI backend wallet and gameplay services. Board 10 — Exact Screen Mapping # Screen 1 Self-Service Experience Command Center 2 Self-Service Kiosk Profile & Channel Configuration 3 Customer Card / Wallet Identification 4 Customer Wallet & Balance Summary 5 Self-Service Wallet Top-Up 6 Bonus, Free Game & Benefit View 7 Game & Ride Eligibility / “What Can I Play?” 8 Redemption Balance & Prize Discovery",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Session Configuration) and no display directory — it is settings, not a population",
  "purpose": "Allow TICVAI administrators to configure the customer-facing kiosk experience without changing business logic.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Session Timeout",
       "provenance": "pack Game_and_Ride_Module.pdf, page 103 §Session Configuration"
      },
      {
       "kind": "selectField",
       "label": "Auto Logout",
       "provenance": "pack Game_and_Ride_Module.pdf, page 103 §Session Configuration"
      },
      {
       "kind": "selectField",
       "label": "Confirmation Timeout",
       "provenance": "pack Game_and_Ride_Module.pdf, page 103 §Session Configuration"
      },
      {
       "kind": "textField",
       "label": "Privacy Reset After Session",
       "provenance": "pack Game_and_Ride_Module.pdf, page 103 §Session Configuration"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The self-service theme language configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the self-service theme language untouched.",
   "emptyFirstRun": "No self-service theme language configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setGameKioskConfiguration",
    "contract": "games",
    "purpose": "Theme, language and journey",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-493",
   "workshopBoard": "wireframes/WS67 Game and Ride Board 10.dc.html#bo-493"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 103. 0 of 0 labels bound to a contract property; 4 of 59 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "getGameEligibility": {
  "method": "GET",
  "path": "/game-eligibility",
  "contract": "games",
  "summary": "What this guest can play right now, and what it would cost",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "cardId",
    "in": "query",
    "required": null
   },
   {
    "name": "subjectId",
    "in": "query",
    "required": null
   },
   {
    "name": "venueId",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "GameEligibility"
 },
 "getWallet": {
  "method": "GET",
  "path": "/wallets/{subjectId}",
  "contract": "wallet",
  "summary": "Read a guest wallet",
  "permission": "WALLET_VIEW",
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
  "responds": "Wallet"
 },
 "getWalletExitBalance": {
  "method": "GET",
  "path": "/wallets/{walletId}/exit-balance",
  "contract": "wallet",
  "summary": "What the holder owes or is owed on leaving",
  "permission": "WALLET_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "WalletExitBalance"
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
 "listPrizes": {
  "method": "GET",
  "path": "/prizes",
  "contract": "games",
  "summary": "The prize catalogue",
  "permission": "PRODUCT_VIEW",
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
    "name": "maxPoints",
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
 "setGameKioskConfiguration": {
  "method": "PUT",
  "path": "/game-kiosk-config",
  "contract": "games",
  "summary": "The self-service journey, its theme and its languages",
  "permission": "TENANT_CONFIGURE",
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
  "requestBody": "GameKioskConfig",
  "responds": "GameKioskConfig"
 },
 "settleWalletAtExit": {
  "method": "POST",
  "path": "/wallets/{walletId}/exit-settlement",
  "contract": "wallet",
  "summary": "Settle a short balance, or refund a credit, when the holder leaves",
  "permission": "WALLET_OPERATE",
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
  "responds": "WalletExitSettlement"
 },
 "topUpWallet": {
  "method": "POST",
  "path": "/wallets/{subjectId}/top-ups",
  "contract": "wallet",
  "summary": "Add value to a wallet",
  "permission": "WALLET_OPERATE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "workstation",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Wallet"
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
 "GameEligibility": {
  "type": "object",
  "description": "Board 10.7 — *\"What Can I Play?\"*, and every fact in it lives somewhere different.",
  "properties": {
   "gameId": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string"
   },
   "playable": {
    "type": "boolean"
   },
   "costKind": {
    "type": "string",
    "enum": [
     "freeWithEntitlement",
     "credit",
     "directPay",
     "notPlayable"
    ]
   },
   "price": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "entitlementId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "remainingPlays": {
    "type": "integer",
    "nullable": true
   },
   "blockedReason": {
    "type": "string",
    "nullable": true
   },
   "ticketsTypicallyEarned": {
    "type": "integer",
    "nullable": true
   }
  }
 },
 "GameKioskConfig": {
  "type": "object",
  "x-ticvai-persistence": "games.kiosk_config",
  "description": "Boards 10.2 and 10.10. **Used by a child holding a wristband.**",
  "properties": {
   "kioskDeviceId": {
    "type": "string",
    "format": "uuid"
   },
   "steps": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "identify",
      "balance",
      "topUp",
      "entitlements",
      "whatCanIPlay",
      "redemption",
      "history"
     ]
    }
   },
   "languages": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "themeCode": {
    "type": "string",
    "nullable": true
   },
   "idleTimeoutSeconds": {
    "type": "integer",
    "default": 30
   },
   "requiresPinForTopUp": {
    "type": "boolean",
    "default": false
   },
   "scopePath": {
    "type": "string"
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
 "Money": {
  "type": "object",
  "x-ticvai-persistence-kind": "valueObject",
  "x-ticvai-persistence-column": "numeric(18,4)",
  "description": "**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n",
  "required": [
   "amount",
   "currency",
   "scale"
  ],
  "properties": {
   "amount": {
    "type": "string",
    "description": "Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n",
    "pattern": "^-?\\d+(\\.\\d{1,4})?$"
   },
   "currency": {
    "type": "string",
    "description": "**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n",
    "pattern": "^[A-Z]{3}$"
   },
   "scale": {
    "type": "integer",
    "description": "Resolved from the region alongside `currency`.",
    "minimum": 0,
    "maximum": 4
   }
  }
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
 "Prize": {
  "x-ticvai-persistence": "games.prize",
  "type": "object",
  "required": [
   "id",
   "name",
   "venueId",
   "pointCost",
   "onHand"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "description": {
    "type": "string",
    "nullable": true
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "merchandiseId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Links to retail. Redemption depletes stock through the inventory ledger — a prize wall running out is a stock problem and should look like one.\n"
   },
   "pointCost": {
    "type": "integer",
    "minimum": 1
   },
   "onHand": {
    "type": "integer"
   },
   "isAvailable": {
    "type": "boolean"
   },
   "tier": {
    "type": "string",
    "nullable": true,
    "description": "Small, medium, large, jackpot. Drives prize-wall layout."
   },
   "imageAssetRef": {
    "type": "string",
    "nullable": true
   },
   "barcode": {
    "type": "string",
    "maxLength": 64,
    "nullable": true,
    "description": "The prize's own barcode, read by `lookupPrize` before the linked retail item's barcode or SKU. Unique within the venue (VM close-out, 29 September)."
   },
   "isActive": {
    "type": "boolean"
   }
  }
 },
 "Wallet": {
  "x-ticvai-persistence": "wallet.wallet + wallet.credit_lot",
  "type": "object",
  "required": [
   "subjectId",
   "balance",
   "currency",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "balance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "credits": {
    "type": "array",
    "description": "4.3.5 and 4.3.19. **One balance and one bonus balance with one expiry could not express what the requirement asks for** — cash, bonus and redemption credit, each with its own expiry.\n**The expiries are the reason this is a list.** Cash a guest paid for should outlive a promotional credit they were given, and a single `expiresAt` either expires the money they paid or never expires the promotion.\n**Consumed first-expiry-first-out across all three** (4.3.19), which is also the order that is fairest to the guest — spend what is about to die before what is not.\n**One entry per `active` lot in `wallet.credit_lot`** for this wallet: `amount` is the lot's `remaining_amount`, `expiresAt` its `expires_at`, `sourceRef` its `source_reference`. `kind` and `isRefundable` are not stored on the lot; they come from the lot's credit type (`listCreditLots` returns the lots themselves).\n",
    "items": {
     "type": "object",
     "required": [
      "kind",
      "amount"
     ],
     "properties": {
      "kind": {
       "type": "string",
       "enum": [
        "cash",
        "bonus",
        "redemption",
        "refund",
        "goodwill"
       ],
       "description": "**`cash` is money the guest paid and the others are not.** That distinction decides what is refundable, what expires, and what shows as a liability.\n",
       "x-ticvai-persisted": false
      },
      "amount": {
       "x-ticvai-column": "remaining_amount",
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "expiresAt": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      },
      "sourceRef": {
       "type": "string",
       "nullable": true,
       "x-ticvai-column": "source_reference"
      },
      "isRefundable": {
       "type": "boolean",
       "default": false,
       "x-ticvai-persisted": false,
       "description": "**True only for `cash`.** A guest cannot cash out a promotional credit, and a wallet that lets them has given away the promotion twice.\n"
      }
     }
    }
   },
   "bonusBalance": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Promotional value. Typically non-refundable and spent first."
   },
   "currency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$"
   },
   "status": {
    "type": "string",
    "enum": [
     "active",
     "suspended",
     "closed"
    ]
   },
   "homeCellName": {
    "type": "string",
    "nullable": true,
    "description": "Where the authoritative balance lives. Present when the guest is linked across cells.\n"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "lastActivityAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "WalletExitBalance": {
  "type": "object",
  "x-ticvai-persistence": "none — computed from wallet.wallet, wallet.credit_lot and held offline transactions",
  "required": [
   "walletId",
   "balance",
   "amountDue",
   "refundable"
  ],
  "properties": {
   "walletId": {
    "type": "string",
    "format": "uuid"
   },
   "balance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "pendingOfflineAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "amountDue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "refundable": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "nonRefundableCredit": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "waiveAllowedUpTo": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "asAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "WalletExitSettlement": {
  "type": "object",
  "x-ticvai-persistence": "wallet.exit_settlement",
  "description": "4.3.4. One settlement of a wallet at exit.",
  "required": [
   "id",
   "walletId",
   "action",
   "amount",
   "settledAt"
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
   "action": {
    "type": "string",
    "enum": [
     "collect",
     "refund",
     "waive"
    ]
   },
   "method": {
    "type": "string",
    "nullable": true,
    "enum": [
     "card",
     "cash",
     "storedCard",
     "originalPayment"
    ]
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "balanceBefore": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "paymentId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "refundId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "walletTransactionId": {
    "type": "string",
    "nullable": true
   },
   "reason": {
    "type": "string",
    "nullable": true
   },
   "settledByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "settledAt": {
    "type": "string",
    "format": "date-time"
   },
   "scopePath": {
    "type": "string",
    "readOnly": true
   }
  }
 }
}
```
