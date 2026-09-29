# WS83 — Game and Ride board 6

**10 screens · 9 operations · 7 schemas · 5 permissions**

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
  `ORDER_CREATE, PRICE_VIEW, PRODUCT_CONFIGURE, PRODUCT_VIEW, WALLET_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-444` | Redemption Operations Dashboard | commandCentre | 1 | 0 | — |
| `BO-445` | Redemption Credit Rule Configuration | configEditor | 2 | 0 | — |
| `BO-446` | Ticket-Based Redemption / Ticket-Eater Integration | listDetail | 1 | 0 | — |
| `BO-447` | Ticketless Redemption Game Integration | listDetail | 1 | 0 | — |
| `BO-448` | Redemption Wallet & Balance View | listDetail | 1 | 0 | — |
| `BO-449` | Redemption Counter / Prize Checkout | listDetail | 4 | 2 | — |
| `BO-450` | Prize Catalogue & Credit Cost Configuration | listDetail | 2 | 0 | — |
| `BO-451` | Prize Inventory Integration | listDetail | 2 | 0 | — |
| `BO-452` | Direct-Pay / Crane & Prize Machine Configuration | listDetail | 1 | 0 | — |
| `BO-453` | Redemption Transaction Ledger, Reconciliation & Audit | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-446, BO-447, BO-448, BO-450, BO-451, BO-453 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-444",
  "name": "Redemption Operations Dashboard",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "6",
   "number": "1",
   "page": 53
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/redemption-operations-dashboard-bo-444",
   "component": "apps/venue-management-web/src/routes/games-rides/RedemptionOperationsDashboard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-445",
    "BO-446",
    "BO-447",
    "BO-448",
    "BO-449",
    "BO-450",
    "BO-451",
    "BO-452",
    "BO-453"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 6 wiring, 11 September 2026",
     "back": true
    },
    {
     "to": "BO-445",
     "trigger": "Redemption Credit Rule Configuration",
     "provenance": "structural — pack board 6 wiring, 11 September 2026"
    },
    {
     "to": "BO-446",
     "trigger": "Ticket-Based Redemption / Ticket-Eater Integration",
     "provenance": "structural — pack board 6 wiring, 11 September 2026"
    },
    {
     "to": "BO-447",
     "trigger": "Ticketless Redemption Game Integration",
     "provenance": "structural — pack board 6 wiring, 11 September 2026"
    },
    {
     "to": "BO-448",
     "trigger": "Redemption Wallet & Balance View",
     "provenance": "structural — pack board 6 wiring, 11 September 2026"
    },
    {
     "to": "BO-449",
     "trigger": "Redemption Counter / Prize Checkout",
     "provenance": "structural — pack board 6 wiring, 11 September 2026"
    },
    {
     "to": "BO-450",
     "trigger": "Prize Catalogue & Credit Cost Configuration",
     "provenance": "structural — pack board 6 wiring, 11 September 2026"
    },
    {
     "to": "BO-451",
     "trigger": "Prize Inventory Integration",
     "provenance": "structural — pack board 6 wiring, 11 September 2026"
    },
    {
     "to": "BO-452",
     "trigger": "Direct-Pay / Crane & Prize Machine Configuration",
     "provenance": "structural — pack board 6 wiring, 11 September 2026"
    },
    {
     "to": "BO-453",
     "trigger": "Redemption Transaction Ledger, Reconciliation & Audit",
     "provenance": "structural — pack board 6 wiring, 11 September 2026"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Operators can understand redemption-credit earning and prize-redemption activity from one central screen.",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide a central operational view of redemption activity across venues.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search redemption operations",
       "provenance": "pack Game_and_Ride_Module.pdf, page 53 §Filters"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Venue",
        "Zone",
        "Source Type",
        "Game",
        "Prize",
        "Date",
        "Transaction Status"
       ],
       "notes": "The pack filters this screen by venue, zone, source type, game, prize, date and 1 more — which are present is a decision the pack already made.",
       "provenance": "pack Game_and_Ride_Module.pdf, page 53 §Filters"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Redemption Credits Earned Today",
       "provenance": "pack Game_and_Ride_Module.pdf, page 53 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Redemption Credits Redeemed",
       "provenance": "pack Game_and_Ride_Module.pdf, page 53 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Active Redemption Wallets",
       "provenance": "pack Game_and_Ride_Module.pdf, page 53 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Prize Redemptions Today",
       "provenance": "pack Game_and_Ride_Module.pdf, page 53 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Ticket-Eater Transactions",
       "provenance": "pack Game_and_Ride_Module.pdf, page 53 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Ticketless Redemption Transactions",
       "provenance": "pack Game_and_Ride_Module.pdf, page 53 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Low-Stock Prize Items",
       "provenance": "pack Game_and_Ride_Module.pdf, page 53 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Failed Redemption Transactions",
       "provenance": "pack Game_and_Ride_Module.pdf, page 53 §KPI Cards"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The redemption operations list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the redemption operations untouched.",
   "emptyFirstRun": "No redemption operations yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the redemption operations are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listRedemption",
    "contract": "promotions",
    "purpose": "Redemption Analytics, Audit & AI Optimization",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-444",
   "workshopBoard": "wireframes/WS63 Game and Ride Board 6.dc.html#bo-444"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 53. 0 of 7 labels bound to a contract property; 15 of 26 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-445",
  "name": "Redemption Credit Rule Configuration",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "6",
   "number": "2",
   "page": 54
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/redemption-credit-rule-configuration-bo-445",
   "component": "apps/venue-management-web/src/routes/games-rides/RedemptionCreditRuleConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-444"
   ],
   "exitTo": [
    "BO-444"
   ],
   "transitions": [
    {
     "to": "BO-444",
     "trigger": "Back to Redemption Operations Dashboard",
     "provenance": "structural — pack board 6 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "from games but does not define the calculation method.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configuration) and no display directory — it is settings, not a population",
  "purpose": "Configure how games generate redemption credits.",
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
       "provenance": "pack Game_and_Ride_Module.pdf, page 54 §Configuration"
      },
      {
       "kind": "textField",
       "label": "Game / Game Group",
       "provenance": "pack Game_and_Ride_Module.pdf, page 54 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Game_and_Ride_Module.pdf, page 54 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Redemption Enabled",
       "provenance": "pack Game_and_Ride_Module.pdf, page 54 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Credit Calculation Method",
       "provenance": "pack Game_and_Ride_Module.pdf, page 54 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Effective Dates",
       "provenance": "pack Game_and_Ride_Module.pdf, page 54 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Status",
       "provenance": "pack Game_and_Ride_Module.pdf, page 54 §Configuration"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "External Game Value",
       "provenance": "pack Game_and_Ride_Module.pdf, page 54 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Machine-Reported Value",
       "provenance": "pack Game_and_Ride_Module.pdf, page 54 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The redemption credit rule configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the redemption credit rule untouched.",
   "emptyFirstRun": "No redemption credit rule configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "listPrizes",
    "contract": "games",
    "purpose": "Redemption operations",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "setRedemptionRules",
    "contract": "games",
    "purpose": "Save how games earn redemption credits (credit source per earn rule)",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration): serves the pack action(s) External Game Value, Machine-Reported Value",
    "invalidates": [
     "listPrizes"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-445",
   "workshopBoard": "wireframes/WS63 Game and Ride Board 6.dc.html#bo-445"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 54. 0 of 0 labels bound to a contract property; 9 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** External Game Value, Machine-Reported Value: `setRedemptionRules`.",
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
  "id": "BO-446",
  "name": "Ticket-Based Redemption / Ticket-Eater Integration",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "6",
   "number": "3",
   "page": 55
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/ticket-based-redemption-ticket-eater-integration-bo-446",
   "component": "apps/venue-management-web/src/routes/games-rides/TicketBasedRedemptionTicketEaterIntegration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-444"
   ],
   "exitTo": [
    "BO-444"
   ],
   "transitions": [
    {
     "to": "BO-444",
     "trigger": "Back to Redemption Operations Dashboard",
     "provenance": "structural — pack board 6 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Physical tickets accepted by an integrated ticket-eater are securely converted into digital redemption credits and posted to the correct guest wallet.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Customer identifies wallet/card) and no metric row",
  "purpose": "Configure the integration with ticket-eater machines that convert physical redemption tickets into digital wallet credits.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Game_and_Ride_Module.pdf, page 55 §Customer identifies wallet/card"
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
       "label": "Every ticket-based redemption ticket-eater",
       "columns": [
        "↓"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Game_and_Ride_Module.pdf, page 55 §Customer identifies wallet/card"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected ticket-based redemption ticket-eater",
       "bindsTo": null,
       "columns": [
        "↓"
       ],
       "notes": "The pack groups this record's detail under its own headings: “The source specifically requires”, “Physical tickets inserted”, “Ticket-Eater counts tickets”, “Machine sends count to TICVAI”, “Credits added to wallet”, “Transaction Result”.",
       "provenance": "pack Game_and_Ride_Module.pdf, page 55 §Customer identifies wallet/card"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The ticket-based redemption ticket-eater list.",
   "error": "Could not load. Names which read failed and leaves the ticket-based redemption ticket-eater untouched.",
   "emptyFirstRun": "No ticket-based redemption ticket-eater yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the ticket-based redemption ticket-eater are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setRedemptionRules",
    "contract": "games",
    "purpose": "How tickets are earned",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listPrizes"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "↓"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-446",
   "workshopBoard": "wireframes/WS63 Game and Ride Board 6.dc.html#bo-446"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 55. 0 of 1 labels bound to a contract property; 9 of 29 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-447",
  "name": "Ticketless Redemption Game Integration",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "6",
   "number": "4",
   "page": 56
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/ticketless-redemption-game-integration-bo-447",
   "component": "apps/venue-management-web/src/routes/games-rides/TicketlessRedemptionGameIntegration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-444"
   ],
   "exitTo": [
    "BO-444"
   ],
   "transitions": [
    {
     "to": "BO-444",
     "trigger": "Back to Redemption Operations Dashboard",
     "provenance": "structural — pack board 6 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Ticketless games can send redemption results to TICVAI and automatically update the guest's wallet.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Guest taps card) and no metric row",
  "purpose": "Configure games that automatically send redemption-credit results to TICVAI after gameplay. The source requires integration with redemption games to digitally load credits after the guest completes a game.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Game_and_Ride_Module.pdf, page 56 §Guest taps card"
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
       "label": "Every ticketless redemption game",
       "columns": [
        "↓"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Game_and_Ride_Module.pdf, page 56 §Guest taps card"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected ticketless redemption game",
       "bindsTo": null,
       "columns": [
        "↓"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Game Integration”, “Gameplay authorized”, “Game starts”, “Game completes”, “Game calculates win/score”, “Game sends redemption result”.",
       "provenance": "pack Game_and_Ride_Module.pdf, page 56 §Guest taps card"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The ticketless redemption game list.",
   "error": "Could not load. Names which read failed and leaves the ticketless redemption game untouched.",
   "emptyFirstRun": "No ticketless redemption game yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the ticketless redemption game are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setRedemptionRules",
    "contract": "games",
    "purpose": "Ticket-eater integration",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listPrizes"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "↓"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-447",
   "workshopBoard": "wireframes/WS63 Game and Ride Board 6.dc.html#bo-447"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 56. 0 of 1 labels bound to a contract property; 1 of 27 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-448",
  "name": "Redemption Wallet & Balance View",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "6",
   "number": "5",
   "page": 57
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/redemption-wallet-balance-view-bo-448",
   "component": "apps/venue-management-web/src/routes/games-rides/RedemptionWalletBalanceView.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-444"
   ],
   "exitTo": [
    "BO-444"
   ],
   "transitions": [
    {
     "to": "BO-444",
     "trigger": "Back to Redemption Operations Dashboard",
     "provenance": "structural — pack board 6 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "The customer's current redemption-credit balance can be retrieved consistently across supported channels.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow operators and systems to view the redemption-credit balance stored within a customer wallet. The source requires redemption credits stored in the wallet to be viewable from operator kiosks and self-service kiosks.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 57"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 57"
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
       "impliedBy": "getWallet",
       "notes": "One record, read-only."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The redemption wallet balance list.",
   "error": "Could not load. Names which read failed and leaves the redemption wallet balance untouched.",
   "emptyFirstRun": "No redemption wallet balance yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the redemption wallet balance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getWallet",
    "contract": "wallet",
    "purpose": "Redemption balance",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-448",
   "workshopBoard": "wireframes/WS63 Game and Ride Board 6.dc.html#bo-448"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 57. 0 of 0 labels bound to a contract property; 0 of 18 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-449",
  "name": "Redemption Counter / Prize Checkout",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "6",
   "number": "6",
   "page": 58
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/redemption-counter-prize-checkout-bo-449",
   "component": "apps/venue-management-web/src/routes/games-rides/RedemptionCounterPrizeCheckout.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-444"
   ],
   "exitTo": [
    "BO-444"
   ],
   "transitions": [
    {
     "to": "BO-444",
     "trigger": "Back to Redemption Operations Dashboard",
     "provenance": "structural — pack board 6 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "The redemption counter can deduct the correct credits and issue only valid, available prizes.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Scan / Tap Customer Card; Display) and no metric row",
  "purpose": "Provide the operator interface used when a customer exchanges redemption credits for prizes. The source explicitly requires redemption-credit usage at a redemption counter for prizes.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Game_and_Ride_Module.pdf, page 58 §Scan / Tap Customer Card"
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
       "label": "Every redemption counter prize",
       "columns": [
        "↓",
        "Redemption Balance: 2,450"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Game_and_Ride_Module.pdf, page 58 §Scan / Tap Customer Card"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected redemption counter prize",
       "bindsTo": null,
       "columns": [
        "↓",
        "Redemption Balance: 2,450"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Football 1 1,000”, “Before completing”, “REDEMPTION APPROVED”.",
       "provenance": "pack Game_and_Ride_Module.pdf, page 58 §Scan / Tap Customer Card"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Scan Prize Barcode",
       "operation": "lookupPrize",
       "provenance": "pack Game_and_Ride_Module.pdf, page 58 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Search Prize",
       "operation": "lookupPrize",
       "provenance": "pack Game_and_Ride_Module.pdf, page 58 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Change Quantity",
       "provenance": "pack Game_and_Ride_Module.pdf, page 58 §Actions"
      },
      {
       "kind": "destructiveButton",
       "label": "Remove Item",
       "provenance": "pack Game_and_Ride_Module.pdf, page 58 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Complete Redemption",
       "provenance": "pack Game_and_Ride_Module.pdf, page 58 §Actions"
      },
      {
       "kind": "destructiveButton",
       "label": "Cancel Transaction",
       "provenance": "pack Game_and_Ride_Module.pdf, page 58 §Actions"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmRemoveItem",
    "component": "confirmDialog",
    "trigger": "Remove Item",
    "body": "**Remove Item on a redemption counter prize is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Game_and_Ride_Module.pdf, page 58 §Actions"
   },
   {
    "id": "confirmCancelTransaction",
    "component": "confirmDialog",
    "trigger": "Cancel Transaction",
    "body": "**Cancel Transaction on a redemption counter prize is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Game_and_Ride_Module.pdf, page 58 §Actions"
   }
  ],
  "states": {
   "loading": "The redemption counter prize list.",
   "error": "Could not load. Names which read failed and leaves the redemption counter prize untouched.",
   "emptyFirstRun": "No redemption counter prize yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the redemption counter prize are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setRedemptionRules",
    "contract": "games",
    "purpose": "Ticketless redemption",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listPrizes"
    ]
   },
   {
    "operationId": "listPrizes",
    "contract": "games",
    "purpose": "Search the prize catalogue at this counter",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration): serves the pack action(s) Search Prize; Complete Redemption"
   },
   {
    "operationId": "redeemPrize",
    "contract": "games",
    "purpose": "Redeem the basket's prizes against the card's tickets",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration): serves the pack action(s) Search Prize; Complete Redemption",
    "invalidates": [
     "listPrizes"
    ]
   },
   {
    "operationId": "lookupPrize",
    "contract": "games",
    "purpose": "Look up prize",
    "trigger": "onScan"
   }
  ],
  "entryState": {
   "preloaded": [
    "↓",
    "Redemption Balance: 2,450"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-449",
   "workshopBoard": "wireframes/WS63 Game and Ride Board 6.dc.html#bo-449"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 58. 0 of 2 labels bound to a contract property; 8 of 21 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Change Quantity, Remove Item are choices sent by `redeemPrize` (basket lines (prizeId, quantity) held client-side until redeemPrize); Search Prize: `listPrizes`; Complete Redemption: `redeemPrize`; Cancel Transaction dropped (basket is client-side until redeemPrize; cancelling discards it, no server state); still owed by a contract change: `lookupPrize`.",
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
  "id": "BO-450",
  "name": "Prize Catalogue & Credit Cost Configuration",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "6",
   "number": "7",
   "page": 59
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/prize-catalogue-credit-cost-configuration-bo-450",
   "component": "apps/venue-management-web/src/routes/games-rides/PrizeCatalogueCreditCostConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-444"
   ],
   "exitTo": [
    "BO-444"
   ],
   "transitions": [
    {
     "to": "BO-444",
     "trigger": "Back to Redemption Operations Dashboard",
     "provenance": "structural — pack board 6 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Every redeemable prize has a controlled redemption-credit cost and active/inactive status.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure the prize catalogue and how many redemption credits each prize requires.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 59"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 59"
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
       "impliedBy": "redeemPrize",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listPrizes",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "redeemPrize"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The prize catalogue credit list.",
   "error": "Could not load. Names which read failed and leaves the prize catalogue credit untouched.",
   "emptyFirstRun": "No prize catalogue credit yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the prize catalogue credit are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "redeemPrize",
    "contract": "games",
    "purpose": "Hand over a prize",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listPrizes",
    "contract": "games",
    "purpose": "The prize catalogue",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-450",
   "workshopBoard": "wireframes/WS63 Game and Ride Board 6.dc.html#bo-450"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 59. 0 of 0 labels bound to a contract property; 0 of 19 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-451",
  "name": "Prize Inventory Integration",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "6",
   "number": "8",
   "page": 60
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/prize-inventory-integration-bo-451",
   "component": "apps/venue-management-web/src/routes/games-rides/PrizeInventoryIntegration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-444"
   ],
   "exitTo": [
    "BO-444"
   ],
   "transitions": [
    {
     "to": "BO-444",
     "trigger": "Back to Redemption Operations Dashboard",
     "provenance": "structural — pack board 6 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Prize stock is automatically adjusted when a prize is redeemed or dispensed.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Connect prize redemption directly with TICVAI inventory so redemption transactions reduce stock in real time. The source explicitly requires prizes at the redemption counter, skill games and direct-pay machines such as cranes to be integrated with the inventory system.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 60"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 60"
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
       "label": "Redemption Counter",
       "provenance": "pack Game_and_Ride_Module.pdf, page 60 §Support"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setPrizeCost"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The prize inventory integration list.",
   "error": "Could not load. Names which read failed and leaves the prize inventory integration untouched.",
   "emptyFirstRun": "No prize inventory integration yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the prize inventory integration are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setPrizeCost",
    "contract": "games",
    "purpose": "Ticket price and unit cost",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listPrizes"
    ]
   },
   {
    "operationId": "createPrize",
    "contract": "games",
    "purpose": "Add a prize",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-451",
   "workshopBoard": "wireframes/WS63 Game and Ride Board 6.dc.html#bo-451"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 60. 0 of 0 labels bound to a contract property; 1 of 19 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Redemption Counter dropped (navigation to the Redemption Counter screen (BO-449)).",
  "entryState": {
   "params": [
    {
     "name": "prizeId",
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
  "id": "BO-452",
  "name": "Direct-Pay / Crane & Prize Machine Configuration",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "6",
   "number": "9",
   "page": 61
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/direct-pay-crane-prize-machine-configuration-bo-452",
   "component": "apps/venue-management-web/src/routes/games-rides/DirectPayCranePrizeMachineConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-444"
   ],
   "exitTo": [
    "BO-444"
   ],
   "transitions": [
    {
     "to": "BO-444",
     "trigger": "Back to Redemption Operations Dashboard",
     "provenance": "structural — pack board 6 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Direct-pay prize machines can be associated with both wallet payment and prize inventory.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure prize machines such as cranes or other direct-pay devices that may consume wallet value and dispense inventory items. The matrix specifically references skill games and direct pay machines (e.g., cranes) as part of the inventory integration requirement.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 61"
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
       "label": "Inventory location",
       "operation": "getStockPositions",
       "notes": "Sends `?locationId=`; the machine's prize location.",
       "provenance": "contract inventory.yaml GET /stock"
      },
      {
       "kind": "selectField",
       "label": "Linked prize / SKU",
       "operation": "getStockPositions",
       "notes": "Sends `?itemId=`.",
       "provenance": "contract inventory.yaml GET /stock"
      },
      {
       "kind": "toggle",
       "label": "Include out-of-stock prizes",
       "operation": "getStockPositions",
       "notes": "Sends `?includeZero=true`; a machine whose prize is at zero must not complete redemption.",
       "provenance": "contract inventory.yaml GET /stock"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Prize machines and their stock",
       "bindsTo": "StockPosition",
       "columns": [
        "Machine ID",
        "Machine name",
        "Machine type",
        "StockPosition.itemName",
        "StockPosition.sku",
        "StockPosition.locationName",
        "StockPosition.available",
        "StockPosition.onHand",
        "StockPosition.allocated",
        "StockPosition.lastMovementAt",
        "Play price",
        "Machine status"
       ],
       "operation": "getStockPositions",
       "notes": "Only stock is bound. No operation lists machines, so the machine columns are pack labels.",
       "provenance": "pack Game_and_Ride_Module.pdf, page 61"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected machine profile",
       "bindsTo": "StockPosition",
       "columns": [
        "Machine ID",
        "Machine name",
        "Machine type",
        "Venue",
        "Zone",
        "Reader",
        "StockPosition.itemName",
        "StockPosition.sku",
        "StockPosition.locationName",
        "StockPosition.available",
        "StockPosition.unit",
        "StockPosition.value",
        "StockPosition.lastCountedAt",
        "Play price",
        "Machine status"
       ],
       "operation": "getStockPositions",
       "notes": "The pack's Machine Profile; current stock is `available`.",
       "provenance": "pack Game_and_Ride_Module.pdf, page 61"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The direct-pay crane prize list.",
   "error": "Could not load. Names which read failed and leaves the direct-pay crane prize untouched.",
   "emptyFirstRun": "No direct-pay crane prize yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the direct-pay crane prize are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getStockPositions",
    "contract": "inventory",
    "purpose": "Prize stock",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-452",
   "workshopBoard": "wireframes/WS63 Game and Ride Board 6.dc.html#bo-452"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 61. 0 of 0 labels bound to a contract property; 0 of 27 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Layout drafted 29 September (VM close-out)** from pack Game_and_Ride_Module.pdf p.61; contract inventory.yaml GET /stock. Pack labels with no schema field yet (shown as plain labels): Machine ID, Machine name, Machine type (Crane / Capsule / Direct Prize / Skill Prize), Venue, Zone, Reader, Play price, Machine status, A machine read (bound op is getStockPositions).",
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
  "id": "BO-453",
  "name": "Redemption Transaction Ledger, Reconciliation & Audit",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "6",
   "number": "10",
   "page": 62
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/redemption-transaction-ledger-reconciliation-audit-bo-453",
   "component": "apps/venue-management-web/src/routes/games-rides/RedemptionTransactionLedgerReconciliationAudit.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-444"
   ],
   "exitTo": [
    "BO-444"
   ],
   "transitions": [
    {
     "to": "BO-444",
     "trigger": "Back to Redemption Operations Dashboard",
     "provenance": "structural — pack board 6 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Every redemption-credit and prize transaction can be traced and reconciled against the originating device and resulting wallet/inventory movement. Board 6 — Exact Screen Mapping The Board 6 visual design must contain exactly these ten screens in this order: # Screen 1 Redemption Operations Dashboard 2 Redemption Credit Rule Configuration 3 Ticket-Based Redemption / Ticket-Eater Integration 4 Ticketless Redemption Game Integration 5 Redemption Wallet & Balance View 6 Redemption Counter / Prize Checkout 7 Prize Catalogue & Credit Cost Configuration 8 Prize Inventory Integration 9 Direct-Pay / Cr",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Compare; Redemption Counter / Prize Machine) and no metric row",
  "purpose": "Provide complete traceability of redemption credits earned, redeemed, adjusted and associated inventory movements.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Game_and_Ride_Module.pdf, page 62 §Compare"
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
       "label": "Every redemption transaction ledger",
       "columns": [
        "Game-reported credits",
        "TICVAI-posted credits",
        "Ticket-eater counts",
        "Wallet balance movements",
        "Prize transactions",
        "Inventory deductions",
        "versus"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Game_and_Ride_Module.pdf, page 62 §Compare"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected redemption transaction ledger",
       "bindsTo": null,
       "columns": [
        "Game-reported credits",
        "TICVAI-posted credits",
        "Ticket-eater counts",
        "Wallet balance movements",
        "Prize transactions",
        "Inventory deductions",
        "versus"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Transaction Ledger”, “Transaction Details”, “Exceptions”, “Page 62 of 105”, “Critical architecture for Board 6”, “Ticket-Eater”.",
       "provenance": "pack Game_and_Ride_Module.pdf, page 62 §Compare"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The redemption transaction ledger list.",
   "error": "Could not load. Names which read failed and leaves the redemption transaction ledger untouched.",
   "emptyFirstRun": "No redemption transaction ledger yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the redemption transaction ledger are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setPrizeCost",
    "contract": "games",
    "purpose": "Direct-pay price",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listPrizes"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "Game-reported credits",
    "TICVAI-posted credits",
    "Ticket-eater counts",
    "Wallet balance movements",
    "Prize transactions",
    "Inventory deductions"
   ],
   "params": [
    {
     "name": "prizeId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-453",
   "workshopBoard": "wireframes/WS63 Game and Ride Board 6.dc.html#bo-453"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 62. 0 of 7 labels bound to a contract property; 7 of 69 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "createPrize": {
  "method": "POST",
  "path": "/prizes",
  "contract": "games",
  "summary": "Add a prize",
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
  "requestBody": "Prize",
  "responds": "Prize"
 },
 "getStockPositions": {
  "method": "GET",
  "path": "/stock",
  "contract": "inventory",
  "summary": "Stock on hand by item and location",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "locationId",
    "in": "query",
    "required": null
   },
   {
    "name": "itemId",
    "in": "query",
    "required": null
   },
   {
    "name": "includeZero",
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
 "getWallet": {
  "method": "GET",
  "path": "/wallets/{subjectId}",
  "contract": "wallet",
  "summary": "Read a guest wallet",
  "permission": "WALLET_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "Wallet"
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
 "listRedemption": {
  "method": "GET",
  "path": "/redemption",
  "contract": "promotions",
  "summary": "Redemption Analytics, Audit & AI Optimization",
  "permission": "PRICE_VIEW",
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
    "name": "campaign",
    "in": "query",
    "required": false
   },
   {
    "name": "code",
    "in": "query",
    "required": false
   },
   {
    "name": "batch",
    "in": "query",
    "required": false
   },
   {
    "name": "product",
    "in": "query",
    "required": false
   },
   {
    "name": "venue",
    "in": "query",
    "required": false
   },
   {
    "name": "channel",
    "in": "query",
    "required": false
   },
   {
    "name": "customerSegment",
    "in": "query",
    "required": false
   },
   {
    "name": "partner",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "RedemptionAnalyticsAuditAiOptimizationView"
 },
 "lookupPrize": {
  "method": "GET",
  "path": "/prizes/lookup",
  "contract": "games",
  "summary": "Look up a prize by barcode or SKU",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "code",
    "in": "query",
    "required": true
   },
   {
    "name": "venueId",
    "in": "query",
    "required": true
   }
  ],
  "requestBody": null,
  "responds": "Prize"
 },
 "redeemPrize": {
  "method": "POST",
  "path": "/prize-redemptions",
  "contract": "games",
  "summary": "Redeem points for a prize",
  "permission": "ORDER_CREATE",
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
  "responds": "PrizeRedemption"
 },
 "setPrizeCost": {
  "method": "PUT",
  "path": "/prizes/{prizeId}/cost",
  "contract": "games",
  "summary": "What a prize costs in tickets, and what it costs the venue",
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
  "requestBody": "PrizeCost",
  "responds": "PrizeCost"
 },
 "setRedemptionRules": {
  "method": "PUT",
  "path": "/redemption-rules",
  "contract": "games",
  "summary": "How tickets are earned, held and spent",
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
  "requestBody": "RedemptionRules",
  "responds": "RedemptionRules"
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
 "PrizeCost": {
  "type": "object",
  "x-ticvai-persistence": "games.prize_cost",
  "description": "Boards 6.7 and 6.8. **Two numbers, one of them on the shelf.**",
  "properties": {
   "prizeId": {
    "type": "string",
    "format": "uuid"
   },
   "ticketPrice": {
    "type": "integer"
   },
   "unitCost": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "marginPercent": {
    "type": "number",
    "readOnly": true
   },
   "inventoryItemId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**Stock comes from `inventory`.** A prize catalogue with its own count is one that disagrees with the stockroom.\n"
   },
   "directPayPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "displayTier": {
    "type": "string",
    "nullable": true
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "PrizeRedemption": {
  "x-ticvai-persistence": "games.redemption + games.redemption_line",
  "type": "object",
  "required": [
   "id",
   "cardCode",
   "lines",
   "pointsUsed",
   "pointsRemaining",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string"
   },
   "redemptionNumber": {
    "type": "string"
   },
   "cardCode": {
    "type": "string"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "lines": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "prizeId": {
       "type": "string",
       "format": "uuid"
      },
      "name": {
       "type": "string"
      },
      "quantity": {
       "type": "integer"
      },
      "pointCost": {
       "type": "integer"
      }
     }
    }
   },
   "pointsUsed": {
    "type": "integer"
   },
   "pointsRemaining": {
    "type": "integer"
   },
   "stockMovementIds": {
    "type": "array",
    "description": "Movements raised in the inventory ledger.",
    "items": {
     "type": "string"
    }
   },
   "issuedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "RedemptionAnalyticsAuditAiOptimizationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Redemption Analytics, Audit & AI Optimization displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "codesGenerated": {
    "type": "string",
    "description": "Codes generated"
   },
   "codesDistributed": {
    "type": "string",
    "description": "Codes distributed"
   },
   "codesRedeemed": {
    "type": "string",
    "description": "Codes redeemed"
   },
   "redemptionRate": {
    "type": "number",
    "description": "Redemption rate"
   },
   "conversionRate": {
    "type": "number",
    "description": "Conversion rate"
   },
   "revenueGenerated": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue generated"
   },
   "discountGranted": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Discount granted"
   },
   "incrementalRevenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Incremental revenue"
   },
   "aovUplift": {
    "type": "number",
    "description": "AOV uplift"
   },
   "costPerRedemption": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Cost per redemption"
   },
   "marginImpact": {
    "type": "number",
    "description": "Margin impact"
   },
   "expiredUnusedCodes": {
    "type": "integer",
    "description": "Expired unused codes"
   },
   "user": {
    "type": "string",
    "description": "User"
   },
   "timestamp": {
    "type": "string",
    "format": "date-time",
    "description": "Timestamp"
   },
   "previousValue": {
    "type": "string",
    "description": "Previous value"
   },
   "newValue": {
    "type": "integer",
    "description": "New value"
   },
   "reason": {
    "type": "string",
    "description": "Reason"
   },
   "approvalReference": {
    "type": "string",
    "description": "Approval reference"
   },
   "auditEvent": {
    "type": "string",
    "enum": [
     "created",
     "modified",
     "assigned",
     "suspended",
     "reactivated",
     "cancelled"
    ],
    "description": "Code audit event."
   }
  }
 },
 "RedemptionRules": {
  "type": "object",
  "x-ticvai-persistence": "games.redemption_rules",
  "description": "Board 6. **Ticket-based and ticketless are one currency arriving two ways.**",
  "properties": {
   "ticketCreditTypeId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "earnRules": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "gameId": {
       "type": "string",
       "format": "uuid"
      },
      "ticketsPerPlay": {
       "type": "integer",
       "nullable": true
      },
      "ticketsPerScorePoint": {
       "type": "number",
       "nullable": true
      },
      "maximumPerPlay": {
       "type": "integer",
       "nullable": true
      }
     }
    }
   },
   "ticketEaterEnabled": {
    "type": "boolean",
    "default": false
   },
   "ticketlessEnabled": {
    "type": "boolean",
    "default": true
   },
   "ticketsExpire": {
    "type": "boolean",
    "default": false
   },
   "ticketValidityDays": {
    "type": "integer",
    "nullable": true
   },
   "counterApprovalAboveTickets": {
    "type": "integer",
    "nullable": true,
    "description": "**A prize above a threshold needs a second person.** The alternative is a counter that can hand out the top shelf.\n"
   },
   "scopePath": {
    "type": "string"
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
 }
}
```
