# WS39 — Pricing   Revenue Management board 6

**10 screens · 12 operations · 15 schemas · 3 permissions**

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
  `AI_CONFIGURE, PRICE_CONFIGURE, PRODUCT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-098` | AI Pricing Intelligence Command Center | commandCentre | 1 | 0 | — |
| `ADM-099` | Internal Demand & Booking Signal Hub | listDetail | 1 | 0 | — |
| `ADM-100` | Weather Intelligence & Demand Impact Configuration | commandCentre | 2 | 1 | — |
| `ADM-101` | Nearby Event, Exhibition & Local Demand Intelligence | configEditor | 2 | 1 | — |
| `ADM-102` | Competitor Pricing & Market Position Intelligence | listDetail | 2 | 1 | — |
| `ADM-103` | Market, Tourism, Holiday & Contextual Signal Hub | listDetail | 2 | 1 | — |
| `ADM-104` | AI Demand Forecasting & Booking Curve Studio | listDetail | 1 | 0 | — |
| `ADM-105` | Price Elasticity & Revenue Response Intelligence | listDetail | 1 | 0 | — |
| `ADM-106` | AI Pricing Recommendation & Explainability Center | listDetail | 1 | 0 | — |
| `ADM-107` | AI Signal Registry, Data Quality & Model Governance | listDetail | 2 | 1 | — |

## Thin screens in this batch

**ADM-099, ADM-102, ADM-103, ADM-104, ADM-105, ADM-106 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

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
     "provenance": "derived — ADM-002 declares entryState.params  and ADM-098 holds none of them, so the edge carries nothing and ADM-002 opens cold"
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
  "purposeNote": "Revenue teams can understand all significant AI pricing opportunities, risks, forecasts and external demand drivers from one centralized intelligence workspace.",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each opportunity displays) — counts over a population, then the population",
  "purpose": "Provide Revenue Managers with a single operational view of all AI signals, forecasts, opportunities and risks influencing pricing.",
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
       "bindsTo": "AiPricingIntelligenceCommandCenterSummary.activeAiRecommendations"
      },
      {
       "kind": "metricTile",
       "label": "High-Priority Opportunities",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 94 §Display",
       "bindsTo": "AiPricingIntelligenceCommandCenterSummary.highPriorityOpportunities"
      },
      {
       "kind": "metricTile",
       "label": "Estimated Revenue Opportunity",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 94 §Display",
       "bindsTo": "AiPricingIntelligenceCommandCenterSummary.estimatedRevenueOpportunity"
      },
      {
       "kind": "metricTile",
       "label": "Demand Surges Detected",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 94 §Display",
       "bindsTo": "AiPricingIntelligenceCommandCenterSummary.demandSurgesDetected"
      },
      {
       "kind": "metricTile",
       "label": "Demand Risks Detected",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 94 §Display",
       "bindsTo": "AiPricingIntelligenceCommandCenterSummary.demandRisksDetected"
      },
      {
       "kind": "metricTile",
       "label": "External Signals Active",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 94 §Display",
       "bindsTo": "AiPricingIntelligenceCommandCenterSummary.externalSignalsActive"
      },
      {
       "kind": "metricTile",
       "label": "Nearby Events Detected",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 94 §Display",
       "bindsTo": "AiPricingIntelligenceCommandCenterSummary.nearbyEventsDetected"
      },
      {
       "kind": "metricTile",
       "label": "Weather Impacts",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 94 §Display",
       "bindsTo": "AiPricingIntelligenceCommandCenterSummary.weatherImpacts"
      },
      {
       "kind": "metricTile",
       "label": "Competitor Movements",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 94 §Display",
       "bindsTo": "AiPricingIntelligenceCommandCenterSummary.competitorMovements"
      },
      {
       "kind": "metricTile",
       "label": "Forecast Accuracy",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 94 §Display",
       "bindsTo": "AiPricingIntelligenceCommandCenterSummary.forecastAccuracy"
      },
      {
       "kind": "metricTile",
       "label": "Average AI Confidence",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 94 §Display",
       "bindsTo": "AiPricingIntelligenceCommandCenterSummary.averageAiConfidence"
      },
      {
       "kind": "metricTile",
       "label": "Data Quality Issues",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 94 §Display",
       "bindsTo": "AiPricingIntelligenceCommandCenterSummary.dataQualityIssues"
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-098",
   "workshopBoard": "wireframes/WS100 Pricing   Revenue Management Board 6.dc.html#adm-098"
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
  "purposeNote": "pricing intelligence.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Centralize the internal TICVAI signals used by forecasting and AI pricing models. These are generally the highest-confidence signals because they come directly from TICVAI transactions.",
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-099",
   "workshopBoard": "wireframes/WS100 Pricing   Revenue Management Board 6.dc.html#adm-099"
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
  "purposeNote": "Weather conditions are converted into venue-specific, explainable demand signals rather than directly changing prices.",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Show) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Allow TICVAI to understand how weather conditions affect demand for different venues and experiences. This should be much more sophisticated than simply connecting a weather API.",
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
       "bindsTo": "WeatherIntelligenceDemandImpactConfigurationView.weatherForecastConfidence"
      },
      {
       "kind": "metricTile",
       "label": "Estimated Demand Impact: +8–12%",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 97 §Show",
       "bindsTo": "WeatherIntelligenceDemandImpactConfigurationView.estimatedDemandImpactMin"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Hourly Forecast",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 97 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Daily Forecast",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 97 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Save demand signal configuration",
       "operation": "setDemandSignalConfiguration",
       "permission": "PRICE_CONFIGURE",
       "notes": "**The person's half of `catalogue.demand_signal`** (29 September, writers pass).",
       "provenance": "contract catalogue.yaml PUT /demand-signals/{signalId}"
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
   },
   {
    "operationId": "setDemandSignalConfiguration",
    "contract": "catalogue",
    "purpose": "Enter a calendar signal or configure how a demand signal is used",
    "trigger": "onAction",
    "invalidates": [
     "listWeatherDemandImpact"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "WeatherIntelligenceDemandImpactConfigurationView.weatherForecastConfidence",
    "WeatherIntelligenceDemandImpactConfigurationView.estimatedDemandImpactMin"
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-100",
   "workshopBoard": "wireframes/WS100 Pricing   Revenue Management Board 6.dc.html#adm-100"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 97. 2 of 2 labels bound to a contract property; 4 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "purposeNote": "impact signals for AI pricing decisions.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Detect/configure; Capture; Configure per TICVAI venue) and no display directory — it is settings, not a population",
  "purpose": "Detect external events around TICVAI venues that could materially affect visitor demand. This directly addresses the exhibition-near-the-venue scenario.",
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
   },
   {
    "operationId": "setDemandSignalConfiguration",
    "contract": "catalogue",
    "purpose": "Enter a calendar signal or configure how a demand signal is used",
    "trigger": "onAction",
    "invalidates": [
     "listNearbyEventExhibition"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-101",
   "workshopBoard": "wireframes/WS100 Pricing   Revenue Management Board 6.dc.html#adm-101"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 99. 0 of 0 labels bound to a contract property; 22 of 47 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "entryState": {
   "params": [
    {
     "name": "signalId",
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
  "purposeNote": "competitor data alone to determine the selling price.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Track) and no metric row",
  "purpose": "Allow TICVAI to understand its commercial position relative to relevant competitors.",
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
   },
   {
    "operationId": "setDemandSignalConfiguration",
    "contract": "catalogue",
    "purpose": "Enter a calendar signal or configure how a demand signal is used",
    "trigger": "onAction",
    "invalidates": [
     "listCompetitorPricingMarket"
    ]
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-102",
   "workshopBoard": "wireframes/WS100 Pricing   Revenue Management Board 6.dc.html#adm-102"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 100. 9 of 9 labels bound to a contract property; 18 of 30 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "purposeNote": "demand-intelligence layer.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Capture broader external factors that may affect visitor demand beyond weather and nearby events.",
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
   },
   {
    "operationId": "setDemandSignalConfiguration",
    "contract": "catalogue",
    "purpose": "Enter a calendar signal or configure how a demand signal is used",
    "trigger": "onAction",
    "invalidates": [
     "listMarketTourismHoliday"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "MarketTourismHolidayContextualSignalHubView.signalType"
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-103",
   "workshopBoard": "wireframes/WS100 Pricing   Revenue Management Board 6.dc.html#adm-103"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 102. 0 of 0 labels bound to a contract property; 0 of 38 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "purposeNote": "approved external signals.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display; Track) and no metric row",
  "purpose": "Predict future demand at a granular commercial level. This is the core predictive engine behind intelligent dynamic pricing.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Event Horizon. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 103 §Support"
   },
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
        "AiDemandForecastingBookingCurveStudioView.confidence",
        "AiDemandForecastingBookingCurveStudioView.confidenceReasons",
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
        "AiDemandForecastingBookingCurveStudioView.confidence",
        "AiDemandForecastingBookingCurveStudioView.confidenceReasons",
        "AiDemandForecastingBookingCurveStudioView.mape",
        "AiDemandForecastingBookingCurveStudioView.forecastBias",
        "AiDemandForecastingBookingCurveStudioView.overForecast",
        "AiDemandForecastingBookingCurveStudioView.underForecast"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Historical Expected Curve”, “Current Actual Curve”, “Saturday Performance”, “Actual”, “Provide”, “Clearly show which signals contributed”.",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 103 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Event Horizon",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 103 §Support"
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
    "AiDemandForecastingBookingCurveStudioView.confidence",
    "AiDemandForecastingBookingCurveStudioView.confidenceReasons",
    "AiDemandForecastingBookingCurveStudioView.mape",
    "AiDemandForecastingBookingCurveStudioView.forecastBias"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-104",
   "workshopBoard": "wireframes/WS100 Pricing   Revenue Management Board 6.dc.html#adm-104"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 103. 8 of 8 labels bound to a contract property; 9 of 48 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "purposeNote": "visible confidence and supporting evidence.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Analyze) and no metric row",
  "purpose": "Estimate how customers are likely to respond to different prices.",
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-105",
   "workshopBoard": "wireframes/WS100 Pricing   Revenue Management Board 6.dc.html#adm-105"
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
  "purposeNote": "Every AI pricing recommendation is accompanied by understandable evidence, expected commercial impact, confidence and human-governance actions.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Convert all intelligence generated by Board 6 into actionable pricing recommendations. This is the central AI recommendation screen.",
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
    "AiPricingRecommendationExplainabilityCenterView.drivers"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-106",
   "workshopBoard": "wireframes/WS100 Pricing   Revenue Management Board 6.dc.html#adm-106"
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
  "purposeNote": "signals and predictive models used by AI pricing. Board 6 — Final Screen Register # Backend Screen Core Responsibility 10.6. AI Pricing Intelligence Command Center AI opportunity overview 1 10.6. TICVAI transactional Internal Demand & Booking Signal Hub 2 intelligence 10.6. Weather Intelligence & Demand Impact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display; Monitor; Track) and no metric row",
  "purpose": "Govern the complete data and intelligence ecosystem behind AI pricing. This is critical. Without this screen, Development team could connect many external sources without giving TICVAI proper control over them.",
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
      },
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
   },
   {
    "operationId": "setSignalRegistryPolicy",
    "contract": "catalogue",
    "purpose": "Register a signal or model and set how far AI may trust it",
    "trigger": "onAction",
    "invalidates": [
     "listSignalDataQuality"
    ]
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-107",
   "workshopBoard": "wireframes/WS100 Pricing   Revenue Management Board 6.dc.html#adm-107"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 108. 23 of 24 labels bound to a contract property; 32 of 121 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "listCompetitorPricingMarket": {
  "method": "GET",
  "path": "/competitor-pricing-market",
  "contract": "catalogue",
  "summary": "Competitor Pricing & Market Position Intelligence",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "competitor",
    "in": "query",
    "required": false
   },
   {
    "name": "market",
    "in": "query",
    "required": false
   },
   {
    "name": "comparableTicvaiProduct",
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
 "listDemandBookingCurve": {
  "method": "GET",
  "path": "/demand-booking-curve",
  "contract": "catalogue",
  "summary": "AI Demand Forecasting & Booking Curve Studio",
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
    "name": "product",
    "in": "query",
    "required": false
   },
   {
    "name": "event",
    "in": "query",
    "required": false
   },
   {
    "name": "performance",
    "in": "query",
    "required": false
   },
   {
    "name": "channel",
    "in": "query",
    "required": false
   },
   {
    "name": "horizon",
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
    "name": "priceCategory",
    "in": "query",
    "required": false
   },
   {
    "name": "sectionCode",
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
 "listInternalDemandBooking": {
  "method": "GET",
  "path": "/internal-demand-booking",
  "contract": "catalogue",
  "summary": "Internal Demand & Booking Signal Hub",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "granularity",
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
    "name": "performance",
    "in": "query",
    "required": false
   },
   {
    "name": "product",
    "in": "query",
    "required": false
   },
   {
    "name": "channel",
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
    "name": "compareTo",
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
 "listMarketTourismHoliday": {
  "method": "GET",
  "path": "/market-tourism-holiday",
  "contract": "catalogue",
  "summary": "Market, Tourism, Holiday & Contextual Signal Hub",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "category",
    "in": "query",
    "required": false
   },
   {
    "name": "signalType",
    "in": "query",
    "required": false
   },
   {
    "name": "geography",
    "in": "query",
    "required": false
   },
   {
    "name": "active",
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
 "listNearbyEventExhibition": {
  "method": "GET",
  "path": "/nearby-event-exhibition",
  "contract": "catalogue",
  "summary": "Nearby Event, Exhibition & Local Demand Intelligence",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "ticvaiVenue",
    "in": "query",
    "required": false
   },
   {
    "name": "eventType",
    "in": "query",
    "required": false
   },
   {
    "name": "radiusKm",
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
   },
   {
    "name": "product",
    "in": "query",
    "required": false
   },
   {
    "name": "customerSegment",
    "in": "query",
    "required": false
   },
   {
    "name": "channel",
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
 "listPricing": {
  "method": "GET",
  "path": "/pricing",
  "contract": "catalogue",
  "summary": "AI Pricing Intelligence Command Center",
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
    "name": "urgency",
    "in": "query",
    "required": false
   },
   {
    "name": "risk",
    "in": "query",
    "required": false
   },
   {
    "name": "minConfidence",
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
 "listPricingRecommendationExplainability": {
  "method": "GET",
  "path": "/pricing-recommendation-explainability",
  "contract": "catalogue",
  "summary": "AI Pricing Recommendation & Explainability Center",
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
    "name": "reviewOutcome",
    "in": "query",
    "required": false
   },
   {
    "name": "minConfidence",
    "in": "query",
    "required": false
   },
   {
    "name": "recommendationType",
    "in": "query",
    "required": false
   },
   {
    "name": "objective",
    "in": "query",
    "required": false
   },
   {
    "name": "priceCategory",
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
 "listSignalDataQuality": {
  "method": "GET",
  "path": "/signal-data-quality",
  "contract": "catalogue",
  "summary": "AI Signal Registry, Data Quality & Model Governance",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "registryKind",
    "in": "query",
    "required": false
   },
   {
    "name": "internalExternal",
    "in": "query",
    "required": false
   },
   {
    "name": "trustLevel",
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
 "listWeatherDemandImpact": {
  "method": "GET",
  "path": "/weather-demand-impact",
  "contract": "catalogue",
  "summary": "Weather Intelligence & Demand Impact Configuration",
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
    "name": "venueExposure",
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
 "AiDemandForecastingBookingCurveStudioView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What AI Demand Forecasting & Booking Curve Studio displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "venue": {
    "type": "string",
    "description": "Venue id"
   },
   "product": {
    "type": "string",
    "description": "Product id",
    "nullable": true
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
   "date": {
    "type": "string",
    "description": "Date",
    "format": "date"
   },
   "timeslot": {
    "type": "string",
    "description": "Timeslot",
    "nullable": true
   },
   "priceCategory": {
    "type": "string",
    "description": "Price category",
    "nullable": true
   },
   "sectionCode": {
    "type": "string",
    "nullable": true,
    "description": "Seat-map section (`seating.Section.code`) the row forecasts; null for a row at price-category or performance level (29 September, build pass, group G2; 21.11.4)"
   },
   "channel": {
    "$ref": "#/components/schemas/Channel",
    "description": "Channel"
   },
   "confidence": {
    "type": "number",
    "description": "Forecast Confidence, percent"
   },
   "forecastFinalOccupancy": {
    "type": "number",
    "description": "Forecast Final Occupancy, percent"
   },
   "demand": {
    "type": "integer",
    "description": "Forecast demand"
   },
   "attendance": {
    "type": "integer",
    "description": "Forecast attendance"
   },
   "occupancy": {
    "type": "number",
    "description": "Forecast occupancy, percent"
   },
   "sellThrough": {
    "type": "number",
    "description": "Forecast sell-through, percent"
   },
   "expectedSellOutTime": {
    "type": "string",
    "description": "Expected Sell-Out Time; empty if no sell-out forecast",
    "format": "date-time",
    "nullable": true
   },
   "revenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Forecast revenue"
   },
   "conversion": {
    "type": "number",
    "description": "Forecast conversion, percent"
   },
   "remainingInventory": {
    "type": "integer",
    "description": "Forecast remaining inventory at event"
   },
   "mape": {
    "type": "number",
    "description": "MAPE over closed forecasts at this level, percent"
   },
   "forecastBias": {
    "type": "number",
    "description": "Forecast Bias (positive = over-forecast), percent"
   },
   "overForecast": {
    "type": "number",
    "description": "Share of closed forecasts that over-forecast, percent"
   },
   "underForecast": {
    "type": "number",
    "description": "Share of closed forecasts that under-forecast, percent"
   },
   "forecastId": {
    "type": "string",
    "description": "Forecast id"
   },
   "horizon": {
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
   "bookingCurve": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "daysBeforeEvent": {
       "type": "integer",
       "description": "T minus days"
      },
      "historicalExpectedPercentSold": {
       "type": "number",
       "description": "Historical expected curve, percent sold"
      },
      "actualPercentSold": {
       "type": "number",
       "nullable": true,
       "description": "Current actual curve, percent sold (empty for future points)"
      },
      "forecastPercentSold": {
       "type": "number",
       "description": "AI forecast curve, percent sold"
      }
     }
    },
    "description": "Booking Curve"
   },
   "signalContributions": {
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
       "description": "Signal category"
      },
      "contributionPercent": {
       "type": "number",
       "description": "Explanatory share of the forecast"
      }
     }
    },
    "description": "Model Inputs: which signals contributed"
   },
   "confidenceReasons": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "strongHistoricalData",
      "stableBookingPattern",
      "reliableExternalSignals",
      "limitedHistoricalData",
      "volatileBookingPattern",
      "degradedExternalSignals"
     ]
    },
    "description": "Reasons behind the forecast confidence"
   },
   "modelVersion": {
    "type": "string",
    "description": "Model version that produced the forecast"
   },
   "generatedAt": {
    "type": "string",
    "description": "When the forecast was produced",
    "format": "date-time"
   }
  }
 },
 "AiPricingIntelligenceCommandCenterSummary": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection; the headline tiles over the list, computed at read time for the filters in force",
  "description": "**The headline figures on AI Pricing Intelligence Command Center.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.",
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
    "type": "integer",
    "description": "Demand Surges Detected: granules forecast materially above baseline"
   },
   "demandRisksDetected": {
    "type": "integer",
    "description": "Demand Risks Detected: granules forecast materially below baseline"
   },
   "externalSignalsActive": {
    "type": "integer",
    "description": "External Signals Active"
   },
   "nearbyEventsDetected": {
    "type": "integer",
    "description": "Nearby Events Detected within the configured monitoring radius"
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
    "type": "number",
    "description": "Forecast Accuracy (100 - MAPE over the last 30 days (decided 29 September, readiness close-out)), percent"
   },
   "averageAiConfidence": {
    "type": "number",
    "description": "Average AI Confidence across active recommendations, percent"
   },
   "dataQualityIssues": {
    "type": "integer",
    "description": "Data Quality Issues"
   },
   "aiSummary": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "AI Summary (pack p.95), e.g. demand forecast 19% above baseline and its drivers. Advisory only: generated narrative never changes a price (decided 29 September, readiness close-out)"
   }
  }
 },
 "AiPricingIntelligenceCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What AI Pricing Intelligence Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "productEvent": {
    "type": "string",
    "description": "Product/Event name the opportunity applies to"
   },
   "venue": {
    "type": "string",
    "description": "Venue name"
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
    "description": "Adjustment % from current to recommended price, percent"
   },
   "demandForecast": {
    "type": "integer",
    "description": "Demand Forecast: forecast demand (admissions) for the period"
   },
   "revenueOpportunity": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue Opportunity"
   },
   "confidence": {
    "type": "number",
    "description": "AI confidence in the recommendation, 0-100, percent"
   },
   "risk": {
    "type": "string",
    "description": "Risk of acting on the recommendation",
    "enum": [
     "low",
     "medium",
     "high"
    ]
   },
   "urgency": {
    "type": "string",
    "description": "Urgency (time to event and velocity)",
    "enum": [
     "low",
     "medium",
     "high",
     "critical"
    ]
   },
   "recommendationId": {
    "type": "string",
    "description": "Recommendation id; drill-down key into listPricingRecommendationExplainability"
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
    "description": "Expected Revenue Impact"
   },
   "expectedOccupancy": {
    "type": "number",
    "description": "Expected Occupancy, percent"
   },
   "confidence": {
    "type": "number",
    "description": "Overall confidence, percent"
   },
   "recommendationId": {
    "type": "string",
    "description": "Recommendation id"
   },
   "productEvent": {
    "type": "string",
    "description": "Product/event/performance the card applies to"
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
    "description": "AI Recommended Price"
   },
   "adjustmentPercent": {
    "type": "number",
    "description": "Change from current price, percent"
   },
   "demandImpact": {
    "type": "number",
    "description": "Demand Impact, percent"
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
        "conversionRate",
        "other"
       ],
       "description": "Signal category behind the driver; `conversionRate` (carts reaching the price against orders placed) added 29 September for `objective` `conversion` (build pass, group G2; 8.5.37)"
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
   "counterfactuals": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "condition": {
       "type": "string",
       "description": "e.g. if the nearby exhibition were not occurring"
      },
      "recommendedPrice": {
       "$ref": "../shared/common.yaml#/components/schemas/Money",
       "description": "Price the model would recommend then"
      }
     }
    },
    "description": "Counterfactual Explanation"
   },
   "confidenceBreakdown": {
    "type": "object",
    "properties": {
     "dataQuality": {
      "type": "number",
      "description": "Data Quality, percent"
     },
     "forecastConfidence": {
      "type": "number",
      "description": "Forecast Confidence, percent"
     },
     "elasticityConfidence": {
      "type": "number",
      "description": "Elasticity Confidence, percent"
     },
     "externalSignalConfidence": {
      "type": "number",
      "description": "External Signal Confidence, percent"
     }
    },
    "description": "Confidence Breakdown"
   },
   "explanation": {
    "type": "string",
    "description": "Natural-language explanation in business language (advisory)",
    "nullable": true
   },
   "reviewOutcome": {
    "type": "string",
    "description": "Where the human decision on the card stands; every card starts pending (decided 29 September, readiness close-out)",
    "enum": [
     "pending",
     "accepted",
     "rejected",
     "modified",
     "ignored",
     "sentToSimulation",
     "sentForApproval"
    ]
   },
   "modelVersion": {
    "type": "string",
    "description": "Model version (auditability chain)"
   },
   "generatedAt": {
    "type": "string",
    "description": "When the recommendation was generated",
    "format": "date-time"
   },
   "priceCategoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The price (seat) category the card is for, `PricingRecommendation.priceCategoryId`; null for a product priced without categories (29 September, build pass, group G2; 1.4.27)"
   },
   "priceCategory": {
    "type": "string",
    "nullable": true,
    "description": "The price category's name, for the card"
   },
   "recommendationType": {
    "type": "string",
    "enum": [
     "standard",
     "earlyBird",
     "lastMinute",
     "volumeDiscount",
     "conversion"
    ],
    "description": "`PricingRecommendation.recommendationType` (29 September, build pass, group G2; 8.5.31 to 8.5.33, 8.5.37)"
   },
   "validFrom": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "validTo": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "quantityTier": {
    "type": "object",
    "nullable": true,
    "properties": {
     "minQuantity": {
      "type": "integer"
     },
     "maxQuantity": {
      "type": "integer",
      "nullable": true
     }
    }
   },
   "objective": {
    "type": "string",
    "enum": [
     "revenue",
     "occupancy",
     "conversion"
    ]
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
    "description": "Signal name (signal rows)",
    "nullable": true
   },
   "category": {
    "type": "string",
    "description": "Category",
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
     "other"
    ]
   },
   "provider": {
    "type": "string",
    "description": "Provider name (vendor-neutral, data)",
    "nullable": true
   },
   "source": {
    "type": "string",
    "description": "Source / feed name",
    "nullable": true
   },
   "internalExternal": {
    "type": "string",
    "description": "Internal/External",
    "enum": [
     "internal",
     "external"
    ]
   },
   "market": {
    "type": "string",
    "description": "Market",
    "nullable": true
   },
   "refreshFrequency": {
    "type": "string",
    "description": "Refresh Frequency",
    "enum": [
     "realTime",
     "minutes10",
     "hourly",
     "daily",
     "weekly",
     "manual"
    ]
   },
   "lastUpdate": {
    "type": "string",
    "description": "Last Update",
    "format": "date-time",
    "nullable": true
   },
   "freshness": {
    "type": "string",
    "description": "Freshness, e.g. live, 10 min, 8 hr",
    "nullable": true
   },
   "reliability": {
    "type": "number",
    "description": "Reliability, percent"
   },
   "historicalCorrelation": {
    "type": "number",
    "description": "Historical correlation with demand, -1..1",
    "nullable": true
   },
   "status": {
    "type": "string",
    "description": "Status: healthy, delayed, failed or disabled for signals; candidate, validation, approved, production, monitored or retired for models"
   },
   "missingData": {
    "type": "integer",
    "description": "Missing Data issues in the last 24 hours"
   },
   "delayedData": {
    "type": "integer",
    "description": "Delayed Data issues in the last 24 hours"
   },
   "outliers": {
    "type": "integer",
    "description": "Outliers in the last 24 hours"
   },
   "invalidValues": {
    "type": "integer",
    "description": "Invalid Values in the last 24 hours"
   },
   "unexpectedChanges": {
    "type": "integer",
    "description": "Unexpected Changes in the last 24 hours"
   },
   "sourceFailure": {
    "type": "integer",
    "description": "Source Failures in the last 24 hours"
   },
   "modelName": {
    "type": "string",
    "description": "Model Name (model rows)",
    "nullable": true
   },
   "version": {
    "type": "string",
    "description": "Version (model rows)",
    "nullable": true
   },
   "purpose": {
    "type": "string",
    "description": "Purpose (model rows)",
    "nullable": true
   },
   "deploymentDate": {
    "type": "string",
    "description": "Deployment Date",
    "format": "date",
    "nullable": true
   },
   "trainingWindow": {
    "type": "string",
    "description": "Training Window, e.g. 24 months to 2026-08-31",
    "nullable": true
   },
   "validationResult": {
    "type": "string",
    "description": "Validation Result summary",
    "nullable": true
   },
   "owner": {
    "type": "string",
    "description": "Owner (user id)",
    "nullable": true
   },
   "forecastAccuracy": {
    "type": "number",
    "description": "Forecast Accuracy, percent"
   },
   "bias": {
    "type": "number",
    "description": "Bias, percent"
   },
   "recommendationAccuracy": {
    "type": "number",
    "description": "Recommendation Accuracy, percent"
   },
   "revenuePerformance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue Performance attributed to the model's accepted recommendations"
   },
   "drift": {
    "type": "number",
    "description": "Drift: change in accuracy over the last 30 days, percent"
   },
   "registryId": {
    "type": "string",
    "description": "Registry entry id"
   },
   "registryKind": {
    "type": "string",
    "description": "Signal or model row",
    "enum": [
     "signal",
     "model"
    ]
   },
   "duplicateData": {
    "type": "integer",
    "description": "Duplicate Data issues in the last 24 hours"
   },
   "trustLevel": {
    "type": "string",
    "description": "Signal Trust; external signals default advisoryOnly (decided 29 September, readiness close-out)",
    "enum": [
     "approved",
     "experimental",
     "advisoryOnly",
     "blocked"
    ]
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
    },
    "description": "AI Use Permission; automatedPricing is never granted by default (decided 29 September, readiness close-out)"
   },
   "fallbackPolicy": {
    "type": "string",
    "description": "Fallback Policy; default reduceConfidence (decided 29 September, readiness close-out)",
    "enum": [
     "useHistoricalValue",
     "ignore",
     "substitute",
     "reduceConfidence",
     "stopAiRecommendation"
    ]
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
 "CompetitorPricingMarketPositionIntelligenceView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Competitor Pricing & Market Position Intelligence displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "competitor": {
    "type": "string",
    "description": "Competitor name"
   },
   "market": {
    "type": "string",
    "description": "Market"
   },
   "venueProduct": {
    "type": "string",
    "description": "Competitor venue/product"
   },
   "comparableTicvaiProduct": {
    "type": "string",
    "description": "Comparable TICVAI product id"
   },
   "source": {
    "type": "string",
    "description": "Source name (vendor-neutral: website, feed or partner, as data)"
   },
   "currency": {
    "type": "string",
    "description": "Currency, ISO 4217"
   },
   "collectionMethod": {
    "type": "string",
    "description": "Collection Method (decided 29 September, readiness close-out)",
    "enum": [
     "manualEntry",
     "dataFeed",
     "publishedWebsite",
     "partnerSupplied"
    ]
   },
   "refreshFrequency": {
    "type": "string",
    "description": "Refresh Frequency",
    "enum": [
     "realTime",
     "hourly",
     "daily",
     "weekly",
     "manual"
    ]
   },
   "reliability": {
    "type": "number",
    "description": "Reliability of the source, percent"
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
    "description": "Availability as published",
    "enum": [
     "available",
     "limited",
     "soldOut",
     "unknown"
    ]
   },
   "date": {
    "type": "string",
    "description": "Date the price applies to",
    "format": "date"
   },
   "timeslot": {
    "type": "string",
    "description": "Timeslot",
    "nullable": true
   },
   "observationId": {
    "type": "string",
    "description": "Observation id"
   },
   "observedAt": {
    "type": "string",
    "description": "When the price was collected",
    "format": "date-time"
   },
   "marketMedianPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Market median price for the comparable set"
   },
   "positionVsMedian": {
    "type": "number",
    "description": "TICVAI position against the market median (-9.1 = below), percent"
   },
   "movementPercent": {
    "type": "number",
    "description": "Competitor Movement: change against the previous observation, percent"
   },
   "historicalCorrelation": {
    "type": "object",
    "properties": {
     "demand": {
      "type": "number",
      "description": "Correlation with TICVAI demand, -1..1"
     },
     "conversion": {
      "type": "number",
      "description": "Correlation with TICVAI conversion, -1..1"
     },
     "priceSensitivity": {
      "type": "number",
      "description": "Correlation with TICVAI price sensitivity, -1..1"
     }
    },
    "description": "Historical Correlation of competitor changes with TICVAI outcomes"
   },
   "comparabilityApproved": {
    "type": "boolean",
    "description": "An administrator confirmed the products are genuinely comparable"
   },
   "sourceApproved": {
    "type": "boolean",
    "description": "Source approved as legally permissible; unapproved sources are ignored by AI"
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
 "InternalDemandBookingSignalHubView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Internal Demand & Booking Signal Hub displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "ticketsSold": {
    "type": "integer",
    "description": "Tickets Sold"
   },
   "orders": {
    "type": "integer",
    "description": "Orders"
   },
   "revenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue"
   },
   "averageSellingPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Average Selling Price"
   },
   "conversionRate": {
    "type": "number",
    "description": "Conversion Rate, percent"
   },
   "cartAbandonment": {
    "type": "number",
    "description": "Cart Abandonment rate, percent"
   },
   "searchToPurchaseConversion": {
    "type": "number",
    "description": "Search-to-Purchase Conversion, percent"
   },
   "capacity": {
    "type": "integer",
    "description": "Capacity"
   },
   "remainingInventory": {
    "type": "integer",
    "description": "Remaining Inventory (units)"
   },
   "availability": {
    "type": "number",
    "description": "Availability: remaining inventory as a share of capacity, percent"
   },
   "occupancy": {
    "type": "number",
    "description": "Occupancy, percent"
   },
   "seatZoneAvailability": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "zone": {
       "type": "string",
       "description": "Seat zone / section"
      },
      "available": {
       "type": "integer",
       "description": "Seats available"
      }
     }
    },
    "description": "Seat/Zone Availability; empty for unseated products"
   },
   "salesPerHour": {
    "type": "number",
    "description": "Sales per Hour (tickets)"
   },
   "salesPerDay": {
    "type": "number",
    "description": "Sales per Day (tickets)"
   },
   "bookingVelocity": {
    "type": "number",
    "description": "Booking Velocity against forecast (+31 = 31% above), percent"
   },
   "revenueVelocity": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue Velocity: revenue per hour over the last hour"
   },
   "accelerationDeceleration": {
    "type": "number",
    "description": "Acceleration/Deceleration: change in booking velocity against the previous window, percent"
   },
   "repeatPurchase": {
    "type": "number",
    "description": "Repeat Purchase rate, percent"
   },
   "leadTime": {
    "type": "number",
    "description": "Lead Time: average days between purchase and visit"
   },
   "cancellation": {
    "type": "integer",
    "description": "Cancellations"
   },
   "noShow": {
    "type": "integer",
    "description": "No-Shows"
   },
   "reschedule": {
    "type": "integer",
    "description": "Reschedules"
   },
   "granularity": {
    "type": "string",
    "description": "Level of this row in the signal granularity hierarchy (pack p.97)",
    "enum": [
     "tenant",
     "market",
     "venue",
     "event",
     "performance",
     "product",
     "priceCategory",
     "channel",
     "timeslot"
    ]
   },
   "venue": {
    "type": "string",
    "description": "Venue id"
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
   "product": {
    "type": "string",
    "description": "Product id",
    "nullable": true
   },
   "priceCategory": {
    "type": "string",
    "description": "Price category",
    "nullable": true
   },
   "channel": {
    "$ref": "#/components/schemas/Channel",
    "description": "Channel"
   },
   "timeslot": {
    "type": "string",
    "description": "Timeslot",
    "nullable": true
   },
   "date": {
    "type": "string",
    "description": "Business date",
    "format": "date"
   },
   "refunds": {
    "type": "integer",
    "description": "Refunds"
   },
   "customerMix": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "dimension": {
       "type": "string",
       "enum": [
        "segment",
        "membership",
        "geography"
       ],
       "description": "Customer dimension"
      },
      "value": {
       "type": "string",
       "description": "Segment / membership tier / geography"
      },
      "share": {
       "type": "number",
       "description": "Share of tickets sold, percent"
      }
     }
    },
    "description": "Customer signals: Segment, Membership, Geography mix"
   },
   "comparison": {
    "type": "object",
    "properties": {
     "basis": {
      "type": "string",
      "enum": [
       "yesterday",
       "previousWeek",
       "sameDayLastYear",
       "previousEvent",
       "similarEvent",
       "forecastBaseline"
      ],
      "description": "Comparison basis (compareTo)"
     },
     "ticketsSoldChange": {
      "type": "number",
      "description": "Change in tickets sold, percent"
     },
     "revenueChange": {
      "type": "number",
      "description": "Change in revenue, percent"
     },
     "conversionChange": {
      "type": "number",
      "description": "Change in conversion, percentage points"
     },
     "bookingVelocityChange": {
      "type": "number",
      "description": "Change in booking velocity, percent"
     }
    },
    "description": "Historical Comparison against the basis chosen in compareTo"
   },
   "anomalies": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Anomaly Detection, e.g. booking velocity increased 47% during the last 90 minutes. Advisory only: generated narrative never changes a price (decided 29 September, readiness close-out)"
   },
   "lastUpdated": {
    "type": "string",
    "description": "When the signal was last refreshed",
    "format": "date-time"
   }
  }
 },
 "MarketTourismHolidayContextualSignalHubView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Market, Tourism, Holiday & Contextual Signal Hub displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "source": {
    "type": "string",
    "description": "Source name (vendor-neutral)"
   },
   "geography": {
    "type": "string",
    "description": "Geography the signal covers"
   },
   "refreshFrequency": {
    "type": "string",
    "description": "Refresh Frequency",
    "enum": [
     "realTime",
     "hourly",
     "daily",
     "weekly",
     "manual"
    ]
   },
   "weight": {
    "type": "number",
    "description": "Weight given to the signal in forecasting, 0-1; default 0.5 (decided 29 September, readiness close-out)"
   },
   "reliability": {
    "type": "number",
    "description": "Reliability, percent"
   },
   "historicalCorrelation": {
    "type": "number",
    "description": "Historical correlation with venue demand, -1..1"
   },
   "active": {
    "type": "boolean",
    "description": "Active/Inactive; new external sources start inactive (decided 29 September, readiness close-out)"
   },
   "currentEstimatedImpact": {
    "type": "number",
    "description": "Current Estimated Impact on venue demand, percent"
   },
   "signalId": {
    "type": "string",
    "description": "Signal id"
   },
   "category": {
    "type": "string",
    "description": "Signal Category",
    "enum": [
     "calendar",
     "tourism",
     "transport",
     "market"
    ]
   },
   "signalType": {
    "type": "string",
    "description": "Signal",
    "enum": [
     "publicHoliday",
     "schoolHoliday",
     "ramadan",
     "eid",
     "christmas",
     "newYear",
     "longWeekend",
     "visitorArrivals",
     "tourismDemand",
     "hotelOccupancy",
     "hotelRates",
     "destinationDemand",
     "flightArrivals",
     "airportPassengerVolume",
     "publicTransportDemand",
     "trafficConditions",
     "consumerDemandTrends",
     "searchTrends",
     "destinationPopularity",
     "marketActivity"
    ]
   },
   "currentValue": {
    "type": "number",
    "description": "Current reading, e.g. hotel occupancy 92",
    "nullable": true
   },
   "unit": {
    "type": "string",
    "description": "Unit of currentValue (percent, count, currency...)",
    "nullable": true
   },
   "periodStart": {
    "type": "string",
    "description": "Calendar signals: first day",
    "format": "date",
    "nullable": true
   },
   "periodEnd": {
    "type": "string",
    "description": "Calendar signals: last day",
    "format": "date",
    "nullable": true
   },
   "lastUpdated": {
    "type": "string",
    "description": "Last refresh",
    "format": "date-time"
   }
  }
 },
 "NearbyEventExhibitionLocalDemandIntelligenceView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Nearby Event, Exhibition & Local Demand Intelligence displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "eventName": {
    "type": "string",
    "description": "Event Name"
   },
   "venue": {
    "type": "string",
    "description": "External venue hosting the event"
   },
   "location": {
    "type": "string",
    "description": "Location (address or area)"
   },
   "distanceKm": {
    "type": "number",
    "description": "Distance from the TICVAI venue, km"
   },
   "expectedAttendance": {
    "type": "integer",
    "description": "Expected Attendance"
   },
   "eventType": {
    "type": "string",
    "description": "Event Type",
    "enum": [
     "exhibition",
     "conference",
     "concert",
     "sportsEvent",
     "festival",
     "tradeShow",
     "convention",
     "publicCelebration",
     "majorAttractionEvent",
     "schoolEvent",
     "customLocalEvent"
    ]
   },
   "audienceType": {
    "type": "string",
    "description": "Audience Type (decided 29 September, readiness close-out)",
    "enum": [
     "family",
     "business",
     "youth",
     "general",
     "tourist",
     "other"
    ]
   },
   "source": {
    "type": "string",
    "description": "Source: name of the event feed or 'manual' (vendor-neutral)"
   },
   "confidence": {
    "type": "number",
    "description": "Confidence that the event and its attendance are accurate, percent"
   },
   "externalEventId": {
    "type": "string",
    "description": "External event id"
   },
   "ticvaiVenue": {
    "type": "string",
    "description": "TICVAI venue whose monitoring radius the event falls in"
   },
   "monitoringRadiusKm": {
    "type": "number",
    "description": "Geographic Radius configured for that venue: 1, 3, 5, 10 or custom km; default 5 (decided 29 September, readiness close-out)"
   },
   "startDate": {
    "type": "string",
    "description": "Start date",
    "format": "date"
   },
   "endDate": {
    "type": "string",
    "description": "End date",
    "format": "date"
   },
   "startTime": {
    "type": "string",
    "description": "Start time (HH:mm)",
    "nullable": true
   },
   "endTime": {
    "type": "string",
    "description": "End time (HH:mm)",
    "nullable": true
   },
   "historicalCorrelation": {
    "type": "number",
    "description": "Historical correlation: demand change seen at the venue for similar past events, percent"
   },
   "predictedImpactMin": {
    "type": "number",
    "description": "Predicted demand impact, low end, percent"
   },
   "predictedImpactMax": {
    "type": "number",
    "description": "Predicted demand impact, high end, percent"
   },
   "impactWindows": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "beforeEvent",
      "duringEvent",
      "lunchPeriod",
      "afterEvent",
      "evening",
      "followingDay"
     ]
    },
    "description": "Timing Intelligence: when the impact is expected"
   },
   "audienceMatch": {
    "type": "string",
    "description": "Audience Matching between the event and the TICVAI venue",
    "enum": [
     "low",
     "medium",
     "high"
    ]
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
 "PriceElasticityRevenueResponseIntelligenceView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Price Elasticity & Revenue Response Intelligence displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "price": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price tested on the curve"
   },
   "demand": {
    "type": "integer",
    "description": "Expected demand at this price"
   },
   "conversion": {
    "type": "number",
    "description": "Expected conversion, percent"
   },
   "revenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Expected revenue"
   },
   "margin": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Expected margin"
   },
   "occupancy": {
    "type": "number",
    "description": "Expected occupancy, percent"
   },
   "customerSegment": {
    "type": "string",
    "description": "Customer segment (e.g. tourist, resident, family, VIP)",
    "nullable": true
   },
   "channel": {
    "$ref": "#/components/schemas/Channel",
    "description": "Channel"
   },
   "time": {
    "type": "string",
    "description": "Time context of the curve: weekday/weekend, peak/off-peak or season label"
   },
   "product": {
    "type": "string",
    "description": "Product id"
   },
   "venue": {
    "type": "string",
    "description": "Venue id"
   },
   "priceSensitivity": {
    "type": "string",
    "description": "Price sensitivity of the segment",
    "enum": [
     "low",
     "medium",
     "high"
    ]
   },
   "elasticityCoefficient": {
    "type": "number",
    "description": "Estimated price elasticity of demand (negative)",
    "nullable": true
   },
   "elasticityConfidence": {
    "type": "string",
    "description": "Elasticity Confidence",
    "enum": [
     "low",
     "medium",
     "high"
    ]
   },
   "inRecommendedRevenueZone": {
    "type": "boolean",
    "description": "Price lies inside the Recommended Revenue Zone"
   },
   "revenueZoneMin": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Optimal revenue range, low end"
   },
   "revenueZoneMax": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Optimal revenue range, high end"
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
 },
 "WeatherIntelligenceDemandImpactConfigurationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Weather Intelligence & Demand Impact Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "temperature": {
    "type": "number",
    "description": "Temperature, degrees C"
   },
   "feelsLikeTemperature": {
    "type": "number",
    "description": "Feels-Like Temperature, degrees C"
   },
   "rain": {
    "type": "number",
    "description": "Rain, mm in the last hour"
   },
   "rainProbability": {
    "type": "number",
    "description": "Rain Probability, percent"
   },
   "humidity": {
    "type": "number",
    "description": "Humidity, percent"
   },
   "wind": {
    "type": "number",
    "description": "Wind speed, km/h"
   },
   "visibility": {
    "type": "number",
    "description": "Visibility, km"
   },
   "storm": {
    "type": "boolean",
    "description": "Storm warning in force"
   },
   "extremeHeat": {
    "type": "boolean",
    "description": "Extreme Heat: temperature at or above the venue's configured heat threshold"
   },
   "currentConditions": {
    "type": "string",
    "description": "Current Conditions summary as reported by the source"
   },
   "hourlyForecast": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "at": {
       "type": "string",
       "format": "date-time",
       "description": "Hour"
      },
      "temperature": {
       "type": "number",
       "description": "Degrees C"
      },
      "rainProbability": {
       "type": "number",
       "description": "Percent"
      },
      "conditions": {
       "type": "string",
       "description": "Conditions"
      }
     }
    },
    "description": "Hourly Forecast"
   },
   "dailyForecast": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "date": {
       "type": "string",
       "format": "date",
       "description": "Day"
      },
      "minTemperature": {
       "type": "number",
       "description": "Degrees C"
      },
      "maxTemperature": {
       "type": "number",
       "description": "Degrees C"
      },
      "rainProbability": {
       "type": "number",
       "description": "Percent"
      },
      "conditions": {
       "type": "string",
       "description": "Conditions"
      }
     }
    },
    "description": "Daily Forecast"
   },
   "weatherForecastConfidence": {
    "type": "number",
    "description": "Weather Forecast Confidence, percent"
   },
   "estimatedDemandImpactMin": {
    "type": "number",
    "description": "Estimated Demand Impact, low end of the range, percent"
   },
   "venue": {
    "type": "string",
    "description": "TICVAI venue id"
   },
   "venueExposure": {
    "type": "string",
    "description": "Venue Sensitivity: Indoor / Outdoor / Mixed",
    "enum": [
     "indoor",
     "outdoor",
     "mixed"
    ]
   },
   "weatherSensitivity": {
    "type": "string",
    "description": "Weather sensitivity of the venue; default medium (decided 29 September, readiness close-out)",
    "enum": [
     "low",
     "medium",
     "high"
    ]
   },
   "airQualityIndex": {
    "type": "integer",
    "description": "Air quality index where available",
    "nullable": true
   },
   "conditionImpacts": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "condition": {
       "type": "string",
       "enum": [
        "temperature",
        "feelsLikeTemperature",
        "rain",
        "rainProbability",
        "humidity",
        "wind",
        "visibility",
        "storm",
        "extremeHeat",
        "airQuality",
        "heavyRain",
        "highTemperature"
       ],
       "description": "Weather condition"
      },
      "threshold": {
       "type": "number",
       "nullable": true,
       "description": "Threshold in the condition's unit, e.g. 42 (degrees C)"
      },
      "demandImpactPercent": {
       "type": "number",
       "description": "Modelled demand impact, e.g. +8 indoor / -17 outdoor"
      }
     }
    },
    "description": "Weather Impact Model: condition -> demand impact rules for this venue"
   },
   "estimatedDemandImpactMax": {
    "type": "number",
    "description": "Estimated Demand Impact, high end of the range, percent"
   },
   "forecastHorizon": {
    "type": "string",
    "description": "Forecast Horizon",
    "enum": [
     "today",
     "hours24",
     "days3",
     "days7",
     "custom"
    ]
   },
   "forecastWindowDays": {
    "type": "integer",
    "description": "Configurable future window in days when forecastHorizon is custom; max 14 (decided 29 September, readiness close-out)",
    "nullable": true
   },
   "dataFailurePolicy": {
    "type": "string",
    "description": "What happens when weather data is unavailable; default reduceConfidence (decided 29 September, readiness close-out)",
    "enum": [
     "useLastValidSignal",
     "useHistoricalBaseline",
     "reduceConfidence",
     "ignoreWeather",
     "suspendWeatherDrivenRecommendation"
    ]
   },
   "historicalInsights": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Historical Learning, e.g. similar weather historically gave +11% indoor demand. Advisory only: generated narrative never changes a price (decided 29 September, readiness close-out)"
   },
   "weatherSource": {
    "type": "string",
    "description": "Name of the configured weather data source (vendor-neutral: the provider is data in the signal registry)"
   },
   "lastUpdated": {
    "type": "string",
    "description": "When the source last refreshed",
    "format": "date-time"
   }
  }
 }
}
```
