# WS53 — Promotions   Bundles Management board 9

**10 screens · 10 operations · 13 schemas · 2 permissions**

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

- **Every control that can be refused must be gated.** 2 permissions apply here:
  `PRICE_CONFIGURE, PRICE_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **0 of these operations work offline**
  
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-218` | Campaign Governance & Budget Command Center | commandCentre | 1 | 0 | — |
| `ADM-219` | Campaign Budget & Financial Limit Setup | configEditor | 1 | 0 | — |
| `ADM-220` | Redemption, Discount & Exposure Limit Manager | configEditor | 1 | 0 | — |
| `ADM-221` | Budget Consumption & Forecast Monitor | listDetail | 1 | 0 | — |
| `ADM-222` | Threshold Actions & Automatic Suspension | listDetail | 1 | 4 | — |
| `ADM-223` | Campaign Approval Workflow Designer | listDetail | 1 | 0 | — |
| `ADM-224` | Approval Inbox & Decision Workspace | listDetail | 1 | 0 | — |
| `ADM-225` | Campaign Financial & Commercial Simulator | listDetail | 1 | 0 | — |
| `ADM-226` | Campaign Experiment & A/B Test Manager | listDetail | 1 | 0 | — |
| `ADM-227` | Governance Audit, AI Risk & Launch Readiness | configEditor | 1 | 0 | — |

## Thin screens in this batch

**ADM-221, ADM-224, ADM-225, ADM-226, ADM-227 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-218",
  "name": "Campaign Governance & Budget Command Center",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "9",
   "number": "1",
   "page": 125
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/campaign-governance-budget-command-center-adm-218",
   "component": "apps/ticvai-web/src/routes/commercial/CampaignGovernanceBudgetCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-219",
    "ADM-220",
    "ADM-221",
    "ADM-222",
    "ADM-223",
    "ADM-224",
    "ADM-225",
    "ADM-226",
    "ADM-227"
   ],
   "inferred": false,
   "notes": "**The board's hub.** The workshop specified this module as boards of ten and opened each with a command centre; the other nine screens are that board's detail, so they are reached from here and return here.",
   "transitions": [
    {
     "to": "ADM-002",
     "trigger": "Platform Dashboard",
     "carries": [
      "tenantId"
     ],
     "provenance": "derived — ADM-002 declares entryState.params tenantId, so an edge into it must carry them"
    },
    {
     "to": "ADM-219",
     "trigger": "Works in Campaign Budget & Financial Limit Setup",
     "provenance": "flow F162 step 1→2",
     "operation": "listCampaignGovernanceBudget"
    },
    {
     "to": "ADM-220",
     "trigger": "Works in Redemption, Discount & Exposure Limit Manager",
     "provenance": "flow F162 step 3→4",
     "operation": "listCampaignGovernanceBudget"
    },
    {
     "to": "ADM-221",
     "trigger": "Works in Budget Consumption & Forecast Monitor",
     "provenance": "flow F162 step 5→6",
     "operation": "listCampaignGovernanceBudget"
    },
    {
     "to": "ADM-222",
     "trigger": "Works in Threshold Actions & Automatic Suspension",
     "provenance": "flow F162 step 7→8",
     "operation": "listCampaignGovernanceBudget"
    },
    {
     "to": "ADM-223",
     "trigger": "Works in Campaign Approval Workflow Designer",
     "provenance": "flow F162 step 9→10",
     "operation": "listCampaignGovernanceBudget"
    },
    {
     "to": "ADM-224",
     "trigger": "Works in Approval Inbox & Decision Workspace",
     "provenance": "flow F162 step 11→12",
     "operation": "listCampaignGovernanceBudget"
    },
    {
     "to": "ADM-225",
     "trigger": "Works in Campaign Financial & Commercial Simulator",
     "provenance": "flow F162 step 13→14",
     "operation": "listCampaignGovernanceBudget"
    },
    {
     "to": "ADM-226",
     "trigger": "Works in Campaign Experiment & A/B Test Manager",
     "provenance": "flow F162 step 15→16",
     "operation": "listCampaignGovernanceBudget"
    },
    {
     "to": "ADM-227",
     "trigger": "Works in Governance Audit, AI Risk & Launch Readiness",
     "provenance": "flow F162 step 17→18",
     "operation": "listCampaignGovernanceBudget"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide executives, Marketing, Commercial, Revenue, and Finance with one centralized view of the financial and governance status of promotional campaigns.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Active Campaigns",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 125 §KPI Cards",
       "bindsTo": "CampaignGovernanceBudgetCommandCenterView.activeCampaigns"
      },
      {
       "kind": "metricTile",
       "label": "Campaign Budget",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 125 §KPI Cards",
       "bindsTo": "CampaignGovernanceBudgetCommandCenterView.campaignBudget"
      },
      {
       "kind": "metricTile",
       "label": "Budget Consumed",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 125 §KPI Cards",
       "bindsTo": "CampaignGovernanceBudgetCommandCenterView.budgetConsumed"
      },
      {
       "kind": "metricTile",
       "label": "Remaining Budget",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 125 §KPI Cards",
       "bindsTo": "CampaignGovernanceBudgetCommandCenterView.remainingBudget"
      },
      {
       "kind": "metricTile",
       "label": "Discount Exposure",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 125 §KPI Cards",
       "bindsTo": "CampaignGovernanceBudgetCommandCenterView.discountExposure"
      },
      {
       "kind": "metricTile",
       "label": "Redemption Value",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 125 §KPI Cards",
       "bindsTo": "CampaignGovernanceBudgetCommandCenterView.redemptionValue"
      },
      {
       "kind": "metricTile",
       "label": "Revenue Generated",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 125 §KPI Cards",
       "bindsTo": "CampaignGovernanceBudgetCommandCenterView.revenueGenerated"
      },
      {
       "kind": "metricTile",
       "label": "Incremental Revenue",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 125 §KPI Cards",
       "bindsTo": "CampaignGovernanceBudgetCommandCenterView.incrementalRevenue"
      },
      {
       "kind": "metricTile",
       "label": "Campaign ROI",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 125 §KPI Cards",
       "bindsTo": "CampaignGovernanceBudgetCommandCenterView.campaignRoi"
      },
      {
       "kind": "metricTile",
       "label": "Campaigns Near Budget Limit",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 125 §KPI Cards",
       "bindsTo": "CampaignGovernanceBudgetCommandCenterView.campaignsNearBudgetLimit"
      },
      {
       "kind": "metricTile",
       "label": "Pending Approvals",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 125 §KPI Cards",
       "bindsTo": "CampaignGovernanceBudgetCommandCenterView.pendingApprovals"
      },
      {
       "kind": "metricTile",
       "label": "Suspended Campaigns",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 125 §KPI Cards",
       "bindsTo": "CampaignGovernanceBudgetCommandCenterView.suspendedCampaigns"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The campaign governance budget list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the campaign governance budget untouched.",
   "emptyFirstRun": "No campaign governance budget yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the campaign governance budget are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCampaignGovernanceBudget",
    "contract": "promotions",
    "purpose": "Campaign Governance & Budget Command Center",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "CampaignGovernanceBudgetCommandCenterView.activeCampaigns",
    "CampaignGovernanceBudgetCommandCenterView.campaignBudget",
    "CampaignGovernanceBudgetCommandCenterView.budgetConsumed",
    "CampaignGovernanceBudgetCommandCenterView.remainingBudget",
    "CampaignGovernanceBudgetCommandCenterView.discountExposure",
    "CampaignGovernanceBudgetCommandCenterView.redemptionValue"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-218"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 125. 12 of 12 labels bound to a contract property; 12 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-219",
  "name": "Campaign Budget & Financial Limit Setup",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "9",
   "number": "2",
   "page": 126
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/campaign-budget-financial-limit-setup-adm-219",
   "component": "apps/ticvai-web/src/routes/commercial/CampaignBudgetFinancialLimitSetup.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-218"
   ],
   "exitTo": [
    "ADM-218"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-218, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-218",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F162 step 2→3",
     "operation": "setCampaignBudgetFinancial"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configuration) and no display directory — it is settings, not a population",
  "purpose": "Define the financial envelope within which a campaign is permitted to operate.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Total campaign budget. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 126 §Support"
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
       "label": "Campaign",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 126 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Budget amount",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 126 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Currency",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 126 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Effective dates",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 126 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Budget owner",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 126 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Cost center",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 126 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Business entity",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 126 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 126 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Department",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 126 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Funding source",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 126 §Configuration"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Total campaign budget",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 126 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The campaign budget financial configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the campaign budget financial untouched.",
   "emptyFirstRun": "No campaign budget financial configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setCampaignBudgetFinancial",
    "contract": "promotions",
    "purpose": "Campaign Budget & Financial Limit Setup",
    "trigger": "onAction",
    "invalidates": [
     "setCampaignBudgetFinancial"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-219"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 126. 0 of 0 labels bound to a contract property; 11 of 31 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-220",
  "name": "Redemption, Discount & Exposure Limit Manager",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "9",
   "number": "3",
   "page": 128
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/redemption-discount-exposure-limit-manager-adm-220",
   "component": "apps/ticvai-web/src/routes/commercial/RedemptionDiscountExposureLimitManager.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-218"
   ],
   "exitTo": [
    "ADM-218"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-218, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-218",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F162 step 4→5",
     "operation": "listRedemptionDiscountExposure"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Define non-budget commercial limits controlling campaign exposure.",
  "gaps": [
   {
    "operation": null,
    "why": "**Redemption, Discount & Exposure Limit Manager declares no operation that writes anything** — its only declared call is `listRedemptionDiscountExposure`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
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
       "label": "50%",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 128 §Configure"
      },
      {
       "kind": "selectField",
       "label": "75%",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 128 §Configure"
      },
      {
       "kind": "selectField",
       "label": "90%",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 128 §Configure"
      },
      {
       "kind": "selectField",
       "label": "95%",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 128 §Configure"
      },
      {
       "kind": "selectField",
       "label": "100%",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 128 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The redemption discount exposure configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the redemption discount exposure untouched.",
   "emptyFirstRun": "No redemption discount exposure configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listRedemptionDiscountExposure",
    "contract": "promotions",
    "purpose": "Redemption, Discount & Exposure Limit Manager",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-220"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 128. 0 of 0 labels bound to a contract property; 5 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-221",
  "name": "Budget Consumption & Forecast Monitor",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "9",
   "number": "4",
   "page": 129
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/budget-consumption-forecast-monitor-adm-221",
   "component": "apps/ticvai-web/src/routes/commercial/BudgetConsumptionForecastMonitor.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-218"
   ],
   "exitTo": [
    "ADM-218"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-218, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-218",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F162 step 6→7",
     "operation": "listBudgetConsumptionForecast"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide real-time tracking of campaign financial consumption and predict when limits will be reached.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every budget consumption forecast",
       "columns": [
        "BudgetConsumptionForecastMonitorView.originalBudget",
        "BudgetConsumptionForecastMonitorView.consumed",
        "BudgetConsumptionForecastMonitorView.committed",
        "BudgetConsumptionForecastMonitorView.reserved",
        "BudgetConsumptionForecastMonitorView.remaining",
        "BudgetConsumptionForecastMonitorView.forecastFinalSpend",
        "BudgetConsumptionForecastMonitorView.dailyBurnRate"
       ],
       "bindsTo": "BudgetConsumptionForecastMonitorView",
       "operation": "listBudgetConsumptionForecast",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 129 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected budget consumption forecast",
       "bindsTo": "BudgetConsumptionForecastMonitorView",
       "columns": [
        "BudgetConsumptionForecastMonitorView.originalBudget",
        "BudgetConsumptionForecastMonitorView.consumed",
        "BudgetConsumptionForecastMonitorView.committed",
        "BudgetConsumptionForecastMonitorView.reserved",
        "BudgetConsumptionForecastMonitorView.remaining",
        "BudgetConsumptionForecastMonitorView.forecastFinalSpend",
        "BudgetConsumptionForecastMonitorView.dailyBurnRate"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Consumed”, “Reserved”, “Committed”, “Remaining campaign”.",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 129 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The budget consumption forecast list.",
   "error": "Could not load. Names which read failed and leaves the budget consumption forecast untouched.",
   "emptyFirstRun": "No budget consumption forecast yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the budget consumption forecast are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listBudgetConsumptionForecast",
    "contract": "promotions",
    "purpose": "Budget Consumption & Forecast Monitor",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "BudgetConsumptionForecastMonitorView.originalBudget",
    "BudgetConsumptionForecastMonitorView.consumed",
    "BudgetConsumptionForecastMonitorView.committed",
    "BudgetConsumptionForecastMonitorView.reserved",
    "BudgetConsumptionForecastMonitorView.remaining",
    "BudgetConsumptionForecastMonitorView.forecastFinalSpend"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-221"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 129. 7 of 7 labels bound to a contract property; 7 of 15 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-222",
  "name": "Threshold Actions & Automatic Suspension",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "9",
   "number": "5",
   "page": 130
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/threshold-actions-automatic-suspension-adm-222",
   "component": "apps/ticvai-web/src/routes/commercial/ThresholdActionsAutomaticSuspension.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-218"
   ],
   "exitTo": [
    "ADM-218"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-218, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-218",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F162 step 8→9",
     "operation": "listThresholdActionAutomatic"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Define what TICVAI should do as financial or redemption thresholds are approached or exceeded. This is explicitly required by the matrix.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 10 actions on this screen and the screen declares 1 operation.** Unserved: Notify, Warn, Require approval, Reduce allocation, Stop specific channel, Stop partner, Stop promotion, Stop campaign …. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 130 §Available Actions"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 130"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 130"
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
       "label": "Notify",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 130 §Available Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Warn",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 130 §Available Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Require approval",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 130 §Available Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Reduce allocation",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 130 §Available Actions"
      },
      {
       "kind": "destructiveButton",
       "label": "Stop specific channel",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 130 §Available Actions"
      },
      {
       "kind": "destructiveButton",
       "label": "Stop partner",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 130 §Available Actions"
      },
      {
       "kind": "destructiveButton",
       "label": "Stop promotion",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 130 §Available Actions"
      },
      {
       "kind": "destructiveButton",
       "label": "Stop campaign",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 130 §Available Actions"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": []
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmStopSpecificChannel",
    "component": "confirmDialog",
    "trigger": "Stop specific channel",
    "body": "**Stop specific channel on a threshold actions automatic is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 130 §Available Actions"
   },
   {
    "id": "confirmStopPartner",
    "component": "confirmDialog",
    "trigger": "Stop partner",
    "body": "**Stop partner on a threshold actions automatic is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 130 §Available Actions"
   },
   {
    "id": "confirmStopPromotion",
    "component": "confirmDialog",
    "trigger": "Stop promotion",
    "body": "**Stop promotion on a threshold actions automatic is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 130 §Available Actions"
   },
   {
    "id": "confirmStopCampaign",
    "component": "confirmDialog",
    "trigger": "Stop campaign",
    "body": "**Stop campaign on a threshold actions automatic is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 130 §Available Actions"
   }
  ],
  "states": {
   "loading": "The threshold actions automatic list.",
   "error": "Could not load. Names which read failed and leaves the threshold actions automatic untouched.",
   "emptyFirstRun": "No threshold actions automatic yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the threshold actions automatic are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listThresholdActionAutomatic",
    "contract": "promotions",
    "purpose": "Threshold Actions & Automatic Suspension",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "ThresholdActionsAutomaticSuspensionView.warn",
    "ThresholdActionsAutomaticSuspensionView.requireApproval",
    "ThresholdActionsAutomaticSuspensionView.reduceAllocation",
    "ThresholdActionsAutomaticSuspensionView.stopSpecificChannel",
    "ThresholdActionsAutomaticSuspensionView.stopPartner"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-222"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 130. 0 of 0 labels bound to a contract property; 10 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-223",
  "name": "Campaign Approval Workflow Designer",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "9",
   "number": "6",
   "page": 131
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/campaign-approval-workflow-designer-adm-223",
   "component": "apps/ticvai-web/src/routes/commercial/CampaignApprovalWorkflowDesigner.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-218"
   ],
   "exitTo": [
    "ADM-218"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-218, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-218",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F162 step 10→11",
     "operation": "approveCampaignWorkflow"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure multi-level approval workflows for promotions and campaigns. The matrix explicitly requires configurable multi-level approval for promotion creation, modification, activation, and deactivation.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 5 actions on this screen and the screen declares 1 operation.** Unserved: Sequential approval, Parallel approval, Conditional approval, Mandatory approval, Optional review. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 131 §Support"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 131"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 131"
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
       "label": "Sequential approval",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 131 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Parallel approval",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 131 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Conditional approval",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 131 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Mandatory approval",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 131 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Optional review",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 131 §Support"
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
   "loading": "The campaign approval workflow list.",
   "error": "Could not load. Names which read failed and leaves the campaign approval workflow untouched.",
   "emptyFirstRun": "No campaign approval workflow yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the campaign approval workflow are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "approveCampaignWorkflow",
    "contract": "promotions",
    "purpose": "Campaign Approval Workflow Designer",
    "trigger": "onAction",
    "invalidates": [
     "approveCampaignWorkflow"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-223"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 131. 0 of 0 labels bound to a contract property; 5 of 36 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-224",
  "name": "Approval Inbox & Decision Workspace",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "9",
   "number": "7",
   "page": 132
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/approval-inbox-decision-workspace-adm-224",
   "component": "apps/ticvai-web/src/routes/commercial/ApprovalInboxDecisionWorkspace.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-218"
   ],
   "exitTo": [
    "ADM-218"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-218, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-218",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F162 step 12→13",
     "operation": "approveDecision"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Provide approvers with enough commercial information to make an informed decision without navigating through every configuration screen.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every approval decision",
       "columns": [
        "ApprovalInboxDecisionWorkspaceView.campaign",
        "ApprovalInboxDecisionWorkspaceView.promotion",
        "ApprovalInboxDecisionWorkspaceView.requestedBy",
        "ApprovalInboxDecisionWorkspaceView.requestDate",
        "ApprovalInboxDecisionWorkspaceView.requestedAction",
        "ApprovalInboxDecisionWorkspaceView.discount",
        "ApprovalInboxDecisionWorkspaceView.budget",
        "ApprovalInboxDecisionWorkspaceView.estimatedRedemptions",
        "ApprovalInboxDecisionWorkspaceView.estimatedRevenue",
        "ApprovalInboxDecisionWorkspaceView.marginImpact",
        "ApprovalInboxDecisionWorkspaceView.customerReach",
        "ApprovalInboxDecisionWorkspaceView.riskLevel",
        "ApprovalInboxDecisionWorkspaceView.aiForecast"
       ],
       "bindsTo": "ApprovalInboxDecisionWorkspaceView",
       "operation": "approveDecision",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 132 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected approval decision",
       "bindsTo": "ApprovalInboxDecisionWorkspaceView",
       "columns": [
        "ApprovalInboxDecisionWorkspaceView.campaign",
        "ApprovalInboxDecisionWorkspaceView.promotion",
        "ApprovalInboxDecisionWorkspaceView.requestedBy",
        "ApprovalInboxDecisionWorkspaceView.requestDate",
        "ApprovalInboxDecisionWorkspaceView.requestedAction",
        "ApprovalInboxDecisionWorkspaceView.discount",
        "ApprovalInboxDecisionWorkspaceView.budget",
        "ApprovalInboxDecisionWorkspaceView.estimatedRedemptions",
        "ApprovalInboxDecisionWorkspaceView.estimatedRevenue",
        "ApprovalInboxDecisionWorkspaceView.marginImpact",
        "ApprovalInboxDecisionWorkspaceView.customerReach",
        "ApprovalInboxDecisionWorkspaceView.riskLevel",
        "ApprovalInboxDecisionWorkspaceView.aiForecast"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Current”, “Discount”, “Budget”, “Duration”, “Approver Actions”, “Comments”.",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 132 §Show"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Approve",
       "provenance": "contract operation approveDecision"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The approval decision list.",
   "error": "Could not load. Names which read failed and leaves the approval decision untouched.",
   "emptyFirstRun": "No approval decision yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the approval decision are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "approveDecision",
    "contract": "promotions",
    "purpose": "Approval Inbox & Decision Workspace",
    "trigger": "onAction",
    "invalidates": [
     "approveDecision"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "ApprovalInboxDecisionWorkspaceView.campaign",
    "ApprovalInboxDecisionWorkspaceView.promotion",
    "ApprovalInboxDecisionWorkspaceView.requestedBy",
    "ApprovalInboxDecisionWorkspaceView.requestDate",
    "ApprovalInboxDecisionWorkspaceView.requestedAction",
    "ApprovalInboxDecisionWorkspaceView.discount"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-224"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 132. 13 of 13 labels bound to a contract property; 13 of 27 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-225",
  "name": "Campaign Financial & Commercial Simulator",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "9",
   "number": "8",
   "page": 133
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/campaign-financial-commercial-simulator-adm-225",
   "component": "apps/ticvai-web/src/routes/commercial/CampaignFinancialCommercialSimulator.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-218"
   ],
   "exitTo": [
    "ADM-218"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-218, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-218",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F162 step 14→15",
     "operation": "listCampaignFinancialCommercial"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Simulate the likely financial result of a campaign before activation. This is a major matrix requirement.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every campaign financial commercial",
       "columns": [
        "CampaignFinancialCommercialSimulatorView.eligibleAudience",
        "CampaignFinancialCommercialSimulatorView.expectedTransactions",
        "CampaignFinancialCommercialSimulatorView.expectedRedemptions",
        "CampaignFinancialCommercialSimulatorView.grossRevenue",
        "CampaignFinancialCommercialSimulatorView.discountCost",
        "CampaignFinancialCommercialSimulatorView.netRevenue",
        "CampaignFinancialCommercialSimulatorView.incrementalRevenue",
        "CampaignFinancialCommercialSimulatorView.averageOrderValue",
        "CampaignFinancialCommercialSimulatorView.grossMargin",
        "CampaignFinancialCommercialSimulatorView.marginImpact",
        "CampaignFinancialCommercialSimulatorView.expectedBudgetConsumption",
        "CampaignFinancialCommercialSimulatorView.roi"
       ],
       "bindsTo": "CampaignFinancialCommercialSimulatorView",
       "operation": "listCampaignFinancialCommercial",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 133 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected campaign financial commercial",
       "bindsTo": "CampaignFinancialCommercialSimulatorView",
       "columns": [
        "CampaignFinancialCommercialSimulatorView.eligibleAudience",
        "CampaignFinancialCommercialSimulatorView.expectedTransactions",
        "CampaignFinancialCommercialSimulatorView.expectedRedemptions",
        "CampaignFinancialCommercialSimulatorView.grossRevenue",
        "CampaignFinancialCommercialSimulatorView.discountCost",
        "CampaignFinancialCommercialSimulatorView.netRevenue",
        "CampaignFinancialCommercialSimulatorView.incrementalRevenue",
        "CampaignFinancialCommercialSimulatorView.averageOrderValue",
        "CampaignFinancialCommercialSimulatorView.grossMargin",
        "CampaignFinancialCommercialSimulatorView.marginImpact",
        "CampaignFinancialCommercialSimulatorView.expectedBudgetConsumption",
        "CampaignFinancialCommercialSimulatorView.roi"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Simulation Inputs”, “Scenario ROI”, “Historical Replay”.",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 133 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The campaign financial commercial list.",
   "error": "Could not load. Names which read failed and leaves the campaign financial commercial untouched.",
   "emptyFirstRun": "No campaign financial commercial yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the campaign financial commercial are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCampaignFinancialCommercial",
    "contract": "promotions",
    "purpose": "Campaign Financial & Commercial Simulator",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "CampaignFinancialCommercialSimulatorView.eligibleAudience",
    "CampaignFinancialCommercialSimulatorView.expectedTransactions",
    "CampaignFinancialCommercialSimulatorView.expectedRedemptions",
    "CampaignFinancialCommercialSimulatorView.grossRevenue",
    "CampaignFinancialCommercialSimulatorView.discountCost",
    "CampaignFinancialCommercialSimulatorView.netRevenue"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-225"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 133. 12 of 12 labels bound to a contract property; 12 of 36 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-226",
  "name": "Campaign Experiment & A/B Test Manager",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "9",
   "number": "9",
   "page": 134
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/campaign-experiment-a-b-test-manager-adm-226",
   "component": "apps/ticvai-web/src/routes/commercial/CampaignExperimentABTestManager.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-218"
   ],
   "exitTo": [
    "ADM-218"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-218, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-218",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F162 step 16→17",
     "operation": "listCampaignExperimentTest"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Measure) and no metric row",
  "purpose": "Allow TICVAI to test campaign variants and determine which commercial strategy performs better. The matrix explicitly requires A/B testing of promotion variants, including discount levels, validity periods, bundles, and target segments.",
  "gaps": [
   {
    "operation": null,
    "why": "**Campaign Experiment & A/B Test Manager declares no operation that writes anything** — its only declared call is `listCampaignExperimentTest`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
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
       "label": "Every campaign experiment test",
       "columns": [
        "CampaignExperimentABTestManagerView.conversion",
        "CampaignExperimentABTestManagerView.revenue",
        "CampaignExperimentABTestManagerView.aov",
        "CampaignExperimentABTestManagerView.redemption",
        "CampaignExperimentABTestManagerView.discountCost",
        "CampaignExperimentABTestManagerView.margin",
        "CampaignExperimentABTestManagerView.incrementalRevenue",
        "CampaignExperimentABTestManagerView.roi"
       ],
       "bindsTo": "CampaignExperimentABTestManagerView",
       "operation": "listCampaignExperimentTest",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 134 §Measure"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected campaign experiment test",
       "bindsTo": "CampaignExperimentABTestManagerView",
       "columns": [
        "CampaignExperimentABTestManagerView.conversion",
        "CampaignExperimentABTestManagerView.revenue",
        "CampaignExperimentABTestManagerView.aov",
        "CampaignExperimentABTestManagerView.redemption",
        "CampaignExperimentABTestManagerView.discountCost",
        "CampaignExperimentABTestManagerView.margin",
        "CampaignExperimentABTestManagerView.incrementalRevenue",
        "CampaignExperimentABTestManagerView.roi"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Variant A”, “Variant B”, “Variant C”, “Audience Allocation”, “Test”.",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 134 §Measure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The campaign experiment test list.",
   "error": "Could not load. Names which read failed and leaves the campaign experiment test untouched.",
   "emptyFirstRun": "No campaign experiment test yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the campaign experiment test are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCampaignExperimentTest",
    "contract": "promotions",
    "purpose": "Campaign Experiment & A/B Test Manager",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "CampaignExperimentABTestManagerView.conversion",
    "CampaignExperimentABTestManagerView.revenue",
    "CampaignExperimentABTestManagerView.aov",
    "CampaignExperimentABTestManagerView.redemption",
    "CampaignExperimentABTestManagerView.discountCost",
    "CampaignExperimentABTestManagerView.margin"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-226"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 134. 8 of 8 labels bound to a contract property; 8 of 33 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-227",
  "name": "Governance Audit, AI Risk & Launch Readiness",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "9",
   "number": "10",
   "page": 136
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/governance-audit-ai-risk-launch-readiness-adm-227",
   "component": "apps/ticvai-web/src/routes/commercial/GovernanceAuditAiRiskLaunchReadiness.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-218"
   ],
   "exitTo": [
    "ADM-218"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-218, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation."
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure commercial behavior) and no display directory — it is settings, not a population",
  "purpose": "Provide the final governance checkpoint before a campaign is allowed to go live.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "↓",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 136 §Configure commercial behavior"
      },
      {
       "kind": "textField",
       "label": "Board 9 — Governance",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 136 §Configure commercial behavior"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The governance audit risk configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the governance audit risk untouched.",
   "emptyFirstRun": "No governance audit risk configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listGovernanceRiskLaunch",
    "contract": "promotions",
    "purpose": "Governance Audit, AI Risk & Launch Readiness",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-227"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 136. 0 of 0 labels bound to a contract property; 2 of 102 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "approveCampaignWorkflow": {
  "method": "PUT",
  "path": "/campaign-workflow",
  "contract": "promotions",
  "summary": "Campaign Approval Workflow Designer",
  "permission": "PRICE_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "CampaignApprovalWorkflowDesignerInput",
  "responds": "CampaignApprovalWorkflowDesignerView"
 },
 "approveDecision": {
  "method": "PUT",
  "path": "/decision",
  "contract": "promotions",
  "summary": "Approval Inbox & Decision Workspace",
  "permission": "PRICE_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "ApprovalInboxDecisionWorkspaceInput",
  "responds": "ApprovalInboxDecisionWorkspaceView"
 },
 "listBudgetConsumptionForecast": {
  "method": "GET",
  "path": "/budget-consumption-forecast",
  "contract": "promotions",
  "summary": "Budget Consumption & Forecast Monitor",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "BudgetConsumptionForecastMonitorView"
 },
 "listCampaignExperimentTest": {
  "method": "GET",
  "path": "/campaign-experiment-test",
  "contract": "promotions",
  "summary": "Campaign Experiment & A/B Test Manager",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "CampaignExperimentABTestManagerView"
 },
 "listCampaignFinancialCommercial": {
  "method": "GET",
  "path": "/campaign-financial-commercial",
  "contract": "promotions",
  "summary": "Campaign Financial & Commercial Simulator",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "CampaignFinancialCommercialSimulatorView"
 },
 "listCampaignGovernanceBudget": {
  "method": "GET",
  "path": "/campaign-governance-budget",
  "contract": "promotions",
  "summary": "Campaign Governance & Budget Command Center",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "CampaignGovernanceBudgetCommandCenterView"
 },
 "listGovernanceRiskLaunch": {
  "method": "GET",
  "path": "/governance-risk-launch",
  "contract": "promotions",
  "summary": "Governance Audit, AI Risk & Launch Readiness",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "GovernanceAuditAiRiskLaunchReadinessView"
 },
 "listRedemptionDiscountExposure": {
  "method": "GET",
  "path": "/redemption-discount-exposure",
  "contract": "promotions",
  "summary": "Redemption, Discount & Exposure Limit Manager",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "RedemptionDiscountExposureLimitManagerView"
 },
 "listThresholdActionAutomatic": {
  "method": "GET",
  "path": "/threshold-action-automatic",
  "contract": "promotions",
  "summary": "Threshold Actions & Automatic Suspension",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ThresholdActionsAutomaticSuspensionView"
 },
 "setCampaignBudgetFinancial": {
  "method": "PUT",
  "path": "/campaign-budget-financial",
  "contract": "promotions",
  "summary": "Campaign Budget & Financial Limit Setup",
  "permission": "PRICE_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "CampaignBudgetFinancialLimitSetupInput",
  "responds": "CampaignBudgetFinancialLimitSetupView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "ApprovalInboxDecisionWorkspaceInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Approval Inbox & Decision Workspace submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "aed500kAed750k": {
    "type": "string",
    "description": "AED 500K → AED 750K"
   },
   "returnForChange": {
    "type": "string",
    "description": "Return for Change"
   },
   "requestInformation": {
    "type": "string",
    "description": "Request Information"
   },
   "delegate": {
    "type": "string",
    "description": "Delegate"
   }
  }
 },
 "ApprovalInboxDecisionWorkspaceView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Approval Inbox & Decision Workspace displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "campaign": {
    "type": "string",
    "description": "Campaign"
   },
   "promotion": {
    "type": "string",
    "description": "Promotion"
   },
   "requestedBy": {
    "type": "string",
    "description": "Requested by"
   },
   "requestDate": {
    "type": "string",
    "format": "date-time",
    "description": "Request date"
   },
   "requestedAction": {
    "type": "string",
    "description": "Requested action"
   },
   "discount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Discount"
   },
   "budget": {
    "type": "string",
    "description": "Budget"
   },
   "estimatedRedemptions": {
    "type": "integer",
    "description": "Estimated redemptions"
   },
   "estimatedRevenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Estimated revenue"
   },
   "marginImpact": {
    "type": "number",
    "description": "Margin impact"
   },
   "customerReach": {
    "type": "string",
    "description": "Customer reach"
   },
   "riskLevel": {
    "type": "string",
    "description": "Risk level"
   },
   "aiForecast": {
    "type": "string",
    "description": "AI forecast"
   },
   "aed500kAed750k": {
    "type": "string",
    "description": "AED 500K → AED 750K"
   },
   "returnForChange": {
    "type": "string",
    "description": "Return for Change"
   },
   "requestInformation": {
    "type": "string",
    "description": "Request Information"
   },
   "delegate": {
    "type": "string",
    "description": "Delegate"
   },
   "marketing": {
    "type": "string",
    "description": "Marketing ✓"
   },
   "commercial": {
    "type": "string",
    "description": "Commercial ✓"
   }
  }
 },
 "BudgetConsumptionForecastMonitorView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Budget Consumption & Forecast Monitor displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "originalBudget": {
    "type": "string",
    "description": "Original budget"
   },
   "consumed": {
    "type": "string",
    "description": "Consumed"
   },
   "committed": {
    "type": "string",
    "description": "Committed"
   },
   "reserved": {
    "type": "string",
    "description": "Reserved"
   },
   "remaining": {
    "type": "string",
    "description": "Remaining"
   },
   "forecastFinalSpend": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Forecast final spend"
   },
   "dailyBurnRate": {
    "type": "number",
    "description": "Daily burn rate"
   },
   "completedTransaction": {
    "type": "string",
    "description": "Completed transaction"
   }
  }
 },
 "CampaignApprovalWorkflowDesignerInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table covers these fields** — the closest is promotions.coupon_campaign at 6%, so this is not an update to anything the package stores today and no new table has been decided",
  "description": "**What Campaign Approval Workflow Designer submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "discount": {
    "type": "number",
    "description": "Discount %"
   },
   "campaignBudget": {
    "type": "string",
    "description": "Campaign budget"
   },
   "margin": {
    "type": "number",
    "description": "Margin"
   },
   "promotionType": {
    "type": "string",
    "description": "Promotion type"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "partner": {
    "type": "string",
    "description": "Partner"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "freeProductValue": {
    "type": "string",
    "description": "Free-product value"
   },
   "campaignDuration": {
    "type": "string",
    "format": "date-time",
    "description": "Campaign duration"
   },
   "financialExposure": {
    "type": "string",
    "description": "Financial exposure"
   },
   "discount1025": {
    "type": "number",
    "description": "Discount 10–25%"
   },
   "sequentialApproval": {
    "type": "string",
    "description": "Sequential approval"
   },
   "parallelApproval": {
    "type": "string",
    "description": "Parallel approval"
   },
   "conditionalApproval": {
    "type": "string",
    "description": "Conditional approval"
   },
   "mandatoryApproval": {
    "type": "string",
    "description": "Mandatory approval"
   },
   "optionalReview": {
    "type": "string",
    "description": "Optional review"
   },
   "delegation": {
    "type": "string",
    "description": "Delegation"
   },
   "escalation": {
    "type": "string",
    "description": "Escalation"
   }
  }
 },
 "CampaignApprovalWorkflowDesignerView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Campaign Approval Workflow Designer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "discount": {
    "type": "number",
    "description": "Discount %"
   },
   "campaignBudget": {
    "type": "string",
    "description": "Campaign budget"
   },
   "margin": {
    "type": "number",
    "description": "Margin"
   },
   "promotionType": {
    "type": "string",
    "description": "Promotion type"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "partner": {
    "type": "string",
    "description": "Partner"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "freeProductValue": {
    "type": "string",
    "description": "Free-product value"
   },
   "campaignDuration": {
    "type": "string",
    "format": "date-time",
    "description": "Campaign duration"
   },
   "financialExposure": {
    "type": "string",
    "description": "Financial exposure"
   },
   "discount1025": {
    "type": "number",
    "description": "Discount 10–25%"
   },
   "sequentialApproval": {
    "type": "string",
    "description": "Sequential approval"
   },
   "parallelApproval": {
    "type": "string",
    "description": "Parallel approval"
   },
   "conditionalApproval": {
    "type": "string",
    "description": "Conditional approval"
   },
   "mandatoryApproval": {
    "type": "string",
    "description": "Mandatory approval"
   },
   "optionalReview": {
    "type": "string",
    "description": "Optional review"
   },
   "delegation": {
    "type": "string",
    "description": "Delegation"
   },
   "escalation": {
    "type": "string",
    "description": "Escalation"
   }
  }
 },
 "CampaignBudgetFinancialLimitSetupInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Campaign Budget & Financial Limit Setup submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "totalCampaignBudget": {
    "type": "integer",
    "description": "Total campaign budget"
   },
   "discountBudget": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Discount budget"
   },
   "rewardBudget": {
    "type": "string",
    "description": "Reward budget"
   },
   "freeProductBudget": {
    "type": "string",
    "description": "Free-product budget"
   },
   "partnerFundedBudget": {
    "type": "string",
    "description": "Partner-funded budget"
   },
   "marketingFundedBudget": {
    "type": "string",
    "description": "Marketing-funded budget"
   },
   "venueBudget": {
    "type": "string",
    "description": "Venue budget"
   },
   "departmentBudget": {
    "type": "string",
    "description": "Department budget"
   },
   "campaign": {
    "type": "string",
    "description": "Campaign"
   },
   "budgetAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Budget amount"
   },
   "currency": {
    "type": "string",
    "description": "Currency"
   },
   "effectiveDates": {
    "type": "string",
    "description": "Effective dates"
   },
   "budgetOwner": {
    "type": "string",
    "description": "Budget owner"
   },
   "costCenter": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Cost center"
   },
   "businessEntity": {
    "type": "string",
    "description": "Business entity"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "department": {
    "type": "string",
    "description": "Department"
   },
   "fundingSource": {
    "type": "string",
    "description": "Funding source"
   },
   "entireCampaign": {
    "type": "string",
    "description": "Entire campaign"
   },
   "promotion": {
    "type": "string",
    "description": "Promotion"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "partner": {
    "type": "string",
    "description": "Partner"
   },
   "customerSegment": {
    "type": "string",
    "description": "Customer segment"
   }
  }
 },
 "CampaignBudgetFinancialLimitSetupView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Campaign Budget & Financial Limit Setup displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "totalCampaignBudget": {
    "type": "integer",
    "description": "Total campaign budget"
   },
   "discountBudget": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Discount budget"
   },
   "rewardBudget": {
    "type": "string",
    "description": "Reward budget"
   },
   "freeProductBudget": {
    "type": "string",
    "description": "Free-product budget"
   },
   "partnerFundedBudget": {
    "type": "string",
    "description": "Partner-funded budget"
   },
   "marketingFundedBudget": {
    "type": "string",
    "description": "Marketing-funded budget"
   },
   "venueBudget": {
    "type": "string",
    "description": "Venue budget"
   },
   "departmentBudget": {
    "type": "string",
    "description": "Department budget"
   },
   "campaign": {
    "type": "string",
    "description": "Campaign"
   },
   "budgetAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Budget amount"
   },
   "currency": {
    "type": "string",
    "description": "Currency"
   },
   "effectiveDates": {
    "type": "string",
    "description": "Effective dates"
   },
   "budgetOwner": {
    "type": "string",
    "description": "Budget owner"
   },
   "costCenter": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Cost center"
   },
   "businessEntity": {
    "type": "string",
    "description": "Business entity"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "department": {
    "type": "string",
    "description": "Department"
   },
   "fundingSource": {
    "type": "string",
    "description": "Funding source"
   },
   "entireCampaign": {
    "type": "string",
    "description": "Entire campaign"
   },
   "promotion": {
    "type": "string",
    "description": "Promotion"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "partner": {
    "type": "string",
    "description": "Partner"
   },
   "customerSegment": {
    "type": "string",
    "description": "Customer segment"
   }
  }
 },
 "CampaignExperimentABTestManagerView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Campaign Experiment & A/B Test Manager displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "freeFBVoucher": {
    "type": "string",
    "description": "Free F&B voucher"
   },
   "a40": {
    "type": "number",
    "description": "A — 40%"
   },
   "b40": {
    "type": "number",
    "description": "B — 40%"
   },
   "control20": {
    "type": "number",
    "description": "Control — 20%"
   },
   "discount": {
    "type": "number",
    "description": "Discount %"
   },
   "discountValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Discount value"
   },
   "promotionType": {
    "type": "string",
    "description": "Promotion type"
   },
   "bundle": {
    "type": "string",
    "description": "Bundle"
   },
   "reward": {
    "type": "string",
    "description": "Reward"
   },
   "audience": {
    "type": "string",
    "description": "Audience"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "validity": {
    "type": "string",
    "description": "Validity"
   },
   "messageOffer": {
    "type": "string",
    "description": "Message/offer"
   },
   "timing": {
    "type": "string",
    "description": "Timing"
   },
   "conversion": {
    "type": "number",
    "description": "Conversion"
   },
   "revenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue"
   },
   "aov": {
    "type": "string",
    "description": "AOV"
   },
   "redemption": {
    "type": "string",
    "description": "Redemption"
   },
   "discountCost": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Discount cost"
   },
   "margin": {
    "type": "number",
    "description": "Margin"
   },
   "incrementalRevenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Incremental revenue"
   },
   "roi": {
    "type": "string",
    "description": "ROI"
   },
   "manualWinner": {
    "type": "string",
    "description": "Manual winner"
   },
   "ruleBasedWinner": {
    "type": "string",
    "description": "Rule-based winner"
   },
   "aiRecommendation": {
    "type": "string",
    "description": "AI recommendation"
   }
  }
 },
 "CampaignFinancialCommercialSimulatorView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Campaign Financial & Commercial Simulator displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "audience": {
    "type": "string",
    "description": "Audience"
   },
   "products": {
    "type": "string",
    "description": "Products"
   },
   "promotion": {
    "type": "string",
    "description": "Promotion"
   },
   "discount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Discount"
   },
   "duration": {
    "type": "string",
    "format": "date-time",
    "description": "Duration"
   },
   "channels": {
    "type": "string",
    "description": "Channels"
   },
   "historicalConversion": {
    "type": "number",
    "description": "Historical conversion"
   },
   "expectedTraffic": {
    "type": "string",
    "description": "Expected traffic"
   },
   "redemptionLimit": {
    "type": "integer",
    "description": "Redemption limit"
   },
   "budget": {
    "type": "string",
    "description": "Budget"
   },
   "eligibleAudience": {
    "type": "string",
    "description": "Eligible audience"
   },
   "expectedTransactions": {
    "type": "integer",
    "description": "Expected transactions"
   },
   "expectedRedemptions": {
    "type": "integer",
    "description": "Expected redemptions"
   },
   "grossRevenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Gross revenue"
   },
   "discountCost": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Discount cost"
   },
   "netRevenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Net revenue"
   },
   "incrementalRevenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Incremental revenue"
   },
   "averageOrderValue": {
    "type": "number",
    "description": "Average order value"
   },
   "grossMargin": {
    "type": "number",
    "description": "Gross margin"
   },
   "marginImpact": {
    "type": "number",
    "description": "Margin impact"
   },
   "expectedBudgetConsumption": {
    "type": "string",
    "description": "Expected budget consumption"
   },
   "roi": {
    "type": "string",
    "description": "ROI"
   }
  }
 },
 "CampaignGovernanceBudgetCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Campaign Governance & Budget Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "activeCampaigns": {
    "type": "integer",
    "description": "Active Campaigns"
   },
   "campaignBudget": {
    "type": "string",
    "description": "Campaign Budget"
   },
   "budgetConsumed": {
    "type": "string",
    "description": "Budget Consumed"
   },
   "remainingBudget": {
    "type": "string",
    "description": "Remaining Budget"
   },
   "discountExposure": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Discount Exposure"
   },
   "redemptionValue": {
    "type": "string",
    "description": "Redemption Value"
   },
   "revenueGenerated": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue Generated"
   },
   "incrementalRevenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Incremental Revenue"
   },
   "campaignRoi": {
    "type": "string",
    "description": "Campaign ROI"
   },
   "campaignsNearBudgetLimit": {
    "type": "integer",
    "description": "Campaigns Near Budget Limit"
   },
   "pendingApprovals": {
    "type": "integer",
    "description": "Pending Approvals"
   },
   "suspendedCampaigns": {
    "type": "integer",
    "description": "Suspended Campaigns"
   },
   "healthy": {
    "type": "string",
    "description": "Healthy"
   },
   "monitor": {
    "type": "string",
    "description": "Monitor"
   },
   "warning": {
    "type": "string",
    "description": "Warning"
   },
   "critical": {
    "type": "string",
    "description": "Critical"
   },
   "budgetExhausted": {
    "type": "string",
    "description": "Budget Exhausted"
   },
   "suspended": {
    "type": "string",
    "description": "Suspended"
   },
   "budgetAed500000": {
    "type": "string",
    "description": "Budget: AED 500,000"
   },
   "consumedAed387500": {
    "type": "string",
    "description": "Consumed: AED 387,500"
   },
   "remainingAed112500": {
    "type": "string",
    "description": "Remaining: AED 112,500"
   },
   "utilization775": {
    "type": "number",
    "description": "Utilization: 77.5%"
   },
   "revenueAed284m": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue: AED 2.84M"
   },
   "roi53x": {
    "type": "string",
    "description": "ROI: 5.3x"
   },
   "statusHealthy": {
    "type": "string",
    "description": "Status: HEALTHY"
   }
  }
 },
 "GovernanceAuditAiRiskLaunchReadinessView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Governance Audit, AI Risk & Launch Readiness displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "promotionConfiguration": {
    "type": "string",
    "description": "Promotion Configuration ✓"
   },
   "eligibility": {
    "type": "string",
    "description": "Eligibility ✓"
   },
   "stackingRules": {
    "type": "string",
    "description": "Stacking Rules ✓"
   },
   "budget": {
    "type": "string",
    "description": "Budget ✓"
   },
   "redemptionLimits": {
    "type": "string",
    "description": "Redemption Limits ✓"
   },
   "marginGuardrail": {
    "type": "number",
    "description": "Margin Guardrail ✓"
   },
   "simulationCompleted": {
    "type": "string",
    "description": "Simulation Completed ✓"
   },
   "requiredApproval": {
    "type": "string",
    "description": "Required Approval ✓"
   },
   "channelPublication": {
    "type": "string",
    "description": "Channel Publication ✓"
   },
   "auditRequirements": {
    "type": "string",
    "description": "Audit Requirements ✓"
   },
   "budgetCreation": {
    "type": "string",
    "description": "Budget creation"
   },
   "budgetChange": {
    "type": "string",
    "description": "Budget change"
   },
   "limitChanges": {
    "type": "integer",
    "description": "Limit changes"
   },
   "approvalSubmissions": {
    "type": "string",
    "description": "Approval submissions"
   },
   "approvalDecisions": {
    "type": "string",
    "description": "Approval decisions"
   },
   "overrides": {
    "type": "string",
    "description": "Overrides"
   },
   "automaticSuspension": {
    "type": "string",
    "description": "Automatic suspension"
   },
   "reactivation": {
    "type": "string",
    "description": "Reactivation"
   },
   "simulationResults": {
    "type": "string",
    "description": "Simulation results"
   },
   "experimentChanges": {
    "type": "string",
    "description": "Experiment changes"
   },
   "campaignLaunch": {
    "type": "string",
    "description": "Campaign launch"
   },
   "level1Advisory": {
    "type": "string",
    "description": "Level 1 — Advisory"
   },
   "aiRecommends": {
    "type": "string",
    "description": "AI recommends"
   },
   "humanDecides": {
    "type": "string",
    "description": "Human decides"
   },
   "level2GovernedAutomation": {
    "type": "string",
    "description": "Level 2 — Governed Automation"
   },
   "campaignOperationalStatus": {
    "type": "string",
    "description": "Campaign operational status"
   },
   "boards24PromotionMechanics": {
    "type": "string",
    "description": "Boards 2–4 — Promotion Mechanics"
   },
   "discountRewardExposure": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Discount/reward exposure"
   },
   "boards56Bundles": {
    "type": "string",
    "description": "Boards 5–6 — Bundles"
   },
   "bundleFinancialImpact": {
    "type": "string",
    "description": "Bundle financial impact"
   },
   "board7Targeting": {
    "type": "string",
    "description": "Board 7 — Targeting"
   },
   "audienceSize": {
    "type": "string",
    "description": "Audience size"
   },
   "board8Stacking": {
    "type": "string",
    "description": "Board 8 — Stacking"
   },
   "combinedDiscountExposure": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Combined discount exposure"
   },
   "priceAndMargin": {
    "type": "number",
    "description": "Price and margin"
   },
   "audienceAndHistoricalResponse": {
    "type": "string",
    "description": "Audience and historical response"
   },
   "budgetAccountingAndProfitability": {
    "type": "string",
    "description": "Budget, accounting and profitability"
   },
   "actualTransactionValues": {
    "type": "string",
    "description": "Actual transaction values"
   },
   "forecastsAndCampaignAnalytics": {
    "type": "string",
    "description": "Forecasts and campaign analytics"
   },
   "approvalAuthority": {
    "type": "string",
    "description": "Approval authority"
   }
  }
 },
 "RedemptionDiscountExposureLimitManagerView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Redemption, Discount & Exposure Limit Manager displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "typesType": {
    "type": "string",
    "enum": [
     "maximumRedemptions",
     "maximumDiscountValue",
     "maximumDiscount",
     "maximumRewardQuantity",
     "maximumFreeTickets",
     "maximumFreeProducts",
     "maximumTransactions",
     "maximumCustomers",
     "maximumRedemptionsPerCustomer",
     "maximumDailyExposure"
    ],
    "description": "Vocabulary listed under Limit Types."
   },
   "maximumRedemptions": {
    "type": "integer",
    "description": "Maximum redemptions (the pack shows 50,000)"
   },
   "maximumCustomerRedemption": {
    "type": "string",
    "description": "Maximum customer redemption (the pack shows 2)"
   },
   "dailyRedemptionLimit": {
    "type": "integer",
    "description": "Daily redemption limit (the pack shows 5,000)"
   },
   "orCustomThresholds": {
    "type": "string",
    "description": "or custom thresholds"
   }
  }
 },
 "ThresholdActionsAutomaticSuspensionView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Threshold Actions & Automatic Suspension displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "warn": {
    "type": "string",
    "description": "Warn"
   },
   "requireApproval": {
    "type": "boolean",
    "description": "Require approval"
   },
   "reduceAllocation": {
    "type": "string",
    "description": "Reduce allocation"
   },
   "stopSpecificChannel": {
    "type": "string",
    "description": "Stop specific channel"
   },
   "stopPartner": {
    "type": "string",
    "description": "Stop partner"
   },
   "stopPromotion": {
    "type": "string",
    "description": "Stop promotion"
   },
   "stopCampaign": {
    "type": "string",
    "description": "Stop campaign"
   },
   "allowGraceAmount": {
    "type": "boolean",
    "description": "Allow grace amount"
   },
   "continueWithExecutiveAuthorization": {
    "type": "string",
    "description": "Continue with executive authorization"
   }
  }
 }
}
```
