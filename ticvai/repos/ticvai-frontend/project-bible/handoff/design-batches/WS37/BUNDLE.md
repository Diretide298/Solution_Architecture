# WS37 — Pricing   Revenue Management board 4

**10 screens · 15 operations · 18 schemas · 4 permissions**

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

- **Every control that can be refused must be gated.** 4 permissions apply here:
  `PRICE_CONFIGURE, PRODUCT_APPROVE, PRODUCT_CONFIGURE, PRODUCT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-078` | Pricing Governance Command Center | listDetail | 2 | 0 | — |
| `ADM-079` | Pricing Change Request & Workspace | configEditor | 3 | 0 | — |
| `ADM-080` | Bulk Pricing Update, Import & Mass Maintenance | listDetail | 1 | 0 | — |
| `ADM-081` | Pricing Version & Baseline Management | listDetail | 1 | 0 | — |
| `ADM-082` | Pricing Change Impact Analysis | listDetail | 2 | 0 | — |
| `ADM-083` | Pricing Approval Workflow & Authority Matrix | configEditor | 1 | 0 | — |
| `ADM-084` | Pricing Publication & Effective-Date Scheduler | configEditor | 1 | 0 | — |
| `ADM-085` | Pricing Distribution, Synchronization & Publication Monitor | listDetail | 1 | 0 | — |
| `ADM-086` | Pricing Rollback & Emergency Control Center | listDetail | 3 | 2 | — |
| `ADM-087` | Pricing History, Audit & Compliance Explorer | listDetail | 1 | 0 | — |

## Thin screens in this batch

**ADM-081, ADM-082, ADM-085 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

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
     "provenance": "derived — ADM-002 declares entryState.params  and ADM-078 holds none of them, so the edge carries nothing and ADM-002 opens cold"
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
    },
    {
     "to": "ADM-079",
     "trigger": "Works in Pricing Change Request & Workspace",
     "provenance": "flow F146 step 1→2",
     "operation": "listPricingGovernance",
     "carries": [
      "changeId"
     ]
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Authorized administrators can monitor and control the complete pricing-change lifecycle from a centralized governance workspace.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide Commercial, Revenue, Finance, and authorized management with one operational view of all pricing changes and governance activities.",
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
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Pricing Changes in Draft",
       "bindsTo": "PricingGovernanceCommandCenterSummary.pricingChangesInDraft",
       "operation": "listPricingGovernance",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Pending Validation",
       "bindsTo": "PricingGovernanceCommandCenterSummary.pendingValidation",
       "operation": "listPricingGovernance",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Pending Approval",
       "bindsTo": "PricingGovernanceCommandCenterSummary.pendingApproval",
       "operation": "listPricingGovernance",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Approved Changes",
       "bindsTo": "PricingGovernanceCommandCenterSummary.approvedChanges",
       "operation": "listPricingGovernance",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Scheduled Publications",
       "bindsTo": "PricingGovernanceCommandCenterSummary.scheduledPublications",
       "operation": "listPricingGovernance",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Published today",
       "bindsTo": "PricingGovernanceCommandCenterSummary.publishedToday",
       "operation": "listPricingGovernance",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Failed Publications",
       "bindsTo": "PricingGovernanceCommandCenterSummary.failedPublications",
       "operation": "listPricingGovernance",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Emergency Changes",
       "bindsTo": "PricingGovernanceCommandCenterSummary.emergencyChanges",
       "operation": "listPricingGovernance",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Rollbacks",
       "bindsTo": "PricingGovernanceCommandCenterSummary.rollbacks",
       "operation": "listPricingGovernance",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Expiring prices",
       "bindsTo": "PricingGovernanceCommandCenterSummary.expiringPrices",
       "operation": "listPricingGovernance",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Governance exceptions",
       "bindsTo": "PricingGovernanceCommandCenterSummary.governanceExceptions",
       "operation": "listPricingGovernance",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "High risk changes",
       "bindsTo": "PricingGovernanceCommandCenterSummary.highRiskChanges",
       "operation": "listPricingGovernance",
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
       "label": "Every pricing governance",
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
       "operation": "decidePricingChangeRequest",
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
   },
   {
    "operationId": "decidePricingChangeRequest",
    "contract": "catalogue",
    "purpose": "Approve, reject or return a pricing change request",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "changeId",
     "from": "navigation"
    }
   ],
   "preloaded": [
    "PricingGovernanceCommandCenterSummary.pricingChangesInDraft",
    "PricingGovernanceCommandCenterSummary.pendingValidation",
    "PricingGovernanceCommandCenterSummary.pendingApproval",
    "PricingGovernanceCommandCenterSummary.approvedChanges",
    "PricingGovernanceCommandCenterSummary.scheduledPublications",
    "PricingGovernanceCommandCenterSummary.publishedToday"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-078",
   "workshopBoard": "wireframes/WS98 Pricing   Revenue Management Board 4.dc.html#adm-078"
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
     "operation": "setPricingChangeRequest",
     "carries": [
      "changeId"
     ]
    }
   ]
  },
  "density": "compact",
  "purposeNote": "All governed pricing modifications can originate from a traceable change request without directly editing live commercial configuration.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population",
  "purpose": "Provide a governed workspace for creating individual or structured pricing changes before modifying production pricing.",
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
      },
      {
       "kind": "primaryButton",
       "label": "Submit",
       "operation": "submitPricingChangeRequest",
       "provenance": "contract catalogue.yaml POST /pricing-change-request/{changeId}/submit (decided 29 September, readiness close-out)"
      },
      {
       "kind": "secondaryButton",
       "label": "Approve, reject or return",
       "operation": "decidePricingChangeRequest",
       "notes": "Shown to an approver holding PRODUCT_APPROVE once the request is submitted; the author cannot decide their own.",
       "provenance": "contract catalogue.yaml POST /pricing-change-request/{changeId}/decision (decided 29 September, readiness close-out)"
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
    "trigger": "onAction"
   },
   {
    "operationId": "submitPricingChangeRequest",
    "contract": "catalogue",
    "purpose": "Submit the draft pricing change for validation and approval",
    "trigger": "onAction"
   },
   {
    "operationId": "decidePricingChangeRequest",
    "contract": "catalogue",
    "purpose": "Approve, reject or return the pricing change request",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-079",
   "workshopBoard": "wireframes/WS98 Pricing   Revenue Management Board 4.dc.html#adm-079"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 58. 0 of 0 labels bound to a contract property; 23 of 46 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "changeId",
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
  "purposeNote": "Large-scale pricing changes can be safely prepared, validated, previewed, and submitted through controlled bulk operations.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Allow large pricing portfolios to be updated efficiently without manually editing hundreds or thousands of records.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 12 actions on this screen and the screen declares 1 operation.** Unserved: Increase by %, Decrease by %, Increase Fixed Amount, Decrease Fixed Amount, Replace Amount, Copy Rate, Change Currency, Set Effective Dates …. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
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
        "BulkPricingUpdateImportMassMaintenanceView.recordsRead",
        "BulkPricingUpdateImportMassMaintenanceView.validRecords",
        "BulkPricingUpdateImportMassMaintenanceView.warningCount",
        "BulkPricingUpdateImportMassMaintenanceView.errorCount"
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
        "BulkPricingUpdateImportMassMaintenanceView.recordsRead",
        "BulkPricingUpdateImportMassMaintenanceView.validRecords",
        "BulkPricingUpdateImportMassMaintenanceView.warningCount",
        "BulkPricingUpdateImportMassMaintenanceView.errorCount"
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
       "label": "Decrease by %",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 60 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Increase Fixed Amount",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 60 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Decrease Fixed Amount",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 60 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Replace Amount",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 60 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Copy Rate",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 60 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Change Currency",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 60 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Set Effective Dates",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 60 §Support"
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
    "BulkPricingUpdateImportMassMaintenanceView.recordsRead",
    "BulkPricingUpdateImportMassMaintenanceView.validRecords",
    "BulkPricingUpdateImportMassMaintenanceView.warningCount",
    "BulkPricingUpdateImportMassMaintenanceView.errorCount"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-080",
   "workshopBoard": "wireframes/WS98 Pricing   Revenue Management Board 4.dc.html#adm-080"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 60. 4 of 4 labels bound to a contract property; 27 of 49 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "purposeNote": "configuration was effective for any historical transaction.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display; Compare; Show) and no metric row",
  "purpose": "Maintain immutable versions of pricing configuration so TICVAI always knows what configuration existed at a particular time.",
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-081",
   "workshopBoard": "wireframes/WS98 Pricing   Revenue Management Board 4.dc.html#adm-081"
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
  "purposeNote": "Approvers can understand financial, customer, channel, dependency, and operational impact before authorizing a pricing change.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Analyze) and no metric row",
  "purpose": "Determine the commercial and operational consequences of a pricing change before approval and publication. This is one of the most important screens in Board 4.",
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
   },
   {
    "operationId": "listChangeImpactAnalysis",
    "contract": "catalogue",
    "purpose": "Change Impact Analysis",
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-082",
   "workshopBoard": "wireframes/WS98 Pricing   Revenue Management Board 4.dc.html#adm-082"
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
  "purposeNote": "Pricing changes cannot progress beyond their configured governance threshold without all required approvals.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure who must approve pricing changes based on their commercial risk and scope.",
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
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-083",
   "workshopBoard": "wireframes/WS98 Pricing   Revenue Management Board 4.dc.html#adm-083"
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
  "purposeNote": "Only validated and fully approved pricing configurations can be scheduled and activated at controlled effective dates.",
  "pattern": "configEditor",
  "patternReason": "the screen declares a publishing operation over fields the pack configures",
  "purpose": "Control exactly when approved pricing becomes commercially effective.",
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
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-084",
   "workshopBoard": "wireframes/WS98 Pricing   Revenue Management Board 4.dc.html#adm-084"
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
  "purposeNote": "Administrators can confirm that approved pricing has been successfully distributed and synchronized to all intended channels and systems.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Monitor; Display) and no metric row",
  "purpose": "Ensure published pricing reaches every TICVAI channel and dependent system consistently.",
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
        "PricingDistributionSynchronizationPublicationMonitorView.target",
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
        "PricingDistributionSynchronizationPublicationMonitorView.target",
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
    "PricingDistributionSynchronizationPublicationMonitorView.target"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-085",
   "workshopBoard": "wireframes/WS98 Pricing   Revenue Management Board 4.dc.html#adm-085"
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
  "purposeNote": "Authorized users can rapidly contain and reverse problematic pricing changes without altering historical transactions or losing audit traceability.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide controlled recovery when a pricing publication is incorrect or creates unacceptable commercial impact.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 9 actions on this screen; 8 are served since the writers pass (29 September): Previous Version, Selected Version, Previous Price, Commercial Baseline, Selected Products, Selected Venue, Selected Market, Selected Channel by `requestPricingRollback`.** Still unserved: the rest of the pack list past the eight shown here. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
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
       "label": "Previous Version",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 69 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Selected Version",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 69 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Previous Price",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 69 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Commercial Baseline",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 69 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Selected Products",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 69 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Selected Venue",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 69 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Selected Market",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 69 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Selected Channel",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 69 §Support"
      },
      {
       "kind": "banner",
       "label": "Permissions this screen separates",
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** Freeze Price List, Freeze Product Pricing, Freeze Venue Pricing, Stop Scheduled Publication, Stop Distribution, Restore Last Known Good Version. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 69 §Authorized users should have"
      },
      {
       "kind": "secondaryButton",
       "label": "Request pricing rollback",
       "operation": "requestPricingRollback",
       "permission": "PRICE_CONFIGURE",
       "notes": "**A pricing rollback or emergency action, as a record first** (29 September, writers pass).",
       "provenance": "contract catalogue.yaml POST /pricing-rollback-emergency"
      },
      {
       "kind": "destructiveButton",
       "label": "Cancel pricing rollback",
       "operation": "cancelPricingRollback",
       "permission": "PRICE_CONFIGURE",
       "notes": "**Only before it runs** (29 September, writers pass).",
       "provenance": "contract catalogue.yaml POST /pricing-rollback-emergency/{actionId}/cancel"
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
   },
   {
    "operationId": "requestPricingRollback",
    "contract": "catalogue",
    "purpose": "Roll pricing back, or take an emergency pricing action",
    "trigger": "onAction",
    "invalidates": [
     "listPricingRollbackEmergency"
    ]
   },
   {
    "operationId": "cancelPricingRollback",
    "contract": "catalogue",
    "purpose": "Cancel a rollback that has not started",
    "trigger": "onAction",
    "invalidates": [
     "listPricingRollbackEmergency"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "PricingRollbackEmergencyControlCenterView.rollbackTarget",
    "PricingRollbackEmergencyControlCenterView.rollbackScope"
   ],
   "params": [
    {
     "name": "actionId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-086",
   "workshopBoard": "wireframes/WS98 Pricing   Revenue Management Board 4.dc.html#adm-086"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 69. 0 of 0 labels bound to a contract property; 15 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formRequestPricingRollback",
    "component": "modal",
    "trigger": "Request pricing rollback",
    "body": "**Collects what `requestPricingRollback` sends before it is called.** Required: `id`, `scopePath`, `subject`, `actionType`, `reason`, `status`, `requestedByPrincipalId`, `requestedAt`. Optional: `productId`, `priceListId`, `fromVersion`, `toVersion`, `productScope`, `rollbackTarget`, `rollbackScope`, `scopeIds`, `dependencies`, `executionMode`, `isEmergency`, `scheduledAt` and 6 more. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "CatalogueRollbackAction",
    "confirm": {
     "label": "Request pricing rollback",
     "operation": "requestPricingRollback"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "id",
      "scopePath",
      "subject",
      "actionType",
      "reason",
      "status",
      "requestedByPrincipalId",
      "requestedAt",
      "productId",
      "priceListId",
      "fromVersion",
      "toVersion",
      "productScope",
      "rollbackTarget",
      "rollbackScope",
      "scopeIds",
      "dependencies",
      "executionMode"
     ]
    },
    "provenance": "contract catalogue.yaml POST /pricing-rollback-emergency"
   },
   {
    "id": "confirmCancelPricingRollback",
    "component": "confirmDialog",
    "trigger": "Cancel pricing rollback",
    "body": "**Names what `cancelPricingRollback` changes and what it leaves alone**, in the consequence rather than the verb. A catalogue rollback action this affects should be identified in the dialog, not just counted. **Collects what `cancelPricingRollback` sends before it is called.** Required: `reason`.",
    "provenance": "contract catalogue.yaml POST /pricing-rollback-emergency/{actionId}/cancel"
   }
  ],
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
   "notes": "**Reached from ADM-078, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-078",
     "trigger": "Pricing Governance Command Center",
     "provenance": "derived — ADM-078 declares entryState.params changeId and ADM-087 holds none of them, so the edge carries nothing and ADM-078 opens cold"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Every material pricing configuration, approval, publication, override, and rollback is fully traceable and can be reconstructed for operational, financial, and compliance purposes. Board 4 — Final Screen Register # Backend Screen Core Responsibility 10.4. Pricing Governance Command Center Governance operations 1 10.4. Pricing Change Request & Workspace Controlled change creation 2 10.4. Bulk Pricing Update, Import & Mass Maintenance Mass pricing operations 3 10.4. Pricing Version & Baseline Management Version control 4 10.4. Pricing Change Impact Analysis Pre-change impact 5 10.4. Pricing Appr",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide complete forensic traceability for every pricing configuration and change. Enable TICVAI revenue administrators to configure dynamic-pricing strategies using real-time commercial conditions such as: Demand + Occupancy + Availability + Inventory + Booking Velocity + Time-to- Event + Season + Day + Timeslot + Channel + Customer Segment + Location The engine converts those conditions into controlled price movements while always respecting commercial guardrails.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Board 5 — Dynamic Pricing, Revenue. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Pricing___Revenue_Management_Reference.pdf, page 70 §Operations"
   },
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
       "kind": "primaryButton",
       "label": "Board 5 — Dynamic Pricing, Revenue",
       "provenance": "pack Pricing___Revenue_Management_Reference.pdf, page 70 §Operations"
      },
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-087",
   "workshopBoard": "wireframes/WS98 Pricing   Revenue Management Board 4.dc.html#adm-087"
  },
  "apisNote": "Regenerated 9 September 2026 from Pricing___Revenue_Management_Reference.pdf page 70. 0 of 12 labels bound to a contract property; 14 of 118 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "PricingApprovalWorkflowAuthorityMatrixInput",
  "responds": "PricingApprovalWorkflowAuthorityMatrixView"
 },
 "cancelPricingRollback": {
  "method": "POST",
  "path": "/pricing-rollback-emergency/{actionId}/cancel",
  "contract": "catalogue",
  "summary": "Cancel a rollback that has not started",
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
  "responds": "CatalogueRollbackAction"
 },
 "decidePricingChangeRequest": {
  "method": "POST",
  "path": "/pricing-change-request/{changeId}/decision",
  "contract": "catalogue",
  "summary": "Approve, reject or return a pricing change request",
  "permission": "PRODUCT_APPROVE",
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
  "requestBody": "PricingChangeRequestDecisionInput",
  "responds": "PricingChangeRequestWorkspaceView"
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
  "parameters": [
   {
    "name": "jobKind",
    "in": "query",
    "required": false
   },
   {
    "name": "operation",
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
 "listChangeImpactAnalysis": {
  "method": "GET",
  "path": "/change-impact-analysi",
  "contract": "catalogue",
  "summary": "Change Impact Analysis",
  "permission": "PRODUCT_VIEW",
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
    "name": "changeRequestId",
    "in": "query",
    "required": false
   },
   {
    "name": "productId",
    "in": "query",
    "required": false
   },
   {
    "name": "area",
    "in": "query",
    "required": false
   },
   {
    "name": "minRisk",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "ChangeImpactAnalysisView"
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
  "parameters": [
   {
    "name": "changeRequestId",
    "in": "query",
    "required": false
   },
   {
    "name": "riskLevel",
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
   },
   {
    "name": "channel",
    "in": "query",
    "required": false
   },
   {
    "name": "dateFrom",
    "in": "query",
    "required": false
   },
   {
    "name": "dateTo",
    "in": "query",
    "required": false
   },
   {
    "name": "transaction",
    "in": "query",
    "required": false
   },
   {
    "name": "approval",
    "in": "query",
    "required": false
   },
   {
    "name": "auditType",
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
 "listPricingDistributionSynchronization": {
  "method": "GET",
  "path": "/pricing-distribution-synchronization",
  "contract": "catalogue",
  "summary": "Pricing Distribution, Synchronization & Publication Monitor",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "publicationVersion",
    "in": "query",
    "required": false
   },
   {
    "name": "target",
    "in": "query",
    "required": false
   },
   {
    "name": "status",
    "in": "query",
    "required": false
   },
   {
    "name": "outOfSyncOnly",
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
    "name": "owner",
    "in": "query",
    "required": false
   },
   {
    "name": "changeType",
    "in": "query",
    "required": false
   },
   {
    "name": "approver",
    "in": "query",
    "required": false
   },
   {
    "name": "riskLevel",
    "in": "query",
    "required": false
   },
   {
    "name": "status",
    "in": "query",
    "required": false
   },
   {
    "name": "effectiveFrom",
    "in": "query",
    "required": false
   },
   {
    "name": "effectiveTo",
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
 "listPricingRollbackEmergency": {
  "method": "GET",
  "path": "/pricing-rollback-emergency",
  "contract": "catalogue",
  "summary": "Pricing Rollback & Emergency Control Center",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "actionType",
    "in": "query",
    "required": false
   },
   {
    "name": "status",
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
 "listPricingVersionBaseline": {
  "method": "GET",
  "path": "/pricing-version-baseline",
  "contract": "catalogue",
  "summary": "Pricing Version & Baseline Management",
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
    "name": "status",
    "in": "query",
    "required": false
   },
   {
    "name": "compareTo",
    "in": "query",
    "required": false
   },
   {
    "name": "effectiveOn",
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
 "publishPricingEffectiveDate": {
  "method": "PUT",
  "path": "/pricing-effective-date",
  "contract": "catalogue",
  "summary": "Pricing Publication & Effective-Date Scheduler",
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
  "requestBody": "PricingPublicationEffectiveDateSchedulerInput",
  "responds": "PricingPublicationEffectiveDateSchedulerView"
 },
 "requestPricingRollback": {
  "method": "POST",
  "path": "/pricing-rollback-emergency",
  "contract": "catalogue",
  "summary": "Roll pricing back, or take an emergency pricing action",
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
  "requestBody": "CatalogueRollbackAction",
  "responds": "CatalogueRollbackAction"
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "PricingChangeRequestWorkspaceInput",
  "responds": "PricingChangeRequestWorkspaceView"
 },
 "submitPricingChangeRequest": {
  "method": "POST",
  "path": "/pricing-change-request/{changeId}/submit",
  "contract": "catalogue",
  "summary": "Submit a draft pricing change for validation and approval",
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
  "requestBody": null,
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
   "selectBy": {
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
   "recordsRead": {
    "type": "integer",
    "description": "Records read (import preview)",
    "nullable": true
   },
   "validRecords": {
    "type": "integer",
    "description": "Valid records",
    "nullable": true
   },
   "warningCount": {
    "type": "integer",
    "description": "Records with warnings",
    "nullable": true
   },
   "errorCount": {
    "type": "integer",
    "description": "Records with errors; the job cannot be submitted while above zero",
    "nullable": true
   },
   "jobId": {
    "type": "string",
    "description": "Bulk job ID"
   },
   "jobKind": {
    "type": "string",
    "enum": [
     "bulkOperation",
     "import"
    ],
    "description": "Bulk operation on selected records, or spreadsheet import (CSV/XLSX)"
   },
   "selectionValues": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "IDs selected under selectBy (e.g. the price lists or products)"
   },
   "effectivePeriodFrom": {
    "type": "string",
    "format": "date",
    "description": "Selection: effective period from",
    "nullable": true
   },
   "effectivePeriodTo": {
    "type": "string",
    "format": "date",
    "description": "Selection: effective period to",
    "nullable": true
   },
   "recordsSelected": {
    "type": "integer",
    "description": "Records selected, e.g. 428 admission rates"
   },
   "operation": {
    "type": "string",
    "enum": [
     "increasePercent",
     "decreasePercent",
     "increaseFixedAmount",
     "decreaseFixedAmount",
     "replaceAmount",
     "copyRate",
     "changeCurrency",
     "applyRounding",
     "setEffectiveDates",
     "activateDeactivate",
     "cloneForNewSeason"
    ],
    "description": "Bulk Operation (pack p.60)",
    "nullable": true
   },
   "adjustmentPercent": {
    "type": "number",
    "description": "Percent for increasePercent / decreasePercent",
    "nullable": true
   },
   "adjustmentAmount": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Amount for fixed-amount and replace operations",
    "nullable": true
   },
   "targetCurrency": {
    "type": "string",
    "description": "ISO 4217 currency for changeCurrency",
    "nullable": true
   },
   "currentPortfolioValue": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Preview: current portfolio value",
    "nullable": true
   },
   "proposedPortfolioValue": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Preview: proposed portfolio value",
    "nullable": true
   },
   "fileName": {
    "type": "string",
    "description": "Imported file name",
    "nullable": true
   },
   "columnMappings": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "sourceColumn": {
       "type": "string",
       "description": "Column in the file"
      },
      "targetField": {
       "type": "string",
       "description": "TICVAI field, e.g. rateAmount"
      },
      "suggestedByAi": {
       "type": "boolean",
       "description": "Suggested by AI mapping"
      },
      "confirmed": {
       "type": "boolean",
       "description": "Confirmed by the administrator; unconfirmed mappings block validation"
      }
     },
     "description": "Column mapping"
    },
    "description": "Import column mappings"
   },
   "validationIssues": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "code": {
       "type": "string",
       "enum": [
        "invalidProduct",
        "unknownRateCode",
        "duplicateRecord",
        "unsupportedCurrency",
        "missingMandatoryField",
        "invalidDate",
        "invalidAmount"
       ],
       "description": "Import Validation check (pack p.61)"
      },
      "rowNumber": {
       "type": "integer",
       "description": "File row",
       "nullable": true
      },
      "severity": {
       "type": "string",
       "enum": [
        "warning",
        "error"
       ],
       "description": "Errors block submission"
      },
      "message": {
       "type": "string",
       "description": "Message"
      }
     },
     "description": "One issue"
    },
    "description": "Validation issues found before commit"
   },
   "changeRequestId": {
    "type": "string",
    "description": "Change request the job was submitted as",
    "nullable": true
   },
   "status": {
    "type": "string",
    "description": "Status: draft, validating, validationFailed, readyToSubmit, submitted or cancelled"
   },
   "createdBy": {
    "type": "string",
    "description": "Created by"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time",
    "description": "Created at"
   }
  }
 },
 "CatalogueRollbackAction": {
  "type": "object",
  "x-ticvai-persistence": "catalogue.rollback_action",
  "description": "**A rollback or emergency action on a product or on pricing** (29 September, data model DM3). Merges product rollback (ADM-133) and the pricing rollback and emergency centre (ADM-086). A rollback restores an earlier `catalogue.product_version` or `catalogue.price_list_version` as a new version; nothing is edited in place. Emergency actions may run before approval and then need `retrospectiveApprovalRequired`.",
  "required": [
   "id",
   "scopePath",
   "subject",
   "actionType",
   "reason",
   "status",
   "requestedByPrincipalId",
   "requestedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Operations write it at `venue` scope."
   },
   "subject": {
    "type": "string",
    "enum": [
     "product",
     "pricing"
    ]
   },
   "actionType": {
    "type": "string",
    "enum": [
     "rollback",
     "freezePriceList",
     "freezeProductPricing",
     "freezeVenuePricing",
     "stopScheduledPublication",
     "stopDistribution",
     "restoreLastKnownGood"
    ],
    "description": "Product rollbacks are `rollback`."
   },
   "productId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "priceListId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "fromVersion": {
    "type": "integer",
    "nullable": true
   },
   "toVersion": {
    "type": "integer",
    "nullable": true
   },
   "productScope": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "entireProduct",
      "pricingAssociation",
      "channelAssociation",
      "validityConfiguration",
      "media",
      "policy",
      "entitlementConfiguration"
     ]
    },
    "description": "Product rollbacks: which parts are restored."
   },
   "rollbackTarget": {
    "type": "string",
    "enum": [
     "previousVersion",
     "selectedVersion",
     "previousPrice",
     "commercialBaseline",
     null
    ],
    "nullable": true
   },
   "rollbackScope": {
    "type": "string",
    "enum": [
     "selectedProducts",
     "selectedVenue",
     "selectedMarket",
     "selectedChannel",
     "entirePublication",
     null
    ],
    "nullable": true
   },
   "scopeIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "dependencies": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Product rollbacks: the dependent objects reviewed before executing."
   },
   "reason": {
    "type": "string"
   },
   "executionMode": {
    "type": "string",
    "enum": [
     "immediate",
     "scheduled"
    ],
    "default": "immediate"
   },
   "isEmergency": {
    "type": "boolean",
    "default": false
   },
   "scheduledAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "incidentReference": {
    "type": "string",
    "maxLength": 200,
    "nullable": true
   },
   "authorisedRole": {
    "type": "string",
    "maxLength": 100,
    "nullable": true
   },
   "retrospectiveApprovalRequired": {
    "type": "boolean",
    "default": false
   },
   "approvalRequestId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "changeRequestId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The change request whose publication is being rolled back."
   },
   "status": {
    "type": "string",
    "enum": [
     "requested",
     "scheduled",
     "executing",
     "completed",
     "failed",
     "cancelled"
    ],
    "default": "requested"
   },
   "requestedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "requestedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "completedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "readOnly": true
   }
  }
 },
 "ChangeImpactAnalysisView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Change Impact Analysis displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "area": {
    "type": "string",
    "enum": [
     "futureOrders",
     "reservations",
     "issuedTickets",
     "capacity",
     "pricing",
     "tax",
     "promotions",
     "membership",
     "entitlements",
     "accessControl",
     "salesChannels",
     "b2bPartners",
     "otas",
     "pos",
     "b2c",
     "kiosk",
     "media",
     "finance",
     "reporting"
    ],
    "description": "Impact area (pack p.21-22)"
   },
   "changeRequestId": {
    "type": "string",
    "description": "Change request analysed",
    "format": "uuid"
   },
   "affectedCount": {
    "type": "integer",
    "description": "How many items in this area are affected (orders, reservations, agreements, channels...)"
   },
   "riskLevel": {
    "type": "string",
    "enum": [
     "low",
     "medium",
     "high",
     "critical"
    ],
    "description": "Risk classification"
   },
   "explanation": {
    "type": "string",
    "description": "AI explanation in business language; advisory",
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
 "PricingApprovalWorkflowAuthorityMatrixInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table covers these fields** — the closest is catalogue.channel_allocation at 4%, so this is not an update to anything the package stores today and no new table has been decided",
  "description": "**What Pricing Approval Workflow & Authority Matrix submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.\n\n**The pack defines this as a record**, under *Every approval action records* - one of only 13 drafted writes that does. That is the client writing a row rather than a screen, and it is where the table conversation should start.",
  "properties": {
   "venue": {
    "type": "string",
    "description": "Scope: venue; empty for all",
    "nullable": true
   },
   "market": {
    "type": "string",
    "description": "Scope: market; empty for all",
    "nullable": true
   },
   "legalEntity": {
    "type": "string",
    "description": "Scope: legal entity; empty for all",
    "nullable": true
   },
   "policyId": {
    "type": "string",
    "description": "Authority policy ID; empty on create",
    "nullable": true
   },
   "policyName": {
    "type": "string",
    "description": "Policy name"
   },
   "tiers": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "dimension": {
       "type": "string",
       "enum": [
        "changePercent",
        "monetaryImpact",
        "revenueImpact",
        "priceList",
        "product",
        "venue",
        "market",
        "legalEntity",
        "channel",
        "taxChange",
        "feeChange",
        "emergencyStatus"
       ],
       "description": "Approval Rules dimension (pack pp.64-65)"
      },
      "minValue": {
       "type": "number",
       "description": "Lower bound (exclusive) for numeric dimensions, e.g. 5 for >5%",
       "nullable": true
      },
      "maxValue": {
       "type": "number",
       "description": "Upper bound (inclusive), e.g. 10 for up to 10%",
       "nullable": true
      },
      "matchValue": {
       "type": "string",
       "description": "Matching value for non-numeric dimensions (a price list, venue, channel...); taxChange/feeChange/emergencyStatus match true",
       "nullable": true
      },
      "approvalLevels": {
       "type": "array",
       "items": {
        "type": "object",
        "properties": {
         "sequence": {
          "type": "integer",
          "description": "Order in the multi-level workflow, 1 first"
         },
         "approverRole": {
          "type": "string",
          "description": "Role that must approve, e.g. Pricing Manager, Commercial Director, Finance"
         },
         "approverUserId": {
          "type": "string",
          "description": "Named approver instead of the role",
          "nullable": true
         }
        },
        "description": "One approval step"
       },
       "description": "Approvers in sequence"
      }
     },
     "description": "One row of the authority matrix"
    },
    "description": "Authority matrix: the first matching row applies; when several dimensions match, all their approval levels are required (decided 29 September, readiness close-out)"
   },
   "creatorCannotGiveFinalApproval": {
    "type": "boolean",
    "description": "Segregation of duties: the user who created a change cannot give final approval; defaults to true (decided 29 September, readiness close-out)"
   },
   "expectedApprovalHours": {
    "type": "integer",
    "description": "Approval SLA: expected approval time in hours; defaults to 48 (decided 29 September, readiness close-out)"
   },
   "reminderAfterHours": {
    "type": "integer",
    "description": "Reminder sent to the pending approver after this many hours; defaults to 24 (decided 29 September, readiness close-out)"
   },
   "escalateAfterHours": {
    "type": "integer",
    "description": "Escalation after this many hours; defaults to 72 (decided 29 September, readiness close-out)"
   },
   "escalateToRole": {
    "type": "string",
    "description": "Role escalated to",
    "nullable": true
   },
   "alternateApproverRole": {
    "type": "string",
    "description": "Alternate approver role when the approver is unavailable or delegates",
    "nullable": true
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
   "venue": {
    "type": "string",
    "description": "Scope: venue; empty for all",
    "nullable": true
   },
   "market": {
    "type": "string",
    "description": "Scope: market; empty for all",
    "nullable": true
   },
   "legalEntity": {
    "type": "string",
    "description": "Scope: legal entity; empty for all",
    "nullable": true
   },
   "policyId": {
    "type": "string",
    "description": "Authority policy ID; empty on create",
    "nullable": true
   },
   "policyName": {
    "type": "string",
    "description": "Policy name"
   },
   "tiers": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "dimension": {
       "type": "string",
       "enum": [
        "changePercent",
        "monetaryImpact",
        "revenueImpact",
        "priceList",
        "product",
        "venue",
        "market",
        "legalEntity",
        "channel",
        "taxChange",
        "feeChange",
        "emergencyStatus"
       ],
       "description": "Approval Rules dimension (pack pp.64-65)"
      },
      "minValue": {
       "type": "number",
       "description": "Lower bound (exclusive) for numeric dimensions, e.g. 5 for >5%",
       "nullable": true
      },
      "maxValue": {
       "type": "number",
       "description": "Upper bound (inclusive), e.g. 10 for up to 10%",
       "nullable": true
      },
      "matchValue": {
       "type": "string",
       "description": "Matching value for non-numeric dimensions (a price list, venue, channel...); taxChange/feeChange/emergencyStatus match true",
       "nullable": true
      },
      "approvalLevels": {
       "type": "array",
       "items": {
        "type": "object",
        "properties": {
         "sequence": {
          "type": "integer",
          "description": "Order in the multi-level workflow, 1 first"
         },
         "approverRole": {
          "type": "string",
          "description": "Role that must approve, e.g. Pricing Manager, Commercial Director, Finance"
         },
         "approverUserId": {
          "type": "string",
          "description": "Named approver instead of the role",
          "nullable": true
         }
        },
        "description": "One approval step"
       },
       "description": "Approvers in sequence"
      }
     },
     "description": "One row of the authority matrix"
    },
    "description": "Authority matrix: the first matching row applies; when several dimensions match, all their approval levels are required (decided 29 September, readiness close-out)"
   },
   "creatorCannotGiveFinalApproval": {
    "type": "boolean",
    "description": "Segregation of duties: the user who created a change cannot give final approval; defaults to true (decided 29 September, readiness close-out)"
   },
   "expectedApprovalHours": {
    "type": "integer",
    "description": "Approval SLA: expected approval time in hours; defaults to 48 (decided 29 September, readiness close-out)"
   },
   "reminderAfterHours": {
    "type": "integer",
    "description": "Reminder sent to the pending approver after this many hours; defaults to 24 (decided 29 September, readiness close-out)"
   },
   "escalateAfterHours": {
    "type": "integer",
    "description": "Escalation after this many hours; defaults to 72 (decided 29 September, readiness close-out)"
   },
   "escalateToRole": {
    "type": "string",
    "description": "Role escalated to",
    "nullable": true
   },
   "alternateApproverRole": {
    "type": "string",
    "description": "Alternate approver role when the approver is unavailable or delegates",
    "nullable": true
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
    "type": "integer",
    "description": "Affected products (count)"
   },
   "events": {
    "type": "integer",
    "description": "Affected events (count)"
   },
   "performances": {
    "type": "integer",
    "description": "Affected performances (count)"
   },
   "venues": {
    "type": "integer",
    "description": "Affected venues (count)"
   },
   "markets": {
    "type": "integer",
    "description": "Affected markets (count)"
   },
   "channels": {
    "type": "integer",
    "description": "Affected channels (count)"
   },
   "b2bPartners": {
    "type": "integer",
    "description": "Affected b2bPartners (count)"
   },
   "memberships": {
    "type": "integer",
    "description": "Affected memberships (count)"
   },
   "packages": {
    "type": "integer",
    "description": "Affected packages (count)"
   },
   "existingReservations": {
    "type": "integer",
    "description": "Existing reservations affected; normally 0 because changes never reach already-sold tickets (MoM 31 Aug §4.10)"
   },
   "futureReservations": {
    "type": "integer",
    "description": "Affected futureReservations (count)"
   },
   "apis": {
    "type": "integer",
    "description": "Affected apis (count)"
   },
   "integrations": {
    "type": "integer",
    "description": "Affected integrations (count)"
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
    "description": "Average price change in percent"
   },
   "maximumChange": {
    "type": "number",
    "description": "Largest single price change in percent"
   },
   "minimumChange": {
    "type": "number",
    "description": "Smallest single price change in percent"
   },
   "marginImpact": {
    "type": "number",
    "description": "Margin impact in percentage points"
   },
   "customerExposure": {
    "type": "integer",
    "description": "Customers or tickets exposed per year at current volumes (decided 29 September, readiness close-out)"
   },
   "transactionVolume": {
    "type": "integer",
    "description": "Transactions per year affected at current volumes (decided 29 September, readiness close-out)"
   },
   "derivedRates": {
    "type": "integer",
    "description": "Dependency impact: derivedRates affected (count)"
   },
   "contractRates": {
    "type": "integer",
    "description": "Dependency impact: contractRates affected (count)"
   },
   "membershipRates": {
    "type": "integer",
    "description": "Dependency impact: membershipRates affected (count)"
   },
   "groupRates": {
    "type": "integer",
    "description": "Dependency impact: groupRates affected (count)"
   },
   "promotions": {
    "type": "integer",
    "description": "Dependency impact: promotions affected (count)"
   },
   "dynamicPricingGuardrails": {
    "type": "integer",
    "description": "Dependency impact: dynamicPricingGuardrails affected (count)"
   },
   "changeRequestId": {
    "type": "string",
    "description": "Change request analysed"
   },
   "changeName": {
    "type": "string",
    "description": "Change name"
   },
   "analysedAt": {
    "type": "string",
    "format": "date-time",
    "description": "When the analysis was computed"
   },
   "revenueImpact": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Projected minus current revenue (annualised)"
   },
   "affectsExistingOrders": {
    "type": "boolean",
    "description": "Whether the change affects existing orders; always false for price changes (never retroactive)"
   },
   "affectsExistingReservations": {
    "type": "boolean",
    "description": "Whether the change affects existing reservations"
   },
   "affectsFutureUnsoldInventory": {
    "type": "boolean",
    "description": "Whether the change affects future unsold inventory"
   },
   "riskLevel": {
    "type": "string",
    "enum": [
     "low",
     "medium",
     "high",
     "critical"
    ],
    "description": "Risk score, classified by the tenant's configurable criteria"
   },
   "aiInsights": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "AI summary lines for this record: advisory only, never approves, publishes or changes a price"
   }
  }
 },
 "PricingChangeRequestDecisionInput": {
  "type": "object",
  "x-ticvai-persistence": "none — request only; the decision is recorded on the approvals request",
  "description": "What `decidePricingChangeRequest` takes (decided 29 September, readiness close-out).",
  "required": [
   "decision"
  ],
  "properties": {
   "decision": {
    "type": "string",
    "enum": [
     "approve",
     "reject",
     "returnForModification"
    ]
   },
   "comment": {
    "type": "string",
    "maxLength": 2000,
    "description": "Required for reject and returnForModification."
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
    "description": "Change ID; empty on create (the server assigns it), set to update a draft",
    "nullable": true
   },
   "changeName": {
    "type": "string",
    "description": "Change Name"
   },
   "changeType": {
    "type": "string",
    "enum": [
     "priceChange",
     "newRate",
     "rateRemoval",
     "priceListChange",
     "eligibilityRuleChange",
     "taxChange",
     "feeChange",
     "formulaChange",
     "currencyRoundingChange",
     "emergencyChange"
    ],
    "description": "Change Type (pack p.59)"
   },
   "businessReason": {
    "type": "string",
    "description": "Business reason in the requester's words"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   },
   "businessUnit": {
    "type": "string",
    "description": "Business unit",
    "nullable": true
   },
   "legalEntity": {
    "type": "string",
    "description": "Legal entity",
    "nullable": true
   },
   "market": {
    "type": "string",
    "description": "Market",
    "nullable": true
   },
   "venue": {
    "type": "string",
    "description": "Venue",
    "nullable": true
   },
   "effectiveDate": {
    "type": "string",
    "format": "date-time",
    "description": "Effective date and time requested; must be in the future, never retroactive (MoM 31 Aug §4.10)"
   },
   "expiryDate": {
    "type": "string",
    "format": "date-time",
    "description": "Expiry date and time; empty for open-ended",
    "nullable": true
   },
   "priority": {
    "type": "string",
    "enum": [
     "low",
     "normal",
     "high",
     "urgent"
    ],
    "description": "Priority; defaults to normal (decided 29 September, readiness close-out)"
   },
   "supportingNotes": {
    "type": "string",
    "description": "Supporting notes",
    "nullable": true
   },
   "attachments": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Attachment document IDs"
   },
   "reasonCode": {
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
   },
   "lines": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "objectType": {
       "type": "string",
       "enum": [
        "product",
        "rate",
        "priceList",
        "eligibilityRule",
        "tax",
        "fee",
        "formula",
        "currencyRounding"
       ],
       "description": "What this line changes"
      },
      "objectId": {
       "type": "string",
       "description": "ID of the product, rate, price list, rule, tax, fee or formula"
      },
      "venue": {
       "type": "string",
       "description": "Venue the line applies to; empty for all in scope",
       "nullable": true
      },
      "market": {
       "type": "string",
       "description": "Market the line applies to; empty for all in scope",
       "nullable": true
      },
      "proposedAmount": {
       "allOf": [
        {
         "$ref": "../shared/common.yaml#/components/schemas/Money"
        }
       ],
       "description": "Proposed amount for a monetary line; empty for removals and non-monetary changes",
       "nullable": true
      },
      "proposedValue": {
       "type": "string",
       "description": "Proposed value for a non-monetary line (rule, formula, rounding), as the target screen's own format",
       "nullable": true
      },
      "remove": {
       "type": "boolean",
       "description": "True when the line removes the rate or object (Rate Removal)"
      }
     },
     "description": "One changed object"
    },
    "description": "Change lines: one request may cover many products, rates, venues and markets"
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
    "description": "Change ID; empty on create (the server assigns it), set to update a draft",
    "nullable": true
   },
   "changeName": {
    "type": "string",
    "description": "Change Name"
   },
   "changeType": {
    "type": "string",
    "enum": [
     "priceChange",
     "newRate",
     "rateRemoval",
     "priceListChange",
     "eligibilityRuleChange",
     "taxChange",
     "feeChange",
     "formulaChange",
     "currencyRoundingChange",
     "emergencyChange"
    ],
    "description": "Change Type (pack p.59)"
   },
   "businessReason": {
    "type": "string",
    "description": "Business reason in the requester's words"
   },
   "requestedBy": {
    "type": "string",
    "description": "Requested by: the user who created the request (server-set)"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   },
   "businessUnit": {
    "type": "string",
    "description": "Business unit",
    "nullable": true
   },
   "legalEntity": {
    "type": "string",
    "description": "Legal entity",
    "nullable": true
   },
   "market": {
    "type": "string",
    "description": "Market",
    "nullable": true
   },
   "venue": {
    "type": "string",
    "description": "Venue",
    "nullable": true
   },
   "effectiveDate": {
    "type": "string",
    "format": "date-time",
    "description": "Effective date and time requested; must be in the future, never retroactive (MoM 31 Aug §4.10)"
   },
   "expiryDate": {
    "type": "string",
    "format": "date-time",
    "description": "Expiry date and time; empty for open-ended",
    "nullable": true
   },
   "priority": {
    "type": "string",
    "enum": [
     "low",
     "normal",
     "high",
     "urgent"
    ],
    "description": "Priority; defaults to normal (decided 29 September, readiness close-out)"
   },
   "supportingNotes": {
    "type": "string",
    "description": "Supporting notes",
    "nullable": true
   },
   "attachments": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Attachment document IDs"
   },
   "reasonCode": {
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
   },
   "lines": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "objectType": {
       "type": "string",
       "enum": [
        "product",
        "rate",
        "priceList",
        "eligibilityRule",
        "tax",
        "fee",
        "formula",
        "currencyRounding"
       ],
       "description": "What this line changes"
      },
      "objectId": {
       "type": "string",
       "description": "ID of the product, rate, price list, rule, tax, fee or formula"
      },
      "venue": {
       "type": "string",
       "description": "Venue the line applies to; empty for all in scope",
       "nullable": true
      },
      "market": {
       "type": "string",
       "description": "Market the line applies to; empty for all in scope",
       "nullable": true
      },
      "proposedAmount": {
       "allOf": [
        {
         "$ref": "../shared/common.yaml#/components/schemas/Money"
        }
       ],
       "description": "Proposed amount for a monetary line; empty for removals and non-monetary changes",
       "nullable": true
      },
      "proposedValue": {
       "type": "string",
       "description": "Proposed value for a non-monetary line (rule, formula, rounding), as the target screen's own format",
       "nullable": true
      },
      "remove": {
       "type": "boolean",
       "description": "True when the line removes the rate or object (Rate Removal)"
      },
      "currentAmount": {
       "allOf": [
        {
         "$ref": "../shared/common.yaml#/components/schemas/Money"
        }
       ],
       "description": "Current live amount (Before)",
       "nullable": true
      },
      "differenceAmount": {
       "allOf": [
        {
         "$ref": "../shared/common.yaml#/components/schemas/Money"
        }
       ],
       "description": "Proposed minus current",
       "nullable": true
      },
      "differencePercent": {
       "type": "number",
       "description": "Difference in percent of the current amount",
       "nullable": true
      }
     },
     "description": "One changed object with before/after"
    },
    "description": "Change lines: one request may cover many products, rates, venues and markets"
   },
   "status": {
    "type": "string",
    "description": "Status: draft, pendingValidation, pendingApproval, returnedForModification, approved, scheduled, published, publicationFailed, rejected, cancelled or rolledBack; saving leaves it draft"
   },
   "approvalRequestId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "The `approvals.ApprovalRequest` opened by `submitPricingChangeRequest`; null while the request is a draft (decided 29 September, readiness close-out)."
   },
   "aiInsights": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "AI summary lines for this record: advisory only, never approves, publishes or changes a price"
   }
  }
 },
 "PricingDistributionSynchronizationPublicationMonitorView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Pricing Distribution, Synchronization & Publication Monitor displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "publicationStarted": {
    "type": "string",
    "format": "date-time",
    "description": "Publication started"
   },
   "lastUpdated": {
    "type": "string",
    "format": "date-time",
    "description": "Last updated"
   },
   "recordsPublished": {
    "type": "integer",
    "description": "Records published"
   },
   "recordsFailed": {
    "type": "integer",
    "description": "Records failed"
   },
   "latency": {
    "type": "number",
    "description": "Latency in seconds from publication start to confirmation",
    "nullable": true
   },
   "targetVersion": {
    "type": "string",
    "description": "Pricing version the target currently serves"
   },
   "publicationVersion": {
    "type": "string",
    "description": "Version being published"
   },
   "target": {
    "type": "string",
    "enum": [
     "b2c",
     "mobileApp",
     "pos",
     "mobilePos",
     "kiosk",
     "callCenter",
     "b2b",
     "reseller",
     "ota",
     "api",
     "cacheCdn",
     "externalSystem"
    ],
    "description": "Distribution Target (pack p.68)"
   },
   "targetName": {
    "type": "string",
    "description": "Named target where there are several, e.g. OTA A",
    "nullable": true
   },
   "status": {
    "type": "string",
    "description": "Status: pending, publishing, synchronized, warning, failed or suspended"
   },
   "currentProductionVersion": {
    "type": "string",
    "description": "Current production version"
   },
   "inSync": {
    "type": "boolean",
    "description": "Consistency check: targetVersion equals currentProductionVersion"
   },
   "failureReason": {
    "type": "string",
    "description": "Failure reason",
    "nullable": true
   }
  }
 },
 "PricingGovernanceCommandCenterSummary": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection; the headline tiles over the list, computed at read time for the filters in force",
  "description": "**The headline figures on Pricing Governance Command Center.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.",
  "properties": {
   "pricingChangesInDraft": {
    "type": "integer",
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
    "type": "integer",
    "description": "Published Today: change requests published since 00:00 venue time"
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
    "description": "Expiring Prices: rates whose expiry falls within the next 30 days (decided 29 September, readiness close-out)"
   },
   "governanceExceptions": {
    "type": "integer",
    "description": "Governance Exceptions: changes that breached a configured threshold, bypassed a step under emergency override, or await retrospective approval (decided 29 September, readiness close-out)"
   },
   "highRiskChanges": {
    "type": "integer",
    "description": "High-Risk Changes: open changes whose risk score is high or critical"
   },
   "governanceAlerts": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Governance Alerts (pack p.58), e.g. changes activating within 24 hours, changes over the configured commercial-change threshold, failed channel synchronizations"
   },
   "aiSummary": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "AI Governance Assistant summary lines: advisory only"
   }
  }
 },
 "PricingGovernanceCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Pricing Governance Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "changeId": {
    "type": "string",
    "description": "Change request ID"
   },
   "changeName": {
    "type": "string",
    "description": "Change name, e.g. Summer Admission 2027"
   },
   "changeType": {
    "type": "string",
    "enum": [
     "priceChange",
     "newRate",
     "rateRemoval",
     "priceListChange",
     "eligibilityRuleChange",
     "taxChange",
     "feeChange",
     "formulaChange",
     "currencyRoundingChange",
     "emergencyChange"
    ],
    "description": "Change Type (pack p.59)"
   },
   "scope": {
    "type": "string",
    "description": "Scope summary, e.g. \"24 products\", \"8 partners\", \"UAE\""
   },
   "revenueImpact": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Estimated revenue impact from the impact analysis; empty when not monetary (e.g. a regulatory VAT change)",
    "nullable": true
   },
   "impactNote": {
    "type": "string",
    "description": "Impact label when not monetary, e.g. Regulatory",
    "nullable": true
   },
   "requestedBy": {
    "type": "string",
    "description": "Requested by (user or team)"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   },
   "approver": {
    "type": "string",
    "description": "Current approver (role or user) awaited",
    "nullable": true
   },
   "riskLevel": {
    "type": "string",
    "enum": [
     "low",
     "medium",
     "high",
     "critical"
    ],
    "description": "Risk score from the impact analysis (pack p.64)"
   },
   "status": {
    "type": "string",
    "description": "Status: draft, pendingValidation, pendingApproval, returnedForModification, approved, scheduled, published, publicationFailed, rejected, cancelled or rolledBack"
   },
   "effectiveDate": {
    "type": "string",
    "format": "date-time",
    "description": "Effective date requested"
   }
  }
 },
 "PricingHistoryAuditComplianceExplorerView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Pricing History, Audit & Compliance Explorer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "changedBy": {
    "type": "string",
    "description": "Changed by (user, or the system actor)"
   },
   "dateTime": {
    "type": "string",
    "format": "date-time",
    "description": "Date/time"
   },
   "reason": {
    "type": "string",
    "description": "Reason",
    "nullable": true
   },
   "source": {
    "type": "string",
    "enum": [
     "backOffice",
     "bulkImport",
     "api",
     "dynamicPricingEngine",
     "rollback",
     "emergencyAction"
    ],
    "description": "Source of the change (decided 29 September, readiness close-out)"
   },
   "effectiveDate": {
    "type": "string",
    "format": "date-time",
    "description": "Effective date",
    "nullable": true
   },
   "publication": {
    "type": "string",
    "description": "Publication ID",
    "nullable": true
   },
   "auditId": {
    "type": "string",
    "description": "Audit entry ID"
   },
   "auditType": {
    "type": "string",
    "enum": [
     "configuration",
     "approval",
     "publication",
     "synchronization",
     "override",
     "rollback",
     "emergencyAction"
    ],
    "description": "Audit Type (pack p.71)"
   },
   "entityType": {
    "type": "string",
    "description": "What changed: price list, rate, rule, tax, fee, formula, strategy, guardrail..."
   },
   "entityId": {
    "type": "string",
    "description": "ID of what changed"
   },
   "field": {
    "type": "string",
    "description": "Field changed",
    "nullable": true
   },
   "oldValue": {
    "type": "string",
    "description": "Old value",
    "nullable": true
   },
   "newValue": {
    "type": "string",
    "description": "New value",
    "nullable": true
   },
   "changeRequestId": {
    "type": "string",
    "description": "Change request",
    "nullable": true
   },
   "approvalId": {
    "type": "string",
    "description": "Approval",
    "nullable": true
   },
   "version": {
    "type": "string",
    "description": "Pricing version",
    "nullable": true
   },
   "rollbackId": {
    "type": "string",
    "description": "Rollback, if applicable",
    "nullable": true
   }
  }
 },
 "PricingPublicationEffectiveDateSchedulerInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Pricing Publication & Effective-Date Scheduler submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "version": {
    "type": "string",
    "description": "Approved pricing version to publish"
   },
   "publicationDate": {
    "type": "string",
    "format": "date-time",
    "description": "Publish configuration at (empty for immediate)",
    "nullable": true
   },
   "effectiveDate": {
    "type": "string",
    "format": "date-time",
    "description": "Sales effective from; must not be in the past (never retroactive)"
   },
   "expiryDate": {
    "type": "string",
    "format": "date-time",
    "description": "Expiry; empty for open-ended",
    "nullable": true
   },
   "venue": {
    "type": "string",
    "description": "Scope: venue; empty for all venues in the version",
    "nullable": true
   },
   "market": {
    "type": "string",
    "description": "Scope: market; empty for all",
    "nullable": true
   },
   "channel": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/SalesChannel"
     }
    ],
    "nullable": true,
    "description": "Scope: channel; empty for all"
   },
   "changeRequestId": {
    "type": "string",
    "description": "Change request being published"
   },
   "publicationMode": {
    "type": "string",
    "enum": [
     "immediate",
     "scheduled",
     "futureEffectiveDate",
     "staged"
    ],
    "description": "Publication Mode (pack p.66)"
   },
   "visitEffectiveFrom": {
    "type": "string",
    "format": "date",
    "description": "Visit dates from which the new prices apply, when different from the sales effective date",
    "nullable": true
   },
   "stages": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "dimension": {
       "type": "string",
       "enum": [
        "market",
        "venue",
        "channel"
       ],
       "description": "Staged by"
      },
      "target": {
       "type": "string",
       "description": "Market, venue or channel ID"
      },
      "publicationDate": {
       "type": "string",
       "format": "date-time",
       "description": "Publish at"
      },
      "effectiveDate": {
       "type": "string",
       "format": "date-time",
       "description": "Effective from"
      }
     },
     "description": "One stage"
    },
    "description": "Stages for staged publication (market-by-market, venue-by-venue, channel-by-channel)"
   },
   "cancel": {
    "type": "boolean",
    "description": "True cancels this scheduled publication; allowed only before activation"
   }
  }
 },
 "PricingPublicationEffectiveDateSchedulerView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Pricing Publication & Effective-Date Scheduler displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "publicationDate": {
    "type": "string",
    "format": "date-time",
    "description": "Publish configuration at (empty for immediate)",
    "nullable": true
   },
   "effectiveDate": {
    "type": "string",
    "format": "date-time",
    "description": "Sales effective from; must not be in the past (never retroactive)"
   },
   "expiryDate": {
    "type": "string",
    "format": "date-time",
    "description": "Expiry; empty for open-ended",
    "nullable": true
   },
   "venue": {
    "type": "string",
    "description": "Scope: venue; empty for all venues in the version",
    "nullable": true
   },
   "market": {
    "type": "string",
    "description": "Scope: market; empty for all",
    "nullable": true
   },
   "channel": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/SalesChannel"
     }
    ],
    "nullable": true,
    "description": "Scope: channel; empty for all"
   },
   "version": {
    "type": "string",
    "description": "Approved pricing version to publish"
   },
   "changeRequestId": {
    "type": "string",
    "description": "Change request being published"
   },
   "publicationMode": {
    "type": "string",
    "enum": [
     "immediate",
     "scheduled",
     "futureEffectiveDate",
     "staged"
    ],
    "description": "Publication Mode (pack p.66)"
   },
   "visitEffectiveFrom": {
    "type": "string",
    "format": "date",
    "description": "Visit dates from which the new prices apply, when different from the sales effective date",
    "nullable": true
   },
   "stages": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "dimension": {
       "type": "string",
       "enum": [
        "market",
        "venue",
        "channel"
       ],
       "description": "Staged by"
      },
      "target": {
       "type": "string",
       "description": "Market, venue or channel ID"
      },
      "publicationDate": {
       "type": "string",
       "format": "date-time",
       "description": "Publish at"
      },
      "effectiveDate": {
       "type": "string",
       "format": "date-time",
       "description": "Effective from"
      }
     },
     "description": "One stage"
    },
    "description": "Stages for staged publication (market-by-market, venue-by-venue, channel-by-channel)"
   },
   "cancel": {
    "type": "boolean",
    "description": "True cancels this scheduled publication; allowed only before activation"
   },
   "prePublicationChecks": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "check": {
       "type": "string",
       "enum": [
        "approvalComplete",
        "validationPassed",
        "noCriticalConflicts",
        "dependenciesAvailable",
        "channelsReady",
        "effectiveDatesValid"
       ],
       "description": "Pre-Publication Check (pack p.67)"
      },
      "passed": {
       "type": "boolean",
       "description": "Passed"
      },
      "message": {
       "type": "string",
       "description": "Detail, e.g. the colliding version",
       "nullable": true
      }
     },
     "description": "One check"
    },
    "description": "Pre-publication check results"
   },
   "collisions": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Other versions scheduled to become effective for the same object and date"
   },
   "status": {
    "type": "string",
    "description": "Status: scheduled, blocked, published, cancelled or failed"
   }
  }
 },
 "PricingRollbackEmergencyControlCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Pricing Rollback & Emergency Control Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "productsAffected": {
    "type": "integer",
    "description": "Products affected"
   },
   "channelsAffected": {
    "type": "integer",
    "description": "Channels affected"
   },
   "transactionsSinceActivation": {
    "type": "integer",
    "description": "Transactions since the faulty version activated"
   },
   "revenueExposure": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Revenue exposure"
   },
   "existingOrders": {
    "type": "integer",
    "description": "Existing orders in scope; kept at the price they were sold at"
   },
   "futureSales": {
    "type": "integer",
    "description": "Future sales (unsold inventory) whose price the action changes"
   },
   "reason": {
    "type": "string",
    "description": "Reason"
   },
   "authorizedRole": {
    "type": "string",
    "description": "Role under which the action was authorised"
   },
   "incidentReference": {
    "type": "string",
    "description": "Incident reference",
    "nullable": true
   },
   "timestamp": {
    "type": "string",
    "format": "date-time",
    "description": "When the action was executed",
    "nullable": true
   },
   "actionId": {
    "type": "string",
    "description": "Action ID"
   },
   "actionType": {
    "type": "string",
    "enum": [
     "rollback",
     "freezePriceList",
     "freezeProductPricing",
     "freezeVenuePricing",
     "stopScheduledPublication",
     "stopDistribution",
     "restoreLastKnownGood"
    ],
    "description": "Rollback or Emergency Freeze control (pack pp.69-70)"
   },
   "rollbackTarget": {
    "type": "string",
    "enum": [
     "previousVersion",
     "selectedVersion",
     "previousPrice",
     "commercialBaseline"
    ],
    "description": "Rollback to",
    "nullable": true
   },
   "rollbackScope": {
    "type": "string",
    "enum": [
     "selectedProducts",
     "selectedVenue",
     "selectedMarket",
     "selectedChannel",
     "entirePublication"
    ],
    "description": "Rollback scope",
    "nullable": true
   },
   "scopeIds": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Products, venue, market or channel in scope"
   },
   "fromVersion": {
    "type": "string",
    "description": "Version in force before the action",
    "nullable": true
   },
   "toVersion": {
    "type": "string",
    "description": "Version restored",
    "nullable": true
   },
   "performedBy": {
    "type": "string",
    "description": "User who performed the action"
   },
   "retrospectiveApprovalRequired": {
    "type": "boolean",
    "description": "Retrospective approval required; true by default for emergency actions (decided 29 September, readiness close-out)"
   },
   "status": {
    "type": "string",
    "description": "Status: previewed, executed, awaitingRetrospectiveApproval, approved, failed or released"
   },
   "aiInsights": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "AI summary lines for this record: advisory only, never approves, publishes or changes a price"
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
    "description": "Version number, e.g. 5.3"
   },
   "priceList": {
    "type": "string",
    "description": "Price list name"
   },
   "createdDate": {
    "type": "string",
    "format": "date-time",
    "description": "Created date"
   },
   "effectiveDate": {
    "type": "string",
    "format": "date-time",
    "description": "Effective date",
    "nullable": true
   },
   "createdBy": {
    "type": "string",
    "description": "Created by"
   },
   "changeRequest": {
    "type": "string",
    "description": "Change request ID that produced the version",
    "nullable": true
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
    "type": "string",
    "description": "Status: draft, candidate, approved, scheduled, active, superseded, rolledBack or archived"
   },
   "added": {
    "type": "integer",
    "description": "Rates added compared with the compareTo version (default: the commercial baseline)"
   },
   "removed": {
    "type": "integer",
    "description": "Rates removed compared with the compareTo version"
   },
   "modified": {
    "type": "integer",
    "description": "Rates modified compared with the compareTo version"
   },
   "unchanged": {
    "type": "integer",
    "description": "Rates unchanged compared with the compareTo version"
   },
   "isCommercialBaseline": {
    "type": "boolean",
    "description": "Designated as the commercial baseline for its price list"
   }
  }
 }
}
```
