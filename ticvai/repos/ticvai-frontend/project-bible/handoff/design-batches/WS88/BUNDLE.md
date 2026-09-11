# WS88 — Rental Management board 1

**10 screens · 0 operations · 0 schemas · 0 permissions**

Platform P08 Venue Management · ships as **venue-management** ·
staff audience · web ·
online only

## Who this is for

**staff on web.** Everything below is how you know what is
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
| `BO-494` | Rental Product Command Center | commandCentre | 0 | 0 | — |
| `BO-495` | Create Rental Product Wizard | listDetail | 0 | 0 | — |
| `BO-496` | Rental Product Profile | listDetail | 0 | 0 | — |
| `BO-497` | Rental Category & Classification Setup | listDetail | 0 | 0 | — |
| `BO-498` | Inventory Tracking Model | configEditor | 0 | 0 | — |
| `BO-499` | Rental Location Assignment | listDetail | 0 | 0 | — |
| `BO-500` | Rental Duration & Turnaround Configuration | configEditor | 0 | 0 | — |
| `BO-501` | Rental Rules & Operational Policy | listDetail | 0 | 0 | — |
| `BO-502` | Customer Requirements, Agreement & Waiver | configEditor | 0 | 0 | — |
| `BO-503` | Product Validation, Approval & Publication | configEditor | 0 | 0 | — |

## Thin screens in this batch

**BO-495, BO-496, BO-497, BO-499, BO-501 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-494",
  "name": "Rental Product Command Center",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "1",
   "number": "1",
   "page": 6
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/rental-product-command-center-bo-494",
   "component": "apps/venue-management-web/src/routes/rentals/RentalProductCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-495",
    "BO-496",
    "BO-497",
    "BO-498",
    "BO-499",
    "BO-500",
    "BO-501",
    "BO-502",
    "BO-503"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 1 wiring, 11 September 2026",
     "back": true
    },
    {
     "to": "BO-495",
     "trigger": "Create Rental Product Wizard",
     "provenance": "structural — pack board 1 wiring, 11 September 2026"
    },
    {
     "to": "BO-496",
     "trigger": "Rental Product Profile",
     "provenance": "structural — pack board 1 wiring, 11 September 2026"
    },
    {
     "to": "BO-497",
     "trigger": "Rental Category & Classification Setup",
     "provenance": "structural — pack board 1 wiring, 11 September 2026"
    },
    {
     "to": "BO-498",
     "trigger": "Inventory Tracking Model",
     "provenance": "structural — pack board 1 wiring, 11 September 2026"
    },
    {
     "to": "BO-499",
     "trigger": "Rental Location Assignment",
     "provenance": "structural — pack board 1 wiring, 11 September 2026"
    },
    {
     "to": "BO-500",
     "trigger": "Rental Duration & Turnaround Configuration",
     "provenance": "structural — pack board 1 wiring, 11 September 2026"
    },
    {
     "to": "BO-501",
     "trigger": "Rental Rules & Operational Policy",
     "provenance": "structural — pack board 1 wiring, 11 September 2026"
    },
    {
     "to": "BO-502",
     "trigger": "Customer Requirements, Agreement & Waiver",
     "provenance": "structural — pack board 1 wiring, 11 September 2026"
    },
    {
     "to": "BO-503",
     "trigger": "Product Validation, Approval & Publication",
     "provenance": "structural — pack board 1 wiring, 11 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Display configurable KPI cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Central management screen for all rental products across tenants, venues and rental locations.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 0 operations.** Unserved: + Create Rental Product. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Rental_Management.pdf, page 6 §Actions"
   }
  ],
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search rental product",
       "provenance": "pack Rental_Management.pdf, page 6 §Support filters by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Tenant",
        "Venue",
        "Rental location",
        "Category",
        "Product status",
        "Tracking model",
        "Availability status",
        "Season",
        "Configuration status"
       ],
       "notes": "The pack filters this screen by tenant, venue, rental location, category, product status, tracking model and 3 more — which are present is a decision the pack already made.",
       "provenance": "pack Rental_Management.pdf, page 6 §Support filters by"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Total Rental Products",
       "provenance": "pack Rental_Management.pdf, page 6 §Display configurable KPI cards"
      },
      {
       "kind": "metricTile",
       "label": "Active Products",
       "provenance": "pack Rental_Management.pdf, page 6 §Display configurable KPI cards"
      },
      {
       "kind": "metricTile",
       "label": "Inactive Products",
       "provenance": "pack Rental_Management.pdf, page 6 §Display configurable KPI cards"
      },
      {
       "kind": "metricTile",
       "label": "Serialized Products",
       "provenance": "pack Rental_Management.pdf, page 6 §Display configurable KPI cards"
      },
      {
       "kind": "metricTile",
       "label": "Pooled Products",
       "provenance": "pack Rental_Management.pdf, page 6 §Display configurable KPI cards"
      },
      {
       "kind": "metricTile",
       "label": "Products Requiring Maintenance",
       "provenance": "pack Rental_Management.pdf, page 6 §Display configurable KPI cards"
      },
      {
       "kind": "metricTile",
       "label": "Products With Configuration Issues",
       "provenance": "pack Rental_Management.pdf, page 6 §Display configurable KPI cards"
      },
      {
       "kind": "metricTile",
       "label": "Products Awaiting Approval",
       "provenance": "pack Rental_Management.pdf, page 6 §Display configurable KPI cards"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "+ Create Rental Product",
       "provenance": "pack Rental_Management.pdf, page 6 §Actions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The rental product list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the rental product untouched.",
   "emptyFirstRun": "No rental product yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the rental product are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "entryState": {
   "preloaded": [
    "Total Rental Products",
    "Active Products",
    "Inactive Products",
    "Serialized Products",
    "Pooled Products",
    "Products Requiring Maintenance"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-494"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 6. 0 of 9 labels bound to a contract property; 18 of 29 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-495",
  "name": "Create Rental Product Wizard",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "1",
   "number": "2",
   "page": 8
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/create-rental-product-wizard-bo-495",
   "component": "apps/venue-management-web/src/routes/rentals/CreateRentalProductWizard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-494"
   ],
   "exitTo": [
    "BO-494"
   ],
   "transitions": [
    {
     "to": "BO-494",
     "trigger": "Back to Rental Product Command Center",
     "provenance": "structural — pack board 1 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Guided workflow for creating a new rental product.",
  "gaps": [
   {
    "operation": null,
    "why": "**Create Rental Product Wizard declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 8"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 8"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The create rental product list.",
   "error": "Could not load. Names which read failed and leaves the create rental product untouched.",
   "emptyFirstRun": "No create rental product yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the create rental product are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-495"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 8. 0 of 0 labels bound to a contract property; 0 of 27 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-496",
  "name": "Rental Product Profile",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "1",
   "number": "3",
   "page": 8
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/rental-product-profile-bo-496",
   "component": "apps/venue-management-web/src/routes/rentals/RentalProductProfile.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-494"
   ],
   "exitTo": [
    "BO-494"
   ],
   "transitions": [
    {
     "to": "BO-494",
     "trigger": "Back to Rental Product Command Center",
     "provenance": "structural — pack board 1 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Provide the complete master configuration of a rental product.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Rental_Management.pdf, page 8 §Show"
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
       "label": "Every rental product profile",
       "columns": [
        "Product name",
        "Code",
        "Category",
        "Description",
        "Images",
        "Tracking model",
        "Inventory quantity",
        "Rental locations",
        "Minimum duration",
        "Maximum duration",
        "Default turnaround time",
        "Rental agreement requirement",
        "Deposit requirement",
        "Current status"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Rental_Management.pdf, page 8 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected rental product profile",
       "bindsTo": null,
       "columns": [
        "Product name",
        "Code",
        "Category",
        "Description",
        "Images",
        "Tracking model",
        "Inventory quantity",
        "Rental locations",
        "Minimum duration",
        "Maximum duration",
        "Default turnaround time",
        "Rental agreement requirement",
        "Deposit requirement",
        "Current status"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Product Header”, “Display tabs”, “Missing”.",
       "provenance": "pack Rental_Management.pdf, page 8 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The rental product profile list.",
   "error": "Could not load. Names which read failed and leaves the rental product profile untouched.",
   "emptyFirstRun": "No rental product profile yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the rental product profile are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "entryState": {
   "preloaded": [
    "Product name",
    "Code",
    "Category",
    "Description",
    "Images",
    "Tracking model"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-496"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 8. 0 of 14 labels bound to a contract property; 14 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-497",
  "name": "Rental Category & Classification Setup",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "1",
   "number": "4",
   "page": 9
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/rental-category-classification-setup-bo-497",
   "component": "apps/venue-management-web/src/routes/rentals/RentalCategoryClassificationSetup.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-494"
   ],
   "exitTo": [
    "BO-494"
   ],
   "transitions": [
    {
     "to": "BO-494",
     "trigger": "Back to Rental Product Command Center",
     "provenance": "structural — pack board 1 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure reusable categories rather than hard-coding individual rental types.",
  "gaps": [
   {
    "operation": null,
    "why": "**Rental Category & Classification Setup declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 9"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 9"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The rental category classification list.",
   "error": "Could not load. Names which read failed and leaves the rental category classification untouched.",
   "emptyFirstRun": "No rental category classification yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the rental category classification are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-497"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 9. 0 of 0 labels bound to a contract property; 0 of 30 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-498",
  "name": "Inventory Tracking Model",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "1",
   "number": "5",
   "page": 10
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/inventory-tracking-model-bo-498",
   "component": "apps/venue-management-web/src/routes/rentals/InventoryTrackingModel.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-494"
   ],
   "exitTo": [
    "BO-494"
   ],
   "transitions": [
    {
     "to": "BO-494",
     "trigger": "Back to Rental Product Command Center",
     "provenance": "structural — pack board 1 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configuration) and no display directory — it is settings, not a population",
  "purpose": "Determine how the product's physical inventory will be controlled.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Tracking Model",
       "provenance": "pack Rental_Management.pdf, page 10 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Inventory Unit",
       "provenance": "pack Rental_Management.pdf, page 10 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Quantity Control",
       "provenance": "pack Rental_Management.pdf, page 10 §Configuration"
      },
      {
       "kind": "textField",
       "label": "Assignment Required at Checkout",
       "provenance": "pack Rental_Management.pdf, page 10 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Scan Required",
       "provenance": "pack Rental_Management.pdf, page 10 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Allow Manual Assignment",
       "provenance": "pack Rental_Management.pdf, page 10 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Allow Substitution",
       "provenance": "pack Rental_Management.pdf, page 10 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Allow Equipment Swap",
       "provenance": "pack Rental_Management.pdf, page 10 §Configuration"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The inventory tracking model configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the inventory tracking model untouched.",
   "emptyFirstRun": "No inventory tracking model configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-498"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 10. 0 of 0 labels bound to a contract property; 8 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-499",
  "name": "Rental Location Assignment",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "1",
   "number": "6",
   "page": 11
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/rental-location-assignment-bo-499",
   "component": "apps/venue-management-web/src/routes/rentals/RentalLocationAssignment.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-494"
   ],
   "exitTo": [
    "BO-494"
   ],
   "transitions": [
    {
     "to": "BO-494",
     "trigger": "Back to Rental Product Command Center",
     "provenance": "structural — pack board 1 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Define where a product can physically be rented, collected and returned.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 2 actions on this screen and the screen declares 0 operations.** Unserved: Different return locations, Allow return to different location: YES/NO. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Rental_Management.pdf, page 11 §Support"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 11"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 11"
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
       "label": "Different return locations",
       "provenance": "pack Rental_Management.pdf, page 11 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Allow return to different location: YES/NO",
       "provenance": "pack Rental_Management.pdf, page 11 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The rental location list.",
   "error": "Could not load. Names which read failed and leaves the rental location untouched.",
   "emptyFirstRun": "No rental location yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the rental location are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-499"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 11. 0 of 0 labels bound to a contract property; 2 of 19 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-500",
  "name": "Rental Duration & Turnaround Configuration",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "1",
   "number": "7",
   "page": 12
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/rental-duration-turnaround-configuration-bo-500",
   "component": "apps/venue-management-web/src/routes/rentals/RentalDurationTurnaroundConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-494"
   ],
   "exitTo": [
    "BO-494"
   ],
   "transitions": [
    {
     "to": "BO-494",
     "trigger": "Back to Rental Product Command Center",
     "provenance": "structural — pack board 1 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configuration; Configure) and no display directory — it is settings, not a population",
  "purpose": "Define how long the product can be rented. The source requires minimum and maximum rental durations and both fixed and customer-defined durations.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Minimum Duration",
       "provenance": "pack Rental_Management.pdf, page 12 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Maximum Duration",
       "provenance": "pack Rental_Management.pdf, page 12 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Duration Increment",
       "provenance": "pack Rental_Management.pdf, page 12 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Default Duration",
       "provenance": "pack Rental_Management.pdf, page 12 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Allow Extension",
       "provenance": "pack Rental_Management.pdf, page 12 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Maximum Extension",
       "provenance": "pack Rental_Management.pdf, page 12 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Same-Day Return Required",
       "provenance": "pack Rental_Management.pdf, page 12 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Overnight Rental Allowed",
       "provenance": "pack Rental_Management.pdf, page 12 §Configuration"
      },
      {
       "kind": "textField",
       "label": "Recommended Addition — Turnaround Time",
       "provenance": "pack Rental_Management.pdf, page 12 §Configuration"
      },
      {
       "kind": "textField",
       "label": "Preparation / Inspection / Cleaning Buffer",
       "provenance": "pack Rental_Management.pdf, page 12 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The rental duration turnaround configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the rental duration turnaround untouched.",
   "emptyFirstRun": "No rental duration turnaround configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-500"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 12. 0 of 0 labels bound to a contract property; 10 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-501",
  "name": "Rental Rules & Operational Policy",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "1",
   "number": "8",
   "page": 13
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/rental-rules-operational-policy-bo-501",
   "component": "apps/venue-management-web/src/routes/rentals/RentalRulesOperationalPolicy.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-494"
   ],
   "exitTo": [
    "BO-494"
   ],
   "transitions": [
    {
     "to": "BO-494",
     "trigger": "Back to Rental Product Command Center",
     "provenance": "structural — pack board 1 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Define the fundamental operational restrictions for the product.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 13"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rental_Management.pdf, page 13"
   }
  ],
  "layout": {
   "template": "split",
   "regions": []
  },
  "states": {
   "loading": "The rental rules operational list.",
   "error": "Could not load. Names which read failed and leaves the rental rules operational untouched.",
   "emptyFirstRun": "No rental rules operational yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the rental rules operational are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-501"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 13. 0 of 0 labels bound to a contract property; 0 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-502",
  "name": "Customer Requirements, Agreement & Waiver",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "1",
   "number": "9",
   "page": 13
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/customer-requirements-agreement-waiver-bo-502",
   "component": "apps/venue-management-web/src/routes/rentals/CustomerRequirementsAgreementWaiver.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-494"
   ],
   "exitTo": [
    "BO-494"
   ],
   "transitions": [
    {
     "to": "BO-494",
     "trigger": "Back to Rental Product Command Center",
     "provenance": "structural — pack board 1 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configurable fields; Configure) and no display directory — it is settings, not a population",
  "purpose": "Define information and agreements required before a customer can receive the rental.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 4 actions on this screen and the screen declares 0 operations.** Unserved: Participant details, Individual waiver, Group waiver, Guardian consent. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Rental_Management.pdf, page 13 §Support"
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
       "label": "Name",
       "provenance": "pack Rental_Management.pdf, page 13 §Configurable fields"
      },
      {
       "kind": "selectField",
       "label": "Mobile",
       "provenance": "pack Rental_Management.pdf, page 13 §Configurable fields"
      },
      {
       "kind": "selectField",
       "label": "Email",
       "provenance": "pack Rental_Management.pdf, page 13 §Configurable fields"
      },
      {
       "kind": "selectField",
       "label": "Nationality",
       "provenance": "pack Rental_Management.pdf, page 13 §Configurable fields"
      },
      {
       "kind": "selectField",
       "label": "ID Number",
       "provenance": "pack Rental_Management.pdf, page 13 §Configurable fields"
      },
      {
       "kind": "selectField",
       "label": "Date of Birth",
       "provenance": "pack Rental_Management.pdf, page 13 §Configurable fields"
      },
      {
       "kind": "selectField",
       "label": "Emergency Contact",
       "provenance": "pack Rental_Management.pdf, page 13 §Configurable fields"
      },
      {
       "kind": "selectField",
       "label": "Address",
       "provenance": "pack Rental_Management.pdf, page 13 §Configurable fields"
      },
      {
       "kind": "selectField",
       "label": "Custom Fields",
       "provenance": "pack Rental_Management.pdf, page 13 §Configurable fields"
      },
      {
       "kind": "selectField",
       "label": "Rental Agreement Required",
       "provenance": "pack Rental_Management.pdf, page 13 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Liability Waiver Required",
       "provenance": "pack Rental_Management.pdf, page 13 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Terms & Conditions",
       "provenance": "pack Rental_Management.pdf, page 13 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Safety Declaration",
       "provenance": "pack Rental_Management.pdf, page 13 §Configure"
      },
      {
       "kind": "selectField",
       "label": "E-Signature Required",
       "provenance": "pack Rental_Management.pdf, page 13 §Configure"
      },
      {
       "kind": "textField",
       "label": "Guardian Signature for Minor",
       "provenance": "pack Rental_Management.pdf, page 13 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Agreement Version",
       "provenance": "pack Rental_Management.pdf, page 13 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Participant details",
       "provenance": "pack Rental_Management.pdf, page 13 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Individual waiver",
       "provenance": "pack Rental_Management.pdf, page 13 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Group waiver",
       "provenance": "pack Rental_Management.pdf, page 13 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Guardian consent",
       "provenance": "pack Rental_Management.pdf, page 13 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The customer requirements agreement configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the customer requirements agreement untouched.",
   "emptyFirstRun": "No customer requirements agreement configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-502"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 13. 0 of 0 labels bound to a contract property; 20 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-503",
  "name": "Product Validation, Approval & Publication",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Rental_Management.pdf",
   "board": "1",
   "number": "10",
   "page": 14
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/product-validation-approval-publication-bo-503",
   "component": "apps/venue-management-web/src/routes/rentals/ProductValidationApprovalPublication.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-494"
   ],
   "exitTo": [
    "BO-494"
   ],
   "transitions": [
    {
     "to": "BO-494",
     "trigger": "Back to Rental Product Command Center",
     "provenance": "structural — pack board 1 wiring, 11 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Product Setup; Operational Setup; AI Configuration Review) and no display directory — it is settings, not a population",
  "purpose": "Provide controlled governance before a rental product becomes sellable.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 4 actions on this screen and the screen declares 0 operations.** Unserved: Maker/checker workflow, Approval comments, Rejection reason, Version history. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Rental_Management.pdf, page 14 §Support"
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
       "label": "✓ Basic information",
       "provenance": "pack Rental_Management.pdf, page 14 §Product Setup"
      },
      {
       "kind": "selectField",
       "label": "✓ Category",
       "provenance": "pack Rental_Management.pdf, page 14 §Product Setup"
      },
      {
       "kind": "selectField",
       "label": "✓ Rental location",
       "provenance": "pack Rental_Management.pdf, page 14 §Product Setup"
      },
      {
       "kind": "selectField",
       "label": "✓ Inventory model",
       "provenance": "pack Rental_Management.pdf, page 14 §Product Setup"
      },
      {
       "kind": "selectField",
       "label": "✓ Duration",
       "provenance": "pack Rental_Management.pdf, page 14 §Product Setup"
      },
      {
       "kind": "selectField",
       "label": "✓ Rental rules",
       "provenance": "pack Rental_Management.pdf, page 14 §Operational Setup"
      },
      {
       "kind": "selectField",
       "label": "✓ Customer requirements",
       "provenance": "pack Rental_Management.pdf, page 14 §Operational Setup"
      },
      {
       "kind": "selectField",
       "label": "✓ Agreement",
       "provenance": "pack Rental_Management.pdf, page 14 §Operational Setup"
      },
      {
       "kind": "textField",
       "label": "⚠ Inventory not yet assigned",
       "provenance": "pack Rental_Management.pdf, page 14 §Operational Setup"
      },
      {
       "kind": "selectField",
       "label": "Product: Double Kayak",
       "provenance": "pack Rental_Management.pdf, page 14 §AI Configuration Review"
      },
      {
       "kind": "selectField",
       "label": "Configuration Score: 87%",
       "provenance": "pack Rental_Management.pdf, page 14 §AI Configuration Review"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Maker/checker workflow",
       "provenance": "pack Rental_Management.pdf, page 14 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Approval comments",
       "provenance": "pack Rental_Management.pdf, page 14 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Rejection reason",
       "provenance": "pack Rental_Management.pdf, page 14 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Version history",
       "provenance": "pack Rental_Management.pdf, page 14 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The product validation approval configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the product validation approval untouched.",
   "emptyFirstRun": "No product validation approval configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-503"
  },
  "apisNote": "Regenerated 9 September 2026 from Rental_Management.pdf page 14. 0 of 0 labels bound to a contract property; 15 of 38 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
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
