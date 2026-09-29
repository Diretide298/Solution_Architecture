# WS34 — Pricing   Revenue Management board 1

**10 screens · 16 operations · 25 schemas · 5 permissions**

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

- **Every control that can be refused must be gated.** 5 permissions apply here:
  `PLATFORM_TENANT_VIEW, PRICE_CONFIGURE, PRICE_VIEW, PRODUCT_CONFIGURE, PRODUCT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-048` | Commercial Pricing Command Center | commandCentre | 4 | 1 | — |
| `ADM-049` | Price List Master Configuration | configEditor | 1 | 0 | — |
| `ADM-050` | Price Category & Rate Type Library | listDetail | 2 | 1 | — |
| `ADM-051` | Rate Structure Builder | listDetail | 1 | 0 | — |
| `ADM-052` | Product & Service Price Assignment | listDetail | 1 | 0 | — |
| `ADM-053` | Package, Bundle & Add-On Pricing | configEditor | 2 | 1 | — |
| `ADM-054` | Market, Venue & Currency Pricing Structure | configEditor | 2 | 1 | — |
| `ADM-055` | Price Hierarchy & Inheritance Configuration | configEditor | 1 | 0 | — |
| `ADM-056` | Price List Templates, Clone & Reuse | configEditor | 2 | 1 | — |
| `ADM-057` | Commercial Pricing Structure Validation | listDetail | 1 | 0 | — |

## Thin screens in this batch

**ADM-050, ADM-057 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

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
     "provenance": "derived — ADM-002 declares entryState.params  and ADM-048 holds none of them, so the edge carries nothing and ADM-002 opens cold"
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
  "purposeNote": "Authorized administrators can view and manage TICVAI's complete commercial pricing portfolio from one centralized workspace.",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each price list should show) — counts over a population, then the population",
  "purpose": "Provide the central administrative workspace for all commercial pricing structures across This is the first page a Revenue/Pricing Administrator sees when entering the module.",
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
       "bindsTo": "CommercialPricingCommandCenterSummary.totalPriceLists"
      },
      {
       "kind": "metricTile",
       "label": "Active Price Lists",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 6 §Display",
       "bindsTo": "CommercialPricingCommandCenterSummary.activePriceLists"
      },
      {
       "kind": "metricTile",
       "label": "Draft Price Lists",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 6 §Display",
       "bindsTo": "CommercialPricingCommandCenterSummary.draftPriceLists"
      },
      {
       "kind": "metricTile",
       "label": "Price Categories",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 6 §Display",
       "bindsTo": "CommercialPricingCommandCenterSummary.priceCategories"
      },
      {
       "kind": "metricTile",
       "label": "Configured Rates",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 6 §Display",
       "bindsTo": "CommercialPricingCommandCenterSummary.configuredRates"
      },
      {
       "kind": "metricTile",
       "label": "Products with Pricing",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 6 §Display",
       "bindsTo": "CommercialPricingCommandCenterSummary.productsWithPricing"
      },
      {
       "kind": "metricTile",
       "label": "Products Missing Pricing",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 6 §Display",
       "bindsTo": "CommercialPricingCommandCenterSummary.productsMissingPricing"
      },
      {
       "kind": "metricTile",
       "label": "Markets",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 6 §Display",
       "bindsTo": "CommercialPricingCommandCenterSummary.markets"
      },
      {
       "kind": "metricTile",
       "label": "Currencies",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 6 §Display",
       "bindsTo": "CommercialPricingCommandCenterSummary.currencies"
      },
      {
       "kind": "metricTile",
       "label": "Pricing Validation Issues",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 6 §Display",
       "bindsTo": "CommercialPricingCommandCenterSummary.pricingValidationIssues"
      },
      {
       "kind": "metricTile",
       "label": "Recently Modified Price Lists",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 6 §Display",
       "bindsTo": "CommercialPricingCommandCenterSummary.recentlyModifiedPriceLists"
      },
      {
       "kind": "metricTile",
       "label": "Upcoming Price Structures",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 6 §Display",
       "bindsTo": "CommercialPricingCommandCenterSummary.upcomingPriceStructures"
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
   },
   {
    "operationId": "listMembershipCommercialPricing",
    "contract": "subscription",
    "purpose": "Membership Commercial, Pricing & Channel Association",
    "trigger": "onLoad"
   },
   {
    "operationId": "listCommercialPricingStructure",
    "contract": "catalogue",
    "purpose": "Commercial Pricing Structure Validation",
    "trigger": "onLoad"
   },
   {
    "operationId": "listBundlePricingCommercial",
    "contract": "promotions",
    "purpose": "Bundle Pricing & Commercial Model",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-048",
   "workshopBoard": "wireframes/WS95 Pricing   Revenue Management Board 1.dc.html#adm-048"
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
  "purposeNote": "Administrators can create reusable commercial price-list masters with clearly defined ownership, scope, currency, market, and business applicability.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Create the master container that holds commercial rates. A Price List should be reusable across products and channels.",
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
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-049",
   "workshopBoard": "wireframes/WS95 Pricing   Revenue Management Board 1.dc.html#adm-049"
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
  "purposeNote": "types across all tenants, venues, and products.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Define standardized commercial rate categories used across TICVAI. This avoids different venues independently creating categories such as: “Adult,” “Adult Standard,” “Normal Adult,” and “Full Adult.”",
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
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save price category rate type",
       "operation": "setPriceCategoryRateType",
       "permission": "PRICE_CONFIGURE",
       "notes": "**The tenant's library of price categories and rate types** (29 September, writers pass).",
       "provenance": "contract catalogue.yaml PUT /price-categories"
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
   },
   {
    "operationId": "setPriceCategoryRateType",
    "contract": "catalogue",
    "purpose": "Create or update a price category or rate type",
    "trigger": "onAction",
    "invalidates": [
     "listPriceCategoryRate"
    ]
   }
  ],
  "entryState": {
   "preloaded": []
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-050",
   "workshopBoard": "wireframes/WS95 Pricing   Revenue Management Board 1.dc.html#adm-050"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 9. 0 of 0 labels bound to a contract property; 0 of 49 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formSetPriceCategoryRateType",
    "component": "modal",
    "trigger": "Save price category rate type",
    "body": "**Collects what `setPriceCategoryRateType` sends before it is called.** Required: `id`, `scopePath`, `entryKind`, `code`, `name`, `isActive`. Optional: `description`, `categoryFamily`, `displayName`, `localizedDisplayNames`, `iconLabel`, `parentId`, `isStandard`, `sortOrder`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "PriceCategory",
    "confirm": {
     "label": "Save price category rate type",
     "operation": "setPriceCategoryRateType"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "scopePath",
      "entryKind",
      "code",
      "name",
      "isActive",
      "description",
      "categoryFamily",
      "displayName",
      "localizedDisplayNames",
      "iconLabel",
      "parentId",
      "isStandard",
      "sortOrder"
     ]
    },
    "provenance": "contract catalogue.yaml PUT /price-categories"
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
  "purposeNote": "Administrators can define monetary rate structures for all TICVAI commercial product types through configurable rate matrices.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Detect) and no metric row",
  "purpose": "Define the actual monetary rates contained within a price list. This is the core commercial configuration screen.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 4 actions on this screen and the screen declares 1 operation.** Unserved: Per Ticket, Per Resource, Per Package, Per Membership Period. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
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
        "RateStructureBuilderView.validationIssues"
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
        "RateStructureBuilderView.validationIssues"
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
       "label": "Per Resource",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 11 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Per Package",
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
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "preloaded": [
    "Duplicate Rates",
    "RateStructureBuilderView.validationIssues"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-051",
   "workshopBoard": "wireframes/WS95 Pricing   Revenue Management Board 1.dc.html#adm-051"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 11. 4 of 5 labels bound to a contract property; 9 of 47 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "purposeNote": "All sellable TICVAI objects can reference centrally managed price lists and rates without maintaining duplicate price definitions inside business modules.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Product configuration should display) and no metric row",
  "purpose": "Connect commercial rates to the actual products and services being sold.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 5 actions on this screen and the screen declares 1 operation.** Unserved: Ticket Type, Event, Venue. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
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
       "label": "Product Level",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 13 §Allow"
      },
      {
       "kind": "secondaryButton",
       "label": "Product Variant",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 13 §Allow"
      },
      {
       "kind": "secondaryButton",
       "label": "Ticket Type",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 13 §Allow"
      },
      {
       "kind": "secondaryButton",
       "label": "Event",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 13 §Allow"
      },
      {
       "kind": "secondaryButton",
       "label": "Venue",
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
    "trigger": "onAction"
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-052",
   "workshopBoard": "wireframes/WS95 Pricing   Revenue Management Board 1.dc.html#adm-052"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 13. 0 of 1 labels bound to a contract property; 7 of 37 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "purposeNote": "Packages, bundles, and add-ons can use centralized commercial pricing while their product composition remains owned by the Product Catalogue.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure pricing for; Configure whether the customer sees) and no display directory — it is settings, not a population",
  "purpose": "Provide dedicated commercial structures for products containing multiple components. This is separate from the Product Relationship/Bundle module. Product Catalogue defines what the bundle contains. Pricing defines how that bundle is priced.",
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
       "label": "Fixed Package Price",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 14 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Component Override",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 14 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Save package pricing definition",
       "operation": "setPackagePricingDefinition",
       "permission": "PRICE_CONFIGURE",
       "notes": "**The pricing model of a package, bundle or add-on** (29 September, writers pass).",
       "provenance": "contract catalogue.yaml PUT /package-pricing"
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
   },
   {
    "operationId": "setPackagePricingDefinition",
    "contract": "catalogue",
    "purpose": "Set how a package, bundle or add-on is priced",
    "trigger": "onAction",
    "invalidates": [
     "listPackageBundleAdd"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-053",
   "workshopBoard": "wireframes/WS95 Pricing   Revenue Management Board 1.dc.html#adm-053"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 14. 0 of 0 labels bound to a contract property; 13 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formSetPackagePricingDefinition",
    "component": "modal",
    "trigger": "Save package pricing definition",
    "body": "**Collects what `setPackagePricingDefinition` sends before it is called.** Required: `id`, `scopePath`, `productId`, `recordKind`, `pricingModel`, `status`. Optional: `name`, `priceListId`, `addOnType`, `packagePrice`, `components`, `componentPriceVisibility`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "PackagePricing",
    "confirm": {
     "label": "Save package pricing definition",
     "operation": "setPackagePricingDefinition"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "scopePath",
      "productId",
      "recordKind",
      "pricingModel",
      "status",
      "name",
      "priceListId",
      "addOnType",
      "packagePrice",
      "components",
      "componentPriceVisibility"
     ]
    },
    "provenance": "contract catalogue.yaml PUT /package-pricing"
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
  "purposeNote": "entities, and currencies.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure; FX-Assisted Setup) and no display directory — it is settings, not a population",
  "purpose": "Support TICVAI's multi-country, multi-market, multi-venue and multi-currency commercial model.",
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
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save market pricing configuration",
       "operation": "setMarketPricingConfiguration",
       "permission": "PRICE_CONFIGURE",
       "notes": "**Global, country, region, market or venue** (29 September, writers pass).",
       "provenance": "contract catalogue.yaml PUT /pricing-markets"
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
   },
   {
    "operationId": "setMarketPricingConfiguration",
    "contract": "catalogue",
    "purpose": "Create or update a node of the market pricing structure",
    "trigger": "onAction",
    "invalidates": [
     "listMarketVenueCurrency"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-054",
   "workshopBoard": "wireframes/WS95 Pricing   Revenue Management Board 1.dc.html#adm-054"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 15. 0 of 0 labels bound to a contract property; 8 of 32 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formSetMarketPricingConfiguration",
    "component": "modal",
    "trigger": "Save market pricing configuration",
    "body": "**Collects what `setMarketPricingConfiguration` sends before it is called.** Required: `id`, `scopePath`, `hierarchyLevel`. Optional: `parentId`, `countryCode`, `marketCode`, `region`, `venueId`, `brand`, `legalEntityId`, `baseCurrency`, `sellingCurrency`, `roundingProfileId`, `displayFormat`, `priceListId` and 2 more. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "PricingMarket",
    "confirm": {
     "label": "Save market pricing configuration",
     "operation": "setMarketPricingConfiguration"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "scopePath",
      "hierarchyLevel",
      "parentId",
      "countryCode",
      "marketCode",
      "region",
      "venueId",
      "brand",
      "legalEntityId",
      "baseCurrency",
      "sellingCurrency",
      "roundingProfileId",
      "displayFormat",
      "priceListId",
      "inheritsFromParent",
      "fxReferenceRate"
     ]
    },
    "provenance": "contract catalogue.yaml PUT /pricing-markets"
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
  "purposeNote": "The platform deterministically resolves the correct commercial price source across global, market, venue, and product hierarchies.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Administrators configure; Configure) and no display directory — it is settings, not a population",
  "purpose": "Define where TICVAI should obtain a price when multiple commercial pricing layers exist. This is essential to prevent conflicting prices.",
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
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-055",
   "workshopBoard": "wireframes/WS95 Pricing   Revenue Management Board 1.dc.html#adm-055"
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
  "purposeNote": "Administrators can rapidly create consistent commercial pricing structures by cloning and reusing approved templates instead of rebuilding pricing manually.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Options) and no display directory — it is settings, not a population",
  "purpose": "Accelerate commercial setup across new venues, events, seasons and markets.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 5 actions on this screen and the screen declares 1 operation.** Unserved: Complete Price List, Rate Structure Only, Selected Categories, Product Assignments, Market Structure. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
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
      },
      {
       "kind": "secondaryButton",
       "label": "Rate Structure Only",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 18 §Allow cloning"
      },
      {
       "kind": "secondaryButton",
       "label": "Selected Categories",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 18 §Allow cloning"
      },
      {
       "kind": "secondaryButton",
       "label": "Product Assignments",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 18 §Allow cloning"
      },
      {
       "kind": "secondaryButton",
       "label": "Market Structure",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 18 §Allow cloning"
      },
      {
       "kind": "secondaryButton",
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
   },
   {
    "operationId": "setConfigurationTemplate",
    "contract": "catalogue",
    "purpose": "Create or update a product or price-list template",
    "trigger": "onAction",
    "invalidates": [
     "listPriceListTemplate"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-056",
   "workshopBoard": "wireframes/WS95 Pricing   Revenue Management Board 1.dc.html#adm-056"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 18. 0 of 0 labels bound to a contract property; 10 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "purposeNote": "from progressing downstream without clearly identifying the issue. Board 1 — Final Screen Register # Screen Responsibility 10.1. Commercial Pricing Command",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Validate that the commercial pricing foundation is structurally complete before it proceeds to rule configuration, governance, or publication. This is not the final publication screen. Board 4 owns approval and publication. Board 1 defined what the commercial prices are and how they are structured.",
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
    "CommercialPricingStructureValidationView.check"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-057",
   "workshopBoard": "wireframes/WS95 Pricing   Revenue Management Board 1.dc.html#adm-057"
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
 "listBundlePricingCommercial": {
  "method": "GET",
  "path": "/bundle-pricing-commercial",
  "contract": "promotions",
  "summary": "Bundle Pricing & Commercial Model",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "BundlePricingCommercialModelView"
 },
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
   },
   {
    "name": "venue",
    "in": "query",
    "required": false
   },
   {
    "name": "brand",
    "in": "query",
    "required": false
   },
   {
    "name": "market",
    "in": "query",
    "required": false
   },
   {
    "name": "currency",
    "in": "query",
    "required": false
   },
   {
    "name": "owner",
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
 "listCommercialPricingStructure": {
  "method": "GET",
  "path": "/commercial-pricing-structure",
  "contract": "catalogue",
  "summary": "Commercial Pricing Structure Validation",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "severity",
    "in": "query",
    "required": false
   },
   {
    "name": "category",
    "in": "query",
    "required": false
   },
   {
    "name": "priceListId",
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
 "listMarketVenueCurrency": {
  "method": "GET",
  "path": "/market-venue-currency",
  "contract": "catalogue",
  "summary": "Market, Venue & Currency Pricing Structure",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "hierarchyLevel",
    "in": "query",
    "required": false
   },
   {
    "name": "country",
    "in": "query",
    "required": false
   },
   {
    "name": "market",
    "in": "query",
    "required": false
   },
   {
    "name": "venue",
    "in": "query",
    "required": false
   },
   {
    "name": "legalEntity",
    "in": "query",
    "required": false
   },
   {
    "name": "currency",
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
 "listMembershipCommercialPricing": {
  "method": "GET",
  "path": "/membership-commercial-pricing",
  "contract": "subscription",
  "summary": "Membership Commercial, Pricing & Channel Association",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "membershipCode",
    "in": "query",
    "required": false
   },
   {
    "name": "channel",
    "in": "query",
    "required": false
   },
   {
    "name": "salesPeriod",
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
 "listPackageBundleAdd": {
  "method": "GET",
  "path": "/package-bundle-add",
  "contract": "catalogue",
  "summary": "Package, Bundle & Add-On Pricing",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "recordKind",
    "in": "query",
    "required": false
   },
   {
    "name": "pricingModel",
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
 "listPriceCategoryRate": {
  "method": "GET",
  "path": "/price-category-rate",
  "contract": "catalogue",
  "summary": "Price Category & Rate Type Library",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "entryKind",
    "in": "query",
    "required": false
   },
   {
    "name": "categoryFamily",
    "in": "query",
    "required": false
   },
   {
    "name": "active",
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
 "listPriceListTemplate": {
  "method": "GET",
  "path": "/price-list-template",
  "contract": "catalogue",
  "summary": "Price List Templates, Clone & Reuse",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "templateType",
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
 "setMarketPricingConfiguration": {
  "method": "PUT",
  "path": "/pricing-markets",
  "contract": "catalogue",
  "summary": "Create or update a node of the market pricing structure",
  "permission": "PRICE_CONFIGURE",
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
  "requestBody": "PricingMarket",
  "responds": "PricingMarket"
 },
 "setPackagePricingDefinition": {
  "method": "PUT",
  "path": "/package-pricing",
  "contract": "catalogue",
  "summary": "Set how a package, bundle or add-on is priced",
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
  "requestBody": "PackagePricing",
  "responds": "PackagePricing"
 },
 "setPriceCategoryRateType": {
  "method": "PUT",
  "path": "/price-categories",
  "contract": "catalogue",
  "summary": "Create or update a price category or rate type",
  "permission": "PRICE_CONFIGURE",
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
  "requestBody": "PriceCategory",
  "responds": "PriceCategory"
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "RateStructureBuilderInput",
  "responds": "RateStructureBuilderView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "BundlePricingCommercialModelView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Bundle Pricing & Commercial Model displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "basePrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Base price"
   },
   "currency": {
    "type": "string",
    "description": "Currency"
   },
   "discount": {
    "type": "number",
    "description": "Discount %"
   },
   "discountAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Discount amount"
   },
   "minimumPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Minimum price"
   },
   "maximumPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Maximum price"
   },
   "priceFloor": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price floor"
   },
   "marginFloor": {
    "type": "number",
    "description": "Margin floor"
   },
   "guestSpecificPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Guest-specific price"
   },
   "channelSpecificPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Channel-specific price"
   },
   "pricingModel": {
    "type": "string",
    "enum": [
     "fixedBundlePrice",
     "sumMinusDiscount",
     "componentPricing",
     "startingFrom",
     "tieredBundlePrice",
     "dynamicBundlePrice"
    ],
    "description": "How the bundle is priced; a dynamic bundle price is calculated by the pricing engine"
   },
   "upgradeCharge": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Surcharge when the guest picks a premium option"
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
 "CommercialPricingCommandCenterSummary": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection; the headline tiles over the list, computed at read time for the filters in force",
  "description": "**The headline figures on Commercial Pricing Command Center.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.",
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
    "type": "integer",
    "description": "Products with Pricing: sellable products that reference at least one active price list rate"
   },
   "productsMissingPricing": {
    "type": "integer",
    "description": "Products Missing Pricing: active sellable products with no price list rate"
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
    "type": "integer",
    "description": "Recently Modified Price Lists: price lists changed in the last 7 days (decided 29 September, readiness close-out)"
   },
   "upcomingPriceStructures": {
    "type": "integer",
    "description": "Upcoming Price Structures: price lists whose effective-from date is in the future"
   },
   "aiInsights": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "AI observations for this screen; advisory only, never applied automatically"
   }
  }
 },
 "CommercialPricingCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Commercial Pricing Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
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
    "enum": [
     "standardRetail",
     "venue",
     "attraction",
     "event",
     "membership",
     "group",
     "corporate",
     "b2b",
     "reseller",
     "ota",
     "internal",
     "specialMarket"
    ],
    "description": "Price List Type (the pack's Price List Types, pp.6-7)"
   },
   "currency": {
    "type": "string",
    "description": "Currency: ISO 4217 code of the default currency",
    "pattern": "^[A-Z]{3}$"
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
   "version": {
    "type": "string",
    "description": "Version"
   },
   "status": {
    "type": "string",
    "description": "Status: draft, configured, validated, active, inactive, expired or archived (p.7); approval and publication are Board 4's"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date",
    "description": "Effective From (the first half of the pack's Effective Period)"
   },
   "effectiveTo": {
    "type": "string",
    "format": "date",
    "description": "Effective To; empty for open-ended",
    "nullable": true
   }
  }
 },
 "CommercialPricingStructureValidationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Commercial Pricing Structure Validation displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "findingId": {
    "type": "string",
    "description": "Finding ID"
   },
   "category": {
    "type": "string",
    "enum": [
     "priceList",
     "rateStructure",
     "productMapping",
     "package",
     "market",
     "hierarchy"
    ],
    "description": "Validation Category (pp.19-20)"
   },
   "check": {
    "type": "string",
    "enum": [
     "requiredFieldsComplete",
     "currencyDefined",
     "ownershipAssigned",
     "categoriesConfigured",
     "monetaryValuesValid",
     "derivedRelationshipsValid",
     "requiredProductsPriced",
     "noOrphanAssignments",
     "componentPricingValid",
     "currencyAndVenueConfigurationValid",
     "noConflictingSourcePriority",
     "fallbackConfigured"
    ],
    "description": "The check that failed"
   },
   "severity": {
    "type": "string",
    "enum": [
     "critical",
     "warning",
     "information"
    ],
    "description": "Validation Results: critical (sale cannot proceed), warning (review), information (optimization suggestion)"
   },
   "message": {
    "type": "string",
    "description": "What was found, e.g. \"7 active ticket products have no Adult rate\""
   },
   "subjectType": {
    "type": "string",
    "enum": [
     "priceList",
     "rate",
     "priceCategory",
     "product",
     "package",
     "venue",
     "market",
     "hierarchy"
    ],
    "description": "What the finding is about"
   },
   "subjectId": {
    "type": "string",
    "description": "ID of that record"
   },
   "aiGenerated": {
    "type": "boolean",
    "description": "Raised by AI QA rather than a rule; advisory"
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
 "LocalisedText": {
  "x-ticvai-persistence": "none — jsonb column",
  "type": "object",
  "additionalProperties": {
   "type": "string"
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
   "baseCurrency": {
    "type": "string",
    "description": "Base Currency: ISO 4217 code",
    "pattern": "^[A-Z]{3}$"
   },
   "sellingCurrency": {
    "type": "string",
    "description": "Selling Currency: ISO 4217 code",
    "pattern": "^[A-Z]{3}$"
   },
   "currencyPrecision": {
    "type": "integer",
    "description": "Currency Precision: decimal places, 0 to 3",
    "minimum": 0,
    "maximum": 3
   },
   "rounding": {
    "type": "string",
    "description": "Rounding: code of the currency rounding rule (ADM-075)"
   },
   "displayFormat": {
    "type": "string",
    "description": "Display Format: e.g. \"AED 1,250.00\" or \"1.250,00 EUR\""
   },
   "structureId": {
    "type": "string",
    "description": "Pricing structure node ID"
   },
   "hierarchyLevel": {
    "type": "string",
    "enum": [
     "global",
     "country",
     "region",
     "market",
     "venue"
    ],
    "description": "Level of this node in the Market Hierarchy (p.15)"
   },
   "parentStructureId": {
    "type": "string",
    "nullable": true,
    "description": "Parent node; empty for Global"
   },
   "priceListId": {
    "type": "string",
    "nullable": true,
    "description": "Price list governing this node; empty when it inherits"
   },
   "inheritsFromParent": {
    "type": "boolean",
    "description": "Venue Overrides (p.16): true when the node uses its parent's prices (Abu Dhabi Venue -> inherit AED 250)"
   },
   "fxReferenceRate": {
    "type": "number",
    "nullable": true,
    "description": "FX-Assisted Setup: reference rate base -> selling currency shown during setup; advisory"
   }
  }
 },
 "MembershipCommercialPricingChannelAssociationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Membership Commercial, Pricing & Channel Association displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "basePricingProfile": {
    "type": "string",
    "description": "Base Pricing Profile id"
   },
   "membershipTierPrice": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Membership Tier Price, as calculated by the linked pricing profile (read-only)"
   },
   "renewalPrice": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "Renewal Price, as calculated by the linked renewal pricing (read-only)"
   },
   "promotionalPricingEligibility": {
    "type": "boolean",
    "description": "Promotional Pricing Eligibility: promotions may apply to this membership"
   },
   "taxProfile": {
    "type": "string",
    "description": "Tax Profile id"
   },
   "feeProfile": {
    "type": "string",
    "description": "Fee Profile id",
    "nullable": true
   },
   "salesCapacity": {
    "type": "integer",
    "description": "Capacity limit for a capacityLimited sales period",
    "nullable": true
   },
   "membershipCode": {
    "type": "string",
    "description": "Membership code"
   },
   "upgradePricePolicy": {
    "type": "string",
    "description": "Upgrade Price Policy id (pack p.14); pro-rata credit on upgrade per MoM 1 Sep §4.9",
    "nullable": true
   },
   "availableChannels": {
    "type": "array",
    "items": {
     "$ref": "../shared/common.yaml#/components/schemas/SalesChannel"
    },
    "description": "Channel Availability (pack p.14): B2C -> guestWeb, Mobile App -> guestApp, POS and Box Office -> pos, Call Center -> callCentre, Kiosk -> kiosk, B2B and Corporate -> b2b, Reseller -> partner, API -> api"
   },
   "paymentTerms": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "fullPayment",
      "installments",
      "corporateCredit",
      "autoRenewPayment"
     ]
    },
    "description": "Payment Eligibility (pp.14-15); installments only where the payments module supports them"
   },
   "salesPeriod": {
    "type": "string",
    "enum": [
     "alwaysAvailable",
     "fixedSalesWindow",
     "seasonalSale",
     "invitationOnly",
     "capacityLimited"
    ],
    "description": "Sales Period (pack p.15)"
   },
   "billingFrequency": {
    "type": "string",
    "enum": [
     "upFront",
     "monthly",
     "quarterly",
     "semiAnnual",
     "annual",
     "custom"
    ],
    "default": "upFront",
    "description": "2.14.19 (29 September, build). **How often the member is charged, independent of the validity term**: an annual membership may be billed monthly or quarterly. `upFront` charges the whole term at sale. A recurring frequency needs `autoRenewPayment` or `installments` in `paymentTerms` and a card on file under a recurring mandate; each cycle is an instalment of the plan payments `createInstalmentPlan` schedules at sale, charged to the stored card on its due date."
   },
   "billingIntervalMonths": {
    "type": "integer",
    "minimum": 1,
    "maximum": 24,
    "nullable": true,
    "description": "For `custom`, every how many months. Null otherwise."
   },
   "billingAnchor": {
    "type": "string",
    "enum": [
     "purchaseDate",
     "calendarMonthStart"
    ],
    "default": "purchaseDate",
    "description": "`purchaseDate` bills on the purchase day each cycle; `calendarMonthStart` on the 1st of the month, the first cycle prorated. A cycle longer than the term is refused (422)."
   },
   "salesWindowFrom": {
    "type": "string",
    "format": "date",
    "description": "Sales window start, for fixedSalesWindow or seasonalSale",
    "nullable": true
   },
   "salesWindowTo": {
    "type": "string",
    "format": "date",
    "description": "Sales window end",
    "nullable": true
   }
  }
 },
 "PackageBundleAddOnPricingView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Package, Bundle & Add-On Pricing displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "packagePrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Package Price: the fixed or derived price charged for the package (AED 850 in the example)"
   },
   "pricingId": {
    "type": "string",
    "description": "Package / add-on pricing ID"
   },
   "recordKind": {
    "type": "string",
    "enum": [
     "package",
     "bundle",
     "addOn"
    ],
    "description": "What is priced"
   },
   "productId": {
    "type": "string",
    "description": "The catalogue package, bundle or add-on product"
   },
   "name": {
    "type": "string",
    "description": "Name"
   },
   "priceListId": {
    "type": "string",
    "description": "Price list the pricing belongs to"
   },
   "pricingModel": {
    "type": "string",
    "enum": [
     "fixedPackagePrice",
     "sumOfComponents",
     "discountedComponentSum",
     "componentOverride"
    ],
    "description": "Package Pricing Model (p.14)",
    "nullable": true
   },
   "addOnType": {
    "type": "string",
    "enum": [
     "fastTrack",
     "parking",
     "meal",
     "photo",
     "equipment",
     "upgrade",
     "additionalPerformance",
     "premiumAccess",
     "other"
    ],
    "description": "Add-On Pricing kind (p.15); additionalPerformance is the design's \"additional session\"; empty for a package",
    "nullable": true
   },
   "components": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "productId": {
       "type": "string"
      },
      "quantity": {
       "type": "integer"
      },
      "role": {
       "type": "string",
       "enum": [
        "included",
        "requiredPaid",
        "optionalPaid"
       ]
      },
      "componentPrice": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      }
     }
    },
    "description": "Components with their role (Required vs Optional, p.15) and the price each contributes"
   },
   "normalTotal": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Normal Total: sum of the components at their own rates; read-only"
   },
   "packageSaving": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Commercial package saving: normal total less package price; read-only"
   },
   "componentPriceVisibility": {
    "type": "string",
    "enum": [
     "packageTotalOnly",
     "individualComponents",
     "componentAndSaving"
    ],
    "description": "Component Price Visibility (p.15): what the customer sees"
   },
   "status": {
    "type": "string",
    "description": "Status: draft, active, disabled or expired"
   },
   "validationIssues": {
    "type": "array",
    "description": "Bundle Price Integrity (p.15)",
    "items": {
     "type": "object",
     "properties": {
      "code": {
       "type": "string",
       "enum": [
        "componentPriceChanged",
        "missingComponentRate",
        "packageAboveNormalTotal"
       ]
      },
      "message": {
       "type": "string"
      }
     }
    }
   }
  }
 },
 "PackagePricing": {
  "type": "object",
  "x-ticvai-persistence": "catalogue.package_pricing",
  "description": "**How a package, bundle or add-on is priced from its components** (29 September, data model DM3). ADM-062. The bundle's composition for sale stays `catalogue.published_bundle`; this row is its pricing model. `normalTotal` and `packageSaving` are computed on read from the component rates.",
  "required": [
   "id",
   "scopePath",
   "productId",
   "recordKind",
   "pricingModel",
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
   "productId": {
    "type": "string",
    "format": "uuid"
   },
   "recordKind": {
    "type": "string",
    "enum": [
     "package",
     "bundle",
     "addOn"
    ]
   },
   "name": {
    "type": "string",
    "maxLength": 200,
    "nullable": true
   },
   "priceListId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "pricingModel": {
    "type": "string",
    "enum": [
     "fixedPackagePrice",
     "sumOfComponents",
     "discountedComponentSum",
     "componentOverride"
    ]
   },
   "addOnType": {
    "type": "string",
    "enum": [
     "fastTrack",
     "parking",
     "meal",
     "photo",
     "equipment",
     "upgrade",
     "additionalPerformance",
     "premiumAccess",
     "other",
     null
    ],
    "nullable": true
   },
   "packagePrice": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true
   },
   "components": {
    "type": "object",
    "additionalProperties": true,
    "description": "`[{productId, quantity, role, componentPrice}]`; `componentPrice` only for `componentOverride`."
   },
   "componentPriceVisibility": {
    "type": "string",
    "enum": [
     "packageTotalOnly",
     "individualComponents",
     "componentAndSaving"
    ],
    "default": "packageTotalOnly"
   },
   "status": {
    "allOf": [
     {
      "$ref": "#/components/schemas/CatalogueConfigStatus"
     }
    ],
    "default": "draft"
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
 "PriceCategory": {
  "type": "object",
  "x-ticvai-persistence": "catalogue.price_category",
  "description": "**The library of price categories and rate types** (29 September, data model DM3). ADM-059. A price category is who or what is priced (Adult, Child, Resident ...); a rate type is how (Standard, Peak, Member ...). Both are rows here, `entryKind` says which. Distinct from `catalogue.product_category`, which groups merchandise.",
  "required": [
   "id",
   "scopePath",
   "entryKind",
   "code",
   "name",
   "isActive"
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
    "description": "**The partition key** (ADR-0005). Operations write it at `tenant` scope."
   },
   "entryKind": {
    "type": "string",
    "enum": [
     "priceCategory",
     "rateType"
    ]
   },
   "code": {
    "type": "string",
    "maxLength": 40,
    "description": "Unique per `entryKind` within the tenant."
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "description": {
    "type": "string",
    "nullable": true
   },
   "categoryFamily": {
    "type": "string",
    "maxLength": 60,
    "nullable": true
   },
   "displayName": {
    "type": "string",
    "maxLength": 200,
    "nullable": true
   },
   "localizedDisplayNames": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "nullable": true
   },
   "iconLabel": {
    "type": "string",
    "maxLength": 40,
    "nullable": true
   },
   "parentId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "A parent `catalogue.price_category` of the same `entryKind`."
   },
   "isStandard": {
    "type": "boolean",
    "default": false,
    "description": "Shipped with the tenant; may be deactivated, not deleted."
   },
   "sortOrder": {
    "type": "integer",
    "default": 100
   },
   "isActive": {
    "type": "boolean",
    "default": true
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
 "PriceCategoryRateTypeLibraryView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Price Category & Rate Type Library displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
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
    "description": "Category Family: e.g. Visitor or Member (Parent/Child Structure, p.10)"
   },
   "displayName": {
    "type": "string",
    "description": "Display Name"
   },
   "iconLabel": {
    "type": "string",
    "description": "Icon/Label"
   },
   "active": {
    "type": "boolean",
    "description": "Active/Inactive: true when the category can be used on new rates"
   },
   "entryKind": {
    "type": "string",
    "enum": [
     "priceCategory",
     "rateType"
    ],
    "description": "Whether the row is a price category (who the price represents) or a rate type (how the rate behaves: standard, reduced, contract, negotiated, complimentary, fixed, derived, package, add-on), p.10"
   },
   "standard": {
    "type": "boolean",
    "description": "A TICVAI standard category (Adult, Child, Junior, Senior, Student, Resident, Non-Resident, Member, VIP, Group, Corporate, B2B, Complimentary, Staff, Promotional) rather than a custom one"
   },
   "sortOrder": {
    "type": "integer",
    "description": "Sort Order"
   },
   "parentCategoryId": {
    "type": "string",
    "nullable": true,
    "description": "Parent category (Parent/Child Structure: Visitor -> Adult, Member -> Gold); empty for a top-level category"
   },
   "localizedDisplayNames": {
    "type": "object",
    "additionalProperties": {
     "type": "string"
    },
    "description": "Display name per language code, at least en and ar (Localization, p.11)"
   },
   "possibleDuplicateOf": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "AI Standardization: ids of categories that appear to mean the same thing (Kids / Child / Children Rate); advisory"
   }
  }
 },
 "PriceHierarchyInheritanceConfigurationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table covers these fields** — the closest is catalogue.price_list at 17%, so this is not an update to anything the package stores today and no new table has been decided",
  "description": "**What Price Hierarchy & Inheritance Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "hierarchyId": {
    "type": "string",
    "description": "Price hierarchy ID; empty on create"
   },
   "name": {
    "type": "string",
    "description": "Hierarchy name"
   },
   "levels": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "hierarchyLevel": {
       "type": "string",
       "enum": [
        "globalMaster",
        "country",
        "market",
        "venue",
        "product",
        "approvedOverride"
       ],
       "description": "Hierarchy Level (Example Hierarchy, p.17)"
      },
      "priority": {
       "type": "integer",
       "description": "Priority; the lower number is the more general level, the most specific existing price wins"
      },
      "inheritance": {
       "type": "boolean",
       "description": "Inheritance: the level takes its parent's price when it has none of its own"
      },
      "overrideAllowed": {
       "type": "boolean",
       "description": "Override Permission / Override Allowed"
      },
      "overrideRequiresReason": {
       "type": "boolean",
       "description": "Override Requires Reason"
      },
      "maximumOverrideRangePercent": {
       "type": "number",
       "nullable": true,
       "description": "Maximum Override Range: largest allowed deviation from the parent price, in percent; empty for no limit"
      },
      "overrideExpiryDays": {
       "type": "integer",
       "nullable": true,
       "description": "Override Expiry: days an override stays in force; empty for no expiry (decided 29 September, readiness close-out)"
      },
      "returnToParentPrice": {
       "type": "boolean",
       "description": "Return to Parent Price when an override expires"
      },
      "fallbackBehavior": {
       "type": "string",
       "enum": [
        "useParent",
        "useDefault",
        "blockSale"
       ],
       "description": "Fallback (p.18): what happens when a child rate does not exist"
      }
     }
    },
    "description": "Hierarchy Builder (p.17): the ordered levels; saved as a whole so two sources can never be left at equal priority"
   }
  }
 },
 "PriceHierarchyInheritanceConfigurationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Price Hierarchy & Inheritance Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "hierarchyId": {
    "type": "string",
    "description": "Price hierarchy ID; empty on create"
   },
   "name": {
    "type": "string",
    "description": "Hierarchy name"
   },
   "levels": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "hierarchyLevel": {
       "type": "string",
       "enum": [
        "globalMaster",
        "country",
        "market",
        "venue",
        "product",
        "approvedOverride"
       ],
       "description": "Hierarchy Level (Example Hierarchy, p.17)"
      },
      "priority": {
       "type": "integer",
       "description": "Priority; the lower number is the more general level, the most specific existing price wins"
      },
      "inheritance": {
       "type": "boolean",
       "description": "Inheritance: the level takes its parent's price when it has none of its own"
      },
      "overrideAllowed": {
       "type": "boolean",
       "description": "Override Permission / Override Allowed"
      },
      "overrideRequiresReason": {
       "type": "boolean",
       "description": "Override Requires Reason"
      },
      "maximumOverrideRangePercent": {
       "type": "number",
       "nullable": true,
       "description": "Maximum Override Range: largest allowed deviation from the parent price, in percent; empty for no limit"
      },
      "overrideExpiryDays": {
       "type": "integer",
       "nullable": true,
       "description": "Override Expiry: days an override stays in force; empty for no expiry (decided 29 September, readiness close-out)"
      },
      "returnToParentPrice": {
       "type": "boolean",
       "description": "Return to Parent Price when an override expires"
      },
      "fallbackBehavior": {
       "type": "string",
       "enum": [
        "useParent",
        "useDefault",
        "blockSale"
       ],
       "description": "Fallback (p.18): what happens when a child rate does not exist"
      }
     }
    },
    "description": "Hierarchy Builder (p.17): the ordered levels; saved as a whole so two sources can never be left at equal priority"
   },
   "validationIssues": {
    "type": "array",
    "description": "Conflict Detection (p.18); read-only",
    "items": {
     "type": "object",
     "properties": {
      "code": {
       "type": "string",
       "enum": [
        "equalPriority",
        "missingFallback",
        "circularInheritance"
       ]
      },
      "message": {
       "type": "string"
      }
     }
    }
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
    "type": "string",
    "description": "Price List Name"
   },
   "priceListCode": {
    "type": "string",
    "description": "Price List Code; unique within the tenant"
   },
   "description": {
    "type": "string",
    "description": "Description"
   },
   "priceListType": {
    "type": "string",
    "enum": [
     "standardRetail",
     "venue",
     "attraction",
     "event",
     "membership",
     "group",
     "corporate",
     "b2b",
     "reseller",
     "ota",
     "internal",
     "specialMarket"
    ],
    "description": "Price List Type (Commercial Types, pp.8-9, and the directory's Price List Types)"
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
    "description": "Default Currency: ISO 4217 code",
    "pattern": "^[A-Z]{3}$"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   },
   "tags": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Tags"
   },
   "status": {
    "type": "string",
    "description": "Status: draft, configured, inactive or archived are set here; validated is set by structure validation (ADM-057) and active / expired by Board 4 publication"
   },
   "defaultRateCategory": {
    "type": "string",
    "description": "Default Rate Category: code of a price category from the library (ADM-050)"
   },
   "defaultRoundingProfile": {
    "type": "string",
    "description": "Default Rounding Profile: code of a currency rounding rule (ADM-075)"
   },
   "defaultPriceHierarchy": {
    "type": "string",
    "description": "Default Price Hierarchy: id of the price hierarchy (ADM-055) this list resolves against"
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
   "priceListId": {
    "type": "string",
    "description": "Price List ID; empty on create, the list to update otherwise"
   },
   "scope": {
    "type": "string",
    "enum": [
     "global",
     "country",
     "market",
     "brand",
     "venue",
     "event",
     "businessUnit"
    ],
    "description": "Scope: where the price list can apply (p.8)"
   },
   "clonedFromPriceListId": {
    "type": "string",
    "nullable": true,
    "description": "The price list this one was duplicated from (Duplicate, p.9: UAE Standard 2026 into UAE Standard 2027); empty when built from scratch"
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
    "type": "string",
    "description": "Price List Name"
   },
   "priceListCode": {
    "type": "string",
    "description": "Price List Code; unique within the tenant"
   },
   "description": {
    "type": "string",
    "description": "Description"
   },
   "priceListType": {
    "type": "string",
    "enum": [
     "standardRetail",
     "venue",
     "attraction",
     "event",
     "membership",
     "group",
     "corporate",
     "b2b",
     "reseller",
     "ota",
     "internal",
     "specialMarket"
    ],
    "description": "Price List Type (Commercial Types, pp.8-9, and the directory's Price List Types)"
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
    "description": "Default Currency: ISO 4217 code",
    "pattern": "^[A-Z]{3}$"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   },
   "tags": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Tags"
   },
   "status": {
    "type": "string",
    "description": "Status: draft, configured, inactive or archived are set here; validated is set by structure validation (ADM-057) and active / expired by Board 4 publication"
   },
   "defaultRateCategory": {
    "type": "string",
    "description": "Default Rate Category: code of a price category from the library (ADM-050)"
   },
   "defaultRoundingProfile": {
    "type": "string",
    "description": "Default Rounding Profile: code of a currency rounding rule (ADM-075)"
   },
   "defaultPriceHierarchy": {
    "type": "string",
    "description": "Default Price Hierarchy: id of the price hierarchy (ADM-055) this list resolves against"
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
   "priceListId": {
    "type": "string",
    "description": "Price List ID; empty on create, the list to update otherwise"
   },
   "scope": {
    "type": "string",
    "enum": [
     "global",
     "country",
     "market",
     "brand",
     "venue",
     "event",
     "businessUnit"
    ],
    "description": "Scope: where the price list can apply (p.8)"
   },
   "clonedFromPriceListId": {
    "type": "string",
    "nullable": true,
    "description": "The price list this one was duplicated from (Duplicate, p.9: UAE Standard 2026 into UAE Standard 2027); empty when built from scratch"
   },
   "consumingModules": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "ticketing",
      "b2c",
      "pos",
      "kiosk",
      "b2b",
      "groupSales",
      "membership",
      "fnb",
      "retail",
      "rental"
     ]
    },
    "description": "Dependencies: the modules that consume this list (p.9); read-only"
   }
  }
 },
 "PriceListTemplatesCloneReuseView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Price List Templates, Clone & Reuse displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "templateId": {
    "type": "string",
    "description": "Template ID"
   },
   "name": {
    "type": "string",
    "description": "Template name, e.g. Theme Park Pricing"
   },
   "templateType": {
    "type": "string",
    "description": "Template Library type: standardAttraction, themePark, museum, concert, sports, membership, group, corporate, b2b, rental or custom (p.18)"
   },
   "description": {
    "type": "string",
    "description": "Description"
   },
   "components": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "priceCategories",
      "rateTypes",
      "rateMatrixStructure",
      "currencyStructure",
      "hierarchy",
      "productMappingPattern",
      "packagePricingPattern"
     ]
    },
    "description": "Template Components the template carries (p.18)"
   },
   "sourcePriceListId": {
    "type": "string",
    "nullable": true,
    "description": "Price list the template was taken from; empty when built directly"
   },
   "aiDrafted": {
    "type": "boolean",
    "description": "Drafted by AI-assisted template generation and awaiting administrator review"
   },
   "status": {
    "type": "string",
    "description": "Status: draft, active or archived"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   }
  }
 },
 "PricingMarket": {
  "type": "object",
  "x-ticvai-persistence": "catalogue.pricing_market",
  "description": "**A node of the market pricing structure: global, country, region, market or venue** (29 September, data model DM3). ADM-064. Says which price list and rounding a market uses and whether it inherits from its parent. **At venue level the selling currency is the venue's trading currency** and cannot differ from it (ADR-0018, frozen once the venue has traded); above venue level the currencies are reporting and base currencies.",
  "required": [
   "id",
   "scopePath",
   "hierarchyLevel"
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
    "description": "**The partition key** (ADR-0005). Operations write it at `tenant` scope."
   },
   "hierarchyLevel": {
    "type": "string",
    "enum": [
     "global",
     "country",
     "region",
     "market",
     "venue"
    ]
   },
   "parentId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The parent `catalogue.pricing_market`."
   },
   "countryCode": {
    "type": "string",
    "maxLength": 2,
    "nullable": true,
    "pattern": "^[A-Z]{2}$"
   },
   "marketCode": {
    "type": "string",
    "maxLength": 40,
    "nullable": true
   },
   "region": {
    "type": "string",
    "maxLength": 100,
    "nullable": true
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "brand": {
    "type": "string",
    "maxLength": 100,
    "nullable": true
   },
   "legalEntityId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "baseCurrency": {
    "type": "string",
    "maxLength": 3,
    "nullable": true,
    "pattern": "^[A-Z]{3}$"
   },
   "sellingCurrency": {
    "type": "string",
    "maxLength": 3,
    "nullable": true,
    "pattern": "^[A-Z]{3}$"
   },
   "roundingProfileId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "displayFormat": {
    "type": "string",
    "maxLength": 40,
    "nullable": true
   },
   "priceListId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "inheritsFromParent": {
    "type": "boolean",
    "default": true
   },
   "fxReferenceRate": {
    "type": "number",
    "nullable": true,
    "description": "Reference only; FX supplies inputs, it never decides a price."
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
 "ProductServicePriceAssignmentInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Product & Service Price Assignment submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "assignmentId": {
    "type": "string",
    "description": "Assignment ID; empty on create"
   },
   "objectType": {
    "type": "string",
    "enum": [
     "ticketProduct",
     "ticketType",
     "admission",
     "event",
     "performance",
     "membership",
     "annualPass",
     "addOn",
     "fnbItem",
     "retailProduct",
     "rentalItem",
     "resource",
     "reservationService",
     "experience",
     "otherSellableService"
    ],
    "description": "Supported Commercial Objects (p.13): the kind of sellable object being priced"
   },
   "objectIds": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "The objects assigned; more than one is a Bulk Assignment (25 attraction products -> one price list)"
   },
   "assignmentScope": {
    "type": "string",
    "enum": [
     "productLevel",
     "productVariant",
     "ticketType",
     "event",
     "performance",
     "venue"
    ],
    "description": "Assignment Scope (p.14): the level at which the assignment holds"
   },
   "scopeRefId": {
    "type": "string",
    "nullable": true,
    "description": "The variant, ticket type, event, performance or venue the assignment is limited to; empty at product level"
   },
   "priceListId": {
    "type": "string",
    "description": "The price list assigned"
   },
   "categoryRates": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "priceCategory": {
       "type": "string"
      },
      "rateId": {
       "type": "string"
      }
     }
    },
    "description": "Product -> Price List -> Category -> Rate (Assignment Workspace, p.13): which rate of the list serves each category; empty uses every active rate of the list"
   }
  }
 },
 "ProductServicePriceAssignmentView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Product & Service Price Assignment displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "assignmentId": {
    "type": "string",
    "description": "Assignment ID; empty on create"
   },
   "objectType": {
    "type": "string",
    "enum": [
     "ticketProduct",
     "ticketType",
     "admission",
     "event",
     "performance",
     "membership",
     "annualPass",
     "addOn",
     "fnbItem",
     "retailProduct",
     "rentalItem",
     "resource",
     "reservationService",
     "experience",
     "otherSellableService"
    ],
    "description": "Supported Commercial Objects (p.13): the kind of sellable object being priced"
   },
   "objectIds": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "The objects assigned; more than one is a Bulk Assignment (25 attraction products -> one price list)"
   },
   "assignmentScope": {
    "type": "string",
    "enum": [
     "productLevel",
     "productVariant",
     "ticketType",
     "event",
     "performance",
     "venue"
    ],
    "description": "Assignment Scope (p.14): the level at which the assignment holds"
   },
   "scopeRefId": {
    "type": "string",
    "nullable": true,
    "description": "The variant, ticket type, event, performance or venue the assignment is limited to; empty at product level"
   },
   "priceListId": {
    "type": "string",
    "description": "The price list assigned"
   },
   "categoryRates": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "priceCategory": {
       "type": "string"
      },
      "rateId": {
       "type": "string"
      }
     }
    },
    "description": "Product -> Price List -> Category -> Rate (Assignment Workspace, p.13): which rate of the list serves each category; empty uses every active rate of the list"
   },
   "pricingSource": {
    "type": "string",
    "description": "Price Source Visibility (p.14): the name shown on the product, e.g. UAE Standard Admission 2027; read-only"
   }
  }
 },
 "RateStructureBuilderInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table covers these fields** — the closest is catalogue.price at 4%, so this is not an update to anything the package stores today and no new table has been decided",
  "description": "**What Rate Structure Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.\n\n**The pack defines this as a record**, under *Each rate should contain* - one of only 13 drafted writes that does. That is the client writing a row rather than a screen, and it is where the table conversation should start.",
  "properties": {
   "rateId": {
    "type": "string",
    "description": "Rate ID"
   },
   "rateName": {
    "type": "string",
    "description": "Rate Name"
   },
   "rateCode": {
    "type": "string",
    "description": "Rate Code"
   },
   "priceCategory": {
    "type": "string",
    "description": "Price Category: code of a category from the library (ADM-050)"
   },
   "rateType": {
    "type": "string",
    "description": "Rate Type: code of a rate type from the library (ADM-050), e.g. standard, reduced, derived"
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Amount; ignored when derivedFrom is set"
   },
   "currency": {
    "type": "string",
    "description": "Currency: ISO 4217 code",
    "pattern": "^[A-Z]{3}$"
   },
   "unitBasis": {
    "type": "string",
    "enum": [
     "perTicket",
     "perPerson",
     "perUnit",
     "perHour",
     "perDay",
     "perPerformance",
     "perResource",
     "perPackage",
     "perMembershipPeriod"
    ],
    "description": "Unit Basis (p.12); perPerformance is the pack's \"Per Session\" (a session is a Performance)"
   },
   "precision": {
    "type": "integer",
    "description": "Precision: decimal places, 0 to 3 (MoM 1 Sep §4.5 requires up to three)",
    "minimum": 0,
    "maximum": 3
   },
   "roundingProfile": {
    "type": "string",
    "description": "Rounding Profile: code of a currency rounding rule (ADM-075)"
   },
   "status": {
    "type": "string",
    "description": "Status: draft, active or disabled"
   },
   "priceListId": {
    "type": "string",
    "description": "The price list the rate belongs to"
   },
   "derivedFrom": {
    "type": "object",
    "nullable": true,
    "description": "Derived Rates (p.12): this rate is another rate adjusted (Child = Adult - 25%, VIP = Standard + AED 200); a commercial relationship, not dynamic pricing. Empty for an entered amount",
    "properties": {
     "baseRateId": {
      "type": "string"
     },
     "adjustmentType": {
      "type": "string",
      "enum": [
       "percentage",
       "fixedAmount"
      ]
     },
     "adjustmentValue": {
      "type": "number",
      "description": "Percent or amount in the rate currency; negative reduces"
     }
    }
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
   "rateId": {
    "type": "string",
    "description": "Rate ID"
   },
   "rateName": {
    "type": "string",
    "description": "Rate Name"
   },
   "rateCode": {
    "type": "string",
    "description": "Rate Code"
   },
   "priceCategory": {
    "type": "string",
    "description": "Price Category: code of a category from the library (ADM-050)"
   },
   "rateType": {
    "type": "string",
    "description": "Rate Type: code of a rate type from the library (ADM-050), e.g. standard, reduced, derived"
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Amount; for a derived rate this is the computed value, read-only"
   },
   "currency": {
    "type": "string",
    "description": "Currency: ISO 4217 code",
    "pattern": "^[A-Z]{3}$"
   },
   "unitBasis": {
    "type": "string",
    "enum": [
     "perTicket",
     "perPerson",
     "perUnit",
     "perHour",
     "perDay",
     "perPerformance",
     "perResource",
     "perPackage",
     "perMembershipPeriod"
    ],
    "description": "Unit Basis (p.12); perPerformance is the pack's \"Per Session\" (a session is a Performance)"
   },
   "precision": {
    "type": "integer",
    "description": "Precision: decimal places, 0 to 3 (MoM 1 Sep §4.5 requires up to three)",
    "minimum": 0,
    "maximum": 3
   },
   "roundingProfile": {
    "type": "string",
    "description": "Rounding Profile: code of a currency rounding rule (ADM-075)"
   },
   "status": {
    "type": "string",
    "description": "Status: draft, active or disabled"
   },
   "priceListId": {
    "type": "string",
    "description": "The price list the rate belongs to"
   },
   "derivedFrom": {
    "type": "object",
    "nullable": true,
    "description": "Derived Rates (p.12): this rate is another rate adjusted (Child = Adult - 25%, VIP = Standard + AED 200); a commercial relationship, not dynamic pricing. Empty for an entered amount",
    "properties": {
     "baseRateId": {
      "type": "string"
     },
     "adjustmentType": {
      "type": "string",
      "enum": [
       "percentage",
       "fixedAmount"
      ]
     },
     "adjustmentValue": {
      "type": "number",
      "description": "Percent or amount in the rate currency; negative reduces"
     }
    }
   },
   "validationIssues": {
    "type": "array",
    "description": "Validation (pp.12-13): problems found on this rate; read-only",
    "items": {
     "type": "object",
     "properties": {
      "code": {
       "type": "string",
       "enum": [
        "duplicateRate",
        "missingAmount",
        "unsupportedCurrency",
        "invalidDerivedRate",
        "circularRateRelationship"
       ]
      },
      "message": {
       "type": "string"
      }
     }
    }
   }
  }
 }
}
```
