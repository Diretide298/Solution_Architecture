# P08-sell-03 — P08 · Sell (3 of 4)

**10 screens · 28 operations · 48 schemas · 10 permissions**

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
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-114` | Variants, Attributes, Barcode & RFID Management | listDetail | 2 | 0 | — |
| `BO-115` | Category, Brand & Merchandise Hierarchy | listDetail | 6 | 3 | — |
| `BO-116` | Merchandising & Product Presentation | commandCentre | 7 | 4 | — |
| `BO-117` | Product Import, Governance & AI Configuration Assistant | listDetail | 6 | 4 | — |
| `BO-118` | Campaign & Audience Management | commandCentre | 6 | 3 | — |
| `BO-119` | Cross-Sell, Upsell & Recommendation Rules | statusTracker | 3 | 0 | — |
| `BO-120` | Omnichannel Commerce & Journey Configuration | listDetail | 2 | 1 | — |
| `BO-121` | Personalized Offers & Guest Engagement | listDetail | 2 | 1 | — |
| `BO-122` | POS Experience Dashboard | listDetail | 1 | 0 | — |
| `BO-1190` | Donation Campaigns | listDetail | 3 | 1 | — |

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
     "provenance": "derived — BO-102 declares entryState.params  and BO-114 holds none of them, so the edge carries nothing and BO-102 opens cold"
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
       "kind": "textField",
       "label": "Serial",
       "operation": "listSerialisedItems",
       "notes": "Sends `?serial=` to `listSerialisedItems`.",
       "provenance": "contract inventory.yaml GET /serialised-items"
      },
      {
       "kind": "textField",
       "label": "Status",
       "operation": "listSerialisedItems",
       "notes": "Sends `?status=` to `listSerialisedItems`.",
       "provenance": "contract inventory.yaml GET /serialised-items"
      },
      {
       "kind": "dataTable",
       "label": "Every serialised",
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
      },
      {
       "kind": "searchField",
       "label": "Search variants, attributes, barcode",
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
       "label": "The selected serialised",
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
       "label": "Lookup merchandise",
       "operation": "lookupMerchandise",
       "provenance": "contract retail.yaml GET /merchandise/lookup"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The variants attributes barcode list.",
   "error": "Could not load. Names which read failed and leaves the variants attributes barcode untouched.",
   "emptyFirstRun": "No variants attributes barcode yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on serial, status and the variants attributes barcode are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `PRODUCT_VIEW`, which `listSerialisedItems` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
   "derivedFrom": "wireframes/reference/Retail Board 4.dc.html",
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
     "to": "BO-102",
     "trigger": "Sell",
     "provenance": "derived — BO-102 declares entryState.params  and BO-115 holds none of them, so the edge carries nothing and BO-102 opens cold"
    },
    {
     "to": "BO-116",
     "trigger": "Merchandising & Product Presentation",
     "provenance": "flow F86 step 1→2",
     "carries": [
      "saleBoardId"
     ]
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
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every product category",
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
        "ProductCategory.description",
        "ProductCategory.isActive"
       ],
       "operation": "listProductCategories",
       "provenance": "contract catalogue.yaml GET /product-categories"
      },
      {
       "kind": "dataTable",
       "label": "Every sale board",
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
      },
      {
       "kind": "searchField",
       "label": "Search category, brand",
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
       "label": "The selected product category",
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
        "ProductCategory.description",
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
       "label": "Save product categories",
       "operation": "setProductCategories",
       "provenance": "contract catalogue.yaml PUT /product-categories"
      },
      {
       "kind": "secondaryButton",
       "label": "Request suggestion",
       "operation": "requestSuggestion",
       "provenance": "contract ai.yaml POST /ai/suggestions"
      },
      {
       "kind": "secondaryButton",
       "label": "Run report",
       "operation": "runReport",
       "provenance": "contract reporting.yaml POST /reports/{reportId}/run"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "selectField",
       "label": "Booking flow for this category",
       "bindsTo": "ProductCategory.bookingFlowId",
       "operation": "listBookingFlows",
       "notes": "**Every product filed here that names no flow of its own is sold through this one** (decided 29 September, W12). Empty means the venue's flow for each product's kind. Saved with `setProductCategories`.",
       "provenance": "decided 29 September, W12; agreed name white-label listBookingFlows (P29 brief)"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The category brand merchandise list.",
   "error": "Could not load. Names which read failed and leaves the category brand merchandise untouched.",
   "emptyFirstRun": "No category brand merchandise yet. Offers Request suggestion (`requestSuggestion`).",
   "emptyNoResults": "Never shown: `listProductCategories` takes no filter, so an empty list is always the first-run state above.",
   "emptyNoAccess": "Shown when the caller lacks `PRODUCT_VIEW`, which `listProductCategories` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listBookingFlows",
    "contract": "white-label",
    "purpose": "The booking flows a category can default to (W12)",
    "trigger": "onAction",
    "provenance": "decided 29 September, W12 (P29)"
   },
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
   "derivedFrom": "wireframes/reference/POS Board 4.dc.html",
   "source": "Claude Design POS pack, 24 August",
   "note": "**Drawn by Claude Design on `POS Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 5 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formSetProductCategories",
    "component": "modal",
    "trigger": "Save product categories",
    "body": "**Collects what `setProductCategories` sends before it is called.** Required: `categories`. Each category may carry a `description` per language: the short text under the option in the guest's \"Choose your experience\" list (decided 29 September, rev 3 REV3-19). Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save product categories",
     "operation": "setProductCategories"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "categories"
     ]
    },
    "provenance": "contract catalogue.yaml PUT /product-categories"
   },
   {
    "id": "formRequestSuggestion",
    "component": "modal",
    "trigger": "Request suggestion",
    "body": "**Collects what `requestSuggestion` sends before it is called.** Required: `kind`. Optional: `subjectRef`, `horizon`, `context`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Request suggestion",
     "operation": "requestSuggestion"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "kind",
      "subjectRef",
      "horizon",
      "context"
     ]
    },
    "provenance": "contract ai.yaml POST /ai/suggestions"
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
     "to": "BO-102",
     "trigger": "Sell",
     "provenance": "derived — BO-102 declares entryState.params  and BO-116 holds none of them, so the edge carries nothing and BO-102 opens cold"
    },
    {
     "to": "BO-117",
     "trigger": "Product Import, Governance & AI Configuration Assistant",
     "provenance": "flow F86 step 2→3",
     "carries": [
      "saleBoardId"
     ]
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
      },
      {
       "kind": "textField",
       "label": "Outlet id",
       "operation": "listMerchandise",
       "notes": "Sends `?outletId=` to `listMerchandise`.",
       "provenance": "contract retail.yaml GET /merchandise"
      },
      {
       "kind": "textField",
       "label": "Category id",
       "operation": "listMerchandise",
       "notes": "Sends `?categoryId=` to `listMerchandise`.",
       "provenance": "contract retail.yaml GET /merchandise"
      },
      {
       "kind": "toggle",
       "label": "In stock only",
       "operation": "listMerchandise",
       "notes": "Sends `?inStockOnly=` to `listMerchandise`.",
       "provenance": "contract retail.yaml GET /merchandise"
      },
      {
       "kind": "searchField",
       "label": "Search",
       "operation": "listMerchandise",
       "notes": "Sends `?search=` to `listMerchandise`.",
       "provenance": "contract retail.yaml GET /merchandise"
      },
      {
       "kind": "dataTable",
       "label": "Every merchandise",
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
      },
      {
       "kind": "searchField",
       "label": "Search merchandising",
       "provenance": "carried from the previous definition"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save merchandise",
       "operation": "updateMerchandise",
       "provenance": "contract retail.yaml PATCH /merchandise/{merchandiseId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Save role permissions",
       "operation": "setRolePermissions",
       "provenance": "contract tenancy.yaml PUT /roles/{roleId}/permissions"
      },
      {
       "kind": "secondaryButton",
       "label": "Save venue settings",
       "operation": "setVenueSettings",
       "provenance": "contract tenancy.yaml PUT /venues/{venueId}/settings"
      },
      {
       "kind": "secondaryButton",
       "label": "Save sale board",
       "operation": "updateSaleBoard",
       "provenance": "contract tenancy.yaml PUT /sale-boards/{saleBoardId}"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The merchandising product presentation figures; each tile loads on its own.",
   "error": "Could not load. Names which read failed and leaves the merchandising product presentation untouched.",
   "emptyFirstRun": "No merchandising product presentation yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on outletId, categoryId, inStockOnly, search and the merchandising product presentation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `PRODUCT_VIEW`, which `listMerchandise` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
   "derivedFrom": "wireframes/reference/POS Board 4.dc.html",
   "source": "Claude Design POS pack, 24 August",
   "note": "**Drawn by Claude Design on `POS Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 7 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formUpdateMerchandise",
    "component": "modal",
    "trigger": "Save merchandise",
    "body": "**Collects what `updateMerchandise` sends before it is called.** Nothing in the body is required. Optional: `name`, `description`, `barcode`, `categoryId`, `inventoryItemId`, `imageAssetRef`, `isReturnable`, `returnWindowDays`, `requiresSerialNumber`, `isActive`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save merchandise",
     "operation": "updateMerchandise"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "name",
      "description",
      "barcode",
      "categoryId",
      "inventoryItemId",
      "imageAssetRef",
      "isReturnable",
      "returnWindowDays",
      "requiresSerialNumber",
      "isActive"
     ]
    },
    "provenance": "contract retail.yaml PATCH /merchandise/{merchandiseId}"
   },
   {
    "id": "formSetRolePermissions",
    "component": "modal",
    "trigger": "Save role permissions",
    "body": "**Collects what `setRolePermissions` sends before it is called.** Required: `permissions`. Optional: `inheritsFromRoleId`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save role permissions",
     "operation": "setRolePermissions"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "permissions",
      "inheritsFromRoleId"
     ]
    },
    "provenance": "contract tenancy.yaml PUT /roles/{roleId}/permissions"
   },
   {
    "id": "formSetVenueSettings",
    "component": "modal",
    "trigger": "Save venue settings",
    "body": "**Collects what `setVenueSettings` sends before it is called.** Nothing in the body is required. Optional: `id`, `venueId`, `currencyCode`, `currencyScale`, `supportHours`, `quietHours`, `biometrics`, `segregatedAccess`, `alerting`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "VenueSettings",
    "confirm": {
     "label": "Save venue settings",
     "operation": "setVenueSettings"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "venueId",
      "currencyCode",
      "currencyScale",
      "supportHours",
      "quietHours",
      "biometrics",
      "segregatedAccess",
      "alerting"
     ]
    },
    "provenance": "contract tenancy.yaml PUT /venues/{venueId}/settings"
   },
   {
    "id": "formUpdateSaleBoard",
    "component": "modal",
    "trigger": "Save sale board",
    "body": "**Collects what `updateSaleBoard` sends before it is called.** Required: `id`, `code`, `name`, `venueId`, `kind`, `pages`. Optional: `isActive`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "SaleBoard",
    "confirm": {
     "label": "Save sale board",
     "operation": "updateSaleBoard"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "code",
      "name",
      "venueId",
      "kind",
      "pages",
      "isActive"
     ]
    },
    "provenance": "contract tenancy.yaml PUT /sale-boards/{saleBoardId}"
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
     "to": "BO-102",
     "trigger": "Sell",
     "provenance": "derived — BO-102 declares entryState.params  and BO-117 holds none of them, so the edge carries nothing and BO-102 opens cold"
    },
    {
     "to": "BO-118",
     "trigger": "Campaign & Audience Management",
     "provenance": "flow F86 step 3→4",
     "carries": [
      "saleBoardId"
     ]
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
       "kind": "textField",
       "label": "Venue id",
       "operation": "listSaleBoards",
       "notes": "Sends `?venueId=` to `listSaleBoards`.",
       "provenance": "contract tenancy.yaml GET /sale-boards"
      },
      {
       "kind": "textField",
       "label": "Kind",
       "operation": "listSaleBoards",
       "notes": "Sends `?kind=` to `listSaleBoards`.",
       "provenance": "contract tenancy.yaml GET /sale-boards"
      },
      {
       "kind": "dataTable",
       "label": "Every sale board",
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
      },
      {
       "kind": "searchField",
       "label": "Search product import, governance",
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
       "label": "The selected sale board",
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
       "label": "Import product catalogue",
       "operation": "importProductCatalogue",
       "provenance": "contract catalogue.yaml POST /products/import"
      },
      {
       "kind": "secondaryButton",
       "label": "Generate configuration",
       "operation": "generateConfiguration",
       "provenance": "contract ai.yaml POST /generate/configuration"
      },
      {
       "kind": "secondaryButton",
       "label": "Request suggestion",
       "operation": "requestSuggestion",
       "provenance": "contract ai.yaml POST /ai/suggestions"
      },
      {
       "kind": "secondaryButton",
       "label": "Save sale board",
       "operation": "updateSaleBoard",
       "provenance": "contract tenancy.yaml PUT /sale-boards/{saleBoardId}"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The product import governance list.",
   "error": "Could not load. Names which read failed and leaves the product import governance untouched.",
   "emptyFirstRun": "No product import governance yet. Offers Import product catalogue (`importProductCatalogue`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on venueId, kind and the product import governance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `SCOPE_VIEW`, which `listSaleBoards` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
   },
   {
    "operationId": "commitCatalogueImport",
    "contract": "catalogue",
    "purpose": "Apply a parsed catalogue import",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
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
    },
    {
     "name": "jobId",
     "from": "navigation"
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
   "derivedFrom": "wireframes/reference/POS Board 4.dc.html",
   "source": "Claude Design POS pack, 24 August",
   "note": "**Drawn by Claude Design on `POS Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 5 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formImportProductCatalogue",
    "component": "modal",
    "trigger": "Import product catalogue",
    "body": "**Collects what `importProductCatalogue` sends before it is called.** Required: `format`, `sourceRef`. Optional: `mode`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Import product catalogue",
     "operation": "importProductCatalogue"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "format",
      "sourceRef",
      "mode"
     ]
    },
    "provenance": "contract catalogue.yaml POST /products/import"
   },
   {
    "id": "formGenerateConfiguration",
    "component": "modal",
    "trigger": "Generate configuration",
    "body": "**Collects what `generateConfiguration` sends before it is called.** Required: `kind`, `description`. Optional: `conversationId`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Generate configuration",
     "operation": "generateConfiguration"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "kind",
      "description",
      "conversationId"
     ]
    },
    "provenance": "contract ai.yaml POST /generate/configuration"
   },
   {
    "id": "formRequestSuggestion",
    "component": "modal",
    "trigger": "Request suggestion",
    "body": "**Collects what `requestSuggestion` sends before it is called.** Required: `kind`. Optional: `subjectRef`, `horizon`, `context`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Request suggestion",
     "operation": "requestSuggestion"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "kind",
      "subjectRef",
      "horizon",
      "context"
     ]
    },
    "provenance": "contract ai.yaml POST /ai/suggestions"
   },
   {
    "id": "formUpdateSaleBoard",
    "component": "modal",
    "trigger": "Save sale board",
    "body": "**Collects what `updateSaleBoard` sends before it is called.** Required: `id`, `code`, `name`, `venueId`, `kind`, `pages`. Optional: `isActive`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "SaleBoard",
    "confirm": {
     "label": "Save sale board",
     "operation": "updateSaleBoard"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "code",
      "name",
      "venueId",
      "kind",
      "pages",
      "isActive"
     ]
    },
    "provenance": "contract tenancy.yaml PUT /sale-boards/{saleBoardId}"
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
     "to": "BO-102",
     "trigger": "Sell",
     "provenance": "derived — BO-102 declares entryState.params  and BO-118 holds none of them, so the edge carries nothing and BO-102 opens cold"
    },
    {
     "to": "BO-126",
     "trigger": "Deployment, Preview & Audit",
     "provenance": "flow F86 step 4→5",
     "operation": "createCampaign",
     "carries": [
      "reportId",
      "saleBoardId"
     ]
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
      },
      {
       "kind": "textField",
       "label": "Status",
       "operation": "listCampaigns",
       "notes": "Sends `?status=` to `listCampaigns`.",
       "provenance": "contract marketing-crm.yaml GET /campaigns"
      },
      {
       "kind": "dataTable",
       "label": "Every campaign",
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
      },
      {
       "kind": "searchField",
       "label": "Search campaign",
       "provenance": "carried from the previous definition"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create campaign",
       "operation": "createCampaign",
       "provenance": "contract marketing-crm.yaml POST /campaigns"
      },
      {
       "kind": "secondaryButton",
       "label": "Run report",
       "operation": "runReport",
       "provenance": "contract reporting.yaml POST /reports/{reportId}/run"
      },
      {
       "kind": "secondaryButton",
       "label": "Save sale board",
       "operation": "updateSaleBoard",
       "provenance": "contract tenancy.yaml PUT /sale-boards/{saleBoardId}"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The campaign audience figures; each tile loads on its own.",
   "error": "Could not load. Names which read failed and leaves the campaign audience untouched.",
   "emptyFirstRun": "No campaign audience yet. Offers Create campaign (`createCampaign`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on status and the campaign audience are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `MARKETING_VIEW`, which `listCampaigns` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
   "derivedFrom": "wireframes/reference/POS Board 4.dc.html",
   "source": "Claude Design POS pack, 24 August",
   "note": "**Drawn by Claude Design on `POS Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 6 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formCreateCampaign",
    "component": "modal",
    "trigger": "Create campaign",
    "body": "**Collects what `createCampaign` sends before it is called.** Required: `name`, `kind`, `channel`, `segmentId`, `content`. Optional: `venueId`, `trigger`, `scheduledFor`, `consentPurpose`, `sendWindow`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateCampaignRequest",
    "confirm": {
     "label": "Create campaign",
     "operation": "createCampaign"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "name",
      "kind",
      "channel",
      "segmentId",
      "content",
      "venueId",
      "trigger",
      "scheduledFor",
      "consentPurpose",
      "sendWindow"
     ]
    },
    "provenance": "contract marketing-crm.yaml POST /campaigns"
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
    "id": "formUpdateSaleBoard",
    "component": "modal",
    "trigger": "Save sale board",
    "body": "**Collects what `updateSaleBoard` sends before it is called.** Required: `id`, `code`, `name`, `venueId`, `kind`, `pages`. Optional: `isActive`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "SaleBoard",
    "confirm": {
     "label": "Save sale board",
     "operation": "updateSaleBoard"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "code",
      "name",
      "venueId",
      "kind",
      "pages",
      "isActive"
     ]
    },
    "provenance": "contract tenancy.yaml PUT /sale-boards/{saleBoardId}"
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
     "provenance": "derived — BO-102 declares entryState.params  and BO-119 holds none of them, so the edge carries nothing and BO-102 opens cold"
    }
   ]
  },
  "notes": "**Added 20 August from the client design board.** The operations existed and no screen called them. **Named in the board contents and not written up in it** — the operations are real, the layout is not. **Upsell rules are read-only here** (decided 28 September, audit R183): rules are created and deleted at region level, and this venue screen only shows what they suggest.",
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
    "why": "**`getRecommendations` declares its response inline**, so the component that shows it names fields but binds to no schema. The contract should name the shape.",
    "source": "contract promotions.yaml POST /recommendations"
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
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "getRecommendations"
      },
      {
       "kind": "dataTable",
       "label": "Recommendations",
       "operation": "getRecommendations",
       "notes": "Shows `productId`, `reason`, `confidence` from `getRecommendations`'s inline response. **The response has no named schema**, so this cannot bind until the contract names one.",
       "provenance": "contract promotions.yaml POST /recommendations"
      },
      {
       "kind": "detailPanel",
       "label": "The upsell suggestion",
       "bindsTo": "UpsellSuggestion",
       "columns": [
        "UpsellSuggestion.variantId",
        "UpsellSuggestion.bundleId",
        "UpsellSuggestion.name",
        "UpsellSuggestion.price",
        "UpsellSuggestion.discountedPrice",
        "UpsellSuggestion.source",
        "UpsellSuggestion.ruleId",
        "UpsellSuggestion.rank",
        "UpsellSuggestion.rationale"
       ],
       "operation": "getUpsellSuggestions",
       "provenance": "contract promotions.yaml POST /upsell-suggestions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The cross-sell upsell recommendation, read by `getUpsellSuggestions`.",
   "error": "Could not load. Names which read failed and leaves the cross-sell upsell recommendation untouched.",
   "emptyFirstRun": "No cross-sell upsell recommendation yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoAccess": "Shown when the caller lacks `PRODUCT_VIEW`, which `getRecommendations` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createUpsellRule",
    "contract": "promotions",
    "purpose": "Create an upsell rule",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   },
   {
    "operationId": "deleteUpsellRule",
    "contract": "promotions",
    "purpose": "Remove an upsell rule",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   },
   {
    "operationId": "decideRecommendations",
    "contract": "ai",
    "purpose": "Fill a recommendation slot",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "venueId",
     "from": "session"
    },
    {
     "name": "ruleId",
     "from": "navigation"
    }
   ],
   "coldEntry": "Resolves from the session. A principal with more than one venue is asked which before the page renders."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-119",
   "derivedFrom": "wireframes/reference/Retail Board 5.dc.html",
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
     "provenance": "derived — BO-102 declares entryState.params  and BO-120 holds none of them, so the edge carries nothing and BO-102 opens cold"
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
       "label": "Every journey",
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
      },
      {
       "kind": "searchField",
       "label": "Search omnichannel commerce",
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
       "label": "The selected journey",
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
       "label": "Create journey",
       "operation": "createJourney",
       "provenance": "contract marketing-crm.yaml POST /journeys"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The omnichannel commerce journey list.",
   "error": "Could not load. Names which read failed and leaves the omnichannel commerce journey untouched.",
   "emptyFirstRun": "No omnichannel commerce journey yet. Offers Create journey (`createJourney`).",
   "emptyNoResults": "Never shown: `listJourneys` takes no filter, so an empty list is always the first-run state above.",
   "emptyNoAccess": "Shown when the caller lacks `MARKETING_VIEW`, which `listJourneys` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
   "derivedFrom": "wireframes/reference/Retail Board 5.dc.html",
   "note": "**Drawn by Claude Design on `Retail Board 5.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formCreateJourney",
    "component": "modal",
    "trigger": "Create journey",
    "body": "**Collects what `createJourney` sends before it is called.** Required: `id`, `name`, `entryEvent`, `steps`, `status`. Optional: `templateKind`, `entryConditions`, `maxDurationDays`, `reentryPolicy`, `scopePath`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "Journey",
    "confirm": {
     "label": "Create journey",
     "operation": "createJourney"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "name",
      "entryEvent",
      "steps",
      "status",
      "templateKind",
      "entryConditions",
      "maxDurationDays",
      "reentryPolicy",
      "scopePath"
     ]
    },
    "provenance": "contract marketing-crm.yaml POST /journeys"
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
     "provenance": "derived — BO-102 declares entryState.params  and BO-121 holds none of them, so the edge carries nothing and BO-102 opens cold"
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
       "kind": "searchField",
       "label": "Search",
       "operation": "listSegments",
       "notes": "Sends `?search=` to `listSegments`.",
       "provenance": "contract marketing-crm.yaml GET /segments"
      },
      {
       "kind": "dataTable",
       "label": "Every segment",
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
      },
      {
       "kind": "searchField",
       "label": "Search personalized offers",
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
       "label": "The selected segment",
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
       "label": "Create campaign",
       "operation": "createCampaign",
       "provenance": "contract marketing-crm.yaml POST /campaigns"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The personalized offers guest list.",
   "error": "Could not load. Names which read failed and leaves the personalized offers guest untouched.",
   "emptyFirstRun": "No personalized offers guest yet. Offers Create campaign (`createCampaign`); distinct from a filter that matched nothing.",
   "emptyNoResults": "Nothing matches the filter on search and the personalized offers guest are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `MARKETING_VIEW`, which `listSegments` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
   "derivedFrom": "wireframes/reference/Retail Board 5.dc.html",
   "source": "Claude Design Retail pack, 24 August",
   "note": "**Drawn by Claude Design on `Retail Board 5.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "overlays": [
   {
    "id": "formCreateCampaign",
    "component": "modal",
    "trigger": "Create campaign",
    "body": "**Collects what `createCampaign` sends before it is called.** Required: `name`, `kind`, `channel`, `segmentId`, `content`. Optional: `venueId`, `trigger`, `scheduledFor`, `consentPurpose`, `sendWindow`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CreateCampaignRequest",
    "confirm": {
     "label": "Create campaign",
     "operation": "createCampaign"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "name",
      "kind",
      "channel",
      "segmentId",
      "content",
      "venueId",
      "trigger",
      "scheduledFor",
      "consentPurpose",
      "sendWindow"
     ]
    },
    "provenance": "contract marketing-crm.yaml POST /campaigns"
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
     "provenance": "derived — BO-102 declares entryState.params  and BO-122 holds none of them, so the edge carries nothing and BO-102 opens cold"
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
       "kind": "textField",
       "label": "Venue id",
       "operation": "listSaleBoards",
       "notes": "Sends `?venueId=` to `listSaleBoards`.",
       "provenance": "contract tenancy.yaml GET /sale-boards"
      },
      {
       "kind": "textField",
       "label": "Kind",
       "operation": "listSaleBoards",
       "notes": "Sends `?kind=` to `listSaleBoards`.",
       "provenance": "contract tenancy.yaml GET /sale-boards"
      },
      {
       "kind": "dataTable",
       "label": "Every sale board",
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
      },
      {
       "kind": "searchField",
       "label": "Search pos experience dashboard",
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
       "label": "The selected sale board",
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
    }
   ]
  },
  "states": {
   "loading": "The pos experience list.",
   "error": "Could not load. Names which read failed and leaves the pos experience untouched.",
   "emptyFirstRun": "No pos experience yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on venueId, kind and the pos experience are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `SCOPE_VIEW`, which `listSaleBoards` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
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
   "derivedFrom": "wireframes/reference/Retail Board 5.dc.html",
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
  "id": "BO-1190",
  "name": "Donation Campaigns",
  "module": "Sell",
  "requiresModule": "ticketing",
  "wave": 2,
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/donation-campaigns",
   "component": "apps/venue-management-web/src/routes/sell/DonationCampaigns.tsx",
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
   "notes": "Reached from BO-102 Sell. New 29 September (VM close-out): donations are a configuration area with operations and no screen.",
   "transitions": [
    {
     "to": "BO-102",
     "trigger": "Sell",
     "provenance": "decided 29 September, VM close-out (venue management and configuration)"
    }
   ]
  },
  "notes": "**Created 29 September (VM close-out)** because `listDonationCampaigns`, `createDonationCampaign` and `updateDonationCampaign` had no screen (matrix 1.1.128-1.1.133). **The amounts are configuration, not code**: fixed choices, a free amount or round-up. **Donations post to a liability account, not revenue** (1.1.132), so the liability account is required before a campaign goes live.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listDonationCampaigns` reads the population and the panel edits one of them — list, select, act",
  "purpose": "Create, run and close the donation campaigns guests can give to at checkout.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "filters",
     "slot": "filters",
     "components": [
      {
       "kind": "toggle",
       "label": "Active only",
       "notes": "Filters the loaded list on `isActive`.",
       "provenance": "our build plan"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every donation campaign",
       "bindsTo": "DonationCampaign",
       "columns": [
        "DonationCampaign.name",
        "DonationCampaign.beneficiary",
        "DonationCampaign.amountMode",
        "DonationCampaign.channels",
        "DonationCampaign.validFrom",
        "DonationCampaign.validTo",
        "DonationCampaign.isActive",
        "DonationCampaign.raisedTotal"
       ],
       "operation": "listDonationCampaigns",
       "provenance": "contract catalogue.yaml GET /donation-campaigns"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected campaign",
       "bindsTo": "DonationCampaign",
       "columns": [
        "DonationCampaign.name",
        "DonationCampaign.description",
        "DonationCampaign.beneficiary",
        "DonationCampaign.venueIds",
        "DonationCampaign.amountMode",
        "DonationCampaign.fixedAmounts",
        "DonationCampaign.minAmount",
        "DonationCampaign.maxAmount",
        "DonationCampaign.liabilityAccountId",
        "DonationCampaign.channels",
        "DonationCampaign.validFrom",
        "DonationCampaign.validTo",
        "DonationCampaign.isActive",
        "DonationCampaign.raisedTotal"
       ],
       "operation": "listDonationCampaigns",
       "provenance": "contract catalogue.yaml GET /donation-campaigns"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "New campaign",
       "operation": "createDonationCampaign",
       "provenance": "contract catalogue.yaml POST /donation-campaigns"
      },
      {
       "kind": "secondaryButton",
       "label": "Save campaign",
       "operation": "updateDonationCampaign",
       "provenance": "contract catalogue.yaml PATCH /donation-campaigns/{campaignId}"
      },
      {
       "kind": "destructiveButton",
       "label": "Close campaign",
       "operation": "updateDonationCampaign",
       "notes": "Sends `isActive` false. **Closing does not reverse donations already given**; the raised total is still owed to the beneficiary.",
       "provenance": "contract catalogue.yaml PATCH /donation-campaigns/{campaignId}"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The tenant's donation campaigns, read by `listDonationCampaigns`.",
   "error": "Could not load. Names which read failed and leaves the campaigns untouched.",
   "emptyFirstRun": "No donation campaigns yet. Offers New campaign; checkout shows no donation prompt until one is active.",
   "emptyNoResults": "The Active only filter matched nothing and the closed campaigns are still there. Offers to clear it.",
   "emptyNoAccess": "Names the missing permission (`PRODUCT_VIEW` to see, `PRODUCT_CONFIGURE` to change). **Never an empty table.**",
   "validation": "`400` on a missing name or amount mode, fixed amounts missing when the mode is fixed choices, or a minimum above the maximum; marked on the field. A campaign without a liability account cannot be activated."
  },
  "apis": [
   {
    "operationId": "listDonationCampaigns",
    "contract": "catalogue",
    "purpose": "Every campaign with what it has raised",
    "trigger": "onLoad",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   },
   {
    "operationId": "createDonationCampaign",
    "contract": "catalogue",
    "purpose": "Create a campaign with its amounts, channels and liability account",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listDonationCampaigns"
    ]
   },
   {
    "operationId": "updateDonationCampaign",
    "contract": "catalogue",
    "purpose": "Amend or close a campaign",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "listDonationCampaigns"
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
     "from": "navigation"
    }
   ],
   "coldEntry": "Resolves the tenant and venue from the session; a cold arrival is the ordinary case."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-1190"
  },
  "overlays": [
   {
    "id": "formCreateDonationCampaign",
    "component": "modal",
    "trigger": "New campaign",
    "body": "**Collects what `createDonationCampaign` sends.** Required: `name`, `amountMode`, `isActive`. With fixed choices, `fixedAmounts`; with a free amount, `minAmount` and `maxAmount`; always the `liabilityAccountId` before activation. Optional: `description`, `beneficiary`, `venueIds`, `channels`, `validFrom`, `validTo`.",
    "bindsTo": "DonationCampaign",
    "confirm": {
     "label": "Create campaign",
     "operation": "createDonationCampaign"
    },
    "dismiss": {
     "label": "Cancel"
    },
    "provenance": "contract catalogue.yaml POST /donation-campaigns"
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
 "commitCatalogueImport": {
  "method": "POST",
  "path": "/products/import/{jobId}/commit",
  "contract": "catalogue",
  "summary": "Apply a parsed catalogue import",
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
  "responds": "CatalogueImportJob"
 },
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
 "createDonationCampaign": {
  "method": "POST",
  "path": "/donation-campaigns",
  "contract": "catalogue",
  "summary": "Create a campaign",
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
  "requestBody": "DonationCampaign",
  "responds": "DonationCampaign"
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
 "createUpsellRule": {
  "method": "POST",
  "path": "/upsell-rules",
  "contract": "promotions",
  "summary": "Create an upsell rule",
  "permission": "PRODUCT_CONFIGURE",
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
  "requestBody": "UpsellRule",
  "responds": "UpsellRule"
 },
 "decideRecommendations": {
  "method": "POST",
  "path": "/recommendations/decide",
  "contract": "ai",
  "summary": "Fill a recommendation slot",
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
  "responds": "AiRecommendationResult"
 },
 "deleteUpsellRule": {
  "method": "DELETE",
  "path": "/upsell-rules/{ruleId}",
  "contract": "promotions",
  "summary": "Remove an upsell rule",
  "permission": "PRODUCT_CONFIGURE",
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
 "listBookingFlows": {
  "method": "GET",
  "path": "/venues/{venueId}/booking-flows",
  "contract": "white-label",
  "summary": "A venue's booking flows, in the working draft",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "flowTypeKey",
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
 "listDonationCampaigns": {
  "method": "GET",
  "path": "/donation-campaigns",
  "contract": "catalogue",
  "summary": "Campaigns a guest can give to",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "DonationCampaign"
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
  "responds": "ProductCategoryNode"
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
  "responds": "Page"
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
   },
   {
    "name": "outletId",
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
 "updateDonationCampaign": {
  "method": "PATCH",
  "path": "/donation-campaigns/{campaignId}",
  "contract": "catalogue",
  "summary": "Amend or close a campaign",
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
  "requestBody": "DonationCampaign",
  "responds": "DonationCampaign"
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
 "AiMaturity": {
  "type": "object",
  "x-ticvai-persistence": "none — embedded as jsonb on ai.suggestion and ai.forecast_version",
  "description": "**Where an answer stands, on every answer** (29 September, AI functions review; baseline then learn). The customer sees a stage badge and a \"Based on\" chip, never a bare percentage (design 5.6), and \"Limited historical data\" while the starting pattern carries more than half the weight.",
  "required": [
   "stage",
   "basedOn"
  ],
  "properties": {
   "stage": {
    "type": "string",
    "enum": [
     "starting",
     "learning",
     "established",
     "learned"
    ],
    "description": "`starting`: the baseline (venue AI settings, the starting pattern for the venue type, the UAE calendar, weather). `learning`: own data carries short-range patterns (about 4 weeks). `established`: own level and trend lead, the baseline fills gaps such as a holiday not yet seen (about 3 months, or at once with 12+ months imported). `learned`: a model trained on this tenant's data, promoted by an admin (AI-D16)."
   },
   "basedOn": {
    "type": "string",
    "description": "The \"Based on\" line, in words, e.g. *Based on: your venue profile, UAE calendar, weather, 23 days of your sales*. Always present."
   },
   "sources": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "source"
     ],
     "properties": {
      "source": {
       "type": "string",
       "enum": [
        "venueSettings",
        "startingPattern",
        "calendar",
        "weather",
        "bookingsOnHand",
        "ownHistory",
        "importedHistory",
        "configuration",
        "trainedModel"
       ]
      },
      "detail": {
       "type": "string",
       "nullable": true,
       "description": "e.g. *23 days*, *water park pattern v3*, *Eid al-Adha 2027*."
      },
      "observations": {
       "type": "integer",
       "nullable": true
      }
     }
    }
   },
   "ownDataShare": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "description": "The weight own data carries, `n / (k + n)`. Below 0.5 the answer is marked \"Limited historical data\"."
   },
   "limitedHistory": {
    "type": "boolean"
   },
   "nextStage": {
    "type": "object",
    "nullable": true,
    "description": "What the next stage needs, e.g. *8 more Saturdays of sales*, or *an admin promotion*.",
    "properties": {
     "stage": {
      "type": "string",
      "enum": [
       "learning",
       "established",
       "learned"
      ]
     },
     "needs": {
      "type": "string"
     },
     "expectedBy": {
      "type": "string",
      "format": "date",
      "nullable": true
     }
    }
   }
  }
 },
 "AiRecommendationItem": {
  "type": "object",
  "x-ticvai-persistence": "none — held in jsonb on ai.rec_decision.items, through AiRecommendationItemList",
  "description": "One recommended item. **Carries a Pricing price reference, never a computed price** (AIR-029).",
  "required": [
   "trackingId",
   "rank"
  ],
  "properties": {
   "trackingId": {
    "type": "string",
    "format": "uuid",
    "description": "Echoed on every `recordRecommendationEvents` event and as `orders.addCartLine.recommendationId`, so attribution never guesses."
   },
   "productId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The product recommended. **Exactly one of `productId`, `promotionId` or `couponRef`, `rewardId` or `challengeId` is set, by `kind`** (29 September, build): `offer` carries a promotion or coupon, `reward` a loyalty reward, `challenge` a challenge, every other kind a product."
   },
   "promotionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "For `offer`, a published promotion the guest is eligible for. Promotions computes the discount at the basket, never the engine."
   },
   "couponRef": {
    "type": "string",
    "nullable": true,
    "description": "For `offer`, a coupon campaign; a code is assigned only when the guest takes it (`promotions.assignCoupon`)."
   },
   "rewardId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "For `reward`, a marketing-crm loyalty reward the guest can redeem."
   },
   "challengeId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "For `challenge`, a marketing-crm challenge the guest can join."
   },
   "kind": {
    "type": "string",
    "enum": [
     "upsell",
     "crossSell",
     "upgrade",
     "bundle",
     "addOn",
     "membership",
     "nextBestOffer",
     "offer",
     "reward",
     "challenge"
    ]
   },
   "rank": {
    "type": "integer",
    "minimum": 1
   },
   "priceRef": {
    "type": "string",
    "nullable": true,
    "description": "The Pricing reference the channel resolves to a price. AI never computes a price."
   },
   "reasonTemplateKey": {
    "type": "string",
    "nullable": true,
    "description": "The template reason (decided 29 September, decision 9): no model writes guest-visible reasons."
   },
   "reasonText": {
    "type": "string",
    "nullable": true,
    "description": "The rendered template in the session locale, where the channel shows reasons."
   },
   "confidenceBand": {
    "type": "string",
    "enum": [
     "high",
     "medium",
     "low"
    ],
    "description": "Design 5.6: a band, never a bare percentage."
   },
   "score": {
    "type": "number",
    "nullable": true,
    "description": "Normalised score. **Returned to staff callers only**; a guest response omits it."
   }
  }
 },
 "AiRecommendationResult": {
  "type": "object",
  "x-ticvai-persistence": "none — written as ai.rec_decision after the response",
  "description": "The recommendation slot's content (design 2.2 A). Empty `items` is a valid answer: the slot stays empty.",
  "required": [
   "decisionId",
   "mode",
   "items",
   "expiresAt"
  ],
  "properties": {
   "decisionId": {
    "type": "string",
    "format": "uuid"
   },
   "placement": {
    "type": "string",
    "enum": [
     "productPage",
     "cart",
     "checkout",
     "postPurchase",
     "preVisit",
     "inVenue",
     "posBasket",
     "kioskBasket",
     "fnbMenu",
     "retailBasket",
     "seatUpgrade",
     "membership",
     "email",
     "homepage",
     "loyalty"
    ]
   },
   "mode": {
    "type": "string",
    "enum": [
     "personalised",
     "contextual",
     "rulesOnly",
     "fallback"
    ]
   },
   "items": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/AiRecommendationItem"
    }
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "BookingFlow": {
  "x-ticvai-persistence": "whitelabel.booking_flow",
  "type": "object",
  "description": "**A venue's booking flow (decided 29 September, W12: operators pick their flows, see which steps are required, set their own order).** Made from a `BookingFlowType`; lives in the working draft and reaches guests with `publishTenantConfig`, which copies the venue's flows into the version's snapshot. A product or category names its flow (catalogue `bookingFlowId`); otherwise the venue's default for the type serving its kind applies.\n",
  "required": [
   "flowTypeKey",
   "name"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "From the path of `createBookingFlowDefinition`."
   },
   "flowTypeKey": {
    "$ref": "#/components/schemas/BookingFlowTypeKey"
   },
   "name": {
    "type": "string",
    "maxLength": 80,
    "description": "Staff-facing, e.g. \"Day pass, date first\". Not shown to guests."
   },
   "isDefaultForType": {
    "type": "boolean",
    "default": false,
    "description": "At most one per venue and type; setting it takes it from the previous default."
   },
   "isEnabled": {
    "type": "boolean",
    "default": true,
    "description": "A disabled flow is kept and not published; products naming it fall back to the default."
   },
   "steps": {
    "type": "array",
    "maxItems": 30,
    "description": "Every step of the type, in the venue's order. Filled from the type when left out on create.",
    "items": {
     "$ref": "#/components/schemas/BookingFlowStep"
    }
   },
   "settings": {
    "$ref": "#/components/schemas/BookingFlowLevelSettings"
   },
   "isValid": {
    "type": "boolean",
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "Whether the flow passes `validateBookingFlow`; worked out in the same transaction as each write. `publishTenantConfig` refuses a draft holding an invalid enabled flow."
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "The partition key (ADR-0005). Written at `venue` scope."
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "BookingFlowLevelSettings": {
  "x-ticvai-persistence": "none — jsonb column on whitelabel.booking_flow",
  "type": "object",
  "description": "**The settings that belong to one flow, not to the venue (decided 29 September, W12).** Moved here from `BookingFlowSettings`, which keeps the venue-wide ones. Each keeps its rev 3 meaning and default. A field left out takes its default.\n",
  "properties": {
   "performanceReveal": {
    "type": "string",
    "enum": [
     "dateTimeTicket",
     "allAtOnce"
    ],
    "default": "dateTimeTicket",
    "description": "**Performance reveal (rev 3 REV3-2).** `dateTimeTicket` shows the times only once a date is picked and the tickets only once a time is picked; `allAtOnce` shows them together. Product-first (W8) is the step order of `experienceWorkshop`, not a value here.\n"
   },
   "signInAt": {
    "type": "string",
    "enum": [
     "afterAddOns",
     "atPayment"
    ],
    "default": "afterAddOns",
    "description": "**Where the guest is asked to sign in, or for a guest-checkout code (rev 3 REV3-3).** `afterAddOns` asks as the guest leaves the extras step; `atPayment` asks at payment. The basket is kept either way.\n"
   },
   "seatEventDateMode": {
    "type": "string",
    "enum": [
     "inlineStep",
     "popupOnSeatMap"
    ],
    "default": "inlineStep",
    "description": "**Date and time on a seated event (rev 3 REV3-4).** `inlineStep` asks for them before the seat map; `popupOnSeatMap` opens the seat map with a date and time pop-up. Read only by the seated flow types.\n"
   },
   "extrasStep": {
    "type": "string",
    "enum": [
     "auto",
     "always",
     "never"
    ],
    "default": "auto",
    "description": "`auto` shows the extras step only when the cart's products have add-ons; `never` is the same as turning the optional `extras` step off."
   },
   "quickTour": {
    "type": "boolean",
    "default": false,
    "description": "**Quick tour (rev 3 REV3-20).** A first visit gets a coach-mark tour of this flow's steps, replayable from a Quick tour button. Seen-state kept on the device only.\n"
   },
   "consentQuestionIds": {
    "type": "array",
    "maxItems": 10,
    "uniqueItems": true,
    "default": [],
    "description": "**The flow's own consent questions (rev 3 REV3-26).** Asked on every booking through this flow, together with those of each product in the cart, each question once. Each id names an active `ConsentQuestion` of the tenant in marketing-crm, or 400. A Help me choose answer may pre-fill one (`GuidedChoice` `consentPrefill`); the guest still confirms it.\n",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   }
  }
 },
 "BookingFlowStep": {
  "x-ticvai-persistence": "whitelabel.booking_flow_step",
  "type": "object",
  "description": "One step of a venue's flow, in the venue's order (decided 29 September, W12).",
  "required": [
   "stepKey",
   "enabled",
   "sortOrder"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "bookingFlowId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "stepKey": {
    "$ref": "#/components/schemas/BookingFlowStepKey"
   },
   "enabled": {
    "type": "boolean",
    "description": "A `required` step cannot be off; the flow saves and `isValid` turns false."
   },
   "sortOrder": {
    "type": "integer",
    "minimum": 0
   },
   "requirement": {
    "type": "string",
    "enum": [
     "required",
     "optional",
     "conditional"
    ],
    "readOnly": true,
    "x-ticvai-derived": "onRead",
    "description": "From the flow type, so the CMS can mark the step without a second read."
   },
   "settings": {
    "type": "object",
    "additionalProperties": true,
    "default": {},
    "description": "The step's own settings, by the names the type's `stepSettings` gives for this step (e.g. `languages` on `language`, `minHours` on `duration`). A name the type does not give is refused with 400."
   }
  }
 },
 "BookingFlowTypeKey": {
  "type": "string",
  "description": "**The flow types the system catalogue offers (decided 29 September, W12; impact.md b).** `seatedFixedPerformance` and `seatedDateTimeSeatMap` are the two seated flows; `cabanaMap` and `cabanaBySize` are the two cabana flows (W6); `experienceWorkshop` puts the product before the date (W8); `multiLocation` opens on the location switcher.\n",
  "enum": [
   "datedDayPass",
   "timedEntry",
   "openDated",
   "seatedFixedPerformance",
   "seatedDateTimeSeatMap",
   "experienceWorkshop",
   "surfSession",
   "meetingRoomHourly",
   "cabanaMap",
   "cabanaBySize",
   "guidedTourByLanguage",
   "transport",
   "tableReservation",
   "membership",
   "giftCard",
   "multiLocation"
  ]
 },
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
     },
     "sentCount": {
      "type": "integer",
      "readOnly": true,
      "x-ticvai-persisted": false,
      "description": "**How many messages went out**, counted from `marketing.message_dispatch` at read time rather than kept as a counter on the campaign row, so it cannot drift from the dispatch records it summarises. Test sends are not dispatches of the campaign and are not counted.\n"
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
    "description": "Fallback values for the template's `mergeFields`, by name, used where a guest has no value.",
    "additionalProperties": {
     "type": "string"
    }
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
     "inactivity",
     "entitlementExpiring"
    ],
    "description": "`entitlementExpiring` (29 September, build pass, group G2; 5.5.30) fires on `entitlement.expiringSoon`: a ticket or pass the guest still holds comes within its template's `expiryNoticeDays` of `validTo`. The notice period is set on the template, so `delayHours` shifts the send within it rather than setting it. An entitlement belonging to a membership is left to `membershipExpiring`, so a member is not told twice."
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
 "CatalogueImportJob": {
  "type": "object",
  "x-ticvai-persistence": "catalogue.import_job",
  "description": "1.4.2. **Two-phase, following `seating.ImportJob`** — and carrying the same lesson: a job that parses zero products is not a parsed job.\n",
  "required": [
   "id",
   "status",
   "parsedCount"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "status": {
    "type": "string",
    "enum": [
     "parsing",
     "previewReady",
     "committing",
     "committed",
     "failed"
    ]
   },
   "outcome": {
    "type": "string",
    "enum": [
     "parsed",
     "parsedWithFindings",
     "nothingFound",
     "unreadable"
    ]
   },
   "parsedCount": {
    "type": "integer"
   },
   "createCount": {
    "type": "integer"
   },
   "updateCount": {
    "type": "integer"
   },
   "findings": {
    "type": "array",
    "description": "**What an operator sees before committing** — missing prices, duplicate codes, unknown categories, codes that do not match the tenant's schema.\n",
    "items": {
     "type": "object",
     "properties": {
      "row": {
       "type": "integer"
      },
      "severity": {
       "type": "string",
       "enum": [
        "error",
        "warning"
       ]
      },
      "message": {
       "type": "string"
      }
     }
    }
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"
   },
   "jobKind": {
    "type": "string",
    "enum": [
     "productImport",
     "environmentTransfer",
     "pricingBulkUpdate",
     "pricingImport"
    ],
    "default": "productImport",
    "description": "**One job table for every catalogue bulk operation** (29 September, data model DM3): product import (the original use), environment transfer (ADM-124) and bulk pricing update or import (ADM-080). A pricing job never writes prices; committing it creates a change request (`changeRequestId`)."
   },
   "direction": {
    "type": "string",
    "enum": [
     "export",
     "import",
     null
    ],
    "nullable": true
   },
   "sourceEnvironment": {
    "type": "string",
    "enum": [
     "development",
     "sandbox",
     "uat",
     "staging",
     "production",
     null
    ],
    "nullable": true
   },
   "targetEnvironment": {
    "type": "string",
    "enum": [
     "development",
     "sandbox",
     "uat",
     "staging",
     "production",
     null
    ],
    "nullable": true
   },
   "productIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "components": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Transfer components, per `ProductImportExportEnvironmentTransferView.components`."
   },
   "referenceMappings": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true,
    "description": "`[{kind, sourceRef, targetRef}]`."
   },
   "missingReferences": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "fileId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "sourceFormat": {
    "type": "string",
    "maxLength": 40,
    "nullable": true
   },
   "columnMappings": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true,
    "description": "`[{sourceColumn, targetField, suggestedByAi, confirmed}]`."
   },
   "parameters": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true,
    "description": "Bulk pricing: `{selectBy, selectionValues, operation, adjustmentPercent, adjustmentAmount, targetCurrency, effectivePeriodFrom, effectivePeriodTo}`."
   },
   "warningCount": {
    "type": "integer",
    "default": 0
   },
   "errorCount": {
    "type": "integer",
    "default": 0
   },
   "changeRequestId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true
   },
   "requestedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true
   },
   "createdAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "completedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   }
  }
 },
 "CatalogueState": {
  "x-ticvai-persistence": "none — computed from workstation bundle_version",
  "type": "object",
  "description": "The workstation's local catalogue position. A terminal beyond `staleAfter` must refuse to trade rather than transact against stale prices.\n",
  "required": [
   "appliedBundleVersion",
   "appliedAt",
   "staleAfter",
   "isStale"
  ],
  "properties": {
   "appliedBundleVersion": {
    "type": "string"
   },
   "appliedAt": {
    "type": "string",
    "format": "date-time"
   },
   "staleAfter": {
    "type": "string",
    "format": "date-time",
    "description": "Beyond this the terminal refuses to trade."
   },
   "isStale": {
    "type": "boolean"
   },
   "pendingBundleVersion": {
    "type": "string",
    "nullable": true,
    "description": "Published but not yet applied."
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
   },
   "sendTimeMode": {
    "type": "string",
    "enum": [
     "fixed",
     "optimised"
    ],
    "default": "fixed",
    "description": "`optimised` sends each recipient at the hour `ai.requestSuggestion` (kind `sendTime`) gives for them, inside `sendWindow` (29 September, build pass, group G2; 22.3.19). `fixed` is the behaviour before. Falls back to `scheduledFor` per recipient where there is no suggestion or AI is off."
   },
   "optimiseChannel": {
    "type": "boolean",
    "default": false,
    "description": "With `sendTimeMode` `optimised`, route each recipient to the channel the suggestion names, among the channels they consented to (22.9.16). Off keeps `channel`."
   },
   "variants": {
    "type": "array",
    "maxItems": 5,
    "nullable": true,
    "description": "**A/B (or up to five-way) content and subject variants** (29 September, build pass, group G2; 22.1.17, BO-772). Each is a subject override and optionally a different template, written by a person or taken from an AI draft (`ai.proposeMarketingContent`, `source` `aiDraft`). Held as rows of `marketing.campaign_variant`. Null or empty is a single-content campaign.",
    "items": {
     "$ref": "#/components/schemas/MarketingCampaignVariant"
    }
   },
   "abTest": {
    "type": "object",
    "nullable": true,
    "description": "How the variants are tested. Required when `variants` has two or more.",
    "properties": {
     "testPercent": {
      "type": "integer",
      "minimum": 5,
      "maximum": 100,
      "default": 20,
      "description": "Share of the audience the variants are tested on; 100 splits everyone and picks no winner."
     },
     "successMetric": {
      "type": "string",
      "enum": [
       "openRate",
       "clickRate",
       "conversionRate",
       "attributedRevenue"
      ],
      "default": "clickRate"
     },
     "decideAfterHours": {
      "type": "integer",
      "minimum": 1,
      "maximum": 168,
      "default": 4
     },
     "winnerRule": {
      "type": "string",
      "enum": [
       "automatic",
       "manual"
      ],
      "default": "automatic"
     },
     "minimumSamplePerVariant": {
      "type": "integer",
      "minimum": 1,
      "default": 500,
      "description": "Below this many sends per variant no winner is declared automatically; a person picks."
     },
     "winningVariantId": {
      "type": "string",
      "format": "uuid",
      "nullable": true,
      "description": "Set by the automatic rule, or by a person through `updateCampaign`."
     }
    }
   }
  }
 },
 "CreateSegmentRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "name",
   "criteria"
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
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "match": {
    "type": "string",
    "enum": [
     "all",
     "any"
    ],
    "default": "all"
   },
   "criteria": {
    "type": "array",
    "minItems": 1,
    "items": {
     "$ref": "#/components/schemas/SegmentCriterion"
    }
   },
   "excludeSegmentIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   }
  }
 },
 "DeploymentProfile": {
  "type": "string",
  "description": "How this workstation obtains catalogue and inventory (ADR-0013).\n- `terminalLocal` — own SQLite, leases direct from the cell. Small venues, 4G sites - `venueEdge` — own SQLite, distributed via the venue edge node which holds the\n  venue lease and sub-leases to terminals. Mid and large venues, stadium gates\n- `thin` — no local catalogue, server reads. Non-transactional surfaces only\n",
  "enum": [
   "terminalLocal",
   "venueEdge",
   "thin"
  ]
 },
 "DeviceBinding": {
  "x-ticvai-persistence": "platform.device",
  "type": "object",
  "required": [
   "kind",
   "driver"
  ],
  "properties": {
   "kind": {
    "$ref": "#/components/schemas/DeviceKind"
   },
   "driver": {
    "type": "string",
    "description": "Driver identifier. Adding a vendor is a driver plus configuration, never a core change — every venue arrives with hardware not previously seen.\n"
   },
   "identifier": {
    "type": "string",
    "description": "Serial",
    "port or network address.": null
   },
   "isRequired": {
    "type": "boolean",
    "default": false,
    "description": "When true, the workstation refuses to open a shift if the device is absent.\n"
   }
  }
 },
 "DonationAmountMode": {
  "type": "string",
  "enum": [
   "fixedChoices",
   "freeAmount",
   "roundUp"
  ]
 },
 "DonationCampaign": {
  "type": "object",
  "x-ticvai-persistence": "catalogue.donation_campaign",
  "required": [
   "name",
   "amountMode",
   "isActive"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "description": {
    "type": "string",
    "maxLength": 1000
   },
   "beneficiary": {
    "type": "string",
    "description": "Who the money is for. Shown to the guest, and it is the reason they give."
   },
   "venueIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "amountMode": {
    "$ref": "#/components/schemas/DonationAmountMode"
   },
   "fixedAmounts": {
    "type": "array",
    "description": "1.1.129. Predefined values, e.g. 5, 10, 25.",
    "items": {
     "$ref": "../shared/common.yaml#/components/schemas/Money"
    }
   },
   "minAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "maxAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "liabilityAccountId": {
    "type": "string",
    "format": "uuid",
    "description": "**Donations post here, not to revenue** (1.1.132). Money collected for a charity is not the venue's to recognise, and treating it as revenue is a restatement waiting to happen.\n"
   },
   "channels": {
    "type": "array",
    "description": "1.1.133. Where it may be solicited — POS, kiosk, web, app.",
    "items": {
     "$ref": "../shared/common.yaml#/components/schemas/SalesChannel"
    }
   },
   "isActive": {
    "type": "boolean"
   },
   "validFrom": {
    "type": "string",
    "format": "date-time"
   },
   "validTo": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "raisedTotal": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "readOnly": true,
    "description": "**Not reversed when the campaign closes.** The money is still owed.\n"
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
  "x-ticvai-persistence": "none — a draft, applied through the owning contract; the draft itself is the ai.proposed_action row named by proposedActionId",
  "required": [
   "proposedActionId",
   "kind",
   "targetContract",
   "targetOperation",
   "payload"
  ],
  "properties": {
   "proposedActionId": {
    "type": "string",
    "format": "uuid",
    "description": "**The `ai.proposed_action` row this draft was written as**, and the id `decideProposedAction` takes. Without it a reviewer (BO-598) has a draft and no way to approve it.\n"
   },
   "kind": {
    "type": "string",
    "enum": [
     "product",
     "membership",
     "pass",
     "promotion",
     "discountRule",
     "pricingCalendar",
     "seatingZone",
     "operatingHours",
     "campaign"
    ],
    "description": "The `kind` the request asked for."
   },
   "targetContract": {
    "type": "string"
   },
   "targetOperation": {
    "type": "string"
   },
   "payload": {
    "type": "object",
    "additionalProperties": true,
    "description": "**Open on purpose: its shape is the request body of `targetOperation` in `targetContract`**, validated against that operation before it is returned — this contract does not restate thirty other contracts' request schemas.\n"
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
   },
   "planId": {
    "type": "string",
    "format": "uuid",
    "description": "The one-step `ai.action_plan` the draft was written as (AI design 2.3), readable with `getActionPlan`."
   }
  }
 },
 "GuestMerchandiseItem": {
  "x-ticvai-persistence": "none — guest projection of MerchandiseItem",
  "type": "object",
  "description": "**What a guest caller of `listMerchandise` receives.** The fields a shop screen shows and the ids a guest needs to reserve or buy, and nothing else: no inventory link, no catalogue variant, no stock count, no serial-number flag. `additionalProperties: false` is the guarantee: a staff field added to `MerchandiseItem` does not reach a guest by default.\n",
  "additionalProperties": false,
  "required": [
   "id",
   "name",
   "outletId",
   "price",
   "isAvailable"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "sku": {
    "type": "string"
   },
   "name": {
    "type": "string"
   },
   "description": {
    "type": "string",
    "nullable": true
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
   "price": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "isAvailable": {
    "type": "boolean",
    "description": "True when the item is active and in stock at its outlet. An item with no `inventoryItemId` never runs out, so it is available while active.\n"
   },
   "isReturnable": {
    "type": "boolean"
   },
   "returnWindowDays": {
    "type": "integer",
    "nullable": true
   },
   "imageAssetRef": {
    "type": "string",
    "nullable": true
   }
  }
 },
 "Journey": {
  "type": "object",
  "x-ticvai-persistence": "marketing.journey + marketing.journey_step",
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
    "readOnly": true,
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
    "readOnly": true,
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
    "readOnly": true,
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
    "x-ticvai-column": "type",
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
    "x-ticvai-column": "message_template_id",
    "description": "For `send`. Channel is resolved from the guest's preference at the moment of sending."
   },
   "sendTimeMode": {
    "type": "string",
    "enum": [
     "fixed",
     "optimised"
    ],
    "default": "fixed",
    "description": "For `send` (29 September, build pass, group G2; 22.3.19). `optimised` delays the send, after the step is reached, to the recipient's suggested hour from `ai.requestSuggestion` (kind `sendTime`) within the next 24 hours and inside `waitUntil`; no suggestion or AI off sends at once, as `fixed`."
   },
   "channelMode": {
    "type": "string",
    "enum": [
     "preference",
     "optimised"
    ],
    "default": "preference",
    "description": "For `send`. `optimised` tries first the consented channel the send-time suggestion names, then `channelPreference` in order (22.9.16)."
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
    "nullable": true,
    "x-ticvai-column": "next_journey_step_id"
   },
   "goalEvent": {
    "type": "string",
    "nullable": true,
    "description": "For `goal`. **The event that means this journey worked and the guest should leave it** — a purchase for abandoned cart, a renewal for membership. **Reaching a goal exits immediately**, which is what stops a recovered cart from being chased.\n"
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
 "MarketingCampaignVariant": {
  "type": "object",
  "x-ticvai-persistence": "marketing.campaign_variant",
  "description": "One content or subject variant of a campaign, for an A/B test (22.1.17; 29 September, build pass, group G2, from group G1's handoff). Written with its campaign by `createCampaign` and `updateCampaign`.",
  "required": [
   "label"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "campaignId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "x-ticvai-references": "marketing.campaign"
   },
   "label": {
    "type": "string",
    "maxLength": 20,
    "description": "A, B, C..."
   },
   "subjectOverride": {
    "type": "object",
    "nullable": true,
    "description": "Subject line by locale.",
    "additionalProperties": {
     "type": "string"
    }
   },
   "templateId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "A different template for this variant; null uses the campaign's `content.templateId`."
   },
   "splitPercent": {
    "type": "integer",
    "minimum": 1,
    "maximum": 100,
    "nullable": true,
    "description": "Share of the test group; null splits evenly."
   },
   "source": {
    "type": "string",
    "enum": [
     "manual",
     "aiDraft"
    ],
    "default": "manual"
   },
   "aiDecisionRecordId": {
    "type": "string",
    "nullable": true,
    "description": "The decision record of the `ai.proposeMarketingContent` draft it came from, for `aiDraft`."
   },
   "isWinner": {
    "type": "boolean",
    "default": false,
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005), the campaign's."
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
 "Permission": {
  "type": "string",
  "enum": [
   "SESSION_FORCE_LOGOUT",
   "USER_MANAGE",
   "ROLE_MANAGE",
   "PERMISSION_GRANT",
   "PERMISSION_VIEW",
   "PERMISSION_MANAGE",
   "PLATFORM_TENANT_VIEW",
   "PLATFORM_TENANT_MANAGE",
   "PLATFORM_TENANT_TERMINATE",
   "PLATFORM_PLAN_MANAGE",
   "PLATFORM_CELL_VIEW",
   "PLATFORM_CELL_MANAGE",
   "PLATFORM_BILLING_VIEW",
   "PLATFORM_AI_MANAGE",
   "PLATFORM_BILLING_MANAGE",
   "PLATFORM_RELEASE_VIEW",
   "PLATFORM_RELEASE_MANAGE",
   "PLATFORM_RELEASE_PROMOTE",
   "PLATFORM_MIGRATION_VIEW",
   "PLATFORM_MIGRATION_APPLY",
   "PLATFORM_TENANT_ACCESS",
   "TENANT_CONFIGURE",
   "TENANT_VIEW",
   "TENANT_PUBLISH",
   "SCOPE_VIEW",
   "SCOPE_MANAGE",
   "REGION_CONFIGURE",
   "WORKSTATION_CONFIGURE",
   "PRODUCT_VIEW",
   "PRODUCT_CONFIGURE",
   "PRODUCT_APPROVE",
   "PRODUCT_PUBLISH",
   "PRICE_VIEW",
   "PRICE_CONFIGURE",
   "EVENT_CONFIGURE",
   "PERFORMANCE_CONFIGURE",
   "CAPACITY_CONFIGURE",
   "ORDER_VIEW",
   "ORDER_VIEW_OTHER",
   "ORDER_CREATE",
   "ORDER_MODIFY",
   "ORDER_DISCOUNT",
   "ORDER_CANCEL",
   "ORDER_VOID",
   "ORDER_REFUND",
   "ORDER_REFUND_APPROVE",
   "ORDER_REFUND_BULK",
   "ORDER_EXCHANGE",
   "ORDER_RESCHEDULE",
   "ORDER_REPRINT",
   "PRICE_OVERRIDE",
   "DISCOUNT_APPLY",
   "CREDIT_MANAGE",
   "CREDIT_OVERRIDE",
   "WALLET_VIEW",
   "WALLET_OPERATE",
   "WALLET_CONFIGURE",
   "PAYMENT_VIEW",
   "PAYMENT_CONFIGURE",
   "PAYMENT_PROVIDER_MANAGE",
   "PAYMENT_DISPUTE",
   "SHIFT_OPEN",
   "SHIFT_CLOSE",
   "SHIFT_SUSPEND",
   "SHIFT_CLOSE_OTHER",
   "SHIFT_APPROVE_OPEN",
   "SHIFT_APPROVE_CLOSE",
   "SHIFT_REOPEN",
   "CASH_LIFT",
   "CASH_ADD",
   "CASH_NO_SALE",
   "DEPOSIT_BOX_MODIFY_OWN",
   "DEPOSIT_BOX_MODIFY_OTHER",
   "OVERSHORT_ACCEPT",
   "ACCESS_VALIDATE",
   "ACCESS_OVERRIDE",
   "ACCESS_POINT_CONFIGURE",
   "TURNSTILE_MODE_SET",
   "TICKET_LOOKUP",
   "ACCREDITATION_VIEW",
   "ACCREDITATION_APPLY",
   "ACCREDITATION_APPROVE",
   "ACCREDITATION_ISSUE",
   "ACCREDITATION_MANAGE",
   "ACCREDITATION_CONFIGURE",
   "REPORT_VIEW_OWN",
   "REPORT_VIEW_WORKSTATION",
   "REPORT_VIEW_VENUE",
   "REPORT_VIEW_REGION",
   "REPORT_VIEW_TENANT",
   "REPORT_EXPORT",
   "REPORT_EXPORT_PII",
   "REPORT_MANAGE",
   "REPORT_SCHEDULE",
   "LEDGER_VIEW",
   "LEDGER_POST",
   "LEDGER_APPROVE",
   "TAX_CONFIGURE",
   "ACCOUNT_CONFIGURE",
   "SETTLEMENT_VIEW",
   "SETTLEMENT_RECONCILE",
   "GUEST_VIEW",
   "GUEST_VIEW_PII",
   "GUEST_MANAGE",
   "VENUE_MAP_VIEW",
   "VENUE_MAP_MANAGE",
   "VENUE_MAP_PUBLISH",
   "RESOURCE_VIEW",
   "RESOURCE_BOOK",
   "RESOURCE_MANAGE",
   "RESOURCE_CONFIGURE",
   "RENTAL_VIEW",
   "RENTAL_BOOK",
   "RENTAL_OPERATE",
   "RENTAL_MANAGE",
   "RENTAL_CONFIGURE",
   "RENTAL_PRICE",
   "RENTAL_APPROVE",
   "RENTAL_OVERRIDE",
   "DEVELOPER_VIEW",
   "DEVELOPER_MANAGE",
   "DEVELOPER_ADMIN",
   "LOYALTY_ACCRUE",
   "LOYALTY_REDEEM",
   "LOYALTY_ADJUST",
   "MARKETING_VIEW",
   "MARKETING_MANAGE",
   "MARKETING_SEND",
   "CASE_VIEW",
   "CASE_MANAGE",
   "ASSET_LIBRARY_VIEW",
   "ASSET_LIBRARY_MANAGE",
   "ASSET_LIBRARY_APPROVE",
   "ASSET_LIBRARY_SHARE",
   "QUEUE_VIEW",
   "QUEUE_MANAGE",
   "QUEUE_REDEEM",
   "QUEUE_OVERRIDE",
   "TRANSPORT_VIEW",
   "TRANSPORT_MANAGE",
   "TRANSPORT_PRICE",
   "ASSET_VIEW",
   "ASSET_MANAGE",
   "WORK_ORDER_VIEW",
   "WORK_ORDER_MANAGE",
   "WORK_ORDER_VERIFY",
   "INSPECTION_VIEW",
   "INSPECTION_SUBMIT",
   "INSPECTION_MANAGE",
   "INCIDENT_REPORT",
   "INCIDENT_VIEW",
   "INCIDENT_MANAGE",
   "KIOSK_ATTEND",
   "DEVICE_VIEW",
   "DEVICE_CONFIGURE",
   "DEVICE_MANAGE",
   "APPROVAL_ACT",
   "APPROVAL_DELEGATE",
   "AI_USE",
   "AI_CONFIGURE",
   "AI_APPROVE",
   "AI_AUDIT_VIEW",
   "RISK_REVIEW",
   "RISK_INVESTIGATE",
   "AUDIT_VIEW",
   "APPROVAL_VIEW",
   "APPROVAL_REQUEST",
   "APPROVAL_DECIDE",
   "APPROVAL_CONFIGURE",
   "MAINTENANCE_EXECUTE",
   "MAINTENANCE_APPROVE",
   "WORKFORCE_VIEW",
   "WORKFORCE_MANAGE",
   "ATTENDANCE_RECORD",
   "ANNOUNCEMENT_PUBLISH",
   "ANNOUNCEMENT_EMERGENCY",
   "PARTNER_VIEW",
   "PARTNER_MANAGE",
   "PARKING_CONFIGURE",
   "PAYMENT_VOID",
   "PROCUREMENT_VIEW",
   "PROCUREMENT_REQUEST",
   "PROCUREMENT_MANAGE",
   "PROCUREMENT_RECEIVE"
  ]
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
   "outletId": {
    "type": "string",
    "format": "uuid",
    "description": "The outlet whose price and stock this is: the asking workstation's outlet, or `outletId` for a caller with none (decided 28 September, audit R215).\n"
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
   "code": {
    "type": "string",
    "maxLength": 64,
    "nullable": true,
    "x-ticvai-unique": "tenant",
    "description": "**Taken from their category tables, 20 September.** Ours had a uuid and a localised name, so an importer matching *Beverages* had to match on a display string that a venue is free to translate.\n**Unique per tenant where set** (decided 28 September, audit R108): two categories in one tenant never share a code, and `setProductCategories` refuses a body that would, with `409 duplicate-code`.\n"
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
    "type": "string",
    "readOnly": true,
    "description": "Set by the server from the venue the caller acts at; not sent."
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
   "description": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "nullable": true,
    "description": "The short line a guest reads under a category option, e.g. *Surf lessons: learn on the beginner wave with a coach* (decided 29 September, rev 3 REV3-19). Each language value at most 200 characters.\n"
   },
   "bookingFlowId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**The booking flow for every product filed here** that names none of its own (decided 29 September, W12, BO-115). Null means the venue's flow for each product's `kind`. A white-label `BookingFlow` of the venue; `setProductCategories` refuses any other id with `422`.\n"
   },
   "isActive": {
    "type": "boolean",
    "default": true,
    "description": "**Deactivated rather than deleted.** A category with a season behind it still names the products sold under it, and removing it rewrites last year's report.\n"
   }
  }
 },
 "ProductCategoryNode": {
  "x-ticvai-persistence": "none — projection over catalogue.product_category",
  "description": "**One node of the tree `listProductCategories` returns.** A `ProductCategory` with its children nested under it, in `displayOrder`, so no caller reassembles the hierarchy from `parentId`. `setProductCategories` still takes the flat list, because a write names each parent by id.\n",
  "allOf": [
   {
    "$ref": "#/components/schemas/ProductCategory"
   },
   {
    "type": "object",
    "required": [
     "children"
    ],
    "properties": {
     "children": {
      "type": "array",
      "description": "Empty on a leaf.",
      "items": {
       "$ref": "#/components/schemas/ProductCategoryNode"
      }
     }
    }
   }
  ]
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
    "format": "uuid",
    "readOnly": true
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
 "Segment": {
  "x-ticvai-persistence": "marketing.segment + marketing.segment_criterion",
  "allOf": [
   {
    "$ref": "#/components/schemas/CreateSegmentRequest"
   },
   {
    "type": "object",
    "required": [
     "id",
     "createdAt"
    ],
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid"
     },
     "lastEvaluatedSize": {
      "type": "integer",
      "nullable": true
     },
     "lastEvaluatedAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true
     },
     "createdAt": {
      "type": "string",
      "format": "date-time"
     }
    }
   }
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
   "maturity",
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
   "maturity": {
    "$ref": "#/components/schemas/AiMaturity"
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
  "description": "What is being suggested. **A closed set, and the reason it is closed is the swap.** Every entry here is a question a venue asks that a model could answer better than a rule — and each one starts as a heuristic and becomes a model when there is data.\n**Six of these were drawn as their own endpoints on the client F&B boards** — `suggestPrice`, `simulateScenario`, `simulateSlaPolicy`, `suggestRequisition`, `suggestReplenishment`, `publishDemandPlan`. **Building six endpoints means six places to change when a model changes**, and the model will change more often than the venue's question does.\n**What each kind is based on, and when the venue's own data takes over. Proposed, client to correct (decided 28 September, audit R213; re-read 29 September, AI functions review).** The figure after each rule is **the point where own data takes over from the baseline, not a refusal**: below it the kind answers from the baseline (venue AI settings, the starting pattern for the venue type, the UAE calendar, the weather) with `maturity.stage` `starting`, and between it and about three months it blends the two (`learning`). The day-one baseline per kind: `replenishment`, `requisition`, `prepPlan`, `staffing`, `demandForecast` and `scenario` from the baseline forecast (typical attendance from the venue AI settings x the venue-type month curve x the calendar x weather, bookings on hand as a floor); `menuEngineering` ranked by margin with popularity marked learning; `slaTarget` a standard default; `waitTime` people ahead / configured capacity; `upsell` the relationship map and business priority; `segmentation` known guest attributes; `anomaly` the venue's configured thresholds and actual against the forecast's low end; `sendTime` the channel's typical hour; `wasteRisk` shelf life and par against the forecast; `queueBalancing` configured capacity per queue. Only a missing setting refuses (422 `AiMissingSettingProblem`).\n- `price`: unit cost plus the category's target margin, held inside the price band. Minimum: a current cost, no history.\n- `replenishment`: par level minus on-hand plus expected use over the supplier lead time. Minimum: 14 days of stock movements.\n- `requisition`: the next service's prep-plan ingredient needs minus kitchen stock. Minimum: 14 days of sales.\n- `demandForecast`: the average of the same weekday over the last 8 weeks, adjusted by admissions already booked. Minimum: 8 weeks of sales.\n- `prepPlan`: forecast covers for the service times each item's share of the last 4 same weekdays. Minimum: 4 weeks of sales.\n- `menuEngineering`: each item placed by popularity against margin, over 90 days. Minimum: 90 days of sales.\n- `staffing`: forecast demand divided by the role's standard covers per staff hour. Minimum: 8 weeks of sales (the forecast it rests on).\n- `slaTarget`: the 80th percentile of actual times over the last 30 days. Minimum: 30 days of timed events.\n- `waitTime`: people ahead divided by the throughput of the last 30 minutes. Minimum: 30 minutes of throughput today.\n- `upsell`: the item most often bought with the basket's items over 90 days. Minimum: 90 days of orders.\n- `segmentation`: recency, frequency and spend scores over 12 months. Minimum: 90 days of orders.\n- `anomaly`: a value outside three standard deviations of the same weekday over 8 weeks. Minimum: 8 weeks of the measure.\n- `scenario`: the demand forecast re-run with the stated changes. Minimum: as `demandForecast`.\n- `sendTime` (added 29 September): per recipient, the hour inside `context.sendWindow` in which they have most often opened or clicked over the last 90 days (marketing-crm attribution touches), and where `context.channel` is `best`, the consented channel with the highest engagement. A recipient with fewer than three touches gets their segment's modal hour, and one with none the window's start. Asked with `subjectRef` a segment id or `context.subjectIds` (at most 10,000). `value` is `{recommendations: [{subjectId, sendAt, channel, basisTouches}]}`. Minimum: 90 days of message touches at the scope.\n- `wasteRisk` (added 29 September): per item at an outlet or store location, planned production and stock on hand minus forecast demand over the item's shelf life, plus batches expiring inside the horizon (`inventory.listExpiringBatches`). `value` is `{items: [{itemRef, quantityAtRisk, valueAtCost, expiresAt, recommendedAction (reducePrep, promote, transfer, useInRecipe), transferTo}]}`. Minimum: 14 days of recorded waste and of sales.\n- `queueBalancing` (added 29 September): per queue or attraction at `subjectRef` (a venue) over `horizon`, the forecast wait (the `queue` forecast definition) against throughput capacity, a recommended virtual-queue return-slot allocation by queue type, and guest redirection from over-used to under-used attractions. `value` is `{queues: [{queueId, forecastWaitMinutes, capacityPerHour, returnSlotsPerInterval, redirectTo}]}`. Minimum: 14 days of queue readings.\n- `itinerary` (added 29 September, MOB-6, guest-allowed): refines a `venue-map` visit plan the guest owns. `subjectRef` is the plan id; `value` is `{planId, baseVersion, changes, rationale}`, applied with `updateVisitPlan` as the guest. Minimum: none; the rules plan is the baseline.\n",
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
   "scenario",
   "sendTime",
   "wasteRisk",
   "queueBalancing",
   "itinerary"
  ]
 },
 "UpsellPlacement": {
  "type": "string",
  "enum": [
   "productDetail",
   "cart",
   "checkout",
   "postPurchase",
   "atGate",
   "inVenue"
  ]
 },
 "UpsellRule": {
  "x-ticvai-persistence": "promotions.upsell_rule",
  "type": "object",
  "required": [
   "id",
   "name",
   "placement",
   "triggerVariantIds",
   "suggestedVariantIds"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "regionId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "The region that owns the rule. Upsell rules are owned at region and read at venue (decided 28 September, audit R183); set from the caller's region scope on create.\n"
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "placement": {
    "$ref": "#/components/schemas/UpsellPlacement"
   },
   "triggerVariantIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "triggerCategoryIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "suggestedVariantIds": {
    "type": "array",
    "minItems": 1,
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "suggestedBundleId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "channels": {
    "type": "array",
    "description": "Empty applies to every channel. Restriction is opt-in — a rule that fires on the website but not at a counter is a guest experience inconsistency.\n",
    "items": {
     "type": "string"
    }
   },
   "priority": {
    "type": "integer",
    "default": 0
   },
   "maxSuggestions": {
    "type": "integer",
    "default": 3
   },
   "isActive": {
    "type": "boolean"
   }
  }
 },
 "VenueSettings": {
  "type": "object",
  "x-ticvai-persistence": "platform.venue_settings",
  "description": "**Venue-level operational configuration that no other level can answer.**\nRegion owns currency, tax regime and fiscal year (ADR-0011). Venue owns the things that vary between two venues in one region — **opening hours, support hours, and what the local law requires of the gate.**\n**And the configured limits** (decided 28 September, audit R094): every limit the contracts call *configured* is a field here, from `displayCurrencies` and `cartLeaseSeconds` down to the grouped `catalogue`, `inventory`, `seating`, `promotions`, `fnb`, `queue`, `reporting`, `marketing` and `identity` settings. **Each has a tenant-level default**: the tenant sets it once with `setVenueSettingsDefaults`, a venue overrides it within the field's bounds, and a null field here inherits it. Each field's `default` is the proposed tenant default, marked proposed, client to correct (audit R094); `docs/active/configured-limits-proposal.md` is the sheet the client corrects, and where the two differ this contract is what runs.\n",
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
    "description": "From the path of `setVenueSettings`."
   },
   "calendarDayStartHour": {
    "type": "integer",
    "minimum": 0,
    "maximum": 23,
    "nullable": true,
    "default": 6,
    "description": "**Where the venue's calendar day starts** (17 September minutes M17-03, added 30 September): the first hour row of every day and week calendar view (`calendarView` in `screens/_components.yaml`), so a venue open 06:00 to 02:00 sees its night on the day it belongs to. Display only: it moves no booking, slot or business date. Null inherits the tenant default (proposed 6, client to correct).\n"
   },
   "currencyCode": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "nullable": true,
    "readOnly": true,
    "description": "**`readOnly` is the freeze.** `setVenueSettings` takes this whole schema as its request body, so without it any settings save could rewrite the currency of a venue that had already traded — which is the one thing ADR-0018's amendment forbids. It is set when the venue is provisioned, defaulted from the region, and changed only by an operation whose precondition is that the venue has not yet traded.\n**The venue's trading currency, defaulted from its region and frozen once the venue has traded** (ADR-0018, amended 20 September). Currency was a region-only fact, grouped with tax rates on the reasoning that *\"a venue cannot choose its VAT\"* -- true of tax and over-applied to currency, because a free-zone unit, a duty-free shop and a cruise terminal genuinely trade in a currency their region does not.\n**This column exists because the freeze needs somewhere to live.** A venue that resolved purely from its region would silently follow a region currency change after it had already traded, and every dated artefact beneath it -- a price list is a `validFrom`/`validTo` range -- would render retrospectively wrong. Null means \"resolve from the region\", which is the answer for every venue that has not overridden.\n"
   },
   "currencyScale": {
    "type": "integer",
    "minimum": 0,
    "maximum": 4,
    "nullable": true,
    "readOnly": true,
    "description": "**Scale travels with currency** (ADR-0008), and so does the freeze. OMR is three decimal places because Oman says so; overriding the currency without the scale gets rounding wrong. Set together or not at all.\n"
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
      "type": "string",
      "description": "IANA zone the `windows` are read in. Absent, they are read in the region's `timeZone`, like every other wall-clock time in this contract.\n"
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
         "type": "string",
         "description": "Wall-clock time the desk opens."
        },
        "to": {
         "type": "string",
         "description": "Wall-clock time the desk closes."
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
      "type": "string",
      "description": "Wall-clock time sending stops",
      "in the region's time zone.": null
     },
     "to": {
      "type": "string",
      "description": "Wall-clock time sending resumes",
      "in the region's time zone.": null
     }
    }
   },
   "biometrics": {
    "type": "object",
    "nullable": true,
    "description": "CF-35, BL-096, BL-105, BL-106. **The venue-level master switch, and the one place a person is asked whether the paperwork exists.** Biometric data is sensitive under PDPL (Federal Decree-Law 45/2021) — heightened protection, explicit consent, and an Article 21 assessment before the processing rather than after it.\n**Nothing below this switch operates while it is off.** `AdmissionRules` may carry a `biometricPolicy` per ticket type and those rules are inert until a venue enables biometrics here, which means a profile copied between venues cannot start capturing faces at the destination.\n**Venue level because that is where the assessment is filed.** Region owns tax and currency; the DPIA, the consent notice and the hardware are a venue's.\n",
    "properties": {
     "isEnabled": {
      "type": "boolean",
      "default": false,
      "description": "**Off by default, and turning it on is refused without the two fields below.** `setVenueSettings` answers 422 rather than accepting an enable it cannot evidence — **a DPIA nobody can name is a DPIA nobody did**, and the point of the refusal is that the person switching this on is asked at the moment they switch it on rather than by an auditor a year later.\n"
     },
     "dpiaReference": {
      "type": "string",
      "nullable": true,
      "maxLength": 200,
      "description": "**The venue's own reference for its Article 21 assessment.** The platform does not hold the document and does not judge it; it records that one was named, by whom, and when — which is what an audit asks for and what the venue can produce.\n"
     },
     "consentNoticeAcknowledgedAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true,
      "description": "**When somebody confirmed the consent forms are in place at the point of capture.** A guest consenting in an app is a record; a guest consenting at a ticket counter is a notice somebody has to have printed and a question somebody has to have asked.\n"
     },
     "acknowledgedByPrincipalId": {
      "type": "string",
      "format": "uuid",
      "nullable": true,
      "readOnly": true,
      "description": "**Who confirmed it.** An acknowledgement with no name behind it cannot be followed up, and this is the field that makes the switch an act rather than a setting. Recorded by the server as the caller whose save carried the acknowledgement, so it cannot name somebody else.\n"
     },
     "faceTagPurgeMinutesAfterClose": {
      "type": "integer",
      "nullable": true,
      "default": 0,
      "description": "BL-106. **How long a same-visit Face Tag survives past the close of the operating day**, and zero is the default because that is what 3.2.44 describes. A non-zero value is an operational allowance for a late reconciliation, not a retention period — **`facePass` ignores this entirely** and is bounded by its entitlement.\n"
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
         "type": "string",
         "description": "Wall-clock time",
         "in the region's time zone.": null
        },
        "to": {
         "type": "string",
         "description": "Wall-clock time",
         "in the region's time zone.": null
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
       "off",
       "staffAssisted",
       "deviceAssisted"
      ],
      "default": "off",
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
   },
   "displayCurrencies": {
    "type": "array",
    "nullable": true,
    "description": "**Which currencies this venue shows guests** (decided 28 September, audit R120 (a)). ISO 4217 codes, each one its region holds an `FxRate` for; the rate itself stays per region and is never set here. `finance.listFxRates` with `venueId` narrows the region's rates to these. Null or empty shows the trading currency only. A code the region has no rate for is refused `400`.\n",
    "items": {
     "type": "string",
     "pattern": "^[A-Z]{3}$"
    }
   },
   "cartLeaseSeconds": {
    "type": "integer",
    "nullable": true,
    "minimum": 30,
    "maximum": 3600,
    "default": 900,
    "description": "**How long a cart holds capacity** (decided 28 September, audit R169): 15 minutes, the default `catalogue.acquireInventoryHold` takes for `ttlSeconds`. Proposed, client to correct (audit R094).\n"
   },
   "cartHoldExtensionMinutes": {
    "type": "integer",
    "nullable": true,
    "minimum": 1,
    "maximum": 30,
    "default": 5,
    "description": "How long one `orders.extendCart` extension adds. Proposed, client to correct (audit R094)."
   },
   "cartMaxExtensions": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "maximum": 5,
    "default": 1,
    "description": "How many extensions a cart may take before `extensionCapReached` (`Cart.maxExtensions`). Proposed, client to correct (audit R094)."
   },
   "resaleCutoffHours": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "maximum": 168,
    "default": 24,
    "description": "Hours before the performance after which a ticket can no longer be listed for resale (`orders.createResaleListing`). Proposed, client to correct (audit R094)."
   },
   "exchangeCutoffHours": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "maximum": 720,
    "default": 24,
    "description": "Hours before the original performance after which lines can no longer be exchanged (`orders.exchangeOrderLines`, `outsideExchangeWindow`). Proposed, client to correct (audit R094)."
   },
   "rescheduleCutoffHours": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "maximum": 720,
    "default": 24,
    "description": "Hours before the original performance after which an order can no longer be rescheduled (`orders.rescheduleOrder`, `outsideRescheduleWindow`). Proposed, client to correct (audit R094)."
   },
   "reservationMaxExtensions": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "maximum": 5,
    "default": 1,
    "description": "How many times `orders.extendReservation` may extend one reservation. Proposed, client to correct (audit R094)."
   },
   "shiftVarianceThreshold": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "Over or short at shift close beyond which the shift waits in `pendingVariance` for `shift.acceptShiftVariance`. **Proposed tenant default AED 20.00, bounds 0 to 1,000 in the venue currency; client finance to correct (audit R094).**\n"
   },
   "catalogue": {
    "type": "object",
    "nullable": true,
    "properties": {
     "maxVariantsPerProduct": {
      "type": "integer",
      "nullable": true,
      "minimum": 1,
      "maximum": 2000,
      "default": 200,
      "description": "Variants one product may generate from its attributes (`setProductAttributes` refuses above it). Proposed, client to correct (audit R094)."
     },
     "waitlistOfferHoldMinutes": {
      "type": "integer",
      "nullable": true,
      "minimum": 1,
      "maximum": 1440,
      "default": 30,
      "description": "How long a waitlist offer holds the released capacity for the guest it was offered to. Proposed, client to correct (audit R094)."
     },
     "bulkPriceChangeEscalationPercent": {
      "type": "number",
      "nullable": true,
      "minimum": 0,
      "maximum": 100,
      "default": 10,
      "description": "A `bulkChangePrices` run changing any price by more than this percentage needs `PRICE_CONFIGURE` (audit R197). Proposed, client to correct (audit R094)."
     },
     "bulkPriceChangeEscalationCount": {
      "type": "integer",
      "nullable": true,
      "minimum": 1,
      "default": 50,
      "description": "A `bulkChangePrices` run touching more prices than this needs `PRICE_CONFIGURE` (audit R197). Proposed, client to correct (audit R094)."
     }
    }
   },
   "inventory": {
    "type": "object",
    "nullable": true,
    "properties": {
     "overReceiptTolerancePercent": {
      "type": "number",
      "nullable": true,
      "minimum": 0,
      "maximum": 25,
      "default": 5,
      "description": "Percent above the outstanding ordered quantity a goods receipt line may record (`createGoodsReceipt`). Proposed, client to correct (audit R094)."
     },
     "countVarianceTolerancePercent": {
      "type": "number",
      "nullable": true,
      "minimum": 0,
      "maximum": 25,
      "default": 2,
      "description": "Percent difference between counted and expected quantity before a count line is an exception (`getCountVariance`). Proposed, client to correct (audit R094)."
     },
     "countVarianceApprovalAmount": {
      "allOf": [
       {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      ],
      "nullable": true,
      "description": "Total variance value of a count above which posting it needs approval (`postStockCount`). **Proposed tenant default 1,000.00 in the venue currency, client finance to correct (audit R094).**\n"
     }
    }
   },
   "seating": {
    "type": "object",
    "nullable": true,
    "properties": {
     "seatHoldExtensionSeconds": {
      "type": "integer",
      "nullable": true,
      "minimum": 60,
      "maximum": 1800,
      "default": 300,
      "description": "What one `extendSeatHold` adds. No hold outlives 30 minutes in all (audit R169). Proposed, client to correct (audit R094)."
     },
     "seatHoldMaxExtensions": {
      "type": "integer",
      "nullable": true,
      "minimum": 0,
      "maximum": 5,
      "default": 2,
      "description": "How many times a seat hold may be extended. Proposed, client to correct (audit R094). A resource hold on a venue map (`resources.extendResourceHold`) uses the same two bounds (decided 29 September, rev 3 REV3-15)."
     },
     "maxSeatsPerGuestOrder": {
      "type": "integer",
      "nullable": true,
      "minimum": 1,
      "maximum": 50,
      "default": 10,
      "description": "**Seats one guest may take in one booking on a guest channel** (Guest Web, Guest App), decided 29 September, rev 3 REV3-7. `seating.createSeatHold` counts the seats in the request plus the seats the same guest already holds on the same performance, and refuses above this with `422` `seat-limit-exceeded`, naming the limit. Default 10, bounds 1 to 50; a venue sets its own in Venue Management. Staff and POS sales keep 10 per sale (audit R080 (c)) and do not read this field.\n"
     }
    }
   },
   "promotions": {
    "type": "object",
    "nullable": true,
    "properties": {
     "maxDiscountPercent": {
      "type": "number",
      "nullable": true,
      "minimum": 0,
      "maximum": 100,
      "default": 30,
      "description": "The largest discount one promotion may give (`createPromotion` refuses above it). Proposed, client to correct (audit R094)."
     },
     "nearZeroLinePrice": {
      "allOf": [
       {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      ],
      "nullable": true,
      "description": "Net line price below which a stacked combination is flagged near-zero in `analysePromotionConflicts` (audit R096 (5)); a warning, not a refusal. **Proposed tenant default AED 1.00, client to correct (audit R094).**\n"
     }
    }
   },
   "fnb": {
    "type": "object",
    "nullable": true,
    "properties": {
     "recallWindowMinutes": {
      "type": "integer",
      "nullable": true,
      "minimum": 0,
      "maximum": 60,
      "default": 10,
      "description": "Minutes after a bump during which `recallKitchenTicket` still recalls; after it the act is a refire. Proposed, client to correct (audit R094)."
     },
     "compEscalationAmount": {
      "allOf": [
       {
        "$ref": "../shared/common.yaml#/components/schemas/Money"
       }
      ],
      "nullable": true,
      "description": "Line value above which `compItem` needs `ORDER_DISCOUNT` (audit R197). **Proposed tenant default AED 100.00, client to correct (audit R094).**\n"
     },
     "foodSafetyLeadPrincipalId": {
      "type": "string",
      "format": "uuid",
      "nullable": true,
      "description": "**The venue's food-safety lead**, to whom `escalateCorrectiveAction` sends every escalation (decided 28 September, audit R096 (9)). A venue fact, so it has no tenant default; while it is null an escalation is refused `409 no-food-safety-lead`.\n"
     }
    }
   },
   "queue": {
    "type": "object",
    "nullable": true,
    "properties": {
     "crossQueueLimit": {
      "type": "integer",
      "nullable": true,
      "minimum": 1,
      "maximum": 10,
      "default": 2,
      "description": "Virtual queues one guest party may wait in at once (`joinQueue`, `crossQueueLimitReached`). Proposed, client to correct (audit R094)."
     }
    }
   },
   "reporting": {
    "type": "object",
    "nullable": true,
    "properties": {
     "inlineRunRowLimit": {
      "type": "integer",
      "nullable": true,
      "minimum": 1000,
      "maximum": 100000,
      "default": 5000,
      "description": "Estimated rows above which `runReport` answers `202` and runs in the background. Proposed, client to correct (audit R094)."
     },
     "dashboardRefreshBudgetPerMinute": {
      "type": "integer",
      "nullable": true,
      "minimum": 1,
      "default": 24,
      "description": "Tile refreshes per minute, summed over a dashboard's tiles, that `createDashboard` allows. Proposed, client to correct (audit R094)."
     }
    }
   },
   "marketing": {
    "type": "object",
    "nullable": true,
    "properties": {
     "attributionWindowDays": {
      "type": "integer",
      "nullable": true,
      "minimum": 1,
      "maximum": 30,
      "default": 7,
      "description": "Days after a campaign touch within which a booking is attributed to it (`getCampaignPerformance`). Proposed, client to correct (audit R094)."
     }
    }
   },
   "identity": {
    "type": "object",
    "nullable": true,
    "properties": {
     "guestOtpMaxAttempts": {
      "type": "integer",
      "nullable": true,
      "minimum": 3,
      "maximum": 10,
      "default": 5,
      "description": "Wrong entries allowed per guest one-time code before `verifyGuestOtp` invalidates it. A guest code is tenant-scoped, so the tenant default is the value used. Proposed, client to correct (audit R094).\n"
     },
     "guestTwoStep": {
      "type": "object",
      "nullable": true,
      "description": "**Guest two-step verification: a venue option, off unless the venue enables it in Venue Management** (decided 29 September, rev 3 GAP-B1, per venue, superseding the second part of audit R167, \"no guest MFA\"; an earlier draft of the same day put it on the tenant's `PasswordPolicy`, which no longer carries it). **The guest's enrolment stays tenant-wide**: one guest account across the tenant's venues, so a method enrolled once is used in every venue that has this on, and is never asked in a venue that has it off. Identity learns the venue from `venueId` on the guest sign-in (`verifyGuestOtp`, `guestPasswordLogin`, `guestSocialLogin`, `guestUaePassLogin`) and on `createMfaChallenge`: the venue the guest app or booking is in; with no venue given, an enrolled guest is asked when any venue of the tenant has it on. Guests may enrol `totp` with `emailOtp` as the fallback, as staff do (audit R126 (5)); it is never forced. Guests still never use enterprise SSO (R167, first part). A null inherits the tenant default set with `setVenueSettingsDefaults`.\n",
      "properties": {
       "enabled": {
        "type": "boolean",
        "default": false,
        "description": "Off unless the venue enables it. While no venue of the tenant has it on, guests cannot enrol (`enrolMfaMethod` answers 403 `guest-two-step-disabled`)."
       },
       "stepUpActions": {
        "type": "array",
        "uniqueItems": true,
        "description": "The guest actions in this venue that ask an enrolled guest for the factor again, whatever the age of the session. The service performing the action passes this venue to `createMfaChallenge`. Proposed, client to correct (rev 3 GAP-B1).\n",
        "items": {
         "type": "string",
         "enum": [
          "changeContactDetails",
          "changePassword",
          "managePaymentMethods",
          "transferTickets",
          "deleteAccount"
         ]
        },
        "default": [
         "changeContactDetails",
         "changePassword",
         "managePaymentMethods",
         "deleteAccount"
        ]
       }
      }
     }
    }
   }
  }
 },
 "Workstation": {
  "x-ticvai-persistence": "platform.workstation",
  "type": "object",
  "required": [
   "id",
   "code",
   "name",
   "venueId",
   "regionId",
   "scopePath",
   "saleBoard",
   "currency",
   "currencyScale",
   "timeZone"
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
   "regionId": {
    "type": "string",
    "format": "uuid"
   },
   "departmentId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "scopePath": {
    "type": "string"
   },
   "saleBoard": {
    "type": "object",
    "description": "Determines which front end loads. Bound to the workstation, not the role — the F&B terminal opens the F&B board. What the operator may then DO within it is governed by their permissions.\n",
    "required": [
     "id",
     "kind"
    ],
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid"
     },
     "kind": {
      "$ref": "#/components/schemas/SaleBoardKind"
     },
     "name": {
      "type": "string"
     }
    }
   },
   "accessPointId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Inherited from the workstation, never selected by the operator. Null where the workstation is not at an access point.\n"
   },
   "devices": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/DeviceBinding"
    }
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
   "timeZone": {
    "type": "string"
   },
   "deploymentProfile": {
    "$ref": "#/components/schemas/DeploymentProfile"
   },
   "edgeNodeId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Present when `deploymentProfile` is `venueEdge`."
   },
   "healthScore": {
    "type": "integer",
    "nullable": true,
    "minimum": 0,
    "maximum": 100,
    "readOnly": true,
    "description": "Board 1 of the client's POS set. **A number a manager can sort by** — the package held `lastHeartbeatAt` and a heartbeat timestamp is not a score.\nThe client's board shows 1,248 workstations at 96% healthy, and **the value of that figure is that it ranks**: a fleet dashboard exists so somebody can open the worst one first.\n**Derived from its devices, its heartbeat age, its firmware currency and its error rate.** Read-only, because a workstation that could set its own score would.\n**The formula, proposed, client to correct (audit R096 (2)):** score = 40% device online share (the share of its devices reporting online) + 25% heartbeat freshness (100 at one minute old or less, 0 at 15 minutes or more, linear between) + 20% firmware and profile currency (100 on the latest, 50 one version behind, 0 older) + 15% error rate (100 at 0 errors an hour, 0 at 10 or more, linear between), rounded to a whole number. **Below 80 is a warning and below 60 a failure.**\n"
   },
   "configurationProfileId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Which profile this workstation runs, and at which version. **The client's board shows a fleet split four ways — 72% latest, 18.8% one behind, 6.1% outdated** — and the package had a firmware version field and no profile.\n**A profile is what a venue changes; a version is what it deploys.** Conflating them means a venue cannot say *roll the ticketing counters back and leave the kiosks*.\n"
   },
   "catalogueState": {
    "$ref": "#/components/schemas/CatalogueState"
   },
   "offlineCapable": {
    "type": "boolean",
    "description": "Derived from `deploymentProfile`. False only for `thin`. Under local-first, catalogue READS are always local on transactional surfaces; this flag governs whether WRITES can be queued.\n"
   },
   "isActive": {
    "type": "boolean"
   }
  }
 }
}
```
