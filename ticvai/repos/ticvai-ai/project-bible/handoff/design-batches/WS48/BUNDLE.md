# WS48 — Promotions   Bundles Management board 4

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
  `PRICE_CONFIGURE, PRICE_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **0 of these operations work offline**
  
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-168` | Advanced Offer Command Center | commandCentre | 1 | 0 | — |
| `ADM-169` | Buy X Get Y / BOGO Rule Builder | configEditor | 1 | 0 | — |
| `ADM-170` | Multi-Buy & Quantity Offer Configurator | configEditor | 1 | 0 | — |
| `ADM-171` | Cheapest / Lowest-Value Item Promotion | configEditor | 1 | 0 | — |
| `ADM-172` | Fixed-Price & “N for X” Offer Builder | configEditor | 1 | 0 | — |
| `ADM-173` | Gift, Free Product & Added-Value Offer Builder | configEditor | 1 | 0 | — |
| `ADM-174` | Cross-Category Promotion Builder | listDetail | 1 | 0 | — |
| `ADM-175` | Reward Selection, Substitution & Customer Choice | listDetail | 1 | 0 | — |
| `ADM-176` | Advanced Offer Guardrails & Conflict Controls | configEditor | 1 | 0 | — |
| `ADM-177` | Offer Simulation, Basket Trace & AI Optimization | listDetail | 1 | 0 | — |

## Thin screens in this batch

**ADM-170, ADM-174, ADM-175, ADM-177 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-168",
  "name": "Advanced Offer Command Center",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "4",
   "number": "1",
   "page": 50
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/advanced-offer-command-center-adm-168",
   "component": "apps/ticvai-web/src/routes/commercial/AdvancedOfferCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-169",
    "ADM-170",
    "ADM-171",
    "ADM-172",
    "ADM-173",
    "ADM-174",
    "ADM-175",
    "ADM-176",
    "ADM-177"
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
     "to": "ADM-169",
     "trigger": "Works in Buy X Get Y / BOGO Rule Builder",
     "provenance": "flow F157 step 1→2",
     "operation": "listAdvancedOffer"
    },
    {
     "to": "ADM-170",
     "trigger": "Works in Multi-Buy & Quantity Offer Configurator",
     "provenance": "flow F157 step 3→4",
     "operation": "listAdvancedOffer"
    },
    {
     "to": "ADM-171",
     "trigger": "Works in Cheapest / Lowest-Value Item Promotion",
     "provenance": "flow F157 step 5→6",
     "operation": "listAdvancedOffer"
    },
    {
     "to": "ADM-172",
     "trigger": "Works in Fixed-Price & “N for X” Offer Builder",
     "provenance": "flow F157 step 7→8",
     "operation": "listAdvancedOffer"
    },
    {
     "to": "ADM-173",
     "trigger": "Works in Gift, Free Product & Added-Value Offer Builder",
     "provenance": "flow F157 step 9→10",
     "operation": "listAdvancedOffer"
    },
    {
     "to": "ADM-174",
     "trigger": "Works in Cross-Category Promotion Builder",
     "provenance": "flow F157 step 11→12",
     "operation": "listAdvancedOffer"
    },
    {
     "to": "ADM-175",
     "trigger": "Works in Reward Selection, Substitution & Customer Choice",
     "provenance": "flow F157 step 13→14",
     "operation": "listAdvancedOffer"
    },
    {
     "to": "ADM-176",
     "trigger": "Works in Advanced Offer Guardrails & Conflict Controls",
     "provenance": "flow F157 step 15→16",
     "operation": "listAdvancedOffer"
    },
    {
     "to": "ADM-177",
     "trigger": "Works in Offer Simulation, Basket Trace & AI Optimization",
     "provenance": "flow F157 step 17→18",
     "operation": "listAdvancedOffer"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide the centralized management workspace for all advanced promotional mechanics.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search advanced offer",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 50 §Filter by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Buy X Get X",
        "Buy X Get Y",
        "Buy N Get X",
        "Buy N Get Multiple",
        "Cheapest Item Free",
        "Percentage Off Another Product",
        "Amount Off Another Product",
        "Fixed Bundle Price",
        "Gift with Purchase",
        "Added Value",
        "Cross-category reward",
        "Upgrade offer"
       ],
       "notes": "The pack filters this screen by buy x get x, buy x get y, buy n get x, buy n get multiple, cheapest item free, percentage off another product and 6 more — which are present is a decision the pack already made.",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 50 §Filter by"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Active Advanced Offers",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 50 §KPI Cards",
       "bindsTo": "AdvancedOfferCommandCenterView.activeAdvancedOffers"
      },
      {
       "kind": "metricTile",
       "label": "Scheduled Offers",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 50 §KPI Cards",
       "bindsTo": "AdvancedOfferCommandCenterView.scheduledOffers"
      },
      {
       "kind": "metricTile",
       "label": "BOGO Campaigns",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 50 §KPI Cards",
       "bindsTo": "AdvancedOfferCommandCenterView.bogoCampaigns"
      },
      {
       "kind": "metricTile",
       "label": "Gift-with-Purchase Offers",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 50 §KPI Cards",
       "bindsTo": "AdvancedOfferCommandCenterView.giftWithPurchaseOffers"
      },
      {
       "kind": "metricTile",
       "label": "Fixed-Price Offers",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 50 §KPI Cards",
       "bindsTo": "AdvancedOfferCommandCenterView.fixedPriceOffers"
      },
      {
       "kind": "metricTile",
       "label": "Cross-Category Offers",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 50 §KPI Cards",
       "bindsTo": "AdvancedOfferCommandCenterView.crossCategoryOffers"
      },
      {
       "kind": "metricTile",
       "label": "Total Redemptions",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 50 §KPI Cards",
       "bindsTo": "AdvancedOfferCommandCenterView.totalRedemptions"
      },
      {
       "kind": "metricTile",
       "label": "Free Items Issued",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 50 §KPI Cards",
       "bindsTo": "AdvancedOfferCommandCenterView.freeItemsIssued"
      },
      {
       "kind": "metricTile",
       "label": "Discount Granted",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 50 §KPI Cards",
       "bindsTo": "AdvancedOfferCommandCenterView.discountGranted"
      },
      {
       "kind": "metricTile",
       "label": "Revenue Generated",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 50 §KPI Cards",
       "bindsTo": "AdvancedOfferCommandCenterView.revenueGenerated"
      },
      {
       "kind": "metricTile",
       "label": "AOV Uplift",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 50 §KPI Cards",
       "bindsTo": "AdvancedOfferCommandCenterView.aovUplift"
      },
      {
       "kind": "metricTile",
       "label": "Margin Impact",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 50 §KPI Cards",
       "bindsTo": "AdvancedOfferCommandCenterView.marginImpact"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The advanced offer list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the advanced offer untouched.",
   "emptyFirstRun": "No advanced offer yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the advanced offer are still there. The pack's own statuses are Draft — the state names which is selected.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAdvancedOffer",
    "contract": "promotions",
    "purpose": "Advanced Offer Command Center",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "AdvancedOfferCommandCenterView.activeAdvancedOffers",
    "AdvancedOfferCommandCenterView.scheduledOffers",
    "AdvancedOfferCommandCenterView.bogoCampaigns",
    "AdvancedOfferCommandCenterView.giftWithPurchaseOffers",
    "AdvancedOfferCommandCenterView.fixedPriceOffers",
    "AdvancedOfferCommandCenterView.crossCategoryOffers"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-168"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 50. 12 of 24 labels bound to a contract property; 33 of 36 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-169",
  "name": "Buy X Get Y / BOGO Rule Builder",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "4",
   "number": "2",
   "page": 52
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/buy-x-get-y-bogo-rule-builder-adm-169",
   "component": "apps/ticvai-web/src/routes/commercial/BuyXGetYBogoRuleBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-168"
   ],
   "exitTo": [
    "ADM-168"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-168, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-168",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F157 step 2→3",
     "operation": "setBuyGetBogo"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure the fundamental qualifier → reward relationship.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Product",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 52 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Product category",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 52 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Ticket type",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 52 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Quantity",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 52 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Minimum spend",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 52 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Customer segment",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 52 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Channel",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 52 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 52 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Date/time",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 52 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Same product",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 52 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Different product",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 52 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Free",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 52 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Percentage discount",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 52 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Fixed discount",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 52 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Fixed reward price",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 52 §Configure"
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
       "provenance": "contract operation setBuyGetBogo"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The buy get bogo configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the buy get bogo untouched.",
   "emptyFirstRun": "No buy get bogo configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setBuyGetBogo",
    "contract": "promotions",
    "purpose": "Buy X Get Y / BOGO Rule Builder",
    "trigger": "onAction",
    "invalidates": [
     "setBuyGetBogo"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-169"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 52. 0 of 0 labels bound to a contract property; 15 of 27 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-170",
  "name": "Multi-Buy & Quantity Offer Configurator",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "4",
   "number": "3",
   "page": 53
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/multi-buy-quantity-offer-configurator-adm-170",
   "component": "apps/ticvai-web/src/routes/commercial/MultiBuyQuantityOfferConfigurator.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-168"
   ],
   "exitTo": [
    "ADM-168"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-168, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-168",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F157 step 4→5",
     "operation": "listMultiBuyQuantity"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Administrator shall configure) and no display directory — it is settings, not a population",
  "purpose": "Configure advanced quantity relationships that go beyond simple BOGO.",
  "gaps": [
   {
    "operation": null,
    "why": "**Multi-Buy & Quantity Offer Configurator declares no operation that writes anything** — its only declared call is `listMultiBuyQuantity`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
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
       "label": "Apply once",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 53 §Administrator shall configure"
      },
      {
       "kind": "selectField",
       "label": "Repeat automatically",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 53 §Administrator shall configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum repetitions",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 53 §Administrator shall configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The multi-buy quantity offer configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the multi-buy quantity offer untouched.",
   "emptyFirstRun": "No multi-buy quantity offer configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listMultiBuyQuantity",
    "contract": "promotions",
    "purpose": "Multi-Buy & Quantity Offer Configurator",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-170"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 53. 0 of 0 labels bound to a contract property; 3 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-171",
  "name": "Cheapest / Lowest-Value Item Promotion",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "4",
   "number": "4",
   "page": 53
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/cheapest-lowest-value-item-promotion-adm-171",
   "component": "apps/ticvai-web/src/routes/commercial/CheapestLowestValueItemPromotion.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-168"
   ],
   "exitTo": [
    "ADM-168"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-168, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-168",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F157 step 6→7",
     "operation": "listCheapestLowestValue"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configuration) and no display directory — it is settings, not a population",
  "purpose": "Configure offers where TICVAI dynamically identifies the lowest-priced qualifying item. The matrix explicitly requires “buy multiple products and get cheapest item free” and adding cheaper qualifying items within the same transaction.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Eligible products",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 53 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Eligible categories",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 53 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Minimum quantity",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 53 §Configuration"
      },
      {
       "kind": "textField",
       "label": "Number of free items",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 53 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Cheapest/lowest-priced selection",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 53 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Maximum free-item value",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 53 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Maximum repetitions",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 53 §Configuration"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The cheapest lowest-value item configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the cheapest lowest-value item untouched.",
   "emptyFirstRun": "No cheapest lowest-value item configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCheapestLowestValue",
    "contract": "promotions",
    "purpose": "Cheapest / Lowest-Value Item Promotion",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-171"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 53. 0 of 0 labels bound to a contract property; 7 of 17 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-172",
  "name": "Fixed-Price & “N for X” Offer Builder",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "4",
   "number": "5",
   "page": 54
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/fixed-price-n-for-x-offer-builder-adm-172",
   "component": "apps/ticvai-web/src/routes/commercial/FixedPriceNForXOfferBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-168"
   ],
   "exitTo": [
    "ADM-168"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-168, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-168",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F157 step 8→9",
     "operation": "setFixedPriceOffer"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configuration) and no display directory — it is settings, not a population",
  "purpose": "Configure promotions where a qualifying collection of products is sold for a fixed promotional total.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Required quantity",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 54 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Required products",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 54 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Product category",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 54 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Mix-and-match allowed",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 54 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Fixed promotional price",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 54 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Currency",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 54 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Maximum repetitions",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 54 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Minimum/maximum product values",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 54 §Configuration"
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
       "provenance": "contract operation setFixedPriceOffer"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The fixed-price for offer configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the fixed-price for offer untouched.",
   "emptyFirstRun": "No fixed-price for offer configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setFixedPriceOffer",
    "contract": "promotions",
    "purpose": "Fixed-Price & “N for X” Offer Builder",
    "trigger": "onAction",
    "invalidates": [
     "setFixedPriceOffer"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-172"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 54. 0 of 0 labels bound to a contract property; 8 of 21 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-173",
  "name": "Gift, Free Product & Added-Value Offer Builder",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "4",
   "number": "6",
   "page": 55
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/gift-free-product-added-value-offer-builder-adm-173",
   "component": "apps/ticvai-web/src/routes/commercial/GiftFreeProductAddedValueOfferBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-168"
   ],
   "exitTo": [
    "ADM-168"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-168, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-168",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F157 step 10→11",
     "operation": "setGiftFreeProduct"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure promotions where a purchase generates an additional entitlement rather than simply reducing price. The matrix explicitly provides the example: “Buy for more than 200 AED and get a free pencil.”",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "textField",
       "label": "Do not offer promotion",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 55 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Provide alternative reward",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 55 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Issue voucher",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 55 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Allow later fulfillment",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 55 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Escalate to operator",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 55 §Configure"
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
       "provenance": "contract operation setGiftFreeProduct"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The gift free product configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the gift free product untouched.",
   "emptyFirstRun": "No gift free product configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setGiftFreeProduct",
    "contract": "promotions",
    "purpose": "Gift, Free Product & Added-Value Offer Builder",
    "trigger": "onAction",
    "invalidates": [
     "setGiftFreeProduct"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-173"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 55. 0 of 0 labels bound to a contract property; 5 of 32 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-174",
  "name": "Cross-Category Promotion Builder",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "4",
   "number": "7",
   "page": 56
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/cross-category-promotion-builder-adm-174",
   "component": "apps/ticvai-web/src/routes/commercial/CrossCategoryPromotionBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-168"
   ],
   "exitTo": [
    "ADM-168"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-168, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-168",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F157 step 12→13",
     "operation": "setCrossCategoryPromotion"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Create promotions spanning different TICVAI commercial domains.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 56"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 56"
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
       "provenance": "contract operation setCrossCategoryPromotion"
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
       "impliedBy": "setCrossCategoryPromotion"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The cross-category promotion list.",
   "error": "Could not load. Names which read failed and leaves the cross-category promotion untouched.",
   "emptyFirstRun": "No cross-category promotion yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the cross-category promotion are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setCrossCategoryPromotion",
    "contract": "promotions",
    "purpose": "Cross-Category Promotion Builder",
    "trigger": "onAction",
    "invalidates": [
     "setCrossCategoryPromotion"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-174"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 56. 0 of 0 labels bound to a contract property; 0 of 23 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-175",
  "name": "Reward Selection, Substitution & Customer Choice",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "4",
   "number": "8",
   "page": 57
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/reward-selection-substitution-customer-choice-adm-175",
   "component": "apps/ticvai-web/src/routes/commercial/RewardSelectionSubstitutionCustomerChoice.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-168"
   ],
   "exitTo": [
    "ADM-168"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-168, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-168",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F157 step 14→15",
     "operation": "listRewardSelectionSubstitution"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Control situations where the customer can choose between multiple promotional rewards.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 57"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 57"
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
       "impliedBy": "listRewardSelectionSubstitution",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The reward selection substitution list.",
   "error": "Could not load. Names which read failed and leaves the reward selection substitution untouched.",
   "emptyFirstRun": "No reward selection substitution yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the reward selection substitution are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listRewardSelectionSubstitution",
    "contract": "promotions",
    "purpose": "Reward Selection, Substitution & Customer Choice",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "RewardSelectionSubstitutionCustomerChoiceView.guestSelectsFromConfiguredOptions",
    "RewardSelectionSubstitutionCustomerChoiceView.posCallCenterOperatorSelects"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-175"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 57. 0 of 0 labels bound to a contract property; 0 of 12 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-176",
  "name": "Advanced Offer Guardrails & Conflict Controls",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "4",
   "number": "9",
   "page": 58
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/advanced-offer-guardrails-conflict-controls-adm-176",
   "component": "apps/ticvai-web/src/routes/commercial/AdvancedOfferGuardrailsConflictControls.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-168"
   ],
   "exitTo": [
    "ADM-168"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-168, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-168",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F157 step 16→17",
     "operation": "listAdvancedOfferGuardrail"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Define preliminary behavior; Prevent configurations such as) and no display directory — it is settings, not a population",
  "purpose": "Prevent advanced offers from generating unintended financial or operational outcomes. This screen handles offer-specific safeguards; the complete cross-promotion stacking hierarchy remains in Board 8.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Can combine",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 58 §Define preliminary behavior"
      },
      {
       "kind": "selectField",
       "label": "Cannot combine",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 58 §Define preliminary behavior"
      },
      {
       "kind": "selectField",
       "label": "Exclusive",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 58 §Define preliminary behavior"
      },
      {
       "kind": "textField",
       "label": "Defer to central stacking engine",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 58 §Define preliminary behavior"
      },
      {
       "kind": "textField",
       "label": "Product A gives Product B free",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 58 §Prevent configurations such as"
      },
      {
       "kind": "textField",
       "label": "Product B gives Product A free",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 58 §Prevent configurations such as"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The advanced offer guardrails configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the advanced offer guardrails untouched.",
   "emptyFirstRun": "No advanced offer guardrails configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAdvancedOfferGuardrail",
    "contract": "promotions",
    "purpose": "Advanced Offer Guardrails & Conflict Controls",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-176"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 58. 0 of 0 labels bound to a contract property; 6 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-177",
  "name": "Offer Simulation, Basket Trace & AI Optimization",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "4",
   "number": "10",
   "page": 59
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/offer-simulation-basket-trace-ai-optimization-adm-177",
   "component": "apps/ticvai-web/src/routes/commercial/OfferSimulationBasketTraceAiOptimization.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-168"
   ],
   "exitTo": [
    "ADM-168"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-168, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation."
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Test complex promotion mechanics before publication.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 3 actions on this screen and the screen declares 1 operation.** Unserved: Sample customer segment, Forecast simulation, Bulk scenario testing. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 59 §Allow"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 59"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 59"
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
       "label": "Sample customer segment",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 59 §Allow"
      },
      {
       "kind": "secondaryButton",
       "label": "Forecast simulation",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 59 §Allow"
      },
      {
       "kind": "secondaryButton",
       "label": "Bulk scenario testing",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 59 §Allow"
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
   "loading": "The offer simulation basket list.",
   "error": "Could not load. Names which read failed and leaves the offer simulation basket untouched.",
   "emptyFirstRun": "No offer simulation basket yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the offer simulation basket are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listOfferBasketTrace",
    "contract": "promotions",
    "purpose": "Offer Simulation, Basket Trace & AI Optimization",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "OfferSimulationBasketTraceAiOptimizationView.yPrice",
    "OfferSimulationBasketTraceAiOptimizationView.adult",
    "OfferSimulationBasketTraceAiOptimizationView.child",
    "OfferSimulationBasketTraceAiOptimizationView.subtotalAed750",
    "OfferSimulationBasketTraceAiOptimizationView.originalTotalAed750"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-177"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 59. 0 of 0 labels bound to a contract property; 3 of 71 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "listAdvancedOffer": {
  "method": "GET",
  "path": "/advanced-offer",
  "contract": "promotions",
  "summary": "Advanced Offer Command Center",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "buyXGetX",
    "in": "query",
    "required": false
   },
   {
    "name": "buyXGetY",
    "in": "query",
    "required": false
   },
   {
    "name": "buyNGetX",
    "in": "query",
    "required": false
   },
   {
    "name": "buyNGetMultiple",
    "in": "query",
    "required": false
   },
   {
    "name": "cheapestItemFree",
    "in": "query",
    "required": false
   },
   {
    "name": "percentageOffAnotherProduct",
    "in": "query",
    "required": false
   },
   {
    "name": "amountOffAnotherProduct",
    "in": "query",
    "required": false
   },
   {
    "name": "fixedBundlePrice",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "AdvancedOfferCommandCenterView"
 },
 "listAdvancedOfferGuardrail": {
  "method": "GET",
  "path": "/advanced-offer-guardrail",
  "contract": "promotions",
  "summary": "Advanced Offer Guardrails & Conflict Controls",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AdvancedOfferGuardrailsConflictControlsView"
 },
 "listCheapestLowestValue": {
  "method": "GET",
  "path": "/cheapest-lowest-value",
  "contract": "promotions",
  "summary": "Cheapest / Lowest-Value Item Promotion",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "CheapestLowestValueItemPromotionView"
 },
 "listMultiBuyQuantity": {
  "method": "GET",
  "path": "/multi-buy-quantity",
  "contract": "promotions",
  "summary": "Multi-Buy & Quantity Offer Configurator",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "MultiBuyQuantityOfferConfiguratorView"
 },
 "listOfferBasketTrace": {
  "method": "GET",
  "path": "/offer-basket-trace",
  "contract": "promotions",
  "summary": "Offer Simulation, Basket Trace & AI Optimization",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "OfferSimulationBasketTraceAiOptimizationView"
 },
 "listRewardSelectionSubstitution": {
  "method": "GET",
  "path": "/reward-selection-substitution",
  "contract": "promotions",
  "summary": "Reward Selection, Substitution & Customer Choice",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "RewardSelectionSubstitutionCustomerChoiceView"
 },
 "setBuyGetBogo": {
  "method": "PUT",
  "path": "/buy-get-bogo",
  "contract": "promotions",
  "summary": "Buy X Get Y / BOGO Rule Builder",
  "permission": "PRICE_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "BuyXGetYBogoRuleBuilderInput",
  "responds": "BuyXGetYBogoRuleBuilderView"
 },
 "setCrossCategoryPromotion": {
  "method": "PUT",
  "path": "/cross-category-promotion",
  "contract": "promotions",
  "summary": "Cross-Category Promotion Builder",
  "permission": "PRICE_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "CrossCategoryPromotionBuilderInput",
  "responds": "CrossCategoryPromotionBuilderView"
 },
 "setFixedPriceOffer": {
  "method": "PUT",
  "path": "/fixed-price-offer",
  "contract": "promotions",
  "summary": "Fixed-Price & “N for X” Offer Builder",
  "permission": "PRICE_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "FixedPriceNForXOfferBuilderInput",
  "responds": "FixedPriceNForXOfferBuilderView"
 },
 "setGiftFreeProduct": {
  "method": "PUT",
  "path": "/gift-free-product",
  "contract": "promotions",
  "summary": "Gift, Free Product & Added-Value Offer Builder",
  "permission": "PRICE_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "GiftFreeProductAddedValueOfferBuilderInput",
  "responds": "GiftFreeProductAddedValueOfferBuilderView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AdvancedOfferCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Advanced Offer Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "activeAdvancedOffers": {
    "type": "integer",
    "description": "Active Advanced Offers"
   },
   "scheduledOffers": {
    "type": "integer",
    "description": "Scheduled Offers"
   },
   "bogoCampaigns": {
    "type": "integer",
    "description": "BOGO Campaigns"
   },
   "giftWithPurchaseOffers": {
    "type": "integer",
    "description": "Gift-with-Purchase Offers"
   },
   "fixedPriceOffers": {
    "type": "integer",
    "description": "Fixed-Price Offers"
   },
   "crossCategoryOffers": {
    "type": "integer",
    "description": "Cross-Category Offers"
   },
   "totalRedemptions": {
    "type": "integer",
    "description": "Total Redemptions"
   },
   "freeItemsIssued": {
    "type": "string",
    "description": "Free Items Issued"
   },
   "discountGranted": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Discount Granted"
   },
   "revenueGenerated": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue Generated"
   },
   "aovUplift": {
    "type": "number",
    "description": "AOV Uplift"
   },
   "marginImpact": {
    "type": "number",
    "description": "Margin Impact"
   },
   "draft": {
    "type": "string",
    "description": "Draft"
   },
   "pendingValidation": {
    "type": "integer",
    "description": "Pending Validation"
   },
   "pendingApproval": {
    "type": "integer",
    "description": "Pending Approval"
   },
   "scheduled": {
    "type": "string",
    "format": "date-time",
    "description": "Scheduled"
   },
   "active": {
    "type": "integer",
    "description": "Active"
   },
   "paused": {
    "type": "string",
    "description": "Paused"
   },
   "suspended": {
    "type": "string",
    "description": "Suspended"
   },
   "expired": {
    "type": "integer",
    "description": "Expired"
   },
   "archived": {
    "type": "string",
    "description": "Archived"
   }
  }
 },
 "AdvancedOfferGuardrailsConflictControlsView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Advanced Offer Guardrails & Conflict Controls displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "maximumFreeItems": {
    "type": "string",
    "description": "Maximum free items"
   },
   "maximumRewardValue": {
    "type": "string",
    "description": "Maximum reward value"
   },
   "maximumDiscount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Maximum discount"
   },
   "maximumApplicationsPerBasket": {
    "type": "string",
    "description": "Maximum applications per basket"
   },
   "maximumApplicationsPerCustomer": {
    "type": "string",
    "description": "Maximum applications per customer"
   },
   "maximumDailyRedemptions": {
    "type": "string",
    "description": "Maximum daily redemptions"
   },
   "maximumCampaignRedemptions": {
    "type": "string",
    "description": "Maximum campaign redemptions"
   },
   "minimumTransactionValue": {
    "type": "string",
    "description": "Minimum transaction value"
   },
   "minimumMargin": {
    "type": "number",
    "description": "Minimum margin"
   },
   "inventoryRequirement": {
    "type": "string",
    "description": "Inventory requirement"
   },
   "canCombine": {
    "type": "boolean",
    "description": "Can combine"
   },
   "cannotCombine": {
    "type": "string",
    "description": "Cannot combine"
   },
   "exclusive": {
    "type": "string",
    "description": "Exclusive"
   },
   "deferToCentralStackingEngine": {
    "type": "string",
    "description": "Defer to central stacking engine"
   }
  }
 },
 "BuyXGetYBogoRuleBuilderInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table covers these fields** — the closest is promotions.bundle_component at 7%, so this is not an update to anything the package stores today and no new table has been decided",
  "description": "**What Buy X Get Y / BOGO Rule Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "product": {
    "type": "string",
    "description": "Product"
   },
   "productCategory": {
    "type": "string",
    "description": "Product category"
   },
   "ticketType": {
    "type": "string",
    "description": "Ticket type"
   },
   "quantity": {
    "type": "integer",
    "description": "Quantity"
   },
   "minimumSpend": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Minimum spend"
   },
   "customerSegment": {
    "type": "string",
    "description": "Customer segment"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "dateTime": {
    "type": "string",
    "format": "date-time",
    "description": "Date/time"
   },
   "sameProduct": {
    "type": "string",
    "description": "Same product"
   },
   "differentProduct": {
    "type": "string",
    "description": "Different product"
   },
   "free": {
    "type": "string",
    "description": "Free"
   },
   "percentageDiscount": {
    "type": "number",
    "description": "Percentage discount"
   },
   "fixedDiscount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Fixed discount"
   },
   "fixedRewardPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Fixed reward price"
   }
  }
 },
 "BuyXGetYBogoRuleBuilderView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Buy X Get Y / BOGO Rule Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "product": {
    "type": "string",
    "description": "Product"
   },
   "productCategory": {
    "type": "string",
    "description": "Product category"
   },
   "ticketType": {
    "type": "string",
    "description": "Ticket type"
   },
   "quantity": {
    "type": "integer",
    "description": "Quantity"
   },
   "minimumSpend": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Minimum spend"
   },
   "customerSegment": {
    "type": "string",
    "description": "Customer segment"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "dateTime": {
    "type": "string",
    "format": "date-time",
    "description": "Date/time"
   },
   "sameProduct": {
    "type": "string",
    "description": "Same product"
   },
   "differentProduct": {
    "type": "string",
    "description": "Different product"
   },
   "free": {
    "type": "string",
    "description": "Free"
   },
   "percentageDiscount": {
    "type": "number",
    "description": "Percentage discount"
   },
   "fixedDiscount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Fixed discount"
   },
   "fixedRewardPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Fixed reward price"
   }
  }
 },
 "CheapestLowestValueItemPromotionView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Cheapest / Lowest-Value Item Promotion displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "e100": {
    "type": "string",
    "description": "e 100"
   },
   "buy4CheapestFree": {
    "type": "string",
    "description": "Buy 4 → Cheapest Free"
   },
   "eligibleProducts": {
    "type": "string",
    "description": "Eligible products"
   },
   "eligibleCategories": {
    "type": "string",
    "description": "Eligible categories"
   },
   "minimumQuantity": {
    "type": "integer",
    "description": "Minimum quantity"
   },
   "numberOfFreeItems": {
    "type": "integer",
    "description": "Number of free items"
   },
   "cheapestLowestPricedSelection": {
    "type": "string",
    "description": "Cheapest/lowest-priced selection"
   },
   "maximumFreeItemValue": {
    "type": "string",
    "description": "Maximum free-item value"
   },
   "maximumRepetitions": {
    "type": "string",
    "description": "Maximum repetitions"
   },
   "cheapestItemFree": {
    "type": "string",
    "description": "Cheapest item free"
   },
   "cheapestItem50Off": {
    "type": "number",
    "description": "Cheapest item 50% off"
   },
   "nCheapestItemsFree": {
    "type": "string",
    "description": "N cheapest items free"
   }
  }
 },
 "CrossCategoryPromotionBuilderInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Cross-Category Promotion Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "ticketing": {
    "type": "string",
    "description": "Ticketing"
   },
   "attractions": {
    "type": "string",
    "description": "Attractions"
   },
   "events": {
    "type": "string",
    "description": "Events"
   },
   "fB": {
    "type": "string",
    "description": "F&B"
   },
   "retail": {
    "type": "string",
    "description": "Retail"
   },
   "membership": {
    "type": "string",
    "description": "Membership"
   },
   "experiences": {
    "type": "string",
    "description": "Experiences"
   },
   "addOns": {
    "type": "string",
    "description": "Add-ons"
   },
   "parking": {
    "type": "string",
    "description": "Parking"
   },
   "services": {
    "type": "string",
    "description": "Services"
   }
  }
 },
 "CrossCategoryPromotionBuilderView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Cross-Category Promotion Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "ticketing": {
    "type": "string",
    "description": "Ticketing"
   },
   "attractions": {
    "type": "string",
    "description": "Attractions"
   },
   "events": {
    "type": "string",
    "description": "Events"
   },
   "fB": {
    "type": "string",
    "description": "F&B"
   },
   "retail": {
    "type": "string",
    "description": "Retail"
   },
   "membership": {
    "type": "string",
    "description": "Membership"
   },
   "experiences": {
    "type": "string",
    "description": "Experiences"
   },
   "addOns": {
    "type": "string",
    "description": "Add-ons"
   },
   "parking": {
    "type": "string",
    "description": "Parking"
   },
   "services": {
    "type": "string",
    "description": "Services"
   }
  }
 },
 "FixedPriceNForXOfferBuilderInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Fixed-Price & “N for X” Offer Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "requiredQuantity": {
    "type": "integer",
    "description": "Required quantity"
   },
   "requiredProducts": {
    "type": "string",
    "description": "Required products"
   },
   "productCategory": {
    "type": "string",
    "description": "Product category"
   },
   "mixAndMatchAllowed": {
    "type": "boolean",
    "description": "Mix-and-match allowed"
   },
   "fixedPromotionalPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Fixed promotional price"
   },
   "currency": {
    "type": "string",
    "description": "Currency"
   },
   "maximumRepetitions": {
    "type": "string",
    "description": "Maximum repetitions"
   },
   "minimumMaximumProductValues": {
    "type": "string",
    "description": "Minimum/maximum product values"
   },
   "for": {
    "type": "string",
    "description": "for"
   },
   "refunds": {
    "type": "string",
    "description": "Refunds"
   },
   "tax": {
    "type": "string",
    "description": "Tax"
   },
   "revenueRecognition": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue recognition"
   },
   "partnerSettlement": {
    "type": "string",
    "description": "Partner settlement"
   },
   "reporting": {
    "type": "string",
    "description": "Reporting"
   }
  }
 },
 "FixedPriceNForXOfferBuilderView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Fixed-Price & “N for X” Offer Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "requiredQuantity": {
    "type": "integer",
    "description": "Required quantity"
   },
   "requiredProducts": {
    "type": "string",
    "description": "Required products"
   },
   "productCategory": {
    "type": "string",
    "description": "Product category"
   },
   "mixAndMatchAllowed": {
    "type": "boolean",
    "description": "Mix-and-match allowed"
   },
   "fixedPromotionalPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Fixed promotional price"
   },
   "currency": {
    "type": "string",
    "description": "Currency"
   },
   "maximumRepetitions": {
    "type": "string",
    "description": "Maximum repetitions"
   },
   "minimumMaximumProductValues": {
    "type": "string",
    "description": "Minimum/maximum product values"
   },
   "for": {
    "type": "string",
    "description": "for"
   },
   "refunds": {
    "type": "string",
    "description": "Refunds"
   },
   "tax": {
    "type": "string",
    "description": "Tax"
   },
   "revenueRecognition": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue recognition"
   },
   "partnerSettlement": {
    "type": "string",
    "description": "Partner settlement"
   },
   "reporting": {
    "type": "string",
    "description": "Reporting"
   }
  }
 },
 "GiftFreeProductAddedValueOfferBuilderInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table covers these fields** — the closest is promotions.bundle_component at 7%, so this is not an update to anything the package stores today and no new table has been decided",
  "description": "**What Gift, Free Product & Added-Value Offer Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "basketValue": {
    "type": "string",
    "description": "Basket value"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "quantity": {
    "type": "integer",
    "description": "Quantity"
   },
   "productCategory": {
    "type": "string",
    "description": "Product category"
   },
   "ticket": {
    "type": "string",
    "description": "Ticket"
   },
   "membership": {
    "type": "string",
    "description": "Membership"
   },
   "customerSegment": {
    "type": "string",
    "description": "Customer segment"
   },
   "typesType": {
    "type": "string",
    "enum": [
     "freeRetailProduct",
     "freeFBProduct",
     "freeTicket",
     "freeAddOn",
     "freeExperience",
     "voucher",
     "upgrade",
     "service",
     "additionalEntitlement"
    ],
    "description": "Vocabulary listed under Reward Types."
   },
   "inventoryAvailability": {
    "type": "string",
    "description": "Inventory availability"
   },
   "locationInventory": {
    "type": "string",
    "description": "Location inventory"
   },
   "eligibleFulfillmentPoint": {
    "type": "string",
    "description": "Eligible fulfillment point"
   },
   "substitutionRules": {
    "type": "string",
    "description": "Substitution rules"
   },
   "doNotOfferPromotion": {
    "type": "string",
    "description": "Do not offer promotion"
   },
   "provideAlternativeReward": {
    "type": "string",
    "description": "Provide alternative reward"
   },
   "allowLaterFulfillment": {
    "type": "boolean",
    "description": "Allow later fulfillment"
   }
  }
 },
 "GiftFreeProductAddedValueOfferBuilderView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Gift, Free Product & Added-Value Offer Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "basketValue": {
    "type": "string",
    "description": "Basket value"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "quantity": {
    "type": "integer",
    "description": "Quantity"
   },
   "productCategory": {
    "type": "string",
    "description": "Product category"
   },
   "ticket": {
    "type": "string",
    "description": "Ticket"
   },
   "membership": {
    "type": "string",
    "description": "Membership"
   },
   "customerSegment": {
    "type": "string",
    "description": "Customer segment"
   },
   "typesType": {
    "type": "string",
    "enum": [
     "freeRetailProduct",
     "freeFBProduct",
     "freeTicket",
     "freeAddOn",
     "freeExperience",
     "voucher",
     "upgrade",
     "service",
     "additionalEntitlement"
    ],
    "description": "Vocabulary listed under Reward Types."
   },
   "inventoryAvailability": {
    "type": "string",
    "description": "Inventory availability"
   },
   "locationInventory": {
    "type": "string",
    "description": "Location inventory"
   },
   "eligibleFulfillmentPoint": {
    "type": "string",
    "description": "Eligible fulfillment point"
   },
   "substitutionRules": {
    "type": "string",
    "description": "Substitution rules"
   },
   "doNotOfferPromotion": {
    "type": "string",
    "description": "Do not offer promotion"
   },
   "provideAlternativeReward": {
    "type": "string",
    "description": "Provide alternative reward"
   },
   "allowLaterFulfillment": {
    "type": "boolean",
    "description": "Allow later fulfillment"
   }
  }
 },
 "MultiBuyQuantityOfferConfiguratorView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Multi-Buy & Quantity Offer Configurator displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "minimumQuantity": {
    "type": "integer",
    "description": "Minimum quantity"
   },
   "exactQuantity": {
    "type": "integer",
    "description": "Exact quantity"
   },
   "quantityRange": {
    "type": "integer",
    "description": "Quantity range"
   },
   "multiplesOfX": {
    "type": "string",
    "description": "Multiples of X"
   },
   "oneFree": {
    "type": "string",
    "description": "One free"
   },
   "multipleFree": {
    "type": "string",
    "description": "Multiple free"
   },
   "percentageOff": {
    "type": "number",
    "description": "Percentage off"
   },
   "amountOff": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Amount off"
   },
   "fixedTotalPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Fixed total price"
   },
   "repeatAutomatically": {
    "type": "string",
    "description": "Repeat automatically"
   },
   "maximumRepetitions": {
    "type": "string",
    "description": "Maximum repetitions"
   }
  }
 },
 "OfferSimulationBasketTraceAiOptimizationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Offer Simulation, Basket Trace & AI Optimization displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "yPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "y Price"
   },
   "adult": {
    "type": "string",
    "description": "Adult (the pack shows 2 AED 200)"
   },
   "child": {
    "type": "string",
    "description": "Child (the pack shows 2 AED 150)"
   },
   "subtotalAed750": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Subtotal: AED 750"
   },
   "originalTotalAed750": {
    "type": "string",
    "description": "Original Total: AED 750"
   },
   "promotionAed150": {
    "type": "string",
    "description": "Promotion: −AED 150"
   },
   "finalTotalAed600": {
    "type": "string",
    "description": "Final Total: AED 600"
   },
   "eligibleVenue": {
    "type": "string",
    "description": "Eligible venue ✓"
   },
   "eligibleChannel": {
    "type": "string",
    "description": "Eligible channel ✓"
   },
   "cheapestAdmissionSelected": {
    "type": "string",
    "description": "Cheapest admission selected ✓"
   },
   "childTicketAed150": {
    "type": "string",
    "description": "Child Ticket AED 150 ✓"
   },
   "maximumRewardAed200": {
    "type": "string",
    "description": "Maximum reward AED 200 ✓"
   },
   "marginFloorMaintained": {
    "type": "number",
    "description": "Margin floor maintained ✓"
   },
   "singleTransaction": {
    "type": "string",
    "description": "Single transaction"
   },
   "historicalTransactionReplay": {
    "type": "string",
    "description": "Historical transaction replay"
   },
   "sampleCustomerSegment": {
    "type": "string",
    "description": "Sample customer segment"
   },
   "forecastSimulation": {
    "type": "string",
    "description": "Forecast simulation"
   },
   "bulkScenarioTesting": {
    "type": "string",
    "description": "Bulk scenario testing"
   },
   "qualifierAndRewardTicketProducts": {
    "type": "string",
    "description": "Qualifier and reward ticket products"
   },
   "couponEngineBoard3": {
    "type": "string",
    "description": "Coupon Engine — Board 3"
   },
   "codeTriggeredAdvancedOffers": {
    "type": "string",
    "description": "Code-triggered advanced offers"
   },
   "menuProductsPricesAndInventory": {
    "type": "string",
    "description": "Menu products, prices and inventory"
   },
   "retailProductsAndStockAvailability": {
    "type": "string",
    "description": "Retail products and stock availability"
   },
   "freeProductAvailabilityAndSubstitution": {
    "type": "string",
    "description": "Free-product availability and substitution"
   },
   "memberEligibilityAndBenefits": {
    "type": "string",
    "description": "Member eligibility and benefits"
   },
   "customerSegmentationAndPersonalization": {
    "type": "string",
    "description": "Customer segmentation and personalization"
   },
   "priceBasisAndMarginProtection": {
    "type": "number",
    "description": "Price basis and margin protection"
   },
   "revenueAllocationAndPromotionalCost": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue allocation and promotional cost"
   },
   "finalTransactionAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Final transaction amount"
   },
   "board4AdvancedMechanics": {
    "type": "string",
    "description": "Board 4 — Advanced Mechanics"
   },
   "whatProductToProductRewardRelationshipOccurs": {
    "type": "string",
    "description": "What product-to-product reward relationship occurs?"
   },
   "matrixCoverageBoard4": {
    "type": "string",
    "description": "Matrix Coverage — Board 4"
   }
  }
 },
 "RewardSelectionSubstitutionCustomerChoiceView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Reward Selection, Substitution & Customer Choice displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "guestSelectsFromConfiguredOptions": {
    "type": "string",
    "description": "Guest selects from configured options"
   },
   "posCallCenterOperatorSelects": {
    "type": "string",
    "description": "POS/call-center operator selects"
   }
  }
 }
}
```
