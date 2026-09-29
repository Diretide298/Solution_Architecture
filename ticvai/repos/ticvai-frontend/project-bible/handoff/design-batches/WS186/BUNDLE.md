# WS186 — Wallet Configuration Backend Structure v1.0 board 1

**10 screens · 12 operations · 8 schemas · 3 permissions**

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
| `BO-1083` | Wallet Command Center | configEditor | 2 | 0 | — |
| `BO-1084` | Wallet Type Library | configEditor | 2 | 0 | — |
| `BO-1085` | Wallet Creation & Provisioning Rules | configEditor | 2 | 0 | — |
| `BO-1086` | Wallet Ownership & Account Association | configEditor | 4 | 0 | — |
| `BO-1087` | Wallet Currency & Monetary Configuration | configEditor | 1 | 0 | — |
| `BO-1088` | Credit & Balance Type Configuration | configEditor | 3 | 0 | — |
| `BO-1089` | Wallet Feature Profile | listDetail | 1 | 0 | — |
| `BO-1090` | Wallet Lifecycle Configuration | configEditor | 1 | 0 | — |
| `BO-1091` | Wallet Numbering, Identity & Digital Credentials | configEditor | 2 | 0 | — |
| `BO-1092` | Wallet Configuration Preview, Validation & Publication | configEditor | 1 | 0 | — |

## Thin screens in this batch

**BO-1089 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-1083",
  "name": "Wallet Command Center",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "1",
   "number": "01",
   "page": 3
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/wallet-command-center-bo-1083",
   "component": "apps/venue-management-web/src/routes/orders-money/WalletCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-1084",
    "BO-1085",
    "BO-1086",
    "BO-1087",
    "BO-1088",
    "BO-1089",
    "BO-1090",
    "BO-1091",
    "BO-1092"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "BO-1084",
     "trigger": "Wallet Type Library",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "BO-1085",
     "trigger": "Wallet Creation & Provisioning Rules",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "carries": [
      "walletTypeId"
     ]
    },
    {
     "to": "BO-1086",
     "trigger": "Wallet Ownership & Account Association",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "carries": [
      "walletTypeId"
     ]
    },
    {
     "to": "BO-1087",
     "trigger": "Wallet Currency & Monetary Configuration",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "carries": [
      "walletTypeId"
     ]
    },
    {
     "to": "BO-1088",
     "trigger": "Credit & Balance Type Configuration",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "BO-1089",
     "trigger": "Wallet Feature Profile",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "carries": [
      "walletTypeId"
     ]
    },
    {
     "to": "BO-1090",
     "trigger": "Wallet Lifecycle Configuration",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "carries": [
      "walletTypeId"
     ]
    },
    {
     "to": "BO-1091",
     "trigger": "Wallet Numbering, Identity & Digital Credentials",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "carries": [
      "walletTypeId"
     ]
    },
    {
     "to": "BO-1092",
     "trigger": "Wallet Configuration Preview, Validation & Publication",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Backend Configuration) and no display directory — it is settings, not a population",
  "purpose": "Provide administrators with the central operational and configuration overview of all wallet products across the TICVAI platform.",
  "purposeNote": "Authorized users can obtain a consolidated wallet operational view and navigate directly to permitted wallet configuration and administrative actions.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Active",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 3 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Pending Activation",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 3 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Suspended",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 3 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Blocked",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 3 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Expired",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 3 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Closed",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 3 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Cash value",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 3 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Bonus value",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 3 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Gift card value",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 3 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Promotional credits",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 3 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Ride credits",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 3 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Redemption credits",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 3 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Membership credits",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 3 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Top-ups",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 3 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Spending",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 3 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Refunds",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 3 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Transfers",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 3 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Adjustments",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 3 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Tenant",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 3 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 3 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Wallet type",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 3 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Currency",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 3 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Customer type",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 3 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Wallet status",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 3 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Balance range",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 3 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Date range",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 3 §Backend Configuration"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The wallet configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the wallet untouched.",
   "emptyFirstRun": "No wallet configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "listWalletTypes",
    "contract": "wallet",
    "purpose": "Wallet types in use",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "getWalletLiability",
    "contract": "wallet",
    "purpose": "What is outstanding",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1083",
   "workshopBoard": "wireframes/WS186 Wallet Configuration Backend Structure v1.0 Board 1.dc.html#bo-1083"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 3. 0 of 0 labels bound to a contract property; 26 of 43 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1084",
  "name": "Wallet Type Library",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "1",
   "number": "02",
   "page": 4
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/wallet-type-library-bo-1084",
   "component": "apps/venue-management-web/src/routes/orders-money/WalletTypeLibrary.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1083"
   ],
   "exitTo": [
    "BO-1083"
   ],
   "transitions": [
    {
     "to": "BO-1083",
     "trigger": "Back to Wallet Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Backend Configuration; Each wallet type can configure) and no display directory — it is settings, not a population",
  "purpose": "Create and maintain reusable wallet types used throughout TICVAI.",
  "purposeNote": "Administrators can configure reusable wallet types without modifying application code.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Guest Wallet",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 4 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Registered Customer Wallet",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 4 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Family Wallet",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 4 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Parent Wallet",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 4 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Child Wallet",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 4 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Corporate Wallet",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 4 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "School Wallet",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 4 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Employee Wallet",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 4 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Membership Wallet",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 4 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Event Wallet",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 4 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Resort Wallet",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 4 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Cashless Venue Wallet",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 4 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Closed-Loop Wallet",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 4 §Backend Configuration"
      },
      {
       "kind": "selectField",
       "label": "Wallet name",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 4 §Each wallet type can configure"
      },
      {
       "kind": "selectField",
       "label": "Internal wallet code",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 4 §Each wallet type can configure"
      },
      {
       "kind": "selectField",
       "label": "Description",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 4 §Each wallet type can configure"
      },
      {
       "kind": "selectField",
       "label": "Wallet category",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 4 §Each wallet type can configure"
      },
      {
       "kind": "selectField",
       "label": "Owning tenant",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 4 §Each wallet type can configure"
      },
      {
       "kind": "selectField",
       "label": "Applicable venue",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 4 §Each wallet type can configure"
      },
      {
       "kind": "selectField",
       "label": "Supported customer/account type",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 4 §Each wallet type can configure"
      },
      {
       "kind": "selectField",
       "label": "Supported currencies",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 4 §Each wallet type can configure"
      },
      {
       "kind": "selectField",
       "label": "Stored-value capability",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 4 §Each wallet type can configure"
      },
      {
       "kind": "selectField",
       "label": "Transfer capability",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 4 §Each wallet type can configure"
      },
      {
       "kind": "selectField",
       "label": "Top-up capability",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 4 §Each wallet type can configure"
      },
      {
       "kind": "selectField",
       "label": "Refund capability",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 4 §Each wallet type can configure"
      },
      {
       "kind": "selectField",
       "label": "Gift card support",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 4 §Each wallet type can configure"
      },
      {
       "kind": "selectField",
       "label": "Voucher support",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 4 §Each wallet type can configure"
      },
      {
       "kind": "selectField",
       "label": "Membership credit support",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 4 §Each wallet type can configure"
      },
      {
       "kind": "selectField",
       "label": "Wearable support",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 4 §Each wallet type can configure"
      },
      {
       "kind": "selectField",
       "label": "Online usage",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 4 §Each wallet type can configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The wallet type configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the wallet type untouched.",
   "emptyFirstRun": "No wallet type configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "listWalletTypes",
    "contract": "wallet",
    "purpose": "The type library",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "createWalletType",
    "contract": "wallet",
    "purpose": "Define a type",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listWalletTypes"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1084",
   "workshopBoard": "wireframes/WS186 Wallet Configuration Backend Structure v1.0 Board 1.dc.html#bo-1084"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 4. 0 of 0 labels bound to a contract property; 36 of 43 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1085",
  "name": "Wallet Creation & Provisioning Rules",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "1",
   "number": "03",
   "page": 5
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/wallet-creation-provisioning-rules-bo-1085",
   "component": "apps/venue-management-web/src/routes/orders-money/WalletCreationProvisioningRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1083"
   ],
   "exitTo": [
    "BO-1083"
   ],
   "transitions": [
    {
     "to": "BO-1083",
     "trigger": "Back to Wallet Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Define how and when TICVAI automatically or manually creates a wallet.",
  "purposeNote": "The system creates wallets according to configurable business triggers, validation rules and authorization controls.",
  "gaps": [
   {
    "operation": null,
    "why": "**Wallet Creation & Provisioning Rules declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
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
       "kind": "textField",
       "label": "Automatic vs manual creation",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 5 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Required customer information",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 5 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Anonymous wallet permission",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 5 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Account verification requirement",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 5 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Mobile verification",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 5 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Email verification",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 5 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Digital ID verification",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 5 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Default wallet type",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 5 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Default currency",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 5 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Default status",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 5 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Initial credit",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 5 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Initial promotional value",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 5 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Wallet validity",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 5 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Wallet activation rules",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 5 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Duplicate-wallet handling",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 5 §Configure"
      },
      {
       "kind": "textField",
       "label": "One wallet per customer vs multiple wallets",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 5 §Configure"
      },
      {
       "kind": "textField",
       "label": "Maximum wallets per account",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 5 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The wallet creation provisioning configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the wallet creation provisioning untouched.",
   "emptyFirstRun": "No wallet creation provisioning configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "createWalletType",
    "contract": "wallet",
    "purpose": "Provisioning rules for a type",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listWalletTypes"
    ]
   },
   {
    "operationId": "updateWalletType",
    "contract": "wallet",
    "purpose": "Change them",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listWalletTypes"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1085",
   "workshopBoard": "wireframes/WS186 Wallet Configuration Backend Structure v1.0 Board 1.dc.html#bo-1085"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 5. 0 of 0 labels bound to a contract property; 17 of 33 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "walletTypeId",
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
  "id": "BO-1086",
  "name": "Wallet Ownership & Account Association",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "1",
   "number": "04",
   "page": 6
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/wallet-ownership-account-association-bo-1086",
   "component": "apps/venue-management-web/src/routes/orders-money/WalletOwnershipAccountAssociation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1083"
   ],
   "exitTo": [
    "BO-1083"
   ],
   "transitions": [
    {
     "to": "BO-1083",
     "trigger": "Back to Wallet Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure roles such as) and no display directory — it is settings, not a population",
  "purpose": "Configure which customer, family or organization owns and controls a wallet.",
  "purposeNote": "Wallet ownership and delegated access can be configured independently of the wallet balance.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Wallet Owner",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 6 §Configure roles such as"
      },
      {
       "kind": "selectField",
       "label": "Wallet Administrator",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 6 §Configure roles such as"
      },
      {
       "kind": "selectField",
       "label": "Authorized User",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 6 §Configure roles such as"
      },
      {
       "kind": "selectField",
       "label": "Dependant",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 6 §Configure roles such as"
      },
      {
       "kind": "selectField",
       "label": "Viewer",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 6 §Configure roles such as"
      },
      {
       "kind": "selectField",
       "label": "Finance Controller",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 6 §Configure roles such as"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "One wallet → multiple users",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 6 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Primary wallet owner",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 6 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Delegated wallet administration",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 6 §Support"
      },
      {
       "kind": "banner",
       "label": "Permissions this screen separates",
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** View balance, Top up, Spend, Transfer, Receive transfer, View transactions, Add payment instruments, Add/remove wearables, Configure spending limits, Freeze wallet, Receive notifications. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 6 §Permissions can determine who may"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The wallet ownership account configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the wallet ownership account untouched.",
   "emptyFirstRun": "No wallet ownership account configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "getWallet",
    "contract": "wallet",
    "purpose": "The wallet and its owner",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "updateWalletType",
    "contract": "wallet",
    "purpose": "Ownership and association rules",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listWalletTypes"
    ]
   },
   {
    "operationId": "setSharedWalletMembers",
    "contract": "wallet",
    "purpose": "Set the primary owner and delegated administrators of a shared wallet",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration): serves the pack action(s) Primary wallet owner, Delegated wallet administration",
    "invalidates": [
     "getWallet"
    ]
   },
   {
    "operationId": "listSharedWallets",
    "contract": "wallet",
    "purpose": "The shared wallets whose members are set",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1086",
   "workshopBoard": "wireframes/WS186 Wallet Configuration Backend Structure v1.0 Board 1.dc.html#bo-1086"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 6. 0 of 0 labels bound to a contract property; 20 of 35 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** One wallet → multiple users are choices sent by `updateWalletType` (sharedStructureAllowed, holderMayDifferFromOwner); Primary wallet owner, Delegated wallet administration: `setSharedWalletMembers`.",
  "entryState": {
   "params": [
    {
     "name": "subjectId",
     "from": "navigation"
    },
    {
     "name": "walletTypeId",
     "from": "navigation"
    },
    {
     "name": "sharedWalletId",
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
  "id": "BO-1087",
  "name": "Wallet Currency & Monetary Configuration",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "1",
   "number": "05",
   "page": 7
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/wallet-currency-monetary-configuration-bo-1087",
   "component": "apps/venue-management-web/src/routes/orders-money/WalletCurrencyMonetaryConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1083"
   ],
   "exitTo": [
    "BO-1083"
   ],
   "transitions": [
    {
     "to": "BO-1083",
     "trigger": "Back to Wallet Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Define currencies and monetary rules applicable to wallet balances.",
  "purposeNote": "Wallet transactions consistently follow configured currency, conversion and rounding rules.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Base wallet currency",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Permitted currencies",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Multi-currency wallet enabled/disabled",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Venue currency",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Settlement currency",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Currency conversion permitted",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Exchange-rate source",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Conversion timing",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Exchange-rate markup",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Decimal precision",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Minimum wallet balance",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum wallet balance",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Negative balance permission",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Zero-balance behavior",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Currency-specific limits",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Rounding policy",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 7 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The wallet currency monetary configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the wallet currency monetary untouched.",
   "emptyFirstRun": "No wallet currency monetary configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "updateWalletType",
    "contract": "wallet",
    "purpose": "Currency and monetary limits",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listWalletTypes"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1087",
   "workshopBoard": "wireframes/WS186 Wallet Configuration Backend Structure v1.0 Board 1.dc.html#bo-1087"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 7. 0 of 0 labels bound to a contract property; 16 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "walletTypeId",
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
  "id": "BO-1088",
  "name": "Credit & Balance Type Configuration",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "1",
   "number": "06",
   "page": 8
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/credit-balance-type-configuration-bo-1088",
   "component": "apps/venue-management-web/src/routes/orders-money/CreditBalanceTypeConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1083"
   ],
   "exitTo": [
    "BO-1083"
   ],
   "transitions": [
    {
     "to": "BO-1083",
     "trigger": "Back to Wallet Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Administrators can define; For each balance type configure) and no display directory — it is settings, not a population",
  "purpose": "Configure all value types that may be stored inside a TICVAI wallet. The attached requirements explicitly call for multiple wallet credit types including Cash Credit, Bonus Credit, Redemption Tickets Credit and Rides Credit.",
  "purposeNote": "New wallet credit types can be introduced through configuration without development changes.",
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
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 8 §Administrators can define"
      },
      {
       "kind": "selectField",
       "label": "Refund Credit",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 8 §Administrators can define"
      },
      {
       "kind": "selectField",
       "label": "Bonus Credit",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 8 §Administrators can define"
      },
      {
       "kind": "selectField",
       "label": "Promotional Credit",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 8 §Administrators can define"
      },
      {
       "kind": "selectField",
       "label": "Gift Card Credit",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 8 §Administrators can define"
      },
      {
       "kind": "selectField",
       "label": "Membership Credit",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 8 §Administrators can define"
      },
      {
       "kind": "selectField",
       "label": "Loyalty Credit",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 8 §Administrators can define"
      },
      {
       "kind": "selectField",
       "label": "Ride Credit",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 8 §Administrators can define"
      },
      {
       "kind": "selectField",
       "label": "Attraction Credit",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 8 §Administrators can define"
      },
      {
       "kind": "selectField",
       "label": "Redemption Ticket Credit",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 8 §Administrators can define"
      },
      {
       "kind": "selectField",
       "label": "Meal Credit",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 8 §Administrators can define"
      },
      {
       "kind": "selectField",
       "label": "Retail Credit",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 8 §Administrators can define"
      },
      {
       "kind": "selectField",
       "label": "Parking Credit",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 8 §Administrators can define"
      },
      {
       "kind": "selectField",
       "label": "Event Credit",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 8 §Administrators can define"
      },
      {
       "kind": "selectField",
       "label": "Custom Credit Type",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 8 §Administrators can define"
      },
      {
       "kind": "selectField",
       "label": "Balance code",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 8 §For each balance type configure"
      },
      {
       "kind": "selectField",
       "label": "Display name",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 8 §For each balance type configure"
      },
      {
       "kind": "selectField",
       "label": "Monetary/non-monetary",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 8 §For each balance type configure"
      },
      {
       "kind": "selectField",
       "label": "Currency applicable",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 8 §For each balance type configure"
      },
      {
       "kind": "selectField",
       "label": "Transferable",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 8 §For each balance type configure"
      },
      {
       "kind": "selectField",
       "label": "Refundable",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 8 §For each balance type configure"
      },
      {
       "kind": "selectField",
       "label": "Top-up allowed",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 8 §For each balance type configure"
      },
      {
       "kind": "selectField",
       "label": "Promotional",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 8 §For each balance type configure"
      },
      {
       "kind": "selectField",
       "label": "Expirable",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 8 §For each balance type configure"
      },
      {
       "kind": "selectField",
       "label": "Redeemable channels",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 8 §For each balance type configure"
      },
      {
       "kind": "selectField",
       "label": "Applicable products",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 8 §For each balance type configure"
      },
      {
       "kind": "selectField",
       "label": "Applicable venues",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 8 §For each balance type configure"
      },
      {
       "kind": "selectField",
       "label": "Accounting classification",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 8 §For each balance type configure"
      },
      {
       "kind": "selectField",
       "label": "Liability classification",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 8 §For each balance type configure"
      },
      {
       "kind": "selectField",
       "label": "Consumption priority",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 8 §For each balance type configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The credit balance type configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the credit balance type untouched.",
   "emptyFirstRun": "No credit balance type configured yet. Carries the create action and says what the platform does in the meantime.",
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
    "purpose": "Define a credit type, without a release",
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-1088",
   "workshopBoard": "wireframes/WS186 Wallet Configuration Backend Structure v1.0 Board 1.dc.html#bo-1088"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 8. 0 of 0 labels bound to a contract property; 31 of 35 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1089",
  "name": "Wallet Feature Profile",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "1",
   "number": "07",
   "page": 8
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/wallet-feature-profile-bo-1089",
   "component": "apps/venue-management-web/src/routes/orders-money/WalletFeatureProfile.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1083"
   ],
   "exitTo": [
    "BO-1083"
   ],
   "transitions": [
    {
     "to": "BO-1083",
     "trigger": "Back to Wallet Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Control which capabilities are available for each wallet type.",
  "purposeNote": "Features can be centrally enabled or restricted based on wallet context.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 8"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 8"
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
       "impliedBy": "updateWalletType",
       "label": "Save wallet type",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "updateWalletType"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The wallet feature profile list.",
   "error": "Could not load. Names which read failed and leaves the wallet feature profile untouched.",
   "emptyFirstRun": "No wallet feature profile yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the wallet feature profile are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "updateWalletType",
    "contract": "wallet",
    "purpose": "Which features this wallet type has",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listWalletTypes"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1089",
   "workshopBoard": "wireframes/WS186 Wallet Configuration Backend Structure v1.0 Board 1.dc.html#bo-1089"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 8. 0 of 0 labels bound to a contract property; 0 of 29 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "walletTypeId",
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
  "id": "BO-1090",
  "name": "Wallet Lifecycle Configuration",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "1",
   "number": "08",
   "page": 9
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/wallet-lifecycle-configuration-bo-1090",
   "component": "apps/venue-management-web/src/routes/orders-money/WalletLifecycleConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1083"
   ],
   "exitTo": [
    "BO-1083"
   ],
   "transitions": [
    {
     "to": "BO-1083",
     "trigger": "Back to Wallet Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Govern the complete wallet lifecycle from creation through closure.",
  "purposeNote": "Every status transition is controlled by permissions, configurable business rules and audit logging.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Activation conditions",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 9 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Verification requirements",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 9 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Suspension reasons",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 9 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Block reasons",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 9 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Expiry behavior",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 9 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Dormancy rules",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 9 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Closure requirements",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 9 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Remaining balance handling",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 9 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Reactivation rules",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 9 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Archival period",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 9 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Data retention period",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 9 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The wallet lifecycle configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the wallet lifecycle untouched.",
   "emptyFirstRun": "No wallet lifecycle configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "updateWalletType",
    "contract": "wallet",
    "purpose": "Lifecycle states and transitions",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listWalletTypes"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1090",
   "workshopBoard": "wireframes/WS186 Wallet Configuration Backend Structure v1.0 Board 1.dc.html#bo-1090"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 9. 0 of 0 labels bound to a contract property; 11 of 21 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "walletTypeId",
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
  "id": "BO-1091",
  "name": "Wallet Numbering, Identity & Digital Credentials",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "1",
   "number": "09",
   "page": 10
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/wallet-numbering-identity-digital-credentials-bo-1091",
   "component": "apps/venue-management-web/src/routes/orders-money/WalletNumberingIdentityDigitalCredentials.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1083"
   ],
   "exitTo": [
    "BO-1083"
   ],
   "transitions": [
    {
     "to": "BO-1083",
     "trigger": "Back to Wallet Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure how wallets are uniquely identified across TICVAI.",
  "purposeNote": "Wallet credentials are uniquely generated, securely managed and independently replaceable without changing the underlying wallet.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Wallet ID structure",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 10 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Wallet number format",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 10 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Prefix/suffix",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 10 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Tenant code",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 10 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Venue code",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 10 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Sequential/random identifier",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 10 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Customer-facing wallet reference",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 10 §Configure"
      },
      {
       "kind": "selectField",
       "label": "QR identifier",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 10 §Configure"
      },
      {
       "kind": "selectField",
       "label": "NFC identifier",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 10 §Configure"
      },
      {
       "kind": "selectField",
       "label": "RFID identifier",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 10 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Wearable token",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 10 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Mobile credential",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 10 §Configure"
      },
      {
       "kind": "textField",
       "label": "Digital Key / Digital ID",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 10 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Tokenization",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 10 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Credential expiry",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 10 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Credential replacement",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 10 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Lost/stolen credential handling",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 10 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The wallet numbering identity configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the wallet numbering identity untouched.",
   "emptyFirstRun": "No wallet numbering identity configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "updateWalletType",
    "contract": "wallet",
    "purpose": "Numbering and identity",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listWalletTypes"
    ]
   },
   {
    "operationId": "linkWalletCredential",
    "contract": "wallet",
    "purpose": "Digital credentials",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getWallet"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1091",
   "workshopBoard": "wireframes/WS186 Wallet Configuration Backend Structure v1.0 Board 1.dc.html#bo-1091"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 10. 0 of 0 labels bound to a contract property; 17 of 30 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "walletTypeId",
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
  "id": "BO-1092",
  "name": "Wallet Configuration Preview, Validation & Publication",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "1",
   "number": "10",
   "page": 11
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/wallet-configuration-preview-validation-publication-bo-1092",
   "component": "apps/venue-management-web/src/routes/orders-money/WalletConfigurationPreviewValidationPublication.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1083"
   ],
   "exitTo": [
    "BO-1083"
   ],
   "transitions": [
    {
     "to": "BO-1083",
     "trigger": "Back to Wallet Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Show configuration summary covering; Every configuration publication records) and no display directory — it is settings, not a population",
  "purpose": "Provide a governed final validation step before wallet configuration becomes operational. Configure how value enters a TICVAI wallet across digital and physical channels, including manual top-ups, payment-method funding, automatic reload, recurring funding, authorization controls, reversals, limits, and operational monitoring. This board directly covers the wallet requirements for multiple funding methods, auto-reload, recurring funding, configurable limits, security controls, and complete transaction auditing.",
  "purposeNote": "No wallet configuration can become operational unless validation, permissions and applicable approval requirements have been successfully completed. This makes Board 1 the foundation of the entire wallet engine, rather than jumping immediately into transactions. Once these 10 screens exist, Boards 2–10 can reuse the Wallet Type, Credit Type, Currency, Ownership and Lifecycle objects without recreating them. The next board should therefore be Board 2 — Funding, Top-Up & Reload Management, covering cash/card top-up, payment-source rules, auto-reload, recurring funding, funding authorization, rev",
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
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 11 §Show configuration summary covering"
      },
      {
       "kind": "selectField",
       "label": "Ownership model",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 11 §Show configuration summary covering"
      },
      {
       "kind": "selectField",
       "label": "Currency",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 11 §Show configuration summary covering"
      },
      {
       "kind": "selectField",
       "label": "Credit types",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 11 §Show configuration summary covering"
      },
      {
       "kind": "selectField",
       "label": "Features",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 11 §Show configuration summary covering"
      },
      {
       "kind": "selectField",
       "label": "Lifecycle",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 11 §Show configuration summary covering"
      },
      {
       "kind": "selectField",
       "label": "Credentials",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 11 §Show configuration summary covering"
      },
      {
       "kind": "selectField",
       "label": "Financial configuration",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 11 §Show configuration summary covering"
      },
      {
       "kind": "selectField",
       "label": "Security profile",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 11 §Show configuration summary covering"
      },
      {
       "kind": "selectField",
       "label": "Applicable venues",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 11 §Show configuration summary covering"
      },
      {
       "kind": "selectField",
       "label": "Applicable channels",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 11 §Show configuration summary covering"
      },
      {
       "kind": "selectField",
       "label": "Effective date",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 11 §Show configuration summary covering"
      },
      {
       "kind": "selectField",
       "label": "User",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 11 §Every configuration publication records"
      },
      {
       "kind": "selectField",
       "label": "Date/time",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 11 §Every configuration publication records"
      },
      {
       "kind": "selectField",
       "label": "Old value",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 11 §Every configuration publication records"
      },
      {
       "kind": "selectField",
       "label": "New value",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 11 §Every configuration publication records"
      },
      {
       "kind": "selectField",
       "label": "Reason",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 11 §Every configuration publication records"
      },
      {
       "kind": "selectField",
       "label": "Approval",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 11 §Every configuration publication records"
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
   "loading": "The wallet preview validation configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the wallet preview validation untouched.",
   "emptyFirstRun": "No wallet preview validation configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "publishWalletConfiguration",
    "contract": "wallet",
    "purpose": "Validate and publish",
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
   "board": "wireframes/P08 Venue Management.dc.html#bo-1092",
   "workshopBoard": "wireframes/WS186 Wallet Configuration Backend Structure v1.0 Board 1.dc.html#bo-1092"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 11. 0 of 0 labels bound to a contract property; 18 of 55 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "createWalletType": {
  "method": "POST",
  "path": "/wallet-types",
  "contract": "wallet",
  "summary": "Define a kind of wallet",
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
  "requestBody": "WalletType",
  "responds": "WalletType"
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
 "listSharedWallets": {
  "method": "GET",
  "path": "/shared-wallets",
  "contract": "wallet",
  "summary": "Family, household and corporate structures",
  "permission": "WALLET_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "kind",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "SharedWallet"
 },
 "listWalletTypes": {
  "method": "GET",
  "path": "/wallet-types",
  "contract": "wallet",
  "summary": "The kinds of wallet that may exist — who owns one",
  "permission": "WALLET_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "WalletType"
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
 "setSharedWalletMembers": {
  "method": "PUT",
  "path": "/shared-wallets/{sharedWalletId}/members",
  "contract": "wallet",
  "summary": "Allowances, budgets and what each member may spend on",
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
  "responds": "SharedWalletMember"
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
 },
 "updateWalletType": {
  "method": "PUT",
  "path": "/wallet-types/{walletTypeId}",
  "contract": "wallet",
  "summary": "Change a kind of wallet",
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
  "requestBody": "WalletType",
  "responds": "WalletType"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
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
 "SharedWallet": {
  "type": "object",
  "x-ticvai-persistence": "wallet.shared_wallet",
  "description": "Board 4. **One pot, distributed authority.**",
  "required": [
   "kind",
   "walletId"
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
     "family",
     "household",
     "corporate",
     "school",
     "group"
    ]
   },
   "ownerPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "organisationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "members": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/SharedWalletMember"
    }
   },
   "totalBudget": {
    "x-ticvai-column": "budget_amount",
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "approvalAboveAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "SharedWalletMember": {
  "type": "object",
  "x-ticvai-persistence": "wallet.shared_wallet_member",
  "description": "Boards 4.5 and 4.6. **An allowance is a cap with a refresh, not a transfer.**",
  "required": [
   "subjectId"
  ],
  "properties": {
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "role": {
    "type": "string",
    "enum": [
     "owner",
     "administrator",
     "spender",
     "viewer"
    ]
   },
   "allowanceAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "allowanceCadence": {
    "type": "string",
    "enum": [
     "daily",
     "weekly",
     "monthly",
     "none"
    ],
    "default": "none"
   },
   "spendCapPerTransaction": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "allowedCategoryIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "blockedCategoryIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "allowedVenueIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "activeFrom": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "activeTo": {
    "type": "string",
    "format": "date",
    "nullable": true
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
 "WalletType": {
  "type": "object",
  "x-ticvai-persistence": "wallet.wallet_type",
  "description": "Board 1.2. **Who owns a wallet** — the first of the two vocabularies.",
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
   "ownerKind": {
    "type": "string",
    "enum": [
     "guest",
     "registeredCustomer",
     "family",
     "parent",
     "child",
     "corporate",
     "school",
     "employee"
    ]
   },
   "storedValueCapability": {
    "type": "boolean",
    "default": true,
    "description": "Board 1.2. Whether this wallet holds a balance at all. A pure entitlement wallet — passes and vouchers, no money — does not.\n"
   },
   "topUpCapability": {
    "type": "boolean",
    "default": false
   },
   "transferCapability": {
    "type": "boolean",
    "default": false
   },
   "refundCapability": {
    "type": "boolean",
    "default": false
   },
   "giftCardSupport": {
    "type": "boolean",
    "default": false
   },
   "voucherSupport": {
    "type": "boolean",
    "default": false
   },
   "membershipCreditSupport": {
    "type": "boolean",
    "default": false
   },
   "wearableSupport": {
    "type": "boolean",
    "default": false
   },
   "usageChannels": {
    "type": "array",
    "description": "**Where this wallet may be used, declared on the type itself.** Board 1.2 configures online, POS, mobile-app and API usage per wallet type, and this is what lets one `topUpWallet` serve every caller: the operation is shared and the type says which channel may reach it. `WalletChannelRules` still governs the per-credential detail — PIN thresholds, offline floor limits — and this governs whether the channel is open at all.\n",
    "items": {
     "type": "string",
     "enum": [
      "online",
      "pos",
      "mobileApp",
      "api",
      "kiosk",
      "reader"
     ]
    }
   },
   "presetName": {
    "type": "string",
    "description": "**The client's own name for this composition** — \"Resort Wallet\", \"Cashless Venue Wallet\", \"Closed-Loop Wallet\". Board 1.2 lists thirteen such names as examples, not as kinds: they are combinations of `ownerKind`, `allowedCreditTypeIds` and `scopePath`. Naming the preset keeps the client's vocabulary without hard-coding it into an enum.\n"
   },
   "holderMayDifferFromOwner": {
    "type": "boolean",
    "default": false,
    "description": "**A child wallet's owner is the parent.** Without this the model has to pretend a seven-year-old holds an account.\n"
   },
   "requiresIdentification": {
    "type": "boolean",
    "default": false
   },
   "maximumBalance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "allowedCreditTypeIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "allowNegativeBalance": {
    "type": "boolean",
    "default": false
   },
   "sharedStructureAllowed": {
    "type": "boolean",
    "default": false
   },
   "lifecycleStates": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "numberingPattern": {
    "type": "string",
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
 }
}
```
