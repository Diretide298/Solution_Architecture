# WS22 — B2B, Reseller & OTA Partner Management board 2

**10 screens · 14 operations · 23 schemas · 4 permissions**

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

- **Every control that can be refused must be gated.** 4 permissions apply here:
  `CREDIT_MANAGE, PARTNER_MANAGE, PLATFORM_CELL_MANAGE, PLATFORM_TENANT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `PTR-032` | Commercial Agreement Command Center | commandCentre | 2 | 0 | — |
| `PTR-033` | Agreement & Contract Terms Builder | configEditor | 1 | 0 | — |
| `PTR-034` | Partner Rate & Net Pricing Configuration | configEditor | 1 | 0 | — |
| `PTR-035` | Commission, Margin & Incentive Management | listDetail | 2 | 1 | — |
| `PTR-036` | Credit Limit & Exposure Management | configEditor | 2 | 1 | — |
| `PTR-037` | Deposit, Guarantee & Financial Security Management | listDetail | 2 | 1 | — |
| `PTR-038` | Payment Terms, Billing & Account Configuration | listDetail | 1 | 0 | — |
| `PTR-039` | Commercial Allocation, Quota & Commitment Management | listDetail | 2 | 1 | — |
| `PTR-040` | Booking Limits, Commercial Exceptions & Approval | configEditor | 1 | 0 | — |
| `PTR-041` | Commercial Agreement 360°, Health & AI Review | listDetail | 1 | 0 | — |

## Thin screens in this batch

**PTR-035, PTR-041 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

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
    },
    {
     "to": "PTR-035",
     "trigger": "Works in Commission, Margin & Incentive Management",
     "provenance": "flow F131 step 5→6",
     "operation": "listCommercialAgreement",
     "carries": [
      "agreementId"
     ]
    },
    {
     "to": "PTR-036",
     "trigger": "Works in Credit Limit & Exposure Management",
     "provenance": "flow F131 step 7→8",
     "operation": "listCommercialAgreement",
     "carries": [
      "agreementId"
     ]
    },
    {
     "to": "PTR-039",
     "trigger": "Works in Commercial Allocation, Quota & Commitment Management",
     "provenance": "flow F131 step 13→14",
     "operation": "listCommercialAgreement",
     "carries": [
      "agreementId"
     ]
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Commercial management can understand the status, exposure, expiry and major commercial terms of every partner agreement from one central workspace.",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each agreement should show) — counts over a population, then the population",
  "purpose": "Provide commercial and finance teams with a centralized view of all partner agreements and their current commercial health.",
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
       "bindsTo": "CommercialAgreementCommandCenterSummary.activeAgreements"
      },
      {
       "kind": "metricTile",
       "label": "Draft Agreements",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 23 §Display",
       "bindsTo": "CommercialAgreementCommandCenterSummary.draftAgreements"
      },
      {
       "kind": "metricTile",
       "label": "Pending Approval",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 23 §Display",
       "bindsTo": "CommercialAgreementCommandCenterSummary.pendingApproval"
      },
      {
       "kind": "metricTile",
       "label": "Agreements Expiring Soon",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 23 §Display",
       "bindsTo": "CommercialAgreementCommandCenterSummary.agreementsExpiringSoon"
      },
      {
       "kind": "metricTile",
       "label": "Expired Agreements",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 23 §Display",
       "bindsTo": "CommercialAgreementCommandCenterSummary.expiredAgreements"
      },
      {
       "kind": "metricTile",
       "label": "Partners on Credit Hold",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 23 §Display",
       "bindsTo": "CommercialAgreementCommandCenterSummary.partnersOnCreditHold"
      },
      {
       "kind": "metricTile",
       "label": "Total Approved Credit",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 23 §Display",
       "bindsTo": "CommercialAgreementCommandCenterSummary.totalApprovedCredit"
      },
      {
       "kind": "metricTile",
       "label": "Current Credit Exposure",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 23 §Display",
       "bindsTo": "CommercialAgreementCommandCenterSummary.currentCreditExposure"
      },
      {
       "kind": "metricTile",
       "label": "Outstanding Receivables",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 23 §Display",
       "bindsTo": "CommercialAgreementCommandCenterSummary.outstandingReceivables"
      },
      {
       "kind": "metricTile",
       "label": "Active Commercial Allocations",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 23 §Display",
       "bindsTo": "CommercialAgreementCommandCenterSummary.activeCommercialAllocations"
      },
      {
       "kind": "metricTile",
       "label": "Agreements With Exceptions",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 23 §Display",
       "bindsTo": "CommercialAgreementCommandCenterSummary.agreementsWithExceptions"
      },
      {
       "kind": "metricTile",
       "label": "Commercial Risk Alerts",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 23 §Display",
       "bindsTo": "CommercialAgreementCommandCenterSummary.commercialRiskAlerts"
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
        "CommercialAgreementCommandCenterView.validFrom",
        "CommercialAgreementCommandCenterView.validTo",
        "CommercialAgreementCommandCenterView.pricingModel",
        "CommercialAgreementCommandCenterView.commissionModel",
        "CommercialAgreementCommandCenterView.creditTermDays",
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
        "CommercialAgreementCommandCenterView.validFrom",
        "CommercialAgreementCommandCenterView.validTo",
        "CommercialAgreementCommandCenterView.pricingModel",
        "CommercialAgreementCommandCenterView.commissionModel",
        "CommercialAgreementCommandCenterView.creditTermDays",
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
   },
   {
    "operationId": "listCommercialAgreementHealth",
    "contract": "subscription",
    "purpose": "Commercial Agreement 360°, Health & AI Review",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-032",
   "workshopBoard": "wireframes/WS39 B2B, Reseller & OTA Partner Management Board 2.dc.html#ptr-032"
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
  "purposeNote": "every governed partner relationship.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure; Configure/reference) and no display directory — it is settings, not a population",
  "purpose": "Create the structured commercial agreement governing the partner relationship.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 3 actions on this screen and the screen declares 1 operation.** Unserved: Manual Renewal, Renewal Notice Period, Renewal Approval. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
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
       "label": "Manual Renewal",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 25 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Renewal Notice Period",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 25 §Support"
      },
      {
       "kind": "secondaryButton",
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
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-033",
   "workshopBoard": "wireframes/WS39 B2B, Reseller & OTA Partner Management Board 2.dc.html#ptr-033"
  },
  "apisNote": "Regenerated 9 September 2026 from B2B, Reseller & OTA Partner Management_Reference.pdf page 25. 0 of 0 labels bound to a contract property; 29 of 49 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "purposeNote": "the authoritative calculation service.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure by) and no display directory — it is settings, not a population",
  "purpose": "Define the commercial pricing basis available to a partner without recreating TICVAI's Pricing Engine.",
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
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-034",
   "workshopBoard": "wireframes/WS39 B2B, Reseller & OTA Partner Management Board 2.dc.html#ptr-034"
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
      },
      {
       "kind": "secondaryButton",
       "label": "Save partner commission rules",
       "operation": "setPartnerCommissionRules",
       "permission": "PARTNER_MANAGE",
       "notes": "The writer for PTR-035 (decided 29 September, writers pass; DM4).",
       "provenance": "contract subscription.yaml PUT /partner-agreements/{agreementId}/commission-rules"
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
   },
   {
    "operationId": "setPartnerCommissionRules",
    "contract": "subscription",
    "purpose": "Replace the commission and incentive rules of an agreement",
    "trigger": "onAction",
    "invalidates": [
     "listCommissionMarginIncentive"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-035",
   "workshopBoard": "wireframes/WS39 B2B, Reseller & OTA Partner Management Board 2.dc.html#ptr-035"
  },
  "apisNote": "Regenerated 9 September 2026 from B2B, Reseller & OTA Partner Management_Reference.pdf page 29. 0 of 0 labels bound to a contract property; 1 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formSetPartnerCommissionRules",
    "component": "modal",
    "trigger": "Save partner commission rules",
    "body": "**Collects what `setPartnerCommissionRules` sends before it is called.** Required: `rules`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save partner commission rules",
     "operation": "setPartnerCommissionRules"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "rules"
     ]
    },
    "provenance": "contract subscription.yaml PUT /partner-agreements/{agreementId}/commission-rules"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "agreementId",
     "from": "navigation",
     "optional": true
    }
   ]
  },
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
  "purposeNote": "time visibility of available and utilized credit.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Control the financial exposure TICVAI permits for partners buying on account. This should be one of the strongest finance-control screens in the B2B module.",
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
      },
      {
       "kind": "primaryButton",
       "label": "Save partner credit profile",
       "operation": "setPartnerCreditProfile",
       "permission": "CREDIT_MANAGE",
       "notes": "The writer for PTR-036 (decided 29 September, writers pass; DM4).",
       "provenance": "contract subscription.yaml PUT /partner-agreements/{agreementId}/credit-profile"
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
   },
   {
    "operationId": "setPartnerCreditProfile",
    "contract": "subscription",
    "purpose": "Set the credit controls of an agreement",
    "trigger": "onAction",
    "invalidates": [
     "listCreditLimitExposure"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "Open Invoices: AED 210,000",
    "CreditLimitExposureManagementView.unbilledTransactions",
    "CreditLimitExposureManagementView.activeHoldsReservations",
    "CreditLimitExposureManagementView.availableCredit"
   ],
   "params": [
    {
     "name": "agreementId",
     "from": "navigation",
     "optional": true
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-036",
   "workshopBoard": "wireframes/WS39 B2B, Reseller & OTA Partner Management Board 2.dc.html#ptr-036"
  },
  "apisNote": "Regenerated 9 September 2026 from B2B, Reseller & OTA Partner Management_Reference.pdf page 30. 0 of 0 labels bound to a contract property; 22 of 31 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formSetPartnerCreditProfile",
    "component": "modal",
    "trigger": "Save partner credit profile",
    "body": "**Collects what `setPartnerCreditProfile` sends before it is called.** Required: `id`, `partnerId`, `agreementId`, `creditEnabled`, `creditStatus`. Optional: `temporaryCreditLimit`, `temporaryLimitUntil`, `creditOwnerPrincipalId`, `approvalAuthority`, `riskClassification`, `warningThresholdPercent`, `highRiskThresholdPercent`, `blockThresholdPercent`, `effectiveFrom`, `effectiveTo`, `approvalRequestId`, `scopePath`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "PartnerCreditProfile",
    "confirm": {
     "label": "Save partner credit profile",
     "operation": "setPartnerCreditProfile"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "partnerId",
      "agreementId",
      "creditEnabled",
      "creditStatus",
      "temporaryCreditLimit",
      "temporaryLimitUntil",
      "creditOwnerPrincipalId",
      "approvalAuthority",
      "riskClassification",
      "warningThresholdPercent",
      "highRiskThresholdPercent",
      "blockThresholdPercent",
      "effectiveFrom",
      "effectiveTo",
      "approvalRequestId",
      "scopePath"
     ]
    },
    "provenance": "contract subscription.yaml PUT /partner-agreements/{agreementId}/credit-profile"
   }
  ],
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
  "purposeNote": "Finance can track all financial securities supporting partner exposure and automatically enforce configured controls when security becomes insufficient or expires.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Manage financial security required to support partner credit or commercial access.",
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
        "DepositGuaranteeFinancialSecurityManagementView.creditExposure",
        "DepositGuaranteeFinancialSecurityManagementView.securityCoverage",
        "DepositGuaranteeFinancialSecurityManagementView.unsecuredExposure"
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
        "DepositGuaranteeFinancialSecurityManagementView.creditExposure",
        "DepositGuaranteeFinancialSecurityManagementView.securityCoverage",
        "DepositGuaranteeFinancialSecurityManagementView.unsecuredExposure"
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
       "label": "Cash Deposit",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 32 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Security Deposit",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 32 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Prepayment Balance",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 32 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Other Approved Security",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 32 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Save partner security",
       "operation": "setPartnerSecurity",
       "permission": "CREDIT_MANAGE",
       "notes": "The writer for PTR-037 (decided 29 September, writers pass; DM4).",
       "provenance": "contract subscription.yaml PUT /partners/{partnerId}/securities"
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
   },
   {
    "operationId": "setPartnerSecurity",
    "contract": "subscription",
    "purpose": "Record, amend, verify or reject a partner's deposit or guarantee",
    "trigger": "onAction",
    "invalidates": [
     "listDepositGuaranteeFinancial"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "DepositGuaranteeFinancialSecurityManagementView.creditExposure",
    "DepositGuaranteeFinancialSecurityManagementView.securityCoverage",
    "DepositGuaranteeFinancialSecurityManagementView.unsecuredExposure"
   ],
   "params": [
    {
     "name": "partnerId",
     "from": "session"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-037",
   "workshopBoard": "wireframes/WS39 B2B, Reseller & OTA Partner Management Board 2.dc.html#ptr-037"
  },
  "apisNote": "Regenerated 9 September 2026 from B2B, Reseller & OTA Partner Management_Reference.pdf page 32. 3 of 3 labels bound to a contract property; 24 of 32 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formSetPartnerSecurity",
    "component": "modal",
    "trigger": "Save partner security",
    "body": "**Collects what `setPartnerSecurity` sends before it is called.** Required: `id`, `partnerId`, `securityType`, `amount`, `currency`, `effectiveDate`, `verificationStatus`. Optional: `agreementId`, `issuingInstitution`, `reference`, `expiryDate`, `documentId`, `expiryAction`, `scopePath`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "PartnerSecurity",
    "confirm": {
     "label": "Save partner security",
     "operation": "setPartnerSecurity"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "partnerId",
      "securityType",
      "amount",
      "currency",
      "effectiveDate",
      "verificationStatus",
      "agreementId",
      "issuingInstitution",
      "reference",
      "expiryDate",
      "documentId",
      "expiryAction",
      "scopePath"
     ]
    },
    "provenance": "contract subscription.yaml PUT /partners/{partnerId}/securities"
   }
  ],
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
  "purposeNote": "Every partner transaction can be routed to the correct approved payment and billing model based on its commercial agreement.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Define how the partner pays TICVAI and how transactions are financially grouped.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 8 actions on this screen and the screen declares 1 operation.** Unserved: Immediate Payment, Credit Account, Deposit Balance, Bank Transfer, Card, Prepaid Balance, Other approved method. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 33 §Support"
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
       "label": "Immediate Payment",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 33 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Credit Account",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 33 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Deposit Balance",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 33 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Bank Transfer",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 33 §Allow/reference"
      },
      {
       "kind": "secondaryButton",
       "label": "Card",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 33 §Allow/reference"
      },
      {
       "kind": "secondaryButton",
       "label": "Payment Link",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 33 §Allow/reference"
      },
      {
       "kind": "secondaryButton",
       "label": "Prepaid Balance",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 33 §Allow/reference"
      },
      {
       "kind": "secondaryButton",
       "label": "Other approved method",
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
    "trigger": "onAction"
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
   "board": "wireframes/P10 Partner Web.dc.html#ptr-038",
   "workshopBoard": "wireframes/WS39 B2B, Reseller & OTA Partner Management Board 2.dc.html#ptr-038"
  },
  "apisNote": "Regenerated 9 September 2026 from B2B, Reseller & OTA Partner Management_Reference.pdf page 33. 7 of 7 labels bound to a contract property; 24 of 41 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "purposeNote": "permitted availability with central capacity management.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Define the commercial commitment of inventory to a partner. This differs from Area 4's operational channel allocation.",
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
       "label": "Fixed Quantity",
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
      },
      {
       "kind": "secondaryButton",
       "label": "Take-or-pay where commercially applicable",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 35 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Save partner allocations",
       "operation": "setPartnerAllocations",
       "permission": "PARTNER_MANAGE",
       "notes": "The writer for PTR-039 (decided 29 September, writers pass; DM4).",
       "provenance": "contract subscription.yaml PUT /partner-agreements/{agreementId}/allocations"
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
   },
   {
    "operationId": "setPartnerAllocations",
    "contract": "subscription",
    "purpose": "Replace the allocations of an agreement",
    "trigger": "onAction",
    "invalidates": [
     "listCommercialAllocationQuota"
    ]
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
   ],
   "params": [
    {
     "name": "agreementId",
     "from": "navigation",
     "optional": true
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-039",
   "workshopBoard": "wireframes/WS39 B2B, Reseller & OTA Partner Management Board 2.dc.html#ptr-039"
  },
  "apisNote": "Regenerated 9 September 2026 from B2B, Reseller & OTA Partner Management_Reference.pdf page 35. 7 of 7 labels bound to a contract property; 27 of 45 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formSetPartnerAllocations",
    "component": "modal",
    "trigger": "Save partner allocations",
    "body": "**Collects what `setPartnerAllocations` sends before it is called.** Required: `allocations`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save partner allocations",
     "operation": "setPartnerAllocations"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "allocations"
     ]
    },
    "provenance": "contract subscription.yaml PUT /partner-agreements/{agreementId}/allocations"
   }
  ],
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
  "purposeNote": "Transactions outside standard partner commercial rules cannot proceed without the appropriate documented exception and approval.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure; Capture) and no display directory — it is settings, not a population",
  "purpose": "Control transaction limits and provide a governed mechanism for commercial exceptions.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 4 actions on this screen and the screen declares 1 operation.** Unserved: Price Exception, Credit Exception, Allocation Exception. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
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
       "label": "Credit Exception",
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
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-040",
   "workshopBoard": "wireframes/WS39 B2B, Reseller & OTA Partner Management Board 2.dc.html#ptr-040"
  },
  "apisNote": "Regenerated 9 September 2026 from B2B, Reseller & OTA Partner Management_Reference.pdf page 37. 0 of 0 labels bound to a contract property; 22 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "purposeNote": "Management can evaluate the complete commercial relationship, financial exposure, performance and upcoming risks from a single Partner Commercial 360 workspace. Board 2 — Final Screen Register Screen Backend Screen Primary Responsibility",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Give management a single consolidated view of the complete commercial relationship with a partner. Board 3 manages the day-to-day operational and financial relationship with active B2B, reseller and OTA partners. The three boards now form a clean lifecycle: Board 1 — Who is the partner? Onboarding → Organization → Users → Territory → Compliance → Permissions → Activation Board 2 — Under what commercial terms can they transact? Agreement → Rates → Commission → Credit → Security → Billing → Allocation → Limits Board 3 — What happens once the partner starts doing business? Orders → Reservations → Cancellations → Statements → Reconciliation → Commission Settlement → Disputes → Performance → Risk → AI Optimization A key principle for Board 3 is that it should provide a Partner Operations 360° without rebuilding functionality already owned by Orders, Finance, Ticketing, Payment or Channel Management.",
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
    "CommercialAgreement360HealthAiReviewView.renewal",
    "CommercialAgreement360HealthAiReviewView.rateModel",
    "CommercialAgreement360HealthAiReviewView.averageDiscount"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-041",
   "workshopBoard": "wireframes/WS39 B2B, Reseller & OTA Partner Management Board 2.dc.html#ptr-041"
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
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
    "name": "risk",
    "in": "query",
    "required": false
   },
   {
    "name": "creditStatus",
    "in": "query",
    "required": false
   },
   {
    "name": "expiringWithinDays",
    "in": "query",
    "required": false
   },
   {
    "name": "partnerId",
    "in": "query",
    "required": false
   },
   {
    "name": "agreementType",
    "in": "query",
    "required": false
   },
   {
    "name": "commercialOwner",
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
 "listCommercialAgreementHealth": {
  "method": "GET",
  "path": "/commercial-agreement-health",
  "contract": "subscription",
  "summary": "Commercial Agreement 360°, Health & AI Review",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "partnerId",
    "in": "query",
    "required": false
   },
   {
    "name": "agreementId",
    "in": "query",
    "required": false
   },
   {
    "name": "status",
    "in": "query",
    "required": false
   },
   {
    "name": "risk",
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
 "listCommercialAllocationQuota": {
  "method": "GET",
  "path": "/commercial-allocation-quota",
  "contract": "subscription",
  "summary": "Commercial Allocation, Quota & Commitment Management",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "partnerId",
    "in": "query",
    "required": false
   },
   {
    "name": "eventId",
    "in": "query",
    "required": false
   },
   {
    "name": "allocationModel",
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
 "listCommissionMarginIncentive": {
  "method": "GET",
  "path": "/commission-margin-incentive",
  "contract": "subscription",
  "summary": "Commission, Margin & Incentive Management",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "partnerId",
    "in": "query",
    "required": false
   },
   {
    "name": "agreementId",
    "in": "query",
    "required": false
   },
   {
    "name": "commissionModel",
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
 "listCreditLimitExposure": {
  "method": "GET",
  "path": "/credit-limit-exposure",
  "contract": "subscription",
  "summary": "Credit Limit & Exposure Management",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "partnerId",
    "in": "query",
    "required": false
   },
   {
    "name": "creditStatus",
    "in": "query",
    "required": false
   },
   {
    "name": "riskClassification",
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
 "listDepositGuaranteeFinancial": {
  "method": "GET",
  "path": "/deposit-guarantee-financial",
  "contract": "subscription",
  "summary": "Deposit, Guarantee & Financial Security Management",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "partnerId",
    "in": "query",
    "required": false
   },
   {
    "name": "securityType",
    "in": "query",
    "required": false
   },
   {
    "name": "verificationStatus",
    "in": "query",
    "required": false
   },
   {
    "name": "expiringWithinDays",
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
 "setAgreementContractTerm": {
  "method": "PUT",
  "path": "/agreement-contract-term",
  "contract": "subscription",
  "summary": "Agreement & Contract Terms Builder",
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
  "requestBody": "AgreementContractTermsBuilderInput",
  "responds": "AgreementContractTermsBuilderView"
 },
 "setPartnerAllocations": {
  "method": "PUT",
  "path": "/partner-agreements/{agreementId}/allocations",
  "contract": "subscription",
  "summary": "Replace the allocations of an agreement",
  "permission": "PARTNER_MANAGE",
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
  "requestBody": null,
  "responds": "PartnerApprovalRoutedResult"
 },
 "setPartnerCommissionRules": {
  "method": "PUT",
  "path": "/partner-agreements/{agreementId}/commission-rules",
  "contract": "subscription",
  "summary": "Replace the commission and incentive rules of an agreement",
  "permission": "PARTNER_MANAGE",
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
  "requestBody": null,
  "responds": "PartnerApprovalRoutedResult"
 },
 "setPartnerCreditProfile": {
  "method": "PUT",
  "path": "/partner-agreements/{agreementId}/credit-profile",
  "contract": "subscription",
  "summary": "Set the credit controls of an agreement",
  "permission": "CREDIT_MANAGE",
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
  "requestBody": "PartnerCreditProfile",
  "responds": "PartnerApprovalRoutedResult"
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "PartnerRateNetPricingConfigurationInput",
  "responds": "PartnerRateNetPricingConfigurationView"
 },
 "setPartnerSecurity": {
  "method": "PUT",
  "path": "/partners/{partnerId}/securities",
  "contract": "subscription",
  "summary": "Record, amend, verify or reject a partner's deposit or guarantee",
  "permission": "CREDIT_MANAGE",
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
  "requestBody": "PartnerSecurity",
  "responds": "PartnerSecurity"
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
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
  "x-ticvai-persistence": "none — request only; stored as control.partner_agreement (PartnerAgreement), a new version per amendment; documents are control.partner_document rows with agreementId; legalEntity, commercialOwner and financeOwner land in legalEntityId, commercialOwnerPrincipalId and financeOwnerPrincipalId (data model DM4)",
  "description": "**What Agreement & Contract Terms Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "agreementId": {
    "type": "string",
    "format": "uuid",
    "description": "Agreement ID; omit to create"
   },
   "agreementName": {
    "type": "string",
    "description": "Agreement Name"
   },
   "partnerId": {
    "type": "string",
    "format": "uuid",
    "description": "Partner"
   },
   "agreementType": {
    "type": "string",
    "description": "Agreement Type code, seeded with reseller, ota, travelTrade, corporate, wholesale, affiliate, distribution, apiCommercial (pack p.26)"
   },
   "contractReference": {
    "type": "string",
    "description": "Contract Reference"
   },
   "legalEntity": {
    "type": "string",
    "description": "Legal Entity"
   },
   "brandId": {
    "type": "string",
    "description": "Brand id",
    "nullable": true
   },
   "allowedVenueIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "Venues the agreement covers"
   },
   "territory": {
    "type": "string",
    "description": "Territory"
   },
   "settlementCurrency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "description": "Settlement currency, ISO 4217"
   },
   "validFrom": {
    "type": "string",
    "format": "date",
    "description": "Effective From"
   },
   "validTo": {
    "type": "string",
    "format": "date",
    "description": "Effective To; empty for open-ended",
    "nullable": true
   },
   "renewalType": {
    "type": "string",
    "enum": [
     "manual",
     "auto"
    ],
    "description": "Renewal Type"
   },
   "commercialOwner": {
    "type": "string",
    "description": "Commercial Owner: staff principal id"
   },
   "financeOwner": {
    "type": "string",
    "description": "Finance Owner: staff principal id"
   },
   "creditTermDays": {
    "type": "integer",
    "description": "Payment Terms in days (0 = due immediately; Net 7/15/30/45 or custom)"
   },
   "commissionTerms": {
    "type": "string",
    "description": "Commission Terms: summary or reference to the commission rules (listCommissionMarginIncentive)",
    "nullable": true
   },
   "pricingBasis": {
    "type": "string",
    "enum": [
     "retailPrice",
     "netRate",
     "discountFromRetail",
     "markup",
     "derivedRate"
    ],
    "description": "Pricing Basis (pack p.27 pricing models)"
   },
   "creditTerms": {
    "type": "string",
    "description": "Credit Terms",
    "nullable": true
   },
   "allocationTerms": {
    "type": "string",
    "description": "Allocation Terms",
    "nullable": true
   },
   "cancellationConditions": {
    "type": "string",
    "description": "Cancellation Conditions",
    "nullable": true
   },
   "bookingRestrictions": {
    "type": "string",
    "description": "Booking Restrictions",
    "nullable": true
   },
   "settlementTerms": {
    "type": "string",
    "description": "Settlement Terms",
    "nullable": true
   },
   "minimumCommitment": {
    "type": "integer",
    "description": "Minimum Commitment: tickets over the agreement term",
    "nullable": true
   },
   "salesTarget": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Sales Target over the agreement term"
   },
   "renewalNoticeDays": {
    "type": "integer",
    "description": "Renewal Notice Period in days",
    "nullable": true
   },
   "renegotiationRequired": {
    "type": "boolean",
    "description": "Renegotiation Required"
   },
   "renewalRequiresApproval": {
    "type": "boolean",
    "description": "Renewal Approval: renewal needs approval"
   },
   "rateMode": {
    "$ref": "#/components/schemas/PartnerRateMode",
    "description": "Net rate or commission, as on PartnerAgreement"
   },
   "paymentModel": {
    "type": "string",
    "enum": [
     "creditAccount",
     "prepaid",
     "payPerTransaction"
    ],
    "description": "Payment model, the three confirmed at MoM 5 Aug and MoM 31 Aug 4.4: creditAccount (sells to an approved credit ceiling, invoiced periodically), prepaid (pre-funded wallet drawn down per sale) or payPerTransaction (card at each sale)"
   },
   "refundConditions": {
    "type": "string",
    "description": "Refund Conditions (pack p.26)",
    "nullable": true
   },
   "agreementValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Agreement value (MoM 31 Aug 4.4: each agreement captures term/value)"
   },
   "documents": {
    "type": "array",
    "description": "Document Association",
    "items": {
     "type": "object",
     "properties": {
      "documentType": {
       "type": "string",
       "enum": [
        "signedContract",
        "addendum",
        "rateSheet",
        "sla",
        "nda",
        "commercialAnnex"
       ]
      },
      "documentId": {
       "type": "string",
       "format": "uuid"
      }
     }
    }
   }
  }
 },
 "AgreementContractTermsBuilderView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over control.partner_agreement and control.partner_document and the existing subscription state, assembled at read time (data model DM4)",
  "description": "**What Agreement & Contract Terms Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "agreementId": {
    "type": "string",
    "format": "uuid",
    "description": "Agreement ID; omit to create"
   },
   "agreementName": {
    "type": "string",
    "description": "Agreement Name"
   },
   "partnerId": {
    "type": "string",
    "format": "uuid",
    "description": "Partner"
   },
   "agreementType": {
    "type": "string",
    "description": "Agreement Type code, seeded with reseller, ota, travelTrade, corporate, wholesale, affiliate, distribution, apiCommercial (pack p.26)"
   },
   "contractReference": {
    "type": "string",
    "description": "Contract Reference"
   },
   "legalEntity": {
    "type": "string",
    "description": "Legal Entity"
   },
   "brandId": {
    "type": "string",
    "description": "Brand id",
    "nullable": true
   },
   "allowedVenueIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "Venues the agreement covers"
   },
   "territory": {
    "type": "string",
    "description": "Territory"
   },
   "settlementCurrency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "description": "Settlement currency, ISO 4217"
   },
   "validFrom": {
    "type": "string",
    "format": "date",
    "description": "Effective From"
   },
   "validTo": {
    "type": "string",
    "format": "date",
    "description": "Effective To; empty for open-ended",
    "nullable": true
   },
   "renewalType": {
    "type": "string",
    "enum": [
     "manual",
     "auto"
    ],
    "description": "Renewal Type"
   },
   "commercialOwner": {
    "type": "string",
    "description": "Commercial Owner: staff principal id"
   },
   "financeOwner": {
    "type": "string",
    "description": "Finance Owner: staff principal id"
   },
   "creditTermDays": {
    "type": "integer",
    "description": "Payment Terms in days (0 = due immediately; Net 7/15/30/45 or custom)"
   },
   "commissionTerms": {
    "type": "string",
    "description": "Commission Terms: summary or reference to the commission rules (listCommissionMarginIncentive)",
    "nullable": true
   },
   "pricingBasis": {
    "type": "string",
    "enum": [
     "retailPrice",
     "netRate",
     "discountFromRetail",
     "markup",
     "derivedRate"
    ],
    "description": "Pricing Basis (pack p.27 pricing models)"
   },
   "creditTerms": {
    "type": "string",
    "description": "Credit Terms",
    "nullable": true
   },
   "allocationTerms": {
    "type": "string",
    "description": "Allocation Terms",
    "nullable": true
   },
   "cancellationConditions": {
    "type": "string",
    "description": "Cancellation Conditions",
    "nullable": true
   },
   "bookingRestrictions": {
    "type": "string",
    "description": "Booking Restrictions",
    "nullable": true
   },
   "settlementTerms": {
    "type": "string",
    "description": "Settlement Terms",
    "nullable": true
   },
   "minimumCommitment": {
    "type": "integer",
    "description": "Minimum Commitment: tickets over the agreement term",
    "nullable": true
   },
   "salesTarget": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Sales Target over the agreement term"
   },
   "renewalNoticeDays": {
    "type": "integer",
    "description": "Renewal Notice Period in days",
    "nullable": true
   },
   "renegotiationRequired": {
    "type": "boolean",
    "description": "Renegotiation Required"
   },
   "renewalRequiresApproval": {
    "type": "boolean",
    "description": "Renewal Approval: renewal needs approval"
   },
   "rateMode": {
    "$ref": "#/components/schemas/PartnerRateMode",
    "description": "Net rate or commission, as on PartnerAgreement"
   },
   "paymentModel": {
    "type": "string",
    "enum": [
     "creditAccount",
     "prepaid",
     "payPerTransaction"
    ],
    "description": "Payment model, the three confirmed at MoM 5 Aug and MoM 31 Aug 4.4: creditAccount (sells to an approved credit ceiling, invoiced periodically), prepaid (pre-funded wallet drawn down per sale) or payPerTransaction (card at each sale)"
   },
   "refundConditions": {
    "type": "string",
    "description": "Refund Conditions (pack p.26)",
    "nullable": true
   },
   "agreementValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Agreement value (MoM 31 Aug 4.4: each agreement captures term/value)"
   },
   "documents": {
    "type": "array",
    "description": "Document Association",
    "items": {
     "type": "object",
     "properties": {
      "documentType": {
       "type": "string",
       "enum": [
        "signedContract",
        "addendum",
        "rateSheet",
        "sla",
        "nda",
        "commercialAnnex"
       ]
      },
      "documentId": {
       "type": "string",
       "format": "uuid"
      }
     }
    }
   },
   "version": {
    "type": "integer",
    "description": "Agreement version; amendments create a new one"
   },
   "status": {
    "$ref": "#/components/schemas/PartnerAgreementStatus",
    "description": "Agreement status"
   }
  }
 },
 "BookingLimitsCommercialExceptionsApprovalInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; stored as control.partner_booking_limit (PartnerBookingLimit) for the limits and control.partner_commercial_exception (PartnerCommercialException) for a request or decision; the decision itself goes to approvals (data model DM4)",
  "description": "**What Booking Limits, Commercial Exceptions & Approval submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "maximumTicketsPerBooking": {
    "type": "integer",
    "description": "Maximum Tickets Per Booking",
    "nullable": true
   },
   "maximumBookingValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Maximum Booking Value"
   },
   "dailyBookingLimit": {
    "type": "integer",
    "description": "Daily Booking Limit: bookings per day (MoM 31 Aug 4.4: transactions per day)",
    "nullable": true
   },
   "monthlyBookingLimit": {
    "type": "integer",
    "description": "Monthly Booking Limit: bookings per month",
    "nullable": true
   },
   "eventLimit": {
    "type": "integer",
    "description": "Event Limit: tickets per event",
    "nullable": true
   },
   "productLimit": {
    "type": "integer",
    "description": "Product Limit: tickets per product per day",
    "nullable": true
   },
   "holdLimit": {
    "type": "integer",
    "description": "Hold Limit: tickets on hold at once",
    "nullable": true
   },
   "holdDurationMinutes": {
    "type": "integer",
    "description": "Reservation Duration: hold duration in minutes",
    "nullable": true
   },
   "cancellationLimitPercent": {
    "type": "number",
    "description": "Cancellation Limit: percent of a booking that may be cancelled without approval (decided 29 September, readiness close-out)",
    "nullable": true
   },
   "partnerId": {
    "type": "string",
    "format": "uuid",
    "description": "Partner; empty for the overall limit that applies to every partner",
    "nullable": true
   },
   "agreementId": {
    "type": "string",
    "format": "uuid",
    "description": "Agreement",
    "nullable": true
   },
   "requestType": {
    "type": "string",
    "enum": [
     "priceException",
     "creditException",
     "allocationException",
     "commissionException",
     "bookingLimitException",
     "paymentTermException",
     "cancellationException"
    ],
    "description": "Exception Request type",
    "nullable": true
   },
   "currentRule": {
    "type": "string",
    "description": "Current Rule",
    "nullable": true
   },
   "requestedException": {
    "type": "string",
    "description": "Requested Exception",
    "nullable": true
   },
   "amountImpact": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Amount/Impact"
   },
   "reason": {
    "type": "string",
    "description": "Reason",
    "nullable": true
   },
   "exceptionId": {
    "type": "string",
    "format": "uuid",
    "description": "Exception request id; omit to raise a new request",
    "nullable": true
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date",
    "description": "Effective Period start",
    "nullable": true
   },
   "effectiveTo": {
    "type": "string",
    "format": "date",
    "description": "Effective Period end",
    "nullable": true
   },
   "decision": {
    "type": "string",
    "enum": [
     "approve",
     "reject",
     "returnForChanges"
    ],
    "description": "Approver's decision on exceptionId; empty when setting limits or raising a request",
    "nullable": true
   }
  }
 },
 "BookingLimitsCommercialExceptionsApprovalView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over control.partner_booking_limit and control.partner_commercial_exception and the existing subscription state, assembled at read time (data model DM4)",
  "description": "**What Booking Limits, Commercial Exceptions & Approval displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "maximumTicketsPerBooking": {
    "type": "integer",
    "description": "Maximum Tickets Per Booking",
    "nullable": true
   },
   "maximumBookingValue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Maximum Booking Value"
   },
   "dailyBookingLimit": {
    "type": "integer",
    "description": "Daily Booking Limit: bookings per day (MoM 31 Aug 4.4: transactions per day)",
    "nullable": true
   },
   "monthlyBookingLimit": {
    "type": "integer",
    "description": "Monthly Booking Limit: bookings per month",
    "nullable": true
   },
   "eventLimit": {
    "type": "integer",
    "description": "Event Limit: tickets per event",
    "nullable": true
   },
   "productLimit": {
    "type": "integer",
    "description": "Product Limit: tickets per product per day",
    "nullable": true
   },
   "holdLimit": {
    "type": "integer",
    "description": "Hold Limit: tickets on hold at once",
    "nullable": true
   },
   "holdDurationMinutes": {
    "type": "integer",
    "description": "Reservation Duration: hold duration in minutes",
    "nullable": true
   },
   "cancellationLimitPercent": {
    "type": "number",
    "description": "Cancellation Limit: percent of a booking that may be cancelled without approval (decided 29 September, readiness close-out)",
    "nullable": true
   },
   "partnerId": {
    "type": "string",
    "format": "uuid",
    "description": "Partner; empty for the overall limit that applies to every partner",
    "nullable": true
   },
   "agreementId": {
    "type": "string",
    "format": "uuid",
    "description": "Agreement",
    "nullable": true
   },
   "requestType": {
    "type": "string",
    "enum": [
     "priceException",
     "creditException",
     "allocationException",
     "commissionException",
     "bookingLimitException",
     "paymentTermException",
     "cancellationException"
    ],
    "description": "Exception Request type",
    "nullable": true
   },
   "currentRule": {
    "type": "string",
    "description": "Current Rule",
    "nullable": true
   },
   "requestedException": {
    "type": "string",
    "description": "Requested Exception",
    "nullable": true
   },
   "amountImpact": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Amount/Impact"
   },
   "reason": {
    "type": "string",
    "description": "Reason",
    "nullable": true
   },
   "requester": {
    "type": "string",
    "description": "Requester",
    "nullable": true
   },
   "exceptionId": {
    "type": "string",
    "format": "uuid",
    "description": "Exception request id; omit to raise a new request",
    "nullable": true
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date",
    "description": "Effective Period start",
    "nullable": true
   },
   "effectiveTo": {
    "type": "string",
    "format": "date",
    "description": "Effective Period end",
    "nullable": true
   },
   "decision": {
    "type": "string",
    "enum": [
     "approve",
     "reject",
     "returnForChanges"
    ],
    "description": "Approver's decision on exceptionId; empty when setting limits or raising a request",
    "nullable": true
   },
   "approvalStatus": {
    "type": "string",
    "description": "Approval status of the exception: pendingApproval, approved, rejected, returned or expired",
    "nullable": true
   },
   "approvalRequestId": {
    "type": "string",
    "description": "Approval request",
    "nullable": true
   },
   "aiImpactSummary": {
    "type": "string",
    "description": "Advisory AI impact summary",
    "nullable": true
   }
  }
 },
 "CommercialAgreement360HealthAiReviewView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over control.partner_agreement with control.partner_security, control.partner_allocation, control.partner_commission_rule, control.partner_rate and control.partner_commercial_exception and the existing subscription state, assembled at read time (data model DM4)",
  "description": "**What Commercial Agreement 360°, Health & AI Review displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "contractStatus": {
    "$ref": "#/components/schemas/PartnerAgreementStatus",
    "description": "Contract status"
   },
   "renewal": {
    "type": "string",
    "description": "Renewal: manual or auto, and whether a renewal workflow is open"
   },
   "rateModel": {
    "type": "string",
    "enum": [
     "retailPrice",
     "netRate",
     "discountFromRetail",
     "markup",
     "derivedRate"
    ],
    "description": "Rate model"
   },
   "averageDiscount": {
    "type": "number",
    "description": "Average discount from retail, percent"
   },
   "currentCommissionPercent": {
    "type": "number",
    "description": "Current commission, percent",
    "nullable": true
   },
   "incentives": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Active incentives"
   },
   "creditLimit": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Credit limit"
   },
   "creditExposure": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Credit exposure"
   },
   "availableCredit": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Available credit"
   },
   "depositGuarantee": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Deposit/guarantee held"
   },
   "securityExpiry": {
    "type": "string",
    "format": "date",
    "description": "Security expiry",
    "nullable": true
   },
   "creditTermDays": {
    "type": "integer",
    "description": "Payment terms in days",
    "nullable": true
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
    "type": "integer",
    "description": "Contractual allocation, units"
   },
   "utilization": {
    "type": "number",
    "description": "Allocation utilisation, percent"
   },
   "minimumSales": {
    "type": "integer",
    "description": "Minimum sales commitment, units",
    "nullable": true
   },
   "achievement": {
    "type": "number",
    "description": "Commitment achievement, percent"
   },
   "activeApprovedExceptions": {
    "type": "integer",
    "description": "Active approved exceptions"
   },
   "partnerId": {
    "type": "string",
    "format": "uuid",
    "description": "Partner"
   },
   "partnerName": {
    "type": "string",
    "description": "Partner"
   },
   "agreementId": {
    "type": "string",
    "format": "uuid",
    "description": "Agreement"
   },
   "commercialOwner": {
    "type": "string",
    "description": "Commercial Owner"
   },
   "validFrom": {
    "type": "string",
    "format": "date",
    "description": "Effective period start"
   },
   "validTo": {
    "type": "string",
    "format": "date",
    "description": "Effective period end",
    "nullable": true
   },
   "riskRating": {
    "type": "string",
    "enum": [
     "low",
     "medium",
     "high",
     "critical"
    ],
    "description": "Risk"
   },
   "healthScore": {
    "type": "integer",
    "description": "Commercial Health score, 0-100"
   },
   "healthBreakdown": {
    "type": "object",
    "description": "Commercial Health by component, each 0-100",
    "properties": {
     "agreement": {
      "type": "integer"
     },
     "margin": {
      "type": "integer"
     },
     "credit": {
      "type": "integer"
     },
     "payment": {
      "type": "integer"
     },
     "security": {
      "type": "integer"
     },
     "allocation": {
      "type": "integer"
     },
     "commitment": {
      "type": "integer"
     }
    }
   },
   "recommendations": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "reviewRate",
      "adjustCredit",
      "rebalanceAllocation",
      "renewAgreement",
      "reviewCommission",
      "requestUpdatedGuarantee",
      "reduceUnusedCommitment",
      "placePartnerUnderReview"
     ]
    },
    "description": "Advisory AI Recommendations"
   },
   "aiInsights": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Advisory AI Executive Review"
   }
  }
 },
 "CommercialAgreementCommandCenterSummary": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection; the headline tiles over the list, computed at read time for the filters in force",
  "description": "**The headline figures on Commercial Agreement Command Center.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.",
  "properties": {
   "activeAgreements": {
    "type": "integer",
    "description": "Active Agreements"
   },
   "draftAgreements": {
    "type": "integer",
    "description": "Draft Agreements: pendingApproval agreements not yet submitted to the approvals engine (decided 29 September, readiness close-out)"
   },
   "pendingApproval": {
    "type": "integer",
    "description": "Pending Approval: pendingApproval agreements with an open approval request"
   },
   "agreementsExpiringSoon": {
    "type": "integer",
    "description": "Agreements Expiring Soon: status expiringSoon"
   },
   "expiredAgreements": {
    "type": "integer",
    "description": "Expired Agreements"
   },
   "partnersOnCreditHold": {
    "type": "integer",
    "description": "Partners on Credit Hold"
   },
   "totalApprovedCredit": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Total Approved Credit"
   },
   "currentCreditExposure": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Current Credit Exposure"
   },
   "outstandingReceivables": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
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
   }
  }
 },
 "CommercialAgreementCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over control.partner_agreement with control.partner, control.partner_credit_profile, control.partner_allocation and control.partner_commission_rule and the existing subscription state, assembled at read time (data model DM4)",
  "description": "**What Commercial Agreement Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "agreementId": {
    "type": "string",
    "format": "uuid",
    "description": "Agreement ID"
   },
   "partner": {
    "type": "string",
    "description": "Partner trading name"
   },
   "agreementType": {
    "type": "string",
    "description": "Agreement Type code, seeded with reseller, ota, travelTrade, corporate, wholesale, affiliate, distribution, apiCommercial (pack p.26)"
   },
   "brandVenue": {
    "type": "string",
    "description": "Brand/Venue summary of the agreement scope"
   },
   "market": {
    "type": "string",
    "description": "Market"
   },
   "validFrom": {
    "type": "string",
    "format": "date",
    "description": "Effective From"
   },
   "validTo": {
    "type": "string",
    "format": "date",
    "description": "Effective To; empty for open-ended",
    "nullable": true
   },
   "pricingModel": {
    "type": "string",
    "enum": [
     "retailPrice",
     "netRate",
     "discountFromRetail",
     "markup",
     "derivedRate"
    ],
    "description": "Pricing Model (pack p.27)"
   },
   "commissionModel": {
    "type": "string",
    "enum": [
     "fixedPercentage",
     "fixedAmount",
     "productSpecific",
     "tiered",
     "volumeBased",
     "revenueBased",
     "performanceIncentive",
     "campaignIncentive",
     "none"
    ],
    "description": "Commission Model (pack p.29); none for a net-rate agreement"
   },
   "creditTermDays": {
    "type": "integer",
    "description": "Payment Terms in days (0 = due immediately; Net 7/15/30/45 or custom)",
    "nullable": true
   },
   "creditLimit": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Credit Limit; empty unless the payment model is creditAccount"
   },
   "currentExposure": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Current Exposure"
   },
   "allocationModel": {
    "type": "string",
    "enum": [
     "guaranteed",
     "onRequest",
     "shared",
     "fixedQuantity",
     "percentage",
     "rolling",
     "seasonal",
     "none"
    ],
    "description": "Allocation Model (pack p.35)"
   },
   "agreementStatus": {
    "$ref": "#/components/schemas/PartnerAgreementStatus",
    "description": "Agreement Status"
   },
   "commercialOwner": {
    "type": "string",
    "description": "Commercial Owner"
   },
   "partnerId": {
    "type": "string",
    "format": "uuid",
    "description": "Partner"
   },
   "rateMode": {
    "$ref": "#/components/schemas/PartnerRateMode",
    "description": "Net rate or commission, as on PartnerAgreement"
   },
   "paymentModel": {
    "type": "string",
    "enum": [
     "creditAccount",
     "prepaid",
     "payPerTransaction"
    ],
    "description": "Payment model, the three confirmed at MoM 5 Aug and MoM 31 Aug 4.4: creditAccount (sells to an approved credit ceiling, invoiced periodically), prepaid (pre-funded wallet drawn down per sale) or payPerTransaction (card at each sale)"
   },
   "riskRating": {
    "type": "string",
    "enum": [
     "low",
     "medium",
     "high",
     "critical"
    ],
    "description": "Commercial risk"
   },
   "aiInsights": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Advisory AI commercial-risk flags, e.g. expiry against forward bookings"
   }
  }
 },
 "CommercialAllocationQuotaCommitmentManagementView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over control.partner_allocation (PartnerAllocation) and the existing subscription state, assembled at read time (data model DM4)",
  "description": "**What Commercial Allocation, Quota & Commitment Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "allocationPercent": {
    "type": "number",
    "description": "Percent of capacity, for the percentage model",
    "nullable": true
   },
   "partnerId": {
    "type": "string",
    "format": "uuid",
    "description": "Partner"
   },
   "agreementId": {
    "type": "string",
    "format": "uuid",
    "description": "Agreement"
   },
   "venueId": {
    "type": "string",
    "description": "Venue id"
   },
   "eventId": {
    "type": "string",
    "description": "Event id",
    "nullable": true
   },
   "productId": {
    "type": "string",
    "description": "Product id",
    "nullable": true
   },
   "ticketType": {
    "type": "string",
    "description": "Ticket Type",
    "nullable": true
   },
   "quantity": {
    "type": "integer",
    "description": "Contractual allocation quantity"
   },
   "minimumCommitment": {
    "type": "integer",
    "description": "Minimum Commitment, units",
    "nullable": true
   },
   "maximumAllocation": {
    "type": "integer",
    "description": "Maximum Allocation, units",
    "nullable": true
   },
   "returnRule": {
    "type": "string",
    "description": "Return Rule",
    "nullable": true
   },
   "sellThroughTarget": {
    "type": "number",
    "description": "Sell-Through Target, percent",
    "nullable": true
   },
   "allocated": {
    "type": "integer",
    "description": "Allocated"
   },
   "booked": {
    "type": "integer",
    "description": "Booked"
   },
   "sold": {
    "type": "integer",
    "description": "Sold"
   },
   "returned": {
    "type": "integer",
    "description": "Returned"
   },
   "remaining": {
    "type": "integer",
    "description": "Remaining"
   },
   "utilization": {
    "type": "number",
    "description": "Utilization, percent"
   },
   "commitmentAchievement": {
    "type": "number",
    "description": "Commitment Achievement, percent of the minimum commitment"
   },
   "allocationId": {
    "type": "string",
    "format": "uuid",
    "description": "Allocation id"
   },
   "allocationModel": {
    "type": "string",
    "enum": [
     "guaranteed",
     "onRequest",
     "shared",
     "fixedQuantity",
     "percentage",
     "rolling",
     "seasonal"
    ],
    "description": "Allocation Model"
   },
   "commitmentRule": {
    "type": "string",
    "enum": [
     "useItOrRelease",
     "takeOrPay",
     "guaranteedMinimum"
    ],
    "description": "Commitment Rule",
    "nullable": true
   },
   "releaseMode": {
    "type": "string",
    "enum": [
     "automatic",
     "manual"
    ],
    "description": "Release: automatic or manual"
   },
   "releaseHoursBeforeEvent": {
    "type": "integer",
    "description": "Release Date as a deadline before the event (e.g. 48 hours)",
    "nullable": true
   },
   "releaseDate": {
    "type": "string",
    "format": "date-time",
    "description": "Release Date as a fixed time",
    "nullable": true
   },
   "aiInsights": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Advisory AI under-utilisation forecast"
   }
  }
 },
 "CommissionMarginIncentiveManagementView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over control.partner_commission_rule + control.partner_commission_rule_tier (PartnerCommissionRule) and the existing subscription state, assembled at read time (data model DM4)",
  "description": "**What Commission, Margin & Incentive Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "partnerId": {
    "type": "string",
    "format": "uuid",
    "description": "Partner"
   },
   "agreementId": {
    "type": "string",
    "format": "uuid",
    "description": "Agreement"
   },
   "productId": {
    "type": "string",
    "description": "Product id",
    "nullable": true
   },
   "ruleId": {
    "type": "string",
    "format": "uuid",
    "description": "Commission rule id"
   },
   "commissionModel": {
    "type": "string",
    "enum": [
     "fixedPercentage",
     "fixedAmount",
     "productSpecific",
     "tiered",
     "volumeBased",
     "revenueBased",
     "performanceIncentive",
     "campaignIncentive"
    ],
    "description": "Commission Model"
   },
   "productCategory": {
    "type": "string",
    "description": "Product Category",
    "nullable": true
   },
   "venueId": {
    "type": "string",
    "description": "Venue",
    "nullable": true
   },
   "eventId": {
    "type": "string",
    "description": "Event",
    "nullable": true
   },
   "market": {
    "type": "string",
    "description": "Market",
    "nullable": true
   },
   "salesChannel": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/SalesChannel"
     }
    ],
    "nullable": true,
    "description": "Sales Channel"
   },
   "commissionPercent": {
    "type": "number",
    "description": "Commission percent, for percentage models",
    "nullable": true
   },
   "commissionAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Fixed commission per ticket, for fixedAmount"
   },
   "tiers": {
    "type": "array",
    "description": "Tiers for tiered/volume/revenue models, e.g. 0-1,000 tickets 8%, 1,001-5,000 10%, 5,001+ 12%",
    "items": {
     "type": "object",
     "properties": {
      "fromUnits": {
       "type": "integer"
      },
      "commissionPercent": {
       "type": "number"
      }
     }
    }
   },
   "volumeWindow": {
    "type": "string",
    "enum": [
     "calendarMonth",
     "calendarQuarter",
     "calendarYear",
     "agreementYear",
     "rolling12Months"
    ],
    "description": "Period over which volume is counted, as on PartnerAgreement",
    "nullable": true
   },
   "incentiveType": {
    "type": "string",
    "enum": [
     "volumeBonus",
     "growthBonus",
     "targetAchievement",
     "seasonalIncentive",
     "newProductIncentive",
     "strategicPartnerBonus"
    ],
    "description": "Incentive type",
    "nullable": true
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date",
    "description": "Effective from"
   },
   "effectiveTo": {
    "type": "string",
    "format": "date",
    "description": "Effective to",
    "nullable": true
   },
   "estimatedNetContribution": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Margin Visibility: retail price - partner rate - commission/incentive - commercial cost"
   },
   "validationIssues": {
    "type": "array",
    "description": "Conflict Detection",
    "items": {
     "type": "object",
     "properties": {
      "code": {
       "type": "string",
       "enum": [
        "overlappingCommissionRule"
       ]
      },
      "message": {
       "type": "string"
      }
     }
    }
   },
   "aiInsights": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Advisory AI observations for this row; never acted on without a human decision"
   }
  }
 },
 "CreditLimitExposureManagementView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over control.partner_credit_profile (PartnerCreditProfile) with control.partner_agreement.credit_limit and the existing subscription state, assembled at read time (data model DM4)",
  "description": "**What Credit Limit & Exposure Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "creditEnabled": {
    "type": "boolean",
    "description": "Credit Enabled"
   },
   "approvedCreditLimit": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Approved Credit Limit (PartnerAgreement.creditLimit)"
   },
   "currency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "description": "Currency of the limit (the agreement's settlement currency)"
   },
   "temporaryCreditLimit": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Temporary Credit Limit; empty when none"
   },
   "creditOwner": {
    "type": "string",
    "description": "Credit Owner"
   },
   "riskClassification": {
    "type": "string",
    "enum": [
     "low",
     "medium",
     "high",
     "critical"
    ],
    "description": "Risk Classification"
   },
   "approvalAuthority": {
    "type": "string",
    "description": "Approval Authority"
   },
   "warningThresholdPercent": {
    "type": "number",
    "description": "Threshold: warning at this utilisation percent, default 70 (decided 29 September, readiness close-out)"
   },
   "highRiskThresholdPercent": {
    "type": "number",
    "description": "Threshold: high risk at this utilisation percent, default 90 (decided 29 September, readiness close-out)"
   },
   "unbilledTransactions": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Unbilled Transactions"
   },
   "activeHoldsReservations": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Active Holds/Reservations"
   },
   "availableCredit": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Available Credit"
   },
   "partnerId": {
    "type": "string",
    "format": "uuid",
    "description": "Partner"
   },
   "partnerName": {
    "type": "string",
    "description": "Partner trading name"
   },
   "agreementId": {
    "type": "string",
    "format": "uuid",
    "description": "Agreement"
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date",
    "description": "Effective from"
   },
   "effectiveTo": {
    "type": "string",
    "format": "date",
    "description": "Effective to",
    "nullable": true
   },
   "temporaryLimitUntil": {
    "type": "string",
    "format": "date",
    "description": "Temporary limit ends (e.g. until 31 December)",
    "nullable": true
   },
   "blockThresholdPercent": {
    "type": "number",
    "description": "Threshold: block at this utilisation percent, default 100 (decided 29 September, readiness close-out)"
   },
   "openInvoices": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Open Invoices"
   },
   "utilizationPercent": {
    "type": "number",
    "description": "Credit Utilization, percent"
   },
   "creditStatus": {
    "type": "string",
    "description": "Credit status: notEnabled, withinLimit, warning, highRisk, onHold, blocked"
   },
   "aiInsights": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Advisory AI credit-pressure forecast"
   }
  }
 },
 "DepositGuaranteeFinancialSecurityManagementView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over control.partner_security (PartnerSecurity) and the existing subscription state, assembled at read time (data model DM4)",
  "description": "**What Deposit, Guarantee & Financial Security Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "securityId": {
    "type": "string",
    "description": "Security ID"
   },
   "partnerId": {
    "type": "string",
    "format": "uuid",
    "description": "Partner"
   },
   "agreementId": {
    "type": "string",
    "format": "uuid",
    "description": "Agreement"
   },
   "securityType": {
    "type": "string",
    "enum": [
     "cashDeposit",
     "bankGuarantee",
     "securityDeposit",
     "letterOfCredit",
     "prepaymentBalance",
     "corporateGuarantee",
     "other"
    ],
    "description": "Security type"
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Amount"
   },
   "currency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
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
    "format": "date",
    "description": "Effective Date"
   },
   "expiryDate": {
    "type": "string",
    "format": "date",
    "description": "Expiry Date",
    "nullable": true
   },
   "documentId": {
    "type": "string",
    "description": "Supporting document id",
    "nullable": true
   },
   "verificationStatus": {
    "type": "string",
    "description": "Verification Status: pending, verified, rejected or expired"
   },
   "creditExposure": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Coverage: partner credit exposure"
   },
   "securityCoverage": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Coverage: verified security held for the partner"
   },
   "unsecuredExposure": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Coverage: exposure not covered by verified security"
   },
   "daysToExpiry": {
    "type": "integer",
    "description": "Days until expiry",
    "nullable": true
   },
   "expiryAction": {
    "type": "string",
    "enum": [
     "generateWarning",
     "reduceCredit",
     "blockNewCreditSales",
     "placePartnerOnHold",
     "requireFinanceReview"
    ],
    "description": "Rules: what expiry of this security does"
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
 "PartnerAgreementStatus": {
  "type": "string",
  "enum": [
   "pendingApproval",
   "active",
   "expiringSoon",
   "expired",
   "suspended",
   "terminated"
  ]
 },
 "PartnerAllocation": {
  "type": "object",
  "x-ticvai-persistence": "control.partner_allocation",
  "description": "A contractual allocation under an agreement: the event or product, the quantity or percent of capacity, the commitment and the release rule. Booked, sold and remaining are counted from orders against it, not stored (decided 29 September, data model DM4)\n\n**Written by** setPartnerAllocations, which replaces the agreement's allocations as a set; a new or increased guaranteed allocation goes through approvals.request. The corporate allocations once held on `PartnerAgreement.corporateAllocations` are rows here, with `perMemberLimit` (decided 29 September, writers pass; DM4).",
  "required": [
   "id",
   "partnerId",
   "agreementId",
   "allocationModel",
   "releaseMode"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "partnerId": {
    "type": "string",
    "format": "uuid",
    "description": "The partner (control.partner)."
   },
   "agreementId": {
    "type": "string",
    "format": "uuid",
    "description": "The agreement (control.partner_agreement) this row belongs to."
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Venue."
   },
   "eventId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Event (catalogue.event)."
   },
   "productId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Product (catalogue.product)."
   },
   "ticketType": {
    "type": "string",
    "nullable": true,
    "description": "Ticket type."
   },
   "allocationModel": {
    "type": "string",
    "enum": [
     "guaranteed",
     "onRequest",
     "shared",
     "fixedQuantity",
     "percentage",
     "rolling",
     "seasonal"
    ],
    "description": "Allocation model (pack p.35)."
   },
   "quantity": {
    "type": "integer",
    "minimum": 0,
    "nullable": true,
    "description": "Contractual allocation quantity."
   },
   "allocationPercent": {
    "type": "number",
    "minimum": 0,
    "maximum": 100,
    "nullable": true,
    "description": "Percent of capacity, for the percentage model."
   },
   "minimumCommitment": {
    "type": "integer",
    "minimum": 0,
    "nullable": true,
    "description": "Minimum commitment, units."
   },
   "maximumAllocation": {
    "type": "integer",
    "minimum": 0,
    "nullable": true,
    "description": "Maximum allocation, units."
   },
   "commitmentRule": {
    "type": "string",
    "enum": [
     "useItOrRelease",
     "takeOrPay",
     "guaranteedMinimum"
    ],
    "nullable": true,
    "description": "Commitment rule."
   },
   "sellThroughTarget": {
    "type": "number",
    "minimum": 0,
    "maximum": 100,
    "nullable": true,
    "description": "Sell-through target, percent."
   },
   "returnRule": {
    "type": "string",
    "nullable": true,
    "description": "Return rule."
   },
   "releaseMode": {
    "type": "string",
    "enum": [
     "automatic",
     "manual"
    ],
    "description": "Release: automatic or manual."
   },
   "releaseHoursBeforeEvent": {
    "type": "integer",
    "minimum": 0,
    "nullable": true,
    "description": "Release deadline before the event (e.g. 48 hours)."
   },
   "releaseDate": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "Release at a fixed time instead."
   },
   "perMemberLimit": {
    "type": "integer",
    "minimum": 1,
    "nullable": true,
    "description": "For a corporate allocation: places one member (employee) may take from it; empty for no per-member limit. Carried over from the retired `PartnerAgreement.corporateAllocations` (decided 29 September, writers pass; DM4)"
   },
   "approvalRequestId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "The approvals.request raised for this row when it was created or changed; the row is not in force until that request is approved, as a PartnerRate is not (decided 29 September, writers pass; DM4)"
   },
   "scopePath": {
    "type": "string",
    "description": "The partition key (ADR-0005), written at `tenant` scope."
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
 "PartnerApprovalRoutedResult": {
  "type": "object",
  "x-ticvai-persistence": "none — response only (decided 29 September, writers pass; DM4)",
  "description": "The answer of a partner set operation whose change is money and goes through approvals (setPartnerCommissionRules, setPartnerCreditProfile, setPartnerAllocations), shaped like the approvePartnerStatuLifecycle response (decided 29 September, writers pass; DM4)",
  "required": [
   "applied"
  ],
  "properties": {
   "applied": {
    "type": "boolean",
    "description": "True when the change is in force now; false when it awaits the approval below"
   },
   "approvalRequestId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The approvals.request raised; empty when none was needed"
   },
   "items": {
    "type": "array",
    "description": "The rows as saved (PartnerCommissionRule, PartnerCreditProfile or PartnerAllocation)",
    "items": {
     "oneOf": [
      {
       "$ref": "#/components/schemas/PartnerCommissionRule"
      },
      {
       "$ref": "#/components/schemas/PartnerCreditProfile"
      },
      {
       "$ref": "#/components/schemas/PartnerAllocation"
      }
     ]
    }
   }
  }
 },
 "PartnerCommissionRule": {
  "type": "object",
  "x-ticvai-persistence": "control.partner_commission_rule + control.partner_commission_rule_tier",
  "description": "One commission or incentive rule under an agreement: the model, the product, venue, event, market and channel it applies to, the percent, amount or tiers, and the dates. The agreement's own `commissionPercent` is the default these rules refine (decided 29 September, data model DM4)\n\n**Written by** setPartnerCommissionRules; a new or changed rule goes through approvals.request and is not in force until approved, as a partner rate below its guardrails is not (decided 29 September, writers pass; DM4).",
  "required": [
   "id",
   "partnerId",
   "agreementId",
   "commissionModel",
   "effectiveFrom"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "partnerId": {
    "type": "string",
    "format": "uuid",
    "description": "The partner (control.partner)."
   },
   "agreementId": {
    "type": "string",
    "format": "uuid",
    "description": "The agreement (control.partner_agreement) this row belongs to."
   },
   "commissionModel": {
    "type": "string",
    "enum": [
     "fixedPercentage",
     "fixedAmount",
     "productSpecific",
     "tiered",
     "volumeBased",
     "revenueBased",
     "performanceIncentive",
     "campaignIncentive"
    ],
    "description": "Commission model (pack p.29)."
   },
   "productId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Product (catalogue.product)."
   },
   "productCategory": {
    "type": "string",
    "nullable": true,
    "description": "Product category."
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Venue."
   },
   "eventId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Event (catalogue.event)."
   },
   "market": {
    "type": "string",
    "nullable": true,
    "description": "Market."
   },
   "salesChannel": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/SalesChannel"
     }
    ],
    "nullable": true,
    "description": "Sales channel; blank = all."
   },
   "commissionPercent": {
    "type": "number",
    "minimum": 0,
    "maximum": 100,
    "nullable": true,
    "description": "Commission percent, for percentage models."
   },
   "commissionAmount": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "Fixed commission per ticket, for fixedAmount."
   },
   "tiers": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "fromUnits",
      "commissionPercent"
     ],
     "properties": {
      "fromUnits": {
       "type": "integer",
       "minimum": 0
      },
      "commissionPercent": {
       "type": "number",
       "minimum": 0,
       "maximum": 100
      }
     }
    },
    "description": "Tiers for tiered/volume/revenue models, e.g. 0-1,000 tickets 8%, 1,001-5,000 10%, 5,001+ 12%. The rows of control.partner_commission_rule_tier."
   },
   "volumeWindow": {
    "type": "string",
    "enum": [
     "calendarMonth",
     "calendarQuarter",
     "calendarYear",
     "agreementYear",
     "rolling12Months"
    ],
    "nullable": true,
    "description": "Period over which volume is counted, as on PartnerAgreement."
   },
   "incentiveType": {
    "type": "string",
    "enum": [
     "volumeBonus",
     "growthBonus",
     "targetAchievement",
     "seasonalIncentive",
     "newProductIncentive",
     "strategicPartnerBonus"
    ],
    "nullable": true,
    "description": "Incentive type."
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date",
    "description": "Effective from."
   },
   "effectiveTo": {
    "type": "string",
    "format": "date",
    "nullable": true,
    "description": "Effective to."
   },
   "approvalRequestId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "The approvals.request raised for this row when it was created or changed; the row is not in force until that request is approved, as a PartnerRate is not (decided 29 September, writers pass; DM4)"
   },
   "scopePath": {
    "type": "string",
    "description": "The partition key (ADR-0005), written at `tenant` scope."
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
 "PartnerCreditProfile": {
  "type": "object",
  "x-ticvai-persistence": "control.partner_credit_profile",
  "description": "The credit controls around an agreement's approved limit: thresholds, a temporary limit and its end, the owner, the risk class and the credit status. The approved limit itself stays `PartnerAgreement.creditLimit`; this row is how it is watched (decided 29 September, data model DM4)\n\n**Written by** setPartnerCreditProfile; enabling credit, a temporary limit and loosened thresholds go through approvals.request, a manual hold applies at once (decided 29 September, writers pass; DM4).",
  "required": [
   "id",
   "partnerId",
   "agreementId",
   "creditEnabled",
   "creditStatus"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "partnerId": {
    "type": "string",
    "format": "uuid",
    "description": "The partner (control.partner)."
   },
   "agreementId": {
    "type": "string",
    "format": "uuid",
    "description": "The agreement (control.partner_agreement) this row belongs to."
   },
   "creditEnabled": {
    "type": "boolean",
    "default": false,
    "description": "Credit enabled."
   },
   "temporaryCreditLimit": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "Temporary credit limit; empty when none."
   },
   "temporaryLimitUntil": {
    "type": "string",
    "format": "date",
    "nullable": true,
    "description": "Temporary limit ends (e.g. until 31 December)."
   },
   "creditOwnerPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Credit owner, a staff principal."
   },
   "approvalAuthority": {
    "type": "string",
    "nullable": true,
    "description": "Approval authority."
   },
   "riskClassification": {
    "type": "string",
    "enum": [
     "low",
     "medium",
     "high",
     "critical"
    ],
    "nullable": true,
    "description": "Risk classification."
   },
   "warningThresholdPercent": {
    "type": "number",
    "minimum": 0,
    "maximum": 100,
    "default": 70,
    "description": "Warning at this utilisation percent (decided 29 September, readiness close-out)."
   },
   "highRiskThresholdPercent": {
    "type": "number",
    "minimum": 0,
    "maximum": 100,
    "default": 90,
    "description": "High risk at this utilisation percent (decided 29 September, readiness close-out)."
   },
   "blockThresholdPercent": {
    "type": "number",
    "minimum": 0,
    "default": 100,
    "description": "Block at this utilisation percent (decided 29 September, readiness close-out)."
   },
   "creditStatus": {
    "type": "string",
    "enum": [
     "notEnabled",
     "withinLimit",
     "warning",
     "highRisk",
     "onHold",
     "blocked"
    ],
    "default": "notEnabled",
    "description": "Credit status. withinLimit, warning and highRisk are recomputed from utilisation against the thresholds; onHold and blocked are set by finance and stay until lifted."
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date",
    "description": "Effective from."
   },
   "effectiveTo": {
    "type": "string",
    "format": "date",
    "nullable": true,
    "description": "Effective to."
   },
   "approvalRequestId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "The approvals.request raised when credit was enabled, a temporary limit set or a threshold loosened; those changes are not in force until it is approved (decided 29 September, writers pass; DM4)"
   },
   "scopePath": {
    "type": "string",
    "description": "The partition key (ADR-0005), written at `tenant` scope."
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
 "PartnerRateMode": {
  "type": "string",
  "description": "**Alternatives, not both.** A partner buys at a net rate and keeps the margin, or sells at face value and is paid commission. Both is being paid twice for the same sale.\n",
  "enum": [
   "netRate",
   "commission"
  ]
 },
 "PartnerRateNetPricingConfigurationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; stored as control.partner_rate + control.partner_rate_volume_band (PartnerRate); rateId is its id (data model DM4)",
  "description": "**What Partner Rate & Net Pricing Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "partnerId": {
    "type": "string",
    "format": "uuid",
    "description": "Partner"
   },
   "agreementId": {
    "type": "string",
    "format": "uuid",
    "description": "Agreement"
   },
   "product": {
    "type": "string",
    "description": "Product id; blank = all in the family/venue",
    "nullable": true
   },
   "productFamily": {
    "type": "string",
    "description": "Product Family",
    "nullable": true
   },
   "venue": {
    "type": "string",
    "description": "Venue id; rates may differ per venue (MoM 31 Aug 4.3)",
    "nullable": true
   },
   "event": {
    "type": "string",
    "description": "Event id",
    "nullable": true
   },
   "ticketType": {
    "type": "string",
    "description": "Ticket Type",
    "nullable": true
   },
   "priceCategory": {
    "type": "string",
    "description": "Price Category",
    "nullable": true
   },
   "market": {
    "type": "string",
    "description": "Market",
    "nullable": true
   },
   "channel": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/SalesChannel"
     }
    ],
    "nullable": true,
    "description": "Channel"
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date",
    "description": "Effective From"
   },
   "effectiveTo": {
    "type": "string",
    "format": "date",
    "description": "Effective To",
    "nullable": true
   },
   "blackoutDates": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "date"
    },
    "description": "Blackout Dates"
   },
   "eventExceptions": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Event Exceptions: event ids this rate does not apply to"
   },
   "seasonalRate": {
    "type": "boolean",
    "description": "Seasonal Rate: this row overrides the base rate within its dates"
   },
   "minimumPermittedRate": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Guardrail: minimum permitted rate"
   },
   "maxDiscountPercent": {
    "type": "number",
    "description": "Guardrail: maximum discount from retail, percent",
    "nullable": true
   },
   "marginFloor": {
    "type": "number",
    "description": "Guardrail: margin floor, percent",
    "nullable": true
   },
   "manualOverrideAllowed": {
    "type": "boolean",
    "description": "Guardrail: manual override permitted"
   },
   "approvalThreshold": {
    "type": "number",
    "description": "Guardrail: discount percent above which the rate needs approval (pack p.37: discount > 15% requires approval)",
    "nullable": true
   },
   "rateId": {
    "type": "string",
    "format": "uuid",
    "description": "Rate id; omit to create"
   },
   "pricingModel": {
    "type": "string",
    "enum": [
     "retailPrice",
     "netRate",
     "discountFromRetail",
     "markup",
     "derivedRate"
    ],
    "description": "Pricing Model: retail price, net rate, discount from retail, markup or derived from a pricing profile"
   },
   "netRate": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Partner net rate, for netRate"
   },
   "discountPercent": {
    "type": "number",
    "description": "Discount from retail, percent, for discountFromRetail",
    "nullable": true
   },
   "maxMarkupPercent": {
    "type": "number",
    "description": "Permitted markup, percent, for markup",
    "nullable": true
   },
   "pricingProfileId": {
    "type": "string",
    "description": "Approved pricing profile, for derivedRate",
    "nullable": true
   },
   "volumeBands": {
    "type": "array",
    "description": "Tiered volume bands (MoM 31 Aug 4.4, MoM 1 Sep 4.3: e.g. 10% up to 1,000 tickets, 15% from 1,000-5,000); fromUnits as on PartnerAgreement.volumeTiers",
    "items": {
     "type": "object",
     "properties": {
      "fromUnits": {
       "type": "integer"
      },
      "discountPercent": {
       "type": "number"
      }
     }
    }
   }
  }
 },
 "PartnerRateNetPricingConfigurationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over control.partner_rate (PartnerRate) and the existing subscription state, assembled at read time (data model DM4)",
  "description": "**What Partner Rate & Net Pricing Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "partnerId": {
    "type": "string",
    "format": "uuid",
    "description": "Partner"
   },
   "agreementId": {
    "type": "string",
    "format": "uuid",
    "description": "Agreement"
   },
   "product": {
    "type": "string",
    "description": "Product id; blank = all in the family/venue",
    "nullable": true
   },
   "productFamily": {
    "type": "string",
    "description": "Product Family",
    "nullable": true
   },
   "venue": {
    "type": "string",
    "description": "Venue id; rates may differ per venue (MoM 31 Aug 4.3)",
    "nullable": true
   },
   "event": {
    "type": "string",
    "description": "Event id",
    "nullable": true
   },
   "ticketType": {
    "type": "string",
    "description": "Ticket Type",
    "nullable": true
   },
   "priceCategory": {
    "type": "string",
    "description": "Price Category",
    "nullable": true
   },
   "market": {
    "type": "string",
    "description": "Market",
    "nullable": true
   },
   "channel": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/SalesChannel"
     }
    ],
    "nullable": true,
    "description": "Channel"
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date",
    "description": "Effective From"
   },
   "effectiveTo": {
    "type": "string",
    "format": "date",
    "description": "Effective To",
    "nullable": true
   },
   "blackoutDates": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "date"
    },
    "description": "Blackout Dates"
   },
   "eventExceptions": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Event Exceptions: event ids this rate does not apply to"
   },
   "seasonalRate": {
    "type": "boolean",
    "description": "Seasonal Rate: this row overrides the base rate within its dates"
   },
   "minimumPermittedRate": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Guardrail: minimum permitted rate"
   },
   "maxDiscountPercent": {
    "type": "number",
    "description": "Guardrail: maximum discount from retail, percent",
    "nullable": true
   },
   "marginFloor": {
    "type": "number",
    "description": "Guardrail: margin floor, percent",
    "nullable": true
   },
   "manualOverrideAllowed": {
    "type": "boolean",
    "description": "Guardrail: manual override permitted"
   },
   "approvalThreshold": {
    "type": "number",
    "description": "Guardrail: discount percent above which the rate needs approval (pack p.37: discount > 15% requires approval)",
    "nullable": true
   },
   "rateId": {
    "type": "string",
    "format": "uuid",
    "description": "Rate id; omit to create"
   },
   "pricingModel": {
    "type": "string",
    "enum": [
     "retailPrice",
     "netRate",
     "discountFromRetail",
     "markup",
     "derivedRate"
    ],
    "description": "Pricing Model: retail price, net rate, discount from retail, markup or derived from a pricing profile"
   },
   "netRate": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Partner net rate, for netRate"
   },
   "discountPercent": {
    "type": "number",
    "description": "Discount from retail, percent, for discountFromRetail",
    "nullable": true
   },
   "maxMarkupPercent": {
    "type": "number",
    "description": "Permitted markup, percent, for markup",
    "nullable": true
   },
   "pricingProfileId": {
    "type": "string",
    "description": "Approved pricing profile, for derivedRate",
    "nullable": true
   },
   "volumeBands": {
    "type": "array",
    "description": "Tiered volume bands (MoM 31 Aug 4.4, MoM 1 Sep 4.3: e.g. 10% up to 1,000 tickets, 15% from 1,000-5,000); fromUnits as on PartnerAgreement.volumeTiers",
    "items": {
     "type": "object",
     "properties": {
      "fromUnits": {
       "type": "integer"
      },
      "discountPercent": {
       "type": "number"
      }
     }
    }
   },
   "publicRate": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Public rate from the price list, read-only, for comparison"
   },
   "rateHierarchyLevel": {
    "type": "string",
    "enum": [
     "standardPrice",
     "partnerTypeRate",
     "partnerAgreementRate",
     "productEventException"
    ],
    "description": "Rate Hierarchy level of this row"
   },
   "validationIssues": {
    "type": "array",
    "description": "Guardrail breaches and overlaps",
    "items": {
     "type": "object",
     "properties": {
      "code": {
       "type": "string",
       "enum": [
        "belowMinimumRate",
        "discountAboveMaximum",
        "marginBelowFloor",
        "overlappingRate"
       ]
      },
      "message": {
       "type": "string"
      }
     }
    }
   },
   "aiInsights": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Advisory AI margin-erosion or inconsistent-rate flags"
   }
  }
 },
 "PartnerSecurity": {
  "type": "object",
  "x-ticvai-persistence": "control.partner_security",
  "description": "A deposit, guarantee or other financial security a partner has lodged, with its verification and what its expiry does. Verified, unexpired security is what covers credit exposure (decided 29 September, data model DM4)\n\n**Written by** setPartnerSecurity (record a security, then verify or reject it); only a `verified`, unexpired row counts against exposure (decided 29 September, writers pass; DM4).",
  "required": [
   "id",
   "partnerId",
   "securityType",
   "amount",
   "currency",
   "effectiveDate",
   "verificationStatus"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "partnerId": {
    "type": "string",
    "format": "uuid",
    "description": "The partner (control.partner)."
   },
   "agreementId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The agreement (control.partner_agreement) this row belongs to; empty when it applies to the partner as a whole."
   },
   "securityType": {
    "type": "string",
    "enum": [
     "cashDeposit",
     "bankGuarantee",
     "securityDeposit",
     "letterOfCredit",
     "prepaymentBalance",
     "corporateGuarantee",
     "other"
    ],
    "description": "Security type."
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Amount, in `currency`."
   },
   "currency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "description": "Currency of the security, ISO 4217; a guarantee is issued in its own currency, not necessarily the settlement one."
   },
   "issuingInstitution": {
    "type": "string",
    "nullable": true,
    "description": "Issuing institution."
   },
   "reference": {
    "type": "string",
    "nullable": true,
    "description": "Reference."
   },
   "effectiveDate": {
    "type": "string",
    "format": "date",
    "description": "Effective date."
   },
   "expiryDate": {
    "type": "string",
    "format": "date",
    "nullable": true,
    "description": "Expiry date."
   },
   "documentId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Supporting document (control.partner_document)."
   },
   "verificationStatus": {
    "type": "string",
    "enum": [
     "pending",
     "verified",
     "rejected",
     "expired"
    ],
    "default": "pending",
    "description": "Verification status."
   },
   "expiryAction": {
    "type": "string",
    "enum": [
     "generateWarning",
     "reduceCredit",
     "blockNewCreditSales",
     "placePartnerOnHold",
     "requireFinanceReview"
    ],
    "nullable": true,
    "description": "What expiry of this security does."
   },
   "scopePath": {
    "type": "string",
    "description": "The partition key (ADR-0005), written at `tenant` scope."
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
 "PaymentTermsBillingAccountConfigurationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; stored as control.partner_billing_profile (PartnerBillingProfile); paymentModel and creditTermDays are control.partner_agreement columns, billingCurrency is its settlementCurrency, billingEntity lands in billingEntityName, the partner's own billing entity as text, not a ledger.legal_entity reference (decided 29 September, writers pass; DM4)",
  "description": "**What Payment Terms, Billing & Account Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "consolidatedBilling": {
    "type": "boolean",
    "description": "Consolidated Billing: one invoice across the partner's branches"
   },
   "billingEntity": {
    "type": "string",
    "description": "Billing Entity: the partner's own legal entity invoiced, as text; stored as PartnerBillingProfile.billingEntityName, not a ledger.legal_entity reference (decided 29 September, writers pass; DM4)"
   },
   "billingCurrency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "description": "Billing Currency; equals the agreement settlementCurrency"
   },
   "invoiceFrequency": {
    "type": "string",
    "enum": [
     "perTransaction",
     "weekly",
     "monthly"
    ],
    "description": "Invoice Frequency"
   },
   "invoiceGrouping": {
    "type": "string",
    "enum": [
     "perPartner",
     "perBranch",
     "perVenue",
     "perEvent",
     "perPurchaseOrder"
    ],
    "description": "Invoice Grouping (decided 29 September, readiness close-out)"
   },
   "taxProfile": {
    "type": "string",
    "description": "Tax Profile id"
   },
   "purchaseOrderRequired": {
    "type": "boolean",
    "description": "Purchase Order Required"
   },
   "statementFrequency": {
    "type": "string",
    "enum": [
     "weekly",
     "monthly"
    ],
    "description": "Statement Frequency"
   },
   "billingContact": {
    "type": "string",
    "description": "Billing Contact (partner contact id)"
   },
   "financeEmail": {
    "type": "string",
    "description": "Finance Email",
    "format": "email"
   },
   "partnerId": {
    "type": "string",
    "format": "uuid",
    "description": "Partner"
   },
   "agreementId": {
    "type": "string",
    "format": "uuid",
    "description": "Agreement"
   },
   "paymentModel": {
    "type": "string",
    "enum": [
     "creditAccount",
     "prepaid",
     "payPerTransaction"
    ],
    "description": "Payment model, the three confirmed at MoM 5 Aug and MoM 31 Aug 4.4: creditAccount (sells to an approved credit ceiling, invoiced periodically), prepaid (pre-funded wallet drawn down per sale) or payPerTransaction (card at each sale)"
   },
   "creditTermDays": {
    "type": "integer",
    "description": "Payment Terms in days: 0 due immediately, 7, 15, 30, 45 or custom (as on PartnerAgreement)"
   },
   "allowedPaymentMethods": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "creditAccount",
      "bankTransfer",
      "cheque",
      "card",
      "paymentLink",
      "prepaidBalance",
      "other"
     ]
    },
    "description": "Payment Methods (cheque from MoM 31 Aug 4.4)"
   }
  }
 },
 "PaymentTermsBillingAccountConfigurationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over control.partner_billing_profile (PartnerBillingProfile) and the existing subscription state, assembled at read time (data model DM4)",
  "description": "**What Payment Terms, Billing & Account Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "consolidatedBilling": {
    "type": "boolean",
    "description": "Consolidated Billing: one invoice across the partner's branches"
   },
   "billingEntity": {
    "type": "string",
    "description": "Billing Entity: the partner's own legal entity invoiced, as text; stored as PartnerBillingProfile.billingEntityName, not a ledger.legal_entity reference (decided 29 September, writers pass; DM4)"
   },
   "billingCurrency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "description": "Billing Currency; equals the agreement settlementCurrency"
   },
   "invoiceFrequency": {
    "type": "string",
    "enum": [
     "perTransaction",
     "weekly",
     "monthly"
    ],
    "description": "Invoice Frequency"
   },
   "invoiceGrouping": {
    "type": "string",
    "enum": [
     "perPartner",
     "perBranch",
     "perVenue",
     "perEvent",
     "perPurchaseOrder"
    ],
    "description": "Invoice Grouping (decided 29 September, readiness close-out)"
   },
   "taxProfile": {
    "type": "string",
    "description": "Tax Profile id"
   },
   "purchaseOrderRequired": {
    "type": "boolean",
    "description": "Purchase Order Required"
   },
   "statementFrequency": {
    "type": "string",
    "enum": [
     "weekly",
     "monthly"
    ],
    "description": "Statement Frequency"
   },
   "billingContact": {
    "type": "string",
    "description": "Billing Contact (partner contact id)"
   },
   "financeEmail": {
    "type": "string",
    "description": "Finance Email",
    "format": "email"
   },
   "prepaidBalance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Prepaid wallet balance (payment model prepaid)"
   },
   "currentBalance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Current Balance"
   },
   "outstanding": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Outstanding"
   },
   "overdue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Overdue"
   },
   "availableCredit": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Available Credit"
   },
   "lastPayment": {
    "type": "string",
    "format": "date",
    "description": "Last Payment date",
    "nullable": true
   },
   "nextInvoice": {
    "type": "string",
    "format": "date",
    "description": "Next Invoice date",
    "nullable": true
   },
   "oldestOutstandingInvoice": {
    "type": "string",
    "format": "date",
    "description": "Due date of the Oldest Outstanding Invoice",
    "nullable": true
   },
   "partnerId": {
    "type": "string",
    "format": "uuid",
    "description": "Partner"
   },
   "agreementId": {
    "type": "string",
    "format": "uuid",
    "description": "Agreement"
   },
   "paymentModel": {
    "type": "string",
    "enum": [
     "creditAccount",
     "prepaid",
     "payPerTransaction"
    ],
    "description": "Payment model, the three confirmed at MoM 5 Aug and MoM 31 Aug 4.4: creditAccount (sells to an approved credit ceiling, invoiced periodically), prepaid (pre-funded wallet drawn down per sale) or payPerTransaction (card at each sale)"
   },
   "creditTermDays": {
    "type": "integer",
    "description": "Payment Terms in days: 0 due immediately, 7, 15, 30, 45 or custom (as on PartnerAgreement)"
   },
   "allowedPaymentMethods": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "creditAccount",
      "bankTransfer",
      "cheque",
      "card",
      "paymentLink",
      "prepaidBalance",
      "other"
     ]
    },
    "description": "Payment Methods (cheque from MoM 31 Aug 4.4)"
   },
   "applied": {
    "type": "boolean",
    "description": "False when the save changed `paymentModel` or `creditTermDays` and the agreement amendment awaits approval; the billing-profile fields are applied either way (decided 29 September, writers pass; DM4)"
   },
   "approvalRequestId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The approvals.request raised for the agreement amendment; empty when none was needed (decided 29 September, writers pass; DM4)"
   }
  }
 }
}
```
