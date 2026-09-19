# WS55 — Rules  Workflow  Approval   Automation Engine board 1

**10 screens · 10 operations · 17 schemas · 2 permissions**

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
| `ADM-238` | Rules & Workflow Command Center | commandCentre | 1 | 0 | — |
| `ADM-239` | Visual Business Rule Builder | listDetail | 1 | 0 | — |
| `ADM-240` | Conditions, Decision Logic & Decision Tables | listDetail | 1 | 0 | — |
| `ADM-241` | Visual Workflow Designer | configEditor | 1 | 0 | — |
| `ADM-242` | Approval Matrix & Multi-Level Approval Configuration | configEditor | 1 | 0 | — |
| `ADM-243` | Roles, Authority, Delegation & Approval Limits | configEditor | 1 | 0 | — |
| `ADM-244` | SLA, Escalation, Reminder & Timeout Rules | configEditor | 1 | 0 | — |
| `ADM-245` | Trigger, Action & Cross-Module Orchestration Configuration | configEditor | 1 | 0 | — |
| `ADM-246` | Workflow Testing, Simulation & Impact Analysis | listDetail | 1 | 0 | — |
| `ADM-247` | Versioning, Governance, Approval & Publication | listDetail | 1 | 0 | — |

## Thin screens in this batch

**ADM-239, ADM-240 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-238",
  "name": "Rules & Workflow Command Center",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Rules__Workflow__Approval___Automation_Engine_Reference.pdf",
   "board": "1",
   "number": "13.1.1",
   "page": 5
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/rules-workflow-command-center-adm-238",
   "component": "apps/ticvai-web/src/routes/platform/RulesWorkflowCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-239",
    "ADM-240",
    "ADM-241",
    "ADM-242",
    "ADM-243",
    "ADM-244",
    "ADM-245",
    "ADM-246",
    "ADM-247"
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
     "to": "ADM-239",
     "trigger": "Works in Visual Business Rule Builder",
     "provenance": "flow F164 step 1→2",
     "operation": "listRuleWorkflow"
    },
    {
     "to": "ADM-240",
     "trigger": "Works in Conditions, Decision Logic & Decision Tables",
     "provenance": "flow F164 step 3→4",
     "operation": "listRuleWorkflow"
    },
    {
     "to": "ADM-241",
     "trigger": "Works in Visual Workflow Designer",
     "provenance": "flow F164 step 5→6",
     "operation": "listRuleWorkflow"
    },
    {
     "to": "ADM-242",
     "trigger": "Works in Approval Matrix & Multi-Level Approval Configuration",
     "provenance": "flow F164 step 7→8",
     "operation": "listRuleWorkflow"
    },
    {
     "to": "ADM-243",
     "trigger": "Works in Roles, Authority, Delegation & Approval Limits",
     "provenance": "flow F164 step 9→10",
     "operation": "listRuleWorkflow"
    },
    {
     "to": "ADM-244",
     "trigger": "Works in SLA, Escalation, Reminder & Timeout Rules",
     "provenance": "flow F164 step 11→12",
     "operation": "listRuleWorkflow"
    },
    {
     "to": "ADM-245",
     "trigger": "Works in Trigger, Action & Cross-Module Orchestration Configuration",
     "provenance": "flow F164 step 13→14",
     "operation": "listRuleWorkflow"
    },
    {
     "to": "ADM-246",
     "trigger": "Works in Workflow Testing, Simulation & Impact Analysis",
     "provenance": "flow F164 step 15→16",
     "operation": "listRuleWorkflow"
    },
    {
     "to": "ADM-247",
     "trigger": "Works in Versioning, Governance, Approval & Publication",
     "provenance": "flow F164 step 17→18",
     "operation": "listRuleWorkflow"
    }
   ]
  },
  "density": "compact",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each configuration should show) — counts over a population, then the population",
  "purpose": "Provide administrators with a centralized portfolio of all business rules, workflows, approvals and automations configured across TICVAI.",
  "purposeNote": "Administrators can locate, understand and govern all TICVAI rules and workflows from one centralized workspace.",
  "layout": {
   "template": "dashboard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Active Rules",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 5 §Display",
       "bindsTo": "RulesWorkflowCommandCenterView.activeRules"
      },
      {
       "kind": "metricTile",
       "label": "Active Workflows",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 5 §Display",
       "bindsTo": "RulesWorkflowCommandCenterView.activeWorkflows"
      },
      {
       "kind": "metricTile",
       "label": "Approval Workflows",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 5 §Display",
       "bindsTo": "RulesWorkflowCommandCenterView.approvalWorkflows"
      },
      {
       "kind": "metricTile",
       "label": "Draft Configurations",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 5 §Display",
       "bindsTo": "RulesWorkflowCommandCenterView.draftConfigurations"
      },
      {
       "kind": "metricTile",
       "label": "Pending Approval",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 5 §Display",
       "bindsTo": "RulesWorkflowCommandCenterView.pendingApproval"
      },
      {
       "kind": "metricTile",
       "label": "Scheduled Changes",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 5 §Display",
       "bindsTo": "RulesWorkflowCommandCenterView.scheduledChanges"
      },
      {
       "kind": "metricTile",
       "label": "Rules With Errors",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 5 §Display",
       "bindsTo": "RulesWorkflowCommandCenterView.rulesWithErrors"
      },
      {
       "kind": "metricTile",
       "label": "Workflows With Warnings",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 5 §Display",
       "bindsTo": "RulesWorkflowCommandCenterView.workflowsWithWarnings"
      },
      {
       "kind": "metricTile",
       "label": "Recently Modified",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 5 §Display",
       "bindsTo": "RulesWorkflowCommandCenterView.recentlyModified"
      },
      {
       "kind": "metricTile",
       "label": "Modules Covered",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 5 §Display",
       "bindsTo": "RulesWorkflowCommandCenterView.modulesCovered"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "moduleTiles",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every rules workflow",
       "columns": [
        "RulesWorkflowCommandCenterView.ruleWorkflowId",
        "RulesWorkflowCommandCenterView.name",
        "RulesWorkflowCommandCenterView.type",
        "RulesWorkflowCommandCenterView.sourceModule",
        "RulesWorkflowCommandCenterView.businessProcess",
        "RulesWorkflowCommandCenterView.version",
        "RulesWorkflowCommandCenterView.owner",
        "RulesWorkflowCommandCenterView.effectiveDate",
        "RulesWorkflowCommandCenterView.status",
        "RulesWorkflowCommandCenterView.lastModified",
        "RulesWorkflowCommandCenterView.usage"
       ],
       "bindsTo": "RulesWorkflowCommandCenterView",
       "operation": "listRuleWorkflow",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 5 §Each configuration should show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected rules workflow",
       "bindsTo": "RulesWorkflowCommandCenterView",
       "columns": [
        "RulesWorkflowCommandCenterView.ruleWorkflowId",
        "RulesWorkflowCommandCenterView.name",
        "RulesWorkflowCommandCenterView.type",
        "RulesWorkflowCommandCenterView.sourceModule",
        "RulesWorkflowCommandCenterView.businessProcess",
        "RulesWorkflowCommandCenterView.version",
        "RulesWorkflowCommandCenterView.owner",
        "RulesWorkflowCommandCenterView.effectiveDate",
        "RulesWorkflowCommandCenterView.status",
        "RulesWorkflowCommandCenterView.lastModified",
        "RulesWorkflowCommandCenterView.usage"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Classify as”.",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 5 §Each configuration should show"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The rules workflow list; the counts above it resolve separately.",
   "error": "Could not load. Names which read failed and leaves the rules workflow untouched.",
   "emptyFirstRun": "No rules workflow yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the rules workflow are still there. The pack's own statuses are Suspended → Retired — the state names which is selected.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listRuleWorkflow",
    "contract": "approvals",
    "purpose": "Rules & Workflow Command Center",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-238"
  },
  "apisNote": "Regenerated 9 September 2026 from Rules__Workflow__Approval___Automation_Engine_Reference.pdf page 5. 21 of 21 labels bound to a contract property; 22 of 45 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-239",
  "name": "Visual Business Rule Builder",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Rules__Workflow__Approval___Automation_Engine_Reference.pdf",
   "board": "1",
   "number": "13.1.2",
   "page": 6
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/visual-business-rule-builder-adm-239",
   "component": "apps/ticvai-web/src/routes/platform/VisualBusinessRuleBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-238"
   ],
   "exitTo": [
    "ADM-238"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-238, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-238",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F164 step 2→3",
     "operation": "setVisualBusinessRule"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow administrators to create business rules without software development.",
  "purposeNote": "Authorized administrators can configure deterministic business decisions using governed",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 6"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 6"
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
       "provenance": "contract operation setVisualBusinessRule"
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
       "impliedBy": "setVisualBusinessRule"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The visual business rule list.",
   "error": "Could not load. Names which read failed and leaves the visual business rule untouched.",
   "emptyFirstRun": "No visual business rule yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the visual business rule are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setVisualBusinessRule",
    "contract": "approvals",
    "purpose": "Visual Business Rule Builder",
    "trigger": "onAction",
    "invalidates": [
     "setVisualBusinessRule"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-239"
  },
  "apisNote": "Regenerated 9 September 2026 from Rules__Workflow__Approval___Automation_Engine_Reference.pdf page 6. 0 of 0 labels bound to a contract property; 0 of 41 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-240",
  "name": "Conditions, Decision Logic & Decision Tables",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Rules__Workflow__Approval___Automation_Engine_Reference.pdf",
   "board": "1",
   "number": "13.1.3",
   "page": 8
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/conditions-decision-logic-decision-tables-adm-240",
   "component": "apps/ticvai-web/src/routes/platform/ConditionsDecisionLogicDecisionTables.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-238"
   ],
   "exitTo": [
    "ADM-238"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-238, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-238",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F164 step 4→5",
     "operation": "listConditionDecisionLogic"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure advanced decision logic where simple IF/THEN rules are insufficient.",
  "purposeNote": "Complex business decisions can be modeled predictably, tested and reused without creating contradictory or ambiguous outcomes.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 8"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 8"
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
       "impliedBy": "listConditionDecisionLogic",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The conditions decision logic list.",
   "error": "Could not load. Names which read failed and leaves the conditions decision logic untouched.",
   "emptyFirstRun": "No conditions decision logic yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the conditions decision logic are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listConditionDecisionLogic",
    "contract": "approvals",
    "purpose": "Conditions, Decision Logic & Decision Tables",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "preloaded": [
    "ConditionsDecisionLogicDecisionTablesView.anyCancelledAutoApprove",
    "ConditionsDecisionLogicDecisionTablesView.aed251",
    "ConditionsDecisionLogicDecisionTablesView.manager",
    "ConditionsDecisionLogicDecisionTablesView.priority",
    "ConditionsDecisionLogicDecisionTablesView.sequence"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-240"
  },
  "apisNote": "Regenerated 9 September 2026 from Rules__Workflow__Approval___Automation_Engine_Reference.pdf page 8. 0 of 0 labels bound to a contract property; 0 of 33 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-241",
  "name": "Visual Workflow Designer",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Rules__Workflow__Approval___Automation_Engine_Reference.pdf",
   "board": "1",
   "number": "13.1.4",
   "page": 10
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/visual-workflow-designer-adm-241",
   "component": "apps/ticvai-web/src/routes/platform/VisualWorkflowDesigner.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-238"
   ],
   "exitTo": [
    "ADM-238"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-238, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-238",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F164 step 6→7",
     "operation": "setVisualWorkflow"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Allow administrators to visually design complete business processes.",
  "purposeNote": "Administrators can visually design governed end-to-end business processes including decisions, approvals, tasks and system actions.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Workflow Name",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 10 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Module",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 10 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Business Process",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 10 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Owner",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 10 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Trigger",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 10 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Version",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 10 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Priority",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 10 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Effective Dates",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 10 §Configure"
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
       "provenance": "contract operation setVisualWorkflow"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The visual workflow designer configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the visual workflow designer untouched.",
   "emptyFirstRun": "No visual workflow designer configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setVisualWorkflow",
    "contract": "approvals",
    "purpose": "Visual Workflow Designer",
    "trigger": "onAction",
    "invalidates": [
     "setVisualWorkflow"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-241"
  },
  "apisNote": "Regenerated 9 September 2026 from Rules__Workflow__Approval___Automation_Engine_Reference.pdf page 10. 0 of 0 labels bound to a contract property; 8 of 42 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "gaps": [
   {
    "operation": null,
    "why": "**Visual Workflow Designer declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 13"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 13"
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
  "id": "ADM-242",
  "name": "Approval Matrix & Multi-Level Approval Configuration",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Rules__Workflow__Approval___Automation_Engine_Reference.pdf",
   "board": "1",
   "number": "13.1.5",
   "page": 11
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/approval-matrix-multi-level-approval-configuration-adm-242",
   "component": "apps/ticvai-web/src/routes/platform/ApprovalMatrixMultiLevelApprovalConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-238"
   ],
   "exitTo": [
    "ADM-238"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-238, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-238",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F164 step 8→9",
     "operation": "approveMatrixMultiLevel"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure when approvals are required and who must approve.",
  "purposeNote": "and configured authority rules.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 6 actions on this screen and the screen declares 1 operation.** Unserved: Single Approval, Sequential Approval, Parallel Approval, Any-One Approval, Conditional Approval, Multi-Level Approval. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 11 §Support"
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
       "label": "Sequential/Parallel",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 11 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Minimum Approvals",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 11 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Rejection Behavior",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 11 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Request Changes",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 11 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Delegate",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 11 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Reassign",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 11 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Skip Conditions",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 11 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Single Approval",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 11 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Sequential Approval",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 11 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Parallel Approval",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 11 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Any-One Approval",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 11 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Conditional Approval",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 11 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Multi-Level Approval",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 11 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The approval multi-level approval configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the approval multi-level approval untouched.",
   "emptyFirstRun": "No approval multi-level approval configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "approveMatrixMultiLevel",
    "contract": "approvals",
    "purpose": "Approval Matrix & Multi-Level Approval Configuration",
    "trigger": "onAction",
    "invalidates": [
     "approveMatrixMultiLevel"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-242"
  },
  "apisNote": "Regenerated 9 September 2026 from Rules__Workflow__Approval___Automation_Engine_Reference.pdf page 11. 0 of 0 labels bound to a contract property; 13 of 50 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-243",
  "name": "Roles, Authority, Delegation & Approval Limits",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Rules__Workflow__Approval___Automation_Engine_Reference.pdf",
   "board": "1",
   "number": "13.1.6",
   "page": 13
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/roles-authority-delegation-approval-limits-adm-243",
   "component": "apps/ticvai-web/src/routes/platform/RolesAuthorityDelegationApprovalLimits.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-238"
   ],
   "exitTo": [
    "ADM-238"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-238, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-238",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F164 step 10→11",
     "operation": "approveRoleAuthorityDelegation"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Define by; Capture) and no display directory — it is settings, not a population",
  "purpose": "Define who has authority to perform or approve specific actions. This should work with TICVAI RBAC/PBAC rather than replace it.",
  "purposeNote": "Every approval is routed only to an authorized approver with valid authority for that transaction and organizational scope.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "User",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 13 §Define by"
      },
      {
       "kind": "selectField",
       "label": "Role",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 13 §Define by"
      },
      {
       "kind": "selectField",
       "label": "Position",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 13 §Define by"
      },
      {
       "kind": "selectField",
       "label": "Department",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 13 §Define by"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 13 §Define by"
      },
      {
       "kind": "selectField",
       "label": "Business Unit",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 13 §Define by"
      },
      {
       "kind": "selectField",
       "label": "Legal Entity",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 13 §Define by"
      },
      {
       "kind": "selectField",
       "label": "Region",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 13 §Define by"
      },
      {
       "kind": "selectField",
       "label": "Delegator",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 13 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Delegate",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 13 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Scope",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 13 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Start",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 13 §Capture"
      },
      {
       "kind": "selectField",
       "label": "End",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 13 §Capture"
      },
      {
       "kind": "selectField",
       "label": "Reason",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 13 §Capture"
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
       "provenance": "contract operation approveRoleAuthorityDelegation"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The roles authority delegation configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the roles authority delegation untouched.",
   "emptyFirstRun": "No roles authority delegation configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "approveRoleAuthorityDelegation",
    "contract": "approvals",
    "purpose": "Roles, Authority, Delegation & Approval Limits",
    "trigger": "onAction",
    "invalidates": [
     "approveRoleAuthorityDelegation"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-243"
  },
  "apisNote": "Regenerated 9 September 2026 from Rules__Workflow__Approval___Automation_Engine_Reference.pdf page 13. 0 of 0 labels bound to a contract property; 14 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-244",
  "name": "SLA, Escalation, Reminder & Timeout Rules",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Rules__Workflow__Approval___Automation_Engine_Reference.pdf",
   "board": "1",
   "number": "13.1.7",
   "page": 14
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/sla-escalation-reminder-timeout-rules-adm-244",
   "component": "apps/ticvai-web/src/routes/platform/SlaEscalationReminderTimeoutRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-238"
   ],
   "exitTo": [
    "ADM-238"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-238, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-238",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F164 step 12→13",
     "operation": "listSlaEscalationReminder"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Define how workflows behave when people or systems do not act within the expected time.",
  "purposeNote": "Every time-sensitive workflow can automatically remind, escalate or safely handle overdue activities according to configurable SLA policies.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Response SLA",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 14 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Approval SLA",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 14 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Task SLA",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 14 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Resolution SLA",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 14 §Configure"
      },
      {
       "kind": "selectField",
       "label": "System Action Timeout",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 14 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The sla escalation reminder configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the sla escalation reminder untouched.",
   "emptyFirstRun": "No sla escalation reminder configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listSlaEscalationReminder",
    "contract": "approvals",
    "purpose": "SLA, Escalation, Reminder & Timeout Rules",
    "trigger": "onLoad"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-244"
  },
  "apisNote": "Regenerated 9 September 2026 from Rules__Workflow__Approval___Automation_Engine_Reference.pdf page 14. 0 of 0 labels bound to a contract property; 5 of 36 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-245",
  "name": "Trigger, Action & Cross-Module Orchestration Configuration",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Rules__Workflow__Approval___Automation_Engine_Reference.pdf",
   "board": "1",
   "number": "13.1.8",
   "page": 16
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/trigger-action-cross-module-orchestration-configuration-adm-245",
   "component": "apps/ticvai-web/src/routes/platform/TriggerActionCrossModuleOrchestrationConfigurati.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-238"
   ],
   "exitTo": [
    "ADM-238"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-238, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-238",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F164 step 14→15",
     "operation": "setTriggerActionCross"
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Define what starts a workflow and what TICVAI services may be called during execution.",
  "purposeNote": "Workflows can securely orchestrate approved actions across TICVAI modules while preserving module ownership, authorization and transactional integrity.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 11 actions on this screen and the screen declares 1 operation.** Unserved: Create Approval, Create Task, Update Status, Apply Hold, Release Hold, Create Notification, Execute Refund, Update Allocation …. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 16 §Actions can include"
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
       "label": "Retry",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 16 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Rollback where supported",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 16 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Compensation Action",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 16 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Exception Queue",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 16 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Human Intervention",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 16 §Configure"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create Approval",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 16 §Actions can include"
      },
      {
       "kind": "secondaryButton",
       "label": "Create Task",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 16 §Actions can include"
      },
      {
       "kind": "secondaryButton",
       "label": "Update Status",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 16 §Actions can include"
      },
      {
       "kind": "secondaryButton",
       "label": "Apply Hold",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 16 §Actions can include"
      },
      {
       "kind": "secondaryButton",
       "label": "Release Hold",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 16 §Actions can include"
      },
      {
       "kind": "secondaryButton",
       "label": "Create Notification",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 16 §Actions can include"
      },
      {
       "kind": "secondaryButton",
       "label": "Execute Refund",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 16 §Actions can include"
      },
      {
       "kind": "secondaryButton",
       "label": "Update Allocation",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 16 §Actions can include"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The trigger action cross-module configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the trigger action cross-module untouched.",
   "emptyFirstRun": "No trigger action cross-module configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setTriggerActionCross",
    "contract": "approvals",
    "purpose": "Trigger, Action & Cross-Module Orchestration Configuration",
    "trigger": "onAction",
    "invalidates": [
     "setTriggerActionCross"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-245"
  },
  "apisNote": "Regenerated 9 September 2026 from Rules__Workflow__Approval___Automation_Engine_Reference.pdf page 16. 0 of 0 labels bound to a contract property; 16 of 43 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-246",
  "name": "Workflow Testing, Simulation & Impact Analysis",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Rules__Workflow__Approval___Automation_Engine_Reference.pdf",
   "board": "1",
   "number": "13.1.9",
   "page": 18
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/workflow-testing-simulation-impact-analysis-adm-246",
   "component": "apps/ticvai-web/src/routes/platform/WorkflowTestingSimulationImpactAnalysis.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-238"
   ],
   "exitTo": [
    "ADM-238"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-238, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation.",
   "transitions": [
    {
     "to": "ADM-238",
     "trigger": "Returns to the board's landing screen",
     "provenance": "flow F164 step 16→17",
     "operation": "simulateWorkflowTestingImpact"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Allow administrators to test rules and workflows before they affect live operations. This is a critical screen.",
  "purposeNote": "No workflow needs to be tested for the first time in production; administrators can simulate logic, routing and expected impact safely before publication.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 3 actions on this screen and the screen declares 1 operation.** Unserved: Manual Test Case, Scenario Simulation, Batch Test. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 18 §Support"
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
       "label": "Every workflow testing simulation",
       "columns": [
        "WorkflowTestingSimulationImpactAnalysisView.rulesEvaluated",
        "WorkflowTestingSimulationImpactAnalysisView.conditionsMatched",
        "WorkflowTestingSimulationImpactAnalysisView.decisions",
        "WorkflowTestingSimulationImpactAnalysisView.approvalPath",
        "WorkflowTestingSimulationImpactAnalysisView.actions",
        "WorkflowTestingSimulationImpactAnalysisView.notifications",
        "WorkflowTestingSimulationImpactAnalysisView.sla",
        "WorkflowTestingSimulationImpactAnalysisView.expectedOutcome"
       ],
       "bindsTo": "WorkflowTestingSimulationImpactAnalysisView",
       "operation": "simulateWorkflowTestingImpact",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 18 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected workflow testing simulation",
       "bindsTo": "WorkflowTestingSimulationImpactAnalysisView",
       "columns": [
        "WorkflowTestingSimulationImpactAnalysisView.rulesEvaluated",
        "WorkflowTestingSimulationImpactAnalysisView.conditionsMatched",
        "WorkflowTestingSimulationImpactAnalysisView.decisions",
        "WorkflowTestingSimulationImpactAnalysisView.approvalPath",
        "WorkflowTestingSimulationImpactAnalysisView.actions",
        "WorkflowTestingSimulationImpactAnalysisView.notifications",
        "WorkflowTestingSimulationImpactAnalysisView.sla",
        "WorkflowTestingSimulationImpactAnalysisView.expectedOutcome"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Input”, “Historical Replay”, “Result”, “This workflow is used by”, “Regression Testing”.",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 18 §Show"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Manual Test Case",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 18 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Scenario Simulation",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 18 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Batch Test",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 18 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The workflow testing simulation list.",
   "error": "Could not load. Names which read failed and leaves the workflow testing simulation untouched.",
   "emptyFirstRun": "No workflow testing simulation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the workflow testing simulation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "simulateWorkflowTestingImpact",
    "contract": "approvals",
    "purpose": "Workflow Testing, Simulation & Impact Analysis",
    "trigger": "onAction",
    "invalidates": [
     "simulateWorkflowTestingImpact"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "WorkflowTestingSimulationImpactAnalysisView.rulesEvaluated",
    "WorkflowTestingSimulationImpactAnalysisView.conditionsMatched",
    "WorkflowTestingSimulationImpactAnalysisView.decisions",
    "WorkflowTestingSimulationImpactAnalysisView.approvalPath",
    "WorkflowTestingSimulationImpactAnalysisView.actions",
    "WorkflowTestingSimulationImpactAnalysisView.notifications"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-246"
  },
  "apisNote": "Regenerated 9 September 2026 from Rules__Workflow__Approval___Automation_Engine_Reference.pdf page 18. 8 of 8 labels bound to a contract property; 11 of 42 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-247",
  "name": "Versioning, Governance, Approval & Publication",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Rules__Workflow__Approval___Automation_Engine_Reference.pdf",
   "board": "1",
   "number": "13.1.10",
   "page": 19
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/versioning-governance-approval-publication-adm-247",
   "component": "apps/ticvai-web/src/routes/platform/VersioningGovernanceApprovalPublication.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-238"
   ],
   "exitTo": [
    "ADM-238"
   ],
   "inferred": false,
   "notes": "**Reached from ADM-238, the hub of its workshop board.** Stated on 4 September: the pack groups its screens ten to a board behind a command centre, and that grouping is the navigation."
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Control how rules and workflows move safely from configuration into production. Board 1 configured the rules and workflows. Board 2 is the live operational layer where TICVAI executes, monitors, manages, troubleshoots, analyzes, and optimizes those workflows across the entire platform.",
  "purposeNote": "Only tested, approved and version-controlled rules/workflows can become active, with complete auditability and controlled rollback/suspension capability. Board 1 — Final Screen Register",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 2 actions on this screen and the screen declares 1 operation.** Unserved: Publish Now, Schedule. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 19 §Support"
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
       "label": "Every versioning governance approval",
       "columns": [
        "VersioningGovernanceApprovalPublicationView.v11V20"
       ],
       "bindsTo": "VersioningGovernanceApprovalPublicationView",
       "operation": "approveVersioningGovernance",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 19 §Show"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected versioning governance approval",
       "bindsTo": "VersioningGovernanceApprovalPublicationView",
       "columns": [
        "VersioningGovernanceApprovalPublicationView.v11V20"
       ],
       "notes": "The pack groups this record's detail under its own headings: “Refund Approval”, “Highlight changes to”, “Draft”, “Rollback”, “Kill Switch”, “Record”.",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 19 §Show"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Publish Now",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 19 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Schedule",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 19 §Support"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The versioning governance approval list.",
   "error": "Could not load. Names which read failed and leaves the versioning governance approval untouched.",
   "emptyFirstRun": "No versioning governance approval yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the versioning governance approval are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "approveVersioningGovernance",
    "contract": "approvals",
    "purpose": "Versioning, Governance, Approval & Publication",
    "trigger": "onAction",
    "invalidates": [
     "approveVersioningGovernance"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "VersioningGovernanceApprovalPublicationView.v11V20"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-247"
  },
  "apisNote": "Regenerated 9 September 2026 from Rules__Workflow__Approval___Automation_Engine_Reference.pdf page 19. 1 of 1 labels bound to a contract property; 12 of 103 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "approveMatrixMultiLevel": {
  "method": "PUT",
  "path": "/matrix-multi-level",
  "contract": "approvals",
  "summary": "Approval Matrix & Multi-Level Approval Configuration",
  "permission": "APPROVAL_REQUEST",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "ApprovalMatrixMultiLevelApprovalConfigurationInput",
  "responds": "ApprovalMatrixMultiLevelApprovalConfigurationView"
 },
 "approveRoleAuthorityDelegation": {
  "method": "PUT",
  "path": "/role-authority-delegation",
  "contract": "approvals",
  "summary": "Roles, Authority, Delegation & Approval Limits",
  "permission": "APPROVAL_REQUEST",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "RolesAuthorityDelegationApprovalLimitsInput",
  "responds": "RolesAuthorityDelegationApprovalLimitsView"
 },
 "approveVersioningGovernance": {
  "method": "PUT",
  "path": "/versioning-governance",
  "contract": "approvals",
  "summary": "Versioning, Governance, Approval & Publication",
  "permission": "APPROVAL_REQUEST",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "VersioningGovernanceApprovalPublicationInput",
  "responds": "VersioningGovernanceApprovalPublicationView"
 },
 "listConditionDecisionLogic": {
  "method": "GET",
  "path": "/condition-decision-logic",
  "contract": "approvals",
  "summary": "Conditions, Decision Logic & Decision Tables",
  "permission": "APPROVAL_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ConditionsDecisionLogicDecisionTablesView"
 },
 "listRuleWorkflow": {
  "method": "GET",
  "path": "/rule-workflow",
  "contract": "approvals",
  "summary": "Rules & Workflow Command Center",
  "permission": "APPROVAL_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "RulesWorkflowCommandCenterView"
 },
 "listSlaEscalationReminder": {
  "method": "GET",
  "path": "/sla-escalation-reminder",
  "contract": "approvals",
  "summary": "SLA, Escalation, Reminder & Timeout Rules",
  "permission": "APPROVAL_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "SlaEscalationReminderTimeoutRulesView"
 },
 "setTriggerActionCross": {
  "method": "PUT",
  "path": "/trigger-action-cross",
  "contract": "approvals",
  "summary": "Trigger, Action & Cross-Module Orchestration Configuration",
  "permission": "APPROVAL_REQUEST",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "TriggerActionCrossModuleOrchestrationConfigurationInput",
  "responds": "TriggerActionCrossModuleOrchestrationConfigurationView"
 },
 "setVisualBusinessRule": {
  "method": "PUT",
  "path": "/visual-business-rule",
  "contract": "approvals",
  "summary": "Visual Business Rule Builder",
  "permission": "APPROVAL_REQUEST",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "VisualBusinessRuleBuilderInput",
  "responds": "VisualBusinessRuleBuilderView"
 },
 "setVisualWorkflow": {
  "method": "PUT",
  "path": "/visual-workflow",
  "contract": "approvals",
  "summary": "Visual Workflow Designer",
  "permission": "APPROVAL_REQUEST",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "VisualWorkflowDesignerInput",
  "responds": "VisualWorkflowDesignerView"
 },
 "simulateWorkflowTestingImpact": {
  "method": "PUT",
  "path": "/workflow-testing-impact",
  "contract": "approvals",
  "summary": "Workflow Testing, Simulation & Impact Analysis",
  "permission": "APPROVAL_REQUEST",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "WorkflowTestingSimulationImpactAnalysisInput",
  "responds": "WorkflowTestingSimulationImpactAnalysisView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "ApprovalMatrixMultiLevelApprovalConfigurationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table covers these fields** — the closest is approvals.request at 3%, so this is not an update to anything the package stores today and no new table has been decided",
  "description": "**What Approval Matrix & Multi-Level Approval Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "singleApproval": {
    "type": "string",
    "description": "Single Approval"
   },
   "sequentialApproval": {
    "type": "string",
    "description": "Sequential Approval"
   },
   "parallelApproval": {
    "type": "string",
    "description": "Parallel Approval"
   },
   "anyOneApproval": {
    "type": "string",
    "description": "Any-One Approval"
   },
   "conditionalApproval": {
    "type": "string",
    "description": "Conditional Approval"
   },
   "multiLevelApproval": {
    "type": "string",
    "description": "Multi-Level Approval"
   },
   "exampleDiscount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Example — Discount"
   },
   "commercialDirectorCfo": {
    "type": "string",
    "description": "Commercial Director + CFO"
   },
   "exampleProcurement": {
    "type": "string",
    "description": "Example — Procurement"
   },
   "aed10k50k": {
    "type": "string",
    "description": "AED 10K–50K"
   },
   "departmentHeadFinance": {
    "type": "string",
    "description": "Department Head → Finance"
   },
   "aed50k100k": {
    "type": "string",
    "description": "AED 50K–100K"
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Amount"
   },
   "percentage": {
    "type": "number",
    "description": "Percentage"
   },
   "module": {
    "type": "string",
    "description": "Module"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "department": {
    "type": "string",
    "description": "Department"
   },
   "customerType": {
    "type": "string",
    "description": "Customer Type"
   },
   "risk": {
    "type": "string",
    "description": "Risk"
   },
   "exceptionType": {
    "type": "string",
    "description": "Exception Type"
   },
   "legalEntity": {
    "type": "string",
    "description": "Legal Entity"
   },
   "sequentialParallel": {
    "type": "string",
    "description": "Sequential/Parallel"
   },
   "minimumApprovals": {
    "type": "string",
    "description": "Minimum Approvals"
   },
   "rejectionBehavior": {
    "type": "string",
    "description": "Rejection Behavior"
   },
   "requestChanges": {
    "type": "string",
    "description": "Request Changes"
   },
   "delegate": {
    "type": "string",
    "description": "Delegate"
   },
   "reassign": {
    "type": "string",
    "description": "Reassign"
   },
   "skipConditions": {
    "type": "string",
    "description": "Skip Conditions"
   },
   "approveAed18000": {
    "type": "string",
    "description": "“Approve AED 18,000?”"
   }
  }
 },
 "ApprovalMatrixMultiLevelApprovalConfigurationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over approvals state, assembled at read time from tables that already exist",
  "description": "**What Approval Matrix & Multi-Level Approval Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "singleApproval": {
    "type": "string",
    "description": "Single Approval"
   },
   "sequentialApproval": {
    "type": "string",
    "description": "Sequential Approval"
   },
   "parallelApproval": {
    "type": "string",
    "description": "Parallel Approval"
   },
   "anyOneApproval": {
    "type": "string",
    "description": "Any-One Approval"
   },
   "conditionalApproval": {
    "type": "string",
    "description": "Conditional Approval"
   },
   "multiLevelApproval": {
    "type": "string",
    "description": "Multi-Level Approval"
   },
   "exampleDiscount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Example — Discount"
   },
   "noApproval": {
    "type": "string",
    "description": "No Approval (the pack shows 10.01–15%)"
   },
   "salesManager": {
    "type": "string",
    "description": "Sales Manager (the pack shows 15.01–20%)"
   },
   "commercialDirectorCfo": {
    "type": "string",
    "description": "Commercial Director + CFO"
   },
   "exampleProcurement": {
    "type": "string",
    "description": "Example — Procurement"
   },
   "aed10k50k": {
    "type": "string",
    "description": "AED 10K–50K"
   },
   "departmentHeadFinance": {
    "type": "string",
    "description": "Department Head → Finance"
   },
   "aed50k100k": {
    "type": "string",
    "description": "AED 50K–100K"
   },
   "amount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Amount"
   },
   "percentage": {
    "type": "number",
    "description": "Percentage"
   },
   "module": {
    "type": "string",
    "description": "Module"
   },
   "product": {
    "type": "string",
    "description": "Product"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "department": {
    "type": "string",
    "description": "Department"
   },
   "customerType": {
    "type": "string",
    "description": "Customer Type"
   },
   "risk": {
    "type": "string",
    "description": "Risk"
   },
   "exceptionType": {
    "type": "string",
    "description": "Exception Type"
   },
   "legalEntity": {
    "type": "string",
    "description": "Legal Entity"
   },
   "sequentialParallel": {
    "type": "string",
    "description": "Sequential/Parallel"
   },
   "minimumApprovals": {
    "type": "string",
    "description": "Minimum Approvals"
   },
   "rejectionBehavior": {
    "type": "string",
    "description": "Rejection Behavior"
   },
   "requestChanges": {
    "type": "string",
    "description": "Request Changes"
   },
   "delegate": {
    "type": "string",
    "description": "Delegate"
   },
   "reassign": {
    "type": "string",
    "description": "Reassign"
   },
   "skipConditions": {
    "type": "string",
    "description": "Skip Conditions"
   },
   "approveAed18000": {
    "type": "string",
    "description": "“Approve AED 18,000?”"
   }
  }
 },
 "ConditionsDecisionLogicDecisionTablesView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over approvals state, assembled at read time from tables that already exist",
  "description": "**What Conditions, Decision Logic & Decision Tables displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "anyCancelledAutoApprove": {
    "type": "string",
    "description": "Any Cancelled Auto Approve (the pack shows 250, AED 251–)"
   },
   "aed251": {
    "type": "string",
    "description": "AED 251–"
   },
   "manager": {
    "type": "string",
    "description": "Manager +"
   },
   "priority": {
    "type": "string",
    "description": "Priority"
   },
   "sequence": {
    "type": "string",
    "description": "Sequence"
   },
   "specificity": {
    "type": "string",
    "description": "Specificity"
   },
   "stopProcessing": {
    "type": "string",
    "description": "Stop Processing"
   },
   "continueEvaluation": {
    "type": "string",
    "description": "Continue Evaluation"
   },
   "contradictoryRules": {
    "type": "string",
    "description": "Contradictory Rules"
   },
   "overlappingConditions": {
    "type": "string",
    "description": "Overlapping Conditions"
   },
   "unreachableOutcomes": {
    "type": "string",
    "description": "Unreachable Outcomes"
   },
   "circularLogic": {
    "type": "string",
    "description": "Circular Logic"
   },
   "missingOutcomes": {
    "type": "string",
    "description": "Missing Outcomes"
   }
  }
 },
 "RolesAuthorityDelegationApprovalLimitsInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table covers these fields** — the closest is approvals.decision at 4%, so this is not an update to anything the package stores today and no new table has been decided",
  "description": "**What Roles, Authority, Delegation & Approval Limits submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "user": {
    "type": "string",
    "description": "User"
   },
   "role": {
    "type": "string",
    "description": "Role"
   },
   "position": {
    "type": "string",
    "description": "Position"
   },
   "department": {
    "type": "string",
    "description": "Department"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "businessUnit": {
    "type": "string",
    "description": "Business Unit"
   },
   "legalEntity": {
    "type": "string",
    "description": "Legal Entity"
   },
   "region": {
    "type": "string",
    "description": "Region"
   },
   "delegator": {
    "type": "string",
    "description": "Delegator"
   },
   "delegate": {
    "type": "string",
    "description": "Delegate"
   },
   "scope": {
    "type": "string",
    "description": "Scope"
   },
   "start": {
    "type": "string",
    "description": "Start"
   },
   "end": {
    "type": "string",
    "description": "End"
   },
   "reason": {
    "type": "string",
    "description": "Reason"
   },
   "leave": {
    "type": "string",
    "description": "Leave"
   },
   "travel": {
    "type": "string",
    "description": "Travel"
   },
   "vacancy": {
    "type": "string",
    "description": "Vacancy"
   },
   "eventOperations": {
    "type": "string",
    "description": "Event operations"
   },
   "requesterCannotApproveOwnRequest": {
    "type": "string",
    "description": "Requester cannot approve own request"
   },
   "userActive": {
    "type": "integer",
    "description": "User active"
   },
   "requiredRole": {
    "type": "string",
    "description": "Required role"
   },
   "authorityAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Authority amount"
   },
   "businessScope": {
    "type": "string",
    "description": "Business scope"
   },
   "delegationValidity": {
    "type": "string",
    "description": "Delegation validity"
   }
  }
 },
 "RolesAuthorityDelegationApprovalLimitsView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over approvals state, assembled at read time from tables that already exist",
  "description": "**What Roles, Authority, Delegation & Approval Limits displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "user": {
    "type": "string",
    "description": "User"
   },
   "role": {
    "type": "string",
    "description": "Role"
   },
   "position": {
    "type": "string",
    "description": "Position"
   },
   "department": {
    "type": "string",
    "description": "Department"
   },
   "venue": {
    "type": "string",
    "description": "Venue"
   },
   "businessUnit": {
    "type": "string",
    "description": "Business Unit"
   },
   "legalEntity": {
    "type": "string",
    "description": "Legal Entity"
   },
   "region": {
    "type": "string",
    "description": "Region"
   },
   "delegator": {
    "type": "string",
    "description": "Delegator"
   },
   "delegate": {
    "type": "string",
    "description": "Delegate"
   },
   "scope": {
    "type": "string",
    "description": "Scope"
   },
   "start": {
    "type": "string",
    "description": "Start"
   },
   "end": {
    "type": "string",
    "description": "End"
   },
   "reason": {
    "type": "string",
    "description": "Reason"
   },
   "leave": {
    "type": "string",
    "description": "Leave"
   },
   "travel": {
    "type": "string",
    "description": "Travel"
   },
   "vacancy": {
    "type": "string",
    "description": "Vacancy"
   },
   "eventOperations": {
    "type": "string",
    "description": "Event operations"
   },
   "requesterCannotApproveOwnRequest": {
    "type": "string",
    "description": "Requester cannot approve own request"
   },
   "userActive": {
    "type": "integer",
    "description": "User active"
   },
   "requiredRole": {
    "type": "string",
    "description": "Required role"
   },
   "authorityAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Authority amount"
   },
   "businessScope": {
    "type": "string",
    "description": "Business scope"
   },
   "delegationValidity": {
    "type": "string",
    "description": "Delegation validity"
   }
  }
 },
 "RulesWorkflowCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over approvals state, assembled at read time from tables that already exist",
  "description": "**What Rules & Workflow Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "activeRules": {
    "type": "integer",
    "description": "Active Rules"
   },
   "activeWorkflows": {
    "type": "integer",
    "description": "Active Workflows"
   },
   "approvalWorkflows": {
    "type": "integer",
    "description": "Approval Workflows"
   },
   "draftConfigurations": {
    "type": "integer",
    "description": "Draft Configurations"
   },
   "pendingApproval": {
    "type": "integer",
    "description": "Pending Approval"
   },
   "scheduledChanges": {
    "type": "integer",
    "description": "Scheduled Changes"
   },
   "rulesWithErrors": {
    "type": "integer",
    "description": "Rules With Errors"
   },
   "workflowsWithWarnings": {
    "type": "integer",
    "description": "Workflows With Warnings"
   },
   "recentlyModified": {
    "type": "string",
    "description": "Recently Modified"
   },
   "modulesCovered": {
    "type": "string",
    "description": "Modules Covered"
   },
   "ruleWorkflowId": {
    "type": "string",
    "description": "Rule/Workflow ID"
   },
   "name": {
    "type": "string",
    "description": "Name"
   },
   "type": {
    "type": "string",
    "description": "Type"
   },
   "sourceModule": {
    "type": "string",
    "description": "Source Module"
   },
   "businessProcess": {
    "type": "string",
    "description": "Business Process"
   },
   "version": {
    "type": "string",
    "description": "Version"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   },
   "effectiveDate": {
    "type": "string",
    "format": "date-time",
    "description": "Effective Date"
   },
   "status": {
    "type": "integer",
    "description": "Status"
   },
   "lastModified": {
    "type": "string",
    "format": "date-time",
    "description": "Last Modified"
   },
   "usage": {
    "type": "string",
    "description": "Usage"
   },
   "businessRule": {
    "type": "string",
    "description": "Business Rule"
   },
   "approvalWorkflow": {
    "type": "string",
    "description": "Approval Workflow"
   },
   "operationalWorkflow": {
    "type": "string",
    "description": "Operational Workflow"
   },
   "decisionRule": {
    "type": "string",
    "description": "Decision Rule"
   },
   "validationRule": {
    "type": "string",
    "description": "Validation Rule"
   },
   "escalationRule": {
    "type": "string",
    "description": "Escalation Rule"
   },
   "automation": {
    "type": "string",
    "description": "Automation"
   },
   "crossModuleWorkflow": {
    "type": "string",
    "description": "Cross-Module Workflow"
   },
   "suspendedRetired": {
    "type": "string",
    "description": "Suspended → Retired"
   }
  }
 },
 "SlaEscalationReminderTimeoutRulesView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over approvals state, assembled at read time from tables that already exist",
  "description": "**What SLA, Escalation, Reminder & Timeout Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "responseSla": {
    "type": "string",
    "description": "Response SLA"
   },
   "approvalSla": {
    "type": "string",
    "description": "Approval SLA"
   },
   "taskSla": {
    "type": "string",
    "description": "Task SLA"
   },
   "resolutionSla": {
    "type": "string",
    "description": "Resolution SLA"
   },
   "systemActionTimeout": {
    "type": "string",
    "description": "System Action Timeout"
   },
   "target4Hours": {
    "type": "string",
    "description": "Target: 4 hours"
   },
   "at50": {
    "type": "number",
    "description": "At 50%"
   },
   "at75": {
    "type": "number",
    "description": "At 75%"
   },
   "at100": {
    "type": "number",
    "description": "At 100%"
   },
   "calendarHours": {
    "type": "string",
    "description": "Calendar Hours"
   },
   "businessHours": {
    "type": "string",
    "description": "Business Hours"
   },
   "workingDays": {
    "type": "string",
    "description": "Working Days"
   },
   "venueCalendar": {
    "type": "string",
    "description": "Venue Calendar"
   },
   "holidayCalendar": {
    "type": "string",
    "description": "Holiday Calendar"
   },
   "reassign": {
    "type": "string",
    "description": "Reassign"
   },
   "raisePriority": {
    "type": "string",
    "description": "Raise Priority"
   },
   "channelsType": {
    "type": "string",
    "enum": [
     "email",
     "push",
     "inApp",
     "smsWhereAppropriate"
    ],
    "description": "Vocabulary listed under Reminder Channels."
   }
  }
 },
 "TriggerActionCrossModuleOrchestrationConfigurationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Trigger, Action & Cross-Module Orchestration Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "authorizedUserStartsWorkflow": {
    "type": "string",
    "description": "Authorized user starts workflow"
   },
   "executeRefund": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Execute Refund"
   },
   "callApprovedApi": {
    "type": "string",
    "description": "Call Approved API"
   },
   "callApprovedService": {
    "type": "string",
    "description": "Call Approved Service"
   },
   "startSubWorkflow": {
    "type": "string",
    "description": "Start Sub-Workflow"
   },
   "workflowAuthority": {
    "type": "string",
    "description": "Workflow Authority"
   },
   "userSystemAuthority": {
    "type": "string",
    "description": "User/System Authority"
   },
   "modulePolicy": {
    "type": "string",
    "description": "Module Policy"
   },
   "businessRule": {
    "type": "string",
    "description": "Business Rule"
   },
   "rollbackWhereSupported": {
    "type": "string",
    "description": "Rollback where supported"
   },
   "compensationAction": {
    "type": "string",
    "description": "Compensation Action"
   },
   "exceptionQueue": {
    "type": "string",
    "description": "Exception Queue"
   },
   "humanIntervention": {
    "type": "string",
    "description": "Human Intervention"
   },
   "refunds": {
    "type": "string",
    "description": "Refunds"
   },
   "orders": {
    "type": "string",
    "description": "Orders"
   },
   "payments": {
    "type": "string",
    "description": "Payments"
   },
   "approvals": {
    "type": "string",
    "description": "Approvals"
   },
   "tickets": {
    "type": "string",
    "description": "Tickets"
   }
  }
 },
 "TriggerActionCrossModuleOrchestrationConfigurationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over approvals state, assembled at read time from tables that already exist",
  "description": "**What Trigger, Action & Cross-Module Orchestration Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "authorizedUserStartsWorkflow": {
    "type": "string",
    "description": "Authorized user starts workflow"
   },
   "executeRefund": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Execute Refund"
   },
   "callApprovedApi": {
    "type": "string",
    "description": "Call Approved API"
   },
   "callApprovedService": {
    "type": "string",
    "description": "Call Approved Service"
   },
   "startSubWorkflow": {
    "type": "string",
    "description": "Start Sub-Workflow"
   },
   "workflowAuthority": {
    "type": "string",
    "description": "Workflow Authority"
   },
   "userSystemAuthority": {
    "type": "string",
    "description": "User/System Authority"
   },
   "modulePolicy": {
    "type": "string",
    "description": "Module Policy"
   },
   "businessRule": {
    "type": "string",
    "description": "Business Rule"
   },
   "rollbackWhereSupported": {
    "type": "string",
    "description": "Rollback where supported"
   },
   "compensationAction": {
    "type": "string",
    "description": "Compensation Action"
   },
   "exceptionQueue": {
    "type": "string",
    "description": "Exception Queue"
   },
   "humanIntervention": {
    "type": "string",
    "description": "Human Intervention"
   },
   "refunds": {
    "type": "string",
    "description": "Refunds"
   },
   "orders": {
    "type": "string",
    "description": "Orders"
   },
   "payments": {
    "type": "string",
    "description": "Payments"
   },
   "approvals": {
    "type": "string",
    "description": "Approvals"
   },
   "tickets": {
    "type": "string",
    "description": "Tickets"
   }
  }
 },
 "VersioningGovernanceApprovalPublicationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Versioning, Governance, Approval & Publication submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "v10Retired": {
    "type": "string",
    "description": "v1.0 — Retired"
   },
   "v11Active": {
    "type": "integer",
    "description": "v1.1 — Active"
   },
   "v20Draft": {
    "type": "string",
    "description": "v2.0 — Draft"
   },
   "version": {
    "type": "string",
    "description": "Version"
   },
   "changedBy": {
    "type": "string",
    "description": "Changed By"
   },
   "changeDate": {
    "type": "string",
    "format": "date-time",
    "description": "Change Date"
   },
   "changeReason": {
    "type": "string",
    "description": "Change Reason"
   },
   "businessOwner": {
    "type": "string",
    "description": "Business Owner"
   },
   "technicalOwner": {
    "type": "string",
    "description": "Technical Owner"
   },
   "riskClassification": {
    "type": "string",
    "description": "Risk Classification"
   },
   "testResults": {
    "type": "string",
    "description": "Test Results"
   },
   "approval": {
    "type": "string",
    "description": "Approval"
   },
   "conditions": {
    "type": "string",
    "description": "Conditions"
   },
   "thresholds": {
    "type": "string",
    "description": "Thresholds"
   },
   "approvers": {
    "type": "string",
    "description": "Approvers"
   },
   "actions": {
    "type": "string",
    "description": "Actions"
   },
   "sla": {
    "type": "string",
    "description": "SLA"
   },
   "escalation": {
    "type": "string",
    "description": "Escalation"
   },
   "integrations": {
    "type": "string",
    "description": "Integrations"
   },
   "selectedTenant": {
    "type": "string",
    "description": "Selected Tenant"
   },
   "selectedVenue": {
    "type": "string",
    "description": "Selected Venue"
   },
   "selectedBrand": {
    "type": "string",
    "description": "Selected Brand"
   },
   "controlledRollout": {
    "type": "string",
    "description": "Controlled Rollout"
   },
   "technicallySafe": {
    "type": "string",
    "description": "technically safe"
   },
   "whoCreated": {
    "type": "string",
    "format": "date-time",
    "description": "Who created"
   },
   "whoChanged": {
    "type": "string",
    "description": "Who changed"
   },
   "whoTested": {
    "type": "string",
    "description": "Who tested"
   },
   "whoApproved": {
    "type": "string",
    "description": "Who approved"
   },
   "whoPublished": {
    "type": "string",
    "description": "Who published"
   },
   "whatChanged": {
    "type": "string",
    "description": "What changed"
   },
   "businessTransaction": {
    "type": "string",
    "description": "business transaction"
   }
  }
 },
 "VersioningGovernanceApprovalPublicationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over approvals state, assembled at read time from tables that already exist",
  "description": "**What Versioning, Governance, Approval & Publication displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "v10Retired": {
    "type": "string",
    "description": "v1.0 — Retired"
   },
   "v11Active": {
    "type": "integer",
    "description": "v1.1 — Active"
   },
   "v20Draft": {
    "type": "string",
    "description": "v2.0 — Draft"
   },
   "version": {
    "type": "string",
    "description": "Version"
   },
   "changedBy": {
    "type": "string",
    "description": "Changed By"
   },
   "changeDate": {
    "type": "string",
    "format": "date-time",
    "description": "Change Date"
   },
   "changeReason": {
    "type": "string",
    "description": "Change Reason"
   },
   "businessOwner": {
    "type": "string",
    "description": "Business Owner"
   },
   "technicalOwner": {
    "type": "string",
    "description": "Technical Owner"
   },
   "riskClassification": {
    "type": "string",
    "description": "Risk Classification"
   },
   "testResults": {
    "type": "string",
    "description": "Test Results"
   },
   "approval": {
    "type": "string",
    "description": "Approval"
   },
   "v11V20": {
    "type": "string",
    "description": "v1.1 ↔ v2.0"
   },
   "conditions": {
    "type": "string",
    "description": "Conditions"
   },
   "thresholds": {
    "type": "string",
    "description": "Thresholds"
   },
   "approvers": {
    "type": "string",
    "description": "Approvers"
   },
   "actions": {
    "type": "string",
    "description": "Actions"
   },
   "sla": {
    "type": "string",
    "description": "SLA"
   },
   "escalation": {
    "type": "string",
    "description": "Escalation"
   },
   "integrations": {
    "type": "string",
    "description": "Integrations"
   },
   "selectedTenant": {
    "type": "string",
    "description": "Selected Tenant"
   },
   "selectedVenue": {
    "type": "string",
    "description": "Selected Venue"
   },
   "selectedBrand": {
    "type": "string",
    "description": "Selected Brand"
   },
   "controlledRollout": {
    "type": "string",
    "description": "Controlled Rollout"
   },
   "technicallySafe": {
    "type": "string",
    "description": "technically safe"
   },
   "whoCreated": {
    "type": "string",
    "format": "date-time",
    "description": "Who created"
   },
   "whoChanged": {
    "type": "string",
    "description": "Who changed"
   },
   "whoTested": {
    "type": "string",
    "description": "Who tested"
   },
   "whoApproved": {
    "type": "string",
    "description": "Who approved"
   },
   "whoPublished": {
    "type": "string",
    "description": "Who published"
   },
   "whatChanged": {
    "type": "string",
    "description": "What changed"
   },
   "businessTransaction": {
    "type": "string",
    "description": "business transaction"
   }
  }
 },
 "VisualBusinessRuleBuilderInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Visual Business Rule Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "equals": {
    "type": "string",
    "description": "Equals"
   },
   "notEquals": {
    "type": "string",
    "description": "Not Equals"
   },
   "inList": {
    "type": "string",
    "description": "In List"
   },
   "exists": {
    "type": "string",
    "description": "Exists"
   },
   "doesNotExist": {
    "type": "string",
    "description": "Does Not Exist"
   },
   "beforeAfter": {
    "type": "string",
    "description": "Before/After"
   },
   "percentageThreshold": {
    "type": "integer",
    "description": "Percentage Threshold"
   },
   "boolean": {
    "type": "string",
    "description": "Boolean"
   },
   "cancelled": {
    "type": "integer",
    "description": "cancelled"
   }
  }
 },
 "VisualBusinessRuleBuilderView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over approvals state, assembled at read time from tables that already exist",
  "description": "**What Visual Business Rule Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "equals": {
    "type": "string",
    "description": "Equals"
   },
   "notEquals": {
    "type": "string",
    "description": "Not Equals"
   },
   "inList": {
    "type": "string",
    "description": "In List"
   },
   "exists": {
    "type": "string",
    "description": "Exists"
   },
   "doesNotExist": {
    "type": "string",
    "description": "Does Not Exist"
   },
   "beforeAfter": {
    "type": "string",
    "description": "Before/After"
   },
   "percentageThreshold": {
    "type": "integer",
    "description": "Percentage Threshold"
   },
   "boolean": {
    "type": "string",
    "description": "Boolean"
   },
   "cancelled": {
    "type": "integer",
    "description": "cancelled"
   }
  }
 },
 "VisualWorkflowDesignerInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table covers these fields** — the closest is approvals.decision at 4%, so this is not an update to anything the package stores today and no new table has been decided",
  "description": "**What Visual Workflow Designer submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "start": {
    "type": "string",
    "description": "Start"
   },
   "task": {
    "type": "string",
    "description": "Task"
   },
   "decision": {
    "type": "string",
    "description": "Decision"
   },
   "approval": {
    "type": "string",
    "description": "Approval"
   },
   "systemAction": {
    "type": "string",
    "description": "System Action"
   },
   "notification": {
    "type": "string",
    "description": "Notification"
   },
   "wait": {
    "type": "string",
    "description": "Wait"
   },
   "timer": {
    "type": "string",
    "description": "Timer"
   },
   "parallelBranch": {
    "type": "string",
    "description": "Parallel Branch"
   },
   "escalation": {
    "type": "string",
    "description": "Escalation"
   },
   "subWorkflow": {
    "type": "string",
    "description": "Sub-Workflow"
   },
   "end": {
    "type": "string",
    "description": "End"
   },
   "yesNo": {
    "type": "string",
    "description": "↙ YES ↘ NO"
   },
   "workflowName": {
    "type": "string",
    "description": "Workflow Name"
   },
   "module": {
    "type": "string",
    "description": "Module"
   },
   "businessProcess": {
    "type": "string",
    "description": "Business Process"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   },
   "version": {
    "type": "string",
    "description": "Version"
   },
   "priority": {
    "type": "string",
    "description": "Priority"
   },
   "effectiveDates": {
    "type": "string",
    "description": "Effective Dates"
   },
   "deadEnds": {
    "type": "string",
    "description": "Dead Ends"
   },
   "missingOutcomes": {
    "type": "string",
    "description": "Missing Outcomes"
   },
   "circularLoops": {
    "type": "string",
    "description": "Circular Loops"
   },
   "missingAssignee": {
    "type": "string",
    "description": "Missing Assignee"
   },
   "invalidActions": {
    "type": "string",
    "description": "Invalid Actions"
   }
  }
 },
 "VisualWorkflowDesignerView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over approvals state, assembled at read time from tables that already exist",
  "description": "**What Visual Workflow Designer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "start": {
    "type": "string",
    "description": "Start"
   },
   "task": {
    "type": "string",
    "description": "Task"
   },
   "decision": {
    "type": "string",
    "description": "Decision"
   },
   "approval": {
    "type": "string",
    "description": "Approval"
   },
   "systemAction": {
    "type": "string",
    "description": "System Action"
   },
   "notification": {
    "type": "string",
    "description": "Notification"
   },
   "wait": {
    "type": "string",
    "description": "Wait"
   },
   "timer": {
    "type": "string",
    "description": "Timer"
   },
   "parallelBranch": {
    "type": "string",
    "description": "Parallel Branch"
   },
   "escalation": {
    "type": "string",
    "description": "Escalation"
   },
   "subWorkflow": {
    "type": "string",
    "description": "Sub-Workflow"
   },
   "end": {
    "type": "string",
    "description": "End"
   },
   "yesNo": {
    "type": "string",
    "description": "↙ YES ↘ NO"
   },
   "workflowName": {
    "type": "string",
    "description": "Workflow Name"
   },
   "module": {
    "type": "string",
    "description": "Module"
   },
   "businessProcess": {
    "type": "string",
    "description": "Business Process"
   },
   "owner": {
    "type": "string",
    "description": "Owner"
   },
   "version": {
    "type": "string",
    "description": "Version"
   },
   "priority": {
    "type": "string",
    "description": "Priority"
   },
   "effectiveDates": {
    "type": "string",
    "description": "Effective Dates"
   },
   "deadEnds": {
    "type": "string",
    "description": "Dead Ends"
   },
   "missingOutcomes": {
    "type": "string",
    "description": "Missing Outcomes"
   },
   "circularLoops": {
    "type": "string",
    "description": "Circular Loops"
   },
   "missingAssignee": {
    "type": "string",
    "description": "Missing Assignee"
   },
   "invalidActions": {
    "type": "string",
    "description": "Invalid Actions"
   }
  }
 },
 "WorkflowTestingSimulationImpactAnalysisInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures",
  "description": "**What Workflow Testing, Simulation & Impact Analysis submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "manualTestCase": {
    "type": "string",
    "description": "Manual Test Case"
   },
   "sampleTransaction": {
    "type": "string",
    "description": "Sample Transaction"
   },
   "historicalReplay": {
    "type": "string",
    "description": "Historical Replay"
   },
   "scenarioSimulation": {
    "type": "string",
    "description": "Scenario Simulation"
   },
   "batchTest": {
    "type": "string",
    "description": "Batch Test"
   },
   "refundAed1500": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Refund: AED 1,500"
   },
   "customerGold": {
    "type": "string",
    "description": "Customer: Gold"
   },
   "eventActive": {
    "type": "integer",
    "description": "Event: Active"
   },
   "reasonCustomerRequest": {
    "type": "string",
    "description": "Reason: Customer Request"
   }
  }
 },
 "WorkflowTestingSimulationImpactAnalysisView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over approvals state, assembled at read time from tables that already exist",
  "description": "**What Workflow Testing, Simulation & Impact Analysis displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "manualTestCase": {
    "type": "string",
    "description": "Manual Test Case"
   },
   "sampleTransaction": {
    "type": "string",
    "description": "Sample Transaction"
   },
   "historicalReplay": {
    "type": "string",
    "description": "Historical Replay"
   },
   "scenarioSimulation": {
    "type": "string",
    "description": "Scenario Simulation"
   },
   "batchTest": {
    "type": "string",
    "description": "Batch Test"
   },
   "refundAed1500": {
    "$ref": "../shared/common.yaml#/components/schemas/Money",
    "description": "Refund: AED 1,500"
   },
   "customerGold": {
    "type": "string",
    "description": "Customer: Gold"
   },
   "eventActive": {
    "type": "integer",
    "description": "Event: Active"
   },
   "reasonCustomerRequest": {
    "type": "string",
    "description": "Reason: Customer Request"
   },
   "rulesEvaluated": {
    "type": "string",
    "description": "Rules Evaluated"
   },
   "conditionsMatched": {
    "type": "string",
    "description": "Conditions Matched"
   },
   "decisions": {
    "type": "integer",
    "description": "Decisions"
   },
   "approvalPath": {
    "type": "string",
    "description": "Approval Path"
   },
   "actions": {
    "type": "integer",
    "description": "Actions"
   },
   "notifications": {
    "type": "integer",
    "description": "Notifications"
   },
   "sla": {
    "type": "string",
    "description": "SLA"
   },
   "expectedOutcome": {
    "type": "string",
    "description": "Expected Outcome"
   }
  }
 }
}
```
