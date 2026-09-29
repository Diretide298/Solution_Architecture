# WS51 — Promotions   Bundles Management board 7

**10 screens · 11 operations · 13 schemas · 3 permissions**

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
  `ORDER_CREATE, PRICE_CONFIGURE, PRICE_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-198` | Targeting & Eligibility Command Center | commandCentre | 1 | 0 | — |
| `ADM-199` | Eligibility Rule Builder | listDetail | 2 | 0 | — |
| `ADM-200` | CRM & Customer Segment Manager | listDetail | 1 | 0 | — |
| `ADM-201` | Membership, Loyalty & Guest Eligibility | listDetail | 1 | 0 | — |
| `ADM-202` | Behavioral & Transaction Targeting | configEditor | 1 | 0 | — |
| `ADM-203` | Context, Location, Channel & Time Targeting | listDetail | 1 | 0 | — |
| `ADM-204` | Partner, B2B & Payment Eligibility | listDetail | 1 | 0 | — |
| `ADM-205` | Audience Preview, Reach & Eligibility Simulator | commandCentre | 1 | 0 | — |
| `ADM-206` | Targeting Conflict, Frequency & Exclusion Controls | configEditor | 1 | 0 | — |
| `ADM-207` | AI Audience Discovery & Targeting Optimization | listDetail | 1 | 0 | — |

## Thin screens in this batch

**ADM-199, ADM-200, ADM-201, ADM-203, ADM-204, ADM-207 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-198",
  "name": "Targeting & Eligibility Command Center",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "7",
   "number": "1",
   "page": 94
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/targeting-eligibility-command-center-adm-198",
   "component": "apps/ticvai-web/src/routes/commercial/TargetingEligibilityCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-199",
    "ADM-200",
    "ADM-201",
    "ADM-202",
    "ADM-203",
    "ADM-204",
    "ADM-205",
    "ADM-206",
    "ADM-207"
   ],
   "inferred": false,
   "notes": "**The board's hub.** The workshop specified this module as boards of ten and opened each with a command centre; the other nine screens are that board's detail, so they are reached from here and return here.",
   "transitions": [
    {
     "to": "ADM-002",
     "trigger": "Platform Dashboard",
     "provenance": "derived — ADM-002 declares entryState.params  and ADM-198 holds none of them, so the edge carries nothing and ADM-002 opens cold"
    },
    {
     "to": "ADM-199",
     "trigger": "Works in Eligibility Rule Builder",
     "provenance": "flow F160 step 1→2",
     "operation": "listTargetingEligibility"
    },
    {
     "to": "ADM-200",
     "trigger": "Works in CRM & Customer Segment Manager",
     "provenance": "flow F160 step 3→4",
     "operation": "listTargetingEligibility"
    },
    {
     "to": "ADM-201",
     "trigger": "Works in Membership, Loyalty & Guest Eligibility",
     "provenance": "flow F160 step 5→6",
     "operation": "listTargetingEligibility"
    },
    {
     "to": "ADM-202",
     "trigger": "Works in Behavioral & Transaction Targeting",
     "provenance": "flow F160 step 7→8",
     "operation": "listTargetingEligibility"
    },
    {
     "to": "ADM-203",
     "trigger": "Works in Context, Location, Channel & Time Targeting",
     "provenance": "flow F160 step 9→10",
     "operation": "listTargetingEligibility"
    },
    {
     "to": "ADM-204",
     "trigger": "Works in Partner, B2B & Payment Eligibility",
     "provenance": "flow F160 step 11→12",
     "operation": "listTargetingEligibility"
    },
    {
     "to": "ADM-205",
     "trigger": "Works in Audience Preview, Reach & Eligibility Simulator",
     "provenance": "flow F160 step 13→14",
     "operation": "listTargetingEligibility"
    },
    {
     "to": "ADM-206",
     "trigger": "Works in Targeting Conflict, Frequency & Exclusion Controls",
     "provenance": "flow F160 step 15→16",
     "operation": "listTargetingEligibility"
    },
    {
     "to": "ADM-207",
     "trigger": "Works in AI Audience Discovery & Targeting Optimization",
     "provenance": "flow F160 step 17→18",
     "operation": "listTargetingEligibility"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§KPI Cards) and a per-row directory (§Each rule shows) — counts over a population, then the population",
  "purpose": "Provide centralized visibility into all promotion audiences, eligibility rules, segments, targeting strategies, and their performance.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search targeting eligibility",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 94 §Filter by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Guest type",
        "CRM segment",
        "Membership",
        "Loyalty",
        "Demographic",
        "Behavioral",
        "Transaction",
        "Geographic",
        "Channel",
        "Partner",
        "B2B",
        "Payment",
        "Contextual",
        "AI-generated"
       ],
       "notes": "The pack filters this screen by guest type, crm segment, membership, loyalty, demographic, behavioral and 8 more — which are present is a decision the pack already made.",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 94 §Filter by"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Active Targeting Rules",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 94 §KPI Cards",
       "bindsTo": "TargetingEligibilityCommandCenterView.activeTargetingRules"
      },
      {
       "kind": "metricTile",
       "label": "Active Segments",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 94 §KPI Cards",
       "bindsTo": "TargetingEligibilityCommandCenterView.activeSegments"
      },
      {
       "kind": "metricTile",
       "label": "Promotions Using Targeting",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 94 §KPI Cards",
       "bindsTo": "TargetingEligibilityCommandCenterView.promotionsUsingTargeting"
      },
      {
       "kind": "metricTile",
       "label": "Bundles Using Targeting",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 94 §KPI Cards",
       "bindsTo": "TargetingEligibilityCommandCenterView.bundlesUsingTargeting"
      },
      {
       "kind": "metricTile",
       "label": "Eligible Customers",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 94 §KPI Cards",
       "bindsTo": "TargetingEligibilityCommandCenterView.eligibleCustomers"
      },
      {
       "kind": "metricTile",
       "label": "Targeted Customers",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 94 §KPI Cards",
       "bindsTo": "TargetingEligibilityCommandCenterView.targetedCustomers"
      },
      {
       "kind": "metricTile",
       "label": "Personalized Offers",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 94 §KPI Cards",
       "bindsTo": "TargetingEligibilityCommandCenterView.personalizedOffers"
      },
      {
       "kind": "metricTile",
       "label": "Eligibility Pass Rate",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 94 §KPI Cards",
       "bindsTo": "TargetingEligibilityCommandCenterView.eligibilityPassRate"
      },
      {
       "kind": "metricTile",
       "label": "Conversion Rate",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 94 §KPI Cards",
       "bindsTo": "TargetingEligibilityCommandCenterView.conversionRate"
      },
      {
       "kind": "metricTile",
       "label": "Targeted Revenue",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 94 §KPI Cards",
       "bindsTo": "TargetingEligibilityCommandCenterView.targetedRevenue"
      },
      {
       "kind": "metricTile",
       "label": "AOV Uplift",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 94 §KPI Cards",
       "bindsTo": "TargetingEligibilityCommandCenterView.aovUplift"
      },
      {
       "kind": "metricTile",
       "label": "AI-Recommended Segments",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 94 §KPI Cards",
       "bindsTo": "TargetingEligibilityCommandCenterView.aiRecommendedSegments"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every targeting eligibility",
       "columns": [
        "TargetingEligibilityCommandCenterView.ruleHealth"
       ],
       "bindsTo": "TargetingEligibilityCommandCenterView",
       "operation": "listTargetingEligibility",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 94 §Each rule shows"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected targeting eligibility",
       "bindsTo": "TargetingEligibilityCommandCenterView",
       "columns": [
        "TargetingEligibilityCommandCenterView.ruleHealth"
       ],
       "notes": null,
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 94 §Each rule shows"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The targeting eligibility list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the targeting eligibility untouched.",
   "emptyFirstRun": "No targeting eligibility yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the targeting eligibility are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listTargetingEligibility",
    "contract": "promotions",
    "purpose": "Targeting & Eligibility Command Center",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-198",
   "workshopBoard": "wireframes/WS112 Promotions   Bundles Management Board 7.dc.html#adm-198"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 94. 19 of 33 labels bound to a contract property; 33 of 37 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-199",
  "name": "Eligibility Rule Builder",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "7",
   "number": "2",
   "page": 95
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/eligibility-rule-builder-adm-199",
   "component": "apps/ticvai-web/src/routes/commercial/EligibilityRuleBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-198"
   ],
   "exitTo": [
    "ADM-198"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-198, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-198",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F160 step 2→3",
     "operation": "setEligibilityRule"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide a no-code rule engine for determining promotion eligibility.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Multiple condition sets. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 95 §Support"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 95"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 95"
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
       "label": "Multiple condition sets",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 95 §Support"
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
       "impliedBy": "setEligibilityRule"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The eligibility rule list.",
   "error": "Could not load. Names which read failed and leaves the eligibility rule untouched.",
   "emptyFirstRun": "No eligibility rule yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the eligibility rule are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setEligibilityRule",
    "contract": "promotions",
    "purpose": "Eligibility Rule Builder",
    "trigger": "onAction"
   },
   {
    "operationId": "setResaleEligibilityRule",
    "contract": "orders",
    "purpose": "Resale Eligibility Rule Configuration",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-199",
   "workshopBoard": "wireframes/WS112 Promotions   Bundles Management Board 7.dc.html#adm-199"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 95. 0 of 0 labels bound to a contract property; 1 of 33 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-200",
  "name": "CRM & Customer Segment Manager",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "7",
   "number": "3",
   "page": 96
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/crm-customer-segment-manager-adm-200",
   "component": "apps/ticvai-web/src/routes/commercial/CrmCustomerSegmentManager.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-198"
   ],
   "exitTo": [
    "ADM-198"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-198, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-198",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F160 step 4→5",
     "operation": "listCrmCustomerSegment"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Connect promotion eligibility directly to TICVAI CRM segmentation. The board should consume CRM segments rather than recreate CRM functionality.",
  "gaps": [
   {
    "operation": null,
    "why": "**CRM & Customer Segment Manager declares no operation that writes anything** — its only declared call is `listCrmCustomerSegment`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
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
       "label": "Every crm customer segment",
       "columns": [
        "CrmCustomerSegmentManagerView.segmentName",
        "CrmCustomerSegmentManagerView.source",
        "CrmCustomerSegmentManagerView.estimatedAudience",
        "CrmCustomerSegmentManagerView.lastRefreshed",
        "CrmCustomerSegmentManagerView.promotionsUsingSegment",
        "CrmCustomerSegmentManagerView.conversion",
        "CrmCustomerSegmentManagerView.revenue",
        "CrmCustomerSegmentManagerView.status"
       ],
       "bindsTo": "CrmCustomerSegmentManagerView",
       "operation": "listCrmCustomerSegment",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 96 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected crm customer segment",
       "bindsTo": "CrmCustomerSegmentManagerView",
       "columns": [
        "CrmCustomerSegmentManagerView.segmentName",
        "CrmCustomerSegmentManagerView.source",
        "CrmCustomerSegmentManagerView.estimatedAudience",
        "CrmCustomerSegmentManagerView.lastRefreshed",
        "CrmCustomerSegmentManagerView.promotionsUsingSegment",
        "CrmCustomerSegmentManagerView.conversion",
        "CrmCustomerSegmentManagerView.revenue",
        "CrmCustomerSegmentManagerView.status"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Segment Sources”.",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 96 §Show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The crm customer segment list.",
   "error": "Could not load. Names which read failed and leaves the crm customer segment untouched.",
   "emptyFirstRun": "No crm customer segment yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the crm customer segment are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCrmCustomerSegment",
    "contract": "promotions",
    "purpose": "CRM & Customer Segment Manager",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "CrmCustomerSegmentManagerView.segmentName",
    "CrmCustomerSegmentManagerView.source",
    "CrmCustomerSegmentManagerView.estimatedAudience",
    "CrmCustomerSegmentManagerView.lastRefreshed",
    "CrmCustomerSegmentManagerView.promotionsUsingSegment",
    "CrmCustomerSegmentManagerView.conversion"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-200",
   "workshopBoard": "wireframes/WS112 Promotions   Bundles Management Board 7.dc.html#adm-200"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 96. 8 of 8 labels bound to a contract property; 8 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-201",
  "name": "Membership, Loyalty & Guest Eligibility",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "7",
   "number": "4",
   "page": 97
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/membership-loyalty-guest-eligibility-adm-201",
   "component": "apps/ticvai-web/src/routes/commercial/MembershipLoyaltyGuestEligibility.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-198"
   ],
   "exitTo": [
    "ADM-198"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-198, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-198",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F160 step 6→7",
     "operation": "listMembershipLoyaltyGuest"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure targeting based on membership, loyalty status, guest categories, and entitlement relationships.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 97"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 97"
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
       "impliedBy": "listMembershipLoyaltyGuest",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The membership loyalty guest list.",
   "error": "Could not load. Names which read failed and leaves the membership loyalty guest untouched.",
   "emptyFirstRun": "No membership loyalty guest yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the membership loyalty guest are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listMembershipLoyaltyGuest",
    "contract": "promotions",
    "purpose": "Membership, Loyalty & Guest Eligibility",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "MembershipLoyaltyGuestEligibilityView.membershipType",
    "MembershipLoyaltyGuestEligibilityView.membershipTier",
    "MembershipLoyaltyGuestEligibilityView.membershipStatus",
    "MembershipLoyaltyGuestEligibilityView.membershipStartDate",
    "MembershipLoyaltyGuestEligibilityView.renewalStatus"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-201",
   "workshopBoard": "wireframes/WS112 Promotions   Bundles Management Board 7.dc.html#adm-201"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 97. 0 of 0 labels bound to a contract property; 0 of 32 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-202",
  "name": "Behavioral & Transaction Targeting",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "7",
   "number": "5",
   "page": 98
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/behavioral-transaction-targeting-adm-202",
   "component": "apps/ticvai-web/src/routes/commercial/BehavioralTransactionTargeting.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-198"
   ],
   "exitTo": [
    "ADM-198"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-198, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-198",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F160 step 8→9",
     "operation": "listBehavioralTransactionTargeting"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Target promotions according to what the guest has previously purchased or done.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Last 7 days",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 98 §Configure"
      },
      {
       "kind": "selectField",
       "label": "30 days",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 98 §Configure"
      },
      {
       "kind": "selectField",
       "label": "90 days",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 98 §Configure"
      },
      {
       "kind": "selectField",
       "label": "12 months",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 98 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Lifetime",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 98 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Custom period",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 98 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The behavioral transaction targeting configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the behavioral transaction targeting untouched.",
   "emptyFirstRun": "No behavioral transaction targeting configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listBehavioralTransactionTargeting",
    "contract": "promotions",
    "purpose": "Behavioral & Transaction Targeting",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-202",
   "workshopBoard": "wireframes/WS112 Promotions   Bundles Management Board 7.dc.html#adm-202"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 98. 0 of 0 labels bound to a contract property; 6 of 29 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-203",
  "name": "Context, Location, Channel & Time Targeting",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "7",
   "number": "6",
   "page": 99
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/context-location-channel-time-targeting-adm-203",
   "component": "apps/ticvai-web/src/routes/commercial/ContextLocationChannelTimeTargeting.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-198"
   ],
   "exitTo": [
    "ADM-198"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-198, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-198",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F160 step 10→11",
     "operation": "listContextLocationChannel"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Determine promotion eligibility according to the customer's current commercial context.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 2 actions on this screen and the screen declares 1 operation.** Unserved: Product currently viewed, Current booking. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 99 §Support"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 99"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 99"
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
       "label": "Product currently viewed",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 99 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Current booking",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 99 §Support"
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
   "loading": "The context location channel list.",
   "error": "Could not load. Names which read failed and leaves the context location channel untouched.",
   "emptyFirstRun": "No context location channel yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the context location channel are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listContextLocationChannel",
    "contract": "promotions",
    "purpose": "Context, Location, Channel & Time Targeting",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "ContextLocationChannelTimeTargetingView.channels"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-203",
   "workshopBoard": "wireframes/WS112 Promotions   Bundles Management Board 7.dc.html#adm-203"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 99. 0 of 0 labels bound to a contract property; 2 of 32 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-204",
  "name": "Partner, B2B & Payment Eligibility",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "7",
   "number": "7",
   "page": 100
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/partner-b2b-payment-eligibility-adm-204",
   "component": "apps/ticvai-web/src/routes/commercial/PartnerB2bPaymentEligibility.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-198"
   ],
   "exitTo": [
    "ADM-198"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-198, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-198",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F160 step 12→13",
     "operation": "listPartnerPaymentEligibility"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure eligibility for partner, corporate, reseller, B2B, and payment-related campaigns.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 100"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 100"
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
       "impliedBy": "listPartnerPaymentEligibility",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The partner b2b payment list.",
   "error": "Could not load. Names which read failed and leaves the partner b2b payment untouched.",
   "emptyFirstRun": "No partner b2b payment yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the partner b2b payment are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPartnerPaymentEligibility",
    "contract": "promotions",
    "purpose": "Partner, B2B & Payment Eligibility",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "PartnerB2bPaymentEligibilityView.partner",
    "PartnerB2bPaymentEligibilityView.partnerCategory",
    "PartnerB2bPaymentEligibilityView.corporateAccount",
    "PartnerB2bPaymentEligibilityView.employer",
    "PartnerB2bPaymentEligibilityView.hotel"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-204",
   "workshopBoard": "wireframes/WS112 Promotions   Bundles Management Board 7.dc.html#adm-204"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 100. 0 of 0 labels bound to a contract property; 0 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-205",
  "name": "Audience Preview, Reach & Eligibility Simulator",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "7",
   "number": "8",
   "page": 101
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/audience-preview-reach-eligibility-simulator-adm-205",
   "component": "apps/ticvai-web/src/routes/commercial/AudiencePreviewReachEligibilitySimulator.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-198"
   ],
   "exitTo": [
    "ADM-198"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-198, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-198",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F160 step 14→15",
     "operation": "listAudiencePreviewReach"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Audience Metrics) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Allow administrators to understand exactly who will qualify before activating the targeting rule. This is a critical safeguard.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Estimated audience",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 101 §Audience Metrics",
       "bindsTo": "AudiencePreviewReachEligibilitySimulatorView.estimatedAudience"
      },
      {
       "kind": "metricTile",
       "label": "Percentage of customer base",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 101 §Audience Metrics",
       "bindsTo": "AudiencePreviewReachEligibilitySimulatorView.percentageOfCustomerBase"
      },
      {
       "kind": "metricTile",
       "label": "Historical conversion",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 101 §Audience Metrics",
       "bindsTo": "AudiencePreviewReachEligibilitySimulatorView.historicalConversion"
      },
      {
       "kind": "metricTile",
       "label": "Historical AOV",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 101 §Audience Metrics",
       "bindsTo": "AudiencePreviewReachEligibilitySimulatorView.historicalAov"
      },
      {
       "kind": "metricTile",
       "label": "Expected redemptions",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 101 §Audience Metrics",
       "bindsTo": "AudiencePreviewReachEligibilitySimulatorView.expectedRedemptions"
      },
      {
       "kind": "metricTile",
       "label": "Estimated promotion cost",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 101 §Audience Metrics",
       "bindsTo": "AudiencePreviewReachEligibilitySimulatorView.estimatedPromotionCost"
      },
      {
       "kind": "metricTile",
       "label": "Estimated revenue",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 101 §Audience Metrics",
       "bindsTo": "AudiencePreviewReachEligibilitySimulatorView.estimatedRevenue"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The audience preview reach list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the audience preview reach untouched.",
   "emptyFirstRun": "No audience preview reach yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the audience preview reach are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAudiencePreviewReach",
    "contract": "promotions",
    "purpose": "Audience Preview, Reach & Eligibility Simulator",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "AudiencePreviewReachEligibilitySimulatorView.estimatedAudience",
    "AudiencePreviewReachEligibilitySimulatorView.percentageOfCustomerBase",
    "AudiencePreviewReachEligibilitySimulatorView.historicalConversion",
    "AudiencePreviewReachEligibilitySimulatorView.historicalAov",
    "AudiencePreviewReachEligibilitySimulatorView.expectedRedemptions",
    "AudiencePreviewReachEligibilitySimulatorView.estimatedPromotionCost"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-205",
   "workshopBoard": "wireframes/WS112 Promotions   Bundles Management Board 7.dc.html#adm-205"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 101. 7 of 7 labels bound to a contract property; 7 of 26 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-206",
  "name": "Targeting Conflict, Frequency & Exclusion Controls",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "7",
   "number": "9",
   "page": 102
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/targeting-conflict-frequency-exclusion-controls-adm-206",
   "component": "apps/ticvai-web/src/routes/commercial/TargetingConflictFrequencyExclusionControls.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-198"
   ],
   "exitTo": [
    "ADM-198"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-198, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-198",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F160 step 16→17",
     "operation": "listTargetingConflictFrequency"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Prevent customers from being over-targeted and prevent inappropriate promotional eligibility.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 4 actions on this screen and the screen declares 1 operation.** Unserved: Existing member, Specific CRM segment, Partner restriction, Product ownership. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 102 §Support"
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
       "kind": "textField",
       "label": "Maximum offers per day",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 102 §Configure"
      },
      {
       "kind": "textField",
       "label": "Maximum offers per week",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 102 §Configure"
      },
      {
       "kind": "textField",
       "label": "Maximum campaigns per month",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 102 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum redemptions",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 102 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Cooling-off period",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 102 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Repeat campaign restriction",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 102 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Existing member",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 102 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Specific CRM segment",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 102 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Partner restriction",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 102 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Product ownership",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 102 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The targeting conflict frequency configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the targeting conflict frequency untouched.",
   "emptyFirstRun": "No targeting conflict frequency configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listTargetingConflictFrequency",
    "contract": "promotions",
    "purpose": "Targeting Conflict, Frequency & Exclusion Controls",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-206",
   "workshopBoard": "wireframes/WS112 Promotions   Bundles Management Board 7.dc.html#adm-206"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 102. 0 of 0 labels bound to a contract property; 10 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-207",
  "name": "AI Audience Discovery & Targeting Optimization",
  "module": "Commercial",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Promotions___Bundles_Management_Reference.pdf",
   "board": "7",
   "number": "10",
   "page": 103
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/ai-audience-discovery-targeting-optimization-adm-207",
   "component": "apps/ticvai-web/src/routes/commercial/AiAudienceDiscoveryTargetingOptimization.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-198"
   ],
   "exitTo": [
    "ADM-198"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-198, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation."
  },
  "density": "compact",
  "purposeNote": "Board 7 shall be complete when: 1. Authorized users can create eligibility rules without development. 2. Rules support AND/OR/NOT and nested conditions. 3. Rules can explicitly include and exclude audiences. 4. CRM segments can be consumed without recreating CRM segmentation unnecessarily. 5. Membership status and tier can determine eligibility. 6. Loyalty tier and permitted loyalty attributes can determine eligibility. 7. Guest categories can determine eligibility. 8. Historical purchases can determine eligibility. 9. Visit history can determine eligibility. 10.Previous promotion redemption c",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Use TICVAI's AI layer to identify customer audiences and promotion opportunities that business users may not have manually defined. Board 8 shall provide TICVAI with the centralized Promotion Decision Engine responsible for determining what happens when multiple promotions, discounts, coupons, bundles, loyalty benefits, membership benefits, payment offers, BOGO mechanics, partner offers, or special prices qualify for the same transaction. This is one of the most important boards in the Promotions module because the previous boards may all produce valid offers simultaneously. For example, a guest could qualify for: Annual Pass Holder — 15% discount SUMMER20 coupon — 20% discount Emirates NBD card — 10% discount Buy 4 Pay 3 — promotional mechanic Loyalty Gold — 5% benefit Can they combine? In what order? Which promotion wins? What is the maximum permitted benefit? The matrix explicitly requires configurable promotion hierarchy, stacking and conflict resolution, including scenarios where promotions are combined, mutually exclusive, or prioritized, with clear explanation of which promotion was applied and why. Board 8 shall contain 10 backend screens.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 103"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Promotions___Bundles_Management_Reference.pdf, page 103"
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
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** Audience size: 126,500. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Promotions___Bundles_Management_Reference.pdf, page 103 §Permission Example"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listAudienceDiscoveryTargeting",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The audience discovery targeting list.",
   "error": "Could not load. Names which read failed and leaves the audience discovery targeting untouched.",
   "emptyFirstRun": "No audience discovery targeting yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the audience discovery targeting are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAudienceDiscoveryTargeting",
    "contract": "promotions",
    "purpose": "AI Audience Discovery & Targeting Optimization",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "AiAudienceDiscoveryTargetingOptimizationView.predictedConversion",
    "AiAudienceDiscoveryTargetingOptimizationView.estimatedIncrementalRevenue"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-207",
   "workshopBoard": "wireframes/WS112 Promotions   Bundles Management Board 7.dc.html#adm-207"
  },
  "apisNote": "Regenerated 9 September 2026 from Promotions___Bundles_Management_Reference.pdf page 103. 0 of 0 labels bound to a contract property; 1 of 163 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "listAudienceDiscoveryTargeting": {
  "method": "GET",
  "path": "/audience-discovery-targeting",
  "contract": "promotions",
  "summary": "AI Audience Discovery & Targeting Optimization",
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
  "responds": "AiAudienceDiscoveryTargetingOptimizationView"
 },
 "listAudiencePreviewReach": {
  "method": "GET",
  "path": "/audience-preview-reach",
  "contract": "promotions",
  "summary": "Audience Preview, Reach & Eligibility Simulator",
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
  "responds": "AudiencePreviewReachEligibilitySimulatorView"
 },
 "listBehavioralTransactionTargeting": {
  "method": "GET",
  "path": "/behavioral-transaction-targeting",
  "contract": "promotions",
  "summary": "Behavioral & Transaction Targeting",
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
  "responds": "BehavioralTransactionTargetingView"
 },
 "listContextLocationChannel": {
  "method": "GET",
  "path": "/context-location-channel",
  "contract": "promotions",
  "summary": "Context, Location, Channel & Time Targeting",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ContextLocationChannelTimeTargetingView"
 },
 "listCrmCustomerSegment": {
  "method": "GET",
  "path": "/crm-customer-segment",
  "contract": "promotions",
  "summary": "CRM & Customer Segment Manager",
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
  "responds": "CrmCustomerSegmentManagerView"
 },
 "listMembershipLoyaltyGuest": {
  "method": "GET",
  "path": "/membership-loyalty-guest",
  "contract": "promotions",
  "summary": "Membership, Loyalty & Guest Eligibility",
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
  "responds": "MembershipLoyaltyGuestEligibilityView"
 },
 "listPartnerPaymentEligibility": {
  "method": "GET",
  "path": "/partner-payment-eligibility",
  "contract": "promotions",
  "summary": "Partner, B2B & Payment Eligibility",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "PartnerB2bPaymentEligibilityView"
 },
 "listTargetingConflictFrequency": {
  "method": "GET",
  "path": "/targeting-conflict-frequency",
  "contract": "promotions",
  "summary": "Targeting Conflict, Frequency & Exclusion Controls",
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
  "responds": "TargetingConflictFrequencyExclusionControlsView"
 },
 "listTargetingEligibility": {
  "method": "GET",
  "path": "/targeting-eligibility",
  "contract": "promotions",
  "summary": "Targeting & Eligibility Command Center",
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
    "name": "guestType",
    "in": "query",
    "required": false
   },
   {
    "name": "crmSegment",
    "in": "query",
    "required": false
   },
   {
    "name": "membership",
    "in": "query",
    "required": false
   },
   {
    "name": "loyalty",
    "in": "query",
    "required": false
   },
   {
    "name": "demographic",
    "in": "query",
    "required": false
   },
   {
    "name": "behavioral",
    "in": "query",
    "required": false
   },
   {
    "name": "transaction",
    "in": "query",
    "required": false
   },
   {
    "name": "geographic",
    "in": "query",
    "required": false
   },
   {
    "name": "channel",
    "in": "query",
    "required": false
   },
   {
    "name": "partner",
    "in": "query",
    "required": false
   },
   {
    "name": "b2b",
    "in": "query",
    "required": false
   },
   {
    "name": "payment",
    "in": "query",
    "required": false
   },
   {
    "name": "contextual",
    "in": "query",
    "required": false
   },
   {
    "name": "aiGenerated",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "TargetingEligibilityCommandCenterView"
 },
 "setEligibilityRule": {
  "method": "PUT",
  "path": "/eligibility-rule",
  "contract": "promotions",
  "summary": "Eligibility Rule Builder",
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
  "requestBody": "EligibilityRuleBuilderInput",
  "responds": "EligibilityRuleBuilderView"
 },
 "setResaleEligibilityRule": {
  "method": "PUT",
  "path": "/resale-eligibility-rule",
  "contract": "orders",
  "summary": "Resale Eligibility Rule Configuration",
  "permission": "ORDER_CREATE",
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
  "requestBody": "ResaleEligibilityRuleConfigurationInput",
  "responds": "ResaleEligibilityRuleConfigurationView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AiAudienceDiscoveryTargetingOptimizationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What AI Audience Discovery & Targeting Optimization displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "narrowAudience": {
    "type": "string",
    "description": "Narrow audience"
   },
   "expandAudience": {
    "type": "string",
    "description": "Expand audience"
   },
   "excludeLowValueSegment": {
    "type": "string",
    "description": "Exclude low-value segment"
   },
   "changeEligibility": {
    "type": "string",
    "description": "Change eligibility"
   },
   "changeChannel": {
    "type": "string",
    "description": "Change channel"
   },
   "changeTiming": {
    "type": "string",
    "description": "Change timing"
   },
   "changePromotion": {
    "type": "string",
    "description": "Change promotion"
   },
   "reduceFrequency": {
    "type": "string",
    "description": "Reduce frequency"
   },
   "membershipTierEligibility": {
    "type": "string",
    "description": "Membership/tier eligibility"
   },
   "membershipAndLoyaltyEligibility": {
    "type": "string",
    "description": "Membership and loyalty eligibility"
   },
   "audienceName": {
    "type": "string",
    "description": "Discovered audience"
   },
   "audienceSize": {
    "type": "integer",
    "description": "Audience size"
   },
   "suggestedOffer": {
    "type": "string",
    "description": "Suggested offer"
   },
   "predictedConversion": {
    "type": "number",
    "description": "Predicted conversion, percent"
   },
   "estimatedIncrementalRevenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Estimated incremental revenue"
   },
   "rationale": {
    "type": "string",
    "description": "Why this audience (explainable factors)"
   }
  }
 },
 "AudiencePreviewReachEligibilitySimulatorView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Audience Preview, Reach & Eligibility Simulator displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "estimatedAudience": {
    "type": "string",
    "description": "Estimated audience"
   },
   "percentageOfCustomerBase": {
    "type": "number",
    "description": "Percentage of customer base"
   },
   "historicalConversion": {
    "type": "number",
    "description": "Historical conversion"
   },
   "historicalAov": {
    "type": "string",
    "description": "Historical AOV"
   },
   "expectedRedemptions": {
    "type": "integer",
    "description": "Expected redemptions"
   },
   "estimatedPromotionCost": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Estimated promotion cost"
   },
   "estimatedRevenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Estimated revenue"
   },
   "sampleProfileResult": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Sample profiles tested and whether each is eligible"
   }
  }
 },
 "BehavioralTransactionTargetingView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Behavioral & Transaction Targeting displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "previousProductPurchased": {
    "type": "string",
    "description": "Previous product purchased"
   },
   "previousAttractionVisited": {
    "type": "string",
    "description": "Previous attraction visited"
   },
   "visitFrequency": {
    "type": "string",
    "description": "Visit frequency"
   },
   "daysSinceLastVisit": {
    "type": "string",
    "description": "Days since last visit"
   },
   "previousPromotionRedemption": {
    "type": "string",
    "description": "Previous promotion redemption"
   },
   "abandonedCart": {
    "type": "string",
    "description": "Abandoned cart"
   },
   "bookingFrequency": {
    "type": "string",
    "description": "Booking frequency"
   },
   "purchaseFrequency": {
    "type": "string",
    "description": "Purchase frequency"
   },
   "averageTransactionValue": {
    "type": "number",
    "description": "Average transaction value"
   },
   "totalCustomerValue": {
    "type": "integer",
    "description": "Total customer value"
   },
   "productAffinity": {
    "type": "string",
    "description": "Product affinity"
   },
   "lifetimeSpend": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Lifetime spend"
   },
   "averageBasket": {
    "type": "number",
    "description": "Average basket"
   },
   "numberOfTransactions": {
    "type": "integer",
    "description": "Number of transactions"
   },
   "lastPurchase": {
    "type": "string",
    "format": "date-time",
    "description": "Last purchase"
   },
   "purchaseChannel": {
    "type": "string",
    "description": "Purchase channel"
   },
   "productMix": {
    "type": "string",
    "description": "Product mix"
   },
   "lifetime": {
    "type": "string",
    "description": "Lifetime"
   },
   "lookbackPeriod": {
    "type": "string",
    "enum": [
     "last7Days",
     "last30Days",
     "last90Days",
     "lastYear",
     "customPeriod"
    ],
    "description": "Look-back period for behavioural conditions"
   }
  }
 },
 "ContextLocationChannelTimeTargetingView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Context, Location, Channel & Time Targeting displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "businessEntity": {
    "type": "string",
    "description": "Business entity"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "attraction": {
    "type": "string",
    "description": "Attraction"
   },
   "operatingArea": {
    "type": "string",
    "description": "Operating area"
   },
   "marketCountry": {
    "type": "string",
    "description": "Market/country"
   },
   "salesLocation": {
    "type": "string",
    "description": "Sales location"
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
   "day": {
    "type": "string",
    "description": "Day"
   },
   "time": {
    "type": "string",
    "format": "date-time",
    "description": "Time"
   },
   "season": {
    "type": "string",
    "description": "Season"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "holiday": {
    "type": "string",
    "description": "Holiday"
   },
   "campaignPeriod": {
    "type": "string",
    "format": "date-time",
    "description": "Campaign period"
   },
   "currentBasket": {
    "type": "string",
    "description": "Current basket"
   },
   "productCurrentlyViewed": {
    "type": "string",
    "description": "Product currently viewed"
   },
   "currentBooking": {
    "type": "string",
    "description": "Current booking"
   },
   "visitState": {
    "type": "string",
    "description": "Visit state"
   },
   "inVenueState": {
    "type": "string",
    "description": "In-venue state where available"
   },
   "channels": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "b2cWebsite",
      "mobileApp",
      "pos",
      "mobilePos",
      "kiosk",
      "b2b",
      "callCenter",
      "api",
      "ota",
      "reseller",
      "partner"
     ]
    },
    "description": "Channels that qualify."
   }
  }
 },
 "CrmCustomerSegmentManagerView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What CRM & Customer Segment Manager displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "segmentName": {
    "type": "string",
    "description": "Segment name"
   },
   "estimatedAudience": {
    "type": "string",
    "description": "Estimated audience"
   },
   "lastRefreshed": {
    "type": "string",
    "format": "date-time",
    "description": "Last refreshed"
   },
   "promotionsUsingSegment": {
    "type": "string",
    "description": "Promotions using segment"
   },
   "conversion": {
    "type": "number",
    "description": "Conversion"
   },
   "revenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue"
   },
   "status": {
    "type": "integer",
    "description": "Status"
   },
   "source": {
    "type": "string",
    "enum": [
     "ticvaiCrm",
     "importedSegment",
     "externalCrm",
     "externalCdp",
     "membership",
     "loyalty",
     "b2bAccounts",
     "marketingAutomation"
    ],
    "description": "Where the segment comes from."
   }
  }
 },
 "EligibilityRuleBuilderInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; saved as a `promotions.promotion_rule` row (PromotionRule, ruleType eligibility, its criteria as the condition group and ruleEffect as effect) (DM5, 29 September: data model for the agreed operations)",
  "description": "**What Eligibility Rule Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "guestType": {
    "type": "string",
    "description": "Guest type"
   },
   "customerSegment": {
    "type": "string",
    "description": "Customer segment"
   },
   "ageCategory": {
    "type": "string",
    "description": "Age/category"
   },
   "membership": {
    "type": "string",
    "description": "Membership"
   },
   "loyaltyTier": {
    "type": "string",
    "description": "Loyalty tier"
   },
   "purchaseHistory": {
    "type": "string",
    "description": "Purchase history"
   },
   "visitHistory": {
    "type": "string",
    "description": "Visit history"
   },
   "transactionValue": {
    "type": "string",
    "description": "Transaction value"
   },
   "productPurchased": {
    "type": "string",
    "description": "Product purchased"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "location": {
    "type": "string",
    "description": "Location"
   },
   "partner": {
    "type": "string",
    "description": "Partner"
   },
   "dateTime": {
    "type": "string",
    "format": "date-time",
    "description": "Date/time"
   },
   "paymentMethod": {
    "type": "string",
    "description": "Payment method"
   },
   "campaign": {
    "type": "string",
    "description": "Campaign"
   },
   "customerAccountAttributes": {
    "type": "string",
    "description": "Customer/account attributes"
   },
   "nestedGroups": {
    "type": "string",
    "description": "Nested groups"
   },
   "multipleConditionSets": {
    "type": "string",
    "description": "Multiple condition sets"
   },
   "ruleEffect": {
    "type": "string",
    "enum": [
     "include",
     "exclude"
    ],
    "description": "Whether matching guests are included or excluded."
   }
  }
 },
 "EligibilityRuleBuilderView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Eligibility Rule Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "guestType": {
    "type": "string",
    "description": "Guest type"
   },
   "customerSegment": {
    "type": "string",
    "description": "Customer segment"
   },
   "ageCategory": {
    "type": "string",
    "description": "Age/category"
   },
   "membership": {
    "type": "string",
    "description": "Membership"
   },
   "loyaltyTier": {
    "type": "string",
    "description": "Loyalty tier"
   },
   "purchaseHistory": {
    "type": "string",
    "description": "Purchase history"
   },
   "visitHistory": {
    "type": "string",
    "description": "Visit history"
   },
   "transactionValue": {
    "type": "string",
    "description": "Transaction value"
   },
   "productPurchased": {
    "type": "string",
    "description": "Product purchased"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "location": {
    "type": "string",
    "description": "Location"
   },
   "partner": {
    "type": "string",
    "description": "Partner"
   },
   "dateTime": {
    "type": "string",
    "format": "date-time",
    "description": "Date/time"
   },
   "paymentMethod": {
    "type": "string",
    "description": "Payment method"
   },
   "campaign": {
    "type": "string",
    "description": "Campaign"
   },
   "customerAccountAttributes": {
    "type": "string",
    "description": "Customer/account attributes"
   },
   "nestedGroups": {
    "type": "string",
    "description": "Nested groups"
   },
   "multipleConditionSets": {
    "type": "string",
    "description": "Multiple condition sets"
   },
   "ruleEffect": {
    "type": "string",
    "enum": [
     "include",
     "exclude"
    ],
    "description": "Whether matching guests are included or excluded."
   }
  }
 },
 "MembershipLoyaltyGuestEligibilityView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Membership, Loyalty & Guest Eligibility displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "membershipType": {
    "type": "string",
    "description": "Membership type"
   },
   "membershipTier": {
    "type": "string",
    "description": "Membership tier"
   },
   "membershipStatus": {
    "type": "string",
    "description": "Membership status"
   },
   "membershipStartDate": {
    "type": "string",
    "format": "date-time",
    "description": "Membership start date"
   },
   "renewalStatus": {
    "type": "string",
    "description": "Renewal status"
   },
   "expiryDate": {
    "type": "string",
    "format": "date-time",
    "description": "Expiry date"
   },
   "membershipTenure": {
    "type": "string",
    "description": "Membership tenure"
   },
   "loyaltyTier": {
    "type": "string",
    "description": "Loyalty tier"
   },
   "pointsBalance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Points balance"
   },
   "pointsEarned": {
    "type": "string",
    "description": "Points earned"
   },
   "pointsRedeemed": {
    "type": "string",
    "description": "Points redeemed"
   },
   "loyaltyActivity": {
    "type": "string",
    "description": "Loyalty activity"
   },
   "tierProgression": {
    "type": "string",
    "description": "Tier progression"
   },
   "guestCategories": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "adult",
      "child",
      "senior",
      "family",
      "student",
      "resident",
      "tourist",
      "group",
      "vip"
     ]
    },
    "description": "Guest categories that qualify."
   },
   "tierBenefits": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Benefit per loyalty tier, for example Bronze 5%, Silver 10%, Gold 15%"
   }
  }
 },
 "PartnerB2bPaymentEligibilityView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Partner, B2B & Payment Eligibility displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "partner": {
    "type": "string",
    "description": "Partner"
   },
   "partnerCategory": {
    "type": "string",
    "description": "Partner category"
   },
   "corporateAccount": {
    "type": "string",
    "description": "Corporate account"
   },
   "employer": {
    "type": "string",
    "description": "Employer"
   },
   "hotel": {
    "type": "string",
    "description": "Hotel"
   },
   "travelAgency": {
    "type": "string",
    "description": "Travel agency"
   },
   "tourOperator": {
    "type": "string",
    "description": "Tour operator"
   },
   "school": {
    "type": "string",
    "description": "School"
   },
   "governmentEntity": {
    "type": "string",
    "description": "Government entity"
   },
   "bank": {
    "type": "string",
    "description": "Bank"
   },
   "b2bAccount": {
    "type": "string",
    "description": "B2B account"
   },
   "masterAccount": {
    "type": "string",
    "description": "Master account"
   },
   "subAccount": {
    "type": "string",
    "description": "Sub-account"
   },
   "contract": {
    "type": "string",
    "description": "Contract"
   },
   "customerGroup": {
    "type": "string",
    "description": "Customer group"
   },
   "market": {
    "type": "string",
    "description": "Market"
   },
   "salesChannel": {
    "type": "string",
    "description": "Sales channel"
   },
   "paymentMethod": {
    "type": "string",
    "description": "Payment method"
   },
   "eligibleCardProgram": {
    "type": "string",
    "description": "Eligible card program"
   },
   "wallet": {
    "type": "string",
    "description": "Wallet"
   },
   "loyaltyPayment": {
    "type": "string",
    "description": "Loyalty payment"
   },
   "giftCard": {
    "type": "string",
    "description": "Gift card"
   },
   "approvedPaymentPartner": {
    "type": "integer",
    "description": "Approved payment partner"
   }
  }
 },
 "ResaleEligibilityRuleConfigurationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; lands in `orders.resale_eligibility_rule` (DM5, 29 September)",
  "description": "**What Resale Eligibility Rule Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "product": {
    "type": "string",
    "description": "Product"
   },
   "ticketType": {
    "type": "string",
    "description": "Ticket type"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "performance": {
    "type": "string",
    "description": "Performance"
   },
   "membershipType": {
    "type": "string",
    "description": "Membership type"
   },
   "salesChannel": {
    "type": "string",
    "description": "Sales channel"
   },
   "customerSegment": {
    "type": "string",
    "description": "Customer segment"
   },
   "priceCategory": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price category"
   },
   "promotion": {
    "type": "string",
    "description": "Promotion"
   },
   "ticketStatus": {
    "type": "string",
    "description": "Ticket status"
   },
   "paymentStatus": {
    "type": "string",
    "description": "Payment status"
   },
   "ticketOwnershipStatus": {
    "type": "string",
    "description": "Ticket ownership status"
   },
   "specificResaleStartEndDate": {
    "type": "string",
    "format": "date-time",
    "description": "Specific resale start/end date"
   },
   "blackoutPeriod": {
    "type": "string",
    "format": "date-time",
    "description": "Blackout period"
   },
   "maximumResaleAttempts": {
    "type": "integer",
    "description": "Maximum resale attempts"
   },
   "maximumListingsPerCustomer": {
    "type": "string",
    "description": "Maximum listings per customer"
   },
   "minimumOwnershipPeriod": {
    "type": "string",
    "format": "date-time",
    "description": "Minimum ownership period"
   },
   "identityVerificationRequirement": {
    "type": "string",
    "description": "Identity verification requirement"
   },
   "originalPurchaserOnly": {
    "type": "string",
    "description": "Original purchaser only"
   },
   "membershipRestriction": {
    "type": "string",
    "description": "Membership restriction"
   },
   "resaleImmediatelyAfterPurchase": {
    "type": "boolean",
    "description": "Allow resale immediately after purchase"
   },
   "requiredConditions": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "fullyPaid",
      "notScanned",
      "notExpired",
      "eventNotStarted",
      "notRefunded",
      "notComplimentary",
      "notStaff",
      "notInternal",
      "notBlocked",
      "notUnderDispute"
     ]
    },
    "description": "Conditions a ticket must meet to be listed."
   }
  }
 },
 "ResaleEligibilityRuleConfigurationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over orders state, assembled at read time from tables that already exist",
  "description": "**What Resale Eligibility Rule Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "product": {
    "type": "string",
    "description": "Product"
   },
   "ticketType": {
    "type": "string",
    "description": "Ticket type"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "performance": {
    "type": "string",
    "description": "Performance"
   },
   "membershipType": {
    "type": "string",
    "description": "Membership type"
   },
   "salesChannel": {
    "type": "string",
    "description": "Sales channel"
   },
   "customerSegment": {
    "type": "string",
    "description": "Customer segment"
   },
   "priceCategory": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price category"
   },
   "promotion": {
    "type": "string",
    "description": "Promotion"
   },
   "ticketStatus": {
    "type": "string",
    "description": "Ticket status"
   },
   "paymentStatus": {
    "type": "string",
    "description": "Payment status"
   },
   "ticketOwnershipStatus": {
    "type": "string",
    "description": "Ticket ownership status"
   },
   "specificResaleStartEndDate": {
    "type": "string",
    "format": "date-time",
    "description": "Specific resale start/end date"
   },
   "blackoutPeriod": {
    "type": "string",
    "format": "date-time",
    "description": "Blackout period"
   },
   "maximumResaleAttempts": {
    "type": "integer",
    "description": "Maximum resale attempts"
   },
   "maximumListingsPerCustomer": {
    "type": "string",
    "description": "Maximum listings per customer"
   },
   "minimumOwnershipPeriod": {
    "type": "string",
    "format": "date-time",
    "description": "Minimum ownership period"
   },
   "identityVerificationRequirement": {
    "type": "string",
    "description": "Identity verification requirement"
   },
   "originalPurchaserOnly": {
    "type": "string",
    "description": "Original purchaser only"
   },
   "membershipRestriction": {
    "type": "string",
    "description": "Membership restriction"
   },
   "resaleImmediatelyAfterPurchase": {
    "type": "boolean",
    "description": "Allow resale immediately after purchase"
   },
   "requiredConditions": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "fullyPaid",
      "notScanned",
      "notExpired",
      "eventNotStarted",
      "notRefunded",
      "notComplimentary",
      "notStaff",
      "notInternal",
      "notBlocked",
      "notUnderDispute"
     ]
    },
    "description": "Conditions a ticket must meet to be listed."
   }
  }
 },
 "TargetingConflictFrequencyExclusionControlsView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Targeting Conflict, Frequency & Exclusion Controls displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "maximumOffersPerDay": {
    "type": "string",
    "description": "Maximum offers per day"
   },
   "maximumOffersPerWeek": {
    "type": "string",
    "description": "Maximum offers per week"
   },
   "maximumCampaignsPerMonth": {
    "type": "string",
    "description": "Maximum campaigns per month"
   },
   "maximumRedemptions": {
    "type": "string",
    "description": "Maximum redemptions"
   },
   "coolingOffPeriod": {
    "type": "string",
    "format": "date-time",
    "description": "Cooling-off period"
   },
   "repeatCampaignRestriction": {
    "type": "string",
    "description": "Repeat campaign restriction"
   },
   "alreadyPurchasedProduct": {
    "type": "string",
    "description": "Already purchased product"
   },
   "alreadyRedeemedPromotion": {
    "type": "string",
    "description": "Already redeemed promotion"
   },
   "existingMember": {
    "type": "string",
    "description": "Existing member"
   },
   "employee": {
    "type": "string",
    "description": "Employee"
   },
   "specificCrmSegment": {
    "type": "string",
    "description": "Specific CRM segment"
   },
   "fraudRiskStatus": {
    "type": "string",
    "description": "Fraud/risk status"
   },
   "accountType": {
    "type": "string",
    "description": "Account type"
   },
   "partnerRestriction": {
    "type": "string",
    "description": "Partner restriction"
   },
   "productOwnership": {
    "type": "string",
    "description": "Product ownership"
   },
   "campaignExclusions": {
    "type": "string",
    "description": "Campaign exclusions"
   },
   "partnerExclusions": {
    "type": "string",
    "description": "Partner exclusions"
   },
   "operationalExclusions": {
    "type": "string",
    "description": "Operational exclusions"
   }
  }
 },
 "TargetingEligibilityCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over promotions state, assembled at read time from tables that already exist",
  "description": "**What Targeting & Eligibility Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "activeTargetingRules": {
    "type": "integer",
    "description": "Active Targeting Rules"
   },
   "activeSegments": {
    "type": "integer",
    "description": "Active Segments"
   },
   "promotionsUsingTargeting": {
    "type": "string",
    "description": "Promotions Using Targeting"
   },
   "bundlesUsingTargeting": {
    "type": "string",
    "description": "Bundles Using Targeting"
   },
   "eligibleCustomers": {
    "type": "integer",
    "description": "Eligible Customers"
   },
   "targetedCustomers": {
    "type": "integer",
    "description": "Targeted Customers"
   },
   "personalizedOffers": {
    "type": "integer",
    "description": "Personalized Offers"
   },
   "eligibilityPassRate": {
    "type": "number",
    "description": "Eligibility Pass Rate"
   },
   "conversionRate": {
    "type": "number",
    "description": "Conversion Rate"
   },
   "targetedRevenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Targeted Revenue"
   },
   "aovUplift": {
    "type": "number",
    "description": "AOV Uplift"
   },
   "aiRecommendedSegments": {
    "type": "integer",
    "description": "AI-Recommended Segments"
   },
   "ruleHealth": {
    "type": "string",
    "enum": [
     "healthy",
     "warning",
     "conflict",
     "noAudience",
     "oversizedAudience",
     "expired",
     "missingData"
    ],
    "description": "Health of the targeting rule."
   }
  }
 }
}
```
