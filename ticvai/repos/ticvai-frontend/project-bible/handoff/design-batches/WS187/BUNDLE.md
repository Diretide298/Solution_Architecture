# WS187 — Wallet Configuration Backend Structure v1.0 board 2

**10 screens · 6 operations · 5 schemas · 3 permissions**

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

- **Every control that can be refused must be gated.** 3 permissions apply here:
  `WALLET_CONFIGURE, WALLET_OPERATE, WALLET_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-1093` | Funding Command Center | configEditor | 2 | 0 | — |
| `BO-1094` | Funding Method Configuration | configEditor | 1 | 0 | — |
| `BO-1095` | Top-Up Rule Configuration | configEditor | 1 | 0 | — |
| `BO-1096` | Channel & Funding Source Mapping | configEditor | 1 | 0 | — |
| `BO-1097` | Auto-Reload Configuration | configEditor | 1 | 0 | — |
| `BO-1098` | Recurring Funding Schedule | configEditor | 1 | 0 | — |
| `BO-1099` | Funding Authorization & Approval Rules | configEditor | 1 | 0 | — |
| `BO-1100` | Funding Reversal & Correction Management | configEditor | 2 | 0 | — |
| `BO-1101` | Funding Limits & Velocity Controls | configEditor | 1 | 0 | — |
| `BO-1102` | Funding Transaction Audit & Reconciliation | listDetail | 2 | 0 | — |

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-1093",
  "name": "Funding Command Center",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "2",
   "number": "01",
   "page": 13
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/funding-command-center-bo-1093",
   "component": "apps/venue-management-web/src/routes/orders-money/FundingCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-1094",
    "BO-1095",
    "BO-1096",
    "BO-1097",
    "BO-1098",
    "BO-1099",
    "BO-1100",
    "BO-1101",
    "BO-1102"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "BO-1094",
     "trigger": "Funding Method Configuration",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    },
    {
     "to": "BO-1095",
     "trigger": "Top-Up Rule Configuration",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    },
    {
     "to": "BO-1096",
     "trigger": "Channel & Funding Source Mapping",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    },
    {
     "to": "BO-1097",
     "trigger": "Auto-Reload Configuration",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    },
    {
     "to": "BO-1098",
     "trigger": "Recurring Funding Schedule",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    },
    {
     "to": "BO-1099",
     "trigger": "Funding Authorization & Approval Rules",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    },
    {
     "to": "BO-1100",
     "trigger": "Funding Reversal & Correction Management",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "carries": [
      "subjectId"
     ]
    },
    {
     "to": "BO-1101",
     "trigger": "Funding Limits & Velocity Controls",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    },
    {
     "to": "BO-1102",
     "trigger": "Funding Transaction Audit & Reconciliation",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "carries": [
      "subjectId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Backend Configuration) and no display directory — it is settings, not a population",
  "purpose": "Provide administrators and finance/operations teams with a centralized view of all wallet funding activity.",
  "purposeNote": "Authorized users can monitor wallet funding activity across all configured channels and investigate individual transactions with complete traceability.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Today",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 13 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Week",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 13 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Month",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 13 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Custom period",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 13 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Credit card",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 13 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Debit card",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 13 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Cash",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 13 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Online payment",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 13 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Gift card conversion",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 13 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Bank-linked funding",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 13 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Kiosk",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 13 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "POS",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 13 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Manual adjustment",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 13 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Auto-reload",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 13 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Recurring funding",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 13 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Successful top-ups",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 13 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Pending top-ups",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 13 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Failed top-ups",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 13 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Reversed top-ups",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 13 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Declined transactions",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 13 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Wallet type",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 13 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Customer",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 13 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Funding method",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 13 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Channel",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 13 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 13 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Currency",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 13 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Transaction status",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 13 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Date",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 13 §Backend Configuration"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The funding configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the funding untouched.",
   "emptyFirstRun": "No funding configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "getWalletFundingRules",
    "contract": "wallet",
    "purpose": "Funding rules in force",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listWalletTransactions",
    "contract": "wallet",
    "purpose": "Recent funding",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1093",
   "workshopBoard": "wireframes/WS187 Wallet Configuration Backend Structure v1.0 Board 2.dc.html#bo-1093"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 13. 0 of 0 labels bound to a contract property; 28 of 42 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1094",
  "name": "Funding Method Configuration",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "2",
   "number": "02",
   "page": 14
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/funding-method-configuration-bo-1094",
   "component": "apps/venue-management-web/src/routes/orders-money/FundingMethodConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1093"
   ],
   "exitTo": [
    "BO-1093"
   ],
   "transitions": [
    {
     "to": "BO-1093",
     "trigger": "Back to Funding Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§For each method configure) and no display directory — it is settings, not a population",
  "purpose": "Configure which funding methods TICVAI wallets can accept. The source requires multiple methods for funding wallet value, including bank-linked funding, credit/debit cards through digital channels, and cash/cards through physical channels.",
  "purposeNote": "Administrators can introduce, modify or deactivate wallet funding methods through configuration without changing application code.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Funding method name",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 14 §For each method configure"
      },
      {
       "kind": "selectField",
       "label": "Internal code",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 14 §For each method configure"
      },
      {
       "kind": "selectField",
       "label": "Funding category",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 14 §For each method configure"
      },
      {
       "kind": "selectField",
       "label": "Payment service/provider",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 14 §For each method configure"
      },
      {
       "kind": "selectField",
       "label": "Supported currencies",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 14 §For each method configure"
      },
      {
       "kind": "selectField",
       "label": "Minimum top-up",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 14 §For each method configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum top-up",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 14 §For each method configure"
      },
      {
       "kind": "selectField",
       "label": "Applicable wallet types",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 14 §For each method configure"
      },
      {
       "kind": "selectField",
       "label": "Applicable credit types",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 14 §For each method configure"
      },
      {
       "kind": "selectField",
       "label": "Applicable tenants",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 14 §For each method configure"
      },
      {
       "kind": "selectField",
       "label": "Applicable venues",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 14 §For each method configure"
      },
      {
       "kind": "selectField",
       "label": "Applicable channels",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 14 §For each method configure"
      },
      {
       "kind": "selectField",
       "label": "Customer verification requirement",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 14 §For each method configure"
      },
      {
       "kind": "selectField",
       "label": "Authorization requirement",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 14 §For each method configure"
      },
      {
       "kind": "selectField",
       "label": "Refund/reversal eligibility",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 14 §For each method configure"
      },
      {
       "kind": "selectField",
       "label": "Fees",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 14 §For each method configure"
      },
      {
       "kind": "selectField",
       "label": "Effective dates",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 14 §For each method configure"
      },
      {
       "kind": "selectField",
       "label": "Active/inactive status",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 14 §For each method configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The funding method configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the funding method untouched.",
   "emptyFirstRun": "No funding method configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setWalletFundingRules",
    "contract": "wallet",
    "purpose": "Which methods may fund a wallet",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getWalletFundingRules"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1094",
   "workshopBoard": "wireframes/WS187 Wallet Configuration Backend Structure v1.0 Board 2.dc.html#bo-1094"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 14. 0 of 0 labels bound to a contract property; 18 of 35 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1095",
  "name": "Top-Up Rule Configuration",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "2",
   "number": "03",
   "page": 15
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/top-up-rule-configuration-bo-1095",
   "component": "apps/venue-management-web/src/routes/orders-money/TopUpRuleConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1093"
   ],
   "exitTo": [
    "BO-1093"
   ],
   "transitions": [
    {
     "to": "BO-1093",
     "trigger": "Back to Funding Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Control the business rules governing individual wallet top-up transactions.",
  "purposeNote": "Every wallet top-up is evaluated against the applicable funding rules before value is credited.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Minimum top-up amount",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 15 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum top-up amount",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 15 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Allowed increments",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 15 §Configure"
      },
      {
       "kind": "textField",
       "label": "Maximum number of top-ups per day",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 15 §Configure"
      },
      {
       "kind": "textField",
       "label": "Maximum number per week/month",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 15 §Configure"
      },
      {
       "kind": "textField",
       "label": "Maximum daily funding value",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 15 §Configure"
      },
      {
       "kind": "textField",
       "label": "Maximum monthly funding value",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 15 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Wallet maximum-balance check",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 15 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Customer-specific limits",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 15 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Wallet-type-specific limits",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 15 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Currency-specific limits",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 15 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Channel-specific limits",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 15 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Venue-specific limits",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 15 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Funding-source restrictions",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 15 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Anonymous-wallet restrictions",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 15 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Membership-specific rules",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 15 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Corporate-wallet rules",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 15 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Promotional top-up rules",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 15 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Reject",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 15 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Warn",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 15 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Request approval",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 15 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Hold transaction",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 15 §Configure"
      },
      {
       "kind": "textField",
       "label": "Route for risk review",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 15 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The top-up rule configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the top-up rule untouched.",
   "emptyFirstRun": "No top-up rule configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setWalletFundingRules",
    "contract": "wallet",
    "purpose": "Amounts, presets and bonus rules",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getWalletFundingRules"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1095",
   "workshopBoard": "wireframes/WS187 Wallet Configuration Backend Structure v1.0 Board 2.dc.html#bo-1095"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 15. 0 of 0 labels bound to a contract property; 23 of 27 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1096",
  "name": "Channel & Funding Source Mapping",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "2",
   "number": "04",
   "page": 16
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/channel-funding-source-mapping-bo-1096",
   "component": "apps/venue-management-web/src/routes/orders-money/ChannelFundingSourceMapping.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1093"
   ],
   "exitTo": [
    "BO-1093"
   ],
   "transitions": [
    {
     "to": "BO-1093",
     "trigger": "Back to Funding Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure funding availability across; Configure) and no display directory — it is settings, not a population",
  "purpose": "Determine where each funding method may be used.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "B2C Website",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 16 §Configure funding availability across"
      },
      {
       "kind": "selectField",
       "label": "Customer Mobile App",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 16 §Configure funding availability across"
      },
      {
       "kind": "selectField",
       "label": "POS",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 16 §Configure funding availability across"
      },
      {
       "kind": "selectField",
       "label": "Mobile POS",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 16 §Configure funding availability across"
      },
      {
       "kind": "selectField",
       "label": "Kiosk",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 16 §Configure funding availability across"
      },
      {
       "kind": "selectField",
       "label": "Guest Services",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 16 §Configure funding availability across"
      },
      {
       "kind": "selectField",
       "label": "Call Center",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 16 §Configure funding availability across"
      },
      {
       "kind": "selectField",
       "label": "Back Office",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 16 §Configure funding availability across"
      },
      {
       "kind": "selectField",
       "label": "Corporate Portal",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 16 §Configure funding availability across"
      },
      {
       "kind": "selectField",
       "label": "Partner/Reseller",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 16 §Configure funding availability across"
      },
      {
       "kind": "selectField",
       "label": "API",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 16 §Configure funding availability across"
      },
      {
       "kind": "selectField",
       "label": "Third-party systems",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 16 §Configure funding availability across"
      },
      {
       "kind": "selectField",
       "label": "Channel eligibility",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 16 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Wallet type",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 16 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Credit type generated",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 16 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Funding limits",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 16 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Authentication requirements",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 16 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Applicable venue",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 16 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Applicable customer type",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 16 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Effective dates",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 16 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The channel funding source configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the channel funding source untouched.",
   "emptyFirstRun": "No channel funding source configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setWalletFundingRules",
    "contract": "wallet",
    "purpose": "Channel and funding-source mapping",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getWalletFundingRules"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1096",
   "workshopBoard": "wireframes/WS187 Wallet Configuration Backend Structure v1.0 Board 2.dc.html#bo-1096"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 16. 0 of 0 labels bound to a contract property; 20 of 26 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1097",
  "name": "Auto-Reload Configuration",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "2",
   "number": "05",
   "page": 17
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/auto-reload-configuration-bo-1097",
   "component": "apps/venue-management-web/src/routes/orders-money/AutoReloadConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1093"
   ],
   "exitTo": [
    "BO-1093"
   ],
   "transitions": [
    {
     "to": "BO-1093",
     "trigger": "Back to Funding Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure automatic wallet replenishment when balances fall below predefined thresholds. The attached scope specifically requires automatic top-up when a wallet balance falls below a configurable threshold.",
  "purposeNote": "Auto-reload occurs only after the configured threshold is reached and all consent, payment, security and funding-limit validations have passed.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Trigger Balance",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 17 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Eligible wallet types",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 17 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Eligible credit types",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 17 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Reload amount",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 17 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum reload amount",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 17 §Configure"
      },
      {
       "kind": "textField",
       "label": "Maximum auto-reloads per day",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 17 §Configure"
      },
      {
       "kind": "textField",
       "label": "Maximum auto-reloads per month",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 17 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Payment method",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 17 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Stored payment instrument",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 17 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Customer consent required",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 17 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Consent validity",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 17 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Failed payment behavior",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 17 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Retry rules",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 17 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum retries",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 17 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Notification rules",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 17 §Configure"
      },
      {
       "kind": "textField",
       "label": "Suspension after repeated failure",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 17 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Funding limits",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 17 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Effective dates",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 17 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The auto-reload configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the auto-reload untouched.",
   "emptyFirstRun": "No auto-reload configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setWalletFundingRules",
    "contract": "wallet",
    "purpose": "Auto-reload on a threshold",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getWalletFundingRules"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1097",
   "workshopBoard": "wireframes/WS187 Wallet Configuration Backend Structure v1.0 Board 2.dc.html#bo-1097"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 17. 0 of 0 labels bound to a contract property; 18 of 27 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1098",
  "name": "Recurring Funding Schedule",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "2",
   "number": "06",
   "page": 17
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/recurring-funding-schedule-bo-1098",
   "component": "apps/venue-management-web/src/routes/orders-money/RecurringFundingSchedule.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1093"
   ],
   "exitTo": [
    "BO-1093"
   ],
   "transitions": [
    {
     "to": "BO-1093",
     "trigger": "Back to Funding Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure scheduled wallet funding independent of the wallet's current balance. The source specifically requires scheduled or recurring top-ups based on date, frequency, amount, payment method and customer authorization.",
  "purposeNote": "and authorization requirements.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Schedule name",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 17 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Source wallet/payment method",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 17 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Destination wallet",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 17 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Amount",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 17 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Credit type",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 17 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Start date",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 17 §Configure"
      },
      {
       "kind": "selectField",
       "label": "End date",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 17 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Frequency",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 17 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Execution time",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 17 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum occurrences",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 17 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Funding limits",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 17 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Customer authorization",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 17 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Retry policy",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 17 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Failure behavior",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 17 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Notification rules",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 17 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Pause/resume",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 17 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Cancellation",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 17 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Specific day of month",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 17 §Support schedules such as"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The recurring funding schedule configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the recurring funding schedule untouched.",
   "emptyFirstRun": "No recurring funding schedule configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setWalletFundingRules",
    "contract": "wallet",
    "purpose": "Recurring funding on a date",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getWalletFundingRules"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1098",
   "workshopBoard": "wireframes/WS187 Wallet Configuration Backend Structure v1.0 Board 2.dc.html#bo-1098"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 17. 0 of 0 labels bound to a contract property; 18 of 29 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Specific day of month are choices sent by `setWalletFundingRules` (recurringFunding.dayOfMonth).",
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
  "id": "BO-1099",
  "name": "Funding Authorization & Approval Rules",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "2",
   "number": "07",
   "page": 18
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/funding-authorization-approval-rules-bo-1099",
   "component": "apps/venue-management-web/src/routes/orders-money/FundingAuthorizationApprovalRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1093"
   ],
   "exitTo": [
    "BO-1093"
   ],
   "transitions": [
    {
     "to": "BO-1093",
     "trigger": "Back to Funding Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure approval based on; Configure) and no display directory — it is settings, not a population",
  "purpose": "Apply governance and approval controls to wallet funding operations.",
  "purposeNote": "Funding transactions requiring approval cannot alter the wallet balance until all configured authorization requirements are satisfied.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Funding amount",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 18 §Configure approval based on"
      },
      {
       "kind": "selectField",
       "label": "Funding method",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 18 §Configure approval based on"
      },
      {
       "kind": "selectField",
       "label": "Wallet type",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 18 §Configure approval based on"
      },
      {
       "kind": "selectField",
       "label": "Customer type",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 18 §Configure approval based on"
      },
      {
       "kind": "selectField",
       "label": "Channel",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 18 §Configure approval based on"
      },
      {
       "kind": "selectField",
       "label": "Credit type",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 18 §Configure approval based on"
      },
      {
       "kind": "selectField",
       "label": "Administrative user",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 18 §Configure approval based on"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 18 §Configure approval based on"
      },
      {
       "kind": "selectField",
       "label": "Tenant",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 18 §Configure approval based on"
      },
      {
       "kind": "selectField",
       "label": "Risk score",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 18 §Configure approval based on"
      },
      {
       "kind": "selectField",
       "label": "Single approval",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 18 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Multi-level approval",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 18 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maker-checker control",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 18 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Role-based approval",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 18 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Amount threshold",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 18 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Approval SLA",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 18 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Escalation",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 18 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Auto-rejection after expiry",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 18 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Mandatory reason",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 18 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Supporting documentation",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 18 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Approval notifications",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 18 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The funding authorization approval configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the funding authorization approval untouched.",
   "emptyFirstRun": "No funding authorization approval configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setWalletFundingRules",
    "contract": "wallet",
    "purpose": "Approval above a threshold",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getWalletFundingRules"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1099",
   "workshopBoard": "wireframes/WS187 Wallet Configuration Backend Structure v1.0 Board 2.dc.html#bo-1099"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 18. 0 of 0 labels bound to a contract property; 21 of 31 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1100",
  "name": "Funding Reversal & Correction Management",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "2",
   "number": "08",
   "page": 19
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/funding-reversal-correction-management-bo-1100",
   "component": "apps/venue-management-web/src/routes/orders-money/FundingReversalCorrectionManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1093"
   ],
   "exitTo": [
    "BO-1093"
   ],
   "transitions": [
    {
     "to": "BO-1093",
     "trigger": "Back to Funding Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "subjectId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Provide controlled correction of incorrectly funded wallet transactions without deleting financial history.",
  "purposeNote": "Every funding correction creates a traceable compensating transaction while preserving the original transaction and complete audit history.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Eligible transaction status",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 19 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum reversal period",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 19 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Full/partial reversal permission",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 19 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Required reason code",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 19 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Required notes",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 19 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Approval threshold",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 19 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maker-checker requirement",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 19 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Original funding reference",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 19 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Related payment reference",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 19 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Financial posting requirement",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 19 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Customer notification",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 19 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Credit expiry impact",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 19 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Full reversal",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 19 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Partial reversal",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 19 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Duplicate top-up correction",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 19 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Failed funding correction",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 19 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Payment reversal",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 19 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The funding reversal correction configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the funding reversal correction untouched.",
   "emptyFirstRun": "No funding reversal correction configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "reverseWalletFunding",
    "contract": "wallet",
    "purpose": "Reverse or correct a top-up",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listWalletTransactions",
     "listCreditLots"
    ]
   },
   {
    "operationId": "adjustWallet",
    "contract": "wallet",
    "purpose": "Credit a top-up that was paid but never reached the wallet",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration): serves the pack action(s) Failed funding correction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "subjectId",
     "from": "navigation"
    }
   ],
   "coldEntry": "Opened from BO-1093 with the wallet holder picked there. Opened cold (a bookmark or a refresh), it shows the list to pick from rather than an empty record, and says plainly if the wallet holder no longer exists."
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1100",
   "workshopBoard": "wireframes/WS187 Wallet Configuration Backend Structure v1.0 Board 2.dc.html#bo-1100"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 19. 0 of 0 labels bound to a contract property; 17 of 27 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Full reversal, Partial reversal, Duplicate top-up correction, Payment reversal are choices sent by `reverseWalletFunding` (amount (full/partial), kind duplicate|chargeback|error); Failed funding correction: `adjustWallet`.",
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
  "id": "BO-1101",
  "name": "Funding Limits & Velocity Controls",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "2",
   "number": "09",
   "page": 20
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/funding-limits-velocity-controls-bo-1101",
   "component": "apps/venue-management-web/src/routes/orders-money/FundingLimitsVelocityControls.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1093"
   ],
   "exitTo": [
    "BO-1093"
   ],
   "transitions": [
    {
     "to": "BO-1093",
     "trigger": "Back to Funding Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Protect wallets against excessive or suspicious funding activity. The source specifically requires configurable maximum balance, daily top-up limit, single-transaction limit and user- specific limits.",
  "purposeNote": "Funding limits are evaluated in real time before wallet value is credited, with configurable actions for violations.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Balance Limits",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 20 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum wallet balance",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 20 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum credit-type balance",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 20 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Transaction Limits",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 20 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Minimum funding",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 20 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum single top-up",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 20 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Velocity Limits",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 20 §Configure"
      },
      {
       "kind": "textField",
       "label": "Maximum top-ups per hour",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 20 §Configure"
      },
      {
       "kind": "textField",
       "label": "Maximum top-ups per day",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 20 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum daily amount",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 20 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum weekly amount",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 20 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum monthly amount",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 20 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Source Limits",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 20 §Configure"
      },
      {
       "kind": "textField",
       "label": "Maximum per payment instrument",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 20 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum cash funding",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 20 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum gift-card conversion",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 20 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum promotional funding",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 20 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Customer Limits",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 20 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Individual",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 20 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Child",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 20 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Family",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 20 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Corporate",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 20 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Employee",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 20 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Guest",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 20 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Allow",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 20 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Warn",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 20 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Decline",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 20 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Hold",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 20 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Require MFA",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 20 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Require approval",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 20 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The funding limits velocity configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the funding limits velocity untouched.",
   "emptyFirstRun": "No funding limits velocity configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setWalletFundingRules",
    "contract": "wallet",
    "purpose": "Limits and velocity controls",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getWalletFundingRules"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1101",
   "workshopBoard": "wireframes/WS187 Wallet Configuration Backend Structure v1.0 Board 2.dc.html#bo-1101"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 20. 0 of 0 labels bound to a contract property; 32 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1102",
  "name": "Funding Transaction Audit & Reconciliation",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "2",
   "number": "10",
   "page": 21
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/funding-transaction-audit-reconciliation-bo-1102",
   "component": "apps/venue-management-web/src/routes/orders-money/FundingTransactionAuditReconciliation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1093"
   ],
   "exitTo": [
    "BO-1093"
   ],
   "transitions": [
    {
     "to": "BO-1093",
     "trigger": "Back to Funding Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "subjectId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide a complete administrative record of every value entering a wallet. The source requires a complete audit trail for wallet top-ups, payments, refunds, transfers, adjustments, expirations, reversals and administrative actions. Configure the intelligence behind the TICVAI wallet balance: what types of value can be stored, where each credit can be spent, when it expires, which balance is consumed first, how FEFO operates, and how credits behave across Ticketing, F&B, Retail, Attractions, Parking, Membership and other TICVAI services. This board directly addresses requirements including multiple credit types, configurable expiry, usage criteria, FEFO consumption, stored-value balances, membership-related credits, and wallet reporting.",
  "purposeNote": "Every wallet funding transaction is traceable from its originating funding/payment event through the wallet ledger, with discrepancies clearly identified and no financial transaction removable from audit history. Board 2 Flow",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 21"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 21"
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
       "label": "Payment succeeded but wallet not funded",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 21 §Allow administrators to identify"
      },
      {
       "kind": "secondaryButton",
       "label": "Wallet funded but payment unresolved",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 21 §Allow administrators to identify"
      },
      {
       "kind": "secondaryButton",
       "label": "Duplicate funding",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 21 §Allow administrators to identify"
      },
      {
       "kind": "secondaryButton",
       "label": "Missing external reference",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 21 §Allow administrators to identify"
      },
      {
       "kind": "secondaryButton",
       "label": "Unreconciled transaction",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 21 §Allow administrators to identify"
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
   "loading": "The funding transaction audit list.",
   "error": "Could not load. Names which read failed and leaves the funding transaction audit untouched.",
   "emptyFirstRun": "No funding transaction audit yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the funding transaction audit are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listWalletTransactions",
    "contract": "wallet",
    "purpose": "The funding audit trail",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "getWalletReconciliation",
    "contract": "wallet",
    "purpose": "Against the acquirer and the ledger",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1102",
   "workshopBoard": "wireframes/WS187 Wallet Configuration Backend Structure v1.0 Board 2.dc.html#bo-1102"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 21. 0 of 0 labels bound to a contract property; 5 of 56 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Payment succeeded but wallet not funded, Wallet funded but payment unresolved, Duplicate funding, Missing external reference, Unreconciled transaction are choices sent by `getWalletReconciliation` (exception categories on the reconciliation result).",
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
 "getWalletFundingRules": {
  "method": "GET",
  "path": "/wallet-funding-rules",
  "contract": "wallet",
  "summary": "How a wallet may be topped up",
  "permission": "WALLET_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "WalletFundingRules"
 },
 "getWalletReconciliation": {
  "method": "GET",
  "path": "/wallet-reconciliation",
  "contract": "wallet",
  "summary": "The wallet sub-ledger against the general ledger and the acquirer",
  "permission": "WALLET_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "tenant",
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
   }
  ],
  "requestBody": null,
  "responds": "WalletReconciliation"
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
   }
  ],
  "requestBody": null,
  "responds": "Page"
 },
 "reverseWalletFunding": {
  "method": "POST",
  "path": "/wallet-funding/reversals",
  "contract": "wallet",
  "summary": "Undo a top-up, in full or in part",
  "permission": "WALLET_OPERATE",
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
  "responds": "WalletAdjustment"
 },
 "setWalletFundingRules": {
  "method": "PUT",
  "path": "/wallet-funding-rules",
  "contract": "wallet",
  "summary": "Amounts, channels, bonuses, limits and velocity",
  "permission": "WALLET_CONFIGURE",
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
  "requestBody": "WalletFundingRules",
  "responds": "WalletFundingRules"
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
 "WalletAdjustment": {
  "type": "object",
  "x-ticvai-persistence": "wallet.adjustment",
  "description": "Board 7.7. **A correction, distinguishable from a spend.**",
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
     "reversal",
     "chargeback",
     "goodwill",
     "correction",
     "writeOff"
    ]
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "affectedLotIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "reason": {
    "type": "string"
   },
   "performedBy": {
    "type": "string",
    "format": "uuid"
   },
   "approvedBy": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "at": {
    "type": "string",
    "format": "date-time"
   },
   "scopePath": {
    "type": "string"
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
 "WalletReconciliation": {
  "type": "object",
  "description": "Board 9.4. **Three sources, and the exception names which pair disagrees.**",
  "properties": {
   "from": {
    "type": "string",
    "format": "date"
   },
   "to": {
    "type": "string",
    "format": "date"
   },
   "subLedgerTotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "generalLedgerTotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "acquirerTotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "exceptions": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "pair": {
       "type": "string",
       "enum": [
        "subLedgerVsGeneralLedger",
        "subLedgerVsAcquirer",
        "generalLedgerVsAcquirer"
       ]
      },
      "difference": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "transactionIds": {
       "type": "array",
       "items": {
        "type": "string",
        "format": "uuid"
       }
      },
      "likelyCause": {
       "type": "string",
       "nullable": true
      }
     }
    }
   }
  }
 }
}
```
