# WS56 — Rules  Workflow  Approval   Automation Engine board 2

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
  `APPROVAL_REQUEST, APPROVAL_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **0 of these operations work offline**
  
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-248` | Workflow Operations Command Center | listDetail | 1 | 0 | — |
| `ADM-249` | Unified Approval Inbox & Decision Workspace | listDetail | 1 | 0 | — |
| `ADM-250` | Workflow Instance Monitor & Process Timeline | commandCentre | 1 | 0 | — |
| `ADM-251` | Workflow Exception, Failure & Recovery Center | listDetail | 1 | 1 | — |
| `ADM-252` | SLA, Escalation & Bottleneck Monitor | listDetail | 1 | 0 | — |
| `ADM-253` | Automation Execution & Autonomous Action Monitor | listDetail | 1 | 0 | — |
| `ADM-254` | Cross-Module Orchestration Monitor | listDetail | 1 | 0 | — |
| `ADM-255` | Workflow Analytics & Process Performance | commandCentre | 1 | 0 | — |
| `ADM-256` | Process Optimization & Automation Opportunity Center | listDetail | 1 | 0 | — |
| `ADM-257` | AI Workflow Intelligence & Autonomous Governance Center | listDetail | 1 | 0 | — |

## Thin screens in this batch

**ADM-248, ADM-249, ADM-252, ADM-253, ADM-254, ADM-256, ADM-257 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

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
     "carries": [
      "tenantId"
     ],
     "provenance": "derived — ADM-002 declares entryState.params tenantId, so an edge into it must carry them"
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
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide administrators and operational managers with a real-time view of all workflow activity across TICVAI.",
  "purposeNote": "Authorized users can understand the real-time state and health of workflow execution across the entire TICVAI platform.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every workflow operations",
       "columns": [
        "WorkflowOperationsCommandCenterView.workflowsRunning",
        "WorkflowOperationsCommandCenterView.startedToday",
        "WorkflowOperationsCommandCenterView.completedToday",
        "WorkflowOperationsCommandCenterView.pendingApprovals",
        "WorkflowOperationsCommandCenterView.waitingTasks",
        "WorkflowOperationsCommandCenterView.slaAtRisk",
        "WorkflowOperationsCommandCenterView.slaBreached",
        "WorkflowOperationsCommandCenterView.failedWorkflows",
        "WorkflowOperationsCommandCenterView.escalated",
        "WorkflowOperationsCommandCenterView.automatedExecutions",
        "WorkflowOperationsCommandCenterView.averageCompletionTime",
        "WorkflowOperationsCommandCenterView.automationSuccessRate",
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
        "WorkflowOperationsCommandCenterView.workflowsRunning",
        "WorkflowOperationsCommandCenterView.startedToday",
        "WorkflowOperationsCommandCenterView.completedToday",
        "WorkflowOperationsCommandCenterView.pendingApprovals",
        "WorkflowOperationsCommandCenterView.waitingTasks",
        "WorkflowOperationsCommandCenterView.slaAtRisk",
        "WorkflowOperationsCommandCenterView.slaBreached",
        "WorkflowOperationsCommandCenterView.failedWorkflows",
        "WorkflowOperationsCommandCenterView.escalated",
        "WorkflowOperationsCommandCenterView.automatedExecutions",
        "WorkflowOperationsCommandCenterView.averageCompletionTime",
        "WorkflowOperationsCommandCenterView.automationSuccessRate",
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
    "WorkflowOperationsCommandCenterView.workflowsRunning",
    "WorkflowOperationsCommandCenterView.startedToday",
    "WorkflowOperationsCommandCenterView.completedToday",
    "WorkflowOperationsCommandCenterView.pendingApprovals",
    "WorkflowOperationsCommandCenterView.waitingTasks",
    "WorkflowOperationsCommandCenterView.slaAtRisk"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-248"
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
     "provenance": "flow F165 step 2→3",
     "operation": "approveUnifiedDecision"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide users with one approval inbox across all TICVAI modules. This is extremely important. A manager should not need to open Finance for one approval, Pricing for another, Procurement for another, and Customer Service for another.",
  "purposeNote": "Authorized approvers can review and action approval requests from all TICVAI modules through one governed inbox.",
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
        "UnifiedApprovalInboxDecisionWorkspaceView.approvalId",
        "UnifiedApprovalInboxDecisionWorkspaceView.requestType",
        "UnifiedApprovalInboxDecisionWorkspaceView.sourceModule",
        "UnifiedApprovalInboxDecisionWorkspaceView.requester",
        "UnifiedApprovalInboxDecisionWorkspaceView.amountImpact",
        "UnifiedApprovalInboxDecisionWorkspaceView.priority",
        "UnifiedApprovalInboxDecisionWorkspaceView.submitted",
        "UnifiedApprovalInboxDecisionWorkspaceView.slaRemaining",
        "UnifiedApprovalInboxDecisionWorkspaceView.approvalLevel",
        "UnifiedApprovalInboxDecisionWorkspaceView.status"
       ],
       "bindsTo": "UnifiedApprovalInboxDecisionWorkspaceView",
       "operation": "approveUnifiedDecision",
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
       "bindsTo": "UnifiedApprovalInboxDecisionWorkspaceView",
       "columns": [
        "UnifiedApprovalInboxDecisionWorkspaceView.approvalId",
        "UnifiedApprovalInboxDecisionWorkspaceView.requestType",
        "UnifiedApprovalInboxDecisionWorkspaceView.sourceModule",
        "UnifiedApprovalInboxDecisionWorkspaceView.requester",
        "UnifiedApprovalInboxDecisionWorkspaceView.amountImpact",
        "UnifiedApprovalInboxDecisionWorkspaceView.priority",
        "UnifiedApprovalInboxDecisionWorkspaceView.submitted",
        "UnifiedApprovalInboxDecisionWorkspaceView.slaRemaining",
        "UnifiedApprovalInboxDecisionWorkspaceView.approvalLevel",
        "UnifiedApprovalInboxDecisionWorkspaceView.status"
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
       "provenance": "contract operation approveUnifiedDecision"
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
    "operationId": "approveUnifiedDecision",
    "contract": "approvals",
    "purpose": "Unified Approval Inbox & Decision Workspace",
    "trigger": "onAction",
    "invalidates": [
     "approveUnifiedDecision"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "UnifiedApprovalInboxDecisionWorkspaceView.approvalId",
    "UnifiedApprovalInboxDecisionWorkspaceView.requestType",
    "UnifiedApprovalInboxDecisionWorkspaceView.sourceModule",
    "UnifiedApprovalInboxDecisionWorkspaceView.requester",
    "UnifiedApprovalInboxDecisionWorkspaceView.amountImpact",
    "UnifiedApprovalInboxDecisionWorkspaceView.priority"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-249"
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
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Display) and a per-row directory (§For each step show) — counts over a population, then the population",
  "purpose": "Allow administrators to inspect exactly what is happening inside an individual running workflow.",
  "purposeNote": "Administrators can reconstruct exactly how a workflow reached its current state and why every major decision or action occurred.",
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
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-250"
  },
  "apisNote": "Regenerated 9 September 2026 from Rules__Workflow__Approval___Automation_Engine_Reference.pdf page 27. 20 of 20 labels bound to a contract property; 27 of 52 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide one controlled workspace for failed workflow executions.",
  "purposeNote": "Failed workflows can be identified, investigated, recovered or safely compensated without losing business context or audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 8 actions on this screen and the screen declares 1 operation.** Unserved: Business Rule Failure, Duplicate Event, Configuration Error, Retry, Retry From Step, Resume, Cancel, Escalate. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
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
       "label": "Duplicate Event",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 28 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Configuration Error",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 28 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Retry",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 28 §Allow"
      },
      {
       "kind": "secondaryButton",
       "label": "Retry From Step",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 28 §Allow"
      },
      {
       "kind": "secondaryButton",
       "label": "Resume",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 28 §Allow"
      },
      {
       "kind": "destructiveButton",
       "label": "Cancel",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 28 §Allow"
      },
      {
       "kind": "secondaryButton",
       "label": "Escalate",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 28 §Allow"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmCancel",
    "component": "confirmDialog",
    "trigger": "Cancel",
    "body": "**Cancel on a workflow exception failure is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.",
    "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 28 §Allow"
   }
  ],
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
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-251"
  },
  "apisNote": "Regenerated 9 September 2026 from Rules__Workflow__Approval___Automation_Engine_Reference.pdf page 28. 10 of 11 labels bound to a contract property; 19 of 46 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display; Show) and no metric row",
  "purpose": "Monitor workflows approaching or exceeding configured time limits.",
  "purposeNote": "Management can identify and resolve workflow bottlenecks before they materially impact business operations.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every sla escalation bottleneck",
       "columns": [
        "SlaEscalationBottleneckMonitorView.withinSla",
        "SlaEscalationBottleneckMonitorView.atRisk",
        "SlaEscalationBottleneckMonitorView.breached",
        "SlaEscalationBottleneckMonitorView.escalated",
        "SlaEscalationBottleneckMonitorView.averageProcessingTime",
        "SlaEscalationBottleneckMonitorView.averageApprovalTime",
        "SlaEscalationBottleneckMonitorView.longestWaitingStep",
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
        "SlaEscalationBottleneckMonitorView.withinSla",
        "SlaEscalationBottleneckMonitorView.atRisk",
        "SlaEscalationBottleneckMonitorView.breached",
        "SlaEscalationBottleneckMonitorView.escalated",
        "SlaEscalationBottleneckMonitorView.averageProcessingTime",
        "SlaEscalationBottleneckMonitorView.averageApprovalTime",
        "SlaEscalationBottleneckMonitorView.longestWaitingStep",
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
   }
  ],
  "entryState": {
   "preloaded": [
    "SlaEscalationBottleneckMonitorView.withinSla",
    "SlaEscalationBottleneckMonitorView.atRisk",
    "SlaEscalationBottleneckMonitorView.breached",
    "SlaEscalationBottleneckMonitorView.escalated",
    "SlaEscalationBottleneckMonitorView.averageProcessingTime",
    "SlaEscalationBottleneckMonitorView.averageApprovalTime"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-252"
  },
  "apisNote": "Regenerated 9 September 2026 from Rules__Workflow__Approval___Automation_Engine_Reference.pdf page 30. 21 of 21 labels bound to a contract property; 26 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Display) and no metric row",
  "purpose": "Provide visibility and governance over actions executed automatically by TICVAI. This becomes especially important as TICVAI becomes more AI-driven.",
  "purposeNote": "immediate suspension where required.",
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
    "trigger": "onAction",
    "invalidates": [
     "createAutomationAutonomouAction"
    ]
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-253"
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
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Monitor complex workflows involving multiple TICVAI services. Example — Group Booking Confirmation",
  "purposeNote": "Complex cross-module business processes can be monitored as one business workflow rather than requiring administrators to inspect individual microservices independently.",
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
    "CrossModuleOrchestrationMonitorView.bookingConfirmed",
    "CrossModuleOrchestrationMonitorView.reserve420Tickets",
    "CrossModuleOrchestrationMonitorView.reserve4Guides",
    "CrossModuleOrchestrationMonitorView.reserve420Meals",
    "CrossModuleOrchestrationMonitorView.service"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-254"
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
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen a metric directory (§Analyze; Measure; Compare) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's",
  "purpose": "Measure how effectively TICVAI's business workflows are performing.",
  "purposeNote": "Management can quantitatively evaluate whether workflows and automation are improving operational efficiency.",
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
      },
      {
       "kind": "metricTile",
       "label": "Workflow v1.4 vs v1.5",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 34 §Compare",
       "bindsTo": "WorkflowAnalyticsProcessPerformanceView.workflowV14VsV15"
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-255"
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
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Identify; Display) and no metric row",
  "purpose": "Identify business processes that should be simplified, redesigned or automated. This is where TICVAI moves beyond simply running workflows.",
  "purposeNote": "operational evidence rather than assumptions.",
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
        "ProcessOptimizationAutomationOpportunityCenterView.repetitiveApproval",
        "ProcessOptimizationAutomationOpportunityCenterView.unnecessaryApproval",
        "ProcessOptimizationAutomationOpportunityCenterView.highManualWork",
        "ProcessOptimizationAutomationOpportunityCenterView.excessiveRework",
        "ProcessOptimizationAutomationOpportunityCenterView.longWaitingTime",
        "Duplicate Steps",
        "ProcessOptimizationAutomationOpportunityCenterView.highFailureRate",
        "ProcessOptimizationAutomationOpportunityCenterView.lowRiskManualAction",
        "ProcessOptimizationAutomationOpportunityCenterView.processBottleneck",
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
        "ProcessOptimizationAutomationOpportunityCenterView.repetitiveApproval",
        "ProcessOptimizationAutomationOpportunityCenterView.unnecessaryApproval",
        "ProcessOptimizationAutomationOpportunityCenterView.highManualWork",
        "ProcessOptimizationAutomationOpportunityCenterView.excessiveRework",
        "ProcessOptimizationAutomationOpportunityCenterView.longWaitingTime",
        "Duplicate Steps",
        "ProcessOptimizationAutomationOpportunityCenterView.highFailureRate",
        "ProcessOptimizationAutomationOpportunityCenterView.lowRiskManualAction",
        "ProcessOptimizationAutomationOpportunityCenterView.processBottleneck",
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
    "ProcessOptimizationAutomationOpportunityCenterView.repetitiveApproval",
    "ProcessOptimizationAutomationOpportunityCenterView.unnecessaryApproval",
    "ProcessOptimizationAutomationOpportunityCenterView.highManualWork",
    "ProcessOptimizationAutomationOpportunityCenterView.excessiveRework",
    "ProcessOptimizationAutomationOpportunityCenterView.longWaitingTime",
    "Duplicate Steps"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-256"
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
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Analyze) and no metric row",
  "purpose": "Create the AI intelligence layer across TICVAI's entire rules, workflow and automation ecosystem. This is the management-level AI brain for Area 13.",
  "purposeNote": "explainability, human governance, version control and immediate operational control. Board 2 — Final Screen Register",
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
       "columns": [
        "AiWorkflowIntelligenceAutonomousGovernanceCenterView.rules",
        "AiWorkflowIntelligenceAutonomousGovernanceCenterView.workflows",
        "AiWorkflowIntelligenceAutonomousGovernanceCenterView.approvals",
        "AiWorkflowIntelligenceAutonomousGovernanceCenterView.executionHistory",
        "AiWorkflowIntelligenceAutonomousGovernanceCenterView.sla",
        "AiWorkflowIntelligenceAutonomousGovernanceCenterView.exceptions",
        "AiWorkflowIntelligenceAutonomousGovernanceCenterView.automation",
        "AiWorkflowIntelligenceAutonomousGovernanceCenterView.processPerformance",
        "AiWorkflowIntelligenceAutonomousGovernanceCenterView.approverBehavior",
        "AiWorkflowIntelligenceAutonomousGovernanceCenterView.moduleActivity",
        "AiWorkflowIntelligenceAutonomousGovernanceCenterView.businessOutcomes"
       ],
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
       "columns": [
        "AiWorkflowIntelligenceAutonomousGovernanceCenterView.rules",
        "AiWorkflowIntelligenceAutonomousGovernanceCenterView.workflows",
        "AiWorkflowIntelligenceAutonomousGovernanceCenterView.approvals",
        "AiWorkflowIntelligenceAutonomousGovernanceCenterView.executionHistory",
        "AiWorkflowIntelligenceAutonomousGovernanceCenterView.sla",
        "AiWorkflowIntelligenceAutonomousGovernanceCenterView.exceptions",
        "AiWorkflowIntelligenceAutonomousGovernanceCenterView.automation",
        "AiWorkflowIntelligenceAutonomousGovernanceCenterView.processPerformance",
        "AiWorkflowIntelligenceAutonomousGovernanceCenterView.approverBehavior",
        "AiWorkflowIntelligenceAutonomousGovernanceCenterView.moduleActivity",
        "AiWorkflowIntelligenceAutonomousGovernanceCenterView.businessOutcomes"
       ],
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
   "preloaded": [
    "AiWorkflowIntelligenceAutonomousGovernanceCenterView.rules",
    "AiWorkflowIntelligenceAutonomousGovernanceCenterView.workflows",
    "AiWorkflowIntelligenceAutonomousGovernanceCenterView.approvals",
    "AiWorkflowIntelligenceAutonomousGovernanceCenterView.executionHistory",
    "AiWorkflowIntelligenceAutonomousGovernanceCenterView.sla",
    "AiWorkflowIntelligenceAutonomousGovernanceCenterView.exceptions"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-257"
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
 "approveUnifiedDecision": {
  "method": "PUT",
  "path": "/unified-decision",
  "contract": "approvals",
  "summary": "Unified Approval Inbox & Decision Workspace",
  "permission": "APPROVAL_REQUEST",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "UnifiedApprovalInboxDecisionWorkspaceInput",
  "responds": "UnifiedApprovalInboxDecisionWorkspaceView"
 },
 "createAutomationAutonomouAction": {
  "method": "POST",
  "path": "/automation-autonomou-action",
  "contract": "approvals",
  "summary": "Automation Execution & Autonomous Action Monitor",
  "permission": "APPROVAL_REQUEST",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "AutomationExecutionAutonomousActionMonitorInput",
  "responds": "AutomationExecutionAutonomousActionMonitorView"
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
  "parameters": [],
  "requestBody": null,
  "responds": "CrossModuleOrchestrationMonitorView"
 },
 "listProcessAutomationOpportunity": {
  "method": "GET",
  "path": "/process-automation-opportunity",
  "contract": "approvals",
  "summary": "Process Optimization & Automation Opportunity Center",
  "permission": "APPROVAL_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ProcessOptimizationAutomationOpportunityCenterView"
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
  "parameters": [],
  "requestBody": null,
  "responds": "SlaEscalationBottleneckMonitorView"
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
  "parameters": [],
  "requestBody": null,
  "responds": "WorkflowOperationsCommandCenterView"
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
  "parameters": [],
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
  "parameters": [],
  "requestBody": null,
  "responds": "WorkflowExceptionFailureRecoveryCenterView"
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
  "parameters": [],
  "requestBody": null,
  "responds": "WorkflowInstanceMonitorProcessTimelineView"
 },
 "listWorkflowProcessPerformance": {
  "method": "GET",
  "path": "/workflow-process-performance",
  "contract": "approvals",
  "summary": "Workflow Analytics & Process Performance",
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
 "AiWorkflowIntelligenceAutonomousGovernanceCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over approvals state, assembled at read time from tables that already exist",
  "description": "**What AI Workflow Intelligence & Autonomous Governance Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "rules": {
    "type": "string",
    "description": "Rules"
   },
   "workflows": {
    "type": "string",
    "description": "Workflows"
   },
   "approvals": {
    "type": "string",
    "description": "Approvals"
   },
   "executionHistory": {
    "type": "string",
    "description": "Execution History"
   },
   "sla": {
    "type": "string",
    "description": "SLA"
   },
   "exceptions": {
    "type": "string",
    "description": "Exceptions"
   },
   "automation": {
    "type": "string",
    "description": "Automation"
   },
   "processPerformance": {
    "type": "string",
    "description": "Process Performance"
   },
   "approverBehavior": {
    "type": "string",
    "description": "Approver Behavior"
   },
   "moduleActivity": {
    "type": "string",
    "description": "Module Activity"
   },
   "businessOutcomes": {
    "type": "string",
    "description": "Business Outcomes"
   },
   "clarificationExecute": {
    "type": "string",
    "description": "Clarification → Execute"
   },
   "aiIdentifiesExcessiveRework": {
    "type": "string",
    "description": "AI identifies excessive rework"
   },
   "by34Hours": {
    "type": "string",
    "description": "by 3.4 hours"
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
    "description": "Autonomy Level"
   },
   "decisionScope": {
    "type": "string",
    "description": "Decision Scope"
   },
   "confidenceThreshold": {
    "type": "integer",
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
   "humanSystemDecisionFinalAction": {
    "type": "string",
    "description": "Human/System Decision → Final Action"
   },
   "crossModuleOrchestrationMonitorMultiModuleExecution": {
    "type": "string",
    "description": "Cross-Module Orchestration Monitor Multi-module execution"
   },
   "area13CompleteArchitecture": {
    "type": "string",
    "description": "Area 13 — Complete Architecture"
   },
   "employeeApp": {
    "type": "string",
    "description": "Employee App"
   }
  }
 },
 "AutomationExecutionAutonomousActionMonitorInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Automation Execution & Autonomous Action Monitor submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "triggerT24Hours": {
    "type": "string",
    "description": "Trigger: T−24 hours"
   },
   "participantsEvaluated842": {
    "type": "string",
    "description": "Participants evaluated: 842"
   },
   "incomplete118": {
    "type": "string",
    "description": "Incomplete: 118"
   },
   "messagesTriggered118": {
    "type": "string",
    "description": "Messages triggered: 118"
   },
   "successful116": {
    "type": "string",
    "description": "Successful: 116"
   },
   "failed2": {
    "type": "integer",
    "description": "Failed: 2"
   },
   "inspectRule": {
    "type": "string",
    "description": "Inspect Rule"
   },
   "inspectExecution": {
    "type": "string",
    "description": "Inspect Execution"
   }
  }
 },
 "AutomationExecutionAutonomousActionMonitorView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over approvals state, assembled at read time from tables that already exist",
  "description": "**What Automation Execution & Autonomous Action Monitor displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "automatedActionsToday": {
    "type": "string",
    "description": "Automated Actions Today"
   },
   "successful": {
    "type": "string",
    "description": "Successful"
   },
   "failed": {
    "type": "integer",
    "description": "Failed"
   },
   "humanConfirmationRequired": {
    "type": "boolean",
    "description": "Human Confirmation Required"
   },
   "reversed": {
    "type": "string",
    "description": "Reversed"
   },
   "suspended": {
    "type": "string",
    "description": "Suspended"
   },
   "estimatedManualActionsAvoided": {
    "type": "string",
    "description": "Estimated Manual Actions Avoided"
   },
   "estimatedTimeSaved": {
    "type": "string",
    "format": "date-time",
    "description": "Estimated Time Saved"
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
    "type": "string",
    "description": "Confidence where AI-assisted"
   },
   "executionTime": {
    "type": "string",
    "format": "date-time",
    "description": "Execution Time"
   },
   "status": {
    "type": "integer",
    "description": "Status"
   },
   "triggerT24Hours": {
    "type": "string",
    "description": "Trigger: T−24 hours"
   },
   "participantsEvaluated842": {
    "type": "string",
    "description": "Participants evaluated: 842"
   },
   "incomplete118": {
    "type": "string",
    "description": "Incomplete: 118"
   },
   "messagesTriggered118": {
    "type": "string",
    "description": "Messages triggered: 118"
   },
   "successful116": {
    "type": "string",
    "description": "Successful: 116"
   },
   "failed2": {
    "type": "integer",
    "description": "Failed: 2"
   },
   "inspectRule": {
    "type": "string",
    "description": "Inspect Rule"
   },
   "inspectExecution": {
    "type": "string",
    "description": "Inspect Execution"
   }
  }
 },
 "CrossModuleOrchestrationMonitorView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over approvals state, assembled at read time from tables that already exist",
  "description": "**What Cross-Module Orchestration Monitor displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "bookingConfirmed": {
    "type": "string",
    "description": "Booking confirmed ✓"
   },
   "reserve420Tickets": {
    "type": "string",
    "description": "Reserve 420 tickets ✓"
   },
   "reserve4Guides": {
    "type": "string",
    "description": "Reserve 4 guides ✓"
   },
   "reserve420Meals": {
    "type": "string",
    "description": "Reserve 420 meals ✓"
   },
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
    "description": "Status"
   },
   "started": {
    "type": "string",
    "description": "Started"
   },
   "completed": {
    "type": "string",
    "description": "Completed"
   },
   "duration": {
    "type": "string",
    "format": "date-time",
    "description": "Duration"
   },
   "inputOutput": {
    "type": "string",
    "description": "Input/Output"
   },
   "waits": {
    "type": "string",
    "description": "Waits"
   },
   "retries": {
    "type": "integer",
    "description": "Retries"
   },
   "rollsBack": {
    "type": "string",
    "description": "Rolls back"
   },
   "continuesPartially": {
    "type": "string",
    "description": "Continues partially"
   },
   "requiresHumanIntervention": {
    "type": "string",
    "description": "Requires human intervention"
   },
   "aCommonCorrelationWorkflowId": {
    "type": "string",
    "description": "a common correlation/workflow ID"
   }
  }
 },
 "ProcessOptimizationAutomationOpportunityCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over approvals state, assembled at read time from tables that already exist",
  "description": "**What Process Optimization & Automation Opportunity Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "repetitiveApproval": {
    "type": "string",
    "description": "Repetitive Approval"
   },
   "unnecessaryApproval": {
    "type": "string",
    "description": "Unnecessary Approval"
   },
   "highManualWork": {
    "type": "string",
    "description": "High Manual Work"
   },
   "excessiveRework": {
    "type": "string",
    "description": "Excessive Rework"
   },
   "longWaitingTime": {
    "type": "string",
    "format": "date-time",
    "description": "Long Waiting Time"
   },
   "highFailureRate": {
    "type": "number",
    "description": "High Failure Rate"
   },
   "lowRiskManualAction": {
    "type": "string",
    "description": "Low-Risk Manual Action"
   },
   "processBottleneck": {
    "type": "string",
    "description": "Process Bottleneck"
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
    "type": "string",
    "format": "date-time",
    "description": "Average Duration"
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
   },
   "monthlyRequests4820": {
    "type": "string",
    "description": "Monthly Requests: 4,820"
   },
   "approvalRate992": {
    "type": "number",
    "description": "Approval Rate: 99.2%"
   },
   "averageApprovalDelay18Hours": {
    "type": "number",
    "description": "Average Approval Delay: 1.8 hours"
   }
  }
 },
 "SlaEscalationBottleneckMonitorView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over approvals state, assembled at read time from tables that already exist",
  "description": "**What SLA, Escalation & Bottleneck Monitor displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "withinSla": {
    "type": "string",
    "description": "Within SLA"
   },
   "atRisk": {
    "type": "string",
    "description": "At Risk"
   },
   "breached": {
    "type": "string",
    "description": "Breached"
   },
   "escalated": {
    "type": "string",
    "description": "Escalated"
   },
   "averageProcessingTime": {
    "type": "string",
    "format": "date-time",
    "description": "Average Processing Time"
   },
   "averageApprovalTime": {
    "type": "string",
    "format": "date-time",
    "description": "Average Approval Time"
   },
   "longestWaitingStep": {
    "type": "string",
    "description": "Longest Waiting Step"
   },
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
    "description": "Started"
   },
   "target": {
    "type": "string",
    "description": "Target"
   },
   "timeRemaining": {
    "type": "string",
    "format": "date-time",
    "description": "Time Remaining"
   },
   "risk": {
    "type": "string",
    "description": "Risk"
   },
   "escalationLevel": {
    "type": "string",
    "description": "Escalation Level"
   },
   "averageWorkflow112Hours": {
    "type": "number",
    "description": "Average workflow: 11.2 hours"
   },
   "departmentHead42Min": {
    "type": "string",
    "description": "Department Head — 42 min"
   },
   "finance21Hrs": {
    "type": "string",
    "description": "Finance — 2.1 hrs"
   },
   "cfo78Hrs": {
    "type": "string",
    "description": "CFO — 7.8 hrs"
   },
   "execution18Min": {
    "type": "string",
    "description": "Execution — 18 min"
   },
   "primaryBottleneckCfoApproval": {
    "type": "string",
    "description": "Primary Bottleneck: CFO Approval"
   },
   "firstReminder": {
    "type": "string",
    "description": "First Reminder"
   },
   "secondReminder": {
    "type": "string",
    "description": "Second Reminder"
   },
   "managerEscalation": {
    "type": "string",
    "description": "Manager Escalation"
   },
   "executiveEscalation": {
    "type": "string",
    "description": "Executive Escalation"
   },
   "finalOutcome": {
    "type": "string",
    "description": "Final Outcome"
   },
   "reassign": {
    "type": "string",
    "description": "Reassign"
   },
   "changePriority": {
    "type": "string",
    "description": "Change Priority"
   }
  }
 },
 "UnifiedApprovalInboxDecisionWorkspaceInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Unified Approval Inbox & Decision Workspace submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "discountException18": {
    "type": "number",
    "description": "Discount Exception — 18%"
   },
   "purchaseOrderAed72000": {
    "type": "string",
    "description": "Purchase Order — AED 72,000"
   },
   "overtimeRequest18Hours": {
    "type": "string",
    "description": "Overtime Request — 18 Hours"
   },
   "whatIsBeingRequested": {
    "type": "string",
    "description": "What is being requested?"
   },
   "whyIsApprovalRequired": {
    "type": "string",
    "description": "Why is approval required?"
   },
   "documentsCommentsHistory": {
    "type": "string",
    "description": "Documents, comments, history"
   }
  }
 },
 "UnifiedApprovalInboxDecisionWorkspaceView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over approvals state, assembled at read time from tables that already exist",
  "description": "**What Unified Approval Inbox & Decision Workspace displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "approvalId": {
    "type": "string",
    "description": "Approval ID"
   },
   "requestType": {
    "type": "string",
    "description": "Request Type"
   },
   "sourceModule": {
    "type": "string",
    "description": "Source Module"
   },
   "requester": {
    "type": "string",
    "description": "Requester"
   },
   "amountImpact": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Amount/Impact"
   },
   "priority": {
    "type": "string",
    "description": "Priority"
   },
   "submitted": {
    "type": "string",
    "description": "Submitted"
   },
   "slaRemaining": {
    "type": "string",
    "description": "SLA Remaining"
   },
   "approvalLevel": {
    "type": "string",
    "description": "Approval Level"
   },
   "status": {
    "type": "integer",
    "description": "Status"
   },
   "discountException18": {
    "type": "number",
    "description": "Discount Exception — 18%"
   },
   "purchaseOrderAed72000": {
    "type": "string",
    "description": "Purchase Order — AED 72,000"
   },
   "overtimeRequest18Hours": {
    "type": "string",
    "description": "Overtime Request — 18 Hours"
   },
   "whatIsBeingRequested": {
    "type": "string",
    "description": "What is being requested?"
   },
   "whyIsApprovalRequired": {
    "type": "string",
    "description": "Why is approval required?"
   },
   "documentsCommentsHistory": {
    "type": "string",
    "description": "Documents, comments, history"
   }
  }
 },
 "WorkflowAnalyticsProcessPerformanceView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over approvals state, assembled at read time from tables that already exist",
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
    "type": "string",
    "format": "date-time",
    "description": "Average Completion Time"
   },
   "approvalTime": {
    "type": "string",
    "format": "date-time",
    "description": "Approval Time"
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
    "type": "string",
    "description": "SLA Compliance"
   },
   "averageApprovalTime": {
    "type": "string",
    "format": "date-time",
    "description": "Average Approval Time"
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
   "workflowV14VsV15": {
    "type": "string",
    "description": "Workflow v1.4 vs v1.5"
   },
   "v1448Hours": {
    "type": "string",
    "description": "v1.4 — 4.8 hours"
   },
   "v1529Hours": {
    "type": "string",
    "description": "v1.5 — 2.9 hours"
   },
   "manualStepsRemoved": {
    "type": "string",
    "description": "Manual Steps Removed"
   },
   "processingTimeSaved": {
    "type": "string",
    "format": "date-time",
    "description": "Processing Time Saved"
   },
   "workloadReduced": {
    "type": "string",
    "description": "Workload Reduced"
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
  "x-ticvai-persistence": "none — projection over approvals state, assembled at read time from tables that already exist",
  "description": "**What Workflow Exception, Failure & Recovery Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "businessRuleFailure": {
    "type": "string",
    "description": "Business Rule Failure"
   },
   "missingData": {
    "type": "string",
    "description": "Missing Data"
   },
   "missingApprover": {
    "type": "string",
    "description": "Missing Approver"
   },
   "permissionFailure": {
    "type": "string",
    "description": "Permission Failure"
   },
   "integrationFailure": {
    "type": "string",
    "description": "Integration Failure"
   },
   "timeout": {
    "type": "string",
    "description": "Timeout"
   },
   "actionFailure": {
    "type": "string",
    "description": "Action Failure"
   },
   "invalidState": {
    "type": "string",
    "description": "Invalid State"
   },
   "serviceUnavailable": {
    "type": "string",
    "description": "Service Unavailable"
   },
   "configurationError": {
    "type": "string",
    "description": "Configuration Error"
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
    "type": "integer",
    "description": "Failed Step"
   },
   "errorType": {
    "type": "string",
    "description": "Error Type"
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
   "reassign": {
    "type": "string",
    "description": "Reassign"
   },
   "correctData": {
    "type": "string",
    "description": "Correct Data"
   },
   "useApprovedAlternative": {
    "type": "string",
    "description": "Use Approved Alternative"
   },
   "disappear": {
    "type": "string",
    "description": "disappear"
   }
  }
 },
 "WorkflowInstanceMonitorProcessTimelineView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over approvals state, assembled at read time from tables that already exist",
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
    "type": "integer",
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
    "description": "Started"
   },
   "completed": {
    "type": "string",
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
    "type": "string",
    "format": "date-time",
    "description": "Duration"
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
   },
   "reassign": {
    "type": "string",
    "description": "Reassign"
   },
   "skipStepWhereExplicitlyAllowed": {
    "type": "boolean",
    "description": "Skip Step where explicitly allowed"
   }
  }
 },
 "WorkflowOperationsCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over approvals state, assembled at read time from tables that already exist",
  "description": "**What Workflow Operations Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "workflowsRunning": {
    "type": "string",
    "description": "Workflows Running"
   },
   "startedToday": {
    "type": "string",
    "description": "Started Today"
   },
   "completedToday": {
    "type": "string",
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
    "type": "string",
    "description": "SLA At Risk"
   },
   "slaBreached": {
    "type": "string",
    "description": "SLA Breached"
   },
   "failedWorkflows": {
    "type": "integer",
    "description": "Failed Workflows"
   },
   "escalated": {
    "type": "string",
    "description": "Escalated"
   },
   "automatedExecutions": {
    "type": "integer",
    "description": "Automated Executions"
   },
   "averageCompletionTime": {
    "type": "string",
    "format": "date-time",
    "description": "Average Completion Time"
   },
   "automationSuccessRate": {
    "type": "number",
    "description": "Automation Success Rate"
   },
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
    "description": "Module"
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
    "type": "integer",
    "description": "Status"
   },
   "ticketing": {
    "type": "string",
    "description": "Ticketing"
   },
   "pricing": {
    "type": "string",
    "description": "Pricing"
   },
   "finance": {
    "type": "string",
    "description": "Finance"
   },
   "procurement": {
    "type": "string",
    "description": "Procurement"
   },
   "crm": {
    "type": "string",
    "description": "CRM"
   },
   "resourceManagement": {
    "type": "string",
    "description": "Resource Management"
   },
   "fB": {
    "type": "string",
    "description": "F&B"
   },
   "retail": {
    "type": "string",
    "description": "Retail"
   },
   "groupSales": {
    "type": "integer",
    "description": "Group Sales"
   },
   "customerService": {
    "type": "string",
    "description": "Customer Service"
   },
   "membership": {
    "type": "string",
    "description": "Membership"
   },
   "wallet": {
    "type": "string",
    "description": "Wallet"
   },
   "waiver": {
    "type": "string",
    "description": "Waiver"
   },
   "subscriptionLicensing": {
    "type": "string",
    "description": "Subscription & Licensing"
   }
  }
 }
}
```
