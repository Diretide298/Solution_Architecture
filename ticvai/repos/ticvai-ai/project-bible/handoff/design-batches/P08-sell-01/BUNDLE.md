# P08-sell-01 — P08 · Sell (1 of 4)

**10 screens · 67 operations · 57 schemas · 10 permissions**

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

- **Every control that can be refused must be gated.** 10 permissions apply here:
  `CAPACITY_CONFIGURE, EVENT_CONFIGURE, PARTNER_MANAGE, PARTNER_VIEW, PERFORMANCE_CONFIGURE, PRICE_CONFIGURE, PRICE_VIEW, PRODUCT_CONFIGURE, PRODUCT_VIEW, REPORT_VIEW_VENUE`. A control nobody can use must say so,
  not sit enabled and fail.
- **12 of these operations work offline**: evaluatePromotions, getPerformance, getProduct, getPromotion, listCatalogueBundles, listEntitlementTemplates, listMerchandise, listPerformances
  — and the rest do not. A surface that looks the same online and off is lying.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-007` | Product Directory | listDetail | 14 | 0 | — |
| `BO-009` | Pricing Rules | listDetail | 7 | 0 | — |
| `BO-010` | Promotions & Coupons | listDetail | 19 | 1 | — |
| `BO-011` | Packages & Bundles | listDetail | 5 | 0 | — |
| `BO-012` | Membership Products | listDetail | 12 | 0 | — |
| `BO-013` | Channel & Distribution | listDetail | 10 | 0 | — |
| `BO-014` | Catalogue Publishing | listDetail | 13 | 0 | — |
| `BO-015` | Session Calendar | listDetail | 11 | 1 | — |
| `BO-016` | Session Template | listDetail | 11 | 1 | — |
| `BO-017` | Capacity Management | listDetail | 6 | 0 | — |

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-007",
  "name": "Product Directory",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/product-directory",
   "component": "apps/venue-management-web/src/routes/venue-operations/ProductDirectoryDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-001",
    "BO-008",
    "BO-009",
    "BO-010",
    "BO-045",
    "BO-112"
   ],
   "inferred": true,
   "entryFrom": [
    "BO-083",
    "BO-102"
   ],
   "transitions": [
    {
     "to": "BO-045",
     "trigger": "Menu Management",
     "provenance": "flow F85 step 4→5"
    },
    {
     "to": "BO-112",
     "trigger": "Production Planning & Production Sheets",
     "provenance": "flow F78 step 2→3"
    },
    {
     "to": "BO-001",
     "trigger": "Queue Directory",
     "carries": [
      "eventId",
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "carries": [
      "productId",
      "venueId"
     ],
     "provenance": "derived — BO-008 declares entryState.params productId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-009",
     "trigger": "Pricing Rules",
     "carries": [
      "priceListId"
     ],
     "provenance": "derived — BO-009 declares entryState.params priceListId, so an edge into it must carry them"
    },
    {
     "to": "BO-010",
     "trigger": "Promotions & Coupons",
     "carries": [
      "campaignId",
      "code",
      "dashboardId",
      "promotionId",
      "reportId",
      "venueId"
     ],
     "provenance": "derived — BO-010 declares entryState.params campaignId, code, dashboardId, promotionId, reportId, venueId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Improved 20 August against the client design board.** Answers 5 board screen(s): Menu & Product Command Center; Product / PLU Master; Variants, Modifiers & Special Selling Rules and 2 more. **The board specifies this screen further rather than replacing it** — the id, its flows and its navigation are unchanged, which is what keeps 3,184 traceability rows and every board anchor pointing at something real. **Retail board operations wired 24 August.**",
  "density": "compact",
  "boardFrames": [
   "FnB Board 2.dc.html#fnb-2c",
   "Retail Board 2.dc.html#ret-2a",
   "Retail Board 2.dc.html#ret-2b"
  ],
  "pattern": "listDetail",
  "patternReason": "`listProducts` reads the population and `getProduct` reads one of them — list, select, act",
  "purpose": "Find anything sellable at this venue.",
  "gaps": [
   {
    "operation": "listAlternativeCodes",
    "why": "**4 declared operations reach no component on this screen**: listAlternativeCodes, listProductVariants, listMenus, listMerchandise. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
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
       "label": "Every product",
       "bindsTo": "Product",
       "columns": [
        "Product.id",
        "Product.code",
        "Product.name",
        "Product.description",
        "Product.kind",
        "Product.venueId",
        "Product.scopePath",
        "Product.createdByPrincipalId",
        "Product.approvedByPrincipalId",
        "Product.responsibleDepartmentId",
        "Product.onSaleFrom",
        "Product.onSaleTo"
       ],
       "operation": "listProducts",
       "provenance": "contract catalogue.yaml GET /products"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected product",
       "bindsTo": "Product",
       "columns": [
        "Product.id",
        "Product.code",
        "Product.name",
        "Product.description",
        "Product.kind",
        "Product.venueId",
        "Product.scopePath",
        "Product.createdByPrincipalId",
        "Product.approvedByPrincipalId",
        "Product.responsibleDepartmentId",
        "Product.onSaleFrom",
        "Product.onSaleTo",
        "Product.lifecycleState",
        "Product.isSellable",
        "Product.hasVariants",
        "Product.variantCount"
       ],
       "operation": "getProduct",
       "provenance": "contract catalogue.yaml GET /products/{productId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create",
       "operation": "createProduct",
       "provenance": "contract catalogue.yaml POST /products"
      },
      {
       "kind": "secondaryButton",
       "label": "Resolve",
       "operation": "resolveProductByCode",
       "provenance": "contract catalogue.yaml GET /products/resolve"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "setAlternativeCodes",
       "provenance": "contract catalogue.yaml PUT /products/{productId}/alternative-codes"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "setProductAttributes",
       "provenance": "contract catalogue.yaml PUT /products/{productId}/attributes"
      },
      {
       "kind": "secondaryButton",
       "label": "Transition",
       "operation": "transitionProductLifecycle",
       "provenance": "contract catalogue.yaml POST /products/{productId}/lifecycle"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateProduct",
       "provenance": "contract catalogue.yaml PATCH /products/{productId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createMerchandise",
       "provenance": "contract retail.yaml POST /merchandise"
      },
      {
       "kind": "secondaryButton",
       "label": "Bulk",
       "operation": "bulkUpdateProducts",
       "provenance": "contract inventory.yaml POST /products/bulk"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "detailPanel",
       "notes": "Structure from the wireframe board. Components not yet enumerated.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listProducts",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createProduct",
       "label": "Create product",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createProduct",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The product list.",
   "error": "Could not load. Names which read failed and leaves the product untouched.",
   "emptyFirstRun": "No product yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the product are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listProducts",
    "contract": "catalogue",
    "purpose": "List products",
    "trigger": "onLoad"
   },
   {
    "operationId": "getProduct",
    "contract": "catalogue",
    "purpose": "Read a product",
    "trigger": "onLoad"
   },
   {
    "operationId": "createProduct",
    "contract": "catalogue",
    "purpose": "Create a product",
    "trigger": "onAction",
    "invalidates": [
     "listProducts"
    ]
   },
   {
    "operationId": "listAlternativeCodes",
    "contract": "catalogue",
    "purpose": "External identifiers for a product",
    "trigger": "onLoad"
   },
   {
    "operationId": "listProductVariants",
    "contract": "catalogue",
    "purpose": "List generated variants",
    "trigger": "onLoad"
   },
   {
    "operationId": "resolveProductByCode",
    "contract": "catalogue",
    "purpose": "Resolve a partner code to a product",
    "trigger": "onLoad"
   },
   {
    "operationId": "setAlternativeCodes",
    "contract": "catalogue",
    "purpose": "Set external identifiers",
    "trigger": "onAction",
    "invalidates": [
     "listProducts"
    ]
   },
   {
    "operationId": "setProductAttributes",
    "contract": "catalogue",
    "purpose": "Set the attribute axes for a product",
    "trigger": "onAction",
    "invalidates": [
     "listProducts"
    ]
   },
   {
    "operationId": "transitionProductLifecycle",
    "contract": "catalogue",
    "purpose": "Move a product through its lifecycle",
    "trigger": "onAction",
    "invalidates": [
     "listProducts"
    ]
   },
   {
    "operationId": "updateProduct",
    "contract": "catalogue",
    "purpose": "Update a product",
    "trigger": "onAction",
    "invalidates": [
     "listProducts"
    ]
   },
   {
    "operationId": "createMerchandise",
    "contract": "retail",
    "purpose": "Create a merchandise item",
    "trigger": "onAction",
    "invalidates": [
     "listProducts"
    ]
   },
   {
    "operationId": "listMenus",
    "contract": "fnb",
    "purpose": "List menus",
    "trigger": "onLoad"
   },
   {
    "operationId": "listMerchandise",
    "contract": "retail",
    "purpose": "List merchandise",
    "trigger": "onLoad"
   },
   {
    "operationId": "bulkUpdateProducts",
    "contract": "inventory",
    "purpose": "Change many products at once, with a preview",
    "trigger": "onAction",
    "invalidates": [
     "listProducts"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "productId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A shared product link after the product retired.** Shows what replaced it where a successor exists, and the catalogue where none does.",
   "preloaded": [
    "Product.id",
    "Product.code",
    "Product.name",
    "Product.description",
    "Product.kind"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-007",
   "source": "Claude Design Retail pack, 24 August",
   "note": "**Drawn by Claude Design on `Retail Board 2.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 14 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "BO-009",
  "name": "Pricing Rules",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/pricing-rules",
   "component": "apps/venue-management-web/src/routes/venue-operations/PricingRulesDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-001",
    "BO-007",
    "BO-008",
    "BO-010"
   ],
   "inferred": true,
   "entryFrom": [
    "BO-102",
    "BO-112"
   ],
   "transitions": [
    {
     "to": "BO-001",
     "trigger": "Queue Directory",
     "carries": [
      "eventId",
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-007",
     "trigger": "Product Directory",
     "carries": [
      "productId"
     ],
     "provenance": "derived — BO-007 declares entryState.params productId, so an edge into it must carry them"
    },
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "carries": [
      "productId",
      "venueId"
     ],
     "provenance": "derived — BO-008 declares entryState.params productId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-010",
     "trigger": "Promotions & Coupons",
     "carries": [
      "campaignId",
      "code",
      "dashboardId",
      "promotionId",
      "reportId",
      "venueId"
     ],
     "provenance": "derived — BO-010 declares entryState.params campaignId, code, dashboardId, promotionId, reportId, venueId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Improved 20 August against the client design board.** Answers 1 board screen(s): Price Book & Retail Pricing Management. **The board specifies this screen further rather than replacing it** — the id, its flows and its navigation are unchanged, which is what keeps 3,184 traceability rows and every board anchor pointing at something real.",
  "density": "compact",
  "boardFrames": [
   "Retail Board 2.dc.html#ret-2f"
  ],
  "pattern": "listDetail",
  "patternReason": "`listPriceLists` reads the population and `getPriceList` reads one of them — list, select, act",
  "purpose": "Set what something costs, and when that changes.",
  "gaps": [
   {
    "operation": "listPrices",
    "why": "**1 declared operation reach no component on this screen**: listPrices. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
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
       "label": "Every pricing rules",
       "bindsTo": "PriceList",
       "columns": [
        "PriceList.id",
        "PriceList.code",
        "PriceList.name",
        "PriceList.venueId",
        "PriceList.currency",
        "PriceList.currencyScale",
        "PriceList.channels",
        "PriceList.validFrom",
        "PriceList.validTo",
        "PriceList.priority"
       ],
       "operation": "listPriceLists",
       "provenance": "contract catalogue.yaml GET /price-lists"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected pricing rules",
       "bindsTo": "PriceList",
       "columns": [
        "PriceList.id",
        "PriceList.code",
        "PriceList.name",
        "PriceList.venueId",
        "PriceList.currency",
        "PriceList.currencyScale",
        "PriceList.channels",
        "PriceList.validFrom",
        "PriceList.validTo",
        "PriceList.priority"
       ],
       "operation": "getPriceList",
       "provenance": "contract catalogue.yaml GET /price-lists/{priceListId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create",
       "operation": "createPriceList",
       "provenance": "contract catalogue.yaml POST /price-lists"
      },
      {
       "kind": "secondaryButton",
       "label": "Copy",
       "operation": "copyPriceList",
       "provenance": "contract catalogue.yaml POST /price-lists/{priceListId}/copy"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "setPrices",
       "provenance": "contract catalogue.yaml PUT /price-lists/{priceListId}/prices"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updatePriceList",
       "provenance": "contract catalogue.yaml PATCH /price-lists/{priceListId}"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "detailPanel",
       "notes": "Structure from the wireframe board. Components not yet enumerated.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listPriceLists",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createPriceList",
       "label": "Create price list",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createPriceList",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The pricing rules list.",
   "error": "Could not load. Names which read failed and leaves the pricing rules untouched.",
   "emptyFirstRun": "No pricing rules yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the pricing rules are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPriceLists",
    "contract": "catalogue",
    "purpose": "List price lists",
    "trigger": "onLoad"
   },
   {
    "operationId": "listPrices",
    "contract": "catalogue",
    "purpose": "List prices in a list",
    "trigger": "onLoad"
   },
   {
    "operationId": "createPriceList",
    "contract": "catalogue",
    "purpose": "Create a price list",
    "trigger": "onAction",
    "invalidates": [
     "listPriceLists"
    ]
   },
   {
    "operationId": "copyPriceList",
    "contract": "catalogue",
    "purpose": "Copy a price list, optionally with an adjustment",
    "trigger": "onAction",
    "invalidates": [
     "listPriceLists"
    ]
   },
   {
    "operationId": "getPriceList",
    "contract": "catalogue",
    "purpose": "Read a price list",
    "trigger": "onLoad"
   },
   {
    "operationId": "setPrices",
    "contract": "catalogue",
    "purpose": "Set prices in bulk",
    "trigger": "onAction",
    "invalidates": [
     "listPriceLists"
    ]
   },
   {
    "operationId": "updatePriceList",
    "contract": "catalogue",
    "purpose": "Amend a price list",
    "trigger": "onAction",
    "invalidates": [
     "listPriceLists"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "priceListId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `priceListId`.",
   "preloaded": [
    "PriceList.id",
    "PriceList.code",
    "PriceList.name",
    "PriceList.venueId",
    "PriceList.currency"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-009",
   "source": "Claude Design Retail pack, 24 August",
   "note": "**Drawn by Claude Design on `Retail Board 2.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 7 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "BO-010",
  "name": "Promotions & Coupons",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/promotions-coupons",
   "component": "apps/venue-management-web/src/routes/venue-operations/PromotionsCouponsDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-001",
    "BO-007",
    "BO-008",
    "BO-009"
   ],
   "inferred": true,
   "entryFrom": [
    "BO-102",
    "BO-119"
   ],
   "transitions": [
    {
     "to": "BO-001",
     "trigger": "Queue Directory",
     "carries": [
      "eventId",
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-007",
     "trigger": "Product Directory",
     "carries": [
      "productId"
     ],
     "provenance": "derived — BO-007 declares entryState.params productId, so an edge into it must carry them"
    },
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "carries": [
      "productId",
      "venueId"
     ],
     "provenance": "derived — BO-008 declares entryState.params productId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-009",
     "trigger": "Pricing Rules",
     "carries": [
      "priceListId"
     ],
     "provenance": "derived — BO-009 declares entryState.params priceListId, so an edge into it must carry them"
    },
    {
     "to": "ANL-009",
     "trigger": "AI Assistant & Action Center",
     "provenance": "flow F90 step 2→3",
     "crossesDevice": true,
     "back": false
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Improved 20 August against the client design board.** Answers 6 board screen(s): Retail Commercial Command Center; Promotion & Offer Builder; Promotion Eligibility, Priority & Conflict Rules and 3 more. **The board specifies this screen further rather than replacing it** — the id, its flows and its navigation are unchanged, which is what keeps 3,184 traceability rows and every board anchor pointing at something real. **Owns POS board frame(s) POS-4E** (client pack, 24 August). **Assigned by board purpose rather than by operation overlap** — three attempts at deriving that mapping produced plausible nonsense, and a reader who trusts a bad table is worse off than one who has none. **Retail board operations wired 24 August.**",
  "density": "compact",
  "boardFrames": [
   "POS Board 4.dc.html#pos-4e",
   "Retail Board 5.dc.html#ret-5a",
   "Retail Board 5.dc.html#ret-5b",
   "Retail Board 5.dc.html#ret-5c",
   "Retail Board 5.dc.html#ret-5e"
  ],
  "pattern": "listDetail",
  "patternReason": "`listPromotions` reads the population and `getPromotion` reads one of them — list, select, act",
  "purpose": "Issue a code and control what it does.",
  "gaps": [
   {
    "operation": "listCouponCampaigns",
    "why": "**4 declared operations reach no component on this screen**: listCouponCampaigns, getPromotionUsage, listCouponCodes, getDashboard. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
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
       "label": "Every promotions coupons",
       "bindsTo": "Promotion",
       "columns": [
        "Promotion.code",
        "Promotion.name",
        "Promotion.description",
        "Promotion.venueId",
        "Promotion.discount",
        "Promotion.conditions",
        "Promotion.stackingMode",
        "Promotion.stackingGroup",
        "Promotion.precedence",
        "Promotion.validFrom",
        "Promotion.validTo",
        "Promotion.maxRedemptions"
       ],
       "operation": "listPromotions",
       "provenance": "contract promotions.yaml GET /promotions"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected promotions coupons",
       "bindsTo": "Promotion",
       "columns": [
        "Promotion.code",
        "Promotion.name",
        "Promotion.description",
        "Promotion.venueId",
        "Promotion.discount",
        "Promotion.conditions",
        "Promotion.stackingMode",
        "Promotion.stackingGroup",
        "Promotion.precedence",
        "Promotion.validFrom",
        "Promotion.validTo",
        "Promotion.maxRedemptions",
        "Promotion.maxRedemptionsPerGuest",
        "Promotion.budgetCap",
        "Promotion.id",
        "Promotion.status"
       ],
       "operation": "getPromotion",
       "provenance": "contract promotions.yaml GET /promotions/{promotionId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Analyse",
       "operation": "analysePromotionConflicts",
       "provenance": "contract promotions.yaml GET /promotions/{promotionId}/conflicts"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createCouponCampaign",
       "provenance": "contract promotions.yaml POST /coupon-campaigns"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createPromotion",
       "provenance": "contract promotions.yaml POST /promotions"
      },
      {
       "kind": "secondaryButton",
       "label": "End",
       "operation": "endPromotion",
       "provenance": "contract promotions.yaml POST /promotions/{promotionId}/end"
      },
      {
       "kind": "secondaryButton",
       "label": "Evaluate",
       "operation": "evaluatePromotions",
       "provenance": "contract promotions.yaml POST /promotions/evaluate"
      },
      {
       "kind": "secondaryButton",
       "label": "Generate",
       "operation": "generateCouponCodes",
       "provenance": "contract promotions.yaml POST /coupon-campaigns/{campaignId}/codes"
      },
      {
       "kind": "secondaryButton",
       "label": "Pause",
       "operation": "pausePromotion",
       "provenance": "contract promotions.yaml POST /promotions/{promotionId}/pause"
      },
      {
       "kind": "secondaryButton",
       "label": "Publish",
       "operation": "publishPromotion",
       "provenance": "contract promotions.yaml POST /promotions/{promotionId}/publish"
      },
      {
       "kind": "secondaryButton",
       "label": "Unschedule",
       "operation": "unschedulePromotion",
       "provenance": "contract promotions.yaml POST /promotions/{promotionId}/unschedule"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updatePromotion",
       "provenance": "contract promotions.yaml PATCH /promotions/{promotionId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Simulate",
       "operation": "simulatePromotion",
       "provenance": "contract promotions.yaml POST /promotions/{promotionId}/simulate"
      },
      {
       "kind": "secondaryButton",
       "label": "Run",
       "operation": "runReport",
       "provenance": "contract reporting.yaml POST /reports/{reportId}/run"
      },
      {
       "kind": "destructiveButton",
       "label": "Void",
       "operation": "voidCouponCode",
       "provenance": "contract promotions.yaml POST /coupon-codes/{code}/void"
      },
      {
       "kind": "publishGate",
       "label": "What publishing changes",
       "notes": "**Names what goes live, where, and from when.** A publish with no stated consequence is one somebody presses meaning to save.",
       "provenance": "authored — required by check-screens"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "detailPanel",
       "notes": "Structure from the wireframe board. Components not yet enumerated.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listPromotions",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createCouponCampaign",
       "label": "Create coupon campaign",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "destructiveButton",
       "derived": true,
       "impliedBy": "voidCouponCode",
       "label": "Void coupon code",
       "notes": "**Always confirms, never the default focus.** The consequence goes in the body — *cancel 3 orders worth AED 480* is a confirmation, *are you sure* is not.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createCouponCampaign",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "confirmDialog",
       "derived": true,
       "label": "Confirm",
       "notes": "**The consequence goes in the body, not the title.** *Cancel 3 orders worth AED 480* is a confirmation; *are you sure* is not — and a dialog that cannot name what it destroys is a dialog somebody dismisses.\n\n**Added 31 August.** `confirmDialog` and `modal` were both in the component library and used **zero times across 492 screens**, while `destructiveButton` was used 39 times and its own entry reads *always requires confirmation*.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "publishGate",
       "impliedBy": "publishPromotion",
       "notes": "Declares `publishPromotion`. **The gate names what the publish will affect before it happens** — a disabled Publish with no reason is the state operators escalate.\n",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmVoidCouponCode",
    "component": "confirmDialog",
    "trigger": "Void",
    "body": "**Names what `voidCouponCode` changes and what it leaves alone**, in the consequence rather than the verb. A promotions coupons this affects should be identified in the dialog, not just counted.",
    "provenance": "contract promotions.yaml POST /coupon-codes/{code}/void"
   }
  ],
  "states": {
   "loading": "The promotions coupons list.",
   "error": "Could not load. Names which read failed and leaves the promotions coupons untouched.",
   "emptyFirstRun": "No promotions coupons yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the promotions coupons are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPromotions",
    "contract": "promotions",
    "purpose": "List promotions",
    "trigger": "onLoad"
   },
   {
    "operationId": "listCouponCampaigns",
    "contract": "promotions",
    "purpose": "List coupon campaigns",
    "trigger": "onLoad"
   },
   {
    "operationId": "analysePromotionConflicts",
    "contract": "promotions",
    "purpose": "Analyse stacking against live promotions",
    "trigger": "onLoad"
   },
   {
    "operationId": "createCouponCampaign",
    "contract": "promotions",
    "purpose": "Create a coupon campaign",
    "trigger": "onAction",
    "invalidates": [
     "listPromotions"
    ]
   },
   {
    "operationId": "createPromotion",
    "contract": "promotions",
    "purpose": "Create a promotion",
    "trigger": "onAction",
    "invalidates": [
     "listPromotions"
    ]
   },
   {
    "operationId": "endPromotion",
    "contract": "promotions",
    "purpose": "End a promotion early",
    "trigger": "onAction",
    "invalidates": [
     "listPromotions"
    ]
   },
   {
    "operationId": "evaluatePromotions",
    "contract": "promotions",
    "purpose": "Evaluate promotions against a cart",
    "trigger": "onAction",
    "invalidates": [
     "listPromotions"
    ]
   },
   {
    "operationId": "generateCouponCodes",
    "contract": "promotions",
    "purpose": "Generate codes in bulk",
    "trigger": "onAction",
    "invalidates": [
     "listPromotions"
    ]
   },
   {
    "operationId": "getPromotion",
    "contract": "promotions",
    "purpose": "Read a promotion",
    "trigger": "onLoad"
   },
   {
    "operationId": "getPromotionUsage",
    "contract": "promotions",
    "purpose": "Redemption count and discount given",
    "trigger": "onLoad"
   },
   {
    "operationId": "listCouponCodes",
    "contract": "promotions",
    "purpose": "List generated codes",
    "trigger": "onLoad"
   },
   {
    "operationId": "pausePromotion",
    "contract": "promotions",
    "purpose": "Pause a live promotion",
    "trigger": "onAction",
    "invalidates": [
     "listPromotions"
    ]
   },
   {
    "operationId": "publishPromotion",
    "contract": "promotions",
    "purpose": "Publish a promotion",
    "trigger": "onAction",
    "invalidates": [
     "listPromotions"
    ]
   },
   {
    "operationId": "unschedulePromotion",
    "contract": "promotions",
    "purpose": "Pull a scheduled promotion before it starts",
    "trigger": "onAction",
    "invalidates": [
     "listPromotions"
    ]
   },
   {
    "operationId": "updatePromotion",
    "contract": "promotions",
    "purpose": "Amend a promotion",
    "trigger": "onAction",
    "invalidates": [
     "listPromotions"
    ]
   },
   {
    "operationId": "getDashboard",
    "contract": "reporting",
    "purpose": "Read a dashboard with tile data",
    "trigger": "onLoad"
   },
   {
    "operationId": "simulatePromotion",
    "contract": "promotions",
    "purpose": "What this promotion would have cost on real history",
    "trigger": "onAction",
    "invalidates": [
     "listPromotions"
    ]
   },
   {
    "operationId": "runReport",
    "contract": "reporting",
    "purpose": "Run a report",
    "trigger": "onAction",
    "invalidates": [
     "listPromotions"
    ]
   },
   {
    "operationId": "voidCouponCode",
    "contract": "promotions",
    "purpose": "Void a code",
    "trigger": "onAction",
    "invalidates": [
     "listPromotions"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    },
    {
     "name": "campaignId",
     "from": "deepLink"
    },
    {
     "name": "dashboardId",
     "from": "deepLink"
    },
    {
     "name": "promotionId",
     "from": "deepLink"
    },
    {
     "name": "reportId",
     "from": "deepLink"
    },
    {
     "name": "code",
     "from": "deepLink"
    }
   ],
   "coldEntry": "A dashboard opened from a link or a saved view. A coupon code opened from the list, or scanned at a till.",
   "preloaded": [
    "Promotion.code",
    "Promotion.name",
    "Promotion.description",
    "Promotion.venueId",
    "Promotion.discount"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-010",
   "source": "Claude Design POS pack, 24 August",
   "note": "**Drawn by Claude Design on `POS Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 19 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "BO-011",
  "name": "Packages & Bundles",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/packages-bundles",
   "component": "apps/venue-management-web/src/routes/venue-operations/PackagesBundlesDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-001",
    "BO-007",
    "BO-008",
    "BO-009"
   ],
   "inferred": true,
   "entryFrom": [
    "BO-013",
    "BO-102"
   ],
   "transitions": [
    {
     "to": "BO-001",
     "trigger": "Queue Directory",
     "carries": [
      "eventId",
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-007",
     "trigger": "Product Directory",
     "carries": [
      "productId"
     ],
     "provenance": "derived — BO-007 declares entryState.params productId, so an edge into it must carry them"
    },
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "carries": [
      "productId",
      "venueId"
     ],
     "provenance": "derived — BO-008 declares entryState.params productId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-009",
     "trigger": "Pricing Rules",
     "carries": [
      "priceListId"
     ],
     "provenance": "derived — BO-009 declares entryState.params priceListId, so an edge into it must carry them"
    },
    {
     "to": "ANL-009",
     "trigger": "AI Assistant & Action Center",
     "provenance": "flow F77 step 2→3",
     "crossesDevice": true,
     "back": false
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Improved 20 August against the client design board.** Answers 2 board screen(s): Combo & Meal Builder; Bundle, Kit & Gift Set Builder. **The board specifies this screen further rather than replacing it** — the id, its flows and its navigation are unchanged, which is what keeps 3,184 traceability rows and every board anchor pointing at something real.",
  "density": "compact",
  "boardFrames": [
   "FnB Board 2.dc.html#fnb-2g",
   "Retail Board 5.dc.html#ret-5h"
  ],
  "pattern": "listDetail",
  "patternReason": "`listCatalogueBundles` reads the population and `getLatestBundle` reads one of them — list, select, act",
  "purpose": "Sell several products as one line.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every packages bundles",
       "bindsTo": "BundleSummary",
       "columns": [
        "BundleSummary.venueId",
        "BundleSummary.publishedAt",
        "BundleSummary.publishedBy",
        "BundleSummary.contentHash",
        "BundleSummary.signatureKeyId",
        "BundleSummary.staleAfter",
        "BundleSummary.sizeBytes",
        "BundleSummary.note",
        "BundleSummary.appliedByWorkstations"
       ],
       "operation": "listCatalogueBundles",
       "provenance": "contract catalogue.yaml GET /catalogue/bundles"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected packages bundles",
       "bindsTo": "CatalogueBundle",
       "columns": [
        "CatalogueBundle.venueId",
        "CatalogueBundle.isDelta",
        "CatalogueBundle.baseVersion",
        "CatalogueBundle.signature",
        "CatalogueBundle.signatureKeyId",
        "CatalogueBundle.contentHash",
        "CatalogueBundle.staleAfter",
        "CatalogueBundle.payload"
       ],
       "operation": "getLatestBundle",
       "provenance": "contract catalogue.yaml GET /catalogue/bundles/latest"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Publish",
       "operation": "publishBundle",
       "provenance": "contract catalogue.yaml POST /catalogue/bundles"
      },
      {
       "kind": "secondaryButton",
       "label": "Report",
       "operation": "reportBundleApplied",
       "provenance": "contract catalogue.yaml POST /catalogue/bundles/{version}/applied"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createBundle",
       "provenance": "contract promotions.yaml POST /bundles"
      },
      {
       "kind": "publishGate",
       "label": "What publishing changes",
       "notes": "**Names what goes live, where, and from when.** A publish with no stated consequence is one somebody presses meaning to save.",
       "provenance": "authored — required by check-screens"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "detailPanel",
       "notes": "Structure from the wireframe board. Components not yet enumerated.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listCatalogueBundles",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "publishBundle",
       "label": "Publish bundle",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "publishBundle",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "publishGate",
       "impliedBy": "publishBundle",
       "notes": "Declares `publishBundle`. **The gate names what the publish will affect before it happens** — a disabled Publish with no reason is the state operators escalate.\n",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The packages bundles list.",
   "error": "Could not load. Names which read failed and leaves the packages bundles untouched.",
   "emptyFirstRun": "No packages bundles yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the packages bundles are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCatalogueBundles",
    "contract": "catalogue",
    "purpose": "List published bundles",
    "trigger": "onLoad"
   },
   {
    "operationId": "getLatestBundle",
    "contract": "catalogue",
    "purpose": "Pull the current bundle for this workstation's venue",
    "trigger": "onLoad"
   },
   {
    "operationId": "publishBundle",
    "contract": "catalogue",
    "purpose": "Compute, sign and publish a catalogue bundle",
    "trigger": "onAction",
    "invalidates": [
     "listCatalogueBundles"
    ]
   },
   {
    "operationId": "reportBundleApplied",
    "contract": "catalogue",
    "purpose": "Report that a workstation applied a bundle",
    "trigger": "onAction",
    "invalidates": [
     "listCatalogueBundles"
    ]
   },
   {
    "operationId": "createBundle",
    "contract": "promotions",
    "purpose": "Create a bundle",
    "trigger": "onAction",
    "invalidates": [
     "listCatalogueBundles"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "version",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A version link is expected to point at something superseded — that is what versions are for.** The screen opens the requested version read-only, says it is not current, and links to the one that is. **An old version is history, not an error.** Arrives with `version`.",
   "preloaded": [
    "CatalogueBundle.venueId",
    "CatalogueBundle.isDelta",
    "CatalogueBundle.baseVersion",
    "CatalogueBundle.signature",
    "CatalogueBundle.signatureKeyId"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-011",
   "source": "Claude Design Retail pack, 24 August",
   "note": "**Drawn by Claude Design on `Retail Board 5.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 5 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "BO-012",
  "name": "Membership Products",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/membership-products",
   "component": "apps/venue-management-web/src/routes/venue-operations/MembershipProductsDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-001",
    "BO-007",
    "BO-008",
    "BO-009"
   ],
   "inferred": true,
   "entryFrom": [
    "BO-102"
   ],
   "transitions": [
    {
     "to": "BO-001",
     "trigger": "Queue Directory",
     "carries": [
      "eventId",
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-007",
     "trigger": "Product Directory",
     "carries": [
      "productId"
     ],
     "provenance": "derived — BO-007 declares entryState.params productId, so an edge into it must carry them"
    },
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "carries": [
      "productId",
      "venueId"
     ],
     "provenance": "derived — BO-008 declares entryState.params productId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-009",
     "trigger": "Pricing Rules",
     "carries": [
      "priceListId"
     ],
     "provenance": "derived — BO-009 declares entryState.params priceListId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listProducts` reads the population and `getProduct` reads one of them — list, select, act",
  "purpose": "Define what a membership includes.",
  "gaps": [
   {
    "operation": "listEntitlementTemplates",
    "why": "**3 declared operations reach no component on this screen**: listEntitlementTemplates, listAlternativeCodes, listProductVariants. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
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
       "label": "Every membership products",
       "bindsTo": "Product",
       "columns": [
        "Product.id",
        "Product.code",
        "Product.name",
        "Product.description",
        "Product.kind",
        "Product.venueId",
        "Product.scopePath",
        "Product.createdByPrincipalId",
        "Product.approvedByPrincipalId",
        "Product.responsibleDepartmentId",
        "Product.onSaleFrom",
        "Product.onSaleTo"
       ],
       "operation": "listProducts",
       "provenance": "contract catalogue.yaml GET /products"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected membership products",
       "bindsTo": "Product",
       "columns": [
        "Product.id",
        "Product.code",
        "Product.name",
        "Product.description",
        "Product.kind",
        "Product.venueId",
        "Product.scopePath",
        "Product.createdByPrincipalId",
        "Product.approvedByPrincipalId",
        "Product.responsibleDepartmentId",
        "Product.onSaleFrom",
        "Product.onSaleTo",
        "Product.lifecycleState",
        "Product.isSellable",
        "Product.hasVariants",
        "Product.variantCount"
       ],
       "operation": "getProduct",
       "provenance": "contract catalogue.yaml GET /products/{productId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create",
       "operation": "createEntitlementTemplate",
       "provenance": "contract catalogue.yaml POST /entitlement-templates"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createProduct",
       "provenance": "contract catalogue.yaml POST /products"
      },
      {
       "kind": "secondaryButton",
       "label": "Resolve",
       "operation": "resolveProductByCode",
       "provenance": "contract catalogue.yaml GET /products/resolve"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "setAlternativeCodes",
       "provenance": "contract catalogue.yaml PUT /products/{productId}/alternative-codes"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "setProductAttributes",
       "provenance": "contract catalogue.yaml PUT /products/{productId}/attributes"
      },
      {
       "kind": "secondaryButton",
       "label": "Transition",
       "operation": "transitionProductLifecycle",
       "provenance": "contract catalogue.yaml POST /products/{productId}/lifecycle"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateProduct",
       "provenance": "contract catalogue.yaml PATCH /products/{productId}"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "detailPanel",
       "notes": "Structure from the wireframe board. Components not yet enumerated.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listProducts",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createEntitlementTemplate",
       "label": "Create entitlement template",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createEntitlementTemplate",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The membership products list.",
   "error": "Could not load. Names which read failed and leaves the membership products untouched.",
   "emptyFirstRun": "No membership products yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the membership products are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listProducts",
    "contract": "catalogue",
    "purpose": "List products",
    "trigger": "onLoad"
   },
   {
    "operationId": "listEntitlementTemplates",
    "contract": "catalogue",
    "purpose": "List entitlement templates",
    "trigger": "onLoad"
   },
   {
    "operationId": "createEntitlementTemplate",
    "contract": "catalogue",
    "purpose": "Create an entitlement template",
    "trigger": "onAction",
    "invalidates": [
     "listProducts"
    ]
   },
   {
    "operationId": "createProduct",
    "contract": "catalogue",
    "purpose": "Create a product",
    "trigger": "onAction",
    "invalidates": [
     "listProducts"
    ]
   },
   {
    "operationId": "getProduct",
    "contract": "catalogue",
    "purpose": "Read a product",
    "trigger": "onLoad"
   },
   {
    "operationId": "listAlternativeCodes",
    "contract": "catalogue",
    "purpose": "External identifiers for a product",
    "trigger": "onLoad"
   },
   {
    "operationId": "listProductVariants",
    "contract": "catalogue",
    "purpose": "List generated variants",
    "trigger": "onLoad"
   },
   {
    "operationId": "resolveProductByCode",
    "contract": "catalogue",
    "purpose": "Resolve a partner code to a product",
    "trigger": "onLoad"
   },
   {
    "operationId": "setAlternativeCodes",
    "contract": "catalogue",
    "purpose": "Set external identifiers",
    "trigger": "onAction",
    "invalidates": [
     "listProducts"
    ]
   },
   {
    "operationId": "setProductAttributes",
    "contract": "catalogue",
    "purpose": "Set the attribute axes for a product",
    "trigger": "onAction",
    "invalidates": [
     "listProducts"
    ]
   },
   {
    "operationId": "transitionProductLifecycle",
    "contract": "catalogue",
    "purpose": "Move a product through its lifecycle",
    "trigger": "onAction",
    "invalidates": [
     "listProducts"
    ]
   },
   {
    "operationId": "updateProduct",
    "contract": "catalogue",
    "purpose": "Update a product",
    "trigger": "onAction",
    "invalidates": [
     "listProducts"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "productId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A shared product link after the product retired.** Shows what replaced it where a successor exists, and the catalogue where none does.",
   "preloaded": [
    "Product.id",
    "Product.code",
    "Product.name",
    "Product.description",
    "Product.kind"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-012"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 12 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "BO-013",
  "name": "Channel & Distribution",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/channel-distribution",
   "component": "apps/venue-management-web/src/routes/venue-operations/ChannelDistributionDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-001",
    "BO-007",
    "BO-008",
    "BO-009",
    "BO-011"
   ],
   "inferred": true,
   "entryFrom": [
    "BO-102"
   ],
   "transitions": [
    {
     "to": "BO-011",
     "trigger": "Packages & Bundles",
     "provenance": "flow F77 step 1→2"
    },
    {
     "to": "BO-001",
     "trigger": "Queue Directory",
     "carries": [
      "eventId",
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-007",
     "trigger": "Product Directory",
     "carries": [
      "productId"
     ],
     "provenance": "derived — BO-007 declares entryState.params productId, so an edge into it must carry them"
    },
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "carries": [
      "productId",
      "venueId"
     ],
     "provenance": "derived — BO-008 declares entryState.params productId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-009",
     "trigger": "Pricing Rules",
     "carries": [
      "priceListId"
     ],
     "provenance": "derived — BO-009 declares entryState.params priceListId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Improved 20 August against the client design board.** Answers 2 board screen(s): Catalog Builder & Store Assortment; Ticketing, Event & Experience Commerce Integration. **The board specifies this screen further rather than replacing it** — the id, its flows and its navigation are unchanged, which is what keeps 3,184 traceability rows and every board anchor pointing at something real. **Improved 20 August against the client design board**, answering 1 board screen(s): Sales Channel Configuration. **The id, flows and navigation are unchanged** — a board specifies a screen further; it does not replace it. **Retail board operations wired 24 August.**",
  "density": "compact",
  "boardFrames": [
   "Retail Board 5.dc.html#ret-5g"
  ],
  "pattern": "listDetail",
  "patternReason": "`listChannelCapacities` reads the population and `getChannelAllocations` reads one of them — list, select, act",
  "purpose": "Decide where each product can be sold.",
  "gaps": [
   {
    "operation": "listChannelListings",
    "why": "**2 declared operations reach no component on this screen**: listChannelListings, listProducts. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
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
       "label": "Every channel distribution",
       "bindsTo": "ChannelCapacity",
       "columns": [
        "ChannelCapacity.id",
        "ChannelCapacity.performanceId",
        "ChannelCapacity.name",
        "ChannelCapacity.seatCategoryId",
        "ChannelCapacity.oversellAllowance",
        "ChannelCapacity.oversellBasis",
        "ChannelCapacity.capacity",
        "ChannelCapacity.sold",
        "ChannelCapacity.leased",
        "ChannelCapacity.remaining",
        "ChannelCapacity.hasChannelAllocations",
        "ChannelCapacity.isSeated"
       ],
       "operation": "listChannelCapacities",
       "provenance": "contract catalogue.yaml GET /channel-capacities"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected channel distribution",
       "bindsTo": "ChannelAllocationSet",
       "columns": [
        "ChannelAllocationSet.channelCapacityId",
        "ChannelAllocationSet.capacity",
        "ChannelAllocationSet.allocations",
        "ChannelAllocationSet.generalPoolUnits",
        "ChannelAllocationSet.totalSold",
        "ChannelAllocationSet.totalRemaining"
       ],
       "operation": "getChannelAllocations",
       "provenance": "contract catalogue.yaml GET /channel-capacities/{channelCapacityId}/channel-allocations"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save changes",
       "operation": "setChannelAllocations",
       "provenance": "contract catalogue.yaml PUT /channel-capacities/{channelCapacityId}/channel-allocations"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createChannelCapacity",
       "provenance": "contract catalogue.yaml POST /channel-capacities"
      },
      {
       "kind": "secondaryButton",
       "label": "Release hold",
       "operation": "relinquishChannelAllocation",
       "provenance": "contract catalogue.yaml POST /channel-capacities/{channelCapacityId}/channel-allocations/release"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateChannelCapacity",
       "provenance": "contract catalogue.yaml PATCH /channel-capacities/{channelCapacityId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Publish",
       "operation": "publishBundle",
       "provenance": "contract catalogue.yaml POST /catalogue/bundles"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "setChannelListing",
       "provenance": "contract subscription.yaml PUT /channel-listings"
      },
      {
       "kind": "publishGate",
       "label": "What publishing changes",
       "notes": "**Names what goes live, where, and from when.** A publish with no stated consequence is one somebody presses meaning to save.",
       "provenance": "authored — required by check-screens"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "detailPanel",
       "notes": "Structure from the wireframe board. Components not yet enumerated.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "setChannelAllocations",
       "label": "Save channel allocations",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listChannelCapacities",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setChannelAllocations",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "publishGate",
       "impliedBy": "publishBundle",
       "notes": "Declares `publishBundle`. **The gate names what the publish will affect before it happens** — a disabled Publish with no reason is the state operators escalate.\n",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The channel distribution list.",
   "error": "Could not load. Names which read failed and leaves the channel distribution untouched.",
   "emptyFirstRun": "No channel distribution yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the channel distribution are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getChannelAllocations",
    "contract": "catalogue",
    "purpose": "Capacity allocated to each channel",
    "trigger": "onLoad"
   },
   {
    "operationId": "setChannelAllocations",
    "contract": "catalogue",
    "purpose": "Allocate envelope capacity across channels",
    "trigger": "onAction",
    "invalidates": [
     "listChannelCapacities"
    ]
   },
   {
    "operationId": "createChannelCapacity",
    "contract": "catalogue",
    "purpose": "Create a capacity envelope",
    "trigger": "onAction",
    "invalidates": [
     "listChannelCapacities"
    ]
   },
   {
    "operationId": "listChannelCapacities",
    "contract": "catalogue",
    "purpose": "List capacity envelopes",
    "trigger": "onLoad"
   },
   {
    "operationId": "relinquishChannelAllocation",
    "contract": "catalogue",
    "purpose": "Return unsold channel allocation to the general pool",
    "trigger": "onAction",
    "invalidates": [
     "listChannelCapacities"
    ]
   },
   {
    "operationId": "updateChannelCapacity",
    "contract": "catalogue",
    "purpose": "Amend an envelope",
    "trigger": "onAction",
    "invalidates": [
     "listChannelCapacities"
    ]
   },
   {
    "operationId": "listChannelListings",
    "contract": "subscription",
    "purpose": "What is listed on which OTA",
    "trigger": "onLoad"
   },
   {
    "operationId": "listProducts",
    "contract": "catalogue",
    "purpose": "List products",
    "trigger": "onLoad"
   },
   {
    "operationId": "publishBundle",
    "contract": "catalogue",
    "purpose": "Compute, sign and publish a catalogue bundle",
    "trigger": "onAction",
    "invalidates": [
     "listChannelCapacities"
    ]
   },
   {
    "operationId": "setChannelListing",
    "contract": "subscription",
    "purpose": "List a product on a channel, with its own allocation",
    "trigger": "onAction",
    "invalidates": [
     "listChannelCapacities"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "channelCapacityId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `channelCapacityId`.",
   "preloaded": [
    "ChannelAllocationSet.channelCapacityId",
    "ChannelAllocationSet.capacity",
    "ChannelAllocationSet.allocations",
    "ChannelAllocationSet.generalPoolUnits",
    "ChannelAllocationSet.totalSold"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-013",
   "source": "Claude Design Retail pack, 24 August",
   "note": "**Drawn by Claude Design on `Retail Board 5.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 10 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "BO-014",
  "name": "Catalogue Publishing",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/catalogue-publishing",
   "component": "apps/venue-management-web/src/routes/venue-operations/CataloguePublishingDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-001",
    "BO-007",
    "BO-008",
    "BO-009"
   ],
   "inferred": true,
   "entryFrom": [
    "BO-102"
   ],
   "transitions": [
    {
     "to": "BO-001",
     "trigger": "Queue Directory",
     "carries": [
      "eventId",
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-007",
     "trigger": "Product Directory",
     "carries": [
      "productId"
     ],
     "provenance": "derived — BO-007 declares entryState.params productId, so an edge into it must carry them"
    },
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "carries": [
      "productId",
      "venueId"
     ],
     "provenance": "derived — BO-008 declares entryState.params productId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-009",
     "trigger": "Pricing Rules",
     "carries": [
      "priceListId"
     ],
     "provenance": "derived — BO-009 declares entryState.params priceListId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Improved 20 August against the client design board.** Answers 2 board screen(s): Availability, Pricing, Channels & Publishing; Product Availability, Lifecycle & Publishing. **The board specifies this screen further rather than replacing it** — the id, its flows and its navigation are unchanged, which is what keeps 3,184 traceability rows and every board anchor pointing at something real.",
  "density": "compact",
  "boardFrames": [
   "FnB Board 2.dc.html#fnb-2h",
   "Retail Board 2.dc.html#ret-2h"
  ],
  "pattern": "listDetail",
  "patternReason": "`listProducts` reads the population and `getProduct` reads one of them — list, select, act",
  "purpose": "Push catalogue changes live, or schedule them.",
  "gaps": [
   {
    "operation": "listAlternativeCodes",
    "why": "**3 declared operations reach no component on this screen**: listAlternativeCodes, listProductVariants, listPrices. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
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
       "label": "Every catalogue publishing",
       "bindsTo": "Product",
       "columns": [
        "Product.id",
        "Product.code",
        "Product.name",
        "Product.description",
        "Product.kind",
        "Product.venueId",
        "Product.scopePath",
        "Product.createdByPrincipalId",
        "Product.approvedByPrincipalId",
        "Product.responsibleDepartmentId",
        "Product.onSaleFrom",
        "Product.onSaleTo"
       ],
       "operation": "listProducts",
       "provenance": "contract catalogue.yaml GET /products"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected catalogue publishing",
       "bindsTo": "Product",
       "columns": [
        "Product.id",
        "Product.code",
        "Product.name",
        "Product.description",
        "Product.kind",
        "Product.venueId",
        "Product.scopePath",
        "Product.createdByPrincipalId",
        "Product.approvedByPrincipalId",
        "Product.responsibleDepartmentId",
        "Product.onSaleFrom",
        "Product.onSaleTo",
        "Product.lifecycleState",
        "Product.isSellable",
        "Product.hasVariants",
        "Product.variantCount"
       ],
       "operation": "getProduct",
       "provenance": "contract catalogue.yaml GET /products/{productId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create",
       "operation": "createProduct",
       "provenance": "contract catalogue.yaml POST /products"
      },
      {
       "kind": "secondaryButton",
       "label": "Resolve",
       "operation": "resolveProductByCode",
       "provenance": "contract catalogue.yaml GET /products/resolve"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "setAlternativeCodes",
       "provenance": "contract catalogue.yaml PUT /products/{productId}/alternative-codes"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "setProductAttributes",
       "provenance": "contract catalogue.yaml PUT /products/{productId}/attributes"
      },
      {
       "kind": "secondaryButton",
       "label": "Transition",
       "operation": "transitionProductLifecycle",
       "provenance": "contract catalogue.yaml POST /products/{productId}/lifecycle"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateProduct",
       "provenance": "contract catalogue.yaml PATCH /products/{productId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Publish",
       "operation": "publishBundle",
       "provenance": "contract catalogue.yaml POST /catalogue/bundles"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "setItemAvailability",
       "provenance": "contract fnb.yaml PUT /menu-items/{itemId}/availability"
      },
      {
       "kind": "publishGate",
       "label": "What publishing changes",
       "notes": "**Names what goes live, where, and from when.** A publish with no stated consequence is one somebody presses meaning to save.",
       "provenance": "authored — required by check-screens"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "detailPanel",
       "notes": "Structure from the wireframe board. Components not yet enumerated.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listProducts",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createProduct",
       "label": "Create product",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createProduct",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "publishGate",
       "impliedBy": "publishBundle",
       "notes": "Declares `publishBundle`. **The gate names what the publish will affect before it happens** — a disabled Publish with no reason is the state operators escalate.\n",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The catalogue publishing list.",
   "error": "Could not load. Names which read failed and leaves the catalogue publishing untouched.",
   "emptyFirstRun": "No catalogue publishing yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the catalogue publishing are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listProducts",
    "contract": "catalogue",
    "purpose": "List products",
    "trigger": "onLoad"
   },
   {
    "operationId": "getProduct",
    "contract": "catalogue",
    "purpose": "Read a product",
    "trigger": "onLoad"
   },
   {
    "operationId": "createProduct",
    "contract": "catalogue",
    "purpose": "Create a product",
    "trigger": "onAction",
    "invalidates": [
     "listProducts"
    ]
   },
   {
    "operationId": "listAlternativeCodes",
    "contract": "catalogue",
    "purpose": "External identifiers for a product",
    "trigger": "onLoad"
   },
   {
    "operationId": "listProductVariants",
    "contract": "catalogue",
    "purpose": "List generated variants",
    "trigger": "onLoad"
   },
   {
    "operationId": "resolveProductByCode",
    "contract": "catalogue",
    "purpose": "Resolve a partner code to a product",
    "trigger": "onLoad"
   },
   {
    "operationId": "setAlternativeCodes",
    "contract": "catalogue",
    "purpose": "Set external identifiers",
    "trigger": "onAction",
    "invalidates": [
     "listProducts"
    ]
   },
   {
    "operationId": "setProductAttributes",
    "contract": "catalogue",
    "purpose": "Set the attribute axes for a product",
    "trigger": "onAction",
    "invalidates": [
     "listProducts"
    ]
   },
   {
    "operationId": "transitionProductLifecycle",
    "contract": "catalogue",
    "purpose": "Move a product through its lifecycle",
    "trigger": "onAction",
    "invalidates": [
     "listProducts"
    ]
   },
   {
    "operationId": "updateProduct",
    "contract": "catalogue",
    "purpose": "Update a product",
    "trigger": "onAction",
    "invalidates": [
     "listProducts"
    ]
   },
   {
    "operationId": "listPrices",
    "contract": "catalogue",
    "purpose": "List prices in a list",
    "trigger": "onLoad"
   },
   {
    "operationId": "publishBundle",
    "contract": "catalogue",
    "purpose": "Compute, sign and publish a catalogue bundle",
    "trigger": "onAction",
    "invalidates": [
     "listProducts"
    ]
   },
   {
    "operationId": "setItemAvailability",
    "contract": "fnb",
    "purpose": "Mark an item available or eighty-sixed",
    "trigger": "onAction",
    "invalidates": [
     "listProducts"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    },
    {
     "name": "itemId",
     "from": "deepLink"
    },
    {
     "name": "priceListId",
     "from": "deepLink"
    },
    {
     "name": "productId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "An item opened from the catalogue. A price list opened from the price book. A product opened from the directory.",
   "preloaded": [
    "Product.id",
    "Product.code",
    "Product.name",
    "Product.description",
    "Product.kind"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-014",
   "source": "Claude Design Retail pack, 24 August",
   "note": "**Drawn by Claude Design on `Retail Board 2.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 13 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "BO-015",
  "name": "Session Calendar",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/session-calendar",
   "component": "apps/venue-management-web/src/routes/venue-operations/SessionCalendarDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-001",
    "BO-007",
    "BO-008",
    "BO-009"
   ],
   "inferred": true,
   "entryFrom": [
    "BO-102"
   ],
   "transitions": [
    {
     "to": "BO-001",
     "trigger": "Queue Directory",
     "carries": [
      "eventId",
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-007",
     "trigger": "Product Directory",
     "carries": [
      "productId"
     ],
     "provenance": "derived — BO-007 declares entryState.params productId, so an edge into it must carry them"
    },
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "carries": [
      "productId",
      "venueId"
     ],
     "provenance": "derived — BO-008 declares entryState.params productId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-009",
     "trigger": "Pricing Rules",
     "carries": [
      "priceListId"
     ],
     "provenance": "derived — BO-009 declares entryState.params priceListId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Drawn 26 August** — `Seat Board 2.dc.html` frame `seat-2a`. **The frame names this screen on its own face**, which is the first pack to do that: the earlier F&B, POS and Retail boards had to be hand-assigned by purpose after three derivation attempts produced nonsense. **A board that says what it draws removes the guess entirely.**",
  "density": "compact",
  "boardFrames": [
   "Seat Board 2.dc.html#seat-2a"
  ],
  "pattern": "listDetail",
  "patternReason": "`listPerformances` reads the population and `getPerformance` reads one of them — list, select, act",
  "purpose": "See what is scheduled and how full it is.",
  "gaps": [
   {
    "operation": "getEvent",
    "why": "**3 declared operations reach no component on this screen**: getEvent, getSeatAvailability, listEvents. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
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
       "label": "Every session calendar",
       "bindsTo": "Performance",
       "columns": [
        "Performance.id",
        "Performance.eventId",
        "Performance.startsAt",
        "Performance.endsAt",
        "Performance.approvalRequestId",
        "Performance.requiresApprovalToCancel",
        "Performance.status",
        "Performance.admissionRulesId",
        "Performance.seatMapId"
       ],
       "operation": "listPerformances",
       "provenance": "contract catalogue.yaml GET /events/{eventId}/performances"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected session calendar",
       "bindsTo": "Performance",
       "columns": [
        "Performance.id",
        "Performance.eventId",
        "Performance.startsAt",
        "Performance.endsAt",
        "Performance.approvalRequestId",
        "Performance.requiresApprovalToCancel",
        "Performance.status",
        "Performance.admissionRulesId",
        "Performance.seatMapId"
       ],
       "operation": "getPerformance",
       "provenance": "contract catalogue.yaml GET /performances/{performanceId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create",
       "operation": "createPerformances",
       "provenance": "contract catalogue.yaml POST /events/{eventId}/performances"
      },
      {
       "kind": "destructiveButton",
       "label": "Cancel",
       "operation": "cancelPerformance",
       "provenance": "contract catalogue.yaml POST /performances/{performanceId}/cancel"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createEvent",
       "provenance": "contract catalogue.yaml POST /events"
      },
      {
       "kind": "secondaryButton",
       "label": "Recommend",
       "operation": "recommendSeats",
       "provenance": "contract seating.yaml POST /performances/{performanceId}/seat-recommendations"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateEvent",
       "provenance": "contract catalogue.yaml PATCH /events/{eventId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updatePerformance",
       "provenance": "contract catalogue.yaml PATCH /performances/{performanceId}"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "detailPanel",
       "notes": "Structure from the wireframe board. Components not yet enumerated.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listPerformances",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createPerformances",
       "label": "Create performances",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "destructiveButton",
       "derived": true,
       "impliedBy": "cancelPerformance",
       "label": "Cancel performance",
       "notes": "**Always confirms, never the default focus.** The consequence goes in the body — *cancel 3 orders worth AED 480* is a confirmation, *are you sure* is not.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createPerformances",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "confirmDialog",
       "derived": true,
       "label": "Confirm",
       "notes": "**The consequence goes in the body, not the title.** *Cancel 3 orders worth AED 480* is a confirmation; *are you sure* is not — and a dialog that cannot name what it destroys is a dialog somebody dismisses.\n\n**Added 31 August.** `confirmDialog` and `modal` were both in the component library and used **zero times across 492 screens**, while `destructiveButton` was used 39 times and its own entry reads *always requires confirmation*.",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmCancelPerformance",
    "component": "confirmDialog",
    "trigger": "Cancel",
    "body": "**Names what `cancelPerformance` changes and what it leaves alone**, in the consequence rather than the verb. A session calendar this affects should be identified in the dialog, not just counted.",
    "provenance": "contract catalogue.yaml POST /performances/{performanceId}/cancel"
   }
  ],
  "states": {
   "loading": "The session calendar list.",
   "error": "Could not load. Names which read failed and leaves the session calendar untouched.",
   "emptyFirstRun": "No session calendar yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the session calendar are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPerformances",
    "contract": "catalogue",
    "purpose": "List performances of an event",
    "trigger": "onLoad"
   },
   {
    "operationId": "getPerformance",
    "contract": "catalogue",
    "purpose": "Read a performance",
    "trigger": "onLoad"
   },
   {
    "operationId": "createPerformances",
    "contract": "catalogue",
    "purpose": "Create performances, singly or by schedule",
    "trigger": "onAction",
    "invalidates": [
     "listPerformances"
    ]
   },
   {
    "operationId": "cancelPerformance",
    "contract": "catalogue",
    "purpose": "Cancel a performance",
    "trigger": "onAction",
    "invalidates": [
     "listPerformances"
    ]
   },
   {
    "operationId": "createEvent",
    "contract": "catalogue",
    "purpose": "Create an event",
    "trigger": "onAction",
    "invalidates": [
     "listPerformances"
    ]
   },
   {
    "operationId": "getEvent",
    "contract": "catalogue",
    "purpose": "Read an event",
    "trigger": "onLoad"
   },
   {
    "operationId": "getSeatAvailability",
    "contract": "seating",
    "purpose": "Seat status for a performance",
    "trigger": "onLoad"
   },
   {
    "operationId": "listEvents",
    "contract": "catalogue",
    "purpose": "List events",
    "trigger": "onLoad"
   },
   {
    "operationId": "recommendSeats",
    "contract": "seating",
    "purpose": "Recommend seats for a party",
    "trigger": "onAction",
    "invalidates": [
     "listPerformances"
    ]
   },
   {
    "operationId": "updateEvent",
    "contract": "catalogue",
    "purpose": "Amend an event",
    "trigger": "onAction",
    "invalidates": [
     "listPerformances"
    ]
   },
   {
    "operationId": "updatePerformance",
    "contract": "catalogue",
    "purpose": "Amend a performance",
    "trigger": "onAction",
    "invalidates": [
     "listPerformances"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "eventId",
     "from": "deepLink"
    },
    {
     "name": "performanceId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A link to a performance that has happened.** Offers the next performance of the same event.",
   "preloaded": [
    "Performance.id",
    "Performance.eventId",
    "Performance.startsAt",
    "Performance.endsAt",
    "Performance.approvalRequestId"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-015",
   "note": "**Drawn by Claude Design on `Seat Board 2.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 11 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "BO-016",
  "name": "Session Template",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/session-template",
   "component": "apps/venue-management-web/src/routes/venue-operations/SessionTemplateDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-001",
    "BO-007",
    "BO-008",
    "BO-009"
   ],
   "inferred": true,
   "entryFrom": [
    "BO-102"
   ],
   "transitions": [
    {
     "to": "BO-001",
     "trigger": "Queue Directory",
     "carries": [
      "eventId",
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-007",
     "trigger": "Product Directory",
     "carries": [
      "productId"
     ],
     "provenance": "derived — BO-007 declares entryState.params productId, so an edge into it must carry them"
    },
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "carries": [
      "productId",
      "venueId"
     ],
     "provenance": "derived — BO-008 declares entryState.params productId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-009",
     "trigger": "Pricing Rules",
     "carries": [
      "priceListId"
     ],
     "provenance": "derived — BO-009 declares entryState.params priceListId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Drawn 26 August** — `Seat Board 2.dc.html` frame `seat-2b`. **The frame names this screen on its own face**, which is the first pack to do that: the earlier F&B, POS and Retail boards had to be hand-assigned by purpose after three derivation attempts produced nonsense. **A board that says what it draws removes the guess entirely.**",
  "density": "compact",
  "boardFrames": [
   "Seat Board 2.dc.html#seat-2b"
  ],
  "pattern": "listDetail",
  "patternReason": "`listPerformances` reads the population and `getPerformance` reads one of them — list, select, act",
  "purpose": "Define the pattern the calendar is generated from.",
  "gaps": [
   {
    "operation": "getEvent",
    "why": "**3 declared operations reach no component on this screen**: getEvent, getSeatAvailability, listEvents. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
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
       "label": "Every session template",
       "bindsTo": "Performance",
       "columns": [
        "Performance.id",
        "Performance.eventId",
        "Performance.startsAt",
        "Performance.endsAt",
        "Performance.approvalRequestId",
        "Performance.requiresApprovalToCancel",
        "Performance.status",
        "Performance.admissionRulesId",
        "Performance.seatMapId"
       ],
       "operation": "listPerformances",
       "provenance": "contract catalogue.yaml GET /events/{eventId}/performances"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected session template",
       "bindsTo": "Performance",
       "columns": [
        "Performance.id",
        "Performance.eventId",
        "Performance.startsAt",
        "Performance.endsAt",
        "Performance.approvalRequestId",
        "Performance.requiresApprovalToCancel",
        "Performance.status",
        "Performance.admissionRulesId",
        "Performance.seatMapId"
       ],
       "operation": "getPerformance",
       "provenance": "contract catalogue.yaml GET /performances/{performanceId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create",
       "operation": "createPerformances",
       "provenance": "contract catalogue.yaml POST /events/{eventId}/performances"
      },
      {
       "kind": "destructiveButton",
       "label": "Cancel",
       "operation": "cancelPerformance",
       "provenance": "contract catalogue.yaml POST /performances/{performanceId}/cancel"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createEvent",
       "provenance": "contract catalogue.yaml POST /events"
      },
      {
       "kind": "secondaryButton",
       "label": "Recommend",
       "operation": "recommendSeats",
       "provenance": "contract seating.yaml POST /performances/{performanceId}/seat-recommendations"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateEvent",
       "provenance": "contract catalogue.yaml PATCH /events/{eventId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updatePerformance",
       "provenance": "contract catalogue.yaml PATCH /performances/{performanceId}"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "detailPanel",
       "notes": "Structure from the wireframe board. Components not yet enumerated.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listPerformances",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createPerformances",
       "label": "Create performances",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "destructiveButton",
       "derived": true,
       "impliedBy": "cancelPerformance",
       "label": "Cancel performance",
       "notes": "**Always confirms, never the default focus.** The consequence goes in the body — *cancel 3 orders worth AED 480* is a confirmation, *are you sure* is not.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createPerformances",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "confirmDialog",
       "derived": true,
       "label": "Confirm",
       "notes": "**The consequence goes in the body, not the title.** *Cancel 3 orders worth AED 480* is a confirmation; *are you sure* is not — and a dialog that cannot name what it destroys is a dialog somebody dismisses.\n\n**Added 31 August.** `confirmDialog` and `modal` were both in the component library and used **zero times across 492 screens**, while `destructiveButton` was used 39 times and its own entry reads *always requires confirmation*.",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmCancelPerformance",
    "component": "confirmDialog",
    "trigger": "Cancel",
    "body": "**Names what `cancelPerformance` changes and what it leaves alone**, in the consequence rather than the verb. A session template this affects should be identified in the dialog, not just counted.",
    "provenance": "contract catalogue.yaml POST /performances/{performanceId}/cancel"
   }
  ],
  "states": {
   "loading": "The session template list.",
   "error": "Could not load. Names which read failed and leaves the session template untouched.",
   "emptyFirstRun": "No session template yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the session template are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPerformances",
    "contract": "catalogue",
    "purpose": "List performances of an event",
    "trigger": "onLoad"
   },
   {
    "operationId": "getPerformance",
    "contract": "catalogue",
    "purpose": "Read a performance",
    "trigger": "onLoad"
   },
   {
    "operationId": "createPerformances",
    "contract": "catalogue",
    "purpose": "Create performances, singly or by schedule",
    "trigger": "onAction",
    "invalidates": [
     "listPerformances"
    ]
   },
   {
    "operationId": "cancelPerformance",
    "contract": "catalogue",
    "purpose": "Cancel a performance",
    "trigger": "onAction",
    "invalidates": [
     "listPerformances"
    ]
   },
   {
    "operationId": "createEvent",
    "contract": "catalogue",
    "purpose": "Create an event",
    "trigger": "onAction",
    "invalidates": [
     "listPerformances"
    ]
   },
   {
    "operationId": "getEvent",
    "contract": "catalogue",
    "purpose": "Read an event",
    "trigger": "onLoad"
   },
   {
    "operationId": "getSeatAvailability",
    "contract": "seating",
    "purpose": "Seat status for a performance",
    "trigger": "onLoad"
   },
   {
    "operationId": "listEvents",
    "contract": "catalogue",
    "purpose": "List events",
    "trigger": "onLoad"
   },
   {
    "operationId": "recommendSeats",
    "contract": "seating",
    "purpose": "Recommend seats for a party",
    "trigger": "onAction",
    "invalidates": [
     "listPerformances"
    ]
   },
   {
    "operationId": "updateEvent",
    "contract": "catalogue",
    "purpose": "Amend an event",
    "trigger": "onAction",
    "invalidates": [
     "listPerformances"
    ]
   },
   {
    "operationId": "updatePerformance",
    "contract": "catalogue",
    "purpose": "Amend a performance",
    "trigger": "onAction",
    "invalidates": [
     "listPerformances"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "eventId",
     "from": "deepLink"
    },
    {
     "name": "performanceId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A link to a performance that has happened.** Offers the next performance of the same event.",
   "preloaded": [
    "Performance.id",
    "Performance.eventId",
    "Performance.startsAt",
    "Performance.endsAt",
    "Performance.approvalRequestId"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-016",
   "note": "**Drawn by Claude Design on `Seat Board 2.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 11 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "BO-017",
  "name": "Capacity Management",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/capacity-management",
   "component": "apps/venue-management-web/src/routes/venue-operations/CapacityManagementDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-001",
    "BO-007",
    "BO-008",
    "BO-009"
   ],
   "inferred": true,
   "entryFrom": [
    "BO-102"
   ],
   "transitions": [
    {
     "to": "BO-001",
     "trigger": "Queue Directory",
     "carries": [
      "eventId",
      "feedId",
      "queueId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId, so an edge into it must carry them"
    },
    {
     "to": "BO-007",
     "trigger": "Product Directory",
     "carries": [
      "productId"
     ],
     "provenance": "derived — BO-007 declares entryState.params productId, so an edge into it must carry them"
    },
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "carries": [
      "productId",
      "venueId"
     ],
     "provenance": "derived — BO-008 declares entryState.params productId, venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-009",
     "trigger": "Pricing Rules",
     "carries": [
      "priceListId"
     ],
     "provenance": "derived — BO-009 declares entryState.params priceListId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listChannelCapacities` reads the population and `getChannelAllocations` reads one of them — list, select, act",
  "purpose": "Change how many people a session can take.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every capacity",
       "bindsTo": "ChannelCapacity",
       "columns": [
        "ChannelCapacity.id",
        "ChannelCapacity.performanceId",
        "ChannelCapacity.name",
        "ChannelCapacity.seatCategoryId",
        "ChannelCapacity.oversellAllowance",
        "ChannelCapacity.oversellBasis",
        "ChannelCapacity.capacity",
        "ChannelCapacity.sold",
        "ChannelCapacity.leased",
        "ChannelCapacity.remaining",
        "ChannelCapacity.hasChannelAllocations",
        "ChannelCapacity.isSeated"
       ],
       "operation": "listChannelCapacities",
       "provenance": "contract catalogue.yaml GET /channel-capacities"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected capacity",
       "bindsTo": "ChannelAllocationSet",
       "columns": [
        "ChannelAllocationSet.channelCapacityId",
        "ChannelAllocationSet.capacity",
        "ChannelAllocationSet.allocations",
        "ChannelAllocationSet.generalPoolUnits",
        "ChannelAllocationSet.totalSold",
        "ChannelAllocationSet.totalRemaining"
       ],
       "operation": "getChannelAllocations",
       "provenance": "contract catalogue.yaml GET /channel-capacities/{channelCapacityId}/channel-allocations"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create",
       "operation": "createChannelCapacity",
       "provenance": "contract catalogue.yaml POST /channel-capacities"
      },
      {
       "kind": "secondaryButton",
       "label": "Release hold",
       "operation": "relinquishChannelAllocation",
       "provenance": "contract catalogue.yaml POST /channel-capacities/{channelCapacityId}/channel-allocations/release"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "setChannelAllocations",
       "provenance": "contract catalogue.yaml PUT /channel-capacities/{channelCapacityId}/channel-allocations"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateChannelCapacity",
       "provenance": "contract catalogue.yaml PATCH /channel-capacities/{channelCapacityId}"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "detailPanel",
       "notes": "Structure from the wireframe board. Components not yet enumerated.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listChannelCapacities",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createChannelCapacity",
       "label": "Create envelope",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createChannelCapacity",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The capacity list.",
   "error": "Could not load. Names which read failed and leaves the capacity untouched.",
   "emptyFirstRun": "No capacity yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the capacity are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listChannelCapacities",
    "contract": "catalogue",
    "purpose": "List capacity envelopes",
    "trigger": "onLoad"
   },
   {
    "operationId": "getChannelAllocations",
    "contract": "catalogue",
    "purpose": "Capacity allocated to each channel",
    "trigger": "onLoad"
   },
   {
    "operationId": "createChannelCapacity",
    "contract": "catalogue",
    "purpose": "Create a capacity envelope",
    "trigger": "onAction",
    "invalidates": [
     "listChannelCapacities"
    ]
   },
   {
    "operationId": "relinquishChannelAllocation",
    "contract": "catalogue",
    "purpose": "Return unsold channel allocation to the general pool",
    "trigger": "onAction",
    "invalidates": [
     "listChannelCapacities"
    ]
   },
   {
    "operationId": "setChannelAllocations",
    "contract": "catalogue",
    "purpose": "Allocate envelope capacity across channels",
    "trigger": "onAction",
    "invalidates": [
     "listChannelCapacities"
    ]
   },
   {
    "operationId": "updateChannelCapacity",
    "contract": "catalogue",
    "purpose": "Amend an envelope",
    "trigger": "onAction",
    "invalidates": [
     "listChannelCapacities"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "channelCapacityId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `channelCapacityId`.",
   "preloaded": [
    "ChannelAllocationSet.channelCapacityId",
    "ChannelAllocationSet.capacity",
    "ChannelAllocationSet.allocations",
    "ChannelAllocationSet.generalPoolUnits",
    "ChannelAllocationSet.totalSold"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-017"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 6 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
{
 "analysePromotionConflicts": {
  "method": "GET",
  "path": "/promotions/{promotionId}/conflicts",
  "contract": "promotions",
  "summary": "Analyse stacking against live promotions",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ConflictAnalysis"
 },
 "bulkUpdateProducts": {
  "method": "POST",
  "path": "/products/bulk",
  "contract": "inventory",
  "summary": "Change many products at once, with a preview",
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
 },
 "cancelPerformance": {
  "method": "POST",
  "path": "/performances/{performanceId}/cancel",
  "contract": "catalogue",
  "summary": "Cancel a performance",
  "permission": "PERFORMANCE_CONFIGURE",
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
  "responds": "PerformanceCancellationResult"
 },
 "copyPriceList": {
  "method": "POST",
  "path": "/price-lists/{priceListId}/copy",
  "contract": "catalogue",
  "summary": "Copy a price list, optionally with an adjustment",
  "permission": "PRICE_CONFIGURE",
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
 },
 "createBundle": {
  "method": "POST",
  "path": "/bundles",
  "contract": "promotions",
  "summary": "Create a bundle",
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
  "requestBody": "CreateBundleRequest",
  "responds": "Bundle"
 },
 "createChannelCapacity": {
  "method": "POST",
  "path": "/channel-capacities",
  "contract": "catalogue",
  "summary": "Create a capacity envelope",
  "permission": "CAPACITY_CONFIGURE",
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
  "requestBody": "CreateEnvelopeRequest",
  "responds": "ChannelCapacity"
 },
 "createCouponCampaign": {
  "method": "POST",
  "path": "/coupon-campaigns",
  "contract": "promotions",
  "summary": "Create a coupon campaign",
  "permission": "PRICE_CONFIGURE",
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
  "requestBody": "CreateCouponCampaignRequest",
  "responds": "CouponCampaign"
 },
 "createEntitlementTemplate": {
  "method": "POST",
  "path": "/entitlement-templates",
  "contract": "catalogue",
  "summary": "Create an entitlement template",
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
  "requestBody": "EntitlementTemplate",
  "responds": "EntitlementTemplate"
 },
 "createEvent": {
  "method": "POST",
  "path": "/events",
  "contract": "catalogue",
  "summary": "Create an event",
  "permission": "EVENT_CONFIGURE",
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
  "requestBody": "CreateEventRequest",
  "responds": "Event"
 },
 "createMerchandise": {
  "method": "POST",
  "path": "/merchandise",
  "contract": "retail",
  "summary": "Create a merchandise item",
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
  "requestBody": "CreateMerchandiseRequest",
  "responds": "MerchandiseItem"
 },
 "createPerformances": {
  "method": "POST",
  "path": "/events/{eventId}/performances",
  "contract": "catalogue",
  "summary": "Create performances, singly or by schedule",
  "permission": "PERFORMANCE_CONFIGURE",
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
  "requestBody": "CreatePerformancesRequest",
  "responds": null
 },
 "createPriceList": {
  "method": "POST",
  "path": "/price-lists",
  "contract": "catalogue",
  "summary": "Create a price list",
  "permission": "PRICE_CONFIGURE",
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
  "requestBody": "CreatePriceListRequest",
  "responds": "PriceList"
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
 "createPromotion": {
  "method": "POST",
  "path": "/promotions",
  "contract": "promotions",
  "summary": "Create a promotion",
  "permission": "PRICE_CONFIGURE",
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
  "requestBody": "CreatePromotionRequest",
  "responds": "Promotion"
 },
 "endPromotion": {
  "method": "POST",
  "path": "/promotions/{promotionId}/end",
  "contract": "promotions",
  "summary": "End a promotion early",
  "permission": "PRICE_CONFIGURE",
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
 },
 "evaluatePromotions": {
  "method": "POST",
  "path": "/promotions/evaluate",
  "contract": "promotions",
  "summary": "Evaluate promotions against a cart",
  "permission": "PRICE_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "EvaluatePromotionsRequest",
  "responds": "PromotionEvaluation"
 },
 "generateCouponCodes": {
  "method": "POST",
  "path": "/coupon-campaigns/{campaignId}/codes",
  "contract": "promotions",
  "summary": "Generate codes in bulk",
  "permission": "PRICE_CONFIGURE",
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
 },
 "getChannelAllocations": {
  "method": "GET",
  "path": "/channel-capacities/{channelCapacityId}/channel-allocations",
  "contract": "catalogue",
  "summary": "Capacity allocated to each channel",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ChannelAllocationSet"
 },
 "getDashboard": {
  "method": "GET",
  "path": "/dashboards/{dashboardId}",
  "contract": "reporting",
  "summary": "Read a dashboard with tile data",
  "permission": "REPORT_VIEW_VENUE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "refresh",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "DashboardData"
 },
 "getEvent": {
  "method": "GET",
  "path": "/events/{eventId}",
  "contract": "catalogue",
  "summary": "Read an event",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "Event"
 },
 "getLatestBundle": {
  "method": "GET",
  "path": "/catalogue/bundles/latest",
  "contract": "catalogue",
  "summary": "Pull the current bundle for this workstation's venue",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "workstation",
  "parameters": [
   {
    "name": "since",
    "in": "query",
    "required": null
   },
   {
    "name": "If-None-Match",
    "in": "header",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "CatalogueBundle"
 },
 "getPerformance": {
  "method": "GET",
  "path": "/performances/{performanceId}",
  "contract": "catalogue",
  "summary": "Read a performance",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "Performance"
 },
 "getPriceList": {
  "method": "GET",
  "path": "/price-lists/{priceListId}",
  "contract": "catalogue",
  "summary": "Read a price list",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "PriceList"
 },
 "getProduct": {
  "method": "GET",
  "path": "/products/{productId}",
  "contract": "catalogue",
  "summary": "Read a product",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "Product"
 },
 "getPromotion": {
  "method": "GET",
  "path": "/promotions/{promotionId}",
  "contract": "promotions",
  "summary": "Read a promotion",
  "permission": "PRICE_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "Promotion"
 },
 "getPromotionUsage": {
  "method": "GET",
  "path": "/promotions/{promotionId}/usage",
  "contract": "promotions",
  "summary": "Redemption count and discount given",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "PromotionUsage"
 },
 "getSeatAvailability": {
  "method": "GET",
  "path": "/performances/{performanceId}/seat-availability",
  "contract": "seating",
  "summary": "Seat status for a performance",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "sectionCode",
    "in": "query",
    "required": null
   },
   {
    "name": "categoryId",
    "in": "query",
    "required": null
   },
   {
    "name": "availableOnly",
    "in": "query",
    "required": null
   },
   {
    "name": "mode",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "SeatAvailability"
 },
 "listAlternativeCodes": {
  "method": "GET",
  "path": "/products/{productId}/alternative-codes",
  "contract": "catalogue",
  "summary": "External identifiers for a product",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AlternativeCode"
 },
 "listCatalogueBundles": {
  "method": "GET",
  "path": "/catalogue/bundles",
  "contract": "catalogue",
  "summary": "List published bundles",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "BundleSummary"
 },
 "listChannelCapacities": {
  "method": "GET",
  "path": "/channel-capacities",
  "contract": "catalogue",
  "summary": "List capacity envelopes",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "performanceId",
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
 "listChannelListings": {
  "method": "GET",
  "path": "/channel-listings",
  "contract": "subscription",
  "summary": "What is listed on which OTA",
  "permission": "PARTNER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ChannelListing"
 },
 "listCouponCampaigns": {
  "method": "GET",
  "path": "/coupon-campaigns",
  "contract": "promotions",
  "summary": "List coupon campaigns",
  "permission": "PRICE_VIEW",
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
 "listCouponCodes": {
  "method": "GET",
  "path": "/coupon-campaigns/{campaignId}/codes",
  "contract": "promotions",
  "summary": "List generated codes",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "status",
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
 "listEntitlementTemplates": {
  "method": "GET",
  "path": "/entitlement-templates",
  "contract": "catalogue",
  "summary": "List entitlement templates",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "EntitlementTemplate"
 },
 "listEvents": {
  "method": "GET",
  "path": "/events",
  "contract": "catalogue",
  "summary": "List events",
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
 "listMenus": {
  "method": "GET",
  "path": "/menus",
  "contract": "fnb",
  "summary": "List menus",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "outletId",
    "in": "query",
    "required": null
   },
   {
    "name": "activeAt",
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
 "listMerchandise": {
  "method": "GET",
  "path": "/merchandise",
  "contract": "retail",
  "summary": "List merchandise",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "outletId",
    "in": "query",
    "required": null
   },
   {
    "name": "categoryId",
    "in": "query",
    "required": null
   },
   {
    "name": "inStockOnly",
    "in": "query",
    "required": null
   },
   {
    "name": "search",
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
 "listPerformances": {
  "method": "GET",
  "path": "/events/{eventId}/performances",
  "contract": "catalogue",
  "summary": "List performances of an event",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
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
 "listPriceLists": {
  "method": "GET",
  "path": "/price-lists",
  "contract": "catalogue",
  "summary": "List price lists",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "channel",
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
 "listPrices": {
  "method": "GET",
  "path": "/price-lists/{priceListId}/prices",
  "contract": "catalogue",
  "summary": "List prices in a list",
  "permission": "PRICE_VIEW",
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
 "listProductVariants": {
  "method": "GET",
  "path": "/products/{productId}/variants",
  "contract": "catalogue",
  "summary": "List generated variants",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": true,
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
 "listProducts": {
  "method": "GET",
  "path": "/products",
  "contract": "catalogue",
  "summary": "List products",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "venueId",
    "in": "query",
    "required": null
   },
   {
    "name": "kind",
    "in": "query",
    "required": null
   },
   {
    "name": "isSellable",
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
 "listPromotions": {
  "method": "GET",
  "path": "/promotions",
  "contract": "promotions",
  "summary": "List promotions",
  "permission": "PRICE_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "venueId",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "activeAt",
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
 "pausePromotion": {
  "method": "POST",
  "path": "/promotions/{promotionId}/pause",
  "contract": "promotions",
  "summary": "Pause a live promotion",
  "permission": "PRICE_CONFIGURE",
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
 },
 "publishBundle": {
  "method": "POST",
  "path": "/catalogue/bundles",
  "contract": "catalogue",
  "summary": "Compute, sign and publish a catalogue bundle",
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
  "responds": "BundleSummary"
 },
 "publishPromotion": {
  "method": "POST",
  "path": "/promotions/{promotionId}/publish",
  "contract": "promotions",
  "summary": "Publish a promotion",
  "permission": "PRICE_CONFIGURE",
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
  "responds": "Promotion"
 },
 "recommendSeats": {
  "method": "POST",
  "path": "/performances/{performanceId}/seat-recommendations",
  "contract": "seating",
  "summary": "Recommend seats for a party",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "SeatRecommendationRequest",
  "responds": null
 },
 "relinquishChannelAllocation": {
  "method": "POST",
  "path": "/channel-capacities/{channelCapacityId}/channel-allocations/release",
  "contract": "catalogue",
  "summary": "Return unsold channel allocation to the general pool",
  "permission": "CAPACITY_CONFIGURE",
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
  "responds": "ChannelAllocationSet"
 },
 "reportBundleApplied": {
  "method": "POST",
  "path": "/catalogue/bundles/{version}/applied",
  "contract": "catalogue",
  "summary": "Report that a workstation applied a bundle",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "append",
  "scopeLevel": "workstation",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": null
 },
 "resolveProductByCode": {
  "method": "GET",
  "path": "/products/resolve",
  "contract": "catalogue",
  "summary": "Resolve a partner code to a product",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "code",
    "in": "query",
    "required": true
   },
   {
    "name": "partnerId",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "ProductVariant"
 },
 "runReport": {
  "method": "POST",
  "path": "/reports/{reportId}/run",
  "contract": "reporting",
  "summary": "Run a report",
  "permission": "REPORT_VIEW_VENUE",
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
  "requestBody": "RunReportRequest",
  "responds": "ReportResult"
 },
 "setAlternativeCodes": {
  "method": "PUT",
  "path": "/products/{productId}/alternative-codes",
  "contract": "catalogue",
  "summary": "Set external identifiers",
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
  "responds": "AlternativeCode"
 },
 "setChannelAllocations": {
  "method": "PUT",
  "path": "/channel-capacities/{channelCapacityId}/channel-allocations",
  "contract": "catalogue",
  "summary": "Allocate envelope capacity across channels",
  "permission": "CAPACITY_CONFIGURE",
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
  "responds": "ChannelAllocationSet"
 },
 "setChannelListing": {
  "method": "PUT",
  "path": "/channel-listings",
  "contract": "subscription",
  "summary": "List a product on a channel, with its own allocation",
  "permission": "PARTNER_MANAGE",
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
  "requestBody": "ChannelListing",
  "responds": "ChannelListing"
 },
 "setItemAvailability": {
  "method": "PUT",
  "path": "/menu-items/{itemId}/availability",
  "contract": "fnb",
  "summary": "Mark an item available or eighty-sixed",
  "permission": "PRODUCT_CONFIGURE",
  "offlineCapable": true,
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
  "responds": "MenuItem"
 },
 "setPrices": {
  "method": "PUT",
  "path": "/price-lists/{priceListId}/prices",
  "contract": "catalogue",
  "summary": "Set prices in bulk",
  "permission": "PRICE_CONFIGURE",
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
 },
 "setProductAttributes": {
  "method": "PUT",
  "path": "/products/{productId}/attributes",
  "contract": "catalogue",
  "summary": "Set the attribute axes for a product",
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
 },
 "simulatePromotion": {
  "method": "POST",
  "path": "/promotions/{promotionId}/simulate",
  "contract": "promotions",
  "summary": "What this promotion would have cost on real history",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": null
 },
 "transitionProductLifecycle": {
  "method": "POST",
  "path": "/products/{productId}/lifecycle",
  "contract": "catalogue",
  "summary": "Move a product through its lifecycle",
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
  "responds": "Product"
 },
 "unschedulePromotion": {
  "method": "POST",
  "path": "/promotions/{promotionId}/unschedule",
  "contract": "promotions",
  "summary": "Pull a scheduled promotion before it starts",
  "permission": "PRICE_CONFIGURE",
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
 },
 "updateChannelCapacity": {
  "method": "PATCH",
  "path": "/channel-capacities/{channelCapacityId}",
  "contract": "catalogue",
  "summary": "Amend an envelope",
  "permission": "CAPACITY_CONFIGURE",
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
  "responds": "ChannelCapacity"
 },
 "updateEvent": {
  "method": "PATCH",
  "path": "/events/{eventId}",
  "contract": "catalogue",
  "summary": "Amend an event",
  "permission": "EVENT_CONFIGURE",
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
  "responds": "Event"
 },
 "updatePerformance": {
  "method": "PATCH",
  "path": "/performances/{performanceId}",
  "contract": "catalogue",
  "summary": "Amend a performance",
  "permission": "PERFORMANCE_CONFIGURE",
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
  "responds": "Performance"
 },
 "updatePriceList": {
  "method": "PATCH",
  "path": "/price-lists/{priceListId}",
  "contract": "catalogue",
  "summary": "Amend a price list",
  "permission": "PRICE_CONFIGURE",
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
  "responds": "PriceList"
 },
 "updateProduct": {
  "method": "PATCH",
  "path": "/products/{productId}",
  "contract": "catalogue",
  "summary": "Update a product",
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
  "requestBody": "UpdateProductRequest",
  "responds": "Product"
 },
 "updatePromotion": {
  "method": "PATCH",
  "path": "/promotions/{promotionId}",
  "contract": "promotions",
  "summary": "Amend a promotion",
  "permission": "PRICE_CONFIGURE",
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
  "responds": "Promotion"
 },
 "voidCouponCode": {
  "method": "POST",
  "path": "/coupon-codes/{code}/void",
  "contract": "promotions",
  "summary": "Void a code",
  "permission": "PRICE_CONFIGURE",
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
  "responds": "CouponCode"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AllocationComponent": {
  "x-ticvai-persistence": "promotions.allocation_component",
  "type": "object",
  "required": [
   "variantId"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "variantId": {
    "type": "string",
    "format": "uuid"
   },
   "percentage": {
    "type": "number",
    "minimum": 0,
    "maximum": 100
   },
   "fixedAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "listPrice": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "For `proRataListPrice` — weights derived from list prices."
   },
   "revenueAccountId": {
    "type": "string",
    "format": "uuid"
   },
   "legalEntityId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Set where the component is earned by a different legal entity. Cross-currency allocation is deferred pending the FX policy decision.\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   }
  }
 },
 "AllocationMethod": {
  "type": "string",
  "enum": [
   "percentage",
   "fixedAmount",
   "proRataListPrice"
  ]
 },
 "AlternativeCode": {
  "x-ticvai-persistence": "catalogue.alternative_code",
  "type": "object",
  "required": [
   "code",
   "partnerId"
  ],
  "properties": {
   "code": {
    "type": "string",
    "maxLength": 128
   },
   "partnerId": {
    "type": "string",
    "format": "uuid"
   },
   "partnerName": {
    "type": "string"
   },
   "variantId": {
    "type": "string",
    "format": "uuid"
   },
   "note": {
    "type": "string",
    "maxLength": 200
   }
  }
 },
 "Bundle": {
  "x-ticvai-persistence": "promotions.bundle + promotions.bundle_component",
  "allOf": [
   {
    "$ref": "#/components/schemas/CreateBundleRequest"
   },
   {
    "type": "object",
    "required": [
     "id",
     "savingsAmount",
     "isActive",
     "hasBeenSold"
    ],
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid"
     },
     "savingsAmount": {
      "allOf": [
       {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      ],
      "description": "Sum of component list prices less the bundle price."
     },
     "savingsPercentage": {
      "type": "number"
     },
     "hasBeenSold": {
      "type": "boolean",
      "description": "True locks components and allocation against amendment."
     },
     "isActive": {
      "type": "boolean"
     }
    }
   }
  ]
 },
 "BundleChoiceGroup": {
  "type": "object",
  "x-ticvai-persistence": "promotions.bundle_choice_group",
  "description": "**Pick n from a set** (3.5.10). The shape a dynamic bundle needs and `BundleComponent` could not express — it names specific variants, which describes a fixed bundle with swaps.\nThe bundle price does not move with the choice (ADR-0019). **The allocation does.**\n",
  "required": [
   "label",
   "choose",
   "options"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "label": {
    "type": "string",
    "description": "What the guest is asked. \"Choose 3 attractions\"."
   },
   "choose": {
    "type": "integer",
    "minimum": 1,
    "description": "How many options the guest picks."
   },
   "allowDuplicates": {
    "type": "boolean",
    "default": false,
    "description": "Whether the same option may be picked twice. False for attractions, sometimes true for F&B.\n"
   },
   "options": {
    "type": "array",
    "minItems": 2,
    "items": {
     "type": "object",
     "required": [
      "variantId"
     ],
     "properties": {
      "variantId": {
       "type": "string",
       "format": "uuid"
      },
      "quantity": {
       "type": "integer",
       "default": 1
      },
      "isDefault": {
       "type": "boolean",
       "default": false
      }
     }
    }
   },
   "unavailableBehaviour": {
    "type": "string",
    "enum": [
     "hideOption",
     "hideBundle"
    ],
    "default": "hideOption",
    "description": "An option that has sold out for the chosen date is **not offered**. Where the group can no longer be satisfied at all, the bundle itself becomes unavailable — **it is never sold with a component that cannot be delivered**, because a substitution the guest did not choose is a complaint at the gate.\n"
   }
  }
 },
 "BundleComponent": {
  "x-ticvai-persistence": "promotions.bundle_component",
  "type": "object",
  "required": [
   "variantId",
   "quantity"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "variantId": {
    "type": "string",
    "format": "uuid"
   },
   "quantity": {
    "type": "integer",
    "minimum": 1
   },
   "isOptional": {
    "type": "boolean",
    "default": false
   },
   "substituteVariantIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "For dynamic bundles — guest chooses among these."
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Where this component is redeemed. Differs from the selling venue for multi-venue passes, which is why the allocation split exists.\n"
   }
  }
 },
 "BundleKind": {
  "type": "string",
  "enum": [
   "fixed",
   "dynamic",
   "mandatory",
   "optional",
   "promotional"
  ]
 },
 "BundleSummary": {
  "x-ticvai-persistence": "none — projection over bundle",
  "type": "object",
  "required": [
   "version",
   "venueId",
   "publishedAt",
   "publishedBy",
   "contentHash",
   "staleAfter",
   "sizeBytes"
  ],
  "properties": {
   "version": {
    "type": "string"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "publishedAt": {
    "type": "string",
    "format": "date-time"
   },
   "publishedBy": {
    "type": "string",
    "format": "uuid"
   },
   "contentHash": {
    "type": "string"
   },
   "signatureKeyId": {
    "type": "string",
    "description": "Key that signed this bundle. A terminal offline across a key rotation needs a grace window, or it cannot verify the next bundle.\n"
   },
   "staleAfter": {
    "type": "string",
    "format": "date-time"
   },
   "sizeBytes": {
    "type": "integer"
   },
   "note": {
    "type": "string"
   },
   "appliedByWorkstations": {
    "type": "integer"
   }
  }
 },
 "CatalogueBundle": {
  "x-ticvai-persistence": "catalogue.published_bundle",
  "type": "object",
  "required": [
   "version",
   "venueId",
   "isDelta",
   "signature",
   "signatureKeyId",
   "contentHash",
   "staleAfter",
   "payload"
  ],
  "properties": {
   "version": {
    "type": "string"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "isDelta": {
    "type": "boolean"
   },
   "baseVersion": {
    "type": "string",
    "nullable": true,
    "description": "Present when `isDelta`. The version this delta applies to."
   },
   "signature": {
    "type": "string",
    "description": "Detached signature over `contentHash`. The terminal verifies before applying and rolls back on failure — a half-applied catalogue is never traded against.\n"
   },
   "signatureKeyId": {
    "type": "string"
   },
   "contentHash": {
    "type": "string"
   },
   "staleAfter": {
    "type": "string",
    "format": "date-time"
   },
   "payload": {
    "type": "object",
    "description": "Products, variants, price lists, prices, tax codes, events, performances, envelope definitions and data mask field definitions. Shape is versioned with the bundle format, not with this API.\n",
    "additionalProperties": true
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
 "ChannelAllocation": {
  "x-ticvai-persistence": "catalogue.channel_allocation",
  "type": "object",
  "required": [
   "channel",
   "allocatedUnits"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "channel": {
    "$ref": "#/components/schemas/Channel"
   },
   "allocatedUnits": {
    "type": "integer",
    "minimum": 0
   },
   "soldUnits": {
    "type": "integer",
    "readOnly": true
   },
   "leasedUnits": {
    "type": "integer",
    "readOnly": true,
    "description": "Held by terminals on this channel but not yet sold."
   },
   "remainingUnits": {
    "type": "integer",
    "readOnly": true
   },
   "releaseAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "Unsold units return to the general pool at this time. How distribution holds are freed close to a performance without someone remembering to do it.\n"
   }
  }
 },
 "ChannelAllocationSet": {
  "x-ticvai-persistence": "none — projection",
  "type": "object",
  "required": [
   "channelCapacityId",
   "capacity",
   "allocations",
   "generalPoolUnits"
  ],
  "properties": {
   "channelCapacityId": {
    "type": "string",
    "format": "uuid"
   },
   "capacity": {
    "type": "integer"
   },
   "allocations": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/ChannelAllocation"
    }
   },
   "generalPoolUnits": {
    "type": "integer",
    "description": "Unallocated remainder. Any channel may draw from it once its own allocation is exhausted.\n"
   },
   "totalSold": {
    "type": "integer"
   },
   "totalRemaining": {
    "type": "integer"
   }
  }
 },
 "ChannelCapacity": {
  "x-ticvai-persistence": "catalogue.channel_capacity",
  "type": "object",
  "required": [
   "id",
   "performanceId",
   "capacity",
   "sold",
   "leased",
   "remaining",
   "isSeated"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "performanceId": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string"
   },
   "seatCategoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "oversellAllowance": {
    "type": "integer",
    "default": 0,
    "description": "BL-046, 1.3.13. **The guard existed in one direction** — an envelope could be raised freely and refused reduction below what had sold.\n**Free events oversell deliberately because no-show rates are known.** An allowance on the envelope rather than an admission policy, because **the gate must still refuse when actual capacity is reached** — overselling is a sales decision and admission is a safety one, and they must not share a number.\n"
   },
   "oversellBasis": {
    "type": "string",
    "nullable": true,
    "enum": [
     "fixedCount",
     "historicNoShowRate",
     "percentage"
    ]
   },
   "capacity": {
    "type": "integer",
    "minimum": 0
   },
   "sold": {
    "type": "integer"
   },
   "leased": {
    "type": "integer"
   },
   "remaining": {
    "type": "integer"
   },
   "hasChannelAllocations": {
    "type": "boolean",
    "description": "True where capacity is divided across channels. Leases then draw from a channel allocation rather than from raw capacity.\n"
   },
   "isSeated": {
    "type": "boolean",
    "description": "Seated envelopes cannot be leased and are blocked offline. A seat map is not a count.\n"
   }
  }
 },
 "ChannelListing": {
  "type": "object",
  "x-ticvai-persistence": "control.channel_listing",
  "description": "BL-076. **The integration register marks *Resellers & OTA* as covered, and that is true of the commercial model and not of the integration.** Agreements, allocations and credit exist; the exchange with Viator, Klook, Headout and GetYourGuide does not.\n**An OTA is not a partner portal.** A partner logs in and books; an OTA pulls a feed, caches it, and sells against the cache — **so the failure mode is a sale against stale inventory**, and everything below exists to bound that.\n",
  "required": [
   "id",
   "channelName",
   "productId",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "channelName": {
    "type": "string",
    "enum": [
     "viator",
     "klook",
     "headout",
     "getYourGuide",
     "tiqets",
     "expedia",
     "other"
    ]
   },
   "productId": {
    "type": "string",
    "format": "uuid"
   },
   "externalProductRef": {
    "type": "string",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "draft",
     "live",
     "paused",
     "delisted"
    ]
   },
   "allocationUnits": {
    "type": "integer",
    "nullable": true,
    "description": "**Inventory published to this channel, not the venue's whole capacity.** An OTA given the full envelope will sell it, and the venue discovers at the gate.\n"
   },
   "priceListId": {
    "type": "string",
    "format": "uuid"
   },
   "adapter": {
    "type": "string",
    "nullable": true,
    "enum": [
     "viatorApi",
     "klookApi",
     "headoutApi",
     "getYourGuideApi",
     "tiqetsApi",
     "octoStandard",
     "generic"
    ],
    "description": "BL-067. **The commercial model was complete and the wire was not** — `PartnerAgreement` carries rates, commission, credit and channels, and `alternative-codes` maps a partner SKU so an inbound order matches. What was missing is which protocol speaks to whom.\n**`octoStandard` is the one that matters.** OCTo is the open connectivity standard the OTAs converged on, and a venue that implements it once reaches several channels — **a per-OTA adapter is a per-OTA maintenance commitment**, and naming the standard first is what keeps that list from growing.\n"
   },
   "adapterCredentialRef": {
    "type": "string",
    "nullable": true,
    "description": "A vault reference. **Never the credential**, following the rule ADR-0020 set for AI providers."
   },
   "pushIntervalMinutes": {
    "type": "integer",
    "default": 15,
    "description": "How often availability is pushed. **The gap between pushes is the oversell window**, and a channel selling a high-demand slot needs a shorter one than a channel selling a museum on a Tuesday.\n"
   },
   "guestDataScope": {
    "type": "string",
    "enum": [
     "none",
     "nameOnly",
     "nameAndContact",
     "full"
    ],
    "default": "nameOnly",
    "description": "**What the OTA passes through, and it is usually less than the venue wants.** A ticket arriving with no contact detail cannot be reissued or notified of a cancellation, and the venue should know that at listing time rather than at the gate.\n"
   },
   "lastPushedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"
   }
  }
 },
 "ConflictAnalysis": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "promotionId",
   "conflicts",
   "worstCaseDiscount"
  ],
  "properties": {
   "promotionId": {
    "type": "string",
    "format": "uuid"
   },
   "conflicts": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "otherPromotionId",
      "otherPromotionCode",
      "overlap",
      "combinedDiscount"
     ],
     "properties": {
      "otherPromotionId": {
       "type": "string",
       "format": "uuid"
      },
      "otherPromotionCode": {
       "type": "string"
      },
      "overlap": {
       "type": "string",
       "enum": [
        "products",
        "period",
        "channel",
        "full"
       ]
      },
      "combinedDiscount": {
       "type": "number",
       "description": "Combined percentage where both apply to the same line."
      },
      "isBlocking": {
       "type": "boolean",
       "description": "True where the combination would produce a negative or near-zero price."
      }
     }
    }
   },
   "worstCaseDiscount": {
    "type": "number",
    "description": "Largest combined discount any single line could receive."
   }
  }
 },
 "CouponCampaign": {
  "x-ticvai-persistence": "promotions.coupon_campaign",
  "allOf": [
   {
    "$ref": "#/components/schemas/CreateCouponCampaignRequest"
   },
   {
    "type": "object",
    "required": [
     "id",
     "generatedCount",
     "redeemedCount"
    ],
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid"
     },
     "generatedCount": {
      "type": "integer"
     },
     "redeemedCount": {
      "type": "integer"
     },
     "isActive": {
      "type": "boolean"
     }
    }
   }
  ]
 },
 "CouponCode": {
  "x-ticvai-persistence": "promotions.coupon_code",
  "type": "object",
  "required": [
   "code",
   "campaignId",
   "status"
  ],
  "properties": {
   "code": {
    "type": "string"
   },
   "campaignId": {
    "type": "string",
    "format": "uuid"
   },
   "status": {
    "$ref": "#/components/schemas/CouponStatus"
   },
   "assignedSubjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "redemptionCount": {
    "type": "integer"
   },
   "maxRedemptions": {
    "type": "integer"
   },
   "discount": {
    "$ref": "#/components/schemas/Discount"
   },
   "invalidReason": {
    "type": "string",
    "nullable": true,
    "description": "Why the code cannot be applied. A cashier reading `expired` to a guest is a very different conversation from reading `already used`.\n",
    "enum": [
     "expired",
     "alreadyRedeemed",
     "voided",
     "notYetValid",
     "wrongVenue",
     "conditionsNotMet",
     "notAssignedToGuest"
    ]
   },
   "validFrom": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "validTo": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "redeemedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "redeemedOrderId": {
    "type": "string",
    "nullable": true
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"
   }
  }
 },
 "CouponStatus": {
  "type": "string",
  "enum": [
   "issued",
   "assigned",
   "redeemed",
   "expired",
   "voided"
  ]
 },
 "CreateBundleRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "code",
   "name",
   "venueId",
   "kind",
   "price",
   "components",
   "allocation"
  ],
  "properties": {
   "code": {
    "type": "string",
    "maxLength": 64
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "description": {
    "type": "string",
    "maxLength": 1000
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "$ref": "#/components/schemas/BundleKind"
   },
   "price": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "components": {
    "type": "array",
    "minItems": 0,
    "items": {
     "$ref": "#/components/schemas/BundleComponent"
    }
   },
   "choiceGroups": {
    "type": "array",
    "description": "Dynamic bundles (3.5.10). A bundle may carry fixed components and choice groups at once — a family pass with fixed parking and two groups the guest chooses from. **The bundle price does not move with the choice** (ADR-0019).\n",
    "items": {
     "$ref": "#/components/schemas/BundleChoiceGroup"
    }
   },
   "allocation": {
    "type": "object",
    "required": [
     "method",
     "components"
    ],
    "properties": {
     "method": {
      "$ref": "#/components/schemas/AllocationMethod"
     },
     "components": {
      "type": "array",
      "items": {
       "$ref": "#/components/schemas/AllocationComponent"
      }
     }
    }
   },
   "validFrom": {
    "type": "string",
    "format": "date-time"
   },
   "validTo": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "CreateCouponCampaignRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "code",
   "name",
   "venueId",
   "discount",
   "validFrom"
  ],
  "properties": {
   "code": {
    "type": "string",
    "maxLength": 64
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "discount": {
    "$ref": "#/components/schemas/Discount"
   },
   "conditions": {
    "$ref": "#/components/schemas/PromotionConditions"
   },
   "isSingleUse": {
    "type": "boolean",
    "default": true,
    "description": "True generates individually redeemable codes. False issues one shared code with a redemption limit.\n"
   },
   "maxRedemptionsPerCode": {
    "type": "integer",
    "default": 1
   },
   "validFrom": {
    "type": "string",
    "format": "date-time"
   },
   "validTo": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "CreateEnvelopeRequest": {
  "type": "object",
  "required": [
   "performanceId",
   "name",
   "capacity"
  ],
  "properties": {
   "performanceId": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "seatCategoryId": {
    "type": "string",
    "format": "uuid"
   },
   "capacity": {
    "type": "integer",
    "minimum": 0
   }
  }
 },
 "CreateEventRequest": {
  "type": "object",
  "required": [
   "code",
   "name",
   "venueId"
  ],
  "properties": {
   "code": {
    "type": "string",
    "maxLength": 64
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "parentEventId": {
    "type": "string",
    "format": "uuid"
   }
  }
 },
 "CreateMerchandiseRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "sku",
   "name",
   "outletId",
   "variantId"
  ],
  "properties": {
   "sku": {
    "type": "string",
    "maxLength": 64
   },
   "barcode": {
    "type": "string",
    "maxLength": 128
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "outletId": {
    "type": "string",
    "format": "uuid"
   },
   "categoryId": {
    "type": "string",
    "format": "uuid"
   },
   "variantId": {
    "type": "string",
    "format": "uuid"
   },
   "inventoryItemId": {
    "type": "string",
    "format": "uuid"
   },
   "isReturnable": {
    "type": "boolean",
    "default": true
   },
   "returnWindowDays": {
    "type": "integer"
   },
   "requiresSerialNumber": {
    "type": "boolean",
    "default": false
   },
   "imageAssetRef": {
    "type": "string"
   }
  }
 },
 "CreatePerformancesRequest": {
  "type": "object",
  "required": [
   "startsAt",
   "endsAt"
  ],
  "properties": {
   "startsAt": {
    "type": "string",
    "format": "date-time"
   },
   "endsAt": {
    "type": "string",
    "format": "date-time"
   },
   "admissionRulesId": {
    "type": "string",
    "format": "uuid"
   },
   "seatMapId": {
    "type": "string",
    "format": "uuid"
   },
   "recurrence": {
    "type": "object",
    "description": "Generate a series rather than a single performance.",
    "properties": {
     "intervalMinutes": {
      "type": "integer",
      "minimum": 1
     },
     "until": {
      "type": "string",
      "format": "date-time"
     },
     "daysOfWeek": {
      "type": "array",
      "items": {
       "type": "integer",
       "minimum": 0,
       "maximum": 6
      }
     }
    }
   }
  }
 },
 "CreatePriceListRequest": {
  "type": "object",
  "required": [
   "code",
   "name",
   "venueId",
   "channels"
  ],
  "properties": {
   "code": {
    "type": "string",
    "maxLength": 64
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "channels": {
    "type": "array",
    "minItems": 1,
    "items": {
     "$ref": "#/components/schemas/Channel"
    }
   },
   "validFrom": {
    "type": "string",
    "format": "date-time"
   },
   "validTo": {
    "type": "string",
    "format": "date-time"
   },
   "priority": {
    "type": "integer",
    "default": 0
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
 "CreatePromotionRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "code",
   "name",
   "venueId",
   "discount",
   "validFrom"
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
    "type": "string",
    "maxLength": 1000
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "discount": {
    "$ref": "#/components/schemas/Discount"
   },
   "conditions": {
    "$ref": "#/components/schemas/PromotionConditions"
   },
   "stackingMode": {
    "allOf": [
     {
      "$ref": "#/components/schemas/StackingMode"
     }
    ],
    "default": "bestOnly"
   },
   "stackingGroup": {
    "type": "string",
    "maxLength": 64
   },
   "precedence": {
    "type": "integer",
    "default": 0,
    "description": "Higher evaluates first where several could apply."
   },
   "validFrom": {
    "type": "string",
    "format": "date-time"
   },
   "validTo": {
    "type": "string",
    "format": "date-time"
   },
   "maxRedemptions": {
    "type": "integer",
    "nullable": true
   },
   "maxRedemptionsPerGuest": {
    "type": "integer",
    "nullable": true
   },
   "budgetCap": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Total discount value after which the promotion stops automatically."
   }
  }
 },
 "Dashboard": {
  "x-ticvai-persistence": "reporting.dashboard + reporting.dashboard_tile",
  "allOf": [
   {
    "$ref": "#/components/schemas/CreateDashboardRequest"
   },
   {
    "type": "object",
    "required": [
     "id",
     "ownerPrincipalId",
     "aggregateCost",
     "createdAt"
    ],
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid"
     },
     "ownerPrincipalId": {
      "type": "string",
      "format": "uuid"
     },
     "aggregateCost": {
      "type": "string",
      "enum": [
       "low",
       "medium",
       "high"
      ],
      "description": "Combined refresh load of every tile."
     },
     "createdAt": {
      "type": "string",
      "format": "date-time"
     }
    }
   }
  ]
 },
 "DashboardData": {
  "x-ticvai-persistence": "none — computed",
  "allOf": [
   {
    "$ref": "#/components/schemas/Dashboard"
   },
   {
    "type": "object",
    "properties": {
     "tileData": {
      "type": "array",
      "items": {
       "type": "object",
       "properties": {
        "tileId": {
         "type": "string",
         "format": "uuid"
        },
        "result": {
         "$ref": "#/components/schemas/ReportResult"
        },
        "isCached": {
         "type": "boolean"
        },
        "error": {
         "type": "string",
         "nullable": true
        }
       }
      }
     }
    }
   }
  ]
 },
 "Discount": {
  "x-ticvai-persistence": "none — embedded in promotion",
  "type": "object",
  "required": [
   "kind"
  ],
  "properties": {
   "kind": {
    "$ref": "#/components/schemas/DiscountKind"
   },
   "percentage": {
    "type": "number",
    "minimum": 0,
    "maximum": 100
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "fixedPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "buyQuantity": {
    "type": "integer",
    "minimum": 1
   },
   "getQuantity": {
    "type": "integer",
    "minimum": 1
   },
   "getDiscountPercentage": {
    "type": "number",
    "minimum": 0,
    "maximum": 100,
    "description": "100 makes the free items actually free; lower values give a partial discount."
   },
   "tiers": {
    "type": "array",
    "description": "For `tieredPercentage` — more units, larger discount.",
    "items": {
     "type": "object",
     "required": [
      "minQuantity",
      "percentage"
     ],
     "properties": {
      "minQuantity": {
       "type": "integer",
       "minimum": 1
      },
      "percentage": {
       "type": "number",
       "minimum": 0,
       "maximum": 100
      }
     }
    }
   },
   "maxDiscountAmount": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Cap on a percentage discount. Prevents an unbounded discount on a large basket."
   }
  }
 },
 "EntitlementTemplate": {
  "x-ticvai-persistence": "catalogue.entitlement_template",
  "type": "object",
  "required": [
   "id",
   "code",
   "name",
   "validityKind"
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
   "validityKind": {
    "type": "string",
    "enum": [
     "singleUse",
     "dated",
     "dateRange",
     "rolling",
     "unlimited",
     "countLimited"
    ]
   },
   "validFromOffsetDays": {
    "type": "integer",
    "nullable": true
   },
   "validForDays": {
    "type": "integer",
    "nullable": true
   },
   "daysOfWeek": {
    "type": "array",
    "nullable": true,
    "description": "1.1.7 and 1.1.82. **A camp ticket admits on Tuesdays and Thursdays for six weeks**, and `validityKind` had six values with no day pattern among them.\nThe shape is settled elsewhere in the package — `fnb.MenuAvailability` and `promotions.PromotionConditions` both carry it. **Null means every day**, which is what every existing entitlement means today.\n",
    "items": {
     "type": "string",
     "enum": [
      "mon",
      "tue",
      "wed",
      "thu",
      "fri",
      "sat",
      "sun"
     ]
    }
   },
   "expiryAnchor": {
    "type": "string",
    "nullable": true,
    "enum": [
     "offsetDays",
     "endOfMonth",
     "endOfQuarter",
     "endOfYear",
     "fixedDate",
     "seasonEnd"
    ],
    "description": "1.1.90 to 1.1.92. **A pass bought on the 20th and expiring on the 31st cannot be expressed by an offset in days.** `offsetDays` is the existing behaviour and stays the default.\n`seasonEnd` anchors to the venue's own season rather than the calendar — a water park closing in October is not a quarter boundary.\n"
   },
   "expiryDate": {
    "type": "string",
    "format": "date",
    "nullable": true,
    "description": "Where `expiryAnchor` is `fixedDate`. Every pass expires the same day regardless of purchase."
   },
   "carriesStoredValue": {
    "type": "boolean",
    "default": false,
    "description": "BL-033. **A ticket that is also a wallet** — a resort pass with 200 dirhams of spend on it, deducted at a gate or a till.\n**The value is a `retail.Wallet` bound to the entitlement, not a balance on the ticket.** One balance mechanism (CF-126), so it holds authorisations, expires by credit type and appears in the same reports — a second balance on the entitlement would have been the seventh implementation.\n"
   },
   "includedValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "validTimeWindows": {
    "type": "array",
    "nullable": true,
    "description": "BL-036, 1.1.81 and 1.1.83. **A time-window entitlement needed a performance to express** — valid 09:00 to 13:00 on any day was a thing you built by creating performances.\n**A window is a property of the entitlement and a performance is an occurrence**, and conflating them means a morning pass generates 365 performances a year.\n",
    "items": {
     "type": "object",
     "properties": {
      "from": {
       "type": "string"
      },
      "to": {
       "type": "string"
      },
      "daysOfWeek": {
       "type": "array",
       "items": {
        "type": "string"
       }
      }
     }
    }
   },
   "blackoutDates": {
    "type": "array",
    "nullable": true,
    "description": "**Calendar exceptions on the entitlement.** An annual pass excluding public holidays is the normal case and had nowhere to live.\n",
    "items": {
     "type": "string",
     "format": "date"
    }
   },
   "fastTrackTier": {
    "type": "string",
    "nullable": true,
    "enum": [
     "none",
     "priority",
     "express",
     "unlimited"
    ],
    "description": "19.2.20, BL-015. **Fast track existed nowhere in the package** — not an enum value, not a description, not a screen.\n**An attribute of the entitlement rather than a queue class or a product kind**, because the same ride serves standby and fast-track guests from one capacity: `queue` already has `isFastPass` on an entry and needed something to read it from.\n"
   },
   "entriesAllowed": {
    "type": "integer",
    "nullable": true,
    "description": "Null means unlimited. The Fast Pass consumption counter lives here."
   },
   "reentryAllowed": {
    "type": "boolean",
    "default": false
   },
   "purchaseEligibility": {
    "type": "object",
    "nullable": true,
    "description": "1.1.38, 1.1.121, 1.1.125, 1.1.126. **`admissionRulesId` governs where an entitlement admits, not who may buy it**, and `promotions.evaluatePromotions` gates a discount rather than a sale. Neither refuses a purchase.\n**Evaluated at add-to-cart, not at checkout.** A guest told at payment that they cannot buy a resident rate has already entered a card.\n",
    "properties": {
     "minAgeYears": {
      "type": "integer",
      "nullable": true
     },
     "maxAgeYears": {
      "type": "integer",
      "nullable": true
     },
     "minHeightCm": {
      "type": "integer",
      "nullable": true,
      "description": "**Height gates a ride and can gate a sale.** A ticket sold to somebody who cannot ride it is a refund at the gate.\n"
     },
     "residencyRequired": {
      "type": "boolean",
      "default": false
     },
     "nationalities": {
      "type": "array",
      "nullable": true,
      "items": {
       "type": "string"
      }
     },
     "minLoyaltyTier": {
      "type": "string",
      "nullable": true
     },
     "requiresVerification": {
      "type": "boolean",
      "default": false,
      "description": "**Whether the claim is checked or taken on trust.** A resident rate sold unverified and refused at the gate is worse than one that could not be bought.\n"
     }
    }
   },
   "personType": {
    "type": "string",
    "nullable": true,
    "enum": [
     "adult",
     "child",
     "infant",
     "senior",
     "student",
     "resident",
     "staff"
    ],
    "description": "2.11.7. **Adult, child and senior existed only as `ProductVariant.axisValues` — a variant axis rather than an attribute of the holder.** So changing a child ticket to an adult one was an exchange to a different product, and an upgrade that should be a price difference became a cancel-and-rebuy.\nRecorded here as well as on the variant, because **the guest ages and the product does not.**\n"
   },
   "admissionRulesId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "isTransferable": {
    "type": "boolean",
    "default": true
   },
   "canShareMedia": {
    "type": "boolean",
    "default": true,
    "description": "Whether this entitlement may be appended to media a guest already holds (CF-58). False for anything surrendered at use — a single-entry ticket taken at the gate is not a claim token for a locker bought afterwards.\n"
   },
   "canClaimShopAndDrop": {
    "type": "boolean",
    "default": false,
    "description": "Whether this entitlement may be scanned to claim goods left under 4.4.7. False for a single-entry ticket that is surrendered at the gate — a claim token the guest no longer holds is not a claim token.\n"
   },
   "isNameBound": {
    "type": "boolean",
    "default": false,
    "description": "True requires a holder name at sale. Most entitlements carry none — identity and entitlement are separate concerns.\n"
   },
   "crossesCells": {
    "type": "boolean",
    "default": false,
    "description": "True propagates a redemption right to other cells on issue (ADR-0010).\n"
   },
   "isActive": {
    "type": "boolean"
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"
   }
  }
 },
 "EvaluatePromotionsRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "venueId",
   "channel",
   "lines"
  ],
  "properties": {
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "channel": {
    "type": "string"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "membershipTierId": {
    "type": "string",
    "format": "uuid"
   },
   "couponCodes": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "evaluateAt": {
    "type": "string",
    "format": "date-time",
    "description": "For back-office testing of a rule before publishing."
   },
   "lines": {
    "type": "array",
    "minItems": 1,
    "items": {
     "type": "object",
     "required": [
      "lineId",
      "variantId",
      "quantity",
      "unitPrice"
     ],
     "properties": {
      "lineId": {
       "type": "string"
      },
      "variantId": {
       "type": "string",
       "format": "uuid"
      },
      "performanceId": {
       "type": "string",
       "format": "uuid"
      },
      "quantity": {
       "type": "integer",
       "minimum": 1
      },
      "unitPrice": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      }
     }
    }
   }
  }
 },
 "Event": {
  "x-ticvai-persistence": "catalogue.event",
  "type": "object",
  "required": [
   "id",
   "code",
   "name",
   "venueId",
   "scopePath"
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
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string"
   },
   "parentEventId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "For grouped events."
   },
   "performanceCount": {
    "type": "integer"
   },
   "isActive": {
    "type": "boolean"
   }
  }
 },
 "FieldType": {
  "type": "string",
  "enum": [
   "string",
   "integer",
   "decimal",
   "money",
   "boolean",
   "date",
   "dateTime",
   "uuid",
   "enum"
  ]
 },
 "MenuItem": {
  "x-ticvai-persistence": "fnb.menu_item",
  "type": "object",
  "required": [
   "id",
   "productVariantId",
   "name",
   "price",
   "isAvailable"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "productVariantId": {
    "type": "string",
    "format": "uuid",
    "description": "The catalogue variant this item sells. Pricing and tax come from there — a menu is a presentation of the catalogue, not a second catalogue.\n"
   },
   "name": {
    "type": "string"
   },
   "description": {
    "type": "string",
    "nullable": true
   },
   "price": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "sortOrder": {
    "type": "integer"
   },
   "modifierGroupIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "stationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "isStockTracked": {
    "type": "boolean",
    "description": "True where a recipe exists. Stock-tracked items cannot be sold offline."
   },
   "isAvailable": {
    "type": "boolean"
   },
   "unavailableReason": {
    "type": "string",
    "nullable": true
   },
   "preparationMinutes": {
    "type": "integer",
    "nullable": true
   },
   "allergens": {
    "type": "array",
    "items": {
     "type": "string"
    }
   }
  }
 },
 "MerchandiseItem": {
  "x-ticvai-persistence": "retail.merchandise",
  "type": "object",
  "required": [
   "id",
   "sku",
   "name",
   "outletId",
   "variantId",
   "price",
   "onHand",
   "isActive"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "sku": {
    "type": "string"
   },
   "barcode": {
    "type": "string",
    "nullable": true
   },
   "name": {
    "type": "string"
   },
   "outletId": {
    "type": "string",
    "format": "uuid"
   },
   "categoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "variantId": {
    "type": "string",
    "format": "uuid",
    "description": "The catalogue variant sold. Price and tax come from there."
   },
   "inventoryItemId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The stock item depleted on sale. Null means the item sells but never runs out, which is almost always a configuration error.\n"
   },
   "price": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "onHand": {
    "type": "number"
   },
   "isReturnable": {
    "type": "boolean",
    "default": true
   },
   "returnWindowDays": {
    "type": "integer",
    "nullable": true
   },
   "requiresSerialNumber": {
    "type": "boolean",
    "default": false
   },
   "imageAssetRef": {
    "type": "string",
    "nullable": true
   },
   "isActive": {
    "type": "boolean"
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
 "Performance": {
  "x-ticvai-persistence": "catalogue.performance",
  "type": "object",
  "required": [
   "id",
   "eventId",
   "startsAt",
   "endsAt",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "eventId": {
    "type": "string",
    "format": "uuid"
   },
   "startsAt": {
    "type": "string",
    "format": "date-time"
   },
   "endsAt": {
    "type": "string",
    "format": "date-time"
   },
   "approvalRequestId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "BL-048. **The approval chain and the occurrence lifecycle sat on different entities**, so neither was complete: `states/performance.yaml` models scheduled, onSale, soldOut, suspended, cancelled and completed properly, and nothing said which of those transitions somebody had to sign.\n**Set on the transition that needs it, not on the performance.** Publishing a performance is routine; cancelling one that has sold is the act somebody signs — and binding approval to the whole entity would have required a signature to reschedule a wet Tuesday.\n"
   },
   "requiresApprovalToCancel": {
    "type": "boolean",
    "default": true,
    "description": "**Cancelling a sold performance is the one transition that needs a name against it.** `assessProductChange` already answers how many tickets are affected; this decides who has to look at that number before the button works.\n"
   },
   "status": {
    "type": "string",
    "enum": [
     "scheduled",
     "onSale",
     "soldOut",
     "suspended",
     "cancelled",
     "completed"
    ]
   },
   "admissionRulesId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "seatMapId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   }
  }
 },
 "PerformanceCancellationResult": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "performanceId",
   "dryRun",
   "affectedOrders",
   "refundExposure"
  ],
  "properties": {
   "performanceId": {
    "type": "string",
    "format": "uuid"
   },
   "dryRun": {
    "type": "boolean"
   },
   "affectedOrders": {
    "type": "integer"
   },
   "affectedGuests": {
    "type": "integer"
   },
   "refundExposure": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "What the cancellation costs. Returned before committing, so the person cancelling sees the number at the moment they decide.\n"
   },
   "bulkRefundBatchId": {
    "type": "string",
    "nullable": true,
    "description": "Queued for approval. Refunds are not issued automatically."
   },
   "notificationsQueued": {
    "type": "integer"
   }
  }
 },
 "PriceList": {
  "x-ticvai-persistence": "catalogue.price_list",
  "type": "object",
  "required": [
   "id",
   "code",
   "name",
   "venueId",
   "currency",
   "currencyScale",
   "channels"
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
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "currency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "x-ticvai-persisted": false,
    "description": "**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"
   },
   "currencyScale": {
    "type": "integer",
    "minimum": 0,
    "maximum": 4,
    "x-ticvai-persisted": false,
    "description": "**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"
   },
   "channels": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/Channel"
    }
   },
   "validFrom": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "validTo": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "priority": {
    "type": "integer",
    "description": "Where lists overlap, higher priority wins."
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
 "ProductVariant": {
  "x-ticvai-persistence": "catalogue.variant",
  "type": "object",
  "required": [
   "id",
   "productId",
   "sku",
   "axisValues",
   "isActive"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "productId": {
    "type": "string",
    "format": "uuid"
   },
   "sku": {
    "type": "string"
   },
   "axisValues": {
    "type": "object",
    "additionalProperties": {
     "type": "string"
    }
   },
   "isActive": {
    "type": "boolean",
    "description": "False when retired. Retired variants are never deleted — orders reference them."
   }
  }
 },
 "Promotion": {
  "x-ticvai-persistence": "promotions.promotion",
  "allOf": [
   {
    "$ref": "#/components/schemas/CreatePromotionRequest"
   },
   {
    "type": "object",
    "required": [
     "id",
     "status"
    ],
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid"
     },
     "status": {
      "$ref": "#/components/schemas/PromotionStatus"
     },
     "isPaused": {
      "type": "boolean"
     },
     "redemptionCount": {
      "type": "integer"
     },
     "discountGiven": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "publishedAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     }
    }
   }
  ]
 },
 "PromotionConditions": {
  "x-ticvai-persistence": "none — embedded in promotion",
  "type": "object",
  "description": "All conditions must hold. An empty object matches everything.",
  "properties": {
   "variantIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "productKinds": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "categoryIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "minQuantity": {
    "type": "integer",
    "minimum": 1
   },
   "minBasketValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "channels": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "purchaseGate": {
    "type": "boolean",
    "default": false,
    "description": "BL-037. **`evaluatePromotions` gates a price and nothing gated a sale.** A non-member could buy a member-only product at the member price refused, which is a discount failure rather than an eligibility one.\nTrue makes these conditions a **precondition of purchase**: fail them and the line cannot be added, not merely charged more. **Evaluated at add-to-cart**, because a guest told at payment has already entered a card.\n"
   },
   "paymentMethod": {
    "type": "array",
    "nullable": true,
    "description": "BL-113. **Card-issuer and payment-type promotions** — *10% with a Network International card* is a real campaign a bank co-funds, and it was unexpressible.\n**Evaluated at payment, not at cart**, which is the awkward part: the discount appears after the tender is chosen, and the basket total must be allowed to move at that point.\n",
    "items": {
     "type": "string"
    }
   },
   "issuerBins": {
    "type": "array",
    "nullable": true,
    "description": "Card BIN ranges, where the campaign is issuer-specific rather than scheme-specific. **The bank supplies these and they change**, so they are data rather than configuration.\n",
    "items": {
     "type": "string"
    }
   },
   "componentRedemption": {
    "type": "string",
    "nullable": true,
    "enum": [
     "allTogether",
     "independently",
     "sequenced"
    ],
    "description": "BL-112. **Per-component redemption inside a bundle was unstated.** A park-plus-lunch bundle where lunch may be used another day behaves differently from one where both must be used on the same visit, and **the difference is revenue recognition, not just convenience.**\n"
   },
   "daysOfWeek": {
    "type": "array",
    "items": {
     "type": "integer",
     "minimum": 0,
     "maximum": 6
    }
   },
   "startTime": {
    "type": "string",
    "pattern": "^([01]\\d|2[0-3]):[0-5]\\d$"
   },
   "endTime": {
    "type": "string",
    "pattern": "^([01]\\d|2[0-3]):[0-5]\\d$"
   },
   "membershipTierIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "requiresCoupon": {
    "type": "boolean",
    "default": false
   },
   "firstPurchaseOnly": {
    "type": "boolean",
    "default": false
   },
   "performanceIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "advanceDaysMin": {
    "type": "integer",
    "description": "Early-bird — booked at least this many days ahead."
   },
   "advanceDaysMax": {
    "type": "integer",
    "description": "Last-minute — booked no more than this many days ahead."
   }
  }
 },
 "PromotionEvaluation": {
  "x-ticvai-persistence": "none — computed",
  "parameters": [
   {
    "$ref": "../shared/common.yaml#/components/parameters/IdempotencyKey"
   }
  ],
  "type": "object",
  "required": [
   "totalDiscount",
   "lines",
   "applied",
   "rejected"
  ],
  "properties": {
   "totalDiscount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "lines": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "lineId",
      "originalPrice",
      "discountedPrice",
      "discount"
     ],
     "properties": {
      "lineId": {
       "type": "string"
      },
      "originalPrice": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "discountedPrice": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "discount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "appliedPromotionIds": {
       "type": "array",
       "items": {
        "type": "string",
        "format": "uuid"
       }
      }
     }
    }
   },
   "applied": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "promotionId",
      "promotionCode",
      "discount"
     ],
     "properties": {
      "promotionId": {
       "type": "string",
       "format": "uuid"
      },
      "promotionCode": {
       "type": "string"
      },
      "promotionName": {
       "type": "string"
      },
      "discount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "couponCode": {
       "type": "string",
       "nullable": true
      }
     }
    }
   },
   "rejected": {
    "type": "array",
    "description": "Promotions that matched the products but did not apply, with the reason. This is what a cashier reads to a guest who expected a discount.\n",
    "items": {
     "type": "object",
     "required": [
      "promotionCode",
      "reason"
     ],
     "properties": {
      "promotionCode": {
       "type": "string"
      },
      "promotionName": {
       "type": "string"
      },
      "reason": {
       "type": "string",
       "enum": [
        "conditionsNotMet",
        "supersededByBetterOffer",
        "exclusivePromotionApplied",
        "redemptionLimitReached",
        "budgetExhausted",
        "outsideValidPeriod",
        "wrongChannel",
        "membershipRequired",
        "couponRequired"
       ]
      },
      "detail": {
       "type": "string"
      }
     }
    }
   }
  }
 },
 "PromotionStatus": {
  "type": "string",
  "enum": [
   "draft",
   "scheduled",
   "live",
   "paused",
   "expired",
   "ended"
  ]
 },
 "PromotionUsage": {
  "x-ticvai-persistence": "none — aggregated from ledger and orders",
  "type": "object",
  "required": [
   "promotionId",
   "redemptionCount",
   "discountGiven"
  ],
  "properties": {
   "promotionId": {
    "type": "string",
    "format": "uuid"
   },
   "redemptionCount": {
    "type": "integer"
   },
   "discountGiven": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "budgetCap": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "budgetRemaining": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "isBudgetExhausted": {
    "type": "boolean"
   },
   "byChannel": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "channel": {
       "type": "string"
      },
      "redemptionCount": {
       "type": "integer"
      },
      "discountGiven": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      }
     }
    }
   }
  }
 },
 "ReportResult": {
  "x-ticvai-persistence": "none — result set, cached in object storage",
  "type": "object",
  "required": [
   "executionId",
   "columns",
   "rows"
  ],
  "properties": {
   "executionId": {
    "type": "string"
   },
   "columns": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "key": {
       "type": "string"
      },
      "label": {
       "type": "string"
      },
      "type": {
       "$ref": "#/components/schemas/FieldType"
      }
     }
    }
   },
   "rows": {
    "type": "array",
    "items": {
     "type": "object",
     "additionalProperties": true
    }
   },
   "totals": {
    "type": "object",
    "additionalProperties": true
   },
   "rowCount": {
    "type": "integer"
   },
   "nextCursor": {
    "type": "string",
    "nullable": true
   },
   "generatedAt": {
    "type": "string",
    "format": "date-time"
   },
   "dataAsOf": {
    "type": "string",
    "format": "date-time",
    "description": "Replica position the result was read at. Reporting reads a lag-tolerant replica, so this may trail the primary by seconds — stating it prevents an argument about a figure that moved.\n"
   }
  }
 },
 "RunReportRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "properties": {
   "parameters": {
    "type": "object",
    "additionalProperties": true
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "description": "Narrows to one venue. Omitting it returns everything the caller's scope permits — it cannot be used to reach beyond that.\n"
   },
   "dateFrom": {
    "type": "string",
    "format": "date"
   },
   "dateTo": {
    "type": "string",
    "format": "date"
   },
   "forceAsync": {
    "type": "boolean",
    "default": false,
    "description": "Queue regardless of size, for a result to be collected later."
   }
  }
 },
 "SeatAvailability": {
  "x-ticvai-persistence": "none — computed from seat, hold and block",
  "type": "object",
  "required": [
   "performanceId",
   "seatMapId",
   "totals",
   "seats"
  ],
  "properties": {
   "performanceId": {
    "type": "string",
    "format": "uuid"
   },
   "seatMapId": {
    "type": "string",
    "format": "uuid"
   },
   "totals": {
    "type": "object",
    "properties": {
     "total": {
      "type": "integer"
     },
     "available": {
      "type": "integer"
     },
     "held": {
      "type": "integer"
     },
     "sold": {
      "type": "integer"
     },
     "blocked": {
      "type": "integer"
     },
     "buffered": {
      "type": "integer"
     }
    }
   },
   "byCategory": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "categoryId": {
       "type": "string",
       "format": "uuid"
      },
      "available": {
       "type": "integer"
      },
      "sold": {
       "type": "integer"
      },
      "price": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      }
     }
    }
   },
   "seats": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "seatId",
      "status"
     ],
     "properties": {
      "seatId": {
       "type": "string"
      },
      "status": {
       "$ref": "#/components/schemas/SeatStatus"
      },
      "categoryId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      }
     }
    }
   }
  }
 },
 "SeatRecommendationRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "partySize",
   "strategy"
  ],
  "properties": {
   "partySize": {
    "type": "integer",
    "minimum": 1,
    "maximum": 50
   },
   "strategy": {
    "$ref": "#/components/schemas/SeatRecommendationStrategy"
   },
   "categoryIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "maxPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "accessibleCount": {
    "type": "integer",
    "default": 0,
    "description": "Wheelchair spaces in the party. Companions are added automatically."
   },
   "maxOptions": {
    "type": "integer",
    "default": 3,
    "maximum": 10
   }
  }
 },
 "SeatRecommendationStrategy": {
  "type": "string",
  "enum": [
   "bestAvailable",
   "bestValue",
   "closestToStage",
   "accessible",
   "contiguous"
  ]
 },
 "SeatStatus": {
  "type": "string",
  "enum": [
   "available",
   "held",
   "sold",
   "blocked",
   "buffered",
   "unavailable"
  ]
 },
 "StackingMode": {
  "type": "string",
  "description": "How this promotion combines with others. Declared, never inferred from creation order — two reasonable promotions can otherwise combine into a free ticket.\n",
  "enum": [
   "exclusive",
   "stackable",
   "bestOnly",
   "stackWithGroup"
  ]
 },
 "UpdateProductRequest": {
  "type": "object",
  "minProperties": 1,
  "properties": {
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "description": {
    "type": "string"
   },
   "isSellable": {
    "type": "boolean"
   },
   "channels": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/Channel"
    }
   },
   "dataMaskValues": {
    "type": "object",
    "additionalProperties": true
   }
  }
 }
}
```
