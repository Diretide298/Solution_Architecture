# WS191 — Wallet Configuration Backend Structure v1.0 board 6

**10 screens · 6 operations · 9 schemas · 4 permissions**

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
  `PAYMENT_VIEW, WALLET_CONFIGURE, WALLET_OPERATE, WALLET_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-1133` | Wallet Usage & Channel Command Center | listDetail | 1 | 0 | — |
| `BO-1134` | Wallet Channel Configuration | configEditor | 1 | 0 | — |
| `BO-1135` | Wallet Payment & Redemption Policy | configEditor | 1 | 0 | — |
| `BO-1136` | Wearable & Credential Type Configuration | configEditor | 1 | 0 | — |
| `BO-1137` | Wearable Linking & Wallet Association Rules | configEditor | 1 | 0 | — |
| `BO-1138` | NFC, RFID & QR Interaction Rules | configEditor | 1 | 0 | — |
| `BO-1139` | Digital Key & Wallet Authentication Policy | configEditor | 2 | 0 | — |
| `BO-1140` | Offline Wallet & Degraded Mode Configuration | configEditor | 1 | 0 | — |
| `BO-1141` | Device, Terminal & Acceptance Point Mapping | configEditor | 2 | 0 | — |
| `BO-1142` | Wallet Transaction Simulator, Monitoring & Channel Audit | listDetail | 2 | 0 | — |

## Thin screens in this batch

**BO-1142 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-1133",
  "name": "Wallet Usage & Channel Command Center",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "6",
   "number": "01",
   "page": 62
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/wallet-usage-channel-command-center-bo-1133",
   "component": "apps/venue-management-web/src/routes/orders-money/WalletUsageChannelCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-1134",
    "BO-1135",
    "BO-1136",
    "BO-1137",
    "BO-1138",
    "BO-1139",
    "BO-1140",
    "BO-1141",
    "BO-1142"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "BO-1134",
     "trigger": "Wallet Channel Configuration",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    },
    {
     "to": "BO-1135",
     "trigger": "Wallet Payment & Redemption Policy",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    },
    {
     "to": "BO-1136",
     "trigger": "Wearable & Credential Type Configuration",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    },
    {
     "to": "BO-1137",
     "trigger": "Wearable Linking & Wallet Association Rules",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    },
    {
     "to": "BO-1138",
     "trigger": "NFC, RFID & QR Interaction Rules",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    },
    {
     "to": "BO-1139",
     "trigger": "Digital Key & Wallet Authentication Policy",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    },
    {
     "to": "BO-1140",
     "trigger": "Offline Wallet & Degraded Mode Configuration",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    },
    {
     "to": "BO-1141",
     "trigger": "Device, Terminal & Acceptance Point Mapping",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    },
    {
     "to": "BO-1142",
     "trigger": "Wallet Transaction Simulator, Monitoring & Channel Audit",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide a real-time operational view of wallet usage across all TICVAI channels and venue touchpoints. Dashboard KPIs",
  "purposeNote": "Authorized users can monitor wallet consumption across channels and drill down to individual wallet transactions and devices.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 62 §Display"
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
       "label": "Search wallet usage channel",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 62 §Filters"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Tenant",
        "Venue",
        "Channel",
        "Outlet",
        "Device",
        "Wallet type",
        "Credential type",
        "Transaction status",
        "Currency",
        "Date/time",
        "Operational Alerts"
       ],
       "notes": "The pack filters this screen by tenant, venue, channel, outlet, device, wallet type and 5 more — which are present is a decision the pack already made.",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 62 §Filters"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every wallet usage channel",
       "columns": [
        "Wallet Transactions Today",
        "Wallet Spend Today",
        "Online Wallet Spend",
        "Onsite Wallet Spend",
        "POS Transactions",
        "Mobile App Transactions",
        "Wearable Transactions",
        "QR Transactions",
        "NFC Transactions",
        "RFID Transactions",
        "Declined Wallet Transactions",
        "Offline Transactions",
        "Pending Synchronizations",
        "Usage by Business Area"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 62 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected wallet usage channel",
       "bindsTo": null,
       "columns": [
        "Wallet Transactions Today",
        "Wallet Spend Today",
        "Online Wallet Spend",
        "Onsite Wallet Spend",
        "POS Transactions",
        "Mobile App Transactions",
        "Wearable Transactions",
        "QR Transactions",
        "NFC Transactions",
        "RFID Transactions",
        "Declined Wallet Transactions",
        "Offline Transactions",
        "Pending Synchronizations",
        "Usage by Business Area"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Break down by”, “Highlight”.",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 62 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The wallet usage channel list.",
   "error": "Could not load. Names which read failed and leaves the wallet usage channel untouched.",
   "emptyFirstRun": "No wallet usage channel yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the wallet usage channel are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setWalletChannelRules",
    "contract": "wallet",
    "purpose": "Where wallets are accepted",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getWalletFundingRules"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "Wallet Transactions Today",
    "Wallet Spend Today",
    "Online Wallet Spend",
    "Onsite Wallet Spend",
    "POS Transactions",
    "Mobile App Transactions"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1133",
   "workshopBoard": "wireframes/WS191 Wallet Configuration Backend Structure v1.0 Board 6.dc.html#bo-1133"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 62. 0 of 25 labels bound to a contract property; 25 of 47 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1134",
  "name": "Wallet Channel Configuration",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "6",
   "number": "02",
   "page": 63
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/wallet-channel-configuration-bo-1134",
   "component": "apps/venue-management-web/src/routes/orders-money/WalletChannelConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1133"
   ],
   "exitTo": [
    "BO-1133"
   ],
   "transitions": [
    {
     "to": "BO-1133",
     "trigger": "Back to Wallet Usage & Channel Command Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Define which TICVAI channels can use Wallet as a payment or redemption method. Requirement 4.3.8 requires multiple wallet payment channels including mobile applications and wearables, with online, onsite POS and in-app payment modes. Supported Channels",
  "purposeNote": "Wallet capabilities are available only through explicitly configured and authorized channels.",
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
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 63 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Customer Mobile App",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 63 §Configure"
      },
      {
       "kind": "selectField",
       "label": "POS",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 63 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Mobile POS",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 63 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Kiosk",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 63 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Self-Service Terminal",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 63 §Configure"
      },
      {
       "kind": "selectField",
       "label": "F&B POS",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 63 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Retail POS",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 63 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Parking",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 63 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Attraction Terminal",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 63 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Access Device",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 63 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Customer Service",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 63 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Corporate Portal",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 63 §Configure"
      },
      {
       "kind": "selectField",
       "label": "B2B",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 63 §Configure"
      },
      {
       "kind": "selectField",
       "label": "API",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 63 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Third-party system",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 63 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Per Channel Configure",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 63 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Wallet payment enabled",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 63 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Balance inquiry enabled",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 63 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Voucher redemption",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 63 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Gift card redemption",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 63 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Refund-to-wallet",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 63 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Split tender",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 63 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Top-up",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 63 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Transfer",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 63 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Offline wallet usage",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 63 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Supported currencies",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 63 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Supported credit types",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 63 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum transaction",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 63 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Authentication requirement",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 63 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The wallet channel configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the wallet channel untouched.",
   "emptyFirstRun": "No wallet channel configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setWalletChannelRules",
    "contract": "wallet",
    "purpose": "Channel configuration",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getWalletFundingRules"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1134",
   "workshopBoard": "wireframes/WS191 Wallet Configuration Backend Structure v1.0 Board 6.dc.html#bo-1134"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 63. 0 of 0 labels bound to a contract property; 32 of 38 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1135",
  "name": "Wallet Payment & Redemption Policy",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "6",
   "number": "03",
   "page": 64
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/wallet-payment-redemption-policy-bo-1135",
   "component": "apps/venue-management-web/src/routes/orders-money/WalletPaymentRedemptionPolicy.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1133"
   ],
   "exitTo": [
    "BO-1133"
   ],
   "transitions": [
    {
     "to": "BO-1133",
     "trigger": "Back to Wallet Usage & Channel Command Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure; Whereas another venue could configure) and no display directory — it is settings, not a population",
  "purpose": "Configure the business rules applied when a customer selects Wallet at checkout.",
  "purposeNote": "Every wallet payment follows the applicable published transaction and redemption policy.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Wallet payment enabled",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 64 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Full wallet payment",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 64 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Partial wallet payment",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 64 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Split tender",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 64 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Minimum wallet contribution",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 64 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum wallet contribution",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 64 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum transaction value",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 64 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Minimum remaining balance",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 64 §Configure"
      },
      {
       "kind": "textField",
       "label": "Negative balance allowed/not allowed",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 64 §Configure"
      },
      {
       "kind": "selectField",
       "label": "External tender fallback",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 64 §Configure"
      },
      {
       "kind": "selectField",
       "label": "PIN requirement",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 64 §Configure"
      },
      {
       "kind": "selectField",
       "label": "MFA requirement",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 64 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Customer confirmation",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 64 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Receipt requirement",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 64 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Transaction Types",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 64 §Configure"
      },
      {
       "kind": "textField",
       "label": "Partial wallet payment = Not Allowed",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 64 §Whereas another venue could configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The wallet payment redemption configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the wallet payment redemption untouched.",
   "emptyFirstRun": "No wallet payment redemption configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setWalletChannelRules",
    "contract": "wallet",
    "purpose": "Payment and redemption policy",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getWalletFundingRules"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1135",
   "workshopBoard": "wireframes/WS191 Wallet Configuration Backend Structure v1.0 Board 6.dc.html#bo-1135"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 64. 0 of 0 labels bound to a contract property; 16 of 34 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1136",
  "name": "Wearable & Credential Type Configuration",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "6",
   "number": "04",
   "page": 65
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/wearable-credential-type-configuration-bo-1136",
   "component": "apps/venue-management-web/src/routes/orders-money/WearableCredentialTypeConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1133"
   ],
   "exitTo": [
    "BO-1133"
   ],
   "transitions": [
    {
     "to": "BO-1133",
     "trigger": "Back to Wallet Usage & Channel Command Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Define physical and digital credentials that can represent a wallet. The source requires venue-provided wearables to be linked to digital wallets and used to make payments. Credential Types",
  "purposeNote": "Administrators can introduce and govern wallet credentials independently from the wallet account itself.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Credential name",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 65 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Internal code",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 65 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Technology",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 65 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Identifier format",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 65 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Tokenization",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 65 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Encryption requirement",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 65 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Wallet linking allowed",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 65 §Configure"
      },
      {
       "kind": "textField",
       "label": "Multiple credentials per wallet",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 65 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Credential sharing permitted",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 65 §Configure"
      },
      {
       "kind": "selectField",
       "label": "PIN required",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 65 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Customer verification",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 65 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Activation",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 65 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Expiry",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 65 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Replacement",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 65 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Lost/stolen handling",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 65 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Offline eligibility",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 65 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Applicable venue",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 65 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Applicable device types",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 65 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "RFID Card",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 65 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "NFC Card",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 65 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Mobile Wallet Credential",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 65 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Digital Key",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 65 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Hotel Key",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 65 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Event Badge",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 65 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The wearable credential type configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the wearable credential type untouched.",
   "emptyFirstRun": "No wearable credential type configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setWalletChannelRules",
    "contract": "wallet",
    "purpose": "Credential kinds accepted",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getWalletFundingRules"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1136",
   "workshopBoard": "wireframes/WS191 Wallet Configuration Backend Structure v1.0 Board 6.dc.html#bo-1136"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 65. 0 of 0 labels bound to a contract property; 24 of 34 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** RFID Card, NFC Card, Mobile Wallet Credential, Digital Key are choices sent by `setWalletChannelRules` (allowedCredentialKinds rfid|nfc|mobileApp|digitalKey); Hotel Key, Event Badge are choices sent by `setWalletChannelRules` (field gap: extend credential kind enum with hotelKey|eventBadge).",
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
  "id": "BO-1137",
  "name": "Wearable Linking & Wallet Association Rules",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "6",
   "number": "05",
   "page": 66
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/wearable-linking-wallet-association-rules-bo-1137",
   "component": "apps/venue-management-web/src/routes/orders-money/WearableLinkingWalletAssociationRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1133"
   ],
   "exitTo": [
    "BO-1133"
   ],
   "transitions": [
    {
     "to": "BO-1133",
     "trigger": "Back to Wallet Usage & Channel Command Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure how wristbands, cards and other credentials are linked to wallet accounts. Requirement 4.3.12 specifically requires guests to link and remove venue-issued wearables from their wallet. Linking Methods Customer Mobile App B2C Portal POS Guest Services Kiosk Hotel Check-In Event Registration Administrative Backend API",
  "purposeNote": "Credentials can be securely linked, removed or replaced without modifying the underlying wallet balance or ledger.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Wallet type eligibility",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 66 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Credential type",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 66 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Customer verification",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 66 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Activation code",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 66 §Configure"
      },
      {
       "kind": "selectField",
       "label": "PIN verification",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 66 §Configure"
      },
      {
       "kind": "selectField",
       "label": "OTP verification",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 66 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Digital ID verification",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 66 §Configure"
      },
      {
       "kind": "textField",
       "label": "Maximum credentials per wallet",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 66 §Configure"
      },
      {
       "kind": "textField",
       "label": "Maximum wallets per credential",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 66 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Automatic activation",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 66 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Manual approval",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 66 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Effective date",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 66 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Expiry",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 66 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Credential Lifecycle",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 66 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Administrative Actions",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 66 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Link",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 66 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Unlink",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 66 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Suspend",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 66 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Reactivate",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 66 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Replace",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 66 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Transfer",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 66 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Mark Lost",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 66 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Mark Stolen",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 66 §Configure"
      },
      {
       "kind": "selectField",
       "label": "View Usage",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 66 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The wearable linking wallet configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the wearable linking wallet untouched.",
   "emptyFirstRun": "No wearable linking wallet configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "linkWalletCredential",
    "contract": "wallet",
    "purpose": "Bind a wearable to a wallet",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getWallet"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1137",
   "workshopBoard": "wireframes/WS191 Wallet Configuration Backend Structure v1.0 Board 6.dc.html#bo-1137"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 66. 0 of 0 labels bound to a contract property; 24 of 44 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1138",
  "name": "NFC, RFID & QR Interaction Rules",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "6",
   "number": "06",
   "page": 67
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/nfc-rfid-qr-interaction-rules-bo-1138",
   "component": "apps/venue-management-web/src/routes/orders-money/NfcRfidQrInteractionRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1133"
   ],
   "exitTo": [
    "BO-1133"
   ],
   "transitions": [
    {
     "to": "BO-1133",
     "trigger": "Back to Wallet Usage & Channel Command Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure how different proximity/contactless technologies interact with TICVAI Wallet. Requirement 4.3.13 specifically requires wallet payments using RFID, NFC and QR code. Configure by Technology RFID Reader type Card/wristband format Identifier validation Offline support NFC Token validation Device authentication Tap behavior Secure token requirements QR Static QR Dynamic QR QR validity period Single-use token Refresh frequency Screenshot protection controls where supported Interaction Types",
  "purposeNote": "All supported proximity interactions resolve securely to the correct wallet and enforce the applicable wallet policy.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Tap to Pay",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 67 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Scan to Pay",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 67 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Tap to Redeem",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 67 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Scan to Redeem",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 67 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Balance Check",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 67 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Attraction Entry",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 67 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Ride Redemption",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 67 §Configure"
      },
      {
       "kind": "selectField",
       "label": "F&B Purchase",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 67 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Retail Purchase",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 67 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Parking",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 67 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Transaction Feedback",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 67 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The nfc rfid interaction configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the nfc rfid interaction untouched.",
   "emptyFirstRun": "No nfc rfid interaction configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setWalletChannelRules",
    "contract": "wallet",
    "purpose": "NFC, RFID and QR rules",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getWalletFundingRules"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1138",
   "workshopBoard": "wireframes/WS191 Wallet Configuration Backend Structure v1.0 Board 6.dc.html#bo-1138"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 67. 0 of 0 labels bound to a contract property; 11 of 45 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1139",
  "name": "Digital Key & Wallet Authentication Policy",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "6",
   "number": "07",
   "page": 68
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/digital-key-wallet-authentication-policy-bo-1139",
   "component": "apps/venue-management-web/src/routes/orders-money/DigitalKeyWalletAuthenticationPolicy.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1133"
   ],
   "exitTo": [
    "BO-1133"
   ],
   "transitions": [
    {
     "to": "BO-1133",
     "trigger": "Back to Wallet Usage & Channel Command Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure based on) and no display directory — it is settings, not a population",
  "purpose": "Configure authentication requirements based on transaction risk. Requirement 4.3.10 specifically calls for Digital Key/Digital ID authentication wherever possible to enhance security and credential management. Authentication Methods",
  "purposeNote": "published risk rules.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Transaction amount",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 68 §Configure based on"
      },
      {
       "kind": "selectField",
       "label": "Credit type",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 68 §Configure based on"
      },
      {
       "kind": "selectField",
       "label": "Customer",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 68 §Configure based on"
      },
      {
       "kind": "selectField",
       "label": "Wallet type",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 68 §Configure based on"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 68 §Configure based on"
      },
      {
       "kind": "selectField",
       "label": "Channel",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 68 §Configure based on"
      },
      {
       "kind": "selectField",
       "label": "Credential",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 68 §Configure based on"
      },
      {
       "kind": "selectField",
       "label": "Risk score",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 68 §Configure based on"
      },
      {
       "kind": "selectField",
       "label": "Transaction velocity",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 68 §Configure based on"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Wallet PIN",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 68 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Device authentication",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 68 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Digital Key",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 68 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Customer login",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 68 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Membership credential",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 68 §Support"
      },
      {
       "kind": "primaryButton",
       "label": "Save authentication policy",
       "operation": "setWalletAuthenticationPolicy",
       "provenance": "contract wallet.yaml PUT /wallet-authentication-policy (decided 29 September, VM close-out)"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The digital key wallet configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the digital key wallet untouched.",
   "emptyFirstRun": "No digital key wallet configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setWalletChannelRules",
    "contract": "wallet",
    "purpose": "Authentication and PIN policy",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getWalletFundingRules"
    ]
   },
   {
    "operationId": "setWalletAuthenticationPolicy",
    "contract": "wallet",
    "purpose": "Save authentication policy",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1139",
   "workshopBoard": "wireframes/WS191 Wallet Configuration Backend Structure v1.0 Board 6.dc.html#bo-1139"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 68. 0 of 0 labels bound to a contract property; 14 of 33 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** still owed by a contract change: `setWalletAuthenticationPolicy`.",
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
  "id": "BO-1140",
  "name": "Offline Wallet & Degraded Mode Configuration",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "6",
   "number": "08",
   "page": 69
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/offline-wallet-degraded-mode-configuration-bo-1140",
   "component": "apps/venue-management-web/src/routes/orders-money/OfflineWalletDegradedModeConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1133"
   ],
   "exitTo": [
    "BO-1133"
   ],
   "transitions": [
    {
     "to": "BO-1133",
     "trigger": "Back to Wallet Usage & Channel Command Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure by; Configure) and no display directory — it is settings, not a population",
  "purpose": "Maintain controlled venue operations during temporary network or service interruptions. This is especially important for amusement parks, festivals, stadiums and large attractions where wristband transactions cannot simply stop because connectivity is temporarily unavailable. Offline Eligibility",
  "purposeNote": "Offline wallet usage remains within configured exposure limits, and all transactions synchronize and reconcile after connectivity restoration.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 69 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Outlet",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 69 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Device",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 69 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Credential",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 69 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Wallet type",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 69 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Credit type",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 69 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Transaction type",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 69 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Offline Controls",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 69 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Offline wallet enabled",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 69 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum offline transaction",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 69 §Configure"
      },
      {
       "kind": "textField",
       "label": "Maximum cumulative offline spend",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 69 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum transactions",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 69 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Offline duration",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 69 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Cached balance permitted",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 69 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Reserved offline allowance",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 69 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Credential whitelist",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 69 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Risk profile",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 69 §Configure"
      },
      {
       "kind": "textField",
       "label": "Expiry of cached data",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 69 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Device storage requirements",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 69 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Example",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 69 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The offline wallet degraded configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the offline wallet degraded untouched.",
   "emptyFirstRun": "No offline wallet degraded configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setWalletChannelRules",
    "contract": "wallet",
    "purpose": "Offline and degraded mode",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getWalletFundingRules"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1140",
   "workshopBoard": "wireframes/WS191 Wallet Configuration Backend Structure v1.0 Board 6.dc.html#bo-1140"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 69. 0 of 0 labels bound to a contract property; 20 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1141",
  "name": "Device, Terminal & Acceptance Point Mapping",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "6",
   "number": "09",
   "page": 70
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/device-terminal-acceptance-point-mapping-bo-1141",
   "component": "apps/venue-management-web/src/routes/orders-money/DeviceTerminalAcceptancePointMapping.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1133"
   ],
   "exitTo": [
    "BO-1133"
   ],
   "transitions": [
    {
     "to": "BO-1133",
     "trigger": "Back to Wallet Usage & Channel Command Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Determine exactly which devices and locations are authorized to accept TICVAI Wallet. Hierarchy Tenant → Venue → Business Area → Outlet / Attraction → Terminal → Device Acceptance Points",
  "purposeNote": "Only registered and authorized acceptance points can initiate wallet payment or redemption requests.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Device ID",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 70 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Device type",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 70 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 70 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Outlet",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 70 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Business function",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 70 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Wallet enabled",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 70 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Supported credentials",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 70 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Supported credit types",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 70 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum transaction",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 70 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Offline permission",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 70 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Device risk profile",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 70 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Authentication policy",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 70 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Operating hours",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 70 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Device status",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 70 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The device terminal acceptance configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the device terminal acceptance untouched.",
   "emptyFirstRun": "No device terminal acceptance configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "listPaymentTerminals",
    "contract": "payments",
    "purpose": "Terminals and acceptance points",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "setWalletChannelRules",
    "contract": "wallet",
    "purpose": "Map acceptance points",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getWalletFundingRules"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1141",
   "workshopBoard": "wireframes/WS191 Wallet Configuration Backend Structure v1.0 Board 6.dc.html#bo-1141"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 70. 0 of 0 labels bound to a contract property; 14 of 43 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1142",
  "name": "Wallet Transaction Simulator, Monitoring & Channel Audit",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "6",
   "number": "10",
   "page": 71
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/wallet-transaction-simulator-monitoring-channel-audit-bo-1142",
   "component": "apps/venue-management-web/src/routes/orders-money/WalletTransactionSimulatorMonitoringChannelAudit.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1133"
   ],
   "exitTo": [
    "BO-1133"
   ],
   "transitions": [
    {
     "to": "BO-1133",
     "trigger": "Back to Wallet Usage & Channel Command Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Test the complete channel-to-wallet transaction flow before configuration is published. Simulation Scenario Customer: Family Member / Child Wallet: Family Wallet Credential: RFID Wristband #CH-0045 Venue: Theme Park Device: F&B POS #12 Purchase: AED 85 TICVAI Evaluation Credential Active → PASS Credential Linked → PASS Device Authorized → PASS Channel Wallet Enabled → PASS F&B Credit Eligible → PASS Member Spending Permission → PASS Daily Limit → PASS Authentication Requirement → PASS Connectivity → ONLINE Consumption Meal Credit → AED 30 Bonus Credit → AED 20 Cash Credit → AED 35 Transaction Approved: AED 85 Remaining wallet balances displayed. Alternative Failure Scenario Configure the complete operational lifecycle of wallet value after it has been funded or issued— including peer-to-peer transfers, refund-to-wallet, reversals, balance adjustments, blocking/freezing, disputes, corrections, exception handling and governed administrative actions. This board directly addresses requirements 4.3.15, 4.3.16, 4.3.21 and 4.3.35, while complementing the family/corporate internal allocation capabilities already configured in Board 4.",
  "purposeNote": "Administrators can simulate wallet transactions end-to-end before publication, and every real transaction remains traceable from the acceptance device through credential resolution, authorization, consumption and wallet ledger posting. Board 6 — Backend Transaction Flow This is the important architecture to follow: Customer / Family Member → Credential RFID / NFC / QR / Mobile / Digital Key → Acceptance Point POS / Kiosk / Ride / F&B / Retail / Parking / App / B2C → Credential Resolution → Wallet Identification → Channel Policy → Member Permission → Authentication / Risk Check → Credit Eligibi",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 71"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 71"
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
       "impliedBy": "simulateCreditConsumption",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listWalletTransactions",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "simulateCreditConsumption"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The wallet transaction simulator list.",
   "error": "Could not load. Names which read failed and leaves the wallet transaction simulator untouched.",
   "emptyFirstRun": "No wallet transaction simulator yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the wallet transaction simulator are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "simulateCreditConsumption",
    "contract": "wallet",
    "purpose": "Simulate a wallet transaction",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listWalletTransactions",
    "contract": "wallet",
    "purpose": "Monitor and audit",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1142",
   "workshopBoard": "wireframes/WS191 Wallet Configuration Backend Structure v1.0 Board 6.dc.html#bo-1142"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 71. 0 of 0 labels bound to a contract property; 0 of 95 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "linkWalletCredential": {
  "method": "POST",
  "path": "/wallet-credentials",
  "contract": "wallet",
  "summary": "Bind a wristband, card or device to a wallet",
  "permission": "WALLET_OPERATE",
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
  "requestBody": "WalletCredential",
  "responds": "WalletCredential"
 },
 "listPaymentTerminals": {
  "method": "GET",
  "path": "/payment-terminals",
  "contract": "payments",
  "summary": "Terminals, and the payment configuration on each",
  "permission": "PAYMENT_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "venueId",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "PaymentTerminal"
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
 "setWalletAuthenticationPolicy": {
  "method": "PUT",
  "path": "/wallet-authentication-policy",
  "contract": "wallet",
  "summary": "Which proof of identity a wallet spend needs, by amount, channel and kind",
  "permission": "WALLET_CONFIGURE",
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
  "requestBody": "WalletAuthenticationPolicy",
  "responds": "WalletAuthenticationPolicy"
 },
 "setWalletChannelRules": {
  "method": "PUT",
  "path": "/wallet-channel-rules",
  "contract": "wallet",
  "summary": "Where a wallet may be used, on what, and when it may not",
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
  "requestBody": "WalletChannelRules",
  "responds": "WalletChannelRules"
 },
 "simulateCreditConsumption": {
  "method": "POST",
  "path": "/credit-consumption/simulate",
  "contract": "wallet",
  "summary": "Which credit this purchase would actually use",
  "permission": "WALLET_VIEW",
  "offlineCapable": null,
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
  "responds": "CreditAllocation"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "CreditAllocation": {
  "type": "object",
  "description": "Board 3.10. **Which lots this purchase would draw on**, in order.",
  "properties": {
   "requested": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "covered": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "shortfall": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "lines": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "lotId": {
       "type": "string",
       "format": "uuid"
      },
      "creditTypeId": {
       "type": "string",
       "format": "uuid"
      },
      "creditTypeName": {
       "type": "string"
      },
      "amount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "expiresAt": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      },
      "reason": {
       "type": "string"
      }
     }
    }
   },
   "rejected": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "creditTypeId": {
       "type": "string",
       "format": "uuid"
      },
      "reason": {
       "type": "string",
       "enum": [
        "notEligibleHere",
        "notEligibleForProduct",
        "expired",
        "basketCapReached",
        "restricted"
       ]
      }
     }
    }
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
 "PaymentTerminal": {
  "type": "object",
  "x-ticvai-persistence": "payments.terminal",
  "description": "Board 3. **The payment layer on a `tenancy` device**, not a second device register.",
  "required": [
   "deviceId"
  ],
  "properties": {
   "deviceId": {
    "type": "string",
    "format": "uuid",
    "description": "The `tenancy.RegisteredDevice`. **Enrolment, credentials, firmware and tamper state live there.**"
   },
   "merchantAccountId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "acquirerConnectionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "terminalIdentifier": {
    "type": "string",
    "nullable": true
   },
   "emvConfigurationVersion": {
    "type": "string",
    "nullable": true
   },
   "terminalModelCode": {
    "type": "string",
    "nullable": true,
    "description": "4.3.1. The model whose EMV and PCI certification applies (`listPaymentTerminalCertifications`)."
   },
   "entryModes": {
    "type": "array",
    "description": "4.3.2. The card entry modes this terminal accepts. **`magstripe` (swipe) is off unless listed**, since a swiped card carries no chip cryptogram; it stays available as a fallback where the acquirer allows it.",
    "items": {
     "type": "string",
     "enum": [
      "chip",
      "contactless",
      "magstripe",
      "manualEntry",
      "mobileWallet"
     ]
    }
   },
   "dccEnabled": {
    "type": "boolean",
    "default": false,
    "description": "4.3.2. Offer Dynamic Currency Conversion on a foreign card at this terminal. The rate is the provider's and is recorded on the payment (`fxRateSource` `cardScheme`); the ledger still holds the base currency."
   },
   "dccProviderConnectionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "contactlessLimit": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "pinBypassAllowed": {
    "type": "boolean",
    "default": false
   },
   "storeAndForward": {
    "type": "object",
    "description": "**A risk decision, not a technical one.**",
    "properties": {
     "enabled": {
      "type": "boolean",
      "default": false
     },
     "floorLimit": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "maximumHeldTotal": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "maximumAgeMinutes": {
      "type": "integer",
      "nullable": true
     }
    }
   },
   "status": {
    "type": "string",
    "enum": [
     "unconfigured",
     "active",
     "offline",
     "suspended"
    ]
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "WalletAuthenticationPolicy": {
  "type": "object",
  "x-ticvai-persistence": "wallet.authentication_policy",
  "description": "Board 6, p.68. **Risk-tiered proof of identity for a wallet spend.** The highest matching tier wins; with no policy, `WalletChannelRules.requiresPin` applies.",
  "required": [
   "tiers"
  ],
  "properties": {
   "tiers": {
    "type": "array",
    "maxItems": 20,
    "items": {
     "type": "object",
     "required": [
      "aboveAmount",
      "methods"
     ],
     "properties": {
      "aboveAmount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "channels": {
       "type": "array",
       "description": "Empty means every channel in `WalletChannelRules.allowedChannels`.",
       "items": {
        "type": "string"
       }
      },
      "transactionKinds": {
       "type": "array",
       "description": "Empty means every kind.",
       "items": {
        "$ref": "#/components/schemas/WalletTransactionKind"
       }
      },
      "methods": {
       "type": "array",
       "minItems": 1,
       "uniqueItems": true,
       "description": "Any one of these satisfies the tier.",
       "items": {
        "type": "string",
        "enum": [
         "walletPin",
         "deviceAuthentication",
         "digitalKey",
         "customerLogin",
         "membershipCredential"
        ]
       }
      }
     }
    }
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "WalletChannelRules": {
  "type": "object",
  "x-ticvai-persistence": "wallet.channel_rules",
  "description": "Board 6. **The offline rule is stated once, not per device.**",
  "properties": {
   "allowedChannels": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "allowedCredentialKinds": {
    "type": "array",
    "items": {
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
    }
   },
   "requiresPin": {
    "type": "boolean",
    "default": false
   },
   "pinAboveAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "offlineAllowed": {
    "type": "boolean",
    "default": false
   },
   "offlineFloorLimit": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "offlineMaximumAgeMinutes": {
    "type": "integer",
    "nullable": true,
    "description": "**How stale a cached balance may be before the device refuses.** Without a ceiling an offline terminal spends a balance that ran out yesterday.\n"
   },
   "acceptancePointIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
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
