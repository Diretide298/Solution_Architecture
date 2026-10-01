# WS44 — Product Lifecycle   Catalogue Governance board 2

**10 screens · 12 operations · 19 schemas · 3 permissions**

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

- **Every control that can be refused must be gated.** 3 permissions apply here:
  `AI_APPROVE, PRODUCT_CONFIGURE, PRODUCT_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-128` | Product Governance Command Center | listDetail | 2 | 1 | — |
| `ADM-129` | Approval Workflow Designer | configEditor | 1 | 0 | — |
| `ADM-130` | Approval Review & Decision Workspace | listDetail | 1 | 0 | — |
| `ADM-131` | Product Version Management | listDetail | 1 | 0 | — |
| `ADM-132` | Rollback & Recovery Management | listDetail | 1 | 0 | — |
| `ADM-133` | Change Impact Analysis | listDetail | 2 | 0 | — |
| `ADM-134` | Change Propagation & Dependency Control | listDetail | 2 | 0 | — |
| `ADM-135` | Product Retirement, Suspension & Archive | configEditor | 1 | 3 | — |
| `ADM-136` | Product Audit Trail & Change History | configEditor | 1 | 0 | — |
| `ADM-137` | Governance Risk, AI Monitoring & Control Center | listDetail | 2 | 1 | — |

## Thin screens in this batch

**ADM-130, ADM-132, ADM-133, ADM-134, ADM-137 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

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
     "provenance": "derived — ADM-002 declares entryState.params  and ADM-128 holds none of them. The edge carries nothing: ADM-128 is opened from ADM-002, so this edge is the way back and ADM-002 keeps its own state"
    },
    {
     "to": "ADM-131",
     "trigger": "Product Version Management",
     "carries": [
      "productId"
     ],
     "provenance": "derived — ADM-131 declares entryState.params productId and ADM-128 holds productId, so an edge into it carries them"
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
     "to": "ADM-133",
     "trigger": "Works in Change Impact Analysis",
     "provenance": "flow F153 step 9→10",
     "operation": "listProductGovernance",
     "carries": [
      "productId"
     ]
    },
    {
     "to": "ADM-134",
     "trigger": "Works in Change Propagation & Dependency Control",
     "provenance": "flow F153 step 11→12",
     "operation": "listProductGovernance",
     "carries": [
      "productId"
     ]
    },
    {
     "to": "ADM-137",
     "trigger": "Works in Governance Risk, AI Monitoring & Control Center",
     "provenance": "flow F153 step 17→18",
     "operation": "listProductGovernance",
     "carries": [
      "findingId"
     ]
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Authorized users can identify every product requiring governance attention and prioritize actions from a single dashboard.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§The dashboard shall display; Each record should display) and no metric row",
  "purpose": "Provide management and administrators with a single control center for all product governance activities.",
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
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Products awaiting approval",
       "bindsTo": "ProductGovernanceCommandCenterSummary.productsAwaitingApproval",
       "operation": "listProductGovernance",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Changes awaiting approval",
       "bindsTo": "ProductGovernanceCommandCenterSummary.changesAwaitingApproval",
       "operation": "listProductGovernance",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Rejected changes",
       "bindsTo": "ProductGovernanceCommandCenterSummary.rejectedChanges",
       "operation": "listProductGovernance",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Products with governance warnings",
       "bindsTo": "ProductGovernanceCommandCenterSummary.productsWithGovernanceWarnings",
       "operation": "listProductGovernance",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Scheduled changes",
       "bindsTo": "ProductGovernanceCommandCenterSummary.scheduledChanges",
       "operation": "listProductGovernance",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Products with unpublished changes",
       "bindsTo": "ProductGovernanceCommandCenterSummary.productsWithUnpublishedChanges",
       "operation": "listProductGovernance",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Products with dependency conflicts",
       "bindsTo": "ProductGovernanceCommandCenterSummary.productsWithDependencyConflicts",
       "operation": "listProductGovernance",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Products approaching retirement",
       "bindsTo": "ProductGovernanceCommandCenterSummary.productsApproachingRetirement",
       "operation": "listProductGovernance",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Recently published versions",
       "bindsTo": "ProductGovernanceCommandCenterSummary.recentlyPublishedVersions",
       "operation": "listProductGovernance",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "High risk configuration changes",
       "bindsTo": "ProductGovernanceCommandCenterSummary.highRiskConfigurationChanges",
       "operation": "listProductGovernance",
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
       "label": "Every product governance",
       "columns": [
        "Failed publications/rollbacks",
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
        "Failed publications/rollbacks",
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
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Decide catalogue AI finding",
       "operation": "decideCatalogueAiFinding",
       "permission": "AI_APPROVE",
       "notes": "**The human control on a governance risk or a channel recommendation** (29 September, writers pass).",
       "provenance": "contract catalogue.yaml POST /ai-findings/{findingId}/decision"
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
   },
   {
    "operationId": "decideCatalogueAiFinding",
    "contract": "catalogue",
    "purpose": "Acknowledge, accept, dismiss or resolve an AI finding",
    "trigger": "onAction",
    "invalidates": [
     "listProductGovernance"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "ProductGovernanceCommandCenterSummary.productsAwaitingApproval",
    "ProductGovernanceCommandCenterSummary.changesAwaitingApproval",
    "ProductGovernanceCommandCenterSummary.rejectedChanges",
    "ProductGovernanceCommandCenterSummary.productsWithGovernanceWarnings",
    "ProductGovernanceCommandCenterSummary.scheduledChanges",
    "ProductGovernanceCommandCenterSummary.productsWithUnpublishedChanges"
   ],
   "params": [
    {
     "name": "findingId",
     "from": "navigation",
     "optional": true
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-128",
   "workshopBoard": "wireframes/WS105 Product Lifecycle   Catalogue Governance Board 2.dc.html#adm-128"
  },
  "apisNote": "Regenerated 9 September 2026 from Product_Lifecycle___Catalogue_Governance_Reference.pdf page 15. 26 of 34 labels bound to a contract property; 34 of 41 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formDecideCatalogueAiFinding",
    "component": "modal",
    "trigger": "Decide catalogue AI finding",
    "body": "**Collects what `decideCatalogueAiFinding` sends before it is called.** Required: `decision`. Optional: `comment`, `ownerPrincipalId`, `dueDate`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Decide catalogue AI finding",
     "operation": "decideCatalogueAiFinding"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "decision",
      "comment",
      "ownerPrincipalId",
      "dueDate"
     ]
    },
    "provenance": "contract catalogue.yaml POST /ai-findings/{findingId}/decision"
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
  "purposeNote": "Administrators can configure product approval workflows without development work and route different types of changes through different approval paths.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Each workflow can define; Tax configuration) and no display directory — it is settings, not a population",
  "purpose": "Configure reusable approval workflows governing product creation and modification.",
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
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-129",
   "workshopBoard": "wireframes/WS105 Product Lifecycle   Catalogue Governance Board 2.dc.html#adm-129"
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
  "purposeNote": "An approver can understand exactly what is changing, why it is changing and what it may affect before approving or rejecting the request.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Give approvers a clear interface for reviewing a proposed product or product change before making a decision.",
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
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-130",
   "workshopBoard": "wireframes/WS105 Product Lifecycle   Catalogue Governance Board 2.dc.html#adm-130"
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
  "purposeNote": "Every governed product modification creates a traceable version, and authorized users can compare any two versions.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Maintain controlled versions of every governed product configuration. The source matrix specifically requires version history for products and the ability to roll back to earlier versions.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 6 actions on this screen and the screen declares 1 operation.** Unserved: Basic product information, Pricing, Capacity, Entitlements, Channels. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
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
       "label": "Version 4.2 ↔ Version 4.1",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 19 §Users can compare"
      },
      {
       "kind": "secondaryButton",
       "label": "Basic product information",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 19 §Users can compare"
      },
      {
       "kind": "secondaryButton",
       "label": "Pricing",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 19 §Users can compare"
      },
      {
       "kind": "secondaryButton",
       "label": "Capacity",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 19 §Users can compare"
      },
      {
       "kind": "secondaryButton",
       "label": "Entitlements",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 19 §Users can compare"
      },
      {
       "kind": "secondaryButton",
       "label": "Channels",
       "provenance": "pack Product_Lifecycle___Catalogue_Governance_Reference.pdf, page 19 §Users can compare"
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
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "productId",
     "from": "navigation"
    }
   ],
   "coldEntry": "**Reached from the list that owns it**, so the identifier arrives with the navigation. Opened cold without one, the screen says what is missing and offers that list — never an empty form that looks configurable."
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-131",
   "workshopBoard": "wireframes/WS105 Product Lifecycle   Catalogue Governance Board 2.dc.html#adm-131"
  },
  "apisNote": "Regenerated 9 September 2026 from Product_Lifecycle___Catalogue_Governance_Reference.pdf page 19. 0 of 0 labels bound to a contract property; 6 of 37 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "purposeNote": "An authorized user can restore a safe earlier configuration without corrupting historical sales, reservations or issued entitlements.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Safely restore an earlier product configuration when a newly published configuration causes an issue.",
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
    "RollbackRecoveryManagementView.dependencies",
    "RollbackRecoveryManagementView.reason",
    "RollbackRecoveryManagementView.executionMode",
    "RollbackRecoveryManagementView.status",
    "RollbackRecoveryManagementView.scope"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-132",
   "workshopBoard": "wireframes/WS105 Product Lifecycle   Catalogue Governance Board 2.dc.html#adm-132"
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
  "purposeNote": "Before a material configuration change is approved or published, authorized users can see its potential cross-module and transactional impact.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Show administrators what will be affected before a product change is approved or published. This directly addresses the matrix requirement to perform impact analysis before product changes are published.",
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
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save product links",
       "operation": "setProductLinks",
       "permission": "PRODUCT_CONFIGURE",
       "notes": "**Set whole, per source product** (29 September, writers pass).",
       "provenance": "contract catalogue.yaml PUT /products/{productId}/links"
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
   },
   {
    "operationId": "setProductLinks",
    "contract": "catalogue",
    "purpose": "Replace what depends on a product",
    "trigger": "onAction",
    "invalidates": [
     "listChangeImpactAnalysis"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "ChangeImpactAnalysisView.area"
   ],
   "params": [
    {
     "name": "productId",
     "from": "navigation",
     "optional": true
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-133",
   "workshopBoard": "wireframes/WS105 Product Lifecycle   Catalogue Governance Board 2.dc.html#adm-133"
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
  "purposeNote": "Product changes can propagate through defined relationships without unintentionally overwriting approved local exceptions.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Control whether approved product changes should automatically propagate to related products or dependent configurations. The source matrix requires controlled propagation of changes to linked products.",
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
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Save product links",
       "operation": "setProductLinks",
       "permission": "PRODUCT_CONFIGURE",
       "notes": "**Set whole, per source product** (29 September, writers pass).",
       "provenance": "contract catalogue.yaml PUT /products/{productId}/links"
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
   },
   {
    "operationId": "setProductLinks",
    "contract": "catalogue",
    "purpose": "Replace what depends on a product",
    "trigger": "onAction",
    "invalidates": [
     "listChangePropagationDependency"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "ChangePropagationDependencyControlView.dependencyType"
   ],
   "params": [
    {
     "name": "productId",
     "from": "navigation",
     "optional": true
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-134",
   "workshopBoard": "wireframes/WS105 Product Lifecycle   Catalogue Governance Board 2.dc.html#adm-134"
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
  "purposeNote": "A product can be safely removed from future sale while protecting existing valid customer transactions and identifying unresolved dependencies.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Administrator defines) and no display directory — it is settings, not a population",
  "purpose": "Provide a governed end-of-life process for products. The source matrix explicitly requires disabling or retiring products without affecting previously sold tickets.",
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-135",
   "workshopBoard": "wireframes/WS105 Product Lifecycle   Catalogue Governance Board 2.dc.html#adm-135"
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
  "purposeNote": "Every material product configuration and governance action is traceable to who performed it, when it occurred, what changed and under which approval.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Each entry should capture) and no display directory — it is settings, not a population",
  "purpose": "Provide a complete, immutable history of product configuration and governance activity. The matrix requires tracking configuration changes with timestamps and user information.",
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-136",
   "workshopBoard": "wireframes/WS105 Product Lifecycle   Catalogue Governance Board 2.dc.html#adm-136"
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
   "notes": "**Reached from ADM-128, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-128",
     "trigger": "Product Governance Command Center",
     "carries": [
      "findingId"
     ],
     "provenance": "derived — ADM-128 declares entryState.params findingId and ADM-137 holds findingId, so an edge into it carries them"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Administrators receive proactive governance intelligence with clear explanations and recommended actions while material product decisions remain controlled by the configured authorization framework. Board 2 — Final Screen Register",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Use TICVAI intelligence to continuously identify catalogue governance risks rather than relying entirely on administrators to discover them manually.",
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
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Decide catalogue AI finding",
       "operation": "decideCatalogueAiFinding",
       "permission": "AI_APPROVE",
       "notes": "**The human control on a governance risk or a channel recommendation** (29 September, writers pass).",
       "provenance": "contract catalogue.yaml POST /ai-findings/{findingId}/decision"
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
   },
   {
    "operationId": "decideCatalogueAiFinding",
    "contract": "catalogue",
    "purpose": "Acknowledge, accept, dismiss or resolve an AI finding",
    "trigger": "onAction",
    "invalidates": [
     "listGovernanceRiskMonitoring"
    ]
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
   ],
   "params": [
    {
     "name": "findingId",
     "from": "navigation",
     "optional": true
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-137",
   "workshopBoard": "wireframes/WS105 Product Lifecycle   Catalogue Governance Board 2.dc.html#adm-137"
  },
  "apisNote": "Regenerated 9 September 2026 from Product_Lifecycle___Catalogue_Governance_Reference.pdf page 26. 8 of 9 labels bound to a contract property; 9 of 55 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formDecideCatalogueAiFinding",
    "component": "modal",
    "trigger": "Decide catalogue AI finding",
    "body": "**Collects what `decideCatalogueAiFinding` sends before it is called.** Required: `decision`. Optional: `comment`, `ownerPrincipalId`, `dueDate`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Decide catalogue AI finding",
     "operation": "decideCatalogueAiFinding"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "decision",
      "comment",
      "ownerPrincipalId",
      "dueDate"
     ]
    },
    "provenance": "contract catalogue.yaml POST /ai-findings/{findingId}/decision"
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
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
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "ApprovalWorkflowDesignerInput",
  "responds": "ApprovalWorkflowDesignerView"
 },
 "decideCatalogueAiFinding": {
  "method": "POST",
  "path": "/ai-findings/{findingId}/decision",
  "contract": "catalogue",
  "summary": "Acknowledge, accept, dismiss or resolve an AI finding",
  "permission": "AI_APPROVE",
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
  "responds": "CatalogueAiFinding"
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
 "listChangePropagationDependency": {
  "method": "GET",
  "path": "/change-propagation-dependency",
  "contract": "catalogue",
  "summary": "Change Propagation & Dependency Control",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "productId",
    "in": "query",
    "required": false
   },
   {
    "name": "changeRequestId",
    "in": "query",
    "required": false
   },
   {
    "name": "dependencyType",
    "in": "query",
    "required": false
   },
   {
    "name": "conflictsOnly",
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
 "listGovernanceRiskMonitoring": {
  "method": "GET",
  "path": "/governance-risk-monitoring",
  "contract": "catalogue",
  "summary": "Governance Risk, AI Monitoring & Control Center",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "severity",
    "in": "query",
    "required": false
   },
   {
    "name": "risk",
    "in": "query",
    "required": false
   },
   {
    "name": "venueId",
    "in": "query",
    "required": false
   },
   {
    "name": "owner",
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
    "name": "venueId",
    "in": "query",
    "required": false
   },
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
    "name": "channel",
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
 "listProductRetirementSuspension": {
  "method": "GET",
  "path": "/product-retirement-suspension",
  "contract": "catalogue",
  "summary": "Product Retirement, Suspension & Archive",
  "permission": "PRODUCT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "action",
    "in": "query",
    "required": false
   },
   {
    "name": "lifecycleState",
    "in": "query",
    "required": false
   },
   {
    "name": "venueId",
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
    "name": "productId",
    "in": "query",
    "required": false
   },
   {
    "name": "userId",
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
    "name": "action",
    "in": "query",
    "required": false
   },
   {
    "name": "version",
    "in": "query",
    "required": false
   },
   {
    "name": "configurationArea",
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
   },
   {
    "name": "environment",
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
  "parameters": [
   {
    "name": "productId",
    "in": "query",
    "required": false
   },
   {
    "name": "status",
    "in": "query",
    "required": false
   },
   {
    "name": "scope",
    "in": "query",
    "required": false
   },
   {
    "name": "emergency",
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
 "setProductLinks": {
  "method": "PUT",
  "path": "/products/{productId}/links",
  "contract": "catalogue",
  "summary": "Replace what depends on a product",
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
  "requestBody": "ProductLink",
  "responds": "ProductLink"
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
   "decision": {
    "type": "string",
    "enum": [
     "approve",
     "reject",
     "requestChanges",
     "reassign",
     "delegate",
     "escalate"
    ],
    "description": "Approver action (pack p.18)"
   },
   "assignToPrincipalId": {
    "type": "string",
    "description": "New approver for reassign/delegate/escalate",
    "nullable": true
   },
   "changeRequestId": {
    "type": "string",
    "description": "Change request id",
    "format": "uuid"
   },
   "comment": {
    "type": "string",
    "description": "Comment; required for reject and requestChanges",
    "nullable": true
   }
  }
 },
 "ApprovalReviewDecisionWorkspaceView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Approval Review & Decision Workspace displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "approvalStatus": {
    "type": "string",
    "description": "Approval status after this decision: pending, changesRequested, approved, rejected, escalated or withdrawn"
   },
   "requester": {
    "type": "string",
    "description": "Requester (display name)"
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
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "fileId": {
       "type": "string"
      },
      "name": {
       "type": "string"
      }
     }
    },
    "description": "Attachments"
   },
   "effectiveDate": {
    "type": "string",
    "description": "Effective date; empty = on approval",
    "format": "date",
    "nullable": true
   },
   "currentSales": {
    "type": "integer",
    "description": "Tickets sold under the current version"
   },
   "futureReservations": {
    "type": "integer",
    "description": "Future reservations of the product"
   },
   "channelsAffected": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/Channel"
    },
    "description": "Channels affected"
   },
   "pricingImpact": {
    "type": "string",
    "description": "Pricing impact in plain language; the figures are in comparison"
   },
   "capacityImpact": {
    "type": "integer",
    "description": "Change in capacity units (negative = reduction)"
   },
   "financeImpact": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "Estimated revenue difference over future reservations and forecast sales; advisory"
   },
   "accessImpact": {
    "type": "string",
    "description": "Access impact in plain language"
   },
   "changeRequestId": {
    "type": "string",
    "description": "Change request id",
    "format": "uuid"
   },
   "productId": {
    "type": "string",
    "description": "Product id",
    "format": "uuid"
   },
   "comparison": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "configurationArea": {
       "type": "string",
       "enum": [
        "basicInformation",
        "validity",
        "pricing",
        "capacity",
        "entitlements",
        "eligibility",
        "media",
        "channels",
        "policies",
        "relationships",
        "lifecycle"
       ]
      },
      "field": {
       "type": "string"
      },
      "currentValue": {
       "type": "string",
       "nullable": true
      },
      "proposedValue": {
       "type": "string",
       "nullable": true
      },
      "changed": {
       "type": "boolean"
      }
     }
    },
    "description": "Change comparison, current vs proposed; changed rows are highlighted"
   },
   "aiSummary": {
    "type": "string",
    "description": "AI summary of the proposed change; advisory, the AI does not approve",
    "nullable": true
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
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/ProductKind"
    },
    "description": "Applicable product types; empty = all"
   },
   "venue": {
    "type": "string",
    "description": "Venue id; empty = all venues",
    "nullable": true
   },
   "department": {
    "type": "string",
    "description": "Department",
    "nullable": true
   },
   "changeTypes": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "newProduct",
      "description",
      "price",
      "validity",
      "capacity",
      "entitlement",
      "eligibility",
      "tax",
      "channel",
      "media",
      "policy",
      "relationship",
      "retirement"
     ]
    },
    "description": "Change types routed to this workflow (Conditional Approval: e.g. price -> Commercial + Finance)"
   },
   "approvalStages": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "order": {
       "type": "integer",
       "description": "Stage order; stages sharing an order run in parallel, otherwise sequential"
      },
      "name": {
       "type": "string"
      },
      "approverRole": {
       "type": "string",
       "nullable": true
      },
      "specificApproverId": {
       "type": "string",
       "nullable": true
      },
      "approvalGroupId": {
       "type": "string",
       "nullable": true
      },
      "mandatory": {
       "type": "boolean"
      },
      "slaHours": {
       "type": "integer",
       "description": "SLA in hours"
      },
      "escalateToRole": {
       "type": "string",
       "nullable": true,
       "description": "Escalation when the SLA is missed"
      },
      "delegationAllowed": {
       "type": "boolean"
      },
      "reminderEveryHours": {
       "type": "integer",
       "nullable": true,
       "description": "Reminder frequency"
      }
     }
    },
    "description": "Approval stages, e.g. Product Manager -> Commercial Manager -> Operations -> Finance -> Final Approval; each stage names a role, a specific approver or a group"
   },
   "rejectionBehavior": {
    "type": "string",
    "enum": [
     "returnToDraft",
     "returnToPreviousStage",
     "closeRequest"
    ],
    "description": "What happens on rejection; default returnToDraft (decided 29 September, readiness close-out)"
   },
   "resubmissionBehavior": {
    "type": "string",
    "enum": [
     "restartFromFirstStage",
     "resumeAtRejectingStage"
    ],
    "description": "Where a resubmitted request re-enters; default restartFromFirstStage (decided 29 September, readiness close-out)"
   },
   "workflowId": {
    "type": "string",
    "description": "Existing workflow to change; empty to create",
    "format": "uuid",
    "nullable": true
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
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/ProductKind"
    },
    "description": "Applicable product types; empty = all"
   },
   "venue": {
    "type": "string",
    "description": "Venue id; empty = all venues",
    "nullable": true
   },
   "department": {
    "type": "string",
    "description": "Department",
    "nullable": true
   },
   "changeTypes": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "newProduct",
      "description",
      "price",
      "validity",
      "capacity",
      "entitlement",
      "eligibility",
      "tax",
      "channel",
      "media",
      "policy",
      "relationship",
      "retirement"
     ]
    },
    "description": "Change types routed to this workflow (Conditional Approval: e.g. price -> Commercial + Finance)"
   },
   "approvalStages": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "order": {
       "type": "integer",
       "description": "Stage order; stages sharing an order run in parallel, otherwise sequential"
      },
      "name": {
       "type": "string"
      },
      "approverRole": {
       "type": "string",
       "nullable": true
      },
      "specificApproverId": {
       "type": "string",
       "nullable": true
      },
      "approvalGroupId": {
       "type": "string",
       "nullable": true
      },
      "mandatory": {
       "type": "boolean"
      },
      "slaHours": {
       "type": "integer",
       "description": "SLA in hours"
      },
      "escalateToRole": {
       "type": "string",
       "nullable": true,
       "description": "Escalation when the SLA is missed"
      },
      "delegationAllowed": {
       "type": "boolean"
      },
      "reminderEveryHours": {
       "type": "integer",
       "nullable": true,
       "description": "Reminder frequency"
      }
     }
    },
    "description": "Approval stages, e.g. Product Manager -> Commercial Manager -> Operations -> Finance -> Final Approval; each stage names a role, a specific approver or a group"
   },
   "rejectionBehavior": {
    "type": "string",
    "enum": [
     "returnToDraft",
     "returnToPreviousStage",
     "closeRequest"
    ],
    "description": "What happens on rejection; default returnToDraft (decided 29 September, readiness close-out)"
   },
   "resubmissionBehavior": {
    "type": "string",
    "enum": [
     "restartFromFirstStage",
     "resumeAtRejectingStage"
    ],
    "description": "Where a resubmitted request re-enters; default restartFromFirstStage (decided 29 September, readiness close-out)"
   },
   "workflowId": {
    "type": "string",
    "description": "Workflow id",
    "format": "uuid"
   }
  }
 },
 "CatalogueAiFinding": {
  "type": "object",
  "x-ticvai-persistence": "catalogue.ai_finding",
  "description": "**Something the AI noticed about the catalogue or its channels, for a person to act on** (29 September, data model DM3). Merges governance risks (ADM-137) and channel optimisation recommendations (ADM-272). Advisory only: a finding never changes configuration; acting on it goes through the ordinary operations and their approvals. **Created by the AI monitoring job** (29 September, writers pass); a person acknowledges, accepts, dismisses or resolves it with `decideCatalogueAiFinding`, and the job resolves one whose condition has cleared (`states/catalogue-ai-finding.yaml`).",
  "required": [
   "id",
   "scopePath",
   "domain",
   "findingType",
   "status",
   "detectedAt"
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
   "domain": {
    "type": "string",
    "enum": [
     "productGovernance",
     "channel"
    ]
   },
   "findingType": {
    "type": "string",
    "maxLength": 60,
    "description": "Governance: the `risk` value; channel: the recommendation `category`."
   },
   "productId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "salesChannelIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "severity": {
    "type": "string",
    "enum": [
     "critical",
     "high",
     "medium",
     "low",
     null
    ],
    "nullable": true
   },
   "confidence": {
    "type": "number",
    "nullable": true,
    "minimum": 0,
    "maximum": 1
   },
   "summary": {
    "type": "string",
    "description": "The recommendation, or the risk in one line."
   },
   "explanation": {
    "type": "string",
    "nullable": true
   },
   "businessImpact": {
    "type": "string",
    "nullable": true
   },
   "recommendedAction": {
    "type": "string",
    "nullable": true
   },
   "constraints": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "signals": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "simulation": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true,
    "description": "Channel findings: `{expectedUnitsSold, revenueImpact, channelUtilization, risk, contractualConstraints}`."
   },
   "requiredApproval": {
    "type": "string",
    "maxLength": 100,
    "nullable": true
   },
   "ownerPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "dueDate": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "status": {
    "type": "string",
    "enum": [
     "open",
     "acknowledged",
     "accepted",
     "dismissed",
     "resolved"
    ],
    "default": "open"
   },
   "modelVersion": {
    "type": "string",
    "maxLength": 60,
    "nullable": true
   },
   "detectedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "resolvedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
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
 "ChangePropagationDependencyControlView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Change Propagation & Dependency Control displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "dependencyType": {
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
    "description": "Dependency type (pack pp.22-23)"
   },
   "propagate": {
    "type": "boolean",
    "description": "Whether the change will propagate to this linked object"
   },
   "localOverrideConflict": {
    "type": "boolean",
    "description": "The linked object has a local override the change would overwrite"
   },
   "linkId": {
    "type": "string",
    "description": "Link id",
    "format": "uuid"
   },
   "sourceProductId": {
    "type": "string",
    "description": "Master product",
    "format": "uuid"
   },
   "linkedObjectId": {
    "type": "string",
    "description": "Linked product or configuration id"
   },
   "linkedObjectName": {
    "type": "string",
    "description": "Linked object name"
   },
   "overriddenFields": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Fields the linked object overrides locally"
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
 "GovernanceRiskAiMonitoringControlCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Governance Risk, AI Monitoring & Control Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "risk": {
    "type": "string",
    "enum": [
     "productWithoutOwner",
     "missingApproval",
     "outdatedPricing",
     "conflictingValidity",
     "missingChannelConfiguration",
     "orphanedDependency",
     "unusedProduct",
     "duplicateProduct",
     "unusualConfigurationChange",
     "highOverrideLevel",
     "scheduledPublicationConflict",
     "expiredCommercialConfiguration",
     "activeAfterEventEnd",
     "brokenDependency"
    ],
    "description": "Risk detected (AI Monitoring, pack p.26)"
   },
   "product": {
    "type": "string",
    "description": "Product name"
   },
   "venue": {
    "type": "string",
    "description": "Venue name"
   },
   "businessImpact": {
    "type": "string",
    "description": "Business impact, in plain language"
   },
   "recommendedAction": {
    "type": "string",
    "description": "Recommended action; advisory"
   },
   "owner": {
    "type": "string",
    "description": "Owner (display name)",
    "nullable": true
   },
   "dueDate": {
    "type": "string",
    "description": "Due date",
    "format": "date",
    "nullable": true
   },
   "status": {
    "type": "string",
    "description": "Status: open, acknowledged, inRemediation, resolved or dismissed (decided 29 September, readiness close-out)"
   },
   "riskId": {
    "type": "string",
    "description": "Risk id",
    "format": "uuid"
   },
   "productId": {
    "type": "string",
    "description": "Product id",
    "format": "uuid",
    "nullable": true
   },
   "severity": {
    "type": "string",
    "enum": [
     "critical",
     "high",
     "medium",
     "low"
    ],
    "description": "Severity (Risk Dashboard)"
   },
   "explanation": {
    "type": "string",
    "description": "AI explanation, e.g. the two products share 96% of their configuration; advisory"
   },
   "detectedAt": {
    "type": "string",
    "description": "Detected",
    "format": "date-time"
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
 "ProductAuditTrailChangeHistoryView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Product Audit Trail & Change History displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "dateTime": {
    "type": "string",
    "description": "Date/time",
    "format": "date-time"
   },
   "user": {
    "type": "string",
    "description": "User (display name)"
   },
   "role": {
    "type": "string",
    "description": "Role at the time"
   },
   "product": {
    "type": "string",
    "description": "Product name"
   },
   "version": {
    "type": "integer",
    "nullable": true,
    "description": "Product version"
   },
   "action": {
    "type": "string",
    "enum": [
     "created",
     "updated",
     "submitted",
     "approved",
     "rejected",
     "changesRequested",
     "scheduled",
     "published",
     "rolledBack",
     "suspended",
     "retired",
     "archived",
     "imported",
     "exported",
     "duplicated"
    ],
    "description": "Action (decided 29 September, readiness close-out)"
   },
   "configurationArea": {
    "type": "string",
    "enum": [
     "basicInformation",
     "validity",
     "pricing",
     "capacity",
     "entitlements",
     "eligibility",
     "media",
     "channels",
     "policies",
     "relationships",
     "lifecycle"
    ],
    "description": "Configuration area"
   },
   "previousValue": {
    "type": "string",
    "description": "Previous value",
    "nullable": true
   },
   "newValue": {
    "type": "string",
    "description": "New value",
    "nullable": true
   },
   "reason": {
    "type": "string",
    "description": "Reason",
    "nullable": true
   },
   "approvalReference": {
    "type": "string",
    "description": "Approval reference (change request id)",
    "nullable": true
   },
   "sourceChannel": {
    "type": "string",
    "enum": [
     "backOffice",
     "api",
     "bulkImport",
     "environmentTransfer",
     "scheduler",
     "aiAssistant"
    ],
    "description": "Where the change was made (decided 29 September, readiness close-out)"
   },
   "environment": {
    "type": "string",
    "enum": [
     "development",
     "sandbox",
     "uat",
     "staging",
     "production"
    ],
    "description": "Environment"
   },
   "deviceMetadata": {
    "type": "object",
    "nullable": true,
    "properties": {
     "ipAddress": {
      "type": "string"
     },
     "userAgent": {
      "type": "string"
     },
     "deviceId": {
      "type": "string",
      "nullable": true
     }
    },
    "description": "IP/device metadata where applicable"
   },
   "auditId": {
    "type": "string",
    "description": "Audit entry id",
    "format": "uuid"
   },
   "productId": {
    "type": "string",
    "description": "Product id",
    "format": "uuid"
   },
   "userId": {
    "type": "string",
    "description": "User principal id",
    "format": "uuid"
   }
  }
 },
 "ProductGovernanceCommandCenterSummary": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection; the headline tiles over the list, computed at read time for the filters in force",
  "description": "**The headline figures on Product Governance Command Center.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.",
  "properties": {
   "productsAwaitingApproval": {
    "type": "integer",
    "description": "Products awaiting approval"
   },
   "changesAwaitingApproval": {
    "type": "integer",
    "description": "Changes awaiting approval"
   },
   "rejectedChanges": {
    "type": "integer",
    "description": "Rejected changes (last 30 days) (decided 29 September, readiness close-out)"
   },
   "productsWithGovernanceWarnings": {
    "type": "integer",
    "description": "Products with governance warnings"
   },
   "scheduledChanges": {
    "type": "integer",
    "description": "Scheduled changes"
   },
   "productsWithUnpublishedChanges": {
    "type": "integer",
    "description": "Products with unpublished changes"
   },
   "productsWithDependencyConflicts": {
    "type": "integer",
    "description": "Products with dependency conflicts"
   },
   "productsApproachingRetirement": {
    "type": "integer",
    "description": "Products approaching retirement: retirement date within 30 days (decided 29 September, readiness close-out)"
   },
   "recentlyPublishedVersions": {
    "type": "integer",
    "description": "Recently published versions: published in the last 7 days (decided 29 September, readiness close-out)"
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
    "description": "High-risk configuration changes (riskLevel high or critical) awaiting decision"
   }
  }
 },
 "ProductGovernanceCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Product Governance Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "product": {
    "type": "string",
    "description": "Product name"
   },
   "venue": {
    "type": "string",
    "description": "Venue name"
   },
   "productOwner": {
    "type": "string",
    "description": "Product owner (display name)"
   },
   "changeType": {
    "type": "string",
    "enum": [
     "newProduct",
     "description",
     "price",
     "validity",
     "capacity",
     "entitlement",
     "eligibility",
     "tax",
     "channel",
     "media",
     "policy",
     "relationship",
     "retirement"
    ],
    "description": "Change type (decided 29 September, readiness close-out)"
   },
   "currentVersion": {
    "type": "integer",
    "nullable": true,
    "description": "Current version number (ProductVersion.version); empty for a new product"
   },
   "proposedVersion": {
    "type": "integer",
    "description": "Proposed version number"
   },
   "requestedBy": {
    "type": "string",
    "description": "Requested by (display name)"
   },
   "requestedDate": {
    "type": "string",
    "description": "Requested date-time",
    "format": "date-time"
   },
   "riskLevel": {
    "type": "string",
    "enum": [
     "low",
     "medium",
     "high",
     "critical"
    ],
    "description": "Risk level"
   },
   "approvalStatus": {
    "type": "string",
    "description": "Approval status: pending, changesRequested, approved, rejected, escalated or withdrawn"
   },
   "effectiveDate": {
    "type": "string",
    "description": "Effective date of the change; empty = on approval",
    "format": "date",
    "nullable": true
   },
   "impactedChannels": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/Channel"
    },
    "description": "Impacted channels"
   },
   "assignedApprover": {
    "type": "string",
    "description": "Assigned approver (display name)",
    "nullable": true
   },
   "changeRequestId": {
    "type": "string",
    "description": "Change request id",
    "format": "uuid"
   },
   "productId": {
    "type": "string",
    "description": "Product id",
    "format": "uuid"
   },
   "lifecycleState": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ProductLifecycleState"
     }
    ],
    "description": "Product's current lifecycle state"
   },
   "aiInsights": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "AI insights: advisory only; the AI never approves, publishes, retires or changes a product (pack p.26-27)"
   }
  }
 },
 "ProductKind": {
  "type": "string",
  "description": "**`openDated` added 24 August** from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no kind: **valid on any date within an eligible range, rather than for a named performance or a fixed date.**\nThe mechanism already existed — `access.entitlement` carries `valid_from`, `valid_to`, `entries_allowed` and `frozen_days`, which is exactly an open-dated pass. **What was missing was the product saying it is one**, so a catalogue could not offer it and a report could not count it.\n**`datedAdmission` is a different thing and the two were being conflated**: dated is *this Tuesday*, open-dated is *any Tuesday between March and June*. A guest buying the second and being sold the first has bought the wrong ticket.\n**Transport uses two existing kinds, not a new one** (decided 29 September, rev 3 REV3-21). A one-way trip is `timedAdmission`: `transport.createTransportRoute` creates the route's product with one variant per passenger type, and each departure is a performance. A multi-trip or unlimited pass is `openDated`: `transport.createTransportPassType` creates it, with `EntitlementTemplate.entriesAllowed` = the pass's trips (null for unlimited), the validity = `validityDays`, and `EntitlementTemplate.transportRestriction` naming the station pair the pass was bought for, so `access` refuses it on another journey. The sale path is unchanged: both are cart lines, priced by `transport.quoteTransportFare` (orders `TransportLineAttributes`).\n",
  "enum": [
   "admission",
   "timedAdmission",
   "datedAdmission",
   "openDated",
   "seated",
   "membership",
   "bundle",
   "fnb",
   "retail",
   "rental",
   "addOn",
   "giftCard"
  ]
 },
 "ProductLifecycleState": {
  "type": "string",
  "enum": [
   "draft",
   "inReview",
   "approved",
   "live",
   "withdrawn",
   "archived"
  ]
 },
 "ProductLink": {
  "type": "object",
  "x-ticvai-persistence": "catalogue.product_link",
  "description": "**What depends on a product, so a change can be propagated or held** (29 September, data model DM3). ADM-134. `propagatesChanges` says whether an approved change to the source flows to the linked object; `overriddenFields` are the local overrides a propagation must not overwrite (a conflict is reported, not resolved silently).",
  "required": [
   "id",
   "scopePath",
   "sourceProductId",
   "dependencyType",
   "linkedObjectId"
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
   "sourceProductId": {
    "type": "string",
    "format": "uuid"
   },
   "dependencyType": {
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
    ]
   },
   "linkedObjectId": {
    "type": "string",
    "format": "uuid"
   },
   "linkedObjectName": {
    "type": "string",
    "maxLength": 200,
    "nullable": true
   },
   "propagatesChanges": {
    "type": "boolean",
    "default": true
   },
   "overriddenFields": {
    "type": "array",
    "items": {
     "type": "string"
    }
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
 "ProductRetirementSuspensionArchiveView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over catalogue state, assembled at read time from tables that already exist",
  "description": "**What Product Retirement, Suspension & Archive displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "action": {
    "type": "string",
    "enum": [
     "suspendSales",
     "temporarilyDisable",
     "endSale",
     "retire",
     "archive"
    ],
    "description": "End-of-life action (Available Actions, pack pp.23-24)"
   },
   "retirementDate": {
    "type": "string",
    "description": "Retirement date",
    "format": "date",
    "nullable": true
   },
   "endOfSaleDate": {
    "type": "string",
    "description": "End-of-sale date",
    "format": "date",
    "nullable": true
   },
   "channels": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/Channel"
    },
    "description": "Channels the action applies to; empty = all"
   },
   "reason": {
    "type": "string",
    "description": "Reason"
   },
   "replacementProductId": {
    "type": "string",
    "description": "Replacement product",
    "format": "uuid",
    "nullable": true
   },
   "existingReservationTreatment": {
    "type": "string",
    "enum": [
     "honour",
     "moveToReplacement",
     "cancel"
    ],
    "description": "Existing reservation treatment; default honour (decided 29 September, readiness close-out)"
   },
   "existingTicketTreatment": {
    "type": "string",
    "enum": [
     "remainValid",
     "exchangeForReplacement",
     "invalidate"
    ],
    "description": "Existing ticket treatment; default remainValid, and invalidate needs its own governed approval (decided 29 September, readiness close-out)"
   },
   "communicationRequirements": {
    "type": "string",
    "description": "Communication requirements to holders and staff",
    "nullable": true
   },
   "reportingTreatment": {
    "type": "string",
    "enum": [
     "keepInReports",
     "reportUnderReplacement",
     "historicalOnly"
    ],
    "description": "Reporting treatment; default keepInReports (decided 29 September, readiness close-out)"
   },
   "activePromotions": {
    "type": "integer",
    "description": "Active promotions"
   },
   "bundles": {
    "type": "integer",
    "description": "Bundles"
   },
   "membershipBenefits": {
    "type": "integer",
    "description": "Membership benefits"
   },
   "resellerAgreements": {
    "type": "integer",
    "description": "Reseller agreements"
   },
   "futureReservations": {
    "type": "integer",
    "description": "Future reservations"
   },
   "activePriceLists": {
    "type": "integer",
    "description": "Active price lists"
   },
   "channelAssignments": {
    "type": "integer",
    "description": "Channel assignments"
   },
   "productId": {
    "type": "string",
    "description": "Product id",
    "format": "uuid"
   },
   "productName": {
    "type": "string",
    "description": "Product name"
   },
   "lifecycleState": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ProductLifecycleState"
     }
    ],
    "description": "Current lifecycle state"
   },
   "upgradePaths": {
    "type": "integer",
    "description": "Upgrade paths"
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
   "dependencies": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Dependencies identified for the rollback"
   },
   "reason": {
    "type": "string",
    "description": "Rollback reason (mandatory)"
   },
   "executionMode": {
    "type": "string",
    "enum": [
     "immediate",
     "scheduled"
    ],
    "description": "Immediate (where authorised) or scheduled"
   },
   "status": {
    "type": "string",
    "description": "Rollback status: requested, awaitingApproval, scheduled, executing, completed, failed or cancelled"
   },
   "scope": {
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
    "description": "Rollback scope"
   },
   "rollbackId": {
    "type": "string",
    "description": "Rollback id",
    "format": "uuid"
   },
   "productId": {
    "type": "string",
    "description": "Product id",
    "format": "uuid"
   },
   "productName": {
    "type": "string",
    "description": "Product name"
   },
   "fromVersion": {
    "type": "integer",
    "description": "Current version rolled back from"
   },
   "toVersion": {
    "type": "integer",
    "description": "Earlier version restored"
   },
   "emergency": {
    "type": "boolean",
    "description": "Emergency rollback"
   },
   "scheduledAt": {
    "type": "string",
    "description": "Scheduled time",
    "format": "date-time",
    "nullable": true
   },
   "requestedBy": {
    "type": "string",
    "description": "Requested by (display name)"
   },
   "requestedAt": {
    "type": "string",
    "description": "Requested",
    "format": "date-time"
   },
   "completedAt": {
    "type": "string",
    "description": "Completed",
    "format": "date-time",
    "nullable": true
   },
   "approvalReference": {
    "type": "string",
    "description": "Approval reference",
    "nullable": true
   }
  }
 }
}
```
