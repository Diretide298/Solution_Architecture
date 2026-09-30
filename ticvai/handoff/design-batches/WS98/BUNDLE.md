# WS98 — Subscription Licensing AI Self Service board 1

**10 screens · 11 operations · 21 schemas · 3 permissions**

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
  `PLATFORM_BILLING_VIEW, PLATFORM_PLAN_MANAGE, PLATFORM_TENANT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-369` | Commercial Command Center | commandCentre | 2 | 0 | — |
| `ADM-370` | Customer Subscription & Commercial Portfolio | listDetail | 1 | 0 | — |
| `ADM-371` | Customer Commercial 360° | listDetail | 2 | 0 | — |
| `ADM-372` | Operational Profile, VSI & Commercial Model Intelligence | commandCentre | 1 | 0 | — |
| `ADM-373` | Revenue & Commercial Model Analytics | commandCentre | 1 | 0 | — |
| `ADM-374` | Trial & Conversion Monitor | commandCentre | 2 | 0 | — |
| `ADM-375` | Renewal & Retention Center | commandCentre | 1 | 0 | — |
| `ADM-376` | Commercial Optimization & Expansion Opportunities | commandCentre | 1 | 0 | — |
| `ADM-377` | Subscription Exceptions & Commercial Alerts | listDetail | 1 | 0 | — |
| `ADM-378` | Executive AI Commercial Intelligence | commandCentre | 2 | 0 | — |

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
  "apis": [
   {
    "operationId": "listTenants",
    "contract": "subscription",
    "purpose": "The commercial portfolio",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "getSubscription",
    "contract": "subscription",
    "purpose": "One customer",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-369",
   "workshopBoard": "wireframes/WS153 Subscription Licensing AI Self Service Board 1.dc.html#adm-369"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 6. 0 of 0 labels bound to a contract property; 12 of 36 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "tenantId",
     "from": "session"
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
  "apis": [
   {
    "operationId": "listTenants",
    "contract": "subscription",
    "purpose": "Subscriptions by tier",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-370",
   "workshopBoard": "wireframes/WS153 Subscription Licensing AI Self Service Board 1.dc.html#adm-370"
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
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "detailPanel",
       "derived": true,
       "impliedBy": "getSubscription",
       "notes": "One record, read-only."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The customer commercial 360° list.",
   "error": "Could not load. Names which read failed and leaves the customer commercial 360° untouched.",
   "emptyFirstRun": "No customer commercial 360° yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the customer commercial 360° are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getSubscription",
    "contract": "subscription",
    "purpose": "Commercial 360",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "getEntitlementUsage",
    "contract": "subscription",
    "purpose": "What they consume",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-371",
   "workshopBoard": "wireframes/WS153 Subscription Licensing AI Self Service Board 1.dc.html#adm-371"
  },
  "apisNote": "Regenerated 9 September 2026 from Subscription_Licensing_AI_Self_Service.pdf page 9. 0 of 0 labels bound to a contract property; 0 of 43 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "tenantId",
     "from": "session"
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
  "apis": [
   {
    "operationId": "scoreVsiAssessment",
    "contract": "subscription",
    "purpose": "Their VSI and model",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-372",
   "workshopBoard": "wireframes/WS153 Subscription Licensing AI Self Service Board 1.dc.html#adm-372"
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
  "apis": [
   {
    "operationId": "getBillingReconciliation",
    "contract": "subscription",
    "purpose": "Revenue against metering",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-373",
   "workshopBoard": "wireframes/WS153 Subscription Licensing AI Self Service Board 1.dc.html#adm-373"
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
  "apis": [
   {
    "operationId": "setTrialConfiguration",
    "contract": "subscription",
    "purpose": "Trial rules",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listTenants",
    "contract": "subscription",
    "purpose": "Trials running",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-374",
   "workshopBoard": "wireframes/WS153 Subscription Licensing AI Self Service Board 1.dc.html#adm-374"
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
  "apis": [
   {
    "operationId": "listMembershipRenewalRetention",
    "contract": "subscription",
    "purpose": "Membership Analytics, Renewal Intelligence & AI Retention Center",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-375",
   "workshopBoard": "wireframes/WS153 Subscription Licensing AI Self Service Board 1.dc.html#adm-375"
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
  "apis": [
   {
    "operationId": "listRenewalAuto",
    "contract": "subscription",
    "purpose": "Renewals due",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-376",
   "workshopBoard": "wireframes/WS153 Subscription Licensing AI Self Service Board 1.dc.html#adm-376"
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
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "simulateCommercialPackage",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "simulateCommercialPackage"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The subscription exceptions commercial list.",
   "error": "Could not load. Names which read failed and leaves the subscription exceptions commercial untouched.",
   "emptyFirstRun": "No subscription exceptions commercial yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the subscription exceptions commercial are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "simulateCommercialPackage",
    "contract": "subscription",
    "purpose": "Expansion options",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-377",
   "workshopBoard": "wireframes/WS153 Subscription Licensing AI Self Service Board 1.dc.html#adm-377"
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
  "purpose": "Provide TICVAI leadership with an AI-powered executive commercial intelligence layer. Allow a new customer to register, describe their venue/business, and let TICVAI intelligently determine their operational requirements before calculating the VSI, recommending a subscription tier, and suggesting modules.",
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
  "apis": [
   {
    "operationId": "getLicenceEnforcement",
    "contract": "subscription",
    "purpose": "Exceptions and overage",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "getPlanRecommendations",
    "contract": "subscription",
    "purpose": "Commercial recommendations beside the enforcement position",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-378",
   "workshopBoard": "wireframes/WS153 Subscription Licensing AI Self Service Board 1.dc.html#adm-378"
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
{
 "getBillingReconciliation": {
  "method": "GET",
  "path": "/billing-reconciliation",
  "contract": "subscription",
  "summary": "Metered consumption against what was invoiced",
  "permission": "PLATFORM_BILLING_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "platform",
  "parameters": [
   {
    "name": "tenantId",
    "in": "query",
    "required": true
   },
   {
    "name": "period",
    "in": "query",
    "required": true
   }
  ],
  "requestBody": null,
  "responds": "BillingReconciliation"
 },
 "getEntitlementUsage": {
  "method": "GET",
  "path": "/tenants/{tenantId}/entitlement-usage",
  "contract": "subscription",
  "summary": "Usage against licensed limits",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "EntitlementUsage"
 },
 "getLicenceEnforcement": {
  "method": "GET",
  "path": "/licence-enforcement",
  "contract": "subscription",
  "summary": "Where a tenant stands against its entitlements, and what happens next",
  "permission": "PLATFORM_BILLING_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "platform",
  "parameters": [
   {
    "name": "tenantId",
    "in": "query",
    "required": true
   }
  ],
  "requestBody": null,
  "responds": "LicenceEnforcement"
 },
 "getPlanRecommendations": {
  "method": "GET",
  "path": "/plan-recommendations",
  "contract": "subscription",
  "summary": "Which plan, module or pack would fit this tenant better, and what it would cost or save",
  "permission": "PLATFORM_BILLING_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "platform",
  "parameters": [
   {
    "name": "tenantId",
    "in": "query",
    "required": true
   },
   {
    "name": "horizonMonths",
    "in": "query",
    "required": null
   },
   {
    "name": "kind",
    "in": "query",
    "required": null
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
 "getSubscription": {
  "method": "GET",
  "path": "/tenants/{tenantId}/subscription",
  "contract": "subscription",
  "summary": "Read the current subscription",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "Subscription"
 },
 "listMembershipRenewalRetention": {
  "method": "GET",
  "path": "/membership-renewal-retention",
  "contract": "subscription",
  "summary": "Membership Analytics, Renewal Intelligence & AI Retention Center",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "membershipProduct",
    "in": "query",
    "required": false
   },
   {
    "name": "tier",
    "in": "query",
    "required": false
   },
   {
    "name": "venue",
    "in": "query",
    "required": false
   },
   {
    "name": "customerSegment",
    "in": "query",
    "required": false
   },
   {
    "name": "geography",
    "in": "query",
    "required": false
   },
   {
    "name": "renewalCohort",
    "in": "query",
    "required": false
   },
   {
    "name": "purchaseMonth",
    "in": "query",
    "required": false
   },
   {
    "name": "acquisitionChannel",
    "in": "query",
    "required": false
   },
   {
    "name": "churnFlag",
    "in": "query",
    "required": false
   },
   {
    "name": "maxRenewalProbability",
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
 "listRenewalAuto": {
  "method": "GET",
  "path": "/renewal-auto",
  "contract": "subscription",
  "summary": "Renewal Operations & Auto-Renewal Management",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "renewalStatus",
    "in": "query",
    "required": false
   },
   {
    "name": "membershipProduct",
    "in": "query",
    "required": false
   },
   {
    "name": "tier",
    "in": "query",
    "required": false
   },
   {
    "name": "autoRenew",
    "in": "query",
    "required": false
   },
   {
    "name": "expiringFrom",
    "in": "query",
    "required": false
   },
   {
    "name": "expiringTo",
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
 "listTenants": {
  "method": "GET",
  "path": "/tenants",
  "contract": "subscription",
  "summary": "List tenants",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "planId",
    "in": "query",
    "required": null
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
 "scoreVsiAssessment": {
  "method": "POST",
  "path": "/vsi-assessments",
  "contract": "subscription",
  "summary": "Score a prospect's answers into a tier and a package",
  "permission": "PLATFORM_PLAN_MANAGE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "platform",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "VsiAssessment",
  "responds": "VsiResult"
 },
 "setTrialConfiguration": {
  "method": "PUT",
  "path": "/trial-configurations",
  "contract": "subscription",
  "summary": "What a trial includes, how long it lasts and how it converts",
  "permission": "PLATFORM_PLAN_MANAGE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "platform",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "TrialConfiguration",
  "responds": "TrialConfiguration"
 },
 "simulateCommercialPackage": {
  "method": "POST",
  "path": "/package-simulations",
  "contract": "subscription",
  "summary": "What this package would cost, and what it would provision",
  "permission": "PLATFORM_PLAN_MANAGE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "platform",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "PackageSimulationRequest",
  "responds": "PackageSimulation"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "BillingReconciliation": {
  "type": "object",
  "description": "Boards 10.2 and 10.3. **The first invoice sets the tone for the relationship.**",
  "properties": {
   "tenantId": {
    "type": "string",
    "format": "uuid"
   },
   "period": {
    "type": "string"
   },
   "lines": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "unit": {
       "type": "string"
      },
      "meteredQuantity": {
       "type": "integer"
      },
      "billedQuantity": {
       "type": "integer"
      },
      "unitPrice": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "amount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "variance": {
       "type": "integer"
      }
     }
    }
   },
   "meteredNotBilled": {
    "type": "integer"
   },
   "billedNotMetered": {
    "type": "integer"
   },
   "invoiceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "approvedBy": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   }
  }
 },
 "EntitlementUsage": {
  "x-ticvai-persistence": "none — aggregated from usage_record",
  "type": "object",
  "required": [
   "tenantId",
   "metrics"
  ],
  "properties": {
   "tenantId": {
    "type": "string",
    "format": "uuid"
   },
   "metrics": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "metric",
      "current",
      "isNearLimit"
     ],
     "properties": {
      "metric": {
       "$ref": "#/components/schemas/UsageMetric"
      },
      "current": {
       "type": "integer"
      },
      "limit": {
       "type": "integer",
       "nullable": true
      },
      "percentUsed": {
       "type": "number",
       "nullable": true
      },
      "isNearLimit": {
       "type": "boolean",
       "description": "Approaching a limit is an account conversation. Hitting one silently at a gate is an incident.\n"
      },
      "isExceeded": {
       "type": "boolean"
      }
     }
    }
   },
   "asAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "LicenceEnforcement": {
  "type": "object",
  "description": "Board 9.5. **Three states, three responses.**",
  "properties": {
   "tenantId": {
    "type": "string",
    "format": "uuid"
   },
   "period": {
    "type": "string"
   },
   "units": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "unit": {
       "type": "string"
      },
      "allowance": {
       "type": "integer"
      },
      "consumed": {
       "type": "integer"
      },
      "percentUsed": {
       "type": "number"
      },
      "projectedAtPeriodEnd": {
       "type": "integer",
       "nullable": true
      },
      "state": {
       "type": "string",
       "enum": [
        "withinAllowance",
        "approaching",
        "atLimit",
        "overage"
       ]
      },
      "nextAction": {
       "type": "string",
       "nullable": true
      },
      "overageCharge": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      }
     }
    }
   },
   "minimumGuaranteeMet": {
    "type": "boolean"
   },
   "alertsRaised": {
    "type": "integer"
   }
  }
 },
 "LocalisedText": {
  "x-ticvai-persistence": "none — jsonb column",
  "type": "object",
  "additionalProperties": {
   "type": "string"
  }
 },
 "MembershipAnalyticsRenewalIntelligenceAiRetentionCenSummary": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection; the headline tiles over the list, computed at read time for the filters in force",
  "description": "**The headline figures on Membership Analytics, Renewal Intelligence & AI Retention Center.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.",
  "properties": {
   "activeMembers": {
    "type": "integer",
    "description": "Active Members"
   },
   "newMemberships": {
    "type": "integer",
    "description": "New Memberships"
   },
   "renewalRate": {
    "type": "number",
    "description": "Renewal Rate"
   },
   "churnRate": {
    "type": "number",
    "description": "Churn Rate"
   },
   "autoRenewSuccess": {
    "type": "number",
    "description": "Auto-Renew Success: percentage of auto-renew attempts that succeeded"
   },
   "averageMembershipTenure": {
    "type": "number",
    "description": "Average Membership Tenure in months"
   },
   "averageVisitsPerMember": {
    "type": "number",
    "description": "Average Visits per Member"
   },
   "revenuePerMember": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue per Member"
   },
   "membershipUtilization": {
    "type": "number",
    "description": "Membership Utilization"
   },
   "benefitUtilization": {
    "type": "number",
    "description": "Benefit Utilization"
   },
   "freezeSuspensionRate": {
    "type": "number",
    "description": "Freeze/Suspension Rate"
   },
   "expectedRenewals": {
    "type": "integer",
    "description": "Expected Renewals in the forecast period"
   },
   "expectedChurn": {
    "type": "integer",
    "description": "Expected Churn in the forecast period"
   },
   "renewalRevenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Renewal Revenue"
   },
   "membershipBaseGrowth": {
    "type": "number",
    "description": "Membership Base Growth, percent"
   },
   "upgradeRate": {
    "type": "number",
    "description": "Upgrade Rate, percent (pack p.35)"
   },
   "upgradeRevenue": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Upgrade Revenue forecast (pack p.37)"
   },
   "renewalFunnel": {
    "type": "object",
    "description": "Renewal Funnel (pack p.36)",
    "properties": {
     "eligibleForRenewal": {
      "type": "integer"
     },
     "contacted": {
      "type": "integer"
     },
     "renewalStarted": {
      "type": "integer"
     },
     "paymentAttempted": {
      "type": "integer"
     },
     "renewed": {
      "type": "integer"
     },
     "failed": {
      "type": "integer"
     },
     "expired": {
      "type": "integer"
     }
    }
   }
  }
 },
 "MembershipAnalyticsRenewalIntelligenceAiRetentionCenView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Membership Analytics, Renewal Intelligence & AI Retention Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "visits": {
    "type": "integer",
    "description": "Visits in the current term"
   },
   "benefitUsage": {
    "type": "number",
    "description": "Benefit usage, percent of allocation used"
   },
   "guestTicketUsage": {
    "type": "integer",
    "description": "Guest tickets used this term"
   },
   "complaintsExceptions": {
    "type": "integer",
    "description": "Complaints/Exceptions this term"
   },
   "confidence": {
    "type": "number",
    "description": "Confidence of the prediction, 0-1"
   },
   "keyDrivers": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Key Drivers, e.g. visits down 58%, no visits in 90 days"
   },
   "modelVersion": {
    "type": "string",
    "description": "Model Version"
   },
   "dataFreshness": {
    "type": "string",
    "format": "date-time",
    "description": "Data Freshness: when the inputs were last refreshed"
   },
   "membershipId": {
    "type": "string",
    "description": "Membership ID"
   },
   "memberName": {
    "type": "string",
    "description": "Member name"
   },
   "membershipProduct": {
    "type": "string",
    "description": "Membership product"
   },
   "tier": {
    "type": "string",
    "description": "Tier",
    "nullable": true
   },
   "expiryDate": {
    "type": "string",
    "format": "date",
    "description": "Expiry date"
   },
   "lastVisitDate": {
    "type": "string",
    "format": "date",
    "description": "Last visit",
    "nullable": true
   },
   "renewalProbability": {
    "type": "number",
    "description": "Member Renewal Probability, 0-1 (advisory)"
   },
   "churnFlag": {
    "type": "boolean",
    "description": "No visit in the last 90 days: flagged for churn follow-up (MoM 8 Sep)"
   },
   "recommendedActions": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "renewalReminder",
      "benefitReminder",
      "membershipEducation",
      "upgradeOffer",
      "retentionOffer",
      "serviceFollowUp"
     ]
    },
    "description": "Recommended Actions (pack p.36), advisory"
   }
  }
 },
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
 "PackageSimulation": {
  "type": "object",
  "description": "Boards 3.9 and 4.8. **Refused at quote time rather than at go-live.**",
  "properties": {
   "lines": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "kind": {
       "type": "string",
       "enum": [
        "baseTier",
        "module",
        "addOn",
        "capacityPack",
        "overage",
        "professionalServices",
        "discount"
       ]
      },
      "label": {
       "type": "string"
      },
      "quantity": {
       "type": "number",
       "nullable": true
      },
      "unitPrice": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "amount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      }
     }
    }
   },
   "recurringTotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "oneOffTotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "contractTotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "minimumGuarantee": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "findings": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "severity": {
       "type": "string",
       "enum": [
        "blocking",
        "warning",
        "advisory"
       ]
      },
      "code": {
       "type": "string"
      },
      "message": {
       "type": "string"
      }
     }
    }
   },
   "provisionable": {
    "type": "boolean"
   }
  }
 },
 "PackageSimulationRequest": {
  "type": "object",
  "required": [
   "tierCode"
  ],
  "properties": {
   "tierCode": {
    "type": "string"
   },
   "licensingModelId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "moduleCodes": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "venueCount": {
    "type": "integer",
    "default": 1
   },
   "projectedVolumes": {
    "type": "object",
    "additionalProperties": {
     "type": "integer"
    }
   },
   "contractMonths": {
    "type": "integer",
    "default": 12
   },
   "billingCycle": {
    "type": "string",
    "nullable": true
   },
   "currency": {
    "type": "string",
    "nullable": true
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
 "RenewalOperationsAutoRenewalManagementSummary": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection; the headline tiles over the list, computed at read time for the filters in force",
  "description": "**The headline figures on Renewal Operations & Auto-Renewal Management.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.",
  "properties": {
   "renewalNotOpen": {
    "type": "integer",
    "description": "Renewal Not Open"
   },
   "renewalEligible": {
    "type": "integer",
    "description": "Renewal Eligible"
   },
   "renewalInvitationSent": {
    "type": "integer",
    "description": "Renewal Invitation Sent"
   },
   "renewalStarted": {
    "type": "integer",
    "description": "Renewal Started"
   },
   "paymentPending": {
    "type": "integer",
    "description": "Payment Pending"
   },
   "renewed": {
    "type": "integer",
    "description": "Renewed"
   },
   "autoRenewScheduled": {
    "type": "integer",
    "description": "Auto-Renew Scheduled"
   },
   "autoRenewFailed": {
    "type": "integer",
    "description": "Auto-Renew Failed"
   },
   "gracePeriod": {
    "type": "integer",
    "description": "Grace Period"
   },
   "expiredWithoutRenewal": {
    "type": "integer",
    "description": "Expired Without Renewal"
   }
  }
 },
 "RenewalOperationsAutoRenewalManagementView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Renewal Operations & Auto-Renewal Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "member": {
    "type": "string",
    "description": "Member"
   },
   "membership": {
    "type": "string",
    "description": "Membership"
   },
   "tier": {
    "type": "string",
    "description": "Tier"
   },
   "expiry": {
    "type": "string",
    "format": "date",
    "description": "Expiry"
   },
   "renewalWindow": {
    "type": "object",
    "description": "Renewal Window",
    "properties": {
     "opens": {
      "type": "string",
      "format": "date"
     },
     "closes": {
      "type": "string",
      "format": "date"
     }
    }
   },
   "renewalPrice": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "Renewal Price from pricing (Area 10)"
   },
   "autoRenew": {
    "type": "boolean",
    "description": "Auto-Renew: the member has explicitly opted in"
   },
   "paymentMethodStatus": {
    "type": "string",
    "description": "Payment Method Status: none, valid, expiringSoon, expired or failed"
   },
   "eligibility": {
    "type": "string",
    "enum": [
     "eligible",
     "notEligible",
     "reviewRequired"
    ],
    "description": "Eligibility for renewal"
   },
   "renewalStatus": {
    "type": "string",
    "description": "Renewal Status: renewalNotOpen, renewalEligible, renewalInvitationSent, renewalStarted, paymentPending, renewed, autoRenewScheduled, autoRenewFailed, gracePeriod or expiredWithoutRenewal (pack p.30 Renewal Pipeline)"
   },
   "membershipStatus": {
    "type": "string",
    "description": "Current membership status: one of the membership lifecycle values active, frozen, suspended, expired or cancelled (shape follows catalogue GuestMembership.status; states/guest-membership-status.yaml): frozen is the member's pause and extends validity, suspended is a sanction and does not"
   },
   "outstandingIssues": {
    "type": "string",
    "description": "Outstanding Issues",
    "nullable": true
   },
   "autoRenewConsentAt": {
    "type": "string",
    "format": "date-time",
    "description": "Consent: when the member accepted the auto-renewal terms; empty means no consent and auto-renew will not run",
    "nullable": true
   },
   "membershipVersion": {
    "type": "integer",
    "description": "Membership Version the renewal will be on"
   },
   "membershipId": {
    "type": "string",
    "description": "Membership ID"
   },
   "preNotificationSentAt": {
    "type": "string",
    "format": "date-time",
    "description": "Pre-renewal reminder sent",
    "nullable": true
   },
   "paymentAttempts": {
    "type": "integer",
    "description": "Auto-renew payment attempts so far"
   },
   "nextAttemptAt": {
    "type": "string",
    "format": "date-time",
    "description": "Next scheduled payment attempt",
    "nullable": true
   }
  }
 },
 "Subscription": {
  "x-ticvai-persistence": "subscription.contract",
  "type": "object",
  "required": [
   "tenantId",
   "planId",
   "planVersion",
   "status",
   "startsAt"
  ],
  "properties": {
   "tenantId": {
    "type": "string",
    "format": "uuid"
   },
   "planId": {
    "type": "string",
    "format": "uuid"
   },
   "planName": {
    "type": "string"
   },
   "planVersion": {
    "type": "string"
   },
   "status": {
    "type": "string",
    "enum": [
     "trial",
     "active",
     "pastDue",
     "cancelled",
     "expired"
    ]
   },
   "startsAt": {
    "type": "string",
    "format": "date"
   },
   "renewsAt": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "cancelledAt": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "scheduledChange": {
    "type": "object",
    "nullable": true,
    "readOnly": true,
    "description": "A downgrade waiting for the next renewal (decided 28 September, audit R214 (1)). Null when none is scheduled.",
    "properties": {
     "planId": {
      "type": "string",
      "format": "uuid"
     },
     "planVersion": {
      "type": "string"
     },
     "effectiveFrom": {
      "type": "string",
      "format": "date",
      "description": "Always the `renewsAt` it was scheduled against."
     }
    }
   },
   "currentPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "billingPeriod": {
    "type": "string"
   }
  }
 },
 "SubscriptionPlanRecommendation": {
  "type": "object",
  "x-ticvai-persistence": "none — computed from control.usage_record, the plan, tier and add-on limits and capacity packs, priced as simulateCommercialPackage prices",
  "description": "One plan-fit move for a tenant, priced against staying as it is (20.8.4, 20.8.5; decided 29 September, build pass, group G2).",
  "required": [
   "kind",
   "reason",
   "projectedMonthlyCost"
  ],
  "properties": {
   "kind": {
    "type": "string",
    "enum": [
     "upgrade",
     "downgrade",
     "addModule",
     "removeModule",
     "removeAddOn",
     "capacityPack"
    ]
   },
   "targetPlanId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The tier to move to, for `upgrade` and `downgrade`."
   },
   "moduleCode": {
    "type": "string",
    "nullable": true,
    "description": "For `addModule` and `removeModule`."
   },
   "addOnCode": {
    "type": "string",
    "nullable": true,
    "description": "For `removeAddOn`."
   },
   "billableUnit": {
    "type": "string",
    "nullable": true,
    "description": "The unit that drives it (for `upgrade`, `downgrade` and `capacityPack`), as `getLicenceEnforcement` names it."
   },
   "capacityPackSize": {
    "type": "integer",
    "nullable": true,
    "description": "For `capacityPack`, the pack size that covers the projected overage."
   },
   "projectedMonthlyCost": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "projectedSaving": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "Against staying as it is over the horizon, monthly. Set where the move saves money."
   },
   "projectedAddedCost": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "Where the move costs more than today but less than the alternative named in `comparedWith`."
   },
   "comparedWith": {
    "type": "string",
    "enum": [
     "currentPackage",
     "projectedOverage",
     "nextTier",
     "capacityPack"
    ],
    "description": "What the move is cheaper than. An `upgrade` is compared with paying the projected overage; a `capacityPack` with the next tier."
   },
   "reason": {
    "type": "string",
    "maxLength": 500,
    "description": "One sentence a person can repeat to the customer."
   },
   "basis": {
    "type": "object",
    "description": "The numbers it rests on.",
    "properties": {
     "usageWindowDays": {
      "type": "integer"
     },
     "usedAverage": {
      "type": "number",
      "nullable": true
     },
     "usedPeak": {
      "type": "number",
      "nullable": true
     },
     "projectedPeak": {
      "type": "number",
      "nullable": true
     },
     "currentLimit": {
      "type": "number",
      "nullable": true
     },
     "targetLimit": {
      "type": "number",
      "nullable": true
     },
     "lastUsedAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true,
      "description": "For `removeModule` and `removeAddOn`, the last metered use; null for never."
     }
    }
   },
   "applyWith": {
    "type": "string",
    "enum": [
     "setSubscription",
     "addCapacityPack"
    ],
    "description": "The operation a person uses to carry it out (after `previewSubscriptionChange` for `setSubscription`)."
   }
  }
 },
 "SuspensionMode": {
  "type": "string",
  "description": "Access validation continues under every mode. A commercial dispute must not strand guests at a gate holding valid tickets.\n",
  "enum": [
   "readOnly",
   "noNewSales",
   "fullLockout"
  ]
 },
 "Tenant": {
  "x-ticvai-persistence": "control.tenant",
  "type": "object",
  "required": [
   "id",
   "code",
   "name",
   "status",
   "createdAt"
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
   "status": {
    "$ref": "#/components/schemas/TenantStatus"
   },
   "suspensionMode": {
    "$ref": "#/components/schemas/SuspensionMode"
   },
   "suspensionReason": {
    "type": "string",
    "nullable": true
   },
   "suspensionEffectiveAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "When the suspension takes, or took, effect — `suspendTenant.effectiveAt`. **A future value is a pending suspension**: the tenant stays `active` until then, and this row is the only place that says a suspension is coming."
   },
   "suspensionNoticeMessage": {
    "$ref": "#/components/schemas/LocalisedText",
    "description": "The notice shown to the tenant's users about the suspension — `suspendTenant.noticeMessage`."
   },
   "terminationScheduledAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "When `terminateTenant` started the retention window. Null when no termination is under way."
   },
   "terminationRetentionUntil": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "`terminationScheduledAt` plus the request's `retentionDays`. **Stored, not recomputed** — the day count is client-supplied and exists nowhere else, and this is the date the cells are destroyed after."
   },
   "terminationReason": {
    "type": "string",
    "maxLength": 1000,
    "nullable": true
   },
   "terminationRequestedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "planId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "planName": {
    "type": "string",
    "nullable": true
   },
   "cellCount": {
    "type": "integer"
   },
   "venueCount": {
    "type": "integer"
   },
   "regionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "The tenant's home region: the `tenancy` region node whose `RegionSettings` govern tenant-wide gates, today `allowedAiResidencies` (decided 28 September, audit R203). Written by the server when the tenant's first region is created; null until then. ADM-037 reads it to show the region's residency restriction, and `ai.setAiProvider` checks against the same region.\n"
   },
   "billingEmail": {
    "type": "string"
   },
   "billingAddress": {
    "type": "string",
    "maxLength": 500,
    "nullable": true,
    "description": "Accepted by `createTenant` and `updateTenant`; stored here so the response can return what was sent."
   },
   "accountManagerPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "activatedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "TenantStatus": {
  "type": "string",
  "enum": [
   "onboarding",
   "active",
   "suspended",
   "terminating",
   "terminated"
  ]
 },
 "TrialConfiguration": {
  "type": "object",
  "x-ticvai-persistence": "subscription.trial_config",
  "description": "Board 5.5. **A trial that expires with no conversion path is a tenant full of real data nobody can bill.**\n",
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "tierCode": {
    "type": "string",
    "nullable": true
   },
   "durationDays": {
    "type": "integer",
    "default": 30
   },
   "includedModules": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "usageCaps": {
    "type": "object",
    "additionalProperties": {
     "type": "integer"
    }
   },
   "paymentMethodRequiredUpFront": {
    "type": "boolean",
    "default": false
   },
   "conversionOfferPercent": {
    "type": "number",
    "nullable": true
   },
   "noticeDaysBeforeExpiry": {
    "type": "array",
    "items": {
     "type": "integer"
    }
   },
   "onExpiry": {
    "type": "string",
    "enum": [
     "suspend",
     "convert",
     "decommission"
    ],
    "default": "suspend",
    "description": "**Suspension is the humane default.** Customers routinely let a trial lapse and come back a week later.\n"
   },
   "retainDataDays": {
    "type": "integer",
    "default": 90
   }
  }
 },
 "UsageMetric": {
  "type": "string",
  "enum": [
   "venues",
   "workstations",
   "activeUsers",
   "devices",
   "brandedApps",
   "aiTokens",
   "apiCalls",
   "storageGb",
   "transactions",
   "guestProfiles"
  ]
 },
 "VsiAssessment": {
  "type": "object",
  "x-ticvai-persistence": "subscription.vsi_assessment",
  "description": "Board 2 — the ten-screen questionnaire, as data.",
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "organisationName": {
    "type": "string",
    "nullable": true
   },
   "contactEmail": {
    "type": "string",
    "nullable": true
   },
   "venueType": {
    "type": "string",
    "nullable": true
   },
   "answers": {
    "type": "object",
    "additionalProperties": true
   },
   "requestedModules": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "submittedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "VsiResult": {
  "type": "object",
  "description": "Board 2.10. **A prospect told only their price has been told nothing they can argue with.**\n",
  "properties": {
   "assessmentId": {
    "type": "string",
    "format": "uuid"
   },
   "score": {
    "type": "number"
   },
   "tierCode": {
    "type": "string"
   },
   "tierName": {
    "type": "string"
   },
   "factors": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "code": {
       "type": "string"
      },
      "label": {
       "type": "string"
      },
      "answer": {
       "type": "string"
      },
      "points": {
       "type": "number"
      }
     }
    }
   },
   "recommendedModules": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "recommendedPlanId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "indicativePrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   }
  }
 }
}
```
