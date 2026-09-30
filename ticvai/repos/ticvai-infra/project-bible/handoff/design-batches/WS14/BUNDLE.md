# WS14 — Approval Workflows and Governance board 2

**9 screens · 8 operations · 16 schemas · 4 permissions**

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
  `APPROVAL_CONFIGURE, APPROVAL_VIEW, GUEST_VIEW, PRODUCT_CONFIGURE`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-319` | Approval Workflow Library | listDetail | 2 | 0 | — |
| `ADM-320` | Create Approval Workflow | configEditor | 1 | 0 | — |
| `ADM-322` | Approval Stage Configuration | configEditor | 1 | 0 | — |
| `ADM-323` | Condition & Decision Rule Builder | listDetail | 2 | 0 | — |
| `ADM-324` | Approval Sequence & Parallel Routing | listDetail | 1 | 0 | — |
| `ADM-325` | Workflow Outcome & Action Configuration | listDetail | 1 | 0 | — |
| `ADM-326` | Workflow Validation & Simulation | listDetail | 1 | 0 | — |
| `ADM-327` | Workflow Publication & Lifecycle | configEditor | 2 | 0 | — |
| `ADM-328` | Workflow Versioning & Change History | listDetail | 2 | 0 | — |

## Thin screens in this batch

**ADM-319, ADM-322, ADM-323, ADM-324, ADM-325, ADM-326, ADM-328 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-319",
  "name": "Approval Workflow Library",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "2",
   "number": "1",
   "page": 11
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/approval-workflow-library-adm-319",
   "component": "apps/ticvai-web/src/routes/platform/ApprovalWorkflowLibrary.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "exitTo": [
    "ADM-002",
    "ADM-241",
    "ADM-320",
    "ADM-322",
    "ADM-323",
    "ADM-324",
    "ADM-325",
    "ADM-326",
    "ADM-327",
    "ADM-328"
   ],
   "transitions": [
    {
     "to": "ADM-002",
     "trigger": "Back to Platform Dashboard",
     "provenance": "structural — pack board 2 wiring, 9 September 2026",
     "back": true
    },
    {
     "to": "ADM-328",
     "trigger": "Workflow Versioning & Change History",
     "provenance": "structural — pack board 2 wiring, 9 September 2026"
    },
    {
     "to": "ADM-320",
     "trigger": "Create Approval Workflow",
     "provenance": "structural — pack board 2 wiring, 9 September 2026"
    },
    {
     "to": "ADM-241",
     "trigger": "Visual Workflow Designer",
     "provenance": "structural — pack board 2 wiring, 9 September 2026"
    },
    {
     "to": "ADM-322",
     "trigger": "Approval Stage Configuration",
     "provenance": "structural — pack board 2 wiring, 9 September 2026"
    },
    {
     "to": "ADM-323",
     "trigger": "Condition & Decision Rule Builder",
     "provenance": "structural — pack board 2 wiring, 9 September 2026"
    },
    {
     "to": "ADM-324",
     "trigger": "Approval Sequence & Parallel Routing",
     "provenance": "structural — pack board 2 wiring, 9 September 2026"
    },
    {
     "to": "ADM-325",
     "trigger": "Workflow Outcome & Action Configuration",
     "provenance": "structural — pack board 2 wiring, 9 September 2026"
    },
    {
     "to": "ADM-326",
     "trigger": "Workflow Validation & Simulation",
     "provenance": "structural — pack board 2 wiring, 9 September 2026"
    },
    {
     "to": "ADM-327",
     "trigger": "Workflow Publication & Lifecycle",
     "provenance": "structural — pack board 2 wiring, 9 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Provide a centralized directory of every approval workflow configured within the tenant.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 11"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 11"
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
       "impliedBy": "listRuleWorkflow",
       "bindsTo": "RulesWorkflowCommandCenterView",
       "operation": "listRuleWorkflow",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "approveWorkflow",
       "label": "Approve workflow",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "approveWorkflow"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The approval workflow list.",
   "error": "Could not load. Names which read failed and leaves the approval workflow untouched.",
   "emptyFirstRun": "No approval workflow yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the approval workflow are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listRuleWorkflow",
    "contract": "approvals",
    "purpose": "Every approval workflow definition",
    "trigger": "onLoad",
    "provenance": "decided 29 September, readiness close-out (QA wiring note)"
   },
   {
    "operationId": "approveWorkflow",
    "contract": "catalogue",
    "purpose": "Approval Workflow Designer",
    "trigger": "onAction"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-319",
   "workshopBoard": "wireframes/WS31 Approval Workflows and Governance Board 2.dc.html#adm-319"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 11. 0 of 0 labels bound to a contract property; 0 of 15 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-320",
  "name": "Create Approval Workflow",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "2",
   "number": "2",
   "page": 12
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/create-approval-workflow-adm-320",
   "component": "apps/ticvai-web/src/routes/platform/CreateApprovalWorkflow.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-319"
   ],
   "exitTo": [
    "ADM-319"
   ],
   "transitions": [
    {
     "to": "ADM-319",
     "trigger": "Back to Approval Workflow Library",
     "provenance": "structural — pack board 2 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population",
  "purpose": "Provide a guided setup wizard for creating a new approval workflow. Step 1 — Basic Information",
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
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 12 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Description",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 12 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Business Process",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 12 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Source Module",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 12 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Request Type",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 12 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Tenant",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 12 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Department",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 12 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 12 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Workflow Owner",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 12 §Configure"
      },
      {
       "kind": "textField",
       "label": "Step 2 — Applicability",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 12 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Require approval",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 12 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Allow automatic approval",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 12 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Allow delegation",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 12 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Allow escalation",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 12 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Require comments",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 12 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Require rejection reason",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 12 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Require MFA",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 12 §Configure"
      },
      {
       "kind": "selectField",
       "label": "Require digital signature",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 12 §Configure"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The create approval workflow configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the create approval workflow untouched.",
   "emptyFirstRun": "No create approval workflow configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setVisualWorkflow",
    "contract": "approvals",
    "purpose": "Create the workflow",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listWorkflow"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-320",
   "workshopBoard": "wireframes/WS31 Approval Workflows and Governance Board 2.dc.html#adm-320"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 12. 0 of 0 labels bound to a contract property; 18 of 27 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-322",
  "name": "Approval Stage Configuration",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "2",
   "number": "4",
   "page": 14
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/approval-stage-configuration-adm-322",
   "component": "apps/ticvai-web/src/routes/platform/ApprovalStageConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-319"
   ],
   "exitTo": [
    "ADM-319"
   ],
   "transitions": [
    {
     "to": "ADM-319",
     "trigger": "Back to Approval Workflow Library",
     "provenance": "structural — pack board 2 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configuration) and no display directory — it is settings, not a population",
  "purpose": "Configure each approval stage in detail. When the administrator clicks an Approval Node in Screen 3, this screen/panel opens.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "textField",
       "label": "Stage Name: Finance Manager Approval",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 14 §Configuration"
      },
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "setVisualWorkflow",
       "label": "Save visual workflow",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setVisualWorkflow"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The approval stage configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the approval stage untouched.",
   "emptyFirstRun": "No approval stage configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setVisualWorkflow",
    "contract": "approvals",
    "purpose": "Stages and approvers",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listWorkflow"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-322",
   "workshopBoard": "wireframes/WS31 Approval Workflows and Governance Board 2.dc.html#adm-322"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 14. 0 of 0 labels bound to a contract property; 1 of 13 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-323",
  "name": "Condition & Decision Rule Builder",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "2",
   "number": "5",
   "page": 15
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/condition-decision-rule-builder-adm-323",
   "component": "apps/ticvai-web/src/routes/platform/ConditionDecisionRuleBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-319"
   ],
   "exitTo": [
    "ADM-319"
   ],
   "transitions": [
    {
     "to": "ADM-319",
     "trigger": "Back to Approval Workflow Library",
     "provenance": "structural — pack board 2 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow administrators to determine when a particular approval path should apply. The rule builder should use business-friendly configuration rather than programming.",
  "gaps": [
   {
    "operation": null,
    "why": "**Condition & Decision Rule Builder declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 15"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 15"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "setVisualBusinessRule",
       "label": "Save visual business rule",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listConditionDecisionLogic",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
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
   "loading": "The condition decision rule list.",
   "error": "Could not load. Names which read failed and leaves the condition decision rule untouched.",
   "emptyFirstRun": "No condition decision rule yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the condition decision rule are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setVisualBusinessRule",
    "contract": "approvals",
    "purpose": "Conditions and decision rules",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listConditionDecisionLogic"
    ]
   },
   {
    "operationId": "listConditionDecisionLogic",
    "contract": "approvals",
    "purpose": "Rules already defined",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-323",
   "workshopBoard": "wireframes/WS31 Approval Workflows and Governance Board 2.dc.html#adm-323"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 15. 0 of 0 labels bound to a contract property; 0 of 22 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-324",
  "name": "Approval Sequence & Parallel Routing",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "2",
   "number": "6",
   "page": 16
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/approval-sequence-parallel-routing-adm-324",
   "component": "apps/ticvai-web/src/routes/platform/ApprovalSequenceParallelRouting.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-319"
   ],
   "exitTo": [
    "ADM-319"
   ],
   "transitions": [
    {
     "to": "ADM-319",
     "trigger": "Back to Approval Workflow Library",
     "provenance": "structural — pack board 2 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure complex multi-level approval structures.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 16"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 16"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "setVisualWorkflow",
       "label": "Save visual workflow",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setVisualWorkflow"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The approval sequence parallel list.",
   "error": "Could not load. Names which read failed and leaves the approval sequence parallel untouched.",
   "emptyFirstRun": "No approval sequence parallel yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the approval sequence parallel are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setVisualWorkflow",
    "contract": "approvals",
    "purpose": "Sequence and parallel routing",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listWorkflow"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-324",
   "workshopBoard": "wireframes/WS31 Approval Workflows and Governance Board 2.dc.html#adm-324"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 16. 0 of 0 labels bound to a contract property; 0 of 12 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-325",
  "name": "Workflow Outcome & Action Configuration",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "2",
   "number": "7",
   "page": 16
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/workflow-outcome-action-configuration-adm-325",
   "component": "apps/ticvai-web/src/routes/platform/WorkflowOutcomeActionConfiguration.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-319"
   ],
   "exitTo": [
    "ADM-319"
   ],
   "transitions": [
    {
     "to": "ADM-319",
     "trigger": "Back to Approval Workflow Library",
     "provenance": "structural — pack board 2 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Define what TICVAI should actually do after the approval process reaches an outcome. This is important because approval and execution should be separated.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 16"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 16"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "setTriggerActionCross",
       "label": "Save trigger action cross",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setTriggerActionCross"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The workflow outcome action list.",
   "error": "Could not load. Names which read failed and leaves the workflow outcome action untouched.",
   "emptyFirstRun": "No workflow outcome action yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the workflow outcome action are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setTriggerActionCross",
    "contract": "approvals",
    "purpose": "What happens on each outcome",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listCrossModuleOrchestration"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-325",
   "workshopBoard": "wireframes/WS31 Approval Workflows and Governance Board 2.dc.html#adm-325"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 16. 0 of 0 labels bound to a contract property; 0 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-326",
  "name": "Workflow Validation & Simulation",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "2",
   "number": "8",
   "page": 17
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/workflow-validation-simulation-adm-326",
   "component": "apps/ticvai-web/src/routes/platform/WorkflowValidationSimulation.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-319"
   ],
   "exitTo": [
    "ADM-319"
   ],
   "transitions": [
    {
     "to": "ADM-319",
     "trigger": "Back to Approval Workflow Library",
     "provenance": "structural — pack board 2 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow administrators to test workflows before putting them into production. This is something I strongly recommend adding to the UX because these workflows can directly affect money, access and customer operations.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 17"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 17"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "simulateWorkflowTestingImpact",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "simulateWorkflowTestingImpact"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The workflow validation simulation list.",
   "error": "Could not load. Names which read failed and leaves the workflow validation simulation untouched.",
   "emptyFirstRun": "No workflow validation simulation yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the workflow validation simulation are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "simulateWorkflowTestingImpact",
    "contract": "approvals",
    "purpose": "Simulate before publishing",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-326",
   "workshopBoard": "wireframes/WS31 Approval Workflows and Governance Board 2.dc.html#adm-326"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 17. 0 of 0 labels bound to a contract property; 0 of 24 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-327",
  "name": "Workflow Publication & Lifecycle",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "2",
   "number": "9",
   "page": 18
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/workflow-publication-lifecycle-adm-327",
   "component": "apps/ticvai-web/src/routes/platform/WorkflowPublicationLifecycle.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-319"
   ],
   "exitTo": [
    "ADM-319"
   ],
   "transitions": [
    {
     "to": "ADM-319",
     "trigger": "Back to Approval Workflow Library",
     "provenance": "structural — pack board 2 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "configEditor",
  "patternReason": "the pack gives this screen a configuration directory (§Configuration) and no display directory — it is settings, not a population",
  "purpose": "Govern the transition of workflow configurations into production.",
  "layout": {
   "template": "form",
   "regions": [
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Effective From",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 18 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Effective Until",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 18 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Tenant",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 18 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Venue",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 18 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Deployment scope",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 18 §Configuration"
      },
      {
       "kind": "selectField",
       "label": "Activation schedule",
       "provenance": "pack Approval_Workflows_and_Governance_Reference.pdf, page 18 §Configuration"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The workflow publication lifecycle configuration as saved.",
   "error": "Could not load. Names which read failed and leaves the workflow publication lifecycle untouched.",
   "emptyFirstRun": "No workflow publication lifecycle configured yet. Carries the create action and says what the platform does in the meantime.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listRuleWorkflow",
    "contract": "approvals",
    "purpose": "The workflow definitions and their lifecycle",
    "trigger": "onLoad",
    "provenance": "decided 29 September, readiness close-out (QA wiring note)"
   },
   {
    "operationId": "setVisualWorkflow",
    "contract": "approvals",
    "purpose": "Publish",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026",
    "invalidates": [
     "listWorkflow"
    ]
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-327",
   "workshopBoard": "wireframes/WS31 Approval Workflows and Governance Board 2.dc.html#adm-327"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 18. 0 of 0 labels bound to a contract property; 6 of 20 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "ADM-328",
  "name": "Workflow Versioning & Change History",
  "module": "Platform",
  "requiresModule": "core",
  "wave": 3,
  "source": {
   "pack": "Approval_Workflows_and_Governance_Reference.pdf",
   "board": "2",
   "number": "10",
   "page": 19
  },
  "implementation": {
   "app": "ticvai-web",
   "route": "/platform/workflow-versioning-change-history-adm-328",
   "component": "apps/ticvai-web/src/routes/platform/WorkflowVersioningChangeHistory.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-319"
   ],
   "exitTo": [
    "ADM-319"
   ],
   "transitions": [
    {
     "to": "ADM-319",
     "trigger": "Back to Approval Workflow Library",
     "provenance": "structural — pack board 2 wiring, 9 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Maintain complete governance over changes made to approval workflows. The matrix specifically requires Approval Workflow Versioning.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 19"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Approval_Workflows_and_Governance_Reference.pdf, page 19"
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
       "impliedBy": "listVersioningEffectiveDate",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The workflow versioning change list.",
   "error": "Could not load. Names which read failed and leaves the workflow versioning change untouched.",
   "emptyFirstRun": "No workflow versioning change yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the workflow versioning change are still there. The pack's own statuses are n By — the state names which is selected.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listVersioningEffectiveDate",
    "contract": "marketing-crm",
    "purpose": "Version history",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listRuleWorkflow",
    "contract": "approvals",
    "purpose": "The workflow being versioned",
    "trigger": "onLoad",
    "provenance": "decided 29 September, readiness close-out (QA wiring note)"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-328",
   "workshopBoard": "wireframes/WS31 Approval Workflows and Governance Board 2.dc.html#adm-328"
  },
  "apisNote": "Regenerated 9 September 2026 from Approval_Workflows_and_Governance_Reference.pdf page 19. 0 of 0 labels bound to a contract property; 2 of 12 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
 "listVersioningEffectiveDate": {
  "method": "GET",
  "path": "/versioning-effective-date",
  "contract": "marketing-crm",
  "summary": "Versioning, Effective Dates & Legal Change Control",
  "permission": "GUEST_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "formId",
    "in": "query",
    "required": false
   },
   {
    "name": "compareWith",
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
 "VersioningEffectiveDatesLegalChangeControlView": {
  "type": "object",
  "x-ticvai-persistence": "none — projection over marketing.form_definition, marketing.waiver_version_control (new), marketing.form_submission and marketing.waiver_signature",
  "description": "One version of one waiver and its change control (pack 11.1.8).",
  "required": [
   "formId",
   "versionNumber",
   "status",
   "createdAt"
  ],
  "properties": {
   "formId": {
    "type": "string",
    "format": "uuid"
   },
   "waiverName": {
    "type": "string"
   },
   "versionNumber": {
    "type": "integer",
    "minimum": 1
   },
   "status": {
    "type": "string",
    "enum": [
     "draft",
     "published",
     "superseded",
     "retired"
    ],
    "description": "`FormDefinition.status` (states/form-definition.yaml)."
   },
   "lifecycleStatus": {
    "type": "string",
    "enum": [
     "draft",
     "review",
     "pendingApproval",
     "approved",
     "scheduled",
     "published",
     "suspended",
     "expired",
     "archived"
    ]
   },
   "createdByUserId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "changeReason": {
    "type": "string",
    "maxLength": 1000,
    "nullable": true
   },
   "legalReviewer": {
    "type": "string",
    "nullable": true,
    "description": "`FormDefinition.legalReviewedBy`."
   },
   "legalReviewedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "approvedByUserId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "approvedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "effectiveFrom": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "effectiveTo": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "resignRule": {
    "type": "string",
    "enum": [
     "noResign",
     "resignAtNextBooking",
     "resignBeforeNextVisit"
    ],
    "description": "Whether people who signed an earlier version must sign this one."
   },
   "suspended": {
    "type": "boolean",
    "default": false
   },
   "suspensionReason": {
    "type": "string",
    "maxLength": 500,
    "nullable": true
   },
   "signatureCount": {
    "type": "integer",
    "minimum": 0,
    "description": "Signatures taken against this exact version."
   },
   "comparison": {
    "type": "object",
    "nullable": true,
    "description": "Present when `compareWith` is given.",
    "properties": {
     "comparedWithVersion": {
      "type": "integer",
      "minimum": 1
     },
     "addedText": {
      "type": "array",
      "items": {
       "type": "object",
       "properties": {
        "blockKey": {
         "type": "string"
        },
        "language": {
         "type": "string"
        },
        "text": {
         "type": "string"
        }
       }
      }
     },
     "removedText": {
      "type": "array",
      "items": {
       "type": "object",
       "properties": {
        "blockKey": {
         "type": "string"
        },
        "language": {
         "type": "string"
        },
        "text": {
         "type": "string"
        }
       }
      }
     },
     "changedQuestions": {
      "type": "array",
      "items": {
       "type": "string"
      },
      "description": "Field keys added, removed or changed."
     },
     "changedSignatoryRules": {
      "type": "array",
      "items": {
       "type": "string"
      },
      "description": "Names of the signatory-rule properties that differ."
     },
     "changedAssociations": {
      "type": "array",
      "items": {
       "type": "string",
       "format": "uuid"
      },
      "description": "Associations added, removed or changed between the two versions' publication."
     }
    }
   }
  }
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
