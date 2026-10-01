# WS47 — Promotions   Bundles Management board 3

**10 screens · 10 operations · 15 schemas · 2 permissions**

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
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-158` | Coupon & Promo Code Command Center | commandCentre | 1 | 0 | — |
| `ADM-159` | Coupon & Promo Code Builder | configEditor | 1 | 0 | — |
| `ADM-160` | Unique Code Generation & Batch Manager | configEditor | 1 | 0 | — |
| `ADM-161` | Code Eligibility & Restriction Manager | listDetail | 1 | 0 | — |
| `ADM-162` | Usage, Capacity & Frequency Control | listDetail | 1 | 0 | — |
| `ADM-163` | Validity, Date & Time Control | listDetail | 1 | 0 | — |
| `ADM-164` | Code Distribution & Assignment Manager | listDetail | 1 | 0 | — |
| `ADM-165` | Redemption Monitor & Code Lookup | listDetail | 1 | 0 | — |
| `ADM-166` | Code Security, Fraud & Exception Center | listDetail | 1 | 0 | — |
| `ADM-167` | Redemption Analytics, Audit & AI Optimization | commandCentre | 1 | 0 | — |

## Thin screens in this batch

**ADM-161, ADM-162, ADM-163, ADM-164, ADM-165, ADM-166 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-158",
  "name": "Coupon & Promo Code Command Center",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "3",
   "number": "1",
   "page": 36
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/coupon-promo-code-command-center-adm-158",
   "component": "apps/ticvai-web/src/routes/commercial/CouponPromoCodeCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-159",
    "ADM-160",
    "ADM-161",
    "ADM-162",
    "ADM-163",
    "ADM-164",
    "ADM-165",
    "ADM-166",
    "ADM-167"
   ],
   "inferred": false,
   "notes": "**The board's hub.** The workshop specified this module as boards of ten and opened each with a command centre; the other nine screens are that board's detail, so they are reached from here and return here.",
   "transitions": [
    {
     "to": "ADM-002",
     "trigger": "Platform Dashboard",
     "provenance": "derived — ADM-002 declares entryState.params  and ADM-158 holds none of them. The edge carries nothing: ADM-158 is opened from ADM-002, so this edge is the way back and ADM-002 keeps its own state"
    },
    {
     "to": "ADM-159",
     "trigger": "Works in Coupon & Promo Code Builder",
     "provenance": "flow F156 step 1→2",
     "operation": "listCouponCodes"
    },
    {
     "to": "ADM-160",
     "trigger": "Works in Unique Code Generation & Batch Manager",
     "provenance": "flow F156 step 3→4",
     "operation": "listCouponCodes"
    },
    {
     "to": "ADM-161",
     "trigger": "Works in Code Eligibility & Restriction Manager",
     "provenance": "flow F156 step 5→6",
     "operation": "listCouponCodes"
    },
    {
     "to": "ADM-162",
     "trigger": "Works in Usage, Capacity & Frequency Control",
     "provenance": "flow F156 step 7→8",
     "operation": "listCouponCodes"
    },
    {
     "to": "ADM-163",
     "trigger": "Works in Validity, Date & Time Control",
     "provenance": "flow F156 step 9→10",
     "operation": "listCouponCodes"
    },
    {
     "to": "ADM-164",
     "trigger": "Works in Code Distribution & Assignment Manager",
     "provenance": "flow F156 step 11→12",
     "operation": "listCouponCodes"
    },
    {
     "to": "ADM-165",
     "trigger": "Works in Redemption Monitor & Code Lookup",
     "provenance": "flow F156 step 13→14",
     "operation": "listCouponCodes"
    },
    {
     "to": "ADM-166",
     "trigger": "Works in Code Security, Fraud & Exception Center",
     "provenance": "flow F156 step 15→16",
     "operation": "listCouponCodes"
    },
    {
     "to": "ADM-167",
     "trigger": "Works in Redemption Analytics, Audit & AI Optimization",
     "provenance": "flow F156 step 17→18",
     "operation": "listCouponCodes"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§KPI Cards) and a per-row directory (§Show) — counts over a population, then the population",
  "purpose": "Provide the central operational dashboard for all coupon, promo-code, and promotional voucher activities.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 3 actions on this screen and the screen declares 1 operation.** Unserved: Draft, Pending Approval, Capacity Reached. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 36 §Support"
   }
  ],
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Active Code Campaigns",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 36 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Active Coupons",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 36 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Unique Codes Issued",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 36 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Codes Redeemed",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 36 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Redemption Rate",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 36 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Unused Codes",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 36 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Expired Codes",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 36 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Suspended Codes",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 36 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Remaining Redemption Capacity",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 36 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Discount Granted",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 36 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Revenue Generated",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 36 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Average Order Value",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 36 §KPI Cards"
      },
      {
       "kind": "metricTile",
       "label": "Fraud/Suspicious Usage Alerts",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 36 §KPI Cards"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every coupon promo code",
       "columns": [
        "Top-performing codes",
        "Redemption trend",
        "Redemption by channel",
        "Redemption by venue",
        "Redemption by partner",
        "Redemption by customer segment",
        "Discount exposure",
        "Campaign budget consumption"
       ],
       "bindsTo": "CouponCode",
       "operation": "listCouponCodes",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 36 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected coupon promo code",
       "bindsTo": "CouponCode",
       "columns": [
        "Top-performing codes",
        "Redemption trend",
        "Redemption by channel",
        "Redemption by venue",
        "Redemption by partner",
        "Redemption by customer segment",
        "Discount exposure",
        "Campaign budget consumption"
       ],
       "notes": null,
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 36 §Show"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Draft",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 36 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Pending Approval",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 36 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Capacity Reached",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 36 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The coupon promo code list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the coupon promo code untouched.",
   "emptyFirstRun": "No coupon promo code yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the coupon promo code are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCouponCodes",
    "contract": "promotions",
    "purpose": "List generated codes",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "campaignId",
     "from": "navigation"
    }
   ],
   "coldEntry": "**Reached from the list that owns it**, so the identifier arrives with the navigation. Opened cold without one, the screen says what is missing and offers that list — never an empty form that looks configurable."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-158",
   "workshopBoard": "wireframes/WS108 Promotions   Bundles Management Board 3.dc.html#adm-158"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 36. 0 of 8 labels bound to a contract property; 24 of 36 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-159",
  "name": "Coupon & Promo Code Builder",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "3",
   "number": "2",
   "page": 37
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/coupon-promo-code-builder-adm-159",
   "component": "apps/ticvai-web/src/routes/commercial/CouponPromoCodeBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-158"
   ],
   "exitTo": [
    "ADM-158"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-158, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-158",
     "trigger": "Coupon & Promo Code Command Center",
     "provenance": "derived — ADM-158 declares entryState.params campaignId and ADM-159 holds none of them. The edge carries nothing: ADM-159 is opened from ADM-158, so this edge is the way back and ADM-158 keeps its own state"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Create the commercial definition of a coupon or promo-code campaign.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Percentage discount",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 37 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Fixed-value discount",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 37 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Fixed promotional price",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 37 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Free product",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 37 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Free ticket",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 37 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Free add-on",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 37 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Upgrade",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 37 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Bundle benefit",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 37 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Added value",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 37 §Configure"
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
       "provenance": "contract operation setCouponPromoCode"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The coupon promo code configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the coupon promo code untouched.",
   "emptyFirstRun": "No coupon promo code configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setCouponPromoCode",
    "contract": "promotions",
    "purpose": "Coupon & Promo Code Builder",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-159",
   "workshopBoard": "wireframes/WS108 Promotions   Bundles Management Board 3.dc.html#adm-159"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 37. 0 of 0 labels bound to a contract property; 9 of 30 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-160",
  "name": "Unique Code Generation & Batch Manager",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "3",
   "number": "3",
   "page": 38
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/unique-code-generation-batch-manager-adm-160",
   "component": "apps/ticvai-web/src/routes/commercial/UniqueCodeGenerationBatchManager.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-158"
   ],
   "exitTo": [
    "ADM-158"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-158, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-158",
     "trigger": "Coupon & Promo Code Command Center",
     "provenance": "derived — ADM-158 declares entryState.params campaignId and ADM-160 holds none of them. The edge carries nothing: ADM-160 is opened from ADM-158, so this edge is the way back and ADM-158 keeps its own state"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Users define) and no display directory — it is settings, not a population",
  "purpose": "Generate and manage large quantities of secure unique promotional codes.",
  "gaps": [
   {
    "operation": null,
    "why": "**Unique Code Generation & Batch Manager declares no operation that writes anything** — its only declared call is `listUniqueCodeGeneration`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
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
       "label": "Campaign",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 38 §Users define"
      },
      {
       "kind": "selectField",
       "label": "Number of codes",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 38 §Users define"
      },
      {
       "kind": "selectField",
       "label": "Code length",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 38 §Users define"
      },
      {
       "kind": "selectField",
       "label": "Prefix",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 38 §Users define"
      },
      {
       "kind": "selectField",
       "label": "Suffix",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 38 §Users define"
      },
      {
       "kind": "selectField",
       "label": "Character type",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 38 §Users define"
      },
      {
       "kind": "selectField",
       "label": "Case sensitivity",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 38 §Users define"
      },
      {
       "kind": "selectField",
       "label": "Expiration",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 38 §Users define"
      },
      {
       "kind": "selectField",
       "label": "Number of uses",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 38 §Users define"
      },
      {
       "kind": "selectField",
       "label": "Distribution owner",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 38 §Users define"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The unique code generation configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the unique code generation untouched.",
   "emptyFirstRun": "No unique code generation configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listUniqueCodeGeneration",
    "contract": "promotions",
    "purpose": "Unique Code Generation & Batch Manager",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-160",
   "workshopBoard": "wireframes/WS108 Promotions   Bundles Management Board 3.dc.html#adm-160"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 38. 0 of 0 labels bound to a contract property; 10 of 26 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-161",
  "name": "Code Eligibility & Restriction Manager",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "3",
   "number": "4",
   "page": 39
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/code-eligibility-restriction-manager-adm-161",
   "component": "apps/ticvai-web/src/routes/commercial/CodeEligibilityRestrictionManager.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-158"
   ],
   "exitTo": [
    "ADM-158"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-158, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-158",
     "trigger": "Coupon & Promo Code Command Center",
     "provenance": "derived — ADM-158 declares entryState.params campaignId and ADM-161 holds none of them. The edge carries nothing: ADM-161 is opened from ADM-158, so this edge is the way back and ADM-158 keeps its own state"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Determine where, when, by whom, and against what a code can be redeemed. The matrix explicitly requires promo codes to support restrictions for usage, dates, duration, capacity, frequency, location, group, partner, operating area, and sales channel.",
  "gaps": [
   {
    "operation": null,
    "why": "**Code Eligibility & Restriction Manager declares no operation that writes anything** — its only declared call is `listCodeEligibilityRestriction`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 39"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 39"
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
       "impliedBy": "listCodeEligibilityRestriction",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The code eligibility restriction list.",
   "error": "Could not load. Names which read failed and leaves the code eligibility restriction untouched.",
   "emptyFirstRun": "No code eligibility restriction yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the code eligibility restriction are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCodeEligibilityRestriction",
    "contract": "promotions",
    "purpose": "Code Eligibility & Restriction Manager",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "CodeEligibilityRestrictionManagerView.productScopes"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-161",
   "workshopBoard": "wireframes/WS108 Promotions   Bundles Management Board 3.dc.html#adm-161"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 39. 0 of 0 labels bound to a contract property; 0 of 38 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-162",
  "name": "Usage, Capacity & Frequency Control",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "3",
   "number": "5",
   "page": 41
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/usage-capacity-frequency-control-adm-162",
   "component": "apps/ticvai-web/src/routes/commercial/UsageCapacityFrequencyControl.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-158"
   ],
   "exitTo": [
    "ADM-158"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-158, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-158",
     "trigger": "Coupon & Promo Code Command Center",
     "provenance": "derived — ADM-158 declares entryState.params campaignId and ADM-162 holds none of them. The edge carries nothing: ADM-162 is opened from ADM-158, so this edge is the way back and ADM-158 keeps its own state"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Control exactly how frequently and how many times promotional codes may be redeemed.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every usage capacity frequency",
       "columns": [
        "UsageCapacityFrequencyControlView.issued",
        "UsageCapacityFrequencyControlView.redeemed",
        "UsageCapacityFrequencyControlView.reservedPending",
        "UsageCapacityFrequencyControlView.remaining"
       ],
       "bindsTo": "UsageCapacityFrequencyControlView",
       "operation": "listUsageCapacityFrequency",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 41 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected usage capacity frequency",
       "bindsTo": "UsageCapacityFrequencyControlView",
       "columns": [
        "UsageCapacityFrequencyControlView.issued",
        "UsageCapacityFrequencyControlView.redeemed",
        "UsageCapacityFrequencyControlView.reservedPending",
        "UsageCapacityFrequencyControlView.remaining"
       ],
       "notes": null,
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 41 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The usage capacity frequency list.",
   "error": "Could not load. Names which read failed and leaves the usage capacity frequency untouched.",
   "emptyFirstRun": "No usage capacity frequency yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the usage capacity frequency are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listUsageCapacityFrequency",
    "contract": "promotions",
    "purpose": "Usage, Capacity & Frequency Control",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "UsageCapacityFrequencyControlView.issued",
    "UsageCapacityFrequencyControlView.redeemed",
    "UsageCapacityFrequencyControlView.reservedPending",
    "UsageCapacityFrequencyControlView.remaining"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-162",
   "workshopBoard": "wireframes/WS108 Promotions   Bundles Management Board 3.dc.html#adm-162"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 41. 4 of 4 labels bound to a contract property; 4 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-163",
  "name": "Validity, Date & Time Control",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "3",
   "number": "6",
   "page": 41
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/validity-date-time-control-adm-163",
   "component": "apps/ticvai-web/src/routes/commercial/ValidityDateTimeControl.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-158"
   ],
   "exitTo": [
    "ADM-158"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-158, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-158",
     "trigger": "Coupon & Promo Code Command Center",
     "provenance": "derived — ADM-158 declares entryState.params campaignId and ADM-163 holds none of them. The edge carries nothing: ADM-163 is opened from ADM-158, so this edge is the way back and ADM-158 keeps its own state"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Control the temporal validity of coupons and codes.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 41"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 41"
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
       "impliedBy": "listValidityDateTime",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The validity date time list.",
   "error": "Could not load. Names which read failed and leaves the validity date time untouched.",
   "emptyFirstRun": "No validity date time yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the validity date time are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listValidityDateTime",
    "contract": "promotions",
    "purpose": "Validity, Date & Time Control",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "ValidityDateTimeControlView.blackoutDates",
    "ValidityDateTimeControlView.holidays",
    "ValidityDateTimeControlView.selectedTimeslots"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-163",
   "workshopBoard": "wireframes/WS108 Promotions   Bundles Management Board 3.dc.html#adm-163"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 41. 0 of 0 labels bound to a contract property; 0 of 15 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-164",
  "name": "Code Distribution & Assignment Manager",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "3",
   "number": "7",
   "page": 42
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/code-distribution-assignment-manager-adm-164",
   "component": "apps/ticvai-web/src/routes/commercial/CodeDistributionAssignmentManager.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-158"
   ],
   "exitTo": [
    "ADM-158"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-158, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-158",
     "trigger": "Coupon & Promo Code Command Center",
     "provenance": "derived — ADM-158 declares entryState.params campaignId and ADM-164 holds none of them. The edge carries nothing: ADM-164 is opened from ADM-158, so this edge is the way back and ADM-158 keeps its own state"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Manage how promotional codes are allocated and distributed.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every code distribution",
       "columns": [
        "CodeDistributionAssignmentManagerView.generated",
        "CodeDistributionAssignmentManagerView.assigned",
        "CodeDistributionAssignmentManagerView.sent",
        "CodeDistributionAssignmentManagerView.delivered",
        "CodeDistributionAssignmentManagerView.viewed",
        "CodeDistributionAssignmentManagerView.redeemed",
        "CodeDistributionAssignmentManagerView.expired",
        "CodeDistributionAssignmentManagerView.cancelled"
       ],
       "bindsTo": "CodeDistributionAssignmentManagerView",
       "operation": "setCodeDistributionManager",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 42 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected code distribution",
       "bindsTo": "CodeDistributionAssignmentManagerView",
       "columns": [
        "CodeDistributionAssignmentManagerView.generated",
        "CodeDistributionAssignmentManagerView.assigned",
        "CodeDistributionAssignmentManagerView.sent",
        "CodeDistributionAssignmentManagerView.delivered",
        "CodeDistributionAssignmentManagerView.viewed",
        "CodeDistributionAssignmentManagerView.redeemed",
        "CodeDistributionAssignmentManagerView.expired",
        "CodeDistributionAssignmentManagerView.cancelled"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Distribution Channels”, “Codes may be assigned to”, “External Partner Example”.",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 42 §Show"
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
       "provenance": "contract operation setCodeDistributionManager"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The code distribution list.",
   "error": "Could not load. Names which read failed and leaves the code distribution untouched.",
   "emptyFirstRun": "No code distribution yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the code distribution are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setCodeDistributionManager",
    "contract": "promotions",
    "purpose": "Code Distribution & Assignment Manager",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "preloaded": [
    "CodeDistributionAssignmentManagerView.generated",
    "CodeDistributionAssignmentManagerView.assigned",
    "CodeDistributionAssignmentManagerView.sent",
    "CodeDistributionAssignmentManagerView.delivered",
    "CodeDistributionAssignmentManagerView.viewed",
    "CodeDistributionAssignmentManagerView.redeemed"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-164",
   "workshopBoard": "wireframes/WS108 Promotions   Bundles Management Board 3.dc.html#adm-164"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 42. 8 of 8 labels bound to a contract property; 8 of 40 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-165",
  "name": "Redemption Monitor & Code Lookup",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "3",
   "number": "8",
   "page": 43
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/redemption-monitor-code-lookup-adm-165",
   "component": "apps/ticvai-web/src/routes/commercial/RedemptionMonitorCodeLookup.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-158"
   ],
   "exitTo": [
    "ADM-158"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-158, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-158",
     "trigger": "Coupon & Promo Code Command Center",
     "provenance": "derived — ADM-158 declares entryState.params campaignId and ADM-165 holds none of them. The edge carries nothing: ADM-165 is opened from ADM-158, so this edge is the way back and ADM-158 keeps its own state"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Provide real-time operational visibility into coupon and promo-code redemption.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every redemption code lookup",
       "columns": [
        "RedemptionMonitorCodeLookupView.code",
        "Redemption date/time",
        "RedemptionMonitorCodeLookupView.product",
        "RedemptionMonitorCodeLookupView.originalValue",
        "RedemptionMonitorCodeLookupView.discount",
        "RedemptionMonitorCodeLookupView.finalValue",
        "RedemptionMonitorCodeLookupView.channel",
        "RedemptionMonitorCodeLookupView.venue",
        "RedemptionMonitorCodeLookupView.devicePos",
        "RedemptionMonitorCodeLookupView.operator",
        "RedemptionMonitorCodeLookupView.validationResult"
       ],
       "bindsTo": "RedemptionMonitorCodeLookupView",
       "operation": "listRedemptionCodeLookup",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 43 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected redemption code lookup",
       "bindsTo": "RedemptionMonitorCodeLookupView",
       "columns": [
        "RedemptionMonitorCodeLookupView.code",
        "Redemption date/time",
        "RedemptionMonitorCodeLookupView.product",
        "RedemptionMonitorCodeLookupView.originalValue",
        "RedemptionMonitorCodeLookupView.discount",
        "RedemptionMonitorCodeLookupView.finalValue",
        "RedemptionMonitorCodeLookupView.channel",
        "RedemptionMonitorCodeLookupView.venue",
        "RedemptionMonitorCodeLookupView.devicePos",
        "RedemptionMonitorCodeLookupView.operator",
        "RedemptionMonitorCodeLookupView.validationResult"
       ],
       "notes": null,
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 43 §Show"
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
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** Promo code, Coupon ID, Batch ID, Transaction, Booking, Customer, Partner, Campaign. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 43 §Authorized users can search by"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The redemption code lookup list.",
   "error": "Could not load. Names which read failed and leaves the redemption code lookup untouched.",
   "emptyFirstRun": "No redemption code lookup yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the redemption code lookup are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listRedemptionCodeLookup",
    "contract": "promotions",
    "purpose": "Redemption Monitor & Code Lookup",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "RedemptionMonitorCodeLookupView.code",
    "Redemption date/time"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-165",
   "workshopBoard": "wireframes/WS108 Promotions   Bundles Management Board 3.dc.html#adm-165"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 43. 14 of 15 labels bound to a contract property; 23 of 37 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-166",
  "name": "Code Security, Fraud & Exception Center",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "3",
   "number": "9",
   "page": 44
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/code-security-fraud-exception-center-adm-166",
   "component": "apps/ticvai-web/src/routes/commercial/CodeSecurityFraudExceptionCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-158"
   ],
   "exitTo": [
    "ADM-158"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-158, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-158",
     "trigger": "Coupon & Promo Code Command Center",
     "provenance": "derived — ADM-158 declares entryState.params campaignId and ADM-166 holds none of them. The edge carries nothing: ADM-166 is opened from ADM-158, so this edge is the way back and ADM-158 keeps its own state"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Monitor) and no metric row",
  "purpose": "Detect promo-code abuse, leakage, abnormal redemption, and suspicious campaign behavior.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every code security fraud",
       "columns": [
        "CodeSecurityFraudExceptionCenterView.signalType"
       ],
       "bindsTo": "CodeSecurityFraudExceptionCenterView",
       "operation": "listCodeSecurityFraud",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 44 §Monitor"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected code security fraud",
       "bindsTo": "CodeSecurityFraudExceptionCenterView",
       "columns": [
        "CodeSecurityFraudExceptionCenterView.signalType"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Risk Levels”.",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 44 §Monitor"
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
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** Suspend individual code, Suspend batch, Suspend campaign, Block redemption, Reinstate code, Assign investigation, Add case note. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 44 §Authorized users can"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The code security fraud list.",
   "error": "Could not load. Names which read failed and leaves the code security fraud untouched.",
   "emptyFirstRun": "No code security fraud yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the code security fraud are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCodeSecurityFraud",
    "contract": "promotions",
    "purpose": "Code Security, Fraud & Exception Center",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "CodeSecurityFraudExceptionCenterView.signalType"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-166",
   "workshopBoard": "wireframes/WS108 Promotions   Bundles Management Board 3.dc.html#adm-166"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 44. 9 of 9 labels bound to a contract property; 16 of 27 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-167",
  "name": "Redemption Analytics, Audit & AI Optimization",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "3",
   "number": "10",
   "page": 45
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/redemption-analytics-audit-ai-optimization-adm-167",
   "component": "apps/ticvai-web/src/routes/commercial/RedemptionAnalyticsAuditAiOptimization.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-158"
   ],
   "exitTo": [
    "ADM-158"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-158, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-158",
     "trigger": "Coupon & Promo Code Command Center",
     "provenance": "derived — ADM-158 declares entryState.params campaignId and ADM-167 holds none of them. The edge carries nothing: ADM-167 is opened from ADM-158, so this edge is the way back and ADM-158 keeps its own state"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Board 3 shall be considered complete when: 1. Users can create common and unique promotional codes. 2. Coupons and promotional vouchers can be configured. 3. Large unique-code batches can be generated. 4. Codes can support single, multiple, capped, or unlimited redemption. 5. Usage can be limited per booking, customer, account, channel, venue, or campaign. 6. Date/time/relative validity rules are supported. 7. Product and ticket eligibility can be configured. 8. Customer and segment eligibility can be configured. 9. Channel, partner, and location restrictions can be configured. 10.Codes can tr",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Performance KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide complete performance analytics and governance for coupon and promo-code campaigns. Board 4 shall provide TICVAI with an enterprise-grade Advanced Promotion Mechanics Engine for promotions involving relationships between products, quantities, basket composition, rewards, and qualifying purchases. While Board 2 defines standard discounts and thresholds and Board 3 manages promo codes/coupons, Board 4 answers: “When the customer buys X, what exactly should TICVAI give them, discount, replace, upgrade, or add to the transaction?” The matrix requires mechanics such as Buy X Get X, Buy X Get Y, Buy N Get X, percentage/amount discounts on another product, cheapest-item-free, fixed-price combinations, cross-category F&B/Retail rewards, added-value gifts, and automatic cart-level promotion application. Board 4 shall contain 10 backend screens.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search redemption analytics audit",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 45 §Analyze by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Campaign",
        "Code",
        "Batch",
        "Product",
        "Venue",
        "Channel",
        "Customer segment",
        "Partner",
        "Date/time",
        "Promotion type"
       ],
       "notes": "The pack filters this screen by campaign, code, batch, product, venue, channel and 4 more — which are present is a decision the pack already made.",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 45 §Analyze by"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Codes generated",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 45 §Performance KPIs",
       "bindsTo": "RedemptionAnalyticsAuditAiOptimizationView.codesGenerated"
      },
      {
       "kind": "metricTile",
       "label": "Codes distributed",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 45 §Performance KPIs",
       "bindsTo": "RedemptionAnalyticsAuditAiOptimizationView.codesDistributed"
      },
      {
       "kind": "metricTile",
       "label": "Codes redeemed",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 45 §Performance KPIs",
       "bindsTo": "RedemptionAnalyticsAuditAiOptimizationView.codesRedeemed"
      },
      {
       "kind": "metricTile",
       "label": "Redemption rate",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 45 §Performance KPIs",
       "bindsTo": "RedemptionAnalyticsAuditAiOptimizationView.redemptionRate"
      },
      {
       "kind": "metricTile",
       "label": "Conversion rate",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 45 §Performance KPIs",
       "bindsTo": "RedemptionAnalyticsAuditAiOptimizationView.conversionRate"
      },
      {
       "kind": "metricTile",
       "label": "Revenue generated",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 45 §Performance KPIs",
       "bindsTo": "RedemptionAnalyticsAuditAiOptimizationView.revenueGenerated"
      },
      {
       "kind": "metricTile",
       "label": "Discount granted",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 45 §Performance KPIs",
       "bindsTo": "RedemptionAnalyticsAuditAiOptimizationView.discountGranted"
      },
      {
       "kind": "metricTile",
       "label": "Incremental revenue",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 45 §Performance KPIs",
       "bindsTo": "RedemptionAnalyticsAuditAiOptimizationView.incrementalRevenue"
      },
      {
       "kind": "metricTile",
       "label": "AOV uplift",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 45 §Performance KPIs",
       "bindsTo": "RedemptionAnalyticsAuditAiOptimizationView.aovUplift"
      },
      {
       "kind": "metricTile",
       "label": "Cost per redemption",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 45 §Performance KPIs",
       "bindsTo": "RedemptionAnalyticsAuditAiOptimizationView.costPerRedemption"
      },
      {
       "kind": "metricTile",
       "label": "Margin impact",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 45 §Performance KPIs",
       "bindsTo": "RedemptionAnalyticsAuditAiOptimizationView.marginImpact"
      },
      {
       "kind": "metricTile",
       "label": "Expired unused codes",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 45 §Performance KPIs",
       "bindsTo": "RedemptionAnalyticsAuditAiOptimizationView.expiredUnusedCodes"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The redemption analytics audit list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the redemption analytics audit untouched.",
   "emptyFirstRun": "No redemption analytics audit yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the redemption analytics audit are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listRedemption",
    "contract": "promotions",
    "purpose": "Redemption Analytics, Audit & AI Optimization",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "RedemptionAnalyticsAuditAiOptimizationView.codesGenerated",
    "RedemptionAnalyticsAuditAiOptimizationView.codesDistributed",
    "RedemptionAnalyticsAuditAiOptimizationView.codesRedeemed",
    "RedemptionAnalyticsAuditAiOptimizationView.redemptionRate",
    "RedemptionAnalyticsAuditAiOptimizationView.conversionRate",
    "RedemptionAnalyticsAuditAiOptimizationView.revenueGenerated"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-167",
   "workshopBoard": "wireframes/WS108 Promotions   Bundles Management Board 3.dc.html#adm-167"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 45. 12 of 22 labels bound to a contract property; 22 of 144 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "listCodeEligibilityRestriction": {
  "method": "GET",
  "path": "/code-eligibility-restriction",
  "contract": "promotions",
  "summary": "Code Eligibility & Restriction Manager",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "CodeEligibilityRestrictionManagerView"
 },
 "listCodeSecurityFraud": {
  "method": "GET",
  "path": "/code-security-fraud",
  "contract": "promotions",
  "summary": "Code Security, Fraud & Exception Center",
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
  "responds": "CodeSecurityFraudExceptionCenterView"
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
 "listRedemption": {
  "method": "GET",
  "path": "/redemption",
  "contract": "promotions",
  "summary": "Redemption Analytics, Audit & AI Optimization",
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
    "name": "campaign",
    "in": "query",
    "required": false
   },
   {
    "name": "code",
    "in": "query",
    "required": false
   },
   {
    "name": "batch",
    "in": "query",
    "required": false
   },
   {
    "name": "product",
    "in": "query",
    "required": false
   },
   {
    "name": "venue",
    "in": "query",
    "required": false
   },
   {
    "name": "channel",
    "in": "query",
    "required": false
   },
   {
    "name": "customerSegment",
    "in": "query",
    "required": false
   },
   {
    "name": "partner",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "RedemptionAnalyticsAuditAiOptimizationView"
 },
 "listRedemptionCodeLookup": {
  "method": "GET",
  "path": "/redemption-code-lookup",
  "contract": "promotions",
  "summary": "Redemption Monitor & Code Lookup",
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
    "name": "promoCode",
    "in": "query",
    "required": false
   },
   {
    "name": "couponId",
    "in": "query",
    "required": false
   },
   {
    "name": "batchId",
    "in": "query",
    "required": false
   },
   {
    "name": "transaction",
    "in": "query",
    "required": false
   },
   {
    "name": "booking",
    "in": "query",
    "required": false
   },
   {
    "name": "customer",
    "in": "query",
    "required": false
   },
   {
    "name": "partner",
    "in": "query",
    "required": false
   },
   {
    "name": "campaign",
    "in": "query",
    "required": false
   },
   {
    "name": "customerAccountReference",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "RedemptionMonitorCodeLookupView"
 },
 "listUniqueCodeGeneration": {
  "method": "GET",
  "path": "/unique-code-generation",
  "contract": "promotions",
  "summary": "Unique Code Generation & Batch Manager",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "UniqueCodeGenerationBatchManagerView"
 },
 "listUsageCapacityFrequency": {
  "method": "GET",
  "path": "/usage-capacity-frequency",
  "contract": "promotions",
  "summary": "Usage, Capacity & Frequency Control",
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
  "responds": "UsageCapacityFrequencyControlView"
 },
 "listValidityDateTime": {
  "method": "GET",
  "path": "/validity-date-time",
  "contract": "promotions",
  "summary": "Validity, Date & Time Control",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ValidityDateTimeControlView"
 },
 "setCodeDistributionManager": {
  "method": "PUT",
  "path": "/code-distribution-manager",
  "contract": "promotions",
  "summary": "Code Distribution & Assignment Manager",
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
  "requestBody": "CodeDistributionAssignmentManagerInput",
  "responds": "CodeDistributionAssignmentManagerView"
 },
 "setCouponPromoCode": {
  "method": "PUT",
  "path": "/coupon-promo-code",
  "contract": "promotions",
  "summary": "Coupon & Promo Code Builder",
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
  "requestBody": "CouponPromoCodeBuilderInput",
  "responds": "CouponPromoCodeBuilderView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "CodeDistributionAssignmentManagerInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Code Distribution & Assignment Manager submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "channelsType": {
    "type": "string",
    "enum": [
     "email",
     "sms",
     "whatsapp",
     "mobileApp",
     "crmJourney",
     "guestPortal",
     "b2bPortal",
     "partnerPortal",
     "pos",
     "callCenter",
     "api",
     "exportedBatch"
    ],
    "description": "Vocabulary listed under Distribution Channels."
   },
   "assigneeType": {
    "type": "string",
    "enum": [
     "individualCustomer",
     "customerSegment",
     "membershipAccount",
     "b2bCompany",
     "reseller",
     "travelAgency",
     "school",
     "hotel",
     "bank",
     "corporatePartner",
     "marketingCampaign"
    ],
    "description": "Who the codes are assigned to."
   },
   "batchId": {
    "type": "string",
    "description": "Batch ID"
   },
   "assigneeReference": {
    "type": "string",
    "description": "Customer, segment, account or partner the codes go to"
   },
   "quantity": {
    "type": "integer",
    "description": "Codes to assign"
   }
  }
 },
 "CodeDistributionAssignmentManagerView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Code Distribution & Assignment Manager displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "channelsType": {
    "type": "string",
    "enum": [
     "email",
     "sms",
     "whatsapp",
     "mobileApp",
     "crmJourney",
     "guestPortal",
     "b2bPortal",
     "partnerPortal",
     "pos",
     "callCenter",
     "api",
     "exportedBatch"
    ],
    "description": "Vocabulary listed under Distribution Channels."
   },
   "generated": {
    "type": "string",
    "description": "Generated"
   },
   "assigned": {
    "type": "string",
    "description": "Assigned"
   },
   "sent": {
    "type": "string",
    "description": "Sent"
   },
   "delivered": {
    "type": "string",
    "description": "Delivered"
   },
   "redeemed": {
    "type": "string",
    "description": "Redeemed"
   },
   "expired": {
    "type": "integer",
    "description": "Expired"
   },
   "cancelled": {
    "type": "integer",
    "description": "Cancelled"
   },
   "viewed": {
    "type": "string",
    "description": "Viewed where available"
   },
   "assigneeType": {
    "type": "string",
    "enum": [
     "individualCustomer",
     "customerSegment",
     "membershipAccount",
     "b2bCompany",
     "reseller",
     "travelAgency",
     "school",
     "hotel",
     "bank",
     "corporatePartner",
     "marketingCampaign"
    ],
    "description": "Who the codes are assigned to."
   },
   "batchId": {
    "type": "string",
    "description": "Batch ID"
   },
   "partner": {
    "type": "string",
    "description": "Partner, for a partner batch"
   }
  }
 },
 "CodeEligibilityRestrictionManagerView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Code Eligibility & Restriction Manager displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "partner": {
    "type": "string",
    "description": "Partner"
   },
   "businessEntity": {
    "type": "string",
    "description": "Business entity"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "location": {
    "type": "string",
    "description": "Location"
   },
   "operatingArea": {
    "type": "string",
    "description": "Operating area"
   },
   "productScopes": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "ticket",
      "ticketType",
      "product",
      "productCategory",
      "attraction",
      "event",
      "bundle",
      "membership",
      "fB",
      "retail",
      "addOn"
     ]
    },
    "description": "Products the code is restricted to."
   },
   "customerScopes": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "guestType",
      "crmSegment",
      "loyaltyTier",
      "b2bAccount",
      "corporateGroup",
      "b2b"
     ]
    },
    "description": "Customers the code is restricted to."
   },
   "channels": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "b2c",
      "pos",
      "mobilePos",
      "kiosk",
      "mobileApp",
      "callCenter",
      "reseller",
      "api"
     ]
    },
    "description": "Channels the code is valid on."
   }
  }
 },
 "CodeSecurityFraudExceptionCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Code Security, Fraud & Exception Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "levelsType": {
    "type": "string",
    "enum": [
     "low",
     "medium",
     "high",
     "critical"
    ],
    "description": "Vocabulary listed under Risk Levels."
   },
   "signalType": {
    "type": "string",
    "enum": [
     "excessiveRedemptionVelocity",
     "repeatedFailedAttempts",
     "multipleCustomersUsingCustomerSpecificCode",
     "unusualGeographicUsage",
     "highVolumeRedemptionFromOneDevice",
     "suspiciousPosOperatorActivity",
     "codeEnumerationAttempts",
     "partnerCodeLeakage",
     "redemptionAboveExpectedCampaignPattern"
    ],
    "description": "The fraud signal monitored."
   },
   "codeId": {
    "type": "string",
    "description": "Code or batch ID"
   },
   "detectedAt": {
    "type": "string",
    "format": "date-time",
    "description": "When detected"
   },
   "details": {
    "type": "string",
    "description": "What was observed"
   }
  }
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
 "CouponPromoCodeBuilderInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Coupon & Promo Code Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "codeType": {
    "type": "string",
    "enum": [
     "commonPromoCode",
     "uniquePromoCode",
     "coupon",
     "promotionalVoucher",
     "freeTicketCode",
     "discountVoucher",
     "partnerCode",
     "employeeCode",
     "influencerAffiliateCode",
     "compensationServiceRecoveryCode",
     "bulkCampaignCode"
    ],
    "description": "Kind of code."
   },
   "benefitType": {
    "type": "string",
    "enum": [
     "percentageDiscount",
     "fixedValueDiscount",
     "fixedPromotionalPrice",
     "freeProduct",
     "freeTicket",
     "freeAddOn",
     "upgrade",
     "bundleBenefit",
     "addedValue"
    ],
    "description": "What the code grants; the discount itself is calculated by the promotion rule engine rather than duplicated here."
   },
   "benefitValue": {
    "type": "number",
    "description": "Benefit value: the percentage, or the amount in the promotion's currency"
   },
   "campaign": {
    "type": "string",
    "description": "Campaign"
   },
   "code": {
    "type": "string",
    "description": "Code text for a common code, or the batch pattern for unique codes"
   },
   "maximumDiscount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Maximum discount"
   },
   "eligibleProducts": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Eligible products"
   },
   "channels": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Channels the code works on"
   },
   "validFrom": {
    "type": "string",
    "format": "date-time",
    "description": "Valid from"
   },
   "validTo": {
    "type": "string",
    "format": "date-time",
    "description": "Valid to"
   }
  }
 },
 "CouponPromoCodeBuilderView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Coupon & Promo Code Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "codeType": {
    "type": "string",
    "enum": [
     "commonPromoCode",
     "uniquePromoCode",
     "coupon",
     "promotionalVoucher",
     "freeTicketCode",
     "discountVoucher",
     "partnerCode",
     "employeeCode",
     "influencerAffiliateCode",
     "compensationServiceRecoveryCode",
     "bulkCampaignCode"
    ],
    "description": "Kind of code."
   },
   "benefitType": {
    "type": "string",
    "enum": [
     "percentageDiscount",
     "fixedValueDiscount",
     "fixedPromotionalPrice",
     "freeProduct",
     "freeTicket",
     "freeAddOn",
     "upgrade",
     "bundleBenefit",
     "addedValue"
    ],
    "description": "What the code grants; the discount itself is calculated by the promotion rule engine rather than duplicated here."
   },
   "benefitValue": {
    "type": "number",
    "description": "Benefit value: the percentage, or the amount in the promotion's currency"
   },
   "campaign": {
    "type": "string",
    "description": "Campaign"
   },
   "code": {
    "type": "string",
    "description": "Code text for a common code, or the batch pattern for unique codes"
   },
   "maximumDiscount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Maximum discount"
   },
   "eligibleProducts": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Eligible products"
   },
   "channels": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Channels the code works on"
   },
   "validFrom": {
    "type": "string",
    "format": "date-time",
    "description": "Valid from"
   },
   "validTo": {
    "type": "string",
    "format": "date-time",
    "description": "Valid to"
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
   },
   "rewardVariantIds": {
    "type": "array",
    "nullable": true,
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "The reward products, where the reward is not the qualifying product: the free gift of `freeItem`, the \"different product\" of a `buyXGetY` (setGiftFreeProduct, setBuyGetBogo). Absent means the reward is taken from the qualifying lines. (DM5, 29 September: data model for the agreed operations)"
   },
   "maxApplicationsPerBasket": {
    "type": "integer",
    "minimum": 1,
    "nullable": true,
    "description": "How many times the offer repeats in one basket: the \"maximum repetitions\" of an N-for-X offer (setFixedPriceOffer). Null repeats for every complete set. (DM5, 29 September: data model for the agreed operations)"
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
 "RedemptionAnalyticsAuditAiOptimizationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Redemption Analytics, Audit & AI Optimization displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "codesGenerated": {
    "type": "string",
    "description": "Codes generated"
   },
   "codesDistributed": {
    "type": "string",
    "description": "Codes distributed"
   },
   "codesRedeemed": {
    "type": "string",
    "description": "Codes redeemed"
   },
   "redemptionRate": {
    "type": "number",
    "description": "Redemption rate"
   },
   "conversionRate": {
    "type": "number",
    "description": "Conversion rate"
   },
   "revenueGenerated": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue generated"
   },
   "discountGranted": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Discount granted"
   },
   "incrementalRevenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Incremental revenue"
   },
   "aovUplift": {
    "type": "number",
    "description": "AOV uplift"
   },
   "costPerRedemption": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Cost per redemption"
   },
   "marginImpact": {
    "type": "number",
    "description": "Margin impact"
   },
   "expiredUnusedCodes": {
    "type": "integer",
    "description": "Expired unused codes"
   },
   "user": {
    "type": "string",
    "description": "User"
   },
   "timestamp": {
    "type": "string",
    "format": "date-time",
    "description": "Timestamp"
   },
   "previousValue": {
    "type": "string",
    "description": "Previous value"
   },
   "newValue": {
    "type": "integer",
    "description": "New value"
   },
   "reason": {
    "type": "string",
    "description": "Reason"
   },
   "approvalReference": {
    "type": "string",
    "description": "Approval reference"
   },
   "auditEvent": {
    "type": "string",
    "enum": [
     "created",
     "modified",
     "assigned",
     "suspended",
     "reactivated",
     "cancelled"
    ],
    "description": "Code audit event."
   }
  }
 },
 "RedemptionMonitorCodeLookupView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Redemption Monitor & Code Lookup displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "promoCode": {
    "type": "string",
    "description": "Promo code"
   },
   "code": {
    "type": "string",
    "description": "Code"
   },
   "redemptionDate": {
    "type": "string",
    "format": "date-time",
    "description": "Redemption date"
   },
   "redemptionTime": {
    "type": "string",
    "format": "date-time",
    "description": "Redemption time"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "originalValue": {
    "type": "string",
    "description": "Original value"
   },
   "discount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Discount"
   },
   "finalValue": {
    "type": "string",
    "description": "Final value"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "devicePos": {
    "type": "integer",
    "description": "Device/POS"
   },
   "operator": {
    "type": "string",
    "description": "Operator"
   },
   "validationResult": {
    "type": "string",
    "enum": [
     "valid",
     "redeemed",
     "expired",
     "notStarted",
     "usageLimitReached",
     "invalidProduct",
     "invalidChannel",
     "invalidLocation",
     "invalidCustomer",
     "suspended",
     "cancelled"
    ],
    "description": "Validation result of the redemption attempt"
   }
  }
 },
 "UniqueCodeGenerationBatchManagerView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Unique Code Generation & Batch Manager displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "campaign": {
    "type": "string",
    "description": "Campaign"
   },
   "numberOfCodes": {
    "type": "integer",
    "description": "Number of codes"
   },
   "codeLength": {
    "type": "string",
    "description": "Code length"
   },
   "prefix": {
    "type": "string",
    "description": "Prefix"
   },
   "suffix": {
    "type": "string",
    "description": "Suffix"
   },
   "characterType": {
    "type": "string",
    "description": "Character type"
   },
   "caseSensitivity": {
    "type": "string",
    "description": "Case sensitivity"
   },
   "expiration": {
    "type": "string",
    "description": "Expiration"
   },
   "numberOfUses": {
    "type": "integer",
    "description": "Number of uses"
   },
   "distributionOwner": {
    "type": "string",
    "description": "Distribution owner"
   },
   "batchId": {
    "type": "string",
    "description": "Batch ID"
   },
   "quantityGenerated": {
    "type": "integer",
    "description": "Quantity generated"
   },
   "generatedBy": {
    "type": "string",
    "description": "Generated by"
   },
   "generationDate": {
    "type": "string",
    "format": "date-time",
    "description": "Generation date"
   },
   "expiry": {
    "type": "string",
    "format": "date-time",
    "description": "Expiry"
   },
   "assignedPartner": {
    "type": "string",
    "description": "Assigned partner"
   },
   "distributionStatus": {
    "type": "string",
    "description": "Distribution status"
   },
   "redeemedQuantity": {
    "type": "integer",
    "description": "Redeemed quantity"
   },
   "remainingQuantity": {
    "type": "integer",
    "description": "Remaining quantity"
   }
  }
 },
 "UsageCapacityFrequencyControlView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Usage, Capacity & Frequency Control displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "maximumTotalRedemptions": {
    "type": "string",
    "description": "Maximum total redemptions"
   },
   "maximumPerCustomer": {
    "type": "string",
    "description": "Maximum per customer"
   },
   "maximumPerAccount": {
    "type": "string",
    "description": "Maximum per account"
   },
   "maximumPerTransaction": {
    "type": "string",
    "description": "Maximum per transaction"
   },
   "maximumPerDay": {
    "type": "string",
    "description": "Maximum per day"
   },
   "maximumPerChannel": {
    "type": "string",
    "description": "Maximum per channel"
   },
   "maximumPerVenue": {
    "type": "string",
    "description": "Maximum per venue"
   },
   "usageType": {
    "type": "string",
    "enum": [
     "singleUse",
     "multipleUse",
     "unlimitedUse"
    ],
    "description": "How often one code may be used."
   },
   "issued": {
    "type": "integer",
    "description": "Codes issued"
   },
   "redeemed": {
    "type": "integer",
    "description": "Codes redeemed"
   },
   "reservedPending": {
    "type": "integer",
    "description": "Codes reserved or pending"
   },
   "remaining": {
    "type": "integer",
    "description": "Codes remaining"
   }
  }
 },
 "ValidityDateTimeControlView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Validity, Date & Time Control displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "blackoutDates": {
    "type": "string",
    "description": "Blackout dates"
   },
   "holidays": {
    "type": "string",
    "description": "Holidays"
   },
   "selectedTimeslots": {
    "type": "string",
    "description": "Selected timeslots"
   },
   "selectedEvents": {
    "type": "string",
    "description": "Selected events"
   },
   "seasonalCalendars": {
    "type": "string",
    "description": "Seasonal calendars"
   },
   "expirationGracePeriod": {
    "type": "string",
    "format": "date-time",
    "description": "Expiration grace period"
   }
  }
 }
}
```
