# WS39 — Pricing   Revenue Management board 6

**10 screens · 10 operations · 10 schemas · 1 permissions**

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

- **Every control that can be refused must be gated.** 1 permissions apply here:
  `PRODUCT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **0 of these operations work offline**
  
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-098` | AI Pricing Intelligence Command Center | commandCentre | 1 | 0 | — |
| `ADM-099` | Internal Demand & Booking Signal Hub | listDetail | 1 | 0 | — |
| `ADM-100` | Weather Intelligence & Demand Impact Configuration | commandCentre | 1 | 0 | — |
| `ADM-101` | Nearby Event, Exhibition & Local Demand Intelligence | configEditor | 1 | 0 | — |
| `ADM-102` | Competitor Pricing & Market Position Intelligence | listDetail | 1 | 0 | — |
| `ADM-103` | Market, Tourism, Holiday & Contextual Signal Hub | listDetail | 1 | 0 | — |
| `ADM-104` | AI Demand Forecasting & Booking Curve Studio | listDetail | 1 | 0 | — |
| `ADM-105` | Price Elasticity & Revenue Response Intelligence | listDetail | 1 | 0 | — |
| `ADM-106` | AI Pricing Recommendation & Explainability Center | listDetail | 1 | 0 | — |
| `ADM-107` | AI Signal Registry, Data Quality & Model Governance | listDetail | 1 | 0 | — |

## Thin screens in this batch

**ADM-099, ADM-100, ADM-102, ADM-103, ADM-104, ADM-105, ADM-106, ADM-107 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-098",
  "name": "AI Pricing Intelligence Command Center",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "6",
   "number": "10.6.1",
   "page": 94
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/ai-pricing-intelligence-command-center-adm-098",
   "component": "apps/ticvai-web/src/routes/commercial/AiPricingIntelligenceCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-099",
    "ADM-100",
    "ADM-101",
    "ADM-102",
    "ADM-103",
    "ADM-104",
    "ADM-105",
    "ADM-106",
    "ADM-107"
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
     "to": "ADM-099",
     "trigger": "Works in Internal Demand & Booking Signal Hub",
     "provenance": "flow F148 step 1→2",
     "operation": "listPricing"
    },
    {
     "to": "ADM-100",
     "trigger": "Works in Weather Intelligence & Demand Impact Configuration",
     "provenance": "flow F148 step 3→4",
     "operation": "listPricing"
    },
    {
     "to": "ADM-101",
     "trigger": "Works in Nearby Event, Exhibition & Local Demand Intelligence",
     "provenance": "flow F148 step 5→6",
     "operation": "listPricing"
    },
    {
     "to": "ADM-102",
     "trigger": "Works in Competitor Pricing & Market Position Intelligence",
     "provenance": "flow F148 step 7→8",
     "operation": "listPricing"
    },
    {
     "to": "ADM-103",
     "trigger": "Works in Market, Tourism, Holiday & Contextual Signal Hub",
     "provenance": "flow F148 step 9→10",
     "operation": "listPricing"
    },
    {
     "to": "ADM-104",
     "trigger": "Works in AI Demand Forecasting & Booking Curve Studio",
     "provenance": "flow F148 step 11→12",
     "operation": "listPricing"
    },
    {
     "to": "ADM-105",
     "trigger": "Works in Price Elasticity & Revenue Response Intelligence",
     "provenance": "flow F148 step 13→14",
     "operation": "listPricing"
    },
    {
     "to": "ADM-106",
     "trigger": "Works in AI Pricing Recommendation & Explainability Center",
     "provenance": "flow F148 step 15→16",
     "operation": "listPricing"
    },
    {
     "to": "ADM-107",
     "trigger": "Works in AI Signal Registry, Data Quality & Model Governance",
     "provenance": "flow F148 step 17→18",
     "operation": "listPricing"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each opportunity displays) — counts over a population, then the population",
  "purpose": "Provide Revenue Managers with a single operational view of all AI signals, forecasts, opportunities and risks influencing pricing.",
  "purposeNote": "Revenue teams can understand all significant AI pricing opportunities, risks, forecasts and external demand drivers from one centralized intelligence workspace.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Active AI Recommendations",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 94 §Display",
       "bindsTo": "AiPricingIntelligenceCommandCenterView.activeAiRecommendations"
      },
      {
       "kind": "metricTile",
       "label": "High-Priority Opportunities",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 94 §Display",
       "bindsTo": "AiPricingIntelligenceCommandCenterView.highPriorityOpportunities"
      },
      {
       "kind": "metricTile",
       "label": "Estimated Revenue Opportunity",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 94 §Display",
       "bindsTo": "AiPricingIntelligenceCommandCenterView.estimatedRevenueOpportunity"
      },
      {
       "kind": "metricTile",
       "label": "Demand Surges Detected",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 94 §Display",
       "bindsTo": "AiPricingIntelligenceCommandCenterView.demandSurgesDetected"
      },
      {
       "kind": "metricTile",
       "label": "Demand Risks Detected",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 94 §Display",
       "bindsTo": "AiPricingIntelligenceCommandCenterView.demandRisksDetected"
      },
      {
       "kind": "metricTile",
       "label": "External Signals Active",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 94 §Display",
       "bindsTo": "AiPricingIntelligenceCommandCenterView.externalSignalsActive"
      },
      {
       "kind": "metricTile",
       "label": "Nearby Events Detected",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 94 §Display",
       "bindsTo": "AiPricingIntelligenceCommandCenterView.nearbyEventsDetected"
      },
      {
       "kind": "metricTile",
       "label": "Weather Impacts",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 94 §Display",
       "bindsTo": "AiPricingIntelligenceCommandCenterView.weatherImpacts"
      },
      {
       "kind": "metricTile",
       "label": "Competitor Movements",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 94 §Display",
       "bindsTo": "AiPricingIntelligenceCommandCenterView.competitorMovements"
      },
      {
       "kind": "metricTile",
       "label": "Forecast Accuracy",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 94 §Display",
       "bindsTo": "AiPricingIntelligenceCommandCenterView.forecastAccuracy"
      },
      {
       "kind": "metricTile",
       "label": "Average AI Confidence",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 94 §Display",
       "bindsTo": "AiPricingIntelligenceCommandCenterView.averageAiConfidence"
      },
      {
       "kind": "metricTile",
       "label": "Data Quality Issues",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 94 §Display",
       "bindsTo": "AiPricingIntelligenceCommandCenterView.dataQualityIssues"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every pricing intelligence",
       "columns": [
        "AiPricingIntelligenceCommandCenterView.productEvent",
        "AiPricingIntelligenceCommandCenterView.venue",
        "AiPricingIntelligenceCommandCenterView.currentPrice",
        "AiPricingIntelligenceCommandCenterView.recommendedPrice",
        "AiPricingIntelligenceCommandCenterView.adjustment",
        "AiPricingIntelligenceCommandCenterView.demandForecast",
        "AiPricingIntelligenceCommandCenterView.revenueOpportunity",
        "AiPricingIntelligenceCommandCenterView.primaryDrivers",
        "AiPricingIntelligenceCommandCenterView.confidence",
        "AiPricingIntelligenceCommandCenterView.risk",
        "AiPricingIntelligenceCommandCenterView.urgency"
       ],
       "bindsTo": "AiPricingIntelligenceCommandCenterView",
       "operation": "listPricing",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 94 §Each opportunity displays"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected pricing intelligence",
       "bindsTo": "AiPricingIntelligenceCommandCenterView",
       "columns": [
        "AiPricingIntelligenceCommandCenterView.productEvent",
        "AiPricingIntelligenceCommandCenterView.venue",
        "AiPricingIntelligenceCommandCenterView.currentPrice",
        "AiPricingIntelligenceCommandCenterView.recommendedPrice",
        "AiPricingIntelligenceCommandCenterView.adjustment",
        "AiPricingIntelligenceCommandCenterView.demandForecast",
        "AiPricingIntelligenceCommandCenterView.revenueOpportunity",
        "AiPricingIntelligenceCommandCenterView.primaryDrivers",
        "AiPricingIntelligenceCommandCenterView.confidence",
        "AiPricingIntelligenceCommandCenterView.risk",
        "AiPricingIntelligenceCommandCenterView.urgency"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Saturday Evening Admission”, “Drivers”.",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 94 §Each opportunity displays"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The pricing intelligence list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the pricing intelligence untouched.",
   "emptyFirstRun": "No pricing intelligence yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the pricing intelligence are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPricing",
    "contract": "catalogue",
    "purpose": "AI Pricing Intelligence Command Center",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-098"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 94. 23 of 23 labels bound to a contract property; 23 of 49 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-099",
  "name": "Internal Demand & Booking Signal Hub",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "6",
   "number": "10.6.2",
   "page": 95
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/internal-demand-booking-signal-hub-adm-099",
   "component": "apps/ticvai-web/src/routes/commercial/InternalDemandBookingSignalHub.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-098"
   ],
   "exitTo": [
    "ADM-098"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-098, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-098",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F148 step 2→3",
     "operation": "listInternalDemandBooking"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Centralize the internal TICVAI signals used by forecasting and AI pricing models. These are generally the highest-confidence signals because they come directly from TICVAI transactions.",
  "purposeNote": "pricing intelligence.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 95"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 95"
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
       "impliedBy": "listInternalDemandBooking",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The internal demand booking list.",
   "error": "Could not load. Names which read failed and leaves the internal demand booking untouched.",
   "emptyFirstRun": "No internal demand booking yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the internal demand booking are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listInternalDemandBooking",
    "contract": "catalogue",
    "purpose": "Internal Demand & Booking Signal Hub",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "InternalDemandBookingSignalHubView.ticketsSold",
    "InternalDemandBookingSignalHubView.orders",
    "InternalDemandBookingSignalHubView.revenue",
    "InternalDemandBookingSignalHubView.averageSellingPrice",
    "InternalDemandBookingSignalHubView.conversionRate"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-099"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 95. 0 of 0 labels bound to a contract property; 0 of 45 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-100",
  "name": "Weather Intelligence & Demand Impact Configuration",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "6",
   "number": "10.6.3",
   "page": 97
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/weather-intelligence-demand-impact-configuration-adm-100",
   "component": "apps/ticvai-web/src/routes/commercial/WeatherIntelligenceDemandImpactConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-098"
   ],
   "exitTo": [
    "ADM-098"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-098, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-098",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F148 step 4→5",
     "operation": "listWeatherDemandImpact"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Show) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Allow TICVAI to understand how weather conditions affect demand for different venues and experiences. This should be much more sophisticated than simply connecting a weather API.",
  "purposeNote": "Weather conditions are converted into venue-specific, explainable demand signals rather than directly changing prices.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Weather Forecast Confidence: 93%",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 97 §Show",
       "bindsTo": "WeatherIntelligenceDemandImpactConfigurationView.weatherForecastConfidence93"
      },
      {
       "kind": "metricTile",
       "label": "Estimated Demand Impact: +8–12%",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 97 §Show",
       "bindsTo": "WeatherIntelligenceDemandImpactConfigurationView.estimatedDemandImpact812"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The weather intelligence demand list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the weather intelligence demand untouched.",
   "emptyFirstRun": "No weather intelligence demand yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the weather intelligence demand are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listWeatherDemandImpact",
    "contract": "catalogue",
    "purpose": "Weather Intelligence & Demand Impact Configuration",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "WeatherIntelligenceDemandImpactConfigurationView.weatherForecastConfidence93",
    "WeatherIntelligenceDemandImpactConfigurationView.estimatedDemandImpact812"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-100"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 97. 2 of 2 labels bound to a contract property; 2 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-101",
  "name": "Nearby Event, Exhibition & Local Demand Intelligence",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "6",
   "number": "10.6.4",
   "page": 99
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/nearby-event-exhibition-local-demand-intelligence-adm-101",
   "component": "apps/ticvai-web/src/routes/commercial/NearbyEventExhibitionLocalDemandIntelligence.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-098"
   ],
   "exitTo": [
    "ADM-098"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-098, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-098",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F148 step 6→7",
     "operation": "listNearbyEventExhibition"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Detect/configure; Capture; Configure per TICVAI venue) and no display directory — it is settings, not a population",
  "purpose": "Detect external events around TICVAI venues that could materially affect visitor demand. This directly addresses the exhibition-near-the-venue scenario.",
  "purposeNote": "impact signals for AI pricing decisions.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Exhibition",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 99 §Detect/configure"
      },
      {
       "kind": "selectField",
       "label": "Conference",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 99 §Detect/configure"
      },
      {
       "kind": "selectField",
       "label": "Concert",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 99 §Detect/configure"
      },
      {
       "kind": "selectField",
       "label": "Sports Event",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 99 §Detect/configure"
      },
      {
       "kind": "selectField",
       "label": "Festival",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 99 §Detect/configure"
      },
      {
       "kind": "selectField",
       "label": "Trade Show",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 99 §Detect/configure"
      },
      {
       "kind": "selectField",
       "label": "Convention",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 99 §Detect/configure"
      },
      {
       "kind": "selectField",
       "label": "Public Celebration",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 99 §Detect/configure"
      },
      {
       "kind": "selectField",
       "label": "Major Attraction Event",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 99 §Detect/configure"
      },
      {
       "kind": "selectField",
       "label": "School Event",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 99 §Detect/configure"
      },
      {
       "kind": "selectField",
       "label": "Custom Local Event",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 99 §Detect/configure"
      },
      {
       "kind": "selectField",
       "label": "Event Name",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 99 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 99 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Location",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 99 §Capture"
      },
      {
       "kind": "textField",
       "label": "Distance from TICVAI Venue",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 99 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Start/End Date",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 99 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Start/End Time",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 99 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Expected Attendance",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 99 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Event Type",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 99 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Audience Type",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 99 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Source",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 99 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Confidence",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 99 §Capture"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The nearby event exhibition configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the nearby event exhibition untouched.",
   "emptyFirstRun": "No nearby event exhibition configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listNearbyEventExhibition",
    "contract": "catalogue",
    "purpose": "Nearby Event, Exhibition & Local Demand Intelligence",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-101"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 99. 0 of 0 labels bound to a contract property; 22 of 47 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-102",
  "name": "Competitor Pricing & Market Position Intelligence",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "6",
   "number": "10.6.5",
   "page": 100
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/competitor-pricing-market-position-intelligence-adm-102",
   "component": "apps/ticvai-web/src/routes/commercial/CompetitorPricingMarketPositionIntelligence.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-098"
   ],
   "exitTo": [
    "ADM-098"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-098, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-098",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F148 step 8→9",
     "operation": "listCompetitorPricingMarket"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Track) and no metric row",
  "purpose": "Allow TICVAI to understand its commercial position relative to relevant competitors.",
  "purposeNote": "competitor data alone to determine the selling price.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every competitor pricing market",
       "columns": [
        "CompetitorPricingMarketPositionIntelligenceView.publishedPrice",
        "CompetitorPricingMarketPositionIntelligenceView.promotionalPrice",
        "CompetitorPricingMarketPositionIntelligenceView.weekendPrice",
        "CompetitorPricingMarketPositionIntelligenceView.peakPrice",
        "CompetitorPricingMarketPositionIntelligenceView.residentPrice",
        "CompetitorPricingMarketPositionIntelligenceView.memberPriceWherePubliclyAvailable",
        "CompetitorPricingMarketPositionIntelligenceView.availability",
        "CompetitorPricingMarketPositionIntelligenceView.date",
        "CompetitorPricingMarketPositionIntelligenceView.timeslot"
       ],
       "bindsTo": "CompetitorPricingMarketPositionIntelligenceView",
       "operation": "listCompetitorPricingMarket",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 100 §Track"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected competitor pricing market",
       "bindsTo": "CompetitorPricingMarketPositionIntelligenceView",
       "columns": [
        "CompetitorPricingMarketPositionIntelligenceView.publishedPrice",
        "CompetitorPricingMarketPositionIntelligenceView.promotionalPrice",
        "CompetitorPricingMarketPositionIntelligenceView.weekendPrice",
        "CompetitorPricingMarketPositionIntelligenceView.peakPrice",
        "CompetitorPricingMarketPositionIntelligenceView.residentPrice",
        "CompetitorPricingMarketPositionIntelligenceView.memberPriceWherePubliclyAvailable",
        "CompetitorPricingMarketPositionIntelligenceView.availability",
        "CompetitorPricingMarketPositionIntelligenceView.date",
        "CompetitorPricingMarketPositionIntelligenceView.timeslot"
       ],
       "notes": "The pack groups this record's detail under its own headings: “AED 275”, “Comparable Product Mapping”, “General Admission”, “Historical Correlation”, “Ethical/Legal Controls”.",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 100 §Track"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The competitor pricing market list.",
   "error": "Could not load. Names which read failed and leaves the competitor pricing market untouched.",
   "emptyFirstRun": "No competitor pricing market yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the competitor pricing market are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCompetitorPricingMarket",
    "contract": "catalogue",
    "purpose": "Competitor Pricing & Market Position Intelligence",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "CompetitorPricingMarketPositionIntelligenceView.publishedPrice",
    "CompetitorPricingMarketPositionIntelligenceView.promotionalPrice",
    "CompetitorPricingMarketPositionIntelligenceView.weekendPrice",
    "CompetitorPricingMarketPositionIntelligenceView.peakPrice",
    "CompetitorPricingMarketPositionIntelligenceView.residentPrice",
    "CompetitorPricingMarketPositionIntelligenceView.memberPriceWherePubliclyAvailable"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-102"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 100. 9 of 9 labels bound to a contract property; 18 of 30 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-103",
  "name": "Market, Tourism, Holiday & Contextual Signal Hub",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "6",
   "number": "10.6.6",
   "page": 102
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/market-tourism-holiday-contextual-signal-hub-adm-103",
   "component": "apps/ticvai-web/src/routes/commercial/MarketTourismHolidayContextualSignalHub.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-098"
   ],
   "exitTo": [
    "ADM-098"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-098, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-098",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F148 step 10→11",
     "operation": "listMarketTourismHoliday"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Capture broader external factors that may affect visitor demand beyond weather and nearby events.",
  "purposeNote": "demand-intelligence layer.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 102"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 102"
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
       "impliedBy": "listMarketTourismHoliday",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The market tourism holiday list.",
   "error": "Could not load. Names which read failed and leaves the market tourism holiday untouched.",
   "emptyFirstRun": "No market tourism holiday yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the market tourism holiday are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listMarketTourismHoliday",
    "contract": "catalogue",
    "purpose": "Market, Tourism, Holiday & Contextual Signal Hub",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "MarketTourismHolidayContextualSignalHubView.publicHolidays",
    "MarketTourismHolidayContextualSignalHubView.schoolHolidays",
    "MarketTourismHolidayContextualSignalHubView.ramadan",
    "MarketTourismHolidayContextualSignalHubView.eid",
    "MarketTourismHolidayContextualSignalHubView.christmas"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-103"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 102. 0 of 0 labels bound to a contract property; 0 of 38 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-104",
  "name": "AI Demand Forecasting & Booking Curve Studio",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "6",
   "number": "10.6.7",
   "page": 103
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/ai-demand-forecasting-booking-curve-studio-adm-104",
   "component": "apps/ticvai-web/src/routes/commercial/AiDemandForecastingBookingCurveStudio.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-098"
   ],
   "exitTo": [
    "ADM-098"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-098, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-098",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F148 step 12→13",
     "operation": "listDemandBookingCurve"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display; Track) and no metric row",
  "purpose": "Predict future demand at a granular commercial level. This is the core predictive engine behind intelligent dynamic pricing.",
  "purposeNote": "approved external signals.",
  "gaps": [
   {
    "operation": null,
    "why": "**AI Demand Forecasting & Booking Curve Studio declares no operation that writes anything** — its only declared call is `listDemandBookingCurve`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
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
       "label": "Every demand forecasting booking",
       "columns": [
        "AiDemandForecastingBookingCurveStudioView.confidence91",
        "AiDemandForecastingBookingCurveStudioView.strongHistoricalData",
        "AiDemandForecastingBookingCurveStudioView.stableBookingPattern",
        "AiDemandForecastingBookingCurveStudioView.reliableExternalSignals",
        "AiDemandForecastingBookingCurveStudioView.mape",
        "AiDemandForecastingBookingCurveStudioView.forecastBias",
        "AiDemandForecastingBookingCurveStudioView.overForecast",
        "AiDemandForecastingBookingCurveStudioView.underForecast"
       ],
       "bindsTo": "AiDemandForecastingBookingCurveStudioView",
       "operation": "listDemandBookingCurve",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 103 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected demand forecasting booking",
       "bindsTo": "AiDemandForecastingBookingCurveStudioView",
       "columns": [
        "AiDemandForecastingBookingCurveStudioView.confidence91",
        "AiDemandForecastingBookingCurveStudioView.strongHistoricalData",
        "AiDemandForecastingBookingCurveStudioView.stableBookingPattern",
        "AiDemandForecastingBookingCurveStudioView.reliableExternalSignals",
        "AiDemandForecastingBookingCurveStudioView.mape",
        "AiDemandForecastingBookingCurveStudioView.forecastBias",
        "AiDemandForecastingBookingCurveStudioView.overForecast",
        "AiDemandForecastingBookingCurveStudioView.underForecast"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Historical Expected Curve”, “Current Actual Curve”, “Saturday Performance”, “Actual”, “Provide”, “Clearly show which signals contributed”.",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 103 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The demand forecasting booking list.",
   "error": "Could not load. Names which read failed and leaves the demand forecasting booking untouched.",
   "emptyFirstRun": "No demand forecasting booking yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the demand forecasting booking are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listDemandBookingCurve",
    "contract": "catalogue",
    "purpose": "AI Demand Forecasting & Booking Curve Studio",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "AiDemandForecastingBookingCurveStudioView.confidence91",
    "AiDemandForecastingBookingCurveStudioView.strongHistoricalData",
    "AiDemandForecastingBookingCurveStudioView.stableBookingPattern",
    "AiDemandForecastingBookingCurveStudioView.reliableExternalSignals",
    "AiDemandForecastingBookingCurveStudioView.mape",
    "AiDemandForecastingBookingCurveStudioView.forecastBias"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-104"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 103. 8 of 8 labels bound to a contract property; 8 of 48 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-105",
  "name": "Price Elasticity & Revenue Response Intelligence",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "6",
   "number": "10.6.8",
   "page": 105
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/price-elasticity-revenue-response-intelligence-adm-105",
   "component": "apps/ticvai-web/src/routes/commercial/PriceElasticityRevenueResponseIntelligence.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-098"
   ],
   "exitTo": [
    "ADM-098"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-098, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-098",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F148 step 14→15",
     "operation": "listPriceElasticityRevenue"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Analyze) and no metric row",
  "purpose": "Estimate how customers are likely to respond to different prices.",
  "purposeNote": "visible confidence and supporting evidence.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every price elasticity revenue",
       "columns": [
        "PriceElasticityRevenueResponseIntelligenceView.price",
        "PriceElasticityRevenueResponseIntelligenceView.demand",
        "PriceElasticityRevenueResponseIntelligenceView.conversion",
        "PriceElasticityRevenueResponseIntelligenceView.revenue",
        "PriceElasticityRevenueResponseIntelligenceView.margin",
        "PriceElasticityRevenueResponseIntelligenceView.occupancy",
        "PriceElasticityRevenueResponseIntelligenceView.customerSegment",
        "PriceElasticityRevenueResponseIntelligenceView.channel",
        "PriceElasticityRevenueResponseIntelligenceView.time",
        "PriceElasticityRevenueResponseIntelligenceView.product"
       ],
       "bindsTo": "PriceElasticityRevenueResponseIntelligenceView",
       "operation": "listPriceElasticityRevenue",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 105 §Analyze"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected price elasticity revenue",
       "bindsTo": "PriceElasticityRevenueResponseIntelligenceView",
       "columns": [
        "PriceElasticityRevenueResponseIntelligenceView.price",
        "PriceElasticityRevenueResponseIntelligenceView.demand",
        "PriceElasticityRevenueResponseIntelligenceView.conversion",
        "PriceElasticityRevenueResponseIntelligenceView.revenue",
        "PriceElasticityRevenueResponseIntelligenceView.margin",
        "PriceElasticityRevenueResponseIntelligenceView.occupancy",
        "PriceElasticityRevenueResponseIntelligenceView.customerSegment",
        "PriceElasticityRevenueResponseIntelligenceView.channel",
        "PriceElasticityRevenueResponseIntelligenceView.time",
        "PriceElasticityRevenueResponseIntelligenceView.product"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Elasticity answers”, “AED AED”, “Analyze differences by”, “Where insufficient data exists”.",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 105 §Analyze"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The price elasticity revenue list.",
   "error": "Could not load. Names which read failed and leaves the price elasticity revenue untouched.",
   "emptyFirstRun": "No price elasticity revenue yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the price elasticity revenue are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPriceElasticityRevenue",
    "contract": "catalogue",
    "purpose": "Price Elasticity & Revenue Response Intelligence",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "PriceElasticityRevenueResponseIntelligenceView.price",
    "PriceElasticityRevenueResponseIntelligenceView.demand",
    "PriceElasticityRevenueResponseIntelligenceView.conversion",
    "PriceElasticityRevenueResponseIntelligenceView.revenue",
    "PriceElasticityRevenueResponseIntelligenceView.margin",
    "PriceElasticityRevenueResponseIntelligenceView.occupancy"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-105"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 105. 10 of 10 labels bound to a contract property; 10 of 34 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-106",
  "name": "AI Pricing Recommendation & Explainability Center",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "6",
   "number": "10.6.9",
   "page": 107
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/ai-pricing-recommendation-explainability-center-adm-106",
   "component": "apps/ticvai-web/src/routes/commercial/AiPricingRecommendationExplainabilityCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-098"
   ],
   "exitTo": [
    "ADM-098"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-098, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-098",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F148 step 16→17",
     "operation": "listPricingRecommendationExplainability"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Convert all intelligence generated by Board 6 into actionable pricing recommendations. This is the central AI recommendation screen.",
  "purposeNote": "Every AI pricing recommendation is accompanied by understandable evidence, expected commercial impact, confidence and human-governance actions.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 107"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 107"
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
       "kind": "banner",
       "label": "Permissions this screen separates",
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** Accept, Reject, Modify, Send to Simulation, Send for Approval, Ignore, Add Comment. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 107 §Authorized users can"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listPricingRecommendationExplainability",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The pricing recommendation explainability list.",
   "error": "Could not load. Names which read failed and leaves the pricing recommendation explainability untouched.",
   "emptyFirstRun": "No pricing recommendation explainability yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the pricing recommendation explainability are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPricingRecommendationExplainability",
    "contract": "catalogue",
    "purpose": "AI Pricing Recommendation & Explainability Center",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "AiPricingRecommendationExplainabilityCenterView.expectedRevenueImpact",
    "AiPricingRecommendationExplainabilityCenterView.expectedOccupancy",
    "AiPricingRecommendationExplainabilityCenterView.confidence",
    "AiPricingRecommendationExplainabilityCenterView.bookingVelocity",
    "AiPricingRecommendationExplainabilityCenterView.nearbyExhibition"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-106"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 107. 0 of 0 labels bound to a contract property; 7 of 38 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-107",
  "name": "AI Signal Registry, Data Quality & Model Governance",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "6",
   "number": "10.6.10",
   "page": 108
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/ai-signal-registry-data-quality-model-governance-adm-107",
   "component": "apps/ticvai-web/src/routes/commercial/AiSignalRegistryDataQualityModelGovernance.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-098"
   ],
   "exitTo": [
    "ADM-098"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-098, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation."
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display; Monitor; Track) and no metric row",
  "purpose": "Govern the complete data and intelligence ecosystem behind AI pricing. This is critical. Without this screen, Development team could connect many external sources without giving TICVAI proper control over them.",
  "purposeNote": "signals and predictive models used by AI pricing. Board 6 — Final Screen Register # Backend Screen Core Responsibility 10.6. AI Pricing Intelligence Command Center AI opportunity overview 1 10.6. TICVAI transactional Internal Demand & Booking Signal Hub 2 intelligence 10.6. Weather Intelligence & Demand Impact",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every signal registry data",
       "columns": [
        "AiSignalRegistryDataQualityModelGovernanceView.signal",
        "AiSignalRegistryDataQualityModelGovernanceView.category",
        "AiSignalRegistryDataQualityModelGovernanceView.provider",
        "AiSignalRegistryDataQualityModelGovernanceView.source",
        "AiSignalRegistryDataQualityModelGovernanceView.internalExternal",
        "AiSignalRegistryDataQualityModelGovernanceView.market",
        "AiSignalRegistryDataQualityModelGovernanceView.refreshFrequency",
        "AiSignalRegistryDataQualityModelGovernanceView.lastUpdate",
        "AiSignalRegistryDataQualityModelGovernanceView.freshness",
        "AiSignalRegistryDataQualityModelGovernanceView.reliability",
        "AiSignalRegistryDataQualityModelGovernanceView.historicalCorrelation",
        "AiSignalRegistryDataQualityModelGovernanceView.status",
        "AiSignalRegistryDataQualityModelGovernanceView.missingData",
        "AiSignalRegistryDataQualityModelGovernanceView.delayedData",
        "AiSignalRegistryDataQualityModelGovernanceView.outliers",
        "Duplicate Data",
        "AiSignalRegistryDataQualityModelGovernanceView.invalidValues",
        "AiSignalRegistryDataQualityModelGovernanceView.unexpectedChanges",
        "AiSignalRegistryDataQualityModelGovernanceView.sourceFailure",
        "AiSignalRegistryDataQualityModelGovernanceView.forecastAccuracy",
        "AiSignalRegistryDataQualityModelGovernanceView.bias",
        "AiSignalRegistryDataQualityModelGovernanceView.recommendationAccuracy",
        "AiSignalRegistryDataQualityModelGovernanceView.revenuePerformance",
        "AiSignalRegistryDataQualityModelGovernanceView.drift"
       ],
       "bindsTo": "AiSignalRegistryDataQualityModelGovernanceView",
       "operation": "listSignalDataQuality",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 108 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected signal registry data",
       "bindsTo": "AiSignalRegistryDataQualityModelGovernanceView",
       "columns": [
        "AiSignalRegistryDataQualityModelGovernanceView.signal",
        "AiSignalRegistryDataQualityModelGovernanceView.category",
        "AiSignalRegistryDataQualityModelGovernanceView.provider",
        "AiSignalRegistryDataQualityModelGovernanceView.source",
        "AiSignalRegistryDataQualityModelGovernanceView.internalExternal",
        "AiSignalRegistryDataQualityModelGovernanceView.market",
        "AiSignalRegistryDataQualityModelGovernanceView.refreshFrequency",
        "AiSignalRegistryDataQualityModelGovernanceView.lastUpdate",
        "AiSignalRegistryDataQualityModelGovernanceView.freshness",
        "AiSignalRegistryDataQualityModelGovernanceView.reliability",
        "AiSignalRegistryDataQualityModelGovernanceView.historicalCorrelation",
        "AiSignalRegistryDataQualityModelGovernanceView.status",
        "AiSignalRegistryDataQualityModelGovernanceView.missingData",
        "AiSignalRegistryDataQualityModelGovernanceView.delayedData",
        "AiSignalRegistryDataQualityModelGovernanceView.outliers",
        "Duplicate Data",
        "AiSignalRegistryDataQualityModelGovernanceView.invalidValues",
        "AiSignalRegistryDataQualityModelGovernanceView.unexpectedChanges",
        "AiSignalRegistryDataQualityModelGovernanceView.sourceFailure",
        "AiSignalRegistryDataQualityModelGovernanceView.forecastAccuracy",
        "AiSignalRegistryDataQualityModelGovernanceView.bias",
        "AiSignalRegistryDataQualityModelGovernanceView.recommendationAccuracy",
        "AiSignalRegistryDataQualityModelGovernanceView.revenuePerformance",
        "AiSignalRegistryDataQualityModelGovernanceView.drift"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Signal Status”, “Health”, “Delaye”, “Hotel Health”, “For example”, “For each signal”.",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 108 §Display"
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
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** Forecasting, Recommendations, Simulation, Automated Pricing. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 108 §AI Use Permission"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The signal registry data list.",
   "error": "Could not load. Names which read failed and leaves the signal registry data untouched.",
   "emptyFirstRun": "No signal registry data yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the signal registry data are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listSignalDataQuality",
    "contract": "catalogue",
    "purpose": "AI Signal Registry, Data Quality & Model Governance",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "AiSignalRegistryDataQualityModelGovernanceView.signal",
    "AiSignalRegistryDataQualityModelGovernanceView.category",
    "AiSignalRegistryDataQualityModelGovernanceView.provider",
    "AiSignalRegistryDataQualityModelGovernanceView.source",
    "AiSignalRegistryDataQualityModelGovernanceView.internalExternal",
    "AiSignalRegistryDataQualityModelGovernanceView.market"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-107"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 108. 23 of 24 labels bound to a contract property; 32 of 121 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "listCompetitorPricingMarket": {
  "method": "GET",
  "path": "/competitor-pricing-market",
  "contract": "catalogue",
  "summary": "Competitor Pricing & Market Position Intelligence",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "CompetitorPricingMarketPositionIntelligenceView"
 },
 "listDemandBookingCurve": {
  "method": "GET",
  "path": "/demand-booking-curve",
  "contract": "catalogue",
  "summary": "AI Demand Forecasting & Booking Curve Studio",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AiDemandForecastingBookingCurveStudioView"
 },
 "listInternalDemandBooking": {
  "method": "GET",
  "path": "/internal-demand-booking",
  "contract": "catalogue",
  "summary": "Internal Demand & Booking Signal Hub",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "InternalDemandBookingSignalHubView"
 },
 "listMarketTourismHoliday": {
  "method": "GET",
  "path": "/market-tourism-holiday",
  "contract": "catalogue",
  "summary": "Market, Tourism, Holiday & Contextual Signal Hub",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "MarketTourismHolidayContextualSignalHubView"
 },
 "listNearbyEventExhibition": {
  "method": "GET",
  "path": "/nearby-event-exhibition",
  "contract": "catalogue",
  "summary": "Nearby Event, Exhibition & Local Demand Intelligence",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "NearbyEventExhibitionLocalDemandIntelligenceView"
 },
 "listPriceElasticityRevenue": {
  "method": "GET",
  "path": "/price-elasticity-revenue",
  "contract": "catalogue",
  "summary": "Price Elasticity & Revenue Response Intelligence",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "weekdayWeekend",
    "in": "query",
    "required": false
   },
   {
    "name": "peakOffPeak",
    "in": "query",
    "required": false
   },
   {
    "name": "eventProximity",
    "in": "query",
    "required": false
   },
   {
    "name": "season",
    "in": "query",
    "required": false
   },
   {
    "name": "venue",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "PriceElasticityRevenueResponseIntelligenceView"
 },
 "listPricing": {
  "method": "GET",
  "path": "/pricing",
  "contract": "catalogue",
  "summary": "AI Pricing Intelligence Command Center",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AiPricingIntelligenceCommandCenterView"
 },
 "listPricingRecommendationExplainability": {
  "method": "GET",
  "path": "/pricing-recommendation-explainability",
  "contract": "catalogue",
  "summary": "AI Pricing Recommendation & Explainability Center",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AiPricingRecommendationExplainabilityCenterView"
 },
 "listSignalDataQuality": {
  "method": "GET",
  "path": "/signal-data-quality",
  "contract": "catalogue",
  "summary": "AI Signal Registry, Data Quality & Model Governance",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AiSignalRegistryDataQualityModelGovernanceView"
 },
 "listWeatherDemandImpact": {
  "method": "GET",
  "path": "/weather-demand-impact",
  "contract": "catalogue",
  "summary": "Weather Intelligence & Demand Impact Configuration",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "WeatherIntelligenceDemandImpactConfigurationView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AiDemandForecastingBookingCurveStudioView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What AI Demand Forecasting & Booking Curve Studio displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
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
   "date": {
    "type": "string",
    "format": "date-time",
    "description": "Date"
   },
   "timeslot": {
    "type": "string",
    "description": "Timeslot"
   },
   "priceCategory": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price Category"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "intraday": {
    "type": "string",
    "description": "Intraday"
   },
   "tomorrow": {
    "type": "string",
    "description": "Tomorrow"
   },
   "eventHorizon": {
    "type": "string",
    "description": "Event Horizon"
   },
   "seasonalHorizon": {
    "type": "string",
    "description": "Seasonal Horizon"
   },
   "confidence91": {
    "type": "number",
    "description": "Confidence: 91%"
   },
   "strongHistoricalData": {
    "type": "string",
    "description": "Strong Historical Data"
   },
   "stableBookingPattern": {
    "type": "string",
    "description": "Stable Booking Pattern"
   },
   "reliableExternalSignals": {
    "type": "integer",
    "description": "Reliable External Signals"
   },
   "expectedAtT7": {
    "type": "string",
    "description": "Expected at T−7"
   },
   "forecastFinalOccupancy": {
    "type": "integer",
    "description": "Forecast Final Occupancy (the pack shows 97%)"
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
   "sellThrough": {
    "type": "string",
    "description": "Sell-Through"
   },
   "expectedSellOutTime": {
    "type": "string",
    "format": "date-time",
    "description": "Expected Sell-Out Time"
   },
   "revenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue"
   },
   "conversion": {
    "type": "number",
    "description": "Conversion"
   },
   "remainingInventory": {
    "type": "string",
    "description": "Remaining Inventory"
   },
   "internalSales35": {
    "type": "number",
    "description": "Internal Sales: 35%"
   },
   "bookingVelocity20": {
    "type": "number",
    "description": "Booking Velocity: 20%"
   },
   "historicalEvents15": {
    "type": "number",
    "description": "Historical Events: 15%"
   },
   "nearbyExhibition10": {
    "type": "number",
    "description": "Nearby Exhibition: 10%"
   },
   "weather8": {
    "type": "number",
    "description": "Weather: 8%"
   },
   "marketTourism7": {
    "type": "number",
    "description": "Market/Tourism: 7%"
   },
   "competitor5": {
    "type": "number",
    "description": "Competitor: 5%"
   },
   "mape": {
    "type": "string",
    "description": "MAPE"
   },
   "forecastBias": {
    "type": "integer",
    "description": "Forecast Bias"
   },
   "overForecast": {
    "type": "string",
    "description": "Over-Forecast"
   },
   "underForecast": {
    "type": "string",
    "description": "Under-Forecast"
   }
  }
 },
 "AiPricingIntelligenceCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What AI Pricing Intelligence Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "activeAiRecommendations": {
    "type": "integer",
    "description": "Active AI Recommendations"
   },
   "highPriorityOpportunities": {
    "type": "integer",
    "description": "High-Priority Opportunities"
   },
   "estimatedRevenueOpportunity": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Estimated Revenue Opportunity"
   },
   "demandSurgesDetected": {
    "type": "string",
    "description": "Demand Surges Detected"
   },
   "demandRisksDetected": {
    "type": "string",
    "description": "Demand Risks Detected"
   },
   "externalSignalsActive": {
    "type": "integer",
    "description": "External Signals Active"
   },
   "nearbyEventsDetected": {
    "type": "string",
    "description": "Nearby Events Detected"
   },
   "weatherImpacts": {
    "type": "integer",
    "description": "Weather Impacts"
   },
   "competitorMovements": {
    "type": "integer",
    "description": "Competitor Movements"
   },
   "forecastAccuracy": {
    "type": "string",
    "description": "Forecast Accuracy"
   },
   "averageAiConfidence": {
    "type": "number",
    "description": "Average AI Confidence"
   },
   "dataQualityIssues": {
    "type": "integer",
    "description": "Data Quality Issues"
   },
   "productEvent": {
    "type": "string",
    "description": "Product/Event"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "currentPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Current Price"
   },
   "recommendedPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Recommended Price"
   },
   "adjustment": {
    "type": "number",
    "description": "Adjustment %"
   },
   "demandForecast": {
    "type": "string",
    "description": "Demand Forecast"
   },
   "revenueOpportunity": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue Opportunity"
   },
   "primaryDrivers": {
    "type": "string",
    "description": "Primary Drivers"
   },
   "confidence": {
    "type": "string",
    "description": "Confidence"
   },
   "risk": {
    "type": "string",
    "description": "Risk"
   },
   "urgency": {
    "type": "string",
    "description": "Urgency"
   },
   "currentAed250": {
    "type": "string",
    "description": "Current: AED 250"
   },
   "recommendedAed270": {
    "type": "string",
    "description": "Recommended: AED 270"
   },
   "expectedRevenueUpliftAed73400": {
    "type": "number",
    "description": "Expected Revenue Uplift: +AED 73,400"
   },
   "confidence91": {
    "type": "number",
    "description": "Confidence: 91%"
   },
   "nearbyExhibition": {
    "type": "string",
    "description": "↑ Nearby Exhibition"
   },
   "bookingVelocity": {
    "type": "string",
    "description": "↑ Booking Velocity"
   },
   "competitorPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "↑ Competitor Price"
   },
   "remainingCapacity": {
    "type": "integer",
    "description": "↓ Remaining Capacity"
   },
   "exhibitions": {
    "type": "string",
    "description": "Exhibitions"
   },
   "conferences": {
    "type": "string",
    "description": "Conferences"
   },
   "concerts": {
    "type": "string",
    "description": "Concerts"
   },
   "sportsEvents": {
    "type": "string",
    "description": "Sports Events"
   },
   "festivals": {
    "type": "string",
    "description": "Festivals"
   },
   "tourismEvents": {
    "type": "string",
    "description": "Tourism Events"
   },
   "weatherConditions": {
    "type": "string",
    "description": "Weather Conditions"
   }
  }
 },
 "AiPricingRecommendationExplainabilityCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What AI Pricing Recommendation & Explainability Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "expectedRevenueImpact": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Expected Revenue Impact (the pack shows +AED 73,400)"
   },
   "expectedOccupancy": {
    "type": "integer",
    "description": "Expected Occupancy (the pack shows 96%)"
   },
   "confidence": {
    "type": "string",
    "description": "Confidence (the pack shows 91%)"
   },
   "bookingVelocity": {
    "type": "string",
    "description": "+ Booking Velocity"
   },
   "nearbyExhibition": {
    "type": "string",
    "description": "+ Nearby Exhibition"
   },
   "weather": {
    "type": "string",
    "description": "+ Weather"
   },
   "occupancy": {
    "type": "integer",
    "description": "+ Occupancy"
   },
   "competitorPricing": {
    "type": "string",
    "description": "+ Competitor Pricing"
   },
   "priceElasticity": {
    "type": "number",
    "description": "− Price Elasticity"
   },
   "overall": {
    "type": "string",
    "description": "Overall (the pack shows 91%)"
   },
   "accept": {
    "type": "string",
    "description": "Accept"
   },
   "modify": {
    "type": "string",
    "description": "Modify"
   },
   "ignore": {
    "type": "string",
    "description": "Ignore"
   },
   "executionBelongsDownstream": {
    "type": "string",
    "description": "Execution belongs downstream"
   }
  }
 },
 "AiSignalRegistryDataQualityModelGovernanceView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What AI Signal Registry, Data Quality & Model Governance displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "signal": {
    "type": "string",
    "description": "Signal"
   },
   "category": {
    "type": "string",
    "description": "Category"
   },
   "provider": {
    "type": "string",
    "description": "Provider"
   },
   "source": {
    "type": "string",
    "description": "Source"
   },
   "internalExternal": {
    "type": "string",
    "description": "Internal/External"
   },
   "market": {
    "type": "string",
    "description": "Market"
   },
   "refreshFrequency": {
    "type": "string",
    "description": "Refresh Frequency"
   },
   "lastUpdate": {
    "type": "string",
    "format": "date-time",
    "description": "Last Update"
   },
   "freshness": {
    "type": "string",
    "description": "Freshness"
   },
   "reliability": {
    "type": "string",
    "description": "Reliability"
   },
   "historicalCorrelation": {
    "type": "string",
    "description": "Historical Correlation"
   },
   "status": {
    "type": "integer",
    "description": "Status"
   },
   "ssTy": {
    "type": "string",
    "description": "ss ty"
   },
   "weather10Min97": {
    "type": "number",
    "description": "Weather 10 min 97%"
   },
   "nearbyEvents1Hr91": {
    "type": "number",
    "description": "Nearby Events 1 hr 91%"
   },
   "competitorA8Hr83": {
    "type": "number",
    "description": "Competitor A 8 hr 83%"
   },
   "daily88": {
    "type": "number",
    "description": "Daily 88%"
   },
   "missingData": {
    "type": "string",
    "description": "Missing Data"
   },
   "delayedData": {
    "type": "string",
    "description": "Delayed Data"
   },
   "outliers": {
    "type": "integer",
    "description": "Outliers"
   },
   "invalidValues": {
    "type": "integer",
    "description": "Invalid Values"
   },
   "unexpectedChanges": {
    "type": "integer",
    "description": "Unexpected Changes"
   },
   "sourceFailure": {
    "type": "string",
    "description": "Source Failure"
   },
   "approved": {
    "type": "integer",
    "description": "Approved"
   },
   "experimental": {
    "type": "string",
    "description": "Experimental"
   },
   "advisoryOnly": {
    "type": "string",
    "description": "Advisory Only"
   },
   "blocked": {
    "type": "string",
    "description": "Blocked"
   },
   "modelName": {
    "type": "string",
    "description": "Model Name"
   },
   "version": {
    "type": "string",
    "description": "Version"
   },
   "purpose": {
    "type": "string",
    "description": "Purpose"
   },
   "deploymentDate": {
    "type": "string",
    "format": "date-time",
    "description": "Deployment Date"
   },
   "trainingWindow": {
    "type": "string",
    "format": "date-time",
    "description": "Training Window"
   },
   "validationResult": {
    "type": "string",
    "description": "Validation Result"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   },
   "forecastAccuracy": {
    "type": "string",
    "description": "Forecast Accuracy"
   },
   "bias": {
    "type": "integer",
    "description": "Bias"
   },
   "recommendationAccuracy": {
    "type": "string",
    "description": "Recommendation Accuracy"
   },
   "revenuePerformance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue Performance"
   },
   "drift": {
    "type": "string",
    "description": "Drift"
   },
   "confidenceExplanation": {
    "type": "string",
    "description": "Confidence → Explanation"
   }
  }
 },
 "CompetitorPricingMarketPositionIntelligenceView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Competitor Pricing & Market Position Intelligence displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "competitor": {
    "type": "string",
    "description": "Competitor"
   },
   "market": {
    "type": "string",
    "description": "Market"
   },
   "venueProduct": {
    "type": "string",
    "description": "Venue/Product"
   },
   "comparableTicvaiProduct": {
    "type": "string",
    "description": "Comparable TICVAI Product"
   },
   "source": {
    "type": "string",
    "description": "Source"
   },
   "currency": {
    "type": "string",
    "description": "Currency"
   },
   "collectionMethod": {
    "type": "string",
    "description": "Collection Method"
   },
   "refreshFrequency": {
    "type": "string",
    "description": "Refresh Frequency"
   },
   "reliability": {
    "type": "string",
    "description": "Reliability"
   },
   "publishedPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Published Price"
   },
   "promotionalPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Promotional Price"
   },
   "weekendPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Weekend Price"
   },
   "peakPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Peak Price"
   },
   "residentPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Resident Price"
   },
   "memberPriceWherePubliclyAvailable": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Member Price where publicly available"
   },
   "availability": {
    "type": "string",
    "description": "Availability"
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
   "against": {
    "type": "string",
    "description": "against"
   },
   "vipPremiumPackage": {
    "type": "string",
    "description": "VIP Premium Package"
   },
   "demand": {
    "type": "string",
    "description": "Demand"
   },
   "conversion": {
    "type": "number",
    "description": "Conversion"
   },
   "priceSensitivity": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price Sensitivity"
   }
  }
 },
 "InternalDemandBookingSignalHubView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Internal Demand & Booking Signal Hub displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "ticketsSold": {
    "type": "string",
    "description": "Tickets Sold"
   },
   "orders": {
    "type": "string",
    "description": "Orders"
   },
   "revenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue"
   },
   "averageSellingPrice": {
    "type": "number",
    "description": "Average Selling Price"
   },
   "conversionRate": {
    "type": "number",
    "description": "Conversion Rate"
   },
   "cartAbandonment": {
    "type": "string",
    "description": "Cart Abandonment"
   },
   "searchToPurchaseConversion": {
    "type": "number",
    "description": "Search-to-Purchase Conversion"
   },
   "capacity": {
    "type": "integer",
    "description": "Capacity"
   },
   "remainingInventory": {
    "type": "string",
    "description": "Remaining Inventory"
   },
   "availability": {
    "type": "string",
    "description": "Availability"
   },
   "occupancy": {
    "type": "integer",
    "description": "Occupancy"
   },
   "seatZoneAvailability": {
    "type": "string",
    "description": "Seat/Zone Availability"
   },
   "salesPerHour": {
    "type": "string",
    "description": "Sales per Hour"
   },
   "salesPerDay": {
    "type": "string",
    "description": "Sales per Day"
   },
   "bookingVelocity": {
    "type": "string",
    "description": "Booking Velocity"
   },
   "revenueVelocity": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue Velocity"
   },
   "accelerationDeceleration": {
    "type": "string",
    "description": "Acceleration/Deceleration"
   },
   "segment": {
    "type": "string",
    "description": "Segment"
   },
   "membership": {
    "type": "string",
    "description": "Membership"
   },
   "geography": {
    "type": "string",
    "description": "Geography"
   },
   "repeatPurchase": {
    "type": "string",
    "description": "Repeat Purchase"
   },
   "leadTime": {
    "type": "string",
    "format": "date-time",
    "description": "Lead Time"
   },
   "cancellation": {
    "type": "string",
    "description": "Cancellation"
   },
   "noShow": {
    "type": "string",
    "description": "No-Show"
   },
   "reschedule": {
    "type": "string",
    "description": "Reschedule"
   },
   "yesterday": {
    "type": "string",
    "description": "Yesterday"
   },
   "previousWeek": {
    "type": "string",
    "description": "Previous Week"
   },
   "sameDayLastYear": {
    "type": "string",
    "description": "Same Day Last Year"
   },
   "previousEvent": {
    "type": "string",
    "description": "Previous Event"
   },
   "similarEvent": {
    "type": "string",
    "description": "Similar Event"
   },
   "forecastBaseline": {
    "type": "string",
    "description": "Forecast Baseline"
   },
   "conversion": {
    "type": "number",
    "description": "Conversion (the pack shows +7.2%)"
   },
   "channelTimeslot": {
    "type": "string",
    "description": "Channel → Timeslot"
   }
  }
 },
 "MarketTourismHolidayContextualSignalHubView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Market, Tourism, Holiday & Contextual Signal Hub displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "publicHolidays": {
    "type": "string",
    "description": "Public Holidays"
   },
   "schoolHolidays": {
    "type": "string",
    "description": "School Holidays"
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
   "longWeekends": {
    "type": "string",
    "description": "Long Weekends"
   },
   "visitorArrivals": {
    "type": "string",
    "description": "Visitor Arrivals"
   },
   "tourismDemand": {
    "type": "string",
    "description": "Tourism Demand"
   },
   "hotelOccupancy": {
    "type": "integer",
    "description": "Hotel Occupancy"
   },
   "hotelRates": {
    "type": "string",
    "description": "Hotel Rates"
   },
   "destinationDemand": {
    "type": "string",
    "description": "Destination Demand"
   },
   "flightArrivals": {
    "type": "string",
    "description": "Flight Arrivals"
   },
   "airportPassengerVolume": {
    "type": "integer",
    "description": "Airport Passenger Volume"
   },
   "publicTransportDemand": {
    "type": "string",
    "description": "Public Transport Demand"
   },
   "trafficConditions": {
    "type": "string",
    "description": "Traffic Conditions"
   },
   "consumerDemandTrends": {
    "type": "string",
    "description": "Consumer Demand Trends"
   },
   "destinationPopularity": {
    "type": "string",
    "description": "Destination Popularity"
   },
   "marketActivity": {
    "type": "string",
    "description": "Market Activity"
   },
   "source": {
    "type": "string",
    "description": "Source"
   },
   "geography": {
    "type": "string",
    "description": "Geography"
   },
   "refreshFrequency": {
    "type": "string",
    "description": "Refresh Frequency"
   },
   "weight": {
    "type": "string",
    "description": "Weight"
   },
   "reliability": {
    "type": "string",
    "description": "Reliability"
   },
   "historicalCorrelation": {
    "type": "string",
    "description": "Historical Correlation"
   },
   "activeInactive": {
    "type": "integer",
    "description": "Active/Inactive"
   },
   "dubaiHotelOccupancy": {
    "type": "integer",
    "description": "Dubai Hotel Occupancy (the pack shows 92%)"
   },
   "venueDemand8": {
    "type": "number",
    "description": "Venue demand +8%"
   },
   "currentEstimatedImpact": {
    "type": "string",
    "description": "Current Estimated Impact (the pack shows +6%)"
   }
  }
 },
 "NearbyEventExhibitionLocalDemandIntelligenceView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Nearby Event, Exhibition & Local Demand Intelligence displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "exhibition": {
    "type": "string",
    "description": "Exhibition"
   },
   "conference": {
    "type": "string",
    "description": "Conference"
   },
   "concert": {
    "type": "string",
    "description": "Concert"
   },
   "sportsEvent": {
    "type": "string",
    "description": "Sports Event"
   },
   "festival": {
    "type": "string",
    "description": "Festival"
   },
   "tradeShow": {
    "type": "string",
    "description": "Trade Show"
   },
   "convention": {
    "type": "string",
    "description": "Convention"
   },
   "publicCelebration": {
    "type": "string",
    "description": "Public Celebration"
   },
   "majorAttractionEvent": {
    "type": "string",
    "description": "Major Attraction Event"
   },
   "schoolEvent": {
    "type": "string",
    "description": "School Event"
   },
   "customLocalEvent": {
    "type": "string",
    "description": "Custom Local Event"
   },
   "eventName": {
    "type": "string",
    "description": "Event Name"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "location": {
    "type": "string",
    "description": "Location"
   },
   "distanceFromTicvaiVenue": {
    "type": "string",
    "description": "Distance from TICVAI Venue"
   },
   "startEndDate": {
    "type": "string",
    "format": "date-time",
    "description": "Start/End Date"
   },
   "startEndTime": {
    "type": "string",
    "format": "date-time",
    "description": "Start/End Time"
   },
   "expectedAttendance": {
    "type": "integer",
    "description": "Expected Attendance"
   },
   "eventType": {
    "type": "string",
    "description": "Event Type"
   },
   "audienceType": {
    "type": "string",
    "description": "Audience Type"
   },
   "source": {
    "type": "string",
    "description": "Source"
   },
   "confidence": {
    "type": "string",
    "description": "Confidence"
   },
   "distance12Km": {
    "type": "string",
    "description": "Distance: 1.2 km"
   },
   "attendance60000": {
    "type": "integer",
    "description": "Attendance: 60,000"
   },
   "duration4Days": {
    "type": "string",
    "format": "date-time",
    "description": "Duration: 4 days"
   },
   "predictedImpact": {
    "type": "string",
    "description": "Predicted Impact (the pack shows +14–21%)"
   },
   "beforeEvent": {
    "type": "string",
    "description": "Before Event"
   },
   "duringEvent": {
    "type": "string",
    "description": "During Event"
   },
   "lunchPeriod": {
    "type": "string",
    "format": "date-time",
    "description": "Lunch Period"
   },
   "afterEvent": {
    "type": "string",
    "description": "After Event"
   },
   "evening": {
    "type": "string",
    "description": "Evening"
   },
   "followingDay": {
    "type": "string",
    "description": "Following Day"
   },
   "ticvaiEvents": {
    "type": "string",
    "description": "TICVAI Events"
   },
   "demandForecast": {
    "type": "string",
    "description": "Demand Forecast"
   },
   "occupancy": {
    "type": "integer",
    "description": "Occupancy"
   },
   "currentPricing": {
    "type": "string",
    "description": "Current Pricing"
   }
  }
 },
 "PriceElasticityRevenueResponseIntelligenceView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Price Elasticity & Revenue Response Intelligence displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "price": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price"
   },
   "demand": {
    "type": "string",
    "description": "Demand"
   },
   "conversion": {
    "type": "number",
    "description": "Conversion"
   },
   "revenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue"
   },
   "margin": {
    "type": "number",
    "description": "Margin"
   },
   "occupancy": {
    "type": "integer",
    "description": "Occupancy"
   },
   "customerSegment": {
    "type": "string",
    "description": "Customer Segment"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "time": {
    "type": "string",
    "format": "date-time",
    "description": "Time"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "elasticityConfidenceLow": {
    "type": "number",
    "description": "Elasticity Confidence: Low"
   }
  }
 },
 "WeatherIntelligenceDemandImpactConfigurationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Weather Intelligence & Demand Impact Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "temperature": {
    "type": "string",
    "description": "Temperature"
   },
   "feelsLikeTemperature": {
    "type": "string",
    "description": "Feels-Like Temperature"
   },
   "rain": {
    "type": "string",
    "description": "Rain"
   },
   "rainProbability": {
    "type": "string",
    "description": "Rain Probability"
   },
   "humidity": {
    "type": "string",
    "description": "Humidity"
   },
   "wind": {
    "type": "string",
    "description": "Wind"
   },
   "visibility": {
    "type": "string",
    "description": "Visibility"
   },
   "storm": {
    "type": "string",
    "description": "Storm"
   },
   "extremeHeat": {
    "type": "string",
    "description": "Extreme Heat"
   },
   "airQualityWhereAvailable": {
    "type": "string",
    "description": "Air Quality where available"
   },
   "currentConditions": {
    "type": "string",
    "description": "Current Conditions"
   },
   "hourlyForecast": {
    "type": "string",
    "description": "Hourly Forecast"
   },
   "dailyForecast": {
    "type": "string",
    "description": "Daily Forecast"
   },
   "today": {
    "type": "string",
    "description": "Today"
   },
   "configurableFutureWindow": {
    "type": "string",
    "format": "date-time",
    "description": "Configurable Future Window"
   },
   "andWeatherSensitivity": {
    "type": "string",
    "description": "and weather sensitivity"
   },
   "extremeHeatNegative": {
    "type": "string",
    "description": "Extreme Heat → Negative"
   },
   "extremeHeatPotentialPositive": {
    "type": "string",
    "description": "Extreme Heat → Potential Positive"
   },
   "highTemperaturePositive": {
    "type": "string",
    "description": "High Temperature → Positive"
   },
   "heavyRainStrongNegative": {
    "type": "string",
    "description": "Heavy Rain → Strong Negative"
   },
   "demandImpact8": {
    "type": "number",
    "description": "Demand Impact +8%"
   },
   "demandImpact17": {
    "type": "number",
    "description": "Demand Impact −17%"
   },
   "weatherForecastConfidence93": {
    "type": "number",
    "description": "Weather Forecast Confidence: 93%"
   },
   "estimatedDemandImpact812": {
    "type": "number",
    "description": "Estimated Demand Impact: +8–12%"
   }
  }
 }
}
```
