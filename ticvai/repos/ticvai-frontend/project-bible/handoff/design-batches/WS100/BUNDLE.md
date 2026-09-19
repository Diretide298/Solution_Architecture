# WS100 — Subscription Licensing AI Self Service board 3

**10 screens · 0 operations · 0 schemas · 0 permissions**

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

- **Every control that can be refused must be gated.** 0 permissions apply here:
  ``. A control nobody can use must say so,
  not sit enabled and fail.
- **0 of these operations work offline**
  
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-389` | Commercial Rules Engine Overview | commandCentre | 0 | 0 | — |
| `ADM-390` | VSI Model Builder | configEditor | 0 | 0 | — |
| `ADM-391` | VSI Scoring & Tier Threshold Configuration | listDetail | 0 | 0 | — |
| `ADM-392` | Subscription Tier Configuration | listDetail | 0 | 0 | — |
| `ADM-393` | Tier Included Allowances | configEditor | 0 | 0 | — |
| `ADM-394` | Commercial & Licensing Model Configuration | configEditor | 0 | 0 | — |
| `ADM-395` | Billable Unit, Minimum Guarantee & Enforcement Rules | configEditor | 0 | 0 | — |
| `ADM-396` | Overage Pricing & Capacity Packs | configEditor | 0 | 0 | — |
| `ADM-397` | Commercial Model & Rule Simulation | listDetail | 0 | 0 | — |
| `ADM-398` | Rule Versioning, Approval & Publication | listDetail | 0 | 0 | — |

## Thin screens in this batch

**ADM-391, ADM-392, ADM-397, ADM-398 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-389",
  "name": "Commercial Rules Engine Overview",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "3",
   "number": "1",
   "page": 31
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/commercial-rules-engine-overview-adm-389",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/CommercialRulesEngineOverview.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-390",
    "ADM-391",
    "ADM-392",
    "ADM-393",
    "ADM-394",
    "ADM-395",
    "ADM-396",
    "ADM-397",
    "ADM-398"
   ],
   "transitions": [
    {
     "to": "ADM-002",
     "trigger": "Back to Platform Dashboard",
     "provenance": "structural — pack board 3 wiring, 11 September 2026",
     "back": true
    },
    {
     "to": "ADM-390",
     "trigger": "VSI Model Builder",
     "provenance": "structural — pack board 3 wiring, 11 September 2026"
    },
    {
     "to": "ADM-391",
     "trigger": "VSI Scoring & Tier Threshold Configuration",
     "provenance": "structural — pack board 3 wiring, 11 September 2026"
    },
    {
     "to": "ADM-392",
     "trigger": "Subscription Tier Configuration",
     "provenance": "structural — pack board 3 wiring, 11 September 2026"
    },
    {
     "to": "ADM-393",
     "trigger": "Tier Included Allowances",
     "provenance": "structural — pack board 3 wiring, 11 September 2026"
    },
    {
     "to": "ADM-394",
     "trigger": "Commercial & Licensing Model Configuration",
     "provenance": "structural — pack board 3 wiring, 11 September 2026"
    },
    {
     "to": "ADM-395",
     "trigger": "Billable Unit, Minimum Guarantee & Enforcement Rules",
     "provenance": "structural — pack board 3 wiring, 11 September 2026"
    },
    {
     "to": "ADM-396",
     "trigger": "Overage Pricing & Capacity Packs",
     "provenance": "structural — pack board 3 wiring, 11 September 2026"
    },
    {
     "to": "ADM-397",
     "trigger": "Commercial Model & Rule Simulation",
     "provenance": "structural — pack board 3 wiring, 11 September 2026"
    },
    {
     "to": "ADM-398",
     "trigger": "Rule Versioning, Approval & Publication",
     "provenance": "structural — pack board 3 wiring, 11 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide TICVAI administrators with the central configuration overview for all commercial and licensing rules.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Active Commercial Models",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 31 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Active Tiers",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 31 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Active VSI Model",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 31 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Customers by Commercial Model",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 31 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Average VSI",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 31 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Customers Near Threshold",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 31 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Customers Above Allowance",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 31 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Per-Ticket Contracts",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 31 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Minimum Guarantee Contracts",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 31 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Pending Rule Changes",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 31 §KPI Cards"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The commercial rules overview list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the commercial rules overview untouched.",
   "emptyFirstRun": "No commercial rules overview yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the commercial rules overview are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-389"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 31. 0 of 0 labels bound to a contract property; 10 of 31 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-390",
  "name": "VSI Model Builder",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "3",
   "number": "2",
   "page": 32
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/vsi-model-builder-adm-390",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/VsiModelBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-389"
   ],
   "exitTo": [
    "ADM-389"
   ],
   "transitions": [
    {
     "to": "ADM-389",
     "trigger": "Back to Commercial Rules Engine Overview",
     "provenance": "structural — pack board 3 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configuration Fields) and no display directory — it is settings, not a population",
  "purpose": "Configure how TICVAI determines the operational size and complexity of a customer. VSI remains important even where VSI does not determine customer pricing.",
  "gaps": [
   {
    "operation": null,
    "why": "**VSI Model Builder declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
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
       "label": "Factor Name",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 32 §Configuration Fields"
      },
      {
       "kind": "selectField",
       "label": "Weight",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 32 §Configuration Fields"
      },
      {
       "kind": "selectField",
       "label": "Data Source",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 32 §Configuration Fields"
      },
      {
       "kind": "selectField",
       "label": "Minimum Value",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 32 §Configuration Fields"
      },
      {
       "kind": "selectField",
       "label": "Maximum Value",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 32 §Configuration Fields"
      },
      {
       "kind": "selectField",
       "label": "Scoring Method",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 32 §Configuration Fields"
      },
      {
       "kind": "selectField",
       "label": "Mandatory/Optional",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 32 §Configuration Fields"
      },
      {
       "kind": "selectField",
       "label": "Venue Type Applicability",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 32 §Configuration Fields"
      },
      {
       "kind": "selectField",
       "label": "Market Applicability",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 32 §Configuration Fields"
      },
      {
       "kind": "selectField",
       "label": "Effective Date",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 32 §Configuration Fields"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The vsi model configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the vsi model untouched.",
   "emptyFirstRun": "No vsi model configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-390"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 32. 0 of 0 labels bound to a contract property; 10 of 27 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-391",
  "name": "VSI Scoring & Tier Threshold Configuration",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "3",
   "number": "3",
   "page": 33
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/vsi-scoring-tier-threshold-configuration-adm-391",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/VsiScoringTierThresholdConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-389"
   ],
   "exitTo": [
    "ADM-389"
   ],
   "transitions": [
    {
     "to": "ADM-389",
     "trigger": "Back to Commercial Rules Engine Overview",
     "provenance": "structural — pack board 3 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Translate actual customer characteristics into a standardized VSI score and recommended operational tier.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 33"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 33"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The vsi scoring tier list.",
   "error": "Could not load. Names which read failed and leaves the vsi scoring tier untouched.",
   "emptyFirstRun": "No vsi scoring tier yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the vsi scoring tier are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-391"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 33. 0 of 0 labels bound to a contract property; 0 of 1 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-392",
  "name": "Subscription Tier Configuration",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "3",
   "number": "4",
   "page": 34
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/subscription-tier-configuration-adm-392",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/SubscriptionTierConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-389"
   ],
   "exitTo": [
    "ADM-389"
   ],
   "transitions": [
    {
     "to": "ADM-389",
     "trigger": "Back to Commercial Rules Engine Overview",
     "provenance": "structural — pack board 3 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure TICVAI's standard subscription tiers for customers using tier-based commercial models.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 34"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 34"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The subscription tier list.",
   "error": "Could not load. Names which read failed and leaves the subscription tier untouched.",
   "emptyFirstRun": "No subscription tier yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the subscription tier are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-392"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 34. 0 of 0 labels bound to a contract property; 0 of 21 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-393",
  "name": "Tier Included Allowances",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "3",
   "number": "5",
   "page": 35
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/tier-included-allowances-adm-393",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/TierIncludedAllowances.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-389"
   ],
   "exitTo": [
    "ADM-389"
   ],
   "transitions": [
    {
     "to": "ADM-389",
     "trigger": "Back to Commercial Rules Engine Overview",
     "provenance": "structural — pack board 3 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configuration per Allowance) and no display directory — it is settings, not a population",
  "purpose": "Configure the resources included within each standard subscription tier.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Metric",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 35 §Configuration per Allowance"
      },
      {
       "kind": "selectField",
       "label": "Quantity",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 35 §Configuration per Allowance"
      },
      {
       "kind": "selectField",
       "label": "Measurement Period",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 35 §Configuration per Allowance"
      },
      {
       "kind": "selectField",
       "label": "Reset Period",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 35 §Configuration per Allowance"
      },
      {
       "kind": "selectField",
       "label": "Warning Threshold",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 35 §Configuration per Allowance"
      },
      {
       "kind": "selectField",
       "label": "Enforcement Type",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 35 §Configuration per Allowance"
      },
      {
       "kind": "selectField",
       "label": "Overage Allowed",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 35 §Configuration per Allowance"
      },
      {
       "kind": "selectField",
       "label": "Overage Rate",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 35 §Configuration per Allowance"
      },
      {
       "kind": "selectField",
       "label": "Additional Pack Allowed",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 35 §Configuration per Allowance"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The tier included allowances configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the tier included allowances untouched.",
   "emptyFirstRun": "No tier included allowances configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-393"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 35. 0 of 0 labels bound to a contract property; 9 of 13 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-394",
  "name": "Commercial & Licensing Model Configuration",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "3",
   "number": "6",
   "page": 36
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/commercial-licensing-model-configuration-adm-394",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/CommercialLicensingModelConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-389"
   ],
   "exitTo": [
    "ADM-389"
   ],
   "transitions": [
    {
     "to": "ADM-389",
     "trigger": "Back to Commercial Rules Engine Overview",
     "provenance": "structural — pack board 3 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Commercial Configuration Fields; Separately configure) and no display directory — it is settings, not a population",
  "purpose": "This is the major revised screen. Configure how TICVAI charges a customer independently from how TICVAI technically licenses the customer. A. Commercial Charging Model",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Commercial Model",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 36 §Commercial Configuration Fields"
      },
      {
       "kind": "selectField",
       "label": "Charging Unit",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 36 §Commercial Configuration Fields"
      },
      {
       "kind": "selectField",
       "label": "Rate",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 36 §Commercial Configuration Fields"
      },
      {
       "kind": "selectField",
       "label": "Currency",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 36 §Commercial Configuration Fields"
      },
      {
       "kind": "selectField",
       "label": "Billing Period",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 36 §Commercial Configuration Fields"
      },
      {
       "kind": "selectField",
       "label": "Included Volume",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 36 §Commercial Configuration Fields"
      },
      {
       "kind": "selectField",
       "label": "Minimum Guarantee",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 36 §Commercial Configuration Fields"
      },
      {
       "kind": "selectField",
       "label": "Guarantee Period",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 36 §Commercial Configuration Fields"
      },
      {
       "kind": "selectField",
       "label": "Percentage Rate",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 36 §Commercial Configuration Fields"
      },
      {
       "kind": "selectField",
       "label": "Fixed Base Fee",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 36 §Commercial Configuration Fields"
      },
      {
       "kind": "selectField",
       "label": "Module Charging",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 36 §Commercial Configuration Fields"
      },
      {
       "kind": "selectField",
       "label": "Effective Date",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 36 §Commercial Configuration Fields"
      },
      {
       "kind": "selectField",
       "label": "Expiry",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 36 §Commercial Configuration Fields"
      },
      {
       "kind": "selectField",
       "label": "Contract Applicability",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 36 §Commercial Configuration Fields"
      },
      {
       "kind": "selectField",
       "label": "POS Limit",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 36 §Separately configure"
      },
      {
       "kind": "selectField",
       "label": "Access Device Limit",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 36 §Separately configure"
      },
      {
       "kind": "selectField",
       "label": "User Limit",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 36 §Separately configure"
      },
      {
       "kind": "selectField",
       "label": "Venue Limit",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 36 §Separately configure"
      },
      {
       "kind": "selectField",
       "label": "API Limit",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 36 §Separately configure"
      },
      {
       "kind": "selectField",
       "label": "Storage Limit",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 36 §Separately configure"
      },
      {
       "kind": "selectField",
       "label": "Module Entitlements",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 36 §Separately configure"
      },
      {
       "kind": "selectField",
       "label": "Technical Capacity Profile",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 36 §Separately configure"
      },
      {
       "kind": "selectField",
       "label": "Hard/Soft/Approval Enforcement",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 36 §Separately configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The commercial licensing model configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the commercial licensing model untouched.",
   "emptyFirstRun": "No commercial licensing model configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-394"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 36. 0 of 0 labels bound to a contract property; 23 of 44 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-395",
  "name": "Billable Unit, Minimum Guarantee & Enforcement Rules",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "3",
   "number": "7",
   "page": 38
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/billable-unit-minimum-guarantee-enforcement-rules-adm-395",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/BillableUnitMinimumGuaranteeEnforcementRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-389"
   ],
   "exitTo": [
    "ADM-389"
   ],
   "transitions": [
    {
     "to": "ADM-389",
     "trigger": "Back to Commercial Rules Engine Overview",
     "provenance": "structural — pack board 3 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configuration should support; Commercial rule can specify; Configure) and no display directory — it is settings, not a population",
  "purpose": "Define exactly what TICVAI counts commercially and what happens when contractual or technical thresholds are reached.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Ticket Sold",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 38 §Configuration should support"
      },
      {
       "kind": "selectField",
       "label": "Ticket Issued",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 38 §Configuration should support"
      },
      {
       "kind": "selectField",
       "label": "Paid Ticket",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 38 §Configuration should support"
      },
      {
       "kind": "selectField",
       "label": "Transaction",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 38 §Configuration should support"
      },
      {
       "kind": "selectField",
       "label": "Admission/Redemption",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 38 §Configuration should support"
      },
      {
       "kind": "selectField",
       "label": "Gross Transaction Value",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 38 §Configuration should support"
      },
      {
       "kind": "selectField",
       "label": "Net Transaction Value",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 38 §Configuration should support"
      },
      {
       "kind": "selectField",
       "label": "Custom Billable Event",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 38 §Configuration should support"
      },
      {
       "kind": "selectField",
       "label": "50 billable tickets",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 38 §Commercial rule can specify"
      },
      {
       "kind": "selectField",
       "label": "1 billable transaction",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 38 §Commercial rule can specify"
      },
      {
       "kind": "selectField",
       "label": "Guarantee Amount",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 38 §Configure"
      },
      {
       "kind": "textField",
       "label": "Monthly / Quarterly / Annual",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 38 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Carry Forward Allowed",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 38 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Carry Forward Period",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 38 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Reconciliation Method",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 38 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Currency",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 38 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Effective Dates",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 38 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The billable unit minimum configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the billable unit minimum untouched.",
   "emptyFirstRun": "No billable unit minimum configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-395"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 38. 0 of 0 labels bound to a contract property; 17 of 30 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-396",
  "name": "Overage Pricing & Capacity Packs",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "3",
   "number": "8",
   "page": 39
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/overage-pricing-capacity-packs-adm-396",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/OveragePricingCapacityPacks.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-389"
   ],
   "exitTo": [
    "ADM-389"
   ],
   "transitions": [
    {
     "to": "ADM-389",
     "trigger": "Back to Commercial Rules Engine Overview",
     "provenance": "structural — pack board 3 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Pack Configuration) and no display directory — it is settings, not a population",
  "purpose": "Configure additional consumption pricing and purchasable capacity.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Pack Name",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 39 §Pack Configuration"
      },
      {
       "kind": "selectField",
       "label": "Resource",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 39 §Pack Configuration"
      },
      {
       "kind": "selectField",
       "label": "Quantity",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 39 §Pack Configuration"
      },
      {
       "kind": "selectField",
       "label": "Price",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 39 §Pack Configuration"
      },
      {
       "kind": "selectField",
       "label": "Recurring/One-Time",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 39 §Pack Configuration"
      },
      {
       "kind": "selectField",
       "label": "Validity",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 39 §Pack Configuration"
      },
      {
       "kind": "selectField",
       "label": "Applicable Tier",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 39 §Pack Configuration"
      },
      {
       "kind": "selectField",
       "label": "Applicable Commercial Model",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 39 §Pack Configuration"
      },
      {
       "kind": "selectField",
       "label": "Auto-Renew",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 39 §Pack Configuration"
      },
      {
       "kind": "selectField",
       "label": "Proration",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 39 §Pack Configuration"
      },
      {
       "kind": "selectField",
       "label": "Effective Dates",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 39 §Pack Configuration"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The overage pricing capacity configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the overage pricing capacity untouched.",
   "emptyFirstRun": "No overage pricing capacity configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-396"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 39. 0 of 0 labels bound to a contract property; 11 of 23 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-397",
  "name": "Commercial Model & Rule Simulation",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "3",
   "number": "9",
   "page": 40
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/commercial-model-rule-simulation-adm-397",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/CommercialModelRuleSimulation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-389"
   ],
   "exitTo": [
    "ADM-389"
   ],
   "transitions": [
    {
     "to": "ADM-389",
     "trigger": "Back to Commercial Rules Engine Overview",
     "provenance": "structural — pack board 3 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Allow TICVAI to test commercial models before applying them. This screen now becomes more powerful than the original Board 3 simulator.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 40 §Show"
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
       "label": "Every commercial model rule",
       "columns": [
        "Customer Annual Cost",
        "TICVAI Revenue",
        "Variable Revenue",
        "Minimum Guarantee",
        "Capacity",
        "Projected Overage",
        "Contract Value",
        "Commercial Risk"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 40 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected commercial model rule",
       "bindsTo": null,
       "columns": [
        "Customer Annual Cost",
        "TICVAI Revenue",
        "Variable Revenue",
        "Minimum Guarantee",
        "Capacity",
        "Projected Overage",
        "Contract Value",
        "Commercial Risk"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Customer Inputs”, “AED 145K/year”, “AED 150K/year”, “AED 120K/year”.",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 40 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The commercial model rule list.",
   "error": "Could not load. Names which read failed and leaves the commercial model rule untouched.",
   "emptyFirstRun": "No commercial model rule yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the commercial model rule are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "entryState": {
   "preloaded": [
    "Customer Annual Cost",
    "TICVAI Revenue",
    "Variable Revenue",
    "Minimum Guarantee",
    "Capacity",
    "Projected Overage"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-397"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 40. 0 of 8 labels bound to a contract property; 8 of 31 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-398",
  "name": "Rule Versioning, Approval & Publication",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "3",
   "number": "10",
   "page": 41
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/rule-versioning-approval-publication-adm-398",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/RuleVersioningApprovalPublication.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-389"
   ],
   "exitTo": [
    "ADM-389"
   ],
   "transitions": [
    {
     "to": "ADM-389",
     "trigger": "Back to Commercial Rules Engine Overview",
     "provenance": "structural — pack board 3 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Govern changes to all commercial, VSI, licensing, billable-unit and pricing rules.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 2 actions on this screen and the screen declares 0 operations.** Unserved: Revised Board 3 — Critical Architecture, 1. Operational Classification. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 41 §Actions"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 41"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 41"
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
       "label": "Revised Board 3 — Critical Architecture",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 41 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "1. Operational Classification",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 41 §Actions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The rule versioning approval list.",
   "error": "Could not load. Names which read failed and leaves the rule versioning approval untouched.",
   "emptyFirstRun": "No rule versioning approval yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the rule versioning approval are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-398"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 41. 0 of 0 labels bound to a contract property; 2 of 73 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
{}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{}
```
