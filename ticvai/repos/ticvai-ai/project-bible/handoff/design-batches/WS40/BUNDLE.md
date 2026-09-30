# WS40 — Pricing   Revenue Management board 7

**10 screens · 13 operations · 20 schemas · 5 permissions**

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

- **Every control that can be refused must be gated.** 5 permissions apply here:
  `AI_APPROVE, AI_CONFIGURE, PRICE_CONFIGURE, PRODUCT_CONFIGURE, PRODUCT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
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
| `ADM-113` | AI Recommendation Review & Decision Queue | listDetail | 2 | 0 | — |
| `ADM-114` | Automation Policy & Autonomous Pricing Orchestrator | configEditor | 2 | 1 | — |
| `ADM-115` | Live Dynamic Price Execution & Deployment Monitor | listDetail | 1 | 0 | — |
| `ADM-116` | Dynamic Pricing Performance & Optimization Analytics | listDetail | 1 | 0 | — |
| `ADM-117` | AI Learning, Model Performance & Optimization Feedback | listDetail | 2 | 1 | — |

## Thin screens in this batch

**ADM-111, ADM-117 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

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
     "provenance": "derived — ADM-002 declares entryState.params  and ADM-108 holds none of them, so the edge carries nothing and ADM-002 opens cold"
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
    },
    {
     "to": "ADM-113",
     "trigger": "Works in AI Recommendation Review & Decision Queue",
     "provenance": "flow F149 step 9→10",
     "operation": "listRevenue",
     "carries": [
      "recommendationId"
     ]
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Revenue teams can monitor and act on pricing optimization opportunities across the organization from one centralized workspace.",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each row displays) — counts over a population, then the population",
  "purpose": "Provide Revenue Managers with the operational control center for all dynamic pricing simulations, AI recommendations, automated changes, experiments and revenue optimization activity.",
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
       "bindsTo": "RevenueOptimizationCommandCenterSummary.incrementalRevenueGenerated"
      },
      {
       "kind": "metricTile",
       "label": "Active Optimizations",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 114 §Display",
       "bindsTo": "RevenueOptimizationCommandCenterSummary.activeOptimizations"
      },
      {
       "kind": "metricTile",
       "label": "Recommendations Awaiting Action",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 114 §Display",
       "bindsTo": "RevenueOptimizationCommandCenterSummary.recommendationsAwaitingAction"
      },
      {
       "kind": "metricTile",
       "label": "Pending Simulations",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 114 §Display",
       "bindsTo": "RevenueOptimizationCommandCenterSummary.pendingSimulations"
      },
      {
       "kind": "metricTile",
       "label": "Auto-Executed Changes",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 114 §Display",
       "bindsTo": "RevenueOptimizationCommandCenterSummary.autoExecutedChanges"
      },
      {
       "kind": "metricTile",
       "label": "Approval Required",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 114 §Display",
       "bindsTo": "RevenueOptimizationCommandCenterSummary.approvalRequired"
      },
      {
       "kind": "metricTile",
       "label": "Active A/B Tests",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 114 §Display",
       "bindsTo": "RevenueOptimizationCommandCenterSummary.activeABTests"
      },
      {
       "kind": "metricTile",
       "label": "Pricing Exceptions",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 114 §Display",
       "bindsTo": "RevenueOptimizationCommandCenterSummary.pricingExceptions"
      },
      {
       "kind": "metricTile",
       "label": "Revenue at Risk",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 114 §Display",
       "bindsTo": "RevenueOptimizationCommandCenterSummary.revenueAtRisk"
      },
      {
       "kind": "metricTile",
       "label": "Forecast Accuracy",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 114 §Display",
       "bindsTo": "RevenueOptimizationCommandCenterSummary.forecastAccuracy"
      },
      {
       "kind": "metricTile",
       "label": "Optimization Success Rate",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 114 §Display",
       "bindsTo": "RevenueOptimizationCommandCenterSummary.optimizationSuccessRate"
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-108",
   "workshopBoard": "wireframes/WS101 Pricing   Revenue Management Board 7.dc.html#adm-108"
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
  "purposeNote": "Authorized users can safely evaluate a pricing recommendation or strategy against forecast commercial outcomes without modifying production prices.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Allow any proposed dynamic-pricing change to be tested before affecting live customers. This should become the sandbox of the Dynamic Pricing Engine.",
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
        "PricingSimulationStudioView.simulationConfidence",
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
        "PricingSimulationStudioView.simulationConfidence",
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
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "preloaded": [
    "PricingSimulationStudioView.simulationConfidence",
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-109",
   "workshopBoard": "wireframes/WS101 Pricing   Revenue Management Board 7.dc.html#adm-109"
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
  "purposeNote": "Revenue teams can model alternative market and demand conditions and compare different pricing responses before implementation.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Scenario Modeling & What-If Analysis",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 11 actions on this screen and the screen declares 1 operation.** Unserved: Low Demand, Expected Demand, High Demand, Competitor Price Drop, Competitor Price Increase, Inventory Reduction, Custom Scenario, Save …. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
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
       "label": "Low Demand",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 117 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Expected Demand",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 117 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "High Demand",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 117 §Support"
      },
      {
       "kind": "secondaryButton",
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
       "label": "Inventory Reduction",
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
    "ScenarioModelingWhatIfAnalysisView.scenarioTypes"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-110",
   "workshopBoard": "wireframes/WS101 Pricing   Revenue Management Board 7.dc.html#adm-110"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 117. 0 of 0 labels bound to a contract property; 11 of 52 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "purposeNote": "Authorized users can execute controlled pricing experiments and determine statistically whether one strategy performs better than another.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Allow TICVAI to scientifically test different pricing strategies using controlled customer groups. This is essential because AI should learn from actual customer behavior, not only historical assumptions.",
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
    "trigger": "onAction"
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-111",
   "workshopBoard": "wireframes/WS101 Pricing   Revenue Management Board 7.dc.html#adm-111"
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
  "purposeNote": "Approvers can clearly understand expected revenue, demand and customer consequences before authorizing a dynamic pricing action.",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Forecast; Display) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide a dedicated commercial impact assessment before a dynamic-pricing action is approved or executed.",
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
   "preloaded": []
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-112",
   "workshopBoard": "wireframes/WS101 Pricing   Revenue Management Board 7.dc.html#adm-112"
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
  "purposeNote": "Every material AI recommendation can be reviewed, explained, simulated, approved, modified or rejected with complete traceability.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide the human decision workspace for recommendations produced by Board 6. This should be the Revenue Manager's inbox.",
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
       "notes": "**The pack separates these permissions; since 29 September the decision buttons are `decidePricingRecommendation` (AI_APPROVE)** — earlier text: Accept, Reject, Modify, Simulate Again, Schedule, Send for Approval. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 122 §Authorized users can"
      },
      {
       "kind": "primaryButton",
       "label": "Accept",
       "operation": "decidePricingRecommendation",
       "notes": "Sends `decision: accept`.",
       "provenance": "contract catalogue.yaml POST /recommendation-review-decision/{recommendationId}/decision (decided 29 September, readiness close-out)"
      },
      {
       "kind": "secondaryButton",
       "label": "Modify",
       "operation": "decidePricingRecommendation",
       "notes": "Sends `decision: modify`.",
       "provenance": "contract catalogue.yaml POST /recommendation-review-decision/{recommendationId}/decision (decided 29 September, readiness close-out)"
      },
      {
       "kind": "secondaryButton",
       "label": "Reject",
       "operation": "decidePricingRecommendation",
       "notes": "Sends `decision: reject`.",
       "provenance": "contract catalogue.yaml POST /recommendation-review-decision/{recommendationId}/decision (decided 29 September, readiness close-out)"
      },
      {
       "kind": "secondaryButton",
       "label": "Schedule",
       "operation": "decidePricingRecommendation",
       "notes": "Sends `decision: schedule`.",
       "provenance": "contract catalogue.yaml POST /recommendation-review-decision/{recommendationId}/decision (decided 29 September, readiness close-out)"
      },
      {
       "kind": "secondaryButton",
       "label": "Send for approval",
       "operation": "decidePricingRecommendation",
       "notes": "Sends `decision: sendForApproval`.",
       "provenance": "contract catalogue.yaml POST /recommendation-review-decision/{recommendationId}/decision (decided 29 September, readiness close-out)"
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
   },
   {
    "operationId": "decidePricingRecommendation",
    "contract": "catalogue",
    "purpose": "Record a human decision on an AI pricing recommendation",
    "trigger": "onAction"
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
   ],
   "params": [
    {
     "name": "recommendationId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-113",
   "workshopBoard": "wireframes/WS101 Pricing   Revenue Management Board 7.dc.html#adm-113"
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
  "purposeNote": "confidence, commercial guardrails and emergency safety controls.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Control when TICVAI is allowed to execute pricing changes automatically. Board 5 defines the strategy-level automation permission. This screen manages operational autonomous execution at scale.",
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
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save dynamic pricing guardrail policy",
       "operation": "setDynamicPricingGuardrailPolicy",
       "permission": "PRICE_CONFIGURE",
       "notes": "**Guardrails and automation policy, one row per scope** (29 September, writers pass).",
       "provenance": "contract catalogue.yaml PUT /dynamic-pricing-controls"
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
   },
   {
    "operationId": "setDynamicPricingGuardrailPolicy",
    "contract": "catalogue",
    "purpose": "Set the guardrails and automation level of dynamic pricing at one scope",
    "trigger": "onAction",
    "invalidates": [
     "listAutomationPolicyAutonomous"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-114",
   "workshopBoard": "wireframes/WS101 Pricing   Revenue Management Board 7.dc.html#adm-114"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 123. 0 of 0 labels bound to a contract property; 12 of 34 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formSetDynamicPricingGuardrailPolicy",
    "component": "modal",
    "trigger": "Save dynamic pricing guardrail policy",
    "body": "**Collects what `setDynamicPricingGuardrailPolicy` sends before it is called.** Required: `id`, `scopePath`, `scopeLevel`, `automationLevel`. Optional: `scopeId`, `absoluteMinimumPrice`, `absoluteMaximumPrice`, `minimumMarginPercent`, `maximumUpliftPercent`, `maximumReductionPercent`, `maximumSingleChangePercent`, `maximumDailyChangePercent`, `maximumWeeklyChangePercent`, `minimumChangeIntervalMinutes`, `maximumChangesPerDay`, `minimumInventory` and 21 more. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "DynamicPricingControl",
    "confirm": {
     "label": "Save dynamic pricing guardrail policy",
     "operation": "setDynamicPricingGuardrailPolicy"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "scopePath",
      "scopeLevel",
      "automationLevel",
      "scopeId",
      "absoluteMinimumPrice",
      "absoluteMaximumPrice",
      "minimumMarginPercent",
      "maximumUpliftPercent",
      "maximumReductionPercent",
      "maximumSingleChangePercent",
      "maximumDailyChangePercent",
      "maximumWeeklyChangePercent",
      "minimumChangeIntervalMinutes",
      "maximumChangesPerDay",
      "minimumInventory",
      "maximumOccupancyTriggerPercent",
      "protectedRateTypes"
     ]
    },
    "provenance": "contract catalogue.yaml PUT /dynamic-pricing-controls"
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
  "purposeNote": "Operations teams can monitor the real-time execution and distribution of dynamic prices across all applicable sales channels.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Each execution shows) and no metric row",
  "purpose": "Monitor pricing actions as they are executed across TICVAI's selling ecosystem.",
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
    "trigger": "onAction"
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-115",
   "workshopBoard": "wireframes/WS101 Pricing   Revenue Management Board 7.dc.html#adm-115"
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
  "purposeNote": "pricing strategies and AI recommendations.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Measure) and no metric row",
  "purpose": "Determine whether dynamic pricing actually improves TICVAI's commercial performance.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 4 actions on this screen and the screen declares 1 operation.** Unserved: Strategy vs Strategy, Venue vs Venue, Event vs Event, Channel vs Channel. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
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
       "label": "Venue vs Venue",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 126 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Event vs Event",
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-116",
   "workshopBoard": "wireframes/WS101 Pricing   Revenue Management Board 7.dc.html#adm-116"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 126. 18 of 18 labels bound to a contract property; 22 of 44 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "purposeNote": "outcomes and provides governed feedback for improving future pricing intelligence. Board 7 — Final Screen Register # Backend Screen Core Responsibility 10.7. Revenue Optimization Command Center Optimization operations 1 # Backend Screen Core Responsibility 10.7. Pricing Simulation Studio Test proposed pricing 2 10.7. Commercial scenario",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Forecast; Track; Detect) and no metric row",
  "purpose": "Close the intelligence loop by comparing AI predictions and recommendations with actual commercial outcomes. This is what allows the system to improve over time.",
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
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save signal registry policy",
       "operation": "setSignalRegistryPolicy",
       "permission": "AI_CONFIGURE",
       "notes": "**AI governance of signals and models** (29 September, writers pass).",
       "provenance": "contract catalogue.yaml PUT /signal-registry"
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
   },
   {
    "operationId": "setSignalRegistryPolicy",
    "contract": "catalogue",
    "purpose": "Register a signal or model and set how far AI may trust it",
    "trigger": "onAction",
    "invalidates": [
     "listLearningModelPerformance"
    ]
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-117",
   "workshopBoard": "wireframes/WS101 Pricing   Revenue Management Board 7.dc.html#adm-117"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 128. 7 of 8 labels bound to a contract property; 8 of 96 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formSetSignalRegistryPolicy",
    "component": "modal",
    "trigger": "Save signal registry policy",
    "body": "**Collects what `setSignalRegistryPolicy` sends before it is called.** Required: `id`, `scopePath`, `registryKind`, `name`, `trustLevel`. Optional: `category`, `provider`, `source`, `internalExternal`, `marketCode`, `refreshFrequency`, `aiUsePermissions`, `fallbackPolicy`, `status`, `ownerPrincipalId`, `purpose`, `deployedAt` and 5 more. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "SignalRegistryEntry",
    "confirm": {
     "label": "Save signal registry policy",
     "operation": "setSignalRegistryPolicy"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "scopePath",
      "registryKind",
      "name",
      "trustLevel",
      "category",
      "provider",
      "source",
      "internalExternal",
      "marketCode",
      "refreshFrequency",
      "aiUsePermissions",
      "fallbackPolicy",
      "status",
      "ownerPrincipalId",
      "purpose",
      "deployedAt",
      "trainingWindow"
     ]
    },
    "provenance": "contract catalogue.yaml PUT /signal-registry"
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "LiveDynamicPriceExecutionDeploymentMonitorInput",
  "responds": "LiveDynamicPriceExecutionDeploymentMonitorView"
 },
 "decidePricingRecommendation": {
  "method": "POST",
  "path": "/recommendation-review-decision/{recommendationId}/decision",
  "contract": "catalogue",
  "summary": "Record a human decision on an AI pricing recommendation",
  "permission": "AI_APPROVE",
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
  "requestBody": "PricingRecommendationDecisionInput",
  "responds": "PricingRecommendationDecision"
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
  "parameters": [
   {
    "name": "venue",
    "in": "query",
    "required": false
   },
   {
    "name": "automationLevel",
    "in": "query",
    "required": false
   },
   {
    "name": "strategy",
    "in": "query",
    "required": false
   },
   {
    "name": "paused",
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
 "listDynamicPricingPerformance": {
  "method": "GET",
  "path": "/dynamic-pricing-performance",
  "contract": "catalogue",
  "summary": "Dynamic Pricing Performance & Optimization Analytics",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "level",
    "in": "query",
    "required": false
   },
   {
    "name": "market",
    "in": "query",
    "required": false
   },
   {
    "name": "venue",
    "in": "query",
    "required": false
   },
   {
    "name": "event",
    "in": "query",
    "required": false
   },
   {
    "name": "channel",
    "in": "query",
    "required": false
   },
   {
    "name": "compareBy",
    "in": "query",
    "required": false
   },
   {
    "name": "dateFrom",
    "in": "query",
    "required": false
   },
   {
    "name": "dateTo",
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
 "listLearningModelPerformance": {
  "method": "GET",
  "path": "/learning-model-performance",
  "contract": "catalogue",
  "summary": "AI Learning, Model Performance & Optimization Feedback",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "modelName",
    "in": "query",
    "required": false
   },
   {
    "name": "venue",
    "in": "query",
    "required": false
   },
   {
    "name": "product",
    "in": "query",
    "required": false
   },
   {
    "name": "eventType",
    "in": "query",
    "required": false
   },
   {
    "name": "season",
    "in": "query",
    "required": false
   },
   {
    "name": "channel",
    "in": "query",
    "required": false
   },
   {
    "name": "market",
    "in": "query",
    "required": false
   },
   {
    "name": "forecastHorizon",
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
 "listRecommendationReviewDecision": {
  "method": "GET",
  "path": "/recommendation-review-decision",
  "contract": "catalogue",
  "summary": "AI Recommendation Review & Decision Queue",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "venue",
    "in": "query",
    "required": false
   },
   {
    "name": "event",
    "in": "query",
    "required": false
   },
   {
    "name": "urgency",
    "in": "query",
    "required": false
   },
   {
    "name": "decision",
    "in": "query",
    "required": false
   },
   {
    "name": "governanceLevel",
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
 "listRevenue": {
  "method": "GET",
  "path": "/revenue",
  "contract": "catalogue",
  "summary": "Revenue Optimization Command Center",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "venue",
    "in": "query",
    "required": false
   },
   {
    "name": "automationMode",
    "in": "query",
    "required": false
   },
   {
    "name": "urgency",
    "in": "query",
    "required": false
   },
   {
    "name": "rankBy",
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
 "listRevenueDemandImpact": {
  "method": "GET",
  "path": "/revenue-demand-impact",
  "contract": "catalogue",
  "summary": "Revenue & Demand Impact Forecasting",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "recommendationId",
    "in": "query",
    "required": false
   },
   {
    "name": "simulationId",
    "in": "query",
    "required": false
   },
   {
    "name": "venue",
    "in": "query",
    "required": false
   },
   {
    "name": "event",
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
 "listScenarioModelingWhat": {
  "method": "GET",
  "path": "/scenario-modeling-what",
  "contract": "catalogue",
  "summary": "Scenario Modeling & What-If Analysis",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "scenarioType",
    "in": "query",
    "required": false
   },
   {
    "name": "venue",
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
 "setDynamicPricingGuardrailPolicy": {
  "method": "PUT",
  "path": "/dynamic-pricing-controls",
  "contract": "catalogue",
  "summary": "Set the guardrails and automation level of dynamic pricing at one scope",
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
  "requestBody": "DynamicPricingControl",
  "responds": "DynamicPricingControl"
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "ABPricingExperimentStudioInput",
  "responds": "ABPricingExperimentStudioView"
 },
 "setSignalRegistryPolicy": {
  "method": "PUT",
  "path": "/signal-registry",
  "contract": "catalogue",
  "summary": "Register a signal or model and set how far AI may trust it",
  "permission": "AI_CONFIGURE",
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
  "requestBody": "SignalRegistryEntry",
  "responds": "SignalRegistryEntry"
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
    "description": "Product id"
   },
   "event": {
    "type": "string",
    "description": "Event id",
    "nullable": true
   },
   "performance": {
    "type": "string",
    "description": "Performance id",
    "nullable": true
   },
   "channel": {
    "$ref": "#/components/schemas/Channel",
    "description": "Channel"
   },
   "customerSegment": {
    "type": "string",
    "description": "Customer segment",
    "nullable": true
   },
   "startDate": {
    "type": "string",
    "description": "Start Date",
    "format": "date"
   },
   "endDate": {
    "type": "string",
    "description": "End Date",
    "format": "date"
   },
   "minimumPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Minimum Price no variant may go below"
   },
   "maximumPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Maximum Price no variant may exceed"
   },
   "variants": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "label": {
       "type": "string",
       "description": "Variant label (A = control)"
      },
      "price": {
       "$ref": "../shared/common.yaml#/components/schemas/Money",
       "description": "Variant price"
      },
      "trafficSharePercent": {
       "type": "number",
       "description": "Share of traffic, percent; variants sum to 100"
      }
     }
    },
    "description": "Variant Configuration: control plus 1-3 variants (decided 29 September, readiness close-out)"
   },
   "successMetrics": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "revenue",
      "conversion",
      "averageSellingPrice",
      "margin",
      "sellThrough",
      "occupancy",
      "revenuePerVisitor"
     ]
    },
    "description": "Success Metrics"
   },
   "targetConfidenceLevel": {
    "type": "number",
    "description": "Target confidence level, percent; default 95 (decided 29 September, readiness close-out)"
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
    "description": "Product id"
   },
   "event": {
    "type": "string",
    "description": "Event id",
    "nullable": true
   },
   "performance": {
    "type": "string",
    "description": "Performance id",
    "nullable": true
   },
   "channel": {
    "$ref": "#/components/schemas/Channel",
    "description": "Channel"
   },
   "customerSegment": {
    "type": "string",
    "description": "Customer segment",
    "nullable": true
   },
   "startDate": {
    "type": "string",
    "description": "Start Date",
    "format": "date"
   },
   "endDate": {
    "type": "string",
    "description": "End Date",
    "format": "date"
   },
   "minimumPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Minimum Price no variant may go below"
   },
   "maximumPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Maximum Price no variant may exceed"
   },
   "sampleSize": {
    "type": "integer",
    "description": "Sample Size reached"
   },
   "confidenceLevel": {
    "type": "number",
    "description": "Target Confidence Level; default 95 (decided 29 September, readiness close-out), percent"
   },
   "experimentDuration": {
    "type": "integer",
    "description": "Experiment Duration, days"
   },
   "statisticalSignificance": {
    "type": "boolean",
    "description": "Statistical Significance reached at the target confidence level"
   },
   "experimentId": {
    "type": "string",
    "description": "Experiment id"
   },
   "variants": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "label": {
       "type": "string",
       "description": "Variant label (A = control)"
      },
      "price": {
       "$ref": "../shared/common.yaml#/components/schemas/Money",
       "description": "Variant price"
      },
      "trafficSharePercent": {
       "type": "number",
       "description": "Share of traffic, percent; variants sum to 100"
      }
     }
    },
    "description": "Variant Configuration: control plus 1-3 variants (decided 29 September, readiness close-out)"
   },
   "successMetrics": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "revenue",
      "conversion",
      "averageSellingPrice",
      "margin",
      "sellThrough",
      "occupancy",
      "revenuePerVisitor"
     ]
    },
    "description": "Success Metrics"
   },
   "guardrailChecks": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "check": {
       "type": "string",
       "enum": [
        "minimumPrice",
        "maximumPrice",
        "contractRates",
        "membershipRates",
        "regulatoryRequirements"
       ],
       "description": "Guardrail"
      },
      "passed": {
       "type": "boolean",
       "description": "Pass / fail"
      }
     }
    },
    "description": "Guardrails the experiment must respect"
   },
   "variantResults": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "label": {
       "type": "string",
       "description": "Variant"
      },
      "revenueChangePercent": {
       "type": "number",
       "description": "Revenue change vs control, percent"
      },
      "conversionChangePercent": {
       "type": "number",
       "description": "Conversion change vs control, percent"
      },
      "aspChangePercent": {
       "type": "number",
       "description": "ASP change vs control, percent"
      },
      "confidence": {
       "type": "number",
       "description": "Statistical confidence, percent"
      }
     }
    },
    "description": "Results per variant"
   },
   "recommendedWinner": {
    "type": "string",
    "description": "Statistically preferred variant label, advisory",
    "nullable": true
   },
   "experimentStage": {
    "type": "string",
    "description": "Stage: draft, pendingApproval, running, completed or stopped (decided 29 September, readiness close-out)"
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
    "type": "number",
    "description": "Mean forecast error (actual vs forecast demand), percent"
   },
   "demandForecastAccuracy": {
    "type": "number",
    "description": "Demand Forecast Accuracy, percent"
   },
   "revenueForecastAccuracy": {
    "type": "number",
    "description": "Revenue Forecast Accuracy, percent"
   },
   "elasticityAccuracy": {
    "type": "number",
    "description": "Elasticity Accuracy, percent"
   },
   "recommendationSuccess": {
    "type": "number",
    "description": "Recommendation Success, percent"
   },
   "confidenceCalibration": {
    "type": "number",
    "description": "Confidence Calibration: how closely stated confidence matched realised accuracy, percent"
   },
   "falsePositiveRate": {
    "type": "number",
    "description": "False Positive Rate, percent"
   },
   "revenueUplift": {
    "type": "number",
    "description": "Revenue Uplift, percent"
   },
   "venue": {
    "type": "string",
    "description": "Venue",
    "nullable": true
   },
   "product": {
    "type": "string",
    "description": "Product",
    "nullable": true
   },
   "eventType": {
    "type": "string",
    "description": "Event type",
    "nullable": true
   },
   "season": {
    "type": "string",
    "description": "Season",
    "nullable": true
   },
   "channel": {
    "$ref": "#/components/schemas/Channel",
    "description": "Channel"
   },
   "market": {
    "type": "string",
    "description": "Market",
    "nullable": true
   },
   "forecastHorizon": {
    "type": "string",
    "description": "Forecast Horizon",
    "enum": [
     "intraday",
     "tomorrow",
     "days7",
     "days30",
     "eventHorizon",
     "seasonalHorizon"
    ]
   },
   "modelName": {
    "type": "string",
    "description": "Model name"
   },
   "modelVersion": {
    "type": "string",
    "description": "Model version"
   },
   "lifecycleStage": {
    "type": "string",
    "description": "Model lifecycle: candidate, validation, approved, production, monitored or retired"
   },
   "accuracyChange30d": {
    "type": "number",
    "description": "Model Drift: accuracy change over the last 30 days, percent"
   },
   "signalEffectiveness": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "signal": {
       "type": "string",
       "enum": [
        "internalSales",
        "bookingVelocity",
        "occupancy",
        "historicalEvents",
        "nearbyEvent",
        "weather",
        "marketTourism",
        "competitor",
        "priceElasticity",
        "other"
       ],
       "description": "Signal"
      },
      "forecastContribution": {
       "type": "string",
       "enum": [
        "low",
        "medium",
        "high"
       ],
       "description": "Forecast contribution"
      },
      "reliability": {
       "type": "number",
       "description": "Reliability, percent"
      }
     }
    },
    "description": "Signal Effectiveness"
   },
   "humanOverrideRate": {
    "type": "number",
    "description": "Share of AI recommendations modified by Revenue Managers, percent"
   },
   "overrideOutcomeDelta": {
    "type": "number",
    "description": "Revenue outcome of overridden vs unmodified recommendations, percent"
   },
   "optimizationSuggestions": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "AI Optimization Recommendations; adopting one requires governance. Advisory only: generated narrative never changes a price (decided 29 September, readiness close-out)"
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
    "description": "Recommendation title"
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
    "description": "Change %, percent"
   },
   "revenueOpportunity": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue Opportunity"
   },
   "demandImpact": {
    "type": "number",
    "description": "Demand Impact, percent"
   },
   "confidence": {
    "type": "number",
    "description": "AI Confidence, percent"
   },
   "urgency": {
    "type": "string",
    "description": "Urgency",
    "enum": [
     "low",
     "medium",
     "high",
     "critical"
    ]
   },
   "governanceLevel": {
    "type": "string",
    "description": "Governance Level: approval level required, from the configured approval matrix"
   },
   "simulationRevenueUplift": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Simulation Revenue Uplift (Board 7)"
   },
   "recommendationId": {
    "type": "string",
    "description": "Recommendation id"
   },
   "drivers": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "signal": {
       "type": "string",
       "enum": [
        "internalSales",
        "bookingVelocity",
        "occupancy",
        "historicalEvents",
        "nearbyEvent",
        "weather",
        "marketTourism",
        "competitor",
        "priceElasticity",
        "other"
       ],
       "description": "Signal category behind the driver"
      },
      "direction": {
       "type": "string",
       "enum": [
        "up",
        "down"
       ],
       "description": "Whether the driver pushes the price up or down"
      },
      "explanation": {
       "type": "string",
       "description": "Business-language evidence, e.g. booking velocity 31% above forecast"
      }
     }
    },
    "description": "Primary drivers of the recommendation (pack's up/down driver list); explanatory, not literal model weights"
   },
   "guardrailsPassed": {
    "type": "boolean",
    "description": "Guardrails passed"
   },
   "decision": {
    "type": "string",
    "description": "Decision: pending, accepted, rejected, modified, scheduled or sentForApproval; every item starts pending"
   },
   "rejectionReason": {
    "type": "string",
    "description": "Rejection Reason",
    "enum": [
     "commercialJudgment",
     "brandPositioning",
     "customerSensitivity",
     "eventStrategy",
     "incorrectSignal",
     "dataConcern",
     "other"
    ],
    "nullable": true
   },
   "rejectionNote": {
    "type": "string",
    "description": "Free-text note, required when reason is other",
    "nullable": true
   },
   "humanSelectedPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price the Revenue Manager chose when modifying"
   },
   "scheduledFor": {
    "type": "string",
    "description": "When a scheduled change should execute",
    "format": "date-time",
    "nullable": true
   },
   "decidedBy": {
    "type": "string",
    "description": "User who decided",
    "nullable": true
   },
   "decidedAt": {
    "type": "string",
    "description": "When decided",
    "format": "date-time",
    "nullable": true
   },
   "actualRevenueResultPercent": {
    "type": "number",
    "description": "Feedback Loop: actual revenue result after execution; empty until measured, percent"
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
    "description": "Venue",
    "nullable": true
   },
   "product": {
    "type": "string",
    "description": "Product",
    "nullable": true
   },
   "event": {
    "type": "string",
    "description": "Event",
    "nullable": true
   },
   "strategy": {
    "type": "string",
    "description": "Dynamic pricing strategy (Board 5)"
   },
   "channel": {
    "$ref": "#/components/schemas/Channel",
    "description": "Channel"
   },
   "market": {
    "type": "string",
    "description": "Market",
    "nullable": true
   },
   "effectiveFrom": {
    "type": "string",
    "description": "Effective from",
    "format": "date-time"
   },
   "evaluationFrequency": {
    "type": "integer",
    "description": "Evaluation Frequency, minutes; default 60 (decided 29 September, readiness close-out)"
   },
   "executionFrequency": {
    "type": "integer",
    "description": "Execution Frequency, minutes; default 240 (decided 29 September, readiness close-out)"
   },
   "minimumTimeBetweenChanges": {
    "type": "integer",
    "description": "Minimum Time Between Changes, minutes; default 240 (decided 29 September, readiness close-out)"
   },
   "maximumChangesPerDay": {
    "type": "integer",
    "description": "Maximum Changes per Day; default 3 (decided 29 September, readiness close-out)"
   },
   "requireGuardrailsPassed": {
    "type": "boolean",
    "description": "Auto-execute only if guardrails passed; always true, cannot be switched off"
   },
   "excludeProtectedRates": {
    "type": "boolean",
    "description": "Auto-execute only if no protected (contract/member) rate is affected; default true (decided 29 September, readiness close-out)"
   },
   "requireHealthyForecastData": {
    "type": "boolean",
    "description": "Auto-execute only if forecast data is healthy; default true (decided 29 September, readiness close-out)"
   },
   "policyId": {
    "type": "string",
    "description": "Policy id"
   },
   "effectiveTo": {
    "type": "string",
    "description": "Effective to",
    "format": "date-time",
    "nullable": true
   },
   "automationLevel": {
    "type": "string",
    "description": "Automation Level; default advisory (decided 29 September, readiness close-out)",
    "enum": [
     "advisory",
     "humanInTheLoop",
     "conditionalAutonomous",
     "autonomous"
    ]
   },
   "maxAdjustmentPercent": {
    "type": "number",
    "description": "Auto-execute only if adjustment is at or below this, percent; default 5 (decided 29 September, readiness close-out)"
   },
   "minAiConfidence": {
    "type": "number",
    "description": "Auto-execute only if AI confidence is at or above this, percent; default 90 (decided 29 September, readiness close-out)"
   },
   "minRevenueUpliftPercent": {
    "type": "number",
    "description": "Auto-execute only if expected uplift is at or above this, percent; default 2 (decided 29 September, readiness close-out)"
   },
   "quietPeriodMinutes": {
    "type": "integer",
    "description": "Quiet Period: no automated change within this many minutes of event start; default 60 (decided 29 September, readiness close-out)"
   },
   "circuitBreakers": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "trigger": {
       "type": "string",
       "enum": [
        "dataQualityFalls",
        "modelConfidenceDrops",
        "conversionDropsAbnormally",
        "priceVolatilityExceedsThreshold",
        "revenueFalls",
        "integrationFails"
       ],
       "description": "Circuit breaker"
      },
      "threshold": {
       "type": "number",
       "description": "Trigger threshold, in the trigger's unit"
      },
      "enabled": {
       "type": "boolean",
       "description": "Enabled; all enabled by default"
      },
      "tripped": {
       "type": "boolean",
       "description": "Currently tripped"
      }
     }
    },
    "description": "Circuit Breakers (decided 29 September, readiness close-out)"
   },
   "paused": {
    "type": "boolean",
    "description": "Paused by PAUSE ALL AUTONOMOUS PRICING or a tripped breaker"
   }
  }
 },
 "Channel": {
  "type": "string",
  "enum": [
   "pos",
   "kiosk",
   "web",
   "mobile",
   "b2b",
   "ota",
   "callCentre"
  ]
 },
 "DynamicPricingControl": {
  "type": "object",
  "x-ticvai-persistence": "catalogue.dynamic_pricing_control",
  "description": "**The limits and the autonomy of dynamic pricing at one scope** (29 September, data model DM3). Merges guardrails (ADM-093) and automation policy (ADM-094, ADM-113): both are per-scope controls a price change must pass, and they share the rate-of-change limits. The most specific scope wins; guardrails are re-checked at execution (`createLiveDynamicPrice`). `automationLevel` is the one vocabulary: the strategy screen's `monitor`/`recommend` read as `advisory`, `prepareChange` as `humanInTheLoop`, `autoExecuteWithinGuardrails` as `conditionalAutonomous`.",
  "required": [
   "id",
   "scopePath",
   "scopeLevel",
   "automationLevel"
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
   "scopeLevel": {
    "type": "string",
    "enum": [
     "global",
     "market",
     "venue",
     "strategy",
     "product",
     "event",
     "performance",
     "channel"
    ]
   },
   "scopeId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Null at `global`."
   },
   "absoluteMinimumPrice": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true
   },
   "absoluteMaximumPrice": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true
   },
   "minimumMarginPercent": {
    "type": "number",
    "nullable": true
   },
   "maximumUpliftPercent": {
    "type": "number",
    "nullable": true,
    "minimum": 0
   },
   "maximumReductionPercent": {
    "type": "number",
    "nullable": true,
    "minimum": 0
   },
   "maximumSingleChangePercent": {
    "type": "number",
    "nullable": true,
    "minimum": 0
   },
   "maximumDailyChangePercent": {
    "type": "number",
    "nullable": true,
    "minimum": 0
   },
   "maximumWeeklyChangePercent": {
    "type": "number",
    "nullable": true,
    "minimum": 0
   },
   "minimumChangeIntervalMinutes": {
    "type": "integer",
    "nullable": true,
    "minimum": 0
   },
   "maximumChangesPerDay": {
    "type": "integer",
    "nullable": true,
    "minimum": 0
   },
   "minimumInventory": {
    "type": "integer",
    "nullable": true,
    "minimum": 0
   },
   "maximumOccupancyTriggerPercent": {
    "type": "number",
    "nullable": true,
    "minimum": 0,
    "maximum": 100
   },
   "protectedRateTypes": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "contractRates",
      "membershipRates",
      "corporateRates",
      "promotionalLockedRates",
      "regulatoryPrices",
      "complimentaryRates"
     ]
    }
   },
   "isFrozen": {
    "type": "boolean",
    "default": false
   },
   "isKillSwitchActive": {
    "type": "boolean",
    "default": false,
    "description": "Stops every automatic change in scope at once."
   },
   "automationLevel": {
    "type": "string",
    "enum": [
     "advisory",
     "humanInTheLoop",
     "conditionalAutonomous",
     "autonomous"
    ],
    "default": "advisory"
   },
   "authorityTiers": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true,
    "description": "`[{maxAdjustmentPercent, action, confidenceThreshold}]`."
   },
   "maxAdjustmentPercent": {
    "type": "number",
    "nullable": true,
    "minimum": 0
   },
   "minAiConfidence": {
    "type": "number",
    "nullable": true,
    "minimum": 0,
    "maximum": 1
   },
   "minRevenueUpliftPercent": {
    "type": "number",
    "nullable": true
   },
   "evaluationFrequencyMinutes": {
    "type": "integer",
    "nullable": true,
    "minimum": 1
   },
   "executionFrequencyMinutes": {
    "type": "integer",
    "nullable": true,
    "minimum": 1
   },
   "quietPeriodMinutes": {
    "type": "integer",
    "nullable": true,
    "minimum": 0
   },
   "noChangeWindows": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true,
    "description": "`[{anchor, minutesBefore, minutesAfter, clockFrom, clockTo}]`."
   },
   "circuitBreakers": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true,
    "description": "`[{trigger, threshold, enabled, tripped}]`."
   },
   "requireGuardrailsPassed": {
    "type": "boolean",
    "default": true
   },
   "excludeProtectedRates": {
    "type": "boolean",
    "default": true
   },
   "requireHealthyForecastData": {
    "type": "boolean",
    "default": true
   },
   "safeFailureBehavior": {
    "type": "string",
    "enum": [
     "holdLastPrice",
     "returnToBase",
     "freeze",
     "requestReview"
    ],
    "default": "holdLastPrice"
   },
   "activeOverride": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true,
    "description": "`{user, reason, overridePrice, start, expiry, returnBehavior}`."
   },
   "isPaused": {
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
    "description": "Revenue Uplift, percent"
   },
   "marginUplift": {
    "type": "number",
    "description": "Margin Uplift, percent"
   },
   "averageSellingPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Average Selling Price"
   },
   "conversion": {
    "type": "number",
    "description": "Conversion, percent"
   },
   "attendance": {
    "type": "integer",
    "description": "Attendance"
   },
   "occupancy": {
    "type": "number",
    "description": "Occupancy, percent"
   },
   "sellThrough": {
    "type": "number",
    "description": "Sell-Through, percent"
   },
   "revenuePerAvailableCapacity": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue per Available Capacity"
   },
   "numberOfPriceChanges": {
    "type": "integer",
    "description": "Number of Price Changes"
   },
   "strategyRoi": {
    "type": "number",
    "description": "Strategy ROI, percent"
   },
   "recommendationsGenerated": {
    "type": "integer",
    "description": "Recommendations Generated"
   },
   "accepted": {
    "type": "integer",
    "description": "Accepted"
   },
   "rejected": {
    "type": "integer",
    "description": "Rejected"
   },
   "modified": {
    "type": "integer",
    "description": "Modified"
   },
   "autoExecuted": {
    "type": "integer",
    "description": "Auto-Executed"
   },
   "successful": {
    "type": "integer",
    "description": "Successful"
   },
   "negativeOutcome": {
    "type": "integer",
    "description": "Negative Outcome"
   },
   "level": {
    "type": "string",
    "description": "Drilldown level of this row",
    "enum": [
     "market",
     "venue",
     "event",
     "performance",
     "product",
     "priceCategory",
     "channel"
    ]
   },
   "key": {
    "type": "string",
    "description": "Id of the market/venue/event/... at that level"
   },
   "label": {
    "type": "string",
    "description": "Display name"
   },
   "comparisonGroup": {
    "type": "string",
    "description": "Side of the comparison this row is, e.g. dynamic / fixed, AI / rules",
    "nullable": true
   },
   "opportunityLost": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Opportunity Lost: estimated revenue not captured through rejected recommendations (analytical estimate)"
   },
   "priceTimeline": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "at": {
       "type": "string",
       "format": "date-time",
       "description": "Moment of the price movement"
      },
      "price": {
       "$ref": "../shared/common.yaml#/components/schemas/Money",
       "description": "Price"
      },
      "demand": {
       "type": "integer",
       "description": "Demand"
      },
      "occupancy": {
       "type": "number",
       "description": "Occupancy, percent"
      },
      "conversion": {
       "type": "number",
       "description": "Conversion, percent"
      },
      "bookingVelocity": {
       "type": "number",
       "description": "Booking velocity vs forecast, percent"
      },
      "revenue": {
       "$ref": "../shared/common.yaml#/components/schemas/Money",
       "description": "Revenue"
      }
     }
    },
    "description": "Price Timeline overlay"
   }
  }
 },
 "LiveDynamicPriceExecutionDeploymentMonitorInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Live Dynamic Price Execution & Deployment Monitor submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "product": {
    "type": "string",
    "description": "Product id"
   },
   "event": {
    "type": "string",
    "description": "Event id",
    "nullable": true
   },
   "newPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "New Price"
   },
   "strategy": {
    "type": "string",
    "description": "Strategy id",
    "nullable": true
   },
   "aiRecommendation": {
    "type": "string",
    "description": "Recommendation id",
    "nullable": true
   },
   "approval": {
    "type": "string",
    "description": "Approval reference; required unless the automation policy permits automatic execution",
    "nullable": true
   },
   "executionSource": {
    "type": "string",
    "description": "Execution Source",
    "enum": [
     "manual",
     "humanApproved",
     "scheduled",
     "conditionalAutonomous",
     "autonomous"
    ]
   },
   "performance": {
    "type": "string",
    "description": "Performance id",
    "nullable": true
   },
   "trigger": {
    "type": "string",
    "description": "Trigger",
    "nullable": true
   },
   "channels": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "b2c",
      "mobileApp",
      "pos",
      "kiosk",
      "callCenter",
      "b2b",
      "reseller",
      "ota",
      "api"
     ]
    },
    "description": "Channels to deploy to; default all channels the product is sold on (decided 29 September, readiness close-out)"
   },
   "scheduledFor": {
    "type": "string",
    "description": "Execute at; empty = now",
    "format": "date-time",
    "nullable": true
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
    "description": "Timestamp",
    "format": "date-time"
   },
   "product": {
    "type": "string",
    "description": "Product id"
   },
   "event": {
    "type": "string",
    "description": "Event id",
    "nullable": true
   },
   "previousPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Previous Price"
   },
   "newPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "New Price"
   },
   "strategy": {
    "type": "string",
    "description": "Strategy id",
    "nullable": true
   },
   "aiRecommendation": {
    "type": "string",
    "description": "Recommendation id the change came from",
    "nullable": true
   },
   "approval": {
    "type": "string",
    "description": "Approval reference; empty only for policy-permitted automatic execution",
    "nullable": true
   },
   "executionSource": {
    "type": "string",
    "description": "Execution Source",
    "enum": [
     "manual",
     "humanApproved",
     "scheduled",
     "conditionalAutonomous",
     "autonomous"
    ]
   },
   "status": {
    "type": "string",
    "description": "Status: queued, processing, live, partial, failed or rolledBack"
   },
   "executionId": {
    "type": "string",
    "description": "Execution id"
   },
   "trigger": {
    "type": "string",
    "description": "Trigger, e.g. booking velocity + occupancy",
    "nullable": true
   },
   "aiConfidence": {
    "type": "number",
    "description": "AI confidence at execution, percent"
   },
   "channelDeployments": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "channel": {
       "type": "string",
       "enum": [
        "b2c",
        "mobileApp",
        "pos",
        "kiosk",
        "callCenter",
        "b2b",
        "reseller",
        "ota",
        "api"
       ],
       "description": "Channel"
      },
      "price": {
       "$ref": "../shared/common.yaml#/components/schemas/Money",
       "description": "Price live on the channel"
      },
      "consistent": {
       "type": "boolean",
       "description": "Channel shows the new price"
      },
      "deploymentStatus": {
       "type": "string",
       "description": "queued, processing, live, failed or rolledBack"
      }
     }
    },
    "description": "Channel Deployment"
   },
   "priceInconsistency": {
    "type": "boolean",
    "description": "Price inconsistency detected across channels"
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
 "PricingRecommendationDecision": {
  "type": "object",
  "x-ticvai-persistence": "catalogue.pricing_recommendation_decision",
  "description": "**One human decision on one AI pricing recommendation** (decided 29 September, readiness close-out). New table: the queue row `AiRecommendationReviewDecisionQueueView` reads its decision fields from here. Written once by `decidePricingRecommendation` and never edited; a changed mind is a new recommendation.\n",
  "required": [
   "id",
   "recommendationId",
   "decision",
   "decidedByPrincipalId",
   "decidedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "recommendationId": {
    "type": "string",
    "format": "uuid",
    "description": "A `catalogue.pricing_recommendation` (29 September, data model DM3)."
   },
   "decision": {
    "type": "string",
    "enum": [
     "accept",
     "modify",
     "reject",
     "schedule",
     "sendForApproval"
    ]
   },
   "rejectionReason": {
    "type": "string",
    "nullable": true,
    "enum": [
     "commercialJudgment",
     "brandPositioning",
     "customerSensitivity",
     "eventStrategy",
     "incorrectSignal",
     "dataConcern",
     "other",
     null
    ]
   },
   "rejectionNote": {
    "type": "string",
    "nullable": true
   },
   "recommendedPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "humanSelectedPrice": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true
   },
   "scheduledFor": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "approvalRequestId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The approvals request opened by `sendForApproval`."
   },
   "executionId": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "The `createLiveDynamicPrice` execution that carried it out, once it has."
   },
   "decidedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "decidedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true
   }
  }
 },
 "PricingRecommendationDecisionInput": {
  "type": "object",
  "x-ticvai-persistence": "none — request only",
  "description": "What `decidePricingRecommendation` takes (decided 29 September, readiness close-out).",
  "required": [
   "decision"
  ],
  "properties": {
   "decision": {
    "type": "string",
    "enum": [
     "accept",
     "modify",
     "reject",
     "schedule",
     "sendForApproval"
    ]
   },
   "rejectionReason": {
    "type": "string",
    "enum": [
     "commercialJudgment",
     "brandPositioning",
     "customerSensitivity",
     "eventStrategy",
     "incorrectSignal",
     "dataConcern",
     "other"
    ],
    "description": "Required for reject."
   },
   "rejectionNote": {
    "type": "string",
    "maxLength": 2000
   },
   "humanSelectedPrice": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Required for modify; must sit inside the strategy's guardrails."
   },
   "scheduledFor": {
    "type": "string",
    "format": "date-time",
    "description": "Required for schedule; in the future."
   }
  }
 },
 "PricingSimulationStudioInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Pricing Simulation Studio submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "venue": {
    "type": "string",
    "description": "Scope: venue id",
    "nullable": true
   },
   "product": {
    "type": "string",
    "description": "Scope: product id",
    "nullable": true
   },
   "event": {
    "type": "string",
    "description": "Scope: event id",
    "nullable": true
   },
   "performance": {
    "type": "string",
    "description": "Scope: performance id",
    "nullable": true
   },
   "timeslot": {
    "type": "string",
    "description": "Scope: timeslot",
    "nullable": true
   },
   "priceCategory": {
    "type": "string",
    "description": "Scope: price category",
    "nullable": true
   },
   "channel": {
    "$ref": "#/components/schemas/Channel",
    "description": "Scope: channel"
   },
   "customerSegment": {
    "type": "string",
    "description": "Scope: customer segment",
    "nullable": true
   },
   "dateFrom": {
    "type": "string",
    "description": "Scope: first date",
    "format": "date"
   },
   "dateTo": {
    "type": "string",
    "description": "Scope: last date",
    "format": "date"
   },
   "simulationSource": {
    "type": "string",
    "description": "Simulation Source",
    "enum": [
     "manualPriceChange",
     "dynamicRule",
     "aiRecommendation",
     "newDynamicStrategy",
     "strategyModification",
     "bulkPriceChange"
    ]
   },
   "sourceReference": {
    "type": "string",
    "description": "Id of the rule, recommendation or strategy the simulation came from",
    "nullable": true
   },
   "proposedPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Proposed price (single-price change)"
   },
   "proposedAdjustmentPercent": {
    "type": "number",
    "description": "Proposed adjustment, percent (bulk change or strategy)",
    "nullable": true
   }
  }
 },
 "PricingSimulationStudioView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Pricing Simulation Studio displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "expectedDemand": {
    "type": "integer",
    "description": "Expected Demand"
   },
   "expectedConversion": {
    "type": "number",
    "description": "Expected Conversion, percent"
   },
   "expectedAttendance": {
    "type": "integer",
    "description": "Expected Attendance"
   },
   "expectedOccupancy": {
    "type": "number",
    "description": "Expected Occupancy, percent"
   },
   "expectedRevenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Expected Revenue"
   },
   "expectedMargin": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Expected Margin"
   },
   "expectedSellThrough": {
    "type": "number",
    "description": "Expected Sell-Through, percent"
   },
   "expectedSellOutTime": {
    "type": "string",
    "description": "Expected Sell-Out Time",
    "format": "date-time",
    "nullable": true
   },
   "averageSellingPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Average Selling Price"
   },
   "simulationConfidence": {
    "type": "number",
    "description": "Simulation Confidence, percent"
   },
   "dataVolume": {
    "type": "integer",
    "description": "Data Volume: transactions behind the simulation"
   },
   "historicalSimilarity": {
    "type": "number",
    "description": "Historical Similarity, percent"
   },
   "forecastConfidence": {
    "type": "number",
    "description": "Forecast Confidence, percent"
   },
   "elasticityConfidence": {
    "type": "number",
    "description": "Elasticity Confidence, percent"
   },
   "externalSignalQuality": {
    "type": "number",
    "description": "External Signal Quality, percent"
   },
   "simulationId": {
    "type": "string",
    "description": "Simulation id (saved scenarios keep it)"
   },
   "simulationSource": {
    "type": "string",
    "description": "Simulation Source",
    "enum": [
     "manualPriceChange",
     "dynamicRule",
     "aiRecommendation",
     "newDynamicStrategy",
     "strategyModification",
     "bulkPriceChange"
    ]
   },
   "currentPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Current price"
   },
   "proposedPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Proposed price"
   },
   "baselineRevenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Current strategy: expected revenue"
   },
   "baselineDemand": {
    "type": "integer",
    "description": "Current strategy: expected demand"
   },
   "baselineOccupancy": {
    "type": "number",
    "description": "Current strategy: expected occupancy, percent"
   },
   "guardrailChecks": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "check": {
       "type": "string",
       "enum": [
        "commercialGuardrail",
        "contractProtection",
        "priceLadder",
        "approvalThreshold"
       ],
       "description": "Guardrail"
      },
      "passed": {
       "type": "boolean",
       "description": "Pass / fail"
      },
      "message": {
       "type": "string",
       "description": "Why it failed, or the approval level required"
      }
     }
    },
    "description": "Guardrail Check shown before the simulation completes"
   }
  }
 },
 "RevenueDemandImpactForecastingView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Revenue & Demand Impact Forecasting displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "revenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Proposed: expected revenue"
   },
   "demand": {
    "type": "integer",
    "description": "Proposed: expected demand"
   },
   "attendance": {
    "type": "integer",
    "description": "Proposed: attendance"
   },
   "occupancy": {
    "type": "number",
    "description": "Proposed: occupancy, percent"
   },
   "conversion": {
    "type": "number",
    "description": "Proposed: conversion, percent"
   },
   "margin": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Proposed: margin"
   },
   "asp": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Proposed: average selling price"
   },
   "sellThrough": {
    "type": "number",
    "description": "Proposed: sell-through, percent"
   },
   "sellOutProbability": {
    "type": "number",
    "description": "Proposed: sell-out probability, percent"
   },
   "assessmentId": {
    "type": "string",
    "description": "Assessment id"
   },
   "recommendationId": {
    "type": "string",
    "description": "Recommendation assessed",
    "nullable": true
   },
   "simulationId": {
    "type": "string",
    "description": "Simulation assessed",
    "nullable": true
   },
   "baselineRevenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Without change: expected revenue"
   },
   "baselineDemand": {
    "type": "integer",
    "description": "Without change: expected demand"
   },
   "baselineOccupancy": {
    "type": "number",
    "description": "Without change: expected occupancy, percent"
   },
   "revenueChange": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Impact: revenue"
   },
   "revenueChangePercent": {
    "type": "number",
    "description": "Impact: revenue, percent"
   },
   "demandChange": {
    "type": "integer",
    "description": "Impact: demand"
   },
   "demandChangePercent": {
    "type": "number",
    "description": "Impact: demand, percent"
   },
   "marginChange": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Impact: margin"
   },
   "customerImpacts": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "group": {
       "type": "string",
       "enum": [
        "member",
        "resident",
        "tourist",
        "family",
        "b2b"
       ],
       "description": "Customer group"
      },
      "demandChangePercent": {
       "type": "number",
       "description": "Estimated demand change, percent"
      },
      "note": {
       "type": "string",
       "description": "Explanation"
      }
     }
    },
    "description": "Customer Impact, where supported"
   },
   "cannibalization": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "toProduct": {
       "type": "string",
       "description": "Product demand shifts toward"
      },
      "demandShiftPercent": {
       "type": "number",
       "description": "Share of demand shifting, percent"
      }
     }
    },
    "description": "Cannibalization"
   },
   "bestCaseRevenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Sensitivity: best case revenue"
   },
   "worstCaseRevenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Sensitivity: worst case revenue"
   }
  }
 },
 "RevenueOptimizationCommandCenterSummary": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection; the headline tiles over the list, computed at read time for the filters in force",
  "description": "**The headline figures on Revenue Optimization Command Center.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.",
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
    "type": "integer",
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
    "type": "integer",
    "description": "Approval Required: changes waiting for an approver"
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
    "type": "number",
    "description": "Forecast Accuracy over the last 30 days (decided 29 September, readiness close-out), percent"
   },
   "optimizationSuccessRate": {
    "type": "number",
    "description": "Optimization Success Rate: executed changes with a positive measured outcome, percent"
   },
   "aiRevenueBrief": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "AI Revenue Brief, e.g. AED 284,000 of opportunity in the next seven days. Advisory only: generated narrative never changes a price (decided 29 September, readiness close-out)"
   }
  }
 },
 "RevenueOptimizationCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Revenue Optimization Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
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
    "description": "Performance",
    "nullable": true
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
    "description": "Expected Uplift, percent"
   },
   "confidence": {
    "type": "number",
    "description": "Confidence, percent"
   },
   "automationMode": {
    "type": "string",
    "description": "Automation Mode in force for this scope",
    "enum": [
     "advisory",
     "humanInTheLoop",
     "conditionalAutonomous",
     "autonomous"
    ]
   },
   "approvalStatus": {
    "type": "string",
    "description": "Approval Status: notRequired, pending, approved or rejected"
   },
   "executionStatus": {
    "type": "string",
    "description": "Execution Status: notStarted, queued, processing, live, partial, failed or rolledBack"
   },
   "revenueRisk": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue Risk if no action is taken"
   },
   "eventProximity": {
    "type": "integer",
    "description": "Event Proximity: days until the event"
   },
   "inventoryPosition": {
    "type": "number",
    "description": "Inventory Position: remaining inventory, percent"
   },
   "demandVariance": {
    "type": "number",
    "description": "Demand Variance against forecast, percent"
   },
   "urgency": {
    "type": "string",
    "description": "Urgency",
    "enum": [
     "low",
     "medium",
     "high",
     "critical"
    ]
   },
   "optimizationId": {
    "type": "string",
    "description": "Optimisation id"
   },
   "recommendationId": {
    "type": "string",
    "description": "Recommendation id",
    "nullable": true
   },
   "revenueOpportunity": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue Opportunity"
   },
   "priorityRank": {
    "type": "integer",
    "description": "Priority rank (1 = act first)"
   },
   "nextAction": {
    "type": "string",
    "description": "Suggested next action (the pack's Action column)",
    "enum": [
     "review",
     "simulate",
     "approve"
    ]
   }
  }
 },
 "ScenarioModelingWhatIfAnalysisView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Scenario Modeling & What-If Analysis displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "demand": {
    "type": "number",
    "description": "Demand adjustment (+/-), percent"
   },
   "occupancy": {
    "type": "number",
    "description": "Occupancy, percent"
   },
   "inventory": {
    "type": "integer",
    "description": "Inventory available"
   },
   "bookingVelocity": {
    "type": "number",
    "description": "Booking velocity adjustment, percent"
   },
   "weatherImpact": {
    "type": "number",
    "description": "Weather impact on demand, percent"
   },
   "nearbyEventImpact": {
    "type": "number",
    "description": "Nearby event impact on demand, percent"
   },
   "competitorPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Competitor price"
   },
   "conversion": {
    "type": "number",
    "description": "Conversion, percent"
   },
   "price": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price"
   },
   "eventProximity": {
    "type": "integer",
    "description": "Event proximity, days"
   },
   "remainingCapacity": {
    "type": "number",
    "description": "Remaining Capacity, percent"
   },
   "scenarioId": {
    "type": "string",
    "description": "Scenario id"
   },
   "name": {
    "type": "string",
    "description": "Scenario name"
   },
   "scenarioTypes": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "lowDemand",
      "expectedDemand",
      "highDemand",
      "sellOut",
      "competitorPriceDrop",
      "competitorPriceIncrease",
      "extremeWeather",
      "rain",
      "nearbyExhibition",
      "majorConcert",
      "tourismSurge",
      "cancellationSurge",
      "inventoryReduction",
      "customScenario"
     ]
    },
    "description": "Scenario Library entries combined"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "event": {
    "type": "string",
    "description": "Event",
    "nullable": true
   },
   "strategyResults": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "strategy": {
       "type": "string",
       "enum": [
        "fixedPrice",
        "ruleBased",
        "aiRecommendation",
        "custom"
       ],
       "description": "Strategy compared"
      },
      "averagePrice": {
       "$ref": "../shared/common.yaml#/components/schemas/Money",
       "description": "Avg. price"
      },
      "demand": {
       "type": "integer",
       "description": "Demand"
      },
      "revenue": {
       "$ref": "../shared/common.yaml#/components/schemas/Money",
       "description": "Revenue"
      },
      "occupancy": {
       "type": "number",
       "description": "Occupancy, percent"
      },
      "margin": {
       "$ref": "../shared/common.yaml#/components/schemas/Money",
       "description": "Margin"
      }
     }
    },
    "description": "Results per strategy"
   },
   "reviewStage": {
    "type": "string",
    "description": "Review stage: draft, submittedForReview or reviewed (decided 29 September, readiness close-out)"
   },
   "createdBy": {
    "type": "string",
    "description": "Author user id"
   },
   "updatedAt": {
    "type": "string",
    "description": "Last saved",
    "format": "date-time"
   }
  }
 },
 "SignalRegistryEntry": {
  "type": "object",
  "x-ticvai-persistence": "catalogue.signal_registry",
  "description": "**The registry of AI signals and models, with their trust and quality** (29 September, data model DM3). ADM-106 and ADM-118. A signal or model not `approved` for a use in `aiUsePermissions` is not used for it.",
  "required": [
   "id",
   "scopePath",
   "registryKind",
   "name",
   "trustLevel"
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
   "registryKind": {
    "type": "string",
    "enum": [
     "signal",
     "model"
    ]
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "category": {
    "type": "string",
    "enum": [
     "internalSales",
     "inventory",
     "weather",
     "nearbyEvents",
     "competitor",
     "tourism",
     "calendar",
     "transport",
     "market",
     "other",
     null
    ],
    "nullable": true
   },
   "provider": {
    "type": "string",
    "maxLength": 100,
    "nullable": true
   },
   "source": {
    "type": "string",
    "maxLength": 100,
    "nullable": true
   },
   "internalExternal": {
    "type": "string",
    "enum": [
     "internal",
     "external",
     null
    ],
    "nullable": true
   },
   "marketCode": {
    "type": "string",
    "maxLength": 40,
    "nullable": true
   },
   "refreshFrequency": {
    "type": "string",
    "enum": [
     "realTime",
     "minutes10",
     "hourly",
     "daily",
     "weekly",
     "manual",
     null
    ],
    "nullable": true
   },
   "trustLevel": {
    "type": "string",
    "enum": [
     "approved",
     "experimental",
     "advisoryOnly",
     "blocked"
    ],
    "default": "experimental"
   },
   "aiUsePermissions": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "forecasting",
      "recommendations",
      "simulation",
      "automatedPricing"
     ]
    }
   },
   "fallbackPolicy": {
    "type": "string",
    "enum": [
     "useHistoricalValue",
     "ignore",
     "substitute",
     "reduceConfidence",
     "stopAiRecommendation",
     null
    ],
    "nullable": true
   },
   "status": {
    "type": "string",
    "maxLength": 40,
    "nullable": true
   },
   "ownerPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "version": {
    "type": "string",
    "maxLength": 40,
    "nullable": true,
    "description": "Models."
   },
   "purpose": {
    "type": "string",
    "nullable": true
   },
   "deployedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "trainingWindow": {
    "type": "string",
    "maxLength": 60,
    "nullable": true
   },
   "validationResult": {
    "type": "string",
    "nullable": true
   },
   "lastUpdateAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "qualityCounts": {
    "type": "object",
    "additionalProperties": true,
    "readOnly": true,
    "description": "Signals: `{missingData, delayedData, outliers, invalidValues, unexpectedChanges, sourceFailure, duplicateData}`."
   },
   "performance": {
    "type": "object",
    "additionalProperties": true,
    "readOnly": true,
    "description": "Models: `{forecastAccuracy, bias, recommendationAccuracy, revenuePerformance, drift}` and the per-segment learning metrics."
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
 }
}
```
