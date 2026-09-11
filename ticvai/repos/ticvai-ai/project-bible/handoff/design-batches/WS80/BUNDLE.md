# WS80 — Game and Ride board 3

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
| `BO-414` | Wallet & Credit Management Dashboard | commandCentre | 0 | 0 | — |
| `BO-415` | Wallet & Credit Type Configuration | configEditor | 0 | 0 | — |
| `BO-416` | Wallet Account & Balance View | listDetail | 0 | 0 | — |
| `BO-417` | Top-Up Configuration | listDetail | 0 | 0 | — |
| `BO-418` | Top-Up Bonus Rule Configuration | listDetail | 0 | 0 | — |
| `BO-419` | Bonus Usage Restrictions | listDetail | 0 | 0 | — |
| `BO-420` | Bonus Validity & Expiry Configuration | listDetail | 0 | 0 | — |
| `BO-421` | Free Game & Ride Credit Management | configEditor | 0 | 0 | — |
| `BO-422` | Refund, Adjustment & Manual Bonus Control | listDetail | 0 | 0 | — |
| `BO-423` | Wallet Credit Transaction Ledger & Audit | listDetail | 0 | 0 | — |

## Thin screens in this batch

**BO-417, BO-418, BO-419, BO-420, BO-422, BO-423 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-414",
  "name": "Wallet & Credit Management Dashboard",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "3",
   "number": "1",
   "page": 23
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/wallet-credit-management-dashboard-bo-414",
   "component": "apps/venue-management-web/src/routes/games-rides/WalletCreditManagementDashboard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-415",
    "BO-416",
    "BO-417",
    "BO-418",
    "BO-419",
    "BO-420",
    "BO-421",
    "BO-422",
    "BO-423"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 3 wiring, 11 September 2026",
     "back": true
    },
    {
     "to": "BO-415",
     "trigger": "Wallet & Credit Type Configuration",
     "provenance": "structural — pack board 3 wiring, 11 September 2026"
    },
    {
     "to": "BO-416",
     "trigger": "Wallet Account & Balance View",
     "provenance": "structural — pack board 3 wiring, 11 September 2026"
    },
    {
     "to": "BO-417",
     "trigger": "Top-Up Configuration",
     "provenance": "structural — pack board 3 wiring, 11 September 2026"
    },
    {
     "to": "BO-418",
     "trigger": "Top-Up Bonus Rule Configuration",
     "provenance": "structural — pack board 3 wiring, 11 September 2026"
    },
    {
     "to": "BO-419",
     "trigger": "Bonus Usage Restrictions",
     "provenance": "structural — pack board 3 wiring, 11 September 2026"
    },
    {
     "to": "BO-420",
     "trigger": "Bonus Validity & Expiry Configuration",
     "provenance": "structural — pack board 3 wiring, 11 September 2026"
    },
    {
     "to": "BO-421",
     "trigger": "Free Game & Ride Credit Management",
     "provenance": "structural — pack board 3 wiring, 11 September 2026"
    },
    {
     "to": "BO-422",
     "trigger": "Refund, Adjustment & Manual Bonus Control",
     "provenance": "structural — pack board 3 wiring, 11 September 2026"
    },
    {
     "to": "BO-423",
     "trigger": "Wallet Credit Transaction Ledger & Audit",
     "provenance": "structural — pack board 3 wiring, 11 September 2026"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Authorized users can understand current wallet and credit activity without navigating through individual wallets.",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§KPI Cards) and a per-row directory (§Show) — counts over a population, then the population",
  "purpose": "Provide a central management view of wallet balances, credit issuance, bonus utilization, free-game credits and top-up activity across the operation.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Game_and_Ride_Module.pdf, page 23 §Show"
   }
  ],
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search wallet credit",
       "provenance": "pack Game_and_Ride_Module.pdf, page 23 §Filters"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Venue",
        "Date",
        "Wallet Type",
        "Credit Type",
        "Customer",
        "Status"
       ],
       "notes": "The pack filters this screen by venue, date, wallet type, credit type, customer, status — which are present is a decision the pack already made.",
       "provenance": "pack Game_and_Ride_Module.pdf, page 23 §Filters"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Active Wallets",
       "provenance": "pack Game_and_Ride_Module.pdf, page 23 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Total Paid Credit Balance",
       "provenance": "pack Game_and_Ride_Module.pdf, page 23 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Total Bonus Balance",
       "provenance": "pack Game_and_Ride_Module.pdf, page 23 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Free Game/Ride Credits",
       "provenance": "pack Game_and_Ride_Module.pdf, page 23 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Top-Ups Today",
       "provenance": "pack Game_and_Ride_Module.pdf, page 23 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Bonus Issued Today",
       "provenance": "pack Game_and_Ride_Module.pdf, page 23 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Bonus Used Today",
       "provenance": "pack Game_and_Ride_Module.pdf, page 23 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Expiring Bonus",
       "provenance": "pack Game_and_Ride_Module.pdf, page 23 §KPI Cards"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every wallet credit",
       "columns": [
        "Top-Ups"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Game_and_Ride_Module.pdf, page 23 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected wallet credit",
       "bindsTo": null,
       "columns": [
        "Top-Ups"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Page 23 of 105”, “Break down wallet value into”.",
       "provenance": "pack Game_and_Ride_Module.pdf, page 23 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The wallet credit list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the wallet credit untouched.",
   "emptyFirstRun": "No wallet credit yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the wallet credit are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-414"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 23. 0 of 7 labels bound to a contract property; 15 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-415",
  "name": "Wallet & Credit Type Configuration",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "3",
   "number": "2",
   "page": 24
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/wallet-credit-type-configuration-bo-415",
   "component": "apps/venue-management-web/src/routes/games-rides/WalletCreditTypeConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-414"
   ],
   "exitTo": [
    "BO-414"
   ],
   "transitions": [
    {
     "to": "BO-414",
     "trigger": "Back to Wallet & Credit Management Dashboard",
     "provenance": "structural — pack board 3 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Administrators can define and maintain distinct wallet value types with controlled usage behavior. Redemption-credit accumulation and prize redemption will be configured in detail under Board 6, rather than duplicated here.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configuration Fields) and no display directory — it is settings, not a population",
  "purpose": "Define the different value buckets that can exist inside a guest's digital wallet. The source distinguishes normal wallet value, bonus value, free-game credits and game/ride entitlements.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Credit Type Name",
       "provenance": "pack Game_and_Ride_Module.pdf, page 24 §Configuration Fields"
      },
      {
       "kind": "selectField",
       "label": "Code",
       "provenance": "pack Game_and_Ride_Module.pdf, page 24 §Configuration Fields"
      },
      {
       "kind": "selectField",
       "label": "Description",
       "provenance": "pack Game_and_Ride_Module.pdf, page 24 §Configuration Fields"
      },
      {
       "kind": "selectField",
       "label": "Monetary / Non-Monetary",
       "provenance": "pack Game_and_Ride_Module.pdf, page 24 §Configuration Fields"
      },
      {
       "kind": "selectField",
       "label": "Usage Scope",
       "provenance": "pack Game_and_Ride_Module.pdf, page 24 §Configuration Fields"
      },
      {
       "kind": "selectField",
       "label": "Refundable",
       "provenance": "pack Game_and_Ride_Module.pdf, page 24 §Configuration Fields"
      },
      {
       "kind": "selectField",
       "label": "Transferable",
       "provenance": "pack Game_and_Ride_Module.pdf, page 24 §Configuration Fields"
      },
      {
       "kind": "selectField",
       "label": "Validity Required",
       "provenance": "pack Game_and_Ride_Module.pdf, page 24 §Configuration Fields"
      },
      {
       "kind": "selectField",
       "label": "Priority",
       "provenance": "pack Game_and_Ride_Module.pdf, page 24 §Configuration Fields"
      },
      {
       "kind": "selectField",
       "label": "Active / Inactive",
       "provenance": "pack Game_and_Ride_Module.pdf, page 24 §Configuration Fields"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The wallet credit type configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the wallet credit type untouched.",
   "emptyFirstRun": "No wallet credit type configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-415"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 24. 0 of 0 labels bound to a contract property; 10 of 27 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-416",
  "name": "Wallet Account & Balance View",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "3",
   "number": "3",
   "page": 25
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/wallet-account-balance-view-bo-416",
   "component": "apps/venue-management-web/src/routes/games-rides/WalletAccountBalanceView.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-414"
   ],
   "exitTo": [
    "BO-414"
   ],
   "transitions": [
    {
     "to": "BO-414",
     "trigger": "Back to Wallet & Credit Management Dashboard",
     "provenance": "structural — pack board 3 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "The operator can clearly distinguish paid, bonus, free, redemption and entitlement balances belonging to the same wallet.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow authorized operators to inspect all value held in an individual guest wallet. The source requires stored credits to be viewable through operator and self-service kiosks.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 5 actions on this screen and the screen declares 0 operations.** Unserved: View Transactions, Add Credit — permission controlled, Add Bonus — permission controlled, View Entitlements, Block Wallet. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Game_and_Ride_Module.pdf, page 25 §Actions"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 25"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 25"
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
       "label": "View Transactions",
       "provenance": "pack Game_and_Ride_Module.pdf, page 25 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Add Credit — permission controlled",
       "provenance": "pack Game_and_Ride_Module.pdf, page 25 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Add Bonus — permission controlled",
       "provenance": "pack Game_and_Ride_Module.pdf, page 25 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "View Entitlements",
       "provenance": "pack Game_and_Ride_Module.pdf, page 25 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Block Wallet",
       "provenance": "pack Game_and_Ride_Module.pdf, page 25 §Actions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The wallet account balance list.",
   "error": "Could not load. Names which read failed and leaves the wallet account balance untouched.",
   "emptyFirstRun": "No wallet account balance yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the wallet account balance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-416"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 25. 0 of 0 labels bound to a contract property; 5 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-417",
  "name": "Top-Up Configuration",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "3",
   "number": "4",
   "page": 26
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/top-up-configuration-bo-417",
   "component": "apps/venue-management-web/src/routes/games-rides/TopUpConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-414"
   ],
   "exitTo": [
    "BO-414"
   ],
   "transitions": [
    {
     "to": "BO-414",
     "trigger": "Back to Wallet & Credit Management Dashboard",
     "provenance": "structural — pack board 3 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Administrators can define permitted wallet top-up values and their applicable channels/effective periods.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure the rules governing customer wallet recharges.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 26"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 26"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The top-up list.",
   "error": "Could not load. Names which read failed and leaves the top-up untouched.",
   "emptyFirstRun": "No top-up yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the top-up are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-417"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 26. 0 of 0 labels bound to a contract property; 0 of 19 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-418",
  "name": "Top-Up Bonus Rule Configuration",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "3",
   "number": "5",
   "page": 27
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/top-up-bonus-rule-configuration-bo-418",
   "component": "apps/venue-management-web/src/routes/games-rides/TopUpBonusRuleConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-414"
   ],
   "exitTo": [
    "BO-414"
   ],
   "transitions": [
    {
     "to": "BO-414",
     "trigger": "Back to Wallet & Credit Management Dashboard",
     "provenance": "structural — pack board 3 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "The system automatically calculates and allocates the correct bonus based on the configured top-up rule.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure promotional bonus value automatically awarded when a customer tops up. The requirement explicitly gives the example: Top-Up AED 100 → AED 100 Paid Credit + AED 25 Bonus.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 27"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 27"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The top-up bonus rule list.",
   "error": "Could not load. Names which read failed and leaves the top-up bonus rule untouched.",
   "emptyFirstRun": "No top-up bonus rule yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the top-up bonus rule are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-418"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 27. 0 of 0 labels bound to a contract property; 0 of 18 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-419",
  "name": "Bonus Usage Restrictions",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "3",
   "number": "6",
   "page": 27
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/bonus-usage-restrictions-bo-419",
   "component": "apps/venue-management-web/src/routes/games-rides/BonusUsageRestrictions.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-414"
   ],
   "exitTo": [
    "BO-414"
   ],
   "transitions": [
    {
     "to": "BO-414",
     "trigger": "Back to Wallet & Credit Management Dashboard",
     "provenance": "structural — pack board 3 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Bonus value cannot be consumed outside its configured business scope.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Control where promotional bonus value can and cannot be spent. This is a critical requirement because the source states that the bonus can be used for amusement park games/rides but not for F&B or Retail, and that this must be configurable.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 27"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 27"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The bonus usage restrictions list.",
   "error": "Could not load. Names which read failed and leaves the bonus usage restrictions untouched.",
   "emptyFirstRun": "No bonus usage restrictions yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the bonus usage restrictions are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-419"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 27. 0 of 0 labels bound to a contract property; 0 of 19 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-420",
  "name": "Bonus Validity & Expiry Configuration",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "3",
   "number": "7",
   "page": 28
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/bonus-validity-expiry-configuration-bo-420",
   "component": "apps/venue-management-web/src/routes/games-rides/BonusValidityExpiryConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-414"
   ],
   "exitTo": [
    "BO-414"
   ],
   "transitions": [
    {
     "to": "BO-414",
     "trigger": "Back to Wallet & Credit Management Dashboard",
     "provenance": "structural — pack board 3 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Every bonus allocation follows the configured validity rule and becomes unusable after expiry.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Define how long promotional bonus credit remains valid. The source specifically requires the ability to set a validity period for the bonus.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 28"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 28"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The bonus validity expiry list.",
   "error": "Could not load. Names which read failed and leaves the bonus validity expiry untouched.",
   "emptyFirstRun": "No bonus validity expiry yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the bonus validity expiry are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-420"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 28. 0 of 0 labels bound to a contract property; 0 of 17 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-421",
  "name": "Free Game & Ride Credit Management",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "3",
   "number": "8",
   "page": 29
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/free-game-ride-credit-management-bo-421",
   "component": "apps/venue-management-web/src/routes/games-rides/FreeGameRideCreditManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-414"
   ],
   "exitTo": [
    "BO-414"
   ],
   "transitions": [
    {
     "to": "BO-414",
     "trigger": "Back to Wallet & Credit Management Dashboard",
     "provenance": "structural — pack board 3 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Authorized users can issue free-game/ride credits and restrict them to applicable attractions and validity periods.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Free Credit Configuration) and no display directory — it is settings, not a population",
  "purpose": "Configure and allocate free gameplay credits to customer wallets. The requirement explicitly requires the system to add credits for free games and rides to a guest's digital wallet, usable across applicable attractions.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Credit Name",
       "provenance": "pack Game_and_Ride_Module.pdf, page 29 §Free Credit Configuration"
      },
      {
       "kind": "selectField",
       "label": "Game / Ride",
       "provenance": "pack Game_and_Ride_Module.pdf, page 29 §Free Credit Configuration"
      },
      {
       "kind": "selectField",
       "label": "Attraction Type",
       "provenance": "pack Game_and_Ride_Module.pdf, page 29 §Free Credit Configuration"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Game_and_Ride_Module.pdf, page 29 §Free Credit Configuration"
      },
      {
       "kind": "textField",
       "label": "Number of Free Plays",
       "provenance": "pack Game_and_Ride_Module.pdf, page 29 §Free Credit Configuration"
      },
      {
       "kind": "selectField",
       "label": "Unlimited / Limited",
       "provenance": "pack Game_and_Ride_Module.pdf, page 29 §Free Credit Configuration"
      },
      {
       "kind": "selectField",
       "label": "Valid From",
       "provenance": "pack Game_and_Ride_Module.pdf, page 29 §Free Credit Configuration"
      },
      {
       "kind": "selectField",
       "label": "Valid Until",
       "provenance": "pack Game_and_Ride_Module.pdf, page 29 §Free Credit Configuration"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The free game ride configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the free game ride untouched.",
   "emptyFirstRun": "No free game ride configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-421"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 29. 0 of 0 labels bound to a contract property; 8 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-422",
  "name": "Refund, Adjustment & Manual Bonus Control",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "3",
   "number": "9",
   "page": 30
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/refund-adjustment-manual-bonus-control-bo-422",
   "component": "apps/venue-management-web/src/routes/games-rides/RefundAdjustmentManualBonusControl.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-414"
   ],
   "exitTo": [
    "BO-414"
   ],
   "transitions": [
    {
     "to": "BO-414",
     "trigger": "Back to Wallet & Credit Management Dashboard",
     "provenance": "structural — pack board 3 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Bonus cannot be refunded, while authorized staff can provide additional bonus under controlled permissions and audit rules.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Enforce refund restrictions and provide governed manual wallet adjustments.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 30"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 30"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The refund adjustment manual list.",
   "error": "Could not load. Names which read failed and leaves the refund adjustment manual untouched.",
   "emptyFirstRun": "No refund adjustment manual yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the refund adjustment manual are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-422"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 30. 0 of 0 labels bound to a contract property; 0 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-423",
  "name": "Wallet Credit Transaction Ledger & Audit",
  "module": "Games & Rides",
  "requiresModule": "games",
  "wave": 3,
  "source": {
   "pack": "Game_and_Ride_Module.pdf",
   "board": "3",
   "number": "10",
   "page": 30
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/games-rides/wallet-credit-transaction-ledger-audit-bo-423",
   "component": "apps/venue-management-web/src/routes/games-rides/WalletCreditTransactionLedgerAudit.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-414"
   ],
   "exitTo": [
    "BO-414"
   ],
   "transitions": [
    {
     "to": "BO-414",
     "trigger": "Back to Wallet & Credit Management Dashboard",
     "provenance": "structural — pack board 3 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Every credit issuance, deduction, expiry or adjustment can be traced to its source and resulting balance.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide complete traceability for every change to wallet value.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 30"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Game_and_Ride_Module.pdf, page 30"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The wallet credit transaction list.",
   "error": "Could not load. Names which read failed and leaves the wallet credit transaction untouched.",
   "emptyFirstRun": "No wallet credit transaction yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the wallet credit transaction are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-423"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 30. 0 of 0 labels bound to a contract property; 0 of 66 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
