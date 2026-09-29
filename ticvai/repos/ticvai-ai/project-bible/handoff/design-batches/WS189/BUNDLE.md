# WS189 — Wallet Configuration Backend Structure v1.0 board 4

**10 screens · 6 operations · 8 schemas · 3 permissions**

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
  `APPROVAL_CONFIGURE, WALLET_OPERATE, WALLET_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-1113` | Shared Wallet Command Center | listDetail | 3 | 1 | — |
| `BO-1114` | Shared Wallet Model Configuration | configEditor | 1 | 0 | — |
| `BO-1115` | Family & Household Structure Configuration | configEditor | 1 | 0 | — |
| `BO-1116` | Parent–Child Stored Value Distribution | configEditor | 2 | 0 | — |
| `BO-1117` | Allowance & Budget Allocation Engine | configEditor | 1 | 0 | — |
| `BO-1118` | Member Spending Controls & Permissions | configEditor | 1 | 0 | — |
| `BO-1119` | Corporate Wallet & Organizational Hierarchy | configEditor | 2 | 0 | — |
| `BO-1120` | Corporate Budget, Policy & Approval Rules | configEditor | 2 | 0 | — |
| `BO-1121` | Shared Wallet Transfers & Balance Reallocation | configEditor | 1 | 0 | — |
| `BO-1122` | Shared Wallet Simulator, Monitoring & Audit | listDetail | 2 | 0 | — |

## Thin screens in this batch

**BO-1122 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-1113",
  "name": "Shared Wallet Command Center",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "4",
   "number": "01",
   "page": 38
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/shared-wallet-command-center-bo-1113",
   "component": "apps/venue-management-web/src/routes/orders-money/SharedWalletCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-1114",
    "BO-1115",
    "BO-1116",
    "BO-1117",
    "BO-1118",
    "BO-1119",
    "BO-1120",
    "BO-1121",
    "BO-1122"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "BO-1114",
     "trigger": "Shared Wallet Model Configuration",
     "provenance": "structural — pack board 4 wiring, 19 September 2026"
    },
    {
     "to": "BO-1115",
     "trigger": "Family & Household Structure Configuration",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "carries": [
      "sharedWalletId"
     ]
    },
    {
     "to": "BO-1116",
     "trigger": "Parent–Child Stored Value Distribution",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "carries": [
      "sharedWalletId",
      "walletId"
     ]
    },
    {
     "to": "BO-1117",
     "trigger": "Allowance & Budget Allocation Engine",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "carries": [
      "sharedWalletId"
     ]
    },
    {
     "to": "BO-1118",
     "trigger": "Member Spending Controls & Permissions",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "carries": [
      "sharedWalletId"
     ]
    },
    {
     "to": "BO-1119",
     "trigger": "Corporate Wallet & Organizational Hierarchy",
     "provenance": "structural — pack board 4 wiring, 19 September 2026"
    },
    {
     "to": "BO-1120",
     "trigger": "Corporate Budget, Policy & Approval Rules",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "carries": [
      "sharedWalletId"
     ]
    },
    {
     "to": "BO-1121",
     "trigger": "Shared Wallet Transfers & Balance Reallocation",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "carries": [
      "walletId"
     ]
    },
    {
     "to": "BO-1122",
     "trigger": "Shared Wallet Simulator, Monitoring & Audit",
     "provenance": "structural — pack board 4 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide administrators with a centralized operational view of all Family, Parent–Child and Corporate wallets. Backend Configuration & Monitoring",
  "purposeNote": "Authorized administrators can monitor shared-wallet structures and drill down from consolidated information to individual wallets, members, allocations and transactions.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 38 §Display"
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
       "label": "Every shared wallet",
       "columns": [
        "Total shared wallets",
        "Family wallets",
        "Parent–child wallets",
        "Corporate wallets",
        "School/group wallets",
        "Active linked users",
        "Total shared balance",
        "Allocated balance",
        "Unallocated balance",
        "Spending today",
        "Transfers today",
        "Wallets approaching limits",
        "Suspended child/member access",
        "Pending invitations/associations"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 38 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected shared wallet",
       "bindsTo": null,
       "columns": [
        "Total shared wallets",
        "Family wallets",
        "Parent–child wallets",
        "Corporate wallets",
        "School/group wallets",
        "Active linked users",
        "Total shared balance",
        "Allocated balance",
        "Unallocated balance",
        "Spending today",
        "Transfers today",
        "Wallets approaching limits",
        "Suspended child/member access",
        "Pending invitations/associations"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Break down wallets by”.",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 38 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create Shared Wallet",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 38 §Provide quick actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Add Member",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 38 §Provide quick actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Adjust Limits",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 38 §Provide quick actions"
      },
      {
       "kind": "destructiveButton",
       "label": "Suspend Member",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 38 §Provide quick actions"
      },
      {
       "kind": "secondaryButton",
       "label": "View Transactions",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 38 §Provide quick actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Investigate Exceptions",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 38 §Provide quick actions"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmSuspendMember",
    "component": "confirmDialog",
    "trigger": "Suspend Member",
    "body": "**Suspend Member on a shared wallet is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 38 §Provide quick actions"
   }
  ],
  "states": {
   "loading": "The shared wallet list.",
   "error": "Could not load. Names which read failed and leaves the shared wallet untouched.",
   "emptyFirstRun": "No shared wallet yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the shared wallet are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listSharedWallets",
    "contract": "wallet",
    "purpose": "Family and corporate structures",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "createSharedWallet",
    "contract": "wallet",
    "purpose": "Set up a family, household or corporate wallet",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration): serves the pack action(s) Create Shared Wallet; Add Member, Adjust Limits, Suspend Member",
    "invalidates": [
     "listSharedWallets"
    ]
   },
   {
    "operationId": "setSharedWalletMembers",
    "contract": "wallet",
    "purpose": "Add a member, change limits, or suspend a member (activeTo)",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration): serves the pack action(s) Create Shared Wallet; Add Member, Adjust Limits, Suspend Member",
    "invalidates": [
     "listSharedWallets"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "Total shared wallets",
    "Family wallets",
    "Parent–child wallets",
    "Corporate wallets",
    "School/group wallets",
    "Active linked users"
   ],
   "params": [
    {
     "name": "sharedWalletId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1113",
   "workshopBoard": "wireframes/WS189 Wallet Configuration Backend Structure v1.0 Board 4.dc.html#bo-1113"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 38. 0 of 14 labels bound to a contract property; 20 of 33 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Create Shared Wallet: `createSharedWallet`; Add Member, Adjust Limits, Suspend Member: `setSharedWalletMembers`; View Transactions, Investigate Exceptions dropped (navigation).",
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
  "id": "BO-1114",
  "name": "Shared Wallet Model Configuration",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "4",
   "number": "02",
   "page": 39
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/shared-wallet-model-configuration-bo-1114",
   "component": "apps/venue-management-web/src/routes/orders-money/SharedWalletModelConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1113"
   ],
   "exitTo": [
    "BO-1113"
   ],
   "transitions": [
    {
     "to": "BO-1113",
     "trigger": "Back to Shared Wallet Command Center",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "sharedWalletId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Define reusable shared-wallet structures. Administrators can create models such as: Family Wallet Parent–Child Wallet Corporate Wallet Employee Wallet School Wallet Student Wallet Tour Group Wallet Event Group Wallet Hospitality Group Wallet Balance Models Model A — Fully Shared Balance Parent:",
  "purposeNote": "customer or venue.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Wallet model",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 39 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Ownership type",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 39 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum members",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 39 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Shared balance allowed",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 39 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Individual allocations allowed",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 39 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Hybrid mode",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 39 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Transfer capability",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 39 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Credit sharing",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 39 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Default permissions",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 39 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Default spending policy",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 39 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Applicable credit types",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 39 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The shared wallet model configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the shared wallet model untouched.",
   "emptyFirstRun": "No shared wallet model configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "createSharedWallet",
    "contract": "wallet",
    "purpose": "Set one up",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listSharedWallets"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1114",
   "workshopBoard": "wireframes/WS189 Wallet Configuration Backend Structure v1.0 Board 4.dc.html#bo-1114"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 39. 0 of 0 labels bound to a contract property; 11 of 38 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1115",
  "name": "Family & Household Structure Configuration",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "4",
   "number": "03",
   "page": 40
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/family-household-structure-configuration-bo-1115",
   "component": "apps/venue-management-web/src/routes/orders-money/FamilyHouseholdStructureConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1113"
   ],
   "exitTo": [
    "BO-1113"
   ],
   "transitions": [
    {
     "to": "BO-1113",
     "trigger": "Back to Shared Wallet Command Center",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "sharedWalletId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure family relationships and wallet participation. The source requires customers to register individually or as a family/group, with a designated owner able to allocate budgets to linked accounts and monitor/cancel spending authorization. Supported Roles Family Owner Co-Owner Parent Guardian Adult Member Child Dependant Viewer",
  "purposeNote": "Authorized users can create and maintain family structures while preserving individual identities and wallet permissions.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Primary account holder",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 40 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Secondary parent/guardian",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 40 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Dependants",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 40 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Relationship type",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 40 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum family members",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 40 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Member invitation",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 40 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Member verification",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 40 §Configure"
      },
      {
       "kind": "textField",
       "label": "Approval required to join",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 40 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Removal rules",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 40 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Member status",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 40 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Effective dates",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 40 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The family household structure configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the family household structure untouched.",
   "emptyFirstRun": "No family household structure configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setSharedWalletMembers",
    "contract": "wallet",
    "purpose": "Household members and roles",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listSharedWallets"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1115",
   "workshopBoard": "wireframes/WS189 Wallet Configuration Backend Structure v1.0 Board 4.dc.html#bo-1115"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 40. 0 of 0 labels bound to a contract property; 11 of 41 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
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
  "id": "BO-1116",
  "name": "Parent–Child Stored Value Distribution",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "4",
   "number": "04",
   "page": 41
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/parent-child-stored-value-distribution-bo-1116",
   "component": "apps/venue-management-web/src/routes/orders-money/ParentChildStoredValueDistribution.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1113"
   ],
   "exitTo": [
    "BO-1113"
   ],
   "transitions": [
    {
     "to": "BO-1113",
     "trigger": "Back to Shared Wallet Command Center",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "sharedWalletId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure the amusement-park style parent-card/child-card wallet model required specifically by 4.3.38. Example Parent Wallet Available Stored Value: AED 1,000",
  "purposeNote": "Multiple child credentials can securely consume configured stored value from a parent-controlled wallet while respecting individual restrictions.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Parent wallet",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 41 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Child/dependant account",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 41 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Child card",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 41 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Child wristband",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 41 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum linked children",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 41 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Shared-value access",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 41 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Allocated-value access",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 41 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum spend",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 41 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Per-transaction limit",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 41 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Daily limit",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 41 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Venue restriction",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 41 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Product/category restriction",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 41 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Time restriction",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 41 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Credit-type restriction",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 41 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The parent–child stored value configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the parent–child stored value untouched.",
   "emptyFirstRun": "No parent–child stored value configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setSharedWalletMembers",
    "contract": "wallet",
    "purpose": "Parent and child distribution",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listSharedWallets"
    ]
   },
   {
    "operationId": "transferWalletBalance",
    "contract": "wallet",
    "purpose": "Move value between them",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getWallet",
     "listWalletTransactions"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1116",
   "workshopBoard": "wireframes/WS189 Wallet Configuration Backend Structure v1.0 Board 4.dc.html#bo-1116"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 41. 0 of 0 labels bound to a contract property; 14 of 34 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "sharedWalletId",
     "from": "navigation"
    },
    {
     "name": "walletId",
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
  "id": "BO-1117",
  "name": "Allowance & Budget Allocation Engine",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "4",
   "number": "05",
   "page": 42
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/allowance-budget-allocation-engine-bo-1117",
   "component": "apps/venue-management-web/src/routes/orders-money/AllowanceBudgetAllocationEngine.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1113"
   ],
   "exitTo": [
    "BO-1113"
   ],
   "transitions": [
    {
     "to": "BO-1113",
     "trigger": "Back to Shared Wallet Command Center",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "sharedWalletId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure how wallet owners distribute value to linked members. Allocation Types One-time allowance Daily allowance Weekly allowance Monthly allowance Event allowance Attraction allowance Meal allowance Ride allowance Shopping allowance Custom allocation",
  "purposeNote": "Wallet owners or authorized administrators can distribute stored value according to configurable allocation rules while preserving central financial control.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Allocation amount",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 42 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Credit type",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 42 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Start date",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 42 §Configure"
      },
      {
       "kind": "selectField",
       "label": "End date",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 42 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Frequency",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 42 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Auto-renewal",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 42 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Unused-balance behavior",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 42 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Carry-forward",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 42 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Return-to-parent",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 42 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Expiry",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 42 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Reallocation",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 42 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Funding priority",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 42 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The allowance budget allocation configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the allowance budget allocation untouched.",
   "emptyFirstRun": "No allowance budget allocation configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setSharedWalletMembers",
    "contract": "wallet",
    "purpose": "Allowance and budget",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listSharedWallets"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1117",
   "workshopBoard": "wireframes/WS189 Wallet Configuration Backend Structure v1.0 Board 4.dc.html#bo-1117"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 42. 0 of 0 labels bound to a contract property; 12 of 31 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
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
  "id": "BO-1118",
  "name": "Member Spending Controls & Permissions",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "4",
   "number": "06",
   "page": 43
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/member-spending-controls-permissions-bo-1118",
   "component": "apps/venue-management-web/src/routes/orders-money/MemberSpendingControlsPermissions.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1113"
   ],
   "exitTo": [
    "BO-1113"
   ],
   "transitions": [
    {
     "to": "BO-1113",
     "trigger": "Back to Shared Wallet Command Center",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "sharedWalletId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§For each member configure; Configure) and no display directory — it is settings, not a population",
  "purpose": "Give wallet owners granular control over what each linked member can do. The source explicitly requires family owners to cap expenses and cancel spending authorization at any time. Permission Controls",
  "purposeNote": "Every member transaction is evaluated against that member's current permissions and spending policy before wallet value is authorized.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "View balance",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 43 §For each member configure"
      },
      {
       "kind": "selectField",
       "label": "Spend",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 43 §For each member configure"
      },
      {
       "kind": "selectField",
       "label": "Top up",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 43 §For each member configure"
      },
      {
       "kind": "selectField",
       "label": "Receive funds",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 43 §For each member configure"
      },
      {
       "kind": "selectField",
       "label": "Transfer funds",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 43 §For each member configure"
      },
      {
       "kind": "selectField",
       "label": "Send funds",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 43 §For each member configure"
      },
      {
       "kind": "selectField",
       "label": "Redeem vouchers",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 43 §For each member configure"
      },
      {
       "kind": "selectField",
       "label": "Use gift cards",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 43 §For each member configure"
      },
      {
       "kind": "selectField",
       "label": "Use membership benefits",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 43 §For each member configure"
      },
      {
       "kind": "selectField",
       "label": "Add payment method",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 43 §For each member configure"
      },
      {
       "kind": "selectField",
       "label": "Add/remove wearable",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 43 §For each member configure"
      },
      {
       "kind": "selectField",
       "label": "View transaction history",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 43 §For each member configure"
      },
      {
       "kind": "selectField",
       "label": "Spending Controls",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 43 §For each member configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum transaction amount",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 43 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Hourly limit",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 43 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Daily limit",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 43 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Weekly limit",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 43 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Monthly limit",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 43 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Number of transactions",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 43 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Product/category restrictions",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 43 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Venue restrictions",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 43 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Channel restrictions",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 43 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Time restrictions",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 43 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The member spending controls configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the member spending controls untouched.",
   "emptyFirstRun": "No member spending controls configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setSharedWalletMembers",
    "contract": "wallet",
    "purpose": "Spending controls per member",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listSharedWallets"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1118",
   "workshopBoard": "wireframes/WS189 Wallet Configuration Backend Structure v1.0 Board 4.dc.html#bo-1118"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 43. 0 of 0 labels bound to a contract property; 23 of 37 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
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
  "id": "BO-1119",
  "name": "Corporate Wallet & Organizational Hierarchy",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "4",
   "number": "07",
   "page": 44
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/corporate-wallet-organizational-hierarchy-bo-1119",
   "component": "apps/venue-management-web/src/routes/orders-money/CorporateWalletOrganizationalHierarchy.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1113"
   ],
   "exitTo": [
    "BO-1113"
   ],
   "transitions": [
    {
     "to": "BO-1113",
     "trigger": "Back to Shared Wallet Command Center",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "sharedWalletId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure wallets for companies, schools, partners and other organizations. Requirement 4.3.27 calls specifically for corporate wallets with spending limits, user-level permissions, departmental allocation and reporting. Organizational Structure",
  "purposeNote": "configured organizational level.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Organization",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 44 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Business account",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 44 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Corporate wallet",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 44 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Cost center",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 44 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Department",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 44 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Team",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 44 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Employee/user",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 44 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Corporate hierarchy",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 44 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Budget owner",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 44 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Finance approver",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 44 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Wallet administrator",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 44 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The corporate wallet organizational configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the corporate wallet organizational untouched.",
   "emptyFirstRun": "No corporate wallet organizational configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "createSharedWallet",
    "contract": "wallet",
    "purpose": "Corporate hierarchy",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listSharedWallets"
    ]
   },
   {
    "operationId": "listSharedWallets",
    "contract": "wallet",
    "purpose": "Existing corporate wallets",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1119",
   "workshopBoard": "wireframes/WS189 Wallet Configuration Backend Structure v1.0 Board 4.dc.html#bo-1119"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 44. 0 of 0 labels bound to a contract property; 11 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-1120",
  "name": "Corporate Budget, Policy & Approval Rules",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "4",
   "number": "08",
   "page": 44
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/corporate-budget-policy-approval-rules-bo-1120",
   "component": "apps/venue-management-web/src/routes/orders-money/CorporateBudgetPolicyApprovalRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1113"
   ],
   "exitTo": [
    "BO-1113"
   ],
   "transitions": [
    {
     "to": "BO-1113",
     "trigger": "Back to Shared Wallet Command Center",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "sharedWalletId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Control how organizational wallet funds may be spent. Budget Configuration",
  "purposeNote": "Corporate spending follows configured budgets, policies and approval hierarchies before wallet funds are committed.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Corporate budget",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 44 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Department budget",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 44 §Configure"
      },
      {
       "kind": "selectField",
       "label": "User budget",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 44 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Period",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 44 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Currency",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 44 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Credit type",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 44 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Carry-forward",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 44 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Remaining-budget treatment",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 44 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Spending Policies",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 44 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Post-spend review",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 44 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Single approval",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 44 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Multi-level approval",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 44 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Exception approval",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 44 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The corporate budget policy configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the corporate budget policy untouched.",
   "emptyFirstRun": "No corporate budget policy configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "setSharedWalletMembers",
    "contract": "wallet",
    "purpose": "Corporate budget and policy",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listSharedWallets"
    ]
   },
   {
    "operationId": "setApprovalMatrix",
    "contract": "approvals",
    "purpose": "Set how corporate wallet spend is approved (levels, mode, thresholds)",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration): serves the pack action(s) Post-spend review, Single approval, Multi-level approval, Exception approval"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1120",
   "workshopBoard": "wireframes/WS189 Wallet Configuration Backend Structure v1.0 Board 4.dc.html#bo-1120"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 44. 0 of 0 labels bound to a contract property; 13 of 37 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Post-spend review, Single approval, Multi-level approval, Exception approval: `setApprovalMatrix`.",
  "entryState": {
   "params": [
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
  "id": "BO-1121",
  "name": "Shared Wallet Transfers & Balance Reallocation",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "4",
   "number": "09",
   "page": 45
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/shared-wallet-transfers-balance-reallocation-bo-1121",
   "component": "apps/venue-management-web/src/routes/orders-money/SharedWalletTransfersBalanceReallocation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1113"
   ],
   "exitTo": [
    "BO-1113"
   ],
   "transitions": [
    {
     "to": "BO-1113",
     "trigger": "Back to Shared Wallet Command Center",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Manage movement of stored value within a family or corporate wallet structure. Supported Operations Family Parent → Child Child → Parent Parent → Parent Child → Child (if permitted) Corporate Corporate → Department Department → Employee Employee → Department Department → Corporate Department → Department",
  "purposeNote": "All internal balance reallocations are controlled, ledgered and traceable to their source and destination.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Transfer permission",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 45 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Transferable credit types",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 45 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Minimum transfer",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 45 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum transfer",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 45 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Daily transfer limit",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 45 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Approval requirement",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 45 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Transfer fees",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 45 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Expiry inheritance",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 45 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Source-credit preservation",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 45 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Return unused allocation",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 45 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Automatic reallocation",
       "provenance": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 45 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The shared wallet transfers configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the shared wallet transfers untouched.",
   "emptyFirstRun": "No shared wallet transfers configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "transferWalletBalance",
    "contract": "wallet",
    "purpose": "Reallocate balance",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getWallet",
     "listWalletTransactions"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1121",
   "workshopBoard": "wireframes/WS189 Wallet Configuration Backend Structure v1.0 Board 4.dc.html#bo-1121"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 45. 0 of 0 labels bound to a contract property; 11 of 30 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "walletId",
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
  "id": "BO-1122",
  "name": "Shared Wallet Simulator, Monitoring & Audit",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Wallet_Configuration_Backend_Structure_v1.0.pdf",
   "board": "4",
   "number": "10",
   "page": 46
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money/shared-wallet-simulator-monitoring-audit-bo-1122",
   "component": "apps/venue-management-web/src/routes/orders-money/SharedWalletSimulatorMonitoringAudit.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-1113"
   ],
   "exitTo": [
    "BO-1113"
   ],
   "transitions": [
    {
     "to": "BO-1113",
     "trigger": "Back to Shared Wallet Command Center",
     "provenance": "structural — pack board 4 wiring, 19 September 2026",
     "back": true,
     "carries": [
      "sharedWalletId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Test complex family/corporate wallet policies before publication and provide complete traceability after activation. Simulation Example Family Wallet Balance: AED 1,500 Child A Daily Limit: AED 100 Used Today: AED 70 Requested Transaction: AED 50 Wallet Balance → PASS Member Permission → PASS Product Eligibility → PASS Daily Limit → FAIL Remaining allowance = AED 30 Result Transaction Declined Reason: Daily member spending limit exceeded. Corporate Simulation Configure the complete lifecycle of gift cards, digital vouchers, coupons, campaign rewards, complimentary credits and membership-related benefits stored or presented inside the TICVAI Wallet. This board covers the requirements to support gift-card balances, digital vouchers, membership-related credits and benefits, activation, partial redemption, expiry, balance inquiry, transaction history, gift-card liability, and integration with other TICVAI modules.",
  "purposeNote": "Shared-wallet policies can be simulated before publication, and every configuration or financial action remains traceable through immutable audit history. Board 4 — Backend Logic",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 46"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Wallet_Configuration_Backend_Structure_v1.0.pdf, page 46"
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
       "impliedBy": "listSharedWallets",
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
   "loading": "The shared wallet simulator list.",
   "error": "Could not load. Names which read failed and leaves the shared wallet simulator untouched.",
   "emptyFirstRun": "No shared wallet simulator yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the shared wallet simulator are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "simulateCreditConsumption",
    "contract": "wallet",
    "purpose": "Simulate a member spend",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listSharedWallets",
    "contract": "wallet",
    "purpose": "Monitor the structures",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1122",
   "workshopBoard": "wireframes/WS189 Wallet Configuration Backend Structure v1.0 Board 4.dc.html#bo-1122"
  },
  "apisNote": "Regenerated 9 September 2026 from Wallet_Configuration_Backend_Structure_v1.0.pdf page 46. 0 of 0 labels bound to a contract property; 0 of 85 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "createSharedWallet": {
  "method": "POST",
  "path": "/shared-wallets",
  "contract": "wallet",
  "summary": "Set up a family, household or corporate wallet",
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
  "requestBody": "SharedWallet",
  "responds": "SharedWallet"
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
 "transferWalletBalance": {
  "method": "POST",
  "path": "/wallets/{walletId}/transfer",
  "contract": "wallet",
  "summary": "Send balance to another guest",
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
  "responds": "WalletTransaction"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "ApprovalKind": {
  "type": "string",
  "description": "11.1.7 and 11.1.30–11.1.37. **The first four already exist as bespoke implementations** and this contract is what they collapse into.\n**Which actions route here — decided 28 September, audit R144.** Finance and procurement acts go through this engine to a **finance approver**: closing a fiscal period (`periodClose`), reopening one (`periodReopen`), cancelling a purchase order (`purchaseOrderCancel`) and closing one short (`purchaseOrderShortClose`). The tenant default matrix for each of these names the finance approver role; a venue may tighten it and never loosen it. Starting a release rollout routes through `releasePromotion` to the platform release manager (a holder of `PLATFORM_RELEASE_PROMOTE`). **Not every `requiresApproval` goes here:** reopening a shift, recounting a stock count and a retail return above the venue threshold take a supervisor's step-up on the same device instead, and never raise a request.\n**Catalogue change requests route through `productChange` and `pricingChange`** (decided 29 September, writers pass): a product change and a price or pricing change raised in `catalogue` ask for approval under these two kinds, so a venue can route product edits and price edits to different approvers.\n",
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
   "tenantMigration",
   "productChange",
   "pricingChange"
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
