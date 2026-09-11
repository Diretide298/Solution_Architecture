# WS46 — Promotions   Bundles Management board 2

**10 screens · 10 operations · 12 schemas · 2 permissions**

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
| `ADM-148` | Promotion Rule Builder | listDetail | 1 | 0 | — |
| `ADM-149` | Percentage & Fixed Discount Configurator | configEditor | 1 | 0 | — |
| `ADM-150` | Cart & Transaction Threshold Rules | listDetail | 1 | 0 | — |
| `ADM-151` | Volume, Bulk & Tier Discount Configurator | listDetail | 1 | 0 | — |
| `ADM-152` | Time-Based & Seasonal Discount Rules | listDetail | 1 | 0 | — |
| `ADM-153` | Customer, Membership & Segment Discount Rules | listDetail | 1 | 0 | — |
| `ADM-154` | Payment Method, Bank & Partner Discount Rules | configEditor | 1 | 0 | — |
| `ADM-155` | Special Price & Guest Offer Configurator | configEditor | 1 | 0 | — |
| `ADM-156` | Discount Limits, Guardrails & Commercial Controls | configEditor | 1 | 0 | — |
| `ADM-157` | Rule Test, Simulation & AI Recommendation Workspace | listDetail | 1 | 0 | — |

## Thin screens in this batch

**ADM-148, ADM-150, ADM-151, ADM-152, ADM-153, ADM-157 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-148",
  "name": "Promotion Rule Builder",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "2",
   "number": "1",
   "page": 22
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/promotion-rule-builder-adm-148",
   "component": "apps/ticvai-web/src/routes/commercial/PromotionRuleBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-149",
    "ADM-150",
    "ADM-151",
    "ADM-152",
    "ADM-153",
    "ADM-154",
    "ADM-155",
    "ADM-156",
    "ADM-157"
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
     "to": "ADM-149",
     "trigger": "Works in Percentage & Fixed Discount Configurator",
     "provenance": "flow F155 step 1→2",
     "operation": "setPromotionRule"
    },
    {
     "to": "ADM-150",
     "trigger": "Works in Cart & Transaction Threshold Rules",
     "provenance": "flow F155 step 3→4",
     "operation": "setPromotionRule"
    },
    {
     "to": "ADM-151",
     "trigger": "Works in Volume, Bulk & Tier Discount Configurator",
     "provenance": "flow F155 step 5→6",
     "operation": "setPromotionRule"
    },
    {
     "to": "ADM-152",
     "trigger": "Works in Time-Based & Seasonal Discount Rules",
     "provenance": "flow F155 step 7→8",
     "operation": "setPromotionRule"
    },
    {
     "to": "ADM-153",
     "trigger": "Works in Customer, Membership & Segment Discount Rules",
     "provenance": "flow F155 step 9→10",
     "operation": "setPromotionRule"
    },
    {
     "to": "ADM-154",
     "trigger": "Works in Payment Method, Bank & Partner Discount Rules",
     "provenance": "flow F155 step 11→12",
     "operation": "setPromotionRule"
    },
    {
     "to": "ADM-155",
     "trigger": "Works in Special Price & Guest Offer Configurator",
     "provenance": "flow F155 step 13→14",
     "operation": "setPromotionRule"
    },
    {
     "to": "ADM-156",
     "trigger": "Works in Discount Limits, Guardrails & Commercial Controls",
     "provenance": "flow F155 step 15→16",
     "operation": "setPromotionRule"
    },
    {
     "to": "ADM-157",
     "trigger": "Works in Rule Test, Simulation & AI Recommendation Workspace",
     "provenance": "flow F155 step 17→18",
     "operation": "setPromotionRule"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide the main no-code workspace for creating the commercial logic behind a promotion.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 22"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 22"
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
       "label": "Rule ordering",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 22 §Support"
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
       "impliedBy": "setPromotionRule"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The promotion rule list.",
   "error": "Could not load. Names which read failed and leaves the promotion rule untouched.",
   "emptyFirstRun": "No promotion rule yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the promotion rule are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setPromotionRule",
    "contract": "promotions",
    "purpose": "Promotion Rule Builder",
    "trigger": "onAction",
    "invalidates": [
     "setPromotionRule"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-148"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 22. 0 of 0 labels bound to a contract property; 1 of 51 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-149",
  "name": "Percentage & Fixed Discount Configurator",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "2",
   "number": "2",
   "page": 24
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/percentage-fixed-discount-configurator-adm-149",
   "component": "apps/ticvai-web/src/routes/commercial/PercentageFixedDiscountConfigurator.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-148"
   ],
   "exitTo": [
    "ADM-148"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-148, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-148",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F155 step 2→3",
     "operation": "listPercentageFixedDiscount"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure the two fundamental discount types required by the matrix. The matrix explicitly states that discounts may be defined as percentage or fixed value.",
  "gaps": [
   {
    "operation": null,
    "why": "**Percentage & Fixed Discount Configurator declares no operation that writes anything** — its only declared call is `listPercentageFixedDiscount`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
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
       "label": "Discount percentage",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 24 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum percentage",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 24 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum monetary discount",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 24 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Minimum qualifying amount",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 24 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Rounding method",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 24 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Discount amount",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 24 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Currency",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 24 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Minimum basket value",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 24 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum uses",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 24 §Configure"
      },
      {
       "kind": "textField",
       "label": "Whether applied per item or transaction",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 24 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The percentage fixed discount configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the percentage fixed discount untouched.",
   "emptyFirstRun": "No percentage fixed discount configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPercentageFixedDiscount",
    "contract": "promotions",
    "purpose": "Percentage & Fixed Discount Configurator",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-149"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 24. 0 of 0 labels bound to a contract property; 10 of 26 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-150",
  "name": "Cart & Transaction Threshold Rules",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "2",
   "number": "3",
   "page": 25
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/cart-transaction-threshold-rules-adm-150",
   "component": "apps/ticvai-web/src/routes/commercial/CartTransactionThresholdRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-148"
   ],
   "exitTo": [
    "ADM-148"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-148, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-148",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F155 step 4→5",
     "operation": "listCartTransactionThreshold"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure promotions triggered by basket value, ticket quantity, transaction value, or purchase composition. The matrix specifically requires rules such as if more than X tickets are purchased, apply Y discount to the entire transaction.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 25"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 25"
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
       "impliedBy": "listCartTransactionThreshold",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The cart transaction threshold list.",
   "error": "Could not load. Names which read failed and leaves the cart transaction threshold untouched.",
   "emptyFirstRun": "No cart transaction threshold yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the cart transaction threshold are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCartTransactionThreshold",
    "contract": "promotions",
    "purpose": "Cart & Transaction Threshold Rules",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "CartTransactionThresholdRulesView.nt",
    "CartTransactionThresholdRulesView.aed2505",
    "CartTransactionThresholdRulesView.aed50010",
    "CartTransactionThresholdRulesView.aed",
    "CartTransactionThresholdRulesView.taxCountsTowardThreshold"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-150"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 25. 0 of 0 labels bound to a contract property; 0 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-151",
  "name": "Volume, Bulk & Tier Discount Configurator",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "2",
   "number": "4",
   "page": 26
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/volume-bulk-tier-discount-configurator-adm-151",
   "component": "apps/ticvai-web/src/routes/commercial/VolumeBulkTierDiscountConfigurator.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-148"
   ],
   "exitTo": [
    "ADM-148"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-148, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-148",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F155 step 6→7",
     "operation": "listVolumeBulkTier"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Manage quantity-based and bulk-purchase commercial rules. The matrix requires configurable bulk thresholds and discount percentages, dedicated group pricing, and tiered bulk purchasing.",
  "gaps": [
   {
    "operation": null,
    "why": "**Volume, Bulk & Tier Discount Configurator declares no operation that writes anything** — its only declared call is `listVolumeBulkTier`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 26"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 26"
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
       "impliedBy": "listVolumeBulkTier",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The volume bulk tier list.",
   "error": "Could not load. Names which read failed and leaves the volume bulk tier untouched.",
   "emptyFirstRun": "No volume bulk tier yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the volume bulk tier are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listVolumeBulkTier",
    "contract": "promotions",
    "purpose": "Volume, Bulk & Tier Discount Configurator",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-151"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 26. 0 of 0 labels bound to a contract property; 0 of 4 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-152",
  "name": "Time-Based & Seasonal Discount Rules",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "2",
   "number": "5",
   "page": 27
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/time-based-seasonal-discount-rules-adm-152",
   "component": "apps/ticvai-web/src/routes/commercial/TimeBasedSeasonalDiscountRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-148"
   ],
   "exitTo": [
    "ADM-148"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-148, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-148",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F155 step 8→9",
     "operation": "listTimeBasedSeasonal"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure promotional pricing based on when the customer purchases or visits.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 27"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 27"
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
       "impliedBy": "listTimeBasedSeasonal",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The time-based seasonal discount list.",
   "error": "Could not load. Names which read failed and leaves the time-based seasonal discount untouched.",
   "emptyFirstRun": "No time-based seasonal discount yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the time-based seasonal discount are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listTimeBasedSeasonal",
    "contract": "promotions",
    "purpose": "Time-Based & Seasonal Discount Rules",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "TimeBasedSeasonalDiscountRulesView.summer",
    "TimeBasedSeasonalDiscountRulesView.ramadan",
    "TimeBasedSeasonalDiscountRulesView.eid",
    "TimeBasedSeasonalDiscountRulesView.schoolHolidays",
    "TimeBasedSeasonalDiscountRulesView.nationalDay"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-152"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 27. 0 of 0 labels bound to a contract property; 0 of 21 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-153",
  "name": "Customer, Membership & Segment Discount Rules",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "2",
   "number": "6",
   "page": 28
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/customer-membership-segment-discount-rules-adm-153",
   "component": "apps/ticvai-web/src/routes/commercial/CustomerMembershipSegmentDiscountRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-148"
   ],
   "exitTo": [
    "ADM-148"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-148, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-148",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F155 step 10→11",
     "operation": "listCustomerMembershipSegment"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure discounts based on who the customer is.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 28"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 28"
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
       "impliedBy": "listCustomerMembershipSegment",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The customer membership segment list.",
   "error": "Could not load. Names which read failed and leaves the customer membership segment untouched.",
   "emptyFirstRun": "No customer membership segment yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the customer membership segment are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCustomerMembershipSegment",
    "contract": "promotions",
    "purpose": "Customer, Membership & Segment Discount Rules",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "CustomerMembershipSegmentDiscountRulesView.customerSegment",
    "CustomerMembershipSegmentDiscountRulesView.crmSegment",
    "CustomerMembershipSegmentDiscountRulesView.guestCategory",
    "CustomerMembershipSegmentDiscountRulesView.ageCategory",
    "CustomerMembershipSegmentDiscountRulesView.membershipStatus"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-153"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 28. 0 of 0 labels bound to a contract property; 0 of 30 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-154",
  "name": "Payment Method, Bank & Partner Discount Rules",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "2",
   "number": "7",
   "page": 29
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/payment-method-bank-partner-discount-rules-adm-154",
   "component": "apps/ticvai-web/src/routes/commercial/PaymentMethodBankPartnerDiscountRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-148"
   ],
   "exitTo": [
    "ADM-148"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-148, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-148",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F155 step 12→13",
     "operation": "listPaymentMethodBank"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure discounts triggered by how the guest pays or which commercial partner they belong to. The matrix specifically includes discounts for payment types and bank credit/debit cards.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Membership programs. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 29 §Support"
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
       "label": "Partner bank",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 29 §Configure"
      },
      {
       "kind": "selectField",
       "label": "BIN/IIN eligibility reference",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 29 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Promotion period",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 29 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Eligible products",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 29 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Minimum spend",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 29 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Discount %",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 29 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum discount",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 29 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Number of uses",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 29 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Customer limit",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 29 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Campaign budget",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 29 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Membership programs",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 29 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The payment method bank configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the payment method bank untouched.",
   "emptyFirstRun": "No payment method bank configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPaymentMethodBank",
    "contract": "promotions",
    "purpose": "Payment Method, Bank & Partner Discount Rules",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-154"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 29. 0 of 0 labels bound to a contract property; 11 of 33 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-155",
  "name": "Special Price & Guest Offer Configurator",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "2",
   "number": "8",
   "page": 30
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/special-price-guest-offer-configurator-adm-155",
   "component": "apps/ticvai-web/src/routes/commercial/SpecialPriceGuestOfferConfigurator.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-148"
   ],
   "exitTo": [
    "ADM-148"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-148, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-148",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F155 step 14→15",
     "operation": "listSpecialPriceGuest"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configuration) and no display directory — it is settings, not a population",
  "purpose": "Manage commercially distinct special-price products and targeted offers without unnecessarily duplicating product SKUs.",
  "gaps": [
   {
    "operation": null,
    "why": "**Special Price & Guest Offer Configurator declares no operation that writes anything** — its only declared call is `listSpecialPriceGuest`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
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
       "label": "Offer name",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 30 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Eligible product",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 30 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Eligible guest",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 30 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Price",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 30 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Discount",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 30 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Valid dates",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 30 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Valid visit dates",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 30 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Quantity",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 30 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Channel",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 30 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 30 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Capacity",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 30 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Restrictions",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 30 §Configuration"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The special price guest configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the special price guest untouched.",
   "emptyFirstRun": "No special price guest configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listSpecialPriceGuest",
    "contract": "promotions",
    "purpose": "Special Price & Guest Offer Configurator",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-155"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 30. 0 of 0 labels bound to a contract property; 12 of 29 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-156",
  "name": "Discount Limits, Guardrails & Commercial Controls",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "2",
   "number": "9",
   "page": 31
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/discount-limits-guardrails-commercial-controls-adm-156",
   "component": "apps/ticvai-web/src/routes/commercial/DiscountLimitsGuardrailsCommercialControls.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-148"
   ],
   "exitTo": [
    "ADM-148"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-148, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-148",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F155 step 16→17",
     "operation": "listDiscountLimitGuardrail"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Protect the business from incorrectly configured discounts and excessive commercial exposure.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Maximum discount %",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 31 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum discount value",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 31 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Minimum selling price",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 31 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Minimum margin",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 31 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum transaction discount",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 31 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum customer discount",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 31 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum campaign exposure",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 31 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum redemption count",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 31 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Per-customer usage",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 31 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Per-account usage",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 31 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The discount limits guardrails configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the discount limits guardrails untouched.",
   "emptyFirstRun": "No discount limits guardrails configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listDiscountLimitGuardrail",
    "contract": "promotions",
    "purpose": "Discount Limits, Guardrails & Commercial Controls",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-156"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 31. 0 of 0 labels bound to a contract property; 10 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-157",
  "name": "Rule Test, Simulation & AI Recommendation Workspace",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "2",
   "number": "10",
   "page": 32
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/rule-test-simulation-ai-recommendation-workspace-adm-157",
   "component": "apps/ticvai-web/src/routes/commercial/RuleTestSimulationAiRecommendationWorkspace.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-148"
   ],
   "exitTo": [
    "ADM-148"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-148, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation."
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow administrators to test promotional rules before activating them. This is critical because the matrix requires simulation of redemption, discount exposure, revenue impact, margin impact and financial performance before activation.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Campaign Manager. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 32 §Support roles including"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 32"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 32"
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
       "label": "Campaign Manager",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 32 §Support roles including"
      },
      {
       "kind": "banner",
       "label": "Permissions this screen separates",
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** Create rules, Edit rules, Change discount, Change thresholds, Change segments, Change dates, Override limits, Run simulation, Submit, Approve, Activate. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 32 §Permissions must independently control"
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
   "loading": "The rule test simulation list.",
   "error": "Could not load. Names which read failed and leaves the rule test simulation untouched.",
   "emptyFirstRun": "No rule test simulation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the rule test simulation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setRuleTestRecommendation",
    "contract": "promotions",
    "purpose": "Rule Test, Simulation & AI Recommendation Workspace",
    "trigger": "onAction",
    "invalidates": [
     "setRuleTestRecommendation"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-157"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 32. 0 of 0 labels bound to a contract property; 12 of 76 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "listCartTransactionThreshold": {
  "method": "GET",
  "path": "/cart-transaction-threshold",
  "contract": "promotions",
  "summary": "Cart & Transaction Threshold Rules",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "CartTransactionThresholdRulesView"
 },
 "listCustomerMembershipSegment": {
  "method": "GET",
  "path": "/customer-membership-segment",
  "contract": "promotions",
  "summary": "Customer, Membership & Segment Discount Rules",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "CustomerMembershipSegmentDiscountRulesView"
 },
 "listDiscountLimitGuardrail": {
  "method": "GET",
  "path": "/discount-limit-guardrail",
  "contract": "promotions",
  "summary": "Discount Limits, Guardrails & Commercial Controls",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "DiscountLimitsGuardrailsCommercialControlsView"
 },
 "listPaymentMethodBank": {
  "method": "GET",
  "path": "/payment-method-bank",
  "contract": "promotions",
  "summary": "Payment Method, Bank & Partner Discount Rules",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "PaymentMethodBankPartnerDiscountRulesView"
 },
 "listPercentageFixedDiscount": {
  "method": "GET",
  "path": "/percentage-fixed-discount",
  "contract": "promotions",
  "summary": "Percentage & Fixed Discount Configurator",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "PercentageFixedDiscountConfiguratorView"
 },
 "listSpecialPriceGuest": {
  "method": "GET",
  "path": "/special-price-guest",
  "contract": "promotions",
  "summary": "Special Price & Guest Offer Configurator",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "SpecialPriceGuestOfferConfiguratorView"
 },
 "listTimeBasedSeasonal": {
  "method": "GET",
  "path": "/time-based-seasonal",
  "contract": "promotions",
  "summary": "Time-Based & Seasonal Discount Rules",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "TimeBasedSeasonalDiscountRulesView"
 },
 "listVolumeBulkTier": {
  "method": "GET",
  "path": "/volume-bulk-tier",
  "contract": "promotions",
  "summary": "Volume, Bulk & Tier Discount Configurator",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "VolumeBulkTierDiscountConfiguratorView"
 },
 "setPromotionRule": {
  "method": "PUT",
  "path": "/promotion-rule",
  "contract": "promotions",
  "summary": "Promotion Rule Builder",
  "permission": "PRICE_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "PromotionRuleBuilderInput",
  "responds": "PromotionRuleBuilderView"
 },
 "setRuleTestRecommendation": {
  "method": "PUT",
  "path": "/rule-test-recommendation",
  "contract": "promotions",
  "summary": "Rule Test, Simulation & AI Recommendation Workspace",
  "permission": "PRICE_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "RuleTestSimulationAiRecommendationWorkspaceInput",
  "responds": "RuleTestSimulationAiRecommendationWorkspaceView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "CartTransactionThresholdRulesView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Cart & Transaction Threshold Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "nt": {
    "type": "string",
    "description": "nt"
   },
   "aed2505": {
    "type": "number",
    "description": "AED 250 5%"
   },
   "aed50010": {
    "type": "number",
    "description": "AED 500 10%"
   },
   "aed": {
    "type": "string",
    "description": "AED (the pack shows 15%, 1,000)"
   },
   "taxCountsTowardThreshold": {
    "type": "integer",
    "description": "Tax counts toward threshold"
   },
   "feesCount": {
    "type": "integer",
    "description": "Fees count"
   },
   "vouchersCount": {
    "type": "integer",
    "description": "Vouchers count"
   },
   "discountsAreEvaluatedBeforeAfterThreshold": {
    "type": "integer",
    "description": "Discounts are evaluated before/after threshold"
   },
   "voidedItemsAreExcluded": {
    "type": "string",
    "description": "Voided items are excluded"
   },
   "refundedItemsAffectQualification": {
    "type": "string",
    "description": "Refunded items affect qualification"
   }
  }
 },
 "CustomerMembershipSegmentDiscountRulesView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Customer, Membership & Segment Discount Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "customerSegment": {
    "type": "string",
    "description": "Customer segment"
   },
   "crmSegment": {
    "type": "string",
    "description": "CRM segment"
   },
   "guestCategory": {
    "type": "string",
    "description": "Guest category"
   },
   "ageCategory": {
    "type": "string",
    "description": "Age category"
   },
   "membershipStatus": {
    "type": "string",
    "description": "Membership status"
   },
   "membershipTier": {
    "type": "string",
    "description": "Membership tier"
   },
   "loyaltyTier": {
    "type": "string",
    "description": "Loyalty tier"
   },
   "annualPassHolder": {
    "type": "string",
    "description": "Annual pass holder"
   },
   "corporateAffiliation": {
    "type": "string",
    "description": "Corporate affiliation"
   },
   "partnerAffiliation": {
    "type": "string",
    "description": "Partner affiliation"
   },
   "account": {
    "type": "string",
    "description": "Account"
   },
   "countryResidency": {
    "type": "string",
    "description": "Country/residency"
   },
   "b2bCustomer": {
    "type": "string",
    "description": "B2B customer"
   }
  }
 },
 "DiscountLimitsGuardrailsCommercialControlsView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Discount Limits, Guardrails & Commercial Controls displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "maximumDiscount": {
    "type": "number",
    "description": "Maximum discount %"
   },
   "maximumDiscountValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Maximum discount value"
   },
   "minimumSellingPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Minimum selling price"
   },
   "minimumMargin": {
    "type": "number",
    "description": "Minimum margin"
   },
   "maximumTransactionDiscount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Maximum transaction discount"
   },
   "maximumCustomerDiscount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Maximum customer discount"
   },
   "maximumCampaignExposure": {
    "type": "string",
    "description": "Maximum campaign exposure"
   },
   "maximumRedemptionCount": {
    "type": "integer",
    "description": "Maximum redemption count"
   },
   "perCustomerUsage": {
    "type": "string",
    "description": "Per-customer usage"
   },
   "perAccountUsage": {
    "type": "string",
    "description": "Per-account usage"
   },
   "maximumDiscount15": {
    "type": "number",
    "description": "Maximum discount: 15%"
   },
   "maximumDiscount25": {
    "type": "number",
    "description": "Maximum discount: 25%"
   },
   "maximumDiscount40": {
    "type": "number",
    "description": "Maximum discount: 40%"
   },
   "above40": {
    "type": "number",
    "description": "Above 40%"
   },
   "requireApproval": {
    "type": "boolean",
    "description": "Require approval"
   },
   "requiredByTheMatrix": {
    "type": "string",
    "description": "required by the matrix"
   }
  }
 },
 "PaymentMethodBankPartnerDiscountRulesView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Payment Method, Bank & Partner Discount Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "creditCard": {
    "type": "string",
    "description": "Credit card"
   },
   "debitCard": {
    "type": "string",
    "description": "Debit card"
   },
   "visa": {
    "type": "string",
    "description": "Visa"
   },
   "mastercard": {
    "type": "string",
    "description": "Mastercard"
   },
   "mada": {
    "type": "string",
    "description": "Mada"
   },
   "applePay": {
    "type": "string",
    "description": "Apple Pay"
   },
   "wallet": {
    "type": "string",
    "description": "Wallet"
   },
   "giftCard": {
    "type": "string",
    "description": "Gift card"
   },
   "bankSpecificCard": {
    "type": "string",
    "description": "Bank-specific card"
   },
   "selectedPaymentGateway": {
    "type": "string",
    "description": "Selected payment gateway"
   },
   "partnerBank": {
    "type": "string",
    "description": "Partner bank"
   },
   "binIinEligibilityReference": {
    "type": "string",
    "description": "BIN/IIN eligibility reference"
   },
   "promotionPeriod": {
    "type": "string",
    "format": "date-time",
    "description": "Promotion period"
   },
   "eligibleProducts": {
    "type": "string",
    "description": "Eligible products"
   },
   "minimumSpend": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Minimum spend"
   },
   "discount": {
    "type": "number",
    "description": "Discount %"
   },
   "maximumDiscount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Maximum discount"
   },
   "numberOfUses": {
    "type": "integer",
    "description": "Number of uses"
   },
   "customerLimit": {
    "type": "integer",
    "description": "Customer limit"
   },
   "campaignBudget": {
    "type": "string",
    "description": "Campaign budget"
   },
   "banks": {
    "type": "string",
    "description": "Banks"
   },
   "hotels": {
    "type": "string",
    "description": "Hotels"
   },
   "airlines": {
    "type": "string",
    "description": "Airlines"
   },
   "tourismPartners": {
    "type": "string",
    "description": "Tourism partners"
   },
   "corporatePartners": {
    "type": "string",
    "description": "Corporate partners"
   },
   "governmentPartners": {
    "type": "string",
    "description": "Government partners"
   },
   "membershipPrograms": {
    "type": "string",
    "description": "Membership programs"
   }
  }
 },
 "PercentageFixedDiscountConfiguratorView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Percentage & Fixed Discount Configurator displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "discountPercentage": {
    "type": "number",
    "description": "Discount percentage"
   },
   "maximumPercentage": {
    "type": "number",
    "description": "Maximum percentage"
   },
   "maximumMonetaryDiscount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Maximum monetary discount"
   },
   "minimumQualifyingAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Minimum qualifying amount"
   },
   "roundingMethod": {
    "type": "string",
    "description": "Rounding method"
   },
   "discountAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Discount amount"
   },
   "currency": {
    "type": "string",
    "description": "Currency"
   },
   "minimumBasketValue": {
    "type": "string",
    "description": "Minimum basket value"
   },
   "maximumUses": {
    "type": "string",
    "description": "Maximum uses"
   },
   "standardPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Standard price"
   },
   "currentSellingPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Current selling price"
   },
   "dynamicPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Dynamic price"
   },
   "membershipPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Membership price"
   },
   "b2bPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "B2B price"
   },
   "packagePrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Package price"
   },
   "negativePrices": {
    "type": "string",
    "description": "Negative prices"
   },
   "priceBelowConfiguredFloor": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price below configured floor"
   },
   "discountAboveAuthorizedCeiling": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Discount above authorized ceiling"
   },
   "marginBelowMinimumThreshold": {
    "type": "integer",
    "description": "Margin below minimum threshold"
   }
  }
 },
 "PromotionRuleBuilderInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table covers these fields** — the closest is promotions.upsell_rule at 5%, so this is not an update to anything the package stores today and no new table has been decided",
  "description": "**What Promotion Rule Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "logic": {
    "type": "string",
    "description": "logic"
   },
   "ruleName": {
    "type": "string",
    "description": "Rule name"
   },
   "ruleId": {
    "type": "string",
    "description": "Rule ID"
   },
   "promotion": {
    "type": "string",
    "description": "Promotion"
   },
   "description": {
    "type": "string",
    "description": "Description"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   },
   "businessEntity": {
    "type": "string",
    "description": "Business entity"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "ruleStatus": {
    "type": "string",
    "description": "Rule status"
   },
   "priority": {
    "type": "string",
    "description": "Priority"
   },
   "percentageDiscount": {
    "type": "number",
    "description": "Percentage discount"
   },
   "fixedDiscount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Fixed discount"
   },
   "fixedSellingPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Fixed selling price"
   },
   "freeProduct": {
    "type": "string",
    "description": "Free product"
   },
   "freeTicket": {
    "type": "string",
    "description": "Free ticket"
   },
   "addedValue": {
    "type": "string",
    "description": "Added value"
   },
   "voucher": {
    "type": "string",
    "description": "Voucher"
   },
   "rewardEntitlement": {
    "type": "string",
    "description": "Reward entitlement"
   },
   "nestedConditionGroups": {
    "type": "string",
    "description": "Nested condition groups"
   },
   "multipleOutcomes": {
    "type": "string",
    "description": "Multiple outcomes"
   },
   "ruleOrdering": {
    "type": "string",
    "description": "Rule ordering"
   }
  }
 },
 "PromotionRuleBuilderView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Promotion Rule Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "logic": {
    "type": "string",
    "description": "logic"
   },
   "ruleName": {
    "type": "string",
    "description": "Rule name"
   },
   "ruleId": {
    "type": "string",
    "description": "Rule ID"
   },
   "promotion": {
    "type": "string",
    "description": "Promotion"
   },
   "description": {
    "type": "string",
    "description": "Description"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   },
   "businessEntity": {
    "type": "string",
    "description": "Business entity"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "ruleStatus": {
    "type": "string",
    "description": "Rule status"
   },
   "priority": {
    "type": "string",
    "description": "Priority"
   },
   "percentageDiscount": {
    "type": "number",
    "description": "Percentage discount"
   },
   "fixedDiscount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Fixed discount"
   },
   "fixedSellingPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Fixed selling price"
   },
   "freeProduct": {
    "type": "string",
    "description": "Free product"
   },
   "freeTicket": {
    "type": "string",
    "description": "Free ticket"
   },
   "addedValue": {
    "type": "string",
    "description": "Added value"
   },
   "voucher": {
    "type": "string",
    "description": "Voucher"
   },
   "rewardEntitlement": {
    "type": "string",
    "description": "Reward entitlement"
   },
   "nestedConditionGroups": {
    "type": "string",
    "description": "Nested condition groups"
   },
   "multipleOutcomes": {
    "type": "string",
    "description": "Multiple outcomes"
   },
   "ruleOrdering": {
    "type": "string",
    "description": "Rule ordering"
   }
  }
 },
 "RuleTestSimulationAiRecommendationWorkspaceInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table covers these fields** — the closest is promotions.bundle_component at 3%, so this is not an update to anything the package stores today and no new table has been decided",
  "description": "**What Rule Test, Simulation & AI Recommendation Workspace submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "guest": {
    "type": "string",
    "description": "Guest"
   },
   "segment": {
    "type": "string",
    "description": "Segment"
   },
   "products": {
    "type": "string",
    "description": "Products"
   },
   "quantity": {
    "type": "integer",
    "description": "Quantity"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "date": {
    "type": "string",
    "format": "date-time",
    "description": "Date"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "membership": {
    "type": "string",
    "description": "Membership"
   },
   "loyalty": {
    "type": "string",
    "description": "Loyalty"
   },
   "paymentType": {
    "type": "string",
    "description": "Payment type"
   },
   "promoCode": {
    "type": "string",
    "description": "Promo code"
   },
   "familySegment": {
    "type": "string",
    "description": "Family segment ✓"
   },
   "b2c": {
    "type": "string",
    "description": "B2C ✓"
   },
   "validDate": {
    "type": "string",
    "format": "date-time",
    "description": "Valid date ✓"
   },
   "marketingAdministrator": {
    "type": "string",
    "description": "Marketing Administrator"
   },
   "campaignManager": {
    "type": "string",
    "description": "Campaign Manager"
   },
   "commercialManager": {
    "type": "string",
    "description": "Commercial Manager"
   },
   "revenueManager": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue Manager"
   },
   "finance": {
    "type": "string",
    "description": "Finance"
   },
   "b2bManager": {
    "type": "string",
    "description": "B2B Manager"
   },
   "venueManager": {
    "type": "string",
    "description": "Venue Manager"
   },
   "systemAdministrator": {
    "type": "string",
    "description": "System Administrator"
   },
   "approver": {
    "type": "string",
    "description": "Approver"
   },
   "auditor": {
    "type": "string",
    "description": "Auditor"
   },
   "changeDiscount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Change discount"
   },
   "changeThresholds": {
    "type": "string",
    "description": "Change thresholds"
   },
   "changeSegments": {
    "type": "string",
    "description": "Change segments"
   },
   "changeDates": {
    "type": "string",
    "description": "Change dates"
   },
   "currentPriceAndPricingFloors": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Current price and pricing floors"
   },
   "guestCustomerSegments": {
    "type": "string",
    "description": "Guest/customer segments"
   },
   "membershipAndTierEligibility": {
    "type": "string",
    "description": "Membership and tier eligibility"
   },
   "companySegmentsAndPartnerPricing": {
    "type": "string",
    "description": "Company segments and partner pricing"
   },
   "paymentMethodAndBankEligibility": {
    "type": "string",
    "description": "Payment-method and bank eligibility"
   },
   "productsEligibleForPromotionalRules": {
    "type": "string",
    "description": "Products eligible for promotional rules"
   },
   "revenueMarginAndDiscountExposure": {
    "type": "number",
    "description": "Revenue, margin and discount exposure"
   }
  }
 },
 "RuleTestSimulationAiRecommendationWorkspaceView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Rule Test, Simulation & AI Recommendation Workspace displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "guest": {
    "type": "string",
    "description": "Guest"
   },
   "segment": {
    "type": "string",
    "description": "Segment"
   },
   "products": {
    "type": "string",
    "description": "Products"
   },
   "quantity": {
    "type": "integer",
    "description": "Quantity"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "date": {
    "type": "string",
    "format": "date-time",
    "description": "Date"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "membership": {
    "type": "string",
    "description": "Membership"
   },
   "loyalty": {
    "type": "string",
    "description": "Loyalty"
   },
   "paymentType": {
    "type": "string",
    "description": "Payment type"
   },
   "promoCode": {
    "type": "string",
    "description": "Promo code"
   },
   "discount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Discount (the pack shows 15% / AED 90)"
   },
   "familySegment": {
    "type": "string",
    "description": "Family segment ✓"
   },
   "b2c": {
    "type": "string",
    "description": "B2C ✓"
   },
   "validDate": {
    "type": "string",
    "format": "date-time",
    "description": "Valid date ✓"
   },
   "rule421Qualified": {
    "type": "string",
    "description": "Rule 421 qualified"
   },
   "marketingAdministrator": {
    "type": "string",
    "description": "Marketing Administrator"
   },
   "campaignManager": {
    "type": "string",
    "description": "Campaign Manager"
   },
   "commercialManager": {
    "type": "string",
    "description": "Commercial Manager"
   },
   "revenueManager": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue Manager"
   },
   "finance": {
    "type": "string",
    "description": "Finance"
   },
   "b2bManager": {
    "type": "string",
    "description": "B2B Manager"
   },
   "venueManager": {
    "type": "string",
    "description": "Venue Manager"
   },
   "systemAdministrator": {
    "type": "string",
    "description": "System Administrator"
   },
   "approver": {
    "type": "string",
    "description": "Approver"
   },
   "auditor": {
    "type": "string",
    "description": "Auditor"
   },
   "changeDiscount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Change discount"
   },
   "changeThresholds": {
    "type": "string",
    "description": "Change thresholds"
   },
   "changeSegments": {
    "type": "string",
    "description": "Change segments"
   },
   "changeDates": {
    "type": "string",
    "description": "Change dates"
   },
   "currentPriceAndPricingFloors": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Current price and pricing floors"
   },
   "guestCustomerSegments": {
    "type": "string",
    "description": "Guest/customer segments"
   },
   "membershipAndTierEligibility": {
    "type": "string",
    "description": "Membership and tier eligibility"
   },
   "companySegmentsAndPartnerPricing": {
    "type": "string",
    "description": "Company segments and partner pricing"
   },
   "paymentMethodAndBankEligibility": {
    "type": "string",
    "description": "Payment-method and bank eligibility"
   },
   "productsEligibleForPromotionalRules": {
    "type": "string",
    "description": "Products eligible for promotional rules"
   },
   "revenueMarginAndDiscountExposure": {
    "type": "number",
    "description": "Revenue, margin and discount exposure"
   }
  }
 },
 "SpecialPriceGuestOfferConfiguratorView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Special Price & Guest Offer Configurator displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "twoParksPass": {
    "type": "string",
    "description": "Two-parks pass"
   },
   "multiParksPass": {
    "type": "string",
    "description": "Multi-parks pass"
   },
   "ladiesNight": {
    "type": "string",
    "description": "Ladies night"
   },
   "annualPass": {
    "type": "string",
    "description": "Annual pass"
   },
   "familyPass": {
    "type": "string",
    "description": "Family pass"
   },
   "offerName": {
    "type": "string",
    "description": "Offer name"
   },
   "eligibleProduct": {
    "type": "string",
    "description": "Eligible product"
   },
   "eligibleGuest": {
    "type": "string",
    "description": "Eligible guest"
   },
   "price": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price"
   },
   "discount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Discount"
   },
   "validDates": {
    "type": "string",
    "description": "Valid dates"
   },
   "validVisitDates": {
    "type": "string",
    "description": "Valid visit dates"
   },
   "quantity": {
    "type": "integer",
    "description": "Quantity"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "capacity": {
    "type": "integer",
    "description": "Capacity"
   },
   "restrictions": {
    "type": "string",
    "description": "Restrictions"
   },
   "residentPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Resident price"
   },
   "touristPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Tourist price"
   },
   "employeePrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Employee price"
   },
   "studentPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Student price"
   },
   "schoolPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "School price"
   },
   "familyPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Family price"
   },
   "groupPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Group price"
   },
   "partnerPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Partner price"
   }
  }
 },
 "TimeBasedSeasonalDiscountRulesView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Time-Based & Seasonal Discount Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "summer": {
    "type": "string",
    "description": "Summer"
   },
   "ramadan": {
    "type": "string",
    "description": "Ramadan"
   },
   "eid": {
    "type": "string",
    "description": "Eid"
   },
   "schoolHolidays": {
    "type": "string",
    "description": "School holidays"
   },
   "nationalDay": {
    "type": "string",
    "description": "National Day"
   },
   "peakOffPeak": {
    "type": "string",
    "description": "Peak/off-peak"
   },
   "customSeasons": {
    "type": "string",
    "description": "Custom seasons"
   },
   "purchaseDate": {
    "type": "string",
    "format": "date-time",
    "description": "Purchase date"
   },
   "visitDate": {
    "type": "string",
    "format": "date-time",
    "description": "Visit date"
   },
   "daysBeforeVisit": {
    "type": "string",
    "description": "Days-before-visit"
   },
   "hoursBeforeVisit": {
    "type": "string",
    "description": "Hours-before-visit"
   },
   "dayOfWeek": {
    "type": "string",
    "description": "Day of week"
   },
   "time": {
    "type": "string",
    "format": "date-time",
    "description": "Time"
   },
   "timeslot": {
    "type": "string",
    "description": "Timeslot"
   },
   "season": {
    "type": "string",
    "description": "Season"
   },
   "eventPeriod": {
    "type": "string",
    "format": "date-time",
    "description": "Event period"
   }
  }
 },
 "VolumeBulkTierDiscountConfiguratorView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Volume, Bulk & Tier Discount Configurator displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "tyNt": {
    "type": "string",
    "description": "ty nt"
   },
   "minimumQuantity": {
    "type": "integer",
    "description": "Minimum quantity"
   },
   "maximumQuantity": {
    "type": "integer",
    "description": "Maximum quantity"
   },
   "discount": {
    "type": "number",
    "description": "Discount %"
   },
   "discountValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Discount value"
   },
   "fixedUnitPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Fixed unit price"
   },
   "eligibleProduct": {
    "type": "string",
    "description": "Eligible product"
   },
   "eligibleCustomer": {
    "type": "string",
    "description": "Eligible customer"
   },
   "eligibleChannel": {
    "type": "string",
    "description": "Eligible channel"
   },
   "schools": {
    "type": "string",
    "description": "Schools"
   }
  }
 }
}
```
