# WS34 — Pricing   Revenue Management board 1

**10 screens · 10 operations · 14 schemas · 2 permissions**

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
| `ADM-048` | Commercial Pricing Command Center | commandCentre | 1 | 1 | — |
| `ADM-049` | Price List Master Configuration | configEditor | 1 | 0 | — |
| `ADM-050` | Price Category & Rate Type Library | listDetail | 1 | 0 | — |
| `ADM-051` | Rate Structure Builder | listDetail | 1 | 0 | — |
| `ADM-052` | Product & Service Price Assignment | listDetail | 1 | 0 | — |
| `ADM-053` | Package, Bundle & Add-On Pricing | configEditor | 1 | 0 | — |
| `ADM-054` | Market, Venue & Currency Pricing Structure | configEditor | 1 | 0 | — |
| `ADM-055` | Price Hierarchy & Inheritance Configuration | configEditor | 1 | 0 | — |
| `ADM-056` | Price List Templates, Clone & Reuse | configEditor | 1 | 0 | — |
| `ADM-057` | Commercial Pricing Structure Validation | listDetail | 1 | 0 | — |

## Thin screens in this batch

**ADM-050, ADM-052, ADM-057 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-048",
  "name": "Commercial Pricing Command Center",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "1",
   "number": "10.1.1",
   "page": 6
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/commercial-pricing-command-center-adm-048",
   "component": "apps/ticvai-web/src/routes/commercial/CommercialPricingCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-049",
    "ADM-050",
    "ADM-051",
    "ADM-052",
    "ADM-053",
    "ADM-054",
    "ADM-055",
    "ADM-056",
    "ADM-057"
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
     "to": "ADM-049",
     "trigger": "Works in Price List Master Configuration",
     "provenance": "flow F143 step 1→2",
     "operation": "listCommercialPricing"
    },
    {
     "to": "ADM-050",
     "trigger": "Works in Price Category & Rate Type Library",
     "provenance": "flow F143 step 3→4",
     "operation": "listCommercialPricing"
    },
    {
     "to": "ADM-051",
     "trigger": "Works in Rate Structure Builder",
     "provenance": "flow F143 step 5→6",
     "operation": "listCommercialPricing"
    },
    {
     "to": "ADM-052",
     "trigger": "Works in Product & Service Price Assignment",
     "provenance": "flow F143 step 7→8",
     "operation": "listCommercialPricing"
    },
    {
     "to": "ADM-053",
     "trigger": "Works in Package, Bundle & Add-On Pricing",
     "provenance": "flow F143 step 9→10",
     "operation": "listCommercialPricing"
    },
    {
     "to": "ADM-054",
     "trigger": "Works in Market, Venue & Currency Pricing Structure",
     "provenance": "flow F143 step 11→12",
     "operation": "listCommercialPricing"
    },
    {
     "to": "ADM-055",
     "trigger": "Works in Price Hierarchy & Inheritance Configuration",
     "provenance": "flow F143 step 13→14",
     "operation": "listCommercialPricing"
    },
    {
     "to": "ADM-056",
     "trigger": "Works in Price List Templates, Clone & Reuse",
     "provenance": "flow F143 step 15→16",
     "operation": "listCommercialPricing"
    },
    {
     "to": "ADM-057",
     "trigger": "Works in Commercial Pricing Structure Validation",
     "provenance": "flow F143 step 17→18",
     "operation": "listCommercialPricing"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each price list should show) — counts over a population, then the population",
  "purpose": "Provide the central administrative workspace for all commercial pricing structures across This is the first page a Revenue/Pricing Administrator sees when entering the module.",
  "purposeNote": "Authorized administrators can view and manage TICVAI's complete commercial pricing portfolio from one centralized workspace.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 8 actions on this screen and the screen declares 1 operation.** Unserved: Create Price List, Duplicate, Open, Compare, Validate, View Dependencies, Export, Archive. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 6 §Quick Actions"
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
       "label": "Search commercial pricing",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 6 §Filter by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "CommercialPricingCommandCenterView.venue",
        "CommercialPricingCommandCenterView.brand",
        "CommercialPricingCommandCenterView.market",
        "Country",
        "CommercialPricingCommandCenterView.currency",
        "Product Type",
        "Price List Type",
        "CommercialPricingCommandCenterView.owner",
        "CommercialPricingCommandCenterView.status"
       ],
       "notes": "The pack filters this screen by venue, brand, market, country, currency, product type and 3 more — which are present is a decision the pack already made.",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 6 §Filter by"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Total Price Lists",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 6 §Display",
       "bindsTo": "CommercialPricingCommandCenterView.totalPriceLists"
      },
      {
       "kind": "metricTile",
       "label": "Active Price Lists",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 6 §Display",
       "bindsTo": "CommercialPricingCommandCenterView.activePriceLists"
      },
      {
       "kind": "metricTile",
       "label": "Draft Price Lists",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 6 §Display",
       "bindsTo": "CommercialPricingCommandCenterView.draftPriceLists"
      },
      {
       "kind": "metricTile",
       "label": "Price Categories",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 6 §Display",
       "bindsTo": "CommercialPricingCommandCenterView.priceCategories"
      },
      {
       "kind": "metricTile",
       "label": "Configured Rates",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 6 §Display",
       "bindsTo": "CommercialPricingCommandCenterView.configuredRates"
      },
      {
       "kind": "metricTile",
       "label": "Products with Pricing",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 6 §Display",
       "bindsTo": "CommercialPricingCommandCenterView.productsWithPricing"
      },
      {
       "kind": "metricTile",
       "label": "Products Missing Pricing",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 6 §Display",
       "bindsTo": "CommercialPricingCommandCenterView.productsMissingPricing"
      },
      {
       "kind": "metricTile",
       "label": "Markets",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 6 §Display",
       "bindsTo": "CommercialPricingCommandCenterView.markets"
      },
      {
       "kind": "metricTile",
       "label": "Currencies",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 6 §Display",
       "bindsTo": "CommercialPricingCommandCenterView.currencies"
      },
      {
       "kind": "metricTile",
       "label": "Pricing Validation Issues",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 6 §Display",
       "bindsTo": "CommercialPricingCommandCenterView.pricingValidationIssues"
      },
      {
       "kind": "metricTile",
       "label": "Recently Modified Price Lists",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 6 §Display",
       "bindsTo": "CommercialPricingCommandCenterView.recentlyModifiedPriceLists"
      },
      {
       "kind": "metricTile",
       "label": "Upcoming Price Structures",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 6 §Display",
       "bindsTo": "CommercialPricingCommandCenterView.upcomingPriceStructures"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every commercial pricing",
       "columns": [
        "CommercialPricingCommandCenterView.priceListId",
        "CommercialPricingCommandCenterView.name",
        "CommercialPricingCommandCenterView.code",
        "CommercialPricingCommandCenterView.type",
        "CommercialPricingCommandCenterView.currency",
        "CommercialPricingCommandCenterView.market",
        "CommercialPricingCommandCenterView.venue",
        "CommercialPricingCommandCenterView.brand",
        "CommercialPricingCommandCenterView.productCount",
        "CommercialPricingCommandCenterView.rateCount",
        "CommercialPricingCommandCenterView.effectivePeriod",
        "CommercialPricingCommandCenterView.version",
        "CommercialPricingCommandCenterView.status",
        "CommercialPricingCommandCenterView.owner"
       ],
       "bindsTo": "CommercialPricingCommandCenterView",
       "operation": "listCommercialPricing",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 6 §Each price list should show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected commercial pricing",
       "bindsTo": "CommercialPricingCommandCenterView",
       "columns": [
        "CommercialPricingCommandCenterView.priceListId",
        "CommercialPricingCommandCenterView.name",
        "CommercialPricingCommandCenterView.code",
        "CommercialPricingCommandCenterView.type",
        "CommercialPricingCommandCenterView.currency",
        "CommercialPricingCommandCenterView.market",
        "CommercialPricingCommandCenterView.venue",
        "CommercialPricingCommandCenterView.brand",
        "CommercialPricingCommandCenterView.productCount",
        "CommercialPricingCommandCenterView.rateCount",
        "CommercialPricingCommandCenterView.effectivePeriod",
        "CommercialPricingCommandCenterView.version",
        "CommercialPricingCommandCenterView.status",
        "CommercialPricingCommandCenterView.owner"
       ],
       "notes": null,
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 6 §Each price list should show"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create Price List",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 6 §Quick Actions",
       "permission": "Create Price Lists"
      },
      {
       "kind": "secondaryButton",
       "label": "Duplicate",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 6 §Quick Actions",
       "permission": "Duplicate"
      },
      {
       "kind": "secondaryButton",
       "label": "Open",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 6 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Compare",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 6 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Validate",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 6 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "View Dependencies",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 6 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Export",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 6 §Quick Actions",
       "permission": "Export"
      },
      {
       "kind": "destructiveButton",
       "label": "Archive",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 6 §Quick Actions",
       "permission": "Archive"
      },
      {
       "kind": "banner",
       "label": "Permissions this screen separates",
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** View Pricing, Modify Pricing Structure. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 6 §Separate permissions for"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmArchive",
    "component": "confirmDialog",
    "trigger": "Archive",
    "body": "**Archive on a commercial pricing is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 6 §Quick Actions"
   }
  ],
  "states": {
   "loading": "The commercial pricing list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the commercial pricing untouched.",
   "emptyFirstRun": "No commercial pricing yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the commercial pricing are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCommercialPricing",
    "contract": "catalogue",
    "purpose": "Commercial Pricing Command Center",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-048"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 6. 32 of 35 labels bound to a contract property; 49 of 71 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-049",
  "name": "Price List Master Configuration",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "1",
   "number": "10.1.2",
   "page": 8
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/price-list-master-configuration-adm-049",
   "component": "apps/ticvai-web/src/routes/commercial/PriceListMasterConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-048"
   ],
   "exitTo": [
    "ADM-048"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-048, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-048",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F143 step 2→3",
     "operation": "setPriceListMaster"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Create the master container that holds commercial rates. A Price List should be reusable across products and channels.",
  "purposeNote": "Administrators can create reusable commercial price-list masters with clearly defined ownership, scope, currency, market, and business applicability.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Price List Name",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 8 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Price List Code",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 8 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Description",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 8 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Price List Type",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 8 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Legal Entity",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 8 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Brand",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 8 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Business Unit",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 8 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Country",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 8 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Market",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 8 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 8 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Default Currency",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 8 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Owner",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 8 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Tags",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 8 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Status",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 8 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Default Rate Category",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 8 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Default Rounding Profile",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 8 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Default Price Hierarchy",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 8 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Allow Overrides",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 8 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Allow Inheritance",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 8 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Allow Multiple Currencies",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 8 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Allow Product-Specific Rates",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 8 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save changes",
       "provenance": "contract operation setPriceListMaster"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The price list master configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the price list master untouched.",
   "emptyFirstRun": "No price list master configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setPriceListMaster",
    "contract": "catalogue",
    "purpose": "Price List Master Configuration",
    "trigger": "onAction",
    "invalidates": [
     "setPriceListMaster"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-049"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 8. 0 of 0 labels bound to a contract property; 21 of 37 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-050",
  "name": "Price Category & Rate Type Library",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "1",
   "number": "10.1.3",
   "page": 9
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/price-category-rate-type-library-adm-050",
   "component": "apps/ticvai-web/src/routes/commercial/PriceCategoryRateTypeLibrary.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-048"
   ],
   "exitTo": [
    "ADM-048"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-048, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-048",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F143 step 4→5",
     "operation": "listPriceCategoryRate"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Define standardized commercial rate categories used across TICVAI. This avoids different venues independently creating categories such as: “Adult,” “Adult Standard,” “Normal Adult,” and “Full Adult.”",
  "purposeNote": "types across all tenants, venues, and products.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 9"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 9"
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
       "impliedBy": "listPriceCategoryRate",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The price category rate list.",
   "error": "Could not load. Names which read failed and leaves the price category rate untouched.",
   "emptyFirstRun": "No price category rate yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the price category rate are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPriceCategoryRate",
    "contract": "catalogue",
    "purpose": "Price Category & Rate Type Library",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "PriceCategoryRateTypeLibraryView.adult",
    "PriceCategoryRateTypeLibraryView.child",
    "PriceCategoryRateTypeLibraryView.junior",
    "PriceCategoryRateTypeLibraryView.senior",
    "PriceCategoryRateTypeLibraryView.student"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-050"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 9. 0 of 0 labels bound to a contract property; 0 of 49 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-051",
  "name": "Rate Structure Builder",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "1",
   "number": "10.1.4",
   "page": 11
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/rate-structure-builder-adm-051",
   "component": "apps/ticvai-web/src/routes/commercial/RateStructureBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-048"
   ],
   "exitTo": [
    "ADM-048"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-048, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-048",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F143 step 6→7",
     "operation": "setRateStructure"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Detect) and no metric row",
  "purpose": "Define the actual monetary rates contained within a price list. This is the core commercial configuration screen.",
  "purposeNote": "Administrators can define monetary rate structures for all TICVAI commercial product types through configurable rate matrices.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 2 actions on this screen and the screen declares 1 operation.** Unserved: Per Ticket, Per Membership Period. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 11 §Support"
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
       "label": "Every rate structure",
       "columns": [
        "Duplicate Rates",
        "RateStructureBuilderView.missingAmounts",
        "RateStructureBuilderView.unsupportedCurrency",
        "RateStructureBuilderView.invalidDerivedRate",
        "RateStructureBuilderView.circularRateRelationship"
       ],
       "bindsTo": "RateStructureBuilderView",
       "operation": "setRateStructure",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 11 §Detect"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected rate structure",
       "bindsTo": "RateStructureBuilderView",
       "columns": [
        "Duplicate Rates",
        "RateStructureBuilderView.missingAmounts",
        "RateStructureBuilderView.unsupportedCurrency",
        "RateStructureBuilderView.invalidDerivedRate",
        "RateStructureBuilderView.circularRateRelationship"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Adult”, “Child Reduced”, “Senior Reduced”, “Resident Reduced”, “Group Group”, “Each rate should contain”.",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 11 §Detect"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Per Ticket",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 11 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Per Membership Period",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 11 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The rate structure list.",
   "error": "Could not load. Names which read failed and leaves the rate structure untouched.",
   "emptyFirstRun": "No rate structure yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the rate structure are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setRateStructure",
    "contract": "catalogue",
    "purpose": "Rate Structure Builder",
    "trigger": "onAction",
    "invalidates": [
     "setRateStructure"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "Duplicate Rates",
    "RateStructureBuilderView.missingAmounts",
    "RateStructureBuilderView.unsupportedCurrency",
    "RateStructureBuilderView.invalidDerivedRate",
    "RateStructureBuilderView.circularRateRelationship"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-051"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 11. 4 of 5 labels bound to a contract property; 7 of 47 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-052",
  "name": "Product & Service Price Assignment",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "1",
   "number": "10.1.5",
   "page": 13
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/product-service-price-assignment-adm-052",
   "component": "apps/ticvai-web/src/routes/commercial/ProductServicePriceAssignment.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-048"
   ],
   "exitTo": [
    "ADM-048"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-048, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-048",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F143 step 8→9",
     "operation": "setProductServicePrice"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Product configuration should display) and no metric row",
  "purpose": "Connect commercial rates to the actual products and services being sold.",
  "purposeNote": "All sellable TICVAI objects can reference centrally managed price lists and rates without maintaining duplicate price definitions inside business modules.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Ticket Type. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 13 §Allow"
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
       "label": "Every product service price",
       "columns": [
        "Pricing Source: UAE Standard Admission 2027"
       ],
       "bindsTo": "ProductServicePriceAssignmentView",
       "operation": "setProductServicePrice",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 13 §Product configuration should display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected product service price",
       "bindsTo": "ProductServicePriceAssignmentView",
       "columns": [
        "Pricing Source: UAE Standard Admission 2027"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Pricing can be assigned to”, “Dependency View”.",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 13 §Product configuration should display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Ticket Type",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 13 §Allow"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The product service price list.",
   "error": "Could not load. Names which read failed and leaves the product service price untouched.",
   "emptyFirstRun": "No product service price yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the product service price are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setProductServicePrice",
    "contract": "catalogue",
    "purpose": "Product & Service Price Assignment",
    "trigger": "onAction",
    "invalidates": [
     "setProductServicePrice"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "Pricing Source: UAE Standard Admission 2027"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-052"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 13. 0 of 1 labels bound to a contract property; 3 of 37 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-053",
  "name": "Package, Bundle & Add-On Pricing",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "1",
   "number": "10.1.6",
   "page": 14
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/package-bundle-add-on-pricing-adm-053",
   "component": "apps/ticvai-web/src/routes/commercial/PackageBundleAddOnPricing.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-048"
   ],
   "exitTo": [
    "ADM-048"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-048, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-048",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F143 step 10→11",
     "operation": "listPackageBundleAdd"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure pricing for; Configure whether the customer sees) and no display directory — it is settings, not a population",
  "purpose": "Provide dedicated commercial structures for products containing multiple components. This is separate from the Product Relationship/Bundle module. Product Catalogue defines what the bundle contains. Pricing defines how that bundle is priced.",
  "purposeNote": "Packages, bundles, and add-ons can use centralized commercial pricing while their product composition remains owned by the Product Catalogue.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Component Override. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 14 §Support"
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
       "label": "Fast Track",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 14 §Configure pricing for"
      },
      {
       "kind": "selectField",
       "label": "Parking",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 14 §Configure pricing for"
      },
      {
       "kind": "selectField",
       "label": "Meal",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 14 §Configure pricing for"
      },
      {
       "kind": "selectField",
       "label": "Photo",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 14 §Configure pricing for"
      },
      {
       "kind": "selectField",
       "label": "Equipment",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 14 §Configure pricing for"
      },
      {
       "kind": "selectField",
       "label": "Upgrade",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 14 §Configure pricing for"
      },
      {
       "kind": "selectField",
       "label": "Additional Session",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 14 §Configure pricing for"
      },
      {
       "kind": "selectField",
       "label": "Premium Access",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 14 §Configure pricing for"
      },
      {
       "kind": "selectField",
       "label": "Package Total Only",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 14 §Configure whether the customer sees"
      },
      {
       "kind": "selectField",
       "label": "Individual Components",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 14 §Configure whether the customer sees"
      },
      {
       "kind": "textField",
       "label": "Component + Package Saving",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 14 §Configure whether the customer sees"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Component Override",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 14 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The package bundle add-on configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the package bundle add-on untouched.",
   "emptyFirstRun": "No package bundle add-on configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPackageBundleAdd",
    "contract": "catalogue",
    "purpose": "Package, Bundle & Add-On Pricing",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-053"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 14. 0 of 0 labels bound to a contract property; 12 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-054",
  "name": "Market, Venue & Currency Pricing Structure",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "1",
   "number": "10.1.7",
   "page": 15
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/market-venue-currency-pricing-structure-adm-054",
   "component": "apps/ticvai-web/src/routes/commercial/MarketVenueCurrencyPricingStructure.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-048"
   ],
   "exitTo": [
    "ADM-048"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-048, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-048",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F143 step 12→13",
     "operation": "listMarketVenueCurrency"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure; FX-Assisted Setup) and no display directory — it is settings, not a population",
  "purpose": "Support TICVAI's multi-country, multi-market, multi-venue and multi-currency commercial model.",
  "purposeNote": "entities, and currencies.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Country",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 15 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Market",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 15 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Region",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 15 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 15 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Brand",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 15 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Legal Entity",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 15 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Currency",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 15 §Configure"
      },
      {
       "kind": "textField",
       "label": "AED 250 ≈ SAR 255",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 15 §FX-Assisted Setup"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The market venue currency configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the market venue currency untouched.",
   "emptyFirstRun": "No market venue currency configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listMarketVenueCurrency",
    "contract": "catalogue",
    "purpose": "Market, Venue & Currency Pricing Structure",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-054"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 15. 0 of 0 labels bound to a contract property; 8 of 32 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-055",
  "name": "Price Hierarchy & Inheritance Configuration",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "1",
   "number": "10.1.8",
   "page": 17
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/price-hierarchy-inheritance-configuration-adm-055",
   "component": "apps/ticvai-web/src/routes/commercial/PriceHierarchyInheritanceConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-048"
   ],
   "exitTo": [
    "ADM-048"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-048, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-048",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F143 step 14→15",
     "operation": "setPriceHierarchyInheritance"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Administrators configure; Configure) and no display directory — it is settings, not a population",
  "purpose": "Define where TICVAI should obtain a price when multiple commercial pricing layers exist. This is essential to prevent conflicting prices.",
  "purposeNote": "The platform deterministically resolves the correct commercial price source across global, market, venue, and product hierarchies.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Hierarchy Level",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 17 §Administrators configure"
      },
      {
       "kind": "selectField",
       "label": "Priority",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 17 §Administrators configure"
      },
      {
       "kind": "selectField",
       "label": "Inheritance",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 17 §Administrators configure"
      },
      {
       "kind": "selectField",
       "label": "Override Permission",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 17 §Administrators configure"
      },
      {
       "kind": "selectField",
       "label": "Fallback Behavior",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 17 §Administrators configure"
      },
      {
       "kind": "selectField",
       "label": "Override Allowed",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 17 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Override Requires Reason",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 17 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum Override Range",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 17 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Override Expiry",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 17 §Configure"
      },
      {
       "kind": "textField",
       "label": "Return to Parent Price",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 17 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save changes",
       "provenance": "contract operation setPriceHierarchyInheritance"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The price hierarchy inheritance configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the price hierarchy inheritance untouched.",
   "emptyFirstRun": "No price hierarchy inheritance configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setPriceHierarchyInheritance",
    "contract": "catalogue",
    "purpose": "Price Hierarchy & Inheritance Configuration",
    "trigger": "onAction",
    "invalidates": [
     "setPriceHierarchyInheritance"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-055"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 17. 0 of 0 labels bound to a contract property; 10 of 29 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-056",
  "name": "Price List Templates, Clone & Reuse",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "1",
   "number": "10.1.9",
   "page": 18
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/price-list-templates-clone-reuse-adm-056",
   "component": "apps/ticvai-web/src/routes/commercial/PriceListTemplatesCloneReuse.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-048"
   ],
   "exitTo": [
    "ADM-048"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-048, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-048",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F143 step 16→17",
     "operation": "listPriceListTemplate"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Options) and no display directory — it is settings, not a population",
  "purpose": "Accelerate commercial setup across new venues, events, seasons and markets.",
  "purposeNote": "Administrators can rapidly create consistent commercial pricing structures by cloning and reusing approved templates instead of rebuilding pricing manually.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Complete Price List. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 18 §Allow cloning"
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
       "label": "☑ Copy categories",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 18 §Options"
      },
      {
       "kind": "textField",
       "label": "☑ Copy rate structure",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 18 §Options"
      },
      {
       "kind": "textField",
       "label": "☑ Copy product mapping",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 18 §Options"
      },
      {
       "kind": "textField",
       "label": "☐ Copy monetary values",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 18 §Options"
      },
      {
       "kind": "textField",
       "label": "☑ Increase values by 5%",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 18 §Options"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Complete Price List",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 18 §Allow cloning"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The price list templates configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the price list templates untouched.",
   "emptyFirstRun": "No price list templates configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPriceListTemplate",
    "contract": "catalogue",
    "purpose": "Price List Templates, Clone & Reuse",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-056"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 18. 0 of 0 labels bound to a contract property; 6 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-057",
  "name": "Commercial Pricing Structure Validation",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "1",
   "number": "10.1.10",
   "page": 19
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/commercial-pricing-structure-validation-adm-057",
   "component": "apps/ticvai-web/src/routes/commercial/CommercialPricingStructureValidation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-048"
   ],
   "exitTo": [
    "ADM-048"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-048, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation."
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Validate that the commercial pricing foundation is structurally complete before it proceeds to rule configuration, governance, or publication. This is not the final publication screen. Board 4 owns approval and publication. Board 1 defined what the commercial prices are and how they are structured.",
  "purposeNote": "from progressing downstream without clearly identifying the issue. Board 1 — Final Screen Register # Screen Responsibility 10.1. Commercial Pricing Command",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 19"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 19"
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
       "impliedBy": "listCommercialPricingStructure",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The commercial pricing structure list.",
   "error": "Could not load. Names which read failed and leaves the commercial pricing structure untouched.",
   "emptyFirstRun": "No commercial pricing structure yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the commercial pricing structure are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCommercialPricingStructure",
    "contract": "catalogue",
    "purpose": "Commercial Pricing Structure Validation",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "CommercialPricingStructureValidationView.requiredFieldsComplete",
    "CommercialPricingStructureValidationView.currencyDefined",
    "CommercialPricingStructureValidationView.ownershipAssigned",
    "CommercialPricingStructureValidationView.categoriesConfigured",
    "CommercialPricingStructureValidationView.monetaryValuesValid"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-057"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 19. 0 of 0 labels bound to a contract property; 0 of 83 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "listCommercialPricing": {
  "method": "GET",
  "path": "/commercial-pricing",
  "contract": "catalogue",
  "summary": "Commercial Pricing Command Center",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "country",
    "in": "query",
    "required": false
   },
   {
    "name": "productType",
    "in": "query",
    "required": false
   },
   {
    "name": "priceListType",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "CommercialPricingCommandCenterView"
 },
 "listCommercialPricingStructure": {
  "method": "GET",
  "path": "/commercial-pricing-structure",
  "contract": "catalogue",
  "summary": "Commercial Pricing Structure Validation",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "CommercialPricingStructureValidationView"
 },
 "listMarketVenueCurrency": {
  "method": "GET",
  "path": "/market-venue-currency",
  "contract": "catalogue",
  "summary": "Market, Venue & Currency Pricing Structure",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "MarketVenueCurrencyPricingStructureView"
 },
 "listPackageBundleAdd": {
  "method": "GET",
  "path": "/package-bundle-add",
  "contract": "catalogue",
  "summary": "Package, Bundle & Add-On Pricing",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "PackageBundleAddOnPricingView"
 },
 "listPriceCategoryRate": {
  "method": "GET",
  "path": "/price-category-rate",
  "contract": "catalogue",
  "summary": "Price Category & Rate Type Library",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "PriceCategoryRateTypeLibraryView"
 },
 "listPriceListTemplate": {
  "method": "GET",
  "path": "/price-list-template",
  "contract": "catalogue",
  "summary": "Price List Templates, Clone & Reuse",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "PriceListTemplatesCloneReuseView"
 },
 "setPriceHierarchyInheritance": {
  "method": "PUT",
  "path": "/price-hierarchy-inheritance",
  "contract": "catalogue",
  "summary": "Price Hierarchy & Inheritance Configuration",
  "permission": "PRODUCT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "PriceHierarchyInheritanceConfigurationInput",
  "responds": "PriceHierarchyInheritanceConfigurationView"
 },
 "setPriceListMaster": {
  "method": "PUT",
  "path": "/price-list-master",
  "contract": "catalogue",
  "summary": "Price List Master Configuration",
  "permission": "PRODUCT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "PriceListMasterConfigurationInput",
  "responds": "PriceListMasterConfigurationView"
 },
 "setProductServicePrice": {
  "method": "PUT",
  "path": "/product-service-price",
  "contract": "catalogue",
  "summary": "Product & Service Price Assignment",
  "permission": "PRODUCT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "ProductServicePriceAssignmentInput",
  "responds": "ProductServicePriceAssignmentView"
 },
 "setRateStructure": {
  "method": "PUT",
  "path": "/rate-structure",
  "contract": "catalogue",
  "summary": "Rate Structure Builder",
  "permission": "PRODUCT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "RateStructureBuilderInput",
  "responds": "RateStructureBuilderView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "CommercialPricingCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Commercial Pricing Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "totalPriceLists": {
    "type": "integer",
    "description": "Total Price Lists"
   },
   "activePriceLists": {
    "type": "integer",
    "description": "Active Price Lists"
   },
   "draftPriceLists": {
    "type": "integer",
    "description": "Draft Price Lists"
   },
   "priceCategories": {
    "type": "integer",
    "description": "Price Categories"
   },
   "configuredRates": {
    "type": "integer",
    "description": "Configured Rates"
   },
   "productsWithPricing": {
    "type": "string",
    "description": "Products with Pricing"
   },
   "productsMissingPricing": {
    "type": "string",
    "description": "Products Missing Pricing"
   },
   "markets": {
    "type": "integer",
    "description": "Markets"
   },
   "currencies": {
    "type": "integer",
    "description": "Currencies"
   },
   "pricingValidationIssues": {
    "type": "integer",
    "description": "Pricing Validation Issues"
   },
   "recentlyModifiedPriceLists": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Recently Modified Price Lists"
   },
   "upcomingPriceStructures": {
    "type": "integer",
    "description": "Upcoming Price Structures"
   },
   "priceListId": {
    "type": "string",
    "description": "Price List ID"
   },
   "name": {
    "type": "string",
    "description": "Name"
   },
   "code": {
    "type": "string",
    "description": "Code"
   },
   "type": {
    "type": "string",
    "description": "Type"
   },
   "currency": {
    "type": "string",
    "description": "Currency"
   },
   "market": {
    "type": "string",
    "description": "Market"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "brand": {
    "type": "string",
    "description": "Brand"
   },
   "productCount": {
    "type": "integer",
    "description": "Product Count"
   },
   "rateCount": {
    "type": "integer",
    "description": "Rate Count"
   },
   "effectivePeriod": {
    "type": "string",
    "format": "date-time",
    "description": "Effective Period"
   },
   "version": {
    "type": "string",
    "description": "Version"
   },
   "status": {
    "type": "integer",
    "description": "Status"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   },
   "modifyPricingStructure": {
    "type": "string",
    "description": "Modify Pricing Structure"
   }
  }
 },
 "CommercialPricingStructureValidationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Commercial Pricing Structure Validation displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "requiredFieldsComplete": {
    "type": "string",
    "description": "Required fields complete"
   },
   "currencyDefined": {
    "type": "string",
    "description": "Currency defined"
   },
   "ownershipAssigned": {
    "type": "string",
    "description": "Ownership assigned"
   },
   "categoriesConfigured": {
    "type": "string",
    "description": "Categories configured"
   },
   "monetaryValuesValid": {
    "type": "string",
    "description": "Monetary values valid"
   },
   "derivedRelationshipsValid": {
    "type": "string",
    "description": "Derived relationships valid"
   },
   "requiredProductsPriced": {
    "type": "string",
    "description": "Required products priced"
   },
   "noOrphanAssignments": {
    "type": "string",
    "description": "No orphan assignments"
   },
   "componentPricingValid": {
    "type": "string",
    "description": "Component pricing valid"
   },
   "currencyAndVenueConfigurationValid": {
    "type": "string",
    "description": "Currency and venue configuration valid"
   },
   "noConflictingSourcePriority": {
    "type": "string",
    "description": "No conflicting source priority"
   },
   "fallbackConfigured": {
    "type": "string",
    "description": "Fallback configured"
   },
   "saleCannotProceed": {
    "type": "string",
    "description": "Sale cannot proceed"
   },
   "optimizationSuggestion": {
    "type": "string",
    "description": "Optimization suggestion"
   },
   "calculation": {
    "type": "string",
    "description": "calculation"
   },
   "revenueOptimization": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "revenue optimization"
   },
   "calculationEngine": {
    "type": "string",
    "description": "calculation engine"
   },
   "doesNotPerformDynamicPricing": {
    "type": "string",
    "description": "does not perform dynamic pricing"
   }
  }
 },
 "MarketVenueCurrencyPricingStructureView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Market, Venue & Currency Pricing Structure displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "country": {
    "type": "string",
    "description": "Country"
   },
   "market": {
    "type": "string",
    "description": "Market"
   },
   "region": {
    "type": "string",
    "description": "Region"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "brand": {
    "type": "string",
    "description": "Brand"
   },
   "legalEntity": {
    "type": "string",
    "description": "Legal Entity"
   },
   "currency": {
    "type": "string",
    "description": "Currency"
   },
   "baseCurrency": {
    "type": "string",
    "description": "Base Currency"
   },
   "sellingCurrency": {
    "type": "string",
    "description": "Selling Currency"
   },
   "currencyPrecision": {
    "type": "string",
    "description": "Currency Precision"
   },
   "rounding": {
    "type": "string",
    "description": "Rounding"
   },
   "displayFormat": {
    "type": "string",
    "description": "Display Format"
   },
   "conversions": {
    "type": "string",
    "description": "conversions"
   },
   "aed250Sar255": {
    "type": "string",
    "description": "AED 250 ≈ SAR 255"
   }
  }
 },
 "PackageBundleAddOnPricingView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Package, Bundle & Add-On Pricing displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "fixedPackagePrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Fixed Package Price"
   },
   "sumOfComponents": {
    "type": "string",
    "description": "Sum of Components"
   },
   "discountedComponentSum": {
    "type": "string",
    "description": "Discounted Component Sum"
   },
   "componentOverride": {
    "type": "string",
    "description": "Component Override"
   },
   "includedComponent": {
    "type": "string",
    "description": "Included Component"
   },
   "optionalPaidComponent": {
    "type": "string",
    "description": "Optional Paid Component"
   },
   "fastTrack": {
    "type": "string",
    "description": "Fast Track"
   },
   "parking": {
    "type": "string",
    "description": "Parking"
   },
   "meal": {
    "type": "string",
    "description": "Meal"
   },
   "photo": {
    "type": "string",
    "description": "Photo"
   },
   "equipment": {
    "type": "string",
    "description": "Equipment"
   },
   "additionalSession": {
    "type": "string",
    "description": "Additional Session"
   },
   "premiumAccess": {
    "type": "string",
    "description": "Premium Access"
   },
   "packageTotalOnly": {
    "type": "string",
    "description": "Package Total Only"
   },
   "individualComponents": {
    "type": "string",
    "description": "Individual Components"
   },
   "componentPackageSaving": {
    "type": "string",
    "description": "Component + Package Saving"
   },
   "derivedPackagePrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "derived package price"
   }
  }
 },
 "PriceCategoryRateTypeLibraryView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Price Category & Rate Type Library displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "adult": {
    "type": "string",
    "description": "Adult"
   },
   "child": {
    "type": "string",
    "description": "Child"
   },
   "junior": {
    "type": "string",
    "description": "Junior"
   },
   "senior": {
    "type": "string",
    "description": "Senior"
   },
   "student": {
    "type": "string",
    "description": "Student"
   },
   "resident": {
    "type": "string",
    "description": "Resident"
   },
   "nonResident": {
    "type": "string",
    "description": "Non-Resident"
   },
   "member": {
    "type": "string",
    "description": "Member"
   },
   "vip": {
    "type": "string",
    "description": "VIP"
   },
   "group": {
    "type": "string",
    "description": "Group"
   },
   "corporate": {
    "type": "string",
    "description": "Corporate"
   },
   "b2b": {
    "type": "string",
    "description": "B2B"
   },
   "complimentary": {
    "type": "string",
    "description": "Complimentary"
   },
   "staff": {
    "type": "string",
    "description": "Staff"
   },
   "promotional": {
    "type": "string",
    "description": "Promotional"
   },
   "custom": {
    "type": "string",
    "description": "Custom"
   },
   "categoryId": {
    "type": "string",
    "description": "Category ID"
   },
   "name": {
    "type": "string",
    "description": "Name"
   },
   "code": {
    "type": "string",
    "description": "Code"
   },
   "description": {
    "type": "string",
    "description": "Description"
   },
   "categoryFamily": {
    "type": "string",
    "description": "Category Family"
   },
   "displayName": {
    "type": "string",
    "description": "Display Name"
   },
   "iconLabel": {
    "type": "string",
    "description": "Icon/Label"
   },
   "activeInactive": {
    "type": "integer",
    "description": "Active/Inactive"
   }
  }
 },
 "PriceHierarchyInheritanceConfigurationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table covers these fields** — the closest is catalogue.price_list at 17%, so this is not an update to anything the package stores today and no new table has been decided",
  "description": "**What Price Hierarchy & Inheritance Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "hierarchyLevel": {
    "type": "string",
    "description": "Hierarchy Level"
   },
   "priority": {
    "type": "string",
    "description": "Priority"
   },
   "inheritance": {
    "type": "string",
    "description": "Inheritance"
   },
   "fallbackBehavior": {
    "type": "string",
    "description": "Fallback Behavior"
   },
   "maximumOverrideRange": {
    "type": "string",
    "description": "Maximum Override Range"
   },
   "returnToParentPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Return to Parent Price"
   }
  }
 },
 "PriceHierarchyInheritanceConfigurationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Price Hierarchy & Inheritance Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "hierarchyLevel": {
    "type": "string",
    "description": "Hierarchy Level"
   },
   "priority": {
    "type": "string",
    "description": "Priority"
   },
   "inheritance": {
    "type": "string",
    "description": "Inheritance"
   },
   "fallbackBehavior": {
    "type": "string",
    "description": "Fallback Behavior"
   },
   "maximumOverrideRange": {
    "type": "string",
    "description": "Maximum Override Range"
   },
   "returnToParentPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Return to Parent Price"
   }
  }
 },
 "PriceListMasterConfigurationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Price List Master Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "priceListName": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price List Name"
   },
   "priceListCode": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price List Code"
   },
   "description": {
    "type": "string",
    "description": "Description"
   },
   "priceListType": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price List Type"
   },
   "legalEntity": {
    "type": "string",
    "description": "Legal Entity"
   },
   "brand": {
    "type": "string",
    "description": "Brand"
   },
   "businessUnit": {
    "type": "string",
    "description": "Business Unit"
   },
   "country": {
    "type": "string",
    "description": "Country"
   },
   "market": {
    "type": "string",
    "description": "Market"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "defaultCurrency": {
    "type": "string",
    "description": "Default Currency"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   },
   "tags": {
    "type": "string",
    "description": "Tags"
   },
   "status": {
    "type": "string",
    "description": "Status"
   },
   "defaultRateCategory": {
    "type": "number",
    "description": "Default Rate Category"
   },
   "defaultRoundingProfile": {
    "type": "string",
    "description": "Default Rounding Profile"
   },
   "defaultPriceHierarchy": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Default Price Hierarchy"
   },
   "allowOverrides": {
    "type": "boolean",
    "description": "Allow Overrides"
   },
   "allowInheritance": {
    "type": "boolean",
    "description": "Allow Inheritance"
   },
   "allowMultipleCurrencies": {
    "type": "boolean",
    "description": "Allow Multiple Currencies"
   },
   "allowProductSpecificRates": {
    "type": "boolean",
    "description": "Allow Product-Specific Rates"
   },
   "global": {
    "type": "string",
    "description": "Global"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "into": {
    "type": "string",
    "description": "into"
   }
  }
 },
 "PriceListMasterConfigurationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Price List Master Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "priceListName": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price List Name"
   },
   "priceListCode": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price List Code"
   },
   "description": {
    "type": "string",
    "description": "Description"
   },
   "priceListType": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price List Type"
   },
   "legalEntity": {
    "type": "string",
    "description": "Legal Entity"
   },
   "brand": {
    "type": "string",
    "description": "Brand"
   },
   "businessUnit": {
    "type": "string",
    "description": "Business Unit"
   },
   "country": {
    "type": "string",
    "description": "Country"
   },
   "market": {
    "type": "string",
    "description": "Market"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "defaultCurrency": {
    "type": "string",
    "description": "Default Currency"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   },
   "tags": {
    "type": "string",
    "description": "Tags"
   },
   "status": {
    "type": "string",
    "description": "Status"
   },
   "defaultRateCategory": {
    "type": "number",
    "description": "Default Rate Category"
   },
   "defaultRoundingProfile": {
    "type": "string",
    "description": "Default Rounding Profile"
   },
   "defaultPriceHierarchy": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Default Price Hierarchy"
   },
   "allowOverrides": {
    "type": "boolean",
    "description": "Allow Overrides"
   },
   "allowInheritance": {
    "type": "boolean",
    "description": "Allow Inheritance"
   },
   "allowMultipleCurrencies": {
    "type": "boolean",
    "description": "Allow Multiple Currencies"
   },
   "allowProductSpecificRates": {
    "type": "boolean",
    "description": "Allow Product-Specific Rates"
   },
   "global": {
    "type": "string",
    "description": "Global"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "into": {
    "type": "string",
    "description": "into"
   }
  }
 },
 "PriceListTemplatesCloneReuseView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Price List Templates, Clone & Reuse displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "priceCategories": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price Categories"
   },
   "rateTypes": {
    "type": "number",
    "description": "Rate Types"
   },
   "rateMatrixStructure": {
    "type": "number",
    "description": "Rate Matrix Structure"
   },
   "currencyStructure": {
    "type": "string",
    "description": "Currency Structure"
   },
   "hierarchy": {
    "type": "string",
    "description": "Hierarchy"
   },
   "productMappingPattern": {
    "type": "string",
    "description": "Product Mapping Pattern"
   },
   "packagePricingPattern": {
    "type": "string",
    "description": "Package Pricing Pattern"
   },
   "completePriceList": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Complete Price List"
   },
   "rateStructureOnly": {
    "type": "number",
    "description": "Rate Structure Only"
   },
   "selectedCategories": {
    "type": "string",
    "description": "Selected Categories"
   },
   "productAssignments": {
    "type": "string",
    "description": "Product Assignments"
   },
   "marketStructure": {
    "type": "string",
    "description": "Market Structure"
   },
   "optionsType": {
    "type": "string",
    "enum": [
     "copyCategories",
     "copyRateStructure",
     "copyProductMapping",
     "copyMonetaryValues",
     "increaseValuesBy5"
    ],
    "description": "Vocabulary listed under Options."
   },
   "venueType": {
    "type": "string",
    "description": "Venue Type"
   },
   "productPortfolio": {
    "type": "string",
    "description": "Product Portfolio"
   },
   "similarVenues": {
    "type": "string",
    "description": "Similar Venues"
   },
   "existingTicvaiConfiguration": {
    "type": "string",
    "description": "Existing TICVAI Configuration"
   }
  }
 },
 "ProductServicePriceAssignmentInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Product & Service Price Assignment submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "ticketProduct": {
    "type": "string",
    "description": "Ticket Product"
   },
   "ticketType": {
    "type": "string",
    "description": "Ticket Type"
   },
   "admission": {
    "type": "string",
    "description": "Admission"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "performance": {
    "type": "string",
    "description": "Performance"
   },
   "membership": {
    "type": "string",
    "description": "Membership"
   },
   "annualPass": {
    "type": "string",
    "description": "Annual Pass"
   },
   "addOn": {
    "type": "string",
    "description": "Add-On"
   },
   "fBItem": {
    "type": "string",
    "description": "F&B Item"
   },
   "retailProduct": {
    "type": "string",
    "description": "Retail Product"
   },
   "rentalItem": {
    "type": "string",
    "description": "Rental Item"
   },
   "resource": {
    "type": "string",
    "description": "Resource"
   },
   "reservationService": {
    "type": "string",
    "description": "Reservation Service"
   },
   "experience": {
    "type": "string",
    "description": "Experience"
   },
   "otherSellableService": {
    "type": "string",
    "description": "Other Sellable Service"
   },
   "andAssign": {
    "type": "string",
    "description": "and assign"
   },
   "uaeStandardAdmissionPriceList": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "UAE Standard Admission Price List"
   },
   "productLevel": {
    "type": "string",
    "description": "Product Level"
   },
   "productVariant": {
    "type": "string",
    "description": "Product Variant"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   }
  }
 },
 "ProductServicePriceAssignmentView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Product & Service Price Assignment displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "ticketProduct": {
    "type": "string",
    "description": "Ticket Product"
   },
   "ticketType": {
    "type": "string",
    "description": "Ticket Type"
   },
   "admission": {
    "type": "string",
    "description": "Admission"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "performance": {
    "type": "string",
    "description": "Performance"
   },
   "membership": {
    "type": "string",
    "description": "Membership"
   },
   "annualPass": {
    "type": "string",
    "description": "Annual Pass"
   },
   "addOn": {
    "type": "string",
    "description": "Add-On"
   },
   "fBItem": {
    "type": "string",
    "description": "F&B Item"
   },
   "retailProduct": {
    "type": "string",
    "description": "Retail Product"
   },
   "rentalItem": {
    "type": "string",
    "description": "Rental Item"
   },
   "resource": {
    "type": "string",
    "description": "Resource"
   },
   "reservationService": {
    "type": "string",
    "description": "Reservation Service"
   },
   "experience": {
    "type": "string",
    "description": "Experience"
   },
   "otherSellableService": {
    "type": "string",
    "description": "Other Sellable Service"
   },
   "andAssign": {
    "type": "string",
    "description": "and assign"
   },
   "uaeStandardAdmissionPriceList": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "UAE Standard Admission Price List"
   },
   "productLevel": {
    "type": "string",
    "description": "Product Level"
   },
   "productVariant": {
    "type": "string",
    "description": "Product Variant"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   }
  }
 },
 "RateStructureBuilderInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table covers these fields** — the closest is catalogue.price at 4%, so this is not an update to anything the package stores today and no new table has been decided",
  "description": "**What Rate Structure Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.\n\n**The pack defines this as a record**, under *Each rate should contain* - one of only 13 drafted writes that does. That is the client writing a row rather than a screen, and it is where the table conversation should start.",
  "properties": {
   "d250": {
    "type": "string",
    "description": "d 250"
   },
   "rateId": {
    "type": "string",
    "description": "Rate ID"
   },
   "rateName": {
    "type": "number",
    "description": "Rate Name"
   },
   "rateCode": {
    "type": "number",
    "description": "Rate Code"
   },
   "priceCategory": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price Category"
   },
   "rateType": {
    "type": "number",
    "description": "Rate Type"
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Amount"
   },
   "currency": {
    "type": "string",
    "description": "Currency"
   },
   "unitBasis": {
    "type": "string",
    "description": "Unit Basis"
   },
   "precision": {
    "type": "string",
    "description": "Precision"
   },
   "roundingProfile": {
    "type": "string",
    "description": "Rounding Profile"
   },
   "status": {
    "type": "string",
    "description": "Status"
   },
   "perTicket": {
    "type": "string",
    "description": "Per Ticket"
   },
   "perPerson": {
    "type": "string",
    "description": "Per Person"
   },
   "perUnit": {
    "type": "string",
    "description": "Per Unit"
   },
   "perHour": {
    "type": "string",
    "description": "Per Hour"
   },
   "perDay": {
    "type": "string",
    "description": "Per Day"
   },
   "perSession": {
    "type": "string",
    "description": "Per Session"
   },
   "perResource": {
    "type": "string",
    "description": "Per Resource"
   },
   "perPackage": {
    "type": "string",
    "description": "Per Package"
   },
   "perMembershipPeriod": {
    "type": "string",
    "format": "date-time",
    "description": "Per Membership Period"
   },
   "missingAmounts": {
    "type": "string",
    "description": "Missing Amounts"
   },
   "unsupportedCurrency": {
    "type": "string",
    "description": "Unsupported Currency"
   },
   "invalidDerivedRate": {
    "type": "number",
    "description": "Invalid Derived Rate"
   },
   "circularRateRelationship": {
    "type": "number",
    "description": "Circular Rate Relationship"
   }
  },
  "x-ticvai-record-definition": "Each rate should contain"
 },
 "RateStructureBuilderView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Rate Structure Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "d250": {
    "type": "string",
    "description": "d 250"
   },
   "childReduced": {
    "type": "string",
    "description": "Child Reduced (the pack shows 180)"
   },
   "seniorReduced": {
    "type": "string",
    "description": "Senior Reduced (the pack shows 190)"
   },
   "residentReduced": {
    "type": "string",
    "description": "Resident Reduced (the pack shows 210)"
   },
   "groupGroup": {
    "type": "string",
    "description": "Group Group (the pack shows 195)"
   },
   "rateId": {
    "type": "string",
    "description": "Rate ID"
   },
   "rateName": {
    "type": "number",
    "description": "Rate Name"
   },
   "rateCode": {
    "type": "number",
    "description": "Rate Code"
   },
   "priceCategory": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price Category"
   },
   "rateType": {
    "type": "number",
    "description": "Rate Type"
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Amount"
   },
   "currency": {
    "type": "string",
    "description": "Currency"
   },
   "unitBasis": {
    "type": "string",
    "description": "Unit Basis"
   },
   "precision": {
    "type": "string",
    "description": "Precision"
   },
   "roundingProfile": {
    "type": "string",
    "description": "Rounding Profile"
   },
   "status": {
    "type": "string",
    "description": "Status"
   },
   "perTicket": {
    "type": "string",
    "description": "Per Ticket"
   },
   "perPerson": {
    "type": "string",
    "description": "Per Person"
   },
   "perUnit": {
    "type": "string",
    "description": "Per Unit"
   },
   "perHour": {
    "type": "string",
    "description": "Per Hour"
   },
   "perDay": {
    "type": "string",
    "description": "Per Day"
   },
   "perSession": {
    "type": "string",
    "description": "Per Session"
   },
   "perResource": {
    "type": "string",
    "description": "Per Resource"
   },
   "perPackage": {
    "type": "string",
    "description": "Per Package"
   },
   "perMembershipPeriod": {
    "type": "string",
    "format": "date-time",
    "description": "Per Membership Period"
   },
   "missingAmounts": {
    "type": "string",
    "description": "Missing Amounts"
   },
   "unsupportedCurrency": {
    "type": "string",
    "description": "Unsupported Currency"
   },
   "invalidDerivedRate": {
    "type": "number",
    "description": "Invalid Derived Rate"
   },
   "circularRateRelationship": {
    "type": "number",
    "description": "Circular Rate Relationship"
   }
  }
 }
}
```
