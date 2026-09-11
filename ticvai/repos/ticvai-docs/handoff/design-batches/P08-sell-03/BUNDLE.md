# P08-sell-03 — P08 · Sell (3 of 4)

**10 screens · 23 operations · 26 schemas · 10 permissions**

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
  `AI_USE, MARKETING_MANAGE, MARKETING_VIEW, PRODUCT_CONFIGURE, PRODUCT_VIEW, REPORT_VIEW_VENUE, ROLE_MANAGE, SCOPE_VIEW, TENANT_CONFIGURE, WORKSTATION_CONFIGURE`. A control nobody can use must say so,
  not sit enabled and fail.
- **5 of these operations work offline**: getUpsellSuggestions, listMerchandise, listProductCategories, listSaleBoards, listSerialisedItems
  — and the rest do not. A surface that looks the same online and off is lying.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-114` | Variants, Attributes, Barcode & RFID Management | listDetail | 2 | 0 | — |
| `BO-115` | Category, Brand & Merchandise Hierarchy | listDetail | 5 | 0 | — |
| `BO-116` | Merchandising & Product Presentation | commandCentre | 7 | 0 | — |
| `BO-117` | Product Import, Governance & AI Configuration Assistant | listDetail | 5 | 0 | — |
| `BO-118` | Campaign & Audience Management | commandCentre | 6 | 0 | — |
| `BO-119` | Cross-Sell, Upsell & Recommendation Rules | statusTracker | 2 | 0 | — |
| `BO-120` | Omnichannel Commerce & Journey Configuration | listDetail | 2 | 0 | — |
| `BO-121` | Personalized Offers & Guest Engagement | listDetail | 2 | 0 | — |
| `BO-122` | POS Experience Dashboard | listDetail | 1 | 0 | — |
| `BO-123` | POS Profile Management | listDetail | 2 | 0 | — |

## Thin screens in this batch

**BO-119, BO-122 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-114",
  "name": "Variants, Attributes, Barcode & RFID Management",
  "module": "Sell",
  "requiresModule": "inventory",
  "wave": 2,
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/variants-attributes-barcode-rfid-management",
   "component": "apps/venue-management-web/src/routes/sell/VariantsAttributesBarcodeRfidManagemenList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-102"
   ],
   "exitTo": [
    "BO-102"
   ],
   "inferred": false,
   "notes": "**Returns to BO-102.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "BO-102",
     "trigger": "Sell",
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-102 declares entryState.params venueId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "**Added 20 August from the client design board.** The operations existed and no screen called them. **Named in the board contents and not written up in it** — the operations are real, the layout is not.",
  "density": "compact",
  "boardFrames": [
   "Retail Board 4.dc.html#ret-4j"
  ],
  "pattern": "listDetail",
  "patternReason": "`listSerialisedItems` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Variants, Attributes, Barcode & RFID Management — from the client design board, 20 August.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every variants attributes barcode",
       "bindsTo": "SerialisedItem",
       "columns": [
        "SerialisedItem.id",
        "SerialisedItem.itemId",
        "SerialisedItem.batchId",
        "SerialisedItem.serial",
        "SerialisedItem.locationId",
        "SerialisedItem.status",
        "SerialisedItem.soldOnOrderLineId",
        "SerialisedItem.warrantyUntil",
        "SerialisedItem.receivedAt"
       ],
       "operation": "listSerialisedItems",
       "provenance": "contract inventory.yaml GET /serialised-items"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected variants attributes barcode",
       "bindsTo": "SerialisedItem",
       "columns": [
        "SerialisedItem.id",
        "SerialisedItem.itemId",
        "SerialisedItem.batchId",
        "SerialisedItem.serial",
        "SerialisedItem.locationId",
        "SerialisedItem.status",
        "SerialisedItem.soldOnOrderLineId",
        "SerialisedItem.warrantyUntil",
        "SerialisedItem.receivedAt"
       ],
       "operation": "listSerialisedItems",
       "provenance": "contract inventory.yaml GET /serialised-items"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Lookup",
       "operation": "lookupMerchandise",
       "provenance": "contract retail.yaml GET /merchandise/lookup"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "searchField",
       "label": "Search variants, attributes, barcode",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The variants attributes barcode list.",
   "error": "Could not load. Names which read failed and leaves the variants attributes barcode untouched.",
   "emptyFirstRun": "No variants attributes barcode yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the variants attributes barcode are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listSerialisedItems",
    "contract": "inventory",
    "purpose": "listSerialisedItems",
    "trigger": "onLoad"
   },
   {
    "operationId": "lookupMerchandise",
    "contract": "retail",
    "purpose": "Price and stock check by barcode",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    }
   ],
   "coldEntry": "Resolves from the session. A principal with more than one venue is asked which before the page renders.",
   "preloaded": [
    "SerialisedItem.id",
    "SerialisedItem.itemId",
    "SerialisedItem.batchId",
    "SerialisedItem.serial",
    "SerialisedItem.locationId"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-114",
   "source": "Claude Design Retail pack, 24 August",
   "note": "**Drawn by Claude Design on `Retail Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "BO-115",
  "name": "Category, Brand & Merchandise Hierarchy",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 2,
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/category-brand-merchandise-hierarchy",
   "component": "apps/venue-management-web/src/routes/sell/CategoryBrandMerchandiseHierarchyList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-102"
   ],
   "exitTo": [
    "BO-102",
    "BO-116"
   ],
   "inferred": false,
   "notes": "**Returns to BO-102.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "BO-116",
     "trigger": "Merchandising & Product Presentation",
     "provenance": "flow F86 step 1→2"
    },
    {
     "to": "BO-102",
     "trigger": "Sell",
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-102 declares entryState.params venueId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "**Added 20 August from the client design board.** The operations existed and no screen called them. **Named in the board contents and not written up in it** — the operations are real, the layout is not. **Owns POS board frame(s) POS-4A** (client pack, 24 August). **Assigned by board purpose rather than by operation overlap** — three attempts at deriving that mapping produced plausible nonsense, and a reader who trusts a bad table is worse off than one who has none.",
  "density": "compact",
  "boardFrames": [
   "POS Board 4.dc.html#pos-4a"
  ],
  "pattern": "listDetail",
  "patternReason": "`listProductCategories` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Category, Brand & Merchandise Hierarchy — from the client design board, 20 August.",
  "gaps": [
   {
    "operation": "listSaleBoards",
    "why": "**1 declared operation reach no component on this screen**: listSaleBoards. Either the screen is missing what calls them, or the declaration is residue.",
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
       "label": "Every category brand merchandise",
       "bindsTo": "ProductCategory",
       "columns": [
        "ProductCategory.id",
        "ProductCategory.name",
        "ProductCategory.nameLocalised",
        "ProductCategory.kind",
        "ProductCategory.parentId",
        "ProductCategory.scopePath",
        "ProductCategory.displayOrder",
        "ProductCategory.imageAssetId",
        "ProductCategory.isActive"
       ],
       "operation": "listProductCategories",
       "provenance": "contract catalogue.yaml GET /product-categories"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected category brand merchandise",
       "bindsTo": "ProductCategory",
       "columns": [
        "ProductCategory.id",
        "ProductCategory.name",
        "ProductCategory.nameLocalised",
        "ProductCategory.kind",
        "ProductCategory.parentId",
        "ProductCategory.scopePath",
        "ProductCategory.displayOrder",
        "ProductCategory.imageAssetId",
        "ProductCategory.isActive"
       ],
       "operation": "listProductCategories",
       "provenance": "contract catalogue.yaml GET /product-categories"
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
       "operation": "setProductCategories",
       "provenance": "contract catalogue.yaml PUT /product-categories"
      },
      {
       "kind": "secondaryButton",
       "label": "Request",
       "operation": "requestSuggestion",
       "provenance": "contract ai.yaml POST /ai/suggestions"
      },
      {
       "kind": "secondaryButton",
       "label": "Run",
       "operation": "runReport",
       "provenance": "contract reporting.yaml POST /reports/{reportId}/run"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "searchField",
       "label": "Search category, brand",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The category brand merchandise list.",
   "error": "Could not load. Names which read failed and leaves the category brand merchandise untouched.",
   "emptyFirstRun": "No category brand merchandise yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the category brand merchandise are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listProductCategories",
    "contract": "catalogue",
    "purpose": "listProductCategories",
    "trigger": "onLoad"
   },
   {
    "operationId": "setProductCategories",
    "contract": "catalogue",
    "purpose": "setProductCategories",
    "trigger": "onAction",
    "invalidates": [
     "listProductCategories"
    ]
   },
   {
    "operationId": "listSaleBoards",
    "contract": "tenancy",
    "purpose": "List sale boards",
    "trigger": "onLoad"
   },
   {
    "operationId": "requestSuggestion",
    "contract": "ai",
    "purpose": "requestSuggestion",
    "trigger": "onAction",
    "invalidates": [
     "listProductCategories"
    ]
   },
   {
    "operationId": "runReport",
    "contract": "reporting",
    "purpose": "Run a report",
    "trigger": "onAction",
    "invalidates": [
     "listProductCategories"
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
     "name": "reportId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "Resolves from the session. A principal with more than one venue is asked which before the page renders.",
   "preloaded": [
    "ProductCategory.id",
    "ProductCategory.name",
    "ProductCategory.nameLocalised",
    "ProductCategory.kind",
    "ProductCategory.parentId"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-115",
   "source": "Claude Design POS pack, 24 August",
   "note": "**Drawn by Claude Design on `POS Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
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
  "id": "BO-116",
  "name": "Merchandising & Product Presentation",
  "module": "Sell",
  "requiresModule": "retail",
  "wave": 2,
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/merchandising-product-presentation",
   "component": "apps/venue-management-web/src/routes/sell/MerchandisingProductPresentationList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-102",
    "BO-115"
   ],
   "exitTo": [
    "BO-102",
    "BO-117"
   ],
   "inferred": false,
   "notes": "**Returns to BO-102.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "BO-117",
     "trigger": "Product Import, Governance & AI Configuration Assistant",
     "provenance": "flow F86 step 2→3"
    },
    {
     "to": "BO-102",
     "trigger": "Sell",
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-102 declares entryState.params venueId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "**Added 20 August from the client design board.** The operations existed and no screen called them. **Named in the board contents and not written up in it** — the operations are real, the layout is not. **Owns POS board frame(s) POS-4B** (client pack, 24 August). **Assigned by board purpose rather than by operation overlap** — three attempts at deriving that mapping produced plausible nonsense, and a reader who trusts a bad table is worse off than one who has none.",
  "density": "compact",
  "boardFrames": [
   "POS Board 4.dc.html#pos-4b"
  ],
  "pattern": "commandCentre",
  "patternReason": "3 independent reads and no read of one record — the screen watches a population rather than working one",
  "purpose": "Merchandising & Product Presentation — from the client design board, 20 August.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Merchandise",
       "bindsTo": "MerchandiseItem",
       "operation": "listMerchandise",
       "provenance": "contract retail.yaml GET /merchandise"
      },
      {
       "kind": "metricTile",
       "label": "Sale boards",
       "bindsTo": "SaleBoard",
       "operation": "listSaleBoards",
       "provenance": "contract tenancy.yaml GET /sale-boards"
      },
      {
       "kind": "metricTile",
       "label": "Workstations",
       "bindsTo": "Workstation",
       "operation": "listWorkstations",
       "provenance": "contract tenancy.yaml GET /workstations"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every merchandising product presentation",
       "bindsTo": "MerchandiseItem",
       "columns": [
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
        "MerchandiseItem.isReturnable",
        "MerchandiseItem.returnWindowDays"
       ],
       "operation": "listMerchandise",
       "provenance": "contract retail.yaml GET /merchandise"
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
       "operation": "updateMerchandise",
       "provenance": "contract retail.yaml PATCH /merchandise/{merchandiseId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "setRolePermissions",
       "provenance": "contract tenancy.yaml PUT /roles/{roleId}/permissions"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "setVenueSettings",
       "provenance": "contract tenancy.yaml PUT /venues/{venueId}/settings"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateSaleBoard",
       "provenance": "contract tenancy.yaml PUT /sale-boards/{saleBoardId}"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "searchField",
       "label": "Search merchandising",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The merchandising product presentation list.",
   "error": "Could not load. Names which read failed and leaves the merchandising product presentation untouched.",
   "emptyFirstRun": "No merchandising product presentation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the merchandising product presentation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listMerchandise",
    "contract": "retail",
    "purpose": "List merchandise",
    "trigger": "onLoad"
   },
   {
    "operationId": "updateMerchandise",
    "contract": "retail",
    "purpose": "Amend a merchandise item",
    "trigger": "onAction",
    "invalidates": [
     "listMerchandise"
    ]
   },
   {
    "operationId": "listSaleBoards",
    "contract": "tenancy",
    "purpose": "List sale boards",
    "trigger": "onLoad"
   },
   {
    "operationId": "listWorkstations",
    "contract": "tenancy",
    "purpose": "List workstations",
    "trigger": "onLoad"
   },
   {
    "operationId": "setRolePermissions",
    "contract": "tenancy",
    "purpose": "What this role may do",
    "trigger": "onAction",
    "invalidates": [
     "listMerchandise"
    ]
   },
   {
    "operationId": "setVenueSettings",
    "contract": "tenancy",
    "purpose": "Set support hours, quiet hours, segregated access and alerti",
    "trigger": "onAction",
    "invalidates": [
     "listMerchandise"
    ]
   },
   {
    "operationId": "updateSaleBoard",
    "contract": "tenancy",
    "purpose": "Update a sale board",
    "trigger": "onAction",
    "invalidates": [
     "listMerchandise"
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
     "name": "merchandiseId",
     "from": "deepLink"
    },
    {
     "name": "roleId",
     "from": "deepLink"
    },
    {
     "name": "saleBoardId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "Resolves from the session. A principal with more than one venue is asked which before the page renders. A role opened from the directory."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-116",
   "source": "Claude Design POS pack, 24 August",
   "note": "**Drawn by Claude Design on `POS Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
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
  "id": "BO-117",
  "name": "Product Import, Governance & AI Configuration Assistant",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 2,
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/product-import-governance-ai-configuration-assistant",
   "component": "apps/venue-management-web/src/routes/sell/ProductImportGovernanceAiConfigurationList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-102",
    "BO-116"
   ],
   "exitTo": [
    "BO-102",
    "BO-118"
   ],
   "inferred": false,
   "notes": "**Returns to BO-102.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "BO-118",
     "trigger": "Campaign & Audience Management",
     "provenance": "flow F86 step 3→4"
    },
    {
     "to": "BO-102",
     "trigger": "Sell",
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-102 declares entryState.params venueId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "**Added 20 August from the client design board.** The operations existed and no screen called them. **Named in the board contents and not written up in it** — the operations are real, the layout is not. **Owns POS board frame(s) POS-4C** (client pack, 24 August). **Assigned by board purpose rather than by operation overlap** — three attempts at deriving that mapping produced plausible nonsense, and a reader who trusts a bad table is worse off than one who has none.",
  "density": "compact",
  "boardFrames": [
   "POS Board 4.dc.html#pos-4c"
  ],
  "pattern": "listDetail",
  "patternReason": "`listSaleBoards` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Product Import, Governance & AI Configuration Assistant — from the client design board, 20 August.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every product import governance",
       "bindsTo": "SaleBoard",
       "columns": [
        "SaleBoard.id",
        "SaleBoard.code",
        "SaleBoard.name",
        "SaleBoard.venueId",
        "SaleBoard.kind",
        "SaleBoard.pages",
        "SaleBoard.isActive"
       ],
       "operation": "listSaleBoards",
       "provenance": "contract tenancy.yaml GET /sale-boards"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected product import governance",
       "bindsTo": "SaleBoard",
       "columns": [
        "SaleBoard.id",
        "SaleBoard.code",
        "SaleBoard.name",
        "SaleBoard.venueId",
        "SaleBoard.kind",
        "SaleBoard.pages",
        "SaleBoard.isActive"
       ],
       "operation": "listSaleBoards",
       "provenance": "contract tenancy.yaml GET /sale-boards"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Import",
       "operation": "importProductCatalogue",
       "provenance": "contract catalogue.yaml POST /products/import"
      },
      {
       "kind": "secondaryButton",
       "label": "Generate",
       "operation": "generateConfiguration",
       "provenance": "contract ai.yaml POST /generate/configuration"
      },
      {
       "kind": "secondaryButton",
       "label": "Request",
       "operation": "requestSuggestion",
       "provenance": "contract ai.yaml POST /ai/suggestions"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateSaleBoard",
       "provenance": "contract tenancy.yaml PUT /sale-boards/{saleBoardId}"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "searchField",
       "label": "Search product import, governance",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The product import governance list.",
   "error": "Could not load. Names which read failed and leaves the product import governance untouched.",
   "emptyFirstRun": "No product import governance yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the product import governance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "importProductCatalogue",
    "contract": "catalogue",
    "purpose": "Parse a catalogue file into a preview",
    "trigger": "onAction",
    "invalidates": [
     "listSaleBoards"
    ]
   },
   {
    "operationId": "generateConfiguration",
    "contract": "ai",
    "purpose": "Draft a configuration from a description",
    "trigger": "onAction",
    "invalidates": [
     "listSaleBoards"
    ]
   },
   {
    "operationId": "listSaleBoards",
    "contract": "tenancy",
    "purpose": "List sale boards",
    "trigger": "onLoad"
   },
   {
    "operationId": "requestSuggestion",
    "contract": "ai",
    "purpose": "requestSuggestion",
    "trigger": "onAction",
    "invalidates": [
     "listSaleBoards"
    ]
   },
   {
    "operationId": "updateSaleBoard",
    "contract": "tenancy",
    "purpose": "Update a sale board",
    "trigger": "onAction",
    "invalidates": [
     "listSaleBoards"
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
     "name": "saleBoardId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "Resolves from the session. A principal with more than one venue is asked which before the page renders.",
   "preloaded": [
    "SaleBoard.id",
    "SaleBoard.code",
    "SaleBoard.name",
    "SaleBoard.venueId",
    "SaleBoard.kind"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-117",
   "source": "Claude Design POS pack, 24 August",
   "note": "**Drawn by Claude Design on `POS Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
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
  "id": "BO-118",
  "name": "Campaign & Audience Management",
  "module": "Sell",
  "requiresModule": "marketing",
  "wave": 2,
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/campaign-audience-management",
   "component": "apps/venue-management-web/src/routes/sell/CampaignAudienceManagementList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-102",
    "BO-117"
   ],
   "exitTo": [
    "BO-102",
    "BO-126"
   ],
   "inferred": false,
   "notes": "**Returns to BO-102.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "BO-126",
     "trigger": "Deployment, Preview & Audit",
     "provenance": "flow F86 step 4→5",
     "operation": "createCampaign"
    },
    {
     "to": "BO-102",
     "trigger": "Sell",
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-102 declares entryState.params venueId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "**Added 20 August from the client design board.** The operations existed and no screen called them. **Owns POS board frame(s) POS-4D** (client pack, 24 August). **Assigned by board purpose rather than by operation overlap** — three attempts at deriving that mapping produced plausible nonsense, and a reader who trusts a bad table is worse off than one who has none.",
  "density": "compact",
  "boardFrames": [
   "POS Board 4.dc.html#pos-4d"
  ],
  "pattern": "commandCentre",
  "patternReason": "3 independent reads and no read of one record — the screen watches a population rather than working one",
  "purpose": "Campaign & Audience Management — from the client design board, 20 August.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Campaigns",
       "bindsTo": "Campaign",
       "operation": "listCampaigns",
       "provenance": "contract marketing-crm.yaml GET /campaigns"
      },
      {
       "kind": "metricTile",
       "label": "Segments",
       "bindsTo": "Segment",
       "operation": "listSegments",
       "provenance": "contract marketing-crm.yaml GET /segments"
      },
      {
       "kind": "metricTile",
       "label": "Sale boards",
       "bindsTo": "SaleBoard",
       "operation": "listSaleBoards",
       "provenance": "contract tenancy.yaml GET /sale-boards"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every campaign audience",
       "bindsTo": "Campaign",
       "columns": [
        "Campaign.name",
        "Campaign.kind",
        "Campaign.channel",
        "Campaign.venueId",
        "Campaign.segmentId",
        "Campaign.content",
        "Campaign.trigger",
        "Campaign.scheduledFor",
        "Campaign.consentPurpose",
        "Campaign.sendWindow",
        "Campaign.id",
        "Campaign.budgetCap"
       ],
       "operation": "listCampaigns",
       "provenance": "contract marketing-crm.yaml GET /campaigns"
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
       "operation": "createCampaign",
       "provenance": "contract marketing-crm.yaml POST /campaigns"
      },
      {
       "kind": "secondaryButton",
       "label": "Run",
       "operation": "runReport",
       "provenance": "contract reporting.yaml POST /reports/{reportId}/run"
      },
      {
       "kind": "secondaryButton",
       "label": "Save changes",
       "operation": "updateSaleBoard",
       "provenance": "contract tenancy.yaml PUT /sale-boards/{saleBoardId}"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "searchField",
       "label": "Search campaign",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The campaign audience list.",
   "error": "Could not load. Names which read failed and leaves the campaign audience untouched.",
   "emptyFirstRun": "No campaign audience yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the campaign audience are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCampaigns",
    "contract": "marketing-crm",
    "purpose": "List campaigns",
    "trigger": "onLoad"
   },
   {
    "operationId": "createCampaign",
    "contract": "marketing-crm",
    "purpose": "Create a campaign",
    "trigger": "onAction",
    "invalidates": [
     "listCampaigns"
    ]
   },
   {
    "operationId": "listSegments",
    "contract": "marketing-crm",
    "purpose": "List segments",
    "trigger": "onLoad"
   },
   {
    "operationId": "listSaleBoards",
    "contract": "tenancy",
    "purpose": "List sale boards",
    "trigger": "onLoad"
   },
   {
    "operationId": "runReport",
    "contract": "reporting",
    "purpose": "Run a report",
    "trigger": "onAction",
    "invalidates": [
     "listCampaigns"
    ]
   },
   {
    "operationId": "updateSaleBoard",
    "contract": "tenancy",
    "purpose": "Update a sale board",
    "trigger": "onAction",
    "invalidates": [
     "listCampaigns"
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
     "name": "reportId",
     "from": "deepLink"
    },
    {
     "name": "saleBoardId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "Resolves from the session. A principal with more than one venue is asked which before the page renders."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-118",
   "source": "Claude Design POS pack, 24 August",
   "note": "**Drawn by Claude Design on `POS Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
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
  "id": "BO-119",
  "name": "Cross-Sell, Upsell & Recommendation Rules",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 2,
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/cross-sell-upsell-recommendation-rules",
   "component": "apps/venue-management-web/src/routes/sell/CrossSellUpsellRecommendationRulesList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-102"
   ],
   "exitTo": [
    "BO-010",
    "BO-102"
   ],
   "inferred": false,
   "notes": "**Returns to BO-102.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "BO-010",
     "trigger": "Promotions & Coupons",
     "provenance": "flow F90 step 1→2"
    },
    {
     "to": "BO-102",
     "trigger": "Sell",
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-102 declares entryState.params venueId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "**Added 20 August from the client design board.** The operations existed and no screen called them. **Named in the board contents and not written up in it** — the operations are real, the layout is not.",
  "density": "compact",
  "boardFrames": [
   "Retail Board 5.dc.html#ret-5d"
  ],
  "pattern": "statusTracker",
  "patternReason": "`getRecommendations` reads one record and nothing reads a population — the screen is about that one thing",
  "purpose": "Cross-Sell, Upsell & Recommendation Rules — from the client design board, 20 August.",
  "gaps": [
   {
    "operation": "getRecommendations",
    "why": "**2 declared operations reach no component on this screen**: getRecommendations, getUpsellSuggestions. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
   }
  ],
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "searchField",
       "label": "Search cross-sell, upsell",
       "provenance": "carried from the previous definition"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "getRecommendations",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "getRecommendations"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The cross-sell upsell recommendation list.",
   "error": "Could not load. Names which read failed and leaves the cross-sell upsell recommendation untouched.",
   "emptyFirstRun": "No cross-sell upsell recommendation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the cross-sell upsell recommendation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getRecommendations",
    "contract": "promotions",
    "purpose": "What else this guest might want",
    "trigger": "onAction"
   },
   {
    "operationId": "getUpsellSuggestions",
    "contract": "promotions",
    "purpose": "Suggestions for a cart",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    }
   ],
   "coldEntry": "Resolves from the session. A principal with more than one venue is asked which before the page renders."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-119",
   "source": "Claude Design Retail pack, 24 August",
   "note": "**Drawn by Claude Design on `Retail Board 5.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "BO-120",
  "name": "Omnichannel Commerce & Journey Configuration",
  "module": "Sell",
  "requiresModule": "marketing",
  "wave": 2,
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/omnichannel-commerce-journey-configuration",
   "component": "apps/venue-management-web/src/routes/sell/OmnichannelCommerceJourneyConfiguratioList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-102"
   ],
   "exitTo": [
    "BO-102"
   ],
   "inferred": false,
   "notes": "**Returns to BO-102.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "BO-102",
     "trigger": "Sell",
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-102 declares entryState.params venueId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "**Added 20 August from the client design board.** The operations existed and no screen called them. **Named in the board contents and not written up in it** — the operations are real, the layout is not. **Drawn 31 August** — `Retail Board 5.dc.html` frame `ret-5g`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Omnichannel Commerce &amp; Journey Configuration* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.",
  "density": "compact",
  "boardFrames": [
   "Retail Board 5.dc.html#ret-5g"
  ],
  "pattern": "listDetail",
  "patternReason": "`listJourneys` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Omnichannel Commerce & Journey Configuration — from the client design board, 20 August.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every omnichannel commerce journey",
       "bindsTo": "Journey",
       "columns": [
        "Journey.id",
        "Journey.name",
        "Journey.templateKind",
        "Journey.entryEvent",
        "Journey.entryConditions",
        "Journey.steps",
        "Journey.status",
        "Journey.maxDurationDays",
        "Journey.reentryPolicy",
        "Journey.scopePath"
       ],
       "operation": "listJourneys",
       "provenance": "contract marketing-crm.yaml GET /journeys"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected omnichannel commerce journey",
       "bindsTo": "Journey",
       "columns": [
        "Journey.id",
        "Journey.name",
        "Journey.templateKind",
        "Journey.entryEvent",
        "Journey.entryConditions",
        "Journey.steps",
        "Journey.status",
        "Journey.maxDurationDays",
        "Journey.reentryPolicy",
        "Journey.scopePath"
       ],
       "operation": "listJourneys",
       "provenance": "contract marketing-crm.yaml GET /journeys"
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
       "operation": "createJourney",
       "provenance": "contract marketing-crm.yaml POST /journeys"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "searchField",
       "label": "Search omnichannel commerce",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The omnichannel commerce journey list.",
   "error": "Could not load. Names which read failed and leaves the omnichannel commerce journey untouched.",
   "emptyFirstRun": "No omnichannel commerce journey yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the omnichannel commerce journey are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listJourneys",
    "contract": "marketing-crm",
    "purpose": "Automated journeys",
    "trigger": "onLoad"
   },
   {
    "operationId": "createJourney",
    "contract": "marketing-crm",
    "purpose": "Define an automated journey",
    "trigger": "onAction",
    "invalidates": [
     "listJourneys"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    }
   ],
   "coldEntry": "Resolves from the session. A principal with more than one venue is asked which before the page renders.",
   "preloaded": [
    "Journey.id",
    "Journey.name",
    "Journey.templateKind",
    "Journey.entryEvent",
    "Journey.entryConditions"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-120",
   "note": "**Drawn by Claude Design on `Retail Board 5.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "BO-121",
  "name": "Personalized Offers & Guest Engagement",
  "module": "Sell",
  "requiresModule": "marketing",
  "wave": 2,
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/personalized-offers-guest-engagement",
   "component": "apps/venue-management-web/src/routes/sell/PersonalizedOffersGuestEngagementList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-102"
   ],
   "exitTo": [
    "BO-102"
   ],
   "inferred": false,
   "notes": "**Returns to BO-102.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "BO-102",
     "trigger": "Sell",
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-102 declares entryState.params venueId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "**Added 20 August from the client design board.** The operations existed and no screen called them.",
  "density": "compact",
  "boardFrames": [
   "Retail Board 5.dc.html#ret-5f"
  ],
  "pattern": "listDetail",
  "patternReason": "`listSegments` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Personalized Offers & Guest Engagement — from the client design board, 20 August.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every personalized offers guest",
       "bindsTo": "Segment",
       "columns": [
        "Segment.name",
        "Segment.description",
        "Segment.venueId",
        "Segment.match",
        "Segment.criteria",
        "Segment.excludeSegmentIds",
        "Segment.id",
        "Segment.lastEvaluatedSize",
        "Segment.lastEvaluatedAt"
       ],
       "operation": "listSegments",
       "provenance": "contract marketing-crm.yaml GET /segments"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected personalized offers guest",
       "bindsTo": "Segment",
       "columns": [
        "Segment.name",
        "Segment.description",
        "Segment.venueId",
        "Segment.match",
        "Segment.criteria",
        "Segment.excludeSegmentIds",
        "Segment.id",
        "Segment.lastEvaluatedSize",
        "Segment.lastEvaluatedAt"
       ],
       "operation": "listSegments",
       "provenance": "contract marketing-crm.yaml GET /segments"
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
       "operation": "createCampaign",
       "provenance": "contract marketing-crm.yaml POST /campaigns"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "searchField",
       "label": "Search personalized offers",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The personalized offers guest list.",
   "error": "Could not load. Names which read failed and leaves the personalized offers guest untouched.",
   "emptyFirstRun": "No personalized offers guest yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the personalized offers guest are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listSegments",
    "contract": "marketing-crm",
    "purpose": "List segments",
    "trigger": "onLoad"
   },
   {
    "operationId": "createCampaign",
    "contract": "marketing-crm",
    "purpose": "Create a campaign",
    "trigger": "onAction",
    "invalidates": [
     "listSegments"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    }
   ],
   "coldEntry": "Resolves from the session. A principal with more than one venue is asked which before the page renders.",
   "preloaded": [
    "Segment.name",
    "Segment.description",
    "Segment.venueId",
    "Segment.match",
    "Segment.criteria"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-121",
   "source": "Claude Design Retail pack, 24 August",
   "note": "**Drawn by Claude Design on `Retail Board 5.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
  "id": "BO-122",
  "name": "POS Experience Dashboard",
  "module": "Sell",
  "requiresModule": "core",
  "wave": 2,
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/pos-experience-dashboard",
   "component": "apps/venue-management-web/src/routes/sell/PosExperienceDashboardList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-102"
   ],
   "exitTo": [
    "BO-102"
   ],
   "inferred": false,
   "notes": "**Returns to BO-102.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "BO-102",
     "trigger": "Sell",
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-102 declares entryState.params venueId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "**Added 20 August from the client design board.** The operations existed and no screen called them. **Named in the board contents and not written up in it** — the operations are real, the layout is not.",
  "density": "compact",
  "boardFrames": [
   "Retail Board 5.dc.html#ret-5j"
  ],
  "pattern": "listDetail",
  "patternReason": "`listSaleBoards` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "POS Experience Dashboard — from the client design board, 20 August.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every pos experience",
       "bindsTo": "SaleBoard",
       "columns": [
        "SaleBoard.id",
        "SaleBoard.code",
        "SaleBoard.name",
        "SaleBoard.venueId",
        "SaleBoard.kind",
        "SaleBoard.pages",
        "SaleBoard.isActive"
       ],
       "operation": "listSaleBoards",
       "provenance": "contract tenancy.yaml GET /sale-boards"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected pos experience",
       "bindsTo": "SaleBoard",
       "columns": [
        "SaleBoard.id",
        "SaleBoard.code",
        "SaleBoard.name",
        "SaleBoard.venueId",
        "SaleBoard.kind",
        "SaleBoard.pages",
        "SaleBoard.isActive"
       ],
       "operation": "listSaleBoards",
       "provenance": "contract tenancy.yaml GET /sale-boards"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "searchField",
       "label": "Search pos experience dashboard",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The pos experience list.",
   "error": "Could not load. Names which read failed and leaves the pos experience untouched.",
   "emptyFirstRun": "No pos experience yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the pos experience are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listSaleBoards",
    "contract": "tenancy",
    "purpose": "List sale boards",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    }
   ],
   "coldEntry": "Resolves from the session. A principal with more than one venue is asked which before the page renders.",
   "preloaded": [
    "SaleBoard.id",
    "SaleBoard.code",
    "SaleBoard.name",
    "SaleBoard.venueId",
    "SaleBoard.kind"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-122",
   "source": "Claude Design Retail pack, 24 August",
   "note": "**Drawn by Claude Design on `Retail Board 5.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
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
  "id": "BO-123",
  "name": "POS Profile Management",
  "module": "Sell",
  "requiresModule": "core",
  "wave": 2,
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/pos-profile-management",
   "component": "apps/venue-management-web/src/routes/sell/PosProfileManagementList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-102"
   ],
   "exitTo": [
    "BO-102"
   ],
   "inferred": false,
   "notes": "**Returns to BO-102.** Stated on 4 September: this screen declared where it is reached from and no way to leave, so whoever landed on it was stuck. The return path is the same edge travelled the other way, not a guess about the product.",
   "transitions": [
    {
     "to": "BO-102",
     "trigger": "Sell",
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-102 declares entryState.params venueId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "**Added 20 August from the client design board.** The operations existed and no screen called them. **Named in the board contents and not written up in it** — the operations are real, the layout is not.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listSaleBoards` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "POS Profile Management — from the client design board, 20 August.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every pos profile",
       "bindsTo": "SaleBoard",
       "columns": [
        "SaleBoard.id",
        "SaleBoard.code",
        "SaleBoard.name",
        "SaleBoard.venueId",
        "SaleBoard.kind",
        "SaleBoard.pages",
        "SaleBoard.isActive"
       ],
       "operation": "listSaleBoards",
       "provenance": "contract tenancy.yaml GET /sale-boards"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected pos profile",
       "bindsTo": "SaleBoard",
       "columns": [
        "SaleBoard.id",
        "SaleBoard.code",
        "SaleBoard.name",
        "SaleBoard.venueId",
        "SaleBoard.kind",
        "SaleBoard.pages",
        "SaleBoard.isActive"
       ],
       "operation": "listSaleBoards",
       "provenance": "contract tenancy.yaml GET /sale-boards"
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
       "operation": "setConfigurationProfile",
       "provenance": "contract tenancy.yaml PUT /configuration-profiles"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "carried",
     "components": [
      {
       "kind": "searchField",
       "label": "Search pos profile management",
       "provenance": "carried from the previous definition"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The pos profile list.",
   "error": "Could not load. Names which read failed and leaves the pos profile untouched.",
   "emptyFirstRun": "No pos profile yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the pos profile are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setConfigurationProfile",
    "contract": "tenancy",
    "purpose": "setConfigurationProfile",
    "trigger": "onAction",
    "invalidates": [
     "listSaleBoards"
    ]
   },
   {
    "operationId": "listSaleBoards",
    "contract": "tenancy",
    "purpose": "List sale boards",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    }
   ],
   "coldEntry": "Resolves from the session. A principal with more than one venue is asked which before the page renders.",
   "preloaded": [
    "SaleBoard.id",
    "SaleBoard.code",
    "SaleBoard.name",
    "SaleBoard.venueId",
    "SaleBoard.kind"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-123"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
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
 "createCampaign": {
  "method": "POST",
  "path": "/campaigns",
  "contract": "marketing-crm",
  "summary": "Create a campaign",
  "permission": "MARKETING_MANAGE",
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
  "requestBody": "CreateCampaignRequest",
  "responds": "Campaign"
 },
 "createJourney": {
  "method": "POST",
  "path": "/journeys",
  "contract": "marketing-crm",
  "summary": "Define an automated journey",
  "permission": "MARKETING_MANAGE",
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
  "requestBody": "Journey",
  "responds": "Journey"
 },
 "generateConfiguration": {
  "method": "POST",
  "path": "/generate/configuration",
  "contract": "ai",
  "summary": "Draft a configuration from a description",
  "permission": "AI_USE",
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
  "responds": "GeneratedConfiguration"
 },
 "getRecommendations": {
  "method": "POST",
  "path": "/recommendations",
  "contract": "promotions",
  "summary": "What else this guest might want",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": null
 },
 "getUpsellSuggestions": {
  "method": "POST",
  "path": "/upsell-suggestions",
  "contract": "promotions",
  "summary": "Suggestions for a cart",
  "permission": "PRODUCT_VIEW",
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
  "responds": null
 },
 "importProductCatalogue": {
  "method": "POST",
  "path": "/products/import",
  "contract": "catalogue",
  "summary": "Parse a catalogue file into a preview",
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
 "listCampaigns": {
  "method": "GET",
  "path": "/campaigns",
  "contract": "marketing-crm",
  "summary": "List campaigns",
  "permission": "MARKETING_VIEW",
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
 "listJourneys": {
  "method": "GET",
  "path": "/journeys",
  "contract": "marketing-crm",
  "summary": "Automated journeys",
  "permission": "MARKETING_VIEW",
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
  "responds": "Journey"
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
 "listProductCategories": {
  "method": "GET",
  "path": "/product-categories",
  "contract": "catalogue",
  "summary": "The merchandise hierarchy — categories, brands, collections",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ProductCategory"
 },
 "listSaleBoards": {
  "method": "GET",
  "path": "/sale-boards",
  "contract": "tenancy",
  "summary": "List sale boards",
  "permission": "SCOPE_VIEW",
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
   }
  ],
  "requestBody": null,
  "responds": "SaleBoard"
 },
 "listSegments": {
  "method": "GET",
  "path": "/segments",
  "contract": "marketing-crm",
  "summary": "List segments",
  "permission": "MARKETING_VIEW",
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
 "listSerialisedItems": {
  "method": "GET",
  "path": "/serialised-items",
  "contract": "inventory",
  "summary": "Where each individual item is",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "serial",
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
  "responds": "SerialisedItem"
 },
 "listWorkstations": {
  "method": "GET",
  "path": "/workstations",
  "contract": "tenancy",
  "summary": "List workstations",
  "permission": "SCOPE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "venueId",
    "in": "query",
    "required": null
   },
   {
    "name": "saleBoardKind",
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
 "lookupMerchandise": {
  "method": "GET",
  "path": "/merchandise/lookup",
  "contract": "retail",
  "summary": "Price and stock check by barcode",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "barcode",
    "in": "query",
    "required": null
   },
   {
    "name": "sku",
    "in": "query",
    "required": null
   },
   {
    "name": "includeSiblingOutlets",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "PriceCheck"
 },
 "requestSuggestion": {
  "method": "POST",
  "path": "/ai/suggestions",
  "contract": "ai",
  "summary": "Ask for an answer, however it is currently produced",
  "permission": "AI_USE",
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
  "responds": "Suggestion"
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
 "setConfigurationProfile": {
  "method": "PUT",
  "path": "/configuration-profiles",
  "contract": "tenancy",
  "summary": "What a class of workstation is configured to be",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "ConfigurationProfile",
  "responds": "ConfigurationProfile"
 },
 "setProductCategories": {
  "method": "PUT",
  "path": "/product-categories",
  "contract": "catalogue",
  "summary": "Define the hierarchy, in the order a guest sees it",
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
  "responds": "ProductCategory"
 },
 "setRolePermissions": {
  "method": "PUT",
  "path": "/roles/{roleId}/permissions",
  "contract": "tenancy",
  "summary": "What this role may do",
  "permission": "ROLE_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
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
 "setVenueSettings": {
  "method": "PUT",
  "path": "/venues/{venueId}/settings",
  "contract": "tenancy",
  "summary": "Set support hours, quiet hours, segregated access and alerting",
  "permission": "TENANT_CONFIGURE",
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
  "requestBody": "VenueSettings",
  "responds": "VenueSettings"
 },
 "updateMerchandise": {
  "method": "PATCH",
  "path": "/merchandise/{merchandiseId}",
  "contract": "retail",
  "summary": "Amend a merchandise item",
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
  "responds": "MerchandiseItem"
 },
 "updateSaleBoard": {
  "method": "PUT",
  "path": "/sale-boards/{saleBoardId}",
  "contract": "tenancy",
  "summary": "Update a sale board",
  "permission": "WORKSTATION_CONFIGURE",
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
  "requestBody": "SaleBoard",
  "responds": "SaleBoard"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "Campaign": {
  "x-ticvai-persistence": "marketing.campaign",
  "allOf": [
   {
    "$ref": "#/components/schemas/CreateCampaignRequest"
   },
   {
    "type": "object",
    "required": [
     "id",
     "status",
     "createdAt"
    ],
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid"
     },
     "budgetCap": {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     },
     "budgetSpent": {
      "allOf": [
       {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      ],
      "readOnly": true,
      "description": "BL-169. **A campaign could spend without limit** — following the promotions `budgetCap` precedent. **Sending stops at the cap rather than overspending and reporting it**, because a marketing budget discovered after it was exceeded is a budget nobody set.\n"
     },
     "status": {
      "$ref": "#/components/schemas/CampaignStatus"
     },
     "isPaused": {
      "type": "boolean"
     },
     "createdByPrincipalId": {
      "type": "string",
      "format": "uuid"
     },
     "createdAt": {
      "type": "string",
      "format": "date-time"
     },
     "launchedAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     },
     "completedAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     }
    }
   }
  ]
 },
 "CampaignContent": {
  "x-ticvai-persistence": "none — embedded in campaign",
  "type": "object",
  "required": [
   "templateId"
  ],
  "properties": {
   "templateId": {
    "type": "string",
    "format": "uuid"
   },
   "subjectOverride": {
    "type": "object",
    "additionalProperties": {
     "type": "string"
    }
   },
   "mergeDefaults": {
    "type": "object",
    "additionalProperties": true
   },
   "promotionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Offer carried by the campaign. Coupon codes are issued from it."
   }
  }
 },
 "CampaignKind": {
  "type": "string",
  "enum": [
   "oneOff",
   "scheduled",
   "triggered",
   "recurring"
  ]
 },
 "CampaignStatus": {
  "type": "string",
  "enum": [
   "draft",
   "scheduled",
   "sending",
   "paused",
   "completed",
   "stopped",
   "failed"
  ]
 },
 "CampaignTrigger": {
  "x-ticvai-persistence": "none — embedded in campaign",
  "type": "object",
  "properties": {
   "event": {
    "type": "string",
    "enum": [
     "bookingConfirmed",
     "visitCompleted",
     "membershipExpiring",
     "birthday",
     "abandonedCart",
     "firstVisit",
     "inactivity"
    ]
   },
   "delayHours": {
    "type": "integer"
   },
   "conditions": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/SegmentCriterion"
    }
   }
  }
 },
 "ConfigurationProfile": {
  "type": "object",
  "x-ticvai-persistence": "platform.configuration_profile",
  "description": "Board 1 of the client's POS design set, 20 August. **The board shows 1,248 workstations across four versions and the package modelled none of it** — a firmware version field on the workstation, and nothing that says what a workstation is configured to be.\n**A profile is what a venue changes; a version is what it deploys.** Conflating them means a venue cannot say *roll the ticketing counters back and leave the kiosks alone*, which is the only reason to version a profile at all.\n",
  "required": [
   "id",
   "name",
   "venueKindScope",
   "version",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string"
   },
   "scopePath": {
    "type": "string"
   },
   "venueKindScope": {
    "type": "array",
    "description": "Which workstation types it applies to. **A ticketing counter and a kitchen display do not share a profile**, and a profile that claims to is a profile somebody deploys to the wrong fleet.\n",
    "items": {
     "type": "string"
    }
   },
   "version": {
    "type": "integer",
    "description": "**Immutable once deployed anywhere.** A change makes a new version, and the old one stays readable — a workstation still running v2.3 must be able to say what v2.3 was.\n"
   },
   "settings": {
    "type": "object",
    "additionalProperties": true
   },
   "status": {
    "type": "string",
    "enum": [
     "draft",
     "published",
     "deploying",
     "deployed",
     "superseded",
     "rolledBack"
    ]
   },
   "deployedCount": {
    "type": "integer",
    "readOnly": true
   },
   "publishedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "ConsentPurpose": {
  "type": "string",
  "enum": [
   "marketing",
   "personalisation",
   "profiling",
   "thirdPartySharing",
   "aiProcessing",
   "transactional"
  ]
 },
 "CreateCampaignRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "name",
   "kind",
   "channel",
   "segmentId",
   "content"
  ],
  "properties": {
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "kind": {
    "$ref": "#/components/schemas/CampaignKind"
   },
   "channel": {
    "$ref": "#/components/schemas/MessageChannel"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "segmentId": {
    "type": "string",
    "format": "uuid"
   },
   "content": {
    "$ref": "#/components/schemas/CampaignContent"
   },
   "trigger": {
    "$ref": "#/components/schemas/CampaignTrigger"
   },
   "scheduledFor": {
    "type": "string",
    "format": "date-time"
   },
   "consentPurpose": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ConsentPurpose"
     }
    ],
    "default": "marketing"
   },
   "sendWindow": {
    "type": "object",
    "description": "Hours during which sending is permitted. A promotional message at 3am is a complaint waiting to happen.\n",
    "properties": {
     "startTime": {
      "type": "string"
     },
     "endTime": {
      "type": "string"
     },
     "timeZone": {
      "type": "string"
     }
    }
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
 "GeneratedConfiguration": {
  "type": "object",
  "x-ticvai-persistence": "none — a draft, applied through the owning contract",
  "required": [
   "kind",
   "targetContract",
   "targetOperation",
   "payload"
  ],
  "properties": {
   "kind": {
    "type": "string"
   },
   "targetContract": {
    "type": "string"
   },
   "targetOperation": {
    "type": "string"
   },
   "payload": {
    "type": "object",
    "additionalProperties": true
   },
   "assumptions": {
    "type": "array",
    "description": "**What it had to guess.** An admin reviewing a draft needs to know which fields came from what they said and which the assistant chose, or they approve a decision they did not make.\n",
    "items": {
     "type": "object",
     "properties": {
      "field": {
       "type": "string"
      },
      "value": {
       "type": "string"
      },
      "reason": {
       "type": "string"
      }
     }
    }
   },
   "clarificationsNeeded": {
    "type": "array",
    "description": "What it could not resolve and should ask about.",
    "items": {
     "type": "string"
    }
   },
   "confidence": {
    "type": "number",
    "nullable": true
   },
   "traceId": {
    "type": "string"
   }
  }
 },
 "Journey": {
  "type": "object",
  "x-ticvai-persistence": "marketing.journey",
  "description": "22.3.1b to 22.3.10b, CF-137. **A journey is a sequence with branches; a `MessageTrigger` is one step of it.** The trigger already handles *\"send this when that happens\"* — a journey is what you need when the next message depends on what the guest did about the last one.\nFive of the ten requirements are named lifecycles — abandoned cart, membership, loyalty, wallet, birthday. **They are not five features.** Each is a journey with a different entry event and a different set of steps, which is why this is one entity and a template library rather than five contracts.\n**Consent is checked at every send, not at entry.** A guest who opts out mid-journey stops receiving, and the journey does not need to know — the same rule `MessageTrigger` follows and the one PDPL Article 17(1) makes unconditional.\n",
  "required": [
   "id",
   "name",
   "entryEvent",
   "status",
   "steps"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string"
   },
   "templateKind": {
    "type": "string",
    "nullable": true,
    "enum": [
     "abandonedCart",
     "membershipLifecycle",
     "loyaltyLifecycle",
     "walletLifecycle",
     "birthday",
     "onboarding",
     "winBack",
     "custom"
    ],
    "description": "Which named lifecycle this implements. **Set for reporting and for the library**, not for behaviour — the steps decide what happens.\n"
   },
   "entryEvent": {
    "type": "string",
    "description": "22.3.2b. From the event catalogue, so a journey cannot enter on something nothing publishes.\n"
   },
   "entryConditions": {
    "type": "object",
    "nullable": true,
    "description": "Narrows entry — a segment, a tier, a venue. **Evaluated once at entry**, unlike step conditions.\n"
   },
   "steps": {
    "type": "array",
    "description": "22.3.1b. What the builder produces. **The visual builder is a frontend over this** — the contract holds the graph and the canvas is a rendering of it.\n",
    "items": {
     "$ref": "#/components/schemas/JourneyStep"
    }
   },
   "status": {
    "type": "string",
    "enum": [
     "draft",
     "active",
     "paused",
     "archived"
    ]
   },
   "maxDurationDays": {
    "type": "integer",
    "default": 30,
    "description": "**A journey with no end is a guest who never leaves it.** After this, entrants exit wherever they are.\n"
   },
   "reentryPolicy": {
    "type": "string",
    "enum": [
     "never",
     "afterCompletion",
     "always"
    ],
    "default": "afterCompletion",
    "description": "22.3.6b. **Abandoned cart is the case that needs this.** A guest who abandons three carts in an hour should not get three recovery sequences, and `never` is wrong too — they may genuinely abandon one next month.\n"
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"
   }
  }
 },
 "JourneyStep": {
  "type": "object",
  "description": "One node. **A step either sends, waits, or branches** — three kinds rather than a general graph, because a marketing user drawing an arbitrary graph draws a loop.\n",
  "required": [
   "id",
   "kind"
  ],
  "properties": {
   "id": {
    "type": "string"
   },
   "kind": {
    "type": "string",
    "enum": [
     "send",
     "wait",
     "branch",
     "exit",
     "goal"
    ]
   },
   "templateId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "For `send`. Channel is resolved from the guest's preference at the moment of sending."
   },
   "channelPreference": {
    "type": "array",
    "nullable": true,
    "description": "22.3.3b. Ordered fallback — email, then SMS, then push. **A guest with no email address does not get an email step**, and the step does not fail, it moves down the list.\n",
    "items": {
     "type": "string",
     "enum": [
      "email",
      "sms",
      "whatsapp",
      "push",
      "inApp"
     ]
    }
   },
   "waitMinutes": {
    "type": "integer",
    "nullable": true
   },
   "waitUntil": {
    "type": "object",
    "nullable": true,
    "description": "22.3.5b. **Business hours, time zone and blackout windows** — a wallet low-balance alert at 3am is a complaint, and the venue's quiet hours are venue configuration rather than a property of this step.\n",
    "properties": {
     "businessHoursOnly": {
      "type": "boolean",
      "default": false
     },
     "timezone": {
      "type": "string",
      "nullable": true
     },
     "respectQuietHours": {
      "type": "boolean",
      "default": true
     },
     "notBefore": {
      "type": "string",
      "nullable": true
     }
    }
   },
   "condition": {
    "type": "object",
    "nullable": true,
    "description": "22.3.4b. IF/THEN over guest profile, behaviour and prior steps. **The most common condition is whether the previous message worked** — a recovery sequence must stop when the guest buys.\n",
    "properties": {
     "field": {
      "type": "string"
     },
     "operator": {
      "type": "string",
      "enum": [
       "eq",
       "neq",
       "gt",
       "lt",
       "contains",
       "exists",
       "notExists"
      ]
     },
     "value": {
      "type": "string",
      "nullable": true
     }
    }
   },
   "onTrue": {
    "type": "string",
    "nullable": true,
    "description": "Next step id."
   },
   "onFalse": {
    "type": "string",
    "nullable": true
   },
   "next": {
    "type": "string",
    "nullable": true
   },
   "goalEvent": {
    "type": "string",
    "nullable": true,
    "description": "For `goal`. **The event that means this journey worked and the guest should leave it** — a purchase for abandoned cart, a renewal for membership. **Reaching a goal exits immediately**, which is what stops a recovered cart from being chased.\n"
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
 "MessageChannel": {
  "type": "string",
  "enum": [
   "email",
   "sms",
   "whatsapp",
   "push",
   "inApp",
   "post"
  ]
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
 "PriceCheck": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "merchandiseId",
   "name",
   "listPrice",
   "effectivePrice",
   "onHand"
  ],
  "properties": {
   "merchandiseId": {
    "type": "string",
    "format": "uuid"
   },
   "sku": {
    "type": "string"
   },
   "name": {
    "type": "string"
   },
   "listPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "effectivePrice": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "After any live promotion."
   },
   "appliedPromotionCode": {
    "type": "string",
    "nullable": true
   },
   "onHand": {
    "type": "number"
   },
   "isAvailable": {
    "type": "boolean"
   },
   "siblingOutlets": {
    "type": "array",
    "description": "Stock elsewhere in the venue, so a colleague can be sent.",
    "items": {
     "type": "object",
     "properties": {
      "outletId": {
       "type": "string",
       "format": "uuid"
      },
      "outletName": {
       "type": "string"
      },
      "onHand": {
       "type": "number"
      }
     }
    }
   }
  }
 },
 "ProductCategory": {
  "type": "object",
  "x-ticvai-persistence": "catalogue.product_category",
  "description": "Retail Board 2 of the client's design set, 20 August. **`listSeatCategories` existed and a product category did not** — a seat category prices a seat, and a merchandise hierarchy groups a catalogue.\n**Brand sits here rather than as its own entity.** A venue with four brands and a hierarchy five levels deep can express that with a parent; a venue with one brand should not have to maintain a table containing one row.\n**`displayOrder` is not alphabetical and that is the point.** A retail category list runs in the order the merchandiser wants a guest to see it, and sorting by name puts *Accessories* above *Apparel* forever.\n",
  "required": [
   "id",
   "name",
   "kind"
  ],
  "properties": {
   "id": {
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
   "kind": {
    "type": "string",
    "enum": [
     "category",
     "brand",
     "collection",
     "season",
     "department"
    ]
   },
   "parentId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**One tree, not four.** A brand under a department under a category is how a real merchandise hierarchy runs, and separate tables for each level cannot express a venue that nests them differently.\n"
   },
   "scopePath": {
    "type": "string"
   },
   "displayOrder": {
    "type": "integer",
    "default": 100
   },
   "imageAssetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "isActive": {
    "type": "boolean",
    "default": true,
    "description": "**Deactivated rather than deleted.** A category with a season behind it still names the products sold under it, and removing it rewrites last year's report.\n"
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
 "SaleBoard": {
  "x-ticvai-persistence": "platform.sale_board",
  "type": "object",
  "required": [
   "id",
   "code",
   "name",
   "venueId",
   "kind",
   "pages"
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
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "$ref": "#/components/schemas/SaleBoardKind"
   },
   "pages": {
    "type": "array",
    "minItems": 1,
    "items": {
     "type": "object",
     "required": [
      "name",
      "sortOrder",
      "tiles"
     ],
     "properties": {
      "name": {
       "type": "string"
      },
      "sortOrder": {
       "type": "integer"
      },
      "tiles": {
       "type": "array",
       "items": {
        "type": "object",
        "required": [
         "position",
         "kind"
        ],
        "properties": {
         "position": {
          "type": "integer"
         },
         "kind": {
          "type": "string",
          "enum": [
           "product",
           "category",
           "action",
           "spacer"
          ]
         },
         "variantId": {
          "type": "string",
          "format": "uuid",
          "nullable": true
         },
         "label": {
          "type": "string"
         },
         "colour": {
          "type": "string",
          "nullable": true
         },
         "imageAssetRef": {
          "type": "string",
          "nullable": true
         }
        }
       }
      }
     }
    }
   },
   "isActive": {
    "type": "boolean"
   }
  }
 },
 "SaleBoardKind": {
  "type": "string",
  "enum": [
   "ticketing",
   "fnb",
   "retail",
   "mixed"
  ]
 },
 "SerialisedItem": {
  "type": "object",
  "x-ticvai-persistence": "inventory.serialised_item",
  "description": "Retail Board 4 of the client's design set, 20 August. **`StockBatch` was added on 18 August with a lot number, and serialisation to the individual item is a step beyond it.**\nA lot answers *which delivery did this come from*. A serial answers *where is this exact one* — which is what a jewellery counter, a phone, a ticketed collectible or anything with a warranty needs.\n**Most stock is not serialised and should not be.** Turning it on for a 2 AED keyring creates a row per keyring, so it is a per-item decision rather than a policy.\n",
  "required": [
   "id",
   "itemId",
   "serial",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "itemId": {
    "type": "string",
    "format": "uuid"
   },
   "batchId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The batch it arrived in, where the item is both lotted and serialised."
   },
   "serial": {
    "type": "string",
    "description": "**Unique within the item, not globally.** Two manufacturers reuse serial numbers and a global constraint would refuse the second one.\n"
   },
   "locationId": {
    "type": "string",
    "format": "uuid"
   },
   "status": {
    "type": "string",
    "enum": [
     "inStock",
     "reserved",
     "sold",
     "returned",
     "damaged",
     "lost",
     "inTransit",
     "warranty"
    ]
   },
   "soldOnOrderLineId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**The link that makes serialisation worth having.** A warranty claim, a recall and a proof of purchase all start with *which sale was this exact item*.\n"
   },
   "warrantyUntil": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "receivedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "Suggestion": {
  "type": "object",
  "x-ticvai-persistence": "ai.suggestion",
  "description": "One answer to one question, with its reasoning and its confidence. **Built 24 August so that machine learning can be swapped in without touching a screen.**\n**A suggestion is never an action.** It proposes; `ProposedAction` and its approval path decide. A model that can order stock is a model that will order stock wrongly at three in the morning.\n**`inputs` is recorded, not just referenced.** A suggestion that cannot be reproduced cannot be defended to a finance controller asking why the system said to order four hundred.\n",
  "required": [
   "id",
   "kind",
   "basis",
   "producedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "$ref": "#/components/schemas/SuggestionKind"
   },
   "basis": {
    "$ref": "#/components/schemas/SuggestionBasis"
   },
   "scopePath": {
    "type": "string"
   },
   "subjectRef": {
    "type": "string",
    "nullable": true,
    "description": "What it is about — a product, an outlet, an item, a party."
   },
   "value": {
    "type": "object",
    "additionalProperties": true,
    "description": "The suggestion itself. Shape depends on `kind`."
   },
   "confidence": {
    "type": "number",
    "nullable": true,
    "minimum": 0,
    "maximum": 1,
    "description": "**Null for a heuristic and that is honest.** A rule has no confidence — dressing one up with 0.85 is the fastest way to make a manager trust a number that means nothing.\n"
   },
   "explanation": {
    "type": "string",
    "description": "**Plain words, always present, whatever the basis.** *Because covers are up 12% on this day last year* — a suggestion a manager cannot explain to their own boss is a suggestion they will not action.\n"
   },
   "inputs": {
    "type": "object",
    "additionalProperties": true,
    "description": "What went in. **Recorded so the answer can be reproduced** — and so that when a model replaces the rule, the two can be run against the same inputs and compared.\n"
   },
   "producerRef": {
    "type": "string",
    "description": "The rule name or the model id and version. **A model version is part of the record**: *the model said so* is not an answer to *which model, when*.\n"
   },
   "producedAt": {
    "type": "string",
    "format": "date-time"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "**A demand forecast for Saturday is worthless on Sunday.** An expired suggestion is hidden rather than shown stale.\n"
   }
  }
 },
 "SuggestionBasis": {
  "type": "string",
  "description": "**How the answer was reached, and this is the field the whole design exists for.**\nA venue must be able to see that today's price suggestion is a margin rule and next quarter's is a trained model — **the same operation, the same screen, a different basis** — and a screen that cannot say which is a screen that asks a manager to trust arithmetic it will not show.\n**Swapping a heuristic for a model is a provider change, not a contract change.** That is the point of the abstraction: the frontend, the audit record and the outcome capture all stay exactly as they are.\n",
  "enum": [
   "heuristic",
   "statistical",
   "model",
   "hybrid",
   "manual"
  ]
 },
 "SuggestionKind": {
  "type": "string",
  "description": "What is being suggested. **A closed set, and the reason it is closed is the swap.** Every entry here is a question a venue asks that a model could answer better than a rule — and each one starts as a heuristic and becomes a model when there is data.\n**Six of these were drawn as their own endpoints on the client F&B boards** — `suggestPrice`, `simulateScenario`, `simulateSlaPolicy`, `suggestRequisition`, `suggestReplenishment`, `publishDemandPlan`. **Building six endpoints means six places to change when a model changes**, and the model will change more often than the venue's question does.\n",
  "enum": [
   "price",
   "replenishment",
   "requisition",
   "demandForecast",
   "prepPlan",
   "menuEngineering",
   "staffing",
   "slaTarget",
   "waitTime",
   "upsell",
   "segmentation",
   "anomaly",
   "scenario"
  ]
 },
 "VenueSettings": {
  "type": "object",
  "x-ticvai-persistence": "platform.venue_settings",
  "description": "**Venue-level operational configuration that no other level can answer.**\nRegion owns currency, tax regime and fiscal year (ADR-0011). Venue owns the things that vary between two venues in one region — **opening hours, support hours, and what the local law requires of the gate.**\n",
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "supportHours": {
    "type": "object",
    "description": "CF-100. **A venue decides whether its support desk is 24/7 or bounded, and the platform does not.** This was recorded as an open question for eleven days and was never one — the code is identical either way, and what was missing was somewhere to put the answer.\n",
    "properties": {
     "mode": {
      "type": "string",
      "enum": [
       "alwaysOn",
       "businessHours",
       "custom",
       "none"
      ]
     },
     "timezone": {
      "type": "string"
     },
     "windows": {
      "type": "array",
      "items": {
       "type": "object",
       "properties": {
        "day": {
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
        },
        "from": {
         "type": "string"
        },
        "to": {
         "type": "string"
        }
       }
      }
     },
     "outOfHoursMessage": {
      "type": "string",
      "nullable": true
     }
    }
   },
   "quietHours": {
    "type": "object",
    "nullable": true,
    "description": "**When the platform does not send.** A wallet low-balance alert at 3am is a complaint, and journeys and message triggers both respect this.\n**Operational messages ignore it** — a queue-turn alert is why a guest is holding the phone.\n",
    "properties": {
     "from": {
      "type": "string"
     },
     "to": {
      "type": "string"
     }
    }
   },
   "segregatedAccess": {
    "type": "object",
    "nullable": true,
    "description": "CF-130. **Configured at venue level because it changes by region and the venue is where it is known** — a Ladies Night, a family session, a prayer-time closure.\n**The platform does not infer gender.** 3.2.45 asks for automatic gender recognition and 3.2.46 for rule-based facial recognition validation, and neither is built. Two reasons, and the second is the one that decided it:\n**A Ladies Night ticket is already gendered at the point of sale**, so the gate checks the entitlement the platform issued rather than the face in front of it — deterministic, auditable, and already contracted through `admissionRules`.\n**And these events are staffed.** A steward at the entrance is making the judgment anyway, and a classifier that overrules a person who can see more than it can is a machine and a human disagreeing while a guest waits.\n**`genderVerification` is a switch, not an implementation.** Where a venue's access hardware offers the capability and the venue chooses to use it, this turns it on — following ADR-0015's standards-first driver model, where the device does what the device does. **Not everything needs to be built.**\n",
    "properties": {
     "isEnabled": {
      "type": "boolean",
      "default": false
     },
     "appliesToAccessPointIds": {
      "type": "array",
      "items": {
       "type": "string",
       "format": "uuid"
      }
     },
     "schedule": {
      "type": "array",
      "items": {
       "type": "object",
       "properties": {
        "day": {
         "type": "string"
        },
        "from": {
         "type": "string"
        },
        "to": {
         "type": "string"
        },
        "admits": {
         "type": "string",
         "enum": [
          "all",
          "women",
          "womenAndChildren",
          "families",
          "members"
         ]
        }
       }
      }
     },
     "entitlementGated": {
      "type": "boolean",
      "default": true,
      "readOnly": true,
      "description": "**Always true, and stated rather than assumed.** The gate admits on the entitlement. Everything below is advisory on top of that, and nothing replaces it.\n"
     },
     "genderVerification": {
      "type": "string",
      "enum": [
       false,
       "staffAssisted",
       "deviceAssisted"
      ],
      "default": false,
      "description": "`off` — the entitlement decides and a steward handles exceptions. **The default, and what is contracted.**\n`staffAssisted` — the steward's screen shows the ticket type so they can ask. No inference anywhere.\n`deviceAssisted` — **the venue's access hardware performs the check, not the platform.** Available only where the driver reports the capability, and the result is **advisory to the steward rather than decisive at the turnstile** (3.2.45 asks for rejection; this deviates deliberately).\n"
     },
     "overrideRateAlertThreshold": {
      "type": "number",
      "nullable": true,
      "description": "Where `deviceAssisted` is on. **An override rate near zero means the steward has stopped deciding**, and that is the number that says whether the human safeguard is working or decorative.\n"
     }
    }
   },
   "alerting": {
    "type": "object",
    "description": "CF-134. **On-platform notification, marked as read.** Six contracts detect their own trouble and none told a person.\n**The panel is the default and email or WhatsApp only where the matrix names them** — an operational alert that arrives by email is an alert nobody sees in time.\n",
    "properties": {
     "channel": {
      "type": "string",
      "enum": [
       "dashboardPanel",
       "dashboardAndEmail",
       "dashboardAndWhatsapp"
      ],
      "default": "dashboardPanel"
     },
     "acknowledgementRequired": {
      "type": "boolean",
      "default": true
     },
     "escalateAfterMinutes": {
      "type": "integer",
      "nullable": true
     }
    }
   }
  }
 }
}
```
