# WS185 — Upsell,CrossSellEngine board 6

**10 screens · 8 operations · 4 schemas · 3 permissions**

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
  `AI_USE, PRODUCT_CONFIGURE, PRODUCT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-689` | Recommendation Performance Command Center | commandCentre | 1 | 0 | — |
| `ADM-690` | Recommendation Strategy & Placement Analytics | listDetail | 1 | 0 | — |
| `ADM-691` | Recommendation Experiment & A/B Test Studio | commandCentre | 2 | 0 | — |
| `ADM-692` | Experiment Results & Winner Decision Workspace | listDetail | 2 | 0 | — |
| `ADM-693` | Recommendation Attribution & Incrementality Analytics | configEditor | 1 | 0 | — |
| `ADM-694` | AI Model Performance & Drift Monitor | listDetail | 1 | 0 | — |
| `ADM-695` | Recommendation Governance & Deployment Control | listDetail | 2 | 0 | — |
| `ADM-696` | AI Risk, Fairness, Explainability & Safety Center | listDetail | 1 | 3 | — |
| `ADM-697` | Recommendation Audit, Decision Trace & Investigation | listDetail | 1 | 0 | — |
| `ADM-698` | AI Optimization & Recommendation Intelligence Lab | listDetail | 1 | 0 | — |

## Thin screens in this batch

**ADM-690, ADM-694, ADM-697 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-689",
  "name": "Recommendation Performance Command Center",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Upsell,CrossSellEngine.pdf",
   "board": "6",
   "number": "1",
   "page": 153
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/recommendation-performance-command-center-adm-689",
   "component": "apps/ticvai-web/src/routes/commercial/RecommendationPerformanceCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-690",
    "ADM-691",
    "ADM-692",
    "ADM-693",
    "ADM-694",
    "ADM-695",
    "ADM-696",
    "ADM-697",
    "ADM-698"
   ],
   "transitions": [
    {
     "to": "ADM-002",
     "trigger": "Back to Platform Dashboard",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "ADM-690",
     "trigger": "Recommendation Strategy & Placement Analytics",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    },
    {
     "to": "ADM-691",
     "trigger": "Recommendation Experiment & A/B Test Studio",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    },
    {
     "to": "ADM-692",
     "trigger": "Experiment Results & Winner Decision Workspace",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    },
    {
     "to": "ADM-693",
     "trigger": "Recommendation Attribution & Incrementality Analytics",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    },
    {
     "to": "ADM-694",
     "trigger": "AI Model Performance & Drift Monitor",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    },
    {
     "to": "ADM-695",
     "trigger": "Recommendation Governance & Deployment Control",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    },
    {
     "to": "ADM-696",
     "trigger": "AI Risk, Fairness, Explainability & Safety Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    },
    {
     "to": "ADM-697",
     "trigger": "Recommendation Audit, Decision Trace & Investigation",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    },
    {
     "to": "ADM-698",
     "trigger": "AI Optimization & Recommendation Intelligence Lab",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide executive and operational visibility across the complete Recommendation Engine.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search recommendation performance",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 153 §Analyze by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Upsell",
        "Cross-sell",
        "Membership",
        "Bundle",
        "F&B",
        "Retail",
        "Experience",
        "Ancillary",
        "Channel",
        "Venue",
        "Customer segment"
       ],
       "notes": "The pack filters this screen by upsell, cross-sell, membership, bundle, f&b, retail and 5 more — which are present is a decision the pack already made.",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 153 §Analyze by"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Recommendations Generated",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 153 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Recommendations Presented",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 153 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Recommendations Accepted",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 153 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Recommendation Conversion",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 153 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Upsell Revenue",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 153 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Cross-Sell Revenue",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 153 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Estimated Incremental Revenue",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 153 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "AOV Uplift",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 153 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Attach Rate",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 153 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Incremental Margin",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 153 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "AI Recommendation Share",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 153 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Rule-Based Recommendation Share",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 153 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Suppression Rate",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 153 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Active Experiments",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 153 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Model Health",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 153 §KPI Cards"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The recommendation performance list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the recommendation performance untouched.",
   "emptyFirstRun": "No recommendation performance yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the recommendation performance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getRecommendationPerformance",
    "contract": "promotions",
    "purpose": "The headline numbers",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-689",
   "workshopBoard": "wireframes/WS183 Upsell,CrossSellEngine Board 6.dc.html#adm-689"
  },
  "apisNote": "Regenerated 9 September 2026 from Upsell,CrossSellEngine.pdf page 153. 0 of 11 labels bound to a contract property; 26 of 38 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-690",
  "name": "Recommendation Strategy & Placement Analytics",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Upsell,CrossSellEngine.pdf",
   "board": "6",
   "number": "2",
   "page": 155
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/recommendation-strategy-placement-analytics-adm-690",
   "component": "apps/ticvai-web/src/routes/commercial/RecommendationStrategyPlacementAnalytics.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-689"
   ],
   "exitTo": [
    "ADM-689"
   ],
   "transitions": [
    {
     "to": "ADM-689",
     "trigger": "Back to Recommendation Performance Command Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Compare) and no metric row",
  "purpose": "Determine which recommendation strategies, placements, channels and journey stages perform best.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 155 §Compare"
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
       "label": "Every recommendation strategy placement",
       "columns": [
        "Ticket Selection",
        "Cart",
        "Checkout",
        "Confirmation",
        "Pre-Visit",
        "Mobile App",
        "In-Venue",
        "Post-Visit",
        "B2C",
        "App",
        "POS",
        "Kiosk",
        "B2B",
        "Call Center",
        "API/Partner"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 155 §Compare"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected recommendation strategy placement",
       "bindsTo": null,
       "columns": [
        "Ticket Selection",
        "Cart",
        "Checkout",
        "Confirmation",
        "Pre-Visit",
        "Mobile App",
        "In-Venue",
        "Post-Visit",
        "B2C",
        "App",
        "POS",
        "Kiosk",
        "B2B",
        "Call Center",
        "API/Partner"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Strategy”, “Max”, “Relevance”, “Cart conversion”, “Checkout conversion”.",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 155 §Compare"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The recommendation strategy placement list.",
   "error": "Could not load. Names which read failed and leaves the recommendation strategy placement untouched.",
   "emptyFirstRun": "No recommendation strategy placement yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the recommendation strategy placement are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getRecommendationPerformance",
    "contract": "promotions",
    "purpose": "By strategy and placement",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Ticket Selection",
    "Cart",
    "Checkout",
    "Confirmation",
    "Pre-Visit",
    "Mobile App"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-690",
   "workshopBoard": "wireframes/WS183 Upsell,CrossSellEngine Board 6.dc.html#adm-690"
  },
  "apisNote": "Regenerated 9 September 2026 from Upsell,CrossSellEngine.pdf page 155. 0 of 15 labels bound to a contract property; 15 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-691",
  "name": "Recommendation Experiment & A/B Test Studio",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Upsell,CrossSellEngine.pdf",
   "board": "6",
   "number": "3",
   "page": 156
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/recommendation-experiment-a-b-test-studio-adm-691",
   "component": "apps/ticvai-web/src/routes/commercial/RecommendationExperimentABTestStudio.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-689"
   ],
   "exitTo": [
    "ADM-689"
   ],
   "transitions": [
    {
     "to": "ADM-689",
     "trigger": "Back to Recommendation Performance Command Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Measure) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Allow TICVAI to scientifically test recommendation strategies rather than relying only on assumptions. Increase Family Meal cross-sell.",
  "gaps": [
   {
    "operation": null,
    "why": "**Recommendation Experiment & A/B Test Studio declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
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
       "label": "Conversion",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 156 §Measure"
      },
      {
       "kind": "metricTile",
       "label": "Attach rate",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 156 §Measure"
      },
      {
       "kind": "metricTile",
       "label": "Revenue",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 156 §Measure"
      },
      {
       "kind": "metricTile",
       "label": "Incremental revenue",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 156 §Measure"
      },
      {
       "kind": "metricTile",
       "label": "AOV",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 156 §Measure"
      },
      {
       "kind": "metricTile",
       "label": "Margin",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 156 §Measure"
      },
      {
       "kind": "metricTile",
       "label": "Customer response",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 156 §Measure"
      },
      {
       "kind": "metricTile",
       "label": "Recommendation fatigue",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 156 §Measure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The recommendation experiment test list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the recommendation experiment test untouched.",
   "emptyFirstRun": "No recommendation experiment test yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the recommendation experiment test are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listRecommendationExperiments",
    "contract": "promotions",
    "purpose": "Experiments running",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "createRecommendationExperiment",
    "contract": "promotions",
    "purpose": "Start one",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listRecommendationExperiments"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-691",
   "workshopBoard": "wireframes/WS183 Upsell,CrossSellEngine Board 6.dc.html#adm-691"
  },
  "apisNote": "Regenerated 9 September 2026 from Upsell,CrossSellEngine.pdf page 156. 0 of 0 labels bound to a contract property; 8 of 27 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-692",
  "name": "Experiment Results & Winner Decision Workspace",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Upsell,CrossSellEngine.pdf",
   "board": "6",
   "number": "4",
   "page": 158
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/experiment-results-winner-decision-workspace-adm-692",
   "component": "apps/ticvai-web/src/routes/commercial/ExperimentResultsWinnerDecisionWorkspace.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-689"
   ],
   "exitTo": [
    "ADM-689"
   ],
   "transitions": [
    {
     "to": "ADM-689",
     "trigger": "Back to Recommendation Performance Command Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Evaluate experiments and decide whether a recommendation strategy should be deployed.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 158"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 158"
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
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** Declare Winner, Extend Test, Stop Test, Reject Result, Create Deployment Draft, Send for Approval. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 158 §Authorized users can"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listRecommendationExperiments",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "concludeRecommendationExperiment",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "concludeRecommendationExperiment"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The experiment results winner list.",
   "error": "Could not load. Names which read failed and leaves the experiment results winner untouched.",
   "emptyFirstRun": "No experiment results winner yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the experiment results winner are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listRecommendationExperiments",
    "contract": "promotions",
    "purpose": "Results so far",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "concludeRecommendationExperiment",
    "contract": "promotions",
    "purpose": "Declare a winner",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listRecommendationExperiments",
     "listRecommendationStrategies"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-692",
   "workshopBoard": "wireframes/WS183 Upsell,CrossSellEngine Board 6.dc.html#adm-692"
  },
  "apisNote": "Regenerated 9 September 2026 from Upsell,CrossSellEngine.pdf page 158. 0 of 0 labels bound to a contract property; 6 of 23 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "experimentId",
     "from": "navigation"
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
  "id": "ADM-693",
  "name": "Recommendation Attribution & Incrementality Analytics",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Upsell,CrossSellEngine.pdf",
   "board": "6",
   "number": "5",
   "page": 159
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/recommendation-attribution-incrementality-analytics-adm-693",
   "component": "apps/ticvai-web/src/routes/commercial/RecommendationAttributionIncrementalityAnalytics.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-689"
   ],
   "exitTo": [
    "ADM-689"
   ],
   "transitions": [
    {
     "to": "ADM-689",
     "trigger": "Back to Recommendation Performance Command Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Determine whether a recommendation genuinely created additional commercial value. This is essential. A customer purchasing a recommended product does not automatically mean the recommendation caused the purchase.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 4 actions on this screen and the screen declares 0 operations.** Unserved: Recommendation tracking ID, Last recommendation, First recommendation, A/B experiment. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 159 §Support, where data permits"
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
       "label": "Same session",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 159 §Configure"
      },
      {
       "kind": "selectField",
       "label": "24 hours",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 159 §Configure"
      },
      {
       "kind": "selectField",
       "label": "7 days",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 159 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Until visit",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 159 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Custom",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 159 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Recommendation tracking ID",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 159 §Support, where data permits"
      },
      {
       "kind": "secondaryButton",
       "label": "Last recommendation",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 159 §Support, where data permits"
      },
      {
       "kind": "secondaryButton",
       "label": "First recommendation",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 159 §Support, where data permits"
      },
      {
       "kind": "secondaryButton",
       "label": "A/B experiment",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 159 §Support, where data permits"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The recommendation attribution incrementality configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the recommendation attribution incrementality untouched.",
   "emptyFirstRun": "No recommendation attribution incrementality configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "getRecommendationPerformance",
    "contract": "promotions",
    "purpose": "Attributed against incremental",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-693",
   "workshopBoard": "wireframes/WS183 Upsell,CrossSellEngine Board 6.dc.html#adm-693"
  },
  "apisNote": "Regenerated 9 September 2026 from Upsell,CrossSellEngine.pdf page 159. 0 of 0 labels bound to a contract property; 16 of 29 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-694",
  "name": "AI Model Performance & Drift Monitor",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Upsell,CrossSellEngine.pdf",
   "board": "6",
   "number": "6",
   "page": 161
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/ai-model-performance-drift-monitor-adm-694",
   "component": "apps/ticvai-web/src/routes/commercial/AiModelPerformanceDriftMonitor.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-689"
   ],
   "exitTo": [
    "ADM-689"
   ],
   "transitions": [
    {
     "to": "ADM-689",
     "trigger": "Back to Recommendation Performance Command Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show; Detect) and no metric row",
  "purpose": "Monitor whether recommendation and propensity models continue performing correctly after deployment. This screen is critical if TICVAI wants a serious AI architecture.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 161 §Show"
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
       "label": "Every model performance drift",
       "columns": [
        "Model",
        "Version",
        "Purpose",
        "Deployment date",
        "Status",
        "Last evaluation",
        "Data freshness",
        "Input drift",
        "Behavioral drift",
        "Performance drift",
        "Segment drift",
        "Product mix change"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 161 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected model performance drift",
       "bindsTo": null,
       "columns": [
        "Model",
        "Version",
        "Purpose",
        "Deployment date",
        "Status",
        "Last evaluation",
        "Data freshness",
        "Input drift",
        "Behavioral drift",
        "Performance drift",
        "Segment drift",
        "Product mix change"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Models Could Include”.",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 161 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The model performance drift list.",
   "error": "Could not load. Names which read failed and leaves the model performance drift untouched.",
   "emptyFirstRun": "No model performance drift yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the model performance drift are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getRecommendationPerformance",
    "contract": "promotions",
    "purpose": "Model performance over time",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Model",
    "Version",
    "Purpose",
    "Deployment date",
    "Status",
    "Last evaluation"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-694",
   "workshopBoard": "wireframes/WS183 Upsell,CrossSellEngine Board 6.dc.html#adm-694"
  },
  "apisNote": "Regenerated 9 September 2026 from Upsell,CrossSellEngine.pdf page 161. 0 of 12 labels bound to a contract property; 12 of 31 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-695",
  "name": "Recommendation Governance & Deployment Control",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Upsell,CrossSellEngine.pdf",
   "board": "6",
   "number": "7",
   "page": 162
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/recommendation-governance-deployment-control-adm-695",
   "component": "apps/ticvai-web/src/routes/commercial/RecommendationGovernanceDeploymentControl.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-689"
   ],
   "exitTo": [
    "ADM-689"
   ],
   "transitions": [
    {
     "to": "ADM-689",
     "trigger": "Back to Recommendation Performance Command Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Monitor) and no metric row",
  "purpose": "Control how new strategies, rules, models and AI changes move into production.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 2 actions on this screen and the screen declares 0 operations.** Unserved: Channel rollout, Venue rollout. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 162 §Support"
   },
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 162 §Monitor"
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
       "label": "Every recommendation governance deployment",
       "columns": [
        "↓"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 162 §Monitor"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected recommendation governance deployment",
       "bindsTo": null,
       "columns": [
        "↓"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Draft”, “Testing”, “Simulation”, “Approval”, “Scheduled”, “Active”.",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 162 §Monitor"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Channel rollout",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 162 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Venue rollout",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 162 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The recommendation governance deployment list.",
   "error": "Could not load. Names which read failed and leaves the recommendation governance deployment untouched.",
   "emptyFirstRun": "No recommendation governance deployment yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the recommendation governance deployment are still there. The pack's own statuses are Recommendation strategy — the state names which is selected.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listRecommendationStrategies",
    "contract": "promotions",
    "purpose": "What is deployed where",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "updateRecommendationStrategy",
    "contract": "promotions",
    "purpose": "Pause or retire",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listRecommendationStrategies"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "↓"
   ],
   "params": [
    {
     "name": "strategyId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-695",
   "workshopBoard": "wireframes/WS183 Upsell,CrossSellEngine Board 6.dc.html#adm-695"
  },
  "apisNote": "Regenerated 9 September 2026 from Upsell,CrossSellEngine.pdf page 162. 0 of 1 labels bound to a contract property; 11 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-696",
  "name": "AI Risk, Fairness, Explainability & Safety Center",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Upsell,CrossSellEngine.pdf",
   "board": "6",
   "number": "8",
   "page": 164
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/ai-risk-fairness-explainability-safety-center-adm-696",
   "component": "apps/ticvai-web/src/routes/commercial/AiRiskFairnessExplainabilitySafetyCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-689"
   ],
   "exitTo": [
    "ADM-689"
   ],
   "transitions": [
    {
     "to": "ADM-689",
     "trigger": "Back to Recommendation Performance Command Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide governance over how AI recommendation decisions behave across customer populations and business contexts.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 5 actions on this screen and the screen declares 0 operations.** Unserved: Disable model, Disable recommendation type, Disable specific relationship, Raise confidence threshold, Emergency suspend. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 164 §Allow"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 164"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 164"
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
       "kind": "destructiveButton",
       "label": "Disable model",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 164 §Allow"
      },
      {
       "kind": "destructiveButton",
       "label": "Disable recommendation type",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 164 §Allow"
      },
      {
       "kind": "destructiveButton",
       "label": "Disable specific relationship",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 164 §Allow"
      },
      {
       "kind": "secondaryButton",
       "label": "Raise confidence threshold",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 164 §Allow"
      },
      {
       "kind": "secondaryButton",
       "label": "Emergency suspend",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 164 §Allow"
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
    "id": "confirmDisableModel",
    "component": "confirmDialog",
    "trigger": "Disable model",
    "body": "**Disable model on a risk fairness explainability is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Upsell,CrossSellEngine.pdf, page 164 §Allow"
   },
   {
    "id": "confirmDisableRecommendationTyp",
    "component": "confirmDialog",
    "trigger": "Disable recommendation type",
    "body": "**Disable recommendation type on a risk fairness explainability is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Upsell,CrossSellEngine.pdf, page 164 §Allow"
   },
   {
    "id": "confirmDisableSpecificRelations",
    "component": "confirmDialog",
    "trigger": "Disable specific relationship",
    "body": "**Disable specific relationship on a risk fairness explainability is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Upsell,CrossSellEngine.pdf, page 164 §Allow"
   }
  ],
  "states": {
   "loading": "The risk fairness explainability list.",
   "error": "Could not load. Names which read failed and leaves the risk fairness explainability untouched.",
   "emptyFirstRun": "No risk fairness explainability yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the risk fairness explainability are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "explainRecommendationDecision",
    "contract": "ai",
    "purpose": "Why these recommendations",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-696",
   "workshopBoard": "wireframes/WS183 Upsell,CrossSellEngine Board 6.dc.html#adm-696"
  },
  "apisNote": "Regenerated 9 September 2026 from Upsell,CrossSellEngine.pdf page 164. 0 of 0 labels bound to a contract property; 5 of 26 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "decisionId",
     "from": "navigation"
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
  "id": "ADM-697",
  "name": "Recommendation Audit, Decision Trace & Investigation",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Upsell,CrossSellEngine.pdf",
   "board": "6",
   "number": "9",
   "page": 166
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/recommendation-audit-decision-trace-investigation-adm-697",
   "component": "apps/ticvai-web/src/routes/commercial/RecommendationAuditDecisionTraceInvestigation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-689"
   ],
   "exitTo": [
    "ADM-689"
   ],
   "transitions": [
    {
     "to": "ADM-689",
     "trigger": "Back to Recommendation Performance Command Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide transaction-level explainability for Customer Service, Commercial, Audit, and technical investigation.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 166"
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
       "label": "Search recommendation audit decision",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 166 §Search by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Recommendation ID",
        "Transaction",
        "Customer/session where permitted",
        "Ticket",
        "Product",
        "Date",
        "Channel",
        "Model",
        "Strategy"
       ],
       "notes": "The pack filters this screen by recommendation id, transaction, customer/session where permitted, ticket, product, date and 3 more — which are present is a decision the pack already made.",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 166 §Search by"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The recommendation audit decision list.",
   "error": "Could not load. Names which read failed and leaves the recommendation audit decision untouched.",
   "emptyFirstRun": "No recommendation audit decision yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the recommendation audit decision are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "explainRecommendationDecision",
    "contract": "ai",
    "purpose": "Why these recommendations",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-697",
   "workshopBoard": "wireframes/WS183 Upsell,CrossSellEngine Board 6.dc.html#adm-697"
  },
  "apisNote": "Regenerated 9 September 2026 from Upsell,CrossSellEngine.pdf page 166. 0 of 9 labels bound to a contract property; 9 of 38 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "decisionId",
     "from": "navigation"
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
  "id": "ADM-698",
  "name": "AI Optimization & Recommendation Intelligence Lab",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Upsell,CrossSellEngine.pdf",
   "board": "6",
   "number": "10",
   "page": 168
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/ai-optimization-recommendation-intelligence-lab-adm-698",
   "component": "apps/ticvai-web/src/routes/commercial/AiOptimizationRecommendationIntelligenceLab.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-689"
   ],
   "exitTo": [
    "ADM-689"
   ],
   "transitions": [
    {
     "to": "ADM-689",
     "trigger": "Back to Recommendation Performance Command Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Track; Measure) and no metric row",
  "purpose": "Turn all Recommendation Engine data into actionable improvement opportunities. This is the final optimization screen for Module 2.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 6 actions on this screen and the screen declares 0 operations.** Unserved: Simulate, Create Experiment, Create Draft, Send for Approval, Dismiss, Snooze. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 168 §Actions"
   },
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 168 §Track"
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
       "label": "Every optimization recommendation intelligence",
       "columns": [
        "↓"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 168 §Track"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected optimization recommendation intelligence",
       "bindsTo": null,
       "columns": [
        "↓"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Product Relationships”, “Ranking”, “Journey”, “Timing”, “Suppression”, “Strategy”.",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 168 §Track"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Simulate",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 168 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Create Experiment",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 168 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Create Draft",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 168 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Send for Approval",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 168 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Dismiss",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 168 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Snooze",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 168 §Actions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The optimization recommendation intelligence list.",
   "error": "Could not load. Names which read failed and leaves the optimization recommendation intelligence untouched.",
   "emptyFirstRun": "No optimization recommendation intelligence yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the optimization recommendation intelligence are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "simulateRecommendationStrategy",
    "contract": "promotions",
    "purpose": "Optimisation lab",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "↓"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-698",
   "workshopBoard": "wireframes/WS183 Upsell,CrossSellEngine Board 6.dc.html#adm-698"
  },
  "apisNote": "Regenerated 9 September 2026 from Upsell,CrossSellEngine.pdf page 168. 0 of 1 labels bound to a contract property; 7 of 80 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "concludeRecommendationExperiment": {
  "method": "POST",
  "path": "/recommendation-experiments/{experimentId}/conclude",
  "contract": "promotions",
  "summary": "Declare a winner and roll it out",
  "permission": "PRODUCT_CONFIGURE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "RecommendationExperiment"
 },
 "createRecommendationExperiment": {
  "method": "POST",
  "path": "/recommendation-experiments",
  "contract": "promotions",
  "summary": "Split traffic between strategies",
  "permission": "PRODUCT_CONFIGURE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "RecommendationExperiment",
  "responds": "RecommendationExperiment"
 },
 "explainRecommendationDecision": {
  "method": "GET",
  "path": "/recommendations/decisions/{decisionId}/explanation",
  "contract": "ai",
  "summary": "Why these recommendations",
  "permission": "AI_USE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "depth",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "AiRecommendationExplanation"
 },
 "getRecommendationPerformance": {
  "method": "GET",
  "path": "/recommendation-performance",
  "contract": "promotions",
  "summary": "Impressions, acceptance, revenue and incremental lift",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "from",
    "in": "query",
    "required": null
   },
   {
    "name": "to",
    "in": "query",
    "required": null
   },
   {
    "name": "groupBy",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "RecommendationPerformance"
 },
 "listRecommendationExperiments": {
  "method": "GET",
  "path": "/recommendation-experiments",
  "contract": "promotions",
  "summary": "A/B tests on placements and strategies",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "RecommendationExperiment"
 },
 "listRecommendationStrategies": {
  "method": "GET",
  "path": "/recommendation-strategies",
  "contract": "promotions",
  "summary": "The strategies deciding what gets offered where",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "placement",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "RecommendationStrategy"
 },
 "simulateRecommendationStrategy": {
  "method": "POST",
  "path": "/recommendation-simulations",
  "contract": "promotions",
  "summary": "Replay a strategy against history before it goes live",
  "permission": "PRODUCT_CONFIGURE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "RecommendationPerformance"
 },
 "updateRecommendationStrategy": {
  "method": "PUT",
  "path": "/recommendation-strategies/{strategyId}",
  "contract": "promotions",
  "summary": "Change a strategy",
  "permission": "PRODUCT_CONFIGURE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
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
  "requestBody": "RecommendationStrategy",
  "responds": "RecommendationStrategy"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AiRecommendationExplanation": {
  "type": "object",
  "x-ticvai-persistence": "none — built from ai.rec_decision and its decision record",
  "description": "Why these items (AIR-193..202), at three depths each gated by permission (AIC-195): business, governance, technical.",
  "required": [
   "decisionId",
   "depth"
  ],
  "properties": {
   "decisionId": {
    "type": "string",
    "format": "uuid"
   },
   "depth": {
    "type": "string",
    "enum": [
     "business",
     "governance",
     "technical"
    ]
   },
   "funnel": {
    "type": "object",
    "additionalProperties": true
   },
   "exclusions": {
    "type": "object",
    "additionalProperties": true
   },
   "items": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "trackingId": {
       "type": "string",
       "format": "uuid"
      },
      "productId": {
       "type": "string",
       "format": "uuid"
      },
      "reasons": {
       "type": "array",
       "items": {
        "type": "string"
       }
      },
      "scoreBreakdown": {
       "type": "object",
       "additionalProperties": true,
       "nullable": true
      }
     }
    }
   },
   "versions": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true,
    "description": "Strategy, model and feature-set versions. `technical` depth only."
   }
  }
 },
 "RecommendationExperiment": {
  "type": "object",
  "x-ticvai-persistence": "promotions.recommendation_experiment",
  "description": "Boards 6.3 and 6.4. **Fixed allocation, explicit conclusion, and a holdout.**",
  "required": [
   "code",
   "variants"
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
   "placement": {
    "type": "string",
    "nullable": true
   },
   "variants": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "name": {
       "type": "string"
      },
      "strategyId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "allocationPercent": {
       "type": "integer"
      }
     }
    }
   },
   "holdoutPercent": {
    "type": "integer",
    "default": 5
   },
   "primaryMetric": {
    "type": "string"
   },
   "minimumSampleSize": {
    "type": "integer",
    "nullable": true
   },
   "startedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "endedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "draft",
     "running",
     "concluded",
     "abandoned"
    ]
   },
   "winningVariant": {
    "type": "string",
    "nullable": true
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "RecommendationPerformance": {
  "type": "object",
  "description": "Board 6.5. **Attributed and incremental reported apart** — the first flatters.",
  "properties": {
   "key": {
    "type": "string"
   },
   "label": {
    "type": "string"
   },
   "impressions": {
    "type": "integer"
   },
   "clicks": {
    "type": "integer"
   },
   "accepted": {
    "type": "integer"
   },
   "acceptanceRate": {
    "type": "number"
   },
   "attributedRevenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "incrementalRevenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "holdoutAcceptanceRate": {
    "type": "number",
    "nullable": true
   },
   "lift": {
    "type": "number",
    "nullable": true
   }
  }
 },
 "RecommendationStrategy": {
  "type": "object",
  "x-ticvai-persistence": "promotions.recommendation_strategy",
  "description": "Upsell board 1. **Objective, placement, ranking and guardrail in one record**, because any one of them alone produces a recommender that is either aimless or dangerous.\n",
  "required": [
   "code",
   "name",
   "objective"
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
   "objective": {
    "type": "string",
    "enum": [
     "attachRevenue",
     "averageOrderValue",
     "upgradeRate",
     "visitFrequency",
     "inventoryBalance",
     "guestSatisfaction"
    ]
   },
   "kinds": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "upsell",
      "upgrade",
      "crossSell",
      "bundle",
      "nextBestOffer",
      "reactivation"
     ]
    }
   },
   "itemKinds": {
    "type": "array",
    "description": "What the strategy may put in a slot (29 September, build pass, group G2, from group G1's handoff; 8.6.30 to 8.6.36, 5.4.21, 22.6.18): `product` (the default and the behaviour before), `offer` (a live promotion marked `recommendable`), `reward` (a marketing-crm loyalty reward the guest can redeem) and `challenge` (a challenge they can join). Mirrors `ai.decideRecommendations` item kinds.",
    "default": [
     "product"
    ],
    "items": {
     "type": "string",
     "enum": [
      "product",
      "offer",
      "reward",
      "challenge"
     ]
    }
   },
   "placements": {
    "type": "array",
    "description": "`homepage` (8.6.10) and `loyalty` (5.4.21, 22.6.18) added 29 September (build pass, group G2), matching the placements `ai.decideRecommendations` fills.",
    "items": {
     "type": "string",
     "enum": [
      "productPage",
      "cart",
      "checkout",
      "postPurchase",
      "preVisitEmail",
      "inVenueApp",
      "kiosk",
      "pos",
      "signage",
      "callCentre",
      "homepage",
      "loyalty"
     ]
    }
   },
   "channels": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "maxRecommendations": {
    "type": "integer",
    "default": 3,
    "description": "**A guardrail before it is a layout choice.** Nine upsells at checkout is not a denser page, it is an abandoned basket.\n"
   },
   "minConfidence": {
    "type": "number",
    "nullable": true
   },
   "rankingWeights": {
    "type": "object",
    "additionalProperties": {
     "type": "number"
    },
    "description": "Propensity, margin, inventory pressure, affinity, recency."
   },
   "requireAvailability": {
    "type": "boolean",
    "default": true
   },
   "excludeInBasket": {
    "type": "boolean",
    "default": true
   },
   "guardrails": {
    "type": "object",
    "properties": {
     "maxDiscountPercent": {
      "type": "number",
      "nullable": true
     },
     "minMarginPercent": {
      "type": "number",
      "nullable": true
     },
     "neverRecommendCategoryIds": {
      "type": "array",
      "items": {
       "type": "string",
       "format": "uuid"
      }
     },
     "requireHumanApproval": {
      "type": "boolean",
      "default": false
     }
    }
   },
   "status": {
    "type": "string",
    "enum": [
     "draft",
     "active",
     "paused",
     "retired"
    ]
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "effectiveTo": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "scopePath": {
    "type": "string"
   }
  }
 }
}
```
