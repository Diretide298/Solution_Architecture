# WS43 — Product Lifecycle   Catalogue Governance board 1

**10 screens · 12 operations · 28 schemas · 2 permissions**

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
  `PRODUCT_CONFIGURE, PRODUCT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-118` | Product Lifecycle Command Center | listDetail | 1 | 0 | — |
| `ADM-119` | Product Creation Workspace | listDetail | 1 | 0 | — |
| `ADM-120` | Lifecycle Status & Workflow Configuration | listDetail | 1 | 0 | — |
| `ADM-121` | Bulk Product Creation & Catalogue Import | listDetail | 1 | 0 | — |
| `ADM-122` | Product Import / Export & Environment Transfer | listDetail | 1 | 0 | — |
| `ADM-123` | Product Context, Ownership & Assignment | listDetail | 1 | 0 | — |
| `ADM-124` | Channel Publication & Availability | listDetail | 1 | 0 | — |
| `ADM-125` | Publication & Activation Scheduler | listDetail | 2 | 0 | — |
| `ADM-126` | Product Duplication & Template Library | configEditor | 2 | 1 | — |
| `ADM-127` | AI Catalogue Builder & Configuration Review | listDetail | 1 | 0 | — |

## Thin screens in this batch

**ADM-118, ADM-119, ADM-120, ADM-121, ADM-122, ADM-123, ADM-124, ADM-125, ADM-127 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-118",
  "name": "Product Lifecycle Command Center",
  "module": "Catalogue",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Product_Lifecycle___Catalogue_Governance_Reference.pdf",
   "board": "1",
   "number": "1",
   "page": 3
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/catalogue/product-lifecycle-command-center-adm-118",
   "component": "apps/ticvai-web/src/routes/catalogue/ProductLifecycleCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-119",
    "ADM-120",
    "ADM-121",
    "ADM-122",
    "ADM-123",
    "ADM-124",
    "ADM-125",
    "ADM-126",
    "ADM-127"
   ],
   "inferred": false,
   "notes": "**The board's hub.** The workshop specified this module as boards of ten and opened each with a command centre; the other nine screens are that board's detail, so they are reached from here and return here.",
   "transitions": [
    {
     "to": "ADM-002",
     "trigger": "Platform Dashboard",
     "provenance": "derived — ADM-002 declares entryState.params  and ADM-118 holds none of them. The edge carries nothing: ADM-118 is opened from ADM-002, so this edge is the way back and ADM-002 keeps its own state"
    },
    {
     "to": "ADM-119",
     "trigger": "Works in Product Creation Workspace",
     "provenance": "flow F152 step 1→2",
     "operation": "listProductLifecycle"
    },
    {
     "to": "ADM-120",
     "trigger": "Works in Lifecycle Status & Workflow Configuration",
     "provenance": "flow F152 step 3→4",
     "operation": "listProductLifecycle"
    },
    {
     "to": "ADM-121",
     "trigger": "Works in Bulk Product Creation & Catalogue Import",
     "provenance": "flow F152 step 5→6",
     "operation": "listProductLifecycle"
    },
    {
     "to": "ADM-122",
     "trigger": "Works in Product Import / Export & Environment Transfer",
     "provenance": "flow F152 step 7→8",
     "operation": "listProductLifecycle"
    },
    {
     "to": "ADM-123",
     "trigger": "Works in Product Context, Ownership & Assignment",
     "provenance": "flow F152 step 9→10",
     "operation": "listProductLifecycle"
    },
    {
     "to": "ADM-124",
     "trigger": "Works in Channel Publication & Availability",
     "provenance": "flow F152 step 11→12",
     "operation": "listProductLifecycle"
    },
    {
     "to": "ADM-125",
     "trigger": "Works in Publication & Activation Scheduler",
     "provenance": "flow F152 step 13→14",
     "operation": "listProductLifecycle"
    },
    {
     "to": "ADM-126",
     "trigger": "Works in Product Duplication & Template Library",
     "provenance": "flow F152 step 15→16",
     "operation": "listProductLifecycle"
    },
    {
     "to": "ADM-127",
     "trigger": "Works in AI Catalogue Builder & Configuration Review",
     "provenance": "flow F152 step 17→18",
     "operation": "listProductLifecycle"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "An authorized administrator can locate any product, identify its exact lifecycle state and determine the next required operational action from one screen.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide administrators with a centralized operational view of every product and its current lifecycle state.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 3"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 3"
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
       "impliedBy": "listProductLifecycle",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The product lifecycle list.",
   "error": "Could not load. Names which read failed and leaves the product lifecycle untouched.",
   "emptyFirstRun": "No product lifecycle yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the product lifecycle are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listProductLifecycle",
    "contract": "catalogue",
    "purpose": "Product Lifecycle Command Center",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "ProductLifecycleCommandCenterView.lifecycleState"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-118",
   "workshopBoard": "wireframes/WS104 Product Lifecycle   Catalogue Governance Board 1.dc.html#adm-118"
  },
  "apisNote": "Regenerated 9 September 2026 from Product_Lifecycle___Catalogue_Governance_Reference.pdf page 3. 0 of 0 labels bound to a contract property; 0 of 37 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-119",
  "name": "Product Creation Workspace",
  "module": "Catalogue",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Product_Lifecycle___Catalogue_Governance_Reference.pdf",
   "board": "1",
   "number": "2",
   "page": 4
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/catalogue/product-creation-workspace-adm-119",
   "component": "apps/ticvai-web/src/routes/catalogue/ProductCreationWorkspace.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-118"
   ],
   "exitTo": [
    "ADM-118"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-118, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-118",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F152 step 2→3",
     "operation": "createProduct"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "A new product can be created and saved in Draft without becoming commercially available until all required configuration and governance conditions are satisfied.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide a governed starting point for creating a new ticketing product.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 4"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 4"
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
       "label": "Create",
       "provenance": "contract operation createProduct"
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
       "impliedBy": "createProduct"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The product creation list.",
   "error": "Could not load. Names which read failed and leaves the product creation untouched.",
   "emptyFirstRun": "No product creation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the product creation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createProduct",
    "contract": "catalogue",
    "purpose": "Create a product",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-119",
   "workshopBoard": "wireframes/WS104 Product Lifecycle   Catalogue Governance Board 1.dc.html#adm-119"
  },
  "apisNote": "Regenerated 9 September 2026 from Product_Lifecycle___Catalogue_Governance_Reference.pdf page 4. 0 of 0 labels bound to a contract property; 0 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-120",
  "name": "Lifecycle Status & Workflow Configuration",
  "module": "Catalogue",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Product_Lifecycle___Catalogue_Governance_Reference.pdf",
   "board": "1",
   "number": "3",
   "page": 5
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/catalogue/lifecycle-status-workflow-configuration-adm-120",
   "component": "apps/ticvai-web/src/routes/catalogue/LifecycleStatusWorkflowConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-118"
   ],
   "exitTo": [
    "ADM-118"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-118, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-118",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F152 step 4→5",
     "operation": "setLifecycleStatuWorkflow"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Administrators can configure a controlled product lifecycle without development or database changes.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure how products move between lifecycle states.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 5"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 5"
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
       "provenance": "contract operation setLifecycleStatuWorkflow"
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
       "impliedBy": "setLifecycleStatuWorkflow"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The lifecycle status workflow list.",
   "error": "Could not load. Names which read failed and leaves the lifecycle status workflow untouched.",
   "emptyFirstRun": "No lifecycle status workflow yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the lifecycle status workflow are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setLifecycleStatuWorkflow",
    "contract": "catalogue",
    "purpose": "Lifecycle Status & Workflow Configuration",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-120",
   "workshopBoard": "wireframes/WS104 Product Lifecycle   Catalogue Governance Board 1.dc.html#adm-120"
  },
  "apisNote": "Regenerated 9 September 2026 from Product_Lifecycle___Catalogue_Governance_Reference.pdf page 5. 0 of 0 labels bound to a contract property; 0 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-121",
  "name": "Bulk Product Creation & Catalogue Import",
  "module": "Catalogue",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Product_Lifecycle___Catalogue_Governance_Reference.pdf",
   "board": "1",
   "number": "4",
   "page": 6
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/catalogue/bulk-product-creation-catalogue-import-adm-121",
   "component": "apps/ticvai-web/src/routes/catalogue/BulkProductCreationCatalogueImport.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-118"
   ],
   "exitTo": [
    "ADM-118"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-118, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-118",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F152 step 6→7",
     "operation": "createBulkProductCatalogue"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "An administrator can convert a large existing catalogue into draft TICVAI products through a controlled import and validation process.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow large catalogues to be created efficiently rather than configuring every product manually. This directly addresses the matrix requirement for catalogue creation through bulk-file upload.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 6"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 6"
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
       "label": "Create",
       "provenance": "contract operation createBulkProductCatalogue"
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
       "impliedBy": "createBulkProductCatalogue"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The bulk product creation list.",
   "error": "Could not load. Names which read failed and leaves the bulk product creation untouched.",
   "emptyFirstRun": "No bulk product creation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the bulk product creation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createBulkProductCatalogue",
    "contract": "catalogue",
    "purpose": "Bulk Product Creation & Catalogue Import",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-121",
   "workshopBoard": "wireframes/WS104 Product Lifecycle   Catalogue Governance Board 1.dc.html#adm-121"
  },
  "apisNote": "Regenerated 9 September 2026 from Product_Lifecycle___Catalogue_Governance_Reference.pdf page 6. 0 of 0 labels bound to a contract property; 0 of 37 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-122",
  "name": "Product Import / Export & Environment Transfer",
  "module": "Catalogue",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Product_Lifecycle___Catalogue_Governance_Reference.pdf",
   "board": "1",
   "number": "5",
   "page": 7
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/catalogue/product-import-export-environment-transfer-adm-122",
   "component": "apps/ticvai-web/src/routes/catalogue/ProductImportExportEnvironmentTransfer.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-118"
   ],
   "exitTo": [
    "ADM-118"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-118, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-118",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F152 step 8→9",
     "operation": "listProductImportExport"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Products can be moved between authorized environments without manually recreating their configuration and without silently overwriting incompatible production settings.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow controlled movement of product configurations between TICVAI environments. This covers the matrix requirement for importing/exporting catalogue products between different environments.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 7"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 7"
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
       "impliedBy": "listProductImportExport",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The product import export list.",
   "error": "Could not load. Names which read failed and leaves the product import export untouched.",
   "emptyFirstRun": "No product import export yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the product import export are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listProductImportExport",
    "contract": "catalogue",
    "purpose": "Product Import / Export & Environment Transfer",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "ProductImportExportEnvironmentTransferView.referenceMappings",
    "ProductImportExportEnvironmentTransferView.missingReferences",
    "ProductImportExportEnvironmentTransferView.changePreview"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-122",
   "workshopBoard": "wireframes/WS104 Product Lifecycle   Catalogue Governance Board 1.dc.html#adm-122"
  },
  "apisNote": "Regenerated 9 September 2026 from Product_Lifecycle___Catalogue_Governance_Reference.pdf page 7. 0 of 0 labels bound to a contract property; 0 of 26 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-123",
  "name": "Product Context, Ownership & Assignment",
  "module": "Catalogue",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Product_Lifecycle___Catalogue_Governance_Reference.pdf",
   "board": "1",
   "number": "6",
   "page": 8
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/catalogue/product-context-ownership-assignment-adm-123",
   "component": "apps/ticvai-web/src/routes/catalogue/ProductContextOwnershipAssignment.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-118"
   ],
   "exitTo": [
    "ADM-118"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-118, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-118",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F152 step 10→11",
     "operation": "setProductContextOwnership"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Every governed product has clearly defined ownership, organizational context and operational/commercial assignment.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Define where the product belongs and who is responsible for it.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 8"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 8"
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
       "provenance": "contract operation setProductContextOwnership"
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
       "impliedBy": "setProductContextOwnership"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The product context ownership list.",
   "error": "Could not load. Names which read failed and leaves the product context ownership untouched.",
   "emptyFirstRun": "No product context ownership yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the product context ownership are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setProductContextOwnership",
    "contract": "catalogue",
    "purpose": "Product Context, Ownership & Assignment",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-123",
   "workshopBoard": "wireframes/WS104 Product Lifecycle   Catalogue Governance Board 1.dc.html#adm-123"
  },
  "apisNote": "Regenerated 9 September 2026 from Product_Lifecycle___Catalogue_Governance_Reference.pdf page 8. 0 of 0 labels bound to a contract property; 0 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-124",
  "name": "Channel Publication & Availability",
  "module": "Catalogue",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Product_Lifecycle___Catalogue_Governance_Reference.pdf",
   "board": "1",
   "number": "7",
   "page": 9
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/catalogue/channel-publication-availability-adm-124",
   "component": "apps/ticvai-web/src/routes/catalogue/ChannelPublicationAvailability.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-118"
   ],
   "exitTo": [
    "ADM-118"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-118, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-118",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F152 step 12→13",
     "operation": "publishChannelAvailability"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "An authorized user can control precisely which approved channels expose a product while previously issued valid entitlements remain unaffected unless a separate governed action explicitly changes them.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Control where a product may be exposed for sale.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 9"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 9"
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
       "label": "Publish",
       "provenance": "contract operation publishChannelAvailability"
      },
      {
       "kind": "publishGate",
       "label": "What publishing changes",
       "notes": "**Names what goes live, where, and from when.** A publish with no stated consequence is one somebody presses meaning to save.",
       "provenance": "authored — required by check-screens for publishChannelAvailability"
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
   "loading": "The channel publication availability list.",
   "error": "Could not load. Names which read failed and leaves the channel publication availability untouched.",
   "emptyFirstRun": "No channel publication availability yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the channel publication availability are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "publishChannelAvailability",
    "contract": "catalogue",
    "purpose": "Channel Publication & Availability",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-124",
   "workshopBoard": "wireframes/WS104 Product Lifecycle   Catalogue Governance Board 1.dc.html#adm-124"
  },
  "apisNote": "Regenerated 9 September 2026 from Product_Lifecycle___Catalogue_Governance_Reference.pdf page 9. 0 of 0 labels bound to a contract property; 0 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-125",
  "name": "Publication & Activation Scheduler",
  "module": "Catalogue",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Product_Lifecycle___Catalogue_Governance_Reference.pdf",
   "board": "1",
   "number": "8",
   "page": 10
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/catalogue/publication-activation-scheduler-adm-125",
   "component": "apps/ticvai-web/src/routes/catalogue/PublicationActivationScheduler.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-118"
   ],
   "exitTo": [
    "ADM-118"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-118, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-118",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F152 step 14→15",
     "operation": "publishActivationScheduler"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Products can automatically enter or leave defined commercial lifecycle states at configured times without manual intervention.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Automate future product lifecycle actions.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 10"
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
       "label": "Publish",
       "operation": "publishActivationScheduler",
       "provenance": "contract operation publishActivationScheduler"
      },
      {
       "kind": "publishGate",
       "label": "What publishing changes",
       "notes": "**Names what goes live, where, and from when.** A publish with no stated consequence is one somebody presses meaning to save.",
       "provenance": "authored — required by check-screens for publishActivationScheduler"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "timeline",
       "label": "Calendar",
       "bindsTo": "PublicationActivationSchedulerView",
       "operation": "listScheduledLifecycleActions",
       "notes": "**Every scheduled lifecycle action in the range, on a calendar**: upcoming as scheduled, done as executed, failed with its reason, so failed jobs and conflicts show where they happened. Without a range, the next 31 days (decided 29 September, readiness close-out).",
       "provenance": "contract catalogue.yaml GET /activation-scheduler"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The publication activation scheduler list.",
   "error": "Could not load. Names which read failed and leaves the publication activation scheduler untouched.",
   "emptyFirstRun": "No publication activation scheduler yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the publication activation scheduler are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "publishActivationScheduler",
    "contract": "catalogue",
    "purpose": "Publication & Activation Scheduler",
    "trigger": "onAction"
   },
   {
    "operationId": "listScheduledLifecycleActions",
    "contract": "catalogue",
    "purpose": "Scheduled lifecycle actions, for the scheduler calendar",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-125",
   "workshopBoard": "wireframes/WS104 Product Lifecycle   Catalogue Governance Board 1.dc.html#adm-125"
  },
  "apisNote": "Regenerated 9 September 2026 from Product_Lifecycle___Catalogue_Governance_Reference.pdf page 10. 0 of 0 labels bound to a contract property; 0 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-126",
  "name": "Product Duplication & Template Library",
  "module": "Catalogue",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Product_Lifecycle___Catalogue_Governance_Reference.pdf",
   "board": "1",
   "number": "9",
   "page": 11
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/catalogue/product-duplication-template-library-adm-126",
   "component": "apps/ticvai-web/src/routes/catalogue/ProductDuplicationTemplateLibrary.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-118"
   ],
   "exitTo": [
    "ADM-118"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-118, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-118",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F152 step 16→17",
     "operation": "listProductDuplicationTemplate"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Users can create a new Draft product from an existing product/template while preventing accidental reuse of inappropriate dates, venues, prices or other context-sensitive values.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Duplication Options) and no display directory — it is settings, not a population",
  "purpose": "Accelerate product configuration by allowing administrators to reuse proven configurations. The source matrix explicitly requires duplication of products together with associated configuration, rules, pricing and entitlements.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Core product details",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 11 §Duplication Options"
      },
      {
       "kind": "selectField",
       "label": "Validity",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 11 §Duplication Options"
      },
      {
       "kind": "selectField",
       "label": "Pricing references",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 11 §Duplication Options"
      },
      {
       "kind": "selectField",
       "label": "Entitlements",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 11 §Duplication Options"
      },
      {
       "kind": "selectField",
       "label": "Capacity references",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 11 §Duplication Options"
      },
      {
       "kind": "selectField",
       "label": "Eligibility",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 11 §Duplication Options"
      },
      {
       "kind": "selectField",
       "label": "Sales channels",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 11 §Duplication Options"
      },
      {
       "kind": "selectField",
       "label": "Media",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 11 §Duplication Options"
      },
      {
       "kind": "selectField",
       "label": "Policies",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 11 §Duplication Options"
      },
      {
       "kind": "selectField",
       "label": "Rules",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 11 §Duplication Options"
      },
      {
       "kind": "selectField",
       "label": "Content",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 11 §Duplication Options"
      },
      {
       "kind": "selectField",
       "label": "Images",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 11 §Duplication Options"
      },
      {
       "kind": "selectField",
       "label": "Relationships",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 11 §Duplication Options"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save configuration template",
       "operation": "setConfigurationTemplate",
       "permission": "PRODUCT_CONFIGURE",
       "notes": "**One template library for products and price lists** (29 September, writers pass).",
       "provenance": "contract catalogue.yaml PUT /configuration-templates"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The product duplication template configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the product duplication template untouched.",
   "emptyFirstRun": "No product duplication template configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listProductDuplicationTemplate",
    "contract": "catalogue",
    "purpose": "Product Duplication & Template Library",
    "trigger": "onLoad"
   },
   {
    "operationId": "setConfigurationTemplate",
    "contract": "catalogue",
    "purpose": "Create or update a product or price-list template",
    "trigger": "onAction",
    "invalidates": [
     "listProductDuplicationTemplate"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-126",
   "workshopBoard": "wireframes/WS104 Product Lifecycle   Catalogue Governance Board 1.dc.html#adm-126"
  },
  "apisNote": "Regenerated 9 September 2026 from Product_Lifecycle___Catalogue_Governance_Reference.pdf page 11. 0 of 0 labels bound to a contract property; 13 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formSetConfigurationTemplate",
    "component": "modal",
    "trigger": "Save configuration template",
    "body": "**Collects what `setConfigurationTemplate` sends before it is called.** Required: `id`, `scopePath`, `subject`, `name`, `status`. Optional: `description`, `templateKind`, `productKind`, `venueId`, `sourceProductId`, `sourcePriceListId`, `includedComponents`, `reviewFields`, `isAiDrafted`, `ownerPrincipalId`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "ConfigurationTemplate",
    "confirm": {
     "label": "Save configuration template",
     "operation": "setConfigurationTemplate"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "scopePath",
      "subject",
      "name",
      "status",
      "description",
      "templateKind",
      "productKind",
      "venueId",
      "sourceProductId",
      "sourcePriceListId",
      "includedComponents",
      "reviewFields",
      "isAiDrafted",
      "ownerPrincipalId"
     ]
    },
    "provenance": "contract catalogue.yaml PUT /configuration-templates"
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
  "id": "ADM-127",
  "name": "AI Catalogue Builder & Configuration Review",
  "module": "Catalogue",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Product_Lifecycle___Catalogue_Governance_Reference.pdf",
   "board": "1",
   "number": "10",
   "page": 12
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/catalogue/ai-catalogue-builder-configuration-review-adm-127",
   "component": "apps/ticvai-web/src/routes/catalogue/AiCatalogueBuilderConfigurationReview.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-118"
   ],
   "exitTo": [
    "ADM-118"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-118, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation."
  },
  "density": "compact",
  "purposeNote": "An administrator can transform unstructured or semi-structured commercial information into a structured Draft product configuration, review every AI-generated recommendation and approve or modify it before the normal lifecycle workflow begins. Board 1 — Final Screen Register",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide TICVAI's AI-first interface for accelerating product creation and configuration. This directly supports the matrix requirement allowing administrators to upload spreadsheets, brochures, PDFs or existing catalogues and use AI to generate product structures, pricing, rules, entitlements and configurations. Board 2 governs what happens after a product has been created or while an existing product is being changed.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 12"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 12"
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
       "provenance": "contract operation setCatalogueReview"
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
       "impliedBy": "setCatalogueReview"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The catalogue review list.",
   "error": "Could not load. Names which read failed and leaves the catalogue review untouched.",
   "emptyFirstRun": "No catalogue review yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the catalogue review are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setCatalogueReview",
    "contract": "catalogue",
    "purpose": "AI Catalogue Builder & Configuration Review",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-127",
   "workshopBoard": "wireframes/WS104 Product Lifecycle   Catalogue Governance Board 1.dc.html#adm-127"
  },
  "apisNote": "Regenerated 9 September 2026 from Product_Lifecycle___Catalogue_Governance_Reference.pdf page 12. 0 of 0 labels bound to a contract property; 0 of 68 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "createBulkProductCatalogue": {
  "method": "POST",
  "path": "/bulk-product-catalogue",
  "contract": "catalogue",
  "summary": "Bulk Product Creation & Catalogue Import",
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
  "requestBody": "BulkProductCreationCatalogueImportInput",
  "responds": "BulkProductCreationCatalogueImportView"
 },
 "createProduct": {
  "method": "POST",
  "path": "/products",
  "contract": "catalogue",
  "summary": "Create a product",
  "permission": "PRODUCT_CONFIGURE",
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
  "requestBody": "CreateProductRequest",
  "responds": "Product"
 },
 "listProductDuplicationTemplate": {
  "method": "GET",
  "path": "/product-duplication-template",
  "contract": "catalogue",
  "summary": "Product Duplication & Template Library",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "templateKind",
    "in": "query",
    "required": false
   },
   {
    "name": "productType",
    "in": "query",
    "required": false
   },
   {
    "name": "venueId",
    "in": "query",
    "required": false
   },
   {
    "name": "search",
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
 "listProductImportExport": {
  "method": "GET",
  "path": "/product-import-export",
  "contract": "catalogue",
  "summary": "Product Import / Export & Environment Transfer",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "direction",
    "in": "query",
    "required": false
   },
   {
    "name": "environment",
    "in": "query",
    "required": false
   },
   {
    "name": "status",
    "in": "query",
    "required": false
   },
   {
    "name": "search",
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
 "listProductLifecycle": {
  "method": "GET",
  "path": "/product-lifecycle",
  "contract": "catalogue",
  "summary": "Product Lifecycle Command Center",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "productType",
    "in": "query",
    "required": false
   },
   {
    "name": "venueId",
    "in": "query",
    "required": false
   },
   {
    "name": "locationId",
    "in": "query",
    "required": false
   },
   {
    "name": "lifecycleState",
    "in": "query",
    "required": false
   },
   {
    "name": "owner",
    "in": "query",
    "required": false
   },
   {
    "name": "department",
    "in": "query",
    "required": false
   },
   {
    "name": "channel",
    "in": "query",
    "required": false
   },
   {
    "name": "effectiveOn",
    "in": "query",
    "required": false
   },
   {
    "name": "createdFrom",
    "in": "query",
    "required": false
   },
   {
    "name": "createdTo",
    "in": "query",
    "required": false
   },
   {
    "name": "modifiedSince",
    "in": "query",
    "required": false
   },
   {
    "name": "search",
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
 "listScheduledLifecycleActions": {
  "method": "GET",
  "path": "/activation-scheduler",
  "contract": "catalogue",
  "summary": "Scheduled lifecycle actions, for the scheduler calendar",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "from",
    "in": "query",
    "required": false
   },
   {
    "name": "to",
    "in": "query",
    "required": false
   },
   {
    "name": "actionType",
    "in": "query",
    "required": false
   },
   {
    "name": "status",
    "in": "query",
    "required": false
   },
   {
    "name": "productId",
    "in": "query",
    "required": false
   },
   {
    "name": "venueId",
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
 "publishActivationScheduler": {
  "method": "PUT",
  "path": "/activation-scheduler",
  "contract": "catalogue",
  "summary": "Publication & Activation Scheduler",
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
  "requestBody": "PublicationActivationSchedulerInput",
  "responds": "PublicationActivationSchedulerView"
 },
 "publishChannelAvailability": {
  "method": "PUT",
  "path": "/channel-availability",
  "contract": "catalogue",
  "summary": "Channel Publication & Availability",
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
  "requestBody": "ChannelPublicationAvailabilityInput",
  "responds": "ChannelPublicationAvailabilityView"
 },
 "setCatalogueReview": {
  "method": "PUT",
  "path": "/catalogue-review",
  "contract": "catalogue",
  "summary": "AI Catalogue Builder & Configuration Review",
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
  "requestBody": "AiCatalogueBuilderConfigurationReviewInput",
  "responds": "AiCatalogueBuilderConfigurationReviewView"
 },
 "setConfigurationTemplate": {
  "method": "PUT",
  "path": "/configuration-templates",
  "contract": "catalogue",
  "summary": "Create or update a product or price-list template",
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
  "requestBody": "ConfigurationTemplate",
  "responds": "ConfigurationTemplate"
 },
 "setLifecycleStatuWorkflow": {
  "method": "PUT",
  "path": "/lifecycle-statu-workflow",
  "contract": "catalogue",
  "summary": "Lifecycle Status & Workflow Configuration",
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
  "requestBody": "LifecycleStatusWorkflowConfigurationInput",
  "responds": "LifecycleStatusWorkflowConfigurationView"
 },
 "setProductContextOwnership": {
  "method": "PUT",
  "path": "/product-context-ownership",
  "contract": "catalogue",
  "summary": "Product Context, Ownership & Assignment",
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
  "requestBody": "ProductContextOwnershipAssignmentInput",
  "responds": "ProductContextOwnershipAssignmentView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AiCatalogueBuilderConfigurationReviewInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What AI Catalogue Builder & Configuration Review submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "prompt": {
    "type": "string",
    "description": "Natural-language request",
    "nullable": true
   },
   "sessionId": {
    "type": "string",
    "description": "Existing session to update; empty to start one",
    "format": "uuid",
    "nullable": true
   },
   "inputMethod": {
    "type": "string",
    "enum": [
     "naturalLanguage",
     "excel",
     "csv",
     "pdf",
     "brochure",
     "existingCatalogue",
     "referenceProduct"
    ],
    "description": "Input method (pack p.12)"
   },
   "fileId": {
    "type": "string",
    "description": "Uploaded source file id",
    "nullable": true
   },
   "referenceProductId": {
    "type": "string",
    "description": "Existing product used as reference",
    "format": "uuid",
    "nullable": true
   },
   "decisions": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "recommendationId": {
       "type": "string"
      },
      "decision": {
       "type": "string",
       "enum": [
        "accepted",
        "modified",
        "rejected",
        "requiresReview"
       ]
      },
      "modifiedValue": {
       "type": "string",
       "nullable": true
      }
     }
    },
    "description": "Administrator's classification of each recommendation"
   },
   "createDraft": {
    "type": "boolean",
    "description": "Build the draft product from the accepted/modified recommendations"
   }
  }
 },
 "AiCatalogueBuilderConfigurationReviewView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What AI Catalogue Builder & Configuration Review displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "prompt": {
    "type": "string",
    "description": "Natural-language request",
    "nullable": true
   },
   "sessionId": {
    "type": "string",
    "description": "Review session id",
    "format": "uuid"
   },
   "inputMethod": {
    "type": "string",
    "enum": [
     "naturalLanguage",
     "excel",
     "csv",
     "pdf",
     "brochure",
     "existingCatalogue",
     "referenceProduct"
    ],
    "description": "Input method (pack p.12)"
   },
   "fileId": {
    "type": "string",
    "description": "Uploaded source file id",
    "nullable": true
   },
   "referenceProductId": {
    "type": "string",
    "description": "Existing product used as reference",
    "format": "uuid",
    "nullable": true
   },
   "recommendations": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "recommendationId": {
       "type": "string"
      },
      "area": {
       "type": "string",
       "enum": [
        "productStructure",
        "ticketType",
        "nameDescription",
        "validity",
        "pricing",
        "entitlements",
        "eligibility",
        "capacity",
        "channels",
        "media",
        "relationships",
        "policies",
        "missingInformation"
       ]
      },
      "sourceExcerpt": {
       "type": "string",
       "description": "Source"
      },
      "interpretation": {
       "type": "string",
       "description": "AI interpretation"
      },
      "proposedValue": {
       "type": "string",
       "description": "Proposed TICVAI configuration"
      },
      "confidence": {
       "type": "string",
       "enum": [
        "high",
        "medium",
        "low",
        "requiresClarification",
        "missing"
       ]
      },
      "decision": {
       "type": "string",
       "enum": [
        "accepted",
        "modified",
        "rejected",
        "requiresReview"
       ]
      },
      "modifiedValue": {
       "type": "string",
       "nullable": true
      }
     }
    },
    "description": "AI recommendations: Source -> AI interpretation -> Proposed configuration, with confidence and the administrator's classification"
   },
   "draftProductId": {
    "type": "string",
    "description": "Draft product built from the accepted recommendations",
    "format": "uuid",
    "nullable": true
   }
  }
 },
 "BulkProductCreationCatalogueImportInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Bulk Product Creation & Catalogue Import submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "rowCorrections": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "row": {
       "type": "integer"
      },
      "field": {
       "type": "string"
      },
      "value": {
       "type": "string"
      }
     }
    },
    "description": "Corrections to individual records before re-validating"
   },
   "excludedRows": {
    "type": "array",
    "items": {
     "type": "integer"
    },
    "description": "Rows to exclude"
   },
   "jobId": {
    "type": "string",
    "description": "Existing job to re-validate or commit; empty to start a new one",
    "format": "uuid",
    "nullable": true
   },
   "fileId": {
    "type": "string",
    "description": "Uploaded source file id"
   },
   "sourceFormat": {
    "type": "string",
    "enum": [
     "excel",
     "csv",
     "spreadsheetTemplate",
     "catalogueFile",
     "pdfBrochure",
     "productDocument"
    ],
    "description": "Supported source (pack p.6)"
   },
   "targetVenueId": {
    "type": "string",
    "description": "Target venue/site",
    "format": "uuid"
   },
   "defaultTemplateId": {
    "type": "string",
    "description": "Default product configuration (template) applied to every row",
    "format": "uuid",
    "nullable": true
   },
   "columnMapping": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "sourceColumn": {
       "type": "string"
      },
      "targetField": {
       "type": "string"
      }
     }
    },
    "description": "Source columns mapped to TICVAI fields"
   },
   "mode": {
    "type": "string",
    "enum": [
     "validate",
     "commit"
    ],
    "description": "validate previews without creating; commit runs the import (decided 29 September, readiness close-out)"
   }
  }
 },
 "BulkProductCreationCatalogueImportView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Bulk Product Creation & Catalogue Import displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "previewProducts": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "row": {
       "type": "integer"
      },
      "productName": {
       "type": "string"
      },
      "productType": {
       "$ref": "#/components/schemas/ProductKind"
      },
      "excluded": {
       "type": "boolean"
      },
      "aiProposed": {
       "type": "boolean"
      }
     }
    },
    "description": "Products that the import will create, previewed before creation; all are created in draft"
   },
   "validationIssues": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "row": {
       "type": "integer"
      },
      "field": {
       "type": "string"
      },
      "code": {
       "type": "string",
       "enum": [
        "missingRequired",
        "invalidValue",
        "unknownReference",
        "duplicate",
        "unmappedColumn"
       ]
      },
      "message": {
       "type": "string"
      }
     }
    },
    "description": "Record errors to correct before import (decided 29 September, readiness close-out)"
   },
   "excludedRows": {
    "type": "array",
    "items": {
     "type": "integer"
    },
    "description": "Rows excluded from the import"
   },
   "jobId": {
    "type": "string",
    "description": "Import job id",
    "format": "uuid"
   },
   "status": {
    "type": "string",
    "description": "Job status: parsing, previewReady, committing, committed or failed (as CatalogueImportJob)"
   },
   "sourceFormat": {
    "type": "string",
    "enum": [
     "excel",
     "csv",
     "spreadsheetTemplate",
     "catalogueFile",
     "pdfBrochure",
     "productDocument"
    ],
    "description": "Supported source (pack p.6)"
   },
   "targetVenueId": {
    "type": "string",
    "description": "Target venue/site",
    "format": "uuid"
   },
   "parsedCount": {
    "type": "integer",
    "description": "Records parsed"
   },
   "createdCount": {
    "type": "integer",
    "description": "Products created (after commit)"
   },
   "failedCount": {
    "type": "integer",
    "description": "Records failed"
   },
   "errorReportUrl": {
    "type": "string",
    "description": "Downloadable error report",
    "format": "uri",
    "nullable": true
   }
  }
 },
 "CatalogueConfigStatus": {
  "type": "string",
  "enum": [
   "draft",
   "active",
   "inactive",
   "retired"
  ],
  "description": "**The status of a catalogue configuration record** (29 September, data model DM3): price lists, rates, fees and fee rules, tax profiles and rules, calculation and rounding profiles, package pricing and templates. `draft` is being prepared and is never used by a calculation; `active` is in use from its effective date; `inactive` is switched off and may be switched back; `retired` is kept for history only. A record already used by a live price becomes `active` through a published change request, not by an edit."
 },
 "Channel": {
  "type": "string",
  "enum": [
   "pos",
   "kiosk",
   "web",
   "mobile",
   "b2b",
   "ota",
   "callCentre"
  ]
 },
 "ChannelPublicationAvailabilityInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Channel Publication & Availability submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "channels": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "channel": {
       "$ref": "#/components/schemas/Channel"
      },
      "enabled": {
       "type": "boolean"
      },
      "siteIds": {
       "type": "array",
       "items": {
        "type": "string"
       },
       "description": "Specific sites/webstores; empty = all"
      },
      "posGroupIds": {
       "type": "array",
       "items": {
        "type": "string"
       },
       "description": "Specific POS groups; empty = all"
      },
      "venueIds": {
       "type": "array",
       "items": {
        "type": "string"
       },
       "description": "Availability by venue; empty = all the product's venues"
      },
      "effectiveFrom": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      },
      "effectiveTo": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      }
     }
    },
    "description": "Channels the product is published on, with channel-specific sites, POS groups, venues and effective dates"
   },
   "productId": {
    "type": "string",
    "description": "Product id",
    "format": "uuid"
   }
  }
 },
 "ChannelPublicationAvailabilityView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Channel Publication & Availability displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "channels": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "channel": {
       "$ref": "#/components/schemas/Channel"
      },
      "enabled": {
       "type": "boolean"
      },
      "siteIds": {
       "type": "array",
       "items": {
        "type": "string"
       },
       "description": "Specific sites/webstores; empty = all"
      },
      "posGroupIds": {
       "type": "array",
       "items": {
        "type": "string"
       },
       "description": "Specific POS groups; empty = all"
      },
      "venueIds": {
       "type": "array",
       "items": {
        "type": "string"
       },
       "description": "Availability by venue; empty = all the product's venues"
      },
      "effectiveFrom": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      },
      "effectiveTo": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      }
     }
    },
    "description": "Channels the product is published on, with channel-specific sites, POS groups, venues and effective dates"
   },
   "publicationPreview": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "channel": {
       "$ref": "#/components/schemas/Channel"
      },
      "venueId": {
       "type": "string"
      },
      "exposed": {
       "type": "boolean"
      },
      "reason": {
       "type": "string",
       "nullable": true
      }
     }
    },
    "description": "Preview of where the product will actually be on sale"
   },
   "validationIssues": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "code": {
       "type": "string",
       "enum": [
        "channelNotConfigured",
        "noPriceForChannel",
        "noCapacityAllocation",
        "productNotApproved",
        "venueNotAssigned"
       ]
      },
      "message": {
       "type": "string"
      }
     }
    },
    "description": "Missing channel dependencies (decided 29 September, readiness close-out)"
   },
   "productId": {
    "type": "string",
    "description": "Product id",
    "format": "uuid"
   },
   "issuedEntitlementsUnaffected": {
    "type": "integer",
    "description": "Valid issued tickets/entitlements that remain valid whatever the channel change (pack p.10 Important Rule)"
   }
  }
 },
 "ConfigurationTemplate": {
  "type": "object",
  "x-ticvai-persistence": "catalogue.configuration_template",
  "description": "**A reusable starting point for a product or a price list** (29 September, data model DM3). Merges the product duplication and template library (ADM-126) and price list templates (ADM-063). `subject` says which; a template copies the listed components and marks `reviewFields` for the operator to confirm.",
  "required": [
   "id",
   "scopePath",
   "subject",
   "name",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Operations write it at `venue` scope."
   },
   "subject": {
    "type": "string",
    "enum": [
     "product",
     "priceList"
    ]
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "description": {
    "type": "string",
    "nullable": true
   },
   "templateKind": {
    "type": "string",
    "maxLength": 60,
    "nullable": true,
    "description": "Product: `ProductDuplicationTemplateLibraryView.templateKind`; price list: its `templateType`."
   },
   "productKind": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ProductKind"
     }
    ],
    "nullable": true
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "sourceProductId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "sourcePriceListId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "includedComponents": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Product or price-list component names, per `subject`."
   },
   "reviewFields": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "dates",
      "prices",
      "venue",
      "capacity",
      "event",
      "tax",
      "channels"
     ]
    }
   },
   "isAiDrafted": {
    "type": "boolean",
    "default": false
   },
   "status": {
    "allOf": [
     {
      "$ref": "#/components/schemas/CatalogueConfigStatus"
     }
    ],
    "default": "draft"
   },
   "ownerPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "createdAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "CreateProductRequest": {
  "type": "object",
  "required": [
   "code",
   "name",
   "kind",
   "venueId"
  ],
  "properties": {
   "code": {
    "type": "string",
    "maxLength": 64,
    "pattern": "^[A-Za-z0-9_-]+$",
    "x-ticvai-unique": "tenant",
    "description": "**Unique per tenant** (decided 28 September, audit R108). A code already used by any product in the tenant, at any venue, is refused with `409 duplicate-code`.\n"
   },
   "familyKey": {
    "type": "string",
    "maxLength": 64,
    "pattern": "^[A-Za-z0-9_-]+$",
    "nullable": true,
    "x-ticvai-unique": "venue",
    "description": "The product family across the tenant's venues (decided 29 September, rev 3 REV3-18); see `Product.familyKey`. At most one product per venue in a family, else `409 duplicate-code`."
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "description": {
    "type": "string"
   },
   "kind": {
    "$ref": "#/components/schemas/ProductKind"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "channels": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/Channel"
    }
   },
   "entitlementTemplateId": {
    "type": "string",
    "format": "uuid"
   },
   "dataMaskValues": {
    "type": "object",
    "additionalProperties": true
   },
   "guestListing": {
    "$ref": "#/components/schemas/GuestListing"
   },
   "notBookableLabel": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "nullable": true
   },
   "salesContact": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ProductSalesContact"
     }
    ],
    "nullable": true,
    "description": "See `Product.salesContact` (W3, 29 September)."
   },
   "bookingFlowId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "See `Product.bookingFlowId` (W8, W12, 29 September)."
   },
   "displayTags": {
    "type": "array",
    "maxItems": 6,
    "items": {
     "$ref": "#/components/schemas/ProductDisplayTag"
    }
   },
   "media": {
    "type": "array",
    "maxItems": 20,
    "items": {
     "$ref": "#/components/schemas/ProductMedia"
    }
   },
   "consentQuestionIds": {
    "type": "array",
    "maxItems": 10,
    "uniqueItems": true,
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "requiresTimeWindow": {
    "type": "boolean"
   }
  }
 },
 "GuestListing": {
  "type": "string",
  "enum": [
   "bookable",
   "infoOnly",
   "hidden"
  ],
  "default": "bookable",
  "description": "**How a product appears to a guest** (decided 29 September, rev 3 REV3-14). `bookable`: listed and searched while it is on sale, and added to the basket. `infoOnly`: listed and searched with its details, photo and `notBookableLabel` whether or not it is on sale, and **never added to a basket** (`addCartLine` refuses it with `409`); the screen opens its details instead. `hidden`: never listed or searched for a guest, and reachable only where a staff channel sells it. Independent of `isSellable`, which says whether a channel may sell it at all.\n"
 },
 "LifecycleStatusWorkflowConfigurationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Lifecycle Status & Workflow Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "availableLifecycleStatuses": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "state": {
       "$ref": "#/components/schemas/ProductLifecycleState"
      },
      "label": {
       "type": "string",
       "description": "Venue's display label for the state"
      },
      "enabled": {
       "type": "boolean"
      }
     }
    },
    "description": "Available lifecycle statuses, in sequence order; states come from ProductLifecycleState, the venue sets labels and switches optional ones off (decided 29 September, readiness close-out)"
   },
   "allowedStatusTransitions": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "from": {
       "$ref": "#/components/schemas/ProductLifecycleState"
      },
      "to": {
       "$ref": "#/components/schemas/ProductLifecycleState"
      },
      "initiatorRoles": {
       "type": "array",
       "items": {
        "type": "string"
       },
       "description": "Roles that can initiate this transition"
      },
      "trigger": {
       "type": "string",
       "enum": [
        "manual",
        "automatic"
       ],
       "description": "Whether the transition is manual or automatic (scheduler)"
      },
      "approvalRequired": {
       "type": "boolean"
      },
      "requiredSections": {
       "type": "array",
       "items": {
        "type": "string",
        "enum": [
         "validity",
         "entitlements",
         "capacity",
         "pricing",
         "eligibility",
         "media",
         "channels",
         "policies"
        ]
       },
       "description": "Required information / validation before the transition (the completeness sections of p.5)"
      },
      "effectiveDateRequired": {
       "type": "boolean"
      },
      "reasonRequired": {
       "type": "boolean",
       "description": "Reason/comment required"
      },
      "notifyRoles": {
       "type": "array",
       "items": {
        "type": "string"
       },
       "description": "Notification triggers: roles notified when the transition happens (sent through the central notifications module)"
      }
     }
    },
    "description": "Allowed status transitions, each with its initiator roles, trigger, approval, required information, effective-date, reason and notification rules"
   },
   "statusSpecificEditPermissions": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "state": {
       "$ref": "#/components/schemas/ProductLifecycleState"
      },
      "editableByRoles": {
       "type": "array",
       "items": {
        "type": "string"
       }
      },
      "lockedSections": {
       "type": "array",
       "items": {
        "type": "string"
       }
      }
     }
    },
    "description": "Status-specific edit permissions: who may edit a product in each state, and which sections are locked"
   }
  }
 },
 "LifecycleStatusWorkflowConfigurationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Lifecycle Status & Workflow Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "availableLifecycleStatuses": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "state": {
       "$ref": "#/components/schemas/ProductLifecycleState"
      },
      "label": {
       "type": "string",
       "description": "Venue's display label for the state"
      },
      "enabled": {
       "type": "boolean"
      }
     }
    },
    "description": "Available lifecycle statuses, in sequence order; states come from ProductLifecycleState, the venue sets labels and switches optional ones off (decided 29 September, readiness close-out)"
   },
   "allowedStatusTransitions": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "from": {
       "$ref": "#/components/schemas/ProductLifecycleState"
      },
      "to": {
       "$ref": "#/components/schemas/ProductLifecycleState"
      },
      "initiatorRoles": {
       "type": "array",
       "items": {
        "type": "string"
       },
       "description": "Roles that can initiate this transition"
      },
      "trigger": {
       "type": "string",
       "enum": [
        "manual",
        "automatic"
       ],
       "description": "Whether the transition is manual or automatic (scheduler)"
      },
      "approvalRequired": {
       "type": "boolean"
      },
      "requiredSections": {
       "type": "array",
       "items": {
        "type": "string",
        "enum": [
         "validity",
         "entitlements",
         "capacity",
         "pricing",
         "eligibility",
         "media",
         "channels",
         "policies"
        ]
       },
       "description": "Required information / validation before the transition (the completeness sections of p.5)"
      },
      "effectiveDateRequired": {
       "type": "boolean"
      },
      "reasonRequired": {
       "type": "boolean",
       "description": "Reason/comment required"
      },
      "notifyRoles": {
       "type": "array",
       "items": {
        "type": "string"
       },
       "description": "Notification triggers: roles notified when the transition happens (sent through the central notifications module)"
      }
     }
    },
    "description": "Allowed status transitions, each with its initiator roles, trigger, approval, required information, effective-date, reason and notification rules"
   },
   "statusSpecificEditPermissions": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "state": {
       "$ref": "#/components/schemas/ProductLifecycleState"
      },
      "editableByRoles": {
       "type": "array",
       "items": {
        "type": "string"
       }
      },
      "lockedSections": {
       "type": "array",
       "items": {
        "type": "string"
       }
      }
     }
    },
    "description": "Status-specific edit permissions: who may edit a product in each state, and which sections are locked"
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
 "Product": {
  "x-ticvai-persistence": "catalogue.product",
  "type": "object",
  "required": [
   "id",
   "code",
   "name",
   "kind",
   "venueId",
   "scopePath",
   "isSellable",
   "hasVariants"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "code": {
    "type": "string",
    "maxLength": 64
   },
   "familyKey": {
    "type": "string",
    "maxLength": 64,
    "pattern": "^[A-Za-z0-9_-]+$",
    "nullable": true,
    "x-ticvai-unique": "venue",
    "description": "**The same product at another location** (decided 29 September, rev 3 REV3-18). Optional. A tenant that sells one attraction at several venues gives each venue's product the same key, e.g. `aquarium-entry`; the key names the family across the tenant and each venue has at most one product in it, so a second product at the same venue with the key is refused with `409 duplicate-code`. **What it is for:** when a guest changes location on the booking screen (the 'Booking at' switcher, `BookingFlowConfig.locationSwitcher`), lines whose product shares a `familyKey` with a product at the new venue are carried over to that product, with times and prices refreshed; every other line is cleared. Null means the product belongs to no family and its lines always clear on a switch. Compared case-insensitively, like `code`.\n"
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "description": {
    "type": "string"
   },
   "kind": {
    "$ref": "#/components/schemas/ProductKind"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string"
   },
   "createdByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "1.4.18. **The approval gate refuses an approver who is the author, and nothing recorded either.** `SeatBlock`, `DelegatedAccess` and `ManualDiscountRequest` all carry this and the product passing through approval did not.\n"
   },
   "approvedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true
   },
   "responsibleDepartmentId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Who owns this product commercially. A scope node at `department` level."
   },
   "onSaleFrom": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "1.4.8. **A seasonal product should not need somebody awake at midnight.** Archiving already runs on a timer in this contract, so the machinery exists; `effectiveFrom` appears on tax codes, FX rates and white-label policies and not here.\n"
   },
   "onSaleTo": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "Retires the product automatically. **Retirement is not deletion** — the product stops selling and every order that referenced it still resolves.\n"
   },
   "categoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**Taken from their `fnb.product` and `retail.product`, 20 September.** `catalogue.product_category` has existed since 20 August with two operations and nothing could be filed under it — a merchandise hierarchy with a tree and no leaves. Their per-domain product tables both carried this column and ours did not.\n"
   },
   "lifecycleState": {
    "$ref": "#/components/schemas/ProductLifecycleState"
   },
   "isSellable": {
    "type": "boolean",
    "readOnly": true,
    "description": "True only when live **and** carried by a published bundle. Approval and publication are different acts.\n**Derived, never set.** It changes when `transitionProductLifecycle` moves the product and when `publishBundle` carries it, so `updateProduct` does not take it — `withdraw` is how a product stops selling.\n"
   },
   "isStockTracked": {
    "type": "boolean",
    "default": false,
    "description": "**Taken from their `fnb.product`, 20 September.** Whether a sale decrements stock, which is not what `isSellable` asks. A ticket is sellable and tracks no stock; a bottle of water is both. Without it, an F&B sale cannot tell inventory whether to move.\n"
   },
   "hasVariants": {
    "type": "boolean"
   },
   "variantCount": {
    "type": "integer"
   },
   "segmentTags": {
    "type": "array",
    "description": "7.3.5. **A channel and a segment tag are mandatory and nothing required either.** A catalogue that cannot be filtered by segment is a catalogue nobody can report on.\n**Hierarchical, not flat** — `family/with-toddlers` narrows `family` without duplicating it, which is how the promotions engine already treats scope.\n**A level is a tag under `level/`** (decided 29 September, rev 3 REV3-19): `level/beginner`, `level/intermediate`, `level/advanced`, `level/expert` (proposed codes, client to correct). A guest screen filters on it with `listProducts` `segmentTag`, and the words a guest reads beside each option come from `ProductCategory.description`, not from the tag.\n",
    "items": {
     "type": "string"
    }
   },
   "codeSchema": {
    "type": "string",
    "readOnly": true,
    "description": "7.3.4 specifies `[ParkCode]-[ProductType]-[Variant]`. **`Product.code` existed and nothing required a format**, so a venue with three thousand products had three thousand conventions.\nThe tenant sets the pattern and the platform generates against it. **Validation is the point, not the string** — a code typed by hand is a code that will not sort.\n"
   },
   "channels": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/Channel"
    }
   },
   "entitlementTemplateId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "What the buyer receives. Null for products that grant nothing — F&B and retail. Identity and entitlement are separate concerns.\n"
   },
   "blockedOffline": {
    "type": "boolean",
    "description": "True for seated and retail. Seated because a seat map is not a count; retail because stock depletes in real time.\n"
   },
   "dataMaskValues": {
    "type": "object",
    "additionalProperties": true,
    "description": "Custom fields. JSONB-backed, defined by the venue's data mask."
   },
   "guestListing": {
    "$ref": "#/components/schemas/GuestListing"
   },
   "notBookableLabel": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "nullable": true,
    "description": "The label a guest reads on an `infoOnly` product, e.g. *Info only* or *Not bookable online; ask at the desk* (decided 29 September, rev 3 REV3-14). Each value at most 60 characters. Null means the guest screen shows its default wording. Ignored unless `guestListing` is `infoOnly`.\n"
   },
   "salesContact": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ProductSalesContact"
     }
    ],
    "nullable": true,
    "description": "**Who a guest contacts to book a view-only product** (decided 29 September, W3), e.g. a training course listed with full details and no Book button. Shown as *Call sales* and *Email sales* on an `infoOnly` product. Null means the venue's own contact (white-label `getTenantAppStatus.contact`). Ignored unless `guestListing` is `infoOnly`.\n"
   },
   "bookingFlowId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**The booking flow this product is sold through** (decided 29 September, W8 and W12): a white-label `BookingFlow` of the venue, which orders the guest's steps (for a workshop, the product first and then the date and time). Null means the category's flow (`ProductCategory.bookingFlowId`), and failing that the venue's flow for the product's `kind`. Written by `createProduct` and `updateProduct`, which refuse an id that is not a flow of the venue with `422`.\n"
   },
   "displayTags": {
    "type": "array",
    "maxItems": 6,
    "items": {
     "$ref": "#/components/schemas/ProductDisplayTag"
    },
    "description": "**Short facts a guest reads on the ticket card and under *Read more***: *2 Hours*, *Min 1.10 m*, *Free adult entry*, *Valid 90 days*, *Emirates ID* (decided 29 September, 23SEP-3). Not `segmentTags`, which are for reporting and segmentation and which a guest never reads.\n**Derived on read when none are set.** When the venue has written no tags, a read returns tags derived from the product's duration (`clock`), entitlement validity (`calendar`) and the eligibility rule's `minHeightCm` (`height`), each marked `derived: true`; they are never stored. Once the venue writes any tag, only what it wrote is returned. Whether the guest screen shows them is `BookingFlowConfig.ticketTags` (white-label).\n"
   },
   "media": {
    "type": "array",
    "maxItems": 20,
    "items": {
     "$ref": "#/components/schemas/ProductMedia"
    },
    "description": "**The product's own photos and video** (decided 29 September, 23SEP-4). *Read more* opens on the `isPrimary` item, and a listing shows each product's primary image, so two tickets in one category no longer share the category's picture (`ProductCategory.imageAssetId`).\nEvery `assetId` names an asset of the asset library (`assets.yaml` `MediaAsset`) in status `ready` whose kind matches `kind`; anything else is a `422`. **Exactly one item is `isPrimary`** when the list is not empty, and an `assetId` appears once; otherwise `400`. Setting the list records each reference as asset usage (`MediaUsage` with `surface: product`, `referenceId` the product id, `isLive` true while the product is listed to guests), which is what stops a used asset being archived from under the product.\n"
   },
   "consentQuestionIds": {
    "type": "array",
    "maxItems": 10,
    "uniqueItems": true,
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "**The consent questions a guest answers when booking this product**, in the order they are asked (decided 29 September, rev 3 REV3-26): *Are you able to swim?*, *Do you hold a scuba certification?*, *I accept the risk*. Each id names a consent question defined in marketing-crm (`ConsentQuestion`), which owns the text, its version and whether it is asked per person or once per booking; the answer is stored there as a consent record (question version, answer, who answered, when). **One question or several, as the venue chooses.** A flow can carry its own list too (`white-label.BookingFlow.settings.consentQuestionIds`, on the product's published booking flow as `getPublishedBookingFlow` resolves it: product, then category, then the venue's flow for the kind; moved from `BookingFlowConfig` 29 September, W12); a booking asks the union of the flow's questions and those of every product in the cart, each question once (`orders.Cart.consentQuestions`). An id that names no active consent question of the tenant is a `422`.\n"
   },
   "requiresTimeWindow": {
    "type": "boolean",
    "default": false,
    "description": "**True for a space sold by the hour**, e.g. a meeting room type (decided 29 September, rev 3 REV3-13). The product is the room type (*focus pod*, *majlis*, *boardroom*, *auditorium*), never a named room; its lengths are a `length` axis (`setProductAttributes`) whose values carry `durationMinutes`, and each length is a variant priced on its own in the price list, so price is the room rate for that length. The cart line carries the booked start and end (orders), the end being the start plus the chosen variant's `durationMinutes`; `resources.listProductStartTimes` supplies the start times for a variant and a date and `allocateResources` picks the room from the product's resource requirements (`setExperienceResourceRequirements`) at checkout. True requires every active variant to have a `durationMinutes`; otherwise `422`.\n"
   },
   "productOwnerPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The product owner (29 September, data model DM3), set with `setProductContextOwnership`. `responsibleDepartmentId` is the owning department."
   },
   "operationalContact": {
    "type": "string",
    "maxLength": 200,
    "nullable": true,
    "description": "A principal id or a name, as the context screen takes it."
   },
   "businessUnitId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "legalEntityId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "A `ledger.legal_entity`, read through finance."
   },
   "attractionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "siteId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "locationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "brandId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The brand, as the context screen names it (a catalogue brand category)."
   },
   "marketCode": {
    "type": "string",
    "maxLength": 40,
    "nullable": true
   },
   "salesTerritory": {
    "type": "string",
    "maxLength": 100,
    "nullable": true
   }
  }
 },
 "ProductContextOwnershipAssignmentInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Product Context, Ownership & Assignment submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "businessUnit": {
    "type": "string",
    "description": "Business unit id",
    "nullable": true
   },
   "legalEntity": {
    "type": "string",
    "description": "Legal entity id",
    "nullable": true
   },
   "venue": {
    "type": "string",
    "description": "Venue id"
   },
   "attraction": {
    "type": "string",
    "description": "Attraction id",
    "nullable": true
   },
   "event": {
    "type": "string",
    "description": "Event id",
    "nullable": true
   },
   "site": {
    "type": "string",
    "description": "Site id",
    "nullable": true
   },
   "location": {
    "type": "string",
    "description": "Location id",
    "nullable": true
   },
   "productOwner": {
    "type": "string",
    "description": "Product owner (principal id)"
   },
   "responsibleDepartment": {
    "type": "string",
    "description": "Responsible department"
   },
   "operationalContact": {
    "type": "string",
    "description": "Operational contact (principal id or name)",
    "nullable": true
   },
   "customerSegment": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Applicable customer segments"
   },
   "market": {
    "type": "string",
    "description": "Market",
    "nullable": true
   },
   "salesTerritory": {
    "type": "string",
    "description": "Sales territory",
    "nullable": true
   },
   "brand": {
    "type": "string",
    "description": "Brand (catalogue brand category id)",
    "nullable": true
   },
   "productFamily": {
    "type": "string",
    "description": "Product family",
    "nullable": true
   },
   "productId": {
    "type": "string",
    "description": "Product id",
    "format": "uuid"
   }
  }
 },
 "ProductContextOwnershipAssignmentView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Product Context, Ownership & Assignment displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "tenant": {
    "type": "string",
    "description": "Tenant id (set from the caller's tenant)"
   },
   "businessUnit": {
    "type": "string",
    "description": "Business unit id",
    "nullable": true
   },
   "legalEntity": {
    "type": "string",
    "description": "Legal entity id",
    "nullable": true
   },
   "venue": {
    "type": "string",
    "description": "Venue id"
   },
   "attraction": {
    "type": "string",
    "description": "Attraction id",
    "nullable": true
   },
   "event": {
    "type": "string",
    "description": "Event id",
    "nullable": true
   },
   "site": {
    "type": "string",
    "description": "Site id",
    "nullable": true
   },
   "location": {
    "type": "string",
    "description": "Location id",
    "nullable": true
   },
   "productOwner": {
    "type": "string",
    "description": "Product owner (principal id)"
   },
   "creator": {
    "type": "string",
    "description": "Creator (principal id), recorded by the system"
   },
   "responsibleDepartment": {
    "type": "string",
    "description": "Responsible department"
   },
   "operationalContact": {
    "type": "string",
    "description": "Operational contact (principal id or name)",
    "nullable": true
   },
   "customerSegment": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Applicable customer segments"
   },
   "market": {
    "type": "string",
    "description": "Market",
    "nullable": true
   },
   "salesTerritory": {
    "type": "string",
    "description": "Sales territory",
    "nullable": true
   },
   "brand": {
    "type": "string",
    "description": "Brand (catalogue brand category id)",
    "nullable": true
   },
   "productFamily": {
    "type": "string",
    "description": "Product family",
    "nullable": true
   },
   "productId": {
    "type": "string",
    "description": "Product id",
    "format": "uuid"
   }
  }
 },
 "ProductDisplayTag": {
  "x-ticvai-persistence": "none — jsonb column on catalogue.product",
  "type": "object",
  "required": [
   "kind",
   "label"
  ],
  "description": "One short fact on a ticket card (decided 29 September, 23SEP-3). `kind` picks the icon.",
  "properties": {
   "kind": {
    "type": "string",
    "enum": [
     "clock",
     "height",
     "free",
     "calendar",
     "id"
    ],
    "description": "`clock` a duration, `height` a height rule, `free` something included free, `calendar` a validity, `id` a document the guest must bring."
   },
   "label": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "description": "What the guest reads, e.g. *2 Hours*. Each language value at most 40 characters."
   },
   "derived": {
    "type": "boolean",
    "readOnly": true,
    "default": false,
    "description": "True on a tag the server derived on read because the venue set none. Never sent."
   }
  }
 },
 "ProductDuplicationTemplateLibraryView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Product Duplication & Template Library displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "includedComponents": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "coreProductDetails",
      "validity",
      "pricingReferences",
      "entitlements",
      "capacityReferences",
      "eligibility",
      "salesChannels",
      "media",
      "policies",
      "rules",
      "content",
      "images",
      "relationships"
     ]
    },
    "description": "Duplication options copied by this template"
   },
   "templateId": {
    "type": "string",
    "description": "Template id",
    "format": "uuid"
   },
   "name": {
    "type": "string",
    "description": "Template name"
   },
   "templateKind": {
    "type": "string",
    "enum": [
     "standardAdmission",
     "childAdmission",
     "vipTicket",
     "timeslotTicket",
     "eventTicket",
     "groupProduct",
     "annualPass",
     "addOn",
     "venueSpecific"
    ],
    "description": "Template kind (Template Library, pack p.11)"
   },
   "productType": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ProductKind"
     }
    ],
    "description": "Product type the template creates"
   },
   "venueId": {
    "type": "string",
    "description": "Venue for a venue-specific template; empty for all venues",
    "format": "uuid",
    "nullable": true
   },
   "sourceProductId": {
    "type": "string",
    "description": "Product the template was saved from",
    "format": "uuid",
    "nullable": true
   },
   "reviewFields": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "dates",
      "prices",
      "venue",
      "capacity",
      "event",
      "tax",
      "channels"
     ]
    },
    "description": "Smart Clone: sensitive fields the user must review before the clone is saved (default all seven) (decided 29 September, readiness close-out)"
   },
   "updatedAt": {
    "type": "string",
    "description": "Last changed",
    "format": "date-time"
   }
  }
 },
 "ProductImportExportEnvironmentTransferView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Product Import / Export & Environment Transfer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "referenceMappings": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "kind": {
       "type": "string",
       "enum": [
        "venue",
        "location",
        "dependency"
       ]
      },
      "sourceRef": {
       "type": "string"
      },
      "targetRef": {
       "type": "string",
       "nullable": true
      }
     }
    },
    "description": "Venue/location and dependency references mapped from source to target"
   },
   "missingReferences": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "References with no mapping in the target environment"
   },
   "changePreview": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "productId": {
       "type": "string"
      },
      "component": {
       "type": "string"
      },
      "change": {
       "type": "string",
       "enum": [
        "create",
        "update",
        "unchanged",
        "conflict"
       ]
      },
      "detail": {
       "type": "string"
      }
     }
    },
    "description": "Source vs target comparison: what executing will change"
   },
   "transferId": {
    "type": "string",
    "description": "Transfer / package id",
    "format": "uuid"
   },
   "direction": {
    "type": "string",
    "enum": [
     "export",
     "import"
    ],
    "description": "Direction"
   },
   "sourceEnvironment": {
    "type": "string",
    "enum": [
     "development",
     "sandbox",
     "uat",
     "staging",
     "production"
    ],
    "description": "Environment (the pack's example list, p.7) (decided 29 September, readiness close-out)"
   },
   "targetEnvironment": {
    "type": "string",
    "enum": [
     "development",
     "sandbox",
     "uat",
     "staging",
     "production"
    ],
    "description": "Environment (the pack's example list, p.7) (decided 29 September, readiness close-out)"
   },
   "productIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "Products in the package"
   },
   "components": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "coreProductDetails",
      "validity",
      "pricingReferences",
      "entitlements",
      "capacityReferences",
      "eligibility",
      "salesChannels",
      "media",
      "policies",
      "rules",
      "relationships"
     ]
    },
    "description": "Associated configuration components included"
   },
   "status": {
    "type": "string",
    "description": "Transfer status: draft, validated, awaitingApproval, executing, completed or failed (decided 29 September, readiness close-out)"
   },
   "requestedBy": {
    "type": "string",
    "description": "Requested by (principal display name)"
   },
   "createdAt": {
    "type": "string",
    "description": "Created",
    "format": "date-time"
   },
   "completedAt": {
    "type": "string",
    "description": "Transfer result time",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "ProductKind": {
  "type": "string",
  "description": "**`openDated` added 24 August** from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no kind: **valid on any date within an eligible range, rather than for a named performance or a fixed date.**\nThe mechanism already existed — `access.entitlement` carries `valid_from`, `valid_to`, `entries_allowed` and `frozen_days`, which is exactly an open-dated pass. **What was missing was the product saying it is one**, so a catalogue could not offer it and a report could not count it.\n**`datedAdmission` is a different thing and the two were being conflated**: dated is *this Tuesday*, open-dated is *any Tuesday between March and June*. A guest buying the second and being sold the first has bought the wrong ticket.\n**Transport uses two existing kinds, not a new one** (decided 29 September, rev 3 REV3-21). A one-way trip is `timedAdmission`: `transport.createTransportRoute` creates the route's product with one variant per passenger type, and each departure is a performance. A multi-trip or unlimited pass is `openDated`: `transport.createTransportPassType` creates it, with `EntitlementTemplate.entriesAllowed` = the pass's trips (null for unlimited), the validity = `validityDays`, and `EntitlementTemplate.transportRestriction` naming the station pair the pass was bought for, so `access` refuses it on another journey. The sale path is unchanged: both are cart lines, priced by `transport.quoteTransportFare` (orders `TransportLineAttributes`).\n",
  "enum": [
   "admission",
   "timedAdmission",
   "datedAdmission",
   "openDated",
   "seated",
   "membership",
   "bundle",
   "fnb",
   "retail",
   "rental",
   "addOn",
   "giftCard"
  ]
 },
 "ProductLifecycleCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Product Lifecycle Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "lifecycleState": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ProductLifecycleState"
     }
    ],
    "description": "Current lifecycle state (see handoff for how the pack's 11 statuses map to it)"
   },
   "channelPublication": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "channel": {
       "$ref": "#/components/schemas/Channel"
      },
      "published": {
       "type": "boolean"
      },
      "effectiveFrom": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      }
     }
    },
    "description": "Publication status by channel"
   },
   "effectiveFrom": {
    "type": "string",
    "description": "Effective / activation date-time: when the product becomes commercially active",
    "format": "date-time",
    "nullable": true
   },
   "pendingActions": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "action": {
       "type": "string",
       "enum": [
        "publication",
        "salesStart",
        "activation",
        "salesSuspension",
        "deactivation",
        "endOfSale",
        "retirement",
        "approval"
       ]
      },
      "dueAt": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      }
     }
    },
    "description": "Pending lifecycle actions: scheduled or awaiting approval, soonest first"
   },
   "productId": {
    "type": "string",
    "description": "Product id",
    "format": "uuid"
   },
   "productName": {
    "type": "string",
    "description": "Internal product name"
   },
   "productType": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ProductKind"
     }
    ],
    "description": "Product type"
   },
   "venueId": {
    "type": "string",
    "description": "Venue id",
    "format": "uuid"
   },
   "locationId": {
    "type": "string",
    "description": "Location id",
    "format": "uuid",
    "nullable": true
   },
   "productOwner": {
    "type": "string",
    "description": "Product owner (principal display name)"
   },
   "responsibleDepartment": {
    "type": "string",
    "description": "Responsible department"
   },
   "effectiveTo": {
    "type": "string",
    "description": "End of the effective period; empty for open-ended",
    "format": "date-time",
    "nullable": true
   },
   "createdAt": {
    "type": "string",
    "description": "Creation date-time",
    "format": "date-time"
   },
   "lastModifiedAt": {
    "type": "string",
    "description": "Last modification date-time",
    "format": "date-time"
   },
   "validationIssues": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "code": {
       "type": "string",
       "enum": [
        "missingValidity",
        "missingEntitlements",
        "missingCapacity",
        "missingPricing",
        "missingEligibility",
        "missingMedia",
        "missingChannels",
        "missingPolicies",
        "missingOwner",
        "awaitingApproval"
       ]
      },
      "message": {
       "type": "string"
      }
     }
    },
    "description": "Incomplete configuration or publication blockers (pack p.4); codes follow the configuration-completeness sections of p.5 (decided 29 September, readiness close-out)"
   },
   "aiInsights": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "AI attention flags (incomplete setup, unusual configuration, approaching activation, lifecycle conflicts); advisory only"
   }
  }
 },
 "ProductLifecycleState": {
  "type": "string",
  "enum": [
   "draft",
   "inReview",
   "approved",
   "live",
   "withdrawn",
   "archived"
  ]
 },
 "ProductMedia": {
  "x-ticvai-persistence": "catalogue.product_media",
  "type": "object",
  "required": [
   "assetId",
   "kind",
   "isPrimary"
  ],
  "description": "One photo or video of a product, referencing the asset library (decided 29 September, 23SEP-4). One row per product and asset, so the asset library can answer which products use an asset.\n",
  "properties": {
   "assetId": {
    "type": "string",
    "format": "uuid",
    "description": "A `MediaAsset` of `assets.yaml`, in status `ready`."
   },
   "kind": {
    "type": "string",
    "enum": [
     "image",
     "video"
    ]
   },
   "isPrimary": {
    "type": "boolean",
    "default": false,
    "description": "The item *Read more* opens on and a listing shows. Exactly one per product."
   },
   "displayOrder": {
    "type": "integer",
    "default": 100
   },
   "altText": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "nullable": true
   }
  }
 },
 "ProductSalesContact": {
  "x-ticvai-persistence": "none — jsonb column on catalogue.product",
  "type": "object",
  "description": "Who to contact to book a view-only product (decided 29 September, W3). At least one of `phone` or `email`.\n",
  "minProperties": 1,
  "properties": {
   "phone": {
    "type": "string",
    "maxLength": 32,
    "nullable": true
   },
   "email": {
    "type": "string",
    "format": "email",
    "maxLength": 254,
    "nullable": true
   },
   "note": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "nullable": true,
    "description": "A line shown under the contact, e.g. *Group courses are booked by phone*. At most 200 characters per language."
   }
  }
 },
 "PublicationActivationSchedulerInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table covers these fields** — the closest is catalogue.channel_allocation at 4%, so this is not an update to anything the package stores today and no new table has been decided",
  "description": "**What Publication & Activation Scheduler submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "actionType": {
    "type": "string",
    "enum": [
     "publication",
     "salesStart",
     "activation",
     "salesSuspension",
     "deactivation",
     "endOfSale",
     "retirement"
    ],
    "description": "Scheduled action (Configurable Actions, pack p.10)"
   },
   "scheduledAt": {
    "type": "string",
    "description": "Date and time the action runs",
    "format": "date-time"
   },
   "timeZone": {
    "type": "string",
    "description": "IANA time zone the date is entered in"
   },
   "venueId": {
    "type": "string",
    "description": "Venue id",
    "nullable": true
   },
   "channels": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/Channel"
    },
    "description": "Channels the action applies to; empty = all"
   },
   "productId": {
    "type": "string",
    "description": "Product id",
    "format": "uuid"
   },
   "targetState": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ProductLifecycleState"
     }
    ],
    "description": "Lifecycle state the product moves to"
   },
   "notifyRoles": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Roles notified when the action runs or fails"
   },
   "preActionValidation": {
    "type": "boolean",
    "description": "Validate the product before running; the action fails with issues if blockers exist"
   },
   "failureHandling": {
    "type": "string",
    "enum": [
     "retryThenNotify",
     "skipAndNotify",
     "holdForManualAction"
    ],
    "description": "Failure handling when the action cannot run; default retryThenNotify (decided 29 September, readiness close-out)"
   },
   "scheduleId": {
    "type": "string",
    "description": "Existing scheduled action to change; empty to create",
    "format": "uuid",
    "nullable": true
   }
  }
 },
 "PublicationActivationSchedulerView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Publication & Activation Scheduler displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "actionType": {
    "type": "string",
    "enum": [
     "publication",
     "salesStart",
     "activation",
     "salesSuspension",
     "deactivation",
     "endOfSale",
     "retirement"
    ],
    "description": "Scheduled action (Configurable Actions, pack p.10)"
   },
   "scheduledAt": {
    "type": "string",
    "description": "Date and time the action runs",
    "format": "date-time"
   },
   "timeZone": {
    "type": "string",
    "description": "IANA time zone the date is entered in"
   },
   "venueId": {
    "type": "string",
    "description": "Venue id",
    "nullable": true
   },
   "channels": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/Channel"
    },
    "description": "Channels the action applies to; empty = all"
   },
   "productId": {
    "type": "string",
    "description": "Product id",
    "format": "uuid"
   },
   "targetState": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ProductLifecycleState"
     }
    ],
    "description": "Lifecycle state the product moves to"
   },
   "notifyRoles": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Roles notified when the action runs or fails"
   },
   "preActionValidation": {
    "type": "boolean",
    "description": "Validate the product before running; the action fails with issues if blockers exist"
   },
   "failureHandling": {
    "type": "string",
    "enum": [
     "retryThenNotify",
     "skipAndNotify",
     "holdForManualAction"
    ],
    "description": "Failure handling when the action cannot run; default retryThenNotify (decided 29 September, readiness close-out)"
   },
   "validationIssues": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "code": {
       "type": "string",
       "enum": [
        "afterValidityEnd",
        "overlapsOtherAction",
        "productNotApproved",
        "invalidTransition",
        "pastDate"
       ]
      },
      "message": {
       "type": "string"
      }
     }
    },
    "description": "Lifecycle conflicts found for this action (decided 29 September, readiness close-out)"
   },
   "scheduleId": {
    "type": "string",
    "description": "Scheduled action id",
    "format": "uuid"
   },
   "status": {
    "type": "string",
    "description": "Scheduled action status: scheduled, executed, failed or cancelled"
   },
   "failureReason": {
    "type": "string",
    "description": "Why the last run failed",
    "nullable": true
   }
  }
 }
}
```
