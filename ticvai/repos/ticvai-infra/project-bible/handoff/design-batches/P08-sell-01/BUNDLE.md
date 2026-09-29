# P08-sell-01 — P08 · Sell (1 of 4)

**10 screens · 85 operations · 78 schemas · 10 permissions**

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
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-007` | Product Directory | listDetail | 14 | 7 | — |
| `BO-009` | Pricing Rules | listDetail | 11 | 4 | — |
| `BO-010` | Promotions & Coupons | listDetail | 24 | 10 | — |
| `BO-011` | Packages & Bundles | listDetail | 10 | 4 | — |
| `BO-012` | Membership Products | listDetail | 12 | 6 | — |
| `BO-013` | Channel & Distribution | listDetail | 10 | 6 | — |
| `BO-014` | Catalogue Publishing | listDetail | 13 | 7 | — |
| `BO-015` | Performance Calendar | listDetail | 11 | 6 | — |
| `BO-016` | Performance Template | listDetail | 2 | 1 | — |
| `BO-017` | Capacity Management | listDetail | 8 | 4 | — |

## Thin screens in this batch

**BO-016 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

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
     "to": "BO-112",
     "trigger": "Production Planning & Production Sheets",
     "provenance": "flow F78 step 2→3"
    },
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "carries": [
      "productId",
      "variantId"
     ],
     "provenance": "derived — BO-008 declares entryState.params productId, variantId, version and BO-007 holds productId, variantId, so an edge into it carries them"
    },
    {
     "to": "BO-009",
     "trigger": "Pricing Rules",
     "provenance": "derived — BO-009 declares entryState.params priceListId, ruleId and BO-007 holds none of them, so the edge carries nothing and BO-009 opens cold"
    },
    {
     "to": "BO-010",
     "trigger": "Promotions & Coupons",
     "carries": [
      "code"
     ],
     "provenance": "derived — BO-010 declares entryState.params campaignId, code, dashboardId, promotionId, reportId, voucherId and BO-007 holds code, so an edge into it carries them"
    },
    {
     "to": "BO-045",
     "trigger": "Menu Management",
     "provenance": "flow F85 step 4→5",
     "carries": [
      "menuId"
     ]
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
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Venue id",
       "operation": "listProducts",
       "notes": "Sends `?venueId=` to `listProducts`.",
       "provenance": "contract catalogue.yaml GET /products"
      },
      {
       "kind": "textField",
       "label": "Kind",
       "operation": "listProducts",
       "notes": "Sends `?kind=` to `listProducts`.",
       "provenance": "contract catalogue.yaml GET /products"
      },
      {
       "kind": "toggle",
       "label": "Is sellable",
       "operation": "listProducts",
       "notes": "Sends `?isSellable=` to `listProducts`.",
       "provenance": "contract catalogue.yaml GET /products"
      },
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
      },
      {
       "kind": "dataTable",
       "label": "Every alternative code",
       "bindsTo": "AlternativeCode",
       "columns": [
        "AlternativeCode.code",
        "AlternativeCode.partnerId",
        "AlternativeCode.partnerName",
        "AlternativeCode.variantId",
        "AlternativeCode.note"
       ],
       "operation": "listAlternativeCodes",
       "provenance": "contract catalogue.yaml GET /products/{productId}/alternative-codes"
      },
      {
       "kind": "dataTable",
       "label": "Every product variant",
       "bindsTo": "ProductVariant",
       "columns": [
        "ProductVariant.id",
        "ProductVariant.productId",
        "ProductVariant.sku",
        "ProductVariant.axisValues",
        "ProductVariant.name",
        "ProductVariant.barcode",
        "ProductVariant.isDefault",
        "ProductVariant.isActive"
       ],
       "operation": "listProductVariants",
       "provenance": "contract catalogue.yaml GET /products/{productId}/variants"
      },
      {
       "kind": "dataTable",
       "label": "Every menu",
       "bindsTo": "Menu",
       "columns": [
        "Menu.id",
        "Menu.code",
        "Menu.name",
        "Menu.outletId",
        "Menu.availability",
        "Menu.sections",
        "Menu.isActive",
        "Menu.publishedVersion",
        "Menu.publishedAt"
       ],
       "operation": "listMenus",
       "provenance": "contract fnb.yaml GET /menus"
      },
      {
       "kind": "dataTable",
       "label": "Every merchandise",
       "bindsTo": "MerchandiseItem",
       "columns": [
        "MerchandiseItem.description",
        "MerchandiseItem.id",
        "MerchandiseItem.sku",
        "MerchandiseItem.barcode",
        "MerchandiseItem.name",
        "MerchandiseItem.outletId",
        "MerchandiseItem.categoryId",
        "MerchandiseItem.variantId",
        "MerchandiseItem.inventoryItemId",
        "MerchandiseItem.price",
        "MerchandiseItem.onHand",
        "MerchandiseItem.isReturnable"
       ],
       "operation": "listMerchandise",
       "provenance": "contract retail.yaml GET /merchandise"
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
       "label": "Create product",
       "operation": "createProduct",
       "provenance": "contract catalogue.yaml POST /products"
      },
      {
       "kind": "secondaryButton",
       "label": "Resolve product by code",
       "operation": "resolveProductByCode",
       "provenance": "contract catalogue.yaml GET /products/resolve"
      },
      {
       "kind": "secondaryButton",
       "label": "Save alternative codes",
       "operation": "setAlternativeCodes",
       "provenance": "contract catalogue.yaml PUT /products/{productId}/alternative-codes"
      },
      {
       "kind": "secondaryButton",
       "label": "Save product attributes",
       "operation": "setProductAttributes",
       "provenance": "contract catalogue.yaml PUT /products/{productId}/attributes"
      },
      {
       "kind": "secondaryButton",
       "label": "Transition product lifecycle",
       "operation": "transitionProductLifecycle",
       "notes": "**Approve and publish are guarded separately** (decided 28 September, audit R091 (2)): the Approve transition (review to approved) is offered only to a holder of `PRODUCT_APPROVE`, and Publish (approved to live) only to a holder of `PRODUCT_PUBLISH`; the server refuses the other with 403 transition-permission-required.",
       "provenance": "contract catalogue.yaml POST /products/{productId}/lifecycle"
      },
      {
       "kind": "secondaryButton",
       "label": "Save product",
       "operation": "updateProduct",
       "provenance": "contract catalogue.yaml PATCH /products/{productId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Create merchandise",
       "operation": "createMerchandise",
       "provenance": "contract retail.yaml POST /merchandise"
      },
      {
       "kind": "secondaryButton",
       "label": "Bulk update products",
       "operation": "bulkUpdateProducts",
       "provenance": "contract inventory.yaml POST /products/bulk"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The product list.",
   "error": "Could not load. Names which read failed and leaves the product untouched.",
   "emptyFirstRun": "No product yet. Offers Create product (`createProduct`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on venueId, kind, isSellable and the product are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `PRODUCT_VIEW`, which `listProducts` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
    "trigger": "onAction"
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
    "trigger": "onAction"
   },
   {
    "operationId": "listProductVariants",
    "contract": "catalogue",
    "purpose": "List generated variants",
    "trigger": "onAction"
   },
   {
    "operationId": "resolveProductByCode",
    "contract": "catalogue",
    "purpose": "Resolve a partner code to a product",
    "trigger": "onAction"
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
   "derivedFrom": "wireframes/reference/Retail Board 2.dc.html",
   "source": "Claude Design Retail pack, 24 August",
   "note": "**Drawn by Claude Design on `Retail Board 2.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 14 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formCreateProduct",
    "component": "modal",
    "trigger": "Create product",
    "body": "**Collects what `createProduct` sends before it is called.** Required: `code`, `name`, `kind`, `venueId`. Optional: `description`, `channels`, `entitlementTemplateId`, `dataMaskValues`, `guestListing` and `notBookableLabel` (REV3-14), `displayTags` (23SEP-3), `media` (23SEP-4), `consentQuestionIds` (REV3-26), `requiresTimeWindow` (REV3-13), all decided 29 September, rev 3. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateProductRequest",
    "confirm": {
     "label": "Create product",
     "operation": "createProduct"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "code",
      "name",
      "kind",
      "venueId",
      "description",
      "channels",
      "entitlementTemplateId",
      "dataMaskValues",
      "guestListing",
      "notBookableLabel",
      "displayTags",
      "media",
      "consentQuestionIds",
      "requiresTimeWindow"
     ]
    },
    "provenance": "contract catalogue.yaml POST /products"
   },
   {
    "id": "formSetAlternativeCodes",
    "component": "modal",
    "trigger": "Save alternative codes",
    "body": "**Collects what `setAlternativeCodes` sends before it is called.** Required: `codes`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save alternative codes",
     "operation": "setAlternativeCodes"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "codes"
     ]
    },
    "provenance": "contract catalogue.yaml PUT /products/{productId}/alternative-codes"
   },
   {
    "id": "formSetProductAttributes",
    "component": "modal",
    "trigger": "Save product attributes",
    "body": "**Collects what `setProductAttributes` sends before it is called.** Required: `axes`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save product attributes",
     "operation": "setProductAttributes"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "axes"
     ]
    },
    "provenance": "contract catalogue.yaml PUT /products/{productId}/attributes"
   },
   {
    "id": "formTransitionProductLifecycle",
    "component": "modal",
    "trigger": "Transition product lifecycle",
    "body": "**Collects what `transitionProductLifecycle` sends before it is called.** Required: `transition`, `reason`. Optional: `effectiveAt`. The transition picker lists only what the principal may do — approve needs `PRODUCT_APPROVE`, publish needs `PRODUCT_PUBLISH` (decided 28 September, audit R091 (2)). Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Transition product lifecycle",
     "operation": "transitionProductLifecycle"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "transition",
      "reason",
      "effectiveAt"
     ]
    },
    "provenance": "contract catalogue.yaml POST /products/{productId}/lifecycle"
   },
   {
    "id": "formUpdateProduct",
    "component": "modal",
    "trigger": "Save product",
    "body": "**Collects what `updateProduct` sends before it is called.** Nothing in the body is required. Optional: `name`, `description`, `channels`, `dataMaskValues`, `guestListing`, `notBookableLabel`, `displayTags`, `media`, `consentQuestionIds`, `requiresTimeWindow` (decided 29 September, rev 3 REV3-14, 23SEP-3, 23SEP-4, REV3-26, REV3-13). Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "UpdateProductRequest",
    "confirm": {
     "label": "Save product",
     "operation": "updateProduct"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "name",
      "description",
      "channels",
      "dataMaskValues",
      "guestListing",
      "notBookableLabel",
      "displayTags",
      "media",
      "consentQuestionIds",
      "requiresTimeWindow"
     ]
    },
    "provenance": "contract catalogue.yaml PATCH /products/{productId}"
   },
   {
    "id": "formCreateMerchandise",
    "component": "modal",
    "trigger": "Create merchandise",
    "body": "**Collects what `createMerchandise` sends before it is called.** Required: `sku`, `name`, `outletId`, `variantId`. Optional: `barcode`, `description`, `categoryId`, `inventoryItemId`, `isReturnable`, `returnWindowDays`, `requiresSerialNumber`, `imageAssetRef`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateMerchandiseRequest",
    "confirm": {
     "label": "Create merchandise",
     "operation": "createMerchandise"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "sku",
      "name",
      "outletId",
      "variantId",
      "barcode",
      "description",
      "categoryId",
      "inventoryItemId",
      "isReturnable",
      "returnWindowDays",
      "requiresSerialNumber",
      "imageAssetRef"
     ]
    },
    "provenance": "contract retail.yaml POST /merchandise"
   },
   {
    "id": "formBulkUpdateProducts",
    "component": "modal",
    "trigger": "Bulk update products",
    "body": "**Collects what `bulkUpdateProducts` sends before it is called.** Required: `selector`, `changes`. Optional: `previewOnly`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Bulk update products",
     "operation": "bulkUpdateProducts"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "selector",
      "changes",
      "previewOnly"
     ]
    },
    "provenance": "contract inventory.yaml POST /products/bulk"
   }
  ],
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
    "BO-007",
    "BO-010",
    "BO-014"
   ],
   "inferred": true,
   "entryFrom": [
    "BO-102",
    "BO-112"
   ],
   "transitions": [
    {
     "to": "BO-007",
     "trigger": "Product Directory",
     "carries": [
      "productId"
     ],
     "provenance": "derived — BO-007 declares entryState.params productId and BO-009 holds productId, so an edge into it carries them"
    },
    {
     "to": "BO-010",
     "trigger": "Promotions & Coupons",
     "carries": [
      "code"
     ],
     "provenance": "derived — BO-010 declares entryState.params campaignId, code, dashboardId, promotionId, reportId, voucherId and BO-009 holds code, so an edge into it carries them"
    },
    {
     "to": "BO-014",
     "trigger": "The priced range is published to the tills",
     "provenance": "flow F78 step 3→4",
     "carries": [
      "priceListId",
      "productId"
     ]
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
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Channel",
       "operation": "listPriceLists",
       "notes": "Sends `?channel=` to `listPriceLists`.",
       "provenance": "contract catalogue.yaml GET /price-lists"
      },
      {
       "kind": "dataTable",
       "label": "Every price list",
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
      },
      {
       "kind": "dataTable",
       "label": "Every price",
       "bindsTo": "Price",
       "columns": [
        "Price.id",
        "Price.priceListId",
        "Price.variantId",
        "Price.amount",
        "Price.taxCodeId"
       ],
       "operation": "listPrices",
       "provenance": "contract catalogue.yaml GET /price-lists/{priceListId}/prices"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected price list",
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
       "label": "Create price list",
       "operation": "createPriceList",
       "provenance": "contract catalogue.yaml POST /price-lists"
      },
      {
       "kind": "secondaryButton",
       "label": "Copy price list",
       "operation": "copyPriceList",
       "provenance": "contract catalogue.yaml POST /price-lists/{priceListId}/copy"
      },
      {
       "kind": "secondaryButton",
       "label": "Save prices",
       "operation": "setPrices",
       "provenance": "contract catalogue.yaml PUT /price-lists/{priceListId}/prices"
      },
      {
       "kind": "secondaryButton",
       "label": "Save price list",
       "operation": "updatePriceList",
       "provenance": "contract catalogue.yaml PATCH /price-lists/{priceListId}"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The pricing rules list.",
   "error": "Could not load. Names which read failed and leaves the pricing rules untouched.",
   "emptyFirstRun": "No pricing rules yet. Offers Create price list (`createPriceList`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on channel and the pricing rules are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `PRICE_VIEW`, which `listPriceLists` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
    "trigger": "onAction"
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
    "trigger": "onAction"
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
   },
   {
    "operationId": "bulkChangePrices",
    "contract": "catalogue",
    "purpose": "Reprice a category or a whole catalogue",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listPriceLists",
     "listPrices",
     "getPriceList"
    ]
   },
   {
    "operationId": "listDynamicPriceRules",
    "contract": "catalogue",
    "purpose": "Dynamic price rules",
    "trigger": "onLoad",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   },
   {
    "operationId": "getDynamicPriceRule",
    "contract": "catalogue",
    "purpose": "One dynamic rule with its conditions and actions",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   },
   {
    "operationId": "setDynamicPriceRule",
    "contract": "catalogue",
    "purpose": "Replace a rule, its conditions and its actions",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listPriceLists",
     "listPrices",
     "getPriceList",
     "listDynamicPriceRules"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "priceListId",
     "from": "deepLink"
    },
    {
     "name": "ruleId",
     "from": "navigation"
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
   "derivedFrom": "wireframes/reference/Retail Board 2.dc.html",
   "source": "Claude Design Retail pack, 24 August",
   "note": "**Drawn by Claude Design on `Retail Board 2.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 7 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formCreatePriceList",
    "component": "modal",
    "trigger": "Create price list",
    "body": "**Collects what `createPriceList` sends before it is called.** Required: `code`, `name`, `venueId`, `channels`. Optional: `validFrom`, `validTo`, `priority`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreatePriceListRequest",
    "confirm": {
     "label": "Create price list",
     "operation": "createPriceList"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "code",
      "name",
      "venueId",
      "channels",
      "validFrom",
      "validTo",
      "priority"
     ]
    },
    "provenance": "contract catalogue.yaml POST /price-lists"
   },
   {
    "id": "formCopyPriceList",
    "component": "modal",
    "trigger": "Copy price list",
    "body": "**Collects what `copyPriceList` sends before it is called.** Required: `code`, `name`. Optional: `adjustmentPercent`, `roundTo`, `validFrom`, `validTo`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Copy price list",
     "operation": "copyPriceList"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "code",
      "name",
      "adjustmentPercent",
      "roundTo",
      "validFrom",
      "validTo"
     ]
    },
    "provenance": "contract catalogue.yaml POST /price-lists/{priceListId}/copy"
   },
   {
    "id": "formSetPrices",
    "component": "modal",
    "trigger": "Save prices",
    "body": "**Collects what `setPrices` sends before it is called.** Required: `prices`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save prices",
     "operation": "setPrices"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "prices"
     ]
    },
    "provenance": "contract catalogue.yaml PUT /price-lists/{priceListId}/prices"
   },
   {
    "id": "formUpdatePriceList",
    "component": "modal",
    "trigger": "Save price list",
    "body": "**Collects what `updatePriceList` sends before it is called.** Nothing in the body is required. Optional: `name`, `validFrom`, `validTo`, `priority`, `isActive`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save price list",
     "operation": "updatePriceList"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "name",
      "validFrom",
      "validTo",
      "priority",
      "isActive"
     ]
    },
    "provenance": "contract catalogue.yaml PATCH /price-lists/{priceListId}"
   }
  ],
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
    "BO-007",
    "BO-009"
   ],
   "inferred": true,
   "entryFrom": [
    "BO-102",
    "BO-119"
   ],
   "transitions": [
    {
     "to": "BO-007",
     "trigger": "Product Directory",
     "provenance": "derived — BO-007 declares entryState.params productId and BO-010 holds none of them, so the edge carries nothing and BO-007 opens cold"
    },
    {
     "to": "BO-009",
     "trigger": "Pricing Rules",
     "provenance": "derived — BO-009 declares entryState.params priceListId, ruleId and BO-010 holds none of them, so the edge carries nothing and BO-009 opens cold"
    },
    {
     "to": "ANL-009",
     "trigger": "AI Assistant & Action Center",
     "provenance": "flow F90 step 2→3",
     "crossesDevice": true,
     "back": false,
     "carries": [
      "reportId"
     ]
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
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Venue id",
       "operation": "listPromotions",
       "notes": "Sends `?venueId=` to `listPromotions`.",
       "provenance": "contract promotions.yaml GET /promotions"
      },
      {
       "kind": "textField",
       "label": "Status",
       "operation": "listPromotions",
       "notes": "Sends `?status=` to `listPromotions`.",
       "provenance": "contract promotions.yaml GET /promotions"
      },
      {
       "kind": "datePicker",
       "label": "Active at",
       "operation": "listPromotions",
       "notes": "Sends `?activeAt=` to `listPromotions`.",
       "provenance": "contract promotions.yaml GET /promotions"
      },
      {
       "kind": "dataTable",
       "label": "Every promotion",
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
      },
      {
       "kind": "dataTable",
       "label": "Every coupon campaign",
       "bindsTo": "CouponCampaign",
       "columns": [
        "CouponCampaign.code",
        "CouponCampaign.name",
        "CouponCampaign.venueId",
        "CouponCampaign.discount",
        "CouponCampaign.conditions",
        "CouponCampaign.isSingleUse",
        "CouponCampaign.maxRedemptionsPerCode",
        "CouponCampaign.validFrom",
        "CouponCampaign.validTo",
        "CouponCampaign.id",
        "CouponCampaign.generatedCount",
        "CouponCampaign.redeemedCount"
       ],
       "operation": "listCouponCampaigns",
       "provenance": "contract promotions.yaml GET /coupon-campaigns"
      },
      {
       "kind": "dataTable",
       "label": "Every coupon code",
       "bindsTo": "CouponCode",
       "columns": [
        "CouponCode.code",
        "CouponCode.campaignId",
        "CouponCode.batchId",
        "CouponCode.status",
        "CouponCode.assignedSubjectId",
        "CouponCode.redemptionCount",
        "CouponCode.maxRedemptions",
        "CouponCode.discount",
        "CouponCode.invalidReason",
        "CouponCode.validFrom",
        "CouponCode.validTo",
        "CouponCode.redeemedAt"
       ],
       "operation": "listCouponCodes",
       "provenance": "contract promotions.yaml GET /coupon-campaigns/{campaignId}/codes"
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
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected promotion",
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
      },
      {
       "kind": "detailPanel",
       "label": "The promotion usage",
       "bindsTo": "PromotionUsage",
       "columns": [
        "PromotionUsage.promotionId",
        "PromotionUsage.redemptionCount",
        "PromotionUsage.discountGiven",
        "PromotionUsage.budgetCap",
        "PromotionUsage.budgetRemaining",
        "PromotionUsage.isBudgetExhausted",
        "PromotionUsage.byChannel"
       ],
       "operation": "getPromotionUsage",
       "provenance": "contract promotions.yaml GET /promotions/{promotionId}/usage"
      },
      {
       "kind": "detailPanel",
       "label": "The dashboard data",
       "bindsTo": "DashboardData",
       "columns": [
        "DashboardData.tileData"
       ],
       "operation": "getDashboard",
       "provenance": "contract reporting.yaml GET /dashboards/{dashboardId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Analyse promotion conflicts",
       "operation": "analysePromotionConflicts",
       "provenance": "contract promotions.yaml GET /promotions/{promotionId}/conflicts"
      },
      {
       "kind": "secondaryButton",
       "label": "Create coupon campaign",
       "operation": "createCouponCampaign",
       "provenance": "contract promotions.yaml POST /coupon-campaigns"
      },
      {
       "kind": "secondaryButton",
       "label": "Create promotion",
       "operation": "createPromotion",
       "provenance": "contract promotions.yaml POST /promotions"
      },
      {
       "kind": "secondaryButton",
       "label": "End promotion",
       "operation": "endPromotion",
       "provenance": "contract promotions.yaml POST /promotions/{promotionId}/end"
      },
      {
       "kind": "secondaryButton",
       "label": "Evaluate promotions",
       "operation": "evaluatePromotions",
       "provenance": "contract promotions.yaml POST /promotions/evaluate"
      },
      {
       "kind": "secondaryButton",
       "label": "Generate coupon codes",
       "operation": "generateCouponCodes",
       "provenance": "contract promotions.yaml POST /coupon-campaigns/{campaignId}/codes"
      },
      {
       "kind": "secondaryButton",
       "label": "Pause promotion",
       "operation": "pausePromotion",
       "provenance": "contract promotions.yaml POST /promotions/{promotionId}/pause"
      },
      {
       "kind": "secondaryButton",
       "label": "Publish promotion",
       "operation": "publishPromotion",
       "provenance": "contract promotions.yaml POST /promotions/{promotionId}/publish"
      },
      {
       "kind": "secondaryButton",
       "label": "Unschedule promotion",
       "operation": "unschedulePromotion",
       "provenance": "contract promotions.yaml POST /promotions/{promotionId}/unschedule"
      },
      {
       "kind": "secondaryButton",
       "label": "Save promotion",
       "operation": "updatePromotion",
       "provenance": "contract promotions.yaml PATCH /promotions/{promotionId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Simulate promotion",
       "operation": "simulatePromotion",
       "provenance": "contract promotions.yaml POST /promotions/{promotionId}/simulate"
      },
      {
       "kind": "secondaryButton",
       "label": "Run report",
       "operation": "runReport",
       "provenance": "contract reporting.yaml POST /reports/{reportId}/run"
      },
      {
       "kind": "destructiveButton",
       "label": "Void coupon code",
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
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmVoidCouponCode",
    "component": "confirmDialog",
    "trigger": "Void coupon code",
    "body": "**Names what `voidCouponCode` changes and what it leaves alone**, in the consequence rather than the verb. A promotions coupons this affects should be identified in the dialog, not just counted. **Collects what `voidCouponCode` sends before it is called.** Required: `reason`.",
    "provenance": "contract promotions.yaml POST /coupon-codes/{code}/void"
   },
   {
    "id": "formCreateCouponCampaign",
    "component": "modal",
    "trigger": "Create coupon campaign",
    "body": "**Collects what `createCouponCampaign` sends before it is called.** Required: `code`, `name`, `venueId`, `discount`, `validFrom`. Optional: `conditions`, `isSingleUse`, `maxRedemptionsPerCode`, `validTo`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateCouponCampaignRequest",
    "confirm": {
     "label": "Create coupon campaign",
     "operation": "createCouponCampaign"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "code",
      "name",
      "venueId",
      "discount",
      "validFrom",
      "conditions",
      "isSingleUse",
      "maxRedemptionsPerCode",
      "validTo"
     ]
    },
    "provenance": "contract promotions.yaml POST /coupon-campaigns"
   },
   {
    "id": "formCreatePromotion",
    "component": "modal",
    "trigger": "Create promotion",
    "body": "**Collects what `createPromotion` sends before it is called.** Required: `code`, `name`, `venueId`, `discount`, `validFrom`. Optional: `description`, `conditions`, `stackingMode`, `stackingGroup`, `precedence`, `validTo`, `maxRedemptions`, `maxRedemptionsPerGuest`, `budgetCap`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreatePromotionRequest",
    "confirm": {
     "label": "Create promotion",
     "operation": "createPromotion"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "code",
      "name",
      "venueId",
      "discount",
      "validFrom",
      "description",
      "conditions",
      "stackingMode",
      "stackingGroup",
      "precedence",
      "validTo",
      "maxRedemptions",
      "maxRedemptionsPerGuest",
      "budgetCap"
     ]
    },
    "provenance": "contract promotions.yaml POST /promotions"
   },
   {
    "id": "formEndPromotion",
    "component": "modal",
    "trigger": "End promotion",
    "body": "**Collects what `endPromotion` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "End promotion",
     "operation": "endPromotion"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "reason"
     ]
    },
    "provenance": "contract promotions.yaml POST /promotions/{promotionId}/end"
   },
   {
    "id": "formEvaluatePromotions",
    "component": "modal",
    "trigger": "Evaluate promotions",
    "body": "**Collects what `evaluatePromotions` sends before it is called.** Required: `venueId`, `channel`, `lines`. Optional: `subjectId`, `membershipTierId`, `couponCodes`, `evaluateAt`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "EvaluatePromotionsRequest",
    "confirm": {
     "label": "Evaluate promotions",
     "operation": "evaluatePromotions"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "venueId",
      "channel",
      "lines",
      "subjectId",
      "membershipTierId",
      "couponCodes",
      "evaluateAt"
     ]
    },
    "provenance": "contract promotions.yaml POST /promotions/evaluate"
   },
   {
    "id": "formGenerateCouponCodes",
    "component": "modal",
    "trigger": "Generate coupon codes",
    "body": "**Collects what `generateCouponCodes` sends before it is called.** Required: `quantity`. Optional: `prefix`, `length`, `assignToSubjectIds`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Generate coupon codes",
     "operation": "generateCouponCodes"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "quantity",
      "prefix",
      "length",
      "assignToSubjectIds"
     ]
    },
    "provenance": "contract promotions.yaml POST /coupon-campaigns/{campaignId}/codes"
   },
   {
    "id": "formPausePromotion",
    "component": "modal",
    "trigger": "Pause promotion",
    "body": "**Collects what `pausePromotion` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Pause promotion",
     "operation": "pausePromotion"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "reason"
     ]
    },
    "provenance": "contract promotions.yaml POST /promotions/{promotionId}/pause"
   },
   {
    "id": "formUpdatePromotion",
    "component": "modal",
    "trigger": "Save promotion",
    "body": "**Collects what `updatePromotion` sends before it is called.** Nothing in the body is required. Optional: `name`, `validTo`, `isPaused`, `conditions`, `discount`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save promotion",
     "operation": "updatePromotion"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "name",
      "validTo",
      "isPaused",
      "conditions",
      "discount"
     ]
    },
    "provenance": "contract promotions.yaml PATCH /promotions/{promotionId}"
   },
   {
    "id": "formSimulatePromotion",
    "component": "modal",
    "trigger": "Simulate promotion",
    "body": "**Collects what `simulatePromotion` sends before it is called.** Required: `periodFrom`, `periodTo`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Simulate promotion",
     "operation": "simulatePromotion"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "periodFrom",
      "periodTo"
     ]
    },
    "provenance": "contract promotions.yaml POST /promotions/{promotionId}/simulate"
   },
   {
    "id": "formRunReport",
    "component": "modal",
    "trigger": "Run report",
    "body": "**Collects what `runReport` sends before it is called.** Nothing in the body is required. Optional: `parameters`, `venueId`, `dateFrom`, `dateTo`, `forceAsync`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "RunReportRequest",
    "confirm": {
     "label": "Run report",
     "operation": "runReport"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "parameters",
      "venueId",
      "dateFrom",
      "dateTo",
      "forceAsync"
     ]
    },
    "provenance": "contract reporting.yaml POST /reports/{reportId}/run"
   }
  ],
  "states": {
   "loading": "The promotions coupons list.",
   "error": "Could not load. Names which read failed and leaves the promotions coupons untouched.",
   "emptyFirstRun": "No promotions coupons yet. Offers Create coupon campaign (`createCouponCampaign`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on venueId, status, activeAt and the promotions coupons are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `PRICE_VIEW`, which `listPromotions` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
    "trigger": "onAction"
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
    "trigger": "onAction"
   },
   {
    "operationId": "getPromotionUsage",
    "contract": "promotions",
    "purpose": "Redemption count and discount given",
    "trigger": "onAction"
   },
   {
    "operationId": "listCouponCodes",
    "contract": "promotions",
    "purpose": "List generated codes",
    "trigger": "onAction"
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
   },
   {
    "operationId": "setPromotionVariants",
    "contract": "promotions",
    "purpose": "A/B test two versions of a promotion",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listPromotions",
     "listCouponCampaigns",
     "analysePromotionConflicts",
     "getPromotion"
    ]
   },
   {
    "operationId": "assignCoupon",
    "contract": "promotions",
    "purpose": "Assign a coupon code to a named guest",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listPromotions",
     "listCouponCampaigns",
     "analysePromotionConflicts",
     "getPromotion"
    ]
   },
   {
    "operationId": "listVoucherBatches",
    "contract": "promotions",
    "purpose": "Voucher batches issued",
    "trigger": "onLoad",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   },
   {
    "operationId": "createVoucherBatch",
    "contract": "promotions",
    "purpose": "Issue a voucher batch",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listPromotions",
     "listCouponCampaigns",
     "analysePromotionConflicts",
     "getPromotion"
    ]
   },
   {
    "operationId": "voidVoucher",
    "contract": "promotions",
    "purpose": "Cancel a voucher",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listPromotions",
     "listCouponCampaigns",
     "analysePromotionConflicts",
     "getPromotion"
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
    },
    {
     "name": "voucherId",
     "from": "navigation"
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
   "derivedFrom": "wireframes/reference/POS Board 4.dc.html",
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
     "to": "BO-007",
     "trigger": "Product Directory",
     "carries": [
      "productId"
     ],
     "provenance": "derived — BO-007 declares entryState.params productId and BO-011 holds productId, so an edge into it carries them"
    },
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "carries": [
      "productId",
      "version"
     ],
     "provenance": "derived — BO-008 declares entryState.params productId, variantId, version and BO-011 holds productId, version, so an edge into it carries them"
    },
    {
     "to": "BO-009",
     "trigger": "Pricing Rules",
     "provenance": "derived — BO-009 declares entryState.params priceListId, ruleId and BO-011 holds none of them, so the edge carries nothing and BO-009 opens cold"
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
       "label": "Every bundle",
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
      },
      {
       "kind": "publishGate",
       "impliedBy": "publishBundle",
       "notes": "Declares `publishBundle`. **The gate names what the publish will affect before it happens** — a disabled Publish with no reason is the state operators escalate.\n",
       "provenance": "carried from the previous definition"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected bundle",
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
      },
      {
       "kind": "detailPanel",
       "label": "The group package definition",
       "bindsTo": "GroupPackageDefinition",
       "columns": [
        "GroupPackageDefinition.id",
        "GroupPackageDefinition.productId",
        "GroupPackageDefinition.kind",
        "GroupPackageDefinition.maxParticipants",
        "GroupPackageDefinition.durationMinutes",
        "GroupPackageDefinition.hostCount",
        "GroupPackageDefinition.pricingBasis",
        "GroupPackageDefinition.freeLeaderRatio",
        "GroupPackageDefinition.paymentMode",
        "GroupPackageDefinition.includes",
        "GroupPackageDefinition.scopePath"
       ],
       "operation": "getGroupPackageDefinition",
       "provenance": "contract catalogue.yaml GET /products/{productId}/group-package"
      },
      {
       "kind": "detailPanel",
       "label": "The catalogue bundle",
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
       "label": "Publish bundle",
       "operation": "publishBundle",
       "provenance": "contract catalogue.yaml POST /catalogue/bundles"
      },
      {
       "kind": "secondaryButton",
       "label": "Report bundle applied",
       "operation": "reportBundleApplied",
       "provenance": "contract catalogue.yaml POST /catalogue/bundles/{version}/applied"
      },
      {
       "kind": "secondaryButton",
       "label": "Create bundle",
       "operation": "createBundle",
       "provenance": "contract promotions.yaml POST /bundles"
      },
      {
       "kind": "publishGate",
       "label": "What publishing changes",
       "notes": "**Names what goes live, where, and from when.** A publish with no stated consequence is one somebody presses meaning to save.",
       "provenance": "authored — required by check-screens"
      },
      {
       "kind": "secondaryButton",
       "label": "Save group package definition",
       "operation": "setGroupPackageDefinition",
       "provenance": "contract catalogue.yaml PUT /products/{productId}/group-package"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The packages bundles list.",
   "error": "Could not load. Names which read failed and leaves the packages bundles untouched.",
   "emptyFirstRun": "No packages bundles yet. Offers Create bundle (`createBundle`).",
   "emptyNoResults": "Never shown: `listCatalogueBundles` takes no filter, so an empty list is always the first-run state above.",
   "emptyNoAccess": "Shown when the caller lacks `PRODUCT_VIEW`, which `getGroupPackageDefinition` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getGroupPackageDefinition",
    "contract": "catalogue",
    "purpose": "A school-trip format or party package",
    "trigger": "onAction"
   },
   {
    "operationId": "setGroupPackageDefinition",
    "contract": "catalogue",
    "purpose": "Define a school-trip format or party package",
    "trigger": "onAction"
   },
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
   },
   {
    "operationId": "createCombo",
    "contract": "fnb",
    "purpose": "Create a meal deal priced as one thing",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   },
   {
    "operationId": "setComboSlots",
    "contract": "fnb",
    "purpose": "Set what the guest chooses in a combo and what it costs extra",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   },
   {
    "operationId": "updateBundle",
    "contract": "promotions",
    "purpose": "Amend a bundle",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "version",
     "from": "deepLink"
    },
    {
     "name": "productId",
     "from": "navigation"
    },
    {
     "name": "bundleId",
     "from": "navigation"
    },
    {
     "name": "comboId",
     "from": "navigation"
    }
   ],
   "coldEntry": "**A version link is expected to point at something superseded — that is what versions are for.** The screen opens the requested version read-only, says it is not current, and links to the one that is. **An old version is history, not an error.** Arrives with `version`.",
   "preloaded": [
    "BundleSummary.venueId",
    "BundleSummary.publishedAt",
    "BundleSummary.publishedBy",
    "BundleSummary.contentHash",
    "BundleSummary.signatureKeyId"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-011",
   "derivedFrom": "wireframes/reference/Retail Board 5.dc.html",
   "source": "Claude Design Retail pack, 24 August",
   "note": "**Drawn by Claude Design on `Retail Board 5.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 5 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formSetGroupPackageDefinition",
    "component": "modal",
    "trigger": "Save group package definition",
    "body": "**Collects what `setGroupPackageDefinition` sends before it is called.** Required: `kind`, `maxParticipants`, `durationMinutes`. Optional: `id`, `productId`, `hostCount`, `pricingBasis`, `freeLeaderRatio`, `paymentMode`, `includes`, `scopePath`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "GroupPackageDefinition",
    "confirm": {
     "label": "Save group package definition",
     "operation": "setGroupPackageDefinition"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "kind",
      "maxParticipants",
      "durationMinutes",
      "id",
      "productId",
      "hostCount",
      "pricingBasis",
      "freeLeaderRatio",
      "paymentMode",
      "includes",
      "scopePath"
     ]
    },
    "provenance": "contract catalogue.yaml PUT /products/{productId}/group-package"
   },
   {
    "id": "formPublishBundle",
    "component": "modal",
    "trigger": "Publish bundle",
    "body": "**Collects what `publishBundle` sends before it is called.** Required: `venueId`. Optional: `note`, `staleAfterHours`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Publish bundle",
     "operation": "publishBundle"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "venueId",
      "note",
      "staleAfterHours"
     ]
    },
    "provenance": "contract catalogue.yaml POST /catalogue/bundles"
   },
   {
    "id": "formReportBundleApplied",
    "component": "modal",
    "trigger": "Report bundle applied",
    "body": "**Collects what `reportBundleApplied` sends before it is called.** Required: `appliedAt`, `outcome`. Optional: `error`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Report bundle applied",
     "operation": "reportBundleApplied"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "appliedAt",
      "outcome",
      "error"
     ]
    },
    "provenance": "contract catalogue.yaml POST /catalogue/bundles/{version}/applied"
   },
   {
    "id": "formCreateBundle",
    "component": "modal",
    "trigger": "Create bundle",
    "body": "**Collects what `createBundle` sends before it is called.** Required: `code`, `name`, `venueId`, `kind`, `price`, `components`, `allocation`. Optional: `description`, `choiceGroups`, `validFrom`, `validTo`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateBundleRequest",
    "confirm": {
     "label": "Create bundle",
     "operation": "createBundle"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "code",
      "name",
      "venueId",
      "kind",
      "price",
      "components",
      "allocation",
      "description",
      "choiceGroups",
      "validFrom",
      "validTo"
     ]
    },
    "provenance": "contract promotions.yaml POST /bundles"
   }
  ],
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
     "to": "BO-007",
     "trigger": "Product Directory",
     "carries": [
      "productId"
     ],
     "provenance": "derived — BO-007 declares entryState.params productId and BO-012 holds productId, so an edge into it carries them"
    },
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "carries": [
      "productId",
      "variantId"
     ],
     "provenance": "derived — BO-008 declares entryState.params productId, variantId, version and BO-012 holds productId, variantId, so an edge into it carries them"
    },
    {
     "to": "BO-009",
     "trigger": "Pricing Rules",
     "provenance": "derived — BO-009 declares entryState.params priceListId, ruleId and BO-012 holds none of them, so the edge carries nothing and BO-009 opens cold"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listProducts` reads the population and `getProduct` reads one of them — list, select, act",
  "purpose": "Define what a membership includes.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Venue id",
       "operation": "listProducts",
       "notes": "Sends `?venueId=` to `listProducts`.",
       "provenance": "contract catalogue.yaml GET /products"
      },
      {
       "kind": "textField",
       "label": "Kind",
       "operation": "listProducts",
       "notes": "Sends `?kind=` to `listProducts`.",
       "provenance": "contract catalogue.yaml GET /products"
      },
      {
       "kind": "toggle",
       "label": "Is sellable",
       "operation": "listProducts",
       "notes": "Sends `?isSellable=` to `listProducts`.",
       "provenance": "contract catalogue.yaml GET /products"
      },
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
      },
      {
       "kind": "dataTable",
       "label": "Every entitlement template",
       "bindsTo": "EntitlementTemplate",
       "columns": [
        "EntitlementTemplate.description",
        "EntitlementTemplate.id",
        "EntitlementTemplate.code",
        "EntitlementTemplate.name",
        "EntitlementTemplate.validityKind",
        "EntitlementTemplate.validFromOffsetDays",
        "EntitlementTemplate.validForDays",
        "EntitlementTemplate.daysOfWeek",
        "EntitlementTemplate.expiryAnchor",
        "EntitlementTemplate.expiryDate",
        "EntitlementTemplate.carriesStoredValue",
        "EntitlementTemplate.includedValue"
       ],
       "operation": "listEntitlementTemplates",
       "provenance": "contract catalogue.yaml GET /entitlement-templates"
      },
      {
       "kind": "dataTable",
       "label": "Every alternative code",
       "bindsTo": "AlternativeCode",
       "columns": [
        "AlternativeCode.code",
        "AlternativeCode.partnerId",
        "AlternativeCode.partnerName",
        "AlternativeCode.variantId",
        "AlternativeCode.note"
       ],
       "operation": "listAlternativeCodes",
       "provenance": "contract catalogue.yaml GET /products/{productId}/alternative-codes"
      },
      {
       "kind": "dataTable",
       "label": "Every product variant",
       "bindsTo": "ProductVariant",
       "columns": [
        "ProductVariant.id",
        "ProductVariant.productId",
        "ProductVariant.sku",
        "ProductVariant.axisValues",
        "ProductVariant.name",
        "ProductVariant.barcode",
        "ProductVariant.isDefault",
        "ProductVariant.isActive"
       ],
       "operation": "listProductVariants",
       "provenance": "contract catalogue.yaml GET /products/{productId}/variants"
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
       "label": "Create entitlement template",
       "operation": "createEntitlementTemplate",
       "provenance": "contract catalogue.yaml POST /entitlement-templates"
      },
      {
       "kind": "secondaryButton",
       "label": "Create product",
       "operation": "createProduct",
       "provenance": "contract catalogue.yaml POST /products"
      },
      {
       "kind": "secondaryButton",
       "label": "Resolve product by code",
       "operation": "resolveProductByCode",
       "provenance": "contract catalogue.yaml GET /products/resolve"
      },
      {
       "kind": "secondaryButton",
       "label": "Save alternative codes",
       "operation": "setAlternativeCodes",
       "provenance": "contract catalogue.yaml PUT /products/{productId}/alternative-codes"
      },
      {
       "kind": "secondaryButton",
       "label": "Save product attributes",
       "operation": "setProductAttributes",
       "provenance": "contract catalogue.yaml PUT /products/{productId}/attributes"
      },
      {
       "kind": "secondaryButton",
       "label": "Transition product lifecycle",
       "operation": "transitionProductLifecycle",
       "provenance": "contract catalogue.yaml POST /products/{productId}/lifecycle"
      },
      {
       "kind": "secondaryButton",
       "label": "Save product",
       "operation": "updateProduct",
       "provenance": "contract catalogue.yaml PATCH /products/{productId}"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The membership products list.",
   "error": "Could not load. Names which read failed and leaves the membership products untouched.",
   "emptyFirstRun": "No membership products yet. Offers Create entitlement template (`createEntitlementTemplate`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on venueId, kind, isSellable and the membership products are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `PRODUCT_VIEW`, which `listProducts` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
    "trigger": "onAction"
   },
   {
    "operationId": "listAlternativeCodes",
    "contract": "catalogue",
    "purpose": "External identifiers for a product",
    "trigger": "onAction"
   },
   {
    "operationId": "listProductVariants",
    "contract": "catalogue",
    "purpose": "List generated variants",
    "trigger": "onAction"
   },
   {
    "operationId": "resolveProductByCode",
    "contract": "catalogue",
    "purpose": "Resolve a partner code to a product",
    "trigger": "onAction"
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
  "overlays": [
   {
    "id": "formCreateEntitlementTemplate",
    "component": "modal",
    "trigger": "Create entitlement template",
    "body": "**Collects what `createEntitlementTemplate` sends before it is called.** Required: `id`, `code`, `name`, `validityKind`. Optional: `description`, `validFromOffsetDays`, `validForDays`, `daysOfWeek`, `expiryAnchor`, `expiryDate`, `carriesStoredValue`, `includedValue`, `validTimeWindows`, `blackoutDates`, `fastTrackTier`, `entriesAllowed` and 15 more. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "EntitlementTemplate",
    "confirm": {
     "label": "Create entitlement template",
     "operation": "createEntitlementTemplate"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "code",
      "name",
      "validityKind",
      "description",
      "validFromOffsetDays",
      "validForDays",
      "daysOfWeek",
      "expiryAnchor",
      "expiryDate",
      "carriesStoredValue",
      "includedValue",
      "validTimeWindows",
      "blackoutDates",
      "fastTrackTier",
      "entriesAllowed",
      "reentryAllowed",
      "purchaseEligibility"
     ]
    },
    "provenance": "contract catalogue.yaml POST /entitlement-templates"
   },
   {
    "id": "formCreateProduct",
    "component": "modal",
    "trigger": "Create product",
    "body": "**Collects what `createProduct` sends before it is called.** Required: `code`, `name`, `kind`, `venueId`. Optional: `description`, `channels`, `entitlementTemplateId`, `dataMaskValues`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateProductRequest",
    "confirm": {
     "label": "Create product",
     "operation": "createProduct"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "code",
      "name",
      "kind",
      "venueId",
      "description",
      "channels",
      "entitlementTemplateId",
      "dataMaskValues"
     ]
    },
    "provenance": "contract catalogue.yaml POST /products"
   },
   {
    "id": "formSetAlternativeCodes",
    "component": "modal",
    "trigger": "Save alternative codes",
    "body": "**Collects what `setAlternativeCodes` sends before it is called.** Required: `codes`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save alternative codes",
     "operation": "setAlternativeCodes"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "codes"
     ]
    },
    "provenance": "contract catalogue.yaml PUT /products/{productId}/alternative-codes"
   },
   {
    "id": "formSetProductAttributes",
    "component": "modal",
    "trigger": "Save product attributes",
    "body": "**Collects what `setProductAttributes` sends before it is called.** Required: `axes`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save product attributes",
     "operation": "setProductAttributes"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "axes"
     ]
    },
    "provenance": "contract catalogue.yaml PUT /products/{productId}/attributes"
   },
   {
    "id": "formTransitionProductLifecycle",
    "component": "modal",
    "trigger": "Transition product lifecycle",
    "body": "**Collects what `transitionProductLifecycle` sends before it is called.** Required: `transition`, `reason`. Optional: `effectiveAt`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Transition product lifecycle",
     "operation": "transitionProductLifecycle"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "transition",
      "reason",
      "effectiveAt"
     ]
    },
    "provenance": "contract catalogue.yaml POST /products/{productId}/lifecycle"
   },
   {
    "id": "formUpdateProduct",
    "component": "modal",
    "trigger": "Save product",
    "body": "**Collects what `updateProduct` sends before it is called.** Nothing in the body is required. Optional: `name`, `description`, `channels`, `dataMaskValues`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "UpdateProductRequest",
    "confirm": {
     "label": "Save product",
     "operation": "updateProduct"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "name",
      "description",
      "channels",
      "dataMaskValues"
     ]
    },
    "provenance": "contract catalogue.yaml PATCH /products/{productId}"
   }
  ],
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
     "to": "BO-007",
     "trigger": "Product Directory",
     "carries": [
      "productId"
     ],
     "provenance": "derived — BO-007 declares entryState.params productId and BO-013 holds productId, so an edge into it carries them"
    },
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "carries": [
      "productId",
      "version"
     ],
     "provenance": "derived — BO-008 declares entryState.params productId, variantId, version and BO-013 holds productId, version, so an edge into it carries them"
    },
    {
     "to": "BO-009",
     "trigger": "Pricing Rules",
     "provenance": "derived — BO-009 declares entryState.params priceListId, ruleId and BO-013 holds none of them, so the edge carries nothing and BO-009 opens cold"
    },
    {
     "to": "BO-011",
     "trigger": "Packages & Bundles",
     "provenance": "flow F77 step 1→2",
     "carries": [
      "productId",
      "version"
     ]
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
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Performance id",
       "operation": "listChannelCapacities",
       "notes": "Sends `?performanceId=` to `listChannelCapacities`.",
       "provenance": "contract catalogue.yaml GET /channel-capacities"
      },
      {
       "kind": "dataTable",
       "label": "Every channel capacity",
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
      },
      {
       "kind": "dataTable",
       "label": "Every channel listing",
       "bindsTo": "ChannelListing",
       "columns": [
        "ChannelListing.id",
        "ChannelListing.channelName",
        "ChannelListing.productId",
        "ChannelListing.externalProductRef",
        "ChannelListing.status",
        "ChannelListing.allocationUnits",
        "ChannelListing.priceListId",
        "ChannelListing.adapter",
        "ChannelListing.adapterCredentialRef",
        "ChannelListing.pushIntervalMinutes",
        "ChannelListing.guestDataScope",
        "ChannelListing.lastPushedAt"
       ],
       "operation": "listChannelListings",
       "provenance": "contract subscription.yaml GET /channel-listings"
      },
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
      },
      {
       "kind": "publishGate",
       "impliedBy": "publishBundle",
       "notes": "Declares `publishBundle`. **The gate names what the publish will affect before it happens** — a disabled Publish with no reason is the state operators escalate.\n",
       "provenance": "carried from the previous definition"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected channel capacity",
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
      },
      {
       "kind": "detailPanel",
       "label": "The channel allocation set",
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
       "label": "Save channel allocations",
       "operation": "setChannelAllocations",
       "provenance": "contract catalogue.yaml PUT /channel-capacities/{channelCapacityId}/channel-allocations"
      },
      {
       "kind": "secondaryButton",
       "label": "Create channel capacity",
       "operation": "createChannelCapacity",
       "provenance": "contract catalogue.yaml POST /channel-capacities"
      },
      {
       "kind": "secondaryButton",
       "label": "Release channel allocation",
       "operation": "relinquishChannelAllocation",
       "provenance": "contract catalogue.yaml POST /channel-capacities/{channelCapacityId}/channel-allocations/release"
      },
      {
       "kind": "secondaryButton",
       "label": "Save channel capacity",
       "operation": "updateChannelCapacity",
       "provenance": "contract catalogue.yaml PATCH /channel-capacities/{channelCapacityId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Publish bundle",
       "operation": "publishBundle",
       "provenance": "contract catalogue.yaml POST /catalogue/bundles"
      },
      {
       "kind": "secondaryButton",
       "label": "Save channel listing",
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
    }
   ]
  },
  "states": {
   "loading": "The channel distribution list.",
   "error": "Could not load. Names which read failed and leaves the channel distribution untouched.",
   "emptyFirstRun": "No channel distribution yet. Offers Create channel capacity (`createChannelCapacity`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on performanceId and the channel distribution are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `PRODUCT_VIEW`, which `getChannelAllocations` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getChannelAllocations",
    "contract": "catalogue",
    "purpose": "Capacity allocated to each channel",
    "trigger": "onAction"
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
    "ChannelCapacity.id",
    "ChannelCapacity.performanceId",
    "ChannelCapacity.name",
    "ChannelCapacity.seatCategoryId",
    "ChannelCapacity.oversellAllowance"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-013",
   "derivedFrom": "wireframes/reference/Retail Board 5.dc.html",
   "source": "Claude Design Retail pack, 24 August",
   "note": "**Drawn by Claude Design on `Retail Board 5.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 10 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formSetChannelAllocations",
    "component": "modal",
    "trigger": "Save channel allocations",
    "body": "**Collects what `setChannelAllocations` sends before it is called.** Required: `allocations`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save channel allocations",
     "operation": "setChannelAllocations"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "allocations"
     ]
    },
    "provenance": "contract catalogue.yaml PUT /channel-capacities/{channelCapacityId}/channel-allocations"
   },
   {
    "id": "formCreateChannelCapacity",
    "component": "modal",
    "trigger": "Create channel capacity",
    "body": "**Collects what `createChannelCapacity` sends before it is called.** Required: `performanceId`, `name`, `capacity`. Optional: `seatCategoryId`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateEnvelopeRequest",
    "confirm": {
     "label": "Create channel capacity",
     "operation": "createChannelCapacity"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "performanceId",
      "name",
      "capacity",
      "seatCategoryId"
     ]
    },
    "provenance": "contract catalogue.yaml POST /channel-capacities"
   },
   {
    "id": "formRelinquishChannelAllocation",
    "component": "modal",
    "trigger": "Release channel allocation",
    "body": "**Collects what `relinquishChannelAllocation` sends before it is called.** Required: `channels`. Optional: `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Release channel allocation",
     "operation": "relinquishChannelAllocation"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "channels",
      "reason"
     ]
    },
    "provenance": "contract catalogue.yaml POST /channel-capacities/{channelCapacityId}/channel-allocations/release"
   },
   {
    "id": "formUpdateChannelCapacity",
    "component": "modal",
    "trigger": "Save channel capacity",
    "body": "**Collects what `updateChannelCapacity` sends before it is called.** Nothing in the body is required. Optional: `name`, `capacity`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save channel capacity",
     "operation": "updateChannelCapacity"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "name",
      "capacity"
     ]
    },
    "provenance": "contract catalogue.yaml PATCH /channel-capacities/{channelCapacityId}"
   },
   {
    "id": "formPublishBundle",
    "component": "modal",
    "trigger": "Publish bundle",
    "body": "**Collects what `publishBundle` sends before it is called.** Required: `venueId`. Optional: `note`, `staleAfterHours`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Publish bundle",
     "operation": "publishBundle"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "venueId",
      "note",
      "staleAfterHours"
     ]
    },
    "provenance": "contract catalogue.yaml POST /catalogue/bundles"
   },
   {
    "id": "formSetChannelListing",
    "component": "modal",
    "trigger": "Save channel listing",
    "body": "**Collects what `setChannelListing` sends before it is called.** Required: `id`, `channelName`, `productId`, `status`. Optional: `externalProductRef`, `allocationUnits`, `priceListId`, `adapter`, `adapterCredentialRef`, `pushIntervalMinutes`, `guestDataScope`, `lastPushedAt`, `scopePath`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "ChannelListing",
    "confirm": {
     "label": "Save channel listing",
     "operation": "setChannelListing"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "channelName",
      "productId",
      "status",
      "externalProductRef",
      "allocationUnits",
      "priceListId",
      "adapter",
      "adapterCredentialRef",
      "pushIntervalMinutes",
      "guestDataScope",
      "lastPushedAt",
      "scopePath"
     ]
    },
    "provenance": "contract subscription.yaml PUT /channel-listings"
   }
  ],
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
    "BO-007",
    "BO-008",
    "BO-009"
   ],
   "inferred": true,
   "entryFrom": [
    "BO-009",
    "BO-102"
   ],
   "transitions": [
    {
     "to": "BO-007",
     "trigger": "Product Directory",
     "carries": [
      "productId"
     ],
     "provenance": "derived — BO-007 declares entryState.params productId and BO-014 holds productId, so an edge into it carries them"
    },
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "carries": [
      "productId",
      "variantId",
      "version"
     ],
     "provenance": "derived — BO-008 declares entryState.params productId, variantId, version and BO-014 holds productId, variantId, version, so an edge into it carries them"
    },
    {
     "to": "BO-009",
     "trigger": "Pricing Rules",
     "carries": [
      "priceListId"
     ],
     "provenance": "derived — BO-009 declares entryState.params priceListId, ruleId and BO-014 holds priceListId, so an edge into it carries them"
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
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Venue id",
       "operation": "listProducts",
       "notes": "Sends `?venueId=` to `listProducts`.",
       "provenance": "contract catalogue.yaml GET /products"
      },
      {
       "kind": "textField",
       "label": "Kind",
       "operation": "listProducts",
       "notes": "Sends `?kind=` to `listProducts`.",
       "provenance": "contract catalogue.yaml GET /products"
      },
      {
       "kind": "toggle",
       "label": "Is sellable",
       "operation": "listProducts",
       "notes": "Sends `?isSellable=` to `listProducts`.",
       "provenance": "contract catalogue.yaml GET /products"
      },
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
      },
      {
       "kind": "dataTable",
       "label": "Every alternative code",
       "bindsTo": "AlternativeCode",
       "columns": [
        "AlternativeCode.code",
        "AlternativeCode.partnerId",
        "AlternativeCode.partnerName",
        "AlternativeCode.variantId",
        "AlternativeCode.note"
       ],
       "operation": "listAlternativeCodes",
       "provenance": "contract catalogue.yaml GET /products/{productId}/alternative-codes"
      },
      {
       "kind": "dataTable",
       "label": "Every product variant",
       "bindsTo": "ProductVariant",
       "columns": [
        "ProductVariant.id",
        "ProductVariant.productId",
        "ProductVariant.sku",
        "ProductVariant.axisValues",
        "ProductVariant.name",
        "ProductVariant.barcode",
        "ProductVariant.isDefault",
        "ProductVariant.isActive"
       ],
       "operation": "listProductVariants",
       "provenance": "contract catalogue.yaml GET /products/{productId}/variants"
      },
      {
       "kind": "dataTable",
       "label": "Every price",
       "bindsTo": "Price",
       "columns": [
        "Price.id",
        "Price.priceListId",
        "Price.variantId",
        "Price.amount",
        "Price.taxCodeId"
       ],
       "operation": "listPrices",
       "provenance": "contract catalogue.yaml GET /price-lists/{priceListId}/prices"
      },
      {
       "kind": "publishGate",
       "impliedBy": "publishBundle",
       "notes": "Declares `publishBundle`. **The gate names what the publish will affect before it happens** — a disabled Publish with no reason is the state operators escalate.\n",
       "provenance": "carried from the previous definition"
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
       "label": "Create product",
       "operation": "createProduct",
       "provenance": "contract catalogue.yaml POST /products"
      },
      {
       "kind": "secondaryButton",
       "label": "Resolve product by code",
       "operation": "resolveProductByCode",
       "provenance": "contract catalogue.yaml GET /products/resolve"
      },
      {
       "kind": "secondaryButton",
       "label": "Save alternative codes",
       "operation": "setAlternativeCodes",
       "provenance": "contract catalogue.yaml PUT /products/{productId}/alternative-codes"
      },
      {
       "kind": "secondaryButton",
       "label": "Save product attributes",
       "operation": "setProductAttributes",
       "provenance": "contract catalogue.yaml PUT /products/{productId}/attributes"
      },
      {
       "kind": "secondaryButton",
       "label": "Transition product lifecycle",
       "operation": "transitionProductLifecycle",
       "notes": "**Approve and publish are guarded separately** (decided 28 September, audit R091 (2)): the Approve transition (review to approved) is offered only to a holder of `PRODUCT_APPROVE`, and Publish (approved to live) only to a holder of `PRODUCT_PUBLISH`; the server refuses the other with 403 transition-permission-required.",
       "provenance": "contract catalogue.yaml POST /products/{productId}/lifecycle"
      },
      {
       "kind": "secondaryButton",
       "label": "Save product",
       "operation": "updateProduct",
       "provenance": "contract catalogue.yaml PATCH /products/{productId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Publish bundle",
       "operation": "publishBundle",
       "provenance": "contract catalogue.yaml POST /catalogue/bundles"
      },
      {
       "kind": "secondaryButton",
       "label": "Save item availability",
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
    }
   ]
  },
  "states": {
   "loading": "The catalogue publishing list.",
   "error": "Could not load. Names which read failed and leaves the catalogue publishing untouched.",
   "emptyFirstRun": "No catalogue publishing yet. Offers Create product (`createProduct`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on venueId, kind, isSellable and the catalogue publishing are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `PRODUCT_VIEW`, which `listProducts` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
    "trigger": "onAction"
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
    "trigger": "onAction"
   },
   {
    "operationId": "listProductVariants",
    "contract": "catalogue",
    "purpose": "List generated variants",
    "trigger": "onAction"
   },
   {
    "operationId": "resolveProductByCode",
    "contract": "catalogue",
    "purpose": "Resolve a partner code to a product",
    "trigger": "onAction"
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
   "derivedFrom": "wireframes/reference/Retail Board 2.dc.html",
   "source": "Claude Design Retail pack, 24 August",
   "note": "**Drawn by Claude Design on `Retail Board 2.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 13 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formCreateProduct",
    "component": "modal",
    "trigger": "Create product",
    "body": "**Collects what `createProduct` sends before it is called.** Required: `code`, `name`, `kind`, `venueId`. Optional: `description`, `channels`, `entitlementTemplateId`, `dataMaskValues`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateProductRequest",
    "confirm": {
     "label": "Create product",
     "operation": "createProduct"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "code",
      "name",
      "kind",
      "venueId",
      "description",
      "channels",
      "entitlementTemplateId",
      "dataMaskValues"
     ]
    },
    "provenance": "contract catalogue.yaml POST /products"
   },
   {
    "id": "formSetAlternativeCodes",
    "component": "modal",
    "trigger": "Save alternative codes",
    "body": "**Collects what `setAlternativeCodes` sends before it is called.** Required: `codes`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save alternative codes",
     "operation": "setAlternativeCodes"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "codes"
     ]
    },
    "provenance": "contract catalogue.yaml PUT /products/{productId}/alternative-codes"
   },
   {
    "id": "formSetProductAttributes",
    "component": "modal",
    "trigger": "Save product attributes",
    "body": "**Collects what `setProductAttributes` sends before it is called.** Required: `axes`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save product attributes",
     "operation": "setProductAttributes"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "axes"
     ]
    },
    "provenance": "contract catalogue.yaml PUT /products/{productId}/attributes"
   },
   {
    "id": "formTransitionProductLifecycle",
    "component": "modal",
    "trigger": "Transition product lifecycle",
    "body": "**Collects what `transitionProductLifecycle` sends before it is called.** Required: `transition`, `reason`. Optional: `effectiveAt`. The transition picker lists only what the principal may do — approve needs `PRODUCT_APPROVE`, publish needs `PRODUCT_PUBLISH` (decided 28 September, audit R091 (2)). Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Transition product lifecycle",
     "operation": "transitionProductLifecycle"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "transition",
      "reason",
      "effectiveAt"
     ]
    },
    "provenance": "contract catalogue.yaml POST /products/{productId}/lifecycle"
   },
   {
    "id": "formUpdateProduct",
    "component": "modal",
    "trigger": "Save product",
    "body": "**Collects what `updateProduct` sends before it is called.** Nothing in the body is required. Optional: `name`, `description`, `channels`, `dataMaskValues`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "UpdateProductRequest",
    "confirm": {
     "label": "Save product",
     "operation": "updateProduct"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "name",
      "description",
      "channels",
      "dataMaskValues"
     ]
    },
    "provenance": "contract catalogue.yaml PATCH /products/{productId}"
   },
   {
    "id": "formPublishBundle",
    "component": "modal",
    "trigger": "Publish bundle",
    "body": "**Collects what `publishBundle` sends before it is called.** Required: `venueId`. Optional: `note`, `staleAfterHours`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Publish bundle",
     "operation": "publishBundle"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "venueId",
      "note",
      "staleAfterHours"
     ]
    },
    "provenance": "contract catalogue.yaml POST /catalogue/bundles"
   },
   {
    "id": "formSetItemAvailability",
    "component": "modal",
    "trigger": "Save item availability",
    "body": "**Collects what `setItemAvailability` sends before it is called.** Required: `isAvailable`, `recordedAt`. Optional: `reason`, `restoreAt`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save item availability",
     "operation": "setItemAvailability"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "isAvailable",
      "recordedAt",
      "reason",
      "restoreAt"
     ]
    },
    "provenance": "contract fnb.yaml PUT /menu-items/{itemId}/availability"
   }
  ],
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
  "name": "Performance Calendar",
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
    "BO-009",
    "BO-099"
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
      "eventId"
     ],
     "provenance": "derived — BO-001 declares entryState.params eventId, feedId, queueId and BO-015 holds eventId, so an edge into it carries them"
    },
    {
     "to": "BO-007",
     "trigger": "Product Directory",
     "provenance": "derived — BO-007 declares entryState.params productId and BO-015 holds none of them, so the edge carries nothing and BO-007 opens cold"
    },
    {
     "to": "BO-009",
     "trigger": "Pricing Rules",
     "provenance": "derived — BO-009 declares entryState.params priceListId, ruleId and BO-015 holds none of them, so the edge carries nothing and BO-009 opens cold"
    },
    {
     "to": "BO-099",
     "trigger": "Performance manifest",
     "carries": [
      "performanceId"
     ],
     "provenance": "stated 28 September — BO-099 Performance Manifest is opened from a Performance (audit R165); the selected performance's id is its path parameter"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Drawn 26 August** — `Seat Board 2.dc.html` frame `seat-2a`. **The frame names this screen on its own face**, which is the first pack to do that: the earlier F&B, POS and Retail boards had to be hand-assigned by purpose after three derivation attempts produced nonsense. **A board that says what it draws removes the guess entirely.** **Kept separate from BO-016 (decided 28 September, audit R276)** — this screen lists, creates, changes and cancels performances; the template they are generated from is BO-016 Performance Template.",
  "density": "compact",
  "boardFrames": [
   "Seat Board 2.dc.html#seat-2a"
  ],
  "pattern": "listDetail",
  "patternReason": "`listPerformances` reads the population and `getPerformance` reads one of them — list, select, act",
  "purpose": "See what is scheduled and how full it is.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "datePicker",
       "label": "From",
       "operation": "listPerformances",
       "notes": "Sends `?from=` to `listPerformances`.",
       "provenance": "contract catalogue.yaml GET /events/{eventId}/performances"
      },
      {
       "kind": "datePicker",
       "label": "To",
       "operation": "listPerformances",
       "notes": "Sends `?to=` to `listPerformances`.",
       "provenance": "contract catalogue.yaml GET /events/{eventId}/performances"
      },
      {
       "kind": "dataTable",
       "label": "Every performance",
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
        "Performance.seatMapId",
        "Performance.language",
        "Performance.format"
       ],
       "operation": "listPerformances",
       "provenance": "contract catalogue.yaml GET /events/{eventId}/performances"
      },
      {
       "kind": "dataTable",
       "label": "Every event",
       "bindsTo": "Event",
       "columns": [
        "Event.id",
        "Event.code",
        "Event.name",
        "Event.venueId",
        "Event.scopePath",
        "Event.parentEventId",
        "Event.performanceCount",
        "Event.isActive"
       ],
       "operation": "listEvents",
       "provenance": "contract catalogue.yaml GET /events"
      },
      {
       "kind": "confirmDialog",
       "derived": true,
       "label": "Confirm",
       "notes": "**The consequence goes in the body, not the title.** *Cancel 3 orders worth AED 480* is a confirmation; *are you sure* is not — and a dialog that cannot name what it destroys is a dialog somebody dismisses.\n\n**Added 31 August.** `confirmDialog` and `modal` were both in the component library and used **zero times across 492 screens**, while `destructiveButton` was used 39 times and its own entry reads *always requires confirmation*.",
       "provenance": "carried from the previous definition"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected performance",
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
        "Performance.seatMapId",
        "Performance.language",
        "Performance.format"
       ],
       "operation": "getPerformance",
       "provenance": "contract catalogue.yaml GET /performances/{performanceId}"
      },
      {
       "kind": "detailPanel",
       "label": "The event",
       "bindsTo": "Event",
       "columns": [
        "Event.id",
        "Event.code",
        "Event.name",
        "Event.venueId",
        "Event.scopePath",
        "Event.parentEventId",
        "Event.performanceCount",
        "Event.isActive"
       ],
       "operation": "getEvent",
       "provenance": "contract catalogue.yaml GET /events/{eventId}"
      },
      {
       "kind": "detailPanel",
       "label": "The seat availability",
       "bindsTo": "SeatAvailability",
       "columns": [
        "SeatAvailability.performanceId",
        "SeatAvailability.seatMapId",
        "SeatAvailability.renderMode",
        "SeatAvailability.totals",
        "SeatAvailability.byCategory",
        "SeatAvailability.seats"
       ],
       "operation": "getSeatAvailability",
       "provenance": "contract seating.yaml GET /performances/{performanceId}/seat-availability"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create performances",
       "operation": "createPerformances",
       "provenance": "contract catalogue.yaml POST /events/{eventId}/performances"
      },
      {
       "kind": "destructiveButton",
       "label": "Cancel performance",
       "operation": "cancelPerformance",
       "provenance": "contract catalogue.yaml POST /performances/{performanceId}/cancel"
      },
      {
       "kind": "secondaryButton",
       "label": "Create event",
       "operation": "createEvent",
       "provenance": "contract catalogue.yaml POST /events"
      },
      {
       "kind": "secondaryButton",
       "label": "Recommend seats",
       "operation": "recommendSeats",
       "provenance": "contract seating.yaml POST /performances/{performanceId}/seat-recommendations"
      },
      {
       "kind": "secondaryButton",
       "label": "Save event",
       "operation": "updateEvent",
       "provenance": "contract catalogue.yaml PATCH /events/{eventId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Save performance",
       "operation": "updatePerformance",
       "provenance": "contract catalogue.yaml PATCH /performances/{performanceId}"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmCancelPerformance",
    "component": "confirmDialog",
    "trigger": "Cancel performance",
    "body": "**Names what `cancelPerformance` changes and what it leaves alone**, in the consequence rather than the verb. A session calendar this affects should be identified in the dialog, not just counted. **Collects what `cancelPerformance` sends before it is called.** Required: `reason`. Optional: `guestMessage`, `refundPercentage`, `offerAlternativePerformanceId`, `dryRun`. **A real run needs a supervisor PIN on this device** (`supervisorStepUp` {principalId, credential}); a dry run does not (decided 28 September, audit R144).",
    "provenance": "contract catalogue.yaml POST /performances/{performanceId}/cancel"
   },
   {
    "id": "formCreatePerformances",
    "component": "modal",
    "trigger": "Create performances",
    "body": "**Collects what `createPerformances` sends before it is called.** Required: `startsAt`, `endsAt`. Optional: `admissionRulesId`, `seatMapId`, `language` (BCP 47, e.g. `ar`, `fr`) and `format` (e.g. 2D, 3D, subtitled) for a tour or a screening (decided 29 September, rev 3 REV3-17), `recurrence`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreatePerformancesRequest",
    "confirm": {
     "label": "Create performances",
     "operation": "createPerformances"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "startsAt",
      "endsAt",
      "admissionRulesId",
      "seatMapId",
      "language",
      "format",
      "recurrence"
     ]
    },
    "provenance": "contract catalogue.yaml POST /events/{eventId}/performances"
   },
   {
    "id": "formCreateEvent",
    "component": "modal",
    "trigger": "Create event",
    "body": "**Collects what `createEvent` sends before it is called.** Required: `code`, `name`, `venueId`. Optional: `parentEventId`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateEventRequest",
    "confirm": {
     "label": "Create event",
     "operation": "createEvent"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "code",
      "name",
      "venueId",
      "parentEventId"
     ]
    },
    "provenance": "contract catalogue.yaml POST /events"
   },
   {
    "id": "formRecommendSeats",
    "component": "modal",
    "trigger": "Recommend seats",
    "body": "**Collects what `recommendSeats` sends before it is called.** Required: `partySize`, `strategy`. Optional: `categoryIds`, `maxPrice`, `accessibleCount`, `maxOptions`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "SeatRecommendationRequest",
    "confirm": {
     "label": "Recommend seats",
     "operation": "recommendSeats"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "partySize",
      "strategy",
      "categoryIds",
      "maxPrice",
      "accessibleCount",
      "maxOptions"
     ]
    },
    "provenance": "contract seating.yaml POST /performances/{performanceId}/seat-recommendations"
   },
   {
    "id": "formUpdateEvent",
    "component": "modal",
    "trigger": "Save event",
    "body": "**Collects what `updateEvent` sends before it is called.** Nothing in the body is required. Optional: `name`, `parentEventId`, `isActive`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save event",
     "operation": "updateEvent"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "name",
      "parentEventId",
      "isActive"
     ]
    },
    "provenance": "contract catalogue.yaml PATCH /events/{eventId}"
   },
   {
    "id": "formUpdatePerformance",
    "component": "modal",
    "trigger": "Save performance",
    "body": "**Collects what `updatePerformance` sends before it is called.** Nothing in the body is required. Optional: `startsAt`, `endsAt`, `status`, `admissionRulesId`, `language`, `format` (rev 3 REV3-17). Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save performance",
     "operation": "updatePerformance"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "startsAt",
      "endsAt",
      "status",
      "admissionRulesId",
      "language",
      "format"
     ]
    },
    "provenance": "contract catalogue.yaml PATCH /performances/{performanceId}"
   }
  ],
  "states": {
   "loading": "The session calendar list.",
   "error": "Could not load. Names which read failed and leaves the session calendar untouched.",
   "emptyFirstRun": "No session calendar yet. Offers Create performances (`createPerformances`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on from, to and the session calendar are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `PRODUCT_VIEW`, which `listPerformances` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPerformances",
    "contract": "catalogue",
    "purpose": "List performances of an event",
    "trigger": "onAction"
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
    "trigger": "onAction"
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
   "derivedFrom": "wireframes/reference/Seat Board 2.dc.html",
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
  "name": "Performance Template",
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
    "BO-007",
    "BO-009"
   ],
   "inferred": true,
   "entryFrom": [
    "BO-102"
   ],
   "transitions": [
    {
     "to": "BO-007",
     "trigger": "Product Directory",
     "provenance": "derived — BO-007 declares entryState.params productId and BO-016 holds none of them, so the edge carries nothing and BO-007 opens cold"
    },
    {
     "to": "BO-009",
     "trigger": "Pricing Rules",
     "provenance": "derived — BO-009 declares entryState.params priceListId, ruleId and BO-016 holds none of them, so the edge carries nothing and BO-009 opens cold"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Drawn 26 August** — `Seat Board 2.dc.html` frame `seat-2b`. **The frame names this screen on its own face**, which is the first pack to do that: the earlier F&B, POS and Retail boards had to be hand-assigned by purpose after three derivation attempts produced nonsense. **A board that says what it draws removes the guess entirely.** **Split from BO-015 on 28 September (audit R276)** — the two carried identical performance and event operations; this screen now owns the performance template (`listPerformanceTemplates`, `setPerformanceTemplate`) and BO-015 keeps the calendar of performances.",
  "density": "compact",
  "boardFrames": [
   "Seat Board 2.dc.html#seat-2b"
  ],
  "pattern": "listDetail",
  "patternReason": "`listPerformanceTemplates` reads the population and the selected row is the detail; `setPerformanceTemplate` saves one — list, select, act",
  "purpose": "Define the pattern the calendar is generated from — slot length, turnaround, concurrent capacity, peak bands and walk-in rules. BO-015 Performance Calendar generates and manages the performances themselves (kept separate, decided 28 September, audit R276).",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every performance template",
       "bindsTo": "PerformanceTemplate",
       "columns": [
        "PerformanceTemplate.code",
        "PerformanceTemplate.name",
        "PerformanceTemplate.spaceId",
        "PerformanceTemplate.slotMinutes",
        "PerformanceTemplate.turnaroundMinutes",
        "PerformanceTemplate.concurrentCapacity"
       ],
       "operation": "listPerformanceTemplates",
       "provenance": "contract catalogue.yaml GET /performance-templates"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected performance template",
       "bindsTo": "PerformanceTemplate",
       "columns": [
        "PerformanceTemplate.id",
        "PerformanceTemplate.code",
        "PerformanceTemplate.name",
        "PerformanceTemplate.spaceId",
        "PerformanceTemplate.slotMinutes",
        "PerformanceTemplate.turnaroundMinutes",
        "PerformanceTemplate.concurrentCapacity",
        "PerformanceTemplate.bands",
        "PerformanceTemplate.walkIn"
       ],
       "operation": "listPerformanceTemplates",
       "provenance": "contract catalogue.yaml GET /performance-templates"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save performance template",
       "operation": "setPerformanceTemplate",
       "provenance": "contract catalogue.yaml PUT /performance-templates"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The performance template list.",
   "error": "Could not load. Names which read failed and leaves the performance templates untouched.",
   "emptyFirstRun": "No performance template yet. Offers Save performance template (`setPerformanceTemplate`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Never shown: `listPerformanceTemplates` takes no filter, so an empty list is always the first-run state above.",
   "emptyNoAccess": "Shown when the caller lacks `PERFORMANCE_CONFIGURE`, which `listPerformanceTemplates` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPerformanceTemplates",
    "contract": "catalogue",
    "purpose": "Slot templates, peak bands and walk-in rules",
    "trigger": "onLoad"
   },
   {
    "operationId": "setPerformanceTemplate",
    "contract": "catalogue",
    "purpose": "Create or change a performance template",
    "trigger": "onAction",
    "invalidates": [
     "listPerformanceTemplates"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-016",
   "derivedFrom": "wireframes/reference/Seat Board 2.dc.html",
   "note": "**Drawn by Claude Design on `Seat Board 2.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 28 September 2026 on performance templates (audit R276). Until then it was a clone of BO-015 carrying the same 11 performance and event operations; those stay on BO-015.",
  "overlays": [
   {
    "id": "formSetPerformanceTemplate",
    "component": "modal",
    "trigger": "Save performance template",
    "body": "**Collects what `setPerformanceTemplate` sends before it is called.** Required: `code`. Optional: `id`, `name`, `spaceId`, `slotMinutes`, `turnaroundMinutes`, `concurrentCapacity`, `bands`, `walkIn`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "PerformanceTemplate",
    "confirm": {
     "label": "Save performance template",
     "operation": "setPerformanceTemplate"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "code",
      "name",
      "spaceId",
      "slotMinutes",
      "turnaroundMinutes",
      "concurrentCapacity",
      "bands",
      "walkIn"
     ]
    },
    "provenance": "contract catalogue.yaml PUT /performance-templates"
   }
  ],
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
    "BO-007",
    "BO-009"
   ],
   "inferred": true,
   "entryFrom": [
    "BO-102"
   ],
   "transitions": [
    {
     "to": "BO-007",
     "trigger": "Product Directory",
     "provenance": "derived — BO-007 declares entryState.params productId and BO-017 holds none of them, so the edge carries nothing and BO-007 opens cold"
    },
    {
     "to": "BO-009",
     "trigger": "Pricing Rules",
     "provenance": "derived — BO-009 declares entryState.params priceListId, ruleId and BO-017 holds none of them, so the edge carries nothing and BO-009 opens cold"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listChannelCapacities` reads the population and `getChannelAllocations` reads one of them — list, select, act",
  "purpose": "Change how many people a performance can take (renamed from session, decided 28 September, audit R165).",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Performance id",
       "operation": "listChannelCapacities",
       "notes": "Sends `?performanceId=` to `listChannelCapacities`.",
       "provenance": "contract catalogue.yaml GET /channel-capacities"
      },
      {
       "kind": "dataTable",
       "label": "Every channel capacity",
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
       "label": "The selected channel capacity",
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
      },
      {
       "kind": "detailPanel",
       "label": "The channel allocation set",
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
       "label": "Create channel capacity",
       "operation": "createChannelCapacity",
       "provenance": "contract catalogue.yaml POST /channel-capacities"
      },
      {
       "kind": "secondaryButton",
       "label": "Release channel allocation",
       "operation": "relinquishChannelAllocation",
       "provenance": "contract catalogue.yaml POST /channel-capacities/{channelCapacityId}/channel-allocations/release"
      },
      {
       "kind": "secondaryButton",
       "label": "Save channel allocations",
       "operation": "setChannelAllocations",
       "provenance": "contract catalogue.yaml PUT /channel-capacities/{channelCapacityId}/channel-allocations"
      },
      {
       "kind": "secondaryButton",
       "label": "Save channel capacity",
       "operation": "updateChannelCapacity",
       "provenance": "contract catalogue.yaml PATCH /channel-capacities/{channelCapacityId}"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The capacity list.",
   "error": "Could not load. Names which read failed and leaves the capacity untouched.",
   "emptyFirstRun": "No capacity yet. Offers Create channel capacity (`createChannelCapacity`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on performanceId and the capacity are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `PRODUCT_VIEW`, which `listChannelCapacities` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
    "trigger": "onAction"
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
   },
   {
    "operationId": "listWaitlistEntries",
    "contract": "catalogue",
    "purpose": "Guests waiting for capacity",
    "trigger": "onLoad",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   },
   {
    "operationId": "offerWaitlistCapacity",
    "contract": "catalogue",
    "purpose": "Tell a waiting guest that capacity appeared",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listChannelCapacities",
     "getChannelAllocations",
     "listWaitlistEntries"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "channelCapacityId",
     "from": "deepLink"
    },
    {
     "name": "entryId",
     "from": "navigation"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `channelCapacityId`.",
   "preloaded": [
    "ChannelCapacity.id",
    "ChannelCapacity.performanceId",
    "ChannelCapacity.name",
    "ChannelCapacity.seatCategoryId",
    "ChannelCapacity.oversellAllowance"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-017"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 6 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formCreateChannelCapacity",
    "component": "modal",
    "trigger": "Create channel capacity",
    "body": "**Collects what `createChannelCapacity` sends before it is called.** Required: `performanceId`, `name`, `capacity`. Optional: `seatCategoryId`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateEnvelopeRequest",
    "confirm": {
     "label": "Create channel capacity",
     "operation": "createChannelCapacity"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "performanceId",
      "name",
      "capacity",
      "seatCategoryId"
     ]
    },
    "provenance": "contract catalogue.yaml POST /channel-capacities"
   },
   {
    "id": "formRelinquishChannelAllocation",
    "component": "modal",
    "trigger": "Release channel allocation",
    "body": "**Collects what `relinquishChannelAllocation` sends before it is called.** Required: `channels`. Optional: `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Release channel allocation",
     "operation": "relinquishChannelAllocation"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "channels",
      "reason"
     ]
    },
    "provenance": "contract catalogue.yaml POST /channel-capacities/{channelCapacityId}/channel-allocations/release"
   },
   {
    "id": "formSetChannelAllocations",
    "component": "modal",
    "trigger": "Save channel allocations",
    "body": "**Collects what `setChannelAllocations` sends before it is called.** Required: `allocations`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save channel allocations",
     "operation": "setChannelAllocations"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "allocations"
     ]
    },
    "provenance": "contract catalogue.yaml PUT /channel-capacities/{channelCapacityId}/channel-allocations"
   },
   {
    "id": "formUpdateChannelCapacity",
    "component": "modal",
    "trigger": "Save channel capacity",
    "body": "**Collects what `updateChannelCapacity` sends before it is called.** Nothing in the body is required. Optional: `name`, `capacity`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save channel capacity",
     "operation": "updateChannelCapacity"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "name",
      "capacity"
     ]
    },
    "provenance": "contract catalogue.yaml PATCH /channel-capacities/{channelCapacityId}"
   }
  ],
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
 "assignCoupon": {
  "method": "POST",
  "path": "/coupon-codes/{code}/assign",
  "contract": "promotions",
  "summary": "Assign a coupon to a named guest",
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
 "bulkChangePrices": {
  "method": "POST",
  "path": "/products/bulk-price",
  "contract": "catalogue",
  "summary": "Reprice a category or a whole catalogue",
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
  "responds": "BulkPriceResult"
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
  "summary": "Create a channel capacity",
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
 "createCombo": {
  "method": "POST",
  "path": "/combos",
  "contract": "fnb",
  "summary": "A meal deal, priced as one thing",
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
  "requestBody": "Combo",
  "responds": "Combo"
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
 "createVoucherBatch": {
  "method": "POST",
  "path": "/voucher-batches",
  "contract": "promotions",
  "summary": "Issue a voucher batch",
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
  "requestBody": "CreateVoucherBatchRequest",
  "responds": "VoucherBatch"
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
 "getDynamicPriceRule": {
  "method": "GET",
  "path": "/pricing/dynamic-rules/{ruleId}",
  "contract": "catalogue",
  "summary": "One rule with its conditions and actions",
  "permission": "PRICE_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "ruleId",
    "in": "path",
    "required": true
   }
  ],
  "requestBody": null,
  "responds": "DynamicPriceRuleDetail"
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
 "getGroupPackageDefinition": {
  "method": "GET",
  "path": "/products/{productId}/group-package",
  "contract": "catalogue",
  "summary": "A school-trip format or party package",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "productId",
    "in": "path",
    "required": true
   }
  ],
  "requestBody": null,
  "responds": "GroupPackageDefinition"
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
  "summary": "List published catalogue bundles",
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
  "summary": "List channel capacities",
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
    "name": "batchId",
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
 "listDynamicPriceRules": {
  "method": "GET",
  "path": "/pricing/dynamic-rules",
  "contract": "catalogue",
  "summary": "Dynamic pricing rules",
  "permission": "PRICE_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "PricingDynamicPriceRule"
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
 "listPerformanceTemplates": {
  "method": "GET",
  "path": "/performance-templates",
  "contract": "catalogue",
  "summary": "Slot templates, peak bands and walk-in rules",
  "permission": "PERFORMANCE_CONFIGURE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "PerformanceTemplate"
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
    "name": "language",
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
    "name": "categoryId",
    "in": "query",
    "required": null
   },
   {
    "name": "segmentTag",
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
 "listVoucherBatches": {
  "method": "GET",
  "path": "/voucher-batches",
  "contract": "promotions",
  "summary": "List voucher batches",
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
 "listWaitlistEntries": {
  "method": "GET",
  "path": "/waitlist-entries",
  "contract": "catalogue",
  "summary": "Who is waiting for capacity",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "performanceId",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "WaitlistEntry"
 },
 "offerWaitlistCapacity": {
  "method": "POST",
  "path": "/waitlist-entries/{entryId}/offer",
  "contract": "catalogue",
  "summary": "Tell a waiting guest that capacity appeared",
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
  "responds": "WaitlistEntry"
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
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
  "summary": "Allocate a channel capacity across sales channels",
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
 "setComboSlots": {
  "method": "PUT",
  "path": "/combos/{comboId}/slots",
  "contract": "fnb",
  "summary": "What the guest chooses, and what it costs extra",
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
  "responds": "Combo"
 },
 "setDynamicPriceRule": {
  "method": "PUT",
  "path": "/pricing/dynamic-rules/{ruleId}",
  "contract": "catalogue",
  "summary": "Replace a rule, its conditions and its actions",
  "permission": "PRICE_CONFIGURE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "ruleId",
    "in": "path",
    "required": true
   },
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "DynamicPriceRuleDetail",
  "responds": "DynamicPriceRuleDetail"
 },
 "setGroupPackageDefinition": {
  "method": "PUT",
  "path": "/products/{productId}/group-package",
  "contract": "catalogue",
  "summary": "Define a school-trip format or party package",
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
    "name": "productId",
    "in": "path",
    "required": true
   }
  ],
  "requestBody": "GroupPackageDefinition",
  "responds": "GroupPackageDefinition"
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
 "setPerformanceTemplate": {
  "method": "PUT",
  "path": "/performance-templates",
  "contract": "catalogue",
  "summary": "Define slot length, capacity, bands and walk-in policy",
  "permission": "PERFORMANCE_CONFIGURE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "PerformanceTemplate",
  "responds": "PerformanceTemplate"
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
 "setPromotionVariants": {
  "method": "PUT",
  "path": "/promotions/{promotionId}/variants",
  "contract": "promotions",
  "summary": "A/B test two versions against each other",
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
 "simulatePromotion": {
  "method": "POST",
  "path": "/promotions/{promotionId}/simulate",
  "contract": "promotions",
  "summary": "What this promotion would have cost on real history",
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
 "updateBundle": {
  "method": "PATCH",
  "path": "/bundles/{bundleId}",
  "contract": "promotions",
  "summary": "Amend a bundle",
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
  "responds": "Bundle"
 },
 "updateChannelCapacity": {
  "method": "PATCH",
  "path": "/channel-capacities/{channelCapacityId}",
  "contract": "catalogue",
  "summary": "Amend a channel capacity",
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
 },
 "voidVoucher": {
  "method": "POST",
  "path": "/vouchers/{voucherId}/void",
  "contract": "promotions",
  "summary": "Cancel a voucher",
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
  "responds": "Voucher"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AllergenCode": {
  "type": "string",
  "description": "**The fourteen declarable allergens, as one closed list.** Every allergen field in this contract uses it — the menu claim, the ticket line, a substitution's delta, a modifier option, the label on a bag — so a declared set and an actual set compare without anybody normalising case or synonyms. It was the `Allergen.contains` enum; the other fields were free text.\n",
  "enum": [
   "gluten",
   "crustaceans",
   "eggs",
   "fish",
   "peanuts",
   "soybeans",
   "milk",
   "nuts",
   "celery",
   "mustard",
   "sesame",
   "sulphites",
   "lupin",
   "molluscs"
  ]
 },
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
    "description": "For `proRataListPrice` — weights derived from list prices. **The variant's current price when the bundle is created** (decided 28 September, audit R101), then frozen with the allocation."
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
 "BulkPriceResult": {
  "type": "object",
  "description": "2.9.9. Dry run or applied — the shape is the same, `applied` says which.",
  "required": [
   "applied",
   "productsMatched"
  ],
  "properties": {
   "applied": {
    "type": "boolean"
   },
   "productsMatched": {
    "type": "integer"
   },
   "pricesChanged": {
    "type": "integer"
   },
   "skipped": {
    "type": "array",
    "description": "**Products the selection matched and the adjustment could not touch** — a fixed-price bundle, a partner net rate, a product in an open period. Named rather than counted, because whoever ran this will be asked why the total is short.\n",
    "items": {
     "type": "object",
     "properties": {
      "productId": {
       "type": "string",
       "format": "uuid"
      },
      "reason": {
       "type": "string"
      }
     }
    }
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
  "x-ticvai-persistence": "promotions.bundle_choice_group + promotions.bundle_choice_option",
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
    "description": "The rows of `promotions.bundle_choice_option`, one per option, each keyed to its group. A required array with nowhere to be stored was a group whose choices were lost on write.\n",
    "items": {
     "type": "object",
     "required": [
      "variantId"
     ],
     "properties": {
      "id": {
       "type": "string",
       "format": "uuid",
       "readOnly": true
      },
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
  "description": "One published catalogue bundle — the signed snapshot terminals pull (ADR-0013). Not `promotions.Bundle`, which is a sellable product made of other products.",
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
    "description": "Products, variants, price lists, prices, tax codes, events, performances, envelope definitions, data mask field definitions and the venue's sale boards. Shape is versioned with the bundle format, not with this API.\n",
    "additionalProperties": true,
    "properties": {
     "saleBoards": {
      "type": "array",
      "description": "**The venue's sale boards as `tenancy.listSaleBoards` returns them**, read from `platform.sale_board` when the bundle is snapshotted (decided 28 September, audit R129 (4)). A board changed by `updateSaleBoard` reaches terminals here, with the next bundle, and never mid-transaction.\n",
      "items": {
       "type": "object",
       "additionalProperties": true
      }
     }
    }
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
    "type": "integer",
    "readOnly": true
   },
   "leased": {
    "type": "integer",
    "readOnly": true
   },
   "remaining": {
    "type": "integer",
    "readOnly": true
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
 "Combo": {
  "type": "object",
  "x-ticvai-persistence": "fnb.combo",
  "description": "Board 2G, 24 August. **A meal deal is one product with slots, not a bundle of products.** `listCatalogueBundles` bundles ticketing products — a ticket and a parking pass, both fixed — and **a burger with a choice of side and a choice of drink is a different shape entirely.**\n**The price is on the combo, not the sum of its parts.** That is the whole commercial point: a meal deal is cheaper than its items, and a model that prices by summing cannot express it.\n**Upcharges live on the slot options.** A large drink in a meal deal costs two dirhams more than a regular, and it is not a separate combo.\n",
  "required": [
   "id",
   "name",
   "price",
   "slots"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "outletId": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string"
   },
   "nameLocalised": {
    "type": "object",
    "additionalProperties": {
     "type": "string"
    }
   },
   "price": {
    "x-ticvai-column": "list_price",
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "slots": {
    "type": "array",
    "minItems": 1,
    "items": {
     "$ref": "#/components/schemas/ComboSlot"
    }
   },
   "availability": {
    "allOf": [
     {
      "$ref": "#/components/schemas/MenuAvailability"
     }
    ],
    "nullable": true,
    "description": "Service periods it sells in, in the same shape as a menu's. **A lunch deal at 9pm is a margin leak** and the venue only notices at month end.\n"
   },
   "isActive": {
    "type": "boolean",
    "default": true
   }
  }
 },
 "ComboSlot": {
  "type": "object",
  "x-ticvai-persistence": "fnb.combo_slot",
  "description": "One choice within a combo. **`minSelect` and `maxSelect` are what make it a slot rather than a line** — a main is exactly one, a side is one of four, and a sauce might be none or two.\n",
  "required": [
   "id",
   "name",
   "options"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "comboId": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string"
   },
   "minSelect": {
    "type": "integer",
    "default": 1
   },
   "maxSelect": {
    "type": "integer",
    "default": 1
   },
   "sortOrder": {
    "type": "integer",
    "default": 100
   },
   "options": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "menuItemId"
     ],
     "properties": {
      "menuItemId": {
       "type": "string",
       "format": "uuid"
      },
      "upcharge": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "isDefault": {
       "type": "boolean",
       "default": false,
       "description": "**The one a cashier gets without asking.** A combo with no default is four taps at every till in the venue.\n"
      }
     }
    }
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
       "description": "True where the combination would produce a line price of zero or below (decided 28 September, audit R101)."
      },
      "isNearZero": {
       "type": "boolean",
       "description": "True where the combination leaves a net line price above zero but below the venue setting `promotions.nearZeroLinePrice` (proposed AED 1.00; decided 28 September, audit R096 (5)). A warning, not a refusal."
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
   "batchId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The `generateCouponCodes` batch that issued this code. Null where no batch did."
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
    "x-ticvai-column": "list_price",
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
      "allOf": [
       {
        "$ref": "#/components/schemas/AllocationMethod"
       }
      ],
      "default": "proRataListPrice",
      "description": "Proportional to list price by default. The rounding remainder in the currency's minor unit goes to the first component (decided 28 September, audit R101).\n"
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
  "description": "The body of `createChannelCapacity`. **Named before the 26 August rename** (envelope to `ChannelCapacity`); the name stays because generated code is keyed on it.",
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
    "maxLength": 64,
    "x-ticvai-unique": "tenant",
    "description": "**Unique per tenant** (decided 28 September, audit R108). A code already used by any event in the tenant is refused with `409 duplicate-code`.\n"
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
   "description": {
    "type": "string",
    "description": "What the item is, in the guest's words. Indexed for guest-app search."
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
   "language": {
    "type": "string",
    "nullable": true,
    "maxLength": 35,
    "pattern": "^[A-Za-z]{2,3}(-[A-Za-z0-9]{1,8})*$",
    "description": "As `Performance.language`; every performance of a generated series takes it (decided 29 September, rev 3 REV3-17)."
   },
   "format": {
    "type": "string",
    "nullable": true,
    "maxLength": 40,
    "description": "As `Performance.format` (decided 29 September, rev 3 REV3-17)."
   },
   "recurrence": {
    "type": "object",
    "description": "Generate a series rather than a single performance. **Read in the region's time zone**: the Region owns the zone and every venue inherits it without override (tenancy), so `daysOfWeek` are the region's calendar days and `until` is compared on the region's clock.\n",
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
    "description": "Total discount value after which the promotion stops automatically. **Enforced at checkout**, where an order whose discount would take the total past the cap does not receive the promotion (decided 28 September, audit R101)."
   }
  }
 },
 "CreateVoucherBatchRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "name",
   "venueId",
   "faceValue",
   "quantity",
   "validTo"
  ],
  "properties": {
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "faceValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "quantity": {
    "type": "integer",
    "minimum": 1,
    "maximum": 50000
   },
   "allowPartialRedemption": {
    "type": "boolean",
    "default": true,
    "description": "False forfeits any unused balance, which is then recognised as breakage.\n"
   },
   "validFrom": {
    "type": "string",
    "format": "date-time"
   },
   "validTo": {
    "type": "string",
    "format": "date-time"
   },
   "restrictToVariantIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
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
     "archivedAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true,
      "readOnly": true,
      "description": "**Set by `deleteDashboard`, which archives rather than removes.** A dashboard's tiles carry `visualisation`, `parameters` and `refresh_seconds` that somebody configured, and `reporting.dashboard_tile` cascades — so a hard delete takes an afternoon's work with it and leaves nothing to say what was there.\nArchived dashboards are excluded from `listDashboards` unless asked for with `includeArchived=true`.\n"
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
 "DynamicPriceRuleDetail": {
  "type": "object",
  "x-ticvai-persistence": "none — composed from a rule, its conditions and its actions",
  "description": "**A rule is unreadable without both halves.** The conditions say when it fires, the actions say what it does to the price, and `minPrice`/`maxPrice` on the action are the guard rails a reviewer looks for first.\n",
  "required": [
   "rule"
  ],
  "properties": {
   "rule": {
    "$ref": "#/components/schemas/PricingDynamicPriceRule"
   },
   "conditions": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/PricingDynamicPriceCondition"
    }
   },
   "actions": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/PricingDynamicPriceAction"
    }
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
   "description": {
    "type": "string",
    "description": "**Validity, re-entry and transfer rules in prose.** \"Can I leave and come back\" is answered from here, and a name cannot answer it.\n"
   },
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "Assigned by the server on create; `createEntitlementTemplate` does not take it."
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
   "transportRestriction": {
    "type": "object",
    "nullable": true,
    "description": "**The journey a transport pass is good for** (decided 29 September, rev 3 REV3-21). Set on the template `transport.createTransportPassType` creates, from the station pair the guest bought the pass for, and copied to the entitlement. `access` refuses a boarding scan whose departure does not serve both stations in a direction the restriction allows, and consumes one of `entriesAllowed` per boarding. Null on every other template.\n",
    "required": [
     "fromStationId",
     "toStationId"
    ],
    "properties": {
     "fromStationId": {
      "type": "string",
      "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
      "description": "A `transport.Station`."
     },
     "toStationId": {
      "type": "string",
      "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
     },
     "bothDirections": {
      "type": "boolean",
      "default": true,
      "description": "Valid from either station to the other, as the prototype sells it."
     },
     "routeIds": {
      "type": "array",
      "description": "The routes it may be used on. Empty means any active route serving both stations.",
      "items": {
       "type": "string",
       "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
      }
     }
    }
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
   "autoRenewDefault": {
    "type": "boolean",
    "default": false,
    "description": "**Taken from their `membership_plan`, 20 September — the \"take those\" half of the TAKE BODY verdict.** `identity.customer_membership.auto_renew` carries the flag per holder and nothing said what it should start as.\n"
   },
   "renewalTermDays": {
    "type": "integer",
    "nullable": true,
    "description": "What a renewal extends the membership by. `orders.membership_renewal` records `previousExpiryAt` and `newExpiryAt` and **the number between them lived nowhere**.\n"
   },
   "renewalGraceDays": {
    "type": "integer",
    "default": 0,
    "description": "How long after expiry a membership can still be renewed rather than rejoined. `membership_renewal.failureReason` implies a window and there was none, so a failed card on the expiry date had no defined consequence.\n"
   },
   "renewalVariantId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**What a renewal sells, which is usually not what joining sold.** A first-year price and a renewal price are different products, and pointing both at one variant makes a loyalty discount unrepresentable. Null means renewal sells the same thing.\n"
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
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.** Set by the server, never taken from a body."
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
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/SalesChannel"
     }
    ],
    "description": "Where the sale is being made. Matched against `PromotionConditions.channels`, so both sides use the one shared vocabulary.\n"
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
    "type": "integer",
    "readOnly": true,
    "description": "How many performances the event has. Counted by the server; never sent by a client."
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
 "GroupPackageDefinition": {
  "type": "object",
  "x-ticvai-persistence": "catalogue.group_package",
  "required": [
   "kind",
   "maxParticipants",
   "durationMinutes"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "productId": {
    "type": "string",
    "readOnly": true
   },
   "kind": {
    "type": "string",
    "enum": [
     "school",
     "party"
    ]
   },
   "maxParticipants": {
    "type": "integer",
    "minimum": 1,
    "description": "Pupils or children, e.g. 30 or 10."
   },
   "durationMinutes": {
    "type": "integer",
    "minimum": 15
   },
   "hostCount": {
    "type": "integer",
    "minimum": 0,
    "default": 1,
    "description": "Party hosts included."
   },
   "pricingBasis": {
    "type": "string",
    "enum": [
     "perParticipant",
     "perPackage"
    ]
   },
   "freeLeaderRatio": {
    "type": "integer",
    "nullable": true,
    "default": 10,
    "description": "Schools: one teacher or assistant enters free per this many pupils."
   },
   "paymentMode": {
    "type": "string",
    "enum": [
     "invoice",
     "deposit",
     "full"
    ],
    "description": "Schools are invoiced; parties take a deposit (see `DepositPolicy`)."
   },
   "includes": {
    "type": "array",
    "items": {
     "type": "string",
     "maxLength": 120
    }
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Operations write it at `venue` scope."
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
 "LocalisedText": {
  "x-ticvai-persistence": "none — jsonb column",
  "type": "object",
  "additionalProperties": {
   "type": "string"
  }
 },
 "MenuAvailability": {
  "x-ticvai-persistence": "none — embedded in menu",
  "type": "object",
  "description": "When this menu is in force. Absent means always. Days, times and dates are all read in the Region's time zone, not UTC.",
  "properties": {
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
    "pattern": "^([01]\\d|2[0-3]):[0-5]\\d$",
    "description": "Wall-clock time, in the Region's time zone."
   },
   "endTime": {
    "type": "string",
    "pattern": "^([01]\\d|2[0-3]):[0-5]\\d$",
    "description": "Wall-clock time, in the Region's time zone."
   },
   "validFrom": {
    "type": "string",
    "format": "date",
    "nullable": true,
    "description": "Calendar day, in the Region's time zone, not UTC."
   },
   "validTo": {
    "type": "string",
    "format": "date",
    "nullable": true,
    "description": "Calendar day, in the Region's time zone, not UTC."
   }
  }
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
    "x-ticvai-column": "list_price",
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
   "menuSectionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "The section the item sits in, set by `setMenuSections` and `applyMenuActions` (`moveSection`)."
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
   "restoreAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "When an unavailable item comes back on its own (`setItemAvailability`). Null means by hand."
   },
   "preparationMinutes": {
    "type": "integer",
    "nullable": true
   },
   "allergens": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/AllergenCode"
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
   "description": {
    "type": "string",
    "description": "What the item is, in the guest's words. Indexed for guest-app search.\n"
   },
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
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "x-ticvai-column": "list_price"
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
   },
   "language": {
    "type": "string",
    "nullable": true,
    "maxLength": 35,
    "pattern": "^[A-Za-z]{2,3}(-[A-Za-z0-9]{1,8})*$",
    "description": "The language the performance is given in, as a BCP 47 tag (`en`, `ar`, `fr`, `de`, `zh`, `ru`, `ar-AE`). **A guided tour at 10:00 in French and one at 10:00 in Arabic are two performances**, so a guest who picks a language sees only the tours in it (`listPerformances` `language`). Null when the performance is not language-specific (decided 29 September, rev 3 REV3-17).\n"
   },
   "format": {
    "type": "string",
    "nullable": true,
    "maxLength": 40,
    "description": "How it is presented, free text the venue chooses, e.g. `2D`, `3D`, `IMAX`, `subtitled`. A cinema screening shows language and format together. Null when it does not apply (decided 29 September, rev 3 REV3-17).\n"
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
    "description": "**Null on this response.** The refund batch is created by `orders` when it consumes `performance.cancelled` (F09), after this call has returned, and is queued there for approval — refunds are not issued automatically. Read it from orders, not from here.\n"
   },
   "notificationsQueued": {
    "type": "integer"
   }
  }
 },
 "PerformanceTemplate": {
  "type": "object",
  "x-ticvai-persistence": "catalogue.performance_template",
  "description": "Event board 8. **An activity venue sells time, not seats.** Each slot the template produces is a Performance. Formerly `SessionTemplate` on `catalogue.session_template`: a session is a Performance (decided 28 September, audit R165).",
  "required": [
   "code"
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
   "spaceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "slotMinutes": {
    "type": "integer"
   },
   "turnaroundMinutes": {
    "type": "integer",
    "default": 0
   },
   "concurrentCapacity": {
    "type": "integer"
   },
   "bands": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "kind": {
       "type": "string",
       "enum": [
        "offPeak",
        "standard",
        "peak",
        "superPrime"
       ]
      },
      "daysOfWeek": {
       "type": "array",
       "items": {
        "type": "string"
       }
      },
      "from": {
       "type": "string"
      },
      "to": {
       "type": "string"
      },
      "priceMultiplier": {
       "type": "number",
       "nullable": true
      },
      "minuteMultiplier": {
       "type": "number",
       "nullable": true
      }
     }
    }
   },
   "walkIn": {
    "type": "object",
    "description": "**Configured, not assumed.** It decides whether a family turning up on a Sunday is turned away.\n",
    "properties": {
     "allowed": {
      "type": "boolean",
      "default": true
     },
     "heldBackPercent": {
      "type": "integer",
      "default": 0
     },
     "cutoffMinutesBefore": {
      "type": "integer",
      "nullable": true
     }
    }
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "Point": {
  "type": "object",
  "required": [
   "x",
   "y"
  ],
  "properties": {
   "x": {
    "type": "number"
   },
   "y": {
    "type": "number"
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
    "description": "**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overridable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire, removed from the table** — a client should not walk a hierarchy to read a figure, and the database should not hold nine million copies of AED. Four tables genuinely differ from their region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, `ledger.account`, `control.partner_agreement`.\n"
   },
   "currencyScale": {
    "type": "integer",
    "minimum": 0,
    "maximum": 4,
    "x-ticvai-persisted": false,
    "description": "**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overridable below, so a row in a UAE region is AED and cannot be anything else — storing it per row is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a client reading a figure should not walk a hierarchy to know what it means, and the database should not hold nine million copies of AED. Four tables genuinely differ from their region and keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.account`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a workstation with its own currency is a misconfiguration.**\n"
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
 "PricingDynamicPriceAction": {
  "type": "object",
  "x-ticvai-persistence": "pricing.dynamic_price_action",
  "description": "**Taken from the backend workbook, 20 September.** Configurable dynamic pricing component for dynamic price action.",
  "required": [
   "dynamicPriceRuleId",
   "type",
   "value"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "dynamicPriceRuleId": {
    "type": "string",
    "format": "uuid"
   },
   "type": {
    "type": "string",
    "maxLength": 30
   },
   "value": {
    "type": "number"
   },
   "minPrice": {
    "type": "number",
    "nullable": true
   },
   "maxPrice": {
    "type": "number",
    "nullable": true
   }
  }
 },
 "PricingDynamicPriceCondition": {
  "type": "object",
  "x-ticvai-persistence": "pricing.dynamic_price_condition",
  "description": "**Taken from the backend workbook, 20 September.** Configurable dynamic pricing component for dynamic price rule condition.",
  "required": [
   "actionId",
   "dynamicPriceRuleId",
   "type",
   "ruleOperator",
   "valueJson",
   "sequenceNo"
  ],
  "properties": {
   "actionId": {
    "type": "string",
    "format": "uuid"
   },
   "dynamicPriceRuleId": {
    "type": "string",
    "format": "uuid"
   },
   "type": {
    "type": "string",
    "maxLength": 50
   },
   "ruleOperator": {
    "type": "string",
    "maxLength": 20
   },
   "valueJson": {
    "type": "string"
   },
   "sequenceNo": {
    "type": "integer"
   }
  }
 },
 "PricingDynamicPriceRule": {
  "type": "object",
  "x-ticvai-persistence": "pricing.dynamic_price_rule",
  "description": "**Taken from the backend workbook, 20 September.** Configurable dynamic pricing component for dynamic price rule.",
  "required": [
   "pricingRuleCode",
   "name",
   "priority",
   "isActive"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "pricingRuleCode": {
    "type": "string",
    "maxLength": 100
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "productId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "priceListId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "scopePath": {
    "type": "string",
    "nullable": true
   },
   "channelId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "priority": {
    "type": "integer"
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
   "isActive": {
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
    "description": "**The consent questions a guest answers when booking this product**, in the order they are asked (decided 29 September, rev 3 REV3-26): *Are you able to swim?*, *Do you hold a scuba certification?*, *I accept the risk*. Each id names a consent question defined in marketing-crm (`ConsentQuestion`), which owns the text, its version and whether it is asked per person or once per booking; the answer is stored there as a consent record (question version, answer, who answered, when). **One question or several, as the venue chooses.** A flow can carry its own list too (`white-label.BookingFlowConfig.consentQuestionIds`, per venue through `venueOverrides`); a booking asks the union of the flow's questions and those of every product in the cart, each question once (`orders.Cart.consentQuestions`). An id that names no active consent question of the tenant is a `422`.\n"
   },
   "requiresTimeWindow": {
    "type": "boolean",
    "default": false,
    "description": "**True for a space sold by the hour**, e.g. a meeting room type (decided 29 September, rev 3 REV3-13). The product is the room type (*focus pod*, *majlis*, *boardroom*, *auditorium*), never a named room; its lengths are a `length` axis (`setProductAttributes`) whose values carry `durationMinutes`, and each length is a variant priced on its own in the price list, so price is the room rate for that length. The cart line carries the booked start and end (orders), the end being the start plus the chosen variant's `durationMinutes`; `resources.listProductStartTimes` supplies the start times for a variant and a date and `allocateResources` picks the room from the product's resource requirements (`setExperienceResourceRequirements`) at checkout. True requires every active variant to have a `durationMinutes`; otherwise `422`.\n"
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
   "name": {
    "type": "string",
    "maxLength": 150,
    "nullable": true,
    "description": "**Taken from their variant tables, 20 September.** `axisValues` gives `{size: L}` and no string a guest can read. A menu showing *Large* needs somewhere for the word to live.\n"
   },
   "barcode": {
    "type": "string",
    "maxLength": 64,
    "nullable": true,
    "description": "**Taken from their variant tables, 20 September.** `catalogue.alternative_code` is a partner's own code for a variant and **requires `partnerId`**, so a manufacturer's EAN had nowhere to go. One per variant against many per variant is a different cardinality and belongs in a different place — and a POS scan should be an indexed column lookup, not a join.\n"
   },
   "isDefault": {
    "type": "boolean",
    "default": false,
    "description": "Taken from their variant tables. Which variant a product page opens on. Ours had no way to say, so a three-size drink opened on whichever row sorted first.\n"
   },
   "isActive": {
    "type": "boolean",
    "description": "False when retired. Retired variants are never deleted — orders reference them."
   },
   "description": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "nullable": true,
    "description": "**Who this ticket type is for and what it includes**, shown behind the (i) on each Adult, Child, Senior or Infant row (decided 29 September, 23SEP-6). Each language value at most 300 characters; longer is a `400`. Set with `updateProductVariant`. Whether the guest screen shows it is `BookingFlowConfig.cardInfo` (white-label).\n"
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
    "description": "Empty or absent matches every channel.",
    "items": {
     "$ref": "../shared/common.yaml#/components/schemas/SalesChannel"
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
       "$ref": "../shared/common.yaml#/components/schemas/SalesChannel"
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
    "description": "**Open on purpose; the shape is `columns`.** Each row is keyed by `columns[].key`, and each value is of that column's `type` — money as a `Money`, dates, date-times and uuids as strings. A report's columns are chosen at run time, so no fixed schema can name them.\n",
    "items": {
     "type": "object",
     "additionalProperties": true
    }
   },
   "totals": {
    "type": "object",
    "additionalProperties": true,
    "description": "Aggregated columns only, keyed and typed as a row is."
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
    "additionalProperties": true,
    "description": "**Open on purpose; its shape is the report's.** Keyed by `ReportParameter.key` of the definition being run, each value of that parameter's `type`. An `isRequired` parameter with no value here and no `defaultValue` is the `400` `runReport` lists.\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "description": "Narrows to one venue. Omitting it returns everything the caller's scope permits — it cannot be used to reach beyond that.\n"
   },
   "dateFrom": {
    "type": "string",
    "format": "date",
    "description": "Defaults to today in the venue's time zone when not sent (decided 28 September, audit R158)."
   },
   "dateTo": {
    "type": "string",
    "format": "date",
    "description": "Defaults to today in the venue's time zone when not sent (audit R158)."
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
   "renderMode",
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
   "renderMode": {
    "type": "string",
    "enum": [
     "graphical",
     "list"
    ],
    "description": "The mode the server actually used. With `mode=auto` this is how a client knows what it got: `list` means the map has no geometry (the seat map's `noGeometry` state), so the client sells from categories and best-available groups and does not draw a plan. `graphical` means every seat carries `position`.\n"
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
   "sections": {
    "type": "array",
    "description": "The map's sections with what a guest screen needs to show the view from each (decided 29 September, rev 3 23SEP-14): the photo where the venue supplied one, otherwise null and the client renders the view from `boundary` and the seat positions. In this response so WEB-007 and GST-049 need no second call.\n",
    "items": {
     "type": "object",
     "required": [
      "code",
      "name"
     ],
     "properties": {
      "code": {
       "type": "string"
      },
      "name": {
       "type": "string"
      },
      "viewAssetId": {
       "type": "string",
       "format": "uuid",
       "nullable": true,
       "description": "As `Section.viewAssetId`. Null means render the view from geometry."
      },
      "boundary": {
       "type": "array",
       "nullable": true,
       "items": {
        "$ref": "#/components/schemas/Point"
       },
       "description": "As `Section.boundary`. Null when `renderMode` is `list`."
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
      },
      "displayLabel": {
       "type": "string",
       "description": "What the guest sees, e.g. `A2-7-11`, as on `Seat`."
      },
      "position": {
       "allOf": [
        {
         "$ref": "#/components/schemas/Point"
        }
       ],
       "nullable": true,
       "description": "The seat's coordinates on the map, as on `Seat`. Present when `renderMode` is `graphical`; null when it is `list`."
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
   "channels": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/Channel"
    }
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
 "Voucher": {
  "x-ticvai-persistence": "promotions.voucher",
  "type": "object",
  "required": [
   "code",
   "batchId",
   "faceValue",
   "balance",
   "status"
  ],
  "properties": {
   "code": {
    "type": "string"
   },
   "batchId": {
    "type": "string",
    "format": "uuid"
   },
   "faceValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "balance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "status": {
    "type": "string",
    "enum": [
     "issued",
     "partiallyRedeemed",
     "redeemed",
     "expired",
     "voided"
    ]
   },
   "validTo": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "VoucherBatch": {
  "x-ticvai-persistence": "promotions.voucher_batch",
  "allOf": [
   {
    "$ref": "#/components/schemas/CreateVoucherBatchRequest"
   },
   {
    "type": "object",
    "required": [
     "id",
     "issuedCount",
     "redeemedValue",
     "outstandingLiability"
    ],
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid"
     },
     "issuedCount": {
      "type": "integer"
     },
     "redeemedValue": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "outstandingLiability": {
      "allOf": [
       {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      ],
      "description": "Unredeemed value. A liability until redeemed or expired."
     }
    }
   }
  ]
 },
 "WaitlistEntry": {
  "type": "object",
  "x-ticvai-persistence": "catalogue.waitlist_entry",
  "required": [
   "performanceId",
   "partySize"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "performanceId": {
    "type": "string",
    "format": "uuid"
   },
   "variantId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "contactPoint": {
    "type": "string",
    "description": "**Where the offer goes.** An entry with no way to reach the guest is an entry that can never be honoured, so this is required even for an anonymous guest.\n"
   },
   "partySize": {
    "type": "integer",
    "minimum": 1
   },
   "status": {
    "allOf": [
     {
      "$ref": "#/components/schemas/WaitlistStatus"
     }
    ],
    "readOnly": true,
    "description": "Set by the server. `joinWaitlist` does not take it; a new entry is `waiting`."
   },
   "position": {
    "type": "integer",
    "readOnly": true,
    "description": "First in, first offered. Shown to the guest, because not knowing is worse than waiting."
   },
   "offeredAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "offerExpiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "description": "**The offer moves on when this passes.** Notifying everyone at once produces a race the fastest guest wins; holding indefinitely for someone asleep leaves the seat unsold.\n"
   },
   "joinedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "WaitlistStatus": {
  "type": "string",
  "enum": [
   "waiting",
   "offered",
   "converted",
   "expired",
   "left"
  ]
 }
}
```
