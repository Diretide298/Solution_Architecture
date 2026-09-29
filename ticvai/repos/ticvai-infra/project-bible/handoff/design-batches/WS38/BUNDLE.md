# WS38 — Pricing   Revenue Management board 5

**10 screens · 15 operations · 23 schemas · 3 permissions**

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

- **Every control that can be refused must be gated.** 3 permissions apply here:
  `PRICE_CONFIGURE, PRODUCT_CONFIGURE, PRODUCT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-088` | Dynamic Pricing Strategy Command Center | commandCentre | 2 | 1 | — |
| `ADM-089` | Dynamic Pricing Strategy Builder | configEditor | 2 | 1 | — |
| `ADM-090` | Demand, Occupancy & Availability Rule Builder | listDetail | 1 | 0 | — |
| `ADM-091` | Booking Velocity & Time-to-Event Rule Builder | listDetail | 1 | 0 | — |
| `ADM-092` | Seasonal, Calendar, Day & Timeslot Dynamic Rules | listDetail | 2 | 1 | — |
| `ADM-093` | Channel, Customer Segment & Location Dynamic Rules | listDetail | 1 | 0 | — |
| `ADM-094` | Dynamic Price Bands, Ladders & Adjustment Matrix | configEditor | 2 | 1 | — |
| `ADM-095` | Dynamic Pricing Guardrails & Commercial Protection | configEditor | 2 | 1 | — |
| `ADM-096` | Dynamic Pricing Automation Policy & Control | configEditor | 2 | 1 | — |
| `ADM-097` | Rule Priority, Conflict Resolution & Dynamic Pricing Test Console | listDetail | 2 | 1 | — |

## Thin screens in this batch

**ADM-090, ADM-093 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

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
     "provenance": "derived — ADM-002 declares entryState.params  and ADM-088 holds none of them, so the edge carries nothing and ADM-002 opens cold"
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
    },
    {
     "to": "ADM-089",
     "trigger": "Works in Dynamic Pricing Strategy Builder",
     "provenance": "flow F147 step 1→2",
     "operation": "listDynamicPricingStrategy",
     "carries": [
      "strategyId"
     ]
    },
    {
     "to": "ADM-094",
     "trigger": "Works in Dynamic Price Bands, Ladders & Adjustment Matrix",
     "provenance": "flow F147 step 11→12",
     "operation": "listDynamicPricingStrategy",
     "carries": [
      "strategyId"
     ]
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Authorized users can view and manage the complete dynamic-pricing strategy portfolio from one centralized workspace.",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each strategy should show) — counts over a population, then the population",
  "purpose": "Provide the central backend workspace for creating, monitoring, and managing all dynamic- pricing strategies. This should be the primary operational screen for Revenue Managers.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 13 actions on this screen and the screen declares 1 operation.** Unserved: Demand Based, Inventory Based, Booking Velocity, Timeslot, Channel, Create Strategy, Duplicate, Open …. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
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
       "bindsTo": "DynamicPricingStrategyCommandCenterSummary.activeStrategies"
      },
      {
       "kind": "metricTile",
       "label": "Draft Strategies",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 75 §Display",
       "bindsTo": "DynamicPricingStrategyCommandCenterSummary.draftStrategies"
      },
      {
       "kind": "metricTile",
       "label": "Products Under Dynamic Pricing",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 75 §Display",
       "bindsTo": "DynamicPricingStrategyCommandCenterSummary.productsUnderDynamicPricing"
      },
      {
       "kind": "metricTile",
       "label": "Events Under Dynamic Pricing",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 75 §Display",
       "bindsTo": "DynamicPricingStrategyCommandCenterSummary.eventsUnderDynamicPricing"
      },
      {
       "kind": "metricTile",
       "label": "Performances Under Dynamic Pricing",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 75 §Display",
       "bindsTo": "DynamicPricingStrategyCommandCenterSummary.performancesUnderDynamicPricing"
      },
      {
       "kind": "metricTile",
       "label": "Rules Active",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 75 §Display",
       "bindsTo": "DynamicPricingStrategyCommandCenterSummary.rulesActive"
      },
      {
       "kind": "metricTile",
       "label": "Current Price Adjustments",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 75 §Display",
       "bindsTo": "DynamicPricingStrategyCommandCenterSummary.currentPriceAdjustments"
      },
      {
       "kind": "metricTile",
       "label": "Prices at Maximum Guardrail",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 75 §Display",
       "bindsTo": "DynamicPricingStrategyCommandCenterSummary.pricesAtMaximumGuardrail"
      },
      {
       "kind": "metricTile",
       "label": "Prices at Minimum Guardrail",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 75 §Display",
       "bindsTo": "DynamicPricingStrategyCommandCenterSummary.pricesAtMinimumGuardrail"
      },
      {
       "kind": "metricTile",
       "label": "Rule Conflicts",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 75 §Display",
       "bindsTo": "DynamicPricingStrategyCommandCenterSummary.ruleConflicts"
      },
      {
       "kind": "metricTile",
       "label": "Frozen Strategies",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 75 §Display",
       "bindsTo": "DynamicPricingStrategyCommandCenterSummary.frozenStrategies"
      },
      {
       "kind": "metricTile",
       "label": "Upcoming Activations",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 75 §Display",
       "bindsTo": "DynamicPricingStrategyCommandCenterSummary.upcomingActivations"
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
       "label": "Demand Based",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 75 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Inventory Based",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 75 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Booking Velocity",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 75 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Timeslot",
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
       "label": "Transition dynamic pricing strategy",
       "operation": "transitionDynamicPricingStrategy",
       "permission": "PRICE_CONFIGURE",
       "notes": "**The strategy's status moves, as calls** (29 September, writers pass).",
       "provenance": "contract catalogue.yaml POST /dynamic-pricing-strategies/{strategyId}/lifecycle"
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
   },
   {
    "operationId": "transitionDynamicPricingStrategy",
    "contract": "catalogue",
    "purpose": "Activate, pause, resume or retire a dynamic pricing strategy",
    "trigger": "onAction",
    "invalidates": [
     "listDynamicPricingStrategy"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-088",
   "workshopBoard": "wireframes/WS99 Pricing   Revenue Management Board 5.dc.html#adm-088"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 75. 25 of 25 labels bound to a contract property; 38 of 55 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formTransitionDynamicPricingStrategy",
    "component": "modal",
    "trigger": "Transition dynamic pricing strategy",
    "body": "**Collects what `transitionDynamicPricingStrategy` sends before it is called.** Required: `action`. Optional: `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Transition dynamic pricing strategy",
     "operation": "transitionDynamicPricingStrategy"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "action",
      "reason"
     ]
    },
    "provenance": "contract catalogue.yaml POST /dynamic-pricing-strategies/{strategyId}/lifecycle"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "strategyId",
     "from": "navigation",
     "optional": true
    }
   ]
  },
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
     "operation": "setDynamicPricingStrategy",
     "carries": [
      "strategyId"
     ]
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Administrators can create reusable dynamic-pricing strategies linked to governed commercial base prices and clearly defined product/event scopes.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure; Configure whether a strategy) and no display directory — it is settings, not a population",
  "purpose": "Create the master dynamic-pricing strategy and define what commercial objects it controls.",
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
      },
      {
       "kind": "secondaryButton",
       "label": "Transition dynamic pricing strategy",
       "operation": "transitionDynamicPricingStrategy",
       "permission": "PRICE_CONFIGURE",
       "notes": "**The strategy's status moves, as calls** (29 September, writers pass).",
       "provenance": "contract catalogue.yaml POST /dynamic-pricing-strategies/{strategyId}/lifecycle"
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
    "trigger": "onAction"
   },
   {
    "operationId": "transitionDynamicPricingStrategy",
    "contract": "catalogue",
    "purpose": "Activate, pause, resume or retire a dynamic pricing strategy",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-089",
   "workshopBoard": "wireframes/WS99 Pricing   Revenue Management Board 5.dc.html#adm-089"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 76. 0 of 0 labels bound to a contract property; 22 of 45 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formTransitionDynamicPricingStrategy",
    "component": "modal",
    "trigger": "Transition dynamic pricing strategy",
    "body": "**Collects what `transitionDynamicPricingStrategy` sends before it is called.** Required: `action`. Optional: `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Transition dynamic pricing strategy",
     "operation": "transitionDynamicPricingStrategy"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "action",
      "reason"
     ]
    },
    "provenance": "contract catalogue.yaml POST /dynamic-pricing-strategies/{strategyId}/lifecycle"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "strategyId",
     "from": "navigation",
     "optional": true
    }
   ]
  },
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
     "operation": "setDemandOccupancyAvailability",
     "carries": [
      "strategyId"
     ]
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
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-090",
   "workshopBoard": "wireframes/WS99 Pricing   Revenue Management Board 5.dc.html#adm-090"
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
     "operation": "setBookingVelocityTime",
     "carries": [
      "strategyId"
     ]
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Dynamic pricing can respond to both booking pace and remaining selling time rather than relying solely on current occupancy.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Control price movement based on how quickly inventory is selling and how much time remains before the event or visit date. This is critical because occupancy alone is insufficient for effective revenue management.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 7 actions on this screen and the screen declares 1 operation.** Unserved: Sales per Hour, Sales per Day, Sales per Week, Current Booking Pace, Expected Booking Pace, Historical Booking Curve, Remaining Inventory. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
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
      },
      {
       "kind": "secondaryButton",
       "label": "Remaining Inventory",
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
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-091",
   "workshopBoard": "wireframes/WS99 Pricing   Revenue Management Board 5.dc.html#adm-091"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 80. 0 of 0 labels bound to a contract property; 7 of 41 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
     "operation": "listSeasonalCalendarDay",
     "carries": [
      "strategyId"
     ]
    }
   ]
  },
  "density": "compact",
  "purposeNote": "performances, and timeslots without creating conflicting temporal rules.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision Rendered on the calendar template (M17-03, 29 September).",
  "purpose": "Configure dynamic pricing behavior according to temporal commercial patterns.",
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
   "template": "calendar",
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
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save demand signal configuration",
       "operation": "setDemandSignalConfiguration",
       "permission": "PRICE_CONFIGURE",
       "notes": "**The person's half of `catalogue.demand_signal`** (29 September, writers pass).",
       "provenance": "contract catalogue.yaml PUT /demand-signals/{signalId}"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "selectField",
       "label": "View: day, week or month",
       "notes": "**Every calendar has day, week and month views, and the day view is broken into hours from the venue's day start hour** (17 September minutes, M17-03). Built on the shared calendar view (`calendarView`, to be added to the component library); until then a timeline per view.",
       "provenance": "29 September pass (P29 group A)"
      },
      {
       "kind": "multiSelect",
       "label": "Category",
       "notes": "**Filtered by category, so a team sees only what is theirs** (M17-03).",
       "provenance": "29 September pass (P29 group A)"
      },
      {
       "kind": "calendarView",
       "label": "Calendar",
       "operation": "listSeasonalCalendarDay",
       "notes": "Entries of the view in force, placed by date and hour.",
       "provenance": "29 September pass (P29 group A)"
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
   },
   {
    "operationId": "setDemandSignalConfiguration",
    "contract": "catalogue",
    "purpose": "Enter a calendar signal or configure how a demand signal is used",
    "trigger": "onAction",
    "invalidates": [
     "listSeasonalCalendarDay"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "SeasonalCalendarDayTimeslotDynamicRulesView.season",
    "SeasonalCalendarDayTimeslotDynamicRulesView.month",
    "SeasonalCalendarDayTimeslotDynamicRulesView.week",
    "SeasonalCalendarDayTimeslotDynamicRulesView.dateRange",
    "SeasonalCalendarDayTimeslotDynamicRulesView.dimension"
   ],
   "params": [
    {
     "name": "signalId",
     "from": "navigation",
     "optional": true
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-092",
   "workshopBoard": "wireframes/WS99 Pricing   Revenue Management Board 5.dc.html#adm-092"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 81. 0 of 0 labels bound to a contract property; 0 of 33 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formSetDemandSignalConfiguration",
    "component": "modal",
    "trigger": "Save demand signal configuration",
    "body": "**Collects what `setDemandSignalConfiguration` sends before it is called.** Required: `id`, `scopePath`, `signalKind`, `source`. Optional: `signalType`, `name`, `venueId`, `productId`, `geography`, `marketCode`, `periodStart`, `periodEnd`, `currentValue`, `unit`, `reading`, `configuration` and 11 more. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "DemandSignal",
    "confirm": {
     "label": "Save demand signal configuration",
     "operation": "setDemandSignalConfiguration"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "scopePath",
      "signalKind",
      "source",
      "signalType",
      "name",
      "venueId",
      "productId",
      "geography",
      "marketCode",
      "periodStart",
      "periodEnd",
      "currentValue",
      "unit",
      "reading",
      "configuration",
      "weight",
      "reliability"
     ]
    },
    "provenance": "contract catalogue.yaml PUT /demand-signals/{signalId}"
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
     "operation": "listChannelCustomerSegment",
     "carries": [
      "strategyId"
     ]
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Dynamic pricing can vary appropriately by channel, customer segment, and location without violating protected commercial agreements.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow dynamic-pricing behavior to differ according to commercial context.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 3 actions on this screen and the screen declares 1 operation.** Unserved: POS, Call Center, API. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 83 §Support"
   },
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
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "POS",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 83 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Call Center",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 83 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "API",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 83 §Support"
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
    "ChannelCustomerSegmentLocationDynamicRulesView.channel"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-093",
   "workshopBoard": "wireframes/WS99 Pricing   Revenue Management Board 5.dc.html#adm-093"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 83. 0 of 0 labels bound to a contract property; 3 of 38 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
     "operation": "listDynamicPriceBand",
     "carries": [
      "strategyId"
     ]
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Dynamic prices move through controlled commercial price bands or adjustment ranges rather than generating arbitrary uncontrolled selling prices.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Define the controlled monetary steps through which prices can move. This is preferable to allowing unrestricted price generation for many products.",
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
      },
      {
       "kind": "secondaryButton",
       "label": "Continuous Range where permitted",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 84 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Save price ladder matrix",
       "operation": "setPriceLadderMatrix",
       "permission": "PRICE_CONFIGURE",
       "notes": "**The bands a strategy's price moves between, and how fast** (29 September, writers pass).",
       "provenance": "contract catalogue.yaml PUT /dynamic-pricing-strategies/{strategyId}/price-ladder"
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
   },
   {
    "operationId": "setPriceLadderMatrix",
    "contract": "catalogue",
    "purpose": "Set a strategy's price ladder",
    "trigger": "onAction",
    "invalidates": [
     "listDynamicPriceBand"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-094",
   "workshopBoard": "wireframes/WS99 Pricing   Revenue Management Board 5.dc.html#adm-094"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 84. 0 of 0 labels bound to a contract property; 8 of 40 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formSetPriceLadderMatrix",
    "component": "modal",
    "trigger": "Save price ladder matrix",
    "body": "**Collects what `setPriceLadderMatrix` sends before it is called.** Required: `id`, `scopePath`, `dynamicPricingStrategyId`, `adjustmentModel`. Optional: `basePriceSource`, `bands`, `baseBandCode`, `stepAmount`, `minimumPrice`, `basePrice`, `maximumPrice`, `allowUpward`, `allowDownward`, `maxIncreasePercentPerAdjustment`, `maxDecreasePercentPerAdjustment`, `maximumBandsPerMovement` and 4 more. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "PriceLadder",
    "confirm": {
     "label": "Save price ladder matrix",
     "operation": "setPriceLadderMatrix"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "scopePath",
      "dynamicPricingStrategyId",
      "adjustmentModel",
      "basePriceSource",
      "bands",
      "baseBandCode",
      "stepAmount",
      "minimumPrice",
      "basePrice",
      "maximumPrice",
      "allowUpward",
      "allowDownward",
      "maxIncreasePercentPerAdjustment",
      "maxDecreasePercentPerAdjustment",
      "maximumBandsPerMovement",
      "minimumMinutesBetweenMovements",
      "cooldownMinutes"
     ]
    },
    "provenance": "contract catalogue.yaml PUT /dynamic-pricing-strategies/{strategyId}/price-ladder"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "strategyId",
     "from": "navigation",
     "optional": true
    }
   ]
  },
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
  "purposeNote": "No dynamic pricing strategy can generate a selling price outside approved financial, contractual, operational, or regulatory boundaries.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Establish the non-negotiable boundaries for every dynamic-pricing strategy.",
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
      },
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
   },
   {
    "operationId": "setDynamicPricingGuardrailPolicy",
    "contract": "catalogue",
    "purpose": "Set the guardrails and automation level of dynamic pricing at one scope",
    "trigger": "onAction",
    "invalidates": [
     "listDynamicPricingGuardrail"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-095",
   "workshopBoard": "wireframes/WS99 Pricing   Revenue Management Board 5.dc.html#adm-095"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 86. 0 of 0 labels bound to a contract property; 18 of 32 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "purposeNote": "authorized boundaries into the central governance process.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure independently by; Configure; Capture) and no display directory — it is settings, not a population",
  "purpose": "Define how much authority the pricing engine has to act on a calculated dynamic price. This is different from Board 4's approval workflow. Board 5 determines whether the engine may act automatically. Board 4 handles governance when formal approval is required.",
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
   },
   {
    "operationId": "setDynamicPricingGuardrailPolicy",
    "contract": "catalogue",
    "purpose": "Set the guardrails and automation level of dynamic pricing at one scope",
    "trigger": "onAction",
    "invalidates": [
     "listDynamicPricingAutomation"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-096",
   "workshopBoard": "wireframes/WS99 Pricing   Revenue Management Board 5.dc.html#adm-096"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 87. 0 of 0 labels bound to a contract property; 15 of 41 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
   "notes": "**Reached from ADM-088, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-088",
     "trigger": "Dynamic Pricing Strategy Command Center",
     "provenance": "derived — ADM-088 declares entryState.params strategyId and ADM-097 holds none of them, so the edge carries nothing and ADM-088 opens cold"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "For any configured commercial scenario, TICVAI can deterministically calculate, test, and explain the final dynamic price before the strategy is activated. Board 5 — Final Screen Register # Backend Screen Primary Responsibility 10.5. Dynamic Pricing Strategy Command Center Strategy portfolio 1 10.5. Strategy master",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Identify; Show) and no metric row",
  "purpose": "Determine the final dynamic price when multiple strategies and rules are simultaneously applicable. This is the final and most important control screen of Board 5.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Contradictory rules",
       "bindsTo": "RulePriorityConflictResolutionDynamicPricingTestConsSummary.contradictoryRules",
       "operation": "listRulePriorityConflict",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Same priority",
       "bindsTo": "RulePriorityConflictResolutionDynamicPricingTestConsSummary.samePriority",
       "operation": "listRulePriorityConflict",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Impossible condition",
       "bindsTo": "RulePriorityConflictResolutionDynamicPricingTestConsSummary.impossibleCondition",
       "operation": "listRulePriorityConflict",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Overlapping strategy",
       "bindsTo": "RulePriorityConflictResolutionDynamicPricingTestConsSummary.overlappingStrategy",
       "operation": "listRulePriorityConflict",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Circular dependency",
       "bindsTo": "RulePriorityConflictResolutionDynamicPricingTestConsSummary.circularDependency",
       "operation": "listRulePriorityConflict",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Missing fallback",
       "bindsTo": "RulePriorityConflictResolutionDynamicPricingTestConsSummary.missingFallback",
       "operation": "listRulePriorityConflict",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Guardrail conflict",
       "bindsTo": "RulePriorityConflictResolutionDynamicPricingTestConsSummary.guardrailConflict",
       "operation": "listRulePriorityConflict",
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
       "label": "Every rule priority conflict",
       "columns": [
        "RulePriorityConflictResolutionDynamicPricingTestConsView.calculationPath"
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
        "RulePriorityConflictResolutionDynamicPricingTestConsView.calculationPath"
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
       "operation": "setRulePriorityConflict",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 89 §Support"
      },
      {
       "kind": "destructiveButton",
       "label": "Stop Processing",
       "operation": "setRulePriorityConflict",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 89 §Support"
      },
      {
       "kind": "primaryButton",
       "label": "Run Test",
       "operation": "setRulePriorityConflict",
       "provenance": "contract catalogue.yaml PUT /rule-priority-conflict (decided 29 September, readiness close-out)"
      },
      {
       "kind": "secondaryButton",
       "label": "Save Case",
       "operation": "setRulePriorityConflict",
       "provenance": "contract catalogue.yaml PUT /rule-priority-conflict (decided 29 September, readiness close-out)"
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
   },
   {
    "operationId": "setRulePriorityConflict",
    "contract": "catalogue",
    "purpose": "Reorder, validate, test or save the pricing rule priority",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "preloaded": [
    "RulePriorityConflictResolutionDynamicPricingTestConsSummary.contradictoryRules",
    "RulePriorityConflictResolutionDynamicPricingTestConsSummary.samePriority",
    "RulePriorityConflictResolutionDynamicPricingTestConsSummary.impossibleCondition",
    "RulePriorityConflictResolutionDynamicPricingTestConsSummary.overlappingStrategy",
    "RulePriorityConflictResolutionDynamicPricingTestConsSummary.circularDependency",
    "RulePriorityConflictResolutionDynamicPricingTestConsSummary.missingFallback"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-097",
   "workshopBoard": "wireframes/WS99 Pricing   Revenue Management Board 5.dc.html#adm-097"
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
  "parameters": [
   {
    "name": "dimension",
    "in": "query",
    "required": false
   },
   {
    "name": "strategyId",
    "in": "query",
    "required": false
   },
   {
    "name": "channel",
    "in": "query",
    "required": false
   },
   {
    "name": "customerSegment",
    "in": "query",
    "required": false
   },
   {
    "name": "locationLevel",
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
 "listDynamicPriceBand": {
  "method": "GET",
  "path": "/dynamic-price-band",
  "contract": "catalogue",
  "summary": "Dynamic Price Bands, Ladders & Adjustment Matrix",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "strategyId",
    "in": "query",
    "required": false
   },
   {
    "name": "adjustmentModel",
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
 "listDynamicPricingAutomation": {
  "method": "GET",
  "path": "/dynamic-pricing-automation",
  "contract": "catalogue",
  "summary": "Dynamic Pricing Automation Policy & Control",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "scopeLevel",
    "in": "query",
    "required": false
   },
   {
    "name": "automationMode",
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
 "listDynamicPricingGuardrail": {
  "method": "GET",
  "path": "/dynamic-pricing-guardrail",
  "contract": "catalogue",
  "summary": "Dynamic Pricing Guardrails & Commercial Protection",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "scopeLevel",
    "in": "query",
    "required": false
   },
   {
    "name": "scopeId",
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
 "listDynamicPricingStrategy": {
  "method": "GET",
  "path": "/dynamic-pricing-strategy",
  "contract": "catalogue",
  "summary": "Dynamic Pricing Strategy Command Center",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "strategyType",
    "in": "query",
    "required": false
   },
   {
    "name": "status",
    "in": "query",
    "required": false
   },
   {
    "name": "automationMode",
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
 "listRulePriorityConflict": {
  "method": "GET",
  "path": "/rule-priority-conflict",
  "contract": "catalogue",
  "summary": "Rule Priority, Conflict Resolution & Dynamic Pricing Test Console",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "caseType",
    "in": "query",
    "required": false
   },
   {
    "name": "conflictCode",
    "in": "query",
    "required": false
   },
   {
    "name": "strategyId",
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
 "listSeasonalCalendarDay": {
  "method": "GET",
  "path": "/seasonal-calendar-day",
  "contract": "catalogue",
  "summary": "Seasonal, Calendar, Day & Timeslot Dynamic Rules",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "dimension",
    "in": "query",
    "required": false
   },
   {
    "name": "strategyId",
    "in": "query",
    "required": false
   },
   {
    "name": "season",
    "in": "query",
    "required": false
   },
   {
    "name": "from",
    "in": "query",
    "required": false
   },
   {
    "name": "to",
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
 "setBookingVelocityTime": {
  "method": "PUT",
  "path": "/booking-velocity-time",
  "contract": "catalogue",
  "summary": "Booking Velocity & Time-to-Event Rule Builder",
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "DemandOccupancyAvailabilityRuleBuilderInput",
  "responds": "DemandOccupancyAvailabilityRuleBuilderView"
 },
 "setDemandSignalConfiguration": {
  "method": "PUT",
  "path": "/demand-signals/{signalId}",
  "contract": "catalogue",
  "summary": "Enter a calendar signal or configure how a demand signal is used",
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
  "requestBody": "DemandSignal",
  "responds": "DemandSignal"
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
 "setDynamicPricingStrategy": {
  "method": "PUT",
  "path": "/dynamic-pricing-strategy-2",
  "contract": "catalogue",
  "summary": "Dynamic Pricing Strategy Builder",
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
  "requestBody": "DynamicPricingStrategyBuilderInput",
  "responds": "DynamicPricingStrategyBuilderView"
 },
 "setPriceLadderMatrix": {
  "method": "PUT",
  "path": "/dynamic-pricing-strategies/{strategyId}/price-ladder",
  "contract": "catalogue",
  "summary": "Set a strategy's price ladder",
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
  "requestBody": "PriceLadder",
  "responds": "PriceLadder"
 },
 "setRulePriorityConflict": {
  "method": "PUT",
  "path": "/rule-priority-conflict",
  "contract": "catalogue",
  "summary": "Reorder, validate, test or save the pricing rule priority",
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
  "requestBody": "RulePriorityConflictInput",
  "responds": "RulePriorityConflictView"
 },
 "transitionDynamicPricingStrategy": {
  "method": "POST",
  "path": "/dynamic-pricing-strategies/{strategyId}/lifecycle",
  "contract": "catalogue",
  "summary": "Activate, pause, resume or retire a dynamic pricing strategy",
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
  "requestBody": null,
  "responds": "DynamicPricingStrategy"
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
   "ruleId": {
    "type": "string",
    "description": "Rule ID; empty on create",
    "nullable": true
   },
   "strategyId": {
    "type": "string",
    "description": "Strategy the rule belongs to"
   },
   "ruleName": {
    "type": "string",
    "description": "Rule name"
   },
   "ruleKind": {
    "type": "string",
    "enum": [
     "bookingVelocity",
     "earlyBird",
     "lastMinute",
     "combined",
     "decayEscalation"
    ],
    "description": "Rule family (pack pp.80-81)"
   },
   "expectedPaceSource": {
    "type": "string",
    "enum": [
     "historicalBookingCurve",
     "configuredTarget"
    ],
    "description": "What pace variance is measured against; defaults to configuredTarget until a historical curve exists (decided 29 September, readiness close-out)"
   },
   "expectedSalesPerDay": {
    "type": "integer",
    "description": "Expected sales per day when expectedPaceSource is configuredTarget",
    "nullable": true
   },
   "conditions": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "metric": {
       "type": "string",
       "enum": [
        "salesPerHour",
        "salesPerDay",
        "salesPerWeek",
        "currentBookingPace",
        "paceVariancePercent",
        "remainingInventory",
        "daysToEvent",
        "occupancyPercent"
       ],
       "description": "Input evaluated (pack p.80; daysToEvent 0 = same day)"
      },
      "operator": {
       "type": "string",
       "enum": [
        "lt",
        "lte",
        "gt",
        "gte",
        "eq",
        "between"
       ],
       "description": "Comparison"
      },
      "value": {
       "type": "number",
       "description": "Threshold value (percent for percentages, count for counts, days for time-to-event)"
      },
      "valueTo": {
       "type": "number",
       "description": "Upper value when operator is between",
       "nullable": true
      }
     },
     "description": "One condition; persisted as a PricingDynamicPriceCondition"
    },
    "description": "Conditions (all must hold unless conditionLogic is any)"
   },
   "conditionLogic": {
    "type": "string",
    "enum": [
     "all",
     "any"
    ],
    "description": "How conditions combine; defaults to all (decided 29 September, readiness close-out)"
   },
   "timeToEventSchedule": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "daysBefore": {
       "type": "integer",
       "description": "Days before the event/visit (T-180 ... T-1; 0 = same day); custom intervals allowed"
      },
      "action": {
       "type": "object",
       "properties": {
        "actionType": {
         "type": "string",
         "enum": [
          "percentAdjustment",
          "fixedAmountAdjustment",
          "moveToBand",
          "returnToBase"
         ],
         "description": "What the rule does to the current price"
        },
        "percent": {
         "type": "number",
         "description": "Adjustment in percent (negative lowers the price) when actionType is percentAdjustment",
         "nullable": true
        },
        "amount": {
         "allOf": [
          {
           "$ref": "../shared/common.yaml#/components/schemas/Money"
          }
         ],
         "description": "Signed amount when actionType is fixedAmountAdjustment",
         "nullable": true
        },
        "bandCode": {
         "type": "string",
         "description": "Target band on the strategy's price ladder (listDynamicPriceBand) when actionType is moveToBand",
         "nullable": true
        }
       },
       "description": "The price action; the result still passes through the price ladder and the guardrails"
      }
     },
     "description": "One time-to-event step, e.g. T-90 -> -15%"
    },
    "description": "Time-to-event steps (early-bird, decay/escalation); empty for condition-only rules"
   },
   "action": {
    "type": "object",
    "properties": {
     "actionType": {
      "type": "string",
      "enum": [
       "percentAdjustment",
       "fixedAmountAdjustment",
       "moveToBand",
       "returnToBase"
      ],
      "description": "What the rule does to the current price"
     },
     "percent": {
      "type": "number",
      "description": "Adjustment in percent (negative lowers the price) when actionType is percentAdjustment",
      "nullable": true
     },
     "amount": {
      "allOf": [
       {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      ],
      "description": "Signed amount when actionType is fixedAmountAdjustment",
      "nullable": true
     },
     "bandCode": {
      "type": "string",
      "description": "Target band on the strategy's price ladder (listDynamicPriceBand) when actionType is moveToBand",
      "nullable": true
     }
    },
    "description": "Action when the conditions hold (for condition rules)",
    "nullable": true
   },
   "priority": {
    "type": "integer",
    "description": "Priority within the strategy; lower wins"
   },
   "enabled": {
    "type": "boolean",
    "description": "Enabled"
   }
  }
 },
 "BookingVelocityTimeToEventRuleBuilderView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Booking Velocity & Time-to-Event Rule Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "ruleId": {
    "type": "string",
    "description": "Rule ID; empty on create",
    "nullable": true
   },
   "strategyId": {
    "type": "string",
    "description": "Strategy the rule belongs to"
   },
   "ruleName": {
    "type": "string",
    "description": "Rule name"
   },
   "ruleKind": {
    "type": "string",
    "enum": [
     "bookingVelocity",
     "earlyBird",
     "lastMinute",
     "combined",
     "decayEscalation"
    ],
    "description": "Rule family (pack pp.80-81)"
   },
   "expectedPaceSource": {
    "type": "string",
    "enum": [
     "historicalBookingCurve",
     "configuredTarget"
    ],
    "description": "What pace variance is measured against; defaults to configuredTarget until a historical curve exists (decided 29 September, readiness close-out)"
   },
   "expectedSalesPerDay": {
    "type": "integer",
    "description": "Expected sales per day when expectedPaceSource is configuredTarget",
    "nullable": true
   },
   "conditions": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "metric": {
       "type": "string",
       "enum": [
        "salesPerHour",
        "salesPerDay",
        "salesPerWeek",
        "currentBookingPace",
        "paceVariancePercent",
        "remainingInventory",
        "daysToEvent",
        "occupancyPercent"
       ],
       "description": "Input evaluated (pack p.80; daysToEvent 0 = same day)"
      },
      "operator": {
       "type": "string",
       "enum": [
        "lt",
        "lte",
        "gt",
        "gte",
        "eq",
        "between"
       ],
       "description": "Comparison"
      },
      "value": {
       "type": "number",
       "description": "Threshold value (percent for percentages, count for counts, days for time-to-event)"
      },
      "valueTo": {
       "type": "number",
       "description": "Upper value when operator is between",
       "nullable": true
      }
     },
     "description": "One condition; persisted as a PricingDynamicPriceCondition"
    },
    "description": "Conditions (all must hold unless conditionLogic is any)"
   },
   "conditionLogic": {
    "type": "string",
    "enum": [
     "all",
     "any"
    ],
    "description": "How conditions combine; defaults to all (decided 29 September, readiness close-out)"
   },
   "timeToEventSchedule": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "daysBefore": {
       "type": "integer",
       "description": "Days before the event/visit (T-180 ... T-1; 0 = same day); custom intervals allowed"
      },
      "action": {
       "type": "object",
       "properties": {
        "actionType": {
         "type": "string",
         "enum": [
          "percentAdjustment",
          "fixedAmountAdjustment",
          "moveToBand",
          "returnToBase"
         ],
         "description": "What the rule does to the current price"
        },
        "percent": {
         "type": "number",
         "description": "Adjustment in percent (negative lowers the price) when actionType is percentAdjustment",
         "nullable": true
        },
        "amount": {
         "allOf": [
          {
           "$ref": "../shared/common.yaml#/components/schemas/Money"
          }
         ],
         "description": "Signed amount when actionType is fixedAmountAdjustment",
         "nullable": true
        },
        "bandCode": {
         "type": "string",
         "description": "Target band on the strategy's price ladder (listDynamicPriceBand) when actionType is moveToBand",
         "nullable": true
        }
       },
       "description": "The price action; the result still passes through the price ladder and the guardrails"
      }
     },
     "description": "One time-to-event step, e.g. T-90 -> -15%"
    },
    "description": "Time-to-event steps (early-bird, decay/escalation); empty for condition-only rules"
   },
   "action": {
    "type": "object",
    "properties": {
     "actionType": {
      "type": "string",
      "enum": [
       "percentAdjustment",
       "fixedAmountAdjustment",
       "moveToBand",
       "returnToBase"
      ],
      "description": "What the rule does to the current price"
     },
     "percent": {
      "type": "number",
      "description": "Adjustment in percent (negative lowers the price) when actionType is percentAdjustment",
      "nullable": true
     },
     "amount": {
      "allOf": [
       {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      ],
      "description": "Signed amount when actionType is fixedAmountAdjustment",
      "nullable": true
     },
     "bandCode": {
      "type": "string",
      "description": "Target band on the strategy's price ladder (listDynamicPriceBand) when actionType is moveToBand",
      "nullable": true
     }
    },
    "description": "Action when the conditions hold (for condition rules)",
    "nullable": true
   },
   "priority": {
    "type": "integer",
    "description": "Priority within the strategy; lower wins"
   },
   "enabled": {
    "type": "boolean",
    "description": "Enabled"
   }
  }
 },
 "ChannelCustomerSegmentLocationDynamicRulesView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Channel, Customer Segment & Location Dynamic Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "ruleId": {
    "type": "string",
    "description": "Rule ID"
   },
   "strategyId": {
    "type": "string",
    "description": "Strategy the rule belongs to; empty for a tenant-wide rule",
    "nullable": true
   },
   "dimension": {
    "type": "string",
    "enum": [
     "channel",
     "customerSegment",
     "location"
    ],
    "description": "Rule dimension"
   },
   "channel": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/SalesChannel"
     }
    ],
    "nullable": true,
    "description": "Channel (B2C = guestWeb, Mobile App = guestApp, Reseller = partner)"
   },
   "customerSegment": {
    "type": "string",
    "enum": [
     "standardCustomer",
     "member",
     "loyaltyTier",
     "resident",
     "vip",
     "corporate",
     "group",
     "b2b",
     "customSegment"
    ],
    "description": "Customer segment (pack p.83)",
    "nullable": true
   },
   "segmentRef": {
    "type": "string",
    "description": "Loyalty tier or custom segment ID",
    "nullable": true
   },
   "locationLevel": {
    "type": "string",
    "enum": [
     "country",
     "market",
     "venue",
     "attraction",
     "zone",
     "eventLocation"
    ],
    "description": "Location level (pack pp.83-84)",
    "nullable": true
   },
   "locationId": {
    "type": "string",
    "description": "Country, market, venue, attraction, zone or event location ID",
    "nullable": true
   },
   "dynamicPricingEnabled": {
    "type": "boolean",
    "description": "Whether dynamic pricing applies in this context"
   },
   "rangeMinPercent": {
    "type": "number",
    "description": "Lowest adjustment from base in percent",
    "nullable": true
   },
   "rangeMaxPercent": {
    "type": "number",
    "description": "Highest adjustment from base in percent (maximum uplift)",
    "nullable": true
   },
   "protected": {
    "type": "boolean",
    "description": "Protected segment: always receives its protected rate and is excluded from dynamic adjustment"
   }
  }
 },
 "DemandOccupancyAvailabilityRuleBuilderInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Demand, Occupancy & Availability Rule Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "ruleId": {
    "type": "string",
    "description": "Rule ID; empty on create",
    "nullable": true
   },
   "strategyId": {
    "type": "string",
    "description": "Strategy the rule belongs to"
   },
   "ruleName": {
    "type": "string",
    "description": "Rule name"
   },
   "ruleKind": {
    "type": "string",
    "enum": [
     "occupancy",
     "inventory",
     "availability",
     "demand"
    ],
    "description": "Rule family (pack p.78-79)"
   },
   "inputMetric": {
    "type": "string",
    "enum": [
     "ticketsSold",
     "currentDemand",
     "occupancyPercent",
     "remainingCapacity",
     "remainingInventory",
     "availableSeats",
     "capacityUtilization",
     "salesPace"
    ],
    "description": "Supported Input evaluated (pack p.78)"
   },
   "tiers": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "fromValue": {
       "type": "number",
       "description": "From (inclusive)"
      },
      "toValue": {
       "type": "number",
       "description": "To (inclusive); empty for no upper bound",
       "nullable": true
      },
      "action": {
       "type": "object",
       "properties": {
        "actionType": {
         "type": "string",
         "enum": [
          "percentAdjustment",
          "fixedAmountAdjustment",
          "moveToBand",
          "returnToBase"
         ],
         "description": "What the rule does to the current price"
        },
        "percent": {
         "type": "number",
         "description": "Adjustment in percent (negative lowers the price) when actionType is percentAdjustment",
         "nullable": true
        },
        "amount": {
         "allOf": [
          {
           "$ref": "../shared/common.yaml#/components/schemas/Money"
          }
         ],
         "description": "Signed amount when actionType is fixedAmountAdjustment",
         "nullable": true
        },
        "bandCode": {
         "type": "string",
         "description": "Target band on the strategy's price ladder (listDynamicPriceBand) when actionType is moveToBand",
         "nullable": true
        }
       },
       "description": "The price action; the result still passes through the price ladder and the guardrails"
      }
     },
     "description": "One step of the matrix, e.g. occupancy 81-90% -> +10%"
    },
    "description": "Threshold matrix; tiers must not overlap"
   },
   "demandIndexDefinition": {
    "type": "string",
    "description": "Required when inputMetric is currentDemand: how the demand index is calculated (the pack requires it to be explicitly configured and documented)",
    "nullable": true
   },
   "exitThresholdOffset": {
    "type": "number",
    "description": "Exit threshold: how far the metric must fall back below a tier's entry before the price reverses; defaults to 2 (points or units of the metric) (decided 29 September, readiness close-out)"
   },
   "minimumDurationMinutes": {
    "type": "integer",
    "description": "Minimum duration a threshold must hold before the price moves; defaults to 15 (decided 29 September, readiness close-out)"
   },
   "cooldownMinutes": {
    "type": "integer",
    "description": "Cooldown after a movement before the next; defaults to 60 (decided 29 September, readiness close-out)"
   },
   "priority": {
    "type": "integer",
    "description": "Priority within the strategy; lower wins"
   },
   "enabled": {
    "type": "boolean",
    "description": "Enabled"
   }
  }
 },
 "DemandOccupancyAvailabilityRuleBuilderView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Demand, Occupancy & Availability Rule Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "ruleId": {
    "type": "string",
    "description": "Rule ID; empty on create",
    "nullable": true
   },
   "strategyId": {
    "type": "string",
    "description": "Strategy the rule belongs to"
   },
   "ruleName": {
    "type": "string",
    "description": "Rule name"
   },
   "ruleKind": {
    "type": "string",
    "enum": [
     "occupancy",
     "inventory",
     "availability",
     "demand"
    ],
    "description": "Rule family (pack p.78-79)"
   },
   "inputMetric": {
    "type": "string",
    "enum": [
     "ticketsSold",
     "currentDemand",
     "occupancyPercent",
     "remainingCapacity",
     "remainingInventory",
     "availableSeats",
     "capacityUtilization",
     "salesPace"
    ],
    "description": "Supported Input evaluated (pack p.78)"
   },
   "tiers": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "fromValue": {
       "type": "number",
       "description": "From (inclusive)"
      },
      "toValue": {
       "type": "number",
       "description": "To (inclusive); empty for no upper bound",
       "nullable": true
      },
      "action": {
       "type": "object",
       "properties": {
        "actionType": {
         "type": "string",
         "enum": [
          "percentAdjustment",
          "fixedAmountAdjustment",
          "moveToBand",
          "returnToBase"
         ],
         "description": "What the rule does to the current price"
        },
        "percent": {
         "type": "number",
         "description": "Adjustment in percent (negative lowers the price) when actionType is percentAdjustment",
         "nullable": true
        },
        "amount": {
         "allOf": [
          {
           "$ref": "../shared/common.yaml#/components/schemas/Money"
          }
         ],
         "description": "Signed amount when actionType is fixedAmountAdjustment",
         "nullable": true
        },
        "bandCode": {
         "type": "string",
         "description": "Target band on the strategy's price ladder (listDynamicPriceBand) when actionType is moveToBand",
         "nullable": true
        }
       },
       "description": "The price action; the result still passes through the price ladder and the guardrails"
      }
     },
     "description": "One step of the matrix, e.g. occupancy 81-90% -> +10%"
    },
    "description": "Threshold matrix; tiers must not overlap"
   },
   "demandIndexDefinition": {
    "type": "string",
    "description": "Required when inputMetric is currentDemand: how the demand index is calculated (the pack requires it to be explicitly configured and documented)",
    "nullable": true
   },
   "exitThresholdOffset": {
    "type": "number",
    "description": "Exit threshold: how far the metric must fall back below a tier's entry before the price reverses; defaults to 2 (points or units of the metric) (decided 29 September, readiness close-out)"
   },
   "minimumDurationMinutes": {
    "type": "integer",
    "description": "Minimum duration a threshold must hold before the price moves; defaults to 15 (decided 29 September, readiness close-out)"
   },
   "cooldownMinutes": {
    "type": "integer",
    "description": "Cooldown after a movement before the next; defaults to 60 (decided 29 September, readiness close-out)"
   },
   "priority": {
    "type": "integer",
    "description": "Priority within the strategy; lower wins"
   },
   "enabled": {
    "type": "boolean",
    "description": "Enabled"
   }
  }
 },
 "DemandSignal": {
  "type": "object",
  "x-ticvai-persistence": "catalogue.demand_signal",
  "description": "**An external or calendar signal that moves demand** (29 September, data model DM3). Merges weather (ADM-101), nearby events (ADM-102), competitor prices (ADM-103), tourism, holiday and market signals (ADM-104) and the tenant's special calendar (Ramadan, Eid, school breaks) used by temporal rules. `signalKind` says which; the readings specific to a kind are in `reading`, and a venue's sensitivity settings in `configuration`. A signal informs forecasts and recommendations; it never sets a price.",
  "required": [
   "id",
   "scopePath",
   "signalKind",
   "source"
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
   "signalKind": {
    "type": "string",
    "enum": [
     "weather",
     "nearbyEvent",
     "competitorPrice",
     "calendar",
     "tourism",
     "transport",
     "market"
    ]
   },
   "signalType": {
    "type": "string",
    "maxLength": 60,
    "nullable": true,
    "description": "E.g. `publicHoliday`, `ramadan`, an event type, a weather condition."
   },
   "name": {
    "type": "string",
    "maxLength": 200,
    "nullable": true
   },
   "source": {
    "type": "string",
    "maxLength": 100,
    "description": "Provider, feed or `tenant` for manual entries."
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "productId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Competitor observations: the comparable TICVAI product."
   },
   "geography": {
    "type": "string",
    "maxLength": 100,
    "nullable": true
   },
   "marketCode": {
    "type": "string",
    "maxLength": 40,
    "nullable": true
   },
   "periodStart": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "periodEnd": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "currentValue": {
    "type": "number",
    "nullable": true
   },
   "unit": {
    "type": "string",
    "maxLength": 20,
    "nullable": true
   },
   "reading": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true,
    "description": "Kind-specific values: weather conditions and forecasts, event attendance and distance, competitor prices."
   },
   "configuration": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true,
    "description": "Weather: `{venueExposure, weatherSensitivity, conditionImpacts, forecastHorizon, dataFailurePolicy}`; events: `{monitoringRadiusKm}`."
   },
   "weight": {
    "type": "number",
    "nullable": true
   },
   "reliability": {
    "type": "number",
    "nullable": true,
    "minimum": 0,
    "maximum": 1
   },
   "historicalCorrelation": {
    "type": "number",
    "nullable": true
   },
   "confidence": {
    "type": "number",
    "nullable": true,
    "minimum": 0,
    "maximum": 1
   },
   "impactMinPercent": {
    "type": "number",
    "nullable": true
   },
   "impactMaxPercent": {
    "type": "number",
    "nullable": true
   },
   "refreshFrequency": {
    "type": "string",
    "enum": [
     "realTime",
     "hourly",
     "daily",
     "weekly",
     "manual",
     null
    ],
    "nullable": true
   },
   "isApproved": {
    "type": "boolean",
    "default": false,
    "description": "Competitor sources and comparability approved for use."
   },
   "isActive": {
    "type": "boolean",
    "default": true
   },
   "observedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "lastUpdatedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "createdAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "DynamicPriceBandsLaddersAdjustmentMatrixView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Dynamic Price Bands, Ladders & Adjustment Matrix displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "maximumBandsPerMovement": {
    "type": "integer",
    "description": "Maximum bands per movement; defaults to 1 (decided 29 September, readiness close-out)"
   },
   "minimumTimeBetweenMovements": {
    "type": "integer",
    "description": "Minimum minutes between movements; defaults to 60 (decided 29 September, readiness close-out)"
   },
   "reversalRules": {
    "type": "string",
    "enum": [
     "allowed",
     "afterCooldown",
     "notAllowed"
    ],
    "description": "Whether a movement may be reversed; defaults to afterCooldown (decided 29 September, readiness close-out)"
   },
   "cooldownPeriod": {
    "type": "integer",
    "description": "Cooldown in minutes after a movement; defaults to 60 (decided 29 September, readiness close-out)"
   },
   "ladderId": {
    "type": "string",
    "description": "Ladder ID"
   },
   "strategyId": {
    "type": "string",
    "description": "Strategy the ladder belongs to"
   },
   "basePriceSource": {
    "type": "string",
    "description": "Board 1 rate the ladder is built around"
   },
   "adjustmentModel": {
    "type": "string",
    "enum": [
     "fixedPriceBands",
     "percentageBands",
     "fixedAmountSteps",
     "derivedBands",
     "continuousRange"
    ],
    "description": "Adjustment Model (pack p.85)"
   },
   "bands": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "code": {
       "type": "string",
       "description": "Band code, e.g. P4"
      },
      "price": {
       "allOf": [
        {
         "$ref": "../shared/common.yaml#/components/schemas/Money"
        }
       ],
       "description": "Band price (fixed and derived bands)",
       "nullable": true
      },
      "percent": {
       "type": "number",
       "description": "Band offset from base in percent (percentage bands)",
       "nullable": true
      }
     },
     "description": "One band"
    },
    "description": "Bands, lowest first"
   },
   "baseBandCode": {
    "type": "string",
    "description": "Band holding the base price, e.g. P3"
   },
   "stepAmount": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Step for fixedAmountSteps",
    "nullable": true
   },
   "allowUpward": {
    "type": "boolean",
    "description": "Upward movement allowed"
   },
   "allowDownward": {
    "type": "boolean",
    "description": "Downward movement allowed"
   },
   "maxIncreasePercentPerAdjustment": {
    "type": "number",
    "description": "Asymmetric movement: maximum increase per adjustment in percent",
    "nullable": true
   },
   "maxDecreasePercentPerAdjustment": {
    "type": "number",
    "description": "Asymmetric movement: maximum decrease per adjustment in percent",
    "nullable": true
   },
   "allowedEndpoints": {
    "type": "array",
    "items": {
     "allOf": [
      {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      }
     ]
    },
    "description": "Psychological pricing: governed endpoints (e.g. AED 249, 259, 279) a price may land on"
   },
   "minimumPrice": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Preview: lowest price on the ladder"
   },
   "basePrice": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Preview: base price"
   },
   "maximumPrice": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Preview: highest price on the ladder"
   }
  }
 },
 "DynamicPricingAutomationPolicyControlView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Dynamic Pricing Automation Policy & Control displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "maximumAutomaticChangesDay": {
    "type": "integer",
    "description": "Maximum automatic changes per day; defaults to 4 (decided 29 September, readiness close-out)"
   },
   "minimumTimeBetweenChanges": {
    "type": "integer",
    "description": "Minimum minutes between automatic changes; defaults to 60 (decided 29 September, readiness close-out)"
   },
   "noChangeWindows": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "anchor": {
       "type": "string",
       "enum": [
        "gatesOpening",
        "eventStart",
        "clockTime"
       ],
       "description": "What the window is measured from"
      },
      "minutesBefore": {
       "type": "integer",
       "description": "Minutes before the anchor",
       "nullable": true
      },
      "minutesAfter": {
       "type": "integer",
       "description": "Minutes after the anchor",
       "nullable": true
      },
      "clockFrom": {
       "type": "string",
       "description": "HH:mm when anchor is clockTime",
       "nullable": true
      },
      "clockTo": {
       "type": "string",
       "description": "HH:mm",
       "nullable": true
      }
     },
     "description": "One window"
    },
    "description": "No-Change Windows, e.g. 30 minutes before gates open"
   },
   "policyId": {
    "type": "string",
    "description": "Policy ID"
   },
   "scopeLevel": {
    "type": "string",
    "enum": [
     "product",
     "event",
     "venue",
     "strategy",
     "channel",
     "market"
    ],
    "description": "Automation Scope (pack p.88)"
   },
   "scopeId": {
    "type": "string",
    "description": "ID of the product, event, venue, strategy, channel or market"
   },
   "automationMode": {
    "type": "string",
    "enum": [
     "monitor",
     "recommend",
     "prepareChange",
     "autoExecuteWithinGuardrails"
    ],
    "description": "Automation mode; defaults to recommend (decided 29 September, readiness close-out)"
   },
   "authorityTiers": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "maxAdjustmentPercent": {
       "type": "number",
       "description": "Applies to adjustments up to this percent (absolute)",
       "nullable": true
      },
      "action": {
       "type": "string",
       "enum": [
        "autoExecute",
        "autoExecuteIfConfident",
        "revenueManager",
        "commercialDirector",
        "board4Governance"
       ],
       "description": "Who acts"
      },
      "confidenceThreshold": {
       "type": "number",
       "description": "Confidence percent required for autoExecuteIfConfident",
       "nullable": true
      }
     },
     "description": "One tier"
    },
    "description": "Authority policy, smallest adjustment first; empty means every change needs a Revenue Manager (decided 29 September, readiness close-out)"
   },
   "safeFailureBehavior": {
    "type": "string",
    "enum": [
     "holdLastPrice",
     "returnToBase",
     "freeze",
     "requestReview"
    ],
    "description": "Safe Failure when inputs are unavailable; defaults to holdLastPrice (decided 29 September, readiness close-out)"
   },
   "activeOverride": {
    "type": "object",
    "properties": {
     "user": {
      "type": "string",
      "description": "User"
     },
     "reason": {
      "type": "string",
      "description": "Reason"
     },
     "overridePrice": {
      "allOf": [
       {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      ],
      "description": "Override price"
     },
     "start": {
      "type": "string",
      "format": "date-time",
      "description": "Start"
     },
     "expiry": {
      "type": "string",
      "format": "date-time",
      "description": "Expiry"
     },
     "returnBehavior": {
      "type": "string",
      "enum": [
       "resumeEngine",
       "returnToBase",
       "holdOverridePrice"
      ],
      "description": "What happens at expiry"
     }
    },
    "description": "Manual override in force, if any",
    "nullable": true
   }
  }
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
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Minimum contribution margin per unit; the price never falls below cost plus this margin",
    "nullable": true
   },
   "maximumUplift": {
    "type": "number",
    "description": "Maximum uplift from base in percent"
   },
   "maximumReduction": {
    "type": "number",
    "description": "Maximum reduction from base in percent"
   },
   "maximumSingleChange": {
    "type": "number",
    "description": "Maximum single change in percent"
   },
   "maximumDailyChange": {
    "type": "number",
    "description": "Maximum change within 24 hours in percent"
   },
   "maximumWeeklyChange": {
    "type": "number",
    "description": "Maximum change within 7 days in percent",
    "nullable": true
   },
   "minimumChangeInterval": {
    "type": "integer",
    "description": "Minimum minutes between changes"
   },
   "maximumChangesPerDay": {
    "type": "integer",
    "description": "Maximum changes per day"
   },
   "minimumInventory": {
    "type": "integer",
    "description": "Below this remaining inventory no downward adjustment is made (decided 29 September, readiness close-out)",
    "nullable": true
   },
   "maximumOccupancyTrigger": {
    "type": "number",
    "description": "Occupancy percent above which no further uplift is triggered (decided 29 September, readiness close-out)",
    "nullable": true
   },
   "guardrailId": {
    "type": "string",
    "description": "Guardrail set ID"
   },
   "scopeLevel": {
    "type": "string",
    "enum": [
     "global",
     "strategy",
     "venue",
     "product",
     "event",
     "performance"
    ],
    "description": "Scope the guardrails apply to; the narrowest scope wins, and a narrower set can only tighten a wider one (decided 29 September, readiness close-out)"
   },
   "scopeId": {
    "type": "string",
    "description": "Strategy, venue, product, event or performance ID; empty for global",
    "nullable": true
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
    },
    "description": "Commercial Protection: rate types dynamic pricing never moves; all six by default (decided 29 September, readiness close-out)"
   },
   "frozen": {
    "type": "boolean",
    "description": "Frozen: the engine holds the current price in this scope"
   },
   "killSwitchActive": {
    "type": "boolean",
    "description": "Global kill switch: dynamic pricing suspended tenant-wide"
   }
  }
 },
 "DynamicPricingStrategy": {
  "type": "object",
  "x-ticvai-persistence": "catalogue.dynamic_pricing_strategy",
  "description": "**A dynamic pricing strategy: what it prices, from which base and how often** (29 September, data model DM3). ADM-088 and ADM-089. Its rules are `pricing.dynamic_price_rule` rows naming it; its ladder `catalogue.price_ladder`; its limits and automation `catalogue.dynamic_pricing_control`. **Rules-based now; AI factors inform, never replace, the rules** (MoM 19 Aug 2026).",
  "required": [
   "id",
   "scopePath",
   "code",
   "name",
   "strategyType",
   "scopeType",
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
   "strategyType": {
    "type": "string",
    "enum": [
     "demandBased",
     "occupancyBased",
     "availabilityBased",
     "inventoryBased",
     "bookingVelocity",
     "timeToEvent",
     "seasonal",
     "dayOfWeek",
     "timeslot",
     "channel",
     "segment",
     "location",
     "hybrid"
    ]
   },
   "scopeType": {
    "type": "string",
    "enum": [
     "singleProduct",
     "productFamily",
     "event",
     "multiplePerformances",
     "venue",
     "selectedTimeslots",
     "selectedPriceCategories"
    ]
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "productId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "productFamily": {
    "type": "string",
    "maxLength": 100,
    "nullable": true
   },
   "eventId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "performanceIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "timeslotIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "priceCategoryIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "businessUnit": {
    "type": "string",
    "maxLength": 100,
    "nullable": true
   },
   "marketCode": {
    "type": "string",
    "maxLength": 40,
    "nullable": true
   },
   "basePriceSource": {
    "type": "string",
    "maxLength": 100,
    "description": "The price list or rate the adjustments start from."
   },
   "evaluationFrequency": {
    "type": "string",
    "enum": [
     "every15Minutes",
     "every30Minutes",
     "hourly",
     "daily",
     "onInventoryChange",
     "onThresholdTrigger"
    ],
    "default": "hourly"
   },
   "combinationMode": {
    "type": "string",
    "enum": [
     "independent",
     "combinable",
     "exclusive",
     "fallback"
    ],
    "default": "independent"
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
   "clonedFromStrategyId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "ownerPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "draft",
     "active",
     "paused",
     "frozen",
     "expired",
     "retired"
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
    "enum": [
     "demandBased",
     "occupancyBased",
     "availabilityBased",
     "inventoryBased",
     "bookingVelocity",
     "timeToEvent",
     "seasonal",
     "dayOfWeek",
     "timeslot",
     "channel",
     "segment",
     "location",
     "hybrid"
    ],
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
    "description": "Market",
    "nullable": true
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
   "performances": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Performances in scope (one or many)"
   },
   "timeslots": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Timeslots in scope; empty for all"
   },
   "priceCategories": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Price categories in scope; empty for all"
   },
   "basePriceSource": {
    "type": "string",
    "description": "Board 1 price-list rate ID the strategy moves from; a strategy never holds its own base amount"
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date-time",
    "description": "Effective from"
   },
   "effectiveTo": {
    "type": "string",
    "format": "date-time",
    "description": "Effective to; empty for open-ended",
    "nullable": true
   },
   "evaluationFrequency": {
    "type": "string",
    "enum": [
     "every15Minutes",
     "every30Minutes",
     "hourly",
     "daily",
     "onInventoryChange",
     "onThresholdTrigger"
    ],
    "description": "Evaluation frequency; defaults to hourly (decided 29 September, readiness close-out)"
   },
   "productFamily": {
    "type": "string",
    "description": "Product family (for scopeType productFamily)",
    "nullable": true
   },
   "scopeType": {
    "type": "string",
    "enum": [
     "singleProduct",
     "productFamily",
     "event",
     "multiplePerformances",
     "venue",
     "selectedTimeslots",
     "selectedPriceCategories"
    ],
    "description": "Scope Assignment (pack p.77)"
   },
   "combinationMode": {
    "type": "string",
    "enum": [
     "independent",
     "combinable",
     "exclusive",
     "fallback"
    ],
    "description": "Strategy Combination: independent, combinable with other strategies, exclusive control, or fallback; defaults to independent (decided 29 September, readiness close-out)"
   },
   "clonedFromStrategyId": {
    "type": "string",
    "description": "Strategy this one was cloned from (inherits its rules)",
    "nullable": true
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
    "enum": [
     "demandBased",
     "occupancyBased",
     "availabilityBased",
     "inventoryBased",
     "bookingVelocity",
     "timeToEvent",
     "seasonal",
     "dayOfWeek",
     "timeslot",
     "channel",
     "segment",
     "location",
     "hybrid"
    ],
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
    "description": "Market",
    "nullable": true
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
   "performances": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Performances in scope (one or many)"
   },
   "timeslots": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Timeslots in scope; empty for all"
   },
   "priceCategories": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Price categories in scope; empty for all"
   },
   "basePriceSource": {
    "type": "string",
    "description": "Board 1 price-list rate ID the strategy moves from; a strategy never holds its own base amount"
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date-time",
    "description": "Effective from"
   },
   "effectiveTo": {
    "type": "string",
    "format": "date-time",
    "description": "Effective to; empty for open-ended",
    "nullable": true
   },
   "evaluationFrequency": {
    "type": "string",
    "enum": [
     "every15Minutes",
     "every30Minutes",
     "hourly",
     "daily",
     "onInventoryChange",
     "onThresholdTrigger"
    ],
    "description": "Evaluation frequency; defaults to hourly (decided 29 September, readiness close-out)"
   },
   "status": {
    "type": "string",
    "description": "Status: draft, testing, ready, scheduled, active, paused, frozen, expired or retired; draft on create"
   },
   "productFamily": {
    "type": "string",
    "description": "Product family (for scopeType productFamily)",
    "nullable": true
   },
   "scopeType": {
    "type": "string",
    "enum": [
     "singleProduct",
     "productFamily",
     "event",
     "multiplePerformances",
     "venue",
     "selectedTimeslots",
     "selectedPriceCategories"
    ],
    "description": "Scope Assignment (pack p.77)"
   },
   "combinationMode": {
    "type": "string",
    "enum": [
     "independent",
     "combinable",
     "exclusive",
     "fallback"
    ],
    "description": "Strategy Combination: independent, combinable with other strategies, exclusive control, or fallback; defaults to independent (decided 29 September, readiness close-out)"
   },
   "clonedFromStrategyId": {
    "type": "string",
    "description": "Strategy this one was cloned from (inherits its rules)",
    "nullable": true
   }
  }
 },
 "DynamicPricingStrategyCommandCenterSummary": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection; the headline tiles over the list, computed at read time for the filters in force",
  "description": "**The headline figures on Dynamic Pricing Strategy Command Center.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.",
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
    "type": "integer",
    "description": "Products Under Dynamic Pricing"
   },
   "eventsUnderDynamicPricing": {
    "type": "integer",
    "description": "Events Under Dynamic Pricing"
   },
   "performancesUnderDynamicPricing": {
    "type": "integer",
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
    "type": "integer",
    "description": "Prices at Maximum Guardrail"
   },
   "pricesAtMinimumGuardrail": {
    "type": "integer",
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
    "description": "Upcoming Activations: strategies scheduled to activate within 7 days (decided 29 September, readiness close-out)"
   },
   "operationalAlerts": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Operational Alerts (pack p.76), e.g. performances at their upper band, strategies with unresolved conflicts, strategies activating within 48 hours"
   }
  }
 },
 "DynamicPricingStrategyCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Dynamic Pricing Strategy Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
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
    "enum": [
     "demandBased",
     "occupancyBased",
     "availabilityBased",
     "inventoryBased",
     "bookingVelocity",
     "timeToEvent",
     "seasonal",
     "dayOfWeek",
     "timeslot",
     "channel",
     "segment",
     "location",
     "hybrid"
    ],
    "description": "Strategy Type (pack pp.75-76)"
   },
   "productEvent": {
    "type": "string",
    "description": "Product or event the strategy controls"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "basePriceSource": {
    "type": "string",
    "description": "Base price source: the Board 1 price list and rate the strategy moves from, e.g. UAE Standard Admission -> Adult"
   },
   "currentPrice": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Current resolved dynamic price (for a single-price scope)",
    "nullable": true
   },
   "adjustmentRange": {
    "type": "object",
    "properties": {
     "minPercent": {
      "type": "number",
      "description": "Lowest adjustment from base, percent"
     },
     "maxPercent": {
      "type": "number",
      "description": "Highest adjustment from base, percent"
     }
    },
    "description": "Adjustment range allowed by the strategy"
   },
   "ruleCount": {
    "type": "integer",
    "description": "Rule Count"
   },
   "effectivePeriod": {
    "type": "object",
    "properties": {
     "from": {
      "type": "string",
      "format": "date-time",
      "description": "Effective from"
     },
     "to": {
      "type": "string",
      "format": "date-time",
      "description": "Effective to; empty for open-ended",
      "nullable": true
     }
    },
    "description": "Effective period"
   },
   "automationMode": {
    "type": "string",
    "enum": [
     "monitor",
     "recommend",
     "prepareChange",
     "autoExecuteWithinGuardrails"
    ],
    "description": "Automation mode from the automation policy (listDynamicPricingAutomation); recommend by default"
   },
   "status": {
    "type": "string",
    "description": "Status: draft, testing, ready, scheduled, active, paused, frozen, expired or retired"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
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
 "PriceLadder": {
  "type": "object",
  "x-ticvai-persistence": "catalogue.price_ladder",
  "description": "**The bands a dynamic price may move between, and how fast** (29 September, data model DM3). ADM-092. A strategy's adjustment lands on a band, never between them.",
  "required": [
   "id",
   "scopePath",
   "dynamicPricingStrategyId",
   "adjustmentModel"
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
   "dynamicPricingStrategyId": {
    "type": "string",
    "format": "uuid"
   },
   "basePriceSource": {
    "type": "string",
    "maxLength": 100,
    "nullable": true
   },
   "adjustmentModel": {
    "type": "string",
    "enum": [
     "fixedPriceBands",
     "percentageBands",
     "fixedAmountSteps",
     "derivedBands",
     "continuousRange"
    ]
   },
   "bands": {
    "type": "object",
    "additionalProperties": true,
    "description": "`[{code, price, percent}]`, ascending."
   },
   "baseBandCode": {
    "type": "string",
    "maxLength": 40,
    "nullable": true
   },
   "stepAmount": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true
   },
   "minimumPrice": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true
   },
   "basePrice": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true
   },
   "maximumPrice": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true
   },
   "allowUpward": {
    "type": "boolean",
    "default": true
   },
   "allowDownward": {
    "type": "boolean",
    "default": true
   },
   "maxIncreasePercentPerAdjustment": {
    "type": "number",
    "nullable": true
   },
   "maxDecreasePercentPerAdjustment": {
    "type": "number",
    "nullable": true
   },
   "maximumBandsPerMovement": {
    "type": "integer",
    "nullable": true,
    "minimum": 1
   },
   "minimumMinutesBetweenMovements": {
    "type": "integer",
    "nullable": true,
    "minimum": 0
   },
   "cooldownMinutes": {
    "type": "integer",
    "nullable": true,
    "minimum": 0
   },
   "reversalRule": {
    "type": "string",
    "enum": [
     "allowed",
     "afterCooldown",
     "notAllowed"
    ],
    "default": "afterCooldown"
   },
   "allowedEndpoints": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Psychological price endings, e.g. `.99`, `.00`."
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
 "RulePriorityConflictInput": {
  "type": "object",
  "x-ticvai-persistence": "none — request only; the saved hierarchy and test cases are the rows listRulePriorityConflict reads",
  "description": "What `setRulePriorityConflict` takes (decided 29 September, readiness close-out; VM close-out for BO-441 Reorder, Validate, Test, Save).",
  "required": [
   "mode"
  ],
  "properties": {
   "orderedRuleIds": {
    "type": "array",
    "description": "The rules in priority order, highest first. Reorder is this list.",
    "items": {
     "type": "string"
    }
   },
   "resolutionMethod": {
    "type": "string",
    "enum": [
     "highestPriorityWins",
     "mostSpecificRuleWins",
     "cumulativeAdjustment",
     "maximumAdjustmentWins",
     "minimumAdjustmentWins",
     "weightedCombination",
     "stopProcessing",
     "customGovernedResolution"
    ],
    "default": "highestPriorityWins",
    "description": "How two applicable rules are resolved; the same vocabulary as `RulePriorityConflictResolutionDynamicPricingTestConsSummary.resolutionMethod`. Never lowest-price-wins by default (decided 29 September, readiness close-out)."
   },
   "priorityHierarchy": {
    "type": "array",
    "description": "The priority matrix, highest first; defaults to the pack's order.",
    "items": {
     "type": "string",
     "enum": [
      "commercialProtection",
      "contractMemberProtection",
      "eventSpecificStrategy",
      "inventoryOccupancy",
      "bookingVelocity",
      "timeToEvent",
      "seasonDayTimeslot",
      "basePrice"
     ]
    }
   },
   "mode": {
    "type": "string",
    "enum": [
     "save",
     "validate",
     "test"
    ],
    "description": "`validate` checks the order and returns conflicts without saving; `test` runs `testScenario` against the order and saves it as a test case; `save` stores the order and method, refused with `409` while a critical conflict is open."
   },
   "testScenario": {
    "$ref": "#/components/schemas/RulePriorityTestScenario"
   }
  }
 },
 "RulePriorityConflictResolutionDynamicPricingTestConsSummary": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection; the headline tiles over the list, computed at read time for the filters in force",
  "description": "**The headline figures on Rule Priority, Conflict Resolution & Dynamic Pricing Test Console.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.",
  "properties": {
   "contradictoryRules": {
    "type": "integer",
    "description": "Open contradictoryRules conflicts detected across active and draft rules"
   },
   "samePriority": {
    "type": "integer",
    "description": "Open samePriority conflicts detected across active and draft rules"
   },
   "impossibleCondition": {
    "type": "integer",
    "description": "Open impossibleCondition conflicts detected across active and draft rules"
   },
   "overlappingStrategy": {
    "type": "integer",
    "description": "Open overlappingStrategy conflicts detected across active and draft rules"
   },
   "circularDependency": {
    "type": "integer",
    "description": "Open circularDependency conflicts detected across active and draft rules"
   },
   "missingFallback": {
    "type": "integer",
    "description": "Open missingFallback conflicts detected across active and draft rules"
   },
   "guardrailConflict": {
    "type": "integer",
    "description": "Open guardrailConflict conflicts detected across active and draft rules"
   },
   "resolutionMethod": {
    "type": "string",
    "enum": [
     "highestPriorityWins",
     "mostSpecificRuleWins",
     "cumulativeAdjustment",
     "maximumAdjustmentWins",
     "minimumAdjustmentWins",
     "weightedCombination",
     "stopProcessing",
     "customGovernedResolution"
    ],
    "description": "Resolution Method in force (pack p.89); defaults to highestPriorityWins (decided 29 September, readiness close-out)"
   },
   "priorityHierarchy": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "commercialProtection",
      "contractMemberProtection",
      "eventSpecificStrategy",
      "inventoryOccupancy",
      "bookingVelocity",
      "timeToEvent",
      "seasonDayTimeslot",
      "basePrice"
     ]
    },
    "description": "Priority Matrix, highest first; defaults to the pack's order (decided 29 September, readiness close-out)"
   }
  }
 },
 "RulePriorityConflictResolutionDynamicPricingTestConsView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Rule Priority, Conflict Resolution & Dynamic Pricing Test Console displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "product": {
    "type": "string",
    "description": "Test input: product"
   },
   "event": {
    "type": "string",
    "description": "Test input: event",
    "nullable": true
   },
   "performance": {
    "type": "string",
    "description": "Test input: performance",
    "nullable": true
   },
   "date": {
    "type": "string",
    "format": "date",
    "description": "Test input: visit/event date"
   },
   "timeslot": {
    "type": "string",
    "description": "Test input: timeslot",
    "nullable": true
   },
   "channel": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/SalesChannel"
     }
    ],
    "description": "Test input: channel"
   },
   "customerSegment": {
    "type": "string",
    "description": "Test input: customer segment"
   },
   "basePrice": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Test input: base price"
   },
   "occupancy": {
    "type": "number",
    "description": "Test input: occupancy percent"
   },
   "inventory": {
    "type": "integer",
    "description": "Test input: remaining inventory"
   },
   "bookingVelocity": {
    "type": "number",
    "description": "Test input: booking velocity, percent against expected pace"
   },
   "timeToEvent": {
    "type": "integer",
    "description": "Test input: days to event (0 = same day)"
   },
   "calculationPath": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Explainability: the complete calculation path, one step per line"
   },
   "testCaseId": {
    "type": "string",
    "description": "Test case ID"
   },
   "caseName": {
    "type": "string",
    "description": "Test case name"
   },
   "caseType": {
    "type": "string",
    "enum": [
     "lowDemand",
     "highDemand",
     "nearSellOut",
     "earlyBird",
     "lastMinute",
     "weekendPeak",
     "memberPurchase",
     "b2bContract",
     "custom"
    ],
    "description": "Test case type (pack p.91)"
   },
   "rulesMatched": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "ruleId": {
       "type": "string",
       "description": "Rule"
      },
      "ruleName": {
       "type": "string",
       "description": "Rule name"
      },
      "priorityLevel": {
       "type": "string",
       "enum": [
        "commercialProtection",
        "contractMemberProtection",
        "eventSpecificStrategy",
        "inventoryOccupancy",
        "bookingVelocity",
        "timeToEvent",
        "seasonDayTimeslot",
        "basePrice"
       ],
       "description": "Hierarchy level"
      },
      "adjustmentPercent": {
       "type": "number",
       "description": "Adjustment in percent",
       "nullable": true
      },
      "applied": {
       "type": "boolean",
       "description": "Applied after resolution"
      }
     },
     "description": "One matched rule"
    },
    "description": "Rules matched"
   },
   "rawCalculatedPrice": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Raw calculated price"
   },
   "ladderPrice": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Nearest allowed band"
   },
   "guardrailOutcome": {
    "type": "string",
    "enum": [
     "passed",
     "cappedAtMaximum",
     "raisedToMinimum",
     "protectedRateApplied"
    ],
    "description": "Guardrail result"
   },
   "finalPrice": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Final dynamic price"
   },
   "conflicts": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "code": {
       "type": "string",
       "enum": [
        "contradictoryRules",
        "samePriority",
        "impossibleCondition",
        "overlappingStrategy",
        "circularDependency",
        "missingFallback",
        "guardrailConflict"
       ],
       "description": "Conflict type (pack p.90)"
      },
      "message": {
       "type": "string",
       "description": "Message"
      },
      "ruleIds": {
       "type": "array",
       "items": {
        "type": "string"
       },
       "description": "Rules involved"
      }
     },
     "description": "One conflict"
    },
    "description": "Conflicts met while resolving this case"
   },
   "lastRunAt": {
    "type": "string",
    "format": "date-time",
    "description": "Last run"
   },
   "passed": {
    "type": "boolean",
    "description": "Final price matched the expected price saved with the case",
    "nullable": true
   },
   "expectedPrice": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Expected final price for regression",
    "nullable": true
   }
  }
 },
 "RulePriorityConflictView": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over the saved priority order and test cases",
  "description": "What `setRulePriorityConflict` returns: the order in force, the conflicts it has and, in `test` mode, the result.",
  "properties": {
   "mode": {
    "type": "string",
    "enum": [
     "save",
     "validate",
     "test"
    ]
   },
   "saved": {
    "type": "boolean"
   },
   "orderedRuleIds": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "resolutionMethod": {
    "type": "string"
   },
   "priorityHierarchy": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "conflicts": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "code": {
       "type": "string",
       "enum": [
        "contradictoryRules",
        "samePriority",
        "impossibleCondition",
        "overlappingStrategy",
        "circularDependency",
        "missingFallback",
        "guardrailConflict"
       ]
      },
      "severity": {
       "type": "string",
       "enum": [
        "critical",
        "warning"
       ]
      },
      "ruleIds": {
       "type": "array",
       "items": {
        "type": "string"
       }
      },
      "message": {
       "type": "string"
      }
     }
    }
   },
   "testResult": {
    "nullable": true,
    "allOf": [
     {
      "$ref": "#/components/schemas/RulePriorityConflictResolutionDynamicPricingTestConsView"
     }
    ],
    "description": "The saved test case with its deterministic result, in `test` mode."
   },
   "savedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "RulePriorityTestScenario": {
  "type": "object",
  "description": "A sample booking for the conflict test console (pack p.90), the same inputs as a saved test case.",
  "properties": {
   "caseName": {
    "type": "string",
    "maxLength": 120
   },
   "caseType": {
    "type": "string",
    "enum": [
     "lowDemand",
     "highDemand",
     "nearSellOut",
     "earlyBird",
     "lastMinute",
     "weekendPeak",
     "memberPurchase",
     "b2bContract",
     "custom"
    ]
   },
   "productId": {
    "type": "string",
    "format": "uuid"
   },
   "eventId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "performanceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "date": {
    "type": "string",
    "format": "date"
   },
   "timeslot": {
    "type": "string",
    "nullable": true
   },
   "channel": {
    "$ref": "../shared/common.yaml#/components/schemas/SalesChannel"
   },
   "customerSegment": {
    "type": "string",
    "nullable": true
   },
   "basePrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "occupancy": {
    "type": "number",
    "minimum": 0,
    "maximum": 100
   },
   "inventory": {
    "type": "integer",
    "minimum": 0
   },
   "bookingVelocity": {
    "type": "number"
   },
   "timeToEvent": {
    "type": "integer",
    "minimum": 0
   },
   "expectedPrice": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true
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
    "description": "Season name (e.g. Low Season, Peak Season)",
    "nullable": true
   },
   "month": {
    "type": "integer",
    "description": "Month 1-12",
    "nullable": true
   },
   "week": {
    "type": "integer",
    "description": "ISO week 1-53",
    "nullable": true
   },
   "dateRange": {
    "type": "object",
    "properties": {
     "from": {
      "type": "string",
      "format": "date",
      "description": "From"
     },
     "to": {
      "type": "string",
      "format": "date",
      "description": "To"
     }
    },
    "description": "Date range",
    "nullable": true
   },
   "daysOfWeek": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "monday",
      "tuesday",
      "wednesday",
      "thursday",
      "friday",
      "saturday",
      "sunday"
     ]
    },
    "description": "Days of week; saturday+sunday for weekend"
   },
   "timeOfDay": {
    "type": "object",
    "properties": {
     "from": {
      "type": "string",
      "description": "From, HH:mm"
     },
     "to": {
      "type": "string",
      "description": "To, HH:mm"
     }
    },
    "description": "Time-of-day window",
    "nullable": true
   },
   "timeslotIds": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Timeslot IDs"
   },
   "performanceIds": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Performance IDs"
   },
   "specialCalendarEntry": {
    "type": "string",
    "description": "Special-calendar entry (public/school holiday, Ramadan, Eid, custom), maintained as tenant data",
    "nullable": true
   },
   "ruleId": {
    "type": "string",
    "description": "Rule ID"
   },
   "ruleName": {
    "type": "string",
    "description": "Rule name"
   },
   "strategyId": {
    "type": "string",
    "description": "Strategy the rule belongs to"
   },
   "dimension": {
    "type": "string",
    "enum": [
     "season",
     "month",
     "week",
     "dateRange",
     "publicHoliday",
     "schoolHoliday",
     "dayOfWeek",
     "weekend",
     "timeOfDay",
     "timeslot",
     "performance",
     "specialDate"
    ],
    "description": "Supported Dimension (pack p.81)"
   },
   "dynamicRangeMinPercent": {
    "type": "number",
    "description": "Dynamic range low end in percent of base, e.g. -15"
   },
   "dynamicRangeMaxPercent": {
    "type": "number",
    "description": "Dynamic range high end in percent of base, e.g. +20"
   },
   "assignedStrategyId": {
    "type": "string",
    "description": "Strategy applied in this window (Timeslot Rules: 09:00-12:00 -> Off-Peak Strategy)",
    "nullable": true
   },
   "overlapsWith": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Rule IDs this rule overlaps (Overlap Detection)"
   },
   "enabled": {
    "type": "boolean",
    "description": "Enabled"
   }
  }
 }
}
```
