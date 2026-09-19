# WS43 — Product Lifecycle   Catalogue Governance board 1

**10 screens · 10 operations · 20 schemas · 2 permissions**

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
- **0 of these operations work offline**
  
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
| `ADM-125` | Publication & Activation Scheduler | listDetail | 1 | 0 | — |
| `ADM-126` | Product Duplication & Template Library | configEditor | 1 | 0 | — |
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
     "carries": [
      "tenantId"
     ],
     "provenance": "derived — ADM-002 declares entryState.params tenantId, so an edge into it must carry them"
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
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide administrators with a centralized operational view of every product and its current lifecycle state.",
  "purposeNote": "An authorized administrator can locate any product, identify its exact lifecycle state and determine the next required operational action from one screen.",
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
    "ProductLifecycleCommandCenterView.showCurrentLifecycleStatus",
    "ProductLifecycleCommandCenterView.oDraft",
    "ProductLifecycleCommandCenterView.oInConfiguration",
    "ProductLifecycleCommandCenterView.oPendingApproval",
    "ProductLifecycleCommandCenterView.oApproved"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-118"
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
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide a governed starting point for creating a new ticketing product.",
  "purposeNote": "A new product can be created and saved in Draft without becoming commercially available until all required configuration and governance conditions are satisfied.",
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
    "trigger": "onAction",
    "invalidates": [
     "createProduct"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-119"
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
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure how products move between lifecycle states.",
  "purposeNote": "Administrators can configure a controlled product lifecycle without development or database changes.",
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
    "trigger": "onAction",
    "invalidates": [
     "setLifecycleStatuWorkflow"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-120"
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
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow large catalogues to be created efficiently rather than configuring every product manually. This directly addresses the matrix requirement for catalogue creation through bulk-file upload.",
  "purposeNote": "An administrator can convert a large existing catalogue into draft TICVAI products through a controlled import and validation process.",
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
    "trigger": "onAction",
    "invalidates": [
     "createBulkProductCatalogue"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-121"
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
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow controlled movement of product configurations between TICVAI environments. This covers the matrix requirement for importing/exporting catalogue products between different environments.",
  "purposeNote": "Products can be moved between authorized environments without manually recreating their configuration and without silently overwriting incompatible production settings.",
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
    "ProductImportExportEnvironmentTransferView.mapVenueLocationReferences",
    "ProductImportExportEnvironmentTransferView.mapDependencies",
    "ProductImportExportEnvironmentTransferView.detectMissingReferences",
    "ProductImportExportEnvironmentTransferView.previewChanges",
    "ProductImportExportEnvironmentTransferView.executeTransfer"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-122"
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
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Define where the product belongs and who is responsible for it.",
  "purposeNote": "Every governed product has clearly defined ownership, organizational context and operational/commercial assignment.",
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
    "trigger": "onAction",
    "invalidates": [
     "setProductContextOwnership"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-123"
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
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Control where a product may be exposed for sale.",
  "purposeNote": "An authorized user can control precisely which approved channels expose a product while previously issued valid entitlements remain unaffected unless a separate governed action explicitly changes them.",
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
    "trigger": "onAction",
    "invalidates": [
     "publishChannelAvailability"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-124"
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
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Automate future product lifecycle actions.",
  "purposeNote": "Products can automatically enter or leave defined commercial lifecycle states at configured times without manual intervention.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 10"
   },
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
     "components": []
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
    "trigger": "onAction",
    "invalidates": [
     "publishActivationScheduler"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-125"
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
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Duplication Options) and no display directory — it is settings, not a population",
  "purpose": "Accelerate product configuration by allowing administrators to reuse proven configurations. The source matrix explicitly requires duplication of products together with associated configuration, rules, pricing and entitlements.",
  "purposeNote": "Users can create a new Draft product from an existing product/template while preventing accidental reuse of inappropriate dates, venues, prices or other context-sensitive values.",
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
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-126"
  },
  "apisNote": "Regenerated 9 September 2026 from Product_Lifecycle___Catalogue_Governance_Reference.pdf page 11. 0 of 0 labels bound to a contract property; 13 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide TICVAI's AI-first interface for accelerating product creation and configuration. This directly supports the matrix requirement allowing administrators to upload spreadsheets, brochures, PDFs or existing catalogues and use AI to generate product structures, pricing, rules, entitlements and configurations. Board 2 governs what happens after a product has been created or while an existing product is being changed.",
  "purposeNote": "An administrator can transform unstructured or semi-structured commercial information into a structured Draft product configuration, review every AI-generated recommendation and approve or modify it before the normal lifecycle workflow begins. Board 1 — Final Screen Register",
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
    "trigger": "onAction",
    "invalidates": [
     "setCatalogueReview"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-127"
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
  "parameters": [],
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
  "parameters": [],
  "requestBody": null,
  "responds": "ProductDuplicationTemplateLibraryView"
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
  "parameters": [],
  "requestBody": null,
  "responds": "ProductImportExportEnvironmentTransferView"
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
  "parameters": [],
  "requestBody": null,
  "responds": "ProductLifecycleCommandCenterView"
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
  "parameters": [],
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
  "parameters": [],
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
  "parameters": [],
  "requestBody": "AiCatalogueBuilderConfigurationReviewInput",
  "responds": "AiCatalogueBuilderConfigurationReviewView"
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
  "parameters": [],
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
  "parameters": [],
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
   "typeANaturalLanguageRequest": {
    "type": "string",
    "description": "Type a natural-language request"
   },
   "andPublishingIt": {
    "type": "string",
    "description": "and publishing it"
   },
   "productSafely": {
    "type": "string",
    "description": "product safely?”"
   },
   "eventualDesign": {
    "type": "string",
    "description": "eventual design"
   },
   "scheduledLifecycleGovernanceAndOwnership": {
    "type": "string",
    "format": "date-time",
    "description": "scheduled lifecycle governance and ownership"
   },
   "scheduledLifecycleGovernanceAndAccountability": {
    "type": "string",
    "format": "date-time",
    "description": "scheduled lifecycle governance and accountability"
   }
  }
 },
 "AiCatalogueBuilderConfigurationReviewView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What AI Catalogue Builder & Configuration Review displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "typeANaturalLanguageRequest": {
    "type": "string",
    "description": "Type a natural-language request"
   },
   "andPublishingIt": {
    "type": "string",
    "description": "and publishing it"
   },
   "productSafely": {
    "type": "string",
    "description": "product safely?”"
   },
   "eventualDesign": {
    "type": "string",
    "description": "eventual design"
   },
   "scheduledLifecycleGovernanceAndOwnership": {
    "type": "string",
    "format": "date-time",
    "description": "scheduled lifecycle governance and ownership"
   },
   "scheduledLifecycleGovernanceAndAccountability": {
    "type": "string",
    "format": "date-time",
    "description": "scheduled lifecycle governance and accountability"
   }
  }
 },
 "BulkProductCreationCatalogueImportInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Bulk Product Creation & Catalogue Import submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "excel": {
    "type": "string",
    "description": "Excel"
   },
   "csv": {
    "type": "string",
    "description": "CSV"
   },
   "structuredSpreadsheetTemplates": {
    "type": "string",
    "description": "Structured spreadsheet templates"
   },
   "existingCatalogueFiles": {
    "type": "string",
    "description": "Existing catalogue files"
   },
   "pdfBrochures": {
    "type": "string",
    "description": "PDF brochures"
   },
   "productDocuments": {
    "type": "string",
    "description": "Product documents"
   },
   "previewProductsBeforeCreation": {
    "type": "string",
    "description": "Preview products before creation"
   },
   "correctErrors": {
    "type": "integer",
    "description": "Correct errors"
   },
   "excludeSelectedRecords": {
    "type": "string",
    "description": "Exclude selected records"
   }
  }
 },
 "BulkProductCreationCatalogueImportView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Bulk Product Creation & Catalogue Import displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "excel": {
    "type": "string",
    "description": "Excel"
   },
   "csv": {
    "type": "string",
    "description": "CSV"
   },
   "structuredSpreadsheetTemplates": {
    "type": "string",
    "description": "Structured spreadsheet templates"
   },
   "existingCatalogueFiles": {
    "type": "string",
    "description": "Existing catalogue files"
   },
   "pdfBrochures": {
    "type": "string",
    "description": "PDF brochures"
   },
   "productDocuments": {
    "type": "string",
    "description": "Product documents"
   },
   "previewProductsBeforeCreation": {
    "type": "string",
    "description": "Preview products before creation"
   },
   "correctErrors": {
    "type": "integer",
    "description": "Correct errors"
   },
   "excludeSelectedRecords": {
    "type": "string",
    "description": "Exclude selected records"
   }
  }
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
   "enableDisableChannels": {
    "type": "boolean",
    "description": "Enable/disable channels"
   },
   "previewPublicationStatus": {
    "type": "string",
    "description": "Preview publication status"
   },
   "detectMissingChannelDependencies": {
    "type": "string",
    "description": "Detect missing channel dependencies"
   }
  }
 },
 "ChannelPublicationAvailabilityView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Channel Publication & Availability displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "enableDisableChannels": {
    "type": "boolean",
    "description": "Enable/disable channels"
   },
   "previewPublicationStatus": {
    "type": "string",
    "description": "Preview publication status"
   },
   "detectMissingChannelDependencies": {
    "type": "string",
    "description": "Detect missing channel dependencies"
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
    "pattern": "^[A-Za-z0-9_-]+$"
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
   }
  }
 },
 "LifecycleStatusWorkflowConfigurationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Lifecycle Status & Workflow Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "availableLifecycleStatuses": {
    "type": "string",
    "description": "Available lifecycle statuses"
   },
   "statusSequence": {
    "type": "string",
    "description": "Status sequence"
   },
   "allowedStatusTransitions": {
    "type": "string",
    "description": "Allowed status transitions"
   },
   "requiredInformationBeforeTransition": {
    "type": "string",
    "description": "Required information before transition"
   },
   "whetherApprovalIsRequired": {
    "type": "boolean",
    "description": "Whether approval is required"
   },
   "notificationTriggers": {
    "type": "string",
    "description": "Notification triggers"
   },
   "effectiveDateRequirements": {
    "type": "string",
    "format": "date-time",
    "description": "Effective-date requirements"
   },
   "validationRequirements": {
    "type": "string",
    "description": "Validation requirements"
   },
   "reasonCommentRequirements": {
    "type": "string",
    "description": "Reason/comment requirements"
   },
   "statusSpecificEditPermissions": {
    "type": "string",
    "description": "Status-specific edit permissions"
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
    "type": "string",
    "description": "Available lifecycle statuses"
   },
   "statusSequence": {
    "type": "string",
    "description": "Status sequence"
   },
   "allowedStatusTransitions": {
    "type": "string",
    "description": "Allowed status transitions"
   },
   "requiredInformationBeforeTransition": {
    "type": "string",
    "description": "Required information before transition"
   },
   "whetherApprovalIsRequired": {
    "type": "boolean",
    "description": "Whether approval is required"
   },
   "notificationTriggers": {
    "type": "string",
    "description": "Notification triggers"
   },
   "effectiveDateRequirements": {
    "type": "string",
    "format": "date-time",
    "description": "Effective-date requirements"
   },
   "validationRequirements": {
    "type": "string",
    "description": "Validation requirements"
   },
   "reasonCommentRequirements": {
    "type": "string",
    "description": "Reason/comment requirements"
   },
   "statusSpecificEditPermissions": {
    "type": "string",
    "description": "Status-specific edit permissions"
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
   "lifecycleState": {
    "$ref": "#/components/schemas/ProductLifecycleState"
   },
   "isSellable": {
    "type": "boolean",
    "description": "True only when live **and** carried by a published bundle. Approval and publication are different acts.\n"
   },
   "hasVariants": {
    "type": "boolean"
   },
   "variantCount": {
    "type": "integer"
   },
   "segmentTags": {
    "type": "array",
    "description": "7.3.5. **A channel and a segment tag are mandatory and nothing required either.** A catalogue that cannot be filtered by segment is a catalogue nobody can report on.\n**Hierarchical, not flat** — `family/with-toddlers` narrows `family` without duplicating it, which is how the promotions engine already treats scope.\n",
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
   }
  }
 },
 "ProductContextOwnershipAssignmentInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Product Context, Ownership & Assignment submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "tenant": {
    "type": "string",
    "description": "Tenant"
   },
   "businessUnit": {
    "type": "string",
    "description": "Business unit"
   },
   "legalEntity": {
    "type": "string",
    "description": "Legal entity"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "attraction": {
    "type": "string",
    "description": "Attraction"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "site": {
    "type": "string",
    "description": "Site"
   },
   "location": {
    "type": "string",
    "description": "Location"
   },
   "productOwner": {
    "type": "string",
    "description": "Product owner"
   },
   "creator": {
    "type": "string",
    "description": "Creator"
   },
   "responsibleDepartment": {
    "type": "string",
    "description": "Responsible department"
   },
   "operationalContact": {
    "type": "string",
    "description": "Operational contact"
   },
   "customerSegment": {
    "type": "string",
    "description": "Customer segment"
   },
   "market": {
    "type": "string",
    "description": "Market"
   },
   "salesTerritory": {
    "type": "string",
    "description": "Sales territory"
   },
   "brand": {
    "type": "string",
    "description": "Brand"
   },
   "productFamily": {
    "type": "string",
    "description": "Product family"
   },
   "segments": {
    "type": "string",
    "description": "segments"
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
    "description": "Tenant"
   },
   "businessUnit": {
    "type": "string",
    "description": "Business unit"
   },
   "legalEntity": {
    "type": "string",
    "description": "Legal entity"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "attraction": {
    "type": "string",
    "description": "Attraction"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "site": {
    "type": "string",
    "description": "Site"
   },
   "location": {
    "type": "string",
    "description": "Location"
   },
   "productOwner": {
    "type": "string",
    "description": "Product owner"
   },
   "creator": {
    "type": "string",
    "description": "Creator"
   },
   "responsibleDepartment": {
    "type": "string",
    "description": "Responsible department"
   },
   "operationalContact": {
    "type": "string",
    "description": "Operational contact"
   },
   "customerSegment": {
    "type": "string",
    "description": "Customer segment"
   },
   "market": {
    "type": "string",
    "description": "Market"
   },
   "salesTerritory": {
    "type": "string",
    "description": "Sales territory"
   },
   "brand": {
    "type": "string",
    "description": "Brand"
   },
   "productFamily": {
    "type": "string",
    "description": "Product family"
   },
   "segments": {
    "type": "string",
    "description": "segments"
   }
  }
 },
 "ProductDuplicationTemplateLibraryView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Product Duplication & Template Library displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "optionsType": {
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
    ],
    "description": "Vocabulary listed under Duplication Options."
   },
   "standardAdmission": {
    "type": "string",
    "description": "Standard Admission"
   },
   "childAdmission": {
    "type": "string",
    "description": "Child Admission"
   },
   "vipTicket": {
    "type": "string",
    "description": "VIP Ticket"
   },
   "timeslotTicket": {
    "type": "string",
    "description": "Timeslot Ticket"
   },
   "eventTicket": {
    "type": "string",
    "description": "Event Ticket"
   },
   "groupProduct": {
    "type": "string",
    "description": "Group Product"
   },
   "annualPass": {
    "type": "string",
    "description": "Annual Pass"
   },
   "addOn": {
    "type": "string",
    "description": "Add-On"
   },
   "venueSpecificTemplates": {
    "type": "string",
    "description": "Venue-specific templates"
   },
   "dates": {
    "type": "string",
    "description": "Dates"
   },
   "prices": {
    "type": "string",
    "description": "Prices"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "capacity": {
    "type": "integer",
    "description": "Capacity"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "tax": {
    "type": "string",
    "description": "Tax"
   },
   "channels": {
    "type": "string",
    "description": "Channels"
   }
  }
 },
 "ProductImportExportEnvironmentTransferView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Product Import / Export & Environment Transfer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "mapVenueLocationReferences": {
    "type": "string",
    "description": "Map venue/location references"
   },
   "mapDependencies": {
    "type": "string",
    "description": "Map dependencies"
   },
   "detectMissingReferences": {
    "type": "string",
    "description": "Detect missing references"
   },
   "previewChanges": {
    "type": "string",
    "description": "Preview changes"
   },
   "executeTransfer": {
    "type": "string",
    "description": "Execute transfer"
   }
  }
 },
 "ProductKind": {
  "type": "string",
  "description": "**`openDated` added 24 August** from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no kind: **valid on any date within an eligible range, rather than for a named performance or a fixed date.**\nThe mechanism already existed — `access.entitlement` carries `valid_from`, `valid_to`, `entries_allowed` and `frozen_days`, which is exactly an open-dated pass. **What was missing was the product saying it is one**, so a catalogue could not offer it and a report could not count it.\n**`datedAdmission` is a different thing and the two were being conflated**: dated is *this Tuesday*, open-dated is *any Tuesday between March and June*. A guest buying the second and being sold the first has bought the wrong ticket.\n",
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
   "showCurrentLifecycleStatus": {
    "type": "string",
    "description": "Show current lifecycle status"
   },
   "oDraft": {
    "type": "string",
    "description": "o Draft"
   },
   "oInConfiguration": {
    "type": "string",
    "description": "o In Configuration"
   },
   "oPendingApproval": {
    "type": "string",
    "description": "o Pending Approval"
   },
   "oApproved": {
    "type": "string",
    "description": "o Approved"
   },
   "oScheduled": {
    "type": "string",
    "format": "date-time",
    "description": "o Scheduled"
   },
   "oPublished": {
    "type": "string",
    "description": "o Published"
   },
   "oActive": {
    "type": "integer",
    "description": "o Active"
   },
   "oSuspended": {
    "type": "string",
    "description": "o Suspended"
   },
   "oDisabled": {
    "type": "string",
    "description": "o Disabled"
   },
   "oRetired": {
    "type": "string",
    "description": "o Retired"
   },
   "oArchived": {
    "type": "string",
    "description": "o Archived"
   },
   "showPublicationStatusByChannel": {
    "type": "string",
    "description": "Show publication status by channel"
   },
   "displayEffectiveActivationDates": {
    "type": "string",
    "description": "Display effective/activation dates"
   },
   "showPendingLifecycleActions": {
    "type": "string",
    "description": "Show pending lifecycle actions"
   },
   "allowAdvancedFilteringBy": {
    "type": "boolean",
    "description": "Allow advanced filtering by"
   },
   "oProductType": {
    "type": "string",
    "description": "o Product type"
   },
   "oVenue": {
    "type": "string",
    "description": "o Venue"
   },
   "oLocation": {
    "type": "string",
    "description": "o Location"
   },
   "oStatus": {
    "type": "string",
    "description": "o Status"
   },
   "oOwner": {
    "type": "string",
    "description": "o Owner"
   },
   "oDepartment": {
    "type": "string",
    "description": "o Department"
   },
   "oChannel": {
    "type": "string",
    "description": "o Channel"
   },
   "oEffectiveDate": {
    "type": "string",
    "format": "date-time",
    "description": "o Effective date"
   },
   "oCreationDate": {
    "type": "string",
    "format": "date-time",
    "description": "o Creation date"
   },
   "oLastModification": {
    "type": "string",
    "description": "o Last modification"
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
 "PublicationActivationSchedulerInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table covers these fields** — the closest is catalogue.channel_allocation at 4%, so this is not an update to anything the package stores today and no new table has been decided",
  "description": "**What Publication & Activation Scheduler submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "publication": {
    "type": "string",
    "description": "Publication"
   },
   "salesStart": {
    "type": "string",
    "description": "Sales start"
   },
   "activation": {
    "type": "string",
    "description": "Activation"
   },
   "salesSuspension": {
    "type": "string",
    "description": "Sales suspension"
   },
   "deactivation": {
    "type": "string",
    "description": "Deactivation"
   },
   "endOfSale": {
    "type": "string",
    "description": "End of sale"
   },
   "retirementTrigger": {
    "type": "string",
    "description": "Retirement trigger"
   },
   "date": {
    "type": "string",
    "format": "date-time",
    "description": "Date"
   },
   "time": {
    "type": "string",
    "format": "date-time",
    "description": "Time"
   },
   "timeZone": {
    "type": "string",
    "format": "date-time",
    "description": "Time zone"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "statusTransition": {
    "type": "string",
    "description": "Status transition"
   },
   "notification": {
    "type": "string",
    "description": "Notification"
   },
   "preActionValidation": {
    "type": "string",
    "description": "Pre-action validation"
   },
   "failureHandling": {
    "type": "string",
    "description": "Failure handling"
   },
   "upcomingActivations": {
    "type": "string",
    "description": "Upcoming activations"
   },
   "upcomingPublications": {
    "type": "string",
    "description": "Upcoming publications"
   },
   "endOfSaleDates": {
    "type": "string",
    "description": "End-of-sale dates"
   },
   "scheduledSuspensions": {
    "type": "string",
    "format": "date-time",
    "description": "Scheduled suspensions"
   },
   "lifecycleConflicts": {
    "type": "string",
    "description": "Lifecycle conflicts"
   },
   "failedScheduledJobs": {
    "type": "string",
    "format": "date-time",
    "description": "Failed scheduled jobs"
   }
  }
 },
 "PublicationActivationSchedulerView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Publication & Activation Scheduler displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "publication": {
    "type": "string",
    "description": "Publication"
   },
   "salesStart": {
    "type": "string",
    "description": "Sales start"
   },
   "activation": {
    "type": "string",
    "description": "Activation"
   },
   "salesSuspension": {
    "type": "string",
    "description": "Sales suspension"
   },
   "deactivation": {
    "type": "string",
    "description": "Deactivation"
   },
   "endOfSale": {
    "type": "string",
    "description": "End of sale"
   },
   "retirementTrigger": {
    "type": "string",
    "description": "Retirement trigger"
   },
   "date": {
    "type": "string",
    "format": "date-time",
    "description": "Date"
   },
   "time": {
    "type": "string",
    "format": "date-time",
    "description": "Time"
   },
   "timeZone": {
    "type": "string",
    "format": "date-time",
    "description": "Time zone"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "statusTransition": {
    "type": "string",
    "description": "Status transition"
   },
   "notification": {
    "type": "string",
    "description": "Notification"
   },
   "preActionValidation": {
    "type": "string",
    "description": "Pre-action validation"
   },
   "failureHandling": {
    "type": "string",
    "description": "Failure handling"
   },
   "upcomingActivations": {
    "type": "string",
    "description": "Upcoming activations"
   },
   "upcomingPublications": {
    "type": "string",
    "description": "Upcoming publications"
   },
   "endOfSaleDates": {
    "type": "string",
    "description": "End-of-sale dates"
   },
   "scheduledSuspensions": {
    "type": "string",
    "format": "date-time",
    "description": "Scheduled suspensions"
   },
   "lifecycleConflicts": {
    "type": "string",
    "description": "Lifecycle conflicts"
   },
   "failedScheduledJobs": {
    "type": "string",
    "format": "date-time",
    "description": "Failed scheduled jobs"
   }
  }
 }
}
```
