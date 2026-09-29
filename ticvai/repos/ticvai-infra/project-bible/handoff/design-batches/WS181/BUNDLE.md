# WS181 — Upsell,CrossSellEngine board 2

**10 screens · 6 operations · 4 schemas · 3 permissions**

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
  `ORDER_MODIFY, PRODUCT_CONFIGURE, PRODUCT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-649` | Upsell & Upgrade Command Center | commandCentre | 1 | 0 | — |
| `ADM-650` | Upgrade Path & Product Ladder Builder | listDetail | 2 | 0 | — |
| `ADM-651` | Upsell Eligibility & Qualification Rules | listDetail | 1 | 0 | — |
| `ADM-652` | Upgrade Price Difference & Value Proposition Manager | configEditor | 1 | 0 | — |
| `ADM-653` | Ticket, Experience & Bundle Upgrade Manager | listDetail | 1 | 0 | — |
| `ADM-654` | Membership & Pass Upgrade Engine | listDetail | 1 | 0 | — |
| `ADM-655` | Pre-Purchase, Cart & Checkout Upsell Manager | configEditor | 1 | 0 | — |
| `ADM-656` | Post-Purchase & In-Journey Upgrade Manager | configEditor | 2 | 0 | — |
| `ADM-657` | Upsell Ranking, Propensity & AI Opportunity Engine | listDetail | 1 | 0 | — |
| `ADM-658` | Upgrade Simulator, Comparison & AI Advisor | listDetail | 1 | 0 | — |

## Thin screens in this batch

**ADM-650, ADM-653, ADM-654, ADM-657, ADM-658 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-649",
  "name": "Upsell & Upgrade Command Center",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Upsell,CrossSellEngine.pdf",
   "board": "2",
   "number": "1",
   "page": 37
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/upsell-upgrade-command-center-adm-649",
   "component": "apps/ticvai-web/src/routes/commercial/UpsellUpgradeCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-650",
    "ADM-651",
    "ADM-652",
    "ADM-653",
    "ADM-654",
    "ADM-655",
    "ADM-656",
    "ADM-657",
    "ADM-658"
   ],
   "transitions": [
    {
     "to": "ADM-002",
     "trigger": "Back to Platform Dashboard",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "ADM-650",
     "trigger": "Upgrade Path & Product Ladder Builder",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    },
    {
     "to": "ADM-651",
     "trigger": "Upsell Eligibility & Qualification Rules",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    },
    {
     "to": "ADM-652",
     "trigger": "Upgrade Price Difference & Value Proposition Manager",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    },
    {
     "to": "ADM-653",
     "trigger": "Ticket, Experience & Bundle Upgrade Manager",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    },
    {
     "to": "ADM-654",
     "trigger": "Membership & Pass Upgrade Engine",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    },
    {
     "to": "ADM-655",
     "trigger": "Pre-Purchase, Cart & Checkout Upsell Manager",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    },
    {
     "to": "ADM-656",
     "trigger": "Post-Purchase & In-Journey Upgrade Manager",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    },
    {
     "to": "ADM-657",
     "trigger": "Upsell Ranking, Propensity & AI Opportunity Engine",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    },
    {
     "to": "ADM-658",
     "trigger": "Upgrade Simulator, Comparison & AI Advisor",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide centralized operational and commercial visibility into all upsell and upgrade activities.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Active Upsell Rules",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 37 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Active Upgrade Paths",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 37 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Upsell Recommendations",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 37 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Upgrade Offers Presented",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 37 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Acceptance Rate",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 37 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Upgrade Conversion",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 37 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Upsell Revenue",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 37 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Incremental Revenue",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 37 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Average Upgrade Value",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 37 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "AOV Uplift",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 37 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Margin Uplift",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 37 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "AI-Generated Opportunities",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 37 §KPI Cards"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The upsell upgrade list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the upsell upgrade untouched.",
   "emptyFirstRun": "No upsell upgrade yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the upsell upgrade are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getRecommendationPerformance",
    "contract": "promotions",
    "purpose": "Upgrade performance",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-649",
   "workshopBoard": "wireframes/WS179 Upsell,CrossSellEngine Board 2.dc.html#adm-649"
  },
  "apisNote": "Regenerated 9 September 2026 from Upsell,CrossSellEngine.pdf page 37. 0 of 0 labels bound to a contract property; 12 of 34 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-650",
  "name": "Upgrade Path & Product Ladder Builder",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Upsell,CrossSellEngine.pdf",
   "board": "2",
   "number": "2",
   "page": 39
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/upgrade-path-product-ladder-builder-adm-650",
   "component": "apps/ticvai-web/src/routes/commercial/UpgradePathProductLadderBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-649"
   ],
   "exitTo": [
    "ADM-649"
   ],
   "transitions": [
    {
     "to": "ADM-649",
     "trigger": "Back to Upsell & Upgrade Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Define valid upgrade relationships between products. governed product relationships.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 2 actions on this screen and the screen declares 0 operations.** Unserved: Recommend next level only, Recommend multiple levels. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 39 §Allow"
   },
   {
    "operation": null,
    "why": "**Upgrade Path & Product Ladder Builder declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 39"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 39"
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
       "label": "Recommend next level only",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 39 §Allow"
      },
      {
       "kind": "secondaryButton",
       "label": "Recommend multiple levels",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 39 §Allow"
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
   "loading": "The upgrade path product list.",
   "error": "Could not load. Names which read failed and leaves the upgrade path product untouched.",
   "emptyFirstRun": "No upgrade path product yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the upgrade path product are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listProductRelationships",
    "contract": "promotions",
    "purpose": "The ladder",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "setProductRelationships",
    "contract": "promotions",
    "purpose": "Order it",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listProductRelationships"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-650",
   "workshopBoard": "wireframes/WS179 Upsell,CrossSellEngine Board 2.dc.html#adm-650"
  },
  "apisNote": "Regenerated 9 September 2026 from Upsell,CrossSellEngine.pdf page 39. 0 of 0 labels bound to a contract property; 2 of 30 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-651",
  "name": "Upsell Eligibility & Qualification Rules",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Upsell,CrossSellEngine.pdf",
   "board": "2",
   "number": "3",
   "page": 41
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/upsell-eligibility-qualification-rules-adm-651",
   "component": "apps/ticvai-web/src/routes/commercial/UpsellEligibilityQualificationRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-649"
   ],
   "exitTo": [
    "ADM-649"
   ],
   "transitions": [
    {
     "to": "ADM-649",
     "trigger": "Back to Upsell & Upgrade Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Determine whether an upsell opportunity is valid for the current customer and transaction. This screen provides upgrade-specific qualification, while the reusable customer targeting capabilities remain centralized in the recommendation/CRM eligibility architecture.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 10 actions on this screen and the screen declares 0 operations.** Unserved: Current product, Product variant, Customer type, Guest type, Membership, Channel, Venue, Timeslot …. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 41 §Support"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 41"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 41"
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
       "label": "Current product",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 41 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Product variant",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 41 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Customer type",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 41 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Guest type",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 41 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Membership",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 41 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Channel",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 41 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Venue",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 41 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Timeslot",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 41 §Support"
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
   "loading": "The upsell eligibility qualification list.",
   "error": "Could not load. Names which read failed and leaves the upsell eligibility qualification untouched.",
   "emptyFirstRun": "No upsell eligibility qualification yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the upsell eligibility qualification are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "updateRecommendationStrategy",
    "contract": "promotions",
    "purpose": "Eligibility and qualification",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listRecommendationStrategies"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-651",
   "workshopBoard": "wireframes/WS179 Upsell,CrossSellEngine Board 2.dc.html#adm-651"
  },
  "apisNote": "Regenerated 9 September 2026 from Upsell,CrossSellEngine.pdf page 41. 0 of 0 labels bound to a contract property; 10 of 34 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-652",
  "name": "Upgrade Price Difference & Value Proposition Manager",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Upsell,CrossSellEngine.pdf",
   "board": "2",
   "number": "4",
   "page": 42
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/upgrade-price-difference-value-proposition-manager-adm-652",
   "component": "apps/ticvai-web/src/routes/commercial/UpgradePriceDifferenceValuePropositionManager.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-649"
   ],
   "exitTo": [
    "ADM-649"
   ],
   "transitions": [
    {
     "to": "ADM-649",
     "trigger": "Back to Upsell & Upgrade Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure benefits such as) and no display directory — it is settings, not a population",
  "purpose": "Configure how TICVAI calculates and communicates the commercial difference between the current product and the recommended upgrade. The Recommendation Engine should not become the authoritative pricing engine. It should consume the authoritative price difference from Pricing/Promotion services.",
  "gaps": [
   {
    "operation": null,
    "why": "**Upgrade Price Difference & Value Proposition Manager declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
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
       "label": "Fast Track",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 42 §Configure benefits such as"
      },
      {
       "kind": "selectField",
       "label": "Additional attractions",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 42 §Configure benefits such as"
      },
      {
       "kind": "selectField",
       "label": "Premium seating",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 42 §Configure benefits such as"
      },
      {
       "kind": "selectField",
       "label": "Extra validity",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 42 §Configure benefits such as"
      },
      {
       "kind": "selectField",
       "label": "Exclusive access",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 42 §Configure benefits such as"
      },
      {
       "kind": "selectField",
       "label": "Included meal",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 42 §Configure benefits such as"
      },
      {
       "kind": "selectField",
       "label": "Free parking",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 42 §Configure benefits such as"
      },
      {
       "kind": "selectField",
       "label": "Additional visits",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 42 §Configure benefits such as"
      },
      {
       "kind": "selectField",
       "label": "VIP experience",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 42 §Configure benefits such as"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The upgrade price difference configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the upgrade price difference untouched.",
   "emptyFirstRun": "No upgrade price difference configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "quoteUpgrade",
    "contract": "orders",
    "purpose": "The price gap, and what the guest gains",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-652",
   "workshopBoard": "wireframes/WS179 Upsell,CrossSellEngine Board 2.dc.html#adm-652"
  },
  "apisNote": "Regenerated 9 September 2026 from Upsell,CrossSellEngine.pdf page 42. 0 of 0 labels bound to a contract property; 9 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "orderId",
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
  "id": "ADM-653",
  "name": "Ticket, Experience & Bundle Upgrade Manager",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Upsell,CrossSellEngine.pdf",
   "board": "2",
   "number": "5",
   "page": 44
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/ticket-experience-bundle-upgrade-manager-adm-653",
   "component": "apps/ticvai-web/src/routes/commercial/TicketExperienceBundleUpgradeManager.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-649"
   ],
   "exitTo": [
    "ADM-649"
   ],
   "transitions": [
    {
     "to": "ADM-649",
     "trigger": "Back to Upsell & Upgrade Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Track; Show) and no metric row",
  "purpose": "Configure detailed upsell relationships for ticketing and experience products.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 44 §Track"
   },
   {
    "operation": null,
    "why": "**Ticket, Experience & Bundle Upgrade Manager declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
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
       "label": "Every ticket experience bundle",
       "columns": [
        "Meal — ✓",
        "Parking — ✓",
        "Photo — ✓",
        "Original Basket: AED 720",
        "Premium Basket: AED 940"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 44 §Track"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected ticket experience bundle",
       "bindsTo": null,
       "columns": [
        "Meal — ✓",
        "Parking — ✓",
        "Photo — ✓",
        "Original Basket: AED 720",
        "Premium Basket: AED 940"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Experience Upgrade”, “Standard Family Bundle”, “Benefit”, “Fast”.",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 44 §Track"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The ticket experience bundle list.",
   "error": "Could not load. Names which read failed and leaves the ticket experience bundle untouched.",
   "emptyFirstRun": "No ticket experience bundle yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the ticket experience bundle are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "quoteUpgrade",
    "contract": "orders",
    "purpose": "Ticket, experience and bundle upgrades",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Meal — ✓",
    "Parking — ✓",
    "Photo — ✓",
    "Original Basket: AED 720",
    "Premium Basket: AED 940"
   ],
   "params": [
    {
     "name": "orderId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-653",
   "workshopBoard": "wireframes/WS179 Upsell,CrossSellEngine Board 2.dc.html#adm-653"
  },
  "apisNote": "Regenerated 9 September 2026 from Upsell,CrossSellEngine.pdf page 44. 0 of 5 labels bound to a contract property; 5 of 21 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-654",
  "name": "Membership & Pass Upgrade Engine",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Upsell,CrossSellEngine.pdf",
   "board": "2",
   "number": "6",
   "page": 45
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/membership-pass-upgrade-engine-adm-654",
   "component": "apps/ticvai-web/src/routes/commercial/MembershipPassUpgradeEngine.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-649"
   ],
   "exitTo": [
    "ADM-649"
   ],
   "transitions": [
    {
     "to": "ADM-649",
     "trigger": "Back to Upsell & Upgrade Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Handle one of the most commercially valuable upgrade scenarios: Converting visitors into members/pass holders.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 45"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 45"
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
       "impliedBy": "quoteUpgrade",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "quoteUpgrade"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The membership pass upgrade list.",
   "error": "Could not load. Names which read failed and leaves the membership pass upgrade untouched.",
   "emptyFirstRun": "No membership pass upgrade yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the membership pass upgrade are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "quoteUpgrade",
    "contract": "orders",
    "purpose": "Membership and pass upgrades",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-654",
   "workshopBoard": "wireframes/WS179 Upsell,CrossSellEngine Board 2.dc.html#adm-654"
  },
  "apisNote": "Regenerated 9 September 2026 from Upsell,CrossSellEngine.pdf page 45. 0 of 0 labels bound to a contract property; 0 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "orderId",
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
  "id": "ADM-655",
  "name": "Pre-Purchase, Cart & Checkout Upsell Manager",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Upsell,CrossSellEngine.pdf",
   "board": "2",
   "number": "7",
   "page": 47
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/pre-purchase-cart-checkout-upsell-manager-adm-655",
   "component": "apps/ticvai-web/src/routes/commercial/PrePurchaseCartCheckoutUpsellManager.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-649"
   ],
   "exitTo": [
    "ADM-649"
   ],
   "transitions": [
    {
     "to": "ADM-649",
     "trigger": "Back to Upsell & Upgrade Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Control upselling during the active purchase journey.",
  "gaps": [
   {
    "operation": null,
    "why": "**Pre-Purchase, Cart & Checkout Upsell Manager declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
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
       "label": "Maximum upgrade cards",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 47 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Upgrade order",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 47 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Display style",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 47 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Price-difference threshold",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 47 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Minimum relevance",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 47 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Suppression behavior",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 47 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The pre-purchase cart checkout configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the pre-purchase cart checkout untouched.",
   "emptyFirstRun": "No pre-purchase cart checkout configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "updateRecommendationStrategy",
    "contract": "promotions",
    "purpose": "Cart and checkout placements",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listRecommendationStrategies"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-655",
   "workshopBoard": "wireframes/WS179 Upsell,CrossSellEngine Board 2.dc.html#adm-655"
  },
  "apisNote": "Regenerated 9 September 2026 from Upsell,CrossSellEngine.pdf page 47. 0 of 0 labels bound to a contract property; 6 of 21 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-656",
  "name": "Post-Purchase & In-Journey Upgrade Manager",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Upsell,CrossSellEngine.pdf",
   "board": "2",
   "number": "8",
   "page": 48
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/post-purchase-in-journey-upgrade-manager-adm-656",
   "component": "apps/ticvai-web/src/routes/commercial/PostPurchaseInJourneyUpgradeManager.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-649"
   ],
   "exitTo": [
    "ADM-649"
   ],
   "transitions": [
    {
     "to": "ADM-649",
     "trigger": "Back to Upsell & Upgrade Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Support upgrades after the initial transaction where the product and operational rules permit them. This is explicitly important because upselling should not stop at checkout.",
  "gaps": [
   {
    "operation": null,
    "why": "**Post-Purchase & In-Journey Upgrade Manager declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
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
       "label": "Immediately after purchase",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 48 §Configure"
      },
      {
       "kind": "textField",
       "label": "Up to X hours before visit",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 48 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Until first redemption",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 48 §Configure"
      },
      {
       "kind": "textField",
       "label": "After first redemption where allowed",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 48 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Until product expiry",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 48 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The post-purchase in-journey upgrade configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the post-purchase in-journey upgrade untouched.",
   "emptyFirstRun": "No post-purchase in-journey upgrade configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "updateRecommendationStrategy",
    "contract": "promotions",
    "purpose": "Post-purchase placements",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listRecommendationStrategies"
    ]
   },
   {
    "operationId": "quoteUpgrade",
    "contract": "orders",
    "purpose": "Upgrade after the fact",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-656",
   "workshopBoard": "wireframes/WS179 Upsell,CrossSellEngine Board 2.dc.html#adm-656"
  },
  "apisNote": "Regenerated 9 September 2026 from Upsell,CrossSellEngine.pdf page 48. 0 of 0 labels bound to a contract property; 5 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "orderId",
     "from": "navigation"
    },
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
  "id": "ADM-657",
  "name": "Upsell Ranking, Propensity & AI Opportunity Engine",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Upsell,CrossSellEngine.pdf",
   "board": "2",
   "number": "9",
   "page": 50
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/upsell-ranking-propensity-ai-opportunity-engine-adm-657",
   "component": "apps/ticvai-web/src/routes/commercial/UpsellRankingPropensityAiOpportunityEngine.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-649"
   ],
   "exitTo": [
    "ADM-649"
   ],
   "transitions": [
    {
     "to": "ADM-649",
     "trigger": "Back to Upsell & Upgrade Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Use AI and commercial logic to identify the strongest upgrade opportunity for each customer/context.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 50"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 50"
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
   "loading": "The upsell ranking propensity list.",
   "error": "Could not load. Names which read failed and leaves the upsell ranking propensity untouched.",
   "emptyFirstRun": "No upsell ranking propensity yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the upsell ranking propensity are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getRecommendationPerformance",
    "contract": "promotions",
    "purpose": "Propensity and opportunity",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-657",
   "workshopBoard": "wireframes/WS179 Upsell,CrossSellEngine Board 2.dc.html#adm-657"
  },
  "apisNote": "Regenerated 9 September 2026 from Upsell,CrossSellEngine.pdf page 50. 0 of 0 labels bound to a contract property; 0 of 30 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-658",
  "name": "Upgrade Simulator, Comparison & AI Advisor",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Upsell,CrossSellEngine.pdf",
   "board": "2",
   "number": "10",
   "page": 51
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/upgrade-simulator-comparison-ai-advisor-adm-658",
   "component": "apps/ticvai-web/src/routes/commercial/UpgradeSimulatorComparisonAiAdvisor.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-649"
   ],
   "exitTo": [
    "ADM-649"
   ],
   "transitions": [
    {
     "to": "ADM-649",
     "trigger": "Back to Upsell & Upgrade Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow business users to simulate an upsell strategy before activation.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 51"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 51"
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
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** Create upgrade path, Activate upgrade path, Change priority, Change commercial threshold, Enable AI discovery, Approve AI-generated relationship, Enable post-purchase upgrade, Override product restriction. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 51 §Permissions should separately govern"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "simulateRecommendationStrategy",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "simulateRecommendationStrategy"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The upgrade simulator comparison list.",
   "error": "Could not load. Names which read failed and leaves the upgrade simulator comparison untouched.",
   "emptyFirstRun": "No upgrade simulator comparison yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the upgrade simulator comparison are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "simulateRecommendationStrategy",
    "contract": "promotions",
    "purpose": "Simulate the ladder",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-658",
   "workshopBoard": "wireframes/WS179 Upsell,CrossSellEngine Board 2.dc.html#adm-658"
  },
  "apisNote": "Regenerated 9 September 2026 from Upsell,CrossSellEngine.pdf page 51. 0 of 0 labels bound to a contract property; 8 of 137 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "quoteUpgrade": {
  "method": "POST",
  "path": "/orders/{orderId}/upgrade-quote",
  "contract": "orders",
  "summary": "What an upgrade costs, pro-rata",
  "permission": "ORDER_MODIFY",
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
  "responds": null
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
 "Money": {
  "type": "object",
  "x-ticvai-persistence-kind": "valueObject",
  "x-ticvai-persistence-column": "numeric(18,4)",
  "description": "**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n",
  "required": [
   "amount",
   "currency",
   "scale"
  ],
  "properties": {
   "amount": {
    "type": "string",
    "description": "Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n",
    "pattern": "^-?\\d+(\\.\\d{1,4})?$"
   },
   "currency": {
    "type": "string",
    "description": "**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n",
    "pattern": "^[A-Z]{3}$"
   },
   "scale": {
    "type": "integer",
    "description": "Resolved from the region alongside `currency`.",
    "minimum": 0,
    "maximum": 4
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
 }
}
```
