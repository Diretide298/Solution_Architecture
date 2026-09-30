# WS194 — Wallet Configuration Backend Structure v1.0 board 9

**10 screens · 9 operations · 12 schemas · 5 permissions**

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
  `LEDGER_APPROVE, LEDGER_VIEW, WALLET_CONFIGURE, WALLET_OPERATE, WALLET_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-1163` | Wallet Finance & Liability Command Center | listDetail | 1 | 0 | — |
| `BO-1164` | Wallet Financial Classification & Accounting Mapping | configEditor | 1 | 0 | — |
| `BO-1165` | Wallet Sub-Ledger & Balance Control | listDetail | 1 | 0 | — |
| `BO-1166` | Multi-Source Reconciliation Configuration | configEditor | 2 | 0 | — |
| `BO-1167` | Reconciliation Exception & Resolution Workbench | listDetail | 2 | 0 | — |
| `BO-1168` | Gift Card Liability Management | listDetail | 1 | 0 | — |
| `BO-1169` | Breakage & Revenue Recognition Policy | listDetail | 1 | 0 | — |
| `BO-1170` | Wallet Financial Period & Closing Controls | configEditor | 2 | 0 | — |
| `BO-1171` | Wallet Analytics & Management Reporting | listDetail | 1 | 0 | — |
| `BO-1172` | Finance Validation, Reporting & Audit Center | listDetail | 6 | 0 | — |

## Thin screens in this batch

**BO-1163, BO-1167, BO-1168, BO-1169, BO-1171 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-1163",
  "name": "Wallet Finance & Liability Command Center",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "9",
   "number": "01",
   "page": 102
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/wallet-finance-liability-command-center-bo-1163",
   "component": "apps/venue-management-web/src/routes/orders-money/WalletFinanceLiabilityCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-1164",
    "BO-1165",
    "BO-1166",
    "BO-1167",
    "BO-1168",
    "BO-1169",
    "BO-1170",
    "BO-1171",
    "BO-1172"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 9 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "BO-1164",
     "trigger": "Wallet Financial Classification & Accounting Mapping",
     "provenance": "structural — pack board 9 wiring, 19 September 2026"
    },
    {
     "to": "BO-1165",
     "trigger": "Wallet Sub-Ledger & Balance Control",
     "provenance": "structural — pack board 9 wiring, 19 September 2026"
    },
    {
     "to": "BO-1166",
     "trigger": "Multi-Source Reconciliation Configuration",
     "provenance": "structural — pack board 9 wiring, 19 September 2026"
    },
    {
     "to": "BO-1167",
     "trigger": "Reconciliation Exception & Resolution Workbench",
     "provenance": "structural — pack board 9 wiring, 19 September 2026"
    },
    {
     "to": "BO-1168",
     "trigger": "Gift Card Liability Management",
     "provenance": "structural — pack board 9 wiring, 19 September 2026"
    },
    {
     "to": "BO-1169",
     "trigger": "Breakage & Revenue Recognition Policy",
     "provenance": "structural — pack board 9 wiring, 19 September 2026"
    },
    {
     "to": "BO-1170",
     "trigger": "Wallet Financial Period & Closing Controls",
     "provenance": "structural — pack board 9 wiring, 19 September 2026"
    },
    {
     "to": "BO-1171",
     "trigger": "Wallet Analytics & Management Reporting",
     "provenance": "structural — pack board 9 wiring, 19 September 2026"
    },
    {
     "to": "BO-1172",
     "trigger": "Finance Validation, Reporting & Audit Center",
     "provenance": "structural — pack board 9 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display; Show) and no metric row",
  "purpose": "Provide Finance and authorized management users with a consolidated financial view of all wallet obligations and movements. Executive KPIs",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 102 §Display"
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
       "label": "Every wallet finance liability",
       "columns": [
        "Total Wallet Liability",
        "Cash Credit Liability",
        "Gift Card Liability",
        "Refund Credit Liability",
        "Bonus/Promotional Value",
        "Membership Credit Exposure",
        "Outstanding Stored Value",
        "Issued Value",
        "Redeemed Value",
        "Expired Value",
        "Breakage Recognized",
        "Unreconciled Value",
        "Suspended/Frozen Value",
        "Liability Breakdown",
        "Credit type",
        "Wallet type",
        "Gift card",
        "Tenant",
        "Venue",
        "Currency",
        "Customer type",
        "Accounting period",
        "Movement Analysis",
        "Opening Liability",
        "Funding",
        "Gift Cards Issued",
        "Credits Issued",
        "Refunds to Wallet",
        "− Redemptions",
        "− Expirations",
        "− Reversals/Corrections",
        "= Closing Liability",
        "Alerts"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 102 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected wallet finance liability",
       "bindsTo": null,
       "columns": [
        "Total Wallet Liability",
        "Cash Credit Liability",
        "Gift Card Liability",
        "Refund Credit Liability",
        "Bonus/Promotional Value",
        "Membership Credit Exposure",
        "Outstanding Stored Value",
        "Issued Value",
        "Redeemed Value",
        "Expired Value",
        "Breakage Recognized",
        "Unreconciled Value",
        "Suspended/Frozen Value",
        "Liability Breakdown",
        "Credit type",
        "Wallet type",
        "Gift card",
        "Tenant",
        "Venue",
        "Currency",
        "Customer type",
        "Accounting period",
        "Movement Analysis",
        "Opening Liability",
        "Funding",
        "Gift Cards Issued",
        "Credits Issued",
        "Refunds to Wallet",
        "− Redemptions",
        "− Expirations",
        "− Reversals/Corrections",
        "= Closing Liability",
        "Alerts"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Highlight”.",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 102 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The wallet finance liability list.",
   "error": "Could not load. Names which read failed and leaves the wallet finance liability untouched.",
   "emptyFirstRun": "No wallet finance liability yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the wallet finance liability are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getWalletLiability",
    "contract": "wallet",
    "purpose": "Liability at a glance",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Total Wallet Liability",
    "Cash Credit Liability",
    "Gift Card Liability",
    "Refund Credit Liability",
    "Bonus/Promotional Value",
    "Membership Credit Exposure"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1163",
   "workshopBoard": "wireframes/WS194 Wallet Configuration Backend Structure v1.0 Board 9.dc.html#bo-1163"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 102. 0 of 33 labels bound to a contract property; 33 of 47 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1164",
  "name": "Wallet Financial Classification & Accounting Mapping",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "9",
   "number": "02",
   "page": 103
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/wallet-financial-classification-accounting-mapping-bo-1164",
   "component": "apps/venue-management-web/src/routes/orders-money/WalletFinancialClassificationAccountingMapping.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1163"
   ],
   "exitTo": [
    "BO-1163"
   ],
   "transitions": [
    {
     "to": "BO-1163",
     "trigger": "Back to Wallet Finance & Liability Command Center",
     "provenance": "structural — pack board 9 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure accounting treatment for; Configure) and no display directory — it is settings, not a population",
  "purpose": "Define the financial classification of every wallet credit and transaction type. Credit Mapping",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Cash Credit",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 103 §Configure accounting treatment for"
      },
      {
       "kind": "selectField",
       "label": "Refund Credit",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 103 §Configure accounting treatment for"
      },
      {
       "kind": "selectField",
       "label": "Gift Card",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 103 §Configure accounting treatment for"
      },
      {
       "kind": "selectField",
       "label": "Bonus Credit",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 103 §Configure accounting treatment for"
      },
      {
       "kind": "selectField",
       "label": "Promotional Credit",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 103 §Configure accounting treatment for"
      },
      {
       "kind": "selectField",
       "label": "Membership Credit",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 103 §Configure accounting treatment for"
      },
      {
       "kind": "selectField",
       "label": "Ride Credit",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 103 §Configure accounting treatment for"
      },
      {
       "kind": "selectField",
       "label": "F&B Credit",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 103 §Configure accounting treatment for"
      },
      {
       "kind": "selectField",
       "label": "Retail Credit",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 103 §Configure accounting treatment for"
      },
      {
       "kind": "selectField",
       "label": "Parking Credit",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 103 §Configure accounting treatment for"
      },
      {
       "kind": "selectField",
       "label": "Other credits",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 103 §Configure accounting treatment for"
      },
      {
       "kind": "selectField",
       "label": "Transaction Mapping",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 103 §Configure accounting treatment for"
      },
      {
       "kind": "selectField",
       "label": "Top-Up",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 103 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Redemption",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 103 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Refund",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 103 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Transfer",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 103 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Adjustment",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 103 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Reversal",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 103 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Expiration",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 103 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Gift Card Sale",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 103 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Gift Card Redemption",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 103 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Breakage",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 103 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Mapping Dimensions",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 103 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The wallet financial classification configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the wallet financial classification untouched.",
   "emptyFirstRun": "No wallet financial classification configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setWalletAccountingMapping",
    "contract": "wallet",
    "purpose": "Credit types to ledger accounts",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getWalletLiability"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1164",
   "workshopBoard": "wireframes/WS194 Wallet Configuration Backend Structure v1.0 Board 9.dc.html#bo-1164"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 103. 0 of 0 labels bound to a contract property; 23 of 48 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1165",
  "name": "Wallet Sub-Ledger & Balance Control",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "9",
   "number": "03",
   "page": 104
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/wallet-sub-ledger-balance-control-bo-1165",
   "component": "apps/venue-management-web/src/routes/orders-money/WalletSubLedgerBalanceControl.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1163"
   ],
   "exitTo": [
    "BO-1163"
   ],
   "transitions": [
    {
     "to": "BO-1163",
     "trigger": "Back to Wallet Finance & Liability Command Center",
     "provenance": "structural — pack board 9 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Maintain the authoritative financial transaction history behind every wallet balance. Sub-Ledger View",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 104"
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
       "kind": "datePicker",
       "label": "From",
       "operation": "getWalletReconciliation",
       "notes": "Sends `?from=` (required).",
       "provenance": "contract wallet.yaml GET /wallet-reconciliation"
      },
      {
       "kind": "datePicker",
       "label": "To",
       "operation": "getWalletReconciliation",
       "notes": "Sends `?to=` (required).",
       "provenance": "contract wallet.yaml GET /wallet-reconciliation"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Sub-ledger total",
       "bindsTo": "WalletReconciliation",
       "columns": [
        "WalletReconciliation.subLedgerTotal"
       ],
       "operation": "getWalletReconciliation",
       "provenance": "contract wallet.yaml GET /wallet-reconciliation"
      },
      {
       "kind": "metricTile",
       "label": "General ledger total",
       "bindsTo": "WalletReconciliation",
       "columns": [
        "WalletReconciliation.generalLedgerTotal"
       ],
       "operation": "getWalletReconciliation",
       "provenance": "contract wallet.yaml GET /wallet-reconciliation"
      },
      {
       "kind": "metricTile",
       "label": "Acquirer total",
       "bindsTo": "WalletReconciliation",
       "columns": [
        "WalletReconciliation.acquirerTotal"
       ],
       "operation": "getWalletReconciliation",
       "provenance": "contract wallet.yaml GET /wallet-reconciliation"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Balance exceptions",
       "bindsTo": "WalletReconciliation.exceptions",
       "columns": [
        "WalletReconciliation.exceptions[].pair",
        "WalletReconciliation.exceptions[].difference",
        "WalletReconciliation.exceptions[].transactionIds",
        "WalletReconciliation.exceptions[].likelyCause"
       ],
       "operation": "getWalletReconciliation",
       "notes": "The pack's balance integrity check: any mismatch is a financial exception.",
       "provenance": "contract wallet.yaml GET /wallet-reconciliation"
      },
      {
       "kind": "dataTable",
       "label": "Sub-ledger entries",
       "columns": [
        "Ledger entry ID",
        "Wallet ID",
        "Customer / account",
        "Transaction ID",
        "Transaction type",
        "Credit bucket",
        "Credit lot",
        "Debit",
        "Credit",
        "Currency",
        "Balance before",
        "Balance after",
        "Source system",
        "Venue",
        "Channel",
        "Timestamp",
        "Financial status",
        "Related transaction"
       ],
       "notes": "No ledger-entry read is bound to this screen.",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 105"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The wallet sub-ledger balance list.",
   "error": "Could not load. Names which read failed and leaves the wallet sub-ledger balance untouched.",
   "emptyFirstRun": "No wallet sub-ledger balance yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the wallet sub-ledger balance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getWalletReconciliation",
    "contract": "wallet",
    "purpose": "Sub-ledger against the ledger",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1165",
   "workshopBoard": "wireframes/WS194 Wallet Configuration Backend Structure v1.0 Board 9.dc.html#bo-1165"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 104. 0 of 0 labels bound to a contract property; 0 of 35 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Layout drafted 29 September (VM close-out)** from pack Wallet_Configuration_Backend_Structure_v1.0.pdf p.105; contract wallet.yaml GET /wallet-reconciliation. Pack labels with no schema field yet (shown as plain labels): Sub-ledger entry read, Ledger entry ID, Credit bucket, Credit lot, Balance before / after, Source system, Financial status, Related transaction.",
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
  "id": "BO-1166",
  "name": "Multi-Source Reconciliation Configuration",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "9",
   "number": "04",
   "page": 105
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/multi-source-reconciliation-configuration-bo-1166",
   "component": "apps/venue-management-web/src/routes/orders-money/MultiSourceReconciliationConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1163"
   ],
   "exitTo": [
    "BO-1163"
   ],
   "transitions": [
    {
     "to": "BO-1163",
     "trigger": "Back to Wallet Finance & Liability Command Center",
     "provenance": "structural — pack board 9 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Reconcile wallet financial events across Wallet, Payments, Sales Channels and Finance. The supplied requirements specifically call for reconciliation of payment status between sales channels, the bank/payment gateway and the ticketing system. Reconciliation Sources",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Transaction ID",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 105 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Wallet ID",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 105 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Payment reference",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 105 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Order number",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 105 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Amount",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 105 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Currency",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 105 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Date",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 105 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 105 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Terminal",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 105 §Configure"
      },
      {
       "kind": "selectField",
       "label": "External reference",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 105 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Reconciliation Status",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 105 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Matched",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 105 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Partially Matched",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 105 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Unmatched",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 105 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Duplicate",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 105 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Amount Mismatch",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 105 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Currency Mismatch",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 105 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Missing Wallet Entry",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 105 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Missing Payment Entry",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 105 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Reconciliation Frequency",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 105 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Real-time",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 105 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Hourly",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 105 §Configure"
      },
      {
       "kind": "selectField",
       "label": "End of day",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 105 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Scheduled",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 105 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Manual",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 105 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Wallet Ledger",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 105 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "POS",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 105 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Payment Gateway",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 105 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Payment Server",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 105 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Gift Card",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 105 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Finance",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 105 §Support"
      },
      {
       "kind": "primaryButton",
       "label": "Save reconciliation sources",
       "operation": "setWalletReconciliationSources",
       "provenance": "contract wallet.yaml PUT /wallet-reconciliation-sources (decided 29 September, VM close-out)"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The multi-source reconciliation configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the multi-source reconciliation untouched.",
   "emptyFirstRun": "No multi-source reconciliation configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "getWalletReconciliation",
    "contract": "wallet",
    "purpose": "Three sources compared",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "setWalletReconciliationSources",
    "contract": "wallet",
    "purpose": "Save reconciliation sources",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1166",
   "workshopBoard": "wireframes/WS194 Wallet Configuration Backend Structure v1.0 Board 9.dc.html#bo-1166"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 105. 0 of 0 labels bound to a contract property; 31 of 45 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** still owed by a contract change: `setWalletReconciliationSources`.",
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
  "id": "BO-1167",
  "name": "Reconciliation Exception & Resolution Workbench",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "9",
   "number": "05",
   "page": 106
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/reconciliation-exception-resolution-workbench-bo-1167",
   "component": "apps/venue-management-web/src/routes/orders-money/ReconciliationExceptionResolutionWorkbench.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1163"
   ],
   "exitTo": [
    "BO-1163"
   ],
   "transitions": [
    {
     "to": "BO-1163",
     "trigger": "Back to Wallet Finance & Liability Command Center",
     "provenance": "structural — pack board 9 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide Finance and Operations with a governed workspace to investigate reconciliation failures. Exception Examples Payment successful / Wallet not funded Wallet funded / Payment failed Wallet debited / POS transaction missing Duplicate wallet debit Refund issued / Finance event missing Gift card redeemed / Liability unchanged",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 106 §Display"
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
       "label": "Every reconciliation exception resolution",
       "columns": [
        "Exception ID",
        "Transaction",
        "Wallet",
        "Source",
        "Expected amount",
        "Actual amount",
        "Difference",
        "Currency",
        "Age",
        "Priority",
        "Owner",
        "Status"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 106 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected reconciliation exception resolution",
       "bindsTo": null,
       "columns": [
        "Exception ID",
        "Transaction",
        "Wallet",
        "Source",
        "Expected amount",
        "Actual amount",
        "Difference",
        "Currency",
        "Age",
        "Priority",
        "Owner",
        "Status"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Workflow”.",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 106 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The reconciliation exception resolution list.",
   "error": "Could not load. Names which read failed and leaves the reconciliation exception resolution untouched.",
   "emptyFirstRun": "No reconciliation exception resolution yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the reconciliation exception resolution are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getWalletReconciliation",
    "contract": "wallet",
    "purpose": "Exceptions to resolve",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "adjustWallet",
    "contract": "wallet",
    "purpose": "Correct one",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getWallet",
     "listWalletTransactions",
     "listCreditLots"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "Exception ID",
    "Transaction",
    "Wallet",
    "Source",
    "Expected amount",
    "Actual amount"
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-1167",
   "workshopBoard": "wireframes/WS194 Wallet Configuration Backend Structure v1.0 Board 9.dc.html#bo-1167"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 106. 0 of 12 labels bound to a contract property; 12 of 43 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1168",
  "name": "Gift Card Liability Management",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "9",
   "number": "06",
   "page": 107
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/gift-card-liability-management-bo-1168",
   "component": "apps/venue-management-web/src/routes/orders-money/GiftCardLiabilityManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1163"
   ],
   "exitTo": [
    "BO-1163"
   ],
   "transitions": [
    {
     "to": "BO-1163",
     "trigger": "Back to Wallet Finance & Liability Command Center",
     "provenance": "structural — pack board 9 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide detailed financial control of outstanding gift-card obligations. Requirement 4.3.36 explicitly requires reporting of outstanding gift-card balances, redeemed value, unredeemed balances, expired balances and liability exposure by venue, tenant, currency and accounting period. Liability Dashboard",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 107 §Display"
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
       "label": "Every gift card liability",
       "columns": [
        "Gift Cards Issued",
        "Original Issued Value",
        "Outstanding Value",
        "Redeemed Value",
        "Partially Redeemed Value",
        "Unredeemed Value",
        "Expired Value",
        "Suspended Value",
        "Breakage",
        "Liability Exposure",
        "Breakdown",
        "Gift card program",
        "Tenant",
        "Venue",
        "Currency",
        "Issuance date",
        "Expiry date",
        "Accounting period",
        "Sales channel",
        "Corporate program",
        "Aging Analysis"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 107 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected gift card liability",
       "bindsTo": null,
       "columns": [
        "Gift Cards Issued",
        "Original Issued Value",
        "Outstanding Value",
        "Redeemed Value",
        "Partially Redeemed Value",
        "Unredeemed Value",
        "Expired Value",
        "Suspended Value",
        "Breakage",
        "Liability Exposure",
        "Breakdown",
        "Gift card program",
        "Tenant",
        "Venue",
        "Currency",
        "Issuance date",
        "Expiry date",
        "Accounting period",
        "Sales channel",
        "Corporate program",
        "Aging Analysis"
       ],
       "notes": null,
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 107 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The gift card liability list.",
   "error": "Could not load. Names which read failed and leaves the gift card liability untouched.",
   "emptyFirstRun": "No gift card liability yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the gift card liability are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getWalletLiability",
    "contract": "wallet",
    "purpose": "Gift card liability",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Gift Cards Issued",
    "Original Issued Value",
    "Outstanding Value",
    "Redeemed Value",
    "Partially Redeemed Value",
    "Unredeemed Value"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1168",
   "workshopBoard": "wireframes/WS194 Wallet Configuration Backend Structure v1.0 Board 9.dc.html#bo-1168"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 107. 0 of 21 labels bound to a contract property; 21 of 26 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1169",
  "name": "Breakage & Revenue Recognition Policy",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "9",
   "number": "07",
   "page": 108
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/breakage-revenue-recognition-policy-bo-1169",
   "component": "apps/venue-management-web/src/routes/orders-money/BreakageRevenueRecognitionPolicy.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1163"
   ],
   "exitTo": [
    "BO-1163"
   ],
   "transitions": [
    {
     "to": "BO-1163",
     "trigger": "Back to Wallet Finance & Liability Command Center",
     "provenance": "structural — pack board 9 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Gift Card) and no metric row",
  "purpose": "Configure the wallet-side business rules for expired/unredeemed gift-card value. Requirement 4.3.37 requires configurable expiration policies, gift-card breakage calculation and generation of revenue- recognition entries according to configured accounting policies. Breakage Configuration",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 108 §Gift Card"
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
       "label": "Every breakage revenue recognition",
       "columns": [
        "Original value → AED 500",
        "Redeemed → AED 350",
        "Expired remaining balance → AED 150"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 108 §Gift Card"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected breakage revenue recognition",
       "bindsTo": null,
       "columns": [
        "Original value → AED 500",
        "Redeemed → AED 350",
        "Expired remaining balance → AED 150"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Finance approval”, “Instead”.",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 108 §Gift Card"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The breakage revenue recognition list.",
   "error": "Could not load. Names which read failed and leaves the breakage revenue recognition untouched.",
   "emptyFirstRun": "No breakage revenue recognition yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the breakage revenue recognition are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setWalletAccountingMapping",
    "contract": "wallet",
    "purpose": "Breakage recognition policy",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getWalletLiability"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "Original value → AED 500",
    "Redeemed → AED 350",
    "Expired remaining balance → AED 150"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1169",
   "workshopBoard": "wireframes/WS194 Wallet Configuration Backend Structure v1.0 Board 9.dc.html#bo-1169"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 108. 0 of 3 labels bound to a contract property; 20 of 34 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1170",
  "name": "Wallet Financial Period & Closing Controls",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "9",
   "number": "08",
   "page": 109
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/wallet-financial-period-closing-controls-bo-1170",
   "component": "apps/venue-management-web/src/routes/orders-money/WalletFinancialPeriodClosingControls.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1163"
   ],
   "exitTo": [
    "BO-1163"
   ],
   "transitions": [
    {
     "to": "BO-1163",
     "trigger": "Back to Wallet Finance & Liability Command Center",
     "provenance": "structural — pack board 9 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population",
  "purpose": "Support controlled month-end and financial-period processing for wallet balances. Period Status Open → Closing → Under Review → Closed → Reopened with Authorization Pre-Close Validation Unreconciled transactions Pending refunds Pending reversals Pending adjustments Negative balances Missing accounting mappings Failed integrations Unprocessed expirations Gift-card breakage candidates Pending approvals Closing Snapshot",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Opening liability",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 109 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Funding",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 109 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Credits issued",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 109 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Redemption",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 109 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Refunds",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 109 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Transfers",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 109 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Adjustments",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 109 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Expiration",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 109 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Breakage",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 109 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Closing liability",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 109 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Controls",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 109 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Close by tenant",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 109 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Close by venue",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 109 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Close by currency",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 109 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Lock financial period",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 109 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Reopen with approval",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 109 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Carry exceptions forward",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 109 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Export close package",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 109 §Capture"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The wallet financial period configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the wallet financial period untouched.",
   "emptyFirstRun": "No wallet financial period configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "listFiscalPeriods",
    "contract": "finance",
    "purpose": "The period being closed",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "getWalletLiability",
    "contract": "wallet",
    "purpose": "Closing balance",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1170",
   "workshopBoard": "wireframes/WS194 Wallet Configuration Backend Structure v1.0 Board 9.dc.html#bo-1170"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 109. 0 of 0 labels bound to a contract property; 18 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1171",
  "name": "Wallet Analytics & Management Reporting",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "9",
   "number": "09",
   "page": 110
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/wallet-analytics-management-reporting-bo-1171",
   "component": "apps/venue-management-web/src/routes/orders-money/WalletAnalyticsManagementReporting.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1163"
   ],
   "exitTo": [
    "BO-1163"
   ],
   "transitions": [
    {
     "to": "BO-1163",
     "trigger": "Back to Wallet Finance & Liability Command Center",
     "provenance": "structural — pack board 9 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Compare; Analyze) and no metric row",
  "purpose": "Provide comprehensive analytics for wallet usage, financial performance and customer behavior. Requirement 4.3.17 requires intensive reporting across wallet credit types, including usage, balance and expiry, while 4.3.33 calls for dashboards covering balances, top-ups, redemptions, refunds, outstanding liability, expired value, usage by channel and transaction volume. Financial Analytics Wallet Liability Outstanding Stored Value Funding Redemption Refunds Transfers Expired Value Breakage Gift Card Liability Operational Analytics Active wallets Average wallet balance Average top-up Average spend Transaction volume Wallet usage frequency Dormant wallets Credit utilization Channel Analytics",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 110 §Compare"
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
       "label": "Every wallet analytics reporting",
       "columns": [
        "POS",
        "Mobile App",
        "B2C",
        "Kiosk",
        "Wearables",
        "API",
        "F&B",
        "Retail",
        "Attractions",
        "Customer Analytics",
        "Individual",
        "Family",
        "Membership",
        "Corporate",
        "Employee",
        "Guest",
        "AI Insights"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 110 §Compare"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected wallet analytics reporting",
       "bindsTo": null,
       "columns": [
        "POS",
        "Mobile App",
        "B2C",
        "Kiosk",
        "Wearables",
        "API",
        "F&B",
        "Retail",
        "Attractions",
        "Customer Analytics",
        "Individual",
        "Family",
        "Membership",
        "Corporate",
        "Employee",
        "Guest",
        "AI Insights"
       ],
       "notes": null,
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 110 §Compare"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The wallet analytics reporting list.",
   "error": "Could not load. Names which read failed and leaves the wallet analytics reporting untouched.",
   "emptyFirstRun": "No wallet analytics reporting yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the wallet analytics reporting are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getWalletLiability",
    "contract": "wallet",
    "purpose": "Management reporting",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "POS",
    "Mobile App",
    "B2C",
    "Kiosk",
    "Wearables",
    "API"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1171",
   "workshopBoard": "wireframes/WS194 Wallet Configuration Backend Structure v1.0 Board 9.dc.html#bo-1171"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 110. 0 of 17 labels bound to a contract property; 17 of 51 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1172",
  "name": "Finance Validation, Reporting & Audit Center",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "9",
   "number": "10",
   "page": 111
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/finance-validation-reporting-audit-center-bo-1172",
   "component": "apps/venue-management-web/src/routes/orders-money/FinanceValidationReportingAuditCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1163"
   ],
   "exitTo": [
    "BO-1163"
   ],
   "transitions": [
    {
     "to": "BO-1163",
     "trigger": "Back to Wallet Finance & Liability Command Center",
     "provenance": "structural — pack board 9 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Compare) and no metric row",
  "purpose": "Provide a final finance-control screen for validating wallet financial integrity and reviewing all financial configuration changes. Finance Health Check Complete the TICVAI Wallet module with the enterprise integration and governance layer that allows Wallet to operate securely across the entire TICVAI ecosystem and with approved third-party platforms. This board covers Wallet APIs, integration profiles, event/webhook orchestration, synchronization, integration monitoring, access/security governance, configuration versioning, approval and publication, audit governance, and end-to-end platform health. It directly addresses requirements 4.3.20 and 4.3.34, while consolidating governance and administration capabilities required across the full wallet scope. The source specifically requires integration with internal and external systems through APIs, including balance inquiry, transaction history, wallet funding, wallet payment, refund processing and wallet-to-wallet transfers.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 111 §Compare"
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
       "label": "Every finance validation reporting",
       "columns": [
        "Sum of Customer Wallet Balances",
        "against",
        "Wallet Sub-Ledger Liability",
        "Finance Interface Control Total",
        "Configuration Audit"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 111 §Compare"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected finance validation reporting",
       "bindsTo": null,
       "columns": [
        "Sum of Customer Wallet Balances",
        "against",
        "Wallet Sub-Ledger Liability",
        "Finance Interface Control Total",
        "Configuration Audit"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Validate”, “Record changes to”, “For every change record”, “So we now have”, “Administration”.",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 111 §Compare"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Run Finance Validation",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 111 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Review Exceptions",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 111 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Submit Close",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 111 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Approve Close",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 111 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Generate Liability Report",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 111 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Generate Reconciliation Report",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 111 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Export Audit",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 111 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Send to Finance",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 111 §Actions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The finance validation reporting list.",
   "error": "Could not load. Names which read failed and leaves the finance validation reporting untouched.",
   "emptyFirstRun": "No finance validation reporting yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the finance validation reporting are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getWalletReconciliation",
    "contract": "wallet",
    "purpose": "Validation and audit",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "getUnifiedReconciliation",
    "contract": "finance",
    "purpose": "Run the finance validation across every money source",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration): serves the pack action(s) Run Finance Validation; Submit Close; Approve Close; Generate Liability Report"
   },
   {
    "operationId": "beginPeriodClose",
    "contract": "finance",
    "purpose": "Submit the period for close",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration): serves the pack action(s) Run Finance Validation; Submit Close; Approve Close; Generate Liability Report",
    "invalidates": [
     "getUnifiedReconciliation"
    ]
   },
   {
    "operationId": "closeFiscalPeriod",
    "contract": "finance",
    "purpose": "Approve and lock the period",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration): serves the pack action(s) Run Finance Validation; Submit Close; Approve Close; Generate Liability Report",
    "invalidates": [
     "getUnifiedReconciliation"
    ]
   },
   {
    "operationId": "getWalletLiability",
    "contract": "wallet",
    "purpose": "Generate the wallet liability report",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration): serves the pack action(s) Run Finance Validation; Submit Close; Approve Close; Generate Liability Report"
   },
   {
    "operationId": "listFiscalPeriods",
    "contract": "finance",
    "purpose": "The fiscal periods to begin closing or close",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "Sum of Customer Wallet Balances",
    "against",
    "Wallet Sub-Ledger Liability",
    "Finance Interface Control Total",
    "Configuration Audit"
   ],
   "params": [
    {
     "name": "periodId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1172",
   "workshopBoard": "wireframes/WS194 Wallet Configuration Backend Structure v1.0 Board 9.dc.html#bo-1172"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 111. 0 of 5 labels bound to a contract property; 23 of 99 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Generate Reconciliation Report are choices sent by `getWalletReconciliation` (the screen's reconciliation read is the report); Run Finance Validation: `getUnifiedReconciliation`; Submit Close: `beginPeriodClose`; Approve Close: `closeFiscalPeriod`; Generate Liability Report: `getWalletLiability`; Review Exceptions dropped (navigation to the exception workbench); Export Audit dropped (export exists on the audit/reporting screens); Send to Finance … dropped (no hand-off step: wallet postings reach the ledger through the accounting mapping).",
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
 "beginPeriodClose": {
  "method": "POST",
  "path": "/fiscal-periods/{periodId}/begin-close",
  "contract": "finance",
  "summary": "Begin closing a period",
  "permission": "LEDGER_APPROVE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "FiscalPeriod"
 },
 "closeFiscalPeriod": {
  "method": "POST",
  "path": "/fiscal-periods/{periodId}/close",
  "contract": "finance",
  "summary": "Close a period and lock postings",
  "permission": "LEDGER_APPROVE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "PeriodCloseResult"
 },
 "getUnifiedReconciliation": {
  "method": "GET",
  "path": "/reconciliation/unified",
  "contract": "finance",
  "summary": "Every money source against the ledger, in one view",
  "permission": "LEDGER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
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
  "responds": "UnifiedReconciliation"
 },
 "getWalletLiability": {
  "method": "GET",
  "path": "/wallet-liability",
  "contract": "wallet",
  "summary": "What is outstanding, and what is breakage",
  "permission": "WALLET_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "asOf",
    "in": "query",
    "required": null
   },
   {
    "name": "groupBy",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "WalletLiabilityRow"
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
 "listFiscalPeriods": {
  "method": "GET",
  "path": "/fiscal-periods",
  "contract": "finance",
  "summary": "List fiscal periods",
  "permission": "LEDGER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [
   {
    "name": "legalEntityId",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
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
 "setWalletAccountingMapping": {
  "method": "PUT",
  "path": "/wallet-accounting",
  "contract": "wallet",
  "summary": "Which ledger account each credit type sits in",
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
  "requestBody": "WalletAccountingMapping",
  "responds": "WalletAccountingMapping"
 },
 "setWalletReconciliationSources": {
  "method": "PUT",
  "path": "/wallet-reconciliation-sources",
  "contract": "wallet",
  "summary": "Which sources the wallet reconciles against, matched how, and when",
  "permission": "WALLET_CONFIGURE",
  "offlineCapable": false,
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
  "requestBody": "WalletReconciliationSources",
  "responds": "WalletReconciliationSources"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "FiscalPeriod": {
  "x-ticvai-persistence": "ledger.fiscal_period + ledger.fiscal_period_event",
  "type": "object",
  "description": "`startDate` and `endDate` are days in the region's time zone: a posting belongs to the period when its `postedAt`, in that zone, falls on or between them.\n",
  "required": [
   "id",
   "legalEntityId",
   "name",
   "startDate",
   "endDate",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "legalEntityId": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string"
   },
   "startDate": {
    "type": "string",
    "format": "date",
    "description": "A day in the region's time zone, local midnight to local midnight."
   },
   "endDate": {
    "type": "string",
    "format": "date",
    "description": "A day in the region's time zone, local midnight to local midnight."
   },
   "status": {
    "$ref": "#/components/schemas/PeriodStatus"
   },
   "closedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "closedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "approvalRequestId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "The approval request a close or reopen is waiting on (`approvals`), routed to a finance approver (decided 28 September, audit R144). Null when nothing is waiting."
   },
   "events": {
    "type": "array",
    "description": "**Every step of the period's close, oldest first**: begin, abandon, close and reopen, each with who, when and (for abandon and reopen) why. A reopened period restates figures somebody has already reported, so the reason is kept, not just the latest status.\n",
    "items": {
     "$ref": "#/components/schemas/FiscalPeriodEvent"
    }
   }
  }
 },
 "FiscalPeriodEvent": {
  "type": "object",
  "description": "One step in a fiscal period's close. Written by the operation that took the step; never edited.",
  "required": [
   "action",
   "principalId",
   "occurredAt"
  ],
  "properties": {
   "action": {
    "type": "string",
    "enum": [
     "beginClose",
     "abandonClose",
     "close",
     "reopen"
    ]
   },
   "reason": {
    "type": "string",
    "nullable": true,
    "description": "Required by `abandonPeriodClose` and `reopenPeriod`; null for the other steps."
   },
   "principalId": {
    "type": "string",
    "format": "uuid",
    "description": "Who took the step."
   },
   "approverPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The approver of a `reopen`. Null for the other steps."
   },
   "occurredAt": {
    "type": "string",
    "format": "date-time"
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
 "PeriodCloseResult": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "fiscalPeriodId",
   "dryRun",
   "passed",
   "checks"
  ],
  "properties": {
   "fiscalPeriodId": {
    "type": "string",
    "format": "uuid"
   },
   "dryRun": {
    "type": "boolean"
   },
   "passed": {
    "type": "boolean"
   },
   "checks": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "check",
      "passed"
     ],
     "properties": {
      "check": {
       "type": "string",
       "enum": [
        "trialBalanceBalances",
        "noUnapprovedJournals",
        "noOpenShifts",
        "settlementsReconciled",
        "recognitionRunComplete",
        "priorPeriodClosed",
        "varianceExceptionsReviewed"
       ]
      },
      "passed": {
       "type": "boolean"
      },
      "detail": {
       "type": "string"
      },
      "blockingCount": {
       "type": "integer"
      }
     }
    }
   }
  }
 },
 "PeriodStatus": {
  "type": "string",
  "enum": [
   "open",
   "closing",
   "closed"
  ]
 },
 "UnifiedReconciliation": {
  "type": "object",
  "description": "4.2.19. **Four sources and the variances between them.** A view showing each balanced against itself has not reconciled anything.\n",
  "properties": {
   "from": {
    "type": "string",
    "format": "date",
    "description": "A day in the region's time zone, local midnight to local midnight."
   },
   "to": {
    "type": "string",
    "format": "date",
    "description": "A day in the region's time zone, local midnight to local midnight."
   },
   "sources": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "source": {
       "type": "string",
       "enum": [
        "pos",
        "gateway",
        "bank",
        "wallet",
        "ledger"
       ]
      },
      "providerName": {
       "type": "string",
       "nullable": true
      },
      "total": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "transactionCount": {
       "type": "integer"
      }
     }
    }
   },
   "variances": {
    "type": "array",
    "description": "**Where two sources disagree, named.** A discrepancy is usually the gap between two of them rather than inside one, and *\"out by 240\"* without saying between what is not actionable.\n",
    "items": {
     "type": "object",
     "properties": {
      "between": {
       "type": "array",
       "description": "The two sources that disagree, as named in `sources[].source`.",
       "minItems": 2,
       "maxItems": 2,
       "items": {
        "type": "string",
        "enum": [
         "pos",
         "gateway",
         "bank",
         "wallet",
         "ledger"
        ]
       }
      },
      "amount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "likelyCause": {
       "type": "string",
       "nullable": true
      }
     }
    }
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
 "WalletAccountingMapping": {
  "type": "object",
  "x-ticvai-persistence": "wallet.accounting_mapping",
  "description": "Boards 9.2 and 9.3. **Different credit types are different liabilities.**",
  "properties": {
   "mappings": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "creditTypeId": {
       "type": "string",
       "format": "uuid"
      },
      "liabilityAccountCode": {
       "type": "string"
      },
      "breakageRevenueAccountCode": {
       "type": "string",
       "nullable": true
      },
      "costAccountCode": {
       "type": "string",
       "nullable": true,
       "description": "**For credit the venue gave away.** Promotional credit is a marketing cost already incurred, not money owed back, and booking it as a liability overstates what the venue owes by whatever marketing did last quarter.\n"
      }
     }
    }
   },
   "breakagePolicy": {
    "type": "object",
    "properties": {
     "recogniseAfterMonths": {
      "type": "integer",
      "nullable": true,
      "description": "**Recognised on a policy, not on the expiry date.** Some jurisdictions require the liability to be held long after the printed expiry.\n"
     },
     "requiresApproval": {
      "type": "boolean",
      "default": true
     }
    }
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "WalletLiabilityRow": {
  "type": "object",
  "description": "Boards 9.5 and 9.6. **The number the finance director asks for.**",
  "properties": {
   "key": {
    "type": "string"
   },
   "label": {
    "type": "string"
   },
   "outstanding": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "expiringThisPeriod": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "breakageRecognised": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "walletCount": {
    "type": "integer"
   },
   "oldestLotAt": {
    "type": "string",
    "format": "date",
    "nullable": true
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
 },
 "WalletReconciliationSources": {
  "type": "object",
  "x-ticvai-persistence": "wallet.reconciliation_source",
  "description": "Board 9, p.105. **What `getWalletReconciliation` compares.** `walletLedger` is always on.",
  "required": [
   "sources"
  ],
  "properties": {
   "sources": {
    "type": "array",
    "minItems": 1,
    "items": {
     "type": "object",
     "required": [
      "kind",
      "enabled"
     ],
     "properties": {
      "kind": {
       "type": "string",
       "enum": [
        "walletLedger",
        "pos",
        "paymentGateway",
        "paymentServer",
        "giftCard",
        "finance"
       ]
      },
      "enabled": {
       "type": "boolean",
       "default": true
      },
      "matchKeys": {
       "type": "array",
       "description": "Fields a movement is matched on, e.g. transactionId, authorisationCode, terminalId, amount, businessDate.",
       "items": {
        "type": "string"
       }
      },
      "toleranceAmount": {
       "allOf": [
        {
         "$ref": "../shared/common.yaml#/components/schemas/Money"
        }
       ],
       "description": "A pair differing by no more than this is agreed. Default zero."
      },
      "schedule": {
       "type": "string",
       "enum": [
        "realTime",
        "hourly",
        "daily",
        "endOfBusinessDay"
       ],
       "default": "endOfBusinessDay"
      }
     }
    }
   },
   "scopePath": {
    "type": "string"
   }
  }
 }
}
```
