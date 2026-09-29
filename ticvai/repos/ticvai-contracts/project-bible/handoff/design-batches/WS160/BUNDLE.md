# WS160 — Resource Management Configuration board 6

**10 screens · 22 operations · 31 schemas · 11 permissions**

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

- **Every control that can be refused must be gated.** 11 permissions apply here:
  `ASSET_VIEW, INSPECTION_SUBMIT, INSPECTION_VIEW, RENTAL_CONFIGURE, RENTAL_OPERATE, RENTAL_PRICE, RENTAL_VIEW, RESOURCE_BOOK, RESOURCE_MANAGE, RESOURCE_VIEW, WORK_ORDER_MANAGE`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-903` | Equipment & Asset Command Center | listDetail | 2 | 0 | — |
| `BO-904` | Rental Resource Configuration | configEditor | 2 | 0 | — |
| `BO-905` | Rental Inventory & Availability Control | configEditor | 2 | 0 | — |
| `BO-906` | Resource Checkout Workspace | configEditor | 2 | 0 | — |
| `BO-907` | Guest & Resource Assignment | listDetail | 2 | 0 | — |
| `BO-908` | Rental Duration, Extension & Return Management | listDetail | 2 | 0 | — |
| `BO-909` | Deposit & Rental Financial Control | listDetail | 2 | 0 | — |
| `BO-910` | Maintenance & Resource Blocking | configEditor | 3 | 0 | — |
| `BO-911` | Inspection, Condition & Compliance Management | listDetail | 3 | 0 | — |
| `BO-912` | Asset Lifecycle, Depreciation & Retirement | listDetail | 2 | 0 | — |

## Thin screens in this batch

**BO-903, BO-907, BO-908, BO-909 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-903",
  "name": "Equipment & Asset Command Center",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "6",
   "number": "01",
   "page": 82
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/equipment-asset-command-center-bo-903",
   "component": "apps/venue-management-web/src/routes/rentals/EquipmentAssetCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-904",
    "BO-905",
    "BO-906",
    "BO-907",
    "BO-908",
    "BO-909",
    "BO-910",
    "BO-911",
    "BO-912"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "BO-904",
     "trigger": "Rental Resource Configuration",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    },
    {
     "to": "BO-905",
     "trigger": "Rental Inventory & Availability Control",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    },
    {
     "to": "BO-906",
     "trigger": "Resource Checkout Workspace",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    },
    {
     "to": "BO-907",
     "trigger": "Guest & Resource Assignment",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    },
    {
     "to": "BO-908",
     "trigger": "Rental Duration, Extension & Return Management",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    },
    {
     "to": "BO-909",
     "trigger": "Deposit & Rental Financial Control",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    },
    {
     "to": "BO-910",
     "trigger": "Maintenance & Resource Blocking",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    },
    {
     "to": "BO-911",
     "trigger": "Inspection, Condition & Compliance Management",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    },
    {
     "to": "BO-912",
     "trigger": "Asset Lifecycle, Depreciation & Retirement",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "carries": [
      "assetId",
      "resourceId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide operations teams with a real-time overview of all physical resources across the organization.",
  "purposeNote": "Authorized users can understand the real-time operational state of all physical resources and immediately identify assets requiring operational action.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 82 §Display"
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
       "label": "Every equipment asset",
       "columns": [
        "Total assets",
        "Available",
        "Reserved",
        "Checked out",
        "In use",
        "Due for return",
        "Overdue",
        "Under maintenance",
        "Inspection due",
        "Damaged",
        "Lost",
        "Retired",
        "Asset Value Indicators"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 82 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected equipment asset",
       "bindsTo": null,
       "columns": [
        "Total assets",
        "Available",
        "Reserved",
        "Checked out",
        "In use",
        "Due for return",
        "Overdue",
        "Under maintenance",
        "Inspection due",
        "Damaged",
        "Lost",
        "Retired",
        "Asset Value Indicators"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Users shall view resources by”, “Users may initiate”.",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 82 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "banner",
       "label": "Permissions this screen separates",
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** Total asset value, Replacement value, Depreciated value, Maintenance cost, Lost/damaged value. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 82 §Where financial permissions allow"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The equipment asset list.",
   "error": "Could not load. Names which read failed and leaves the equipment asset untouched.",
   "emptyFirstRun": "No equipment asset yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the equipment asset are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listResources",
    "contract": "resources",
    "purpose": "Equipment and assets",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listAssets",
    "contract": "maintenance",
    "purpose": "The asset register",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Total assets",
    "Available",
    "Reserved",
    "Checked out",
    "In use",
    "Due for return"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-903",
   "workshopBoard": "wireframes/WS131 Resource Management Configuration Board 6.dc.html#bo-903"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 82. 0 of 13 labels bound to a contract property; 18 of 41 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-904",
  "name": "Rental Resource Configuration",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "6",
   "number": "02",
   "page": 83
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/rental-resource-configuration-bo-904",
   "component": "apps/venue-management-web/src/routes/rentals/RentalResourceConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-903"
   ],
   "exitTo": [
    "BO-903"
   ],
   "transitions": [
    {
     "to": "BO-903",
     "trigger": "Back to Equipment & Asset Command Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Administrators shall configure; Configure) and no display directory — it is settings, not a population",
  "purpose": "Define how a physical resource behaves when offered as a customer-rental resource.",
  "purposeNote": "Administrators can define how each physical resource or resource category behaves throughout the rental process.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Rental enabled",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 83 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Rental item/resource type",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 83 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Rental duration",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 83 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Minimum duration",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 83 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum duration",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 83 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Rental increments",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 83 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Same-day return required",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 83 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Overnight rental permitted",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 83 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Extension permitted",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 83 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum extension",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 83 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Advance reservation permitted",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 83 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Walk-in rental permitted",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 83 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Customer eligibility",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 83 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Venue availability",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 83 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Quantity Model",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 83 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Expected return time",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 83 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Grace period",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 83 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Late-return policy",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 83 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Automatic overdue status",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 83 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Return venue",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 83 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Cross-venue return allowed",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 83 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Inspection required",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 83 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Channel Rules",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 83 §Configure"
      },
      {
       "kind": "selectField",
       "label": "POS",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 83 §Configure"
      },
      {
       "kind": "selectField",
       "label": "B2C",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 83 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Mobile App",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 83 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Kiosk",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 83 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Employee App",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 83 §Configure"
      },
      {
       "kind": "selectField",
       "label": "API",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 83 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The rental resource configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the rental resource untouched.",
   "emptyFirstRun": "No rental resource configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "getRentalProduct",
    "contract": "rental",
    "purpose": "The rental product behind the resource",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "setRentalInventoryModel",
    "contract": "rental",
    "purpose": "Pooled, serialised or hybrid",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getRentalProduct",
     "getRentalAvailability"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-904",
   "workshopBoard": "wireframes/WS131 Resource Management Configuration Board 6.dc.html#bo-904"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 83. 0 of 0 labels bound to a contract property; 29 of 40 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "productId",
     "from": "navigation"
    }
   ]
  },
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
  "id": "BO-905",
  "name": "Rental Inventory & Availability Control",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "6",
   "number": "03",
   "page": 84
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/rental-inventory-availability-control-bo-905",
   "component": "apps/venue-management-web/src/routes/rentals/RentalInventoryAvailabilityControl.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-903"
   ],
   "exitTo": [
    "BO-903"
   ],
   "transitions": [
    {
     "to": "BO-903",
     "trigger": "Back to Equipment & Asset Command Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Administrators shall configure) and no display directory — it is settings, not a population",
  "purpose": "Provide real-time inventory visibility for rental and operational resources.",
  "purposeNote": "before they impact customer operations.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Minimum available quantity",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 84 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Reorder/transfer threshold",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 84 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Critical threshold",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 84 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum quantity",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 84 §Administrators shall configure"
      },
      {
       "kind": "selectField",
       "label": "Smart Alerts",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 84 §Administrators shall configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The rental inventory availability configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the rental inventory availability untouched.",
   "emptyFirstRun": "No rental inventory availability configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "getRentalAvailability",
    "contract": "rental",
    "purpose": "What is free, with turnaround subtracted",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "setRentalAvailabilityRules",
    "contract": "rental",
    "purpose": "Buffers and release rules",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getRentalAvailability"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-905",
   "workshopBoard": "wireframes/WS131 Resource Management Configuration Board 6.dc.html#bo-905"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 84. 0 of 0 labels bound to a contract property; 5 of 34 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "productId",
     "from": "navigation"
    }
   ]
  },
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
  "id": "BO-906",
  "name": "Resource Checkout Workspace",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "6",
   "number": "04",
   "page": 85
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/resource-checkout-workspace-bo-906",
   "component": "apps/venue-management-web/src/routes/rentals/ResourceCheckoutWorkspace.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-903"
   ],
   "exitTo": [
    "BO-903"
   ],
   "transitions": [
    {
     "to": "BO-903",
     "trigger": "Back to Equipment & Asset Command Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population",
  "purpose": "Provide frontline employees with a fast digital interface for issuing physical resources to guests.",
  "purposeNote": "Frontline employees can issue a resource to a guest through a fast scan-driven workflow, and resource availability updates immediately.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Resource",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 85 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Guest",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 85 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Checkout time",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 85 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Expected return",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 85 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Rental duration",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 85 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 85 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Rental station",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 85 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Employee",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 85 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Condition at checkout",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 85 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Deposit",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 85 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Notes",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 85 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Fast Checkout",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 85 §Capture"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The resource checkout configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the resource checkout untouched.",
   "emptyFirstRun": "No resource checkout configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "checkOutRental",
    "contract": "rental",
    "purpose": "Hand it over",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getRentalBooking",
     "listRentalBookings",
     "getRentalAvailability"
    ]
   },
   {
    "operationId": "getRentalBooking",
    "contract": "rental",
    "purpose": "The booking being checked out",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-906",
   "workshopBoard": "wireframes/WS131 Resource Management Configuration Board 6.dc.html#bo-906"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 85. 0 of 0 labels bound to a contract property; 12 of 41 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "bookingId",
     "from": "navigation"
    }
   ]
  },
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
  "id": "BO-907",
  "name": "Guest & Resource Assignment",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "6",
   "number": "05",
   "page": 87
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/guest-resource-assignment-bo-907",
   "component": "apps/venue-management-web/src/routes/rentals/GuestResourceAssignment.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-903"
   ],
   "exitTo": [
    "BO-903"
   ],
   "transitions": [
    {
     "to": "BO-903",
     "trigger": "Back to Equipment & Asset Command Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Maintain a live relationship between every checked-out physical resource and the guest responsible for it.",
  "purposeNote": "Every checked-out tracked resource can be traced to the responsible guest, booking, transaction, and issuing employee.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 87 §Display"
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
       "label": "Every guest resource",
       "columns": [
        "Guest",
        "Photograph where available",
        "Ticket/booking",
        "Membership",
        "Resource",
        "Resource ID",
        "Checkout time",
        "Expected return",
        "Current status",
        "Deposit",
        "Venue",
        "Responsible employee",
        "Guest Resource Timeline"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 87 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected guest resource",
       "bindsTo": null,
       "columns": [
        "Guest",
        "Photograph where available",
        "Ticket/booking",
        "Membership",
        "Resource",
        "Resource ID",
        "Checkout time",
        "Expected return",
        "Current status",
        "Deposit",
        "Venue",
        "Responsible employee",
        "Guest Resource Timeline"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Expected returns”.",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 87 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The guest resource list.",
   "error": "Could not load. Names which read failed and leaves the guest resource untouched.",
   "emptyFirstRun": "No guest resource yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the guest resource are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "assignRentalEquipment",
    "contract": "rental",
    "purpose": "Bind assets to the booking",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getRentalBooking"
    ]
   },
   {
    "operationId": "checkOutResource",
    "contract": "resources",
    "purpose": "Hand the resource over",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Guest",
    "Photograph where available",
    "Ticket/booking",
    "Membership",
    "Resource",
    "Resource ID"
   ],
   "params": [
    {
     "name": "bookingId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-907",
   "workshopBoard": "wireframes/WS131 Resource Management Configuration Board 6.dc.html#bo-907"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 87. 0 of 13 labels bound to a contract property; 21 of 38 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-908",
  "name": "Rental Duration, Extension & Return Management",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "6",
   "number": "06",
   "page": 88
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/rental-duration-extension-return-management-bo-908",
   "component": "apps/venue-management-web/src/routes/rentals/RentalDurationExtensionReturnManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-903"
   ],
   "exitTo": [
    "BO-903"
   ],
   "transitions": [
    {
     "to": "BO-903",
     "trigger": "Back to Equipment & Asset Command Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Control rental periods and manage extensions, overdue items, and returns.",
  "purposeNote": "and final return.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 88 §Display"
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
       "label": "Every rental duration extension",
       "columns": [
        "Resource",
        "Guest",
        "Checkout",
        "Due time",
        "Remaining time",
        "Status",
        "Deposit",
        "Extension eligibility",
        "Status Indicators",
        "Active",
        "Due Soon",
        "Overdue",
        "Extended",
        "Return Pending",
        "Returned",
        "Extension"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 88 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected rental duration extension",
       "bindsTo": null,
       "columns": [
        "Resource",
        "Guest",
        "Checkout",
        "Due time",
        "Remaining time",
        "Status",
        "Deposit",
        "Extension eligibility",
        "Status Indicators",
        "Active",
        "Due Soon",
        "Overdue",
        "Extended",
        "Return Pending",
        "Returned",
        "Extension"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Extend Rental”, “On return”, “Possible next status”, “Overdue Management”.",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 88 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The rental duration extension list.",
   "error": "Could not load. Names which read failed and leaves the rental duration extension untouched.",
   "emptyFirstRun": "No rental duration extension yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the rental duration extension are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "extendRental",
    "contract": "rental",
    "purpose": "Keep it longer",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getRentalBooking",
     "getRentalAvailability"
    ]
   },
   {
    "operationId": "returnRental",
    "contract": "rental",
    "purpose": "Take it back and settle",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getRentalBooking",
     "listRentalBookings",
     "getRentalAvailability",
     "listOverdueRentals"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "Resource",
    "Guest",
    "Checkout",
    "Due time",
    "Remaining time",
    "Status"
   ],
   "params": [
    {
     "name": "bookingId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-908",
   "workshopBoard": "wireframes/WS131 Resource Management Configuration Board 6.dc.html#bo-908"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 88. 0 of 16 labels bound to a contract property; 16 of 40 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-909",
  "name": "Deposit & Rental Financial Control",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "6",
   "number": "07",
   "page": 89
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/deposit-rental-financial-control-bo-909",
   "component": "apps/venue-management-web/src/routes/rentals/DepositRentalFinancialControl.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-903"
   ],
   "exitTo": [
    "BO-903"
   ],
   "transitions": [
    {
     "to": "BO-903",
     "trigger": "Back to Equipment & Asset Command Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Track) and no metric row",
  "purpose": "Configure and manage deposits associated with rental resources.",
  "purposeNote": "Deposits are collected, held, adjusted, and returned according to configurable rental policies with complete financial traceability.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 89 §Track"
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
       "label": "Every deposit rental financial",
       "columns": [
        "Required",
        "Collected",
        "Authorized",
        "Held",
        "Partially retained",
        "Returned",
        "Forfeited",
        "Return Decision"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 89 §Track"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected deposit rental financial",
       "bindsTo": null,
       "columns": [
        "Required",
        "Collected",
        "Authorized",
        "Held",
        "Partially retained",
        "Returned",
        "Forfeited",
        "Return Decision"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Stroller”, “Premium Camera”, “Collection Methods”, “Upon resource return”, “Governance”, “Finance Integration”.",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 89 §Track"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The deposit rental financial list.",
   "error": "Could not load. Names which read failed and leaves the deposit rental financial untouched.",
   "emptyFirstRun": "No deposit rental financial yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the deposit rental financial are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setRentalDepositPolicy",
    "contract": "rental",
    "purpose": "How much is held, and how",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listRentalPricingProfiles"
    ]
   },
   {
    "operationId": "setRentalFeePolicy",
    "contract": "rental",
    "purpose": "Grace period and late fees",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listRentalPricingProfiles"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "Required",
    "Collected",
    "Authorized",
    "Held",
    "Partially retained",
    "Returned"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-909",
   "workshopBoard": "wireframes/WS131 Resource Management Configuration Board 6.dc.html#bo-909"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 89. 0 of 8 labels bound to a contract property; 16 of 44 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-910",
  "name": "Maintenance & Resource Blocking",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "6",
   "number": "08",
   "page": 91
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/maintenance-resource-blocking-bo-910",
   "component": "apps/venue-management-web/src/routes/rentals/MaintenanceResourceBlocking.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-903"
   ],
   "exitTo": [
    "BO-903"
   ],
   "transitions": [
    {
     "to": "BO-903",
     "trigger": "Back to Equipment & Asset Command Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population",
  "purpose": "Prevent unavailable or unsafe resources from being assigned, rented, or reserved.",
  "purposeNote": "Resources under maintenance are automatically removed from operational availability and affected future assignments are identified immediately.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Resource",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 91 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Maintenance type",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 91 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Issue",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 91 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Severity",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 91 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Start date/time",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 91 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Expected completion",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 91 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Actual completion",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 91 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Technician/vendor",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 91 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Cost",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 91 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Attachments",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 91 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Notes",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 91 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Automatic Blocking",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 91 §Capture"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Manufacturer service",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 91 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The maintenance resource blocking configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the maintenance resource blocking untouched.",
   "emptyFirstRun": "No maintenance resource blocking configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist"
  },
  "apis": [
   {
    "operationId": "createResourceBlock",
    "contract": "resources",
    "purpose": "Take it out of service",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listResourceBlocks",
     "getResourceCalendar"
    ]
   },
   {
    "operationId": "createWorkOrder",
    "contract": "maintenance",
    "purpose": "Raise the repair",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listWorkOrders",
     "getDueMaintenance"
    ]
   },
   {
    "operationId": "getDueMaintenance",
    "contract": "maintenance",
    "purpose": "What is due",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-910",
   "workshopBoard": "wireframes/WS131 Resource Management Configuration Board 6.dc.html#bo-910"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 91. 0 of 0 labels bound to a contract property; 13 of 32 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Manufacturer service are choices sent by `createWorkOrder` (planned work order assigned to the manufacturer (resolution referredExternal)).",
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
  "id": "BO-911",
  "name": "Inspection, Condition & Compliance Management",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "6",
   "number": "09",
   "page": 92
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/inspection-condition-compliance-management-bo-911",
   "component": "apps/venue-management-web/src/routes/rentals/InspectionConditionComplianceManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-903"
   ],
   "exitTo": [
    "BO-903"
   ],
   "transitions": [
    {
     "to": "BO-903",
     "trigger": "Back to Equipment & Asset Command Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Track) and no metric row",
  "purpose": "Ensure physical resources remain safe, compliant, and operationally fit for use.",
  "purposeNote": "resources from operational use.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 92 §Track"
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
       "label": "Every inspection condition compliance",
       "columns": [
        "Last inspection",
        "Next inspection",
        "Inspection frequency",
        "Responsible person",
        "Compliance status",
        "Automatic Status"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 92 §Track"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected inspection condition compliance",
       "bindsTo": null,
       "columns": [
        "Last inspection",
        "Next inspection",
        "Inspection frequency",
        "Responsible person",
        "Compliance status",
        "Automatic Status"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Inspection Templates”, “Stroller Return Inspection”, “AV Equipment Inspection”, “Users may attach”.",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 92 §Track"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Passed with Observation",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 92 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Failed",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 92 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Evidence",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 92 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The inspection condition compliance list.",
   "error": "Could not load. Names which read failed and leaves the inspection condition compliance untouched.",
   "emptyFirstRun": "No inspection condition compliance yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the inspection condition compliance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "recordRentalInspection",
    "contract": "rental",
    "purpose": "Condition, with evidence",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getRentalBooking"
    ]
   },
   {
    "operationId": "submitInspection",
    "contract": "maintenance",
    "purpose": "The maintenance inspection",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listInspections",
    "contract": "maintenance",
    "purpose": "Inspections so far",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Last inspection",
    "Next inspection",
    "Inspection frequency",
    "Responsible person",
    "Compliance status",
    "Automatic Status"
   ],
   "params": [
    {
     "name": "bookingId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-911",
   "workshopBoard": "wireframes/WS131 Resource Management Configuration Board 6.dc.html#bo-911"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 92. 0 of 6 labels bound to a contract property; 9 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Passed with Observation, Failed, Evidence are choices sent by `submitInspection` (responses[].passed + note (passed with observation / failed), attachmentRefs (evidence)).",
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
  "id": "BO-912",
  "name": "Asset Lifecycle, Depreciation & Retirement",
  "module": "Rentals",
  "requiresModule": "resources",
  "wave": 3,
  "source": {
   "pack": "Resource_Management_Configuration_Reference.pdf",
   "board": "6",
   "number": "10",
   "page": 93
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/rentals/asset-lifecycle-depreciation-retirement-bo-912",
   "component": "apps/venue-management-web/src/routes/rentals/AssetLifecycleDepreciationRetirement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-903"
   ],
   "exitTo": [
    "BO-903"
   ],
   "transitions": [
    {
     "to": "BO-903",
     "trigger": "Back to Equipment & Asset Command Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Track) and no metric row",
  "purpose": "Manage the physical resource from acquisition through operational use to final retirement. Provide TICVAI with a centralized Event Resource Planning Engine that allows event managers and operations teams to define everything required to deliver an event and convert those requirements into actual resource reservations and assignments. The board shall manage event requirements across: Venues Auditoriums Halls Rooms Stages Breakout areas Outdoor areas AV systems Lighting Sound systems Projectors Screens Chairs Tables Booths Operational equipment Event managers Ushers Security Technical crew Hosts Performers Mascots Temporary staff Other configurable resources",
  "purposeNote": "retirement, including operational history, maintenance, condition, value references, and governance. Board 6 Shared Digital Resource Journey A physical resource should have a complete digital operational history.",
  "gaps": [
   {
    "operation": null,
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Resource_Management_Configuration_Reference.pdf, page 93 §Track"
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
       "label": "Every asset lifecycle depreciation",
       "columns": [
        "Acquisition date",
        "Purchase cost",
        "Supplier",
        "Warranty",
        "Expected useful life",
        "Replacement value",
        "Current book/reference value",
        "Depreciation method",
        "Depreciation period",
        "Maintenance history",
        "Utilization",
        "Condition",
        "Depreciation",
        "Straight-line depreciation",
        "Configurable financial method",
        "Accumulated depreciation",
        "Current value"
       ],
       "bindsTo": null,
       "operation": null,
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 93 §Track"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected asset lifecycle depreciation",
       "bindsTo": null,
       "columns": [
        "Acquisition date",
        "Purchase cost",
        "Supplier",
        "Warranty",
        "Expected useful life",
        "Replacement value",
        "Current book/reference value",
        "Depreciation method",
        "Depreciation period",
        "Maintenance history",
        "Utilization",
        "Condition",
        "Depreciation",
        "Straight-line depreciation",
        "Configurable financial method",
        "Accumulated depreciation",
        "Current value"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Retirement Assessment”, “Projector P-17”, “Retirement may require”, “Stroller S-084”, “Typical operational states include”, “Board 6 shall integrate with”.",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 93 §Track"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "→ End of Life",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 93 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Asset Information",
       "provenance": "pack Resource_Management_Configuration_Reference.pdf, page 93 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The asset lifecycle depreciation list.",
   "error": "Could not load. Names which read failed and leaves the asset lifecycle depreciation untouched.",
   "emptyFirstRun": "No asset lifecycle depreciation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the asset lifecycle depreciation are still there. The pack's own statuses are deliver this event? — the state names which is selected.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setResourceLifecycleState",
    "contract": "resources",
    "purpose": "Retire or archive it",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "getResource",
     "listResources",
     "getResourceAuditTrail"
    ]
   },
   {
    "operationId": "getAssetHistory",
    "contract": "maintenance",
    "purpose": "Its life so far",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "Acquisition date",
    "Purchase cost",
    "Supplier",
    "Warranty",
    "Expected useful life",
    "Replacement value"
   ],
   "params": [
    {
     "name": "assetId",
     "from": "navigation"
    },
    {
     "name": "resourceId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-912",
   "workshopBoard": "wireframes/WS131 Resource Management Configuration Board 6.dc.html#bo-912"
  },
  "apisNote": "Regenerated 9 September 2026 from Resource_Management_Configuration_Reference.pdf page 93. 0 of 17 labels bound to a contract property; 25 of 188 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** → End of Life are choices sent by `setResourceLifecycleState` (state retired with disposal); Asset Information dropped (section heading).",
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
 "assignRentalEquipment": {
  "method": "POST",
  "path": "/rental-bookings/{bookingId}/equipment",
  "contract": "rental",
  "summary": "Bind specific assets to the booking, by scan where required",
  "permission": "RENTAL_OPERATE",
  "offlineCapable": true,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "RentalEquipmentAssignment"
 },
 "checkOutRental": {
  "method": "POST",
  "path": "/rental-bookings/{bookingId}/check-out",
  "contract": "rental",
  "summary": "Hand it over, with the deposit held and the condition recorded",
  "permission": "RENTAL_OPERATE",
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
  "requestBody": "RentalCheckOut",
  "responds": "RentalBooking"
 },
 "checkOutResource": {
  "method": "POST",
  "path": "/resource-bookings/{bookingId}/check-out",
  "contract": "resources",
  "summary": "Hand it over, with a deposit against it",
  "permission": "RESOURCE_BOOK",
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
  "responds": "ResourceBooking"
 },
 "createResourceBlock": {
  "method": "POST",
  "path": "/resource-blocks",
  "contract": "resources",
  "summary": "Take a resource out of service for a window, with a reason",
  "permission": "RESOURCE_MANAGE",
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
  "requestBody": "ResourceBlock",
  "responds": "ResourceBlock"
 },
 "createWorkOrder": {
  "method": "POST",
  "path": "/work-orders",
  "contract": "maintenance",
  "summary": "Raise a work order",
  "permission": "WORK_ORDER_MANAGE",
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
  "requestBody": "CreateWorkOrderRequest",
  "responds": "WorkOrder"
 },
 "extendRental": {
  "method": "POST",
  "path": "/rental-bookings/{bookingId}/extend",
  "contract": "rental",
  "summary": "Keep it longer, if it is free and the guest accepts the price",
  "permission": "RENTAL_OPERATE",
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
  "requestBody": null,
  "responds": "RentalBooking"
 },
 "getAssetHistory": {
  "method": "GET",
  "path": "/assets/{assetId}/history",
  "contract": "maintenance",
  "summary": "Service history",
  "permission": "ASSET_VIEW",
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
 "getDueMaintenance": {
  "method": "GET",
  "path": "/maintenance-plans/due",
  "contract": "maintenance",
  "summary": "Planned tasks due or overdue",
  "permission": "ASSET_VIEW",
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
    "name": "withinDays",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "DueMaintenanceTask"
 },
 "getRentalAvailability": {
  "method": "GET",
  "path": "/rental-availability",
  "contract": "rental",
  "summary": "What can be rented, when, with turnaround already subtracted",
  "permission": "RENTAL_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "productId",
    "in": "query",
    "required": true
   },
   {
    "name": "locationId",
    "in": "query",
    "required": null
   },
   {
    "name": "from",
    "in": "query",
    "required": true
   },
   {
    "name": "to",
    "in": "query",
    "required": true
   },
   {
    "name": "quantity",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "RentalAvailability"
 },
 "getRentalBooking": {
  "method": "GET",
  "path": "/rental-bookings/{bookingId}",
  "contract": "rental",
  "summary": "One booking, its timeline and its readiness",
  "permission": "RENTAL_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "RentalBooking"
 },
 "getRentalProduct": {
  "method": "GET",
  "path": "/rental-products/{productId}",
  "contract": "rental",
  "summary": "The master configuration of one rental product",
  "permission": "RENTAL_VIEW",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "RentalProduct"
 },
 "listAssets": {
  "method": "GET",
  "path": "/assets",
  "contract": "maintenance",
  "summary": "List assets",
  "permission": "ASSET_VIEW",
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
    "name": "categoryId",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "maintenanceDue",
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
 "listInspections": {
  "method": "GET",
  "path": "/inspections",
  "contract": "maintenance",
  "summary": "List completed inspections",
  "permission": "INSPECTION_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "templateId",
    "in": "query",
    "required": null
   },
   {
    "name": "assetId",
    "in": "query",
    "required": null
   },
   {
    "name": "outcome",
    "in": "query",
    "required": null
   },
   {
    "name": "performedFrom",
    "in": "query",
    "required": null
   },
   {
    "name": "performedTo",
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
 "listResources": {
  "method": "GET",
  "path": "/resources",
  "contract": "resources",
  "summary": "Resources at this venue",
  "permission": "RESOURCE_VIEW",
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
    "name": "availableFrom",
    "in": "query",
    "required": null
   },
   {
    "name": "availableTo",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Resource"
 },
 "recordRentalInspection": {
  "method": "POST",
  "path": "/rental-bookings/{bookingId}/inspection",
  "contract": "rental",
  "summary": "Condition before or after, with evidence",
  "permission": "RENTAL_OPERATE",
  "offlineCapable": true,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "RentalInspection",
  "responds": "RentalInspection"
 },
 "returnRental": {
  "method": "POST",
  "path": "/rental-bookings/{bookingId}/return",
  "contract": "rental",
  "summary": "Take it back, inspect it, and settle everything at once",
  "permission": "RENTAL_OPERATE",
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
  "requestBody": "RentalReturn",
  "responds": "RentalSettlement"
 },
 "setRentalAvailabilityRules": {
  "method": "PUT",
  "path": "/rental-products/{productId}/availability-rules",
  "contract": "rental",
  "summary": "Operating hours, rental windows, buffers and release rules",
  "permission": "RENTAL_CONFIGURE",
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
  "requestBody": "RentalAvailabilityRules",
  "responds": "RentalAvailabilityRules"
 },
 "setRentalDepositPolicy": {
  "method": "PUT",
  "path": "/rental-deposit-policies",
  "contract": "rental",
  "summary": "How much is held, how, and what happens to it",
  "permission": "RENTAL_PRICE",
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
  "requestBody": "RentalDepositPolicy",
  "responds": "RentalDepositPolicy"
 },
 "setRentalFeePolicy": {
  "method": "PUT",
  "path": "/rental-fee-policies",
  "contract": "rental",
  "summary": "Grace period, late fees and extension pricing",
  "permission": "RENTAL_PRICE",
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
  "requestBody": "RentalFeePolicy",
  "responds": "RentalFeePolicy"
 },
 "setRentalInventoryModel": {
  "method": "PUT",
  "path": "/rental-products/{productId}/inventory-model",
  "contract": "rental",
  "summary": "Pooled, serialised or hybrid",
  "permission": "RENTAL_CONFIGURE",
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
  "requestBody": "RentalInventoryModel",
  "responds": "RentalInventoryModel"
 },
 "setResourceLifecycleState": {
  "method": "POST",
  "path": "/resources/{resourceId}/state",
  "contract": "resources",
  "summary": "Move a resource through its lifecycle, with a reason",
  "permission": "RESOURCE_MANAGE",
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
  "responds": "Resource"
 },
 "submitInspection": {
  "method": "POST",
  "path": "/inspections",
  "contract": "maintenance",
  "summary": "Submit a completed inspection",
  "permission": "INSPECTION_SUBMIT",
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
  "requestBody": "SubmitInspectionRequest",
  "responds": "InspectionResult"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AssetCriticality": {
  "type": "string",
  "enum": [
   "safetyCritical",
   "revenueCritical",
   "standard",
   "low"
  ]
 },
 "CreateWorkOrderRequest": {
  "x-ticvai-persistence": "none — request only",
  "type": "object",
  "required": [
   "id",
   "title",
   "venueId",
   "priority",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "title": {
    "type": "string",
    "maxLength": 200
   },
   "description": {
    "type": "string",
    "maxLength": 5000
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "assetId": {
    "type": "string",
    "format": "uuid"
   },
   "locationDescription": {
    "type": "string",
    "maxLength": 500
   },
   "kind": {
    "allOf": [
     {
      "$ref": "#/components/schemas/WorkOrderKind"
     }
    ],
    "default": "corrective"
   },
   "priority": {
    "$ref": "#/components/schemas/WorkOrderPriority"
   },
   "categoryId": {
    "type": "string",
    "format": "uuid"
   },
   "assignedToPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "dueAt": {
    "type": "string",
    "format": "date-time"
   },
   "attachmentRefs": {
    "type": "array",
    "description": "Photo-first. Expected at creation, not added later from memory.",
    "items": {
     "type": "string"
    }
   },
   "takeAssetOutOfService": {
    "type": "boolean",
    "default": false,
    "description": "Raise and immediately suspend the asset. For a fault found on a live ride, the two are one action.\n"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "DueMaintenanceTask": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "planId",
   "assetId",
   "assetName",
   "dueAt",
   "isOverdue",
   "criticality"
  ],
  "properties": {
   "planId": {
    "type": "string",
    "format": "uuid"
   },
   "planName": {
    "type": "string"
   },
   "assetId": {
    "type": "string",
    "format": "uuid"
   },
   "assetName": {
    "type": "string"
   },
   "criticality": {
    "$ref": "#/components/schemas/AssetCriticality"
   },
   "dueAt": {
    "type": "string",
    "format": "date-time"
   },
   "isOverdue": {
    "type": "boolean"
   },
   "daysOverdue": {
    "type": "integer"
   },
   "triggeredBy": {
    "type": "string",
    "enum": [
     "interval",
     "usage"
    ]
   },
   "workOrderId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "nullable": true
   }
  }
 },
 "Inspection": {
  "x-ticvai-persistence": "maintenance.inspection",
  "type": "object",
  "required": [
   "id",
   "templateId",
   "venueId",
   "outcome",
   "performedByPrincipalId",
   "performedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "templateId": {
    "type": "string",
    "format": "uuid"
   },
   "templateName": {
    "type": "string"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "assetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "outcome": {
    "$ref": "#/components/schemas/InspectionOutcome"
   },
   "failedItemCount": {
    "type": "integer"
   },
   "failedSafetyCriticalCount": {
    "type": "integer"
   },
   "performedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "description": "An inspection nobody signed is not an inspection."
   },
   "performedAt": {
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
   },
   "retainUntil": {
    "type": "string",
    "format": "date",
    "nullable": true
   }
  }
 },
 "InspectionItem": {
  "x-ticvai-persistence": "maintenance.inspection_item",
  "type": "object",
  "description": "**One answer to one question, which the API has always accepted and never stored.** `SubmitInspectionRequest.responses[]` takes a key, a value, a pass flag, a note and attachments; the only persistence ever claimed for them was `maintenance.inspection_response`, a table that does not exist.\nSo `maintenance.inspection_template_item` held the questions, `maintenance.inspection` held `failedItemCount` and `failedSafetyCriticalCount`, and **which check failed was accepted over the wire and dropped** — on a record that takes an asset out of service.\nReturned on `InspectionResult`, not on `Inspection`: `listInspections` returns the latter in a list, and twenty item rows per inspection on a list screen is the wrong trade. The counts stay for exactly that reason.\n",
  "required": [
   "id",
   "inspectionId",
   "itemKey"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "inspectionId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "templateItemId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**Nullable because a template changes and an inspection does not.** An answer recorded against an item that was later removed still has to be readable, so the key below is the durable record and this is the live link.\n"
   },
   "itemKey": {
    "type": "string",
    "maxLength": 120,
    "description": "The template item's `key`, copied at submission and never updated."
   },
   "label": {
    "type": "string",
    "nullable": true,
    "description": "The question as it was asked, copied at submission. **A template reworded next season must not silently reword last season's inspection.**\n"
   },
   "value": {
    "nullable": true,
    "description": "Whatever the item's `kind` calls for — a boolean, a number, a string."
   },
   "passed": {
    "type": "boolean",
    "nullable": true,
    "description": "Null where the item is informational rather than pass or fail."
   },
   "isSafetyCritical": {
    "type": "boolean",
    "default": false,
    "description": "Copied from the template item at submission, for the same reason as `label`: it is what makes `failedSafetyCriticalCount` reproducible, and the template can change.\n"
   },
   "note": {
    "type": "string",
    "maxLength": 1000,
    "nullable": true
   },
   "attachmentAssetIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "**A deliberate array, and the same exception as `workforce.sync_conflict.affectedAssignmentIds`**: evidence attached to this answer at the moment it was recorded. It is never queried from the other end — nobody asks which inspection items reference a photograph — and it must not change when an asset library is reorganised.\n"
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "InspectionResult": {
  "x-ticvai-persistence": "none — computed",
  "type": "object",
  "required": [
   "inspection",
   "consequences"
  ],
  "properties": {
   "inspection": {
    "$ref": "#/components/schemas/Inspection"
   },
   "items": {
    "type": "array",
    "description": "**The answers, which had nowhere to live until 20 September.** A failed safety-critical item takes an asset out of service and `consequences` below says it happened; this says which check caused it.\n",
    "items": {
     "$ref": "#/components/schemas/InspectionItem"
    }
   },
   "consequences": {
    "type": "object",
    "description": "What the submission triggered. A failed safety-critical item takes the asset out of service without waiting for anyone to decide.\n",
    "properties": {
     "assetTakenOutOfService": {
      "type": "boolean"
     },
     "workOrdersRaised": {
      "type": "array",
      "items": {
       "type": "string",
       "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
      }
     },
     "productsSuspended": {
      "type": "array",
      "items": {
       "type": "string",
       "format": "uuid"
      }
     },
     "escalatedToPrincipalId": {
      "type": "string",
      "format": "uuid",
      "nullable": true
     }
    }
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
 "RentalAvailability": {
  "type": "object",
  "description": "Board 3. **A pooled product answers with a count, a serialised one with assets.**",
  "properties": {
   "productId": {
    "type": "string",
    "format": "uuid"
   },
   "locationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "windows": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "from": {
       "type": "string",
       "format": "date-time"
      },
      "to": {
       "type": "string",
       "format": "date-time"
      },
      "availableQuantity": {
       "type": "integer"
      },
      "availableAssetIds": {
       "type": "array",
       "items": {
        "type": "string",
        "format": "uuid"
       }
      }
     }
    }
   },
   "blockedWindows": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "from": {
       "type": "string",
       "format": "date-time"
      },
      "to": {
       "type": "string",
       "format": "date-time"
      },
      "reason": {
       "type": "string",
       "enum": [
        "booked",
        "turnaround",
        "maintenance",
        "blackout",
        "closed",
        "buffer",
        "held"
       ]
      }
     }
    }
   }
  }
 },
 "RentalAvailabilityRules": {
  "type": "object",
  "x-ticvai-persistence": "rental.availability_rules",
  "description": "Boards 3.2, 3.3 and 3.9. **The hold-release rule is the one that quietly loses stock.**\n",
  "properties": {
   "operatingWindows": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
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
      }
     }
    }
   },
   "slotMinutes": {
    "type": "integer",
    "nullable": true
   },
   "holdMinutes": {
    "type": "integer",
    "default": 15,
    "description": "**How long an unconfirmed basket keeps stock.** A hold that never expires removes inventory from sale after every abandoned checkout.\n"
   },
   "releaseOnPaymentFailure": {
    "type": "boolean",
    "default": true
   },
   "overbookPercent": {
    "type": "number",
    "default": 0
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "RentalBooking": {
  "type": "object",
  "x-ticvai-persistence": "rental.booking",
  "description": "Board 5. **The booking outlives the order** — an order completes at payment and the rental is still out.\n",
  "required": [
   "id",
   "productId",
   "from",
   "to",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "reference": {
    "type": "string"
   },
   "productId": {
    "type": "string",
    "format": "uuid"
   },
   "locationId": {
    "type": "string",
    "format": "uuid"
   },
   "returnLocationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "customerId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "orderId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "from": {
    "type": "string",
    "format": "date-time"
   },
   "to": {
    "type": "string",
    "format": "date-time"
   },
   "quantity": {
    "type": "integer"
   },
   "status": {
    "type": "string",
    "enum": [
     "draft",
     "confirmed",
     "awaitingArrival",
     "checkedOut",
     "overdue",
     "partiallyReturned",
     "completed",
     "completedWithDamage",
     "notReturned",
     "cancelled",
     "noShow"
    ]
   },
   "checkedOutAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "dueBackAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "returnedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "depositAuthorisationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "accruedLateFee": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "readiness": {
    "type": "array",
    "readOnly": true,
    "description": "**Computed, not stored** — agreement, requirements, deposit, equipment.",
    "items": {
     "type": "object",
     "properties": {
      "check": {
       "type": "string"
      },
      "satisfied": {
       "type": "boolean"
      },
      "detail": {
       "type": "string",
       "nullable": true
      }
     }
    }
   },
   "participants": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/RentalParticipant"
    }
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "RentalCheckOut": {
  "type": "object",
  "description": "Board 6. **The readiness gate is enforced server-side.**",
  "properties": {
   "depositAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "depositInstrument": {
    "type": "string",
    "nullable": true
   },
   "conditionNote": {
    "type": "string",
    "nullable": true
   },
   "photoAssetIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "safetyBriefingGiven": {
    "type": "boolean",
    "default": false
   },
   "dueBackAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "overrideId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**A supervisor override for a failed precondition**, which is recorded rather than allowed silently.\n"
   }
  }
 },
 "RentalDamageAssessment": {
  "type": "object",
  "x-ticvai-persistence": "rental.damage_assessment",
  "description": "Board 8.6. **A dispute is a state, not a deletion.**",
  "required": [
   "amount",
   "description"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "assetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "description": {
    "type": "string"
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "inspectionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "assessedBy": {
    "type": "string",
    "format": "uuid"
   },
   "approvedBy": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "customerAcknowledgement": {
    "type": "string",
    "enum": [
     "accepted",
     "disputed",
     "notPresented"
    ],
    "default": "notPresented"
   },
   "workOrderId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Raised in `maintenance`, so the repair is tracked where every other repair is."
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "RentalDepositPolicy": {
  "type": "object",
  "x-ticvai-persistence": "rental.deposit_policy",
  "description": "Boards 4.6 and 4.7. **Held, not taken**, and settled against an inspection.",
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "productId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "categoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "required": {
    "type": "boolean",
    "default": true
   },
   "basis": {
    "type": "string",
    "enum": [
     "fixed",
     "percentage",
     "riskBased"
    ]
   },
   "fixedAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "percentage": {
    "type": "number",
    "nullable": true
   },
   "minimumAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "maximumAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "instruments": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "cardPreAuthorisation",
      "cardCharge",
      "cash",
      "wallet"
     ]
    }
   },
   "autoRelease": {
    "type": "boolean",
    "default": true
   },
   "inspectionRequiredBeforeRelease": {
    "type": "boolean",
    "default": false
   },
   "autoReleaseDelayHours": {
    "type": "integer",
    "default": 0
   },
   "partialCapturePermitted": {
    "type": "boolean",
    "default": true
   },
   "supervisorApprovalThreshold": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "waiverEligible": {
    "type": "boolean",
    "default": false
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "RentalEquipmentAssignment": {
  "type": "object",
  "x-ticvai-persistence": "rental.equipment_assignment",
  "description": "Board 6.4. **The moment a serialised rental stops being a quantity.**",
  "required": [
   "assetId"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "assetId": {
    "type": "string",
    "format": "uuid",
    "description": "A `maintenance.Asset`, which is also a `resources` resource where the product is schedule-controlled."
   },
   "serialNumber": {
    "type": "string",
    "nullable": true
   },
   "scannedCode": {
    "type": "string",
    "nullable": true
   },
   "assignedManually": {
    "type": "boolean",
    "default": false
   },
   "assignedAt": {
    "type": "string",
    "format": "date-time"
   },
   "returnedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "RentalFeePolicy": {
  "type": "object",
  "x-ticvai-persistence": "rental.fee_policy",
  "description": "Board 4.8. **Extension is priced below late return on purpose** — *\"this encourages customers to extend properly rather than returning late.\"*\n",
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "productId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "gracePeriodMinutes": {
    "type": "integer",
    "default": 0
   },
   "lateFeeBasis": {
    "type": "string",
    "enum": [
     "fixed",
     "perMinute",
     "per15Minutes",
     "per30Minutes",
     "perHour",
     "tiered"
    ]
   },
   "lateFeeAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "lateFeeTiers": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "afterMinutes": {
       "type": "integer"
      },
      "amount": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      }
     }
    }
   },
   "maximumDailyCharge": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "extensionPricePerIncrement": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "extensionIncrementMinutes": {
    "type": "integer",
    "default": 30
   },
   "notReturnedAfterHours": {
    "type": "integer",
    "nullable": true,
    "description": "**When a late rental becomes a lost one.** The deposit is captured in full and the asset retired; without a threshold the fee accrues forever and nobody decides.\n"
   },
   "damageFeeMaximum": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "**A ceiling, not a rate.** Added 22 September: `rental.settlement.damage_fee` was stored with nothing bounding it. **A dent is assessed, not tabulated** — the amount is entered per incident against the actual damage, so the control is how high an operator may go, the same shape `maximumDailyCharge` already gives the late fee.\n"
   },
   "damageFeeApprovalAbove": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "**Above this, a second person signs it off.** A damage fee is the one charge on a settlement that a single operator decides alone, and the one a guest is most likely to dispute. The shape is `orders.RefundPolicy.requiresApprovalAbove`, applied to the other direction of money.\n"
   },
   "missingItemFeeBasis": {
    "type": "string",
    "enum": [
     "replacementCost",
     "fixedAmount"
    ],
    "description": "**What an unreturned item costs.** `replacementCost` reads the item's own replacement value, which is what the fee usually is; `fixedAmount` uses `missingItemFeeAmount`. Added 22 September — `rental.settlement.missing_item_fee` was stored with no source.\n"
   },
   "missingItemFeeAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Used when `missingItemFeeBasis` is `fixedAmount`."
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "RentalInspection": {
  "type": "object",
  "x-ticvai-persistence": "rental.inspection",
  "description": "Boards 6.5 and 8.4. **Before and after are one record shape with a phase**, which is what makes the comparison view possible.\n",
  "required": [
   "phase",
   "condition"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "assetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "phase": {
    "type": "string",
    "enum": [
     "preRental",
     "postRental"
    ]
   },
   "condition": {
    "type": "string",
    "enum": [
     "good",
     "minorDamage",
     "majorDamage",
     "faulty",
     "notReturned"
    ],
    "description": "**26 August: simplified state attributes.** *\"rental/equipment items can be tracked with simplified state attributes (e.g., available, rented, faulty) rather than requiring granular custom attributes for this category — agreed by Allam.\"* So the condition is a short enum, and anything finer belongs in the note or the photographs.\n"
   },
   "checklist": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "item": {
       "type": "string"
      },
      "passed": {
       "type": "boolean"
      },
      "note": {
       "type": "string",
       "nullable": true
      }
     }
    }
   },
   "note": {
    "type": "string",
    "nullable": true
   },
   "photoAssetIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "inspectedBy": {
    "type": "string",
    "format": "uuid"
   },
   "inspectedAt": {
    "type": "string",
    "format": "date-time"
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "RentalInventoryModel": {
  "type": "object",
  "x-ticvai-persistence": "rental.inventory_model",
  "description": "Board 1.5. **Pooled, serialised or hybrid**, and the switches the counter obeys.",
  "required": [
   "trackingModel"
  ],
  "properties": {
   "trackingModel": {
    "type": "string",
    "enum": [
     "pooled",
     "serialised",
     "hybrid"
    ]
   },
   "inventoryUnit": {
    "type": "string",
    "nullable": true
   },
   "totalQuantity": {
    "type": "integer",
    "nullable": true,
    "description": "Pooled only. *150 lockers.*"
   },
   "components": {
    "type": "array",
    "description": "**Hybrid only** — *one serialised kayak, two pooled paddles, two pooled life jackets.* One booking, two mechanisms.\n",
    "items": {
     "type": "object",
     "properties": {
      "resourceTypeId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "label": {
       "type": "string"
      },
      "quantity": {
       "type": "integer"
      },
      "serialised": {
       "type": "boolean"
      }
     }
    }
   },
   "assignmentRequiredAtCheckout": {
    "type": "boolean",
    "default": false
   },
   "scanRequired": {
    "type": "boolean",
    "default": false
   },
   "allowManualAssignment": {
    "type": "boolean",
    "default": true
   },
   "allowSubstitution": {
    "type": "boolean",
    "default": true
   },
   "allowEquipmentSwap": {
    "type": "boolean",
    "default": true
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "RentalParticipant": {
  "type": "object",
  "x-ticvai-persistence": "rental.participant",
  "description": "Board 5.5. **A group rental is one booking with participants**, because the agreement, the deposit and the return are handled together.\n",
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string"
   },
   "isPrimaryRenter": {
    "type": "boolean",
    "default": false
   },
   "dateOfBirth": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "idNumber": {
    "type": "string",
    "nullable": true
   },
   "guardianName": {
    "type": "string",
    "nullable": true
   },
   "emergencyContact": {
    "type": "string",
    "nullable": true
   },
   "hasSignedWaiver": {
    "type": "boolean",
    "readOnly": true
   },
   "customFields": {
    "type": "object",
    "additionalProperties": true
   }
  }
 },
 "RentalProduct": {
  "type": "object",
  "x-ticvai-persistence": "rental.product",
  "description": "Board 1.3. **The master reference every later board resolves against.**",
  "required": [
   "code",
   "name",
   "venueId"
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
   "internalName": {
    "type": "string",
    "nullable": true
   },
   "description": {
    "type": "string",
    "nullable": true
   },
   "categoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "imageAssetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "tags": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "tenantId": {
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
   "trackingModel": {
    "type": "string",
    "enum": [
     "pooled",
     "serialised",
     "hybrid"
    ]
   },
   "catalogueProductId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**The thing the guest actually buys.** `catalogue` sells it and this configures how it behaves once sold; the link is here so a rental is never sold twice through two different product records.\n"
   },
   "resourceTypeId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**For serialised products, the `resources` type its assets belong to.** The individual bikes are resources and maintenance assets — this contract does not keep a third register of them.\n"
   },
   "status": {
    "type": "string",
    "enum": [
     "draft",
     "configurationReview",
     "approved",
     "active",
     "suspended",
     "archived"
    ]
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "version": {
    "type": "integer",
    "default": 1
   },
   "isActive": {
    "type": "boolean",
    "default": true
   }
  }
 },
 "RentalReturn": {
  "type": "object",
  "description": "Board 8. **Late fee, damage and partial return all land on one deposit.**",
  "required": [
   "returnedAt"
  ],
  "properties": {
   "returnedAt": {
    "type": "string",
    "format": "date-time"
   },
   "returnLocationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "returnedAssetIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "missingAssetIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "inspection": {
    "$ref": "#/components/schemas/RentalInspection"
   },
   "damage": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/RentalDamageAssessment"
    }
   },
   "waiveLateFee": {
    "type": "boolean",
    "default": false
   },
   "overrideId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   }
  }
 },
 "RentalSettlement": {
  "type": "object",
  "x-ticvai-persistence": "rental.settlement",
  "description": "Board 8.8. **One statement, because there is one deposit.** *Capture AED 120, release AED 380.*\n",
  "properties": {
   "bookingId": {
    "type": "string",
    "format": "uuid"
   },
   "expectedReturnAt": {
    "type": "string",
    "format": "date-time"
   },
   "actualReturnAt": {
    "type": "string",
    "format": "date-time"
   },
   "gracePeriodMinutes": {
    "type": "integer"
   },
   "chargeableLateMinutes": {
    "type": "integer"
   },
   "lateFee": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "damageFee": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "missingItemFee": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "totalCharged": {
    "x-ticvai-column": "gross_charged_amount",
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "depositCaptured": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "depositReleased": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "balanceDue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "**Where the charges exceed the deposit.** A bike written off against a AED 200 hold leaves a real debt, and netting it to zero hides it.\n"
   },
   "outcome": {
    "type": "string",
    "enum": [
     "completed",
     "completedWithDamage",
     "partiallyReturned",
     "notReturned"
    ]
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "Resource": {
  "type": "object",
  "x-ticvai-persistence": "resources.resource",
  "description": "**A specific object, not a quantity of interchangeable ones.** A venue with forty identical strollers has forty resources, because guest number twelve returned stroller number twelve.\n",
  "required": [
   "id",
   "code",
   "name",
   "kind",
   "venueId"
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
   "kind": {
    "$ref": "#/components/schemas/ResourceKind"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string"
   },
   "parentResourceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**A pool cabana belongs to the pool area; a seat belongs to an auditorium.** Booking a parent takes its children with it, which is the behaviour a venue expects and would otherwise have to enforce by hand.\n"
   },
   "principalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "For a resource of kind `instructor` or `staff`. **`workforce` still owns their rota** — this says whether they are qualified and whether they are already committed.\n"
   },
   "attributes": {
    "type": "object",
    "additionalProperties": true,
    "description": "Configurable per kind — capacity, size, shade, power, poolside."
   },
   "setupMinutes": {
    "type": "integer",
    "default": 0,
    "description": "**Before the booking, not inside it.** An auditorium booked 14:00–16:00 is unavailable from 13:30 with a 30-minute setup, and a calendar that cannot express that double-books every time.\n"
   },
   "teardownMinutes": {
    "type": "integer",
    "default": 0
   },
   "requiresQualification": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Qualification codes a person must hold to be assigned to this."
   },
   "depositAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "status": {
    "type": "string",
    "enum": [
     "available",
     "booked",
     "checkedOut",
     "maintenance",
     "retired"
    ]
   },
   "isActive": {
    "type": "boolean",
    "default": true
   }
  }
 },
 "ResourceBlock": {
  "type": "object",
  "x-ticvai-persistence": "resources.resource_block",
  "description": "Board 2.07. **A block is not a booking**, and the reason travels with it so an operator knows whether to wait or to look elsewhere.\n",
  "required": [
   "resourceId",
   "from",
   "to",
   "reason"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "resourceId": {
    "type": "string",
    "format": "uuid"
   },
   "from": {
    "type": "string",
    "format": "date-time"
   },
   "to": {
    "type": "string",
    "format": "date-time"
   },
   "reason": {
    "type": "string",
    "enum": [
     "setup",
     "teardown",
     "maintenance",
     "blackout",
     "closed",
     "operational",
     "training"
    ]
   },
   "note": {
    "type": "string",
    "nullable": true
   },
   "createdBy": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "scopePath": {
    "type": "string"
   }
  }
 },
 "ResourceBooking": {
  "type": "object",
  "x-ticvai-persistence": "resources.booking",
  "required": [
   "id",
   "resourceId",
   "from",
   "to",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "resourceId": {
    "type": "string",
    "format": "uuid"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "orderId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "from": {
    "type": "string",
    "format": "date-time"
   },
   "to": {
    "type": "string",
    "format": "date-time"
   },
   "status": {
    "$ref": "#/components/schemas/ResourceBookingStatus"
   },
   "holdId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "nullable": true,
    "description": "The `ResourceHold` this booking was converted from, where a guest picked the resource on a venue map (rev 3 REV3-15). Null for a staff booking or an allocation.\n"
   },
   "recurrenceGroupId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Ties the occurrences of a recurring booking. **Cancelling one week does not cancel the series**, and cancelling the series is a separate act with a separate confirmation.\n"
   },
   "depositAuthorisationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The hold, through `orders.authoriseStoredValue` (CF-126). **A deposit taken and refunded is two transactions and a fee; held and released is neither.**\n"
   },
   "checkedOutAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "dueBackAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "returnedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "conditionOut": {
    "type": "string",
    "nullable": true
   },
   "conditionIn": {
    "type": "string",
    "nullable": true
   },
   "syncedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true,
    "description": "When the latest offline check-out or check-in write reached the server. **The device times are `checkedOutAt` and `returnedAt`**, taken from each write's `recordedAt`; this is the server's half of the pair naming-and-style 5.2 requires. Null while pending.\n"
   }
  }
 },
 "ResourceBookingStatus": {
  "type": "string",
  "enum": [
   "reserved",
   "checkedOut",
   "returned",
   "overdue",
   "cancelled",
   "noShow"
  ]
 },
 "ResourceKind": {
  "type": "string",
  "description": "BL-135. **`locker` was an entitlement kind in `orders` and nothing issued, assigned or released one.** A locker is a specific object checked out to a named guest and returned — which is this context exactly, and modelling it as an entitlement would have needed a second check-out mechanism.\nA seed for `ResourceType` rather than the law (board 1.02): a customer adding a class does it with `createResourceType`, not by waiting for this list to grow.\n**`table` is a non-dining spot** (decided 29 September, rev 3 GAP-C2, confirmed by Chinmay): a beach or event table placed on a venue map, picked and sold like a cabana (`createResourceHold`, then the order). **A dining table is not this**: restaurant tables stay `fnb` tables, booked with `fnb.createTableReservation` and the waitlist (audit R073 (d)).\n",
  "enum": [
   "cabana",
   "lounger",
   "locker",
   "wheelchair",
   "stroller",
   "equipment",
   "room",
   "auditorium",
   "vehicle",
   "instructor",
   "staff",
   "table",
   "pitch",
   "studio",
   "other"
  ],
  "x-ticvai-refuses": {
   "mealPlan": "**Listed by 5.5.8b and deliberately not a kind.** 5.5.8b groups meal plans with lockers and parking, but a meal plan is a balance rather than an object. It resolves to `retail.Wallet` with a `mealPlan` credit kind (CF-126), not to a resource — so it is not offered here, and a form built from this enum cannot offer it either."
  }
 },
 "SubmitInspectionRequest": {
  "x-ticvai-persistence": "maintenance.inspection + maintenance.inspection_item",
  "type": "object",
  "required": [
   "id",
   "templateId",
   "venueId",
   "responses",
   "recordedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "templateId": {
    "type": "string",
    "format": "uuid"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "assetId": {
    "type": "string",
    "format": "uuid"
   },
   "responses": {
    "type": "array",
    "minItems": 1,
    "items": {
     "type": "object",
     "required": [
      "key",
      "value"
     ],
     "properties": {
      "key": {
       "type": "string"
      },
      "value": {},
      "passed": {
       "type": "boolean",
       "nullable": true
      },
      "note": {
       "type": "string",
       "maxLength": 1000
      },
      "attachmentRefs": {
       "type": "array",
       "items": {
        "type": "string"
       }
      }
     }
    }
   },
   "signatureRef": {
    "type": "string",
    "nullable": true
   },
   "recordedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "WorkOrder": {
  "x-ticvai-persistence": "maintenance.work_order",
  "x-ticvai-retired-columns": [
   "is_overdue"
  ],
  "type": "object",
  "required": [
   "id",
   "workOrderNumber",
   "title",
   "venueId",
   "status",
   "priority",
   "kind",
   "createdAt"
  ],
  "properties": {
   "downtimeMinutes": {
    "type": "integer",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "**Measured from out-of-service to back-in-service, not from work start to work end.** A ride down for six hours of which two were spent working is down six hours, and the gap between the two numbers is the thing worth managing.\n**Maintained on write**: set when the asset returns to service, as the minutes from the `maintenance.asset_status_change` row that took it out carrying this work order's id to the asset's next change back to `inService`. Null while the asset is still out, and for a work order that never took it out.\n"
   },
   "rootCause": {
    "type": "string",
    "nullable": true,
    "enum": [
     "wearAndTear",
     "operatorError",
     "guestDamage",
     "manufacturingDefect",
     "environmental",
     "softwareFault",
     "powerFailure",
     "deferredMaintenance",
     "unknown"
    ],
    "description": "**Structured, because free text cannot be counted.** *Deferred maintenance* is the value a venue least wants to see and most needs to — a fault caused by work that was postponed is an argument for a budget.\n"
   },
   "rootCauseNote": {
    "type": "string",
    "nullable": true
   },
   "escalatedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "escalationLevel": {
    "type": "integer",
    "default": 0,
    "description": "**Escalation is a clock, not a decision.** A work order on a ride nobody has accepted after twenty minutes escalates itself, because the alternative is somebody noticing.\n"
   },
   "id": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
   },
   "workOrderNumber": {
    "type": "string",
    "readOnly": true,
    "description": "**Server-assigned: the venue prefix plus a sequence per venue** (decided 28 September, audit R152). Not gapless; only tax invoices are gapless, per legal entity.\n"
   },
   "title": {
    "type": "string"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "assetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "assetName": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "The asset's name, copied when the work order is raised or its asset changes, and not updated when the asset is later renamed — the record reads as it was raised.\n"
   },
   "status": {
    "$ref": "#/components/schemas/WorkOrderStatus"
   },
   "priority": {
    "$ref": "#/components/schemas/WorkOrderPriority"
   },
   "kind": {
    "$ref": "#/components/schemas/WorkOrderKind"
   },
   "assignedToPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "raisedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "categoryId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "As raised in `CreateWorkOrderRequest.categoryId`, amendable by `updateWorkOrder`. The category is what `completeWorkOrder` reads to decide whether completion photographs are required.\n"
   },
   "locationDescription": {
    "type": "string",
    "maxLength": 500,
    "nullable": true,
    "description": "Where the fault is, as raised. Needed where there is no asset — a broken tile, a leak in a corridor.\n"
   },
   "elapsedMinutes": {
    "type": "integer",
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "Labour minutes accumulated up to the last pause or stop. **Maintained on write** by `recordWorkOrderTime`, `pauseWorkOrder` and `completeWorkOrder`; while `isTimerRunning` is true the interval since the last start is not yet included.\n"
   },
   "isTimerRunning": {
    "type": "boolean",
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "Maintained on write by `startWorkOrder`, `resumeWorkOrder`, `recordWorkOrderTime`, `pauseWorkOrder` and `completeWorkOrder`.\n"
   },
   "dueAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "isOverdue": {
    "type": "boolean",
    "readOnly": true,
    "x-ticvai-persisted": false,
    "x-ticvai-derived": "onRead",
    "description": "`dueAt` is in the past and the status is still `open`, `assigned`, `inProgress`, `paused` or `awaitingParts`. **Computed on read and not stored** — it depends on the clock. `listWorkOrders?overdueOnly` applies the same test to `due_at`.\n"
   },
   "requiresVerification": {
    "type": "boolean"
   },
   "sourcePlanId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "sourceInspectionId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
    "nullable": true
   },
   "sourceIncidentId": {
    "type": "string",
    "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
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
   "completedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "syncedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "WorkOrderKind": {
  "type": "string",
  "enum": [
   "corrective",
   "planned",
   "inspectionFollowUp",
   "incidentCorrective",
   "improvement"
  ]
 },
 "WorkOrderPriority": {
  "type": "string",
  "enum": [
   "low",
   "normal",
   "high",
   "urgent",
   "emergency"
  ]
 },
 "WorkOrderStatus": {
  "type": "string",
  "enum": [
   "open",
   "assigned",
   "inProgress",
   "paused",
   "awaitingParts",
   "completed",
   "verified",
   "closed",
   "cancelled"
  ]
 }
}
```
