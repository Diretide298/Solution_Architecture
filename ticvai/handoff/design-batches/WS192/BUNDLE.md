# WS192 — Wallet Configuration Backend Structure v1.0 board 7

**10 screens · 13 operations · 13 schemas · 6 permissions**

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

- **Every control that can be refused must be gated.** 6 permissions apply here:
  `APPROVAL_CONFIGURE, ORDER_REFUND, REGION_CONFIGURE, WALLET_CONFIGURE, WALLET_OPERATE, WALLET_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-1143` | Wallet Operations Command Center | listDetail | 2 | 0 | — |
| `BO-1144` | Peer-to-Peer Transfer Configuration | configEditor | 1 | 0 | — |
| `BO-1145` | Transfer Eligibility, Limits & Approval Rules | configEditor | 1 | 0 | — |
| `BO-1146` | Refund-to-Wallet Policy Configuration | configEditor | 2 | 0 | — |
| `BO-1147` | Refund Routing & Credit Restoration Engine | configEditor | 2 | 0 | — |
| `BO-1148` | Reversal & Transaction Correction Management | configEditor | 1 | 0 | — |
| `BO-1149` | Administrative Balance Adjustment Studio | configEditor | 2 | 0 | — |
| `BO-1150` | Wallet Block, Freeze & Restriction Management | configEditor | 2 | 4 | — |
| `BO-1151` | Wallet Disputes & Operational Exception Queue | configEditor | 3 | 0 | — |
| `BO-1152` | Operations Simulator, Approval & Audit Trail | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-1152 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-1143",
  "name": "Wallet Operations Command Center",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "7",
   "number": "01",
   "page": 75
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/wallet-operations-command-center-bo-1143",
   "component": "apps/venue-management-web/src/routes/orders-money/WalletOperationsCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-1144",
    "BO-1145",
    "BO-1146",
    "BO-1147",
    "BO-1148",
    "BO-1149",
    "BO-1150",
    "BO-1151",
    "BO-1152"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "BO-1144",
     "trigger": "Peer-to-Peer Transfer Configuration",
     "provenance": "structural — pack board 7 wiring, 19 September 2026"
    },
    {
     "to": "BO-1145",
     "trigger": "Transfer Eligibility, Limits & Approval Rules",
     "provenance": "structural — pack board 7 wiring, 19 September 2026"
    },
    {
     "to": "BO-1146",
     "trigger": "Refund-to-Wallet Policy Configuration",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "carries": [
      "venueId"
     ]
    },
    {
     "to": "BO-1147",
     "trigger": "Refund Routing & Credit Restoration Engine",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "carries": [
      "orderId"
     ]
    },
    {
     "to": "BO-1148",
     "trigger": "Reversal & Transaction Correction Management",
     "provenance": "structural — pack board 7 wiring, 19 September 2026"
    },
    {
     "to": "BO-1149",
     "trigger": "Administrative Balance Adjustment Studio",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "carries": [
      "subjectId"
     ]
    },
    {
     "to": "BO-1150",
     "trigger": "Wallet Block, Freeze & Restriction Management",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "carries": [
      "walletId"
     ]
    },
    {
     "to": "BO-1151",
     "trigger": "Wallet Disputes & Operational Exception Queue",
     "provenance": "structural — pack board 7 wiring, 19 September 2026"
    },
    {
     "to": "BO-1152",
     "trigger": "Operations Simulator, Approval & Audit Trail",
     "provenance": "structural — pack board 7 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide operations, finance and customer-service administrators with a centralized view of wallet operational activity and exceptions. Dashboard KPIs",
  "purposeNote": "Authorized users can monitor all wallet operational activity and trace every operation to the underlying wallet, transaction and administrator action.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 75 §Display"
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
       "label": "Search wallet operations",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 75 §Filters"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Tenant",
        "Venue",
        "Wallet type",
        "Customer",
        "Operation",
        "Credit type",
        "Currency",
        "Status",
        "Risk level",
        "Administrator",
        "Date/time",
        "Operational Alerts"
       ],
       "notes": "The pack filters this screen by tenant, venue, wallet type, customer, operation, credit type and 6 more — which are present is a decision the pack already made.",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 75 §Filters"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every wallet operations",
       "columns": [
        "Transfers Today",
        "Transfer Value",
        "Refunds Today",
        "Refund Value",
        "Reversals",
        "Manual Adjustments",
        "Blocked Wallets",
        "Frozen Balances",
        "Pending Operations",
        "Failed Operations",
        "Disputed Transactions",
        "Operations Awaiting Approval",
        "Activity Breakdown",
        "P2P Transfer",
        "Refund",
        "Reversal",
        "Credit Adjustment",
        "Debit Adjustment",
        "Wallet Block",
        "Wallet Unblock",
        "Balance Freeze",
        "Correction",
        "Administrative Operation"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 75 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected wallet operations",
       "bindsTo": null,
       "columns": [
        "Transfers Today",
        "Transfer Value",
        "Refunds Today",
        "Refund Value",
        "Reversals",
        "Manual Adjustments",
        "Blocked Wallets",
        "Frozen Balances",
        "Pending Operations",
        "Failed Operations",
        "Disputed Transactions",
        "Operations Awaiting Approval",
        "Activity Breakdown",
        "P2P Transfer",
        "Refund",
        "Reversal",
        "Credit Adjustment",
        "Debit Adjustment",
        "Wallet Block",
        "Wallet Unblock",
        "Balance Freeze",
        "Correction",
        "Administrative Operation"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Highlight”.",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 75 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The wallet operations list.",
   "error": "Could not load. Names which read failed and leaves the wallet operations untouched.",
   "emptyFirstRun": "No wallet operations yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the wallet operations are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listWalletDisputes",
    "contract": "wallet",
    "purpose": "Open exceptions",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listWalletTransactions",
    "contract": "wallet",
    "purpose": "Recent activity",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Transfers Today",
    "Transfer Value",
    "Refunds Today",
    "Refund Value",
    "Reversals",
    "Manual Adjustments"
   ],
   "params": [
    {
     "name": "subjectId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1143",
   "workshopBoard": "wireframes/WS192 Wallet Configuration Backend Structure v1.0 Board 7.dc.html#bo-1143"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 75. 0 of 35 labels bound to a contract property; 35 of 49 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1144",
  "name": "Peer-to-Peer Transfer Configuration",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "7",
   "number": "02",
   "page": 76
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/peer-to-peer-transfer-configuration-bo-1144",
   "component": "apps/venue-management-web/src/routes/orders-money/PeerToPeerTransferConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1143"
   ],
   "exitTo": [
    "BO-1143"
   ],
   "transitions": [
    {
     "to": "BO-1143",
     "trigger": "Back to Wallet Operations Command Center",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure direct value transfers between independent TICVAI wallet accounts. Requirement 4.3.16 specifically requires guests to transfer money from their wallet to another guest's wallet. Transfer Methods",
  "purposeNote": "P2P transfers create balanced debit and credit ledger entries and occur only after all eligibility, security and limit rules have passed.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "P2P enabled",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 76 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Eligible wallet types",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 76 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Eligible customer types",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 76 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Eligible credit types",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 76 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Supported currencies",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 76 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Minimum transfer",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 76 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum transfer",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 76 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Daily transfer amount",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 76 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Monthly transfer amount",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 76 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum transfer count",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 76 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Transfer fee",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 76 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Recipient verification",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 76 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Sender authentication",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 76 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Recipient confirmation",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 76 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Transfer expiry",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 76 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Cross-tenant transfer",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 76 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Cross-venue transfer",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 76 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Cross-currency transfer",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 76 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Example",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 76 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Wallet A",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 76 §Configure"
      },
      {
       "kind": "textField",
       "label": "Cash Credit: AED 500",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 76 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Wallet ID",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 76 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Customer ID",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 76 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Membership ID",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 76 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Contact selection",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 76 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "API",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 76 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The peer-to-peer transfer configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the peer-to-peer transfer untouched.",
   "emptyFirstRun": "No peer-to-peer transfer configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setWalletTransferRules",
    "contract": "wallet",
    "purpose": "Whether guests may transfer",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1144",
   "workshopBoard": "wireframes/WS192 Wallet Configuration Backend Structure v1.0 Board 7.dc.html#bo-1144"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 76. 0 of 0 labels bound to a contract property; 26 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Wallet ID, Customer ID, Membership ID, Contact selection, API are choices sent by `setWalletTransferRules` (field gap: add recipientLookupMethods walletId|customerId|membershipId|contact|api).",
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
  "id": "BO-1145",
  "name": "Transfer Eligibility, Limits & Approval Rules",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "7",
   "number": "03",
   "page": 77
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/transfer-eligibility-limits-approval-rules-bo-1145",
   "component": "apps/venue-management-web/src/routes/orders-money/TransferEligibilityLimitsApprovalRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1143"
   ],
   "exitTo": [
    "BO-1143"
   ],
   "transitions": [
    {
     "to": "BO-1143",
     "trigger": "Back to Wallet Operations Command Center",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure by; Configure) and no display directory — it is settings, not a population",
  "purpose": "Apply governance controls to wallet-to-wallet transfers. Eligibility",
  "purposeNote": "Every transfer is evaluated against current eligibility, transferability, velocity and authorization rules before wallet value moves.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Wallet type",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 77 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Credit type",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 77 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Customer verification status",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 77 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Membership",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 77 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Customer age",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 77 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Family role",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 77 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Corporate role",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 77 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Tenant",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 77 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 77 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Country/region where applicable",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 77 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Credit Transferability",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 77 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Per transaction",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 77 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Per hour",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 77 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Daily",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 77 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Weekly",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 77 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Monthly",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 77 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Recipient limits",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 77 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Sender limits",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 77 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Approval / Authentication",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 77 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The transfer eligibility limits configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the transfer eligibility limits untouched.",
   "emptyFirstRun": "No transfer eligibility limits configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setWalletTransferRules",
    "contract": "wallet",
    "purpose": "Eligibility, limits and approval",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1145",
   "workshopBoard": "wireframes/WS192 Wallet Configuration Backend Structure v1.0 Board 7.dc.html#bo-1145"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 77. 0 of 0 labels bound to a contract property; 19 of 41 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1146",
  "name": "Refund-to-Wallet Policy Configuration",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "7",
   "number": "04",
   "page": 79
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/refund-to-wallet-policy-configuration-bo-1146",
   "component": "apps/venue-management-web/src/routes/orders-money/RefundToWalletPolicyConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1143"
   ],
   "exitTo": [
    "BO-1143"
   ],
   "transitions": [
    {
     "to": "BO-1143",
     "trigger": "Back to Wallet Operations Command Center",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure; Refund policy can define) and no display directory — it is settings, not a population",
  "purpose": "Configure when refunds from TICVAI transactions may be returned directly to a digital wallet. Requirement 4.3.15 specifically requires instant refund to the digital wallet with customer notification. Refund Sources Ticket cancellation Event cancellation F&B refund Retail return Rental refund Parking refund Membership adjustment Attraction cancellation Failed service Customer-service compensation Refund Destinations",
  "purposeNote": "Refunds follow configured tender and wallet policies while preserving a direct relationship with the original transaction.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Original wallet",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 79 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Refund Credit bucket",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 79 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Cash Credit",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 79 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Original gift-card balance",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 79 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Original credit bucket",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 79 §Configure"
      },
      {
       "kind": "selectField",
       "label": "External payment method",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 79 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Rules",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 79 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Instant wallet refund",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 79 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Full refund",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 79 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Partial refund",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 79 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Refund amount limit",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 79 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Refund fee",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 79 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Refund validity",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 79 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Refund-credit expiry",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 79 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Transferability",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 79 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Withdrawal eligibility",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 79 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Original tender dependency",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 79 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Original customer requirement",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 79 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Approval requirement",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 79 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Example",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 79 §Configure"
      },
      {
       "kind": "textField",
       "label": "Wallet → AED 200 returned",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 79 §Refund policy can define"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The refund-to-wallet policy configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the refund-to-wallet policy untouched.",
   "emptyFirstRun": "No refund-to-wallet policy configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setRefundPolicy",
    "contract": "orders",
    "purpose": "Set a venue's refund policy",
    "trigger": "onAction"
   },
   {
    "operationId": "setWalletRefundPolicy",
    "contract": "wallet",
    "purpose": "What a refund puts back, and where",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1146",
   "workshopBoard": "wireframes/WS192 Wallet Configuration Backend Structure v1.0 Board 7.dc.html#bo-1146"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 79. 0 of 0 labels bound to a contract property; 21 of 42 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "navigation"
    }
   ],
   "coldEntry": "**Reached from the list that owns it**, so the identifier arrives with the navigation. Opened cold without one, the screen says what is missing and offers that list — never an empty form that looks configurable."
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
  "id": "BO-1147",
  "name": "Refund Routing & Credit Restoration Engine",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "7",
   "number": "05",
   "page": 80
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/refund-routing-credit-restoration-engine-bo-1147",
   "component": "apps/venue-management-web/src/routes/orders-money/RefundRoutingCreditRestorationEngine.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1143"
   ],
   "exitTo": [
    "BO-1143"
   ],
   "transitions": [
    {
     "to": "BO-1143",
     "trigger": "Back to Wallet Operations Command Center",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Determine exactly where returned value goes when the original transaction consumed multiple wallet credits. This is important because a simple “+AED 200 to Cash Credit” can corrupt wallet economics. Example",
  "purposeNote": "Refund processing correctly reconstructs or converts the value originally consumed without unintentionally changing its financial or promotional classification.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "textField",
       "label": "Restore with original expiry",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 80 §Configure"
      },
      {
       "kind": "textField",
       "label": "Restore with new validity",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 80 §Configure"
      },
      {
       "kind": "textField",
       "label": "Convert to refund credit",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 80 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Do not restore",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 80 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Require administrator approval",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 80 §Configure"
      },
      {
       "kind": "selectField",
       "label": "FEFO Interaction",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 80 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The refund routing credit configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the refund routing credit untouched.",
   "emptyFirstRun": "No refund routing credit configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setWalletRefundPolicy",
    "contract": "wallet",
    "purpose": "Restoration to the original lots",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "createRefund",
    "contract": "orders",
    "purpose": "Issue the refund",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1147",
   "workshopBoard": "wireframes/WS192 Wallet Configuration Backend Structure v1.0 Board 7.dc.html#bo-1147"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 80. 0 of 0 labels bound to a contract property; 6 of 37 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "orderId",
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
  "id": "BO-1148",
  "name": "Reversal & Transaction Correction Management",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "7",
   "number": "06",
   "page": 81
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/reversal-transaction-correction-management-bo-1148",
   "component": "apps/venue-management-web/src/routes/orders-money/ReversalTransactionCorrectionManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1143"
   ],
   "exitTo": [
    "BO-1143"
   ],
   "transitions": [
    {
     "to": "BO-1143",
     "trigger": "Back to Wallet Operations Command Center",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Correct operational wallet transactions while maintaining an immutable ledger. Supported Operations Payment reversal Transfer reversal Refund reversal Duplicate debit correction Duplicate credit correction Failed transaction correction Offline synchronization correction Incorrect wallet correction Incorrect amount correction Important Rule Never delete or overwrite the original wallet ledger transaction.",
  "purposeNote": "Every reversal or correction creates linked compensating ledger entries while preserving the complete original transaction history.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Eligible transaction type",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 81 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Reversal period",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 81 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Full reversal",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 81 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Partial reversal",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 81 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Reason code",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 81 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Notes",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 81 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Approval",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 81 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Supporting documentation",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 81 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Customer notification",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 81 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Finance notification",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 81 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Reconciliation behavior",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 81 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The reversal transaction correction configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the reversal transaction correction untouched.",
   "emptyFirstRun": "No reversal transaction correction configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "reverseWalletFunding",
    "contract": "wallet",
    "purpose": "Reverse a transaction",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listWalletTransactions",
     "listCreditLots"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1148",
   "workshopBoard": "wireframes/WS192 Wallet Configuration Backend Structure v1.0 Board 7.dc.html#bo-1148"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 81. 0 of 0 labels bound to a contract property; 11 of 30 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1149",
  "name": "Administrative Balance Adjustment Studio",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "7",
   "number": "07",
   "page": 81
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/administrative-balance-adjustment-studio-bo-1149",
   "component": "apps/venue-management-web/src/routes/orders-money/AdministrativeBalanceAdjustmentStudio.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1143"
   ],
   "exitTo": [
    "BO-1143"
   ],
   "transitions": [
    {
     "to": "BO-1143",
     "trigger": "Back to Wallet Operations Command Center",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
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
  "purpose": "Allow authorized personnel to perform governed wallet balance adjustments. Adjustment Types Credit Customer compensation Service recovery Promotional correction Migration adjustment Balance correction Manual award Debit Incorrect credit recovery Duplicate credit recovery Administrative correction Fraud recovery where authorized",
  "purposeNote": "No manual balance adjustment can occur without the required permissions, reason, approval and ledger record.",
  "gaps": [
   {
    "operation": null,
    "why": "**Administrative Balance Adjustment Studio declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
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
       "label": "Adjustment reason",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 81 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Credit type",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 81 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Amount",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 81 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Wallet",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 81 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Currency",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 81 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Expiry",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 81 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Financial classification",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 81 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Customer-visible description",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 81 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Supporting reference",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 81 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Multi-level approval",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 81 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The administrative balance adjustment configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the administrative balance adjustment untouched.",
   "emptyFirstRun": "No administrative balance adjustment configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "adjustWallet",
    "contract": "wallet",
    "purpose": "Administrative adjustment",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getWallet",
     "listWalletTransactions",
     "listCreditLots"
    ]
   },
   {
    "operationId": "setApprovalMatrix",
    "contract": "approvals",
    "purpose": "Require multi-level approval on balance adjustments",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration): serves the pack action(s) Multi-level approval"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1149",
   "workshopBoard": "wireframes/WS192 Wallet Configuration Backend Structure v1.0 Board 7.dc.html#bo-1149"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 81. 0 of 0 labels bound to a contract property; 10 of 35 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Multi-level approval: `setApprovalMatrix`.",
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
  "id": "BO-1150",
  "name": "Wallet Block, Freeze & Restriction Management",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "7",
   "number": "08",
   "page": 82
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/wallet-block-freeze-restriction-management-bo-1150",
   "component": "apps/venue-management-web/src/routes/orders-money/WalletBlockFreezeRestrictionManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1143"
   ],
   "exitTo": [
    "BO-1143"
   ],
   "transitions": [
    {
     "to": "BO-1143",
     "trigger": "Back to Wallet Operations Command Center",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
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
  "purpose": "Protect wallet accounts and individual balances without necessarily closing the wallet. Requirement 4.3.21 explicitly states that it must be possible to block a wallet account.",
  "purposeNote": "Authorized administrators can apply granular restrictions without modifying or deleting underlying wallet balances.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Immediate",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 82 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Until date",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 82 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Until investigation completed",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 82 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Permanent",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 82 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Manual release",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 82 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Example",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 82 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Block wallet",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 82 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Unblock wallet",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 82 §Support"
      },
      {
       "kind": "destructiveButton",
       "label": "Suspend wallet",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 82 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Freeze entire balance",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 82 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Freeze specific credit",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 82 §Support"
      },
      {
       "kind": "destructiveButton",
       "label": "Disable spending",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 82 §Support"
      },
      {
       "kind": "destructiveButton",
       "label": "Disable transfers",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 82 §Support"
      },
      {
       "kind": "destructiveButton",
       "label": "Disable top-up",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 82 §Support"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmSuspendWallet",
    "component": "confirmDialog",
    "trigger": "Suspend wallet",
    "body": "**Suspend wallet on a wallet block freeze is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 82 §Support"
   },
   {
    "id": "confirmDisableSpending",
    "component": "confirmDialog",
    "trigger": "Disable spending",
    "body": "**Disable spending on a wallet block freeze is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 82 §Support"
   },
   {
    "id": "confirmDisableTransfers",
    "component": "confirmDialog",
    "trigger": "Disable transfers",
    "body": "**Disable transfers on a wallet block freeze is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 82 §Support"
   },
   {
    "id": "confirmDisableTopUp",
    "component": "confirmDialog",
    "trigger": "Disable top-up",
    "body": "**Disable top-up on a wallet block freeze is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 82 §Support"
   }
  ],
  "states": {
   "loading": "The wallet block freeze configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the wallet block freeze untouched.",
   "emptyFirstRun": "No wallet block freeze configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setWalletRestriction",
    "contract": "wallet",
    "purpose": "Freeze, block or restrict",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getWallet"
    ]
   },
   {
    "operationId": "suspendWallet",
    "contract": "wallet",
    "purpose": "Suspend the wallet",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration): serves the pack action(s) Suspend wallet"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "walletId",
     "from": "navigation"
    }
   ],
   "coldEntry": "Opened from BO-1143 with the wallet picked there. Opened cold (a bookmark or a refresh), it shows the list to pick from rather than an empty record, and says plainly if the wallet no longer exists."
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1150",
   "workshopBoard": "wireframes/WS192 Wallet Configuration Backend Structure v1.0 Board 7.dc.html#bo-1150"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 82. 0 of 0 labels bound to a contract property; 22 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Block wallet, Unblock wallet, Freeze entire balance, Freeze specific credit, Disable spending, Disable transfers, Disable top-up … are choices sent by `setWalletRestriction` (kind block|none|freeze|restrict + blockedChannels; field gap: blockedCreditTypeIds for freezing one credit); Suspend wallet: `suspendWallet`.",
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
  "id": "BO-1151",
  "name": "Wallet Disputes & Operational Exception Queue",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "7",
   "number": "09",
   "page": 83
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/wallet-disputes-operational-exception-queue-bo-1151",
   "component": "apps/venue-management-web/src/routes/orders-money/WalletDisputesOperationalExceptionQueue.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1143"
   ],
   "exitTo": [
    "BO-1143"
   ],
   "transitions": [
    {
     "to": "BO-1143",
     "trigger": "Back to Wallet Operations Command Center",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture; Configure) and no display directory — it is settings, not a population",
  "purpose": "Provide a controlled workflow for wallet transaction problems requiring investigation. Exception Types Customer disputes transaction Duplicate wallet debit Wallet charged but service failed Transfer recipient not received Refund missing Offline transaction conflict Balance mismatch Gift card issue Credential misuse Suspicious transfer Reconciliation mismatch Case Information",
  "purposeNote": "Every operational wallet dispute is managed through a traceable case workflow linked to the affected transactions and corrective actions.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Case ID",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 83 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Wallet",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 83 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Customer",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 83 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Transaction",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 83 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Amount",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 83 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Channel",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 83 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Device",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 83 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 83 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Date/time",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 83 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Issue category",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 83 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Customer description",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 83 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Evidence",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 83 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Risk score",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 83 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Priority",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 83 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Resolution SLA",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 83 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Assignment",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 83 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Escalation",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 83 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Notifications",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 83 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "banner",
       "label": "Permissions this screen separates",
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** No action, Refund, Reverse, Adjust balance, Block wallet, Replace credential, Escalate, Refer to finance/security, SLA. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 83 §Authorized users may"
      },
      {
       "kind": "primaryButton",
       "label": "Withdraw dispute",
       "operation": "withdrawWalletDispute",
       "provenance": "contract wallet.yaml POST /wallet-disputes/{disputeId}/withdraw (decided 29 September, VM close-out)"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The wallet disputes operational configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the wallet disputes operational untouched.",
   "emptyFirstRun": "No wallet disputes operational configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "listWalletDisputes",
    "contract": "wallet",
    "purpose": "The dispute queue",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "raiseWalletDispute",
    "contract": "wallet",
    "purpose": "Raise one",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listWalletDisputes"
    ]
   },
   {
    "operationId": "withdrawWalletDispute",
    "contract": "wallet",
    "purpose": "Withdraw dispute",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1151",
   "workshopBoard": "wireframes/WS192 Wallet Configuration Backend Structure v1.0 Board 7.dc.html#bo-1151"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 83. 0 of 0 labels bound to a contract property; 27 of 53 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "disputeId",
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
  "id": "BO-1152",
  "name": "Operations Simulator, Approval & Audit Trail",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "7",
   "number": "10",
   "page": 85
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/operations-simulator-approval-audit-trail-bo-1152",
   "component": "apps/venue-management-web/src/routes/orders-money/OperationsSimulatorApprovalAuditTrail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1143"
   ],
   "exitTo": [
    "BO-1143"
   ],
   "transitions": [
    {
     "to": "BO-1143",
     "trigger": "Back to Wallet Operations Command Center",
     "provenance": "structural — pack board 7 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide administrators with a final controlled workspace for testing sensitive wallet operations and reviewing the immutable operational history. Simulation Example — Refund Configure TICVAI’s centralized wallet security and fraud-control layer, combining rule-based controls, transaction risk scoring, velocity monitoring, device and credential intelligence, AI anomaly detection, automated protective actions, fraud investigation, and security governance. This board directly covers requirements 4.3.30, 4.3.31 and 4.3.32, which require configurable wallet limits, suspicious- transaction controls, manual review, spending/transfer restrictions and AI identification of unusual top-ups, spending, account sharing, rapid transfers, duplicate transactions and unauthorized-access patterns.",
  "purposeNote": "Sensitive wallet operations can be validated before execution, and every financial or administrative action is permanently traceable through the wallet ledger and audit history. Board 7 — Operational Architecture",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 85"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 85"
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
       "impliedBy": "listWalletDisputes",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The operations simulator approval list.",
   "error": "Could not load. Names which read failed and leaves the operations simulator approval untouched.",
   "emptyFirstRun": "No operations simulator approval yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the operations simulator approval are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listWalletDisputes",
    "contract": "wallet",
    "purpose": "Operations audit trail",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1152",
   "workshopBoard": "wireframes/WS192 Wallet Configuration Backend Structure v1.0 Board 7.dc.html#bo-1152"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 85. 0 of 0 labels bound to a contract property; 0 of 91 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "createRefund": {
  "method": "POST",
  "path": "/orders/{orderId}/refunds",
  "contract": "orders",
  "summary": "Refund an order, wholly or in part",
  "permission": "ORDER_REFUND",
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
  "requestBody": "CreateRefundRequest",
  "responds": null
 },
 "listWalletDisputes": {
  "method": "GET",
  "path": "/wallet-disputes",
  "contract": "wallet",
  "summary": "Contested transactions and operational exceptions",
  "permission": "WALLET_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "status",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "WalletDispute"
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
 "raiseWalletDispute": {
  "method": "POST",
  "path": "/wallet-disputes",
  "contract": "wallet",
  "summary": "A guest contests a wallet transaction",
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
  "requestBody": "WalletDispute",
  "responds": "WalletDispute"
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
 "setApprovalMatrix": {
  "method": "PUT",
  "path": "/approval-matrices",
  "contract": "approvals",
  "summary": "Configure what requires approval",
  "permission": "APPROVAL_CONFIGURE",
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
  "requestBody": "ApprovalMatrix",
  "responds": "ApprovalMatrix"
 },
 "setRefundPolicy": {
  "method": "PUT",
  "path": "/venues/{venueId}/refund-policy",
  "contract": "orders",
  "summary": "Set a venue's refund policy",
  "permission": "REGION_CONFIGURE",
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
  "requestBody": "RefundPolicy",
  "responds": "RefundPolicy"
 },
 "setWalletRefundPolicy": {
  "method": "PUT",
  "path": "/wallet-refund-policy",
  "contract": "wallet",
  "summary": "What a refund puts back, and where",
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
  "requestBody": "WalletRefundPolicy",
  "responds": "WalletRefundPolicy"
 },
 "setWalletRestriction": {
  "method": "POST",
  "path": "/wallet-restrictions",
  "contract": "wallet",
  "summary": "Block, freeze or restrict a wallet",
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
  "requestBody": "WalletRestriction",
  "responds": "WalletRestriction"
 },
 "setWalletTransferRules": {
  "method": "PUT",
  "path": "/wallet-transfer-rules",
  "contract": "wallet",
  "summary": "Whether guests may move money to each other, and on what terms",
  "permission": "WALLET_CONFIGURE",
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
  "requestBody": "WalletTransferRules",
  "responds": "WalletTransferRules"
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
 "withdrawWalletDispute": {
  "method": "POST",
  "path": "/wallet-disputes/{disputeId}/withdraw",
  "contract": "wallet",
  "summary": "Withdraw a wallet dispute that is still open or under review",
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
  "responds": "WalletDispute"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "ApprovalKind": {
  "type": "string",
  "description": "11.1.7 and 11.1.30–11.1.37. **The first four already exist as bespoke implementations** and this contract is what they collapse into.\n**Which actions route here — decided 28 September, audit R144.** Finance and procurement acts go through this engine to a **finance approver**: closing a fiscal period (`periodClose`), reopening one (`periodReopen`), cancelling a purchase order (`purchaseOrderCancel`) and closing one short (`purchaseOrderShortClose`). The tenant default matrix for each of these names the finance approver role; a venue may tighten it and never loosen it. Starting a release rollout routes through `releasePromotion` to the platform release manager (a holder of `PLATFORM_RELEASE_PROMOTE`). **Not every `requiresApproval` goes here:** reopening a shift, recounting a stock count and a retail return above the venue threshold take a supervisor's step-up on the same device instead, and never raise a request.\n",
  "enum": [
   "refund",
   "priceOverride",
   "discountOverride",
   "complimentaryTicket",
   "membershipCancellation",
   "accessPermissionChange",
   "configurationChange",
   "aiRecommendation",
   "releasePromotion",
   "requisition",
   "stockWriteOff",
   "journalEntry",
   "periodClose",
   "periodReopen",
   "purchaseOrderCancel",
   "purchaseOrderShortClose",
   "tenantMigration"
  ]
 },
 "ApprovalMatrix": {
  "type": "object",
  "x-ticvai-persistence": "approvals.matrix",
  "required": [
   "kind",
   "scopeLevel",
   "rules"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "kind": {
    "$ref": "#/components/schemas/ApprovalKind"
   },
   "scopeLevel": {
    "type": "string",
    "enum": [
     "tenant",
     "region",
     "venue"
    ]
   },
   "scopePath": {
    "type": "string",
    "readOnly": true
   },
   "version": {
    "type": "integer",
    "readOnly": true,
    "description": "11.1.80. **A request is decided by the rules it was raised under.** Changing the matrix mid-flight would mean an approver answering a question that changed while they read it.\n**(`kind`, `scopePath`, `version`) is unique**, and a stored version is never edited: a request's `matrixVersion` names exactly one rule set (decided 28 September, audit R129 (2)).\n"
   },
   "rules": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/ApprovalRule"
    }
   },
   "isActive": {
    "type": "boolean"
   }
  }
 },
 "ApprovalRule": {
  "type": "object",
  "x-ticvai-persistence": "approvals.rule",
  "required": [
   "order",
   "approverRoleIds",
   "mode"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "order": {
    "type": "integer",
    "description": "**First match wins.** Explicit ordering is what makes a matrix reviewable — an unordered set of overlapping rules is one nobody can reason about.\n"
   },
   "minAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "maxAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "riskScoreAbove": {
    "type": "number",
    "nullable": true,
    "description": "11.1.12. **Nothing supplies this yet** — risk scoring is parked with the model-dependent AI. The field exists so adding the engine later is configuration rather than a schema change.\n"
   },
   "condition": {
    "type": "string",
    "nullable": true,
    "description": "11.1.13. Evaluated against the attributes the caller supplied.\n\n**No condition language is defined yet** (pull audit R104, 26 September): the grammar, the attributes it may name and how two conditions are compared for `unreachableRule` are an open decision, not something to infer from this field.\n"
   },
   "approverRoleIds": {
    "type": "array",
    "minItems": 1,
    "description": "Role ids from `identity.listRoles` (`Role.id`), which is where an editor gets the names to show and pick from. This contract stores the ids only.\n",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "approverScopeLevel": {
    "type": "string",
    "enum": [
     "venue",
     "department",
     "region",
     "tenant"
    ],
    "description": "11.1.39. Which organisational level the approver must sit at."
   },
   "mode": {
    "$ref": "#/components/schemas/ApprovalMode"
   },
   "levels": {
    "type": "integer",
    "default": 1,
    "description": "11.1.3. Multi-level chains ask each level in turn."
   },
   "requiresMfa": {
    "type": "boolean",
    "default": false
   },
   "requiresSignature": {
    "type": "boolean",
    "default": false
   },
   "slaMinutes": {
    "type": "integer",
    "nullable": true,
    "description": "11.1.14. Null means no SLA, which is different from a long one."
   },
   "escalateAfterMinutes": {
    "type": "integer",
    "nullable": true
   },
   "escalateToRoleIds": {
    "type": "array",
    "description": "Role ids from `identity.listRoles`, as `approverRoleIds`.",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "expiresAfterMinutes": {
    "type": "integer",
    "nullable": true,
    "description": "11.1.53. An unanswered request eventually stops waiting."
   }
  }
 },
 "CreateRefundRequest": {
  "type": "object",
  "required": [
   "id",
   "amount",
   "reason",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "Client-generated ULID of the refund, and its idempotency key — it must equal the `Idempotency-Key` header."
   },
   "lineIds": {
    "type": "array",
    "items": {
     "type": "string",
     "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
    },
    "description": "Omit to refund the whole order."
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "reason": {
    "type": "string",
    "minLength": 3,
    "maxLength": 500
   },
   "secondaryAuthorisation": {
    "type": "object",
    "description": "Required above the venue's `requiresSecondUserAbove`. A second user — cashier or supervisor — names themselves. This is dual-authorisation, not escalation.\n",
    "required": [
     "principalId",
     "credential"
    ],
    "properties": {
     "principalId": {
      "type": "string",
      "format": "uuid"
     },
     "credential": {
      "type": "string",
      "maxLength": 512,
      "description": "The second person's staff PIN, as they sign in at a till with it. **A PIN, never a password** (decided 28 September, audit R123 (7))."
     }
    }
   },
   "refundToOriginalTender": {
    "type": "boolean",
    "default": true
   },
   "alternateTender": {
    "$ref": "#/components/schemas/TenderKind"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
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
 "RefundPolicy": {
  "x-ticvai-persistence": "orders.refund_policy + orders.refund_policy_time_band",
  "type": "object",
  "description": "Venue-configured. Thresholds are policy, not permission scope — venues run different policies and the permission model should not encode commercial rules.\n**The three thresholds must ascend** (decided 28 September, audit R123 (6)): `selfAuthoriseLimit` <= `requiresSecondUserAbove` <= `requiresApprovalAbove`, where the second is set. `setRefundPolicy` refuses a policy that does not with 422 `refund-thresholds-not-ascending`.\n",
  "required": [
   "venueId",
   "selfAuthoriseLimit",
   "requiresApprovalAbove"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "The venue in the path. Not taken from a `setRefundPolicy` body."
   },
   "selfAuthoriseLimit": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Up to this, a holder of ORDER_REFUND refunds alone. Zero means every refund needs a second authoriser.\n"
   },
   "requiresSecondUserAbove": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Above this, a second user — cashier OR supervisor — names themselves as audit control. Dual-authorisation, not escalation (2.12.3).\n"
   },
   "requiresApprovalAbove": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Above this, an ORDER_REFUND_APPROVE holder must approve."
   },
   "timeBands": {
    "type": "array",
    "description": "Refundable percentage by time before the performance. Evaluated most-specific first.\n",
    "items": {
     "type": "object",
     "required": [
      "hoursBefore",
      "percentage"
     ],
     "properties": {
      "hoursBefore": {
       "type": "integer",
       "minimum": 0
      },
      "percentage": {
       "type": "number",
       "minimum": 0,
       "maximum": 100
      }
     }
    }
   },
   "allowPartial": {
    "type": "boolean",
    "default": true
   },
   "refundWindowDays": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "description": "Days after purchase within which a refund may be made. 0 is allowed and means the day of purchase only; null means no window (decided 28 September, audit R123 (6))."
   },
   "varianceThreshold": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Price variance above this is an exception requiring review rather than a routine posting (CF-38). Venue-configured.\n**A venue setting with a tenant default** (decided 28 September, audit R094). **Proposed default, client to correct (audit R094): AED 5.00 per order line.**\n"
   }
  }
 },
 "TenderKind": {
  "type": "string",
  "description": "`wallet` is a **digital wallet** (Apple Pay, Google Pay and the like, taken through the gateway), the value the guest channels accept beside `card` (decided 28 September, audit R080 (a)). **The stored-value TICVAI wallet is a separate tender**: it is spent through `authoriseStoredValue` and `captureStoredValue` (`StoredValueKind` `wallet`), never as this value, so the client can see which of the two the decision meant.\n",
  "enum": [
   "cash",
   "card",
   "wallet",
   "voucher",
   "bankTransfer",
   "hotelCharge",
   "installment",
   "giftCard",
   "complimentary"
  ]
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
 "WalletDispute": {
  "type": "object",
  "x-ticvai-persistence": "wallet.dispute",
  "description": "Board 7.9. **Internal, and the venue decides it** — unlike a card chargeback.",
  "required": [
   "walletId",
   "description"
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
   "transactionIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "description": {
    "type": "string"
   },
   "raisedBy": {
    "type": "string",
    "format": "uuid"
   },
   "raisedAt": {
    "type": "string",
    "format": "date-time"
   },
   "status": {
    "type": "string",
    "enum": [
     "open",
     "investigating",
     "escalated",
     "upheld",
     "rejected",
     "withdrawn"
    ],
    "description": "`escalated` added with `resolveWalletDispute` (VM close-out, 29 September). `upheld`, `rejected` and `withdrawn` are closed."
   },
   "resolution": {
    "type": "string",
    "nullable": true
   },
   "escalatedToRoleId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true
   },
   "reprocessedTransactionIds": {
    "type": "array",
    "readOnly": true,
    "description": "Transactions created by a `reprocess` action.",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "resolvedBy": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true
   },
   "resolvedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "adjustmentId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "WalletRefundPolicy": {
  "type": "object",
  "x-ticvai-persistence": "wallet.refund_policy",
  "description": "Boards 7.4 and 7.5. **Restoration is to the lot, not to the balance.**",
  "properties": {
   "defaultDestination": {
    "type": "string",
    "enum": [
     "originalTender",
     "wallet",
     "guestChoice"
    ]
   },
   "walletRefundCreditTypeId": {
    "type": "string",
    "format": "uuid"
   },
   "restoreToOriginalLots": {
    "type": "boolean",
    "default": true
   },
   "restoreOriginalExpiry": {
    "type": "boolean",
    "default": true,
    "description": "**Refunding into a new lot with a fresh expiry is a gift.** Sometimes intended, never by accident.\n"
   },
   "walletRefundBonusPercent": {
    "type": "number",
    "nullable": true,
    "description": "An incentive to take the refund as credit rather than to a card."
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "WalletRestriction": {
  "type": "object",
  "x-ticvai-persistence": "wallet.restriction",
  "description": "Board 7.8. **Freeze, block and restrict are three different things.**",
  "required": [
   "walletId",
   "kind",
   "reason"
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
     "freeze",
     "block",
     "restrict",
     "none"
    ],
    "description": "**`freeze` stops spending and allows funding** — what you do while investigating. **`block` stops both** — a confirmed fraud. **`restrict` limits channels or categories** — what a parent asked for.\n"
   },
   "blockedChannels": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "blockedCategoryIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "reason": {
    "type": "string"
   },
   "appliedBy": {
    "type": "string",
    "format": "uuid"
   },
   "appliedAt": {
    "type": "string",
    "format": "date-time"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "WalletTransferRules": {
  "type": "object",
  "x-ticvai-persistence": "wallet.transfer_rules",
  "description": "Boards 7.2 and 7.3. **A money-transmission question before it is a feature.**",
  "properties": {
   "peerToPeerAllowed": {
    "type": "boolean",
    "default": false
   },
   "transferableCreditTypeIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "maximumPerTransfer": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "maximumPerDay": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "approvalAboveAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "bothPartiesIdentified": {
    "type": "boolean",
    "default": true
   },
   "withinSharedWalletOnly": {
    "type": "boolean",
    "default": false
   },
   "scopePath": {
    "type": "string"
   }
  }
 }
}
```
