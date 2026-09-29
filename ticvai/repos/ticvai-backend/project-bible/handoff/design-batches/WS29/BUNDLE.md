# WS29 — Membership   Annual Pass Management board 1

**10 screens · 19 operations · 26 schemas · 6 permissions**

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

- **Every control that can be refused must be gated.** 6 permissions apply here:
  `PLATFORM_CELL_MANAGE, PLATFORM_TENANT_VIEW, PRICE_CONFIGURE, PRICE_VIEW, PRODUCT_CONFIGURE, PRODUCT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-284` | Membership & Annual Pass Command Center | listDetail | 2 | 1 | — |
| `BO-285` | Membership Product & Tier Builder | configEditor | 2 | 0 | — |
| `BO-286` | Membership Eligibility & Qualification Rule Builder | configEditor | 1 | 0 | — |
| `BO-287` | Validity, Activation & Expiry Configuration | listDetail | 1 | 0 | — |
| `BO-288` | Membership Entitlement & Admission Benefit Builder | configEditor | 4 | 0 | — |
| `BO-289` | Membership Usage, Visit & Consumption Rules | listDetail | 4 | 1 | — |
| `BO-290` | Family, Household & Dependent Membership Configuration | configEditor | 1 | 0 | — |
| `BO-291` | Membership Commercial, Pricing & Channel Association | configEditor | 5 | 1 | — |
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
     "provenance": "derived — BO-100 declares entryState.params  and BO-284 holds none of them, so the edge carries nothing and BO-100 opens cold"
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
  "purposeNote": "Administrators can view, search and manage the complete portfolio of membership and annual-pass products from one workspace.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display; Identify) and no metric row",
  "purpose": "Provide administrators with a centralized view of all membership, annual pass, season pass and subscription-style admission products.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Active Membership Products",
       "bindsTo": "MembershipAnnualPassCommandCenterSummary.activeMembershipProducts",
       "operation": "listMembershipAnnualPass",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Annual Pass Products",
       "bindsTo": "MembershipAnnualPassCommandCenterSummary.annualPassProducts",
       "operation": "listMembershipAnnualPass",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Draft Products",
       "bindsTo": "MembershipAnnualPassCommandCenterSummary.draftProducts",
       "operation": "listMembershipAnnualPass",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Active Members",
       "bindsTo": "MembershipAnnualPassCommandCenterSummary.activeMembers",
       "operation": "listMembershipAnnualPass",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Family Memberships",
       "bindsTo": "MembershipAnnualPassCommandCenterSummary.familyMemberships",
       "operation": "listMembershipAnnualPass",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Memberships expiring soon",
       "bindsTo": "MembershipAnnualPassCommandCenterSummary.membershipsExpiringSoon",
       "operation": "listMembershipAnnualPass",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Renewal-Enabled Products",
       "bindsTo": "MembershipAnnualPassCommandCenterSummary.renewalEnabledProducts",
       "operation": "listMembershipAnnualPass",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Suspended Products",
       "bindsTo": "MembershipAnnualPassCommandCenterSummary.suspendedProducts",
       "operation": "listMembershipAnnualPass",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Products with configuration issues",
       "bindsTo": "MembershipAnnualPassCommandCenterSummary.productsWithConfigurationIssues",
       "operation": "listMembershipAnnualPass",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Average membership duration",
       "bindsTo": "MembershipAnnualPassCommandCenterSummary.averageMembershipDuration",
       "operation": "listMembershipAnnualPass",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every membership annual pass",
       "columns": [
        "MembershipAnnualPassCommandCenterView.productId",
        "MembershipAnnualPassCommandCenterView.membershipName",
        "MembershipAnnualPassCommandCenterView.type",
        "MembershipAnnualPassCommandCenterView.tier",
        "MembershipAnnualPassCommandCenterView.venueAttraction",
        "MembershipAnnualPassCommandCenterView.validityMethod",
        "MembershipAnnualPassCommandCenterView.activationMethod",
        "MembershipAnnualPassCommandCenterView.renewalMode",
        "MembershipAnnualPassCommandCenterView.membershipStructure",
        "MembershipAnnualPassCommandCenterView.currentMembers",
        "MembershipAnnualPassCommandCenterView.effectiveFrom",
        "MembershipAnnualPassCommandCenterView.status",
        "MembershipAnnualPassCommandCenterView.owner",
        "MembershipAnnualPassCommandCenterView.validationIssues"
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
        "MembershipAnnualPassCommandCenterView.productId",
        "MembershipAnnualPassCommandCenterView.membershipName",
        "MembershipAnnualPassCommandCenterView.type",
        "MembershipAnnualPassCommandCenterView.tier",
        "MembershipAnnualPassCommandCenterView.venueAttraction",
        "MembershipAnnualPassCommandCenterView.validityMethod",
        "MembershipAnnualPassCommandCenterView.activationMethod",
        "MembershipAnnualPassCommandCenterView.renewalMode",
        "MembershipAnnualPassCommandCenterView.membershipStructure",
        "MembershipAnnualPassCommandCenterView.currentMembers",
        "MembershipAnnualPassCommandCenterView.effectiveFrom",
        "MembershipAnnualPassCommandCenterView.status",
        "MembershipAnnualPassCommandCenterView.owner",
        "MembershipAnnualPassCommandCenterView.validationIssues"
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
      },
      {
       "kind": "destructiveButton",
       "label": "Suspend membership product",
       "operation": "approveMembershipProductValidation",
       "permission": "PLATFORM_CELL_MANAGE",
       "notes": "Quick action: sends `action: suspend` with a `reason`. Allowed only on an `active` version; selling stops on every channel at once and members already holding it keep their entitlements until their own expiry (decided 29 September, writers pass; DM4).",
       "provenance": "contract subscription.yaml PUT /membership-product-validation"
      },
      {
       "kind": "secondaryButton",
       "label": "Reinstate membership product",
       "operation": "approveMembershipProductValidation",
       "permission": "PLATFORM_CELL_MANAGE",
       "notes": "Quick action: sends `action: reinstate`, moving a `suspended` version back to `active`; refused once its `effectiveTo` has passed (decided 29 September, writers pass; DM4).",
       "provenance": "contract subscription.yaml PUT /membership-product-validation"
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
   },
   {
    "operationId": "approveMembershipProductValidation",
    "contract": "subscription",
    "purpose": "Membership Product Validation, Approval, Publication & Versioning",
    "trigger": "onAction",
    "invalidates": [
     "listMembershipAnnualPass"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "MembershipAnnualPassCommandCenterSummary.activeMembershipProducts",
    "MembershipAnnualPassCommandCenterSummary.annualPassProducts",
    "MembershipAnnualPassCommandCenterSummary.draftProducts",
    "MembershipAnnualPassCommandCenterSummary.activeMembers",
    "MembershipAnnualPassCommandCenterSummary.familyMemberships",
    "MembershipAnnualPassCommandCenterSummary.membershipsExpiringSoon"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-284",
   "workshopBoard": "wireframes/WS82 Membership   Annual Pass Management Board 1.dc.html#bo-284"
  },
  "apisNote": "Regenerated 9 September 2026 from Membership___Annual_Pass_Management_Reference.pdf page 4. 29 of 29 labels bound to a contract property; 45 of 53 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Monthly Membership, Fixed-Term Membership, Corporate Membership, Family Membership, Individual Membership, Student Membership, VIP Membership, Custom Membership … are choices sent by `listMembershipAnnualPass`.",
  "overlays": [
   {
    "id": "confirmSuspendMembershipProduct",
    "component": "confirmDialog",
    "trigger": "Suspend membership product",
    "body": "**Names what suspending stops and what it leaves alone**: the membership product and version, every channel it stops selling on, and that members already holding it keep their entitlements until their own expiry. **Collects what `approveMembershipProductValidation` sends before it is called.** Required: `membershipCode`, `action` (`suspend`), `reason`.",
    "bindsTo": "MembershipProductValidationApprovalPublicationVersioInput",
    "provenance": "contract subscription.yaml PUT /membership-product-validation"
   }
  ],
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
  "purposeNote": "Administrators can create and version membership products and tiers with clear relationships to the central TICVAI product catalogue.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture; Define; Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure the fundamental definition and hierarchy of a membership/pass.",
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
    "trigger": "onAction"
   },
   {
    "operationId": "setMembershipProgramme",
    "contract": "catalogue",
    "purpose": "Define a membership programme",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-285",
   "workshopBoard": "wireframes/WS82 Membership   Annual Pass Management Board 1.dc.html#bo-285"
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
  "purposeNote": "rules and returns an explainable result.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure; Configure whether qualification requires) and no display directory — it is settings, not a population",
  "purpose": "Determine who is allowed to purchase, activate, hold or renew a particular membership.",
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
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-286",
   "workshopBoard": "wireframes/WS82 Membership   Annual Pass Management Board 1.dc.html#bo-286"
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
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-287",
   "workshopBoard": "wireframes/WS82 Membership   Annual Pass Management Board 1.dc.html#bo-287"
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
  "purposeNote": "Administrators can define the complete admission and benefit package associated with every membership tier.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Define exactly what the member receives. This is the heart of the membership product.",
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
       "label": "Attraction Access",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 9 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Event Access",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 9 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Zone Access",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 9 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Priority Entry",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 9 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Guest Tickets",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 9 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "F&B Benefit",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 9 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Retail Benefit",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 9 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Rental Benefit",
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
    "trigger": "onAction"
   },
   {
    "operationId": "setMembershipBenefit",
    "contract": "catalogue",
    "purpose": "Define a benefit",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   },
   {
    "operationId": "setPlanBenefits",
    "contract": "catalogue",
    "purpose": "Replace the benefits a plan grants",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   },
   {
    "operationId": "listEntitlementTemplates",
    "contract": "catalogue",
    "purpose": "The membership plan templates whose benefits are set",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-288",
   "workshopBoard": "wireframes/WS82 Membership   Annual Pass Management Board 1.dc.html#bo-288"
  },
  "apisNote": "Regenerated 9 September 2026 from Membership___Annual_Pass_Management_Reference.pdf page 9. 0 of 0 labels bound to a contract property; 24 of 45 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Attraction Access, Event Access, Zone Access, Priority Entry, Guest Tickets, F&B Benefit, Retail Benefit, Rental Benefit … are choices sent by `setMembershipEntitlementAdmission`.",
  "entryState": {
   "params": [
    {
     "name": "templateId",
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
  "purposeNote": "Membership entitlement usage is governed consistently across reservation, ticketing and access-control channels.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Maintain counters such as) and no metric row",
  "purpose": "Control how membership entitlements may actually be consumed. Screen 13.1.5 defines what the member receives. Screen 13.1.6 defines how it may be used.",
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
       "notes": "The pack groups this record's detail under its own headings: “Unlimited annual visits”, “Access Integration”.",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 11 §Maintain counters such as"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save membership usage policy",
       "operation": "setMembershipUsagePolicy",
       "permission": "PLATFORM_CELL_MANAGE",
       "notes": "The writer for the rules BO-289 shows through listMembershipUsageVisit: visit and admission limits, re-entry, reservations, no-show treatment, cancellations and guest usage for one membership product version, one row of subscription.membership_usage_policy per version (decided 29 September, writers pass; DM4).",
       "provenance": "contract subscription.yaml PUT /membership-usage-policy"
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
   },
   {
    "operationId": "setPlanBenefits",
    "contract": "catalogue",
    "purpose": "Save the usage limit and period of each benefit a plan grants",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   },
   {
    "operationId": "listEntitlementTemplates",
    "contract": "catalogue",
    "purpose": "The membership plan templates whose usage rules are set",
    "trigger": "onLoad"
   },
   {
    "operationId": "setMembershipUsagePolicy",
    "contract": "subscription",
    "purpose": "Save a membership product's usage, visit and consumption rules",
    "trigger": "onAction",
    "invalidates": [
     "listMembershipUsageVisit",
     "listEntitlementTemplates"
    ]
   }
  ],
  "entryState": {
   "preloaded": [],
   "params": [
    {
     "name": "templateId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-289",
   "workshopBoard": "wireframes/WS82 Membership   Annual Pass Management Board 1.dc.html#bo-289"
  },
  "apisNote": "Regenerated 9 September 2026 from Membership___Annual_Pass_Management_Reference.pdf page 11. 1 of 1 labels bound to a contract property; 20 of 32 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formSetMembershipUsagePolicy",
    "component": "modal",
    "trigger": "Save membership usage policy",
    "body": "**Collects what `setMembershipUsagePolicy` sends before it is called.** Required: `membershipCode`, `reEntryPolicy`, `reservationRequirement`. Optional: `tier`, `maximumVisitsPerDay`, `maximumAdmissionsPerPeriod`, `admissionPeriod`, `reEntryCooldownMinutes`, `walkInAllowed`, `maximumAdvanceBookingDays`, `maximumActiveFutureReservations`, `concurrentReservations`, `noShowTreatment`, `noShowThreshold`, `noShowWindowDays` and 4 more. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "MembershipUsagePolicyInput",
    "confirm": {
     "label": "Save membership usage policy",
     "operation": "setMembershipUsagePolicy"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "membershipCode",
      "reEntryPolicy",
      "reservationRequirement",
      "tier",
      "maximumVisitsPerDay",
      "maximumAdmissionsPerPeriod",
      "admissionPeriod",
      "reEntryCooldownMinutes",
      "walkInAllowed",
      "maximumAdvanceBookingDays",
      "maximumActiveFutureReservations",
      "concurrentReservations",
      "noShowTreatment",
      "noShowThreshold",
      "noShowWindowDays",
      "noShowRestrictionDays",
      "cancellationLimit",
      "guestUsage"
     ]
    },
    "provenance": "contract subscription.yaml PUT /membership-usage-policy"
   }
  ],
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
  "purposeNote": "roles, eligibility and shared/individual entitlements.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure; Possible configured action) and no display directory — it is settings, not a population",
  "purpose": "Support memberships covering more than one person while preserving individual identities and entitlements.",
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
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-290",
   "workshopBoard": "wireframes/WS82 Membership   Annual Pass Management Board 1.dc.html#bo-290"
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
  "purposeNote": "Membership products can be commercially sold across authorized channels using centrally governed pricing, tax, fee and payment services.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure sale through; Configure) and no display directory — it is settings, not a population",
  "purpose": "Connect the membership contract to TICVAI's central commercial engines without duplicating pricing configuration.",
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
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "publishGate",
       "label": "What publishing changes",
       "operation": "publishChannelAvailability",
       "notes": "**Names the membership products, the channels they go on or come off, and from when**, before it runs. A publish with no stated consequence is one somebody presses meaning to save.",
       "provenance": "contract catalogue.yaml PUT /channel-availability (authored: required by check-screens)"
      },
      {
       "kind": "primaryButton",
       "label": "Save membership commercial config",
       "operation": "setMembershipCommercialConfig",
       "permission": "PLATFORM_CELL_MANAGE",
       "notes": "The writer for the commercial columns BO-291 shows through listMembershipCommercialPricing: `basePricingProfile`, `taxProfile`, `feeProfile`, `upgradePricePolicy`, `promotionalPricingEligibility`, `paymentTerms` and `salesPeriod` on subscription.membership_product (decided 29 September, writers pass; DM4).",
       "provenance": "contract subscription.yaml PUT /membership-commercial-config"
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
   },
   {
    "operationId": "setPrices",
    "contract": "catalogue",
    "purpose": "Set the membership price in a price list",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   },
   {
    "operationId": "publishChannelAvailability",
    "contract": "catalogue",
    "purpose": "Choose the channels that sell the membership",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   },
   {
    "operationId": "listPriceLists",
    "contract": "catalogue",
    "purpose": "The price lists a membership is priced on",
    "trigger": "onLoad"
   },
   {
    "operationId": "setMembershipCommercialConfig",
    "contract": "subscription",
    "purpose": "Save a membership product's commercial references, payment eligibility and sales period",
    "trigger": "onAction",
    "invalidates": [
     "listMembershipCommercialPricing",
     "listPriceLists"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-291",
   "workshopBoard": "wireframes/WS82 Membership   Annual Pass Management Board 1.dc.html#bo-291"
  },
  "apisNote": "Regenerated 9 September 2026 from Membership___Annual_Pass_Management_Reference.pdf page 14. 0 of 0 labels bound to a contract property; 15 of 38 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "priceListId",
     "from": "navigation"
    }
   ]
  },
  "overlays": [
   {
    "id": "formSetMembershipCommercialConfig",
    "component": "modal",
    "trigger": "Save membership commercial config",
    "body": "**Collects what `setMembershipCommercialConfig` sends before it is called.** Required: `membershipCode`, `basePricingProfile`, `taxProfile`, `salesPeriod`. Optional: `feeProfile`, `upgradePricePolicy`, `promotionalPricingEligibility`, `paymentTerms`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "MembershipCommercialConfigInput",
    "confirm": {
     "label": "Save membership commercial config",
     "operation": "setMembershipCommercialConfig"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "membershipCode",
      "basePricingProfile",
      "taxProfile",
      "salesPeriod",
      "feeProfile",
      "upgradePricePolicy",
      "promotionalPricingEligibility",
      "paymentTerms"
     ]
    },
    "provenance": "contract subscription.yaml PUT /membership-commercial-config"
   }
  ],
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
  "purposeNote": "continuity, commercial terms and required customer consent.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure; At renewal, configure whether) and no display directory — it is settings, not a population",
  "purpose": "Define how a membership moves from one validity period into the next.",
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
       "label": "Manual Renewal",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 15 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Customer Self-Service Renewal",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 15 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Agent-Assisted Renewal",
       "provenance": "pack Membership___Annual_Pass_Management_Reference.pdf, page 15 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Invitation-Only Renewal",
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
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-292",
   "workshopBoard": "wireframes/WS82 Membership   Annual Pass Management Board 1.dc.html#bo-292"
  },
  "apisNote": "Regenerated 9 September 2026 from Membership___Annual_Pass_Management_Reference.pdf page 15. 0 of 0 labels bound to a contract property; 15 of 37 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Pack actions reconciled 29 September (VM close-out):** Manual Renewal, Customer Self-Service Renewal, Agent-Assisted Renewal, Invitation-Only Renewal are choices sent by `setRenewalAutoMembership`.",
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
  "purposeNote": "Only validated, approved and correctly versioned membership configurations can become commercially active, with complete impact and audit history. Board 1 — Final Screen Register # Backend Screen Core Responsibility 13.1. Membership & Annual Pass Command Center Portfolio management 1 13.1. Membership Product & Tier Builder Product/tier definition 2 13.1. Membership Eligibility & Qualification Rule Builder Member eligibility 3 13.1. Validity, Activation & Expiry Configuration Membership lifecycle 4 13.1. Benefits and Membership Entitlement & Admission Benefit Builder 5 entitlements 13.1. Member",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Synchronize relevant configuration with; AI Configuration Review) and no display directory — it is settings, not a population",
  "purpose": "Provide the final governance layer before a membership/pass configuration becomes commercially available.",
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
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P08 Venue Management.dc.html#bo-293",
   "workshopBoard": "wireframes/WS82 Membership   Annual Pass Management Board 1.dc.html#bo-293"
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "MembershipProductValidationApprovalPublicationVersioInput",
  "responds": "MembershipProductValidationApprovalPublicationVersioView"
 },
 "listEntitlementTemplates": {
  "method": "GET",
  "path": "/entitlement-templates",
  "contract": "catalogue",
  "summary": "List entitlement templates",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "EntitlementTemplate"
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
  "parameters": [
   {
    "name": "membershipType",
    "in": "query",
    "required": false
   },
   {
    "name": "status",
    "in": "query",
    "required": false
   },
   {
    "name": "tier",
    "in": "query",
    "required": false
   },
   {
    "name": "venue",
    "in": "query",
    "required": false
   },
   {
    "name": "hasConfigurationIssues",
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
 "listMembershipUsageVisit": {
  "method": "GET",
  "path": "/membership-usage-visit",
  "contract": "subscription",
  "summary": "Membership Usage, Visit & Consumption Rules",
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
    "name": "tier",
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
 "listPriceLists": {
  "method": "GET",
  "path": "/price-lists",
  "contract": "catalogue",
  "summary": "List price lists",
  "permission": "PRICE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "channel",
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
 "publishChannelAvailability": {
  "method": "PUT",
  "path": "/channel-availability",
  "contract": "catalogue",
  "summary": "Channel Publication & Availability",
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
  "requestBody": "ChannelPublicationAvailabilityInput",
  "responds": "ChannelPublicationAvailabilityView"
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "FamilyHouseholdDependentMembershipConfigurationInput",
  "responds": "FamilyHouseholdDependentMembershipConfigurationView"
 },
 "setMembershipBenefit": {
  "method": "PUT",
  "path": "/membership-benefits",
  "contract": "catalogue",
  "summary": "Define a benefit",
  "permission": "PRODUCT_CONFIGURE",
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
  "requestBody": "CatalogueMembershipBenefit",
  "responds": "CatalogueMembershipBenefit"
 },
 "setMembershipCommercialConfig": {
  "method": "PUT",
  "path": "/membership-commercial-config",
  "contract": "subscription",
  "summary": "Save a membership product's commercial references, payment eligibility and sales period",
  "permission": "PLATFORM_CELL_MANAGE",
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
  "requestBody": "MembershipCommercialConfigInput",
  "responds": "MembershipCommercialPricingChannelAssociationView"
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "MembershipProductTierBuilderInput",
  "responds": "MembershipProductTierBuilderView"
 },
 "setMembershipProgramme": {
  "method": "PUT",
  "path": "/membership-programmes",
  "contract": "catalogue",
  "summary": "Define a membership programme",
  "permission": "PRODUCT_CONFIGURE",
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
  "requestBody": "CatalogueMembershipProgramme",
  "responds": "CatalogueMembershipProgramme"
 },
 "setMembershipUsagePolicy": {
  "method": "PUT",
  "path": "/membership-usage-policy",
  "contract": "subscription",
  "summary": "Save a membership product's usage, visit and consumption rules",
  "permission": "PLATFORM_CELL_MANAGE",
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
  "requestBody": "MembershipUsagePolicyInput",
  "responds": "MembershipUsageVisitConsumptionRulesView"
 },
 "setPlanBenefits": {
  "method": "PUT",
  "path": "/entitlement-templates/{templateId}/benefits",
  "contract": "catalogue",
  "summary": "Replace the benefits a plan grants",
  "permission": "PRODUCT_CONFIGURE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "templateId",
    "in": "path",
    "required": true
   },
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "CataloguePlanBenefit",
  "responds": "CataloguePlanBenefit"
 },
 "setPrices": {
  "method": "PUT",
  "path": "/price-lists/{priceListId}/prices",
  "contract": "catalogue",
  "summary": "Set prices in bulk",
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
  "requestBody": null,
  "responds": null
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "ValidityActivationExpiryConfigurationInput",
  "responds": "ValidityActivationExpiryConfigurationView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "CatalogueMembershipBenefit": {
  "type": "object",
  "x-ticvai-persistence": "catalogue.membership_benefit",
  "description": "**Taken from the backend workbook, 20 September.** Defines a benefit that can be included in one or more membership plans.",
  "required": [
   "code",
   "name",
   "type",
   "isActive",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "code": {
    "type": "string",
    "maxLength": 100
   },
   "name": {
    "type": "string",
    "maxLength": 150
   },
   "type": {
    "type": "string",
    "maxLength": 30
   },
   "description": {
    "type": "string",
    "maxLength": 500,
    "nullable": true
   },
   "value": {
    "type": "number",
    "nullable": true
   },
   "unit": {
    "type": "string",
    "maxLength": 30,
    "nullable": true
   },
   "entitlementTemplateId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "isActive": {
    "type": "boolean"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "CatalogueMembershipProgramme": {
  "type": "object",
  "x-ticvai-persistence": "catalogue.membership_programme",
  "description": "**Taken from the backend workbook, 20 September.** Defines the overall membership programme available to customers.",
  "required": [
   "programId",
   "programCode",
   "programName",
   "isActive",
   "createdAt"
  ],
  "properties": {
   "programId": {
    "type": "string",
    "format": "uuid"
   },
   "programCode": {
    "type": "string",
    "maxLength": 100
   },
   "programName": {
    "type": "string",
    "maxLength": 150
   },
   "description": {
    "type": "string",
    "maxLength": 500,
    "nullable": true
   },
   "isActive": {
    "type": "boolean"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "CataloguePlanBenefit": {
  "type": "object",
  "x-ticvai-persistence": "catalogue.plan_benefit",
  "description": "**Taken from the backend workbook, 20 September.** Maps membership benefits to plans and defines usage limits for each benefit.",
  "required": [
   "entitlementTemplateId",
   "membershipBenefitId",
   "priority",
   "isActive",
   "createdAt"
  ],
  "properties": {
   "entitlementTemplateId": {
    "type": "string",
    "format": "uuid"
   },
   "membershipBenefitId": {
    "type": "string",
    "format": "uuid"
   },
   "usageLimit": {
    "type": "number",
    "nullable": true
   },
   "usagePeriod": {
    "type": "string",
    "maxLength": 30,
    "nullable": true
   },
   "priority": {
    "type": "integer"
   },
   "isActive": {
    "type": "boolean"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "Channel": {
  "type": "string",
  "enum": [
   "pos",
   "kiosk",
   "web",
   "mobile",
   "b2b",
   "ota",
   "callCentre"
  ]
 },
 "ChannelPublicationAvailabilityInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Channel Publication & Availability submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "channels": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "channel": {
       "$ref": "#/components/schemas/Channel"
      },
      "enabled": {
       "type": "boolean"
      },
      "siteIds": {
       "type": "array",
       "items": {
        "type": "string"
       },
       "description": "Specific sites/webstores; empty = all"
      },
      "posGroupIds": {
       "type": "array",
       "items": {
        "type": "string"
       },
       "description": "Specific POS groups; empty = all"
      },
      "venueIds": {
       "type": "array",
       "items": {
        "type": "string"
       },
       "description": "Availability by venue; empty = all the product's venues"
      },
      "effectiveFrom": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      },
      "effectiveTo": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      }
     }
    },
    "description": "Channels the product is published on, with channel-specific sites, POS groups, venues and effective dates"
   },
   "productId": {
    "type": "string",
    "description": "Product id",
    "format": "uuid"
   }
  }
 },
 "ChannelPublicationAvailabilityView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Channel Publication & Availability displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "channels": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "channel": {
       "$ref": "#/components/schemas/Channel"
      },
      "enabled": {
       "type": "boolean"
      },
      "siteIds": {
       "type": "array",
       "items": {
        "type": "string"
       },
       "description": "Specific sites/webstores; empty = all"
      },
      "posGroupIds": {
       "type": "array",
       "items": {
        "type": "string"
       },
       "description": "Specific POS groups; empty = all"
      },
      "venueIds": {
       "type": "array",
       "items": {
        "type": "string"
       },
       "description": "Availability by venue; empty = all the product's venues"
      },
      "effectiveFrom": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      },
      "effectiveTo": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      }
     }
    },
    "description": "Channels the product is published on, with channel-specific sites, POS groups, venues and effective dates"
   },
   "publicationPreview": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "channel": {
       "$ref": "#/components/schemas/Channel"
      },
      "venueId": {
       "type": "string"
      },
      "exposed": {
       "type": "boolean"
      },
      "reason": {
       "type": "string",
       "nullable": true
      }
     }
    },
    "description": "Preview of where the product will actually be on sale"
   },
   "validationIssues": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "code": {
       "type": "string",
       "enum": [
        "channelNotConfigured",
        "noPriceForChannel",
        "noCapacityAllocation",
        "productNotApproved",
        "venueNotAssigned"
       ]
      },
      "message": {
       "type": "string"
      }
     }
    },
    "description": "Missing channel dependencies (decided 29 September, readiness close-out)"
   },
   "productId": {
    "type": "string",
    "description": "Product id",
    "format": "uuid"
   },
   "issuedEntitlementsUnaffected": {
    "type": "integer",
    "description": "Valid issued tickets/entitlements that remain valid whatever the channel change (pack p.10 Important Rule)"
   }
  }
 },
 "EntitlementTemplate": {
  "x-ticvai-persistence": "catalogue.entitlement_template",
  "type": "object",
  "required": [
   "id",
   "code",
   "name",
   "validityKind"
  ],
  "properties": {
   "description": {
    "type": "string",
    "description": "**Validity, re-entry and transfer rules in prose.** \"Can I leave and come back\" is answered from here, and a name cannot answer it.\n"
   },
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "Assigned by the server on create; `createEntitlementTemplate` does not take it."
   },
   "code": {
    "type": "string",
    "maxLength": 64
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "validityKind": {
    "type": "string",
    "enum": [
     "singleUse",
     "dated",
     "dateRange",
     "rolling",
     "unlimited",
     "countLimited"
    ]
   },
   "validFromOffsetDays": {
    "type": "integer",
    "nullable": true
   },
   "validForDays": {
    "type": "integer",
    "nullable": true
   },
   "daysOfWeek": {
    "type": "array",
    "nullable": true,
    "description": "1.1.7 and 1.1.82. **A camp ticket admits on Tuesdays and Thursdays for six weeks**, and `validityKind` had six values with no day pattern among them.\nThe shape is settled elsewhere in the package — `fnb.MenuAvailability` and `promotions.PromotionConditions` both carry it. **Null means every day**, which is what every existing entitlement means today.\n",
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
    }
   },
   "expiryAnchor": {
    "type": "string",
    "nullable": true,
    "enum": [
     "offsetDays",
     "endOfMonth",
     "endOfQuarter",
     "endOfYear",
     "fixedDate",
     "seasonEnd"
    ],
    "description": "1.1.90 to 1.1.92. **A pass bought on the 20th and expiring on the 31st cannot be expressed by an offset in days.** `offsetDays` is the existing behaviour and stays the default.\n`seasonEnd` anchors to the venue's own season rather than the calendar — a water park closing in October is not a quarter boundary.\n"
   },
   "expiryDate": {
    "type": "string",
    "format": "date",
    "nullable": true,
    "description": "Where `expiryAnchor` is `fixedDate`. Every pass expires the same day regardless of purchase."
   },
   "carriesStoredValue": {
    "type": "boolean",
    "default": false,
    "description": "BL-033. **A ticket that is also a wallet** — a resort pass with 200 dirhams of spend on it, deducted at a gate or a till.\n**The value is a `retail.Wallet` bound to the entitlement, not a balance on the ticket.** One balance mechanism (CF-126), so it holds authorisations, expires by credit type and appears in the same reports — a second balance on the entitlement would have been the seventh implementation.\n"
   },
   "includedValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "validTimeWindows": {
    "type": "array",
    "nullable": true,
    "description": "BL-036, 1.1.81 and 1.1.83. **A time-window entitlement needed a performance to express** — valid 09:00 to 13:00 on any day was a thing you built by creating performances.\n**A window is a property of the entitlement and a performance is an occurrence**, and conflating them means a morning pass generates 365 performances a year.\n",
    "items": {
     "type": "object",
     "properties": {
      "from": {
       "type": "string"
      },
      "to": {
       "type": "string"
      },
      "daysOfWeek": {
       "type": "array",
       "items": {
        "type": "string"
       }
      }
     }
    }
   },
   "blackoutDates": {
    "type": "array",
    "nullable": true,
    "description": "**Calendar exceptions on the entitlement.** An annual pass excluding public holidays is the normal case and had nowhere to live.\n",
    "items": {
     "type": "string",
     "format": "date"
    }
   },
   "fastTrackTier": {
    "type": "string",
    "nullable": true,
    "enum": [
     "none",
     "priority",
     "express",
     "unlimited"
    ],
    "description": "19.2.20, BL-015. **Fast track existed nowhere in the package** — not an enum value, not a description, not a screen.\n**An attribute of the entitlement rather than a queue class or a product kind**, because the same ride serves standby and fast-track guests from one capacity: `queue` already has `isFastPass` on an entry and needed something to read it from.\n"
   },
   "entriesAllowed": {
    "type": "integer",
    "nullable": true,
    "description": "Null means unlimited. The Fast Pass consumption counter lives here."
   },
   "transportRestriction": {
    "type": "object",
    "nullable": true,
    "description": "**The journey a transport pass is good for** (decided 29 September, rev 3 REV3-21). Set on the template `transport.createTransportPassType` creates, from the station pair the guest bought the pass for, and copied to the entitlement. `access` refuses a boarding scan whose departure does not serve both stations in a direction the restriction allows, and consumes one of `entriesAllowed` per boarding. Null on every other template.\n",
    "required": [
     "fromStationId",
     "toStationId"
    ],
    "properties": {
     "fromStationId": {
      "type": "string",
      "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$",
      "description": "A `transport.Station`."
     },
     "toStationId": {
      "type": "string",
      "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
     },
     "bothDirections": {
      "type": "boolean",
      "default": true,
      "description": "Valid from either station to the other, as the prototype sells it."
     },
     "routeIds": {
      "type": "array",
      "description": "The routes it may be used on. Empty means any active route serving both stations.",
      "items": {
       "type": "string",
       "pattern": "^[0-9A-HJKMNP-TV-Z]{26}$"
      }
     }
    }
   },
   "reentryAllowed": {
    "type": "boolean",
    "default": false
   },
   "purchaseEligibility": {
    "type": "object",
    "nullable": true,
    "description": "1.1.38, 1.1.121, 1.1.125, 1.1.126. **`admissionRulesId` governs where an entitlement admits, not who may buy it**, and `promotions.evaluatePromotions` gates a discount rather than a sale. Neither refuses a purchase.\n**Evaluated at add-to-cart, not at checkout.** A guest told at payment that they cannot buy a resident rate has already entered a card.\n",
    "properties": {
     "minAgeYears": {
      "type": "integer",
      "nullable": true
     },
     "maxAgeYears": {
      "type": "integer",
      "nullable": true
     },
     "minHeightCm": {
      "type": "integer",
      "nullable": true,
      "description": "**Height gates a ride and can gate a sale.** A ticket sold to somebody who cannot ride it is a refund at the gate.\n"
     },
     "residencyRequired": {
      "type": "boolean",
      "default": false
     },
     "nationalities": {
      "type": "array",
      "nullable": true,
      "items": {
       "type": "string"
      }
     },
     "minLoyaltyTier": {
      "type": "string",
      "nullable": true
     },
     "requiresVerification": {
      "type": "boolean",
      "default": false,
      "description": "**Whether the claim is checked or taken on trust.** A resident rate sold unverified and refused at the gate is worse than one that could not be bought.\n"
     }
    }
   },
   "personType": {
    "type": "string",
    "nullable": true,
    "enum": [
     "adult",
     "child",
     "infant",
     "senior",
     "student",
     "resident",
     "staff"
    ],
    "description": "2.11.7. **Adult, child and senior existed only as `ProductVariant.axisValues` — a variant axis rather than an attribute of the holder.** So changing a child ticket to an adult one was an exchange to a different product, and an upgrade that should be a price difference became a cancel-and-rebuy.\nRecorded here as well as on the variant, because **the guest ages and the product does not.**\n"
   },
   "admissionRulesId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "isTransferable": {
    "type": "boolean",
    "default": true
   },
   "canShareMedia": {
    "type": "boolean",
    "default": true,
    "description": "Whether this entitlement may be appended to media a guest already holds (CF-58). False for anything surrendered at use — a single-entry ticket taken at the gate is not a claim token for a locker bought afterwards.\n"
   },
   "canClaimShopAndDrop": {
    "type": "boolean",
    "default": false,
    "description": "Whether this entitlement may be scanned to claim goods left under 4.4.7. False for a single-entry ticket that is surrendered at the gate — a claim token the guest no longer holds is not a claim token.\n"
   },
   "isNameBound": {
    "type": "boolean",
    "default": false,
    "description": "True requires a holder name at sale. Most entitlements carry none — identity and entitlement are separate concerns.\n"
   },
   "autoRenewDefault": {
    "type": "boolean",
    "default": false,
    "description": "**Taken from their `membership_plan`, 20 September — the \"take those\" half of the TAKE BODY verdict.** `identity.customer_membership.auto_renew` carries the flag per holder and nothing said what it should start as.\n"
   },
   "renewalTermDays": {
    "type": "integer",
    "nullable": true,
    "description": "What a renewal extends the membership by. `orders.membership_renewal` records `previousExpiryAt` and `newExpiryAt` and **the number between them lived nowhere**.\n"
   },
   "renewalGraceDays": {
    "type": "integer",
    "default": 0,
    "description": "How long after expiry a membership can still be renewed rather than rejoined. `membership_renewal.failureReason` implies a window and there was none, so a failed card on the expiry date had no defined consequence.\n"
   },
   "renewalVariantId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**What a renewal sells, which is usually not what joining sold.** A first-year price and a renewal price are different products, and pointing both at one variant makes a loyalty discount unrepresentable. Null means renewal sells the same thing.\n"
   },
   "crossesCells": {
    "type": "boolean",
    "default": false,
    "description": "True propagates a redemption right to other cells on issue (ADR-0010).\n"
   },
   "isActive": {
    "type": "boolean"
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.** Set by the server, never taken from a body."
   }
  }
 },
 "FamilyHouseholdDependentMembershipConfigurationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; stored as subscription.membership_household_policy (MembershipHouseholdPolicy) (decided 29 September, data model DM4)",
  "description": "**What Family, Household & Dependent Membership Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "minimumAge": {
    "type": "integer",
    "description": "Dependent Rules: minimum age of a dependent",
    "nullable": true
   },
   "maximumAge": {
    "type": "integer",
    "description": "Dependent Rules: maximum age of a dependent (pack example: a child dependent turning 16 is flagged)",
    "nullable": true
   },
   "relationshipRequirement": {
    "type": "string",
    "enum": [
     "none",
     "declared",
     "verified"
    ],
    "description": "Relationship Requirement between dependent and primary member. Default declared (decided 29 September, readiness close-out)"
   },
   "verificationRequirement": {
    "type": "string",
    "enum": [
     "none",
     "customerDeclaration",
     "documentVerification",
     "identityVerification",
     "staffVerification",
     "externalVerification"
    ],
    "description": "Verification Requirement for dependents"
   },
   "sameHouseholdRequired": {
    "type": "boolean",
    "description": "Same Household Requirement where applicable. Default false (decided 29 September, readiness close-out)"
   },
   "memberChangesAllowed": {
    "type": "boolean",
    "description": "Add/Remove Member Rules: members may be added or removed during the term"
   },
   "memberChangeEffective": {
    "type": "string",
    "enum": [
     "immediately",
     "nextRenewal"
    ],
    "description": "Add/Remove effective date. Default immediately (decided 29 September, readiness close-out)"
   },
   "memberChangesPerTerm": {
    "type": "integer",
    "description": "Frequency: add/remove changes allowed per membership term; empty for unlimited",
    "nullable": true
   },
   "memberChangeFee": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "Fee charged per add/remove change, as the venue configures it; empty for no fee"
   },
   "memberChangeApprovalRequired": {
    "type": "boolean",
    "description": "Approval: add/remove changes need staff approval. Default false (decided 29 September, readiness close-out)"
   },
   "eligibilityRevalidation": {
    "type": "boolean",
    "description": "Eligibility Revalidation of the added member against the dependent rules. Default true (decided 29 September, readiness close-out)"
   },
   "membershipCode": {
    "type": "string",
    "description": "Membership code"
   },
   "membershipStructure": {
    "type": "string",
    "enum": [
     "individual",
     "couple",
     "family",
     "household",
     "parentChild",
     "corporateGroup",
     "custom"
    ],
    "description": "Membership Structure (pack p.12)"
   },
   "roleLimits": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "role": {
       "type": "string",
       "enum": [
        "primaryMember",
        "secondaryAdult",
        "dependent",
        "child",
        "guardian",
        "authorizedManager"
       ]
      },
      "minCount": {
       "type": "integer"
      },
      "maxCount": {
       "type": "integer",
       "nullable": true
      }
     }
    },
    "description": "Roles and Family Limits (pack p.13; example Family Gold: 2 adults, maximum 3 children)"
   },
   "entitlementModel": {
    "type": "string",
    "enum": [
     "individual",
     "shared",
     "mixed"
    ],
    "description": "Entitlement Model (pack p.13): each member's own benefits, shared benefits (e.g. 6 guest tickets for the family) or both"
   },
   "ageTransitionAction": {
    "type": "string",
    "enum": [
     "gracePeriod",
     "upgradeRequired",
     "renewalCorrection",
     "manualReview"
    ],
    "description": "Age Transition (pp.13-14): action when a dependent no longer qualifies. Default manualReview (decided 29 September, readiness close-out)"
   },
   "ageTransitionGraceDays": {
    "type": "integer",
    "description": "Days a dependent keeps access after ageing out, for gracePeriod",
    "nullable": true
   }
  }
 },
 "FamilyHouseholdDependentMembershipConfigurationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Family, Household & Dependent Membership Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "minimumAge": {
    "type": "integer",
    "description": "Dependent Rules: minimum age of a dependent",
    "nullable": true
   },
   "maximumAge": {
    "type": "integer",
    "description": "Dependent Rules: maximum age of a dependent (pack example: a child dependent turning 16 is flagged)",
    "nullable": true
   },
   "relationshipRequirement": {
    "type": "string",
    "enum": [
     "none",
     "declared",
     "verified"
    ],
    "description": "Relationship Requirement between dependent and primary member. Default declared (decided 29 September, readiness close-out)"
   },
   "verificationRequirement": {
    "type": "string",
    "enum": [
     "none",
     "customerDeclaration",
     "documentVerification",
     "identityVerification",
     "staffVerification",
     "externalVerification"
    ],
    "description": "Verification Requirement for dependents"
   },
   "sameHouseholdRequired": {
    "type": "boolean",
    "description": "Same Household Requirement where applicable. Default false (decided 29 September, readiness close-out)"
   },
   "memberChangesAllowed": {
    "type": "boolean",
    "description": "Add/Remove Member Rules: members may be added or removed during the term"
   },
   "memberChangeEffective": {
    "type": "string",
    "enum": [
     "immediately",
     "nextRenewal"
    ],
    "description": "Add/Remove effective date. Default immediately (decided 29 September, readiness close-out)"
   },
   "memberChangesPerTerm": {
    "type": "integer",
    "description": "Frequency: add/remove changes allowed per membership term; empty for unlimited",
    "nullable": true
   },
   "memberChangeFee": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "Fee charged per add/remove change, as the venue configures it; empty for no fee"
   },
   "memberChangeApprovalRequired": {
    "type": "boolean",
    "description": "Approval: add/remove changes need staff approval. Default false (decided 29 September, readiness close-out)"
   },
   "eligibilityRevalidation": {
    "type": "boolean",
    "description": "Eligibility Revalidation of the added member against the dependent rules. Default true (decided 29 September, readiness close-out)"
   },
   "membershipCode": {
    "type": "string",
    "description": "Membership code"
   },
   "membershipStructure": {
    "type": "string",
    "enum": [
     "individual",
     "couple",
     "family",
     "household",
     "parentChild",
     "corporateGroup",
     "custom"
    ],
    "description": "Membership Structure (pack p.12)"
   },
   "roleLimits": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "role": {
       "type": "string",
       "enum": [
        "primaryMember",
        "secondaryAdult",
        "dependent",
        "child",
        "guardian",
        "authorizedManager"
       ]
      },
      "minCount": {
       "type": "integer"
      },
      "maxCount": {
       "type": "integer",
       "nullable": true
      }
     }
    },
    "description": "Roles and Family Limits (pack p.13; example Family Gold: 2 adults, maximum 3 children)"
   },
   "entitlementModel": {
    "type": "string",
    "enum": [
     "individual",
     "shared",
     "mixed"
    ],
    "description": "Entitlement Model (pack p.13): each member's own benefits, shared benefits (e.g. 6 guest tickets for the family) or both"
   },
   "ageTransitionAction": {
    "type": "string",
    "enum": [
     "gracePeriod",
     "upgradeRequired",
     "renewalCorrection",
     "manualReview"
    ],
    "description": "Age Transition (pp.13-14): action when a dependent no longer qualifies. Default manualReview (decided 29 September, readiness close-out)"
   },
   "ageTransitionGraceDays": {
    "type": "integer",
    "description": "Days a dependent keeps access after ageing out, for gracePeriod",
    "nullable": true
   }
  }
 },
 "MembershipCommercialConfigInput": {
  "type": "object",
  "x-ticvai-persistence": "none — request only; stored as the commercial columns of subscription.membership_product (MembershipProduct: basePricingProfile, taxProfile, feeProfile, upgradePricePolicy, promotionalPricingEligibility, paymentTerms, salesPeriod) (decided 29 September, writers pass; DM4)",
  "description": "What setMembershipCommercialConfig submits. Prices, channels, the sales window and capacity are catalogue data and are set there (setPrices, publishChannelAvailability, createChannelCapacity/updateChannelCapacity), so none is repeated here (decided 29 September, writers pass; DM4)",
  "required": [
   "membershipCode",
   "basePricingProfile",
   "taxProfile",
   "salesPeriod"
  ],
  "properties": {
   "membershipCode": {
    "type": "string",
    "description": "The membership product (subscription.membership_product) being associated."
   },
   "basePricingProfile": {
    "type": "string",
    "description": "Base Pricing Profile id"
   },
   "taxProfile": {
    "type": "string",
    "description": "Tax Profile id"
   },
   "feeProfile": {
    "type": "string",
    "nullable": true,
    "description": "Fee Profile id"
   },
   "upgradePricePolicy": {
    "type": "string",
    "nullable": true,
    "description": "Upgrade Price Policy id (pack p.14); pro-rata credit on upgrade per MoM 1 Sep §4.9"
   },
   "promotionalPricingEligibility": {
    "type": "boolean",
    "default": false,
    "description": "Promotional Pricing Eligibility: promotions may apply to this membership"
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
    "description": "Sales Period (pack p.15); the window itself is the catalogue product's sales window"
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
 "MembershipEligibilityQualificationRuleBuilderInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; stored as subscription.membership_eligibility_rule (MembershipEligibilityRule) for the rules and subscription.membership_product for the product-level switches (decided 29 September, data model DM4)",
  "description": "**What Membership Eligibility & Qualification Rule Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "multipleMembershipsAllowed": {
    "type": "boolean",
    "description": "Multiple Memberships Allowed: false means one membership of this product per customer. Default false (decided 29 September, readiness close-out)"
   },
   "mutuallyExclusiveMemberships": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Mutually Exclusive Memberships: membership codes a customer may not hold alongside this one"
   },
   "prerequisiteMembership": {
    "type": "string",
    "description": "Prerequisite Membership: code of a membership the customer must already hold",
    "nullable": true
   },
   "existingTierRequirement": {
    "type": "string",
    "description": "Existing Tier Requirement: minimum tier the customer must already hold",
    "nullable": true
   },
   "separatePurchaseAndActivationRules": {
    "type": "boolean",
    "description": "Purchase vs Activation: true when the rules apply at activation to the assigned member rather than to the buyer (pack p.8: a parent may buy a Junior Pass that must be assigned to an eligible child). Default true (decided 29 September, readiness close-out)"
   },
   "membershipCode": {
    "type": "string",
    "description": "Membership code the rules belong to"
   },
   "rules": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "dimension": {
       "type": "string",
       "enum": [
        "age",
        "personType",
        "residency",
        "country",
        "customerSegment",
        "corporateAffiliation",
        "studentStatus",
        "existingMembership",
        "previousPurchase",
        "membershipHistory",
        "channel",
        "venue",
        "promotionalQualification"
       ],
       "description": "Eligibility Dimension (pack p.7)"
      },
      "operator": {
       "type": "string",
       "enum": [
        "equals",
        "notEquals",
        "in",
        "notIn",
        "between",
        "atLeast",
        "atMost"
       ]
      },
      "values": {
       "type": "array",
       "items": {
        "type": "string"
       },
       "description": "Values compared, e.g. the age bounds of a junior pass"
      },
      "appliesAt": {
       "type": "array",
       "items": {
        "type": "string",
        "enum": [
         "purchase",
         "activation",
         "holding",
         "renewal"
        ]
       },
       "description": "When the rule is evaluated (pack p.7 purpose: purchase, activate, hold or renew)"
      }
     }
    },
    "description": "Eligibility rules; all must pass"
   },
   "verificationMethod": {
    "type": "string",
    "enum": [
     "none",
     "customerDeclaration",
     "documentVerification",
     "identityVerification",
     "staffVerification",
     "externalVerification"
    ],
    "description": "Verification (pack pp.7-8): how qualification is proven. Default none (decided 29 September, readiness close-out)"
   }
  }
 },
 "MembershipEligibilityQualificationRuleBuilderView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Membership Eligibility & Qualification Rule Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "multipleMembershipsAllowed": {
    "type": "boolean",
    "description": "Multiple Memberships Allowed: false means one membership of this product per customer. Default false (decided 29 September, readiness close-out)"
   },
   "mutuallyExclusiveMemberships": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Mutually Exclusive Memberships: membership codes a customer may not hold alongside this one"
   },
   "prerequisiteMembership": {
    "type": "string",
    "description": "Prerequisite Membership: code of a membership the customer must already hold",
    "nullable": true
   },
   "existingTierRequirement": {
    "type": "string",
    "description": "Existing Tier Requirement: minimum tier the customer must already hold",
    "nullable": true
   },
   "separatePurchaseAndActivationRules": {
    "type": "boolean",
    "description": "Purchase vs Activation: true when the rules apply at activation to the assigned member rather than to the buyer (pack p.8: a parent may buy a Junior Pass that must be assigned to an eligible child). Default true (decided 29 September, readiness close-out)"
   },
   "membershipCode": {
    "type": "string",
    "description": "Membership code the rules belong to"
   },
   "rules": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "dimension": {
       "type": "string",
       "enum": [
        "age",
        "personType",
        "residency",
        "country",
        "customerSegment",
        "corporateAffiliation",
        "studentStatus",
        "existingMembership",
        "previousPurchase",
        "membershipHistory",
        "channel",
        "venue",
        "promotionalQualification"
       ],
       "description": "Eligibility Dimension (pack p.7)"
      },
      "operator": {
       "type": "string",
       "enum": [
        "equals",
        "notEquals",
        "in",
        "notIn",
        "between",
        "atLeast",
        "atMost"
       ]
      },
      "values": {
       "type": "array",
       "items": {
        "type": "string"
       },
       "description": "Values compared, e.g. the age bounds of a junior pass"
      },
      "appliesAt": {
       "type": "array",
       "items": {
        "type": "string",
        "enum": [
         "purchase",
         "activation",
         "holding",
         "renewal"
        ]
       },
       "description": "When the rule is evaluated (pack p.7 purpose: purchase, activate, hold or renew)"
      }
     }
    },
    "description": "Eligibility rules; all must pass"
   },
   "verificationMethod": {
    "type": "string",
    "enum": [
     "none",
     "customerDeclaration",
     "documentVerification",
     "identityVerification",
     "staffVerification",
     "externalVerification"
    ],
    "description": "Verification (pack pp.7-8): how qualification is proven. Default none (decided 29 September, readiness close-out)"
   }
  }
 },
 "MembershipEntitlementAdmissionBenefitBuilderInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; stored as subscription.membership_entitlement (MembershipEntitlement), one row per entitlement (decided 29 September, data model DM4)",
  "description": "**What Membership Entitlement & Admission Benefit Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "membershipCode": {
    "type": "string",
    "description": "Membership code"
   },
   "tier": {
    "type": "string",
    "description": "Tier the package belongs to"
   },
   "entitlements": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "entitlementType": {
       "type": "string",
       "enum": [
        "unlimitedAdmission",
        "limitedAdmissions",
        "attractionAccess",
        "eventAccess",
        "zoneAccess",
        "fastTrack",
        "priorityEntry",
        "guestTickets",
        "parking",
        "fnbBenefit",
        "retailBenefit",
        "rentalBenefit",
        "specialEventAccess",
        "bookingPrivileges",
        "other"
       ],
       "description": "Entitlement Type (pack pp.9-10)"
      },
      "venue": {
       "type": "string",
       "nullable": true
      },
      "attraction": {
       "type": "string",
       "nullable": true
      },
      "eventType": {
       "type": "string",
       "nullable": true
      },
      "admissionType": {
       "type": "string",
       "nullable": true
      },
      "quantity": {
       "type": "integer",
       "nullable": true,
       "description": "Number of visits or uses per limitPeriod; empty for unlimited"
      },
      "limitPeriod": {
       "type": "string",
       "enum": [
        "perDay",
        "perWeek",
        "perMonth",
        "perMembershipYear",
        "lifetimeOfMembership"
       ],
       "description": "Benefit Limits (pack p.10)"
      },
      "days": {
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
       "description": "Days the entitlement is valid; empty for every day"
      },
      "timeFrom": {
       "type": "string",
       "nullable": true,
       "description": "Times: local start time HH:mm"
      },
      "timeTo": {
       "type": "string",
       "nullable": true,
       "description": "Times: local end time HH:mm"
      },
      "timeslots": {
       "type": "array",
       "items": {
        "type": "string"
       },
       "description": "Timeslot ids the entitlement is restricted to"
      },
      "blackoutDates": {
       "type": "array",
       "items": {
        "type": "string",
        "format": "date"
       },
       "description": "Blackouts (pack pp.10-11; MoM 25 Aug blockout dates)"
      },
      "requiresSameDayVisit": {
       "type": "boolean",
       "description": "Benefit Dependencies (pack p.11): valid only with a valid visit the same day, e.g. parking"
      },
      "pricingRuleId": {
       "type": "string",
       "nullable": true,
       "description": "For a discount benefit (F&B, retail, rental): the central pricing rule that calculates it (pack p.15: Area 13 identifies the benefit, the commercial engine calculates)"
      },
      "ownership": {
       "type": "string",
       "enum": [
        "memberSpecific",
        "familyShared",
        "dependentSpecific",
        "accountShared"
       ],
       "description": "Entitlement Ownership (pack p.11)"
      }
     }
    },
    "description": "The admission and benefit package for the tier (pack p.10 example: Gold Annual Pass)"
   }
  }
 },
 "MembershipEntitlementAdmissionBenefitBuilderView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Membership Entitlement & Admission Benefit Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "membershipCode": {
    "type": "string",
    "description": "Membership code"
   },
   "tier": {
    "type": "string",
    "description": "Tier the package belongs to"
   },
   "entitlements": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "entitlementType": {
       "type": "string",
       "enum": [
        "unlimitedAdmission",
        "limitedAdmissions",
        "attractionAccess",
        "eventAccess",
        "zoneAccess",
        "fastTrack",
        "priorityEntry",
        "guestTickets",
        "parking",
        "fnbBenefit",
        "retailBenefit",
        "rentalBenefit",
        "specialEventAccess",
        "bookingPrivileges",
        "other"
       ],
       "description": "Entitlement Type (pack pp.9-10)"
      },
      "venue": {
       "type": "string",
       "nullable": true
      },
      "attraction": {
       "type": "string",
       "nullable": true
      },
      "eventType": {
       "type": "string",
       "nullable": true
      },
      "admissionType": {
       "type": "string",
       "nullable": true
      },
      "quantity": {
       "type": "integer",
       "nullable": true,
       "description": "Number of visits or uses per limitPeriod; empty for unlimited"
      },
      "limitPeriod": {
       "type": "string",
       "enum": [
        "perDay",
        "perWeek",
        "perMonth",
        "perMembershipYear",
        "lifetimeOfMembership"
       ],
       "description": "Benefit Limits (pack p.10)"
      },
      "days": {
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
       "description": "Days the entitlement is valid; empty for every day"
      },
      "timeFrom": {
       "type": "string",
       "nullable": true,
       "description": "Times: local start time HH:mm"
      },
      "timeTo": {
       "type": "string",
       "nullable": true,
       "description": "Times: local end time HH:mm"
      },
      "timeslots": {
       "type": "array",
       "items": {
        "type": "string"
       },
       "description": "Timeslot ids the entitlement is restricted to"
      },
      "blackoutDates": {
       "type": "array",
       "items": {
        "type": "string",
        "format": "date"
       },
       "description": "Blackouts (pack pp.10-11; MoM 25 Aug blockout dates)"
      },
      "requiresSameDayVisit": {
       "type": "boolean",
       "description": "Benefit Dependencies (pack p.11): valid only with a valid visit the same day, e.g. parking"
      },
      "pricingRuleId": {
       "type": "string",
       "nullable": true,
       "description": "For a discount benefit (F&B, retail, rental): the central pricing rule that calculates it (pack p.15: Area 13 identifies the benefit, the commercial engine calculates)"
      },
      "ownership": {
       "type": "string",
       "enum": [
        "memberSpecific",
        "familyShared",
        "dependentSpecific",
        "accountShared"
       ],
       "description": "Entitlement Ownership (pack p.11)"
      }
     }
    },
    "description": "The admission and benefit package for the tier (pack p.10 example: Gold Annual Pass)"
   }
  }
 },
 "MembershipProductTierBuilderInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; stored as subscription.membership_product (MembershipProduct), a new version when the product is active (decided 29 September, data model DM4)",
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
    "enum": [
     "annualPass",
     "seasonPass",
     "monthlyMembership",
     "fixedTermMembership",
     "corporateMembership",
     "familyMembership",
     "individualMembership",
     "studentMembership",
     "vipMembership",
     "customMembership"
    ],
    "description": "Membership Type (pack pp.4-5)"
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
    "description": "Currency Context: ISO 4217 currency code the product is sold in"
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
   "tierLevel": {
    "type": "integer",
    "description": "Tier Level: rank within the membership family; higher is more premium"
   },
   "displayOrder": {
    "type": "integer",
    "description": "Display Order in listings and upgrade choices"
   },
   "parentMembership": {
    "type": "string",
    "description": "Parent Membership: code of the membership family this tier belongs to",
    "nullable": true
   },
   "replacementMembership": {
    "type": "string",
    "description": "Replacement Membership: code of the product that replaces this one when it is retired",
    "nullable": true
   },
   "holderModel": {
    "type": "string",
    "enum": [
     "individual",
     "family",
     "corporate"
    ],
    "description": "Individual / Family / Corporate (pack p.6 Product Characteristics)"
   },
   "transferable": {
    "type": "boolean",
    "description": "Named / Transferable: true when the membership may be transferred; false (the default) keeps it named to one member (decided 29 September, readiness close-out)"
   },
   "credentialForm": {
    "type": "string",
    "enum": [
     "physical",
     "digital",
     "both"
    ],
    "description": "Physical / Digital credential form"
   },
   "renewable": {
    "type": "boolean",
    "description": "Renewable / Non-Renewable: true when the membership can be renewed"
   },
   "autoRenewEligible": {
    "type": "boolean",
    "description": "Auto-Renew Eligible: the product may be auto-renewed; a member is only auto-renewed after their own explicit opt-in. Default false (decided 29 September, readiness close-out)"
   },
   "benefitModel": {
    "type": "string",
    "enum": [
     "admissionBased",
     "benefitBased",
     "hybrid"
    ],
    "description": "Admission-Based / Benefit-Based / Hybrid"
   },
   "tier": {
    "type": "string",
    "description": "Tier: Standard, Silver, Gold, Platinum, VIP or a custom tier the venue names (pack p.6 Tier Configuration)"
   },
   "upgradePath": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Upgrade Path: membership codes this tier may upgrade to (pack p.6 Tier Relationships; the transaction runs in Area 11)"
   },
   "downgradePath": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Downgrade Path: membership codes this tier may downgrade to"
   },
   "catalogueProductId": {
    "type": "string",
    "description": "Catalogue Association: the sellable product in the Ticketing Catalogue this membership configures (a membership ProductKind)"
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
    "enum": [
     "annualPass",
     "seasonPass",
     "monthlyMembership",
     "fixedTermMembership",
     "corporateMembership",
     "familyMembership",
     "individualMembership",
     "studentMembership",
     "vipMembership",
     "customMembership"
    ],
    "description": "Membership Type (pack pp.4-5)"
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
    "description": "Currency Context: ISO 4217 currency code the product is sold in"
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
   "tierLevel": {
    "type": "integer",
    "description": "Tier Level: rank within the membership family; higher is more premium"
   },
   "displayOrder": {
    "type": "integer",
    "description": "Display Order in listings and upgrade choices"
   },
   "parentMembership": {
    "type": "string",
    "description": "Parent Membership: code of the membership family this tier belongs to",
    "nullable": true
   },
   "replacementMembership": {
    "type": "string",
    "description": "Replacement Membership: code of the product that replaces this one when it is retired",
    "nullable": true
   },
   "holderModel": {
    "type": "string",
    "enum": [
     "individual",
     "family",
     "corporate"
    ],
    "description": "Individual / Family / Corporate (pack p.6 Product Characteristics)"
   },
   "transferable": {
    "type": "boolean",
    "description": "Named / Transferable: true when the membership may be transferred; false (the default) keeps it named to one member (decided 29 September, readiness close-out)"
   },
   "credentialForm": {
    "type": "string",
    "enum": [
     "physical",
     "digital",
     "both"
    ],
    "description": "Physical / Digital credential form"
   },
   "renewable": {
    "type": "boolean",
    "description": "Renewable / Non-Renewable: true when the membership can be renewed"
   },
   "autoRenewEligible": {
    "type": "boolean",
    "description": "Auto-Renew Eligible: the product may be auto-renewed; a member is only auto-renewed after their own explicit opt-in. Default false (decided 29 September, readiness close-out)"
   },
   "benefitModel": {
    "type": "string",
    "enum": [
     "admissionBased",
     "benefitBased",
     "hybrid"
    ],
    "description": "Admission-Based / Benefit-Based / Hybrid"
   },
   "tier": {
    "type": "string",
    "description": "Tier: Standard, Silver, Gold, Platinum, VIP or a custom tier the venue names (pack p.6 Tier Configuration)"
   },
   "upgradePath": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Upgrade Path: membership codes this tier may upgrade to (pack p.6 Tier Relationships; the transaction runs in Area 11)"
   },
   "downgradePath": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Downgrade Path: membership codes this tier may downgrade to"
   },
   "catalogueProductId": {
    "type": "string",
    "description": "Catalogue Association: the sellable product in the Ticketing Catalogue this membership configures (a membership ProductKind)"
   },
   "version": {
    "type": "integer",
    "description": "Version number of this configuration; each saved change to an active product creates a new version"
   },
   "status": {
    "type": "string",
    "description": "Status of the membership product: draft, inReview, approved, scheduled, active, suspended, expired or retired (pack p.5 Statuses)"
   }
  }
 },
 "MembershipProductValidationApprovalPublicationVersioInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; stored as subscription.membership_product (status, approvalStage) with an audit row in subscription.membership_product_history (decided 29 September, data model DM4)",
  "description": "**What Membership Product Validation, Approval, Publication & Versioning submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "migrationPolicy": {
    "type": "string",
    "enum": [
     "remainOnCurrentVersion",
     "moveAtNextRenewal",
     "moveOnEffectiveDate"
    ],
    "description": "Migration policy for existing member contracts (pack p.18). Default moveAtNextRenewal (decided 29 September, readiness close-out)"
   },
   "membershipCode": {
    "type": "string",
    "description": "Membership code"
   },
   "version": {
    "type": "integer",
    "description": "Configuration version the decision applies to"
   },
   "action": {
    "type": "string",
    "enum": [
     "validate",
     "submitForReview",
     "approveCommercial",
     "approveOperational",
     "reject",
     "schedule",
     "publish",
     "suspend",
     "reinstate"
    ],
    "description": "Decision taken on BO-293; `suspend` (from `active`, reason required) and `reinstate` (from `suspended`) are the BO-284 quick actions (decided 29 September, writers pass; DM4)"
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date",
    "description": "Effective date for schedule/publish",
    "nullable": true
   },
   "reason": {
    "type": "string",
    "description": "Reason, recorded in the audit",
    "nullable": true
   }
  }
 },
 "MembershipProductValidationApprovalPublicationVersioView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Membership Product Validation, Approval, Publication & Versioning displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "migrationPolicy": {
    "type": "string",
    "enum": [
     "remainOnCurrentVersion",
     "moveAtNextRenewal",
     "moveOnEffectiveDate"
    ],
    "description": "Migration policy for existing member contracts (pack p.18). Default moveAtNextRenewal (decided 29 September, readiness close-out)"
   },
   "activeMembersAffected": {
    "type": "integer",
    "description": "Active Members Affected"
   },
   "futureRenewals": {
    "type": "integer",
    "description": "Future Renewals affected by the change"
   },
   "entitlementsAffected": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Entitlements Affected"
   },
   "channels": {
    "type": "array",
    "items": {
     "$ref": "../shared/common.yaml#/components/schemas/SalesChannel"
    },
    "description": "Channels affected"
   },
   "pricingDependencies": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Pricing Dependencies: pricing profiles and rules referenced"
   },
   "accessDependencies": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Access Dependencies: access-control rules and credentials referenced"
   },
   "membershipCode": {
    "type": "string",
    "description": "Membership code"
   },
   "version": {
    "type": "integer",
    "description": "Configuration version under approval"
   },
   "approvalStage": {
    "type": "string",
    "description": "Approval stage: draft, review, commercialApproval, operationalApproval, approved, scheduled or published (pack p.17)"
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date",
    "description": "Effective Dating: date this version takes effect"
   },
   "validationChecks": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "check": {
       "type": "string",
       "enum": [
        "productDefinitionComplete",
        "catalogueAssociation",
        "eligibilityRules",
        "validity",
        "activation",
        "entitlements",
        "usageRules",
        "pricingAssociation",
        "taxFeeAssociation",
        "channelAvailability",
        "renewalPolicy",
        "requiredCredentialConfiguration"
       ]
      },
      "passed": {
       "type": "boolean"
      },
      "message": {
       "type": "string",
       "nullable": true
      }
     }
    },
    "description": "Configuration Validation (pack p.17)"
   },
   "validationIssues": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "code": {
       "type": "string",
       "enum": [
        "inactivePricingProfile",
        "missingDependentEligibility",
        "autoRenewWithoutConsentConfiguration",
        "missingCancellationPolicy",
        "other"
       ]
      },
      "message": {
       "type": "string"
      }
     }
    },
    "description": "Dependency Health (pack p.17 examples); missingCancellationPolicy is a warning (decided 29 September, readiness close-out)"
   },
   "publicationTargets": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "target": {
       "type": "string",
       "enum": [
        "b2c",
        "pos",
        "mobileApp",
        "callCenter",
        "b2b",
        "accessControl",
        "ticketing",
        "otherDependentServices"
       ]
      },
      "synchronisedAt": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      }
     }
    },
    "description": "Publication (pack p.18): services the configuration is synchronised to"
   },
   "aiInsights": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "AI Assistance: advisory observations only; never applied automatically (pack AI sections)"
   }
  }
 },
 "MembershipUsagePolicyInput": {
  "type": "object",
  "x-ticvai-persistence": "none — request only; stored as subscription.membership_usage_policy (MembershipUsagePolicy), one row per product version (decided 29 September, writers pass; DM4)",
  "description": "What setMembershipUsagePolicy submits for one membership product version; the fields of MembershipUsagePolicy a venue sets. Counters and figures are not sent (decided 29 September, writers pass; DM4)",
  "required": [
   "membershipCode",
   "reEntryPolicy",
   "reservationRequirement"
  ],
  "properties": {
   "membershipCode": {
    "type": "string",
    "description": "The membership product (subscription.membership_product) whose rules these are."
   },
   "tier": {
    "type": "string",
    "nullable": true,
    "description": "Tier, where the product code covers several tiers."
   },
   "maximumVisitsPerDay": {
    "type": "integer",
    "minimum": 1,
    "nullable": true,
    "description": "Maximum Visits per Day; empty for unlimited"
   },
   "maximumAdmissionsPerPeriod": {
    "type": "integer",
    "minimum": 1,
    "nullable": true,
    "description": "Maximum Admissions per admissionPeriod; empty for unlimited"
   },
   "admissionPeriod": {
    "type": "string",
    "enum": [
     "perDay",
     "perWeek",
     "perMonth",
     "perMembershipYear"
    ],
    "nullable": true,
    "description": "Period for maximumAdmissionsPerPeriod; required when that is set"
   },
   "reEntryPolicy": {
    "type": "string",
    "enum": [
     "unlimitedSameDay",
     "noReEntry",
     "afterMinutes",
     "venueSpecific"
    ],
    "description": "Re-entry (pack p.12)"
   },
   "reEntryCooldownMinutes": {
    "type": "integer",
    "minimum": 1,
    "nullable": true,
    "description": "Re-entry Cooldown in minutes; required for reEntryPolicy afterMinutes"
   },
   "reservationRequirement": {
    "type": "string",
    "enum": [
     "required",
     "optional"
    ],
    "description": "Advance Reservation (pack pp.11-12)"
   },
   "walkInAllowed": {
    "type": "boolean",
    "default": true,
    "description": "Walk-In Allowed without a reservation"
   },
   "maximumAdvanceBookingDays": {
    "type": "integer",
    "minimum": 0,
    "nullable": true,
    "description": "Maximum Advance Booking Days"
   },
   "maximumActiveFutureReservations": {
    "type": "integer",
    "minimum": 1,
    "nullable": true,
    "description": "Maximum Active Future Reservations"
   },
   "concurrentReservations": {
    "type": "integer",
    "minimum": 1,
    "default": 1,
    "description": "Concurrent Reservations: maximum active reservations per timeslot. Default 1 (decided 29 September, readiness close-out)"
   },
   "noShowTreatment": {
    "type": "string",
    "enum": [
     "none",
     "restrictReservations"
    ],
    "default": "none",
    "description": "No-Show Treatment (pack p.12)"
   },
   "noShowThreshold": {
    "type": "integer",
    "minimum": 1,
    "nullable": true,
    "description": "No-shows that trigger the restriction; required for restrictReservations"
   },
   "noShowWindowDays": {
    "type": "integer",
    "minimum": 1,
    "nullable": true,
    "description": "Window in which no-shows are counted; required for restrictReservations"
   },
   "noShowRestrictionDays": {
    "type": "integer",
    "minimum": 1,
    "nullable": true,
    "default": 14,
    "description": "Days reservation privilege stays restricted. Default 14 (decided 29 September, readiness close-out)"
   },
   "cancellationLimit": {
    "type": "integer",
    "minimum": 0,
    "nullable": true,
    "description": "Reservation cancellations allowed per 30 days; empty for unlimited"
   },
   "guestUsage": {
    "type": "string",
    "enum": [
     "withMemberOnly",
     "independent"
    ],
    "default": "withMemberOnly",
    "description": "Guest Usage: whether guest tickets need the member present"
   },
   "benefitConsumption": {
    "type": "string",
    "enum": [
     "onRedemption",
     "onValidatedVisit"
    ],
    "default": "onRedemption",
    "description": "Benefit Consumption: when a benefit counter decrements"
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
    "type": "integer",
    "description": "Maximum Visits per Day; empty for unlimited",
    "nullable": true
   },
   "maximumAdmissionsPerPeriod": {
    "type": "integer",
    "description": "Maximum Admissions per admissionPeriod; empty for unlimited",
    "nullable": true
   },
   "reEntryCooldownMinutes": {
    "type": "integer",
    "description": "Re-entry Cooldown in minutes, for reEntryPolicy afterMinutes",
    "nullable": true
   },
   "concurrentReservations": {
    "type": "integer",
    "description": "Concurrent Reservations: maximum active reservations per timeslot (pack example: one). Default 1 (decided 29 September, readiness close-out)"
   },
   "noShowTreatment": {
    "type": "string",
    "enum": [
     "none",
     "restrictReservations"
    ],
    "description": "No-Show Treatment (pack p.12)"
   },
   "cancellationLimit": {
    "type": "integer",
    "description": "Cancellation Limit: reservation cancellations allowed per 30 days; empty for unlimited (decided 29 September, readiness close-out)",
    "nullable": true
   },
   "guestUsage": {
    "type": "string",
    "enum": [
     "withMemberOnly",
     "independent"
    ],
    "description": "Guest Usage: whether guest tickets need the member present. Default withMemberOnly (decided 29 September, readiness close-out)"
   },
   "benefitConsumption": {
    "type": "string",
    "enum": [
     "onRedemption",
     "onValidatedVisit"
    ],
    "description": "Benefit Consumption: when a benefit counter decrements. Default onRedemption (decided 29 September, readiness close-out)"
   },
   "walkInAllowed": {
    "type": "boolean",
    "description": "Walk-In Allowed without a reservation"
   },
   "maximumAdvanceBookingDays": {
    "type": "integer",
    "description": "Maximum Advance Booking Days",
    "nullable": true
   },
   "maximumActiveFutureReservations": {
    "type": "integer",
    "description": "Maximum Active Future Reservations",
    "nullable": true
   },
   "membershipCode": {
    "type": "string",
    "description": "Membership code"
   },
   "tier": {
    "type": "string",
    "description": "Tier",
    "nullable": true
   },
   "admissionPeriod": {
    "type": "string",
    "enum": [
     "perDay",
     "perWeek",
     "perMonth",
     "perMembershipYear"
    ],
    "description": "Period for maximumAdmissionsPerPeriod",
    "nullable": true
   },
   "reEntryPolicy": {
    "type": "string",
    "enum": [
     "unlimitedSameDay",
     "noReEntry",
     "afterMinutes",
     "venueSpecific"
    ],
    "description": "Re-entry (pack p.12)"
   },
   "reservationRequirement": {
    "type": "string",
    "enum": [
     "required",
     "optional"
    ],
    "description": "Advance Reservation (pack pp.11-12)"
   },
   "noShowThreshold": {
    "type": "integer",
    "description": "No-shows that trigger the restriction (pack example: 3)",
    "nullable": true
   },
   "noShowWindowDays": {
    "type": "integer",
    "description": "Window in which no-shows are counted (pack example: 30 days)",
    "nullable": true
   },
   "noShowRestrictionDays": {
    "type": "integer",
    "description": "Days reservation privilege stays restricted. Default 14 (decided 29 September, readiness close-out)",
    "nullable": true
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
 "RenewalAutoRenewalMembershipContinuityConfigurationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; stored as subscription.membership_renewal_policy (MembershipRenewalPolicy) (decided 29 September, data model DM4)",
  "description": "**What Renewal, Auto-Renewal & Membership Continuity Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "autoRenewEligible": {
    "type": "boolean",
    "description": "Eligible Products: this product may be auto-renewed. Default false (decided 29 September, readiness close-out)"
   },
   "autoRenewTermsVersion": {
    "type": "string",
    "description": "Consent Requirement: version of the auto-renewal terms the member accepts when opting in. Auto-renew is only ever switched on by the member's own explicit opt-in (MoM 25 Aug: subject to consent on terms and conditions), never pre-selected (decided 29 September, readiness close-out)",
    "nullable": true
   },
   "cardOnFileRequired": {
    "type": "boolean",
    "description": "Payment Method Requirement: a tokenised card on file held by the payments module is required before auto-renew can be scheduled (MoM 25 Aug); the membership engine never holds card data. Default true (decided 29 September, readiness close-out)"
   },
   "preRenewalNoticeDays": {
    "type": "integer",
    "description": "Pre-Renewal Notification: days before the charge that the member is reminded, with the amount and how to opt out. Default 14, minimum 7 (decided 29 September, readiness close-out)"
   },
   "failureHandling": {
    "type": "string",
    "enum": [
     "gracePeriod",
     "manualAction",
     "expire"
    ],
    "description": "Failure Handling after the final retry (pack p.16: Payment Failed -> Retry -> Grace Period -> Manual Action -> Expired). Default gracePeriod (decided 29 September, readiness close-out)"
   },
   "membershipCode": {
    "type": "string",
    "description": "Membership code"
   },
   "renewalModes": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "manual",
      "customerSelfService",
      "agentAssisted",
      "autoRenewal",
      "invitationOnly",
      "nonRenewable"
     ]
    },
    "description": "Renewal Modes (pack p.15); nonRenewable excludes the others"
   },
   "renewalWindowOpensDaysBefore": {
    "type": "integer",
    "description": "Renewal Window opens this many days before expiry. Default 60, the pack's example"
   },
   "renewalWindowClosesDaysAfter": {
    "type": "integer",
    "description": "Renewal Window closes this many days after expiry. Default 30, the pack's example"
   },
   "earlyRenewalStart": {
    "type": "string",
    "enum": [
     "immediately",
     "afterCurrentExpiry"
    ],
    "description": "Early Renewal (pack p.16): when the new period starts. Default afterCurrentExpiry, preserving remaining validity as the pack advises"
   },
   "renewalPriceBasis": {
    "type": "string",
    "enum": [
     "currentMembershipPrice",
     "protectedRenewalPrice",
     "renewalDiscount",
     "loyaltyRate",
     "fixedRenewalRate"
    ],
    "description": "Renewal Pricing (pack p.16); calculated by pricing (Area 10). Default currentMembershipPrice (decided 29 September, readiness close-out)"
   },
   "renewalPricingProfile": {
    "type": "string",
    "description": "Renewal pricing profile id in pricing (Area 10)",
    "nullable": true
   },
   "retryIntervalsDays": {
    "type": "array",
    "items": {
     "type": "integer"
    },
    "description": "Retry Policy: days between failed auto-renew payment attempts. Default [2, 3], the pack's example (p.31)"
   },
   "renewalGraceDays": {
    "type": "integer",
    "description": "Days a failed renewal stays in Renewal Grace before failureHandling applies. Default 7 (decided 29 September, readiness close-out)"
   },
   "revalidateOnRenewal": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "age",
      "residency",
      "membershipStatus",
      "outstandingBalance",
      "qualification",
      "corporateAssociation"
     ]
    },
    "description": "Renewal Eligibility (pack p.16): what is revalidated at renewal"
   },
   "tierMovementAtRenewal": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "sameTierOnly",
      "upgradeAllowed",
      "downgradeAllowed",
      "suggestedTier"
     ]
    },
    "description": "Tier Movement (pack p.16)"
   },
   "cancellationPolicyId": {
    "type": "string",
    "description": "Cancellation/refund policy from the central policy management (MoM 25 Aug: refund and cancellation rules are managed centrally). Empty means no refund on cancellation unless the commercial team configures one; cancelling always stops the next auto-renew charge (decided 29 September, readiness close-out)",
    "nullable": true
   }
  }
 },
 "RenewalAutoRenewalMembershipContinuityConfigurationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Renewal, Auto-Renewal & Membership Continuity Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "autoRenewEligible": {
    "type": "boolean",
    "description": "Eligible Products: this product may be auto-renewed. Default false (decided 29 September, readiness close-out)"
   },
   "autoRenewTermsVersion": {
    "type": "string",
    "description": "Consent Requirement: version of the auto-renewal terms the member accepts when opting in. Auto-renew is only ever switched on by the member's own explicit opt-in (MoM 25 Aug: subject to consent on terms and conditions), never pre-selected (decided 29 September, readiness close-out)",
    "nullable": true
   },
   "cardOnFileRequired": {
    "type": "boolean",
    "description": "Payment Method Requirement: a tokenised card on file held by the payments module is required before auto-renew can be scheduled (MoM 25 Aug); the membership engine never holds card data. Default true (decided 29 September, readiness close-out)"
   },
   "preRenewalNoticeDays": {
    "type": "integer",
    "description": "Pre-Renewal Notification: days before the charge that the member is reminded, with the amount and how to opt out. Default 14, minimum 7 (decided 29 September, readiness close-out)"
   },
   "failureHandling": {
    "type": "string",
    "enum": [
     "gracePeriod",
     "manualAction",
     "expire"
    ],
    "description": "Failure Handling after the final retry (pack p.16: Payment Failed -> Retry -> Grace Period -> Manual Action -> Expired). Default gracePeriod (decided 29 September, readiness close-out)"
   },
   "membershipCode": {
    "type": "string",
    "description": "Membership code"
   },
   "renewalModes": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "manual",
      "customerSelfService",
      "agentAssisted",
      "autoRenewal",
      "invitationOnly",
      "nonRenewable"
     ]
    },
    "description": "Renewal Modes (pack p.15); nonRenewable excludes the others"
   },
   "renewalWindowOpensDaysBefore": {
    "type": "integer",
    "description": "Renewal Window opens this many days before expiry. Default 60, the pack's example"
   },
   "renewalWindowClosesDaysAfter": {
    "type": "integer",
    "description": "Renewal Window closes this many days after expiry. Default 30, the pack's example"
   },
   "earlyRenewalStart": {
    "type": "string",
    "enum": [
     "immediately",
     "afterCurrentExpiry"
    ],
    "description": "Early Renewal (pack p.16): when the new period starts. Default afterCurrentExpiry, preserving remaining validity as the pack advises"
   },
   "renewalPriceBasis": {
    "type": "string",
    "enum": [
     "currentMembershipPrice",
     "protectedRenewalPrice",
     "renewalDiscount",
     "loyaltyRate",
     "fixedRenewalRate"
    ],
    "description": "Renewal Pricing (pack p.16); calculated by pricing (Area 10). Default currentMembershipPrice (decided 29 September, readiness close-out)"
   },
   "renewalPricingProfile": {
    "type": "string",
    "description": "Renewal pricing profile id in pricing (Area 10)",
    "nullable": true
   },
   "retryIntervalsDays": {
    "type": "array",
    "items": {
     "type": "integer"
    },
    "description": "Retry Policy: days between failed auto-renew payment attempts. Default [2, 3], the pack's example (p.31)"
   },
   "renewalGraceDays": {
    "type": "integer",
    "description": "Days a failed renewal stays in Renewal Grace before failureHandling applies. Default 7 (decided 29 September, readiness close-out)"
   },
   "revalidateOnRenewal": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "age",
      "residency",
      "membershipStatus",
      "outstandingBalance",
      "qualification",
      "corporateAssociation"
     ]
    },
    "description": "Renewal Eligibility (pack p.16): what is revalidated at renewal"
   },
   "tierMovementAtRenewal": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "sameTierOnly",
      "upgradeAllowed",
      "downgradeAllowed",
      "suggestedTier"
     ]
    },
    "description": "Tier Movement (pack p.16)"
   },
   "cancellationPolicyId": {
    "type": "string",
    "description": "Cancellation/refund policy from the central policy management (MoM 25 Aug: refund and cancellation rules are managed centrally). Empty means no refund on cancellation unless the commercial team configures one; cancelling always stops the next auto-renew charge (decided 29 September, readiness close-out)",
    "nullable": true
   }
  }
 },
 "ValidityActivationExpiryConfigurationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; stored as subscription.membership_product (MembershipProduct) (decided 29 September, data model DM4)",
  "description": "**What Validity, Activation & Expiry Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "configuredStart": {
    "type": "string",
    "format": "date",
    "description": "Configured start: start date for fixedCalendar, seasonBased and customPeriod validity, and the start of a future-dated membership (fixedStartDate activation)",
    "nullable": true
   },
   "configuredEnd": {
    "type": "string",
    "format": "date",
    "description": "Configured end: end date for fixedCalendar, seasonBased and customPeriod validity",
    "nullable": true
   },
   "membershipCode": {
    "type": "string",
    "description": "Membership code this configuration belongs to"
   },
   "validityMethod": {
    "type": "string",
    "enum": [
     "fixedCalendar",
     "durationFromPurchase",
     "durationFromActivation",
     "seasonBased",
     "customPeriod"
    ],
    "description": "Validity Method (pack p.8)"
   },
   "durationDays": {
    "type": "integer",
    "description": "Duration in days for durationFromPurchase / durationFromActivation (the pack's example: 365)",
    "nullable": true
   },
   "seasonName": {
    "type": "string",
    "description": "Season name for seasonBased validity, e.g. the 2026-2027 season",
    "nullable": true
   },
   "activationMethod": {
    "type": "string",
    "enum": [
     "immediateOnPurchase",
     "fixedStartDate",
     "firstVisit",
     "manualActivation",
     "customerActivation",
     "membershipCardCollection",
     "identityVerification",
     "configuredTrigger"
    ],
    "description": "Activation Method (pack pp.8-9)"
   },
   "activationDeadlineDays": {
    "type": "integer",
    "description": "Activation Deadline: days after purchase by which a membership must be activated. Required when activation is deferred (firstVisit, manualActivation, customerActivation, membershipCardCollection, identityVerification, configuredTrigger); an unactivated membership expires at the deadline so it never stays open indefinitely (MoM 25 Aug fallback expiry for first-use activation). Default 90, the pack's example (decided 29 September, readiness close-out)",
    "nullable": true
   },
   "expiryRule": {
    "type": "string",
    "enum": [
     "exactExpiryDate",
     "endOfDay",
     "endOfSeason",
     "duration"
    ],
    "description": "Expiry (pack p.9)"
   },
   "gracePeriodDays": {
    "type": "integer",
    "description": "Grace Period: days after expiry during which renewal continues the membership without a gap. Default 0 (decided 29 September, readiness close-out)"
   },
   "backdatingAllowed": {
    "type": "boolean",
    "description": "Backdating: whether authorised staff may backdate activation. Default false (decided 29 September, readiness close-out)"
   },
   "backdatingApprovalRequired": {
    "type": "boolean",
    "description": "Backdating needs a second user's approval. Default true (decided 29 September, readiness close-out)"
   }
  }
 },
 "ValidityActivationExpiryConfigurationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Validity, Activation & Expiry Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "configuredStart": {
    "type": "string",
    "format": "date",
    "description": "Configured start: start date for fixedCalendar, seasonBased and customPeriod validity, and the start of a future-dated membership (fixedStartDate activation)",
    "nullable": true
   },
   "configuredEnd": {
    "type": "string",
    "format": "date",
    "description": "Configured end: end date for fixedCalendar, seasonBased and customPeriod validity",
    "nullable": true
   },
   "membershipCode": {
    "type": "string",
    "description": "Membership code this configuration belongs to"
   },
   "validityMethod": {
    "type": "string",
    "enum": [
     "fixedCalendar",
     "durationFromPurchase",
     "durationFromActivation",
     "seasonBased",
     "customPeriod"
    ],
    "description": "Validity Method (pack p.8)"
   },
   "durationDays": {
    "type": "integer",
    "description": "Duration in days for durationFromPurchase / durationFromActivation (the pack's example: 365)",
    "nullable": true
   },
   "seasonName": {
    "type": "string",
    "description": "Season name for seasonBased validity, e.g. the 2026-2027 season",
    "nullable": true
   },
   "activationMethod": {
    "type": "string",
    "enum": [
     "immediateOnPurchase",
     "fixedStartDate",
     "firstVisit",
     "manualActivation",
     "customerActivation",
     "membershipCardCollection",
     "identityVerification",
     "configuredTrigger"
    ],
    "description": "Activation Method (pack pp.8-9)"
   },
   "activationDeadlineDays": {
    "type": "integer",
    "description": "Activation Deadline: days after purchase by which a membership must be activated. Required when activation is deferred (firstVisit, manualActivation, customerActivation, membershipCardCollection, identityVerification, configuredTrigger); an unactivated membership expires at the deadline so it never stays open indefinitely (MoM 25 Aug fallback expiry for first-use activation). Default 90, the pack's example (decided 29 September, readiness close-out)",
    "nullable": true
   },
   "expiryRule": {
    "type": "string",
    "enum": [
     "exactExpiryDate",
     "endOfDay",
     "endOfSeason",
     "duration"
    ],
    "description": "Expiry (pack p.9)"
   },
   "gracePeriodDays": {
    "type": "integer",
    "description": "Grace Period: days after expiry during which renewal continues the membership without a gap. Default 0 (decided 29 September, readiness close-out)"
   },
   "backdatingAllowed": {
    "type": "boolean",
    "description": "Backdating: whether authorised staff may backdate activation. Default false (decided 29 September, readiness close-out)"
   },
   "backdatingApprovalRequired": {
    "type": "boolean",
    "description": "Backdating needs a second user's approval. Default true (decided 29 September, readiness close-out)"
   }
  }
 }
}
```
