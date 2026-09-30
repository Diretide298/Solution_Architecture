# WS21 — B2B, Reseller & OTA Partner Management board 1

**10 screens · 16 operations · 25 schemas · 3 permissions**

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

- **Every control that can be refused must be gated.** 3 permissions apply here:
  `PARTNER_MANAGE, PLATFORM_CELL_MANAGE, PLATFORM_TENANT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `PTR-022` | Partner Management Command Center | commandCentre | 2 | 0 | — |
| `PTR-023` | Partner Profile & Organization Setup | configEditor | 1 | 0 | — |
| `PTR-024` | Partner Onboarding & Application Workflow | configEditor | 2 | 1 | — |
| `PTR-025` | Partner Contacts & User Administration | configEditor | 3 | 2 | — |
| `PTR-026` | Territory, Market & Distribution Rights | configEditor | 2 | 1 | — |
| `PTR-027` | Partner Brand, Venue & Business Scope Assignment | listDetail | 1 | 0 | — |
| `PTR-028` | Partner Documentation & Compliance Repository | configEditor | 1 | 0 | — |
| `PTR-029` | Partner Access, Roles & Permission Profile | configEditor | 2 | 1 | — |
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
  "purposeNote": "Authorized administrators can identify every partner, its business relationship, current status and outstanding actions from a single workspace.",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each partner record should display) — counts over a population, then the population",
  "purpose": "Provide a centralized management dashboard for all B2B, reseller, OTA and distribution partners across the TICVAI ecosystem.",
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
       "bindsTo": "PartnerManagementCommandCenterSummary.totalPartners"
      },
      {
       "kind": "metricTile",
       "label": "Active Partners",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 5 §Display",
       "bindsTo": "PartnerManagementCommandCenterSummary.activePartners"
      },
      {
       "kind": "metricTile",
       "label": "Pending Onboarding",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 5 §Display",
       "bindsTo": "PartnerManagementCommandCenterSummary.pendingOnboarding"
      },
      {
       "kind": "metricTile",
       "label": "Pending Approval",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 5 §Display",
       "bindsTo": "PartnerManagementCommandCenterSummary.pendingApproval"
      },
      {
       "kind": "metricTile",
       "label": "Suspended Partners",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 5 §Display",
       "bindsTo": "PartnerManagementCommandCenterSummary.suspendedPartners"
      },
      {
       "kind": "metricTile",
       "label": "Expiring Agreements",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 5 §Display",
       "bindsTo": "PartnerManagementCommandCenterSummary.expiringAgreements"
      },
      {
       "kind": "metricTile",
       "label": "Documentation Issues",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 5 §Display",
       "bindsTo": "PartnerManagementCommandCenterSummary.documentationIssues"
      },
      {
       "kind": "metricTile",
       "label": "Partners With Credit Holds",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 5 §Display",
       "bindsTo": "PartnerManagementCommandCenterSummary.partnersWithCreditHolds"
      },
      {
       "kind": "metricTile",
       "label": "Connected OTA/API Partners",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 5 §Display",
       "bindsTo": "PartnerManagementCommandCenterSummary.connectedOtaApiPartners"
      },
      {
       "kind": "metricTile",
       "label": "Partner Sales YTD",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 5 §Display",
       "bindsTo": "PartnerManagementCommandCenterSummary.partnerSalesYtd"
      },
      {
       "kind": "metricTile",
       "label": "Partner Revenue YTD",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 5 §Display",
       "bindsTo": "PartnerManagementCommandCenterSummary.partnerRevenueYtd"
      },
      {
       "kind": "metricTile",
       "label": "High-Risk Partners",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 5 §Display",
       "bindsTo": "PartnerManagementCommandCenterSummary.highRiskPartners"
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
    "operationId": "listPartner2",
    "contract": "subscription",
    "purpose": "Partner Operations Command Center",
    "trigger": "onLoad"
   },
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
   "board": "wireframes/P10 Partner Web.dc.html#ptr-022",
   "workshopBoard": "wireframes/WS38 B2B, Reseller & OTA Partner Management Board 1.dc.html#ptr-022"
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
  "purposeNote": "Each external partner has one governed master organization record that can be referenced by commercial, operational, finance and distribution processes.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population",
  "purpose": "Create the master business record for each external distribution partner.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 2 actions on this screen and the screen declares 1 operation.** Unserved: Key Account, New Partner. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
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
       "label": "Key Account",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 7 §Allow internal tags such as"
      },
      {
       "kind": "secondaryButton",
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
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-023",
   "workshopBoard": "wireframes/WS38 B2B, Reseller & OTA Partner Management Board 1.dc.html#ptr-023"
  },
  "apisNote": "Regenerated 9 September 2026 from B2B, Reseller & OTA Partner Management_Reference.pdf page 7. 0 of 0 labels bound to a contract property; 18 of 53 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "purposeNote": "New partners cannot become commercially active until the configured onboarding and approval stages have been successfully completed.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population",
  "purpose": "Manage the complete journey from a new partner application through internal review and activation.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 5 actions on this screen; 1 are served since the writers pass (29 September): Request More Information by `actOnPartnerApplicationReview`.** Still unserved: Product requirements, Sequential approval, Parallel approval, Rejection. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 8 §Operations"
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
       "label": "Product requirements",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 8 §Operations"
      },
      {
       "kind": "secondaryButton",
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
       "label": "Rejection",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 8 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Request More Information",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 8 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Act on partner application review",
       "operation": "actOnPartnerApplicationReview",
       "permission": "PARTNER_MANAGE",
       "notes": "The review actions on PTR-024 (decided 29 September, writers pass; DM4).",
       "provenance": "contract subscription.yaml POST /partner-applications/{applicationId}/review-actions"
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
   },
   {
    "operationId": "actOnPartnerApplicationReview",
    "contract": "subscription",
    "purpose": "Move a partner application through its departmental review",
    "trigger": "onAction",
    "invalidates": [
     "listPartnerOnboardingApplication"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-024",
   "workshopBoard": "wireframes/WS38 B2B, Reseller & OTA Partner Management Board 1.dc.html#ptr-024"
  },
  "apisNote": "Regenerated 9 September 2026 from B2B, Reseller & OTA Partner Management_Reference.pdf page 8. 0 of 0 labels bound to a contract property; 15 of 43 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formActOnPartnerApplicationReview",
    "component": "modal",
    "trigger": "Act on partner application review",
    "body": "**Collects what `actOnPartnerApplicationReview` sends before it is called.** Required: `action`. Optional: `department`, `assigneePrincipalId`, `note`, `documentIds`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "PartnerApplicationReviewAction",
    "confirm": {
     "label": "Act on partner application review",
     "operation": "actOnPartnerApplicationReview"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "action",
      "department",
      "assigneePrincipalId",
      "note",
      "documentIds"
     ]
    },
    "provenance": "contract subscription.yaml POST /partner-applications/{applicationId}/review-actions"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "applicationId",
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
  "purposeNote": "Every external user accessing TICVAI on behalf of a partner is associated with a valid partner account and controlled through appropriate roles and permissions.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture; Configure) and no display directory — it is settings, not a population",
  "purpose": "Manage the individuals authorized to interact with TICVAI on behalf of each partner.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 9 actions on this screen; 6 are served since the writers pass (29 September): Primary Contact, Commercial, Finance, Operations, Management, Emergency Contact by `setPartnerContact`.** Still unserved: Password policy, SSO where available …. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 10 §Support"
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
       "label": "Primary Contact",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 10 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Commercial",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 10 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Finance",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 10 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Operations",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 10 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Management",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 10 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Emergency Contact",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 10 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Password policy",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 10 §Support/reference"
      },
      {
       "kind": "secondaryButton",
       "label": "SSO where available",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 10 §Support/reference"
      },
      {
       "kind": "secondaryButton",
       "label": "Save partner contact",
       "operation": "setPartnerContact",
       "permission": "PARTNER_MANAGE",
       "notes": "The contact half of PTR-025 (decided 29 September, writers pass; DM4).",
       "provenance": "contract subscription.yaml PUT /partner-contacts"
      },
      {
       "kind": "secondaryButton",
       "label": "Create partner user",
       "operation": "createPartnerUser",
       "permission": "PARTNER_MANAGE",
       "notes": "2.7.51.",
       "provenance": "contract subscription.yaml POST /partners/{partnerId}/users"
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
   },
   {
    "operationId": "setPartnerContact",
    "contract": "subscription",
    "purpose": "Create, edit, disable, enable or revoke a partner contact",
    "trigger": "onAction",
    "invalidates": [
     "listPartnerContactUser"
    ]
   },
   {
    "operationId": "createPartnerUser",
    "contract": "subscription",
    "purpose": "Add a user to a partner branch",
    "trigger": "onAction",
    "invalidates": [
     "listPartnerContactUser"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-025",
   "workshopBoard": "wireframes/WS38 B2B, Reseller & OTA Partner Management Board 1.dc.html#ptr-025"
  },
  "apisNote": "Regenerated 9 September 2026 from B2B, Reseller & OTA Partner Management_Reference.pdf page 10. 0 of 0 labels bound to a contract property; 26 of 52 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formSetPartnerContact",
    "component": "modal",
    "trigger": "Save partner contact",
    "body": "**Collects what `setPartnerContact` sends before it is called.** Required: `partnerId`. Optional: `contactId`, `action`, `name`, `position`, `department`, `email`, `mobile`, `telephone`, `language`, `timeZone`, `contactType`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "PartnerContactInput",
    "confirm": {
     "label": "Save partner contact",
     "operation": "setPartnerContact"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "partnerId",
      "contactId",
      "action",
      "name",
      "position",
      "department",
      "email",
      "mobile",
      "telephone",
      "language",
      "timeZone",
      "contactType"
     ]
    },
    "provenance": "contract subscription.yaml PUT /partner-contacts"
   },
   {
    "id": "formCreatePartnerUser",
    "component": "modal",
    "trigger": "Create partner user",
    "body": "**Collects what `createPartnerUser` sends before it is called.** Required: `id`, `partnerId`, `principalId`, `branchScopePath`. Optional: `role`, `salesLocation`, `currency`, `accountExpiresAt`, `allocationQuota`, `creditLimitOverride`, `canManageUsers`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "PartnerUser",
    "confirm": {
     "label": "Create partner user",
     "operation": "createPartnerUser"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "partnerId",
      "principalId",
      "branchScopePath",
      "role",
      "salesLocation",
      "currency",
      "accountExpiresAt",
      "allocationQuota",
      "creditLimitOverride",
      "canManageUsers"
     ]
    },
    "provenance": "contract subscription.yaml POST /partners/{partnerId}/users"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "partnerId",
     "from": "session"
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
  "purposeNote": "partner is authorized to use.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Define where and through what business scope a partner is authorized to distribute TICVAI products.",
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
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save partner distribution rights",
       "operation": "setPartnerDistributionRights",
       "permission": "PARTNER_MANAGE",
       "notes": "The writer for PTR-026 (decided 29 September, writers pass; DM4).",
       "provenance": "contract subscription.yaml PUT /partners/{partnerId}/distribution-rights"
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
   },
   {
    "operationId": "setPartnerDistributionRights",
    "contract": "subscription",
    "purpose": "Replace a partner's territory, market and distribution rights",
    "trigger": "onAction",
    "invalidates": [
     "listTerritoryMarketDistribution"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-026",
   "workshopBoard": "wireframes/WS38 B2B, Reseller & OTA Partner Management Board 1.dc.html#ptr-026"
  },
  "apisNote": "Regenerated 9 September 2026 from B2B, Reseller & OTA Partner Management_Reference.pdf page 12. 0 of 0 labels bound to a contract property; 4 of 40 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formSetPartnerDistributionRights",
    "component": "modal",
    "trigger": "Save partner distribution rights",
    "body": "**Collects what `setPartnerDistributionRights` sends before it is called.** Required: `rights`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save partner distribution rights",
     "operation": "setPartnerDistributionRights"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "rights"
     ]
    },
    "provenance": "contract subscription.yaml PUT /partners/{partnerId}/distribution-rights"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "partnerId",
     "from": "session"
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
  "purposeNote": "Every partner is associated only with the TICVAI brands, venues and business entities for which the commercial relationship has been approved.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Determine which TICVAI business entities the partner relationship covers. This is deliberately separate from product assignment, which is governed through the Sales Channel and commercial configuration layers.",
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
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-027",
   "workshopBoard": "wireframes/WS38 B2B, Reseller & OTA Partner Management Board 1.dc.html#ptr-027"
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
  "purposeNote": "restrict commercial activity when mandatory documentation is missing or invalid.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture; Configure whether expiration should) and no display directory — it is settings, not a population",
  "purpose": "Maintain required partner documentation and ensure that commercial accounts remain compliant.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 4 actions on this screen and the screen declares 1 operation.** Unserved: Commercial Registration, Bank Details, Signed Agreement, API Agreement. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 15 §Support configurable documents such as"
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
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Commercial Registration",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 15 §Support configurable documents such as"
      },
      {
       "kind": "secondaryButton",
       "label": "Bank Details",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 15 §Support configurable documents such as"
      },
      {
       "kind": "secondaryButton",
       "label": "Signed Agreement",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 15 §Support configurable documents such as"
      },
      {
       "kind": "secondaryButton",
       "label": "API Agreement",
       "provenance": "pack B2B, Reseller & OTA Partner Management_Reference.pdf, page 15 §Support configurable documents such as"
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
   "board": "wireframes/P10 Partner Web.dc.html#ptr-028",
   "workshopBoard": "wireframes/WS38 B2B, Reseller & OTA Partner Management Board 1.dc.html#ptr-028"
  },
  "apisNote": "Regenerated 9 September 2026 from B2B, Reseller & OTA Partner Management_Reference.pdf page 15. 0 of 0 labels bound to a contract property; 19 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "purposeNote": "Partner organizations can access only the capabilities authorized by TICVAI, regardless of permissions assigned to individual partner users.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure whether the partner may) and no display directory — it is settings, not a population",
  "purpose": "Control what a partner organization is permitted to do, beyond individual-user permissions.",
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
      },
      {
       "kind": "primaryButton",
       "label": "Save partner capability grants",
       "operation": "setPartnerCapabilityGrants",
       "permission": "PARTNER_MANAGE",
       "notes": "The writer for PTR-029's organisation ceiling (decided 29 September, writers pass; DM4).",
       "provenance": "contract subscription.yaml PUT /partners/{partnerId}/capability-grants"
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
   },
   {
    "operationId": "setPartnerCapabilityGrants",
    "contract": "subscription",
    "purpose": "Replace the capability ceiling of a partner",
    "trigger": "onAction",
    "invalidates": [
     "listPartnerAccessRole"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-029",
   "workshopBoard": "wireframes/WS38 B2B, Reseller & OTA Partner Management Board 1.dc.html#ptr-029"
  },
  "apisNote": "Regenerated 9 September 2026 from B2B, Reseller & OTA Partner Management_Reference.pdf page 16. 0 of 0 labels bound to a contract property; 23 of 34 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formSetPartnerCapabilityGrants",
    "component": "modal",
    "trigger": "Save partner capability grants",
    "body": "**Collects what `setPartnerCapabilityGrants` sends before it is called.** Required: `grants`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save partner capability grants",
     "operation": "setPartnerCapabilityGrants"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "grants"
     ]
    },
    "provenance": "contract subscription.yaml PUT /partners/{partnerId}/capability-grants"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "partnerId",
     "from": "session"
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
  "purposeNote": "Partner lifecycle changes are governed, effective-dated, auditable and do not unintentionally damage valid existing customer transactions.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population",
  "purpose": "Govern the complete business lifecycle of a partner after onboarding.",
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
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P10 Partner Web.dc.html#ptr-030",
   "workshopBoard": "wireframes/WS38 B2B, Reseller & OTA Partner Management Board 1.dc.html#ptr-030"
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
  "purposeNote": "Before activation, authorized management can evaluate the partner's complete organizational, compliance, access, commercial and technical readiness from one consolidated view. Board 1 — Final Screen Register Screen Backend Screen Primary Responsibility 8.1.1 Partner Management Command Center Partner portfolio & status Screen Backend Screen Primary Responsibility 8.1.2 Partner Profile & Organization Setup Master partner record 8.1.3 Partner Onboarding & Application Workflow Partner onboarding 8.1.4 Partner Contacts & User Administration Contacts and B2B users",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide one consolidated Partner 360 screen before activation and throughout the relationship. This should become one of the most useful screens for TICVAI commercial management. Board 1 established who the partner is and what they are authorized to access. Board 2 establishes the commercial rules under which that partner can transact with TICVAI.",
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
   "board": "wireframes/P10 Partner Web.dc.html#ptr-031",
   "workshopBoard": "wireframes/WS38 B2B, Reseller & OTA Partner Management Board 1.dc.html#ptr-031"
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
 "actOnPartnerApplicationReview": {
  "method": "POST",
  "path": "/partner-applications/{applicationId}/review-actions",
  "contract": "subscription",
  "summary": "Move a partner application through its departmental review",
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
  "requestBody": "PartnerApplicationReviewAction",
  "responds": "PartnerApplication"
 },
 "approvePartnerStatuLifecycle": {
  "method": "PUT",
  "path": "/partner-statu-lifecycle",
  "contract": "subscription",
  "summary": "Partner Approval, Status & Lifecycle Management",
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
  "requestBody": "PartnerApprovalStatusLifecycleManagementInput",
  "responds": "PartnerApprovalStatusLifecycleManagementView"
 },
 "createPartnerUser": {
  "method": "POST",
  "path": "/partners/{partnerId}/users",
  "contract": "subscription",
  "summary": "Add a user to a partner branch",
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
  "requestBody": "PartnerUser",
  "responds": "PartnerUser"
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
    "name": "risk",
    "in": "query",
    "required": false
   },
   {
    "name": "integrationType",
    "in": "query",
    "required": false
   },
   {
    "name": "partnerType",
    "in": "query",
    "required": false
   },
   {
    "name": "country",
    "in": "query",
    "required": false
   },
   {
    "name": "territory",
    "in": "query",
    "required": false
   },
   {
    "name": "agreementStatus",
    "in": "query",
    "required": false
   },
   {
    "name": "creditStatus",
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
 "listPartner2": {
  "method": "GET",
  "path": "/partner-2",
  "contract": "subscription",
  "summary": "Partner Operations Command Center",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "venue",
    "in": "query",
    "required": false
   },
   {
    "name": "event",
    "in": "query",
    "required": false
   },
   {
    "name": "market",
    "in": "query",
    "required": false
   },
   {
    "name": "channel",
    "in": "query",
    "required": false
   },
   {
    "name": "from",
    "in": "query",
    "required": false
   },
   {
    "name": "to",
    "in": "query",
    "required": false
   },
   {
    "name": "partnerId",
    "in": "query",
    "required": false
   },
   {
    "name": "partnerType",
    "in": "query",
    "required": false
   },
   {
    "name": "accountManager",
    "in": "query",
    "required": false
   },
   {
    "name": "operationalStatus",
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
 "listPartnerAccessRole": {
  "method": "GET",
  "path": "/partner-access-role",
  "contract": "subscription",
  "summary": "Partner Access, Roles & Permission Profile",
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
    "name": "capability",
    "in": "query",
    "required": false
   },
   {
    "name": "grantType",
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
 "listPartnerContactUser": {
  "method": "GET",
  "path": "/partner-contact-user",
  "contract": "subscription",
  "summary": "Partner Contacts & User Administration",
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
    "name": "contactType",
    "in": "query",
    "required": false
   },
   {
    "name": "status",
    "in": "query",
    "required": false
   },
   {
    "name": "hasUserAccount",
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
 "listPartnerDocumentationCompliance": {
  "method": "GET",
  "path": "/partner-documentation-compliance",
  "contract": "subscription",
  "summary": "Partner Documentation & Compliance Repository",
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
    "name": "documentType",
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
 "listPartnerOnboardingApplication": {
  "method": "GET",
  "path": "/partner-onboarding-application",
  "contract": "subscription",
  "summary": "Partner Onboarding & Application Workflow",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "stage",
    "in": "query",
    "required": false
   },
   {
    "name": "status",
    "in": "query",
    "required": false
   },
   {
    "name": "requestedPartnerType",
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
 "listPartnerProfileReadiness": {
  "method": "GET",
  "path": "/partner-profile-readiness",
  "contract": "subscription",
  "summary": "Partner 360° Profile, Readiness & AI Review",
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
 "listTerritoryMarketDistribution": {
  "method": "GET",
  "path": "/territory-market-distribution",
  "contract": "subscription",
  "summary": "Territory, Market & Distribution Rights",
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
    "name": "country",
    "in": "query",
    "required": false
   },
   {
    "name": "market",
    "in": "query",
    "required": false
   },
   {
    "name": "distributionMethod",
    "in": "query",
    "required": false
   },
   {
    "name": "exclusivity",
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
 "setPartnerBrandVenue": {
  "method": "PUT",
  "path": "/partner-brand-venue",
  "contract": "subscription",
  "summary": "Partner Brand, Venue & Business Scope Assignment",
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
  "requestBody": "PartnerBrandVenueBusinessScopeAssignmentInput",
  "responds": "PartnerBrandVenueBusinessScopeAssignmentView"
 },
 "setPartnerCapabilityGrants": {
  "method": "PUT",
  "path": "/partners/{partnerId}/capability-grants",
  "contract": "subscription",
  "summary": "Replace the capability ceiling of a partner",
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
  "responds": null
 },
 "setPartnerContact": {
  "method": "PUT",
  "path": "/partner-contacts",
  "contract": "subscription",
  "summary": "Create, edit, disable, enable or revoke a partner contact",
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
  "requestBody": "PartnerContactInput",
  "responds": "PartnerContact"
 },
 "setPartnerDistributionRights": {
  "method": "PUT",
  "path": "/partners/{partnerId}/distribution-rights",
  "contract": "subscription",
  "summary": "Replace a partner's territory, market and distribution rights",
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
  "responds": null
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "PartnerProfileOrganizationSetupInput",
  "responds": "PartnerProfileOrganizationSetupView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
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
 "Partner360ProfileReadinessAiReviewView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over control.partner and its control.partner_* rows and the existing subscription state, assembled at read time (data model DM4)",
  "description": "**What Partner 360° Profile, Readiness & AI Review displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "companyInformationAndHierarchy": {
    "type": "string",
    "description": "Organization: legal entity and parent chain, e.g. \"Gulf Travel LLC > Gulf Travel Group\""
   },
   "keyPartnerContacts": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Contacts: key partner contacts (name and contact type)"
   },
   "activeB2bUsers": {
    "type": "integer",
    "description": "Users: active B2B users"
   },
   "authorizedMarkets": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Territories: authorized markets"
   },
   "brandsAndVenues": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Business Scope: brands and venues"
   },
   "complianceStatus": {
    "type": "string",
    "description": "Documentation: compliant, expiring, incomplete or nonCompliant"
   },
   "authorizedCapabilities": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Permissions: authorized capabilities"
   },
   "commercialSummary": {
    "type": "string",
    "description": "Commercial: agreement and credit summary"
   },
   "connectedChannels": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "b2bPortal",
      "api",
      "otaConnection",
      "agentPortal",
      "affiliateLink",
      "voucherDistribution",
      "bulkTicketExport",
      "other"
     ]
    },
    "description": "Distribution: connected channels"
   },
   "performanceSummary": {
    "type": "string",
    "description": "Performance: scorecard summary"
   },
   "partnerId": {
    "type": "string",
    "format": "uuid",
    "description": "Partner"
   },
   "partnerName": {
    "type": "string",
    "description": "Partner Name"
   },
   "partnerType": {
    "type": "string",
    "description": "Partner Type code"
   },
   "accountManager": {
    "type": "string",
    "description": "Account Manager"
   },
   "country": {
    "type": "string",
    "description": "Country, ISO 3166-1 alpha-2"
   },
   "status": {
    "type": "string",
    "description": "Status: lead, applicant, underReview, approved, configuration, active, restricted, suspended, terminated or archived (pack p.6 and p.18 merged with MoM 31 Aug 4.3 lead -> submitted -> active -> suspended; \"submitted\" is applicant)"
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
   "salesYtd": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Sales YTD"
   },
   "outstandingBalance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Outstanding Balance"
   },
   "readinessScore": {
    "type": "integer",
    "description": "Readiness Score, 0-100"
   },
   "readinessBreakdown": {
    "type": "object",
    "description": "Readiness by section, each 0-100",
    "properties": {
     "organization": {
      "type": "integer"
     },
     "contacts": {
      "type": "integer"
     },
     "documentation": {
      "type": "integer"
     },
     "territory": {
      "type": "integer"
     },
     "permissions": {
      "type": "integer"
     },
     "commercialAgreement": {
      "type": "integer"
     },
     "credit": {
      "type": "integer"
     },
     "integration": {
      "type": "integer"
     }
    }
   },
   "blockers": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Critical blockers to activation"
   },
   "aiRecommendation": {
    "type": "string",
    "enum": [
     "recommendedForActivation",
     "activationNotRecommended"
    ],
    "description": "Advisory AI Partner Review verdict",
    "nullable": true
   },
   "aiInsights": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Advisory AI Partner Review narrative"
   }
  }
 },
 "PartnerAccessRolesPermissionProfileView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over control.partner_capability_grant (PartnerCapabilityGrant) and the existing subscription state, assembled at read time (data model DM4)",
  "description": "**What Partner Access, Roles & Permission Profile displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "partnerId": {
    "type": "string",
    "format": "uuid",
    "description": "Partner"
   },
   "capability": {
    "type": "string",
    "enum": [
     "searchAvailability",
     "createBooking",
     "holdInventory",
     "confirmBooking",
     "cancelBooking",
     "modifyBooking",
     "rescheduleBooking",
     "downloadTicket",
     "printTicket",
     "sendTicket",
     "accessCustomerDetails",
     "useCredit",
     "usePaymentCard",
     "viewCommission",
     "viewNetRates",
     "accessReports",
     "exportData",
     "useApi",
     "createSubAgents",
     "refund",
     "manualPriceOverride",
     "creditAdjustment",
     "highValueBooking",
     "customerDataExport"
    ],
    "description": "Organization-level capability (pack pp.16-17; refund and rescheduleBooking from MoM 31 Aug 4.3)"
   },
   "allowed": {
    "type": "boolean",
    "description": "Whether the partner may use this capability"
   },
   "requiresInternalApproval": {
    "type": "boolean",
    "description": "Sensitive function: each use needs additional internal approval"
   },
   "grantType": {
    "type": "string",
    "enum": [
     "permanent",
     "temporary",
     "seasonal",
     "eventSpecific"
    ],
    "description": "Effective Dates: how long the grant lasts"
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date",
    "description": "Effective from",
    "nullable": true
   },
   "effectiveTo": {
    "type": "string",
    "format": "date",
    "description": "Effective to",
    "nullable": true
   },
   "eventId": {
    "type": "string",
    "description": "Event the grant is limited to, for an eventSpecific grant",
    "nullable": true
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
 "PartnerApplication": {
  "type": "object",
  "x-ticvai-persistence": "control.partner_application + control.partner_application_review_task",
  "description": "A partner onboarding application and where it stands in the review. `registerPartner` creates one with the partner record it opens (lifecycle `applicant`); the stage moves through the departmental reviews and the decision itself goes through `approvals` (decided 29 September, data model DM4)\n\n**Written by** registerPartner (creates the application `submitted` with the partner `applicant`) and actOnPartnerApplicationReview (starts the review, completes a departmental task, asks for and receives more information, withdraws); the approval itself is decided in approvals (decided 29 September, writers pass; DM4).",
  "required": [
   "id",
   "companyName",
   "stage",
   "status",
   "submittedAt"
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
    "nullable": true,
    "description": "Partner record created on submission (lifecycle applicant)."
   },
   "companyName": {
    "type": "string",
    "description": "Company legal name as applied."
   },
   "tradingName": {
    "type": "string",
    "nullable": true,
    "description": "Trading name as applied."
   },
   "country": {
    "type": "string",
    "nullable": true,
    "description": "Country, ISO 3166-1 alpha-2."
   },
   "requestedPartnerType": {
    "type": "string",
    "nullable": true,
    "description": "Requested partner type code (see `Partner.partnerType`)."
   },
   "markets": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Markets the applicant wants to sell into."
   },
   "expectedSalesVolume": {
    "type": "integer",
    "nullable": true,
    "description": "Expected sales volume, tickets per year."
   },
   "requestedProducts": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Requested products."
   },
   "requestedVenues": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Requested venues."
   },
   "preferredDistributionMethod": {
    "type": "string",
    "enum": [
     "b2bPortal",
     "api",
     "otaConnection",
     "agentPortal",
     "affiliateLink",
     "voucherDistribution",
     "bulkTicketExport",
     "other"
    ],
    "nullable": true,
    "description": "Preferred distribution method."
   },
   "estimatedAnnualBusiness": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "Estimated annual business value."
   },
   "contactName": {
    "type": "string",
    "nullable": true,
    "description": "Applicant contact name."
   },
   "contactEmail": {
    "type": "string",
    "format": "email",
    "description": "Applicant contact email."
   },
   "billingRequirements": {
    "type": "string",
    "nullable": true,
    "description": "Billing requirements as stated by the applicant."
   },
   "businessCase": {
    "type": "string",
    "nullable": true,
    "description": "Commercial review: business case."
   },
   "territory": {
    "type": "string",
    "nullable": true,
    "description": "Commercial review: territory."
   },
   "creditRequest": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "Finance review: requested credit limit."
   },
   "paymentTerms": {
    "type": "string",
    "nullable": true,
    "description": "Finance review: requested payment terms."
   },
   "taxRegistrationNumber": {
    "type": "string",
    "nullable": true,
    "description": "Finance review: tax/VAT registration number."
   },
   "productRequirements": {
    "type": "string",
    "nullable": true,
    "description": "Operations review: product requirements."
   },
   "fulfillmentRequirements": {
    "type": "string",
    "nullable": true,
    "description": "Operations review: fulfilment requirements."
   },
   "apiIntegrationRequirements": {
    "type": "string",
    "nullable": true,
    "description": "Technical review: API/integration requirements."
   },
   "stage": {
    "type": "string",
    "enum": [
     "application",
     "businessVerification",
     "documentation",
     "commercialReview",
     "financeReview",
     "technicalReview",
     "approval",
     "configuration",
     "activation"
    ],
    "default": "application",
    "description": "Current onboarding stage (pack p.9 Onboarding Workflow)."
   },
   "status": {
    "type": "string",
    "enum": [
     "submitted",
     "inReview",
     "moreInformationRequested",
     "approved",
     "rejected",
     "withdrawn"
    ],
    "default": "submitted",
    "description": "Application status."
   },
   "reviewTasks": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "department",
      "completed"
     ],
     "properties": {
      "department": {
       "type": "string",
       "enum": [
        "commercial",
        "finance",
        "operations",
        "technical"
       ]
      },
      "assigneePrincipalId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "dueAt": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      },
      "completed": {
       "type": "boolean"
      }
     }
    },
    "description": "Internal Review: the task each department receives; the rows of control.partner_application_review_task."
   },
   "submittedAt": {
    "type": "string",
    "format": "date-time",
    "description": "Submitted at."
   },
   "slaDueAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "When the current stage breaches its SLA."
   },
   "approvalRequestId": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "The approvals request carrying the decision, as on `PartnerAgreement`."
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
 "PartnerApplicationReviewAction": {
  "type": "object",
  "x-ticvai-persistence": "none — request only; applied to control.partner_application and control.partner_application_review_task, and to control.partner on startReview and withdraw (decided 29 September, writers pass; DM4)",
  "description": "One review action on a partner application (actOnPartnerApplicationReview) (decided 29 September, writers pass; DM4)",
  "required": [
   "action"
  ],
  "properties": {
   "action": {
    "type": "string",
    "enum": [
     "startReview",
     "completeTask",
     "requestInformation",
     "supplyInformation",
     "withdraw"
    ],
    "description": "The action (states/partner-application.yaml)"
   },
   "department": {
    "type": "string",
    "enum": [
     "commercial",
     "finance",
     "operations",
     "technical"
    ],
    "nullable": true,
    "description": "For completeTask, the department whose review task is done"
   },
   "assigneePrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "For startReview, who each opened task is assigned to when one person reviews all; empty leaves them to each department's queue"
   },
   "note": {
    "type": "string",
    "nullable": true,
    "description": "The reviewer's finding (completeTask), what is missing (requestInformation, required) or the applicant's answer (supplyInformation)"
   },
   "documentIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "For supplyInformation, documents uploaded in answer (control.partner_document)"
   }
  }
 },
 "PartnerApprovalStatusLifecycleManagementInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; stored as control.partner_status_history (PartnerStatusHistory), with the resulting status on control.partner (data model DM4)",
  "description": "**What Partner Approval, Status & Lifecycle Management submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "partnerId": {
    "type": "string",
    "format": "uuid",
    "description": "Partner"
   },
   "action": {
    "type": "string",
    "enum": [
     "approve",
     "activate",
     "restrict",
     "suspend",
     "reactivate",
     "terminate",
     "archive"
    ],
    "description": "Status Actions"
   },
   "reasonCategory": {
    "type": "string",
    "enum": [
     "commercial",
     "compliance",
     "credit",
     "fraud",
     "contractExpiry",
     "performance",
     "technical",
     "managementDecision"
    ],
    "description": "Status Reasons"
   },
   "reasonNote": {
    "type": "string",
    "description": "Free-text reason",
    "nullable": true
   },
   "suspensionScope": {
    "type": "string",
    "enum": [
     "full",
     "selected"
    ],
    "description": "Suspension Scope: full suspension or selected restrictions",
    "nullable": true
   },
   "restrictions": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "stopNewBookings",
      "stopCreditSales",
      "stopApi",
      "stopSpecificVenue",
      "stopSpecificMarket"
     ]
    },
    "description": "Selected restrictions when suspensionScope is selected, or for restrict"
   },
   "restrictedVenueIds": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Venues for stopSpecificVenue"
   },
   "restrictedMarkets": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Markets for stopSpecificMarket"
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date-time",
    "description": "When the change takes effect; lifecycle changes are effective-dated"
   },
   "dryRun": {
    "type": "boolean",
    "description": "When true, return the impact analysis without changing anything, so the screen can show it before the administrator confirms (decided 29 September, readiness close-out)"
   }
  }
 },
 "PartnerApprovalStatusLifecycleManagementView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over control.partner and control.partner_status_history and the existing subscription state, assembled at read time (data model DM4)",
  "description": "**What Partner Approval, Status & Lifecycle Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "futureBookings": {
    "type": "integer",
    "description": "Impact: future bookings"
   },
   "activeHolds": {
    "type": "integer",
    "description": "Impact: active holds"
   },
   "outstandingBalance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Impact: outstanding balance"
   },
   "pendingSettlement": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Impact: pending settlement"
   },
   "activeUsers": {
    "type": "integer",
    "description": "Impact: active users"
   },
   "activeIntegrations": {
    "type": "integer",
    "description": "Impact: active integrations"
   },
   "existingCustomers": {
    "type": "integer",
    "description": "Impact: existing customers holding tickets"
   },
   "existingTickets": {
    "type": "integer",
    "description": "Impact: existing tickets; never invalidated by a suspension"
   },
   "currentAllocations": {
    "type": "integer",
    "description": "Impact: current contractual allocations"
   },
   "partnerId": {
    "type": "string",
    "format": "uuid",
    "description": "Partner"
   },
   "action": {
    "type": "string",
    "enum": [
     "approve",
     "activate",
     "restrict",
     "suspend",
     "reactivate",
     "terminate",
     "archive"
    ],
    "description": "Status Actions"
   },
   "reasonCategory": {
    "type": "string",
    "enum": [
     "commercial",
     "compliance",
     "credit",
     "fraud",
     "contractExpiry",
     "performance",
     "technical",
     "managementDecision"
    ],
    "description": "Status Reasons"
   },
   "reasonNote": {
    "type": "string",
    "description": "Free-text reason",
    "nullable": true
   },
   "suspensionScope": {
    "type": "string",
    "enum": [
     "full",
     "selected"
    ],
    "description": "Suspension Scope: full suspension or selected restrictions",
    "nullable": true
   },
   "restrictions": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "stopNewBookings",
      "stopCreditSales",
      "stopApi",
      "stopSpecificVenue",
      "stopSpecificMarket"
     ]
    },
    "description": "Selected restrictions when suspensionScope is selected, or for restrict"
   },
   "restrictedVenueIds": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Venues for stopSpecificVenue"
   },
   "restrictedMarkets": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Markets for stopSpecificMarket"
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date-time",
    "description": "When the change takes effect; lifecycle changes are effective-dated"
   },
   "status": {
    "type": "string",
    "description": "Resulting account status: lead, applicant, underReview, approved, configuration, active, restricted, suspended, terminated or archived (pack p.6 and p.18 merged with MoM 31 Aug 4.3 lead -> submitted -> active -> suspended; \"submitted\" is applicant)"
   },
   "applied": {
    "type": "boolean",
    "description": "False when dryRun was set or the change awaits approval"
   },
   "approvalRequestId": {
    "type": "string",
    "description": "Approval request raised for the change",
    "nullable": true
   },
   "aiImpactSummary": {
    "type": "string",
    "description": "Advisory AI summary of the business impact",
    "nullable": true
   }
  }
 },
 "PartnerBrandVenueBusinessScopeAssignmentInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; stored as control.partner_scope_assignment (PartnerScopeAssignment); brand, venue and attraction land in brandId, venueId and attractionId, assignmentId is its id (data model DM4)",
  "description": "**What Partner Brand, Venue & Business Scope Assignment submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "tenant": {
    "type": "string",
    "description": "Tenant id"
   },
   "brand": {
    "type": "string",
    "description": "Brand id; blank = every brand of the tenant",
    "nullable": true
   },
   "venue": {
    "type": "string",
    "description": "Venue id; blank = every venue of the brand",
    "nullable": true
   },
   "attraction": {
    "type": "string",
    "description": "Attraction id; blank = every attraction of the venue",
    "nullable": true
   },
   "businessUnit": {
    "type": "string",
    "description": "Business Unit",
    "nullable": true
   },
   "eventPortfolio": {
    "type": "string",
    "description": "Event Portfolio",
    "nullable": true
   },
   "market": {
    "type": "string",
    "description": "Market",
    "nullable": true
   },
   "startDate": {
    "type": "string",
    "format": "date",
    "description": "Start Date"
   },
   "endDate": {
    "type": "string",
    "format": "date",
    "description": "End Date; a set end date makes the assignment temporary",
    "nullable": true
   },
   "seasonalScope": {
    "type": "boolean",
    "description": "Seasonal Scope: when true the start and end month-day recur every year (decided 29 September, readiness close-out)"
   },
   "assignmentId": {
    "type": "string",
    "format": "uuid",
    "description": "Assignment id; omit to create"
   },
   "partnerId": {
    "type": "string",
    "format": "uuid",
    "description": "Partner"
   },
   "authorized": {
    "type": "boolean",
    "description": "Authorized (true) or explicitly not authorized (false), the pack's Not Authorized example"
   },
   "scopeExclusions": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Scope Overrides: product or product-category ids excluded inside this scope (e.g. all Dubai Arena events except VIP Hospitality); consumed by the commercial/channel rules"
   }
  }
 },
 "PartnerBrandVenueBusinessScopeAssignmentView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over control.partner_scope_assignment (PartnerScopeAssignment) and the existing subscription state, assembled at read time (data model DM4)",
  "description": "**What Partner Brand, Venue & Business Scope Assignment displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "tenant": {
    "type": "string",
    "description": "Tenant id"
   },
   "brand": {
    "type": "string",
    "description": "Brand id; blank = every brand of the tenant",
    "nullable": true
   },
   "venue": {
    "type": "string",
    "description": "Venue id; blank = every venue of the brand",
    "nullable": true
   },
   "attraction": {
    "type": "string",
    "description": "Attraction id; blank = every attraction of the venue",
    "nullable": true
   },
   "businessUnit": {
    "type": "string",
    "description": "Business Unit",
    "nullable": true
   },
   "eventPortfolio": {
    "type": "string",
    "description": "Event Portfolio",
    "nullable": true
   },
   "market": {
    "type": "string",
    "description": "Market",
    "nullable": true
   },
   "startDate": {
    "type": "string",
    "format": "date",
    "description": "Start Date"
   },
   "endDate": {
    "type": "string",
    "format": "date",
    "description": "End Date; a set end date makes the assignment temporary",
    "nullable": true
   },
   "seasonalScope": {
    "type": "boolean",
    "description": "Seasonal Scope: when true the start and end month-day recur every year (decided 29 September, readiness close-out)"
   },
   "assignmentId": {
    "type": "string",
    "format": "uuid",
    "description": "Assignment id; omit to create"
   },
   "partnerId": {
    "type": "string",
    "format": "uuid",
    "description": "Partner"
   },
   "authorized": {
    "type": "boolean",
    "description": "Authorized (true) or explicitly not authorized (false), the pack's Not Authorized example"
   },
   "scopeExclusions": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Scope Overrides: product or product-category ids excluded inside this scope (e.g. all Dubai Arena events except VIP Hospitality); consumed by the commercial/channel rules"
   }
  }
 },
 "PartnerCapabilityGrant": {
  "type": "object",
  "x-ticvai-persistence": "control.partner_capability_grant",
  "description": "The ceiling on one capability for one partner: whether the organisation may use it, whether each use needs internal approval, and for how long. A partner user's own permissions sit inside this ceiling (decided 29 September, data model DM4)\n\n**Written by** setPartnerCapabilityGrants, which replaces the partner's ceiling as a set (decided 29 September, writers pass; DM4).",
  "required": [
   "id",
   "partnerId",
   "capability",
   "allowed",
   "grantType"
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
   "capability": {
    "type": "string",
    "enum": [
     "searchAvailability",
     "createBooking",
     "holdInventory",
     "confirmBooking",
     "cancelBooking",
     "modifyBooking",
     "rescheduleBooking",
     "downloadTicket",
     "printTicket",
     "sendTicket",
     "accessCustomerDetails",
     "useCredit",
     "usePaymentCard",
     "viewCommission",
     "viewNetRates",
     "accessReports",
     "exportData",
     "useApi",
     "createSubAgents",
     "refund",
     "manualPriceOverride",
     "creditAdjustment",
     "highValueBooking",
     "customerDataExport"
    ],
    "description": "Organisation-level capability (pack pp.16-17; refund and rescheduleBooking from MoM 31 Aug 4.3)."
   },
   "allowed": {
    "type": "boolean",
    "description": "Whether the partner may use this capability."
   },
   "requiresInternalApproval": {
    "type": "boolean",
    "default": false,
    "description": "Sensitive function: each use needs additional internal approval."
   },
   "grantType": {
    "type": "string",
    "enum": [
     "permanent",
     "temporary",
     "seasonal",
     "eventSpecific"
    ],
    "description": "How long the grant lasts."
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date",
    "nullable": true,
    "description": "Effective from."
   },
   "effectiveTo": {
    "type": "string",
    "format": "date",
    "nullable": true,
    "description": "Effective to."
   },
   "eventId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Event (catalogue.event) the grant is limited to, for an eventSpecific grant."
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
 "PartnerContact": {
  "type": "object",
  "x-ticvai-persistence": "control.partner_contact",
  "description": "A person at the partner, with or without a B2B user account. A contact with an account links to its principal (`control.partner_user` carries the branch, quota and credit); one without an account is still somebody finance or operations must be able to reach (decided 29 September, data model DM4)\n\n**Written by** setPartnerContact (create, edit, disable, enable, revoke) and by createPartnerUser, which creates the contact `invited` for a user with an account (decided 29 September, writers pass; DM4).",
  "required": [
   "id",
   "partnerId",
   "name",
   "contactType",
   "status"
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
   "name": {
    "type": "string",
    "description": "Name."
   },
   "position": {
    "type": "string",
    "nullable": true,
    "description": "Position."
   },
   "department": {
    "type": "string",
    "nullable": true,
    "description": "Department."
   },
   "email": {
    "type": "string",
    "format": "email",
    "nullable": true,
    "description": "Email."
   },
   "mobile": {
    "type": "string",
    "nullable": true,
    "description": "Mobile."
   },
   "telephone": {
    "type": "string",
    "nullable": true,
    "description": "Telephone."
   },
   "language": {
    "type": "string",
    "nullable": true,
    "description": "Language, BCP 47 tag."
   },
   "timeZone": {
    "type": "string",
    "nullable": true,
    "description": "Time zone, IANA name."
   },
   "contactType": {
    "type": "string",
    "enum": [
     "primary",
     "commercial",
     "reservations",
     "finance",
     "technical",
     "operations",
     "management",
     "emergency"
    ],
    "description": "Contact type."
   },
   "principalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Identity principal of the B2B user account (identity.principal); empty for a contact with no account."
   },
   "status": {
    "type": "string",
    "enum": [
     "invited",
     "active",
     "disabled",
     "revoked",
     "expired"
    ],
    "default": "active",
    "description": "Status; a contact with no user account is active or disabled."
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
 "PartnerContactInput": {
  "type": "object",
  "x-ticvai-persistence": "none — request only; stored as control.partner_contact (PartnerContact) (decided 29 September, writers pass; DM4)",
  "description": "What setPartnerContact submits. Without `contactId` it creates a contact with no user account; a contact who signs in is created through createPartnerUser (decided 29 September, writers pass; DM4)",
  "required": [
   "partnerId"
  ],
  "properties": {
   "contactId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The contact to change; omit to create"
   },
   "partnerId": {
    "type": "string",
    "format": "uuid",
    "description": "The partner (control.partner)"
   },
   "action": {
    "type": "string",
    "enum": [
     "save",
     "disable",
     "enable",
     "revoke"
    ],
    "default": "save",
    "description": "save creates or edits; disable, enable and revoke change access (states/partner-contact.yaml)"
   },
   "name": {
    "type": "string",
    "description": "Name; required to create"
   },
   "position": {
    "type": "string",
    "nullable": true
   },
   "department": {
    "type": "string",
    "nullable": true
   },
   "email": {
    "type": "string",
    "format": "email",
    "nullable": true
   },
   "mobile": {
    "type": "string",
    "nullable": true
   },
   "telephone": {
    "type": "string",
    "nullable": true
   },
   "language": {
    "type": "string",
    "nullable": true,
    "description": "BCP 47 tag"
   },
   "timeZone": {
    "type": "string",
    "nullable": true,
    "description": "IANA name"
   },
   "contactType": {
    "type": "string",
    "enum": [
     "primary",
     "commercial",
     "reservations",
     "finance",
     "technical",
     "operations",
     "management",
     "emergency"
    ],
    "description": "Contact type; required to create"
   }
  }
 },
 "PartnerContactsUserAdministrationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over control.partner_contact (PartnerContact) with control.partner_user and the existing subscription state, assembled at read time (data model DM4)",
  "description": "**What Partner Contacts & User Administration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
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
    "description": "Email",
    "format": "email"
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
    "description": "Language, BCP 47 tag"
   },
   "timeZone": {
    "type": "string",
    "description": "Time Zone, IANA name"
   },
   "contactType": {
    "type": "string",
    "enum": [
     "primary",
     "commercial",
     "reservations",
     "finance",
     "technical",
     "operations",
     "management",
     "emergency"
    ],
    "description": "Contact Type"
   },
   "status": {
    "type": "string",
    "description": "Status: invited, active, disabled, revoked or expired (a contact with no user account is active or disabled)"
   },
   "username": {
    "type": "string",
    "description": "Username of the B2B user account; empty for a contact with no account",
    "nullable": true
   },
   "partnerId": {
    "type": "string",
    "format": "uuid",
    "description": "Partner"
   },
   "branchScopePath": {
    "type": "string",
    "description": "Branch the user sits on, as the PartnerUser scope path",
    "nullable": true
   },
   "role": {
    "type": "string",
    "description": "Partner role, e.g. Partner Administrator, Booking Agent, Supervisor, Finance User, Reporting User, API Administrator; PartnerUser.role (control.partner_user), the grants themselves are RBAC data (decided 29 September, writers pass; DM4)",
    "nullable": true
   },
   "permissions": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Effective permissions of the user, within the partner ceiling"
   },
   "salesLocation": {
    "type": "string",
    "description": "Sales Location; PartnerUser.salesLocation (control.partner_user), empty for a contact with no account (decided 29 September, writers pass; DM4)",
    "nullable": true
   },
   "currency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "description": "Currency the user sells in; PartnerUser.currency (control.partner_user) (decided 29 September, writers pass; DM4)"
   },
   "mfaEnrolled": {
    "type": "boolean",
    "description": "MFA enrolled"
   },
   "accountExpiresAt": {
    "type": "string",
    "format": "date-time",
    "description": "Account expiry; PartnerUser.accountExpiresAt (control.partner_user) (decided 29 September, writers pass; DM4)",
    "nullable": true
   },
   "contactId": {
    "type": "string",
    "format": "uuid",
    "description": "Contact id"
   },
   "principalId": {
    "type": "string",
    "format": "uuid",
    "description": "Identity principal of the B2B user account; empty for a contact with no account",
    "nullable": true
   }
  }
 },
 "PartnerDistributionRight": {
  "type": "object",
  "x-ticvai-persistence": "control.partner_distribution_right",
  "description": "One territory, market and distribution right for a partner: where it may sell, by which methods, how exclusively and whether it may appoint sub-agents. A blank dimension means all; `allowed: false` is an explicit exclusion (decided 29 September, data model DM4)\n\n**Written by** setPartnerDistributionRights, which replaces the partner's rights as a set (decided 29 September, writers pass; DM4).",
  "required": [
   "id",
   "partnerId",
   "allowed",
   "exclusivity",
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
   "country": {
    "type": "string",
    "nullable": true,
    "description": "Country, ISO 3166-1 alpha-2; blank = all."
   },
   "region": {
    "type": "string",
    "nullable": true,
    "description": "Region; blank = all in the country."
   },
   "city": {
    "type": "string",
    "nullable": true,
    "description": "City; blank = all in the region."
   },
   "market": {
    "type": "string",
    "nullable": true,
    "description": "Market (source market the partner sells into)."
   },
   "brandId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Brand (a platform.scope node); blank = all."
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Venue; blank = all venues in scope."
   },
   "attractionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Attraction; blank = all."
   },
   "eventId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Event (catalogue.event); blank = all."
   },
   "allowed": {
    "type": "boolean",
    "description": "Allowed (true) or explicitly not allowed (false), the pack's Allowed / Not allowed example."
   },
   "distributionMethods": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "b2bPortal",
      "api",
      "otaConnection",
      "agentPortal",
      "affiliateLink",
      "voucherDistribution",
      "bulkTicketExport",
      "other"
     ]
    },
    "description": "Distribution methods this right covers."
   },
   "exclusivity": {
    "type": "string",
    "enum": [
     "nonExclusive",
     "exclusive",
     "preferred",
     "restricted"
    ],
    "description": "Exclusivity."
   },
   "subAgentRule": {
    "type": "string",
    "enum": [
     "allowed",
     "prohibited",
     "approvalRequired"
    ],
    "description": "Sub-agent rights."
   },
   "maximumHierarchyDepth": {
    "type": "integer",
    "minimum": 0,
    "nullable": true,
    "description": "Maximum hierarchy depth of sub-agents below the partner."
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
    "description": "Effective to; empty for open-ended."
   },
   "reviewDate": {
    "type": "string",
    "format": "date",
    "nullable": true,
    "description": "Review date."
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
 "PartnerDocumentationComplianceRepositoryView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over control.partner_document (PartnerDocument) and the existing subscription state, assembled at read time (data model DM4)",
  "description": "**What Partner Documentation & Compliance Repository displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "documentType": {
    "type": "string",
    "description": "Document Type code from the configurable list, seeded with tradeLicence, taxVatCertificate, commercialRegistration, bankDetails, insurance, signedAgreement, nda, apiAgreement, complianceDocument, authorizedSignatoryId, other"
   },
   "documentNumber": {
    "type": "string",
    "description": "Document Number"
   },
   "expiryDate": {
    "type": "string",
    "format": "date",
    "description": "Expiry Date",
    "nullable": true
   },
   "issuingAuthority": {
    "type": "string",
    "description": "Issuing Authority"
   },
   "fileRef": {
    "type": "string",
    "description": "Stored file reference",
    "nullable": true
   },
   "verificationStatus": {
    "type": "string",
    "description": "Verification Status: missing, uploaded, underReview, verified, rejected, expiring or expired"
   },
   "verifiedBy": {
    "type": "string",
    "description": "Verified By: staff display name",
    "nullable": true
   },
   "verificationDate": {
    "type": "string",
    "format": "date-time",
    "description": "Verification Date",
    "nullable": true
   },
   "notes": {
    "type": "string",
    "description": "Notes"
   },
   "documentId": {
    "type": "string",
    "format": "uuid",
    "description": "Document id"
   },
   "partnerId": {
    "type": "string",
    "format": "uuid",
    "description": "Partner"
   },
   "issueDate": {
    "type": "string",
    "format": "date",
    "description": "Issue Date",
    "nullable": true
   },
   "mandatory": {
    "type": "boolean",
    "description": "Whether this document type is mandatory for the partner type"
   },
   "daysToExpiry": {
    "type": "integer",
    "description": "Days until expiry; negative once expired",
    "nullable": true
   },
   "expiryAction": {
    "type": "string",
    "enum": [
     "warnOnly",
     "blockNewBookings",
     "blockCreditTransactions",
     "suspendPartner",
     "requireManualReview"
    ],
    "description": "Compliance Rules: what expiry or absence of this document does"
   },
   "aiInsights": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Advisory AI findings from the uploaded file (extracted fields, missing or inconsistent information)"
   }
  }
 },
 "PartnerManagementCommandCenterSummary": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection; the headline tiles over the list, computed at read time for the filters in force",
  "description": "**The headline figures on Partner Management Command Center.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.",
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
    "description": "Expiring Agreements: partners whose active agreement ends within its expiryAlertDays (default 30) (decided 29 September, readiness close-out)"
   },
   "documentationIssues": {
    "type": "integer",
    "description": "Documentation Issues: partners with a mandatory document missing, rejected, expiring or expired"
   },
   "partnersWithCreditHolds": {
    "type": "integer",
    "description": "Partners With Credit Holds: partners whose credit status is onHold or blocked"
   },
   "connectedOtaApiPartners": {
    "type": "integer",
    "description": "Connected OTA/API Partners"
   },
   "partnerSalesYtd": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Partner Sales YTD: gross value of partner orders this calendar year (decided 29 September, readiness close-out)"
   },
   "partnerRevenueYtd": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Partner Revenue YTD: partner sales net of commission this calendar year (decided 29 September, readiness close-out)"
   },
   "highRiskPartners": {
    "type": "integer",
    "description": "High-Risk Partners"
   }
  }
 },
 "PartnerManagementCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over control.partner (Partner), control.partner_credit_profile, control.partner_application, control.partner_scope_assignment and control.partner_distribution_right and the existing subscription state, assembled at read time (data model DM4)",
  "description": "**What Partner Management Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "partnerId": {
    "type": "string",
    "format": "uuid",
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
    "description": "Partner type code from the tenant's configurable partner-type list (MoM 31 Aug 4.3: configurable category/type), seeded with the pack's p.7 list: b2bReseller, travelAgent, tourOperator, ota, corporateCustomer, hotelConcierge, destinationManagementCompany, affiliate, wholesaler, distributor, governmentPartner, schoolInstitution, apiPartner, internalGroupCompany"
   },
   "country": {
    "type": "string",
    "description": "Country, ISO 3166-1 alpha-2"
   },
   "territory": {
    "type": "string",
    "description": "Territory: summary of the authorised markets (listTerritoryMarketDistribution)"
   },
   "assignedBrands": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Assigned Brand/Venue: brand names in the partner's business scope (setPartnerBrandVenue)"
   },
   "assignedVenues": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Assigned Brand/Venue: venue names in the partner's business scope (setPartnerBrandVenue)"
   },
   "commercialOwner": {
    "type": "string",
    "description": "Commercial Owner: staff display name of the account manager"
   },
   "distributionChannel": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "b2bPortal",
      "api",
      "otaConnection",
      "agentPortal",
      "affiliateLink",
      "voucherDistribution",
      "bulkTicketExport",
      "other"
     ]
    },
    "description": "Distribution Channel: Distribution methods: b2bPortal (the TICVAI B2B portal), api (partner consumes the TICVAI API), otaConnection (TICVAI integrates into the OTA, either direction per MoM 31 Aug 4.3), agentPortal, affiliateLink, voucherDistribution, bulkTicketExport (pre-generated QR tickets as CSV, MoM 5 Aug option 3), other"
   },
   "accountStatus": {
    "type": "string",
    "description": "Account Status: lead, applicant, underReview, approved, configuration, active, restricted, suspended, terminated or archived (pack p.6 and p.18 merged with MoM 31 Aug 4.3 lead -> submitted -> active -> suspended; \"submitted\" is applicant)"
   },
   "onboardingStatus": {
    "type": "string",
    "description": "Onboarding Status: the application stage (application, businessVerification, documentation, commercialReview, financeReview, technicalReview, approval, configuration, activation) or complete"
   },
   "agreementStatus": {
    "allOf": [
     {
      "$ref": "#/components/schemas/PartnerAgreementStatus"
     }
    ],
    "nullable": true,
    "description": "Agreement Status of the partner's current agreement; empty when none"
   },
   "creditStatus": {
    "type": "string",
    "description": "Credit Status: notEnabled, withinLimit, warning (at the warning threshold), highRisk, onHold or blocked (decided 29 September, readiness close-out)"
   },
   "integrationStatus": {
    "type": "string",
    "enum": [
     "none",
     "testing",
     "connected",
     "degraded",
     "disconnected"
    ],
    "x-ticvai-persisted": false,
    "description": "Integration Status: none, testing, connected, degraded or disconnected (decided 29 September, readiness close-out). **Derived at read time, not a column** (decided 29 September, writers pass; DM4), from the partner's OTA/API channel listings (control.channel_listing) and the health of its API clients (control.api_client, with webhook deliveries in control.webhook_delivery), first match wins: `none` when the partner has no channel listing and no API client; `disconnected` when every listing is `paused` or `delisted` or every production API client is `suspended` or `revoked`; `degraded` when a `live` listing's `lastPushedAt` is older than twice its `pushIntervalMinutes`, or webhook deliveries to the partner failed in the last hour; `connected` when a `live` listing or an `active` production client exists and none of the above holds; otherwise `testing` (only `draft` listings or only sandbox clients). The thresholds are proposed, the venue may correct them."
   },
   "lastActivity": {
    "type": "string",
    "format": "date-time",
    "description": "Last Activity"
   },
   "riskRating": {
    "type": "string",
    "enum": [
     "low",
     "medium",
     "high",
     "critical"
    ],
    "description": "Risk rating, Low / Medium / High / Critical (pack p.58); drives the Risk filter and the High-Risk Partners KPI"
   },
   "aiInsights": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Partner Attention Required: advisory AI flags such as an agreement expiring against forward bookings (pack p.6)"
   }
  }
 },
 "PartnerOnboardingApplicationWorkflowView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over control.partner_application + control.partner_application_review_task (PartnerApplication) and the existing subscription state, assembled at read time (data model DM4)",
  "description": "**What Partner Onboarding & Application Workflow displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "companyName": {
    "type": "string",
    "description": "Company legal name as applied"
   },
   "requestedPartnerType": {
    "type": "string",
    "description": "Requested partner type code (see partnerType)"
   },
   "markets": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Markets the applicant wants to sell into"
   },
   "expectedSalesVolume": {
    "type": "integer",
    "description": "Expected sales volume, tickets per year"
   },
   "requestedProducts": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Requested products"
   },
   "requestedVenues": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Requested venues"
   },
   "preferredDistributionMethod": {
    "type": "string",
    "enum": [
     "b2bPortal",
     "api",
     "otaConnection",
     "agentPortal",
     "affiliateLink",
     "voucherDistribution",
     "bulkTicketExport",
     "other"
    ],
    "description": "Preferred distribution method. Distribution methods: b2bPortal (the TICVAI B2B portal), api (partner consumes the TICVAI API), otaConnection (TICVAI integrates into the OTA, either direction per MoM 31 Aug 4.3), agentPortal, affiliateLink, voucherDistribution, bulkTicketExport (pre-generated QR tickets as CSV, MoM 5 Aug option 3), other"
   },
   "estimatedAnnualBusiness": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Estimated annual business value"
   },
   "contactName": {
    "type": "string",
    "description": "Applicant contact name"
   },
   "billingRequirements": {
    "type": "string",
    "description": "Billing requirements as stated by the applicant"
   },
   "businessCase": {
    "type": "string",
    "description": "Commercial review: business case"
   },
   "territory": {
    "type": "string",
    "description": "Commercial review: territory"
   },
   "creditRequest": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Finance review: requested credit limit"
   },
   "paymentTerms": {
    "type": "string",
    "description": "Finance review: requested payment terms"
   },
   "taxRegistrationNumber": {
    "type": "string",
    "description": "Finance review: tax/VAT registration number"
   },
   "productRequirements": {
    "type": "string",
    "description": "Operations review: product requirements"
   },
   "fulfillmentRequirements": {
    "type": "string",
    "description": "Operations review: fulfilment requirements"
   },
   "apiIntegrationRequirements": {
    "type": "string",
    "description": "Technical review: API/integration requirements"
   },
   "applicationId": {
    "type": "string",
    "format": "uuid",
    "description": "Application id"
   },
   "partnerId": {
    "type": "string",
    "format": "uuid",
    "description": "Partner record created on submission (lifecycle applicant)",
    "nullable": true
   },
   "contactEmail": {
    "type": "string",
    "description": "Applicant contact email",
    "format": "email"
   },
   "stage": {
    "type": "string",
    "enum": [
     "application",
     "businessVerification",
     "documentation",
     "commercialReview",
     "financeReview",
     "technicalReview",
     "approval",
     "configuration",
     "activation"
    ],
    "description": "Current onboarding stage (pack p.9 Onboarding Workflow)"
   },
   "status": {
    "type": "string",
    "description": "Application status: submitted, inReview, moreInformationRequested, approved, rejected or withdrawn"
   },
   "submittedAt": {
    "type": "string",
    "format": "date-time",
    "description": "Submitted at"
   },
   "slaDueAt": {
    "type": "string",
    "format": "date-time",
    "description": "When the current stage breaches its SLA",
    "nullable": true
   },
   "reviewTasks": {
    "type": "array",
    "description": "Internal Review: the task each department receives",
    "items": {
     "type": "object",
     "properties": {
      "department": {
       "type": "string",
       "enum": [
        "commercial",
        "finance",
        "operations",
        "technical"
       ]
      },
      "assignee": {
       "type": "string"
      },
      "dueAt": {
       "type": "string",
       "format": "date-time"
      },
      "completed": {
       "type": "boolean"
      }
     }
    }
   },
   "aiSummary": {
    "type": "string",
    "description": "Advisory AI summary of the application (pack p.10)",
    "nullable": true
   }
  }
 },
 "PartnerOperationsCommandCenterSummary": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection; the headline tiles over the list, computed at read time for the filters in force",
  "description": "**The headline figures on Partner Operations Command Center.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.",
  "properties": {
   "partnerSalesToday": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Partner Sales Today"
   },
   "partnerSalesMtd": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Partner Sales MTD"
   },
   "activePartnerOrders": {
    "type": "integer",
    "description": "Active Partner Orders"
   },
   "activeReservations": {
    "type": "integer",
    "description": "Active Reservations"
   },
   "activeHolds": {
    "type": "integer",
    "description": "Active Holds"
   },
   "ticketsSold": {
    "type": "integer",
    "description": "Tickets Sold"
   },
   "cancellations": {
    "type": "integer",
    "description": "Cancellations"
   },
   "refunds": {
    "type": "integer",
    "description": "Refunds"
   },
   "outstandingReceivables": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Outstanding Receivables"
   },
   "commissionPayable": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Commission Payable"
   },
   "pendingSettlements": {
    "type": "integer",
    "description": "Pending Settlements"
   },
   "operationalExceptions": {
    "type": "integer",
    "description": "Operational Exceptions"
   },
   "partnersRequiringAttention": {
    "type": "integer",
    "description": "Partners Requiring Attention"
   },
   "activityFeed": {
    "type": "array",
    "description": "Activity Feed: recent partner events, newest first",
    "items": {
     "type": "object",
     "properties": {
      "at": {
       "type": "string",
       "format": "date-time"
      },
      "partnerId": {
       "type": "string",
       "format": "uuid"
      },
      "message": {
       "type": "string"
      }
     }
    }
   }
  }
 },
 "PartnerOperationsCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over subscription state, assembled at read time from tables that already exist",
  "description": "**What Partner Operations Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "partner": {
    "type": "string",
    "description": "Partner trading name"
   },
   "partnerType": {
    "type": "string",
    "description": "Partner Type code"
   },
   "accountManager": {
    "type": "string",
    "description": "Account Manager"
   },
   "orders": {
    "type": "integer",
    "description": "Orders"
   },
   "tickets": {
    "type": "integer",
    "description": "Tickets"
   },
   "grossSales": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Gross Sales"
   },
   "netSales": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Net Sales"
   },
   "commission": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Commission"
   },
   "outstandingBalance": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Outstanding Balance"
   },
   "creditUtilization": {
    "type": "number",
    "description": "Credit Utilization, percent"
   },
   "allocationUtilization": {
    "type": "number",
    "description": "Allocation Utilization, percent"
   },
   "cancellationRate": {
    "type": "number",
    "description": "Cancellation Rate, percent"
   },
   "operationalStatus": {
    "type": "string",
    "description": "Operational Status: normal, attention, restricted, suspended"
   },
   "risk": {
    "type": "string",
    "enum": [
     "low",
     "medium",
     "high",
     "critical"
    ],
    "description": "Risk"
   },
   "partnerId": {
    "type": "string",
    "format": "uuid",
    "description": "Partner"
   },
   "aiInsights": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Advisory AI attention flags for this partner"
   }
  }
 },
 "PartnerProfileOrganizationSetupInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; stored as control.partner (Partner); accountManager and the other owners land in the *PrincipalId columns (data model DM4)",
  "description": "**What Partner Profile & Organization Setup submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "partnerId": {
    "type": "string",
    "format": "uuid",
    "description": "Partner ID; omit to create a new partner"
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
    "description": "Partner type code from the tenant's configurable partner-type list (MoM 31 Aug 4.3: configurable category/type), seeded with the pack's p.7 list: b2bReseller, travelAgent, tourOperator, ota, corporateCustomer, hotelConcierge, destinationManagementCompany, affiliate, wholesaler, distributor, governmentPartner, schoolInstitution, apiPartner, internalGroupCompany"
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
    "description": "Country, ISO 3166-1 alpha-2"
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
    "description": "Website",
    "format": "uri"
   },
   "mainTelephone": {
    "type": "string",
    "description": "Main Telephone"
   },
   "generalEmail": {
    "type": "string",
    "description": "General Email",
    "format": "email"
   },
   "preferredLanguage": {
    "type": "string",
    "description": "Preferred Language, BCP 47 tag"
   },
   "defaultCurrency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "description": "Default Currency, ISO 4217"
   },
   "timeZone": {
    "type": "string",
    "description": "Time Zone, IANA name"
   },
   "accountManager": {
    "type": "string",
    "format": "uuid",
    "description": "Account Manager: staff principal id"
   },
   "commercialManager": {
    "type": "string",
    "format": "uuid",
    "description": "Commercial Manager: staff principal id"
   },
   "financeOwner": {
    "type": "string",
    "format": "uuid",
    "description": "Finance Owner: staff principal id"
   },
   "operationalOwner": {
    "type": "string",
    "format": "uuid",
    "description": "Operational Owner: staff principal id"
   },
   "technicalOwner": {
    "type": "string",
    "format": "uuid",
    "description": "Technical Owner: staff principal id"
   },
   "parentPartnerId": {
    "type": "string",
    "format": "uuid",
    "description": "Parent partner in the hierarchy; empty for a top-level partner",
    "nullable": true
   },
   "classificationTags": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "strategic",
      "keyAccount",
      "standard",
      "newPartner",
      "highVolume",
      "vip",
      "restricted"
     ]
    },
    "description": "Account Classification: internal tags"
   }
  }
 },
 "PartnerProfileOrganizationSetupView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over control.partner (Partner) and the existing subscription state, assembled at read time (data model DM4)",
  "description": "**What Partner Profile & Organization Setup displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "partnerId": {
    "type": "string",
    "format": "uuid",
    "description": "Partner ID; server-assigned"
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
    "description": "Partner type code from the tenant's configurable partner-type list (MoM 31 Aug 4.3: configurable category/type), seeded with the pack's p.7 list: b2bReseller, travelAgent, tourOperator, ota, corporateCustomer, hotelConcierge, destinationManagementCompany, affiliate, wholesaler, distributor, governmentPartner, schoolInstitution, apiPartner, internalGroupCompany"
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
    "description": "Country, ISO 3166-1 alpha-2"
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
    "description": "Website",
    "format": "uri"
   },
   "mainTelephone": {
    "type": "string",
    "description": "Main Telephone"
   },
   "generalEmail": {
    "type": "string",
    "description": "General Email",
    "format": "email"
   },
   "preferredLanguage": {
    "type": "string",
    "description": "Preferred Language, BCP 47 tag"
   },
   "defaultCurrency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "description": "Default Currency, ISO 4217"
   },
   "timeZone": {
    "type": "string",
    "description": "Time Zone, IANA name"
   },
   "accountManager": {
    "type": "string",
    "format": "uuid",
    "description": "Account Manager: staff principal id"
   },
   "commercialManager": {
    "type": "string",
    "format": "uuid",
    "description": "Commercial Manager: staff principal id"
   },
   "financeOwner": {
    "type": "string",
    "format": "uuid",
    "description": "Finance Owner: staff principal id"
   },
   "operationalOwner": {
    "type": "string",
    "format": "uuid",
    "description": "Operational Owner: staff principal id"
   },
   "technicalOwner": {
    "type": "string",
    "format": "uuid",
    "description": "Technical Owner: staff principal id"
   },
   "parentPartnerId": {
    "type": "string",
    "format": "uuid",
    "description": "Parent partner in the hierarchy (Global Partner -> UAE Entity); empty for a top-level partner",
    "nullable": true
   },
   "classificationTags": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "strategic",
      "keyAccount",
      "standard",
      "newPartner",
      "highVolume",
      "vip",
      "restricted"
     ]
    },
    "description": "Account Classification: internal tags"
   },
   "possibleDuplicates": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    },
    "description": "Advisory: partner ids the AI duplicate check matched on company details; a human decides"
   }
  }
 },
 "PartnerUser": {
  "type": "object",
  "x-ticvai-persistence": "control.partner_user",
  "description": "2.7.51, BL-075. **A partner was a flat account** — `registerPartner` created one and nothing created a user beneath it.\nThe requirement asks for Master Agency, Branch, Department and User with permissions, quotas and credit cascading down. **That is a scope tree, and `tenancy` already has one** — so this is a principal on a partner branch rather than a new hierarchy.\n**Quota and credit resolve the way configuration does: nearest ancestor wins.** A branch with no credit limit inherits the agency's, which is the behaviour a partner expects and would otherwise have to be enforced by hand.\n",
  "required": [
   "id",
   "partnerId",
   "principalId",
   "branchScopePath"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "partnerId": {
    "x-ticvai-references": "control.partner",
    "type": "string",
    "format": "uuid",
    "description": "The partner (control.partner) the user belongs to. **Resolves to control.partner**, not to control.partner_agreement as the naming convention guessed before the partner master existed (decided 29 September, writers pass; DM4)"
   },
   "principalId": {
    "type": "string",
    "format": "uuid"
   },
   "role": {
    "type": "string",
    "nullable": true,
    "description": "The partner role shown for the user: Partner Administrator, Booking Agent, Supervisor, Finance User, Reporting User or API Administrator (pack p.12). The permissions the role grants stay RBAC data in identity; this is the label listPartnerContactUser shows (decided 29 September, writers pass; DM4)"
   },
   "salesLocation": {
    "type": "string",
    "nullable": true,
    "description": "The sales location (branch office or desk) the user sells from, shown on listPartnerContactUser (decided 29 September, writers pass; DM4)"
   },
   "currency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "nullable": true,
    "description": "Currency the user sells in, ISO 4217; empty means the agreement's settlementCurrency (decided 29 September, writers pass; DM4)"
   },
   "accountExpiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "When the user's account expires; empty for no expiry. An expired account cannot sign in and shows as `expired` on listPartnerContactUser (decided 29 September, writers pass; DM4)"
   },
   "branchScopePath": {
    "type": "string",
    "description": "The branch this user sits on. **An ltree, like every other scope path**, so a report at agency level rolls up its branches without anybody writing a join.\n"
   },
   "allocationQuota": {
    "type": "integer",
    "nullable": true,
    "description": "Units this branch may sell. **Null inherits the parent's**, and a quota set at branch level below the agency's is a deliberate restriction rather than an error.\n"
   },
   "creditLimitOverride": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "canManageUsers": {
    "type": "boolean",
    "default": false,
    "description": "**Partner-managed access control** — 2.7.51 asks for it, and a venue administering every travel agent's staff list is a venue doing the agency's HR.\n"
   }
  }
 },
 "TerritoryMarketDistributionRightsView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over control.partner_distribution_right (PartnerDistributionRight) and the existing subscription state, assembled at read time (data model DM4)",
  "description": "**What Territory, Market & Distribution Rights displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "country": {
    "type": "string",
    "description": "Country, ISO 3166-1 alpha-2; blank = all",
    "nullable": true
   },
   "region": {
    "type": "string",
    "description": "Region; blank = all in the country",
    "nullable": true
   },
   "city": {
    "type": "string",
    "description": "City; blank = all in the region",
    "nullable": true
   },
   "market": {
    "type": "string",
    "description": "Market (source market the partner sells into)",
    "nullable": true
   },
   "venue": {
    "type": "string",
    "description": "Venue id; blank = all venues in scope",
    "nullable": true
   },
   "attraction": {
    "type": "string",
    "description": "Attraction id",
    "nullable": true
   },
   "event": {
    "type": "string",
    "description": "Event id",
    "nullable": true
   },
   "brand": {
    "type": "string",
    "description": "Brand id",
    "nullable": true
   },
   "maximumHierarchyDepth": {
    "type": "integer",
    "description": "Maximum hierarchy depth of sub-agents below the partner",
    "nullable": true
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
   "rightId": {
    "type": "string",
    "format": "uuid",
    "description": "Distribution right id"
   },
   "partnerId": {
    "type": "string",
    "format": "uuid",
    "description": "Partner"
   },
   "allowed": {
    "type": "boolean",
    "description": "Allowed (true) or explicitly not allowed (false), the pack's Allowed / Not allowed example"
   },
   "distributionMethods": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "b2bPortal",
      "api",
      "otaConnection",
      "agentPortal",
      "affiliateLink",
      "voucherDistribution",
      "bulkTicketExport",
      "other"
     ]
    },
    "description": "Distribution Rights: Distribution methods: b2bPortal (the TICVAI B2B portal), api (partner consumes the TICVAI API), otaConnection (TICVAI integrates into the OTA, either direction per MoM 31 Aug 4.3), agentPortal, affiliateLink, voucherDistribution, bulkTicketExport (pre-generated QR tickets as CSV, MoM 5 Aug option 3), other"
   },
   "exclusivity": {
    "type": "string",
    "enum": [
     "nonExclusive",
     "exclusive",
     "preferred",
     "restricted"
    ],
    "description": "Exclusivity"
   },
   "subAgentRule": {
    "type": "string",
    "enum": [
     "allowed",
     "prohibited",
     "approvalRequired"
    ],
    "description": "Sub-Agent Rights"
   },
   "reviewDate": {
    "type": "string",
    "format": "date",
    "description": "Review Date",
    "nullable": true
   },
   "validationIssues": {
    "type": "array",
    "description": "Conflict Detection: e.g. two partners exclusive for the same market and period",
    "items": {
     "type": "object",
     "properties": {
      "code": {
       "type": "string",
       "enum": [
        "overlappingExclusiveRight",
        "outsideBusinessScope"
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
