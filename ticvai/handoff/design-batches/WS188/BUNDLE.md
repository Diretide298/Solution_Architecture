# WS188 — Wallet Configuration Backend Structure v1.0 board 3

**10 screens · 11 operations · 8 schemas · 3 permissions**

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
| `BO-1103` | Stored Value & Credit Command Center | commandCentre | 2 | 0 | — |
| `BO-1104` | Credit Type Definition Studio | configEditor | 2 | 0 | — |
| `BO-1105` | Credit Issuance Rule Configuration | configEditor | 1 | 0 | — |
| `BO-1106` | Credit Usage & Eligibility Rules | listDetail | 1 | 0 | — |
| `BO-1107` | Consumption Priority Engine | configEditor | 2 | 0 | — |
| `BO-1108` | Expiry & Validity Policy Configuration | configEditor | 1 | 0 | — |
| `BO-1109` | FEFO & Credit Lot Management | configEditor | 1 | 0 | — |
| `BO-1110` | Split Tender & Multi-Credit Consumption | configEditor | 2 | 0 | — |
| `BO-1111` | Credit Expiry, Extension & Forfeiture Operations | listDetail | 1 | 0 | — |
| `BO-1112` | Consumption Simulator, Validation & Rule Publication | listDetail | 2 | 0 | — |

## Thin screens in this batch

**BO-1106, BO-1111, BO-1112 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-1103",
  "name": "Stored Value & Credit Command Center",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "3",
   "number": "01",
   "page": 23
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/stored-value-credit-command-center-bo-1103",
   "component": "apps/venue-management-web/src/routes/orders-money/StoredValueCreditCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-1104",
    "BO-1105",
    "BO-1106",
    "BO-1107",
    "BO-1108",
    "BO-1109",
    "BO-1110",
    "BO-1111",
    "BO-1112"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "BO-1104",
     "trigger": "Credit Type Definition Studio",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "carries": [
      "creditTypeId"
     ]
    },
    {
     "to": "BO-1105",
     "trigger": "Credit Issuance Rule Configuration",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "carries": [
      "creditTypeId"
     ]
    },
    {
     "to": "BO-1106",
     "trigger": "Credit Usage & Eligibility Rules",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "carries": [
      "creditTypeId"
     ]
    },
    {
     "to": "BO-1107",
     "trigger": "Consumption Priority Engine",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "BO-1108",
     "trigger": "Expiry & Validity Policy Configuration",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "carries": [
      "creditTypeId"
     ]
    },
    {
     "to": "BO-1109",
     "trigger": "FEFO & Credit Lot Management",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "BO-1110",
     "trigger": "Split Tender & Multi-Credit Consumption",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "BO-1111",
     "trigger": "Credit Expiry, Extension & Forfeiture Operations",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "BO-1112",
     "trigger": "Consumption Simulator, Validation & Rule Publication",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Show) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide administrators with a centralized operational overview of all stored value and digital credits held across TICVAI wallets.",
  "purposeNote": "Authorized administrators can monitor all wallet credit balances and trace aggregate figures to their originating wallet and ledger transactions.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search stored value credit",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 23 §Filter by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Tenant",
        "Venue",
        "Wallet type",
        "Credit type",
        "Customer/account type",
        "Currency",
        "Source",
        "Expiry period",
        "Status"
       ],
       "notes": "The pack filters this screen by tenant, venue, wallet type, credit type, customer/account type, currency and 3 more — which are present is a decision the pack already made.",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 23 §Filter by"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Total issued value",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 23 §Show"
      },
      {
       "kind": "metricTile",
       "label": "Current outstanding balance",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 23 §Show"
      },
      {
       "kind": "metricTile",
       "label": "Redeemed value",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 23 §Show"
      },
      {
       "kind": "metricTile",
       "label": "Expired value",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 23 §Show"
      },
      {
       "kind": "metricTile",
       "label": "Value expiring soon",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 23 §Show"
      },
      {
       "kind": "metricTile",
       "label": "Suspended/frozen value",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 23 §Show"
      },
      {
       "kind": "metricTile",
       "label": "Average wallet balance",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 23 §Show"
      },
      {
       "kind": "metricTile",
       "label": "Credits issued today",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 23 §Show"
      },
      {
       "kind": "metricTile",
       "label": "Credits consumed today",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 23 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The stored value credit list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the stored value credit untouched.",
   "emptyFirstRun": "No stored value credit yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the stored value credit are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCreditTypes",
    "contract": "wallet",
    "purpose": "Credit types and their balances",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "getWalletLiability",
    "contract": "wallet",
    "purpose": "Outstanding by type",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1103",
   "workshopBoard": "wireframes/WS188 Wallet Configuration Backend Structure v1.0 Board 3.dc.html#bo-1103"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 23. 0 of 9 labels bound to a contract property; 18 of 38 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1104",
  "name": "Credit Type Definition Studio",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "3",
   "number": "02",
   "page": 24
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/credit-type-definition-studio-bo-1104",
   "component": "apps/venue-management-web/src/routes/orders-money/CreditTypeDefinitionStudio.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1103"
   ],
   "exitTo": [
    "BO-1103"
   ],
   "transitions": [
    {
     "to": "BO-1103",
     "trigger": "Back to Stored Value & Credit Command Center",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§For each credit type configure) and no display directory — it is settings, not a population",
  "purpose": "Create and maintain the individual value buckets that can exist inside a TICVAI wallet. The source explicitly requires support for different digital wallet credit types such as Cash Credit, Bonus Credit, Redemption Tickets Credit and Rides Credit, with configurable usage criteria.",
  "purposeNote": "Administrators can introduce and configure new stored-value or entitlement credit types without software development.",
  "gaps": [
   {
    "operation": null,
    "why": "**Credit Type Definition Studio declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
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
       "label": "Credit name",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 24 §For each credit type configure"
      },
      {
       "kind": "selectField",
       "label": "Internal code",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 24 §For each credit type configure"
      },
      {
       "kind": "selectField",
       "label": "Description",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 24 §For each credit type configure"
      },
      {
       "kind": "selectField",
       "label": "Credit category",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 24 §For each credit type configure"
      },
      {
       "kind": "selectField",
       "label": "Monetary / non-monetary",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 24 §For each credit type configure"
      },
      {
       "kind": "selectField",
       "label": "Currency",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 24 §For each credit type configure"
      },
      {
       "kind": "selectField",
       "label": "Unit of measure",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 24 §For each credit type configure"
      },
      {
       "kind": "selectField",
       "label": "Decimal precision",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 24 §For each credit type configure"
      },
      {
       "kind": "selectField",
       "label": "Transferable",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 24 §For each credit type configure"
      },
      {
       "kind": "selectField",
       "label": "Refundable",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 24 §For each credit type configure"
      },
      {
       "kind": "selectField",
       "label": "Reversible",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 24 §For each credit type configure"
      },
      {
       "kind": "selectField",
       "label": "Top-up eligible",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 24 §For each credit type configure"
      },
      {
       "kind": "selectField",
       "label": "Customer purchasable",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 24 §For each credit type configure"
      },
      {
       "kind": "selectField",
       "label": "Promotional",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 24 §For each credit type configure"
      },
      {
       "kind": "selectField",
       "label": "Membership related",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 24 §For each credit type configure"
      },
      {
       "kind": "selectField",
       "label": "Gift related",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 24 §For each credit type configure"
      },
      {
       "kind": "selectField",
       "label": "Expirable",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 24 §For each credit type configure"
      },
      {
       "kind": "selectField",
       "label": "Shareable",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 24 §For each credit type configure"
      },
      {
       "kind": "selectField",
       "label": "Family eligible",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 24 §For each credit type configure"
      },
      {
       "kind": "selectField",
       "label": "Corporate eligible",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 24 §For each credit type configure"
      },
      {
       "kind": "selectField",
       "label": "Offline usage permitted",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 24 §For each credit type configure"
      },
      {
       "kind": "selectField",
       "label": "Customer-visible",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 24 §For each credit type configure"
      },
      {
       "kind": "selectField",
       "label": "Accounting classification",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 24 §For each credit type configure"
      },
      {
       "kind": "selectField",
       "label": "Liability classification",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 24 §For each credit type configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The credit type definition configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the credit type definition untouched.",
   "emptyFirstRun": "No credit type definition configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "createCreditType",
    "contract": "wallet",
    "purpose": "Define a credit type",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listCreditTypes"
    ]
   },
   {
    "operationId": "updateCreditType",
    "contract": "wallet",
    "purpose": "Change one",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listCreditTypes"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1104",
   "workshopBoard": "wireframes/WS188 Wallet Configuration Backend Structure v1.0 Board 3.dc.html#bo-1104"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 24. 0 of 0 labels bound to a contract property; 24 of 36 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1105",
  "name": "Credit Issuance Rule Configuration",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "3",
   "number": "03",
   "page": 25
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/credit-issuance-rule-configuration-bo-1105",
   "component": "apps/venue-management-web/src/routes/orders-money/CreditIssuanceRuleConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1103"
   ],
   "exitTo": [
    "BO-1103"
   ],
   "transitions": [
    {
     "to": "BO-1103",
     "trigger": "Back to Stored Value & Credit Command Center",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Define how credits enter a wallet after the wallet itself has already been funded or as the result of another TICVAI business process. This screen is deliberately different from Board 2: Board 2 controls funding/payment into a wallet; this screen controls the creation of individual credit buckets and entitlements.",
  "purposeNote": "Configured business events generate the correct wallet credits with appropriate source references, expiry rules and audit history.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Source event",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 25 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Credit type",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 25 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Fixed amount",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 25 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Percentage-based amount",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 25 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Quantity",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 25 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum issuance",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 25 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Customer eligibility",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 25 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Applicable wallet",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 25 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Applicable venue",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 25 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Effective dates",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 25 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Approval requirement",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 25 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Expiry policy",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 25 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Accounting treatment",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 25 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The credit issuance rule configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the credit issuance rule untouched.",
   "emptyFirstRun": "No credit issuance rule configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "updateCreditType",
    "contract": "wallet",
    "purpose": "How this credit is issued",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listCreditTypes"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1105",
   "workshopBoard": "wireframes/WS188 Wallet Configuration Backend Structure v1.0 Board 3.dc.html#bo-1105"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 25. 0 of 0 labels bound to a contract property; 13 of 40 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1106",
  "name": "Credit Usage & Eligibility Rules",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "3",
   "number": "04",
   "page": 26
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/credit-usage-eligibility-rules-bo-1106",
   "component": "apps/venue-management-web/src/routes/orders-money/CreditUsageEligibilityRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1103"
   ],
   "exitTo": [
    "BO-1103"
   ],
   "transitions": [
    {
     "to": "BO-1103",
     "trigger": "Back to Stored Value & Credit Command Center",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Define exactly where and under what conditions each wallet credit may be consumed.",
  "purposeNote": "The wallet engine permits redemption only when the transaction satisfies all applicable credit eligibility rules.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 26"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 26"
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
   "loading": "The credit usage eligibility list.",
   "error": "Could not load. Names which read failed and leaves the credit usage eligibility untouched.",
   "emptyFirstRun": "No credit usage eligibility yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the credit usage eligibility are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setCreditEligibilityRules",
    "contract": "wallet",
    "purpose": "Where it may be spent",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listCreditTypes"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1106",
   "workshopBoard": "wireframes/WS188 Wallet Configuration Backend Structure v1.0 Board 3.dc.html#bo-1106"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 26. 0 of 0 labels bound to a contract property; 0 of 43 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1107",
  "name": "Consumption Priority Engine",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "3",
   "number": "05",
   "page": 27
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/consumption-priority-engine-bo-1107",
   "component": "apps/venue-management-web/src/routes/orders-money/ConsumptionPriorityEngine.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1103"
   ],
   "exitTo": [
    "BO-1103"
   ],
   "transitions": [
    {
     "to": "BO-1103",
     "trigger": "Back to Stored Value & Credit Command Center",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Backend Configuration; Configure priority by) and no display directory — it is settings, not a population",
  "purpose": "Configure which wallet balance TICVAI should consume first when multiple eligible credits can pay for the same transaction. This directly addresses the source requirement that usage priority must be configurable—for example, consuming Cash Credit before Bonus Credit.",
  "purposeNote": "When multiple credits are eligible, TICVAI deterministically selects balances according to the published consumption policy.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Expiring Promotional Credit",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 27 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Bonus Credit",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 27 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Gift Card Credit",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 27 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Membership Credit",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 27 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Cash Credit",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 27 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "External Payment",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 27 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Membership Included Credit",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 27 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Ride Credit",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 27 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Tenant",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 27 §Configure priority by"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 27 §Configure priority by"
      },
      {
       "kind": "selectField",
       "label": "Wallet type",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 27 §Configure priority by"
      },
      {
       "kind": "selectField",
       "label": "Product",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 27 §Configure priority by"
      },
      {
       "kind": "selectField",
       "label": "Channel",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 27 §Configure priority by"
      },
      {
       "kind": "selectField",
       "label": "Customer type",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 27 §Configure priority by"
      },
      {
       "kind": "selectField",
       "label": "Membership",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 27 §Configure priority by"
      },
      {
       "kind": "selectField",
       "label": "Credit type",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 27 §Configure priority by"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Cash value last",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 27 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The consumption priority configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the consumption priority untouched.",
   "emptyFirstRun": "No consumption priority configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setCreditConsumptionPolicy",
    "contract": "wallet",
    "purpose": "Which credit is spent first",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getCreditConsumptionPolicy"
    ]
   },
   {
    "operationId": "getCreditConsumptionPolicy",
    "contract": "wallet",
    "purpose": "The order in force",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1107",
   "workshopBoard": "wireframes/WS188 Wallet Configuration Backend Structure v1.0 Board 3.dc.html#bo-1107"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 27. 0 of 0 labels bound to a contract property; 17 of 38 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Cash value last are choices sent by `setCreditConsumptionPolicy` (typeOrder puts cash credit last).",
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
  "id": "BO-1108",
  "name": "Expiry & Validity Policy Configuration",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "3",
   "number": "06",
   "page": 28
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/expiry-validity-policy-configuration-bo-1108",
   "component": "apps/venue-management-web/src/routes/orders-money/ExpiryValidityPolicyConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1103"
   ],
   "exitTo": [
    "BO-1103"
   ],
   "transitions": [
    {
     "to": "BO-1103",
     "trigger": "Back to Stored Value & Credit Command Center",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure how long each type of wallet value remains valid. The source requires configurable expiry periods for all credit types, including the ability to configure unlimited validity, particularly for cash credit.",
  "purposeNote": "Each issued credit receives the correct validity period based on the applicable published expiry policy.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Valid-from date",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 28 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Expiry calculation",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 28 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Grace period",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 28 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Expiry timezone",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 28 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Extension allowed",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 28 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Manual extension permission",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 28 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum extension",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 28 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Renewal behavior",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 28 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Remaining-value behavior",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 28 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Notification schedule",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 28 §Configure"
      },
      {
       "kind": "textField",
       "label": "Accounting treatment after expiry",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 28 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The expiry validity policy configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the expiry validity policy untouched.",
   "emptyFirstRun": "No expiry validity policy configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "updateCreditType",
    "contract": "wallet",
    "purpose": "Expiry and validity",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listCreditTypes"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1108",
   "workshopBoard": "wireframes/WS188 Wallet Configuration Backend Structure v1.0 Board 3.dc.html#bo-1108"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 28. 0 of 0 labels bound to a contract property; 11 of 33 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1109",
  "name": "FEFO & Credit Lot Management",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "3",
   "number": "07",
   "page": 29
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/fefo-credit-lot-management-bo-1109",
   "component": "apps/venue-management-web/src/routes/orders-money/FefoCreditLotManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1103"
   ],
   "exitTo": [
    "BO-1103"
   ],
   "transitions": [
    {
     "to": "BO-1103",
     "trigger": "Back to Stored Value & Credit Command Center",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Control consumption when multiple lots of the same credit type have different expiry dates. Requirement 4.3.19 specifically requires TICVAI to support FEFO — First Expiry, First Out.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "textField",
       "label": "Strategy per credit type",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 29 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Cross-lot consumption",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 29 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Partial lot consumption",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 29 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Lot locking",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 29 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Reserved balance handling",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 29 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Expired lot handling",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 29 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Reversal behavior",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 29 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Refund restoration behavior",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 29 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The fefo credit lot configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the fefo credit lot untouched.",
   "emptyFirstRun": "No fefo credit lot configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "listCreditLots",
    "contract": "wallet",
    "purpose": "The lots behind a balance",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1109",
   "workshopBoard": "wireframes/WS188 Wallet Configuration Backend Structure v1.0 Board 3.dc.html#bo-1109"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 29. 0 of 0 labels bound to a contract property; 8 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1110",
  "name": "Split Tender & Multi-Credit Consumption",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "3",
   "number": "08",
   "page": 30
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/split-tender-multi-credit-consumption-bo-1110",
   "component": "apps/venue-management-web/src/routes/orders-money/SplitTenderMultiCreditConsumption.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1103"
   ],
   "exitTo": [
    "BO-1103"
   ],
   "transitions": [
    {
     "to": "BO-1103",
     "trigger": "Back to Stored Value & Credit Command Center",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure; Options when balance is insufficient) and no display directory — it is settings, not a population",
  "purpose": "Configure transactions where multiple wallet credits and external payment methods are combined.",
  "purposeNote": "complete allocation record.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Multi-credit usage allowed",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 30 §Configure"
      },
      {
       "kind": "textField",
       "label": "Maximum credit types per transaction",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 30 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Partial redemption",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 30 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Wallet + card",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 30 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Wallet + cash",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 30 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Wallet + voucher",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 30 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Wallet + loyalty",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 30 §Configure"
      },
      {
       "kind": "textField",
       "label": "Wallet + gift card",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 30 §Configure"
      },
      {
       "kind": "textField",
       "label": "Wallet + multiple payment methods",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 30 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Minimum external payment",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 30 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Rounding",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 30 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Insufficient-wallet behavior",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 30 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Request external payment",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 30 §Options when balance is insufficient"
      },
      {
       "kind": "selectField",
       "label": "Reject transaction",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 30 §Options when balance is insufficient"
      },
      {
       "kind": "textField",
       "label": "Use next eligible wallet",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 30 §Options when balance is insufficient"
      },
      {
       "kind": "selectField",
       "label": "Ask customer",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 30 §Options when balance is insufficient"
      },
      {
       "kind": "textField",
       "label": "Allow authorized negative balance",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 30 §Options when balance is insufficient"
      },
      {
       "kind": "textField",
       "label": "Route to corporate wallet",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 30 §Options when balance is insufficient"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The split tender multi-credit configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the split tender multi-credit untouched.",
   "emptyFirstRun": "No split tender multi-credit configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setCreditConsumptionPolicy",
    "contract": "wallet",
    "purpose": "Split tender across credit types",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getCreditConsumptionPolicy"
    ]
   },
   {
    "operationId": "simulateCreditConsumption",
    "contract": "wallet",
    "purpose": "What a purchase would use",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1110",
   "workshopBoard": "wireframes/WS188 Wallet Configuration Backend Structure v1.0 Board 3.dc.html#bo-1110"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 30. 0 of 0 labels bound to a contract property; 18 of 31 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1111",
  "name": "Credit Expiry, Extension & Forfeiture Operations",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "3",
   "number": "09",
   "page": 31
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/credit-expiry-extension-forfeiture-operations-bo-1111",
   "component": "apps/venue-management-web/src/routes/orders-money/CreditExpiryExtensionForfeitureOperations.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1103"
   ],
   "exitTo": [
    "BO-1103"
   ],
   "transitions": [
    {
     "to": "BO-1103",
     "trigger": "Back to Stored Value & Credit Command Center",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide governed administrative management of credits approaching or reaching expiry.",
  "purposeNote": "Expiry-related administrative actions preserve the original credit history and create immutable audit entries.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 31 §Display"
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
       "label": "Every credit expiry extension",
       "columns": [
        "Expiring today",
        "Expiring in 7 days",
        "Expiring in 30 days",
        "Expired",
        "Extended",
        "Forfeited",
        "Suspended"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 31 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected credit expiry extension",
       "bindsTo": null,
       "columns": [
        "Expiring today",
        "Expiring in 7 days",
        "Expiring in 30 days",
        "Expired",
        "Extended",
        "Forfeited",
        "Suspended"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Authorized administrators may”, “Require”.",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 31 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The credit expiry extension list.",
   "error": "Could not load. Names which read failed and leaves the credit expiry extension untouched.",
   "emptyFirstRun": "No credit expiry extension yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the credit expiry extension are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "expireCreditLots",
    "contract": "wallet",
    "purpose": "Expire, extend or forfeit",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listCreditLots",
     "getWalletLiability"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "Expiring today",
    "Expiring in 7 days",
    "Expiring in 30 days",
    "Expired",
    "Extended",
    "Forfeited"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1111",
   "workshopBoard": "wireframes/WS188 Wallet Configuration Backend Structure v1.0 Board 3.dc.html#bo-1111"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 31. 0 of 7 labels bound to a contract property; 12 of 30 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1112",
  "name": "Consumption Simulator, Validation & Rule Publication",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "3",
   "number": "10",
   "page": 32
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/consumption-simulator-validation-rule-publication-bo-1112",
   "component": "apps/venue-management-web/src/routes/orders-money/ConsumptionSimulatorValidationRulePublication.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1103"
   ],
   "exitTo": [
    "BO-1103"
   ],
   "transitions": [
    {
     "to": "BO-1103",
     "trigger": "Back to Stored Value & Credit Command Center",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow administrators to test the entire credit engine before publishing new rules. This is important because the interaction between eligibility, expiry, FEFO and priority can otherwise create unintended wallet behavior. Test Scenario Configure TICVAI's shared-wallet architecture for families, parents and children, groups, schools, companies, corporate clients and other organizations. This board covers the requirements for family wallets, designated wallet owners, budget distribution, spending caps, shared balances, corporate spending wallets, permissions, and parent-card/child-card stored-value distribution. The central concept is that TICVAI should support both: Shared Balance Model — multiple authorized users consume one central balance. and Allocated Balance Model — the wallet owner distributes allowances/budgets to linked users while retaining centralized control.",
  "purposeNote": "No consumption-rule configuration becomes active until it passes validation and the required approval/publication workflow. Board 3 — Core Engine Flow The backend logic should effectively operate as:",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 32"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 32"
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
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "simulateCreditConsumption"
      },
      {
       "kind": "publishGate",
       "label": "What publishing changes",
       "notes": "**Takes effect at every till and reader immediately.** Credit types, consumption order and funding rules change for balances that already exist, not only for new ones.",
       "provenance": "authored — required by check-screens, 19 September 2026"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The consumption simulator validation list.",
   "error": "Could not load. Names which read failed and leaves the consumption simulator validation untouched.",
   "emptyFirstRun": "No consumption simulator validation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the consumption simulator validation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "simulateCreditConsumption",
    "contract": "wallet",
    "purpose": "Simulate",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "publishWalletConfiguration",
    "contract": "wallet",
    "purpose": "Validate and publish the rules",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listWalletTypes",
     "listCreditTypes"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1112",
   "workshopBoard": "wireframes/WS188 Wallet Configuration Backend Structure v1.0 Board 3.dc.html#bo-1112"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 32. 0 of 0 labels bound to a contract property; 0 of 79 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "createCreditType": {
  "method": "POST",
  "path": "/credit-types",
  "contract": "wallet",
  "summary": "Define a kind of credit, without a release",
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
  "requestBody": "CreditType",
  "responds": "CreditType"
 },
 "expireCreditLots": {
  "method": "POST",
  "path": "/credit-lots/expire",
  "contract": "wallet",
  "summary": "Expire, extend or forfeit credit that has run out of time",
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
  "responds": "CreditExpiryResult"
 },
 "getCreditConsumptionPolicy": {
  "method": "GET",
  "path": "/credit-consumption-policy",
  "contract": "wallet",
  "summary": "Which credit is spent first",
  "permission": "WALLET_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "CreditConsumptionPolicy"
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
 "publishWalletConfiguration": {
  "method": "POST",
  "path": "/wallet-configuration/publish",
  "contract": "wallet",
  "summary": "Validate and publish the wallet configuration as a version",
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
  "requestBody": null,
  "responds": "WalletConfigurationVersion"
 },
 "setCreditConsumptionPolicy": {
  "method": "PUT",
  "path": "/credit-consumption-policy",
  "contract": "wallet",
  "summary": "The order credit is drawn down in",
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
  "requestBody": "CreditConsumptionPolicy",
  "responds": "CreditConsumptionPolicy"
 },
 "setCreditEligibilityRules": {
  "method": "PUT",
  "path": "/credit-types/{creditTypeId}/eligibility",
  "contract": "wallet",
  "summary": "Where this credit may be spent, and on what",
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
  "requestBody": "CreditEligibility",
  "responds": "CreditEligibility"
 },
 "simulateCreditConsumption": {
  "method": "POST",
  "path": "/credit-consumption/simulate",
  "contract": "wallet",
  "summary": "Which credit this purchase would actually use",
  "permission": "WALLET_VIEW",
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
  "responds": "CreditAllocation"
 },
 "updateCreditType": {
  "method": "PUT",
  "path": "/credit-types/{creditTypeId}",
  "contract": "wallet",
  "summary": "Change a kind of credit",
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
  "requestBody": "CreditType",
  "responds": "CreditType"
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
 "CreditConsumptionPolicy": {
  "type": "object",
  "x-ticvai-persistence": "wallet.consumption_policy",
  "description": "Boards 3.5 and 3.7. **There is no neutral default**, which is why this is configuration.\n",
  "properties": {
   "strategy": {
    "type": "string",
    "enum": [
     "expiringFirst",
     "typePriority",
     "nonRefundableFirst",
     "manual"
    ],
    "default": "expiringFirst",
    "description": "**`expiringFirst` is the default because it is the one that does not quietly profit from the guest forgetting.**\n"
   },
   "typeOrder": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "withinTypeOrder": {
    "type": "string",
    "enum": [
     "fefo",
     "fifo",
     "lifo"
    ],
    "default": "fefo"
   },
   "allowSplitTender": {
    "type": "boolean",
    "default": true
   },
   "allowGuestChoice": {
    "type": "boolean",
    "default": false,
    "description": "**Whether a guest may override the order at the till.** Rarely enabled, and the venues that want it want it badly.\n"
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
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
 "CreditExpiryResult": {
  "type": "object",
  "description": "Board 3.9. **Expiry has an accounting consequence**, so the preview carries it.",
  "properties": {
   "lotsAffected": {
    "type": "integer"
   },
   "totalAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "breakageAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "walletsAffected": {
    "type": "integer"
   },
   "applied": {
    "type": "boolean"
   },
   "asOf": {
    "type": "string",
    "format": "date"
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
 "WalletConfigurationVersion": {
  "type": "object",
  "x-ticvai-persistence": "wallet.configuration_version",
  "description": "Boards 1.10 and 10.8. **Ten boards of configuration that interact.**",
  "properties": {
   "version": {
    "type": "integer"
   },
   "publishedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "publishedBy": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "note": {
    "type": "string",
    "nullable": true
   },
   "findings": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "severity": {
       "type": "string",
       "enum": [
        "blocking",
        "warning"
       ]
      },
      "code": {
       "type": "string"
      },
      "message": {
       "type": "string"
      }
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
 }
}
```
