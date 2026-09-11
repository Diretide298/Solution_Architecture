# WS22 — B2B, Reseller & OTA Partner Management board 2

**10 screens · 10 operations · 14 schemas · 2 permissions**

Platform P10 Partner Web · ships as **ticvai-control** ·
partner audience · web ·
online only

## Who this is for

**partner on web.** Everything below is how you know what is
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
| `PTR-032` | Commercial Agreement Command Center | commandCentre | 1 | 0 | — |
| `PTR-033` | Agreement & Contract Terms Builder | configEditor | 1 | 0 | — |
| `PTR-034` | Partner Rate & Net Pricing Configuration | configEditor | 1 | 0 | — |
| `PTR-035` | Commission, Margin & Incentive Management | listDetail | 1 | 0 | — |
| `PTR-036` | Credit Limit & Exposure Management | configEditor | 1 | 0 | — |
| `PTR-037` | Deposit, Guarantee & Financial Security Management | listDetail | 1 | 0 | — |
| `PTR-038` | Payment Terms, Billing & Account Configuration | listDetail | 1 | 0 | — |
| `PTR-039` | Commercial Allocation, Quota & Commitment Management | listDetail | 1 | 0 | — |
| `PTR-040` | Booking Limits, Commercial Exceptions & Approval | configEditor | 1 | 0 | — |
| `PTR-041` | Commercial Agreement 360°, Health & AI Review | listDetail | 1 | 0 | — |

## Thin screens in this batch

**PTR-035, PTR-037, PTR-038, PTR-041 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "PTR-032",
  "name": "Commercial Agreement Command Center",
  "module": "Partners",
  "requiresModule": "partner",
  "wave": 3,
  "source": {
   "pack": "B2B, Reseller & OTA Partner Management_Reference.pdf",
   "board": "2",
   "number": "8.2.1",
   "page": 23
  },
  "implementation": {
   "app": "partner-web",
   "route": "/partners/commercial-agreement-command-center-ptr-032",
   "component": "apps/partner-web/src/routes/partners/CommercialAgreementCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "PTR-001"
   ],
   "exitTo": [
    "PTR-001",
    "PTR-033",
    "PTR-034",
    "PTR-035",
    "PTR-036",
    "PTR-037",
    "PTR-038",
    "PTR-039",
    "PTR-040",
    "PTR-041"
   ],
   "inferred": false,
   "notes": "**The board's hub.** The workshop specified this module as boards of ten and opened each with a command centre; the other nine screens are that board's detail, so they are reached from here and return here.",
   "transitions": [
    {
     "to": "PTR-001",
     "trigger": "Partner Login / MFA",
     "carries": [
      "accountId",
      "sessionId"
     ],
     "provenance": "derived — PTR-001 declares entryState.params accountId, sessionId, so an edge into it must carry them"
    },
    {
     "to": "PTR-033",
     "trigger": "Works in Agreement & Contract Terms Builder",
     "provenance": "flow F131 step 1→2",
     "operation": "listCommercialAgreement"
    },
    {
     "to": "PTR-034",
     "trigger": "Works in Partner Rate & Net Pricing Configuration",
     "provenance": "flow F131 step 3→4",
     "operation": "listCommercialAgreement"
    },
    {
     "to": "PTR-035",
     "trigger": "Works in Commission, Margin & Incentive Management",
     "provenance": "flow F131 step 5→6",
     "operation": "listCommercialAgreement"
    },
    {
     "to": "PTR-036",
     "trigger": "Works in Credit Limit & Exposure Management",
     "provenance": "flow F131 step 7→8",
     "operation": "listCommercialAgreement"
    },
    {
     "to": "PTR-037",
     "trigger": "Works in Deposit, Guarantee & Financial Security Management",
     "provenance": "flow F131 step 9→10",
     "operation": "listCommercialAgreement"
    },
    {
     "to": "PTR-038",
     "trigger": "Works in Payment Terms, Billing & Account Configuration",
     "provenance": "flow F131 step 11→12",
     "operation": "listCommercialAgreement"
    },
    {
     "to": "PTR-039",
     "trigger": "Works in Commercial Allocation, Quota & Commitment Management",
     "provenance": "flow F131 step 13→14",
     "operation": "listCommercialAgreement"
    },
    {
     "to": "PTR-040",
     "trigger": "Works in Booking Limits, Commercial Exceptions & Approval",
     "provenance": "flow F131 step 15→16",
     "operation": "listCommercialAgreement"
    },
    {
     "to": "PTR-041",
     "trigger": "Works in Commercial Agreement 360°, Health & AI Review",
     "provenance": "flow F131 step 17→18",
     "operation": "listCommercialAgreement"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each agreement should show) — counts over a population, then the population",
  "purpose": "Provide commercial and finance teams with a centralized view of all partner agreements and their current commercial health.",
  "purposeNote": "Commercial management can understand the status, exposure, expiry and major commercial terms of every partner agreement from one central workspace.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search commercial agreement",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 23 §Filter by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "CommercialAgreementCommandCenterView.partner",
        "Partner Type",
        "Brand",
        "Venue",
        "Country",
        "CommercialAgreementCommandCenterView.agreementType",
        "Status",
        "CommercialAgreementCommandCenterView.commercialOwner",
        "Expiry",
        "Credit Status",
        "Risk"
       ],
       "notes": "The pack filters this screen by partner, partner type, brand, venue, country, agreement type and 5 more — which are present is a decision the pack already made.",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 23 §Filter by"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Active Agreements",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 23 §Display",
       "bindsTo": "CommercialAgreementCommandCenterView.activeAgreements"
      },
      {
       "kind": "metricTile",
       "label": "Draft Agreements",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 23 §Display",
       "bindsTo": "CommercialAgreementCommandCenterView.draftAgreements"
      },
      {
       "kind": "metricTile",
       "label": "Pending Approval",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 23 §Display",
       "bindsTo": "CommercialAgreementCommandCenterView.pendingApproval"
      },
      {
       "kind": "metricTile",
       "label": "Agreements Expiring Soon",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 23 §Display",
       "bindsTo": "CommercialAgreementCommandCenterView.agreementsExpiringSoon"
      },
      {
       "kind": "metricTile",
       "label": "Expired Agreements",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 23 §Display",
       "bindsTo": "CommercialAgreementCommandCenterView.expiredAgreements"
      },
      {
       "kind": "metricTile",
       "label": "Partners on Credit Hold",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 23 §Display",
       "bindsTo": "CommercialAgreementCommandCenterView.partnersOnCreditHold"
      },
      {
       "kind": "metricTile",
       "label": "Total Approved Credit",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 23 §Display",
       "bindsTo": "CommercialAgreementCommandCenterView.totalApprovedCredit"
      },
      {
       "kind": "metricTile",
       "label": "Current Credit Exposure",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 23 §Display",
       "bindsTo": "CommercialAgreementCommandCenterView.currentCreditExposure"
      },
      {
       "kind": "metricTile",
       "label": "Outstanding Receivables",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 23 §Display",
       "bindsTo": "CommercialAgreementCommandCenterView.outstandingReceivables"
      },
      {
       "kind": "metricTile",
       "label": "Active Commercial Allocations",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 23 §Display",
       "bindsTo": "CommercialAgreementCommandCenterView.activeCommercialAllocations"
      },
      {
       "kind": "metricTile",
       "label": "Agreements With Exceptions",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 23 §Display",
       "bindsTo": "CommercialAgreementCommandCenterView.agreementsWithExceptions"
      },
      {
       "kind": "metricTile",
       "label": "Commercial Risk Alerts",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 23 §Display",
       "bindsTo": "CommercialAgreementCommandCenterView.commercialRiskAlerts"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every commercial agreement",
       "columns": [
        "CommercialAgreementCommandCenterView.agreementId",
        "CommercialAgreementCommandCenterView.partner",
        "CommercialAgreementCommandCenterView.agreementType",
        "CommercialAgreementCommandCenterView.brandVenue",
        "CommercialAgreementCommandCenterView.market",
        "CommercialAgreementCommandCenterView.effectiveFrom",
        "CommercialAgreementCommandCenterView.effectiveTo",
        "CommercialAgreementCommandCenterView.pricingModel",
        "CommercialAgreementCommandCenterView.commissionModel",
        "CommercialAgreementCommandCenterView.paymentTerms",
        "CommercialAgreementCommandCenterView.creditLimit",
        "CommercialAgreementCommandCenterView.currentExposure",
        "CommercialAgreementCommandCenterView.allocationModel",
        "CommercialAgreementCommandCenterView.agreementStatus",
        "CommercialAgreementCommandCenterView.commercialOwner"
       ],
       "bindsTo": "CommercialAgreementCommandCenterView",
       "operation": "listCommercialAgreement",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 23 §Each agreement should show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected commercial agreement",
       "bindsTo": "CommercialAgreementCommandCenterView",
       "columns": [
        "CommercialAgreementCommandCenterView.agreementId",
        "CommercialAgreementCommandCenterView.partner",
        "CommercialAgreementCommandCenterView.agreementType",
        "CommercialAgreementCommandCenterView.brandVenue",
        "CommercialAgreementCommandCenterView.market",
        "CommercialAgreementCommandCenterView.effectiveFrom",
        "CommercialAgreementCommandCenterView.effectiveTo",
        "CommercialAgreementCommandCenterView.pricingModel",
        "CommercialAgreementCommandCenterView.commissionModel",
        "CommercialAgreementCommandCenterView.paymentTerms",
        "CommercialAgreementCommandCenterView.creditLimit",
        "CommercialAgreementCommandCenterView.currentExposure",
        "CommercialAgreementCommandCenterView.allocationModel",
        "CommercialAgreementCommandCenterView.agreementStatus",
        "CommercialAgreementCommandCenterView.commercialOwner"
       ],
       "notes": null,
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 23 §Each agreement should show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The commercial agreement list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the commercial agreement untouched.",
   "emptyFirstRun": "No commercial agreement yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the commercial agreement are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCommercialAgreement",
    "contract": "subscription",
    "purpose": "Commercial Agreement Command Center",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-032"
  },
  "apisNote": "Regenerated 9 September 2026 from B2B, Reseller & OTA Partner Management_Reference.pdf page 23. 30 of 38 labels bound to a contract property; 38 of 47 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P10",
   "audience": "partner",
   "formFactor": "web",
   "shortName": "Partner Web",
   "name": "Partner Web — Reseller Portal",
   "offlineCapable": false,
   "app": "partner-web",
   "operator": "partner",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
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
  "id": "PTR-033",
  "name": "Agreement & Contract Terms Builder",
  "module": "Partners",
  "requiresModule": "partner",
  "wave": 3,
  "source": {
   "pack": "B2B, Reseller & OTA Partner Management_Reference.pdf",
   "board": "2",
   "number": "8.2.2",
   "page": 25
  },
  "implementation": {
   "app": "partner-web",
   "route": "/partners/agreement-contract-terms-builder-ptr-033",
   "component": "apps/partner-web/src/routes/partners/AgreementContractTermsBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "PTR-032"
   ],
   "exitTo": [
    "PTR-032"
   ],
   "inferred": false,
   "notes": "**Reached from PTR-032, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "PTR-032",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F131 step 2→3",
     "operation": "setAgreementContractTerm"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure; Configure/reference) and no display directory — it is settings, not a population",
  "purpose": "Create the structured commercial agreement governing the partner relationship.",
  "purposeNote": "every governed partner relationship.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Renewal Approval. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 25 §Support"
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
       "label": "Agreement ID",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 25 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Agreement Name",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 25 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Partner",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 25 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Agreement Type",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 25 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Contract Reference",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 25 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Legal Entity",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 25 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Brand",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 25 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 25 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Territory",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 25 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Currency",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 25 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Effective From",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 25 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Effective To",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 25 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Renewal Type",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 25 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Commercial Owner",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 25 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Finance Owner",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 25 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Payment Terms",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 25 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Commission Terms",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 25 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Pricing Basis",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 25 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Credit Terms",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 25 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Allocation Terms",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 25 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Cancellation Conditions",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 25 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Refund Conditions",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 25 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Booking Restrictions",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 25 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Settlement Terms",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 25 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Minimum Commitment",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 25 §Configure/reference"
      },
      {
       "kind": "selectField",
       "label": "Sales Target",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 25 §Configure/reference"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Renewal Approval",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 25 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The agreement contract terms configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the agreement contract terms untouched.",
   "emptyFirstRun": "No agreement contract terms configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setAgreementContractTerm",
    "contract": "subscription",
    "purpose": "Agreement & Contract Terms Builder",
    "trigger": "onAction",
    "invalidates": [
     "setAgreementContractTerm"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-033"
  },
  "apisNote": "Regenerated 9 September 2026 from B2B, Reseller & OTA Partner Management_Reference.pdf page 25. 0 of 0 labels bound to a contract property; 27 of 49 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P10",
   "audience": "partner",
   "formFactor": "web",
   "shortName": "Partner Web",
   "name": "Partner Web — Reseller Portal",
   "offlineCapable": false,
   "app": "partner-web",
   "operator": "partner",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
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
  "id": "PTR-034",
  "name": "Partner Rate & Net Pricing Configuration",
  "module": "Partners",
  "requiresModule": "partner",
  "wave": 3,
  "source": {
   "pack": "B2B, Reseller & OTA Partner Management_Reference.pdf",
   "board": "2",
   "number": "8.2.3",
   "page": 27
  },
  "implementation": {
   "app": "partner-web",
   "route": "/partners/partner-rate-net-pricing-configuration-ptr-034",
   "component": "apps/partner-web/src/routes/partners/PartnerRateNetPricingConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "PTR-032"
   ],
   "exitTo": [
    "PTR-032"
   ],
   "inferred": false,
   "notes": "**Reached from PTR-032, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "PTR-032",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F131 step 4→5",
     "operation": "setPartnerRateNet"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure by) and no display directory — it is settings, not a population",
  "purpose": "Define the commercial pricing basis available to a partner without recreating TICVAI's Pricing Engine.",
  "purposeNote": "the authoritative calculation service.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Partner",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 27 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Agreement",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 27 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Product",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 27 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Product Family",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 27 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 27 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Event",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 27 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Ticket Type",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 27 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Price Category",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 27 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Market",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 27 §Configure by"
      },
      {
       "kind": "selectField",
       "label": "Channel",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 27 §Configure by"
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
       "provenance": "contract operation setPartnerRateNet"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The partner rate net configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the partner rate net untouched.",
   "emptyFirstRun": "No partner rate net configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setPartnerRateNet",
    "contract": "subscription",
    "purpose": "Partner Rate & Net Pricing Configuration",
    "trigger": "onAction",
    "invalidates": [
     "setPartnerRateNet"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-034"
  },
  "apisNote": "Regenerated 9 September 2026 from B2B, Reseller & OTA Partner Management_Reference.pdf page 27. 0 of 0 labels bound to a contract property; 10 of 36 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P10",
   "audience": "partner",
   "formFactor": "web",
   "shortName": "Partner Web",
   "name": "Partner Web — Reseller Portal",
   "offlineCapable": false,
   "app": "partner-web",
   "operator": "partner",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
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
  "id": "PTR-035",
  "name": "Commission, Margin & Incentive Management",
  "module": "Partners",
  "requiresModule": "partner",
  "wave": 3,
  "source": {
   "pack": "B2B, Reseller & OTA Partner Management_Reference.pdf",
   "board": "2",
   "number": "8.2.4",
   "page": 29
  },
  "implementation": {
   "app": "partner-web",
   "route": "/partners/commission-margin-incentive-management-ptr-035",
   "component": "apps/partner-web/src/routes/partners/CommissionMarginIncentiveManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "PTR-032"
   ],
   "exitTo": [
    "PTR-032"
   ],
   "inferred": false,
   "notes": "**Reached from PTR-032, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "PTR-032",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F131 step 6→7",
     "operation": "listCommissionMarginIncentive"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure how partner commissions and commercial incentives are calculated.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Campaign Incentive. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 29 §Support"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 29"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 29"
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
       "label": "Campaign Incentive",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 29 §Support"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listCommissionMarginIncentive",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The commission margin incentive list.",
   "error": "Could not load. Names which read failed and leaves the commission margin incentive untouched.",
   "emptyFirstRun": "No commission margin incentive yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the commission margin incentive are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCommissionMarginIncentive",
    "contract": "subscription",
    "purpose": "Commission, Margin & Incentive Management",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-035"
  },
  "apisNote": "Regenerated 9 September 2026 from B2B, Reseller & OTA Partner Management_Reference.pdf page 29. 0 of 0 labels bound to a contract property; 1 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P10",
   "audience": "partner",
   "formFactor": "web",
   "shortName": "Partner Web",
   "name": "Partner Web — Reseller Portal",
   "offlineCapable": false,
   "app": "partner-web",
   "operator": "partner",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
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
  "id": "PTR-036",
  "name": "Credit Limit & Exposure Management",
  "module": "Partners",
  "requiresModule": "partner",
  "wave": 3,
  "source": {
   "pack": "B2B, Reseller & OTA Partner Management_Reference.pdf",
   "board": "2",
   "number": "8.2.5",
   "page": 30
  },
  "implementation": {
   "app": "partner-web",
   "route": "/partners/credit-limit-exposure-management-ptr-036",
   "component": "apps/partner-web/src/routes/partners/CreditLimitExposureManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "PTR-032"
   ],
   "exitTo": [
    "PTR-032"
   ],
   "inferred": false,
   "notes": "**Reached from PTR-032, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "PTR-032",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F131 step 8→9",
     "operation": "listCreditLimitExposure"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Control the financial exposure TICVAI permits for partners buying on account. This should be one of the strongest finance-control screens in the B2B module.",
  "purposeNote": "time visibility of available and utilized credit.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Credit Enabled",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 30 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Approved Credit Limit",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 30 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Currency",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 30 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Temporary Credit Limit",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 30 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Effective Dates",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 30 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Credit Owner",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 30 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Risk Classification",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 30 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Approval Authority",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 30 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Warning at 70%",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 30 §Configure"
      },
      {
       "kind": "textField",
       "label": "High Risk at 90%",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 30 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Block at 100%",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 30 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "banner",
       "label": "Permissions this screen separates",
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** Increase Limit, Reduce Limit, Temporary Increase, Place Credit Hold, Release Hold, Block Credit Transactions. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 30 §Authorized users can"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The credit limit exposure configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the credit limit exposure untouched.",
   "emptyFirstRun": "No credit limit exposure configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCreditLimitExposure",
    "contract": "subscription",
    "purpose": "Credit Limit & Exposure Management",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "CreditLimitExposureManagementView.approvedCreditLimitAed500000",
    "Open Invoices: AED 210,000",
    "CreditLimitExposureManagementView.unbilledTransactionsAed95000",
    "CreditLimitExposureManagementView.activeHoldsReservationsAed40000",
    "CreditLimitExposureManagementView.availableCreditAed155000"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-036"
  },
  "apisNote": "Regenerated 9 September 2026 from B2B, Reseller & OTA Partner Management_Reference.pdf page 30. 0 of 0 labels bound to a contract property; 22 of 31 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P10",
   "audience": "partner",
   "formFactor": "web",
   "shortName": "Partner Web",
   "name": "Partner Web — Reseller Portal",
   "offlineCapable": false,
   "app": "partner-web",
   "operator": "partner",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
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
  "id": "PTR-037",
  "name": "Deposit, Guarantee & Financial Security Management",
  "module": "Partners",
  "requiresModule": "partner",
  "wave": 3,
  "source": {
   "pack": "B2B, Reseller & OTA Partner Management_Reference.pdf",
   "board": "2",
   "number": "8.2.6",
   "page": 32
  },
  "implementation": {
   "app": "partner-web",
   "route": "/partners/deposit-guarantee-financial-security-management-ptr-037",
   "component": "apps/partner-web/src/routes/partners/DepositGuaranteeFinancialSecurityManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "PTR-032"
   ],
   "exitTo": [
    "PTR-032"
   ],
   "inferred": false,
   "notes": "**Reached from PTR-032, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "PTR-032",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F131 step 10→11",
     "operation": "listDepositGuaranteeFinancial"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Manage financial security required to support partner credit or commercial access.",
  "purposeNote": "Finance can track all financial securities supporting partner exposure and automatically enforce configured controls when security becomes insufficient or expires.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Security Deposit. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 32 §Support"
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
       "label": "Every deposit guarantee financial",
       "columns": [
        "DepositGuaranteeFinancialSecurityManagementView.creditExposureAed500000",
        "DepositGuaranteeFinancialSecurityManagementView.guaranteeAed300000",
        "DepositGuaranteeFinancialSecurityManagementView.unsecuredExposureAed200000"
       ],
       "bindsTo": "DepositGuaranteeFinancialSecurityManagementView",
       "operation": "listDepositGuaranteeFinancial",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 32 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected deposit guarantee financial",
       "bindsTo": "DepositGuaranteeFinancialSecurityManagementView",
       "columns": [
        "DepositGuaranteeFinancialSecurityManagementView.creditExposureAed500000",
        "DepositGuaranteeFinancialSecurityManagementView.guaranteeAed300000",
        "DepositGuaranteeFinancialSecurityManagementView.unsecuredExposureAed200000"
       ],
       "notes": null,
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 32 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Security Deposit",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 32 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The deposit guarantee financial list.",
   "error": "Could not load. Names which read failed and leaves the deposit guarantee financial untouched.",
   "emptyFirstRun": "No deposit guarantee financial yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the deposit guarantee financial are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listDepositGuaranteeFinancial",
    "contract": "subscription",
    "purpose": "Deposit, Guarantee & Financial Security Management",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "DepositGuaranteeFinancialSecurityManagementView.creditExposureAed500000",
    "DepositGuaranteeFinancialSecurityManagementView.guaranteeAed300000",
    "DepositGuaranteeFinancialSecurityManagementView.unsecuredExposureAed200000"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-037"
  },
  "apisNote": "Regenerated 9 September 2026 from B2B, Reseller & OTA Partner Management_Reference.pdf page 32. 3 of 3 labels bound to a contract property; 21 of 32 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P10",
   "audience": "partner",
   "formFactor": "web",
   "shortName": "Partner Web",
   "name": "Partner Web — Reseller Portal",
   "offlineCapable": false,
   "app": "partner-web",
   "operator": "partner",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
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
  "id": "PTR-038",
  "name": "Payment Terms, Billing & Account Configuration",
  "module": "Partners",
  "requiresModule": "partner",
  "wave": 3,
  "source": {
   "pack": "B2B, Reseller & OTA Partner Management_Reference.pdf",
   "board": "2",
   "number": "8.2.7",
   "page": 33
  },
  "implementation": {
   "app": "partner-web",
   "route": "/partners/payment-terms-billing-account-configuration-ptr-038",
   "component": "apps/partner-web/src/routes/partners/PaymentTermsBillingAccountConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "PTR-032"
   ],
   "exitTo": [
    "PTR-032"
   ],
   "inferred": false,
   "notes": "**Reached from PTR-032, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "PTR-032",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F131 step 12→13",
     "operation": "setPaymentTermBilling"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Define how the partner pays TICVAI and how transactions are financially grouped.",
  "purposeNote": "Every partner transaction can be routed to the correct approved payment and billing model based on its commercial agreement.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every payment terms billing",
       "columns": [
        "PaymentTermsBillingAccountConfigurationView.currentBalance",
        "PaymentTermsBillingAccountConfigurationView.outstanding",
        "PaymentTermsBillingAccountConfigurationView.overdue",
        "PaymentTermsBillingAccountConfigurationView.availableCredit",
        "PaymentTermsBillingAccountConfigurationView.lastPayment",
        "PaymentTermsBillingAccountConfigurationView.nextInvoice",
        "PaymentTermsBillingAccountConfigurationView.oldestOutstandingInvoice"
       ],
       "bindsTo": "PaymentTermsBillingAccountConfigurationView",
       "operation": "setPaymentTermBilling",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 33 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected payment terms billing",
       "bindsTo": "PaymentTermsBillingAccountConfigurationView",
       "columns": [
        "PaymentTermsBillingAccountConfigurationView.currentBalance",
        "PaymentTermsBillingAccountConfigurationView.outstanding",
        "PaymentTermsBillingAccountConfigurationView.overdue",
        "PaymentTermsBillingAccountConfigurationView.availableCredit",
        "PaymentTermsBillingAccountConfigurationView.lastPayment",
        "PaymentTermsBillingAccountConfigurationView.nextInvoice",
        "PaymentTermsBillingAccountConfigurationView.oldestOutstandingInvoice"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Important Boundary”.",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 33 §Show"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Payment Link",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 33 §Allow/reference"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The payment terms billing list.",
   "error": "Could not load. Names which read failed and leaves the payment terms billing untouched.",
   "emptyFirstRun": "No payment terms billing yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the payment terms billing are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setPaymentTermBilling",
    "contract": "subscription",
    "purpose": "Payment Terms, Billing & Account Configuration",
    "trigger": "onAction",
    "invalidates": [
     "setPaymentTermBilling"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "PaymentTermsBillingAccountConfigurationView.currentBalance",
    "PaymentTermsBillingAccountConfigurationView.outstanding",
    "PaymentTermsBillingAccountConfigurationView.overdue",
    "PaymentTermsBillingAccountConfigurationView.availableCredit",
    "PaymentTermsBillingAccountConfigurationView.lastPayment",
    "PaymentTermsBillingAccountConfigurationView.nextInvoice"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-038"
  },
  "apisNote": "Regenerated 9 September 2026 from B2B, Reseller & OTA Partner Management_Reference.pdf page 33. 7 of 7 labels bound to a contract property; 17 of 41 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P10",
   "audience": "partner",
   "formFactor": "web",
   "shortName": "Partner Web",
   "name": "Partner Web — Reseller Portal",
   "offlineCapable": false,
   "app": "partner-web",
   "operator": "partner",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
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
  "id": "PTR-039",
  "name": "Commercial Allocation, Quota & Commitment Management",
  "module": "Partners",
  "requiresModule": "partner",
  "wave": 3,
  "source": {
   "pack": "B2B, Reseller & OTA Partner Management_Reference.pdf",
   "board": "2",
   "number": "8.2.8",
   "page": 35
  },
  "implementation": {
   "app": "partner-web",
   "route": "/partners/commercial-allocation-quota-commitment-management-ptr-039",
   "component": "apps/partner-web/src/routes/partners/CommercialAllocationQuotaCommitmentManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "PTR-032"
   ],
   "exitTo": [
    "PTR-032"
   ],
   "inferred": false,
   "notes": "**Reached from PTR-032, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "PTR-032",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F131 step 14→15",
     "operation": "listCommercialAllocationQuota"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Define the commercial commitment of inventory to a partner. This differs from Area 4's operational channel allocation.",
  "purposeNote": "permitted availability with central capacity management.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 6 actions on this screen and the screen declares 1 operation.** Unserved: Guaranteed Allocation, On-Request Allocation, Shared Allocation, Percentage Allocation, Rolling Allocation, Seasonal Allocation. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 35 §Support"
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
       "label": "Every commercial allocation quota",
       "columns": [
        "CommercialAllocationQuotaCommitmentManagementView.allocated",
        "CommercialAllocationQuotaCommitmentManagementView.booked",
        "CommercialAllocationQuotaCommitmentManagementView.sold",
        "CommercialAllocationQuotaCommitmentManagementView.returned",
        "CommercialAllocationQuotaCommitmentManagementView.remaining",
        "CommercialAllocationQuotaCommitmentManagementView.utilization",
        "CommercialAllocationQuotaCommitmentManagementView.commitmentAchievement"
       ],
       "bindsTo": "CommercialAllocationQuotaCommitmentManagementView",
       "operation": "listCommercialAllocationQuota",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 35 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected commercial allocation quota",
       "bindsTo": "CommercialAllocationQuotaCommitmentManagementView",
       "columns": [
        "CommercialAllocationQuotaCommitmentManagementView.allocated",
        "CommercialAllocationQuotaCommitmentManagementView.booked",
        "CommercialAllocationQuotaCommitmentManagementView.sold",
        "CommercialAllocationQuotaCommitmentManagementView.returned",
        "CommercialAllocationQuotaCommitmentManagementView.remaining",
        "CommercialAllocationQuotaCommitmentManagementView.utilization",
        "CommercialAllocationQuotaCommitmentManagementView.commitmentAchievement"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Area 4 asks”, “This screen asks”, “Integration”.",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 35 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Guaranteed Allocation",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 35 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "On-Request Allocation",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 35 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Shared Allocation",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 35 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Percentage Allocation",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 35 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Rolling Allocation",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 35 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Seasonal Allocation",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 35 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The commercial allocation quota list.",
   "error": "Could not load. Names which read failed and leaves the commercial allocation quota untouched.",
   "emptyFirstRun": "No commercial allocation quota yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the commercial allocation quota are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCommercialAllocationQuota",
    "contract": "subscription",
    "purpose": "Commercial Allocation, Quota & Commitment Management",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "CommercialAllocationQuotaCommitmentManagementView.allocated",
    "CommercialAllocationQuotaCommitmentManagementView.booked",
    "CommercialAllocationQuotaCommitmentManagementView.sold",
    "CommercialAllocationQuotaCommitmentManagementView.returned",
    "CommercialAllocationQuotaCommitmentManagementView.remaining",
    "CommercialAllocationQuotaCommitmentManagementView.utilization"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-039"
  },
  "apisNote": "Regenerated 9 September 2026 from B2B, Reseller & OTA Partner Management_Reference.pdf page 35. 7 of 7 labels bound to a contract property; 25 of 45 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P10",
   "audience": "partner",
   "formFactor": "web",
   "shortName": "Partner Web",
   "name": "Partner Web — Reseller Portal",
   "offlineCapable": false,
   "app": "partner-web",
   "operator": "partner",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
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
  "id": "PTR-040",
  "name": "Booking Limits, Commercial Exceptions & Approval",
  "module": "Partners",
  "requiresModule": "partner",
  "wave": 3,
  "source": {
   "pack": "B2B, Reseller & OTA Partner Management_Reference.pdf",
   "board": "2",
   "number": "8.2.9",
   "page": 37
  },
  "implementation": {
   "app": "partner-web",
   "route": "/partners/booking-limits-commercial-exceptions-approval-ptr-040",
   "component": "apps/partner-web/src/routes/partners/BookingLimitsCommercialExceptionsApproval.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "PTR-032"
   ],
   "exitTo": [
    "PTR-032"
   ],
   "inferred": false,
   "notes": "**Reached from PTR-032, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "PTR-032",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F131 step 16→17",
     "operation": "approveBookingLimitCommercial"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure; Capture) and no display directory — it is settings, not a population",
  "purpose": "Control transaction limits and provide a governed mechanism for commercial exceptions.",
  "purposeNote": "Transactions outside standard partner commercial rules cannot proceed without the appropriate documented exception and approval.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 3 actions on this screen and the screen declares 1 operation.** Unserved: Price Exception, Allocation Exception. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 37 §Support"
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
       "label": "Maximum Tickets Per Booking",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 37 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum Booking Value",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 37 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Daily Booking Limit",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 37 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Monthly Booking Limit",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 37 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Event Limit",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 37 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Product Limit",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 37 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Hold Limit",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 37 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Reservation Duration",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 37 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Cancellation Limit",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 37 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Partner",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 37 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Agreement",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 37 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Request Type",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 37 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Current Rule",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 37 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Requested Exception",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 37 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Amount/Impact",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 37 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Reason",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 37 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Effective Period",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 37 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Requester",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 37 §Capture"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Price Exception",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 37 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Allocation Exception",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 37 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Booking Limit Exception",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 37 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The booking limits commercial configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the booking limits commercial untouched.",
   "emptyFirstRun": "No booking limits commercial configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "approveBookingLimitCommercial",
    "contract": "subscription",
    "purpose": "Booking Limits, Commercial Exceptions & Approval",
    "trigger": "onAction",
    "invalidates": [
     "approveBookingLimitCommercial"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-040"
  },
  "apisNote": "Regenerated 9 September 2026 from B2B, Reseller & OTA Partner Management_Reference.pdf page 37. 0 of 0 labels bound to a contract property; 21 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P10",
   "audience": "partner",
   "formFactor": "web",
   "shortName": "Partner Web",
   "name": "Partner Web — Reseller Portal",
   "offlineCapable": false,
   "app": "partner-web",
   "operator": "partner",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
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
  "id": "PTR-041",
  "name": "Commercial Agreement 360°, Health & AI Review",
  "module": "Partners",
  "requiresModule": "partner",
  "wave": 3,
  "source": {
   "pack": "B2B, Reseller & OTA Partner Management_Reference.pdf",
   "board": "2",
   "number": "8.2.10",
   "page": 38
  },
  "implementation": {
   "app": "partner-web",
   "route": "/partners/commercial-agreement-360-health-ai-review-ptr-041",
   "component": "apps/partner-web/src/routes/partners/CommercialAgreement360HealthAiReview.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "PTR-032"
   ],
   "exitTo": [
    "PTR-032"
   ],
   "inferred": false,
   "notes": "**Reached from PTR-032, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation."
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Give management a single consolidated view of the complete commercial relationship with a partner. Board 3 manages the day-to-day operational and financial relationship with active B2B, reseller and OTA partners. The three boards now form a clean lifecycle: Board 1 — Who is the partner? Onboarding → Organization → Users → Territory → Compliance → Permissions → Activation Board 2 — Under what commercial terms can they transact? Agreement → Rates → Commission → Credit → Security → Billing → Allocation → Limits Board 3 — What happens once the partner starts doing business? Orders → Reservations → Cancellations → Statements → Reconciliation → Commission Settlement → Disputes → Performance → Risk → AI Optimization A key principle for Board 3 is that it should provide a Partner Operations 360° without rebuilding functionality already owned by Orders, Finance, Ticketing, Payment or Channel Management.",
  "purposeNote": "Management can evaluate the complete commercial relationship, financial exposure, performance and upcoming risks from a single Partner Commercial 360 workspace. Board 2 — Final Screen Register Screen Backend Screen Primary Responsibility",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 38"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 38"
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
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** Start Renewal, Request Commercial Review, Change Terms, Request Credit Review, Create Exception, Suspend Commercial Access. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 38 §Authorized users can"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listCommercialAgreementHealth",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The commercial agreement 360° list.",
   "error": "Could not load. Names which read failed and leaves the commercial agreement 360° untouched.",
   "emptyFirstRun": "No commercial agreement 360° yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the commercial agreement 360° are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCommercialAgreementHealth",
    "contract": "subscription",
    "purpose": "Commercial Agreement 360°, Health & AI Review",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "CommercialAgreement360HealthAiReviewView.contractStatus",
    "CommercialAgreement360HealthAiReviewView.effectiveDates",
    "CommercialAgreement360HealthAiReviewView.renewal",
    "CommercialAgreement360HealthAiReviewView.rateModel",
    "CommercialAgreement360HealthAiReviewView.averageDiscount"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-041"
  },
  "apisNote": "Regenerated 9 September 2026 from B2B, Reseller & OTA Partner Management_Reference.pdf page 38. 0 of 0 labels bound to a contract property; 6 of 109 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P10",
   "audience": "partner",
   "formFactor": "web",
   "shortName": "Partner Web",
   "name": "Partner Web — Reseller Portal",
   "offlineCapable": false,
   "app": "partner-web",
   "operator": "partner",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
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
 "approveBookingLimitCommercial": {
  "method": "PUT",
  "path": "/booking-limit-commercial",
  "contract": "subscription",
  "summary": "Booking Limits, Commercial Exceptions & Approval",
  "permission": "PLATFORM_CELL_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": "BookingLimitsCommercialExceptionsApprovalInput",
  "responds": "BookingLimitsCommercialExceptionsApprovalView"
 },
 "listCommercialAgreement": {
  "method": "GET",
  "path": "/commercial-agreement",
  "contract": "subscription",
  "summary": "Commercial Agreement Command Center",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "partnerType",
    "in": "query",
    "required": false
   },
   {
    "name": "brand",
    "in": "query",
    "required": false
   },
   {
    "name": "venue",
    "in": "query",
    "required": false
   },
   {
    "name": "country",
    "in": "query",
    "required": false
   },
   {
    "name": "status",
    "in": "query",
    "required": false
   },
   {
    "name": "expiry",
    "in": "query",
    "required": false
   },
   {
    "name": "creditStatus",
    "in": "query",
    "required": false
   },
   {
    "name": "risk",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "CommercialAgreementCommandCenterView"
 },
 "listCommercialAgreementHealth": {
  "method": "GET",
  "path": "/commercial-agreement-health",
  "contract": "subscription",
  "summary": "Commercial Agreement 360°, Health & AI Review",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "CommercialAgreement360HealthAiReviewView"
 },
 "listCommercialAllocationQuota": {
  "method": "GET",
  "path": "/commercial-allocation-quota",
  "contract": "subscription",
  "summary": "Commercial Allocation, Quota & Commitment Management",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "CommercialAllocationQuotaCommitmentManagementView"
 },
 "listCommissionMarginIncentive": {
  "method": "GET",
  "path": "/commission-margin-incentive",
  "contract": "subscription",
  "summary": "Commission, Margin & Incentive Management",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "CommissionMarginIncentiveManagementView"
 },
 "listCreditLimitExposure": {
  "method": "GET",
  "path": "/credit-limit-exposure",
  "contract": "subscription",
  "summary": "Credit Limit & Exposure Management",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "CreditLimitExposureManagementView"
 },
 "listDepositGuaranteeFinancial": {
  "method": "GET",
  "path": "/deposit-guarantee-financial",
  "contract": "subscription",
  "summary": "Deposit, Guarantee & Financial Security Management",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "DepositGuaranteeFinancialSecurityManagementView"
 },
 "setAgreementContractTerm": {
  "method": "PUT",
  "path": "/agreement-contract-term",
  "contract": "subscription",
  "summary": "Agreement & Contract Terms Builder",
  "permission": "PLATFORM_CELL_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": "AgreementContractTermsBuilderInput",
  "responds": "AgreementContractTermsBuilderView"
 },
 "setPartnerRateNet": {
  "method": "PUT",
  "path": "/partner-rate-net",
  "contract": "subscription",
  "summary": "Partner Rate & Net Pricing Configuration",
  "permission": "PLATFORM_CELL_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": "PartnerRateNetPricingConfigurationInput",
  "responds": "PartnerRateNetPricingConfigurationView"
 },
 "setPaymentTermBilling": {
  "method": "PUT",
  "path": "/payment-term-billing",
  "contract": "subscription",
  "summary": "Payment Terms, Billing & Account Configuration",
  "permission": "PLATFORM_CELL_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": "PaymentTermsBillingAccountConfigurationInput",
  "responds": "PaymentTermsBillingAccountConfigurationView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AgreementContractTermsBuilderInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table covers these fields** — the closest is control.api_licence at 6%, so this is not an update to anything the package stores today and no new table has been decided",
  "description": "**What Agreement & Contract Terms Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "agreementId": {
    "type": "string",
    "description": "Agreement ID"
   },
   "agreementName": {
    "type": "string",
    "description": "Agreement Name"
   },
   "partner": {
    "type": "string",
    "description": "Partner"
   },
   "agreementType": {
    "type": "string",
    "description": "Agreement Type"
   },
   "contractReference": {
    "type": "string",
    "description": "Contract Reference"
   },
   "legalEntity": {
    "type": "string",
    "description": "Legal Entity"
   },
   "brand": {
    "type": "string",
    "description": "Brand"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "territory": {
    "type": "string",
    "description": "Territory"
   },
   "currency": {
    "type": "string",
    "description": "Currency"
   },
   "effectiveFrom": {
    "type": "string",
    "description": "Effective From"
   },
   "effectiveTo": {
    "type": "string",
    "description": "Effective To"
   },
   "renewalType": {
    "type": "string",
    "description": "Renewal Type"
   },
   "commercialOwner": {
    "type": "string",
    "description": "Commercial Owner"
   },
   "financeOwner": {
    "type": "string",
    "description": "Finance Owner"
   },
   "paymentTerms": {
    "type": "string",
    "description": "Payment Terms"
   },
   "commissionTerms": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Commission Terms"
   },
   "pricingBasis": {
    "type": "string",
    "description": "Pricing Basis"
   },
   "creditTerms": {
    "type": "string",
    "description": "Credit Terms"
   },
   "allocationTerms": {
    "type": "string",
    "description": "Allocation Terms"
   },
   "cancellationConditions": {
    "type": "string",
    "description": "Cancellation Conditions"
   },
   "bookingRestrictions": {
    "type": "string",
    "description": "Booking Restrictions"
   },
   "settlementTerms": {
    "type": "string",
    "description": "Settlement Terms"
   },
   "minimumCommitment": {
    "type": "string",
    "description": "Minimum Commitment"
   },
   "salesTarget": {
    "type": "string",
    "description": "Sales Target"
   },
   "manualRenewal": {
    "type": "string",
    "description": "Manual Renewal"
   },
   "autoRenewal": {
    "type": "string",
    "description": "Auto-Renewal"
   },
   "renewalNoticePeriod": {
    "type": "string",
    "format": "date-time",
    "description": "Renewal Notice Period"
   },
   "renegotiationRequired": {
    "type": "boolean",
    "description": "Renegotiation Required"
   },
   "renewalApproval": {
    "type": "string",
    "description": "Renewal Approval"
   },
   "signedContract": {
    "type": "string",
    "description": "Signed Contract"
   },
   "addendum": {
    "type": "string",
    "description": "Addendum"
   },
   "rateSheet": {
    "type": "number",
    "description": "Rate Sheet"
   },
   "sla": {
    "type": "string",
    "description": "SLA"
   },
   "nda": {
    "type": "string",
    "description": "NDA"
   },
   "commercialAnnex": {
    "type": "string",
    "description": "Commercial Annex"
   }
  }
 },
 "AgreementContractTermsBuilderView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Agreement & Contract Terms Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "agreementId": {
    "type": "string",
    "description": "Agreement ID"
   },
   "agreementName": {
    "type": "string",
    "description": "Agreement Name"
   },
   "partner": {
    "type": "string",
    "description": "Partner"
   },
   "agreementType": {
    "type": "string",
    "description": "Agreement Type"
   },
   "contractReference": {
    "type": "string",
    "description": "Contract Reference"
   },
   "legalEntity": {
    "type": "string",
    "description": "Legal Entity"
   },
   "brand": {
    "type": "string",
    "description": "Brand"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "territory": {
    "type": "string",
    "description": "Territory"
   },
   "currency": {
    "type": "string",
    "description": "Currency"
   },
   "effectiveFrom": {
    "type": "string",
    "description": "Effective From"
   },
   "effectiveTo": {
    "type": "string",
    "description": "Effective To"
   },
   "renewalType": {
    "type": "string",
    "description": "Renewal Type"
   },
   "commercialOwner": {
    "type": "string",
    "description": "Commercial Owner"
   },
   "financeOwner": {
    "type": "string",
    "description": "Finance Owner"
   },
   "paymentTerms": {
    "type": "string",
    "description": "Payment Terms"
   },
   "commissionTerms": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Commission Terms"
   },
   "pricingBasis": {
    "type": "string",
    "description": "Pricing Basis"
   },
   "creditTerms": {
    "type": "string",
    "description": "Credit Terms"
   },
   "allocationTerms": {
    "type": "string",
    "description": "Allocation Terms"
   },
   "cancellationConditions": {
    "type": "string",
    "description": "Cancellation Conditions"
   },
   "bookingRestrictions": {
    "type": "string",
    "description": "Booking Restrictions"
   },
   "settlementTerms": {
    "type": "string",
    "description": "Settlement Terms"
   },
   "minimumCommitment": {
    "type": "string",
    "description": "Minimum Commitment"
   },
   "salesTarget": {
    "type": "string",
    "description": "Sales Target"
   },
   "manualRenewal": {
    "type": "string",
    "description": "Manual Renewal"
   },
   "autoRenewal": {
    "type": "string",
    "description": "Auto-Renewal"
   },
   "renewalNoticePeriod": {
    "type": "string",
    "format": "date-time",
    "description": "Renewal Notice Period"
   },
   "renegotiationRequired": {
    "type": "boolean",
    "description": "Renegotiation Required"
   },
   "renewalApproval": {
    "type": "string",
    "description": "Renewal Approval"
   },
   "signedContract": {
    "type": "string",
    "description": "Signed Contract"
   },
   "addendum": {
    "type": "string",
    "description": "Addendum"
   },
   "rateSheet": {
    "type": "number",
    "description": "Rate Sheet"
   },
   "sla": {
    "type": "string",
    "description": "SLA"
   },
   "nda": {
    "type": "string",
    "description": "NDA"
   },
   "commercialAnnex": {
    "type": "string",
    "description": "Commercial Annex"
   }
  }
 },
 "BookingLimitsCommercialExceptionsApprovalInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table covers these fields** — the closest is control.tenant_migration at 4%, so this is not an update to anything the package stores today and no new table has been decided",
  "description": "**What Booking Limits, Commercial Exceptions & Approval submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "maximumTicketsPerBooking": {
    "type": "string",
    "description": "Maximum Tickets Per Booking"
   },
   "maximumBookingValue": {
    "type": "string",
    "description": "Maximum Booking Value"
   },
   "dailyBookingLimit": {
    "type": "integer",
    "description": "Daily Booking Limit"
   },
   "monthlyBookingLimit": {
    "type": "integer",
    "description": "Monthly Booking Limit"
   },
   "eventLimit": {
    "type": "integer",
    "description": "Event Limit"
   },
   "productLimit": {
    "type": "integer",
    "description": "Product Limit"
   },
   "holdLimit": {
    "type": "integer",
    "description": "Hold Limit"
   },
   "reservationDuration": {
    "type": "string",
    "format": "date-time",
    "description": "Reservation Duration"
   },
   "cancellationLimit": {
    "type": "integer",
    "description": "Cancellation Limit"
   },
   "priceException": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price Exception"
   },
   "creditException": {
    "type": "string",
    "description": "Credit Exception"
   },
   "allocationException": {
    "type": "string",
    "description": "Allocation Exception"
   },
   "commissionException": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Commission Exception"
   },
   "bookingLimitException": {
    "type": "integer",
    "description": "Booking Limit Exception"
   },
   "paymentTermException": {
    "type": "string",
    "description": "Payment-Term Exception"
   },
   "cancellationException": {
    "type": "string",
    "description": "Cancellation Exception"
   },
   "partner": {
    "type": "string",
    "description": "Partner"
   },
   "agreement": {
    "type": "string",
    "description": "Agreement"
   },
   "requestType": {
    "type": "string",
    "description": "Request Type"
   },
   "currentRule": {
    "type": "string",
    "description": "Current Rule"
   },
   "requestedException": {
    "type": "string",
    "description": "Requested Exception"
   },
   "amountImpact": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Amount/Impact"
   },
   "reason": {
    "type": "string",
    "description": "Reason"
   },
   "effectivePeriod": {
    "type": "string",
    "format": "date-time",
    "description": "Effective Period"
   },
   "requester": {
    "type": "string",
    "description": "Requester"
   }
  }
 },
 "BookingLimitsCommercialExceptionsApprovalView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Booking Limits, Commercial Exceptions & Approval displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "maximumTicketsPerBooking": {
    "type": "string",
    "description": "Maximum Tickets Per Booking"
   },
   "maximumBookingValue": {
    "type": "string",
    "description": "Maximum Booking Value"
   },
   "dailyBookingLimit": {
    "type": "integer",
    "description": "Daily Booking Limit"
   },
   "monthlyBookingLimit": {
    "type": "integer",
    "description": "Monthly Booking Limit"
   },
   "eventLimit": {
    "type": "integer",
    "description": "Event Limit"
   },
   "productLimit": {
    "type": "integer",
    "description": "Product Limit"
   },
   "holdLimit": {
    "type": "integer",
    "description": "Hold Limit"
   },
   "reservationDuration": {
    "type": "string",
    "format": "date-time",
    "description": "Reservation Duration"
   },
   "cancellationLimit": {
    "type": "integer",
    "description": "Cancellation Limit"
   },
   "priceException": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price Exception"
   },
   "creditException": {
    "type": "string",
    "description": "Credit Exception"
   },
   "allocationException": {
    "type": "string",
    "description": "Allocation Exception"
   },
   "commissionException": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Commission Exception"
   },
   "bookingLimitException": {
    "type": "integer",
    "description": "Booking Limit Exception"
   },
   "paymentTermException": {
    "type": "string",
    "description": "Payment-Term Exception"
   },
   "cancellationException": {
    "type": "string",
    "description": "Cancellation Exception"
   },
   "partner": {
    "type": "string",
    "description": "Partner"
   },
   "agreement": {
    "type": "string",
    "description": "Agreement"
   },
   "requestType": {
    "type": "string",
    "description": "Request Type"
   },
   "currentRule": {
    "type": "string",
    "description": "Current Rule"
   },
   "requestedException": {
    "type": "string",
    "description": "Requested Exception"
   },
   "amountImpact": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Amount/Impact"
   },
   "reason": {
    "type": "string",
    "description": "Reason"
   },
   "effectivePeriod": {
    "type": "string",
    "format": "date-time",
    "description": "Effective Period"
   },
   "requester": {
    "type": "string",
    "description": "Requester"
   },
   "dependingOnExceptionType": {
    "type": "string",
    "description": "depending on exception type"
   },
   "dependingOnExceptionValue": {
    "type": "string",
    "description": "depending on exception value"
   }
  }
 },
 "CommercialAgreement360HealthAiReviewView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Commercial Agreement 360°, Health & AI Review displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "contractStatus": {
    "type": "string",
    "description": "Contract status"
   },
   "effectiveDates": {
    "type": "string",
    "description": "Effective dates"
   },
   "renewal": {
    "type": "string",
    "description": "Renewal"
   },
   "rateModel": {
    "type": "number",
    "description": "Rate model"
   },
   "averageDiscount": {
    "type": "number",
    "description": "Average discount"
   },
   "currentCommission": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Current commission"
   },
   "incentives": {
    "type": "string",
    "description": "Incentives"
   },
   "limit": {
    "type": "integer",
    "description": "Limit"
   },
   "exposure": {
    "type": "string",
    "description": "Exposure"
   },
   "availableCredit": {
    "type": "string",
    "description": "Available credit"
   },
   "depositGuarantee": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Deposit/guarantee"
   },
   "expiry": {
    "type": "string",
    "format": "date-time",
    "description": "Expiry"
   },
   "paymentTerms": {
    "type": "string",
    "description": "Payment terms"
   },
   "outstandingBalance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Outstanding balance"
   },
   "overdueAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Overdue amount"
   },
   "contractualAllocation": {
    "type": "string",
    "description": "Contractual allocation"
   },
   "utilization": {
    "type": "number",
    "description": "Utilization"
   },
   "minimumSales": {
    "type": "string",
    "description": "Minimum sales"
   },
   "achievement": {
    "type": "string",
    "description": "Achievement"
   },
   "activeApprovedExceptions": {
    "type": "integer",
    "description": "Active approved exceptions"
   },
   "increaseReduceCredit": {
    "type": "string",
    "description": "Increase/reduce credit"
   },
   "rebalanceAllocation": {
    "type": "string",
    "description": "Rebalance allocation"
   },
   "renewAgreement": {
    "type": "string",
    "description": "Renew agreement"
   },
   "requestUpdatedGuarantee": {
    "type": "string",
    "format": "date-time",
    "description": "Request updated guarantee"
   },
   "reduceUnusedCommitment": {
    "type": "string",
    "description": "Reduce unused commitment"
   },
   "placePartnerUnderReview": {
    "type": "string",
    "description": "Place partner under review"
   },
   "startRenewal": {
    "type": "string",
    "description": "Start Renewal"
   },
   "requestCommercialReview": {
    "type": "string",
    "description": "Request Commercial Review"
   },
   "changeTerms": {
    "type": "string",
    "description": "Change Terms"
   },
   "requestCreditReview": {
    "type": "string",
    "description": "Request Credit Review"
   },
   "commercialRisk": {
    "type": "string",
    "description": "commercial risk"
   },
   "intelligence": {
    "type": "string",
    "description": "intelligence"
   },
   "channelAllocationArea4": {
    "type": "string",
    "description": "Channel Allocation — Area 4"
   }
  }
 },
 "CommercialAgreementCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Commercial Agreement Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "activeAgreements": {
    "type": "integer",
    "description": "Active Agreements"
   },
   "draftAgreements": {
    "type": "integer",
    "description": "Draft Agreements"
   },
   "pendingApproval": {
    "type": "integer",
    "description": "Pending Approval"
   },
   "agreementsExpiringSoon": {
    "type": "string",
    "description": "Agreements Expiring Soon"
   },
   "expiredAgreements": {
    "type": "integer",
    "description": "Expired Agreements"
   },
   "partnersOnCreditHold": {
    "type": "string",
    "description": "Partners on Credit Hold"
   },
   "totalApprovedCredit": {
    "type": "integer",
    "description": "Total Approved Credit"
   },
   "currentCreditExposure": {
    "type": "string",
    "description": "Current Credit Exposure"
   },
   "outstandingReceivables": {
    "type": "integer",
    "description": "Outstanding Receivables"
   },
   "activeCommercialAllocations": {
    "type": "integer",
    "description": "Active Commercial Allocations"
   },
   "agreementsWithExceptions": {
    "type": "integer",
    "description": "Agreements With Exceptions"
   },
   "commercialRiskAlerts": {
    "type": "integer",
    "description": "Commercial Risk Alerts"
   },
   "agreementId": {
    "type": "string",
    "description": "Agreement ID"
   },
   "partner": {
    "type": "string",
    "description": "Partner"
   },
   "agreementType": {
    "type": "string",
    "description": "Agreement Type"
   },
   "brandVenue": {
    "type": "string",
    "description": "Brand/Venue"
   },
   "market": {
    "type": "string",
    "description": "Market"
   },
   "effectiveFrom": {
    "type": "string",
    "description": "Effective From"
   },
   "effectiveTo": {
    "type": "string",
    "description": "Effective To"
   },
   "pricingModel": {
    "type": "string",
    "description": "Pricing Model"
   },
   "commissionModel": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Commission Model"
   },
   "paymentTerms": {
    "type": "integer",
    "description": "Payment Terms"
   },
   "creditLimit": {
    "type": "integer",
    "description": "Credit Limit"
   },
   "currentExposure": {
    "type": "string",
    "description": "Current Exposure"
   },
   "allocationModel": {
    "type": "string",
    "description": "Allocation Model"
   },
   "agreementStatus": {
    "type": "integer",
    "description": "Agreement Status"
   },
   "commercialOwner": {
    "type": "string",
    "description": "Commercial Owner"
   }
  }
 },
 "CommercialAllocationQuotaCommitmentManagementView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Commercial Allocation, Quota & Commitment Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "guaranteedAllocation": {
    "type": "string",
    "description": "Guaranteed Allocation"
   },
   "onRequestAllocation": {
    "type": "string",
    "description": "On-Request Allocation"
   },
   "sharedAllocation": {
    "type": "string",
    "description": "Shared Allocation"
   },
   "fixedQuantity": {
    "type": "integer",
    "description": "Fixed Quantity"
   },
   "percentageAllocation": {
    "type": "number",
    "description": "Percentage Allocation"
   },
   "rollingAllocation": {
    "type": "string",
    "description": "Rolling Allocation"
   },
   "seasonalAllocation": {
    "type": "string",
    "description": "Seasonal Allocation"
   },
   "useItOrReleaseIt": {
    "type": "string",
    "description": "Use-it-or-release-it"
   },
   "takeOrPayWhereCommerciallyApplicable": {
    "type": "string",
    "description": "Take-or-pay where commercially applicable"
   },
   "guaranteedMinimum": {
    "type": "string",
    "description": "Guaranteed minimum"
   },
   "automaticRelease": {
    "type": "string",
    "description": "Automatic release"
   },
   "manualRelease": {
    "type": "string",
    "description": "Manual release"
   },
   "partner": {
    "type": "string",
    "description": "Partner"
   },
   "agreement": {
    "type": "string",
    "description": "Agreement"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "ticketType": {
    "type": "string",
    "description": "Ticket Type"
   },
   "quantity": {
    "type": "integer",
    "description": "Quantity"
   },
   "minimumCommitment": {
    "type": "string",
    "description": "Minimum Commitment"
   },
   "maximumAllocation": {
    "type": "string",
    "description": "Maximum Allocation"
   },
   "returnRule": {
    "type": "string",
    "description": "Return Rule"
   },
   "sellThroughTarget": {
    "type": "string",
    "description": "Sell-Through Target"
   },
   "allocated": {
    "type": "string",
    "description": "Allocated"
   },
   "booked": {
    "type": "string",
    "description": "Booked"
   },
   "sold": {
    "type": "string",
    "description": "Sold"
   },
   "returned": {
    "type": "string",
    "description": "Returned"
   },
   "remaining": {
    "type": "string",
    "description": "Remaining"
   },
   "utilization": {
    "type": "number",
    "description": "Utilization"
   },
   "commitmentAchievement": {
    "type": "string",
    "description": "Commitment Achievement"
   }
  }
 },
 "CommissionMarginIncentiveManagementView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Commission, Margin & Incentive Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "fixedPercentage": {
    "type": "number",
    "description": "Fixed Percentage"
   },
   "fixedAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Fixed Amount"
   },
   "productSpecificCommission": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Product-Specific Commission"
   },
   "tieredCommission": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Tiered Commission"
   },
   "volumeBasedCommission": {
    "type": "integer",
    "description": "Volume-Based Commission"
   },
   "revenueBasedCommission": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue-Based Commission"
   },
   "performanceIncentive": {
    "type": "string",
    "description": "Performance Incentive"
   },
   "campaignIncentive": {
    "type": "string",
    "description": "Campaign Incentive"
   },
   "partner": {
    "type": "string",
    "description": "Partner"
   },
   "agreement": {
    "type": "string",
    "description": "Agreement"
   },
   "product": {
    "type": "string",
    "description": "Product"
   }
  }
 },
 "CreditLimitExposureManagementView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Credit Limit & Exposure Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "creditEnabled": {
    "type": "boolean",
    "description": "Credit Enabled"
   },
   "approvedCreditLimit": {
    "type": "integer",
    "description": "Approved Credit Limit"
   },
   "currency": {
    "type": "string",
    "description": "Currency"
   },
   "temporaryCreditLimit": {
    "type": "integer",
    "description": "Temporary Credit Limit"
   },
   "effectiveDates": {
    "type": "string",
    "description": "Effective Dates"
   },
   "creditOwner": {
    "type": "string",
    "description": "Credit Owner"
   },
   "riskClassification": {
    "type": "string",
    "description": "Risk Classification"
   },
   "approvalAuthority": {
    "type": "string",
    "description": "Approval Authority"
   },
   "warningAt70": {
    "type": "number",
    "description": "Warning at 70%"
   },
   "highRiskAt90": {
    "type": "number",
    "description": "High Risk at 90%"
   },
   "approvedCreditLimitAed500000": {
    "type": "integer",
    "description": "Approved Credit Limit: AED 500,000"
   },
   "unbilledTransactionsAed95000": {
    "type": "string",
    "description": "Unbilled Transactions: AED 95,000"
   },
   "activeHoldsReservationsAed40000": {
    "type": "integer",
    "description": "Active Holds/Reservations: AED 40,000"
   },
   "availableCreditAed155000": {
    "type": "string",
    "description": "Available Credit: AED 155,000"
   },
   "increaseLimit": {
    "type": "integer",
    "description": "Increase Limit"
   },
   "reduceLimit": {
    "type": "integer",
    "description": "Reduce Limit"
   },
   "temporaryIncrease": {
    "type": "string",
    "description": "Temporary Increase"
   },
   "placeCreditHold": {
    "type": "string",
    "description": "Place Credit Hold"
   },
   "unlessAnApprovedExceptionExists": {
    "type": "string",
    "description": "unless an approved exception exists"
   }
  }
 },
 "DepositGuaranteeFinancialSecurityManagementView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Deposit, Guarantee & Financial Security Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "cashDeposit": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Cash Deposit"
   },
   "bankGuarantee": {
    "type": "string",
    "description": "Bank Guarantee"
   },
   "securityDeposit": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Security Deposit"
   },
   "letterOfCredit": {
    "type": "string",
    "description": "Letter of Credit"
   },
   "prepaymentBalance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Prepayment Balance"
   },
   "corporateGuarantee": {
    "type": "string",
    "description": "Corporate Guarantee"
   },
   "otherApprovedSecurity": {
    "type": "string",
    "description": "Other Approved Security"
   },
   "securityId": {
    "type": "string",
    "description": "Security ID"
   },
   "partner": {
    "type": "string",
    "description": "Partner"
   },
   "agreement": {
    "type": "string",
    "description": "Agreement"
   },
   "type": {
    "type": "string",
    "description": "Type"
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Amount"
   },
   "currency": {
    "type": "string",
    "description": "Currency"
   },
   "issuingInstitution": {
    "type": "string",
    "description": "Issuing Institution"
   },
   "reference": {
    "type": "string",
    "description": "Reference"
   },
   "effectiveDate": {
    "type": "string",
    "format": "date-time",
    "description": "Effective Date"
   },
   "expiryDate": {
    "type": "string",
    "format": "date-time",
    "description": "Expiry Date"
   },
   "document": {
    "type": "string",
    "description": "Document"
   },
   "verificationStatus": {
    "type": "string",
    "description": "Verification Status"
   },
   "creditExposureAed500000": {
    "type": "string",
    "description": "Credit Exposure: AED 500,000"
   },
   "guaranteeAed300000": {
    "type": "string",
    "description": "Guarantee: AED 300,000"
   },
   "unsecuredExposureAed200000": {
    "type": "string",
    "description": "Unsecured Exposure: AED 200,000"
   },
   "generatesWarning": {
    "type": "string",
    "description": "Generates warning"
   },
   "reducesCredit": {
    "type": "string",
    "description": "Reduces credit"
   },
   "blocksNewCreditSales": {
    "type": "string",
    "description": "Blocks new credit sales"
   },
   "placesPartnerOnHold": {
    "type": "string",
    "description": "Places partner on hold"
   },
   "requiresFinanceReview": {
    "type": "string",
    "description": "Requires finance review"
   }
  }
 },
 "PartnerRateNetPricingConfigurationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table covers these fields** — the closest is control.api_licence at 10%, so this is not an update to anything the package stores today and no new table has been decided",
  "description": "**What Partner Rate & Net Pricing Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "partner": {
    "type": "string",
    "description": "Partner"
   },
   "agreement": {
    "type": "string",
    "description": "Agreement"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "productFamily": {
    "type": "string",
    "description": "Product Family"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "ticketType": {
    "type": "string",
    "description": "Ticket Type"
   },
   "priceCategory": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price Category"
   },
   "market": {
    "type": "string",
    "description": "Market"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "effectiveFrom": {
    "type": "string",
    "description": "Effective From"
   },
   "effectiveTo": {
    "type": "string",
    "description": "Effective To"
   },
   "blackoutDates": {
    "type": "string",
    "description": "Blackout Dates"
   },
   "eventExceptions": {
    "type": "string",
    "description": "Event Exceptions"
   },
   "seasonalRate": {
    "type": "number",
    "description": "Seasonal Rate"
   },
   "minimumPermittedRate": {
    "type": "number",
    "description": "Minimum permitted rate"
   },
   "maximumDiscount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Maximum discount"
   },
   "marginFloor": {
    "type": "number",
    "description": "Margin floor"
   },
   "manualOverride": {
    "type": "string",
    "description": "Manual override"
   },
   "approvalThreshold": {
    "type": "integer",
    "description": "Approval threshold"
   }
  }
 },
 "PartnerRateNetPricingConfigurationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Partner Rate & Net Pricing Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "partner": {
    "type": "string",
    "description": "Partner"
   },
   "agreement": {
    "type": "string",
    "description": "Agreement"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "productFamily": {
    "type": "string",
    "description": "Product Family"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "ticketType": {
    "type": "string",
    "description": "Ticket Type"
   },
   "priceCategory": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price Category"
   },
   "market": {
    "type": "string",
    "description": "Market"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "effectiveFrom": {
    "type": "string",
    "description": "Effective From"
   },
   "effectiveTo": {
    "type": "string",
    "description": "Effective To"
   },
   "blackoutDates": {
    "type": "string",
    "description": "Blackout Dates"
   },
   "eventExceptions": {
    "type": "string",
    "description": "Event Exceptions"
   },
   "seasonalRate": {
    "type": "number",
    "description": "Seasonal Rate"
   },
   "minimumPermittedRate": {
    "type": "number",
    "description": "Minimum permitted rate"
   },
   "maximumDiscount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Maximum discount"
   },
   "marginFloor": {
    "type": "number",
    "description": "Margin floor"
   },
   "manualOverride": {
    "type": "string",
    "description": "Manual override"
   },
   "approvalThreshold": {
    "type": "integer",
    "description": "Approval threshold"
   }
  }
 },
 "PaymentTermsBillingAccountConfigurationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Payment Terms, Billing & Account Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "immediatePayment": {
    "type": "string",
    "description": "Immediate Payment"
   },
   "prepaid": {
    "type": "string",
    "description": "Prepaid"
   },
   "creditAccount": {
    "type": "string",
    "description": "Credit Account"
   },
   "depositBalance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Deposit Balance"
   },
   "monthlyInvoice": {
    "type": "string",
    "description": "Monthly Invoice"
   },
   "weeklyInvoice": {
    "type": "string",
    "description": "Weekly Invoice"
   },
   "perTransactionBilling": {
    "type": "string",
    "description": "Per-Transaction Billing"
   },
   "consolidatedBilling": {
    "type": "string",
    "description": "Consolidated Billing"
   },
   "billingEntity": {
    "type": "string",
    "description": "Billing Entity"
   },
   "billingCurrency": {
    "type": "string",
    "description": "Billing Currency"
   },
   "invoiceFrequency": {
    "type": "string",
    "description": "Invoice Frequency"
   },
   "invoiceGrouping": {
    "type": "string",
    "description": "Invoice Grouping"
   },
   "taxProfile": {
    "type": "string",
    "description": "Tax Profile"
   },
   "purchaseOrderRequired": {
    "type": "boolean",
    "description": "Purchase Order Required"
   },
   "statementFrequency": {
    "type": "string",
    "description": "Statement Frequency"
   },
   "billingContact": {
    "type": "string",
    "description": "Billing Contact"
   },
   "financeEmail": {
    "type": "string",
    "description": "Finance Email"
   },
   "bankTransfer": {
    "type": "string",
    "description": "Bank Transfer"
   },
   "card": {
    "type": "string",
    "description": "Card"
   },
   "paymentLink": {
    "type": "string",
    "description": "Payment Link"
   },
   "prepaidBalance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Prepaid Balance"
   },
   "otherApprovedMethod": {
    "type": "string",
    "description": "Other approved method"
   }
  }
 },
 "PaymentTermsBillingAccountConfigurationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Payment Terms, Billing & Account Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "immediatePayment": {
    "type": "string",
    "description": "Immediate Payment"
   },
   "prepaid": {
    "type": "string",
    "description": "Prepaid"
   },
   "creditAccount": {
    "type": "string",
    "description": "Credit Account"
   },
   "depositBalance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Deposit Balance"
   },
   "monthlyInvoice": {
    "type": "string",
    "description": "Monthly Invoice"
   },
   "weeklyInvoice": {
    "type": "string",
    "description": "Weekly Invoice"
   },
   "perTransactionBilling": {
    "type": "string",
    "description": "Per-Transaction Billing"
   },
   "consolidatedBilling": {
    "type": "string",
    "description": "Consolidated Billing"
   },
   "billingEntity": {
    "type": "string",
    "description": "Billing Entity"
   },
   "billingCurrency": {
    "type": "string",
    "description": "Billing Currency"
   },
   "invoiceFrequency": {
    "type": "string",
    "description": "Invoice Frequency"
   },
   "invoiceGrouping": {
    "type": "string",
    "description": "Invoice Grouping"
   },
   "taxProfile": {
    "type": "string",
    "description": "Tax Profile"
   },
   "purchaseOrderRequired": {
    "type": "boolean",
    "description": "Purchase Order Required"
   },
   "statementFrequency": {
    "type": "string",
    "description": "Statement Frequency"
   },
   "billingContact": {
    "type": "string",
    "description": "Billing Contact"
   },
   "financeEmail": {
    "type": "string",
    "description": "Finance Email"
   },
   "bankTransfer": {
    "type": "string",
    "description": "Bank Transfer"
   },
   "card": {
    "type": "string",
    "description": "Card"
   },
   "paymentLink": {
    "type": "string",
    "description": "Payment Link"
   },
   "prepaidBalance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Prepaid Balance"
   },
   "otherApprovedMethod": {
    "type": "string",
    "description": "Other approved method"
   },
   "currentBalance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Current Balance"
   },
   "outstanding": {
    "type": "string",
    "description": "Outstanding"
   },
   "overdue": {
    "type": "string",
    "description": "Overdue"
   },
   "availableCredit": {
    "type": "string",
    "description": "Available Credit"
   },
   "lastPayment": {
    "type": "string",
    "format": "date-time",
    "description": "Last Payment"
   },
   "nextInvoice": {
    "type": "string",
    "format": "date-time",
    "description": "Next Invoice"
   },
   "oldestOutstandingInvoice": {
    "type": "string",
    "description": "Oldest Outstanding Invoice"
   }
  }
 }
}
```
