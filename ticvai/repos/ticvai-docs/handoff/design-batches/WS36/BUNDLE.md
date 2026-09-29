# WS36 — Pricing   Revenue Management board 3

**10 screens · 21 operations · 31 schemas · 6 permissions**

Platform P09 TICVAI Web · ships as **ticvai-control** ·
platformAdmin audience · web ·
online only

## Who this is for

**platformAdmin on web.** Everything below is how you know what is
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
  `LEDGER_POST, LEDGER_VIEW, PRICE_CONFIGURE, PRODUCT_CONFIGURE, PRODUCT_VIEW, TAX_CONFIGURE`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-068` | Tax, Fee & Calculation Command Center | listDetail | 3 | 0 | — |
| `ADM-069` | Tax Profile & Jurisdiction Configuration | configEditor | 5 | 0 | — |
| `ADM-070` | Tax Rule & Treatment Builder | listDetail | 1 | 0 | — |
| `ADM-071` | Fee & Surcharge Library | configEditor | 2 | 1 | — |
| `ADM-072` | Fee Applicability & Charging Rule Builder | configEditor | 1 | 0 | — |
| `ADM-073` | Fee Waiver, Tax Exemption & Exception Rules | configEditor | 1 | 0 | — |
| `ADM-074` | Price Calculation Sequence & Formula Engine | configEditor | 2 | 1 | — |
| `ADM-075` | Currency Precision, Rounding & Monetary Rules | listDetail | 2 | 1 | — |
| `ADM-076` | Price Breakdown, Calculation Simulation & Explainability | configEditor | 1 | 0 | — |
| `ADM-077` | Calculation Validation, Reconciliation & Service Interface | listDetail | 4 | 0 | — |

## Thin screens in this batch

**ADM-077 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-068",
  "name": "Tax, Fee & Calculation Command Center",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "3",
   "number": "10.3.1",
   "page": 39
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/tax-fee-calculation-command-center-adm-068",
   "component": "apps/ticvai-web/src/routes/commercial/TaxFeeCalculationCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-069",
    "ADM-070",
    "ADM-071",
    "ADM-072",
    "ADM-073",
    "ADM-074",
    "ADM-075",
    "ADM-076",
    "ADM-077"
   ],
   "inferred": false,
   "notes": "**The board's hub.** The workshop specified this module as boards of ten and opened each with a command centre; the other nine screens are that board's detail, so they are reached from here and return here.",
   "transitions": [
    {
     "to": "ADM-002",
     "trigger": "Platform Dashboard",
     "provenance": "derived — ADM-002 declares entryState.params  and ADM-068 holds none of them, so the edge carries nothing and ADM-002 opens cold"
    },
    {
     "to": "ADM-069",
     "trigger": "Works in Tax Profile & Jurisdiction Configuration",
     "provenance": "flow F145 step 1→2",
     "operation": "listTaxFeeCalculation"
    },
    {
     "to": "ADM-070",
     "trigger": "Works in Tax Rule & Treatment Builder",
     "provenance": "flow F145 step 3→4",
     "operation": "listTaxFeeCalculation"
    },
    {
     "to": "ADM-071",
     "trigger": "Works in Fee & Surcharge Library",
     "provenance": "flow F145 step 5→6",
     "operation": "listTaxFeeCalculation"
    },
    {
     "to": "ADM-072",
     "trigger": "Works in Fee Applicability & Charging Rule Builder",
     "provenance": "flow F145 step 7→8",
     "operation": "listTaxFeeCalculation"
    },
    {
     "to": "ADM-073",
     "trigger": "Works in Fee Waiver, Tax Exemption & Exception Rules",
     "provenance": "flow F145 step 9→10",
     "operation": "listTaxFeeCalculation"
    },
    {
     "to": "ADM-074",
     "trigger": "Works in Price Calculation Sequence & Formula Engine",
     "provenance": "flow F145 step 11→12",
     "operation": "listTaxFeeCalculation"
    },
    {
     "to": "ADM-075",
     "trigger": "Works in Currency Precision, Rounding & Monetary Rules",
     "provenance": "flow F145 step 13→14",
     "operation": "listTaxFeeCalculation"
    },
    {
     "to": "ADM-076",
     "trigger": "Works in Price Breakdown, Calculation Simulation & Explainability",
     "provenance": "flow F145 step 15→16",
     "operation": "listTaxFeeCalculation"
    },
    {
     "to": "ADM-077",
     "trigger": "Works in Calculation Validation, Reconciliation & Service Interface",
     "provenance": "flow F145 step 17→18",
     "operation": "listTaxFeeCalculation"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Authorized administrators can understand the complete status and health of TICVAI tax, fee and price-calculation configuration from one workspace.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide Finance, Commercial and Pricing administrators with one central view of TICVAI's price-calculation configuration.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 6 actions on this screen and the screen declares 1 operation.** Unserved: Create Tax Profile, Create Fee, Create Calculation Profile, Run Simulation, Validate Configuration, View Dependencies. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 39 §Quick Actions"
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
       "label": "Search tax fee calculation",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 39 §Filter by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Tax",
        "Fee",
        "Surcharge",
        "Waiver",
        "Exemption",
        "Calculation Profile",
        "Rounding Profile"
       ],
       "notes": "The pack filters this screen by tax, fee, surcharge, waiver, exemption, calculation profile and 1 more — which are present is a decision the pack already made.",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 39 §Filter by"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Active Tax Profiles",
       "bindsTo": "TaxFeeCalculationCommandCenterSummary.activeTaxProfiles",
       "operation": "listTaxFeeCalculation",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Tax Jurisdictions",
       "bindsTo": "TaxFeeCalculationCommandCenterSummary.taxJurisdictions",
       "operation": "listTaxFeeCalculation",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Active Fee Profiles",
       "bindsTo": "TaxFeeCalculationCommandCenterSummary.activeFeeProfiles",
       "operation": "listTaxFeeCalculation",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Active Surcharges",
       "bindsTo": "TaxFeeCalculationCommandCenterSummary.activeSurcharges",
       "operation": "listTaxFeeCalculation",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Exemption Rules",
       "bindsTo": "TaxFeeCalculationCommandCenterSummary.exemptionRules",
       "operation": "listTaxFeeCalculation",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Calculation Profiles",
       "bindsTo": "TaxFeeCalculationCommandCenterSummary.calculationProfiles",
       "operation": "listTaxFeeCalculation",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Products missing tax",
       "bindsTo": "TaxFeeCalculationCommandCenterSummary.productsMissingTax",
       "operation": "listTaxFeeCalculation",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Products Missing Calculation Profile",
       "bindsTo": "TaxFeeCalculationCommandCenterSummary.productsMissingCalculationProfile",
       "operation": "listTaxFeeCalculation",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Configuration Conflicts",
       "bindsTo": "TaxFeeCalculationCommandCenterSummary.configurationConflicts",
       "operation": "listTaxFeeCalculation",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Upcoming Tax Changes",
       "bindsTo": "TaxFeeCalculationCommandCenterSummary.upcomingTaxChanges",
       "operation": "listTaxFeeCalculation",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Validation Issues",
       "bindsTo": "TaxFeeCalculationCommandCenterSummary.validationIssues",
       "operation": "listTaxFeeCalculation",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Recently modified rules",
       "bindsTo": "TaxFeeCalculationCommandCenterSummary.recentlyModifiedRules",
       "operation": "listTaxFeeCalculation",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every tax fee calculation",
       "columns": [
        "TaxFeeCalculationCommandCenterView.profileName",
        "TaxFeeCalculationCommandCenterView.type",
        "TaxFeeCalculationCommandCenterView.country",
        "TaxFeeCalculationCommandCenterView.legalEntity",
        "TaxFeeCalculationCommandCenterView.market",
        "TaxFeeCalculationCommandCenterView.currency",
        "TaxFeeCalculationCommandCenterView.productScope",
        "TaxFeeCalculationCommandCenterView.status",
        "TaxFeeCalculationCommandCenterView.owner"
       ],
       "bindsTo": "TaxFeeCalculationCommandCenterView",
       "operation": "listTaxFeeCalculation",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 39 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected tax fee calculation",
       "bindsTo": "TaxFeeCalculationCommandCenterView",
       "columns": [
        "TaxFeeCalculationCommandCenterView.profileName",
        "TaxFeeCalculationCommandCenterView.type",
        "TaxFeeCalculationCommandCenterView.country",
        "TaxFeeCalculationCommandCenterView.legalEntity",
        "TaxFeeCalculationCommandCenterView.market",
        "TaxFeeCalculationCommandCenterView.currency",
        "TaxFeeCalculationCommandCenterView.productScope",
        "TaxFeeCalculationCommandCenterView.status",
        "TaxFeeCalculationCommandCenterView.owner"
       ],
       "notes": null,
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 39 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create Tax Profile",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 39 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Create Fee",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 39 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Create Calculation Profile",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 39 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Run Simulation",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 39 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Validate Configuration",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 39 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "View Dependencies",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 39 §Quick Actions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The tax fee calculation list.",
   "error": "Could not load. Names which read failed and leaves the tax fee calculation untouched.",
   "emptyFirstRun": "No tax fee calculation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the tax fee calculation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listTaxFeeCalculation",
    "contract": "catalogue",
    "purpose": "Tax, Fee & Calculation Command Center",
    "trigger": "onLoad"
   },
   {
    "operationId": "listTaxInvoices",
    "contract": "finance",
    "purpose": "List tax invoices",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
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
   "preloaded": [
    "TaxFeeCalculationCommandCenterSummary.activeTaxProfiles",
    "TaxFeeCalculationCommandCenterSummary.taxJurisdictions",
    "TaxFeeCalculationCommandCenterSummary.activeFeeProfiles",
    "TaxFeeCalculationCommandCenterSummary.activeSurcharges",
    "TaxFeeCalculationCommandCenterSummary.exemptionRules",
    "TaxFeeCalculationCommandCenterSummary.calculationProfiles"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-068",
   "workshopBoard": "wireframes/WS97 Pricing   Revenue Management Board 3.dc.html#adm-068"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 39. 22 of 29 labels bound to a contract property; 35 of 44 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P09",
   "audience": "platformAdmin",
   "formFactor": "web",
   "shortName": "TICVAI Web",
   "name": "TICVAI Web — Platform Console",
   "offlineCapable": false,
   "app": "ticvai-web",
   "operator": "ticvai",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P10",
     "P11",
     "P14",
     "P17"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ADM-069",
  "name": "Tax Profile & Jurisdiction Configuration",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "3",
   "number": "10.3.2",
   "page": 40
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/tax-profile-jurisdiction-configuration-adm-069",
   "component": "apps/ticvai-web/src/routes/commercial/TaxProfileJurisdictionConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-068"
   ],
   "exitTo": [
    "ADM-068"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-068, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-068",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F145 step 2→3",
     "operation": "setTaxProfileJurisdiction"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "jurisdictions.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Define reusable tax profiles according to legal entity, country, jurisdiction and commercial context.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 5 actions on this screen and the screen declares 1 operation.** Unserved: Sales Tax, Entertainment Tax, Tourism Tax, Municipality Tax, Service Tax. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 40 §Support"
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
       "label": "Tax Profile Name",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 40 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Tax Profile Code",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 40 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Tax Type",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 40 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Country",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 40 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Region/Jurisdiction",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 40 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Legal Entity",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 40 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Tax Registration Number",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 40 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Currency",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 40 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Effective From",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 40 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Effective To",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 40 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Status",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 40 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Owner",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 40 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Sales Tax",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 40 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Entertainment Tax",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 40 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Tourism Tax",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 40 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Municipality Tax",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 40 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Service Tax",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 40 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The tax profile jurisdiction configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the tax profile jurisdiction untouched.",
   "emptyFirstRun": "No tax profile jurisdiction configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setTaxProfileJurisdiction",
    "contract": "catalogue",
    "purpose": "Tax Profile & Jurisdiction Configuration",
    "trigger": "onAction"
   },
   {
    "operationId": "listTaxInvoiceTemplates",
    "contract": "finance",
    "purpose": "Show invoice templates and number series",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "setTaxInvoiceTemplate",
    "contract": "finance",
    "purpose": "Edit an invoice template and series",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listEInvoicingProviders",
    "contract": "finance",
    "purpose": "Show the e-invoicing provider connection",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "setEInvoicingProvider",
    "contract": "finance",
    "purpose": "Configure the e-invoicing provider",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-069",
   "workshopBoard": "wireframes/WS97 Pricing   Revenue Management Board 3.dc.html#adm-069"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 40. 0 of 0 labels bound to a contract property; 17 of 40 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P09",
   "audience": "platformAdmin",
   "formFactor": "web",
   "shortName": "TICVAI Web",
   "name": "TICVAI Web — Platform Console",
   "offlineCapable": false,
   "app": "ticvai-web",
   "operator": "ticvai",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P10",
     "P11",
     "P14",
     "P17"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ADM-070",
  "name": "Tax Rule & Treatment Builder",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "3",
   "number": "10.3.3",
   "page": 41
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/tax-rule-treatment-builder-adm-070",
   "component": "apps/ticvai-web/src/routes/commercial/TaxRuleTreatmentBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-068"
   ],
   "exitTo": [
    "ADM-068"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-068, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-068",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F145 step 4→5",
     "operation": "setTaxRuleTreatment"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "taxable commercial transaction.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Define how taxes are applied to products and transactions.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 5 actions on this screen and the screen declares 1 operation.** Unserved: Out of Scope, Fixed Tax. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 41 §Support"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 41"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 41"
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
       "label": "Tax Inclusive",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 41 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Tax Exclusive",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 41 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Tax Exempt",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 41 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Out of Scope",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 41 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Fixed Tax",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 41 §Support"
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
   "loading": "The tax rule treatment list.",
   "error": "Could not load. Names which read failed and leaves the tax rule treatment untouched.",
   "emptyFirstRun": "No tax rule treatment yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the tax rule treatment are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setTaxRuleTreatment",
    "contract": "catalogue",
    "purpose": "Tax Rule & Treatment Builder",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-070",
   "workshopBoard": "wireframes/WS97 Pricing   Revenue Management Board 3.dc.html#adm-070"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 41. 0 of 0 labels bound to a contract property; 5 of 29 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P09",
   "audience": "platformAdmin",
   "formFactor": "web",
   "shortName": "TICVAI Web",
   "name": "TICVAI Web — Platform Console",
   "offlineCapable": false,
   "app": "ticvai-web",
   "operator": "ticvai",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P10",
     "P11",
     "P14",
     "P17"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ADM-071",
  "name": "Fee & Surcharge Library",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "3",
   "number": "10.3.4",
   "page": 43
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/fee-surcharge-library-adm-071",
   "component": "apps/ticvai-web/src/routes/commercial/FeeSurchargeLibrary.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-068"
   ],
   "exitTo": [
    "ADM-068"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-068, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-068",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F145 step 6→7",
     "operation": "listFeeSurcharge"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "than defining them separately within sales channels.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture; Configure whether the fee is) and no display directory — it is settings, not a population",
  "purpose": "Create standardized reusable non-base-price charges.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 18 actions on this screen; 8 are served since the writers pass (29 September): Booking Fee, Transaction Fee, Service Fee, Convenience Fee, Delivery Fee, Handling Fee, Modification Fee, Rescheduling Fee by `setFeeDefinition`.** Still unserved: the rest of the pack list past the eight shown here. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 43 §Support"
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
       "label": "Fee Name",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 43 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Fee Code",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 43 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Fee Type",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 43 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Description",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 43 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Calculation Method",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 43 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Value",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 43 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Currency",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 43 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Tax Treatment",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 43 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Refundability",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 43 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Effective Period",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 43 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Status",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 43 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Customer Visible",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 43 §Configure whether the fee is"
      },
      {
       "kind": "textField",
       "label": "Included in Display Price",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 43 §Configure whether the fee is"
      },
      {
       "kind": "selectField",
       "label": "Shown Separately",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 43 §Configure whether the fee is"
      },
      {
       "kind": "selectField",
       "label": "Internal Only",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 43 §Configure whether the fee is"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Booking Fee",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 43 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Transaction Fee",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 43 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Service Fee",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 43 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Convenience Fee",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 43 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Delivery Fee",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 43 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Handling Fee",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 43 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Modification Fee",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 43 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Rescheduling Fee",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 43 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Save fee definition",
       "operation": "setFeeDefinition",
       "permission": "PRICE_CONFIGURE",
       "notes": "**The fee and surcharge library** (29 September, writers pass).",
       "provenance": "contract catalogue.yaml PUT /fees"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The fee surcharge configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the fee surcharge untouched.",
   "emptyFirstRun": "No fee surcharge configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listFeeSurcharge",
    "contract": "catalogue",
    "purpose": "Fee & Surcharge Library",
    "trigger": "onLoad"
   },
   {
    "operationId": "setFeeDefinition",
    "contract": "catalogue",
    "purpose": "Create or update a fee or surcharge",
    "trigger": "onAction",
    "invalidates": [
     "listFeeSurcharge"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-071",
   "workshopBoard": "wireframes/WS97 Pricing   Revenue Management Board 3.dc.html#adm-071"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 43. 0 of 0 labels bound to a contract property; 33 of 43 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formSetFeeDefinition",
    "component": "modal",
    "trigger": "Save fee definition",
    "body": "**Collects what `setFeeDefinition` sends before it is called.** Required: `id`, `scopePath`, `code`, `name`, `feeType`, `valueType`, `chargeBasis`, `status`. Optional: `description`, `amount`, `percentage`, `tiers`, `taxTreatment`, `refundability`, `visibility`, `effectiveFrom`, `effectiveTo`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "PricingFee",
    "confirm": {
     "label": "Save fee definition",
     "operation": "setFeeDefinition"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "scopePath",
      "code",
      "name",
      "feeType",
      "valueType",
      "chargeBasis",
      "status",
      "description",
      "amount",
      "percentage",
      "tiers",
      "taxTreatment",
      "refundability",
      "visibility",
      "effectiveFrom",
      "effectiveTo"
     ]
    },
    "provenance": "contract catalogue.yaml PUT /fees"
   }
  ],
  "_platform": {
   "code": "P09",
   "audience": "platformAdmin",
   "formFactor": "web",
   "shortName": "TICVAI Web",
   "name": "TICVAI Web — Platform Console",
   "offlineCapable": false,
   "app": "ticvai-web",
   "operator": "ticvai",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P10",
     "P11",
     "P14",
     "P17"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ADM-072",
  "name": "Fee Applicability & Charging Rule Builder",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "3",
   "number": "10.3.5",
   "page": 44
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/fee-applicability-charging-rule-builder-adm-072",
   "component": "apps/ticvai-web/src/routes/commercial/FeeApplicabilityChargingRuleBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-068"
   ],
   "exitTo": [
    "ADM-068"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-068, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-068",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F145 step 8→9",
     "operation": "setFeeApplicabilityCharging"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "satisfied.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure whether fees can) and no display directory — it is settings, not a population",
  "purpose": "Determine when a fee or surcharge should apply. Screen 10.3.4 defines the fee. Screen 10.3.5 defines the conditions that trigger it.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 16 actions on this screen and the screen declares 1 operation.** Unserved: Product, Product Category, Channel, Venue, Event, Customer Type, Membership, Transaction Type …. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 44 §Support"
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
       "label": "Stack",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 44 §Configure whether fees can"
      },
      {
       "kind": "selectField",
       "label": "Replace",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 44 §Configure whether fees can"
      },
      {
       "kind": "selectField",
       "label": "Exclude Another Fee",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 44 §Configure whether fees can"
      },
      {
       "kind": "selectField",
       "label": "Apply Once",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 44 §Configure whether fees can"
      },
      {
       "kind": "selectField",
       "label": "Apply Per Item",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 44 §Configure whether fees can"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Product",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 44 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Product Category",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 44 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Channel",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 44 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Venue",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 44 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Event",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 44 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Customer Type",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 44 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Membership",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 44 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Transaction Type",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 44 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The fee applicability charging configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the fee applicability charging untouched.",
   "emptyFirstRun": "No fee applicability charging configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setFeeApplicabilityCharging",
    "contract": "catalogue",
    "purpose": "Fee Applicability & Charging Rule Builder",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-072",
   "workshopBoard": "wireframes/WS97 Pricing   Revenue Management Board 3.dc.html#adm-072"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 44. 0 of 0 labels bound to a contract property; 21 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P09",
   "audience": "platformAdmin",
   "formFactor": "web",
   "shortName": "TICVAI Web",
   "name": "TICVAI Web — Platform Console",
   "offlineCapable": false,
   "app": "ticvai-web",
   "operator": "ticvai",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P10",
     "P11",
     "P14",
     "P17"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ADM-073",
  "name": "Fee Waiver, Tax Exemption & Exception Rules",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "3",
   "number": "10.3.6",
   "page": 46
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/fee-waiver-tax-exemption-exception-rules-adm-073",
   "component": "apps/ticvai-web/src/routes/commercial/FeeWaiverTaxExemptionExceptionRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-068"
   ],
   "exitTo": [
    "ADM-068"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-068, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-068",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F145 step 10→11",
     "operation": "listFeeWaiverTax"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Fees and taxes can only be waived or exempted through explicitly authorized rules or governed manual exceptions.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure by) and no display directory — it is settings, not a population",
  "purpose": "Govern circumstances under which a normally applicable tax or fee may be reduced, waived or exempted.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 7 actions on this screen and the screen declares 1 operation.** Unserved: Zero-Rated Tax, Complimentary Transaction, Operational Waiver, Contractual Waiver. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 46 §Support"
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
       "label": "Membership Benefit",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 46 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Loyalty Tier",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 46 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Corporate Agreement",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 46 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "B2B Contract",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 46 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Customer Segment",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 46 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Staff Role",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 46 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Promotion",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 46 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Service Recovery",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 46 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Operational Issue",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 46 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Legal Exemption",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 46 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Supervisor Override",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 46 §Configure by"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Fee Waiver",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 46 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Fee Reduction",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 46 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Tax Exemption",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 46 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Zero-Rated Tax",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 46 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Complimentary Transaction",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 46 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Operational Waiver",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 46 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Contractual Waiver",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 46 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The fee waiver tax configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the fee waiver tax untouched.",
   "emptyFirstRun": "No fee waiver tax configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listFeeWaiverTax",
    "contract": "catalogue",
    "purpose": "Fee Waiver, Tax Exemption & Exception Rules",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-073",
   "workshopBoard": "wireframes/WS97 Pricing   Revenue Management Board 3.dc.html#adm-073"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 46. 0 of 0 labels bound to a contract property; 18 of 36 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P09",
   "audience": "platformAdmin",
   "formFactor": "web",
   "shortName": "TICVAI Web",
   "name": "TICVAI Web — Platform Console",
   "offlineCapable": false,
   "app": "ticvai-web",
   "operator": "ticvai",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P10",
     "P11",
     "P14",
     "P17"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ADM-074",
  "name": "Price Calculation Sequence & Formula Engine",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "3",
   "number": "10.3.7",
   "page": 47
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/price-calculation-sequence-formula-engine-adm-074",
   "component": "apps/ticvai-web/src/routes/commercial/PriceCalculationSequenceFormulaEngine.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-068"
   ],
   "exitTo": [
    "ADM-068"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-068, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-068",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F145 step 12→13",
     "operation": "listPriceCalculationSequence"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "The system can deterministically calculate the final payable amount using a governed and traceable sequence of commercial components.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Each step should define) and no display directory — it is settings, not a population",
  "purpose": "Define the exact sequence TICVAI follows to calculate the final payable amount. This is the heart of Board 3.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Input",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 47 §Each step should define"
      },
      {
       "kind": "selectField",
       "label": "Formula",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 47 §Each step should define"
      },
      {
       "kind": "selectField",
       "label": "Sequence",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 47 §Each step should define"
      },
      {
       "kind": "selectField",
       "label": "Taxability",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 47 §Each step should define"
      },
      {
       "kind": "selectField",
       "label": "Rounding",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 47 §Each step should define"
      },
      {
       "kind": "selectField",
       "label": "Dependency",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 47 §Each step should define"
      },
      {
       "kind": "selectField",
       "label": "Output",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 47 §Each step should define"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save price calculation policy",
       "operation": "setPriceCalculationPolicy",
       "permission": "PRICE_CONFIGURE",
       "notes": "**The ordered steps that turn a rate into a payable amount** (29 September, writers pass).",
       "provenance": "contract catalogue.yaml PUT /calculation-profiles"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The price calculation sequence configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the price calculation sequence untouched.",
   "emptyFirstRun": "No price calculation sequence configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPriceCalculationSequence",
    "contract": "catalogue",
    "purpose": "Price Calculation Sequence & Formula Engine",
    "trigger": "onLoad"
   },
   {
    "operationId": "setPriceCalculationPolicy",
    "contract": "catalogue",
    "purpose": "Save a price calculation sequence, whole",
    "trigger": "onAction",
    "invalidates": [
     "listPriceCalculationSequence"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-074",
   "workshopBoard": "wireframes/WS97 Pricing   Revenue Management Board 3.dc.html#adm-074"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 47. 0 of 0 labels bound to a contract property; 7 of 43 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formSetPriceCalculationPolicy",
    "component": "modal",
    "trigger": "Save price calculation policy",
    "body": "**Collects what `setPriceCalculationPolicy` sends before it is called.** Required: `id`, `scopePath`, `code`, `name`, `status`. Optional: `isDefault`, `effectiveFrom`, `effectiveTo`, `steps`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CalculationProfile",
    "confirm": {
     "label": "Save price calculation policy",
     "operation": "setPriceCalculationPolicy"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "scopePath",
      "code",
      "name",
      "status",
      "isDefault",
      "effectiveFrom",
      "effectiveTo",
      "steps"
     ]
    },
    "provenance": "contract catalogue.yaml PUT /calculation-profiles"
   }
  ],
  "_platform": {
   "code": "P09",
   "audience": "platformAdmin",
   "formFactor": "web",
   "shortName": "TICVAI Web",
   "name": "TICVAI Web — Platform Console",
   "offlineCapable": false,
   "app": "ticvai-web",
   "operator": "ticvai",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P10",
     "P11",
     "P14",
     "P17"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ADM-075",
  "name": "Currency Precision, Rounding & Monetary Rules",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "3",
   "number": "10.3.8",
   "page": 49
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/currency-precision-rounding-monetary-rules-adm-075",
   "component": "apps/ticvai-web/src/routes/commercial/CurrencyPrecisionRoundingMonetaryRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-068"
   ],
   "exitTo": [
    "ADM-068"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-068, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-068",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F145 step 14→15",
     "operation": "listCurrencyPrecisionRounding"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "currency precision and rounding rules.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Ensure monetary calculations remain consistent across countries, currencies, channels and payment systems.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every currency precision rounding",
       "columns": [
        "AED 199.50"
       ],
       "bindsTo": "CurrencyPrecisionRoundingMonetaryRulesView",
       "operation": "listCurrencyPrecisionRounding",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 49 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected currency precision rounding",
       "bindsTo": "CurrencyPrecisionRoundingMonetaryRulesView",
       "columns": [
        "AED 199.50"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Calculated”, “Calculated Total”, “Cash Payable”, “The engine should ensure”, “Currency Conversion”.",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 49 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Round Down",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 49 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Save currency rounding rule",
       "operation": "setCurrencyRoundingRule",
       "permission": "PRICE_CONFIGURE",
       "notes": "**One rounding profile per currency the tenant sells in** (29 September, writers pass).",
       "provenance": "contract catalogue.yaml PUT /rounding-profiles"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The currency precision rounding list.",
   "error": "Could not load. Names which read failed and leaves the currency precision rounding untouched.",
   "emptyFirstRun": "No currency precision rounding yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the currency precision rounding are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCurrencyPrecisionRounding",
    "contract": "catalogue",
    "purpose": "Currency Precision, Rounding & Monetary Rules",
    "trigger": "onLoad"
   },
   {
    "operationId": "setCurrencyRoundingRule",
    "contract": "catalogue",
    "purpose": "Set precision and rounding for a currency",
    "trigger": "onAction",
    "invalidates": [
     "listCurrencyPrecisionRounding"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "AED 199.50"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-075",
   "workshopBoard": "wireframes/WS97 Pricing   Revenue Management Board 3.dc.html#adm-075"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 49. 0 of 1 labels bound to a contract property; 13 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formSetCurrencyRoundingRule",
    "component": "modal",
    "trigger": "Save currency rounding rule",
    "body": "**Collects what `setCurrencyRoundingRule` sends before it is called.** Required: `id`, `scopePath`, `currency`, `decimalPlaces`, `roundingMethod`, `roundingStage`, `status`. Optional: `code`, `name`, `minimumMonetaryUnit`, `displayPrecision`, `calculationPrecision`, `cashRoundingIncrement`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "RoundingProfile",
    "confirm": {
     "label": "Save currency rounding rule",
     "operation": "setCurrencyRoundingRule"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "scopePath",
      "currency",
      "decimalPlaces",
      "roundingMethod",
      "roundingStage",
      "status",
      "code",
      "name",
      "minimumMonetaryUnit",
      "displayPrecision",
      "calculationPrecision",
      "cashRoundingIncrement"
     ]
    },
    "provenance": "contract catalogue.yaml PUT /rounding-profiles"
   }
  ],
  "_platform": {
   "code": "P09",
   "audience": "platformAdmin",
   "formFactor": "web",
   "shortName": "TICVAI Web",
   "name": "TICVAI Web — Platform Console",
   "offlineCapable": false,
   "app": "ticvai-web",
   "operator": "ticvai",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P10",
     "P11",
     "P14",
     "P17"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ADM-076",
  "name": "Price Breakdown, Calculation Simulation & Explainability",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "3",
   "number": "10.3.9",
   "page": 50
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/price-breakdown-calculation-simulation-explainability-adm-076",
   "component": "apps/ticvai-web/src/routes/commercial/PriceBreakdownCalculationSimulationExplainabilit.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-068"
   ],
   "exitTo": [
    "ADM-068"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-068, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-068",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F145 step 16→17",
     "operation": "simulatePriceBreakdownCalculation"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Authorized users can reproduce and explain every monetary component contributing to the final payable amount before configuration goes live.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Select) and no display directory — it is settings, not a population",
  "purpose": "Allow administrators to test the complete calculation before releasing configuration into production.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Customer",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 50 §Select"
      },
      {
       "kind": "selectField",
       "label": "Product",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 50 §Select"
      },
      {
       "kind": "selectField",
       "label": "Quantity",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 50 §Select"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 50 §Select"
      },
      {
       "kind": "selectField",
       "label": "Event",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 50 §Select"
      },
      {
       "kind": "selectField",
       "label": "Channel",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 50 §Select"
      },
      {
       "kind": "selectField",
       "label": "Date",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 50 §Select"
      },
      {
       "kind": "selectField",
       "label": "Timeslot",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 50 §Select"
      },
      {
       "kind": "selectField",
       "label": "Membership",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 50 §Select"
      },
      {
       "kind": "selectField",
       "label": "Promotion",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 50 §Select"
      },
      {
       "kind": "selectField",
       "label": "Payment Method",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 50 §Select"
      },
      {
       "kind": "selectField",
       "label": "Delivery Method",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 50 §Select"
      },
      {
       "kind": "selectField",
       "label": "Currency",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 50 §Select"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Run simulation",
       "provenance": "contract operation simulatePriceBreakdownCalculation"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The price breakdown calculation configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the price breakdown calculation untouched.",
   "emptyFirstRun": "No price breakdown calculation configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "simulatePriceBreakdownCalculation",
    "contract": "catalogue",
    "purpose": "Price Breakdown, Calculation Simulation & Explainability",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-076",
   "workshopBoard": "wireframes/WS97 Pricing   Revenue Management Board 3.dc.html#adm-076"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 50. 0 of 0 labels bound to a contract property; 13 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P09",
   "audience": "platformAdmin",
   "formFactor": "web",
   "shortName": "TICVAI Web",
   "name": "TICVAI Web — Platform Console",
   "offlineCapable": false,
   "app": "ticvai-web",
   "operator": "ticvai",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P10",
     "P11",
     "P14",
     "P17"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ADM-077",
  "name": "Calculation Validation, Reconciliation & Service Interface",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "3",
   "number": "10.3.10",
   "page": 52
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/calculation-validation-reconciliation-service-interface-adm-077",
   "component": "apps/ticvai-web/src/routes/commercial/CalculationValidationReconciliationServiceInterf.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-068"
   ],
   "exitTo": [
    "ADM-068"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-068, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation."
  },
  "density": "compact",
  "purposeNote": "The calculation engine passes configured reconciliation and regression tests and exposes one authoritative calculation service to all TICVAI sales and operational modules. Board 3 — Final Screen Register # Backend Screen Core Responsibility 10.3. Calculation configuration Tax, Fee & Calculation Command Center 1 health 10.3. Tax Profile & Jurisdiction Configuration Tax master configuration 2 10.3. Tax Rule & Treatment Builder Tax applicability/calculation 3 10.3. Fee & Surcharge Library Reusable fee definitions 4 10.3. Fee Applicability & Charging Rule Builder Fee conditions 5 10.3. Fee Waiver,",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide final technical and commercial validation of the pricing calculation engine and define how other TICVAI modules consume it. Boards 1–3 established the commercial and calculation engines: Board 1: What prices exist? Board 2: Which price applies? Board 3: How is the final payable amount calculated?",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 52"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 52"
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
       "impliedBy": "listCalculationValidationReconciliation",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "transmitEInvoices",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "transmitEInvoices"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The calculation validation reconciliation list.",
   "error": "Could not load. Names which read failed and leaves the calculation validation reconciliation untouched.",
   "emptyFirstRun": "No calculation validation reconciliation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the calculation validation reconciliation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCalculationValidationReconciliation",
    "contract": "catalogue",
    "purpose": "Calculation Validation, Reconciliation & Service Interface",
    "trigger": "onLoad"
   },
   {
    "operationId": "listEInvoicingProviders",
    "contract": "finance",
    "purpose": "Show the e-invoicing provider connection",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "listEInvoiceTransmissions",
    "contract": "finance",
    "purpose": "E-invoicing transmission log and failures",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "transmitEInvoices",
    "contract": "finance",
    "purpose": "Send / resend documents to e-invoicing",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "CalculationValidationReconciliationServiceInterfaceView.code"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-077",
   "workshopBoard": "wireframes/WS97 Pricing   Revenue Management Board 3.dc.html#adm-077"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 52. 0 of 0 labels bound to a contract property; 0 of 121 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P09",
   "audience": "platformAdmin",
   "formFactor": "web",
   "shortName": "TICVAI Web",
   "name": "TICVAI Web — Platform Console",
   "offlineCapable": false,
   "app": "ticvai-web",
   "operator": "ticvai",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P10",
     "P11",
     "P14",
     "P17"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
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
 "listCalculationValidationReconciliation": {
  "method": "GET",
  "path": "/calculation-validation-reconciliation",
  "contract": "catalogue",
  "summary": "Calculation Validation, Reconciliation & Service Interface",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "resultKind",
    "in": "query",
    "required": false
   },
   {
    "name": "area",
    "in": "query",
    "required": false
   },
   {
    "name": "severity",
    "in": "query",
    "required": false
   },
   {
    "name": "passed",
    "in": "query",
    "required": false
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
 "listCurrencyPrecisionRounding": {
  "method": "GET",
  "path": "/currency-precision-rounding",
  "contract": "catalogue",
  "summary": "Currency Precision, Rounding & Monetary Rules",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "CurrencyPrecisionRoundingMonetaryRulesView"
 },
 "listEInvoiceTransmissions": {
  "method": "GET",
  "path": "/e-invoicing/transmissions",
  "contract": "finance",
  "summary": "What was sent to the e-invoicing provider, and what came back",
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
    "name": "documentId",
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
 "listEInvoicingProviders": {
  "method": "GET",
  "path": "/e-invoicing/providers",
  "contract": "finance",
  "summary": "The e-invoicing service provider connection per legal entity",
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
 "listFeeSurcharge": {
  "method": "GET",
  "path": "/fee-surcharge",
  "contract": "catalogue",
  "summary": "Fee & Surcharge Library",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "feeType",
    "in": "query",
    "required": false
   },
   {
    "name": "status",
    "in": "query",
    "required": false
   },
   {
    "name": "search",
    "in": "query",
    "required": false
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
 "listFeeWaiverTax": {
  "method": "GET",
  "path": "/fee-waiver-tax",
  "contract": "catalogue",
  "summary": "Fee Waiver, Tax Exemption & Exception Rules",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "exceptionType",
    "in": "query",
    "required": false
   },
   {
    "name": "eligibilityBasis",
    "in": "query",
    "required": false
   },
   {
    "name": "status",
    "in": "query",
    "required": false
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
 "listPriceCalculationSequence": {
  "method": "GET",
  "path": "/price-calculation-sequence",
  "contract": "catalogue",
  "summary": "Price Calculation Sequence & Formula Engine",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "calculationProfileId",
    "in": "query",
    "required": false
   },
   {
    "name": "asOf",
    "in": "query",
    "required": false
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
 "listTaxFeeCalculation": {
  "method": "GET",
  "path": "/tax-fee-calculation",
  "contract": "catalogue",
  "summary": "Tax, Fee & Calculation Command Center",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "type",
    "in": "query",
    "required": false
   },
   {
    "name": "country",
    "in": "query",
    "required": false
   },
   {
    "name": "legalEntity",
    "in": "query",
    "required": false
   },
   {
    "name": "status",
    "in": "query",
    "required": false
   },
   {
    "name": "search",
    "in": "query",
    "required": false
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
 "listTaxInvoiceTemplates": {
  "method": "GET",
  "path": "/tax-invoice-templates",
  "contract": "finance",
  "summary": "Invoice and credit memo templates and number series, per legal entity",
  "permission": "LEDGER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "legalEntityId",
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
 "listTaxInvoices": {
  "method": "GET",
  "path": "/tax-invoices",
  "contract": "finance",
  "summary": "Tax invoices issued, newest first",
  "permission": "LEDGER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [
   {
    "name": "orderId",
    "in": "query",
    "required": null
   },
   {
    "name": "legalEntityId",
    "in": "query",
    "required": null
   },
   {
    "name": "invoiceType",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "issuedFrom",
    "in": "query",
    "required": null
   },
   {
    "name": "issuedTo",
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
 "setCurrencyRoundingRule": {
  "method": "PUT",
  "path": "/rounding-profiles",
  "contract": "catalogue",
  "summary": "Set precision and rounding for a currency",
  "permission": "PRICE_CONFIGURE",
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
  "requestBody": "RoundingProfile",
  "responds": "RoundingProfile"
 },
 "setEInvoicingProvider": {
  "method": "PUT",
  "path": "/e-invoicing/providers",
  "contract": "finance",
  "summary": "Connect a legal entity to its accredited e-invoicing service provider",
  "permission": "TAX_CONFIGURE",
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
  "requestBody": "FinEInvoicingProvider",
  "responds": "FinEInvoicingProvider"
 },
 "setFeeApplicabilityCharging": {
  "method": "PUT",
  "path": "/fee-applicability-charging",
  "contract": "catalogue",
  "summary": "Fee Applicability & Charging Rule Builder",
  "permission": "PRODUCT_CONFIGURE",
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
  "requestBody": "FeeApplicabilityChargingRuleBuilderInput",
  "responds": "FeeApplicabilityChargingRuleBuilderView"
 },
 "setFeeDefinition": {
  "method": "PUT",
  "path": "/fees",
  "contract": "catalogue",
  "summary": "Create or update a fee or surcharge",
  "permission": "PRICE_CONFIGURE",
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
  "requestBody": "PricingFee",
  "responds": "PricingFee"
 },
 "setPriceCalculationPolicy": {
  "method": "PUT",
  "path": "/calculation-profiles",
  "contract": "catalogue",
  "summary": "Save a price calculation sequence, whole",
  "permission": "PRICE_CONFIGURE",
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
  "requestBody": "CalculationProfile",
  "responds": "CalculationProfile"
 },
 "setTaxInvoiceTemplate": {
  "method": "PUT",
  "path": "/tax-invoice-templates",
  "contract": "finance",
  "summary": "Set a legal entity's template and number series for one document kind",
  "permission": "TAX_CONFIGURE",
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
  "requestBody": "FinTaxInvoiceTemplate",
  "responds": "FinTaxInvoiceTemplate"
 },
 "setTaxProfileJurisdiction": {
  "method": "PUT",
  "path": "/tax-profile-jurisdiction",
  "contract": "catalogue",
  "summary": "Tax Profile & Jurisdiction Configuration",
  "permission": "PRODUCT_CONFIGURE",
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
  "requestBody": "TaxProfileJurisdictionConfigurationInput",
  "responds": "TaxProfileJurisdictionConfigurationView"
 },
 "setTaxRuleTreatment": {
  "method": "PUT",
  "path": "/tax-rule-treatment",
  "contract": "catalogue",
  "summary": "Tax Rule & Treatment Builder",
  "permission": "PRODUCT_CONFIGURE",
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
  "requestBody": "TaxRuleTreatmentBuilderInput",
  "responds": "TaxRuleTreatmentBuilderView"
 },
 "simulatePriceBreakdownCalculation": {
  "method": "PUT",
  "path": "/price-breakdown-calculation",
  "contract": "catalogue",
  "summary": "Price Breakdown, Calculation Simulation & Explainability",
  "permission": "PRODUCT_CONFIGURE",
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
  "requestBody": "PriceBreakdownCalculationSimulationExplainabilityInput",
  "responds": "PriceBreakdownCalculationSimulationExplainabilityView"
 },
 "transmitEInvoices": {
  "method": "POST",
  "path": "/e-invoicing/transmissions",
  "contract": "finance",
  "summary": "Send issued tax documents to the e-invoicing provider",
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
  "responds": null
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "CalculationProfile": {
  "type": "object",
  "x-ticvai-persistence": "catalogue.calculation_profile + catalogue.calculation_step",
  "description": "**The ordered sequence that turns a rate into a payable amount** (29 September, data model DM3). ADM-074: base rate, contextual rate, dynamic adjustment, promotion, package adjustment, fees, tax, rounding, final amount. Versioned; a calculation records the version it used (`calculationVersion`), so history is reproducible.",
  "required": [
   "id",
   "scopePath",
   "code",
   "name",
   "version",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Operations write it at `venue` scope."
   },
   "code": {
    "type": "string",
    "maxLength": 40
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "version": {
    "type": "integer",
    "minimum": 1
   },
   "isDefault": {
    "type": "boolean",
    "default": false
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "effectiveTo": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "status": {
    "allOf": [
     {
      "$ref": "#/components/schemas/CatalogueConfigStatus"
     }
    ],
    "default": "draft"
   },
   "steps": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/CalculationStep"
    }
   },
   "createdAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "CalculationStep": {
  "type": "object",
  "x-ticvai-persistence": "catalogue.calculation_step",
  "description": "**One step of a calculation profile** (29 September, data model DM3). `dependsOn` names earlier steps; a cycle or a step depending on a later one is refused (`422 circularDependency` / `invalidSequence`).",
  "required": [
   "id",
   "calculationProfileId",
   "sequence",
   "stepType",
   "formulaType"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "calculationProfileId": {
    "type": "string",
    "format": "uuid"
   },
   "sequence": {
    "type": "integer",
    "minimum": 1
   },
   "stepType": {
    "type": "string",
    "enum": [
     "commercialBaseRate",
     "contextualRateSelection",
     "dynamicPricingAdjustment",
     "promotionDiscount",
     "packageBundleAdjustment",
     "feesSurcharges",
     "taxCalculation",
     "rounding",
     "finalPayableAmount"
    ]
   },
   "formulaType": {
    "type": "string",
    "enum": [
     "fixedAmount",
     "percentage",
     "percentageOfBase",
     "percentageOfSubtotal",
     "tiered",
     "conditional",
     "minimum",
     "maximum",
     "customGovernedFormula"
    ]
   },
   "input": {
    "type": "string",
    "maxLength": 200,
    "nullable": true
   },
   "formula": {
    "type": "string",
    "nullable": true
   },
   "dependsOn": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "output": {
    "type": "string",
    "maxLength": 200,
    "nullable": true
   },
   "taxability": {
    "type": "string",
    "enum": [
     "inTaxBase",
     "outsideTaxBase",
     null
    ],
    "nullable": true
   },
   "roundingProfileId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   }
  }
 },
 "CalculationValidationReconciliationServiceInterfaceView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Calculation Validation, Reconciliation & Service Interface displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "resultId": {
    "type": "string",
    "description": "Result ID"
   },
   "resultKind": {
    "type": "string",
    "enum": [
     "validationFinding",
     "testScenarioResult"
    ],
    "description": "A configuration finding or a test-suite scenario result"
   },
   "area": {
    "type": "string",
    "enum": [
     "tax",
     "fees",
     "formula",
     "currency",
     "reconciliation",
     "testSuite"
    ],
    "description": "Validation Area (p.52)"
   },
   "code": {
    "type": "string",
    "enum": [
     "missingProfile",
     "invalidRate",
     "expiredRule",
     "overlappingRule",
     "duplicateFee",
     "conflictingRule",
     "missingTaxTreatment",
     "circularDependency",
     "invalidSequence",
     "missingInput",
     "invalidPrecision",
     "unsupportedCurrency",
     "roundingDifference",
     "reconciliationMismatch",
     "scenarioFailed"
    ],
    "description": "What was checked"
   },
   "severity": {
    "type": "string",
    "enum": [
     "critical",
     "warning",
     "information"
    ],
    "description": "Severity; critical blocks progress"
   },
   "message": {
    "type": "string",
    "description": "What was found"
   },
   "subjectId": {
    "type": "string",
    "nullable": true,
    "description": "The profile, rule, fee, formula or currency concerned"
   },
   "scenarioName": {
    "type": "string",
    "nullable": true,
    "description": "Test scenario name"
   },
   "scenarioType": {
    "type": "string",
    "enum": [
     "standardB2cSale",
     "posSale",
     "memberSale",
     "groupBooking",
     "b2bSale",
     "refund",
     "reschedule",
     "multiProductOrder",
     "packageSale",
     "multiCurrencySale"
    ],
    "description": "Test Suite scenario type (pp.52-53)",
    "nullable": true
   },
   "passed": {
    "type": "boolean",
    "nullable": true,
    "description": "Scenario passed; empty for a finding"
   },
   "reconciliation": {
    "type": "object",
    "nullable": true,
    "description": "Reconciliation (p.52): expected against actual totals for a scenario",
    "properties": {
     "lineTotal": {
      "type": "object",
      "properties": {
       "expected": {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       },
       "actual": {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      }
     },
     "taxTotal": {
      "type": "object",
      "properties": {
       "expected": {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       },
       "actual": {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      }
     },
     "feeTotal": {
      "type": "object",
      "properties": {
       "expected": {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       },
       "actual": {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      }
     },
     "discountTotal": {
      "type": "object",
      "properties": {
       "expected": {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       },
       "actual": {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      }
     },
     "finalTotal": {
      "type": "object",
      "properties": {
       "expected": {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       },
       "actual": {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      }
     }
    }
   },
   "calculationVersion": {
    "type": "string",
    "description": "Calculation version the result was produced with (Historical Reproducibility)"
   }
  }
 },
 "CatalogueConfigStatus": {
  "type": "string",
  "enum": [
   "draft",
   "active",
   "inactive",
   "retired"
  ],
  "description": "**The status of a catalogue configuration record** (29 September, data model DM3): price lists, rates, fees and fee rules, tax profiles and rules, calculation and rounding profiles, package pricing and templates. `draft` is being prepared and is never used by a calculation; `active` is in use from its effective date; `inactive` is switched off and may be switched back; `retired` is kept for history only. A record already used by a live price becomes `active` through a published change request, not by an edit."
 },
 "CurrencyPrecisionRoundingMonetaryRulesView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Currency Precision, Rounding & Monetary Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "currency": {
    "type": "string",
    "description": "Currency: ISO 4217 code",
    "pattern": "^[A-Z]{3}$"
   },
   "decimalPlaces": {
    "type": "integer",
    "description": "Decimal Places of the currency, 0 to 3 (MoM 1 Sep §4.5)",
    "minimum": 0,
    "maximum": 3
   },
   "minimumMonetaryUnit": {
    "type": "number",
    "description": "Minimum Monetary Unit, e.g. 0.01, 0.001, 0.05"
   },
   "displayPrecision": {
    "type": "integer",
    "description": "Display Precision: decimals shown",
    "minimum": 0,
    "maximum": 3
   },
   "calculationPrecision": {
    "type": "integer",
    "description": "Calculation Precision: decimals carried while calculating; at most 4, the scale Money is stored at (decided 29 September, readiness close-out)",
    "minimum": 0,
    "maximum": 4
   },
   "roundingMethod": {
    "type": "string",
    "enum": [
     "standard",
     "roundUp",
     "roundDown",
     "bankers",
     "nearestCurrencyUnit",
     "customRegulatoryRule"
    ],
    "description": "Rounding Method (p.49)"
   },
   "ruleId": {
    "type": "string",
    "description": "Currency rule ID"
   },
   "roundingStage": {
    "type": "string",
    "enum": [
     "perItem",
     "perTax",
     "perFee",
     "perLine",
     "atOrderTotal"
    ],
    "description": "Rounding Stage (p.50): where rounding happens"
   },
   "cashRoundingIncrement": {
    "type": "number",
    "nullable": true,
    "description": "Cash Rounding: increment cash totals round to (CHF 19.98 -> 20.00 at 0.05) while electronic payment keeps the exact total; empty for none"
   },
   "status": {
    "type": "string",
    "description": "Status: active or inactive"
   }
  }
 },
 "FeeApplicabilityChargingRuleBuilderInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table covers these fields** — the closest is catalogue.channel_allocation at 5%, so this is not an update to anything the package stores today and no new table has been decided",
  "description": "**What Fee Applicability & Charging Rule Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "product": {
    "type": "string",
    "nullable": true,
    "description": "Condition: product; empty for any"
   },
   "productCategory": {
    "type": "string",
    "nullable": true,
    "description": "Condition: product category"
   },
   "channel": {
    "$ref": "../shared/common.yaml#/components/schemas/SalesChannel",
    "description": "Condition: channel (Call Center Fee IF Channel = Call Center); empty for any"
   },
   "venue": {
    "type": "string",
    "nullable": true,
    "description": "Condition: venue"
   },
   "event": {
    "type": "string",
    "nullable": true,
    "description": "Condition: event"
   },
   "customerType": {
    "type": "string",
    "nullable": true,
    "description": "Condition: customer type"
   },
   "membership": {
    "type": "string",
    "nullable": true,
    "description": "Condition: membership product or tier"
   },
   "transactionType": {
    "type": "string",
    "nullable": true,
    "description": "Condition: transaction type"
   },
   "paymentMethod": {
    "type": "string",
    "nullable": true,
    "description": "Condition: payment method"
   },
   "deliveryMethod": {
    "type": "string",
    "nullable": true,
    "description": "Condition: delivery method"
   },
   "market": {
    "type": "string",
    "nullable": true,
    "description": "Condition: market"
   },
   "country": {
    "type": "string",
    "nullable": true,
    "pattern": "^[A-Z]{2}$",
    "description": "Condition: country"
   },
   "serviceAction": {
    "type": "string",
    "enum": [
     "newSale",
     "modification",
     "reschedule",
     "cancellation",
     "refund",
     "upgrade"
    ],
    "description": "Condition: service action (Action = Reschedule); empty for any",
    "nullable": true
   },
   "rulePriority": {
    "type": "integer",
    "description": "Rule Priority: the lower number is evaluated first"
   },
   "ruleId": {
    "type": "string",
    "description": "Charging rule ID; empty on create"
   },
   "ruleName": {
    "type": "string",
    "description": "Rule name"
   },
   "feeId": {
    "type": "string",
    "description": "The fee from the library (Screen 10.3.4, ADM-071) this rule charges"
   },
   "orderValueMin": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "Threshold: order value at or above which the fee applies"
   },
   "orderValueMax": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "Threshold: order value below which the fee applies (Order Value < AED 100 -> handling fee)"
   },
   "quantityMin": {
    "type": "integer",
    "nullable": true,
    "description": "Condition: minimum quantity"
   },
   "quantityMax": {
    "type": "integer",
    "nullable": true,
    "description": "Condition: maximum quantity"
   },
   "hoursBeforeEventMax": {
    "type": "integer",
    "nullable": true,
    "description": "Condition: the event occurs within this many hours (reschedule within 48 hours)"
   },
   "deliveryDestinationZones": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Condition: delivery destination zones (Dubai, Abu Dhabi, Ras Al Khaimah, international), matched from the checkout address (MoM 1 Sep §4.5 shipping fee)"
   },
   "combination": {
    "type": "string",
    "enum": [
     "stack",
     "replace",
     "exclude"
    ],
    "description": "Fee Combination (p.45): add to other fees, replace them, or exclude named fees"
   },
   "excludedFeeIds": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Fees excluded or replaced when combination is exclude or replace"
   },
   "application": {
    "type": "string",
    "enum": [
     "applyOnce",
     "applyPerItem"
    ],
    "description": "Apply Once per order or Apply Per Item"
   },
   "onMatch": {
    "type": "string",
    "enum": [
     "stopProcessing",
     "continueProcessing"
    ],
    "description": "Stop or Continue Processing after this rule applies"
   },
   "mutualExclusionGroup": {
    "type": "string",
    "nullable": true,
    "description": "Mutual Exclusion: rules sharing a group never apply together; empty for none"
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date",
    "description": "Effective From"
   },
   "effectiveTo": {
    "type": "string",
    "format": "date",
    "description": "Effective To; empty for open-ended",
    "nullable": true
   },
   "status": {
    "type": "string",
    "description": "Status: draft, active, inactive or expired"
   }
  }
 },
 "FeeApplicabilityChargingRuleBuilderView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Fee Applicability & Charging Rule Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "product": {
    "type": "string",
    "nullable": true,
    "description": "Condition: product; empty for any"
   },
   "productCategory": {
    "type": "string",
    "nullable": true,
    "description": "Condition: product category"
   },
   "channel": {
    "$ref": "../shared/common.yaml#/components/schemas/SalesChannel",
    "description": "Condition: channel (Call Center Fee IF Channel = Call Center); empty for any"
   },
   "venue": {
    "type": "string",
    "nullable": true,
    "description": "Condition: venue"
   },
   "event": {
    "type": "string",
    "nullable": true,
    "description": "Condition: event"
   },
   "customerType": {
    "type": "string",
    "nullable": true,
    "description": "Condition: customer type"
   },
   "membership": {
    "type": "string",
    "nullable": true,
    "description": "Condition: membership product or tier"
   },
   "transactionType": {
    "type": "string",
    "nullable": true,
    "description": "Condition: transaction type"
   },
   "paymentMethod": {
    "type": "string",
    "nullable": true,
    "description": "Condition: payment method"
   },
   "deliveryMethod": {
    "type": "string",
    "nullable": true,
    "description": "Condition: delivery method"
   },
   "market": {
    "type": "string",
    "nullable": true,
    "description": "Condition: market"
   },
   "country": {
    "type": "string",
    "nullable": true,
    "pattern": "^[A-Z]{2}$",
    "description": "Condition: country"
   },
   "serviceAction": {
    "type": "string",
    "enum": [
     "newSale",
     "modification",
     "reschedule",
     "cancellation",
     "refund",
     "upgrade"
    ],
    "description": "Condition: service action (Action = Reschedule); empty for any",
    "nullable": true
   },
   "rulePriority": {
    "type": "integer",
    "description": "Rule Priority: the lower number is evaluated first"
   },
   "ruleId": {
    "type": "string",
    "description": "Charging rule ID; empty on create"
   },
   "ruleName": {
    "type": "string",
    "description": "Rule name"
   },
   "feeId": {
    "type": "string",
    "description": "The fee from the library (Screen 10.3.4, ADM-071) this rule charges"
   },
   "orderValueMin": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "Threshold: order value at or above which the fee applies"
   },
   "orderValueMax": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "Threshold: order value below which the fee applies (Order Value < AED 100 -> handling fee)"
   },
   "quantityMin": {
    "type": "integer",
    "nullable": true,
    "description": "Condition: minimum quantity"
   },
   "quantityMax": {
    "type": "integer",
    "nullable": true,
    "description": "Condition: maximum quantity"
   },
   "hoursBeforeEventMax": {
    "type": "integer",
    "nullable": true,
    "description": "Condition: the event occurs within this many hours (reschedule within 48 hours)"
   },
   "deliveryDestinationZones": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Condition: delivery destination zones (Dubai, Abu Dhabi, Ras Al Khaimah, international), matched from the checkout address (MoM 1 Sep §4.5 shipping fee)"
   },
   "combination": {
    "type": "string",
    "enum": [
     "stack",
     "replace",
     "exclude"
    ],
    "description": "Fee Combination (p.45): add to other fees, replace them, or exclude named fees"
   },
   "excludedFeeIds": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Fees excluded or replaced when combination is exclude or replace"
   },
   "application": {
    "type": "string",
    "enum": [
     "applyOnce",
     "applyPerItem"
    ],
    "description": "Apply Once per order or Apply Per Item"
   },
   "onMatch": {
    "type": "string",
    "enum": [
     "stopProcessing",
     "continueProcessing"
    ],
    "description": "Stop or Continue Processing after this rule applies"
   },
   "mutualExclusionGroup": {
    "type": "string",
    "nullable": true,
    "description": "Mutual Exclusion: rules sharing a group never apply together; empty for none"
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date",
    "description": "Effective From"
   },
   "effectiveTo": {
    "type": "string",
    "format": "date",
    "description": "Effective To; empty for open-ended",
    "nullable": true
   },
   "status": {
    "type": "string",
    "description": "Status: draft, active, inactive or expired"
   }
  }
 },
 "FeeSurchargeLibraryView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Fee & Surcharge Library displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "percentage": {
    "type": "number",
    "nullable": true,
    "description": "Value in percent when the method is percentage (Online Service Fee 3%)"
   },
   "feeName": {
    "type": "string",
    "description": "Fee Name"
   },
   "feeCode": {
    "type": "string",
    "description": "Fee Code"
   },
   "feeType": {
    "type": "string",
    "enum": [
     "bookingFee",
     "transactionFee",
     "serviceFee",
     "convenienceFee",
     "deliveryFee",
     "handlingFee",
     "modificationFee",
     "reschedulingFee",
     "cancellationFee",
     "refundFee",
     "paymentFee",
     "channelFee",
     "facilityFee",
     "surcharge",
     "customFee"
    ],
    "description": "Fee Type (p.43)"
   },
   "description": {
    "type": "string",
    "description": "Description"
   },
   "valueType": {
    "type": "string",
    "enum": [
     "fixedAmount",
     "percentage",
     "tiered"
    ],
    "description": "Calculation Method: how the value is expressed"
   },
   "currency": {
    "type": "string",
    "description": "Currency: ISO 4217 code",
    "pattern": "^[A-Z]{3}$"
   },
   "taxTreatment": {
    "type": "string",
    "nullable": true,
    "description": "Tax Treatment: the tax rule (ADM-070) applied to the fee; empty is flagged Missing Tax Treatment by validation"
   },
   "refundability": {
    "type": "string",
    "enum": [
     "refundable",
     "nonRefundable"
    ],
    "description": "Refundability when the order is refunded"
   },
   "status": {
    "type": "string",
    "description": "Status: draft, active, inactive or expired"
   },
   "feeId": {
    "type": "string",
    "description": "Fee ID"
   },
   "chargeBasis": {
    "type": "string",
    "enum": [
     "perTicket",
     "perProduct",
     "perPerson",
     "perOrder",
     "perTransaction",
     "perDay"
    ],
    "description": "What the value is charged per (Call Center Booking Fee AED 15 per order; Online Service Fee 3% per transaction)"
   },
   "amount": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "Value when the method is fixedAmount"
   },
   "tiers": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "fromOrderValue": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "amount": {
       "allOf": [
        {
         "$ref": "../shared/common.yaml#/components/schemas/Money"
        }
       ],
       "nullable": true
      },
      "percentage": {
       "type": "number",
       "nullable": true
      }
     }
    },
    "description": "Tiers when the method is tiered"
   },
   "visibility": {
    "type": "string",
    "enum": [
     "customerVisible",
     "includedInDisplayPrice",
     "shownSeparately",
     "internalOnly"
    ],
    "description": "Fee Visibility (p.44)"
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date",
    "description": "Effective From"
   },
   "effectiveTo": {
    "type": "string",
    "format": "date",
    "description": "Effective To; empty for open-ended",
    "nullable": true
   }
  }
 },
 "FeeWaiverTaxExemptionExceptionRulesView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Fee Waiver, Tax Exemption & Exception Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "reasonRequired": {
    "type": "boolean",
    "description": "Reason mandatory when the exception is applied"
   },
   "exemptionType": {
    "type": "string",
    "nullable": true,
    "description": "Exemption Type for tax exemptions, e.g. diplomatic, charity (the client's list); empty for fee exceptions"
   },
   "ruleId": {
    "type": "string",
    "description": "Exception rule ID"
   },
   "ruleName": {
    "type": "string",
    "description": "Rule name"
   },
   "exceptionType": {
    "type": "string",
    "enum": [
     "feeWaiver",
     "feeReduction",
     "taxExemption",
     "zeroRatedTax",
     "complimentaryTransaction",
     "operationalWaiver",
     "contractualWaiver"
    ],
    "description": "Exception Type (p.46)"
   },
   "targetFeeIds": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Fees waived or reduced; empty for a tax exception"
   },
   "targetTaxProfileIds": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Tax profiles exempted or zero-rated; empty for a fee exception"
   },
   "reductionPercent": {
    "type": "number",
    "nullable": true,
    "description": "Fee Reduction in percent; empty for a full waiver"
   },
   "reductionAmount": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "Fee Reduction as an amount; empty for a full waiver"
   },
   "eligibilityBasis": {
    "type": "string",
    "enum": [
     "membershipBenefit",
     "loyaltyTier",
     "corporateAgreement",
     "b2bContract",
     "customerSegment",
     "staffRole",
     "promotion",
     "serviceRecovery",
     "operationalIssue",
     "legalExemption",
     "supervisorOverride"
    ],
    "description": "Eligibility Condition (p.46)"
   },
   "eligibilityRefId": {
    "type": "string",
    "nullable": true,
    "description": "The membership tier, agreement, contract, segment, role or promotion that qualifies (Gold Member -> Booking Fee waived)"
   },
   "approvalRequired": {
    "type": "boolean",
    "description": "Approval required before the exception takes effect"
   },
   "evidenceRequired": {
    "type": "boolean",
    "description": "Tax Exemption Evidence must be captured (p.47)"
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date",
    "description": "Effective From"
   },
   "effectiveTo": {
    "type": "string",
    "format": "date",
    "description": "Effective To; empty for open-ended",
    "nullable": true
   },
   "status": {
    "type": "string",
    "description": "Status: draft, active, inactive or expired"
   }
  }
 },
 "FinEInvoiceTransmission": {
  "x-ticvai-persistence": "ledger.einvoice_transmission",
  "type": "object",
  "description": "6.1.1. One attempt to send one tax document to the provider, and its answer.",
  "required": [
   "id",
   "documentKind",
   "documentId",
   "legalEntityId",
   "status",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "documentKind": {
    "type": "string",
    "enum": [
     "taxInvoice",
     "creditMemo"
    ]
   },
   "documentId": {
    "type": "string",
    "format": "uuid"
   },
   "documentNumber": {
    "type": "string"
   },
   "legalEntityId": {
    "type": "string",
    "format": "uuid"
   },
   "providerId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "mode": {
    "type": "string",
    "enum": [
     "test",
     "live"
    ]
   },
   "status": {
    "$ref": "#/components/schemas/FinEInvoiceTransmissionStatus"
   },
   "payloadHash": {
    "type": "string",
    "nullable": true,
    "description": "SHA-256 of the document as sent, so a resend can be shown to be the same document."
   },
   "providerMessageId": {
    "type": "string",
    "nullable": true
   },
   "attempt": {
    "type": "integer",
    "minimum": 1
   },
   "errorCodes": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "errorMessage": {
    "type": "string",
    "nullable": true
   },
   "sentAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "answeredAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "scopePath": {
    "type": "string",
    "readOnly": true
   }
  }
 },
 "FinEInvoiceTransmissionStatus": {
  "type": "string",
  "description": "6.1.1. `notRequired` where the legal entity's provider is `disabled` or absent.",
  "enum": [
   "notRequired",
   "queued",
   "sent",
   "accepted",
   "rejected",
   "failed"
  ]
 },
 "FinEInvoicingProvider": {
  "x-ticvai-persistence": "ledger.einvoicing_provider",
  "type": "object",
  "description": "6.1.1. Also the `setEInvoicingProvider` body. One per legal entity.",
  "required": [
   "legalEntityId",
   "providerName",
   "mode"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "legalEntityId": {
    "type": "string",
    "format": "uuid"
   },
   "providerName": {
    "type": "string",
    "maxLength": 200,
    "description": "The accredited service provider the client appoints."
   },
   "endpointUrl": {
    "type": "string",
    "format": "uri",
    "nullable": true
   },
   "testEndpointUrl": {
    "type": "string",
    "format": "uri",
    "nullable": true
   },
   "credentialRef": {
    "type": "string",
    "maxLength": 300,
    "nullable": true,
    "description": "A reference to the secret in the vault; the secret is never stored here."
   },
   "participantId": {
    "type": "string",
    "maxLength": 100,
    "nullable": true,
    "description": "The legal entity's Peppol participant identifier."
   },
   "documentFormat": {
    "type": "string",
    "enum": [
     "pintAe"
    ],
    "default": "pintAe"
   },
   "mode": {
    "type": "string",
    "enum": [
     "disabled",
     "test",
     "live"
    ]
   },
   "transmitWithinHours": {
    "type": "integer",
    "minimum": 1,
    "nullable": true
   },
   "lastAcceptedTestAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Operations write it at `tenant` scope."
   }
  }
 },
 "FinTaxCategory": {
  "type": "string",
  "description": "How a line is treated for VAT. Taken from the tax code the line was posted with.",
  "enum": [
   "standardRated",
   "zeroRated",
   "exempt",
   "outOfScope",
   "reverseCharge"
  ]
 },
 "FinTaxInvoice": {
  "x-ticvai-persistence": "ledger.tax_invoice + ledger.tax_invoice_line",
  "type": "object",
  "description": "5.7.93, 5.10.3. **A guest tax invoice, as issued, never edited.** Corrections are credit memos. The supplier block is a snapshot of the legal entity at issue, so a later change of address does not change a document already given to a guest.",
  "required": [
   "id",
   "invoiceNumber",
   "invoiceType",
   "status",
   "legalEntityId",
   "issuedAt",
   "supplyDate",
   "currency",
   "netAmount",
   "taxAmount",
   "grossAmount",
   "lines"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "invoiceNumber": {
    "type": "string",
    "readOnly": true,
    "description": "Server-assigned from the legal entity's series for the document kind, in sequence and without gaps, e.g. `INV-2026-000123`. Never reused."
   },
   "invoiceType": {
    "$ref": "#/components/schemas/FinTaxInvoiceType"
   },
   "status": {
    "$ref": "#/components/schemas/FinTaxInvoiceStatus"
   },
   "legalEntityId": {
    "type": "string",
    "format": "uuid"
   },
   "templateId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "orderIds": {
    "type": "array",
    "items": {
     "type": "string",
     "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
    }
   },
   "supplierName": {
    "type": "string"
   },
   "supplierAddress": {
    "type": "string",
    "nullable": true
   },
   "supplierTaxRegistrationNumber": {
    "type": "string",
    "nullable": true
   },
   "buyerSubjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The guest the orders belong to; the key a guest's own reads filter on."
   },
   "buyerName": {
    "type": "string",
    "nullable": true
   },
   "buyerAddress": {
    "type": "string",
    "nullable": true
   },
   "buyerCountryCode": {
    "type": "string",
    "pattern": "^[A-Z]{2}$",
    "nullable": true
   },
   "buyerTaxRegistrationNumber": {
    "type": "string",
    "nullable": true
   },
   "customerAccountId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "issuedAt": {
    "type": "string",
    "format": "date-time"
   },
   "supplyDate": {
    "type": "string",
    "format": "date",
    "description": "The date of supply where it differs from the issue date (the latest order's payment date on a consolidated invoice). A day in the region's time zone."
   },
   "currency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$"
   },
   "netAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "discountAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "taxAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "grossAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "taxAmountInLegalCurrency": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "The tax in the legal entity's currency (AED in the UAE) where the invoice currency differs, at the rate the orders were stored at."
   },
   "creditedAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "languages": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "supersedesInvoiceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "renditionAssetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "The PDF rendered at issue; read through getTaxDocumentRendition."
   },
   "eInvoiceStatus": {
    "$ref": "#/components/schemas/FinEInvoiceTransmissionStatus"
   },
   "issuedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "Null where the platform issued it."
   },
   "lines": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/FinTaxInvoiceLine"
    }
   },
   "taxSummary": {
    "type": "array",
    "x-ticvai-persisted": false,
    "description": "VAT per rate and category, summed from the lines for the response.",
    "items": {
     "type": "object",
     "properties": {
      "taxCategory": {
       "$ref": "#/components/schemas/FinTaxCategory"
      },
      "taxRate": {
       "type": "number"
      },
      "taxableAmount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "taxAmount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      }
     }
    }
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Written at the scope of the venue the orders were sold at, or the region for a consolidated invoice across venues."
   }
  }
 },
 "FinTaxInvoiceLine": {
  "type": "object",
  "description": "One line as it was sold and taxed. Amounts are in the invoice currency.",
  "required": [
   "lineNumber",
   "description",
   "quantity",
   "netAmount",
   "taxAmount",
   "grossAmount",
   "taxCategory"
  ],
  "properties": {
   "lineNumber": {
    "type": "integer",
    "minimum": 1
   },
   "orderId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "orderLineId": {
    "type": "string",
    "nullable": true
   },
   "description": {
    "type": "string",
    "maxLength": 500
   },
   "quantity": {
    "type": "number"
   },
   "unitPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "discountAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "netAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "taxCodeId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "taxRate": {
    "type": "number",
    "minimum": 0,
    "maximum": 100
   },
   "taxCategory": {
    "$ref": "#/components/schemas/FinTaxCategory"
   },
   "taxAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "grossAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "creditedAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   }
  }
 },
 "FinTaxInvoiceStatus": {
  "type": "string",
  "description": "`issued` until a credit memo is issued against it; `superseded` where a full invoice replaced a simplified one for the same supply (only if the law allows it; see issueTaxInvoice).",
  "enum": [
   "issued",
   "partiallyCredited",
   "fullyCredited",
   "superseded"
  ]
 },
 "FinTaxInvoiceTemplate": {
  "x-ticvai-persistence": "ledger.tax_invoice_template",
  "type": "object",
  "description": "5.7.93, 5.7.94. Also the `setTaxInvoiceTemplate` body. One per legal entity and document kind.",
  "required": [
   "legalEntityId",
   "documentKind",
   "numberPrefix",
   "languages"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "legalEntityId": {
    "type": "string",
    "format": "uuid"
   },
   "documentKind": {
    "type": "string",
    "enum": [
     "taxInvoice",
     "simplifiedTaxInvoice",
     "creditMemo"
    ]
   },
   "numberPrefix": {
    "type": "string",
    "maxLength": 20,
    "description": "e.g. `INV-`, `SINV-`, `CN-`. The year is added by the series when `resetsYearly`."
   },
   "resetsYearly": {
    "type": "boolean",
    "default": true,
    "description": "A new series per fiscal year of the legal entity."
   },
   "nextNumber": {
    "type": "integer",
    "minimum": 1,
    "description": "May be raised, never lowered below the last number issued."
   },
   "numberPadding": {
    "type": "integer",
    "minimum": 1,
    "maximum": 12,
    "default": 6
   },
   "languages": {
    "type": "array",
    "minItems": 1,
    "description": "Rendered on one page in this order, e.g. `en`, `ar`.",
    "items": {
     "type": "string",
     "pattern": "^[a-z]{2}(-[A-Z]{2})?$"
    }
   },
   "title": {
    "type": "object",
    "description": "The document title per language, e.g. \"Tax Invoice\". Prescribed wording is law (CF-133).",
    "additionalProperties": {
     "type": "string"
    }
   },
   "footerText": {
    "type": "object",
    "additionalProperties": {
     "type": "string"
    }
   },
   "logoAssetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "layoutKey": {
    "type": "string",
    "maxLength": 64,
    "nullable": true
   },
   "autoIssueOnPayment": {
    "type": "boolean",
    "default": false,
    "description": "For `simplifiedTaxInvoice`, issue one on every paid order (the VAT receipt)."
   },
   "simplifiedAllowedUpTo": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "showLegalCurrencyTax": {
    "type": "boolean",
    "default": true,
    "description": "Show the tax in the legal entity's currency when the invoice currency differs."
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date"
   },
   "isActive": {
    "type": "boolean",
    "default": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Operations write it at `tenant` scope."
   }
  }
 },
 "FinTaxInvoiceType": {
  "type": "string",
  "description": "5.7.93. `simplified` for one order with no recipient details, `full` for one order with them, `consolidated` for several paid orders of one buyer on one invoice.",
  "enum": [
   "simplified",
   "full",
   "consolidated"
  ]
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
 "PriceBreakdownCalculationSimulationExplainabilityInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Price Breakdown, Calculation Simulation & Explainability submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "customerId": {
    "type": "string",
    "nullable": true,
    "description": "Customer"
   },
   "productId": {
    "type": "string",
    "description": "Product"
   },
   "quantity": {
    "type": "integer",
    "description": "Quantity",
    "minimum": 1
   },
   "venueId": {
    "type": "string",
    "nullable": true,
    "description": "Venue"
   },
   "eventId": {
    "type": "string",
    "nullable": true,
    "description": "Event"
   },
   "channel": {
    "$ref": "../shared/common.yaml#/components/schemas/SalesChannel",
    "description": "Channel"
   },
   "date": {
    "type": "string",
    "format": "date",
    "description": "Date of visit"
   },
   "timeslotId": {
    "type": "string",
    "nullable": true,
    "description": "Timeslot"
   },
   "membershipId": {
    "type": "string",
    "nullable": true,
    "description": "Membership"
   },
   "promotionCode": {
    "type": "string",
    "nullable": true,
    "description": "Promotion"
   },
   "paymentMethod": {
    "type": "string",
    "nullable": true,
    "description": "Payment Method"
   },
   "deliveryMethod": {
    "type": "string",
    "nullable": true,
    "description": "Delivery Method"
   },
   "currency": {
    "type": "string",
    "description": "Currency: ISO 4217 code",
    "pattern": "^[A-Z]{3}$"
   },
   "compareChannels": {
    "type": "array",
    "items": {
     "$ref": "../shared/common.yaml#/components/schemas/SalesChannel"
    },
    "description": "Channel Comparison (p.51): run the same transaction through these channels too; empty for none"
   }
  }
 },
 "PriceBreakdownCalculationSimulationExplainabilityView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Price Breakdown, Calculation Simulation & Explainability displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "finalPayable": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Final Payable"
   },
   "components": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "sequence": {
       "type": "integer"
      },
      "componentType": {
       "type": "string",
       "enum": [
        "selectedRate",
        "memberAdjustment",
        "dynamicAdjustment",
        "promotion",
        "packageAdjustment",
        "fee",
        "surcharge",
        "waiver",
        "tax",
        "rounding"
       ]
      },
      "label": {
       "type": "string",
       "description": "e.g. Booking Fee, VAT"
      },
      "source": {
       "type": "string",
       "description": "Source: the price list, rule, fee or tax profile"
      },
      "rule": {
       "type": "string",
       "description": "Rule: id of the rule applied, e.g. FE-021, TAX-UAE-01"
      },
      "formula": {
       "type": "string"
      },
      "input": {
       "allOf": [
        {
         "$ref": "../shared/common.yaml#/components/schemas/Money"
        }
       ],
       "description": "Input amount"
      },
      "output": {
       "allOf": [
        {
         "$ref": "../shared/common.yaml#/components/schemas/Money"
        }
       ],
       "description": "Output amount (negative for a reduction)"
      },
      "reason": {
       "type": "string"
      },
      "taxTreatment": {
       "type": "string",
       "nullable": true
      }
     }
    },
    "description": "Explainability Panel and Rule Trace (p.51), in sequence"
   },
   "selectedRate": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Selected Rate x quantity"
   },
   "discountTotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Discounts and adjustments total"
   },
   "feeTotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Fees total"
   },
   "subtotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Subtotal before tax"
   },
   "taxTotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Tax total"
   },
   "calculationVersion": {
    "type": "string",
    "description": "Calculation version used"
   },
   "channelComparison": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "channel": {
       "$ref": "../shared/common.yaml#/components/schemas/SalesChannel"
      },
      "finalPayable": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "difference": {
       "type": "string",
       "description": "Why it differs, e.g. Call Center Booking Fee"
      }
     }
    },
    "description": "Channel Comparison results"
   },
   "aiInsights": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "AI observations for this screen; advisory only, never applied automatically"
   }
  }
 },
 "PriceCalculationSequenceFormulaEngineView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Price Calculation Sequence & Formula Engine displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "input": {
    "type": "string",
    "description": "Input: the named value the step reads, e.g. subtotal"
   },
   "formula": {
    "type": "string",
    "description": "Formula expression, governed"
   },
   "sequence": {
    "type": "integer",
    "description": "Sequence: position in the pipeline"
   },
   "taxability": {
    "type": "string",
    "enum": [
     "inTaxBase",
     "outsideTaxBase"
    ],
    "description": "Taxability: whether this step's amount is part of the tax base; a discount outsideTaxBase gives tax on the pre-discount price where the region requires it (MoM 1 Sep §4.5)"
   },
   "rounding": {
    "type": "string",
    "nullable": true,
    "description": "Rounding rule applied after the step (ADM-075); empty for none"
   },
   "dependsOn": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Dependency: steps whose output this step needs"
   },
   "output": {
    "type": "string",
    "description": "Output: the named value the step produces"
   },
   "stepId": {
    "type": "string",
    "description": "Step ID"
   },
   "calculationProfileId": {
    "type": "string",
    "description": "Calculation profile the step belongs to"
   },
   "stepType": {
    "type": "string",
    "enum": [
     "commercialBaseRate",
     "contextualRateSelection",
     "dynamicPricingAdjustment",
     "promotionDiscount",
     "packageBundleAdjustment",
     "feesSurcharges",
     "taxCalculation",
     "rounding",
     "finalPayableAmount"
    ],
    "description": "Pipeline stage (Recommended Calculation Pipeline, pp.47-48)"
   },
   "formulaType": {
    "type": "string",
    "enum": [
     "fixedAmount",
     "percentage",
     "percentageOfBase",
     "percentageOfSubtotal",
     "tiered",
     "conditional",
     "minimum",
     "maximum",
     "customGovernedFormula"
    ],
    "description": "Formula Builder kind (p.48)"
   },
   "version": {
    "type": "string",
    "description": "Formula version"
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date",
    "description": "Effective From"
   },
   "effectiveTo": {
    "type": "string",
    "format": "date",
    "description": "Effective To; empty for open-ended",
    "nullable": true
   }
  }
 },
 "PricingFee": {
  "type": "object",
  "x-ticvai-persistence": "catalogue.fee",
  "description": "**The fee and surcharge library** (29 September, data model DM3). ADM-071. What a fee is and how it computes; when it applies is `catalogue.fee_rule`. Distinct from `payments.fee_rule` (a provider's processing cost) and `orders.order_fee` (a fee as charged on one order).",
  "required": [
   "id",
   "scopePath",
   "code",
   "name",
   "feeType",
   "valueType",
   "chargeBasis",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Operations write it at `venue` scope."
   },
   "code": {
    "type": "string",
    "maxLength": 40
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "description": {
    "type": "string",
    "nullable": true
   },
   "feeType": {
    "type": "string",
    "enum": [
     "bookingFee",
     "transactionFee",
     "serviceFee",
     "convenienceFee",
     "deliveryFee",
     "handlingFee",
     "modificationFee",
     "reschedulingFee",
     "cancellationFee",
     "refundFee",
     "paymentFee",
     "channelFee",
     "facilityFee",
     "surcharge",
     "customFee"
    ]
   },
   "valueType": {
    "type": "string",
    "enum": [
     "fixedAmount",
     "percentage",
     "tiered"
    ]
   },
   "chargeBasis": {
    "type": "string",
    "enum": [
     "perTicket",
     "perProduct",
     "perPerson",
     "perOrder",
     "perTransaction",
     "perDay"
    ]
   },
   "amount": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true
   },
   "percentage": {
    "type": "number",
    "nullable": true,
    "minimum": 0,
    "maximum": 100
   },
   "tiers": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true,
    "description": "`[{fromOrderValue, amount, percentage}]` for `valueType: tiered`."
   },
   "taxTreatment": {
    "type": "string",
    "maxLength": 60,
    "nullable": true,
    "description": "How the fee is taxed; a `catalogue.tax_rule` may refine it."
   },
   "refundability": {
    "type": "string",
    "enum": [
     "refundable",
     "nonRefundable"
    ],
    "default": "nonRefundable"
   },
   "visibility": {
    "type": "string",
    "enum": [
     "customerVisible",
     "includedInDisplayPrice",
     "shownSeparately",
     "internalOnly"
    ],
    "default": "shownSeparately"
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "effectiveTo": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "status": {
    "allOf": [
     {
      "$ref": "#/components/schemas/CatalogueConfigStatus"
     }
    ],
    "default": "draft"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "RoundingProfile": {
  "type": "object",
  "x-ticvai-persistence": "catalogue.rounding_profile",
  "description": "**Precision and rounding for one currency** (29 September, data model DM3). ADM-075. One per currency the tenant sells in; the engine keeps line totals + tax + fees equal to the transaction total. Distinct from `payments.currency_rule` (settlement currency and payment limits). The currency here is the subject of the rule, not the denomination of an amount.",
  "required": [
   "id",
   "scopePath",
   "currency",
   "decimalPlaces",
   "roundingMethod",
   "roundingStage",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Operations write it at `tenant` scope."
   },
   "code": {
    "type": "string",
    "maxLength": 40,
    "nullable": true
   },
   "name": {
    "type": "string",
    "maxLength": 200,
    "nullable": true
   },
   "currency": {
    "type": "string",
    "maxLength": 3,
    "pattern": "^[A-Z]{3}$"
   },
   "decimalPlaces": {
    "type": "integer",
    "minimum": 0,
    "maximum": 3,
    "description": "Up to three without rounding the third away (MoM 1 Sep 2026 §4.5)."
   },
   "minimumMonetaryUnit": {
    "type": "number",
    "nullable": true
   },
   "displayPrecision": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "maximum": 4
   },
   "calculationPrecision": {
    "type": "integer",
    "minimum": 0,
    "maximum": 4,
    "default": 4
   },
   "roundingMethod": {
    "type": "string",
    "enum": [
     "standard",
     "roundUp",
     "roundDown",
     "bankers",
     "nearestCurrencyUnit",
     "customRegulatoryRule"
    ]
   },
   "roundingStage": {
    "type": "string",
    "enum": [
     "perItem",
     "perTax",
     "perFee",
     "perLine",
     "atOrderTotal"
    ]
   },
   "cashRoundingIncrement": {
    "type": "number",
    "nullable": true
   },
   "status": {
    "allOf": [
     {
      "$ref": "#/components/schemas/CatalogueConfigStatus"
     }
    ],
    "default": "active"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "TaxFeeCalculationCommandCenterSummary": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection; the headline tiles over the list, computed at read time for the filters in force",
  "description": "**The headline figures on Tax, Fee & Calculation Command Center.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.",
  "properties": {
   "activeTaxProfiles": {
    "type": "integer",
    "description": "Active Tax Profiles"
   },
   "taxJurisdictions": {
    "type": "integer",
    "description": "Tax Jurisdictions"
   },
   "activeFeeProfiles": {
    "type": "integer",
    "description": "Active Fee Profiles"
   },
   "activeSurcharges": {
    "type": "integer",
    "description": "Active Surcharges"
   },
   "exemptionRules": {
    "type": "integer",
    "description": "Exemption Rules"
   },
   "calculationProfiles": {
    "type": "integer",
    "description": "Calculation Profiles"
   },
   "productsMissingTax": {
    "type": "integer",
    "description": "Products Missing Tax: active products with no applicable tax profile"
   },
   "productsMissingCalculationProfile": {
    "type": "integer",
    "description": "Products Missing Calculation Profile"
   },
   "configurationConflicts": {
    "type": "integer",
    "description": "Configuration Conflicts"
   },
   "upcomingTaxChanges": {
    "type": "integer",
    "description": "Upcoming Tax Changes"
   },
   "validationIssues": {
    "type": "integer",
    "description": "Validation Issues"
   },
   "recentlyModifiedRules": {
    "type": "integer",
    "description": "Recently Modified Rules: changed in the last 7 days (decided 29 September, readiness close-out)"
   },
   "alerts": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Alerts (pp.39-40), e.g. \"14 active products have no applicable VAT profile\""
   },
   "aiInsights": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "AI observations for this screen; advisory only, never applied automatically"
   }
  }
 },
 "TaxFeeCalculationCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Tax, Fee & Calculation Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "profileName": {
    "type": "string",
    "description": "Profile Name"
   },
   "type": {
    "type": "string",
    "enum": [
     "tax",
     "fee",
     "surcharge",
     "waiver",
     "exemption",
     "calculationProfile",
     "roundingProfile"
    ],
    "description": "Configuration Type (p.39)"
   },
   "country": {
    "type": "string",
    "description": "Country"
   },
   "legalEntity": {
    "type": "string",
    "description": "Legal Entity"
   },
   "market": {
    "type": "string",
    "description": "Market"
   },
   "currency": {
    "type": "string",
    "description": "Currency: ISO 4217 code",
    "pattern": "^[A-Z]{3}$"
   },
   "productScope": {
    "type": "string",
    "description": "Product Scope"
   },
   "status": {
    "type": "string",
    "description": "Status: draft, active, inactive or expired"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   },
   "profileId": {
    "type": "string",
    "description": "ID of the tax profile, fee, rule or profile"
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date",
    "description": "Effective From"
   },
   "effectiveTo": {
    "type": "string",
    "format": "date",
    "description": "Effective To; empty for open-ended",
    "nullable": true
   }
  }
 },
 "TaxProfileJurisdictionConfigurationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Tax Profile & Jurisdiction Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "taxProfileName": {
    "type": "string",
    "description": "Tax Profile Name"
   },
   "taxProfileCode": {
    "type": "string",
    "description": "Tax Profile Code"
   },
   "taxType": {
    "type": "string",
    "enum": [
     "vat",
     "gst",
     "salesTax",
     "entertainmentTax",
     "tourismTax",
     "municipalityTax",
     "serviceTax",
     "customRegulatoryTax"
    ],
    "description": "Tax Type (pp.40-41)"
   },
   "country": {
    "type": "string",
    "description": "Country: ISO 3166-1 alpha-2 code",
    "pattern": "^[A-Z]{2}$"
   },
   "jurisdiction": {
    "type": "string",
    "description": "Region/Jurisdiction"
   },
   "legalEntity": {
    "type": "string",
    "description": "Legal Entity"
   },
   "taxRegistrationNumber": {
    "type": "string",
    "description": "Tax Registration Number"
   },
   "currency": {
    "type": "string",
    "description": "Currency: ISO 4217 code",
    "pattern": "^[A-Z]{3}$"
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date",
    "description": "Effective From; new structures are future-dated and never change historical transactions"
   },
   "effectiveTo": {
    "type": "string",
    "format": "date",
    "description": "Effective To; empty for open-ended",
    "nullable": true
   },
   "status": {
    "type": "string",
    "description": "Status: draft, active, inactive or expired"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   },
   "ratePercent": {
    "type": "number",
    "nullable": true,
    "description": "Rate in percent (UAE VAT 5); empty when the tax is a fixed amount set on the tax rule"
   },
   "taxProfileId": {
    "type": "string",
    "description": "Tax profile ID; empty on create"
   },
   "jurisdictionLevel": {
    "type": "string",
    "enum": [
     "country",
     "region",
     "municipality"
    ],
    "description": "Jurisdiction Hierarchy (p.41): the level this profile applies at"
   },
   "applicability": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "level": {
       "type": "string",
       "enum": [
        "legalEntity",
        "country",
        "market",
        "venue",
        "productCategory",
        "product",
        "service",
        "channel"
       ]
      },
      "refId": {
       "type": "string"
      }
     }
    },
    "description": "Applicability (p.41): where the profile applies; a channel only where legally applicable"
   },
   "taxBase": {
    "type": "string",
    "enum": [
     "discountedPrice",
     "preDiscountPrice"
    ],
    "description": "Which price the tax is computed on; preDiscountPrice where the jurisdiction taxes the full price before discount (MoM 1 Sep §4.5, e.g. Egypt). The client sets it per jurisdiction; discountedPrice is the default (decided 29 September, readiness close-out)"
   }
  }
 },
 "TaxProfileJurisdictionConfigurationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Tax Profile & Jurisdiction Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "taxProfileName": {
    "type": "string",
    "description": "Tax Profile Name"
   },
   "taxProfileCode": {
    "type": "string",
    "description": "Tax Profile Code"
   },
   "taxType": {
    "type": "string",
    "enum": [
     "vat",
     "gst",
     "salesTax",
     "entertainmentTax",
     "tourismTax",
     "municipalityTax",
     "serviceTax",
     "customRegulatoryTax"
    ],
    "description": "Tax Type (pp.40-41)"
   },
   "country": {
    "type": "string",
    "description": "Country: ISO 3166-1 alpha-2 code",
    "pattern": "^[A-Z]{2}$"
   },
   "jurisdiction": {
    "type": "string",
    "description": "Region/Jurisdiction"
   },
   "legalEntity": {
    "type": "string",
    "description": "Legal Entity"
   },
   "taxRegistrationNumber": {
    "type": "string",
    "description": "Tax Registration Number"
   },
   "currency": {
    "type": "string",
    "description": "Currency: ISO 4217 code",
    "pattern": "^[A-Z]{3}$"
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date",
    "description": "Effective From; new structures are future-dated and never change historical transactions"
   },
   "effectiveTo": {
    "type": "string",
    "format": "date",
    "description": "Effective To; empty for open-ended",
    "nullable": true
   },
   "status": {
    "type": "string",
    "description": "Status: draft, active, inactive or expired"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   },
   "ratePercent": {
    "type": "number",
    "nullable": true,
    "description": "Rate in percent (UAE VAT 5); empty when the tax is a fixed amount set on the tax rule"
   },
   "taxProfileId": {
    "type": "string",
    "description": "Tax profile ID; empty on create"
   },
   "jurisdictionLevel": {
    "type": "string",
    "enum": [
     "country",
     "region",
     "municipality"
    ],
    "description": "Jurisdiction Hierarchy (p.41): the level this profile applies at"
   },
   "applicability": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "level": {
       "type": "string",
       "enum": [
        "legalEntity",
        "country",
        "market",
        "venue",
        "productCategory",
        "product",
        "service",
        "channel"
       ]
      },
      "refId": {
       "type": "string"
      }
     }
    },
    "description": "Applicability (p.41): where the profile applies; a channel only where legally applicable"
   },
   "taxBase": {
    "type": "string",
    "enum": [
     "discountedPrice",
     "preDiscountPrice"
    ],
    "description": "Which price the tax is computed on; preDiscountPrice where the jurisdiction taxes the full price before discount (MoM 1 Sep §4.5, e.g. Egypt). The client sets it per jurisdiction; discountedPrice is the default (decided 29 September, readiness close-out)"
   },
   "consumingProductCount": {
    "type": "integer",
    "description": "Dependencies: products using the profile; read-only"
   },
   "consumingVenueCount": {
    "type": "integer",
    "description": "Dependencies: venues using the profile; read-only"
   }
  }
 },
 "TaxRuleTreatmentBuilderInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Tax Rule & Treatment Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "product": {
    "type": "string",
    "nullable": true,
    "description": "Condition: product; empty for any"
   },
   "productCategory": {
    "type": "string",
    "nullable": true,
    "description": "Condition: product category; empty for any"
   },
   "venue": {
    "type": "string",
    "nullable": true,
    "description": "Condition: venue; empty for any"
   },
   "country": {
    "type": "string",
    "nullable": true,
    "pattern": "^[A-Z]{2}$",
    "description": "Condition: country; empty for any"
   },
   "legalEntity": {
    "type": "string",
    "nullable": true,
    "description": "Condition: legal entity; empty for any"
   },
   "transactionType": {
    "type": "string",
    "nullable": true,
    "description": "Condition: transaction type (sale, refund, amendment, ...); empty for any"
   },
   "customerType": {
    "type": "string",
    "nullable": true,
    "description": "Condition: customer type, only where legally relevant"
   },
   "salesChannel": {
    "$ref": "../shared/common.yaml#/components/schemas/SalesChannel",
    "description": "Condition: sales channel, only where legally relevant; empty for any"
   },
   "taxRuleId": {
    "type": "string",
    "description": "Tax rule ID; empty on create"
   },
   "ruleName": {
    "type": "string",
    "description": "Rule name"
   },
   "treatment": {
    "type": "string",
    "enum": [
     "taxInclusive",
     "taxExclusive",
     "taxExempt",
     "zeroRated",
     "outOfScope"
    ],
    "description": "Tax Treatment (pp.41-42): inclusive (displayed price contains the tax) or exclusive (tax added on top), exempt, zero rated or out of scope"
   },
   "calculationMethod": {
    "type": "string",
    "enum": [
     "percentage",
     "fixedTax",
     "tiered",
     "compound",
     "sequential",
     "multipleConcurrent"
    ],
    "description": "Calculation Method (p.42)"
   },
   "taxes": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "taxProfileId": {
       "type": "string"
      },
      "sequence": {
       "type": "integer",
       "description": "Order of application (Base -> Entertainment Tax -> Municipality Fee -> VAT)"
      },
      "onPreviousTaxes": {
       "type": "boolean",
       "description": "Tax-on-tax: computed on the base plus the taxes before it (MoM 1 Sep §4.5)"
      },
      "fixedAmount": {
       "allOf": [
        {
         "$ref": "../shared/common.yaml#/components/schemas/Money"
        }
       ],
       "nullable": true,
       "description": "Amount when the method is fixedTax"
      }
     }
    },
    "description": "The tax profiles applied, in configurable sequence (Multiple Taxes, pp.42-43)"
   },
   "tiers": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "fromAmount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "ratePercent": {
       "type": "number"
      }
     }
    },
    "description": "Tiers when the method is tiered; empty otherwise"
   },
   "exemptionRuleIds": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Approved exemption conditions this rule honours (Screen 10.3.6, ADM-073)"
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date",
    "description": "Effective From"
   },
   "effectiveTo": {
    "type": "string",
    "format": "date",
    "description": "Effective To; empty for open-ended",
    "nullable": true
   },
   "status": {
    "type": "string",
    "description": "Status: draft, active, inactive or expired"
   }
  }
 },
 "TaxRuleTreatmentBuilderView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Tax Rule & Treatment Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "product": {
    "type": "string",
    "nullable": true,
    "description": "Condition: product; empty for any"
   },
   "productCategory": {
    "type": "string",
    "nullable": true,
    "description": "Condition: product category; empty for any"
   },
   "venue": {
    "type": "string",
    "nullable": true,
    "description": "Condition: venue; empty for any"
   },
   "country": {
    "type": "string",
    "nullable": true,
    "pattern": "^[A-Z]{2}$",
    "description": "Condition: country; empty for any"
   },
   "legalEntity": {
    "type": "string",
    "nullable": true,
    "description": "Condition: legal entity; empty for any"
   },
   "transactionType": {
    "type": "string",
    "nullable": true,
    "description": "Condition: transaction type (sale, refund, amendment, ...); empty for any"
   },
   "customerType": {
    "type": "string",
    "nullable": true,
    "description": "Condition: customer type, only where legally relevant"
   },
   "salesChannel": {
    "$ref": "../shared/common.yaml#/components/schemas/SalesChannel",
    "description": "Condition: sales channel, only where legally relevant; empty for any"
   },
   "taxRuleId": {
    "type": "string",
    "description": "Tax rule ID; empty on create"
   },
   "ruleName": {
    "type": "string",
    "description": "Rule name"
   },
   "treatment": {
    "type": "string",
    "enum": [
     "taxInclusive",
     "taxExclusive",
     "taxExempt",
     "zeroRated",
     "outOfScope"
    ],
    "description": "Tax Treatment (pp.41-42): inclusive (displayed price contains the tax) or exclusive (tax added on top), exempt, zero rated or out of scope"
   },
   "calculationMethod": {
    "type": "string",
    "enum": [
     "percentage",
     "fixedTax",
     "tiered",
     "compound",
     "sequential",
     "multipleConcurrent"
    ],
    "description": "Calculation Method (p.42)"
   },
   "taxes": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "taxProfileId": {
       "type": "string"
      },
      "sequence": {
       "type": "integer",
       "description": "Order of application (Base -> Entertainment Tax -> Municipality Fee -> VAT)"
      },
      "onPreviousTaxes": {
       "type": "boolean",
       "description": "Tax-on-tax: computed on the base plus the taxes before it (MoM 1 Sep §4.5)"
      },
      "fixedAmount": {
       "allOf": [
        {
         "$ref": "../shared/common.yaml#/components/schemas/Money"
        }
       ],
       "nullable": true,
       "description": "Amount when the method is fixedTax"
      }
     }
    },
    "description": "The tax profiles applied, in configurable sequence (Multiple Taxes, pp.42-43)"
   },
   "tiers": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "fromAmount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "ratePercent": {
       "type": "number"
      }
     }
    },
    "description": "Tiers when the method is tiered; empty otherwise"
   },
   "exemptionRuleIds": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Approved exemption conditions this rule honours (Screen 10.3.6, ADM-073)"
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date",
    "description": "Effective From"
   },
   "effectiveTo": {
    "type": "string",
    "format": "date",
    "description": "Effective To; empty for open-ended",
    "nullable": true
   },
   "status": {
    "type": "string",
    "description": "Status: draft, active, inactive or expired"
   }
  }
 }
}
```
