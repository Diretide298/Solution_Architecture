# WS44 — Product Lifecycle   Catalogue Governance board 2

**10 screens · 10 operations · 12 schemas · 2 permissions**

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
| `ADM-128` | Product Governance Command Center | listDetail | 1 | 0 | — |
| `ADM-129` | Approval Workflow Designer | configEditor | 1 | 0 | — |
| `ADM-130` | Approval Review & Decision Workspace | listDetail | 1 | 0 | — |
| `ADM-131` | Product Version Management | listDetail | 1 | 0 | — |
| `ADM-132` | Rollback & Recovery Management | listDetail | 1 | 0 | — |
| `ADM-133` | Change Impact Analysis | listDetail | 1 | 0 | — |
| `ADM-134` | Change Propagation & Dependency Control | listDetail | 1 | 0 | — |
| `ADM-135` | Product Retirement, Suspension & Archive | configEditor | 1 | 3 | — |
| `ADM-136` | Product Audit Trail & Change History | configEditor | 1 | 0 | — |
| `ADM-137` | Governance Risk, AI Monitoring & Control Center | listDetail | 1 | 0 | — |

## Thin screens in this batch

**ADM-130, ADM-131, ADM-132, ADM-133, ADM-134, ADM-137 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-128",
  "name": "Product Governance Command Center",
  "module": "Catalogue",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Product_Lifecycle___Catalogue_Governance_Reference.pdf",
   "board": "2",
   "number": "2.1",
   "page": 15
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/catalogue/product-governance-command-center-adm-128",
   "component": "apps/ticvai-web/src/routes/catalogue/ProductGovernanceCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-129",
    "ADM-130",
    "ADM-131",
    "ADM-132",
    "ADM-133",
    "ADM-134",
    "ADM-135",
    "ADM-136",
    "ADM-137"
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
     "to": "ADM-131",
     "trigger": "Product Version Management",
     "carries": [
      "productId"
     ],
     "provenance": "derived — ADM-131 declares entryState.params productId, so an edge into it must carry them"
    },
    {
     "to": "ADM-129",
     "trigger": "Works in Approval Workflow Designer",
     "provenance": "flow F153 step 1→2",
     "operation": "listProductGovernance"
    },
    {
     "to": "ADM-130",
     "trigger": "Works in Approval Review & Decision Workspace",
     "provenance": "flow F153 step 3→4",
     "operation": "listProductGovernance"
    },
    {
     "to": "ADM-132",
     "trigger": "Works in Rollback & Recovery Management",
     "provenance": "flow F153 step 7→8",
     "operation": "listProductGovernance"
    },
    {
     "to": "ADM-133",
     "trigger": "Works in Change Impact Analysis",
     "provenance": "flow F153 step 9→10",
     "operation": "listProductGovernance"
    },
    {
     "to": "ADM-134",
     "trigger": "Works in Change Propagation & Dependency Control",
     "provenance": "flow F153 step 11→12",
     "operation": "listProductGovernance"
    },
    {
     "to": "ADM-135",
     "trigger": "Works in Product Retirement, Suspension & Archive",
     "provenance": "flow F153 step 13→14",
     "operation": "listProductGovernance"
    },
    {
     "to": "ADM-136",
     "trigger": "Works in Product Audit Trail & Change History",
     "provenance": "flow F153 step 15→16",
     "operation": "listProductGovernance"
    },
    {
     "to": "ADM-137",
     "trigger": "Works in Governance Risk, AI Monitoring & Control Center",
     "provenance": "flow F153 step 17→18",
     "operation": "listProductGovernance"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§The dashboard shall display; Each record should display) and no metric row",
  "purpose": "Provide management and administrators with a single control center for all product governance activities.",
  "purposeNote": "Authorized users can identify every product requiring governance attention and prioritize actions from a single dashboard.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search product governance",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 15 §Filter by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "ProductGovernanceCommandCenterView.venue",
        "Product type",
        "Owner",
        "Department",
        "Status",
        "Risk",
        "ProductGovernanceCommandCenterView.changeType",
        "Approver",
        "ProductGovernanceCommandCenterView.effectiveDate",
        "Channel"
       ],
       "notes": "The pack filters this screen by venue, product type, owner, department, status, risk and 4 more — which are present is a decision the pack already made.",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 15 §Filter by"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every product governance",
       "columns": [
        "ProductGovernanceCommandCenterView.productsAwaitingApproval",
        "ProductGovernanceCommandCenterView.changesAwaitingApproval",
        "ProductGovernanceCommandCenterView.rejectedChanges",
        "ProductGovernanceCommandCenterView.productsWithGovernanceWarnings",
        "ProductGovernanceCommandCenterView.scheduledChanges",
        "ProductGovernanceCommandCenterView.productsWithUnpublishedChanges",
        "ProductGovernanceCommandCenterView.productsWithDependencyConflicts",
        "ProductGovernanceCommandCenterView.productsApproachingRetirement",
        "ProductGovernanceCommandCenterView.recentlyPublishedVersions",
        "Failed publications/rollbacks",
        "ProductGovernanceCommandCenterView.highRiskConfigurationChanges",
        "ProductGovernanceCommandCenterView.product",
        "ProductGovernanceCommandCenterView.venue",
        "ProductGovernanceCommandCenterView.productOwner",
        "ProductGovernanceCommandCenterView.changeType",
        "ProductGovernanceCommandCenterView.currentVersion",
        "ProductGovernanceCommandCenterView.proposedVersion",
        "ProductGovernanceCommandCenterView.requestedBy",
        "ProductGovernanceCommandCenterView.requestedDate",
        "ProductGovernanceCommandCenterView.riskLevel",
        "ProductGovernanceCommandCenterView.approvalStatus",
        "ProductGovernanceCommandCenterView.effectiveDate",
        "ProductGovernanceCommandCenterView.impactedChannels",
        "ProductGovernanceCommandCenterView.assignedApprover"
       ],
       "bindsTo": "ProductGovernanceCommandCenterView",
       "operation": "listProductGovernance",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 15 §The dashboard shall display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected product governance",
       "bindsTo": "ProductGovernanceCommandCenterView",
       "columns": [
        "ProductGovernanceCommandCenterView.productsAwaitingApproval",
        "ProductGovernanceCommandCenterView.changesAwaitingApproval",
        "ProductGovernanceCommandCenterView.rejectedChanges",
        "ProductGovernanceCommandCenterView.productsWithGovernanceWarnings",
        "ProductGovernanceCommandCenterView.scheduledChanges",
        "ProductGovernanceCommandCenterView.productsWithUnpublishedChanges",
        "ProductGovernanceCommandCenterView.productsWithDependencyConflicts",
        "ProductGovernanceCommandCenterView.productsApproachingRetirement",
        "ProductGovernanceCommandCenterView.recentlyPublishedVersions",
        "Failed publications/rollbacks",
        "ProductGovernanceCommandCenterView.highRiskConfigurationChanges",
        "ProductGovernanceCommandCenterView.product",
        "ProductGovernanceCommandCenterView.venue",
        "ProductGovernanceCommandCenterView.productOwner",
        "ProductGovernanceCommandCenterView.changeType",
        "ProductGovernanceCommandCenterView.currentVersion",
        "ProductGovernanceCommandCenterView.proposedVersion",
        "ProductGovernanceCommandCenterView.requestedBy",
        "ProductGovernanceCommandCenterView.requestedDate",
        "ProductGovernanceCommandCenterView.riskLevel",
        "ProductGovernanceCommandCenterView.approvalStatus",
        "ProductGovernanceCommandCenterView.effectiveDate",
        "ProductGovernanceCommandCenterView.impactedChannels",
        "ProductGovernanceCommandCenterView.assignedApprover"
       ],
       "notes": null,
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 15 §The dashboard shall display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The product governance list.",
   "error": "Could not load. Names which read failed and leaves the product governance untouched.",
   "emptyFirstRun": "No product governance yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the product governance are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listProductGovernance",
    "contract": "catalogue",
    "purpose": "Product Governance Command Center",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "ProductGovernanceCommandCenterView.productsAwaitingApproval",
    "ProductGovernanceCommandCenterView.changesAwaitingApproval",
    "ProductGovernanceCommandCenterView.rejectedChanges",
    "ProductGovernanceCommandCenterView.productsWithGovernanceWarnings",
    "ProductGovernanceCommandCenterView.scheduledChanges",
    "ProductGovernanceCommandCenterView.productsWithUnpublishedChanges"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-128"
  },
  "apisNote": "Regenerated 9 September 2026 from Product_Lifecycle___Catalogue_Governance_Reference.pdf page 15. 26 of 34 labels bound to a contract property; 34 of 41 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-129",
  "name": "Approval Workflow Designer",
  "module": "Catalogue",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Product_Lifecycle___Catalogue_Governance_Reference.pdf",
   "board": "2",
   "number": "2.2",
   "page": 17
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/catalogue/approval-workflow-designer-adm-129",
   "component": "apps/ticvai-web/src/routes/catalogue/ApprovalWorkflowDesigner.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-128"
   ],
   "exitTo": [
    "ADM-128"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-128, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-128",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F153 step 2→3",
     "operation": "approveWorkflow"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Each workflow can define; Tax configuration) and no display directory — it is settings, not a population",
  "purpose": "Configure reusable approval workflows governing product creation and modification.",
  "purposeNote": "Administrators can configure product approval workflows without development work and route different types of changes through different approval paths.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Workflow name",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 17 §Each workflow can define"
      },
      {
       "kind": "selectField",
       "label": "Applicable product types",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 17 §Each workflow can define"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 17 §Each workflow can define"
      },
      {
       "kind": "selectField",
       "label": "Department",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 17 §Each workflow can define"
      },
      {
       "kind": "selectField",
       "label": "Change type",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 17 §Each workflow can define"
      },
      {
       "kind": "selectField",
       "label": "Approval stages",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 17 §Each workflow can define"
      },
      {
       "kind": "selectField",
       "label": "Approver role",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 17 §Each workflow can define"
      },
      {
       "kind": "selectField",
       "label": "Specific approver",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 17 §Each workflow can define"
      },
      {
       "kind": "selectField",
       "label": "Approval group",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 17 §Each workflow can define"
      },
      {
       "kind": "selectField",
       "label": "Sequential/parallel approval",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 17 §Each workflow can define"
      },
      {
       "kind": "selectField",
       "label": "Mandatory/optional stage",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 17 §Each workflow can define"
      },
      {
       "kind": "selectField",
       "label": "SLA",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 17 §Each workflow can define"
      },
      {
       "kind": "selectField",
       "label": "Escalation",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 17 §Each workflow can define"
      },
      {
       "kind": "selectField",
       "label": "Delegation",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 17 §Each workflow can define"
      },
      {
       "kind": "selectField",
       "label": "Reminder frequency",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 17 §Each workflow can define"
      },
      {
       "kind": "selectField",
       "label": "Rejection behavior",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 17 §Each workflow can define"
      },
      {
       "kind": "selectField",
       "label": "Resubmission behavior",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 17 §Each workflow can define"
      },
      {
       "kind": "selectField",
       "label": "→ Finance",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 17 §Tax configuration"
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
       "provenance": "contract operation approveWorkflow"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The approval workflow designer configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the approval workflow designer untouched.",
   "emptyFirstRun": "No approval workflow designer configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "approveWorkflow",
    "contract": "catalogue",
    "purpose": "Approval Workflow Designer",
    "trigger": "onAction",
    "invalidates": [
     "approveWorkflow"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-129"
  },
  "apisNote": "Regenerated 9 September 2026 from Product_Lifecycle___Catalogue_Governance_Reference.pdf page 17. 0 of 0 labels bound to a contract property; 18 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-130",
  "name": "Approval Review & Decision Workspace",
  "module": "Catalogue",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Product_Lifecycle___Catalogue_Governance_Reference.pdf",
   "board": "2",
   "number": "2.3",
   "page": 18
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/catalogue/approval-review-decision-workspace-adm-130",
   "component": "apps/ticvai-web/src/routes/catalogue/ApprovalReviewDecisionWorkspace.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-128"
   ],
   "exitTo": [
    "ADM-128"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-128, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-128",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F153 step 4→5",
     "operation": "approveReviewDecision"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Give approvers a clear interface for reviewing a proposed product or product change before making a decision.",
  "purposeNote": "An approver can understand exactly what is changing, why it is changing and what it may affect before approving or rejecting the request.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 18"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 18"
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
       "label": "Approve",
       "provenance": "contract operation approveReviewDecision"
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
       "impliedBy": "approveReviewDecision"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The approval review decision list.",
   "error": "Could not load. Names which read failed and leaves the approval review decision untouched.",
   "emptyFirstRun": "No approval review decision yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the approval review decision are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "approveReviewDecision",
    "contract": "catalogue",
    "purpose": "Approval Review & Decision Workspace",
    "trigger": "onAction",
    "invalidates": [
     "approveReviewDecision"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-130"
  },
  "apisNote": "Regenerated 9 September 2026 from Product_Lifecycle___Catalogue_Governance_Reference.pdf page 18. 0 of 0 labels bound to a contract property; 0 of 34 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-131",
  "name": "Product Version Management",
  "module": "Catalogue",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Product_Lifecycle___Catalogue_Governance_Reference.pdf",
   "board": "2",
   "number": "2.4",
   "page": 19
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/catalogue/product-version-management-adm-131",
   "component": "apps/ticvai-web/src/routes/catalogue/ProductVersionManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-128"
   ],
   "exitTo": [
    "ADM-128"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-128, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-128",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F153 step 6→7",
     "operation": "listProductVersions"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Maintain controlled versions of every governed product configuration. The source matrix specifically requires version history for products and the ability to roll back to earlier versions.",
  "purposeNote": "Every governed product modification creates a traceable version, and authorized users can compare any two versions.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Pricing. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 19 §Users can compare"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 19"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 19"
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
       "label": "Pricing",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 19 §Users can compare"
      }
     ]
    },
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listProductVersions",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The product version list.",
   "error": "Could not load. Names which read failed and leaves the product version untouched.",
   "emptyFirstRun": "No product version yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the product version are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listProductVersions",
    "contract": "catalogue",
    "purpose": "What this product used to be",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "productId",
     "from": "navigation"
    }
   ],
   "coldEntry": "**Reached from the list that owns it**, so the identifier arrives with the navigation. Opened cold without one, the screen says what is missing and offers that list — never an empty form that looks configurable.",
   "preloaded": [
    "ProductVersion.productId",
    "ProductVersion.publishedAt",
    "ProductVersion.publishedByPrincipalId",
    "ProductVersion.note",
    "ProductVersion.isCurrent"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-131"
  },
  "apisNote": "Regenerated 9 September 2026 from Product_Lifecycle___Catalogue_Governance_Reference.pdf page 19. 0 of 0 labels bound to a contract property; 1 of 37 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-132",
  "name": "Rollback & Recovery Management",
  "module": "Catalogue",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Product_Lifecycle___Catalogue_Governance_Reference.pdf",
   "board": "2",
   "number": "2.5",
   "page": 20
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/catalogue/rollback-recovery-management-adm-132",
   "component": "apps/ticvai-web/src/routes/catalogue/RollbackRecoveryManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-128"
   ],
   "exitTo": [
    "ADM-128"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-128, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-128",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F153 step 8→9",
     "operation": "listRollbackRecovery"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Safely restore an earlier product configuration when a newly published configuration causes an issue.",
  "purposeNote": "An authorized user can restore a safe earlier configuration without corrupting historical sales, reservations or issued entitlements.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 20"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 20"
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
       "impliedBy": "listRollbackRecovery",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The rollback recovery list.",
   "error": "Could not load. Names which read failed and leaves the rollback recovery untouched.",
   "emptyFirstRun": "No rollback recovery yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the rollback recovery are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listRollbackRecovery",
    "contract": "catalogue",
    "purpose": "Rollback & Recovery Management",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "RollbackRecoveryManagementView.identifyDependencies",
    "RollbackRecoveryManagementView.enterRollbackReason",
    "RollbackRecoveryManagementView.executeImmediateRollbackWhereAuthorized",
    "RollbackRecoveryManagementView.monitorRollbackStatus",
    "RollbackRecoveryManagementView.entireProduct"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-132"
  },
  "apisNote": "Regenerated 9 September 2026 from Product_Lifecycle___Catalogue_Governance_Reference.pdf page 20. 0 of 0 labels bound to a contract property; 0 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-133",
  "name": "Change Impact Analysis",
  "module": "Catalogue",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Product_Lifecycle___Catalogue_Governance_Reference.pdf",
   "board": "2",
   "number": "2.6",
   "page": 21
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/catalogue/change-impact-analysis-adm-133",
   "component": "apps/ticvai-web/src/routes/catalogue/ChangeImpactAnalysis.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-128"
   ],
   "exitTo": [
    "ADM-128"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-128, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-128",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F153 step 10→11",
     "operation": "listChangeImpactAnalysis"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Show administrators what will be affected before a product change is approved or published. This directly addresses the matrix requirement to perform impact analysis before product changes are published.",
  "purposeNote": "Before a material configuration change is approved or published, authorized users can see its potential cross-module and transactional impact.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 21"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 21"
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
       "impliedBy": "listChangeImpactAnalysis",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The change impact analysis list.",
   "error": "Could not load. Names which read failed and leaves the change impact analysis untouched.",
   "emptyFirstRun": "No change impact analysis yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the change impact analysis are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listChangeImpactAnalysis",
    "contract": "catalogue",
    "purpose": "Change Impact Analysis",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "ChangeImpactAnalysisView.futureOrders",
    "ChangeImpactAnalysisView.reservations",
    "ChangeImpactAnalysisView.issuedTickets",
    "ChangeImpactAnalysisView.capacity",
    "ChangeImpactAnalysisView.pricing"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-133"
  },
  "apisNote": "Regenerated 9 September 2026 from Product_Lifecycle___Catalogue_Governance_Reference.pdf page 21. 0 of 0 labels bound to a contract property; 0 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-134",
  "name": "Change Propagation & Dependency Control",
  "module": "Catalogue",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Product_Lifecycle___Catalogue_Governance_Reference.pdf",
   "board": "2",
   "number": "2.7",
   "page": 22
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/catalogue/change-propagation-dependency-control-adm-134",
   "component": "apps/ticvai-web/src/routes/catalogue/ChangePropagationDependencyControl.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-128"
   ],
   "exitTo": [
    "ADM-128"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-128, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-128",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F153 step 12→13",
     "operation": "listChangePropagationDependency"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Control whether approved product changes should automatically propagate to related products or dependent configurations. The source matrix requires controlled propagation of changes to linked products.",
  "purposeNote": "Product changes can propagate through defined relationships without unintentionally overwriting approved local exceptions.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 22"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 22"
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
       "impliedBy": "listChangePropagationDependency",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The change propagation dependency list.",
   "error": "Could not load. Names which read failed and leaves the change propagation dependency untouched.",
   "emptyFirstRun": "No change propagation dependency yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the change propagation dependency are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listChangePropagationDependency",
    "contract": "catalogue",
    "purpose": "Change Propagation & Dependency Control",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "ChangePropagationDependencyControlView.typesType",
    "ChangePropagationDependencyControlView.adultAdmission",
    "ChangePropagationDependencyControlView.childAdmission",
    "ChangePropagationDependencyControlView.seniorAdmission",
    "ChangePropagationDependencyControlView.residentAdmission"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-134"
  },
  "apisNote": "Regenerated 9 September 2026 from Product_Lifecycle___Catalogue_Governance_Reference.pdf page 22. 0 of 0 labels bound to a contract property; 0 of 27 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-135",
  "name": "Product Retirement, Suspension & Archive",
  "module": "Catalogue",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Product_Lifecycle___Catalogue_Governance_Reference.pdf",
   "board": "2",
   "number": "2.8",
   "page": 23
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/catalogue/product-retirement-suspension-archive-adm-135",
   "component": "apps/ticvai-web/src/routes/catalogue/ProductRetirementSuspensionArchive.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-128"
   ],
   "exitTo": [
    "ADM-128"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-128, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-128",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F153 step 14→15",
     "operation": "listProductRetirementSuspension"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Administrator defines) and no display directory — it is settings, not a population",
  "purpose": "Provide a governed end-of-life process for products. The source matrix explicitly requires disabling or retiring products without affecting previously sold tickets.",
  "purposeNote": "A product can be safely removed from future sale while protecting existing valid customer transactions and identifying unresolved dependencies.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 5 actions on this screen and the screen declares 1 operation.** Unserved: Suspend Sales, Temporarily Disable, End Sale, Archive. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 23 §Available Actions"
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
       "label": "Retirement date",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 23 §Administrator defines"
      },
      {
       "kind": "selectField",
       "label": "End-of-sale date",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 23 §Administrator defines"
      },
      {
       "kind": "selectField",
       "label": "Channels",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 23 §Administrator defines"
      },
      {
       "kind": "selectField",
       "label": "Reason",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 23 §Administrator defines"
      },
      {
       "kind": "selectField",
       "label": "Replacement product",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 23 §Administrator defines"
      },
      {
       "kind": "selectField",
       "label": "Existing reservation treatment",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 23 §Administrator defines"
      },
      {
       "kind": "selectField",
       "label": "Existing ticket treatment",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 23 §Administrator defines"
      },
      {
       "kind": "selectField",
       "label": "Communication requirements",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 23 §Administrator defines"
      },
      {
       "kind": "selectField",
       "label": "Reporting treatment",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 23 §Administrator defines"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "destructiveButton",
       "label": "Suspend Sales",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 23 §Available Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Temporarily Disable",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 23 §Available Actions"
      },
      {
       "kind": "destructiveButton",
       "label": "End Sale",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 23 §Available Actions"
      },
      {
       "kind": "secondaryButton",
       "label": "Retire",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 23 §Available Actions"
      },
      {
       "kind": "destructiveButton",
       "label": "Archive",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 23 §Available Actions"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmSuspendSales",
    "component": "confirmDialog",
    "trigger": "Suspend Sales",
    "body": "**Suspend Sales on a product retirement suspension is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 23 §Available Actions"
   },
   {
    "id": "confirmEndSale",
    "component": "confirmDialog",
    "trigger": "End Sale",
    "body": "**End Sale on a product retirement suspension is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 23 §Available Actions"
   },
   {
    "id": "confirmArchive",
    "component": "confirmDialog",
    "trigger": "Archive",
    "body": "**Archive on a product retirement suspension is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 23 §Available Actions"
   }
  ],
  "states": {
   "loading": "The product retirement suspension configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the product retirement suspension untouched.",
   "emptyFirstRun": "No product retirement suspension configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listProductRetirementSuspension",
    "contract": "catalogue",
    "purpose": "Product Retirement, Suspension & Archive",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-135"
  },
  "apisNote": "Regenerated 9 September 2026 from Product_Lifecycle___Catalogue_Governance_Reference.pdf page 23. 0 of 0 labels bound to a contract property; 14 of 30 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-136",
  "name": "Product Audit Trail & Change History",
  "module": "Catalogue",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Product_Lifecycle___Catalogue_Governance_Reference.pdf",
   "board": "2",
   "number": "2.9",
   "page": 24
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/catalogue/product-audit-trail-change-history-adm-136",
   "component": "apps/ticvai-web/src/routes/catalogue/ProductAuditTrailChangeHistory.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-128"
   ],
   "exitTo": [
    "ADM-128"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-128, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-128",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F153 step 16→17",
     "operation": "listProductTrailChange"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Each entry should capture) and no display directory — it is settings, not a population",
  "purpose": "Provide a complete, immutable history of product configuration and governance activity. The matrix requires tracking configuration changes with timestamps and user information.",
  "purposeNote": "Every material product configuration and governance action is traceable to who performed it, when it occurred, what changed and under which approval.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search product audit trail",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 24 §Filter by"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "ProductAuditTrailChangeHistoryView.product",
        "ProductAuditTrailChangeHistoryView.user",
        "Date",
        "ProductAuditTrailChangeHistoryView.action",
        "ProductAuditTrailChangeHistoryView.version",
        "ProductAuditTrailChangeHistoryView.configurationArea",
        "Venue",
        "Approval",
        "Risk",
        "ProductAuditTrailChangeHistoryView.environment"
       ],
       "notes": "The pack filters this screen by product, user, date, action, version, configuration area and 4 more — which are present is a decision the pack already made.",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 24 §Filter by"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Date/time",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 24 §Each entry should capture"
      },
      {
       "kind": "selectField",
       "label": "User",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 24 §Each entry should capture"
      },
      {
       "kind": "selectField",
       "label": "Role",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 24 §Each entry should capture"
      },
      {
       "kind": "selectField",
       "label": "Product",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 24 §Each entry should capture"
      },
      {
       "kind": "selectField",
       "label": "Version",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 24 §Each entry should capture"
      },
      {
       "kind": "selectField",
       "label": "Action",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 24 §Each entry should capture"
      },
      {
       "kind": "selectField",
       "label": "Configuration area",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 24 §Each entry should capture"
      },
      {
       "kind": "selectField",
       "label": "Previous value",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 24 §Each entry should capture"
      },
      {
       "kind": "selectField",
       "label": "New value",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 24 §Each entry should capture"
      },
      {
       "kind": "selectField",
       "label": "Reason",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 24 §Each entry should capture"
      },
      {
       "kind": "selectField",
       "label": "Approval reference",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 24 §Each entry should capture"
      },
      {
       "kind": "selectField",
       "label": "Source channel",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 24 §Each entry should capture"
      },
      {
       "kind": "selectField",
       "label": "Environment",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 24 §Each entry should capture"
      },
      {
       "kind": "textField",
       "label": "IP/device metadata where applicable",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 24 §Each entry should capture"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The product audit trail configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the product audit trail untouched.",
   "emptyFirstRun": "No product audit trail configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoResults": "The filter narrowed it and the product audit trail are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listProductTrailChange",
    "contract": "catalogue",
    "purpose": "Product Audit Trail & Change History",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-136"
  },
  "apisNote": "Regenerated 9 September 2026 from Product_Lifecycle___Catalogue_Governance_Reference.pdf page 24. 6 of 10 labels bound to a contract property; 24 of 34 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-137",
  "name": "Governance Risk, AI Monitoring & Control Center",
  "module": "Catalogue",
  "requiresModule": "ticketing",
  "wave": 3,
  "source": {
   "pack": "Product_Lifecycle___Catalogue_Governance_Reference.pdf",
   "board": "2",
   "number": "2.10",
   "page": 26
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/catalogue/governance-risk-ai-monitoring-control-center-adm-137",
   "component": "apps/ticvai-web/src/routes/catalogue/GovernanceRiskAiMonitoringControlCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-128"
   ],
   "exitTo": [
    "ADM-128"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-128, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation."
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Use TICVAI intelligence to continuously identify catalogue governance risks rather than relying entirely on administrators to discover them manually.",
  "purposeNote": "Administrators receive proactive governance intelligence with clear explanations and recommended actions while material product decisions remain controlled by the configured authorization framework. Board 2 — Final Screen Register",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every governance risk monitoring",
       "columns": [
        "Critical / High / Medium / Low",
        "GovernanceRiskAiMonitoringControlCenterView.risk",
        "GovernanceRiskAiMonitoringControlCenterView.product",
        "GovernanceRiskAiMonitoringControlCenterView.venue",
        "GovernanceRiskAiMonitoringControlCenterView.businessImpact",
        "GovernanceRiskAiMonitoringControlCenterView.recommendedAction",
        "GovernanceRiskAiMonitoringControlCenterView.owner",
        "GovernanceRiskAiMonitoringControlCenterView.dueDate",
        "GovernanceRiskAiMonitoringControlCenterView.status"
       ],
       "bindsTo": "GovernanceRiskAiMonitoringControlCenterView",
       "operation": "listGovernanceRiskMonitoring",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 26 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected governance risk monitoring",
       "bindsTo": "GovernanceRiskAiMonitoringControlCenterView",
       "columns": [
        "Critical / High / Medium / Low",
        "GovernanceRiskAiMonitoringControlCenterView.risk",
        "GovernanceRiskAiMonitoringControlCenterView.product",
        "GovernanceRiskAiMonitoringControlCenterView.venue",
        "GovernanceRiskAiMonitoringControlCenterView.businessImpact",
        "GovernanceRiskAiMonitoringControlCenterView.recommendedAction",
        "GovernanceRiskAiMonitoringControlCenterView.owner",
        "GovernanceRiskAiMonitoringControlCenterView.dueDate",
        "GovernanceRiskAiMonitoringControlCenterView.status"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Potential duplicate detected”, “Governance warning”, “Backend Screen Primary Responsibility”, “Restore previous”, “Pre-change impact”.",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 26 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The governance risk monitoring list.",
   "error": "Could not load. Names which read failed and leaves the governance risk monitoring untouched.",
   "emptyFirstRun": "No governance risk monitoring yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the governance risk monitoring are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listGovernanceRiskMonitoring",
    "contract": "catalogue",
    "purpose": "Governance Risk, AI Monitoring & Control Center",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "Critical / High / Medium / Low",
    "GovernanceRiskAiMonitoringControlCenterView.risk",
    "GovernanceRiskAiMonitoringControlCenterView.product",
    "GovernanceRiskAiMonitoringControlCenterView.venue",
    "GovernanceRiskAiMonitoringControlCenterView.businessImpact",
    "GovernanceRiskAiMonitoringControlCenterView.recommendedAction"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-137"
  },
  "apisNote": "Regenerated 9 September 2026 from Product_Lifecycle___Catalogue_Governance_Reference.pdf page 26. 8 of 9 labels bound to a contract property; 9 of 55 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "approveReviewDecision": {
  "method": "PUT",
  "path": "/review-decision",
  "contract": "catalogue",
  "summary": "Approval Review & Decision Workspace",
  "permission": "PRODUCT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "ApprovalReviewDecisionWorkspaceInput",
  "responds": "ApprovalReviewDecisionWorkspaceView"
 },
 "approveWorkflow": {
  "method": "PUT",
  "path": "/workflow",
  "contract": "catalogue",
  "summary": "Approval Workflow Designer",
  "permission": "PRODUCT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "ApprovalWorkflowDesignerInput",
  "responds": "ApprovalWorkflowDesignerView"
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
  "parameters": [],
  "requestBody": null,
  "responds": "ChangeImpactAnalysisView"
 },
 "listChangePropagationDependency": {
  "method": "GET",
  "path": "/change-propagation-dependency",
  "contract": "catalogue",
  "summary": "Change Propagation & Dependency Control",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ChangePropagationDependencyControlView"
 },
 "listGovernanceRiskMonitoring": {
  "method": "GET",
  "path": "/governance-risk-monitoring",
  "contract": "catalogue",
  "summary": "Governance Risk, AI Monitoring & Control Center",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "GovernanceRiskAiMonitoringControlCenterView"
 },
 "listProductGovernance": {
  "method": "GET",
  "path": "/product-governance",
  "contract": "catalogue",
  "summary": "Product Governance Command Center",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "productType",
    "in": "query",
    "required": false
   },
   {
    "name": "owner",
    "in": "query",
    "required": false
   },
   {
    "name": "department",
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
    "name": "approver",
    "in": "query",
    "required": false
   },
   {
    "name": "channel",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "ProductGovernanceCommandCenterView"
 },
 "listProductRetirementSuspension": {
  "method": "GET",
  "path": "/product-retirement-suspension",
  "contract": "catalogue",
  "summary": "Product Retirement, Suspension & Archive",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ProductRetirementSuspensionArchiveView"
 },
 "listProductTrailChange": {
  "method": "GET",
  "path": "/product-trail-change",
  "contract": "catalogue",
  "summary": "Product Audit Trail & Change History",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "date",
    "in": "query",
    "required": false
   },
   {
    "name": "venue",
    "in": "query",
    "required": false
   },
   {
    "name": "approval",
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
  "responds": "ProductAuditTrailChangeHistoryView"
 },
 "listProductVersions": {
  "method": "GET",
  "path": "/products/{productId}/versions",
  "contract": "catalogue",
  "summary": "What this product used to be",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ProductVersion"
 },
 "listRollbackRecovery": {
  "method": "GET",
  "path": "/rollback-recovery",
  "contract": "catalogue",
  "summary": "Rollback & Recovery Management",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "RollbackRecoveryManagementView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "ApprovalReviewDecisionWorkspaceInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Approval Review & Decision Workspace submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "onD": {
    "type": "string",
    "description": "on d"
   },
   "refundableLe": {
    "type": "string",
    "description": "refundable le"
   },
   "requestChanges": {
    "type": "string",
    "description": "Request Changes"
   },
   "reassign": {
    "type": "string",
    "description": "Reassign"
   },
   "delegate": {
    "type": "string",
    "description": "Delegate"
   },
   "requester": {
    "type": "string",
    "description": "Requester"
   },
   "reasonForChange": {
    "type": "string",
    "description": "Reason for change"
   },
   "businessJustification": {
    "type": "string",
    "description": "Business justification"
   },
   "attachments": {
    "type": "string",
    "description": "Attachments"
   },
   "effectiveDate": {
    "type": "string",
    "format": "date-time",
    "description": "Effective date"
   },
   "currentSales": {
    "type": "string",
    "description": "Current sales"
   },
   "futureReservations": {
    "type": "string",
    "description": "Future reservations"
   },
   "channelsAffected": {
    "type": "string",
    "description": "Channels affected"
   },
   "pricingImpact": {
    "type": "string",
    "description": "Pricing impact"
   },
   "capacityImpact": {
    "type": "integer",
    "description": "Capacity impact"
   },
   "financeImpact": {
    "type": "string",
    "description": "Finance impact"
   },
   "accessImpact": {
    "type": "string",
    "description": "Access impact"
   }
  }
 },
 "ApprovalReviewDecisionWorkspaceView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Approval Review & Decision Workspace displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "onD": {
    "type": "string",
    "description": "on d"
   },
   "refundableLe": {
    "type": "string",
    "description": "refundable le"
   },
   "requestChanges": {
    "type": "string",
    "description": "Request Changes"
   },
   "reassign": {
    "type": "string",
    "description": "Reassign"
   },
   "delegate": {
    "type": "string",
    "description": "Delegate"
   },
   "requester": {
    "type": "string",
    "description": "Requester"
   },
   "reasonForChange": {
    "type": "string",
    "description": "Reason for change"
   },
   "businessJustification": {
    "type": "string",
    "description": "Business justification"
   },
   "attachments": {
    "type": "string",
    "description": "Attachments"
   },
   "effectiveDate": {
    "type": "string",
    "format": "date-time",
    "description": "Effective date"
   },
   "currentSales": {
    "type": "string",
    "description": "Current sales"
   },
   "futureReservations": {
    "type": "string",
    "description": "Future reservations"
   },
   "channelsAffected": {
    "type": "string",
    "description": "Channels affected"
   },
   "pricingImpact": {
    "type": "string",
    "description": "Pricing impact"
   },
   "capacityImpact": {
    "type": "integer",
    "description": "Capacity impact"
   },
   "financeImpact": {
    "type": "string",
    "description": "Finance impact"
   },
   "accessImpact": {
    "type": "string",
    "description": "Access impact"
   }
  }
 },
 "ApprovalWorkflowDesignerInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Approval Workflow Designer submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "workflowName": {
    "type": "string",
    "description": "Workflow name"
   },
   "applicableProductTypes": {
    "type": "string",
    "description": "Applicable product types"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "department": {
    "type": "string",
    "description": "Department"
   },
   "changeType": {
    "type": "string",
    "description": "Change type"
   },
   "approvalStages": {
    "type": "string",
    "description": "Approval stages"
   },
   "approverRole": {
    "type": "string",
    "description": "Approver role"
   },
   "specificApprover": {
    "type": "string",
    "description": "Specific approver"
   },
   "approvalGroup": {
    "type": "string",
    "description": "Approval group"
   },
   "sequentialParallelApproval": {
    "type": "string",
    "description": "Sequential/parallel approval"
   },
   "mandatoryOptionalStage": {
    "type": "string",
    "description": "Mandatory/optional stage"
   },
   "sla": {
    "type": "string",
    "description": "SLA"
   },
   "escalation": {
    "type": "string",
    "description": "Escalation"
   },
   "delegation": {
    "type": "string",
    "description": "Delegation"
   },
   "reminderFrequency": {
    "type": "string",
    "description": "Reminder frequency"
   },
   "rejectionBehavior": {
    "type": "string",
    "description": "Rejection behavior"
   },
   "resubmissionBehavior": {
    "type": "string",
    "description": "Resubmission behavior"
   }
  }
 },
 "ApprovalWorkflowDesignerView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Approval Workflow Designer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "workflowName": {
    "type": "string",
    "description": "Workflow name"
   },
   "applicableProductTypes": {
    "type": "string",
    "description": "Applicable product types"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "department": {
    "type": "string",
    "description": "Department"
   },
   "changeType": {
    "type": "string",
    "description": "Change type"
   },
   "approvalStages": {
    "type": "string",
    "description": "Approval stages"
   },
   "approverRole": {
    "type": "string",
    "description": "Approver role"
   },
   "specificApprover": {
    "type": "string",
    "description": "Specific approver"
   },
   "approvalGroup": {
    "type": "string",
    "description": "Approval group"
   },
   "sequentialParallelApproval": {
    "type": "string",
    "description": "Sequential/parallel approval"
   },
   "mandatoryOptionalStage": {
    "type": "string",
    "description": "Mandatory/optional stage"
   },
   "sla": {
    "type": "string",
    "description": "SLA"
   },
   "escalation": {
    "type": "string",
    "description": "Escalation"
   },
   "delegation": {
    "type": "string",
    "description": "Delegation"
   },
   "reminderFrequency": {
    "type": "string",
    "description": "Reminder frequency"
   },
   "rejectionBehavior": {
    "type": "string",
    "description": "Rejection behavior"
   },
   "resubmissionBehavior": {
    "type": "string",
    "description": "Resubmission behavior"
   }
  }
 },
 "ChangeImpactAnalysisView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Change Impact Analysis displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "futureOrders": {
    "type": "string",
    "description": "Future orders"
   },
   "reservations": {
    "type": "string",
    "description": "Reservations"
   },
   "issuedTickets": {
    "type": "string",
    "description": "Issued tickets"
   },
   "capacity": {
    "type": "integer",
    "description": "Capacity"
   },
   "pricing": {
    "type": "string",
    "description": "Pricing"
   },
   "tax": {
    "type": "string",
    "description": "Tax"
   },
   "promotions": {
    "type": "string",
    "description": "Promotions"
   },
   "membership": {
    "type": "string",
    "description": "Membership"
   },
   "entitlements": {
    "type": "string",
    "description": "Entitlements"
   },
   "accessControl": {
    "type": "string",
    "description": "Access control"
   },
   "salesChannels": {
    "type": "string",
    "description": "Sales channels"
   },
   "b2bPartners": {
    "type": "string",
    "description": "B2B partners"
   },
   "otas": {
    "type": "string",
    "description": "OTAs"
   },
   "pos": {
    "type": "string",
    "description": "POS"
   },
   "b2c": {
    "type": "string",
    "description": "B2C"
   },
   "kiosk": {
    "type": "string",
    "description": "Kiosk"
   },
   "media": {
    "type": "string",
    "description": "Media"
   },
   "finance": {
    "type": "string",
    "description": "Finance"
   },
   "reporting": {
    "type": "string",
    "description": "Reporting"
   },
   "low": {
    "type": "string",
    "description": "Low"
   },
   "medium": {
    "type": "string",
    "description": "Medium"
   },
   "high": {
    "type": "string",
    "description": "High"
   },
   "critical": {
    "type": "string",
    "description": "Critical"
   }
  }
 },
 "ChangePropagationDependencyControlView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Change Propagation & Dependency Control displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "typesType": {
    "type": "string",
    "enum": [
     "parentProduct",
     "childProduct",
     "bundle",
     "addOn",
     "upgrade",
     "membership",
     "package",
     "promotion",
     "priceProfile",
     "capacityPool",
     "entitlement",
     "salesChannel",
     "mediaTemplate"
    ],
    "description": "Vocabulary listed under Dependency Types."
   },
   "adultAdmission": {
    "type": "string",
    "description": "Adult Admission"
   },
   "childAdmission": {
    "type": "string",
    "description": "Child Admission"
   },
   "seniorAdmission": {
    "type": "string",
    "description": "Senior Admission"
   },
   "residentAdmission": {
    "type": "string",
    "description": "Resident Admission"
   },
   "propagates": {
    "type": "string",
    "description": "propagates"
   },
   "overwritten": {
    "type": "string",
    "description": "overwritten"
   }
  }
 },
 "GovernanceRiskAiMonitoringControlCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Governance Risk, AI Monitoring & Control Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "with": {
    "type": "string",
    "description": "with"
   },
   "risk": {
    "type": "string",
    "description": "Risk"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "businessImpact": {
    "type": "string",
    "description": "Business impact"
   },
   "recommendedAction": {
    "type": "string",
    "description": "Recommended action"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   },
   "dueDate": {
    "type": "string",
    "format": "date-time",
    "description": "Due date"
   },
   "status": {
    "type": "integer",
    "description": "Status"
   },
   "configurations": {
    "type": "string",
    "description": "configurations"
   },
   "assessment": {
    "type": "string",
    "description": "assessment"
   }
  }
 },
 "ProductAuditTrailChangeHistoryView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Product Audit Trail & Change History displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "dateTime": {
    "type": "string",
    "format": "date-time",
    "description": "Date/time"
   },
   "user": {
    "type": "string",
    "description": "User"
   },
   "role": {
    "type": "string",
    "description": "Role"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "version": {
    "type": "string",
    "description": "Version"
   },
   "action": {
    "type": "string",
    "description": "Action"
   },
   "configurationArea": {
    "type": "string",
    "description": "Configuration area"
   },
   "previousValue": {
    "type": "string",
    "description": "Previous value"
   },
   "newValue": {
    "type": "integer",
    "description": "New value"
   },
   "reason": {
    "type": "string",
    "description": "Reason"
   },
   "approvalReference": {
    "type": "string",
    "description": "Approval reference"
   },
   "sourceChannel": {
    "type": "string",
    "description": "Source channel"
   },
   "environment": {
    "type": "string",
    "description": "Environment"
   },
   "ipDeviceMetadataWhereApplicable": {
    "type": "string",
    "description": "IP/device metadata where applicable"
   }
  }
 },
 "ProductGovernanceCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Product Governance Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "productsAwaitingApproval": {
    "type": "string",
    "description": "Products awaiting approval"
   },
   "changesAwaitingApproval": {
    "type": "string",
    "description": "Changes awaiting approval"
   },
   "rejectedChanges": {
    "type": "integer",
    "description": "Rejected changes"
   },
   "productsWithGovernanceWarnings": {
    "type": "string",
    "description": "Products with governance warnings"
   },
   "scheduledChanges": {
    "type": "integer",
    "description": "Scheduled changes"
   },
   "productsWithUnpublishedChanges": {
    "type": "string",
    "description": "Products with unpublished changes"
   },
   "productsWithDependencyConflicts": {
    "type": "string",
    "description": "Products with dependency conflicts"
   },
   "productsApproachingRetirement": {
    "type": "string",
    "description": "Products approaching retirement"
   },
   "recentlyPublishedVersions": {
    "type": "integer",
    "description": "Recently published versions"
   },
   "failedPublications": {
    "type": "integer",
    "description": "Failed publications"
   },
   "failedRollbacks": {
    "type": "integer",
    "description": "Failed rollbacks"
   },
   "highRiskConfigurationChanges": {
    "type": "integer",
    "description": "High-risk configuration changes"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "productOwner": {
    "type": "string",
    "description": "Product owner"
   },
   "changeType": {
    "type": "string",
    "description": "Change type"
   },
   "currentVersion": {
    "type": "string",
    "description": "Current version"
   },
   "proposedVersion": {
    "type": "string",
    "description": "Proposed version"
   },
   "requestedBy": {
    "type": "string",
    "description": "Requested by"
   },
   "requestedDate": {
    "type": "string",
    "format": "date-time",
    "description": "Requested date"
   },
   "riskLevel": {
    "type": "string",
    "description": "Risk level"
   },
   "approvalStatus": {
    "type": "string",
    "description": "Approval status"
   },
   "effectiveDate": {
    "type": "string",
    "format": "date-time",
    "description": "Effective date"
   },
   "impactedChannels": {
    "type": "string",
    "description": "Impacted channels"
   },
   "assignedApprover": {
    "type": "string",
    "description": "Assigned approver"
   }
  }
 },
 "ProductRetirementSuspensionArchiveView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Product Retirement, Suspension & Archive displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "temporarilyDisable": {
    "type": "string",
    "description": "Temporarily Disable"
   },
   "endSale": {
    "type": "string",
    "description": "End Sale"
   },
   "retire": {
    "type": "string",
    "description": "Retire"
   },
   "retirementDate": {
    "type": "string",
    "format": "date-time",
    "description": "Retirement date"
   },
   "endOfSaleDate": {
    "type": "string",
    "format": "date-time",
    "description": "End-of-sale date"
   },
   "channels": {
    "type": "string",
    "description": "Channels"
   },
   "reason": {
    "type": "string",
    "description": "Reason"
   },
   "replacementProduct": {
    "type": "string",
    "description": "Replacement product"
   },
   "existingReservationTreatment": {
    "type": "string",
    "description": "Existing reservation treatment"
   },
   "existingTicketTreatment": {
    "type": "string",
    "description": "Existing ticket treatment"
   },
   "communicationRequirements": {
    "type": "string",
    "description": "Communication requirements"
   },
   "reportingTreatment": {
    "type": "string",
    "description": "Reporting treatment"
   },
   "from": {
    "type": "string",
    "description": "from"
   },
   "validityOfPreviouslyIssuedTickets": {
    "type": "string",
    "description": "validity of previously issued tickets"
   },
   "validityOfPreviouslyIssuedEntitlements": {
    "type": "string",
    "description": "validity of previously issued entitlements"
   },
   "activePromotions": {
    "type": "integer",
    "description": "Active promotions"
   },
   "bundles": {
    "type": "string",
    "description": "Bundles"
   },
   "membershipBenefits": {
    "type": "string",
    "description": "Membership benefits"
   },
   "resellerAgreements": {
    "type": "string",
    "description": "Reseller agreements"
   },
   "futureReservations": {
    "type": "string",
    "description": "Future reservations"
   },
   "activePriceLists": {
    "type": "integer",
    "description": "Active price lists"
   },
   "channelAssignments": {
    "type": "string",
    "description": "Channel assignments"
   }
  }
 },
 "ProductVersion": {
  "type": "object",
  "x-ticvai-persistence": "catalogue.product_version",
  "description": "1.1.47, 1.4.9 to 1.4.11. **Follows `white-label.ConfigVersion`** — the same pattern for the same reason, and the fourth place this mechanism was asked for.\n",
  "required": [
   "version",
   "publishedAt",
   "publishedByPrincipalId"
  ],
  "properties": {
   "version": {
    "type": "integer"
   },
   "productId": {
    "type": "string",
    "format": "uuid"
   },
   "publishedAt": {
    "type": "string",
    "format": "date-time"
   },
   "publishedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "note": {
    "type": "string",
    "nullable": true
   },
   "isCurrent": {
    "type": "boolean"
   },
   "contentHash": {
    "type": "string",
    "description": "**Lets a diff be cheap and a no-op change be recognised.** Republishing an unchanged product should not create a version.\n"
   },
   "restoredFromVersion": {
    "type": "integer",
    "nullable": true,
    "description": "Set where this version was created by a restore. **A restore is a new version, not a rewind** — a price that was wrong for three days stays visible, because a finance query run next quarter has to reproduce what was charged.\n"
   }
  }
 },
 "RollbackRecoveryManagementView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Rollback & Recovery Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "identifyDependencies": {
    "type": "string",
    "description": "Identify dependencies"
   },
   "enterRollbackReason": {
    "type": "string",
    "description": "Enter rollback reason"
   },
   "executeImmediateRollbackWhereAuthorized": {
    "type": "string",
    "description": "Execute immediate rollback where authorized"
   },
   "monitorRollbackStatus": {
    "type": "string",
    "description": "Monitor rollback status"
   },
   "entireProduct": {
    "type": "string",
    "description": "Entire product"
   },
   "pricingAssociation": {
    "type": "string",
    "description": "Pricing association"
   },
   "channelAssociation": {
    "type": "string",
    "description": "Channel association"
   },
   "validityConfiguration": {
    "type": "string",
    "description": "Validity configuration"
   },
   "media": {
    "type": "string",
    "description": "Media"
   },
   "policy": {
    "type": "string",
    "description": "Policy"
   },
   "entitlementConfiguration": {
    "type": "string",
    "description": "Entitlement configuration"
   },
   "subjectToSystemGovernance": {
    "type": "string",
    "description": "subject to system governance"
   },
   "enhancedAuditLogging": {
    "type": "string",
    "description": "enhanced audit logging"
   }
  }
 }
}
```
