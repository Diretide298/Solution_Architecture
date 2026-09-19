# WS38 — Pricing   Revenue Management board 5

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
| `ADM-088` | Dynamic Pricing Strategy Command Center | commandCentre | 1 | 0 | — |
| `ADM-089` | Dynamic Pricing Strategy Builder | configEditor | 1 | 0 | — |
| `ADM-090` | Demand, Occupancy & Availability Rule Builder | listDetail | 1 | 0 | — |
| `ADM-091` | Booking Velocity & Time-to-Event Rule Builder | listDetail | 1 | 0 | — |
| `ADM-092` | Seasonal, Calendar, Day & Timeslot Dynamic Rules | listDetail | 1 | 0 | — |
| `ADM-093` | Channel, Customer Segment & Location Dynamic Rules | listDetail | 1 | 0 | — |
| `ADM-094` | Dynamic Price Bands, Ladders & Adjustment Matrix | configEditor | 1 | 0 | — |
| `ADM-095` | Dynamic Pricing Guardrails & Commercial Protection | configEditor | 1 | 0 | — |
| `ADM-096` | Dynamic Pricing Automation Policy & Control | configEditor | 1 | 0 | — |
| `ADM-097` | Rule Priority, Conflict Resolution & Dynamic Pricing Test Console | listDetail | 1 | 1 | — |

## Thin screens in this batch

**ADM-090, ADM-092, ADM-093 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-088",
  "name": "Dynamic Pricing Strategy Command Center",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "5",
   "number": "10.5.1",
   "page": 75
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/dynamic-pricing-strategy-command-center-adm-088",
   "component": "apps/ticvai-web/src/routes/commercial/DynamicPricingStrategyCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-089",
    "ADM-090",
    "ADM-091",
    "ADM-092",
    "ADM-093",
    "ADM-094",
    "ADM-095",
    "ADM-096",
    "ADM-097"
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
     "to": "ADM-089",
     "trigger": "Works in Dynamic Pricing Strategy Builder",
     "provenance": "flow F147 step 1→2",
     "operation": "listDynamicPricingStrategy"
    },
    {
     "to": "ADM-090",
     "trigger": "Works in Demand, Occupancy & Availability Rule Builder",
     "provenance": "flow F147 step 3→4",
     "operation": "listDynamicPricingStrategy"
    },
    {
     "to": "ADM-091",
     "trigger": "Works in Booking Velocity & Time-to-Event Rule Builder",
     "provenance": "flow F147 step 5→6",
     "operation": "listDynamicPricingStrategy"
    },
    {
     "to": "ADM-092",
     "trigger": "Works in Seasonal, Calendar, Day & Timeslot Dynamic Rules",
     "provenance": "flow F147 step 7→8",
     "operation": "listDynamicPricingStrategy"
    },
    {
     "to": "ADM-093",
     "trigger": "Works in Channel, Customer Segment & Location Dynamic Rules",
     "provenance": "flow F147 step 9→10",
     "operation": "listDynamicPricingStrategy"
    },
    {
     "to": "ADM-094",
     "trigger": "Works in Dynamic Price Bands, Ladders & Adjustment Matrix",
     "provenance": "flow F147 step 11→12",
     "operation": "listDynamicPricingStrategy"
    },
    {
     "to": "ADM-095",
     "trigger": "Works in Dynamic Pricing Guardrails & Commercial Protection",
     "provenance": "flow F147 step 13→14",
     "operation": "listDynamicPricingStrategy"
    },
    {
     "to": "ADM-096",
     "trigger": "Works in Dynamic Pricing Automation Policy & Control",
     "provenance": "flow F147 step 15→16",
     "operation": "listDynamicPricingStrategy"
    },
    {
     "to": "ADM-097",
     "trigger": "Works in Rule Priority, Conflict Resolution & Dynamic Pricing Test Console",
     "provenance": "flow F147 step 17→18",
     "operation": "listDynamicPricingStrategy"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each strategy should show) — counts over a population, then the population",
  "purpose": "Provide the central backend workspace for creating, monitoring, and managing all dynamic- pricing strategies. This should be the primary operational screen for Revenue Managers.",
  "purposeNote": "Authorized users can view and manage the complete dynamic-pricing strategy portfolio from one centralized workspace.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 10 actions on this screen and the screen declares 1 operation.** Unserved: Booking Velocity, Channel, Create Strategy, Duplicate, Open, Test, Compare, Pause …. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 75 §Support"
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
       "label": "Active Strategies",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 75 §Display",
       "bindsTo": "DynamicPricingStrategyCommandCenterView.activeStrategies"
      },
      {
       "kind": "metricTile",
       "label": "Draft Strategies",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 75 §Display",
       "bindsTo": "DynamicPricingStrategyCommandCenterView.draftStrategies"
      },
      {
       "kind": "metricTile",
       "label": "Products Under Dynamic Pricing",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 75 §Display",
       "bindsTo": "DynamicPricingStrategyCommandCenterView.productsUnderDynamicPricing"
      },
      {
       "kind": "metricTile",
       "label": "Events Under Dynamic Pricing",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 75 §Display",
       "bindsTo": "DynamicPricingStrategyCommandCenterView.eventsUnderDynamicPricing"
      },
      {
       "kind": "metricTile",
       "label": "Performances Under Dynamic Pricing",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 75 §Display",
       "bindsTo": "DynamicPricingStrategyCommandCenterView.performancesUnderDynamicPricing"
      },
      {
       "kind": "metricTile",
       "label": "Rules Active",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 75 §Display",
       "bindsTo": "DynamicPricingStrategyCommandCenterView.rulesActive"
      },
      {
       "kind": "metricTile",
       "label": "Current Price Adjustments",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 75 §Display",
       "bindsTo": "DynamicPricingStrategyCommandCenterView.currentPriceAdjustments"
      },
      {
       "kind": "metricTile",
       "label": "Prices at Maximum Guardrail",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 75 §Display",
       "bindsTo": "DynamicPricingStrategyCommandCenterView.pricesAtMaximumGuardrail"
      },
      {
       "kind": "metricTile",
       "label": "Prices at Minimum Guardrail",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 75 §Display",
       "bindsTo": "DynamicPricingStrategyCommandCenterView.pricesAtMinimumGuardrail"
      },
      {
       "kind": "metricTile",
       "label": "Rule Conflicts",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 75 §Display",
       "bindsTo": "DynamicPricingStrategyCommandCenterView.ruleConflicts"
      },
      {
       "kind": "metricTile",
       "label": "Frozen Strategies",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 75 §Display",
       "bindsTo": "DynamicPricingStrategyCommandCenterView.frozenStrategies"
      },
      {
       "kind": "metricTile",
       "label": "Upcoming Activations",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 75 §Display",
       "bindsTo": "DynamicPricingStrategyCommandCenterView.upcomingActivations"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every dynamic pricing strategy",
       "columns": [
        "DynamicPricingStrategyCommandCenterView.strategyId",
        "DynamicPricingStrategyCommandCenterView.strategyName",
        "DynamicPricingStrategyCommandCenterView.strategyType",
        "DynamicPricingStrategyCommandCenterView.productEvent",
        "DynamicPricingStrategyCommandCenterView.venue",
        "DynamicPricingStrategyCommandCenterView.basePriceSource",
        "DynamicPricingStrategyCommandCenterView.currentPrice",
        "DynamicPricingStrategyCommandCenterView.adjustmentRange",
        "DynamicPricingStrategyCommandCenterView.ruleCount",
        "DynamicPricingStrategyCommandCenterView.effectivePeriod",
        "DynamicPricingStrategyCommandCenterView.automationMode",
        "DynamicPricingStrategyCommandCenterView.status",
        "DynamicPricingStrategyCommandCenterView.owner"
       ],
       "bindsTo": "DynamicPricingStrategyCommandCenterView",
       "operation": "listDynamicPricingStrategy",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 75 §Each strategy should show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected dynamic pricing strategy",
       "bindsTo": "DynamicPricingStrategyCommandCenterView",
       "columns": [
        "DynamicPricingStrategyCommandCenterView.strategyId",
        "DynamicPricingStrategyCommandCenterView.strategyName",
        "DynamicPricingStrategyCommandCenterView.strategyType",
        "DynamicPricingStrategyCommandCenterView.productEvent",
        "DynamicPricingStrategyCommandCenterView.venue",
        "DynamicPricingStrategyCommandCenterView.basePriceSource",
        "DynamicPricingStrategyCommandCenterView.currentPrice",
        "DynamicPricingStrategyCommandCenterView.adjustmentRange",
        "DynamicPricingStrategyCommandCenterView.ruleCount",
        "DynamicPricingStrategyCommandCenterView.effectivePeriod",
        "DynamicPricingStrategyCommandCenterView.automationMode",
        "DynamicPricingStrategyCommandCenterView.status",
        "DynamicPricingStrategyCommandCenterView.owner"
       ],
       "notes": null,
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 75 §Each strategy should show"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Booking Velocity",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 75 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Channel",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 75 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Create Strategy",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 75 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Duplicate",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 75 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Open",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 75 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Test",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 75 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Compare",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 75 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Pause",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 75 §Quick Actions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The dynamic pricing strategy list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the dynamic pricing strategy untouched.",
   "emptyFirstRun": "No dynamic pricing strategy yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the dynamic pricing strategy are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listDynamicPricingStrategy",
    "contract": "catalogue",
    "purpose": "Dynamic Pricing Strategy Command Center",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-088"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 75. 25 of 25 labels bound to a contract property; 35 of 55 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-089",
  "name": "Dynamic Pricing Strategy Builder",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "5",
   "number": "10.5.2",
   "page": 76
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/dynamic-pricing-strategy-builder-adm-089",
   "component": "apps/ticvai-web/src/routes/commercial/DynamicPricingStrategyBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-088"
   ],
   "exitTo": [
    "ADM-088"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-088, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-088",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F147 step 2→3",
     "operation": "setDynamicPricingStrategy"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure; Configure whether a strategy) and no display directory — it is settings, not a population",
  "purpose": "Create the master dynamic-pricing strategy and define what commercial objects it controls.",
  "purposeNote": "Administrators can create reusable dynamic-pricing strategies linked to governed commercial base prices and clearly defined product/event scopes.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Strategy Name",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 76 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Strategy Code",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 76 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Description",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 76 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Strategy Type",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 76 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Owner",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 76 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Business Unit",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 76 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Market",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 76 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 76 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Product",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 76 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Event",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 76 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Performance",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 76 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Timeslot",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 76 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Price Category",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 76 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Base Price Source",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 76 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Effective From",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 76 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Effective To",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 76 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Evaluation Frequency",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 76 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Status",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 76 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Operates Independently",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 76 §Configure whether a strategy"
      },
      {
       "kind": "textField",
       "label": "Can Combine with Other Strategies",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 76 §Configure whether a strategy"
      },
      {
       "kind": "selectField",
       "label": "Has Exclusive Control",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 76 §Configure whether a strategy"
      },
      {
       "kind": "selectField",
       "label": "Acts as Fallback",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 76 §Configure whether a strategy"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save changes",
       "provenance": "contract operation setDynamicPricingStrategy"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The dynamic pricing strategy configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the dynamic pricing strategy untouched.",
   "emptyFirstRun": "No dynamic pricing strategy configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setDynamicPricingStrategy",
    "contract": "catalogue",
    "purpose": "Dynamic Pricing Strategy Builder",
    "trigger": "onAction",
    "invalidates": [
     "setDynamicPricingStrategy"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-089"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 76. 0 of 0 labels bound to a contract property; 22 of 45 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-090",
  "name": "Demand, Occupancy & Availability Rule Builder",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "5",
   "number": "10.5.3",
   "page": 78
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/demand-occupancy-availability-rule-builder-adm-090",
   "component": "apps/ticvai-web/src/routes/commercial/DemandOccupancyAvailabilityRuleBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-088"
   ],
   "exitTo": [
    "ADM-088"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-088, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-088",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F147 step 4→5",
     "operation": "setDemandOccupancyAvailability"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure price movements driven by actual demand and capacity consumption. This directly covers the fundamental matrix requirements for: Demand-Based Pricing Occupancy-Based Pricing Availability-Based Pricing Inventory-Based Pricing",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 78"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 78"
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
       "label": "Save changes",
       "provenance": "contract operation setDemandOccupancyAvailability"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setDemandOccupancyAvailability"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The demand occupancy availability list.",
   "error": "Could not load. Names which read failed and leaves the demand occupancy availability untouched.",
   "emptyFirstRun": "No demand occupancy availability yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the demand occupancy availability are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setDemandOccupancyAvailability",
    "contract": "catalogue",
    "purpose": "Demand, Occupancy & Availability Rule Builder",
    "trigger": "onAction",
    "invalidates": [
     "setDemandOccupancyAvailability"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-090"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 78. 0 of 0 labels bound to a contract property; 0 of 15 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-091",
  "name": "Booking Velocity & Time-to-Event Rule Builder",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "5",
   "number": "10.5.4",
   "page": 80
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/booking-velocity-time-to-event-rule-builder-adm-091",
   "component": "apps/ticvai-web/src/routes/commercial/BookingVelocityTimeToEventRuleBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-088"
   ],
   "exitTo": [
    "ADM-088"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-088, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-088",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F147 step 6→7",
     "operation": "setBookingVelocityTime"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Control price movement based on how quickly inventory is selling and how much time remains before the event or visit date. This is critical because occupancy alone is insufficient for effective revenue management.",
  "purposeNote": "Dynamic pricing can respond to both booking pace and remaining selling time rather than relying solely on current occupancy.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 6 actions on this screen and the screen declares 1 operation.** Unserved: Sales per Hour, Sales per Day, Sales per Week, Current Booking Pace, Expected Booking Pace, Historical Booking Curve. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 80 §Support"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 80"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 80"
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
       "label": "Sales per Hour",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 80 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Sales per Day",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 80 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Sales per Week",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 80 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Current Booking Pace",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 80 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Expected Booking Pace",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 80 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Historical Booking Curve",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 80 §Support"
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
   "loading": "The booking velocity time-to-event list.",
   "error": "Could not load. Names which read failed and leaves the booking velocity time-to-event untouched.",
   "emptyFirstRun": "No booking velocity time-to-event yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the booking velocity time-to-event are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setBookingVelocityTime",
    "contract": "catalogue",
    "purpose": "Booking Velocity & Time-to-Event Rule Builder",
    "trigger": "onAction",
    "invalidates": [
     "setBookingVelocityTime"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-091"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 80. 0 of 0 labels bound to a contract property; 6 of 41 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-092",
  "name": "Seasonal, Calendar, Day & Timeslot Dynamic Rules",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "5",
   "number": "10.5.5",
   "page": 81
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/seasonal-calendar-day-timeslot-dynamic-rules-adm-092",
   "component": "apps/ticvai-web/src/routes/commercial/SeasonalCalendarDayTimeslotDynamicRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-088"
   ],
   "exitTo": [
    "ADM-088"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-088, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-088",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F147 step 8→9",
     "operation": "listSeasonalCalendarDay"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure dynamic pricing behavior according to temporal commercial patterns.",
  "purposeNote": "performances, and timeslots without creating conflicting temporal rules.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 81"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 81"
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
       "impliedBy": "listSeasonalCalendarDay",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The seasonal calendar day list.",
   "error": "Could not load. Names which read failed and leaves the seasonal calendar day untouched.",
   "emptyFirstRun": "No seasonal calendar day yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the seasonal calendar day are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listSeasonalCalendarDay",
    "contract": "catalogue",
    "purpose": "Seasonal, Calendar, Day & Timeslot Dynamic Rules",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "SeasonalCalendarDayTimeslotDynamicRulesView.season",
    "SeasonalCalendarDayTimeslotDynamicRulesView.month",
    "SeasonalCalendarDayTimeslotDynamicRulesView.week",
    "SeasonalCalendarDayTimeslotDynamicRulesView.dateRange",
    "SeasonalCalendarDayTimeslotDynamicRulesView.publicHoliday"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-092"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 81. 0 of 0 labels bound to a contract property; 0 of 33 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-093",
  "name": "Channel, Customer Segment & Location Dynamic Rules",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "5",
   "number": "10.5.6",
   "page": 83
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/channel-customer-segment-location-dynamic-rules-adm-093",
   "component": "apps/ticvai-web/src/routes/commercial/ChannelCustomerSegmentLocationDynamicRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-088"
   ],
   "exitTo": [
    "ADM-088"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-088, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-088",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F147 step 10→11",
     "operation": "listChannelCustomerSegment"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow dynamic-pricing behavior to differ according to commercial context.",
  "purposeNote": "Dynamic pricing can vary appropriately by channel, customer segment, and location without violating protected commercial agreements.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 83"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 83"
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
       "impliedBy": "listChannelCustomerSegment",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The channel customer segment list.",
   "error": "Could not load. Names which read failed and leaves the channel customer segment untouched.",
   "emptyFirstRun": "No channel customer segment yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the channel customer segment are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listChannelCustomerSegment",
    "contract": "catalogue",
    "purpose": "Channel, Customer Segment & Location Dynamic Rules",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "ChannelCustomerSegmentLocationDynamicRulesView.b2c",
    "ChannelCustomerSegmentLocationDynamicRulesView.mobileApp",
    "ChannelCustomerSegmentLocationDynamicRulesView.pos",
    "ChannelCustomerSegmentLocationDynamicRulesView.kiosk",
    "ChannelCustomerSegmentLocationDynamicRulesView.callCenter"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-093"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 83. 0 of 0 labels bound to a contract property; 0 of 38 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-094",
  "name": "Dynamic Price Bands, Ladders & Adjustment Matrix",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "5",
   "number": "10.5.7",
   "page": 84
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/dynamic-price-bands-ladders-adjustment-matrix-adm-094",
   "component": "apps/ticvai-web/src/routes/commercial/DynamicPriceBandsLaddersAdjustmentMatrix.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-088"
   ],
   "exitTo": [
    "ADM-088"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-088, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-088",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F147 step 12→13",
     "operation": "listDynamicPriceBand"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Define the controlled monetary steps through which prices can move. This is preferable to allowing unrestricted price generation for many products.",
  "purposeNote": "Dynamic prices move through controlled commercial price bands or adjustment ranges rather than generating arbitrary uncontrolled selling prices.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Fixed Price Bands. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 84 §Support"
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
       "label": "Maximum Bands per Movement",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 84 §Configure"
      },
      {
       "kind": "textField",
       "label": "Minimum Time Between Movements",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 84 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Upward Movement",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 84 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Downward Movement",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 84 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Reversal Rules",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 84 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Cooldown Period",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 84 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Fixed Price Bands",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 84 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The dynamic price bands configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the dynamic price bands untouched.",
   "emptyFirstRun": "No dynamic price bands configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listDynamicPriceBand",
    "contract": "catalogue",
    "purpose": "Dynamic Price Bands, Ladders & Adjustment Matrix",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-094"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 84. 0 of 0 labels bound to a contract property; 7 of 40 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-095",
  "name": "Dynamic Pricing Guardrails & Commercial Protection",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "5",
   "number": "10.5.8",
   "page": 86
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/dynamic-pricing-guardrails-commercial-protection-adm-095",
   "component": "apps/ticvai-web/src/routes/commercial/DynamicPricingGuardrailsCommercialProtection.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-088"
   ],
   "exitTo": [
    "ADM-088"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-088, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-088",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F147 step 14→15",
     "operation": "listDynamicPricingGuardrail"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Establish the non-negotiable boundaries for every dynamic-pricing strategy.",
  "purposeNote": "No dynamic pricing strategy can generate a selling price outside approved financial, contractual, operational, or regulatory boundaries.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Absolute Minimum Price",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 86 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Absolute Maximum Price",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 86 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Minimum Margin",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 86 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum Uplift %",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 86 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum Reduction %",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 86 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum Single Change",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 86 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum Daily Change",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 86 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum Weekly Change",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 86 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Minimum Change Interval",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 86 §Configure"
      },
      {
       "kind": "textField",
       "label": "Maximum Changes per Day",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 86 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Minimum Inventory",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 86 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum Occupancy Trigger",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 86 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "banner",
       "label": "Permissions this screen separates",
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** Freeze Product, Freeze Event, Freeze Performance, Freeze Strategy, Freeze Venue, Return to Base Price. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 86 §Authorized users can"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The dynamic pricing guardrails configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the dynamic pricing guardrails untouched.",
   "emptyFirstRun": "No dynamic pricing guardrails configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listDynamicPricingGuardrail",
    "contract": "catalogue",
    "purpose": "Dynamic Pricing Guardrails & Commercial Protection",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-095"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 86. 0 of 0 labels bound to a contract property; 18 of 32 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-096",
  "name": "Dynamic Pricing Automation Policy & Control",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "5",
   "number": "10.5.9",
   "page": 87
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/dynamic-pricing-automation-policy-control-adm-096",
   "component": "apps/ticvai-web/src/routes/commercial/DynamicPricingAutomationPolicyControl.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-088"
   ],
   "exitTo": [
    "ADM-088"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-088, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-088",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F147 step 16→17",
     "operation": "listDynamicPricingAutomation"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure independently by; Configure; Capture) and no display directory — it is settings, not a population",
  "purpose": "Define how much authority the pricing engine has to act on a calculated dynamic price. This is different from Board 4's approval workflow. Board 5 determines whether the engine may act automatically. Board 4 handles governance when formal approval is required.",
  "purposeNote": "authorized boundaries into the central governance process.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Product",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 87 §Configure independently by"
      },
      {
       "kind": "selectField",
       "label": "Event",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 87 §Configure independently by"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 87 §Configure independently by"
      },
      {
       "kind": "selectField",
       "label": "Strategy",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 87 §Configure independently by"
      },
      {
       "kind": "selectField",
       "label": "Channel",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 87 §Configure independently by"
      },
      {
       "kind": "selectField",
       "label": "Market",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 87 §Configure independently by"
      },
      {
       "kind": "textField",
       "label": "Maximum Automatic Changes / Day",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 87 §Configure"
      },
      {
       "kind": "textField",
       "label": "Minimum Time Between Changes",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 87 §Configure"
      },
      {
       "kind": "selectField",
       "label": "No-Change Windows",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 87 §Configure"
      },
      {
       "kind": "selectField",
       "label": "User",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 87 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Reason",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 87 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Override Price",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 87 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Start",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 87 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Expiry",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 87 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Return Behavior",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 87 §Capture"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The dynamic pricing automation configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the dynamic pricing automation untouched.",
   "emptyFirstRun": "No dynamic pricing automation configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listDynamicPricingAutomation",
    "contract": "catalogue",
    "purpose": "Dynamic Pricing Automation Policy & Control",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-096"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 87. 0 of 0 labels bound to a contract property; 15 of 41 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-097",
  "name": "Rule Priority, Conflict Resolution & Dynamic Pricing Test Console",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "5",
   "number": "10.5.10",
   "page": 89
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/rule-priority-conflict-resolution-dynamic-pricing-test-c-adm-097",
   "component": "apps/ticvai-web/src/routes/commercial/RulePriorityConflictResolutionDynamicPricingTest.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-088"
   ],
   "exitTo": [
    "ADM-088"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-088, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation."
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Identify; Show) and no metric row",
  "purpose": "Determine the final dynamic price when multiple strategies and rules are simultaneously applicable. This is the final and most important control screen of Board 5.",
  "purposeNote": "For any configured commercial scenario, TICVAI can deterministically calculate, test, and explain the final dynamic price before the strategy is activated. Board 5 — Final Screen Register # Backend Screen Primary Responsibility 10.5. Dynamic Pricing Strategy Command Center Strategy portfolio 1 10.5. Strategy master",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 2 actions on this screen and the screen declares 1 operation.** Unserved: Most Specific Rule Wins, Stop Processing. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 89 §Support"
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
       "label": "Every rule priority conflict",
       "columns": [
        "RulePriorityConflictResolutionDynamicPricingTestConsView.contradictoryRules",
        "RulePriorityConflictResolutionDynamicPricingTestConsView.samePriority",
        "RulePriorityConflictResolutionDynamicPricingTestConsView.impossibleCondition",
        "RulePriorityConflictResolutionDynamicPricingTestConsView.overlappingStrategy",
        "RulePriorityConflictResolutionDynamicPricingTestConsView.circularDependency",
        "RulePriorityConflictResolutionDynamicPricingTestConsView.missingFallback",
        "RulePriorityConflictResolutionDynamicPricingTestConsView.guardrailConflict",
        "RulePriorityConflictResolutionDynamicPricingTestConsView.whyAed300"
       ],
       "bindsTo": "RulePriorityConflictResolutionDynamicPricingTestConsView",
       "operation": "listRulePriorityConflict",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 89 §Identify"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected rule priority conflict",
       "bindsTo": "RulePriorityConflictResolutionDynamicPricingTestConsView",
       "columns": [
        "RulePriorityConflictResolutionDynamicPricingTestConsView.contradictoryRules",
        "RulePriorityConflictResolutionDynamicPricingTestConsView.samePriority",
        "RulePriorityConflictResolutionDynamicPricingTestConsView.impossibleCondition",
        "RulePriorityConflictResolutionDynamicPricingTestConsView.overlappingStrategy",
        "RulePriorityConflictResolutionDynamicPricingTestConsView.circularDependency",
        "RulePriorityConflictResolutionDynamicPricingTestConsView.missingFallback",
        "RulePriorityConflictResolutionDynamicPricingTestConsView.guardrailConflict",
        "RulePriorityConflictResolutionDynamicPricingTestConsView.whyAed300"
       ],
       "notes": "The pack groups this record's detail under its own headings: “For one Saturday evening ticket”, “Priority Matrix”, “Commercial Protection”, “Contract/Member Protection”, “Event-Specific Strategy”, “Inventory/Occupancy”.",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 89 §Identify"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Most Specific Rule Wins",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 89 §Support"
      },
      {
       "kind": "destructiveButton",
       "label": "Stop Processing",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 89 §Support"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmStopProcessing",
    "component": "confirmDialog",
    "trigger": "Stop Processing",
    "body": "**Stop Processing on a rule priority conflict is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 89 §Support"
   }
  ],
  "states": {
   "loading": "The rule priority conflict list.",
   "error": "Could not load. Names which read failed and leaves the rule priority conflict untouched.",
   "emptyFirstRun": "No rule priority conflict yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the rule priority conflict are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listRulePriorityConflict",
    "contract": "catalogue",
    "purpose": "Rule Priority, Conflict Resolution & Dynamic Pricing Test Console",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "RulePriorityConflictResolutionDynamicPricingTestConsView.contradictoryRules",
    "RulePriorityConflictResolutionDynamicPricingTestConsView.samePriority",
    "RulePriorityConflictResolutionDynamicPricingTestConsView.impossibleCondition",
    "RulePriorityConflictResolutionDynamicPricingTestConsView.overlappingStrategy",
    "RulePriorityConflictResolutionDynamicPricingTestConsView.circularDependency",
    "RulePriorityConflictResolutionDynamicPricingTestConsView.missingFallback"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-097"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 89. 8 of 8 labels bound to a contract property; 10 of 143 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "listChannelCustomerSegment": {
  "method": "GET",
  "path": "/channel-customer-segment",
  "contract": "catalogue",
  "summary": "Channel, Customer Segment & Location Dynamic Rules",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ChannelCustomerSegmentLocationDynamicRulesView"
 },
 "listDynamicPriceBand": {
  "method": "GET",
  "path": "/dynamic-price-band",
  "contract": "catalogue",
  "summary": "Dynamic Price Bands, Ladders & Adjustment Matrix",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "DynamicPriceBandsLaddersAdjustmentMatrixView"
 },
 "listDynamicPricingAutomation": {
  "method": "GET",
  "path": "/dynamic-pricing-automation",
  "contract": "catalogue",
  "summary": "Dynamic Pricing Automation Policy & Control",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "DynamicPricingAutomationPolicyControlView"
 },
 "listDynamicPricingGuardrail": {
  "method": "GET",
  "path": "/dynamic-pricing-guardrail",
  "contract": "catalogue",
  "summary": "Dynamic Pricing Guardrails & Commercial Protection",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "DynamicPricingGuardrailsCommercialProtectionView"
 },
 "listDynamicPricingStrategy": {
  "method": "GET",
  "path": "/dynamic-pricing-strategy",
  "contract": "catalogue",
  "summary": "Dynamic Pricing Strategy Command Center",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "DynamicPricingStrategyCommandCenterView"
 },
 "listRulePriorityConflict": {
  "method": "GET",
  "path": "/rule-priority-conflict",
  "contract": "catalogue",
  "summary": "Rule Priority, Conflict Resolution & Dynamic Pricing Test Console",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "RulePriorityConflictResolutionDynamicPricingTestConsView"
 },
 "listSeasonalCalendarDay": {
  "method": "GET",
  "path": "/seasonal-calendar-day",
  "contract": "catalogue",
  "summary": "Seasonal, Calendar, Day & Timeslot Dynamic Rules",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "SeasonalCalendarDayTimeslotDynamicRulesView"
 },
 "setBookingVelocityTime": {
  "method": "PUT",
  "path": "/booking-velocity-time",
  "contract": "catalogue",
  "summary": "Booking Velocity & Time-to-Event Rule Builder",
  "permission": "PRODUCT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "BookingVelocityTimeToEventRuleBuilderInput",
  "responds": "BookingVelocityTimeToEventRuleBuilderView"
 },
 "setDemandOccupancyAvailability": {
  "method": "PUT",
  "path": "/demand-occupancy-availability",
  "contract": "catalogue",
  "summary": "Demand, Occupancy & Availability Rule Builder",
  "permission": "PRODUCT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "DemandOccupancyAvailabilityRuleBuilderInput",
  "responds": "DemandOccupancyAvailabilityRuleBuilderView"
 },
 "setDynamicPricingStrategy": {
  "method": "PUT",
  "path": "/dynamic-pricing-strategy-2",
  "contract": "catalogue",
  "summary": "Dynamic Pricing Strategy Builder",
  "permission": "PRODUCT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "DynamicPricingStrategyBuilderInput",
  "responds": "DynamicPricingStrategyBuilderView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "BookingVelocityTimeToEventRuleBuilderInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Booking Velocity & Time-to-Event Rule Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "salesPerHour": {
    "type": "string",
    "description": "Sales per Hour"
   },
   "salesPerDay": {
    "type": "string",
    "description": "Sales per Day"
   },
   "salesPerWeek": {
    "type": "string",
    "description": "Sales per Week"
   },
   "currentBookingPace": {
    "type": "string",
    "description": "Current Booking Pace"
   },
   "expectedBookingPace": {
    "type": "string",
    "description": "Expected Booking Pace"
   },
   "historicalBookingCurve": {
    "type": "string",
    "description": "Historical Booking Curve"
   },
   "paceVariance": {
    "type": "number",
    "description": "Pace Variance %"
   },
   "remainingInventory": {
    "type": "string",
    "description": "Remaining Inventory"
   },
   "t180": {
    "type": "string",
    "description": "T−180"
   },
   "t90": {
    "type": "string",
    "description": "T−90"
   },
   "t60": {
    "type": "string",
    "description": "T−60"
   },
   "t30": {
    "type": "string",
    "description": "T−30"
   },
   "t14": {
    "type": "string",
    "description": "T−14"
   },
   "t7": {
    "type": "string",
    "description": "T−7"
   },
   "t3": {
    "type": "string",
    "description": "T−3"
   },
   "t1": {
    "type": "string",
    "description": "T−1"
   },
   "sameDay": {
    "type": "string",
    "description": "Same Day"
   },
   "orCustomIntervals": {
    "type": "string",
    "description": "or custom intervals"
   },
   "increaseCurrentPriceBy5": {
    "type": "number",
    "description": "Increase current price by 5%"
   },
   "t2Days": {
    "type": "string",
    "description": "T−2 Days"
   },
   "then15": {
    "type": "number",
    "description": "THEN +15%"
   }
  }
 },
 "BookingVelocityTimeToEventRuleBuilderView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Booking Velocity & Time-to-Event Rule Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "salesPerHour": {
    "type": "string",
    "description": "Sales per Hour"
   },
   "salesPerDay": {
    "type": "string",
    "description": "Sales per Day"
   },
   "salesPerWeek": {
    "type": "string",
    "description": "Sales per Week"
   },
   "currentBookingPace": {
    "type": "string",
    "description": "Current Booking Pace"
   },
   "expectedBookingPace": {
    "type": "string",
    "description": "Expected Booking Pace"
   },
   "historicalBookingCurve": {
    "type": "string",
    "description": "Historical Booking Curve"
   },
   "paceVariance": {
    "type": "number",
    "description": "Pace Variance %"
   },
   "remainingInventory": {
    "type": "string",
    "description": "Remaining Inventory"
   },
   "t180": {
    "type": "string",
    "description": "T−180"
   },
   "t90": {
    "type": "string",
    "description": "T−90"
   },
   "t60": {
    "type": "string",
    "description": "T−60"
   },
   "t30": {
    "type": "string",
    "description": "T−30"
   },
   "t14": {
    "type": "string",
    "description": "T−14"
   },
   "t7": {
    "type": "string",
    "description": "T−7"
   },
   "t3": {
    "type": "string",
    "description": "T−3"
   },
   "t1": {
    "type": "string",
    "description": "T−1"
   },
   "sameDay": {
    "type": "string",
    "description": "Same Day"
   },
   "orCustomIntervals": {
    "type": "string",
    "description": "or custom intervals"
   },
   "velocity": {
    "type": "string",
    "description": "Velocity (the pack shows +45%)"
   },
   "increaseCurrentPriceBy5": {
    "type": "number",
    "description": "Increase current price by 5%"
   },
   "t2Days": {
    "type": "string",
    "description": "T−2 Days"
   },
   "then15": {
    "type": "number",
    "description": "THEN +15%"
   }
  }
 },
 "ChannelCustomerSegmentLocationDynamicRulesView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Channel, Customer Segment & Location Dynamic Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "b2c": {
    "type": "string",
    "description": "B2C"
   },
   "mobileApp": {
    "type": "string",
    "description": "Mobile App"
   },
   "pos": {
    "type": "string",
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
   "api": {
    "type": "string",
    "description": "API"
   },
   "dynamicRange15": {
    "type": "number",
    "description": "Dynamic range ±15%"
   },
   "dynamicRange0To10": {
    "type": "number",
    "description": "Dynamic range +0% to +10%"
   },
   "standardCustomer": {
    "type": "string",
    "description": "Standard Customer"
   },
   "member": {
    "type": "string",
    "description": "Member"
   },
   "loyaltyTier": {
    "type": "string",
    "description": "Loyalty Tier"
   },
   "resident": {
    "type": "string",
    "description": "Resident"
   },
   "vip": {
    "type": "string",
    "description": "VIP"
   },
   "corporate": {
    "type": "string",
    "description": "Corporate"
   },
   "group": {
    "type": "string",
    "description": "Group"
   },
   "customSegment": {
    "type": "string",
    "description": "Custom Segment"
   },
   "country": {
    "type": "string",
    "description": "Country"
   },
   "market": {
    "type": "string",
    "description": "Market"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "attraction": {
    "type": "string",
    "description": "Attraction"
   },
   "zone": {
    "type": "string",
    "description": "Zone"
   },
   "eventLocation": {
    "type": "string",
    "description": "Event Location"
   },
   "maximumDynamicUplift20": {
    "type": "number",
    "description": "Maximum dynamic uplift +20%"
   },
   "maximum15": {
    "type": "number",
    "description": "Maximum +15%"
   },
   "partnerContractRates": {
    "type": "string",
    "description": "Partner Contract Rates"
   },
   "corporateAgreements": {
    "type": "string",
    "description": "Corporate Agreements"
   },
   "membershipGuarantees": {
    "type": "string",
    "description": "Membership Guarantees"
   },
   "fixedGroupRates": {
    "type": "string",
    "description": "Fixed Group Rates"
   }
  }
 },
 "DemandOccupancyAvailabilityRuleBuilderInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Demand, Occupancy & Availability Rule Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "ticketsSold": {
    "type": "string",
    "description": "Tickets Sold"
   },
   "currentDemand": {
    "type": "string",
    "description": "Current Demand"
   },
   "occupancy": {
    "type": "integer",
    "description": "Occupancy %"
   },
   "remainingCapacity": {
    "type": "integer",
    "description": "Remaining Capacity"
   },
   "remainingInventory": {
    "type": "string",
    "description": "Remaining Inventory"
   },
   "availableSeats": {
    "type": "integer",
    "description": "Available Seats"
   },
   "capacityUtilization": {
    "type": "integer",
    "description": "Capacity Utilization"
   },
   "salesPace": {
    "type": "string",
    "description": "Sales Pace"
   },
   "cyAction": {
    "type": "string",
    "description": "cy Action"
   }
  }
 },
 "DemandOccupancyAvailabilityRuleBuilderView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Demand, Occupancy & Availability Rule Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "ticketsSold": {
    "type": "string",
    "description": "Tickets Sold"
   },
   "currentDemand": {
    "type": "string",
    "description": "Current Demand"
   },
   "occupancy": {
    "type": "integer",
    "description": "Occupancy %"
   },
   "remainingCapacity": {
    "type": "integer",
    "description": "Remaining Capacity"
   },
   "remainingInventory": {
    "type": "string",
    "description": "Remaining Inventory"
   },
   "availableSeats": {
    "type": "integer",
    "description": "Available Seats"
   },
   "capacityUtilization": {
    "type": "integer",
    "description": "Capacity Utilization"
   },
   "salesPace": {
    "type": "string",
    "description": "Sales Pace"
   },
   "cyAction": {
    "type": "string",
    "description": "cy Action"
   }
  }
 },
 "DynamicPriceBandsLaddersAdjustmentMatrixView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Dynamic Price Bands, Ladders & Adjustment Matrix displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "p1": {
    "type": "string",
    "description": "P1"
   },
   "p2": {
    "type": "string",
    "description": "P2"
   },
   "p3": {
    "type": "string",
    "description": "P3"
   },
   "p4": {
    "type": "string",
    "description": "P4"
   },
   "p5": {
    "type": "string",
    "description": "P5"
   },
   "p6": {
    "type": "string",
    "description": "P6"
   },
   "p7": {
    "type": "string",
    "description": "P7"
   },
   "fixedPriceBands": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Fixed Price Bands"
   },
   "percentageBands": {
    "type": "number",
    "description": "Percentage Bands"
   },
   "fixedAmountSteps": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Fixed Amount Steps"
   },
   "derivedBands": {
    "type": "string",
    "description": "Derived Bands"
   },
   "continuousRangeWherePermitted": {
    "type": "string",
    "description": "Continuous Range where permitted"
   },
   "maximumBandsPerMovement": {
    "type": "string",
    "description": "Maximum Bands per Movement"
   },
   "minimumTimeBetweenMovements": {
    "type": "string",
    "format": "date-time",
    "description": "Minimum Time Between Movements"
   },
   "upwardMovement": {
    "type": "string",
    "description": "Upward Movement"
   },
   "downwardMovement": {
    "type": "string",
    "description": "Downward Movement"
   },
   "reversalRules": {
    "type": "string",
    "description": "Reversal Rules"
   },
   "cooldownPeriod": {
    "type": "string",
    "format": "date-time",
    "description": "Cooldown Period"
   },
   "maximum5PerAdjustment": {
    "type": "number",
    "description": "Maximum +5% per adjustment"
   },
   "maximum10": {
    "type": "number",
    "description": "Maximum −10%"
   },
   "whereRequired": {
    "type": "boolean",
    "description": "where required"
   },
   "minimumBaseMaximum": {
    "type": "string",
    "description": "Minimum → Base → Maximum"
   }
  }
 },
 "DynamicPricingAutomationPolicyControlView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Dynamic Pricing Automation Policy & Control displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "mode0Monitor": {
    "type": "string",
    "description": "Mode 0 — Monitor"
   },
   "mode1Recommend": {
    "type": "string",
    "description": "Mode 1 — Recommend"
   },
   "mode2PrepareChange": {
    "type": "string",
    "description": "Mode 2 — Prepare Change"
   },
   "nt": {
    "type": "string",
    "description": "nt"
   },
   "thresholdMet": {
    "type": "integer",
    "description": "threshold met"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
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
   "maximumAutomaticChangesDay": {
    "type": "string",
    "description": "Maximum Automatic Changes / Day"
   },
   "minimumTimeBetweenChanges": {
    "type": "string",
    "format": "date-time",
    "description": "Minimum Time Between Changes"
   },
   "noChangeWindows": {
    "type": "string",
    "description": "No-Change Windows"
   },
   "user": {
    "type": "string",
    "description": "User"
   },
   "reason": {
    "type": "string",
    "description": "Reason"
   },
   "start": {
    "type": "string",
    "description": "Start"
   },
   "expiry": {
    "type": "string",
    "format": "date-time",
    "description": "Expiry"
   },
   "returnBehavior": {
    "type": "string",
    "description": "Return Behavior"
   }
  }
 },
 "DynamicPricingGuardrailsCommercialProtectionView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Dynamic Pricing Guardrails & Commercial Protection displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "absoluteMinimumPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Absolute Minimum Price"
   },
   "absoluteMaximumPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Absolute Maximum Price"
   },
   "minimumMargin": {
    "type": "number",
    "description": "Minimum Margin"
   },
   "maximumUplift": {
    "type": "number",
    "description": "Maximum Uplift %"
   },
   "maximumReduction": {
    "type": "number",
    "description": "Maximum Reduction %"
   },
   "maximumSingleChange": {
    "type": "string",
    "description": "Maximum Single Change"
   },
   "maximumDailyChange": {
    "type": "string",
    "description": "Maximum Daily Change"
   },
   "maximumWeeklyChange": {
    "type": "string",
    "description": "Maximum Weekly Change"
   },
   "minimumChangeInterval": {
    "type": "string",
    "description": "Minimum Change Interval"
   },
   "maximumChangesPerDay": {
    "type": "string",
    "description": "Maximum Changes per Day"
   },
   "minimumInventory": {
    "type": "string",
    "description": "Minimum Inventory"
   },
   "maximumOccupancyTrigger": {
    "type": "integer",
    "description": "Maximum Occupancy Trigger"
   },
   "contractRates": {
    "type": "string",
    "description": "Contract Rates"
   },
   "membershipRates": {
    "type": "string",
    "description": "Membership Rates"
   },
   "corporateRates": {
    "type": "string",
    "description": "Corporate Rates"
   },
   "promotionalLockedRates": {
    "type": "string",
    "description": "Promotional Locked Rates"
   },
   "regulatoryPrices": {
    "type": "string",
    "description": "Regulatory Prices"
   },
   "complimentaryRates": {
    "type": "string",
    "description": "Complimentary Rates"
   },
   "alreadyPurchasedTickets": {
    "type": "string",
    "description": "Already Purchased Tickets"
   },
   "existingReservationsWhereApplicable": {
    "type": "string",
    "description": "Existing Reservations where applicable"
   },
   "returnToBasePrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Return to Base Price"
   },
   "controlForCriticalIncidents": {
    "type": "string",
    "description": "control for critical incidents"
   }
  }
 },
 "DynamicPricingStrategyBuilderInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Dynamic Pricing Strategy Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "strategyName": {
    "type": "string",
    "description": "Strategy Name"
   },
   "strategyCode": {
    "type": "string",
    "description": "Strategy Code"
   },
   "description": {
    "type": "string",
    "description": "Description"
   },
   "strategyType": {
    "type": "string",
    "description": "Strategy Type"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   },
   "businessUnit": {
    "type": "string",
    "description": "Business Unit"
   },
   "market": {
    "type": "string",
    "description": "Market"
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
   "performance": {
    "type": "string",
    "description": "Performance"
   },
   "timeslot": {
    "type": "string",
    "description": "Timeslot"
   },
   "priceCategory": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price Category"
   },
   "basePriceSource": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Base Price Source"
   },
   "effectiveFrom": {
    "type": "string",
    "description": "Effective From"
   },
   "effectiveTo": {
    "type": "string",
    "description": "Effective To"
   },
   "evaluationFrequency": {
    "type": "string",
    "description": "Evaluation Frequency"
   },
   "status": {
    "type": "string",
    "description": "Status"
   },
   "singleProduct": {
    "type": "string",
    "description": "Single Product"
   },
   "productFamily": {
    "type": "string",
    "description": "Product Family"
   },
   "multiplePerformances": {
    "type": "string",
    "description": "Multiple Performances"
   },
   "selectedTimeslots": {
    "type": "string",
    "description": "Selected Timeslots"
   },
   "selectedPriceCategories": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Selected Price Categories"
   },
   "operatesIndependently": {
    "type": "string",
    "description": "Operates Independently"
   },
   "canCombineWithOtherStrategies": {
    "type": "boolean",
    "description": "Can Combine with Other Strategies"
   },
   "hasExclusiveControl": {
    "type": "boolean",
    "description": "Has Exclusive Control"
   },
   "actsAsFallback": {
    "type": "string",
    "description": "Acts as Fallback"
   },
   "canBecome": {
    "type": "boolean",
    "description": "can become"
   }
  }
 },
 "DynamicPricingStrategyBuilderView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Dynamic Pricing Strategy Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "strategyName": {
    "type": "string",
    "description": "Strategy Name"
   },
   "strategyCode": {
    "type": "string",
    "description": "Strategy Code"
   },
   "description": {
    "type": "string",
    "description": "Description"
   },
   "strategyType": {
    "type": "string",
    "description": "Strategy Type"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   },
   "businessUnit": {
    "type": "string",
    "description": "Business Unit"
   },
   "market": {
    "type": "string",
    "description": "Market"
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
   "performance": {
    "type": "string",
    "description": "Performance"
   },
   "timeslot": {
    "type": "string",
    "description": "Timeslot"
   },
   "priceCategory": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price Category"
   },
   "basePriceSource": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Base Price Source"
   },
   "effectiveFrom": {
    "type": "string",
    "description": "Effective From"
   },
   "effectiveTo": {
    "type": "string",
    "description": "Effective To"
   },
   "evaluationFrequency": {
    "type": "string",
    "description": "Evaluation Frequency"
   },
   "status": {
    "type": "string",
    "description": "Status"
   },
   "singleProduct": {
    "type": "string",
    "description": "Single Product"
   },
   "productFamily": {
    "type": "string",
    "description": "Product Family"
   },
   "multiplePerformances": {
    "type": "string",
    "description": "Multiple Performances"
   },
   "selectedTimeslots": {
    "type": "string",
    "description": "Selected Timeslots"
   },
   "selectedPriceCategories": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Selected Price Categories"
   },
   "operatesIndependently": {
    "type": "string",
    "description": "Operates Independently"
   },
   "canCombineWithOtherStrategies": {
    "type": "boolean",
    "description": "Can Combine with Other Strategies"
   },
   "hasExclusiveControl": {
    "type": "boolean",
    "description": "Has Exclusive Control"
   },
   "actsAsFallback": {
    "type": "string",
    "description": "Acts as Fallback"
   },
   "canBecome": {
    "type": "boolean",
    "description": "can become"
   }
  }
 },
 "DynamicPricingStrategyCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Dynamic Pricing Strategy Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "activeStrategies": {
    "type": "integer",
    "description": "Active Strategies"
   },
   "draftStrategies": {
    "type": "integer",
    "description": "Draft Strategies"
   },
   "productsUnderDynamicPricing": {
    "type": "string",
    "description": "Products Under Dynamic Pricing"
   },
   "eventsUnderDynamicPricing": {
    "type": "string",
    "description": "Events Under Dynamic Pricing"
   },
   "performancesUnderDynamicPricing": {
    "type": "string",
    "description": "Performances Under Dynamic Pricing"
   },
   "rulesActive": {
    "type": "integer",
    "description": "Rules Active"
   },
   "currentPriceAdjustments": {
    "type": "integer",
    "description": "Current Price Adjustments"
   },
   "pricesAtMaximumGuardrail": {
    "type": "string",
    "description": "Prices at Maximum Guardrail"
   },
   "pricesAtMinimumGuardrail": {
    "type": "string",
    "description": "Prices at Minimum Guardrail"
   },
   "ruleConflicts": {
    "type": "integer",
    "description": "Rule Conflicts"
   },
   "frozenStrategies": {
    "type": "integer",
    "description": "Frozen Strategies"
   },
   "upcomingActivations": {
    "type": "integer",
    "description": "Upcoming Activations"
   },
   "strategyId": {
    "type": "string",
    "description": "Strategy ID"
   },
   "strategyName": {
    "type": "string",
    "description": "Strategy Name"
   },
   "strategyType": {
    "type": "string",
    "description": "Strategy Type"
   },
   "productEvent": {
    "type": "string",
    "description": "Product/Event"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "basePriceSource": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Base Price Source"
   },
   "currentPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Current Price"
   },
   "adjustmentRange": {
    "type": "string",
    "description": "Adjustment Range"
   },
   "ruleCount": {
    "type": "integer",
    "description": "Rule Count"
   },
   "effectivePeriod": {
    "type": "string",
    "format": "date-time",
    "description": "Effective Period"
   },
   "automationMode": {
    "type": "string",
    "description": "Automation Mode"
   },
   "status": {
    "type": "integer",
    "description": "Status"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   },
   "demandBased": {
    "type": "string",
    "description": "Demand Based"
   },
   "occupancyBased": {
    "type": "integer",
    "description": "Occupancy Based"
   },
   "availabilityBased": {
    "type": "string",
    "description": "Availability Based"
   },
   "inventoryBased": {
    "type": "string",
    "description": "Inventory Based"
   },
   "bookingVelocity": {
    "type": "string",
    "description": "Booking Velocity"
   },
   "timeToEvent": {
    "type": "string",
    "format": "date-time",
    "description": "Time-to-Event"
   },
   "seasonal": {
    "type": "string",
    "description": "Seasonal"
   },
   "dayOfWeek": {
    "type": "string",
    "description": "Day-of-Week"
   },
   "timeslot": {
    "type": "string",
    "description": "Timeslot"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "segment": {
    "type": "string",
    "description": "Segment"
   },
   "location": {
    "type": "string",
    "description": "Location"
   },
   "hybrid": {
    "type": "string",
    "description": "Hybrid"
   },
   "test": {
    "type": "string",
    "description": "Test"
   },
   "retire": {
    "type": "string",
    "description": "Retire"
   }
  }
 },
 "RulePriorityConflictResolutionDynamicPricingTestConsView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Rule Priority, Conflict Resolution & Dynamic Pricing Test Console displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "basePriceAed250": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Base Price: AED 250"
   },
   "weekend5": {
    "type": "number",
    "description": "Weekend → +5%"
   },
   "occupancy8710": {
    "type": "integer",
    "description": "Occupancy 87% → +10%"
   },
   "bookingVelocity305": {
    "type": "number",
    "description": "Booking Velocity +30% → +5%"
   },
   "t3Days8": {
    "type": "number",
    "description": "T−3 Days → +8%"
   },
   "highestPriorityWins": {
    "type": "string",
    "description": "Highest Priority Wins"
   },
   "mostSpecificRuleWins": {
    "type": "string",
    "description": "Most Specific Rule Wins"
   },
   "cumulativeAdjustment": {
    "type": "string",
    "description": "Cumulative Adjustment"
   },
   "maximumAdjustmentWins": {
    "type": "string",
    "description": "Maximum Adjustment Wins"
   },
   "minimumAdjustmentWins": {
    "type": "string",
    "description": "Minimum Adjustment Wins"
   },
   "weightedCombination": {
    "type": "string",
    "description": "Weighted Combination"
   },
   "stopProcessing": {
    "type": "string",
    "description": "Stop Processing"
   },
   "customGovernedResolution": {
    "type": "string",
    "description": "Custom Governed Resolution"
   },
   "administratorsConfigureRuleHierarchy": {
    "type": "string",
    "description": "Administrators configure rule hierarchy"
   },
   "contradictoryRules": {
    "type": "string",
    "description": "Contradictory Rules"
   },
   "samePriority": {
    "type": "string",
    "description": "Same Priority"
   },
   "impossibleCondition": {
    "type": "string",
    "description": "Impossible Condition"
   },
   "overlappingStrategy": {
    "type": "string",
    "description": "Overlapping Strategy"
   },
   "circularDependency": {
    "type": "string",
    "description": "Circular Dependency"
   },
   "missingFallback": {
    "type": "string",
    "description": "Missing Fallback"
   },
   "guardrailConflict": {
    "type": "string",
    "description": "Guardrail Conflict"
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
   "date": {
    "type": "string",
    "format": "date-time",
    "description": "Date"
   },
   "timeslot": {
    "type": "string",
    "description": "Timeslot"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "customerSegment": {
    "type": "string",
    "description": "Customer Segment"
   },
   "basePrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Base Price"
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
   "timeToEvent": {
    "type": "string",
    "format": "date-time",
    "description": "Time-to-Event"
   },
   "occupancy10": {
    "type": "integer",
    "description": "Occupancy +10%"
   },
   "velocity5": {
    "type": "number",
    "description": "Velocity +5%"
   },
   "whyAed300": {
    "type": "string",
    "description": "Why AED 300?"
   },
   "withTheCompleteCalculationPath": {
    "type": "string",
    "description": "with the complete calculation path"
   },
   "lowDemand": {
    "type": "string",
    "description": "Low Demand"
   },
   "highDemand": {
    "type": "string",
    "description": "High Demand"
   },
   "nearSellOut": {
    "type": "string",
    "description": "Near Sell-Out"
   }
  }
 },
 "SeasonalCalendarDayTimeslotDynamicRulesView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Seasonal, Calendar, Day & Timeslot Dynamic Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "season": {
    "type": "string",
    "description": "Season"
   },
   "month": {
    "type": "string",
    "description": "Month"
   },
   "week": {
    "type": "string",
    "description": "Week"
   },
   "dateRange": {
    "type": "string",
    "format": "date-time",
    "description": "Date Range"
   },
   "publicHoliday": {
    "type": "string",
    "description": "Public Holiday"
   },
   "schoolHoliday": {
    "type": "string",
    "description": "School Holiday"
   },
   "dayOfWeek": {
    "type": "string",
    "description": "Day of Week"
   },
   "weekend": {
    "type": "string",
    "description": "Weekend"
   },
   "timeOfDay": {
    "type": "string",
    "format": "date-time",
    "description": "Time of Day"
   },
   "timeslot": {
    "type": "string",
    "description": "Timeslot"
   },
   "performance": {
    "type": "string",
    "description": "Performance"
   },
   "specialDate": {
    "type": "string",
    "format": "date-time",
    "description": "Special Date"
   },
   "base20": {
    "type": "number",
    "description": "Base → +20%"
   },
   "baseTo15": {
    "type": "number",
    "description": "Base to +15%"
   },
   "baseTo20": {
    "type": "number",
    "description": "Base to +20%"
   },
   "ramadan": {
    "type": "string",
    "description": "Ramadan"
   },
   "eid": {
    "type": "string",
    "description": "Eid"
   },
   "christmas": {
    "type": "string",
    "description": "Christmas"
   },
   "newYear": {
    "type": "integer",
    "description": "New Year"
   },
   "schoolBreak": {
    "type": "string",
    "description": "School Break"
   },
   "nationalDay": {
    "type": "string",
    "description": "National Day"
   },
   "customCommercialCalendar": {
    "type": "string",
    "description": "Custom Commercial Calendar"
   }
  }
 }
}
```
