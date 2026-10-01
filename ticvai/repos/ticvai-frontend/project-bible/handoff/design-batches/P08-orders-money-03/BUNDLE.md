# P08-orders-money-03 — P08 · Orders & Money (3 of 3)

**7 screens · 42 operations · 39 schemas · 8 permissions**

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

- **Every control that can be refused must be gated.** 8 permissions apply here:
  `ACCOUNT_CONFIGURE, LEDGER_APPROVE, LEDGER_POST, LEDGER_VIEW, ORDER_VIEW, SETTLEMENT_VIEW, TAX_CONFIGURE, TENANT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-074` | Chart of Accounts | listDetail | 8 | 4 | — |
| `BO-075` | Account Mapping | commandCentre | 8 | 4 | — |
| `BO-076` | Revenue Recognition | listDetail | 5 | 2 | — |
| `BO-077` | FX Rates & Variances | approvalInbox | 5 | 3 | — |
| `BO-089` | Journal Entries | approvalInbox | 6 | 4 | — |
| `BO-090` | Period Close | listDetail | 7 | 3 | — |
| `BO-101` | Orders & Money | listDetail | 3 | 0 | — |

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-074",
  "name": "Chart of Accounts",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/finance/chart-of-accounts",
   "component": "apps/venue-management-web/src/routes/finance/ChartOfAccounts.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-075",
    "BO-076",
    "BO-077"
   ],
   "inferred": true,
   "fromFlows": true,
   "transitions": [
    {
     "to": "BO-075",
     "trigger": "Maps products to accounts",
     "provenance": "flow F16 step 5→6, F98 step 2→3"
    },
    {
     "to": "BO-077",
     "trigger": "FX Rates & Variances",
     "provenance": "derived — BO-077 declares entryState.params varianceId and BO-074 holds none of them. The edge carries nothing: varianceId only pre-selects (deep link or optional), and BO-077 opens on its own"
    }
   ],
   "entryFrom": [
    "BO-043"
   ]
  },
  "notes": "Added 17 August because the contract had operations no screen declared. **Not on the wireframe board** — needs drawing. Pulled to Wave 1 (CF-101). **F16 says it itself** — no chart of accounts blocks the first sale, so it cannot be Wave 2 while venue provisioning is Wave 1.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listAccounts` reads the population and `getAccount` reads one of them — list, select, act",
  "purpose": "Accounts, cost centres and legal entities.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Legal entity id",
       "operation": "listAccounts",
       "notes": "Sends `?legalEntityId=` to `listAccounts`.",
       "provenance": "contract finance.yaml GET /accounts"
      },
      {
       "kind": "textField",
       "label": "Type",
       "operation": "listAccounts",
       "notes": "Sends `?type=` to `listAccounts`.",
       "provenance": "contract finance.yaml GET /accounts"
      },
      {
       "kind": "toggle",
       "label": "Is postable",
       "operation": "listAccounts",
       "notes": "Sends `?isPostable=` to `listAccounts`.",
       "provenance": "contract finance.yaml GET /accounts"
      },
      {
       "kind": "dataTable",
       "label": "Every account",
       "bindsTo": "Account",
       "columns": [
        "Account.id",
        "Account.code",
        "Account.externalCode",
        "Account.isSuspense",
        "Account.subType",
        "Account.tags",
        "Account.notes",
        "Account.name",
        "Account.type",
        "Account.parentId",
        "Account.legalEntityId",
        "Account.currency"
       ],
       "operation": "listAccounts",
       "provenance": "contract finance.yaml GET /accounts"
      },
      {
       "kind": "dataTable",
       "label": "Every cost center",
       "bindsTo": "CostCenter",
       "columns": [
        "CostCenter.id",
        "CostCenter.code",
        "CostCenter.name",
        "CostCenter.parentId",
        "CostCenter.venueId",
        "CostCenter.isActive"
       ],
       "operation": "listCostCenters",
       "provenance": "contract finance.yaml GET /cost-centers"
      },
      {
       "kind": "dataTable",
       "label": "Every legal entity",
       "bindsTo": "LegalEntity",
       "columns": [
        "LegalEntity.id",
        "LegalEntity.code",
        "LegalEntity.name",
        "LegalEntity.countryCode",
        "LegalEntity.currency",
        "LegalEntity.currencyScale",
        "LegalEntity.taxRegistrationNumber",
        "LegalEntity.fiscalYearStartMonth",
        "LegalEntity.regionIds",
        "LegalEntity.isActive",
        "LegalEntity.scopePath"
       ],
       "operation": "listLegalEntities",
       "provenance": "contract finance.yaml GET /legal-entities"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected account",
       "bindsTo": "Account",
       "columns": [
        "Account.id",
        "Account.code",
        "Account.externalCode",
        "Account.isSuspense",
        "Account.subType",
        "Account.tags",
        "Account.notes",
        "Account.name",
        "Account.type",
        "Account.parentId",
        "Account.legalEntityId",
        "Account.currency",
        "Account.isPostable",
        "Account.isActive",
        "Account.balance"
       ],
       "operation": "getAccount",
       "provenance": "contract finance.yaml GET /accounts/{accountId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create account",
       "operation": "createAccount",
       "provenance": "contract finance.yaml POST /accounts"
      },
      {
       "kind": "secondaryButton",
       "label": "Save account",
       "operation": "updateAccount",
       "provenance": "contract finance.yaml PATCH /accounts/{accountId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Create cost center",
       "operation": "createCostCenter",
       "provenance": "contract finance.yaml POST /cost-centers"
      },
      {
       "kind": "secondaryButton",
       "label": "Create legal entity",
       "operation": "createLegalEntity",
       "provenance": "contract finance.yaml POST /legal-entities"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The chart accounts list.",
   "error": "Could not load. Names which read failed and leaves the chart accounts untouched.",
   "emptyFirstRun": "No chart accounts yet. Offers Create account (`createAccount`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on legalEntityId, type, isPostable and the chart accounts are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `LEDGER_VIEW`, which `listAccounts` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAccounts",
    "contract": "finance",
    "purpose": "List the chart of accounts",
    "trigger": "onLoad"
   },
   {
    "operationId": "getAccount",
    "contract": "finance",
    "purpose": "Read an account",
    "trigger": "onAction"
   },
   {
    "operationId": "createAccount",
    "contract": "finance",
    "purpose": "Create an account",
    "trigger": "onAction",
    "invalidates": [
     "listAccounts"
    ]
   },
   {
    "operationId": "updateAccount",
    "contract": "finance",
    "purpose": "Rename, remap or deactivate an account",
    "trigger": "onAction",
    "invalidates": [
     "listAccounts"
    ]
   },
   {
    "operationId": "listCostCenters",
    "contract": "finance",
    "purpose": "List cost centres",
    "trigger": "onLoad"
   },
   {
    "operationId": "createCostCenter",
    "contract": "finance",
    "purpose": "Create a cost centre",
    "trigger": "onAction",
    "invalidates": [
     "listAccounts"
    ]
   },
   {
    "operationId": "listLegalEntities",
    "contract": "finance",
    "purpose": "List legal entities",
    "trigger": "onLoad"
   },
   {
    "operationId": "createLegalEntity",
    "contract": "finance",
    "purpose": "Create a legal entity",
    "trigger": "onAction",
    "invalidates": [
     "listAccounts"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "accountId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `accountId`.",
   "preloaded": [
    "Account.id",
    "Account.code",
    "Account.externalCode",
    "Account.isSuspense",
    "Account.subType"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-074"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 8 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formCreateAccount",
    "component": "modal",
    "trigger": "Create account",
    "body": "**Collects what `createAccount` sends before it is called.** Required: `code`, `name`, `type`, `legalEntityId`. Optional: `externalCode`, `parentId`, `isPostable`, `isSuspense`, `subType`, `tags`, `notes`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateAccountRequest",
    "confirm": {
     "label": "Create account",
     "operation": "createAccount"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "code",
      "name",
      "type",
      "legalEntityId",
      "externalCode",
      "parentId",
      "isPostable",
      "isSuspense",
      "subType",
      "tags",
      "notes"
     ]
    },
    "provenance": "contract finance.yaml POST /accounts"
   },
   {
    "id": "formUpdateAccount",
    "component": "modal",
    "trigger": "Save account",
    "body": "**Collects what `updateAccount` sends before it is called.** Nothing in the body is required. Optional: `code`, `name`, `externalCode`, `isActive`, `isSuspense`, `subType`, `tags`, `notes`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save account",
     "operation": "updateAccount"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "code",
      "name",
      "externalCode",
      "isActive",
      "isSuspense",
      "subType",
      "tags",
      "notes"
     ]
    },
    "provenance": "contract finance.yaml PATCH /accounts/{accountId}"
   },
   {
    "id": "formCreateCostCenter",
    "component": "modal",
    "trigger": "Create cost center",
    "body": "**Collects what `createCostCenter` sends before it is called.** Required: `code`, `name`. Optional: `parentId`, `venueId`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Create cost center",
     "operation": "createCostCenter"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "code",
      "name",
      "parentId",
      "venueId"
     ]
    },
    "provenance": "contract finance.yaml POST /cost-centers"
   },
   {
    "id": "formCreateLegalEntity",
    "component": "modal",
    "trigger": "Create legal entity",
    "body": "**Collects what `createLegalEntity` sends before it is called.** Required: `id`, `code`, `name`, `countryCode`, `currency`, `currencyScale`, `fiscalYearStartMonth`. Optional: `taxRegistrationNumber`, `regionIds`, `isActive`, `scopePath`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "LegalEntity",
    "confirm": {
     "label": "Create legal entity",
     "operation": "createLegalEntity"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "code",
      "name",
      "countryCode",
      "currency",
      "currencyScale",
      "fiscalYearStartMonth",
      "taxRegistrationNumber",
      "regionIds",
      "isActive",
      "scopePath"
     ]
    },
    "provenance": "contract finance.yaml POST /legal-entities"
   }
  ],
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
  "id": "BO-075",
  "name": "Account Mapping",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/finance/account-mapping",
   "component": "apps/venue-management-web/src/routes/finance/AccountMapping.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-074",
    "BO-076",
    "BO-077"
   ],
   "inferred": true,
   "fromFlows": true,
   "transitions": [
    {
     "to": "BO-076",
     "trigger": "Revenue Recognition",
     "provenance": "flow F98 step 3→4"
    },
    {
     "to": "BO-074",
     "trigger": "Chart of Accounts",
     "carries": [
      "accountId"
     ],
     "provenance": "derived — BO-074 declares entryState.params accountId and BO-075 holds accountId, so an edge into it carries them"
    },
    {
     "to": "BO-077",
     "trigger": "FX Rates & Variances",
     "provenance": "derived — BO-077 declares entryState.params varianceId and BO-075 holds none of them. The edge carries nothing: varianceId only pre-selects (deep link or optional), and BO-077 opens on its own"
    },
    {
     "to": "ADM-020",
     "trigger": "Creates the first venue manager",
     "provenance": "flow F16 step 6→7",
     "crossesDevice": true,
     "back": false
    }
   ]
  },
  "notes": "Added 17 August because the contract had operations no screen declared. **Not on the wireframe board** — needs drawing. Pulled to Wave 1 (CF-101). Without a mapping every sale posts to suspense. **Cross-platform navigation removed 24 August**: ADM-020. **A till does not navigate to a back office and a guest app does not navigate to either** — those are device handovers, and a flow declares them with `crossesDevice` rather than a screen pretending there is a link.",
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "3 independent reads and no read of one record — the screen watches a population rather than working one",
  "purpose": "Which product or movement posts to which account.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Account mappings",
       "bindsTo": "AccountMapping",
       "operation": "listAccountMappings",
       "provenance": "contract finance.yaml GET /account-mappings"
      },
      {
       "kind": "metricTile",
       "label": "Tax codes",
       "bindsTo": "TaxCode",
       "operation": "listTaxCodes",
       "provenance": "contract finance.yaml GET /tax-codes"
      },
      {
       "kind": "metricTile",
       "label": "Tax exemptions",
       "bindsTo": "TaxExemption",
       "operation": "listTaxExemptions",
       "provenance": "contract finance.yaml GET /tax-exemptions"
      },
      {
       "kind": "dataTable",
       "label": "Every account mapping",
       "bindsTo": "AccountMapping",
       "columns": [
        "AccountMapping.eventType",
        "AccountMapping.debitAccountId",
        "AccountMapping.creditAccountId",
        "AccountMapping.venueId"
       ],
       "operation": "listAccountMappings",
       "provenance": "contract finance.yaml GET /account-mappings"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save account mappings",
       "operation": "setAccountMappings",
       "provenance": "contract finance.yaml PUT /account-mappings"
      },
      {
       "kind": "secondaryButton",
       "label": "Create tax code",
       "operation": "createTaxCode",
       "provenance": "contract finance.yaml POST /tax-codes"
      },
      {
       "kind": "secondaryButton",
       "label": "Save tax code",
       "operation": "updateTaxCode",
       "provenance": "contract finance.yaml PATCH /tax-codes/{taxCodeId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Create tax exemption",
       "operation": "createTaxExemption",
       "provenance": "contract finance.yaml POST /tax-exemptions"
      },
      {
       "kind": "primaryButton",
       "label": "Verify tax exemption",
       "operation": "verifyTaxExemption",
       "provenance": "contract finance.yaml POST /tax-exemptions/{exemptionId}/verify (decided 29 September, VM close-out)"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The account mapping figures; each tile loads on its own.",
   "error": "Could not load. Names which read failed and leaves the account mapping untouched.",
   "emptyFirstRun": "No account mapping yet. Offers Create tax code (`createTaxCode`).",
   "emptyNoResults": "Never shown: `listAccountMappings` takes no filter, so an empty list is always the first-run state above.",
   "emptyNoAccess": "Shown when the caller lacks `LEDGER_VIEW`, which `listAccountMappings` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAccountMappings",
    "contract": "finance",
    "purpose": "Which account each transaction type posts to",
    "trigger": "onLoad"
   },
   {
    "operationId": "setAccountMappings",
    "contract": "finance",
    "purpose": "Set posting mappings",
    "trigger": "onAction",
    "invalidates": [
     "listAccountMappings"
    ]
   },
   {
    "operationId": "listTaxCodes",
    "contract": "finance",
    "purpose": "List tax codes",
    "trigger": "onLoad"
   },
   {
    "operationId": "createTaxCode",
    "contract": "finance",
    "purpose": "Create a tax code",
    "trigger": "onAction",
    "invalidates": [
     "listAccountMappings"
    ]
   },
   {
    "operationId": "updateTaxCode",
    "contract": "finance",
    "purpose": "Amend a tax code",
    "trigger": "onAction",
    "invalidates": [
     "listAccountMappings"
    ]
   },
   {
    "operationId": "listTaxExemptions",
    "contract": "finance",
    "purpose": "List tax exemptions",
    "trigger": "onLoad"
   },
   {
    "operationId": "createTaxExemption",
    "contract": "finance",
    "purpose": "Grant a tax exemption",
    "trigger": "onAction",
    "invalidates": [
     "listAccountMappings"
    ]
   },
   {
    "operationId": "verifyTaxExemption",
    "contract": "finance",
    "purpose": "Verify tax exemption",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "taxCodeId",
     "from": "deepLink"
    },
    {
     "name": "exemptionId",
     "from": "navigation"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `taxCodeId`."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-075"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 7 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formSetAccountMappings",
    "component": "modal",
    "trigger": "Save account mappings",
    "body": "**Collects what `setAccountMappings` sends before it is called.** Required: `mappings`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save account mappings",
     "operation": "setAccountMappings"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "mappings"
     ]
    },
    "provenance": "contract finance.yaml PUT /account-mappings"
   },
   {
    "id": "formCreateTaxCode",
    "component": "modal",
    "trigger": "Create tax code",
    "body": "**Collects what `createTaxCode` sends before it is called.** Required: `code`, `name`, `countryCode`, `rate`, `accountId`, `effectiveFrom`. Optional: `compoundOnTaxCodeId`, `isInclusive`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateTaxCodeRequest",
    "confirm": {
     "label": "Create tax code",
     "operation": "createTaxCode"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "code",
      "name",
      "countryCode",
      "rate",
      "accountId",
      "effectiveFrom",
      "compoundOnTaxCodeId",
      "isInclusive"
     ]
    },
    "provenance": "contract finance.yaml POST /tax-codes"
   },
   {
    "id": "formUpdateTaxCode",
    "component": "modal",
    "trigger": "Save tax code",
    "body": "**Collects what `updateTaxCode` sends before it is called.** Nothing in the body is required. Optional: `name`, `rate`, `effectiveFrom`, `isActive`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save tax code",
     "operation": "updateTaxCode"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "name",
      "rate",
      "effectiveFrom",
      "isActive"
     ]
    },
    "provenance": "contract finance.yaml PATCH /tax-codes/{taxCodeId}"
   },
   {
    "id": "formCreateTaxExemption",
    "component": "modal",
    "trigger": "Create tax exemption",
    "body": "**Collects what `createTaxExemption` sends before it is called.** Required: `id`, `scope`, `taxCodeId`, `reason`. Optional: `scopeRef`, `certificateReference`, `validFrom`, `validTo`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "TaxExemption",
    "confirm": {
     "label": "Create tax exemption",
     "operation": "createTaxExemption"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "scope",
      "taxCodeId",
      "reason",
      "scopeRef",
      "certificateReference",
      "validFrom",
      "validTo"
     ]
    },
    "provenance": "contract finance.yaml POST /tax-exemptions"
   }
  ],
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
  "id": "BO-076",
  "name": "Revenue Recognition",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/finance/revenue-recognition",
   "component": "apps/venue-management-web/src/routes/finance/RevenueRecognition.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-074",
    "BO-075",
    "BO-077"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "BO-074",
     "trigger": "Chart of Accounts",
     "provenance": "derived — BO-074 declares entryState.params accountId and BO-076 holds none of them. The edge carries nothing: accountId only pre-selects (deep link or optional), and BO-074 opens on its own"
    },
    {
     "to": "BO-075",
     "trigger": "Account Mapping",
     "provenance": "derived — BO-075 declares entryState.params exemptionId, taxCodeId and BO-076 holds none of them. The edge carries nothing: taxCodeId only pre-selects (deep link or optional); BO-075 finds exemptionId (listTaxExemptions) itself, and BO-075 opens on its own"
    },
    {
     "to": "BO-077",
     "trigger": "FX Rates & Variances",
     "provenance": "derived — BO-077 declares entryState.params varianceId and BO-076 holds none of them. The edge carries nothing: varianceId only pre-selects (deep link or optional), and BO-077 opens on its own"
    }
   ]
  },
  "notes": "Added 17 August because the contract had operations no screen declared. **Not on the wireframe board** — needs drawing.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listRecognitionSchedules` reads the population and `getDeferredRevenue` reads one of them — list, select, act",
  "purpose": "Deferred revenue, its ageing, and the schedules that release it.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every recognition schedule",
       "bindsTo": "RecognitionSchedule",
       "columns": [
        "RecognitionSchedule.id",
        "RecognitionSchedule.name",
        "RecognitionSchedule.method",
        "RecognitionSchedule.priority",
        "RecognitionSchedule.recognitionSite",
        "RecognitionSchedule.frequency",
        "RecognitionSchedule.revalidateOnValidityChange",
        "RecognitionSchedule.productKinds",
        "RecognitionSchedule.deferredAccountId",
        "RecognitionSchedule.recognisedAccountId",
        "RecognitionSchedule.breakageAccountId",
        "RecognitionSchedule.noShowTrigger"
       ],
       "operation": "listRecognitionSchedules",
       "provenance": "contract finance.yaml GET /recognition-schedules"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected recognition schedule",
       "bindsTo": "RecognitionSchedule",
       "columns": [
        "RecognitionSchedule.id",
        "RecognitionSchedule.name",
        "RecognitionSchedule.method",
        "RecognitionSchedule.priority",
        "RecognitionSchedule.recognitionSite",
        "RecognitionSchedule.frequency",
        "RecognitionSchedule.revalidateOnValidityChange",
        "RecognitionSchedule.productKinds",
        "RecognitionSchedule.deferredAccountId",
        "RecognitionSchedule.recognisedAccountId",
        "RecognitionSchedule.breakageAccountId",
        "RecognitionSchedule.noShowTrigger",
        "RecognitionSchedule.noShowAccountId",
        "RecognitionSchedule.breakageAfterDays",
        "RecognitionSchedule.isActive"
       ],
       "operation": "listRecognitionSchedules",
       "provenance": "contract finance.yaml GET /recognition-schedules"
      },
      {
       "kind": "detailPanel",
       "label": "The deferred revenue report",
       "bindsTo": "DeferredRevenueReport",
       "columns": [
        "DeferredRevenueReport.asAt",
        "DeferredRevenueReport.totals",
        "DeferredRevenueReport.total",
        "DeferredRevenueReport.buckets"
       ],
       "operation": "getDeferredRevenue",
       "provenance": "contract finance.yaml GET /deferred-revenue"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Run recognition",
       "operation": "runRecognition",
       "provenance": "contract finance.yaml POST /recognition/run"
      },
      {
       "kind": "secondaryButton",
       "label": "Create recognition schedule",
       "operation": "createRecognitionSchedule",
       "provenance": "contract finance.yaml POST /recognition-schedules"
      },
      {
       "kind": "secondaryButton",
       "label": "Validate recognition schedules",
       "operation": "validateRecognitionSchedules",
       "provenance": "contract finance.yaml POST /recognition-schedules/validate"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The revenue recognition list.",
   "error": "Could not load. Names which read failed and leaves the revenue recognition untouched.",
   "emptyFirstRun": "No revenue recognition yet. Offers Create recognition schedule (`createRecognitionSchedule`).",
   "emptyNoResults": "Never shown: `listRecognitionSchedules` takes no filter, so an empty list is always the first-run state above.",
   "emptyNoAccess": "Shown when the caller lacks `LEDGER_VIEW`, which `getDeferredRevenue` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getDeferredRevenue",
    "contract": "finance",
    "purpose": "Deferred revenue balance and ageing",
    "trigger": "onLoad"
   },
   {
    "operationId": "runRecognition",
    "contract": "finance",
    "purpose": "Recognise earned revenue for a period",
    "trigger": "onAction",
    "invalidates": [
     "listRecognitionSchedules"
    ]
   },
   {
    "operationId": "listRecognitionSchedules",
    "contract": "finance",
    "purpose": "List revenue recognition schedules",
    "trigger": "onLoad"
   },
   {
    "operationId": "createRecognitionSchedule",
    "contract": "finance",
    "purpose": "Define how a product class recognises revenue",
    "trigger": "onAction",
    "invalidates": [
     "listRecognitionSchedules"
    ]
   },
   {
    "operationId": "validateRecognitionSchedules",
    "contract": "finance",
    "purpose": "Find product kinds claimed by more than one schedule",
    "trigger": "onAction",
    "provenance": "wiring gap, 19 September 2026 — the screen showed the noun and could not act on it"
   }
  ],
  "entryState": {
   "preloaded": [
    "DeferredRevenueReport.asAt",
    "DeferredRevenueReport.total",
    "DeferredRevenueReport.buckets"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-076"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formRunRecognition",
    "component": "modal",
    "trigger": "Run recognition",
    "body": "**Collects what `runRecognition` sends before it is called.** Required: `fiscalPeriodId`. Optional: `dryRun`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Run recognition",
     "operation": "runRecognition"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "fiscalPeriodId",
      "dryRun"
     ]
    },
    "provenance": "contract finance.yaml POST /recognition/run"
   },
   {
    "id": "formCreateRecognitionSchedule",
    "component": "modal",
    "trigger": "Create recognition schedule",
    "body": "**Collects what `createRecognitionSchedule` sends before it is called.** Required: `id`, `name`, `method`, `productKinds`. Optional: `priority`, `recognitionSite`, `frequency`, `revalidateOnValidityChange`, `deferredAccountId`, `recognisedAccountId`, `breakageAccountId`, `noShowTrigger`, `noShowAccountId`, `breakageAfterDays`, `isActive`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "RecognitionSchedule",
    "confirm": {
     "label": "Create recognition schedule",
     "operation": "createRecognitionSchedule"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "name",
      "method",
      "productKinds",
      "priority",
      "recognitionSite",
      "frequency",
      "revalidateOnValidityChange",
      "deferredAccountId",
      "recognisedAccountId",
      "breakageAccountId",
      "noShowTrigger",
      "noShowAccountId",
      "breakageAfterDays",
      "isActive"
     ]
    },
    "provenance": "contract finance.yaml POST /recognition-schedules"
   }
  ],
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
  "id": "BO-077",
  "name": "FX Rates & Variances",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/finance/fx-rates-variances",
   "component": "apps/venue-management-web/src/routes/finance/FxRatesVariances.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-074",
    "BO-075",
    "BO-076"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "BO-074",
     "trigger": "Chart of Accounts",
     "provenance": "derived — BO-074 declares entryState.params accountId and BO-077 holds none of them. The edge carries nothing: accountId only pre-selects (deep link or optional), and BO-074 opens on its own"
    },
    {
     "to": "BO-075",
     "trigger": "Account Mapping",
     "provenance": "derived — BO-075 declares entryState.params exemptionId, taxCodeId and BO-077 holds none of them. The edge carries nothing: taxCodeId only pre-selects (deep link or optional); BO-075 finds exemptionId (listTaxExemptions) itself, and BO-075 opens on its own"
    }
   ]
  },
  "notes": "Added 17 August because the contract had operations no screen declared. **Not on the wireframe board** — needs drawing.",
  "density": "compact",
  "pattern": "approvalInbox",
  "patternReason": "`reviewPriceVariance` decides items that `listFxRates` queues — every row is waiting for a person, so the empty state is success",
  "purpose": "Rates, and the price variances waiting for review.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "queue",
     "components": [
      {
       "kind": "datePicker",
       "label": "As at",
       "operation": "listFxRates",
       "notes": "Sends `?asAt=` to `listFxRates`.",
       "provenance": "contract finance.yaml GET /fx-rates"
      },
      {
       "kind": "textField",
       "label": "Purpose",
       "operation": "listFxRates",
       "notes": "Sends `?purpose=` to `listFxRates`.",
       "provenance": "contract finance.yaml GET /fx-rates"
      },
      {
       "kind": "dataTable",
       "label": "Waiting for a decision",
       "bindsTo": "FxRate",
       "columns": [
        "FxRate.id",
        "FxRate.fromCurrency",
        "FxRate.toCurrency",
        "FxRate.rate",
        "FxRate.purpose",
        "FxRate.source",
        "FxRate.effectiveFrom",
        "FxRate.effectiveTo",
        "FxRate.setByPrincipalId",
        "FxRate.providerReference",
        "FxRate.fetchedAt"
       ],
       "operation": "listFxRates",
       "provenance": "contract finance.yaml GET /fx-rates"
      },
      {
       "kind": "dataTable",
       "label": "Every price variance",
       "bindsTo": "PriceVariance",
       "columns": [
        "PriceVariance.id",
        "PriceVariance.orderId",
        "PriceVariance.orderLineId",
        "PriceVariance.venueId",
        "PriceVariance.variantId",
        "PriceVariance.quotedPrice",
        "PriceVariance.serverPrice",
        "PriceVariance.variance",
        "PriceVariance.catalogueBundleVersion",
        "PriceVariance.isException",
        "PriceVariance.reviewStatus",
        "PriceVariance.reviewOutcome"
       ],
       "operation": "listPriceVariances",
       "provenance": "contract finance.yaml GET /price-variances"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "item",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected FX rate",
       "bindsTo": "FxRate",
       "columns": [
        "FxRate.id",
        "FxRate.fromCurrency",
        "FxRate.toCurrency",
        "FxRate.rate",
        "FxRate.purpose",
        "FxRate.source",
        "FxRate.effectiveFrom",
        "FxRate.effectiveTo",
        "FxRate.setByPrincipalId",
        "FxRate.providerReference",
        "FxRate.fetchedAt"
       ],
       "operation": "listFxRates",
       "provenance": "contract finance.yaml GET /fx-rates"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "decision",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save FX rate",
       "operation": "setFxRate",
       "provenance": "contract finance.yaml PUT /fx-rates"
      },
      {
       "kind": "secondaryButton",
       "label": "Review price variance",
       "operation": "reviewPriceVariance",
       "provenance": "contract finance.yaml POST /price-variances/{varianceId}/review"
      },
      {
       "kind": "secondaryButton",
       "label": "Ingest FX rates",
       "operation": "ingestFxRates",
       "provenance": "contract finance.yaml POST /fx-rates/ingest"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The rates variances list.",
   "error": "Could not load. Names which read failed and leaves the rates variances untouched.",
   "emptyFirstRun": "**Nothing is waiting, which is the good outcome.** An empty queue means every item has been decided; it offers no create action, because creating work is not what it needs.",
   "emptyNoResults": "Nothing matches the filter on asAt, purpose and the rates variances are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `LEDGER_VIEW`, which `listFxRates` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listFxRates",
    "contract": "finance",
    "purpose": "The rates in force",
    "trigger": "onLoad"
   },
   {
    "operationId": "setFxRate",
    "contract": "finance",
    "purpose": "Set a rate",
    "trigger": "onAction",
    "invalidates": [
     "listFxRates"
    ]
   },
   {
    "operationId": "listPriceVariances",
    "contract": "finance",
    "purpose": "List price variances",
    "trigger": "onLoad"
   },
   {
    "operationId": "reviewPriceVariance",
    "contract": "finance",
    "purpose": "Record a review decision on an exception variance",
    "trigger": "onAction",
    "invalidates": [
     "listFxRates"
    ]
   },
   {
    "operationId": "ingestFxRates",
    "contract": "finance",
    "purpose": "Pull today's rates from the configured provider",
    "trigger": "onAction",
    "provenance": "wiring gap, 19 September 2026 — the screen showed the noun and could not act on it",
    "invalidates": [
     "listFxRates"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "varianceId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `varianceId`.",
   "preloaded": [
    "FxRate.id",
    "FxRate.fromCurrency",
    "FxRate.toCurrency",
    "FxRate.rate",
    "FxRate.purpose"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-077"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formIngestFxRates",
    "component": "modal",
    "trigger": "Ingest FX rates",
    "body": "**Collects what `ingestFxRates` sends before it is called.** Required: `purpose`. Optional: `pairs`, `effectiveFrom`, `dryRun`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Ingest FX rates",
     "operation": "ingestFxRates"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "purpose",
      "pairs",
      "effectiveFrom",
      "dryRun"
     ]
    },
    "provenance": "contract finance.yaml POST /fx-rates/ingest"
   },
   {
    "id": "formSetFxRate",
    "component": "modal",
    "trigger": "Save FX rate",
    "body": "**Collects what `setFxRate` sends before it is called.** Required: `fromCurrency`, `toCurrency`, `rate`, `purpose`, `effectiveFrom`. Optional: `id`, `source`, `effectiveTo`, `setByPrincipalId`, `providerReference`, `fetchedAt`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "FxRate",
    "confirm": {
     "label": "Save FX rate",
     "operation": "setFxRate"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "fromCurrency",
      "toCurrency",
      "rate",
      "purpose",
      "effectiveFrom",
      "id",
      "source",
      "effectiveTo",
      "setByPrincipalId",
      "providerReference",
      "fetchedAt"
     ]
    },
    "provenance": "contract finance.yaml PUT /fx-rates"
   },
   {
    "id": "formReviewPriceVariance",
    "component": "modal",
    "trigger": "Review price variance",
    "body": "**Collects what `reviewPriceVariance` sends before it is called.** Required: `outcome`, `note`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Review price variance",
     "operation": "reviewPriceVariance"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "outcome",
      "note"
     ]
    },
    "provenance": "contract finance.yaml POST /price-variances/{varianceId}/review"
   }
  ],
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
  "id": "BO-089",
  "name": "Journal Entries",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/finance/journal-entries",
   "component": "apps/venue-management-web/src/routes/finance/JournalEntries.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-074",
    "BO-075",
    "BO-076",
    "BO-090"
   ],
   "inferred": true,
   "fromFlows": true,
   "transitions": [
    {
     "to": "BO-090",
     "trigger": "Begins the close",
     "provenance": "flow F13 step 3→4"
    },
    {
     "to": "BO-074",
     "trigger": "Chart of Accounts",
     "carries": [
      "accountId"
     ],
     "provenance": "derived — BO-074 declares entryState.params accountId and BO-089 holds accountId, so an edge into it carries them"
    },
    {
     "to": "BO-075",
     "trigger": "Account Mapping",
     "provenance": "derived — BO-075 declares entryState.params exemptionId, taxCodeId and BO-089 holds none of them. The edge carries nothing: taxCodeId only pre-selects (deep link or optional); BO-075 finds exemptionId (listTaxExemptions) itself, and BO-075 opens on its own"
    }
   ]
  },
  "notes": "Added 17 August because the contract had operations no screen declared. **Not on the wireframe board** — needs drawing.",
  "density": "compact",
  "pattern": "approvalInbox",
  "patternReason": "`approveJournalEntry` decides items that `listJournalEntries` queues — every row is waiting for a person, so the empty state is success",
  "purpose": "Every posting, and the ones waiting for approval.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "queue",
     "components": [
      {
       "kind": "textField",
       "label": "Fiscal period id",
       "operation": "listJournalEntries",
       "notes": "Sends `?fiscalPeriodId=` to `listJournalEntries`.",
       "provenance": "contract finance.yaml GET /journal-entries"
      },
      {
       "kind": "textField",
       "label": "Status",
       "operation": "listJournalEntries",
       "notes": "Sends `?status=` to `listJournalEntries`.",
       "provenance": "contract finance.yaml GET /journal-entries"
      },
      {
       "kind": "textField",
       "label": "Source",
       "operation": "listJournalEntries",
       "notes": "Sends `?source=` to `listJournalEntries`.",
       "provenance": "contract finance.yaml GET /journal-entries"
      },
      {
       "kind": "dataTable",
       "label": "Waiting for a decision",
       "bindsTo": "JournalEntry",
       "columns": [
        "JournalEntry.id",
        "JournalEntry.entryNumber",
        "JournalEntry.fiscalPeriodId",
        "JournalEntry.status",
        "JournalEntry.source",
        "JournalEntry.sourceId",
        "JournalEntry.description",
        "JournalEntry.reference",
        "JournalEntry.lines",
        "JournalEntry.totalDebit",
        "JournalEntry.totalCredit",
        "JournalEntry.postedByPrincipalId"
       ],
       "operation": "listJournalEntries",
       "provenance": "contract finance.yaml GET /journal-entries"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "item",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected journal entry",
       "bindsTo": "JournalEntry",
       "columns": [
        "JournalEntry.id",
        "JournalEntry.entryNumber",
        "JournalEntry.fiscalPeriodId",
        "JournalEntry.status",
        "JournalEntry.source",
        "JournalEntry.sourceId",
        "JournalEntry.description",
        "JournalEntry.reference",
        "JournalEntry.lines",
        "JournalEntry.totalDebit",
        "JournalEntry.totalCredit",
        "JournalEntry.postedByPrincipalId",
        "JournalEntry.approvedByPrincipalId",
        "JournalEntry.reversalOfEntryId",
        "JournalEntry.reversedByEntryId",
        "JournalEntry.postedAt"
       ],
       "operation": "getJournalEntry",
       "provenance": "contract finance.yaml GET /journal-entries/{entryId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "decision",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create journal entry",
       "operation": "createJournalEntry",
       "provenance": "contract finance.yaml POST /journal-entries"
      },
      {
       "kind": "secondaryButton",
       "label": "Approve journal entry",
       "operation": "approveJournalEntry",
       "provenance": "contract finance.yaml POST /journal-entries/{entryId}/approve"
      },
      {
       "kind": "destructiveButton",
       "label": "Reject journal",
       "operation": "rejectJournal",
       "provenance": "contract finance.yaml POST /journal-entries/{entryId}/reject"
      },
      {
       "kind": "destructiveButton",
       "label": "Reverse journal entry",
       "operation": "reverseJournalEntry",
       "provenance": "contract finance.yaml POST /journal-entries/{entryId}/reverse"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmRejectJournal",
    "component": "confirmDialog",
    "trigger": "Reject journal",
    "body": "**Names what `rejectJournal` changes and what it leaves alone**, in the consequence rather than the verb. A journal entries this affects should be identified in the dialog, not just counted. **Collects what `rejectJournal` sends before it is called.** Required: `reason`.",
    "provenance": "contract finance.yaml POST /journal-entries/{entryId}/reject"
   },
   {
    "id": "confirmReverseJournalEntry",
    "component": "confirmDialog",
    "trigger": "Reverse journal entry",
    "body": "**Names what `reverseJournalEntry` changes and what it leaves alone**, in the consequence rather than the verb. A journal entries this affects should be identified in the dialog, not just counted. **Collects what `reverseJournalEntry` sends before it is called.** Required: `reason`. Optional: `fiscalPeriodId`.",
    "provenance": "contract finance.yaml POST /journal-entries/{entryId}/reverse"
   },
   {
    "id": "formCreateJournalEntry",
    "component": "modal",
    "trigger": "Create journal entry",
    "body": "**Collects what `createJournalEntry` sends before it is called.** Required: `id`, `fiscalPeriodId`, `description`, `lines`. Optional: `postingDate`, `reference`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateJournalEntryRequest",
    "confirm": {
     "label": "Create journal entry",
     "operation": "createJournalEntry"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "fiscalPeriodId",
      "description",
      "lines",
      "postingDate",
      "reference"
     ]
    },
    "provenance": "contract finance.yaml POST /journal-entries"
   },
   {
    "id": "formApproveJournalEntry",
    "component": "modal",
    "trigger": "Approve journal entry",
    "body": "**Collects what `approveJournalEntry` sends before it is called.** Nothing in the body is required. Optional: `note`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Approve journal entry",
     "operation": "approveJournalEntry"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "note"
     ]
    },
    "provenance": "contract finance.yaml POST /journal-entries/{entryId}/approve"
   }
  ],
  "states": {
   "loading": "The journal entries list.",
   "error": "Could not load. Names which read failed and leaves the journal entries untouched.",
   "emptyFirstRun": "**Nothing is waiting, which is the good outcome.** An empty queue means every item has been decided; it offers no create action, because creating work is not what it needs.",
   "emptyNoResults": "Nothing matches the filter on fiscalPeriodId, status, source and the journal entries are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `LEDGER_VIEW`, which `listJournalEntries` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listJournalEntries",
    "contract": "finance",
    "purpose": "List journal entries",
    "trigger": "onLoad"
   },
   {
    "operationId": "getJournalEntry",
    "contract": "finance",
    "purpose": "Read a journal entry",
    "trigger": "onAction"
   },
   {
    "operationId": "createJournalEntry",
    "contract": "finance",
    "purpose": "Post a manual journal voucher",
    "trigger": "onAction",
    "invalidates": [
     "listJournalEntries"
    ]
   },
   {
    "operationId": "approveJournalEntry",
    "contract": "finance",
    "purpose": "Approve a journal entry and post it",
    "trigger": "onAction",
    "invalidates": [
     "listJournalEntries"
    ]
   },
   {
    "operationId": "rejectJournal",
    "contract": "finance",
    "purpose": "Reject a journal awaiting approval",
    "trigger": "onAction",
    "invalidates": [
     "listJournalEntries"
    ]
   },
   {
    "operationId": "reverseJournalEntry",
    "contract": "finance",
    "purpose": "Reverse a posted entry",
    "trigger": "onAction",
    "invalidates": [
     "listJournalEntries"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "entryId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `entryId`.",
   "preloaded": [
    "JournalEntry.id",
    "JournalEntry.entryNumber",
    "JournalEntry.fiscalPeriodId",
    "JournalEntry.status",
    "JournalEntry.source"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-089"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 6 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "BO-090",
  "name": "Period Close",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/finance/period-close",
   "component": "apps/venue-management-web/src/routes/finance/PeriodClose.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-040",
    "BO-074",
    "BO-075",
    "BO-076"
   ],
   "inferred": true,
   "fromFlows": true,
   "transitions": [
    {
     "to": "BO-040",
     "trigger": "Clears outstanding shift variances",
     "provenance": "flow F13 step 1→2"
    },
    {
     "to": "BO-074",
     "trigger": "Chart of Accounts",
     "carries": [
      "accountId"
     ],
     "provenance": "derived — BO-074 declares entryState.params accountId and BO-090 holds accountId, so an edge into it carries them"
    },
    {
     "to": "BO-075",
     "trigger": "Account Mapping",
     "provenance": "derived — BO-075 declares entryState.params exemptionId, taxCodeId and BO-090 holds none of them. The edge carries nothing: taxCodeId only pre-selects (deep link or optional); BO-075 finds exemptionId (listTaxExemptions) itself, and BO-075 opens on its own"
    }
   ]
  },
  "notes": "Added 17 August because the contract had operations no screen declared. **Not on the wireframe board** — needs drawing.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listFiscalPeriods` reads the population and `getTrialBalance` reads one of them — list, select, act",
  "purpose": "Close a fiscal period, and see what is stopping it.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Legal entity id",
       "operation": "listFiscalPeriods",
       "notes": "Sends `?legalEntityId=` to `listFiscalPeriods`.",
       "provenance": "contract finance.yaml GET /fiscal-periods"
      },
      {
       "kind": "textField",
       "label": "Status",
       "operation": "listFiscalPeriods",
       "notes": "Sends `?status=` to `listFiscalPeriods`.",
       "provenance": "contract finance.yaml GET /fiscal-periods"
      },
      {
       "kind": "dataTable",
       "label": "Every fiscal period",
       "bindsTo": "FiscalPeriod",
       "columns": [
        "FiscalPeriod.id",
        "FiscalPeriod.legalEntityId",
        "FiscalPeriod.name",
        "FiscalPeriod.startDate",
        "FiscalPeriod.endDate",
        "FiscalPeriod.status",
        "FiscalPeriod.closedByPrincipalId",
        "FiscalPeriod.closedAt"
       ],
       "operation": "listFiscalPeriods",
       "provenance": "contract finance.yaml GET /fiscal-periods"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected fiscal period",
       "bindsTo": "FiscalPeriod",
       "columns": [
        "FiscalPeriod.id",
        "FiscalPeriod.legalEntityId",
        "FiscalPeriod.name",
        "FiscalPeriod.startDate",
        "FiscalPeriod.endDate",
        "FiscalPeriod.status",
        "FiscalPeriod.closedByPrincipalId",
        "FiscalPeriod.closedAt",
        "FiscalPeriod.events"
       ],
       "operation": "listFiscalPeriods",
       "provenance": "contract finance.yaml GET /fiscal-periods"
      },
      {
       "kind": "detailPanel",
       "label": "The trial balance",
       "bindsTo": "TrialBalance",
       "columns": [
        "TrialBalance.fiscalPeriodId",
        "TrialBalance.isBalanced",
        "TrialBalance.totalDebit",
        "TrialBalance.totalCredit",
        "TrialBalance.accounts"
       ],
       "operation": "getTrialBalance",
       "provenance": "contract finance.yaml GET /ledger/trial-balance"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Begin period close",
       "operation": "beginPeriodClose",
       "provenance": "contract finance.yaml POST /fiscal-periods/{periodId}/begin-close"
      },
      {
       "kind": "destructiveButton",
       "label": "Close fiscal period",
       "operation": "closeFiscalPeriod",
       "provenance": "contract finance.yaml POST /fiscal-periods/{periodId}/close"
      },
      {
       "kind": "destructiveButton",
       "label": "Abandon period close",
       "operation": "abandonPeriodClose",
       "provenance": "contract finance.yaml POST /fiscal-periods/{periodId}/abandon-close"
      },
      {
       "kind": "secondaryButton",
       "label": "Reopen period",
       "operation": "reopenPeriod",
       "provenance": "contract finance.yaml POST /fiscal-periods/{periodId}/reopen"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmCloseFiscalPeriod",
    "component": "confirmDialog",
    "trigger": "Close fiscal period",
    "body": "**Names what `closeFiscalPeriod` changes and what it leaves alone**, in the consequence rather than the verb. A period close this affects should be identified in the dialog, not just counted. **Collects what `closeFiscalPeriod` sends before it is called.** Nothing in the body is required. Optional: `dryRun`. **A real close answers 202 pending a finance approver** (decided 28 September, audit R144): the period shows *close pending approval* with its `approvalRequestId` until the approver acts; a dry run answers at once.",
    "provenance": "contract finance.yaml POST /fiscal-periods/{periodId}/close"
   },
   {
    "id": "confirmAbandonPeriodClose",
    "component": "confirmDialog",
    "trigger": "Abandon period close",
    "body": "**Names what `abandonPeriodClose` changes and what it leaves alone**, in the consequence rather than the verb. A period close this affects should be identified in the dialog, not just counted. **Collects what `abandonPeriodClose` sends before it is called.** Required: `reason`.",
    "provenance": "contract finance.yaml POST /fiscal-periods/{periodId}/abandon-close"
   },
   {
    "id": "formReopenPeriod",
    "component": "modal",
    "trigger": "Reopen period",
    "body": "**Collects what `reopenPeriod` sends before it is called.** Required: `reason` only — the approver is not named here. **The request answers 202 with an `approvalRequestId`** and the period shows *reopen pending finance approval* until a finance approver acts (decided 28 September, audit R144). Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Reopen period",
     "operation": "reopenPeriod"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "reason"
     ]
    },
    "provenance": "contract finance.yaml POST /fiscal-periods/{periodId}/reopen"
   }
  ],
  "states": {
   "loading": "The period close list.",
   "error": "Could not load. Names which read failed and leaves the period close untouched.",
   "emptyFirstRun": "No period close yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on legalEntityId, status and the period close are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `LEDGER_VIEW`, which `listFiscalPeriods` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listFiscalPeriods",
    "contract": "finance",
    "purpose": "List fiscal periods",
    "trigger": "onLoad"
   },
   {
    "operationId": "beginPeriodClose",
    "contract": "finance",
    "purpose": "Begin closing a period",
    "trigger": "onAction",
    "invalidates": [
     "listFiscalPeriods"
    ]
   },
   {
    "operationId": "closeFiscalPeriod",
    "contract": "finance",
    "purpose": "Close a period and lock postings — 202 pending finance approval (audit R144)",
    "trigger": "onAction",
    "invalidates": [
     "listFiscalPeriods"
    ]
   },
   {
    "operationId": "abandonPeriodClose",
    "contract": "finance",
    "purpose": "Abandon a close in progress",
    "trigger": "onAction",
    "invalidates": [
     "listFiscalPeriods"
    ]
   },
   {
    "operationId": "reopenPeriod",
    "contract": "finance",
    "purpose": "Request to reopen a closed period — 202 pending finance approval (audit R144)",
    "trigger": "onAction",
    "invalidates": [
     "listFiscalPeriods"
    ]
   },
   {
    "operationId": "getTrialBalance",
    "contract": "finance",
    "purpose": "Trial balance for a period",
    "trigger": "onLoad"
   },
   {
    "operationId": "getVatReturn",
    "contract": "finance",
    "purpose": "VAT return (FTA boxes) for a period",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "periodId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `periodId`.",
   "preloaded": [
    "FiscalPeriod.id",
    "FiscalPeriod.legalEntityId",
    "FiscalPeriod.name",
    "FiscalPeriod.startDate",
    "FiscalPeriod.endDate"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-090"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 6 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "BO-101",
  "name": "Orders & Money",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 1,
  "implementation": {
   "app": "venue-management-web",
   "route": "/orders-money",
   "component": "apps/venue-management-web/src/routes/home/OrdersMoneyList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-008",
    "BO-022",
    "BO-023",
    "BO-024",
    "BO-025",
    "BO-026",
    "BO-027",
    "BO-028",
    "BO-029",
    "BO-039",
    "BO-040",
    "BO-041",
    "BO-042",
    "BO-043",
    "BO-047",
    "BO-048",
    "BO-059",
    "BO-061",
    "BO-062",
    "BO-065",
    "BO-074",
    "BO-075",
    "BO-076",
    "BO-077",
    "BO-089",
    "BO-090"
   ],
   "transitions": [
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "provenance": "derived — BO-008 declares entryState.params productId, variantId, version and BO-101 holds none of them. The edge carries nothing: productId only pre-selects (deep link or optional); BO-008 finds variantId (listProductVariants), version (searchMedia) itself, and BO-008 opens on its own"
    },
    {
     "to": "BO-022",
     "trigger": "Order Detail",
     "provenance": "derived — BO-022 declares entryState.params documentId, invoiceId, orderId and BO-101 holds none of them. The edge carries nothing: orderId only pre-selects (deep link or optional); BO-022 finds invoiceId (listTaxInvoices) itself; BO-022 opens on listOrders, and documentId has no source on BO-022 yet (a gap in BO-022, not in this edge)"
    },
    {
     "to": "BO-023",
     "trigger": "Refunds & Exchanges",
     "provenance": "derived — BO-023 declares entryState.params documentId, invoiceId, orderId and BO-101 holds none of them. The edge carries nothing: orderId only pre-selects (deep link or optional); BO-023 opens on listOrders, and documentId, invoiceId have no source on BO-023 yet (a gap in BO-023, not in this edge)"
    },
    {
     "to": "BO-024",
     "trigger": "Payment Exceptions",
     "provenance": "derived — BO-024 declares entryState.params depositId, paymentId and BO-101 holds none of them. The edge carries nothing: paymentId, depositId only pre-select (deep link or optional), and BO-024 opens on its own"
    },
    {
     "to": "BO-025",
     "trigger": "Chargebacks & Disputes",
     "carries": [
      "settlementId"
     ],
     "provenance": "derived — BO-025 declares entryState.params chargebackId, settlementId and BO-101 holds settlementId, so an edge into it carries them"
    },
    {
     "to": "BO-026",
     "trigger": "Group Bookings",
     "provenance": "derived — BO-026 declares entryState.params groupBookingId, orderId and BO-101 holds none of them. The edge carries nothing: orderId only pre-selects (deep link or optional); BO-026 finds groupBookingId (createGroupBooking) itself, and BO-026 opens on its own"
    },
    {
     "to": "BO-027",
     "trigger": "Reissue & Media Replacement",
     "provenance": "derived — BO-027 declares entryState.params mediaCode, mediaId and BO-101 holds none of them. The edge carries nothing: mediaCode, mediaId only pre-select (deep link or optional), and BO-027 opens on its own"
    },
    {
     "to": "BO-029",
     "trigger": "Report Builder",
     "provenance": "derived — BO-029 declares entryState.params conversationId, reportId and BO-101 holds none of them. The edge carries nothing: conversationId, reportId only pre-select (deep link or optional), and BO-029 opens on its own"
    },
    {
     "to": "BO-039",
     "trigger": "Shift Directory",
     "provenance": "derived — BO-039 declares entryState.params  and BO-101 holds none of them. The edge carries nothing: BO-039 needs nothing to open"
    },
    {
     "to": "BO-040",
     "trigger": "Variance Approval",
     "provenance": "derived — BO-040 declares entryState.params  and BO-101 holds none of them. The edge carries nothing: BO-040 needs nothing to open"
    },
    {
     "to": "BO-041",
     "trigger": "Cash Movements",
     "provenance": "derived — BO-041 declares entryState.params  and BO-101 holds none of them. The edge carries nothing: BO-041 needs nothing to open"
    },
    {
     "to": "BO-042",
     "trigger": "Banking & Safe",
     "provenance": "derived — BO-042 declares entryState.params boxId and BO-101 holds none of them. The edge carries nothing: BO-042 finds boxId (listDepositBoxes) itself, and BO-042 opens on its own"
    },
    {
     "to": "BO-043",
     "trigger": "Daily Reconciliation",
     "carries": [
      "settlementId"
     ],
     "provenance": "derived — BO-043 declares entryState.params settlementId and BO-101 holds settlementId, so an edge into it carries them"
    },
    {
     "to": "BO-047",
     "trigger": "Order Corrections & Exceptions",
     "provenance": "derived — BO-047 declares entryState.params orderId and BO-101 holds none of them. The edge carries nothing: orderId only pre-selects (deep link or optional), and BO-047 opens on its own"
    },
    {
     "to": "BO-048",
     "trigger": "Retail Products",
     "provenance": "derived — BO-048 declares entryState.params merchandiseId and BO-101 holds none of them. The edge carries nothing: merchandiseId only pre-selects (deep link or optional), and BO-048 opens on its own"
    },
    {
     "to": "BO-059",
     "trigger": "Sales Reports",
     "provenance": "derived — BO-059 declares entryState.params conversationId, reportId and BO-101 holds none of them. The edge carries nothing: conversationId, reportId only pre-select (deep link or optional), and BO-059 opens on its own"
    },
    {
     "to": "BO-061",
     "trigger": "Scheduled Reports",
     "provenance": "derived — BO-061 declares entryState.params reportId, scheduleId and BO-101 holds none of them. The edge carries nothing: reportId only pre-selects (deep link or optional); BO-061 finds scheduleId (listReportExecutions) itself, and BO-061 opens on its own"
    },
    {
     "to": "BO-062",
     "trigger": "Venue Profile",
     "provenance": "derived — BO-062 declares entryState.params  and BO-101 holds none of them. The edge carries nothing: BO-062 needs nothing to open"
    },
    {
     "to": "BO-065",
     "trigger": "Venue Configuration",
     "provenance": "derived — BO-065 declares entryState.params locationId and BO-101 holds none of them. The edge carries nothing: BO-065 finds locationId (listDeliveryLocations) itself, and BO-065 opens on its own"
    },
    {
     "to": "BO-074",
     "trigger": "Chart of Accounts",
     "provenance": "derived — BO-074 declares entryState.params accountId and BO-101 holds none of them. The edge carries nothing: accountId only pre-selects (deep link or optional), and BO-074 opens on its own"
    },
    {
     "to": "BO-075",
     "trigger": "Account Mapping",
     "provenance": "derived — BO-075 declares entryState.params exemptionId, taxCodeId and BO-101 holds none of them. The edge carries nothing: taxCodeId only pre-selects (deep link or optional); BO-075 finds exemptionId (listTaxExemptions) itself, and BO-075 opens on its own"
    },
    {
     "to": "BO-077",
     "trigger": "FX Rates & Variances",
     "provenance": "derived — BO-077 declares entryState.params varianceId and BO-101 holds none of them. The edge carries nothing: varianceId only pre-selects (deep link or optional), and BO-077 opens on its own"
    },
    {
     "to": "BO-089",
     "trigger": "Journal Entries",
     "provenance": "derived — BO-089 declares entryState.params entryId and BO-101 holds none of them. The edge carries nothing: entryId only pre-selects (deep link or optional), and BO-089 opens on its own"
    },
    {
     "to": "BO-090",
     "trigger": "Period Close",
     "provenance": "derived — BO-090 declares entryState.params periodId and BO-101 holds none of them. The edge carries nothing: periodId only pre-selects (deep link or optional), and BO-090 opens on its own"
    }
   ]
  },
  "notes": "Section landing. **28 screens reach the entry point through here** — before 20 August they reached it through nothing. **Given its section's own operations on 4 September.** It sat on `getVenueSettings` alone, which made it identical to every other section landing page — a hub that shows nothing of its section is a menu item, not a screen.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listOrders` reads the population and `getVenueSettings` reads one of them — list, select, act",
  "purpose": "Everything in orders & money, and what in it needs attention.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Venue id",
       "operation": "listOrders",
       "notes": "Sends `?venueId=` to `listOrders`.",
       "provenance": "contract orders.yaml GET /orders"
      },
      {
       "kind": "textField",
       "label": "Principal id",
       "operation": "listOrders",
       "notes": "Sends `?principalId=` to `listOrders`.",
       "provenance": "contract orders.yaml GET /orders"
      },
      {
       "kind": "textField",
       "label": "Shift id",
       "operation": "listOrders",
       "notes": "Sends `?shiftId=` to `listOrders`.",
       "provenance": "contract orders.yaml GET /orders"
      },
      {
       "kind": "textField",
       "label": "Status",
       "operation": "listOrders",
       "notes": "Sends `?status=` to `listOrders`.",
       "provenance": "contract orders.yaml GET /orders"
      },
      {
       "kind": "datePicker",
       "label": "Created from",
       "operation": "listOrders",
       "notes": "Sends `?createdFrom=` to `listOrders`.",
       "provenance": "contract orders.yaml GET /orders"
      },
      {
       "kind": "datePicker",
       "label": "Created to",
       "operation": "listOrders",
       "notes": "Sends `?createdTo=` to `listOrders`.",
       "provenance": "contract orders.yaml GET /orders"
      },
      {
       "kind": "dataTable",
       "label": "Every order",
       "bindsTo": "OrderSummary",
       "columns": [
        "OrderSummary.id",
        "OrderSummary.orderNumber",
        "OrderSummary.status",
        "OrderSummary.grossAmount",
        "OrderSummary.refundedAmount",
        "OrderSummary.channel",
        "OrderSummary.lineCount"
       ],
       "operation": "listOrders",
       "provenance": "contract orders.yaml GET /orders"
      },
      {
       "kind": "dataTable",
       "label": "Every settlement",
       "bindsTo": "Settlement",
       "columns": [
        "Settlement.id",
        "Settlement.currencyCode",
        "Settlement.providerName",
        "Settlement.periodStart",
        "Settlement.periodEnd",
        "Settlement.fileReference",
        "Settlement.format",
        "Settlement.status",
        "Settlement.lineCount",
        "Settlement.matchedCount",
        "Settlement.exceptionCount",
        "Settlement.providerGross"
       ],
       "operation": "listSettlements",
       "provenance": "contract finance.yaml GET /settlements"
      },
      {
       "kind": "cardList",
       "bindsTo": "screens",
       "notes": "28 screens, each with what needs attention.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "searchField",
       "label": "Search orders & money",
       "provenance": "carried from the previous definition"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected order",
       "bindsTo": "OrderSummary",
       "columns": [
        "OrderSummary.id",
        "OrderSummary.orderNumber",
        "OrderSummary.status",
        "OrderSummary.grossAmount",
        "OrderSummary.refundedAmount",
        "OrderSummary.channel",
        "OrderSummary.lineCount",
        "OrderSummary.principalId",
        "OrderSummary.holdLabel",
        "OrderSummary.heldUntil"
       ],
       "operation": "listOrders",
       "provenance": "contract orders.yaml GET /orders"
      },
      {
       "kind": "detailPanel",
       "label": "The venue settings",
       "bindsTo": "VenueSettings",
       "columns": [
        "VenueSettings.id",
        "VenueSettings.venueId",
        "VenueSettings.currencyCode",
        "VenueSettings.currencyScale",
        "VenueSettings.supportHours",
        "VenueSettings.quietHours",
        "VenueSettings.biometrics",
        "VenueSettings.segregatedAccess",
        "VenueSettings.alerting"
       ],
       "operation": "getVenueSettings",
       "provenance": "contract tenancy.yaml GET /venues/{venueId}/settings"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The list, with counts.",
   "error": "Could not load. Venue Home is still reachable.",
   "emptyFirstRun": "**Nothing configured in orders & money yet.** The action is the first thing to set up, not a blank list.",
   "emptyNoResults": "Nothing matches the filter.",
   "emptyNoAccess": "You do not have permission for orders & money. **Said plainly** — an empty section reads as broken."
  },
  "apis": [
   {
    "operationId": "getVenueSettings",
    "contract": "tenancy",
    "purpose": "What is enabled here",
    "trigger": "onLoad"
   },
   {
    "operationId": "listOrders",
    "contract": "orders",
    "purpose": "Orders taken in this venue",
    "trigger": "onLoad"
   },
   {
    "operationId": "listSettlements",
    "contract": "finance",
    "purpose": "Money settled and what is outstanding",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    }
   ],
   "coldEntry": "**Resolves from the session, so a cold arrival is the ordinary case** — a manager bookmarks the back office and opens it every morning. A principal with more than one venue is asked which before the page renders, rather than shown the first one.",
   "preloaded": [
    "VenueSettings.id",
    "VenueSettings.venueId",
    "VenueSettings.supportHours",
    "VenueSettings.quietHours",
    "VenueSettings.segregatedAccess"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-101"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 3 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
 "abandonPeriodClose": {
  "method": "POST",
  "path": "/fiscal-periods/{periodId}/abandon-close",
  "contract": "finance",
  "summary": "Abandon a close in progress",
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
 "approveJournalEntry": {
  "method": "POST",
  "path": "/journal-entries/{entryId}/approve",
  "contract": "finance",
  "summary": "Approve a journal entry and post it",
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
  "responds": "JournalEntry"
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
 "createAccount": {
  "method": "POST",
  "path": "/accounts",
  "contract": "finance",
  "summary": "Create an account",
  "permission": "ACCOUNT_CONFIGURE",
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
  "requestBody": "CreateAccountRequest",
  "responds": "Account"
 },
 "createCostCenter": {
  "method": "POST",
  "path": "/cost-centers",
  "contract": "finance",
  "summary": "Create a cost centre",
  "permission": "ACCOUNT_CONFIGURE",
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
  "responds": "CostCenter"
 },
 "createJournalEntry": {
  "method": "POST",
  "path": "/journal-entries",
  "contract": "finance",
  "summary": "Post a manual journal voucher",
  "permission": "LEDGER_POST",
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
  "requestBody": "CreateJournalEntryRequest",
  "responds": "JournalEntry"
 },
 "createLegalEntity": {
  "method": "POST",
  "path": "/legal-entities",
  "contract": "finance",
  "summary": "Create a legal entity",
  "permission": "ACCOUNT_CONFIGURE",
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
  "requestBody": "LegalEntity",
  "responds": "LegalEntity"
 },
 "createRecognitionSchedule": {
  "method": "POST",
  "path": "/recognition-schedules",
  "contract": "finance",
  "summary": "Define how a product class recognises revenue",
  "permission": "ACCOUNT_CONFIGURE",
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
  "requestBody": "RecognitionSchedule",
  "responds": "RecognitionSchedule"
 },
 "createTaxCode": {
  "method": "POST",
  "path": "/tax-codes",
  "contract": "finance",
  "summary": "Create a tax code",
  "permission": "TAX_CONFIGURE",
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
  "requestBody": "CreateTaxCodeRequest",
  "responds": "TaxCode"
 },
 "createTaxExemption": {
  "method": "POST",
  "path": "/tax-exemptions",
  "contract": "finance",
  "summary": "Grant a tax exemption",
  "permission": "TAX_CONFIGURE",
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
  "requestBody": "TaxExemption",
  "responds": "TaxExemption"
 },
 "getAccount": {
  "method": "GET",
  "path": "/accounts/{accountId}",
  "contract": "finance",
  "summary": "Read an account",
  "permission": "LEDGER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [],
  "requestBody": null,
  "responds": "Account"
 },
 "getDeferredRevenue": {
  "method": "GET",
  "path": "/deferred-revenue",
  "contract": "finance",
  "summary": "Deferred revenue balance and ageing",
  "permission": "LEDGER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "asAt",
    "in": "query",
    "required": null
   },
   {
    "name": "venueId",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "DeferredRevenueReport"
 },
 "getJournalEntry": {
  "method": "GET",
  "path": "/journal-entries/{entryId}",
  "contract": "finance",
  "summary": "Read a journal entry",
  "permission": "LEDGER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [],
  "requestBody": null,
  "responds": "JournalEntry"
 },
 "getTrialBalance": {
  "method": "GET",
  "path": "/ledger/trial-balance",
  "contract": "finance",
  "summary": "Trial balance for a period",
  "permission": "LEDGER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [
   {
    "name": "fiscalPeriodId",
    "in": "query",
    "required": true
   },
   {
    "name": "legalEntityId",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "TrialBalance"
 },
 "getVatReturn": {
  "method": "GET",
  "path": "/tax/vat-returns",
  "contract": "finance",
  "summary": "A legal entity's VAT return for a tax period, in the FTA's boxes",
  "permission": "LEDGER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [
   {
    "name": "legalEntityId",
    "in": "query",
    "required": true
   },
   {
    "name": "periodFrom",
    "in": "query",
    "required": true
   },
   {
    "name": "periodTo",
    "in": "query",
    "required": true
   },
   {
    "name": "format",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "FinVatReturn"
 },
 "getVenueSettings": {
  "method": "GET",
  "path": "/venues/{venueId}/settings",
  "contract": "tenancy",
  "summary": "Operational settings for this venue",
  "permission": "TENANT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "VenueSettings"
 },
 "ingestFxRates": {
  "method": "POST",
  "path": "/fx-rates/ingest",
  "contract": "finance",
  "summary": "Pull rates from the configured provider",
  "permission": "LEDGER_APPROVE",
  "offlineCapable": false,
  "conflictPolicy": "append",
  "scopeLevel": "region",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": null
 },
 "listAccountMappings": {
  "method": "GET",
  "path": "/account-mappings",
  "contract": "finance",
  "summary": "Which account each transaction type posts to",
  "permission": "LEDGER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
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
 "listAccounts": {
  "method": "GET",
  "path": "/accounts",
  "contract": "finance",
  "summary": "List the chart of accounts",
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
    "name": "type",
    "in": "query",
    "required": null
   },
   {
    "name": "isPostable",
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
 "listCostCenters": {
  "method": "GET",
  "path": "/cost-centers",
  "contract": "finance",
  "summary": "List cost centres",
  "permission": "LEDGER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
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
 "listFxRates": {
  "method": "GET",
  "path": "/fx-rates",
  "contract": "finance",
  "summary": "The rates in force",
  "permission": "LEDGER_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [
   {
    "name": "asAt",
    "in": "query",
    "required": null
   },
   {
    "name": "purpose",
    "in": "query",
    "required": null
   },
   {
    "name": "venueId",
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
 "listJournalEntries": {
  "method": "GET",
  "path": "/journal-entries",
  "contract": "finance",
  "summary": "List journal entries",
  "permission": "LEDGER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [
   {
    "name": "fiscalPeriodId",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "source",
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
 "listLegalEntities": {
  "method": "GET",
  "path": "/legal-entities",
  "contract": "finance",
  "summary": "List legal entities",
  "permission": "LEDGER_VIEW",
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
 "listOrders": {
  "method": "GET",
  "path": "/orders",
  "contract": "orders",
  "summary": "List orders",
  "permission": "ORDER_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "venueId",
    "in": "query",
    "required": null
   },
   {
    "name": "principalId",
    "in": "query",
    "required": null
   },
   {
    "name": "shiftId",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "createdFrom",
    "in": "query",
    "required": null
   },
   {
    "name": "createdTo",
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
 "listPriceVariances": {
  "method": "GET",
  "path": "/price-variances",
  "contract": "finance",
  "summary": "List price variances",
  "permission": "LEDGER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "venueId",
    "in": "query",
    "required": null
   },
   {
    "name": "exceptionsOnly",
    "in": "query",
    "required": null
   },
   {
    "name": "reviewStatus",
    "in": "query",
    "required": null
   },
   {
    "name": "occurredFrom",
    "in": "query",
    "required": null
   },
   {
    "name": "occurredTo",
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
 "listRecognitionSchedules": {
  "method": "GET",
  "path": "/recognition-schedules",
  "contract": "finance",
  "summary": "List revenue recognition schedules",
  "permission": "LEDGER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
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
 "listSettlements": {
  "method": "GET",
  "path": "/settlements",
  "contract": "finance",
  "summary": "List settlement batches",
  "permission": "SETTLEMENT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [
   {
    "name": "providerName",
    "in": "query",
    "required": null
   },
   {
    "name": "venueId",
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
 "listTaxCodes": {
  "method": "GET",
  "path": "/tax-codes",
  "contract": "finance",
  "summary": "List tax codes",
  "permission": "LEDGER_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [
   {
    "name": "countryCode",
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
 "listTaxExemptions": {
  "method": "GET",
  "path": "/tax-exemptions",
  "contract": "finance",
  "summary": "List tax exemptions",
  "permission": "LEDGER_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
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
 "rejectJournal": {
  "method": "POST",
  "path": "/journal-entries/{entryId}/reject",
  "contract": "finance",
  "summary": "Reject a journal awaiting approval",
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
  "responds": "JournalEntry"
 },
 "reopenPeriod": {
  "method": "POST",
  "path": "/fiscal-periods/{periodId}/reopen",
  "contract": "finance",
  "summary": "Reopen a closed period",
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
  "responds": null
 },
 "reverseJournalEntry": {
  "method": "POST",
  "path": "/journal-entries/{entryId}/reverse",
  "contract": "finance",
  "summary": "Reverse a posted entry",
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
  "responds": "JournalEntry"
 },
 "reviewPriceVariance": {
  "method": "POST",
  "path": "/price-variances/{varianceId}/review",
  "contract": "finance",
  "summary": "Record a review decision on an exception variance",
  "permission": "LEDGER_APPROVE",
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
  "responds": "PriceVariance"
 },
 "runRecognition": {
  "method": "POST",
  "path": "/recognition/run",
  "contract": "finance",
  "summary": "Recognise earned revenue for a period",
  "permission": "LEDGER_POST",
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
  "responds": "RecognitionRunResult"
 },
 "setAccountMappings": {
  "method": "PUT",
  "path": "/account-mappings",
  "contract": "finance",
  "summary": "Set posting mappings",
  "permission": "ACCOUNT_CONFIGURE",
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
  "responds": "AccountMapping"
 },
 "setFxRate": {
  "method": "PUT",
  "path": "/fx-rates",
  "contract": "finance",
  "summary": "Set a rate",
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
  "requestBody": "FxRate",
  "responds": "FxRate"
 },
 "updateAccount": {
  "method": "PATCH",
  "path": "/accounts/{accountId}",
  "contract": "finance",
  "summary": "Rename, remap or deactivate an account",
  "permission": "ACCOUNT_CONFIGURE",
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
  "responds": "Account"
 },
 "updateTaxCode": {
  "method": "PATCH",
  "path": "/tax-codes/{taxCodeId}",
  "contract": "finance",
  "summary": "Amend a tax code",
  "permission": "TAX_CONFIGURE",
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
  "responds": "TaxCode"
 },
 "validateRecognitionSchedules": {
  "method": "POST",
  "path": "/recognition-schedules/validate",
  "contract": "finance",
  "summary": "Find product kinds claimed by more than one schedule",
  "permission": "LEDGER_VIEW",
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
  "responds": null
 },
 "verifyTaxExemption": {
  "method": "POST",
  "path": "/tax-exemptions/{exemptionId}/verify",
  "contract": "finance",
  "summary": "Record that a tax exemption's evidence was checked",
  "permission": "TAX_CONFIGURE",
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
  "responds": "TaxExemption"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "Account": {
  "x-ticvai-persistence": "ledger.account",
  "type": "object",
  "required": [
   "id",
   "code",
   "name",
   "type",
   "legalEntityId",
   "isPostable",
   "isActive"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "code": {
    "type": "string",
    "maxLength": 64
   },
   "externalCode": {
    "type": "string",
    "nullable": true,
    "description": "Code in the client's own chart. Used on export so their team sees their codes."
   },
   "isSuspense": {
    "type": "boolean",
    "default": false,
    "description": "5.7.x. **Where a posting with no account mapping goes.** Today it has no destination, and a posting event that cannot be booked is a posting event that is silently dropped.\n**A suspense balance is a work queue, not a resting place.** It should trend to zero, and a balance that grows is the signal that a mapping is missing — which is the whole reason for having one rather than refusing the posting.\n"
   },
   "subType": {
    "type": "string",
    "nullable": true,
    "description": "5.7.27. **`AccountType` stays a closed enum of asset, liability, equity, revenue and expense because that is correct accounting**, and a venue wanting *Deferred Revenue — Annual Pass* is asking for a sub-type rather than a sixth type.\n"
   },
   "tags": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "How a venue groups accounts for its own reporting. Free-form, and outside the type."
   },
   "notes": {
    "type": "string",
    "nullable": true,
    "description": "5.7.27. Annotations on the account, which an auditor reads before the balance."
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "type": {
    "$ref": "#/components/schemas/AccountType"
   },
   "parentId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "legalEntityId": {
    "type": "string",
    "format": "uuid"
   },
   "currency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$"
   },
   "isPostable": {
    "type": "boolean",
    "description": "False for parent accounts, which aggregate only."
   },
   "isActive": {
    "type": "boolean"
   },
   "balance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   }
  }
 },
 "AccountMapping": {
  "x-ticvai-persistence": "ledger.account_mapping",
  "type": "object",
  "required": [
   "eventType",
   "debitAccountId",
   "creditAccountId"
  ],
  "properties": {
   "eventType": {
    "$ref": "#/components/schemas/PostingEventType"
   },
   "debitAccountId": {
    "type": "string",
    "format": "uuid"
   },
   "creditAccountId": {
    "type": "string",
    "format": "uuid"
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Null applies the mapping to every venue in the region."
   }
  }
 },
 "AccountType": {
  "type": "string",
  "enum": [
   "asset",
   "liability",
   "equity",
   "revenue",
   "expense"
  ]
 },
 "CostCenter": {
  "x-ticvai-persistence": "ledger.cost_center",
  "type": "object",
  "required": [
   "id",
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
   "parentId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "isActive": {
    "type": "boolean"
   }
  }
 },
 "CreateAccountRequest": {
  "type": "object",
  "required": [
   "code",
   "name",
   "type",
   "legalEntityId"
  ],
  "properties": {
   "code": {
    "type": "string",
    "maxLength": 64,
    "pattern": "^[A-Za-z0-9._-]+$"
   },
   "externalCode": {
    "type": "string",
    "maxLength": 64
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "type": {
    "$ref": "#/components/schemas/AccountType"
   },
   "parentId": {
    "type": "string",
    "format": "uuid"
   },
   "legalEntityId": {
    "type": "string",
    "format": "uuid"
   },
   "isPostable": {
    "type": "boolean",
    "default": true
   },
   "isSuspense": {
    "type": "boolean",
    "default": false,
    "description": "See `Account.isSuspense`."
   },
   "subType": {
    "type": "string",
    "nullable": true,
    "description": "See `Account.subType`."
   },
   "tags": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "See `Account.tags`."
   },
   "notes": {
    "type": "string",
    "nullable": true,
    "description": "See `Account.notes`."
   }
  }
 },
 "CreateJournalEntryRequest": {
  "type": "object",
  "required": [
   "id",
   "fiscalPeriodId",
   "description",
   "lines"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "fiscalPeriodId": {
    "type": "string",
    "format": "uuid"
   },
   "postingDate": {
    "type": "string",
    "format": "date",
    "description": "A day in the region's time zone, local midnight to local midnight."
   },
   "description": {
    "type": "string",
    "minLength": 3,
    "maxLength": 500
   },
   "reference": {
    "type": "string",
    "maxLength": 128
   },
   "lines": {
    "type": "array",
    "minItems": 2,
    "items": {
     "$ref": "#/components/schemas/JournalLine"
    }
   }
  }
 },
 "CreateTaxCodeRequest": {
  "type": "object",
  "required": [
   "code",
   "name",
   "countryCode",
   "rate",
   "effectiveFrom",
   "accountId"
  ],
  "properties": {
   "code": {
    "type": "string",
    "maxLength": 64
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "countryCode": {
    "type": "string",
    "pattern": "^[A-Z]{2}$"
   },
   "rate": {
    "type": "number",
    "minimum": 0,
    "maximum": 100
   },
   "compoundOnTaxCodeId": {
    "type": "string",
    "format": "uuid"
   },
   "isInclusive": {
    "type": "boolean",
    "default": false
   },
   "accountId": {
    "type": "string",
    "format": "uuid"
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date",
    "description": "A day in the region's time zone, local midnight to local midnight."
   }
  }
 },
 "DeferredRevenueReport": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "asAt",
   "totals",
   "buckets"
  ],
  "properties": {
   "asAt": {
    "type": "string",
    "format": "date",
    "description": "A day in the region's time zone, local midnight to local midnight."
   },
   "totals": {
    "type": "array",
    "description": "**One `Money` per currency in scope**, never a sum across currencies. One entry when every venue in scope trades in the same currency.\n",
    "items": {
     "$ref": "../shared/common.yaml#/components/schemas/Money"
    }
   },
   "total": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "The single total when everything in scope is in one currency; null otherwise. Read `totals`."
   },
   "buckets": {
    "type": "array",
    "description": "One ageing band in one currency per entry. A band spanning two currencies is two entries.",
    "items": {
     "type": "object",
     "required": [
      "label",
      "amount",
      "itemCount"
     ],
     "properties": {
      "label": {
       "type": "string",
       "description": "Ageing band by expected recognition date."
      },
      "amount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "itemCount": {
       "type": "integer"
      },
      "method": {
       "$ref": "#/components/schemas/RecognitionMethod"
      }
     }
    }
   }
  }
 },
 "FinVatReturn": {
  "x-ticvai-persistence": "none — computed from ledger postings on the reporting replica",
  "type": "object",
  "description": "6.1.23. The FTA VAT 201 boxes for one legal entity and tax period.",
  "required": [
   "legalEntityId",
   "periodFrom",
   "periodTo",
   "boxes",
   "netTaxPayable"
  ],
  "properties": {
   "legalEntityId": {
    "type": "string",
    "format": "uuid"
   },
   "taxRegistrationNumber": {
    "type": "string"
   },
   "periodFrom": {
    "type": "string",
    "format": "date"
   },
   "periodTo": {
    "type": "string",
    "format": "date"
   },
   "boxes": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "box",
      "amount",
      "taxAmount"
     ],
     "properties": {
      "box": {
       "type": "string",
       "description": "The form's box, e.g. `1a` (standard-rated supplies, Abu Dhabi) ... `1g`, `2` (tourist refunds), `3` (reverse charge), `4` (zero-rated), `5` (exempt), `6` and `7` (imports), `9` (standard-rated expenses), `10` (reverse charge inputs)."
      },
      "label": {
       "type": "string"
      },
      "emirate": {
       "type": "string",
       "nullable": true
      },
      "amount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "taxAmount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "adjustmentAmount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "taxCodeIds": {
       "type": "array",
       "items": {
        "type": "string",
        "format": "uuid"
       }
      },
      "postingCount": {
       "type": "integer"
      }
     }
    }
   },
   "totalOutputTax": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "totalRecoverableTax": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "netTaxPayable": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "fileUrl": {
    "type": "string",
    "format": "uri",
    "nullable": true,
    "description": "Set for `format` `csv` or `xlsx`; a short-lived link."
   },
   "generatedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
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
 "FxRate": {
  "type": "object",
  "x-ticvai-persistence": "ledger.fx_rate",
  "description": "Also the `setFxRate` body. **Server-owned fields are `readOnly`** and ignored if sent: `id`, `setByPrincipalId`, and the provenance `ingestFxRates` writes (`source`, `providerReference`, `fetchedAt`). A rate set through `setFxRate` has `source` `manual`.\n",
  "required": [
   "fromCurrency",
   "toCurrency",
   "rate",
   "purpose",
   "effectiveFrom"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "fromCurrency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$"
   },
   "toCurrency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$"
   },
   "rate": {
    "allOf": [
     {
      "$ref": "#/components/schemas/FxRateValue"
     }
    ],
    "description": "Units of `toCurrency` per one `fromCurrency`. Six decimal places — a two-place rate on a three-place currency loses money on every transaction, quietly.\n"
   },
   "purpose": {
    "$ref": "#/components/schemas/FxRatePurpose"
   },
   "source": {
    "allOf": [
     {
      "$ref": "#/components/schemas/FxRateSource"
     }
    ],
    "readOnly": true
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date-time"
   },
   "effectiveTo": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "A rate change is a new row. The old one is never edited — a transaction posted last Tuesday must still reconcile at last Tuesday's rate.\n"
   },
   "setByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "note": {
    "type": "string",
    "maxLength": 500,
    "nullable": true,
    "description": "Why this rate, and from where. **Required when `source` is `manual`** (decided 28 September, audit R127 (4)); null on a rate `ingestFxRates` fetched."
   },
   "providerReference": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "The provider's own identifier for this quote. **What makes a rate reproducible** — an auditor asking why a payment converted at 3.6725 gets an answer that is checkable against the source rather than a number somebody typed."
   },
   "fetchedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "description": "When the rate was pulled. **Distinct from `effectiveFrom`**, which is when it applies — a rate fetched at 06:00 for a business day starting at 00:00 has two different times and conflating them makes a late feed look like a backdated rate."
   }
  }
 },
 "FxRatePurpose": {
  "type": "string",
  "description": "A venue does not accept dollars at the rate it books an intercompany balance at. Separating them is what stops a spread on the counter appearing as a loss in the accounts.\n",
  "enum": [
   "tender",
   "interEntity",
   "reporting",
   "revaluation"
  ]
 },
 "FxRateSource": {
  "type": "string",
  "description": "**Where the rate came from, and which provider specifically.** `source: provider` said a feed set it and not which one — two tenants on different feeds were indistinguishable in the ledger, and a rate cannot be defended in an audit without naming its origin.\n\n**`uaeCentralBank` is the default for AED pairs.** The UAE Central Bank publishes an official daily rate and it is what a UAE auditor expects to see — a commercial feed is defensible for tender and awkward for statutory reporting.\n\n**`openExchangeRates` and `ecb` are the commercial and reference options.** ECB publishes daily reference rates free and is the usual fallback for non-AED pairs; Open Exchange Rates is the common commercial feed with intraday granularity. **The choice is per purpose, not per platform** — a tender rate wants intraday, a reporting rate wants the official daily close.",
  "enum": [
   "manual",
   "uaeCentralBank",
   "ecb",
   "openExchangeRates",
   "cardScheme",
   "provider"
  ]
 },
 "FxRateValue": {
  "x-ticvai-persistence-column": "numeric(18,6)",
  "type": "string",
  "pattern": "^\\d+(\\.\\d{1,6})?$",
  "description": "**An exchange rate: a decimal string, never a float**, for the reason `Money.amount` is one (naming-and-style 5.1). Up to six decimal places — a two-place rate on a three-place currency loses money on every transaction, quietly — and stored as `numeric(18,6)` so the six places the wire carries survive the database.\n"
 },
 "JournalEntry": {
  "x-ticvai-persistence": "ledger.journal_entry + ledger.journal_line",
  "type": "object",
  "required": [
   "id",
   "entryNumber",
   "fiscalPeriodId",
   "status",
   "source",
   "description",
   "lines",
   "totalDebit",
   "totalCredit",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "entryNumber": {
    "type": "string",
    "readOnly": true,
    "description": "Server-assigned, **in sequence per legal entity per fiscal year** (decided 28 September, audit R191), for example `JE-2026-000123`. Gapless within the legal entity and year: a number is taken when the entry reaches the ledger, not when a draft is saved.\n"
   },
   "fiscalPeriodId": {
    "type": "string",
    "format": "uuid"
   },
   "status": {
    "$ref": "#/components/schemas/JournalStatus"
   },
   "source": {
    "$ref": "#/components/schemas/JournalSource"
   },
   "sourceId": {
    "type": "string",
    "nullable": true,
    "description": "The order, refund or run that generated this entry."
   },
   "description": {
    "type": "string"
   },
   "reference": {
    "type": "string",
    "nullable": true
   },
   "lines": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/JournalLine"
    }
   },
   "totalDebit": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "totalCredit": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "postedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "approvedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "reversalOfEntryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "reversedByEntryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "reversalReason": {
    "type": "string",
    "nullable": true,
    "description": "On a reversal, the `reason` given to `reverseJournalEntry`. Null on every other entry."
   },
   "rejectionReason": {
    "type": "string",
    "nullable": true,
    "description": "The comment from the latest `rejectJournal`, which the preparer reads before resubmitting. Null until an entry is rejected.\n"
   },
   "rejectedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "rejectedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "postedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "JournalLine": {
  "x-ticvai-append-only": "postedAt",
  "type": "object",
  "required": [
   "accountId",
   "debit",
   "credit"
  ],
  "properties": {
   "accountId": {
    "type": "string",
    "format": "uuid"
   },
   "debit": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "credit": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "costCenterId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "description": {
    "type": "string",
    "maxLength": 500
   },
   "postedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true,
    "description": "**Copied from the journal entry when it posts** (ADR-0056), so the line table can be partitioned by month on its own column. Never differs from its entry's."
   }
  }
 },
 "JournalSource": {
  "type": "string",
  "enum": [
   "manual",
   "order",
   "refund",
   "void",
   "shift",
   "recognition",
   "settlement",
   "variance",
   "reversal",
   "writeOff",
   "chargeback"
  ]
 },
 "JournalStatus": {
  "type": "string",
  "enum": [
   "draft",
   "pendingApproval",
   "posted",
   "reversed"
  ]
 },
 "LegalEntity": {
  "x-ticvai-persistence": "ledger.legal_entity",
  "type": "object",
  "description": "Also the `createLegalEntity` body. **`id` and `scopePath` are server-owned** (`readOnly`) and ignored if sent.\n",
  "required": [
   "id",
   "code",
   "name",
   "countryCode",
   "currency",
   "currencyScale",
   "fiscalYearStartMonth"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "code": {
    "type": "string",
    "maxLength": 64
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "countryCode": {
    "type": "string",
    "pattern": "^[A-Z]{2}$"
   },
   "currency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$"
   },
   "currencyScale": {
    "type": "integer",
    "minimum": 0,
    "maximum": 4
   },
   "taxRegistrationNumber": {
    "type": "string",
    "nullable": true
   },
   "fiscalYearStartMonth": {
    "type": "integer",
    "minimum": 1,
    "maximum": 12
   },
   "regionIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "isActive": {
    "type": "boolean"
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"
   }
  }
 },
 "OrderChannel": {
  "type": "string",
  "description": "Where the order originated. Added when guest self-ordering was contracted — an order a guest placed on their own phone is commercially and operationally different from one a cashier typed, and reporting that cannot separate them cannot answer whether self-ordering is working.\n",
  "enum": [
   "pos",
   "kiosk",
   "guestApp",
   "guestWeb",
   "callCentre",
   "partner",
   "api",
   "backOffice"
  ]
 },
 "OrderStatus": {
  "type": "string",
  "enum": [
   "pending",
   "held",
   "paid",
   "partiallyPaid",
   "completed",
   "voided",
   "refunded",
   "partiallyRefunded",
   "failed"
  ],
  "description": "`held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that accumulates parked sales across a shift cannot be closed.\n"
 },
 "OrderSummary": {
  "x-ticvai-persistence": "none — projection",
  "type": "object",
  "required": [
   "id",
   "orderNumber",
   "status",
   "grossAmount",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "orderNumber": {
    "type": "string"
   },
   "status": {
    "$ref": "#/components/schemas/OrderStatus"
   },
   "grossAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "refundedAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "channel": {
    "allOf": [
     {
      "$ref": "#/components/schemas/OrderChannel"
     }
    ],
    "description": "The same vocabulary as `Order.channel`, which this projects."
   },
   "lineCount": {
    "type": "integer"
   },
   "principalId": {
    "type": "string",
    "format": "uuid",
    "description": "The cashier who raised it — what the held-orders list shows."
   },
   "holdLabel": {
    "type": "string",
    "nullable": true,
    "description": "As `Order.holdLabel`."
   },
   "heldUntil": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "As `Order.heldUntil`, so a held-orders list can warn about the ones about to lapse."
   },
   "createdAt": {
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
 "PostingEventType": {
  "type": "string",
  "description": "Every event that generates a ledger posting.\n**How each money event posts** (decided 28 September, audit R191). Card payment `cardReceived`, cash payment `cashReceived`, refund `refundIssued`, a POS offline sync the same events as the payments it replays, dated by when the till recorded them. **Two added on that date**: `gameCreditLoaded`, the liability `wallet.loadGameCredits` creates, and `pointsAccrued`, the liability for loyalty points earned. Every posting goes to the fiscal period open for the event date, through the mapping for its event type, or to suspense where none is mapped.\n**Required before a venue trades**: `cardReceived`, `cashReceived`, `refundIssued` and `priceVariance` (audit R127 (1)).\n",
  "enum": [
   "ticketRevenue",
   "fnbRevenue",
   "retailRevenue",
   "rentalRevenue",
   "taxPayable",
   "cashReceived",
   "cardReceived",
   "walletReceived",
   "refundIssued",
   "voidReversal",
   "deferredRevenue",
   "recognisedRevenue",
   "breakageRevenue",
   "priceVariance",
   "cashOverShort",
   "settlementFee",
   "settlementClearing",
   "gameCreditLoaded",
   "pointsAccrued",
   "chargebackDebit",
   "chargebackReversal",
   "chargebackFee"
  ]
 },
 "PriceVariance": {
  "x-ticvai-persistence": "ledger.price_variance",
  "type": "object",
  "required": [
   "id",
   "orderId",
   "orderLineId",
   "venueId",
   "quotedPrice",
   "serverPrice",
   "variance",
   "isException",
   "occurredAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "orderId": {
    "type": "string",
    "format": "uuid"
   },
   "orderLineId": {
    "type": "string"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "variantId": {
    "type": "string",
    "format": "uuid"
   },
   "quotedPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "serverPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "variance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "catalogueBundleVersion": {
    "type": "string",
    "nullable": true,
    "description": "The bundle the terminal priced from. Turns \"the price was wrong\" into \"the terminal was two bundles behind\", which is actionable.\n"
   },
   "isException": {
    "type": "boolean",
    "description": "Above the venue's configured variance threshold."
   },
   "reviewStatus": {
    "$ref": "#/components/schemas/VarianceReviewStatus"
   },
   "reviewOutcome": {
    "type": "string",
    "nullable": true,
    "description": "The `outcome` given to `reviewPriceVariance`. Null until reviewed.",
    "enum": [
     "accepted",
     "investigated",
     "catalogueCorrected"
    ]
   },
   "reviewedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "journalEntryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "occurredAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "ProductKind": {
  "type": "string",
  "description": "**`openDated` added 24 August** from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no kind: **valid on any date within an eligible range, rather than for a named performance or a fixed date.**\nThe mechanism already existed — `access.entitlement` carries `valid_from`, `valid_to`, `entries_allowed` and `frozen_days`, which is exactly an open-dated pass. **What was missing was the product saying it is one**, so a catalogue could not offer it and a report could not count it.\n**`datedAdmission` is a different thing and the two were being conflated**: dated is *this Tuesday*, open-dated is *any Tuesday between March and June*. A guest buying the second and being sold the first has bought the wrong ticket.\n**Transport uses two existing kinds, not a new one** (decided 29 September, rev 3 REV3-21). A one-way trip is `timedAdmission`: `transport.createTransportRoute` creates the route's product with one variant per passenger type, and each departure is a performance. A multi-trip or unlimited pass is `openDated`: `transport.createTransportPassType` creates it, with `EntitlementTemplate.entriesAllowed` = the pass's trips (null for unlimited), the validity = `validityDays`, and `EntitlementTemplate.transportRestriction` naming the station pair the pass was bought for, so `access` refuses it on another journey. The sale path is unchanged: both are cart lines, priced by `transport.quoteTransportFare` (orders `TransportLineAttributes`).\n",
  "enum": [
   "admission",
   "timedAdmission",
   "datedAdmission",
   "openDated",
   "seated",
   "membership",
   "bundle",
   "fnb",
   "retail",
   "rental",
   "addOn",
   "giftCard"
  ]
 },
 "RecognitionMethod": {
  "type": "string",
  "enum": [
   "immediate",
   "onRedemption",
   "straightLine",
   "perVisit",
   "onExpiry"
  ]
 },
 "RecognitionRunResult": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "fiscalPeriodId",
   "dryRun",
   "recognisedTotal",
   "breakageTotal",
   "entryCount"
  ],
  "properties": {
   "fiscalPeriodId": {
    "type": "string",
    "format": "uuid"
   },
   "dryRun": {
    "type": "boolean"
   },
   "recognisedTotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "breakageTotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "entryCount": {
    "type": "integer"
   },
   "byMethod": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "method": {
       "$ref": "#/components/schemas/RecognitionMethod"
      },
      "amount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "itemCount": {
       "type": "integer"
      }
     }
    }
   },
   "journalEntryIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   }
  }
 },
 "RecognitionSchedule": {
  "x-ticvai-persistence": "ledger.recognition_schedule",
  "type": "object",
  "description": "Also the `createRecognitionSchedule` body. **`id` is server-owned** (`readOnly`): a client does not send it, and one sent is ignored.\n",
  "required": [
   "id",
   "name",
   "method",
   "productKinds"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "method": {
    "$ref": "#/components/schemas/RecognitionMethod"
   },
   "priority": {
    "type": "integer",
    "default": 100,
    "description": "**Two schedules may both claim a product kind and nothing resolved which wins** — a silent double-recognition, which is the worst kind of accounting defect because the numbers look plausible.\nLowest priority wins, and **two schedules at the same priority claiming the same kind is refused at save** rather than resolved at run time.\n"
   },
   "recognitionSite": {
    "type": "string",
    "enum": [
     "sale",
     "admission",
     "consumption"
    ],
    "default": "sale",
    "description": "**Where revenue is earned, which is not always where it was sold.** A ticket sold at one venue and admitted at another earns at the gate, and recognising at the sale site puts the revenue in the wrong entity's books.\n`consumption` is for stored value — a wallet top-up is not revenue until it is spent.\n"
   },
   "frequency": {
    "type": "string",
    "enum": [
     "daily",
     "weekly",
     "monthly",
     "onEvent",
     "onPeriodClose"
    ],
    "default": "onPeriodClose",
    "description": "**Driven by the schedule rather than by whoever runs the job.** Recognition that happens when somebody remembers is recognition with no cut-off.\n"
   },
   "revalidateOnValidityChange": {
    "type": "boolean",
    "default": true,
    "description": "**Changing an entitlement's validity did not re-time its deferred balance.** A pass extended by three months has three more months of deferral, and a schedule that ignores that recognises revenue the venue has not yet earned.\n"
   },
   "productKinds": {
    "type": "array",
    "minItems": 1,
    "description": "The product kinds this schedule claims, from the catalogue's `ProductKind`.",
    "items": {
     "type": "string",
     "allOf": [
      {
       "$ref": "../spine/catalogue.yaml#/components/schemas/ProductKind"
      }
     ]
    }
   },
   "deferredAccountId": {
    "type": "string",
    "format": "uuid"
   },
   "recognisedAccountId": {
    "type": "string",
    "format": "uuid"
   },
   "breakageAccountId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "noShowTrigger": {
    "type": "string",
    "nullable": true,
    "enum": [
     "performanceEnd",
     "validityEnd",
     "none"
    ],
    "description": "8.1.1. **A no-show is breakage with a known moment**, and the mechanism already existed — `breakageAfterDays` moves deferred revenue to earned after a period. A ticket for a performance that has finished does not need a waiting period: **the guest cannot arrive any more.**\n`performanceEnd` recognises when the performance completes. `validityEnd` recognises when an open-dated entitlement lapses, which is where `breakageAfterDays` still applies.\n**`none` keeps the current behaviour** — recognise on the schedule and nothing else — so no existing schedule changes.\n"
   },
   "noShowAccountId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Where no-show revenue lands. **Separate from `recognisedAccountId` by default**, because revenue from a guest who came and revenue from one who did not are different lines to whoever reads the P&L — and 8.1.2 asks for a report on exactly that distinction.\n"
   },
   "breakageAfterDays": {
    "type": "integer",
    "nullable": true,
    "description": "Days after expiry at which unredeemed value becomes breakage."
   },
   "isActive": {
    "type": "boolean"
   }
  }
 },
 "Settlement": {
  "x-ticvai-persistence": "ledger.settlement",
  "type": "object",
  "required": [
   "id",
   "providerName",
   "periodStart",
   "periodEnd",
   "status",
   "ingestedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "currencyCode": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "description": "**A settlement has no account, so nothing else denominates it.** A posting takes its currency from `ledger.account.currency` and a payment from `tenderCurrency`, but a settlement is a provider file for a period: `providerGross`, `ledgerGross` and `difference` are bare amounts, and a provider file in one currency against a ledger in another computes a difference that means nothing. Added 20 September, when a venue became able to trade outside its region's currency.\n"
   },
   "providerName": {
    "type": "string"
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "description": "The venue this settlement is for. **Reconciled daily per venue** (decided 28 September, audit R110 (b)), so `periodStart` and `periodEnd` are the same day."
   },
   "periodStart": {
    "type": "string",
    "format": "date",
    "description": "A day in the region's time zone, local midnight to local midnight."
   },
   "periodEnd": {
    "type": "string",
    "format": "date",
    "description": "A day in the region's time zone, local midnight to local midnight."
   },
   "fileReference": {
    "type": "string",
    "format": "uuid",
    "description": "The `MediaAsset` holding the provider file, as given to `ingestSettlementFile`. **Kept on the row because parsing is asynchronous**: the job that parses the file reads it from here.\n"
   },
   "format": {
    "type": "string",
    "nullable": true,
    "enum": [
     "csv",
     "fixedWidth",
     "xml",
     "json"
    ],
    "description": "The file format given at ingest. Null when none was given."
   },
   "status": {
    "$ref": "#/components/schemas/SettlementStatus"
   },
   "lineCount": {
    "type": "integer"
   },
   "matchedCount": {
    "type": "integer"
   },
   "exceptionCount": {
    "type": "integer"
   },
   "providerGross": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "providerFees": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "providerNet": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "ledgerGross": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "difference": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "ingestedAt": {
    "type": "string",
    "format": "date-time"
   },
   "completedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `region` scope.**"
   }
  }
 },
 "SettlementStatus": {
  "type": "string",
  "enum": [
   "ingesting",
   "parsing",
   "matching",
   "matched",
   "hasExceptions",
   "resolved",
   "failed"
  ]
 },
 "TaxCode": {
  "x-ticvai-persistence": "ledger.tax_code",
  "type": "object",
  "required": [
   "id",
   "code",
   "name",
   "countryCode",
   "rate",
   "effectiveFrom",
   "isActive"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "code": {
    "type": "string",
    "maxLength": 64
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "countryCode": {
    "type": "string",
    "pattern": "^[A-Z]{2}$"
   },
   "appliesTo": {
    "type": "array",
    "description": "**What this code covers, and `donation` is why the field exists** (CF-84). Donation tax treatment varies by jurisdiction — **0% is a valid rate, not an absence of one** — and it is set here rather than assumed in the posting.\nThe liability-account posting stays the default and is no longer the only option.\n",
    "items": {
     "type": "string",
     "enum": [
      "goods",
      "services",
      "admission",
      "food",
      "accommodation",
      "donation",
      "gratuity",
      "fee"
     ]
    }
   },
   "rate": {
    "type": "number",
    "minimum": 0,
    "maximum": 100
   },
   "compoundOnTaxCodeId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "When set, this tax applies to the base **plus** the referenced tax, not to the base alone. Ordering is explicit rather than implied.\n"
   },
   "isInclusive": {
    "type": "boolean",
    "description": "True when the displayed price already contains this tax."
   },
   "accountId": {
    "type": "string",
    "format": "uuid"
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date",
    "description": "A day in the region's time zone, local midnight to local midnight."
   },
   "effectiveTo": {
    "type": "string",
    "format": "date",
    "description": "A day in the region's time zone, local midnight to local midnight.",
    "nullable": true
   },
   "isActive": {
    "type": "boolean"
   }
  }
 },
 "TaxExemption": {
  "x-ticvai-persistence": "ledger.tax_exemption",
  "type": "object",
  "description": "Also the `createTaxExemption` body. **`id` is server-owned** (`readOnly`): a client does not send it, and one sent is ignored. OpenAPI 3.1: a `readOnly` property in `required` is required in responses only.\n",
  "required": [
   "id",
   "scope",
   "taxCodeId",
   "reason"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "scope": {
    "type": "string",
    "enum": [
     "account",
     "productKind",
     "channel",
     "legalEntity"
    ]
   },
   "scopeRef": {
    "type": "string",
    "description": "Identifier of the exempt subject, matching `scope`."
   },
   "taxCodeId": {
    "type": "string",
    "format": "uuid"
   },
   "reason": {
    "type": "string",
    "maxLength": 500
   },
   "exemptionType": {
    "type": "string",
    "enum": [
     "diplomatic",
     "export",
     "businessToBusiness",
     "charity",
     "governmentEntity",
     "freeZone",
     "zeroRated",
     "other"
    ],
    "description": "Tax Exemption Evidence: exemption type (pack 'Pricing___Revenue_Management_Reference.pdf' p.47). Moved here from catalogue `listFeeWaiverTax`, whose rule now only says `evidenceRequired` (decided 29 September, readiness close-out). Which types a jurisdiction recognises is the client's tax configuration; the list names the kinds, it does not grant any. **Proposed values: tax configuration per jurisdiction, client to correct.**"
   },
   "certificateReference": {
    "type": "string",
    "maxLength": 100,
    "nullable": true,
    "description": "Tax Exemption Evidence: reference, e.g. the exemption certificate, diplomatic card or export declaration number."
   },
   "evidenceDocumentId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Tax Exemption Evidence: the uploaded document (certificate scan, declaration). Kept for the retention period of the postings it exempted, not of the exemption."
   },
   "verificationStatus": {
    "type": "string",
    "enum": [
     "notRequired",
     "pending",
     "verified",
     "rejected",
     "expired"
    ],
    "default": "pending",
    "description": "Tax Exemption Evidence: verification status. **Only `verified` and `notRequired` exempt a line**; `calculateTax` treats `pending`, `rejected` and `expired` as no exemption and records the exemption id on the line so the refusal is explainable. `expired` is set by the server once `validTo` has passed; evidence checked after the grant is recorded with `verifyTaxExemption`. The granter sends `verified` on `createTaxExemption` when the evidence was checked at the grant; `verifiedBy` and `verifiedAt` are then set from the caller."
   },
   "verifiedBy": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true
   },
   "verifiedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "verificationNote": {
    "type": "string",
    "maxLength": 500,
    "nullable": true,
    "readOnly": true,
    "description": "The `note` given to `verifyTaxExemption`; required when evidence was rejected."
   },
   "validFrom": {
    "type": "string",
    "format": "date",
    "description": "Tax Exemption Evidence: validity, first day. A day in the region's time zone, local midnight to local midnight."
   },
   "validTo": {
    "type": "string",
    "format": "date",
    "description": "Tax Exemption Evidence: validity, last day. A day in the region's time zone, local midnight to local midnight.",
    "nullable": true
   }
  }
 },
 "TrialBalance": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "fiscalPeriodId",
   "isBalanced",
   "totalDebit",
   "totalCredit",
   "accounts"
  ],
  "properties": {
   "fiscalPeriodId": {
    "type": "string",
    "format": "uuid"
   },
   "isBalanced": {
    "type": "boolean",
    "description": "False indicates a defect, not a business condition. Double-entry cannot be unbalanced by legitimate activity.\n"
   },
   "totalDebit": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "totalCredit": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "accounts": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "accountId",
      "accountCode",
      "accountName",
      "debit",
      "credit",
      "balance"
     ],
     "properties": {
      "accountId": {
       "type": "string",
       "format": "uuid"
      },
      "accountCode": {
       "type": "string"
      },
      "accountName": {
       "type": "string"
      },
      "type": {
       "$ref": "#/components/schemas/AccountType"
      },
      "debit": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "credit": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "balance": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      }
     }
    }
   }
  }
 },
 "VarianceReviewStatus": {
  "type": "string",
  "enum": [
   "notRequired",
   "pendingReview",
   "reviewed"
  ]
 },
 "VenueSettings": {
  "type": "object",
  "x-ticvai-persistence": "platform.venue_settings",
  "description": "**Venue-level operational configuration that no other level can answer.**\nRegion owns currency, tax regime and fiscal year (ADR-0011). Venue owns the things that vary between two venues in one region — **opening hours, support hours, and what the local law requires of the gate.**\n**And the configured limits** (decided 28 September, audit R094): every limit the contracts call *configured* is a field here, from `displayCurrencies` and `cartLeaseSeconds` down to the grouped `catalogue`, `inventory`, `seating`, `promotions`, `fnb`, `queue`, `reporting`, `marketing` and `identity` settings. **Each has a tenant-level default**: the tenant sets it once with `setVenueSettingsDefaults`, a venue overrides it within the field's bounds, and a null field here inherits it. Each field's `default` is the proposed tenant default, marked proposed, client to correct (audit R094); `docs/active/configured-limits-proposal.md` is the sheet the client corrects, and where the two differ this contract is what runs.\n",
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
    "description": "From the path of `setVenueSettings`."
   },
   "calendarDayStartHour": {
    "type": "integer",
    "minimum": 0,
    "maximum": 23,
    "nullable": true,
    "default": 6,
    "description": "**Where the venue's calendar day starts** (17 September minutes M17-03, added 30 September): the first hour row of every day and week calendar view (`calendarView` in `screens/_components.yaml`), so a venue open 06:00 to 02:00 sees its night on the day it belongs to. Display only: it moves no booking, slot or business date. Null inherits the tenant default (proposed 6, client to correct).\n"
   },
   "currencyCode": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "nullable": true,
    "readOnly": true,
    "description": "**`readOnly` is the freeze.** `setVenueSettings` takes this whole schema as its request body, so without it any settings save could rewrite the currency of a venue that had already traded — which is the one thing ADR-0018's amendment forbids. It is set when the venue is provisioned, defaulted from the region, and changed only by an operation whose precondition is that the venue has not yet traded.\n**The venue's trading currency, defaulted from its region and frozen once the venue has traded** (ADR-0018, amended 20 September). Currency was a region-only fact, grouped with tax rates on the reasoning that *\"a venue cannot choose its VAT\"* -- true of tax and over-applied to currency, because a free-zone unit, a duty-free shop and a cruise terminal genuinely trade in a currency their region does not.\n**This column exists because the freeze needs somewhere to live.** A venue that resolved purely from its region would silently follow a region currency change after it had already traded, and every dated artefact beneath it -- a price list is a `validFrom`/`validTo` range -- would render retrospectively wrong. Null means \"resolve from the region\", which is the answer for every venue that has not overridden.\n"
   },
   "currencyScale": {
    "type": "integer",
    "minimum": 0,
    "maximum": 4,
    "nullable": true,
    "readOnly": true,
    "description": "**Scale travels with currency** (ADR-0008), and so does the freeze. OMR is three decimal places because Oman says so; overriding the currency without the scale gets rounding wrong. Set together or not at all.\n"
   },
   "supportHours": {
    "type": "object",
    "description": "CF-100. **A venue decides whether its support desk is 24/7 or bounded, and the platform does not.** This was recorded as an open question for eleven days and was never one — the code is identical either way, and what was missing was somewhere to put the answer.\n",
    "properties": {
     "mode": {
      "type": "string",
      "enum": [
       "alwaysOn",
       "businessHours",
       "custom",
       "none"
      ]
     },
     "timezone": {
      "type": "string",
      "description": "IANA zone the `windows` are read in. Absent, they are read in the region's `timeZone`, like every other wall-clock time in this contract.\n"
     },
     "windows": {
      "type": "array",
      "items": {
       "type": "object",
       "properties": {
        "day": {
         "type": "string",
         "enum": [
          "mon",
          "tue",
          "wed",
          "thu",
          "fri",
          "sat",
          "sun"
         ]
        },
        "from": {
         "type": "string",
         "description": "Wall-clock time the desk opens."
        },
        "to": {
         "type": "string",
         "description": "Wall-clock time the desk closes."
        }
       }
      }
     },
     "outOfHoursMessage": {
      "type": "string",
      "nullable": true
     }
    }
   },
   "quietHours": {
    "type": "object",
    "nullable": true,
    "description": "**When the platform does not send.** A wallet low-balance alert at 3am is a complaint, and journeys and message triggers both respect this.\n**Operational messages ignore it** — a queue-turn alert is why a guest is holding the phone.\n",
    "properties": {
     "from": {
      "type": "string",
      "description": "Wall-clock time sending stops",
      "in the region's time zone.": null
     },
     "to": {
      "type": "string",
      "description": "Wall-clock time sending resumes",
      "in the region's time zone.": null
     }
    }
   },
   "biometrics": {
    "type": "object",
    "nullable": true,
    "description": "CF-35, BL-096, BL-105, BL-106. **The venue-level master switch, and the one place a person is asked whether the paperwork exists.** Biometric data is sensitive under PDPL (Federal Decree-Law 45/2021) — heightened protection, explicit consent, and an Article 21 assessment before the processing rather than after it.\n**Nothing below this switch operates while it is off.** `AdmissionRules` may carry a `biometricPolicy` per ticket type and those rules are inert until a venue enables biometrics here, which means a profile copied between venues cannot start capturing faces at the destination.\n**Venue level because that is where the assessment is filed.** Region owns tax and currency; the DPIA, the consent notice and the hardware are a venue's.\n",
    "properties": {
     "isEnabled": {
      "type": "boolean",
      "default": false,
      "description": "**Off by default, and turning it on is refused without the two fields below.** `setVenueSettings` answers 422 rather than accepting an enable it cannot evidence — **a DPIA nobody can name is a DPIA nobody did**, and the point of the refusal is that the person switching this on is asked at the moment they switch it on rather than by an auditor a year later.\n"
     },
     "dpiaReference": {
      "type": "string",
      "nullable": true,
      "maxLength": 200,
      "description": "**The venue's own reference for its Article 21 assessment.** The platform does not hold the document and does not judge it; it records that one was named, by whom, and when — which is what an audit asks for and what the venue can produce.\n"
     },
     "consentNoticeAcknowledgedAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true,
      "description": "**When somebody confirmed the consent forms are in place at the point of capture.** A guest consenting in an app is a record; a guest consenting at a ticket counter is a notice somebody has to have printed and a question somebody has to have asked.\n"
     },
     "acknowledgedByPrincipalId": {
      "type": "string",
      "format": "uuid",
      "nullable": true,
      "readOnly": true,
      "description": "**Who confirmed it.** An acknowledgement with no name behind it cannot be followed up, and this is the field that makes the switch an act rather than a setting. Recorded by the server as the caller whose save carried the acknowledgement, so it cannot name somebody else.\n"
     },
     "faceTagPurgeMinutesAfterClose": {
      "type": "integer",
      "nullable": true,
      "default": 0,
      "description": "BL-106. **How long a same-visit Face Tag survives past the close of the operating day**, and zero is the default because that is what 3.2.44 describes. A non-zero value is an operational allowance for a late reconciliation, not a retention period — **`facePass` ignores this entirely** and is bounded by its entitlement.\n"
     }
    }
   },
   "segregatedAccess": {
    "type": "object",
    "nullable": true,
    "description": "CF-130. **Configured at venue level because it changes by region and the venue is where it is known** — a Ladies Night, a family session, a prayer-time closure.\n**The platform does not infer gender.** 3.2.45 asks for automatic gender recognition and 3.2.46 for rule-based facial recognition validation, and neither is built. Two reasons, and the second is the one that decided it:\n**A Ladies Night ticket is already gendered at the point of sale**, so the gate checks the entitlement the platform issued rather than the face in front of it — deterministic, auditable, and already contracted through `admissionRules`.\n**And these events are staffed.** A steward at the entrance is making the judgment anyway, and a classifier that overrules a person who can see more than it can is a machine and a human disagreeing while a guest waits.\n**`genderVerification` is a switch, not an implementation.** Where a venue's access hardware offers the capability and the venue chooses to use it, this turns it on — following ADR-0015's standards-first driver model, where the device does what the device does. **Not everything needs to be built.**\n",
    "properties": {
     "isEnabled": {
      "type": "boolean",
      "default": false
     },
     "appliesToAccessPointIds": {
      "type": "array",
      "items": {
       "type": "string",
       "format": "uuid"
      }
     },
     "schedule": {
      "type": "array",
      "items": {
       "type": "object",
       "properties": {
        "day": {
         "type": "string",
         "enum": [
          "mon",
          "tue",
          "wed",
          "thu",
          "fri",
          "sat",
          "sun"
         ]
        },
        "from": {
         "type": "string",
         "description": "Wall-clock time",
         "in the region's time zone.": null
        },
        "to": {
         "type": "string",
         "description": "Wall-clock time",
         "in the region's time zone.": null
        },
        "admits": {
         "type": "string",
         "enum": [
          "all",
          "women",
          "womenAndChildren",
          "families",
          "members"
         ]
        }
       }
      }
     },
     "entitlementGated": {
      "type": "boolean",
      "default": true,
      "readOnly": true,
      "description": "**Always true, and stated rather than assumed.** The gate admits on the entitlement. Everything below is advisory on top of that, and nothing replaces it.\n"
     },
     "genderVerification": {
      "type": "string",
      "enum": [
       "off",
       "staffAssisted",
       "deviceAssisted"
      ],
      "default": "off",
      "description": "`off` — the entitlement decides and a steward handles exceptions. **The default, and what is contracted.**\n`staffAssisted` — the steward's screen shows the ticket type so they can ask. No inference anywhere.\n`deviceAssisted` — **the venue's access hardware performs the check, not the platform.** Available only where the driver reports the capability, and the result is **advisory to the steward rather than decisive at the turnstile** (3.2.45 asks for rejection; this deviates deliberately).\n"
     },
     "overrideRateAlertThreshold": {
      "type": "number",
      "nullable": true,
      "description": "Where `deviceAssisted` is on. **An override rate near zero means the steward has stopped deciding**, and that is the number that says whether the human safeguard is working or decorative.\n"
     }
    }
   },
   "alerting": {
    "type": "object",
    "description": "CF-134. **On-platform notification, marked as read.** Six contracts detect their own trouble and none told a person.\n**The panel is the default and email or WhatsApp only where the matrix names them** — an operational alert that arrives by email is an alert nobody sees in time.\n",
    "properties": {
     "channel": {
      "type": "string",
      "enum": [
       "dashboardPanel",
       "dashboardAndEmail",
       "dashboardAndWhatsapp"
      ],
      "default": "dashboardPanel"
     },
     "acknowledgementRequired": {
      "type": "boolean",
      "default": true
     },
     "escalateAfterMinutes": {
      "type": "integer",
      "nullable": true
     }
    }
   },
   "displayCurrencies": {
    "type": "array",
    "nullable": true,
    "description": "**Which currencies this venue shows guests** (decided 28 September, audit R120 (a)). ISO 4217 codes, each one its region holds an `FxRate` for; the rate itself stays per region and is never set here. `finance.listFxRates` with `venueId` narrows the region's rates to these. Null or empty shows the trading currency only. A code the region has no rate for is refused `400`.\n",
    "items": {
     "type": "string",
     "pattern": "^[A-Z]{3}$"
    }
   },
   "cartLeaseSeconds": {
    "type": "integer",
    "nullable": true,
    "minimum": 30,
    "maximum": 3600,
    "default": 900,
    "description": "**How long a cart holds capacity** (decided 28 September, audit R169): 15 minutes, the default `catalogue.acquireInventoryHold` takes for `ttlSeconds`. Proposed, client to correct (audit R094).\n"
   },
   "cartHoldExtensionMinutes": {
    "type": "integer",
    "nullable": true,
    "minimum": 1,
    "maximum": 30,
    "default": 5,
    "description": "How long one `orders.extendCart` extension adds. Proposed, client to correct (audit R094)."
   },
   "cartMaxExtensions": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "maximum": 5,
    "default": 1,
    "description": "How many extensions a cart may take before `extensionCapReached` (`Cart.maxExtensions`). Proposed, client to correct (audit R094)."
   },
   "resaleCutoffHours": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "maximum": 168,
    "default": 24,
    "description": "Hours before the performance after which a ticket can no longer be listed for resale (`orders.createResaleListing`). Proposed, client to correct (audit R094)."
   },
   "exchangeCutoffHours": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "maximum": 720,
    "default": 24,
    "description": "Hours before the original performance after which lines can no longer be exchanged (`orders.exchangeOrderLines`, `outsideExchangeWindow`). Proposed, client to correct (audit R094)."
   },
   "rescheduleCutoffHours": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "maximum": 720,
    "default": 24,
    "description": "Hours before the original performance after which an order can no longer be rescheduled (`orders.rescheduleOrder`, `outsideRescheduleWindow`). Proposed, client to correct (audit R094)."
   },
   "reservationMaxExtensions": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "maximum": 5,
    "default": 1,
    "description": "How many times `orders.extendReservation` may extend one reservation. Proposed, client to correct (audit R094)."
   },
   "shiftVarianceThreshold": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "Over or short at shift close beyond which the shift waits in `pendingVariance` for `shift.acceptShiftVariance`. **Proposed tenant default AED 20.00, bounds 0 to 1,000 in the venue currency; client finance to correct (audit R094).**\n"
   },
   "catalogue": {
    "type": "object",
    "nullable": true,
    "properties": {
     "maxVariantsPerProduct": {
      "type": "integer",
      "nullable": true,
      "minimum": 1,
      "maximum": 2000,
      "default": 200,
      "description": "Variants one product may generate from its attributes (`setProductAttributes` refuses above it). Proposed, client to correct (audit R094)."
     },
     "waitlistOfferHoldMinutes": {
      "type": "integer",
      "nullable": true,
      "minimum": 1,
      "maximum": 1440,
      "default": 30,
      "description": "How long a waitlist offer holds the released capacity for the guest it was offered to. Proposed, client to correct (audit R094)."
     },
     "bulkPriceChangeEscalationPercent": {
      "type": "number",
      "nullable": true,
      "minimum": 0,
      "maximum": 100,
      "default": 10,
      "description": "A `bulkChangePrices` run changing any price by more than this percentage needs `PRICE_CONFIGURE` (audit R197). Proposed, client to correct (audit R094)."
     },
     "bulkPriceChangeEscalationCount": {
      "type": "integer",
      "nullable": true,
      "minimum": 1,
      "default": 50,
      "description": "A `bulkChangePrices` run touching more prices than this needs `PRICE_CONFIGURE` (audit R197). Proposed, client to correct (audit R094)."
     }
    }
   },
   "inventory": {
    "type": "object",
    "nullable": true,
    "properties": {
     "overReceiptTolerancePercent": {
      "type": "number",
      "nullable": true,
      "minimum": 0,
      "maximum": 25,
      "default": 5,
      "description": "Percent above the outstanding ordered quantity a goods receipt line may record (`createGoodsReceipt`). Proposed, client to correct (audit R094)."
     },
     "countVarianceTolerancePercent": {
      "type": "number",
      "nullable": true,
      "minimum": 0,
      "maximum": 25,
      "default": 2,
      "description": "Percent difference between counted and expected quantity before a count line is an exception (`getCountVariance`). Proposed, client to correct (audit R094)."
     },
     "countVarianceApprovalAmount": {
      "allOf": [
       {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      ],
      "nullable": true,
      "description": "Total variance value of a count above which posting it needs approval (`postStockCount`). **Proposed tenant default 1,000.00 in the venue currency, client finance to correct (audit R094).**\n"
     }
    }
   },
   "seating": {
    "type": "object",
    "nullable": true,
    "properties": {
     "seatHoldExtensionSeconds": {
      "type": "integer",
      "nullable": true,
      "minimum": 60,
      "maximum": 1800,
      "default": 300,
      "description": "What one `extendSeatHold` adds. No hold outlives 30 minutes in all (audit R169). Proposed, client to correct (audit R094)."
     },
     "seatHoldMaxExtensions": {
      "type": "integer",
      "nullable": true,
      "minimum": 0,
      "maximum": 5,
      "default": 2,
      "description": "How many times a seat hold may be extended. Proposed, client to correct (audit R094). A resource hold on a venue map (`resources.extendResourceHold`) uses the same two bounds (decided 29 September, rev 3 REV3-15)."
     },
     "maxSeatsPerGuestOrder": {
      "type": "integer",
      "nullable": true,
      "minimum": 1,
      "maximum": 50,
      "default": 10,
      "description": "**Seats one guest may take in one booking on a guest channel** (Guest Web, Guest App), decided 29 September, rev 3 REV3-7. `seating.createSeatHold` counts the seats in the request plus the seats the same guest already holds on the same performance, and refuses above this with `422` `seat-limit-exceeded`, naming the limit. Default 10, bounds 1 to 50; a venue sets its own in Venue Management. Staff and POS sales keep 10 per sale (audit R080 (c)) and do not read this field.\n"
     }
    }
   },
   "promotions": {
    "type": "object",
    "nullable": true,
    "properties": {
     "maxDiscountPercent": {
      "type": "number",
      "nullable": true,
      "minimum": 0,
      "maximum": 100,
      "default": 30,
      "description": "The largest discount one promotion may give (`createPromotion` refuses above it). Proposed, client to correct (audit R094)."
     },
     "nearZeroLinePrice": {
      "allOf": [
       {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      ],
      "nullable": true,
      "description": "Net line price below which a stacked combination is flagged near-zero in `analysePromotionConflicts` (audit R096 (5)); a warning, not a refusal. **Proposed tenant default AED 1.00, client to correct (audit R094).**\n"
     }
    }
   },
   "fnb": {
    "type": "object",
    "nullable": true,
    "properties": {
     "recallWindowMinutes": {
      "type": "integer",
      "nullable": true,
      "minimum": 0,
      "maximum": 60,
      "default": 10,
      "description": "Minutes after a bump during which `recallKitchenTicket` still recalls; after it the act is a refire. Proposed, client to correct (audit R094)."
     },
     "compEscalationAmount": {
      "allOf": [
       {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      ],
      "nullable": true,
      "description": "Line value above which `compItem` needs `ORDER_DISCOUNT` (audit R197). **Proposed tenant default AED 100.00, client to correct (audit R094).**\n"
     },
     "foodSafetyLeadPrincipalId": {
      "type": "string",
      "format": "uuid",
      "nullable": true,
      "description": "**The venue's food-safety lead**, to whom `escalateCorrectiveAction` sends every escalation (decided 28 September, audit R096 (9)). A venue fact, so it has no tenant default; while it is null an escalation is refused `409 no-food-safety-lead`.\n"
     }
    }
   },
   "queue": {
    "type": "object",
    "nullable": true,
    "properties": {
     "crossQueueLimit": {
      "type": "integer",
      "nullable": true,
      "minimum": 1,
      "maximum": 10,
      "default": 2,
      "description": "Virtual queues one guest party may wait in at once (`joinQueue`, `crossQueueLimitReached`). Proposed, client to correct (audit R094)."
     }
    }
   },
   "reporting": {
    "type": "object",
    "nullable": true,
    "properties": {
     "inlineRunRowLimit": {
      "type": "integer",
      "nullable": true,
      "minimum": 1000,
      "maximum": 100000,
      "default": 5000,
      "description": "Estimated rows above which `runReport` answers `202` and runs in the background. Proposed, client to correct (audit R094)."
     },
     "dashboardRefreshBudgetPerMinute": {
      "type": "integer",
      "nullable": true,
      "minimum": 1,
      "default": 24,
      "description": "Tile refreshes per minute, summed over a dashboard's tiles, that `createDashboard` allows. Proposed, client to correct (audit R094)."
     }
    }
   },
   "marketing": {
    "type": "object",
    "nullable": true,
    "properties": {
     "attributionWindowDays": {
      "type": "integer",
      "nullable": true,
      "minimum": 1,
      "maximum": 30,
      "default": 7,
      "description": "Days after a campaign touch within which a booking is attributed to it (`getCampaignPerformance`). Proposed, client to correct (audit R094)."
     }
    }
   },
   "identity": {
    "type": "object",
    "nullable": true,
    "properties": {
     "guestOtpMaxAttempts": {
      "type": "integer",
      "nullable": true,
      "minimum": 3,
      "maximum": 10,
      "default": 5,
      "description": "Wrong entries allowed per guest one-time code before `verifyGuestOtp` invalidates it. A guest code is tenant-scoped, so the tenant default is the value used. Proposed, client to correct (audit R094).\n"
     },
     "guestTwoStep": {
      "type": "object",
      "nullable": true,
      "description": "**Guest two-step verification: a venue option, off unless the venue enables it in Venue Management** (decided 29 September, rev 3 GAP-B1, per venue, superseding the second part of audit R167, \"no guest MFA\"; an earlier draft of the same day put it on the tenant's `PasswordPolicy`, which no longer carries it). **The guest's enrolment stays tenant-wide**: one guest account across the tenant's venues, so a method enrolled once is used in every venue that has this on, and is never asked in a venue that has it off. Identity learns the venue from `venueId` on the guest sign-in (`verifyGuestOtp`, `guestPasswordLogin`, `guestSocialLogin`, `guestUaePassLogin`) and on `createMfaChallenge`: the venue the guest app or booking is in; with no venue given, an enrolled guest is asked when any venue of the tenant has it on. Guests may enrol `totp` with `emailOtp` as the fallback, as staff do (audit R126 (5)); it is never forced. Guests still never use enterprise SSO (R167, first part). A null inherits the tenant default set with `setVenueSettingsDefaults`.\n",
      "properties": {
       "enabled": {
        "type": "boolean",
        "default": false,
        "description": "Off unless the venue enables it. While no venue of the tenant has it on, guests cannot enrol (`enrolMfaMethod` answers 403 `guest-two-step-disabled`)."
       },
       "stepUpActions": {
        "type": "array",
        "uniqueItems": true,
        "description": "The guest actions in this venue that ask an enrolled guest for the factor again, whatever the age of the session. The service performing the action passes this venue to `createMfaChallenge`. Proposed, client to correct (rev 3 GAP-B1).\n",
        "items": {
         "type": "string",
         "enum": [
          "changeContactDetails",
          "changePassword",
          "managePaymentMethods",
          "transferTickets",
          "deleteAccount"
         ]
        },
        "default": [
         "changeContactDetails",
         "changePassword",
         "managePaymentMethods",
         "deleteAccount"
        ]
       }
      }
     }
    }
   }
  }
 }
}
```
