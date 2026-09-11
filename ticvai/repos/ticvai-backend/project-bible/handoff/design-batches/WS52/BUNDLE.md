# WS52 — Promotions   Bundles Management board 8

**10 screens · 10 operations · 11 schemas · 2 permissions**

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
  `PRICE_CONFIGURE, PRICE_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **0 of these operations work offline**
  
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-208` | Stacking & Conflict Command Center | commandCentre | 1 | 0 | — |
| `ADM-209` | Promotion Priority & Hierarchy Manager | listDetail | 1 | 0 | — |
| `ADM-210` | Promotion Stacking Rule Builder | listDetail | 1 | 0 | — |
| `ADM-211` | Promotion Exclusion & Compatibility Matrix | listDetail | 1 | 0 | — |
| `ADM-212` | Discount Calculation & Application Sequence | configEditor | 1 | 0 | — |
| `ADM-213` | Best Offer & Customer Benefit Resolver | listDetail | 1 | 0 | — |
| `ADM-214` | Discount Cap & Maximum Benefit Controller | configEditor | 1 | 0 | — |
| `ADM-215` | Conflict Detection & Resolution Center | listDetail | 1 | 1 | — |
| `ADM-216` | Promotion Decision Trace & Transaction Explainer | listDetail | 1 | 0 | — |
| `ADM-217` | Conflict Simulation & AI Optimization | listDetail | 1 | 0 | — |

## Thin screens in this batch

**ADM-209, ADM-210, ADM-211, ADM-213, ADM-216, ADM-217 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-208",
  "name": "Stacking & Conflict Command Center",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "8",
   "number": "1",
   "page": 109
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/stacking-conflict-command-center-adm-208",
   "component": "apps/ticvai-web/src/routes/commercial/StackingConflictCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-209",
    "ADM-210",
    "ADM-211",
    "ADM-212",
    "ADM-213",
    "ADM-214",
    "ADM-215",
    "ADM-216",
    "ADM-217"
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
     "to": "ADM-209",
     "trigger": "Works in Promotion Priority & Hierarchy Manager",
     "provenance": "flow F161 step 1→2",
     "operation": "listStackingConflict"
    },
    {
     "to": "ADM-210",
     "trigger": "Works in Promotion Stacking Rule Builder",
     "provenance": "flow F161 step 3→4",
     "operation": "listStackingConflict"
    },
    {
     "to": "ADM-211",
     "trigger": "Works in Promotion Exclusion & Compatibility Matrix",
     "provenance": "flow F161 step 5→6",
     "operation": "listStackingConflict"
    },
    {
     "to": "ADM-212",
     "trigger": "Works in Discount Calculation & Application Sequence",
     "provenance": "flow F161 step 7→8",
     "operation": "listStackingConflict"
    },
    {
     "to": "ADM-213",
     "trigger": "Works in Best Offer & Customer Benefit Resolver",
     "provenance": "flow F161 step 9→10",
     "operation": "listStackingConflict"
    },
    {
     "to": "ADM-214",
     "trigger": "Works in Discount Cap & Maximum Benefit Controller",
     "provenance": "flow F161 step 11→12",
     "operation": "listStackingConflict"
    },
    {
     "to": "ADM-215",
     "trigger": "Works in Conflict Detection & Resolution Center",
     "provenance": "flow F161 step 13→14",
     "operation": "listStackingConflict"
    },
    {
     "to": "ADM-216",
     "trigger": "Works in Promotion Decision Trace & Transaction Explainer",
     "provenance": "flow F161 step 15→16",
     "operation": "listStackingConflict"
    },
    {
     "to": "ADM-217",
     "trigger": "Works in Conflict Simulation & AI Optimization",
     "provenance": "flow F161 step 17→18",
     "operation": "listStackingConflict"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide centralized operational visibility into promotion interactions across TICVAI.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Active Promotion Rules",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 109 §KPI Cards",
       "bindsTo": "StackingConflictCommandCenterView.activePromotionRules"
      },
      {
       "kind": "metricTile",
       "label": "Stackable Promotions",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 109 §KPI Cards",
       "bindsTo": "StackingConflictCommandCenterView.stackablePromotions"
      },
      {
       "kind": "metricTile",
       "label": "Exclusive Promotions",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 109 §KPI Cards",
       "bindsTo": "StackingConflictCommandCenterView.exclusivePromotions"
      },
      {
       "kind": "metricTile",
       "label": "Priority Rules",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 109 §KPI Cards",
       "bindsTo": "StackingConflictCommandCenterView.priorityRules"
      },
      {
       "kind": "metricTile",
       "label": "Conflicts Detected",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 109 §KPI Cards",
       "bindsTo": "StackingConflictCommandCenterView.conflictsDetected"
      },
      {
       "kind": "metricTile",
       "label": "Critical Conflicts",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 109 §KPI Cards",
       "bindsTo": "StackingConflictCommandCenterView.criticalConflicts"
      },
      {
       "kind": "metricTile",
       "label": "Auto-Resolved Conflicts",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 109 §KPI Cards",
       "bindsTo": "StackingConflictCommandCenterView.autoResolvedConflicts"
      },
      {
       "kind": "metricTile",
       "label": "Transactions with Multiple Offers",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 109 §KPI Cards",
       "bindsTo": "StackingConflictCommandCenterView.transactionsWithMultipleOffers"
      },
      {
       "kind": "metricTile",
       "label": "Average Promotions per Transaction",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 109 §KPI Cards",
       "bindsTo": "StackingConflictCommandCenterView.averagePromotionsPerTransaction"
      },
      {
       "kind": "metricTile",
       "label": "Discount Exposure",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 109 §KPI Cards",
       "bindsTo": "StackingConflictCommandCenterView.discountExposure"
      },
      {
       "kind": "metricTile",
       "label": "Prevented Over-Discount",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 109 §KPI Cards",
       "bindsTo": "StackingConflictCommandCenterView.preventedOverDiscount"
      },
      {
       "kind": "metricTile",
       "label": "Revenue Protected",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 109 §KPI Cards",
       "bindsTo": "StackingConflictCommandCenterView.revenueProtected"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The stacking conflict list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the stacking conflict untouched.",
   "emptyFirstRun": "No stacking conflict yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the stacking conflict are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listStackingConflict",
    "contract": "promotions",
    "purpose": "Stacking & Conflict Command Center",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "StackingConflictCommandCenterView.activePromotionRules",
    "StackingConflictCommandCenterView.stackablePromotions",
    "StackingConflictCommandCenterView.exclusivePromotions",
    "StackingConflictCommandCenterView.priorityRules",
    "StackingConflictCommandCenterView.conflictsDetected",
    "StackingConflictCommandCenterView.criticalConflicts"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-208"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 109. 12 of 12 labels bound to a contract property; 12 of 31 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-209",
  "name": "Promotion Priority & Hierarchy Manager",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "8",
   "number": "2",
   "page": 110
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/promotion-priority-hierarchy-manager-adm-209",
   "component": "apps/ticvai-web/src/routes/commercial/PromotionPriorityHierarchyManager.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-208"
   ],
   "exitTo": [
    "ADM-208"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-208, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-208",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F161 step 2→3",
     "operation": "listPromotionPriorityHierarchy"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Define the relative priority of different promotion families and individual offers.",
  "gaps": [
   {
    "operation": null,
    "why": "**Promotion Priority & Hierarchy Manager declares no operation that writes anything** — its only declared call is `listPromotionPriorityHierarchy`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 110"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 110"
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
       "impliedBy": "listPromotionPriorityHierarchy",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The promotion priority hierarchy list.",
   "error": "Could not load. Names which read failed and leaves the promotion priority hierarchy untouched.",
   "emptyFirstRun": "No promotion priority hierarchy yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the promotion priority hierarchy are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPromotionPriorityHierarchy",
    "contract": "promotions",
    "purpose": "Promotion Priority & Hierarchy Manager",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "PromotionPriorityHierarchyManagerView.promotionFamily",
    "PromotionPriorityHierarchyManagerView.promotion",
    "PromotionPriorityHierarchyManagerView.priorityNumber",
    "PromotionPriorityHierarchyManagerView.priorityGroup",
    "PromotionPriorityHierarchyManagerView.effectiveDates"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-209"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 110. 0 of 0 labels bound to a contract property; 0 of 29 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-210",
  "name": "Promotion Stacking Rule Builder",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "8",
   "number": "3",
   "page": 111
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/promotion-stacking-rule-builder-adm-210",
   "component": "apps/ticvai-web/src/routes/commercial/PromotionStackingRuleBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-208"
   ],
   "exitTo": [
    "ADM-208"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-208, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-208",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F161 step 4→5",
     "operation": "setPromotionStackingRule"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Define which promotions can be combined.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 111"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 111"
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
       "provenance": "contract operation setPromotionStackingRule"
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
       "impliedBy": "setPromotionStackingRule"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The promotion stacking rule list.",
   "error": "Could not load. Names which read failed and leaves the promotion stacking rule untouched.",
   "emptyFirstRun": "No promotion stacking rule yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the promotion stacking rule are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setPromotionStackingRule",
    "contract": "promotions",
    "purpose": "Promotion Stacking Rule Builder",
    "trigger": "onAction",
    "invalidates": [
     "setPromotionStackingRule"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-210"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 111. 0 of 0 labels bound to a contract property; 0 of 19 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-211",
  "name": "Promotion Exclusion & Compatibility Matrix",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "8",
   "number": "4",
   "page": 112
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/promotion-exclusion-compatibility-matrix-adm-211",
   "component": "apps/ticvai-web/src/routes/commercial/PromotionExclusionCompatibilityMatrix.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-208"
   ],
   "exitTo": [
    "ADM-208"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-208, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-208",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F161 step 6→7",
     "operation": "listPromotionExclusionCompatibility"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Clicking a relationship should show) and no metric row",
  "purpose": "Provide administrators with a visual matrix showing which promotion categories can interact.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every promotion exclusion compatibility",
       "columns": [
        "PromotionExclusionCompatibilityMatrixView.applicableProducts",
        "PromotionExclusionCompatibilityMatrixView.applicableVenues",
        "PromotionExclusionCompatibilityMatrixView.channels",
        "PromotionExclusionCompatibilityMatrixView.customerSegments",
        "PromotionExclusionCompatibilityMatrixView.rule",
        "PromotionExclusionCompatibilityMatrixView.priority",
        "PromotionExclusionCompatibilityMatrixView.effectiveDates",
        "PromotionExclusionCompatibilityMatrixView.exceptions"
       ],
       "bindsTo": "PromotionExclusionCompatibilityMatrixView",
       "operation": "listPromotionExclusionCompatibility",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 112 §Clicking a relationship should show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected promotion exclusion compatibility",
       "bindsTo": "PromotionExclusionCompatibilityMatrixView",
       "columns": [
        "PromotionExclusionCompatibilityMatrixView.applicableProducts",
        "PromotionExclusionCompatibilityMatrixView.applicableVenues",
        "PromotionExclusionCompatibilityMatrixView.channels",
        "PromotionExclusionCompatibilityMatrixView.customerSegments",
        "PromotionExclusionCompatibilityMatrixView.rule",
        "PromotionExclusionCompatibilityMatrixView.priority",
        "PromotionExclusionCompatibilityMatrixView.effectiveDates",
        "PromotionExclusionCompatibilityMatrixView.exceptions"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Coupo Members Loyal Ban BOG”, “Membershi”, “Use”, “Conflict Detection”.",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 112 §Clicking a relationship should show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The promotion exclusion compatibility list.",
   "error": "Could not load. Names which read failed and leaves the promotion exclusion compatibility untouched.",
   "emptyFirstRun": "No promotion exclusion compatibility yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the promotion exclusion compatibility are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPromotionExclusionCompatibility",
    "contract": "promotions",
    "purpose": "Promotion Exclusion & Compatibility Matrix",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "PromotionExclusionCompatibilityMatrixView.applicableProducts",
    "PromotionExclusionCompatibilityMatrixView.applicableVenues",
    "PromotionExclusionCompatibilityMatrixView.channels",
    "PromotionExclusionCompatibilityMatrixView.customerSegments",
    "PromotionExclusionCompatibilityMatrixView.rule",
    "PromotionExclusionCompatibilityMatrixView.priority"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-211"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 112. 8 of 8 labels bound to a contract property; 8 of 23 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-212",
  "name": "Discount Calculation & Application Sequence",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "8",
   "number": "5",
   "page": 113
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/discount-calculation-application-sequence-adm-212",
   "component": "apps/ticvai-web/src/routes/commercial/DiscountCalculationApplicationSequence.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-208"
   ],
   "exitTo": [
    "ADM-208"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-208, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-208",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F161 step 8→9",
     "operation": "listDiscountCalculationApplication"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure whether promotion applies) and no display directory — it is settings, not a population",
  "purpose": "Control the mathematical order in which multiple permitted benefits are calculated.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Before tax",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 113 §Configure whether promotion applies"
      },
      {
       "kind": "selectField",
       "label": "After tax",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 113 §Configure whether promotion applies"
      },
      {
       "kind": "selectField",
       "label": "Before fee",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 113 §Configure whether promotion applies"
      },
      {
       "kind": "selectField",
       "label": "After fee",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 113 §Configure whether promotion applies"
      },
      {
       "kind": "selectField",
       "label": "Product only",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 113 §Configure whether promotion applies"
      },
      {
       "kind": "selectField",
       "label": "Transaction total",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 113 §Configure whether promotion applies"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The discount calculation application configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the discount calculation application untouched.",
   "emptyFirstRun": "No discount calculation application configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listDiscountCalculationApplication",
    "contract": "promotions",
    "purpose": "Discount Calculation & Application Sequence",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-212"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 113. 0 of 0 labels bound to a contract property; 6 of 33 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-213",
  "name": "Best Offer & Customer Benefit Resolver",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "8",
   "number": "6",
   "page": 114
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/best-offer-customer-benefit-resolver-adm-213",
   "component": "apps/ticvai-web/src/routes/commercial/BestOfferCustomerBenefitResolver.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-208"
   ],
   "exitTo": [
    "ADM-208"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-208, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-208",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F161 step 10→11",
     "operation": "listBestOfferCustomer"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Determine which promotion or combination gives the guest the correct/best permitted commercial outcome.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 114"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 114"
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
       "impliedBy": "listBestOfferCustomer",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The best offer customer list.",
   "error": "Could not load. Names which read failed and leaves the best offer customer untouched.",
   "emptyFirstRun": "No best offer customer yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the best offer customer are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listBestOfferCustomer",
    "contract": "promotions",
    "purpose": "Best Offer & Customer Benefit Resolver",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "BestOfferCustomerBenefitResolverView.useTheHighestRankedPromotion",
    "BestOfferCustomerBenefitResolverView.favorAStrategicallySelectedCampaign",
    "BestOfferCustomerBenefitResolverView.honorContractualCustomerSpecificPricingFirst",
    "BestOfferCustomerBenefitResolverView.family15Aed",
    "BestOfferCustomerBenefitResolverView.bank1011750"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-213"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 114. 0 of 0 labels bound to a contract property; 0 of 13 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-214",
  "name": "Discount Cap & Maximum Benefit Controller",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "8",
   "number": "7",
   "page": 115
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/discount-cap-maximum-benefit-controller-adm-214",
   "component": "apps/ticvai-web/src/routes/commercial/DiscountCapMaximumBenefitController.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-208"
   ],
   "exitTo": [
    "ADM-208"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-208, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-208",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F161 step 12→13",
     "operation": "listDiscountCapMaximum"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure; Configured maximum) and no display directory — it is settings, not a population",
  "purpose": "Prevent stacked promotions from exceeding financial or contractual limits.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "textField",
       "label": "Maximum total discount %",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 115 §Configure"
      },
      {
       "kind": "textField",
       "label": "Maximum total discount amount",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 115 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Minimum transaction value",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 115 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Minimum product price",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 115 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Minimum margin",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 115 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum free-item value",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 115 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum promotional benefit",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 115 §Configure"
      },
      {
       "kind": "textField",
       "label": "Maximum promotions per basket",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 115 §Configure"
      },
      {
       "kind": "selectField",
       "label": "30%",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 115 §Configured maximum"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The discount cap maximum configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the discount cap maximum untouched.",
   "emptyFirstRun": "No discount cap maximum configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listDiscountCapMaximum",
    "contract": "promotions",
    "purpose": "Discount Cap & Maximum Benefit Controller",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-214"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 115. 0 of 0 labels bound to a contract property; 9 of 29 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-215",
  "name": "Conflict Detection & Resolution Center",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "8",
   "number": "8",
   "page": 116
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/conflict-detection-resolution-center-adm-215",
   "component": "apps/ticvai-web/src/routes/commercial/ConflictDetectionResolutionCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-208"
   ],
   "exitTo": [
    "ADM-208"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-208, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-208",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F161 step 14→15",
     "operation": "listConflictDetectionResolution"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Detect) and no metric row",
  "purpose": "Detect promotion conflicts during both configuration and runtime.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 2 actions on this screen and the screen declares 1 operation.** Unserved: Best price, Reject transaction where necessary. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 116 §Support"
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
       "label": "Every conflict detection resolution",
       "columns": [
        "ConflictDetectionResolutionCenterView.sameProduct",
        "ConflictDetectionResolutionCenterView.sameAudience",
        "ConflictDetectionResolutionCenterView.sameChannel",
        "ConflictDetectionResolutionCenterView.sameValidity",
        "ConflictDetectionResolutionCenterView.incompatiblePromotions",
        "ConflictDetectionResolutionCenterView.missingHierarchy",
        "ConflictDetectionResolutionCenterView.missingStackingRule",
        "ConflictDetectionResolutionCenterView.discountCapBreach",
        "ConflictDetectionResolutionCenterView.circularDependency"
       ],
       "bindsTo": "ConflictDetectionResolutionCenterView",
       "operation": "listConflictDetectionResolution",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 116 §Detect"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected conflict detection resolution",
       "bindsTo": "ConflictDetectionResolutionCenterView",
       "columns": [
        "ConflictDetectionResolutionCenterView.sameProduct",
        "ConflictDetectionResolutionCenterView.sameAudience",
        "ConflictDetectionResolutionCenterView.sameChannel",
        "ConflictDetectionResolutionCenterView.sameValidity",
        "ConflictDetectionResolutionCenterView.incompatiblePromotions",
        "ConflictDetectionResolutionCenterView.missingHierarchy",
        "ConflictDetectionResolutionCenterView.missingStackingRule",
        "ConflictDetectionResolutionCenterView.discountCapBreach",
        "ConflictDetectionResolutionCenterView.circularDependency"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Customer qualifies for”, “Eligibility”, “Compatibility”, “Priority”, “Calculation sequence”, “Discount cap”.",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 116 §Detect"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Best price",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 116 §Support"
      },
      {
       "kind": "destructiveButton",
       "label": "Reject transaction where necessary",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 116 §Support"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmRejectTransactionWhereNe",
    "component": "confirmDialog",
    "trigger": "Reject transaction where necessary",
    "body": "**Reject transaction where necessary on a conflict detection resolution is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 116 §Support"
   }
  ],
  "states": {
   "loading": "The conflict detection resolution list.",
   "error": "Could not load. Names which read failed and leaves the conflict detection resolution untouched.",
   "emptyFirstRun": "No conflict detection resolution yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the conflict detection resolution are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listConflictDetectionResolution",
    "contract": "promotions",
    "purpose": "Conflict Detection & Resolution Center",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "ConflictDetectionResolutionCenterView.sameProduct",
    "ConflictDetectionResolutionCenterView.sameAudience",
    "ConflictDetectionResolutionCenterView.sameChannel",
    "ConflictDetectionResolutionCenterView.sameValidity",
    "ConflictDetectionResolutionCenterView.incompatiblePromotions",
    "ConflictDetectionResolutionCenterView.missingHierarchy"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-215"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 116. 9 of 9 labels bound to a contract property; 11 of 27 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-216",
  "name": "Promotion Decision Trace & Transaction Explainer",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "8",
   "number": "9",
   "page": 117
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/promotion-decision-trace-transaction-explainer-adm-216",
   "component": "apps/ticvai-web/src/routes/commercial/PromotionDecisionTraceTransactionExplainer.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-208"
   ],
   "exitTo": [
    "ADM-208"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-208, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-208",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F161 step 16→17",
     "operation": "listPromotionDecisionTrace"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide complete explainability of how TICVAI arrived at the final promotional price. This screen will be extremely important for: Customer service Finance Operations Audit Partner disputes Technical support",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 117"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 117"
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
       "impliedBy": "listPromotionDecisionTrace",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The promotion decision trace list.",
   "error": "Could not load. Names which read failed and leaves the promotion decision trace untouched.",
   "emptyFirstRun": "No promotion decision trace yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the promotion decision trace are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPromotionDecisionTrace",
    "contract": "promotions",
    "purpose": "Promotion Decision Trace & Transaction Explainer",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "PromotionDecisionTraceTransactionExplainerView.family20",
    "PromotionDecisionTraceTransactionExplainerView.summer25",
    "PromotionDecisionTraceTransactionExplainerView.bank10",
    "PromotionDecisionTraceTransactionExplainerView.loyalty5",
    "PromotionDecisionTraceTransactionExplainerView.family20Eligible"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-216"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 117. 0 of 0 labels bound to a contract property; 0 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-217",
  "name": "Conflict Simulation & AI Optimization",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "8",
   "number": "10",
   "page": 118
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/conflict-simulation-ai-optimization-adm-217",
   "component": "apps/ticvai-web/src/routes/commercial/ConflictSimulationAiOptimization.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-208"
   ],
   "exitTo": [
    "ADM-208"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-208, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation."
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Test promotion interaction scenarios before publishing campaigns.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 118"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 118"
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
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** Change priority, Allow stacking, Create exclusions, Change calculation sequence, Change discount cap, Override margin floor, Create emergency rule, Activate hierarchy changes. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 118 §Separate permissions should control"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listConflict",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The conflict simulation optimization list.",
   "error": "Could not load. Names which read failed and leaves the conflict simulation optimization untouched.",
   "emptyFirstRun": "No conflict simulation optimization yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the conflict simulation optimization are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listConflict",
    "contract": "promotions",
    "purpose": "Conflict Simulation & AI Optimization",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "ConflictSimulationAiOptimizationView.customerSegment",
    "ConflictSimulationAiOptimizationView.membership",
    "ConflictSimulationAiOptimizationView.loyalty",
    "ConflictSimulationAiOptimizationView.products",
    "ConflictSimulationAiOptimizationView.basket"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-217"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 118. 0 of 0 labels bound to a contract property; 8 of 112 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "listBestOfferCustomer": {
  "method": "GET",
  "path": "/best-offer-customer",
  "contract": "promotions",
  "summary": "Best Offer & Customer Benefit Resolver",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "BestOfferCustomerBenefitResolverView"
 },
 "listConflict": {
  "method": "GET",
  "path": "/conflict",
  "contract": "promotions",
  "summary": "Conflict Simulation & AI Optimization",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ConflictSimulationAiOptimizationView"
 },
 "listConflictDetectionResolution": {
  "method": "GET",
  "path": "/conflict-detection-resolution",
  "contract": "promotions",
  "summary": "Conflict Detection & Resolution Center",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ConflictDetectionResolutionCenterView"
 },
 "listDiscountCalculationApplication": {
  "method": "GET",
  "path": "/discount-calculation-application",
  "contract": "promotions",
  "summary": "Discount Calculation & Application Sequence",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "DiscountCalculationApplicationSequenceView"
 },
 "listDiscountCapMaximum": {
  "method": "GET",
  "path": "/discount-cap-maximum",
  "contract": "promotions",
  "summary": "Discount Cap & Maximum Benefit Controller",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "DiscountCapMaximumBenefitControllerView"
 },
 "listPromotionDecisionTrace": {
  "method": "GET",
  "path": "/promotion-decision-trace",
  "contract": "promotions",
  "summary": "Promotion Decision Trace & Transaction Explainer",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "PromotionDecisionTraceTransactionExplainerView"
 },
 "listPromotionExclusionCompatibility": {
  "method": "GET",
  "path": "/promotion-exclusion-compatibility",
  "contract": "promotions",
  "summary": "Promotion Exclusion & Compatibility Matrix",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "PromotionExclusionCompatibilityMatrixView"
 },
 "listPromotionPriorityHierarchy": {
  "method": "GET",
  "path": "/promotion-priority-hierarchy",
  "contract": "promotions",
  "summary": "Promotion Priority & Hierarchy Manager",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "PromotionPriorityHierarchyManagerView"
 },
 "listStackingConflict": {
  "method": "GET",
  "path": "/stacking-conflict",
  "contract": "promotions",
  "summary": "Stacking & Conflict Command Center",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "StackingConflictCommandCenterView"
 },
 "setPromotionStackingRule": {
  "method": "PUT",
  "path": "/promotion-stacking-rule",
  "contract": "promotions",
  "summary": "Promotion Stacking Rule Builder",
  "permission": "PRICE_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "PromotionStackingRuleBuilderInput",
  "responds": "PromotionStackingRuleBuilderView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "BestOfferCustomerBenefitResolverView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Best Offer & Customer Benefit Resolver displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "useTheHighestRankedPromotion": {
    "type": "string",
    "description": "Use the highest-ranked promotion"
   },
   "favorAStrategicallySelectedCampaign": {
    "type": "string",
    "description": "Favor a strategically selected campaign"
   },
   "honorContractualCustomerSpecificPricingFirst": {
    "type": "string",
    "description": "Honor contractual/customer-specific pricing first"
   },
   "family15Aed": {
    "type": "string",
    "description": "FAMILY15 + AED"
   },
   "bank1011750": {
    "type": "string",
    "description": "BANK10 117.50"
   },
   "saving": {
    "type": "string",
    "description": "Saving (the pack shows AED 117.50)"
   },
   "bestAvailableOfferAppliedAutomatically": {
    "type": "string",
    "description": "Best available offer applied automatically"
   }
  }
 },
 "ConflictDetectionResolutionCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Conflict Detection & Resolution Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "sameProduct": {
    "type": "string",
    "description": "Same product"
   },
   "sameAudience": {
    "type": "string",
    "description": "Same audience"
   },
   "sameChannel": {
    "type": "string",
    "description": "Same channel"
   },
   "sameValidity": {
    "type": "string",
    "description": "Same validity"
   },
   "incompatiblePromotions": {
    "type": "string",
    "description": "Incompatible promotions"
   },
   "missingHierarchy": {
    "type": "string",
    "description": "Missing hierarchy"
   },
   "missingStackingRule": {
    "type": "string",
    "description": "Missing stacking rule"
   },
   "discountCapBreach": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Discount-cap breach"
   },
   "circularDependency": {
    "type": "string",
    "description": "Circular dependency"
   },
   "family20": {
    "type": "string",
    "description": "FAMILY20"
   },
   "vip15": {
    "type": "string",
    "description": "VIP15"
   },
   "summer25": {
    "type": "string",
    "description": "SUMMER25"
   },
   "bank10": {
    "type": "string",
    "description": "BANK10"
   },
   "automatic": {
    "type": "string",
    "description": "Automatic"
   },
   "ruleBased": {
    "type": "string",
    "description": "Rule-based"
   },
   "bestPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Best price"
   },
   "priority": {
    "type": "string",
    "description": "Priority"
   },
   "manualIntervention": {
    "type": "string",
    "description": "Manual intervention"
   }
  }
 },
 "ConflictSimulationAiOptimizationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Conflict Simulation & AI Optimization displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "customerSegment": {
    "type": "string",
    "description": "Customer segment"
   },
   "membership": {
    "type": "string",
    "description": "Membership"
   },
   "loyalty": {
    "type": "string",
    "description": "Loyalty"
   },
   "products": {
    "type": "string",
    "description": "Products"
   },
   "basket": {
    "type": "string",
    "description": "Basket"
   },
   "coupon": {
    "type": "string",
    "description": "Coupon"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "paymentMethod": {
    "type": "string",
    "description": "Payment method"
   },
   "dateTime": {
    "type": "string",
    "format": "date-time",
    "description": "Date/time"
   },
   "whoQualifies": {
    "type": "string",
    "description": "Who qualifies?"
   },
   "boards24PromotionMechanics": {
    "type": "string",
    "description": "Boards 2–4 — Promotion Mechanics"
   },
   "collectFinalAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Collect final amount"
   },
   "sameCentralizedEngine": {
    "type": "string",
    "description": "same centralized engine"
   },
   "paymentMethodOffers": {
    "type": "string",
    "description": "Payment-method offers"
   },
   "goldMember15": {
    "type": "number",
    "description": "Gold Member 15%"
   },
   "buy4Pay3": {
    "type": "string",
    "description": "Buy 4 Pay 3"
   },
   "summer20": {
    "type": "string",
    "description": "SUMMER20"
   },
   "bankAbc10": {
    "type": "number",
    "description": "Bank ABC 10%"
   },
   "gND": {
    "type": "string",
    "description": "g n d"
   },
   "member36": {
    "type": "number",
    "description": "Member 36% ✓"
   },
   "bogo29": {
    "type": "number",
    "description": "BOGO 29% ✓"
   },
   "coupon33": {
    "type": "number",
    "description": "Coupon 33% ✓"
   },
   "memberAed": {
    "type": "string",
    "description": "Member + AED"
   },
   "bogoBank24": {
    "type": "number",
    "description": "BOGO + Bank 24% ✓"
   },
   "bogoAed": {
    "type": "string",
    "description": "BOGO + AED"
   },
   "margin": {
    "type": "number",
    "description": "Margin (the pack shows 24%)"
   },
   "mutuallyExclusive": {
    "type": "string",
    "description": "mutually exclusive"
   },
   "estimatedProtectedMarginAed284kMonth": {
    "type": "number",
    "description": "Estimated protected margin: AED 284K/month"
   },
   "areCommercialLimitsRespected": {
    "type": "string",
    "description": "Are commercial limits respected?"
   },
   "calculateAuthoritativeFinalPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Calculate authoritative final price"
   },
   "marketingAdministrator": {
    "type": "string",
    "description": "Marketing Administrator"
   },
   "campaignManager": {
    "type": "string",
    "description": "Campaign Manager"
   },
   "commercialManager": {
    "type": "string",
    "description": "Commercial Manager"
   },
   "revenueManager": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue Manager"
   },
   "finance": {
    "type": "string",
    "description": "Finance"
   },
   "b2bManager": {
    "type": "string",
    "description": "B2B Manager"
   },
   "systemAdministrator": {
    "type": "string",
    "description": "System Administrator"
   },
   "approver": {
    "type": "string",
    "description": "Approver"
   },
   "auditor": {
    "type": "string",
    "description": "Auditor"
   }
  }
 },
 "DiscountCalculationApplicationSequenceView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Discount Calculation & Application Sequence displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "aed100Aed80": {
    "type": "string",
    "description": "AED 100 → AED 80"
   },
   "then10": {
    "type": "number",
    "description": "Then 10%"
   },
   "aed80Aed72": {
    "type": "string",
    "description": "AED 80 → AED 72"
   },
   "aed100Aed70": {
    "type": "string",
    "description": "AED 100 → AED 70"
   },
   "sequential": {
    "type": "string",
    "description": "Sequential"
   },
   "additivePercentage": {
    "type": "number",
    "description": "Additive percentage"
   },
   "fixedThenPercentage": {
    "type": "number",
    "description": "Fixed then percentage"
   },
   "percentageThenFixed": {
    "type": "number",
    "description": "Percentage then fixed"
   },
   "bestPriceOnly": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Best price only"
   },
   "highestValueDiscountOnly": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Highest-value discount only"
   },
   "lowestPriceResult": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Lowest-price result"
   },
   "priorityOrder": {
    "type": "string",
    "description": "Priority order"
   },
   "beforeTax": {
    "type": "string",
    "description": "Before tax"
   },
   "afterTax": {
    "type": "string",
    "description": "After tax"
   },
   "beforeFee": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Before fee"
   },
   "afterFee": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "After fee"
   },
   "productOnly": {
    "type": "string",
    "description": "Product only"
   },
   "transactionTotal": {
    "type": "string",
    "description": "Transaction total"
   }
  }
 },
 "DiscountCapMaximumBenefitControllerView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Discount Cap & Maximum Benefit Controller displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "maximumTotalDiscount": {
    "type": "number",
    "description": "Maximum total discount %"
   },
   "maximumTotalDiscountAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Maximum total discount amount"
   },
   "minimumTransactionValue": {
    "type": "string",
    "description": "Minimum transaction value"
   },
   "minimumProductPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Minimum product price"
   },
   "minimumMargin": {
    "type": "number",
    "description": "Minimum margin"
   },
   "maximumFreeItemValue": {
    "type": "string",
    "description": "Maximum free-item value"
   },
   "maximumPromotionalBenefit": {
    "type": "string",
    "description": "Maximum promotional benefit"
   },
   "maximumPromotionsPerBasket": {
    "type": "string",
    "description": "Maximum promotions per basket"
   },
   "membership15": {
    "type": "number",
    "description": "Membership 15%"
   },
   "bank10": {
    "type": "number",
    "description": "Bank 10%"
   },
   "coupon20": {
    "type": "number",
    "description": "Coupon 20%"
   },
   "potentialCombinedBenefit": {
    "type": "string",
    "description": "Potential combined benefit (the pack shows 45%)"
   },
   "configuredMaximum": {
    "type": "string",
    "description": "Configured maximum (the pack shows 30%)"
   },
   "tenant": {
    "type": "string",
    "description": "Tenant"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "category": {
    "type": "string",
    "description": "Category"
   },
   "campaign": {
    "type": "string",
    "description": "Campaign"
   },
   "customer": {
    "type": "string",
    "description": "Customer"
   },
   "partner": {
    "type": "string",
    "description": "Partner"
   },
   "transaction": {
    "type": "string",
    "description": "Transaction"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "reduceDiscount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Reduce discount"
   },
   "useBestPermittedCombination": {
    "type": "string",
    "description": "Use best permitted combination"
   },
   "requireApproval": {
    "type": "boolean",
    "description": "Require approval"
   }
  }
 },
 "PromotionDecisionTraceTransactionExplainerView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Promotion Decision Trace & Transaction Explainer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "family20": {
    "type": "string",
    "description": "FAMILY20 ✓"
   },
   "summer25": {
    "type": "string",
    "description": "SUMMER25 ✓"
   },
   "bank10": {
    "type": "string",
    "description": "BANK10 ✓"
   },
   "loyalty5": {
    "type": "string",
    "description": "LOYALTY5 ✓"
   },
   "family20Eligible": {
    "type": "string",
    "description": "FAMILY20 eligible"
   },
   "family20Retained": {
    "type": "string",
    "description": "FAMILY20 retained"
   },
   "bank10StackableWithFamily20": {
    "type": "string",
    "description": "BANK10 stackable with FAMILY20"
   },
   "bestPermittedCombinationCalculated": {
    "type": "string",
    "description": "Best permitted combination calculated"
   },
   "aed160": {
    "type": "string",
    "description": "−AED 160"
   },
   "aed64": {
    "type": "string",
    "description": "−AED 64"
   },
   "totalSaving": {
    "type": "integer",
    "description": "Total Saving (the pack shows AED 224 / 28%)"
   }
  }
 },
 "PromotionExclusionCompatibilityMatrixView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Promotion Exclusion & Compatibility Matrix displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "nHipTyKO": {
    "type": "string",
    "description": "n hip ty k O"
   },
   "allowed": {
    "type": "boolean",
    "description": "Allowed"
   },
   "notAllowed": {
    "type": "boolean",
    "description": "Not Allowed"
   },
   "conditional": {
    "type": "string",
    "description": "Conditional"
   },
   "priorityBased": {
    "type": "string",
    "description": "Priority Based"
   },
   "notConfigured": {
    "type": "string",
    "description": "Not Configured"
   },
   "applicableProducts": {
    "type": "integer",
    "description": "Applicable products"
   },
   "applicableVenues": {
    "type": "integer",
    "description": "Applicable venues"
   },
   "channels": {
    "type": "integer",
    "description": "Channels"
   },
   "customerSegments": {
    "type": "integer",
    "description": "Customer segments"
   },
   "rule": {
    "type": "string",
    "description": "Rule"
   },
   "priority": {
    "type": "string",
    "description": "Priority"
   },
   "effectiveDates": {
    "type": "integer",
    "description": "Effective dates"
   },
   "exceptions": {
    "type": "integer",
    "description": "Exceptions"
   }
  }
 },
 "PromotionPriorityHierarchyManagerView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Promotion Priority & Hierarchy Manager displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "promotionFamily": {
    "type": "string",
    "description": "Promotion family"
   },
   "promotion": {
    "type": "string",
    "description": "Promotion"
   },
   "priorityNumber": {
    "type": "string",
    "description": "Priority number"
   },
   "priorityGroup": {
    "type": "string",
    "description": "Priority group"
   },
   "effectiveDates": {
    "type": "string",
    "description": "Effective dates"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "customerSegment": {
    "type": "string",
    "description": "Customer segment"
   },
   "priority200": {
    "type": "string",
    "description": "Priority: 200"
   },
   "priority300": {
    "type": "string",
    "description": "Priority: 300"
   },
   "tenant": {
    "type": "string",
    "description": "Tenant"
   },
   "businessEntity": {
    "type": "string",
    "description": "Business entity"
   },
   "productCategory": {
    "type": "string",
    "description": "Product category"
   },
   "customerType": {
    "type": "string",
    "description": "Customer type"
   },
   "campaign": {
    "type": "string",
    "description": "Campaign"
   }
  }
 },
 "PromotionStackingRuleBuilderInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Promotion Stacking Rule Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "promotionAPromotionB": {
    "type": "string",
    "description": "Promotion A + Promotion B"
   },
   "onlyOnePromotionCanApply": {
    "type": "string",
    "description": "Only one promotion can apply"
   },
   "but": {
    "type": "string",
    "description": "but"
   },
   "couponDiscount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Coupon Discount"
   },
   "entireTransaction": {
    "type": "string",
    "description": "Entire transaction"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "productCategory": {
    "type": "string",
    "description": "Product category"
   },
   "individualTicket": {
    "type": "string",
    "description": "Individual ticket"
   },
   "bundleComponent": {
    "type": "string",
    "description": "Bundle component"
   },
   "customer": {
    "type": "string",
    "description": "Customer"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   }
  }
 },
 "PromotionStackingRuleBuilderView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Promotion Stacking Rule Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "promotionAPromotionB": {
    "type": "string",
    "description": "Promotion A + Promotion B"
   },
   "onlyOnePromotionCanApply": {
    "type": "string",
    "description": "Only one promotion can apply"
   },
   "but": {
    "type": "string",
    "description": "but"
   },
   "couponDiscount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Coupon Discount"
   },
   "entireTransaction": {
    "type": "string",
    "description": "Entire transaction"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "productCategory": {
    "type": "string",
    "description": "Product category"
   },
   "individualTicket": {
    "type": "string",
    "description": "Individual ticket"
   },
   "bundleComponent": {
    "type": "string",
    "description": "Bundle component"
   },
   "customer": {
    "type": "string",
    "description": "Customer"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   }
  }
 },
 "StackingConflictCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Stacking & Conflict Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "activePromotionRules": {
    "type": "integer",
    "description": "Active Promotion Rules"
   },
   "stackablePromotions": {
    "type": "integer",
    "description": "Stackable Promotions"
   },
   "exclusivePromotions": {
    "type": "integer",
    "description": "Exclusive Promotions"
   },
   "priorityRules": {
    "type": "integer",
    "description": "Priority Rules"
   },
   "conflictsDetected": {
    "type": "string",
    "description": "Conflicts Detected"
   },
   "criticalConflicts": {
    "type": "integer",
    "description": "Critical Conflicts"
   },
   "autoResolvedConflicts": {
    "type": "integer",
    "description": "Auto-Resolved Conflicts"
   },
   "transactionsWithMultipleOffers": {
    "type": "string",
    "description": "Transactions with Multiple Offers"
   },
   "averagePromotionsPerTransaction": {
    "type": "number",
    "description": "Average Promotions per Transaction"
   },
   "discountExposure": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Discount Exposure"
   },
   "preventedOverDiscount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Prevented Over-Discount"
   },
   "revenueProtected": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue Protected"
   },
   "promotionType": {
    "type": "string",
    "enum": [
     "vs",
     "couponVs",
     "couponVsCoupon",
     "bogoVsDiscount",
     "bundleVs",
     "membershipVs",
     "loyaltyVs",
     "bankOfferVs",
     "partnerOfferVs",
     "specialPriceVs"
    ],
    "description": "Vocabulary listed under Conflict Categories."
   },
   "information": {
    "type": "string",
    "description": "Information"
   },
   "warning": {
    "type": "string",
    "description": "Warning"
   },
   "high": {
    "type": "string",
    "description": "High"
   },
   "critical": {
    "type": "string",
    "description": "Critical"
   }
  }
 }
}
```
