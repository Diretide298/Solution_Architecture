# WS37 — Pricing   Revenue Management board 4

**10 screens · 10 operations · 13 schemas · 2 permissions**

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
  `PRODUCT_CONFIGURE, PRODUCT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **0 of these operations work offline**
  
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-078` | Pricing Governance Command Center | listDetail | 1 | 0 | — |
| `ADM-079` | Pricing Change Request & Workspace | configEditor | 1 | 0 | — |
| `ADM-080` | Bulk Pricing Update, Import & Mass Maintenance | listDetail | 1 | 0 | — |
| `ADM-081` | Pricing Version & Baseline Management | listDetail | 1 | 0 | — |
| `ADM-082` | Pricing Change Impact Analysis | listDetail | 1 | 0 | — |
| `ADM-083` | Pricing Approval Workflow & Authority Matrix | configEditor | 1 | 0 | — |
| `ADM-084` | Pricing Publication & Effective-Date Scheduler | configEditor | 1 | 0 | — |
| `ADM-085` | Pricing Distribution, Synchronization & Publication Monitor | listDetail | 1 | 0 | — |
| `ADM-086` | Pricing Rollback & Emergency Control Center | listDetail | 1 | 0 | — |
| `ADM-087` | Pricing History, Audit & Compliance Explorer | listDetail | 1 | 0 | — |

## Thin screens in this batch

**ADM-081, ADM-082, ADM-085, ADM-087 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-078",
  "name": "Pricing Governance Command Center",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "4",
   "number": "10.4.1",
   "page": 57
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/pricing-governance-command-center-adm-078",
   "component": "apps/ticvai-web/src/routes/commercial/PricingGovernanceCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-079",
    "ADM-080",
    "ADM-081",
    "ADM-082",
    "ADM-083",
    "ADM-084",
    "ADM-085",
    "ADM-086",
    "ADM-087"
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
     "to": "ADM-079",
     "trigger": "Works in Pricing Change Request & Workspace",
     "provenance": "flow F146 step 1→2",
     "operation": "listPricingGovernance"
    },
    {
     "to": "ADM-080",
     "trigger": "Works in Bulk Pricing Update, Import & Mass Maintenance",
     "provenance": "flow F146 step 3→4",
     "operation": "listPricingGovernance"
    },
    {
     "to": "ADM-081",
     "trigger": "Works in Pricing Version & Baseline Management",
     "provenance": "flow F146 step 5→6",
     "operation": "listPricingGovernance"
    },
    {
     "to": "ADM-082",
     "trigger": "Works in Pricing Change Impact Analysis",
     "provenance": "flow F146 step 7→8",
     "operation": "listPricingGovernance"
    },
    {
     "to": "ADM-083",
     "trigger": "Works in Pricing Approval Workflow & Authority Matrix",
     "provenance": "flow F146 step 9→10",
     "operation": "listPricingGovernance"
    },
    {
     "to": "ADM-084",
     "trigger": "Works in Pricing Publication & Effective-Date Scheduler",
     "provenance": "flow F146 step 11→12",
     "operation": "listPricingGovernance"
    },
    {
     "to": "ADM-085",
     "trigger": "Works in Pricing Distribution, Synchronization & Publication Monitor",
     "provenance": "flow F146 step 13→14",
     "operation": "listPricingGovernance"
    },
    {
     "to": "ADM-086",
     "trigger": "Works in Pricing Rollback & Emergency Control Center",
     "provenance": "flow F146 step 15→16",
     "operation": "listPricingGovernance"
    },
    {
     "to": "ADM-087",
     "trigger": "Works in Pricing History, Audit & Compliance Explorer",
     "provenance": "flow F146 step 17→18",
     "operation": "listPricingGovernance"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide Commercial, Revenue, Finance, and authorized management with one operational view of all pricing changes and governance activities.",
  "purposeNote": "Authorized administrators can monitor and control the complete pricing-change lifecycle from a centralized governance workspace.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 7 actions on this screen and the screen declares 1 operation.** Unserved: Create Pricing Change, Bulk Update, Import Changes, Review Impact, Approve, Schedule Publication, View Rollbacks. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 57 §Quick Actions"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search pricing governance",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 57 §Filter by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Price List",
        "Product",
        "Venue",
        "Market",
        "Channel",
        "Legal Entity",
        "Change Type",
        "Owner",
        "Approver",
        "Risk",
        "Status",
        "Effective Date"
       ],
       "notes": "The pack filters this screen by price list, product, venue, market, channel, legal entity and 6 more — which are present is a decision the pack already made.",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 57 §Filter by"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every pricing governance",
       "columns": [
        "PricingGovernanceCommandCenterView.pricingChangesInDraft",
        "PricingGovernanceCommandCenterView.pendingValidation",
        "PricingGovernanceCommandCenterView.pendingApproval",
        "PricingGovernanceCommandCenterView.approvedChanges",
        "PricingGovernanceCommandCenterView.scheduledPublications",
        "PricingGovernanceCommandCenterView.publishedToday",
        "PricingGovernanceCommandCenterView.failedPublications",
        "PricingGovernanceCommandCenterView.emergencyChanges",
        "PricingGovernanceCommandCenterView.rollbacks",
        "PricingGovernanceCommandCenterView.expiringPrices",
        "PricingGovernanceCommandCenterView.governanceExceptions",
        "PricingGovernanceCommandCenterView.highRiskChanges"
       ],
       "bindsTo": "PricingGovernanceCommandCenterView",
       "operation": "listPricingGovernance",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 57 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected pricing governance",
       "bindsTo": "PricingGovernanceCommandCenterView",
       "columns": [
        "PricingGovernanceCommandCenterView.pricingChangesInDraft",
        "PricingGovernanceCommandCenterView.pendingValidation",
        "PricingGovernanceCommandCenterView.pendingApproval",
        "PricingGovernanceCommandCenterView.approvedChanges",
        "PricingGovernanceCommandCenterView.scheduledPublications",
        "PricingGovernanceCommandCenterView.publishedToday",
        "PricingGovernanceCommandCenterView.failedPublications",
        "PricingGovernanceCommandCenterView.emergencyChanges",
        "PricingGovernanceCommandCenterView.rollbacks",
        "PricingGovernanceCommandCenterView.expiringPrices",
        "PricingGovernanceCommandCenterView.governanceExceptions",
        "PricingGovernanceCommandCenterView.highRiskChanges"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Change Scope Impact Status”, “VAT Update UAE Finance Scheduled”.",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 57 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create Pricing Change",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 57 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Bulk Update",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 57 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Import Changes",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 57 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Review Impact",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 57 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Approve",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 57 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Schedule Publication",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 57 §Quick Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "View Rollbacks",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 57 §Quick Actions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The pricing governance list.",
   "error": "Could not load. Names which read failed and leaves the pricing governance untouched.",
   "emptyFirstRun": "No pricing governance yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the pricing governance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPricingGovernance",
    "contract": "catalogue",
    "purpose": "Pricing Governance Command Center",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "PricingGovernanceCommandCenterView.pricingChangesInDraft",
    "PricingGovernanceCommandCenterView.pendingValidation",
    "PricingGovernanceCommandCenterView.pendingApproval",
    "PricingGovernanceCommandCenterView.approvedChanges",
    "PricingGovernanceCommandCenterView.scheduledPublications",
    "PricingGovernanceCommandCenterView.publishedToday"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-078"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 57. 12 of 24 labels bound to a contract property; 31 of 47 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-079",
  "name": "Pricing Change Request & Workspace",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "4",
   "number": "10.4.2",
   "page": 58
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/pricing-change-request-workspace-adm-079",
   "component": "apps/ticvai-web/src/routes/commercial/PricingChangeRequestWorkspace.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-078"
   ],
   "exitTo": [
    "ADM-078"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-078, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-078",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F146 step 2→3",
     "operation": "setPricingChangeRequest"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population",
  "purpose": "Provide a governed workspace for creating individual or structured pricing changes before modifying production pricing.",
  "purposeNote": "All governed pricing modifications can originate from a traceable change request without directly editing live commercial configuration.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 8 actions on this screen and the screen declares 1 operation.** Unserved: Price Change, Price List Change, Eligibility Rule Change, Tax Change, Fee Change, Formula Change, Currency/Rounding Change, Emergency Change. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 58 §Support"
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
       "label": "Change ID",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 58 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Change Name",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 58 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Change Type",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 58 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Business Reason",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 58 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Requested By",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 58 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Owner",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 58 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Business Unit",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 58 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Legal Entity",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 58 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Market",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 58 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 58 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Effective Date",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 58 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Expiry Date",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 58 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Priority",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 58 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Supporting Notes",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 58 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Attachments",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 58 §Capture"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Price Change",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 58 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Price List Change",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 58 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Eligibility Rule Change",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 58 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Tax Change",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 58 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Fee Change",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 58 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Formula Change",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 58 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Currency/Rounding Change",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 58 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Emergency Change",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 58 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The pricing change request configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the pricing change request untouched.",
   "emptyFirstRun": "No pricing change request configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setPricingChangeRequest",
    "contract": "catalogue",
    "purpose": "Pricing Change Request & Workspace",
    "trigger": "onAction",
    "invalidates": [
     "setPricingChangeRequest"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-079"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 58. 0 of 0 labels bound to a contract property; 23 of 46 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-080",
  "name": "Bulk Pricing Update, Import & Mass Maintenance",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "4",
   "number": "10.4.3",
   "page": 60
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/bulk-pricing-update-import-mass-maintenance-adm-080",
   "component": "apps/ticvai-web/src/routes/commercial/BulkPricingUpdateImportMassMaintenance.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-078"
   ],
   "exitTo": [
    "ADM-078"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-078, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-078",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F146 step 4→5",
     "operation": "listBulkPricingUpdate"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Allow large pricing portfolios to be updated efficiently without manually editing hundreds or thousands of records.",
  "purposeNote": "Large-scale pricing changes can be safely prepared, validated, previewed, and submitted through controlled bulk operations.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 7 actions on this screen and the screen declares 1 operation.** Unserved: Increase by %, Increase Fixed Amount, Change Currency, Clone for New Season, Increase 5%, CSV/XLSX pricing files, Price lists. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 60 §Support"
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
       "label": "Every bulk pricing update",
       "columns": [
        "BulkPricingUpdateImportMassMaintenanceView.recordsRead5420",
        "BulkPricingUpdateImportMassMaintenanceView.valid5371",
        "BulkPricingUpdateImportMassMaintenanceView.warnings37",
        "BulkPricingUpdateImportMassMaintenanceView.errors12"
       ],
       "bindsTo": "BulkPricingUpdateImportMassMaintenanceView",
       "operation": "listBulkPricingUpdate",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 60 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected bulk pricing update",
       "bindsTo": "BulkPricingUpdateImportMassMaintenanceView",
       "columns": [
        "BulkPricingUpdateImportMassMaintenanceView.recordsRead5420",
        "BulkPricingUpdateImportMassMaintenanceView.valid5371",
        "BulkPricingUpdateImportMassMaintenanceView.warnings37",
        "BulkPricingUpdateImportMassMaintenanceView.errors12"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Preview”, “Before committing”, “Export”.",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 60 §Show"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Increase by %",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 60 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Increase Fixed Amount",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 60 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Change Currency",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 60 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Clone for New Season",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 60 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Increase 5%",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 60 §Action"
      },
      {
       "kind": "secondaryButton",
       "label": "CSV/XLSX pricing files",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 60 §Support controlled import of"
      },
      {
       "kind": "secondaryButton",
       "label": "Price lists",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 60 §Support controlled import of"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The bulk pricing update list.",
   "error": "Could not load. Names which read failed and leaves the bulk pricing update untouched.",
   "emptyFirstRun": "No bulk pricing update yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the bulk pricing update are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listBulkPricingUpdate",
    "contract": "catalogue",
    "purpose": "Bulk Pricing Update, Import & Mass Maintenance",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "BulkPricingUpdateImportMassMaintenanceView.recordsRead5420",
    "BulkPricingUpdateImportMassMaintenanceView.valid5371",
    "BulkPricingUpdateImportMassMaintenanceView.warnings37",
    "BulkPricingUpdateImportMassMaintenanceView.errors12"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-080"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 60. 4 of 4 labels bound to a contract property; 22 of 49 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-081",
  "name": "Pricing Version & Baseline Management",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "4",
   "number": "10.4.4",
   "page": 62
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/pricing-version-baseline-management-adm-081",
   "component": "apps/ticvai-web/src/routes/commercial/PricingVersionBaselineManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-078"
   ],
   "exitTo": [
    "ADM-078"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-078, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-078",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F146 step 6→7",
     "operation": "listPricingVersionBaseline"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display; Compare; Show) and no metric row",
  "purpose": "Maintain immutable versions of pricing configuration so TICVAI always knows what configuration existed at a particular time.",
  "purposeNote": "configuration was effective for any historical transaction.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every pricing version baseline",
       "columns": [
        "PricingVersionBaselineManagementView.version",
        "PricingVersionBaselineManagementView.priceList",
        "PricingVersionBaselineManagementView.createdDate",
        "PricingVersionBaselineManagementView.effectiveDate",
        "PricingVersionBaselineManagementView.createdBy",
        "PricingVersionBaselineManagementView.changeRequest",
        "PricingVersionBaselineManagementView.productCount",
        "PricingVersionBaselineManagementView.changeCount",
        "PricingVersionBaselineManagementView.status",
        "PricingVersionBaselineManagementView.version42",
        "PricingVersionBaselineManagementView.version43",
        "PricingVersionBaselineManagementView.added",
        "PricingVersionBaselineManagementView.removed",
        "PricingVersionBaselineManagementView.modified",
        "PricingVersionBaselineManagementView.unchanged"
       ],
       "bindsTo": "PricingVersionBaselineManagementView",
       "operation": "listPricingVersionBaseline",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 62 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected pricing version baseline",
       "bindsTo": "PricingVersionBaselineManagementView",
       "columns": [
        "PricingVersionBaselineManagementView.version",
        "PricingVersionBaselineManagementView.priceList",
        "PricingVersionBaselineManagementView.createdDate",
        "PricingVersionBaselineManagementView.effectiveDate",
        "PricingVersionBaselineManagementView.createdBy",
        "PricingVersionBaselineManagementView.changeRequest",
        "PricingVersionBaselineManagementView.productCount",
        "PricingVersionBaselineManagementView.changeCount",
        "PricingVersionBaselineManagementView.status",
        "PricingVersionBaselineManagementView.version42",
        "PricingVersionBaselineManagementView.version43",
        "PricingVersionBaselineManagementView.added",
        "PricingVersionBaselineManagementView.removed",
        "PricingVersionBaselineManagementView.modified",
        "PricingVersionBaselineManagementView.unchanged"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Version States”, “Differen”, “AED AED”, “Senio AED AED”, “Baseline”, “Commercial Baseline”.",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 62 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The pricing version baseline list.",
   "error": "Could not load. Names which read failed and leaves the pricing version baseline untouched.",
   "emptyFirstRun": "No pricing version baseline yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the pricing version baseline are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPricingVersionBaseline",
    "contract": "catalogue",
    "purpose": "Pricing Version & Baseline Management",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "PricingVersionBaselineManagementView.version",
    "PricingVersionBaselineManagementView.priceList",
    "PricingVersionBaselineManagementView.createdDate",
    "PricingVersionBaselineManagementView.effectiveDate",
    "PricingVersionBaselineManagementView.createdBy",
    "PricingVersionBaselineManagementView.changeRequest"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-081"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 62. 15 of 15 labels bound to a contract property; 15 of 32 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-082",
  "name": "Pricing Change Impact Analysis",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "4",
   "number": "10.4.5",
   "page": 63
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/pricing-change-impact-analysis-adm-082",
   "component": "apps/ticvai-web/src/routes/commercial/PricingChangeImpactAnalysis.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-078"
   ],
   "exitTo": [
    "ADM-078"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-078, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-078",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F146 step 8→9",
     "operation": "listPricingChangeImpact"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Analyze) and no metric row",
  "purpose": "Determine the commercial and operational consequences of a pricing change before approval and publication. This is one of the most important screens in Board 4.",
  "purposeNote": "Approvers can understand financial, customer, channel, dependency, and operational impact before authorizing a pricing change.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every pricing change impact",
       "columns": [
        "PricingChangeImpactAnalysisView.products",
        "PricingChangeImpactAnalysisView.events",
        "PricingChangeImpactAnalysisView.performances",
        "PricingChangeImpactAnalysisView.venues",
        "PricingChangeImpactAnalysisView.markets",
        "PricingChangeImpactAnalysisView.channels",
        "PricingChangeImpactAnalysisView.b2bPartners",
        "PricingChangeImpactAnalysisView.memberships",
        "PricingChangeImpactAnalysisView.packages",
        "PricingChangeImpactAnalysisView.existingReservations",
        "PricingChangeImpactAnalysisView.futureReservations",
        "PricingChangeImpactAnalysisView.apis",
        "PricingChangeImpactAnalysisView.integrations"
       ],
       "bindsTo": "PricingChangeImpactAnalysisView",
       "operation": "listPricingChangeImpact",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 63 §Analyze"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected pricing change impact",
       "bindsTo": "PricingChangeImpactAnalysisView",
       "columns": [
        "PricingChangeImpactAnalysisView.products",
        "PricingChangeImpactAnalysisView.events",
        "PricingChangeImpactAnalysisView.performances",
        "PricingChangeImpactAnalysisView.venues",
        "PricingChangeImpactAnalysisView.markets",
        "PricingChangeImpactAnalysisView.channels",
        "PricingChangeImpactAnalysisView.b2bPartners",
        "PricingChangeImpactAnalysisView.memberships",
        "PricingChangeImpactAnalysisView.packages",
        "PricingChangeImpactAnalysisView.existingReservations",
        "PricingChangeImpactAnalysisView.futureReservations",
        "PricingChangeImpactAnalysisView.apis",
        "PricingChangeImpactAnalysisView.integrations"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Estimate”, “Proposed change”, “Affected”, “Estimated annual revenue impact”, “Show whether changes affect”, “Existing Booking Protection”.",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 63 §Analyze"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The pricing change impact list.",
   "error": "Could not load. Names which read failed and leaves the pricing change impact untouched.",
   "emptyFirstRun": "No pricing change impact yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the pricing change impact are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPricingChangeImpact",
    "contract": "catalogue",
    "purpose": "Pricing Change Impact Analysis",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "PricingChangeImpactAnalysisView.products",
    "PricingChangeImpactAnalysisView.events",
    "PricingChangeImpactAnalysisView.performances",
    "PricingChangeImpactAnalysisView.venues",
    "PricingChangeImpactAnalysisView.markets",
    "PricingChangeImpactAnalysisView.channels"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-082"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 63. 13 of 13 labels bound to a contract property; 13 of 47 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-083",
  "name": "Pricing Approval Workflow & Authority Matrix",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "4",
   "number": "10.4.6",
   "page": 64
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/pricing-approval-workflow-authority-matrix-adm-083",
   "component": "apps/ticvai-web/src/routes/commercial/PricingApprovalWorkflowAuthorityMatrix.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-078"
   ],
   "exitTo": [
    "ADM-078"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-078, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-078",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F146 step 10→11",
     "operation": "approvePricingWorkflowAuthority"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure who must approve pricing changes based on their commercial risk and scope.",
  "purposeNote": "Pricing changes cannot progress beyond their configured governance threshold without all required approvals.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Expected Approval Time",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 64 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Escalation",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 64 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Reminder",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 64 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Alternate Approver",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 64 §Configure"
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
       "provenance": "contract operation approvePricingWorkflowAuthority"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The pricing approval workflow configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the pricing approval workflow untouched.",
   "emptyFirstRun": "No pricing approval workflow configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "approvePricingWorkflowAuthority",
    "contract": "catalogue",
    "purpose": "Pricing Approval Workflow & Authority Matrix",
    "trigger": "onAction",
    "invalidates": [
     "approvePricingWorkflowAuthority"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-083"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 64. 0 of 0 labels bound to a contract property; 4 of 44 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-084",
  "name": "Pricing Publication & Effective-Date Scheduler",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "4",
   "number": "10.4.7",
   "page": 66
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/pricing-publication-effective-date-scheduler-adm-084",
   "component": "apps/ticvai-web/src/routes/commercial/PricingPublicationEffectiveDateScheduler.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-078"
   ],
   "exitTo": [
    "ADM-078"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-078, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-078",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F146 step 12→13",
     "operation": "publishPricingEffectiveDate"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the screen declares a publishing operation over fields the pack configures",
  "purpose": "Control exactly when approved pricing becomes commercially effective.",
  "purposeNote": "Only validated and fully approved pricing configurations can be scheduled and activated at controlled effective dates.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 3 actions on this screen and the screen declares 1 operation.** Unserved: Scheduled Publication, Staged Publication. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 66 §Support"
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
       "label": "1 March 02:00",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 66 §Publish Configuration"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Publish Immediately",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 66 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Scheduled Publication",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 66 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Staged Publication",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 66 §Support"
      },
      {
       "kind": "publishGate",
       "label": "What publishing changes",
       "notes": "**Names what goes live, where, and from when.** A publish with no stated consequence is one somebody presses meaning to save.",
       "provenance": "authored — required by check-screens for publishPricingEffectiveDate"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The pricing publication effective-date configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the pricing publication effective-date untouched.",
   "emptyFirstRun": "No pricing publication effective-date configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "publishPricingEffectiveDate",
    "contract": "catalogue",
    "purpose": "Pricing Publication & Effective-Date Scheduler",
    "trigger": "onAction",
    "invalidates": [
     "publishPricingEffectiveDate"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-084"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 66. 7 of 7 labels bound to a contract property; 11 of 32 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-085",
  "name": "Pricing Distribution, Synchronization & Publication Monitor",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "4",
   "number": "10.4.8",
   "page": 67
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/pricing-distribution-synchronization-publication-monitor-adm-085",
   "component": "apps/ticvai-web/src/routes/commercial/PricingDistributionSynchronizationPublicationMon.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-078"
   ],
   "exitTo": [
    "ADM-078"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-078, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-078",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F146 step 14→15",
     "operation": "listPricingDistributionSynchronization"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Monitor; Display) and no metric row",
  "purpose": "Ensure published pricing reaches every TICVAI channel and dependent system consistently.",
  "purposeNote": "Administrators can confirm that approved pricing has been successfully distributed and synchronized to all intended channels and systems.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every pricing distribution synchronization",
       "columns": [
        "PricingDistributionSynchronizationPublicationMonitorView.b2c",
        "PricingDistributionSynchronizationPublicationMonitorView.mobileApp",
        "PricingDistributionSynchronizationPublicationMonitorView.pos",
        "PricingDistributionSynchronizationPublicationMonitorView.mobilePos",
        "PricingDistributionSynchronizationPublicationMonitorView.kiosk",
        "PricingDistributionSynchronizationPublicationMonitorView.callCenter",
        "PricingDistributionSynchronizationPublicationMonitorView.b2b",
        "PricingDistributionSynchronizationPublicationMonitorView.reseller",
        "PricingDistributionSynchronizationPublicationMonitorView.ota",
        "PricingDistributionSynchronizationPublicationMonitorView.apis",
        "PricingDistributionSynchronizationPublicationMonitorView.cacheCdnWhereApplicable",
        "PricingDistributionSynchronizationPublicationMonitorView.externalIntegratedSystems",
        "PricingDistributionSynchronizationPublicationMonitorView.publicationStarted",
        "PricingDistributionSynchronizationPublicationMonitorView.lastUpdated",
        "PricingDistributionSynchronizationPublicationMonitorView.recordsPublished",
        "PricingDistributionSynchronizationPublicationMonitorView.recordsFailed",
        "PricingDistributionSynchronizationPublicationMonitorView.latency",
        "PricingDistributionSynchronizationPublicationMonitorView.targetVersion"
       ],
       "bindsTo": "PricingDistributionSynchronizationPublicationMonitorView",
       "operation": "listPricingDistributionSynchronization",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 67 §Monitor"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected pricing distribution synchronization",
       "bindsTo": "PricingDistributionSynchronizationPublicationMonitorView",
       "columns": [
        "PricingDistributionSynchronizationPublicationMonitorView.b2c",
        "PricingDistributionSynchronizationPublicationMonitorView.mobileApp",
        "PricingDistributionSynchronizationPublicationMonitorView.pos",
        "PricingDistributionSynchronizationPublicationMonitorView.mobilePos",
        "PricingDistributionSynchronizationPublicationMonitorView.kiosk",
        "PricingDistributionSynchronizationPublicationMonitorView.callCenter",
        "PricingDistributionSynchronizationPublicationMonitorView.b2b",
        "PricingDistributionSynchronizationPublicationMonitorView.reseller",
        "PricingDistributionSynchronizationPublicationMonitorView.ota",
        "PricingDistributionSynchronizationPublicationMonitorView.apis",
        "PricingDistributionSynchronizationPublicationMonitorView.cacheCdnWhereApplicable",
        "PricingDistributionSynchronizationPublicationMonitorView.externalIntegratedSystems",
        "PricingDistributionSynchronizationPublicationMonitorView.publicationStarted",
        "PricingDistributionSynchronizationPublicationMonitorView.lastUpdated",
        "PricingDistributionSynchronizationPublicationMonitorView.recordsPublished",
        "PricingDistributionSynchronizationPublicationMonitorView.recordsFailed",
        "PricingDistributionSynchronizationPublicationMonitorView.latency",
        "PricingDistributionSynchronizationPublicationMonitorView.targetVersion"
       ],
       "notes": "The pack groups this record's detail under its own headings: “For each target”, “For failed publication”, “Consistency Check”, “Alerts”.",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 67 §Monitor"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The pricing distribution synchronization list.",
   "error": "Could not load. Names which read failed and leaves the pricing distribution synchronization untouched.",
   "emptyFirstRun": "No pricing distribution synchronization yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the pricing distribution synchronization are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPricingDistributionSynchronization",
    "contract": "catalogue",
    "purpose": "Pricing Distribution, Synchronization & Publication Monitor",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "PricingDistributionSynchronizationPublicationMonitorView.b2c",
    "PricingDistributionSynchronizationPublicationMonitorView.mobileApp",
    "PricingDistributionSynchronizationPublicationMonitorView.pos",
    "PricingDistributionSynchronizationPublicationMonitorView.mobilePos",
    "PricingDistributionSynchronizationPublicationMonitorView.kiosk",
    "PricingDistributionSynchronizationPublicationMonitorView.callCenter"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-085"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 67. 18 of 18 labels bound to a contract property; 18 of 36 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-086",
  "name": "Pricing Rollback & Emergency Control Center",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "4",
   "number": "10.4.9",
   "page": 69
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/pricing-rollback-emergency-control-center-adm-086",
   "component": "apps/ticvai-web/src/routes/commercial/PricingRollbackEmergencyControlCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-078"
   ],
   "exitTo": [
    "ADM-078"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-078, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-078",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F146 step 16→17",
     "operation": "listPricingRollbackEmergency"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide controlled recovery when a pricing publication is incorrect or creates unacceptable commercial impact.",
  "purposeNote": "Authorized users can rapidly contain and reverse problematic pricing changes without altering historical transactions or losing audit traceability.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 3 actions on this screen and the screen declares 1 operation.** Unserved: Previous Price, Selected Channel, Entire Publication. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 69 §Support"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 69"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 69"
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
       "label": "Previous Price",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 69 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Selected Channel",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 69 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Entire Publication",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 69 §Support"
      },
      {
       "kind": "banner",
       "label": "Permissions this screen separates",
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** Freeze Price List, Freeze Product Pricing, Freeze Venue Pricing, Stop Scheduled Publication, Stop Distribution, Restore Last Known Good Version. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 69 §Authorized users should have"
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
   "loading": "The pricing rollback emergency list.",
   "error": "Could not load. Names which read failed and leaves the pricing rollback emergency untouched.",
   "emptyFirstRun": "No pricing rollback emergency yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the pricing rollback emergency are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPricingRollbackEmergency",
    "contract": "catalogue",
    "purpose": "Pricing Rollback & Emergency Control Center",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "PricingRollbackEmergencyControlCenterView.previousVersion",
    "PricingRollbackEmergencyControlCenterView.selectedVersion",
    "PricingRollbackEmergencyControlCenterView.previousPrice",
    "PricingRollbackEmergencyControlCenterView.commercialBaseline",
    "PricingRollbackEmergencyControlCenterView.selectedProducts"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-086"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 69. 0 of 0 labels bound to a contract property; 9 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-087",
  "name": "Pricing History, Audit & Compliance Explorer",
  "module": "Commercial",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Pricing___Revenue_Management_Reference.pdf",
   "board": "4",
   "number": "10.4.10",
   "page": 70
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/commercial/pricing-history-audit-compliance-explorer-adm-087",
   "component": "apps/ticvai-web/src/routes/commercial/PricingHistoryAuditComplianceExplorer.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-078"
   ],
   "exitTo": [
    "ADM-078"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-078, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation."
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide complete forensic traceability for every pricing configuration and change. Enable TICVAI revenue administrators to configure dynamic-pricing strategies using real-time commercial conditions such as: Demand + Occupancy + Availability + Inventory + Booking Velocity + Time-to- Event + Season + Day + Timeslot + Channel + Customer Segment + Location The engine converts those conditions into controlled price movements while always respecting commercial guardrails.",
  "purposeNote": "Every material pricing configuration, approval, publication, override, and rollback is fully traceable and can be reconstructed for operational, financial, and compliance purposes. Board 4 — Final Screen Register # Backend Screen Core Responsibility 10.4. Pricing Governance Command Center Governance operations 1 10.4. Pricing Change Request & Workspace Controlled change creation 2 10.4. Bulk Pricing Update, Import & Mass Maintenance Mass pricing operations 3 10.4. Pricing Version & Baseline Management Version control 4 10.4. Pricing Change Impact Analysis Pre-change impact 5 10.4. Pricing Appr",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 70"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search pricing history audit",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 70 §Search by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Price List",
        "Rate",
        "Product",
        "User",
        "Change Request",
        "Version",
        "Venue",
        "Market",
        "Channel",
        "Date",
        "Transaction",
        "Approval"
       ],
       "notes": "The pack filters this screen by price list, rate, product, user, change request, version and 6 more — which are present is a decision the pack already made.",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 70 §Search by"
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
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** “Who approved the Dubai summer pricing?”. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 70 §Authorized users can ask"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The pricing history audit list.",
   "error": "Could not load. Names which read failed and leaves the pricing history audit untouched.",
   "emptyFirstRun": "No pricing history audit yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the pricing history audit are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listPricingCompliance",
    "contract": "catalogue",
    "purpose": "Pricing History, Audit & Compliance Explorer",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-087"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 70. 0 of 12 labels bound to a contract property; 13 of 118 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "approvePricingWorkflowAuthority": {
  "method": "PUT",
  "path": "/pricing-workflow-authority",
  "contract": "catalogue",
  "summary": "Pricing Approval Workflow & Authority Matrix",
  "permission": "PRODUCT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "PricingApprovalWorkflowAuthorityMatrixInput",
  "responds": "PricingApprovalWorkflowAuthorityMatrixView"
 },
 "listBulkPricingUpdate": {
  "method": "GET",
  "path": "/bulk-pricing-update",
  "contract": "catalogue",
  "summary": "Bulk Pricing Update, Import & Mass Maintenance",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "BulkPricingUpdateImportMassMaintenanceView"
 },
 "listPricingChangeImpact": {
  "method": "GET",
  "path": "/pricing-change-impact",
  "contract": "catalogue",
  "summary": "Pricing Change Impact Analysis",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "PricingChangeImpactAnalysisView"
 },
 "listPricingCompliance": {
  "method": "GET",
  "path": "/pricing-compliance",
  "contract": "catalogue",
  "summary": "Pricing History, Audit & Compliance Explorer",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "priceList",
    "in": "query",
    "required": false
   },
   {
    "name": "rate",
    "in": "query",
    "required": false
   },
   {
    "name": "product",
    "in": "query",
    "required": false
   },
   {
    "name": "user",
    "in": "query",
    "required": false
   },
   {
    "name": "changeRequest",
    "in": "query",
    "required": false
   },
   {
    "name": "version",
    "in": "query",
    "required": false
   },
   {
    "name": "venue",
    "in": "query",
    "required": false
   },
   {
    "name": "market",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "PricingHistoryAuditComplianceExplorerView"
 },
 "listPricingDistributionSynchronization": {
  "method": "GET",
  "path": "/pricing-distribution-synchronization",
  "contract": "catalogue",
  "summary": "Pricing Distribution, Synchronization & Publication Monitor",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "PricingDistributionSynchronizationPublicationMonitorView"
 },
 "listPricingGovernance": {
  "method": "GET",
  "path": "/pricing-governance",
  "contract": "catalogue",
  "summary": "Pricing Governance Command Center",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "priceList",
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
    "name": "legalEntity",
    "in": "query",
    "required": false
   },
   {
    "name": "changeType",
    "in": "query",
    "required": false
   },
   {
    "name": "owner",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "PricingGovernanceCommandCenterView"
 },
 "listPricingRollbackEmergency": {
  "method": "GET",
  "path": "/pricing-rollback-emergency",
  "contract": "catalogue",
  "summary": "Pricing Rollback & Emergency Control Center",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "PricingRollbackEmergencyControlCenterView"
 },
 "listPricingVersionBaseline": {
  "method": "GET",
  "path": "/pricing-version-baseline",
  "contract": "catalogue",
  "summary": "Pricing Version & Baseline Management",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "PricingVersionBaselineManagementView"
 },
 "publishPricingEffectiveDate": {
  "method": "PUT",
  "path": "/pricing-effective-date",
  "contract": "catalogue",
  "summary": "Pricing Publication & Effective-Date Scheduler",
  "permission": "PRODUCT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "PricingPublicationEffectiveDateSchedulerInput",
  "responds": "PricingPublicationEffectiveDateSchedulerView"
 },
 "setPricingChangeRequest": {
  "method": "PUT",
  "path": "/pricing-change-request",
  "contract": "catalogue",
  "summary": "Pricing Change Request & Workspace",
  "permission": "PRODUCT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "PricingChangeRequestWorkspaceInput",
  "responds": "PricingChangeRequestWorkspaceView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "BulkPricingUpdateImportMassMaintenanceView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Bulk Pricing Update, Import & Mass Maintenance displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "byType": {
    "type": "string",
    "enum": [
     "priceList",
     "product",
     "productFamily",
     "category",
     "venue",
     "market",
     "currency",
     "rateType",
     "channel",
     "effectivePeriod"
    ],
    "description": "Vocabulary listed under Select by."
   },
   "increaseBy": {
    "type": "number",
    "description": "Increase by %"
   },
   "decreaseBy": {
    "type": "number",
    "description": "Decrease by %"
   },
   "increaseFixedAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Increase Fixed Amount"
   },
   "decreaseFixedAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Decrease Fixed Amount"
   },
   "changeCurrency": {
    "type": "string",
    "description": "Change Currency"
   },
   "activateDeactivate": {
    "type": "string",
    "description": "Activate/Deactivate"
   },
   "increase5": {
    "type": "number",
    "description": "Increase 5%"
   },
   "csvXlsxPricingFiles": {
    "type": "string",
    "description": "CSV/XLSX pricing files"
   },
   "priceLists": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price lists"
   },
   "rateValues": {
    "type": "number",
    "description": "Rate values"
   },
   "effectiveDates": {
    "type": "string",
    "description": "Effective dates"
   },
   "mappings": {
    "type": "string",
    "description": "Mappings"
   },
   "invalidProduct": {
    "type": "string",
    "description": "Invalid Product"
   },
   "unknownRateCode": {
    "type": "number",
    "description": "Unknown Rate Code"
   },
   "unsupportedCurrency": {
    "type": "string",
    "description": "Unsupported Currency"
   },
   "missingMandatoryField": {
    "type": "string",
    "description": "Missing Mandatory Field"
   },
   "invalidDate": {
    "type": "string",
    "format": "date-time",
    "description": "Invalid Date"
   },
   "invalidAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Invalid Amount"
   },
   "recordsRead5420": {
    "type": "string",
    "description": "Records Read: 5,420"
   },
   "valid5371": {
    "type": "string",
    "description": "Valid: 5,371"
   },
   "warnings37": {
    "type": "string",
    "description": "Warnings: 37"
   },
   "errors12": {
    "type": "integer",
    "description": "Errors: 12"
   }
  }
 },
 "PricingApprovalWorkflowAuthorityMatrixInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table covers these fields** — the closest is catalogue.channel_allocation at 4%, so this is not an update to anything the package stores today and no new table has been decided",
  "description": "**What Pricing Approval Workflow & Authority Matrix submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.\n\n**The pack defines this as a record**, under *Every approval action records* - one of only 13 drafted writes that does. That is the client writing a row rather than a screen, and it is where the table conversation should start.",
  "properties": {
   "change": {
    "type": "number",
    "description": "Change %"
   },
   "monetaryImpact": {
    "type": "string",
    "description": "Monetary Impact"
   },
   "revenueImpact": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue Impact"
   },
   "priceList": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price List"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "market": {
    "type": "string",
    "description": "Market"
   },
   "legalEntity": {
    "type": "string",
    "description": "Legal Entity"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "taxChange": {
    "type": "string",
    "description": "Tax Change"
   },
   "feeChange": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Fee Change"
   },
   "emergencyStatus": {
    "type": "string",
    "description": "Emergency Status"
   },
   "commercialDirector": {
    "type": "string",
    "description": "Commercial Director +"
   },
   "financeCompliance": {
    "type": "string",
    "description": "Finance + Compliance"
   },
   "returnForModification": {
    "type": "string",
    "description": "Return for Modification"
   },
   "requestInformation": {
    "type": "string",
    "description": "Request Information"
   },
   "delegate": {
    "type": "string",
    "description": "Delegate"
   },
   "expectedApprovalTime": {
    "type": "string",
    "format": "date-time",
    "description": "Expected Approval Time"
   },
   "escalation": {
    "type": "string",
    "description": "Escalation"
   },
   "reminder": {
    "type": "string",
    "description": "Reminder"
   },
   "alternateApprover": {
    "type": "string",
    "description": "Alternate Approver"
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
    "description": "Date/Time"
   },
   "decision": {
    "type": "string",
    "description": "Decision"
   },
   "comment": {
    "type": "string",
    "description": "Comment"
   },
   "version": {
    "type": "string",
    "description": "Version"
   }
  },
  "x-ticvai-record-definition": "Every approval action records"
 },
 "PricingApprovalWorkflowAuthorityMatrixView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Pricing Approval Workflow & Authority Matrix displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "change": {
    "type": "number",
    "description": "Change %"
   },
   "monetaryImpact": {
    "type": "string",
    "description": "Monetary Impact"
   },
   "revenueImpact": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue Impact"
   },
   "priceList": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price List"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "market": {
    "type": "string",
    "description": "Market"
   },
   "legalEntity": {
    "type": "string",
    "description": "Legal Entity"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "taxChange": {
    "type": "string",
    "description": "Tax Change"
   },
   "feeChange": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Fee Change"
   },
   "emergencyStatus": {
    "type": "string",
    "description": "Emergency Status"
   },
   "commercialDirector": {
    "type": "string",
    "description": "Commercial Director +"
   },
   "financeCompliance": {
    "type": "string",
    "description": "Finance + Compliance"
   },
   "returnForModification": {
    "type": "string",
    "description": "Return for Modification"
   },
   "requestInformation": {
    "type": "string",
    "description": "Request Information"
   },
   "delegate": {
    "type": "string",
    "description": "Delegate"
   },
   "expectedApprovalTime": {
    "type": "string",
    "format": "date-time",
    "description": "Expected Approval Time"
   },
   "escalation": {
    "type": "string",
    "description": "Escalation"
   },
   "reminder": {
    "type": "string",
    "description": "Reminder"
   },
   "alternateApprover": {
    "type": "string",
    "description": "Alternate Approver"
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
    "description": "Date/Time"
   },
   "decision": {
    "type": "string",
    "description": "Decision"
   },
   "comment": {
    "type": "string",
    "description": "Comment"
   },
   "version": {
    "type": "string",
    "description": "Version"
   }
  }
 },
 "PricingChangeImpactAnalysisView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Pricing Change Impact Analysis displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "products": {
    "type": "string",
    "description": "Products"
   },
   "events": {
    "type": "string",
    "description": "Events"
   },
   "performances": {
    "type": "string",
    "description": "Performances"
   },
   "venues": {
    "type": "string",
    "description": "Venues"
   },
   "markets": {
    "type": "string",
    "description": "Markets"
   },
   "channels": {
    "type": "string",
    "description": "Channels"
   },
   "b2bPartners": {
    "type": "string",
    "description": "B2B Partners"
   },
   "memberships": {
    "type": "string",
    "description": "Memberships"
   },
   "packages": {
    "type": "string",
    "description": "Packages"
   },
   "existingReservations": {
    "type": "string",
    "description": "Existing Reservations"
   },
   "futureReservations": {
    "type": "string",
    "description": "Future Reservations"
   },
   "apis": {
    "type": "string",
    "description": "APIs"
   },
   "integrations": {
    "type": "string",
    "description": "Integrations"
   },
   "currentRevenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Current Revenue"
   },
   "projectedRevenue": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Projected Revenue"
   },
   "averagePriceChange": {
    "type": "number",
    "description": "Average Price Change"
   },
   "maximumChange": {
    "type": "string",
    "description": "Maximum Change"
   },
   "minimumChange": {
    "type": "string",
    "description": "Minimum Change"
   },
   "marginImpact": {
    "type": "number",
    "description": "Margin Impact"
   },
   "customerExposure": {
    "type": "string",
    "description": "Customer Exposure"
   },
   "transactionVolume": {
    "type": "integer",
    "description": "Transaction Volume"
   },
   "aed34m": {
    "type": "string",
    "description": "+AED 3.4M"
   },
   "derivedRates": {
    "type": "integer",
    "description": "Derived Rates"
   },
   "contractRates": {
    "type": "integer",
    "description": "Contract Rates"
   },
   "membershipRates": {
    "type": "integer",
    "description": "Membership Rates"
   },
   "groupRates": {
    "type": "integer",
    "description": "Group Rates"
   },
   "promotions": {
    "type": "integer",
    "description": "Promotions"
   },
   "dynamicPricingGuardrails": {
    "type": "integer",
    "description": "Dynamic Pricing Guardrails"
   },
   "existingOrdersNo": {
    "type": "string",
    "description": "Existing Orders: No"
   },
   "existingReservationsNo": {
    "type": "string",
    "description": "Existing Reservations: No"
   },
   "futureUnsoldInventoryYes": {
    "type": "string",
    "description": "Future Unsold Inventory: Yes"
   },
   "basedOnConfigurableCriteria": {
    "type": "string",
    "description": "based on configurable criteria"
   }
  }
 },
 "PricingChangeRequestWorkspaceInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table covers these fields** — the closest is catalogue.entitlement_template at 3%, so this is not an update to anything the package stores today and no new table has been decided",
  "description": "**What Pricing Change Request & Workspace submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "changeId": {
    "type": "string",
    "description": "Change ID"
   },
   "changeName": {
    "type": "string",
    "description": "Change Name"
   },
   "changeType": {
    "type": "string",
    "description": "Change Type"
   },
   "businessReason": {
    "type": "string",
    "description": "Business Reason"
   },
   "requestedBy": {
    "type": "string",
    "description": "Requested By"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   },
   "businessUnit": {
    "type": "string",
    "description": "Business Unit"
   },
   "legalEntity": {
    "type": "string",
    "description": "Legal Entity"
   },
   "market": {
    "type": "string",
    "description": "Market"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
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
   "priority": {
    "type": "string",
    "description": "Priority"
   },
   "supportingNotes": {
    "type": "string",
    "description": "Supporting Notes"
   },
   "attachments": {
    "type": "string",
    "description": "Attachments"
   },
   "priceChange": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price Change"
   },
   "newRate": {
    "type": "integer",
    "description": "New Rate"
   },
   "rateRemoval": {
    "type": "number",
    "description": "Rate Removal"
   },
   "priceListChange": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price List Change"
   },
   "eligibilityRuleChange": {
    "type": "string",
    "description": "Eligibility Rule Change"
   },
   "taxChange": {
    "type": "string",
    "description": "Tax Change"
   },
   "feeChange": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Fee Change"
   },
   "formulaChange": {
    "type": "string",
    "description": "Formula Change"
   },
   "currencyRoundingChange": {
    "type": "string",
    "description": "Currency/Rounding Change"
   },
   "emergencyChange": {
    "type": "string",
    "description": "Emergency Change"
   },
   "multipleProducts": {
    "type": "string",
    "description": "Multiple Products"
   },
   "multipleRates": {
    "type": "string",
    "description": "Multiple Rates"
   },
   "multipleVenues": {
    "type": "string",
    "description": "Multiple Venues"
   },
   "multipleMarkets": {
    "type": "string",
    "description": "Multiple Markets"
   },
   "reasonsType": {
    "type": "string",
    "enum": [
     "annualPriceReview",
     "newSeason",
     "commercialStrategy",
     "contractUpdate",
     "regulatoryChange",
     "costIncrease",
     "marketAdjustment",
     "correction",
     "emergency"
    ],
    "description": "Vocabulary listed under Standard reasons."
   }
  }
 },
 "PricingChangeRequestWorkspaceView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Pricing Change Request & Workspace displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "changeId": {
    "type": "string",
    "description": "Change ID"
   },
   "changeName": {
    "type": "string",
    "description": "Change Name"
   },
   "changeType": {
    "type": "string",
    "description": "Change Type"
   },
   "businessReason": {
    "type": "string",
    "description": "Business Reason"
   },
   "requestedBy": {
    "type": "string",
    "description": "Requested By"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   },
   "businessUnit": {
    "type": "string",
    "description": "Business Unit"
   },
   "legalEntity": {
    "type": "string",
    "description": "Legal Entity"
   },
   "market": {
    "type": "string",
    "description": "Market"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
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
   "priority": {
    "type": "string",
    "description": "Priority"
   },
   "supportingNotes": {
    "type": "string",
    "description": "Supporting Notes"
   },
   "attachments": {
    "type": "string",
    "description": "Attachments"
   },
   "priceChange": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price Change"
   },
   "newRate": {
    "type": "integer",
    "description": "New Rate"
   },
   "rateRemoval": {
    "type": "number",
    "description": "Rate Removal"
   },
   "priceListChange": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price List Change"
   },
   "eligibilityRuleChange": {
    "type": "string",
    "description": "Eligibility Rule Change"
   },
   "taxChange": {
    "type": "string",
    "description": "Tax Change"
   },
   "feeChange": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Fee Change"
   },
   "formulaChange": {
    "type": "string",
    "description": "Formula Change"
   },
   "currencyRoundingChange": {
    "type": "string",
    "description": "Currency/Rounding Change"
   },
   "emergencyChange": {
    "type": "string",
    "description": "Emergency Change"
   },
   "difference": {
    "type": "string",
    "description": "Difference (the pack shows +AED 25 / +10%)"
   },
   "multipleProducts": {
    "type": "string",
    "description": "Multiple Products"
   },
   "multipleRates": {
    "type": "string",
    "description": "Multiple Rates"
   },
   "multipleVenues": {
    "type": "string",
    "description": "Multiple Venues"
   },
   "multipleMarkets": {
    "type": "string",
    "description": "Multiple Markets"
   },
   "reasonsType": {
    "type": "string",
    "enum": [
     "annualPriceReview",
     "newSeason",
     "commercialStrategy",
     "contractUpdate",
     "regulatoryChange",
     "costIncrease",
     "marketAdjustment",
     "correction",
     "emergency"
    ],
    "description": "Vocabulary listed under Standard reasons."
   }
  }
 },
 "PricingDistributionSynchronizationPublicationMonitorView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Pricing Distribution, Synchronization & Publication Monitor displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "b2c": {
    "type": "string",
    "description": "B2C"
   },
   "mobileApp": {
    "type": "string",
    "description": "Mobile App"
   },
   "pos": {
    "type": "integer",
    "description": "POS"
   },
   "mobilePos": {
    "type": "integer",
    "description": "Mobile POS"
   },
   "kiosk": {
    "type": "string",
    "description": "Kiosk"
   },
   "callCenter": {
    "type": "string",
    "description": "Call Center"
   },
   "b2b": {
    "type": "string",
    "description": "B2B"
   },
   "reseller": {
    "type": "string",
    "description": "Reseller"
   },
   "ota": {
    "type": "string",
    "description": "OTA"
   },
   "apis": {
    "type": "integer",
    "description": "APIs"
   },
   "cacheCdnWhereApplicable": {
    "type": "string",
    "description": "Cache/CDN where applicable"
   },
   "externalIntegratedSystems": {
    "type": "integer",
    "description": "External Integrated Systems"
   },
   "queue": {
    "type": "string",
    "description": "Queue"
   },
   "investigate": {
    "type": "string",
    "description": "Investigate"
   },
   "rollbackTarget": {
    "type": "string",
    "description": "Rollback Target"
   },
   "channels": {
    "type": "string",
    "description": "channels"
   },
   "publicationStarted": {
    "type": "string",
    "description": "Publication Started"
   },
   "lastUpdated": {
    "type": "string",
    "format": "date-time",
    "description": "Last Updated"
   },
   "recordsPublished": {
    "type": "string",
    "description": "Records Published"
   },
   "recordsFailed": {
    "type": "integer",
    "description": "Records Failed"
   },
   "latency": {
    "type": "string",
    "description": "Latency"
   },
   "targetVersion": {
    "type": "string",
    "description": "Target Version"
   }
  }
 },
 "PricingGovernanceCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Pricing Governance Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "pricingChangesInDraft": {
    "type": "string",
    "description": "Pricing Changes in Draft"
   },
   "pendingValidation": {
    "type": "integer",
    "description": "Pending Validation"
   },
   "pendingApproval": {
    "type": "integer",
    "description": "Pending Approval"
   },
   "approvedChanges": {
    "type": "integer",
    "description": "Approved Changes"
   },
   "scheduledPublications": {
    "type": "integer",
    "description": "Scheduled Publications"
   },
   "publishedToday": {
    "type": "string",
    "description": "Published Today"
   },
   "failedPublications": {
    "type": "integer",
    "description": "Failed Publications"
   },
   "emergencyChanges": {
    "type": "integer",
    "description": "Emergency Changes"
   },
   "rollbacks": {
    "type": "integer",
    "description": "Rollbacks"
   },
   "expiringPrices": {
    "type": "integer",
    "description": "Expiring Prices"
   },
   "governanceExceptions": {
    "type": "integer",
    "description": "Governance Exceptions"
   },
   "highRiskChanges": {
    "type": "integer",
    "description": "High-Risk Changes"
   },
   "by": {
    "type": "string",
    "description": "By"
   },
   "aed": {
    "type": "string",
    "description": "−AED"
   },
   "bulkUpdate": {
    "type": "string",
    "description": "Bulk Update"
   }
  }
 },
 "PricingHistoryAuditComplianceExplorerView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Pricing History, Audit & Compliance Explorer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "oldValueNewValue": {
    "type": "string",
    "description": "Old Value → New Value"
   },
   "plus": {
    "type": "string",
    "description": "plus"
   },
   "changedBy": {
    "type": "string",
    "description": "Changed By"
   },
   "dateTime": {
    "type": "string",
    "format": "date-time",
    "description": "Date/Time"
   },
   "reason": {
    "type": "string",
    "description": "Reason"
   },
   "source": {
    "type": "string",
    "description": "Source"
   },
   "effectiveDate": {
    "type": "string",
    "format": "date-time",
    "description": "Effective Date"
   },
   "publication": {
    "type": "string",
    "description": "Publication"
   },
   "configurationAudit": {
    "type": "string",
    "description": "Configuration Audit"
   },
   "approvalAudit": {
    "type": "string",
    "description": "Approval Audit"
   },
   "publicationAudit": {
    "type": "string",
    "description": "Publication Audit"
   },
   "synchronizationAudit": {
    "type": "string",
    "description": "Synchronization Audit"
   },
   "rollbackAudit": {
    "type": "string",
    "description": "Rollback Audit"
   },
   "emergencyActionAudit": {
    "type": "string",
    "description": "Emergency Action Audit"
   },
   "internalAudit": {
    "type": "string",
    "description": "Internal Audit"
   },
   "finance": {
    "type": "string",
    "description": "Finance"
   },
   "compliance": {
    "type": "string",
    "description": "Compliance"
   },
   "regulatoryReview": {
    "type": "string",
    "description": "Regulatory Review"
   },
   "producedThisPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "produced this price?"
   },
   "whatPricesExist": {
    "type": "string",
    "description": "What prices exist?"
   },
   "price": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "price?"
   },
   "inBoards6And7": {
    "type": "string",
    "description": "in Boards 6 and 7"
   },
   "respectingCommercialGuardrails": {
    "type": "string",
    "description": "respecting commercial guardrails"
   },
   "guardrailsResolvedDynamicPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Guardrails → Resolved Dynamic Price"
   }
  }
 },
 "PricingPublicationEffectiveDateSchedulerInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Pricing Publication & Effective-Date Scheduler submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "scheduledPublication": {
    "type": "string",
    "format": "date-time",
    "description": "Scheduled Publication"
   },
   "futureEffectiveDate": {
    "type": "string",
    "format": "date-time",
    "description": "Future Effective Date"
   },
   "stagedPublication": {
    "type": "string",
    "description": "Staged Publication"
   },
   "marketByMarket": {
    "type": "string",
    "description": "Market-by-Market"
   },
   "venueByVenue": {
    "type": "string",
    "description": "Venue-by-Venue"
   },
   "channelByChannel": {
    "type": "string",
    "description": "Channel-by-Channel"
   },
   "theseDatesMayDiffer": {
    "type": "string",
    "description": "These dates may differ"
   },
   "approvalComplete": {
    "type": "string",
    "description": "Approval Complete"
   },
   "validationPassed": {
    "type": "string",
    "description": "Validation Passed"
   },
   "noCriticalConflicts": {
    "type": "string",
    "description": "No Critical Conflicts"
   },
   "dependenciesAvailable": {
    "type": "string",
    "description": "Dependencies Available"
   },
   "channelsReady": {
    "type": "string",
    "description": "Channels Ready"
   },
   "effectiveDatesValid": {
    "type": "string",
    "description": "Effective Dates Valid"
   }
  }
 },
 "PricingPublicationEffectiveDateSchedulerView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Pricing Publication & Effective-Date Scheduler displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "scheduledPublication": {
    "type": "string",
    "format": "date-time",
    "description": "Scheduled Publication"
   },
   "futureEffectiveDate": {
    "type": "string",
    "format": "date-time",
    "description": "Future Effective Date"
   },
   "stagedPublication": {
    "type": "string",
    "description": "Staged Publication"
   },
   "marketByMarket": {
    "type": "string",
    "description": "Market-by-Market"
   },
   "venueByVenue": {
    "type": "string",
    "description": "Venue-by-Venue"
   },
   "channelByChannel": {
    "type": "string",
    "description": "Channel-by-Channel"
   },
   "publicationDate": {
    "type": "string",
    "format": "date-time",
    "description": "Publication Date"
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
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "market": {
    "type": "string",
    "description": "Market"
   },
   "channel": {
    "type": "string",
    "description": "Channel"
   },
   "version": {
    "type": "string",
    "description": "Version"
   },
   "theseDatesMayDiffer": {
    "type": "string",
    "description": "These dates may differ"
   },
   "approvalComplete": {
    "type": "string",
    "description": "Approval Complete"
   },
   "validationPassed": {
    "type": "string",
    "description": "Validation Passed"
   },
   "noCriticalConflicts": {
    "type": "string",
    "description": "No Critical Conflicts"
   },
   "dependenciesAvailable": {
    "type": "string",
    "description": "Dependencies Available"
   },
   "channelsReady": {
    "type": "string",
    "description": "Channels Ready"
   },
   "effectiveDatesValid": {
    "type": "string",
    "description": "Effective Dates Valid"
   }
  }
 },
 "PricingRollbackEmergencyControlCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Pricing Rollback & Emergency Control Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "previousVersion": {
    "type": "string",
    "description": "Previous Version"
   },
   "selectedVersion": {
    "type": "string",
    "description": "Selected Version"
   },
   "previousPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Previous Price"
   },
   "commercialBaseline": {
    "type": "string",
    "description": "Commercial Baseline"
   },
   "selectedProducts": {
    "type": "string",
    "description": "Selected Products"
   },
   "selectedVenue": {
    "type": "string",
    "description": "Selected Venue"
   },
   "selectedMarket": {
    "type": "string",
    "description": "Selected Market"
   },
   "selectedChannel": {
    "type": "string",
    "description": "Selected Channel"
   },
   "entirePublication": {
    "type": "string",
    "description": "Entire Publication"
   },
   "version53": {
    "type": "string",
    "description": "Version 5.3"
   },
   "incorrectAdultRate": {
    "type": "number",
    "description": "Incorrect Adult Rate"
   },
   "version52": {
    "type": "string",
    "description": "Version 5.2"
   },
   "dubaiVenueOnly": {
    "type": "string",
    "description": "Dubai Venue only"
   },
   "productsAffected": {
    "type": "string",
    "description": "Products Affected"
   },
   "channelsAffected": {
    "type": "string",
    "description": "Channels Affected"
   },
   "transactionsSinceActivation": {
    "type": "string",
    "description": "Transactions Since Activation"
   },
   "revenueExposure": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Revenue Exposure"
   },
   "existingOrders": {
    "type": "string",
    "description": "Existing Orders"
   },
   "futureSales": {
    "type": "string",
    "description": "Future Sales"
   },
   "stopScheduledPublication": {
    "type": "string",
    "format": "date-time",
    "description": "Stop Scheduled Publication"
   },
   "stopDistribution": {
    "type": "string",
    "description": "Stop Distribution"
   },
   "reason": {
    "type": "string",
    "description": "Reason"
   },
   "authorizedRole": {
    "type": "string",
    "description": "Authorized Role"
   },
   "incidentReference": {
    "type": "string",
    "description": "Incident Reference"
   },
   "timestamp": {
    "type": "string",
    "format": "date-time",
    "description": "Timestamp"
   }
  }
 },
 "PricingVersionBaselineManagementView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Pricing Version & Baseline Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "version": {
    "type": "string",
    "description": "Version"
   },
   "priceList": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Price List"
   },
   "createdDate": {
    "type": "string",
    "format": "date-time",
    "description": "Created Date"
   },
   "effectiveDate": {
    "type": "string",
    "format": "date-time",
    "description": "Effective Date"
   },
   "createdBy": {
    "type": "string",
    "format": "date-time",
    "description": "Created By"
   },
   "changeRequest": {
    "type": "string",
    "description": "Change Request"
   },
   "productCount": {
    "type": "integer",
    "description": "Product Count"
   },
   "changeCount": {
    "type": "integer",
    "description": "Change Count"
   },
   "status": {
    "type": "integer",
    "description": "Status"
   },
   "version42": {
    "type": "string",
    "description": "Version 4.2"
   },
   "version43": {
    "type": "string",
    "description": "Version 4.3"
   },
   "added": {
    "type": "string",
    "description": "Added"
   },
   "removed": {
    "type": "string",
    "description": "Removed"
   },
   "modified": {
    "type": "string",
    "description": "Modified"
   },
   "unchanged": {
    "type": "string",
    "description": "Unchanged"
   },
   "rateV42V43": {
    "type": "number",
    "description": "Rate V4.2 V4.3"
   },
   "ce": {
    "type": "string",
    "description": "ce"
   },
   "adult10": {
    "type": "number",
    "description": "Adult +10%"
   },
   "child83": {
    "type": "number",
    "description": "Child +8.3%"
   },
   "r190200": {
    "type": "string",
    "description": "r 190 200"
   },
   "transactionOccurred": {
    "type": "string",
    "description": "transaction occurred"
   }
  }
 }
}
```
