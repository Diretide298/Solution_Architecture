# WS56 — Rules  Workflow  Approval   Automation Engine board 2

**10 screens · 13 operations · 25 schemas · 5 permissions**

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

- **Every control that can be refused must be gated.** 5 permissions apply here:
  `APPROVAL_ACT, APPROVAL_CONFIGURE, APPROVAL_DECIDE, APPROVAL_VIEW, REPORT_VIEW_VENUE`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-248` | Workflow Operations Command Center | listDetail | 1 | 0 | — |
| `ADM-249` | Unified Approval Inbox & Decision Workspace | listDetail | 3 | 0 | — |
| `ADM-250` | Workflow Instance Monitor & Process Timeline | commandCentre | 2 | 1 | — |
| `ADM-251` | Workflow Exception, Failure & Recovery Center | listDetail | 2 | 1 | — |
| `ADM-252` | SLA, Escalation & Bottleneck Monitor | listDetail | 2 | 1 | — |
| `ADM-253` | Automation Execution & Autonomous Action Monitor | listDetail | 1 | 0 | — |
| `ADM-254` | Cross-Module Orchestration Monitor | listDetail | 1 | 0 | — |
| `ADM-255` | Workflow Analytics & Process Performance | commandCentre | 1 | 0 | — |
| `ADM-256` | Process Optimization & Automation Opportunity Center | listDetail | 1 | 0 | — |
| `ADM-257` | AI Workflow Intelligence & Autonomous Governance Center | listDetail | 1 | 0 | — |

## Thin screens in this batch

**ADM-249, ADM-253, ADM-254, ADM-256, ADM-257 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-248",
  "name": "Workflow Operations Command Center",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Rules__Workflow__Approval___Automation_Engine_Reference.pdf",
   "board": "2",
   "number": "13.2.1",
   "page": 23
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/workflow-operations-command-center-adm-248",
   "component": "apps/ticvai-web/src/routes/platform/WorkflowOperationsCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-249",
    "ADM-250",
    "ADM-251",
    "ADM-252",
    "ADM-253",
    "ADM-254",
    "ADM-255",
    "ADM-256",
    "ADM-257"
   ],
   "inferred": false,
   "notes": "**The board's hub.** The workshop specified this module as boards of ten and opened each with a command centre; the other nine screens are that board's detail, so they are reached from here and return here.",
   "transitions": [
    {
     "to": "ADM-002",
     "trigger": "Platform Dashboard",
     "provenance": "derived — ADM-002 declares entryState.params  and ADM-248 holds none of them, so the edge carries nothing and ADM-002 opens cold"
    },
    {
     "to": "ADM-249",
     "trigger": "Works in Unified Approval Inbox & Decision Workspace",
     "provenance": "flow F165 step 1→2",
     "operation": "listWorkflow"
    },
    {
     "to": "ADM-250",
     "trigger": "Works in Workflow Instance Monitor & Process Timeline",
     "provenance": "flow F165 step 3→4",
     "operation": "listWorkflow"
    },
    {
     "to": "ADM-251",
     "trigger": "Works in Workflow Exception, Failure & Recovery Center",
     "provenance": "flow F165 step 5→6",
     "operation": "listWorkflow"
    },
    {
     "to": "ADM-252",
     "trigger": "Works in SLA, Escalation & Bottleneck Monitor",
     "provenance": "flow F165 step 7→8",
     "operation": "listWorkflow"
    },
    {
     "to": "ADM-253",
     "trigger": "Works in Automation Execution & Autonomous Action Monitor",
     "provenance": "flow F165 step 9→10",
     "operation": "listWorkflow"
    },
    {
     "to": "ADM-254",
     "trigger": "Works in Cross-Module Orchestration Monitor",
     "provenance": "flow F165 step 11→12",
     "operation": "listWorkflow"
    },
    {
     "to": "ADM-255",
     "trigger": "Works in Workflow Analytics & Process Performance",
     "provenance": "flow F165 step 13→14",
     "operation": "listWorkflow"
    },
    {
     "to": "ADM-256",
     "trigger": "Works in Process Optimization & Automation Opportunity Center",
     "provenance": "flow F165 step 15→16",
     "operation": "listWorkflow"
    },
    {
     "to": "ADM-257",
     "trigger": "Works in AI Workflow Intelligence & Autonomous Governance Center",
     "provenance": "flow F165 step 17→18",
     "operation": "listWorkflow"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Authorized users can understand the real-time state and health of workflow execution across the entire TICVAI platform.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide administrators and operational managers with a real-time view of all workflow activity across TICVAI.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Workflows Running",
       "bindsTo": "WorkflowOperationsCommandCenterViewSummary.workflowsRunning",
       "operation": "listWorkflow",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Started Today",
       "bindsTo": "WorkflowOperationsCommandCenterViewSummary.startedToday",
       "operation": "listWorkflow",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Completed Today",
       "bindsTo": "WorkflowOperationsCommandCenterViewSummary.completedToday",
       "operation": "listWorkflow",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Pending Approvals",
       "bindsTo": "WorkflowOperationsCommandCenterViewSummary.pendingApprovals",
       "operation": "listWorkflow",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Waiting Tasks",
       "bindsTo": "WorkflowOperationsCommandCenterViewSummary.waitingTasks",
       "operation": "listWorkflow",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "SLA At Risk",
       "bindsTo": "WorkflowOperationsCommandCenterViewSummary.slaAtRisk",
       "operation": "listWorkflow",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "SLA Breached",
       "bindsTo": "WorkflowOperationsCommandCenterViewSummary.slaBreached",
       "operation": "listWorkflow",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Failed Workflows",
       "bindsTo": "WorkflowOperationsCommandCenterViewSummary.failedWorkflows",
       "operation": "listWorkflow",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Escalated",
       "bindsTo": "WorkflowOperationsCommandCenterViewSummary.escalated",
       "operation": "listWorkflow",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Automated Executions",
       "bindsTo": "WorkflowOperationsCommandCenterViewSummary.automatedExecutions",
       "operation": "listWorkflow",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Minutes",
       "bindsTo": "WorkflowOperationsCommandCenterViewSummary.averageCompletionTime",
       "operation": "listWorkflow",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Automation Success Rate",
       "bindsTo": "WorkflowOperationsCommandCenterViewSummary.automationSuccessRate",
       "operation": "listWorkflow",
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
       "label": "Every workflow operations",
       "columns": [
        "WorkflowOperationsCommandCenterView.workflowInstanceId",
        "WorkflowOperationsCommandCenterView.workflow",
        "WorkflowOperationsCommandCenterView.module",
        "WorkflowOperationsCommandCenterView.businessObject",
        "WorkflowOperationsCommandCenterView.initiatedBy",
        "WorkflowOperationsCommandCenterView.started",
        "WorkflowOperationsCommandCenterView.currentStep",
        "WorkflowOperationsCommandCenterView.owner",
        "WorkflowOperationsCommandCenterView.priority",
        "WorkflowOperationsCommandCenterView.sla",
        "WorkflowOperationsCommandCenterView.status"
       ],
       "bindsTo": "WorkflowOperationsCommandCenterView",
       "operation": "listWorkflow",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 23 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected workflow operations",
       "bindsTo": "WorkflowOperationsCommandCenterView",
       "columns": [
        "WorkflowOperationsCommandCenterView.workflowInstanceId",
        "WorkflowOperationsCommandCenterView.workflow",
        "WorkflowOperationsCommandCenterView.module",
        "WorkflowOperationsCommandCenterView.businessObject",
        "WorkflowOperationsCommandCenterView.initiatedBy",
        "WorkflowOperationsCommandCenterView.started",
        "WorkflowOperationsCommandCenterView.currentStep",
        "WorkflowOperationsCommandCenterView.owner",
        "WorkflowOperationsCommandCenterView.priority",
        "WorkflowOperationsCommandCenterView.sla",
        "WorkflowOperationsCommandCenterView.status"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Show activity originating from”, “Use”, “Refund Approval Workflow”.",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 23 §Display"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The workflow operations list.",
   "error": "Could not load. Names which read failed and leaves the workflow operations untouched.",
   "emptyFirstRun": "No workflow operations yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the workflow operations are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listWorkflow",
    "contract": "approvals",
    "purpose": "Workflow Operations Command Center",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "WorkflowOperationsCommandCenterViewSummary.workflowsRunning",
    "WorkflowOperationsCommandCenterViewSummary.startedToday",
    "WorkflowOperationsCommandCenterViewSummary.completedToday",
    "WorkflowOperationsCommandCenterViewSummary.pendingApprovals",
    "WorkflowOperationsCommandCenterViewSummary.waitingTasks",
    "WorkflowOperationsCommandCenterViewSummary.slaAtRisk"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-248",
   "workshopBoard": "wireframes/WS137 Rules  Workflow  Approval   Automation Engine Board 2.dc.html#adm-248"
  },
  "apisNote": "Regenerated 9 September 2026 from Rules__Workflow__Approval___Automation_Engine_Reference.pdf page 23. 23 of 23 labels bound to a contract property; 23 of 48 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-249",
  "name": "Unified Approval Inbox & Decision Workspace",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Rules__Workflow__Approval___Automation_Engine_Reference.pdf",
   "board": "2",
   "number": "13.2.2",
   "page": 25
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/unified-approval-inbox-decision-workspace-adm-249",
   "component": "apps/ticvai-web/src/routes/platform/UnifiedApprovalInboxDecisionWorkspace.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-248"
   ],
   "exitTo": [
    "ADM-248"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-248, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-248",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F165 step 2→3"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Authorized approvers can review and action approval requests from all TICVAI modules through one governed inbox.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide users with one approval inbox across all TICVAI modules. This is extremely important. A manager should not need to open Finance for one approval, Pricing for another, Procurement for another, and Customer Service for another.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every unified approval decision",
       "columns": [
        "ApprovalRequest.id",
        "ApprovalRequest.kind",
        "ApprovalRequest.subjectContract",
        "ApprovalRequest.requestedByPrincipalId",
        "ApprovalRequest.amount",
        "ApprovalRequest.requestedAt",
        "ApprovalRequest.slaDueAt",
        "ApprovalRequest.currentLevel",
        "ApprovalRequest.status"
       ],
       "bindsTo": "ApprovalRequest",
       "operation": "listApprovalRequests",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 25 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected unified approval decision",
       "bindsTo": "ApprovalRequest",
       "columns": [
        "ApprovalRequest.id",
        "ApprovalRequest.kind",
        "ApprovalRequest.subjectContract",
        "ApprovalRequest.requestedByPrincipalId",
        "ApprovalRequest.amount",
        "ApprovalRequest.requestedAt",
        "ApprovalRequest.slaDueAt",
        "ApprovalRequest.currentLevel",
        "ApprovalRequest.status"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Pricing”, “Customer Service”, “Procurement”, “Resource Management”, “Request”, “Context”.",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 25 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Approve",
       "operation": "decideApprovalRequest",
       "provenance": "contract operation decideApprovalRequest"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The unified approval decision list.",
   "error": "Could not load. Names which read failed and leaves the unified approval decision untouched.",
   "emptyFirstRun": "No unified approval decision yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the unified approval decision are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listApprovalRequests",
    "contract": "approvals",
    "purpose": "The approval inbox",
    "trigger": "onLoad",
    "provenance": "decided 29 September, readiness close-out (QA wiring note)"
   },
   {
    "operationId": "decideApprovalRequest",
    "contract": "approvals",
    "purpose": "Approve, reject, return or ask for more",
    "trigger": "onAction",
    "provenance": "decided 29 September, readiness close-out (QA wiring note)",
    "invalidates": [
     "listApprovalRequests"
    ]
   },
   {
    "operationId": "getApprovalRequestScore",
    "contract": "ai",
    "purpose": "Risk band, priority and suggested escalation for the request, as context only (no approve/reject suggestion)",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "ApprovalRequest.id",
    "ApprovalRequest.kind",
    "ApprovalRequest.subjectContract",
    "ApprovalRequest.requestedByPrincipalId",
    "ApprovalRequest.amount",
    "UnifiedApprovalInboxDecisionWorkspaceView.priority"
   ],
   "params": [
    {
     "name": "requestId",
     "from": "navigation"
    },
    {
     "name": "approvalRequestId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-249",
   "workshopBoard": "wireframes/WS137 Rules  Workflow  Approval   Automation Engine Board 2.dc.html#adm-249"
  },
  "apisNote": "Regenerated 9 September 2026 from Rules__Workflow__Approval___Automation_Engine_Reference.pdf page 25. 10 of 10 labels bound to a contract property; 10 of 34 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-250",
  "name": "Workflow Instance Monitor & Process Timeline",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Rules__Workflow__Approval___Automation_Engine_Reference.pdf",
   "board": "2",
   "number": "13.2.3",
   "page": 27
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/workflow-instance-monitor-process-timeline-adm-250",
   "component": "apps/ticvai-web/src/routes/platform/WorkflowInstanceMonitorProcessTimeline.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-248"
   ],
   "exitTo": [
    "ADM-248"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-248, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-248",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F165 step 4→5",
     "operation": "listWorkflowInstanceProcess"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Administrators can reconstruct exactly how a workflow reached its current state and why every major decision or action occurred.",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Display) and a per-row directory (§For each step show) — counts over a population, then the population",
  "purpose": "Allow administrators to inspect exactly what is happening inside an individual running workflow.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Workflow Instance",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 27 §Display",
       "bindsTo": "WorkflowInstanceMonitorProcessTimelineView.workflowInstance"
      },
      {
       "kind": "metricTile",
       "label": "Workflow Name",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 27 §Display",
       "bindsTo": "WorkflowInstanceMonitorProcessTimelineView.workflowName"
      },
      {
       "kind": "metricTile",
       "label": "Version",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 27 §Display",
       "bindsTo": "WorkflowInstanceMonitorProcessTimelineView.version"
      },
      {
       "kind": "metricTile",
       "label": "Source Module",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 27 §Display",
       "bindsTo": "WorkflowInstanceMonitorProcessTimelineView.sourceModule"
      },
      {
       "kind": "metricTile",
       "label": "Business Object",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 27 §Display",
       "bindsTo": "WorkflowInstanceMonitorProcessTimelineView.businessObject"
      },
      {
       "kind": "metricTile",
       "label": "Initiated By",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 27 §Display",
       "bindsTo": "WorkflowInstanceMonitorProcessTimelineView.initiatedBy"
      },
      {
       "kind": "metricTile",
       "label": "Start Time",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 27 §Display",
       "bindsTo": "WorkflowInstanceMonitorProcessTimelineView.startTime"
      },
      {
       "kind": "metricTile",
       "label": "Current Status",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 27 §Display",
       "bindsTo": "WorkflowInstanceMonitorProcessTimelineView.currentStatus"
      },
      {
       "kind": "metricTile",
       "label": "Current Step",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 27 §Display",
       "bindsTo": "WorkflowInstanceMonitorProcessTimelineView.currentStep"
      },
      {
       "kind": "metricTile",
       "label": "SLA",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 27 §Display",
       "bindsTo": "WorkflowInstanceMonitorProcessTimelineView.sla"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every workflow instance process",
       "columns": [
        "WorkflowInstanceMonitorProcessTimelineView.step",
        "WorkflowInstanceMonitorProcessTimelineView.type",
        "WorkflowInstanceMonitorProcessTimelineView.started",
        "WorkflowInstanceMonitorProcessTimelineView.completed",
        "WorkflowInstanceMonitorProcessTimelineView.assignedTo",
        "WorkflowInstanceMonitorProcessTimelineView.input",
        "WorkflowInstanceMonitorProcessTimelineView.output",
        "WorkflowInstanceMonitorProcessTimelineView.decision",
        "WorkflowInstanceMonitorProcessTimelineView.duration",
        "WorkflowInstanceMonitorProcessTimelineView.status"
       ],
       "bindsTo": "WorkflowInstanceMonitorProcessTimelineView",
       "operation": "listWorkflowInstanceProcess",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 27 §For each step show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected workflow instance process",
       "bindsTo": "WorkflowInstanceMonitorProcessTimelineView",
       "columns": [
        "WorkflowInstanceMonitorProcessTimelineView.step",
        "WorkflowInstanceMonitorProcessTimelineView.type",
        "WorkflowInstanceMonitorProcessTimelineView.started",
        "WorkflowInstanceMonitorProcessTimelineView.completed",
        "WorkflowInstanceMonitorProcessTimelineView.assignedTo",
        "WorkflowInstanceMonitorProcessTimelineView.input",
        "WorkflowInstanceMonitorProcessTimelineView.output",
        "WorkflowInstanceMonitorProcessTimelineView.decision",
        "WorkflowInstanceMonitorProcessTimelineView.duration",
        "WorkflowInstanceMonitorProcessTimelineView.status"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Execute Refund”, “Notify Customer”, “Show all”.",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 27 §For each step show"
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
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** Reassign, Retry Step, Skip Step where explicitly allowed, Cancel Workflow, Resume, Escalate, Open Source Record. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 27 §Subject to permissions"
      },
      {
       "kind": "primaryButton",
       "label": "Act on workflow instance",
       "operation": "actOnWorkflowInstance",
       "permission": "APPROVAL_ACT",
       "notes": "**The monitors' action buttons, as one operation** (decided 29 September, writers pass).",
       "provenance": "contract approvals.yaml POST /workflow-instances/{instanceId}/actions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The workflow instance process list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the workflow instance process untouched.",
   "emptyFirstRun": "No workflow instance process yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the workflow instance process are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listWorkflowInstanceProcess",
    "contract": "approvals",
    "purpose": "Workflow Instance Monitor & Process Timeline",
    "trigger": "onLoad"
   },
   {
    "operationId": "actOnWorkflowInstance",
    "contract": "approvals",
    "purpose": "An operator's intervention in a running workflow",
    "trigger": "onAction",
    "invalidates": [
     "listWorkflowInstanceProcess"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-250",
   "workshopBoard": "wireframes/WS137 Rules  Workflow  Approval   Automation Engine Board 2.dc.html#adm-250"
  },
  "apisNote": "Regenerated 9 September 2026 from Rules__Workflow__Approval___Automation_Engine_Reference.pdf page 27. 20 of 20 labels bound to a contract property; 27 of 52 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formActOnWorkflowInstance",
    "component": "modal",
    "trigger": "Act on workflow instance",
    "body": "**Collects what `actOnWorkflowInstance` sends before it is called.** Required: `action`, `reason`. Optional: `workflowStepExecutionId`, `workflowExceptionId`, `assigneePrincipalId`, `alternativeNodeId`, `correctedInput`, `extendByMinutes`, `priority`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "WorkflowInstanceActionInput",
    "confirm": {
     "label": "Act on workflow instance",
     "operation": "actOnWorkflowInstance"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "action",
      "reason",
      "workflowStepExecutionId",
      "workflowExceptionId",
      "assigneePrincipalId",
      "alternativeNodeId",
      "correctedInput",
      "extendByMinutes",
      "priority"
     ]
    },
    "provenance": "contract approvals.yaml POST /workflow-instances/{instanceId}/actions"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "instanceId",
     "from": "navigation",
     "optional": true
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
  "id": "ADM-251",
  "name": "Workflow Exception, Failure & Recovery Center",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Rules__Workflow__Approval___Automation_Engine_Reference.pdf",
   "board": "2",
   "number": "13.2.4",
   "page": 28
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/workflow-exception-failure-recovery-center-adm-251",
   "component": "apps/ticvai-web/src/routes/platform/WorkflowExceptionFailureRecoveryCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-248"
   ],
   "exitTo": [
    "ADM-248"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-248, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-248",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F165 step 6→7",
     "operation": "listWorkflowExceptionFailure"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Failed workflows can be identified, investigated, recovered or safely compensated without losing business context or audit history.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide one controlled workspace for failed workflow executions.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 15 actions on this screen and the screen declares 1 operation.** Unserved: Business Rule Failure, Missing Data, Permission Failure, Integration Failure, Action Failure, Duplicate Event, Service Unavailable, Configuration Error …. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 28 §Support"
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
       "label": "Every workflow exception failure",
       "columns": [
        "WorkflowExceptionFailureRecoveryCenterView.exceptionId",
        "WorkflowExceptionFailureRecoveryCenterView.workflow",
        "WorkflowExceptionFailureRecoveryCenterView.instance",
        "WorkflowExceptionFailureRecoveryCenterView.module",
        "WorkflowExceptionFailureRecoveryCenterView.failedStep",
        "WorkflowExceptionFailureRecoveryCenterView.errorType",
        "WorkflowExceptionFailureRecoveryCenterView.time",
        "Retry Count",
        "WorkflowExceptionFailureRecoveryCenterView.businessImpact",
        "WorkflowExceptionFailureRecoveryCenterView.priority",
        "WorkflowExceptionFailureRecoveryCenterView.owner"
       ],
       "bindsTo": "WorkflowExceptionFailureRecoveryCenterView",
       "operation": "listWorkflowExceptionFailure",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 28 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected workflow exception failure",
       "bindsTo": "WorkflowExceptionFailureRecoveryCenterView",
       "columns": [
        "WorkflowExceptionFailureRecoveryCenterView.exceptionId",
        "WorkflowExceptionFailureRecoveryCenterView.workflow",
        "WorkflowExceptionFailureRecoveryCenterView.instance",
        "WorkflowExceptionFailureRecoveryCenterView.module",
        "WorkflowExceptionFailureRecoveryCenterView.failedStep",
        "WorkflowExceptionFailureRecoveryCenterView.errorType",
        "WorkflowExceptionFailureRecoveryCenterView.time",
        "Retry Count",
        "WorkflowExceptionFailureRecoveryCenterView.businessImpact",
        "WorkflowExceptionFailureRecoveryCenterView.priority",
        "WorkflowExceptionFailureRecoveryCenterView.owner"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Dead-Letter Handling”, “Compensation Actions”, “Possible compensation”.",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 28 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Business Rule Failure",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 28 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Missing Data",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 28 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Permission Failure",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 28 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Integration Failure",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 28 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Action Failure",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 28 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Duplicate Event",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 28 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Service Unavailable",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 28 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Configuration Error",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 28 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Act on workflow instance",
       "operation": "actOnWorkflowInstance",
       "permission": "APPROVAL_ACT",
       "notes": "**The monitors' action buttons, as one operation** (decided 29 September, writers pass).",
       "provenance": "contract approvals.yaml POST /workflow-instances/{instanceId}/actions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The workflow exception failure list.",
   "error": "Could not load. Names which read failed and leaves the workflow exception failure untouched.",
   "emptyFirstRun": "No workflow exception failure yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the workflow exception failure are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listWorkflowExceptionFailure",
    "contract": "approvals",
    "purpose": "Workflow Exception, Failure & Recovery Center",
    "trigger": "onLoad"
   },
   {
    "operationId": "actOnWorkflowInstance",
    "contract": "approvals",
    "purpose": "An operator's intervention in a running workflow",
    "trigger": "onAction",
    "invalidates": [
     "listWorkflowExceptionFailure"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "WorkflowExceptionFailureRecoveryCenterView.exceptionId",
    "WorkflowExceptionFailureRecoveryCenterView.workflow",
    "WorkflowExceptionFailureRecoveryCenterView.instance",
    "WorkflowExceptionFailureRecoveryCenterView.module",
    "WorkflowExceptionFailureRecoveryCenterView.failedStep",
    "WorkflowExceptionFailureRecoveryCenterView.errorType"
   ],
   "params": [
    {
     "name": "instanceId",
     "from": "navigation",
     "optional": true
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-251",
   "workshopBoard": "wireframes/WS137 Rules  Workflow  Approval   Automation Engine Board 2.dc.html#adm-251"
  },
  "apisNote": "Regenerated 9 September 2026 from Rules__Workflow__Approval___Automation_Engine_Reference.pdf page 28. 10 of 11 labels bound to a contract property; 26 of 46 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formActOnWorkflowInstance",
    "component": "modal",
    "trigger": "Act on workflow instance",
    "body": "**Collects what `actOnWorkflowInstance` sends before it is called.** Required: `action`, `reason`. Optional: `workflowStepExecutionId`, `workflowExceptionId`, `assigneePrincipalId`, `alternativeNodeId`, `correctedInput`, `extendByMinutes`, `priority`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "WorkflowInstanceActionInput",
    "confirm": {
     "label": "Act on workflow instance",
     "operation": "actOnWorkflowInstance"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "action",
      "reason",
      "workflowStepExecutionId",
      "workflowExceptionId",
      "assigneePrincipalId",
      "alternativeNodeId",
      "correctedInput",
      "extendByMinutes",
      "priority"
     ]
    },
    "provenance": "contract approvals.yaml POST /workflow-instances/{instanceId}/actions"
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
  "id": "ADM-252",
  "name": "SLA, Escalation & Bottleneck Monitor",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Rules__Workflow__Approval___Automation_Engine_Reference.pdf",
   "board": "2",
   "number": "13.2.5",
   "page": 30
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/sla-escalation-bottleneck-monitor-adm-252",
   "component": "apps/ticvai-web/src/routes/platform/SlaEscalationBottleneckMonitor.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-248"
   ],
   "exitTo": [
    "ADM-248"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-248, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-248",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F165 step 8→9",
     "operation": "listSlaEscalationBottleneck"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Management can identify and resolve workflow bottlenecks before they materially impact business operations.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display; Show) and no metric row",
  "purpose": "Monitor workflows approaching or exceeding configured time limits.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Within SLA",
       "bindsTo": "SlaEscalationBottleneckMonitorViewSummary.withinSla",
       "operation": "listSlaEscalationBottleneck",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "At Risk",
       "bindsTo": "SlaEscalationBottleneckMonitorViewSummary.atRisk",
       "operation": "listSlaEscalationBottleneck",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Breached",
       "bindsTo": "SlaEscalationBottleneckMonitorViewSummary.breached",
       "operation": "listSlaEscalationBottleneck",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Escalated",
       "bindsTo": "SlaEscalationBottleneckMonitorViewSummary.escalated",
       "operation": "listSlaEscalationBottleneck",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Minutes",
       "bindsTo": "SlaEscalationBottleneckMonitorViewSummary.averageProcessingTime",
       "operation": "listSlaEscalationBottleneck",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Minutes",
       "bindsTo": "SlaEscalationBottleneckMonitorViewSummary.averageApprovalTime",
       "operation": "listSlaEscalationBottleneck",
       "provenance": "moved from the row table to the list summary (decided 29 September, readiness close-out)"
      },
      {
       "kind": "metricTile",
       "label": "Longest Waiting Step",
       "bindsTo": "SlaEscalationBottleneckMonitorViewSummary.longestWaitingStep",
       "operation": "listSlaEscalationBottleneck",
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
       "label": "Every sla escalation bottleneck",
       "columns": [
        "SlaEscalationBottleneckMonitorView.workflow",
        "SlaEscalationBottleneckMonitorView.instance",
        "SlaEscalationBottleneckMonitorView.currentStep",
        "SlaEscalationBottleneckMonitorView.owner",
        "SlaEscalationBottleneckMonitorView.started",
        "SlaEscalationBottleneckMonitorView.target",
        "SlaEscalationBottleneckMonitorView.timeRemaining",
        "SlaEscalationBottleneckMonitorView.risk",
        "SlaEscalationBottleneckMonitorView.escalationLevel",
        "SlaEscalationBottleneckMonitorView.firstReminder",
        "SlaEscalationBottleneckMonitorView.secondReminder",
        "SlaEscalationBottleneckMonitorView.managerEscalation",
        "SlaEscalationBottleneckMonitorView.executiveEscalation",
        "SlaEscalationBottleneckMonitorView.finalOutcome"
       ],
       "bindsTo": "SlaEscalationBottleneckMonitorView",
       "operation": "listSlaEscalationBottleneck",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 30 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected sla escalation bottleneck",
       "bindsTo": "SlaEscalationBottleneckMonitorView",
       "columns": [
        "SlaEscalationBottleneckMonitorView.workflow",
        "SlaEscalationBottleneckMonitorView.instance",
        "SlaEscalationBottleneckMonitorView.currentStep",
        "SlaEscalationBottleneckMonitorView.owner",
        "SlaEscalationBottleneckMonitorView.started",
        "SlaEscalationBottleneckMonitorView.target",
        "SlaEscalationBottleneckMonitorView.timeRemaining",
        "SlaEscalationBottleneckMonitorView.risk",
        "SlaEscalationBottleneckMonitorView.escalationLevel",
        "SlaEscalationBottleneckMonitorView.firstReminder",
        "SlaEscalationBottleneckMonitorView.secondReminder",
        "SlaEscalationBottleneckMonitorView.managerEscalation",
        "SlaEscalationBottleneckMonitorView.executiveEscalation",
        "SlaEscalationBottleneckMonitorView.finalOutcome"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Purchase Order Approval”, “Breakdown”.",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 30 §Display"
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
       "notes": "**The pack separates these permissions and no action on the screen claims them yet:** Reassign, Escalate, Extend SLA, Add Backup Approver, Change Priority. Each needs attaching to the control it gates, or the screen needs the control.",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 30 §Authorized users can"
      },
      {
       "kind": "primaryButton",
       "label": "Act on workflow instance",
       "operation": "actOnWorkflowInstance",
       "permission": "APPROVAL_ACT",
       "notes": "**The monitors' action buttons, as one operation** (decided 29 September, writers pass).",
       "provenance": "contract approvals.yaml POST /workflow-instances/{instanceId}/actions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The sla escalation bottleneck list.",
   "error": "Could not load. Names which read failed and leaves the sla escalation bottleneck untouched.",
   "emptyFirstRun": "No sla escalation bottleneck yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the sla escalation bottleneck are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listSlaEscalationBottleneck",
    "contract": "approvals",
    "purpose": "SLA, Escalation & Bottleneck Monitor",
    "trigger": "onLoad"
   },
   {
    "operationId": "actOnWorkflowInstance",
    "contract": "approvals",
    "purpose": "An operator's intervention in a running workflow",
    "trigger": "onAction",
    "invalidates": [
     "listSlaEscalationBottleneck"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "SlaEscalationBottleneckMonitorViewSummary.withinSla",
    "SlaEscalationBottleneckMonitorViewSummary.atRisk",
    "SlaEscalationBottleneckMonitorViewSummary.breached",
    "SlaEscalationBottleneckMonitorViewSummary.escalated",
    "SlaEscalationBottleneckMonitorViewSummary.averageProcessingTime",
    "SlaEscalationBottleneckMonitorViewSummary.averageApprovalTime"
   ],
   "params": [
    {
     "name": "instanceId",
     "from": "navigation",
     "optional": true
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-252",
   "workshopBoard": "wireframes/WS137 Rules  Workflow  Approval   Automation Engine Board 2.dc.html#adm-252"
  },
  "apisNote": "Regenerated 9 September 2026 from Rules__Workflow__Approval___Automation_Engine_Reference.pdf page 30. 21 of 21 labels bound to a contract property; 26 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "overlays": [
   {
    "id": "formActOnWorkflowInstance",
    "component": "modal",
    "trigger": "Act on workflow instance",
    "body": "**Collects what `actOnWorkflowInstance` sends before it is called.** Required: `action`, `reason`. Optional: `workflowStepExecutionId`, `workflowExceptionId`, `assigneePrincipalId`, `alternativeNodeId`, `correctedInput`, `extendByMinutes`, `priority`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "WorkflowInstanceActionInput",
    "confirm": {
     "label": "Act on workflow instance",
     "operation": "actOnWorkflowInstance"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "action",
      "reason",
      "workflowStepExecutionId",
      "workflowExceptionId",
      "assigneePrincipalId",
      "alternativeNodeId",
      "correctedInput",
      "extendByMinutes",
      "priority"
     ]
    },
    "provenance": "contract approvals.yaml POST /workflow-instances/{instanceId}/actions"
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
  "id": "ADM-253",
  "name": "Automation Execution & Autonomous Action Monitor",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Rules__Workflow__Approval___Automation_Engine_Reference.pdf",
   "board": "2",
   "number": "13.2.6",
   "page": 31
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/automation-execution-autonomous-action-monitor-adm-253",
   "component": "apps/ticvai-web/src/routes/platform/AutomationExecutionAutonomousActionMonitor.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-248"
   ],
   "exitTo": [
    "ADM-248"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-248, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-248",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F165 step 10→11",
     "operation": "createAutomationAutonomouAction"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "immediate suspension where required.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide visibility and governance over actions executed automatically by TICVAI. This becomes especially important as TICVAI becomes more AI-driven.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every automation execution autonomous",
       "columns": [
        "AutomationExecutionAutonomousActionMonitorView.automatedActionsToday",
        "AutomationExecutionAutonomousActionMonitorView.successful",
        "AutomationExecutionAutonomousActionMonitorView.failed",
        "AutomationExecutionAutonomousActionMonitorView.humanConfirmationRequired",
        "AutomationExecutionAutonomousActionMonitorView.reversed",
        "AutomationExecutionAutonomousActionMonitorView.suspended",
        "AutomationExecutionAutonomousActionMonitorView.estimatedManualActionsAvoided",
        "AutomationExecutionAutonomousActionMonitorView.estimatedTimeSaved",
        "AutomationExecutionAutonomousActionMonitorView.automation",
        "Trigger",
        "AutomationExecutionAutonomousActionMonitorView.businessObject",
        "AutomationExecutionAutonomousActionMonitorView.rule",
        "AutomationExecutionAutonomousActionMonitorView.action",
        "AutomationExecutionAutonomousActionMonitorView.result",
        "AutomationExecutionAutonomousActionMonitorView.confidenceWhereAiAssisted",
        "AutomationExecutionAutonomousActionMonitorView.executionTime",
        "AutomationExecutionAutonomousActionMonitorView.status"
       ],
       "bindsTo": "AutomationExecutionAutonomousActionMonitorView",
       "operation": "createAutomationAutonomouAction",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 31 §Display"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected automation execution autonomous",
       "bindsTo": "AutomationExecutionAutonomousActionMonitorView",
       "columns": [
        "AutomationExecutionAutonomousActionMonitorView.automatedActionsToday",
        "AutomationExecutionAutonomousActionMonitorView.successful",
        "AutomationExecutionAutonomousActionMonitorView.failed",
        "AutomationExecutionAutonomousActionMonitorView.humanConfirmationRequired",
        "AutomationExecutionAutonomousActionMonitorView.reversed",
        "AutomationExecutionAutonomousActionMonitorView.suspended",
        "AutomationExecutionAutonomousActionMonitorView.estimatedManualActionsAvoided",
        "AutomationExecutionAutonomousActionMonitorView.estimatedTimeSaved",
        "AutomationExecutionAutonomousActionMonitorView.automation",
        "Trigger",
        "AutomationExecutionAutonomousActionMonitorView.businessObject",
        "AutomationExecutionAutonomousActionMonitorView.rule",
        "AutomationExecutionAutonomousActionMonitorView.action",
        "AutomationExecutionAutonomousActionMonitorView.result",
        "AutomationExecutionAutonomousActionMonitorView.confidenceWhereAiAssisted",
        "AutomationExecutionAutonomousActionMonitorView.executionTime",
        "AutomationExecutionAutonomousActionMonitorView.status"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Waiver Reminder Automation”, “Authorized administrators can”.",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 31 §Display"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create",
       "provenance": "contract operation createAutomationAutonomouAction"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The automation execution autonomous list.",
   "error": "Could not load. Names which read failed and leaves the automation execution autonomous untouched.",
   "emptyFirstRun": "No automation execution autonomous yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the automation execution autonomous are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createAutomationAutonomouAction",
    "contract": "approvals",
    "purpose": "Automation Execution & Autonomous Action Monitor",
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "preloaded": [
    "AutomationExecutionAutonomousActionMonitorView.automatedActionsToday",
    "AutomationExecutionAutonomousActionMonitorView.successful",
    "AutomationExecutionAutonomousActionMonitorView.failed",
    "AutomationExecutionAutonomousActionMonitorView.humanConfirmationRequired",
    "AutomationExecutionAutonomousActionMonitorView.reversed",
    "AutomationExecutionAutonomousActionMonitorView.suspended"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-253",
   "workshopBoard": "wireframes/WS137 Rules  Workflow  Approval   Automation Engine Board 2.dc.html#adm-253"
  },
  "apisNote": "Regenerated 9 September 2026 from Rules__Workflow__Approval___Automation_Engine_Reference.pdf page 31. 16 of 17 labels bound to a contract property; 17 of 45 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-254",
  "name": "Cross-Module Orchestration Monitor",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Rules__Workflow__Approval___Automation_Engine_Reference.pdf",
   "board": "2",
   "number": "13.2.7",
   "page": 33
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/cross-module-orchestration-monitor-adm-254",
   "component": "apps/ticvai-web/src/routes/platform/CrossModuleOrchestrationMonitor.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-248"
   ],
   "exitTo": [
    "ADM-248"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-248, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-248",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F165 step 12→13",
     "operation": "listCrossModuleOrchestration"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Complex cross-module business processes can be monitored as one business workflow rather than requiring administrators to inspect individual microservices independently.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Monitor complex workflows involving multiple TICVAI services. Example — Group Booking Confirmation",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 33"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 33"
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
       "impliedBy": "listCrossModuleOrchestration",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The cross-module orchestration list.",
   "error": "Could not load. Names which read failed and leaves the cross-module orchestration untouched.",
   "emptyFirstRun": "No cross-module orchestration yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the cross-module orchestration are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listCrossModuleOrchestration",
    "contract": "approvals",
    "purpose": "Cross-Module Orchestration Monitor",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "CrossModuleOrchestrationMonitorView.service"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-254",
   "workshopBoard": "wireframes/WS137 Rules  Workflow  Approval   Automation Engine Board 2.dc.html#adm-254"
  },
  "apisNote": "Regenerated 9 September 2026 from Rules__Workflow__Approval___Automation_Engine_Reference.pdf page 33. 0 of 0 labels bound to a contract property; 0 of 38 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-255",
  "name": "Workflow Analytics & Process Performance",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Rules__Workflow__Approval___Automation_Engine_Reference.pdf",
   "board": "2",
   "number": "13.2.8",
   "page": 34
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/workflow-analytics-process-performance-adm-255",
   "component": "apps/ticvai-web/src/routes/platform/WorkflowAnalyticsProcessPerformance.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-248"
   ],
   "exitTo": [
    "ADM-248"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-248, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-248",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F165 step 14→15",
     "operation": "listWorkflowProcessPerformance"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Management can quantitatively evaluate whether workflows and automation are improving operational efficiency.",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Analyze; Measure; Compare) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Measure how effectively TICVAI's business workflows are performing.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "filters",
     "components": [
      {
       "kind": "searchField",
       "label": "Search workflow analytics process",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 34 §Analyze By"
      },
      {
       "kind": "multiSelect",
       "label": "Filter by",
       "columns": [
        "Workflow",
        "Module",
        "Venue",
        "Brand",
        "Business Process",
        "Department",
        "Approver",
        "User",
        "Date",
        "Transaction Value"
       ],
       "notes": "The pack filters this screen by workflow, module, venue, brand, business process, department and 4 more — which are present is a decision the pack already made.",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 34 §Analyze By"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Workflow Volume",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 34 §Analyze",
       "bindsTo": "WorkflowAnalyticsProcessPerformanceView.workflowVolume"
      },
      {
       "kind": "metricTile",
       "label": "Completion Rate",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 34 §Analyze",
       "bindsTo": "WorkflowAnalyticsProcessPerformanceView.completionRate"
      },
      {
       "kind": "metricTile",
       "label": "Failure Rate",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 34 §Analyze",
       "bindsTo": "WorkflowAnalyticsProcessPerformanceView.failureRate"
      },
      {
       "kind": "metricTile",
       "label": "Average Completion Time",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 34 §Analyze",
       "bindsTo": "WorkflowAnalyticsProcessPerformanceView.averageCompletionTime"
      },
      {
       "kind": "metricTile",
       "label": "Approval Time",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 34 §Analyze",
       "bindsTo": "WorkflowAnalyticsProcessPerformanceView.approvalTime"
      },
      {
       "kind": "metricTile",
       "label": "Automation Rate",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 34 §Analyze",
       "bindsTo": "WorkflowAnalyticsProcessPerformanceView.automationRate"
      },
      {
       "kind": "metricTile",
       "label": "Escalation Rate",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 34 §Analyze",
       "bindsTo": "WorkflowAnalyticsProcessPerformanceView.escalationRate"
      },
      {
       "kind": "metricTile",
       "label": "Rejection Rate",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 34 §Analyze",
       "bindsTo": "WorkflowAnalyticsProcessPerformanceView.rejectionRate"
      },
      {
       "kind": "metricTile",
       "label": "Rework Rate",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 34 §Analyze",
       "bindsTo": "WorkflowAnalyticsProcessPerformanceView.reworkRate"
      },
      {
       "kind": "metricTile",
       "label": "SLA Compliance",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 34 §Analyze",
       "bindsTo": "WorkflowAnalyticsProcessPerformanceView.slaCompliance"
      },
      {
       "kind": "metricTile",
       "label": "Average Approval Time",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 34 §Measure",
       "bindsTo": "WorkflowAnalyticsProcessPerformanceView.averageApprovalTime"
      },
      {
       "kind": "metricTile",
       "label": "Approval Rate",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 34 §Measure",
       "bindsTo": "WorkflowAnalyticsProcessPerformanceView.approvalRate"
      },
      {
       "kind": "metricTile",
       "label": "Request Changes Rate",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 34 §Measure",
       "bindsTo": "WorkflowAnalyticsProcessPerformanceView.requestChangesRate"
      },
      {
       "kind": "metricTile",
       "label": "Delegation Rate",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 34 §Measure",
       "bindsTo": "WorkflowAnalyticsProcessPerformanceView.delegationRate"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The workflow analytics process list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the workflow analytics process untouched.",
   "emptyFirstRun": "No workflow analytics process yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the workflow analytics process are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listWorkflowProcessPerformance",
    "contract": "approvals",
    "purpose": "Workflow Analytics & Process Performance",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-255",
   "workshopBoard": "wireframes/WS137 Rules  Workflow  Approval   Automation Engine Board 2.dc.html#adm-255"
  },
  "apisNote": "Regenerated 9 September 2026 from Rules__Workflow__Approval___Automation_Engine_Reference.pdf page 34. 15 of 25 labels bound to a contract property; 25 of 48 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-256",
  "name": "Process Optimization & Automation Opportunity Center",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Rules__Workflow__Approval___Automation_Engine_Reference.pdf",
   "board": "2",
   "number": "13.2.9",
   "page": 36
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/process-optimization-automation-opportunity-center-adm-256",
   "component": "apps/ticvai-web/src/routes/platform/ProcessOptimizationAutomationOpportunityCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-248"
   ],
   "exitTo": [
    "ADM-248"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-248, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-248",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F165 step 16→17",
     "operation": "listProcessAutomationOpportunity"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "operational evidence rather than assumptions.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Identify; Display) and no metric row",
  "purpose": "Identify business processes that should be simplified, redesigned or automated. This is where TICVAI moves beyond simply running workflows.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every process optimization automation",
       "columns": [
        "ProcessOptimizationAutomationOpportunityCenterView.opportunityType",
        "Duplicate Steps",
        "ProcessOptimizationAutomationOpportunityCenterView.process",
        "ProcessOptimizationAutomationOpportunityCenterView.module",
        "ProcessOptimizationAutomationOpportunityCenterView.monthlyVolume",
        "ProcessOptimizationAutomationOpportunityCenterView.currentSteps",
        "ProcessOptimizationAutomationOpportunityCenterView.averageDuration",
        "ProcessOptimizationAutomationOpportunityCenterView.manualSteps",
        "ProcessOptimizationAutomationOpportunityCenterView.approvalRate",
        "ProcessOptimizationAutomationOpportunityCenterView.exceptionRate",
        "ProcessOptimizationAutomationOpportunityCenterView.estimatedOpportunity"
       ],
       "bindsTo": "ProcessOptimizationAutomationOpportunityCenterView",
       "operation": "listProcessAutomationOpportunity",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 36 §Identify"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected process optimization automation",
       "bindsTo": "ProcessOptimizationAutomationOpportunityCenterView",
       "columns": [
        "ProcessOptimizationAutomationOpportunityCenterView.opportunityType",
        "Duplicate Steps",
        "ProcessOptimizationAutomationOpportunityCenterView.process",
        "ProcessOptimizationAutomationOpportunityCenterView.module",
        "ProcessOptimizationAutomationOpportunityCenterView.monthlyVolume",
        "ProcessOptimizationAutomationOpportunityCenterView.currentSteps",
        "ProcessOptimizationAutomationOpportunityCenterView.averageDuration",
        "ProcessOptimizationAutomationOpportunityCenterView.manualSteps",
        "ProcessOptimizationAutomationOpportunityCenterView.approvalRate",
        "ProcessOptimizationAutomationOpportunityCenterView.exceptionRate",
        "ProcessOptimizationAutomationOpportunityCenterView.estimatedOpportunity"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Low-Value Refund Approval”, “Before changing anything”, “Estimated result”.",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 36 §Identify"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The process optimization automation list.",
   "error": "Could not load. Names which read failed and leaves the process optimization automation untouched.",
   "emptyFirstRun": "No process optimization automation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the process optimization automation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listProcessAutomationOpportunity",
    "contract": "approvals",
    "purpose": "Process Optimization & Automation Opportunity Center",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "ProcessOptimizationAutomationOpportunityCenterView.opportunityType",
    "Duplicate Steps"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-256",
   "workshopBoard": "wireframes/WS137 Rules  Workflow  Approval   Automation Engine Board 2.dc.html#adm-256"
  },
  "apisNote": "Regenerated 9 September 2026 from Rules__Workflow__Approval___Automation_Engine_Reference.pdf page 36. 17 of 18 labels bound to a contract property; 18 of 31 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-257",
  "name": "AI Workflow Intelligence & Autonomous Governance Center",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Rules__Workflow__Approval___Automation_Engine_Reference.pdf",
   "board": "2",
   "number": "13.2.10",
   "page": 37
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/ai-workflow-intelligence-autonomous-governance-center-adm-257",
   "component": "apps/ticvai-web/src/routes/platform/AiWorkflowIntelligenceAutonomousGovernanceCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-248"
   ],
   "exitTo": [
    "ADM-248"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-248, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation."
  },
  "density": "compact",
  "purposeNote": "explainability, human governance, version control and immediate operational control. Board 2 — Final Screen Register",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Analyze) and no metric row",
  "purpose": "Create the AI intelligence layer across TICVAI's entire rules, workflow and automation ecosystem. This is the management-level AI brain for Area 13.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every workflow intelligence autonomous",
       "bindsTo": "AiWorkflowIntelligenceAutonomousGovernanceCenterView",
       "operation": "listWorkflowAutonomouGovernance",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 37 §Analyze"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected workflow intelligence autonomous",
       "bindsTo": "AiWorkflowIntelligenceAutonomousGovernanceCenterView",
       "notes": "The pack groups this record's detail under its own headings: “Natural-Language Questions”, “Actual common process”, “Automation”, “Approval Simplification”, “SLA”, “Workflow Redesign”.",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 37 §Analyze"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The workflow intelligence autonomous list.",
   "error": "Could not load. Names which read failed and leaves the workflow intelligence autonomous untouched.",
   "emptyFirstRun": "No workflow intelligence autonomous yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the workflow intelligence autonomous are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listWorkflowAutonomouGovernance",
    "contract": "approvals",
    "purpose": "AI Workflow Intelligence & Autonomous Governance Center",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": []
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-257",
   "workshopBoard": "wireframes/WS137 Rules  Workflow  Approval   Automation Engine Board 2.dc.html#adm-257"
  },
  "apisNote": "Regenerated 9 September 2026 from Rules__Workflow__Approval___Automation_Engine_Reference.pdf page 37. 11 of 11 labels bound to a contract property; 12 of 108 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "actOnWorkflowInstance": {
  "method": "POST",
  "path": "/workflow-instances/{instanceId}/actions",
  "contract": "approvals",
  "summary": "An operator's intervention in a running workflow",
  "permission": "APPROVAL_ACT",
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
  "requestBody": "WorkflowInstanceActionInput",
  "responds": "WorkflowInstance"
 },
 "createAutomationAutonomouAction": {
  "method": "POST",
  "path": "/automation-autonomou-action",
  "contract": "approvals",
  "summary": "Automation Execution & Autonomous Action Monitor",
  "permission": "APPROVAL_CONFIGURE",
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
  "requestBody": "AutomationExecutionAutonomousActionMonitorInput",
  "responds": "AutomationExecutionAutonomousActionMonitorView"
 },
 "decideApprovalRequest": {
  "method": "POST",
  "path": "/approval-requests/{requestId}/decide",
  "contract": "approvals",
  "summary": "Approve, reject, return or ask for information",
  "permission": "APPROVAL_DECIDE",
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
  "responds": "ApprovalRequest"
 },
 "getApprovalRequestScore": {
  "method": "GET",
  "path": "/approval-requests/{approvalRequestId}/score",
  "contract": "ai",
  "summary": "The latest context score of an approval request",
  "permission": "APPROVAL_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AiApprovalRequestScore"
 },
 "listApprovalRequests": {
  "method": "GET",
  "path": "/approval-requests",
  "contract": "approvals",
  "summary": "Requests awaiting a decision, or already decided",
  "permission": "APPROVAL_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "assignedToMe",
    "in": "query",
    "required": null
   },
   {
    "name": "raisedByMe",
    "in": "query",
    "required": null
   },
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "kind",
    "in": "query",
    "required": null
   },
   {
    "name": "breachingWithinMinutes",
    "in": "query",
    "required": null
   },
   {
    "name": "sort",
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
 "listCrossModuleOrchestration": {
  "method": "GET",
  "path": "/cross-module-orchestration",
  "contract": "approvals",
  "summary": "Cross-Module Orchestration Monitor",
  "permission": "APPROVAL_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "correlationId",
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
 "listProcessAutomationOpportunity": {
  "method": "GET",
  "path": "/process-automation-opportunity",
  "contract": "approvals",
  "summary": "Process Optimization & Automation Opportunity Center",
  "permission": "REPORT_VIEW_VENUE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "opportunityType",
    "in": "query",
    "required": false
   },
   {
    "name": "module",
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
 "listSlaEscalationBottleneck": {
  "method": "GET",
  "path": "/sla-escalation-bottleneck",
  "contract": "approvals",
  "summary": "SLA, Escalation & Bottleneck Monitor",
  "permission": "APPROVAL_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "workflow",
    "in": "query",
    "required": false
   },
   {
    "name": "risk",
    "in": "query",
    "required": false
   },
   {
    "name": "escalationLevel",
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
 "listWorkflow": {
  "method": "GET",
  "path": "/workflow",
  "contract": "approvals",
  "summary": "Workflow Operations Command Center",
  "permission": "APPROVAL_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "module",
    "in": "query",
    "required": false
   },
   {
    "name": "status",
    "in": "query",
    "required": false
   },
   {
    "name": "priority",
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
 "listWorkflowAutonomouGovernance": {
  "method": "GET",
  "path": "/workflow-autonomou-governance",
  "contract": "approvals",
  "summary": "AI Workflow Intelligence & Autonomous Governance Center",
  "permission": "APPROVAL_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "autonomyLevel",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "AiWorkflowIntelligenceAutonomousGovernanceCenterView"
 },
 "listWorkflowExceptionFailure": {
  "method": "GET",
  "path": "/workflow-exception-failure",
  "contract": "approvals",
  "summary": "Workflow Exception, Failure & Recovery Center",
  "permission": "APPROVAL_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "errorType",
    "in": "query",
    "required": false
   },
   {
    "name": "module",
    "in": "query",
    "required": false
   },
   {
    "name": "priority",
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
 "listWorkflowInstanceProcess": {
  "method": "GET",
  "path": "/workflow-instance-process",
  "contract": "approvals",
  "summary": "Workflow Instance Monitor & Process Timeline",
  "permission": "APPROVAL_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "workflowInstance",
    "in": "query",
    "required": false
   },
   {
    "name": "sourceModule",
    "in": "query",
    "required": false
   },
   {
    "name": "currentStatus",
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
 "listWorkflowProcessPerformance": {
  "method": "GET",
  "path": "/workflow-process-performance",
  "contract": "approvals",
  "summary": "Workflow Analytics & Process Performance",
  "permission": "REPORT_VIEW_VENUE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "workflow",
    "in": "query",
    "required": false
   },
   {
    "name": "module",
    "in": "query",
    "required": false
   },
   {
    "name": "venue",
    "in": "query",
    "required": false
   },
   {
    "name": "brand",
    "in": "query",
    "required": false
   },
   {
    "name": "businessProcess",
    "in": "query",
    "required": false
   },
   {
    "name": "department",
    "in": "query",
    "required": false
   },
   {
    "name": "approver",
    "in": "query",
    "required": false
   },
   {
    "name": "user",
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
    "name": "minTransactionValue",
    "in": "query",
    "required": false
   },
   {
    "name": "maxTransactionValue",
    "in": "query",
    "required": false
   }
  ],
  "requestBody": null,
  "responds": "WorkflowAnalyticsProcessPerformanceView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AiApprovalRequestScore": {
  "type": "object",
  "x-ticvai-persistence": "ai.approval_request_score",
  "description": "**Context for an approval reviewer** (11.1.73..75): risk, priority and a suggested escalation for one pending request, the latest per request. **There is no approve or reject field, by design** (minutes of 8 September: AI in approvals never recommends or influences approve or reject).",
  "required": [
   "approvalRequestId",
   "riskScore",
   "riskBand",
   "priorityScore",
   "escalationSuggestion"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "approvalRequestId": {
    "type": "string",
    "format": "uuid",
    "x-ticvai-references": "approvals.request"
   },
   "trigger": {
    "type": "string",
    "enum": [
     "submitted",
     "resubmitted",
     "slaTick",
     "escalated"
    ]
   },
   "riskScore": {
    "type": "integer",
    "minimum": 0,
    "maximum": 100
   },
   "riskBand": {
    "type": "string",
    "enum": [
     "low",
     "medium",
     "high",
     "critical"
    ],
    "description": "Design 5.6: a risk score and band, never a probability."
   },
   "priorityScore": {
    "type": "integer",
    "minimum": 0,
    "maximum": 100,
    "description": "For ordering work in an inbox; higher first."
   },
   "escalationSuggestion": {
    "type": "object",
    "required": [
     "action"
    ],
    "properties": {
     "action": {
      "type": "string",
      "enum": [
       "escalate",
       "addBackupApprover",
       "none"
      ]
     },
     "reason": {
      "type": "string",
      "nullable": true
     }
    },
    "description": "A suggestion for an SLA problem, carried out if at all by a person or the tenant's SLA policy."
   },
   "signals": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "code": {
       "type": "string",
       "description": "e.g. `amountAboveRequesterNorm`, `requesterEntityRisk`, `outOfHours`, `irreversibleAction`, `slaDueSoon`, `stepBreachRate`, `approverUnavailable`."
      },
      "contribution": {
       "type": "number"
      },
      "detail": {
       "type": "string",
       "nullable": true
      }
     }
    }
   },
   "basis": {
    "$ref": "#/components/schemas/SuggestionBasis"
   },
   "decisionRecordId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "scoredAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."
   }
  }
 },
 "AiWorkflowIntelligenceAutonomousGovernanceCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over the AI use-case register, which belongs to the AI service (the AI design is under review, 29 September); not an approvals table and not read directly from here",
  "description": "**What AI Workflow Intelligence & Autonomous Governance Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "useCaseId": {
    "type": "string",
    "description": "AI use case identifier"
   },
   "aiModel": {
    "type": "string",
    "description": "AI Model"
   },
   "aiService": {
    "type": "string",
    "description": "AI Service"
   },
   "useCase": {
    "type": "string",
    "description": "Use Case"
   },
   "autonomyLevel": {
    "type": "string",
    "enum": [
     "observe",
     "recommend",
     "prepare",
     "governedAutomation",
     "autonomousLowRisk"
    ],
    "description": "Level 0 to 4; approval decisions are held at observe"
   },
   "decisionScope": {
    "type": "string",
    "description": "Decision Scope"
   },
   "confidenceThreshold": {
    "type": "number",
    "description": "Confidence Threshold"
   },
   "humanApprovalRequirement": {
    "type": "string",
    "description": "Human Approval Requirement"
   },
   "executionVolume": {
    "type": "integer",
    "description": "Execution Volume"
   },
   "exceptionRate": {
    "type": "number",
    "description": "Exception Rate"
   },
   "lastReview": {
    "type": "string",
    "format": "date-time",
    "description": "Last Review"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   },
   "overrideRate": {
    "type": "number",
    "description": "Override rate"
   }
  },
  "required": [
   "useCaseId"
  ]
 },
 "ApprovalDecision": {
  "type": "object",
  "x-ticvai-persistence": "approvals.decision",
  "required": [
   "level",
   "principalId",
   "decision",
   "decidedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "level": {
    "type": "integer"
   },
   "principalId": {
    "type": "string",
    "format": "uuid"
   },
   "displayName": {
    "type": "string"
   },
   "isDelegate": {
    "type": "boolean"
   },
   "delegatedFrom": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "decision": {
    "type": "string",
    "enum": [
     "approve",
     "reject"
    ]
   },
   "comment": {
    "type": "string",
    "nullable": true
   },
   "reason": {
    "type": "string",
    "nullable": true
   },
   "usedMfa": {
    "type": "boolean"
   },
   "signatureRef": {
    "type": "string",
    "nullable": true
   },
   "decidedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "ApprovalKind": {
  "type": "string",
  "description": "11.1.7 and 11.1.30–11.1.37. **The first four already exist as bespoke implementations** and this contract is what they collapse into.\n**Which actions route here — decided 28 September, audit R144.** Finance and procurement acts go through this engine to a **finance approver**: closing a fiscal period (`periodClose`), reopening one (`periodReopen`), cancelling a purchase order (`purchaseOrderCancel`) and closing one short (`purchaseOrderShortClose`). The tenant default matrix for each of these names the finance approver role; a venue may tighten it and never loosen it. Starting a release rollout routes through `releasePromotion` to the platform release manager (a holder of `PLATFORM_RELEASE_PROMOTE`). **Not every `requiresApproval` goes here:** reopening a shift, recounting a stock count and a retail return above the venue threshold take a supervisor's step-up on the same device instead, and never raise a request.\n**Catalogue change requests route through `productChange` and `pricingChange`** (decided 29 September, writers pass): a product change and a price or pricing change raised in `catalogue` ask for approval under these two kinds, so a venue can route product edits and price edits to different approvers.\n",
  "enum": [
   "refund",
   "priceOverride",
   "discountOverride",
   "complimentaryTicket",
   "membershipCancellation",
   "accessPermissionChange",
   "configurationChange",
   "aiRecommendation",
   "releasePromotion",
   "requisition",
   "stockWriteOff",
   "journalEntry",
   "periodClose",
   "periodReopen",
   "purchaseOrderCancel",
   "purchaseOrderShortClose",
   "tenantMigration",
   "productChange",
   "pricingChange"
  ]
 },
 "ApprovalMode": {
  "type": "string",
  "description": "11.1.43–11.1.46. **Sequential** asks one at a time, **parallel** asks everyone at once, **consensus** needs all of them, **majority** needs more than half.\nParallel and consensus differ in when it completes: parallel completes on the first approval, consensus waits for all. Conflating them is how a four-eyes rule turns into a one-eye rule.\n",
  "enum": [
   "sequential",
   "parallel",
   "consensus",
   "majority"
  ]
 },
 "ApprovalRequest": {
  "type": "object",
  "x-ticvai-persistence": "approvals.request",
  "required": [
   "id",
   "kind",
   "status",
   "requestedByPrincipalId",
   "requestedAt"
  ],
  "properties": {
   "id": {
    "type": "string"
   },
   "kind": {
    "$ref": "#/components/schemas/ApprovalKind"
   },
   "rerouteOnNoApprover": {
    "type": "boolean",
    "default": true,
    "description": "BL-154. **An approver on leave is an approval that waits for them to come back.** Reroutes to the next in the chain rather than stalling — `workforce` already knows who is on leave, and an approval queue nobody is watching is the thing that stops a venue.\n"
   },
   "outOfOfficeDelegateId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "allowEmailApproval": {
    "type": "boolean",
    "default": false,
    "description": "**Approving from an email link with no second factor is the weakest path in the system**, so it is off by default and available only below a configured value.\n"
   },
   "reopenedFrom": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**Reopening a decided approval creates a new one that points back.** Editing a decision in place destroys the record of what was originally approved, which is the only thing an audit wants.\n"
   },
   "status": {
    "$ref": "#/components/schemas/ApprovalStatus"
   },
   "subjectContract": {
    "type": "string"
   },
   "subjectType": {
    "type": "string"
   },
   "subjectId": {
    "type": "string"
   },
   "scopePath": {
    "type": "string"
   },
   "summary": {
    "type": "string"
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "justification": {
    "type": "string",
    "nullable": true
   },
   "requestedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "matrixVersion": {
    "type": "integer"
   },
   "mode": {
    "$ref": "#/components/schemas/ApprovalMode"
   },
   "currentLevel": {
    "type": "integer"
   },
   "totalLevels": {
    "type": "integer"
   },
   "pendingApprovers": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "principalId": {
       "type": "string",
       "format": "uuid"
      },
      "displayName": {
       "type": "string"
      },
      "isDelegate": {
       "type": "boolean"
      }
     }
    }
   },
   "decisions": {
    "type": "array",
    "description": "Every decision at every level, in order. **Immutable once the request completes** (11.1.56) — an approval is evidence, and amending one is a different fact.\n",
    "items": {
     "$ref": "#/components/schemas/ApprovalDecision"
    }
   },
   "escalations": {
    "type": "array",
    "description": "11.1.48. Who was asked, when, and why it moved up. **Escalation adds an approver rather than replacing one**, so the original stays in the record.\n",
    "items": {
     "type": "object",
     "properties": {
      "at": {
       "type": "string",
       "format": "date-time"
      },
      "reason": {
       "type": "string"
      },
      "fromLevel": {
       "type": "integer"
      },
      "toLevel": {
       "type": "integer"
      },
      "wasAutomatic": {
       "type": "boolean"
      }
     }
    }
   },
   "resubmittedFromId": {
    "type": "string",
    "nullable": true
   },
   "reopenedFromId": {
    "type": "string",
    "nullable": true
   },
   "slaDueAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "slaBreached": {
    "type": "boolean"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "requestedAt": {
    "type": "string",
    "format": "date-time"
   },
   "completedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "aiAssessment": {
    "type": "object",
    "nullable": true,
    "readOnly": true,
    "description": "**AI context for the reviewer, never an input to the decision** (11.1.73 to 11.1.75; MoM 8 September; 29 September, build pass, group G2). Written by approvals from `ai.scoreApprovalRequest` on submit and on each SLA tick; null where AI is off or has not answered. Shown on the request labelled as AI; orders the inbox only when `sort=aiPriority` is asked for.",
    "properties": {
     "riskScore": {
      "type": "integer",
      "minimum": 0,
      "maximum": 100
     },
     "riskBand": {
      "type": "string",
      "enum": [
       "low",
       "medium",
       "high",
       "critical"
      ]
     },
     "priorityScore": {
      "type": "integer",
      "minimum": 0,
      "maximum": 100
     },
     "escalationSuggestion": {
      "type": "object",
      "description": "A suggestion a person may act on through `escalateApprovalRequest`, or the tenant's own SLA policy may; nothing escalates because of it.",
      "properties": {
       "action": {
        "type": "string",
        "enum": [
         "escalate",
         "addBackupApprover",
         "none"
        ]
       },
       "reason": {
        "type": "string",
        "nullable": true
       }
      }
     },
     "signals": {
      "type": "array",
      "maxItems": 10,
      "description": "The signals behind the scores, largest first, as `ai.AiApprovalRequestScore.signals`.",
      "items": {
       "type": "object",
       "properties": {
        "code": {
         "type": "string"
        },
        "contribution": {
         "type": "number"
        },
        "detail": {
         "type": "string",
         "nullable": true
        }
       }
      }
     },
     "scoreId": {
      "type": "string",
      "format": "uuid",
      "description": "The `ai.approval_request_score` row it was copied from; `ai.getApprovalRequestScore` gives the full context. Not a foreign key (the score lives in the AI service)."
     },
     "decisionRecordId": {
      "type": "string",
      "description": "The ai decision record, for the audit of what the AI said and why."
     },
     "assessedAt": {
      "type": "string",
      "format": "date-time"
     }
    }
   }
  }
 },
 "ApprovalStatus": {
  "type": "string",
  "enum": [
   "draft",
   "pending",
   "escalated",
   "returned",
   "informationRequested",
   "approved",
   "rejected",
   "withdrawn",
   "expired",
   "cancelled"
  ]
 },
 "AutomationExecutionAutonomousActionMonitorInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; updates approvals.automation status (schema Automation) (data model for the agreed operations, 29 September)",
  "description": "**What Automation Execution & Autonomous Action Monitor submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "command": {
    "type": "string",
    "enum": [
     "pause",
     "resume",
     "disable",
     "killSwitch"
    ],
    "description": "Control command"
   },
   "automationId": {
    "type": "string",
    "description": "Automation to control"
   },
   "reason": {
    "type": "string",
    "description": "Why the automation is being controlled"
   }
  },
  "required": [
   "automationId",
   "command"
  ]
 },
 "AutomationExecutionAutonomousActionMonitorView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over approvals.automation and approvals.automation_execution (data model for the agreed operations, 29 September)",
  "description": "**What Automation Execution & Autonomous Action Monitor displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "command": {
    "type": "string",
    "enum": [
     "pause",
     "resume",
     "disable",
     "killSwitch"
    ],
    "description": "Control command"
   },
   "automationId": {
    "type": "string",
    "description": "Automation to control"
   },
   "automatedActionsToday": {
    "type": "integer",
    "description": "Automated Actions Today"
   },
   "successful": {
    "type": "integer",
    "description": "Successful"
   },
   "failed": {
    "type": "integer",
    "description": "Failed"
   },
   "humanConfirmationRequired": {
    "type": "integer",
    "description": "Actions waiting for human confirmation"
   },
   "reversed": {
    "type": "integer",
    "description": "Reversed"
   },
   "suspended": {
    "type": "integer",
    "description": "Suspended"
   },
   "estimatedManualActionsAvoided": {
    "type": "integer",
    "description": "Estimated Manual Actions Avoided"
   },
   "estimatedTimeSaved": {
    "type": "integer",
    "description": "Minutes"
   },
   "automation": {
    "type": "string",
    "description": "Automation"
   },
   "businessObject": {
    "type": "string",
    "description": "Business Object"
   },
   "rule": {
    "type": "string",
    "description": "Rule"
   },
   "action": {
    "type": "string",
    "description": "Action"
   },
   "result": {
    "type": "string",
    "description": "Result"
   },
   "confidenceWhereAiAssisted": {
    "type": "number",
    "description": "Confidence of an AI-assisted non-approval action; never set for approve or reject"
   },
   "executionTime": {
    "type": "string",
    "format": "date-time",
    "description": "Execution Time"
   },
   "status": {
    "type": "string",
    "enum": [
     "active",
     "paused",
     "disabled",
     "killSwitched"
    ],
    "description": "Status"
   },
   "reason": {
    "type": "string",
    "description": "Why the automation is being controlled"
   }
  },
  "required": [
   "automationId",
   "command"
  ]
 },
 "CrossModuleOrchestrationMonitorView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over approvals.workflow_step_execution joined to approvals.workflow_instance by correlation id (data model for the agreed operations, 29 September)",
  "description": "**What Cross-Module Orchestration Monitor displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "service": {
    "type": "string",
    "description": "Service"
   },
   "action": {
    "type": "string",
    "description": "Action"
   },
   "status": {
    "type": "string",
    "enum": [
     "notStarted",
     "running",
     "waiting",
     "successful",
     "failed",
     "compensated"
    ],
    "description": "Status"
   },
   "started": {
    "type": "string",
    "format": "date-time",
    "description": "Started"
   },
   "completed": {
    "type": "string",
    "format": "date-time",
    "description": "Completed"
   },
   "duration": {
    "type": "integer",
    "description": "Seconds"
   },
   "inputOutput": {
    "type": "string",
    "description": "Input/Output"
   },
   "failureHandling": {
    "type": "string",
    "enum": [
     "waits",
     "retries",
     "rollsBack",
     "continuesPartially",
     "requiresHumanIntervention"
    ],
    "description": "What the workflow does after this node fails"
   },
   "retries": {
    "type": "integer",
    "description": "Retries"
   },
   "correlationId": {
    "type": "string",
    "description": "a common correlation/workflow ID"
   }
  },
  "required": [
   "correlationId",
   "service"
  ]
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
 "ProcessOptimizationAutomationOpportunityCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — aggregated from approvals.workflow_instance and workflow_step_execution per process (data model for the agreed operations, 29 September)",
  "description": "**What Process Optimization & Automation Opportunity Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "opportunityType": {
    "type": "string",
    "enum": [
     "repetitiveApproval",
     "unnecessaryApproval",
     "highManualWork",
     "excessiveRework",
     "longWaitingTime",
     "duplicateSteps",
     "highFailureRate",
     "lowRiskManualAction",
     "processBottleneck"
    ],
    "description": "Kind of improvement opportunity"
   },
   "process": {
    "type": "string",
    "description": "Process"
   },
   "module": {
    "type": "string",
    "description": "Module"
   },
   "monthlyVolume": {
    "type": "integer",
    "description": "Monthly Volume"
   },
   "currentSteps": {
    "type": "integer",
    "description": "Current Steps"
   },
   "averageDuration": {
    "type": "integer",
    "description": "Minutes"
   },
   "manualSteps": {
    "type": "integer",
    "description": "Manual Steps"
   },
   "approvalRate": {
    "type": "number",
    "description": "Approval Rate"
   },
   "exceptionRate": {
    "type": "number",
    "description": "Exception Rate"
   },
   "estimatedOpportunity": {
    "type": "string",
    "description": "Estimated Opportunity"
   }
  },
  "required": [
   "process"
  ]
 },
 "SlaEscalationBottleneckMonitorView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over approvals.workflow_instance, whose SLA and reminder timestamps it lists (data model for the agreed operations, 29 September)",
  "description": "**What SLA, Escalation & Bottleneck Monitor displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "workflow": {
    "type": "string",
    "description": "Workflow"
   },
   "instance": {
    "type": "string",
    "description": "Instance"
   },
   "currentStep": {
    "type": "string",
    "description": "Current Step"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   },
   "started": {
    "type": "string",
    "format": "date-time",
    "description": "Started"
   },
   "target": {
    "type": "string",
    "format": "date-time",
    "description": "SLA deadline"
   },
   "timeRemaining": {
    "type": "integer",
    "description": "Minutes until breach; negative once breached"
   },
   "risk": {
    "type": "string",
    "description": "Risk"
   },
   "escalationLevel": {
    "type": "string",
    "description": "Escalation Level"
   },
   "firstReminder": {
    "type": "string",
    "format": "date-time",
    "description": "First Reminder"
   },
   "secondReminder": {
    "type": "string",
    "format": "date-time",
    "description": "Second Reminder"
   },
   "managerEscalation": {
    "type": "string",
    "format": "date-time",
    "description": "Manager Escalation"
   },
   "executiveEscalation": {
    "type": "string",
    "format": "date-time",
    "description": "Executive Escalation"
   },
   "finalOutcome": {
    "type": "string",
    "description": "Final Outcome"
   }
  },
  "required": [
   "instance"
  ]
 },
 "SlaEscalationBottleneckMonitorViewSummary": {
  "type": "object",
  "x-ticvai-persistence": "none - aggregate computed at read time over the rows the page lists",
  "description": "The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September, readiness close-out).",
  "properties": {
   "withinSla": {
    "type": "integer",
    "description": "Within SLA"
   },
   "atRisk": {
    "type": "integer",
    "description": "At Risk"
   },
   "breached": {
    "type": "integer",
    "description": "Breached"
   },
   "escalated": {
    "type": "integer",
    "description": "Escalated"
   },
   "averageProcessingTime": {
    "type": "integer",
    "description": "Minutes"
   },
   "averageApprovalTime": {
    "type": "integer",
    "description": "Minutes"
   },
   "longestWaitingStep": {
    "type": "string",
    "description": "Longest Waiting Step"
   }
  }
 },
 "SuggestionBasis": {
  "type": "string",
  "description": "**How the answer was reached, and this is the field the whole design exists for.**\nA venue must be able to see that today's price suggestion is a margin rule and next quarter's is a trained model — **the same operation, the same screen, a different basis** — and a screen that cannot say which is a screen that asks a manager to trust arithmetic it will not show.\n**Swapping a heuristic for a model is a provider change, not a contract change.** That is the point of the abstraction: the frontend, the audit record and the outcome capture all stay exactly as they are.\n",
  "enum": [
   "heuristic",
   "statistical",
   "model",
   "hybrid",
   "manual"
  ]
 },
 "WorkflowAnalyticsProcessPerformanceView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — aggregated from approvals.workflow_instance, workflow_step_execution, automation_execution, request, decision and escalation (data model for the agreed operations, 29 September)",
  "description": "**What Workflow Analytics & Process Performance displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "workflowVolume": {
    "type": "integer",
    "description": "Workflow Volume"
   },
   "completionRate": {
    "type": "number",
    "description": "Completion Rate"
   },
   "failureRate": {
    "type": "number",
    "description": "Failure Rate"
   },
   "averageCompletionTime": {
    "type": "integer",
    "description": "Minutes"
   },
   "approvalTime": {
    "type": "integer",
    "description": "Minutes"
   },
   "automationRate": {
    "type": "number",
    "description": "Automation Rate"
   },
   "escalationRate": {
    "type": "number",
    "description": "Escalation Rate"
   },
   "rejectionRate": {
    "type": "number",
    "description": "Rejection Rate"
   },
   "reworkRate": {
    "type": "number",
    "description": "Rework Rate"
   },
   "slaCompliance": {
    "type": "number",
    "description": "Percent within SLA"
   },
   "averageApprovalTime": {
    "type": "integer",
    "description": "Minutes"
   },
   "approvalRate": {
    "type": "number",
    "description": "Approval Rate"
   },
   "requestChangesRate": {
    "type": "number",
    "description": "Request Changes Rate"
   },
   "delegationRate": {
    "type": "number",
    "description": "Delegation Rate"
   },
   "manualStepsRemoved": {
    "type": "integer",
    "description": "Manual Steps Removed"
   },
   "processingTimeSaved": {
    "type": "integer",
    "description": "Minutes"
   },
   "workloadReduced": {
    "type": "number",
    "description": "Staff hours"
   },
   "costSavingWhereMeasurable": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Cost Saving where measurable"
   }
  }
 },
 "WorkflowExceptionFailureRecoveryCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over approvals.workflow_exception (schema WorkflowException) (data model for the agreed operations, 29 September)",
  "description": "**What Workflow Exception, Failure & Recovery Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "errorType": {
    "type": "string",
    "enum": [
     "businessRuleFailure",
     "missingData",
     "missingApprover",
     "permissionFailure",
     "integrationFailure",
     "timeout",
     "actionFailure",
     "invalidState",
     "duplicateEvent",
     "serviceUnavailable",
     "configurationError"
    ],
    "description": "Kind of failure"
   },
   "exceptionId": {
    "type": "string",
    "description": "Exception ID"
   },
   "workflow": {
    "type": "string",
    "description": "Workflow"
   },
   "instance": {
    "type": "string",
    "description": "Instance"
   },
   "module": {
    "type": "string",
    "description": "Module"
   },
   "failedStep": {
    "type": "string",
    "description": "Step that failed"
   },
   "time": {
    "type": "string",
    "format": "date-time",
    "description": "Time"
   },
   "businessImpact": {
    "type": "string",
    "description": "Business Impact"
   },
   "priority": {
    "type": "string",
    "description": "Priority"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   },
   "retryCount": {
    "type": "integer",
    "description": "Retry count"
   }
  },
  "required": [
   "exceptionId"
  ]
 },
 "WorkflowInstance": {
  "type": "object",
  "x-ticvai-persistence": "approvals.workflow_instance",
  "description": "**One running workflow** (pack 13.2.1, 13.2.3 and 13.2.5; data model for the agreed operations, 29 September). Started by a `WorkflowTrigger`, on the version in force at that moment and kept on it to the end (audit R129). Its steps are `WorkflowStepExecution` rows, keyed by the same `correlationId` the participating services trace with. **The SLA clock and its reminder and escalation timestamps are held here**, not in a table of their own: there is one clock per instance, and the SLA, Escalation & Bottleneck Monitor lists instances. Lifecycle in `states/workflow-instance.yaml`. The engine writes this row; an operator changes it only through `actOnWorkflowInstance`, which keeps each change as a `WorkflowIntervention` (decided 29 September, writers pass).",
  "required": [
   "id",
   "workflowDefinitionId",
   "workflowVersionId",
   "sourceModule",
   "status",
   "correlationId",
   "startedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "workflowDefinitionId": {
    "type": "string",
    "format": "uuid"
   },
   "workflowVersionId": {
    "type": "string",
    "format": "uuid",
    "description": "The version the instance started on; never changes"
   },
   "workflowTriggerId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "sourceModule": {
    "$ref": "#/components/schemas/WorkflowModule"
   },
   "businessObjectType": {
    "type": "string",
    "maxLength": 100,
    "nullable": true
   },
   "businessObjectId": {
    "type": "string",
    "nullable": true,
    "description": "**A reference, never a copy**, as `ApprovalRequest.subjectId`"
   },
   "initiatedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Null when a system event or schedule started it"
   },
   "ownerPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "priority": {
    "type": "string",
    "maxLength": 30,
    "nullable": true
   },
   "currentNodeId": {
    "type": "string",
    "nullable": true,
    "description": "The node of the version's graph the instance is at"
   },
   "status": {
    "$ref": "#/components/schemas/WorkflowInstanceStatus"
   },
   "correlationId": {
    "type": "string",
    "maxLength": 100,
    "description": "The shared correlation id every participating service logs, for distributed tracing"
   },
   "slaPolicyId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The `ApprovalSlaPolicy` whose clock runs on this instance"
   },
   "slaDueAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "slaBreached": {
    "type": "boolean",
    "default": false
   },
   "escalationLevel": {
    "type": "integer",
    "minimum": 0,
    "default": 0
   },
   "firstReminderAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "secondReminderAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "managerEscalatedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "executiveEscalatedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "slaOutcome": {
    "type": "string",
    "enum": [
     "metWithinTarget",
     "metAfterReminder",
     "metAfterEscalation",
     "breached"
    ],
    "nullable": true,
    "description": "How the instance finished against its SLA; set on completion (the monitor's Final Outcome)"
   },
   "startedAt": {
    "type": "string",
    "format": "date-time"
   },
   "completedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "scopePath": {
    "type": "string",
    "description": "The partition key (ADR-0005). Written at venue scope"
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "WorkflowInstanceActionInput": {
  "type": "object",
  "x-ticvai-persistence": "none — request only; writes approvals.workflow_intervention (schema WorkflowIntervention) (decided 29 September, writers pass)",
  "description": "One operator action on a running workflow instance (decided 29 September, writers pass).",
  "required": [
   "action",
   "reason"
  ],
  "properties": {
   "action": {
    "$ref": "#/components/schemas/WorkflowInterventionAction"
   },
   "reason": {
    "type": "string",
    "minLength": 1,
    "maxLength": 500,
    "description": "Mandatory for every action (pack 13.2.5, \"actions capture a mandatory reason\")"
   },
   "workflowStepExecutionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The step acted on; for `retryStep` the step to retry from. Defaults to the instance's current step"
   },
   "workflowExceptionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The exception the action is taken from; required for `escalateException`"
   },
   "assigneePrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Required for `reassign`, `addBackupApprover` and `escalateException`"
   },
   "alternativeNodeId": {
    "type": "string",
    "nullable": true,
    "description": "For `skipStep`, the node to continue at instead of the next one (Use Approved Alternative)"
   },
   "correctedInput": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true,
    "description": "For `resume`, the corrected input of the failed step (Correct Data)"
   },
   "extendByMinutes": {
    "type": "integer",
    "minimum": 1,
    "maximum": 43200,
    "nullable": true,
    "description": "Required for `extendSla`"
   },
   "priority": {
    "type": "string",
    "maxLength": 30,
    "nullable": true,
    "description": "Required for `changePriority`"
   }
  }
 },
 "WorkflowInstanceMonitorProcessTimelineView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over approvals.workflow_instance and approvals.workflow_step_execution (data model for the agreed operations, 29 September)",
  "description": "**What Workflow Instance Monitor & Process Timeline displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "workflowInstance": {
    "type": "string",
    "description": "Workflow Instance"
   },
   "workflowName": {
    "type": "string",
    "description": "Workflow Name"
   },
   "version": {
    "type": "string",
    "description": "Version"
   },
   "sourceModule": {
    "type": "string",
    "description": "Source Module"
   },
   "businessObject": {
    "type": "string",
    "description": "Business Object"
   },
   "initiatedBy": {
    "type": "string",
    "description": "Initiated By"
   },
   "startTime": {
    "type": "string",
    "format": "date-time",
    "description": "Start Time"
   },
   "currentStatus": {
    "type": "string",
    "enum": [
     "running",
     "waitingApproval",
     "waitingTask",
     "waitingSystem",
     "escalated",
     "failed",
     "completed",
     "cancelled"
    ],
    "description": "Current Status"
   },
   "currentStep": {
    "type": "string",
    "description": "Current Step"
   },
   "sla": {
    "type": "string",
    "description": "SLA"
   },
   "step": {
    "type": "string",
    "description": "Step"
   },
   "type": {
    "type": "string",
    "description": "Type"
   },
   "started": {
    "type": "string",
    "format": "date-time",
    "description": "Started"
   },
   "completed": {
    "type": "string",
    "format": "date-time",
    "description": "Completed"
   },
   "assignedTo": {
    "type": "string",
    "description": "Assigned To"
   },
   "input": {
    "type": "string",
    "description": "Input"
   },
   "output": {
    "type": "string",
    "description": "Output"
   },
   "decision": {
    "type": "string",
    "description": "Decision"
   },
   "duration": {
    "type": "integer",
    "description": "Seconds"
   },
   "status": {
    "type": "string",
    "description": "Status"
   },
   "ruleEvaluations": {
    "type": "integer",
    "description": "Rule evaluations"
   },
   "assignments": {
    "type": "integer",
    "description": "Assignments"
   },
   "approvals": {
    "type": "integer",
    "description": "Approvals"
   },
   "rejections": {
    "type": "integer",
    "description": "Rejections"
   },
   "escalations": {
    "type": "integer",
    "description": "Escalations"
   },
   "notifications": {
    "type": "integer",
    "description": "Notifications"
   },
   "apiCalls": {
    "type": "integer",
    "description": "API calls"
   },
   "systemActions": {
    "type": "integer",
    "description": "System actions"
   },
   "errors": {
    "type": "integer",
    "description": "Errors"
   }
  },
  "required": [
   "workflowInstance"
  ]
 },
 "WorkflowInstanceStatus": {
  "type": "string",
  "description": "Where one running workflow stands (pack 13.2.1 and 13.2.3; decided 29 September, readiness close-out). Modelled in `states/workflow-instance.yaml`.",
  "enum": [
   "running",
   "waitingApproval",
   "waitingTask",
   "waitingSystem",
   "escalated",
   "failed",
   "completed",
   "cancelled"
  ]
 },
 "WorkflowInterventionAction": {
  "type": "string",
  "description": "What an operator did to a running workflow instance (pack 13.2.3, 13.2.4 and 13.2.5; decided 29 September, writers pass). The effect of each is on `actOnWorkflowInstance`.",
  "enum": [
   "reassign",
   "retryStep",
   "skipStep",
   "resume",
   "cancel",
   "extendSla",
   "addBackupApprover",
   "changePriority",
   "escalateException"
  ]
 },
 "WorkflowModule": {
  "type": "string",
  "description": "The module a workflow, rule or automation belongs to and a workflow instance originates from. The same values as `WorkflowOperationsCommandCenterView.module` (decided 29 September, readiness close-out), named so the workflow engine's tables share one vocabulary (data model for the agreed operations, 29 September).",
  "enum": [
   "ticketing",
   "pricing",
   "finance",
   "procurement",
   "crm",
   "resourceManagement",
   "fnb",
   "retail",
   "groupSales",
   "customerService",
   "membership",
   "wallet",
   "waiver",
   "subscriptionLicensing"
  ]
 },
 "WorkflowOperationsCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over approvals.workflow_instance (schema WorkflowInstance) (data model for the agreed operations, 29 September)",
  "description": "**What Workflow Operations Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "workflowInstanceId": {
    "type": "string",
    "description": "Workflow Instance ID"
   },
   "workflow": {
    "type": "string",
    "description": "Workflow"
   },
   "module": {
    "type": "string",
    "enum": [
     "ticketing",
     "pricing",
     "finance",
     "procurement",
     "crm",
     "resourceManagement",
     "fnb",
     "retail",
     "groupSales",
     "customerService",
     "membership",
     "wallet",
     "waiver",
     "subscriptionLicensing"
    ],
    "description": "Module the workflow originates from"
   },
   "businessObject": {
    "type": "string",
    "description": "Business Object"
   },
   "initiatedBy": {
    "type": "string",
    "description": "Initiated By"
   },
   "started": {
    "type": "string",
    "format": "date-time",
    "description": "Started"
   },
   "currentStep": {
    "type": "string",
    "description": "Current Step"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   },
   "priority": {
    "type": "string",
    "description": "Priority"
   },
   "sla": {
    "type": "string",
    "description": "SLA"
   },
   "status": {
    "type": "string",
    "enum": [
     "running",
     "waitingApproval",
     "waitingTask",
     "waitingSystem",
     "escalated",
     "failed",
     "completed",
     "cancelled"
    ],
    "description": "Status"
   }
  },
  "required": [
   "workflowInstanceId"
  ]
 },
 "WorkflowOperationsCommandCenterViewSummary": {
  "type": "object",
  "x-ticvai-persistence": "none - aggregate computed at read time over the rows the page lists",
  "description": "The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September, readiness close-out).",
  "properties": {
   "workflowsRunning": {
    "type": "integer",
    "description": "Workflows Running"
   },
   "startedToday": {
    "type": "integer",
    "description": "Started Today"
   },
   "completedToday": {
    "type": "integer",
    "description": "Completed Today"
   },
   "pendingApprovals": {
    "type": "integer",
    "description": "Pending Approvals"
   },
   "waitingTasks": {
    "type": "integer",
    "description": "Waiting Tasks"
   },
   "slaAtRisk": {
    "type": "integer",
    "description": "SLA At Risk"
   },
   "slaBreached": {
    "type": "integer",
    "description": "SLA Breached"
   },
   "failedWorkflows": {
    "type": "integer",
    "description": "Failed Workflows"
   },
   "escalated": {
    "type": "integer",
    "description": "Escalated"
   },
   "automatedExecutions": {
    "type": "integer",
    "description": "Automated Executions"
   },
   "averageCompletionTime": {
    "type": "integer",
    "description": "Minutes"
   },
   "automationSuccessRate": {
    "type": "number",
    "description": "Automation Success Rate"
   }
  }
 }
}
```
