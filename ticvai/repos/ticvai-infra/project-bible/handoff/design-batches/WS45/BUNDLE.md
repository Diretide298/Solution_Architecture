# WS45 — Promotions   Bundles Management board 1

**10 screens · 11 operations · 14 schemas · 3 permissions**

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

- **Every control that can be refused must be gated.** 3 permissions apply here:
  `APPROVAL_DECIDE, APPROVAL_VIEW, PRICE_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **1 of these operations work offline**: listPromotions
  — and the rest do not. A surface that looks the same online and off is lying.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-138` | Promotion Command Center Dashboard | commandCentre | 2 | 0 | — |
| `ADM-139` | Promotion & Campaign Directory | listDetail | 1 | 0 | — |
| `ADM-140` | Promotion Overview | listDetail | 1 | 0 | — |
| `ADM-141` | Promotion Lifecycle & Status Manager | listDetail | 1 | 0 | — |
| `ADM-142` | Campaign Calendar & Timeline | listDetail | 1 | 0 | — |
| `ADM-143` | Promotion Channel & Publication Monitor | commandCentre | 1 | 1 | — |
| `ADM-144` | Promotion Alerts & Exception Center | configEditor | 1 | 1 | — |
| `ADM-145` | Promotion Approval Inbox | approvalInbox | 3 | 1 | — |
| `ADM-146` | Promotion Health & Performance Monitor | commandCentre | 1 | 0 | — |
| `ADM-147` | Promotion Audit, Activity & Version History | listDetail | 1 | 0 | — |

## Thin screens in this batch

**ADM-140, ADM-141, ADM-142, ADM-147 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-138",
  "name": "Promotion Command Center Dashboard",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "1",
   "number": "1",
   "page": 6
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/promotion-command-center-dashboard-adm-138",
   "component": "apps/ticvai-web/src/routes/commercial/PromotionCommandCenterDashboard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-139",
    "ADM-140",
    "ADM-141",
    "ADM-142",
    "ADM-143",
    "ADM-144",
    "ADM-145",
    "ADM-146",
    "ADM-147"
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
     "to": "ADM-145",
     "trigger": "Promotion Approval Inbox",
     "carries": [
      "requestId"
     ],
     "provenance": "derived — ADM-145 declares entryState.params requestId, so an edge into it must carry them"
    },
    {
     "to": "ADM-139",
     "trigger": "Works in Promotion & Campaign Directory",
     "provenance": "flow F154 step 1→2"
    },
    {
     "to": "ADM-140",
     "trigger": "Works in Promotion Overview",
     "provenance": "flow F154 step 3→4",
     "operation": "listPromotions"
    },
    {
     "to": "ADM-141",
     "trigger": "Works in Promotion Lifecycle & Status Manager",
     "provenance": "flow F154 step 5→6",
     "operation": "listPromotions"
    },
    {
     "to": "ADM-142",
     "trigger": "Works in Campaign Calendar & Timeline",
     "provenance": "flow F154 step 7→8",
     "operation": "listPromotions"
    },
    {
     "to": "ADM-143",
     "trigger": "Works in Promotion Channel & Publication Monitor",
     "provenance": "flow F154 step 9→10",
     "operation": "listPromotions"
    },
    {
     "to": "ADM-144",
     "trigger": "Works in Promotion Alerts & Exception Center",
     "provenance": "flow F154 step 11→12",
     "operation": "listPromotions"
    },
    {
     "to": "ADM-146",
     "trigger": "Works in Promotion Health & Performance Monitor",
     "provenance": "flow F154 step 15→16",
     "operation": "listPromotions"
    },
    {
     "to": "ADM-147",
     "trigger": "Works in Promotion Audit, Activity & Version History",
     "provenance": "flow F154 step 17→18",
     "operation": "listPromotions"
    }
   ]
  },
  "notes": "**Given its section's own operations on 4 September.** It sat on `getVenueSettings` alone, which made it identical to every other section landing page — a hub that shows nothing of its section is a menu item, not a screen.",
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Global KPI cards) and a per-row directory (§Dashboard Visualizations) — counts over a population, then the population",
  "purpose": "Provide management with a real-time executive and operational overview of all promotional activities.",
  "gaps": [
   {
    "operation": "listPromotions",
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 6 §Dashboard Visualizations"
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
       "label": "Active Promotions",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 6 §Global KPI cards"
      },
      {
       "kind": "metricTile",
       "label": "Upcoming Promotions",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 6 §Global KPI cards"
      },
      {
       "kind": "metricTile",
       "label": "Draft Promotions",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 6 §Global KPI cards"
      },
      {
       "kind": "metricTile",
       "label": "Pending Approval",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 6 §Global KPI cards"
      },
      {
       "kind": "metricTile",
       "label": "Suspended Promotions",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 6 §Global KPI cards"
      },
      {
       "kind": "metricTile",
       "label": "Promotions Ending Soon",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 6 §Global KPI cards"
      },
      {
       "kind": "metricTile",
       "label": "Total Promotion Revenue",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 6 §Global KPI cards"
      },
      {
       "kind": "metricTile",
       "label": "Total Discount Granted",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 6 §Global KPI cards"
      },
      {
       "kind": "metricTile",
       "label": "Incremental Revenue",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 6 §Global KPI cards"
      },
      {
       "kind": "metricTile",
       "label": "Promotion Conversion Rate",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 6 §Global KPI cards"
      },
      {
       "kind": "metricTile",
       "label": "Redemption Rate",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 6 §Global KPI cards"
      },
      {
       "kind": "metricTile",
       "label": "Average Order Value Uplift",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 6 §Global KPI cards"
      },
      {
       "kind": "metricTile",
       "label": "Promotion Cost",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 6 §Global KPI cards"
      },
      {
       "kind": "metricTile",
       "label": "Estimated Margin Impact",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 6 §Global KPI cards"
      },
      {
       "kind": "metricTile",
       "label": "Campaign Budget Utilization",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 6 §Global KPI cards"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every promotion",
       "columns": [
        "Promotion revenue trend",
        "Discount exposure trend",
        "Conversion uplift",
        "Promotions by channel",
        "Promotions by venue",
        "Promotions by product",
        "Campaign budget consumption",
        "Top-performing promotions",
        "Underperforming promotions"
       ],
       "bindsTo": "Promotion",
       "operation": "listPromotions",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 6 §Dashboard Visualizations"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected promotion",
       "bindsTo": "Promotion",
       "columns": [
        "Promotion revenue trend",
        "Discount exposure trend",
        "Conversion uplift",
        "Promotions by channel",
        "Promotions by venue",
        "Promotions by product",
        "Campaign budget consumption",
        "Top-performing promotions",
        "Underperforming promotions"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Break down current promotions by”.",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 6 §Dashboard Visualizations"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The promotion list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the promotion untouched.",
   "emptyFirstRun": "No promotion yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the promotion are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPromotions",
    "contract": "promotions",
    "purpose": "List promotions",
    "trigger": "onLoad"
   },
   {
    "operationId": "getPromotionUsage",
    "contract": "promotions",
    "purpose": "Redemption and spend against a promotion",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "promotionId",
     "from": "navigation"
    }
   ],
   "coldEntry": "**Reached from the list that owns it**, so the identifier arrives with the navigation. Opened cold without one the screen says what is missing and offers that list.",
   "preloaded": [
    "Active Promotions",
    "Upcoming Promotions",
    "Draft Promotions",
    "Pending Approval",
    "Suspended Promotions",
    "Promotions Ending Soon"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-138"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 6. 0 of 9 labels bound to a contract property; 24 of 56 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-139",
  "name": "Promotion & Campaign Directory",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "1",
   "number": "2",
   "page": 8
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/promotion-campaign-directory-adm-139",
   "component": "apps/ticvai-web/src/routes/commercial/PromotionCampaignDirectory.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-138"
   ],
   "exitTo": [
    "ADM-138"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-138, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-138",
     "trigger": "Promotion Command Center Dashboard",
     "carries": [
      "promotionId"
     ],
     "provenance": "derived — ADM-138 declares entryState.params promotionId, so an edge into it must carry them"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Table Columns) and no metric row",
  "purpose": "Provide the master searchable list of every promotion and commercial campaign created within TICVAI.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search promotion campaign",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 8 §Allow filtering by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "PromotionCampaignDirectoryView.promotionType",
        "PromotionCampaignDirectoryView.campaign",
        "PromotionCampaignDirectoryView.product",
        "PromotionCampaignDirectoryView.productCategory",
        "PromotionCampaignDirectoryView.venue",
        "PromotionCampaignDirectoryView.attraction",
        "PromotionCampaignDirectoryView.event",
        "PromotionCampaignDirectoryView.fB",
        "PromotionCampaignDirectoryView.retail",
        "PromotionCampaignDirectoryView.membership",
        "PromotionCampaignDirectoryView.channel",
        "PromotionCampaignDirectoryView.partner",
        "PromotionCampaignDirectoryView.customerSegment",
        "PromotionCampaignDirectoryView.date",
        "PromotionCampaignDirectoryView.status",
        "PromotionCampaignDirectoryView.owner",
        "PromotionCampaignDirectoryView.approvalState",
        "PromotionCampaignDirectoryView.promotionValue",
        "PromotionCampaignDirectoryView.budgetStatus"
       ],
       "notes": "The pack filters this screen by promotion type, campaign, product, product category, venue, attraction and 13 more — which are present is a decision the pack already made.",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 8 §Allow filtering by"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every promotion campaign",
       "columns": [
        "PromotionCampaignDirectoryView.promotionId",
        "PromotionCampaignDirectoryView.promotionName",
        "PromotionCampaignDirectoryView.promotionType",
        "PromotionCampaignDirectoryView.campaign",
        "PromotionCampaignDirectoryView.status",
        "PromotionCampaignDirectoryView.businessEntity",
        "PromotionCampaignDirectoryView.venue",
        "PromotionCampaignDirectoryView.product",
        "PromotionCampaignDirectoryView.targetSegment",
        "PromotionCampaignDirectoryView.channel",
        "PromotionCampaignDirectoryView.startDate",
        "PromotionCampaignDirectoryView.endDate",
        "PromotionCampaignDirectoryView.discountType",
        "PromotionCampaignDirectoryView.discountValue",
        "PromotionCampaignDirectoryView.budget",
        "PromotionCampaignDirectoryView.redemptionCount",
        "PromotionCampaignDirectoryView.revenueGenerated",
        "PromotionCampaignDirectoryView.owner",
        "PromotionCampaignDirectoryView.approvalStatus",
        "PromotionCampaignDirectoryView.version",
        "PromotionCampaignDirectoryView.lastModified"
       ],
       "bindsTo": "PromotionCampaignDirectoryView",
       "operation": "listPromotionCampaign",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 8 §Table Columns"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected promotion campaign",
       "bindsTo": "PromotionCampaignDirectoryView",
       "columns": [
        "PromotionCampaignDirectoryView.promotionId",
        "PromotionCampaignDirectoryView.promotionName",
        "PromotionCampaignDirectoryView.promotionType",
        "PromotionCampaignDirectoryView.campaign",
        "PromotionCampaignDirectoryView.status",
        "PromotionCampaignDirectoryView.businessEntity",
        "PromotionCampaignDirectoryView.venue",
        "PromotionCampaignDirectoryView.product",
        "PromotionCampaignDirectoryView.targetSegment",
        "PromotionCampaignDirectoryView.channel",
        "PromotionCampaignDirectoryView.startDate",
        "PromotionCampaignDirectoryView.endDate",
        "PromotionCampaignDirectoryView.discountType",
        "PromotionCampaignDirectoryView.discountValue",
        "PromotionCampaignDirectoryView.budget",
        "PromotionCampaignDirectoryView.redemptionCount",
        "PromotionCampaignDirectoryView.revenueGenerated",
        "PromotionCampaignDirectoryView.owner",
        "PromotionCampaignDirectoryView.approvalStatus",
        "PromotionCampaignDirectoryView.version",
        "PromotionCampaignDirectoryView.lastModified"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Supported Statuses”.",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 8 §Table Columns"
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
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** Activate, Pause, Extend, Duplicate, Archive, Export, Assign owner, Submit for approval. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 8 §Authorized users may"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The promotion campaign list.",
   "error": "Could not load. Names which read failed and leaves the promotion campaign untouched.",
   "emptyFirstRun": "No promotion campaign yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the promotion campaign are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPromotionCampaign",
    "contract": "promotions",
    "purpose": "Promotion & Campaign Directory",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "PromotionCampaignDirectoryView.promotionId",
    "PromotionCampaignDirectoryView.promotionName",
    "PromotionCampaignDirectoryView.promotionType",
    "PromotionCampaignDirectoryView.campaign",
    "PromotionCampaignDirectoryView.status",
    "PromotionCampaignDirectoryView.businessEntity"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-139"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 8. 40 of 40 labels bound to a contract property; 48 of 63 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-140",
  "name": "Promotion Overview",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "1",
   "number": "3",
   "page": 9
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/promotion-overview-adm-140",
   "component": "apps/ticvai-web/src/routes/commercial/PromotionOverview.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-138"
   ],
   "exitTo": [
    "ADM-138"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-138, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-138",
     "trigger": "Promotion Command Center Dashboard",
     "carries": [
      "promotionId"
     ],
     "provenance": "derived — ADM-138 declares entryState.params promotionId, so an edge into it must carry them"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display; Show) and no metric row",
  "purpose": "Provide the complete business summary of one selected promotion without opening its detailed configuration.",
  "gaps": [
   {
    "operation": "listPromotions",
    "why": "**This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape exists.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 9 §Display"
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
       "label": "Every promotion overview",
       "columns": [
        "Promotion name",
        "Promotion ID",
        "Version",
        "Status",
        "Owner",
        "Created by",
        "Effective dates",
        "Campaign",
        "Business entity",
        "Promotion mechanism",
        "Discount/reward",
        "Eligible products",
        "Eligible customers",
        "Eligible channels",
        "Eligible locations",
        "Applicable time/date conditions",
        "Usage limits",
        "Budget",
        "Redemption ceiling",
        "Promotion hierarchy",
        "Stacking behavior",
        "Approval state",
        "Transactions",
        "Redemptions",
        "Gross revenue",
        "Discount granted",
        "Net revenue",
        "Incremental revenue",
        "Conversion",
        "AOV impact",
        "Profit/margin impact",
        "Remaining budget"
       ],
       "bindsTo": "Promotion",
       "operation": "listPromotions",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 9 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected promotion overview",
       "bindsTo": "Promotion",
       "columns": [
        "Promotion name",
        "Promotion ID",
        "Version",
        "Status",
        "Owner",
        "Created by",
        "Effective dates",
        "Campaign",
        "Business entity",
        "Promotion mechanism",
        "Discount/reward",
        "Eligible products",
        "Eligible customers",
        "Eligible channels",
        "Eligible locations",
        "Applicable time/date conditions",
        "Usage limits",
        "Budget",
        "Redemption ceiling",
        "Promotion hierarchy",
        "Stacking behavior",
        "Approval state",
        "Transactions",
        "Redemptions",
        "Gross revenue",
        "Discount granted",
        "Net revenue",
        "Incremental revenue",
        "Conversion",
        "AOV impact",
        "Profit/margin impact",
        "Remaining budget"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Direct links to”.",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 9 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The promotion overview list.",
   "error": "Could not load. Names which read failed and leaves the promotion overview untouched.",
   "emptyFirstRun": "No promotion overview yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the promotion overview are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPromotions",
    "contract": "promotions",
    "purpose": "List promotions",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "Promotion name",
    "Promotion ID",
    "Version",
    "Status",
    "Owner",
    "Created by"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-140"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 9. 0 of 32 labels bound to a contract property; 32 of 44 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-141",
  "name": "Promotion Lifecycle & Status Manager",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "1",
   "number": "4",
   "page": 11
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/promotion-lifecycle-status-manager-adm-141",
   "component": "apps/ticvai-web/src/routes/commercial/PromotionLifecycleStatusManager.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-138"
   ],
   "exitTo": [
    "ADM-138"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-138, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-138",
     "trigger": "Promotion Command Center Dashboard",
     "carries": [
      "promotionId"
     ],
     "provenance": "derived — ADM-138 declares entryState.params promotionId, so an edge into it must carry them"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Control the operational lifecycle of promotions.",
  "gaps": [
   {
    "operation": null,
    "why": "**Promotion Lifecycle & Status Manager declares no operation that writes anything** — its only declared call is `listPromotionLifecycleStatus`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 11"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 11"
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
       "kind": "banner",
       "label": "Permissions this screen separates",
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** Save Draft, Validate, Submit for Simulation, Submit for Approval, Approve, Reject, Schedule, Activate, Pause, Resume, Suspend, Extend, Terminate, Archive. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 11 §Depending on user permissions"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listPromotionLifecycleStatus",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The promotion lifecycle status list.",
   "error": "Could not load. Names which read failed and leaves the promotion lifecycle status untouched.",
   "emptyFirstRun": "No promotion lifecycle status yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the promotion lifecycle status are still there. The pack's own statuses are Paused/Suspended → Expired → Archived — the state names which is selected.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPromotionLifecycleStatus",
    "contract": "promotions",
    "purpose": "Promotion Lifecycle & Status Manager",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "PromotionLifecycleStatusManagerView.pausedSuspendedExpiredArchived",
    "PromotionLifecycleStatusManagerView.terminate",
    "PromotionLifecycleStatusManagerView.requiredConfigurationIsCompleted",
    "PromotionLifecycleStatusManagerView.validProductsExist",
    "PromotionLifecycleStatusManagerView.datesAreValid"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-141"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 11. 0 of 0 labels bound to a contract property; 15 of 34 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-142",
  "name": "Campaign Calendar & Timeline",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "1",
   "number": "5",
   "page": 12
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/campaign-calendar-timeline-adm-142",
   "component": "apps/ticvai-web/src/routes/commercial/CampaignCalendarTimeline.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-138"
   ],
   "exitTo": [
    "ADM-138"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-138, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-138",
     "trigger": "Promotion Command Center Dashboard",
     "carries": [
      "promotionId"
     ],
     "provenance": "derived — ADM-138 declares entryState.params promotionId, so an edge into it must carry them"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Identify) and no metric row",
  "purpose": "Provide a calendar-based operational view of promotions.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every campaign calendar timeline",
       "columns": [
        "CampaignCalendarTimelineView.active",
        "CampaignCalendarTimelineView.upcoming",
        "CampaignCalendarTimelineView.endingSoon",
        "CampaignCalendarTimelineView.expired",
        "CampaignCalendarTimelineView.pendingApproval",
        "CampaignCalendarTimelineView.conflicting",
        "CampaignCalendarTimelineView.suspended"
       ],
       "bindsTo": "CampaignCalendarTimelineView",
       "operation": "listCampaignCalendarTimeline",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 12 §Identify"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected campaign calendar timeline",
       "bindsTo": "CampaignCalendarTimelineView",
       "columns": [
        "CampaignCalendarTimelineView.active",
        "CampaignCalendarTimelineView.upcoming",
        "CampaignCalendarTimelineView.endingSoon",
        "CampaignCalendarTimelineView.expired",
        "CampaignCalendarTimelineView.pendingApproval",
        "CampaignCalendarTimelineView.conflicting",
        "CampaignCalendarTimelineView.suspended"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Views”, “Show promotions by”, “Users may”, “Conflict Detection”.",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 12 §Identify"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The campaign calendar timeline list.",
   "error": "Could not load. Names which read failed and leaves the campaign calendar timeline untouched.",
   "emptyFirstRun": "No campaign calendar timeline yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the campaign calendar timeline are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCampaignCalendarTimeline",
    "contract": "promotions",
    "purpose": "Campaign Calendar & Timeline",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "CampaignCalendarTimelineView.active",
    "CampaignCalendarTimelineView.upcoming",
    "CampaignCalendarTimelineView.endingSoon",
    "CampaignCalendarTimelineView.expired",
    "CampaignCalendarTimelineView.pendingApproval",
    "CampaignCalendarTimelineView.conflicting"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-142"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 12. 7 of 7 labels bound to a contract property; 7 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-143",
  "name": "Promotion Channel & Publication Monitor",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "1",
   "number": "6",
   "page": 13
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/promotion-channel-publication-monitor-adm-143",
   "component": "apps/ticvai-web/src/routes/commercial/PromotionChannelPublicationMonitor.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-138"
   ],
   "exitTo": [
    "ADM-138"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-138, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-138",
     "trigger": "Promotion Command Center Dashboard",
     "carries": [
      "promotionId"
     ],
     "provenance": "derived — ADM-138 declares entryState.params promotionId, so an edge into it must carry them"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Show) and a per-row directory (§For each channel display) — counts over a population, then the population",
  "purpose": "Ensure promotional configurations are correctly synchronized across every TICVAI sales channel.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 5 actions on this screen and the screen declares 1 operation.** Unserved: Publish, Republish, Disable channel, Compare configurations, View synchronization log. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 13 §Actions"
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
       "label": "Promotion version",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 13 §Show",
       "bindsTo": "PromotionChannelPublicationMonitorView.promotionVersion"
      },
      {
       "kind": "metricTile",
       "label": "Last synchronized",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 13 §Show",
       "bindsTo": "PromotionChannelPublicationMonitorView.lastSynchronized"
      },
      {
       "kind": "metricTile",
       "label": "Rules published",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 13 §Show",
       "bindsTo": "PromotionChannelPublicationMonitorView.rulesPublished"
      },
      {
       "kind": "metricTile",
       "label": "Products published",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 13 §Show",
       "bindsTo": "PromotionChannelPublicationMonitorView.productsPublished"
      },
      {
       "kind": "metricTile",
       "label": "Code availability",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 13 §Show",
       "bindsTo": "PromotionChannelPublicationMonitorView.codeAvailability"
      },
      {
       "kind": "metricTile",
       "label": "Channel restrictions",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 13 §Show",
       "bindsTo": "PromotionChannelPublicationMonitorView.channelRestrictions"
      },
      {
       "kind": "metricTile",
       "label": "Error messages",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 13 §Show",
       "bindsTo": "PromotionChannelPublicationMonitorView.errorMessages"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every promotion channel publication",
       "columns": [
        "PromotionChannelPublicationMonitorView.notAssigned",
        "PromotionChannelPublicationMonitorView.pendingPublication",
        "PromotionChannelPublicationMonitorView.published",
        "PromotionChannelPublicationMonitorView.synchronizing",
        "PromotionChannelPublicationMonitorView.publicationFailed",
        "PromotionChannelPublicationMonitorView.outOfSync",
        "PromotionChannelPublicationMonitorView.suspended"
       ],
       "bindsTo": "PromotionChannelPublicationMonitorView",
       "operation": "listPromotionChannel",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 13 §For each channel display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected promotion channel publication",
       "bindsTo": "PromotionChannelPublicationMonitorView",
       "columns": [
        "PromotionChannelPublicationMonitorView.notAssigned",
        "PromotionChannelPublicationMonitorView.pendingPublication",
        "PromotionChannelPublicationMonitorView.published",
        "PromotionChannelPublicationMonitorView.synchronizing",
        "PromotionChannelPublicationMonitorView.publicationFailed",
        "PromotionChannelPublicationMonitorView.outOfSync",
        "PromotionChannelPublicationMonitorView.suspended"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Supported Channels”.",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 13 §For each channel display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Publish",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 13 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Republish",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 13 §Actions"
      },
      {
       "kind": "destructiveButton",
       "label": "Disable channel",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 13 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Compare configurations",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 13 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "View synchronization log",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 13 §Actions"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmDisableChannel",
    "component": "confirmDialog",
    "trigger": "Disable channel",
    "body": "**Disable channel on a promotion channel publication is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 13 §Actions"
   }
  ],
  "states": {
   "loading": "The promotion channel publication list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the promotion channel publication untouched.",
   "emptyFirstRun": "No promotion channel publication yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the promotion channel publication are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPromotionChannel",
    "contract": "promotions",
    "purpose": "Promotion Channel & Publication Monitor",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-143"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 13. 14 of 14 labels bound to a contract property; 19 of 37 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-144",
  "name": "Promotion Alerts & Exception Center",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "1",
   "number": "7",
   "page": 14
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/promotion-alerts-exception-center-adm-144",
   "component": "apps/ticvai-web/src/routes/commercial/PromotionAlertsExceptionCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-138"
   ],
   "exitTo": [
    "ADM-138"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-138, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-138",
     "trigger": "Promotion Command Center Dashboard",
     "carries": [
      "promotionId"
     ],
     "provenance": "derived — ADM-138 declares entryState.params promotionId, so an edge into it must carry them"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configuration) and no display directory — it is settings, not a population",
  "purpose": "Centralize operational, commercial, and financial alerts affecting promotions.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 3 actions on this screen and the screen declares 1 operation.** Unserved: Assign alert, Suspend campaign, Open related configuration. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 14 §Users can"
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
       "label": "Missing product",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 14 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Missing eligibility",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 14 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Invalid dates",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 14 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Invalid discount",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 14 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Invalid code",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 14 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Missing approval",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 14 §Configuration"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Assign alert",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 14 §Users can"
      },
      {
       "kind": "destructiveButton",
       "label": "Suspend campaign",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 14 §Users can"
      },
      {
       "kind": "secondaryButton",
       "label": "Open related configuration",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 14 §Users can"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmSuspendCampaign",
    "component": "confirmDialog",
    "trigger": "Suspend campaign",
    "body": "**Suspend campaign on a promotion alerts exception is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 14 §Users can"
   }
  ],
  "states": {
   "loading": "The promotion alerts exception configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the promotion alerts exception untouched.",
   "emptyFirstRun": "No promotion alerts exception configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPromotionAlertException",
    "contract": "promotions",
    "purpose": "Promotion Alerts & Exception Center",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-144"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 14. 0 of 0 labels bound to a contract property; 9 of 32 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-145",
  "name": "Promotion Approval Inbox",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "1",
   "number": "8",
   "page": 15
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/promotion-approval-inbox-adm-145",
   "component": "apps/ticvai-web/src/routes/commercial/PromotionApprovalInbox.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-138"
   ],
   "exitTo": [
    "ADM-138"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-138, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-138",
     "trigger": "Promotion Command Center Dashboard",
     "carries": [
      "promotionId"
     ],
     "provenance": "derived — ADM-138 declares entryState.params promotionId, so an edge into it must carry them"
    }
   ]
  },
  "density": "compact",
  "pattern": "approvalInbox",
  "patternReason": "the pack lists Approve and Reject among this screen's own actions — every row is waiting for a decision, so the empty state is success rather than a prompt to create something",
  "purpose": "Provide one centralized approval workspace for promotional changes.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 5 actions on this screen and the screen declares 3 operations.** Unserved: Approve, Reject, Return for Change, Delegate. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 15 §Actions"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "queue",
     "components": [
      {
       "kind": "dataTable",
       "label": "Waiting for a decision",
       "columns": [
        "Promotion",
        "Request type",
        "Requested by",
        "Requested date",
        "Discount exposure",
        "Revenue impact estimate",
        "Margin impact",
        "Campaign budget",
        "Risk level",
        "Requested activation date",
        "Current approval level"
       ],
       "bindsTo": "ApprovalRequest",
       "operation": "listApprovalRequests",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 15 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "item",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected promotion approval",
       "bindsTo": "ApprovalRequest",
       "columns": [
        "Promotion",
        "Request type",
        "Requested by",
        "Requested date",
        "Discount exposure",
        "Revenue impact estimate",
        "Margin impact",
        "Campaign budget",
        "Risk level",
        "Requested activation date",
        "Current approval level"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Approval can be required for”.",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 15 §Show"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "decision",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Approve",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 15 §Actions"
      },
      {
       "kind": "destructiveButton",
       "label": "Reject",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 15 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Return for Change",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 15 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Request Information",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 15 §Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Delegate",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 15 §Actions"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmReject",
    "component": "confirmDialog",
    "trigger": "Reject",
    "body": "**Reject on a promotion approval is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 15 §Actions"
   }
  ],
  "states": {
   "loading": "The promotion approval list.",
   "error": "Could not load. Names which read failed and leaves the promotion approval untouched.",
   "emptyFirstRun": "**Nothing is waiting, which is the good outcome.** An empty queue means every request has been decided — this state offers no create action, because creating work is not what an empty inbox needs.",
   "emptyNoResults": "The filter narrowed it and the promotion approval are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPromotions",
    "contract": "promotions",
    "purpose": "List promotions",
    "trigger": "onLoad"
   },
   {
    "operationId": "listApprovalRequests",
    "contract": "approvals",
    "purpose": "Promotions awaiting a decision",
    "trigger": "onLoad"
   },
   {
    "operationId": "decideApprovalRequest",
    "contract": "approvals",
    "purpose": "Approve or refuse one",
    "trigger": "onAction",
    "invalidates": [
     "listApprovalRequests"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "requestId",
     "from": "navigation"
    }
   ],
   "coldEntry": "**Reached from the list that owns it**, so the identifier arrives with the navigation. Opened cold without one the screen says what is missing and offers that list — never an empty form that looks configurable.",
   "preloaded": [
    "Promotion",
    "Request type",
    "Requested by",
    "Requested date",
    "Discount exposure",
    "Revenue impact estimate"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-145"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 15. 0 of 11 labels bound to a contract property; 16 of 31 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-146",
  "name": "Promotion Health & Performance Monitor",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "1",
   "number": "9",
   "page": 16
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/promotion-health-performance-monitor-adm-146",
   "component": "apps/ticvai-web/src/routes/commercial/PromotionHealthPerformanceMonitor.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-138"
   ],
   "exitTo": [
    "ADM-138"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-138, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-138",
     "trigger": "Promotion Command Center Dashboard",
     "carries": [
      "promotionId"
     ],
     "provenance": "derived — ADM-138 declares entryState.params promotionId, so an edge into it must carry them"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§KPIs; Compare) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Provide near-real-time operational performance monitoring while campaigns are running.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Impressions",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 16 §KPIs",
       "bindsTo": "PromotionHealthPerformanceMonitorView.impressions"
      },
      {
       "kind": "metricTile",
       "label": "Promotion views",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 16 §KPIs",
       "bindsTo": "PromotionHealthPerformanceMonitorView.promotionViews"
      },
      {
       "kind": "metricTile",
       "label": "Eligible transactions",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 16 §KPIs",
       "bindsTo": "PromotionHealthPerformanceMonitorView.eligibleTransactions"
      },
      {
       "kind": "metricTile",
       "label": "Promotion applications",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 16 §KPIs",
       "bindsTo": "PromotionHealthPerformanceMonitorView.promotionApplications"
      },
      {
       "kind": "metricTile",
       "label": "Redemptions",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 16 §KPIs",
       "bindsTo": "PromotionHealthPerformanceMonitorView.redemptions"
      },
      {
       "kind": "metricTile",
       "label": "Redemption rate",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 16 §KPIs",
       "bindsTo": "PromotionHealthPerformanceMonitorView.redemptionRate"
      },
      {
       "kind": "metricTile",
       "label": "Conversion rate",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 16 §KPIs",
       "bindsTo": "PromotionHealthPerformanceMonitorView.conversionRate"
      },
      {
       "kind": "metricTile",
       "label": "Gross sales",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 16 §KPIs",
       "bindsTo": "PromotionHealthPerformanceMonitorView.grossSales"
      },
      {
       "kind": "metricTile",
       "label": "Net sales",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 16 §KPIs",
       "bindsTo": "PromotionHealthPerformanceMonitorView.netSales"
      },
      {
       "kind": "metricTile",
       "label": "Discount granted",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 16 §KPIs",
       "bindsTo": "PromotionHealthPerformanceMonitorView.discountGranted"
      },
      {
       "kind": "metricTile",
       "label": "Incremental revenue",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 16 §KPIs",
       "bindsTo": "PromotionHealthPerformanceMonitorView.incrementalRevenue"
      },
      {
       "kind": "metricTile",
       "label": "AOV uplift",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 16 §KPIs",
       "bindsTo": "PromotionHealthPerformanceMonitorView.aovUplift"
      },
      {
       "kind": "metricTile",
       "label": "Margin",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 16 §KPIs",
       "bindsTo": "PromotionHealthPerformanceMonitorView.margin"
      },
      {
       "kind": "metricTile",
       "label": "Cost per redemption",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 16 §KPIs",
       "bindsTo": "PromotionHealthPerformanceMonitorView.costPerRedemption"
      },
      {
       "kind": "metricTile",
       "label": "Budget consumed",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 16 §KPIs",
       "bindsTo": "PromotionHealthPerformanceMonitorView.budgetConsumed"
      },
      {
       "kind": "metricTile",
       "label": "Budget remaining",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 16 §KPIs",
       "bindsTo": "PromotionHealthPerformanceMonitorView.budgetRemaining"
      },
      {
       "kind": "metricTile",
       "label": "Promotion vs baseline",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 16 §Compare",
       "bindsTo": "PromotionHealthPerformanceMonitorView.promotionVsBaseline"
      },
      {
       "kind": "metricTile",
       "label": "Promotion vs previous campaign",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 16 §Compare",
       "bindsTo": "PromotionHealthPerformanceMonitorView.promotionVsPreviousCampaign"
      },
      {
       "kind": "metricTile",
       "label": "Promotion vs AI forecast",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 16 §Compare",
       "bindsTo": "PromotionHealthPerformanceMonitorView.promotionVsAiForecast"
      },
      {
       "kind": "metricTile",
       "label": "Promotion vs control group",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 16 §Compare",
       "bindsTo": "PromotionHealthPerformanceMonitorView.promotionVsControlGroup"
      },
      {
       "kind": "metricTile",
       "label": "Channel vs channel",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 16 §Compare",
       "bindsTo": "PromotionHealthPerformanceMonitorView.channelVsChannel"
      },
      {
       "kind": "metricTile",
       "label": "Venue vs venue",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 16 §Compare",
       "bindsTo": "PromotionHealthPerformanceMonitorView.venueVsVenue"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The promotion health performance list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the promotion health performance untouched.",
   "emptyFirstRun": "No promotion health performance yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the promotion health performance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPromotionHealthPerformance",
    "contract": "promotions",
    "purpose": "Promotion Health & Performance Monitor",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "PromotionHealthPerformanceMonitorView.impressions",
    "PromotionHealthPerformanceMonitorView.promotionViews",
    "PromotionHealthPerformanceMonitorView.eligibleTransactions",
    "PromotionHealthPerformanceMonitorView.promotionApplications",
    "PromotionHealthPerformanceMonitorView.redemptions",
    "PromotionHealthPerformanceMonitorView.redemptionRate"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-146"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 16. 22 of 22 labels bound to a contract property; 22 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-147",
  "name": "Promotion Audit, Activity & Version History",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "1",
   "number": "10",
   "page": 17
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/promotion-audit-activity-version-history-adm-147",
   "component": "apps/ticvai-web/src/routes/commercial/PromotionAuditActivityVersionHistory.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-138"
   ],
   "exitTo": [
    "ADM-138"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-138, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-138",
     "trigger": "Promotion Command Center Dashboard",
     "carries": [
      "promotionId"
     ],
     "provenance": "derived — ADM-138 declares entryState.params promotionId, so an edge into it must carry them"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide complete governance and traceability for every promotion. Board 2 is the core commercial rule engine for promotions. It shall allow authorized TICVAI business users to configure discount and promotion mechanics without development, including percentage and fixed discounts, transaction thresholds, volume discounts, bulk pricing, early-bird and last-minute offers, special guest pricing, payment-method discounts, partner discounts, and dynamic conditional discounts. The matrix explicitly requires percentage/value discounts, quantity thresholds, bulk discounts, early-bird/volume/customer-segment conditions, payment-type offers, group pricing, and special individual pricing. The board should contain 10 backend screens.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 17"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 17"
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
       "kind": "banner",
       "label": "Permissions this screen separates",
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** View, Create, Edit, Submit, Approve, Activate, Pause, Suspend, Change budget, Archive, Export. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 17 §Roles & Permissions"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listPromotionActivityVersion",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The promotion audit activity list.",
   "error": "Could not load. Names which read failed and leaves the promotion audit activity untouched.",
   "emptyFirstRun": "No promotion audit activity yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the promotion audit activity are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPromotionActivityVersion",
    "contract": "promotions",
    "purpose": "Promotion Audit, Activity & Version History",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "PromotionAuditActivityVersionHistoryView.promotionCreated",
    "PromotionAuditActivityVersionHistoryView.promotionEdited",
    "PromotionAuditActivityVersionHistoryView.ruleChanged",
    "PromotionAuditActivityVersionHistoryView.discountChanged",
    "PromotionAuditActivityVersionHistoryView.productAdded"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-147"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 17. 0 of 0 labels bound to a contract property; 11 of 142 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "decideApprovalRequest": {
  "method": "POST",
  "path": "/approval-requests/{requestId}/decide",
  "contract": "approvals",
  "summary": "Approve or reject",
  "permission": "APPROVAL_DECIDE",
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
  "responds": "ApprovalRequest"
 },
 "getPromotionUsage": {
  "method": "GET",
  "path": "/promotions/{promotionId}/usage",
  "contract": "promotions",
  "summary": "Redemption count and discount given",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "PromotionUsage"
 },
 "listApprovalRequests": {
  "method": "GET",
  "path": "/approval-requests",
  "contract": "approvals",
  "summary": "Requests awaiting a decision, or already decided",
  "permission": "APPROVAL_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "assignedToMe",
    "in": "query",
    "required": null
   },
   {
    "name": "raisedByMe",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "kind",
    "in": "query",
    "required": null
   },
   {
    "name": "breachingWithinMinutes",
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
 "listCampaignCalendarTimeline": {
  "method": "GET",
  "path": "/campaign-calendar-timeline",
  "contract": "promotions",
  "summary": "Campaign Calendar & Timeline",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "CampaignCalendarTimelineView"
 },
 "listPromotionActivityVersion": {
  "method": "GET",
  "path": "/promotion-activity-version",
  "contract": "promotions",
  "summary": "Promotion Audit, Activity & Version History",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "PromotionAuditActivityVersionHistoryView"
 },
 "listPromotionAlertException": {
  "method": "GET",
  "path": "/promotion-alert-exception",
  "contract": "promotions",
  "summary": "Promotion Alerts & Exception Center",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "PromotionAlertsExceptionCenterView"
 },
 "listPromotionCampaign": {
  "method": "GET",
  "path": "/promotion-campaign",
  "contract": "promotions",
  "summary": "Promotion & Campaign Directory",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "PromotionCampaignDirectoryView"
 },
 "listPromotionChannel": {
  "method": "GET",
  "path": "/promotion-channel",
  "contract": "promotions",
  "summary": "Promotion Channel & Publication Monitor",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "PromotionChannelPublicationMonitorView"
 },
 "listPromotionHealthPerformance": {
  "method": "GET",
  "path": "/promotion-health-performance",
  "contract": "promotions",
  "summary": "Promotion Health & Performance Monitor",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "PromotionHealthPerformanceMonitorView"
 },
 "listPromotionLifecycleStatus": {
  "method": "GET",
  "path": "/promotion-lifecycle-statu",
  "contract": "promotions",
  "summary": "Promotion Lifecycle & Status Manager",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "PromotionLifecycleStatusManagerView"
 },
 "listPromotions": {
  "method": "GET",
  "path": "/promotions",
  "contract": "promotions",
  "summary": "List promotions",
  "permission": "PRICE_VIEW",
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
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "activeAt",
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
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "ApprovalDecision": {
  "type": "object",
  "x-ticvai-persistence": "approvals.decision",
  "required": [
   "level",
   "principalId",
   "decision",
   "decidedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "level": {
    "type": "integer"
   },
   "principalId": {
    "type": "string",
    "format": "uuid"
   },
   "displayName": {
    "type": "string"
   },
   "isDelegate": {
    "type": "boolean"
   },
   "delegatedFrom": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "decision": {
    "type": "string",
    "enum": [
     "approve",
     "reject"
    ]
   },
   "comment": {
    "type": "string",
    "nullable": true
   },
   "reason": {
    "type": "string",
    "nullable": true
   },
   "usedMfa": {
    "type": "boolean"
   },
   "signatureRef": {
    "type": "string",
    "nullable": true
   },
   "decidedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "ApprovalKind": {
  "type": "string",
  "description": "11.1.7 and 11.1.30–11.1.37. **The first four already exist as bespoke implementations** and this contract is what they collapse into.\n",
  "enum": [
   "refund",
   "priceOverride",
   "discountOverride",
   "complimentaryTicket",
   "membershipCancellation",
   "accessPermissionChange",
   "configurationChange",
   "aiRecommendation",
   "shiftVariance",
   "releasePromotion",
   "requisition",
   "stockWriteOff",
   "journalEntry",
   "periodReopen",
   "tenantMigration"
  ]
 },
 "ApprovalMode": {
  "type": "string",
  "description": "11.1.43–11.1.46. **Sequential** asks one at a time, **parallel** asks everyone at once, **consensus** needs all of them, **majority** needs more than half.\nParallel and consensus differ in when it completes: parallel completes on the first approval, consensus waits for all. Conflating them is how a four-eyes rule turns into a one-eye rule.\n",
  "enum": [
   "sequential",
   "parallel",
   "consensus",
   "majority"
  ]
 },
 "ApprovalRequest": {
  "type": "object",
  "x-ticvai-persistence": "approvals.request",
  "required": [
   "id",
   "kind",
   "status",
   "requestedByPrincipalId",
   "requestedAt"
  ],
  "properties": {
   "id": {
    "type": "string"
   },
   "kind": {
    "$ref": "#/components/schemas/ApprovalKind"
   },
   "rerouteOnNoApprover": {
    "type": "boolean",
    "default": true,
    "description": "BL-154. **An approver on leave is an approval that waits for them to come back.** Reroutes to the next in the chain rather than stalling — `workforce` already knows who is on leave, and an approval queue nobody is watching is the thing that stops a venue.\n"
   },
   "outOfOfficeDelegateId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "allowEmailApproval": {
    "type": "boolean",
    "default": false,
    "description": "**Approving from an email link with no second factor is the weakest path in the system**, so it is off by default and available only below a configured value.\n"
   },
   "reopenedFrom": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**Reopening a decided approval creates a new one that points back.** Editing a decision in place destroys the record of what was originally approved, which is the only thing an audit wants.\n"
   },
   "status": {
    "$ref": "#/components/schemas/ApprovalStatus"
   },
   "subjectContract": {
    "type": "string"
   },
   "subjectType": {
    "type": "string"
   },
   "subjectId": {
    "type": "string"
   },
   "scopePath": {
    "type": "string"
   },
   "summary": {
    "type": "string"
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "justification": {
    "type": "string",
    "nullable": true
   },
   "requestedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "matrixVersion": {
    "type": "integer"
   },
   "mode": {
    "$ref": "#/components/schemas/ApprovalMode"
   },
   "currentLevel": {
    "type": "integer"
   },
   "totalLevels": {
    "type": "integer"
   },
   "pendingApprovers": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "principalId": {
       "type": "string",
       "format": "uuid"
      },
      "displayName": {
       "type": "string"
      },
      "isDelegate": {
       "type": "boolean"
      }
     }
    }
   },
   "decisions": {
    "type": "array",
    "description": "Every decision at every level, in order. **Immutable once the request completes** (11.1.56) — an approval is evidence, and amending one is a different fact.\n",
    "items": {
     "$ref": "#/components/schemas/ApprovalDecision"
    }
   },
   "escalations": {
    "type": "array",
    "description": "11.1.48. Who was asked, when, and why it moved up. **Escalation adds an approver rather than replacing one**, so the original stays in the record.\n",
    "items": {
     "type": "object",
     "properties": {
      "at": {
       "type": "string",
       "format": "date-time"
      },
      "reason": {
       "type": "string"
      },
      "fromLevel": {
       "type": "integer"
      },
      "toLevel": {
       "type": "integer"
      },
      "wasAutomatic": {
       "type": "boolean"
      }
     }
    }
   },
   "resubmittedFromId": {
    "type": "string",
    "nullable": true
   },
   "reopenedFromId": {
    "type": "string",
    "nullable": true
   },
   "slaDueAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "slaBreached": {
    "type": "boolean"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "requestedAt": {
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
 "ApprovalStatus": {
  "type": "string",
  "enum": [
   "draft",
   "pending",
   "escalated",
   "approved",
   "rejected",
   "withdrawn",
   "expired",
   "cancelled"
  ]
 },
 "CampaignCalendarTimelineView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Campaign Calendar & Timeline displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "day": {
    "type": "string",
    "description": "Day"
   },
   "week": {
    "type": "string",
    "description": "Week"
   },
   "month": {
    "type": "string",
    "description": "Month"
   },
   "quarter": {
    "type": "string",
    "description": "Quarter"
   },
   "campaignTimeline": {
    "type": "string",
    "description": "Campaign timeline"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "attraction": {
    "type": "string",
    "description": "Attraction"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "campaign": {
    "type": "string",
    "description": "Campaign"
   },
   "promotionFamily": {
    "type": "string",
    "description": "Promotion family"
   },
   "active": {
    "type": "integer",
    "description": "Active"
   },
   "upcoming": {
    "type": "string",
    "description": "Upcoming"
   },
   "endingSoon": {
    "type": "string",
    "description": "Ending soon"
   },
   "expired": {
    "type": "integer",
    "description": "Expired"
   },
   "pendingApproval": {
    "type": "integer",
    "description": "Pending approval"
   },
   "conflicting": {
    "type": "string",
    "description": "Conflicting"
   },
   "suspended": {
    "type": "string",
    "description": "Suspended"
   },
   "dragChangeDatesSubjectToPermission": {
    "type": "string",
    "description": "Drag/change dates subject to permission"
   },
   "segmentDateAndChannel": {
    "type": "string",
    "format": "date-time",
    "description": "segment, date, and channel"
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
 "PromotionAlertsExceptionCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Promotion Alerts & Exception Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "missingProduct": {
    "type": "string",
    "description": "Missing product"
   },
   "missingEligibility": {
    "type": "string",
    "description": "Missing eligibility"
   },
   "invalidDates": {
    "type": "string",
    "description": "Invalid dates"
   },
   "invalidDiscount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Invalid discount"
   },
   "invalidCode": {
    "type": "string",
    "description": "Invalid code"
   },
   "missingApproval": {
    "type": "string",
    "description": "Missing approval"
   },
   "budgetNearLimit": {
    "type": "integer",
    "description": "Budget near limit"
   },
   "budgetExceeded": {
    "type": "string",
    "description": "Budget exceeded"
   },
   "marginBelowThreshold": {
    "type": "integer",
    "description": "Margin below threshold"
   },
   "excessiveDiscountExposure": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Excessive discount exposure"
   },
   "promotionFailedToPublish": {
    "type": "string",
    "description": "Promotion failed to publish"
   },
   "productUnavailable": {
    "type": "string",
    "description": "Product unavailable"
   },
   "bundleComponentUnavailable": {
    "type": "string",
    "description": "Bundle component unavailable"
   },
   "channelSynchronizationFailure": {
    "type": "string",
    "description": "Channel synchronization failure"
   },
   "lowConversion": {
    "type": "number",
    "description": "Low conversion"
   },
   "lowRedemption": {
    "type": "string",
    "description": "Low redemption"
   },
   "unexpectedHighRedemption": {
    "type": "string",
    "description": "Unexpected high redemption"
   },
   "campaignUnderperforming": {
    "type": "string",
    "description": "Campaign underperforming"
   },
   "abnormalCouponUsage": {
    "type": "string",
    "description": "Abnormal coupon usage"
   },
   "excessiveRepeatRedemption": {
    "type": "string",
    "description": "Excessive repeat redemption"
   },
   "suspiciousCustomerBehavior": {
    "type": "string",
    "description": "Suspicious customer behavior"
   },
   "promoCodeLeakage": {
    "type": "string",
    "description": "Promo-code leakage"
   },
   "information": {
    "type": "string",
    "description": "Information"
   },
   "warning": {
    "type": "string",
    "description": "Warning"
   },
   "critical": {
    "type": "string",
    "description": "Critical"
   }
  }
 },
 "PromotionAuditActivityVersionHistoryView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Promotion Audit, Activity & Version History displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "promotionCreated": {
    "type": "string",
    "format": "date-time",
    "description": "Promotion created"
   },
   "promotionEdited": {
    "type": "string",
    "description": "Promotion edited"
   },
   "ruleChanged": {
    "type": "string",
    "description": "Rule changed"
   },
   "discountChanged": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Discount changed"
   },
   "productAdded": {
    "type": "string",
    "description": "Product added"
   },
   "productRemoved": {
    "type": "string",
    "description": "Product removed"
   },
   "eligibilityChanged": {
    "type": "string",
    "description": "Eligibility changed"
   },
   "channelChanged": {
    "type": "string",
    "description": "Channel changed"
   },
   "datesChanged": {
    "type": "string",
    "description": "Dates changed"
   },
   "budgetChanged": {
    "type": "string",
    "description": "Budget changed"
   },
   "approvalSubmitted": {
    "type": "string",
    "description": "Approval submitted"
   },
   "approvalGranted": {
    "type": "string",
    "description": "Approval granted"
   },
   "approvalRejected": {
    "type": "string",
    "description": "Approval rejected"
   },
   "promotionActivated": {
    "type": "string",
    "description": "Promotion activated"
   },
   "promotionPaused": {
    "type": "string",
    "description": "Promotion paused"
   },
   "promotionSuspended": {
    "type": "string",
    "description": "Promotion suspended"
   },
   "promotionExpired": {
    "type": "string",
    "description": "Promotion expired"
   },
   "promotionArchived": {
    "type": "string",
    "description": "Promotion archived"
   },
   "user": {
    "type": "string",
    "description": "User"
   },
   "role": {
    "type": "string",
    "description": "Role"
   },
   "dateTime": {
    "type": "string",
    "format": "date-time",
    "description": "Date/time"
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
   "promotionVersion": {
    "type": "string",
    "description": "Promotion version"
   },
   "version23Version24": {
    "type": "string",
    "description": "Version 2.3 ↔ Version 2.4"
   },
   "andSeeExactlyWhatChanged": {
    "type": "string",
    "description": "and see exactly what changed"
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
   "venueManager": {
    "type": "string",
    "description": "Venue Manager"
   },
   "operations": {
    "type": "string",
    "description": "Operations"
   },
   "b2bManager": {
    "type": "string",
    "description": "B2B Manager"
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
   "readOnly": {
    "type": "string",
    "description": "Read Only"
   }
  }
 },
 "PromotionCampaignDirectoryView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Promotion & Campaign Directory displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "promotionId": {
    "type": "string",
    "description": "Promotion ID"
   },
   "promotionName": {
    "type": "string",
    "description": "Promotion Name"
   },
   "promotionType": {
    "type": "string",
    "description": "Promotion Type"
   },
   "campaign": {
    "type": "string",
    "description": "Campaign"
   },
   "status": {
    "type": "string",
    "description": "Status"
   },
   "businessEntity": {
    "type": "string",
    "description": "Business Entity"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "targetSegment": {
    "type": "string",
    "description": "Target Segment"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "startDate": {
    "type": "string",
    "format": "date-time",
    "description": "Start Date"
   },
   "endDate": {
    "type": "string",
    "format": "date-time",
    "description": "End Date"
   },
   "discountType": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Discount Type"
   },
   "discountValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Discount Value"
   },
   "budget": {
    "type": "string",
    "description": "Budget"
   },
   "redemptionCount": {
    "type": "integer",
    "description": "Redemption Count"
   },
   "revenueGenerated": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue Generated"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   },
   "approvalStatus": {
    "type": "string",
    "description": "Approval Status"
   },
   "version": {
    "type": "string",
    "description": "Version"
   },
   "lastModified": {
    "type": "string",
    "format": "date-time",
    "description": "Last Modified"
   },
   "statusesType": {
    "type": "string",
    "enum": [
     "draft",
     "configurationIncomplete",
     "simulationRequired",
     "pendingApproval",
     "approved",
     "scheduled",
     "active",
     "paused",
     "suspended",
     "budgetExhausted",
     "expired",
     "cancelled",
     "archived"
    ],
    "description": "Vocabulary listed under Supported Statuses."
   },
   "productCategory": {
    "type": "string",
    "description": "Product category"
   },
   "attraction": {
    "type": "string",
    "description": "Attraction"
   },
   "event": {
    "type": "string",
    "description": "Event"
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
   "partner": {
    "type": "string",
    "description": "Partner"
   },
   "customerSegment": {
    "type": "string",
    "description": "Customer segment"
   },
   "date": {
    "type": "string",
    "format": "date-time",
    "description": "Date"
   },
   "approvalState": {
    "type": "string",
    "description": "Approval state"
   },
   "promotionValue": {
    "type": "string",
    "description": "Promotion value"
   },
   "budgetStatus": {
    "type": "string",
    "description": "Budget status"
   }
  }
 },
 "PromotionChannelPublicationMonitorView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Promotion Channel & Publication Monitor displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "channelsType": {
    "type": "string",
    "enum": [
     "b2cWebsite",
     "b2bPortal",
     "pos",
     "mobilePos",
     "kiosk",
     "mobileApp",
     "callCenter",
     "guestPortal",
     "api",
     "ota",
     "reseller",
     "partnerPortal",
     "fBPos",
     "retailPos"
    ],
    "description": "Vocabulary listed under Supported Channels."
   },
   "notAssigned": {
    "type": "string",
    "description": "Not Assigned"
   },
   "pendingPublication": {
    "type": "integer",
    "description": "Pending Publication"
   },
   "published": {
    "type": "string",
    "description": "Published"
   },
   "synchronizing": {
    "type": "string",
    "description": "Synchronizing"
   },
   "publicationFailed": {
    "type": "integer",
    "description": "Publication Failed"
   },
   "outOfSync": {
    "type": "string",
    "description": "Out of Sync"
   },
   "suspended": {
    "type": "string",
    "description": "Suspended"
   },
   "promotionVersion": {
    "type": "string",
    "description": "Promotion version"
   },
   "lastSynchronized": {
    "type": "string",
    "format": "date-time",
    "description": "Last synchronized"
   },
   "rulesPublished": {
    "type": "string",
    "description": "Rules published"
   },
   "productsPublished": {
    "type": "string",
    "description": "Products published"
   },
   "codeAvailability": {
    "type": "string",
    "description": "Code availability"
   },
   "channelRestrictions": {
    "type": "integer",
    "description": "Channel restrictions"
   },
   "errorMessages": {
    "type": "integer",
    "description": "Error messages"
   },
   "republish": {
    "type": "string",
    "description": "Republish"
   },
   "platformAndAllConsumerFacingChannels": {
    "type": "string",
    "description": "platform and all consumer-facing channels"
   }
  }
 },
 "PromotionHealthPerformanceMonitorView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Promotion Health & Performance Monitor displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "impressions": {
    "type": "integer",
    "description": "Impressions"
   },
   "promotionViews": {
    "type": "integer",
    "description": "Promotion views"
   },
   "eligibleTransactions": {
    "type": "integer",
    "description": "Eligible transactions"
   },
   "promotionApplications": {
    "type": "integer",
    "description": "Promotion applications"
   },
   "redemptions": {
    "type": "integer",
    "description": "Redemptions"
   },
   "redemptionRate": {
    "type": "number",
    "description": "Redemption rate"
   },
   "conversionRate": {
    "type": "number",
    "description": "Conversion rate"
   },
   "grossSales": {
    "type": "integer",
    "description": "Gross sales"
   },
   "netSales": {
    "type": "integer",
    "description": "Net sales"
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
   "margin": {
    "type": "number",
    "description": "Margin"
   },
   "costPerRedemption": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Cost per redemption"
   },
   "budgetConsumed": {
    "type": "string",
    "description": "Budget consumed"
   },
   "budgetRemaining": {
    "type": "string",
    "description": "Budget remaining"
   },
   "promotionVsBaseline": {
    "type": "string",
    "description": "Promotion vs baseline"
   },
   "promotionVsPreviousCampaign": {
    "type": "string",
    "description": "Promotion vs previous campaign"
   },
   "promotionVsAiForecast": {
    "type": "string",
    "description": "Promotion vs AI forecast"
   },
   "promotionVsControlGroup": {
    "type": "string",
    "description": "Promotion vs control group"
   },
   "channelVsChannel": {
    "type": "string",
    "description": "Channel vs channel"
   },
   "venueVsVenue": {
    "type": "string",
    "description": "Venue vs venue"
   }
  }
 },
 "PromotionLifecycleStatusManagerView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Promotion Lifecycle & Status Manager displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "pausedSuspendedExpiredArchived": {
    "type": "string",
    "description": "Paused/Suspended → Expired → Archived"
   },
   "terminate": {
    "type": "string",
    "description": "Terminate"
   },
   "requiredConfigurationIsCompleted": {
    "type": "string",
    "description": "Required configuration is completed"
   },
   "validProductsExist": {
    "type": "string",
    "description": "Valid products exist"
   },
   "datesAreValid": {
    "type": "string",
    "description": "Dates are valid"
   },
   "promotionRulesDoNotConflict": {
    "type": "string",
    "description": "Promotion rules do not conflict"
   },
   "budgetExistsWhereRequired": {
    "type": "boolean",
    "description": "Budget exists where required"
   },
   "channelsAreAssigned": {
    "type": "string",
    "description": "Channels are assigned"
   },
   "customerEligibilityExists": {
    "type": "string",
    "description": "Customer eligibility exists"
   },
   "approvalIsCompleted": {
    "type": "string",
    "description": "Approval is completed"
   },
   "financialExposureIsAbnormal": {
    "type": "string",
    "description": "Financial exposure is abnormal"
   },
   "fraudIsDetected": {
    "type": "string",
    "description": "Fraud is detected"
   },
   "incorrectDiscountOccurs": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Incorrect discount occurs"
   },
   "aPartnerRequestsSuspension": {
    "type": "string",
    "description": "A partner requests suspension"
   },
   "inventoryBecomesUnavailable": {
    "type": "string",
    "description": "Inventory becomes unavailable"
   },
   "campaignBudgetIsExhausted": {
    "type": "string",
    "description": "Campaign budget is exhausted"
   }
  }
 },
 "PromotionUsage": {
  "x-ticvai-persistence": "none — aggregated from ledger and orders",
  "type": "object",
  "required": [
   "promotionId",
   "redemptionCount",
   "discountGiven"
  ],
  "properties": {
   "promotionId": {
    "type": "string",
    "format": "uuid"
   },
   "redemptionCount": {
    "type": "integer"
   },
   "discountGiven": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "budgetCap": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "budgetRemaining": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "isBudgetExhausted": {
    "type": "boolean"
   },
   "byChannel": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "channel": {
       "type": "string"
      },
      "redemptionCount": {
       "type": "integer"
      },
      "discountGiven": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      }
     }
    }
   }
  }
 }
}
```
