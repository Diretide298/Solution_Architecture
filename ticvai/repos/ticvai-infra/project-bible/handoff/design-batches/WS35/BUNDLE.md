# WS35 — Pricing   Revenue Management board 2

**10 screens · 11 operations · 14 schemas · 1 permissions**

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

- **Every control that can be refused must be gated.** 1 permissions apply here:
  `PRODUCT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-058` | Pricing Rule Command Center | commandCentre | 3 | 0 | — |
| `ADM-059` | Customer Segment & Profile Pricing Rules | configEditor | 1 | 0 | — |
| `ADM-060` | Membership & Loyalty Pricing Rules | configEditor | 1 | 0 | — |
| `ADM-061` | Residency, Nationality & Market Pricing Rules | configEditor | 1 | 0 | — |
| `ADM-062` | Channel-Based Pricing Rules | listDetail | 1 | 0 | — |
| `ADM-063` | Location, Venue & Event Pricing Rules | configEditor | 1 | 0 | — |
| `ADM-064` | Quantity, Group & Volume Pricing Rules | listDetail | 1 | 0 | — |
| `ADM-065` | Effective Date, Season & Day-Based Pricing Rules | configEditor | 1 | 0 | — |
| `ADM-066` | Timeslot, Performance & Time-of-Day Pricing Rules | listDetail | 1 | 0 | — |
| `ADM-067` | Pricing Rule Priority, Conflict Resolution & Testing | listDetail | 3 | 0 | — |

## Thin screens in this batch

**ADM-062, ADM-064, ADM-066, ADM-067 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-058",
  "name": "Pricing Rule Command Center",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "2",
   "number": "10.2.1",
   "page": 23
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/pricing-rule-command-center-adm-058",
   "component": "apps/ticvai-web/src/routes/commercial/PricingRuleCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-059",
    "ADM-060",
    "ADM-061",
    "ADM-062",
    "ADM-063",
    "ADM-064",
    "ADM-065",
    "ADM-066",
    "ADM-067"
   ],
   "inferred": false,
   "notes": "**The board's hub.** The workshop specified this module as boards of ten and opened each with a command centre; the other nine screens are that board's detail, so they are reached from here and return here.",
   "transitions": [
    {
     "to": "ADM-002",
     "trigger": "Platform Dashboard",
     "provenance": "derived — ADM-002 declares entryState.params  and ADM-058 holds none of them. The edge carries nothing: ADM-058 is opened from ADM-002, so this edge is the way back and ADM-002 keeps its own state"
    },
    {
     "to": "ADM-059",
     "trigger": "Works in Customer Segment & Profile Pricing Rules",
     "provenance": "flow F144 step 1→2",
     "operation": "listPricingRule"
    },
    {
     "to": "ADM-060",
     "trigger": "Works in Membership & Loyalty Pricing Rules",
     "provenance": "flow F144 step 3→4",
     "operation": "listPricingRule"
    },
    {
     "to": "ADM-061",
     "trigger": "Works in Residency, Nationality & Market Pricing Rules",
     "provenance": "flow F144 step 5→6",
     "operation": "listPricingRule"
    },
    {
     "to": "ADM-062",
     "trigger": "Works in Channel-Based Pricing Rules",
     "provenance": "flow F144 step 7→8",
     "operation": "listPricingRule"
    },
    {
     "to": "ADM-063",
     "trigger": "Works in Location, Venue & Event Pricing Rules",
     "provenance": "flow F144 step 9→10",
     "operation": "listPricingRule"
    },
    {
     "to": "ADM-064",
     "trigger": "Works in Quantity, Group & Volume Pricing Rules",
     "provenance": "flow F144 step 11→12",
     "operation": "listPricingRule"
    },
    {
     "to": "ADM-065",
     "trigger": "Works in Effective Date, Season & Day-Based Pricing Rules",
     "provenance": "flow F144 step 13→14",
     "operation": "listPricingRule"
    },
    {
     "to": "ADM-066",
     "trigger": "Works in Timeslot, Performance & Time-of-Day Pricing Rules",
     "provenance": "flow F144 step 15→16",
     "operation": "listPricingRule"
    },
    {
     "to": "ADM-067",
     "trigger": "Works in Pricing Rule Priority, Conflict Resolution & Testing",
     "provenance": "flow F144 step 17→18",
     "operation": "listPricingRule",
     "carries": [
      "ruleId"
     ]
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Administrators can identify, search, and manage all contextual pricing rules from one workspace.",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each rule should show) — counts over a population, then the population",
  "purpose": "Provide administrators with a centralized workspace for all pricing eligibility and contextual pricing rules.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 13 actions on this screen and the screen declares 1 operation.** Unserved: Customer Segment, Membership, Channel, Quantity, Timeslot, Event, Create Rule, Duplicate …. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 23 §Support"
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
       "label": "Active Pricing Rules",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 23 §Display",
       "bindsTo": "PricingRuleCommandCenterSummary.activePricingRules"
      },
      {
       "kind": "metricTile",
       "label": "Draft Rules",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 23 §Display",
       "bindsTo": "PricingRuleCommandCenterSummary.draftRules"
      },
      {
       "kind": "metricTile",
       "label": "Customer Segment Rules",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 23 §Display",
       "bindsTo": "PricingRuleCommandCenterSummary.customerSegmentRules"
      },
      {
       "kind": "metricTile",
       "label": "Membership Rules",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 23 §Display",
       "bindsTo": "PricingRuleCommandCenterSummary.membershipRules"
      },
      {
       "kind": "metricTile",
       "label": "Residency Rules",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 23 §Display",
       "bindsTo": "PricingRuleCommandCenterSummary.residencyRules"
      },
      {
       "kind": "metricTile",
       "label": "Channel Rules",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 23 §Display",
       "bindsTo": "PricingRuleCommandCenterSummary.channelRules"
      },
      {
       "kind": "metricTile",
       "label": "Location Rules",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 23 §Display",
       "bindsTo": "PricingRuleCommandCenterSummary.locationRules"
      },
      {
       "kind": "metricTile",
       "label": "Quantity Rules",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 23 §Display",
       "bindsTo": "PricingRuleCommandCenterSummary.quantityRules"
      },
      {
       "kind": "metricTile",
       "label": "Seasonal Rules",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 23 §Display",
       "bindsTo": "PricingRuleCommandCenterSummary.seasonalRules"
      },
      {
       "kind": "metricTile",
       "label": "Timeslot Rules",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 23 §Display",
       "bindsTo": "PricingRuleCommandCenterSummary.timeslotRules"
      },
      {
       "kind": "metricTile",
       "label": "Rule Conflicts",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 23 §Display",
       "bindsTo": "PricingRuleCommandCenterSummary.ruleConflicts"
      },
      {
       "kind": "metricTile",
       "label": "Rules Expiring Soon",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 23 §Display",
       "bindsTo": "PricingRuleCommandCenterSummary.rulesExpiringSoon"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every pricing rule",
       "columns": [
        "PricingRuleCommandCenterView.ruleId",
        "PricingRuleCommandCenterView.ruleName",
        "PricingRuleCommandCenterView.ruleType",
        "PricingRuleCommandCenterView.priceList",
        "PricingRuleCommandCenterView.productScope",
        "PricingRuleCommandCenterView.customerScope",
        "PricingRuleCommandCenterView.channel",
        "PricingRuleCommandCenterView.venueLocation",
        "PricingRuleCommandCenterView.effectiveFrom",
        "PricingRuleCommandCenterView.effectiveTo",
        "PricingRuleCommandCenterView.priority",
        "PricingRuleCommandCenterView.status",
        "PricingRuleCommandCenterView.owner"
       ],
       "bindsTo": "PricingRuleCommandCenterView",
       "operation": "listPricingRule",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 23 §Each rule should show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected pricing rule",
       "bindsTo": "PricingRuleCommandCenterView",
       "columns": [
        "PricingRuleCommandCenterView.ruleId",
        "PricingRuleCommandCenterView.ruleName",
        "PricingRuleCommandCenterView.ruleType",
        "PricingRuleCommandCenterView.priceList",
        "PricingRuleCommandCenterView.productScope",
        "PricingRuleCommandCenterView.customerScope",
        "PricingRuleCommandCenterView.channel",
        "PricingRuleCommandCenterView.venueLocation",
        "PricingRuleCommandCenterView.effectiveFrom",
        "PricingRuleCommandCenterView.effectiveTo",
        "PricingRuleCommandCenterView.priority",
        "PricingRuleCommandCenterView.status",
        "PricingRuleCommandCenterView.owner"
       ],
       "notes": null,
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 23 §Each rule should show"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Customer Segment",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 23 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Membership",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 23 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Channel",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 23 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Quantity",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 23 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Timeslot",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 23 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Event",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 23 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Create Rule",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 23 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Duplicate",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 23 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Test Rule",
       "operation": "testPricingRule",
       "provenance": "contract catalogue.yaml POST /pricing-rule/{ruleId}/test (decided 29 September, readiness close-out)"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The pricing rule list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the pricing rule untouched.",
   "emptyFirstRun": "No pricing rule yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the pricing rule are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPricingRule",
    "contract": "catalogue",
    "purpose": "Pricing Rule Command Center",
    "trigger": "onLoad"
   },
   {
    "operationId": "listPricingRulePriority",
    "contract": "catalogue",
    "purpose": "Pricing Rule Priority, Conflict Resolution & Testing",
    "trigger": "onLoad"
   },
   {
    "operationId": "testPricingRule",
    "contract": "catalogue",
    "purpose": "Test one pricing rule against a sample booking, on demand",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-058",
   "workshopBoard": "wireframes/WS96 Pricing   Revenue Management Board 2.dc.html#adm-058"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 23. 25 of 25 labels bound to a contract property; 38 of 52 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "ruleId",
     "from": "navigation"
    }
   ]
  },
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
  "id": "ADM-059",
  "name": "Customer Segment & Profile Pricing Rules",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "2",
   "number": "10.2.2",
   "page": 25
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/customer-segment-profile-pricing-rules-adm-059",
   "component": "apps/ticvai-web/src/routes/commercial/CustomerSegmentProfilePricingRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-058"
   ],
   "exitTo": [
    "ADM-058"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-058, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-058",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F144 step 2→3",
     "operation": "listCustomerSegmentProfile",
     "carries": [
      "ruleId"
     ]
    }
   ]
  },
  "density": "compact",
  "purposeNote": "segmentation.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure by; Capture) and no display directory — it is settings, not a population",
  "purpose": "Define price eligibility based on customer characteristics and commercial segments.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Customer Type",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 25 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Customer Segment",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 25 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Account Type",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 25 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "CRM Segment",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 25 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "VIP Status",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 25 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Corporate Customer",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 25 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Employee/Staff",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 25 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Partner Customer",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 25 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Guest/Registered User",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 25 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Rule Name",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 25 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Segment",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 25 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Applicable Products",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 25 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Price List",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 25 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Rate",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 25 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Priority",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 25 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Effective Dates",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 25 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Status",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 25 §Capture"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The customer segment profile configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the customer segment profile untouched.",
   "emptyFirstRun": "No customer segment profile configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCustomerSegmentProfile",
    "contract": "catalogue",
    "purpose": "Customer Segment & Profile Pricing Rules",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-059",
   "workshopBoard": "wireframes/WS96 Pricing   Revenue Management Board 2.dc.html#adm-059"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 25. 0 of 0 labels bound to a contract property; 17 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-060",
  "name": "Membership & Loyalty Pricing Rules",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "2",
   "number": "10.2.3",
   "page": 26
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/membership-loyalty-pricing-rules-adm-060",
   "component": "apps/ticvai-web/src/routes/commercial/MembershipLoyaltyPricingRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-058"
   ],
   "exitTo": [
    "ADM-058"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-058, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-058",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F144 step 4→5",
     "operation": "listMembershipLoyaltyPricing",
     "carries": [
      "ruleId"
     ]
    }
   ]
  },
  "density": "compact",
  "purposeNote": "entitlement logic.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure whether benefits apply to) and no display directory — it is settings, not a population",
  "purpose": "Control member-specific and loyalty-tier pricing.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 6 actions on this screen and the screen declares 1 operation.** Unserved: Customer Status. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 26 §Support"
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
       "label": "Member Only",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 26 §Configure whether benefits apply to"
      },
      {
       "kind": "textField",
       "label": "Member + 1 Guest",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 26 §Configure whether benefits apply to"
      },
      {
       "kind": "selectField",
       "label": "Member + Family",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 26 §Configure whether benefits apply to"
      },
      {
       "kind": "selectField",
       "label": "Selected Quantity",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 26 §Configure whether benefits apply to"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Membership Product",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 26 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Membership Status",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 26 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Membership Tier",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 26 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Membership Level",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 26 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Loyalty Tier",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 26 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Customer Status",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 26 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The membership loyalty pricing configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the membership loyalty pricing untouched.",
   "emptyFirstRun": "No membership loyalty pricing configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listMembershipLoyaltyPricing",
    "contract": "catalogue",
    "purpose": "Membership & Loyalty Pricing Rules",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-060",
   "workshopBoard": "wireframes/WS96 Pricing   Revenue Management Board 2.dc.html#adm-060"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 26. 0 of 0 labels bound to a contract property; 10 of 31 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-061",
  "name": "Residency, Nationality & Market Pricing Rules",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "2",
   "number": "10.2.4",
   "page": 27
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/residency-nationality-market-pricing-rules-adm-061",
   "component": "apps/ticvai-web/src/routes/commercial/ResidencyNationalityMarketPricingRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-058"
   ],
   "exitTo": [
    "ADM-058"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-058, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-058",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F144 step 6→7",
     "operation": "listResidencyNationalityMarket",
     "carries": [
      "ruleId"
     ]
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Residency, nationality, and market-specific pricing can be applied only when the configured eligibility criteria are satisfied.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure by; Configure whether eligibility requires) and no display directory — it is settings, not a population",
  "purpose": "Support geographically differentiated commercial pricing.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Residency",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 27 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Nationality",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 27 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Country",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 27 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Market",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 27 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Region",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 27 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Customer Address",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 27 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Verified ID",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 27 §Configure by"
      },
      {
       "kind": "textField",
       "label": "Government ID Integration where applicable",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 27 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Customer Declaration",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 27 §Configure whether eligibility requires"
      },
      {
       "kind": "selectField",
       "label": "Account Profile",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 27 §Configure whether eligibility requires"
      },
      {
       "kind": "selectField",
       "label": "ID Upload",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 27 §Configure whether eligibility requires"
      },
      {
       "kind": "selectField",
       "label": "Government/Identity Verification",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 27 §Configure whether eligibility requires"
      },
      {
       "kind": "selectField",
       "label": "Staff Verification",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 27 §Configure whether eligibility requires"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The residency nationality market configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the residency nationality market untouched.",
   "emptyFirstRun": "No residency nationality market configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listResidencyNationalityMarket",
    "contract": "catalogue",
    "purpose": "Residency, Nationality & Market Pricing Rules",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-061",
   "workshopBoard": "wireframes/WS96 Pricing   Revenue Management Board 2.dc.html#adm-061"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 27. 0 of 0 labels bound to a contract property; 13 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-062",
  "name": "Channel-Based Pricing Rules",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "2",
   "number": "10.2.5",
   "page": 29
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/channel-based-pricing-rules-adm-062",
   "component": "apps/ticvai-web/src/routes/commercial/ChannelBasedPricingRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-058"
   ],
   "exitTo": [
    "ADM-058"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-058, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-058",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F144 step 8→9",
     "operation": "listChannelBasedPricing",
     "carries": [
      "ruleId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Determine which commercial rate applies based on sales channel.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 29"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 29"
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
       "impliedBy": "listChannelBasedPricing",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The channel-based pricing rules list.",
   "error": "Could not load. Names which read failed and leaves the channel-based pricing rules untouched.",
   "emptyFirstRun": "No channel-based pricing rules yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the channel-based pricing rules are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listChannelBasedPricing",
    "contract": "catalogue",
    "purpose": "Channel-Based Pricing Rules",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-062",
   "workshopBoard": "wireframes/WS96 Pricing   Revenue Management Board 2.dc.html#adm-062"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 29. 0 of 0 labels bound to a contract property; 0 of 12 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-063",
  "name": "Location, Venue & Event Pricing Rules",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "2",
   "number": "10.2.6",
   "page": 30
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/location-venue-event-pricing-rules-adm-063",
   "component": "apps/ticvai-web/src/routes/commercial/LocationVenueEventPricingRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-058"
   ],
   "exitTo": [
    "ADM-058"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-058, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-058",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F144 step 10→11",
     "operation": "listLocationVenueEvent",
     "carries": [
      "ruleId"
     ]
    }
   ]
  },
  "density": "compact",
  "purposeNote": "event, or performance context.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Allow rates to vary according to where and for which event/experience the product is sold.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 7 actions on this screen and the screen declares 1 operation.** Unserved: Attraction, Zone, Experience, Pop-up Venue, Temporary Event Location. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 30 §Support"
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
       "label": "Venue",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 30 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Event",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 30 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Product",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 30 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Rate",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 30 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Effective Dates",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 30 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Priority",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 30 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Venue",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 30 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Attraction",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 30 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Event",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 30 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Zone",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 30 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Experience",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 30 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Pop-up Venue",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 30 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Temporary Event Location",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 30 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The location venue event configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the location venue event untouched.",
   "emptyFirstRun": "No location venue event configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listLocationVenueEvent",
    "contract": "catalogue",
    "purpose": "Location, Venue & Event Pricing Rules",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-063",
   "workshopBoard": "wireframes/WS96 Pricing   Revenue Management Board 2.dc.html#adm-063"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 30. 0 of 0 labels bound to a contract property; 13 of 29 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-064",
  "name": "Quantity, Group & Volume Pricing Rules",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "2",
   "number": "10.2.7",
   "page": 31
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/quantity-group-volume-pricing-rules-adm-064",
   "component": "apps/ticvai-web/src/routes/commercial/QuantityGroupVolumePricingRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-058"
   ],
   "exitTo": [
    "ADM-058"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-058, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-058",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F144 step 12→13",
     "operation": "listQuantityGroupVolume",
     "carries": [
      "ruleId"
     ]
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Support commercial rates based on purchased quantity or group size.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 2 actions on this screen and the screen declares 1 operation.** Unserved: Minimum Quantity. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 31 §Support"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 31"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 31"
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
       "label": "Minimum Quantity",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 31 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Quantity Bands",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 31 §Support"
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
   "loading": "The quantity group volume list.",
   "error": "Could not load. Names which read failed and leaves the quantity group volume untouched.",
   "emptyFirstRun": "No quantity group volume yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the quantity group volume are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listQuantityGroupVolume",
    "contract": "catalogue",
    "purpose": "Quantity, Group & Volume Pricing Rules",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "QuantityGroupVolumePricingRulesView.quantityModel"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-064",
   "workshopBoard": "wireframes/WS96 Pricing   Revenue Management Board 2.dc.html#adm-064"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 31. 0 of 0 labels bound to a contract property; 2 of 7 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-065",
  "name": "Effective Date, Season & Day-Based Pricing Rules",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "2",
   "number": "10.2.8",
   "page": 32
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/effective-date-season-day-based-pricing-rules-adm-065",
   "component": "apps/ticvai-web/src/routes/commercial/EffectiveDateSeasonDayBasedPricingRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-058"
   ],
   "exitTo": [
    "ADM-058"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-058, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-058",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F144 step 14→15",
     "operation": "listEffectiveDateSeason",
     "carries": [
      "ruleId"
     ]
    }
   ]
  },
  "density": "compact",
  "purposeNote": "day-based rules.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Control commercial price selection over time.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Effective From",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 32 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Effective To",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 32 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Sales Start",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 32 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Sales End",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 32 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Visit Date Range",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 32 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Season",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 32 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Holiday Period",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 32 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Event Period",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 32 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The effective date season configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the effective date season untouched.",
   "emptyFirstRun": "No effective date season configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listEffectiveDateSeason",
    "contract": "catalogue",
    "purpose": "Effective Date, Season & Day-Based Pricing Rules",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-065",
   "workshopBoard": "wireframes/WS96 Pricing   Revenue Management Board 2.dc.html#adm-065"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 32. 0 of 0 labels bound to a contract property; 8 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-066",
  "name": "Timeslot, Performance & Time-of-Day Pricing Rules",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "2",
   "number": "10.2.9",
   "page": 33
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/timeslot-performance-time-of-day-pricing-rules-adm-066",
   "component": "apps/ticvai-web/src/routes/commercial/TimeslotPerformanceTimeOfDayPricingRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-058"
   ],
   "exitTo": [
    "ADM-058"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-058, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-058",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F144 step 16→17",
     "operation": "listTimeslotPerformanceTime",
     "carries": [
      "ruleId"
     ]
    }
   ]
  },
  "density": "compact",
  "purposeNote": "time-of-day context.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Detect) and no metric row",
  "purpose": "Allow commercial pricing to differ across times within the same day or event.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every timeslot performance time-of-day",
       "columns": [
        "TimeslotPerformanceTimeOfDayPricingRulesView.validationIssues"
       ],
       "bindsTo": "TimeslotPerformanceTimeOfDayPricingRulesView",
       "operation": "listTimeslotPerformanceTime",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 33 §Detect"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected timeslot performance time-of-day",
       "bindsTo": "TimeslotPerformanceTimeOfDayPricingRulesView",
       "columns": [
        "TimeslotPerformanceTimeOfDayPricingRulesView.validationIssues"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Supported Contexts”, “Museum Admission”, “Concert”.",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 33 §Detect"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The timeslot performance time-of-day list.",
   "error": "Could not load. Names which read failed and leaves the timeslot performance time-of-day untouched.",
   "emptyFirstRun": "No timeslot performance time-of-day yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the timeslot performance time-of-day are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listTimeslotPerformanceTime",
    "contract": "catalogue",
    "purpose": "Timeslot, Performance & Time-of-Day Pricing Rules",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "TimeslotPerformanceTimeOfDayPricingRulesView.validationIssues"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-066",
   "workshopBoard": "wireframes/WS96 Pricing   Revenue Management Board 2.dc.html#adm-066"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 33. 3 of 3 labels bound to a contract property; 17 of 31 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-067",
  "name": "Pricing Rule Priority, Conflict Resolution & Testing",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "2",
   "number": "10.2.10",
   "page": 34
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/pricing-rule-priority-conflict-resolution-testing-adm-067",
   "component": "apps/ticvai-web/src/routes/commercial/PricingRulePriorityConflictResolutionTesting.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-058"
   ],
   "exitTo": [
    "ADM-058"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-058, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-058",
     "trigger": "Pricing Rule Command Center",
     "carries": [
      "ruleId"
     ],
     "provenance": "derived — ADM-058 declares entryState.params ruleId and ADM-067 holds ruleId, so an edge into it carries them"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "For any commercial transaction, TICVAI can deterministically resolve and explain exactly why a specific rate was selected. Board 2 — Final Screen Register",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Identify; Show) and no metric row",
  "purpose": "Define how TICVAI decides the final applicable rate when multiple pricing rules match. This is the critical control screen for Board 2. Board 1 established what commercial prices exist. Board 2 determines which commercial rate applies to a transaction.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every pricing rule priority",
       "columns": [
        "PricingRulePriorityConflictResolutionTestingView.validationIssues"
       ],
       "bindsTo": "PricingRulePriorityConflictResolutionTestingView",
       "operation": "listPricingRulePriority",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 34 §Identify"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected pricing rule priority",
       "bindsTo": "PricingRulePriorityConflictResolutionTestingView",
       "columns": [
        "PricingRulePriorityConflictResolutionTestingView.validationIssues"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Standard Rate”, “Inputs”, “Input”, “Candidate Rates”, “Resolved Rate”, “Reason”.",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 34 §Identify"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Test Rule",
       "operation": "testPricingRule",
       "provenance": "contract catalogue.yaml POST /pricing-rule/{ruleId}/test (decided 29 September, readiness close-out)"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The pricing rule priority list.",
   "error": "Could not load. Names which read failed and leaves the pricing rule priority untouched.",
   "emptyFirstRun": "No pricing rule priority yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the pricing rule priority are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPricingRulePriority",
    "contract": "catalogue",
    "purpose": "Pricing Rule Priority, Conflict Resolution & Testing",
    "trigger": "onLoad"
   },
   {
    "operationId": "listPricingRule",
    "contract": "catalogue",
    "purpose": "The pricing rules to pick one to test",
    "trigger": "onLoad"
   },
   {
    "operationId": "testPricingRule",
    "contract": "catalogue",
    "purpose": "Test one pricing rule against a sample booking, on demand",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "preloaded": [
    "PricingRulePriorityConflictResolutionTestingView.validationIssues"
   ],
   "params": [
    {
     "name": "ruleId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-067",
   "workshopBoard": "wireframes/WS96 Pricing   Revenue Management Board 2.dc.html#adm-067"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 34. 6 of 6 labels bound to a contract property; 6 of 102 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "listChannelBasedPricing": {
  "method": "GET",
  "path": "/channel-based-pricing",
  "contract": "catalogue",
  "summary": "Channel-Based Pricing Rules",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "channel",
    "in": "query",
    "required": false
   },
   {
    "name": "product",
    "in": "query",
    "required": false
   },
   {
    "name": "isOverride",
    "in": "query",
    "required": false
   },
   {
    "name": "status",
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
 "listCustomerSegmentProfile": {
  "method": "GET",
  "path": "/customer-segment-profile",
  "contract": "catalogue",
  "summary": "Customer Segment & Profile Pricing Rules",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "dimension",
    "in": "query",
    "required": false
   },
   {
    "name": "segmentSource",
    "in": "query",
    "required": false
   },
   {
    "name": "customerId",
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
 "listEffectiveDateSeason": {
  "method": "GET",
  "path": "/effective-date-season",
  "contract": "catalogue",
  "summary": "Effective Date, Season & Day-Based Pricing Rules",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "dateRuleType",
    "in": "query",
    "required": false
   },
   {
    "name": "visitFrom",
    "in": "query",
    "required": false
   },
   {
    "name": "visitTo",
    "in": "query",
    "required": false
   },
   {
    "name": "product",
    "in": "query",
    "required": false
   },
   {
    "name": "status",
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
 "listLocationVenueEvent": {
  "method": "GET",
  "path": "/location-venue-event",
  "contract": "catalogue",
  "summary": "Location, Venue & Event Pricing Rules",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "contextLevel",
    "in": "query",
    "required": false
   },
   {
    "name": "contextRefId",
    "in": "query",
    "required": false
   },
   {
    "name": "status",
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
 "listMembershipLoyaltyPricing": {
  "method": "GET",
  "path": "/membership-loyalty-pricing",
  "contract": "catalogue",
  "summary": "Membership & Loyalty Pricing Rules",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "dimension",
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
 "listPricingRule": {
  "method": "GET",
  "path": "/pricing-rule",
  "contract": "catalogue",
  "summary": "Pricing Rule Command Center",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "ruleType",
    "in": "query",
    "required": false
   },
   {
    "name": "status",
    "in": "query",
    "required": false
   },
   {
    "name": "channel",
    "in": "query",
    "required": false
   },
   {
    "name": "venueLocation",
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
 "listPricingRulePriority": {
  "method": "GET",
  "path": "/pricing-rule-priority",
  "contract": "catalogue",
  "summary": "Pricing Rule Priority, Conflict Resolution & Testing",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "ruleType",
    "in": "query",
    "required": false
   },
   {
    "name": "hasConflict",
    "in": "query",
    "required": false
   },
   {
    "name": "customerId",
    "in": "query",
    "required": false
   },
   {
    "name": "membershipId",
    "in": "query",
    "required": false
   },
   {
    "name": "residency",
    "in": "query",
    "required": false
   },
   {
    "name": "productId",
    "in": "query",
    "required": false
   },
   {
    "name": "quantity",
    "in": "query",
    "required": false
   },
   {
    "name": "venueId",
    "in": "query",
    "required": false
   },
   {
    "name": "channel",
    "in": "query",
    "required": false
   },
   {
    "name": "date",
    "in": "query",
    "required": false
   },
   {
    "name": "time",
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
 "listQuantityGroupVolume": {
  "method": "GET",
  "path": "/quantity-group-volume",
  "contract": "catalogue",
  "summary": "Quantity, Group & Volume Pricing Rules",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "quantityModel",
    "in": "query",
    "required": false
   },
   {
    "name": "groupType",
    "in": "query",
    "required": false
   },
   {
    "name": "status",
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
 "listResidencyNationalityMarket": {
  "method": "GET",
  "path": "/residency-nationality-market",
  "contract": "catalogue",
  "summary": "Residency, Nationality & Market Pricing Rules",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "eligibilityBasis",
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
 "listTimeslotPerformanceTime": {
  "method": "GET",
  "path": "/timeslot-performance-time",
  "contract": "catalogue",
  "summary": "Timeslot, Performance & Time-of-Day Pricing Rules",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "event",
    "in": "query",
    "required": false
   },
   {
    "name": "timeOfDayBand",
    "in": "query",
    "required": false
   },
   {
    "name": "status",
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
 "testPricingRule": {
  "method": "POST",
  "path": "/pricing-rule/{ruleId}/test",
  "contract": "catalogue",
  "summary": "Test one pricing rule against a sample booking, on demand",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "PricingRuleTestInput",
  "responds": "PricingRuleTestResult"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "ChannelBasedPricingRulesView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Channel-Based Pricing Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "channel": {
    "$ref": "../shared/common.yaml#/components/schemas/SalesChannel",
    "description": "Channel (Supported Channels, p.29)"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "priceList": {
    "type": "string",
    "description": "Price List"
   },
   "rate": {
    "type": "string",
    "description": "Rate: code of the rate, e.g. Trade Adult"
   },
   "market": {
    "type": "string",
    "description": "Market"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "priority": {
    "type": "integer",
    "description": "Priority within the configurable pricing hierarchy (MoM 1 Sep §4.4): the lower number wins"
   },
   "ruleId": {
    "type": "string",
    "description": "Rule ID"
   },
   "ruleName": {
    "type": "string",
    "description": "Rule Name"
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date",
    "description": "Effective From"
   },
   "effectiveTo": {
    "type": "string",
    "format": "date",
    "description": "Effective To; empty for open-ended",
    "nullable": true
   },
   "isOverride": {
    "type": "boolean",
    "description": "Channel Override (pp.29-30): a controlled, time-boxed override of the channel's normal rate"
   },
   "overrideReason": {
    "type": "string",
    "nullable": true,
    "description": "Reason, required for an override"
   },
   "fallbackRate": {
    "type": "string",
    "nullable": true,
    "description": "Fallback Rate once the override ends"
   },
   "status": {
    "type": "string",
    "description": "Status: draft, active, disabled or expired"
   }
  }
 },
 "CustomerSegmentProfilePricingRulesView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Customer Segment & Profile Pricing Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "ruleName": {
    "type": "string",
    "description": "Rule Name"
   },
   "segment": {
    "type": "string",
    "description": "Segment: the value the dimension must equal, e.g. VIP"
   },
   "applicableProducts": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Applicable Products: product ids or product category codes"
   },
   "priceList": {
    "type": "string",
    "description": "Price List: the list whose rate the rule selects"
   },
   "rate": {
    "type": "string",
    "description": "Rate: code of the rate used when the rule matches, e.g. VIP Adult"
   },
   "priority": {
    "type": "integer",
    "description": "Priority within the configurable pricing hierarchy (MoM 1 Sep §4.4): the lower number wins"
   },
   "status": {
    "type": "string",
    "description": "Status: draft, active, disabled or expired"
   },
   "ruleId": {
    "type": "string",
    "description": "Rule ID"
   },
   "dimension": {
    "type": "string",
    "enum": [
     "customerType",
     "customerSegment",
     "accountType",
     "crmSegment",
     "vipStatus",
     "corporateCustomer",
     "employeeStaff",
     "partnerCustomer",
     "guestRegisteredUser"
    ],
    "description": "Supported Dimension (p.25) the rule tests"
   },
   "segmentSource": {
    "type": "string",
    "enum": [
     "crm",
     "membership",
     "b2bPartner",
     "corporateAccount",
     "customerProfile"
    ],
    "description": "Customer Segment Source (p.26) the segment is read from"
   },
   "fallbackRate": {
    "type": "string",
    "description": "Fallback (p.26): rate used when the customer no longer qualifies; the standard rate by default (decided 29 September, readiness close-out)"
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date",
    "description": "Effective From"
   },
   "effectiveTo": {
    "type": "string",
    "format": "date",
    "description": "Effective To; empty for open-ended",
    "nullable": true
   }
  }
 },
 "EffectiveDateSeasonDayBasedPricingRulesView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Effective Date, Season & Day-Based Pricing Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "effectiveFrom": {
    "type": "string",
    "format": "date",
    "description": "Effective From"
   },
   "effectiveTo": {
    "type": "string",
    "format": "date",
    "description": "Effective To; empty for open-ended",
    "nullable": true
   },
   "salesStart": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "Sales Start: purchases from this moment get the rule"
   },
   "salesEnd": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "Sales End"
   },
   "season": {
    "type": "string",
    "nullable": true,
    "description": "Season name, e.g. Low, Regular, Peak (Seasonal Pricing, p.33)"
   },
   "ruleId": {
    "type": "string",
    "description": "Rule ID"
   },
   "ruleName": {
    "type": "string",
    "description": "Rule Name"
   },
   "dateRuleType": {
    "type": "string",
    "enum": [
     "effectivePeriod",
     "season",
     "dayOfWeek",
     "holidayPeriod",
     "eventPeriod",
     "publicHoliday",
     "schoolHoliday",
     "specialDate",
     "blackoutDate",
     "peakDate"
    ],
    "description": "Kind of date rule (Effective Dating and Calendar Rules, pp.32-33)"
   },
   "visitFrom": {
    "type": "string",
    "format": "date",
    "description": "Visit Date Range start",
    "nullable": true
   },
   "visitTo": {
    "type": "string",
    "format": "date",
    "description": "Visit Date Range end",
    "nullable": true
   },
   "daysOfWeek": {
    "type": "array",
    "items": {
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
    "description": "Day-of-Week Pricing (p.33); empty for every day"
   },
   "specificDates": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "date"
    },
    "description": "Special, blackout, peak or holiday dates the rule covers"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "priceList": {
    "type": "string",
    "description": "Price List"
   },
   "rate": {
    "type": "string",
    "description": "Rate code"
   },
   "priority": {
    "type": "integer",
    "description": "Priority within the configurable pricing hierarchy (MoM 1 Sep §4.4): the lower number wins"
   },
   "status": {
    "type": "string",
    "description": "Status: draft, active, disabled or expired"
   },
   "validationIssues": {
    "type": "array",
    "description": "Overlap Detection (p.33), e.g. Peak Season and Public Holiday overlap with different rates",
    "items": {
     "type": "object",
     "properties": {
      "code": {
       "type": "string",
       "enum": [
        "overlappingRules"
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
 "LocationVenueEventPricingRulesView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Location, Venue & Event Pricing Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "product": {
    "type": "string",
    "description": "Product"
   },
   "rate": {
    "type": "string",
    "description": "Rate: code of the rate used in this context"
   },
   "priority": {
    "type": "integer",
    "description": "Priority within the configurable pricing hierarchy (MoM 1 Sep §4.4): the lower number wins"
   },
   "ruleId": {
    "type": "string",
    "description": "Rule ID"
   },
   "ruleName": {
    "type": "string",
    "description": "Rule Name"
   },
   "contextLevel": {
    "type": "string",
    "enum": [
     "country",
     "city",
     "venue",
     "attraction",
     "location",
     "event",
     "performance",
     "zone",
     "experience"
    ],
    "description": "Pricing Context (p.30) the rule is keyed on"
   },
   "contextRefId": {
    "type": "string",
    "description": "The country, city, venue, attraction, location, event, performance, zone or experience"
   },
   "temporaryLocationType": {
    "type": "string",
    "enum": [
     "popUpVenue",
     "exhibition",
     "seasonalSite",
     "temporaryEventLocation"
    ],
    "description": "Temporary Location Pricing (p.30); empty for a permanent location",
    "nullable": true
   },
   "priceList": {
    "type": "string",
    "description": "Price List"
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date",
    "description": "Effective From"
   },
   "effectiveTo": {
    "type": "string",
    "format": "date",
    "description": "Effective To; empty for open-ended",
    "nullable": true
   },
   "status": {
    "type": "string",
    "description": "Status: draft, active, disabled or expired"
   }
  }
 },
 "MembershipLoyaltyPricingRulesView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Membership & Loyalty Pricing Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "ruleId": {
    "type": "string",
    "description": "Rule ID"
   },
   "ruleName": {
    "type": "string",
    "description": "Rule Name"
   },
   "conditions": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "dimension": {
       "type": "string",
       "enum": [
        "membershipProduct",
        "membershipStatus",
        "membershipTier",
        "annualPassType",
        "membershipLevel",
        "loyaltyTier",
        "loyaltyProgram",
        "pointsBand",
        "customerStatus"
       ]
      },
      "value": {
       "type": "string",
       "description": "e.g. active, Gold, Platinum"
      }
     }
    },
    "description": "Conditions, all of which must hold (Membership = Active AND Tier = Gold)"
   },
   "priceList": {
    "type": "string",
    "description": "Price List"
   },
   "rate": {
    "type": "string",
    "description": "Rate: code of the rate used when the rule matches, e.g. Gold Member Rate"
   },
   "benefitScope": {
    "type": "string",
    "enum": [
     "memberOnly",
     "memberPlusOneGuest",
     "memberPlusFamily",
     "selectedQuantity"
    ],
    "description": "Member + Guest Rules (p.27): who in the booking receives the member rate"
   },
   "benefitQuantity": {
    "type": "integer",
    "nullable": true,
    "description": "Number of tickets at the member rate when benefitScope is selectedQuantity"
   },
   "priority": {
    "type": "integer",
    "description": "Priority within the configurable pricing hierarchy (MoM 1 Sep §4.4): the lower number wins"
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date",
    "description": "Effective From"
   },
   "effectiveTo": {
    "type": "string",
    "format": "date",
    "description": "Effective To; empty for open-ended",
    "nullable": true
   },
   "status": {
    "type": "string",
    "description": "Status: draft, active, disabled or expired"
   },
   "validationIssues": {
    "type": "array",
    "description": "Validation (p.27)",
    "items": {
     "type": "object",
     "properties": {
      "code": {
       "type": "string",
       "enum": [
        "inactiveMembership",
        "expiredMembership",
        "missingTierRate",
        "conflictingLoyaltyMemberRates"
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
 "PricingRuleCommandCenterSummary": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection; the headline tiles over the list, computed at read time for the filters in force",
  "description": "**The headline figures on Pricing Rule Command Center.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.",
  "properties": {
   "activePricingRules": {
    "type": "integer",
    "description": "Active Pricing Rules"
   },
   "draftRules": {
    "type": "integer",
    "description": "Draft Rules"
   },
   "customerSegmentRules": {
    "type": "integer",
    "description": "Customer Segment Rules"
   },
   "membershipRules": {
    "type": "integer",
    "description": "Membership Rules"
   },
   "residencyRules": {
    "type": "integer",
    "description": "Residency Rules"
   },
   "channelRules": {
    "type": "integer",
    "description": "Channel Rules"
   },
   "locationRules": {
    "type": "integer",
    "description": "Location Rules"
   },
   "quantityRules": {
    "type": "integer",
    "description": "Quantity Rules"
   },
   "seasonalRules": {
    "type": "integer",
    "description": "Seasonal Rules"
   },
   "timeslotRules": {
    "type": "integer",
    "description": "Timeslot Rules"
   },
   "ruleConflicts": {
    "type": "integer",
    "description": "Rule Conflicts"
   },
   "rulesExpiringSoon": {
    "type": "integer",
    "description": "Rules Expiring Soon: active rules whose effective-to date falls within the next 30 days (decided 29 September, readiness close-out)"
   }
  }
 },
 "PricingRuleCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Pricing Rule Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "ruleId": {
    "type": "string",
    "description": "Rule ID"
   },
   "ruleName": {
    "type": "string",
    "description": "Rule Name"
   },
   "ruleType": {
    "type": "string",
    "enum": [
     "customerSegment",
     "membership",
     "loyalty",
     "residency",
     "nationality",
     "channel",
     "location",
     "quantity",
     "group",
     "seasonal",
     "dayOfWeek",
     "timeslot",
     "event",
     "corporateB2b",
     "custom"
    ],
    "description": "Rule Type (the pack's Rule Types list, pp.24-25)"
   },
   "priceList": {
    "type": "string",
    "description": "Price List: the name of the price list whose rate this rule selects"
   },
   "productScope": {
    "type": "string",
    "description": "Product Scope: the products or product categories the rule covers"
   },
   "customerScope": {
    "type": "string",
    "description": "Customer Scope: the customer segment, membership or partner the rule covers"
   },
   "channel": {
    "$ref": "../shared/common.yaml#/components/schemas/SalesChannel",
    "description": "Channel the rule is limited to; empty for all channels"
   },
   "venueLocation": {
    "type": "string",
    "description": "Venue/Location"
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date",
    "description": "Effective From"
   },
   "effectiveTo": {
    "type": "string",
    "format": "date",
    "nullable": true,
    "description": "Effective To; empty for open-ended"
   },
   "priority": {
    "type": "integer",
    "description": "Priority within the configurable pricing hierarchy (MoM 1 Sep §4.4): the lower number wins"
   },
   "status": {
    "type": "string",
    "description": "Status: draft, active, disabled or expired"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   },
   "aiInsights": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "AI Capability (p.25): e.g. three rules may return different prices for the same Adult ticket on Saturday through B2C; advisory"
   }
  }
 },
 "PricingRulePriorityConflictResolutionTestingView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Pricing Rule Priority, Conflict Resolution & Testing displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "priority": {
    "type": "integer",
    "description": "Priority within the configurable pricing hierarchy (MoM 1 Sep §4.4): the lower number wins"
   },
   "specificity": {
    "type": "integer",
    "description": "Specificity: number of conditions the rule tests; breaks ties within a priority"
   },
   "fallbackBehavior": {
    "type": "string",
    "enum": [
     "useStandardRate",
     "useNextMatchingRule",
     "blockSale"
    ],
    "description": "Fallback Behavior when the rule matches but its rate is unavailable"
   },
   "ruleId": {
    "type": "string",
    "description": "Rule ID"
   },
   "ruleName": {
    "type": "string",
    "description": "Rule Name"
   },
   "ruleType": {
    "type": "string",
    "enum": [
     "customerSegment",
     "membership",
     "loyalty",
     "residency",
     "nationality",
     "channel",
     "location",
     "quantity",
     "group",
     "seasonal",
     "dayOfWeek",
     "timeslot",
     "event",
     "corporateB2b",
     "custom"
    ],
    "description": "Rule Type"
   },
   "hierarchyLevel": {
    "type": "string",
    "enum": [
     "contractPartner",
     "customerMember",
     "eventPerformance",
     "venueLocation",
     "channel",
     "quantityGroup",
     "seasonDate",
     "standardRate"
    ],
    "description": "Rule Resolution level (p.35): Contract/Partner -> Customer/Member -> Event/Performance -> Venue/Location -> Channel -> Quantity/Group -> Season/Date -> Standard Rate; the order is configurable"
   },
   "onMatch": {
    "type": "string",
    "enum": [
     "stopProcessing",
     "continueProcessing"
    ],
    "description": "Stop or Continue Processing once this rule matches"
   },
   "overrideAllowed": {
    "type": "boolean",
    "description": "Override Allowed"
   },
   "validationIssues": {
    "type": "array",
    "description": "Conflict Detection (p.35)",
    "items": {
     "type": "object",
     "properties": {
      "code": {
       "type": "string",
       "enum": [
        "samePriorityMatches",
        "contradictoryRates",
        "circularFallback",
        "unreachableRule",
        "missingFallback",
        "overlappingTimeDateConditions"
       ]
      },
      "message": {
       "type": "string"
      }
     }
    }
   },
   "simulationOutcome": {
    "type": "string",
    "enum": [
     "selected",
     "matched",
     "rejected",
     "notMatched"
    ],
    "description": "Pricing Rule Simulator result for this rule; empty when no simulator parameters were sent",
    "nullable": true
   },
   "candidateRate": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "Candidate rate the rule would give in the simulated context (Gold Member - AED 190)"
   },
   "outcomeReason": {
    "type": "string",
    "nullable": true,
    "description": "Why it was selected or rejected, e.g. member pricing priority exceeds resident, day and standard pricing"
   }
  }
 },
 "PricingRuleTestInput": {
  "type": "object",
  "x-ticvai-persistence": "none — request only; a dry run stores nothing",
  "description": "The sample booking `testPricingRule` prices (decided 29 September, readiness close-out). The inputs are the ones `listPricingRulePriority` filters its test rows by.",
  "required": [
   "productId",
   "channel",
   "date"
  ],
  "properties": {
   "productId": {
    "type": "string",
    "format": "uuid"
   },
   "variantId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Absent means the product's own venue."
   },
   "channel": {
    "$ref": "../shared/common.yaml#/components/schemas/SalesChannel"
   },
   "date": {
    "type": "string",
    "format": "date",
    "description": "Visit or event date."
   },
   "time": {
    "type": "string",
    "pattern": "^([01][0-9]|2[0-3]):[0-5][0-9]$",
    "nullable": true,
    "description": "Visit time or timeslot start, venue local."
   },
   "customerSegment": {
    "type": "string",
    "nullable": true
   },
   "customerId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "membershipId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "residency": {
    "type": "string",
    "nullable": true
   },
   "quantity": {
    "type": "integer",
    "minimum": 1,
    "maximum": 500,
    "default": 1
   }
  }
 },
 "PricingRuleTestResult": {
  "type": "object",
  "x-ticvai-persistence": "none — response only; a dry run stores nothing",
  "description": "What `testPricingRule` returns. `matched` answers the question the button asks; the rest is the calculation the checkout would run.",
  "required": [
   "ruleId",
   "matched",
   "basePrice",
   "finalPrice"
  ],
  "properties": {
   "ruleId": {
    "type": "string"
   },
   "matched": {
    "type": "boolean",
    "description": "Whether the tested rule's conditions match the sample booking."
   },
   "notMatchedReasons": {
    "type": "array",
    "description": "The conditions that failed when `matched` is false, e.g. `channel not in rule`.",
    "items": {
     "type": "string"
    }
   },
   "appliedByPriority": {
    "type": "boolean",
    "description": "Matched and actually applied after priority and conflict resolution; a matching rule can still lose to a higher-priority one."
   },
   "basePrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "finalPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "rulesApplied": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "ruleId": {
       "type": "string"
      },
      "ruleName": {
       "type": "string"
      },
      "priority": {
       "type": "integer"
      },
      "adjustment": {
       "$ref": "../shared/common.yaml#/components/schemas/Money"
      },
      "applied": {
       "type": "boolean"
      }
     }
    }
   },
   "calculationPath": {
    "type": "array",
    "description": "Each step from base price to final price, in order, in words.",
    "items": {
     "type": "string"
    }
   },
   "testedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "QuantityGroupVolumePricingRulesView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Quantity, Group & Volume Pricing Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "groupMinimum": {
    "type": "integer",
    "nullable": true,
    "description": "Group Minimum: smallest party the group rate applies to"
   },
   "maximumGroupSize": {
    "type": "integer",
    "nullable": true,
    "description": "Maximum Group Size"
   },
   "groupType": {
    "type": "string",
    "enum": [
     "school",
     "corporate",
     "tour",
     "family",
     "b2b",
     "custom"
    ],
    "description": "Group Type (p.31)",
    "nullable": true
   },
   "ruleId": {
    "type": "string",
    "description": "Rule ID"
   },
   "ruleName": {
    "type": "string",
    "description": "Rule Name"
   },
   "quantityModel": {
    "type": "string",
    "enum": [
     "minimumQuantity",
     "quantityBands",
     "groupSize",
     "volumeThreshold",
     "buyXRate",
     "perPersonGroupRate"
    ],
    "description": "Quantity Model (p.31)"
   },
   "product": {
    "type": "string",
    "description": "Product or product family the rule covers"
   },
   "priceList": {
    "type": "string",
    "description": "Price List"
   },
   "bands": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "minQuantity": {
       "type": "integer"
      },
      "maxQuantity": {
       "type": "integer",
       "nullable": true
      },
      "rate": {
       "type": "string",
       "description": "Rate code for the band"
      }
     }
    },
    "description": "Tiered Rate Matrix (p.32): 1-9, 10-24, 25-49, 50+ each with its rate; the last band has no maximum"
   },
   "quantityBasis": {
    "type": "string",
    "enum": [
     "perProduct",
     "perProductFamily",
     "perOrder",
     "perGroupBooking",
     "cumulativePartnerVolume"
    ],
    "description": "Mixed Products (p.32): what quantity is counted; cumulativePartnerVolume counts a partner's sales over its agreement period (MoM 1 Sep §4.3)"
   },
   "complimentary": {
    "type": "object",
    "nullable": true,
    "description": "Complimentary Logic (p.32): freeQuantity complimentary per paidQuantity paid; empty for none",
    "properties": {
     "freeQuantity": {
      "type": "integer"
     },
     "paidQuantity": {
      "type": "integer"
     },
     "label": {
      "type": "string",
      "description": "e.g. coordinator"
     }
    }
   },
   "priority": {
    "type": "integer",
    "description": "Priority within the configurable pricing hierarchy (MoM 1 Sep §4.4): the lower number wins"
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date",
    "description": "Effective From"
   },
   "effectiveTo": {
    "type": "string",
    "format": "date",
    "description": "Effective To; empty for open-ended",
    "nullable": true
   },
   "status": {
    "type": "string",
    "description": "Status: draft, active, disabled or expired"
   }
  }
 },
 "ResidencyNationalityMarketPricingRulesView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Residency, Nationality & Market Pricing Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "ruleId": {
    "type": "string",
    "description": "Rule ID"
   },
   "ruleName": {
    "type": "string",
    "description": "Rule Name"
   },
   "marketLabel": {
    "type": "string",
    "description": "Market pricing label, e.g. UAE Resident, GCC Resident, International Visitor"
   },
   "eligibilityBasis": {
    "type": "string",
    "enum": [
     "residency",
     "nationality",
     "country",
     "market",
     "region",
     "customerAddress",
     "verifiedId",
     "governmentId"
    ],
    "description": "Eligibility Input (pp.27-28) the rule tests"
   },
   "eligibleValues": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Values that qualify, e.g. ISO country codes AE, SA, or market codes"
   },
   "verificationRequired": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "customerDeclaration",
      "accountProfile",
      "idUpload",
      "governmentIdentityVerification",
      "staffVerification"
     ]
    },
    "description": "Verification Requirements (p.28) that must be satisfied; empty means none"
   },
   "priceList": {
    "type": "string",
    "description": "Price List"
   },
   "rate": {
    "type": "string",
    "description": "Rate used when eligible, e.g. UAE Resident Adult"
   },
   "fallbackRate": {
    "type": "string",
    "description": "Fallback (p.28): rate used when eligibility cannot be verified; the Non-Resident rate by default (decided 29 September, readiness close-out)"
   },
   "priority": {
    "type": "integer",
    "description": "Priority within the configurable pricing hierarchy (MoM 1 Sep §4.4): the lower number wins"
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date",
    "description": "Effective From"
   },
   "effectiveTo": {
    "type": "string",
    "format": "date",
    "description": "Effective To; empty for open-ended",
    "nullable": true
   },
   "status": {
    "type": "string",
    "description": "Status: draft, active, disabled or expired"
   }
  }
 },
 "TimeslotPerformanceTimeOfDayPricingRulesView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Timeslot, Performance & Time-of-Day Pricing Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "timeslot": {
    "type": "string",
    "nullable": true,
    "description": "Timeslot the rule is limited to; empty for any"
   },
   "performance": {
    "type": "string",
    "nullable": true,
    "description": "Performance the rule is limited to (Matinee, Evening, Final Performance); empty for any"
   },
   "timeOfDayBand": {
    "type": "string",
    "enum": [
     "peak",
     "standard",
     "offPeak",
     "lateEntry",
     "earlyEntry"
    ],
    "description": "Time-of-Day Band (Peak/Off-Peak, p.34)",
    "nullable": true
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "event": {
    "type": "string",
    "nullable": true,
    "description": "Event"
   },
   "priceList": {
    "type": "string",
    "description": "Price List"
   },
   "rate": {
    "type": "string",
    "description": "Rate code"
   },
   "priority": {
    "type": "integer",
    "description": "Priority within the configurable pricing hierarchy (MoM 1 Sep §4.4): the lower number wins"
   },
   "ruleId": {
    "type": "string",
    "description": "Rule ID"
   },
   "ruleName": {
    "type": "string",
    "description": "Rule Name"
   },
   "timeBasis": {
    "type": "string",
    "enum": [
     "timeslotStart",
     "performanceStart",
     "arrivalWindow"
    ],
    "description": "Which time the range is tested against (Supported Contexts, p.33)"
   },
   "timeFrom": {
    "type": "string",
    "nullable": true,
    "pattern": "^([01][0-9]|2[0-3]):[0-5][0-9]$",
    "description": "Time Range start, local HH:mm (09:00)"
   },
   "timeTo": {
    "type": "string",
    "nullable": true,
    "pattern": "^([01][0-9]|2[0-3]):[0-5][0-9]$",
    "description": "Time Range end, local HH:mm, exclusive (12:00)"
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date",
    "description": "Effective From"
   },
   "effectiveTo": {
    "type": "string",
    "format": "date",
    "description": "Effective To; empty for open-ended",
    "nullable": true
   },
   "status": {
    "type": "string",
    "description": "Status: draft, active, disabled or expired"
   },
   "validationIssues": {
    "type": "array",
    "description": "Validation (p.34)",
    "items": {
     "type": "object",
     "properties": {
      "code": {
       "type": "string",
       "enum": [
        "overlappingTimeRanges",
        "missingTimeslotRate",
        "conflictingPerformanceRule"
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
