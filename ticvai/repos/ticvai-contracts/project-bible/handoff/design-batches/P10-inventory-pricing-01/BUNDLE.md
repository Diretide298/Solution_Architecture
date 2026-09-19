# P10-inventory-pricing-01 — P10 · Inventory & Pricing

**3 screens · 37 operations · 30 schemas · 13 permissions**

Platform P10 Partner Web · ships as **ticvai-control** ·
partner audience · web ·
online only

## Who this is for

**partner on web.** Everything below is how you know what is
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

- **Every control that can be refused must be gated.** 13 permissions apply here:
  `CAPACITY_CONFIGURE, ORDER_CREATE, ORDER_DISCOUNT, ORDER_EXCHANGE, ORDER_MODIFY, ORDER_REPRINT, ORDER_RESCHEDULE, ORDER_VIEW, ORDER_VOID, PRICE_CONFIGURE, PRICE_VIEW, PRODUCT_CONFIGURE`…. A control nobody can use must say so,
  not sit enabled and fail.
- **11 of these operations work offline**: applyManualDiscount, createOrder, getOrder, getProduct, holdOrder, listOrderRefunds, listOrders, listProductVariants
  — and the rest do not. A surface that looks the same online and off is lying.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `PTR-005` | Inventory & Allocation View | listDetail | 19 | 1 | — |
| `PTR-006` | Product Catalog (B2B Pricing) | listDetail | 17 | 0 | — |
| `PTR-007` | Availability Search | statusTracker | 1 | 0 | — |

## Thin screens in this batch

**PTR-007 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "PTR-005",
  "name": "Inventory & Allocation View",
  "module": "Inventory & Pricing",
  "requiresModule": "partner",
  "wave": 2,
  "capability": "C103",
  "implementation": {
   "app": "partner-web",
   "route": "/general/inventory-and-allocation-view",
   "component": "apps/partner-web/src/routes/general/InventoryAndAllocationViewDetail.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "PTR-001"
   ],
   "inferred": true,
   "exitTo": [
    "PTR-001",
    "PTR-002",
    "PTR-003",
    "PTR-008"
   ],
   "fromFlows": true,
   "transitions": [
    {
     "to": "PTR-008",
     "trigger": "Receives vouchers",
     "provenance": "flow F10 step 2→3",
     "operation": "createOrder"
    },
    {
     "to": "PTR-001",
     "trigger": "Partner Login / MFA",
     "carries": [
      "accountId",
      "sessionId"
     ],
     "provenance": "derived — PTR-001 declares entryState.params accountId, sessionId, so an edge into it must carry them"
    },
    {
     "to": "PTR-002",
     "trigger": "Partner Dashboard",
     "carries": [
      "accountId",
      "orderId"
     ],
     "provenance": "derived — PTR-002 declares entryState.params accountId, orderId, so an edge into it must carry them"
    },
    {
     "to": "PTR-003",
     "trigger": "Profile & Company Details",
     "carries": [
      "principalId"
     ],
     "provenance": "derived — PTR-003 declares entryState.params principalId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **createRefund removed 18 August** — attached by module resemblance, not by what this screen does. A screen that does not handle money should not be able to move it (CF-87's class).",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listChannelCapacities` reads the population and `getChannelAllocations` reads one of them — list, select, act",
  "purpose": "See inventory & allocation view for this venue.",
  "gaps": [
   {
    "operation": "getOrder",
    "why": "**4 declared operations reach no component on this screen**: getOrder, getOrderStatement, listOrderRefunds, listOrders. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every inventory allocation",
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
       "label": "The selected inventory allocation",
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
       "operation": "createOrder",
       "provenance": "contract orders.yaml POST /orders"
      },
      {
       "kind": "secondaryButton",
       "label": "Apply",
       "operation": "applyManualDiscount",
       "provenance": "contract orders.yaml POST /orders/{orderId}/discounts"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createChannelCapacity",
       "provenance": "contract catalogue.yaml POST /channel-capacities"
      },
      {
       "kind": "secondaryButton",
       "label": "Exchange",
       "operation": "exchangeOrderLines",
       "provenance": "contract orders.yaml POST /orders/{orderId}/exchanges"
      },
      {
       "kind": "secondaryButton",
       "label": "Hold",
       "operation": "holdOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/hold"
      },
      {
       "kind": "secondaryButton",
       "label": "Modify",
       "operation": "modifyOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/modify"
      },
      {
       "kind": "secondaryButton",
       "label": "Release hold",
       "operation": "relinquishChannelAllocation",
       "provenance": "contract catalogue.yaml POST /channel-capacities/{channelCapacityId}/channel-allocations/release"
      },
      {
       "kind": "secondaryButton",
       "label": "Reprint",
       "operation": "reprintOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/reprints"
      },
      {
       "kind": "secondaryButton",
       "label": "Reschedule",
       "operation": "rescheduleOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/reschedule"
      },
      {
       "kind": "secondaryButton",
       "label": "Resume",
       "operation": "resumeOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/resume"
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
      },
      {
       "kind": "destructiveButton",
       "label": "Void",
       "operation": "voidOrder",
       "provenance": "contract orders.yaml POST /orders/{orderId}/voids"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createOrder",
       "label": "Create order",
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
       "kind": "destructiveButton",
       "derived": true,
       "impliedBy": "voidOrder",
       "label": "Void order",
       "notes": "**Always confirms, never the default focus.** The consequence goes in the body — *cancel 3 orders worth AED 480* is a confirmation, *are you sure* is not.",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createOrder",
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
    "id": "confirmVoidOrder",
    "component": "confirmDialog",
    "trigger": "Void",
    "body": "**Names what `voidOrder` changes and what it leaves alone**, in the consequence rather than the verb. A inventory allocation this affects should be identified in the dialog, not just counted.",
    "provenance": "contract orders.yaml POST /orders/{orderId}/voids"
   }
  ],
  "states": {
   "loading": "The inventory allocation list.",
   "error": "Could not load. Names which read failed and leaves the inventory allocation untouched.",
   "emptyFirstRun": "No inventory allocation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the inventory allocation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getChannelAllocations",
    "contract": "catalogue",
    "purpose": "from page inventory",
    "trigger": "onLoad"
   },
   {
    "operationId": "createOrder",
    "contract": "orders",
    "purpose": "From the flow it appears in",
    "trigger": "onLoad"
   },
   {
    "operationId": "applyManualDiscount",
    "contract": "orders",
    "purpose": "Apply a discount a cashier chose",
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
    "operationId": "exchangeOrderLines",
    "contract": "orders",
    "purpose": "Exchange lines for different products or dates",
    "trigger": "onAction",
    "invalidates": [
     "listChannelCapacities"
    ]
   },
   {
    "operationId": "getOrder",
    "contract": "orders",
    "purpose": "Read an order",
    "trigger": "onLoad"
   },
   {
    "operationId": "getOrderStatement",
    "contract": "orders",
    "purpose": "Full financial history of an order",
    "trigger": "onLoad"
   },
   {
    "operationId": "holdOrder",
    "contract": "orders",
    "purpose": "Park a sale and free the till",
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
    "operationId": "listOrderRefunds",
    "contract": "orders",
    "purpose": "List refunds against an order",
    "trigger": "onLoad"
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
    "operationId": "reprintOrder",
    "contract": "orders",
    "purpose": "Reprint or resend tickets",
    "trigger": "onAction",
    "invalidates": [
     "listChannelCapacities"
    ]
   },
   {
    "operationId": "rescheduleOrder",
    "contract": "orders",
    "purpose": "Move an order to another performance",
    "trigger": "onAction",
    "invalidates": [
     "listChannelCapacities"
    ]
   },
   {
    "operationId": "resumeOrder",
    "contract": "orders",
    "purpose": "Bring a parked sale back to a till",
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
    "operationId": "voidOrder",
    "contract": "orders",
    "purpose": "Void an order",
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
    },
    {
     "name": "orderId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A guest opening an order link weeks later.** Shows the order if it still resolves; if it was refunded or the performance passed, says which and offers the order list rather than an error.",
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
   "board": "wireframes/P10 Partner Web.dc.html#ptr-005"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 19 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P10",
   "audience": "partner",
   "formFactor": "web",
   "shortName": "Partner Web",
   "name": "Partner Web — Reseller Portal",
   "offlineCapable": false,
   "app": "partner-web",
   "operator": "partner",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
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
  "id": "PTR-006",
  "name": "Product Catalog (B2B Pricing)",
  "module": "Inventory & Pricing",
  "requiresModule": "partner",
  "wave": 2,
  "capability": "C85",
  "implementation": {
   "app": "partner-web",
   "route": "/general/product-catalog-b2b-pricing",
   "component": "apps/partner-web/src/routes/general/ProductCatalogB2bPricingList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "PTR-001"
   ],
   "inferred": true,
   "exitTo": [
    "PTR-001",
    "PTR-002",
    "PTR-003"
   ],
   "transitions": [
    {
     "to": "PTR-001",
     "trigger": "Partner Login / MFA",
     "carries": [
      "accountId",
      "sessionId"
     ],
     "provenance": "derived — PTR-001 declares entryState.params accountId, sessionId, so an edge into it must carry them"
    },
    {
     "to": "PTR-002",
     "trigger": "Partner Dashboard",
     "carries": [
      "accountId",
      "orderId"
     ],
     "provenance": "derived — PTR-002 declares entryState.params accountId, orderId, so an edge into it must carry them"
    },
    {
     "to": "PTR-003",
     "trigger": "Profile & Company Details",
     "carries": [
      "principalId"
     ],
     "provenance": "derived — PTR-003 declares entryState.params principalId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. Purpose derived from the screen name and its operations on 17 August, not from a requirement.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listProducts` reads the population and `getPriceList` reads one of them — list, select, act",
  "purpose": "Find product catalog (b2b pricing) for this venue.",
  "gaps": [
   {
    "operation": "getProduct",
    "why": "**5 declared operations reach no component on this screen**: getProduct, listAlternativeCodes, listPriceLists, listPrices, listProductVariants. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every product catalog (b2b",
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
       "label": "The selected product catalog (b2b",
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
       "label": "Copy",
       "operation": "copyPriceList",
       "provenance": "contract catalogue.yaml POST /price-lists/{priceListId}/copy"
      },
      {
       "kind": "secondaryButton",
       "label": "Create",
       "operation": "createPriceList",
       "provenance": "contract catalogue.yaml POST /price-lists"
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
       "operation": "setPrices",
       "provenance": "contract catalogue.yaml PUT /price-lists/{priceListId}/prices"
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
       "operation": "updatePriceList",
       "provenance": "contract catalogue.yaml PATCH /price-lists/{priceListId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateProduct",
       "provenance": "contract catalogue.yaml PATCH /products/{productId}"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The product catalog (b2b list.",
   "error": "Could not load. Names which read failed and leaves the product catalog (b2b untouched.",
   "emptyFirstRun": "No product catalog (b2b yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the product catalog (b2b are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listProducts",
    "contract": "catalogue",
    "purpose": "from page inventory",
    "trigger": "onLoad"
   },
   {
    "operationId": "getPriceList",
    "contract": "catalogue",
    "purpose": "from page inventory",
    "trigger": "onLoad"
   },
   {
    "operationId": "copyPriceList",
    "contract": "catalogue",
    "purpose": "Copy a price list, optionally with an adjustment",
    "trigger": "onAction",
    "invalidates": [
     "listProducts"
    ]
   },
   {
    "operationId": "createPriceList",
    "contract": "catalogue",
    "purpose": "Create a price list",
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
    "operationId": "setPrices",
    "contract": "catalogue",
    "purpose": "Set prices in bulk",
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
    "operationId": "updatePriceList",
    "contract": "catalogue",
    "purpose": "Amend a price list",
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
     "name": "priceListId",
     "from": "deepLink"
    },
    {
     "name": "productId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A shared product link after the product retired.** Shows what replaced it where a successor exists, and the catalogue where none does.",
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
   "board": "wireframes/P10 Partner Web.dc.html#ptr-006"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 17 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P10",
   "audience": "partner",
   "formFactor": "web",
   "shortName": "Partner Web",
   "name": "Partner Web — Reseller Portal",
   "offlineCapable": false,
   "app": "partner-web",
   "operator": "partner",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
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
  "id": "PTR-007",
  "name": "Availability Search",
  "module": "Inventory & Pricing",
  "requiresModule": "partner",
  "wave": 2,
  "capability": "C81",
  "implementation": {
   "app": "partner-web",
   "route": "/general/availability-search",
   "component": "apps/partner-web/src/routes/general/AvailabilitySearchList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "PTR-001",
    "PTR-002"
   ],
   "inferred": true,
   "exitTo": [
    "PTR-001",
    "PTR-002",
    "PTR-003",
    "PTR-008"
   ],
   "flowDerived": true,
   "transitions": [
    {
     "to": "PTR-008",
     "trigger": "Creates the booking",
     "provenance": "flow F03 step 2→3",
     "operation": "getAvailability"
    },
    {
     "to": "PTR-001",
     "trigger": "Partner Login / MFA",
     "carries": [
      "accountId",
      "sessionId"
     ],
     "provenance": "derived — PTR-001 declares entryState.params accountId, sessionId, so an edge into it must carry them"
    },
    {
     "to": "PTR-002",
     "trigger": "Partner Dashboard",
     "carries": [
      "accountId",
      "orderId"
     ],
     "provenance": "derived — PTR-002 declares entryState.params accountId, orderId, so an edge into it must carry them"
    },
    {
     "to": "PTR-003",
     "trigger": "Profile & Company Details",
     "carries": [
      "principalId"
     ],
     "provenance": "derived — PTR-003 declares entryState.params principalId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. Purpose derived from the screen name and its operations on 17 August, not from a requirement.",
  "density": "compact",
  "pattern": "statusTracker",
  "patternReason": "`getAvailability` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "Find something when the guest does not know what it is called.",
  "gaps": [
   {
    "operation": "getAvailability",
    "why": "**1 declared operation reach no component on this screen**: getAvailability. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
   }
  ],
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "components": []
    }
   ]
  },
  "states": {
   "loading": "The availability search list.",
   "error": "Could not load. Names which read failed and leaves the availability search untouched.",
   "emptyFirstRun": "No availability search yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the availability search are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getAvailability",
    "contract": "catalogue",
    "purpose": "Per-performance capacity on the B2B channel",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-007"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 1 operation this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P10",
   "audience": "partner",
   "formFactor": "web",
   "shortName": "Partner Web",
   "name": "Partner Web — Reseller Portal",
   "offlineCapable": false,
   "app": "partner-web",
   "operator": "partner",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
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
 "getAvailability": {
  "method": "GET",
  "path": "/availability",
  "contract": "catalogue",
  "summary": "Live remaining capacity",
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
    "name": "channelCapacityId",
    "in": "query",
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
  "responds": "Refund"
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "variantId": {
    "type": "string",
    "format": "uuid"
   },
   "performanceId": {
    "type": "string",
    "format": "uuid"
   },
   "inventoryHoldId": {
    "type": "string",
    "nullable": true,
    "description": "Lease the units were drawn from. Absent for uncontended products."
   },
   "seatIds": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Seated products only. Not available offline."
   },
   "quantity": {
    "type": "integer",
    "minimum": 1
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
    "additionalProperties": true
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
    "description": "Client-generated ULID. Also the idempotency key."
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "channel": {
    "$ref": "#/components/schemas/Channel"
   },
   "shiftId": {
    "type": "string"
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "outgoingLineIds": {
    "type": "array",
    "minItems": 1,
    "items": {
     "type": "string"
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
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "lineId": {
    "type": "string",
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
 "ModifyOrderRequest": {
  "type": "object",
  "required": [
   "id",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
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
     "type": "string"
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
    "type": "string"
   },
   "orderNumber": {
    "type": "string"
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
    "nullable": true
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
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
    "type": "string"
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
     "type": "string"
    }
   },
   "revokedEntitlementIds": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "issuedEntitlementIds": {
    "type": "array",
    "items": {
     "type": "string"
    }
   }
  }
 },
 "OrderLine": {
  "x-ticvai-persistence": "orders.order_line",
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
      "items": {
       "type": "string"
      }
     },
     "crossRegionRightIds": {
      "type": "array",
      "items": {
       "type": "string"
      },
      "description": "Redemption rights propagated to other cells for this line."
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
    "nullable": true
   },
   "revokedEntitlementIds": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "issuedEntitlementIds": {
    "type": "array",
    "items": {
     "type": "string"
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
       "type": "string"
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
    "type": "string"
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
    "type": "string"
   },
   "orderId": {
    "type": "string"
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
    "type": "number",
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
 "Refund": {
  "x-ticvai-persistence": "orders.refund",
  "type": "object",
  "required": [
   "id",
   "orderId",
   "amount",
   "status",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string"
   },
   "orderId": {
    "type": "string"
   },
   "fxRate": {
    "type": "number",
    "nullable": true,
    "readOnly": true,
    "description": "**The rate on the original payment, not today's** (BL-087, CF-118).\n`Payment` records `tenderCurrency`, `fxRate` and `fxRateSource` at the moment of sale, so the sale rate is always retrievable. **Refunding at today's rate repays a different amount of money than was taken** — a guest who paid 100 USD at 3.67 and is refunded at 3.72 gets back more AED than they gave, and the venue carries the difference on every refund.\nThe exposure runs both ways and neither direction is defensible: a guest short-changed by a moving rate has a complaint the venue cannot answer, because **the guest did nothing but wait.**\n"
   },
   "taxReversalEntryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "**A refund reverses the tax entry it created, and this is where that is stated rather than implied.** `reverseJournalEntry` and `calculateTax` both exist, so both halves were present and the obligation was assumed — **an implied obligation is one a developer can miss without failing anything.**\nNull only where the original sale carried no tax.\n"
   },
   "settleTo": {
    "type": "string",
    "enum": [
     "originalTender",
     "advanceBalance",
     "wireTransfer",
     "storeCredit"
    ],
    "default": "originalTender",
    "description": "BL-086. **A refund could only go back the way it came.** A guest whose card has expired, a partner settling by wire, a guest who would rather have the credit — three real cases with one answer.\n**`originalTender` stays the default** because refunding elsewhere is how money laundering works, and anything else needs a reason.\n"
   },
   "fxVariance": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Where the sale rate and the current rate differ, **the difference is booked as an FX variance rather than hidden in the refund**. `runFxRevaluation` already handles this class of movement and this is the same act at a smaller scale.\n"
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "appliedPercentage": {
    "type": "number",
    "description": "From the venue's time bands, or an approver override."
   },
   "status": {
    "type": "string",
    "enum": [
     "pendingApproval",
     "pendingGateway",
     "completed",
     "declined",
     "failed"
    ]
   },
   "reason": {
    "type": "string"
   },
   "requestedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "secondaryPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "approvedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "ledgerEntryId": {
    "type": "string",
    "nullable": true,
    "description": "Written before the gateway is called."
   },
   "gatewayReference": {
    "type": "string",
    "nullable": true
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "completedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
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
