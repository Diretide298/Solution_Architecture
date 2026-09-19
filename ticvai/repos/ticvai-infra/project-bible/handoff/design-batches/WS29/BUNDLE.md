# WS29 — Membership   Annual Pass Management board 1

**10 screens · 10 operations · 17 schemas · 2 permissions**

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

- **Every control that can be refused must be gated.** 2 permissions apply here:
  `PLATFORM_CELL_MANAGE, PLATFORM_TENANT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **0 of these operations work offline**
  
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-284` | Membership & Annual Pass Command Center | listDetail | 1 | 0 | — |
| `BO-285` | Membership Product & Tier Builder | configEditor | 1 | 0 | — |
| `BO-286` | Membership Eligibility & Qualification Rule Builder | configEditor | 1 | 0 | — |
| `BO-287` | Validity, Activation & Expiry Configuration | listDetail | 1 | 0 | — |
| `BO-288` | Membership Entitlement & Admission Benefit Builder | configEditor | 1 | 0 | — |
| `BO-289` | Membership Usage, Visit & Consumption Rules | listDetail | 1 | 0 | — |
| `BO-290` | Family, Household & Dependent Membership Configuration | configEditor | 1 | 0 | — |
| `BO-291` | Membership Commercial, Pricing & Channel Association | configEditor | 1 | 0 | — |
| `BO-292` | Renewal, Auto-Renewal & Membership Continuity Configuration | configEditor | 1 | 0 | — |
| `BO-293` | Membership Product Validation, Approval, Publication & Versioning | configEditor | 1 | 0 | — |

## Thin screens in this batch

**BO-287, BO-289 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-284",
  "name": "Membership & Annual Pass Command Center",
  "module": "Sell",
  "requiresModule": "membership",
  "wave": 3,
  "source": {
   "pack": "Membership___Annual_Pass_Management_Reference.pdf",
   "board": "1",
   "number": "13.1.1",
   "page": 4
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/membership-annual-pass-command-center-bo-284",
   "component": "apps/venue-management-web/src/routes/sell/MembershipAnnualPassCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-285",
    "BO-286",
    "BO-287",
    "BO-288",
    "BO-289",
    "BO-290",
    "BO-291",
    "BO-292",
    "BO-293"
   ],
   "inferred": false,
   "notes": "**The board's hub.** The workshop specified this module as boards of ten and opened each with a command centre; the other nine screens are that board's detail, so they are reached from here and return here.",
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Venue Home",
     "carries": [
      "venueId"
     ],
     "provenance": "derived — BO-100 declares entryState.params venueId, so an edge into it must carry them"
    },
    {
     "to": "BO-285",
     "trigger": "Works in Membership Product & Tier Builder",
     "provenance": "flow F138 step 1→2",
     "operation": "listMembershipAnnualPass"
    },
    {
     "to": "BO-286",
     "trigger": "Works in Membership Eligibility & Qualification Rule Builder",
     "provenance": "flow F138 step 3→4",
     "operation": "listMembershipAnnualPass"
    },
    {
     "to": "BO-287",
     "trigger": "Works in Validity, Activation & Expiry Configuration",
     "provenance": "flow F138 step 5→6",
     "operation": "listMembershipAnnualPass"
    },
    {
     "to": "BO-288",
     "trigger": "Works in Membership Entitlement & Admission Benefit Builder",
     "provenance": "flow F138 step 7→8",
     "operation": "listMembershipAnnualPass"
    },
    {
     "to": "BO-289",
     "trigger": "Works in Membership Usage, Visit & Consumption Rules",
     "provenance": "flow F138 step 9→10",
     "operation": "listMembershipAnnualPass"
    },
    {
     "to": "BO-290",
     "trigger": "Works in Family, Household & Dependent Membership Configuration",
     "provenance": "flow F138 step 11→12",
     "operation": "listMembershipAnnualPass"
    },
    {
     "to": "BO-291",
     "trigger": "Works in Membership Commercial, Pricing & Channel Association",
     "provenance": "flow F138 step 13→14",
     "operation": "listMembershipAnnualPass"
    },
    {
     "to": "BO-292",
     "trigger": "Works in Renewal, Auto-Renewal & Membership Continuity Configuration",
     "provenance": "flow F138 step 15→16",
     "operation": "listMembershipAnnualPass"
    },
    {
     "to": "BO-293",
     "trigger": "Works in Membership Product Validation, Approval, Publication & Versioning",
     "provenance": "flow F138 step 17→18",
     "operation": "listMembershipAnnualPass"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display; Identify) and no metric row",
  "purpose": "Provide administrators with a centralized view of all membership, annual pass, season pass and subscription-style admission products.",
  "purposeNote": "Administrators can view, search and manage the complete portfolio of membership and annual-pass products from one workspace.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 16 actions on this screen and the screen declares 1 operation.** Unserved: Monthly Membership, Fixed-Term Membership, Corporate Membership, Family Membership, Individual Membership, Student Membership, VIP Membership, Custom Membership …. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Membership___Annual_Pass_Management_Reference.pdf, page 4 §Support configurable types such as"
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
       "label": "Every membership annual pass",
       "columns": [
        "MembershipAnnualPassCommandCenterView.activeMembershipProducts",
        "MembershipAnnualPassCommandCenterView.annualPassProducts",
        "MembershipAnnualPassCommandCenterView.draftProducts",
        "MembershipAnnualPassCommandCenterView.activeMembers",
        "MembershipAnnualPassCommandCenterView.familyMemberships",
        "MembershipAnnualPassCommandCenterView.membershipsExpiringSoon",
        "MembershipAnnualPassCommandCenterView.renewalEnabledProducts",
        "MembershipAnnualPassCommandCenterView.suspendedProducts",
        "MembershipAnnualPassCommandCenterView.productsWithConfigurationIssues",
        "MembershipAnnualPassCommandCenterView.averageMembershipDuration",
        "MembershipAnnualPassCommandCenterView.productId",
        "MembershipAnnualPassCommandCenterView.membershipName",
        "MembershipAnnualPassCommandCenterView.type",
        "MembershipAnnualPassCommandCenterView.tier",
        "MembershipAnnualPassCommandCenterView.venueAttraction",
        "MembershipAnnualPassCommandCenterView.validity",
        "MembershipAnnualPassCommandCenterView.activationMethod",
        "MembershipAnnualPassCommandCenterView.renewal",
        "MembershipAnnualPassCommandCenterView.familyIndividual",
        "MembershipAnnualPassCommandCenterView.currentMembers",
        "MembershipAnnualPassCommandCenterView.effectiveDates",
        "MembershipAnnualPassCommandCenterView.status",
        "MembershipAnnualPassCommandCenterView.owner",
        "MembershipAnnualPassCommandCenterView.missingEntitlements",
        "MembershipAnnualPassCommandCenterView.missingPricingAssociation",
        "MembershipAnnualPassCommandCenterView.missingValidity",
        "MembershipAnnualPassCommandCenterView.invalidEligibility",
        "MembershipAnnualPassCommandCenterView.conflictingRules",
        "MembershipAnnualPassCommandCenterView.missingRenewalPolicy"
       ],
       "bindsTo": "MembershipAnnualPassCommandCenterView",
       "operation": "listMembershipAnnualPass",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 4 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected membership annual pass",
       "bindsTo": "MembershipAnnualPassCommandCenterView",
       "columns": [
        "MembershipAnnualPassCommandCenterView.activeMembershipProducts",
        "MembershipAnnualPassCommandCenterView.annualPassProducts",
        "MembershipAnnualPassCommandCenterView.draftProducts",
        "MembershipAnnualPassCommandCenterView.activeMembers",
        "MembershipAnnualPassCommandCenterView.familyMemberships",
        "MembershipAnnualPassCommandCenterView.membershipsExpiringSoon",
        "MembershipAnnualPassCommandCenterView.renewalEnabledProducts",
        "MembershipAnnualPassCommandCenterView.suspendedProducts",
        "MembershipAnnualPassCommandCenterView.productsWithConfigurationIssues",
        "MembershipAnnualPassCommandCenterView.averageMembershipDuration",
        "MembershipAnnualPassCommandCenterView.productId",
        "MembershipAnnualPassCommandCenterView.membershipName",
        "MembershipAnnualPassCommandCenterView.type",
        "MembershipAnnualPassCommandCenterView.tier",
        "MembershipAnnualPassCommandCenterView.venueAttraction",
        "MembershipAnnualPassCommandCenterView.validity",
        "MembershipAnnualPassCommandCenterView.activationMethod",
        "MembershipAnnualPassCommandCenterView.renewal",
        "MembershipAnnualPassCommandCenterView.familyIndividual",
        "MembershipAnnualPassCommandCenterView.currentMembers",
        "MembershipAnnualPassCommandCenterView.effectiveDates",
        "MembershipAnnualPassCommandCenterView.status",
        "MembershipAnnualPassCommandCenterView.owner",
        "MembershipAnnualPassCommandCenterView.missingEntitlements",
        "MembershipAnnualPassCommandCenterView.missingPricingAssociation",
        "MembershipAnnualPassCommandCenterView.missingValidity",
        "MembershipAnnualPassCommandCenterView.invalidEligibility",
        "MembershipAnnualPassCommandCenterView.conflictingRules",
        "MembershipAnnualPassCommandCenterView.missingRenewalPolicy"
       ],
       "notes": null,
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 4 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Monthly Membership",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 4 §Support configurable types such as"
      },
      {
       "kind": "secondaryButton",
       "label": "Fixed-Term Membership",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 4 §Support configurable types such as"
      },
      {
       "kind": "secondaryButton",
       "label": "Corporate Membership",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 4 §Support configurable types such as"
      },
      {
       "kind": "secondaryButton",
       "label": "Family Membership",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 4 §Support configurable types such as"
      },
      {
       "kind": "secondaryButton",
       "label": "Individual Membership",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 4 §Support configurable types such as"
      },
      {
       "kind": "secondaryButton",
       "label": "Student Membership",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 4 §Support configurable types such as"
      },
      {
       "kind": "secondaryButton",
       "label": "VIP Membership",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 4 §Support configurable types such as"
      },
      {
       "kind": "secondaryButton",
       "label": "Custom Membership",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 4 §Support configurable types such as"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The membership annual pass list.",
   "error": "Could not load. Names which read failed and leaves the membership annual pass untouched.",
   "emptyFirstRun": "No membership annual pass yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the membership annual pass are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listMembershipAnnualPass",
    "contract": "subscription",
    "purpose": "Membership & Annual Pass Command Center",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "MembershipAnnualPassCommandCenterView.activeMembershipProducts",
    "MembershipAnnualPassCommandCenterView.annualPassProducts",
    "MembershipAnnualPassCommandCenterView.draftProducts",
    "MembershipAnnualPassCommandCenterView.activeMembers",
    "MembershipAnnualPassCommandCenterView.familyMemberships",
    "MembershipAnnualPassCommandCenterView.membershipsExpiringSoon"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-284"
  },
  "apisNote": "Regenerated 9 September 2026 from Membership___Annual_Pass_Management_Reference.pdf page 4. 29 of 29 labels bound to a contract property; 45 of 53 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-285",
  "name": "Membership Product & Tier Builder",
  "module": "Sell",
  "requiresModule": "membership",
  "wave": 3,
  "source": {
   "pack": "Membership___Annual_Pass_Management_Reference.pdf",
   "board": "1",
   "number": "13.1.2",
   "page": 5
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/membership-product-tier-builder-bo-285",
   "component": "apps/venue-management-web/src/routes/sell/MembershipProductTierBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-284"
   ],
   "exitTo": [
    "BO-284"
   ],
   "inferred": false,
   "notes": "**Reached from BO-284, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-284",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F138 step 2→3",
     "operation": "setMembershipProductTier"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture; Define; Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure the fundamental definition and hierarchy of a membership/pass.",
  "purposeNote": "Administrators can create and version membership products and tiers with clear relationships to the central TICVAI product catalogue.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Membership Name",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 5 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Membership Code",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 5 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Description",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 5 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Membership Type",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 5 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Brand",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 5 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 5 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Attraction",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 5 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Market",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 5 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Currency Context",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 5 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Effective From",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 5 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Effective To",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 5 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Tier Level",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 5 §Define"
      },
      {
       "kind": "selectField",
       "label": "Display Order",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 5 §Define"
      },
      {
       "kind": "selectField",
       "label": "Upgrade Path",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 5 §Define"
      },
      {
       "kind": "selectField",
       "label": "Downgrade Path",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 5 §Define"
      },
      {
       "kind": "selectField",
       "label": "Parent Membership",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 5 §Define"
      },
      {
       "kind": "selectField",
       "label": "Replacement Membership",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 5 §Define"
      },
      {
       "kind": "textField",
       "label": "Individual / Family / Corporate",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 5 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Named / Transferable",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 5 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Physical / Digital",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 5 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Renewable / Non-Renewable",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 5 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Auto-Renew Eligible",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 5 §Configure"
      },
      {
       "kind": "textField",
       "label": "Admission-Based / Benefit-Based / Hybrid",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 5 §Configure"
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
       "provenance": "contract operation setMembershipProductTier"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The membership product tier configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the membership product tier untouched.",
   "emptyFirstRun": "No membership product tier configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setMembershipProductTier",
    "contract": "subscription",
    "purpose": "Membership Product & Tier Builder",
    "trigger": "onAction",
    "invalidates": [
     "setMembershipProductTier"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-285"
  },
  "apisNote": "Regenerated 9 September 2026 from Membership___Annual_Pass_Management_Reference.pdf page 5. 0 of 0 labels bound to a contract property; 23 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-286",
  "name": "Membership Eligibility & Qualification Rule Builder",
  "module": "Sell",
  "requiresModule": "membership",
  "wave": 3,
  "source": {
   "pack": "Membership___Annual_Pass_Management_Reference.pdf",
   "board": "1",
   "number": "13.1.3",
   "page": 7
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/membership-eligibility-qualification-rule-builder-bo-286",
   "component": "apps/venue-management-web/src/routes/sell/MembershipEligibilityQualificationRuleBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-284"
   ],
   "exitTo": [
    "BO-284"
   ],
   "inferred": false,
   "notes": "**Reached from BO-284, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-284",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F138 step 4→5",
     "operation": "setMembershipEligibilityQualification"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure; Configure whether qualification requires) and no display directory — it is settings, not a population",
  "purpose": "Determine who is allowed to purchase, activate, hold or renew a particular membership.",
  "purposeNote": "rules and returns an explainable result.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Multiple Memberships Allowed",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 7 §Configure"
      },
      {
       "kind": "textField",
       "label": "One Membership per Customer",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Mutually Exclusive Memberships",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Prerequisite Membership",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Existing Tier Requirement",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 7 §Configure"
      },
      {
       "kind": "selectField",
       "label": "No Verification",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 7 §Configure whether qualification requires"
      },
      {
       "kind": "selectField",
       "label": "Customer Declaration",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 7 §Configure whether qualification requires"
      },
      {
       "kind": "selectField",
       "label": "Document Verification",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 7 §Configure whether qualification requires"
      },
      {
       "kind": "selectField",
       "label": "Identity Verification",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 7 §Configure whether qualification requires"
      },
      {
       "kind": "selectField",
       "label": "Staff Verification",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 7 §Configure whether qualification requires"
      },
      {
       "kind": "selectField",
       "label": "External Verification",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 7 §Configure whether qualification requires"
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
       "provenance": "contract operation setMembershipEligibilityQualification"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The membership eligibility qualification configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the membership eligibility qualification untouched.",
   "emptyFirstRun": "No membership eligibility qualification configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setMembershipEligibilityQualification",
    "contract": "subscription",
    "purpose": "Membership Eligibility & Qualification Rule Builder",
    "trigger": "onAction",
    "invalidates": [
     "setMembershipEligibilityQualification"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-286"
  },
  "apisNote": "Regenerated 9 September 2026 from Membership___Annual_Pass_Management_Reference.pdf page 7. 0 of 0 labels bound to a contract property; 11 of 35 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-287",
  "name": "Validity, Activation & Expiry Configuration",
  "module": "Sell",
  "requiresModule": "membership",
  "wave": 3,
  "source": {
   "pack": "Membership___Annual_Pass_Management_Reference.pdf",
   "board": "1",
   "number": "13.1.4",
   "page": 8
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/validity-activation-expiry-configuration-bo-287",
   "component": "apps/venue-management-web/src/routes/sell/ValidityActivationExpiryConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-284"
   ],
   "exitTo": [
    "BO-284"
   ],
   "inferred": false,
   "notes": "**Reached from BO-284, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-284",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F138 step 6→7",
     "operation": "setValidityActivationExpiry"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Define exactly when a membership becomes valid, how long it remains valid and how it expires.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Membership___Annual_Pass_Management_Reference.pdf, page 8"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Membership___Annual_Pass_Management_Reference.pdf, page 8"
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
       "provenance": "contract operation setValidityActivationExpiry"
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
       "impliedBy": "setValidityActivationExpiry"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The validity activation expiry list.",
   "error": "Could not load. Names which read failed and leaves the validity activation expiry untouched.",
   "emptyFirstRun": "No validity activation expiry yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the validity activation expiry are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setValidityActivationExpiry",
    "contract": "subscription",
    "purpose": "Validity, Activation & Expiry Configuration",
    "trigger": "onAction",
    "invalidates": [
     "setValidityActivationExpiry"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-287"
  },
  "apisNote": "Regenerated 9 September 2026 from Membership___Annual_Pass_Management_Reference.pdf page 8. 0 of 0 labels bound to a contract property; 0 of 5 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-288",
  "name": "Membership Entitlement & Admission Benefit Builder",
  "module": "Sell",
  "requiresModule": "membership",
  "wave": 3,
  "source": {
   "pack": "Membership___Annual_Pass_Management_Reference.pdf",
   "board": "1",
   "number": "13.1.5",
   "page": 9
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/membership-entitlement-admission-benefit-builder-bo-288",
   "component": "apps/venue-management-web/src/routes/sell/MembershipEntitlementAdmissionBenefitBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-284"
   ],
   "exitTo": [
    "BO-284"
   ],
   "inferred": false,
   "notes": "**Reached from BO-284, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-284",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F138 step 8→9",
     "operation": "setMembershipEntitlementAdmission"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Define exactly what the member receives. This is the heart of the membership product.",
  "purposeNote": "Administrators can define the complete admission and benefit package associated with every membership tier.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 2 actions on this screen and the screen declares 1 operation.** Unserved: Guest Tickets, Booking Privileges. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Membership___Annual_Pass_Management_Reference.pdf, page 9 §Support"
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
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 9 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Attraction",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 9 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Event Type",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 9 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Admission Type",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 9 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Number of Visits",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 9 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Period",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 9 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Days",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 9 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Times",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 9 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Timeslots",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 9 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Per Day",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 9 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Per Week",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 9 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Per Month",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 9 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Per Membership Year",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 9 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Lifetime of Membership",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 9 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Guest Tickets",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 9 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Booking Privileges",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 9 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The membership entitlement admission configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the membership entitlement admission untouched.",
   "emptyFirstRun": "No membership entitlement admission configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setMembershipEntitlementAdmission",
    "contract": "subscription",
    "purpose": "Membership Entitlement & Admission Benefit Builder",
    "trigger": "onAction",
    "invalidates": [
     "setMembershipEntitlementAdmission"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-288"
  },
  "apisNote": "Regenerated 9 September 2026 from Membership___Annual_Pass_Management_Reference.pdf page 9. 0 of 0 labels bound to a contract property; 16 of 45 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-289",
  "name": "Membership Usage, Visit & Consumption Rules",
  "module": "Sell",
  "requiresModule": "membership",
  "wave": 3,
  "source": {
   "pack": "Membership___Annual_Pass_Management_Reference.pdf",
   "board": "1",
   "number": "13.1.6",
   "page": 11
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/membership-usage-visit-consumption-rules-bo-289",
   "component": "apps/venue-management-web/src/routes/sell/MembershipUsageVisitConsumptionRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-284"
   ],
   "exitTo": [
    "BO-284"
   ],
   "inferred": false,
   "notes": "**Reached from BO-284, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-284",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F138 step 10→11",
     "operation": "listMembershipUsageVisit"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Maintain counters such as) and no metric row",
  "purpose": "Control how membership entitlements may actually be consumed. Screen 13.1.5 defines what the member receives. Screen 13.1.6 defines how it may be used.",
  "purposeNote": "Membership entitlement usage is governed consistently across reservation, ticketing and access-control channels.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every membership usage visit",
       "columns": [
        "MembershipUsageVisitConsumptionRulesView.parking12UsesThisYear"
       ],
       "bindsTo": "MembershipUsageVisitConsumptionRulesView",
       "operation": "listMembershipUsageVisit",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 11 §Maintain counters such as"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected membership usage visit",
       "bindsTo": "MembershipUsageVisitConsumptionRulesView",
       "columns": [
        "MembershipUsageVisitConsumptionRulesView.parking12UsesThisYear"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Unlimited annual visits”, “Access Integration”.",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 11 §Maintain counters such as"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The membership usage visit list.",
   "error": "Could not load. Names which read failed and leaves the membership usage visit untouched.",
   "emptyFirstRun": "No membership usage visit yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the membership usage visit are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listMembershipUsageVisit",
    "contract": "subscription",
    "purpose": "Membership Usage, Visit & Consumption Rules",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "MembershipUsageVisitConsumptionRulesView.parking12UsesThisYear"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-289"
  },
  "apisNote": "Regenerated 9 September 2026 from Membership___Annual_Pass_Management_Reference.pdf page 11. 1 of 1 labels bound to a contract property; 20 of 32 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-290",
  "name": "Family, Household & Dependent Membership Configuration",
  "module": "Sell",
  "requiresModule": "membership",
  "wave": 3,
  "source": {
   "pack": "Membership___Annual_Pass_Management_Reference.pdf",
   "board": "1",
   "number": "13.1.7",
   "page": 12
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/family-household-dependent-membership-configuration-bo-290",
   "component": "apps/venue-management-web/src/routes/sell/FamilyHouseholdDependentMembershipConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-284"
   ],
   "exitTo": [
    "BO-284"
   ],
   "inferred": false,
   "notes": "**Reached from BO-284, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-284",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F138 step 12→13",
     "operation": "setFamilyHouseholdDependent"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure; Possible configured action) and no display directory — it is settings, not a population",
  "purpose": "Support memberships covering more than one person while preserving individual identities and entitlements.",
  "purposeNote": "roles, eligibility and shared/individual entitlements.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Primary Member",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 12 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Secondary Adult",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 12 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Dependent",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 12 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Child",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 12 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Guardian",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 12 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Authorized Manager",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 12 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Minimum Age",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 12 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum Age",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 12 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Relationship Requirement",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 12 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Verification Requirement",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 12 §Configure"
      },
      {
       "kind": "textField",
       "label": "Same Household Requirement where applicable",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 12 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Allowed",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 12 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Effective Date",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 12 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Frequency",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 12 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Fee",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 12 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Approval",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 12 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Eligibility Revalidation",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 12 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Grace Period",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 12 §Possible configured action"
      },
      {
       "kind": "selectField",
       "label": "Upgrade Required",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 12 §Possible configured action"
      },
      {
       "kind": "selectField",
       "label": "Renewal Correction",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 12 §Possible configured action"
      },
      {
       "kind": "selectField",
       "label": "Manual Review",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 12 §Possible configured action"
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
       "provenance": "contract operation setFamilyHouseholdDependent"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The family household dependent configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the family household dependent untouched.",
   "emptyFirstRun": "No family household dependent configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setFamilyHouseholdDependent",
    "contract": "subscription",
    "purpose": "Family, Household & Dependent Membership Configuration",
    "trigger": "onAction",
    "invalidates": [
     "setFamilyHouseholdDependent"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-290"
  },
  "apisNote": "Regenerated 9 September 2026 from Membership___Annual_Pass_Management_Reference.pdf page 12. 0 of 0 labels bound to a contract property; 21 of 37 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-291",
  "name": "Membership Commercial, Pricing & Channel Association",
  "module": "Sell",
  "requiresModule": "membership",
  "wave": 3,
  "source": {
   "pack": "Membership___Annual_Pass_Management_Reference.pdf",
   "board": "1",
   "number": "13.1.8",
   "page": 14
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/membership-commercial-pricing-channel-association-bo-291",
   "component": "apps/venue-management-web/src/routes/sell/MembershipCommercialPricingChannelAssociation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-284"
   ],
   "exitTo": [
    "BO-284"
   ],
   "inferred": false,
   "notes": "**Reached from BO-284, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-284",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F138 step 14→15",
     "operation": "listMembershipCommercialPricing"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure sale through; Configure) and no display directory — it is settings, not a population",
  "purpose": "Connect the membership contract to TICVAI's central commercial engines without duplicating pricing configuration.",
  "purposeNote": "Membership products can be commercially sold across authorized channels using centrally governed pricing, tax, fee and payment services.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "B2C",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 14 §Configure sale through"
      },
      {
       "kind": "selectField",
       "label": "Mobile App",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 14 §Configure sale through"
      },
      {
       "kind": "selectField",
       "label": "POS",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 14 §Configure sale through"
      },
      {
       "kind": "selectField",
       "label": "Call Center",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 14 §Configure sale through"
      },
      {
       "kind": "selectField",
       "label": "Box Office",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 14 §Configure sale through"
      },
      {
       "kind": "selectField",
       "label": "Kiosk",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 14 §Configure sale through"
      },
      {
       "kind": "selectField",
       "label": "B2B",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 14 §Configure sale through"
      },
      {
       "kind": "selectField",
       "label": "Corporate",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 14 §Configure sale through"
      },
      {
       "kind": "selectField",
       "label": "Reseller",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 14 §Configure sale through"
      },
      {
       "kind": "selectField",
       "label": "API",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 14 §Configure sale through"
      },
      {
       "kind": "selectField",
       "label": "Always Available",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 14 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Fixed Sales Window",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 14 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Seasonal Sale",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 14 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Invitation Only",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 14 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Capacity Limited",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 14 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The membership commercial pricing configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the membership commercial pricing untouched.",
   "emptyFirstRun": "No membership commercial pricing configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listMembershipCommercialPricing",
    "contract": "subscription",
    "purpose": "Membership Commercial, Pricing & Channel Association",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-291"
  },
  "apisNote": "Regenerated 9 September 2026 from Membership___Annual_Pass_Management_Reference.pdf page 14. 0 of 0 labels bound to a contract property; 15 of 38 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-292",
  "name": "Renewal, Auto-Renewal & Membership Continuity Configuration",
  "module": "Sell",
  "requiresModule": "membership",
  "wave": 3,
  "source": {
   "pack": "Membership___Annual_Pass_Management_Reference.pdf",
   "board": "1",
   "number": "13.1.9",
   "page": 15
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/renewal-auto-renewal-membership-continuity-configuration-bo-292",
   "component": "apps/venue-management-web/src/routes/sell/RenewalAutoRenewalMembershipContinuityConfigurat.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-284"
   ],
   "exitTo": [
    "BO-284"
   ],
   "inferred": false,
   "notes": "**Reached from BO-284, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "BO-284",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F138 step 16→17",
     "operation": "setRenewalAutoMembership"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure; At renewal, configure whether) and no display directory — it is settings, not a population",
  "purpose": "Define how a membership moves from one validity period into the next.",
  "purposeNote": "continuity, commercial terms and required customer consent.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Customer Self-Service Renewal. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Membership___Annual_Pass_Management_Reference.pdf, page 15 §Support"
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
       "label": "60 days before expiry",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 15 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Eligible Products",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 15 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Consent Requirement",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 15 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Payment Method Requirement",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 15 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Pre-Renewal Notification",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 15 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Retry Policy",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 15 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Failure Handling",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 15 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Same Tier Only",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 15 §At renewal, configure whether"
      },
      {
       "kind": "selectField",
       "label": "Upgrade Allowed",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 15 §At renewal, configure whether"
      },
      {
       "kind": "selectField",
       "label": "Downgrade Allowed",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 15 §At renewal, configure whether"
      },
      {
       "kind": "selectField",
       "label": "Suggested Tier",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 15 §At renewal, configure whether"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Customer Self-Service Renewal",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 15 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The renewal auto-renewal membership configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the renewal auto-renewal membership untouched.",
   "emptyFirstRun": "No renewal auto-renewal membership configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setRenewalAutoMembership",
    "contract": "subscription",
    "purpose": "Renewal, Auto-Renewal & Membership Continuity Configuration",
    "trigger": "onAction",
    "invalidates": [
     "setRenewalAutoMembership"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-292"
  },
  "apisNote": "Regenerated 9 September 2026 from Membership___Annual_Pass_Management_Reference.pdf page 15. 0 of 0 labels bound to a contract property; 12 of 37 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-293",
  "name": "Membership Product Validation, Approval, Publication & Versioning",
  "module": "Sell",
  "requiresModule": "membership",
  "wave": 3,
  "source": {
   "pack": "Membership___Annual_Pass_Management_Reference.pdf",
   "board": "1",
   "number": "13.1.10",
   "page": 17
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/sell/membership-product-validation-approval-publication-versi-bo-293",
   "component": "apps/venue-management-web/src/routes/sell/MembershipProductValidationApprovalPublicationVe.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-284"
   ],
   "exitTo": [
    "BO-284"
   ],
   "inferred": false,
   "notes": "**Reached from BO-284, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation."
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Synchronize relevant configuration with; AI Configuration Review) and no display directory — it is settings, not a population",
  "purpose": "Provide the final governance layer before a membership/pass configuration becomes commercially available.",
  "purposeNote": "Only validated, approved and correctly versioned membership configurations can become commercially active, with complete impact and audit history. Board 1 — Final Screen Register # Backend Screen Core Responsibility 13.1. Membership & Annual Pass Command Center Portfolio management 1 13.1. Membership Product & Tier Builder Product/tier definition 2 13.1. Membership Eligibility & Qualification Rule Builder Member eligibility 3 13.1. Validity, Activation & Expiry Configuration Membership lifecycle 4 13.1. Benefits and Membership Entitlement & Admission Benefit Builder 5 entitlements 13.1. Member",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "B2C",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 17 §Synchronize relevant configuration with"
      },
      {
       "kind": "selectField",
       "label": "POS",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 17 §Synchronize relevant configuration with"
      },
      {
       "kind": "selectField",
       "label": "Mobile App",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 17 §Synchronize relevant configuration with"
      },
      {
       "kind": "selectField",
       "label": "Call Center",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 17 §Synchronize relevant configuration with"
      },
      {
       "kind": "selectField",
       "label": "B2B",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 17 §Synchronize relevant configuration with"
      },
      {
       "kind": "selectField",
       "label": "Access Control",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 17 §Synchronize relevant configuration with"
      },
      {
       "kind": "selectField",
       "label": "Ticketing",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 17 §Synchronize relevant configuration with"
      },
      {
       "kind": "selectField",
       "label": "Other dependent services",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 17 §Synchronize relevant configuration with"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Approve",
       "provenance": "contract operation approveMembershipProductValidation"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The membership product validation configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the membership product validation untouched.",
   "emptyFirstRun": "No membership product validation configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "approveMembershipProductValidation",
    "contract": "subscription",
    "purpose": "Membership Product Validation, Approval, Publication & Versioning",
    "trigger": "onAction",
    "invalidates": [
     "approveMembershipProductValidation"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-293"
  },
  "apisNote": "Regenerated 9 September 2026 from Membership___Annual_Pass_Management_Reference.pdf page 17. 0 of 0 labels bound to a contract property; 8 of 112 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "approveMembershipProductValidation": {
  "method": "PUT",
  "path": "/membership-product-validation",
  "contract": "subscription",
  "summary": "Membership Product Validation, Approval, Publication & Versioning",
  "permission": "PLATFORM_CELL_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": "MembershipProductValidationApprovalPublicationVersioInput",
  "responds": "MembershipProductValidationApprovalPublicationVersioView"
 },
 "listMembershipAnnualPass": {
  "method": "GET",
  "path": "/membership-annual-pass",
  "contract": "subscription",
  "summary": "Membership & Annual Pass Command Center",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "MembershipAnnualPassCommandCenterView"
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
  "parameters": [],
  "requestBody": null,
  "responds": "MembershipCommercialPricingChannelAssociationView"
 },
 "listMembershipUsageVisit": {
  "method": "GET",
  "path": "/membership-usage-visit",
  "contract": "subscription",
  "summary": "Membership Usage, Visit & Consumption Rules",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "MembershipUsageVisitConsumptionRulesView"
 },
 "setFamilyHouseholdDependent": {
  "method": "PUT",
  "path": "/family-household-dependent",
  "contract": "subscription",
  "summary": "Family, Household & Dependent Membership Configuration",
  "permission": "PLATFORM_CELL_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": "FamilyHouseholdDependentMembershipConfigurationInput",
  "responds": "FamilyHouseholdDependentMembershipConfigurationView"
 },
 "setMembershipEligibilityQualification": {
  "method": "PUT",
  "path": "/membership-eligibility-qualification",
  "contract": "subscription",
  "summary": "Membership Eligibility & Qualification Rule Builder",
  "permission": "PLATFORM_CELL_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": "MembershipEligibilityQualificationRuleBuilderInput",
  "responds": "MembershipEligibilityQualificationRuleBuilderView"
 },
 "setMembershipEntitlementAdmission": {
  "method": "PUT",
  "path": "/membership-entitlement-admission",
  "contract": "subscription",
  "summary": "Membership Entitlement & Admission Benefit Builder",
  "permission": "PLATFORM_CELL_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": "MembershipEntitlementAdmissionBenefitBuilderInput",
  "responds": "MembershipEntitlementAdmissionBenefitBuilderView"
 },
 "setMembershipProductTier": {
  "method": "PUT",
  "path": "/membership-product-tier",
  "contract": "subscription",
  "summary": "Membership Product & Tier Builder",
  "permission": "PLATFORM_CELL_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": "MembershipProductTierBuilderInput",
  "responds": "MembershipProductTierBuilderView"
 },
 "setRenewalAutoMembership": {
  "method": "PUT",
  "path": "/renewal-auto-membership",
  "contract": "subscription",
  "summary": "Renewal, Auto-Renewal & Membership Continuity Configuration",
  "permission": "PLATFORM_CELL_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": "RenewalAutoRenewalMembershipContinuityConfigurationInput",
  "responds": "RenewalAutoRenewalMembershipContinuityConfigurationView"
 },
 "setValidityActivationExpiry": {
  "method": "PUT",
  "path": "/validity-activation-expiry",
  "contract": "subscription",
  "summary": "Validity, Activation & Expiry Configuration",
  "permission": "PLATFORM_CELL_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": "ValidityActivationExpiryConfigurationInput",
  "responds": "ValidityActivationExpiryConfigurationView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "FamilyHouseholdDependentMembershipConfigurationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Family, Household & Dependent Membership Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "individual": {
    "type": "string",
    "description": "Individual"
   },
   "couple": {
    "type": "string",
    "description": "Couple"
   },
   "family": {
    "type": "string",
    "description": "Family"
   },
   "household": {
    "type": "string",
    "description": "Household"
   },
   "parentChild": {
    "type": "string",
    "description": "Parent + Child"
   },
   "corporateGroup": {
    "type": "string",
    "description": "Corporate Group"
   },
   "customGroupStructure": {
    "type": "string",
    "description": "Custom Group Structure"
   },
   "primaryMember": {
    "type": "string",
    "description": "Primary Member"
   },
   "secondaryAdult": {
    "type": "string",
    "description": "Secondary Adult"
   },
   "dependent": {
    "type": "string",
    "description": "Dependent"
   },
   "child": {
    "type": "string",
    "description": "Child"
   },
   "guardian": {
    "type": "string",
    "description": "Guardian"
   },
   "authorizedManager": {
    "type": "string",
    "description": "Authorized Manager"
   },
   "minimumAge": {
    "type": "string",
    "description": "Minimum Age"
   },
   "maximumAge": {
    "type": "string",
    "description": "Maximum Age"
   },
   "relationshipRequirement": {
    "type": "string",
    "description": "Relationship Requirement"
   },
   "verificationRequirement": {
    "type": "string",
    "description": "Verification Requirement"
   },
   "sameHouseholdRequirementWhereApplicable": {
    "type": "string",
    "description": "Same Household Requirement where applicable"
   },
   "allowed": {
    "type": "boolean",
    "description": "Allowed"
   },
   "effectiveDate": {
    "type": "string",
    "format": "date-time",
    "description": "Effective Date"
   },
   "frequency": {
    "type": "string",
    "description": "Frequency"
   },
   "fee": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Fee"
   },
   "approval": {
    "type": "string",
    "description": "Approval"
   },
   "eligibilityRevalidation": {
    "type": "string",
    "description": "Eligibility Revalidation"
   },
   "maximum3Children": {
    "type": "string",
    "description": "Maximum 3 Children"
   },
   "gracePeriod": {
    "type": "string",
    "format": "date-time",
    "description": "Grace Period"
   },
   "renewalCorrection": {
    "type": "string",
    "description": "Renewal Correction"
   },
   "manualReview": {
    "type": "string",
    "description": "Manual Review"
   }
  }
 },
 "FamilyHouseholdDependentMembershipConfigurationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Family, Household & Dependent Membership Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "individual": {
    "type": "string",
    "description": "Individual"
   },
   "couple": {
    "type": "string",
    "description": "Couple"
   },
   "family": {
    "type": "string",
    "description": "Family"
   },
   "household": {
    "type": "string",
    "description": "Household"
   },
   "parentChild": {
    "type": "string",
    "description": "Parent + Child"
   },
   "corporateGroup": {
    "type": "string",
    "description": "Corporate Group"
   },
   "customGroupStructure": {
    "type": "string",
    "description": "Custom Group Structure"
   },
   "primaryMember": {
    "type": "string",
    "description": "Primary Member"
   },
   "secondaryAdult": {
    "type": "string",
    "description": "Secondary Adult"
   },
   "dependent": {
    "type": "string",
    "description": "Dependent"
   },
   "child": {
    "type": "string",
    "description": "Child"
   },
   "guardian": {
    "type": "string",
    "description": "Guardian"
   },
   "authorizedManager": {
    "type": "string",
    "description": "Authorized Manager"
   },
   "minimumAge": {
    "type": "string",
    "description": "Minimum Age"
   },
   "maximumAge": {
    "type": "string",
    "description": "Maximum Age"
   },
   "relationshipRequirement": {
    "type": "string",
    "description": "Relationship Requirement"
   },
   "verificationRequirement": {
    "type": "string",
    "description": "Verification Requirement"
   },
   "sameHouseholdRequirementWhereApplicable": {
    "type": "string",
    "description": "Same Household Requirement where applicable"
   },
   "allowed": {
    "type": "boolean",
    "description": "Allowed"
   },
   "effectiveDate": {
    "type": "string",
    "format": "date-time",
    "description": "Effective Date"
   },
   "frequency": {
    "type": "string",
    "description": "Frequency"
   },
   "fee": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Fee"
   },
   "approval": {
    "type": "string",
    "description": "Approval"
   },
   "eligibilityRevalidation": {
    "type": "string",
    "description": "Eligibility Revalidation"
   },
   "maximum3Children": {
    "type": "string",
    "description": "Maximum 3 Children"
   },
   "gracePeriod": {
    "type": "string",
    "format": "date-time",
    "description": "Grace Period"
   },
   "renewalCorrection": {
    "type": "string",
    "description": "Renewal Correction"
   },
   "manualReview": {
    "type": "string",
    "description": "Manual Review"
   }
  }
 },
 "MembershipAnnualPassCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Membership & Annual Pass Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "activeMembershipProducts": {
    "type": "integer",
    "description": "Active Membership Products"
   },
   "annualPassProducts": {
    "type": "integer",
    "description": "Annual Pass Products"
   },
   "draftProducts": {
    "type": "integer",
    "description": "Draft Products"
   },
   "activeMembers": {
    "type": "integer",
    "description": "Active Members"
   },
   "familyMemberships": {
    "type": "integer",
    "description": "Family Memberships"
   },
   "membershipsExpiringSoon": {
    "type": "string",
    "description": "Memberships Expiring Soon"
   },
   "renewalEnabledProducts": {
    "type": "integer",
    "description": "Renewal-Enabled Products"
   },
   "suspendedProducts": {
    "type": "integer",
    "description": "Suspended Products"
   },
   "productsWithConfigurationIssues": {
    "type": "string",
    "description": "Products with Configuration Issues"
   },
   "averageMembershipDuration": {
    "type": "string",
    "format": "date-time",
    "description": "Average Membership Duration"
   },
   "productId": {
    "type": "string",
    "description": "Product ID"
   },
   "membershipName": {
    "type": "string",
    "description": "Membership Name"
   },
   "type": {
    "type": "string",
    "description": "Type"
   },
   "tier": {
    "type": "string",
    "description": "Tier"
   },
   "venueAttraction": {
    "type": "string",
    "description": "Venue/Attraction"
   },
   "validity": {
    "type": "string",
    "description": "Validity"
   },
   "activationMethod": {
    "type": "string",
    "description": "Activation Method"
   },
   "renewal": {
    "type": "string",
    "description": "Renewal"
   },
   "familyIndividual": {
    "type": "string",
    "description": "Family/Individual"
   },
   "currentMembers": {
    "type": "integer",
    "description": "Current Members"
   },
   "effectiveDates": {
    "type": "integer",
    "description": "Effective Dates"
   },
   "status": {
    "type": "integer",
    "description": "Status"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   },
   "annualPass": {
    "type": "string",
    "description": "Annual Pass"
   },
   "seasonPass": {
    "type": "string",
    "description": "Season Pass"
   },
   "monthlyMembership": {
    "type": "string",
    "description": "Monthly Membership"
   },
   "fixedTermMembership": {
    "type": "string",
    "description": "Fixed-Term Membership"
   },
   "corporateMembership": {
    "type": "string",
    "description": "Corporate Membership"
   },
   "familyMembership": {
    "type": "string",
    "description": "Family Membership"
   },
   "individualMembership": {
    "type": "string",
    "description": "Individual Membership"
   },
   "studentMembership": {
    "type": "string",
    "description": "Student Membership"
   },
   "vipMembership": {
    "type": "string",
    "description": "VIP Membership"
   },
   "customMembership": {
    "type": "string",
    "description": "Custom Membership"
   },
   "missingEntitlements": {
    "type": "string",
    "description": "Missing Entitlements"
   },
   "missingPricingAssociation": {
    "type": "string",
    "description": "Missing Pricing Association"
   },
   "missingValidity": {
    "type": "string",
    "description": "Missing Validity"
   },
   "invalidEligibility": {
    "type": "string",
    "description": "Invalid Eligibility"
   },
   "conflictingRules": {
    "type": "string",
    "description": "Conflicting Rules"
   },
   "missingRenewalPolicy": {
    "type": "string",
    "description": "Missing Renewal Policy"
   },
   "preview": {
    "type": "string",
    "description": "Preview"
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
    "description": "Base Pricing Profile"
   },
   "membershipTierPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Membership Tier Price"
   },
   "renewalPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Renewal Price"
   },
   "promotionalPricingEligibility": {
    "type": "string",
    "description": "Promotional Pricing Eligibility"
   },
   "taxProfile": {
    "type": "string",
    "description": "Tax Profile"
   },
   "feeProfile": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Fee Profile"
   },
   "b2c": {
    "type": "string",
    "description": "B2C"
   },
   "mobileApp": {
    "type": "string",
    "description": "Mobile App"
   },
   "pos": {
    "type": "string",
    "description": "POS"
   },
   "callCenter": {
    "type": "string",
    "description": "Call Center"
   },
   "boxOffice": {
    "type": "string",
    "description": "Box Office"
   },
   "kiosk": {
    "type": "string",
    "description": "Kiosk"
   },
   "b2b": {
    "type": "string",
    "description": "B2B"
   },
   "corporate": {
    "type": "string",
    "description": "Corporate"
   },
   "reseller": {
    "type": "string",
    "description": "Reseller"
   },
   "api": {
    "type": "string",
    "description": "API"
   },
   "callCenterBoxOffice": {
    "type": "string",
    "description": "Call Center + Box Office"
   },
   "fullPayment": {
    "type": "string",
    "description": "Full Payment"
   },
   "installmentsWhereSupported": {
    "type": "string",
    "description": "Installments where supported"
   },
   "corporateCredit": {
    "type": "string",
    "description": "Corporate Credit"
   },
   "autoRenewPayment": {
    "type": "string",
    "description": "Auto-Renew Payment"
   },
   "area13IdentifiesEligibilityBenefit": {
    "type": "string",
    "description": "Area 13 identifies eligibility/benefit"
   },
   "alwaysAvailable": {
    "type": "string",
    "description": "Always Available"
   },
   "fixedSalesWindow": {
    "type": "string",
    "format": "date-time",
    "description": "Fixed Sales Window"
   },
   "seasonalSale": {
    "type": "string",
    "description": "Seasonal Sale"
   },
   "invitationOnly": {
    "type": "string",
    "description": "Invitation Only"
   },
   "capacityLimited": {
    "type": "integer",
    "description": "Capacity Limited"
   }
  }
 },
 "MembershipEligibilityQualificationRuleBuilderInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Membership Eligibility & Qualification Rule Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "age": {
    "type": "string",
    "description": "Age"
   },
   "personType": {
    "type": "string",
    "description": "Person Type"
   },
   "residency": {
    "type": "string",
    "description": "Residency"
   },
   "country": {
    "type": "string",
    "description": "Country"
   },
   "customerSegment": {
    "type": "string",
    "description": "Customer Segment"
   },
   "corporateAffiliation": {
    "type": "string",
    "description": "Corporate Affiliation"
   },
   "studentStatus": {
    "type": "string",
    "description": "Student Status"
   },
   "existingMembership": {
    "type": "string",
    "description": "Existing Membership"
   },
   "previousPurchase": {
    "type": "string",
    "description": "Previous Purchase"
   },
   "membershipHistory": {
    "type": "string",
    "description": "Membership History"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "promotionalQualification": {
    "type": "string",
    "description": "Promotional Qualification"
   },
   "residencyVerificationRequired": {
    "type": "boolean",
    "description": "Residency verification required"
   },
   "approvedCorporateAccountRequired": {
    "type": "boolean",
    "description": "Approved corporate account required"
   },
   "multipleMembershipsAllowed": {
    "type": "boolean",
    "description": "Multiple Memberships Allowed"
   },
   "oneMembershipPerCustomer": {
    "type": "string",
    "description": "One Membership per Customer"
   },
   "mutuallyExclusiveMemberships": {
    "type": "string",
    "description": "Mutually Exclusive Memberships"
   },
   "prerequisiteMembership": {
    "type": "string",
    "description": "Prerequisite Membership"
   },
   "existingTierRequirement": {
    "type": "string",
    "description": "Existing Tier Requirement"
   },
   "noVerification": {
    "type": "string",
    "description": "No Verification"
   },
   "customerDeclaration": {
    "type": "string",
    "description": "Customer Declaration"
   },
   "documentVerification": {
    "type": "string",
    "description": "Document Verification"
   },
   "identityVerification": {
    "type": "string",
    "description": "Identity Verification"
   },
   "staffVerification": {
    "type": "string",
    "description": "Staff Verification"
   },
   "externalVerification": {
    "type": "string",
    "description": "External Verification"
   },
   "allowDifferentRules": {
    "type": "boolean",
    "description": "Allow different rules"
   },
   "withAnExplanation": {
    "type": "string",
    "description": "with an explanation"
   }
  }
 },
 "MembershipEligibilityQualificationRuleBuilderView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Membership Eligibility & Qualification Rule Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "age": {
    "type": "string",
    "description": "Age"
   },
   "personType": {
    "type": "string",
    "description": "Person Type"
   },
   "residency": {
    "type": "string",
    "description": "Residency"
   },
   "country": {
    "type": "string",
    "description": "Country"
   },
   "customerSegment": {
    "type": "string",
    "description": "Customer Segment"
   },
   "corporateAffiliation": {
    "type": "string",
    "description": "Corporate Affiliation"
   },
   "studentStatus": {
    "type": "string",
    "description": "Student Status"
   },
   "existingMembership": {
    "type": "string",
    "description": "Existing Membership"
   },
   "previousPurchase": {
    "type": "string",
    "description": "Previous Purchase"
   },
   "membershipHistory": {
    "type": "string",
    "description": "Membership History"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "promotionalQualification": {
    "type": "string",
    "description": "Promotional Qualification"
   },
   "residencyVerificationRequired": {
    "type": "boolean",
    "description": "Residency verification required"
   },
   "approvedCorporateAccountRequired": {
    "type": "boolean",
    "description": "Approved corporate account required"
   },
   "multipleMembershipsAllowed": {
    "type": "boolean",
    "description": "Multiple Memberships Allowed"
   },
   "oneMembershipPerCustomer": {
    "type": "string",
    "description": "One Membership per Customer"
   },
   "mutuallyExclusiveMemberships": {
    "type": "string",
    "description": "Mutually Exclusive Memberships"
   },
   "prerequisiteMembership": {
    "type": "string",
    "description": "Prerequisite Membership"
   },
   "existingTierRequirement": {
    "type": "string",
    "description": "Existing Tier Requirement"
   },
   "noVerification": {
    "type": "string",
    "description": "No Verification"
   },
   "customerDeclaration": {
    "type": "string",
    "description": "Customer Declaration"
   },
   "documentVerification": {
    "type": "string",
    "description": "Document Verification"
   },
   "identityVerification": {
    "type": "string",
    "description": "Identity Verification"
   },
   "staffVerification": {
    "type": "string",
    "description": "Staff Verification"
   },
   "externalVerification": {
    "type": "string",
    "description": "External Verification"
   },
   "allowDifferentRules": {
    "type": "boolean",
    "description": "Allow different rules"
   },
   "withAnExplanation": {
    "type": "string",
    "description": "with an explanation"
   }
  }
 },
 "MembershipEntitlementAdmissionBenefitBuilderInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table covers these fields** — the closest is control.webhook_delivery at 3%, so this is not an update to anything the package stores today and no new table has been decided",
  "description": "**What Membership Entitlement & Admission Benefit Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "unlimitedAdmission": {
    "type": "string",
    "description": "Unlimited Admission"
   },
   "limitedAdmissions": {
    "type": "string",
    "description": "Limited Admissions"
   },
   "attractionAccess": {
    "type": "string",
    "description": "Attraction Access"
   },
   "eventAccess": {
    "type": "string",
    "description": "Event Access"
   },
   "zoneAccess": {
    "type": "string",
    "description": "Zone Access"
   },
   "fastTrack": {
    "type": "string",
    "description": "Fast Track"
   },
   "priorityEntry": {
    "type": "string",
    "description": "Priority Entry"
   },
   "guestTickets": {
    "type": "string",
    "description": "Guest Tickets"
   },
   "parking": {
    "type": "string",
    "description": "Parking"
   },
   "fBBenefit": {
    "type": "string",
    "description": "F&B Benefit"
   },
   "retailBenefit": {
    "type": "string",
    "description": "Retail Benefit"
   },
   "rentalBenefit": {
    "type": "string",
    "description": "Rental Benefit"
   },
   "specialEventAccess": {
    "type": "string",
    "description": "Special Event Access"
   },
   "bookingPrivileges": {
    "type": "string",
    "description": "Booking Privileges"
   },
   "otherConfiguredBenefits": {
    "type": "string",
    "description": "Other Configured Benefits"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "attraction": {
    "type": "string",
    "description": "Attraction"
   },
   "eventType": {
    "type": "string",
    "description": "Event Type"
   },
   "admissionType": {
    "type": "string",
    "description": "Admission Type"
   },
   "numberOfVisits": {
    "type": "integer",
    "description": "Number of Visits"
   },
   "period": {
    "type": "string",
    "format": "date-time",
    "description": "Period"
   },
   "days": {
    "type": "string",
    "description": "Days"
   },
   "times": {
    "type": "string",
    "description": "Times"
   },
   "timeslots": {
    "type": "string",
    "description": "Timeslots"
   },
   "perDay": {
    "type": "string",
    "description": "Per Day"
   },
   "perWeek": {
    "type": "string",
    "description": "Per Week"
   },
   "perMonth": {
    "type": "string",
    "description": "Per Month"
   },
   "perMembershipYear": {
    "type": "string",
    "description": "Per Membership Year"
   },
   "lifetimeOfMembership": {
    "type": "string",
    "description": "Lifetime of Membership"
   },
   "unlimitedGeneralAdmission": {
    "type": "string",
    "description": "Unlimited General Admission"
   },
   "freeParking": {
    "type": "string",
    "description": "Free Parking"
   },
   "memberSpecific": {
    "type": "string",
    "description": "Member Specific"
   },
   "familyShared": {
    "type": "string",
    "description": "Family Shared"
   },
   "dependentSpecific": {
    "type": "string",
    "description": "Dependent Specific"
   },
   "accountShared": {
    "type": "string",
    "description": "Account Shared"
   }
  }
 },
 "MembershipEntitlementAdmissionBenefitBuilderView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Membership Entitlement & Admission Benefit Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "unlimitedAdmission": {
    "type": "string",
    "description": "Unlimited Admission"
   },
   "limitedAdmissions": {
    "type": "string",
    "description": "Limited Admissions"
   },
   "attractionAccess": {
    "type": "string",
    "description": "Attraction Access"
   },
   "eventAccess": {
    "type": "string",
    "description": "Event Access"
   },
   "zoneAccess": {
    "type": "string",
    "description": "Zone Access"
   },
   "fastTrack": {
    "type": "string",
    "description": "Fast Track"
   },
   "priorityEntry": {
    "type": "string",
    "description": "Priority Entry"
   },
   "guestTickets": {
    "type": "string",
    "description": "Guest Tickets"
   },
   "parking": {
    "type": "string",
    "description": "Parking"
   },
   "fBBenefit": {
    "type": "string",
    "description": "F&B Benefit"
   },
   "retailBenefit": {
    "type": "string",
    "description": "Retail Benefit"
   },
   "rentalBenefit": {
    "type": "string",
    "description": "Rental Benefit"
   },
   "specialEventAccess": {
    "type": "string",
    "description": "Special Event Access"
   },
   "bookingPrivileges": {
    "type": "string",
    "description": "Booking Privileges"
   },
   "otherConfiguredBenefits": {
    "type": "string",
    "description": "Other Configured Benefits"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "attraction": {
    "type": "string",
    "description": "Attraction"
   },
   "eventType": {
    "type": "string",
    "description": "Event Type"
   },
   "admissionType": {
    "type": "string",
    "description": "Admission Type"
   },
   "numberOfVisits": {
    "type": "integer",
    "description": "Number of Visits"
   },
   "period": {
    "type": "string",
    "format": "date-time",
    "description": "Period"
   },
   "days": {
    "type": "string",
    "description": "Days"
   },
   "times": {
    "type": "string",
    "description": "Times"
   },
   "timeslots": {
    "type": "string",
    "description": "Timeslots"
   },
   "perDay": {
    "type": "string",
    "description": "Per Day"
   },
   "perWeek": {
    "type": "string",
    "description": "Per Week"
   },
   "perMonth": {
    "type": "string",
    "description": "Per Month"
   },
   "perMembershipYear": {
    "type": "string",
    "description": "Per Membership Year"
   },
   "lifetimeOfMembership": {
    "type": "string",
    "description": "Lifetime of Membership"
   },
   "unlimitedGeneralAdmission": {
    "type": "string",
    "description": "Unlimited General Admission"
   },
   "freeParking": {
    "type": "string",
    "description": "Free Parking"
   },
   "memberSpecific": {
    "type": "string",
    "description": "Member Specific"
   },
   "familyShared": {
    "type": "string",
    "description": "Family Shared"
   },
   "dependentSpecific": {
    "type": "string",
    "description": "Dependent Specific"
   },
   "accountShared": {
    "type": "string",
    "description": "Account Shared"
   }
  }
 },
 "MembershipProductTierBuilderInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table covers these fields** — the closest is control.api_licence at 7%, so this is not an update to anything the package stores today and no new table has been decided",
  "description": "**What Membership Product & Tier Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "membershipName": {
    "type": "string",
    "description": "Membership Name"
   },
   "membershipCode": {
    "type": "string",
    "description": "Membership Code"
   },
   "description": {
    "type": "string",
    "description": "Description"
   },
   "membershipType": {
    "type": "string",
    "description": "Membership Type"
   },
   "brand": {
    "type": "string",
    "description": "Brand"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "attraction": {
    "type": "string",
    "description": "Attraction"
   },
   "market": {
    "type": "string",
    "description": "Market"
   },
   "currencyContext": {
    "type": "string",
    "description": "Currency Context"
   },
   "effectiveFrom": {
    "type": "string",
    "description": "Effective From"
   },
   "effectiveTo": {
    "type": "string",
    "description": "Effective To"
   },
   "standard": {
    "type": "string",
    "description": "Standard"
   },
   "silver": {
    "type": "string",
    "description": "Silver"
   },
   "gold": {
    "type": "string",
    "description": "Gold"
   },
   "platinum": {
    "type": "string",
    "description": "Platinum"
   },
   "vip": {
    "type": "string",
    "description": "VIP"
   },
   "customTiers": {
    "type": "string",
    "description": "Custom Tiers"
   },
   "tierLevel": {
    "type": "string",
    "description": "Tier Level"
   },
   "displayOrder": {
    "type": "string",
    "description": "Display Order"
   },
   "parentMembership": {
    "type": "string",
    "description": "Parent Membership"
   },
   "replacementMembership": {
    "type": "string",
    "description": "Replacement Membership"
   },
   "individualFamilyCorporate": {
    "type": "string",
    "description": "Individual / Family / Corporate"
   },
   "namedTransferable": {
    "type": "string",
    "description": "Named / Transferable"
   },
   "physicalDigital": {
    "type": "string",
    "description": "Physical / Digital"
   },
   "renewableNonRenewable": {
    "type": "string",
    "description": "Renewable / Non-Renewable"
   },
   "autoRenewEligible": {
    "type": "string",
    "description": "Auto-Renew Eligible"
   },
   "admissionBasedBenefitBasedHybrid": {
    "type": "string",
    "description": "Admission-Based / Benefit-Based / Hybrid"
   },
   "contracts": {
    "type": "string",
    "description": "contracts"
   }
  }
 },
 "MembershipProductTierBuilderView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Membership Product & Tier Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "membershipName": {
    "type": "string",
    "description": "Membership Name"
   },
   "membershipCode": {
    "type": "string",
    "description": "Membership Code"
   },
   "description": {
    "type": "string",
    "description": "Description"
   },
   "membershipType": {
    "type": "string",
    "description": "Membership Type"
   },
   "brand": {
    "type": "string",
    "description": "Brand"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "attraction": {
    "type": "string",
    "description": "Attraction"
   },
   "market": {
    "type": "string",
    "description": "Market"
   },
   "currencyContext": {
    "type": "string",
    "description": "Currency Context"
   },
   "effectiveFrom": {
    "type": "string",
    "description": "Effective From"
   },
   "effectiveTo": {
    "type": "string",
    "description": "Effective To"
   },
   "standard": {
    "type": "string",
    "description": "Standard"
   },
   "silver": {
    "type": "string",
    "description": "Silver"
   },
   "gold": {
    "type": "string",
    "description": "Gold"
   },
   "platinum": {
    "type": "string",
    "description": "Platinum"
   },
   "vip": {
    "type": "string",
    "description": "VIP"
   },
   "customTiers": {
    "type": "string",
    "description": "Custom Tiers"
   },
   "tierLevel": {
    "type": "string",
    "description": "Tier Level"
   },
   "displayOrder": {
    "type": "string",
    "description": "Display Order"
   },
   "parentMembership": {
    "type": "string",
    "description": "Parent Membership"
   },
   "replacementMembership": {
    "type": "string",
    "description": "Replacement Membership"
   },
   "individualFamilyCorporate": {
    "type": "string",
    "description": "Individual / Family / Corporate"
   },
   "namedTransferable": {
    "type": "string",
    "description": "Named / Transferable"
   },
   "physicalDigital": {
    "type": "string",
    "description": "Physical / Digital"
   },
   "renewableNonRenewable": {
    "type": "string",
    "description": "Renewable / Non-Renewable"
   },
   "autoRenewEligible": {
    "type": "string",
    "description": "Auto-Renew Eligible"
   },
   "admissionBasedBenefitBasedHybrid": {
    "type": "string",
    "description": "Admission-Based / Benefit-Based / Hybrid"
   },
   "contracts": {
    "type": "string",
    "description": "contracts"
   }
  }
 },
 "MembershipProductValidationApprovalPublicationVersioInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Membership Product Validation, Approval, Publication & Versioning submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "productDefinitionComplete": {
    "type": "string",
    "description": "Product Definition Complete"
   },
   "catalogueAssociation": {
    "type": "string",
    "description": "Catalogue Association"
   },
   "eligibilityRules": {
    "type": "string",
    "description": "Eligibility Rules"
   },
   "validity": {
    "type": "string",
    "description": "Validity"
   },
   "activation": {
    "type": "string",
    "description": "Activation"
   },
   "entitlements": {
    "type": "string",
    "description": "Entitlements"
   },
   "usageRules": {
    "type": "string",
    "description": "Usage Rules"
   },
   "pricingAssociation": {
    "type": "string",
    "description": "Pricing Association"
   },
   "taxFeeAssociation": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Tax/Fee Association"
   },
   "channelAvailability": {
    "type": "string",
    "description": "Channel Availability"
   },
   "renewalPolicy": {
    "type": "string",
    "description": "Renewal Policy"
   },
   "requiredCredentialConfiguration": {
    "type": "string",
    "description": "Required Credential Configuration"
   },
   "allowFutureConfigurationChanges": {
    "type": "boolean",
    "description": "Allow future configuration changes"
   },
   "effective1Jan": {
    "type": "string",
    "description": "Effective 1 Jan"
   },
   "configuredMigrationPolicy": {
    "type": "string",
    "description": "configured migration policy"
   },
   "activeMembersAffected": {
    "type": "integer",
    "description": "Active Members Affected"
   },
   "futureRenewals": {
    "type": "string",
    "description": "Future Renewals"
   },
   "entitlementsAffected": {
    "type": "string",
    "description": "Entitlements Affected"
   },
   "channels": {
    "type": "string",
    "description": "Channels"
   },
   "pricingDependencies": {
    "type": "string",
    "description": "Pricing Dependencies"
   },
   "accessDependencies": {
    "type": "string",
    "description": "Access Dependencies"
   },
   "b2c": {
    "type": "string",
    "description": "B2C"
   },
   "pos": {
    "type": "string",
    "description": "POS"
   },
   "mobileApp": {
    "type": "string",
    "description": "Mobile App"
   },
   "callCenter": {
    "type": "string",
    "description": "Call Center"
   },
   "b2b": {
    "type": "string",
    "description": "B2B"
   },
   "accessControl": {
    "type": "string",
    "description": "Access Control"
   },
   "ticketing": {
    "type": "string",
    "description": "Ticketing"
   },
   "otherDependentServices": {
    "type": "string",
    "description": "Other dependent services"
   },
   "membershipPass": {
    "type": "string",
    "description": "membership/pass?”"
   },
   "intelligence": {
    "type": "string",
    "description": "& Intelligence"
   }
  }
 },
 "MembershipProductValidationApprovalPublicationVersioView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Membership Product Validation, Approval, Publication & Versioning displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "productDefinitionComplete": {
    "type": "string",
    "description": "Product Definition Complete"
   },
   "catalogueAssociation": {
    "type": "string",
    "description": "Catalogue Association"
   },
   "eligibilityRules": {
    "type": "string",
    "description": "Eligibility Rules"
   },
   "validity": {
    "type": "string",
    "description": "Validity"
   },
   "activation": {
    "type": "string",
    "description": "Activation"
   },
   "entitlements": {
    "type": "string",
    "description": "Entitlements"
   },
   "usageRules": {
    "type": "string",
    "description": "Usage Rules"
   },
   "pricingAssociation": {
    "type": "string",
    "description": "Pricing Association"
   },
   "taxFeeAssociation": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Tax/Fee Association"
   },
   "channelAvailability": {
    "type": "string",
    "description": "Channel Availability"
   },
   "renewalPolicy": {
    "type": "string",
    "description": "Renewal Policy"
   },
   "requiredCredentialConfiguration": {
    "type": "string",
    "description": "Required Credential Configuration"
   },
   "allowFutureConfigurationChanges": {
    "type": "boolean",
    "description": "Allow future configuration changes"
   },
   "effective1Jan": {
    "type": "string",
    "description": "Effective 1 Jan"
   },
   "configuredMigrationPolicy": {
    "type": "string",
    "description": "configured migration policy"
   },
   "activeMembersAffected": {
    "type": "integer",
    "description": "Active Members Affected"
   },
   "futureRenewals": {
    "type": "string",
    "description": "Future Renewals"
   },
   "entitlementsAffected": {
    "type": "string",
    "description": "Entitlements Affected"
   },
   "channels": {
    "type": "string",
    "description": "Channels"
   },
   "pricingDependencies": {
    "type": "string",
    "description": "Pricing Dependencies"
   },
   "accessDependencies": {
    "type": "string",
    "description": "Access Dependencies"
   },
   "b2c": {
    "type": "string",
    "description": "B2C"
   },
   "pos": {
    "type": "string",
    "description": "POS"
   },
   "mobileApp": {
    "type": "string",
    "description": "Mobile App"
   },
   "callCenter": {
    "type": "string",
    "description": "Call Center"
   },
   "b2b": {
    "type": "string",
    "description": "B2B"
   },
   "accessControl": {
    "type": "string",
    "description": "Access Control"
   },
   "ticketing": {
    "type": "string",
    "description": "Ticketing"
   },
   "otherDependentServices": {
    "type": "string",
    "description": "Other dependent services"
   },
   "membershipPass": {
    "type": "string",
    "description": "membership/pass?”"
   },
   "intelligence": {
    "type": "string",
    "description": "& Intelligence"
   }
  }
 },
 "MembershipUsageVisitConsumptionRulesView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Membership Usage, Visit & Consumption Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "maximumVisitsPerDay": {
    "type": "string",
    "description": "Maximum Visits per Day"
   },
   "maximumAdmissionsPerPeriod": {
    "type": "string",
    "format": "date-time",
    "description": "Maximum Admissions per Period"
   },
   "sameDayReEntry": {
    "type": "string",
    "description": "Same-Day Re-entry"
   },
   "reEntryCooldown": {
    "type": "string",
    "description": "Re-entry Cooldown"
   },
   "concurrentReservations": {
    "type": "string",
    "description": "Concurrent Reservations"
   },
   "advanceBookingLimit": {
    "type": "integer",
    "description": "Advance Booking Limit"
   },
   "noShowTreatment": {
    "type": "string",
    "description": "No-Show Treatment"
   },
   "cancellationLimit": {
    "type": "integer",
    "description": "Cancellation Limit"
   },
   "guestUsage": {
    "type": "string",
    "description": "Guest Usage"
   },
   "benefitConsumption": {
    "type": "string",
    "description": "Benefit Consumption"
   },
   "reservationRequired": {
    "type": "boolean",
    "description": "Reservation Required"
   },
   "reservationOptional": {
    "type": "string",
    "description": "Reservation Optional"
   },
   "walkInAllowed": {
    "type": "boolean",
    "description": "Walk-In Allowed"
   },
   "maximumAdvanceBookingDays": {
    "type": "string",
    "description": "Maximum Advance Booking Days"
   },
   "maximumActiveFutureReservations": {
    "type": "string",
    "description": "Maximum Active Future Reservations"
   },
   "unlimitedSameDayReEntry": {
    "type": "string",
    "description": "Unlimited Same-Day Re-entry"
   },
   "noReEntry": {
    "type": "string",
    "description": "No Re-entry"
   },
   "reEntryAfterXMinutes": {
    "type": "string",
    "description": "Re-entry After X Minutes"
   },
   "venueSpecificRule": {
    "type": "string",
    "description": "Venue-Specific Rule"
   },
   "but": {
    "type": "string",
    "description": "but"
   },
   "parking12UsesThisYear": {
    "type": "string",
    "description": "Parking: 12 uses this year"
   },
   "rules": {
    "type": "string",
    "description": "rules"
   }
  }
 },
 "RenewalAutoRenewalMembershipContinuityConfigurationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Renewal, Auto-Renewal & Membership Continuity Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "manualRenewal": {
    "type": "string",
    "description": "Manual Renewal"
   },
   "customerSelfServiceRenewal": {
    "type": "string",
    "description": "Customer Self-Service Renewal"
   },
   "agentAssistedRenewal": {
    "type": "string",
    "description": "Agent-Assisted Renewal"
   },
   "autoRenewal": {
    "type": "string",
    "description": "Auto-Renewal"
   },
   "invitationOnlyRenewal": {
    "type": "string",
    "description": "Invitation-Only Renewal"
   },
   "nonRenewable": {
    "type": "string",
    "description": "Non-Renewable"
   },
   "through": {
    "type": "string",
    "description": "through"
   },
   "eligibleProducts": {
    "type": "string",
    "description": "Eligible Products"
   },
   "consentRequirement": {
    "type": "string",
    "description": "Consent Requirement"
   },
   "paymentMethodRequirement": {
    "type": "string",
    "description": "Payment Method Requirement"
   },
   "preRenewalNotification": {
    "type": "string",
    "description": "Pre-Renewal Notification"
   },
   "failureHandling": {
    "type": "string",
    "description": "Failure Handling"
   },
   "currentMembershipPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Current Membership Price"
   },
   "protectedRenewalPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Protected Renewal Price"
   },
   "renewalDiscount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Renewal Discount"
   },
   "loyaltyRate": {
    "type": "number",
    "description": "Loyalty Rate"
   },
   "fixedRenewalRate": {
    "type": "number",
    "description": "Fixed Renewal Rate"
   },
   "age": {
    "type": "string",
    "description": "Age"
   },
   "residency": {
    "type": "string",
    "description": "Residency"
   },
   "membershipStatus": {
    "type": "string",
    "description": "Membership Status"
   },
   "outstandingBalance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Outstanding Balance"
   },
   "qualification": {
    "type": "string",
    "description": "Qualification"
   },
   "corporateAssociation": {
    "type": "string",
    "description": "Corporate Association"
   },
   "sameTierOnly": {
    "type": "string",
    "description": "Same Tier Only"
   },
   "suggestedTier": {
    "type": "string",
    "description": "Suggested Tier"
   }
  }
 },
 "RenewalAutoRenewalMembershipContinuityConfigurationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Renewal, Auto-Renewal & Membership Continuity Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "manualRenewal": {
    "type": "string",
    "description": "Manual Renewal"
   },
   "customerSelfServiceRenewal": {
    "type": "string",
    "description": "Customer Self-Service Renewal"
   },
   "agentAssistedRenewal": {
    "type": "string",
    "description": "Agent-Assisted Renewal"
   },
   "autoRenewal": {
    "type": "string",
    "description": "Auto-Renewal"
   },
   "invitationOnlyRenewal": {
    "type": "string",
    "description": "Invitation-Only Renewal"
   },
   "nonRenewable": {
    "type": "string",
    "description": "Non-Renewable"
   },
   "through": {
    "type": "string",
    "description": "through"
   },
   "eligibleProducts": {
    "type": "string",
    "description": "Eligible Products"
   },
   "consentRequirement": {
    "type": "string",
    "description": "Consent Requirement"
   },
   "paymentMethodRequirement": {
    "type": "string",
    "description": "Payment Method Requirement"
   },
   "preRenewalNotification": {
    "type": "string",
    "description": "Pre-Renewal Notification"
   },
   "failureHandling": {
    "type": "string",
    "description": "Failure Handling"
   },
   "currentMembershipPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Current Membership Price"
   },
   "protectedRenewalPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Protected Renewal Price"
   },
   "renewalDiscount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Renewal Discount"
   },
   "loyaltyRate": {
    "type": "number",
    "description": "Loyalty Rate"
   },
   "fixedRenewalRate": {
    "type": "number",
    "description": "Fixed Renewal Rate"
   },
   "age": {
    "type": "string",
    "description": "Age"
   },
   "residency": {
    "type": "string",
    "description": "Residency"
   },
   "membershipStatus": {
    "type": "string",
    "description": "Membership Status"
   },
   "outstandingBalance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Outstanding Balance"
   },
   "qualification": {
    "type": "string",
    "description": "Qualification"
   },
   "corporateAssociation": {
    "type": "string",
    "description": "Corporate Association"
   },
   "sameTierOnly": {
    "type": "string",
    "description": "Same Tier Only"
   },
   "suggestedTier": {
    "type": "string",
    "description": "Suggested Tier"
   }
  }
 },
 "ValidityActivationExpiryConfigurationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Validity, Activation & Expiry Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "immediateOnPurchase": {
    "type": "string",
    "description": "Immediate on Purchase"
   },
   "fixedStartDate": {
    "type": "string",
    "format": "date-time",
    "description": "Fixed Start Date"
   },
   "firstVisit": {
    "type": "string",
    "description": "First Visit"
   },
   "manualActivation": {
    "type": "string",
    "description": "Manual Activation"
   },
   "customerActivation": {
    "type": "string",
    "description": "Customer Activation"
   },
   "configuredStart": {
    "type": "string",
    "description": "Configured start"
   },
   "configuredEnd": {
    "type": "string",
    "description": "Configured end"
   }
  }
 },
 "ValidityActivationExpiryConfigurationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Validity, Activation & Expiry Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "immediateOnPurchase": {
    "type": "string",
    "description": "Immediate on Purchase"
   },
   "fixedStartDate": {
    "type": "string",
    "format": "date-time",
    "description": "Fixed Start Date"
   },
   "firstVisit": {
    "type": "string",
    "description": "First Visit"
   },
   "manualActivation": {
    "type": "string",
    "description": "Manual Activation"
   },
   "customerActivation": {
    "type": "string",
    "description": "Customer Activation"
   },
   "configuredStart": {
    "type": "string",
    "description": "Configured start"
   },
   "configuredEnd": {
    "type": "string",
    "description": "Configured end"
   }
  }
 }
}
```
