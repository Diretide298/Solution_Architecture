# WS40 — Pricing   Revenue Management board 7

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
  `PRODUCT_CONFIGURE, PRODUCT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **0 of these operations work offline**
  
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-108` | Revenue Optimization Command Center | commandCentre | 1 | 0 | — |
| `ADM-109` | Pricing Simulation Studio | listDetail | 1 | 1 | — |
| `ADM-110` | Scenario Modeling & What-If Analysis | listDetail | 1 | 0 | — |
| `ADM-111` | A/B Pricing Experiment Studio | listDetail | 1 | 0 | — |
| `ADM-112` | Revenue & Demand Impact Forecasting | commandCentre | 1 | 0 | — |
| `ADM-113` | AI Recommendation Review & Decision Queue | listDetail | 1 | 0 | — |
| `ADM-114` | Automation Policy & Autonomous Pricing Orchestrator | configEditor | 1 | 0 | — |
| `ADM-115` | Live Dynamic Price Execution & Deployment Monitor | listDetail | 1 | 0 | — |
| `ADM-116` | Dynamic Pricing Performance & Optimization Analytics | listDetail | 1 | 0 | — |
| `ADM-117` | AI Learning, Model Performance & Optimization Feedback | listDetail | 1 | 0 | — |

## Thin screens in this batch

**ADM-111, ADM-113, ADM-117 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-108",
  "name": "Revenue Optimization Command Center",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "7",
   "number": "10.7.1",
   "page": 114
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/revenue-optimization-command-center-adm-108",
   "component": "apps/ticvai-web/src/routes/commercial/RevenueOptimizationCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-109",
    "ADM-110",
    "ADM-111",
    "ADM-112",
    "ADM-113",
    "ADM-114",
    "ADM-115",
    "ADM-116",
    "ADM-117"
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
     "to": "ADM-109",
     "trigger": "Works in Pricing Simulation Studio",
     "provenance": "flow F149 step 1→2",
     "operation": "listRevenue"
    },
    {
     "to": "ADM-110",
     "trigger": "Works in Scenario Modeling & What-If Analysis",
     "provenance": "flow F149 step 3→4",
     "operation": "listRevenue"
    },
    {
     "to": "ADM-111",
     "trigger": "Works in A/B Pricing Experiment Studio",
     "provenance": "flow F149 step 5→6",
     "operation": "listRevenue"
    },
    {
     "to": "ADM-112",
     "trigger": "Works in Revenue & Demand Impact Forecasting",
     "provenance": "flow F149 step 7→8",
     "operation": "listRevenue"
    },
    {
     "to": "ADM-113",
     "trigger": "Works in AI Recommendation Review & Decision Queue",
     "provenance": "flow F149 step 9→10",
     "operation": "listRevenue"
    },
    {
     "to": "ADM-114",
     "trigger": "Works in Automation Policy & Autonomous Pricing Orchestrator",
     "provenance": "flow F149 step 11→12",
     "operation": "listRevenue"
    },
    {
     "to": "ADM-115",
     "trigger": "Works in Live Dynamic Price Execution & Deployment Monitor",
     "provenance": "flow F149 step 13→14",
     "operation": "listRevenue"
    },
    {
     "to": "ADM-116",
     "trigger": "Works in Dynamic Pricing Performance & Optimization Analytics",
     "provenance": "flow F149 step 15→16",
     "operation": "listRevenue"
    },
    {
     "to": "ADM-117",
     "trigger": "Works in AI Learning, Model Performance & Optimization Feedback",
     "provenance": "flow F149 step 17→18",
     "operation": "listRevenue"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each row displays) — counts over a population, then the population",
  "purpose": "Provide Revenue Managers with the operational control center for all dynamic pricing simulations, AI recommendations, automated changes, experiments and revenue optimization activity.",
  "purposeNote": "Revenue teams can monitor and act on pricing optimization opportunities across the organization from one centralized workspace.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 6 actions on this screen and the screen declares 1 operation.** Unserved: Run Simulation, Review Recommendations, Start Experiment, Approve Changes, Pause Automation, Open Execution Monitor. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 114 §Quick Actions"
   }
  ],
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Revenue Opportunity",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 114 §Display",
       "bindsTo": "RevenueOptimizationCommandCenterView.revenueOpportunity"
      },
      {
       "kind": "metricTile",
       "label": "Incremental Revenue Generated",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 114 §Display",
       "bindsTo": "RevenueOptimizationCommandCenterView.incrementalRevenueGenerated"
      },
      {
       "kind": "metricTile",
       "label": "Active Optimizations",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 114 §Display",
       "bindsTo": "RevenueOptimizationCommandCenterView.activeOptimizations"
      },
      {
       "kind": "metricTile",
       "label": "Recommendations Awaiting Action",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 114 §Display",
       "bindsTo": "RevenueOptimizationCommandCenterView.recommendationsAwaitingAction"
      },
      {
       "kind": "metricTile",
       "label": "Pending Simulations",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 114 §Display",
       "bindsTo": "RevenueOptimizationCommandCenterView.pendingSimulations"
      },
      {
       "kind": "metricTile",
       "label": "Auto-Executed Changes",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 114 §Display",
       "bindsTo": "RevenueOptimizationCommandCenterView.autoExecutedChanges"
      },
      {
       "kind": "metricTile",
       "label": "Approval Required",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 114 §Display",
       "bindsTo": "RevenueOptimizationCommandCenterView.approvalRequired"
      },
      {
       "kind": "metricTile",
       "label": "Active A/B Tests",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 114 §Display",
       "bindsTo": "RevenueOptimizationCommandCenterView.activeABTests"
      },
      {
       "kind": "metricTile",
       "label": "Pricing Exceptions",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 114 §Display",
       "bindsTo": "RevenueOptimizationCommandCenterView.pricingExceptions"
      },
      {
       "kind": "metricTile",
       "label": "Revenue at Risk",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 114 §Display",
       "bindsTo": "RevenueOptimizationCommandCenterView.revenueAtRisk"
      },
      {
       "kind": "metricTile",
       "label": "Forecast Accuracy",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 114 §Display",
       "bindsTo": "RevenueOptimizationCommandCenterView.forecastAccuracy"
      },
      {
       "kind": "metricTile",
       "label": "Optimization Success Rate",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 114 §Display",
       "bindsTo": "RevenueOptimizationCommandCenterView.optimizationSuccessRate"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every revenue optimization",
       "columns": [
        "RevenueOptimizationCommandCenterView.venue",
        "RevenueOptimizationCommandCenterView.eventProduct",
        "RevenueOptimizationCommandCenterView.performance",
        "RevenueOptimizationCommandCenterView.currentPrice",
        "RevenueOptimizationCommandCenterView.recommendedPrice",
        "RevenueOptimizationCommandCenterView.forecastRevenue",
        "RevenueOptimizationCommandCenterView.expectedUplift",
        "RevenueOptimizationCommandCenterView.confidence",
        "RevenueOptimizationCommandCenterView.automationMode",
        "RevenueOptimizationCommandCenterView.approvalStatus",
        "RevenueOptimizationCommandCenterView.executionStatus"
       ],
       "bindsTo": "RevenueOptimizationCommandCenterView",
       "operation": "listRevenue",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 114 §Each row displays"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected revenue optimization",
       "bindsTo": "RevenueOptimizationCommandCenterView",
       "columns": [
        "RevenueOptimizationCommandCenterView.venue",
        "RevenueOptimizationCommandCenterView.eventProduct",
        "RevenueOptimizationCommandCenterView.performance",
        "RevenueOptimizationCommandCenterView.currentPrice",
        "RevenueOptimizationCommandCenterView.recommendedPrice",
        "RevenueOptimizationCommandCenterView.forecastRevenue",
        "RevenueOptimizationCommandCenterView.expectedUplift",
        "RevenueOptimizationCommandCenterView.confidence",
        "RevenueOptimizationCommandCenterView.automationMode",
        "RevenueOptimizationCommandCenterView.approvalStatus",
        "RevenueOptimizationCommandCenterView.executionStatus"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Event Action”, “AED”, “Attraction AED Simulat”, “B 220 e”.",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 114 §Each row displays"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Run Simulation",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 114 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Review Recommendations",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 114 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Start Experiment",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 114 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Approve Changes",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 114 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Pause Automation",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 114 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Open Execution Monitor",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 114 §Quick Actions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The revenue optimization list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the revenue optimization untouched.",
   "emptyFirstRun": "No revenue optimization yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the revenue optimization are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listRevenue",
    "contract": "catalogue",
    "purpose": "Revenue Optimization Command Center",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-108"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 114. 23 of 23 labels bound to a contract property; 29 of 50 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-109",
  "name": "Pricing Simulation Studio",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "7",
   "number": "10.7.2",
   "page": 115
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/pricing-simulation-studio-adm-109",
   "component": "apps/ticvai-web/src/routes/commercial/PricingSimulationStudio.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-108"
   ],
   "exitTo": [
    "ADM-108"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-108, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-108",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F149 step 2→3",
     "operation": "setPricing"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Allow any proposed dynamic-pricing change to be tested before affecting live customers. This should become the sandbox of the Dynamic Pricing Engine.",
  "purposeNote": "Authorized users can safely evaluate a pricing recommendation or strategy against forecast commercial outcomes without modifying production prices.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 5 actions on this screen and the screen declares 1 operation.** Unserved: Save Scenario, Compare Scenario, Send for Approval, Start Experiment, Discard. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 115 §Actions"
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
       "label": "Every pricing simulation",
       "columns": [
        "PricingSimulationStudioView.simulationConfidence89",
        "PricingSimulationStudioView.dataVolume",
        "PricingSimulationStudioView.historicalSimilarity",
        "PricingSimulationStudioView.forecastConfidence",
        "PricingSimulationStudioView.elasticityConfidence",
        "PricingSimulationStudioView.externalSignalQuality"
       ],
       "bindsTo": "PricingSimulationStudioView",
       "operation": "setPricing",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 115 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected pricing simulation",
       "bindsTo": "PricingSimulationStudioView",
       "columns": [
        "PricingSimulationStudioView.simulationConfidence89",
        "PricingSimulationStudioView.dataVolume",
        "PricingSimulationStudioView.historicalSimilarity",
        "PricingSimulationStudioView.forecastConfidence",
        "PricingSimulationStudioView.elasticityConfidence",
        "PricingSimulationStudioView.externalSignalQuality"
       ],
       "notes": "The pack groups this record's detail under its own headings: “A simulation can originate from”, “Calculate”, “Current Strategy”, “Before simulation completes, show”.",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 115 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save Scenario",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 115 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Compare Scenario",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 115 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Send for Approval",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 115 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Start Experiment",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 115 §Actions"
      },
      {
       "kind": "destructiveButton",
       "label": "Discard",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 115 §Actions"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmDiscard",
    "component": "confirmDialog",
    "trigger": "Discard",
    "body": "**Discard on a pricing simulation is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 115 §Actions"
   }
  ],
  "states": {
   "loading": "The pricing simulation list.",
   "error": "Could not load. Names which read failed and leaves the pricing simulation untouched.",
   "emptyFirstRun": "No pricing simulation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the pricing simulation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setPricing",
    "contract": "catalogue",
    "purpose": "Pricing Simulation Studio",
    "trigger": "onAction",
    "invalidates": [
     "setPricing"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "PricingSimulationStudioView.simulationConfidence89",
    "PricingSimulationStudioView.dataVolume",
    "PricingSimulationStudioView.historicalSimilarity",
    "PricingSimulationStudioView.forecastConfidence",
    "PricingSimulationStudioView.elasticityConfidence",
    "PricingSimulationStudioView.externalSignalQuality"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-109"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 115. 6 of 6 labels bound to a contract property; 20 of 45 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-110",
  "name": "Scenario Modeling & What-If Analysis",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "7",
   "number": "10.7.3",
   "page": 117
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/scenario-modeling-what-if-analysis-adm-110",
   "component": "apps/ticvai-web/src/routes/commercial/ScenarioModelingWhatIfAnalysis.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-108"
   ],
   "exitTo": [
    "ADM-108"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-108, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-108",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F149 step 4→5",
     "operation": "listScenarioModelingWhat"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Scenario Modeling & What-If Analysis",
  "purposeNote": "Revenue teams can model alternative market and demand conditions and compare different pricing responses before implementation.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 7 actions on this screen and the screen declares 1 operation.** Unserved: Competitor Price Drop, Competitor Price Increase, Custom Scenario, Save, Duplicate, Compare, Submit for Review. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 117 §Support"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 117"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 117"
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
       "label": "Competitor Price Drop",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 117 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Competitor Price Increase",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 117 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Custom Scenario",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 117 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Save",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 117 §Allow users to"
      },
      {
       "kind": "secondaryButton",
       "label": "Duplicate",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 117 §Allow users to"
      },
      {
       "kind": "secondaryButton",
       "label": "Compare",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 117 §Allow users to"
      },
      {
       "kind": "secondaryButton",
       "label": "Submit for Review",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 117 §Allow users to"
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
   "loading": "The scenario modeling what-if list.",
   "error": "Could not load. Names which read failed and leaves the scenario modeling what-if untouched.",
   "emptyFirstRun": "No scenario modeling what-if yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the scenario modeling what-if are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listScenarioModelingWhat",
    "contract": "catalogue",
    "purpose": "Scenario Modeling & What-If Analysis",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "ScenarioModelingWhatIfAnalysisView.lowDemand",
    "ScenarioModelingWhatIfAnalysisView.expectedDemand",
    "ScenarioModelingWhatIfAnalysisView.highDemand",
    "ScenarioModelingWhatIfAnalysisView.sellOut",
    "ScenarioModelingWhatIfAnalysisView.competitorPriceDrop"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-110"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 117. 0 of 0 labels bound to a contract property; 7 of 52 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-111",
  "name": "A/B Pricing Experiment Studio",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "7",
   "number": "10.7.4",
   "page": 119
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/a-b-pricing-experiment-studio-adm-111",
   "component": "apps/ticvai-web/src/routes/commercial/ABPricingExperimentStudio.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-108"
   ],
   "exitTo": [
    "ADM-108"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-108, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-108",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F149 step 6→7",
     "operation": "setPricingExperiment"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Allow TICVAI to scientifically test different pricing strategies using controlled customer groups. This is essential because AI should learn from actual customer behavior, not only historical assumptions.",
  "purposeNote": "Authorized users can execute controlled pricing experiments and determine statistically whether one strategy performs better than another.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every pricing experiment",
       "columns": [
        "ABPricingExperimentStudioView.sampleSize",
        "ABPricingExperimentStudioView.confidenceLevel",
        "ABPricingExperimentStudioView.experimentDuration",
        "ABPricingExperimentStudioView.statisticalSignificance"
       ],
       "bindsTo": "ABPricingExperimentStudioView",
       "operation": "setPricingExperiment",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 119 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected pricing experiment",
       "bindsTo": "ABPricingExperimentStudioView",
       "columns": [
        "ABPricingExperimentStudioView.sampleSize",
        "ABPricingExperimentStudioView.confidenceLevel",
        "ABPricingExperimentStudioView.experimentDuration",
        "ABPricingExperimentStudioView.statisticalSignificance"
       ],
       "notes": "The pack groups this record's detail under its own headings: “AED 250”, “Variant B”, “AED 265”, “Experiments must respect”, “Winner”.",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 119 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save changes",
       "provenance": "contract operation setPricingExperiment"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The pricing experiment list.",
   "error": "Could not load. Names which read failed and leaves the pricing experiment untouched.",
   "emptyFirstRun": "No pricing experiment yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the pricing experiment are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setPricingExperiment",
    "contract": "catalogue",
    "purpose": "A/B Pricing Experiment Studio",
    "trigger": "onAction",
    "invalidates": [
     "setPricingExperiment"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "ABPricingExperimentStudioView.sampleSize",
    "ABPricingExperimentStudioView.confidenceLevel",
    "ABPricingExperimentStudioView.experimentDuration",
    "ABPricingExperimentStudioView.statisticalSignificance"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-111"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 119. 4 of 4 labels bound to a contract property; 20 of 42 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-112",
  "name": "Revenue & Demand Impact Forecasting",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "7",
   "number": "10.7.5",
   "page": 120
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/revenue-demand-impact-forecasting-adm-112",
   "component": "apps/ticvai-web/src/routes/commercial/RevenueDemandImpactForecasting.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-108"
   ],
   "exitTo": [
    "ADM-108"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-108, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-108",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F149 step 8→9",
     "operation": "listRevenueDemandImpact"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Forecast; Display) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide a dedicated commercial impact assessment before a dynamic-pricing action is approved or executed.",
  "purposeNote": "Approvers can clearly understand expected revenue, demand and customer consequences before authorizing a dynamic pricing action.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Revenue",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 120 §Forecast",
       "bindsTo": "RevenueDemandImpactForecastingView.revenue"
      },
      {
       "kind": "metricTile",
       "label": "Demand",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 120 §Forecast",
       "bindsTo": "RevenueDemandImpactForecastingView.demand"
      },
      {
       "kind": "metricTile",
       "label": "Attendance",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 120 §Forecast",
       "bindsTo": "RevenueDemandImpactForecastingView.attendance"
      },
      {
       "kind": "metricTile",
       "label": "Occupancy",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 120 §Forecast",
       "bindsTo": "RevenueDemandImpactForecastingView.occupancy"
      },
      {
       "kind": "metricTile",
       "label": "Conversion",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 120 §Forecast",
       "bindsTo": "RevenueDemandImpactForecastingView.conversion"
      },
      {
       "kind": "metricTile",
       "label": "Margin",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 120 §Forecast",
       "bindsTo": "RevenueDemandImpactForecastingView.margin"
      },
      {
       "kind": "metricTile",
       "label": "ASP",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 120 §Forecast",
       "bindsTo": "RevenueDemandImpactForecastingView.asp"
      },
      {
       "kind": "metricTile",
       "label": "Sell-Through",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 120 §Forecast",
       "bindsTo": "RevenueDemandImpactForecastingView.sellThrough"
      },
      {
       "kind": "metricTile",
       "label": "Sell-Out Probability",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 120 §Forecast",
       "bindsTo": "RevenueDemandImpactForecastingView.sellOutProbability"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The revenue demand impact list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the revenue demand impact untouched.",
   "emptyFirstRun": "No revenue demand impact yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the revenue demand impact are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listRevenueDemandImpact",
    "contract": "catalogue",
    "purpose": "Revenue & Demand Impact Forecasting",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "RevenueDemandImpactForecastingView.expectedRevenueAed245m",
    "RevenueDemandImpactForecastingView.expectedDemand9800",
    "RevenueDemandImpactForecastingView.expectedOccupancy91",
    "RevenueDemandImpactForecastingView.expectedRevenueAed252m",
    "RevenueDemandImpactForecastingView.expectedDemand9500"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-112"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 120. 9 of 9 labels bound to a contract property; 9 of 32 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-113",
  "name": "AI Recommendation Review & Decision Queue",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "7",
   "number": "10.7.6",
   "page": 122
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/ai-recommendation-review-decision-queue-adm-113",
   "component": "apps/ticvai-web/src/routes/commercial/AiRecommendationReviewDecisionQueue.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-108"
   ],
   "exitTo": [
    "ADM-108"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-108, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-108",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F149 step 10→11",
     "operation": "listRecommendationReviewDecision"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide the human decision workspace for recommendations produced by Board 6. This should be the Revenue Manager's inbox.",
  "purposeNote": "Every material AI recommendation can be reviewed, explained, simulated, approved, modified or rejected with complete traceability.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every recommendation review decision",
       "columns": [
        "AiRecommendationReviewDecisionQueueView.recommendation",
        "AiRecommendationReviewDecisionQueueView.venue",
        "AiRecommendationReviewDecisionQueueView.event",
        "AiRecommendationReviewDecisionQueueView.currentPrice",
        "AiRecommendationReviewDecisionQueueView.recommendedPrice",
        "AiRecommendationReviewDecisionQueueView.change",
        "AiRecommendationReviewDecisionQueueView.revenueOpportunity",
        "AiRecommendationReviewDecisionQueueView.demandImpact",
        "AiRecommendationReviewDecisionQueueView.confidence",
        "AiRecommendationReviewDecisionQueueView.urgency",
        "AiRecommendationReviewDecisionQueueView.governanceLevel"
       ],
       "bindsTo": "AiRecommendationReviewDecisionQueueView",
       "operation": "listRecommendationReviewDecision",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 122 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected recommendation review decision",
       "bindsTo": "AiRecommendationReviewDecisionQueueView",
       "columns": [
        "AiRecommendationReviewDecisionQueueView.recommendation",
        "AiRecommendationReviewDecisionQueueView.venue",
        "AiRecommendationReviewDecisionQueueView.event",
        "AiRecommendationReviewDecisionQueueView.currentPrice",
        "AiRecommendationReviewDecisionQueueView.recommendedPrice",
        "AiRecommendationReviewDecisionQueueView.change",
        "AiRecommendationReviewDecisionQueueView.revenueOpportunity",
        "AiRecommendationReviewDecisionQueueView.demandImpact",
        "AiRecommendationReviewDecisionQueueView.confidence",
        "AiRecommendationReviewDecisionQueueView.urgency",
        "AiRecommendationReviewDecisionQueueView.governanceLevel"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Simulation Result”, “Simulation Revenue Uplift”, “Demand Impact”, “AED 265”, “Feedback Loop”, “Human Selected AED 265”.",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 122 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "banner",
       "label": "Permissions this screen separates",
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** Accept, Reject, Modify, Simulate Again, Schedule, Send for Approval. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 122 §Authorized users can"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The recommendation review decision list.",
   "error": "Could not load. Names which read failed and leaves the recommendation review decision untouched.",
   "emptyFirstRun": "No recommendation review decision yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the recommendation review decision are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listRecommendationReviewDecision",
    "contract": "catalogue",
    "purpose": "AI Recommendation Review & Decision Queue",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "AiRecommendationReviewDecisionQueueView.recommendation",
    "AiRecommendationReviewDecisionQueueView.venue",
    "AiRecommendationReviewDecisionQueueView.event",
    "AiRecommendationReviewDecisionQueueView.currentPrice",
    "AiRecommendationReviewDecisionQueueView.recommendedPrice",
    "AiRecommendationReviewDecisionQueueView.change"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-113"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 122. 11 of 11 labels bound to a contract property; 24 of 37 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-114",
  "name": "Automation Policy & Autonomous Pricing Orchestrator",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "7",
   "number": "10.7.7",
   "page": 123
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/automation-policy-autonomous-pricing-orchestrator-adm-114",
   "component": "apps/ticvai-web/src/routes/commercial/AutomationPolicyAutonomousPricingOrchestrator.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-108"
   ],
   "exitTo": [
    "ADM-108"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-108, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-108",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F149 step 12→13",
     "operation": "listAutomationPolicyAutonomous"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Control when TICVAI is allowed to execute pricing changes automatically. Board 5 defines the strategy-level automation permission. This screen manages operational autonomous execution at scale.",
  "purposeNote": "confidence, commercial guardrails and emergency safety controls.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Tenant",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 123 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 123 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Product",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 123 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Event",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 123 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Strategy",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 123 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Channel",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 123 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Market",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 123 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Date/Time",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 123 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Evaluation Frequency",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 123 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Execution Frequency",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 123 §Configure"
      },
      {
       "kind": "textField",
       "label": "Minimum Time Between Changes",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 123 §Configure"
      },
      {
       "kind": "textField",
       "label": "Maximum Changes per Day",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 123 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The automation policy autonomous configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the automation policy autonomous untouched.",
   "emptyFirstRun": "No automation policy autonomous configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAutomationPolicyAutonomous",
    "contract": "catalogue",
    "purpose": "Automation Policy & Autonomous Pricing Orchestrator",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-114"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 123. 0 of 0 labels bound to a contract property; 12 of 34 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-115",
  "name": "Live Dynamic Price Execution & Deployment Monitor",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "7",
   "number": "10.7.8",
   "page": 125
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/live-dynamic-price-execution-deployment-monitor-adm-115",
   "component": "apps/ticvai-web/src/routes/commercial/LiveDynamicPriceExecutionDeploymentMonitor.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-108"
   ],
   "exitTo": [
    "ADM-108"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-108, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-108",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F149 step 14→15",
     "operation": "createLiveDynamicPrice"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Each execution shows) and no metric row",
  "purpose": "Monitor pricing actions as they are executed across TICVAI's selling ecosystem.",
  "purposeNote": "Operations teams can monitor the real-time execution and distribution of dynamic prices across all applicable sales channels.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 5 actions on this screen and the screen declares 1 operation.** Unserved: Retry, Hold, Revert, Escalate, Freeze Channel. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 125 §Actions"
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
       "label": "Every live dynamic price",
       "columns": [
        "LiveDynamicPriceExecutionDeploymentMonitorView.timestamp",
        "LiveDynamicPriceExecutionDeploymentMonitorView.product",
        "LiveDynamicPriceExecutionDeploymentMonitorView.event",
        "LiveDynamicPriceExecutionDeploymentMonitorView.previousPrice",
        "LiveDynamicPriceExecutionDeploymentMonitorView.newPrice",
        "Trigger",
        "LiveDynamicPriceExecutionDeploymentMonitorView.strategy",
        "LiveDynamicPriceExecutionDeploymentMonitorView.aiRecommendation",
        "LiveDynamicPriceExecutionDeploymentMonitorView.approval",
        "LiveDynamicPriceExecutionDeploymentMonitorView.executionSource",
        "LiveDynamicPriceExecutionDeploymentMonitorView.status"
       ],
       "bindsTo": "LiveDynamicPriceExecutionDeploymentMonitorView",
       "operation": "createLiveDynamicPrice",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 125 §Each execution shows"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected live dynamic price",
       "bindsTo": "LiveDynamicPriceExecutionDeploymentMonitorView",
       "columns": [
        "LiveDynamicPriceExecutionDeploymentMonitorView.timestamp",
        "LiveDynamicPriceExecutionDeploymentMonitorView.product",
        "LiveDynamicPriceExecutionDeploymentMonitorView.event",
        "LiveDynamicPriceExecutionDeploymentMonitorView.previousPrice",
        "LiveDynamicPriceExecutionDeploymentMonitorView.newPrice",
        "Trigger",
        "LiveDynamicPriceExecutionDeploymentMonitorView.strategy",
        "LiveDynamicPriceExecutionDeploymentMonitorView.aiRecommendation",
        "LiveDynamicPriceExecutionDeploymentMonitorView.approval",
        "LiveDynamicPriceExecutionDeploymentMonitorView.executionSource",
        "LiveDynamicPriceExecutionDeploymentMonitorView.status"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Dubai Indoor Attraction”, “Trigger”, “Monitor propagation to”, “Alert”, “Display every live movement”, “Board 4 Integration”.",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 125 §Each execution shows"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Retry",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 125 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Hold",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 125 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Revert",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 125 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Escalate",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 125 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Freeze Channel",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 125 §Actions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The live dynamic price list.",
   "error": "Could not load. Names which read failed and leaves the live dynamic price untouched.",
   "emptyFirstRun": "No live dynamic price yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the live dynamic price are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createLiveDynamicPrice",
    "contract": "catalogue",
    "purpose": "Live Dynamic Price Execution & Deployment Monitor",
    "trigger": "onAction",
    "invalidates": [
     "createLiveDynamicPrice"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "LiveDynamicPriceExecutionDeploymentMonitorView.timestamp",
    "LiveDynamicPriceExecutionDeploymentMonitorView.product",
    "LiveDynamicPriceExecutionDeploymentMonitorView.event",
    "LiveDynamicPriceExecutionDeploymentMonitorView.previousPrice",
    "LiveDynamicPriceExecutionDeploymentMonitorView.newPrice",
    "Trigger"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-115"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 125. 10 of 11 labels bound to a contract property; 16 of 40 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-116",
  "name": "Dynamic Pricing Performance & Optimization Analytics",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "7",
   "number": "10.7.9",
   "page": 126
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/dynamic-pricing-performance-optimization-analytics-adm-116",
   "component": "apps/ticvai-web/src/routes/commercial/DynamicPricingPerformanceOptimizationAnalytics.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-108"
   ],
   "exitTo": [
    "ADM-108"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-108, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-108",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F149 step 16→17",
     "operation": "listDynamicPricingPerformance"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Measure) and no metric row",
  "purpose": "Determine whether dynamic pricing actually improves TICVAI's commercial performance.",
  "purposeNote": "pricing strategies and AI recommendations.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 2 actions on this screen and the screen declares 1 operation.** Unserved: Strategy vs Strategy, Channel vs Channel. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 126 §Support"
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
       "label": "Every dynamic pricing performance",
       "columns": [
        "DynamicPricingPerformanceOptimizationAnalyticsView.incrementalRevenue",
        "DynamicPricingPerformanceOptimizationAnalyticsView.revenueUplift",
        "DynamicPricingPerformanceOptimizationAnalyticsView.marginUplift",
        "DynamicPricingPerformanceOptimizationAnalyticsView.averageSellingPrice",
        "DynamicPricingPerformanceOptimizationAnalyticsView.conversion",
        "DynamicPricingPerformanceOptimizationAnalyticsView.attendance",
        "DynamicPricingPerformanceOptimizationAnalyticsView.occupancy",
        "DynamicPricingPerformanceOptimizationAnalyticsView.sellThrough",
        "DynamicPricingPerformanceOptimizationAnalyticsView.revenuePerAvailableCapacity",
        "DynamicPricingPerformanceOptimizationAnalyticsView.numberOfPriceChanges",
        "DynamicPricingPerformanceOptimizationAnalyticsView.strategyRoi",
        "DynamicPricingPerformanceOptimizationAnalyticsView.recommendationsGenerated",
        "DynamicPricingPerformanceOptimizationAnalyticsView.accepted",
        "DynamicPricingPerformanceOptimizationAnalyticsView.rejected",
        "DynamicPricingPerformanceOptimizationAnalyticsView.modified",
        "DynamicPricingPerformanceOptimizationAnalyticsView.autoExecuted",
        "DynamicPricingPerformanceOptimizationAnalyticsView.successful",
        "DynamicPricingPerformanceOptimizationAnalyticsView.negativeOutcome"
       ],
       "bindsTo": "DynamicPricingPerformanceOptimizationAnalyticsView",
       "operation": "listDynamicPricingPerformance",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 126 §Measure"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected dynamic pricing performance",
       "bindsTo": "DynamicPricingPerformanceOptimizationAnalyticsView",
       "columns": [
        "DynamicPricingPerformanceOptimizationAnalyticsView.incrementalRevenue",
        "DynamicPricingPerformanceOptimizationAnalyticsView.revenueUplift",
        "DynamicPricingPerformanceOptimizationAnalyticsView.marginUplift",
        "DynamicPricingPerformanceOptimizationAnalyticsView.averageSellingPrice",
        "DynamicPricingPerformanceOptimizationAnalyticsView.conversion",
        "DynamicPricingPerformanceOptimizationAnalyticsView.attendance",
        "DynamicPricingPerformanceOptimizationAnalyticsView.occupancy",
        "DynamicPricingPerformanceOptimizationAnalyticsView.sellThrough",
        "DynamicPricingPerformanceOptimizationAnalyticsView.revenuePerAvailableCapacity",
        "DynamicPricingPerformanceOptimizationAnalyticsView.numberOfPriceChanges",
        "DynamicPricingPerformanceOptimizationAnalyticsView.strategyRoi",
        "DynamicPricingPerformanceOptimizationAnalyticsView.recommendationsGenerated",
        "DynamicPricingPerformanceOptimizationAnalyticsView.accepted",
        "DynamicPricingPerformanceOptimizationAnalyticsView.rejected",
        "DynamicPricingPerformanceOptimizationAnalyticsView.modified",
        "DynamicPricingPerformanceOptimizationAnalyticsView.autoExecuted",
        "DynamicPricingPerformanceOptimizationAnalyticsView.successful",
        "DynamicPricingPerformanceOptimizationAnalyticsView.negativeOutcome"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Revenue”, “ASP”, “Conversion”, “Attendance”, “Margin”, “Price”.",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 126 §Measure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Strategy vs Strategy",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 126 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Channel vs Channel",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 126 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The dynamic pricing performance list.",
   "error": "Could not load. Names which read failed and leaves the dynamic pricing performance untouched.",
   "emptyFirstRun": "No dynamic pricing performance yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the dynamic pricing performance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listDynamicPricingPerformance",
    "contract": "catalogue",
    "purpose": "Dynamic Pricing Performance & Optimization Analytics",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "DynamicPricingPerformanceOptimizationAnalyticsView.incrementalRevenue",
    "DynamicPricingPerformanceOptimizationAnalyticsView.revenueUplift",
    "DynamicPricingPerformanceOptimizationAnalyticsView.marginUplift",
    "DynamicPricingPerformanceOptimizationAnalyticsView.averageSellingPrice",
    "DynamicPricingPerformanceOptimizationAnalyticsView.conversion",
    "DynamicPricingPerformanceOptimizationAnalyticsView.attendance"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-116"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 126. 18 of 18 labels bound to a contract property; 20 of 44 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-117",
  "name": "AI Learning, Model Performance & Optimization Feedback",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "7",
   "number": "10.7.10",
   "page": 128
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/ai-learning-model-performance-optimization-feedback-adm-117",
   "component": "apps/ticvai-web/src/routes/commercial/AiLearningModelPerformanceOptimizationFeedback.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-108"
   ],
   "exitTo": [
    "ADM-108"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-108, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation."
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Forecast; Track; Detect) and no metric row",
  "purpose": "Close the intelligence loop by comparing AI predictions and recommendations with actual commercial outcomes. This is what allows the system to improve over time.",
  "purposeNote": "outcomes and provides governed feedback for improving future pricing intelligence. Board 7 — Final Screen Register # Backend Screen Core Responsibility 10.7. Revenue Optimization Command Center Optimization operations 1 # Backend Screen Core Responsibility 10.7. Pricing Simulation Studio Test proposed pricing 2 10.7. Commercial scenario",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every learning model performance",
       "columns": [
        "↓",
        "AiLearningModelPerformanceOptimizationFeedbackView.demandForecastAccuracy",
        "AiLearningModelPerformanceOptimizationFeedbackView.revenueForecastAccuracy",
        "AiLearningModelPerformanceOptimizationFeedbackView.elasticityAccuracy",
        "AiLearningModelPerformanceOptimizationFeedbackView.recommendationSuccess",
        "AiLearningModelPerformanceOptimizationFeedbackView.confidenceCalibration",
        "AiLearningModelPerformanceOptimizationFeedbackView.falsePositiveRate",
        "AiLearningModelPerformanceOptimizationFeedbackView.revenueUplift"
       ],
       "bindsTo": "AiLearningModelPerformanceOptimizationFeedbackView",
       "operation": "listLearningModelPerformance",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 128 §Forecast"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected learning model performance",
       "bindsTo": "AiLearningModelPerformanceOptimizationFeedbackView",
       "columns": [
        "↓",
        "AiLearningModelPerformanceOptimizationFeedbackView.demandForecastAccuracy",
        "AiLearningModelPerformanceOptimizationFeedbackView.revenueForecastAccuracy",
        "AiLearningModelPerformanceOptimizationFeedbackView.elasticityAccuracy",
        "AiLearningModelPerformanceOptimizationFeedbackView.recommendationSuccess",
        "AiLearningModelPerformanceOptimizationFeedbackView.confidenceCalibration",
        "AiLearningModelPerformanceOptimizationFeedbackView.falsePositiveRate",
        "AiLearningModelPerformanceOptimizationFeedbackView.revenueUplift"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Situation”, “Signals”, “Human/Automation Decision”, “Actual Price”, “Actual Demand”, “Actual Revenue”.",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 128 §Forecast"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The learning model performance list.",
   "error": "Could not load. Names which read failed and leaves the learning model performance untouched.",
   "emptyFirstRun": "No learning model performance yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the learning model performance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listLearningModelPerformance",
    "contract": "catalogue",
    "purpose": "AI Learning, Model Performance & Optimization Feedback",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "↓",
    "AiLearningModelPerformanceOptimizationFeedbackView.demandForecastAccuracy",
    "AiLearningModelPerformanceOptimizationFeedbackView.revenueForecastAccuracy",
    "AiLearningModelPerformanceOptimizationFeedbackView.elasticityAccuracy",
    "AiLearningModelPerformanceOptimizationFeedbackView.recommendationSuccess",
    "AiLearningModelPerformanceOptimizationFeedbackView.confidenceCalibration"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-117"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 128. 7 of 8 labels bound to a contract property; 8 of 96 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "createLiveDynamicPrice": {
  "method": "POST",
  "path": "/live-dynamic-price",
  "contract": "catalogue",
  "summary": "Live Dynamic Price Execution & Deployment Monitor",
  "permission": "PRODUCT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "LiveDynamicPriceExecutionDeploymentMonitorInput",
  "responds": "LiveDynamicPriceExecutionDeploymentMonitorView"
 },
 "listAutomationPolicyAutonomous": {
  "method": "GET",
  "path": "/automation-policy-autonomou",
  "contract": "catalogue",
  "summary": "Automation Policy & Autonomous Pricing Orchestrator",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AutomationPolicyAutonomousPricingOrchestratorView"
 },
 "listDynamicPricingPerformance": {
  "method": "GET",
  "path": "/dynamic-pricing-performance",
  "contract": "catalogue",
  "summary": "Dynamic Pricing Performance & Optimization Analytics",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "DynamicPricingPerformanceOptimizationAnalyticsView"
 },
 "listLearningModelPerformance": {
  "method": "GET",
  "path": "/learning-model-performance",
  "contract": "catalogue",
  "summary": "AI Learning, Model Performance & Optimization Feedback",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AiLearningModelPerformanceOptimizationFeedbackView"
 },
 "listRecommendationReviewDecision": {
  "method": "GET",
  "path": "/recommendation-review-decision",
  "contract": "catalogue",
  "summary": "AI Recommendation Review & Decision Queue",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AiRecommendationReviewDecisionQueueView"
 },
 "listRevenue": {
  "method": "GET",
  "path": "/revenue",
  "contract": "catalogue",
  "summary": "Revenue Optimization Command Center",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "RevenueOptimizationCommandCenterView"
 },
 "listRevenueDemandImpact": {
  "method": "GET",
  "path": "/revenue-demand-impact",
  "contract": "catalogue",
  "summary": "Revenue & Demand Impact Forecasting",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "RevenueDemandImpactForecastingView"
 },
 "listScenarioModelingWhat": {
  "method": "GET",
  "path": "/scenario-modeling-what",
  "contract": "catalogue",
  "summary": "Scenario Modeling & What-If Analysis",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ScenarioModelingWhatIfAnalysisView"
 },
 "setPricing": {
  "method": "PUT",
  "path": "/pricing-2",
  "contract": "catalogue",
  "summary": "Pricing Simulation Studio",
  "permission": "PRODUCT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "PricingSimulationStudioInput",
  "responds": "PricingSimulationStudioView"
 },
 "setPricingExperiment": {
  "method": "PUT",
  "path": "/pricing-experiment",
  "contract": "catalogue",
  "summary": "A/B Pricing Experiment Studio",
  "permission": "PRODUCT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "ABPricingExperimentStudioInput",
  "responds": "ABPricingExperimentStudioView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "ABPricingExperimentStudioInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table covers these fields** — the closest is catalogue.channel_allocation at 5%, so this is not an update to anything the package stores today and no new table has been decided",
  "description": "**What A/B Pricing Experiment Studio submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "experimentName": {
    "type": "string",
    "description": "Experiment Name"
   },
   "objective": {
    "type": "string",
    "description": "Objective"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "performance": {
    "type": "string",
    "description": "Performance"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "customerSegment": {
    "type": "string",
    "description": "Customer Segment"
   },
   "startDate": {
    "type": "string",
    "format": "date-time",
    "description": "Start Date"
   },
   "endDate": {
    "type": "string",
    "format": "date-time",
    "description": "End Date"
   },
   "revenue78": {
    "type": "number",
    "description": "Revenue +7.8%"
   },
   "conversion12": {
    "type": "number",
    "description": "Conversion −1.2%"
   },
   "asp6": {
    "type": "number",
    "description": "ASP +6%"
   },
   "confidence96": {
    "type": "number",
    "description": "Confidence 96%"
   },
   "aAed250": {
    "type": "string",
    "description": "A — AED 250"
   },
   "bAed260": {
    "type": "string",
    "description": "B — AED 260"
   },
   "cAed270": {
    "type": "string",
    "description": "C — AED 270"
   },
   "selectType": {
    "type": "string",
    "enum": [
     "revenue",
     "conversion",
     "averageSellingPrice",
     "margin",
     "sellThrough",
     "occupancy",
     "revenuePerVisitor"
    ],
    "description": "Vocabulary listed under Select."
   },
   "minimumPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Minimum Price"
   },
   "maximumPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Maximum Price"
   },
   "contractRates": {
    "type": "string",
    "description": "Contract Rates"
   },
   "membershipRates": {
    "type": "string",
    "description": "Membership Rates"
   },
   "regulatoryRequirements": {
    "type": "string",
    "description": "Regulatory Requirements"
   }
  }
 },
 "ABPricingExperimentStudioView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What A/B Pricing Experiment Studio displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "experimentName": {
    "type": "string",
    "description": "Experiment Name"
   },
   "objective": {
    "type": "string",
    "description": "Objective"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "performance": {
    "type": "string",
    "description": "Performance"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "customerSegment": {
    "type": "string",
    "description": "Customer Segment"
   },
   "startDate": {
    "type": "string",
    "format": "date-time",
    "description": "Start Date"
   },
   "endDate": {
    "type": "string",
    "format": "date-time",
    "description": "End Date"
   },
   "revenue78": {
    "type": "number",
    "description": "Revenue +7.8%"
   },
   "conversion12": {
    "type": "number",
    "description": "Conversion −1.2%"
   },
   "asp6": {
    "type": "number",
    "description": "ASP +6%"
   },
   "confidence96": {
    "type": "number",
    "description": "Confidence 96%"
   },
   "aAed250": {
    "type": "string",
    "description": "A — AED 250"
   },
   "bAed260": {
    "type": "string",
    "description": "B — AED 260"
   },
   "cAed270": {
    "type": "string",
    "description": "C — AED 270"
   },
   "selectType": {
    "type": "string",
    "enum": [
     "revenue",
     "conversion",
     "averageSellingPrice",
     "margin",
     "sellThrough",
     "occupancy",
     "revenuePerVisitor"
    ],
    "description": "Vocabulary listed under Select."
   },
   "minimumPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Minimum Price"
   },
   "maximumPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Maximum Price"
   },
   "contractRates": {
    "type": "string",
    "description": "Contract Rates"
   },
   "membershipRates": {
    "type": "string",
    "description": "Membership Rates"
   },
   "regulatoryRequirements": {
    "type": "string",
    "description": "Regulatory Requirements"
   },
   "sampleSize": {
    "type": "string",
    "description": "Sample Size"
   },
   "confidenceLevel": {
    "type": "string",
    "description": "Confidence Level"
   },
   "experimentDuration": {
    "type": "string",
    "format": "date-time",
    "description": "Experiment Duration"
   },
   "statisticalSignificance": {
    "type": "string",
    "description": "Statistical Significance"
   }
  }
 },
 "AiLearningModelPerformanceOptimizationFeedbackView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What AI Learning, Model Performance & Optimization Feedback displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "forecastError": {
    "type": "string",
    "description": "Forecast Error (the pack shows +2.3%)"
   },
   "aed256m": {
    "type": "string",
    "description": "AED 2.56M"
   },
   "demandForecastAccuracy": {
    "type": "string",
    "description": "Demand Forecast Accuracy"
   },
   "revenueForecastAccuracy": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue Forecast Accuracy"
   },
   "elasticityAccuracy": {
    "type": "number",
    "description": "Elasticity Accuracy"
   },
   "recommendationSuccess": {
    "type": "string",
    "description": "Recommendation Success"
   },
   "confidenceCalibration": {
    "type": "string",
    "description": "Confidence Calibration"
   },
   "falsePositiveRate": {
    "type": "number",
    "description": "False Positive Rate"
   },
   "revenueUplift": {
    "type": "number",
    "description": "Revenue Uplift"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "eventType": {
    "type": "string",
    "description": "Event Type"
   },
   "season": {
    "type": "string",
    "description": "Season"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "market": {
    "type": "string",
    "description": "Market"
   },
   "forecastHorizon": {
    "type": "string",
    "description": "Forecast Horizon"
   },
   "high96": {
    "type": "number",
    "description": "High 96%"
   },
   "occupancyHigh98": {
    "type": "integer",
    "description": "Occupancy High 98%"
   },
   "weatherMedium87": {
    "type": "number",
    "description": "Weather Medium 87%"
   },
   "high91": {
    "type": "number",
    "description": "High 91%"
   },
   "competitorMedium82": {
    "type": "number",
    "description": "Competitor Medium 82%"
   },
   "configuredAndGoverned": {
    "type": "string",
    "description": "configured and governed"
   },
   "definesTheCommercialPriceStructures": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Defines the commercial price structures"
   },
   "calculatesTheFinalPayableAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Calculates the final payable amount"
   },
   "wouldFreezeForDevelopmentTeam": {
    "type": "string",
    "description": "would freeze for Development team"
   }
  }
 },
 "AiRecommendationReviewDecisionQueueView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What AI Recommendation Review & Decision Queue displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "recommendation": {
    "type": "string",
    "description": "Recommendation"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "currentPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Current Price"
   },
   "recommendedPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Recommended Price"
   },
   "change": {
    "type": "number",
    "description": "Change %"
   },
   "revenueOpportunity": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue Opportunity"
   },
   "demandImpact": {
    "type": "string",
    "description": "Demand Impact"
   },
   "confidence": {
    "type": "string",
    "description": "Confidence"
   },
   "urgency": {
    "type": "string",
    "description": "Urgency"
   },
   "governanceLevel": {
    "type": "string",
    "description": "Governance Level"
   },
   "fromBoard6": {
    "type": "string",
    "description": "from Board 6"
   },
   "fromBoard7": {
    "type": "string",
    "description": "from Board 7"
   },
   "simulationRevenueUplift": {
    "type": "number",
    "description": "Simulation Revenue Uplift (the pack shows +AED 73,400, 122 | Pag e)"
   },
   "accept": {
    "type": "string",
    "description": "Accept"
   },
   "modify": {
    "type": "string",
    "description": "Modify"
   },
   "simulateAgain": {
    "type": "string",
    "description": "Simulate Again"
   },
   "commercialJudgment": {
    "type": "string",
    "description": "Commercial Judgment"
   },
   "brandPositioning": {
    "type": "string",
    "description": "Brand Positioning"
   },
   "customerSensitivity": {
    "type": "string",
    "description": "Customer Sensitivity"
   },
   "eventStrategy": {
    "type": "string",
    "description": "Event Strategy"
   },
   "incorrectSignal": {
    "type": "string",
    "description": "Incorrect Signal"
   },
   "dataConcern": {
    "type": "string",
    "description": "Data Concern"
   },
   "theSystemRecordsTheModification": {
    "type": "string",
    "description": "The system records the modification"
   },
   "actualRevenueResult59": {
    "type": "number",
    "description": "Actual Revenue Result +5.9%"
   }
  }
 },
 "AutomationPolicyAutonomousPricingOrchestratorView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Automation Policy & Autonomous Pricing Orchestrator displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "tenant": {
    "type": "string",
    "description": "Tenant"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "strategy": {
    "type": "string",
    "description": "Strategy"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "market": {
    "type": "string",
    "description": "Market"
   },
   "dateTime": {
    "type": "string",
    "format": "date-time",
    "description": "Date/Time"
   },
   "evaluationFrequency": {
    "type": "string",
    "description": "Evaluation Frequency"
   },
   "executionFrequency": {
    "type": "string",
    "description": "Execution Frequency"
   },
   "minimumTimeBetweenChanges": {
    "type": "string",
    "format": "date-time",
    "description": "Minimum Time Between Changes"
   },
   "maximumChangesPerDay": {
    "type": "string",
    "description": "Maximum Changes per Day"
   },
   "aiRecommendsOnly": {
    "type": "string",
    "description": "AI recommends only"
   },
   "aiRecommendsHumanApproval": {
    "type": "string",
    "description": "AI recommends → human approval"
   },
   "guardrailsPassed": {
    "type": "string",
    "description": "Guardrails Passed"
   },
   "noProtectedRate": {
    "type": "number",
    "description": "No Protected Rate"
   },
   "forecastDataHealthy": {
    "type": "string",
    "description": "Forecast Data Healthy"
   },
   "dataQualityFalls": {
    "type": "string",
    "description": "Data Quality Falls"
   },
   "modelConfidenceDrops": {
    "type": "string",
    "description": "Model Confidence Drops"
   },
   "conversionDropsAbnormally": {
    "type": "number",
    "description": "Conversion Drops Abnormally"
   },
   "priceVolatilityExceedsThreshold": {
    "type": "integer",
    "description": "Price Volatility Exceeds Threshold"
   },
   "revenueFalls": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue Falls"
   },
   "integrationFails": {
    "type": "string",
    "description": "Integration Fails"
   },
   "withStrictPermissionControl": {
    "type": "string",
    "description": "with strict permission control"
   }
  }
 },
 "DynamicPricingPerformanceOptimizationAnalyticsView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Dynamic Pricing Performance & Optimization Analytics displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "incrementalRevenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Incremental Revenue"
   },
   "revenueUplift": {
    "type": "number",
    "description": "Revenue Uplift %"
   },
   "marginUplift": {
    "type": "number",
    "description": "Margin Uplift"
   },
   "averageSellingPrice": {
    "type": "number",
    "description": "Average Selling Price"
   },
   "conversion": {
    "type": "number",
    "description": "Conversion"
   },
   "attendance": {
    "type": "integer",
    "description": "Attendance"
   },
   "occupancy": {
    "type": "integer",
    "description": "Occupancy"
   },
   "sellThrough": {
    "type": "string",
    "description": "Sell-Through"
   },
   "revenuePerAvailableCapacity": {
    "type": "integer",
    "description": "Revenue per Available Capacity"
   },
   "numberOfPriceChanges": {
    "type": "integer",
    "description": "Number of Price Changes"
   },
   "strategyRoi": {
    "type": "string",
    "description": "Strategy ROI"
   },
   "recommendationsGenerated": {
    "type": "string",
    "description": "Recommendations Generated"
   },
   "accepted": {
    "type": "string",
    "description": "Accepted"
   },
   "rejected": {
    "type": "integer",
    "description": "Rejected"
   },
   "modified": {
    "type": "string",
    "description": "Modified"
   },
   "autoExecuted": {
    "type": "string",
    "description": "Auto-Executed"
   },
   "successful": {
    "type": "string",
    "description": "Successful"
   },
   "negativeOutcome": {
    "type": "string",
    "description": "Negative Outcome"
   },
   "dynamicVsFixedPricing": {
    "type": "string",
    "description": "Dynamic vs Fixed Pricing"
   },
   "aiVsRules": {
    "type": "string",
    "description": "AI vs Rules"
   },
   "aiVsHuman": {
    "type": "string",
    "description": "AI vs Human"
   },
   "strategyVsStrategy": {
    "type": "string",
    "description": "Strategy vs Strategy"
   },
   "venueVsVenue": {
    "type": "string",
    "description": "Venue vs Venue"
   },
   "eventVsEvent": {
    "type": "string",
    "description": "Event vs Event"
   },
   "channelVsChannel": {
    "type": "string",
    "description": "Channel vs Channel"
   },
   "currentVsPreviousPeriod": {
    "type": "string",
    "format": "date-time",
    "description": "Current vs Previous Period"
   },
   "revenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue (the pack shows +8.4%)"
   },
   "asp": {
    "type": "string",
    "description": "ASP (the pack shows +6.2%)"
   },
   "margin": {
    "type": "number",
    "description": "Margin (the pack shows +9.7%)"
   },
   "with": {
    "type": "string",
    "description": "with"
   },
   "demand": {
    "type": "string",
    "description": "Demand"
   },
   "bookingVelocity": {
    "type": "string",
    "description": "Booking Velocity"
   },
   "movement": {
    "type": "string",
    "description": "movement"
   },
   "recommendationsWereRejected": {
    "type": "string",
    "description": "recommendations were rejected"
   }
  }
 },
 "LiveDynamicPriceExecutionDeploymentMonitorInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Live Dynamic Price Execution & Deployment Monitor submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "timestamp": {
    "type": "string",
    "format": "date-time",
    "description": "Timestamp"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "previousPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Previous Price"
   },
   "newPrice": {
    "type": "integer",
    "description": "New Price"
   },
   "strategy": {
    "type": "string",
    "description": "Strategy"
   },
   "aiRecommendation": {
    "type": "string",
    "description": "AI Recommendation"
   },
   "approval": {
    "type": "string",
    "description": "Approval"
   },
   "executionSource": {
    "type": "string",
    "description": "Execution Source"
   },
   "status": {
    "type": "string",
    "description": "Status"
   },
   "aed250Aed265": {
    "type": "string",
    "description": "AED 250 → AED 265"
   },
   "bookingVelocityOccupancy": {
    "type": "integer",
    "description": "Booking Velocity + Occupancy"
   },
   "priceInconsistencyDetected": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price inconsistency detected"
   },
   "hold": {
    "type": "string",
    "description": "Hold"
   },
   "revert": {
    "type": "string",
    "description": "Revert"
   }
  }
 },
 "LiveDynamicPriceExecutionDeploymentMonitorView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Live Dynamic Price Execution & Deployment Monitor displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "timestamp": {
    "type": "string",
    "format": "date-time",
    "description": "Timestamp"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "previousPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Previous Price"
   },
   "newPrice": {
    "type": "integer",
    "description": "New Price"
   },
   "strategy": {
    "type": "string",
    "description": "Strategy"
   },
   "aiRecommendation": {
    "type": "string",
    "description": "AI Recommendation"
   },
   "approval": {
    "type": "string",
    "description": "Approval"
   },
   "executionSource": {
    "type": "string",
    "description": "Execution Source"
   },
   "status": {
    "type": "string",
    "description": "Status"
   },
   "aed250Aed265": {
    "type": "string",
    "description": "AED 250 → AED 265"
   },
   "bookingVelocityOccupancy": {
    "type": "integer",
    "description": "Booking Velocity + Occupancy"
   },
   "b2c": {
    "type": "string",
    "description": "B2C"
   },
   "mobileApp": {
    "type": "string",
    "description": "Mobile App"
   },
   "pos": {
    "type": "integer",
    "description": "POS"
   },
   "kiosk": {
    "type": "string",
    "description": "Kiosk"
   },
   "callCenter": {
    "type": "string",
    "description": "Call Center"
   },
   "b2b": {
    "type": "string",
    "description": "B2B"
   },
   "reseller": {
    "type": "string",
    "description": "Reseller"
   },
   "ota": {
    "type": "string",
    "description": "OTA"
   },
   "apis": {
    "type": "integer",
    "description": "APIs"
   },
   "priceInconsistencyDetected": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price inconsistency detected"
   },
   "hold": {
    "type": "string",
    "description": "Hold"
   },
   "revert": {
    "type": "string",
    "description": "Revert"
   }
  }
 },
 "PricingSimulationStudioInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Pricing Simulation Studio submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "manualPriceChange": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Manual Price Change"
   },
   "board5DynamicRule": {
    "type": "string",
    "description": "Board 5 Dynamic Rule"
   },
   "board6AiRecommendation": {
    "type": "string",
    "description": "Board 6 AI Recommendation"
   },
   "newDynamicStrategy": {
    "type": "integer",
    "description": "New Dynamic Strategy"
   },
   "existingStrategyModification": {
    "type": "string",
    "description": "Existing Strategy Modification"
   },
   "bulkPriceChange": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Bulk Price Change"
   },
   "selectType": {
    "type": "string",
    "enum": [
     "venue",
     "product",
     "event",
     "performance",
     "timeslot",
     "priceCategory",
     "channel",
     "customerSegment",
     "dateRange"
    ],
    "description": "Vocabulary listed under Select."
   },
   "expectedDemand": {
    "type": "string",
    "description": "Expected Demand"
   },
   "expectedConversion": {
    "type": "number",
    "description": "Expected Conversion"
   },
   "expectedAttendance": {
    "type": "integer",
    "description": "Expected Attendance"
   },
   "expectedOccupancy": {
    "type": "integer",
    "description": "Expected Occupancy"
   },
   "expectedRevenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Expected Revenue"
   },
   "expectedMargin": {
    "type": "number",
    "description": "Expected Margin"
   },
   "expectedSellThrough": {
    "type": "string",
    "description": "Expected Sell-Through"
   },
   "expectedSellOutTime": {
    "type": "string",
    "format": "date-time",
    "description": "Expected Sell-Out Time"
   },
   "averageSellingPrice": {
    "type": "number",
    "description": "Average Selling Price"
   },
   "commercialGuardrailPass": {
    "type": "string",
    "description": "Commercial Guardrail — PASS"
   },
   "contractProtectionPass": {
    "type": "string",
    "description": "Contract Protection — PASS"
   },
   "priceLadderPass": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price Ladder — PASS"
   },
   "approvalThresholdRevenueManager": {
    "type": "integer",
    "description": "Approval Threshold — Revenue Manager"
   },
   "startExperiment": {
    "type": "string",
    "description": "Start Experiment"
   },
   "discard": {
    "type": "string",
    "description": "Discard"
   }
  }
 },
 "PricingSimulationStudioView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Pricing Simulation Studio displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "manualPriceChange": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Manual Price Change"
   },
   "board5DynamicRule": {
    "type": "string",
    "description": "Board 5 Dynamic Rule"
   },
   "board6AiRecommendation": {
    "type": "string",
    "description": "Board 6 AI Recommendation"
   },
   "newDynamicStrategy": {
    "type": "integer",
    "description": "New Dynamic Strategy"
   },
   "existingStrategyModification": {
    "type": "string",
    "description": "Existing Strategy Modification"
   },
   "bulkPriceChange": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Bulk Price Change"
   },
   "selectType": {
    "type": "string",
    "enum": [
     "venue",
     "product",
     "event",
     "performance",
     "timeslot",
     "priceCategory",
     "channel",
     "customerSegment",
     "dateRange"
    ],
    "description": "Vocabulary listed under Select."
   },
   "expectedDemand": {
    "type": "string",
    "description": "Expected Demand"
   },
   "expectedConversion": {
    "type": "number",
    "description": "Expected Conversion"
   },
   "expectedAttendance": {
    "type": "integer",
    "description": "Expected Attendance"
   },
   "expectedOccupancy": {
    "type": "integer",
    "description": "Expected Occupancy"
   },
   "expectedRevenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Expected Revenue"
   },
   "expectedMargin": {
    "type": "number",
    "description": "Expected Margin"
   },
   "expectedSellThrough": {
    "type": "string",
    "description": "Expected Sell-Through"
   },
   "expectedSellOutTime": {
    "type": "string",
    "format": "date-time",
    "description": "Expected Sell-Out Time"
   },
   "averageSellingPrice": {
    "type": "number",
    "description": "Average Selling Price"
   },
   "simulationConfidence89": {
    "type": "number",
    "description": "Simulation Confidence: 89%"
   },
   "basedOn": {
    "type": "string",
    "description": "based on"
   },
   "dataVolume": {
    "type": "integer",
    "description": "Data Volume"
   },
   "historicalSimilarity": {
    "type": "string",
    "description": "Historical Similarity"
   },
   "forecastConfidence": {
    "type": "string",
    "description": "Forecast Confidence"
   },
   "elasticityConfidence": {
    "type": "number",
    "description": "Elasticity Confidence"
   },
   "externalSignalQuality": {
    "type": "string",
    "description": "External Signal Quality"
   },
   "commercialGuardrailPass": {
    "type": "string",
    "description": "Commercial Guardrail — PASS"
   },
   "contractProtectionPass": {
    "type": "string",
    "description": "Contract Protection — PASS"
   },
   "priceLadderPass": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price Ladder — PASS"
   },
   "approvalThresholdRevenueManager": {
    "type": "integer",
    "description": "Approval Threshold — Revenue Manager"
   },
   "startExperiment": {
    "type": "string",
    "description": "Start Experiment"
   },
   "discard": {
    "type": "string",
    "description": "Discard"
   }
  }
 },
 "RevenueDemandImpactForecastingView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Revenue & Demand Impact Forecasting displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "expectedRevenueAed245m": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Expected Revenue: AED 2.45M"
   },
   "expectedDemand9800": {
    "type": "string",
    "description": "Expected Demand: 9,800"
   },
   "expectedOccupancy91": {
    "type": "integer",
    "description": "Expected Occupancy: 91%"
   },
   "expectedRevenueAed252m": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Expected Revenue: AED 2.52M"
   },
   "expectedDemand9500": {
    "type": "string",
    "description": "Expected Demand: 9,500"
   },
   "expectedOccupancy89": {
    "type": "integer",
    "description": "Expected Occupancy: 89%"
   },
   "aed70k29": {
    "type": "number",
    "description": "+AED 70K / +2.9%"
   },
   "aed62k": {
    "type": "string",
    "description": "+AED 62K"
   },
   "revenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue"
   },
   "demand": {
    "type": "string",
    "description": "Demand"
   },
   "attendance": {
    "type": "integer",
    "description": "Attendance"
   },
   "occupancy": {
    "type": "integer",
    "description": "Occupancy"
   },
   "conversion": {
    "type": "number",
    "description": "Conversion"
   },
   "margin": {
    "type": "number",
    "description": "Margin"
   },
   "asp": {
    "type": "string",
    "description": "ASP"
   },
   "sellThrough": {
    "type": "string",
    "description": "Sell-Through"
   },
   "sellOutProbability": {
    "type": "string",
    "description": "Sell-Out Probability"
   },
   "memberImpact": {
    "type": "string",
    "description": "Member Impact"
   },
   "residentImpact": {
    "type": "string",
    "description": "Resident Impact"
   },
   "touristImpact": {
    "type": "string",
    "description": "Tourist Impact"
   },
   "familyImpact": {
    "type": "string",
    "description": "Family Impact"
   },
   "b2bImpact": {
    "type": "string",
    "description": "B2B Impact"
   },
   "customersToAnotherProduct": {
    "type": "string",
    "description": "customers to another product"
   }
  }
 },
 "RevenueOptimizationCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Revenue Optimization Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "revenueOpportunity": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue Opportunity"
   },
   "incrementalRevenueGenerated": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Incremental Revenue Generated"
   },
   "activeOptimizations": {
    "type": "integer",
    "description": "Active Optimizations"
   },
   "recommendationsAwaitingAction": {
    "type": "string",
    "description": "Recommendations Awaiting Action"
   },
   "pendingSimulations": {
    "type": "integer",
    "description": "Pending Simulations"
   },
   "autoExecutedChanges": {
    "type": "integer",
    "description": "Auto-Executed Changes"
   },
   "approvalRequired": {
    "type": "boolean",
    "description": "Approval Required"
   },
   "activeABTests": {
    "type": "integer",
    "description": "Active A/B Tests"
   },
   "pricingExceptions": {
    "type": "integer",
    "description": "Pricing Exceptions"
   },
   "revenueAtRisk": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue at Risk"
   },
   "forecastAccuracy": {
    "type": "string",
    "description": "Forecast Accuracy"
   },
   "optimizationSuccessRate": {
    "type": "number",
    "description": "Optimization Success Rate"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "eventProduct": {
    "type": "string",
    "description": "Event/Product"
   },
   "performance": {
    "type": "string",
    "description": "Performance"
   },
   "currentPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Current Price"
   },
   "recommendedPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Recommended Price"
   },
   "forecastRevenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Forecast Revenue"
   },
   "expectedUplift": {
    "type": "number",
    "description": "Expected Uplift"
   },
   "confidence": {
    "type": "string",
    "description": "Confidence"
   },
   "automationMode": {
    "type": "string",
    "description": "Automation Mode"
   },
   "approvalStatus": {
    "type": "string",
    "description": "Approval Status"
   },
   "executionStatus": {
    "type": "string",
    "description": "Execution Status"
   },
   "ntEdItyCe": {
    "type": "string",
    "description": "nt ed ity ce"
   },
   "aed235Aed41k88": {
    "type": "number",
    "description": "AED 235 +AED 41K 88%"
   },
   "revenueRisk": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue Risk"
   },
   "eventProximity": {
    "type": "string",
    "description": "Event Proximity"
   },
   "inventoryPosition": {
    "type": "string",
    "description": "Inventory Position"
   },
   "demandVariance": {
    "type": "string",
    "description": "Demand Variance"
   },
   "urgency": {
    "type": "string",
    "description": "Urgency"
   },
   "startExperiment": {
    "type": "string",
    "description": "Start Experiment"
   }
  }
 },
 "ScenarioModelingWhatIfAnalysisView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Scenario Modeling & What-If Analysis displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "lowDemand": {
    "type": "string",
    "description": "Low Demand"
   },
   "expectedDemand": {
    "type": "string",
    "description": "Expected Demand"
   },
   "highDemand": {
    "type": "string",
    "description": "High Demand"
   },
   "sellOut": {
    "type": "string",
    "description": "Sell-Out"
   },
   "competitorPriceDrop": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Competitor Price Drop"
   },
   "competitorPriceIncrease": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Competitor Price Increase"
   },
   "extremeWeather": {
    "type": "string",
    "description": "Extreme Weather"
   },
   "rain": {
    "type": "string",
    "description": "Rain"
   },
   "nearbyExhibition": {
    "type": "string",
    "description": "Nearby Exhibition"
   },
   "majorConcert": {
    "type": "string",
    "description": "Major Concert"
   },
   "tourismSurge": {
    "type": "string",
    "description": "Tourism Surge"
   },
   "cancellationSurge": {
    "type": "string",
    "description": "Cancellation Surge"
   },
   "inventoryReduction": {
    "type": "string",
    "description": "Inventory Reduction"
   },
   "customScenario": {
    "type": "string",
    "description": "Custom Scenario"
   },
   "demand": {
    "type": "number",
    "description": "Demand ±%"
   },
   "occupancy": {
    "type": "integer",
    "description": "Occupancy"
   },
   "inventory": {
    "type": "string",
    "description": "Inventory"
   },
   "bookingVelocity": {
    "type": "string",
    "description": "Booking Velocity"
   },
   "weatherImpact": {
    "type": "string",
    "description": "Weather Impact"
   },
   "nearbyEventImpact": {
    "type": "string",
    "description": "Nearby Event Impact"
   },
   "competitorPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Competitor Price"
   },
   "conversion": {
    "type": "number",
    "description": "Conversion"
   },
   "price": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price"
   },
   "eventProximity": {
    "type": "string",
    "description": "Event Proximity"
   },
   "remainingCapacity": {
    "type": "integer",
    "description": "Remaining Capacity (the pack shows 24%)"
   },
   "avgPrice250262270": {
    "type": "number",
    "description": "Avg. Price 250 262 270"
   },
   "revenue255m261m": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue 2.55M 2.61M"
   },
   "margin191m198m": {
    "type": "number",
    "description": "Margin 1.91M 1.98M"
   },
   "share": {
    "type": "number",
    "description": "Share"
   }
  }
 }
}
```
