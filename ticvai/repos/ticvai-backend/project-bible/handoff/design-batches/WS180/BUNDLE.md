# WS180 — Upsell,CrossSellEngine board 1

**10 screens · 8 operations · 4 schemas · 2 permissions**

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
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-639` | Recommendation Command Center | listDetail | 2 | 0 | — |
| `ADM-640` | Recommendation Strategy Manager | listDetail | 3 | 0 | — |
| `ADM-641` | Recommendation Objective & KPI Configuration | configEditor | 1 | 0 | — |
| `ADM-642` | Recommendation Type & Product Relationship Manager | listDetail | 2 | 0 | — |
| `ADM-643` | Recommendation Placement & Touchpoint Manager | listDetail | 1 | 0 | — |
| `ADM-644` | Channel & Journey Strategy Manager | listDetail | 1 | 0 | — |
| `ADM-645` | Recommendation Priority, Ranking & Suppression Manager17 | listDetail | 2 | 0 | — |
| `ADM-646` | Recommendation Guardrails & Business Controls | listDetail | 1 | 0 | — |
| `ADM-647` | Recommendation Policy, AI Control & Governance | listDetail | 1 | 0 | — |
| `ADM-648` | Recommendation Strategy Simulator & AI Advisor | configEditor | 1 | 0 | — |

## Thin screens in this batch

**ADM-639, ADM-640, ADM-643, ADM-644, ADM-646, ADM-647 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-639",
  "name": "Recommendation Command Center",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Upsell,CrossSellEngine.pdf",
   "board": "1",
   "number": "1",
   "page": 7
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/recommendation-command-center-adm-639",
   "component": "apps/ticvai-web/src/routes/commercial/RecommendationCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-640",
    "ADM-641",
    "ADM-642",
    "ADM-643",
    "ADM-644",
    "ADM-645",
    "ADM-646",
    "ADM-647",
    "ADM-648"
   ],
   "transitions": [
    {
     "to": "ADM-002",
     "trigger": "Back to Platform Dashboard",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "ADM-640",
     "trigger": "Recommendation Strategy Manager",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "ADM-641",
     "trigger": "Recommendation Objective & KPI Configuration",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "ADM-642",
     "trigger": "Recommendation Type & Product Relationship Manager",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "ADM-643",
     "trigger": "Recommendation Placement & Touchpoint Manager",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "ADM-644",
     "trigger": "Channel & Journey Strategy Manager",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "ADM-645",
     "trigger": "Recommendation Priority, Ranking & Suppression Manager17",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "ADM-646",
     "trigger": "Recommendation Guardrails & Business Controls",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "ADM-647",
     "trigger": "Recommendation Policy, AI Control & Governance",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "ADM-648",
     "trigger": "Recommendation Strategy Simulator & AI Advisor",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display; Show) and no metric row",
  "purpose": "Provide the central operational dashboard for the complete TICVAI Recommendation Engine. This becomes the entry point for Marketing, Commercial, Revenue, CRM and authorized operational users.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 7 §Display"
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
       "label": "Every recommendation",
       "columns": [
        "Active Recommendation Strategies",
        "Active Recommendation Rules",
        "AI-Managed Recommendations",
        "Recommendation Impressions",
        "Recommendation Clicks",
        "Recommendation Acceptance",
        "Recommendation Conversion Rate",
        "Upsell Revenue",
        "Cross-Sell Revenue",
        "Incremental Revenue",
        "Average Basket Uplift",
        "Recommendation Attach Rate",
        "Healthy",
        "Monitor",
        "Underperforming",
        "Conflict",
        "Inventory Issue",
        "No Eligible Product",
        "AI Warning",
        "Suspended"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 7 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected recommendation",
       "bindsTo": null,
       "columns": [
        "Active Recommendation Strategies",
        "Active Recommendation Rules",
        "AI-Managed Recommendations",
        "Recommendation Impressions",
        "Recommendation Clicks",
        "Recommendation Acceptance",
        "Recommendation Conversion Rate",
        "Upsell Revenue",
        "Cross-Sell Revenue",
        "Incremental Revenue",
        "Average Basket Uplift",
        "Recommendation Attach Rate",
        "Healthy",
        "Monitor",
        "Underperforming",
        "Conflict",
        "Inventory Issue",
        "No Eligible Product",
        "AI Warning",
        "Suspended"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Break down by”.",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 7 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The recommendation list.",
   "error": "Could not load. Names which read failed and leaves the recommendation untouched.",
   "emptyFirstRun": "No recommendation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the recommendation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listRecommendationStrategies",
    "contract": "promotions",
    "purpose": "Strategies in force",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "getRecommendationPerformance",
    "contract": "promotions",
    "purpose": "How they are doing",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Active Recommendation Strategies",
    "Active Recommendation Rules",
    "AI-Managed Recommendations",
    "Recommendation Impressions",
    "Recommendation Clicks",
    "Recommendation Acceptance"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-639",
   "workshopBoard": "wireframes/WS178 Upsell,CrossSellEngine Board 1.dc.html#adm-639"
  },
  "apisNote": "Regenerated 9 September 2026 from Upsell,CrossSellEngine.pdf page 7. 0 of 20 labels bound to a contract property; 20 of 43 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-640",
  "name": "Recommendation Strategy Manager",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Upsell,CrossSellEngine.pdf",
   "board": "1",
   "number": "2",
   "page": 9
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/recommendation-strategy-manager-adm-640",
   "component": "apps/ticvai-web/src/routes/commercial/RecommendationStrategyManager.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-639"
   ],
   "exitTo": [
    "ADM-639"
   ],
   "transitions": [
    {
     "to": "ADM-639",
     "trigger": "Back to Recommendation Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Define the commercial strategy TICVAI should use when generating recommendations. Instead of hard-coding recommendation behavior into B2C or POS, administrators configure reusable strategies centrally. Increase cross-attraction sales.",
  "gaps": [
   {
    "operation": null,
    "why": "**Recommendation Strategy Manager declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 9"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 9"
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
       "impliedBy": "listRecommendationStrategies",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createRecommendationStrategy",
       "label": "Create",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createRecommendationStrategy"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The recommendation strategy list.",
   "error": "Could not load. Names which read failed and leaves the recommendation strategy untouched.",
   "emptyFirstRun": "No recommendation strategy yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the recommendation strategy are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listRecommendationStrategies",
    "contract": "promotions",
    "purpose": "The strategies",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "createRecommendationStrategy",
    "contract": "promotions",
    "purpose": "Define one",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listRecommendationStrategies"
    ]
   },
   {
    "operationId": "updateRecommendationStrategy",
    "contract": "promotions",
    "purpose": "Change one",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listRecommendationStrategies"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-640",
   "workshopBoard": "wireframes/WS178 Upsell,CrossSellEngine Board 1.dc.html#adm-640"
  },
  "apisNote": "Regenerated 9 September 2026 from Upsell,CrossSellEngine.pdf page 9. 0 of 0 labels bound to a contract property; 0 of 32 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "strategyId",
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
  "id": "ADM-641",
  "name": "Recommendation Objective & KPI Configuration",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Upsell,CrossSellEngine.pdf",
   "board": "1",
   "number": "3",
   "page": 11
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/recommendation-objective-kpi-configuration-adm-641",
   "component": "apps/ticvai-web/src/routes/commercial/RecommendationObjectiveKpiConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-639"
   ],
   "exitTo": [
    "ADM-639"
   ],
   "transitions": [
    {
     "to": "ADM-639",
     "trigger": "Back to Recommendation Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Administrators may configure) and no display directory — it is settings, not a population",
  "purpose": "Define exactly what the recommendation engine should optimize. This is important because the \"best\" recommendation depends on the business objective. Allow weighted objectives.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 5 actions on this screen and the screen declares 0 operations.** Unserved: Revenue, Incremental revenue, Membership conversion, Capacity utilization, Inventory movement. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 11 §Support"
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
       "label": "Minimum margin",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 11 §Administrators may configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum discount",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 11 §Administrators may configure"
      },
      {
       "kind": "selectField",
       "label": "Minimum relevance score",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 11 §Administrators may configure"
      },
      {
       "kind": "selectField",
       "label": "Minimum inventory",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 11 §Administrators may configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum recommendation frequency",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 11 §Administrators may configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Revenue",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 11 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Incremental revenue",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 11 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Membership conversion",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 11 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Capacity utilization",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 11 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Inventory movement",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 11 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The recommendation objective kpi configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the recommendation objective kpi untouched.",
   "emptyFirstRun": "No recommendation objective kpi configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "updateRecommendationStrategy",
    "contract": "promotions",
    "purpose": "Objective and KPI",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listRecommendationStrategies"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-641",
   "workshopBoard": "wireframes/WS178 Upsell,CrossSellEngine Board 1.dc.html#adm-641"
  },
  "apisNote": "Regenerated 9 September 2026 from Upsell,CrossSellEngine.pdf page 11. 0 of 0 labels bound to a contract property; 10 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "strategyId",
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
  "id": "ADM-642",
  "name": "Recommendation Type & Product Relationship Manager",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Upsell,CrossSellEngine.pdf",
   "board": "1",
   "number": "4",
   "page": 13
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/recommendation-type-product-relationship-manager-adm-642",
   "component": "apps/ticvai-web/src/routes/commercial/RecommendationTypeProductRelationshipManager.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-639"
   ],
   "exitTo": [
    "ADM-639"
   ],
   "transitions": [
    {
     "to": "ADM-639",
     "trigger": "Back to Recommendation Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Define the commercial relationships from which recommendations can be generated.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 12 actions on this screen and the screen declares 0 operations.** Unserved: Ticket → Ticket, Ticket → Bundle, Ticket → F&B, Ticket → Retail, Ticket → Parking, Ticket → Locker, Ticket → Photo, Ticket → Rental …. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 13 §Support relationships between"
   },
   {
    "operation": null,
    "why": "**Recommendation Type & Product Relationship Manager declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 13"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 13"
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
       "label": "Ticket → Ticket",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 13 §Support relationships between"
      },
      {
       "kind": "secondaryButton",
       "label": "Ticket → Bundle",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 13 §Support relationships between"
      },
      {
       "kind": "secondaryButton",
       "label": "Ticket → F&B",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 13 §Support relationships between"
      },
      {
       "kind": "secondaryButton",
       "label": "Ticket → Retail",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 13 §Support relationships between"
      },
      {
       "kind": "secondaryButton",
       "label": "Ticket → Parking",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 13 §Support relationships between"
      },
      {
       "kind": "secondaryButton",
       "label": "Ticket → Locker",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 13 §Support relationships between"
      },
      {
       "kind": "secondaryButton",
       "label": "Ticket → Photo",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 13 §Support relationships between"
      },
      {
       "kind": "secondaryButton",
       "label": "Ticket → Rental",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 13 §Support relationships between"
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
   "loading": "The recommendation type product list.",
   "error": "Could not load. Names which read failed and leaves the recommendation type product untouched.",
   "emptyFirstRun": "No recommendation type product yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the recommendation type product are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listProductRelationships",
    "contract": "promotions",
    "purpose": "Ladders and cross-sells",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "setProductRelationships",
    "contract": "promotions",
    "purpose": "Declare them",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listProductRelationships"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-642",
   "workshopBoard": "wireframes/WS178 Upsell,CrossSellEngine Board 1.dc.html#adm-642"
  },
  "apisNote": "Regenerated 9 September 2026 from Upsell,CrossSellEngine.pdf page 13. 0 of 0 labels bound to a contract property; 12 of 31 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-643",
  "name": "Recommendation Placement & Touchpoint Manager",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Upsell,CrossSellEngine.pdf",
   "board": "1",
   "number": "5",
   "page": 15
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/recommendation-placement-touchpoint-manager-adm-643",
   "component": "apps/ticvai-web/src/routes/commercial/RecommendationPlacementTouchpointManager.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-639"
   ],
   "exitTo": [
    "ADM-639"
   ],
   "transitions": [
    {
     "to": "ADM-639",
     "trigger": "Back to Recommendation Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Define where in the customer journey recommendations are permitted to appear. This is a major requirement for the engine.",
  "gaps": [
   {
    "operation": null,
    "why": "**Recommendation Placement & Touchpoint Manager declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 15"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 15"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "updateRecommendationStrategy",
       "label": "Save",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "updateRecommendationStrategy"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The recommendation placement touchpoint list.",
   "error": "Could not load. Names which read failed and leaves the recommendation placement touchpoint untouched.",
   "emptyFirstRun": "No recommendation placement touchpoint yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the recommendation placement touchpoint are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "updateRecommendationStrategy",
    "contract": "promotions",
    "purpose": "Placements and touchpoints",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listRecommendationStrategies"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-643",
   "workshopBoard": "wireframes/WS178 Upsell,CrossSellEngine Board 1.dc.html#adm-643"
  },
  "apisNote": "Regenerated 9 September 2026 from Upsell,CrossSellEngine.pdf page 15. 0 of 0 labels bound to a contract property; 0 of 38 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "strategyId",
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
  "id": "ADM-644",
  "name": "Channel & Journey Strategy Manager",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Upsell,CrossSellEngine.pdf",
   "board": "1",
   "number": "6",
   "page": 17
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/channel-journey-strategy-manager-adm-644",
   "component": "apps/ticvai-web/src/routes/commercial/ChannelJourneyStrategyManager.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-639"
   ],
   "exitTo": [
    "ADM-639"
   ],
   "transitions": [
    {
     "to": "ADM-639",
     "trigger": "Back to Recommendation Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Control recommendation behavior across TICVAI's omnichannel environment.",
  "gaps": [
   {
    "operation": null,
    "why": "**Channel & Journey Strategy Manager declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 17"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 17"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "updateRecommendationStrategy",
       "label": "Save",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "updateRecommendationStrategy"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The channel journey strategy list.",
   "error": "Could not load. Names which read failed and leaves the channel journey strategy untouched.",
   "emptyFirstRun": "No channel journey strategy yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the channel journey strategy are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "updateRecommendationStrategy",
    "contract": "promotions",
    "purpose": "Channels and journey",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listRecommendationStrategies"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-644",
   "workshopBoard": "wireframes/WS178 Upsell,CrossSellEngine Board 1.dc.html#adm-644"
  },
  "apisNote": "Regenerated 9 September 2026 from Upsell,CrossSellEngine.pdf page 17. 0 of 0 labels bound to a contract property; 0 of 26 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "strategyId",
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
  "id": "ADM-645",
  "name": "Recommendation Priority, Ranking & Suppression Manager17",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Upsell,CrossSellEngine.pdf",
   "board": "1",
   "number": "7",
   "page": 19
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/recommendation-priority-ranking-suppression-manager17-adm-645",
   "component": "apps/ticvai-web/src/routes/commercial/RecommendationPriorityRankingSuppressionManager1.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-639"
   ],
   "exitTo": [
    "ADM-639"
   ],
   "transitions": [
    {
     "to": "ADM-639",
     "trigger": "Back to Recommendation Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Define how multiple eligible recommendations are ranked before being presented. This is different from Promotion Board 8.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 7 actions on this screen and the screen declares 0 operations.** Unserved: Revenue potential, Product affinity, Customer propensity, Inventory, Capacity, Commercial priority, Campaign priority. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 19 §Support"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 19"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 19"
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
       "label": "Revenue potential",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 19 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Product affinity",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 19 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Customer propensity",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 19 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Inventory",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 19 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Capacity",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 19 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Commercial priority",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 19 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Campaign priority",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 19 §Support"
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
   "loading": "The recommendation priority ranking list.",
   "error": "Could not load. Names which read failed and leaves the recommendation priority ranking untouched.",
   "emptyFirstRun": "No recommendation priority ranking yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the recommendation priority ranking are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setRecommendationSuppression",
    "contract": "promotions",
    "purpose": "Caps, fatigue and exclusions",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listRecommendationStrategies"
    ]
   },
   {
    "operationId": "updateRecommendationStrategy",
    "contract": "promotions",
    "purpose": "Priority and ranking",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listRecommendationStrategies"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-645",
   "workshopBoard": "wireframes/WS178 Upsell,CrossSellEngine Board 1.dc.html#adm-645"
  },
  "apisNote": "Regenerated 9 September 2026 from Upsell,CrossSellEngine.pdf page 19. 0 of 0 labels bound to a contract property; 7 of 26 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "strategyId",
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
  "id": "ADM-646",
  "name": "Recommendation Guardrails & Business Controls",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Upsell,CrossSellEngine.pdf",
   "board": "1",
   "number": "8",
   "page": 20
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/recommendation-guardrails-business-controls-adm-646",
   "component": "apps/ticvai-web/src/routes/commercial/RecommendationGuardrailsBusinessControls.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-639"
   ],
   "exitTo": [
    "ADM-639"
   ],
   "transitions": [
    {
     "to": "ADM-639",
     "trigger": "Back to Recommendation Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Protect the business and customer experience from inappropriate AI or rule- generated recommendations.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 20"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 20"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "updateRecommendationStrategy",
       "label": "Save",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "updateRecommendationStrategy"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The recommendation guardrails business list.",
   "error": "Could not load. Names which read failed and leaves the recommendation guardrails business untouched.",
   "emptyFirstRun": "No recommendation guardrails business yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the recommendation guardrails business are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "updateRecommendationStrategy",
    "contract": "promotions",
    "purpose": "Commercial guardrails",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listRecommendationStrategies"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-646",
   "workshopBoard": "wireframes/WS178 Upsell,CrossSellEngine Board 1.dc.html#adm-646"
  },
  "apisNote": "Regenerated 9 September 2026 from Upsell,CrossSellEngine.pdf page 20. 0 of 0 labels bound to a contract property; 0 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "strategyId",
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
  "id": "ADM-647",
  "name": "Recommendation Policy, AI Control & Governance",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Upsell,CrossSellEngine.pdf",
   "board": "1",
   "number": "9",
   "page": 22
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/recommendation-policy-ai-control-governance-adm-647",
   "component": "apps/ticvai-web/src/routes/commercial/RecommendationPolicyAiControlGovernance.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-639"
   ],
   "exitTo": [
    "ADM-639"
   ],
   "transitions": [
    {
     "to": "ADM-639",
     "trigger": "Back to Recommendation Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Define how much authority the TICVAI AI layer has over recommendation decisions.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 22"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 22"
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
       "impliedBy": "listRecommendationStrategies",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The recommendation policy governance list.",
   "error": "Could not load. Names which read failed and leaves the recommendation policy governance untouched.",
   "emptyFirstRun": "No recommendation policy governance yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the recommendation policy governance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listRecommendationStrategies",
    "contract": "promotions",
    "purpose": "Policy and governance",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-647",
   "workshopBoard": "wireframes/WS178 Upsell,CrossSellEngine Board 1.dc.html#adm-647"
  },
  "apisNote": "Regenerated 9 September 2026 from Upsell,CrossSellEngine.pdf page 22. 0 of 0 labels bound to a contract property; 0 of 31 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-648",
  "name": "Recommendation Strategy Simulator & AI Advisor",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Upsell,CrossSellEngine.pdf",
   "board": "1",
   "number": "10",
   "page": 24
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/recommendation-strategy-simulator-ai-advisor-adm-648",
   "component": "apps/ticvai-web/src/routes/commercial/RecommendationStrategySimulatorAiAdvisor.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-639"
   ],
   "exitTo": [
    "ADM-639"
   ],
   "transitions": [
    {
     "to": "ADM-639",
     "trigger": "Back to Recommendation Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Select) and no display directory — it is settings, not a population",
  "purpose": "Allow administrators to test recommendation strategies before activating them. This should become the final validation screen for Board 1. ↓ Board 2 shall provide TICVAI with the specialized Upsell & Upgrade Recommendation Engine responsible for identifying when a customer can be moved from their current product, ticket, experience, membership, bundle, or service to a higher-value or more valuable alternative. Board 1 established the overall recommendation strategy, placements, ranking, guardrails, and AI governance.",
  "purposeNote": "Board 1 shall be complete when: 1. Administrators have a centralized Recommendation Command Center. 2. Recommendation strategies can be created and managed. 3. Strategies can have different commercial objectives. 4. Multi-objective optimization can be configured. 5. Recommendation relationships can be defined centrally. 6. Upsell, upgrade, cross-sell, add-on, bundle and membership relationships are supported. 7. Relationships can be manual, rule-generated or AI-discovered. 8. Recommendation placements can be configured. 9. Journey-stage-specific placements are supported. 10.Channel-specific be",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Customer profile",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 24 §Select"
      },
      {
       "kind": "selectField",
       "label": "Customer segment",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 24 §Select"
      },
      {
       "kind": "selectField",
       "label": "Basket",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 24 §Select"
      },
      {
       "kind": "selectField",
       "label": "Product",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 24 §Select"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 24 §Select"
      },
      {
       "kind": "selectField",
       "label": "Channel",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 24 §Select"
      },
      {
       "kind": "selectField",
       "label": "Journey stage",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 24 §Select"
      },
      {
       "kind": "selectField",
       "label": "Date/time",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 24 §Select"
      },
      {
       "kind": "selectField",
       "label": "Membership",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 24 §Select"
      },
      {
       "kind": "selectField",
       "label": "Loyalty",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 24 §Select"
      },
      {
       "kind": "selectField",
       "label": "Inventory conditions",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 24 §Select"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The recommendation strategy simulator configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the recommendation strategy simulator untouched.",
   "emptyFirstRun": "No recommendation strategy simulator configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "simulateRecommendationStrategy",
    "contract": "promotions",
    "purpose": "Replay against history",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-648",
   "workshopBoard": "wireframes/WS178 Upsell,CrossSellEngine Board 1.dc.html#adm-648"
  },
  "apisNote": "Regenerated 9 September 2026 from Upsell,CrossSellEngine.pdf page 24. 0 of 0 labels bound to a contract property; 11 of 224 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "createRecommendationStrategy": {
  "method": "POST",
  "path": "/recommendation-strategies",
  "contract": "promotions",
  "summary": "Define objective, placements, ranking and guardrails",
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
 "listProductRelationships": {
  "method": "GET",
  "path": "/product-relationships",
  "contract": "promotions",
  "summary": "Upgrade ladders, cross-sells, affinities and substitutes",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "productId",
    "in": "query",
    "required": null
   },
   {
    "name": "kind",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "ProductRelationship"
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
 "setProductRelationships": {
  "method": "PUT",
  "path": "/product-relationships",
  "contract": "promotions",
  "summary": "Declare what upgrades to, pairs with or replaces what",
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
  "responds": "ProductRelationship"
 },
 "setRecommendationSuppression": {
  "method": "PUT",
  "path": "/recommendation-suppressions",
  "contract": "promotions",
  "summary": "Fatigue limits, frequency caps and hard exclusions",
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
  "requestBody": "RecommendationSuppression",
  "responds": "RecommendationSuppression"
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
 "ProductRelationship": {
  "type": "object",
  "x-ticvai-persistence": "promotions.product_relationship",
  "description": "Upsell boards 2.2 and 3.2. **Declared, and distinguishable from measured affinity.**",
  "required": [
   "fromProductId",
   "toProductId",
   "kind"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "fromProductId": {
    "type": "string",
    "format": "uuid"
   },
   "toProductId": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "type": "string",
    "enum": [
     "upgradesTo",
     "downgradesTo",
     "crossSell",
     "accessory",
     "substitute",
     "requires",
     "incompatibleWith"
    ]
   },
   "ladderPosition": {
    "type": "integer",
    "nullable": true,
    "description": "**For upgrade ladders only.** Standard → Premium → VIP is ordered, and an unordered set cannot answer *what is the next step up*.\n"
   },
   "source": {
    "type": "string",
    "enum": [
     "declared",
     "measured",
     "aiProposed"
    ],
    "default": "declared"
   },
   "strength": {
    "type": "number",
    "nullable": true
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
 },
 "RecommendationSuppression": {
  "type": "object",
  "x-ticvai-persistence": "promotions.recommendation_suppression",
  "description": "Boards 1.7 and 5.7. **Fatigue is why a good recommender stops working.**",
  "properties": {
   "scopePath": {
    "type": "string"
   },
   "maxImpressionsPerProductPerDay": {
    "type": "integer",
    "nullable": true
   },
   "maxImpressionsPerGuestPerSession": {
    "type": "integer",
    "nullable": true
   },
   "cooldownAfterDismissDays": {
    "type": "integer",
    "nullable": true
   },
   "cooldownAfterAcceptDays": {
    "type": "integer",
    "nullable": true
   },
   "hardExclusions": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "segmentId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "categoryId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "productId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "reason": {
       "type": "string"
      }
     }
    }
   }
  }
 }
}
```
