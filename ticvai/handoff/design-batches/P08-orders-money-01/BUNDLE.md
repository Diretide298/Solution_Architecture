# P08-orders-money-01 — P08 · Orders & Money (1 of 3)

**10 screens · 69 operations · 78 schemas · 29 permissions**

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

- **Every control that can be refused must be gated.** 29 permissions apply here:
  `ASSET_LIBRARY_MANAGE, ASSET_LIBRARY_VIEW, CASH_LIFT, CASH_NO_SALE, GUEST_VIEW, LEDGER_POST, ORDER_CREATE, ORDER_DISCOUNT, ORDER_EXCHANGE, ORDER_MODIFY, ORDER_REFUND, ORDER_REPRINT`…. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-008` | Product Detail & Variants | listDetail | 11 | 3 | — |
| `BO-022` | Order Detail | listDetail | 14 | 9 | — |
| `BO-023` | Refunds & Exchanges | listDetail | 15 | 9 | — |
| `BO-024` | Payment Exceptions | configEditor | 6 | 4 | — |
| `BO-025` | Chargebacks & Disputes | listDetail | 5 | 2 | — |
| `BO-026` | Group Bookings | listDetail | 17 | 11 | — |
| `BO-027` | Reissue & Media Replacement | statusTracker | 6 | 2 | — |
| `BO-028` | Refund Approval Queue | configEditor | 1 | 0 | — |
| `BO-029` | Report Builder | listDetail | 9 | 6 | — |
| `BO-039` | Shift Directory | approvalInbox | 13 | 9 | — |

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-008",
  "name": "Product Detail & Variants",
  "module": "Orders & Money",
  "requiresModule": "ticketing",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/product-detail-variants",
   "component": "apps/venue-management-web/src/routes/venue-operations/ProductDetailVariantsDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-007"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "BO-007",
     "trigger": "Product Directory",
     "provenance": "flow F85 step 3→4, F93 step 3→4",
     "carries": [
      "productId"
     ]
    }
   ],
   "entryFrom": [
    "BO-045",
    "BO-137"
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Carried `runFxRevaluation`, `getForeignTenderReport` and `listInterEntityObligations` until 20 August** — a product screen doing foreign-exchange revaluation. Operations were attached from the 14 August wireframe board by a heuristic that matched nothing. **Rewired 20 August.**",
  "density": "compact",
  "boardFrames": [
   "FnB Board 2.dc.html#fnb-2d",
   "Retail Board 2.dc.html#ret-2c"
  ],
  "pattern": "listDetail",
  "patternReason": "`listProductVariants` reads the population and `getProduct` reads one of them — list, select, act",
  "purpose": "Define what is sold and the ticket types under it.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every product variant",
       "bindsTo": "ProductVariant",
       "columns": [
        "ProductVariant.id",
        "ProductVariant.productId",
        "ProductVariant.sku",
        "ProductVariant.axisValues",
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
       "label": "The selected product variant",
       "bindsTo": "ProductVariant",
       "columns": [
        "ProductVariant.id",
        "ProductVariant.productId",
        "ProductVariant.sku",
        "ProductVariant.axisValues",
        "ProductVariant.name",
        "ProductVariant.barcode",
        "ProductVariant.description",
        "ProductVariant.isDefault",
        "ProductVariant.isActive"
       ],
       "operation": "listProductVariants",
       "provenance": "contract catalogue.yaml GET /products/{productId}/variants"
      },
      {
       "kind": "detailPanel",
       "label": "The product",
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
        "Product.categoryId",
        "Product.lifecycleState",
        "Product.isSellable",
        "Product.isStockTracked"
       ],
       "operation": "getProduct",
       "provenance": "contract catalogue.yaml GET /products/{productId}"
      },
      {
       "kind": "detailPanel",
       "label": "What the guest sees",
       "bindsTo": "Product",
       "columns": [
        "Product.guestListing",
        "Product.notBookableLabel",
        "Product.displayTags",
        "Product.media",
        "Product.consentQuestionIds",
        "Product.requiresTimeWindow",
        "Product.segmentTags"
       ],
       "operation": "getProduct",
       "notes": "**What the guest sees of the product** (decided 29 September, rev 3). `guestListing`: bookable (the default), info only, or hidden; an info-only product keeps its details and photo, shows `notBookableLabel` (default \"Info only / Not bookable online\") and opens details instead of Add to basket, and `addCartLine` refuses it `409` (REV3-14). `displayTags`: up to six, each a kind (clock, height, free, calendar, id) and a label; with none, the guest app derives them from duration, validity and the height rule (23SEP-3). `media`: images and videos from the asset library, one of them primary, which is the photo on the ticket card and what Read more opens on (23SEP-4). `consentQuestionIds`: the consent questions this product asks, in order, from CMS-018 (REV3-26). `requiresTimeWindow`: a space sold by the hour, such as a meeting-room type; its lengths are a `length` attribute whose values carry `durationMinutes` (REV3-13).",
       "provenance": "contract catalogue.yaml GET /products/{productId}"
      },
      {
       "kind": "multiSelect",
       "label": "Photos and videos",
       "bindsTo": "Product.media",
       "operation": "searchMedia",
       "notes": "Picks from the asset library (`searchMedia`); one item is marked primary. Saved with `updateProduct`, which registers the use of each asset (decided 29 September, rev 3 23SEP-4).",
       "provenance": "contract assets.yaml GET /media"
      },
      {
       "kind": "multiSelect",
       "label": "Consent questions this product asks",
       "bindsTo": "Product.consentQuestionIds",
       "operation": "listConsentQuestions",
       "notes": "Active questions from `listConsentQuestions`, written on CMS-018; ordered as the guest meets them. The guest is asked these together with the booking flow's own, each once (decided 29 September, rev 3 REV3-26).",
       "provenance": "contract marketing-crm.yaml GET /consent-questions"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save product attributes",
       "operation": "setProductAttributes",
       "provenance": "contract catalogue.yaml PUT /products/{productId}/attributes"
      },
      {
       "kind": "secondaryButton",
       "label": "Save product",
       "operation": "updateProduct",
       "provenance": "contract catalogue.yaml PATCH /products/{productId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Save ticket type",
       "operation": "updateProductVariant",
       "notes": "**The words and codes on one variant**: its name, the description a guest reads behind the (i) on a ticket-type row (at most 300 characters per language, decided 29 September, rev 3 23SEP-6), its barcode, and whether it is the default. The combination of values and the SKU come from the attributes and are not edited here. A retired variant is refused `409`.",
       "provenance": "contract catalogue.yaml PATCH /products/{productId}/variants/{variantId}"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The product variants list.",
   "error": "Could not load. Names which read failed and leaves the product variants untouched.",
   "emptyFirstRun": "No product variants yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Never shown: `listProductVariants` takes no filter, so an empty list is always the first-run state above.",
   "emptyNoAccess": "Shown when the caller lacks `PRODUCT_VIEW`, which `getProduct` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getProduct",
    "contract": "catalogue",
    "purpose": "Read a product",
    "trigger": "onLoad"
   },
   {
    "operationId": "listProductVariants",
    "contract": "catalogue",
    "purpose": "List generated variants",
    "trigger": "onLoad"
   },
   {
    "operationId": "setProductAttributes",
    "contract": "catalogue",
    "purpose": "Set the attribute axes for a product",
    "trigger": "onAction",
    "invalidates": [
     "listProductVariants"
    ]
   },
   {
    "operationId": "updateProduct",
    "contract": "catalogue",
    "purpose": "Update a product",
    "trigger": "onAction",
    "invalidates": [
     "listProductVariants"
    ]
   },
   {
    "operationId": "updateProductVariant",
    "contract": "catalogue",
    "purpose": "Name, describe, barcode or make default one ticket type (rev 3 23SEP-6)",
    "trigger": "onAction",
    "invalidates": [
     "listProductVariants"
    ]
   },
   {
    "operationId": "searchMedia",
    "contract": "assets",
    "purpose": "Pick the product's photos and videos from the asset library (rev 3 23SEP-4)",
    "trigger": "onAction"
   },
   {
    "operationId": "listConsentQuestions",
    "contract": "marketing-crm",
    "purpose": "The consent questions a product can ask (rev 3 REV3-26)",
    "trigger": "onAction"
   },
   {
    "operationId": "restoreProductVersion",
    "contract": "catalogue",
    "purpose": "Put a previous version of the product back",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "getProduct",
     "listProductVariants"
    ]
   },
   {
    "operationId": "assessProductChange",
    "contract": "catalogue",
    "purpose": "See what a change would touch before making it",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "getProduct",
     "listProductVariants"
    ]
   },
   {
    "operationId": "cloneProduct",
    "contract": "catalogue",
    "purpose": "Copy the product as a new draft",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "getProduct",
     "listProductVariants"
    ]
   },
   {
    "operationId": "listProductVersions",
    "contract": "catalogue",
    "purpose": "The product versions a restore picks from",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    },
    {
     "name": "productId",
     "from": "deepLink"
    },
    {
     "name": "variantId",
     "from": "navigation"
    },
    {
     "name": "version",
     "from": "navigation"
    }
   ],
   "coldEntry": "A product opened from the directory or a shared link. Shows what replaced it where it retired.",
   "preloaded": [
    "ProductVariant.id",
    "ProductVariant.productId",
    "ProductVariant.sku",
    "ProductVariant.axisValues",
    "ProductVariant.name"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-008",
   "derivedFrom": "wireframes/reference/Retail Board 2.dc.html",
   "source": "Claude Design Retail pack, 24 August",
   "note": "**Drawn by Claude Design on `Retail Board 2.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formSetProductAttributes",
    "component": "modal",
    "trigger": "Save product attributes",
    "body": "**Collects what `setProductAttributes` sends before it is called.** Required: `axes`. **A meeting-room type sells by length**: a `length` axis whose values each carry `durationMinutes` (e.g. 60, 120, 240, 480; minimum 15), one such axis per product, on a product with `requiresTimeWindow` on; each length is a variant priced on its own (decided 29 September, rev 3 REV3-13). Dismissing sends nothing; the screen behind is unchanged.",
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
    "id": "formUpdateProduct",
    "component": "modal",
    "trigger": "Save product",
    "body": "**Collects what `updateProduct` sends before it is called.** Nothing in the body is required. Optional: `name`, `description`, `channels`, `dataMaskValues`, and what the guest sees (decided 29 September, rev 3): `guestListing` and `notBookableLabel` (REV3-14), `displayTags` (at most six, 23SEP-3), `media` (23SEP-4), `consentQuestionIds` (REV3-26) and `requiresTimeWindow` (REV3-13). Dismissing sends nothing; the screen behind is unchanged.",
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
    "id": "formUpdateProductVariant",
    "component": "modal",
    "trigger": "Save ticket type",
    "body": "**Collects what `updateProductVariant` sends before it is called.** Nothing in the body is required. Optional: `name`, `description` (who the ticket type is for and what it includes, at most 300 characters per language, shown behind the (i) when the booking flow has `cardInfo` on; decided 29 September, rev 3 23SEP-6), `barcode`, `isDefault` (setting it clears the default on the product's other variants). Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save ticket type",
     "operation": "updateProductVariant"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "name",
      "description",
      "barcode",
      "isDefault"
     ]
    },
    "provenance": "contract catalogue.yaml PATCH /products/{productId}/variants/{variantId}"
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
  "id": "BO-022",
  "name": "Order Detail",
  "module": "Orders & Money",
  "requiresModule": "ticketing",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/order-detail",
   "component": "apps/venue-management-web/src/routes/venue-operations/OrderDetailDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-008"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "provenance": "derived — BO-008 declares entryState.params productId, variantId, version and BO-022 holds none of them, so the edge carries nothing and BO-008 opens cold"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listOrders` reads the population and `getOrder` reads one of them — list, select, act",
  "purpose": "See everything about one order in one place.",
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
       "operation": "listOrders",
       "notes": "Sends `?venueId=` to `listOrders`.",
       "provenance": "contract orders.yaml GET /orders"
      },
      {
       "kind": "textField",
       "label": "Principal id",
       "operation": "listOrders",
       "notes": "Sends `?principalId=` to `listOrders`.",
       "provenance": "contract orders.yaml GET /orders"
      },
      {
       "kind": "textField",
       "label": "Shift id",
       "operation": "listOrders",
       "notes": "Sends `?shiftId=` to `listOrders`.",
       "provenance": "contract orders.yaml GET /orders"
      },
      {
       "kind": "textField",
       "label": "Status",
       "operation": "listOrders",
       "notes": "Sends `?status=` to `listOrders`.",
       "provenance": "contract orders.yaml GET /orders"
      },
      {
       "kind": "datePicker",
       "label": "Created from",
       "operation": "listOrders",
       "notes": "Sends `?createdFrom=` to `listOrders`.",
       "provenance": "contract orders.yaml GET /orders"
      },
      {
       "kind": "datePicker",
       "label": "Created to",
       "operation": "listOrders",
       "notes": "Sends `?createdTo=` to `listOrders`.",
       "provenance": "contract orders.yaml GET /orders"
      },
      {
       "kind": "dataTable",
       "label": "Every order",
       "bindsTo": "OrderSummary",
       "columns": [
        "OrderSummary.id",
        "OrderSummary.orderNumber",
        "OrderSummary.status",
        "OrderSummary.grossAmount",
        "OrderSummary.refundedAmount",
        "OrderSummary.channel",
        "OrderSummary.lineCount"
       ],
       "operation": "listOrders",
       "provenance": "contract orders.yaml GET /orders"
      },
      {
       "kind": "dataTable",
       "label": "Every refund",
       "bindsTo": "Refund",
       "columns": [
        "Refund.id",
        "Refund.orderId",
        "Refund.batchId",
        "Refund.fxRate",
        "Refund.taxReversalEntryId",
        "Refund.settleTo",
        "Refund.fxVariance",
        "Refund.amount",
        "Refund.appliedPercentage",
        "Refund.status",
        "Refund.reason",
        "Refund.requestedByPrincipalId"
       ],
       "operation": "listOrderRefunds",
       "provenance": "contract orders.yaml GET /orders/{orderId}/refunds"
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
       "label": "The selected order",
       "bindsTo": "OrderSummary",
       "columns": [
        "OrderSummary.id",
        "OrderSummary.orderNumber",
        "OrderSummary.status",
        "OrderSummary.grossAmount",
        "OrderSummary.refundedAmount",
        "OrderSummary.channel",
        "OrderSummary.lineCount",
        "OrderSummary.principalId",
        "OrderSummary.holdLabel",
        "OrderSummary.heldUntil"
       ],
       "operation": "listOrders",
       "provenance": "contract orders.yaml GET /orders"
      },
      {
       "kind": "detailPanel",
       "label": "The order statement",
       "bindsTo": "OrderStatement",
       "columns": [
        "OrderStatement.orderId",
        "OrderStatement.orderNumber",
        "OrderStatement.currency",
        "OrderStatement.currencyScale",
        "OrderStatement.entries",
        "OrderStatement.totalPaid",
        "OrderStatement.totalRefunded",
        "OrderStatement.currentBalance"
       ],
       "operation": "getOrderStatement",
       "provenance": "contract orders.yaml GET /orders/{orderId}/statement"
      },
      {
       "kind": "detailPanel",
       "label": "The order",
       "bindsTo": "Order",
       "columns": [
        "Order.id",
        "Order.orderNumber",
        "Order.channel",
        "Order.venueId",
        "Order.scopePath",
        "Order.status",
        "Order.currency",
        "Order.currencyScale",
        "Order.grossAmount",
        "Order.taxAmount",
        "Order.netAmount",
        "Order.refundedAmount",
        "Order.totalPriceVariance",
        "Order.lines",
        "Order.payments",
        "Order.principalId"
       ],
       "operation": "getOrder",
       "provenance": "contract orders.yaml GET /orders/{orderId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create order",
       "operation": "createOrder",
       "provenance": "contract orders.yaml POST /orders"
      },
      {
       "kind": "secondaryButton",
       "label": "Apply manual discount",
       "operation": "applyManualDiscount",
       "provenance": "contract orders.yaml POST /orders/{orderId}/discounts"
      },
      {
       "kind": "secondaryButton",
       "label": "Create refund",
       "operation": "createRefund",
       "provenance": "contract orders.yaml POST /orders/{orderId}/refunds"
      },
      {
       "kind": "secondaryButton",
       "label": "Exchange order lines",
       "operation": "exchangeOrderLines",
       "provenance": "contract orders.yaml POST /orders/{orderId}/exchanges"
      },
      {
       "kind": "secondaryButton",
       "label": "Hold order",
       "operation": "holdOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/hold"
      },
      {
       "kind": "secondaryButton",
       "label": "Modify order",
       "operation": "modifyOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/modify"
      },
      {
       "kind": "secondaryButton",
       "label": "Reprint order",
       "operation": "reprintOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/reprints"
      },
      {
       "kind": "secondaryButton",
       "label": "Reschedule order",
       "operation": "rescheduleOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/reschedule"
      },
      {
       "kind": "secondaryButton",
       "label": "Resume order",
       "operation": "resumeOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/resume"
      },
      {
       "kind": "destructiveButton",
       "label": "Void order",
       "operation": "voidOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/voids"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmVoidOrder",
    "component": "confirmDialog",
    "trigger": "Void order",
    "body": "**Names what `voidOrder` changes and what it leaves alone**, in the consequence rather than the verb. A order this affects should be identified in the dialog, not just counted. **Collects what `voidOrder` sends before it is called.** Required: `id`, `reason`, `recordedAt`. `reason` is the void reason list (`VoidReason`: guestChangedMind, enteredInError, itemUnavailable, qualityIssue, duplicate, other); **choosing Other makes `note` required** (decided 28 September, audit R125 (4), R222).",
    "provenance": "contract orders.yaml POST /orders/{orderId}/voids"
   },
   {
    "id": "formCreateOrder",
    "component": "modal",
    "trigger": "Create order",
    "body": "**Collects what `createOrder` sends before it is called.** Required: `id`, `venueId`, `channel`, `lines`, `recordedAt`. Optional: `shiftId`, `subjectId`, `guestLinkId`, `catalogueBundleVersion`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateOrderRequest",
    "confirm": {
     "label": "Create order",
     "operation": "createOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "venueId",
      "channel",
      "lines",
      "recordedAt",
      "shiftId",
      "subjectId",
      "guestLinkId",
      "catalogueBundleVersion"
     ]
    },
    "provenance": "contract orders.yaml POST /orders"
   },
   {
    "id": "formApplyManualDiscount",
    "component": "modal",
    "trigger": "Apply manual discount",
    "body": "**Collects what `applyManualDiscount` sends before it is called.** Required: `id`, `reason`, `recordedAt`. Optional: `lineId`, `amount`, `percentage`, `reasonCode`, `approverPrincipalId`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "ManualDiscountRequest",
    "confirm": {
     "label": "Apply manual discount",
     "operation": "applyManualDiscount"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "reason",
      "recordedAt",
      "lineId",
      "amount",
      "percentage",
      "reasonCode",
      "approverPrincipalId"
     ]
    },
    "provenance": "contract orders.yaml POST /orders/{orderId}/discounts"
   },
   {
    "id": "formCreateRefund",
    "component": "modal",
    "trigger": "Create refund",
    "body": "**Collects what `createRefund` sends before it is called.** Required: `id`, `amount`, `reason`, `recordedAt`. Optional: `lineIds`, `secondaryAuthorisation`, `refundToOriginalTender`, `alternateTender`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateRefundRequest",
    "confirm": {
     "label": "Create refund",
     "operation": "createRefund"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "amount",
      "reason",
      "recordedAt",
      "lineIds",
      "secondaryAuthorisation",
      "refundToOriginalTender",
      "alternateTender"
     ]
    },
    "provenance": "contract orders.yaml POST /orders/{orderId}/refunds"
   },
   {
    "id": "formExchangeOrderLines",
    "component": "modal",
    "trigger": "Exchange order lines",
    "body": "**Collects what `exchangeOrderLines` sends before it is called.** Required: `id`, `outgoingLineIds`, `incomingLines`, `recordedAt`. Optional: `waiveFee`, `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "ExchangeOrderRequest",
    "confirm": {
     "label": "Exchange order lines",
     "operation": "exchangeOrderLines"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "outgoingLineIds",
      "incomingLines",
      "recordedAt",
      "waiveFee",
      "reason"
     ]
    },
    "provenance": "contract orders.yaml POST /orders/{orderId}/exchanges"
   },
   {
    "id": "formHoldOrder",
    "component": "modal",
    "trigger": "Hold order",
    "body": "**Collects what `holdOrder` sends before it is called.** Required: `recordedAt`. Optional: `label`, `holdUntil`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Hold order",
     "operation": "holdOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "recordedAt",
      "label",
      "holdUntil"
     ]
    },
    "provenance": "contract orders.yaml POST /orders/{orderId}/hold"
   },
   {
    "id": "formModifyOrder",
    "component": "modal",
    "trigger": "Modify order",
    "body": "**Collects what `modifyOrder` sends before it is called.** Required: `id`, `recordedAt`. Optional: `addLines`, `removeLineIds`, `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "ModifyOrderRequest",
    "confirm": {
     "label": "Modify order",
     "operation": "modifyOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "recordedAt",
      "addLines",
      "removeLineIds",
      "reason"
     ]
    },
    "provenance": "contract orders.yaml POST /orders/{orderId}/modify"
   },
   {
    "id": "formReprintOrder",
    "component": "modal",
    "trigger": "Reprint order",
    "body": "**Collects what `reprintOrder` sends before it is called.** Required: `delivery`, `recordedAt`. Optional: `destination`, `lineIds`, `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Reprint order",
     "operation": "reprintOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "delivery",
      "recordedAt",
      "destination",
      "lineIds",
      "reason"
     ]
    },
    "provenance": "contract orders.yaml POST /orders/{orderId}/reprints"
   },
   {
    "id": "formRescheduleOrder",
    "component": "modal",
    "trigger": "Reschedule order",
    "body": "**Collects what `rescheduleOrder` sends before it is called.** Required: `targetPerformanceId`, `recordedAt`. Optional: `lineIds`, `waiveFee`, `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Reschedule order",
     "operation": "rescheduleOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "targetPerformanceId",
      "recordedAt",
      "lineIds",
      "waiveFee",
      "reason"
     ]
    },
    "provenance": "contract orders.yaml POST /orders/{orderId}/reschedule"
   }
  ],
  "states": {
   "loading": "The order list.",
   "error": "Could not load. Names which read failed and leaves the order untouched.",
   "emptyFirstRun": "No order yet. Offers Create order (`createOrder`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on venueId, principalId, shiftId, status, createdFrom, createdTo and the order are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `ORDER_VIEW`, which `listOrders` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listOrders",
    "contract": "orders",
    "purpose": "List orders",
    "trigger": "onLoad"
   },
   {
    "operationId": "getOrder",
    "contract": "orders",
    "purpose": "Read an order",
    "trigger": "onAction"
   },
   {
    "operationId": "createOrder",
    "contract": "orders",
    "purpose": "Create an order",
    "trigger": "onAction",
    "invalidates": [
     "listOrders"
    ]
   },
   {
    "operationId": "applyManualDiscount",
    "contract": "orders",
    "purpose": "Apply a discount a cashier chose",
    "trigger": "onAction",
    "invalidates": [
     "listOrders"
    ]
   },
   {
    "operationId": "createRefund",
    "contract": "orders",
    "purpose": "Refund an order, wholly or in part",
    "trigger": "onAction",
    "invalidates": [
     "listOrders"
    ]
   },
   {
    "operationId": "exchangeOrderLines",
    "contract": "orders",
    "purpose": "Exchange lines for different products or dates",
    "trigger": "onAction",
    "invalidates": [
     "listOrders"
    ]
   },
   {
    "operationId": "getOrderStatement",
    "contract": "orders",
    "purpose": "Full financial history of an order",
    "trigger": "onAction"
   },
   {
    "operationId": "holdOrder",
    "contract": "orders",
    "purpose": "Park a sale and free the till",
    "trigger": "onAction",
    "invalidates": [
     "listOrders"
    ]
   },
   {
    "operationId": "listOrderRefunds",
    "contract": "orders",
    "purpose": "List refunds against an order",
    "trigger": "onAction"
   },
   {
    "operationId": "modifyOrder",
    "contract": "orders",
    "purpose": "Add or remove lines on an existing order",
    "trigger": "onAction",
    "invalidates": [
     "listOrders"
    ]
   },
   {
    "operationId": "reprintOrder",
    "contract": "orders",
    "purpose": "Reprint or resend tickets",
    "trigger": "onAction",
    "invalidates": [
     "listOrders"
    ]
   },
   {
    "operationId": "rescheduleOrder",
    "contract": "orders",
    "purpose": "Move an order to another performance",
    "trigger": "onAction",
    "invalidates": [
     "listOrders"
    ]
   },
   {
    "operationId": "resumeOrder",
    "contract": "orders",
    "purpose": "Bring a parked sale back to a till",
    "trigger": "onAction",
    "invalidates": [
     "listOrders"
    ]
   },
   {
    "operationId": "voidOrder",
    "contract": "orders",
    "purpose": "Void an order",
    "trigger": "onAction",
    "invalidates": [
     "listOrders"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "orderId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A guest opening an order link weeks later.** Shows the order if it still resolves; if it was refunded or the performance passed, says which and offers the order list rather than an error.",
   "preloaded": [
    "OrderSummary.id",
    "OrderSummary.orderNumber",
    "OrderSummary.status",
    "OrderSummary.grossAmount",
    "OrderSummary.refundedAmount"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-022"
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
  "id": "BO-023",
  "name": "Refunds & Exchanges",
  "module": "Orders & Money",
  "requiresModule": "ticketing",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/refunds-exchanges",
   "component": "apps/venue-management-web/src/routes/venue-operations/RefundsExchangesDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-004",
    "BO-008"
   ],
   "inferred": true,
   "entryFrom": [
    "BO-002"
   ],
   "transitions": [
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "provenance": "derived — BO-008 declares entryState.params productId, variantId, version and BO-023 holds none of them, so the edge carries nothing and BO-008 opens cold"
    },
    {
     "to": "BO-004",
     "trigger": "Authorises the bulk refund",
     "provenance": "flow F09 step 3→4",
     "carries": [
      "refundId"
     ]
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **`getRefundPolicy` wired 24 August.** **A refunds screen that cannot read the refund policy** judges every request by memory — and F09 was reaching it through `BO-003 Queue Integration Setup`, which held the operation only because of the 18 August bulk attach.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listOrderRefunds` reads the population and `getOrder` reads one of them — list, select, act",
  "purpose": "Give money back, or move the booking.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every refund",
       "bindsTo": "Refund",
       "columns": [
        "Refund.id",
        "Refund.orderId",
        "Refund.fxRate",
        "Refund.taxReversalEntryId",
        "Refund.settleTo",
        "Refund.fxVariance",
        "Refund.amount",
        "Refund.appliedPercentage",
        "Refund.status",
        "Refund.reason",
        "Refund.requestedByPrincipalId",
        "Refund.secondaryPrincipalId"
       ],
       "operation": "listOrderRefunds",
       "provenance": "contract orders.yaml GET /orders/{orderId}/refunds"
      },
      {
       "kind": "dataTable",
       "label": "Every order",
       "bindsTo": "OrderSummary",
       "columns": [
        "OrderSummary.id",
        "OrderSummary.orderNumber",
        "OrderSummary.status",
        "OrderSummary.grossAmount",
        "OrderSummary.refundedAmount",
        "OrderSummary.channel",
        "OrderSummary.lineCount",
        "OrderSummary.principalId",
        "OrderSummary.holdLabel",
        "OrderSummary.heldUntil"
       ],
       "operation": "listOrders",
       "provenance": "contract orders.yaml GET /orders"
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
       "label": "The selected refund",
       "bindsTo": "Refund",
       "columns": [
        "Refund.id",
        "Refund.orderId",
        "Refund.batchId",
        "Refund.fxRate",
        "Refund.taxReversalEntryId",
        "Refund.settleTo",
        "Refund.fxVariance",
        "Refund.amount",
        "Refund.appliedPercentage",
        "Refund.status",
        "Refund.reason",
        "Refund.requestedByPrincipalId",
        "Refund.secondaryPrincipalId",
        "Refund.approvedByPrincipalId",
        "Refund.ledgerEntryId",
        "Refund.gatewayReference"
       ],
       "operation": "listOrderRefunds",
       "provenance": "contract orders.yaml GET /orders/{orderId}/refunds"
      },
      {
       "kind": "detailPanel",
       "label": "The order statement",
       "bindsTo": "OrderStatement",
       "columns": [
        "OrderStatement.orderId",
        "OrderStatement.orderNumber",
        "OrderStatement.currency",
        "OrderStatement.currencyScale",
        "OrderStatement.entries",
        "OrderStatement.totalPaid",
        "OrderStatement.totalRefunded",
        "OrderStatement.currentBalance"
       ],
       "operation": "getOrderStatement",
       "provenance": "contract orders.yaml GET /orders/{orderId}/statement"
      },
      {
       "kind": "detailPanel",
       "label": "The refund policy",
       "bindsTo": "RefundPolicy",
       "columns": [
        "RefundPolicy.id",
        "RefundPolicy.venueId",
        "RefundPolicy.selfAuthoriseLimit",
        "RefundPolicy.requiresSecondUserAbove",
        "RefundPolicy.requiresApprovalAbove",
        "RefundPolicy.timeBands",
        "RefundPolicy.allowPartial",
        "RefundPolicy.refundWindowDays",
        "RefundPolicy.varianceThreshold"
       ],
       "operation": "getRefundPolicy",
       "provenance": "contract orders.yaml GET /venues/{venueId}/refund-policy"
      },
      {
       "kind": "detailPanel",
       "label": "The order",
       "bindsTo": "Order",
       "columns": [
        "Order.id",
        "Order.orderNumber",
        "Order.channel",
        "Order.venueId",
        "Order.scopePath",
        "Order.status",
        "Order.currency",
        "Order.currencyScale",
        "Order.grossAmount",
        "Order.taxAmount",
        "Order.netAmount",
        "Order.refundedAmount",
        "Order.totalPriceVariance",
        "Order.lines",
        "Order.payments",
        "Order.principalId"
       ],
       "operation": "getOrder",
       "provenance": "contract orders.yaml GET /orders/{orderId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create refund",
       "operation": "createRefund",
       "provenance": "contract orders.yaml POST /orders/{orderId}/refunds"
      },
      {
       "kind": "secondaryButton",
       "label": "Apply manual discount",
       "operation": "applyManualDiscount",
       "provenance": "contract orders.yaml POST /orders/{orderId}/discounts"
      },
      {
       "kind": "secondaryButton",
       "label": "Create order",
       "operation": "createOrder",
       "provenance": "contract orders.yaml POST /orders"
      },
      {
       "kind": "secondaryButton",
       "label": "Exchange order lines",
       "operation": "exchangeOrderLines",
       "provenance": "contract orders.yaml POST /orders/{orderId}/exchanges"
      },
      {
       "kind": "secondaryButton",
       "label": "Hold order",
       "operation": "holdOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/hold"
      },
      {
       "kind": "secondaryButton",
       "label": "Modify order",
       "operation": "modifyOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/modify"
      },
      {
       "kind": "secondaryButton",
       "label": "Reprint order",
       "operation": "reprintOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/reprints"
      },
      {
       "kind": "secondaryButton",
       "label": "Reschedule order",
       "operation": "rescheduleOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/reschedule"
      },
      {
       "kind": "secondaryButton",
       "label": "Resume order",
       "operation": "resumeOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/resume"
      },
      {
       "kind": "destructiveButton",
       "label": "Void order",
       "operation": "voidOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/voids"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmVoidOrder",
    "component": "confirmDialog",
    "trigger": "Void order",
    "body": "**Names what `voidOrder` changes and what it leaves alone**, in the consequence rather than the verb. A refunds exchanges this affects should be identified in the dialog, not just counted. **Collects what `voidOrder` sends before it is called.** Required: `id`, `reason`, `recordedAt`. `reason` is the void reason list (`VoidReason`: guestChangedMind, enteredInError, itemUnavailable, qualityIssue, duplicate, other); **choosing Other makes `note` required** (decided 28 September, audit R125 (4), R222).",
    "provenance": "contract orders.yaml POST /orders/{orderId}/voids"
   },
   {
    "id": "formCreateRefund",
    "component": "modal",
    "trigger": "Create refund",
    "body": "**Collects what `createRefund` sends before it is called.** Required: `id`, `amount`, `reason`, `recordedAt`. Optional: `lineIds`, `secondaryAuthorisation`, `refundToOriginalTender`, `alternateTender`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateRefundRequest",
    "confirm": {
     "label": "Create refund",
     "operation": "createRefund"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "amount",
      "reason",
      "recordedAt",
      "lineIds",
      "secondaryAuthorisation",
      "refundToOriginalTender",
      "alternateTender"
     ]
    },
    "provenance": "contract orders.yaml POST /orders/{orderId}/refunds"
   },
   {
    "id": "formApplyManualDiscount",
    "component": "modal",
    "trigger": "Apply manual discount",
    "body": "**Collects what `applyManualDiscount` sends before it is called.** Required: `id`, `reason`, `recordedAt`. Optional: `lineId`, `amount`, `percentage`, `reasonCode`, `approverPrincipalId`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "ManualDiscountRequest",
    "confirm": {
     "label": "Apply manual discount",
     "operation": "applyManualDiscount"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "reason",
      "recordedAt",
      "lineId",
      "amount",
      "percentage",
      "reasonCode",
      "approverPrincipalId"
     ]
    },
    "provenance": "contract orders.yaml POST /orders/{orderId}/discounts"
   },
   {
    "id": "formCreateOrder",
    "component": "modal",
    "trigger": "Create order",
    "body": "**Collects what `createOrder` sends before it is called.** Required: `id`, `venueId`, `channel`, `lines`, `recordedAt`. Optional: `shiftId`, `subjectId`, `guestLinkId`, `catalogueBundleVersion`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateOrderRequest",
    "confirm": {
     "label": "Create order",
     "operation": "createOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "venueId",
      "channel",
      "lines",
      "recordedAt",
      "shiftId",
      "subjectId",
      "guestLinkId",
      "catalogueBundleVersion"
     ]
    },
    "provenance": "contract orders.yaml POST /orders"
   },
   {
    "id": "formExchangeOrderLines",
    "component": "modal",
    "trigger": "Exchange order lines",
    "body": "**Collects what `exchangeOrderLines` sends before it is called.** Required: `id`, `outgoingLineIds`, `incomingLines`, `recordedAt`. Optional: `waiveFee`, `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "ExchangeOrderRequest",
    "confirm": {
     "label": "Exchange order lines",
     "operation": "exchangeOrderLines"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "outgoingLineIds",
      "incomingLines",
      "recordedAt",
      "waiveFee",
      "reason"
     ]
    },
    "provenance": "contract orders.yaml POST /orders/{orderId}/exchanges"
   },
   {
    "id": "formHoldOrder",
    "component": "modal",
    "trigger": "Hold order",
    "body": "**Collects what `holdOrder` sends before it is called.** Required: `recordedAt`. Optional: `label`, `holdUntil`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Hold order",
     "operation": "holdOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "recordedAt",
      "label",
      "holdUntil"
     ]
    },
    "provenance": "contract orders.yaml POST /orders/{orderId}/hold"
   },
   {
    "id": "formModifyOrder",
    "component": "modal",
    "trigger": "Modify order",
    "body": "**Collects what `modifyOrder` sends before it is called.** Required: `id`, `recordedAt`. Optional: `addLines`, `removeLineIds`, `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "ModifyOrderRequest",
    "confirm": {
     "label": "Modify order",
     "operation": "modifyOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "recordedAt",
      "addLines",
      "removeLineIds",
      "reason"
     ]
    },
    "provenance": "contract orders.yaml POST /orders/{orderId}/modify"
   },
   {
    "id": "formReprintOrder",
    "component": "modal",
    "trigger": "Reprint order",
    "body": "**Collects what `reprintOrder` sends before it is called.** Required: `delivery`, `recordedAt`. Optional: `destination`, `lineIds`, `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Reprint order",
     "operation": "reprintOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "delivery",
      "recordedAt",
      "destination",
      "lineIds",
      "reason"
     ]
    },
    "provenance": "contract orders.yaml POST /orders/{orderId}/reprints"
   },
   {
    "id": "formRescheduleOrder",
    "component": "modal",
    "trigger": "Reschedule order",
    "body": "**Collects what `rescheduleOrder` sends before it is called.** Required: `targetPerformanceId`, `recordedAt`. Optional: `lineIds`, `waiveFee`, `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Reschedule order",
     "operation": "rescheduleOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "targetPerformanceId",
      "recordedAt",
      "lineIds",
      "waiveFee",
      "reason"
     ]
    },
    "provenance": "contract orders.yaml POST /orders/{orderId}/reschedule"
   }
  ],
  "states": {
   "loading": "The refunds exchanges list.",
   "error": "Could not load. Names which read failed and leaves the refunds exchanges untouched.",
   "emptyFirstRun": "No refunds exchanges yet. Offers Create refund (`createRefund`).",
   "emptyNoResults": "Never shown: `listOrderRefunds` takes no filter, so an empty list is always the first-run state above.",
   "emptyNoAccess": "Shown when the caller lacks `ORDER_VIEW`, which `listOrderRefunds` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listOrderRefunds",
    "contract": "orders",
    "purpose": "List refunds against an order",
    "trigger": "onAction"
   },
   {
    "operationId": "createRefund",
    "contract": "orders",
    "purpose": "Refund an order, wholly or in part",
    "trigger": "onAction",
    "invalidates": [
     "listOrderRefunds"
    ]
   },
   {
    "operationId": "applyManualDiscount",
    "contract": "orders",
    "purpose": "Apply a discount a cashier chose",
    "trigger": "onAction",
    "invalidates": [
     "listOrderRefunds"
    ]
   },
   {
    "operationId": "createOrder",
    "contract": "orders",
    "purpose": "Create an order",
    "trigger": "onAction",
    "invalidates": [
     "listOrderRefunds"
    ]
   },
   {
    "operationId": "exchangeOrderLines",
    "contract": "orders",
    "purpose": "Exchange lines for different products or dates",
    "trigger": "onAction",
    "invalidates": [
     "listOrderRefunds"
    ]
   },
   {
    "operationId": "getOrder",
    "contract": "orders",
    "purpose": "Read an order",
    "trigger": "onAction"
   },
   {
    "operationId": "getOrderStatement",
    "contract": "orders",
    "purpose": "Full financial history of an order",
    "trigger": "onAction"
   },
   {
    "operationId": "holdOrder",
    "contract": "orders",
    "purpose": "Park a sale and free the till",
    "trigger": "onAction",
    "invalidates": [
     "listOrderRefunds"
    ]
   },
   {
    "operationId": "listOrders",
    "contract": "orders",
    "purpose": "List orders",
    "trigger": "onLoad"
   },
   {
    "operationId": "modifyOrder",
    "contract": "orders",
    "purpose": "Add or remove lines on an existing order",
    "trigger": "onAction",
    "invalidates": [
     "listOrderRefunds"
    ]
   },
   {
    "operationId": "reprintOrder",
    "contract": "orders",
    "purpose": "Reprint or resend tickets",
    "trigger": "onAction",
    "invalidates": [
     "listOrderRefunds"
    ]
   },
   {
    "operationId": "rescheduleOrder",
    "contract": "orders",
    "purpose": "Move an order to another performance",
    "trigger": "onAction",
    "invalidates": [
     "listOrderRefunds"
    ]
   },
   {
    "operationId": "resumeOrder",
    "contract": "orders",
    "purpose": "Bring a parked sale back to a till",
    "trigger": "onAction",
    "invalidates": [
     "listOrderRefunds"
    ]
   },
   {
    "operationId": "voidOrder",
    "contract": "orders",
    "purpose": "Void an order",
    "trigger": "onAction",
    "invalidates": [
     "listOrderRefunds"
    ]
   },
   {
    "operationId": "getRefundPolicy",
    "contract": "orders",
    "purpose": "The policy this refund is judged against",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "orderId",
     "from": "deepLink"
    },
    {
     "name": "venueId",
     "from": "session"
    }
   ],
   "coldEntry": "**A guest opening an order link weeks later.** Shows the order if it still resolves; if it was refunded or the performance passed, says which and offers the order list rather than an error. **The venue comes from the session** — a back-office user works one venue at a time and the refund policy is a venue setting, so the policy read needs it. Added 24 August with `getRefundPolicy`.",
   "preloaded": [
    "Refund.id",
    "Refund.orderId",
    "Refund.batchId",
    "Refund.fxRate",
    "Refund.taxReversalEntryId"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-023"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 15 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "BO-024",
  "name": "Payment Exceptions",
  "module": "Orders & Money",
  "requiresModule": "ticketing",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/payment-exceptions",
   "component": "apps/venue-management-web/src/routes/venue-operations/PaymentExceptionsDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-008"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "provenance": "derived — BO-008 declares entryState.params productId, variantId, version and BO-024 holds none of them, so the edge carries nothing and BO-008 opens cold"
    },
    {
     "to": "PTR-014",
     "trigger": "Settlement & Payment History",
     "provenance": "flow F99 step 2→3",
     "crossesDevice": true,
     "back": false
    }
   ],
   "entryFrom": [
    "BO-025"
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. Payment exceptions across currencies. **The rate shown is the one stored on the payment, not today's** (CF-37) — an exception opened in March and worked in August is worked at March's rate, or the reconciliation will never close.",
  "density": "compact",
  "boardFrames": [
   "Retail Board 3.dc.html#ret-3k"
  ],
  "pattern": "configEditor",
  "patternReason": "the screen declares only writes (`createPayment`, `addTip`, `capturePayment`) and no read of a population — it is settings, not a list",
  "purpose": "Resolve payments that never resolved themselves.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "textField",
       "label": "id",
       "bindsTo": "CreatePaymentRequest.id",
       "provenance": "contract orders.yaml POST /payments"
      },
      {
       "kind": "textField",
       "label": "orderId",
       "bindsTo": "CreatePaymentRequest.orderId",
       "provenance": "contract orders.yaml POST /payments"
      },
      {
       "kind": "textField",
       "label": "tender",
       "bindsTo": "CreatePaymentRequest.tender",
       "provenance": "contract orders.yaml POST /payments"
      },
      {
       "kind": "textField",
       "label": "amount",
       "bindsTo": "CreatePaymentRequest.amount",
       "provenance": "contract orders.yaml POST /payments"
      },
      {
       "kind": "textField",
       "label": "tenderedAmount",
       "bindsTo": "CreatePaymentRequest.tenderAmount",
       "provenance": "contract orders.yaml POST /payments"
      },
      {
       "kind": "textField",
       "label": "walletAuthorisationId",
       "bindsTo": "CreatePaymentRequest.walletAuthorisationId",
       "provenance": "contract orders.yaml POST /payments"
      },
      {
       "kind": "textField",
       "label": "deviceId",
       "bindsTo": "CreatePaymentRequest.deviceId",
       "provenance": "contract orders.yaml POST /payments"
      },
      {
       "kind": "textField",
       "label": "recordedAt",
       "bindsTo": "CreatePaymentRequest.recordedAt",
       "provenance": "contract orders.yaml POST /payments"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create payment",
       "operation": "createPayment",
       "provenance": "contract orders.yaml POST /payments"
      },
      {
       "kind": "secondaryButton",
       "label": "Add tip",
       "operation": "addTip",
       "provenance": "contract orders.yaml POST /payments/{paymentId}/tip"
      },
      {
       "kind": "secondaryButton",
       "label": "Capture payment",
       "operation": "capturePayment",
       "provenance": "contract orders.yaml POST /payments/{paymentId}/capture"
      },
      {
       "kind": "secondaryButton",
       "label": "Inquire payment status",
       "operation": "inquirePaymentStatus",
       "provenance": "contract orders.yaml POST /payments/{paymentId}/inquiry"
      },
      {
       "kind": "destructiveButton",
       "label": "Close deposit boxes",
       "operation": "closeDepositBoxes",
       "provenance": "contract shift.yaml POST /deposit-boxes/close"
      },
      {
       "kind": "secondaryButton",
       "label": "Settle deposit",
       "operation": "settleDeposit",
       "provenance": "contract finance.yaml POST /deposits/{depositId}/settle"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmCloseDepositBoxes",
    "component": "confirmDialog",
    "trigger": "Close deposit boxes",
    "body": "**Names what `closeDepositBoxes` changes and what it leaves alone**, in the consequence rather than the verb. A payment exceptions this affects should be identified in the dialog, not just counted. **Collects what `closeDepositBoxes` sends before it is called.** Nothing in the body is required. Optional: `boxIds`, `allOpenAtVenue`.",
    "provenance": "contract shift.yaml POST /deposit-boxes/close"
   },
   {
    "id": "formAddTip",
    "component": "modal",
    "trigger": "Add tip",
    "body": "**Collects what `addTip` sends before it is called.** Required: `amount`, `source`, `recordedAt`. Optional: `allocateToPrincipalId`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Add tip",
     "operation": "addTip"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "amount",
      "source",
      "recordedAt",
      "allocateToPrincipalId"
     ]
    },
    "provenance": "contract orders.yaml POST /payments/{paymentId}/tip"
   },
   {
    "id": "formCapturePayment",
    "component": "modal",
    "trigger": "Capture payment",
    "body": "**Collects what `capturePayment` sends before it is called.** Required: `amount`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Capture payment",
     "operation": "capturePayment"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "amount"
     ]
    },
    "provenance": "contract orders.yaml POST /payments/{paymentId}/capture"
   },
   {
    "id": "formSettleDeposit",
    "component": "modal",
    "trigger": "Settle deposit",
    "body": "**Collects what `settleDeposit` sends before it is called.** Required: `outcome`. Optional: `amount`, `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Settle deposit",
     "operation": "settleDeposit"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "outcome",
      "amount",
      "reason"
     ]
    },
    "provenance": "contract finance.yaml POST /deposits/{depositId}/settle"
   }
  ],
  "states": {
   "loading": "The saved payment exceptions.",
   "error": "Could not load. Names which read failed and leaves the payment exceptions untouched.",
   "emptyFirstRun": "No payment exceptions configured. The form opens empty and `createPayment` saves the first one; it says what the platform does in the meantime.",
   "emptyNoAccess": "Shown when the caller lacks `ORDER_CREATE`, which `createPayment` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createPayment",
    "contract": "orders",
    "purpose": "Take a payment against an order",
    "trigger": "onAction"
   },
   {
    "operationId": "addTip",
    "contract": "orders",
    "purpose": "Record a tip against a payment",
    "trigger": "onAction"
   },
   {
    "operationId": "capturePayment",
    "contract": "orders",
    "purpose": "Capture a previously authorised payment",
    "trigger": "onAction"
   },
   {
    "operationId": "inquirePaymentStatus",
    "contract": "orders",
    "purpose": "Ask the provider what actually happened",
    "trigger": "onAction"
   },
   {
    "operationId": "closeDepositBoxes",
    "contract": "shift",
    "purpose": "Close one box or all of them",
    "trigger": "onAction"
   },
   {
    "operationId": "settleDeposit",
    "contract": "finance",
    "purpose": "Convert to revenue, return it, or forfeit it",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "paymentId",
     "from": "deepLink"
    },
    {
     "name": "depositId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `paymentId`, `depositId`."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-024",
   "derivedFrom": "wireframes/reference/Retail Board 3.dc.html",
   "source": "Claude Design Retail pack, 24 August",
   "note": "**Drawn by Claude Design on `Retail Board 3.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
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
 },
 {
  "id": "BO-025",
  "name": "Chargebacks & Disputes",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/chargebacks-disputes",
   "component": "apps/venue-management-web/src/routes/venue-operations/ChargebacksDisputesDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-008",
    "BO-024"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "provenance": "derived — BO-008 declares entryState.params productId, variantId, version and BO-025 holds none of them, so the edge carries nothing and BO-008 opens cold"
    },
    {
     "to": "BO-024",
     "trigger": "Payment Exceptions",
     "provenance": "flow F99 step 1→2",
     "carries": [
      "paymentId"
     ]
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listSettlementExceptions` reads the population and `getSettlement` reads one of them — list, select, act",
  "purpose": "Answer the acquirer with the evidence attached.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every settlement exception",
       "bindsTo": "SettlementException",
       "columns": [
        "SettlementException.id",
        "SettlementException.settlementId",
        "SettlementException.kind",
        "SettlementException.providerReference",
        "SettlementException.paymentId",
        "SettlementException.amount",
        "SettlementException.expectedAmount",
        "SettlementException.resolution",
        "SettlementException.resolvedByPrincipalId",
        "SettlementException.resolvedAt"
       ],
       "operation": "listSettlementExceptions",
       "provenance": "contract finance.yaml GET /settlements/{settlementId}/exceptions"
      },
      {
       "kind": "dataTable",
       "label": "Every settlement",
       "bindsTo": "Settlement",
       "columns": [
        "Settlement.id",
        "Settlement.currencyCode",
        "Settlement.providerName",
        "Settlement.periodStart",
        "Settlement.periodEnd",
        "Settlement.fileReference",
        "Settlement.format",
        "Settlement.status",
        "Settlement.lineCount",
        "Settlement.matchedCount",
        "Settlement.exceptionCount",
        "Settlement.providerGross"
       ],
       "operation": "listSettlements",
       "provenance": "contract finance.yaml GET /settlements"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected settlement exception",
       "bindsTo": "SettlementException",
       "columns": [
        "SettlementException.id",
        "SettlementException.settlementId",
        "SettlementException.kind",
        "SettlementException.providerReference",
        "SettlementException.paymentId",
        "SettlementException.amount",
        "SettlementException.expectedAmount",
        "SettlementException.resolution",
        "SettlementException.note",
        "SettlementException.resolvedByPrincipalId",
        "SettlementException.resolvedAt"
       ],
       "operation": "listSettlementExceptions",
       "provenance": "contract finance.yaml GET /settlements/{settlementId}/exceptions"
      },
      {
       "kind": "detailPanel",
       "label": "The settlement",
       "bindsTo": "Settlement",
       "columns": [
        "Settlement.id",
        "Settlement.currencyCode",
        "Settlement.providerName",
        "Settlement.periodStart",
        "Settlement.periodEnd",
        "Settlement.fileReference",
        "Settlement.format",
        "Settlement.status",
        "Settlement.lineCount",
        "Settlement.matchedCount",
        "Settlement.exceptionCount",
        "Settlement.providerGross",
        "Settlement.providerFees",
        "Settlement.providerNet",
        "Settlement.ledgerGross",
        "Settlement.difference"
       ],
       "operation": "getSettlement",
       "provenance": "contract finance.yaml GET /settlements/{settlementId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Resolve settlement exception",
       "operation": "resolveSettlementException",
       "provenance": "contract finance.yaml POST /settlements/{settlementId}/exceptions"
      },
      {
       "kind": "secondaryButton",
       "label": "Ingest settlement file",
       "operation": "ingestSettlementFile",
       "provenance": "contract finance.yaml POST /settlements"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The chargebacks disputes list.",
   "error": "Could not load. Names which read failed and leaves the chargebacks disputes untouched.",
   "emptyFirstRun": "No chargebacks disputes yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Never shown: `listSettlementExceptions` takes no filter, so an empty list is always the first-run state above.",
   "emptyNoAccess": "Shown when the caller lacks `SETTLEMENT_VIEW`, which `listSettlementExceptions` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listSettlementExceptions",
    "contract": "finance",
    "purpose": "Unmatched or mismatched settlement lines",
    "trigger": "onAction"
   },
   {
    "operationId": "resolveSettlementException",
    "contract": "finance",
    "purpose": "Resolve a settlement exception",
    "trigger": "onAction",
    "invalidates": [
     "listSettlementExceptions"
    ]
   },
   {
    "operationId": "getSettlement",
    "contract": "finance",
    "purpose": "Settlement detail with match results",
    "trigger": "onAction"
   },
   {
    "operationId": "ingestSettlementFile",
    "contract": "finance",
    "purpose": "Ingest a provider settlement file",
    "trigger": "onAction",
    "invalidates": [
     "listSettlementExceptions"
    ]
   },
   {
    "operationId": "listSettlements",
    "contract": "finance",
    "purpose": "List settlement batches",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "settlementId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `settlementId`.",
   "preloaded": [
    "Settlement.id",
    "Settlement.providerName",
    "Settlement.periodStart",
    "Settlement.periodEnd",
    "Settlement.status"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-025"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 5 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formResolveSettlementException",
    "component": "modal",
    "trigger": "Resolve settlement exception",
    "body": "**Collects what `resolveSettlementException` sends before it is called.** Required: `exceptionId`, `resolution`, `note`. Optional: `matchedPaymentId`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Resolve settlement exception",
     "operation": "resolveSettlementException"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "exceptionId",
      "resolution",
      "note",
      "matchedPaymentId"
     ]
    },
    "provenance": "contract finance.yaml POST /settlements/{settlementId}/exceptions"
   },
   {
    "id": "formIngestSettlementFile",
    "component": "modal",
    "trigger": "Ingest settlement file",
    "body": "**Collects what `ingestSettlementFile` sends before it is called.** Required: `providerName`, `periodStart`, `periodEnd`, `fileReference`. Optional: `format`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Ingest settlement file",
     "operation": "ingestSettlementFile"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "providerName",
      "periodStart",
      "periodEnd",
      "fileReference",
      "format"
     ]
    },
    "provenance": "contract finance.yaml POST /settlements"
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
  "id": "BO-026",
  "name": "Group Bookings",
  "module": "Orders & Money",
  "requiresModule": "ticketing",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/group-bookings",
   "component": "apps/venue-management-web/src/routes/venue-operations/GroupBookingsDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-008"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "provenance": "derived — BO-008 declares entryState.params productId, variantId, version and BO-026 holds none of them, so the edge carries nothing and BO-008 opens cold"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Drawn 31 August** — `Seat Platform Board 7.dc.html` frame `seatp-7e`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Group Booking* matched at 0.96. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.",
  "density": "compact",
  "boardFrames": [
   "Seat Platform Board 7.dc.html#seatp-7e"
  ],
  "pattern": "listDetail",
  "patternReason": "`listOrders` reads the population and `getOrder` reads one of them — list, select, act",
  "purpose": "Handle a booking that arrives as a school, not a guest.",
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
       "operation": "listOrders",
       "notes": "Sends `?venueId=` to `listOrders`.",
       "provenance": "contract orders.yaml GET /orders"
      },
      {
       "kind": "textField",
       "label": "Principal id",
       "operation": "listOrders",
       "notes": "Sends `?principalId=` to `listOrders`.",
       "provenance": "contract orders.yaml GET /orders"
      },
      {
       "kind": "textField",
       "label": "Shift id",
       "operation": "listOrders",
       "notes": "Sends `?shiftId=` to `listOrders`.",
       "provenance": "contract orders.yaml GET /orders"
      },
      {
       "kind": "textField",
       "label": "Status",
       "operation": "listOrders",
       "notes": "Sends `?status=` to `listOrders`.",
       "provenance": "contract orders.yaml GET /orders"
      },
      {
       "kind": "datePicker",
       "label": "Created from",
       "operation": "listOrders",
       "notes": "Sends `?createdFrom=` to `listOrders`.",
       "provenance": "contract orders.yaml GET /orders"
      },
      {
       "kind": "datePicker",
       "label": "Created to",
       "operation": "listOrders",
       "notes": "Sends `?createdTo=` to `listOrders`.",
       "provenance": "contract orders.yaml GET /orders"
      },
      {
       "kind": "dataTable",
       "label": "Every order",
       "bindsTo": "OrderSummary",
       "columns": [
        "OrderSummary.id",
        "OrderSummary.orderNumber",
        "OrderSummary.status",
        "OrderSummary.grossAmount",
        "OrderSummary.refundedAmount",
        "OrderSummary.channel",
        "OrderSummary.lineCount"
       ],
       "operation": "listOrders",
       "provenance": "contract orders.yaml GET /orders"
      },
      {
       "kind": "dataTable",
       "label": "Every refund",
       "bindsTo": "Refund",
       "columns": [
        "Refund.id",
        "Refund.orderId",
        "Refund.batchId",
        "Refund.fxRate",
        "Refund.taxReversalEntryId",
        "Refund.settleTo",
        "Refund.fxVariance",
        "Refund.amount",
        "Refund.appliedPercentage",
        "Refund.status",
        "Refund.reason",
        "Refund.requestedByPrincipalId"
       ],
       "operation": "listOrderRefunds",
       "provenance": "contract orders.yaml GET /orders/{orderId}/refunds"
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
       "label": "The selected order",
       "bindsTo": "OrderSummary",
       "columns": [
        "OrderSummary.id",
        "OrderSummary.orderNumber",
        "OrderSummary.status",
        "OrderSummary.grossAmount",
        "OrderSummary.refundedAmount",
        "OrderSummary.channel",
        "OrderSummary.lineCount",
        "OrderSummary.principalId",
        "OrderSummary.holdLabel",
        "OrderSummary.heldUntil"
       ],
       "operation": "listOrders",
       "provenance": "contract orders.yaml GET /orders"
      },
      {
       "kind": "detailPanel",
       "label": "The group booking",
       "bindsTo": "GroupBooking",
       "columns": [
        "GroupBooking.id",
        "GroupBooking.kind",
        "GroupBooking.packageProductId",
        "GroupBooking.yearGroup",
        "GroupBooking.accessAndDietaryNeeds",
        "GroupBooking.celebrantName",
        "GroupBooking.celebrantTurningAge",
        "GroupBooking.allergiesAndRequests",
        "GroupBooking.finalHeadcountDueBy",
        "GroupBooking.quoteSentAt",
        "GroupBooking.riskAssessmentSentAt",
        "GroupBooking.preferredDate",
        "GroupBooking.orderId",
        "GroupBooking.leaderSubjectId",
        "GroupBooking.organisationName",
        "GroupBooking.expectedSize"
       ],
       "operation": "getGroupBooking",
       "provenance": "contract orders.yaml GET /group-bookings/{groupBookingId}"
      },
      {
       "kind": "detailPanel",
       "label": "The order statement",
       "bindsTo": "OrderStatement",
       "columns": [
        "OrderStatement.orderId",
        "OrderStatement.orderNumber",
        "OrderStatement.currency",
        "OrderStatement.currencyScale",
        "OrderStatement.entries",
        "OrderStatement.totalPaid",
        "OrderStatement.totalRefunded",
        "OrderStatement.currentBalance"
       ],
       "operation": "getOrderStatement",
       "provenance": "contract orders.yaml GET /orders/{orderId}/statement"
      },
      {
       "kind": "detailPanel",
       "label": "The order",
       "bindsTo": "Order",
       "columns": [
        "Order.id",
        "Order.orderNumber",
        "Order.channel",
        "Order.venueId",
        "Order.scopePath",
        "Order.status",
        "Order.currency",
        "Order.currencyScale",
        "Order.grossAmount",
        "Order.taxAmount",
        "Order.netAmount",
        "Order.refundedAmount",
        "Order.totalPriceVariance",
        "Order.lines",
        "Order.payments",
        "Order.principalId"
       ],
       "operation": "getOrder",
       "provenance": "contract orders.yaml GET /orders/{orderId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create order",
       "operation": "createOrder",
       "provenance": "contract orders.yaml POST /orders"
      },
      {
       "kind": "secondaryButton",
       "label": "Apply manual discount",
       "operation": "applyManualDiscount",
       "provenance": "contract orders.yaml POST /orders/{orderId}/discounts"
      },
      {
       "kind": "secondaryButton",
       "label": "Create refund",
       "operation": "createRefund",
       "provenance": "contract orders.yaml POST /orders/{orderId}/refunds"
      },
      {
       "kind": "secondaryButton",
       "label": "Exchange order lines",
       "operation": "exchangeOrderLines",
       "provenance": "contract orders.yaml POST /orders/{orderId}/exchanges"
      },
      {
       "kind": "secondaryButton",
       "label": "Hold order",
       "operation": "holdOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/hold"
      },
      {
       "kind": "secondaryButton",
       "label": "Modify order",
       "operation": "modifyOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/modify"
      },
      {
       "kind": "secondaryButton",
       "label": "Reprint order",
       "operation": "reprintOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/reprints"
      },
      {
       "kind": "secondaryButton",
       "label": "Reschedule order",
       "operation": "rescheduleOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/reschedule"
      },
      {
       "kind": "secondaryButton",
       "label": "Resume order",
       "operation": "resumeOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/resume"
      },
      {
       "kind": "destructiveButton",
       "label": "Void order",
       "operation": "voidOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/voids"
      },
      {
       "kind": "secondaryButton",
       "label": "Create group booking",
       "operation": "createGroupBooking",
       "provenance": "contract orders.yaml POST /group-bookings"
      },
      {
       "kind": "secondaryButton",
       "label": "Save group booking",
       "operation": "updateGroupBooking",
       "provenance": "contract orders.yaml PATCH /group-bookings/{groupBookingId}"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmVoidOrder",
    "component": "confirmDialog",
    "trigger": "Void order",
    "body": "**Names what `voidOrder` changes and what it leaves alone**, in the consequence rather than the verb. A group bookings this affects should be identified in the dialog, not just counted. **Collects what `voidOrder` sends before it is called.** Required: `id`, `reason`, `recordedAt`. `reason` is the void reason list (`VoidReason`: guestChangedMind, enteredInError, itemUnavailable, qualityIssue, duplicate, other); **choosing Other makes `note` required** (decided 28 September, audit R125 (4), R222).",
    "provenance": "contract orders.yaml POST /orders/{orderId}/voids"
   },
   {
    "id": "formCreateGroupBooking",
    "component": "modal",
    "trigger": "Create group booking",
    "body": "**Collects what `createGroupBooking` sends before it is called.** Required: `orderId`, `leaderSubjectId`, `expectedSize`. Optional: `kind`, `packageProductId`, `yearGroup`, `accessAndDietaryNeeds`, `celebrantName`, `celebrantTurningAge`, `allergiesAndRequests`, `finalHeadcountDueBy`, `organisationName`, `minimumSize`, `attendeeCaptureRequired`, `attendeeCaptureDueBy`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateGroupBookingRequest",
    "confirm": {
     "label": "Create group booking",
     "operation": "createGroupBooking"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "orderId",
      "leaderSubjectId",
      "expectedSize",
      "kind",
      "packageProductId",
      "yearGroup",
      "accessAndDietaryNeeds",
      "celebrantName",
      "celebrantTurningAge",
      "allergiesAndRequests",
      "finalHeadcountDueBy",
      "organisationName",
      "minimumSize",
      "attendeeCaptureRequired",
      "attendeeCaptureDueBy"
     ]
    },
    "provenance": "contract orders.yaml POST /group-bookings"
   },
   {
    "id": "formUpdateGroupBooking",
    "component": "modal",
    "trigger": "Save group booking",
    "body": "**Collects what `updateGroupBooking` sends before it is called.** Nothing in the body is required. Optional: `packageProductId`, `yearGroup`, `accessAndDietaryNeeds`, `celebrantName`, `celebrantTurningAge`, `allergiesAndRequests`, `finalHeadcountDueBy`, `leaderSubjectId`, `organisationName`, `expectedSize`, `confirmedSize`, `minimumSize` and 3 more. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "UpdateGroupBookingRequest",
    "confirm": {
     "label": "Save group booking",
     "operation": "updateGroupBooking"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "packageProductId",
      "yearGroup",
      "accessAndDietaryNeeds",
      "celebrantName",
      "celebrantTurningAge",
      "allergiesAndRequests",
      "finalHeadcountDueBy",
      "leaderSubjectId",
      "organisationName",
      "expectedSize",
      "confirmedSize",
      "minimumSize",
      "attendeeCaptureRequired",
      "attendeeCaptureDueBy",
      "status"
     ]
    },
    "provenance": "contract orders.yaml PATCH /group-bookings/{groupBookingId}"
   },
   {
    "id": "formCreateOrder",
    "component": "modal",
    "trigger": "Create order",
    "body": "**Collects what `createOrder` sends before it is called.** Required: `id`, `venueId`, `channel`, `lines`, `recordedAt`. Optional: `shiftId`, `subjectId`, `guestLinkId`, `catalogueBundleVersion`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateOrderRequest",
    "confirm": {
     "label": "Create order",
     "operation": "createOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "venueId",
      "channel",
      "lines",
      "recordedAt",
      "shiftId",
      "subjectId",
      "guestLinkId",
      "catalogueBundleVersion"
     ]
    },
    "provenance": "contract orders.yaml POST /orders"
   },
   {
    "id": "formApplyManualDiscount",
    "component": "modal",
    "trigger": "Apply manual discount",
    "body": "**Collects what `applyManualDiscount` sends before it is called.** Required: `id`, `reason`, `recordedAt`. Optional: `lineId`, `amount`, `percentage`, `reasonCode`, `approverPrincipalId`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "ManualDiscountRequest",
    "confirm": {
     "label": "Apply manual discount",
     "operation": "applyManualDiscount"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "reason",
      "recordedAt",
      "lineId",
      "amount",
      "percentage",
      "reasonCode",
      "approverPrincipalId"
     ]
    },
    "provenance": "contract orders.yaml POST /orders/{orderId}/discounts"
   },
   {
    "id": "formCreateRefund",
    "component": "modal",
    "trigger": "Create refund",
    "body": "**Collects what `createRefund` sends before it is called.** Required: `id`, `amount`, `reason`, `recordedAt`. Optional: `lineIds`, `secondaryAuthorisation`, `refundToOriginalTender`, `alternateTender`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateRefundRequest",
    "confirm": {
     "label": "Create refund",
     "operation": "createRefund"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "amount",
      "reason",
      "recordedAt",
      "lineIds",
      "secondaryAuthorisation",
      "refundToOriginalTender",
      "alternateTender"
     ]
    },
    "provenance": "contract orders.yaml POST /orders/{orderId}/refunds"
   },
   {
    "id": "formExchangeOrderLines",
    "component": "modal",
    "trigger": "Exchange order lines",
    "body": "**Collects what `exchangeOrderLines` sends before it is called.** Required: `id`, `outgoingLineIds`, `incomingLines`, `recordedAt`. Optional: `waiveFee`, `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "ExchangeOrderRequest",
    "confirm": {
     "label": "Exchange order lines",
     "operation": "exchangeOrderLines"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "outgoingLineIds",
      "incomingLines",
      "recordedAt",
      "waiveFee",
      "reason"
     ]
    },
    "provenance": "contract orders.yaml POST /orders/{orderId}/exchanges"
   },
   {
    "id": "formHoldOrder",
    "component": "modal",
    "trigger": "Hold order",
    "body": "**Collects what `holdOrder` sends before it is called.** Required: `recordedAt`. Optional: `label`, `holdUntil`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Hold order",
     "operation": "holdOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "recordedAt",
      "label",
      "holdUntil"
     ]
    },
    "provenance": "contract orders.yaml POST /orders/{orderId}/hold"
   },
   {
    "id": "formModifyOrder",
    "component": "modal",
    "trigger": "Modify order",
    "body": "**Collects what `modifyOrder` sends before it is called.** Required: `id`, `recordedAt`. Optional: `addLines`, `removeLineIds`, `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "ModifyOrderRequest",
    "confirm": {
     "label": "Modify order",
     "operation": "modifyOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "recordedAt",
      "addLines",
      "removeLineIds",
      "reason"
     ]
    },
    "provenance": "contract orders.yaml POST /orders/{orderId}/modify"
   },
   {
    "id": "formReprintOrder",
    "component": "modal",
    "trigger": "Reprint order",
    "body": "**Collects what `reprintOrder` sends before it is called.** Required: `delivery`, `recordedAt`. Optional: `destination`, `lineIds`, `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Reprint order",
     "operation": "reprintOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "delivery",
      "recordedAt",
      "destination",
      "lineIds",
      "reason"
     ]
    },
    "provenance": "contract orders.yaml POST /orders/{orderId}/reprints"
   },
   {
    "id": "formRescheduleOrder",
    "component": "modal",
    "trigger": "Reschedule order",
    "body": "**Collects what `rescheduleOrder` sends before it is called.** Required: `targetPerformanceId`, `recordedAt`. Optional: `lineIds`, `waiveFee`, `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Reschedule order",
     "operation": "rescheduleOrder"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "targetPerformanceId",
      "recordedAt",
      "lineIds",
      "waiveFee",
      "reason"
     ]
    },
    "provenance": "contract orders.yaml POST /orders/{orderId}/reschedule"
   }
  ],
  "states": {
   "loading": "The group bookings list.",
   "error": "Could not load. Names which read failed and leaves the group bookings untouched.",
   "emptyFirstRun": "No group bookings yet. Offers Create group booking (`createGroupBooking`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on venueId, principalId, shiftId, status, createdFrom, createdTo and the group bookings are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `ORDER_VIEW`, which `getGroupBooking` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createGroupBooking",
    "contract": "orders",
    "purpose": "Turn an order into a group booking",
    "trigger": "onAction"
   },
   {
    "operationId": "getGroupBooking",
    "contract": "orders",
    "purpose": "The group, its leader and its manifest",
    "trigger": "onAction"
   },
   {
    "operationId": "updateGroupBooking",
    "contract": "orders",
    "purpose": "Confirm numbers, change the leader or cancel",
    "trigger": "onAction",
    "invalidates": [
     "getGroupBooking"
    ]
   },
   {
    "operationId": "listOrders",
    "contract": "orders",
    "purpose": "List orders",
    "trigger": "onLoad"
   },
   {
    "operationId": "createOrder",
    "contract": "orders",
    "purpose": "Create an order",
    "trigger": "onAction",
    "invalidates": [
     "listOrders"
    ]
   },
   {
    "operationId": "applyManualDiscount",
    "contract": "orders",
    "purpose": "Apply a discount a cashier chose",
    "trigger": "onAction",
    "invalidates": [
     "listOrders"
    ]
   },
   {
    "operationId": "createRefund",
    "contract": "orders",
    "purpose": "Refund an order, wholly or in part",
    "trigger": "onAction",
    "invalidates": [
     "listOrders"
    ]
   },
   {
    "operationId": "exchangeOrderLines",
    "contract": "orders",
    "purpose": "Exchange lines for different products or dates",
    "trigger": "onAction",
    "invalidates": [
     "listOrders"
    ]
   },
   {
    "operationId": "getOrder",
    "contract": "orders",
    "purpose": "Read an order",
    "trigger": "onAction"
   },
   {
    "operationId": "getOrderStatement",
    "contract": "orders",
    "purpose": "Full financial history of an order",
    "trigger": "onAction"
   },
   {
    "operationId": "holdOrder",
    "contract": "orders",
    "purpose": "Park a sale and free the till",
    "trigger": "onAction",
    "invalidates": [
     "listOrders"
    ]
   },
   {
    "operationId": "listOrderRefunds",
    "contract": "orders",
    "purpose": "List refunds against an order",
    "trigger": "onAction"
   },
   {
    "operationId": "modifyOrder",
    "contract": "orders",
    "purpose": "Add or remove lines on an existing order",
    "trigger": "onAction",
    "invalidates": [
     "listOrders"
    ]
   },
   {
    "operationId": "reprintOrder",
    "contract": "orders",
    "purpose": "Reprint or resend tickets",
    "trigger": "onAction",
    "invalidates": [
     "listOrders"
    ]
   },
   {
    "operationId": "rescheduleOrder",
    "contract": "orders",
    "purpose": "Move an order to another performance",
    "trigger": "onAction",
    "invalidates": [
     "listOrders"
    ]
   },
   {
    "operationId": "resumeOrder",
    "contract": "orders",
    "purpose": "Bring a parked sale back to a till",
    "trigger": "onAction",
    "invalidates": [
     "listOrders"
    ]
   },
   {
    "operationId": "voidOrder",
    "contract": "orders",
    "purpose": "Void an order",
    "trigger": "onAction",
    "invalidates": [
     "listOrders"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "orderId",
     "from": "deepLink"
    },
    {
     "name": "groupBookingId",
     "from": "navigation"
    }
   ],
   "coldEntry": "**A guest opening an order link weeks later.** Shows the order if it still resolves; if it was refunded or the performance passed, says which and offers the order list rather than an error.",
   "preloaded": [
    "OrderSummary.id",
    "OrderSummary.orderNumber",
    "OrderSummary.status",
    "OrderSummary.grossAmount",
    "OrderSummary.refundedAmount"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-026",
   "derivedFrom": "wireframes/reference/Seat Platform Board 7.dc.html",
   "note": "**Drawn by Claude Design on `Seat Platform Board 7.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
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
  "id": "BO-027",
  "name": "Reissue & Media Replacement",
  "module": "Orders & Money",
  "requiresModule": "ticketing",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/reissue-media-replacement",
   "component": "apps/venue-management-web/src/routes/venue-operations/ReissueMediaReplacementDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-008",
    "BO-314",
    "BO-644"
   ],
   "inferred": true,
   "entryFrom": [
    "BO-314",
    "BO-644"
   ],
   "transitions": [
    {
     "to": "BO-314",
     "trigger": "Back to Amendment & After-Sales Command Center",
     "provenance": "inherited from BO-320 when it was merged here, 28 September (audit R276)",
     "back": true
    },
    {
     "to": "BO-644",
     "trigger": "Back to Credential Issuance Command Center",
     "provenance": "inherited from BO-652 when it was merged here, 28 September (audit R276)",
     "back": true
    },
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "carries": [
      "version"
     ],
     "provenance": "derived — BO-008 declares entryState.params productId, variantId, version and BO-027 holds version, so an edge into it carries them"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **8 assets operations removed 18 August (CF-114).** The whole media contract was attached to this screen. **A till adding an item to a ticket does not manage a media library** — it reads the asset it needs and nothing else. Same shape as CF-87, one level up: that attached sibling operations, this attached a whole contract. **Absorbed BO-320 and BO-652 on 28 September (audit R276)**: Ticket Reissue & Fulfillment Regeneration brought `listTicketReissueFulfillment` (the reissue history of an order's tickets) and Credential Replacement & Reissue brought `listCredentialReplacementReissue` (lost, damaged and stolen credentials replaced); both are retired, and their hubs BO-314 and BO-644 open this screen.",
  "density": "compact",
  "pattern": "statusTracker",
  "patternReason": "`getMediaEntitlements` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "Replace media a guest has lost or damaged.",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The media entitlements",
       "bindsTo": "MediaEntitlements",
       "columns": [
        "MediaEntitlements.mediaCode",
        "MediaEntitlements.mediaKind",
        "MediaEntitlements.subjectId",
        "MediaEntitlements.isValid",
        "MediaEntitlements.invalidReason",
        "MediaEntitlements.canAcceptMore",
        "MediaEntitlements.entitlements"
       ],
       "operation": "getMediaEntitlements",
       "provenance": "contract orders.yaml GET /media/{mediaCode}/entitlements"
      },
      {
       "kind": "detailPanel",
       "label": "The media asset",
       "bindsTo": "MediaAssetDetail",
       "columns": [
        "MediaAssetDetail.id",
        "MediaAssetDetail.kind",
        "MediaAssetDetail.status",
        "MediaAssetDetail.filename",
        "MediaAssetDetail.contentType",
        "MediaAssetDetail.sizeBytes",
        "MediaAssetDetail.title",
        "MediaAssetDetail.description",
        "MediaAssetDetail.altText",
        "MediaAssetDetail.width",
        "MediaAssetDetail.height",
        "MediaAssetDetail.durationSeconds",
        "MediaAssetDetail.customMetadata",
        "MediaAssetDetail.sharedWithTenantIds",
        "MediaAssetDetail.tags",
        "MediaAssetDetail.venueId"
       ],
       "operation": "getMediaAsset",
       "provenance": "contract assets.yaml GET /media/{mediaId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Append entitlement to media",
       "operation": "appendEntitlementToMedia",
       "provenance": "contract orders.yaml POST /media/{mediaCode}/entitlements"
      },
      {
       "kind": "secondaryButton",
       "label": "Replace media asset",
       "operation": "replaceMediaAsset",
       "provenance": "contract assets.yaml POST /media/{mediaId}/replace"
      }
     ]
    },
    {
     "name": "history",
     "slot": "carried",
     "components": [
      {
       "kind": "dataTable",
       "label": "Ticket reissues",
       "derived": true,
       "impliedBy": "listTicketReissueFulfillment",
       "notes": "Carried from BO-320 (merged 28 September, audit R276) — tickets and media regenerated after an amendment, correction, loss or delivery failure. **Cursor pagination, never offset.**"
      },
      {
       "kind": "dataTable",
       "label": "Credential replacements",
       "derived": true,
       "impliedBy": "listCredentialReplacementReissue",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows. Carried from BO-652 (merged 28 September, audit R276)."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The reissue media replacement, read by `getMediaEntitlements`.",
   "error": "Could not load. Names which read failed and leaves the reissue media replacement untouched.",
   "emptyFirstRun": "No reissue media replacement yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "The ticket reissue or credential replacement history for this media has nothing matching; the media itself is still shown. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `ORDER_VIEW`, which `getMediaEntitlements` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getMediaEntitlements",
    "contract": "orders",
    "purpose": "What is already on this media",
    "trigger": "onLoad"
   },
   {
    "operationId": "appendEntitlementToMedia",
    "contract": "orders",
    "purpose": "Add something to a ticket the guest already holds",
    "trigger": "onAction"
   },
   {
    "operationId": "getMediaAsset",
    "contract": "assets",
    "purpose": "Read an asset with derivatives and usage",
    "trigger": "onLoad"
   },
   {
    "operationId": "replaceMediaAsset",
    "contract": "assets",
    "purpose": "Replace the file behind an asset",
    "trigger": "onAction"
   },
   {
    "operationId": "listTicketReissueFulfillment",
    "contract": "orders",
    "purpose": "Ticket reissue and fulfilment regeneration history (absorbed from BO-320, audit R276)",
    "trigger": "onLoad"
   },
   {
    "operationId": "listCredentialReplacementReissue",
    "contract": "access",
    "purpose": "Credential replacement, reissue, revocation and recovery (absorbed from BO-652, audit R276)",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "mediaCode",
     "from": "deepLink"
    },
    {
     "name": "mediaId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know whether the record moved, closed or never existed, because those are three different next actions. **The scope is resolved from the session, never from the link**: a link cannot move somebody to a venue they do not hold. Arrives with `mediaCode`, `mediaId`."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-027"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 4 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formAppendEntitlementToMedia",
    "component": "modal",
    "trigger": "Append entitlement to media",
    "body": "**Collects what `appendEntitlementToMedia` sends before it is called.** Required: `id`, `lines`, `recordedAt`. Optional: `paymentMethod`, `note`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "AppendEntitlementRequest",
    "confirm": {
     "label": "Append entitlement to media",
     "operation": "appendEntitlementToMedia"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "lines",
      "recordedAt",
      "paymentMethod",
      "note"
     ]
    },
    "provenance": "contract orders.yaml POST /media/{mediaCode}/entitlements"
   },
   {
    "id": "formReplaceMediaAsset",
    "component": "modal",
    "trigger": "Replace media asset",
    "body": "**Collects what `replaceMediaAsset` sends before it is called.** Required: `uploadId`. Optional: `note`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Replace media asset",
     "operation": "replaceMediaAsset"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "uploadId",
      "note"
     ]
    },
    "provenance": "contract assets.yaml POST /media/{mediaId}/replace"
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
  "id": "BO-028",
  "name": "Refund Approval Queue",
  "module": "Orders & Money",
  "requiresModule": "ticketing",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/refund-approval-queue",
   "component": "apps/venue-management-web/src/routes/venue-operations/RefundApprovalQueueDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-008"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "provenance": "derived — BO-008 declares entryState.params productId, variantId, version and BO-028 holds none of them, so the edge carries nothing and BO-008 opens cold"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the screen declares only writes (`createRefundRequest`) and no read of a population — it is settings, not a list",
  "purpose": "Approve the refunds a cashier is not allowed to make alone.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create refund request",
       "operation": "createRefundRequest",
       "provenance": "contract orders.yaml POST /refund-requests"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "textField",
       "label": "Order id",
       "operation": "createRefundRequest",
       "notes": "Required.",
       "provenance": "contract orders.yaml POST /refund-requests"
      },
      {
       "kind": "textField",
       "label": "Reason",
       "operation": "createRefundRequest",
       "notes": "Required.",
       "provenance": "contract orders.yaml POST /refund-requests"
      },
      {
       "kind": "multiSelect",
       "label": "Line ids",
       "operation": "createRefundRequest",
       "provenance": "contract orders.yaml POST /refund-requests"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "Figures load; the expected total renders last",
   "error": "**Could not load. Every action that moves money is blocked** — a figure nobody read must not be reconciled against",
   "emptyFirstRun": "Nothing in the period — reported as a result, not an empty screen"
  },
  "apis": [
   {
    "operationId": "createRefundRequest",
    "contract": "orders",
    "purpose": "Guest-initiated refund request",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-028"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 1 operation this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "BO-029",
  "name": "Report Builder",
  "module": "Orders & Money",
  "requiresModule": "analytics",
  "wave": 2,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/report-builder",
   "component": "apps/venue-management-web/src/routes/venue-operations/ReportBuilderDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-008"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "provenance": "derived — BO-008 declares entryState.params productId, variantId, version and BO-029 holds none of them, so the edge carries nothing and BO-008 opens cold"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listReports` reads the population and `getFinancialReport` reads one of them — list, select, act",
  "purpose": "Build the report nobody wrote down, without asking for a release.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Category",
       "operation": "listReports",
       "notes": "Sends `?category=` to `listReports`.",
       "provenance": "contract reporting.yaml GET /reports"
      },
      {
       "kind": "searchField",
       "label": "Search",
       "operation": "listReports",
       "notes": "Sends `?search=` to `listReports`.",
       "provenance": "contract reporting.yaml GET /reports"
      },
      {
       "kind": "dataTable",
       "label": "Every report definition",
       "bindsTo": "ReportDefinition",
       "columns": [
        "ReportDefinition.name",
        "ReportDefinition.description",
        "ReportDefinition.category",
        "ReportDefinition.dataSource",
        "ReportDefinition.columns",
        "ReportDefinition.filters",
        "ReportDefinition.groupBy",
        "ReportDefinition.parameters",
        "ReportDefinition.requiredPermission",
        "ReportDefinition.maxDateRangeDays",
        "ReportDefinition.id",
        "ReportDefinition.isSystem"
       ],
       "operation": "listReports",
       "provenance": "contract reporting.yaml GET /reports"
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
       "label": "The selected report definition",
       "bindsTo": "ReportDefinition",
       "columns": [
        "ReportDefinition.name",
        "ReportDefinition.description",
        "ReportDefinition.category",
        "ReportDefinition.dataSource",
        "ReportDefinition.columns",
        "ReportDefinition.filters",
        "ReportDefinition.groupBy",
        "ReportDefinition.parameters",
        "ReportDefinition.requiredPermission",
        "ReportDefinition.maxDateRangeDays",
        "ReportDefinition.id",
        "ReportDefinition.isSystem",
        "ReportDefinition.isRetired",
        "ReportDefinition.estimatedCost",
        "ReportDefinition.createdByPrincipalId",
        "ReportDefinition.lastRunAt"
       ],
       "operation": "getReport",
       "provenance": "contract reporting.yaml GET /reports/{reportId}"
      },
      {
       "kind": "detailPanel",
       "label": "The financial report",
       "bindsTo": "FinancialReport",
       "columns": [
        "FinancialReport.report",
        "FinancialReport.fiscalPeriodId",
        "FinancialReport.legalEntityId",
        "FinancialReport.currency",
        "FinancialReport.currencyScale",
        "FinancialReport.generatedAt",
        "FinancialReport.sections"
       ],
       "operation": "getFinancialReport",
       "provenance": "contract finance.yaml GET /reports/financial"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create report",
       "operation": "createReport",
       "provenance": "contract reporting.yaml POST /reports"
      },
      {
       "kind": "secondaryButton",
       "label": "Ask reporting question",
       "operation": "askReportingQuestion",
       "provenance": "contract reporting.yaml POST /reports/ask"
      },
      {
       "kind": "destructiveButton",
       "label": "Delete report",
       "operation": "deleteReport",
       "provenance": "contract reporting.yaml DELETE /reports/{reportId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Run report",
       "operation": "runReport",
       "provenance": "contract reporting.yaml POST /reports/{reportId}/run"
      },
      {
       "kind": "secondaryButton",
       "label": "Save natural language query",
       "operation": "saveNaturalLanguageQuery",
       "provenance": "contract reporting.yaml POST /reports/ask/{conversationId}/save"
      },
      {
       "kind": "secondaryButton",
       "label": "Save report",
       "operation": "updateReport",
       "provenance": "contract reporting.yaml PUT /reports/{reportId}"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmDeleteReport",
    "component": "confirmDialog",
    "trigger": "Delete report",
    "body": "**Names what `deleteReport` changes and what it leaves alone**, in the consequence rather than the verb. A report this affects should be identified in the dialog, not just counted.",
    "provenance": "contract reporting.yaml DELETE /reports/{reportId}"
   },
   {
    "id": "formCreateReport",
    "component": "modal",
    "trigger": "Create report",
    "body": "**Collects what `createReport` sends before it is called.** Required: `name`, `category`, `dataSource`, `columns`, `requiredPermission`. Optional: `description`, `filters`, `groupBy`, `parameters`, `maxDateRangeDays`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateReportRequest",
    "confirm": {
     "label": "Create report",
     "operation": "createReport"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "name",
      "category",
      "dataSource",
      "columns",
      "requiredPermission",
      "description",
      "filters",
      "groupBy",
      "parameters",
      "maxDateRangeDays"
     ]
    },
    "provenance": "contract reporting.yaml POST /reports"
   },
   {
    "id": "formAskReportingQuestion",
    "component": "modal",
    "trigger": "Ask reporting question",
    "body": "**Collects what `askReportingQuestion` sends before it is called.** Required: `question`. Optional: `conversationId`, `venueId`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Ask reporting question",
     "operation": "askReportingQuestion"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "question",
      "conversationId",
      "venueId"
     ]
    },
    "provenance": "contract reporting.yaml POST /reports/ask"
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
   },
   {
    "id": "formSaveNaturalLanguageQuery",
    "component": "modal",
    "trigger": "Save natural language query",
    "body": "**Collects what `saveNaturalLanguageQuery` sends before it is called.** Required: `name`. Optional: `category`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save natural language query",
     "operation": "saveNaturalLanguageQuery"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "name",
      "category"
     ]
    },
    "provenance": "contract reporting.yaml POST /reports/ask/{conversationId}/save"
   },
   {
    "id": "formUpdateReport",
    "component": "modal",
    "trigger": "Save report",
    "body": "**Collects what `updateReport` sends before it is called.** Required: `name`, `category`, `dataSource`, `columns`, `requiredPermission`. Optional: `description`, `filters`, `groupBy`, `parameters`, `maxDateRangeDays`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateReportRequest",
    "confirm": {
     "label": "Save report",
     "operation": "updateReport"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "name",
      "category",
      "dataSource",
      "columns",
      "requiredPermission",
      "description",
      "filters",
      "groupBy",
      "parameters",
      "maxDateRangeDays"
     ]
    },
    "provenance": "contract reporting.yaml PUT /reports/{reportId}"
   }
  ],
  "states": {
   "loading": "The report list.",
   "error": "Could not load. Names which read failed and leaves the report untouched.",
   "emptyFirstRun": "No report yet. Offers Create report (`createReport`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on category, search and the report are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `REPORT_VIEW_VENUE`, which `getFinancialReport` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getFinancialReport",
    "contract": "finance",
    "purpose": "P&L, balance sheet or cash flow",
    "trigger": "onLoad"
   },
   {
    "operationId": "listReports",
    "contract": "reporting",
    "purpose": "List available report definitions",
    "trigger": "onLoad"
   },
   {
    "operationId": "createReport",
    "contract": "reporting",
    "purpose": "Create a custom report definition",
    "trigger": "onAction",
    "invalidates": [
     "listReports"
    ]
   },
   {
    "operationId": "askReportingQuestion",
    "contract": "reporting",
    "purpose": "Natural-language reporting query",
    "trigger": "onAction",
    "invalidates": [
     "listReports"
    ]
   },
   {
    "operationId": "deleteReport",
    "contract": "reporting",
    "purpose": "Retire a report definition",
    "trigger": "onAction",
    "invalidates": [
     "listReports"
    ]
   },
   {
    "operationId": "getReport",
    "contract": "reporting",
    "purpose": "Read a report definition",
    "trigger": "onAction"
   },
   {
    "operationId": "runReport",
    "contract": "reporting",
    "purpose": "Run a report",
    "trigger": "onAction",
    "invalidates": [
     "listReports"
    ]
   },
   {
    "operationId": "saveNaturalLanguageQuery",
    "contract": "reporting",
    "purpose": "Save a natural-language answer as a report definition",
    "trigger": "onAction",
    "invalidates": [
     "listReports"
    ]
   },
   {
    "operationId": "updateReport",
    "contract": "reporting",
    "purpose": "Publish a new version of a definition",
    "trigger": "onAction",
    "invalidates": [
     "listReports"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "conversationId",
     "from": "deepLink"
    },
    {
     "name": "reportId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "A conversation link an agent opens from a notification. Resolves, or says it was closed and by whom.",
   "preloaded": [
    "ReportDefinition.name",
    "ReportDefinition.description",
    "ReportDefinition.category",
    "ReportDefinition.dataSource",
    "ReportDefinition.columns"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-029"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 9 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "BO-039",
  "name": "Shift Directory",
  "module": "Orders & Money",
  "requiresModule": "core",
  "wave": 1,
  "capability": "C00",
  "implementation": {
   "app": "venue-management-web",
   "route": "/venue-operations/shift-directory",
   "component": "apps/venue-management-web/src/routes/venue-operations/ShiftDirectoryDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "exitTo": [
    "BO-008"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "BO-008",
     "trigger": "Product Detail & Variants",
     "provenance": "derived — BO-008 declares entryState.params productId, variantId, version and BO-039 holds none of them, so the edge carries nothing and BO-008 opens cold"
    }
   ]
  },
  "notes": "Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.",
  "density": "compact",
  "pattern": "approvalInbox",
  "patternReason": "`approveShiftOpen` decides items that `listShifts` queues — every row is waiting for a person, so the empty state is success",
  "purpose": "See every till, open or closed.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "queue",
     "components": [
      {
       "kind": "textField",
       "label": "Workstation id",
       "operation": "listShifts",
       "notes": "Sends `?workstationId=` to `listShifts`.",
       "provenance": "contract shift.yaml GET /shifts"
      },
      {
       "kind": "textField",
       "label": "Status",
       "operation": "listShifts",
       "notes": "Sends `?status=` to `listShifts`.",
       "provenance": "contract shift.yaml GET /shifts"
      },
      {
       "kind": "datePicker",
       "label": "Opened from",
       "operation": "listShifts",
       "notes": "Sends `?openedFrom=` to `listShifts`.",
       "provenance": "contract shift.yaml GET /shifts"
      },
      {
       "kind": "datePicker",
       "label": "Opened to",
       "operation": "listShifts",
       "notes": "Sends `?openedTo=` to `listShifts`.",
       "provenance": "contract shift.yaml GET /shifts"
      },
      {
       "kind": "dataTable",
       "label": "Waiting for a decision",
       "bindsTo": "Shift",
       "columns": [
        "Shift.id",
        "Shift.workstationId",
        "Shift.venueId",
        "Shift.scopePath",
        "Shift.principalId",
        "Shift.principalDisplayName",
        "Shift.incidents",
        "Shift.status",
        "Shift.currency",
        "Shift.currencyScale",
        "Shift.depositBoxCode",
        "Shift.bagNumber"
       ],
       "operation": "listShifts",
       "provenance": "contract shift.yaml GET /shifts"
      },
      {
       "kind": "dataTable",
       "label": "Every cash movement",
       "bindsTo": "CashMovement",
       "columns": [
        "CashMovement.id",
        "CashMovement.kind",
        "CashMovement.amount",
        "CashMovement.denominations",
        "CashMovement.reference",
        "CashMovement.reason",
        "CashMovement.recordedAt",
        "CashMovement.shiftId",
        "CashMovement.depositBoxId",
        "CashMovement.witnessPrincipalId",
        "CashMovement.withdrawalReason",
        "CashMovement.authorisedByPrincipalId"
       ],
       "operation": "listCashMovements",
       "provenance": "contract shift.yaml GET /shifts/{shiftId}/cash-movements"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "item",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected shift",
       "bindsTo": "Shift",
       "columns": [
        "Shift.id",
        "Shift.workstationId",
        "Shift.venueId",
        "Shift.scopePath",
        "Shift.principalId",
        "Shift.principalDisplayName",
        "Shift.incidents",
        "Shift.status",
        "Shift.currency",
        "Shift.currencyScale",
        "Shift.depositBoxCode",
        "Shift.bagNumber",
        "Shift.openingFloat",
        "Shift.salesTotal",
        "Shift.refundsTotal",
        "Shift.liftsTotal"
       ],
       "operation": "getCurrentShift",
       "provenance": "contract shift.yaml GET /shifts/current"
      },
      {
       "kind": "detailPanel",
       "label": "The shift",
       "bindsTo": "Shift",
       "columns": [
        "Shift.id",
        "Shift.workstationId",
        "Shift.venueId",
        "Shift.scopePath",
        "Shift.principalId",
        "Shift.principalDisplayName",
        "Shift.incidents",
        "Shift.status",
        "Shift.currency",
        "Shift.currencyScale",
        "Shift.depositBoxCode",
        "Shift.bagNumber",
        "Shift.openingFloat",
        "Shift.salesTotal",
        "Shift.refundsTotal",
        "Shift.liftsTotal"
       ],
       "operation": "getShift",
       "provenance": "contract shift.yaml GET /shifts/{shiftId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "decision",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Open shift",
       "operation": "openShift",
       "provenance": "contract shift.yaml POST /shifts"
      },
      {
       "kind": "secondaryButton",
       "label": "Accept shift variance",
       "operation": "acceptShiftVariance",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/accept-variance"
      },
      {
       "kind": "secondaryButton",
       "label": "Approve shift open",
       "operation": "approveShiftOpen",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/approve-open"
      },
      {
       "kind": "destructiveButton",
       "label": "Close shift",
       "operation": "closeShift",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/close"
      },
      {
       "kind": "secondaryButton",
       "label": "Create cash movement",
       "operation": "createCashMovement",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/cash-movements"
      },
      {
       "kind": "secondaryButton",
       "label": "Record no sale",
       "operation": "recordNoSale",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/no-sale"
      },
      {
       "kind": "secondaryButton",
       "label": "Reopen shift",
       "operation": "reopenShift",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/reopen"
      },
      {
       "kind": "secondaryButton",
       "label": "Resume shift",
       "operation": "resumeShift",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/resume"
      },
      {
       "kind": "destructiveButton",
       "label": "Suspend shift",
       "operation": "suspendShift",
       "provenance": "contract shift.yaml POST /shifts/{shiftId}/suspend"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmCloseShift",
    "component": "confirmDialog",
    "trigger": "Close shift",
    "body": "**Names what `closeShift` changes and what it leaves alone**, in the consequence rather than the verb. A shift this affects should be identified in the dialog, not just counted. **Collects what `closeShift` sends before it is called.** Required: `countedCash`, `recordedAt`. Optional: `nonCashDeclared`, `notes`, `releaseHeldLeases`.",
    "provenance": "contract shift.yaml POST /shifts/{shiftId}/close",
    "bindsTo": "CloseShiftRequest"
   },
   {
    "id": "confirmSuspendShift",
    "component": "confirmDialog",
    "trigger": "Suspend shift",
    "body": "**Names what `suspendShift` changes and what it leaves alone**, in the consequence rather than the verb. A shift this affects should be identified in the dialog, not just counted. **Collects what `suspendShift` sends before it is called.** Required: `recordedAt`. Optional: `reason`.",
    "provenance": "contract shift.yaml POST /shifts/{shiftId}/suspend"
   },
   {
    "id": "formOpenShift",
    "component": "modal",
    "trigger": "Open shift",
    "body": "**Collects what `openShift` sends before it is called.** Required: `workstationId`, `openingFloat`. Optional: `depositBoxCode`, `bagNumber`, `recordedAt`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "OpenShiftRequest",
    "confirm": {
     "label": "Open shift",
     "operation": "openShift"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "workstationId",
      "openingFloat",
      "depositBoxCode",
      "bagNumber",
      "recordedAt"
     ]
    },
    "provenance": "contract shift.yaml POST /shifts"
   },
   {
    "id": "formAcceptShiftVariance",
    "component": "modal",
    "trigger": "Accept shift variance",
    "body": "**Collects what `acceptShiftVariance` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Accept shift variance",
     "operation": "acceptShiftVariance"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "reason"
     ]
    },
    "provenance": "contract shift.yaml POST /shifts/{shiftId}/accept-variance"
   },
   {
    "id": "formApproveShiftOpen",
    "component": "modal",
    "trigger": "Approve shift open",
    "body": "**Collects what `approveShiftOpen` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Approve shift open",
     "operation": "approveShiftOpen"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "reason"
     ]
    },
    "provenance": "contract shift.yaml POST /shifts/{shiftId}/approve-open"
   },
   {
    "id": "formCreateCashMovement",
    "component": "modal",
    "trigger": "Create cash movement",
    "body": "**Collects what `createCashMovement` sends before it is called.** Required: `id`, `kind`, `amount`, `recordedAt`. Optional: `denominations`, `reference`, `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateCashMovementRequest",
    "confirm": {
     "label": "Create cash movement",
     "operation": "createCashMovement"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "kind",
      "amount",
      "recordedAt",
      "denominations",
      "reference",
      "reason"
     ]
    },
    "provenance": "contract shift.yaml POST /shifts/{shiftId}/cash-movements"
   },
   {
    "id": "formRecordNoSale",
    "component": "modal",
    "trigger": "Record no sale",
    "body": "**Collects what `recordNoSale` sends before it is called.** Required: `id`, `reason`, `recordedAt`. Optional: `note`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Record no sale",
     "operation": "recordNoSale"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "reason",
      "recordedAt",
      "note"
     ]
    },
    "provenance": "contract shift.yaml POST /shifts/{shiftId}/no-sale"
   },
   {
    "id": "formReopenShift",
    "component": "modal",
    "trigger": "Reopen shift",
    "body": "**Collects what `reopenShift` sends before it is called.** Required: `reason` and `supervisorStepUp` — a supervisor who did not close the shift enters their staff PIN on this device (`principalId`, `credential`) (decided 28 September, audit R144). A refusal names which: the supervisor is the closer (403 approver-is-closer) or the PIN was refused (403 supervisor-step-up-refused). Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Reopen shift",
     "operation": "reopenShift"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "reason",
      "supervisorStepUp"
     ]
    },
    "provenance": "contract shift.yaml POST /shifts/{shiftId}/reopen"
   },
   {
    "id": "formResumeShift",
    "component": "modal",
    "trigger": "Resume shift",
    "body": "**Collects what `resumeShift` sends before it is called.** Required: `recordedAt`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Resume shift",
     "operation": "resumeShift"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "recordedAt"
     ]
    },
    "provenance": "contract shift.yaml POST /shifts/{shiftId}/resume"
   }
  ],
  "states": {
   "loading": "The shift list.",
   "error": "Could not load. Names which read failed and leaves the shift untouched.",
   "emptyFirstRun": "**Nothing is waiting, which is the good outcome.** An empty queue means every item has been decided; it offers no create action, because creating work is not what it needs.",
   "emptyNoResults": "Nothing matches the filter on workstationId, status, openedFrom, openedTo and the shift are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `REPORT_VIEW_WORKSTATION`, which `listShifts` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listShifts",
    "contract": "shift",
    "purpose": "List shifts",
    "trigger": "onLoad"
   },
   {
    "operationId": "getCurrentShift",
    "contract": "shift",
    "purpose": "The open or suspended shift on the session's workstation",
    "trigger": "onLoad"
   },
   {
    "operationId": "openShift",
    "contract": "shift",
    "purpose": "Open a shift",
    "trigger": "onAction",
    "invalidates": [
     "listShifts"
    ]
   },
   {
    "operationId": "acceptShiftVariance",
    "contract": "shift",
    "purpose": "Accept an over/short beyond the threshold",
    "trigger": "onAction",
    "invalidates": [
     "listShifts"
    ]
   },
   {
    "operationId": "approveShiftOpen",
    "contract": "shift",
    "purpose": "Approve a shift opening outside tolerance",
    "trigger": "onAction",
    "invalidates": [
     "listShifts"
    ]
   },
   {
    "operationId": "closeShift",
    "contract": "shift",
    "purpose": "Blind close-out",
    "trigger": "onAction",
    "invalidates": [
     "listShifts"
    ]
   },
   {
    "operationId": "createCashMovement",
    "contract": "shift",
    "purpose": "Record a cash lift or add",
    "trigger": "onAction",
    "invalidates": [
     "listShifts"
    ]
   },
   {
    "operationId": "getShift",
    "contract": "shift",
    "purpose": "Read a shift",
    "trigger": "onLoad"
   },
   {
    "operationId": "listCashMovements",
    "contract": "shift",
    "purpose": "Lifts, adds and the opening float",
    "trigger": "onLoad"
   },
   {
    "operationId": "recordNoSale",
    "contract": "shift",
    "purpose": "Open the drawer without a sale",
    "trigger": "onAction",
    "invalidates": [
     "listShifts"
    ]
   },
   {
    "operationId": "reopenShift",
    "contract": "shift",
    "purpose": "Reopen a shift closed in error",
    "trigger": "onAction",
    "invalidates": [
     "listShifts"
    ]
   },
   {
    "operationId": "resumeShift",
    "contract": "shift",
    "purpose": "Resume a suspended shift",
    "trigger": "onAction",
    "invalidates": [
     "listShifts"
    ]
   },
   {
    "operationId": "suspendShift",
    "contract": "shift",
    "purpose": "Suspend a shift so another user can log in",
    "trigger": "onAction",
    "invalidates": [
     "listShifts"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "shiftId",
     "from": "session"
    }
   ],
   "coldEntry": "Resolves from the session; a cold arrival is the ordinary case.",
   "preloaded": [
    "Shift.id",
    "Shift.workstationId",
    "Shift.venueId",
    "Shift.scopePath",
    "Shift.principalId"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-039"
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
 }
]
```

## `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
 "acceptShiftVariance": {
  "method": "POST",
  "path": "/shifts/{shiftId}/accept-variance",
  "contract": "shift",
  "summary": "Accept an over/short beyond the threshold",
  "permission": "OVERSHORT_ACCEPT",
  "offlineCapable": false,
  "conflictPolicy": "append",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Shift"
 },
 "addTip": {
  "method": "POST",
  "path": "/payments/{paymentId}/tip",
  "contract": "orders",
  "summary": "Record a tip against a payment",
  "permission": "ORDER_MODIFY",
  "offlineCapable": true,
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
  "responds": "Payment"
 },
 "appendEntitlementToMedia": {
  "method": "POST",
  "path": "/media/{mediaCode}/entitlements",
  "contract": "orders",
  "summary": "Add something to a ticket the guest already holds",
  "permission": "ORDER_CREATE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "workstation",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "AppendEntitlementRequest",
  "responds": "AppendEntitlementResult"
 },
 "applyManualDiscount": {
  "method": "POST",
  "path": "/orders/{orderId}/discounts",
  "contract": "orders",
  "summary": "Apply a discount a cashier chose",
  "permission": "ORDER_DISCOUNT",
  "offlineCapable": true,
  "conflictPolicy": "append",
  "scopeLevel": "workstation",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "ManualDiscountRequest",
  "responds": "Order"
 },
 "approveShiftOpen": {
  "method": "POST",
  "path": "/shifts/{shiftId}/approve-open",
  "contract": "shift",
  "summary": "Approve a shift opening outside tolerance",
  "permission": "SHIFT_APPROVE_OPEN",
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
  "responds": "Shift"
 },
 "askReportingQuestion": {
  "method": "POST",
  "path": "/reports/ask",
  "contract": "reporting",
  "summary": "Natural-language reporting query",
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
  "requestBody": null,
  "responds": "NaturalLanguageAnswer"
 },
 "assessProductChange": {
  "method": "POST",
  "path": "/products/{productId}/change-impact",
  "contract": "catalogue",
  "summary": "What a change would touch, before making it",
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
  "responds": "ProductChangeImpact"
 },
 "capturePayment": {
  "method": "POST",
  "path": "/payments/{paymentId}/capture",
  "contract": "orders",
  "summary": "Capture a previously authorised payment",
  "permission": "ORDER_CREATE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "workstation",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Payment"
 },
 "cloneProduct": {
  "method": "POST",
  "path": "/products/{productId}/clone",
  "contract": "catalogue",
  "summary": "Copy a product as a new draft",
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
 "closeDepositBoxes": {
  "method": "POST",
  "path": "/deposit-boxes/close",
  "contract": "shift",
  "summary": "Close one box or all of them",
  "permission": "SHIFT_CLOSE",
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
  "responds": "DepositBox"
 },
 "closeShift": {
  "method": "POST",
  "path": "/shifts/{shiftId}/close",
  "contract": "shift",
  "summary": "Blind close-out",
  "permission": "SHIFT_CLOSE",
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
  "requestBody": "CloseShiftRequest",
  "responds": "ShiftCloseResult"
 },
 "createCashMovement": {
  "method": "POST",
  "path": "/shifts/{shiftId}/cash-movements",
  "contract": "shift",
  "summary": "Record a cash lift or add",
  "permission": "CASH_LIFT",
  "offlineCapable": true,
  "conflictPolicy": "append",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "CreateCashMovementRequest",
  "responds": "CashMovement"
 },
 "createGroupBooking": {
  "method": "POST",
  "path": "/group-bookings",
  "contract": "orders",
  "summary": "Turn an order into a group booking",
  "permission": "ORDER_CREATE",
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
  "requestBody": "CreateGroupBookingRequest",
  "responds": "GroupBooking"
 },
 "createOrder": {
  "method": "POST",
  "path": "/orders",
  "contract": "orders",
  "summary": "Create an order",
  "permission": "ORDER_CREATE",
  "offlineCapable": true,
  "conflictPolicy": "append",
  "scopeLevel": "workstation",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "CreateOrderRequest",
  "responds": "Order"
 },
 "createPayment": {
  "method": "POST",
  "path": "/payments",
  "contract": "orders",
  "summary": "Take a payment against an order",
  "permission": "ORDER_CREATE",
  "offlineCapable": true,
  "conflictPolicy": "append",
  "scopeLevel": "workstation",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "CreatePaymentRequest",
  "responds": "Payment"
 },
 "createRefund": {
  "method": "POST",
  "path": "/orders/{orderId}/refunds",
  "contract": "orders",
  "summary": "Refund an order, wholly or in part",
  "permission": "ORDER_REFUND",
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
  "requestBody": "CreateRefundRequest",
  "responds": null
 },
 "createRefundRequest": {
  "method": "POST",
  "path": "/refund-requests",
  "contract": "orders",
  "summary": "Guest-initiated refund request",
  "permission": null,
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
 "createReport": {
  "method": "POST",
  "path": "/reports",
  "contract": "reporting",
  "summary": "Create a custom report definition",
  "permission": "REPORT_MANAGE",
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
  "requestBody": "CreateReportRequest",
  "responds": "ReportDefinition"
 },
 "deleteReport": {
  "method": "DELETE",
  "path": "/reports/{reportId}",
  "contract": "reporting",
  "summary": "Retire a report definition",
  "permission": "REPORT_MANAGE",
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
 "exchangeOrderLines": {
  "method": "POST",
  "path": "/orders/{orderId}/exchanges",
  "contract": "orders",
  "summary": "Exchange lines for different products or dates",
  "permission": "ORDER_EXCHANGE",
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
  "requestBody": "ExchangeOrderRequest",
  "responds": "OrderExchangeResult"
 },
 "getCurrentShift": {
  "method": "GET",
  "path": "/shifts/current",
  "contract": "shift",
  "summary": "The open or suspended shift on the session's workstation",
  "permission": "SHIFT_OPEN",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "workstation",
  "parameters": [],
  "requestBody": null,
  "responds": "Shift"
 },
 "getFinancialReport": {
  "method": "GET",
  "path": "/reports/financial",
  "contract": "finance",
  "summary": "Financial statements, revenue and tax summaries",
  "permission": "REPORT_VIEW_VENUE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "report",
    "in": "query",
    "required": true
   },
   {
    "name": "fiscalPeriodId",
    "in": "query",
    "required": true
   },
   {
    "name": "legalEntityId",
    "in": "query",
    "required": null
   },
   {
    "name": "venueId",
    "in": "query",
    "required": null
   },
   {
    "name": "costCenterId",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "FinancialReport"
 },
 "getGroupBooking": {
  "method": "GET",
  "path": "/group-bookings/{groupBookingId}",
  "contract": "orders",
  "summary": "A group, its leader and its name-capture duty",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "GroupBooking"
 },
 "getMediaAsset": {
  "method": "GET",
  "path": "/media/{mediaId}",
  "contract": "assets",
  "summary": "Read an asset with derivatives and usage",
  "permission": "ASSET_LIBRARY_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "MediaAssetDetail"
 },
 "getMediaEntitlements": {
  "method": "GET",
  "path": "/media/{mediaCode}/entitlements",
  "contract": "orders",
  "summary": "What is already on this media",
  "permission": "ORDER_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "MediaEntitlements"
 },
 "getOrder": {
  "method": "GET",
  "path": "/orders/{orderId}",
  "contract": "orders",
  "summary": "Read an order",
  "permission": "ORDER_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "Order"
 },
 "getOrderStatement": {
  "method": "GET",
  "path": "/orders/{orderId}/statement",
  "contract": "orders",
  "summary": "Full financial history of an order",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "OrderStatement"
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
 "getRefundPolicy": {
  "method": "GET",
  "path": "/venues/{venueId}/refund-policy",
  "contract": "orders",
  "summary": "Read a venue's refund policy",
  "permission": "ORDER_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "RefundPolicy"
 },
 "getReport": {
  "method": "GET",
  "path": "/reports/{reportId}",
  "contract": "reporting",
  "summary": "Read a report definition",
  "permission": "REPORT_VIEW_VENUE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ReportDefinition"
 },
 "getSettlement": {
  "method": "GET",
  "path": "/settlements/{settlementId}",
  "contract": "finance",
  "summary": "Settlement detail with match results",
  "permission": "SETTLEMENT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [],
  "requestBody": null,
  "responds": "Settlement"
 },
 "getShift": {
  "method": "GET",
  "path": "/shifts/{shiftId}",
  "contract": "shift",
  "summary": "Read a shift",
  "permission": "REPORT_VIEW_WORKSTATION",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "Shift"
 },
 "holdOrder": {
  "method": "POST",
  "path": "/orders/{orderId}/hold",
  "contract": "orders",
  "summary": "Park a sale and free the till",
  "permission": "ORDER_MODIFY",
  "offlineCapable": true,
  "conflictPolicy": "lastWriterWins",
  "scopeLevel": "workstation",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Order"
 },
 "ingestSettlementFile": {
  "method": "POST",
  "path": "/settlements",
  "contract": "finance",
  "summary": "Ingest a provider settlement file",
  "permission": "SETTLEMENT_RECONCILE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
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
 "inquirePaymentStatus": {
  "method": "POST",
  "path": "/payments/{paymentId}/inquiry",
  "contract": "orders",
  "summary": "Ask the provider what actually happened",
  "permission": "ORDER_CREATE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "workstation",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Payment"
 },
 "listCashMovements": {
  "method": "GET",
  "path": "/shifts/{shiftId}/cash-movements",
  "contract": "shift",
  "summary": "Lifts, adds and the opening float",
  "permission": "REPORT_VIEW_WORKSTATION",
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
 "listConsentQuestions": {
  "method": "GET",
  "path": "/consent-questions",
  "contract": "marketing-crm",
  "summary": "The consent questions a venue asks at booking",
  "permission": "GUEST_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "kind",
    "in": "query",
    "required": null
   },
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
 "listCredentialReplacementReissue": {
  "method": "GET",
  "path": "/credential-replacement-reissue",
  "contract": "access",
  "summary": "Credential Replacement, Reissue, Revocation & Recovery",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "CredentialReplacementReissueRevocationRecoveryView"
 },
 "listOrderRefunds": {
  "method": "GET",
  "path": "/orders/{orderId}/refunds",
  "contract": "orders",
  "summary": "List refunds against an order",
  "permission": "ORDER_VIEW",
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
 "listOrders": {
  "method": "GET",
  "path": "/orders",
  "contract": "orders",
  "summary": "List orders",
  "permission": "ORDER_VIEW",
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
    "name": "principalId",
    "in": "query",
    "required": null
   },
   {
    "name": "shiftId",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "createdFrom",
    "in": "query",
    "required": null
   },
   {
    "name": "createdTo",
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
 "listProductVersions": {
  "method": "GET",
  "path": "/products/{productId}/versions",
  "contract": "catalogue",
  "summary": "What this product used to be",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ProductVersion"
 },
 "listReports": {
  "method": "GET",
  "path": "/reports",
  "contract": "reporting",
  "summary": "List available report definitions",
  "permission": "REPORT_VIEW_VENUE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "category",
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
 "listSettlementExceptions": {
  "method": "GET",
  "path": "/settlements/{settlementId}/exceptions",
  "contract": "finance",
  "summary": "Unmatched or mismatched settlement lines",
  "permission": "SETTLEMENT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
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
 "listSettlements": {
  "method": "GET",
  "path": "/settlements",
  "contract": "finance",
  "summary": "List settlement batches",
  "permission": "SETTLEMENT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [
   {
    "name": "providerName",
    "in": "query",
    "required": null
   },
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
 "listShifts": {
  "method": "GET",
  "path": "/shifts",
  "contract": "shift",
  "summary": "List shifts",
  "permission": "REPORT_VIEW_WORKSTATION",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "workstationId",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "openedFrom",
    "in": "query",
    "required": null
   },
   {
    "name": "openedTo",
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
 "listTicketReissueFulfillment": {
  "method": "GET",
  "path": "/ticket-reissue-fulfillment",
  "contract": "orders",
  "summary": "Ticket Reissue & Fulfillment Regeneration",
  "permission": "ORDER_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "TicketReissueFulfillmentRegenerationView"
 },
 "modifyOrder": {
  "method": "POST",
  "path": "/orders/{orderId}/modify",
  "contract": "orders",
  "summary": "Add or remove lines on an existing order",
  "permission": "ORDER_MODIFY",
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
  "requestBody": "ModifyOrderRequest",
  "responds": "OrderModificationResult"
 },
 "openShift": {
  "method": "POST",
  "path": "/shifts",
  "contract": "shift",
  "summary": "Open a shift",
  "permission": "SHIFT_OPEN",
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
  "requestBody": "OpenShiftRequest",
  "responds": "Shift"
 },
 "recordNoSale": {
  "method": "POST",
  "path": "/shifts/{shiftId}/no-sale",
  "contract": "shift",
  "summary": "Open the Deposit Box without a sale",
  "permission": "CASH_NO_SALE",
  "offlineCapable": true,
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
  "responds": "NoSaleEvent"
 },
 "reopenShift": {
  "method": "POST",
  "path": "/shifts/{shiftId}/reopen",
  "contract": "shift",
  "summary": "Reopen a shift closed in error",
  "permission": "SHIFT_REOPEN",
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
  "responds": "Shift"
 },
 "replaceMediaAsset": {
  "method": "POST",
  "path": "/media/{mediaId}/replace",
  "contract": "assets",
  "summary": "Replace the file behind an asset",
  "permission": "ASSET_LIBRARY_MANAGE",
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
  "responds": "MediaReplaceResult"
 },
 "reprintOrder": {
  "method": "POST",
  "path": "/orders/{orderId}/reprints",
  "contract": "orders",
  "summary": "Reprint or resend tickets",
  "permission": "ORDER_REPRINT",
  "offlineCapable": true,
  "conflictPolicy": "append",
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
 "rescheduleOrder": {
  "method": "POST",
  "path": "/orders/{orderId}/reschedule",
  "contract": "orders",
  "summary": "Move an order to another performance",
  "permission": "ORDER_RESCHEDULE",
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
  "responds": "OrderExchangeResult"
 },
 "resolveSettlementException": {
  "method": "POST",
  "path": "/settlements/{settlementId}/exceptions",
  "contract": "finance",
  "summary": "Resolve a settlement exception",
  "permission": "SETTLEMENT_RECONCILE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "SettlementException"
 },
 "restoreProductVersion": {
  "method": "POST",
  "path": "/products/{productId}/versions/{version}/restore",
  "contract": "catalogue",
  "summary": "Put a previous version back",
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
 "resumeOrder": {
  "method": "POST",
  "path": "/orders/{orderId}/resume",
  "contract": "orders",
  "summary": "Bring a parked sale back to a till",
  "permission": "ORDER_MODIFY",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "workstation",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "OrderResumeResult"
 },
 "resumeShift": {
  "method": "POST",
  "path": "/shifts/{shiftId}/resume",
  "contract": "shift",
  "summary": "Resume a suspended shift",
  "permission": "SHIFT_OPEN",
  "offlineCapable": true,
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
  "responds": "Shift"
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
 "saveNaturalLanguageQuery": {
  "method": "POST",
  "path": "/reports/ask/{conversationId}/save",
  "contract": "reporting",
  "summary": "Save a natural-language answer as a report definition",
  "permission": "REPORT_MANAGE",
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
  "responds": "ReportDefinition"
 },
 "searchMedia": {
  "method": "GET",
  "path": "/media",
  "contract": "assets",
  "summary": "Search the asset library",
  "permission": "ASSET_LIBRARY_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "kind",
    "in": "query",
    "required": null
   },
   {
    "name": "tag",
    "in": "query",
    "required": null
   },
   {
    "name": "collectionId",
    "in": "query",
    "required": null
   },
   {
    "name": "venueId",
    "in": "query",
    "required": null
   },
   {
    "name": "search",
    "in": "query",
    "required": null
   },
   {
    "name": "unusedOnly",
    "in": "query",
    "required": null
   },
   {
    "name": "rightsExpiringWithinDays",
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
 "settleDeposit": {
  "method": "POST",
  "path": "/deposits/{depositId}/settle",
  "contract": "finance",
  "summary": "Convert to revenue, return it, or forfeit it",
  "permission": "LEDGER_POST",
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
  "responds": "Deposit"
 },
 "suspendShift": {
  "method": "POST",
  "path": "/shifts/{shiftId}/suspend",
  "contract": "shift",
  "summary": "Suspend a shift so another user can log in",
  "permission": "SHIFT_SUSPEND",
  "offlineCapable": true,
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
  "responds": "Shift"
 },
 "updateGroupBooking": {
  "method": "PATCH",
  "path": "/group-bookings/{groupBookingId}",
  "contract": "orders",
  "summary": "Confirm numbers, change the leader or cancel a group",
  "permission": "ORDER_MODIFY",
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
  "requestBody": "UpdateGroupBookingRequest",
  "responds": "GroupBooking"
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
 "updateProductVariant": {
  "method": "PATCH",
  "path": "/products/{productId}/variants/{variantId}",
  "contract": "catalogue",
  "summary": "Describe a variant",
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
  "responds": "ProductVariant"
 },
 "updateReport": {
  "method": "PUT",
  "path": "/reports/{reportId}",
  "contract": "reporting",
  "summary": "Publish a new version of a definition",
  "permission": "REPORT_MANAGE",
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
  "requestBody": "CreateReportRequest",
  "responds": "ReportDefinition"
 },
 "voidOrder": {
  "method": "POST",
  "path": "/orders/{orderId}/voids",
  "contract": "orders",
  "summary": "Void an order",
  "permission": "ORDER_VOID",
  "offlineCapable": true,
  "conflictPolicy": "append",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Order"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AppendEntitlementRequest": {
  "type": "object",
  "x-ticvai-persistence": "none — request only",
  "required": [
   "id",
   "lines",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "Client-generated ULID of the new order this creates, and its idempotency key — it must equal the `Idempotency-Key` header."
   },
   "lines": {
    "type": "array",
    "minItems": 1,
    "items": {
     "type": "object",
     "required": [
      "variantId",
      "quantity"
     ],
     "properties": {
      "variantId": {
       "type": "string",
       "format": "uuid"
      },
      "quantity": {
       "type": "integer",
       "minimum": 1
      },
      "performanceId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      }
     }
    }
   },
   "paymentMethod": {
    "type": "string",
    "enum": [
     "card",
     "cash",
     "wallet",
     "giftCard",
     "chargeToAccount"
    ]
   },
   "note": {
    "type": "string",
    "maxLength": 300
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "AppendEntitlementResult": {
  "type": "object",
  "x-ticvai-persistence": "none — computed",
  "required": [
   "order",
   "media"
  ],
  "properties": {
   "order": {
    "allOf": [
     {
      "$ref": "#/components/schemas/Order"
     }
    ],
    "description": "A **new** order. The original is untouched — it was paid, receipted and possibly reported on, and editing it would move yesterday's revenue.\n"
   },
   "media": {
    "allOf": [
     {
      "$ref": "#/components/schemas/MediaEntitlements"
     }
    ],
    "description": "The full set now on the media, so the cashier can say what the QR does."
   },
   "addedEntitlementIds": {
    "type": "array",
    "items": {
     "type": "string",
     "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
    }
   }
  }
 },
 "CashMovement": {
  "x-ticvai-persistence": "orders.cash_movement",
  "allOf": [
   {
    "$ref": "#/components/schemas/CreateCashMovementRequest"
   },
   {
    "type": "object",
    "required": [
     "shiftId",
     "authorisedByPrincipalId",
     "sequence"
    ],
    "properties": {
     "shiftId": {
      "type": "string",
      "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
     },
     "depositBoxId": {
      "type": "string",
      "format": "uuid",
      "nullable": true,
      "description": "The box the cash moved in or out of. Set on every lift `withdrawFromDepositBox` records (26 September, pull audit R099).\n"
     },
     "witnessPrincipalId": {
      "type": "string",
      "format": "uuid",
      "nullable": true,
      "description": "The cashier who countersigned a withdrawal. Null on other movements."
     },
     "withdrawalReason": {
      "allOf": [
       {
        "$ref": "#/components/schemas/WithdrawalReason"
       }
      ],
      "nullable": true
     },
     "authorisedByPrincipalId": {
      "type": "string",
      "format": "uuid",
      "description": "The principal who authorised the movement, recorded for audit."
     },
     "sequence": {
      "type": "integer",
      "description": "Monotonic within the shift. Preserves order across an offline batch."
     },
     "syncedAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     }
    }
   }
  ]
 },
 "CashMovementKind": {
  "type": "string",
  "enum": [
   "openingFloat",
   "lift",
   "add"
  ],
  "description": "`openingFloat` is written by `openShift`; `lift` by `createCashMovement` and by `withdrawFromDepositBox`, which is a lift from one cashier's box; `add` by `createCashMovement`.\n"
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
 "CloseShiftRequest": {
  "type": "object",
  "required": [
   "countedCash",
   "recordedAt"
  ],
  "properties": {
   "countedCash": {
    "type": "array",
    "minItems": 1,
    "description": "**The cashier's blind count, one line per denomination counted** (decided 29 September, readiness close-out; our build plan). The server writes each line as one `CashCountLine` (`countKind` close) against the shift, taking the face value from `platform.denomination`. A denomination may appear once; a repeat is refused with 422 `duplicate-denomination`.\n",
    "items": {
     "$ref": "#/components/schemas/CountedDenominationLine"
    }
   },
   "nonCashDeclared": {
    "type": "array",
    "description": "Declared totals per non-cash tender, for reconciliation against captured payments.\n",
    "items": {
     "type": "object",
     "required": [
      "tender",
      "amount"
     ],
     "properties": {
      "tender": {
       "type": "string"
      },
      "amount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      }
     }
    }
   },
   "notes": {
    "type": "string",
    "maxLength": 1000
   },
   "releaseHeldLeases": {
    "type": "boolean",
    "default": true,
    "description": "Return unsold inventory leases held by this workstation (ADR-0013 C103). Closing without releasing strands capacity until TTL expiry, which is visible at a gate during peak.\n"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "CountedDenominationLine": {
  "type": "object",
  "x-ticvai-persistence": "none — request only; lands as `CashCountLine` rows",
  "description": "**One line of a cash count as the cashier types it: which note or coin, how many, and what they come to** (decided 29 September, readiness close-out; our build plan). The shape of the blind count on close (`closeShift`) and of the count columns on the till screens (POS-007, POS-011). It is the request side of `CashCountLine`, which is the stored row and adds the shift, the count kind, who counted and when.\n**`total` is shown to the cashier and checked, not trusted**: the server recomputes `count` times the denomination's face value and refuses a line whose `total` disagrees with 422 `count-total-mismatch`. An inactive or unknown denomination is refused with 422 `unknown-denomination`.\n",
  "required": [
   "denominationId",
   "count"
  ],
  "properties": {
   "denominationId": {
    "type": "string",
    "format": "uuid",
    "description": "References `platform.denomination` (`Denomination.id`) — face value, kind and counting order live there."
   },
   "count": {
    "type": "integer",
    "minimum": 0,
    "maximum": 100000,
    "description": "**How many of this note or coin were counted.** Zero is a line, not an omission: a denomination counted and found empty."
   },
   "total": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "`count` times the face value, in the denomination's currency. Optional on the way in (the server computes it) and checked when sent.\n"
   }
  }
 },
 "CreateCashMovementRequest": {
  "type": "object",
  "required": [
   "id",
   "kind",
   "amount",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "Client-generated ULID."
   },
   "kind": {
    "$ref": "#/components/schemas/CashMovementKind"
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "denominations": {
    "$ref": "#/components/schemas/DenominationCount",
    "x-ticvai-persisted": false,
    "description": "**Stored as `orders.cash_count_line` rows** with `countKind: movement` and this movement's `cashMovementId`, not as a column. The jsonb blob this used to land in is what `Denomination` was created to replace (26 September, pull audit R099).\n"
   },
   "reference": {
    "type": "string",
    "maxLength": 64,
    "description": "Safe drop reference or bag number."
   },
   "reason": {
    "type": "string",
    "maxLength": 500
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "CreateGroupBookingRequest": {
  "type": "object",
  "description": "Request only. Persisted as `GroupBooking`.",
  "required": [
   "orderId",
   "leaderSubjectId",
   "expectedSize"
  ],
  "properties": {
   "kind": {
    "type": "string",
    "enum": [
     "general",
     "school",
     "corporate",
     "party"
    ],
    "default": "general"
   },
   "packageProductId": {
    "type": "string",
    "nullable": true,
    "description": "The school-trip format or party package."
   },
   "yearGroup": {
    "type": "string",
    "maxLength": 40,
    "nullable": true
   },
   "accessAndDietaryNeeds": {
    "type": "string",
    "maxLength": 1000,
    "nullable": true
   },
   "celebrantName": {
    "type": "string",
    "maxLength": 120,
    "nullable": true,
    "description": "The birthday child."
   },
   "celebrantTurningAge": {
    "type": "integer",
    "minimum": 1,
    "maximum": 18,
    "nullable": true
   },
   "allergiesAndRequests": {
    "type": "string",
    "maxLength": 1000,
    "nullable": true
   },
   "finalHeadcountDueBy": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "orderId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "leaderSubjectId": {
    "type": "string",
    "format": "uuid",
    "description": "The person who pays, is called if the coach is late, and collects the names."
   },
   "organisationName": {
    "type": "string",
    "maxLength": 200,
    "nullable": true
   },
   "expectedSize": {
    "type": "integer",
    "minimum": 2
   },
   "minimumSize": {
    "type": "integer",
    "minimum": 1,
    "nullable": true
   },
   "attendeeCaptureRequired": {
    "type": "boolean",
    "default": false
   },
   "attendeeCaptureDueBy": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "CreateOrderLine": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "id",
   "variantId",
   "quantity",
   "quotedUnitPrice"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "Client-generated ULID of the line. `lineIds` everywhere in this contract are these."
   },
   "variantId": {
    "type": "string",
    "format": "uuid"
   },
   "performanceId": {
    "type": "string",
    "format": "uuid"
   },
   "bookedWindow": {
    "$ref": "#/components/schemas/BookedWindow"
   },
   "inventoryHoldId": {
    "type": "string",
    "nullable": true,
    "description": "Lease the units were drawn from — a `catalogue.InventoryHold.id`. Absent for uncontended products."
   },
   "seatIds": {
    "type": "array",
    "maxItems": 50,
    "items": {
     "type": "string",
     "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
    },
    "description": "Seated products only, as `seating.Seat.id`. Not available offline. **At most `VenueSettings.seating.maxSeatsPerGuestOrder` seats per booking on a guest channel** (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); **at most 10 per sale on staff and POS** (audit R080 (c)), across all the lines of one order for one performance. `createOrder` refuses more with 422 `seatLimitExceeded` (problem type `seat-limit-exceeded`)."
   },
   "resourceHoldId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "nullable": true,
    "description": "A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant. `createOrder` converts the hold into a `ResourceBooking` without releasing it. Not available offline."
   },
   "attributes": {
    "$ref": "#/components/schemas/OrderLineAttributes"
   },
   "quantity": {
    "type": "integer",
    "minimum": 1
   },
   "eligibilityDeclaration": {
    "type": "array",
    "nullable": true,
    "x-ticvai-note": "One row per declared guest in `orders.order_line_eligibility` (named on `OrderLine`), because an array of objects is a child table's rows, not a column.\n",
    "items": {
     "type": "object",
     "properties": {
      "ageBand": {
       "type": "string",
       "enum": [
        "infant",
        "child",
        "junior",
        "adult",
        "senior"
       ],
       "description": "Infant under 3, child 3–12, junior 13–17, adult 18–59, senior 60+."
      },
      "ageYears": {
       "type": "integer",
       "nullable": true
      },
      "heightBandIndex": {
       "type": "integer",
       "nullable": true
      },
      "confidentSwimmer": {
       "type": "boolean",
       "nullable": true,
       "description": "**Derived, kept for the gate check** (decided 29 September, rev 3 REV3-26). The swim question is a consent: the answer is a `marketing.BookingConsentRecord` of kind `swim`, and this is filled from it (true for a `yes` covering this person, whether answered for them or once for the booking). A value sent that contradicts the record is ignored and the record wins. No longer the place a swim answer is captured.\n"
      },
      "guardianSigned": {
       "type": "boolean"
      }
     }
    },
    "description": "What was declared for each guest on this line, kept as the record staff check at the gate."
   },
   "quotedUnitPrice": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "What the client charged, from its local bundle."
   },
   "holderName": {
    "type": "string",
    "nullable": true
   },
   "dataMaskValues": {
    "type": "object",
    "additionalProperties": true,
    "description": "**Deliberately open.** Custom fields keyed by the venue's data mask: the field definitions travel in the catalogue bundle (`catalogue.CatalogueBundle.payload`), so the keys are the venue's to define, as on `catalogue`'s own `dataMaskValues`.\n"
   }
  }
 },
 "CreateOrderRequest": {
  "type": "object",
  "required": [
   "id",
   "venueId",
   "channel",
   "lines",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "Client-generated ULID. Also the idempotency key: it must equal the `Idempotency-Key` header, and a replay or a mismatch follows `IdempotencyKey` in `shared/common.yaml`. Offline replay through `syncOrders` carries no header, and this id alone deduplicates there.\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "channel": {
    "$ref": "#/components/schemas/Channel"
   },
   "shiftId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Null for an anonymous sale. Identity and entitlement are separate."
   },
   "guestLinkId": {
    "type": "string",
    "nullable": true,
    "description": "Present where the guest is linked across cells."
   },
   "catalogueBundleVersion": {
    "type": "string",
    "description": "The bundle the client priced from. Lets the server explain a variance rather than merely report one.\n"
   },
   "lines": {
    "type": "array",
    "minItems": 1,
    "items": {
     "$ref": "#/components/schemas/CreateOrderLine"
    }
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "CreatePaymentRequest": {
  "type": "object",
  "required": [
   "id",
   "orderId",
   "tender",
   "amount",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "Client-generated ULID of the payment, and its idempotency key — it must equal the `Idempotency-Key` header."
   },
   "orderId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "tender": {
    "$ref": "#/components/schemas/TenderKind"
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "tenderCurrency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "nullable": true,
    "description": "The currency the guest handed over, where it is not the venue's — becomes `Payment.tenderCurrency`. Omit for a payment in the venue's own currency."
   },
   "tenderAmount": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "**What the guest handed over**, in `tenderCurrency` — becomes `Payment.tenderAmount`, one name for one concept (renamed from `tenderedAmount` on 26 September). For cash, change is the difference.\n"
   },
   "walletAuthorisationId": {
    "type": "string",
    "nullable": true,
    "description": "Cross-cell wallet hold, where the guest's home cell is elsewhere."
   },
   "deviceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "CreateRefundRequest": {
  "type": "object",
  "required": [
   "id",
   "amount",
   "reason",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "Client-generated ULID of the refund, and its idempotency key — it must equal the `Idempotency-Key` header."
   },
   "lineIds": {
    "type": "array",
    "items": {
     "type": "string",
     "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
    },
    "description": "Omit to refund the whole order."
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "reason": {
    "type": "string",
    "minLength": 3,
    "maxLength": 500
   },
   "secondaryAuthorisation": {
    "type": "object",
    "description": "Required above the venue's `requiresSecondUserAbove`. A second user — cashier or supervisor — names themselves. This is dual-authorisation, not escalation.\n",
    "required": [
     "principalId",
     "credential"
    ],
    "properties": {
     "principalId": {
      "type": "string",
      "format": "uuid"
     },
     "credential": {
      "type": "string",
      "maxLength": 512,
      "description": "The second person's staff PIN, as they sign in at a till with it. **A PIN, never a password** (decided 28 September, audit R123 (7))."
     }
    }
   },
   "refundToOriginalTender": {
    "type": "boolean",
    "default": true
   },
   "alternateTender": {
    "$ref": "#/components/schemas/TenderKind"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "CreateReportRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "name",
   "category",
   "dataSource",
   "columns",
   "requiredPermission"
  ],
  "properties": {
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "description": {
    "type": "string",
    "maxLength": 1000
   },
   "category": {
    "$ref": "#/components/schemas/ReportCategory"
   },
   "dataSource": {
    "$ref": "#/components/schemas/DataSource"
   },
   "columns": {
    "type": "array",
    "minItems": 1,
    "items": {
     "$ref": "#/components/schemas/ReportColumn"
    }
   },
   "filters": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/ReportFilter"
    }
   },
   "groupBy": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "parameters": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/ReportParameter"
    }
   },
   "requiredPermission": {
    "$ref": "../shared/permissions.yaml#/components/schemas/Permission",
    "description": "Permission needed to run this report, from the shared `Permission` vocabulary. **The author cannot assign one they do not hold** — otherwise a venue user could build themselves a tenant-wide view.\n"
   },
   "maxDateRangeDays": {
    "type": "integer",
    "nullable": true,
    "minimum": 1,
    "default": 366,
    "description": "Guards against a query spanning years of scan events. **When a report sets none, 366 days applies (decided 28 September, audit R158)**, so `runReport`'s date-range 400 always has a limit."
   }
  }
 },
 "CredentialReplacementReissueRevocationRecoveryView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over access state, assembled at read time from tables that already exist",
  "description": "**What Credential Replacement, Reissue, Revocation & Recovery displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "reason": {
    "type": "string",
    "enum": [
     "lost",
     "stolen",
     "damaged",
     "compromised",
     "customerChangedPhone",
     "rfidFailure",
     "wristbandReplacement",
     "qrCompromise",
     "walletReplacement",
     "faceReEnrollment",
     "incorrectAssignment"
    ],
    "description": "Replacement reason this policy covers"
   },
   "immediateOldMediaRevocation": {
    "type": "boolean",
    "description": "Immediate old-media revocation"
   },
   "gracePeriod": {
    "type": "string",
    "description": "ISO 8601 duration, e.g. PT30M"
   },
   "maximumReplacements": {
    "type": "integer",
    "description": "Maximum replacements"
   },
   "identityVerification": {
    "type": "boolean",
    "description": "Identity verification"
   },
   "supervisorApproval": {
    "type": "boolean",
    "description": "Supervisor approval"
   },
   "reasonCodes": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Reason codes"
   },
   "recoveryAllowed": {
    "type": "boolean",
    "description": "A suspended credential may be restored under this policy"
   }
  },
  "required": [
   "reason"
  ]
 },
 "DataSource": {
  "type": "string",
  "description": "What a report may be built over. **A closed set, and that is the point** — a builder that accepts any table will happily produce a report over data nobody maintains.\n**Eight sources added 18 August** (BL-143), each because the matrix asks for a report the builder could not source. `stockCounts` and `waste`: 6.1.21 wants count variance and `stockMovements` records the movement rather than **the count that found the discrepancy**. `workstations`, `devices` and `principals`: 6.1.28 — **who did what at which till** is the question an auditor asks first and it had no source. `loyalty`: 6.1.37, points earned, burned and expiring. `reviews`: 6.1.46. `queueEntries`: **wait times are already measured and nothing could report on them.**\n**Adding a source is a decision, not an omission.** `principals`, `guests`, `loyalty` and `reviews` all name a person, and `REPORT_EXPORT_PII` gates them.\n",
  "enum": [
   "orders",
   "orderLines",
   "payments",
   "refunds",
   "shifts",
   "scanEvents",
   "entitlements",
   "products",
   "inventory",
   "stockMovements",
   "stockCounts",
   "waste",
   "workstations",
   "devices",
   "principals",
   "loyalty",
   "reviews",
   "queueEntries",
   "guests",
   "campaigns",
   "cases",
   "ledgerEntries",
   "workOrders",
   "approvals",
   "purchaseOrders",
   "receipts",
   "requisitions",
   "stockBatches",
   "resourceBookings",
   "delegations",
   "forms",
   "challenges",
   "wallets",
   "resaleListings"
  ]
 },
 "DenominationCount": {
  "type": "array",
  "description": "**A count is a list of lines and the line is the row.** Until 24 August this array carried the persistence hint itself, so `orders.cash_count_line` derived a single column — `shift_id` — and a count line had no denomination, no quantity and no variance.\n**The array is the transport; `CashCountLine` is the row.**\n",
  "items": {
   "$ref": "#/components/schemas/CashCountLine"
  },
  "minItems": 1
 },
 "Deposit": {
  "type": "object",
  "x-ticvai-persistence": "ledger.deposit",
  "description": "**Money taken before the sale is complete.** Not deferred revenue — that is a sold entitlement not yet consumed, and the sale happened.\n",
  "required": [
   "id",
   "amount",
   "reason",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "reason": {
    "type": "string",
    "enum": [
     "reservation",
     "rental",
     "event",
     "damageBond",
     "other"
    ]
   },
   "status": {
    "type": "string",
    "enum": [
     "held",
     "convertedToRevenue",
     "returned",
     "forfeited",
     "partiallyForfeited"
    ]
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "orderId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "nullable": true
   },
   "bookingId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "refundableUntil": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "**After which a forfeit is permitted rather than a return.** The date is the cancellation term, and a deposit with no date is refundable indefinitely.\n"
   },
   "liabilityAccountId": {
    "type": "string",
    "format": "uuid"
   },
   "settledAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "DepositBox": {
  "type": "object",
  "x-ticvai-persistence": "orders.deposit_box + orders.deposit_box_opening_denomination + orders.deposit_box_foreign_holding",
  "description": "5.8. **Allocated to a cashier, not to a workstation.** A cashier moving between tills takes their float with them, which is what makes a variance attributable to a person.\n**`openingDenominations` and `foreignHoldings` are child rows** (26 September, pull audit R099): `orders.deposit_box_opening_denomination` and `orders.deposit_box_foreign_holding`, one row per item, keyed to the box. Until then the contract carried both and the table had nowhere to put either.\n",
  "required": [
   "cashierPrincipalId",
   "venueId",
   "openingFloat"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "cashierPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "cashierName": {
    "type": "string",
    "readOnly": true
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "workstationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Where it is being used now. **Changes during a shift; the box does not.**"
   },
   "shiftId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "nullable": true,
    "description": "The shift trading from this box. A ULID, as `Shift.id` is."
   },
   "status": {
    "$ref": "#/components/schemas/DepositBoxStatus"
   },
   "openingFloat": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "openingDenominations": {
    "type": "array",
    "description": "5.8.3. **Either this or a total** — a supervisor handing over a counted bag should not have to re-count it into fields. POS-001 offered only denominations until 14 August.\n",
    "items": {
     "type": "object",
     "required": [
      "denominationId",
      "count"
     ],
     "properties": {
      "denominationId": {
       "type": "string",
       "format": "uuid",
       "description": "References `platform.denomination`, as `CashCountLine.denominationId` does. Until 26 September this was `denomination: number` — a face value as a JSON float, which naming-and-style 5.1 forbids and which could disagree with the note it named (pull audit R122).\n"
      },
      "count": {
       "type": "integer",
       "minimum": 0
      }
     }
    }
   },
   "withdrawnTotal": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "readOnly": true,
    "description": "**Reduces the expected close figure.** Cash skimmed for banking is not a shortfall, and a system that treats it as one makes every busy cashier look short.\n"
   },
   "foreignHoldings": {
    "type": "array",
    "description": "4.6.11 and 6.1.10. **Foreign cash accepted at this till, counted separately by currency.** A till taking USD and EUR alongside AED has three counts and three variances — collapsing them into a base-currency total makes a variance unattributable to the currency that caused it.\n**No opening float in a foreign currency and no change given in one.** Foreign cash only ever comes in, which is what keeps this to one number per currency rather than a full reconciliation each.\n",
    "items": {
     "type": "object",
     "required": [
      "currency",
      "countedAmount"
     ],
     "properties": {
      "currency": {
       "type": "string",
       "pattern": "^[A-Z]{3}$",
       "description": "**Stored, because it is the one thing that is not the region's.** A foreign holding is by definition cash in a currency the till does not trade in, so it cannot resolve from the region (ADR-0018) the way the box's own amounts do; it is the key of the row, one per currency per box. The amounts on this item are in this currency.\n"
      },
      "expectedAmount": {
       "allOf": [
        {
         "$ref": "../shared/common.yaml#/components/schemas/Money"
        }
       ],
       "description": "The sum of tenders taken in this currency during the shift."
      },
      "countedAmount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "variance": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "baseEquivalent": {
       "allOf": [
        {
         "$ref": "../shared/common.yaml#/components/schemas/Money"
        }
       ],
       "description": "**At the rates on the payments, not today's.** A shift closed on Friday and reviewed on Monday is reviewed at Friday's rates (CF-37).\n"
      }
     }
    }
   },
   "expectedTotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "countedTotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "variance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "closedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**Flagged where it is not the holder.** A box closed without its holder present is allowed — the cash is counted by somebody, and who counted it is the record.\n"
   },
   "allocatedAt": {
    "type": "string",
    "format": "date-time",
    "description": "When the device recorded the allocation. `allocateDepositBox` is offline-capable, so for a box allocated offline this differs from the server's receipt time.\n"
   },
   "closedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "DepositBoxStatus": {
  "type": "string",
  "enum": [
   "allocated",
   "open",
   "suspended",
   "closing",
   "closed",
   "reconciled"
  ]
 },
 "EntitlementStatus": {
  "type": "string",
  "description": "**What the storage layer holds, and what a guest is shown.** `MediaEntitlements` carried only `isValid` and a reason string — a boolean cannot distinguish a ticket that was used from one that expired, was refunded, or was transferred to somebody else, and those are four different conversations at a gate.\nAdded 17 August. `states/entitlement.yaml` had modelled these six since 14 August and the contract had no enum behind it, which the state checker reported correctly for three days.\n",
  "enum": [
   "issued",
   "partiallyConsumed",
   "fullyConsumed",
   "expired",
   "cancelled",
   "surrendered"
  ]
 },
 "ExchangeOrderRequest": {
  "type": "object",
  "required": [
   "id",
   "outgoingLineIds",
   "incomingLines",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "Client-generated ULID of this exchange, and its idempotency key — it must equal the `Idempotency-Key` header."
   },
   "outgoingLineIds": {
    "type": "array",
    "minItems": 1,
    "items": {
     "type": "string",
     "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
    }
   },
   "incomingLines": {
    "type": "array",
    "minItems": 1,
    "items": {
     "$ref": "#/components/schemas/CreateOrderLine"
    }
   },
   "waiveFee": {
    "type": "boolean",
    "default": false
   },
   "reason": {
    "type": "string",
    "maxLength": 500
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "ExchangeRateDecimal": {
  "type": "string",
  "x-ticvai-persistence-kind": "valueObject",
  "x-ticvai-persistence-column": "numeric(18,6)",
  "description": "**An exchange rate: a decimal string, never a float**, for the reason `Money.amount` is one — a JavaScript client must not round a rate in transit. **Six decimal places**, the precision `finance.FxRate.rate` asks for, and stored at that precision.\n",
  "pattern": "^\\d+(\\.\\d{1,6})?$"
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
 "FinancialReport": {
  "x-ticvai-persistence": "none — computed from replica",
  "type": "object",
  "required": [
   "report",
   "fiscalPeriodId",
   "currency",
   "generatedAt",
   "sections"
  ],
  "properties": {
   "report": {
    "$ref": "#/components/schemas/FinancialReportKind"
   },
   "fiscalPeriodId": {
    "type": "string",
    "format": "uuid"
   },
   "legalEntityId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "currency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$"
   },
   "currencyScale": {
    "type": "integer"
   },
   "generatedAt": {
    "type": "string",
    "format": "date-time"
   },
   "sections": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "name",
      "lines",
      "total"
     ],
     "properties": {
      "name": {
       "type": "string"
      },
      "lines": {
       "type": "array",
       "items": {
        "type": "object",
        "properties": {
         "label": {
          "type": "string"
         },
         "accountCode": {
          "type": "string",
          "nullable": true
         },
         "amount": {
          "$ref": "../shared/common.yaml#/components/schemas/Money"
         },
         "priorPeriodAmount": {
          "allOf": [
           {
            "$ref": "../shared/common.yaml#/components/schemas/Money"
           }
          ],
          "description": "The same line for **the same period last year** (decided 28 September, audit R127 (3)). Absent where that period did not exist."
         }
        }
       }
      },
      "total": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      }
     }
    }
   }
  }
 },
 "FinancialReportKind": {
  "type": "string",
  "description": "The report `getFinancialReport` returns. One vocabulary for the query and the response.",
  "enum": [
   "profitAndLoss",
   "balanceSheet",
   "cashFlow",
   "revenueByVenue",
   "revenueByProduct",
   "taxSummary"
  ]
 },
 "GeneratedQuery": {
  "x-ticvai-persistence": "none — embedded; stored whole in `reporting.natural_language_query`",
  "type": "object",
  "description": "The structured query a natural-language question produced — data source, columns, filters, grouping. Named on 26 September so the answer and the kept copy are one shape.\n",
  "properties": {
   "dataSource": {
    "$ref": "#/components/schemas/DataSource"
   },
   "columns": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/ReportColumn"
    }
   },
   "filters": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/ReportFilter"
    }
   },
   "groupBy": {
    "type": "array",
    "items": {
     "type": "string"
    }
   }
  }
 },
 "GroupBooking": {
  "type": "object",
  "x-ticvai-persistence": "orders.group_booking",
  "description": "BL-028. **`BO-026 Group Bookings` ran on generic order operations** — no group size, no quota, no leader, no per-attendee capture.\n**The leader is the point.** A school booking forty places has one person who pays, one who is called if the coach is late, and forty who need names collecting — and a generic order has one guest.\n",
  "required": [
   "id",
   "orderId",
   "leaderSubjectId",
   "expectedSize",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "type": "string",
    "enum": [
     "general",
     "school",
     "corporate",
     "party"
    ],
    "default": "general"
   },
   "packageProductId": {
    "type": "string",
    "nullable": true,
    "description": "The school-trip format or party package."
   },
   "yearGroup": {
    "type": "string",
    "maxLength": 40,
    "nullable": true
   },
   "accessAndDietaryNeeds": {
    "type": "string",
    "maxLength": 1000,
    "nullable": true
   },
   "celebrantName": {
    "type": "string",
    "maxLength": 120,
    "nullable": true,
    "description": "The birthday child."
   },
   "celebrantTurningAge": {
    "type": "integer",
    "minimum": 1,
    "maximum": 18,
    "nullable": true
   },
   "allergiesAndRequests": {
    "type": "string",
    "maxLength": 1000,
    "nullable": true
   },
   "finalHeadcountDueBy": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "quoteSentAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "riskAssessmentSentAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   },
   "preferredDate": {
    "type": "string",
    "format": "date",
    "nullable": true,
    "description": "The date the guest asked for on `requestGroupBooking` — what its `409 dateUnavailable` is checked against. Null for a group a member of staff built from an order."
   },
   "orderId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "leaderSubjectId": {
    "type": "string",
    "format": "uuid"
   },
   "organisationName": {
    "type": "string",
    "nullable": true
   },
   "expectedSize": {
    "type": "integer"
   },
   "confirmedSize": {
    "type": "integer",
    "nullable": true
   },
   "minimumSize": {
    "type": "integer",
    "nullable": true,
    "description": "**Below which the group rate does not apply.** A booking for forty that arrives as twelve is a pricing question somebody has to answer at the gate, and stating the threshold means answering it at booking instead.\n"
   },
   "attendeeCaptureRequired": {
    "type": "boolean",
    "default": false,
    "description": "**Whether names are needed before admission.** A school trip usually needs them and a corporate day out usually does not, and the difference is a safeguarding requirement rather than a preference.\n"
   },
   "attendeeCaptureDueBy": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "provisional",
     "confirmed",
     "namesPending",
     "complete",
     "cancelled"
    ]
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
 "ManualDiscountRequest": {
  "type": "object",
  "x-ticvai-persistence": "none — request only",
  "required": [
   "id",
   "reason",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "Client-generated ULID of this discount, and its idempotency key — it must equal the `Idempotency-Key` header."
   },
   "lineId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "nullable": true,
    "description": "Omit to discount the order rather than a line."
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "percentage": {
    "type": "number",
    "minimum": 0,
    "maximum": 100
   },
   "reason": {
    "type": "string",
    "minLength": 3,
    "maxLength": 300,
    "description": "Required, and free text rather than a code list. A cashier forced to pick the nearest reason picks the first one, and the register stops meaning anything.\n"
   },
   "reasonCode": {
    "type": "string",
    "nullable": true,
    "description": "Optional alongside the free text, where the venue maintains a list."
   },
   "approverPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Required above the venue threshold. May not be the requester."
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "MediaAsset": {
  "x-ticvai-persistence": "assets.media_asset",
  "type": "object",
  "required": [
   "id",
   "kind",
   "status",
   "filename",
   "contentType",
   "sizeBytes",
   "referenceCount",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "$ref": "#/components/schemas/MediaKind"
   },
   "status": {
    "$ref": "#/components/schemas/MediaStatus"
   },
   "filename": {
    "type": "string"
   },
   "contentType": {
    "type": "string"
   },
   "sizeBytes": {
    "type": "integer"
   },
   "title": {
    "$ref": "#/components/schemas/LocalisedText"
   },
   "description": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "description": "Set by `updateMediaAsset` and matched by `searchMedia`'s `search`. It was accepted and searched on before it had anywhere to be stored.\n"
   },
   "altText": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "description": "Required before use in a guest-facing surface. WCAG 2.2 AA."
   },
   "width": {
    "type": "integer",
    "nullable": true
   },
   "height": {
    "type": "integer",
    "nullable": true
   },
   "durationSeconds": {
    "type": "number",
    "nullable": true
   },
   "customMetadata": {
    "type": "object",
    "nullable": true,
    "additionalProperties": true,
    "description": "BL-178. **`assets` is a strong contract and its metadata was fixed** — kind, title, alt text, dimensions, rights. A venue photographing four thousand products wants its own fields: shoot date, photographer, model release, season.\n**Free-form and searchable, not a schema.** Every venue would want a different one, and a fixed set would be wrong for all of them.\n"
   },
   "sharedWithTenantIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "BL-178. **Cross-tenant sharing, and it is refused by default for a reason.** A brand operating three venues wants one logo library; two unrelated tenants sharing an asset store is the isolation breach ADR-0011 exists to prevent.\n**Only within one tenant's own scope tree.** A share naming a tenant outside it is refused rather than warned about — this is the one place where a permissive default would be a cross-tenant data leak.\n"
   },
   "tags": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "url": {
    "type": "string",
    "description": "Signed and expiring for private assets; stable CDN URL for public ones."
   },
   "thumbnailUrl": {
    "type": "string",
    "nullable": true
   },
   "referenceCount": {
    "type": "integer",
    "description": "How many surfaces reference this asset. Non-zero refuses deletion.\n"
   },
   "rights": {
    "$ref": "#/components/schemas/MediaRights"
   },
   "isRightsExpired": {
    "type": "boolean"
   },
   "version": {
    "type": "integer"
   },
   "uploadedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "MediaAssetDetail": {
  "x-ticvai-persistence": "assets.media_asset",
  "allOf": [
   {
    "$ref": "#/components/schemas/MediaAsset"
   },
   {
    "type": "object",
    "properties": {
     "derivatives": {
      "type": "array",
      "description": "Generated from the original, never uploaded separately. A new breakpoint is a re-render rather than a re-upload of everything.\n",
      "items": {
       "type": "object",
       "properties": {
        "label": {
         "type": "string"
        },
        "width": {
         "type": "integer"
        },
        "height": {
         "type": "integer"
        },
        "sizeBytes": {
         "type": "integer"
        },
        "url": {
         "type": "string"
        }
       }
      }
     },
     "usage": {
      "type": "array",
      "description": "Every place this asset is referenced.",
      "items": {
       "$ref": "#/components/schemas/MediaUsage"
      }
     },
     "collections": {
      "type": "array",
      "items": {
       "type": "object",
       "properties": {
        "id": {
         "type": "string",
         "format": "uuid"
        },
        "name": {
         "type": "string"
        }
       }
      }
     },
     "previousVersions": {
      "type": "array",
      "items": {
       "type": "object",
       "properties": {
        "version": {
         "type": "integer"
        },
        "replacedAt": {
         "type": "string",
         "format": "date-time"
        },
        "replacedByPrincipalId": {
         "type": "string",
         "format": "uuid"
        }
       }
      }
     }
    }
   }
  ]
 },
 "MediaEntitlements": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over entitlement and scan history",
  "required": [
   "mediaCode",
   "isValid",
   "entitlements"
  ],
  "properties": {
   "mediaCode": {
    "type": "string"
   },
   "mediaKind": {
    "type": "string",
    "enum": [
     "qr",
     "wristband",
     "card",
     "nfc",
     "mobilePass"
    ]
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "isValid": {
    "type": "boolean"
   },
   "invalidReason": {
    "type": "string",
    "nullable": true
   },
   "canAcceptMore": {
    "type": "boolean",
    "description": "False where the media has been surrendered, expired or blocked. A cashier should know before taking money, not after.\n"
   },
   "entitlements": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "entitlementId": {
       "type": "string",
       "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
      },
      "name": {
       "type": "string"
      },
      "kind": {
       "type": "string",
       "enum": [
        "admission",
        "locker",
        "fnb",
        "retail",
        "parking",
        "rental",
        "experience",
        "membership"
       ]
      },
      "orderId": {
       "type": "string",
       "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
      },
      "addedAt": {
       "type": "string",
       "format": "date-time"
      },
      "status": {
       "allOf": [
        {
         "$ref": "#/components/schemas/EntitlementStatus"
        }
       ],
       "description": "**Replaced `isRedeemed` on 17 August.** A boolean could not distinguish a ticket that was used from one that expired, was refunded, or was transferred — four different conversations at a gate, and the steward could see only \"not valid\".\n"
      },
      "entriesUsed": {
       "type": "integer"
      },
      "entriesAllowed": {
       "type": "integer",
       "nullable": true
      },
      "redeemedAt": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      },
      "transferredToSubjectId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "validTo": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      }
     }
    }
   }
  }
 },
 "MediaReplaceResult": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "asset",
   "affectedSurfaces"
  ],
  "properties": {
   "asset": {
    "$ref": "#/components/schemas/MediaAsset"
   },
   "affectedSurfaces": {
    "type": "integer",
    "description": "How many surfaces now show the new file."
   },
   "liveSurfaces": {
    "type": "integer",
    "description": "Of those, how many are published to guests right now."
   },
   "derivativesRegenerating": {
    "type": "boolean"
   }
  }
 },
 "MediaUsage": {
  "x-ticvai-persistence": "assets.media_usage",
  "type": "object",
  "description": "One place an asset is used. **`surface: product` is written by catalogue** for each item of `Product.media` (decided 29 September, rev 3 23SEP-4): `referenceId` is the product id and `isLive` is true while the product is listed to guests, which is what stops an asset in use on a ticket card being archived from under it.\n",
  "required": [
   "surface",
   "referenceId"
  ],
  "properties": {
   "extractedText": {
    "type": "string",
    "description": "**Text pulled out of an uploaded document**, after extraction. The generic retrieval path for anything a tenant uploads — a PDF nobody can search is a PDF nobody reads.\n"
   },
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "surface": {
    "type": "string",
    "enum": [
     "tenantBranding",
     "homepageBanner",
     "promoBlock",
     "contentPage",
     "product",
     "event",
     "menuItem",
     "merchandise",
     "workOrder",
     "incident",
     "inspection",
     "campaign"
    ]
   },
   "referenceId": {
    "type": "string"
   },
   "label": {
    "type": "string"
   },
   "isLive": {
    "type": "boolean",
    "description": "True where the referencing surface is published to guests."
   }
  }
 },
 "ModifyOrderRequest": {
  "type": "object",
  "required": [
   "id",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "Client-generated ULID **of this modification, not of the order** — the order is the path's `orderId`. It is the modification's idempotency key and must equal the `Idempotency-Key` header.\n"
   },
   "addLines": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/CreateOrderLine"
    }
   },
   "removeLineIds": {
    "type": "array",
    "items": {
     "type": "string",
     "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
    }
   },
   "reason": {
    "type": "string",
    "maxLength": 500
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "NaturalLanguageAnswer": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "conversationId",
   "question",
   "interpretation",
   "result",
   "confidence"
  ],
  "properties": {
   "conversationId": {
    "type": "string"
   },
   "question": {
    "type": "string"
   },
   "interpretation": {
    "type": "string",
    "description": "What the question was understood to mean, in plain language."
   },
   "generatedQuery": {
    "$ref": "#/components/schemas/GeneratedQuery",
    "description": "The structured query produced — data source, columns, filters, grouping. Returned so the answer can be checked. An answer nobody can verify is worse than no answer. **Also kept, as `NaturalLanguageQuery`**, for `saveNaturalLanguageQuery`.\n"
   },
   "result": {
    "$ref": "#/components/schemas/ReportResult"
   },
   "confidence": {
    "type": "number",
    "minimum": 0,
    "maximum": 1
   },
   "suggestedFollowUps": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "modelVersion": {
    "type": "string"
   },
   "tokensUsed": {
    "type": "integer"
   }
  }
 },
 "NoSaleEvent": {
  "type": "object",
  "x-ticvai-persistence": "orders.no_sale_event",
  "required": [
   "id",
   "shiftId",
   "reason",
   "principalId",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "shiftId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "workstationId": {
    "type": "string",
    "format": "uuid"
   },
   "reason": {
    "type": "string"
   },
   "note": {
    "type": "string",
    "nullable": true
   },
   "principalId": {
    "type": "string",
    "format": "uuid"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   },
   "countThisShift": {
    "type": "integer",
    "description": "Running count. Returned so the terminal can show it — a cashier who can see they are on their ninth no-sale behaves differently from one who cannot.\n"
   }
  }
 },
 "OpenShiftRequest": {
  "type": "object",
  "required": [
   "workstationId",
   "openingFloat"
  ],
  "properties": {
   "workstationId": {
    "type": "string",
    "format": "uuid"
   },
   "openingFloat": {
    "$ref": "#/components/schemas/DenominationCount"
   },
   "depositBoxCode": {
    "type": "string",
    "maxLength": 64,
    "description": "Physical container assigned to this shift. Required where the venue configures deposit box allocation.\n"
   },
   "bagNumber": {
    "type": "string",
    "maxLength": 64,
    "description": "Required where the venue configures bag numbers as mandatory."
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time",
    "description": "When the device recorded it. `openShift` is online-only (F32), so this differs from server receipt time only by transit; it is kept because the shift's other device writes are ordered against it.\n"
   }
  }
 },
 "Order": {
  "x-ticvai-persistence": "orders.sales_order + orders.order_line",
  "type": "object",
  "required": [
   "id",
   "venueId",
   "scopePath",
   "channel",
   "status",
   "currency",
   "currencyScale",
   "grossAmount",
   "taxAmount",
   "netAmount",
   "lines",
   "createdAt",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "The client ULID from `CreateOrderRequest.id`."
   },
   "orderNumber": {
    "type": "string",
    "readOnly": true,
    "description": "The number a guest reads and a cashier types. **Server-assigned: the venue prefix and a sequence per venue**, for example `DXB1-000123` (decided 28 September, audit R152). A till holds a reserved range of the venue sequence, so an order taken offline gets its number on the till and keeps it through `syncOrders`. **Not gapless**: an unused reserved range leaves a gap, and that is allowed. Only tax invoices are gapless, per legal entity. The receipt carries this number.\n"
   },
   "channel": {
    "allOf": [
     {
      "$ref": "#/components/schemas/OrderChannel"
     }
    ],
    "description": "Where it came from. Drives revenue attribution, promotion eligibility and the self-service adoption figures the operator will ask for within a month of launch.\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string"
   },
   "status": {
    "$ref": "#/components/schemas/OrderStatus"
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
   "grossAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "taxAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "netAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "refundedAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "droppedPromotions": {
    "type": "array",
    "readOnly": true,
    "x-ticvai-persisted": false,
    "description": "**Promotions left off this order at checkout because their budget cap would have been exceeded** (decided 28 September, audit R101 (8)). Empty when none was dropped. Returned by `checkoutCart` and `createOrder`, not stored.\n",
    "items": {
     "type": "object",
     "required": [
      "promotionId"
     ],
     "properties": {
      "promotionId": {
       "type": "string",
       "format": "uuid"
      },
      "name": {
       "type": "string"
      },
      "reason": {
       "type": "string",
       "enum": [
        "budgetCapReached"
       ]
      }
     }
    }
   },
   "totalPriceVariance": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Sum across lines. Zero on a normal order."
   },
   "lines": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/OrderLine"
    }
   },
   "payments": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/Payment"
    }
   },
   "principalId": {
    "type": "string",
    "format": "uuid"
   },
   "workstationId": {
    "type": "string",
    "format": "uuid"
   },
   "shiftId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "nullable": true
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "holdLabel": {
    "type": "string",
    "maxLength": 60,
    "nullable": true,
    "readOnly": true,
    "description": "The `label` a cashier gave when parking it with `holdOrder` — how they find it again. Null on an order never held."
   },
   "heldUntil": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "description": "When a held order expires and is voided (states/order.yaml), from `holdOrder`'s `holdUntil`. Null on an order not currently held."
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   },
   "syncedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "OrderChannel": {
  "type": "string",
  "description": "Where the order originated. Added when guest self-ordering was contracted — an order a guest placed on their own phone is commercially and operationally different from one a cashier typed, and reporting that cannot separate them cannot answer whether self-ordering is working.\n",
  "enum": [
   "pos",
   "kiosk",
   "guestApp",
   "guestWeb",
   "callCentre",
   "partner",
   "api",
   "backOffice"
  ]
 },
 "OrderExchangeResult": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "orderId",
   "outgoingValue",
   "incomingValue",
   "difference"
  ],
  "properties": {
   "orderId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "outgoingValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "incomingValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "exchangeFee": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "difference": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Only the difference settles. The replacement is held before the original is released, never the other way round.\n"
   },
   "newLineIds": {
    "type": "array",
    "items": {
     "type": "string",
     "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
    }
   },
   "revokedEntitlementIds": {
    "type": "array",
    "items": {
     "type": "string",
     "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
    }
   },
   "issuedEntitlementIds": {
    "type": "array",
    "items": {
     "type": "string",
     "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
    }
   }
  }
 },
 "OrderLine": {
  "x-ticvai-persistence": "orders.order_line + orders.order_line_eligibility",
  "allOf": [
   {
    "$ref": "#/components/schemas/CreateOrderLine"
   },
   {
    "type": "object",
    "required": [
     "serverUnitPrice",
     "taxAmount",
     "netAmount",
     "grossAmount"
    ],
    "properties": {
     "serverUnitPrice": {
      "allOf": [
       {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      ],
      "description": "What the server computed on ingest."
     },
     "priceVariance": {
      "allOf": [
       {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      ],
      "description": "Server minus quoted. Non-zero means the quoted price was honoured and the difference posted to the variance account.\n"
     },
     "taxAmount": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "netAmount": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "grossAmount": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "entitlementIds": {
      "type": "array",
      "description": "The entitlements this line issued. **These are the ticket ids** — `transferOrderTickets.ticketIds` and `reprintOrder.reissuedTicketIds` take and return them.",
      "items": {
       "type": "string",
       "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
      }
     },
     "crossRegionRightIds": {
      "type": "array",
      "items": {
       "type": "string"
      },
      "description": "Redemption rights propagated to other cells for this line."
     },
     "reprintCount": {
      "type": "integer",
      "minimum": 0,
      "default": 0,
      "readOnly": true,
      "description": "How many times this line's tickets were reprinted or resent. `reprintOrder` increments it; repeated reprints are the signal worth surfacing."
     }
    }
   }
  ]
 },
 "OrderModificationResult": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "order",
   "balanceDue"
  ],
  "properties": {
   "order": {
    "$ref": "#/components/schemas/Order"
   },
   "addedValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "removedValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "balanceDue": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Positive means the guest pays; negative means a refund is due."
   },
   "refundId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "nullable": true
   },
   "revokedEntitlementIds": {
    "type": "array",
    "items": {
     "type": "string",
     "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
    }
   },
   "issuedEntitlementIds": {
    "type": "array",
    "items": {
     "type": "string",
     "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
    }
   }
  }
 },
 "OrderResumeResult": {
  "type": "object",
  "x-ticvai-persistence": "none — computed",
  "required": [
   "order",
   "hasChanged"
  ],
  "properties": {
   "order": {
    "$ref": "#/components/schemas/Order"
   },
   "hasChanged": {
    "type": "boolean",
    "description": "True where anything moved while the sale was parked. The cashier decides — silently charging the old price loses money, silently charging the new one loses the guest.\n"
   },
   "changes": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "kind": {
       "type": "string",
       "enum": [
        "priceChanged",
        "promotionExpired",
        "promotionNowApplies",
        "soldOut",
        "seatHoldExpired",
        "productWithdrawn"
       ]
      },
      "lineId": {
       "type": "string",
       "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
      },
      "detail": {
       "type": "string"
      },
      "wasAmount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "nowAmount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      }
     }
    }
   }
  }
 },
 "OrderStatement": {
  "x-ticvai-persistence": "none — computed from order, payment, refund and ledger",
  "type": "object",
  "required": [
   "orderId",
   "orderNumber",
   "currency",
   "entries",
   "currentBalance"
  ],
  "properties": {
   "orderId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "orderNumber": {
    "type": "string"
   },
   "currency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "x-ticvai-persisted": false,
    "description": "**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"
   },
   "currencyScale": {
    "type": "integer",
    "x-ticvai-persisted": false,
    "description": "**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"
   },
   "entries": {
    "type": "array",
    "description": "Sequential. What an agent reads to a guest asking about a charge.",
    "items": {
     "type": "object",
     "required": [
      "kind",
      "amount",
      "runningBalance",
      "occurredAt"
     ],
     "properties": {
      "kind": {
       "type": "string",
       "enum": [
        "sale",
        "payment",
        "refund",
        "void",
        "modification",
        "exchange",
        "fee",
        "variance",
        "chargeback"
       ]
      },
      "description": {
       "type": "string"
      },
      "amount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "runningBalance": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "referenceId": {
       "type": "string",
       "nullable": true
      },
      "principalId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "occurredAt": {
       "type": "string",
       "format": "date-time"
      }
     }
    }
   },
   "totalPaid": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "totalRefunded": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "currentBalance": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Positive means the guest owes; negative means a refund is outstanding."
   }
  }
 },
 "OrderStatus": {
  "type": "string",
  "enum": [
   "pending",
   "held",
   "paid",
   "partiallyPaid",
   "completed",
   "voided",
   "refunded",
   "partiallyRefunded",
   "failed"
  ],
  "description": "`held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that accumulates parked sales across a shift cannot be closed.\n"
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
 "Payment": {
  "x-ticvai-persistence": "orders.payment",
  "type": "object",
  "required": [
   "id",
   "orderId",
   "tender",
   "amount",
   "status",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "orderId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "tender": {
    "$ref": "#/components/schemas/TenderKind"
   },
   "tenderCurrency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "description": "4.6.11. **What the guest actually handed over**, which is not always what the venue books. A tourist paying USD cash at a till is a foreign tender; the sale is still recorded in base currency.\nEqual to the base currency for almost every payment. **Present on all of them so the foreign-tender report has a source** — `getForeignTenderReport` promised *what was taken in which currency* and nothing recorded it until 18 August.\n"
   },
   "tenderAmount": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "The amount in `tenderCurrency`, at that currency's own scale."
   },
   "fxRate": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ExchangeRateDecimal"
     }
    ],
    "nullable": true,
    "description": "The rate applied, **stored on the payment rather than looked up later** (CF-37). A payment reconciled next month is reconciled at the rate of the day it was taken.\n"
   },
   "fxRateSource": {
    "type": "string",
    "nullable": true,
    "enum": [
     "manual",
     "feed",
     "cardScheme"
    ],
    "description": "4.2.8. Manual or fed on a schedule. **`cardScheme` is where the terminal did the conversion and told us** — dynamic currency conversion, the scheme's rate rather than ours.\n"
   },
   "changeCurrency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "nullable": true,
    "description": "4.6.11 is deliberately asymmetric: **accept foreign currency, refund in local.** A till giving change in five currencies needs five floats and five counts, and the variance becomes unattributable.\n"
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "changeAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "status": {
    "type": "string",
    "enum": [
     "authorised",
     "captured",
     "pendingConfirmation",
     "declined",
     "failed",
     "voided",
     "refunded"
    ]
   },
   "providerName": {
    "type": "string",
    "nullable": true
   },
   "providerReference": {
    "type": "string",
    "nullable": true
   },
   "lastInquiryAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   },
   "syncedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
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
 "ProductChangeImpact": {
  "type": "object",
  "description": "1.4.4 and 1.4.16. What a proposed change would touch. **Modelled on `PerformanceCancellationResult`**, which does this for a cancellation.\n",
  "required": [
   "entitlementsIssued",
   "ordersAffected",
   "propagates"
  ],
  "properties": {
   "entitlementsIssued": {
    "type": "integer",
    "description": "How many live entitlements came from this product."
   },
   "ordersAffected": {
    "type": "integer"
   },
   "futurePerformances": {
    "type": "integer"
   },
   "openCarts": {
    "type": "integer",
    "description": "**A guest with this product in a cart while its price changes underneath them** is the case nobody thinks about until it happens.\n"
   },
   "propagates": {
    "type": "boolean",
    "description": "Whether the change reaches what has already been sold. **A name correction should; a price change must not**, and the difference is the whole reason this operation exists.\n"
   },
   "blockedBy": {
    "type": "array",
    "description": "Reasons the change would be refused outright.",
    "items": {
     "type": "string"
    }
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
 "ProductVersion": {
  "type": "object",
  "x-ticvai-persistence": "catalogue.product_version",
  "description": "1.1.47, 1.4.9 to 1.4.11. **Follows `white-label.ConfigVersion`** — the same pattern for the same reason, and the fourth place this mechanism was asked for.\n",
  "required": [
   "version",
   "publishedAt",
   "publishedByPrincipalId"
  ],
  "properties": {
   "version": {
    "type": "integer"
   },
   "productId": {
    "type": "string",
    "format": "uuid"
   },
   "publishedAt": {
    "type": "string",
    "format": "date-time"
   },
   "publishedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "note": {
    "type": "string",
    "nullable": true
   },
   "isCurrent": {
    "type": "boolean"
   },
   "contentHash": {
    "type": "string",
    "description": "**Lets a diff be cheap and a no-op change be recognised.** Republishing an unchanged product should not create a version.\n"
   },
   "restoredFromVersion": {
    "type": "integer",
    "nullable": true,
    "description": "Set where this version was created by a restore. **A restore is a new version, not a rewind** — a price that was wrong for three days stays visible, because a finance query run next quarter has to reproduce what was charged.\n"
   }
  }
 },
 "RefundPolicy": {
  "x-ticvai-persistence": "orders.refund_policy + orders.refund_policy_time_band",
  "type": "object",
  "description": "Venue-configured. Thresholds are policy, not permission scope — venues run different policies and the permission model should not encode commercial rules.\n**The three thresholds must ascend** (decided 28 September, audit R123 (6)): `selfAuthoriseLimit` <= `requiresSecondUserAbove` <= `requiresApprovalAbove`, where the second is set. `setRefundPolicy` refuses a policy that does not with 422 `refund-thresholds-not-ascending`.\n",
  "required": [
   "venueId",
   "selfAuthoriseLimit",
   "requiresApprovalAbove"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "The venue in the path. Not taken from a `setRefundPolicy` body."
   },
   "selfAuthoriseLimit": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Up to this, a holder of ORDER_REFUND refunds alone. Zero means every refund needs a second authoriser.\n"
   },
   "requiresSecondUserAbove": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Above this, a second user — cashier OR supervisor — names themselves as audit control. Dual-authorisation, not escalation (2.12.3).\n"
   },
   "requiresApprovalAbove": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Above this, an ORDER_REFUND_APPROVE holder must approve."
   },
   "timeBands": {
    "type": "array",
    "description": "Refundable percentage by time before the performance. Evaluated most-specific first.\n",
    "items": {
     "type": "object",
     "required": [
      "hoursBefore",
      "percentage"
     ],
     "properties": {
      "hoursBefore": {
       "type": "integer",
       "minimum": 0
      },
      "percentage": {
       "type": "number",
       "minimum": 0,
       "maximum": 100
      }
     }
    }
   },
   "allowPartial": {
    "type": "boolean",
    "default": true
   },
   "refundWindowDays": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "description": "Days after purchase within which a refund may be made. 0 is allowed and means the day of purchase only; null means no window (decided 28 September, audit R123 (6))."
   },
   "varianceThreshold": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Price variance above this is an exception requiring review rather than a routine posting (CF-38). Venue-configured.\n**A venue setting with a tenant default** (decided 28 September, audit R094). **Proposed default, client to correct (audit R094): AED 5.00 per order line.**\n"
   }
  }
 },
 "ReportCategory": {
  "type": "string",
  "enum": [
   "sales",
   "admission",
   "financial",
   "inventory",
   "guest",
   "operations",
   "marketing",
   "workforce",
   "compliance",
   "custom"
  ]
 },
 "ReportColumn": {
  "x-ticvai-persistence": "reporting.report_column",
  "type": "object",
  "required": [
   "field"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "field": {
    "type": "string"
   },
   "label": {
    "type": "string"
   },
   "aggregation": {
    "allOf": [
     {
      "$ref": "#/components/schemas/Aggregation"
     }
    ],
    "default": "none"
   },
   "sortOrder": {
    "type": "integer"
   },
   "sortDirection": {
    "type": "string",
    "enum": [
     "asc",
     "desc"
    ]
   },
   "format": {
    "type": "string",
    "nullable": true
   }
  }
 },
 "ReportDefinition": {
  "x-ticvai-persistence": "reporting.report_definition + reporting.report_column + reporting.report_filter",
  "allOf": [
   {
    "$ref": "#/components/schemas/CreateReportRequest"
   },
   {
    "type": "object",
    "required": [
     "id",
     "version",
     "isSystem",
     "isRetired",
     "createdAt"
    ],
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid"
     },
     "version": {
      "type": "string",
      "description": "The current version. Assigned by the server on each publish; earlier ones are kept as `ReportDefinitionVersion`."
     },
     "isSystem": {
      "type": "boolean",
      "description": "Shipped with the platform — seeded at provisioning (BL-053, `SeededReport`). **Clone-only (decided 28 September, audit R096)**: `updateReport` and `deleteReport` refuse it with 409 `system-report`; a venue changes a copy made with `createReport`.\n"
     },
     "isRetired": {
      "type": "boolean"
     },
     "estimatedCost": {
      "type": "string",
      "enum": [
       "low",
       "medium",
       "high"
      ],
      "description": "Informs whether it may run inline or must be queued."
     },
     "createdByPrincipalId": {
      "type": "string",
      "format": "uuid",
      "nullable": true
     },
     "createdAt": {
      "type": "string",
      "format": "date-time"
     },
     "lastRunAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     },
     "scopePath": {
      "type": "string",
      "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"
     }
    }
   }
  ]
 },
 "ReportFilter": {
  "x-ticvai-persistence": "reporting.report_filter",
  "type": "object",
  "required": [
   "field",
   "operator"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "field": {
    "type": "string"
   },
   "operator": {
    "type": "string",
    "enum": [
     "equals",
     "notEquals",
     "greaterThan",
     "lessThan",
     "between",
     "in",
     "notIn",
     "contains",
     "isNull",
     "isNotNull"
    ]
   },
   "value": {
    "description": "**Open on purpose; its type is the field's.** One value, of the `FieldType` that `listReportFields` gives for `field` — a string, number, boolean, or a date, date-time or uuid as a string. Absent for `in`, `notIn`, `between`, `isNull` and `isNotNull`.\n"
   },
   "values": {
    "type": "array",
    "description": "The values for `in` and `notIn`, or exactly two (from, to) for `between`. Each of the field's `FieldType`, as `value`.",
    "items": {}
   },
   "isParameter": {
    "type": "boolean",
    "default": false,
    "description": "Prompted at run time rather than fixed. Parameters narrow the result; they never widen scope.\n"
   }
  }
 },
 "ReportParameter": {
  "x-ticvai-persistence": "reporting.report_parameter",
  "type": "object",
  "required": [
   "key",
   "label",
   "type",
   "isRequired"
  ],
  "properties": {
   "key": {
    "type": "string"
   },
   "label": {
    "type": "string"
   },
   "type": {
    "$ref": "#/components/schemas/FieldType"
   },
   "isRequired": {
    "type": "boolean"
   },
   "defaultValue": {
    "description": "Open on purpose. A value of this parameter's `type`, used when a run supplies none."
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
 "Settlement": {
  "x-ticvai-persistence": "ledger.settlement",
  "type": "object",
  "required": [
   "id",
   "providerName",
   "periodStart",
   "periodEnd",
   "status",
   "ingestedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "currencyCode": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "description": "**A settlement has no account, so nothing else denominates it.** A posting takes its currency from `ledger.account.currency` and a payment from `tenderCurrency`, but a settlement is a provider file for a period: `providerGross`, `ledgerGross` and `difference` are bare amounts, and a provider file in one currency against a ledger in another computes a difference that means nothing. Added 20 September, when a venue became able to trade outside its region's currency.\n"
   },
   "providerName": {
    "type": "string"
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "description": "The venue this settlement is for. **Reconciled daily per venue** (decided 28 September, audit R110 (b)), so `periodStart` and `periodEnd` are the same day."
   },
   "periodStart": {
    "type": "string",
    "format": "date",
    "description": "A day in the region's time zone, local midnight to local midnight."
   },
   "periodEnd": {
    "type": "string",
    "format": "date",
    "description": "A day in the region's time zone, local midnight to local midnight."
   },
   "fileReference": {
    "type": "string",
    "format": "uuid",
    "description": "The `MediaAsset` holding the provider file, as given to `ingestSettlementFile`. **Kept on the row because parsing is asynchronous**: the job that parses the file reads it from here.\n"
   },
   "format": {
    "type": "string",
    "nullable": true,
    "enum": [
     "csv",
     "fixedWidth",
     "xml",
     "json"
    ],
    "description": "The file format given at ingest. Null when none was given."
   },
   "status": {
    "$ref": "#/components/schemas/SettlementStatus"
   },
   "lineCount": {
    "type": "integer"
   },
   "matchedCount": {
    "type": "integer"
   },
   "exceptionCount": {
    "type": "integer"
   },
   "providerGross": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "providerFees": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "providerNet": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "ledgerGross": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "difference": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "ingestedAt": {
    "type": "string",
    "format": "date-time"
   },
   "completedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `region` scope.**"
   }
  }
 },
 "SettlementException": {
  "x-ticvai-persistence": "ledger.settlement_exception",
  "type": "object",
  "required": [
   "id",
   "settlementId",
   "kind",
   "providerReference",
   "amount"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "description": "Server-created when parsing finds the exception, so a UUID (naming-and-style 4)."
   },
   "settlementId": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "type": "string",
    "enum": [
     "unmatchedInProvider",
     "unmatchedInLedger",
     "amountMismatch",
     "duplicateInProvider",
     "feeUnexplained"
    ]
   },
   "providerReference": {
    "type": "string",
    "nullable": true
   },
   "paymentId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "nullable": true
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "expectedAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "resolution": {
    "allOf": [
     {
      "$ref": "#/components/schemas/SettlementResolution"
     }
    ],
    "nullable": true,
    "description": "Null while the exception is open."
   },
   "note": {
    "type": "string",
    "nullable": true,
    "description": "The `note` given to `resolveSettlementException`, stored with the resolution."
   },
   "resolvedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "resolvedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "SettlementResolution": {
  "type": "string",
  "description": "How a settlement exception was explained. One vocabulary for the request and the stored exception.",
  "enum": [
   "matchedManually",
   "writeOff",
   "disputeRaised",
   "providerError",
   "timingDifference"
  ]
 },
 "SettlementStatus": {
  "type": "string",
  "enum": [
   "ingesting",
   "parsing",
   "matching",
   "matched",
   "hasExceptions",
   "resolved",
   "failed"
  ]
 },
 "Shift": {
  "x-ticvai-persistence": "orders.pos_shift + orders.pos_shift_approval + orders.pos_shift_incident",
  "description": "**`approvals` and `incidents` are child rows** (26 September, pull audit R099): `orders.pos_shift_approval` and `orders.pos_shift_incident`, one row per item, keyed to the shift. Until then the contract carried both and `orders.pos_shift` had nowhere to put either.\n",
  "type": "object",
  "required": [
   "id",
   "workstationId",
   "venueId",
   "scopePath",
   "principalId",
   "status",
   "currency",
   "currencyScale",
   "openedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "description": "Client-generated ULID. Also the idempotency key."
   },
   "workstationId": {
    "type": "string",
    "format": "uuid"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string"
   },
   "principalId": {
    "type": "string",
    "format": "uuid",
    "description": "Who opened it. Cash reconciles to a person and a drawer."
   },
   "principalDisplayName": {
    "type": "string"
   },
   "incidents": {
    "type": "array",
    "description": "BL-097. **A till has exceptions and there was nowhere to write them** — a no-sale, a drawer opened without a transaction, a manager override, a guest dispute.\n**This is the log a cash-up investigation starts from**, and a shift that balances with four unexplained no-sales is not a shift that balanced.\n",
    "items": {
     "type": "object",
     "properties": {
      "kind": {
       "type": "string",
       "enum": [
        "noSale",
        "drawerOpen",
        "override",
        "voidAfterPayment",
        "guestDispute",
        "tillJam",
        "priceQuery",
        "other"
       ]
      },
      "at": {
       "type": "string",
       "format": "date-time"
      },
      "principalId": {
       "type": "string",
       "format": "uuid"
      },
      "note": {
       "type": "string",
       "nullable": true
      }
     }
    }
   },
   "status": {
    "$ref": "#/components/schemas/ShiftStatus"
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
   "depositBoxCode": {
    "type": "string",
    "nullable": true
   },
   "bagNumber": {
    "type": "string",
    "nullable": true
   },
   "openingFloat": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "salesTotal": {
    "x-ticvai-column": "gross_sales_amount",
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "What the till took in sales, as the guest paid it — tax included."
   },
   "refundsTotal": {
    "x-ticvai-column": "gross_refunded_amount",
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "What the till paid back, as the guest was refunded it — tax included."
   },
   "liftsTotal": {
    "x-ticvai-column": "lifted_amount",
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Cash taken out mid-shift by lifts and withdrawals. Cash, so neither gross nor net."
   },
   "expectedCash": {
    "x-ticvai-column": "expected_cash_amount",
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "readOnly": true,
    "nullable": true,
    "description": "26 September, pull audit R207. **The figure the blind count was measured against**, revealed once the count is in — null until then. Until this date only `ShiftCloseResult` carried it, returned once by `closeShift`, so BO-040 could not show the over/short it exists to accept.\n"
   },
   "countedCash": {
    "x-ticvai-column": "counted_cash_amount",
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "readOnly": true,
    "nullable": true,
    "description": "What the close count found. Null until the shift is counted."
   },
   "variance": {
    "x-ticvai-column": "variance_amount",
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "readOnly": true,
    "nullable": true,
    "description": "Counted minus expected, as `ShiftCloseResult.variance`. Negative is short."
   },
   "heldLeaseCount": {
    "type": "integer",
    "description": "Inventory leases currently held by this workstation. Surfaced so an operator closing a shift can see what will be returned.\n"
   },
   "openedAt": {
    "type": "string",
    "format": "date-time"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time",
    "description": "When the device recorded the open. `openedAt` is the server's time."
   },
   "suspendedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "suspendReason": {
    "type": "string",
    "maxLength": 200,
    "nullable": true,
    "description": "The `reason` given to `suspendShift`. Cleared on resume."
   },
   "closedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "closedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Who submitted the close count. `reopenShift` refuses an approver who is this principal, and until 26 September there was nothing to compare against (pull audit R099).\n"
   },
   "syncedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "Null while the shift has unsynced operations."
   },
   "approvals": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "kind",
      "principalId",
      "at"
     ],
     "properties": {
      "kind": {
       "type": "string",
       "enum": [
        "open",
        "close",
        "variance"
       ],
       "description": "`open` from `approveShiftOpen`, `close` from `approveShiftClose`, `variance` from `acceptShiftVariance`.\n"
      },
      "principalId": {
       "type": "string",
       "format": "uuid"
      },
      "at": {
       "type": "string",
       "format": "date-time"
      },
      "reason": {
       "type": "string"
      }
     }
    }
   }
  }
 },
 "ShiftCloseResult": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "shift",
   "expectedCash",
   "countedCash",
   "variance",
   "requiresAcceptance"
  ],
  "properties": {
   "shift": {
    "$ref": "#/components/schemas/Shift"
   },
   "expectedCash": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "countedCash": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "variance": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Counted minus expected. Negative is short."
   },
   "requiresAcceptance": {
    "type": "boolean",
    "description": "True when the variance exceeds the venue's `shiftVarianceThreshold` (audit R094). The shift is then `pendingVariance` and only `acceptShiftVariance` finalises it (audit R080 (e)).\n"
   },
   "nonCashVariances": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "tender",
      "declared",
      "captured",
      "variance"
     ],
     "properties": {
      "tender": {
       "type": "string"
      },
      "declared": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "captured": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "variance": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      }
     }
    }
   }
  }
 },
 "ShiftStatus": {
  "type": "string",
  "enum": [
   "pendingApproval",
   "open",
   "suspended",
   "pendingVariance",
   "pendingClosure",
   "closed",
   "autoClosed"
  ]
 },
 "TenderKind": {
  "type": "string",
  "description": "`wallet` is a **digital wallet** (Apple Pay, Google Pay and the like, taken through the gateway), the value the guest channels accept beside `card` (decided 28 September, audit R080 (a)). **The stored-value TICVAI wallet is a separate tender**: it is spent through `authoriseStoredValue` and `captureStoredValue` (`StoredValueKind` `wallet`), never as this value, so the client can see which of the two the decision meant.\n",
  "enum": [
   "cash",
   "card",
   "wallet",
   "voucher",
   "bankTransfer",
   "hotelCharge",
   "installment",
   "giftCard",
   "complimentary"
  ]
 },
 "TicketReissueFulfillmentRegenerationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Ticket Reissue & Fulfillment Regeneration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "maximumReissues": {
    "type": "string",
    "description": "Maximum Reissues"
   },
   "freeReissueCount": {
    "type": "integer",
    "description": "Free Reissue Count"
   },
   "supervisorThreshold": {
    "type": "integer",
    "description": "Supervisor Threshold"
   },
   "reissueReason": {
    "type": "string",
    "enum": [
     "dateChanged",
     "timeslotChanged",
     "seatChanged",
     "attendeeChanged",
     "lostTicket",
     "damagedCredential",
     "emailNotReceived",
     "walletPassIssue",
     "printingError",
     "credentialCompromised",
     "administrativeCorrection"
    ],
    "description": "Why the ticket is reissued."
   },
   "credentialMedia": {
    "type": "string",
    "enum": [
     "qr",
     "dynamicQr",
     "barcode",
     "rfid",
     "nfc",
     "printedTicket",
     "wearable"
    ],
    "description": "Credential media regenerated."
   },
   "deliveryMethod": {
    "type": "string",
    "enum": [
     "email",
     "smsWhatsappLink",
     "mobileApp",
     "walletPass",
     "walletUpdate",
     "posPrint",
     "boxOfficeCollection"
    ],
    "description": "How the reissue is delivered."
   },
   "reissueOption": {
    "type": "string",
    "enum": [
     "regenerateNew",
     "resendExisting"
    ],
    "description": "Regenerate a new credential (old one invalidated) or resend the existing one"
   }
  }
 },
 "UpdateGroupBookingRequest": {
  "type": "object",
  "description": "Request only. Every field optional; absent means unchanged.",
  "properties": {
   "packageProductId": {
    "type": "string",
    "nullable": true,
    "description": "The school-trip format or party package."
   },
   "yearGroup": {
    "type": "string",
    "maxLength": 40,
    "nullable": true
   },
   "accessAndDietaryNeeds": {
    "type": "string",
    "maxLength": 1000,
    "nullable": true
   },
   "celebrantName": {
    "type": "string",
    "maxLength": 120,
    "nullable": true,
    "description": "The birthday child."
   },
   "celebrantTurningAge": {
    "type": "integer",
    "minimum": 1,
    "maximum": 18,
    "nullable": true
   },
   "allergiesAndRequests": {
    "type": "string",
    "maxLength": 1000,
    "nullable": true
   },
   "finalHeadcountDueBy": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "leaderSubjectId": {
    "type": "string",
    "format": "uuid"
   },
   "organisationName": {
    "type": "string",
    "maxLength": 200,
    "nullable": true
   },
   "expectedSize": {
    "type": "integer",
    "minimum": 2
   },
   "confirmedSize": {
    "type": "integer",
    "minimum": 0
   },
   "minimumSize": {
    "type": "integer",
    "minimum": 1,
    "nullable": true
   },
   "attendeeCaptureRequired": {
    "type": "boolean"
   },
   "attendeeCaptureDueBy": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "confirmed",
     "namesPending",
     "complete",
     "cancelled"
    ]
   }
  }
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
 "WithdrawalReason": {
  "type": "string",
  "description": "Why a supervisor took cash out of a box. Set only on lifts `withdrawFromDepositBox` records.",
  "enum": [
   "banking",
   "safeDrop",
   "changeOrder",
   "other"
  ]
 }
}
```
