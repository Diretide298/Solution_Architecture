# WS55 — Rules  Workflow  Approval   Automation Engine board 1

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
  `APPROVAL_CONFIGURE, APPROVAL_DECIDE, APPROVAL_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
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
| `ADM-242` | Approval Matrix & Multi-Level Approval Configuration | configEditor | 2 | 0 | — |
| `ADM-243` | Roles, Authority, Delegation & Approval Limits | configEditor | 3 | 0 | — |
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
     "provenance": "derived — ADM-002 declares entryState.params  and ADM-238 holds none of them. The edge carries nothing: ADM-238 is opened from ADM-002, so this edge is the way back and ADM-002 keeps its own state"
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
  "purposeNote": "Administrators can locate, understand and govern all TICVAI rules and workflows from one centralized workspace.",
  "pattern": "commandCentre",
  "patternReason": "the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each configuration should show) — counts over a population, then the population",
  "purpose": "Provide administrators with a centralized portfolio of all business rules, workflows, approvals and automations configured across TICVAI.",
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
       "bindsTo": "RulesWorkflowCommandCenterViewSummary.activeRules"
      },
      {
       "kind": "metricTile",
       "label": "Active Workflows",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 5 §Display",
       "bindsTo": "RulesWorkflowCommandCenterViewSummary.activeWorkflows"
      },
      {
       "kind": "metricTile",
       "label": "Approval Workflows",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 5 §Display",
       "bindsTo": "RulesWorkflowCommandCenterViewSummary.approvalWorkflows"
      },
      {
       "kind": "metricTile",
       "label": "Draft Configurations",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 5 §Display",
       "bindsTo": "RulesWorkflowCommandCenterViewSummary.draftConfigurations"
      },
      {
       "kind": "metricTile",
       "label": "Pending Approval",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 5 §Display",
       "bindsTo": "RulesWorkflowCommandCenterViewSummary.pendingApproval"
      },
      {
       "kind": "metricTile",
       "label": "Scheduled Changes",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 5 §Display",
       "bindsTo": "RulesWorkflowCommandCenterViewSummary.scheduledChanges"
      },
      {
       "kind": "metricTile",
       "label": "Rules With Errors",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 5 §Display",
       "bindsTo": "RulesWorkflowCommandCenterViewSummary.rulesWithErrors"
      },
      {
       "kind": "metricTile",
       "label": "Workflows With Warnings",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 5 §Display",
       "bindsTo": "RulesWorkflowCommandCenterViewSummary.workflowsWithWarnings"
      },
      {
       "kind": "metricTile",
       "label": "Recently Modified",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 5 §Display",
       "bindsTo": "RulesWorkflowCommandCenterViewSummary.recentlyModified"
      },
      {
       "kind": "metricTile",
       "label": "Modules Covered",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 5 §Display",
       "bindsTo": "RulesWorkflowCommandCenterViewSummary.modulesCovered"
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-238",
   "workshopBoard": "wireframes/WS136 Rules  Workflow  Approval   Automation Engine Board 1.dc.html#adm-238"
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
  "purposeNote": "Authorized administrators can configure deterministic business decisions using governed",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow administrators to create business rules without software development.",
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
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-239",
   "workshopBoard": "wireframes/WS136 Rules  Workflow  Approval   Automation Engine Board 1.dc.html#adm-239"
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
  "purposeNote": "Complex business decisions can be modeled predictably, tested and reused without creating contradictory or ambiguous outcomes.",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure advanced decision logic where simple IF/THEN rules are insufficient.",
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
    "ConditionsDecisionLogicDecisionTablesView.resolutionStrategy"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-240",
   "workshopBoard": "wireframes/WS136 Rules  Workflow  Approval   Automation Engine Board 1.dc.html#adm-240"
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
  "purposeNote": "Administrators can visually design governed end-to-end business processes including decisions, approvals, tasks and system actions.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Allow administrators to visually design complete business processes.",
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
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-241",
   "workshopBoard": "wireframes/WS136 Rules  Workflow  Approval   Automation Engine Board 1.dc.html#adm-241"
  },
  "apisNote": "Regenerated 9 September 2026 from Rules__Workflow__Approval___Automation_Engine_Reference.pdf page 10. 0 of 0 labels bound to a contract property; 8 of 42 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
     "provenance": "flow F164 step 8→9"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "and configured authority rules.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Configure when approvals are required and who must approve.",
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
    "operationId": "listApprovalMatrices",
    "contract": "approvals",
    "purpose": "The approval matrices in force",
    "trigger": "onLoad",
    "provenance": "decided 29 September, readiness close-out (QA wiring note)"
   },
   {
    "operationId": "setApprovalMatrix",
    "contract": "approvals",
    "purpose": "Save the approval matrix and its levels",
    "trigger": "onAction",
    "provenance": "decided 29 September, readiness close-out (QA wiring note)",
    "invalidates": [
     "listApprovalMatrices"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-242",
   "workshopBoard": "wireframes/WS136 Rules  Workflow  Approval   Automation Engine Board 1.dc.html#adm-242"
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
     "provenance": "flow F164 step 10→11"
    }
   ]
  },
  "density": "compact",
  "purposeNote": "Every approval is routed only to an authorized approver with valid authority for that transaction and organizational scope.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Define by; Capture) and no display directory — it is settings, not a population",
  "purpose": "Define who has authority to perform or approve specific actions. This should work with TICVAI RBAC/PBAC rather than replace it.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Event operations. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 13 §Support temporary authority for"
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
       "label": "Event operations",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 13 §Support temporary authority for"
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
    "operationId": "listApprovalDelegations",
    "contract": "approvals",
    "purpose": "Delegations in force",
    "trigger": "onLoad",
    "provenance": "decided 29 September, readiness close-out (QA wiring note)"
   },
   {
    "operationId": "createApprovalDelegation",
    "contract": "approvals",
    "purpose": "Delegate approval authority for a period",
    "trigger": "onAction",
    "provenance": "decided 29 September, readiness close-out (QA wiring note)",
    "invalidates": [
     "listApprovalDelegations"
    ]
   },
   {
    "operationId": "setApprovalMatrix",
    "contract": "approvals",
    "purpose": "Set role authority and approval limits",
    "trigger": "onAction",
    "provenance": "decided 29 September, readiness close-out (QA wiring note)"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-243",
   "workshopBoard": "wireframes/WS136 Rules  Workflow  Approval   Automation Engine Board 1.dc.html#adm-243"
  },
  "apisNote": "Regenerated 9 September 2026 from Rules__Workflow__Approval___Automation_Engine_Reference.pdf page 13. 0 of 0 labels bound to a contract property; 15 of 39 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "purposeNote": "Every time-sensitive workflow can automatically remind, escalate or safely handle overdue activities according to configurable SLA policies.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Define how workflows behave when people or systems do not act within the expected time.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Venue Calendar. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
    "source": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 14 §Support"
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
    },
    {
     "name": "actionBar",
     "slot": "publish",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Venue Calendar",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 14 §Support"
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-244",
   "workshopBoard": "wireframes/WS136 Rules  Workflow  Approval   Automation Engine Board 1.dc.html#adm-244"
  },
  "apisNote": "Regenerated 9 September 2026 from Rules__Workflow__Approval___Automation_Engine_Reference.pdf page 14. 0 of 0 labels bound to a contract property; 6 of 36 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "purposeNote": "Workflows can securely orchestrate approved actions across TICVAI modules while preserving module ownership, authorization and transactional integrity.",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Define what starts a workflow and what TICVAI services may be called during execution.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 13 actions on this screen and the screen declares 1 operation.** Unserved: Create Approval, Create Task, Update Status, Apply Hold, Release Hold, Create Notification, Generate Document, Execute Refund …. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
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
       "label": "Generate Document",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 16 §Actions can include"
      },
      {
       "kind": "secondaryButton",
       "label": "Execute Refund",
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
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-245",
   "workshopBoard": "wireframes/WS136 Rules  Workflow  Approval   Automation Engine Board 1.dc.html#adm-245"
  },
  "apisNote": "Regenerated 9 September 2026 from Rules__Workflow__Approval___Automation_Engine_Reference.pdf page 16. 0 of 0 labels bound to a contract property; 18 of 43 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "purposeNote": "No workflow needs to be tested for the first time in production; administrators can simulate logic, routing and expected impact safely before publication.",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Allow administrators to test rules and workflows before they affect live operations. This is a critical screen.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 5 actions on this screen and the screen declares 1 operation.** Unserved: Manual Test Case, Sample Transaction, Historical Replay, Scenario Simulation, Batch Test. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
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
       "label": "Sample Transaction",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 18 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Historical Replay",
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
    "trigger": "onAction"
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
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-246",
   "workshopBoard": "wireframes/WS136 Rules  Workflow  Approval   Automation Engine Board 1.dc.html#adm-246"
  },
  "apisNote": "Regenerated 9 September 2026 from Rules__Workflow__Approval___Automation_Engine_Reference.pdf page 18. 8 of 8 labels bound to a contract property; 13 of 42 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "purposeNote": "Only tested, approved and version-controlled rules/workflows can become active, with complete auditability and controlled rollback/suspension capability. Board 1 — Final Screen Register",
  "pattern": "listDetail",
  "patternReason": "the pack gives this screen a display directory (§Show) and no metric row",
  "purpose": "Control how rules and workflows move safely from configuration into production. Board 1 configured the rules and workflows. Board 2 is the live operational layer where TICVAI executes, monitors, manages, troubleshoots, analyzes, and optimizes those workflows across the entire platform.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack names 5 actions on this screen and the screen declares 1 operation.** Unserved: Publish Now, Schedule, Selected Tenant, Selected Venue, Selected Brand. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation seen from the screen side rather than the contract side.",
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
      },
      {
       "kind": "secondaryButton",
       "label": "Selected Tenant",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 19 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Selected Venue",
       "provenance": "pack Rules__Workflow__Approval___Automation_Engine_Reference.pdf, page 19 §Support"
      },
      {
       "kind": "secondaryButton",
       "label": "Selected Brand",
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
    "trigger": "onAction"
   }
  ],
  "entryState": {
   "preloaded": []
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-247",
   "workshopBoard": "wireframes/WS136 Rules  Workflow  Approval   Automation Engine Board 1.dc.html#adm-247"
  },
  "apisNote": "Regenerated 9 September 2026 from Rules__Workflow__Approval___Automation_Engine_Reference.pdf page 19. 1 of 1 labels bound to a contract property; 15 of 103 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "approveVersioningGovernance": {
  "method": "PUT",
  "path": "/versioning-governance",
  "contract": "approvals",
  "summary": "Versioning, Governance, Approval & Publication",
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
  "requestBody": "VersioningGovernanceApprovalPublicationInput",
  "responds": "VersioningGovernanceApprovalPublicationView"
 },
 "createApprovalDelegation": {
  "method": "POST",
  "path": "/delegations",
  "contract": "approvals",
  "summary": "Delegate approval authority",
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
  "requestBody": "ApprovalDelegation",
  "responds": "ApprovalDelegation"
 },
 "listApprovalDelegations": {
  "method": "GET",
  "path": "/delegations",
  "contract": "approvals",
  "summary": "Who is standing in for whom",
  "permission": "APPROVAL_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "ApprovalDelegation"
 },
 "listApprovalMatrices": {
  "method": "GET",
  "path": "/approval-matrices",
  "contract": "approvals",
  "summary": "What requires approval here",
  "permission": "APPROVAL_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "kind",
    "in": "query",
    "required": null
   },
   {
    "name": "effective",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "ApprovalMatrix"
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
  "parameters": [
   {
    "name": "type",
    "in": "query",
    "required": false
   },
   {
    "name": "status",
    "in": "query",
    "required": false
   },
   {
    "name": "sourceModule",
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
 "setApprovalMatrix": {
  "method": "PUT",
  "path": "/approval-matrices",
  "contract": "approvals",
  "summary": "Configure what requires approval",
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
  "requestBody": "ApprovalMatrix",
  "responds": "ApprovalMatrix"
 },
 "setTriggerActionCross": {
  "method": "PUT",
  "path": "/trigger-action-cross",
  "contract": "approvals",
  "summary": "Trigger, Action & Cross-Module Orchestration Configuration",
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
  "requestBody": "TriggerActionCrossModuleOrchestrationConfigurationInput",
  "responds": "TriggerActionCrossModuleOrchestrationConfigurationView"
 },
 "setVisualBusinessRule": {
  "method": "PUT",
  "path": "/visual-business-rule",
  "contract": "approvals",
  "summary": "Visual Business Rule Builder",
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
  "requestBody": "VisualBusinessRuleBuilderInput",
  "responds": "VisualBusinessRuleBuilderView"
 },
 "setVisualWorkflow": {
  "method": "PUT",
  "path": "/visual-workflow",
  "contract": "approvals",
  "summary": "Visual Workflow Designer",
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
  "requestBody": "VisualWorkflowDesignerInput",
  "responds": "VisualWorkflowDesignerView"
 },
 "simulateWorkflowTestingImpact": {
  "method": "PUT",
  "path": "/workflow-testing-impact",
  "contract": "approvals",
  "summary": "Workflow Testing, Simulation & Impact Analysis",
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
  "requestBody": "WorkflowTestingSimulationImpactAnalysisInput",
  "responds": "WorkflowTestingSimulationImpactAnalysisView"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "ApprovalDelegation": {
  "type": "object",
  "x-ticvai-persistence": "approvals.delegation",
  "required": [
   "delegatorPrincipalId",
   "delegatePrincipalId",
   "from",
   "to"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "delegatorPrincipalId": {
    "type": "string",
    "format": "uuid",
    "description": "A principal id (`identity.Principal.id`). This contract stores the id only; the name to show, and the people to pick from, come from `identity.listPrincipals` and `identity.getPrincipal`.\n"
   },
   "delegatePrincipalId": {
    "type": "string",
    "format": "uuid",
    "description": "A principal id, resolved to a name the same way as `delegatorPrincipalId`."
   },
   "kinds": {
    "type": "array",
    "description": "Absent means everything the delegator may approve.",
    "items": {
     "$ref": "#/components/schemas/ApprovalKind"
    }
   },
   "maxAmount": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "description": "A delegate may be given less authority than the delegator, never more."
   },
   "from": {
    "type": "string",
    "format": "date-time"
   },
   "to": {
    "type": "string",
    "format": "date-time",
    "description": "**Required.** An open-ended delegation is an approver who quietly stopped approving and a delegate who does not know they still hold it.\n"
   },
   "reason": {
    "type": "string"
   },
   "isActive": {
    "type": "boolean",
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"
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
 "ApprovalMatrix": {
  "type": "object",
  "x-ticvai-persistence": "approvals.matrix",
  "required": [
   "kind",
   "scopeLevel",
   "rules"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "kind": {
    "$ref": "#/components/schemas/ApprovalKind"
   },
   "scopeLevel": {
    "type": "string",
    "enum": [
     "tenant",
     "region",
     "venue"
    ]
   },
   "scopePath": {
    "type": "string",
    "readOnly": true
   },
   "version": {
    "type": "integer",
    "readOnly": true,
    "description": "11.1.80. **A request is decided by the rules it was raised under.** Changing the matrix mid-flight would mean an approver answering a question that changed while they read it.\n**(`kind`, `scopePath`, `version`) is unique**, and a stored version is never edited: a request's `matrixVersion` names exactly one rule set (decided 28 September, audit R129 (2)).\n"
   },
   "rules": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/ApprovalRule"
    }
   },
   "isActive": {
    "type": "boolean"
   }
  }
 },
 "ApprovalRule": {
  "type": "object",
  "x-ticvai-persistence": "approvals.rule",
  "required": [
   "order",
   "approverRoleIds",
   "mode"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "order": {
    "type": "integer",
    "description": "**First match wins.** Explicit ordering is what makes a matrix reviewable — an unordered set of overlapping rules is one nobody can reason about.\n"
   },
   "minAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "maxAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "riskScoreAbove": {
    "type": "number",
    "nullable": true,
    "description": "11.1.12. **Not matched against the AI risk score** (29 September, build pass, group G2). The AI assessment on a request (`ApprovalRequest.aiAssessment`, from `ai.scoreApprovalRequest`) is context for the reviewer only (MoM 8 September: AI never influences approve or reject), and routing a request to more approvers because of it would be influence. A rule with this set matches only a `riskScore` the requesting contract passes in `attributes` from its own deterministic rules (a payment's rule score, for example). Using the AI score here needs the client to say so.\n"
   },
   "condition": {
    "type": "string",
    "nullable": true,
    "description": "11.1.13. Evaluated against the attributes the caller supplied.\n\n**No condition language is defined yet** (pull audit R104, 26 September): the grammar, the attributes it may name and how two conditions are compared for `unreachableRule` are an open decision, not something to infer from this field.\n"
   },
   "approverRoleIds": {
    "type": "array",
    "minItems": 1,
    "description": "Role ids from `identity.listRoles` (`Role.id`), which is where an editor gets the names to show and pick from. This contract stores the ids only.\n",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "approverScopeLevel": {
    "type": "string",
    "enum": [
     "venue",
     "department",
     "region",
     "tenant"
    ],
    "description": "11.1.39. Which organisational level the approver must sit at."
   },
   "mode": {
    "$ref": "#/components/schemas/ApprovalMode"
   },
   "levels": {
    "type": "integer",
    "default": 1,
    "description": "11.1.3. Multi-level chains ask each level in turn."
   },
   "requiresMfa": {
    "type": "boolean",
    "default": false
   },
   "requiresSignature": {
    "type": "boolean",
    "default": false
   },
   "slaMinutes": {
    "type": "integer",
    "nullable": true,
    "description": "11.1.14. Null means no SLA, which is different from a long one."
   },
   "escalateAfterMinutes": {
    "type": "integer",
    "nullable": true
   },
   "escalateToRoleIds": {
    "type": "array",
    "description": "Role ids from `identity.listRoles`, as `approverRoleIds`.",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "expiresAfterMinutes": {
    "type": "integer",
    "nullable": true,
    "description": "11.1.53. An unanswered request eventually stops waiting."
   },
   "externalProviderId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "11.1.65 (29 September). **This level is decided in an external workflow system** (`ApprovalExternalProvider`) rather than by a person in TICVAI. `approverRoleIds` stay required: they are who decides if the provider does not answer in time and its `onTimeout` is `fallBackToRoles`.\n"
   }
  }
 },
 "ConditionsDecisionLogicDecisionTablesView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over approvals.decision_table and decision_table_row (schema DecisionTable) (data model for the agreed operations, 29 September)",
  "description": "**What Conditions, Decision Logic & Decision Tables displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "name": {
    "type": "string",
    "description": "Name"
   },
   "decisionTableId": {
    "type": "string",
    "description": "Decision table or condition set identifier"
   },
   "resolutionStrategy": {
    "type": "string",
    "enum": [
     "priority",
     "sequence",
     "specificity"
    ],
    "description": "How to choose when multiple rules apply"
   },
   "onMatch": {
    "type": "string",
    "enum": [
     "stopProcessing",
     "continueEvaluation"
    ],
    "description": "Whether evaluation stops at the first match"
   },
   "conflicts": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "contradictoryRules",
      "overlappingConditions",
      "unreachableOutcomes",
      "circularLogic",
      "missingOutcomes"
     ]
    },
    "description": "Conflicts detected in this decision logic (read-only)"
   }
  },
  "required": [
   "decisionTableId",
   "name"
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
 "RulesWorkflowCommandCenterView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over approvals.workflow_definition, workflow_version, business_rule, decision_table, automation, matrix and rule; one row per configuration (data model for the agreed operations, 29 September)",
  "description": "**What Rules & Workflow Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
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
    "enum": [
     "businessRule",
     "approvalWorkflow",
     "operationalWorkflow",
     "decisionRule",
     "validationRule",
     "escalationRule",
     "automation",
     "crossModuleWorkflow"
    ],
    "description": "Kind of configuration"
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
    "type": "string",
    "enum": [
     "draft",
     "testing",
     "review",
     "pendingApproval",
     "approved",
     "scheduled",
     "active",
     "suspended",
     "retired"
    ],
    "description": "Lifecycle status"
   },
   "lastModified": {
    "type": "string",
    "format": "date-time",
    "description": "Last Modified"
   },
   "usage": {
    "type": "string",
    "description": "Usage"
   }
  },
  "required": [
   "ruleWorkflowId"
  ]
 },
 "RulesWorkflowCommandCenterViewSummary": {
  "type": "object",
  "x-ticvai-persistence": "none - aggregate computed at read time over the rows the page lists",
  "description": "The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September, readiness close-out).",
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
    "type": "integer",
    "description": "Configurations modified in the recent period"
   },
   "modulesCovered": {
    "type": "integer",
    "description": "Number of modules using configured rules and workflows"
   }
  }
 },
 "SlaEscalationReminderTimeoutRulesView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over approvals.sla_policy (schema ApprovalSlaPolicy), including its reminder-percentage columns (data model for the agreed operations, 29 September)",
  "description": "**What SLA, Escalation, Reminder & Timeout Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "code": {
    "type": "string",
    "description": "Policy code, the same key setApprovalSlaPolicy upserts by"
   },
   "slaType": {
    "type": "string",
    "enum": [
     "responseSla",
     "approvalSla",
     "taskSla",
     "resolutionSla",
     "systemActionTimeout"
    ],
    "description": "Which clock this policy governs"
   },
   "calendarBasis": {
    "type": "string",
    "enum": [
     "calendarHours",
     "businessHours",
     "workingDays",
     "venueCalendar",
     "holidayCalendar"
    ],
    "description": "How elapsed time is counted"
   },
   "escalationActions": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "notify",
      "reassign",
      "escalate",
      "addApprover",
      "createTask",
      "raisePriority",
      "triggerBackupWorkflow"
     ]
    },
    "description": "What happens on escalation"
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
   },
   "targetMinutes": {
    "type": "integer",
    "description": "SLA target in minutes"
   },
   "onBreach": {
    "type": "string",
    "enum": [
     "notifyOnly",
     "escalate",
     "autoApprove",
     "autoReject"
    ],
    "description": "Outcome at breach; auto outcomes only where explicitly permitted"
   },
   "autoActionAllowed": {
    "type": "boolean",
    "description": "Auto-approve or auto-reject on breach is explicitly permitted; default false"
   },
   "firstReminderAtPercent": {
    "type": "integer",
    "description": "Percent of target at which the first reminder goes"
   },
   "secondReminderAtPercent": {
    "type": "integer",
    "description": "Percent of target at which the second reminder goes"
   },
   "escalateAtPercent": {
    "type": "integer",
    "description": "Percent of target at which the request escalates"
   }
  },
  "required": [
   "code"
  ]
 },
 "TriggerActionCrossModuleOrchestrationConfigurationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; writes approvals.workflow_trigger (schema WorkflowTrigger) (data model for the agreed operations, 29 September)",
  "description": "**What Trigger, Action & Cross-Module Orchestration Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "triggerType": {
    "type": "string",
    "enum": [
     "event",
     "dataCondition",
     "schedule",
     "manual"
    ],
    "description": "What starts the workflow"
   },
   "workflowId": {
    "type": "string",
    "description": "Workflow this trigger and action set belongs to"
   },
   "allowedActions": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "createApproval",
      "createTask",
      "updateStatus",
      "applyHold",
      "releaseHold",
      "createNotification",
      "generateDocument",
      "executeRefund",
      "updateAllocation",
      "activateMembership",
      "suspendPartner",
      "callApprovedApi",
      "callApprovedService",
      "startSubWorkflow"
     ]
    },
    "description": "Actions this workflow may call"
   },
   "onFailure": {
    "type": "string",
    "enum": [
     "retry",
     "rollback",
     "compensate",
     "exceptionQueue",
     "humanIntervention"
    ],
    "description": "What happens when an action fails"
   },
   "triggerDefinition": {
    "type": "string",
    "description": "Event name, data condition (e.g. Balance > Limit) or schedule"
   },
   "maxRetries": {
    "type": "integer",
    "description": "Retries before the failure handling applies"
   }
  },
  "required": [
   "workflowId",
   "triggerType"
  ]
 },
 "TriggerActionCrossModuleOrchestrationConfigurationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over approvals.workflow_trigger (schema WorkflowTrigger) (data model for the agreed operations, 29 September)",
  "description": "**What Trigger, Action & Cross-Module Orchestration Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "triggerType": {
    "type": "string",
    "enum": [
     "event",
     "dataCondition",
     "schedule",
     "manual"
    ],
    "description": "What starts the workflow"
   },
   "workflowId": {
    "type": "string",
    "description": "Workflow this trigger and action set belongs to"
   },
   "allowedActions": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "createApproval",
      "createTask",
      "updateStatus",
      "applyHold",
      "releaseHold",
      "createNotification",
      "generateDocument",
      "executeRefund",
      "updateAllocation",
      "activateMembership",
      "suspendPartner",
      "callApprovedApi",
      "callApprovedService",
      "startSubWorkflow"
     ]
    },
    "description": "Actions this workflow may call"
   },
   "onFailure": {
    "type": "string",
    "enum": [
     "retry",
     "rollback",
     "compensate",
     "exceptionQueue",
     "humanIntervention"
    ],
    "description": "What happens when an action fails"
   },
   "triggerDefinition": {
    "type": "string",
    "description": "Event name, data condition (e.g. Balance > Limit) or schedule"
   },
   "maxRetries": {
    "type": "integer",
    "description": "Retries before the failure handling applies"
   }
  },
  "required": [
   "workflowId",
   "triggerType"
  ]
 },
 "VersioningGovernanceApprovalPublicationInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; writes approvals.workflow_version and raises an approvals.request for publication (data model for the agreed operations, 29 September)",
  "description": "**What Versioning, Governance, Approval & Publication submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "workflowId": {
    "type": "string",
    "description": "Rule or workflow the version belongs to"
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
    "description": "Approval request id for this version"
   },
   "changedAreas": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "conditions",
      "thresholds",
      "approvers",
      "actions",
      "sla",
      "escalation",
      "integrations"
     ]
    },
    "description": "Areas that differ from the compared version (read-only)"
   },
   "rolloutScope": {
    "type": "string",
    "enum": [
     "allScopes",
     "selectedTenant",
     "selectedVenue",
     "selectedBrand",
     "controlledRollout"
    ],
    "description": "Where the version is published"
   },
   "whoCreated": {
    "type": "string",
    "description": "User who created the version"
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
   "lifecycleStatus": {
    "type": "string",
    "enum": [
     "draft",
     "tested",
     "businessReview",
     "technicalValidation",
     "approval",
     "scheduled",
     "active",
     "suspended",
     "retired"
    ],
    "description": "Version lifecycle status"
   },
   "scopeIds": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Tenant, venue or brand ids for a selected rollout"
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date-time",
    "description": "Scheduled activation; absent means publish now"
   }
  },
  "required": [
   "workflowId",
   "version"
  ]
 },
 "VersioningGovernanceApprovalPublicationView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over approvals.workflow_version (schema WorkflowVersion) (data model for the agreed operations, 29 September)",
  "description": "**What Versioning, Governance, Approval & Publication displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "workflowId": {
    "type": "string",
    "description": "Rule or workflow the version belongs to"
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
    "description": "Approval request id for this version"
   },
   "changedAreas": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "conditions",
      "thresholds",
      "approvers",
      "actions",
      "sla",
      "escalation",
      "integrations"
     ]
    },
    "description": "Areas that differ from the compared version (read-only)"
   },
   "rolloutScope": {
    "type": "string",
    "enum": [
     "allScopes",
     "selectedTenant",
     "selectedVenue",
     "selectedBrand",
     "controlledRollout"
    ],
    "description": "Where the version is published"
   },
   "whoCreated": {
    "type": "string",
    "description": "User who created the version"
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
   "lifecycleStatus": {
    "type": "string",
    "enum": [
     "draft",
     "tested",
     "businessReview",
     "technicalValidation",
     "approval",
     "scheduled",
     "active",
     "suspended",
     "retired"
    ],
    "description": "Version lifecycle status"
   },
   "scopeIds": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Tenant, venue or brand ids for a selected rollout"
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date-time",
    "description": "Scheduled activation; absent means publish now"
   }
  },
  "required": [
   "workflowId",
   "version"
  ]
 },
 "VisualBusinessRuleBuilderInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; writes approvals.business_rule (schema BusinessRule) (data model for the agreed operations, 29 September)",
  "description": "**What Visual Business Rule Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "outcome": {
    "type": "string",
    "enum": [
     "allow",
     "reject",
     "requireApproval",
     "requireAdditionalInformation",
     "applyHold",
     "createTask",
     "generateAlert",
     "startWorkflow",
     "executeApprovedAction"
    ],
    "description": "THEN outcome when the conditions match"
   },
   "businessObjectField": {
    "type": "string",
    "description": "Governed field from a registered module, e.g. Refund.Amount"
   },
   "name": {
    "type": "string",
    "description": "Rule name"
   },
   "operator": {
    "type": "string",
    "enum": [
     "equals",
     "notEquals",
     "greaterThan",
     "lessThan",
     "between",
     "contains",
     "inList",
     "exists",
     "doesNotExist",
     "beforeAfter",
     "percentageThreshold",
     "boolean"
    ],
    "description": "Comparison operator of the condition"
   },
   "ruleId": {
    "type": "string",
    "description": "Rule identifier; absent on input to create a new rule"
   },
   "value": {
    "type": "string",
    "description": "Comparison value"
   },
   "explanation": {
    "type": "string",
    "description": "Plain-language rule explanation"
   }
  },
  "required": [
   "name",
   "businessObjectField",
   "operator",
   "outcome"
  ]
 },
 "VisualBusinessRuleBuilderView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over approvals.business_rule, the row setVisualBusinessRule writes (data model for the agreed operations, 29 September)",
  "description": "**What Visual Business Rule Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "outcome": {
    "type": "string",
    "enum": [
     "allow",
     "reject",
     "requireApproval",
     "requireAdditionalInformation",
     "applyHold",
     "createTask",
     "generateAlert",
     "startWorkflow",
     "executeApprovedAction"
    ],
    "description": "THEN outcome when the conditions match"
   },
   "businessObjectField": {
    "type": "string",
    "description": "Governed field from a registered module, e.g. Refund.Amount"
   },
   "name": {
    "type": "string",
    "description": "Rule name"
   },
   "operator": {
    "type": "string",
    "enum": [
     "equals",
     "notEquals",
     "greaterThan",
     "lessThan",
     "between",
     "contains",
     "inList",
     "exists",
     "doesNotExist",
     "beforeAfter",
     "percentageThreshold",
     "boolean"
    ],
    "description": "Comparison operator of the condition"
   },
   "ruleId": {
    "type": "string",
    "description": "Rule identifier; absent on input to create a new rule"
   },
   "value": {
    "type": "string",
    "description": "Comparison value"
   },
   "explanation": {
    "type": "string",
    "description": "Plain-language rule explanation"
   }
  },
  "required": [
   "name",
   "businessObjectField",
   "operator",
   "outcome"
  ]
 },
 "VisualWorkflowDesignerInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; writes approvals.workflow_definition and a draft approvals.workflow_version (data model for the agreed operations, 29 September)",
  "description": "**What Visual Workflow Designer submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "definition": {
    "type": "string",
    "description": "The workflow graph (nodes and connections) as a JSON document"
   },
   "nodeTypes": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "start",
      "trigger",
      "task",
      "decision",
      "approval",
      "systemAction",
      "notification",
      "wait",
      "timer",
      "parallelBranch",
      "merge",
      "escalation",
      "subWorkflow",
      "end"
     ]
    },
    "description": "Node kinds used in this workflow"
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
   "effectiveFrom": {
    "type": "string",
    "description": "Effective Dates"
   },
   "validationIssues": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "deadEnds",
      "missingOutcomes",
      "circularLoops",
      "missingAssignee",
      "invalidActions"
     ]
    },
    "description": "Design problems the designer found (read-only)"
   },
   "workflowId": {
    "type": "string",
    "description": "Workflow identifier; absent on input to create a new workflow"
   },
   "trigger": {
    "type": "string",
    "description": "What starts the workflow"
   },
   "effectiveTo": {
    "type": "string",
    "format": "date-time",
    "description": "Effective to"
   }
  },
  "required": [
   "workflowName",
   "module",
   "definition"
  ]
 },
 "VisualWorkflowDesignerView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — projection over approvals.workflow_definition and its draft approvals.workflow_version (data model for the agreed operations, 29 September)",
  "description": "**What Visual Workflow Designer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "definition": {
    "type": "string",
    "description": "The workflow graph (nodes and connections) as a JSON document"
   },
   "nodeTypes": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "start",
      "trigger",
      "task",
      "decision",
      "approval",
      "systemAction",
      "notification",
      "wait",
      "timer",
      "parallelBranch",
      "merge",
      "escalation",
      "subWorkflow",
      "end"
     ]
    },
    "description": "Node kinds used in this workflow"
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
   "effectiveFrom": {
    "type": "string",
    "description": "Effective Dates"
   },
   "validationIssues": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "deadEnds",
      "missingOutcomes",
      "circularLoops",
      "missingAssignee",
      "invalidActions"
     ]
    },
    "description": "Design problems the designer found (read-only)"
   },
   "workflowId": {
    "type": "string",
    "description": "Workflow identifier; absent on input to create a new workflow"
   },
   "trigger": {
    "type": "string",
    "description": "What starts the workflow"
   },
   "effectiveTo": {
    "type": "string",
    "format": "date-time",
    "description": "Effective to"
   }
  },
  "required": [
   "workflowName",
   "module",
   "definition"
  ]
 },
 "WorkflowTestingSimulationImpactAnalysisInput": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — request only; the outcome is recorded as approvals.workflow_version test results (data model for the agreed operations, 29 September)",
  "description": "**What Workflow Testing, Simulation & Impact Analysis submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.",
  "properties": {
   "workflowId": {
    "type": "string",
    "description": "Workflow under test"
   },
   "testMode": {
    "type": "string",
    "enum": [
     "manualTestCase",
     "sampleTransaction",
     "historicalReplay",
     "scenarioSimulation",
     "batchTest"
    ],
    "description": "How the workflow is tested"
   },
   "version": {
    "type": "string",
    "description": "Version under test"
   },
   "compareWithVersion": {
    "type": "string",
    "description": "Existing version to compare against for regression"
   },
   "inputPayload": {
    "type": "string",
    "description": "Sample transaction as a JSON document, for manual and sample tests"
   },
   "replayFrom": {
    "type": "string",
    "format": "date",
    "description": "Historical replay start"
   },
   "replayTo": {
    "type": "string",
    "format": "date",
    "description": "Historical replay end"
   }
  },
  "required": [
   "workflowId",
   "testMode"
  ]
 },
 "WorkflowTestingSimulationImpactAnalysisView": {
  "type": "object",
  "x-ticvai-drafted-shape": true,
  "x-ticvai-persistence": "none — computed by simulation over approvals.workflow_version and the rules it calls; never executes actions (data model for the agreed operations, 29 September)",
  "description": "**What Workflow Testing, Simulation & Impact Analysis displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.",
  "properties": {
   "workflowId": {
    "type": "string",
    "description": "Workflow under test"
   },
   "testMode": {
    "type": "string",
    "enum": [
     "manualTestCase",
     "sampleTransaction",
     "historicalReplay",
     "scenarioSimulation",
     "batchTest"
    ],
    "description": "How the workflow is tested"
   },
   "rulesEvaluated": {
    "type": "integer",
    "description": "Rules Evaluated"
   },
   "conditionsMatched": {
    "type": "integer",
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
   },
   "version": {
    "type": "string",
    "description": "Version under test"
   },
   "compareWithVersion": {
    "type": "string",
    "description": "Existing version to compare against for regression"
   },
   "inputPayload": {
    "type": "string",
    "description": "Sample transaction as a JSON document, for manual and sample tests"
   },
   "replayFrom": {
    "type": "string",
    "format": "date",
    "description": "Historical replay start"
   },
   "replayTo": {
    "type": "string",
    "format": "date",
    "description": "Historical replay end"
   }
  },
  "required": [
   "workflowId",
   "testMode"
  ]
 }
}
```
