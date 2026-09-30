# WS193 — Wallet Configuration Backend Structure v1.0 board 8

**10 screens · 16 operations · 15 schemas · 6 permissions**

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
  `AUDIT_VIEW, RISK_INVESTIGATE, RISK_REVIEW, WALLET_CONFIGURE, WALLET_OPERATE, WALLET_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-1153` | Wallet Security & Risk Command Center | listDetail | 1 | 0 | — |
| `BO-1154` | Wallet Risk Policy Configuration | configEditor | 1 | 0 | — |
| `BO-1155` | Transaction Risk Scoring Engine | listDetail | 1 | 0 | — |
| `BO-1156` | Velocity & Behavioral Rule Configuration | configEditor | 1 | 0 | — |
| `BO-1157` | Device, Credential & Account Security | listDetail | 2 | 0 | — |
| `BO-1158` | AI Fraud & Anomaly Detection Studio | listDetail | 1 | 0 | — |
| `BO-1159` | Automated Security Action Orchestration | configEditor | 2 | 0 | — |
| `BO-1160` | Fraud Alert & Investigation Case Management | listDetail | 6 | 0 | — |
| `BO-1161` | Security Rules Testing, Simulation & AI Sandbox | listDetail | 1 | 0 | — |
| `BO-1162` | Security Governance, Audit & Rule Publication | listDetail | 6 | 1 | — |

## Thin screens in this batch

**BO-1155, BO-1160, BO-1161 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-1153",
  "name": "Wallet Security & Risk Command Center",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "8",
   "number": "01",
   "page": 89
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/wallet-security-risk-command-center-bo-1153",
   "component": "apps/venue-management-web/src/routes/orders-money/WalletSecurityRiskCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-1154",
    "BO-1155",
    "BO-1156",
    "BO-1157",
    "BO-1158",
    "BO-1159",
    "BO-1160",
    "BO-1161",
    "BO-1162"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 8 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "BO-1154",
     "trigger": "Wallet Risk Policy Configuration",
     "provenance": "structural — pack board 8 wiring, 19 September 2026"
    },
    {
     "to": "BO-1155",
     "trigger": "Transaction Risk Scoring Engine",
     "provenance": "structural — pack board 8 wiring, 19 September 2026"
    },
    {
     "to": "BO-1156",
     "trigger": "Velocity & Behavioral Rule Configuration",
     "provenance": "structural — pack board 8 wiring, 19 September 2026"
    },
    {
     "to": "BO-1157",
     "trigger": "Device, Credential & Account Security",
     "provenance": "structural — pack board 8 wiring, 19 September 2026"
    },
    {
     "to": "BO-1158",
     "trigger": "AI Fraud & Anomaly Detection Studio",
     "provenance": "structural — pack board 8 wiring, 19 September 2026"
    },
    {
     "to": "BO-1159",
     "trigger": "Automated Security Action Orchestration",
     "provenance": "structural — pack board 8 wiring, 19 September 2026"
    },
    {
     "to": "BO-1160",
     "trigger": "Fraud Alert & Investigation Case Management",
     "provenance": "structural — pack board 8 wiring, 19 September 2026"
    },
    {
     "to": "BO-1161",
     "trigger": "Security Rules Testing, Simulation & AI Sandbox",
     "provenance": "structural — pack board 8 wiring, 19 September 2026"
    },
    {
     "to": "BO-1162",
     "trigger": "Security Governance, Audit & Rule Publication",
     "provenance": "structural — pack board 8 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide Security, Risk, Finance and authorized Operations teams with a real-time overview of wallet security. Dashboard KPIs",
  "purposeNote": "Authorized users can monitor wallet security across tenants and trace each alert to its wallet, customer, credential, transaction and risk decision.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 89 §Display"
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
       "label": "Search wallet security risk",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 89 §Filters"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Tenant",
        "Venue",
        "Wallet type",
        "Customer",
        "Risk level",
        "Channel",
        "Device",
        "Credential",
        "Transaction type",
        "Date/time"
       ],
       "notes": "The pack filters this screen by tenant, venue, wallet type, customer, risk level, channel and 4 more — which are present is a decision the pack already made.",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 89 §Filters"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every wallet security risk",
       "columns": [
        "Transactions Screened",
        "Transactions Approved",
        "Transactions Challenged",
        "Transactions Declined",
        "Transactions Held",
        "High-Risk Transactions",
        "Wallets Under Review",
        "Blocked Wallets",
        "Suspicious Transfers",
        "Suspicious Top-Ups",
        "Account-Takeover Alerts",
        "Credential Security Alerts",
        "Open Fraud Cases",
        "Prevented Value",
        "Risk Distribution"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 89 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected wallet security risk",
       "bindsTo": null,
       "columns": [
        "Transactions Screened",
        "Transactions Approved",
        "Transactions Challenged",
        "Transactions Declined",
        "Transactions Held",
        "High-Risk Transactions",
        "Wallets Under Review",
        "Blocked Wallets",
        "Suspicious Transfers",
        "Suspicious Top-Ups",
        "Account-Takeover Alerts",
        "Credential Security Alerts",
        "Open Fraud Cases",
        "Prevented Value",
        "Risk Distribution"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Display transactions as”, “Break down”.",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 89 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The wallet security risk list.",
   "error": "Could not load. Names which read failed and leaves the wallet security risk untouched.",
   "emptyFirstRun": "No wallet security risk yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the wallet security risk are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setWalletRiskRules",
    "contract": "wallet",
    "purpose": "Rules in force",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Transactions Screened",
    "Transactions Approved",
    "Transactions Challenged",
    "Transactions Declined",
    "Transactions Held",
    "High-Risk Transactions"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1153",
   "workshopBoard": "wireframes/WS193 Wallet Configuration Backend Structure v1.0 Board 8.dc.html#bo-1153"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 89. 0 of 25 labels bound to a contract property; 25 of 46 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1154",
  "name": "Wallet Risk Policy Configuration",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "8",
   "number": "02",
   "page": 90
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/wallet-risk-policy-configuration-bo-1154",
   "component": "apps/venue-management-web/src/routes/orders-money/WalletRiskPolicyConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1153"
   ],
   "exitTo": [
    "BO-1153"
   ],
   "transitions": [
    {
     "to": "BO-1153",
     "trigger": "Back to Wallet Security & Risk Command Center",
     "provenance": "structural — pack board 8 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure policies for) and no display directory — it is settings, not a population",
  "purpose": "Create reusable risk policies controlling wallet activities. Risk Policy Types",
  "purposeNote": "Security teams can create and publish wallet risk policies without modifying application code.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Wallet Funding",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 90 §Configure policies for"
      },
      {
       "kind": "selectField",
       "label": "Wallet Spending",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 90 §Configure policies for"
      },
      {
       "kind": "selectField",
       "label": "P2P Transfers",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 90 §Configure policies for"
      },
      {
       "kind": "selectField",
       "label": "Refunds",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 90 §Configure policies for"
      },
      {
       "kind": "selectField",
       "label": "Gift Cards",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 90 §Configure policies for"
      },
      {
       "kind": "selectField",
       "label": "Vouchers",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 90 §Configure policies for"
      },
      {
       "kind": "selectField",
       "label": "Wearables",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 90 §Configure policies for"
      },
      {
       "kind": "selectField",
       "label": "Offline Transactions",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 90 §Configure policies for"
      },
      {
       "kind": "selectField",
       "label": "Administrative Adjustments",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 90 §Configure policies for"
      },
      {
       "kind": "selectField",
       "label": "API Transactions",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 90 §Configure policies for"
      },
      {
       "kind": "selectField",
       "label": "Risk Conditions",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 90 §Configure policies for"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The wallet risk policy configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the wallet risk policy untouched.",
   "emptyFirstRun": "No wallet risk policy configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setWalletRiskRules",
    "contract": "wallet",
    "purpose": "Risk policy",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1154",
   "workshopBoard": "wireframes/WS193 Wallet Configuration Backend Structure v1.0 Board 8.dc.html#bo-1154"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 90. 0 of 0 labels bound to a contract property; 11 of 42 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1155",
  "name": "Transaction Risk Scoring Engine",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "8",
   "number": "03",
   "page": 91
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/transaction-risk-scoring-engine-bo-1155",
   "component": "apps/venue-management-web/src/routes/orders-money/TransactionRiskScoringEngine.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1153"
   ],
   "exitTo": [
    "BO-1153"
   ],
   "transitions": [
    {
     "to": "BO-1153",
     "trigger": "Back to Wallet Security & Risk Command Center",
     "provenance": "structural — pack board 8 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Calculate a real-time risk score for sensitive wallet operations. Example Risk Score",
  "purposeNote": "Each configured wallet operation receives a reproducible risk score with traceable contributing factors and an associated decision.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 91"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 91"
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
       "impliedBy": "setWalletRiskRules",
       "label": "Save wallet risk rules",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setWalletRiskRules"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The transaction risk scoring list.",
   "error": "Could not load. Names which read failed and leaves the transaction risk scoring untouched.",
   "emptyFirstRun": "No transaction risk scoring yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the transaction risk scoring are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setWalletRiskRules",
    "contract": "wallet",
    "purpose": "Transaction scoring",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1155",
   "workshopBoard": "wireframes/WS193 Wallet Configuration Backend Structure v1.0 Board 8.dc.html#bo-1155"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 91. 0 of 0 labels bound to a contract property; 0 of 36 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1156",
  "name": "Velocity & Behavioral Rule Configuration",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "8",
   "number": "04",
   "page": 92
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/velocity-behavioral-rule-configuration-bo-1156",
   "component": "apps/venue-management-web/src/routes/orders-money/VelocityBehavioralRuleConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1153"
   ],
   "exitTo": [
    "BO-1153"
   ],
   "transitions": [
    {
     "to": "BO-1153",
     "trigger": "Back to Wallet Security & Risk Command Center",
     "provenance": "structural — pack board 8 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Detect abnormal activity based on frequency, amount and behavioral patterns. Requirement 4.3.31 requires controls for suspicious transactions, spending restrictions, transfer restrictions and high-risk activity. Velocity Rules",
  "purposeNote": "applicable operations.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Transactions per minute",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 92 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Transactions per hour",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 92 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Transactions per day",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 92 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Value per hour",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 92 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Value per day",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 92 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Top-ups per hour",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 92 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Transfers per hour",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 92 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Refunds per day",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 92 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Failed attempts",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 92 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Different devices used",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 92 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Different credentials used",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 92 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Number of recipients",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 92 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Number of venues",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 92 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Example",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 92 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Hold additional transfers + Risk Review",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 92 §Action"
      },
      {
       "kind": "secondaryButton",
       "label": "High-Risk Alert",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 92 §Action"
      },
      {
       "kind": "secondaryButton",
       "label": "Behavioral Baseline",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 92 §Action"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The velocity behavioral rule configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the velocity behavioral rule untouched.",
   "emptyFirstRun": "No velocity behavioral rule configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setWalletRiskRules",
    "contract": "wallet",
    "purpose": "Velocity and behaviour",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1156",
   "workshopBoard": "wireframes/WS193 Wallet Configuration Backend Structure v1.0 Board 8.dc.html#bo-1156"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 92. 0 of 0 labels bound to a contract property; 17 of 29 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Hold additional transfers + Risk Review, High-Risk Alert, Behavioral Baseline are choices sent by `setWalletRiskRules` (action holdTransaction/raiseCase, alertOnAction, signal baseline).",
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
  "id": "BO-1157",
  "name": "Device, Credential & Account Security",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "8",
   "number": "05",
   "page": 93
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/device-credential-account-security-bo-1157",
   "component": "apps/venue-management-web/src/routes/orders-money/DeviceCredentialAccountSecurity.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1153"
   ],
   "exitTo": [
    "BO-1153"
   ],
   "transitions": [
    {
     "to": "BO-1153",
     "trigger": "Back to Wallet Security & Risk Command Center",
     "provenance": "structural — pack board 8 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Track; Detect) and no metric row",
  "purpose": "Detect compromised accounts, shared credentials and suspicious device behavior. Requirement 4.3.32 specifically includes detection of account sharing and unauthorized access patterns. Device Intelligence",
  "purposeNote": "customer's underlying balance.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 93 §Track"
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
       "label": "Every device credential account",
       "columns": [
        "Device ID",
        "First seen",
        "Last seen",
        "Customer association",
        "Wallet associations",
        "Trusted/untrusted status",
        "Failed authentications",
        "Credential changes",
        "Risk history",
        "Credential Monitoring",
        "Same credential used simultaneously",
        "Same wallet on excessive devices",
        "Lost/stolen credential use",
        "New device + high-value transaction",
        "Rapid device switching",
        "Repeated PIN failures",
        "Repeated OTP failures",
        "Suspicious account recovery",
        "Credential cloning indicators",
        "Administrative Actions",
        "Trust Device",
        "Untrust Device",
        "Revoke Session",
        "Suspend Credential",
        "Force Reauthentication",
        "Reset Credential",
        "Block Wallet"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 93 §Track"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected device credential account",
       "bindsTo": null,
       "columns": [
        "Device ID",
        "First seen",
        "Last seen",
        "Customer association",
        "Wallet associations",
        "Trusted/untrusted status",
        "Failed authentications",
        "Credential changes",
        "Risk history",
        "Credential Monitoring",
        "Same credential used simultaneously",
        "Same wallet on excessive devices",
        "Lost/stolen credential use",
        "New device + high-value transaction",
        "Rapid device switching",
        "Repeated PIN failures",
        "Repeated OTP failures",
        "Suspicious account recovery",
        "Credential cloning indicators",
        "Administrative Actions",
        "Trust Device",
        "Untrust Device",
        "Revoke Session",
        "Suspend Credential",
        "Force Reauthentication",
        "Reset Credential",
        "Block Wallet"
       ],
       "notes": null,
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 93 §Track"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Digital Key",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 93 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Customer Login",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 93 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "API Credential",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 93 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Security Rules",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 93 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The device credential account list.",
   "error": "Could not load. Names which read failed and leaves the device credential account untouched.",
   "emptyFirstRun": "No device credential account yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the device credential account are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "linkWalletCredential",
    "contract": "wallet",
    "purpose": "Credential and device security",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getWallet"
    ]
   },
   {
    "operationId": "listWalletDisputes",
    "contract": "wallet",
    "purpose": "Where it went wrong",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Device ID",
    "First seen",
    "Last seen",
    "Customer association",
    "Wallet associations",
    "Trusted/untrusted status"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1157",
   "workshopBoard": "wireframes/WS193 Wallet Configuration Backend Structure v1.0 Board 8.dc.html#bo-1157"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 93. 0 of 27 labels bound to a contract property; 31 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Digital Key are choices sent by `linkWalletCredential` (kind digitalKey); Customer Login, API Credential dropped (login and API-key security live on identity and public-api screens, not a wallet action); Security Rules dropped (navigation to the velocity/behaviour rules screen).",
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
  "id": "BO-1158",
  "name": "AI Fraud & Anomaly Detection Studio",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "8",
   "number": "06",
   "page": 94
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/ai-fraud-anomaly-detection-studio-bo-1158",
   "component": "apps/venue-management-web/src/routes/orders-money/AiFraudAnomalyDetectionStudio.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1153"
   ],
   "exitTo": [
    "BO-1153"
   ],
   "transitions": [
    {
     "to": "BO-1153",
     "trigger": "Back to Wallet Security & Risk Command Center",
     "provenance": "structural — pack board 8 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Every AI alert should show) and no metric row",
  "purpose": "Configure AI-driven detection of suspicious wallet behavior that fixed rules may not identify. Requirement 4.3.32 explicitly requires AI monitoring for unusual top-ups, abnormal spending, account sharing, rapid transfers, duplicate transactions and unauthorized access. AI Detection Categories",
  "purposeNote": "AI-generated alerts contain understandable contributing factors and are governed by configurable thresholds and human-review policies.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 94 §Every AI alert should show"
   },
   {
    "operation": null,
    "why": "**AI Fraud & Anomaly Detection Studio declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
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
       "label": "Every fraud anomaly detection",
       "columns": [
        "Why was this flagged?"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 94 §Every AI alert should show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected fraud anomaly detection",
       "bindsTo": null,
       "columns": [
        "Why was this flagged?"
       ],
       "notes": null,
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 94 §Every AI alert should show"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Duplicate Transactions",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 94 §Enable/disable"
      },
      {
       "kind": "secondaryButton",
       "label": "Unauthorized Access",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 94 §Enable/disable"
      },
      {
       "kind": "secondaryButton",
       "label": "Refund Abuse",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 94 §Enable/disable"
      },
      {
       "kind": "secondaryButton",
       "label": "Gift Card Abuse",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 94 §Enable/disable"
      },
      {
       "kind": "secondaryButton",
       "label": "Voucher Abuse",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 94 §Enable/disable"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The fraud anomaly detection list.",
   "error": "Could not load. Names which read failed and leaves the fraud anomaly detection untouched.",
   "emptyFirstRun": "No fraud anomaly detection yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the fraud anomaly detection are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setWalletRiskRules",
    "contract": "wallet",
    "purpose": "Anomaly detection rules",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Why was this flagged?"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1158",
   "workshopBoard": "wireframes/WS193 Wallet Configuration Backend Structure v1.0 Board 8.dc.html#bo-1158"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 94. 0 of 1 labels bound to a contract property; 18 of 37 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Duplicate Transactions, Unauthorized Access, Refund Abuse, Gift Card Abuse, Voucher Abuse dropped (AI design pending review).",
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
  "id": "BO-1159",
  "name": "Automated Security Action Orchestration",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "8",
   "number": "07",
   "page": 95
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/automated-security-action-orchestration-bo-1159",
   "component": "apps/venue-management-web/src/routes/orders-money/AutomatedSecurityActionOrchestration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1153"
   ],
   "exitTo": [
    "BO-1153"
   ],
   "transitions": [
    {
     "to": "BO-1153",
     "trigger": "Back to Wallet Security & Risk Command Center",
     "provenance": "structural — pack board 8 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Determine what TICVAI automatically does when a security or fraud condition occurs. Available Actions Low Risk → Approve Medium Risk → Approve + Monitor Elevated Risk → Step-Up Authentication High Risk → Hold Transaction Very High Risk → Restrict Function Critical → Block Wallet + Create Case Granular Restrictions Instead of always blocking the whole wallet, TICVAI can: Block P2P transfers Disable top-ups Disable online payments Disable wearable payments Disable specific credential Freeze specific credit type Require MFA Set temporary spending limit Allow balance inquiry only",
  "purposeNote": "Configured risk events trigger deterministic and auditable protective actions appropriate to their severity.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Trigger",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 95 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Risk score",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 95 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Action",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 95 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Duration",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 95 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Customer notification",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 95 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Security notification",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 95 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Case creation",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 95 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Approval for release",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 95 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Automatic expiry",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 95 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Escalation",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 95 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Example",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 95 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Suspected credential compromise",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 95 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The automated security action configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the automated security action untouched.",
   "emptyFirstRun": "No automated security action configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setWalletRiskRules",
    "contract": "wallet",
    "purpose": "What an automated action does",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "setWalletRestriction",
    "contract": "wallet",
    "purpose": "Freeze on a hit",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getWallet"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1159",
   "workshopBoard": "wireframes/WS193 Wallet Configuration Backend Structure v1.0 Board 8.dc.html#bo-1159"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 95. 0 of 0 labels bound to a contract property; 12 of 44 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1160",
  "name": "Fraud Alert & Investigation Case Management",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "8",
   "number": "08",
   "page": 96
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/fraud-alert-investigation-case-management-bo-1160",
   "component": "apps/venue-management-web/src/routes/orders-money/FraudAlertInvestigationCaseManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1153"
   ],
   "exitTo": [
    "BO-1153"
   ],
   "transitions": [
    {
     "to": "BO-1153",
     "trigger": "Back to Wallet Security & Risk Command Center",
     "provenance": "structural — pack board 8 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display; Show) and no metric row",
  "purpose": "Provide security teams with a structured investigation workspace. Alert Queue",
  "purposeNote": "Every security alert can be investigated through a controlled case workflow with complete decision history.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 96 §Display"
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
       "label": "Every fraud alert investigation",
       "columns": [
        "Alert ID",
        "Wallet",
        "Customer",
        "Transaction",
        "Amount",
        "Risk score",
        "AI score",
        "Triggered rules",
        "Device",
        "Credential",
        "Venue",
        "Date/time",
        "Priority",
        "Status",
        "Case Workflow",
        "New",
        "→ Triage",
        "→ Under Investigation",
        "→ Customer Verification",
        "→ Escalated",
        "→ Confirmed Fraud / False Positive",
        "→ Resolved",
        "→ Closed",
        "Investigator Workspace",
        "Wallet timeline",
        "Transaction history",
        "Funding history",
        "Transfer network",
        "Devices",
        "Credentials",
        "Authentication history",
        "Refund history",
        "Related alerts",
        "Previous cases",
        "Investigator Actions",
        "Mark Safe",
        "Hold Transaction",
        "Block Transfer",
        "Suspend Credential",
        "Freeze Wallet",
        "Request Verification",
        "Reverse where permitted",
        "Escalate",
        "Close as False Positive",
        "Confirm Fraud"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 96 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected fraud alert investigation",
       "bindsTo": null,
       "columns": [
        "Alert ID",
        "Wallet",
        "Customer",
        "Transaction",
        "Amount",
        "Risk score",
        "AI score",
        "Triggered rules",
        "Device",
        "Credential",
        "Venue",
        "Date/time",
        "Priority",
        "Status",
        "Case Workflow",
        "New",
        "→ Triage",
        "→ Under Investigation",
        "→ Customer Verification",
        "→ Escalated",
        "→ Confirmed Fraud / False Positive",
        "→ Resolved",
        "→ Closed",
        "Investigator Workspace",
        "Wallet timeline",
        "Transaction history",
        "Funding history",
        "Transfer network",
        "Devices",
        "Credentials",
        "Authentication history",
        "Refund history",
        "Related alerts",
        "Previous cases",
        "Investigator Actions",
        "Mark Safe",
        "Hold Transaction",
        "Block Transfer",
        "Suspend Credential",
        "Freeze Wallet",
        "Request Verification",
        "Reverse where permitted",
        "Escalate",
        "Close as False Positive",
        "Confirm Fraud"
       ],
       "notes": null,
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 96 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The fraud alert investigation list.",
   "error": "Could not load. Names which read failed and leaves the fraud alert investigation untouched.",
   "emptyFirstRun": "No fraud alert investigation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the fraud alert investigation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listWalletDisputes",
    "contract": "wallet",
    "purpose": "Fraud cases",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listRiskAlerts",
    "contract": "ai",
    "purpose": "Risk alerts",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "decideRiskAlert",
    "contract": "ai",
    "purpose": "Dismiss, monitor, mark false positive, or escalate",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "createRiskCase",
    "contract": "ai",
    "purpose": "Open an investigation",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "getRiskCase",
    "contract": "ai",
    "purpose": "A case with its evidence and actions",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "closeRiskCase",
    "contract": "ai",
    "purpose": "Close a case with an outcome",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Alert ID",
    "Wallet",
    "Customer",
    "Transaction",
    "Amount",
    "Risk score"
   ],
   "params": [
    {
     "name": "alertId",
     "from": "navigation"
    },
    {
     "name": "caseId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1160",
   "workshopBoard": "wireframes/WS193 Wallet Configuration Backend Structure v1.0 Board 8.dc.html#bo-1160"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 96. 0 of 45 labels bound to a contract property; 45 of 49 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1161",
  "name": "Security Rules Testing, Simulation & AI Sandbox",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "8",
   "number": "09",
   "page": 97
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/security-rules-testing-simulation-ai-sandbox-bo-1161",
   "component": "apps/venue-management-web/src/routes/orders-money/SecurityRulesTestingSimulationAiSandbox.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1153"
   ],
   "exitTo": [
    "BO-1153"
   ],
   "transitions": [
    {
     "to": "BO-1153",
     "trigger": "Back to Wallet Security & Risk Command Center",
     "provenance": "structural — pack board 8 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display; Show) and no metric row",
  "purpose": "Test new fraud rules and AI configurations before applying them to live transactions. This screen is particularly important because overly aggressive security rules can create large numbers of false declines. Simulation Modes Single Transaction Test",
  "purposeNote": "New security policies can be tested against simulated or appropriately controlled historical scenarios before production publication.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 97 §Display"
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
       "label": "Every security rules testing",
       "columns": [
        "Transactions Evaluated → 1,245,000",
        "Would Approve → 98.4%",
        "Would Challenge → 1.1%",
        "Would Hold → 0.4%",
        "Would Decline → 0.1%",
        "Impact Analysis",
        "Potential fraud detected",
        "Potential false positives",
        "Customer impact",
        "Financial exposure",
        "Channels affected",
        "Wallet types affected"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 97 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected security rules testing",
       "bindsTo": null,
       "columns": [
        "Transactions Evaluated → 1,245,000",
        "Would Approve → 98.4%",
        "Would Challenge → 1.1%",
        "Would Hold → 0.4%",
        "Would Decline → 0.1%",
        "Impact Analysis",
        "Potential fraud detected",
        "Potential false positives",
        "Customer impact",
        "Financial exposure",
        "Channels affected",
        "Wallet types affected"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Enter”.",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 97 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The security rules testing list.",
   "error": "Could not load. Names which read failed and leaves the security rules testing untouched.",
   "emptyFirstRun": "No security rules testing yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the security rules testing are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "simulateCreditConsumption",
    "contract": "wallet",
    "purpose": "Test against a scenario",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Transactions Evaluated → 1,245,000",
    "Would Approve → 98.4%",
    "Would Challenge → 1.1%",
    "Would Hold → 0.4%",
    "Would Decline → 0.1%",
    "Impact Analysis"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1161",
   "workshopBoard": "wireframes/WS193 Wallet Configuration Backend Structure v1.0 Board 8.dc.html#bo-1161"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 97. 0 of 12 labels bound to a contract property; 12 of 33 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1162",
  "name": "Security Governance, Audit & Rule Publication",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "8",
   "number": "10",
   "page": 98
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/security-governance-audit-rule-publication-bo-1162",
   "component": "apps/venue-management-web/src/routes/orders-money/SecurityGovernanceAuditRulePublication.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1153"
   ],
   "exitTo": [
    "BO-1153"
   ],
   "transitions": [
    {
     "to": "BO-1153",
     "trigger": "Back to Wallet Security & Risk Command Center",
     "provenance": "structural — pack board 8 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Govern how wallet security policies, fraud models and automated actions are changed and released. Configuration Areas Configure the financial-control layer of TICVAI Wallet, providing complete visibility and governance over wallet liabilities, stored-value balances, gift-card exposure, reconciliation, breakage, revenue-recognition events, accounting mappings, financial exceptions and management analytics. This board directly addresses requirements 4.3.17, 4.3.33, 4.3.36 and 4.3.37, as well as the reconciliation requirement described under 4.3.4. The architectural boundary should remain clear: Wallet Module = sub-ledger and source of wallet financial events. Finance Module = accounting/GL, financial posting and corporate financial reporting. Board 9 therefore controls the wallet-side financial configuration and sends governed accounting events to the TICVAI Finance module.",
  "purposeNote": "No material wallet-security configuration can enter production without appropriate validation, permissions, versioning and approval, and all changes remain permanently auditable. Board 8 — Real-Time Risk Decision Flow We would specify the backend sequence clearly: Wallet Transaction Request → Identity / Credential Validation → Static Security Rules → Velocity Check → Device & Credential Risk → Customer Behavioural Profile → AI Anomaly Detection → Combined Risk Score → Decision Engine",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 98 §Display"
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
       "label": "Every security governance audit",
       "columns": [
        "Risk policies",
        "Rule versions",
        "AI configuration version",
        "Thresholds",
        "Automated actions",
        "Effective dates",
        "Applicable tenants",
        "Applicable venues",
        "Owner",
        "Approval status",
        "Change Governance"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 98 §Display"
      },
      {
       "kind": "publishGate",
       "label": "What publishing changes",
       "notes": "**Takes effect at every till and reader immediately.** Credit types, consumption order and funding rules change for balances that already exist, not only for new ones.",
       "provenance": "authored — required by check-screens, 19 September 2026"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected security governance audit",
       "bindsTo": null,
       "columns": [
        "Risk policies",
        "Rule versions",
        "AI configuration version",
        "Thresholds",
        "Automated actions",
        "Effective dates",
        "Applicable tenants",
        "Applicable venues",
        "Owner",
        "Approval status",
        "Change Governance"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Every change records”, “Maintain history for”, “Then”, “The module progression is now”.",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 98 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Version comparison",
       "operation": "diffWalletConfigurationVersion",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 98 §Support"
      },
      {
       "kind": "destructiveButton",
       "label": "Rollback",
       "operation": "restoreWalletConfigurationVersion",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 98 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Emergency disable",
       "operation": "setWalletRiskRuleStatus",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 98 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Rule suspension",
       "operation": "setWalletRiskRuleStatus",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 98 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Security Audit",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 98 §Support"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmRollback",
    "component": "confirmDialog",
    "trigger": "Rollback",
    "body": "**Rollback on a security governance audit is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 98 §Support"
   }
  ],
  "states": {
   "loading": "The security governance audit list.",
   "error": "Could not load. Names which read failed and leaves the security governance audit untouched.",
   "emptyFirstRun": "No security governance audit yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the security governance audit are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "publishWalletConfiguration",
    "contract": "wallet",
    "purpose": "Publish the rules",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listWalletTypes",
     "listCreditTypes"
    ]
   },
   {
    "operationId": "listAuditRecords",
    "contract": "tenancy",
    "purpose": "Show who changed wallet security configuration",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration): serves the pack action(s) Security Audit"
   },
   {
    "operationId": "listWalletConfigurationVersions",
    "contract": "wallet",
    "purpose": "Wallet configuration versions, newest first",
    "trigger": "onLoad"
   },
   {
    "operationId": "diffWalletConfigurationVersion",
    "contract": "wallet",
    "purpose": "Compare versions",
    "trigger": "onAction"
   },
   {
    "operationId": "restoreWalletConfigurationVersion",
    "contract": "wallet",
    "purpose": "Restore version",
    "trigger": "onAction"
   },
   {
    "operationId": "setWalletRiskRuleStatus",
    "contract": "wallet",
    "purpose": "Set rule status",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "ruleCode",
     "from": "navigation"
    },
    {
     "name": "version",
     "from": "navigation"
    }
   ],
   "preloaded": [
    "Risk policies",
    "Rule versions",
    "AI configuration version",
    "Thresholds",
    "Automated actions",
    "Effective dates"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1162",
   "workshopBoard": "wireframes/WS193 Wallet Configuration Backend Structure v1.0 Board 8.dc.html#bo-1162"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 98. 0 of 11 labels bound to a contract property; 16 of 95 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Security Audit: `listAuditRecords`; still owed by a contract change: `diffWalletConfigurationVersion`, `listWalletConfigurationVersions`, `restoreWalletConfigurationVersion`, `setWalletRiskRuleStatus`.",
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
 "closeRiskCase": {
  "method": "POST",
  "path": "/risk/cases/{caseId}/close",
  "contract": "ai",
  "summary": "Close a case with an outcome",
  "permission": "RISK_INVESTIGATE",
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
  "responds": "AiRiskCase"
 },
 "createRiskCase": {
  "method": "POST",
  "path": "/risk/cases",
  "contract": "ai",
  "summary": "Open an investigation",
  "permission": "RISK_INVESTIGATE",
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
  "responds": "AiRiskCase"
 },
 "decideRiskAlert": {
  "method": "POST",
  "path": "/risk/alerts/{alertId}/decide",
  "contract": "ai",
  "summary": "Dismiss, monitor, mark false positive, or escalate",
  "permission": "RISK_REVIEW",
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
  "responds": "AiRiskAlert"
 },
 "diffWalletConfigurationVersion": {
  "method": "GET",
  "path": "/wallet-configuration/versions/{version}/diff",
  "contract": "wallet",
  "summary": "Compare a wallet configuration version against another or the working draft",
  "permission": "WALLET_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "against",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "WalletConfigurationDiff"
 },
 "getRiskCase": {
  "method": "GET",
  "path": "/risk/cases/{caseId}",
  "contract": "ai",
  "summary": "A case with its evidence and actions",
  "permission": "RISK_INVESTIGATE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AiRiskCaseDetail"
 },
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
 "listAuditRecords": {
  "method": "GET",
  "path": "/audit-records",
  "contract": "tenancy",
  "summary": "Who did what, where, and when",
  "permission": "AUDIT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "orgUnitId",
    "in": "query",
    "required": null
   },
   {
    "name": "principalId",
    "in": "query",
    "required": null
   },
   {
    "name": "workstationId",
    "in": "query",
    "required": null
   },
   {
    "name": "action",
    "in": "query",
    "required": null
   },
   {
    "name": "subjectRef",
    "in": "query",
    "required": null
   },
   {
    "name": "platformStaffGrantId",
    "in": "query",
    "required": null
   },
   {
    "name": "from",
    "in": "query",
    "required": null
   },
   {
    "name": "to",
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
 "listRiskAlerts": {
  "method": "GET",
  "path": "/risk/alerts",
  "contract": "ai",
  "summary": "Risk alerts",
  "permission": "RISK_REVIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "band",
    "in": "query",
    "required": null
   },
   {
    "name": "kind",
    "in": "query",
    "required": null
   },
   {
    "name": "entityType",
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
 "listWalletConfigurationVersions": {
  "method": "GET",
  "path": "/wallet-configuration/versions",
  "contract": "wallet",
  "summary": "Wallet configuration versions, newest first",
  "permission": "WALLET_VIEW",
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
  "requestBody": null,
  "responds": "Page"
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
 "publishWalletConfiguration": {
  "method": "POST",
  "path": "/wallet-configuration/publish",
  "contract": "wallet",
  "summary": "Validate and publish the wallet configuration as a version",
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
  "requestBody": null,
  "responds": "WalletConfigurationVersion"
 },
 "restoreWalletConfigurationVersion": {
  "method": "POST",
  "path": "/wallet-configuration/versions/{version}/restore",
  "contract": "wallet",
  "summary": "Put a previous wallet configuration back as the working draft",
  "permission": "WALLET_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
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
 "setWalletRestriction": {
  "method": "POST",
  "path": "/wallet-restrictions",
  "contract": "wallet",
  "summary": "Block, freeze or restrict a wallet",
  "permission": "WALLET_OPERATE",
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
  "requestBody": "WalletRestriction",
  "responds": "WalletRestriction"
 },
 "setWalletRiskRuleStatus": {
  "method": "POST",
  "path": "/wallet-risk-rules/{ruleCode}/status",
  "contract": "wallet",
  "summary": "Suspend, emergency-disable or reactivate one risk rule",
  "permission": "WALLET_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "WalletRiskRules"
 },
 "setWalletRiskRules": {
  "method": "PUT",
  "path": "/wallet-risk-rules",
  "contract": "wallet",
  "summary": "Velocity, behaviour and what happens when a rule trips",
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
  "requestBody": "WalletRiskRules",
  "responds": "WalletRiskRules"
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
 "AiRiskAlert": {
  "type": "object",
  "x-ticvai-persistence": "ai.risk_alert",
  "description": "**A risk alert** (AIP-109): raised by scoring or re-scoring. **Alert, case and confirmed fraud are kept distinct** (AIP-163): an alert is a signal to look, not a finding.",
  "required": [
   "kind",
   "entityType",
   "entityRef",
   "band",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "kind": {
    "type": "string",
    "enum": [
     "transaction",
     "velocity",
     "entity",
     "network",
     "staffLeakage",
     "scanAbuse",
     "accountTakeover",
     "chargeback"
    ]
   },
   "entityType": {
    "type": "string",
    "enum": [
     "customer",
     "account",
     "device",
     "paymentToken",
     "credential",
     "cluster",
     "staff",
     "wallet",
     "ipAddress"
    ]
   },
   "entityRef": {
    "type": "string"
   },
   "score": {
    "type": "integer",
    "minimum": 0,
    "maximum": 100
   },
   "band": {
    "type": "string",
    "enum": [
     "low",
     "medium",
     "high",
     "critical"
    ],
    "description": "Design 5.6: a risk score and band, never a probability."
   },
   "reasonCodes": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "correlationKey": {
    "type": "string",
    "nullable": true
   },
   "assessmentId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "open",
     "monitoring",
     "dismissed",
     "falsePositive",
     "escalated"
    ],
    "readOnly": true
   },
   "caseId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-references": "ai.risk_case"
   },
   "raisedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "decidedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-references": "identity.principal"
   },
   "decidedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "decisionNote": {
    "type": "string",
    "nullable": true,
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."
   }
  }
 },
 "AiRiskCase": {
  "type": "object",
  "x-ticvai-persistence": "ai.risk_case",
  "description": "**An investigation** (AIP-150..160). Its evidence and actions are `ai.case_evidence` and `ai.case_action`. The summary is written by a model from structured evidence only (AIP-153); the outcome is a person's.",
  "required": [
   "reference",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "reference": {
    "type": "string",
    "readOnly": true
   },
   "title": {
    "type": "string"
   },
   "status": {
    "type": "string",
    "enum": [
     "open",
     "investigating",
     "pendingAction",
     "closed"
    ],
    "readOnly": true
   },
   "priority": {
    "type": "string",
    "enum": [
     "low",
     "medium",
     "high",
     "critical"
    ]
   },
   "entities": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "entityType": {
       "type": "string",
       "enum": [
        "customer",
        "account",
        "device",
        "paymentToken",
        "credential",
        "cluster",
        "staff"
       ]
      },
      "entityRef": {
       "type": "string"
      }
     }
    }
   },
   "alertIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "assigneePrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "x-ticvai-references": "identity.principal"
   },
   "summary": {
    "type": "string",
    "nullable": true,
    "readOnly": true
   },
   "outcome": {
    "type": "string",
    "enum": [
     "confirmedFraud",
     "notFraud",
     "inconclusive"
    ],
    "nullable": true,
    "readOnly": true
   },
   "closureNote": {
    "type": "string",
    "nullable": true,
    "readOnly": true
   },
   "openedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "x-ticvai-references": "identity.principal"
   },
   "openedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "closedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-references": "identity.principal"
   },
   "closedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."
   }
  }
 },
 "AiRiskCaseAction": {
  "type": "object",
  "x-ticvai-persistence": "ai.case_action",
  "description": "**A restrictive action proposed from a case** (AIP-136). It goes to the owning module through the action pipeline, never straight from review; at the first-release ceiling (L1 advisory, design 3.8) it is a recommendation the owning module's operator applies. **Scoped through its case.**",
  "required": [
   "caseId",
   "action",
   "targetContract"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "caseId": {
    "type": "string",
    "format": "uuid",
    "x-ticvai-references": "ai.risk_case"
   },
   "action": {
    "type": "string",
    "enum": [
     "blockPaymentToken",
     "suspendAccount",
     "restrictWallet",
     "revokeEntitlement",
     "flagCustomer",
     "requireStepUp",
     "holdRefunds",
     "lockIdentity"
    ]
   },
   "targetContract": {
    "type": "string"
   },
   "targetOperation": {
    "type": "string"
   },
   "targetRef": {
    "type": "string"
   },
   "rationale": {
    "type": "string"
   },
   "status": {
    "type": "string",
    "enum": [
     "recommended",
     "planned",
     "awaitingApproval",
     "applied",
     "rejected",
     "failed"
    ],
    "readOnly": true
   },
   "planId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-references": "ai.action_plan"
   },
   "proposedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "x-ticvai-references": "identity.principal"
   },
   "proposedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "AiRiskCaseDetail": {
  "type": "object",
  "x-ticvai-persistence": "none — ai.risk_case with its evidence, actions and alerts",
  "description": "A case with everything attached to it.",
  "required": [
   "case"
  ],
  "properties": {
   "case": {
    "$ref": "#/components/schemas/AiRiskCase"
   },
   "evidence": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/AiRiskCaseEvidence"
    }
   },
   "actions": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/AiRiskCaseAction"
    }
   },
   "alerts": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/AiRiskAlert"
    }
   }
  }
 },
 "AiRiskCaseEvidence": {
  "type": "object",
  "x-ticvai-persistence": "ai.case_evidence",
  "description": "**Case evidence** (AIP-155): `jsonb` plus an immutable Blob copy. **Scoped through its case** (`platform.apply_parent_rls`). Never edited; a correction is new evidence.",
  "required": [
   "caseId",
   "kind",
   "label"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "caseId": {
    "type": "string",
    "format": "uuid",
    "x-ticvai-references": "ai.risk_case"
   },
   "kind": {
    "type": "string",
    "enum": [
     "assessment",
     "alert",
     "transaction",
     "networkSnapshot",
     "note",
     "document"
    ]
   },
   "ref": {
    "type": "string",
    "nullable": true
   },
   "content": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true
   },
   "blobRef": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "The immutable (WORM) copy."
   },
   "label": {
    "type": "string",
    "enum": [
     "source",
     "derived",
     "modelInferred"
    ]
   },
   "contentHash": {
    "type": "string",
    "readOnly": true
   },
   "addedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "x-ticvai-references": "identity.principal"
   },
   "addedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "AuditRecord": {
  "x-ticvai-append-only": "occurredAt",
  "type": "object",
  "x-ticvai-persistence": "platform.audit_record",
  "description": "26 September, pull audit R198. **One row of the platform audit trail, as `listAuditRecords` returns it.** It was a free-form object, so nothing said what an audit row carries. These are the fields the operation already filters on — who, where, on which workstation, what action, on what, and when — and nothing more. Written by the operations that audit themselves; never edited and never deleted.\n",
  "required": [
   "id",
   "action",
   "occurredAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "principalId": {
    "type": "string",
    "format": "uuid",
    "description": "Who acted."
   },
   "orgUnitId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The scope node the action happened in."
   },
   "workstationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The workstation it was done from, where there was one."
   },
   "action": {
    "type": "string",
    "description": "What was done, as the writing operation names it."
   },
   "subjectRef": {
    "type": "string",
    "nullable": true,
    "description": "**The thing acted on** — a profile, a shift, an order. The same value the `subjectRef` filter matches.\n"
   },
   "occurredAt": {
    "type": "string",
    "format": "date-time",
    "description": "When. The list is ordered by this, most recent first."
   },
   "platformStaffGrantId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**Set when a TICVAI platform operator acted, naming the grant they acted under** (`identity.openPlatformStaffGrant`; decided 28 September, audit R098). Null for the tenant's own staff. Every platform action in a tenant carries one, so the tenant can see all of them.\n"
   }
  }
 },
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
 "WalletConfigurationDiff": {
  "x-ticvai-persistence": "none — computed from wallet.configuration_version_snapshot (a published version) against the area tables (the working draft)",
  "type": "object",
  "description": "Board 8, p.98. Field-level comparison of two wallet configuration versions, shaped as white-label `ConfigDiff`.",
  "required": [
   "fromVersion",
   "toVersion",
   "changes"
  ],
  "properties": {
   "fromVersion": {
    "type": "integer"
   },
   "toVersion": {
    "type": "integer",
    "nullable": true,
    "description": "Null when compared against the working draft."
   },
   "changes": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "area",
      "path",
      "changeKind"
     ],
     "properties": {
      "area": {
       "type": "string",
       "enum": [
        "walletTypes",
        "creditTypes",
        "consumptionPolicy",
        "fundingRules",
        "channelRules",
        "authenticationPolicy",
        "transferRules",
        "refundPolicy",
        "riskRules",
        "accountingMapping",
        "reconciliationSources",
        "integrationMappings"
       ]
      },
      "path": {
       "type": "string"
      },
      "changeKind": {
       "type": "string",
       "enum": [
        "added",
        "removed",
        "modified"
       ]
      },
      "before": {
       "type": "string",
       "nullable": true
      },
      "after": {
       "type": "string",
       "nullable": true
      }
     }
    }
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
 "WalletRiskRules": {
  "type": "object",
  "x-ticvai-persistence": "wallet.risk_rules",
  "description": "Boards 8.2 to 8.7. **A risk rule with no action is a report.**",
  "properties": {
   "rules": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "code": {
       "type": "string"
      },
      "signal": {
       "type": "string",
       "enum": [
        "velocityCount",
        "velocityAmount",
        "newCredential",
        "geographyJump",
        "deviceChange",
        "dormantThenLarge",
        "repeatedFailure",
        "refundPattern",
        "accountSharing",
        "duplicateTransaction",
        "aiRiskScore"
       ],
       "description": "4.3.32 (29 September, build pass). **`accountSharing`**: one wallet or credential used from more devices or places at once than one person can be (`threshold` concurrent devices within `windowMinutes`). **`duplicateTransaction`**: the same amount at the same acceptance point within `windowMinutes` (`threshold` repeats). **`aiRiskScore`**: the score the `ai` risk engine returns for the wallet operation (`scoreTransactionRisk`, rules first and statistical baselines as history builds, ai-system-design 3.10); `threshold` is the score at or above which the rule acts. The wallet keeps its own rules and actions; the AI finding and its case are the `ai` contract's (`listRiskAlerts`)."
      },
      "threshold": {
       "type": "number"
      },
      "windowMinutes": {
       "type": "integer"
      },
      "action": {
       "type": "string",
       "enum": [
        "scoreOnly",
        "challenge",
        "holdTransaction",
        "freezeWallet",
        "raiseCase"
       ]
      },
      "minimumConfidence": {
       "type": "number",
       "nullable": true,
       "description": "**Required before an automated freeze.** A rule that freezes on a false positive will eventually freeze a family in a queue.\n"
      },
      "alertOnAction": {
       "type": "boolean",
       "default": true
      },
      "status": {
       "type": "string",
       "readOnly": true,
       "enum": [
        "active",
        "suspended",
        "emergencyDisabled"
       ],
       "default": "active",
       "description": "Set by `setWalletRiskRuleStatus`, not by publishing the rule set. A rule not `active` is evaluated for nothing (VM close-out, 29 September)."
      },
      "statusReason": {
       "type": "string",
       "nullable": true,
       "readOnly": true
      },
      "statusUntil": {
       "type": "string",
       "format": "date-time",
       "nullable": true,
       "readOnly": true,
       "description": "When a `suspended` rule returns to `active` by itself."
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
