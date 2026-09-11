# WS98 — Subscription Licensing AI Self Service board 1

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
| `ADM-369` | Commercial Command Center | commandCentre | 0 | 0 | — |
| `ADM-370` | Customer Subscription & Commercial Portfolio | listDetail | 0 | 0 | — |
| `ADM-371` | Customer Commercial 360° | listDetail | 0 | 0 | — |
| `ADM-372` | Operational Profile, VSI & Commercial Model Intelligence | commandCentre | 0 | 0 | — |
| `ADM-373` | Revenue & Commercial Model Analytics | commandCentre | 0 | 0 | — |
| `ADM-374` | Trial & Conversion Monitor | commandCentre | 0 | 0 | — |
| `ADM-375` | Renewal & Retention Center | commandCentre | 0 | 0 | — |
| `ADM-376` | Commercial Optimization & Expansion Opportunities | commandCentre | 0 | 0 | — |
| `ADM-377` | Subscription Exceptions & Commercial Alerts | listDetail | 0 | 0 | — |
| `ADM-378` | Executive AI Commercial Intelligence | commandCentre | 0 | 0 | — |

## Thin screens in this batch

**ADM-371, ADM-377 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-369",
  "name": "Commercial Command Center",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "1",
   "number": "1",
   "page": 6
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/commercial-command-center-adm-369",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/CommercialCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-370",
    "ADM-371",
    "ADM-372",
    "ADM-373",
    "ADM-374",
    "ADM-375",
    "ADM-376",
    "ADM-377",
    "ADM-378"
   ],
   "transitions": [
    {
     "to": "ADM-002",
     "trigger": "Back to Platform Dashboard",
     "provenance": "structural — pack board 1 wiring, 11 September 2026",
     "back": true
    },
    {
     "to": "ADM-370",
     "trigger": "Customer Subscription & Commercial Portfolio",
     "provenance": "structural — pack board 1 wiring, 11 September 2026"
    },
    {
     "to": "ADM-371",
     "trigger": "Customer Commercial 360°",
     "provenance": "structural — pack board 1 wiring, 11 September 2026"
    },
    {
     "to": "ADM-372",
     "trigger": "Operational Profile, VSI & Commercial Model Intelligence",
     "provenance": "structural — pack board 1 wiring, 11 September 2026"
    },
    {
     "to": "ADM-373",
     "trigger": "Revenue & Commercial Model Analytics",
     "provenance": "structural — pack board 1 wiring, 11 September 2026"
    },
    {
     "to": "ADM-374",
     "trigger": "Trial & Conversion Monitor",
     "provenance": "structural — pack board 1 wiring, 11 September 2026"
    },
    {
     "to": "ADM-375",
     "trigger": "Renewal & Retention Center",
     "provenance": "structural — pack board 1 wiring, 11 September 2026"
    },
    {
     "to": "ADM-376",
     "trigger": "Commercial Optimization & Expansion Opportunities",
     "provenance": "structural — pack board 1 wiring, 11 September 2026"
    },
    {
     "to": "ADM-377",
     "trigger": "Subscription Exceptions & Commercial Alerts",
     "provenance": "structural — pack board 1 wiring, 11 September 2026"
    },
    {
     "to": "ADM-378",
     "trigger": "Executive AI Commercial Intelligence",
     "provenance": "structural — pack board 1 wiring, 11 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Primary KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide TICVAI management with a real-time executive overview of the entire subscription and commercial business.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Total Active Customers",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 6 §Primary KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Active Subscriptions",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 6 §Primary KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Active Trials",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 6 §Primary KPIs"
      },
      {
       "kind": "metricTile",
       "label": "MRR / Monthly Equivalent Revenue",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 6 §Primary KPIs"
      },
      {
       "kind": "metricTile",
       "label": "ARR / Annualized Contract Value",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 6 §Primary KPIs"
      },
      {
       "kind": "metricTile",
       "label": "New Revenue",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 6 §Primary KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Expansion Revenue",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 6 §Primary KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Contraction Revenue",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 6 §Primary KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Churned Revenue",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 6 §Primary KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Renewal Rate",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 6 §Primary KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Trial-to-Paid Conversion",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 6 §Primary KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Average Revenue per Customer",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 6 §Primary KPIs"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The commercial list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the commercial untouched.",
   "emptyFirstRun": "No commercial yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the commercial are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-369"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 6. 0 of 0 labels bound to a contract property; 12 of 36 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-370",
  "name": "Customer Subscription & Commercial Portfolio",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "1",
   "number": "2",
   "page": 8
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/customer-subscription-commercial-portfolio-adm-370",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/CustomerSubscriptionCommercialPortfolio.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-369"
   ],
   "exitTo": [
    "ADM-369"
   ],
   "transitions": [
    {
     "to": "ADM-369",
     "trigger": "Back to Commercial Command Center",
     "provenance": "structural — pack board 1 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Table Columns) and no metric row",
  "purpose": "Provide a central portfolio of every TICVAI customer and their current commercial position.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 8 §Table Columns"
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
       "label": "Search customer subscription commercial",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 8 §Filter by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Commercial Model",
        "Operational Profile",
        "Tier",
        "Country",
        "Venue",
        "Status",
        "Renewal Period",
        "VSI",
        "Minimum Guarantee",
        "Usage",
        "Revenue",
        "Opportunity Type"
       ],
       "notes": "The pack filters this screen by commercial model, operational profile, tier, country, venue, status and 6 more — which are present is a decision the pack already made.",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 8 §Filter by"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every customer subscription commercial",
       "columns": [
        "Customer",
        "Venue / Group",
        "Country",
        "VSI",
        "Operational Profile",
        "Commercial Model",
        "Tier where applicable",
        "Contracted Rate",
        "Minimum Guarantee",
        "Active Modules",
        "Monthly Equivalent Revenue",
        "Billable Volume",
        "Usage %",
        "Contract Start",
        "Renewal Date",
        "Subscription Status",
        "Commercial Health"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 8 §Table Columns"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected customer subscription commercial",
       "bindsTo": null,
       "columns": [
        "Customer",
        "Venue / Group",
        "Country",
        "VSI",
        "Operational Profile",
        "Commercial Model",
        "Tier where applicable",
        "Contracted Rate",
        "Minimum Guarantee",
        "Active Modules",
        "Monthly Equivalent Revenue",
        "Billable Volume",
        "Usage %",
        "Contract Start",
        "Renewal Date",
        "Subscription Status",
        "Commercial Health"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Enterprise Operational Profile”, “AED 20K/month minimum”, “Commercial Health Indicators”.",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 8 §Table Columns"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The customer subscription commercial list.",
   "error": "Could not load. Names which read failed and leaves the customer subscription commercial untouched.",
   "emptyFirstRun": "No customer subscription commercial yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the customer subscription commercial are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "entryState": {
   "preloaded": [
    "Customer",
    "Venue / Group",
    "Country",
    "VSI",
    "Operational Profile",
    "Commercial Model"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-370"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 8. 0 of 29 labels bound to a contract property; 29 of 41 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-371",
  "name": "Customer Commercial 360°",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "1",
   "number": "3",
   "page": 9
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/customer-commercial-360-adm-371",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/CustomerCommercial360.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-369"
   ],
   "exitTo": [
    "ADM-369"
   ],
   "transitions": [
    {
     "to": "ADM-369",
     "trigger": "Back to Commercial Command Center",
     "provenance": "structural — pack board 1 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide the complete commercial, operational and subscription profile for one customer. This screen must clearly separate commercial charging from technical/operational classification.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 9"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 9"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The customer commercial 360° list.",
   "error": "Could not load. Names which read failed and leaves the customer commercial 360° untouched.",
   "emptyFirstRun": "No customer commercial 360° yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the customer commercial 360° are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-371"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 9. 0 of 0 labels bound to a contract property; 0 of 43 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-372",
  "name": "Operational Profile, VSI & Commercial Model Intelligence",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "1",
   "number": "4",
   "page": 10
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/operational-profile-vsi-commercial-model-intelligence-adm-372",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/OperationalProfileVsiCommercialModelIntelligence.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-369"
   ],
   "exitTo": [
    "ADM-369"
   ],
   "transitions": [
    {
     "to": "ADM-369",
     "trigger": "Back to Commercial Command Center",
     "provenance": "structural — pack board 1 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Analyze whether customers' operational profiles and commercial structures remain appropriate. This replaces the previous focus only on Tier Distribution & VSI.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Customers by VSI",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 10 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Customers by Operational Profile",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 10 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Customers by Commercial Model",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 10 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Average VSI",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 10 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Profile Misalignment",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 10 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Commercial Model Optimization Candidates",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 10 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Upgrade Candidates",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 10 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Downgrade Candidates",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 10 §KPIs"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The operational profile vsi list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the operational profile vsi untouched.",
   "emptyFirstRun": "No operational profile vsi yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the operational profile vsi are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "entryState": {
   "preloaded": [
    "Customers by VSI",
    "Customers by Operational Profile",
    "Customers by Commercial Model",
    "Average VSI",
    "Profile Misalignment",
    "Commercial Model Optimization Candidates"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-372"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 10. 0 of 0 labels bound to a contract property; 8 of 19 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-373",
  "name": "Revenue & Commercial Model Analytics",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "1",
   "number": "5",
   "page": 11
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/revenue-commercial-model-analytics-adm-373",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/RevenueCommercialModelAnalytics.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-369"
   ],
   "exitTo": [
    "ADM-369"
   ],
   "transitions": [
    {
     "to": "ADM-369",
     "trigger": "Back to Commercial Command Center",
     "provenance": "structural — pack board 1 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§KPIs) and a per-row directory (§Show) — counts over a population, then the population",
  "purpose": "Analyze TICVAI revenue across all commercial structures.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 11 §Show"
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
       "label": "MRR / Monthly Equivalent",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 11 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "ARR / ACV",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 11 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "New Revenue",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 11 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Expansion Revenue",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 11 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Contraction Revenue",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 11 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Churned Revenue",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 11 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "NRR",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 11 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "ARPC",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 11 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Growth %",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 11 §KPIs"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every revenue commercial model",
       "columns": [
        "Guaranteed Revenue",
        "Actual Variable Revenue",
        "Guarantee Shortfall Protection",
        "Contracts Above Guarantee",
        "Contracts at Guarantee"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 11 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected revenue commercial model",
       "bindsTo": null,
       "columns": [
        "Guaranteed Revenue",
        "Actual Variable Revenue",
        "Guarantee Shortfall Protection",
        "Contracts Above Guarantee",
        "Contracts at Guarantee"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Break down”, “Revenue by”.",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 11 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The revenue commercial model list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the revenue commercial model untouched.",
   "emptyFirstRun": "No revenue commercial model yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the revenue commercial model are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "entryState": {
   "preloaded": [
    "MRR / Monthly Equivalent",
    "ARR / ACV",
    "New Revenue",
    "Expansion Revenue",
    "Contraction Revenue",
    "Churned Revenue"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-373"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 11. 0 of 5 labels bound to a contract property; 14 of 38 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-374",
  "name": "Trial & Conversion Monitor",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "1",
   "number": "6",
   "page": 12
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/trial-conversion-monitor-adm-374",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/TrialConversionMonitor.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-369"
   ],
   "exitTo": [
    "ADM-369"
   ],
   "transitions": [
    {
     "to": "ADM-369",
     "trigger": "Back to Commercial Command Center",
     "provenance": "structural — pack board 1 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Monitor trial customers and their expected transition into paid commercial agreements.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Active Trials",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 12 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "New Trials",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 12 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Expiring Trials",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 12 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Trial-to-Paid %",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 12 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Average Trial Duration",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 12 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Setup Completion",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 12 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Go-Live Readiness",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 12 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Estimated Conversion Value",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 12 §KPIs"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The trial conversion list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the trial conversion untouched.",
   "emptyFirstRun": "No trial conversion yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the trial conversion are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-374"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 12. 0 of 0 labels bound to a contract property; 8 of 27 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-375",
  "name": "Renewal & Retention Center",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "1",
   "number": "7",
   "page": 13
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/renewal-retention-center-adm-375",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/RenewalRetentionCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-369"
   ],
   "exitTo": [
    "ADM-369"
   ],
   "transitions": [
    {
     "to": "ADM-369",
     "trigger": "Back to Commercial Command Center",
     "provenance": "structural — pack board 1 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§KPIs) and a per-row directory (§Columns) — counts over a population, then the population",
  "purpose": "Manage upcoming renewals and identify retention or commercial restructuring requirements.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 13 §Columns"
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
       "label": "Renewals Next 30 Days",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 13 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Next 60 Days",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 13 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Next 90 Days",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 13 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Renewal Value",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 13 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Renewal Rate",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 13 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "At-Risk Revenue",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 13 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Auto-Renew Value",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 13 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Expansion Opportunity",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 13 §KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Optimization Opportunity",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 13 §KPIs"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every renewal retention",
       "columns": [
        "Customer",
        "Commercial Model",
        "Current Rate",
        "Minimum Guarantee",
        "Monthly Equivalent",
        "Contract Value",
        "Renewal Date",
        "Usage Trend",
        "Payment Health",
        "Risk",
        "AI Recommendation"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 13 §Columns"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected renewal retention",
       "bindsTo": null,
       "columns": [
        "Customer",
        "Commercial Model",
        "Current Rate",
        "Minimum Guarantee",
        "Monthly Equivalent",
        "Contract Value",
        "Renewal Date",
        "Usage Trend",
        "Payment Health",
        "Risk",
        "AI Recommendation"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Retention Signals”.",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 13 §Columns"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The renewal retention list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the renewal retention untouched.",
   "emptyFirstRun": "No renewal retention yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the renewal retention are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-375"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 13. 0 of 11 labels bound to a contract property; 20 of 36 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-376",
  "name": "Commercial Optimization & Expansion Opportunities",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "1",
   "number": "8",
   "page": 14
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/commercial-optimization-expansion-opportunities-adm-376",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/CommercialOptimizationExpansionOpportunities.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-369"
   ],
   "exitTo": [
    "ADM-369"
   ],
   "transitions": [
    {
     "to": "ADM-369",
     "trigger": "Back to Commercial Command Center",
     "provenance": "structural — pack board 1 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Opportunity KPIs) and a per-row directory (§Show) — counts over a population, then the population",
  "purpose": "Identify opportunities beyond traditional tier upgrades. This is a key revision from the original Upgrade, Downgrade & Expansion Opportunities screen.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 14 §Show"
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
       "label": "Total Opportunities",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 14 §Opportunity KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Potential Expansion Revenue",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 14 §Opportunity KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Potential Retention Value",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 14 §Opportunity KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Model Optimization Opportunities",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 14 §Opportunity KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Module Opportunities",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 14 §Opportunity KPIs"
      },
      {
       "kind": "metricTile",
       "label": "Cost Optimization Opportunities",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 14 §Opportunity KPIs"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every commercial optimization expansion",
       "columns": [
        "Current Customer Cost",
        "Proposed Customer Cost",
        "TICVAI Revenue Impact",
        "Minimum Revenue Protection",
        "Customer Saving/Increase",
        "Confidence"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 14 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected commercial optimization expansion",
       "bindsTo": null,
       "columns": [
        "Current Customer Cost",
        "Proposed Customer Cost",
        "TICVAI Revenue Impact",
        "Minimum Revenue Protection",
        "Customer Saving/Increase",
        "Confidence"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Opportunity Types”, “Current”, “Projected Volume”.",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 14 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The commercial optimization expansion list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the commercial optimization expansion untouched.",
   "emptyFirstRun": "No commercial optimization expansion yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the commercial optimization expansion are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "entryState": {
   "preloaded": [
    "Total Opportunities",
    "Potential Expansion Revenue",
    "Potential Retention Value",
    "Model Optimization Opportunities",
    "Module Opportunities",
    "Cost Optimization Opportunities"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-376"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 14. 0 of 6 labels bound to a contract property; 12 of 32 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-377",
  "name": "Subscription Exceptions & Commercial Alerts",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "1",
   "number": "9",
   "page": 16
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/subscription-exceptions-commercial-alerts-adm-377",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/SubscriptionExceptionsCommercialAlerts.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-369"
   ],
   "exitTo": [
    "ADM-369"
   ],
   "transitions": [
    {
     "to": "ADM-369",
     "trigger": "Back to Commercial Command Center",
     "provenance": "structural — pack board 1 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide management with one consolidated view of subscription, licensing, commercial, billing and metering exceptions.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 16"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 16"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The subscription exceptions commercial list.",
   "error": "Could not load. Names which read failed and leaves the subscription exceptions commercial untouched.",
   "emptyFirstRun": "No subscription exceptions commercial yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the subscription exceptions commercial are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-377"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 16. 0 of 0 labels bound to a contract property; 0 of 29 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-378",
  "name": "Executive AI Commercial Intelligence",
  "module": "Tenants & Licensing",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Subscription_Licensing_AI_Self_Service.pdf",
   "board": "1",
   "number": "10",
   "page": 17
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/tenants-licensing/executive-ai-commercial-intelligence-adm-378",
   "component": "apps/ticvai-web/src/routes/tenants-licensing/ExecutiveAiCommercialIntelligence.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-369"
   ],
   "exitTo": [
    "ADM-369"
   ],
   "transitions": [
    {
     "to": "ADM-369",
     "trigger": "Back to Commercial Command Center",
     "provenance": "structural — pack board 1 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Customer Metrics; Revenue Metrics; Variable Commercial Metrics) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide TICVAI leadership with an AI-powered executive commercial intelligence layer.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 0 operations.** Unserved: Board 1 — Standardized Commercial Metrics. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Subscription_Licensing_AI_Self_Service.pdf, page 17 §Actions"
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
       "label": "Active Customers",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 17 §Customer Metrics"
      },
      {
       "kind": "metricTile",
       "label": "New Customers",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 17 §Customer Metrics"
      },
      {
       "kind": "metricTile",
       "label": "Churned Customers",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 17 §Customer Metrics"
      },
      {
       "kind": "metricTile",
       "label": "Trials",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 17 §Customer Metrics"
      },
      {
       "kind": "metricTile",
       "label": "Conversion",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 17 §Customer Metrics"
      },
      {
       "kind": "metricTile",
       "label": "MRR / Monthly Equivalent Revenue",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 17 §Revenue Metrics"
      },
      {
       "kind": "metricTile",
       "label": "ARR / ACV",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 17 §Revenue Metrics"
      },
      {
       "kind": "metricTile",
       "label": "New Revenue",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 17 §Revenue Metrics"
      },
      {
       "kind": "metricTile",
       "label": "Expansion",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 17 §Revenue Metrics"
      },
      {
       "kind": "metricTile",
       "label": "Contraction",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 17 §Revenue Metrics"
      },
      {
       "kind": "metricTile",
       "label": "Churn",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 17 §Revenue Metrics"
      },
      {
       "kind": "metricTile",
       "label": "NRR",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 17 §Revenue Metrics"
      },
      {
       "kind": "metricTile",
       "label": "ARPC",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 17 §Revenue Metrics"
      },
      {
       "kind": "metricTile",
       "label": "Billable Tickets",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 17 §Variable Commercial Metrics"
      },
      {
       "kind": "metricTile",
       "label": "Billable Transactions",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 17 §Variable Commercial Metrics"
      },
      {
       "kind": "metricTile",
       "label": "Eligible Transaction Value",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 17 §Variable Commercial Metrics"
      },
      {
       "kind": "metricTile",
       "label": "Variable Revenue",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 17 §Variable Commercial Metrics"
      },
      {
       "kind": "metricTile",
       "label": "Minimum Guaranteed Revenue",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 17 §Variable Commercial Metrics"
      },
      {
       "kind": "metricTile",
       "label": "Guarantee Utilization",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 17 §Variable Commercial Metrics"
      },
      {
       "kind": "metricTile",
       "label": "Revenue Above Guarantee",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 17 §Variable Commercial Metrics"
      },
      {
       "kind": "metricTile",
       "label": "VSI",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 17 §Operational Metrics"
      },
      {
       "kind": "metricTile",
       "label": "Operational Profile",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 17 §Operational Metrics"
      },
      {
       "kind": "metricTile",
       "label": "POS Utilization",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 17 §Operational Metrics"
      },
      {
       "kind": "metricTile",
       "label": "Access Utilization",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 17 §Operational Metrics"
      },
      {
       "kind": "metricTile",
       "label": "User Utilization",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 17 §Operational Metrics"
      },
      {
       "kind": "metricTile",
       "label": "API",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 17 §Operational Metrics"
      },
      {
       "kind": "metricTile",
       "label": "Storage",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 17 §Operational Metrics"
      },
      {
       "kind": "metricTile",
       "label": "Admissions",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 17 §Operational Metrics"
      },
      {
       "kind": "metricTile",
       "label": "Renewal Risk",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 17 §Commercial Intelligence Metrics"
      },
      {
       "kind": "metricTile",
       "label": "Expansion Probability",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 17 §Commercial Intelligence Metrics"
      },
      {
       "kind": "metricTile",
       "label": "Model Optimization Opportunity",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 17 §Commercial Intelligence Metrics"
      },
      {
       "kind": "metricTile",
       "label": "Cost Optimization",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 17 §Commercial Intelligence Metrics"
      },
      {
       "kind": "metricTile",
       "label": "Upgrade/Downgrade Probability",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 17 §Commercial Intelligence Metrics"
      },
      {
       "kind": "metricTile",
       "label": "Commercial Health",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 17 §Commercial Intelligence Metrics"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Board 1 — Standardized Commercial Metrics",
       "provenance": "pack Subscription_Licensing_AI_Self_Service.pdf, page 17 §Actions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The executive commercial intelligence list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the executive commercial intelligence untouched.",
   "emptyFirstRun": "No executive commercial intelligence yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the executive commercial intelligence are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "entryState": {
   "preloaded": [
    "Active Customers",
    "New Customers",
    "Churned Customers",
    "Trials",
    "Conversion",
    "MRR / Monthly Equivalent Revenue"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-378"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 17. 0 of 0 labels bound to a contract property; 35 of 95 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
