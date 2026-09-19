# WS54 — Promotions   Bundles Management board 10

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
  `PRICE_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **0 of these operations work offline**
  
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-228` | Promotion Performance Command Center | commandCentre | 1 | 0 | — |
| `ADM-229` | Campaign & Promotion Performance Explorer | listDetail | 1 | 0 | — |
| `ADM-230` | Redemption, Conversion & Funnel Analytics | commandCentre | 1 | 0 | — |
| `ADM-231` | Discount, Margin & Profitability Analytics | commandCentre | 1 | 0 | — |
| `ADM-232` | Bundle, BOGO & Advanced Offer Analytics | commandCentre | 1 | 0 | — |
| `ADM-233` | Upsell, Cross-Sell & Attach-Rate Analytics | commandCentre | 1 | 0 | — |
| `ADM-234` | Customer, Segment, Channel & Partner Analytics | commandCentre | 1 | 0 | — |
| `ADM-235` | Incrementality, Attribution & Cannibalization Analysis | listDetail | 1 | 0 | — |
| `ADM-236` | AI Optimization & Next-Best-Action Center | listDetail | 1 | 0 | — |
| `ADM-237` | Executive Promotion Intelligence & Reporting Studio | listDetail | 1 | 0 | — |

## Thin screens in this batch

**ADM-229, ADM-235, ADM-236, ADM-237 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-228",
  "name": "Promotion Performance Command Center",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "10",
   "number": "1",
   "page": 142
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/promotion-performance-command-center-adm-228",
   "component": "apps/ticvai-web/src/routes/commercial/PromotionPerformanceCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-229",
    "ADM-230",
    "ADM-231",
    "ADM-232",
    "ADM-233",
    "ADM-234",
    "ADM-235",
    "ADM-236",
    "ADM-237"
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
     "to": "ADM-229",
     "trigger": "Works in Campaign & Promotion Performance Explorer",
     "provenance": "flow F163 step 1→2",
     "operation": "listPromotionPerformance"
    },
    {
     "to": "ADM-230",
     "trigger": "Works in Redemption, Conversion & Funnel Analytics",
     "provenance": "flow F163 step 3→4",
     "operation": "listPromotionPerformance"
    },
    {
     "to": "ADM-231",
     "trigger": "Works in Discount, Margin & Profitability Analytics",
     "provenance": "flow F163 step 5→6",
     "operation": "listPromotionPerformance"
    },
    {
     "to": "ADM-232",
     "trigger": "Works in Bundle, BOGO & Advanced Offer Analytics",
     "provenance": "flow F163 step 7→8",
     "operation": "listPromotionPerformance"
    },
    {
     "to": "ADM-233",
     "trigger": "Works in Upsell, Cross-Sell & Attach-Rate Analytics",
     "provenance": "flow F163 step 9→10",
     "operation": "listPromotionPerformance"
    },
    {
     "to": "ADM-234",
     "trigger": "Works in Customer, Segment, Channel & Partner Analytics",
     "provenance": "flow F163 step 11→12",
     "operation": "listPromotionPerformance"
    },
    {
     "to": "ADM-235",
     "trigger": "Works in Incrementality, Attribution & Cannibalization Analysis",
     "provenance": "flow F163 step 13→14",
     "operation": "listPromotionPerformance"
    },
    {
     "to": "ADM-236",
     "trigger": "Works in AI Optimization & Next-Best-Action Center",
     "provenance": "flow F163 step 15→16",
     "operation": "listPromotionPerformance"
    },
    {
     "to": "ADM-237",
     "trigger": "Works in Executive Promotion Intelligence & Reporting Studio",
     "provenance": "flow F163 step 17→18",
     "operation": "listPromotionPerformance"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§KPI Cards; Show) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide executives, Marketing, Commercial, Revenue, and Finance with the overall performance of promotions and bundles.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search promotion performance",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 142 §Global Filters"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "PromotionPerformanceCommandCenterView.dateRange",
        "PromotionPerformanceCommandCenterView.businessEntity",
        "PromotionPerformanceCommandCenterView.venue",
        "PromotionPerformanceCommandCenterView.attraction",
        "PromotionPerformanceCommandCenterView.campaign",
        "PromotionPerformanceCommandCenterView.promotion",
        "PromotionPerformanceCommandCenterView.bundle",
        "PromotionPerformanceCommandCenterView.channel",
        "PromotionPerformanceCommandCenterView.customerSegment",
        "PromotionPerformanceCommandCenterView.product",
        "PromotionPerformanceCommandCenterView.partner",
        "PromotionPerformanceCommandCenterView.market",
        "PromotionPerformanceCommandCenterView.currency"
       ],
       "notes": "The pack filters this screen by date range, business entity, venue, attraction, campaign, promotion and 7 more — which are present is a decision the pack already made.",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 142 §Global Filters"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Gross Sales",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 142 §KPI Cards",
       "bindsTo": "PromotionPerformanceCommandCenterView.grossSales"
      },
      {
       "kind": "metricTile",
       "label": "Promotion-Influenced Revenue",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 142 §KPI Cards",
       "bindsTo": "PromotionPerformanceCommandCenterView.promotionInfluencedRevenue"
      },
      {
       "kind": "metricTile",
       "label": "Estimated Incremental Revenue",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 142 §KPI Cards",
       "bindsTo": "PromotionPerformanceCommandCenterView.estimatedIncrementalRevenue"
      },
      {
       "kind": "metricTile",
       "label": "Discount Granted",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 142 §KPI Cards",
       "bindsTo": "PromotionPerformanceCommandCenterView.discountGranted"
      },
      {
       "kind": "metricTile",
       "label": "Net Revenue",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 142 §KPI Cards",
       "bindsTo": "PromotionPerformanceCommandCenterView.netRevenue"
      },
      {
       "kind": "metricTile",
       "label": "Gross Margin",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 142 §KPI Cards",
       "bindsTo": "PromotionPerformanceCommandCenterView.grossMargin"
      },
      {
       "kind": "metricTile",
       "label": "Promotion Cost",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 142 §KPI Cards",
       "bindsTo": "PromotionPerformanceCommandCenterView.promotionCost"
      },
      {
       "kind": "metricTile",
       "label": "ROI",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 142 §KPI Cards",
       "bindsTo": "PromotionPerformanceCommandCenterView.roi"
      },
      {
       "kind": "metricTile",
       "label": "Transactions",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 142 §KPI Cards",
       "bindsTo": "PromotionPerformanceCommandCenterView.transactions"
      },
      {
       "kind": "metricTile",
       "label": "Redemptions",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 142 §KPI Cards",
       "bindsTo": "PromotionPerformanceCommandCenterView.redemptions"
      },
      {
       "kind": "metricTile",
       "label": "Conversion Rate",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 142 §KPI Cards",
       "bindsTo": "PromotionPerformanceCommandCenterView.conversionRate"
      },
      {
       "kind": "metricTile",
       "label": "Average Order Value",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 142 §KPI Cards",
       "bindsTo": "PromotionPerformanceCommandCenterView.averageOrderValue"
      },
      {
       "kind": "metricTile",
       "label": "Revenue per Redemption",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 142 §KPI Cards",
       "bindsTo": "PromotionPerformanceCommandCenterView.revenuePerRedemption"
      },
      {
       "kind": "metricTile",
       "label": "Active Campaigns",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 142 §KPI Cards",
       "bindsTo": "PromotionPerformanceCommandCenterView.activeCampaigns"
      },
      {
       "kind": "metricTile",
       "label": "Revenue vs Discount Cost vs Incremental Revenue",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 142 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The promotion performance list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the promotion performance untouched.",
   "emptyFirstRun": "No promotion performance yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the promotion performance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPromotionPerformance",
    "contract": "promotions",
    "purpose": "Promotion Performance Command Center",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "PromotionPerformanceCommandCenterView.grossSales",
    "PromotionPerformanceCommandCenterView.promotionInfluencedRevenue",
    "PromotionPerformanceCommandCenterView.estimatedIncrementalRevenue",
    "PromotionPerformanceCommandCenterView.discountGranted",
    "PromotionPerformanceCommandCenterView.netRevenue",
    "PromotionPerformanceCommandCenterView.grossMargin"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-228"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 142. 27 of 27 labels bound to a contract property; 28 of 35 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-229",
  "name": "Campaign & Promotion Performance Explorer",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "10",
   "number": "2",
   "page": 143
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/campaign-promotion-performance-explorer-adm-229",
   "component": "apps/ticvai-web/src/routes/commercial/CampaignPromotionPerformanceExplorer.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-228"
   ],
   "exitTo": [
    "ADM-228"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-228, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-228",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F163 step 2→3",
     "operation": "listCampaignPromotionPerformance"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow users to compare every promotion and campaign using consistent commercial KPIs.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 143"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 143"
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
       "impliedBy": "listCampaignPromotionPerformance",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The campaign promotion performance list.",
   "error": "Could not load. Names which read failed and leaves the campaign promotion performance untouched.",
   "emptyFirstRun": "No campaign promotion performance yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the campaign promotion performance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCampaignPromotionPerformance",
    "contract": "promotions",
    "purpose": "Campaign & Promotion Performance Explorer",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "CampaignPromotionPerformanceExplorerView.aed38",
    "CampaignPromotionPerformanceExplorerView.family20310k740k29118",
    "CampaignPromotionPerformanceExplorerView.summer1Aed26",
    "CampaignPromotionPerformanceExplorerView.aed41",
    "CampaignPromotionPerformanceExplorerView.app1092k310k34132"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-229"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 143. 0 of 0 labels bound to a contract property; 0 of 32 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-230",
  "name": "Redemption, Conversion & Funnel Analytics",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "10",
   "number": "3",
   "page": 144
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/redemption-conversion-funnel-analytics-adm-230",
   "component": "apps/ticvai-web/src/routes/commercial/RedemptionConversionFunnelAnalytics.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-228"
   ],
   "exitTo": [
    "ADM-228"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-228, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-228",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F163 step 4→5",
     "operation": "listRedemptionConversionFunnel"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Measure how effectively offers move customers from exposure to purchase and redemption.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search redemption conversion funnel",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 144 §Analyze by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Channel",
        "Customer segment",
        "Membership tier",
        "Product",
        "Venue",
        "Campaign",
        "Promotion type",
        "Day/time",
        "Device",
        "Partner"
       ],
       "notes": "The pack filters this screen by channel, customer segment, membership tier, product, venue, campaign and 4 more — which are present is a decision the pack already made.",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 144 §Analyze by"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Exposure rate",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 144 §KPIs",
       "bindsTo": "RedemptionConversionFunnelAnalyticsView.exposureRate"
      },
      {
       "kind": "metricTile",
       "label": "Engagement rate",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 144 §KPIs",
       "bindsTo": "RedemptionConversionFunnelAnalyticsView.engagementRate"
      },
      {
       "kind": "metricTile",
       "label": "Cart rate",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 144 §KPIs",
       "bindsTo": "RedemptionConversionFunnelAnalyticsView.cartRate"
      },
      {
       "kind": "metricTile",
       "label": "Conversion rate",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 144 §KPIs",
       "bindsTo": "RedemptionConversionFunnelAnalyticsView.conversionRate"
      },
      {
       "kind": "metricTile",
       "label": "Redemption rate",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 144 §KPIs",
       "bindsTo": "RedemptionConversionFunnelAnalyticsView.redemptionRate"
      },
      {
       "kind": "metricTile",
       "label": "Abandonment",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 144 §KPIs",
       "bindsTo": "RedemptionConversionFunnelAnalyticsView.abandonment"
      },
      {
       "kind": "metricTile",
       "label": "Unused promotion rate",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 144 §KPIs",
       "bindsTo": "RedemptionConversionFunnelAnalyticsView.unusedPromotionRate"
      },
      {
       "kind": "metricTile",
       "label": "Expired benefit rate",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 144 §KPIs",
       "bindsTo": "RedemptionConversionFunnelAnalyticsView.expiredBenefitRate"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The redemption conversion funnel list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the redemption conversion funnel untouched.",
   "emptyFirstRun": "No redemption conversion funnel yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the redemption conversion funnel are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listRedemptionConversionFunnel",
    "contract": "promotions",
    "purpose": "Redemption, Conversion & Funnel Analytics",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "RedemptionConversionFunnelAnalyticsView.exposureRate",
    "RedemptionConversionFunnelAnalyticsView.engagementRate",
    "RedemptionConversionFunnelAnalyticsView.cartRate",
    "RedemptionConversionFunnelAnalyticsView.conversionRate",
    "RedemptionConversionFunnelAnalyticsView.redemptionRate",
    "RedemptionConversionFunnelAnalyticsView.abandonment"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-230"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 144. 8 of 18 labels bound to a contract property; 18 of 34 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-231",
  "name": "Discount, Margin & Profitability Analytics",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "10",
   "number": "4",
   "page": 145
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/discount-margin-profitability-analytics-adm-231",
   "component": "apps/ticvai-web/src/routes/commercial/DiscountMarginProfitabilityAnalytics.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-228"
   ],
   "exitTo": [
    "ADM-228"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-228, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-228",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F163 step 6→7",
     "operation": "listDiscountMarginProfitability"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Core Metrics) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Determine whether promotions are commercially profitable rather than merely generating sales.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Gross Revenue",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 145 §Core Metrics",
       "bindsTo": "DiscountMarginProfitabilityAnalyticsView.grossRevenue"
      },
      {
       "kind": "metricTile",
       "label": "Discount Value",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 145 §Core Metrics",
       "bindsTo": "DiscountMarginProfitabilityAnalyticsView.discountValue"
      },
      {
       "kind": "metricTile",
       "label": "Net Revenue",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 145 §Core Metrics",
       "bindsTo": "DiscountMarginProfitabilityAnalyticsView.netRevenue"
      },
      {
       "kind": "metricTile",
       "label": "Product Cost",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 145 §Core Metrics",
       "bindsTo": "DiscountMarginProfitabilityAnalyticsView.productCost"
      },
      {
       "kind": "metricTile",
       "label": "Promotion Cost",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 145 §Core Metrics",
       "bindsTo": "DiscountMarginProfitabilityAnalyticsView.promotionCost"
      },
      {
       "kind": "metricTile",
       "label": "Gross Profit",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 145 §Core Metrics",
       "bindsTo": "DiscountMarginProfitabilityAnalyticsView.grossProfit"
      },
      {
       "kind": "metricTile",
       "label": "Gross Margin %",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 145 §Core Metrics",
       "bindsTo": "DiscountMarginProfitabilityAnalyticsView.grossMargin"
      },
      {
       "kind": "metricTile",
       "label": "Margin Change",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 145 §Core Metrics",
       "bindsTo": "DiscountMarginProfitabilityAnalyticsView.marginChange"
      },
      {
       "kind": "metricTile",
       "label": "Revenue Uplift",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 145 §Core Metrics",
       "bindsTo": "DiscountMarginProfitabilityAnalyticsView.revenueUplift"
      },
      {
       "kind": "metricTile",
       "label": "Profit Uplift",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 145 §Core Metrics",
       "bindsTo": "DiscountMarginProfitabilityAnalyticsView.profitUplift"
      },
      {
       "kind": "metricTile",
       "label": "ROI",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 145 §Core Metrics",
       "bindsTo": "DiscountMarginProfitabilityAnalyticsView.roi"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The discount margin profitability list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the discount margin profitability untouched.",
   "emptyFirstRun": "No discount margin profitability yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the discount margin profitability are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listDiscountMarginProfitability",
    "contract": "promotions",
    "purpose": "Discount, Margin & Profitability Analytics",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "DiscountMarginProfitabilityAnalyticsView.grossRevenue",
    "DiscountMarginProfitabilityAnalyticsView.discountValue",
    "DiscountMarginProfitabilityAnalyticsView.netRevenue",
    "DiscountMarginProfitabilityAnalyticsView.productCost",
    "DiscountMarginProfitabilityAnalyticsView.promotionCost",
    "DiscountMarginProfitabilityAnalyticsView.grossProfit"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-231"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 145. 11 of 11 labels bound to a contract property; 11 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-232",
  "name": "Bundle, BOGO & Advanced Offer Analytics",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "10",
   "number": "5",
   "page": 146
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/bundle-bogo-advanced-offer-analytics-adm-232",
   "component": "apps/ticvai-web/src/routes/commercial/BundleBogoAdvancedOfferAnalytics.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-228"
   ],
   "exitTo": [
    "ADM-228"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-228, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-228",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F163 step 8→9",
     "operation": "listBundleBogoAdvanced"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Bundle KPIs; BOGO Metrics) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Measure performance specifically for the commercial mechanics created in Boards 4–6.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Bundle Sales",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 146 §Bundle KPIs",
       "bindsTo": "BundleBogoAdvancedOfferAnalyticsView.bundleSales"
      },
      {
       "kind": "metricTile",
       "label": "Bundle Revenue",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 146 §Bundle KPIs",
       "bindsTo": "BundleBogoAdvancedOfferAnalyticsView.bundleRevenue"
      },
      {
       "kind": "metricTile",
       "label": "Bundle Conversion",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 146 §Bundle KPIs",
       "bindsTo": "BundleBogoAdvancedOfferAnalyticsView.bundleConversion"
      },
      {
       "kind": "metricTile",
       "label": "Bundle AOV",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 146 §Bundle KPIs",
       "bindsTo": "BundleBogoAdvancedOfferAnalyticsView.bundleAov"
      },
      {
       "kind": "metricTile",
       "label": "Component Attach Rate",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 146 §Bundle KPIs",
       "bindsTo": "BundleBogoAdvancedOfferAnalyticsView.componentAttachRate"
      },
      {
       "kind": "metricTile",
       "label": "Component Redemption",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 146 §Bundle KPIs",
       "bindsTo": "BundleBogoAdvancedOfferAnalyticsView.componentRedemption"
      },
      {
       "kind": "metricTile",
       "label": "Bundle Margin",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 146 §Bundle KPIs",
       "bindsTo": "BundleBogoAdvancedOfferAnalyticsView.bundleMargin"
      },
      {
       "kind": "metricTile",
       "label": "Bundle vs Standalone Revenue",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 146 §Bundle KPIs",
       "bindsTo": "BundleBogoAdvancedOfferAnalyticsView.bundleVsStandaloneRevenue"
      },
      {
       "kind": "metricTile",
       "label": "Substitution Rate",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 146 §Bundle KPIs",
       "bindsTo": "BundleBogoAdvancedOfferAnalyticsView.substitutionRate"
      },
      {
       "kind": "metricTile",
       "label": "Availability Failure Rate",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 146 §Bundle KPIs",
       "bindsTo": "BundleBogoAdvancedOfferAnalyticsView.availabilityFailureRate"
      },
      {
       "kind": "metricTile",
       "label": "BOGO transactions",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 146 §BOGO Metrics",
       "bindsTo": "BundleBogoAdvancedOfferAnalyticsView.bogoTransactions"
      },
      {
       "kind": "metricTile",
       "label": "Free items issued",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 146 §BOGO Metrics",
       "bindsTo": "BundleBogoAdvancedOfferAnalyticsView.freeItemsIssued"
      },
      {
       "kind": "metricTile",
       "label": "Average reward value",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 146 §BOGO Metrics",
       "bindsTo": "BundleBogoAdvancedOfferAnalyticsView.averageRewardValue"
      },
      {
       "kind": "metricTile",
       "label": "Incremental units",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 146 §BOGO Metrics",
       "bindsTo": "BundleBogoAdvancedOfferAnalyticsView.incrementalUnits"
      },
      {
       "kind": "metricTile",
       "label": "Incremental revenue",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 146 §BOGO Metrics",
       "bindsTo": "BundleBogoAdvancedOfferAnalyticsView.incrementalRevenue"
      },
      {
       "kind": "metricTile",
       "label": "Margin impact",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 146 §BOGO Metrics",
       "bindsTo": "BundleBogoAdvancedOfferAnalyticsView.marginImpact"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The bundle bogo advanced list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the bundle bogo advanced untouched.",
   "emptyFirstRun": "No bundle bogo advanced yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the bundle bogo advanced are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listBundleBogoAdvanced",
    "contract": "promotions",
    "purpose": "Bundle, BOGO & Advanced Offer Analytics",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "BundleBogoAdvancedOfferAnalyticsView.bundleSales",
    "BundleBogoAdvancedOfferAnalyticsView.bundleRevenue",
    "BundleBogoAdvancedOfferAnalyticsView.bundleConversion",
    "BundleBogoAdvancedOfferAnalyticsView.bundleAov",
    "BundleBogoAdvancedOfferAnalyticsView.componentAttachRate",
    "BundleBogoAdvancedOfferAnalyticsView.componentRedemption"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-232"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 146. 16 of 16 labels bound to a contract property; 16 of 26 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-233",
  "name": "Upsell, Cross-Sell & Attach-Rate Analytics",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "10",
   "number": "6",
   "page": 147
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/upsell-cross-sell-attach-rate-analytics-adm-233",
   "component": "apps/ticvai-web/src/routes/commercial/UpsellCrossSellAttachRateAnalytics.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-228"
   ],
   "exitTo": [
    "ADM-228"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-228, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-228",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F163 step 10→11",
     "operation": "listUpsellCrossSell"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§KPIs) and a per-row directory (§Analyze) — counts over a population, then the population",
  "purpose": "Measure whether promotions and bundles successfully increase the customer's basket beyond the original purchase. This screen is particularly important for the cross-sale metrics you originally raised.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Cross-Sell Revenue",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 147 §KPIs",
       "bindsTo": "UpsellCrossSellAttachRateAnalyticsView.crossSellRevenue"
      },
      {
       "kind": "metricTile",
       "label": "Upsell Revenue",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 147 §KPIs",
       "bindsTo": "UpsellCrossSellAttachRateAnalyticsView.upsellRevenue"
      },
      {
       "kind": "metricTile",
       "label": "Attach Rate",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 147 §KPIs",
       "bindsTo": "UpsellCrossSellAttachRateAnalyticsView.attachRate"
      },
      {
       "kind": "metricTile",
       "label": "Items per Transaction",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 147 §KPIs",
       "bindsTo": "UpsellCrossSellAttachRateAnalyticsView.itemsPerTransaction"
      },
      {
       "kind": "metricTile",
       "label": "Revenue per Transaction",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 147 §KPIs",
       "bindsTo": "UpsellCrossSellAttachRateAnalyticsView.revenuePerTransaction"
      },
      {
       "kind": "metricTile",
       "label": "Upgrade Conversion",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 147 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Recommended Offer Acceptance",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 147 §KPIs",
       "bindsTo": "UpsellCrossSellAttachRateAnalyticsView.recommendedOfferAcceptance"
      },
      {
       "kind": "metricTile",
       "label": "Incremental Basket Value",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 147 §KPIs",
       "bindsTo": "UpsellCrossSellAttachRateAnalyticsView.incrementalBasketValue"
      },
      {
       "kind": "metricTile",
       "label": "Cross-Category Conversion",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 147 §KPIs",
       "bindsTo": "UpsellCrossSellAttachRateAnalyticsView.crossCategoryConversion"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every upsell cross-sell attach-rate",
       "columns": [
        "UpsellCrossSellAttachRateAnalyticsView.ticketTicket",
        "UpsellCrossSellAttachRateAnalyticsView.ticketFB",
        "UpsellCrossSellAttachRateAnalyticsView.ticketRetail",
        "UpsellCrossSellAttachRateAnalyticsView.ticketExperience",
        "UpsellCrossSellAttachRateAnalyticsView.ticketMembership",
        "UpsellCrossSellAttachRateAnalyticsView.fBRetail",
        "UpsellCrossSellAttachRateAnalyticsView.retailFB",
        "UpsellCrossSellAttachRateAnalyticsView.membershipExperience"
       ],
       "bindsTo": "UpsellCrossSellAttachRateAnalyticsView",
       "operation": "listUpsellCrossSell",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 147 §Analyze"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected upsell cross-sell attach-rate",
       "bindsTo": "UpsellCrossSellAttachRateAnalyticsView",
       "columns": [
        "UpsellCrossSellAttachRateAnalyticsView.ticketTicket",
        "UpsellCrossSellAttachRateAnalyticsView.ticketFB",
        "UpsellCrossSellAttachRateAnalyticsView.ticketRetail",
        "UpsellCrossSellAttachRateAnalyticsView.ticketExperience",
        "UpsellCrossSellAttachRateAnalyticsView.ticketMembership",
        "UpsellCrossSellAttachRateAnalyticsView.fBRetail",
        "UpsellCrossSellAttachRateAnalyticsView.retailFB",
        "UpsellCrossSellAttachRateAnalyticsView.membershipExperience"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Important Scope Boundary”.",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 147 §Analyze"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The upsell cross-sell attach-rate list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the upsell cross-sell attach-rate untouched.",
   "emptyFirstRun": "No upsell cross-sell attach-rate yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the upsell cross-sell attach-rate are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listUpsellCrossSell",
    "contract": "promotions",
    "purpose": "Upsell, Cross-Sell & Attach-Rate Analytics",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "UpsellCrossSellAttachRateAnalyticsView.crossSellRevenue",
    "UpsellCrossSellAttachRateAnalyticsView.upsellRevenue",
    "UpsellCrossSellAttachRateAnalyticsView.attachRate",
    "UpsellCrossSellAttachRateAnalyticsView.itemsPerTransaction",
    "UpsellCrossSellAttachRateAnalyticsView.revenuePerTransaction",
    "Upgrade Conversion"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-233"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 147. 16 of 16 labels bound to a contract property; 17 of 32 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-234",
  "name": "Customer, Segment, Channel & Partner Analytics",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "10",
   "number": "7",
   "page": 148
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/customer-segment-channel-partner-analytics-adm-234",
   "component": "apps/ticvai-web/src/routes/commercial/CustomerSegmentChannelPartnerAnalytics.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-228"
   ],
   "exitTo": [
    "ADM-228"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-228, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-228",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F163 step 12→13",
     "operation": "listCustomerSegmentChannel"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Customer/Segment KPIs) and a per-row directory (§Compare; Measure) — counts over a population, then the population",
  "purpose": "Determine which audiences and distribution channels respond best to promotions.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Customers reached",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 148 §Customer/Segment KPIs",
       "bindsTo": "CustomerSegmentChannelPartnerAnalyticsView.customersReached"
      },
      {
       "kind": "metricTile",
       "label": "New customers",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 148 §Customer/Segment KPIs",
       "bindsTo": "CustomerSegmentChannelPartnerAnalyticsView.newCustomers"
      },
      {
       "kind": "metricTile",
       "label": "Returning customers",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 148 §Customer/Segment KPIs",
       "bindsTo": "CustomerSegmentChannelPartnerAnalyticsView.returningCustomers"
      },
      {
       "kind": "metricTile",
       "label": "Conversion",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 148 §Customer/Segment KPIs",
       "bindsTo": "CustomerSegmentChannelPartnerAnalyticsView.conversion"
      },
      {
       "kind": "metricTile",
       "label": "Revenue",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 148 §Customer/Segment KPIs",
       "bindsTo": "CustomerSegmentChannelPartnerAnalyticsView.revenue"
      },
      {
       "kind": "metricTile",
       "label": "Discount",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 148 §Customer/Segment KPIs",
       "bindsTo": "CustomerSegmentChannelPartnerAnalyticsView.discount"
      },
      {
       "kind": "metricTile",
       "label": "AOV",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 148 §Customer/Segment KPIs",
       "bindsTo": "CustomerSegmentChannelPartnerAnalyticsView.aov"
      },
      {
       "kind": "metricTile",
       "label": "Margin",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 148 §Customer/Segment KPIs",
       "bindsTo": "CustomerSegmentChannelPartnerAnalyticsView.margin"
      },
      {
       "kind": "metricTile",
       "label": "Repeat purchase",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 148 §Customer/Segment KPIs",
       "bindsTo": "CustomerSegmentChannelPartnerAnalyticsView.repeatPurchase"
      },
      {
       "kind": "metricTile",
       "label": "Redemption",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 148 §Customer/Segment KPIs",
       "bindsTo": "CustomerSegmentChannelPartnerAnalyticsView.redemption"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every customer segment channel",
       "columns": [
        "CustomerSegmentChannelPartnerAnalyticsView.b2c",
        "CustomerSegmentChannelPartnerAnalyticsView.mobileApp",
        "CustomerSegmentChannelPartnerAnalyticsView.pos",
        "CustomerSegmentChannelPartnerAnalyticsView.kiosk",
        "CustomerSegmentChannelPartnerAnalyticsView.b2b",
        "CustomerSegmentChannelPartnerAnalyticsView.callCenter",
        "CustomerSegmentChannelPartnerAnalyticsView.ota",
        "CustomerSegmentChannelPartnerAnalyticsView.reseller",
        "CustomerSegmentChannelPartnerAnalyticsView.api",
        "CustomerSegmentChannelPartnerAnalyticsView.partnerRevenue",
        "CustomerSegmentChannelPartnerAnalyticsView.partnerRedemptions",
        "CustomerSegmentChannelPartnerAnalyticsView.discountCost",
        "CustomerSegmentChannelPartnerAnalyticsView.commission",
        "CustomerSegmentChannelPartnerAnalyticsView.netContribution",
        "CustomerSegmentChannelPartnerAnalyticsView.conversion",
        "CustomerSegmentChannelPartnerAnalyticsView.campaignRoi"
       ],
       "bindsTo": "CustomerSegmentChannelPartnerAnalyticsView",
       "operation": "listCustomerSegmentChannel",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 148 §Compare"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected customer segment channel",
       "bindsTo": "CustomerSegmentChannelPartnerAnalyticsView",
       "columns": [
        "CustomerSegmentChannelPartnerAnalyticsView.b2c",
        "CustomerSegmentChannelPartnerAnalyticsView.mobileApp",
        "CustomerSegmentChannelPartnerAnalyticsView.pos",
        "CustomerSegmentChannelPartnerAnalyticsView.kiosk",
        "CustomerSegmentChannelPartnerAnalyticsView.b2b",
        "CustomerSegmentChannelPartnerAnalyticsView.callCenter",
        "CustomerSegmentChannelPartnerAnalyticsView.ota",
        "CustomerSegmentChannelPartnerAnalyticsView.reseller",
        "CustomerSegmentChannelPartnerAnalyticsView.api",
        "CustomerSegmentChannelPartnerAnalyticsView.partnerRevenue",
        "CustomerSegmentChannelPartnerAnalyticsView.partnerRedemptions",
        "CustomerSegmentChannelPartnerAnalyticsView.discountCost",
        "CustomerSegmentChannelPartnerAnalyticsView.commission",
        "CustomerSegmentChannelPartnerAnalyticsView.netContribution",
        "CustomerSegmentChannelPartnerAnalyticsView.conversion",
        "CustomerSegmentChannelPartnerAnalyticsView.campaignRoi"
       ],
       "notes": "The pack groups this record's detail under its own headings: “AOV ROI”.",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 148 §Compare"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The customer segment channel list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the customer segment channel untouched.",
   "emptyFirstRun": "No customer segment channel yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the customer segment channel are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCustomerSegmentChannel",
    "contract": "promotions",
    "purpose": "Customer, Segment, Channel & Partner Analytics",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "CustomerSegmentChannelPartnerAnalyticsView.customersReached",
    "CustomerSegmentChannelPartnerAnalyticsView.newCustomers",
    "CustomerSegmentChannelPartnerAnalyticsView.returningCustomers",
    "CustomerSegmentChannelPartnerAnalyticsView.conversion",
    "CustomerSegmentChannelPartnerAnalyticsView.revenue",
    "CustomerSegmentChannelPartnerAnalyticsView.discount"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-234"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 148. 26 of 26 labels bound to a contract property; 26 of 37 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-235",
  "name": "Incrementality, Attribution & Cannibalization Analysis",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "10",
   "number": "8",
   "page": 149
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/incrementality-attribution-cannibalization-analysis-adm-235",
   "component": "apps/ticvai-web/src/routes/commercial/IncrementalityAttributionCannibalizationAnalysis.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-228"
   ],
   "exitTo": [
    "ADM-228"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-228, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-228",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F163 step 14→15",
     "operation": "listIncrementalityAttributionCannibalization"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Detect) and no metric row",
  "purpose": "Incrementality, Attribution & Cannibalization Analysis",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every incrementality attribution cannibalization",
       "columns": [
        "Full-price customers moving to discounted products",
        "IncrementalityAttributionCannibalizationAnalysisView.standardTicketDiscountedTicket",
        "IncrementalityAttributionCannibalizationAnalysisView.higherMarginBundleLowerMarginPromotion",
        "Existing member purchase replaced by unnecessary discount",
        "IncrementalityAttributionCannibalizationAnalysisView.channelMigrationCausedByDiscounting"
       ],
       "bindsTo": "IncrementalityAttributionCannibalizationAnalysisView",
       "operation": "listIncrementalityAttributionCannibalization",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 149 §Detect"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected incrementality attribution cannibalization",
       "bindsTo": "IncrementalityAttributionCannibalizationAnalysisView",
       "columns": [
        "Full-price customers moving to discounted products",
        "IncrementalityAttributionCannibalizationAnalysisView.standardTicketDiscountedTicket",
        "IncrementalityAttributionCannibalizationAnalysisView.higherMarginBundleLowerMarginPromotion",
        "Existing member purchase replaced by unnecessary discount",
        "IncrementalityAttributionCannibalizationAnalysisView.channelMigrationCausedByDiscounting"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Answer the difficult question”, “Where sufficient data exists, support”, “Promotion-influenced revenue”, “Estimated baseline revenue”, “Estimated incremental revenue”, “AED 650K”.",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 149 §Detect"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The incrementality attribution cannibalization list.",
   "error": "Could not load. Names which read failed and leaves the incrementality attribution cannibalization untouched.",
   "emptyFirstRun": "No incrementality attribution cannibalization yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the incrementality attribution cannibalization are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listIncrementalityAttributionCannibalization",
    "contract": "promotions",
    "purpose": "Incrementality, Attribution & Cannibalization Analysis",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "Full-price customers moving to discounted products",
    "IncrementalityAttributionCannibalizationAnalysisView.standardTicketDiscountedTicket",
    "IncrementalityAttributionCannibalizationAnalysisView.higherMarginBundleLowerMarginPromotion",
    "Existing member purchase replaced by unnecessary discount",
    "IncrementalityAttributionCannibalizationAnalysisView.channelMigrationCausedByDiscounting"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-235"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 149. 3 of 5 labels bound to a contract property; 5 of 23 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-236",
  "name": "AI Optimization & Next-Best-Action Center",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "10",
   "number": "9",
   "page": 150
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/ai-optimization-next-best-action-center-adm-236",
   "component": "apps/ticvai-web/src/routes/commercial/AiOptimizationNextBestActionCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-228"
   ],
   "exitTo": [
    "ADM-228"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-228, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-228",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F163 step 16→17",
     "operation": "listNextBestAction"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Turn analytics into actionable commercial recommendations. This should be one of the strongest AI screens in the Promotions module.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 150"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 150"
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
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** Review, Accept as Draft, Simulate, Send for Approval, Dismiss, Snooze. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 150 §Authorized users can"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listNextBestAction",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The optimization next-best-action list.",
   "error": "Could not load. Names which read failed and leaves the optimization next-best-action untouched.",
   "emptyFirstRun": "No optimization next-best-action yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the optimization next-best-action are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listNextBestAction",
    "contract": "promotions",
    "purpose": "AI Optimization & Next-Best-Action Center",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "AiOptimizationNextBestActionCenterView.increaseDiscount",
    "AiOptimizationNextBestActionCenterView.reduceDiscount",
    "AiOptimizationNextBestActionCenterView.changeMechanic",
    "AiOptimizationNextBestActionCenterView.endPromotion",
    "AiOptimizationNextBestActionCenterView.changeThreshold"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-236"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 150. 0 of 0 labels bound to a contract property; 6 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-237",
  "name": "Executive Promotion Intelligence & Reporting Studio",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "10",
   "number": "10",
   "page": 151
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/executive-promotion-intelligence-reporting-studio-adm-237",
   "component": "apps/ticvai-web/src/routes/commercial/ExecutivePromotionIntelligenceReportingStudio.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-228"
   ],
   "exitTo": [
    "ADM-228"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-228, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation."
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Promotion Attribution & KPI Engine; Metric Governance) and no metric row",
  "purpose": "Provide executive reporting and configurable analytics output across the complete Promotions & Bundles module.",
  "gaps": [
   {
    "operation": null,
    "why": "**Executive Promotion Intelligence & Reporting Studio declares no operation that writes anything** — its only declared call is `listExecutivePromotionReporting`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
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
       "label": "Every executive promotion intelligence",
       "columns": [
        "↓"
       ],
       "bindsTo": "ExecutivePromotionIntelligenceReportingStudioView",
       "operation": "listExecutivePromotionReporting",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 151 §Promotion Attribution & KPI Engine"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected executive promotion intelligence",
       "bindsTo": "ExecutivePromotionIntelligenceReportingStudioView",
       "columns": [
        "↓"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Promotion ROI”, “Cross-Sell Revenue”, “Upsell Revenue”, “Top Campaigns”, “Underperformers”, “Reporting Data Architecture”.",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 151 §Promotion Attribution & KPI Engine"
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
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** Excel, CSV, PDF, Power BI, API, Scheduled report. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 151 §Subject to permissions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The executive promotion intelligence list.",
   "error": "Could not load. Names which read failed and leaves the executive promotion intelligence untouched.",
   "emptyFirstRun": "No executive promotion intelligence yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the executive promotion intelligence are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listExecutivePromotionReporting",
    "contract": "promotions",
    "purpose": "Executive Promotion Intelligence & Reporting Studio",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "↓"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-237"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 151. 0 of 1 labels bound to a contract property; 9 of 137 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "listBundleBogoAdvanced": {
  "method": "GET",
  "path": "/bundle-bogo-advanced",
  "contract": "promotions",
  "summary": "Bundle, BOGO & Advanced Offer Analytics",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "BundleBogoAdvancedOfferAnalyticsView"
 },
 "listCampaignPromotionPerformance": {
  "method": "GET",
  "path": "/campaign-promotion-performance",
  "contract": "promotions",
  "summary": "Campaign & Promotion Performance Explorer",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "CampaignPromotionPerformanceExplorerView"
 },
 "listCustomerSegmentChannel": {
  "method": "GET",
  "path": "/customer-segment-channel",
  "contract": "promotions",
  "summary": "Customer, Segment, Channel & Partner Analytics",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "CustomerSegmentChannelPartnerAnalyticsView"
 },
 "listDiscountMarginProfitability": {
  "method": "GET",
  "path": "/discount-margin-profitability",
  "contract": "promotions",
  "summary": "Discount, Margin & Profitability Analytics",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "DiscountMarginProfitabilityAnalyticsView"
 },
 "listExecutivePromotionReporting": {
  "method": "GET",
  "path": "/executive-promotion-reporting",
  "contract": "promotions",
  "summary": "Executive Promotion Intelligence & Reporting Studio",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ExecutivePromotionIntelligenceReportingStudioView"
 },
 "listIncrementalityAttributionCannibalization": {
  "method": "GET",
  "path": "/incrementality-attribution-cannibalization",
  "contract": "promotions",
  "summary": "Incrementality, Attribution & Cannibalization Analysis",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "IncrementalityAttributionCannibalizationAnalysisView"
 },
 "listNextBestAction": {
  "method": "GET",
  "path": "/next-best-action",
  "contract": "promotions",
  "summary": "AI Optimization & Next-Best-Action Center",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AiOptimizationNextBestActionCenterView"
 },
 "listPromotionPerformance": {
  "method": "GET",
  "path": "/promotion-performance",
  "contract": "promotions",
  "summary": "Promotion Performance Command Center",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "PromotionPerformanceCommandCenterView"
 },
 "listRedemptionConversionFunnel": {
  "method": "GET",
  "path": "/redemption-conversion-funnel",
  "contract": "promotions",
  "summary": "Redemption, Conversion & Funnel Analytics",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
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
    "name": "membershipTier",
    "in": "query",
    "required": false
   },
   {
    "name": "product",
    "in": "query",
    "required": false
   },
   {
    "name": "venue",
    "in": "query",
    "required": false
   },
   {
    "name": "campaign",
    "in": "query",
    "required": false
   },
   {
    "name": "promotionType",
    "in": "query",
    "required": false
   },
   {
    "name": "dayTime",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "RedemptionConversionFunnelAnalyticsView"
 },
 "listUpsellCrossSell": {
  "method": "GET",
  "path": "/upsell-cross-sell",
  "contract": "promotions",
  "summary": "Upsell, Cross-Sell & Attach-Rate Analytics",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "UpsellCrossSellAttachRateAnalyticsView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AiOptimizationNextBestActionCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What AI Optimization & Next-Best-Action Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "increaseDiscount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Increase discount"
   },
   "reduceDiscount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Reduce discount"
   },
   "changeMechanic": {
    "type": "string",
    "description": "Change mechanic"
   },
   "endPromotion": {
    "type": "string",
    "description": "End promotion"
   },
   "changeThreshold": {
    "type": "integer",
    "description": "Change threshold"
   },
   "expandSegment": {
    "type": "string",
    "description": "Expand segment"
   },
   "narrowSegment": {
    "type": "string",
    "description": "Narrow segment"
   },
   "excludeSegment": {
    "type": "string",
    "description": "Exclude segment"
   },
   "changeBundlePrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Change bundle price"
   },
   "expandChannel": {
    "type": "string",
    "description": "Expand channel"
   },
   "restrictChannel": {
    "type": "string",
    "description": "Restrict channel"
   },
   "reallocateCampaignBudget": {
    "type": "string",
    "description": "Reallocate campaign budget"
   },
   "changeDay": {
    "type": "string",
    "description": "Change day"
   },
   "changeTime": {
    "type": "string",
    "format": "date-time",
    "description": "Change time"
   },
   "reduceCampaignDuration": {
    "type": "string",
    "format": "date-time",
    "description": "Reduce campaign duration"
   },
   "revenueAed42k": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue: −AED 42K"
   },
   "grossProfitAed186k": {
    "type": "string",
    "description": "Gross Profit: +AED 186K"
   },
   "acceptAsDraft": {
    "type": "string",
    "description": "Accept as Draft"
   },
   "simulate": {
    "type": "string",
    "description": "Simulate"
   },
   "snooze": {
    "type": "string",
    "description": "Snooze"
   }
  }
 },
 "BundleBogoAdvancedOfferAnalyticsView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Bundle, BOGO & Advanced Offer Analytics displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "bundleSales": {
    "type": "integer",
    "description": "Bundle Sales"
   },
   "bundleRevenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Bundle Revenue"
   },
   "bundleConversion": {
    "type": "number",
    "description": "Bundle Conversion"
   },
   "bundleAov": {
    "type": "string",
    "description": "Bundle AOV"
   },
   "componentAttachRate": {
    "type": "number",
    "description": "Component Attach Rate"
   },
   "componentRedemption": {
    "type": "string",
    "description": "Component Redemption"
   },
   "bundleMargin": {
    "type": "number",
    "description": "Bundle Margin"
   },
   "bundleVsStandaloneRevenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Bundle vs Standalone Revenue"
   },
   "substitutionRate": {
    "type": "number",
    "description": "Substitution Rate"
   },
   "availabilityFailureRate": {
    "type": "number",
    "description": "Availability Failure Rate"
   },
   "bogoTransactions": {
    "type": "integer",
    "description": "BOGO transactions"
   },
   "freeItemsIssued": {
    "type": "string",
    "description": "Free items issued"
   },
   "averageRewardValue": {
    "type": "number",
    "description": "Average reward value"
   },
   "incrementalUnits": {
    "type": "integer",
    "description": "Incremental units"
   },
   "incrementalRevenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Incremental revenue"
   },
   "marginImpact": {
    "type": "number",
    "description": "Margin impact"
   },
   "waterPark100": {
    "type": "number",
    "description": "Water Park — 100%"
   },
   "aquarium100": {
    "type": "number",
    "description": "Aquarium — 100%"
   },
   "mealA68": {
    "type": "number",
    "description": "Meal A — 68%"
   },
   "mealB22": {
    "type": "number",
    "description": "Meal B — 22%"
   },
   "mealC10": {
    "type": "number",
    "description": "Meal C — 10%"
   },
   "photoAddOn31": {
    "type": "number",
    "description": "Photo Add-on — 31%"
   },
   "parking42": {
    "type": "number",
    "description": "Parking — 42%"
   }
  }
 },
 "CampaignPromotionPerformanceExplorerView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Campaign & Promotion Performance Explorer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "aed38": {
    "type": "string",
    "description": "AED 3.8"
   },
   "family20310k740k29118": {
    "type": "number",
    "description": "FAMILY20 310K 740K 29% 11.8%"
   },
   "summer1Aed26": {
    "type": "string",
    "description": "SUMMER1 AED 2.6"
   },
   "aed41": {
    "type": "string",
    "description": "AED 4.1"
   },
   "app1092k310k34132": {
    "type": "number",
    "description": "APP10 92K 310K 34% 13.2%"
   },
   "revenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue"
   },
   "transactions": {
    "type": "string",
    "description": "Transactions"
   },
   "units": {
    "type": "string",
    "description": "Units"
   },
   "redemptions": {
    "type": "string",
    "description": "Redemptions"
   },
   "discount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Discount"
   },
   "margin": {
    "type": "number",
    "description": "Margin"
   },
   "conversion": {
    "type": "number",
    "description": "Conversion"
   },
   "aov": {
    "type": "string",
    "description": "AOV"
   },
   "roi": {
    "type": "string",
    "description": "ROI"
   },
   "customerAcquisition": {
    "type": "string",
    "description": "Customer acquisition"
   },
   "repeatPurchase": {
    "type": "string",
    "description": "Repeat purchase"
   },
   "excellent": {
    "type": "string",
    "description": "Excellent"
   },
   "healthy": {
    "type": "string",
    "description": "Healthy"
   },
   "monitor": {
    "type": "string",
    "description": "Monitor"
   },
   "underperforming": {
    "type": "string",
    "description": "Underperforming"
   },
   "marginRisk": {
    "type": "number",
    "description": "Margin Risk"
   },
   "critical": {
    "type": "string",
    "description": "Critical"
   },
   "subjectToUserPermissions": {
    "type": "string",
    "description": "subject to user permissions"
   }
  }
 },
 "CustomerSegmentChannelPartnerAnalyticsView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Customer, Segment, Channel & Partner Analytics displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "customersReached": {
    "type": "string",
    "description": "Customers reached"
   },
   "newCustomers": {
    "type": "integer",
    "description": "New customers"
   },
   "returningCustomers": {
    "type": "integer",
    "description": "Returning customers"
   },
   "conversion": {
    "type": "number",
    "description": "Conversion"
   },
   "revenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue"
   },
   "discount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Discount"
   },
   "aov": {
    "type": "string",
    "description": "AOV"
   },
   "margin": {
    "type": "number",
    "description": "Margin"
   },
   "repeatPurchase": {
    "type": "string",
    "description": "Repeat purchase"
   },
   "redemption": {
    "type": "string",
    "description": "Redemption"
   },
   "ntOnN": {
    "type": "string",
    "description": "nt on n"
   },
   "aed44": {
    "type": "string",
    "description": "AED 4.4"
   },
   "families14229": {
    "type": "number",
    "description": "Families 14.2% 29%"
   },
   "aed32": {
    "type": "string",
    "description": "AED 3.2"
   },
   "tourists9834": {
    "type": "number",
    "description": "Tourists 9.8% 34%"
   },
   "memberAed51": {
    "type": "string",
    "description": "Member AED 5.1"
   },
   "s710X": {
    "type": "string",
    "description": "s 710 x"
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
    "type": "string",
    "description": "POS"
   },
   "kiosk": {
    "type": "string",
    "description": "Kiosk"
   },
   "b2b": {
    "type": "string",
    "description": "B2B"
   },
   "callCenter": {
    "type": "string",
    "description": "Call Center"
   },
   "ota": {
    "type": "string",
    "description": "OTA"
   },
   "reseller": {
    "type": "string",
    "description": "Reseller"
   },
   "api": {
    "type": "string",
    "description": "API"
   },
   "partnerRevenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Partner revenue"
   },
   "partnerRedemptions": {
    "type": "integer",
    "description": "Partner redemptions"
   },
   "discountCost": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Discount cost"
   },
   "commission": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Commission"
   },
   "netContribution": {
    "type": "string",
    "description": "Net contribution"
   },
   "campaignRoi": {
    "type": "string",
    "description": "Campaign ROI"
   }
  }
 },
 "DiscountMarginProfitabilityAnalyticsView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Discount, Margin & Profitability Analytics displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "grossRevenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Gross Revenue"
   },
   "discountValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Discount Value"
   },
   "netRevenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Net Revenue"
   },
   "productCost": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Product Cost"
   },
   "promotionCost": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Promotion Cost"
   },
   "grossProfit": {
    "type": "string",
    "description": "Gross Profit"
   },
   "grossMargin": {
    "type": "number",
    "description": "Gross Margin %"
   },
   "marginChange": {
    "type": "number",
    "description": "Margin Change"
   },
   "revenueUplift": {
    "type": "number",
    "description": "Revenue Uplift"
   },
   "profitUplift": {
    "type": "number",
    "description": "Profit Uplift"
   },
   "roi": {
    "type": "string",
    "description": "ROI"
   },
   "toIdentify": {
    "type": "string",
    "description": "to identify"
   },
   "highRevenueHighMargin": {
    "type": "number",
    "description": "High revenue / high margin"
   },
   "highRevenueLowMargin": {
    "type": "number",
    "description": "High revenue / low margin"
   },
   "lowRevenueHighMargin": {
    "type": "number",
    "description": "Low revenue / high margin"
   },
   "lowRevenueLowMargin": {
    "type": "number",
    "description": "Low revenue / low margin"
   }
  }
 },
 "ExecutivePromotionIntelligenceReportingStudioView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Executive Promotion Intelligence & Reporting Studio displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "dashboards": {
    "type": "string",
    "description": "dashboards"
   },
   "productRelationship": {
    "type": "string",
    "description": "product relationship"
   },
   "higherValueOption": {
    "type": "string",
    "description": "higher-value option"
   },
   "by": {
    "type": "string",
    "description": "by"
   },
   "incrementalRevenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Incremental revenue"
   },
   "profit": {
    "type": "string",
    "description": "Profit"
   },
   "roi": {
    "type": "string",
    "description": "ROI"
   },
   "conversion": {
    "type": "number",
    "description": "Conversion"
   },
   "aov": {
    "type": "string",
    "description": "AOV"
   },
   "negativeMarginImpact": {
    "type": "number",
    "description": "Negative margin impact"
   },
   "lowConversion": {
    "type": "number",
    "description": "Low conversion"
   },
   "highDiscountCost": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "High discount cost"
   },
   "lowIncrementality": {
    "type": "string",
    "description": "Low incrementality"
   },
   "metric": {
    "type": "string",
    "description": "Metric"
   },
   "dimension": {
    "type": "string",
    "description": "Dimension"
   },
   "date": {
    "type": "string",
    "format": "date-time",
    "description": "Date"
   },
   "comparisonPeriod": {
    "type": "string",
    "format": "date-time",
    "description": "Comparison period"
   },
   "grouping": {
    "type": "string",
    "description": "Grouping"
   },
   "visualization": {
    "type": "string",
    "description": "Visualization"
   },
   "excel": {
    "type": "string",
    "description": "Excel"
   },
   "csv": {
    "type": "string",
    "description": "CSV"
   },
   "pdf": {
    "type": "string",
    "description": "PDF"
   },
   "powerBi": {
    "type": "string",
    "description": "Power BI"
   },
   "api": {
    "type": "string",
    "description": "API"
   },
   "scheduledReport": {
    "type": "string",
    "format": "date-time",
    "description": "Scheduled report"
   },
   "transactionPromotionEvents": {
    "type": "string",
    "description": "Transaction + Promotion Events"
   },
   "reward": {
    "type": "string",
    "description": "reward"
   },
   "accordingToConfiguredFinancialRules": {
    "type": "string",
    "description": "according to configured financial rules"
   },
   "executive": {
    "type": "string",
    "description": "Executive"
   },
   "marketing": {
    "type": "string",
    "description": "Marketing"
   },
   "commercial": {
    "type": "string",
    "description": "Commercial"
   },
   "revenueManagement": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue Management"
   },
   "finance": {
    "type": "string",
    "description": "Finance"
   },
   "venueManagement": {
    "type": "string",
    "description": "Venue Management"
   },
   "b2b": {
    "type": "string",
    "description": "B2B"
   },
   "crm": {
    "type": "string",
    "description": "CRM"
   },
   "dataAnalyst": {
    "type": "string",
    "description": "Data Analyst"
   },
   "auditor": {
    "type": "string",
    "description": "Auditor"
   },
   "systemAdministrator": {
    "type": "string",
    "description": "System Administrator"
   },
   "familySegmentConversion142": {
    "type": "number",
    "description": "Family Segment — Conversion 14.2%"
   }
  }
 },
 "IncrementalityAttributionCannibalizationAnalysisView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Incrementality, Attribution & Cannibalization Analysis displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "directAttribution": {
    "type": "string",
    "description": "Direct attribution"
   },
   "promotionCodeAttribution": {
    "type": "string",
    "description": "Promotion-code attribution"
   },
   "campaignAttribution": {
    "type": "string",
    "description": "Campaign attribution"
   },
   "controlGroupComparison": {
    "type": "string",
    "description": "Control-group comparison"
   },
   "aBTestAttribution": {
    "type": "string",
    "description": "A/B test attribution"
   },
   "prePostComparison": {
    "type": "string",
    "description": "Pre/post comparison"
   },
   "matchedAudienceAnalysis": {
    "type": "string",
    "description": "Matched audience analysis"
   },
   "aiEstimatedIncrementality": {
    "type": "string",
    "description": "AI-estimated incrementality"
   },
   "aed50m": {
    "type": "string",
    "description": "AED 5.0M"
   },
   "aed38m": {
    "type": "string",
    "description": "AED 3.8M"
   },
   "aed12m": {
    "type": "string",
    "description": "AED 1.2M"
   },
   "standardTicketDiscountedTicket": {
    "type": "string",
    "description": "Standard ticket → discounted ticket"
   },
   "higherMarginBundleLowerMarginPromotion": {
    "type": "number",
    "description": "Higher-margin bundle → lower-margin promotion"
   },
   "channelMigrationCausedByDiscounting": {
    "type": "string",
    "description": "Channel migration caused by discounting"
   }
  }
 },
 "PromotionPerformanceCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Promotion Performance Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "dateRange": {
    "type": "string",
    "format": "date-time",
    "description": "Date range"
   },
   "businessEntity": {
    "type": "string",
    "description": "Business entity"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "attraction": {
    "type": "string",
    "description": "Attraction"
   },
   "campaign": {
    "type": "string",
    "description": "Campaign"
   },
   "promotion": {
    "type": "string",
    "description": "Promotion"
   },
   "bundle": {
    "type": "string",
    "description": "Bundle"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "customerSegment": {
    "type": "string",
    "description": "Customer segment"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "partner": {
    "type": "string",
    "description": "Partner"
   },
   "market": {
    "type": "string",
    "description": "Market"
   },
   "currency": {
    "type": "string",
    "description": "Currency"
   },
   "grossSales": {
    "type": "integer",
    "description": "Gross Sales"
   },
   "promotionInfluencedRevenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Promotion-Influenced Revenue"
   },
   "estimatedIncrementalRevenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Estimated Incremental Revenue"
   },
   "discountGranted": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Discount Granted"
   },
   "netRevenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Net Revenue"
   },
   "grossMargin": {
    "type": "number",
    "description": "Gross Margin"
   },
   "promotionCost": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Promotion Cost"
   },
   "roi": {
    "type": "string",
    "description": "ROI"
   },
   "transactions": {
    "type": "integer",
    "description": "Transactions"
   },
   "redemptions": {
    "type": "integer",
    "description": "Redemptions"
   },
   "conversionRate": {
    "type": "number",
    "description": "Conversion Rate"
   },
   "averageOrderValue": {
    "type": "number",
    "description": "Average Order Value"
   },
   "revenuePerRedemption": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue per Redemption"
   },
   "activeCampaigns": {
    "type": "integer",
    "description": "Active Campaigns"
   },
   "overTime": {
    "type": "string",
    "format": "date-time",
    "description": "over time"
   }
  }
 },
 "RedemptionConversionFunnelAnalyticsView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Redemption, Conversion & Funnel Analytics displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "exposureRate": {
    "type": "number",
    "description": "Exposure rate"
   },
   "engagementRate": {
    "type": "number",
    "description": "Engagement rate"
   },
   "cartRate": {
    "type": "number",
    "description": "Cart rate"
   },
   "conversionRate": {
    "type": "number",
    "description": "Conversion rate"
   },
   "redemptionRate": {
    "type": "number",
    "description": "Redemption rate"
   },
   "abandonment": {
    "type": "string",
    "description": "Abandonment"
   },
   "unusedPromotionRate": {
    "type": "number",
    "description": "Unused promotion rate"
   },
   "expiredBenefitRate": {
    "type": "integer",
    "description": "Expired benefit rate"
   }
  }
 },
 "UpsellCrossSellAttachRateAnalyticsView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Upsell, Cross-Sell & Attach-Rate Analytics displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "crossSellRevenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Cross-Sell Revenue"
   },
   "upsellRevenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Upsell Revenue"
   },
   "attachRate": {
    "type": "number",
    "description": "Attach Rate"
   },
   "itemsPerTransaction": {
    "type": "string",
    "description": "Items per Transaction"
   },
   "revenuePerTransaction": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue per Transaction"
   },
   "recommendedOfferAcceptance": {
    "type": "string",
    "description": "Recommended Offer Acceptance"
   },
   "incrementalBasketValue": {
    "type": "string",
    "description": "Incremental Basket Value"
   },
   "crossCategoryConversion": {
    "type": "number",
    "description": "Cross-Category Conversion"
   },
   "ticketTicket": {
    "type": "string",
    "description": "Ticket → Ticket"
   },
   "ticketFB": {
    "type": "string",
    "description": "Ticket → F&B"
   },
   "ticketRetail": {
    "type": "string",
    "description": "Ticket → Retail"
   },
   "ticketExperience": {
    "type": "string",
    "description": "Ticket → Experience"
   },
   "ticketMembership": {
    "type": "string",
    "description": "Ticket → Membership"
   },
   "fBRetail": {
    "type": "string",
    "description": "F&B → Retail"
   },
   "retailFB": {
    "type": "string",
    "description": "Retail → F&B"
   },
   "membershipExperience": {
    "type": "string",
    "description": "Membership → Experience"
   }
  }
 }
}
```
