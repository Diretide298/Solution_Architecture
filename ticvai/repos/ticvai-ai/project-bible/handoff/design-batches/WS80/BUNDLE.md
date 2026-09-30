# WS80 — Game and Ride board 3

**10 screens · 16 operations · 13 schemas · 5 permissions**

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
  `PRODUCT_CONFIGURE, PRODUCT_VIEW, WALLET_CONFIGURE, WALLET_OPERATE, WALLET_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-414` | Wallet & Credit Management Dashboard | commandCentre | 2 | 0 | — |
| `BO-415` | Wallet & Credit Type Configuration | configEditor | 2 | 0 | — |
| `BO-416` | Wallet Account & Balance View | listDetail | 8 | 0 | — |
| `BO-417` | Top-Up Configuration | listDetail | 1 | 0 | — |
| `BO-418` | Top-Up Bonus Rule Configuration | listDetail | 1 | 0 | — |
| `BO-419` | Bonus Usage Restrictions | listDetail | 1 | 0 | — |
| `BO-420` | Bonus Validity & Expiry Configuration | listDetail | 1 | 0 | — |
| `BO-421` | Free Game & Ride Credit Management | configEditor | 2 | 0 | — |
| `BO-422` | Refund, Adjustment & Manual Bonus Control | listDetail | 1 | 0 | — |
| `BO-423` | Wallet Credit Transaction Ledger & Audit | listDetail | 1 | 0 | — |

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
     "provenance": "structural — pack board 3 wiring, 11 September 2026",
     "carries": [
      "subjectId"
     ]
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
     "provenance": "structural — pack board 3 wiring, 11 September 2026",
     "carries": [
      "subjectId"
     ]
    },
    {
     "to": "BO-423",
     "trigger": "Wallet Credit Transaction Ledger & Audit",
     "provenance": "structural — pack board 3 wiring, 11 September 2026",
     "carries": [
      "subjectId"
     ]
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
  "apis": [
   {
    "operationId": "getWallet",
    "contract": "wallet",
    "purpose": "The game credit balance",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listWalletTransactions",
    "contract": "wallet",
    "purpose": "Recent movement",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-414",
   "workshopBoard": "wireframes/WS60 Game and Ride Board 3.dc.html#bo-414"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 23. 0 of 7 labels bound to a contract property; 15 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "notes": "**Superseded by `BO-1088` Credit & Balance Type Configuration** from `Wallet_Configuration_Backend_Structure_v1.0.pdf`, 19 September 2026. This screen came from `Game_and_Ride_Module.pdf`, which describes the wallet incidentally; the wallet pack is the workshop dedicated to it and is backed by the 27 August MoM and matrix 4.3.28-4.3.35. It has zero components, so nothing rendered is lost. Not `source.sameAs` - that means twin, and these are not copies of each other.",
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
  "apis": [
   {
    "operationId": "listCreditTypes",
    "contract": "wallet",
    "purpose": "The credit type library",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "createCreditType",
    "contract": "wallet",
    "purpose": "Define one",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-415",
   "workshopBoard": "wireframes/WS60 Game and Ride Board 3.dc.html#bo-415"
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
     "back": true,
     "carries": [
      "subjectId"
     ]
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
    },
    {
     "name": "contentBody",
     "components": []
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
  "apis": [
   {
    "operationId": "getWallet",
    "contract": "wallet",
    "purpose": "Account and balance",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listCreditLots",
    "contract": "wallet",
    "purpose": "The lots behind it",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "adjustWallet",
    "contract": "wallet",
    "purpose": "Add credit or bonus to the wallet (permission controlled)",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration): serves the pack action(s) Add Credit — permission controlled, Add Bonus — permission controlled; Block Wallet",
    "invalidates": [
     "getWallet",
     "listCreditLots"
    ]
   },
   {
    "operationId": "suspendWallet",
    "contract": "wallet",
    "purpose": "Block the wallet",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration): serves the pack action(s) Add Credit — permission controlled, Add Bonus — permission controlled; Block Wallet",
    "invalidates": [
     "getWallet",
     "listCreditLots"
    ]
   },
   {
    "operationId": "getWalletAutoReloadSetting",
    "contract": "wallet",
    "purpose": "Show auto top-up",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "setWalletAutoReloadSetting",
    "contract": "wallet",
    "purpose": "Set auto top-up",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
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
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-416",
   "workshopBoard": "wireframes/WS60 Game and Ride Board 3.dc.html#bo-416"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 25. 0 of 0 labels bound to a contract property; 5 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Add Credit — permission controlled, Add Bonus — permission controlled: `adjustWallet`; Block Wallet: `suspendWallet`; View Transactions, View Entitlements dropped (navigation).",
  "entryState": {
   "params": [
    {
     "name": "subjectId",
     "from": "navigation"
    },
    {
     "name": "walletId",
     "from": "navigation"
    }
   ],
   "coldEntry": "Opened from BO-414 with the wallet picked there. Opened cold (a bookmark or a refresh), it shows the list to pick from rather than an empty record, and says plainly if the wallet no longer exists."
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
  "notes": "**Superseded by `BO-1095` Top-Up Rule Configuration** from `Wallet_Configuration_Backend_Structure_v1.0.pdf`, 19 September 2026. This screen came from `Game_and_Ride_Module.pdf`, which describes the wallet incidentally; the wallet pack is the workshop dedicated to it and is backed by the 27 August MoM and matrix 4.3.28-4.3.35. It has zero components, so nothing rendered is lost. Not `source.sameAs` - that means twin, and these are not copies of each other.",
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
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "setWalletFundingRules",
       "label": "Save wallet funding rules",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setWalletFundingRules"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The top-up list.",
   "error": "Could not load. Names which read failed and leaves the top-up untouched.",
   "emptyFirstRun": "No top-up yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the top-up are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setWalletFundingRules",
    "contract": "wallet",
    "purpose": "Top-up rules",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-417",
   "workshopBoard": "wireframes/WS60 Game and Ride Board 3.dc.html#bo-417"
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
  "notes": "**Superseded by `BO-1105` Credit Issuance Rule Configuration** from `Wallet_Configuration_Backend_Structure_v1.0.pdf`, 19 September 2026. This screen came from `Game_and_Ride_Module.pdf`, which describes the wallet incidentally; the wallet pack is the workshop dedicated to it and is backed by the 27 August MoM and matrix 4.3.28-4.3.35. It has zero components, so nothing rendered is lost. Not `source.sameAs` - that means twin, and these are not copies of each other.",
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
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "setWalletFundingRules",
       "label": "Save wallet funding rules",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setWalletFundingRules"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The top-up bonus rule list.",
   "error": "Could not load. Names which read failed and leaves the top-up bonus rule untouched.",
   "emptyFirstRun": "No top-up bonus rule yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the top-up bonus rule are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setWalletFundingRules",
    "contract": "wallet",
    "purpose": "Top-up bonus rules",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-418",
   "workshopBoard": "wireframes/WS60 Game and Ride Board 3.dc.html#bo-418"
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
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "setCreditEligibilityRules",
       "label": "Save",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setCreditEligibilityRules"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The bonus usage restrictions list.",
   "error": "Could not load. Names which read failed and leaves the bonus usage restrictions untouched.",
   "emptyFirstRun": "No bonus usage restrictions yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the bonus usage restrictions are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setCreditEligibilityRules",
    "contract": "wallet",
    "purpose": "Bonus usage restrictions",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-419",
   "workshopBoard": "wireframes/WS60 Game and Ride Board 3.dc.html#bo-419"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 27. 0 of 0 labels bound to a contract property; 0 of 19 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "creditTypeId",
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
  "notes": "**Superseded by `BO-1108` Expiry & Validity Policy Configuration** from `Wallet_Configuration_Backend_Structure_v1.0.pdf`, 19 September 2026. This screen came from `Game_and_Ride_Module.pdf`, which describes the wallet incidentally; the wallet pack is the workshop dedicated to it and is backed by the 27 August MoM and matrix 4.3.28-4.3.35. It has zero components, so nothing rendered is lost. Not `source.sameAs` - that means twin, and these are not copies of each other.",
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
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "updateCreditType",
       "label": "Save credit type",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "updateCreditType"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The bonus validity expiry list.",
   "error": "Could not load. Names which read failed and leaves the bonus validity expiry untouched.",
   "emptyFirstRun": "No bonus validity expiry yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the bonus validity expiry are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "updateCreditType",
    "contract": "wallet",
    "purpose": "Bonus validity and expiry",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-420",
   "workshopBoard": "wireframes/WS60 Game and Ride Board 3.dc.html#bo-420"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 28. 0 of 0 labels bound to a contract property; 0 of 17 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "creditTypeId",
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
  "apis": [
   {
    "operationId": "listGameEntitlements",
    "contract": "games",
    "purpose": "Free game and ride credit",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "createGameEntitlement",
    "contract": "games",
    "purpose": "Grant free play",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listGameEntitlements"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-421",
   "workshopBoard": "wireframes/WS60 Game and Ride Board 3.dc.html#bo-421"
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
     "back": true,
     "carries": [
      "subjectId"
     ]
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
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "adjustWallet",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "adjustWallet"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The refund adjustment manual list.",
   "error": "Could not load. Names which read failed and leaves the refund adjustment manual untouched.",
   "emptyFirstRun": "No refund adjustment manual yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the refund adjustment manual are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "adjustWallet",
    "contract": "wallet",
    "purpose": "Refund, adjust or grant bonus",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-422",
   "workshopBoard": "wireframes/WS60 Game and Ride Board 3.dc.html#bo-422"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 30. 0 of 0 labels bound to a contract property; 0 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
     "back": true,
     "carries": [
      "subjectId"
     ]
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
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listWalletTransactions",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The wallet credit transaction list.",
   "error": "Could not load. Names which read failed and leaves the wallet credit transaction untouched.",
   "emptyFirstRun": "No wallet credit transaction yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the wallet credit transaction are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listWalletTransactions",
    "contract": "wallet",
    "purpose": "The credit ledger",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-423",
   "workshopBoard": "wireframes/WS60 Game and Ride Board 3.dc.html#bo-423"
  },
  "apisNote": "Regenerated 9 September 2026 from Game_and_Ride_Module.pdf page 30. 0 of 0 labels bound to a contract property; 0 of 66 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 }
]
```

## `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
 "adjustWallet": {
  "method": "POST",
  "path": "/wallets/{subjectId}/adjust",
  "contract": "wallet",
  "summary": "Manually adjust a wallet balance",
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
  "responds": "Wallet"
 },
 "createCreditType": {
  "method": "POST",
  "path": "/credit-types",
  "contract": "wallet",
  "summary": "Define a kind of credit, without a release",
  "permission": "WALLET_CONFIGURE",
  "offlineCapable": null,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "CreditType",
  "responds": "CreditType"
 },
 "createGameEntitlement": {
  "method": "POST",
  "path": "/game-entitlements",
  "contract": "games",
  "summary": "Define a pass, package or per-game entitlement",
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
  "requestBody": "GameEntitlement",
  "responds": "GameEntitlement"
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
 "getWalletAutoReloadSetting": {
  "method": "GET",
  "path": "/wallets/{walletId}/auto-reload",
  "contract": "wallet",
  "summary": "A wallet's own auto top-up, if the holder set one",
  "permission": "WALLET_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "WalletAutoReloadSetting"
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
 "listCreditLots": {
  "method": "GET",
  "path": "/credit-lots",
  "contract": "wallet",
  "summary": "The tranches behind a balance, with their expiry",
  "permission": "WALLET_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "walletId",
    "in": "query",
    "required": true
   },
   {
    "name": "includeExhausted",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "CreditLot"
 },
 "listCreditTypes": {
  "method": "GET",
  "path": "/credit-types",
  "contract": "wallet",
  "summary": "The kinds of value that may sit in a wallet",
  "permission": "WALLET_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "CreditType"
 },
 "listGameEntitlements": {
  "method": "GET",
  "path": "/game-entitlements",
  "contract": "games",
  "summary": "Passes, packages and per-game entitlements",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "GameEntitlement"
 },
 "listWalletTransactions": {
  "method": "GET",
  "path": "/wallets/{subjectId}/transactions",
  "contract": "wallet",
  "summary": "Wallet transaction history",
  "permission": "WALLET_VIEW",
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
 "setCreditEligibilityRules": {
  "method": "PUT",
  "path": "/credit-types/{creditTypeId}/eligibility",
  "contract": "wallet",
  "summary": "Where this credit may be spent, and on what",
  "permission": "WALLET_CONFIGURE",
  "offlineCapable": null,
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
  "requestBody": "CreditEligibility",
  "responds": "CreditEligibility"
 },
 "setWalletAutoReloadSetting": {
  "method": "PUT",
  "path": "/wallets/{walletId}/auto-reload",
  "contract": "wallet",
  "summary": "Top the wallet up automatically from a stored card when it runs low",
  "permission": "WALLET_OPERATE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "subject",
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
  "requestBody": "WalletAutoReloadSetting",
  "responds": "WalletAutoReloadSetting"
 },
 "setWalletFundingRules": {
  "method": "PUT",
  "path": "/wallet-funding-rules",
  "contract": "wallet",
  "summary": "Amounts, channels, bonuses, limits and velocity",
  "permission": "WALLET_CONFIGURE",
  "offlineCapable": null,
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
  "requestBody": "WalletFundingRules",
  "responds": "WalletFundingRules"
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
 "suspendWallet": {
  "method": "POST",
  "path": "/wallets/{walletId}/suspend",
  "contract": "wallet",
  "summary": "Freeze a wallet",
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
  "responds": "Wallet"
 },
 "updateCreditType": {
  "method": "PUT",
  "path": "/credit-types/{creditTypeId}",
  "contract": "wallet",
  "summary": "Change a kind of credit",
  "permission": "WALLET_CONFIGURE",
  "offlineCapable": null,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
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
  "requestBody": "CreditType",
  "responds": "CreditType"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "CreditEligibility": {
  "type": "object",
  "x-ticvai-persistence": "wallet.credit_eligibility",
  "description": "Board 3.4. **Where credit may be spent** — acceptance, not funding.",
  "properties": {
   "creditTypeId": {
    "type": "string",
    "format": "uuid"
   },
   "allowedVenueIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "allowedOutletKinds": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "allowedProductCategoryIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "excludedProductIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "allowedChannels": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "minimumSpend": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "maximumPercentOfBasket": {
    "type": "number",
    "nullable": true,
    "description": "**Caps how much of a purchase one credit type may cover.** A venue that lets promotional credit pay for everything has run a free day it did not intend.\n"
   },
   "validDaysOfWeek": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "CreditLot": {
  "type": "object",
  "x-ticvai-persistence": "wallet.credit_lot",
  "description": "Board 3.7. **The tranche behind a balance.** Expiry belongs here, not on the wallet.",
  "required": [
   "id",
   "walletId",
   "creditTypeId"
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
   "creditTypeId": {
    "type": "string",
    "format": "uuid"
   },
   "issuedAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "remainingAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "issuedAt": {
    "type": "string",
    "format": "date-time"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "sourceKind": {
    "type": "string",
    "enum": [
     "topUp",
     "refund",
     "promotion",
     "giftCard",
     "membershipBenefit",
     "loyaltyConversion",
     "transfer",
     "adjustment"
    ]
   },
   "sourceReference": {
    "type": "string",
    "nullable": true
   },
   "termsSnapshot": {
    "type": "object",
    "additionalProperties": true,
    "description": "**The credit type's terms as they stood at issue.** Changing a credit type must not retro-expire credit already given, so the lot carries its own terms.\n**Open on purpose, and its shape lives in `CreditType`**: the snapshot is that credit type's properties copied at issue, so it follows `CreditType` as it stood then rather than as it stands now.\n"
   },
   "status": {
    "type": "string",
    "enum": [
     "active",
     "exhausted",
     "expired",
     "forfeited",
     "reversed"
    ]
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "CreditType": {
  "type": "object",
  "x-ticvai-persistence": "wallet.credit_type",
  "description": "Board 1.6. **What value sits inside a wallet** — the second vocabulary, and the one the acceptance condition requires to be a table.\n",
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
   "category": {
    "type": "string",
    "enum": [
     "cash",
     "refund",
     "bonus",
     "promotional",
     "giftCard",
     "membership",
     "loyalty",
     "ride",
     "attraction",
     "redemption",
     "fnb",
     "retail",
     "parking",
     "event",
     "other"
    ]
   },
   "monetary": {
    "type": "boolean",
    "default": true,
    "description": "**Loyalty points are not money.** A non-monetary credit has a conversion rate to money or it cannot be spent, and treating points as currency puts them on the balance sheet.\n"
   },
   "conversionRate": {
    "type": "number",
    "nullable": true
   },
   "refundable": {
    "type": "boolean",
    "default": false,
    "description": "**Promotional credit is not refundable and cash credit is.** A venue that refunds promotional credit to a card has converted marketing spend into cash.\n"
   },
   "transferable": {
    "type": "boolean",
    "default": false
   },
   "expires": {
    "type": "boolean",
    "default": false
   },
   "validityDays": {
    "type": "integer",
    "nullable": true
   },
   "breakageEligible": {
    "type": "boolean",
    "default": false
   },
   "ledgerAccountCode": {
    "type": "string",
    "nullable": true
   },
   "priority": {
    "type": "integer",
    "default": 0
   },
   "scopePath": {
    "type": "string"
   },
   "isActive": {
    "type": "boolean",
    "default": true
   }
  }
 },
 "GameEntitlement": {
  "type": "object",
  "x-ticvai-persistence": "games.entitlement",
  "description": "Board 4. **A right to play, not money** — consumed before money is.",
  "required": [
   "code",
   "kind"
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
   "kind": {
    "type": "string",
    "enum": [
     "allGamesPass",
     "unlimitedSingleGame",
     "limitedSingleGame",
     "package",
     "freePlay"
    ]
   },
   "gameIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "attractionTypeIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "playCount": {
    "type": "integer",
    "nullable": true,
    "description": "For `limitedSingleGame` and `package`. Null means unlimited."
   },
   "validityKind": {
    "type": "string",
    "enum": [
     "sameDay",
     "days",
     "untilDate",
     "untilUsed"
    ]
   },
   "validityDays": {
    "type": "integer",
    "nullable": true
   },
   "activationKind": {
    "type": "string",
    "enum": [
     "onPurchase",
     "onFirstUse",
     "onDate"
    ],
    "default": "onFirstUse",
    "description": "**On first use is what a guest expects from a day pass bought the night before.** On purchase is what a venue defaults to by accident, and it costs them a day.\n"
   },
   "dailyPlayCap": {
    "type": "integer",
    "nullable": true
   },
   "cooldownMinutes": {
    "type": "integer",
    "nullable": true,
    "description": "**Unlimited does not mean continuous.** A cooldown is how one child does not hold a popular ride all afternoon.\n"
   },
   "linkedProductId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "scopePath": {
    "type": "string"
   },
   "isActive": {
    "type": "boolean",
    "default": true
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
 "WalletAutoReloadSetting": {
  "type": "object",
  "x-ticvai-persistence": "wallet.auto_reload_setting",
  "description": "4.2.17, 4.3.28. Also the `setWalletAutoReloadSetting` body. One per wallet; the holder's own setting within the venue's `WalletFundingRules.autoReload`.",
  "required": [
   "enabled"
  ],
  "properties": {
   "walletId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "enabled": {
    "type": "boolean"
   },
   "thresholdAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "reloadAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "paymentTokenId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "maximumPerDay": {
    "type": "integer",
    "minimum": 1,
    "nullable": true
   },
   "status": {
    "type": "string",
    "readOnly": true,
    "enum": [
     "active",
     "suspendedAfterDecline",
     "disabledByVenue"
    ]
   },
   "lastReloadAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Written at the wallet's venue scope."
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
 },
 "WalletFundingRules": {
  "type": "object",
  "x-ticvai-persistence": "wallet.funding_rules",
  "description": "Board 2, which is the 27 August minute one screen for one.",
  "properties": {
   "walletTypeId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "minimumTopUp": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "maximumTopUp": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "presetAmounts": {
    "type": "array",
    "items": {
     "$ref": "../shared/common.yaml#/components/schemas/Money"
    }
   },
   "allowedChannels": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "allowedFundingSources": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "card",
      "cash",
      "bankTransfer",
      "voucher",
      "corporateAccount",
      "loyaltyConversion"
     ]
    }
   },
   "bonusRules": {
    "type": "array",
    "description": "Board 2.3. *Top up 200, get 20.* **The bonus is a separate lot of a separate credit type**, which is how it can expire on different terms from the cash.\n",
    "items": {
     "type": "object",
     "properties": {
      "minimumAmount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "bonusAmount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "bonusPercent": {
       "type": "number",
       "nullable": true
      },
      "bonusCreditTypeId": {
       "type": "string",
       "format": "uuid"
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
      }
     }
    }
   },
   "autoReload": {
    "type": "object",
    "description": "Board 2.5, matrix 4.3.28. **Fires when the balance drops.**",
    "properties": {
     "enabled": {
      "type": "boolean",
      "default": false
     },
     "thresholdAmount": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "reloadAmount": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "maximumPerDay": {
      "type": "integer",
      "nullable": true
     }
    }
   },
   "recurringFunding": {
    "type": "object",
    "description": "Board 2.6, matrix 4.3.29 — ***\"distinct from auto-reload\"***. **Fires on a date**, which is what an allowance needs.\n",
    "properties": {
     "enabled": {
      "type": "boolean",
      "default": false
     },
     "cadence": {
      "type": "string",
      "enum": [
       "daily",
       "weekly",
       "monthly"
      ]
     },
     "amount": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "dayOfWeek": {
      "type": "string",
      "nullable": true
     },
     "dayOfMonth": {
      "type": "integer",
      "nullable": true
     }
    }
   },
   "approvalAboveAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "velocityLimits": {
    "type": "object",
    "description": "**A fraud control, not a commercial one.** Ten top-ups of ninety-nine in an hour is a card being tested, and a daily cap in total value does not catch it.\n",
    "properties": {
     "maxTransactionsPerHour": {
      "type": "integer",
      "nullable": true
     },
     "maxTransactionsPerDay": {
      "type": "integer",
      "nullable": true
     },
     "maxAmountPerDay": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "maxAmountPerMonth": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    }
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "WalletTransaction": {
  "x-ticvai-persistence": "wallet.wallet_transaction",
  "type": "object",
  "required": [
   "id",
   "kind",
   "amount",
   "balanceAfter",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string"
   },
   "walletId": {
    "type": "string",
    "format": "uuid",
    "x-ticvai-references": "wallet.wallet",
    "description": "The wallet this movement is on (SD-027, 29 September). A shared wallet has many subjects, so the subject alone cannot say which balance moved."
   },
   "walletHoldId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "x-ticvai-references": "wallet.hold",
    "description": "The hold a spend settled, where it came through `holdWalletFunds`."
   },
   "kind": {
    "$ref": "#/components/schemas/WalletTransactionKind"
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "balanceAfter": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "orderId": {
    "type": "string",
    "nullable": true
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "reason": {
    "type": "string",
    "nullable": true
   },
   "principalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "WalletTransactionKind": {
  "type": "string",
  "enum": [
   "topUp",
   "spend",
   "refund",
   "adjustment",
   "bonus",
   "expiry",
   "transfer"
  ]
 }
}
```
