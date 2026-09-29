# WS182 — Upsell,CrossSellEngine board 3

**10 screens · 6 operations · 5 schemas · 3 permissions**

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
  `PRICE_VIEW, PRODUCT_CONFIGURE, PRODUCT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-659` | Cross-Sell Command Center | commandCentre | 2 | 0 | — |
| `ADM-660` | Cross-Sell Relationship Builder | listDetail | 1 | 0 | — |
| `ADM-661` | Product Affinity Matrix & Relationship Map | listDetail | 1 | 0 | — |
| `ADM-662` | Frequently Bought Together & Basket Pattern Engine | listDetail | 1 | 0 | — |
| `ADM-663` | Cross-Category Recommendation Manager | listDetail | 1 | 0 | — |
| `ADM-664` | Multi-Attraction, Destination & Partner Cross-Sell | listDetail | 1 | 0 | — |
| `ADM-665` | Basket-Aware Cross-Sell & Duplicate Prevention | listDetail | 1 | 0 | — |
| `ADM-666` | Availability, Inventory & Capacity-Aware Cross-Sell | configEditor | 1 | 0 | — |
| `ADM-667` | AI Cross-Sell Discovery, Scoring & Ranking Engine | listDetail | 1 | 0 | — |
| `ADM-668` | Cross-Sell Simulator & AI Opportunity Advisor | listDetail | 1 | 0 | — |

## Thin screens in this batch

**ADM-661, ADM-662, ADM-663, ADM-664, ADM-665, ADM-667, ADM-668 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-659",
  "name": "Cross-Sell Command Center",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Upsell,CrossSellEngine.pdf",
   "board": "3",
   "number": "1",
   "page": 64
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/cross-sell-command-center-adm-659",
   "component": "apps/ticvai-web/src/routes/commercial/CrossSellCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-660",
    "ADM-661",
    "ADM-662",
    "ADM-663",
    "ADM-664",
    "ADM-665",
    "ADM-666",
    "ADM-667",
    "ADM-668"
   ],
   "transitions": [
    {
     "to": "ADM-002",
     "trigger": "Back to Platform Dashboard",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "ADM-660",
     "trigger": "Cross-Sell Relationship Builder",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "ADM-661",
     "trigger": "Product Affinity Matrix & Relationship Map",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "ADM-662",
     "trigger": "Frequently Bought Together & Basket Pattern Engine",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "ADM-663",
     "trigger": "Cross-Category Recommendation Manager",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "ADM-664",
     "trigger": "Multi-Attraction, Destination & Partner Cross-Sell",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "ADM-665",
     "trigger": "Basket-Aware Cross-Sell & Duplicate Prevention",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "ADM-666",
     "trigger": "Availability, Inventory & Capacity-Aware Cross-Sell",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "ADM-667",
     "trigger": "AI Cross-Sell Discovery, Scoring & Ranking Engine",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "ADM-668",
     "trigger": "Cross-Sell Simulator & AI Opportunity Advisor",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§KPI Cards) and a per-row directory (§Show) — counts over a population, then the population",
  "purpose": "Provide centralized visibility into cross-sell relationships, recommendation performance, attach rates and commercial opportunities.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 64 §Show"
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
       "label": "Active Cross-Sell Relationships",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 64 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "AI-Discovered Relationships",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 64 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Cross-Sell Recommendations",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 64 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Recommendations Accepted",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 64 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Cross-Sell Conversion",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 64 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Cross-Sell Revenue",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 64 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Estimated Incremental Revenue",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 64 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Attach Rate",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 64 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Items per Transaction",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 64 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "AOV Uplift",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 64 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Cross-Category Revenue",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 64 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Suppressed Recommendations",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 64 §KPI Cards"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every cross-sell",
       "columns": [
        "Recommendations → Acceptances → Purchases → Revenue"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 64 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected cross-sell",
       "bindsTo": null,
       "columns": [
        "Recommendations → Acceptances → Purchases → Revenue"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Break down by”, “Relationships classified”.",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 64 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The cross-sell list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the cross-sell untouched.",
   "emptyFirstRun": "No cross-sell yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the cross-sell are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listUpsellCrossSell",
    "contract": "promotions",
    "purpose": "Upsell, Cross-Sell & Attach-Rate Analytics",
    "trigger": "onLoad"
   },
   {
    "operationId": "getRecommendationPerformance",
    "contract": "promotions",
    "purpose": "Cross-sell performance",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-659",
   "workshopBoard": "wireframes/WS180 Upsell,CrossSellEngine Board 3.dc.html#adm-659"
  },
  "apisNote": "Regenerated 9 September 2026 from Upsell,CrossSellEngine.pdf page 64. 0 of 1 labels bound to a contract property; 13 of 37 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-660",
  "name": "Cross-Sell Relationship Builder",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Upsell,CrossSellEngine.pdf",
   "board": "3",
   "number": "2",
   "page": 66
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/cross-sell-relationship-builder-adm-660",
   "component": "apps/ticvai-web/src/routes/commercial/CrossSellRelationshipBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-659"
   ],
   "exitTo": [
    "ADM-659"
   ],
   "transitions": [
    {
     "to": "ADM-659",
     "trigger": "Back to Cross-Sell Command Center",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Identify) and no metric row",
  "purpose": "Allow administrators to manually define governed complementary-product relationships.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 4 actions on this screen and the screen declares 0 operations.** Unserved: Experience Extension, Destination Extension, Service Add-On, Partner Product. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 66 §Support"
   },
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 66 §Identify"
   },
   {
    "operation": null,
    "why": "**Cross-Sell Relationship Builder declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
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
       "label": "Every cross-sell relationship",
       "columns": [
        "Manual",
        "Historical Data",
        "AI Discovered",
        "Campaign",
        "Partner",
        "Imported"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 66 §Identify"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected cross-sell relationship",
       "bindsTo": null,
       "columns": [
        "Manual",
        "Historical Data",
        "AI Discovered",
        "Campaign",
        "Partner",
        "Imported"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Water Park Admission”, “Cross-Sell”, “For every relationship”, “One-Way”, “Two-Way”.",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 66 §Identify"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Experience Extension",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 66 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Destination Extension",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 66 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Service Add-On",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 66 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Partner Product",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 66 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The cross-sell relationship list.",
   "error": "Could not load. Names which read failed and leaves the cross-sell relationship untouched.",
   "emptyFirstRun": "No cross-sell relationship yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the cross-sell relationship are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setProductRelationships",
    "contract": "promotions",
    "purpose": "Build the relationships",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listProductRelationships"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "Manual",
    "Historical Data",
    "AI Discovered",
    "Campaign",
    "Partner",
    "Imported"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-660",
   "workshopBoard": "wireframes/WS180 Upsell,CrossSellEngine Board 3.dc.html#adm-660"
  },
  "apisNote": "Regenerated 9 September 2026 from Upsell,CrossSellEngine.pdf page 66. 0 of 6 labels bound to a contract property; 10 of 34 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-661",
  "name": "Product Affinity Matrix & Relationship Map",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Upsell,CrossSellEngine.pdf",
   "board": "3",
   "number": "3",
   "page": 68
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/product-affinity-matrix-relationship-map-adm-661",
   "component": "apps/ticvai-web/src/routes/commercial/ProductAffinityMatrixRelationshipMap.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-659"
   ],
   "exitTo": [
    "ADM-659"
   ],
   "transitions": [
    {
     "to": "ADM-659",
     "trigger": "Back to Cross-Sell Command Center",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide a visual representation of how strongly products and categories relate to one another.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 68"
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
       "label": "Search product affinity relationship",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 68 §Filters"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Venue",
        "Product",
        "Category",
        "Segment",
        "Channel",
        "Season",
        "Date range"
       ],
       "notes": "The pack filters this screen by venue, product, category, segment, channel, season and 1 more — which are present is a decision the pack already made.",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 68 §Filters"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The product affinity relationship list.",
   "error": "Could not load. Names which read failed and leaves the product affinity relationship untouched.",
   "emptyFirstRun": "No product affinity relationship yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the product affinity relationship are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getProductAffinity",
    "contract": "promotions",
    "purpose": "The affinity matrix, measured",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-661",
   "workshopBoard": "wireframes/WS180 Upsell,CrossSellEngine Board 3.dc.html#adm-661"
  },
  "apisNote": "Regenerated 9 September 2026 from Upsell,CrossSellEngine.pdf page 68. 0 of 7 labels bound to a contract property; 7 of 27 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-662",
  "name": "Frequently Bought Together & Basket Pattern Engine",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Upsell,CrossSellEngine.pdf",
   "board": "3",
   "number": "4",
   "page": 70
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/frequently-bought-together-basket-pattern-engine-adm-662",
   "component": "apps/ticvai-web/src/routes/commercial/FrequentlyBoughtTogetherBasketPatternEngine.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-659"
   ],
   "exitTo": [
    "ADM-659"
   ],
   "transitions": [
    {
     "to": "ADM-659",
     "trigger": "Back to Cross-Sell Command Center",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Analyze) and no metric row",
  "purpose": "Analyze transaction baskets to discover products commonly purchased together.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 70 §Analyze"
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
       "label": "Every frequently bought together",
       "columns": [
        "Product pairs",
        "Product triplets",
        "Category relationships",
        "Sequential purchases",
        "Same-visit purchases",
        "Pre-visit purchases",
        "Post-purchase additions"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 70 §Analyze"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected frequently bought together",
       "bindsTo": null,
       "columns": [
        "Product pairs",
        "Product triplets",
        "Category relationships",
        "Sequential purchases",
        "Same-visit purchases",
        "Pre-visit purchases",
        "Post-purchase additions"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Water Park Admission”, “Purchase Rate”, “Photo”, “Package”, “Suggested new relationship”.",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 70 §Analyze"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The frequently bought together list.",
   "error": "Could not load. Names which read failed and leaves the frequently bought together untouched.",
   "emptyFirstRun": "No frequently bought together yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the frequently bought together are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getProductAffinity",
    "contract": "promotions",
    "purpose": "Frequently bought together, with lift",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Product pairs",
    "Product triplets",
    "Category relationships",
    "Sequential purchases",
    "Same-visit purchases",
    "Pre-visit purchases"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-662",
   "workshopBoard": "wireframes/WS180 Upsell,CrossSellEngine Board 3.dc.html#adm-662"
  },
  "apisNote": "Regenerated 9 September 2026 from Upsell,CrossSellEngine.pdf page 70. 0 of 7 labels bound to a contract property; 11 of 23 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-663",
  "name": "Cross-Category Recommendation Manager",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Upsell,CrossSellEngine.pdf",
   "board": "3",
   "number": "5",
   "page": 71
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/cross-category-recommendation-manager-adm-663",
   "component": "apps/ticvai-web/src/routes/commercial/CrossCategoryRecommendationManager.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-659"
   ],
   "exitTo": [
    "ADM-659"
   ],
   "transitions": [
    {
     "to": "ADM-659",
     "trigger": "Back to Cross-Sell Command Center",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Manage recommendations across TICVAI's different commercial modules. This is especially important because TICVAI is not only a ticketing platform.",
  "gaps": [
   {
    "operation": null,
    "why": "**Cross-Category Recommendation Manager declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 71"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 71"
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
       "impliedBy": "setProductRelationships",
       "label": "Save product relationships",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setProductRelationships"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The cross-category recommendation list.",
   "error": "Could not load. Names which read failed and leaves the cross-category recommendation untouched.",
   "emptyFirstRun": "No cross-category recommendation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the cross-category recommendation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setProductRelationships",
    "contract": "promotions",
    "purpose": "Across categories",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listProductRelationships"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-663",
   "workshopBoard": "wireframes/WS180 Upsell,CrossSellEngine Board 3.dc.html#adm-663"
  },
  "apisNote": "Regenerated 9 September 2026 from Upsell,CrossSellEngine.pdf page 71. 0 of 0 labels bound to a contract property; 0 of 30 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-664",
  "name": "Multi-Attraction, Destination & Partner Cross-Sell",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Upsell,CrossSellEngine.pdf",
   "board": "3",
   "number": "6",
   "page": 73
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/multi-attraction-destination-partner-cross-sell-adm-664",
   "component": "apps/ticvai-web/src/routes/commercial/MultiAttractionDestinationPartnerCrossSell.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-659"
   ],
   "exitTo": [
    "ADM-659"
   ],
   "transitions": [
    {
     "to": "ADM-659",
     "trigger": "Back to Cross-Sell Command Center",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Support cross-selling beyond the original venue or attraction. This addresses the matrix requirements around multi-destination and external product combinations.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 73"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 73"
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
       "impliedBy": "setProductRelationships",
       "label": "Save product relationships",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setProductRelationships"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The multi-attraction destination partner list.",
   "error": "Could not load. Names which read failed and leaves the multi-attraction destination partner untouched.",
   "emptyFirstRun": "No multi-attraction destination partner yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the multi-attraction destination partner are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setProductRelationships",
    "contract": "promotions",
    "purpose": "Across attractions and partners",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listProductRelationships"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-664",
   "workshopBoard": "wireframes/WS180 Upsell,CrossSellEngine Board 3.dc.html#adm-664"
  },
  "apisNote": "Regenerated 9 September 2026 from Upsell,CrossSellEngine.pdf page 73. 0 of 0 labels bound to a contract property; 0 of 23 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-665",
  "name": "Basket-Aware Cross-Sell & Duplicate Prevention",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Upsell,CrossSellEngine.pdf",
   "board": "3",
   "number": "7",
   "page": 74
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/basket-aware-cross-sell-duplicate-prevention-adm-665",
   "component": "apps/ticvai-web/src/routes/commercial/BasketAwareCrossSellDuplicatePrevention.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-659"
   ],
   "exitTo": [
    "ADM-659"
   ],
   "transitions": [
    {
     "to": "ADM-659",
     "trigger": "Back to Cross-Sell Command Center",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Make cross-selling aware of the customer's complete current basket. This is critical because basic recommendation engines often recommend something the customer already owns.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 74"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 74"
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
   "loading": "The basket-aware cross-sell duplicate list.",
   "error": "Could not load. Names which read failed and leaves the basket-aware cross-sell duplicate untouched.",
   "emptyFirstRun": "No basket-aware cross-sell duplicate yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the basket-aware cross-sell duplicate are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "updateRecommendationStrategy",
    "contract": "promotions",
    "purpose": "Exclude what is in the basket",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listRecommendationStrategies"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-665",
   "workshopBoard": "wireframes/WS180 Upsell,CrossSellEngine Board 3.dc.html#adm-665"
  },
  "apisNote": "Regenerated 9 September 2026 from Upsell,CrossSellEngine.pdf page 74. 0 of 0 labels bound to a contract property; 0 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-666",
  "name": "Availability, Inventory & Capacity-Aware Cross-Sell",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Upsell,CrossSellEngine.pdf",
   "board": "3",
   "number": "8",
   "page": 76
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/availability-inventory-capacity-aware-cross-sell-adm-666",
   "component": "apps/ticvai-web/src/routes/commercial/AvailabilityInventoryCapacityAwareCrossSell.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-659"
   ],
   "exitTo": [
    "ADM-659"
   ],
   "transitions": [
    {
     "to": "ADM-659",
     "trigger": "Back to Cross-Sell Command Center",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Ensure recommendations reflect actual operational availability.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Continue recommending",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 76 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Reduce ranking",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 76 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Suppress",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 76 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Recommend substitute",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 76 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The availability inventory capacity-aware configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the availability inventory capacity-aware untouched.",
   "emptyFirstRun": "No availability inventory capacity-aware configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "updateRecommendationStrategy",
    "contract": "promotions",
    "purpose": "Require availability",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listRecommendationStrategies"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-666",
   "workshopBoard": "wireframes/WS180 Upsell,CrossSellEngine Board 3.dc.html#adm-666"
  },
  "apisNote": "Regenerated 9 September 2026 from Upsell,CrossSellEngine.pdf page 76. 0 of 0 labels bound to a contract property; 4 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-667",
  "name": "AI Cross-Sell Discovery, Scoring & Ranking Engine",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Upsell,CrossSellEngine.pdf",
   "board": "3",
   "number": "9",
   "page": 77
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/ai-cross-sell-discovery-scoring-ranking-engine-adm-667",
   "component": "apps/ticvai-web/src/routes/commercial/AiCrossSellDiscoveryScoringRankingEngine.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-659"
   ],
   "exitTo": [
    "ADM-659"
   ],
   "transitions": [
    {
     "to": "ADM-659",
     "trigger": "Back to Cross-Sell Command Center",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Use AI to discover and rank the strongest complementary products for the current customer/context.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 77"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 77"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": []
    }
   ]
  },
  "states": {
   "loading": "The cross-sell discovery scoring list.",
   "error": "Could not load. Names which read failed and leaves the cross-sell discovery scoring untouched.",
   "emptyFirstRun": "No cross-sell discovery scoring yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the cross-sell discovery scoring are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getProductAffinity",
    "contract": "promotions",
    "purpose": "Discovery and scoring",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-667",
   "workshopBoard": "wireframes/WS180 Upsell,CrossSellEngine Board 3.dc.html#adm-667"
  },
  "apisNote": "Regenerated 9 September 2026 from Upsell,CrossSellEngine.pdf page 77. 0 of 0 labels bound to a contract property; 0 of 32 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-668",
  "name": "Cross-Sell Simulator & AI Opportunity Advisor",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Upsell,CrossSellEngine.pdf",
   "board": "3",
   "number": "10",
   "page": 79
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/cross-sell-simulator-ai-opportunity-advisor-adm-668",
   "component": "apps/ticvai-web/src/routes/commercial/CrossSellSimulatorAiOpportunityAdvisor.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-659"
   ],
   "exitTo": [
    "ADM-659"
   ],
   "transitions": [
    {
     "to": "ADM-659",
     "trigger": "Back to Cross-Sell Command Center",
     "provenance": "structural — pack board 3 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Track) and no metric row",
  "purpose": "Allow administrators to test cross-sell strategies and AI recommendations before activation. ↓",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 79 §Track"
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
       "label": "Every cross-sell simulator opportunity",
       "columns": [
        "Recommendation generated",
        "Product",
        "Target product",
        "Customer/session where permitted",
        "Channel",
        "Placement",
        "Rank",
        "Impression",
        "Click/select",
        "Add to cart",
        "Purchase",
        "Redemption",
        "Revenue"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 79 §Track"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected cross-sell simulator opportunity",
       "bindsTo": null,
       "columns": [
        "Recommendation generated",
        "Product",
        "Target product",
        "Customer/session where permitted",
        "Channel",
        "Placement",
        "Rank",
        "Impression",
        "Click/select",
        "Add to cart",
        "Purchase",
        "Redemption",
        "Revenue"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Basket”, “Candidate Results”, “Expected Incremental Value”, “Maximum Expected Incremental Revenue”, “Current Basket”, “Potential Cross-Sell Products”.",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 79 §Track"
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
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** Create relationship, Edit relationship, Activate relationship, Approve AI relationship, Enable partner relationship, Change affinity threshold, Change category permissions, Override suppression, Import relationships. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 79 §Permissions should govern"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The cross-sell simulator opportunity list.",
   "error": "Could not load. Names which read failed and leaves the cross-sell simulator opportunity untouched.",
   "emptyFirstRun": "No cross-sell simulator opportunity yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the cross-sell simulator opportunity are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "simulateRecommendationStrategy",
    "contract": "promotions",
    "purpose": "Simulate cross-sell",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Recommendation generated",
    "Product",
    "Target product",
    "Customer/session where permitted",
    "Channel",
    "Placement"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-668",
   "workshopBoard": "wireframes/WS180 Upsell,CrossSellEngine Board 3.dc.html#adm-668"
  },
  "apisNote": "Regenerated 9 September 2026 from Upsell,CrossSellEngine.pdf page 79. 0 of 13 labels bound to a contract property; 33 of 158 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "getProductAffinity": {
  "method": "GET",
  "path": "/product-affinity",
  "contract": "promotions",
  "summary": "What is actually bought together",
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
    "name": "minLift",
    "in": "query",
    "required": null
   },
   {
    "name": "windowDays",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "ProductAffinity"
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
 "listUpsellCrossSell": {
  "method": "GET",
  "path": "/upsell-cross-sell",
  "contract": "promotions",
  "summary": "Upsell, Cross-Sell & Attach-Rate Analytics",
  "permission": "PRICE_VIEW",
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
  "responds": "UpsellCrossSellAttachRateAnalyticsView"
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
 "ProductAffinity": {
  "type": "object",
  "description": "Upsell boards 3.3 and 3.4. **Support and lift together**, because high support with no lift is two popular products rather than a relationship.\n",
  "properties": {
   "fromProductId": {
    "type": "string",
    "format": "uuid"
   },
   "toProductId": {
    "type": "string",
    "format": "uuid"
   },
   "basketsTogether": {
    "type": "integer"
   },
   "support": {
    "type": "number"
   },
   "confidence": {
    "type": "number"
   },
   "lift": {
    "type": "number"
   },
   "windowDays": {
    "type": "integer"
   },
   "computedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
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
