# WS50 — Promotions   Bundles Management board 6

**10 screens · 10 operations · 10 schemas · 1 permissions**

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

- **Every control that can be refused must be gated.** 1 permissions apply here:
  `PRICE_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **0 of these operations work offline**
  
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-188` | Dynamic Bundle Operations Command Center | commandCentre | 1 | 0 | — |
| `ADM-189` | Component Inventory & Availability Matrix | listDetail | 1 | 0 | — |
| `ADM-190` | Bundle Sellability & Dependency Rule Engine | listDetail | 1 | 0 | — |
| `ADM-191` | Capacity Pool & Reservation Manager | configEditor | 1 | 0 | — |
| `ADM-192` | Dynamic Component Substitution Engine | configEditor | 1 | 0 | — |
| `ADM-193` | Dynamic Bundle Rule & Composition Engine | listDetail | 1 | 0 | — |
| `ADM-194` | Real-Time Availability & Checkout Validation | configEditor | 1 | 0 | — |
| `ADM-195` | Bundle Availability by Channel, Venue & Partner | configEditor | 1 | 0 | — |
| `ADM-196` | Bundle Availability Forecast, Alerts & Recovery | listDetail | 1 | 0 | — |
| `ADM-197` | Dynamic Bundle Simulation & AI Optimization | listDetail | 1 | 0 | — |

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
     "carries": [
      "tenantId"
     ],
     "provenance": "derived — ADM-002 declares entryState.params tenantId, so an edge into it must carry them"
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
    "operationId": "listDynamicBundle",
    "contract": "promotions",
    "purpose": "Dynamic Bundle Operations Command Center",
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-188"
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
   }
  ],
  "entryState": {
   "preloaded": [
    "ComponentInventoryAvailabilityMatrixView.tRyTyLe",
    "ComponentInventoryAvailabilityMatrixView.dE",
    "ComponentInventoryAvailabilityMatrixView.souvenir0Open",
    "ComponentInventoryAvailabilityMatrixView.ticketInventory",
    "ComponentInventoryAvailabilityMatrixView.attractionCapacity"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-189"
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
    "BundleSellabilityDependencyRuleEngineView.allComponentsRequired",
    "BundleSellabilityDependencyRuleEngineView.atLeastXOfY",
    "BundleSellabilityDependencyRuleEngineView.atLeastOneFromCategory",
    "BundleSellabilityDependencyRuleEngineView.optionalComponent",
    "BundleSellabilityDependencyRuleEngineView.conditionalComponent"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-190"
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
  "gaps": [
   {
    "operation": null,
    "why": "**Capacity Pool & Reservation Manager declares no operation that writes anything** — its only declared call is `listCapacityPoolReservation`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
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
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-191"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 81. 0 of 0 labels bound to a contract property; 7 of 26 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-192"
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-193"
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-194"
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
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-195"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 85. 0 of 0 labels bound to a contract property; 5 of 23 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-196"
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-197"
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
  "parameters": [],
  "requestBody": null,
  "responds": "BundleAvailabilityForecastAlertsRecoveryView"
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
  "parameters": [],
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
   "eEE": {
    "type": "string",
    "description": "e e e"
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
 "BundleSellabilityDependencyRuleEngineView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Bundle Sellability & Dependency Rule Engine displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "allComponentsRequired": {
    "type": "boolean",
    "description": "All components required"
   },
   "atLeastXOfY": {
    "type": "string",
    "description": "At least X of Y"
   },
   "atLeastOneFromCategory": {
    "type": "string",
    "description": "At least one from category"
   },
   "optionalComponent": {
    "type": "string",
    "description": "Optional component"
   },
   "conditionalComponent": {
    "type": "string",
    "description": "Conditional component"
   },
   "substituteAllowed": {
    "type": "boolean",
    "description": "Substitute allowed"
   },
   "partnerComponentRequired": {
    "type": "boolean",
    "description": "Partner component required"
   },
   "waterParkMandatory": {
    "type": "string",
    "description": "Water Park — Mandatory"
   },
   "aquariumMandatory": {
    "type": "string",
    "description": "Aquarium — Mandatory"
   },
   "photoOptional": {
    "type": "string",
    "description": "Photo — Optional"
   }
  }
 },
 "CapacityPoolReservationManagerView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Capacity Pool & Reservation Manager displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "aquariumRemainingCapacity": {
    "type": "integer",
    "description": "Aquarium remaining capacity (the pack shows 100)"
   },
   "standaloneSales": {
    "type": "integer",
    "description": "Standalone sales (the pack shows 60)"
   },
   "held": {
    "type": "string",
    "description": "Held (the pack shows 5)"
   },
   "remainingSellable": {
    "type": "string",
    "description": "Remaining sellable (the pack shows 10)"
   },
   "sharedPool": {
    "type": "string",
    "description": "Shared pool"
   },
   "dedicatedBundleAllocation": {
    "type": "string",
    "description": "Dedicated bundle allocation"
   },
   "channelAllocation": {
    "type": "string",
    "description": "Channel allocation"
   },
   "partnerAllocation": {
    "type": "string",
    "description": "Partner allocation"
   },
   "eventCapacity": {
    "type": "integer",
    "description": "Event capacity"
   },
   "timeslotCapacity": {
    "type": "integer",
    "description": "Timeslot capacity"
   },
   "seatInventory": {
    "type": "string",
    "description": "Seat inventory"
   },
   "resourceCapacity": {
    "type": "integer",
    "description": "Resource capacity"
   },
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
   "capacityAutomaticallyReleased": {
    "type": "integer",
    "description": "Capacity automatically released"
   }
  }
 },
 "ComponentInventoryAvailabilityMatrixView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Component Inventory & Availability Matrix displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "tRyTyLe": {
    "type": "string",
    "description": "t ry ty le"
   },
   "dE": {
    "type": "string",
    "description": "d e"
   },
   "souvenir0Open": {
    "type": "integer",
    "description": "Souvenir 0 — Open"
   },
   "ticketInventory": {
    "type": "string",
    "description": "Ticket inventory"
   },
   "attractionCapacity": {
    "type": "integer",
    "description": "Attraction capacity"
   },
   "eventCapacity": {
    "type": "integer",
    "description": "Event capacity"
   },
   "seatInventory": {
    "type": "string",
    "description": "Seat inventory"
   },
   "timeslots": {
    "type": "string",
    "description": "Timeslots"
   },
   "fBAvailability": {
    "type": "string",
    "description": "F&B availability"
   },
   "retailStock": {
    "type": "string",
    "description": "Retail stock"
   },
   "resourceAvailability": {
    "type": "string",
    "description": "Resource availability"
   },
   "parking": {
    "type": "string",
    "description": "Parking"
   },
   "rental": {
    "type": "string",
    "description": "Rental"
   },
   "externalPartnerApi": {
    "type": "string",
    "description": "External partner API"
   },
   "available": {
    "type": "string",
    "description": "Available"
   },
   "limited": {
    "type": "string",
    "description": "Limited"
   },
   "low": {
    "type": "string",
    "description": "Low"
   },
   "soldOut": {
    "type": "string",
    "description": "Sold Out"
   },
   "closed": {
    "type": "integer",
    "description": "Closed"
   },
   "suspended": {
    "type": "string",
    "description": "Suspended"
   },
   "unpublished": {
    "type": "string",
    "description": "Unpublished"
   },
   "apiUnavailable": {
    "type": "string",
    "description": "API Unavailable"
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
   "healthy": {
    "type": "string",
    "description": "Healthy"
   },
   "warning": {
    "type": "string",
    "description": "Warning"
   },
   "critical": {
    "type": "string",
    "description": "Critical"
   },
   "unavailable": {
    "type": "string",
    "description": "Unavailable"
   },
   "waterParkAvailable": {
    "type": "string",
    "description": "Water Park — Available"
   },
   "aquariumAvailable": {
    "type": "string",
    "description": "Aquarium — Available"
   },
   "familyMealLowStock": {
    "type": "string",
    "description": "Family Meal — Low Stock"
   },
   "photoAvailable": {
    "type": "string",
    "description": "Photo — Available"
   },
   "bundleHealthWarning": {
    "type": "string",
    "description": "Bundle Health: WARNING"
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
   "aquariumUnavailable": {
    "type": "string",
    "description": "Aquarium unavailable"
   },
   "aquariumRequiredSubstituteAllowed": {
    "type": "boolean",
    "description": "Aquarium required → Substitute allowed"
   },
   "observationDeckAvailable": {
    "type": "string",
    "description": "Observation Deck available"
   },
   "aed20": {
    "type": "string",
    "description": "+AED 20"
   },
   "customerApprovalRequired": {
    "type": "boolean",
    "description": "Customer approval required"
   },
   "bundleRemainsSellable": {
    "type": "string",
    "description": "Bundle remains sellable"
   },
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
   },
   "beforeRecommendingSubstitutions": {
    "type": "string",
    "description": "before recommending substitutions"
   },
   "level1RecommendOnly": {
    "type": "string",
    "description": "Level 1 — Recommend Only"
   },
   "humanApproves": {
    "type": "string",
    "description": "Human approves"
   },
   "level2PreApprovedAutomation": {
    "type": "string",
    "description": "Level 2 — Pre-Approved Automation"
   },
   "productStatusAndInventory": {
    "type": "string",
    "description": "Product status and inventory"
   },
   "attractionEventCapacity": {
    "type": "integer",
    "description": "Attraction/event capacity"
   },
   "seatAvailabilityWhereIncluded": {
    "type": "string",
    "description": "Seat availability where included"
   },
   "resourceAvailability": {
    "type": "string",
    "description": "Resource availability"
   },
   "menuAvailability": {
    "type": "string",
    "description": "Menu availability"
   },
   "physicalInventory": {
    "type": "string",
    "description": "Physical inventory"
   },
   "membershipBasedComponents": {
    "type": "string",
    "description": "Membership-based components"
   },
   "entitlementRedemptionState": {
    "type": "string",
    "description": "Entitlement/redemption state"
   },
   "realTimePricing": {
    "type": "string",
    "format": "date-time",
    "description": "Real-time pricing"
   },
   "promotionQualification": {
    "type": "string",
    "description": "Promotion qualification"
   },
   "checkoutPaymentCoordination": {
    "type": "string",
    "description": "Checkout/payment coordination"
   },
   "partnerAllocation": {
    "type": "string",
    "description": "Partner allocation"
   },
   "externalAvailability": {
    "type": "string",
    "description": "External availability"
   },
   "commercialImpact": {
    "type": "string",
    "description": "Commercial impact"
   },
   "whatIsTheBundle": {
    "type": "string",
    "description": "WHAT IS THE BUNDLE?"
   },
   "change": {
    "type": "string",
    "description": "CHANGE?"
   },
   "matrixCoverageBoard6": {
    "type": "string",
    "description": "Matrix Coverage — Board 6"
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
   "soldOut": {
    "type": "string",
    "description": "Sold out"
   },
   "capacityExhausted": {
    "type": "integer",
    "description": "Capacity exhausted"
   },
   "productSuspended": {
    "type": "string",
    "description": "Product suspended"
   },
   "venueClosed": {
    "type": "integer",
    "description": "Venue closed"
   },
   "externalApiUnavailable": {
    "type": "string",
    "description": "External API unavailable"
   },
   "inventoryBelowThreshold": {
    "type": "integer",
    "description": "Inventory below threshold"
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
   }
  }
 },
 "RealTimeAvailabilityCheckoutValidationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Real-Time Availability & Checkout Validation displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "productActive": {
    "type": "integer",
    "description": "Product active"
   },
   "inventoryAvailable": {
    "type": "string",
    "description": "Inventory available"
   },
   "capacityAvailable": {
    "type": "integer",
    "description": "Capacity available"
   },
   "timeslotAvailable": {
    "type": "string",
    "description": "Timeslot available"
   },
   "resourceAvailable": {
    "type": "string",
    "description": "Resource available"
   },
   "priceValid": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price valid"
   },
   "promotionValid": {
    "type": "string",
    "description": "Promotion valid"
   },
   "partnerComponentValid": {
    "type": "string",
    "description": "Partner component valid"
   },
   "componentMappingValid": {
    "type": "string",
    "description": "Component mapping valid"
   }
  }
 }
}
```
