# WS184 — Upsell,CrossSellEngine board 5

**10 screens · 7 operations · 11 schemas · 4 permissions**

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

- **Every control that can be refused must be gated.** 4 permissions apply here:
  `AI_USE, GUEST_VIEW, PRODUCT_CONFIGURE, PRODUCT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-679` | Personalization & NBO Command Center | commandCentre | 1 | 0 | — |
| `ADM-680` | Customer Recommendation Profile | listDetail | 3 | 0 | — |
| `ADM-681` | Customer Feature & Signal Configuration | listDetail | 1 | 0 | — |
| `ADM-682` | Propensity Model & Customer Intent Manager | listDetail | 1 | 0 | — |
| `ADM-683` | Next-Best-Offer Decision Studio | listDetail | 2 | 0 | — |
| `ADM-684` | Personalized Ranking & Decision Policy Builder | listDetail | 1 | 0 | — |
| `ADM-685` | Customer Preference, Fatigue & Suppression Intelligence | listDetail | 1 | 0 | — |
| `ADM-686` | Anonymous, Known & Identity-Transition Personalization.123 | listDetail | 1 | 0 | — |
| `ADM-687` | AI Explainability, Confidence & Model Governance | listDetail | 1 | 0 | — |
| `ADM-688` | Personalization Simulator & Next-Best-Offer Lab | configEditor | 1 | 0 | — |

## Thin screens in this batch

**ADM-680, ADM-681, ADM-682, ADM-683, ADM-685, ADM-686, ADM-687 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-679",
  "name": "Personalization & NBO Command Center",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Upsell,CrossSellEngine.pdf",
   "board": "5",
   "number": "1",
   "page": 124
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/personalization-nbo-command-center-adm-679",
   "component": "apps/ticvai-web/src/routes/commercial/PersonalizationNboCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-680",
    "ADM-681",
    "ADM-682",
    "ADM-683",
    "ADM-684",
    "ADM-685",
    "ADM-686",
    "ADM-687",
    "ADM-688"
   ],
   "transitions": [
    {
     "to": "ADM-002",
     "trigger": "Back to Platform Dashboard",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "ADM-680",
     "trigger": "Customer Recommendation Profile",
     "provenance": "structural — pack board 5 wiring, 19 September 2026"
    },
    {
     "to": "ADM-681",
     "trigger": "Customer Feature & Signal Configuration",
     "provenance": "structural — pack board 5 wiring, 19 September 2026"
    },
    {
     "to": "ADM-682",
     "trigger": "Propensity Model & Customer Intent Manager",
     "provenance": "structural — pack board 5 wiring, 19 September 2026"
    },
    {
     "to": "ADM-683",
     "trigger": "Next-Best-Offer Decision Studio",
     "provenance": "structural — pack board 5 wiring, 19 September 2026"
    },
    {
     "to": "ADM-684",
     "trigger": "Personalized Ranking & Decision Policy Builder",
     "provenance": "structural — pack board 5 wiring, 19 September 2026"
    },
    {
     "to": "ADM-685",
     "trigger": "Customer Preference, Fatigue & Suppression Intelligence",
     "provenance": "structural — pack board 5 wiring, 19 September 2026"
    },
    {
     "to": "ADM-686",
     "trigger": "Anonymous, Known & Identity-Transition Personalization.123",
     "provenance": "structural — pack board 5 wiring, 19 September 2026"
    },
    {
     "to": "ADM-687",
     "trigger": "AI Explainability, Confidence & Model Governance",
     "provenance": "structural — pack board 5 wiring, 19 September 2026"
    },
    {
     "to": "ADM-688",
     "trigger": "Personalization Simulator & Next-Best-Offer Lab",
     "provenance": "structural — pack board 5 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide centralized visibility into the operation and commercial impact of personalized recommendations.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Personalized Recommendations",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 124 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Personalized Customers/Sessions",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 124 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Next-Best-Offers Generated",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 124 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "NBO Acceptance Rate",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 124 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Personalized Conversion",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 124 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Incremental Revenue",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 124 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Personalized AOV Uplift",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 124 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Recommendation Relevance",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 124 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "AI Confidence",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 124 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Rule-Based Fallback Rate",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 124 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Suppressed Recommendations",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 124 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "AI Opportunities",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 124 §KPI Cards"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The personalization nbo list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the personalization nbo untouched.",
   "emptyFirstRun": "No personalization nbo yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the personalization nbo are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getRecommendationPerformance",
    "contract": "promotions",
    "purpose": "Personalisation performance",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-679",
   "workshopBoard": "wireframes/WS182 Upsell,CrossSellEngine Board 5.dc.html#adm-679"
  },
  "apisNote": "Regenerated 9 September 2026 from Upsell,CrossSellEngine.pdf page 124. 0 of 0 labels bound to a contract property; 12 of 32 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-680",
  "name": "Customer Recommendation Profile",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Upsell,CrossSellEngine.pdf",
   "board": "5",
   "number": "2",
   "page": 125
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/customer-recommendation-profile-adm-680",
   "component": "apps/ticvai-web/src/routes/commercial/CustomerRecommendationProfile.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-679"
   ],
   "exitTo": [
    "ADM-679"
   ],
   "transitions": [
    {
     "to": "ADM-679",
     "trigger": "Back to Personalization & NBO Command Center",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide the recommendation engine's commercially relevant customer context used for personalization. This should not become another CRM profile screen. CRM remains the authoritative source of customer information. Board 5 displays only the attributes relevant to recommendation decisioning.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 125"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 125"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "detailPanel",
       "derived": true,
       "impliedBy": "getGuestProfile",
       "notes": "One record, read-only."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "explainRecommendation",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "explainRecommendation"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The customer recommendation profile list.",
   "error": "Could not load. Names which read failed and leaves the customer recommendation profile untouched.",
   "emptyFirstRun": "No customer recommendation profile yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the customer recommendation profile are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getGuestProfile",
    "contract": "marketing-crm",
    "purpose": "The guest behind the recommendation",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "getCustomerRecommendationProfile",
    "contract": "ai",
    "purpose": "What the engine knows about a customer",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-680",
   "workshopBoard": "wireframes/WS182 Upsell,CrossSellEngine Board 5.dc.html#adm-680"
  },
  "apisNote": "Regenerated 9 September 2026 from Upsell,CrossSellEngine.pdf page 125. 0 of 0 labels bound to a contract property; 0 of 27 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "subjectId",
     "from": "navigation"
    },
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
  "id": "ADM-681",
  "name": "Customer Feature & Signal Configuration",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Upsell,CrossSellEngine.pdf",
   "board": "5",
   "number": "3",
   "page": 127
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/customer-feature-signal-configuration-adm-681",
   "component": "apps/ticvai-web/src/routes/commercial/CustomerFeatureSignalConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-679"
   ],
   "exitTo": [
    "ADM-679"
   ],
   "transitions": [
    {
     "to": "ADM-679",
     "trigger": "Back to Personalization & NBO Command Center",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Control which approved data signals the AI may use when calculating personalized recommendations. This is critical for governance and explainability.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 127"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 127"
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
   "loading": "The customer feature signal list.",
   "error": "Could not load. Names which read failed and leaves the customer feature signal untouched.",
   "emptyFirstRun": "No customer feature signal yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the customer feature signal are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "updateRecommendationStrategy",
    "contract": "promotions",
    "purpose": "Which signals count",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listRecommendationStrategies"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-681",
   "workshopBoard": "wireframes/WS182 Upsell,CrossSellEngine Board 5.dc.html#adm-681"
  },
  "apisNote": "Regenerated 9 September 2026 from Upsell,CrossSellEngine.pdf page 127. 0 of 0 labels bound to a contract property; 0 of 36 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-682",
  "name": "Propensity Model & Customer Intent Manager",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Upsell,CrossSellEngine.pdf",
   "board": "5",
   "number": "4",
   "page": 129
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/propensity-model-customer-intent-manager-adm-682",
   "component": "apps/ticvai-web/src/routes/commercial/PropensityModelCustomerIntentManager.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-679"
   ],
   "exitTo": [
    "ADM-679"
   ],
   "transitions": [
    {
     "to": "ADM-679",
     "trigger": "Back to Personalization & NBO Command Center",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Calculate the likelihood that a guest will take specific commercial actions.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 129 §Show"
   },
   {
    "operation": null,
    "why": "**Propensity Model & Customer Intent Manager declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
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
       "label": "Every propensity model customer",
       "columns": [
        "Model name",
        "Model version",
        "Last updated",
        "Training period",
        "Confidence",
        "Population",
        "Data freshness"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 129 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected propensity model customer",
       "bindsTo": null,
       "columns": [
        "Model name",
        "Model version",
        "Last updated",
        "Training period",
        "Confidence",
        "Population",
        "Data freshness"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Membershi”, “Family”, “Meal”, “Propensity Bands”, “Important”.",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 129 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The propensity model customer list.",
   "error": "Could not load. Names which read failed and leaves the propensity model customer untouched.",
   "emptyFirstRun": "No propensity model customer yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the propensity model customer are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getRecommendationPerformance",
    "contract": "promotions",
    "purpose": "Propensity and intent",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Model name",
    "Model version",
    "Last updated",
    "Training period",
    "Confidence",
    "Population"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-682",
   "workshopBoard": "wireframes/WS182 Upsell,CrossSellEngine Board 5.dc.html#adm-682"
  },
  "apisNote": "Regenerated 9 September 2026 from Upsell,CrossSellEngine.pdf page 129. 0 of 7 labels bound to a contract property; 7 of 30 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-683",
  "name": "Next-Best-Offer Decision Studio",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Upsell,CrossSellEngine.pdf",
   "board": "5",
   "number": "5",
   "page": 131
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/next-best-offer-decision-studio-adm-683",
   "component": "apps/ticvai-web/src/routes/commercial/NextBestOfferDecisionStudio.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-679"
   ],
   "exitTo": [
    "ADM-679"
   ],
   "transitions": [
    {
     "to": "ADM-679",
     "trigger": "Back to Personalization & NBO Command Center",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "This is the core screen of Board 5. Combine all eligible candidates and determine the strongest personalized recommendation.",
  "gaps": [
   {
    "operation": null,
    "why": "**Next-Best-Offer Decision Studio declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 131"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 131"
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
   "loading": "The next-best-offer decision list.",
   "error": "Could not load. Names which read failed and leaves the next-best-offer decision untouched.",
   "emptyFirstRun": "No next-best-offer decision yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the next-best-offer decision are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "updateRecommendationStrategy",
    "contract": "promotions",
    "purpose": "Next-best-offer policy",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listRecommendationStrategies"
    ]
   },
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-683",
   "workshopBoard": "wireframes/WS182 Upsell,CrossSellEngine Board 5.dc.html#adm-683"
  },
  "apisNote": "Regenerated 9 September 2026 from Upsell,CrossSellEngine.pdf page 131. 0 of 0 labels bound to a contract property; 0 of 19 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "strategyId",
     "from": "navigation"
    },
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
  "id": "ADM-684",
  "name": "Personalized Ranking & Decision Policy Builder",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Upsell,CrossSellEngine.pdf",
   "board": "5",
   "number": "6",
   "page": 132
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/personalized-ranking-decision-policy-builder-adm-684",
   "component": "apps/ticvai-web/src/routes/commercial/PersonalizedRankingDecisionPolicyBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-679"
   ],
   "exitTo": [
    "ADM-679"
   ],
   "transitions": [
    {
     "to": "ADM-679",
     "trigger": "Back to Personalization & NBO Command Center",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure how TICVAI converts AI scores and commercial factors into the final recommendation ranking.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 10 actions on this screen and the screen declares 0 operations.** Unserved: Customer propensity, Product affinity, Historical acceptance, Revenue, Incremental revenue, Capacity, Inventory, Commercial priority …. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 132 §Support"
   },
   {
    "operation": null,
    "why": "**Personalized Ranking & Decision Policy Builder declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 132"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 132"
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
       "label": "Customer propensity",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 132 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Product affinity",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 132 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Historical acceptance",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 132 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Revenue",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 132 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Incremental revenue",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 132 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Capacity",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 132 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Inventory",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 132 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Commercial priority",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 132 §Support"
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
   "loading": "The personalized ranking decision list.",
   "error": "Could not load. Names which read failed and leaves the personalized ranking decision untouched.",
   "emptyFirstRun": "No personalized ranking decision yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the personalized ranking decision are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "updateRecommendationStrategy",
    "contract": "promotions",
    "purpose": "Ranking and decision policy",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listRecommendationStrategies"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-684",
   "workshopBoard": "wireframes/WS182 Upsell,CrossSellEngine Board 5.dc.html#adm-684"
  },
  "apisNote": "Regenerated 9 September 2026 from Upsell,CrossSellEngine.pdf page 132. 0 of 0 labels bound to a contract property; 10 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-685",
  "name": "Customer Preference, Fatigue & Suppression Intelligence",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Upsell,CrossSellEngine.pdf",
   "board": "5",
   "number": "7",
   "page": 134
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/customer-preference-fatigue-suppression-intelligence-adm-685",
   "component": "apps/ticvai-web/src/routes/commercial/CustomerPreferenceFatigueSuppressionIntelligence.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-679"
   ],
   "exitTo": [
    "ADM-679"
   ],
   "transitions": [
    {
     "to": "ADM-679",
     "trigger": "Back to Personalization & NBO Command Center",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Track) and no metric row",
  "purpose": "Prevent personalization from becoming repetitive or intrusive. Board 4 provides general journey frequency controls. Board 5 adds customer-specific behavioral suppression.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 134 §Track"
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
       "label": "Every customer preference fatigue",
       "columns": [
        "Repeated declines",
        "Repeated ignores",
        "Recent purchase",
        "Previous acceptance",
        "Category preference",
        "Recommendation fatigue",
        "Channel response"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 134 §Track"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected customer preference fatigue",
       "bindsTo": null,
       "columns": [
        "Repeated declines",
        "Repeated ignores",
        "Recent purchase",
        "Previous acceptance",
        "Category preference",
        "Recommendation fatigue",
        "Channel response"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Photo Package”, “System action”, “Customer consistently accepts”, “Explicit Preferences”.",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 134 §Track"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The customer preference fatigue list.",
   "error": "Could not load. Names which read failed and leaves the customer preference fatigue untouched.",
   "emptyFirstRun": "No customer preference fatigue yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the customer preference fatigue are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setRecommendationSuppression",
    "contract": "promotions",
    "purpose": "Preference, fatigue, suppression",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listRecommendationStrategies"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "Repeated declines",
    "Repeated ignores",
    "Recent purchase",
    "Previous acceptance",
    "Category preference",
    "Recommendation fatigue"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-685",
   "workshopBoard": "wireframes/WS182 Upsell,CrossSellEngine Board 5.dc.html#adm-685"
  },
  "apisNote": "Regenerated 9 September 2026 from Upsell,CrossSellEngine.pdf page 134. 0 of 7 labels bound to a contract property; 13 of 27 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-686",
  "name": "Anonymous, Known & Identity-Transition Personalization.123",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Upsell,CrossSellEngine.pdf",
   "board": "5",
   "number": "8",
   "page": 135
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/anonymous-known-identity-transition-personalization-123-adm-686",
   "component": "apps/ticvai-web/src/routes/commercial/AnonymousKnownIdentityTransitionPersonalization1.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-679"
   ],
   "exitTo": [
    "ADM-679"
   ],
   "transitions": [
    {
     "to": "ADM-679",
     "trigger": "Back to Personalization & NBO Command Center",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow useful recommendations even when TICVAI does not yet know the customer's identity.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 135"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 135"
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
       "impliedBy": "explainRecommendation",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "explainRecommendation"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The anonymous known identity-transition list.",
   "error": "Could not load. Names which read failed and leaves the anonymous known identity-transition untouched.",
   "emptyFirstRun": "No anonymous known identity-transition yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the anonymous known identity-transition are still there. Names the active filter and offers to clear it.",
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-686",
   "workshopBoard": "wireframes/WS182 Upsell,CrossSellEngine Board 5.dc.html#adm-686"
  },
  "apisNote": "Regenerated 9 September 2026 from Upsell,CrossSellEngine.pdf page 135. 0 of 0 labels bound to a contract property; 0 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-687",
  "name": "AI Explainability, Confidence & Model Governance",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Upsell,CrossSellEngine.pdf",
   "board": "5",
   "number": "9",
   "page": 137
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/ai-explainability-confidence-model-governance-adm-687",
   "component": "apps/ticvai-web/src/routes/commercial/AiExplainabilityConfidenceModelGovernance.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-679"
   ],
   "exitTo": [
    "ADM-679"
   ],
   "transitions": [
    {
     "to": "ADM-679",
     "trigger": "Back to Personalization & NBO Command Center",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Make personalized AI decisions understandable and governable.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Upsell,CrossSellEngine.pdf, page 137 §Display"
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
       "label": "Every explainability confidence model",
       "columns": [
        "Model",
        "Version",
        "Deployment date",
        "Owner",
        "Status",
        "Confidence threshold",
        "Fallback policy"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 137 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected explainability confidence model",
       "bindsTo": null,
       "columns": [
        "Model",
        "Version",
        "Deployment date",
        "Owner",
        "Status",
        "Confidence threshold",
        "Fallback policy"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Annual Family Membership”, “Confidence”, “Show ranked contributors”.",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 137 §Display"
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
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** Disable model, Change approved threshold, Switch to rules, Suspend recommendation category. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 137 §Authorized users may"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The explainability confidence model list.",
   "error": "Could not load. Names which read failed and leaves the explainability confidence model untouched.",
   "emptyFirstRun": "No explainability confidence model yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the explainability confidence model are still there. Names the active filter and offers to clear it.",
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
  "entryState": {
   "preloaded": [
    "Model",
    "Version",
    "Deployment date",
    "Owner",
    "Status",
    "Confidence threshold"
   ],
   "params": [
    {
     "name": "decisionId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-687",
   "workshopBoard": "wireframes/WS182 Upsell,CrossSellEngine Board 5.dc.html#adm-687"
  },
  "apisNote": "Regenerated 9 September 2026 from Upsell,CrossSellEngine.pdf page 137. 0 of 7 labels bound to a contract property; 11 of 33 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-688",
  "name": "Personalization Simulator & Next-Best-Offer Lab",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Upsell,CrossSellEngine.pdf",
   "board": "5",
   "number": "10",
   "page": 139
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/personalization-simulator-next-best-offer-lab-adm-688",
   "component": "apps/ticvai-web/src/routes/commercial/PersonalizationSimulatorNextBestOfferLab.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-679"
   ],
   "exitTo": [
    "ADM-679"
   ],
   "transitions": [
    {
     "to": "ADM-679",
     "trigger": "Back to Personalization & NBO Command Center",
     "provenance": "structural — pack board 5 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Select) and no display directory — it is settings, not a population",
  "purpose": "Allow administrators to simulate how TICVAI would personalize recommendations for different customers before deploying changes.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "textField",
       "label": "Customer or synthetic profile",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 139 §Select"
      },
      {
       "kind": "selectField",
       "label": "Segment",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 139 §Select"
      },
      {
       "kind": "selectField",
       "label": "Membership",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 139 §Select"
      },
      {
       "kind": "selectField",
       "label": "Loyalty",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 139 §Select"
      },
      {
       "kind": "selectField",
       "label": "Historical spend",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 139 §Select"
      },
      {
       "kind": "selectField",
       "label": "Visit frequency",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 139 §Select"
      },
      {
       "kind": "selectField",
       "label": "Purchase history",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 139 §Select"
      },
      {
       "kind": "selectField",
       "label": "Current basket",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 139 §Select"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 139 §Select"
      },
      {
       "kind": "selectField",
       "label": "Channel",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 139 §Select"
      },
      {
       "kind": "selectField",
       "label": "Journey stage",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 139 §Select"
      },
      {
       "kind": "selectField",
       "label": "Date/time",
       "provenance": "pack Upsell,CrossSellEngine.pdf, page 139 §Select"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The personalization simulator next-best-offer configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the personalization simulator next-best-offer untouched.",
   "emptyFirstRun": "No personalization simulator next-best-offer configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "simulateRecommendationStrategy",
    "contract": "promotions",
    "purpose": "The NBO lab",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-688",
   "workshopBoard": "wireframes/WS182 Upsell,CrossSellEngine Board 5.dc.html#adm-688"
  },
  "apisNote": "Regenerated 9 September 2026 from Upsell,CrossSellEngine.pdf page 139. 0 of 0 labels bound to a contract property; 12 of 15 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "getCustomerRecommendationProfile": {
  "method": "GET",
  "path": "/recommendations/customers/{subjectId}/profile",
  "contract": "ai",
  "summary": "What the engine knows about a customer",
  "permission": "AI_USE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AiCustomerRecommendationProfile"
 },
 "getGuestProfile": {
  "method": "GET",
  "path": "/guests/{subjectId}",
  "contract": "marketing-crm",
  "summary": "Read a guest profile",
  "permission": "GUEST_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "GuestProfileDetail"
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
 "AiCustomerRecommendationProfile": {
  "type": "object",
  "x-ticvai-persistence": "none — assembled from features, ai.rec_decline and ai.rec_event",
  "description": "What the engine knows about one customer for recommendations (ADM-680): segment, affinities, declines, consent flags and recent decisions. Sensitive data never becomes a feature (AIR-185).",
  "required": [
   "subjectId"
  ],
  "properties": {
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "segment": {
    "type": "string",
    "nullable": true
   },
   "personalisationAllowed": {
    "type": "boolean"
   },
   "affinities": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "categoryRef": {
       "type": "string"
      },
      "strength": {
       "type": "number"
      }
     }
    }
   },
   "declines": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/AiRecommendationDecline"
    }
   },
   "recentDecisions": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/AiRecommendationDecision"
    }
   },
   "featureFreshAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "AiRecommendationDecision": {
  "type": "object",
  "x-ticvai-persistence": "ai.rec_decision",
  "description": "**One compact recommendation decision** (design 2.2 A, 3.1 Recommendation): funnel counts, exclusion reasons (AIR-032), versions, scores and the final set. Written after the response, never before it. **AI log database** (design 2.4): append-only, partitioned by month, one Postgres database per tenant on the regional AI log server. The table name stays `ai.<table>`; which server holds it is a deployment matter, not a contract one.",
  "required": [
   "placement",
   "mode",
   "items"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "placement": {
    "type": "string",
    "enum": [
     "productPage",
     "cart",
     "checkout",
     "postPurchase",
     "preVisit",
     "inVenue",
     "posBasket",
     "kioskBasket",
     "fnbMenu",
     "retailBasket",
     "seatUpgrade",
     "membership",
     "email",
     "homepage",
     "loyalty"
    ]
   },
   "channel": {
    "type": "string"
   },
   "cartId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "sessionRef": {
    "type": "string",
    "nullable": true
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "mode": {
    "type": "string",
    "enum": [
     "personalised",
     "contextual",
     "rulesOnly",
     "fallback"
    ],
    "description": "Personalised only where context is sufficient and consent allows (AIR-114, AIR-187)."
   },
   "strategyRef": {
    "type": "string",
    "nullable": true
   },
   "strategyVersion": {
    "type": "integer",
    "nullable": true
   },
   "modelVersion": {
    "type": "string",
    "nullable": true
   },
   "featureSetVersion": {
    "type": "string",
    "nullable": true
   },
   "funnel": {
    "type": "object",
    "additionalProperties": true,
    "description": "Candidate counts at each stage: generated, eligible, ranked, returned."
   },
   "exclusions": {
    "type": "object",
    "additionalProperties": true,
    "description": "Removed candidates by reason: unsaleable, capacity, inventory, owned, inCart, conflict, declined, frequencyCap, guardrail."
   },
   "items": {
    "$ref": "#/components/schemas/AiRecommendationItemList"
   },
   "experimentArm": {
    "type": "string",
    "nullable": true
   },
   "latencyMs": {
    "type": "integer"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "description": "Decision TTL: 30 s where capacity-sensitive, 30 min otherwise (AIR-208)."
   },
   "decidedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."
   }
  }
 },
 "AiRecommendationDecline": {
  "type": "object",
  "x-ticvai-persistence": "ai.rec_decline",
  "description": "**The cross-channel decline store** (AIR-065). Keyed on customer or session, so a declined offer is not repeated at the kiosk after the app. **Only an explicit decline counts; \"ignored\" is not a decline** (decided 29 September, decision 7).",
  "required": [
   "declinedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "sessionRef": {
    "type": "string",
    "nullable": true
   },
   "productId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The declined product. Null where a non-product item was declined (`itemRef`)."
   },
   "itemRef": {
    "type": "string",
    "nullable": true,
    "description": "For a declined `offer`, `reward` or `challenge` item (29 September, build): its `promotionId`, `couponRef`, `rewardId` or `challengeId`, prefixed with the kind (`offer:`, `reward:`, `challenge:`), resolved from the event's `trackingId`."
   },
   "placement": {
    "type": "string",
    "enum": [
     "productPage",
     "cart",
     "checkout",
     "postPurchase",
     "preVisit",
     "inVenue",
     "posBasket",
     "kioskBasket",
     "fnbMenu",
     "retailBasket",
     "seatUpgrade",
     "membership",
     "email",
     "homepage",
     "loyalty"
    ]
   },
   "channel": {
    "type": "string",
    "nullable": true
   },
   "declinedAt": {
    "type": "string",
    "format": "date-time"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."
   }
  }
 },
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
 "ConsentState": {
  "x-ticvai-persistence": "none — projection over consent_record",
  "type": "object",
  "required": [
   "subjectId",
   "purposes"
  ],
  "properties": {
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "purposes": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "purpose",
      "decision",
      "requiresRenewal"
     ],
     "properties": {
      "purpose": {
       "$ref": "#/components/schemas/ConsentPurpose"
      },
      "decision": {
       "$ref": "#/components/schemas/ConsentDecision"
      },
      "channels": {
       "type": "array",
       "items": {
        "$ref": "#/components/schemas/MessageChannel"
       }
      },
      "noticeVersion": {
       "type": "string",
       "nullable": true
      },
      "requiresRenewal": {
       "type": "boolean",
       "description": "True where the notice has been superseded since consent was given."
      },
      "decidedAt": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      }
     }
    }
   }
  }
 },
 "GuestProfile": {
  "x-ticvai-persistence": "marketing.guest_profile",
  "type": "object",
  "required": [
   "subjectId",
   "isActive"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "description": "Opaque reference. Personal data lives in the separately erasable store, which is what makes erasure possible against an append-only ledger.\n"
   },
   "displayName": {
    "type": "string",
    "nullable": true
   },
   "email": {
    "type": "string",
    "nullable": true
   },
   "phone": {
    "type": "string",
    "nullable": true
   },
   "preferredLanguage": {
    "type": "string",
    "nullable": true
   },
   "preferredChannel": {
    "$ref": "#/components/schemas/MessageChannel"
   },
   "guestLinkId": {
    "type": "string",
    "nullable": true,
    "description": "Present where the guest is linked across cells. Marketing acts locally."
   },
   "tags": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "engagementScore": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "maximum": 100,
    "description": "22.2.20 and 22.2.21. **`lifetimeValue` and `visitCount` existed, so value was a stored figure and engagement was not.** They are different questions: a guest who spent a lot once and a guest who visits monthly have the same LTV and need opposite treatment.\n**Recency, frequency and breadth, not spend** — spend is already `lifetimeValue`, and folding it in here would make one number twice.\n"
   },
   "engagementTier": {
    "type": "string",
    "nullable": true,
    "enum": [
     "new",
     "active",
     "occasional",
     "lapsing",
     "lapsed",
     "dormant"
    ],
    "description": "5.3.19. **Automatic classification, computed rather than assigned.** `lapsing` is the tier the whole field exists for — **a guest who has not been for a while and still might is the only one marketing can change**, and lumping them with `lapsed` wastes the window.\n"
   },
   "lifetimeValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "visitCount": {
    "type": "integer"
   },
   "lastVisitAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "isActive": {
    "type": "boolean"
   },
   "mergedIntoSubjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "**Set on the absorbed profile by `mergeGuestProfiles` and `mergeGuests`**, which retain it as a redirect rather than deleting it. A read that lands here follows it; a second merge of a profile that has one is refused as `alreadyMerged`.\n"
   },
   "mergedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   }
  }
 },
 "GuestProfileDetail": {
  "x-ticvai-persistence": "marketing.guest_profile",
  "allOf": [
   {
    "$ref": "#/components/schemas/GuestProfile"
   },
   {
    "type": "object",
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid",
      "readOnly": true,
      "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
     },
     "consents": {
      "$ref": "#/components/schemas/ConsentState"
     },
     "loyalty": {
      "$ref": "#/components/schemas/LoyaltyPosition"
     },
     "openCaseCount": {
      "type": "integer"
     },
     "recentOrderIds": {
      "type": "array",
      "items": {
       "type": "string"
      }
     },
     "membershipIds": {
      "type": "array",
      "items": {
       "type": "string",
       "format": "uuid"
      }
     },
     "notes": {
      "type": "string",
      "nullable": true
     }
    }
   }
  ]
 },
 "LoyaltyPosition": {
  "x-ticvai-persistence": "marketing.loyalty_position",
  "type": "object",
  "required": [
   "subjectId",
   "programmeId",
   "pointsBalance",
   "tierCode"
  ],
  "properties": {
   "leaderboardNickname": {
    "type": "string",
    "nullable": true,
    "maxLength": 24,
    "description": "BL-173. **The name shown on a leaderboard, chosen by the guest.** Offered whenever they reach the board and changeable afterwards; `setLeaderboardNickname` is the only thing that writes it.\n**Null means the guest has not chosen one yet, and the board shows a generated `Player-4821` in its place** — never `pii.subject.display_name`, which would disclose silently on the day a guest first placed and is the case this field exists to prevent.\n**The generated name is computed at read time and not stored here.** Writing it would make *\"has this guest chosen a name\"* unanswerable, and that flag is what the prompt-on-reaching-the-board depends on.\n"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "programmeId": {
    "type": "string",
    "format": "uuid"
   },
   "pointsBalance": {
    "type": "integer"
   },
   "lifetimePoints": {
    "type": "integer"
   },
   "tierId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**The tier this row's `tierCode` and `tierName` are a copy of.** Added 20 September with `marketing.programme_tier`: the two strings were a cache of something that did not exist, and a cache with no source cannot be rebuilt or audited.\n"
   },
   "tierCode": {
    "type": "string"
   },
   "tierName": {
    "type": "string"
   },
   "pointsToNextTier": {
    "type": "integer",
    "nullable": true
   },
   "nextExpiryPoints": {
    "type": "integer",
    "nullable": true
   },
   "nextExpiryAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
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
