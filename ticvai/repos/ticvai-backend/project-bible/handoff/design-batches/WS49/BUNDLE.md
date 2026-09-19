# WS49 — Promotions   Bundles Management board 5

**10 screens · 10 operations · 14 schemas · 2 permissions**

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
| `ADM-178` | Bundle & Combo Command Center | commandCentre | 1 | 0 | — |
| `ADM-179` | Bundle Definition & Setup | configEditor | 1 | 0 | — |
| `ADM-180` | Bundle Component Builder | configEditor | 1 | 0 | — |
| `ADM-181` | Guest Choice & Build-Your-Own Bundle Designer | configEditor | 1 | 0 | — |
| `ADM-182` | Bundle Pricing & Commercial Model | configEditor | 1 | 0 | — |
| `ADM-183` | Bundle Availability, Capacity & Validation | listDetail | 1 | 0 | — |
| `ADM-184` | Bundle Validity, Scheduling & Redemption Rules | listDetail | 1 | 0 | — |
| `ADM-185` | Partner & External Product Bundle Manager | listDetail | 1 | 0 | — |
| `ADM-186` | Revenue Allocation, Cost & Settlement Rules | configEditor | 1 | 0 | — |
| `ADM-187` | Bundle Preview, Simulation & AI Recommendation | listDetail | 1 | 0 | — |

## Thin screens in this batch

**ADM-183, ADM-184, ADM-185, ADM-187 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-178",
  "name": "Bundle & Combo Command Center",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "5",
   "number": "1",
   "page": 63
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/bundle-combo-command-center-adm-178",
   "component": "apps/ticvai-web/src/routes/commercial/BundleComboCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-179",
    "ADM-180",
    "ADM-181",
    "ADM-182",
    "ADM-183",
    "ADM-184",
    "ADM-185",
    "ADM-186",
    "ADM-187"
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
     "to": "ADM-179",
     "trigger": "Works in Bundle Definition & Setup",
     "provenance": "flow F158 step 1→2",
     "operation": "listBundleCombo"
    },
    {
     "to": "ADM-180",
     "trigger": "Works in Bundle Component Builder",
     "provenance": "flow F158 step 3→4",
     "operation": "listBundleCombo"
    },
    {
     "to": "ADM-181",
     "trigger": "Works in Guest Choice & Build-Your-Own Bundle Designer",
     "provenance": "flow F158 step 5→6",
     "operation": "listBundleCombo"
    },
    {
     "to": "ADM-182",
     "trigger": "Works in Bundle Pricing & Commercial Model",
     "provenance": "flow F158 step 7→8",
     "operation": "listBundleCombo"
    },
    {
     "to": "ADM-183",
     "trigger": "Works in Bundle Availability, Capacity & Validation",
     "provenance": "flow F158 step 9→10",
     "operation": "listBundleCombo"
    },
    {
     "to": "ADM-184",
     "trigger": "Works in Bundle Validity, Scheduling & Redemption Rules",
     "provenance": "flow F158 step 11→12",
     "operation": "listBundleCombo"
    },
    {
     "to": "ADM-185",
     "trigger": "Works in Partner & External Product Bundle Manager",
     "provenance": "flow F158 step 13→14",
     "operation": "listBundleCombo"
    },
    {
     "to": "ADM-186",
     "trigger": "Works in Revenue Allocation, Cost & Settlement Rules",
     "provenance": "flow F158 step 15→16",
     "operation": "listBundleCombo"
    },
    {
     "to": "ADM-187",
     "trigger": "Works in Bundle Preview, Simulation & AI Recommendation",
     "provenance": "flow F158 step 17→18",
     "operation": "listBundleCombo"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide centralized visibility and management of all bundles and combo products across",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search bundle combo",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 63 §Filter by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Ticket bundle",
        "Multi-attraction",
        "Multi-park",
        "Family package",
        "Ticket + F&B",
        "Ticket + Retail",
        "Ticket + Experience",
        "Ticket + Parking",
        "Membership package",
        "Partner bundle",
        "Hotel package",
        "Dynamic bundle",
        "Build-your-own bundle"
       ],
       "notes": "The pack filters this screen by ticket bundle, multi-attraction, multi-park, family package, ticket + f&b, ticket + retail and 7 more — which are present is a decision the pack already made.",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 63 §Filter by"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Active Bundles",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 63 §KPI Cards",
       "bindsTo": "BundleComboCommandCenterView.activeBundles"
      },
      {
       "kind": "metricTile",
       "label": "Draft Bundles",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 63 §KPI Cards",
       "bindsTo": "BundleComboCommandCenterView.draftBundles"
      },
      {
       "kind": "metricTile",
       "label": "Scheduled Bundles",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 63 §KPI Cards",
       "bindsTo": "BundleComboCommandCenterView.scheduledBundles"
      },
      {
       "kind": "metricTile",
       "label": "Dynamic Bundles",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 63 §KPI Cards",
       "bindsTo": "BundleComboCommandCenterView.dynamicBundles"
      },
      {
       "kind": "metricTile",
       "label": "Fixed Bundles",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 63 §KPI Cards",
       "bindsTo": "BundleComboCommandCenterView.fixedBundles"
      },
      {
       "kind": "metricTile",
       "label": "Guest-Choice Bundles",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 63 §KPI Cards",
       "bindsTo": "BundleComboCommandCenterView.guestChoiceBundles"
      },
      {
       "kind": "metricTile",
       "label": "Partner Bundles",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 63 §KPI Cards",
       "bindsTo": "BundleComboCommandCenterView.partnerBundles"
      },
      {
       "kind": "metricTile",
       "label": "Bundle Sales",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 63 §KPI Cards",
       "bindsTo": "BundleComboCommandCenterView.bundleSales"
      },
      {
       "kind": "metricTile",
       "label": "Bundle Revenue",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 63 §KPI Cards",
       "bindsTo": "BundleComboCommandCenterView.bundleRevenue"
      },
      {
       "kind": "metricTile",
       "label": "Average Bundle Value",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 63 §KPI Cards",
       "bindsTo": "BundleComboCommandCenterView.averageBundleValue"
      },
      {
       "kind": "metricTile",
       "label": "Bundle Conversion Rate",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 63 §KPI Cards",
       "bindsTo": "BundleComboCommandCenterView.bundleConversionRate"
      },
      {
       "kind": "metricTile",
       "label": "Redemption Rate",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 63 §KPI Cards",
       "bindsTo": "BundleComboCommandCenterView.redemptionRate"
      },
      {
       "kind": "metricTile",
       "label": "AOV Uplift",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 63 §KPI Cards",
       "bindsTo": "BundleComboCommandCenterView.aovUplift"
      },
      {
       "kind": "metricTile",
       "label": "Bundle Margin",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 63 §KPI Cards",
       "bindsTo": "BundleComboCommandCenterView.bundleMargin"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The bundle combo list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the bundle combo untouched.",
   "emptyFirstRun": "No bundle combo yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the bundle combo are still there. The pack's own statuses are Draft — the state names which is selected.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listBundleCombo",
    "contract": "promotions",
    "purpose": "Bundle & Combo Command Center",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "BundleComboCommandCenterView.activeBundles",
    "BundleComboCommandCenterView.draftBundles",
    "BundleComboCommandCenterView.scheduledBundles",
    "BundleComboCommandCenterView.dynamicBundles",
    "BundleComboCommandCenterView.fixedBundles",
    "BundleComboCommandCenterView.guestChoiceBundles"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-178"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 63. 14 of 27 labels bound to a contract property; 37 of 40 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-179",
  "name": "Bundle Definition & Setup",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "5",
   "number": "2",
   "page": 65
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/bundle-definition-setup-adm-179",
   "component": "apps/ticvai-web/src/routes/commercial/BundleDefinitionSetup.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-178"
   ],
   "exitTo": [
    "ADM-178"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-178, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-178",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F158 step 2→3",
     "operation": "setBundleDefinition"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure; Configure whether the bundle) and no display directory — it is settings, not a population",
  "purpose": "Create the commercial identity and high-level behavior of a bundle.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Bundle name",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 65 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Bundle ID",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 65 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Internal description",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 65 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Guest-facing description",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 65 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Business entity",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 65 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 65 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Bundle category",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 65 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Owner",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 65 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Campaign",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 65 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Effective dates",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 65 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Sales status",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 65 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save changes",
       "provenance": "contract operation setBundleDefinition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The bundle definition configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the bundle definition untouched.",
   "emptyFirstRun": "No bundle definition configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setBundleDefinition",
    "contract": "promotions",
    "purpose": "Bundle Definition & Setup",
    "trigger": "onAction",
    "invalidates": [
     "setBundleDefinition"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-179"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 65. 0 of 0 labels bound to a contract property; 11 of 26 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-180",
  "name": "Bundle Component Builder",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "5",
   "number": "3",
   "page": 66
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/bundle-component-builder-adm-180",
   "component": "apps/ticvai-web/src/routes/commercial/BundleComponentBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-178"
   ],
   "exitTo": [
    "ADM-178"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-178, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-178",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F158 step 4→5",
     "operation": "setBundleComponent"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Define exactly what products and services make up the bundle.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Fixed quantity",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 66 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Minimum",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 66 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 66 §Configure"
      },
      {
       "kind": "textField",
       "label": "Quantity based on guest count",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 66 §Configure"
      },
      {
       "kind": "textField",
       "label": "Quantity based on ticket count",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 66 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save changes",
       "provenance": "contract operation setBundleComponent"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The bundle component configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the bundle component untouched.",
   "emptyFirstRun": "No bundle component configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setBundleComponent",
    "contract": "promotions",
    "purpose": "Bundle Component Builder",
    "trigger": "onAction",
    "invalidates": [
     "setBundleComponent"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-180"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 66. 0 of 0 labels bound to a contract property; 5 of 31 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-181",
  "name": "Guest Choice & Build-Your-Own Bundle Designer",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "5",
   "number": "4",
   "page": 67
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/guest-choice-build-your-own-bundle-designer-adm-181",
   "component": "apps/ticvai-web/src/routes/commercial/GuestChoiceBuildYourOwnBundleDesigner.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-178"
   ],
   "exitTo": [
    "ADM-178"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-178, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-178",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F158 step 6→7",
     "operation": "setGuestChoiceBuild"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Choose 1 F&B Option) and no display directory — it is settings, not a population",
  "purpose": "Configure bundles where the guest chooses products from predefined groups. The matrix specifically requires the guest to be able to choose attractions, experiences, F&B, retail products, or services from predefined categories while maintaining bundle pricing rules.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Meal A",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 67 §Choose 1 F&B Option"
      },
      {
       "kind": "selectField",
       "label": "Meal B",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 67 §Choose 1 F&B Option"
      },
      {
       "kind": "selectField",
       "label": "Meal C",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 67 §Choose 1 F&B Option"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save changes",
       "provenance": "contract operation setGuestChoiceBuild"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The guest choice build-your-own configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the guest choice build-your-own untouched.",
   "emptyFirstRun": "No guest choice build-your-own configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setGuestChoiceBuild",
    "contract": "promotions",
    "purpose": "Guest Choice & Build-Your-Own Bundle Designer",
    "trigger": "onAction",
    "invalidates": [
     "setGuestChoiceBuild"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-181"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 67. 0 of 0 labels bound to a contract property; 3 of 27 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-182",
  "name": "Bundle Pricing & Commercial Model",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "5",
   "number": "5",
   "page": 68
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/bundle-pricing-commercial-model-adm-182",
   "component": "apps/ticvai-web/src/routes/commercial/BundlePricingCommercialModel.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-178"
   ],
   "exitTo": [
    "ADM-178"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-178, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-178",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F158 step 8→9",
     "operation": "listBundlePricingCommercial"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Pricing Configuration) and no display directory — it is settings, not a population",
  "purpose": "Determine how the bundle is commercially priced.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Base price",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 68 §Pricing Configuration"
      },
      {
       "kind": "selectField",
       "label": "Currency",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 68 §Pricing Configuration"
      },
      {
       "kind": "selectField",
       "label": "Discount %",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 68 §Pricing Configuration"
      },
      {
       "kind": "selectField",
       "label": "Discount amount",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 68 §Pricing Configuration"
      },
      {
       "kind": "selectField",
       "label": "Minimum price",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 68 §Pricing Configuration"
      },
      {
       "kind": "selectField",
       "label": "Maximum price",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 68 §Pricing Configuration"
      },
      {
       "kind": "selectField",
       "label": "Price floor",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 68 §Pricing Configuration"
      },
      {
       "kind": "selectField",
       "label": "Margin floor",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 68 §Pricing Configuration"
      },
      {
       "kind": "selectField",
       "label": "Guest-specific price",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 68 §Pricing Configuration"
      },
      {
       "kind": "selectField",
       "label": "Channel-specific price",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 68 §Pricing Configuration"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The bundle pricing commercial configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the bundle pricing commercial untouched.",
   "emptyFirstRun": "No bundle pricing commercial configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listBundlePricingCommercial",
    "contract": "promotions",
    "purpose": "Bundle Pricing & Commercial Model",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-182"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 68. 0 of 0 labels bound to a contract property; 10 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-183",
  "name": "Bundle Availability, Capacity & Validation",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "5",
   "number": "6",
   "page": 69
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/bundle-availability-capacity-validation-adm-183",
   "component": "apps/ticvai-web/src/routes/commercial/BundleAvailabilityCapacityValidation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-178"
   ],
   "exitTo": [
    "ADM-178"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-178, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-178",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F158 step 10→11",
     "operation": "listBundleAvailabilityCapacity"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§For each component display) and no metric row",
  "purpose": "Ensure that TICVAI does not sell a bundle unless all required components can actually be fulfilled. This is a direct requirement of the matrix: each bundle component maintains independent inventory, capacity, validity, redemption rules, and availability, and the system validates included products before confirming the sale.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every bundle availability capacity",
       "columns": [
        "BundleAvailabilityCapacityValidationView.available",
        "BundleAvailabilityCapacityValidationView.lowAvailability",
        "BundleAvailabilityCapacityValidationView.soldOut",
        "BundleAvailabilityCapacityValidationView.suspended",
        "BundleAvailabilityCapacityValidationView.unpublished",
        "BundleAvailabilityCapacityValidationView.invalidDate",
        "BundleAvailabilityCapacityValidationView.capacityUnavailable"
       ],
       "bindsTo": "BundleAvailabilityCapacityValidationView",
       "operation": "listBundleAvailabilityCapacity",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 69 §For each component display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected bundle availability capacity",
       "bindsTo": "BundleAvailabilityCapacityValidationView",
       "columns": [
        "BundleAvailabilityCapacityValidationView.available",
        "BundleAvailabilityCapacityValidationView.lowAvailability",
        "BundleAvailabilityCapacityValidationView.soldOut",
        "BundleAvailabilityCapacityValidationView.suspended",
        "BundleAvailabilityCapacityValidationView.unpublished",
        "BundleAvailabilityCapacityValidationView.invalidDate",
        "BundleAvailabilityCapacityValidationView.capacityUnavailable"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Bundle selected”, “Check mandatory components”, “Check inventory”, “Check capacity”, “Check schedule/timeslot”, “Check validity”.",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 69 §For each component display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The bundle availability capacity list.",
   "error": "Could not load. Names which read failed and leaves the bundle availability capacity untouched.",
   "emptyFirstRun": "No bundle availability capacity yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the bundle availability capacity are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listBundleAvailabilityCapacity",
    "contract": "promotions",
    "purpose": "Bundle Availability, Capacity & Validation",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "BundleAvailabilityCapacityValidationView.available",
    "BundleAvailabilityCapacityValidationView.lowAvailability",
    "BundleAvailabilityCapacityValidationView.soldOut",
    "BundleAvailabilityCapacityValidationView.suspended",
    "BundleAvailabilityCapacityValidationView.unpublished",
    "BundleAvailabilityCapacityValidationView.invalidDate"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-183"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 69. 7 of 7 labels bound to a contract property; 7 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-184",
  "name": "Bundle Validity, Scheduling & Redemption Rules",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "5",
   "number": "7",
   "page": 70
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/bundle-validity-scheduling-redemption-rules-adm-184",
   "component": "apps/ticvai-web/src/routes/commercial/BundleValiditySchedulingRedemptionRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-178"
   ],
   "exitTo": [
    "ADM-178"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-178, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-178",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F158 step 12→13",
     "operation": "listBundleValidityScheduling"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Control when bundle components may be consumed and whether they must be redeemed together or separately.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 70"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 70"
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
       "impliedBy": "listBundleValidityScheduling",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The bundle validity scheduling list.",
   "error": "Could not load. Names which read failed and leaves the bundle validity scheduling untouched.",
   "emptyFirstRun": "No bundle validity scheduling yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the bundle validity scheduling are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listBundleValidityScheduling",
    "contract": "promotions",
    "purpose": "Bundle Validity, Scheduling & Redemption Rules",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "BundleValiditySchedulingRedemptionRulesView.valid1June31August",
    "BundleValiditySchedulingRedemptionRulesView.allComponentsTogether",
    "BundleValiditySchedulingRedemptionRulesView.independentRedemption",
    "BundleValiditySchedulingRedemptionRulesView.sequentialRedemption",
    "BundleValiditySchedulingRedemptionRulesView.firstUseActivation"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-184"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 70. 0 of 0 labels bound to a contract property; 0 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-185",
  "name": "Partner & External Product Bundle Manager",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "5",
   "number": "8",
   "page": 71
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/partner-external-product-bundle-manager-adm-185",
   "component": "apps/ticvai-web/src/routes/commercial/PartnerExternalProductBundleManager.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-178"
   ],
   "exitTo": [
    "ADM-178"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-178, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-178",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F158 step 14→15",
     "operation": "listPartnerExternalProduct"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Allow TICVAI bundles to include products or services owned by external operators. The matrix requires combinations with external products/services and bundles across different destinations, including systems that may use different databases.",
  "gaps": [
   {
    "operation": null,
    "why": "**Partner & External Product Bundle Manager declares no operation that writes anything** — its only declared call is `listPartnerExternalProduct`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
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
       "label": "Every partner external product",
       "columns": [
        "PartnerExternalProductBundleManagerView.connected",
        "PartnerExternalProductBundleManagerView.available",
        "PartnerExternalProductBundleManagerView.degraded",
        "PartnerExternalProductBundleManagerView.apiError",
        "PartnerExternalProductBundleManagerView.productUnavailable",
        "PartnerExternalProductBundleManagerView.mappingError"
       ],
       "bindsTo": "PartnerExternalProductBundleManagerView",
       "operation": "listPartnerExternalProduct",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 71 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected partner external product",
       "bindsTo": "PartnerExternalProductBundleManagerView",
       "columns": [
        "PartnerExternalProductBundleManagerView.connected",
        "PartnerExternalProductBundleManagerView.available",
        "PartnerExternalProductBundleManagerView.degraded",
        "PartnerExternalProductBundleManagerView.apiError",
        "PartnerExternalProductBundleManagerView.productUnavailable",
        "PartnerExternalProductBundleManagerView.mappingError"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Dubai Weekend Package”.",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 71 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The partner external product list.",
   "error": "Could not load. Names which read failed and leaves the partner external product untouched.",
   "emptyFirstRun": "No partner external product yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the partner external product are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPartnerExternalProduct",
    "contract": "promotions",
    "purpose": "Partner & External Product Bundle Manager",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "PartnerExternalProductBundleManagerView.connected",
    "PartnerExternalProductBundleManagerView.available",
    "PartnerExternalProductBundleManagerView.degraded",
    "PartnerExternalProductBundleManagerView.apiError",
    "PartnerExternalProductBundleManagerView.productUnavailable",
    "PartnerExternalProductBundleManagerView.mappingError"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-185"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 71. 6 of 6 labels bound to a contract property; 17 of 33 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-186",
  "name": "Revenue Allocation, Cost & Settlement Rules",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "5",
   "number": "9",
   "page": 72
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/revenue-allocation-cost-settlement-rules-adm-186",
   "component": "apps/ticvai-web/src/routes/commercial/RevenueAllocationCostSettlementRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-178"
   ],
   "exitTo": [
    "ADM-178"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-178, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-178",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F158 step 16→17",
     "operation": "listRevenueAllocationCost"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Financial Configuration) and no display directory — it is settings, not a population",
  "purpose": "Determine how bundle revenue is allocated across its components. This is explicitly required by the matrix for allocation across products, attractions, departments, partners, operators, and accounting entities.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Revenue account",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 72 §Financial Configuration"
      },
      {
       "kind": "selectField",
       "label": "Department",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 72 §Financial Configuration"
      },
      {
       "kind": "selectField",
       "label": "Cost center",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 72 §Financial Configuration"
      },
      {
       "kind": "selectField",
       "label": "Legal entity",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 72 §Financial Configuration"
      },
      {
       "kind": "selectField",
       "label": "Tax treatment",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 72 §Financial Configuration"
      },
      {
       "kind": "selectField",
       "label": "Partner payable",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 72 §Financial Configuration"
      },
      {
       "kind": "selectField",
       "label": "Commission",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 72 §Financial Configuration"
      },
      {
       "kind": "selectField",
       "label": "Settlement cycle",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 72 §Financial Configuration"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The revenue allocation cost configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the revenue allocation cost untouched.",
   "emptyFirstRun": "No revenue allocation cost configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listRevenueAllocationCost",
    "contract": "promotions",
    "purpose": "Revenue Allocation, Cost & Settlement Rules",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-186"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 72. 0 of 0 labels bound to a contract property; 8 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-187",
  "name": "Bundle Preview, Simulation & AI Recommendation",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "5",
   "number": "10",
   "page": 32
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/bundle-preview-simulation-ai-recommendation-adm-187",
   "component": "apps/ticvai-web/src/routes/commercial/BundlePreviewSimulationAiRecommendation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-178"
   ],
   "exitTo": [
    "ADM-178"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-178, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation."
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow administrators to test promotional rules before activating them. This is critical because the matrix requires simulation of redemption, discount exposure, revenue impact, margin impact and financial performance before activation.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Campaign Manager. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 32 §Support roles including"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 32"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 32"
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
       "label": "Campaign Manager",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 32 §Support roles including"
      },
      {
       "kind": "banner",
       "label": "Permissions this screen separates",
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** Create rules, Edit rules, Change discount, Change thresholds, Change segments, Change dates, Override limits, Run simulation, Submit, Approve, Activate. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 32 §Permissions must independently control"
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
   "loading": "The bundle preview simulation list.",
   "error": "Could not load. Names which read failed and leaves the bundle preview simulation untouched.",
   "emptyFirstRun": "No bundle preview simulation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the bundle preview simulation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "simulateBundlePreviewRecommendation",
    "contract": "promotions",
    "purpose": "Bundle Preview, Simulation & AI Recommendation",
    "trigger": "onAction",
    "invalidates": [
     "simulateBundlePreviewRecommendation"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-187"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 32. 0 of 0 labels bound to a contract property; 12 of 76 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "listBundleAvailabilityCapacity": {
  "method": "GET",
  "path": "/bundle-availability-capacity",
  "contract": "promotions",
  "summary": "Bundle Availability, Capacity & Validation",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "BundleAvailabilityCapacityValidationView"
 },
 "listBundleCombo": {
  "method": "GET",
  "path": "/bundle-combo",
  "contract": "promotions",
  "summary": "Bundle & Combo Command Center",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "ticketBundle",
    "in": "query",
    "required": false
   },
   {
    "name": "multiAttraction",
    "in": "query",
    "required": false
   },
   {
    "name": "multiPark",
    "in": "query",
    "required": false
   },
   {
    "name": "familyPackage",
    "in": "query",
    "required": false
   },
   {
    "name": "ticketFB",
    "in": "query",
    "required": false
   },
   {
    "name": "ticketRetail",
    "in": "query",
    "required": false
   },
   {
    "name": "ticketExperience",
    "in": "query",
    "required": false
   },
   {
    "name": "ticketParking",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "BundleComboCommandCenterView"
 },
 "listBundlePricingCommercial": {
  "method": "GET",
  "path": "/bundle-pricing-commercial",
  "contract": "promotions",
  "summary": "Bundle Pricing & Commercial Model",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "BundlePricingCommercialModelView"
 },
 "listBundleValidityScheduling": {
  "method": "GET",
  "path": "/bundle-validity-scheduling",
  "contract": "promotions",
  "summary": "Bundle Validity, Scheduling & Redemption Rules",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "BundleValiditySchedulingRedemptionRulesView"
 },
 "listPartnerExternalProduct": {
  "method": "GET",
  "path": "/partner-external-product",
  "contract": "promotions",
  "summary": "Partner & External Product Bundle Manager",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "PartnerExternalProductBundleManagerView"
 },
 "listRevenueAllocationCost": {
  "method": "GET",
  "path": "/revenue-allocation-cost",
  "contract": "promotions",
  "summary": "Revenue Allocation, Cost & Settlement Rules",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "RevenueAllocationCostSettlementRulesView"
 },
 "setBundleComponent": {
  "method": "PUT",
  "path": "/bundle-component",
  "contract": "promotions",
  "summary": "Bundle Component Builder",
  "permission": "PRICE_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "BundleComponentBuilderInput",
  "responds": "BundleComponentBuilderView"
 },
 "setBundleDefinition": {
  "method": "PUT",
  "path": "/bundle-definition",
  "contract": "promotions",
  "summary": "Bundle Definition & Setup",
  "permission": "PRICE_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "BundleDefinitionSetupInput",
  "responds": "BundleDefinitionSetupView"
 },
 "setGuestChoiceBuild": {
  "method": "PUT",
  "path": "/guest-choice-build",
  "contract": "promotions",
  "summary": "Guest Choice & Build-Your-Own Bundle Designer",
  "permission": "PRICE_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "GuestChoiceBuildYourOwnBundleDesignerInput",
  "responds": "GuestChoiceBuildYourOwnBundleDesignerView"
 },
 "simulateBundlePreviewRecommendation": {
  "method": "PUT",
  "path": "/bundle-preview-recommendation",
  "contract": "promotions",
  "summary": "Bundle Preview, Simulation & AI Recommendation",
  "permission": "PRICE_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "BundlePreviewSimulationAiRecommendationInput",
  "responds": "BundlePreviewSimulationAiRecommendationView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "BundleAvailabilityCapacityValidationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Bundle Availability, Capacity & Validation displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "available": {
    "type": "string",
    "description": "Available"
   },
   "lowAvailability": {
    "type": "string",
    "description": "Low availability"
   },
   "soldOut": {
    "type": "string",
    "description": "Sold out"
   },
   "suspended": {
    "type": "string",
    "description": "Suspended"
   },
   "unpublished": {
    "type": "string",
    "description": "Unpublished"
   },
   "invalidDate": {
    "type": "string",
    "format": "date-time",
    "description": "Invalid date"
   },
   "capacityUnavailable": {
    "type": "integer",
    "description": "Capacity unavailable"
   },
   "independentCapacity": {
    "type": "integer",
    "description": "independent capacity"
   }
  }
 },
 "BundleComboCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Bundle & Combo Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "activeBundles": {
    "type": "integer",
    "description": "Active Bundles"
   },
   "draftBundles": {
    "type": "integer",
    "description": "Draft Bundles"
   },
   "scheduledBundles": {
    "type": "integer",
    "description": "Scheduled Bundles"
   },
   "dynamicBundles": {
    "type": "integer",
    "description": "Dynamic Bundles"
   },
   "fixedBundles": {
    "type": "integer",
    "description": "Fixed Bundles"
   },
   "guestChoiceBundles": {
    "type": "integer",
    "description": "Guest-Choice Bundles"
   },
   "partnerBundles": {
    "type": "integer",
    "description": "Partner Bundles"
   },
   "bundleSales": {
    "type": "integer",
    "description": "Bundle Sales"
   },
   "bundleRevenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Bundle Revenue"
   },
   "averageBundleValue": {
    "type": "number",
    "description": "Average Bundle Value"
   },
   "bundleConversionRate": {
    "type": "number",
    "description": "Bundle Conversion Rate"
   },
   "redemptionRate": {
    "type": "number",
    "description": "Redemption Rate"
   },
   "aovUplift": {
    "type": "number",
    "description": "AOV Uplift"
   },
   "bundleMargin": {
    "type": "number",
    "description": "Bundle Margin"
   },
   "draft": {
    "type": "string",
    "description": "Draft"
   },
   "incomplete": {
    "type": "string",
    "description": "Incomplete"
   },
   "pendingValidation": {
    "type": "integer",
    "description": "Pending Validation"
   },
   "pendingApproval": {
    "type": "integer",
    "description": "Pending Approval"
   },
   "scheduled": {
    "type": "string",
    "format": "date-time",
    "description": "Scheduled"
   },
   "active": {
    "type": "integer",
    "description": "Active"
   },
   "paused": {
    "type": "string",
    "description": "Paused"
   },
   "suspended": {
    "type": "string",
    "description": "Suspended"
   },
   "expired": {
    "type": "integer",
    "description": "Expired"
   },
   "archived": {
    "type": "string",
    "description": "Archived"
   }
  }
 },
 "BundleComponentBuilderInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Bundle Component Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "admissionTicket": {
    "type": "string",
    "description": "Admission ticket"
   },
   "attraction": {
    "type": "string",
    "description": "Attraction"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "timeslot": {
    "type": "string",
    "description": "Timeslot"
   },
   "experience": {
    "type": "string",
    "description": "Experience"
   },
   "membership": {
    "type": "string",
    "description": "Membership"
   },
   "annualPass": {
    "type": "string",
    "description": "Annual pass"
   },
   "fBProduct": {
    "type": "string",
    "description": "F&B product"
   },
   "fBMealPackage": {
    "type": "string",
    "description": "F&B meal package"
   },
   "retailProduct": {
    "type": "string",
    "description": "Retail product"
   },
   "parking": {
    "type": "string",
    "description": "Parking"
   },
   "locker": {
    "type": "string",
    "description": "Locker"
   },
   "photo": {
    "type": "string",
    "description": "Photo"
   },
   "rental": {
    "type": "string",
    "description": "Rental"
   },
   "voucher": {
    "type": "string",
    "description": "Voucher"
   },
   "giftCard": {
    "type": "string",
    "description": "Gift card"
   },
   "service": {
    "type": "string",
    "description": "Service"
   },
   "externalProduct": {
    "type": "string",
    "description": "External product"
   },
   "ntYEntTreatment": {
    "type": "string",
    "description": "nt y ent Treatment"
   },
   "photo1OptionalAed30": {
    "type": "string",
    "description": "Photo 1 Optional +AED 30"
   },
   "typesType": {
    "type": "string",
    "enum": [
     "mandatory",
     "optional",
     "choice",
     "conditional",
     "recommended"
    ],
    "description": "Vocabulary listed under Component Types."
   },
   "fixedQuantity": {
    "type": "integer",
    "description": "Fixed quantity"
   },
   "minimum": {
    "type": "string",
    "description": "Minimum"
   },
   "maximum": {
    "type": "string",
    "description": "Maximum"
   },
   "quantityBasedOnGuestCount": {
    "type": "integer",
    "description": "Quantity based on guest count"
   },
   "quantityBasedOnTicketCount": {
    "type": "integer",
    "description": "Quantity based on ticket count"
   }
  }
 },
 "BundleComponentBuilderView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Bundle Component Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "admissionTicket": {
    "type": "string",
    "description": "Admission ticket"
   },
   "attraction": {
    "type": "string",
    "description": "Attraction"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "timeslot": {
    "type": "string",
    "description": "Timeslot"
   },
   "experience": {
    "type": "string",
    "description": "Experience"
   },
   "membership": {
    "type": "string",
    "description": "Membership"
   },
   "annualPass": {
    "type": "string",
    "description": "Annual pass"
   },
   "fBProduct": {
    "type": "string",
    "description": "F&B product"
   },
   "fBMealPackage": {
    "type": "string",
    "description": "F&B meal package"
   },
   "retailProduct": {
    "type": "string",
    "description": "Retail product"
   },
   "parking": {
    "type": "string",
    "description": "Parking"
   },
   "locker": {
    "type": "string",
    "description": "Locker"
   },
   "photo": {
    "type": "string",
    "description": "Photo"
   },
   "rental": {
    "type": "string",
    "description": "Rental"
   },
   "voucher": {
    "type": "string",
    "description": "Voucher"
   },
   "giftCard": {
    "type": "string",
    "description": "Gift card"
   },
   "service": {
    "type": "string",
    "description": "Service"
   },
   "externalProduct": {
    "type": "string",
    "description": "External product"
   },
   "ntYEntTreatment": {
    "type": "string",
    "description": "nt y ent Treatment"
   },
   "photo1OptionalAed30": {
    "type": "string",
    "description": "Photo 1 Optional +AED 30"
   },
   "typesType": {
    "type": "string",
    "enum": [
     "mandatory",
     "optional",
     "choice",
     "conditional",
     "recommended"
    ],
    "description": "Vocabulary listed under Component Types."
   },
   "fixedQuantity": {
    "type": "integer",
    "description": "Fixed quantity"
   },
   "minimum": {
    "type": "string",
    "description": "Minimum"
   },
   "maximum": {
    "type": "string",
    "description": "Maximum"
   },
   "quantityBasedOnGuestCount": {
    "type": "integer",
    "description": "Quantity based on guest count"
   },
   "quantityBasedOnTicketCount": {
    "type": "integer",
    "description": "Quantity based on ticket count"
   }
  }
 },
 "BundleDefinitionSetupInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table covers these fields** — the closest is promotions.allocation_split at 5%, so this is not an update to anything the package stores today and no new table has been decided",
  "description": "**What Bundle Definition & Setup submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "bundleName": {
    "type": "string",
    "description": "Bundle name"
   },
   "bundleId": {
    "type": "string",
    "description": "Bundle ID"
   },
   "internalDescription": {
    "type": "string",
    "description": "Internal description"
   },
   "guestFacingDescription": {
    "type": "string",
    "description": "Guest-facing description"
   },
   "businessEntity": {
    "type": "string",
    "description": "Business entity"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "bundleCategory": {
    "type": "string",
    "description": "Bundle category"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   },
   "campaign": {
    "type": "string",
    "description": "Campaign"
   },
   "effectiveDates": {
    "type": "string",
    "description": "Effective dates"
   },
   "salesStatus": {
    "type": "string",
    "description": "Sales status"
   },
   "allComponentsPredefined": {
    "type": "string",
    "description": "All components predefined"
   },
   "requiredComponentsPlusOptionalChoices": {
    "type": "string",
    "description": "Required components plus optional choices"
   },
   "customerSelectsFromPermittedCategories": {
    "type": "string",
    "description": "Customer selects from permitted categories"
   },
   "chooseAny3Attractions": {
    "type": "string",
    "description": "Choose any 3 attractions"
   },
   "containsInternalAndExternalProducts": {
    "type": "string",
    "description": "Contains internal and external products"
   },
   "appearsAsStandaloneProduct": {
    "type": "string",
    "description": "Appears as standalone product"
   },
   "isRecommendedDuringCheckout": {
    "type": "boolean",
    "description": "Is recommended during checkout"
   },
   "requiresAnotherProduct": {
    "type": "string",
    "description": "Requires another product"
   }
  }
 },
 "BundleDefinitionSetupView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Bundle Definition & Setup displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "bundleName": {
    "type": "string",
    "description": "Bundle name"
   },
   "bundleId": {
    "type": "string",
    "description": "Bundle ID"
   },
   "internalDescription": {
    "type": "string",
    "description": "Internal description"
   },
   "guestFacingDescription": {
    "type": "string",
    "description": "Guest-facing description"
   },
   "businessEntity": {
    "type": "string",
    "description": "Business entity"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "bundleCategory": {
    "type": "string",
    "description": "Bundle category"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   },
   "campaign": {
    "type": "string",
    "description": "Campaign"
   },
   "effectiveDates": {
    "type": "string",
    "description": "Effective dates"
   },
   "salesStatus": {
    "type": "string",
    "description": "Sales status"
   },
   "allComponentsPredefined": {
    "type": "string",
    "description": "All components predefined"
   },
   "requiredComponentsPlusOptionalChoices": {
    "type": "string",
    "description": "Required components plus optional choices"
   },
   "customerSelectsFromPermittedCategories": {
    "type": "string",
    "description": "Customer selects from permitted categories"
   },
   "chooseAny3Attractions": {
    "type": "string",
    "description": "Choose any 3 attractions"
   },
   "containsInternalAndExternalProducts": {
    "type": "string",
    "description": "Contains internal and external products"
   },
   "appearsAsStandaloneProduct": {
    "type": "string",
    "description": "Appears as standalone product"
   },
   "isRecommendedDuringCheckout": {
    "type": "boolean",
    "description": "Is recommended during checkout"
   },
   "requiresAnotherProduct": {
    "type": "string",
    "description": "Requires another product"
   }
  }
 },
 "BundlePreviewSimulationAiRecommendationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table covers these fields** — the closest is promotions.bundle_component at 3%, so this is not an update to anything the package stores today and no new table has been decided",
  "description": "**What Bundle Preview, Simulation & AI Recommendation submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "guest": {
    "type": "string",
    "description": "Guest"
   },
   "segment": {
    "type": "string",
    "description": "Segment"
   },
   "products": {
    "type": "string",
    "description": "Products"
   },
   "quantity": {
    "type": "integer",
    "description": "Quantity"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "date": {
    "type": "string",
    "format": "date-time",
    "description": "Date"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "membership": {
    "type": "string",
    "description": "Membership"
   },
   "loyalty": {
    "type": "string",
    "description": "Loyalty"
   },
   "paymentType": {
    "type": "string",
    "description": "Payment type"
   },
   "promoCode": {
    "type": "string",
    "description": "Promo code"
   },
   "familySegment": {
    "type": "string",
    "description": "Family segment ✓"
   },
   "b2c": {
    "type": "string",
    "description": "B2C ✓"
   },
   "validDate": {
    "type": "string",
    "format": "date-time",
    "description": "Valid date ✓"
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
   "venueManager": {
    "type": "string",
    "description": "Venue Manager"
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
   },
   "changeDiscount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Change discount"
   },
   "changeThresholds": {
    "type": "string",
    "description": "Change thresholds"
   },
   "changeSegments": {
    "type": "string",
    "description": "Change segments"
   },
   "changeDates": {
    "type": "string",
    "description": "Change dates"
   },
   "currentPriceAndPricingFloors": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Current price and pricing floors"
   },
   "guestCustomerSegments": {
    "type": "string",
    "description": "Guest/customer segments"
   },
   "membershipAndTierEligibility": {
    "type": "string",
    "description": "Membership and tier eligibility"
   },
   "companySegmentsAndPartnerPricing": {
    "type": "string",
    "description": "Company segments and partner pricing"
   },
   "paymentMethodAndBankEligibility": {
    "type": "string",
    "description": "Payment-method and bank eligibility"
   },
   "productsEligibleForPromotionalRules": {
    "type": "string",
    "description": "Products eligible for promotional rules"
   },
   "revenueMarginAndDiscountExposure": {
    "type": "number",
    "description": "Revenue, margin and discount exposure"
   }
  }
 },
 "BundlePreviewSimulationAiRecommendationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Bundle Preview, Simulation & AI Recommendation displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "guest": {
    "type": "string",
    "description": "Guest"
   },
   "segment": {
    "type": "string",
    "description": "Segment"
   },
   "products": {
    "type": "string",
    "description": "Products"
   },
   "quantity": {
    "type": "integer",
    "description": "Quantity"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "date": {
    "type": "string",
    "format": "date-time",
    "description": "Date"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "membership": {
    "type": "string",
    "description": "Membership"
   },
   "loyalty": {
    "type": "string",
    "description": "Loyalty"
   },
   "paymentType": {
    "type": "string",
    "description": "Payment type"
   },
   "promoCode": {
    "type": "string",
    "description": "Promo code"
   },
   "discount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Discount (the pack shows 15% / AED 90)"
   },
   "familySegment": {
    "type": "string",
    "description": "Family segment ✓"
   },
   "b2c": {
    "type": "string",
    "description": "B2C ✓"
   },
   "validDate": {
    "type": "string",
    "format": "date-time",
    "description": "Valid date ✓"
   },
   "rule421Qualified": {
    "type": "string",
    "description": "Rule 421 qualified"
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
   "venueManager": {
    "type": "string",
    "description": "Venue Manager"
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
   },
   "changeDiscount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Change discount"
   },
   "changeThresholds": {
    "type": "string",
    "description": "Change thresholds"
   },
   "changeSegments": {
    "type": "string",
    "description": "Change segments"
   },
   "changeDates": {
    "type": "string",
    "description": "Change dates"
   },
   "currentPriceAndPricingFloors": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Current price and pricing floors"
   },
   "guestCustomerSegments": {
    "type": "string",
    "description": "Guest/customer segments"
   },
   "membershipAndTierEligibility": {
    "type": "string",
    "description": "Membership and tier eligibility"
   },
   "companySegmentsAndPartnerPricing": {
    "type": "string",
    "description": "Company segments and partner pricing"
   },
   "paymentMethodAndBankEligibility": {
    "type": "string",
    "description": "Payment-method and bank eligibility"
   },
   "productsEligibleForPromotionalRules": {
    "type": "string",
    "description": "Products eligible for promotional rules"
   },
   "revenueMarginAndDiscountExposure": {
    "type": "number",
    "description": "Revenue, margin and discount exposure"
   }
  }
 },
 "BundlePricingCommercialModelView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Bundle Pricing & Commercial Model displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "bundleDiscount15": {
    "type": "number",
    "description": "Bundle discount 15%"
   },
   "eachComponentRetainsConfiguredPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Each component retains configured price"
   },
   "calculatedThroughTicvaiSPricingEngine": {
    "type": "string",
    "description": "Calculated through TICVAI's pricing engine"
   },
   "basePrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Base price"
   },
   "currency": {
    "type": "string",
    "description": "Currency"
   },
   "discount": {
    "type": "number",
    "description": "Discount %"
   },
   "discountAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Discount amount"
   },
   "minimumPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Minimum price"
   },
   "maximumPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Maximum price"
   },
   "priceFloor": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price floor"
   },
   "marginFloor": {
    "type": "number",
    "description": "Margin floor"
   },
   "guestSpecificPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Guest-specific price"
   },
   "channelSpecificPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Channel-specific price"
   },
   "aed30": {
    "type": "string",
    "description": "+AED 30"
   }
  }
 },
 "BundleValiditySchedulingRedemptionRulesView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Bundle Validity, Scheduling & Redemption Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "valid1June31August": {
    "type": "string",
    "description": "Valid 1 June–31 August"
   },
   "allComponentsTogether": {
    "type": "string",
    "description": "All components together"
   },
   "independentRedemption": {
    "type": "string",
    "description": "Independent redemption"
   },
   "sequentialRedemption": {
    "type": "string",
    "description": "Sequential redemption"
   },
   "firstUseActivation": {
    "type": "string",
    "description": "First-use activation"
   },
   "scheduledRedemption": {
    "type": "string",
    "format": "date-time",
    "description": "Scheduled redemption"
   },
   "timeslotReservationRequired": {
    "type": "boolean",
    "description": "Timeslot reservation required"
   },
   "ownValidity": {
    "type": "string",
    "description": "Own validity"
   },
   "ownCapacity": {
    "type": "integer",
    "description": "Own capacity"
   },
   "ownTimeslot": {
    "type": "string",
    "description": "Own timeslot"
   },
   "ownRedemptionCount": {
    "type": "integer",
    "description": "Own redemption count"
   },
   "ownEntitlement": {
    "type": "string",
    "description": "Own entitlement"
   },
   "ownAccessRule": {
    "type": "string",
    "description": "Own access rule"
   }
  }
 },
 "GuestChoiceBuildYourOwnBundleDesignerInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Guest Choice & Build-Your-Own Bundle Designer submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.\n\n**The pack defines this as a record**, under *For each group* - one of only 13 drafted writes that does. That is the client writing a row rather than a screen, and it is where the table conversation should start.",
  "properties": {
   "waterPark": {
    "type": "string",
    "description": "Water Park"
   },
   "aquarium": {
    "type": "string",
    "description": "Aquarium"
   },
   "observationDeck": {
    "type": "string",
    "description": "Observation Deck"
   },
   "museum": {
    "type": "string",
    "description": "Museum"
   },
   "adventurePark": {
    "type": "string",
    "description": "Adventure Park"
   },
   "mealA": {
    "type": "string",
    "description": "Meal A"
   },
   "mealB": {
    "type": "string",
    "description": "Meal B"
   },
   "mealC": {
    "type": "string",
    "description": "Meal C"
   },
   "photo": {
    "type": "string",
    "description": "Photo"
   },
   "locker": {
    "type": "string",
    "description": "Locker"
   },
   "parking": {
    "type": "string",
    "description": "Parking"
   },
   "groupName": {
    "type": "string",
    "description": "Group name"
   },
   "category": {
    "type": "string",
    "description": "Category"
   },
   "minimumSelections": {
    "type": "string",
    "description": "Minimum selections"
   },
   "maximumSelections": {
    "type": "string",
    "description": "Maximum selections"
   },
   "requiredOptional": {
    "type": "string",
    "description": "Required/optional"
   },
   "eligibleProducts": {
    "type": "string",
    "description": "Eligible products"
   },
   "additionalCharge": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Additional charge"
   },
   "selectionOrder": {
    "type": "string",
    "description": "Selection order"
   }
  },
  "x-ticvai-record-definition": "For each group"
 },
 "GuestChoiceBuildYourOwnBundleDesignerView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Guest Choice & Build-Your-Own Bundle Designer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "waterPark": {
    "type": "string",
    "description": "Water Park"
   },
   "aquarium": {
    "type": "string",
    "description": "Aquarium"
   },
   "observationDeck": {
    "type": "string",
    "description": "Observation Deck"
   },
   "museum": {
    "type": "string",
    "description": "Museum"
   },
   "adventurePark": {
    "type": "string",
    "description": "Adventure Park"
   },
   "mealA": {
    "type": "string",
    "description": "Meal A"
   },
   "mealB": {
    "type": "string",
    "description": "Meal B"
   },
   "mealC": {
    "type": "string",
    "description": "Meal C"
   },
   "photo": {
    "type": "string",
    "description": "Photo"
   },
   "locker": {
    "type": "string",
    "description": "Locker"
   },
   "parking": {
    "type": "string",
    "description": "Parking"
   },
   "groupName": {
    "type": "string",
    "description": "Group name"
   },
   "category": {
    "type": "string",
    "description": "Category"
   },
   "minimumSelections": {
    "type": "string",
    "description": "Minimum selections"
   },
   "maximumSelections": {
    "type": "string",
    "description": "Maximum selections"
   },
   "requiredOptional": {
    "type": "string",
    "description": "Required/optional"
   },
   "eligibleProducts": {
    "type": "string",
    "description": "Eligible products"
   },
   "additionalCharge": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Additional charge"
   },
   "selectionOrder": {
    "type": "string",
    "description": "Selection order"
   }
  }
 },
 "PartnerExternalProductBundleManagerView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Partner & External Product Bundle Manager displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "partner": {
    "type": "string",
    "description": "Partner"
   },
   "externalProductId": {
    "type": "string",
    "description": "External product ID"
   },
   "productName": {
    "type": "string",
    "description": "Product name"
   },
   "apiSource": {
    "type": "string",
    "description": "API source"
   },
   "availabilitySource": {
    "type": "string",
    "description": "Availability source"
   },
   "externalPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "External price"
   },
   "ticvaiSellingPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "TICVAI selling price"
   },
   "commission": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Commission"
   },
   "settlementRule": {
    "type": "string",
    "description": "Settlement rule"
   },
   "cancellationRule": {
    "type": "string",
    "description": "Cancellation rule"
   },
   "redemptionMethod": {
    "type": "string",
    "description": "Redemption method"
   },
   "connected": {
    "type": "string",
    "description": "Connected"
   },
   "available": {
    "type": "string",
    "description": "Available"
   },
   "degraded": {
    "type": "string",
    "description": "Degraded"
   },
   "apiError": {
    "type": "string",
    "description": "API Error"
   },
   "productUnavailable": {
    "type": "string",
    "description": "Product unavailable"
   },
   "mappingError": {
    "type": "string",
    "description": "Mapping error"
   },
   "ticvaiWaterPark": {
    "type": "string",
    "description": "TICVAI Water Park"
   },
   "externalHotelNight": {
    "type": "string",
    "description": "External Hotel Night"
   },
   "externalDesertSafari": {
    "type": "string",
    "description": "External Desert Safari"
   },
   "ticvaiMealVoucher": {
    "type": "string",
    "description": "TICVAI Meal Voucher"
   },
   "soldAsOneCommercialPackage": {
    "type": "string",
    "description": "sold as one commercial package"
   }
  }
 },
 "RevenueAllocationCostSettlementRulesView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Revenue Allocation, Cost & Settlement Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "on": {
    "type": "string",
    "description": "on"
   },
   "fixedAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Fixed amount"
   },
   "percentage": {
    "type": "number",
    "description": "Percentage"
   },
   "proportionalListPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Proportional list price"
   },
   "weightedAllocation": {
    "type": "string",
    "description": "Weighted allocation"
   },
   "costPlus": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Cost-plus"
   },
   "contractualPartnerAllocation": {
    "type": "string",
    "description": "Contractual partner allocation"
   },
   "redemptionBasedAllocation": {
    "type": "string",
    "description": "Redemption-based allocation"
   },
   "revenueAccount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue account"
   },
   "department": {
    "type": "string",
    "description": "Department"
   },
   "costCenter": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Cost center"
   },
   "legalEntity": {
    "type": "string",
    "description": "Legal entity"
   },
   "taxTreatment": {
    "type": "string",
    "description": "Tax treatment"
   },
   "partnerPayable": {
    "type": "string",
    "description": "Partner payable"
   },
   "commission": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Commission"
   },
   "settlementCycle": {
    "type": "string",
    "description": "Settlement cycle"
   },
   "fullRefund": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Full refund"
   },
   "partialRefund": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Partial refund"
   },
   "componentRefund": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Component refund"
   },
   "unredeemedComponentRefund": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Unredeemed component refund"
   }
  }
 }
}
```
