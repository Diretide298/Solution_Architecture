# WS21 — B2B, Reseller & OTA Partner Management board 1

**10 screens · 10 operations · 13 schemas · 2 permissions**

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
| `PTR-022` | Partner Management Command Center | commandCentre | 1 | 0 | — |
| `PTR-023` | Partner Profile & Organization Setup | configEditor | 1 | 0 | — |
| `PTR-024` | Partner Onboarding & Application Workflow | configEditor | 1 | 0 | — |
| `PTR-025` | Partner Contacts & User Administration | configEditor | 1 | 0 | — |
| `PTR-026` | Territory, Market & Distribution Rights | configEditor | 1 | 0 | — |
| `PTR-027` | Partner Brand, Venue & Business Scope Assignment | listDetail | 1 | 0 | — |
| `PTR-028` | Partner Documentation & Compliance Repository | configEditor | 1 | 0 | — |
| `PTR-029` | Partner Access, Roles & Permission Profile | configEditor | 1 | 0 | — |
| `PTR-030` | Partner Approval, Status & Lifecycle Management | configEditor | 1 | 0 | — |
| `PTR-031` | Partner 360° Profile, Readiness & AI Review | listDetail | 1 | 0 | — |

## Thin screens in this batch

**PTR-027, PTR-031 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "PTR-022",
  "name": "Partner Management Command Center",
  "module": "Partners",
  "requiresModule": "partner",
  "wave": 3,
  "source": {
   "pack": "B2B, Reseller & OTA Partner Management_Reference.pdf",
   "board": "1",
   "number": "8.1.1",
   "page": 5
  },
  "implementation": {
   "app": "partner-web",
   "route": "/partners/partner-management-command-center-ptr-022",
   "component": "apps/partner-web/src/routes/partners/PartnerManagementCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "PTR-001"
   ],
   "exitTo": [
    "PTR-001",
    "PTR-023",
    "PTR-024",
    "PTR-025",
    "PTR-026",
    "PTR-027",
    "PTR-028",
    "PTR-029",
    "PTR-030",
    "PTR-031"
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
     "to": "PTR-023",
     "trigger": "Sets up the organisation record",
     "provenance": "flow F110 step 4→5",
     "operation": "listPartner"
    },
    {
     "to": "PTR-024",
     "trigger": "Reads the application the applicant submitted",
     "provenance": "flow F110 step 2→3",
     "operation": "listPartner"
    },
    {
     "to": "PTR-025",
     "trigger": "Creates the partner's first user",
     "provenance": "flow F110 step 12→13",
     "operation": "listPartner"
    },
    {
     "to": "PTR-027",
     "trigger": "Assigns the brands, venues and business scope the partner may sell",
     "provenance": "flow F110 step 6→7",
     "operation": "listPartner"
    },
    {
     "to": "PTR-028",
     "trigger": "Checks the compliance and documentation file",
     "provenance": "flow F110 step 8→9",
     "operation": "listPartner"
    },
    {
     "to": "PTR-029",
     "trigger": "Chooses the permission profile the partner's own users will inherit",
     "provenance": "flow F110 step 10→11",
     "operation": "listPartner"
    },
    {
     "to": "PTR-030",
     "trigger": "Approves the partner and moves it to active",
     "provenance": "flow F110 step 14→15",
     "operation": "listPartner"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each partner record should display) — counts over a population, then the population",
  "purpose": "Provide a centralized management dashboard for all B2B, reseller, OTA and distribution partners across the TICVAI ecosystem.",
  "purposeNote": "Authorized administrators can identify every partner, its business relationship, current status and outstanding actions from a single workspace.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search partner",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 5 §Filter by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "PartnerManagementCommandCenterView.partnerType",
        "PartnerManagementCommandCenterView.country",
        "PartnerManagementCommandCenterView.territory",
        "Brand",
        "Venue",
        "Account Manager",
        "Status",
        "PartnerManagementCommandCenterView.agreementStatus",
        "PartnerManagementCommandCenterView.creditStatus",
        "Integration Type",
        "Risk"
       ],
       "notes": "The pack filters this screen by partner type, country, territory, brand, venue, account manager and 5 more — which are present is a decision the pack already made.",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 5 §Filter by"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Total Partners",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 5 §Display",
       "bindsTo": "PartnerManagementCommandCenterView.totalPartners"
      },
      {
       "kind": "metricTile",
       "label": "Active Partners",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 5 §Display",
       "bindsTo": "PartnerManagementCommandCenterView.activePartners"
      },
      {
       "kind": "metricTile",
       "label": "Pending Onboarding",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 5 §Display",
       "bindsTo": "PartnerManagementCommandCenterView.pendingOnboarding"
      },
      {
       "kind": "metricTile",
       "label": "Pending Approval",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 5 §Display",
       "bindsTo": "PartnerManagementCommandCenterView.pendingApproval"
      },
      {
       "kind": "metricTile",
       "label": "Suspended Partners",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 5 §Display",
       "bindsTo": "PartnerManagementCommandCenterView.suspendedPartners"
      },
      {
       "kind": "metricTile",
       "label": "Expiring Agreements",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 5 §Display",
       "bindsTo": "PartnerManagementCommandCenterView.expiringAgreements"
      },
      {
       "kind": "metricTile",
       "label": "Documentation Issues",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 5 §Display",
       "bindsTo": "PartnerManagementCommandCenterView.documentationIssues"
      },
      {
       "kind": "metricTile",
       "label": "Partners With Credit Holds",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 5 §Display",
       "bindsTo": "PartnerManagementCommandCenterView.partnersWithCreditHolds"
      },
      {
       "kind": "metricTile",
       "label": "Connected OTA/API Partners",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 5 §Display",
       "bindsTo": "PartnerManagementCommandCenterView.connectedOtaApiPartners"
      },
      {
       "kind": "metricTile",
       "label": "Partner Sales YTD",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 5 §Display",
       "bindsTo": "PartnerManagementCommandCenterView.partnerSalesYtd"
      },
      {
       "kind": "metricTile",
       "label": "Partner Revenue YTD",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 5 §Display",
       "bindsTo": "PartnerManagementCommandCenterView.partnerRevenueYtd"
      },
      {
       "kind": "metricTile",
       "label": "High-Risk Partners",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 5 §Display",
       "bindsTo": "PartnerManagementCommandCenterView.highRiskPartners"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every partner",
       "columns": [
        "PartnerManagementCommandCenterView.partnerId",
        "PartnerManagementCommandCenterView.tradingName",
        "PartnerManagementCommandCenterView.legalEntity",
        "PartnerManagementCommandCenterView.partnerType",
        "PartnerManagementCommandCenterView.country",
        "PartnerManagementCommandCenterView.territory",
        "Assigned Brand/Venue",
        "PartnerManagementCommandCenterView.commercialOwner",
        "PartnerManagementCommandCenterView.distributionChannel",
        "PartnerManagementCommandCenterView.accountStatus",
        "PartnerManagementCommandCenterView.onboardingStatus",
        "PartnerManagementCommandCenterView.agreementStatus",
        "PartnerManagementCommandCenterView.creditStatus",
        "PartnerManagementCommandCenterView.integrationStatus",
        "PartnerManagementCommandCenterView.lastActivity"
       ],
       "bindsTo": "PartnerManagementCommandCenterView",
       "operation": "listPartner",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 5 §Each partner record should display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected partner",
       "bindsTo": "PartnerManagementCommandCenterView",
       "columns": [
        "PartnerManagementCommandCenterView.partnerId",
        "PartnerManagementCommandCenterView.tradingName",
        "PartnerManagementCommandCenterView.legalEntity",
        "PartnerManagementCommandCenterView.partnerType",
        "PartnerManagementCommandCenterView.country",
        "PartnerManagementCommandCenterView.territory",
        "Assigned Brand/Venue",
        "PartnerManagementCommandCenterView.commercialOwner",
        "PartnerManagementCommandCenterView.distributionChannel",
        "PartnerManagementCommandCenterView.accountStatus",
        "PartnerManagementCommandCenterView.onboardingStatus",
        "PartnerManagementCommandCenterView.agreementStatus",
        "PartnerManagementCommandCenterView.creditStatus",
        "PartnerManagementCommandCenterView.integrationStatus",
        "PartnerManagementCommandCenterView.lastActivity"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Partner Attention Required”.",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 5 §Each partner record should display"
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
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** Create Partner, Review Application, Approve, Assign Account Manager, Suspend, Open Commercial Profile, View Users, View Documents, View Performance. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 5 §Authorized users can"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The partner list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the partner untouched.",
   "emptyFirstRun": "No partner yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the partner are still there. The pack's own statuses are Suspended → Terminated → Archived — the state names which is selected.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPartner",
    "contract": "subscription",
    "purpose": "Partner Management Command Center",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-022"
  },
  "apisNote": "Regenerated 9 September 2026 from B2B, Reseller & OTA Partner Management_Reference.pdf page 5. 31 of 38 labels bound to a contract property; 48 of 55 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "PTR-023",
  "name": "Partner Profile & Organization Setup",
  "module": "Partners",
  "requiresModule": "partner",
  "wave": 3,
  "source": {
   "pack": "B2B, Reseller & OTA Partner Management_Reference.pdf",
   "board": "1",
   "number": "8.1.2",
   "page": 7
  },
  "implementation": {
   "app": "partner-web",
   "route": "/partners/partner-profile-organization-setup-ptr-023",
   "component": "apps/partner-web/src/routes/partners/PartnerProfileOrganizationSetup.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "PTR-022"
   ],
   "exitTo": [
    "PTR-022"
   ],
   "inferred": false,
   "notes": "**Reached from PTR-022, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "PTR-022",
     "trigger": "Returns to the command centre",
     "provenance": "flow F110 step 5→6",
     "operation": "setPartnerProfileOrganization"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population",
  "purpose": "Create the master business record for each external distribution partner.",
  "purposeNote": "Each external partner has one governed master organization record that can be referenced by commercial, operational, finance and distribution processes.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: New Partner. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 7 §Allow internal tags such as"
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
       "label": "Partner ID",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 7 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Legal Entity Name",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 7 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Trading Name",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 7 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Partner Type",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 7 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Registration Number",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 7 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Tax/VAT Number",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 7 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Country",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 7 §Capture"
      },
      {
       "kind": "selectField",
       "label": "City",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 7 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Registered Address",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 7 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Business Address",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 7 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Website",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 7 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Main Telephone",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 7 §Capture"
      },
      {
       "kind": "selectField",
       "label": "General Email",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 7 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Preferred Language",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 7 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Default Currency",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 7 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Time Zone",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 7 §Capture"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "New Partner",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 7 §Allow internal tags such as"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The partner profile organization configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the partner profile organization untouched.",
   "emptyFirstRun": "No partner profile organization configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setPartnerProfileOrganization",
    "contract": "subscription",
    "purpose": "Partner Profile & Organization Setup",
    "trigger": "onAction",
    "invalidates": [
     "setPartnerProfileOrganization"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-023"
  },
  "apisNote": "Regenerated 9 September 2026 from B2B, Reseller & OTA Partner Management_Reference.pdf page 7. 0 of 0 labels bound to a contract property; 17 of 53 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "PTR-024",
  "name": "Partner Onboarding & Application Workflow",
  "module": "Partners",
  "requiresModule": "partner",
  "wave": 3,
  "source": {
   "pack": "B2B, Reseller & OTA Partner Management_Reference.pdf",
   "board": "1",
   "number": "8.1.3",
   "page": 8
  },
  "implementation": {
   "app": "partner-web",
   "route": "/partners/partner-onboarding-application-workflow-ptr-024",
   "component": "apps/partner-web/src/routes/partners/PartnerOnboardingApplicationWorkflow.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "PTR-022"
   ],
   "exitTo": [
    "PTR-022"
   ],
   "inferred": false,
   "notes": "**Reached from PTR-022, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "PTR-022",
     "trigger": "Returns to the command centre",
     "provenance": "flow F110 step 3→4",
     "operation": "listPartnerOnboardingApplication"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population",
  "purpose": "Manage the complete journey from a new partner application through internal review and activation.",
  "purposeNote": "New partners cannot become commercially active until the configured onboarding and approval stages have been successfully completed.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 3 actions on this screen and the screen declares 1 operation.** Unserved: Sequential approval, Parallel approval, Request More Information. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 8 §Support"
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
       "label": "Company information",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 8 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Requested partner type",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 8 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Markets",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 8 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Expected sales volume",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 8 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Requested products",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 8 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Requested venues",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 8 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Preferred distribution method",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 8 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Estimated annual business",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 8 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Contact information",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 8 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Billing requirements",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 8 §Capture"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Sequential approval",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 8 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Parallel approval",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 8 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Request More Information",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 8 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The partner onboarding application configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the partner onboarding application untouched.",
   "emptyFirstRun": "No partner onboarding application configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPartnerOnboardingApplication",
    "contract": "subscription",
    "purpose": "Partner Onboarding & Application Workflow",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-024"
  },
  "apisNote": "Regenerated 9 September 2026 from B2B, Reseller & OTA Partner Management_Reference.pdf page 8. 0 of 0 labels bound to a contract property; 13 of 43 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "PTR-025",
  "name": "Partner Contacts & User Administration",
  "module": "Partners",
  "requiresModule": "partner",
  "wave": 3,
  "source": {
   "pack": "B2B, Reseller & OTA Partner Management_Reference.pdf",
   "board": "1",
   "number": "8.1.4",
   "page": 10
  },
  "implementation": {
   "app": "partner-web",
   "route": "/partners/partner-contacts-user-administration-ptr-025",
   "component": "apps/partner-web/src/routes/partners/PartnerContactsUserAdministration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "PTR-022"
   ],
   "exitTo": [
    "PTR-022"
   ],
   "inferred": false,
   "notes": "**Reached from PTR-022, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "PTR-022",
     "trigger": "Returns to the command centre",
     "provenance": "flow F110 step 13→14",
     "operation": "listPartnerContactUser"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture; Configure) and no display directory — it is settings, not a population",
  "purpose": "Manage the individuals authorized to interact with TICVAI on behalf of each partner.",
  "purposeNote": "Every external user accessing TICVAI on behalf of a partner is associated with a valid partner account and controlled through appropriate roles and permissions.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Password policy. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 10 §Support/reference"
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
       "label": "Name",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 10 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Position",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 10 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Department",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 10 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Email",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 10 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Mobile",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 10 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Telephone",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 10 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Language",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 10 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Time Zone",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 10 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Contact Type",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 10 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Status",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 10 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Username",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 10 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Partner",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 10 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Branch",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 10 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Role",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 10 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Permissions",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 10 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Sales Location",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 10 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Currency",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 10 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Password policy",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 10 §Support/reference"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The partner contacts user configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the partner contacts user untouched.",
   "emptyFirstRun": "No partner contacts user configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPartnerContactUser",
    "contract": "subscription",
    "purpose": "Partner Contacts & User Administration",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-025"
  },
  "apisNote": "Regenerated 9 September 2026 from B2B, Reseller & OTA Partner Management_Reference.pdf page 10. 0 of 0 labels bound to a contract property; 18 of 52 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "PTR-026",
  "name": "Territory, Market & Distribution Rights",
  "module": "Partners",
  "requiresModule": "partner",
  "wave": 3,
  "source": {
   "pack": "B2B, Reseller & OTA Partner Management_Reference.pdf",
   "board": "1",
   "number": "8.1.5",
   "page": 12
  },
  "implementation": {
   "app": "partner-web",
   "route": "/partners/territory-market-distribution-rights-ptr-026",
   "component": "apps/partner-web/src/routes/partners/TerritoryMarketDistributionRights.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "PTR-022"
   ],
   "exitTo": [
    "PTR-022"
   ],
   "inferred": false,
   "notes": "**Reached from PTR-022, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation."
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Define where and through what business scope a partner is authorized to distribute TICVAI products.",
  "purposeNote": "partner is authorized to use.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Sub-agents allowed",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 12 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Sub-agents prohibited",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 12 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Approval required",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 12 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Maximum hierarchy depth",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 12 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The territory market distribution configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the territory market distribution untouched.",
   "emptyFirstRun": "No territory market distribution configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listTerritoryMarketDistribution",
    "contract": "subscription",
    "purpose": "Territory, Market & Distribution Rights",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-026"
  },
  "apisNote": "Regenerated 9 September 2026 from B2B, Reseller & OTA Partner Management_Reference.pdf page 12. 0 of 0 labels bound to a contract property; 4 of 40 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "PTR-027",
  "name": "Partner Brand, Venue & Business Scope Assignment",
  "module": "Partners",
  "requiresModule": "partner",
  "wave": 3,
  "source": {
   "pack": "B2B, Reseller & OTA Partner Management_Reference.pdf",
   "board": "1",
   "number": "8.1.6",
   "page": 14
  },
  "implementation": {
   "app": "partner-web",
   "route": "/partners/partner-brand-venue-business-scope-assignment-ptr-027",
   "component": "apps/partner-web/src/routes/partners/PartnerBrandVenueBusinessScopeAssignment.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "PTR-022"
   ],
   "exitTo": [
    "PTR-022"
   ],
   "inferred": false,
   "notes": "**Reached from PTR-022, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "PTR-022",
     "trigger": "Returns to the command centre",
     "provenance": "flow F110 step 7→8",
     "operation": "setPartnerBrandVenue"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Determine which TICVAI business entities the partner relationship covers. This is deliberately separate from product assignment, which is governed through the Sales Channel and commercial configuration layers.",
  "purposeNote": "Every partner is associated only with the TICVAI brands, venues and business entities for which the commercial relationship has been approved.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 14"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 14"
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
       "provenance": "contract operation setPartnerBrandVenue"
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
       "impliedBy": "setPartnerBrandVenue"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The partner brand venue list.",
   "error": "Could not load. Names which read failed and leaves the partner brand venue untouched.",
   "emptyFirstRun": "No partner brand venue yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the partner brand venue are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setPartnerBrandVenue",
    "contract": "subscription",
    "purpose": "Partner Brand, Venue & Business Scope Assignment",
    "trigger": "onAction",
    "invalidates": [
     "setPartnerBrandVenue"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-027"
  },
  "apisNote": "Regenerated 9 September 2026 from B2B, Reseller & OTA Partner Management_Reference.pdf page 14. 0 of 0 labels bound to a contract property; 0 of 26 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "PTR-028",
  "name": "Partner Documentation & Compliance Repository",
  "module": "Partners",
  "requiresModule": "partner",
  "wave": 3,
  "source": {
   "pack": "B2B, Reseller & OTA Partner Management_Reference.pdf",
   "board": "1",
   "number": "8.1.7",
   "page": 15
  },
  "implementation": {
   "app": "partner-web",
   "route": "/partners/partner-documentation-compliance-repository-ptr-028",
   "component": "apps/partner-web/src/routes/partners/PartnerDocumentationComplianceRepository.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "PTR-022"
   ],
   "exitTo": [
    "PTR-022"
   ],
   "inferred": false,
   "notes": "**Reached from PTR-022, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "PTR-022",
     "trigger": "Returns to the command centre",
     "provenance": "flow F110 step 9→10",
     "operation": "listPartnerDocumentationCompliance"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture; Configure whether expiration should) and no display directory — it is settings, not a population",
  "purpose": "Maintain required partner documentation and ensure that commercial accounts remain compliant.",
  "purposeNote": "restrict commercial activity when mandatory documentation is missing or invalid.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Document Type",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 15 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Document Number",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 15 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Issue Date",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 15 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Expiry Date",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 15 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Issuing Authority",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 15 §Capture"
      },
      {
       "kind": "selectField",
       "label": "File",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 15 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Verification Status",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 15 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Verified By",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 15 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Verification Date",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 15 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Notes",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 15 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Warn only",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 15 §Configure whether expiration should"
      },
      {
       "kind": "selectField",
       "label": "Block new bookings",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 15 §Configure whether expiration should"
      },
      {
       "kind": "selectField",
       "label": "Block credit transactions",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 15 §Configure whether expiration should"
      },
      {
       "kind": "selectField",
       "label": "Suspend partner",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 15 §Configure whether expiration should"
      },
      {
       "kind": "selectField",
       "label": "Require manual review",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 15 §Configure whether expiration should"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The partner documentation compliance configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the partner documentation compliance untouched.",
   "emptyFirstRun": "No partner documentation compliance configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPartnerDocumentationCompliance",
    "contract": "subscription",
    "purpose": "Partner Documentation & Compliance Repository",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-028"
  },
  "apisNote": "Regenerated 9 September 2026 from B2B, Reseller & OTA Partner Management_Reference.pdf page 15. 0 of 0 labels bound to a contract property; 15 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "PTR-029",
  "name": "Partner Access, Roles & Permission Profile",
  "module": "Partners",
  "requiresModule": "partner",
  "wave": 3,
  "source": {
   "pack": "B2B, Reseller & OTA Partner Management_Reference.pdf",
   "board": "1",
   "number": "8.1.8",
   "page": 16
  },
  "implementation": {
   "app": "partner-web",
   "route": "/partners/partner-access-roles-permission-profile-ptr-029",
   "component": "apps/partner-web/src/routes/partners/PartnerAccessRolesPermissionProfile.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "PTR-022"
   ],
   "exitTo": [
    "PTR-022"
   ],
   "inferred": false,
   "notes": "**Reached from PTR-022, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "PTR-022",
     "trigger": "Returns to the command centre",
     "provenance": "flow F110 step 11→12",
     "operation": "listPartnerAccessRole"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure whether the partner may) and no display directory — it is settings, not a population",
  "purpose": "Control what a partner organization is permitted to do, beyond individual-user permissions.",
  "purposeNote": "Partner organizations can access only the capabilities authorized by TICVAI, regardless of permissions assigned to individual partner users.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Search Availability",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 16 §Configure whether the partner may"
      },
      {
       "kind": "selectField",
       "label": "Create Booking",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 16 §Configure whether the partner may"
      },
      {
       "kind": "selectField",
       "label": "Hold Inventory",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 16 §Configure whether the partner may"
      },
      {
       "kind": "selectField",
       "label": "Confirm Booking",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 16 §Configure whether the partner may"
      },
      {
       "kind": "selectField",
       "label": "Cancel Booking",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 16 §Configure whether the partner may"
      },
      {
       "kind": "selectField",
       "label": "Modify Booking",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 16 §Configure whether the partner may"
      },
      {
       "kind": "selectField",
       "label": "Download Ticket",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 16 §Configure whether the partner may"
      },
      {
       "kind": "selectField",
       "label": "Print Ticket",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 16 §Configure whether the partner may"
      },
      {
       "kind": "selectField",
       "label": "Send Ticket",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 16 §Configure whether the partner may"
      },
      {
       "kind": "selectField",
       "label": "Access Customer Details",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 16 §Configure whether the partner may"
      },
      {
       "kind": "selectField",
       "label": "Use Credit",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 16 §Configure whether the partner may"
      },
      {
       "kind": "selectField",
       "label": "Use Payment Card",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 16 §Configure whether the partner may"
      },
      {
       "kind": "selectField",
       "label": "View Commission",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 16 §Configure whether the partner may"
      },
      {
       "kind": "selectField",
       "label": "View Net Rates",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 16 §Configure whether the partner may"
      },
      {
       "kind": "selectField",
       "label": "Access Reports",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 16 §Configure whether the partner may"
      },
      {
       "kind": "selectField",
       "label": "Export Data",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 16 §Configure whether the partner may"
      },
      {
       "kind": "selectField",
       "label": "Use API",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 16 §Configure whether the partner may"
      },
      {
       "kind": "selectField",
       "label": "Create Sub-Agents",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 16 §Configure whether the partner may"
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
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** ↓, Permanent, Temporary, Seasonal, Event-specific. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 16 §Partner Permission Ceiling"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The partner access roles configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the partner access roles untouched.",
   "emptyFirstRun": "No partner access roles configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPartnerAccessRole",
    "contract": "subscription",
    "purpose": "Partner Access, Roles & Permission Profile",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-029"
  },
  "apisNote": "Regenerated 9 September 2026 from B2B, Reseller & OTA Partner Management_Reference.pdf page 16. 0 of 0 labels bound to a contract property; 23 of 34 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "PTR-030",
  "name": "Partner Approval, Status & Lifecycle Management",
  "module": "Partners",
  "requiresModule": "partner",
  "wave": 3,
  "source": {
   "pack": "B2B, Reseller & OTA Partner Management_Reference.pdf",
   "board": "1",
   "number": "8.1.9",
   "page": 18
  },
  "implementation": {
   "app": "partner-web",
   "route": "/partners/partner-approval-status-lifecycle-management-ptr-030",
   "component": "apps/partner-web/src/routes/partners/PartnerApprovalStatusLifecycleManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "PTR-022"
   ],
   "exitTo": [
    "PTR-022"
   ],
   "inferred": false,
   "notes": "**Reached from PTR-022, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation."
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population",
  "purpose": "Govern the complete business lifecycle of a partner after onboarding.",
  "purposeNote": "Partner lifecycle changes are governed, effective-dated, auditable and do not unintentionally damage valid existing customer transactions.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Commercial",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 18 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Compliance",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 18 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Credit",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 18 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Fraud",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 18 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Contract Expiry",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 18 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Performance",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 18 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Technical",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 18 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Management Decision",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 18 §Capture"
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
       "provenance": "contract operation approvePartnerStatuLifecycle",
       "permission": "Approve"
      },
      {
       "kind": "banner",
       "label": "Permissions this screen separates",
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** Activate, Restrict, Suspend, Reactivate, Terminate, Archive. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 18 §Authorized users can"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The partner approval status configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the partner approval status untouched.",
   "emptyFirstRun": "No partner approval status configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "approvePartnerStatuLifecycle",
    "contract": "subscription",
    "purpose": "Partner Approval, Status & Lifecycle Management",
    "trigger": "onAction",
    "invalidates": [
     "approvePartnerStatuLifecycle"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-030"
  },
  "apisNote": "Regenerated 9 September 2026 from B2B, Reseller & OTA Partner Management_Reference.pdf page 18. 0 of 0 labels bound to a contract property; 15 of 42 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "PTR-031",
  "name": "Partner 360° Profile, Readiness & AI Review",
  "module": "Partners",
  "requiresModule": "partner",
  "wave": 3,
  "source": {
   "pack": "B2B, Reseller & OTA Partner Management_Reference.pdf",
   "board": "1",
   "number": "8.1.10",
   "page": 19
  },
  "implementation": {
   "app": "partner-web",
   "route": "/partners/partner-360-profile-readiness-ai-review-ptr-031",
   "component": "apps/partner-web/src/routes/partners/Partner360ProfileReadinessAiReview.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "PTR-022"
   ],
   "exitTo": [
    "PTR-022"
   ],
   "inferred": false,
   "notes": "**Reached from PTR-022, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation."
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide one consolidated Partner 360 screen before activation and throughout the relationship. This should become one of the most useful screens for TICVAI commercial management. Board 1 established who the partner is and what they are authorized to access. Board 2 establishes the commercial rules under which that partner can transact with TICVAI.",
  "purposeNote": "Before activation, authorized management can evaluate the partner's complete organizational, compliance, access, commercial and technical readiness from one consolidated view. Board 1 — Final Screen Register Screen Backend Screen Primary Responsibility 8.1.1 Partner Management Command Center Partner portfolio & status Screen Backend Screen Primary Responsibility 8.1.2 Partner Profile & Organization Setup Master partner record 8.1.3 Partner Onboarding & Application Workflow Partner onboarding 8.1.4 Partner Contacts & User Administration Contacts and B2B users",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 19"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 19"
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
       "impliedBy": "listPartnerProfileReadiness",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The partner 360° profile list.",
   "error": "Could not load. Names which read failed and leaves the partner 360° profile untouched.",
   "emptyFirstRun": "No partner 360° profile yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the partner 360° profile are still there. The pack's own statuses are 8.1.9 Partner lifecycle governance — the state names which is selected.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPartnerProfileReadiness",
    "contract": "subscription",
    "purpose": "Partner 360° Profile, Readiness & AI Review",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "Partner360ProfileReadinessAiReviewView.companyInformationAndHierarchy",
    "Partner360ProfileReadinessAiReviewView.keyPartnerContacts",
    "Partner360ProfileReadinessAiReviewView.activeB2bUsers",
    "Partner360ProfileReadinessAiReviewView.authorizedMarkets",
    "Partner360ProfileReadinessAiReviewView.brandsAndVenues"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-031"
  },
  "apisNote": "Regenerated 9 September 2026 from B2B, Reseller & OTA Partner Management_Reference.pdf page 19. 0 of 0 labels bound to a contract property; 1 of 78 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "approvePartnerStatuLifecycle": {
  "method": "PUT",
  "path": "/partner-statu-lifecycle",
  "contract": "subscription",
  "summary": "Partner Approval, Status & Lifecycle Management",
  "permission": "PLATFORM_CELL_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": "PartnerApprovalStatusLifecycleManagementInput",
  "responds": "PartnerApprovalStatusLifecycleManagementView"
 },
 "listPartner": {
  "method": "GET",
  "path": "/partner",
  "contract": "subscription",
  "summary": "Partner Management Command Center",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
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
    "name": "accountManager",
    "in": "query",
    "required": false
   },
   {
    "name": "status",
    "in": "query",
    "required": false
   },
   {
    "name": "integrationType",
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
  "responds": "PartnerManagementCommandCenterView"
 },
 "listPartnerAccessRole": {
  "method": "GET",
  "path": "/partner-access-role",
  "contract": "subscription",
  "summary": "Partner Access, Roles & Permission Profile",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "PartnerAccessRolesPermissionProfileView"
 },
 "listPartnerContactUser": {
  "method": "GET",
  "path": "/partner-contact-user",
  "contract": "subscription",
  "summary": "Partner Contacts & User Administration",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "PartnerContactsUserAdministrationView"
 },
 "listPartnerDocumentationCompliance": {
  "method": "GET",
  "path": "/partner-documentation-compliance",
  "contract": "subscription",
  "summary": "Partner Documentation & Compliance Repository",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "PartnerDocumentationComplianceRepositoryView"
 },
 "listPartnerOnboardingApplication": {
  "method": "GET",
  "path": "/partner-onboarding-application",
  "contract": "subscription",
  "summary": "Partner Onboarding & Application Workflow",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "PartnerOnboardingApplicationWorkflowView"
 },
 "listPartnerProfileReadiness": {
  "method": "GET",
  "path": "/partner-profile-readiness",
  "contract": "subscription",
  "summary": "Partner 360° Profile, Readiness & AI Review",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "Partner360ProfileReadinessAiReviewView"
 },
 "listTerritoryMarketDistribution": {
  "method": "GET",
  "path": "/territory-market-distribution",
  "contract": "subscription",
  "summary": "Territory, Market & Distribution Rights",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "TerritoryMarketDistributionRightsView"
 },
 "setPartnerBrandVenue": {
  "method": "PUT",
  "path": "/partner-brand-venue",
  "contract": "subscription",
  "summary": "Partner Brand, Venue & Business Scope Assignment",
  "permission": "PLATFORM_CELL_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": "PartnerBrandVenueBusinessScopeAssignmentInput",
  "responds": "PartnerBrandVenueBusinessScopeAssignmentView"
 },
 "setPartnerProfileOrganization": {
  "method": "PUT",
  "path": "/partner-profile-organization",
  "contract": "subscription",
  "summary": "Partner Profile & Organization Setup",
  "permission": "PLATFORM_CELL_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": "PartnerProfileOrganizationSetupInput",
  "responds": "PartnerProfileOrganizationSetupView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "Partner360ProfileReadinessAiReviewView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Partner 360° Profile, Readiness & AI Review displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "companyInformationAndHierarchy": {
    "type": "string",
    "description": "Company information and hierarchy"
   },
   "keyPartnerContacts": {
    "type": "string",
    "description": "Key partner contacts"
   },
   "activeB2bUsers": {
    "type": "integer",
    "description": "Active B2B users"
   },
   "authorizedMarkets": {
    "type": "string",
    "description": "Authorized markets"
   },
   "brandsAndVenues": {
    "type": "string",
    "description": "Brands and venues"
   },
   "complianceStatus": {
    "type": "string",
    "description": "Compliance status"
   },
   "authorizedCapabilities": {
    "type": "string",
    "description": "Authorized capabilities"
   },
   "agreementCreditSummaryFromBoard2": {
    "type": "string",
    "description": "Agreement/credit summary from Board 2"
   },
   "connectedChannelsFromArea4": {
    "type": "string",
    "description": "Connected channels from Area 4"
   },
   "summaryFromBoard3": {
    "type": "string",
    "description": "Summary from Board 3"
   },
   "approvedLimit": {
    "type": "integer",
    "description": "approved limit"
   },
   "returnForChanges": {
    "type": "string",
    "description": "Return for Changes"
   },
   "restrict": {
    "type": "string",
    "description": "Restrict"
   },
   "configuredHumanAuthorization": {
    "type": "string",
    "description": "configured human authorization"
   },
   "authorization": {
    "type": "string",
    "description": "authorization"
   },
   "allocationsIntoBoard1": {
    "type": "string",
    "description": "allocations into Board 1"
   }
  }
 },
 "PartnerAccessRolesPermissionProfileView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Partner Access, Roles & Permission Profile displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "holdInventory": {
    "type": "string",
    "description": "Hold Inventory"
   },
   "confirmBooking": {
    "type": "string",
    "description": "Confirm Booking"
   },
   "modifyBooking": {
    "type": "string",
    "description": "Modify Booking"
   },
   "accessCustomerDetails": {
    "type": "string",
    "description": "Access Customer Details"
   },
   "useCredit": {
    "type": "string",
    "description": "Use Credit"
   },
   "usePaymentCard": {
    "type": "string",
    "description": "Use Payment Card"
   },
   "accessReports": {
    "type": "string",
    "description": "Access Reports"
   },
   "useApi": {
    "type": "string",
    "description": "Use API"
   },
   "manualPriceOverride": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Manual price override"
   },
   "creditAdjustment": {
    "type": "string",
    "description": "Credit adjustment"
   },
   "highValueBooking": {
    "type": "string",
    "description": "High-value booking"
   },
   "customerDataExport": {
    "type": "string",
    "description": "Customer data export"
   },
   "mayRequireAdditionalInternalApproval": {
    "type": "string",
    "description": "may require additional internal approval"
   },
   "permanent": {
    "type": "string",
    "description": "Permanent"
   },
   "temporary": {
    "type": "string",
    "description": "Temporary"
   },
   "seasonal": {
    "type": "string",
    "description": "Seasonal"
   },
   "eventSpecific": {
    "type": "string",
    "description": "Event-specific"
   }
  }
 },
 "PartnerApprovalStatusLifecycleManagementInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Partner Approval, Status & Lifecycle Management submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "thenPotentially": {
    "type": "string",
    "description": "then potentially"
   },
   "restrict": {
    "type": "string",
    "description": "Restrict"
   },
   "reactivate": {
    "type": "string",
    "description": "Reactivate"
   },
   "terminate": {
    "type": "string",
    "description": "Terminate"
   },
   "commercial": {
    "type": "string",
    "description": "Commercial"
   },
   "compliance": {
    "type": "string",
    "description": "Compliance"
   },
   "credit": {
    "type": "string",
    "description": "Credit"
   },
   "fraud": {
    "type": "string",
    "description": "Fraud"
   },
   "contractExpiry": {
    "type": "string",
    "format": "date-time",
    "description": "Contract Expiry"
   },
   "performance": {
    "type": "string",
    "description": "Performance"
   },
   "technical": {
    "type": "string",
    "description": "Technical"
   },
   "managementDecision": {
    "type": "string",
    "description": "Management Decision"
   },
   "orSelectedRestrictions": {
    "type": "string",
    "description": "or selected restrictions"
   },
   "stopNewBookings": {
    "type": "string",
    "description": "Stop New Bookings"
   },
   "stopCreditSales": {
    "type": "string",
    "description": "Stop Credit Sales"
   },
   "stopApi": {
    "type": "string",
    "description": "Stop API"
   },
   "stopSpecificVenue": {
    "type": "string",
    "description": "Stop Specific Venue"
   },
   "stopSpecificMarket": {
    "type": "string",
    "description": "Stop Specific Market"
   },
   "futureBookings": {
    "type": "string",
    "description": "Future bookings"
   },
   "activeHolds": {
    "type": "integer",
    "description": "Active holds"
   },
   "outstandingBalance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Outstanding balance"
   },
   "pendingSettlement": {
    "type": "integer",
    "description": "Pending settlement"
   },
   "activeUsers": {
    "type": "integer",
    "description": "Active users"
   },
   "activeIntegrations": {
    "type": "integer",
    "description": "Active integrations"
   },
   "existingCustomers": {
    "type": "string",
    "description": "Existing customers"
   },
   "existingTickets": {
    "type": "string",
    "description": "Existing tickets"
   },
   "currentAllocations": {
    "type": "string",
    "description": "Current allocations"
   },
   "customers": {
    "type": "string",
    "description": "customers"
   }
  }
 },
 "PartnerApprovalStatusLifecycleManagementView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Partner Approval, Status & Lifecycle Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "thenPotentially": {
    "type": "string",
    "description": "then potentially"
   },
   "restrict": {
    "type": "string",
    "description": "Restrict"
   },
   "reactivate": {
    "type": "string",
    "description": "Reactivate"
   },
   "terminate": {
    "type": "string",
    "description": "Terminate"
   },
   "commercial": {
    "type": "string",
    "description": "Commercial"
   },
   "compliance": {
    "type": "string",
    "description": "Compliance"
   },
   "credit": {
    "type": "string",
    "description": "Credit"
   },
   "fraud": {
    "type": "string",
    "description": "Fraud"
   },
   "contractExpiry": {
    "type": "string",
    "format": "date-time",
    "description": "Contract Expiry"
   },
   "performance": {
    "type": "string",
    "description": "Performance"
   },
   "technical": {
    "type": "string",
    "description": "Technical"
   },
   "managementDecision": {
    "type": "string",
    "description": "Management Decision"
   },
   "orSelectedRestrictions": {
    "type": "string",
    "description": "or selected restrictions"
   },
   "stopNewBookings": {
    "type": "string",
    "description": "Stop New Bookings"
   },
   "stopCreditSales": {
    "type": "string",
    "description": "Stop Credit Sales"
   },
   "stopApi": {
    "type": "string",
    "description": "Stop API"
   },
   "stopSpecificVenue": {
    "type": "string",
    "description": "Stop Specific Venue"
   },
   "stopSpecificMarket": {
    "type": "string",
    "description": "Stop Specific Market"
   },
   "futureBookings": {
    "type": "string",
    "description": "Future bookings"
   },
   "activeHolds": {
    "type": "integer",
    "description": "Active holds"
   },
   "outstandingBalance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Outstanding balance"
   },
   "pendingSettlement": {
    "type": "integer",
    "description": "Pending settlement"
   },
   "activeUsers": {
    "type": "integer",
    "description": "Active users"
   },
   "activeIntegrations": {
    "type": "integer",
    "description": "Active integrations"
   },
   "existingCustomers": {
    "type": "string",
    "description": "Existing customers"
   },
   "existingTickets": {
    "type": "string",
    "description": "Existing tickets"
   },
   "currentAllocations": {
    "type": "string",
    "description": "Current allocations"
   },
   "customers": {
    "type": "string",
    "description": "customers"
   }
  }
 },
 "PartnerBrandVenueBusinessScopeAssignmentInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Partner Brand, Venue & Business Scope Assignment submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "tenant": {
    "type": "string",
    "description": "Tenant"
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
   "businessUnit": {
    "type": "string",
    "description": "Business Unit"
   },
   "eventPortfolio": {
    "type": "string",
    "description": "Event Portfolio"
   },
   "market": {
    "type": "string",
    "description": "Market"
   },
   "dubaiExperiences": {
    "type": "string",
    "description": "Dubai Experiences"
   },
   "dubaiArena": {
    "type": "string",
    "description": "Dubai Arena"
   },
   "cityMuseum": {
    "type": "string",
    "description": "City Museum"
   },
   "abuDhabiWaterpark": {
    "type": "string",
    "description": "Abu Dhabi Waterpark"
   },
   "allowControlledExceptions": {
    "type": "boolean",
    "description": "Allow controlled exceptions"
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
   "temporaryAssignment": {
    "type": "string",
    "description": "Temporary Assignment"
   },
   "seasonalScope": {
    "type": "string",
    "description": "Seasonal Scope"
   }
  }
 },
 "PartnerBrandVenueBusinessScopeAssignmentView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Partner Brand, Venue & Business Scope Assignment displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "tenant": {
    "type": "string",
    "description": "Tenant"
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
   "businessUnit": {
    "type": "string",
    "description": "Business Unit"
   },
   "eventPortfolio": {
    "type": "string",
    "description": "Event Portfolio"
   },
   "market": {
    "type": "string",
    "description": "Market"
   },
   "dubaiExperiences": {
    "type": "string",
    "description": "Dubai Experiences"
   },
   "dubaiArena": {
    "type": "string",
    "description": "Dubai Arena"
   },
   "cityMuseum": {
    "type": "string",
    "description": "City Museum"
   },
   "abuDhabiWaterpark": {
    "type": "string",
    "description": "Abu Dhabi Waterpark"
   },
   "allowControlledExceptions": {
    "type": "boolean",
    "description": "Allow controlled exceptions"
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
   "temporaryAssignment": {
    "type": "string",
    "description": "Temporary Assignment"
   },
   "seasonalScope": {
    "type": "string",
    "description": "Seasonal Scope"
   }
  }
 },
 "PartnerContactsUserAdministrationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Partner Contacts & User Administration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "primaryContact": {
    "type": "string",
    "description": "Primary Contact"
   },
   "commercial": {
    "type": "string",
    "description": "Commercial"
   },
   "reservations": {
    "type": "string",
    "description": "Reservations"
   },
   "finance": {
    "type": "string",
    "description": "Finance"
   },
   "technical": {
    "type": "string",
    "description": "Technical"
   },
   "operations": {
    "type": "string",
    "description": "Operations"
   },
   "management": {
    "type": "string",
    "description": "Management"
   },
   "emergencyContact": {
    "type": "string",
    "description": "Emergency Contact"
   },
   "name": {
    "type": "string",
    "description": "Name"
   },
   "position": {
    "type": "string",
    "description": "Position"
   },
   "department": {
    "type": "string",
    "description": "Department"
   },
   "email": {
    "type": "string",
    "description": "Email"
   },
   "mobile": {
    "type": "string",
    "description": "Mobile"
   },
   "telephone": {
    "type": "string",
    "description": "Telephone"
   },
   "language": {
    "type": "string",
    "description": "Language"
   },
   "timeZone": {
    "type": "string",
    "format": "date-time",
    "description": "Time Zone"
   },
   "contactType": {
    "type": "string",
    "description": "Contact Type"
   },
   "status": {
    "type": "string",
    "description": "Status"
   },
   "username": {
    "type": "string",
    "description": "Username"
   },
   "partner": {
    "type": "string",
    "description": "Partner"
   },
   "branch": {
    "type": "string",
    "description": "Branch"
   },
   "role": {
    "type": "string",
    "description": "Role"
   },
   "permissions": {
    "type": "string",
    "description": "Permissions"
   },
   "salesLocation": {
    "type": "string",
    "description": "Sales Location"
   },
   "currency": {
    "type": "string",
    "description": "Currency"
   },
   "mfa": {
    "type": "string",
    "description": "MFA"
   },
   "passwordPolicy": {
    "type": "string",
    "description": "Password policy"
   },
   "ssoWhereAvailable": {
    "type": "string",
    "description": "SSO where available"
   },
   "loginRestrictions": {
    "type": "string",
    "description": "Login restrictions"
   },
   "accountExpiry": {
    "type": "string",
    "format": "date-time",
    "description": "Account expiry"
   },
   "sessionControls": {
    "type": "string",
    "description": "Session controls"
   },
   "reassignRole": {
    "type": "string",
    "description": "Reassign Role"
   }
  }
 },
 "PartnerDocumentationComplianceRepositoryView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Partner Documentation & Compliance Repository displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "tradeLicense": {
    "type": "string",
    "description": "Trade License"
   },
   "taxVatCertificate": {
    "type": "string",
    "description": "Tax/VAT Certificate"
   },
   "commercialRegistration": {
    "type": "string",
    "description": "Commercial Registration"
   },
   "bankDetails": {
    "type": "string",
    "description": "Bank Details"
   },
   "insurance": {
    "type": "string",
    "description": "Insurance"
   },
   "signedAgreement": {
    "type": "string",
    "description": "Signed Agreement"
   },
   "nda": {
    "type": "string",
    "description": "NDA"
   },
   "apiAgreement": {
    "type": "string",
    "description": "API Agreement"
   },
   "complianceDocuments": {
    "type": "string",
    "description": "Compliance Documents"
   },
   "identificationOfAuthorizedSignatory": {
    "type": "string",
    "description": "Identification of Authorized Signatory"
   },
   "otherRequiredDocuments": {
    "type": "string",
    "description": "Other required documents"
   },
   "documentType": {
    "type": "string",
    "description": "Document Type"
   },
   "documentNumber": {
    "type": "string",
    "description": "Document Number"
   },
   "expiryDate": {
    "type": "string",
    "format": "date-time",
    "description": "Expiry Date"
   },
   "issuingAuthority": {
    "type": "string",
    "description": "Issuing Authority"
   },
   "file": {
    "type": "string",
    "description": "File"
   },
   "verificationStatus": {
    "type": "string",
    "description": "Verification Status"
   },
   "verifiedBy": {
    "type": "string",
    "description": "Verified By"
   },
   "verificationDate": {
    "type": "string",
    "format": "date-time",
    "description": "Verification Date"
   },
   "notes": {
    "type": "string",
    "description": "Notes"
   },
   "missing": {
    "type": "string",
    "description": "Missing"
   },
   "uploaded": {
    "type": "string",
    "description": "Uploaded"
   },
   "underReview": {
    "type": "string",
    "description": "Under Review"
   },
   "verified": {
    "type": "string",
    "description": "Verified"
   },
   "rejected": {
    "type": "integer",
    "description": "Rejected"
   },
   "expiring": {
    "type": "string",
    "description": "Expiring"
   },
   "expired": {
    "type": "integer",
    "description": "Expired"
   },
   "warnOnly": {
    "type": "string",
    "description": "Warn only"
   },
   "requireManualReview": {
    "type": "boolean",
    "description": "Require manual review"
   }
  }
 },
 "PartnerManagementCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Partner Management Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "totalPartners": {
    "type": "integer",
    "description": "Total Partners"
   },
   "activePartners": {
    "type": "integer",
    "description": "Active Partners"
   },
   "pendingOnboarding": {
    "type": "integer",
    "description": "Pending Onboarding"
   },
   "pendingApproval": {
    "type": "integer",
    "description": "Pending Approval"
   },
   "suspendedPartners": {
    "type": "integer",
    "description": "Suspended Partners"
   },
   "expiringAgreements": {
    "type": "integer",
    "description": "Expiring Agreements"
   },
   "documentationIssues": {
    "type": "integer",
    "description": "Documentation Issues"
   },
   "partnersWithCreditHolds": {
    "type": "string",
    "description": "Partners With Credit Holds"
   },
   "connectedOtaApiPartners": {
    "type": "integer",
    "description": "Connected OTA/API Partners"
   },
   "partnerSalesYtd": {
    "type": "string",
    "description": "Partner Sales YTD"
   },
   "partnerRevenueYtd": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Partner Revenue YTD"
   },
   "highRiskPartners": {
    "type": "integer",
    "description": "High-Risk Partners"
   },
   "partnerId": {
    "type": "string",
    "description": "Partner ID"
   },
   "tradingName": {
    "type": "string",
    "description": "Trading Name"
   },
   "legalEntity": {
    "type": "string",
    "description": "Legal Entity"
   },
   "partnerType": {
    "type": "string",
    "description": "Partner Type"
   },
   "country": {
    "type": "string",
    "description": "Country"
   },
   "territory": {
    "type": "string",
    "description": "Territory"
   },
   "assignedBrand": {
    "type": "string",
    "description": "Assigned Brand"
   },
   "assignedVenue": {
    "type": "string",
    "description": "Assigned Venue"
   },
   "commercialOwner": {
    "type": "string",
    "description": "Commercial Owner"
   },
   "distributionChannel": {
    "type": "string",
    "description": "Distribution Channel"
   },
   "accountStatus": {
    "type": "string",
    "description": "Account Status"
   },
   "onboardingStatus": {
    "type": "string",
    "description": "Onboarding Status"
   },
   "agreementStatus": {
    "type": "string",
    "description": "Agreement Status"
   },
   "creditStatus": {
    "type": "string",
    "description": "Credit Status"
   },
   "integrationStatus": {
    "type": "string",
    "description": "Integration Status"
   },
   "lastActivity": {
    "type": "string",
    "format": "date-time",
    "description": "Last Activity"
   },
   "suspendedTerminatedArchived": {
    "type": "string",
    "description": "Suspended → Terminated → Archived"
   }
  }
 },
 "PartnerOnboardingApplicationWorkflowView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Partner Onboarding & Application Workflow displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "companyInformation": {
    "type": "string",
    "description": "Company information"
   },
   "requestedPartnerType": {
    "type": "string",
    "description": "Requested partner type"
   },
   "markets": {
    "type": "string",
    "description": "Markets"
   },
   "expectedSalesVolume": {
    "type": "integer",
    "description": "Expected sales volume"
   },
   "requestedProducts": {
    "type": "string",
    "description": "Requested products"
   },
   "requestedVenues": {
    "type": "string",
    "description": "Requested venues"
   },
   "preferredDistributionMethod": {
    "type": "string",
    "description": "Preferred distribution method"
   },
   "estimatedAnnualBusiness": {
    "type": "string",
    "description": "Estimated annual business"
   },
   "contactInformation": {
    "type": "string",
    "description": "Contact information"
   },
   "billingRequirements": {
    "type": "string",
    "description": "Billing requirements"
   },
   "eachDepartmentReceivesRelevantTasks": {
    "type": "string",
    "description": "Each department receives relevant tasks"
   },
   "businessCase": {
    "type": "string",
    "description": "Business case"
   },
   "territory": {
    "type": "string",
    "description": "Territory"
   },
   "expectedVolume": {
    "type": "integer",
    "description": "Expected volume"
   },
   "creditRequest": {
    "type": "string",
    "description": "Credit request"
   },
   "paymentTerms": {
    "type": "string",
    "description": "Payment terms"
   },
   "taxInformation": {
    "type": "string",
    "description": "Tax information"
   },
   "productRequirements": {
    "type": "string",
    "description": "Product requirements"
   },
   "fulfillmentRequirements": {
    "type": "string",
    "description": "Fulfillment requirements"
   },
   "apiIntegrationRequirements": {
    "type": "string",
    "description": "API/integration requirements"
   },
   "sequentialApproval": {
    "type": "string",
    "description": "Sequential approval"
   },
   "parallelApproval": {
    "type": "string",
    "description": "Parallel approval"
   },
   "mandatoryStage": {
    "type": "string",
    "description": "Mandatory stage"
   },
   "optionalStage": {
    "type": "string",
    "description": "Optional stage"
   },
   "sla": {
    "type": "string",
    "description": "SLA"
   },
   "escalation": {
    "type": "string",
    "description": "Escalation"
   },
   "reassignment": {
    "type": "string",
    "description": "Reassignment"
   },
   "rejection": {
    "type": "string",
    "description": "Rejection"
   },
   "requestMoreInformation": {
    "type": "string",
    "description": "Request More Information"
   }
  }
 },
 "PartnerProfileOrganizationSetupInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table covers these fields** — the closest is control.developer_account at 3%, so this is not an update to anything the package stores today and no new table has been decided",
  "description": "**What Partner Profile & Organization Setup submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "typesType": {
    "type": "string",
    "enum": [
     "b2bReseller",
     "travelAgent",
     "tourOperator",
     "ota",
     "corporateCustomer",
     "hotelConcierge",
     "destinationManagementCompany",
     "affiliate",
     "wholesaler",
     "distributor",
     "governmentPartner",
     "schoolInstitution",
     "apiPartner",
     "internalGroupCompany"
    ],
    "description": "Vocabulary listed under Partner Types."
   },
   "partnerId": {
    "type": "string",
    "description": "Partner ID"
   },
   "legalEntityName": {
    "type": "string",
    "description": "Legal Entity Name"
   },
   "tradingName": {
    "type": "string",
    "description": "Trading Name"
   },
   "partnerType": {
    "type": "string",
    "description": "Partner Type"
   },
   "registrationNumber": {
    "type": "string",
    "description": "Registration Number"
   },
   "taxVatNumber": {
    "type": "string",
    "description": "Tax/VAT Number"
   },
   "country": {
    "type": "string",
    "description": "Country"
   },
   "city": {
    "type": "string",
    "description": "City"
   },
   "registeredAddress": {
    "type": "string",
    "description": "Registered Address"
   },
   "businessAddress": {
    "type": "string",
    "description": "Business Address"
   },
   "website": {
    "type": "string",
    "description": "Website"
   },
   "mainTelephone": {
    "type": "string",
    "description": "Main Telephone"
   },
   "generalEmail": {
    "type": "string",
    "description": "General Email"
   },
   "preferredLanguage": {
    "type": "string",
    "description": "Preferred Language"
   },
   "defaultCurrency": {
    "type": "string",
    "description": "Default Currency"
   },
   "timeZone": {
    "type": "string",
    "format": "date-time",
    "description": "Time Zone"
   },
   "accountManager": {
    "type": "string",
    "description": "Account Manager"
   },
   "commercialManager": {
    "type": "string",
    "description": "Commercial Manager"
   },
   "financeOwner": {
    "type": "string",
    "description": "Finance Owner"
   },
   "operationalOwner": {
    "type": "string",
    "description": "Operational Owner"
   },
   "technicalOwner": {
    "type": "string",
    "description": "Technical Owner"
   },
   "strategic": {
    "type": "string",
    "description": "Strategic"
   },
   "keyAccount": {
    "type": "string",
    "description": "Key Account"
   },
   "standard": {
    "type": "string",
    "description": "Standard"
   },
   "newPartner": {
    "type": "integer",
    "description": "New Partner"
   },
   "highVolume": {
    "type": "integer",
    "description": "High Volume"
   },
   "vip": {
    "type": "string",
    "description": "VIP"
   },
   "restricted": {
    "type": "string",
    "description": "Restricted"
   }
  }
 },
 "PartnerProfileOrganizationSetupView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Partner Profile & Organization Setup displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "typesType": {
    "type": "string",
    "enum": [
     "b2bReseller",
     "travelAgent",
     "tourOperator",
     "ota",
     "corporateCustomer",
     "hotelConcierge",
     "destinationManagementCompany",
     "affiliate",
     "wholesaler",
     "distributor",
     "governmentPartner",
     "schoolInstitution",
     "apiPartner",
     "internalGroupCompany"
    ],
    "description": "Vocabulary listed under Partner Types."
   },
   "partnerId": {
    "type": "string",
    "description": "Partner ID"
   },
   "legalEntityName": {
    "type": "string",
    "description": "Legal Entity Name"
   },
   "tradingName": {
    "type": "string",
    "description": "Trading Name"
   },
   "partnerType": {
    "type": "string",
    "description": "Partner Type"
   },
   "registrationNumber": {
    "type": "string",
    "description": "Registration Number"
   },
   "taxVatNumber": {
    "type": "string",
    "description": "Tax/VAT Number"
   },
   "country": {
    "type": "string",
    "description": "Country"
   },
   "city": {
    "type": "string",
    "description": "City"
   },
   "registeredAddress": {
    "type": "string",
    "description": "Registered Address"
   },
   "businessAddress": {
    "type": "string",
    "description": "Business Address"
   },
   "website": {
    "type": "string",
    "description": "Website"
   },
   "mainTelephone": {
    "type": "string",
    "description": "Main Telephone"
   },
   "generalEmail": {
    "type": "string",
    "description": "General Email"
   },
   "preferredLanguage": {
    "type": "string",
    "description": "Preferred Language"
   },
   "defaultCurrency": {
    "type": "string",
    "description": "Default Currency"
   },
   "timeZone": {
    "type": "string",
    "format": "date-time",
    "description": "Time Zone"
   },
   "accountManager": {
    "type": "string",
    "description": "Account Manager"
   },
   "commercialManager": {
    "type": "string",
    "description": "Commercial Manager"
   },
   "financeOwner": {
    "type": "string",
    "description": "Finance Owner"
   },
   "operationalOwner": {
    "type": "string",
    "description": "Operational Owner"
   },
   "technicalOwner": {
    "type": "string",
    "description": "Technical Owner"
   },
   "strategic": {
    "type": "string",
    "description": "Strategic"
   },
   "keyAccount": {
    "type": "string",
    "description": "Key Account"
   },
   "standard": {
    "type": "string",
    "description": "Standard"
   },
   "newPartner": {
    "type": "integer",
    "description": "New Partner"
   },
   "highVolume": {
    "type": "integer",
    "description": "High Volume"
   },
   "vip": {
    "type": "string",
    "description": "VIP"
   },
   "restricted": {
    "type": "string",
    "description": "Restricted"
   }
  }
 },
 "TerritoryMarketDistributionRightsView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Territory, Market & Distribution Rights displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "country": {
    "type": "string",
    "description": "Country"
   },
   "region": {
    "type": "string",
    "description": "Region"
   },
   "city": {
    "type": "string",
    "description": "City"
   },
   "market": {
    "type": "string",
    "description": "Market"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "attraction": {
    "type": "string",
    "description": "Attraction"
   },
   "event": {
    "type": "string",
    "description": "Event"
   },
   "brand": {
    "type": "string",
    "description": "Brand"
   },
   "b2bPortal": {
    "type": "string",
    "description": "B2B Portal"
   },
   "api": {
    "type": "string",
    "description": "API"
   },
   "otaConnection": {
    "type": "string",
    "description": "OTA Connection"
   },
   "agentPortal": {
    "type": "string",
    "description": "Agent Portal"
   },
   "affiliateLink": {
    "type": "string",
    "description": "Affiliate Link"
   },
   "voucherDistribution": {
    "type": "string",
    "description": "Voucher Distribution"
   },
   "otherAuthorizedChannel": {
    "type": "string",
    "description": "Other authorized channel"
   },
   "uae": {
    "type": "string",
    "description": "UAE"
   },
   "dubai": {
    "type": "string",
    "description": "Dubai"
   },
   "saudiMarket": {
    "type": "string",
    "description": "Saudi market"
   },
   "directConsumerResale": {
    "type": "string",
    "description": "Direct consumer resale"
   },
   "subDistribution": {
    "type": "string",
    "description": "Sub-distribution"
   },
   "nonExclusive": {
    "type": "string",
    "description": "Non-exclusive"
   },
   "exclusive": {
    "type": "string",
    "description": "Exclusive"
   },
   "preferred": {
    "type": "string",
    "description": "Preferred"
   },
   "restricted": {
    "type": "string",
    "description": "Restricted"
   },
   "subAgentsAllowed": {
    "type": "boolean",
    "description": "Sub-agents allowed"
   },
   "subAgentsProhibited": {
    "type": "string",
    "description": "Sub-agents prohibited"
   },
   "approvalRequired": {
    "type": "boolean",
    "description": "Approval required"
   },
   "maximumHierarchyDepth": {
    "type": "string",
    "description": "Maximum hierarchy depth"
   },
   "effectiveFrom": {
    "type": "string",
    "description": "Effective From"
   },
   "effectiveTo": {
    "type": "string",
    "description": "Effective To"
   }
  }
 }
}
```
