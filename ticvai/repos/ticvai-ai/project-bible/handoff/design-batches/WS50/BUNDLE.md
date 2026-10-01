# WS50 — Promotions   Bundles Management board 6

**10 screens · 13 operations · 14 schemas · 3 permissions**

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
| `ADM-188` | Dynamic Bundle Operations Command Center | commandCentre | 3 | 0 | — |
| `ADM-189` | Component Inventory & Availability Matrix | listDetail | 2 | 0 | — |
| `ADM-190` | Bundle Sellability & Dependency Rule Engine | listDetail | 1 | 0 | — |
| `ADM-191` | Capacity Pool & Reservation Manager | configEditor | 3 | 1 | — |
| `ADM-192` | Dynamic Component Substitution Engine | configEditor | 1 | 0 | — |
| `ADM-193` | Dynamic Bundle Rule & Composition Engine | listDetail | 1 | 0 | — |
| `ADM-194` | Real-Time Availability & Checkout Validation | configEditor | 1 | 0 | — |
| `ADM-195` | Bundle Availability by Channel, Venue & Partner | configEditor | 3 | 1 | — |
| `ADM-196` | Bundle Availability Forecast, Alerts & Recovery | listDetail | 1 | 0 | — |
| `ADM-197` | Dynamic Bundle Simulation & AI Optimization | listDetail | 3 | 0 | — |

## Thin screens in this batch

**ADM-189, ADM-190, ADM-193, ADM-194, ADM-196, ADM-197 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-188",
  "name": "Dynamic Bundle Operations Command Center",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "6",
   "number": "1",
   "page": 78
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/dynamic-bundle-operations-command-center-adm-188",
   "component": "apps/ticvai-web/src/routes/commercial/DynamicBundleOperationsCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-189",
    "ADM-190",
    "ADM-191",
    "ADM-192",
    "ADM-193",
    "ADM-194",
    "ADM-195",
    "ADM-196",
    "ADM-197"
   ],
   "inferred": false,
   "notes": "**The board's hub.** The workshop specified this module as boards of ten and opened each with a command centre; the other nine screens are that board's detail, so they are reached from here and return here.",
   "transitions": [
    {
     "to": "ADM-002",
     "trigger": "Platform Dashboard",
     "provenance": "derived — ADM-002 declares entryState.params  and ADM-188 holds none of them. The edge carries nothing: ADM-188 is opened from ADM-002, so this edge is the way back and ADM-002 keeps its own state"
    },
    {
     "to": "ADM-189",
     "trigger": "Works in Component Inventory & Availability Matrix",
     "provenance": "flow F159 step 1→2",
     "operation": "listDynamicBundle"
    },
    {
     "to": "ADM-190",
     "trigger": "Works in Bundle Sellability & Dependency Rule Engine",
     "provenance": "flow F159 step 3→4",
     "operation": "listDynamicBundle"
    },
    {
     "to": "ADM-191",
     "trigger": "Works in Capacity Pool & Reservation Manager",
     "provenance": "flow F159 step 5→6",
     "operation": "listDynamicBundle"
    },
    {
     "to": "ADM-192",
     "trigger": "Works in Dynamic Component Substitution Engine",
     "provenance": "flow F159 step 7→8",
     "operation": "listDynamicBundle"
    },
    {
     "to": "ADM-193",
     "trigger": "Works in Dynamic Bundle Rule & Composition Engine",
     "provenance": "flow F159 step 9→10",
     "operation": "listDynamicBundle"
    },
    {
     "to": "ADM-194",
     "trigger": "Works in Real-Time Availability & Checkout Validation",
     "provenance": "flow F159 step 11→12",
     "operation": "listDynamicBundle"
    },
    {
     "to": "ADM-195",
     "trigger": "Works in Bundle Availability by Channel, Venue & Partner",
     "provenance": "flow F159 step 13→14",
     "operation": "listDynamicBundle"
    },
    {
     "to": "ADM-196",
     "trigger": "Works in Bundle Availability Forecast, Alerts & Recovery",
     "provenance": "flow F159 step 15→16",
     "operation": "listDynamicBundle"
    },
    {
     "to": "ADM-197",
     "trigger": "Works in Dynamic Bundle Simulation & AI Optimization",
     "provenance": "flow F159 step 17→18",
     "operation": "listDynamicBundle"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide real-time visibility into the operational health of all active bundles.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Active Dynamic Bundles",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 78 §KPI Cards",
       "bindsTo": "DynamicBundleOperationsCommandCenterView.activeDynamicBundles"
      },
      {
       "kind": "metricTile",
       "label": "Sellable Bundles",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 78 §KPI Cards",
       "bindsTo": "DynamicBundleOperationsCommandCenterView.sellableBundles"
      },
      {
       "kind": "metricTile",
       "label": "Partially Available Bundles",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 78 §KPI Cards",
       "bindsTo": "DynamicBundleOperationsCommandCenterView.partiallyAvailableBundles"
      },
      {
       "kind": "metricTile",
       "label": "Unavailable Bundles",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 78 §KPI Cards",
       "bindsTo": "DynamicBundleOperationsCommandCenterView.unavailableBundles"
      },
      {
       "kind": "metricTile",
       "label": "Bundles with Low Capacity",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 78 §KPI Cards",
       "bindsTo": "DynamicBundleOperationsCommandCenterView.bundlesWithLowCapacity"
      },
      {
       "kind": "metricTile",
       "label": "Components Sold Out",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 78 §KPI Cards",
       "bindsTo": "DynamicBundleOperationsCommandCenterView.componentsSoldOut"
      },
      {
       "kind": "metricTile",
       "label": "Substitutions Triggered",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 78 §KPI Cards",
       "bindsTo": "DynamicBundleOperationsCommandCenterView.substitutionsTriggered"
      },
      {
       "kind": "metricTile",
       "label": "Bundle Sales Today",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 78 §KPI Cards",
       "bindsTo": "DynamicBundleOperationsCommandCenterView.bundleSalesToday"
      },
      {
       "kind": "metricTile",
       "label": "Failed Bundle Attempts",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 78 §KPI Cards",
       "bindsTo": "DynamicBundleOperationsCommandCenterView.failedBundleAttempts"
      },
      {
       "kind": "metricTile",
       "label": "Capacity Reserved",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 78 §KPI Cards",
       "bindsTo": "DynamicBundleOperationsCommandCenterView.capacityReserved"
      },
      {
       "kind": "metricTile",
       "label": "Revenue at Risk",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 78 §KPI Cards",
       "bindsTo": "DynamicBundleOperationsCommandCenterView.revenueAtRisk"
      },
      {
       "kind": "metricTile",
       "label": "Recovered Revenue",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 78 §KPI Cards",
       "bindsTo": "DynamicBundleOperationsCommandCenterView.recoveredRevenue"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The dynamic bundle operations list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the dynamic bundle operations untouched.",
   "emptyFirstRun": "No dynamic bundle operations yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the dynamic bundle operations are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listDynamicBundle2",
    "contract": "promotions",
    "purpose": "Dynamic Bundle Simulation & AI Optimization",
    "trigger": "onLoad"
   },
   {
    "operationId": "listDynamicBundle",
    "contract": "promotions",
    "purpose": "Dynamic Bundle Operations Command Center",
    "trigger": "onLoad"
   },
   {
    "operationId": "listDynamicBundleRule",
    "contract": "promotions",
    "purpose": "Dynamic Bundle Rule & Composition Engine",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "DynamicBundleOperationsCommandCenterView.activeDynamicBundles",
    "DynamicBundleOperationsCommandCenterView.sellableBundles",
    "DynamicBundleOperationsCommandCenterView.partiallyAvailableBundles",
    "DynamicBundleOperationsCommandCenterView.unavailableBundles",
    "DynamicBundleOperationsCommandCenterView.bundlesWithLowCapacity",
    "DynamicBundleOperationsCommandCenterView.componentsSoldOut"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-188",
   "workshopBoard": "wireframes/WS111 Promotions   Bundles Management Board 6.dc.html#adm-188"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 78. 12 of 12 labels bound to a contract property; 12 of 26 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-189",
  "name": "Component Inventory & Availability Matrix",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "6",
   "number": "2",
   "page": 79
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/component-inventory-availability-matrix-adm-189",
   "component": "apps/ticvai-web/src/routes/commercial/ComponentInventoryAvailabilityMatrix.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-188"
   ],
   "exitTo": [
    "ADM-188"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-188, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-188",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F159 step 2→3",
     "operation": "listComponentInventoryAvailability"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide one centralized matrix showing availability for every component within every active bundle.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 79"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 79"
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
       "impliedBy": "listComponentInventoryAvailability",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "detailPanel",
       "derived": true,
       "impliedBy": "getInventoryKitDefinition",
       "notes": "One record, read-only."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The component inventory availability list.",
   "error": "Could not load. Names which read failed and leaves the component inventory availability untouched.",
   "emptyFirstRun": "No component inventory availability yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the component inventory availability are still there. The pack's own statuses are t ry ty le — the state names which is selected.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listComponentInventoryAvailability",
    "contract": "promotions",
    "purpose": "Component Inventory & Availability Matrix",
    "trigger": "onLoad"
   },
   {
    "operationId": "getInventoryKitDefinition",
    "contract": "inventory",
    "purpose": "Show kit components",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "ComponentInventoryAvailabilityMatrixView.availabilitySource"
   ],
   "params": [
    {
     "name": "itemId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-189",
   "workshopBoard": "wireframes/WS111 Promotions   Bundles Management Board 6.dc.html#adm-189"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 79. 0 of 0 labels bound to a contract property; 1 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-190",
  "name": "Bundle Sellability & Dependency Rule Engine",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "6",
   "number": "3",
   "page": 80
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/bundle-sellability-dependency-rule-engine-adm-190",
   "component": "apps/ticvai-web/src/routes/commercial/BundleSellabilityDependencyRuleEngine.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-188"
   ],
   "exitTo": [
    "ADM-188"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-188, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-188",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F159 step 4→5",
     "operation": "listBundleSellabilityDependency"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Determine whether the overall bundle can be sold based on the state of its underlying components.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Partner component required. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 80 §Support"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 80"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 80"
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
       "label": "Partner component required",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 80 §Support"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listBundleSellabilityDependency",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The bundle sellability dependency list.",
   "error": "Could not load. Names which read failed and leaves the bundle sellability dependency untouched.",
   "emptyFirstRun": "No bundle sellability dependency yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the bundle sellability dependency are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listBundleSellabilityDependency",
    "contract": "promotions",
    "purpose": "Bundle Sellability & Dependency Rule Engine",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "BundleSellabilityDependencyRuleEngineView.dependencyRule"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-190",
   "workshopBoard": "wireframes/WS111 Promotions   Bundles Management Board 6.dc.html#adm-190"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 80. 0 of 0 labels bound to a contract property; 1 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-191",
  "name": "Capacity Pool & Reservation Manager",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "6",
   "number": "4",
   "page": 81
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/capacity-pool-reservation-manager-adm-191",
   "component": "apps/ticvai-web/src/routes/commercial/CapacityPoolReservationManager.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-188"
   ],
   "exitTo": [
    "ADM-188"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-188, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-188",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F159 step 6→7",
     "operation": "listCapacityPoolReservation"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Manage how bundle sales consume capacity from underlying products. This is particularly important because a bundle must not create artificial inventory separate from the actual attraction/product capacity.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Temporary reservation",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 81 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Hold duration",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 81 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Release timeout",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 81 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Hard allocation",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 81 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Soft allocation",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 81 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Overbooking policy",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 81 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Waitlist behavior",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 81 §Configure"
      },
      {
       "kind": "dataTable",
       "label": "Every bundle capacity policy",
       "bindsTo": "BundleCapacityPolicy",
       "columns": [
        "BundleCapacityPolicy.id",
        "BundleCapacityPolicy.bundleId",
        "BundleCapacityPolicy.channel",
        "BundleCapacityPolicy.venueId",
        "BundleCapacityPolicy.partnerId",
        "BundleCapacityPolicy.capacitySource",
        "BundleCapacityPolicy.allocationMode",
        "BundleCapacityPolicy.capacityCeiling",
        "BundleCapacityPolicy.holdDurationMinutes",
        "BundleCapacityPolicy.bookingCutoffMinutes",
        "BundleCapacityPolicy.allowOverbooking",
        "BundleCapacityPolicy.allowWaitlist"
       ],
       "operation": "listBundleCapacityPolicies",
       "provenance": "contract promotions.yaml GET /bundles/{bundleId}/capacity-policies"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save bundle capacity policy",
       "operation": "setBundleCapacityPolicy",
       "permission": "PRODUCT_CONFIGURE",
       "notes": "Replaces the bundle's `promotions.bundle_capacity_policy` rows with the set sent: a row sent with an `id` is updated, one without is created, and a stored row not sent is removed.",
       "provenance": "contract promotions.yaml PUT /bundles/{bundleId}/capacity-policies"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The capacity pool reservation configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the capacity pool reservation untouched.",
   "emptyFirstRun": "No capacity pool reservation configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCapacityPoolReservation",
    "contract": "promotions",
    "purpose": "Capacity Pool & Reservation Manager",
    "trigger": "onLoad"
   },
   {
    "operationId": "listBundleCapacityPolicies",
    "contract": "promotions",
    "purpose": "List a bundle's capacity policies",
    "trigger": "onLoad"
   },
   {
    "operationId": "setBundleCapacityPolicy",
    "contract": "promotions",
    "purpose": "Set a bundle's capacity policies",
    "trigger": "onAction",
    "invalidates": [
     "listCapacityPoolReservation",
     "listBundleCapacityPolicies"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-191",
   "workshopBoard": "wireframes/WS111 Promotions   Bundles Management Board 6.dc.html#adm-191"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 81. 0 of 0 labels bound to a contract property; 7 of 26 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "bundleId",
     "from": "navigation"
    }
   ]
  },
  "overlays": [
   {
    "id": "formSetBundleCapacityPolicy",
    "component": "modal",
    "trigger": "Save bundle capacity policy",
    "body": "**Collects what `setBundleCapacityPolicy` sends before it is called.** Required: `policies`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save bundle capacity policy",
     "operation": "setBundleCapacityPolicy"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "policies"
     ]
    },
    "provenance": "contract promotions.yaml PUT /bundles/{bundleId}/capacity-policies"
   }
  ],
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
  "id": "ADM-192",
  "name": "Dynamic Component Substitution Engine",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "6",
   "number": "5",
   "page": 82
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/dynamic-component-substitution-engine-adm-192",
   "component": "apps/ticvai-web/src/routes/commercial/DynamicComponentSubstitutionEngine.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-188"
   ],
   "exitTo": [
    "ADM-188"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-188, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-188",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F159 step 8→9",
     "operation": "listDynamicComponentSubstitution"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§For each component define; Define whether substitute) and no display directory — it is settings, not a population",
  "purpose": "Automatically replace unavailable bundle components according to predefined commercial rules.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Primary component",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 82 §For each component define"
      },
      {
       "kind": "selectField",
       "label": "Alternative 1",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 82 §For each component define"
      },
      {
       "kind": "selectField",
       "label": "Alternative 2",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 82 §For each component define"
      },
      {
       "kind": "selectField",
       "label": "Alternative 3",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 82 §For each component define"
      },
      {
       "kind": "selectField",
       "label": "Fallback action",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 82 §For each component define"
      },
      {
       "kind": "textField",
       "label": "Maintains same bundle price",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 82 §Define whether substitute"
      },
      {
       "kind": "selectField",
       "label": "Adds surcharge",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 82 §Define whether substitute"
      },
      {
       "kind": "selectField",
       "label": "Reduces bundle price",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 82 §Define whether substitute"
      },
      {
       "kind": "selectField",
       "label": "Requires customer approval",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 82 §Define whether substitute"
      },
      {
       "kind": "selectField",
       "label": "Requires operator approval",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 82 §Define whether substitute"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The dynamic component substitution configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the dynamic component substitution untouched.",
   "emptyFirstRun": "No dynamic component substitution configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listDynamicComponentSubstitution",
    "contract": "promotions",
    "purpose": "Dynamic Component Substitution Engine",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-192",
   "workshopBoard": "wireframes/WS111 Promotions   Bundles Management Board 6.dc.html#adm-192"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 82. 0 of 0 labels bound to a contract property; 10 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-193",
  "name": "Dynamic Bundle Rule & Composition Engine",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "6",
   "number": "6",
   "page": 83
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/dynamic-bundle-rule-composition-engine-adm-193",
   "component": "apps/ticvai-web/src/routes/commercial/DynamicBundleRuleCompositionEngine.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-188"
   ],
   "exitTo": [
    "ADM-188"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-188, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-188",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F159 step 10→11",
     "operation": "listDynamicBundleRule"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow the actual composition of a bundle to change dynamically according to business and guest conditions. This builds upon the matrix requirement for dynamic bundles where guests select attractions, experiences, F&B, Retail, or services from predefined categories.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 83"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 83"
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
       "impliedBy": "listDynamicBundleRule",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The dynamic bundle rule list.",
   "error": "Could not load. Names which read failed and leaves the dynamic bundle rule untouched.",
   "emptyFirstRun": "No dynamic bundle rule yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the dynamic bundle rule are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listDynamicBundleRule",
    "contract": "promotions",
    "purpose": "Dynamic Bundle Rule & Composition Engine",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "DynamicBundleRuleCompositionEngineView.guestSegment",
    "DynamicBundleRuleCompositionEngineView.membership",
    "DynamicBundleRuleCompositionEngineView.loyaltyTier",
    "DynamicBundleRuleCompositionEngineView.purchaseHistory",
    "DynamicBundleRuleCompositionEngineView.numberOfGuests"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-193",
   "workshopBoard": "wireframes/WS111 Promotions   Bundles Management Board 6.dc.html#adm-193"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 83. 0 of 0 labels bound to a contract property; 0 of 27 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-194",
  "name": "Real-Time Availability & Checkout Validation",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "6",
   "number": "7",
   "page": 84
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/real-time-availability-checkout-validation-adm-194",
   "component": "apps/ticvai-web/src/routes/commercial/RealTimeAvailabilityCheckoutValidation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-188"
   ],
   "exitTo": [
    "ADM-188"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-188, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-188",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F159 step 12→13",
     "operation": "listRealTimeAvailability"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Payment authorization/capture) and no display directory — it is settings, not a population",
  "purpose": "Perform the final authoritative validation immediately before transaction confirmation. This is essential because availability may change between browsing and payment.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "↓",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 84 §Payment authorization/capture"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listRealTimeAvailability",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The real-time availability checkout configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the real-time availability checkout untouched.",
   "emptyFirstRun": "No real-time availability checkout configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listRealTimeAvailability",
    "contract": "promotions",
    "purpose": "Real-Time Availability & Checkout Validation",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-194",
   "workshopBoard": "wireframes/WS111 Promotions   Bundles Management Board 6.dc.html#adm-194"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 84. 0 of 0 labels bound to a contract property; 1 of 27 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-195",
  "name": "Bundle Availability by Channel, Venue & Partner",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "6",
   "number": "8",
   "page": 85
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/bundle-availability-by-channel-venue-partner-adm-195",
   "component": "apps/ticvai-web/src/routes/commercial/BundleAvailabilityByChannelVenuePartner.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-188"
   ],
   "exitTo": [
    "ADM-188"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-188, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-188",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F159 step 14→15",
     "operation": "listBundleAvailabilityChannel"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Control where a bundle is sellable based on operational availability.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Venue-specific availability",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 85 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Attraction-specific availability",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 85 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Operating area",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 85 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Country/market",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 85 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Sales location",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 85 §Configure"
      },
      {
       "kind": "dataTable",
       "label": "Every bundle capacity policy",
       "bindsTo": "BundleCapacityPolicy",
       "columns": [
        "BundleCapacityPolicy.id",
        "BundleCapacityPolicy.bundleId",
        "BundleCapacityPolicy.channel",
        "BundleCapacityPolicy.venueId",
        "BundleCapacityPolicy.partnerId",
        "BundleCapacityPolicy.capacitySource",
        "BundleCapacityPolicy.allocationMode",
        "BundleCapacityPolicy.capacityCeiling",
        "BundleCapacityPolicy.holdDurationMinutes",
        "BundleCapacityPolicy.bookingCutoffMinutes",
        "BundleCapacityPolicy.allowOverbooking",
        "BundleCapacityPolicy.allowWaitlist"
       ],
       "operation": "listBundleCapacityPolicies",
       "provenance": "contract promotions.yaml GET /bundles/{bundleId}/capacity-policies"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save bundle capacity policy",
       "operation": "setBundleCapacityPolicy",
       "permission": "PRODUCT_CONFIGURE",
       "notes": "Replaces the bundle's `promotions.bundle_capacity_policy` rows with the set sent: a row sent with an `id` is updated, one without is created, and a stored row not sent is removed.",
       "provenance": "contract promotions.yaml PUT /bundles/{bundleId}/capacity-policies"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The bundle availability channel configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the bundle availability channel untouched.",
   "emptyFirstRun": "No bundle availability channel configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listBundleAvailabilityChannel",
    "contract": "promotions",
    "purpose": "Bundle Availability by Channel, Venue & Partner",
    "trigger": "onLoad"
   },
   {
    "operationId": "listBundleCapacityPolicies",
    "contract": "promotions",
    "purpose": "List a bundle's capacity policies",
    "trigger": "onLoad"
   },
   {
    "operationId": "setBundleCapacityPolicy",
    "contract": "promotions",
    "purpose": "Set a bundle's capacity policies",
    "trigger": "onAction",
    "invalidates": [
     "listBundleAvailabilityChannel",
     "listBundleCapacityPolicies"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-195",
   "workshopBoard": "wireframes/WS111 Promotions   Bundles Management Board 6.dc.html#adm-195"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 85. 0 of 0 labels bound to a contract property; 5 of 23 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "bundleId",
     "from": "navigation"
    }
   ]
  },
  "overlays": [
   {
    "id": "formSetBundleCapacityPolicy",
    "component": "modal",
    "trigger": "Save bundle capacity policy",
    "body": "**Collects what `setBundleCapacityPolicy` sends before it is called.** Required: `policies`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save bundle capacity policy",
     "operation": "setBundleCapacityPolicy"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "policies"
     ]
    },
    "provenance": "contract promotions.yaml PUT /bundles/{bundleId}/capacity-policies"
   }
  ],
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
  "id": "ADM-196",
  "name": "Bundle Availability Forecast, Alerts & Recovery",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "6",
   "number": "9",
   "page": 86
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/bundle-availability-forecast-alerts-recovery-adm-196",
   "component": "apps/ticvai-web/src/routes/commercial/BundleAvailabilityForecastAlertsRecovery.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-188"
   ],
   "exitTo": [
    "ADM-188"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-188, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-188",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F159 step 16→17",
     "operation": "listBundleAvailabilityForecast"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Analyze) and no metric row",
  "purpose": "Predict bundle availability problems before they affect sales.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every bundle availability forecast",
       "columns": [
        "BundleAvailabilityForecastAlertsRecoveryView.historicalDemand",
        "BundleAvailabilityForecastAlertsRecoveryView.currentBookingVelocity",
        "BundleAvailabilityForecastAlertsRecoveryView.inventory",
        "BundleAvailabilityForecastAlertsRecoveryView.capacity",
        "BundleAvailabilityForecastAlertsRecoveryView.timeslotUtilization",
        "BundleAvailabilityForecastAlertsRecoveryView.seasonality",
        "BundleAvailabilityForecastAlertsRecoveryView.dayOfWeek",
        "BundleAvailabilityForecastAlertsRecoveryView.campaignActivity",
        "BundleAvailabilityForecastAlertsRecoveryView.partnerReservations"
       ],
       "bindsTo": "BundleAvailabilityForecastAlertsRecoveryView",
       "operation": "listBundleAvailabilityForecast",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 86 §Analyze"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected bundle availability forecast",
       "bindsTo": "BundleAvailabilityForecastAlertsRecoveryView",
       "columns": [
        "BundleAvailabilityForecastAlertsRecoveryView.historicalDemand",
        "BundleAvailabilityForecastAlertsRecoveryView.currentBookingVelocity",
        "BundleAvailabilityForecastAlertsRecoveryView.inventory",
        "BundleAvailabilityForecastAlertsRecoveryView.capacity",
        "BundleAvailabilityForecastAlertsRecoveryView.timeslotUtilization",
        "BundleAvailabilityForecastAlertsRecoveryView.seasonality",
        "BundleAvailabilityForecastAlertsRecoveryView.dayOfWeek",
        "BundleAvailabilityForecastAlertsRecoveryView.campaignActivity",
        "BundleAvailabilityForecastAlertsRecoveryView.partnerReservations"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Alert Levels”, “AED 186,500”.",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 86 §Analyze"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The bundle availability forecast list.",
   "error": "Could not load. Names which read failed and leaves the bundle availability forecast untouched.",
   "emptyFirstRun": "No bundle availability forecast yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the bundle availability forecast are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listBundleAvailabilityForecast",
    "contract": "promotions",
    "purpose": "Bundle Availability Forecast, Alerts & Recovery",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "BundleAvailabilityForecastAlertsRecoveryView.historicalDemand",
    "BundleAvailabilityForecastAlertsRecoveryView.currentBookingVelocity",
    "BundleAvailabilityForecastAlertsRecoveryView.inventory",
    "BundleAvailabilityForecastAlertsRecoveryView.capacity",
    "BundleAvailabilityForecastAlertsRecoveryView.timeslotUtilization",
    "BundleAvailabilityForecastAlertsRecoveryView.seasonality"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-196",
   "workshopBoard": "wireframes/WS111 Promotions   Bundles Management Board 6.dc.html#adm-196"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 86. 9 of 9 labels bound to a contract property; 9 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-197",
  "name": "Dynamic Bundle Simulation & AI Optimization",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "6",
   "number": "10",
   "page": 87
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/dynamic-bundle-simulation-ai-optimization-adm-197",
   "component": "apps/ticvai-web/src/routes/commercial/DynamicBundleSimulationAiOptimization.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-188"
   ],
   "exitTo": [
    "ADM-188"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-188, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation."
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Test how a bundle behaves under different operational scenarios before activating dynamic rules.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every dynamic bundle simulation",
       "columns": [
        "DynamicBundleSimulationAiOptimizationView.bundleStatus",
        "DynamicBundleSimulationAiOptimizationView.componentsSelected",
        "DynamicBundleSimulationAiOptimizationView.substitutions",
        "DynamicBundleSimulationAiOptimizationView.priceImpact",
        "DynamicBundleSimulationAiOptimizationView.marginImpact",
        "DynamicBundleSimulationAiOptimizationView.capacityImpact",
        "DynamicBundleSimulationAiOptimizationView.customerImpact",
        "DynamicBundleSimulationAiOptimizationView.revenueImpact"
       ],
       "bindsTo": "DynamicBundleSimulationAiOptimizationView",
       "operation": "listDynamicBundle2",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 87 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected dynamic bundle simulation",
       "bindsTo": "DynamicBundleSimulationAiOptimizationView",
       "columns": [
        "DynamicBundleSimulationAiOptimizationView.bundleStatus",
        "DynamicBundleSimulationAiOptimizationView.componentsSelected",
        "DynamicBundleSimulationAiOptimizationView.substitutions",
        "DynamicBundleSimulationAiOptimizationView.priceImpact",
        "DynamicBundleSimulationAiOptimizationView.marginImpact",
        "DynamicBundleSimulationAiOptimizationView.capacityImpact",
        "DynamicBundleSimulationAiOptimizationView.customerImpact",
        "DynamicBundleSimulationAiOptimizationView.revenueImpact"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Scenario A”, “Scenario B”, “Scenario C”, “Scenario D”, “Scenario E”, “Photo”.",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 87 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The dynamic bundle simulation list.",
   "error": "Could not load. Names which read failed and leaves the dynamic bundle simulation untouched.",
   "emptyFirstRun": "No dynamic bundle simulation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the dynamic bundle simulation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listDynamicBundle2",
    "contract": "promotions",
    "purpose": "Dynamic Bundle Simulation & AI Optimization",
    "trigger": "onLoad"
   },
   {
    "operationId": "listDynamicBundle",
    "contract": "promotions",
    "purpose": "Dynamic Bundle Operations Command Center",
    "trigger": "onLoad"
   },
   {
    "operationId": "listDynamicBundleRule",
    "contract": "promotions",
    "purpose": "Dynamic Bundle Rule & Composition Engine",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "DynamicBundleSimulationAiOptimizationView.bundleStatus",
    "DynamicBundleSimulationAiOptimizationView.componentsSelected",
    "DynamicBundleSimulationAiOptimizationView.substitutions",
    "DynamicBundleSimulationAiOptimizationView.priceImpact",
    "DynamicBundleSimulationAiOptimizationView.marginImpact",
    "DynamicBundleSimulationAiOptimizationView.capacityImpact"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-197",
   "workshopBoard": "wireframes/WS111 Promotions   Bundles Management Board 6.dc.html#adm-197"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 87. 8 of 8 labels bound to a contract property; 9 of 87 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "getInventoryKitDefinition": {
  "method": "GET",
  "path": "/inventory-items/{itemId}/kit-definition",
  "contract": "inventory",
  "summary": "The components a kit item is made of",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "InventoryKitDefinition"
 },
 "listBundleAvailabilityChannel": {
  "method": "GET",
  "path": "/bundle-availability-channel",
  "contract": "promotions",
  "summary": "Bundle Availability by Channel, Venue & Partner",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "BundleAvailabilityByChannelVenuePartnerView"
 },
 "listBundleAvailabilityForecast": {
  "method": "GET",
  "path": "/bundle-availability-forecast",
  "contract": "promotions",
  "summary": "Bundle Availability Forecast, Alerts & Recovery",
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
  "responds": "BundleAvailabilityForecastAlertsRecoveryView"
 },
 "listBundleCapacityPolicies": {
  "method": "GET",
  "path": "/bundles/{bundleId}/capacity-policies",
  "contract": "promotions",
  "summary": "List a bundle's capacity policies",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
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
  "requestBody": null,
  "responds": "Page"
 },
 "listBundleSellabilityDependency": {
  "method": "GET",
  "path": "/bundle-sellability-dependency",
  "contract": "promotions",
  "summary": "Bundle Sellability & Dependency Rule Engine",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "BundleSellabilityDependencyRuleEngineView"
 },
 "listCapacityPoolReservation": {
  "method": "GET",
  "path": "/capacity-pool-reservation",
  "contract": "promotions",
  "summary": "Capacity Pool & Reservation Manager",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "CapacityPoolReservationManagerView"
 },
 "listComponentInventoryAvailability": {
  "method": "GET",
  "path": "/component-inventory-availability",
  "contract": "promotions",
  "summary": "Component Inventory & Availability Matrix",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ComponentInventoryAvailabilityMatrixView"
 },
 "listDynamicBundle": {
  "method": "GET",
  "path": "/dynamic-bundle",
  "contract": "promotions",
  "summary": "Dynamic Bundle Operations Command Center",
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
  "responds": "DynamicBundleOperationsCommandCenterView"
 },
 "listDynamicBundle2": {
  "method": "GET",
  "path": "/dynamic-bundle-2",
  "contract": "promotions",
  "summary": "Dynamic Bundle Simulation & AI Optimization",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "DynamicBundleSimulationAiOptimizationView"
 },
 "listDynamicBundleRule": {
  "method": "GET",
  "path": "/dynamic-bundle-rule",
  "contract": "promotions",
  "summary": "Dynamic Bundle Rule & Composition Engine",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "DynamicBundleRuleCompositionEngineView"
 },
 "listDynamicComponentSubstitution": {
  "method": "GET",
  "path": "/dynamic-component-substitution",
  "contract": "promotions",
  "summary": "Dynamic Component Substitution Engine",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "DynamicComponentSubstitutionEngineView"
 },
 "listRealTimeAvailability": {
  "method": "GET",
  "path": "/real-time-availability",
  "contract": "promotions",
  "summary": "Real-Time Availability & Checkout Validation",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "RealTimeAvailabilityCheckoutValidationView"
 },
 "setBundleCapacityPolicy": {
  "method": "PUT",
  "path": "/bundles/{bundleId}/capacity-policies",
  "contract": "promotions",
  "summary": "Set a bundle's capacity policies",
  "permission": "PRODUCT_CONFIGURE",
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
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "BundleAvailabilityByChannelVenuePartnerView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Bundle Availability by Channel, Venue & Partner displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "channelsType": {
    "type": "string",
    "enum": [
     "b2c",
     "b2b",
     "pos",
     "mobilePos",
     "mobileApp",
     "kiosk",
     "callCenter",
     "api",
     "ota",
     "reseller",
     "partner"
    ],
    "description": "Vocabulary listed under Channels."
   },
   "venueSpecificAvailability": {
    "type": "string",
    "description": "Venue-specific availability"
   },
   "attractionSpecificAvailability": {
    "type": "string",
    "description": "Attraction-specific availability"
   },
   "operatingArea": {
    "type": "string",
    "description": "Operating area"
   },
   "countryMarket": {
    "type": "string",
    "description": "Country/market"
   },
   "salesLocation": {
    "type": "string",
    "description": "Sales location"
   },
   "dedicatedAllocation": {
    "type": "string",
    "description": "Dedicated allocation"
   },
   "sharedAllocation": {
    "type": "string",
    "description": "Shared allocation"
   },
   "capacityCeiling": {
    "type": "integer",
    "description": "Capacity ceiling"
   },
   "bookingCutoff": {
    "type": "string",
    "description": "Booking cutoff"
   }
  }
 },
 "BundleAvailabilityForecastAlertsRecoveryView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Bundle Availability Forecast, Alerts & Recovery displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "historicalDemand": {
    "type": "string",
    "description": "Historical demand"
   },
   "currentBookingVelocity": {
    "type": "string",
    "description": "Current booking velocity"
   },
   "inventory": {
    "type": "string",
    "description": "Inventory"
   },
   "capacity": {
    "type": "integer",
    "description": "Capacity"
   },
   "timeslotUtilization": {
    "type": "number",
    "description": "Timeslot utilization"
   },
   "seasonality": {
    "type": "string",
    "description": "Seasonality"
   },
   "dayOfWeek": {
    "type": "string",
    "description": "Day of week"
   },
   "campaignActivity": {
    "type": "string",
    "description": "Campaign activity"
   },
   "partnerReservations": {
    "type": "string",
    "description": "Partner reservations"
   },
   "levelsType": {
    "type": "string",
    "enum": [
     "information",
     "warning",
     "critical"
    ],
    "description": "Vocabulary listed under Alert Levels."
   },
   "switchChoiceGroup": {
    "type": "string",
    "description": "Switch choice group"
   },
   "restrictChannel": {
    "type": "string",
    "description": "Restrict channel"
   },
   "reduceBundleAllocation": {
    "type": "string",
    "description": "Reduce bundle allocation"
   },
   "increaseAlternativeInventory": {
    "type": "string",
    "description": "Increase alternative inventory"
   },
   "recommendAnotherTimeslot": {
    "type": "string",
    "description": "Recommend another timeslot"
   },
   "potentialRevenueRecoverableThroughSubstitution": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Potential Revenue Recoverable Through Substitution"
   }
  }
 },
 "BundleCapacityPolicy": {
  "x-ticvai-persistence": "promotions.bundle_capacity_policy",
  "type": "object",
  "description": "How a bundle draws on capacity, per channel where it differs: the capacity source, dedicated or shared and hard or soft allocation, the ceiling, how long a hold lasts, the booking cut-off, and whether overbooking or a waitlist is allowed (Capacity Pool & Reservation Manager; Bundle Availability by Channel, Venue & Partner). The capacity itself is the catalogue's (`catalogue.channel_capacity`, `catalogue.inventory_hold`). A row with no channel is the bundle's default. (DM5, 29 September: data model for the agreed operations)\n**Written by setBundleCapacityPolicy; read by listBundleCapacityPolicies, listCapacityPoolReservation and listBundleAvailabilityChannel** (decided 29 September, writers pass).",
  "required": [
   "id",
   "bundleId",
   "capacitySource"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "bundleId": {
    "type": "string",
    "format": "uuid"
   },
   "channel": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/SalesChannel"
     }
    ],
    "nullable": true
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Where the policy differs by venue for a multi-venue bundle."
   },
   "partnerId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "capacitySource": {
    "type": "string",
    "enum": [
     "sharedPool",
     "dedicatedBundleAllocation",
     "channelAllocation",
     "partnerAllocation",
     "eventCapacity",
     "timeslotCapacity",
     "seatInventory",
     "resourceCapacity"
    ]
   },
   "allocationMode": {
    "type": "string",
    "enum": [
     "hard",
     "soft"
    ],
    "default": "hard",
    "description": "Hard allocation is ring-fenced for the bundle; soft is released back when unsold."
   },
   "capacityCeiling": {
    "type": "integer",
    "minimum": 0,
    "nullable": true
   },
   "holdDurationMinutes": {
    "type": "integer",
    "minimum": 1,
    "nullable": true,
    "description": "How long a temporary reservation of the components lasts."
   },
   "bookingCutoffMinutes": {
    "type": "integer",
    "minimum": 0,
    "nullable": true,
    "description": "Minutes before the experience after which the bundle is no longer sold."
   },
   "allowOverbooking": {
    "type": "boolean",
    "default": false
   },
   "allowWaitlist": {
    "type": "boolean",
    "default": false
   }
  }
 },
 "BundleSellabilityDependencyRuleEngineView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Bundle Sellability & Dependency Rule Engine displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "dependencyRule": {
    "type": "string",
    "enum": [
     "allComponentsRequired",
     "atLeastXOfY",
     "atLeastOneFromCategory",
     "optionalComponent",
     "conditionalComponent",
     "substituteAllowed",
     "partnerComponentRequired"
    ],
    "description": "The sellability rule."
   },
   "bundleId": {
    "type": "string",
    "description": "Bundle ID"
   },
   "componentIds": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Components the rule covers"
   },
   "minimumCount": {
    "type": "integer",
    "description": "For atLeastXOfY: X"
   }
  }
 },
 "CapacityPoolReservationManagerView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Capacity Pool & Reservation Manager displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "temporaryReservation": {
    "type": "string",
    "description": "Temporary reservation"
   },
   "holdDuration": {
    "type": "string",
    "format": "date-time",
    "description": "Hold duration"
   },
   "hardAllocation": {
    "type": "string",
    "description": "Hard allocation"
   },
   "softAllocation": {
    "type": "string",
    "description": "Soft allocation"
   },
   "overbookingPolicy": {
    "type": "string",
    "description": "Overbooking policy"
   },
   "waitlistBehavior": {
    "type": "string",
    "description": "Waitlist behavior"
   },
   "capacitySource": {
    "type": "string",
    "enum": [
     "sharedPool",
     "dedicatedBundleAllocation",
     "channelAllocation",
     "partnerAllocation",
     "eventCapacity",
     "timeslotCapacity",
     "seatInventory",
     "resourceCapacity"
    ],
    "description": "Capacity source."
   }
  }
 },
 "ComponentInventoryAvailabilityMatrixView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Component Inventory & Availability Matrix displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "availabilitySource": {
    "type": "string",
    "enum": [
     "ticketInventory",
     "attractionCapacity",
     "eventCapacity",
     "seatInventory",
     "timeslots",
     "fBAvailability",
     "retailStock",
     "resourceAvailability",
     "parking",
     "rental",
     "externalPartnerApi"
    ],
    "description": "Where the component's availability comes from."
   },
   "componentStatus": {
    "type": "string",
    "enum": [
     "available",
     "limited",
     "low",
     "soldOut",
     "closed",
     "suspended",
     "unpublished",
     "apiUnavailable"
    ],
    "description": "Component status."
   },
   "componentId": {
    "type": "string",
    "description": "Component ID"
   },
   "componentName": {
    "type": "string",
    "description": "Component"
   },
   "inventory": {
    "type": "integer",
    "description": "Inventory"
   },
   "capacity": {
    "type": "integer",
    "description": "Capacity"
   },
   "schedule": {
    "type": "string",
    "description": "Schedule"
   }
  }
 },
 "DynamicBundleOperationsCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Dynamic Bundle Operations Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "activeDynamicBundles": {
    "type": "integer",
    "description": "Active Dynamic Bundles"
   },
   "sellableBundles": {
    "type": "integer",
    "description": "Sellable Bundles"
   },
   "partiallyAvailableBundles": {
    "type": "integer",
    "description": "Partially Available Bundles"
   },
   "unavailableBundles": {
    "type": "integer",
    "description": "Unavailable Bundles"
   },
   "bundlesWithLowCapacity": {
    "type": "integer",
    "description": "Bundles with Low Capacity"
   },
   "componentsSoldOut": {
    "type": "string",
    "description": "Components Sold Out"
   },
   "substitutionsTriggered": {
    "type": "string",
    "description": "Substitutions Triggered"
   },
   "bundleSalesToday": {
    "type": "string",
    "description": "Bundle Sales Today"
   },
   "failedBundleAttempts": {
    "type": "integer",
    "description": "Failed Bundle Attempts"
   },
   "capacityReserved": {
    "type": "integer",
    "description": "Capacity Reserved"
   },
   "revenueAtRisk": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue at Risk"
   },
   "recoveredRevenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Recovered Revenue"
   },
   "unavailable": {
    "type": "string",
    "description": "Unavailable"
   },
   "health": {
    "type": "string",
    "enum": [
     "healthy",
     "warning",
     "critical"
    ],
    "description": "Bundle health."
   }
  }
 },
 "DynamicBundleRuleCompositionEngineView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Dynamic Bundle Rule & Composition Engine displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "guestSegment": {
    "type": "string",
    "description": "Guest segment"
   },
   "membership": {
    "type": "string",
    "description": "Membership"
   },
   "loyaltyTier": {
    "type": "string",
    "description": "Loyalty tier"
   },
   "purchaseHistory": {
    "type": "string",
    "description": "Purchase history"
   },
   "numberOfGuests": {
    "type": "integer",
    "description": "Number of guests"
   },
   "guestType": {
    "type": "string",
    "description": "Guest type"
   },
   "salesChannel": {
    "type": "string",
    "description": "Sales channel"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "season": {
    "type": "string",
    "description": "Season"
   },
   "day": {
    "type": "string",
    "description": "Day"
   },
   "time": {
    "type": "string",
    "format": "date-time",
    "description": "Time"
   },
   "capacity": {
    "type": "integer",
    "description": "Capacity"
   },
   "inventory": {
    "type": "string",
    "description": "Inventory"
   },
   "campaign": {
    "type": "string",
    "description": "Campaign"
   },
   "productPopularity": {
    "type": "string",
    "description": "Product popularity"
   }
  }
 },
 "DynamicBundleSimulationAiOptimizationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Dynamic Bundle Simulation & AI Optimization displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "bundleStatus": {
    "type": "integer",
    "description": "Bundle status"
   },
   "componentsSelected": {
    "type": "string",
    "description": "Components selected"
   },
   "substitutions": {
    "type": "integer",
    "description": "Substitutions"
   },
   "priceImpact": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price impact"
   },
   "marginImpact": {
    "type": "number",
    "description": "Margin impact"
   },
   "capacityImpact": {
    "type": "integer",
    "description": "Capacity impact"
   },
   "customerImpact": {
    "type": "string",
    "description": "Customer impact"
   },
   "revenueImpact": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue impact"
   }
  }
 },
 "DynamicComponentSubstitutionEngineView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Dynamic Component Substitution Engine displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "primaryComponent": {
    "type": "string",
    "description": "Primary component"
   },
   "alternative1": {
    "type": "string",
    "description": "Alternative 1"
   },
   "alternative2": {
    "type": "string",
    "description": "Alternative 2"
   },
   "alternative3": {
    "type": "string",
    "description": "Alternative 3"
   },
   "fallbackAction": {
    "type": "string",
    "description": "Fallback action"
   },
   "maintainsSameBundlePrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Maintains same bundle price"
   },
   "addsSurcharge": {
    "type": "string",
    "description": "Adds surcharge"
   },
   "reducesBundlePrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Reduces bundle price"
   },
   "requiresCustomerApproval": {
    "type": "string",
    "description": "Requires customer approval"
   },
   "requiresOperatorApproval": {
    "type": "string",
    "description": "Requires operator approval"
   },
   "substitutionTriggers": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "soldOut",
      "capacityExhausted",
      "productSuspended",
      "venueClosed",
      "externalApiUnavailable",
      "inventoryBelowThreshold"
     ]
    },
    "description": "When substitution may occur."
   }
  }
 },
 "InventoryKitComponent": {
  "x-ticvai-persistence": "inventory.kit_component",
  "type": "object",
  "description": "4.4.20. One component of a kit and the quantity one kit consumes.",
  "required": [
   "componentItemId",
   "quantity"
  ],
  "properties": {
   "kitItemId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "componentItemId": {
    "type": "string",
    "format": "uuid"
   },
   "quantity": {
    "type": "number",
    "exclusiveMinimum": 0
   },
   "unit": {
    "type": "string",
    "nullable": true,
    "description": "The component's base unit where omitted."
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Written at the kit item's venue scope."
   }
  }
 },
 "InventoryKitDefinition": {
  "x-ticvai-persistence": "none — composed of the item's inventory.kit_component rows",
  "type": "object",
  "description": "4.4.20. Also the `setInventoryKitDefinition` body.",
  "required": [
   "components"
  ],
  "properties": {
   "kitItemId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "components": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/InventoryKitComponent"
    }
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
 "RealTimeAvailabilityCheckoutValidationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Real-Time Availability & Checkout Validation displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "failedChecks": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "productInactive",
      "inventoryUnavailable",
      "capacityUnavailable",
      "timeslotUnavailable",
      "resourceUnavailable",
      "priceInvalid",
      "promotionInvalid",
      "partnerComponentInvalid",
      "componentMappingInvalid"
     ]
    },
    "description": "Checkout validations that failed; empty means the bundle is sellable."
   },
   "bundleId": {
    "type": "string",
    "description": "Bundle ID"
   },
   "sellable": {
    "type": "boolean",
    "description": "Whether the bundle can be sold now"
   }
  }
 }
}
```
